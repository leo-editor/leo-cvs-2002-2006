#@+leo-ver=4-thin
#@+node:ekr.20050328092641.4:@thin Library.py
#@<< docstring >>
#@+node:ekr.20050912180445:<< docstring >>

'''A plugin to store Leo trees in anydbm files. Note: there isnt such a thing as an
anydbm file: it's whatever the anydbm module uses.

Under Outline, there is an option called 'Library'. This will open an PMW
dialog with a list of the trees that you have saved. You can insert trees stored
in the library, remove them and add trees to the library. Be aware of unicode,
any characters outside of the ascii set gets turned into a ?. I found this
problem in storing some trees from ed's Leo outline. Id like it to be able to
store unicode, but that may require a more specific db background, than anydbm.
Also note, that your library files may not be OS independent. If your python
distribution does not have the backing db on another machine, it will not be
able to open your library.

This should help people develop templates that they want to reuse between Leo
projects.  For example, Id like a template of many Java interfaces to be easily
accessable.
'''
#@nonl
#@-node:ekr.20050912180445:<< docstring >>
#@nl

__version__ = ".28"  #f05325p10

#@<< version history >>
#@+node:ekr.20050328092641.6:<< version history >>
#@+at
# 0.0 created by the plugin guy & posted to the Leo forums.
#     -
# 0.2 EKR:
#     - Converted to outline.
#     - Used g.os_path methods instead of os.path methods to support unicode.
#     - Removed start2 hook.
# .025 e
#     - add startup/shutdown and config options using plugin_menu
#     - from some ideas fleshed out in forum
#     - no sense to opening a db untill Library first clicked.
# .027 e
#     - refactor class Library methods to be all classmethods.
#       this saves creating one instance per leo or any instance at all!
#     - reuse dialog if already open, destroy on close leo
#     - appears to do the right thing if you click Outline->Library again,
#       that is, add/insert goes from/to the place you expect it to.
# 
# .028 e, still testing. posted url to forum
#     - not sure how to get it to switch leo's w/o Clicking menu
#       like if you click on another leo while keeping the dialog open.
#       there doesn't seem to be a reliable way to know the active leo.
#       spell checker did this ok somehow with one dialog
#        by hooking on select node and change body. a last resort.
#     - py2.2 doesn't want to open a new or existing library22.dbm
#        it appears to create a zero len file then next errors
#        because it can't open an existing zero len library22.dbm
#        fails on a good library.dbm created in py2.4
#        you'll feel better after you upgrade anyway.
#     - rudimentart support for @setting Library_lib*= same as but overrides 
# the ini
#     - fixed the false start of seperating library,libpath,extension
#      -libN= where N can be any aschii chars in ini or @setting, (N is 0..5 
# only)
#      - default/ translates to leo/plugins/ ~/ is g.app.homeDir/
#      - not sure it should respect Leo's don't create non existing 
# directories
#     - add dropdown for multiple libraries, select between them
#      - you can edit the first entry, "libN {path}" to overwrite defaults.
#      - it might be better to enable some extra lib entries and pick between 
# them.
#      - if you mess with the format here or the ini or the @setting:
#      - I continue to hope the worst that can happen on a bad entry is 
# nothing.
#    - no provisions yet to update the @settings or ini on exit.
# .029 e, http://rclick.netfirms.com/Library.htm
#    - preserve users clipboard on paste item from database into outline
#  on click the  dialog is *not* recreated,
#  changed = change  *title
# 
# 
#@-at
#@-node:ekr.20050328092641.6:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20050328092641.7:<< imports >>
import leoGlobals as g
import leoPlugins
#import weakref
import anydbm
import ConfigParser

