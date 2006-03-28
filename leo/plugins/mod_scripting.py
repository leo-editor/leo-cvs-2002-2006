#@+leo-ver=4-thin
#@+node:ekr.20060328125248:@thin mod_scripting.py
#@<< docstring >>
#@+node:ekr.20060328125248.1:<< docstring >>
"""A plugin to create script buttons and @button, @command, @plugin and @script nodes.

This plugin puts two buttons in the icon area: a button called 'run Script' and
a button called 'script Button'.

The 'run Script' button is simply another way of doing the Execute Script
command: it executes the selected text of the presently selected node, or the
entire text if no text is selected.

The 'script Button' button creates another button in the icon area every time
you push it. The name of the button is the headline of the presently selected
node. Hitting this *newly created* button executes the button's script.

For example, to run a script on any part of an outline do the following:

1.  Select the node containing the script.  Suppose its headline is X
2.  Press the scriptButton button.  This will create a new button called X.
3.  Select the node on which you want to run the script.
4.  Push button X.

That's all.  You can delete a script button by right-clicking on it.

This plugin optionally scans for @button nodes, @command, @plugin nodes and
@script nodes whenever a .leo file is opened.

- @button nodes create script buttons.
- @command nodes create minibuffer commands.
- @plugin nodes cause plugins to be loaded.
- @script nodes cause a script to be executed when opening a .leo file.

Such nodes may be security risks. This plugin scans for such nodes only if the
corresponding atButtonNodes, atPluginNodes, and atScriptNodes constants are set
to True in this plugin.

You can bind key shortcuts to @button and @command nodes as follows:

@button name @key=shortcut

This binds the shortcut to the script in the script button. The button's name is
'name', but you can see the full headline in the status line when you move the
mouse over the button.

@command name @key=shortcut

This creates a new minibuffer command and binds shortcut to it.

This plugin is based on ideas from e's dynabutton plugin.   
"""
#@nonl
#@-node:ekr.20060328125248.1:<< docstring >>
#@nl
#@<< imports >>
#@+node:ekr.20060328125248.2:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

import sys
#@nonl
#@-node:ekr.20060328125248.2:<< imports >>
#@nl

__version__ = "0.20"
#@<< version history >>
#@+node:ekr.20060328125248.3:<< version history >>
#@+at
# 
# 0.3 EKR: Don't mess with button sizes or fonts on MacOs/darwin
# 0.4 EKR: Added support for @button, @script and @plugin.
# 0.5 EKR: Added patch by Davide Salomoni: added start2 hook and related code.
# 0.5 EKR: Use g.importExtention to import Tk.
# 0.6.1 EKR: Improved docstring.
# 0.7 EKR:
# - Added support for 'removeMe' hack.
#     Buttons can asked to be removed by setting s.app.scriptDict['removeMe'] 
# = True.
# 0.8 EKR: c.disableCommandsMessage disables buttons.
# 0.9 EKR:
# - Added init, onCreate.
# - Created scriptingController class.
# 0.10 EKR: Changed 'new_c' logic to 'c' logic.
# 0.11 EKR:
# - Removed bindLate options: it should always be on.
# - Added support for:
#     - @button name [@key=shortcut]
#     - @command name [@key=shortcut]
# 0.12 EKR:
# - Use c.executeScript(p=p,silent=True) in @command so the
#   'end of script' message doesn't switch tabs.
# 0.13 EKR: Use set silent=True in all calls to c.executeScript except for the 
# 'Run Script' button.
# 0.14 EKR: All created buttons call bodyWantsFocus when the script completes.
# 0.15 EKR: Fixed a recent crasher in deleteButton.
# 0.16 EKR:
# - Removed the unused bindLate global.
# - Set silent=True in the Run Script callback.
# 0.17 EKR: Added calls to c.updateScreen.
# 0.18 EKR:
# - Removed calls to c.updateScreen and c.frame.bodyWantsFocus.
#   These calls would shift focus improperly when opening a new window.
# 0.19 btheado: Refactored the code in scriptingController to remove 
# duplication.
# 0.20 EKR: converted to @thin.
#@-at
#@nonl
#@-node:ekr.20060328125248.3:<< version history >>
#@nl

atButtonNodes = True
    # True: adds a button for every @button node.
atCommandsNodes = True
    # True: define a minibuffer command for every @command node.
atPluginNodes = False
    # True: dynamically loads plugins in @plugins nodes when a window is created.
atScriptNodes = False
    # True: dynamically executes script in @script nodes when a window is created.  DANGEROUS!
