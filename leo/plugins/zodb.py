#@+leo-ver=4-thin
#@+node:ekr.20050825154553:@thin zodb.py
#@<< docstring >>
#@+node:ekr.20050825154605:<< docstring >>
'''A plugin that stores all Leo outline data in a single zodb database.

This plugin replaces the Open, Save and Revert commands with methods that
access the zodb database.
'''
#@nonl
#@-node:ekr.20050825154605:<< docstring >>
#@nl

# WARNING:
# WARNING: highly experimental code:  USE AT YOUR OWN RISK.
# WARNING:

__version__ = '0.0.1'

#@<< imports >>
#@+node:ekr.20050825154553.1:<< imports >>
import leoGlobals as g

import leoNodes

try:
    import ZODB
    import ZODB.FileStorage
    ok = True
except ImportError:
    ok = False
#@nonl
#@-node:ekr.20050825154553.1:<< imports >>
#@nl
#@<< change log >>
#@+node:ekr.20050825154553.2:<< change log >>
#@@nocolor

#@+at 
#@nonl
# This plugin was written by Edward K. Ream.
# 
# 0.0.1: Initial version.
# 
# - Experimented with replacing tnode class from this plugin.
#     - Apparently,
#@-at
#@nonl
#@-node:ekr.20050825154553.2:<< change log >>
#@nl
#@<< to do >>
#@+node:ekr.20050825154553.3:<< to do >>
#@@nocolor

#@+at
# 
# - Override openWithFileName, and write_LEO_file
# 
# - Create 'open', 'save' hooks ??
#@-at
#@nonl
#@-node:ekr.20050825154553.3:<< to do >>
#@nl

# This should be a user option, and should NOT be a module-level symbol.

zodb_filename = r"c:\prog\zopeTemp\leo.fs"

#@<< define base classes for classes in leoNodes.py >>
#@+node:ekr.20050825195543:<< define base classes for classes in leoNodes.py >>
# The original classes in leoNodes.py are subclasses only of object.

class persistent (ZODB.Persistence.Persistent,object):
    # To eliminate a meta-class conflict.
    pass

if 0: # This doesn't work
    class baseZODBTnodeClass (ZODB.Persistence.Persistent):
        pass
    class baseZODBVnodeClass (ZODB.Persistence.Persistent):
        pass
    class baseZODBPositionClass (ZODB.Persistence.Persistent):
        pass
    
if 0: # meta-class conflict
    class ZODBtnodeClass (leoNodes.baseTnode,persistent):
        def __init__ (self,bodyString=None,headString=None):
            # Init the base classes.
            leoNodes.baseTnode.__init__(self,bodyString,headString)
            persistent.__init__(self)

if 0: # Not yet.
    
    class ZODBvnodeClass (leoNodes.baseVnode,ZODB.Persistence.Persistent):
        pass
        
    class ZODBpositionClass (leoNodes.basePosition,ZODB.Persistence.Persistent):
        pass
#@nonl
#@-node:ekr.20050825195543:<< define base classes for classes in leoNodes.py >>
#@nl

#@+others
#@+node:ekr.20050825165419:Module level...
#@+node:ekr.20050825155043:init
def init ():
    
    global ok, zodb_filename
    
    if g.app.unitTesting:
        return False
        
    if not ok:
        s = 'zodb plugin not loaded: can not import zodb'
        print s ; g.es(s,color='red')
        return False

    controller = zodbControllerClass(zodb_filename)
    ok = controller.init()
        
    if ok:
        patchLeoCore(controller)
        g.plugin_signon(__name__)
    else:
        s = 'zodb plugin not loaded: can not open zodb'
        print s ; g.es(s,color='red')

    return ok
#@nonl
#@-node:ekr.20050825155043:init
#@+node:ekr.20050825162326:patchLeoCore
def patchLeoCore (controller):
        
    g.trace('patching base classes in leoNodes.py')

    tnode = buildTnodeClass()
    
    #g.trace('issubclass object',issubclass(tnode,object))
    #g.trace('issubclass baseClass',issubclass(tnode,baseClass))
    
    # This is a major change.  
    
    leoNodes.tnode = tnode
#@nonl
#@-node:ekr.20050825162326:patchLeoCore
#@-node:ekr.20050825165419:Module level...
#@+node:ekr.20050825155228.1:class zodbControllerClass
class zodbControllerClass:
    
    '''A singleton controller class for the zodb database attached to zodb_filename.'''
    
    #@    @+others
    #@+node:ekr.20050825155308: ctor (zodbControllerClass)
    def __init__ (self,zodb_filename):
    
        self.canOpen = False
        self.connection = None
        self.storage = None
        self.zodb_filename = zodb_filename
    #@nonl
    #@-node:ekr.20050825155308: ctor (zodbControllerClass)
    #@+node:ekr.20050825162137.2:close
    def close (self):
        
        if self.storage and self.connection:
            self.connection.close()
            self.connection = None
    #@nonl
    #@-node:ekr.20050825162137.2:close
    #@+node:ekr.20050825162137.1:getRoot
    def getRoot (self):
        
        if not self.connection:
            return None
    
        root = self.connection.root()
        if 0:
            t = get_transaction()
            t.begin()
            # root.clear()
            root ['count'] = root.get('count',0) + 1
            t.commit()
        g.trace(root)
        return root
    #@nonl
    #@-node:ekr.20050825162137.1:getRoot
    #@+node:ekr.20050825164039:init
    def init (self):
        
        try:
            try:
                self.storage = ZODB.FileStorage.FileStorage(self.zodb_filename)
                self.open()
                ok = self.isOpen()
                g.trace(self.storage,self.connection)
            except Exception:
                g.es_exception()
                ok = False
        finally:
            self.close()
            
        return ok
    #@nonl
    #@-node:ekr.20050825164039:init
    #@+node:ekr.20050825162137:isOpen
    def isOpen (self):
        
        return self.storage is not None and self.connection is not None
    #@nonl
    #@-node:ekr.20050825162137:isOpen
    #@+node:ekr.20050825160255.2:open
    def open(self):
        
        if not self.storage:
            return None
        
        if not self.connection:
            try:
                self.connection = ZODB.DB(self.storage)
            except Exception:
                self.connection = None
            
        return self.connection
    #@nonl
    #@-node:ekr.20050825160255.2:open
    #@-others
