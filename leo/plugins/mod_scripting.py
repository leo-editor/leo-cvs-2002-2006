#@+leo-ver=4-thin
#@+node:EKR.20040613213623:@thin mod_scripting.py
"""Script buttons & menus.

Based on ideas from e's dynabutton plugin."""

#@<< mod_scripting imports >>
#@+node:EKR.20040613215415:<< mod_scripting imports >>
# from __future__ import generators

import leoGlobals as g
import leoPlugins

try: import Tkinter as Tk
except: Tk = None
#@nonl
#@-node:EKR.20040613215415:<< mod_scripting imports >>
#@nl
#@<< to do >>
#@+node:EKR.20040613224458:<< to do >>
#@+at
# 
# How to set shortcut for menu items?
# 
# ** Factor out getScript from executeScript.
#     - Use this when saving script text.
# 
# - Some scripts assume that they are the presently selected headline.
#     - In particular, some top-level unit tests.
# 
# - Implement @script and @addScriptButton nodes.
#     - Possibly @addAllScriptButtons.
#@-at
#@nonl
#@-node:EKR.20040613224458:<< to do >>
#@nl

data = {} # Global data: contains one dict for each commander.
buttons = 0 # Total number of buttons created.

#@+others
#@+node:EKR.20040613215415.2:createButtons
def createButtons (tag, keys):

    """Add scripting buttons to the icon bar."""

    c = keys.get("new_c")
    if not c: return
    p = c.currentPosition()
    script = p.bodyString()

    #@    @+others
    #@+node:EKR.20040614002229:outer callbacks
    def deleteButton(c,kind):
        global data ; d = data.get(c)
        #g.trace(kind)
        if d:
            button = d.get(kind)
            if button:
                button.pack_forget()
                # button.destroy()
                
    def mouseEnter(c,status):
        c.frame.clearStatusLine()
        c.frame.putStatusLine(status)
    
    def mouseLeaveCallback(event=None,c=c):
        c.frame.clearStatusLine()
    #@nonl
    #@-node:EKR.20040614002229:outer callbacks
    #@+node:EKR.20040613222712.1:command handlers
    def execCommand (event=None,c=c):
        
        p = c.currentPosition()
        c.executeScript(p)
        
    def addScriptButtonCommand (event=None,c=c,p=p,script=script):
        
        # Create permanent bindings for callbacks.
        global buttons ; buttons += 1
        p = c.currentPosition()
        script = g.getScript(c,p)
        h = p.headString().strip()
        buttonName = key = "Script %d" % buttons
        text = h
        statusMessage = "Run script: %s" % p.headString()
    
        #@    @+others
        #@+node:EKR.20040613231552:Callbacks
        def deleteButtonCallback(event=None,c=c,buttonName=buttonName):
        
            deleteButton(c,buttonName)
            
        def commandCallback(event=None,c=c,p=p,script=script,statusMessage=statusMessage):
            
            # N.B. p and script are bound at the time this callback is created.
            c.frame.clearStatusLine()
            c.frame.putStatusLine("Executing %s..." % statusMessage)
            c.executeScript(p=p,script=script)
            c.frame.putStatusLine("Finished!")
            
        def mouseEnterCallback(event=None,c=c,statusMessage=statusMessage):
        
            mouseEnter(c,statusMessage)
        #@nonl
        #@-node:EKR.20040613231552:Callbacks
        #@-others
        
        # Create the button.
        b = c.frame.addIconButton(text=text)
        global data ; d = data.get(c,{})
        d [key] = b
        width = int(len(h) * 0.9)
        b.configure(width=width,font=('verdana',7,'bold'),bg='MistyRose1')
        b.configure(command=commandCallback)
        b.bind('<3>',deleteButtonCallback)
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
        data[c] = d
        
    def addScriptItemCommand (event=None,c=c,p=p,script=script):
        
        g.trace(c) # Not ready yet.
    #@-node:EKR.20040613222712.1:command handlers
    #@-others
    
    global data ; d = data.get(c,{})
    
    for key,text,statusLine,command,bg in (
        ("execButton","run Script","Execute script in: %s" % c.currentPosition().headString(),
            execCommand,'MistyRose1'),
        ("addScriptButton","script Button","Add script button",
            addScriptButtonCommand,'gold1'),
        # ("addScriptMenu","scriptMenu","Add script menu item",
        #    addScriptItemCommand,'gold1')
    ):
        #@        << define button-specific callbacks >>
        #@+node:EKR.20040614000551:<< define button-specific callbacks >>
        def deleteButtonCallback(event=None,c=c,key=key):
            deleteButton(c,key)
            
        def mouseEnterCallback(event=None,c=c,statusLine=statusLine):
            mouseEnter(c,statusLine)
        #@nonl
        #@-node:EKR.20040614000551:<< define button-specific callbacks >>
        #@nl
        b = c.frame.addIconButton(text=text)
        d [key] = b
        width = int(len(text) * 0.9)
        b.configure(width=width,font=('verdana',7,'bold'),bg=bg)
        b.configure(command=command)
        # b.bind('<3>',deleteButtonCallback) # No real reason to delete these buttons.
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
        
    data[c] = d
#@nonl
#@-node:EKR.20040613215415.2:createButtons
#@-others

if Tk:
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler(('open2','new'),createButtons)
        __version__ = "0.1"
        g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040613213623:@thin mod_scripting.py
#@-leo
