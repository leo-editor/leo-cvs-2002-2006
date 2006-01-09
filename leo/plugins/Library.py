#@+leo-ver=4-thin
#@+node:ekr.20050328092641.4:@thin Library.py
#@<< docstring >>
#@+node:ekr.20050912180445:<< docstring >>
'''A plugin to store Leo trees in database files.

This plugin creates the following in the Plugins:Library menu:
    
- 

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

#@@language python
#@@tabwidth -4

__version__ = ".5" 

#@<< version history >>
#@+node:ekr.20050328092641.6:<< version history >>
#@@color

#@<< versions before .5 >>
#@+node:ekr.20060108172052:<< versions before .5 >>
#@@nocolor
#@+at
# 0.0 created by the plugin guy & posted to the Leo forums.
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
#@-at
#@nonl
#@-node:ekr.20060108172052:<< versions before .5 >>
#@nl

#@@nocolor
#@+at
# .5 EKR: A major rewrite.
# - Removed all calls to g.top.
# - Added c argument to all cmd_ functions.
# - Created per-commander instances of Libary classes.
#   (This is the only sane way).
# - Created libraries dict to access proper Library class.
# - Converted all methods to normal (non-static) methods.
# - Use settings, not ini files.
#@-at
#@nonl
#@-node:ekr.20050328092641.6:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20050328092641.7:<< imports >>
import leoGlobals as g
import leoPlugins
import anydbm
import ConfigParser
import whichdb

Tk   = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
Pmw  = g.importExtension("Pmw",    pluginName=__name__,verbose=True)
zlib = g.importExtension("zlib",   pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20050328092641.7:<< imports >>
#@nl

libraries = {}  # Keys are commanders, values are Library objects.
dbs = {}        # Keys are full paths.  values are databases.

libconfig = g.Bunch(
    lib = 'default',  #don't touch this one nor use lib=
    #you can hardwire in your own favorites, change the ini or add @setting
    lib0 = 'default/library.dbm',
    verbosity = 0,
)

validlibs = ['lib0', 'lib1', 'lib2', 'lib3', 'lib4', 'lib5',]

#@+others
#@+node:ekr.20060108171207:Moduel-level functions
#@+node:ekr.20050328092641.38:init
def init():

    ok = Tk and Pmw and zlib and not g.app.unitTesting
    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__ )
    
        ok = g.app.gui.guiName() == "tkinter"
    
        if ok:
            leoPlugins.registerHandler("after-create-leo-frame", onCreate)
            leoPlugins.registerHandler("close-frame", onCloseFrame)
            g.plugin_signon(__name__ )

    return ok
#@nonl
#@-node:ekr.20050328092641.38:init
#@+node:ekr.20050328092641.36:onCreate
def onCreate (tag,keywords):

    c = keywords.get('c')
    if c and c.exists:
        global libraries
        libraries[c] = Library(c)
#@nonl
#@-node:ekr.20050328092641.36:onCreate
#@+node:ekr.20050328092641.37:onCloseFrame
def onCloseFrame (tag,keywords):

    c = keywords.get('c')
    if not c or not c.exists: return

    global libraries
    lib = libraries.get(c)
    if lib:
        del libraries [c]
        lib.destroySelf()
#@nonl
#@-node:ekr.20050328092641.37:onCloseFrame
#@+node:ekr.20050328092641.28:cmd_ methods
#@+node:ekr.20050328092641.30:cmd_shutdown
def cmd_shutdown(c): 
    
    lib = libraries.get(c)
    if lib:
        lib.destorySelf()
#@nonl
#@-node:ekr.20050328092641.30:cmd_shutdown
#@+node:ekr.20050328092641.32:cmd_ShowCurrent
def cmd_ShowCurrent(c): 
    
    lib = libraries.get(c)
    if lib:
        lib.showCurrent()
#@nonl
#@-node:ekr.20050328092641.32:cmd_ShowCurrent
#@+node:ekr.20060108191608:cmd_ShowDialog
def cmd_ShowDialog (c):
    
    lib = libraries.get(c)
    if lib:
        lib.showDialog()
#@nonl
#@-node:ekr.20060108191608:cmd_ShowDialog
#@-node:ekr.20050328092641.28:cmd_ methods
#@-node:ekr.20060108171207:Moduel-level functions
#@+node:ekr.20050328092641.8:class Library
class Library(object):

    '''This class presents an interface through which a Libray can be used.
    It also provides a gui dialog to interact with the Library.

    all methods are now classmethods 
    the commander that is last retrieved from keywords is the one used.
    
    '''
    
    #@    @+others
    #@+node:ekr.20060108184110:Birth & death
    #@+node:ekr.20050328092641.9:__init__
    def __init__ (self,c):
    
        self.c = c
        self.db = None
        self.openlibs = {} # keys are db's.
        self.path = None
        self.dialog = None
        self.verbose = True
        
        # Create the db.
        self.startup()
        if self.db is not None:
            self.config()
            self.createDialog()
    #@nonl
    #@-node:ekr.20050328092641.9:__init__
    #@+node:ekr.20060108184110.2:config
    def config (self):
        
        c = self.c
        pass
        
        # if libconfig.lib == 'default': #set to actual path on read ini
            # try:
                # applyConfiguration(getConfiguration())
                # for x in validlibs:
                    # if hasattr(libconfig,x):
                        # libconfig.lib = getattr(libconfig,x)
                        # break
            # except Exception, er:
                # #obviously will need to catch the actual error
                # g.es('error in plugin/Library.ini ',er,color='red')
       
    #@+at         
    # ;default/ is leo/plugins  ~/ is your $HOME env var as seen by leo
    # ; if there is an @setting Library_lib* somewhere it will override the 
    # ini
    # ;there are no provisions yet to change the @setting but hitting 
    # Preferences apply
    # ; from the plugin_menu will reread the ini and the @setting
    # ; you could even change the setting by script then hit apply for now.
    # ; delete or comment out the ones you won't be using.
    # 
    # ; verbosity can be true, True, 1 on, False 0 , turns on extra internal 
    # feedback
    # 
    # [Main]
    # verbosity=0
    # ;lib* = eventually, don't use lib=  it is to be the current lib
    # ; only impliemented lib0..5 for now. lib0 is the opening lib
    # 
    # ;lib0 = default/library.dbm
    # lib1 = default/library1.dbm
    # ;lib2 = default/library22.dbm
    # ;lib3 = default/library23.dbm
    # ;lib4 = default/library24.dbm
    # 
    # ;lib5 = ~/libraryMy.dbm
    # ;libLa = C:\c\leo\libraryL.dbm
    # ;libLb = C:/c/leo/libraryL.dbm
    #@-at
    #@nonl
    #@-node:ekr.20060108184110.2:config
    #@+node:ekr.20060108185916:createDialog
    def createDialog (self):
        
        c = self.c
        title = c.shortFileName()
        self.dialog = Pmw.Dialog(buttons=('Close',),title=title)
        butbox = self.dialog.component('buttonbox')
        close = butbox.button(0)
        close.configure(foreground='blue',background='white')
    
        hull = self.dialog.component('hull')
        sh = hull.winfo_screenheight() / 4
        sw = hull.winfo_screenwidth() / 4
        hull.geometry(str(325)+"x"+str(325)+"+"+str(sw)+"+"+str(sh))
        frame = Tk.Frame(hull)
        frame.pack(fill='both',expand=1)
    
        words = [(xf,getattr(libconfig,xf)[-63:])
                    for xf in libconfig.ivars()
                        if xf in validlibs]
        words += [('lib',libconfig.lib[-63:])]
        words.sort(lambda xf,yf: cmp(xf[0],yf[0]))
    
        self.dropdown = Pmw.ComboBox(frame,
            selectioncommand = self.changeLibs,
            scrolledlist_items = words,
            dropdown = 1,
        )
        self.dropdown.pack(side='top',fill='both',expand=1,padx=2,pady=2)
        self.dropdown.selectitem(0,setentry=1)
    
        self.addList(frame)
        self.dialog.withdraw()
    #@nonl
    #@-node:ekr.20060108185916:createDialog
    #@-node:ekr.20060108184110:Birth & death
    #@+node:ekr.20060108174201:destroySelf
    def destroySelf (self):
    
        if 0:
            if self.verbose:
                for k, v in self.openlibs.iteritems():
                    g.trace(k)
                
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
    #@nonl
    #@-node:ekr.20060108174201:destroySelf
    #@+node:ekr.20060108174432:showCurrent
    def showCurrent (self):
        
        g.es(libconfig)
        try:
            w = whichdb.whichdb(self.path) 
        except Exception:
            w = None
    
        g.es('whichdb is [%s] at\n %s \nor %s'%(w, self.path, libconfig.lib))
    #@nonl
    #@-node:ekr.20060108174432:showCurrent
    #@+node:ekr.20050328092641.10:buttons
    #@+node:ekr.20050328092641.11:insert
    def insert (self):
    
        c = self.c
        item = self.lbox.getvalue()
        if not item: return
        item = item [0]
        s = self.retrieve(item)
    
        #preserve the users clippboard
        stext = g.app.gui.getTextFromClipboard()
        g.app.gui.replaceClipboardWith(s)
        c.pasteOutline()
        g.app.gui.replaceClipboardWith(stext)
    #@nonl
    #@-node:ekr.20050328092641.11:insert
    #@+node:ekr.20050328092641.12:delete
    def delete (self):
    
        c = self.c
        item = self.lbox.getvalue()
        if not item: return
        item = item [0]
        self.remove(item)
        self.setListContents()
    #@nonl
    #@-node:ekr.20050328092641.12:delete
    #@+node:ekr.20050328092641.13:addCurrentNode
    def addCurrentNode (self):
    
        c = self.c ; p = c.currentPosition()
        hs = str(p.headString())
        s = c.fileCommands.putLeoOutline()
        self.add(hs,s)
        self.setListContents()
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
    #@+node:ekr.20050328092641.16:showDialog
    def showDialog (self):
    
        c = self.c
        
        g.trace(self.dialog)
    
        if c and c.exists and self.db is not None:
            self.dialog.deiconify()
    #@nonl
    #@-node:ekr.20050328092641.16:showDialog
    #@+node:ekr.20050328092641.17:addList
    def addList (self,frame):
    
        self.lbox = Pmw.ScrolledListBox(frame)
        lb = self.lbox.component('listbox')
        lb.configure(background='white',foreground='blue')
        self.setListContents()
        self.lbox.pack(side='left')
        frame2 = Tk.Frame(frame)
        frame2.pack(side='right')
        insert = Tk.Button(frame2,text='Insert into outline')
        insert.configure(background='white',foreground='blue')
        insert.configure(command=self.insert)
        insert.pack()
        remove = Tk.Button(frame2,text='Remove from list')
        remove.configure(background='white',foreground='blue')
        remove.configure(command=self.delete)
        remove.pack()
        add = Tk.Button(frame2,text='Add Current Node to list')
        add.configure(background='white',foreground='blue')
        add.configure(command=self.addCurrentNode)
        add.pack()
    #@nonl
    #@-node:ekr.20050328092641.17:addList
    #@+node:ekr.20050328092641.18:setListContents
    def setListContents (self):
    
        items = self.names()
        items.sort()
        self.lbox.setlist(items)
    #@nonl
    #@-node:ekr.20050328092641.18:setListContents
    #@+node:ekr.20050328092641.19:changeLibs
    def changeLibs (self,event):
        """whatevr is selected currently a tupple (libN, path)
         user can edit it in and screw it up probably
        """
        if self.verbose: g.trace(event)
    
        if event and len(event) == 2 and event [0] in validlibs:
            pass
        else:
            g.es('non usable libN in libN {path}',color='red')
            return
    
        try:
            lib = self.fixdefault(event[0],event[1])
        except Exception:
            g.es('non usable path in libN {path}',color='red')
            return
    
        if self.verbose: g.trace('newlib=%s' % lib)
        self.shutdown()
        libconfig.lib = lib
        if self.dialog:
            self.dialog.destroy()
            self.dialog = self.createDialog()
        self.showDialog()
    #@nonl
    #@-node:ekr.20050328092641.19:changeLibs
    #@-node:ekr.20050328092641.15:GUI
    #@+node:ekr.20050328092641.20:db
    #@+node:ekr.20050328092641.22:add (unicode)
    def add (self,name,data):
    
        data = g.toEncodedString(data,"utf-8",reportErrors=True)
        data = zlib.compress(data,9)
        self.db [name] = data
        self.db.sync()
    #@nonl
    #@-node:ekr.20050328092641.22:add (unicode)
    #@+node:ekr.20050328092641.25:fixdefault
    def fixdefault (self,libN,libname):
        """
        can't check isfile yet, anydbm might have to create it
        dido if the directory doesn't exist, up to the user.
        and in the process user gets to possibly trash good libconfig slot
        might the default also add the users leoID to the database name?
        """
    
        if libname == 'default': libname = 'default/library.dbm'
    
        if libname.find('default') != -1:
            pluginspath = g.os_path_join(g.app.loadDir,'../',"plugins")
            libname = g.os_path_normpath(g.os_path_abspath(
                libname.replace('default',pluginspath,1)))
            setattr(libconfig,libN,libname)
    
        elif libname.find('~') != -1:
            libname = g.os_path_normpath(g.os_path_abspath(
                libname.replace('~',g.app.homeDir,1)))
            setattr(libconfig,libN,libname)
    
        return libname
    #@nonl
    #@-node:ekr.20050328092641.25:fixdefault
    #@+node:ekr.20050328092641.24:names
    def names(self):
    
        return self.db.keys()
    #@nonl
    #@-node:ekr.20050328092641.24:names
    #@+node:ekr.20050328092641.21:remove
    def remove (self,name):
    
        del self.db [name]
        self.db.sync()
    #@nonl
    #@-node:ekr.20050328092641.21:remove
    #@+node:ekr.20050328092641.23:retrieve (unicode)
    def retrieve (self,name):
    
        data = self.db [name]
        data = zlib.decompress(data)
        return g.toUnicode(data,"utf-8",reportErrors=True)
    #@nonl
    #@-node:ekr.20050328092641.23:retrieve (unicode)
    #@+node:ekr.20050328092641.26:shutdown
    def shutdown(self):
        '''Close self.db.'''
        
        db = self.db
        
        if db is None: return
    
        if hasattr(db,'isOpen') and db.isOpen():
            if hasattr(db,'synch'): db.synch()
            if hasattr(db,'close'): db.close()
    
        self.db = None
    #@nonl
    #@-node:ekr.20050328092641.26:shutdown
    #@+node:ekr.20050328092641.27:startup
    def startup (self):
        
        path = libconfig.lib ; verbose = self.verbose
        
        global libraries
    
        try:
            # 'r' and 'w' fail if the database doesn't exist.
            # 'c' creates it only if it doesn't exist.
            # 'n' always creates a new database.
            if self.verbose: g.trace('Library path:',path)
    
            if self.openlibs.has_key(path):
                self.db = self.openlibs [path]
                if verbose: g.trace('reusing db on',path)
            elif g.os_path_exists(path):
                self.db = anydbm.open(path,"rw")
                if verbose: g.trace('reopening db ',path)
                self.openlibs [path] = self.db #do I need a deepcopy here?
            else:
                if verbose: g.trace('creating db ',path)
                self.db = anydbm.open(path,"c")
            self.path = path
        except Exception, err:
            g.es('Exception creating Library database %s' % (err,))
    
        ok = (self.path and self.db and
            hasattr(self.db,'isOpen') and self.db.isOpen() and hasattr(self.db,'sync'))
        if ok:
            self.openlibs [path] = self.db
        else:
            g.es('problem starting Library\n %s' % (path,))
        return ok
    #@nonl
    #@-node:ekr.20050328092641.27:startup
    #@-node:ekr.20050328092641.20:db
    #@-others
#@nonl
#@-node:ekr.20050328092641.8:class Library
#@-others

#@-node:ekr.20050328092641.4:@thin Library.py
#@-leo
