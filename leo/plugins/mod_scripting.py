#@+leo-ver=4-thin
#@+node:EKR.20040613213623:@thin mod_scripting.py
#@<< docstring >>
#@+node:ekr.20050130155124:<< docstring >>
"""A plugin to create script buttons and @button, @command, @plugin and @script nodes.

This plugin puts two buttons in the icon area: a button called 'run Script' and
a button called 'script Button'.

The 'run Script' button is simply another way of doing the Execute Script
command: it executes the selected text of the presently selected node, or the
entire text if no text is selected.

The 'script Button' button creates another button in the icon area every time
you push it. The name of the button is the headline of the presently selected
node. Hitting this _new_ button executes the button's script.

For example, to run a script on any part of an outline do the following:

1.  Select the node containing the script.
2.  Press the scriptButton button.  This will create a new button, call it X.
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
#@-node:ekr.20050130155124:<< docstring >>
#@nl
#@<< imports >>
#@+node:EKR.20040613215415:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

import sys
#@nonl
#@-node:EKR.20040613215415:<< imports >>
#@nl

__version__ = "0.15"
#@<< version history >>
#@+node:ekr.20040908094021:<< version history >>
#@+at
# 
# 0.3 EKR:
#     - Don't mess with button sizes or fonts on MacOs/darwin
# 0.4 EKR:
#     -Added support for @button, @script and @plugin.
# 0.5 EKR:
#     - Added patch by Davide Salomoni: added start2 hook and related code.
# 0.5 EKR:
#     - Use g.importExtention to import Tk.
# 0.6.1 EKR:
#     - Add much better docstring.
# 0.7 EKR:
#     - Added support for 'removeMe' hack.
#         Buttons can asked to be removed by setting 
# s.app.scriptDict['removeMe'] = True.
# 0.8 EKR:
#     - c.disableCommandsMessage disables buttons.
# 0.9 EKR:
#     - Added init, onCreate.
#     - Created scriptingController class.
# 0.10 EKR:
#     - Changed 'new_c' logic to 'c' logic.
# 0.11 EKR:
#     - Removed bindLate options: it should always be on.
#     - Added support for:
#         - @button name [@key=shortcut]
#         - @command name [@key=shortcut]
# 0.12 EKR:
#     - Use c.executeScript(p=p,silent=True) in @command so the
#       'end of script' message doesn't switch tabs.
# 0.13 EKR: Use set silent=True in all calls to c.executeScript except for the 
# 'Run Script' button.
# 0.14 EKR:
#     - All created buttons call bodyWantsFocus when the script completes.
# 0.15 EKR:
#     - Fixed a recent crasher in deleteButton.
#@-at
#@nonl
#@-node:ekr.20040908094021:<< version history >>
#@nl

bindLate = True
    # True (recommended) bind script when script is executed.
    # Allows you to change the script after creating the script button.
    # False: Bind script when button is created.
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
#@+node:ekr.20050302082838:init
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
#@-node:ekr.20050302082838:init
#@+node:EKR.20040613215415.2:onCreate
def onCreate (tag, keys):

    """Handle the onCreate event in the mod_scripting plugin."""
    
    c = keys.get('c')

    if c:
        sc = scriptingController(c)
        sc.createAllButtons()
#@nonl
#@-node:EKR.20040613215415.2:onCreate
#@+node:ekr.20050302082838.1:class scriptingController
class scriptingController:
    
    #@    @+others
    #@+node:ekr.20050302082838.2: ctor
    def __init__ (self,c):
        
        self.c = c
        self.d = {}
        self.buttons = 0
        self.scanned = False
    #@nonl
    #@-node:ekr.20050302082838.2: ctor
    #@+node:ekr.20050308105005:createAllButtons
    def createAllButtons (self):
    
        global atButtonNodes,atPluginNodes,atScriptNodes
        
        c = self.c
    
        if not self.scanned: # Not really needed, but can't hurt.
            self.scanned = True
            self.createStandardButtons()
    
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
    #@-node:ekr.20050308105005:createAllButtons
    #@+node:ekr.20051016173424:createMinibufferCommand (New in 4.4)
    def createMinibufferCommand (self,p):
        
        '''Register a minibuffer command.
        
        p.headString has the form @command name [@key=shortcut].'''
        
        c = self.c ; k = c.keyHandler ; h = p.headString()
        if not h.strip(): return
        
        #@    << get the commandName and optional shortcut >>
        #@+node:ekr.20051016192305:<< get the commandName and optional shortcut >>
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
        #@-node:ekr.20051016192305:<< get the commandName and optional shortcut >>
        #@nl
    
        def atCommandCallback (event=None,c=c,p=p.copy()):
            # The 'end-of-script command messes up tabs.
            c.executeScript(p=p,silent=True)
    
        k.registerCommand(commandName,shortcut,atCommandCallback)
    #@nonl
    #@-node:ekr.20051016173424:createMinibufferCommand (New in 4.4)
    #@+node:ekr.20041001184024:createAtButtonButton (Improved for 4.4)
    def createAtButtonButton (self,p):
        
        '''Create a button in the icon area for an @button node.
        
        An optional @key=shortcut defines a shortcut that is bound to the button's script.
        The @key=shortcut does not appear in the button's name, but
        it *does* appear in the statutus line shown when the mouse moves over the button.'''
    
        c = self.c ; h = p.headString() ; tag = "@button"
        assert(g.match(h,0,tag))
        key = h = h[len(tag):].strip()
        statusLine = "Script button: %s" % h
        #@    << get buttonText and optional shortcut >>
        #@+node:ekr.20051016221440:<< get buttonText and optional shortcut >>
        shortcut = None
        i = h.find('@key')
        
        if i > -1:
            buttonText = h[:i].strip()
            j = g.skip_ws(h,i+len('@key'))
            if g.match(h,j,'='):
                shortcut = h[j+1:].strip()
            
        else:
            buttonText = h
            
        fullButtonText = buttonText
        buttonText = buttonText[:maxButtonSize]
            
        # g.trace(commandName,'shortcut',shortcut)
        #@nonl
        #@-node:ekr.20051016221440:<< get buttonText and optional shortcut >>
        #@nl
        b = c.frame.addIconButton(text=buttonText)
        if not b: return
        #@    << define callbacks for @button buttons >>
        #@+node:ekr.20041001185413:<< define callbacks for @button buttons >>
        def deleteButtonCallback(event=None,self=self,key=key):
            self.deleteButton(key)
        
        def atButtonCallback (event=None,self=self,p=p.copy(),b=b,buttonText=buttonText):
            self.executeScriptFromCallback (p,b,buttonText)
            
        def mouseEnterCallback(event=None,self=self,statusLine=statusLine):
            self.mouseEnter(statusLine)
            
        def mouseLeaveCallback(event=None,self=self):
            self.mouseLeave()
        #@nonl
        #@-node:ekr.20041001185413:<< define callbacks for @button buttons >>
        #@nl
        if shortcut:
            #@        << bind the shortcut to atButtonCallback >>
            #@+node:ekr.20051016224708:<< bind the shortcut to atButtonCallback >>
            k = c.keyHandler ; func = atButtonCallback
            
            shortcut, junk = c.frame.menu.canonicalizeShortcut(shortcut)
            ok = k.bindShortcut (shortcut,func.__name__,func,buttonText,
                openWith=False,fromMenu=False)
            
            if ok:
                g.es_print('Bound @button %s to %s' % (
                    fullButtonText,shortcut),color='blue')
            #@nonl
            #@-node:ekr.20051016224708:<< bind the shortcut to atButtonCallback >>
            #@nl
        self.d [key] = b
        #@    << bind the callbacks to b >>
        #@+node:ekr.20051016224007:<< bind the callbacks to b >>
        if sys.platform == "win32":
            width = int(len(buttonText) * 0.9)
            b.configure(width=width,
                font=('verdana',7,'bold'),bg='LightSteelBlue1')
        b.configure(command=atButtonCallback)
        b.bind('<3>',deleteButtonCallback)
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
        #@nonl
        #@-node:ekr.20051016224007:<< bind the callbacks to b >>
        #@nl
    #@nonl
    #@-node:ekr.20041001184024:createAtButtonButton (Improved for 4.4)
    #@+node:ekr.20041001183818:createStandardButtons
    def createStandardButtons(self):
    
        c = self.c ; p = c.currentPosition() ; h = p.headString()
        script = p.bodyString()
    
        #@    << define runScriptCommand >>
        #@+node:EKR.20040618091543.1:<< define runScriptCommand >>
        def runScriptCommand (event=None):
            
            '''Called when user presses the 'Run Script' button.'''
        
            c = self.c
            c.executeScript(c.currentPosition(),useSelectedText=True)
            c.frame.bodyWantsFocus()
        #@nonl
        #@-node:EKR.20040618091543.1:<< define runScriptCommand >>
        #@nl
        #@    << define addScriptButtonCommand >>
        #@+node:EKR.20040618091543.2:<< define addScriptButtonCommand >>
        def addScriptButtonCommand (event=None,self=self):
            # Create permanent bindings for callbacks.
            c = self.c ; p = c.currentPosition()
            self.buttons += 1
            # New in 4.2.1: always use the entire body string.
            script = g.getScript(c,p,useSelectedText=False)
            h = p.headString().strip()
            buttonName = key = "Script %d" % self.buttons
            # Strip @button off the name.
            tag = "@button"
            if h.startswith(tag):
                h = h[len(tag):].strip()
            if not h: return
            text = h
            statusMessage = "Run script: %s" % text
            buttonText = text[:maxButtonSize]
            # Create the button.
            b = c.frame.addIconButton(text=buttonText)
            #@    << define callbacks for addScriptButton >>
            #@+node:EKR.20040613231552:<< define callbacks for addScriptButton >>
            def deleteButtonCallback (event=None,self=self,buttonName=buttonName):
                self.deleteButton(buttonName)
            
            def commandCallback (event=None,self=self,b=b,p=p.copy(),buttonText=buttonText):
                self.executeScriptFromCallback(p,b,buttonText)
            
            def mouseEnterCallback (event=None,self=self,statusMessage=statusMessage):
                self.mouseEnter(statusMessage)
            
            def mouseLeaveCallback (event=None,self=self):
                self.mouseLeave()
            #@nonl
            #@-node:EKR.20040613231552:<< define callbacks for addScriptButton >>
            #@nl
            self.d [key] = b
            if sys.platform == "win32":
                width = int(len(buttonText) * 0.9)
                b.configure(width=width,font=('verdana',7,'bold'))
                b.configure(bg='MistyRose1')
            b.configure(command=commandCallback)
            b.bind('<3>',deleteButtonCallback)
            b.bind('<Enter>', mouseEnterCallback)
            b.bind('<Leave>', mouseLeaveCallback)
            c.frame.bodyWantsFocus()
        #@nonl
        #@-node:EKR.20040618091543.2:<< define addScriptButtonCommand >>
        #@nl
        
        runStatusLine = 'Run script in current node'
        makeStatusLine = 'Make script button current node'
        
        for key,text,command,statusLine,bg in (
            ("execButton","Run Script",runScriptCommand,runStatusLine,'MistyRose1'),
            ("addScriptButton","Script Button",addScriptButtonCommand,makeStatusLine,"#ffffcc")
        ):
            #@        << define callbacks for standard buttons >>
            #@+node:EKR.20040614000551:<< define callbacks for standard buttons >>
            def deleteButtonCallback(event=None,self=self,key=key):
                self.deleteButton(key)
                
            def mouseEnterCallback(event=None,self=self,statusLine=statusLine):
                self.mouseEnter(statusLine)
            
            def mouseLeaveCallback(event=None,self=self):
                self.mouseLeave()
            #@nonl
            #@-node:EKR.20040614000551:<< define callbacks for standard buttons >>
            #@nl
            b = c.frame.addIconButton(text=text)
            self.d [key] = b
            if sys.platform == "win32":
                width = int(len(text) * 0.9)
                b.configure(width=width,font=('verdana',7,'bold'),bg=bg)
            b.configure(command=command)
            b.bind('<Enter>', mouseEnterCallback)
            b.bind('<Leave>', mouseLeaveCallback)
    #@nonl
    #@-node:ekr.20041001183818:createStandardButtons
    #@+node:EKR.20040614002229:deleteButton
    def deleteButton(self,key):
        
        """Delete the button at self.d[key]."""
    
        c = self.c
        button = self.d.get(key)
        if button:
            button.pack_forget()
            # button.destroy()
            
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:EKR.20040614002229:deleteButton
    #@+node:ekr.20041001203145:executeScriptNode
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
    
        c.frame.bodyWantsFocus(later=True)
    #@nonl
    #@-node:ekr.20041001203145:executeScriptNode
    #@+node:ekr.20041001202905:loadPlugin
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
    #@-node:ekr.20041001202905:loadPlugin
    #@+node:EKR.20040618091543:mouseEnter/Leave
    def mouseEnter(self,status):
    
        self.c.frame.clearStatusLine()
        self.c.frame.putStatusLine(status)
        
    def mouseLeave(self):
    
        self.c.frame.clearStatusLine()
    #@nonl
    #@-node:EKR.20040618091543:mouseEnter/Leave
    #@+node:ekr.20051016210846:executeScriptFromCallback
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
                
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051016210846:executeScriptFromCallback
    #@-others
#@nonl
#@-node:ekr.20050302082838.1:class scriptingController
#@-others
#@nonl
#@-node:EKR.20040613213623:@thin mod_scripting.py
#@-leo
