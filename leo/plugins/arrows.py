#@+leo-ver=4-thin
#@+node:EKR.20040517080517.1:@thin arrows.py
"""Rebind up/down arrow keys"""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050101090207:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20050101090207:<< imports >>
#@nl

__version__ = "1.4"
#@<< version history >>
#@+node:ekr.20050311090939.1:<< version history >>
#@@killcolor
#@+at
# 
# 1.4 EKR:
#     - Changed 'new_c' logic to 'c' logic.
#     - Added init function.
#@-at
#@nonl
#@-node:ekr.20050311090939.1:<< version history >>
#@nl

#@+others
#@+node:ekr.20050311090939.2:init
def init ():
    
    ok = Tk and not g.app.unitTesting # Not for unit testing. (conflicts key bindings)
    
    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)
    
        if g.app.gui.guiName() == "tkinter":
            leoPlugins.registerHandler("open2", onOpen)
            g.plugin_signon(__name__)
            
    return ok
#@nonl
#@-node:ekr.20050311090939.2:init
#@+node:EKR.20040517080517.2:onOpen
# Warning: the bindings created this way conflict with shift-arrow keys.

def onOpen (tag,keywords):

    c = keywords.get('c')
    if not c: return

    body = c.frame.body
    tree = c.frame.tree

    # Add "hard" bindings to have up/down arrows move by visual lines.
    old_binding = body.bodyCtrl.bind("<Up>")
    if len(old_binding) == 0:
        body.bodyCtrl.bind("<Up>",tree.OnUpKey)

    old_binding = body.bodyCtrl.bind("<Down>")
    if len(old_binding) == 0:
        body.bodyCtrl.bind("<Down>",tree.OnDownKey)
#@nonl
#@-node:EKR.20040517080517.2:onOpen
#@-others
#@nonl
#@-node:EKR.20040517080517.1:@thin arrows.py
#@-leo
