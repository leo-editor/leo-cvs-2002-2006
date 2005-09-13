#@+leo-ver=4-thin
#@+node:ekr.20040915073637:@thin TabbedLog.py
#@<<docstring>>
#@+node:ekr.20050913084153:<<docstring>>
'''Turns the log into a tabbed component.  Other plugins may add tabs.

To get a new tab in TabbedLog::

    import TabbedLog
    pane = TabbedLog.getPane(name,c)

- ``pane`` is the pane returned for you to work with.

- ``name`` is the name of the tab you want for the pane.

- ``c`` is the commander for the leoFrame.
'''
#@nonl
#@-node:ekr.20050913084153:<<docstring>>
#@nl

#@@language python
#@@tabwidth -4

__version__ = ".2"

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
import leoGlobals as g
import leoPlugins
import leoTkinterFrame

Tk  = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
Pmw = g.importExtension("Pmw",    pluginName=__name__,verbose=True)

import weakref
#@nonl
#@-node:ekr.20040915074133.1:<< imports >>
#@nl

#@+others
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

if Tk and Pmw: # Ok for unit tests even though it modifies core classes!

    nbs = weakref.WeakKeyDictionary()
    oldCLog = leoTkinterFrame.leoTkinterLog.createControl
    leoTkinterFrame.leoTkinterLog.createControl = createLog
    g.plugin_signon( __name__ )
#@nonl
#@-node:ekr.20040915073637:@thin TabbedLog.py
#@-leo