#@nonl
#@-node:ekr.20050825155228.1:class zodbControllerClass
#@+node:ekr.20050825165338:Overrides of core methods
#@+node:ekr.20050825165912:zodb_openWithFileName (from leoGlobals)
def openWithFileName(fileName,old_c,enableLog=True,readAtFileNodesFlag=True):
    
    """Create a Leo Frame for the indicated fileName if the file exists."""

    if not fileName or len(fileName) == 0:
        return False, None
        
    def munge(name):
        name = name or ''
        return g.os_path_normpath(name).lower()

    # Create a full, normalized, Unicode path name, preserving case.
    fileName = g.os_path_normpath(g.os_path_abspath(fileName))

    # If the file is already open just bring its window to the front.
    theList = app.windowList
    for frame in theList:
        if munge(fileName) == munge(frame.c.mFileName):
            frame.bringToFront()
            app.setLog(frame.log,"openWithFileName")
            # g.trace('Already open',fileName)
            return True, frame
    try:
        # g.trace('Not open',fileName)
        # Open the file in binary mode to allow 0x1a in bodies & headlines.
        theFile = open(fileName,'rb')
        c,frame = app.gui.newLeoCommanderAndFrame(fileName)
        frame.log.enable(enableLog)
        g.app.writeWaitingLog() # New in 4.3: write queued log first.
        if not g.doHook("open1",old_c=old_c,c=c,new_c=c,fileName=fileName):
            app.setLog(frame.log,"openWithFileName")
            app.lockLog()
            frame.c.fileCommands.open(
                theFile,fileName,
                readAtFileNodesFlag=readAtFileNodesFlag) # closes file.
            app.unlockLog()
            for frame in g.app.windowList:
                # The recent files list has been updated by menu.updateRecentFiles.
                frame.c.config.setRecentFiles(g.app.config.recentFiles)
        frame.openDirectory = g.os_path_dirname(fileName)
        g.doHook("open2",old_c=old_c,c=c,new_c=frame.c,fileName=fileName)
        return True, frame
    except IOError:
        # Do not use string + here: it will fail for non-ascii strings!
        if not g.app.unitTesting:
            g.es("can not open: %s" % (fileName), color="blue")
        return False, None
    except Exception:
        g.es("exceptions opening: %s" % (fileName),color="red")
        g.es_exception()
        return False, None
#@nonl
#@-node:ekr.20050825165912:zodb_openWithFileName (from leoGlobals)
#@+node:ekr.20050825171046:zodb_write_Leo_file (from fileCommands)
def zodb_write_Leo_file(self,fileName,outlineOnlyFlag):

    c = self.c
    self.assignFileIndices()
    if not outlineOnlyFlag:
        # Update .leoRecentFiles.txt if possible.
        g.app.config.writeRecentFilesFile(c)
        #@        << write all @file nodes >>
        #@+node:ekr.20050825171046.1:<< write all @file nodes >>
        try:
            # Write all @file nodes and set orphan bits.
            c.atFileCommands.writeAll()
        except Exception:
            g.es_error("exception writing derived files")
            g.es_exception()
            return False
        #@nonl
        #@-node:ekr.20050825171046.1:<< write all @file nodes >>
        #@nl
    #@    << return if the .leo file is read-only >>
    #@+node:ekr.20050825171046.2:<< return if the .leo file is read-only >>
    # self.read_only is not valid for Save As and Save To commands.
    
    if g.os_path_exists(fileName):
        try:
            if not os.access(fileName,os.W_OK):
                g.es("can not create: read only: " + fileName,color="red")
                return False
        except:
            pass # os.access() may not exist on all platforms.
    #@nonl
    #@-node:ekr.20050825171046.2:<< return if the .leo file is read-only >>
    #@nl
    try:
        theActualFile = None
        #@        << create backup file >>
        #@+node:ekr.20050825171046.3:<< create backup file >>
        # rename fileName to fileName.bak if fileName exists.
        if g.os_path_exists(fileName):
            backupName = g.os_path_join(g.app.loadDir,fileName)
            backupName = fileName + ".bak"
            if g.os_path_exists(backupName):
                g.utils_remove(backupName)
            ok = g.utils_rename(fileName,backupName)
            if not ok:
                if self.read_only:
                    g.es("read only",color="red")
                return False
        else:
            backupName = None
        #@nonl
        #@-node:ekr.20050825171046.3:<< create backup file >>
        #@nl
        self.mFileName = fileName
        self.outputFile = cStringIO.StringIO() # or g.fileLikeObject()
        theActualFile = open(fileName, 'wb')
        #@        << put the .leo file >>
        #@+node:ekr.20050825171046.4:<< put the .leo file >>
        self.putProlog()
        self.putHeader()
        self.putGlobals()
        self.putPrefs()
        self.putFindSettings()
        #start = g.getTime()
        self.putVnodes()
        #start = g.printDiffTime("vnodes ",start)
        self.putTnodes()
        #start = g.printDiffTime("tnodes ",start)
        self.putPostlog()
        #@nonl
        #@-node:ekr.20050825171046.4:<< put the .leo file >>
        #@nl
        theActualFile.write(self.outputFile.getvalue())
        theActualFile.close()
        self.outputFile = None
        #@        << delete backup file >>
        #@+node:ekr.20050825171046.5:<< delete backup file >>
        if backupName and g.os_path_exists(backupName):
        
            self.deleteFileWithMessage(backupName,'backup')
        #@nonl
        #@-node:ekr.20050825171046.5:<< delete backup file >>
        #@nl
        return True
    except Exception:
        g.es("exception writing: " + fileName)
        g.es_exception(full=False)
        if theActualFile: theActualFile.close()
        self.outputFile = None
        #@        << delete fileName >>
        #@+node:ekr.20050825171046.6:<< delete fileName >>
        if fileName and g.os_path_exists(fileName):
            self.deleteFileWithMessage(fileName,'')
        #@-node:ekr.20050825171046.6:<< delete fileName >>
        #@nl
        #@        << rename backupName to fileName >>
        #@+node:ekr.20050825171046.7:<< rename backupName to fileName >>
        if backupName:
            g.es("restoring " + fileName + " from " + backupName)
            g.utils_rename(backupName,fileName)
        #@nonl
        #@-node:ekr.20050825171046.7:<< rename backupName to fileName >>
        #@nl
        return False
