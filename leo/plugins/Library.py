#@+leo-ver=4-thin
#@+node:ekr.20041003172238:@thin Library.py
"""A plugin to store Leo trees in anydbm files."""

#@<< about this plugin >>
#@+node:ekr.20041003172238.1:<< about this plugin >>
#@+at
# 
# Note: there isnt such a thing as an anydbm file: it's whatever the anydbm 
# module
# uses).
# 
# Under Outline, there is an option called 'Open Library'. This will open an 
# PMW
# dialog with a list of the trees that you have saved. You can insert trees 
# stored
# in the library, remove them and add trees to the library. Be aware of 
# unicode,
# any characters outside of the ascii set gets turned into a ?. I found this
# problem in storing some trees from ed's Leo outline. Id like it to be able 
# to
# store unicode, but that may require a more specific db background, than 
# anydbm.
# Also note, that your library files may not be OS independent. If your python
# distribution does not have the backing db on another machine, it will not be
# able to open your library.
# 
# This should help people develop templates that they want to reuse between 
# Leo
# projects.  For example, Id like a template of many Java interfaces to be 
# easily
# accessable.  This solves my problem I think.
#@-at
#@-node:ekr.20041003172238.1:<< about this plugin >>
#@nl

__version__ = ".2"

#@<< version history >>
#@+node:ekr.20041003172238.2:<< version history >>
#@+at
# 
# 0.2 EKR:
#     - Converted to outline.
#     - Used g.os_path methods instead of os.path methods to support unicode.
#     - Removed start2 hook.
#@-at
#@nonl
#@-node:ekr.20041003172238.2:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20041003172238.3:<< imports >>
import leoGlobals as g
import leoPlugins

import anydbm
import weakref