maxButtonSize = 18
    # Maximum length of button names.

#@+others
#@+node:ekr.20060328125248.4:init
def init ():
    
    ok = Tk and not g.app.unitTesting
    
    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)
            
        ok = g.app.gui.guiName() == "tkinter"

        if ok:
            # Note: call onCreate _after_ reading the .leo file.
            # That is, the 'after-create-leo-frame' hook is too early!
            leoPlugins.registerHandler(('new','open2'),onCreate)
            g.plugin_signon(__name__)
        
    return ok
#@nonl
#@-node:ekr.20060328125248.4:init
#@+node:ekr.20060328125248.5:onCreate
def onCreate (tag, keys):

    """Handle the onCreate event in the mod_scripting plugin."""
    
    c = keys.get('c')

    if c:
        sc = scriptingController(c)
        sc.createAllButtons()
#@nonl
#@-node:ekr.20060328125248.5:onCreate
#@+node:ekr.20060328125248.6:class scriptingController
class scriptingController:
    
    #@    @+others
    #@+node:ekr.20060328125248.7: ctor
    def __init__ (self,c,iconBar=None):
        
        self.c = c
        self.scanned = False
        if not iconBar:
            self.iconBar = c.frame.getIconBarObject()
        else:
            self.iconBar = iconBar
    #@nonl
    #@-node:ekr.20060328125248.7: ctor
    #@+node:ekr.20060328125248.8:createAllButtons
    def createAllButtons (self):
    
        global atButtonNodes,atPluginNodes,atScriptNodes
        
        c = self.c
    
        if not self.scanned: # Not really needed, but can't hurt.
            self.scanned = True
            self.createRunScriptIconButton()
            self.createScriptButtonIconButton()
    
            # scan for user-defined nodes.
            for p in c.allNodes_iter():
                if atButtonNodes and p.headString().startswith("@button"):
                    self.createAtButtonButton(p)
                if atCommandsNodes and p.headString().startswith("@command"):
                    self.createMinibufferCommand(p)
                if atPluginNodes and p.headString().startswith("@plugin"):
                    self.loadPlugin(p)
                if atScriptNodes and p.headString().startswith("@script"):
                    self.executeScriptNode(p)
    #@nonl
    #@-node:ekr.20060328125248.8:createAllButtons
    #@+node:ekr.20060328125248.9:Handlers for the "At scanner"
    #@+node:ekr.20060328125248.10:createMinibufferCommand (New in 4.4)
    def createMinibufferCommand (self,p):
        
        '''Register a minibuffer command.
        
        p.headString has the form @command name [@key=shortcut].'''
        
        c = self.c ; k = c.keyHandler ; h = p.headString()
        if not h.strip(): return
        
        #@    << get the commandName and optional shortcut >>
        #@+node:ekr.20060328125248.11:<< get the commandName and optional shortcut >>
        tag = '@command' ; shortcut = None
        
        i = h.find('@key')
        
        if i > -1:
            commandName = h[len(tag):i].strip()
            j = g.skip_ws(h,i+len('@key'))
            if g.match(h,j,'='):
                shortcut = h[j+1:].strip()
        else:
            commandName = h[len(tag):].strip()
            
        # g.trace(commandName,'shortcut',shortcut)
        #@nonl
        #@-node:ekr.20060328125248.11:<< get the commandName and optional shortcut >>
        #@nl
    
        def atCommandCallback (event=None,c=c,p=p.copy()):
            # The 'end-of-script command messes up tabs.
            c.executeScript(p=p,silent=True)
    
        k.registerCommand(commandName,shortcut,atCommandCallback)
    #@nonl
    #@-node:ekr.20060328125248.10:createMinibufferCommand (New in 4.4)
    #@+node:ekr.20060328125248.12:createAtButtonButton (Improved for 4.4)
    def createAtButtonButton (self,p):
        
        '''Create a button in the icon area for an @button node.
        
        An optional @key=shortcut defines a shortcut that is bound to the button's script.
        The @key=shortcut does not appear in the button's name, but
        it *does* appear in the statutus line shown when the mouse moves over the button.'''
    
        c = self.c ; h = p.headString()
        buttonText = self.getButtonText(h)
        shortcut = self.getShortcut(h)
        statusLine = "Script button: %s" % buttonText
        if shortcut:
            statusLine = statusLine + " @key=" + shortcut
        b = self.createAtButtonIconButton(p,buttonText,statusLine,shortcut)
    #@-node:ekr.20060328125248.12:createAtButtonButton (Improved for 4.4)
    #@+node:ekr.20060328125248.13:loadPlugin
    def loadPlugin (self,p):
        
        global atPluginNodes
        
        c = self.c
        tag = "@plugin"
        h = p.headString()
        assert(g.match(h,0,tag))
        
        # Get the name of the module.
        theFile = h[len(tag):].strip()
        if theFile[-3:] == ".py":
            theFile = theFile[:-3]
        theFile = g.toUnicode(theFile,g.app.tkEncoding)
        
        if not atPluginNodes:
            g.es("disabled @plugin: %s" % (theFile),color="blue")
        elif theFile in g.app.loadedPlugins:
            g.es("plugin already loaded: %s" % (theFile),color="blue")
        else:
            plugins_path = g.os_path_join(g.app.loadDir,"..","plugins")
            theModule = g.importFromPath(theFile,plugins_path,
                pluginName=__name__,verbose=False)
            if theModule:
                g.es("plugin loaded: %s" % (theFile),color="blue")
                g.app.loadedPlugins.append(theFile)
            else:
                g.es("can not load plugin: %s" % (theFile),color="blue")
    #@nonl
    #@-node:ekr.20060328125248.13:loadPlugin
    #@+node:ekr.20060328125248.14:executeScriptNode
    def executeScriptNode (self,p):
        
        global atPluginNodes
        
        c = self.c
        tag = "@script"
        h = p.headString()
        assert(g.match(h,0,tag))
        name = h[len(tag):].strip()
    
        if atPluginNodes:
            g.es("executing script %s" % (name),color="blue")
            c.executeScript(p,useSelectedText=False,silent=True)
        else:
            g.es("disabled @script: %s" % (name),color="blue")
    
        if 0:
            # Do not assume the script will want to remain in this commander.
            c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20060328125248.14:executeScriptNode
    #@-node:ekr.20060328125248.9:Handlers for the "At scanner"
    #@+node:ekr.20060328125248.15:getButtonText
    def getButtonText(self,h):
        
        '''Returns the button text found in the given headline string'''
        
        tag = "@button"
        if h.startswith(tag):
            h = h[len(tag):].strip()
        
        i = h.find('@key')
    
        if i > -1:
            buttonText = h[:i].strip()
        
        else:
            buttonText = h
        
        fullButtonText = buttonText
        buttonText = buttonText[:maxButtonSize]
        return buttonText
    #@nonl
    #@-node:ekr.20060328125248.15:getButtonText
    #@+node:ekr.20060328125248.16:getShortcut
    def getShortcut(self,h):
        
        '''Returns the keyboard shortcut from the given headline string'''
        
        shortcut = None
        i = h.find('@key')
    
        if i > -1:
            j = g.skip_ws(h,i+len('@key'))
            if g.match(h,j,'='):
                shortcut = h[j+1:].strip()
    
        return shortcut
    #@nonl
    #@-node:ekr.20060328125248.16:getShortcut
    #@+node:ekr.20060328125248.17:createIconButton
    def createIconButton (self,text,statusLine,bg):
        b = self.iconBar.add(text=text)
        if sys.platform == "win32":
            width = int(len(text) * 0.9)
            b.configure(width=width,font=('verdana',7,'bold'),bg=bg)
        #@    << define enter/leave callbacks >>
        #@+node:ekr.20060328125248.18:<< define enter/leave callbacks >>
        def mouseEnterCallback(event=None,self=self,statusLine=statusLine):
            self.mouseEnter(statusLine)
        
        def mouseLeaveCallback(event=None,self=self):
            self.mouseLeave()
        #@nonl
        #@-node:ekr.20060328125248.18:<< define enter/leave callbacks >>
        #@nl
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
        return b
    #@nonl
    #@-node:ekr.20060328125248.17:createIconButton
    #@+node:ekr.20060328125248.19:Default buttons
    #@+node:ekr.20060328125248.20:createRunScriptIconButton
    def createRunScriptIconButton (self):
        b = self.createIconButton('Run Script', 'Run script in current node', bg='MistyRose1')
        #@    << define runScriptCommand >>
        #@+node:ekr.20060328125248.21:<< define runScriptCommand >>
        def runScriptCommand (event=None):
            
            '''Called when user presses the 'Run Script' button.'''
        
            c = self.c
            c.executeScript(c.currentPosition(),useSelectedText=True,silent=True)
            
            if 0:
                # Do not assume the script will want to remain in this commander.
                c.frame.bodyWantsFocus()
        #@nonl
        #@-node:ekr.20060328125248.21:<< define runScriptCommand >>
        #@nl
        b.configure(command=runScriptCommand)
        return b
    #@nonl
    #@-node:ekr.20060328125248.20:createRunScriptIconButton
    #@+node:ekr.20060328125248.22:createScriptButtonIconButton
    def createScriptButtonIconButton (self):
        b = self.createIconButton('Script Button', 'Make script button current node', bg="#ffffcc")
        #@    << define addScriptButtonCommand >>
        #@+node:ekr.20060328125248.23:<< define addScriptButtonCommand >>
        def addScriptButtonCommand (event=None,self=self):
            c = self.c ; p = c.currentPosition(); h = p.headString()
            buttonText = self.getButtonText(h)
            shortcut = self.getShortcut(h)
            statusLine = "Run Script: %s" % buttonText
            if shortcut:
                statusLine = statusLine + " @key=" + shortcut
            b = self.createAtButtonIconButton(p,buttonText,statusLine,shortcut,'MistyRose1')
            c.frame.bodyWantsFocus()
        #@nonl
        #@-node:ekr.20060328125248.23:<< define addScriptButtonCommand >>
        #@nl
        b.configure(command=addScriptButtonCommand)
        return b
    #@nonl
    #@-node:ekr.20060328125248.22:createScriptButtonIconButton
    #@-node:ekr.20060328125248.19:Default buttons
    #@+node:ekr.20060328125248.24:createAtButtonIconButton
    def createAtButtonIconButton (self,p,buttonText,statusLine,shortcut,bg='LightSteelBlue1'):
        b = self.createIconButton(text=buttonText,statusLine=statusLine,bg=bg)
        def deleteButtonCallback(event=None,self=self,b=b):
            self.deleteButton(b)
        def atButtonCallback (event=None,self=self,p=p.copy(),b=b,buttonText=buttonText):
            self.executeScriptFromCallback (p,b,buttonText)
        b.configure(command=atButtonCallback)
        b.bind('<3>',deleteButtonCallback)
        if shortcut:
            #@        << bind the shortcut to atButtonCallback >>
            #@+node:ekr.20060328125248.25:<< bind the shortcut to atButtonCallback >>
            c = self.c; k = c.keyHandler ; func = atButtonCallback
            
            #shortcut, junk = c.frame.menu.canonicalizeShortcut(shortcut)
            shortcut = k.canonicalizeShortcut(shortcut)
            ok = k.bindKey ('all', shortcut,func,buttonText)
            
            if ok:
                g.es_print('Bound @button %s to %s' % (buttonText,shortcut),color='blue')
            #@nonl
            #@-node:ekr.20060328125248.25:<< bind the shortcut to atButtonCallback >>
            #@nl
        return b
    #@-node:ekr.20060328125248.24:createAtButtonIconButton
    #@+node:ekr.20060328125248.26:deleteButton
    def deleteButton(self,button):
        
        """Delete the given button."""
    
        if button:
            button.pack_forget()
            # button.destroy()
            
        self.c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20060328125248.26:deleteButton
    #@+node:ekr.20060328125248.27:mouseEnter/Leave
    def mouseEnter(self,status):
    
        self.c.frame.clearStatusLine()
        self.c.frame.putStatusLine(status)
        
    def mouseLeave(self):
    
        self.c.frame.clearStatusLine()
    #@nonl
    #@-node:ekr.20060328125248.27:mouseEnter/Leave
    #@+node:ekr.20060328125248.28:executeScriptFromCallback
    def executeScriptFromCallback (self,p,b,buttonText):
        
        '''Called from callbacks to execute the script in node p.'''
        
        c = self.c
    
        if c.disableCommandsMessage:
            g.es(c.disableCommandsMessage,color='blue')
        else:
            #c.frame.clearStatusLine()
            #c.frame.putStatusLine("Executing button: %s..." % buttonText)
            g.app.scriptDict = {}
            c.executeScript(p=p,silent=True)
            # Remove the button if the script asks to be removed.
            if g.app.scriptDict.get('removeMe'):
                g.es("Removing '%s' button at its request" % buttonText)
                b.pack_forget()
              
        if 0: # Do not assume the script will want to remain in this commander.
            c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20060328125248.28:executeScriptFromCallback
    #@-others
#@nonl
#@-node:ekr.20060328125248.6:class scriptingController
#@-others
#@nonl
#@-node:ekr.20060328125248:@thin mod_scripting.py
#@-leo