#@nonl
#@-node:ekr.20050825171046:zodb_write_Leo_file (from fileCommands)
#@+node:ekr.20050825171046.8:No change required
if 0:
    
    #@    @+others
    #@+node:ekr.20050825165823:top level file commands
    #@+node:ekr.20050825165823.2:open
    def open(self):
    
        c = self
        #@    << Set closeFlag if the only open window is empty >>
        #@+node:ekr.20050825165823.3:<< Set closeFlag if the only open window is empty >>
        #@+at 
        #@nonl
        # If this is the only open window was opened when the app started, and 
        # the window has never been written to or saved, then we will 
        # automatically close that window if this open command completes 
        # successfully.
        #@-at
        #@@c
            
        closeFlag = (
            c.frame.startupWindow and # The window was open on startup
            not c.changed and not c.frame.saved and # The window has never been changed
            g.app.numberOfWindows == 1) # Only one untitled window has ever been opened
        #@nonl
        #@-node:ekr.20050825165823.3:<< Set closeFlag if the only open window is empty >>
        #@nl
    
        fileName = g.app.gui.runOpenFileDialog(
            title="Open",
            filetypes=[("Leo files", "*.leo"), ("All files", "*")],
            defaultextension=".leo")
    
        if fileName and len(fileName) > 0:
            ok, frame = g.openWithFileName(fileName,c)
            if ok and closeFlag:
                g.app.destroyWindow(c.frame)
    #@nonl
    #@-node:ekr.20050825165823.2:open
    #@+node:ekr.20050825165823.4:openWith and allies
    def openWith(self,data=None):
    
        """This routine handles the items in the Open With... menu.
    
        These items can only be created by createOpenWithMenuFromTable().
        Typically this would be done from the "open2" hook.
        
        New in 4.3: The "os.spawnv" now works. You may specify arguments to spawnv
        using a list, e.g.:
            
        openWith("os.spawnv", ["c:/prog.exe","--parm1","frog","--switch2"], None)
        """
        
        c = self ; p = c.currentPosition()
        if not data or len(data) != 3:
            g.trace('bad data')
            return
        try:
            openType,arg,ext=data
            if not g.doHook("openwith1",c=c,p=p,v=p.v,openType=openType,arg=arg,ext=ext):
                #@            << set ext based on the present language >>
                #@+node:ekr.20050825165823.5:<< set ext based on the present language >>
                if not ext:
                    theDict = g.scanDirectives(c)
                    language = theDict.get("language")
                    ext = g.app.language_extension_dict.get(language)
                    # print language,ext
                    if ext == None:
                        ext = "txt"
                    
                if ext[0] != ".":
                    ext = "."+ext
                    
                # print "ext",ext
                #@nonl
                #@-node:ekr.20050825165823.5:<< set ext based on the present language >>
                #@nl
                #@            << create or reopen temp file, testing for conflicting changes >>
                #@+node:ekr.20050825165823.6:<< create or reopen temp file, testing for conflicting changes >>
                theDict = None ; path = None
                #@<< set dict and path if a temp file already refers to p.v.t >>
                #@+node:ekr.20050825165823.7:<<set dict and path if a temp file already refers to p.v.t >>
                searchPath = c.openWithTempFilePath(p,ext)
                
                if g.os_path_exists(searchPath):
                    for theDict in g.app.openWithFiles:
                        if p.v == theDict.get('v') and searchPath == theDict.get("path"):
                            path = searchPath
                            break
                #@-node:ekr.20050825165823.7:<<set dict and path if a temp file already refers to p.v.t >>
                #@nl
                if path:
                    #@    << create or recreate temp file as needed >>
                    #@+node:ekr.20050825165823.8:<< create or recreate temp file as needed >>
                    #@+at 
                    #@nonl
                    # We test for changes in both p and the temp file:
                    # 
                    # - If only p's body text has changed, we recreate the 
                    # temp file.
                    # - If only the temp file has changed, do nothing here.
                    # - If both have changed we must prompt the user to see 
                    # which code to use.
                    #@-at
                    #@@c
                    
                    encoding = theDict.get("encoding")
                    old_body = theDict.get("body")
                    new_body = p.bodyString()
                    new_body = g.toEncodedString(new_body,encoding,reportErrors=True)
                    
                    old_time = theDict.get("time")
                    try:
                        new_time = g.os_path_getmtime(path)
                    except:
                        new_time = None
                        
                    body_changed = old_body != new_body
                    temp_changed = old_time != new_time
                    
                    if body_changed and temp_changed:
                        #@    << Raise dialog about conflict and set result >>
                        #@+node:ekr.20050825165823.9:<< Raise dialog about conflict and set result >>
                        message = (
                            "Conflicting changes in outline and temp file\n\n" +
                            "Do you want to use the code in the outline or the temp file?\n\n")
                        
                        result = g.app.gui.runAskYesNoCancelDialog(c,
                            "Conflict!", message,
                            yesMessage = "Outline",
                            noMessage = "File",
                            defaultButton = "Cancel")
                        #@nonl
                        #@-node:ekr.20050825165823.9:<< Raise dialog about conflict and set result >>
                        #@nl
                        if result == "cancel": return
                        rewrite = result == "outline"
                    else:
                        rewrite = body_changed
                            
                    if rewrite:
                        path = c.createOpenWithTempFile(p,ext)
                    else:
                        g.es("reopening: " + g.shortFileName(path),color="blue")
                    #@nonl
                    #@-node:ekr.20050825165823.8:<< create or recreate temp file as needed >>
                    #@nl
                else:
                    path = c.createOpenWithTempFile(p,ext)
                
                if not path:
                    return # An error has occured.
                #@nonl
                #@-node:ekr.20050825165823.6:<< create or reopen temp file, testing for conflicting changes >>
                #@nl
                #@            << execute a command to open path in external editor >>
                #@+node:ekr.20050825165823.10:<< execute a command to open path in external editor >>
                try:
                    if arg == None: arg = ""
                    shortPath = path # g.shortFileName(path)
                    if openType == "os.system":
                        if 1:
                            # This works, _provided_ that arg does not contain blanks.  Sheesh.
                            command = 'os.system(%s)' % (arg+shortPath)
                            os.system(arg+shortPath)
                        else:
                            # XP does not like this format!
                            command = 'os.system("%s" "%s")' % (arg,shortPath)
                            os.system('"%s" "%s"' % (arg,shortPath))
                    elif openType == "os.startfile":
                        command = "os.startfile(%s)" % (arg+shortPath)
                        os.startfile(arg+path)
                    elif openType == "exec":
                        command = "exec(%s)" % (arg+shortPath)
                        exec arg+path in {}
                    elif openType == "os.spawnl":
                        filename = g.os_path_basename(arg)
                        command = "os.spawnl(%s,%s,%s)" % (arg,filename,path)
                        apply(os.spawnl,(os.P_NOWAIT,arg,filename,path))
                    elif openType == "os.spawnv":
                        filename = os.path.basename(arg[0]) 
                        vtuple = arg[1:] 
                        vtuple.append(path)
                        command = "os.spawnv(%s,%s)" % (arg[0],repr(vtuple))
                        apply(os.spawnv,(os.P_NOWAIT,arg[0],vtuple))
                    else:
                        command="bad command:"+str(openType)
                        g.trace(command)
                except Exception:
                    g.es("exception executing: "+command)
                    g.es_exception()
                #@nonl
                #@-node:ekr.20050825165823.10:<< execute a command to open path in external editor >>
                #@nl
            g.doHook("openwith2",c=c,p=p,v=p.v,openType=openType,arg=arg,ext=ext)
        except Exception:
            g.es("unexpected exception in c.openWith")
            g.es_exception()
    
        return "break"
    #@+node:ekr.20050825165823.11:createOpenWithTempFile
    def createOpenWithTempFile (self,p,ext):
        
        c = self
        path = c.openWithTempFilePath(p,ext)
        try:
            if g.os_path_exists(path):
                g.es("recreating:  " + g.shortFileName(path),color="red")
            else:
                g.es("creating:  " + g.shortFileName(path),color="blue")
            theFile = open(path,"w")
            # Convert s to whatever encoding is in effect.
            s = p.bodyString()
            theDict = g.scanDirectives(c,p=p)
            encoding = theDict.get("encoding",None)
            if encoding == None:
                encoding = c.config.default_derived_file_encoding
            s = g.toEncodedString(s,encoding,reportErrors=True) 
            theFile.write(s)
            theFile.flush()
            theFile.close()
            try:    time = g.os_path_getmtime(path)
            except: time = None
            # g.es("time: " + str(time))
            # New in 4.3: theDict now contains both 'p' and 'v' entries, of the expected type.
            theDict = {
                "body":s, "c":c, "encoding":encoding,
                "f":theFile, "path":path, "time":time,
                "p":p, "v":p.v }
            #@        << remove previous entry from app.openWithFiles if it exists >>
            #@+node:ekr.20050825165823.12:<< remove previous entry from app.openWithFiles if it exists >>
            for d in g.app.openWithFiles[:]:
                p2 = d.get("p")
                if p.v.t == p2.v.t:
                    # print "removing previous entry in g.app.openWithFiles for",p.headString()
                    g.app.openWithFiles.remove(d)
            #@nonl
            #@-node:ekr.20050825165823.12:<< remove previous entry from app.openWithFiles if it exists >>
            #@nl
            g.app.openWithFiles.append(theDict)
            return path
        except:
            if theFile:
                theFile.close()
            theFile = None
            g.es("exception creating temp file",color="red")
            g.es_exception()
            return None
    #@nonl
    #@-node:ekr.20050825165823.11:createOpenWithTempFile
    #@+node:ekr.20050825165823.13:c.openWithTempFilePath
    def openWithTempFilePath (self,p,ext):
        
        """Return the path to the temp file corresponding to p and ext."""
        
        if 0: # new code: similar to code in mod_tempfname.py plugin.
            try:
                # At least in Windows, user name may contain special characters
                # which would require escaping quotes.
                leoTempDir = g.sanitize_filename(getpass.getuser()) + "_" + "Leo"
            except:
                leoTempDir = "LeoTemp"
                g.es("Could not retrieve your user name.")
                g.es("Temporary files will be stored in: %s" % leoTempDir)
            
            td = os.path.join(g.os_path_abspath(tempfile.gettempdir()),leoTempDir)
            if not os.path.exists(td):
                os.mkdir(td)
            
            name = g.sanitize_filename(v.headString()) + '_' + str(id(v.t))  + ext
            path = os.path.join(td,name)
            return path
        else: # Original code.
            name = "LeoTemp_%s_%s%s" % (
                str(id(p.v.t)),
                g.sanitize_filename(p.headString()),
                ext)
        
            name = g.toUnicode(name,g.app.tkEncoding)
        
            if 1:
                td = g.os_path_abspath(tempfile.gettempdir())
            else:
                td = g.os_path_abspath(g.os_path_join(g.app.loadDir,'..','temp'))
        
            path = g.os_path_join(td,name)
        
            return path
    #@nonl
    #@-node:ekr.20050825165823.13:c.openWithTempFilePath
    #@-node:ekr.20050825165823.4:openWith and allies
    #@+node:ekr.20050825165823.1:new
    def new (self):
    
        c,frame = g.app.gui.newLeoCommanderAndFrame(fileName=None)
        
        # Needed for plugins.
        g.doHook("new",old_c=self,c=c,new_c=c)
    
        # Use the config params to set the size and location of the window.
        frame.setInitialWindowGeometry()
        frame.deiconify()
        frame.lift()
        frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio) # Resize the _new_ frame.
        
        c.beginUpdate()
        if 1: # within update
            t = leoNodes.tnode()
            v = leoNodes.vnode(c,t)
            p = leoNodes.position(v,[])
            v.initHeadString("NewHeadline")
            v.moveToRoot()
            c.editPosition(p)
        c.endUpdate()
    
        frame.body.setFocus()
        return c # For unit test.
    #@nonl
    #@-node:ekr.20050825165823.1:new
    #@+node:ekr.20050825165823.14:close
    def close(self):
        
        """Handle the File-Close command."""
    
        g.app.closeLeoWindow(self.frame)
    #@nonl
    #@-node:ekr.20050825165823.14:close
    #@+node:ekr.20050825165823.15:save
    def save(self):
    
        c = self
        
        if g.app.disableSave:
            g.es("Save commands disabled",color="purple")
            return
        
        # Make sure we never pass None to the ctor.
        if not c.mFileName:
            c.frame.title = ""
            c.mFileName = ""
    
        if c.mFileName != "":
            # Calls c.setChanged(False) if no error.
            c.fileCommands.save(c.mFileName) 
            return
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile = c.mFileName,
            title="Save",
            filetypes=[("Leo files", "*.leo")],
            defaultextension=".leo")
    
        if fileName:
            # 7/2/02: don't change mFileName until the dialog has suceeded.
            c.mFileName = g.ensure_extension(fileName, ".leo")
            c.frame.title = c.mFileName
            c.frame.setTitle(g.computeWindowTitle(c.mFileName))
            c.fileCommands.save(c.mFileName)
            c.updateRecentFiles(c.mFileName)
    #@nonl
    #@-node:ekr.20050825165823.15:save
    #@+node:ekr.20050825165823.16:saveAs
    def saveAs(self):
        
        c = self
        
        if g.app.disableSave:
            g.es("Save commands disabled",color="purple")
            return
    
        # Make sure we never pass None to the ctor.
        if not c.mFileName:
            c.frame.title = ""
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile = c.mFileName,
            title="Save As",
            filetypes=[("Leo files", "*.leo")],
            defaultextension=".leo")
    
        if fileName:
            # 7/2/02: don't change mFileName until the dialog has suceeded.
            c.mFileName = g.ensure_extension(fileName, ".leo")
            c.frame.title = c.mFileName
            c.frame.setTitle(g.computeWindowTitle(c.mFileName))
            # Calls c.setChanged(False) if no error.
            c.fileCommands.saveAs(c.mFileName)
            c.updateRecentFiles(c.mFileName)
    #@nonl
    #@-node:ekr.20050825165823.16:saveAs
    #@+node:ekr.20050825165823.17:saveTo
    def saveTo(self):
        
        c = self
        
        if g.app.disableSave:
            g.es("Save commands disabled",color="purple")
            return
    
        # Make sure we never pass None to the ctor.
        if not c.mFileName:
            c.frame.title = ""
    
        # set local fileName, _not_ c.mFileName
        fileName = g.app.gui.runSaveFileDialog(
            initialfile = c.mFileName,
            title="Save To",
            filetypes=[("Leo files", "*.leo")],
            defaultextension=".leo")
    
        if fileName:
            fileName = g.ensure_extension(fileName, ".leo")
            c.fileCommands.saveTo(fileName)
            c.updateRecentFiles(fileName)
    #@nonl
    #@-node:ekr.20050825165823.17:saveTo
    #@+node:ekr.20050825165823.18:revert
    def revert(self):
        
        c = self
    
        # Make sure the user wants to Revert.
        if not c.mFileName:
            return
            
        reply = g.app.gui.runAskYesNoDialog(c,"Revert",
            "Revert to previous version of " + c.mFileName + "?")
    
        if reply=="no":
            return
    
        # Kludge: rename this frame so openWithFileName won't think it is open.
        fileName = c.mFileName ; c.mFileName = ""
    
        # Create a new frame before deleting this frame.
        ok, frame = g.openWithFileName(fileName,c)
        if ok:
            frame.deiconify()
            g.app.destroyWindow(c.frame)
        else:
            c.mFileName = fileName
    #@-node:ekr.20050825165823.18:revert
    #@-node:ekr.20050825165823:top level file commands
    #@+node:ekr.20050825171046.9:fileCommands methods
    #@+node:ekr.20050825171046.10:save
    def save(self,fileName):
    
        c = self.c ; v = c.currentVnode()
    
        # New in 4.2.  Return ok flag so shutdown logic knows if all went well.
        ok = g.doHook("save1",c=c,p=v,v=v,fileName=fileName)
        if ok is None:
            c.beginUpdate()
            c.endEditing()# Set the current headline text.
            self.setDefaultDirectoryForNewFiles(fileName)
            ok = self.write_Leo_file(fileName,False) # outlineOnlyFlag
            if ok:
                c.setChanged(False) # Clears all dirty bits.
                g.es("saved: " + g.shortFileName(fileName))
                if c.config.save_clears_undo_buffer:
                    g.es("clearing undo")
                    c.undoer.clearUndoState()
            c.endUpdate()
        g.doHook("save2",c=c,p=v,v=v,fileName=fileName)
        return ok
    #@nonl
    #@-node:ekr.20050825171046.10:save
    #@+node:ekr.20050825171046.11:saveAs
    def saveAs(self,fileName):
    
        c = self.c ; v = c.currentVnode()
    
        if not g.doHook("save1",c=c,p=v,v=v,fileName=fileName):
            c.beginUpdate()
            c.endEditing() # Set the current headline text.
            self.setDefaultDirectoryForNewFiles(fileName)
            if self.write_Leo_file(fileName,False): # outlineOnlyFlag
                c.setChanged(False) # Clears all dirty bits.
                g.es("saved: " + g.shortFileName(fileName))
            c.endUpdate()
        g.doHook("save2",c=c,p=v,v=v,fileName=fileName)
    #@-node:ekr.20050825171046.11:saveAs
    #@+node:ekr.20050825171046.12:saveTo
    def saveTo (self,fileName):
    
        c = self.c ; v = c.currentVnode()
    
        if not g.doHook("save1",c=c,p=v,v=v,fileName=fileName):
            c.beginUpdate()
            c.endEditing()# Set the current headline text.
            self.setDefaultDirectoryForNewFiles(fileName)
            if self.write_Leo_file(fileName,False): # outlineOnlyFlag
                g.es("saved: " + g.shortFileName(fileName))
            c.endUpdate()
        g.doHook("save2",c=c,p=v,v=v,fileName=fileName)
    #@nonl
    #@-node:ekr.20050825171046.12:saveTo
    #@-node:ekr.20050825171046.9:fileCommands methods
    #@-others
