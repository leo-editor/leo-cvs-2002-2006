#@+leo-ver=4-thin
#@+node:ekr.20040331072607:@thin hoist.py
"""Add Hoist/De-Hoist buttons to the toolbar.
"""
#@<< change history >>
#@+node:ekr.20040908093511:<< change history >>
#@+at
# 
# 0.1: Original version by Davide Salomoni.
# 0.2: EKR, Color mod by EKR.
# 0.3: DS, Works with multiple open files.
# 0.4: EKR: 4.2 coding style, enable or disable buttons, support for unit 
# tests.
# 0.5: EKR: Use constant size for non Windows platforms.
# 0.6: EKR:
#     - Added USE_SIZER and USE_FIXED_SIZES.
#       When USE_SIZER is False (recommended), the code creates buttons using 
# c.frame.addIconButton.
#@-at
#@nonl
#@-node:ekr.20040908093511:<< change history >>
#@nl

__version__ = "0.6"
  
#@<< hoist.py imports >>
#@+node:ekr.20040908093511.1:<< hoist.py imports >>
import leoGlobals as g
import leoPlugins

# g.importExtension('Tkinter') does not seem to work.
try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport('Tkinter',pluginName=__name__)

import sys
#@nonl
#@-node:ekr.20040908093511.1:<< hoist.py imports >>
#@nl

activeHoistColor = "pink1" # The Tk color to use for the active hoist button.

# Set this to 0 if the sizing of the toolbar controls doesn't look good on your platform.
USE_SIZER = False
USE_FIXED_SIZES = sys.platform != "darwin"
SIZER_HEIGHT = 23 # was 25
SIZER_WIDTH = 55 # was 70

#@+others
#@+node:ekr.20040331072607.1:class HoistButtons
class HoistButtons:

    """Hoist/dehoist buttons for the toolbar."""

    #@    @+others
    #@+node:ekr.20040331072607.2:__init__
    def __init__(self):
    
        self.hoistOn = {}
        self.hoistOff = {}
    #@-node:ekr.20040331072607.2:__init__
    #@+node:ekr.20040331072607.3:_getSizer
    def _getSizer(self, parent, height, width):
    
        """Return a sizer object to force a Tk widget to be the right size"""
    
        if USE_FIXED_SIZES: 
            sizer = Tk.Frame(parent, height=height, width=width)
            sizer.pack_propagate(0) # don't shrink 
            sizer.pack(side="right")
            return sizer
        else:
            return parent
    #@nonl
    #@-node:ekr.20040331072607.3:_getSizer
    #@+node:ekr.20040331072607.4:addWidgets
    def addWidgets(self, tags, keywords):
    
        """Add the widgets to the toolbar."""
    
        c = keywords['c'] 
        toolbar = c.frame.iconFrame
        
        def hoistOffCallback(self=self,c=c):
            self.doHoistOff(c)
            
        def hoistOnCallback(self=self,c=c):
            self.doHoistOn(c)
    
        if USE_SIZER: # original code
            self.hoistOff[c] = b = Tk.Button(
                self._getSizer(toolbar, SIZER_HEIGHT, SIZER_WIDTH),text="De-Hoist",
                command = hoistOffCallback)
            b.pack(side="right", fill="both", expand=1)
            self.hoistOn[c] = b = Tk.Button(
                self._getSizer(toolbar, SIZER_HEIGHT, SIZER_WIDTH),text="Hoist", 
                command = hoistOnCallback)
            b.pack(side="left", fill="both", expand=1)
        else: # Use addIconButton for better visual compatibility.
            self.hoistOn[c] = b1 = c.frame.addIconButton(text="Hoist")
            b1.configure(command = hoistOnCallback)
            self.hoistOff[c] = b2 = c.frame.addIconButton(text="De-Hoist")
            b2.configure(command = hoistOffCallback)
            if 1: # use this to force the buttons to the right.
                b1.pack(side="right", fill="y", expand=0)
                b2.pack(side="right", fill="y", expand=0)
    
        self.bgColor = self.hoistOn[c]["background"]
        self.activeBgColor = self.hoistOn[c]["activebackground"]
    #@nonl
    #@-node:ekr.20040331072607.4:addWidgets
    #@+node:ekr.20040331072607.5:doHoistOn
    def doHoistOn (self,c,*args,**keys):
        
        c.hoist()
    
    #@-node:ekr.20040331072607.5:doHoistOn
    #@+node:ekr.20040331072607.6:doHoistOff
    def doHoistOff (self,c,*args,**keys):
        
        c.dehoist()
    #@nonl
    #@-node:ekr.20040331072607.6:doHoistOff
    #@+node:ekr.20040331072607.7:onIdle
    def onIdle(self, tag, keywords):
        
        # This should not be necessary, and it is.
        if g.app.killed:
            return
        
        c = keywords.get('c')
    
        if not c or not hasattr(c,"hoistStack"):
            return
            
        on_widget  = self.hoistOn.get(c)
        off_widget = self.hoistOff.get(c)
    
        if not on_widget or not off_widget:
            return # This can happend during unit tests.
    
        state = g.choose(c.canHoist(),"normal","disabled")
        on_widget.config(state=state)
        
        state = g.choose(c.canDehoist(),"normal","disabled")
        off_widget.config(state=state)
    
        if len(c.hoistStack) > 0:
            on_widget.config(bg=activeHoistColor,
                activebackground=activeHoistColor,
                text="Hoist %s" % len(c.hoistStack))
        else:
            on_widget.config(bg=self.bgColor,
                activebackground=self.activeBgColor,
                text="Hoist")
    #@-node:ekr.20040331072607.7:onIdle
    #@-others
#@nonl
#@-node:ekr.20040331072607.1:class HoistButtons
#@-others

if Tk and not g.app.unitTesting:
    hoist = HoistButtons()

    if g.app.gui is None:
        g.app.createTkGui(__file__)
    
    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("after-create-leo-frame", hoist.addWidgets)
        leoPlugins.registerHandler("idle", hoist.onIdle)
        g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040331072607:@thin hoist.py
#@-leo
