#@+leo-ver=4-thin
#@+node:EKR.20040613213623:@thin mod_scripting.py
"""Script buttons & menus.

Based on ideas from e's dynabutton plugin."""

__version__ = "0.6"
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
#@-at
#@nonl
#@-node:ekr.20040908094021:<< version history >>
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

data = {} # Global data: contains one dict for each commander.
buttons = 0 # Total number of buttons created.

bindLate = True
    # True (recommended) bind script when script is executed.
    # Allows you to change the script after creating the script button.
    # False: Bind script when button is created.
atButtonNodes = True
    # True: adds a button for every @button node.
atPluginNodes = False
    # True: dynamically loads plugins in @plugins nodes when a window is created.
atScriptNodes = False
    # True: dynamically executes script in @script nodes when a window is created.  DANGEROUS!
maxButtonSize = 18
    # Maximum length of button names.

#@+others
#@+node:EKR.20040618091629:Utilities for callbacks
#@+node:EKR.20040614002229:deleteButton
def deleteButton(c,key):
    
    """Delete the button at data[key]."""
    
    global data ; d = data.get(c)

    if d:
        button = d.get(key)
        if button:
            button.pack_forget()
            # button.destroy()
#@nonl
#@-node:EKR.20040614002229:deleteButton
#@+node:EKR.20040618091543:mouseEnter/Leave
def mouseEnter(c,status):

    c.frame.clearStatusLine()
    c.frame.putStatusLine(status)
    
def mouseLeave(c):

    c.frame.clearStatusLine()
#@nonl
#@-node:EKR.20040618091543:mouseEnter/Leave
#@-node:EKR.20040618091629:Utilities for callbacks
#@+node:EKR.20040613215415.2:onOpenWindow
def onOpenWindow (tag, keys):

    """Add scripting buttons to the icon bar."""
    
    if tag == "start2": c = g.top()
    else: c = keys.get("new_c")
    if not c: return
    
    global data ; d = data.get(c,{})
    if d: return
    
    createStandardButtons(c,d)

    if atButtonNodes:
        createDynamicButtons(c,d)
        
    data[c] = d
    
    # Scan for @plugin and @script nodes.
    for p in c.allNodes_iter():
        if p.headString().startswith("@plugin"):
            loadPlugin(c,p)
        elif p.headString().startswith("@script"):
            executeScriptNode(c,p)
#@nonl
#@-node:EKR.20040613215415.2:onOpenWindow
#@+node:ekr.20041001183818:createStandardButtons
def createStandardButtons(c,d):
    
    p = c.currentPosition()
    script = p.bodyString()
    
    #@    << define execCommand >>
    #@+node:EKR.20040618091543.1:<< define execCommand >>
    def execCommand (event=None,c=c):
        c.executeScript(c.currentPosition(),useSelectedText=True)
    #@nonl
    #@-node:EKR.20040618091543.1:<< define execCommand >>
    #@nl
    #@    << define addScriptButtonCommand >>
    #@+node:EKR.20040618091543.2:<< define addScriptButtonCommand >>
    def addScriptButtonCommand (event=None,c=c,p=p,script=script):
        
        # Create permanent bindings for callbacks.
        global buttons ; buttons += 1
        p = c.currentPosition()
        if not script:
            # New in 4.2.1: always use the entire body string.
            script = g.getScript(c,p,useSelectedText=False)
        h = p.headString().strip()
        buttonName = key = "Script %d" % buttons
        # Strip @button off the name.
        tag = "@button"
        if h.startswith(tag):
            h = h[len(tag):].strip()
        if not h: return
        text = h
        statusMessage = "Run script: %s" % text
        buttonText = text[:maxButtonSize]
    
        #@    << define callbacks for addScriptButton >>
        #@+node:EKR.20040613231552:<< define callbacks for addScriptButton >>
        def deleteButtonCallback(event=None,c=c,buttonName=buttonName):
            deleteButton(c,buttonName)
            
        def commandCallback(event=None,c=c,p=p.copy(),script=script,statusMessage=statusMessage):
            global bindLate
            if script is None: script = ""
            c.frame.clearStatusLine()
            c.frame.putStatusLine("Executing %s..." % statusMessage)
            if bindLate:
                # New in 4.2.1: always use the entire body string.
                script = g.getScript(c,p,useSelectedText=False)
            if script:
                c.executeScript(script=script)
            else:
                g.es("No script selected",color="blue")
            
        def mouseEnterCallback(event=None,c=c,statusMessage=statusMessage):
            mouseEnter(c,statusMessage)
            
        def mouseLeaveCallback(event=None,c=c):
            mouseLeave(c)
        #@nonl
        #@-node:EKR.20040613231552:<< define callbacks for addScriptButton >>
        #@nl
        
        # Create the button: limit the text to twelve characters.
        b = c.frame.addIconButton(text=buttonText)
        global data ; d = data.get(c,{})
        d [key] = b
        if sys.platform == "win32":
            width = int(len(buttonText) * 0.9)
            b.configure(width=width,font=('verdana',7,'bold'),bg='MistyRose1')
        b.configure(command=commandCallback)
        b.bind('<3>',deleteButtonCallback)
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
        data[c] = d
    #@-node:EKR.20040618091543.2:<< define addScriptButtonCommand >>
    #@nl
    
    for key,text,statusLine,command,bg in (
        ("execButton","run Script","Run script: %s" % c.currentPosition().headString(),
            execCommand,'MistyRose1'),
        ("addScriptButton","script Button","Add script button",
            addScriptButtonCommand,"#ffffcc")
    ):
        #@        << define callbacks for standard buttons >>
        #@+node:EKR.20040614000551:<< define callbacks for standard buttons >>
        def deleteButtonCallback(event=None,c=c,key=key):
            deleteButton(c,key)
            
        def mouseEnterCallback(event=None,c=c,statusLine=statusLine):
            mouseEnter(c,statusLine)
            
        def mouseLeaveCallback(event=None,c=c):
            mouseLeave(c)
        #@nonl
        #@-node:EKR.20040614000551:<< define callbacks for standard buttons >>
        #@nl
        b = c.frame.addIconButton(text=text)
        d [key] = b
        if sys.platform == "win32":
            width = int(len(text) * 0.9)
            b.configure(width=width,font=('verdana',7,'bold'),bg=bg)
        b.configure(command=command)
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
#@nonl
#@-node:ekr.20041001183818:createStandardButtons
#@+node:ekr.20041001184020:createDynamicButtons
def createDynamicButtons (c,d):
    
    for p in c.allNodes_iter():
        if p.headString().startswith("@button"):
            createDynamicButton(c,p,d)