#@nonl
#@-node:ekr.20050825171046.8:No change required
#@+node:ekr.20050825171046.13:Originals
if 0:
    
    #@    @+others
    #@+node:ekr.20050825171046.14:fileCommands.write_Leo_file
    def write_Leo_file(self,fileName,outlineOnlyFlag):
    
        c = self.c
        self.assignFileIndices()
        if not outlineOnlyFlag:
            # Update .leoRecentFiles.txt if possible.
            g.app.config.writeRecentFilesFile(c)
            #@        << write all @file nodes >>
            #@+node:ekr.20050825171046.15:<< write all @file nodes >>
            try:
                # Write all @file nodes and set orphan bits.
                c.atFileCommands.writeAll()
            except Exception:
                g.es_error("exception writing derived files")
                g.es_exception()
                return False
            #@nonl
            #@-node:ekr.20050825171046.15:<< write all @file nodes >>
            #@nl
        #@    << return if the .leo file is read-only >>
        #@+node:ekr.20050825171046.16:<< return if the .leo file is read-only >>
        # self.read_only is not valid for Save As and Save To commands.
        
        if g.os_path_exists(fileName):
            try:
                if not os.access(fileName,os.W_OK):
                    g.es("can not create: read only: " + fileName,color="red")
                    return False
            except:
                pass # os.access() may not exist on all platforms.
        #@nonl
        #@-node:ekr.20050825171046.16:<< return if the .leo file is read-only >>
        #@nl
        try:
            theActualFile = None
            #@        << create backup file >>
            #@+node:ekr.20050825171046.17:<< create backup file >>
            # rename fileName to fileName.bak if fileName exists.
            if g.os_path_exists(fileName):
                backupName = g.os_path_join(g.app.loadDir,fileName)
                backupName = fileName + ".bak"
                if g.os_path_exists(backupName):
                    g.utils_remove(backupName)
                ok = g.utils_rename(fileName,backupName)
                if not ok:
                    if self.read_only:
                        g.es("read only",color="red")
                    return False
            else:
                backupName = None
            #@nonl
            #@-node:ekr.20050825171046.17:<< create backup file >>
            #@nl
            self.mFileName = fileName
            self.outputFile = cStringIO.StringIO() # or g.fileLikeObject()
            theActualFile = open(fileName, 'wb')
            #@        << put the .leo file >>
            #@+node:ekr.20050825171046.18:<< put the .leo file >>
            self.putProlog()
            self.putHeader()
            self.putGlobals()
            self.putPrefs()
            self.putFindSettings()
            #start = g.getTime()
            self.putVnodes()
            #start = g.printDiffTime("vnodes ",start)
            self.putTnodes()
            #start = g.printDiffTime("tnodes ",start)
            self.putPostlog()
            #@nonl
            #@-node:ekr.20050825171046.18:<< put the .leo file >>
            #@nl
            theActualFile.write(self.outputFile.getvalue())
            theActualFile.close()
            self.outputFile = None
            #@        << delete backup file >>
            #@+node:ekr.20050825171046.19:<< delete backup file >>
            if backupName and g.os_path_exists(backupName):
            
                self.deleteFileWithMessage(backupName,'backup')
            #@nonl
            #@-node:ekr.20050825171046.19:<< delete backup file >>
            #@nl
            return True
        except Exception:
            g.es("exception writing: " + fileName)
            g.es_exception(full=False)
            if theActualFile: theActualFile.close()
            self.outputFile = None
            #@        << delete fileName >>
            #@+node:ekr.20050825171046.20:<< delete fileName >>
            if fileName and g.os_path_exists(fileName):
                self.deleteFileWithMessage(fileName,'')
            #@-node:ekr.20050825171046.20:<< delete fileName >>
            #@nl
            #@        << rename backupName to fileName >>
            #@+node:ekr.20050825171046.21:<< rename backupName to fileName >>
            if backupName:
                g.es("restoring " + fileName + " from " + backupName)
                g.utils_rename(backupName,fileName)
            #@nonl
            #@-node:ekr.20050825171046.21:<< rename backupName to fileName >>
            #@nl
            return False
    
    write_LEO_file = write_Leo_file # For compatibility with old plugins.
    #@nonl
    #@-node:ekr.20050825171046.14:fileCommands.write_Leo_file
    #@+node:ekr.20050825171046.22:g.openWithFileName
    def openWithFileName(fileName,old_c,enableLog=True,readAtFileNodesFlag=True):
        
        """Create a Leo Frame for the indicated fileName if the file exists."""
    
        if not fileName or len(fileName) == 0:
            return False, None
            
        def munge(name):
            name = name or ''
            return g.os_path_normpath(name).lower()
    
        # Create a full, normalized, Unicode path name, preserving case.
        fileName = g.os_path_normpath(g.os_path_abspath(fileName))
    
        # If the file is already open just bring its window to the front.
        theList = app.windowList
        for frame in theList:
            if munge(fileName) == munge(frame.c.mFileName):
                frame.bringToFront()
                app.setLog(frame.log,"openWithFileName")
                # g.trace('Already open',fileName)
                return True, frame
        try:
            # g.trace('Not open',fileName)
            # Open the file in binary mode to allow 0x1a in bodies & headlines.
            theFile = open(fileName,'rb')
            c,frame = app.gui.newLeoCommanderAndFrame(fileName)
            frame.log.enable(enableLog)
            g.app.writeWaitingLog() # New in 4.3: write queued log first.
            if not g.doHook("open1",old_c=old_c,c=c,new_c=c,fileName=fileName):
                app.setLog(frame.log,"openWithFileName")
                app.lockLog()
                frame.c.fileCommands.open(
                    theFile,fileName,
                    readAtFileNodesFlag=readAtFileNodesFlag) # closes file.
                app.unlockLog()
                for frame in g.app.windowList:
                    # The recent files list has been updated by menu.updateRecentFiles.
                    frame.c.config.setRecentFiles(g.app.config.recentFiles)
            frame.openDirectory = g.os_path_dirname(fileName)
            g.doHook("open2",old_c=old_c,c=c,new_c=frame.c,fileName=fileName)
            return True, frame
        except IOError:
            # Do not use string + here: it will fail for non-ascii strings!
            if not g.app.unitTesting:
                g.es("can not open: %s" % (fileName), color="blue")
            return False, None
        except Exception:
            g.es("exceptions opening: %s" % (fileName),color="red")
            g.es_exception()
            return False, None
    #@nonl
    #@-node:ekr.20050825171046.22:g.openWithFileName
    #@-others
