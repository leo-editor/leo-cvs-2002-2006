#@+leo-ver=4-thin
#@+node:ekr.20040831115238:@thin URLloader.py
"""This plugin uses Python's urllib module to download files and import them into Leo.

It requires the TabbedLog plugin.
"""

#@@language python
#@@tabwidth -4

#@<< Change log >>
#@+node:ekr.20040831115918:<< Change log >>
#@+at
# 
# 0.2:  8/31/04 EKR:  Minor changes for 4.2 style.
#@-at
#@nonl
#@-node:ekr.20040831115918:<< Change log >>
#@nl
#@<< URLloader imports >>
#@+node:ekr.20040831115918.1:<< URLloader imports >>
import leoGlobals as g
import leoPlugins

import os
import urllib
import weakref

try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport("Tk")

try:
    import Pmw
except ImportError:
    Pmw = g.cantImport("Pmw")

try:
    import TabbedLog
except ImportError:
    TabbedLog = g.cantImport("TabbedLog")
#@nonl
#@-node:ekr.20040831115918.1:<< URLloader imports >>
#@nl

#@+others
#@+node:ekr.20040831115238.1:addURLPane
def addURLPane( tag, keywords ):

    c = keywords.get('c') or keywords.get('new_c')
    if haveseen.has_key( c ): return
   
    haveseen[ c ] = True
    x = TabbedLog.getPane( "URLLoad", c )
    ef = Pmw.EntryField( x, labelpos = 'n', label_text = 'URL:' )
    e = ef.component( 'entry' )
    e.configure( background = 'white', foreground = 'blue' )
    ef.pack( expand = 1, fill = 'x' )
    b = Tk.Button( x, text = 'Load' )
    b.pack()
    b.bind( '<Button-1>', lambda event , entry = e , c = c: load( event, entry, c ) )
#@nonl
#@-node:ekr.20040831115238.1:addURLPane
#@+node:ekr.20040831115238.2:load
def load( event, entry, c ):

    txt = entry.get()
    f = urllib.urlopen( txt )
    tname = os.tmpnam()
    tf = open( tname, 'w' )
    tf.write( f.read() )
    tf.close()
    f.close()

    c.importCommands.importFilesCommand( [ tname ], '@file')
    cv = c.currentVnode()
    cv = cv.nthChild( 0 )
    cv.setHeadString( txt )
    os.remove( tname )
#@nonl
#@-node:ekr.20040831115238.2:load
#@-others

haveseen = weakref.WeakKeyDictionary()

if Tk and Pmw and TabbedLog:

    leoPlugins.registerHandler( ('start2' , 'open2') , addURLPane)
    __version__ = ".2"
    g.plugin_signon( __name__ )
#@nonl
#@-node:ekr.20040831115238:@thin URLloader.py
#@-leo