Tk   = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
Pmw  = g.importExtension("Pmw",    pluginName=__name__,verbose=True)
zlib = g.importExtension("zlib",   pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20041003172238.3:<< imports >>
#@nl

haveseen = weakref.WeakKeyDictionary()

path,file = g.os_path_split(g.app.loadDir)
libpath = g.os_path_join(path,"plugins","library.dbm")

#@+others
#@+node:ekr.20041003172238.4:class Library
class Library:
    '''This class presents an interface through which a Libray can be used.
    It alsoprovides a gui dialog to interact with the Library.'''
    openlibs = {}
    
    #@    @+others
    #@+node:ekr.20041003172238.5:__init__
    def __init__( self, c, path):
        
        self.c = c
        self.path = path
        
        # Set self.db.
        if Library.openlibs.has_key( path ):
            self.db = Library.openlibs[ path ]
        elif g.os_path_exists( path ):
            self.db = anydbm.open( path, "rw" )
            Library.openlibs[ path ] = self.db
        else:
            self.db = anydbm.open( path, "c" ) 
            Library.openlibs[ path ] = self.db
    #@nonl
    #@-node:ekr.20041003172238.5:__init__
    #@+node:ekr.20041003172238.6:add (unicode)
    def add( self, name, data ):
        
        # data = data.encode( "ascii" , 'replace' )
        data = g.toEncodedString(data,"utf-8",reportErrors=True)
        
        data = zlib.compress( data, 9 )
        self.db[ name ] = data
        self.db.sync()
    #@nonl
    #@-node:ekr.20041003172238.6:add (unicode)
    #@+node:ekr.20041003172238.7:remove
    def remove( self, name ):
        
        del self.db[ name ]
        self.db.sync()
    #@-node:ekr.20041003172238.7:remove
    #@+node:ekr.20041003172238.8:names
    def names( self ):
    
        return self.db.keys()
    #@-node:ekr.20041003172238.8:names
    #@+node:ekr.20041003172238.9:retrieve (unicode)
    def retrieve( self, name ):
        
        data = self.db[ name ]
        data = zlib.decompress( data )
        # return unicode( data )
        return g.toUnicode(data,"utf-8",reportErrors=True)
    #@-node:ekr.20041003172238.9:retrieve (unicode)
    #@+node:ekr.20041003172238.10:getDialog
    def getDialog( self ):
        
        self.dialog = Pmw.Dialog( buttons = ( 'Close' ,) , title =  self.path)
        butbox = self.dialog.component( 'buttonbox' )
        close = butbox.button( 0 )
        close.configure( foreground = 'blue', background = 'white' )
        hull = self.dialog.component( 'hull' )
        sh = hull.winfo_screenheight()/4 
        sw = hull.winfo_screenwidth()/4
        hull.geometry( str( 325 )+"x"+str( 325 )+"+"+str(sw)+"+"+str(sh) )   
        frame = Tk.Frame( hull)
        frame.pack( fill = 'both', expand = 1 )
        self.addList( frame )
    #@-node:ekr.20041003172238.10:getDialog
    #@+node:ekr.20041003172238.11:addList
    def addList( self, frame ):
    
        self.lbox = Pmw.ScrolledListBox( frame )
        lb = self.lbox.component( 'listbox' )
        lb.configure( background = 'white', foreground = 'blue' )
        self.setListContents()
        self.lbox.pack( side = 'left' ) 
        frame2 = Tk.Frame( frame )
        frame2.pack( side = 'right' )
        insert = Tk.Button( frame2, text = 'Insert into outline' )
        insert.configure( background = 'white', foreground = 'blue' )
        insert.configure( command = self.insert )
        insert.pack()
        remove = Tk.Button( frame2, text = 'Remove from list' )
        remove.configure( background = 'white', foreground = 'blue' )
        remove.configure( command = self.delete )
        remove.pack()
        add = Tk.Button( frame2, text = 'Add Current Node to list' )
        add.configure( background = 'white', foreground = 'blue' )
        add.configure( command = self.addCurrentNode )
        add.pack()
    #@-node:ekr.20041003172238.11:addList
    #@+node:ekr.20041003172238.12:setListContents
    def setListContents( self ):
        
        items = self.names()
        items.sort()
        self.lbox.setlist( items )
    #@-node:ekr.20041003172238.12:setListContents
    #@+node:ekr.20041003172238.13:insert
    def insert( self ):
        
        c = self.c
        item = self.lbox.getvalue()
        if len( item ) == 0: return
        item = item[ 0 ]
        s = self.retrieve( item )
        
        g.app.gui.replaceClipboardWith(s)
        self.c.pasteOutline()
    
    #@-node:ekr.20041003172238.13:insert
    #@+node:ekr.20041003172238.14:delete
    def delete( self ):
        
        c = self.c
        item = self.lbox.getvalue()
        if len( item ) == 0: return
        item = item[ 0 ]
        self.remove( item )
        self.setListContents()
    #@-node:ekr.20041003172238.14:delete
    #@+node:ekr.20041003172238.15:addCurrentNode
    def addCurrentNode( self ):
        
        c = self.c 
        p = c.currentPosition()
        hs = str( p.headString())
        s =  c.fileCommands.putLeoOutline()
        self.add( hs, s )
        self.setListContents()
    #@-node:ekr.20041003172238.15:addCurrentNode
    #@-others
#@nonl
#@-node:ekr.20041003172238.4:class Library
#@+node:ekr.20041003172238.16:onCreate
def onCreate( tag, keywords ):

    c = g.top()
    if haveseen.has_key( c ):
        return

    haveseen[ c ] = None
    men = c.frame.menu
    men = men.getMenu( 'Outline' )
    remen = Tk.Menu( men , tearoff = False)
    library = Library( c, libpath )
    men.add_command( label = "Open Library", command = library.getDialog )
#@nonl
#@-node:ekr.20041003172238.16:onCreate
#@-others

if Pmw and Tk and zlib:
    leoPlugins.registerHandler(('open2', "new") , onCreate)
    g.plugin_signon( __name__ ) 
#@nonl
#@-node:ekr.20041003172238:@thin Library.py
#@-leo