#@nonl
#@-node:ekr.20041001184020:createDynamicButtons
#@+node:ekr.20041001184024:createDynamicButton
def createDynamicButton (c,p,d):
    
    tag = "@button"
    p = p.copy()
    text = p.headString()
    assert(g.match(text,0,tag))
    text = text[len(tag):].strip()
    key = text
    script = g.getScript(c,p,useSelectedText=False)
    buttonText = text[:maxButtonSize]

    statusLine = "Script button: %s" % text
    bg = 'LightSteelBlue1'
    
    #@    << define callbacks for dynamic buttons >>
    #@+node:ekr.20041001185413:<< define callbacks for dynamic buttons >>
    def deleteButtonCallback(event=None,c=c,key=key):
        deleteButton(c,key)
        
    def execCommand (event=None,c=c,script=script):
        c.executeScript(script=script)
        
    def mouseEnterCallback(event=None,c=c,statusLine=statusLine):
        mouseEnter(c,statusLine)
        
    def mouseLeaveCallback(event=None,c=c):
        mouseLeave(c)
    #@nonl
    #@-node:ekr.20041001185413:<< define callbacks for dynamic buttons >>
    #@nl
    
    b = c.frame.addIconButton(text=buttonText)
    if not b: return
    d [key] = b
    if sys.platform == "win32":
        width = int(len(text) * 0.9)
        b.configure(width=width,font=('verdana',7,'bold'),bg=bg)
    b.configure(command=execCommand)
    b.bind('<3>',deleteButtonCallback)
    b.bind('<Enter>', mouseEnterCallback)
    b.bind('<Leave>', mouseLeaveCallback)
#@-node:ekr.20041001184024:createDynamicButton
#@+node:ekr.20041001202905:loadPlugin
def loadPlugin (c,p):
    
    tag = "@plugin"
    h = p.headString()
    assert(g.match(h,0,tag))
    
    # Get the name of the module.
    theFile = h[len(tag):].strip()
    if theFile[-3:] == ".py":
        theFile = theFile[:-3]
    theFile = g.toUnicode(theFile,g.app.tkEncoding)
    
    global atPluginNodes

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
#@+node:ekr.20041001203145:executeScriptNode
def executeScriptNode (c,p):
    
    tag = "@script"
    h = p.headString()
    assert(g.match(h,0,tag))
    name = h[len(tag):].strip()
    
    global atPluginNodes

    if not atPluginNodes:
        g.es("disabled @script: %s" % (name),color="blue")
    else:
        g.es("executing script %s" % (name),color="blue")
        c.executeScript(p,useSelectedText=False)
#@nonl
#@-node:ekr.20041001203145:executeScriptNode
#@-others

if Tk and not g.app.unitTesting:
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler(('start2','open2','new'),onOpenWindow)
        g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040613213623:@thin mod_scripting.py
#@-leo