#@nonl
#@-node:ekr.20050825171046.13:Originals
#@-node:ekr.20050825165338:Overrides of core methods
#@+node:ekr.20050826073640:buildTnodeClass
def buildTnodeClass ():
    
    class tnode (ZODB.Persistence.Persistent):
        '''A class that implements tnodes.'''
        #@        << tnode constants >>
        #@+middle:ekr.20050826073640.1:class tnode
        #@+node:ekr.20050826073640.2:<< tnode constants >>
        dirtyBit    =		0x01
        richTextBit =	0x02 # Determines whether we use <bt> or <btr> tags.
        visitedBit  =	0x04
        writeBit    = 0x08 # Set: write the tnode.
        #@nonl
        #@-node:ekr.20050826073640.2:<< tnode constants >>
        #@-middle:ekr.20050826073640.1:class tnode
        #@nl
        #@        @+others
        #@+node:ekr.20050826073640.1:class tnode
        #@+node:ekr.20050826073640.3:t.__init__
        # All params have defaults, so t = tnode() is valid.
        
        def __init__ (self,bodyString=None,headString=None):
        
            self.cloneIndex = 0 # For Pre-3.12 files.  Zero for @file nodes
            self.fileIndex = None # The immutable file index for this tnode.
            self.insertSpot = None # Location of previous insert point.
            self.scrollBarSpot = None # Previous value of scrollbar position.
            self.selectionLength = 0 # The length of the selected body text.
            self.selectionStart = 0 # The start of the selected body text.
            self.statusBits = 0 # status bits
        
            # Convert everything to unicode...
            self.headString = g.toUnicode(headString,g.app.tkEncoding)
            self.bodyString = g.toUnicode(bodyString,g.app.tkEncoding)
            
            self.vnodeList = [] # List of all vnodes pointing to this tnode.
            self._firstChild = None
        #@nonl
        #@-node:ekr.20050826073640.3:t.__init__
        #@+node:ekr.20050826073640.4:t.__repr__ & t.__str__
        def __repr__ (self):
            
            return "<tnode %d>" % (id(self))
                
        __str__ = __repr__
        #@nonl
        #@-node:ekr.20050826073640.4:t.__repr__ & t.__str__
        #@+node:ekr.20050826081159:t.__hash__ (WARNING: added because no tnode no longer inherits from object)
        def __hash__ (self):
            
            return id(self)
        #@nonl
        #@-node:ekr.20050826081159:t.__hash__ (WARNING: added because no tnode no longer inherits from object)
        #@+node:ekr.20050826073640.5:Getters
        #@+node:ekr.20050826073640.6:getBody
        def getBody (self):
        
            return self.bodyString
        #@nonl
        #@-node:ekr.20050826073640.6:getBody
        #@+node:ekr.20050826073640.7:hasBody
        def hasBody (self):
        
            return self.bodyString and len(self.bodyString) > 0
        #@nonl
        #@-node:ekr.20050826073640.7:hasBody
        #@+node:ekr.20050826073640.8:Status bits
        #@+node:ekr.20050826073640.9:isDirty
        def isDirty (self):
        
            return (self.statusBits & self.dirtyBit) != 0
        #@nonl
        #@-node:ekr.20050826073640.9:isDirty
        #@+node:ekr.20050826073640.10:isRichTextBit
        def isRichTextBit (self):
        
            return (self.statusBits & self.richTextBit) != 0
        #@nonl
        #@-node:ekr.20050826073640.10:isRichTextBit
        #@+node:ekr.20050826073640.11:isVisited
        def isVisited (self):
        
            return (self.statusBits & self.visitedBit) != 0
        #@nonl
        #@-node:ekr.20050826073640.11:isVisited
        #@+node:ekr.20050826073640.12:isWriteBit
        def isWriteBit (self):
        
            return (self.statusBits & self.writeBit) != 0
        #@nonl
        #@-node:ekr.20050826073640.12:isWriteBit
        #@-node:ekr.20050826073640.8:Status bits
        #@-node:ekr.20050826073640.5:Getters
        #@+node:ekr.20050826073640.13:Setters
        #@+node:ekr.20050826073640.14:Setting body text
        #@+node:ekr.20050826073640.15:setTnodeText
        # This sets the text in the tnode from the given string.
        
        def setTnodeText (self,s,encoding="utf-8"):
            
            """Set the body text of a tnode to the given string."""
            
            s = g.toUnicode(s,encoding,reportErrors=True)
            
            if 0: # DANGEROUS:  This automatically converts everything when reading files.
            
                ## Self c does not exist yet.
                option = c.config.trailing_body_newlines
                
                if option == "one":
                    s = s.rstrip() + '\n'
                elif option == "zero":
                    s = s.rstrip()
            
            self.bodyString = s
        #@nonl
        #@-node:ekr.20050826073640.15:setTnodeText
        #@+node:ekr.20050826073640.16:setSelection
        def setSelection (self,start,length):
        
            self.selectionStart = start
            self.selectionLength = length
        #@nonl
        #@-node:ekr.20050826073640.16:setSelection
        #@-node:ekr.20050826073640.14:Setting body text
        #@+node:ekr.20050826073640.17:Status bits
        #@+node:ekr.20050826073640.18:clearDirty
        def clearDirty (self):
        
            self.statusBits &= ~ self.dirtyBit
        #@nonl
        #@-node:ekr.20050826073640.18:clearDirty
        #@+node:ekr.20050826073640.19:clearRichTextBit
        def clearRichTextBit (self):
        
            self.statusBits &= ~ self.richTextBit
        #@nonl
        #@-node:ekr.20050826073640.19:clearRichTextBit
        #@+node:ekr.20050826073640.20:clearVisited
        def clearVisited (self):
        
            self.statusBits &= ~ self.visitedBit
        #@nonl
        #@-node:ekr.20050826073640.20:clearVisited
        #@+node:ekr.20050826073640.21:clearWriteBit
        def clearWriteBit (self):
        
            self.statusBits &= ~ self.writeBit
        #@nonl
        #@-node:ekr.20050826073640.21:clearWriteBit
        #@+node:ekr.20050826073640.22:setDirty
        def setDirty (self):
        
            self.statusBits |= self.dirtyBit
        #@nonl
        #@-node:ekr.20050826073640.22:setDirty
        #@+node:ekr.20050826073640.23:setRichTextBit
        def setRichTextBit (self):
        
            self.statusBits |= self.richTextBit
        #@nonl
        #@-node:ekr.20050826073640.23:setRichTextBit
        #@+node:ekr.20050826073640.24:setVisited
        def setVisited (self):
        
            self.statusBits |= self.visitedBit
        #@nonl
        #@-node:ekr.20050826073640.24:setVisited
        #@+node:ekr.20050826073640.25:setWriteBit
        def setWriteBit (self):
        
            self.statusBits |= self.writeBit
        #@nonl
        #@-node:ekr.20050826073640.25:setWriteBit
        #@-node:ekr.20050826073640.17:Status bits
        #@+node:ekr.20050826073640.26:setCloneIndex (used in 3.x)
        def setCloneIndex (self, index):
        
            self.cloneIndex = index
        #@nonl
        #@-node:ekr.20050826073640.26:setCloneIndex (used in 3.x)
        #@+node:ekr.20050826073640.27:setFileIndex
        def setFileIndex (self, index):
        
            self.fileIndex = index
        #@nonl
        #@-node:ekr.20050826073640.27:setFileIndex
        #@+node:ekr.20050826073640.28:setHeadString (new in 4.3)
        def setHeadString (self,s,encoding="utf-8"):
            
            t = self
        
            s = g.toUnicode(s,encoding,reportErrors=True)
            t.headString = s
        #@nonl
        #@-node:ekr.20050826073640.28:setHeadString (new in 4.3)
        #@-node:ekr.20050826073640.13:Setters
        #@-node:ekr.20050826073640.1:class tnode
        #@-others

    return tnode
#@nonl
#@-node:ekr.20050826073640:buildTnodeClass
#@-others
#@nonl
#@-node:ekr.20050825154553:@thin zodb.py
#@-leo
