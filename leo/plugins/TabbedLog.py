#@+leo-ver=4-thin
#@+node:ekr.20040915073637:@thin TabbedLog.py
"""
Turns the log into a tabbed component.  Other plugins may add tabs.
"""

#@@language python
#@@tabwidth -4

__version__ = ".2"

#@<< how to use this plugin >>
#@+node:ekr.20040915082919:<< how to use this plugin >>
#@+at
# 
# To get a new tab in TabbedLog:
# 
# import TabbedLog
# p = TabbedLog.getPane(name,c)
# 
# 
# p is the pane returned for you to work with.
# name is the name of the tab you want for the pane.
# c is the commander for the leoFrame.
#@-at
#@-node:ekr.20040915082919:<< how to use this plugin >>
#@nl
#@<< version history >>
#@+node:ekr.20040915074133:<< version history >>
#@+at
# 
# 0.1: Original by annonymous
# 
# 0.2 EKR:
#     - Style changes.
#     - Enable this plugin only if Tk, Pmw and weakref can be imported.
#@-at
#@nonl
#@-node:ekr.20040915074133:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20040915074133.1:<< imports >>
import leoPlugins
import leoGlobals as g
import leoTkinterFrame

try:
    import Tkinter as Tk
except ImportError:
    Tk = cantImport("Tk")

try:
    import Pmw
except ImportError:
    Pmw = cantImport("Pmw")
    
try:
    import weakref
except ImportError:
    weakref = cantImport("weakref")
#@-node:ekr.20040915074133.1:<< imports >>
#@nl

#@+others
#@+node:ekr.20040915074510:cantImport
def cantImport (s):
    
    message = "Can not import " + s
    print message
    g.es(message,color="blue")
#@-node:ekr.20040915074510:cantImport
#@+node:ekr.20040915074510.1:createLog
def createLog( self, parentframe ):

    nb = Pmw.NoteBook( parentframe, borderwidth = 1, pagemargin = 0 )
    nb.pack(fill = 'both', expand = 1)
    nbs[ self ] = nb
    pn = nb.add( "Log" )
    return oldCLog( self, pn )
#@-node:ekr.20040915074510.1:createLog
#@+node:ekr.20040915074510.2:getPane
def getPane( name, c ):
    f = c.frame.log
    nb = nbs[ f ]
    return nb.add( name )
#@nonl
#@-node:ekr.20040915074510.2:getPane
#@-others

if Tk and Pmw and weakref:
    
    nbs = weakref.WeakKeyDictionary()
    oldCLog = leoTkinterFrame.leoTkinterLog.createControl
    leoTkinterFrame.leoTkinterLog.createControl = createLog
    
    g.plugin_signon( __name__ )
#@nonl
#@-node:ekr.20040915073637:@thin TabbedLog.py
#@-leo
