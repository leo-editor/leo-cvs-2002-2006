#@+leo-ver=4-thin
#@+node:ekr.20040915075530:@thin UASearch.py
"""
A plugin for searching unknownAttributes (uA's).
"""

#@@language python
#@@tabwidth -4

__version__ = ".2"
#@<< version history >>
#@+node:ekr.20040915075530.1:<< version history >>
#@+at
# 
# 0.1: Original
# 
# 0.2 EKR:
#     - Style changes.
#     - Converted to outline.
#     - Enable this plugin only if TabbedLog, Tk, Pmw and weakref can be 
# imported.
#     - Added found function to handle selecting found nodes properly.
#@-at
#@nonl
#@-node:ekr.20040915075530.1:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20040915075530.2:<< imports >>
import leoGlobals as g
import leoPlugins
import leoTkinterFrame
import re

try:
    import TabbedLog
except ImportError:
    TabbedLog = g.cantImport("TabbedLog",__name__)

try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport("Tk",__name__)

try:
    import Pmw
except ImportError:
    Pmw = g.cantImport("Pmw",__name__)
    
try:
    import weakref
except ImportError:
    weakref = g.cantImport("weakref",__name__)

#@-node:ekr.20040915075530.2:<< imports >>
#@nl

#@+others
#@+node:ekr.20040915075530.3:addPMenu
def addPMenu( tag, keywords ):
    if keywords.has_key( 'c' ):
        c = keywords[ 'c' ]
    else:
        c = keywords[ 'new_c' ]
    if haveseen.has_key( c ): return  
    haveseen[ c ] = True  
    x = TabbedLog.getPane( "UASearch", c )
    ef = Pmw.EntryField( x, labelpos = 'w', label_text = 'uaname:' )
    e = ef.component( 'entry' )
    e.configure( background = 'white', foreground = 'blue' )
    ef.pack()
    ev = Pmw.EntryField( x, labelpos = 'w', label_text = 'uavalue:' )
    e = ev.component( 'entry' )
    e.configure( background = 'white', foreground = 'blue' )
    ev.pack()
    rs = Pmw.RadioSelect( x, labelpos = 'n' ,
        label_text = 'Search by:',
        frame_borderwidth = 2,
        frame_relief = 'ridge',
        buttontype = 'radiobutton')
    rs.add( "uaname" )
    rs.add( "uavalue" )
    rs.add( "regex" )
    rs.pack()
    rs.setvalue( "uaname")
    b = Tk.Button( x, text = "Search" )
    b.pack()
    l = Tk.Label( x )
    l.pack()
    #@    << define callbacks >>
    #@+node:ekr.20040915075808:<< define callbacks >>
    def firesearch( event, rs = rs, ef = ef, ev = ev, c = c, l = l ):
    
        stype = rs.getvalue()
        name = ef.getvalue()
        value = ev.getvalue()
        l.configure( text = "Searching    " )
        search( name, value, stype, c )
        l.configure( text = "" )
    #@nonl
    #@-node:ekr.20040915075808:<< define callbacks >>
    #@nl
    b.bind( '<Button-1>', firesearch )
#@-node:ekr.20040915075530.3:addPMenu
#@+node:ekr.20040915081837:found
def found (porv,name):
    
    c = porv.c
    note("found: " + name)
    c.selectVnode(porv)
    c.redraw()
#@nonl
#@-node:ekr.20040915081837:found
#@+node:ekr.20040915082303:note
def note (s):
    
    print s
    g.es(s)
#@nonl
#@-node:ekr.20040915082303:note
#@+node:ekr.20040915075530.4:search
def search( name, value, stype, c ):
    cv = c.currentVnode().threadNext()
    if name.strip() == '':
        return note("empty name")
    if stype == "uaname":
        while cv:
            t = getT( cv )
            if hasattr(t,'unknownAttributes'): 
                if t.unknownAttributes.has_key( name ):
                    return found(cv,name)
            cv = cv.threadNext()
    else:
        if value.strip() == '': return
        if stype == 'regex':
            sea = re.compile( value )
        while cv:
            t = getT( cv )
            if hasattr(t,'unknownAttributes' ):
                if t.unknownAttributes.has_key( name ):
                    if stype == 'uavalue':
                        if t.unknownAttributes[ name ] == value:
                            return found(cv,name)
                    else:
                        st = t.unknownAttributes[ name ]
                        if sea.search( st ):
                            return found(cv,name)
            cv = cv.threadNext()
    note ("not found: " + name)
#@nonl
#@-node:ekr.20040915075530.4:search
#@+node:ekr.20040915075530.5:getT
def getT( node ):

    if str( node.__class__ )== 'leoNodes.vnode':
        return node.t
    else:
        return node.v.t
#@nonl
#@-node:ekr.20040915075530.5:getT
#@-others
   
if TabbedLog and Tk and Pmw and weakref:
    
    nbs = weakref.WeakKeyDictionary()
    haveseen = weakref.WeakKeyDictionary()

    leoPlugins.registerHandler( ('start2' , 'open2') ,addPMenu)
    g.plugin_signon( __name__ ) 
#@-node:ekr.20040915075530:@thin UASearch.py
#@-leo