Tk   = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
Pmw  = g.importExtension("Pmw",    pluginName=__name__,verbose=True)
zlib = g.importExtension("zlib",   pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20050328092641.7:<< imports >>
#@nl


libconfig = g.Bunch(
    lib = 'default',  #don't touch this one nor use lib=
    #you can hardwire in your own favorites, change the ini or add @setting
    lib0 = 'default/library.dbm',
    verbosity = 0,
)
fatal = 1 #for startup
validlibs = ['lib0', 'lib1', 'lib2', 'lib3', 'lib4', 'lib5',]
#@+others
#@+node:ekr.20050328092641.8:class Library
class Library(object):
    '''This class presents an interface through which a Libray can be used.
    It also provides a gui dialog to interact with the Library.

    all methods are now classmethods 
    the commander that is last retrieved from keywords is the one used.
    
    '''
    #cannot create weak reference to 'unicode' object
    #damm the db is an unhashable instance too. not too surprizing
    #and now I see, would be a waste since it is a dict of the databse.
    #really need to preserve a handle to the database, not the databse itself!
    #not sure how to do that yet...
    #maybe  db.db or  db.dbc is the handle and you can do a reread restore
    # to get the full db dictionary back, is caching doing anything useful?
    #its also possibly that the db __str__ method masks the fact by outputting
    #all the key/vals in reponse to a print db, and all that is copied is a handle.
    #openlibs = weakref.WeakKeyDictionary() #cache librarys opened, db is key
    openlibs = {} #cache librarys opened, db is key

    #openlibs = {} #cache librarys opened, path is key
    c = None  # needs to be a weakref?
    db = None # needs to be a weakref?
    path = None
    dialog = None
    
    #@    @+others
    #@+node:ekr.20050328092641.9:__init__
    def __init__(self, c):
        
        pass
    #@nonl
    #@-node:ekr.20050328092641.9:__init__
    #@+node:ekr.20050328092641.10:buttons
    #@+node:ekr.20050328092641.11:insert
    def insert(cls):
        """
        c = g.top() #is still the origional leo even after leftclick
        when a dlg is already opened and more than one leo on screen,
        cls.c isn't necessarily the currently selected leo anymore
        need to hook on first selected and change Library.c?
        is there a way to do that? 
        maybe change cls.c on every node select from any open leo?
        """
        
        c = cls.c 
    
        item = cls.lbox.getvalue()
        if len( item ) == 0: return
        item = item[ 0 ]
        s = cls.retrieve( item )
    
        #preserve the users clippboard
        stext = g.app.gui.getTextFromClipboard()
    
        g.app.gui.replaceClipboardWith(s)
        cls.c.pasteOutline()
    
        g.app.gui.replaceClipboardWith(stext)
    insert = classmethod(insert)
    #@nonl
    #@-node:ekr.20050328092641.11:insert
    #@+node:ekr.20050328092641.12:delete
    def delete(cls):
        
        c = cls.c
        item = cls.lbox.getvalue()
        if len( item ) == 0: return
        item = item[ 0 ]
        cls.remove( item )
        cls.setListContents()
    delete = classmethod(delete)
    #@nonl
    #@-node:ekr.20050328092641.12:delete
    #@+node:ekr.20050328092641.13:addCurrentNode
    def addCurrentNode(cls):
        
        c = cls.c
        p = c.currentPosition()
        hs = str( p.headString())
        s =  c.fileCommands.putLeoOutline()
        cls.add( hs, s )
        cls.setListContents()
    addCurrentNode = classmethod(addCurrentNode)
    #@nonl
    #@-node:ekr.20050328092641.13:addCurrentNode
    #@+node:ekr.20050328092641.14:sort time
    #@+at
    # add button to call htmlize on a node fallback to implicit @others and 
    # text
    # 
    # not sure self consistant or dangling named nodes could be displayed 
    # properly
    # what if clones are involved will they become copies?
    # language and other directives active at the time of add or insert could 
    # matter
    # 
    # add buttons to sort the nodes displayed
    # by time inserted,
    # by filename of leo
    # attributes for internal use to be added at some future time
    # 
    # 
    # sort by path and last access for the dropdown
    # without redoing the whole dialog
    # 
    # en/decrypted nodes on insert/add
    #@-at
    #@-node:ekr.20050328092641.14:sort time
    #@-node:ekr.20050328092641.10:buttons
    #@+node:ekr.20050328092641.15:GUI
    #maybe the dialog should close the database after an insert?
    #maybe sync is good enough
    
    #dialog can get hidden behind the leo after clicking a button
    #clicking Outline->Library again should reuse the same dialog
    # from the same leo or a different leo
    
    
    #key is node name, duplicate is silently overwritten. 
    #maybe should check or warn first?
    #@nonl
    #@+node:ekr.20050328092641.16:getDialog
    def getDialog(cls, c= None):
        """has mixed float and int division, 
         is that depreciated or require // in 2.5?
        """
    
        if c: cls.c = c
        #g.trace(c)
        #g.trace(self.path)
        if cls.db is None and cls.startup() == fatal: return
    
        #also have to account for the possibility you will open dlg from one leo
        #then switch leos. that is something g.top() might be better for
        #maybe when a button is clicked it should first find which leo is active.
    
        #might not want to overwrite the previous c so fast.
        if cls.dialog:
            #later determine if needs to be redrawn or can be reused
            #should be recreated in same place if so, not sure how
            #and what sets c back to None if user closes it?
            #that should allow gc w/o weakrefs. need a cleanup on the dialog?
            #if the dialog can tell when it has focus, it could find g.top?
            #cls.dialog.focus() #? doesn't appear to work or error
            cls.dialog.show()
            
            #this can still be of the wrong commander?
            #but appears to do the right thing if you hit Outline->Library.
            return 
    
        #should lable with the current commander if can't solve which it is.
        title = g.computeWindowTitle(cls.path)
    
        cls.dialog = Pmw.Dialog( buttons = ( 'Close' ,) , title =  title)
        butbox = cls.dialog.component( 'buttonbox' )
        close = butbox.button( 0 )
        close.configure( foreground = 'blue', background = 'white' )
    
        hull = cls.dialog.component( 'hull' )
        sh = hull.winfo_screenheight()/4 
        sw = hull.winfo_screenwidth()/4
        hull.geometry( str( 325 )+"x"+str( 325 )+"+"+str(sw)+"+"+str(sh) )   
        frame = Tk.Frame( hull)
        frame.pack( fill = 'both', expand = 1 )
    
        words = [(xf, getattr(libconfig, xf)[-63:]) 
                    for xf in libconfig.ivars()
                        if xf in validlibs]
        words += [('lib', libconfig.lib[-63:]) ]
        words.sort(lambda xf, yf:cmp(xf[0],yf[0]))
        #lib should be the first entry, is not for editing.
        #words[:] = ('lib', libconfig.lib[-63:]) 
    
        cls.dropdown = Pmw.ComboBox(frame,
                selectioncommand = cls.changeLibs,
                scrolledlist_items = words,
                dropdown = 1,
        )
        cls.dropdown.pack(side = 'top', fill = 'both',
                expand = 1, padx = 2, pady = 2)
        cls.dropdown.selectitem(0, setentry = 1)
        
        cls.addList( frame )
    
    getDialog = classmethod(getDialog)
    #@nonl
    #@-node:ekr.20050328092641.16:getDialog
    #@+node:ekr.20050328092641.17:addList
    def addList(cls, frame ):
    
        cls.lbox = Pmw.ScrolledListBox( frame )
        lb = cls.lbox.component( 'listbox' )
        lb.configure( background = 'white', foreground = 'blue' )
        cls.setListContents()
        cls.lbox.pack( side = 'left' ) 
        frame2 = Tk.Frame( frame )
        frame2.pack( side = 'right' )
        insert = Tk.Button( frame2, text = 'Insert into outline' )
        insert.configure( background = 'white', foreground = 'blue' )
        insert.configure( command = cls.insert )
        insert.pack()
        remove = Tk.Button( frame2, text = 'Remove from list' )
        remove.configure( background = 'white', foreground = 'blue' )
        remove.configure( command = cls.delete )
        remove.pack()
        add = Tk.Button( frame2, text = 'Add Current Node to list' )
        add.configure( background = 'white', foreground = 'blue' )
        add.configure( command = cls.addCurrentNode )
        add.pack()
    addList = classmethod(addList)
    #@nonl
    #@-node:ekr.20050328092641.17:addList
    #@+node:ekr.20050328092641.18:setListContents
    def setListContents(cls):
        
        items = cls.names()
        items.sort()
        cls.lbox.setlist( items )
    setListContents = classmethod(setListContents)
    #@nonl
    #@-node:ekr.20050328092641.18:setListContents
    #@+node:ekr.20050328092641.19:changeLibs
    def changeLibs(cls, event):
        """whatevr is selected currently a tupple (libN, path)
         user can edit it in and screw it up probably
        """
        if libconfig.verbosity: g.trace(event)
    
        #and  if event[1] looks like a filename, but how to verify?
        #limiting to 6 slots for now
        if event and len(event) == 2 and event[0] in validlibs:
                pass
        else:
            g.es('non usable libN in libN {path}', color='red')
            return
        
        try:
            lib = cls.fixdefault(event[0], event[1]) 
        except Exception:
            g.es('non usable path in libN {path}', color='red')
            return
    
        if libconfig.verbosity: g.trace('newlib=%s'%lib)
        cls.shutdown()
        libconfig.lib = lib
        #now have to restart with the possibly new lib
        #doit the expediant way, ok, smaller words the easy way...
        #in production you would just reinitilize the lists
    
        #have to do this in cls.dlgCleanup so can save x&y location
        #plain destroy and new getdialog doesn't startup in the same place
        if Library.dialog: Library.dialog.destroy()
        Library.dialog = None
        cls.getDialog()
    
    changeLibs = classmethod(changeLibs)
    
    #@+at
    #   Event contents:
    #     char: ??
    #     delta: 0
    #     height: ??
    #     keycode: ??
    #     keysym: ??
    #     keysym_num: ??
    #     num: 1
    #     send_event: False
    #     serial: 3768
    #     state: 296
    #     time: 153250950
    #     type: 5
    #     widget: .23273640.23276240.23368968.23369848.23369768.23369728
    #     width: ??
    #     x: 34
    #     x_root: 476
    #     y: 29
    #     y_root: 317
    #@-at
    #@-node:ekr.20050328092641.19:changeLibs
    #@-node:ekr.20050328092641.15:GUI
    #@+node:ekr.20050328092641.20:db
    #@+node:ekr.20050328092641.21:remove
    def remove(cls, name ):
        
        del cls.db[ name ]
        cls.db.sync()
    remove = classmethod(remove)
    #@-node:ekr.20050328092641.21:remove
    #@+node:ekr.20050328092641.22:add (unicode)
    def add(cls, name, data ):
        #should check name is unicode, which might not work as a key?
        
        # data = data.encode( "ascii" , 'replace' )
        data = g.toEncodedString(data,"utf-8",reportErrors=True)
        
        data = zlib.compress( data, 9 )
        cls.db[ name ] = data
        cls.db.sync()
    add = classmethod(add)
    #@nonl
    #@-node:ekr.20050328092641.22:add (unicode)
    #@+node:ekr.20050328092641.23:retrieve (unicode)
    def retrieve(cls, name ):
        
        data = cls.db[ name ]
        data = zlib.decompress( data )
        # return unicode( data )
        return g.toUnicode(data,"utf-8",reportErrors=True)
    retrieve = classmethod(retrieve)
    #@nonl
    #@-node:ekr.20050328092641.23:retrieve (unicode)
    #@+node:ekr.20050328092641.24:names
    def names(cls):
    
        return cls.db.keys()
    names = classmethod(names)
    #@nonl
    #@-node:ekr.20050328092641.24:names
    #@+node:ekr.20050328092641.25:fixdefault
    def fixdefault(cls, libN, libname):
        """
        can't check isfile yet, anydbm might have to create it
        dido if the directory doesn't exist, up to the user.
        and in the process user gets to possibly trash good libconfig slot
        might the default also add the users leoID to the database name?
        """
    
        if libname == 'default': libname = 'default/library.dbm'
                
        if libname.find('default') != -1:
            pluginspath = g.os_path_join(g.app.loadDir, '../', "plugins")
    
            libname = g.os_path_normpath(g.os_path_abspath(
                libname.replace('default', pluginspath, 1) ))
            setattr(libconfig, libN, libname)
    
        elif libname.find('~') != -1:
            libname = g.os_path_normpath(g.os_path_abspath(
                    libname.replace('~', g.app.homeDir, 1) ))
            setattr(libconfig, libN, libname)
    
        return libname
    fixdefault = classmethod(fixdefault)
    #@nonl
    #@-node:ekr.20050328092641.25:fixdefault
    #@+node:ekr.20050328092641.26:shutdown
    def shutdown(cls):
        """anydbm just sync then forget it I guess
        no close mentioned in doc, but db.close exists
        should close() later when everything else works
        """
        if cls.db is not None and hasattr(cls.db, 'isOpen') and cls.db.isOpen(): 
            cls.db.sync()
        cls.db = None
        
        #might want to leave it accessable?
        #cls.path = path = libconfig.lib
        #del Library.openlibs[ path ]  #old
    
        return fatal
    shutdown = classmethod(shutdown)
    #@nonl
    #@-node:ekr.20050328092641.26:shutdown
    #@+node:ekr.20050328092641.27:startup
    def startup(cls):
        """Note: 'r' and 'w' fail if the database doesn't exist; 'c' creates it
        only if it doesn't exist; and 'n' always creates a new database.
        should this also read any @libsettings node in the database for interbal use
        such as node attributes that will stay with the database
        are node attributes from Leo preserved such as for templates plugin?
        """
        path = libconfig.lib
    
        if cls.path != path: #it may be open already
            if cls.db: cls.shutdown()
            cls.path = None
    
        #g.trace(cls.path)
    
        try:
            #probably won't have more than one db as the same path
            #but could have if shutdown does close() and openlibs isn't cleaned up
            if libconfig.verbosity: g.trace(path)
    
            # Set self.db.
    
            if cls.openlibs.has_key( path ):
                cls.db = cls.openlibs[ path ]
                if libconfig.verbosity: g.trace('reusing db on', path)
    
            elif g.os_path_exists( path ):
                cls.db = anydbm.open( path, "rw" )
                if libconfig.verbosity: g.trace('reopening db ', path)
                cls.openlibs[ path ] = cls.db  #do I need a deepcopy here?
    
            else:
                cls.db = anydbm.open( path, "c" ) 
                if libconfig.verbosity: g.trace('creating db ', path)
                cls.openlibs[ path ] = cls.db 
    
            cls.path = path
        except Exception, err: #anydbm.NODBwhatever
            #init() fails and gives user no chance to fix it
            # bad import msg isn't good enough to help diagnose
            g.es('NODB %s' %(err, ))
        
        #slight problem here, g.trace(self.db) is {} even when open
        #py2.2 doesn't want to open a new or existing database
        #or it doesn't have isOpen
        if cls.path and cls.db is not None and hasattr(cls.db, 'isOpen') and \
                cls.db.isOpen() and hasattr(cls.db, 'sync'): 
            return not fatal
    
        #g.trace(cls.db.isOpen())
        g.es('problem starting Library\n %s' %(path, ))
        return fatal
    startup = classmethod(startup)
    #@nonl
    #@-node:ekr.20050328092641.27:startup
    #@-node:ekr.20050328092641.20:db
    #@-others
#@-node:ekr.20050328092641.8:class Library
#@+node:ekr.20050328092641.28:init et al
#@+node:ekr.20050328092641.29:config
#from plugin_menu using the ini

#@+node:ekr.20050328092641.30:cmd_shutdown

def cmd_shutdown(): 
    """shutdown the current database
    this should also close all dialogs and do any cleanup
    shouldn't these get passed the current commander?
    """

    Library.shutdown()
    
#@nonl
#@-node:ekr.20050328092641.30:cmd_shutdown
#@+node:ekr.20050328092641.31:cmd_SetAsDefault

def cmd_SetAsDefault(): 
    """
    set the ini to the current options
    this can't really be implimented yet
    the ini is the only way to change options
    maybe this should write the recent librarys list to ini
    @settings, don't currently know where they are stored
    and for that matter, Library doesn't track where they came from.
    plugins should'nt be writting leoSettings.leo without user intervention?
    """
    g.es('edit the ini/@settings or use the Properties/Settings options')
#@-node:ekr.20050328092641.31:cmd_SetAsDefault
#@+node:ekr.20050328092641.32:cmd_ShowCurrent

def cmd_ShowCurrent(): 
    """
    no interest in maintaing seperate per leo defaults.
    """
    import whichdb
    
    g.es(libconfig)
    try:
        w = whichdb.whichdb(Library.path) 
    except Exception:
        w = None
    g.es('whichdb is [%s] at\n %s \nor %s'%(w, Library.path, libconfig.lib))
#@-node:ekr.20050328092641.32:cmd_ShowCurrent
#@+node:ekr.20050328092641.33:getConfiguration
def getConfiguration(): 
    """Return the config object
    should this look in homeDir first then plugins?   
    """ 
    fileName = g.os_path_join(g.app.loadDir,"..","plugins","Library.ini") 
    config = ConfigParser.ConfigParser() 
    config.read(fileName) 
    return config 
#@-node:ekr.20050328092641.33:getConfiguration
#@+node:ekr.20050328092641.34:applyConfiguration

def applyConfiguration(config):
    """plugin menu calls this in Properties after ini edit
    and override with any @settings and build libconfig
    no way to tell where the ivar lives in for updating.
    config/leoSettings.leo, $home or in the leo or ini(s).
    """

    if not config: return
    if config.has_option('Main', 'verbosity'): 
        xval = config.get('Main', 'verbosity')
        if ('%s'%(xval, )).strip().lower() in ('false', '0', 'off', 'f', ''):
            xval = 0
        else:
            xval = 1

        libconfig.verbosity = xval

    # lib1 thru libN, default/ or ~/whatever
    # the backend might determin which db in the next version

    for x in validlibs:
        try:
            xval = config.get("Main", x)
            #g.es(x, xval)
        except Exception:
            xval = None

        #this seems to be True even if option set to '' in ini
        if xval and xval != '':
            #g.es('ini setting %s %r'%( x, xval))
            setattr(libconfig, x, xval)

    #now check if there are any @settings
    #it would be better if you could positively get all settings for @plugins
    # and for @Library under @plugins, till then we guess a little
    #again lib0..5 a little limited but ok for now
    c = Library.c
    for x in validlibs:
        xval = c.config.getString('Library_'+x)
        if xval and xval != '':
            if libconfig.verbosity: 
                g.es('using @setting %s %r'%( x, xval))
            #Library.fixdefault(x, xval)
            setattr(libconfig, x, xval)

    #now veryify they have decent values
    #lib extension = 'dbm',  might be database dependant
    #should check is a valid file name and not something weird.
    #probably should try to create any directories too. let user handle it.

    for x in libconfig.ivars():
        #print x
        if x in validlibs:
            if hasattr(libconfig, x):
                attr = getattr(libconfig, x)
                Library.fixdefault(x, attr) 
    Library.fixdefault('lib', 'default') 
            

    #signal to redraw if its already open, should maybe do full cleanup?
    #the open lib may be no longer one of the choices!
    if Library.dialog: Library.dialog.destroy()
    Library.dialog = None  
#@nonl
#@-node:ekr.20050328092641.34:applyConfiguration
#@+node:ekr.20050328092641.35:@test _Configuration
#setup is getting to be more complicated than what is tested...
#maybe plugins should define __all__ = ['ok to exports'.split()]
#@+at
# if __name__ == '__builtin__':
#     from Library import *
#     #g.es(validlibs)
#     import leoGlobals as g
#     import ConfigParser
#     g.app.unitTesting = True
#     __file__ = 'Library.py'
#@-at
#@@c

if 0: # Fails unit test.

    def test_Configuration(): 
        """read the ini to save it or back it up
         or pass a StringIO mockable to getConfiguration, 
            write the ini with known values
          test they can be read back in the config object
            make sure if ini exists and is wrong
            or if it doesn't exist, defaults will be preserved.
        no mention of HOME for now
        its not vary convienent to run this with all the dependancies scattered
        likely similar with other more complicated tests
        but do it anyway as part of a more expanded test than plugin import?
        is False return enough or a raise Something? any print a failure?
        
        function name must be test_something but node can be @test something
        and I think doctests can be in any part of the plugin if those tests run.
        no claim yet this tests anything consequential.
        
        what might be useful is a options permutation generator:
        compare all perms of each of the Bunch the ini the @setting
         with valid and invalid possibly user [mis]edits of each and extras.
        do we end up with a valid usable Bunch of paths and options?
         are all the booleans boolable and all the ints and strings viable?
         will it be the same if user edits or changes the ini or @settings
        can we identify where each of the options comes from so on close/exit
         we can offer to update the correct ini or @setting node or just print changes.
        and investigate optparser for getting commandline options as well.
        I think Leo will just pass them on and not mangle them and not be confused.
        """ 
        
    
        #libc = g.Bunch(libconfig) or g.Bunch(dict(libconfig)) shoulv'e worked
        #print dir(libconfig)
    
        libc = libconfig.__dict__.copy()
        #why does Bunch not a copy and intersection method?
        #repr(l1) should be anough to reconstruct w/o additional parsing.
        #sets would be handy to find which settings are global which are per leo,
        #each setting should probably be a tupple of that kind of info. 
        
        #libc['libname'] = 'library00'
        #g.es(libc)
        #g.es(libconfig)
    
        fileName = g.os_path_join(
                g.app.loadDir,"..","plugins", __file__[:-2]+"ini") 
    
        config = ConfigParser.ConfigParser() 
        config.read(fileName) 
        applyConfiguration(config)
        
        #compare this config with getconfig and do in try/except
    
        liba = libconfig.__dict__.copy()
        g.es(libc)
        g.es(liba)
        
        #does this need an element by element comparison?
        return g.es(liba != libc)
        
    # comment this out to test with g.app.unitTesting
    if __name__ == '__builtin__':
    
        test_Configuration() != False
#@nonl
#@-node:ekr.20050328092641.35:@test _Configuration
#@-node:ekr.20050328092641.29:config
#@+node:ekr.20050328092641.36:onCreate
def onCreate( tag, keywords ):

    c = keywords.get('c')
    #g.trace(c )
    if not c: return

    men = c.frame.menu
    men = men.getMenu( 'Outline' )
    remen = Tk.Menu( men, tearoff = False)

    def onC(c):
        def doit(*ev):
            Library.getDialog(c)
        return doit

    men.add_command( label = "Library", command = onC(c))

    if libconfig.lib == 'default': #set to actual path on read ini
        try:
            Library.c = c
            #this is going to be one global config
            #does this even have to happen in init?
            #why slow down testing?  
            #maybe an option for fullblown test 
            # would doconfig and createmenu and any exotic imports
            #the user will have the most control over it working
            # did the ini get munged, are the exotics not installed etc
            applyConfiguration(getConfiguration())

            for x in validlibs:
                if hasattr(libconfig, x):
                    libconfig.lib = getattr(libconfig, x)
                    break 

        except Exception, er:
            #obviously will need to catch the actual error
            g.es('error in plugin/Library.ini ', er, color='red')
#@nonl
#@-node:ekr.20050328092641.36:onCreate
#@+node:ekr.20050328092641.37:onCleanup
def onCleanup( tag, keywords ):
    """this depends on how far along the recent librarys feature is.
    this is called on every close should maintain a changed flag maybe
    so don't repetedly check the ini and recent files.
    maybe check global window list and update then.
    user can update anytime with cmd_setdefaults?

    destroy all global windows isn't caught on close
    """

    c = keywords.get('c') 

    cmd_shutdown()
    
    if Library.c == c:
        if Library.dialog: Library.dialog.destroy()
        Library.dialog = None
        Library.c = None

    #look in ini and write library1, libraryN remove dups, perserve order?
    #maybe just the last leo window should do this
    #and need a button on the dlg to write them also
    if libconfig.verbosity:
        for k,v in Library.openlibs.iteritems():
            g.trace(k)

    
#@nonl
#@-node:ekr.20050328092641.37:onCleanup
#@+node:ekr.20050328092641.38:init
def init():
    """this is getting to be ok overload
    """
    ok = Tk and Pmw and zlib and not g.app.unitTesting

    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__ )
    
        ok = g.app.gui.guiName() == "tkinter"
    
        if ok:
            leoPlugins.registerHandler("after-create-leo-frame", onCreate)
            leoPlugins.registerHandler("close-frame", onCleanup)
            g.plugin_signon(__name__ )
    return ok
#@nonl
#@-node:ekr.20050328092641.38:init
#@-node:ekr.20050328092641.28:init et al
#@-others

#@@color
#@nonl
#@-node:ekr.20050328092641.4:@thin Library.py
#@-leo
