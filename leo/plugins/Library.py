#@+leo-ver=4-thin
#@+node:ekr.20050310084940.4:@thin Library.py
"""A plugin to store Leo trees in anydbm files.

there is an ini you can put an absolute directory
you can shutdown and start up again with a different library

the origional had only one library/database possible.
you have to be aware of deadlock issues 
if you have more than one python/Leo open
or more than one leo open they will share.

a library isn't opened till the first time you click Outline->Library
if it doesn't exist it is created.
see the docs on anydbm for more details.
force backend not implimented yet.
default should be fine.
set libpath to default for library to exist in Leo plugins dir
"""

#@<< about this plugin >>
#@+node:ekr.20050310084940.5:<< about this plugin >>
#@+at
# 
# Note: there isnt such a thing as an anydbm file: it's whatever the anydbm 
# module
# uses).
# 
# Under Outline, there is an option called 'Library'. This will open an PMW
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
# 
# w05309 no longer works in earlier Leo than 4.3a4 init
#   adding configuration to change database while in a leo
#   trapping some errors and maybe adding some tests
#@-at
#@-node:ekr.20050310084940.5:<< about this plugin >>
#@nl

__version__ = ".25"

#@<< version history >>
#@+node:ekr.20050310084940.6:<< version history >>
#@+at
# 
# 0.2 EKR:
#     - Converted to outline.
#     - Used g.os_path methods instead of os.path methods to support unicode.
#     - Removed start2 hook.
# .025 e
#     - add startup/shutdown and config options using plugin_menu
#     - from some ideas fleshed out in forum
#@-at
#@-node:ekr.20050310084940.6:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20050310084940.7:<< imports >>
import leoGlobals as g
import leoPlugins

import anydbm
import ConfigParser
import weakref

