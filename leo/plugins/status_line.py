#@+leo-ver=4-thin
#@+node:ekr.20040201060959:@file-thin status_line.py
"""Adds status line to Leo window."""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

try: import Tkinter as Tk
except ImportError: Tk = None

#@+others
#@+node:EKR.20040424152057:createStatusLine
def createStatusLine(tag,keywords):
    
    c = keywords.get("c")
    c.frame.createStatusLine()
    c.frame.putStatusLine("Welcome to Leo")
    
    if 1: # Experimental.
        createBindings(c)
#@nonl
#@-node:EKR.20040424152057:createStatusLine
#@+node:EKR.20040424152057.1:createBindings (experimental, flakey and probably platform-dependent)
#@+at
# Alt_L,     Alt_R
# Caps_Lock, Shift_Lock
# Control_L, Control_R
# Meta_L,    Meta_R
# Shift_L,   Shift_R
# Super_L,   Super_R
# Hyper_L,   Hyper_R
#@-at
#@@c

def createBindings(c):
    
    def altKeyCallback(event,c=c):      return doKey(c,event,"alt")
    def controlKeyCallback(event,c=c):  return doKey(c,event,"control")
    def escapeKeyCallback(event,c=c):   return doKey(c,event,"escape")
    def keyCallback(event,c=c):         return doKey(c,event,"")
    def metaKeyCallback(event,c=c):     return doKey(c,event,"meta")

    if 1:
        c.frame.top.bind("<Key>", keyCallback)
        # For some reason this is needed.
        c.frame.body.bodyCtrl.bind("<Key-Escape>",metaKeyCallback)
        
    if 0:  # Control-s generates two events.
        c.frame.top.bind("<Control-KeyRelease>", controlKeyCallback)
        
    if 0:  # Control-s generates two events.
        c.frame.top.bind("<Control-KeyPress>", controlKeyCallback)
        
    if 0: # These conflict with the XP.
        c.frame.top.bind("<Alt_L>", altKeyCallback)
        c.frame.top.bind("<Alt_R>", altKeyCallback)
    
    if 0: # Fires while control key is down.
        c.frame.top.bind("<Control_L>", controlKeyCallback)
        c.frame.top.bind("<Control_R>", controlKeyCallback)
        
    if 0:
        c.frame.top.bind("<Key-Control_L>", controlKeyCallback)
        c.frame.top.bind("<Key-Control_R>", controlKeyCallback)
        
    if 0: # Works, sort of, but always fires even if a control sequence has happened.
        c.frame.top.bind("<KeyRelease-Control_L>", controlKeyCallback)
        c.frame.top.bind("<KeyRelease-Control_R>", controlKeyCallback)
#@nonl
#@-node:EKR.20040424152057.1:createBindings (experimental, flakey and probably platform-dependent)
#@+node:EKR.20040424152057.2:doKey
def doKey(c,event,key):

    if key not in ("meta","escape","control"):
        return
        
    enabled = c.frame.statusLineIsEnabled()
    
    g.es(key,event.keycode,event.keysym)
        
    if enabled:
        c.frame.disableStatusLine()
    else:
        c.frame.clearStatusLine()
        c.frame.enableStatusLine()
        
    enabled = not enabled

    if enabled:
        c.frame.setFocusStatusLine()
    else:
        c.frame.body.bodyCtrl.focus_set()
        
    return "break" # disable further handling??
#@nonl
#@-node:EKR.20040424152057.2:doKey
#@-others

if Tk: # Register the handlers...

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("after-create-leo-frame", createStatusLine)
        __version__ = "0.1"
        g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040201060959:@file-thin status_line.py
#@-leo
