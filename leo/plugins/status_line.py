#@+leo-ver=4-thin
#@+node:ekr.20040201060959:@thin status_line.py
"""Adds status line to Leo window."""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20041002154511:<< imports >>
import leoGlobals as g
import leoPlugins

try:
    import Tkinter as Tk
except  ImportError:
    Tk = g.cantImport("Tk")
#@nonl
#@-node:ekr.20041002154511:<< imports >>
#@nl

__version__ = "0.2"
#@<< version history >>
#@+node:ekr.20041002154511.1:<< version history >>
#@+at
# 
# 0.2 EKR:
# - Created statusLineClass.
#     - This solves problems with binding c.
#     - Moved most code into this class.
# - c.frame.updateStatusRowCol now longer schedules itself.
#     - There is no need to do that, and it caused problems.
#@-at
#@nonl
#@-node:ekr.20041002154511.1:<< version history >>
#@nl

#@+others
#@+node:EKR.20040424152057:createStatusLine
def createStatusLine(tag,keywords):
    
    c = keywords.get("c")
    
    if c:
    
        statusLine = statusLineClass(c)
    
        leoPlugins.registerHandler("idle",statusLine.onIdle)
#@nonl
#@-node:EKR.20040424152057:createStatusLine
#@+node:ekr.20041002154511.2:statusLineClass
class statusLineClass:
    
    # A class to manage a status line in a particular Leo window
    
    #@    @+others
    #@+node:ekr.20041002154511.3:ctor
    def __init__ (self,c):
        
        self.c = c
        
        c.frame.createStatusLine()
        c.frame.putStatusLine("Welcome to Leo")
        
        if 0: # Experimental, flakey and probably platform-dependent
            self.createKeyBindings(c)
    #@nonl
    #@-node:ekr.20041002154511.3:ctor
    #@+node:EKR.20040424152057.1:createKeyBindings
    #@+at
    # Experimental, flakey and probably platform-dependent
    # Alt_L,     Alt_R
    # Caps_Lock, Shift_Lock
    # Control_L, Control_R
    # Meta_L,    Meta_R
    # Shift_L,   Shift_R
    # Super_L,   Super_R
    # Hyper_L,   Hyper_R
    #@-at
    #@@c
    
    def createKeyBindings(self):
        
        c = self.c
        
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
    #@-node:EKR.20040424152057.1:createKeyBindings
    #@+node:EKR.20040424152057.2:doKey
    def doKey(self,event,key):
        
        c = self.c
    
        if key not in ("meta","escape","control"):
            return
            
        enabled = c.frame.statusLineIsEnabled()
        
        # g.es(key,event.keycode,event.keysym)
            
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
    #@+node:ekr.20041002154846:onIdle
    def onIdle (self,tag,keys):
        
        assert(tag=="idle")
        
        c = keys.get("c")
        if c and c == self.c:
            c.frame.updateStatusRowCol()
    #@nonl
    #@-node:ekr.20041002154846:onIdle
    #@-others
#@nonl
#@-node:ekr.20041002154511.2:statusLineClass
#@-others

if Tk and not g.app.unitTesting:
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("after-create-leo-frame", createStatusLine)
        g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040201060959:@thin status_line.py
#@-leo