Tk   = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
Pmw  = g.importExtension("Pmw",    pluginName=__name__,verbose=True)
zlib = g.importExtension("zlib",   pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20050310084940.7:<< imports >>
#@nl


libconfig = g.Bunch(
    libpath = 'default',
    backend = 'default',
    libname = 'library0',
    libextension = 'dbm',

    _library = weakref.WeakKeyDictionary(),
)


#@+others
#@+node:ekr.20050310084940.8:class Library
class Library:
    '''This class presents an interface through which a Libray can be used.
    It alsoprovides a gui dialog to interact with the Library.'''
    openlibs = {}  #cache librarys opened
    
    #@    @+others
    #@+node:ekr.20050310084940.9:__init__
    def __init__( self, c):
        
        self.c = c
        self.db = None
        self.path = None
        #no sense to opening a db untill Library clicked
        #self.startup()  
        
    #@-node:ekr.20050310084940.9:__init__
    #@+node:ekr.20050310084940.10:functions
    #@+node:ekr.20050310084940.11:add (unicode)
    def add( self, name, data ):
        
        # data = data.encode( "ascii" , 'replace' )
        data = g.toEncodedString(data,"utf-8",reportErrors=True)
        
        data = zlib.compress( data, 9 )
        self.db[ name ] = data
        self.db.sync()
    #@nonl
    #@-node:ekr.20050310084940.11:add (unicode)
    #@+node:ekr.20050310084940.12:retrieve (unicode)
    def retrieve( self, name ):
        
        data = self.db[ name ]
        data = zlib.decompress( data )
        # return unicode( data )
        return g.toUnicode(data,"utf-8",reportErrors=True)
    #@-node:ekr.20050310084940.12:retrieve (unicode)
    #@+node:ekr.20050310084940.13:remove
    def remove( self, name ):
        
        del self.db[ name ]
        self.db.sync()
    #@-node:ekr.20050310084940.13:remove
    #@+node:ekr.20050310084940.14:insert
    def insert( self ):
        
        c = self.c
        item = self.lbox.getvalue()
        if len( item ) == 0: return
        item = item[ 0 ]
        s = self.retrieve( item )
        
        g.app.gui.replaceClipboardWith(s)
        self.c.pasteOutline()
    
    #@-node:ekr.20050310084940.14:insert
    #@+node:ekr.20050310084940.15:delete
    def delete( self ):
        
        c = self.c
        item = self.lbox.getvalue()
        if len( item ) == 0: return
        item = item[ 0 ]
        self.remove( item )
        self.setListContents()
    #@-node:ekr.20050310084940.15:delete
    #@+node:ekr.20050310084940.16:addCurrentNode
    def addCurrentNode( self ):
        
        c = self.c 
        p = c.currentPosition()
        hs = str( p.headString())
        s =  c.fileCommands.putLeoOutline()
        self.add( hs, s )
        self.setListContents()
    #@-node:ekr.20050310084940.16:addCurrentNode
    #@-node:ekr.20050310084940.10:functions
    #@+node:ekr.20050310084940.17:GUI
    #maybe the dialog should close the database after an insert?
    #maybe sync is good enough
    
    #it can get hidden behind the leo after clicking an insert
    #and calling the Outline->Library again should reuse the dialog
    #fix this later
    #@nonl
    #@+node:ekr.20050310084940.18:names
    def names( self ):
    
        return self.db.keys()
    #@-node:ekr.20050310084940.18:names
    #@+node:ekr.20050310084940.19:getDialog
    def getDialog( self ):
    
        #g.trace(self.path)
        if self.startup():
            return
    
        path, fname = g.os_path_split(self.path)
        title = "%s %s" %( fname, path)
    
        self.dialog = Pmw.Dialog( buttons = ( 'Close' ,) , title =  title)
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
    #@-node:ekr.20050310084940.19:getDialog
    #@+node:ekr.20050310084940.20:addList
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
    #@-node:ekr.20050310084940.20:addList
    #@+node:ekr.20050310084940.21:setListContents
    def setListContents( self ):
        
        items = self.names()
        items.sort()
        self.lbox.setlist( items )
    #@-node:ekr.20050310084940.21:setListContents
    #@-node:ekr.20050310084940.17:GUI
    #@+node:ekr.20050310084940.22:shutdown
    def shutdown( self ):
        """anydbm just sync then forget it I guess
        no close mentioned in doc, but db.close exists
        should close() later when everything else works
        """
        if self.db._checkOpen: 
            self.db.sync()
        self.db = None
        
        #might want to leave it accessable?
        #self.path = path = g.os_path_join(
        #    libconfig.libpath, 
        #    libconfig.libname +'.'+ libconfig.libextension)
        #del Library.openlibs[ path ]
    
        return 1
    #@nonl
    #@-node:ekr.20050310084940.22:shutdown
    #@+node:ekr.20050310084940.23:startup
    def startup( self ):
    
        path = g.os_path_join(
            libconfig.libpath, 
            libconfig.libname +'.'+ libconfig.libextension)
    
        if self.path != path: #it may be open already
            self.path = path
            if self.db: self.shutdown()
    
        #g.trace(self.path)
    
        try:
            # Set self.db.
            if Library.openlibs.has_key( path ):
                self.db = Library.openlibs[ path ]
        
            elif g.os_path_exists( path ):
                self.db = anydbm.open( path, "rw" )
                Library.openlibs[ path ] = self.db
        
            else:
                self.db = anydbm.open( path, "c" ) 
                Library.openlibs[ path ] = self.db    
        except Exception: #anydbm.NODBwhatever
            #init() fails and gives user no chance to fix it
            # the bad import msg isn't good enough to help diagnose
            g.es('problem starting Library\n %s' %path)
            g.es(Library.openlibs)
        
        if self.db._checkOpen: 
            return 0
    
        return 1
    #@nonl
    #@-node:ekr.20050310084940.23:startup
    #@-others
#@nonl
#@-node:ekr.20050310084940.8:class Library
#@+node:ekr.20050310084940.24:config
#for the plugin manager using the ini
#still fluid as of 10/04
#@+node:ekr.20050310084940.25:cmd_shutdown

def cmd_shutdown(): 
    """shutdown the database
    this should also close all dialogs and do any cleanup
    """
    c = g.top() #might loose tie to c this later
    if libconfig._library.has_key(c):
        libconfig._library[c].shutdown()
    
#@nonl
#@-node:ekr.20050310084940.25:cmd_shutdown
#@+node:ekr.20050310084940.26:cmd_SetAsDefault

def cmd_SetAsDefault(): 
    """
    set the ini to the current options
    this can't really be implimented yet
    the ini is the only way to change options
    """
    g.es('edit the ini or use the Properties option')
#@-node:ekr.20050310084940.26:cmd_SetAsDefault
#@+node:ekr.20050310084940.27:cmd_ShowCurrent

def cmd_ShowCurrent(): 
    """
    no interest in maintaing seperate per leo defaults.
    beed to filter out underscored and commanders when !debug
    """
    g.es(libconfig)
#@-node:ekr.20050310084940.27:cmd_ShowCurrent
#@+node:ekr.20050310084940.28:applyConfiguration

def applyConfiguration(config):
    """plugin menu calls this in Properties after ini edit
    """

    if config is None:
        config = getConfiguration()

    for x in ['libpath', 'backend', 'libname', 'libextension']:
        xval = config.get("Main", x)
        #g.es(x, xval)

        #this seems to be True even if option set to '' in ini
        if xval and xval != '':
            #g.es('setting %s %r'%( x, xval))
            setattr(libconfig, x, xval)

    #now veryify they have decent values
    #libpath = libpath, set to plugins if '' or default in ini
    #backend = 'default',  later to pick particular db
    #these don't have defaults
    #libname = 'library',
    #libextension = 'dbm',  might be database dependant

    if not libconfig.libpath or libconfig.libpath == 'default':
        libconfig.libpath = g.os_path_normpath(g.os_path_abspath(
            g.os_path_join(g.app.loadDir, '../', "plugins")
            ))

#@-node:ekr.20050310084940.28:applyConfiguration
#@+node:ekr.20050310084940.29:getConfiguration
def getConfiguration(): 
    """Return the config object""" 
    fileName = g.os_path_join(g.app.loadDir,"../","plugins","Library.ini") 
    config = ConfigParser.ConfigParser() 
    config.read(fileName) 
    return config 
#@-node:ekr.20050310084940.29:getConfiguration
#@-node:ekr.20050310084940.24:config
#@+node:ekr.20050310084940.30:onCreate
def onCreate( tag, keywords ):

    c = g.top()  #c = keywords.get('c') 
    #g.trace(keywords.get('c'))
    #g.trace(c )
    #get('c')  seems not to work in onCreate 4.3 alpha 3/7
    if not c: return

    if libconfig._library.has_key( c ):
        return

    men = c.frame.menu
    men = men.getMenu( 'Outline' )
    remen = Tk.Menu( men, tearoff = False)

    #some chicken/egg precedence going on here
    library = Library( c)

    #save last instance for cmd_*
    libconfig._library[c] = library #why have have seen too?
    men.add_command( label = "Library", command = library.getDialog )
#@-node:ekr.20050310084940.30:onCreate
#@+node:ekr.20050310084940.31:init
def init():
    """this is getting to be ok overload
    """
    ok = Tk and Pmw and zlib and not g.app.unitTesting

    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__ )
    
        ok = g.app.gui.guiName() == "tkinter"
    
        if ok:
            try:
                leoPlugins.registerHandler("after-create-leo-frame", onCreate)
                #leoPlugins.registerHandler(('open2', "new"), onCreate)
                #leoPlugins.registerHandler('onCreate', onCreate )
                g.plugin_signon(__name__ )
                #this is going to be one global config
                applyConfiguration(getConfiguration())
            except Exception:
                ok = False
    return ok
#@nonl
#@-node:ekr.20050310084940.31:init
#@-others

#@@color 
#@nonl
#@-node:ekr.20050310084940.4:@thin Library.py
#@-leo
