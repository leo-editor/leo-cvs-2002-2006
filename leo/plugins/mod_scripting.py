#@+leo-ver=4-thin
#@+node:EKR.20040613213623:@thin mod_scripting.py
"""Script buttons & menus.

Based on ideas from e's dynabutton plugin."""

__version__ = "0.3"

#@<< version history >>
#@+node:ekr.20040908094021:<< version history >>
#@+at
# 
# 0.3 EKR: Don't mess with button sizes or fonts on MacOs/darwin
#@-at
#@nonl
#@-node:ekr.20040908094021:<< version history >>
#@nl

#@<< imports >>
#@+node:EKR.20040613215415:<< imports >>
# from __future__ import generators

import leoGlobals as g
import leoPlugins

try: import Tkinter as Tk
except: Tk = None

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

#@+others
#@+node:EKR.20040613215415.2:createButtons
def createButtons (tag, keys):

    """Add scripting buttons to the icon bar."""

    c = keys.get("new_c")
    if not c: return
    p = c.currentPosition()
    script = p.bodyString()

    #@    @+others
    #@+node:EKR.20040613222712.1:Command handlers
        
    #@+node:EKR.20040618091543.1:execCommand
    def execCommand (event=None,c=c):
        
        p = c.currentPosition()
        c.executeScript(p)
    #@nonl
    #@-node:EKR.20040618091543.1:execCommand
    #@+node:EKR.20040618091543.2:addScriptButtonCommand
    def addScriptButtonCommand (event=None,c=c,p=p,script=script):
        
        # Create permanent bindings for callbacks.
        global buttons ; buttons += 1
        p = c.currentPosition()
        script = g.getScript(c,p)
        h = p.headString().strip()
        buttonName = key = "Script %d" % buttons
        text = h
        statusMessage = "Run script: %s" % p.headString()
    
        #@    << define callbacks for addScriptButton >>
        #@+node:EKR.20040613231552:<< define callbacks for addScriptButton >>
        def deleteButtonCallback(event=None,c=c,buttonName=buttonName):
        
            deleteButton(c,buttonName)
            
        def commandCallback(event=None,c=c,p=p.copy(),script=script,statusMessage=statusMessage):
            
            global bindLate
            
            if script is None: script = ""
            # g.trace(bindLate,len(script))
            
            # N.B. p and script are bound at the time this callback is created.
            c.frame.clearStatusLine()
            c.frame.putStatusLine("Executing %s..." % statusMessage)
            if bindLate:
                script = g.getScript(c,p)
            if script:
                try:
                    exec script.strip() + '\n' in {}
                except:
                    g.es("Exception executing script button")
                    g.es_exception(full=False,c=c)
                c.frame.putStatusLine("Finished!")
            else:
                g.es("No script selected",color="blue")
            
        def mouseEnterCallback(event=None,c=c,statusMessage=statusMessage):
            mouseEnter(c,statusMessage)
            
        def mouseLeaveCallback(event=None,c=c):
            mouseLeave(c)
        #@nonl
        #@-node:EKR.20040613231552:<< define callbacks for addScriptButton >>
        #@nl
        
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
    #@-node:EKR.20040618091543.2:addScriptButtonCommand
    #@+node:EKR.20040618091543.3:addScriptItemCommand
    def addScriptItemCommand (event=None,c=c,p=p,script=script):
        
        g.trace(c) # Not ready yet.
    #@nonl
    #@-node:EKR.20040618091543.3:addScriptItemCommand
    #@-node:EKR.20040613222712.1:Command handlers
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
    #@-others
    
    global data ; d = data.get(c,{})
    
    for key,text,statusLine,command,bg in (
        ("execButton","run Script","Execute script in: %s" % c.currentPosition().headString(),
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
        # b.bind('<3>',deleteButtonCallback) # No real reason to delete these buttons.
        b.bind('<Enter>', mouseEnterCallback)
        b.bind('<Leave>', mouseLeaveCallback)
        
    data[c] = d
#@nonl
#@-node:EKR.20040613215415.2:createButtons
#@-others

if Tk and not g.app.unitTesting:
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler(('open2','new'),createButtons)
        g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040613213623:@thin mod_scripting.py
#@-leo
