#@+leo-ver=4-thin
#@+node:ekr.20050825154553:@thin zodb.py
#@<< docstring >>
#@+node:ekr.20050825154605:<< docstring >>
'''An experimental plugin that stores all Leo outline data in a single zodb
database. This plugin replaces the Open, Save and Revert commands with methods
that access the zodb database.
'''
#@nonl
#@-node:ekr.20050825154605:<< docstring >>
#@nl

# WARNING:
# WARNING: highly experimental code:  USE AT YOUR OWN RISK.
# WARNING:
    
from __future__ import generators # To make this plugin work with Python 2.2.

__version__ = '0.0.4'

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
# 
# 0.0.2: Replaced g.app.gui.newLeoCommanderAndFrame with 
# g.app.newLeoCommanderAndFrame.
# 
# - Update to reflect new c argument to position.__init__.
# 
# 0.0.4 EKR:
#     - Added from __future__ import generators to suppress warning in Python 
# 2.2.
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

tnode = None ; vnode = None ; position = None

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
def patchLeoCore (theController):
        
    g.es_print('zodb plugin: patching base classes in leoNodes.py',color='red')
    
    # Set these globals so we don't need to refer to leoNodes.tnode, etc.
    global app,controller, tnode, vnode, position

    app         = g.app
    controller  = theController

    leoNodes.tnode      = tnode     = buildTnodeClass(theController)
    leoNodes.vnode      = vnode     = buildVnodeClass(theController)
    leoNodes.position   = position  = buildPositionClass(theController)
    
    #@    << define openWithFileName_callback >>
    #@+node:ekr.20050826142105:<< define openWithFileName_callback >>
    def openWithFileName_callback (
        fileName,old_c,
        enableLog=True,
        readAtFileNodesFlag=True,
        forceDiskRead=True,
        zodbController=theController
    ):
        return  zodb_openWithFileName(
            fileName,old_c,
            enableLog=enableLog,
            readAtFileNodesFlag=readAtFileNodesFlag,
            forceDiskRead=forceDiskRead,
            zodbController=zodbController)
    #@-node:ekr.20050826142105:<< define openWithFileName_callback >>
    #@nl
    g.openWithFileName = openWithFileName_callback
    
    if 0:
        #@        << define write_Leo_file_callback >>
        #@+node:ekr.20050826142105.1:<< define write_Leo_file_callback >>
        def write_Leo_file_callback (self,
            fileName,
            outlineOnlyFlag,
            zodbController=theController
        ):
            return zodb_write_Leo_file(self,
                fileName,
                outlineOnlyFlag,
                zodbController=zodbController)
        #@nonl
        #@-node:ekr.20050826142105.1:<< define write_Leo_file_callback >>
        #@nl
        leoFileCommands.write_Leo_file = write_Leo_file_callback
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
                # g.trace('zodbControllerClass',self.storage,self.connection)
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
            c,frame = app.newLeoCommanderAndFrame(fileName)
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
#@+node:ekr.20050825165912:zodb_openWithFileName (from leoGlobals)
def zodb_openWithFileName(fileName,old_c,enableLog=True,readAtFileNodesFlag=True,forceDiskRead=False,zodbController=None):
    
    """Create a Leo Frame for the indicated fileName if the file exists."""
    
    g.trace('forceDiskRead',forceDiskRead,zodbController)

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
            
    if not forceDiskRead:
        z = zodbController
        connection = z.open()
        try:
            root = connection.root()
            files = root.get('files',{})
            f = files.get(fileName)
            if f:
                g.trace('found in zodb',fileName)
            connection.close()
        finally:
            z.close()
    try:
        # g.trace('Not open',fileName)
        # Open the file in binary mode to allow 0x1a in bodies & headlines.
        theFile = open(fileName,'rb')
        c,frame = app.newLeoCommanderAndFrame(fileName)
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
#@-node:ekr.20050825165338:Overrides of core methods
#@+node:ekr.20050826073640:buildTnodeClass
def buildTnodeClass (controller=None):
    
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
        #@+node:ekr.20050826081159:t.__hash__ & __cmp__ (for zodb)
        def __hash__ (self):
            
            return id(self)
            
        def __cmp__(self,other):
            
            # Must return 0, 1 or -1
            
            if self is other:
                return 0
            elif id(self) > id(other):
                return 1
            else:
                return -1
        #@nonl
        #@-node:ekr.20050826081159:t.__hash__ & __cmp__ (for zodb)
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
#@+node:ekr.20050826134701:buildVnodeClass
def buildVnodeClass (controller=None):
    
    class vnode (ZODB.Persistence.Persistent):
        '''A class that implements vnodes.'''
        #@        << vnode constants >>
        #@+middle:ekr.20050826134701.1:class vnode
        #@+node:ekr.20050826134701.2:<< vnode constants >>
        # Define the meaning of status bits in new vnodes.
        
        # Archived...
        clonedBit	  = 0x01 # True: vnode has clone mark.
        
        # not used	 = 0x02
        expandedBit = 0x04 # True: vnode is expanded.
        markedBit	  = 0x08 # True: vnode is marked
        orphanBit	  = 0x10 # True: vnode saved in .leo file, not derived file.
        selectedBit = 0x20 # True: vnode is current vnode.
        topBit		    = 0x40 # True: vnode was top vnode when saved.
        
        # Not archived...
        dirtyBit    =	0x060
        richTextBit =	0x080 # Determines whether we use <bt> or <btr> tags.
        visitedBit	 = 0x100
        #@-node:ekr.20050826134701.2:<< vnode constants >>
        #@-middle:ekr.20050826134701.1:class vnode
        #@nl
        #@        @+others
        #@+node:ekr.20050826134701.1:class vnode
        #@+node:ekr.20050826134701.3:Birth & death
        #@+node:ekr.20050826134701.4:v.__cmp__ (not used)
        if 0: # not used
            def __cmp__(self,other):
                
                g.trace(self,other)
                return not (self is other) # Must return 0, 1 or -1
        #@nonl
        #@-node:ekr.20050826134701.4:v.__cmp__ (not used)
        #@+node:ekr.20050826134701.5:v.__init__
        def __init__ (self,c,t):
        
            assert(t)
            #@    << initialize vnode data members >>
            #@+node:ekr.20050826134701.6:<< initialize vnode data members >>
            self.c = c # The commander for this vnode.
            self.t = t # The tnode.
            self.statusBits = 0 # status bits
            
            # Structure links.
            self._parent = self._next = self._back = None
            #@nonl
            #@-node:ekr.20050826134701.6:<< initialize vnode data members >>
            #@nl
        #@nonl
        #@-node:ekr.20050826134701.5:v.__init__
        #@+node:ekr.20050826134701.7:v.__repr__ & v.__str__
        def __repr__ (self):
            
            if self.t:
                return "<vnode %d:'%s'>" % (id(self),self.cleanHeadString())
            else:
                return "<vnode %d:NULL tnode>" % (id(self))
                
        __str__ = __repr__
        #@nonl
        #@-node:ekr.20050826134701.7:v.__repr__ & v.__str__
        #@+node:ekr.20050826135159:t.__hash__ & __cmp__ (for zodb)
        def __hash__ (self):
            
            return id(self)
            
        def __cmp__(self,other):
            
            # Must return 0, 1 or -1
            
            if self is other:
                return 0
            elif id(self) > id(other):
                return 1
            else:
                return -1
        #@nonl
        #@-node:ekr.20050826135159:t.__hash__ & __cmp__ (for zodb)
        #@+node:ekr.20050826134701.8:v.dump
        def dumpLink (self,link):
            return g.choose(link,link,"<none>")
        
        def dump (self,label=""):
            
            v = self
        
            if label:
                print '-'*10,label,v
            else:
                print "self    ",v.dumpLink(v)
                print "len(vnodeList)",len(v.t.vnodeList)
        
            print "_back   ",v.dumpLink(v._back)
            print "_next   ",v.dumpLink(v._next)
            print "_parent ",v.dumpLink(v._parent)
            print "t._child",v.dumpLink(v.t._firstChild)
            
            if 1:
                print "t",v.dumpLink(v.t)
                print "vnodeList"
                for v in v.t.vnodeList:
                    print v
        #@nonl
        #@-node:ekr.20050826134701.8:v.dump
        #@-node:ekr.20050826134701.3:Birth & death
        #@+node:ekr.20050826134701.9:v.Comparisons
        #@+node:ekr.20050826134701.10:findAtFileName (new in 4.2 b3)
        def findAtFileName (self,names):
            
            """Return the name following one of the names in nameList.
            Return an empty string."""
        
            h = self.headString()
            
            if not g.match(h,0,'@'):
                return ""
            
            i = g.skip_id(h,1,'-')
            word = h[:i]
            if word in names and g.match_word(h,0,word):
                name = h[i:].strip()
                # g.trace(word,name)
                return name
            else:
                return ""
        #@nonl
        #@-node:ekr.20050826134701.10:findAtFileName (new in 4.2 b3)
        #@+node:ekr.20050826134701.11:anyAtFileNodeName
        def anyAtFileNodeName (self):
            
            """Return the file name following an @file node or an empty string."""
        
            names = (
                "@file",
                "@thin",   "@file-thin",   "@thinfile",
                "@asis",   "@file-asis",   "@silentfile",
                "@noref",  "@file-noref",  "@rawfile",
                "@nosent", "@file-nosent", "@nosentinelsfile")
        
            return self.findAtFileName(names)
        #@nonl
        #@-node:ekr.20050826134701.11:anyAtFileNodeName
        #@+node:ekr.20050826134701.12:at...FileNodeName
        # These return the filename following @xxx, in v.headString.
        # Return the the empty string if v is not an @xxx node.
        
        def atFileNodeName (self):
            names = ("@file"),
            return self.findAtFileName(names)
        
        def atNoSentinelsFileNodeName (self):
            names = ("@nosent", "@file-nosent", "@nosentinelsfile")
            return self.findAtFileName(names)
        
        def atRawFileNodeName (self):
            names = ("@noref", "@file-noref", "@rawfile")
            return self.findAtFileName(names)
            
        def atSilentFileNodeName (self):
            names = ("@asis", "@file-asis", "@silentfile")
            return self.findAtFileName(names)
            
        def atThinFileNodeName (self):
            names = ("@thin", "@file-thin", "@thinfile")
            return self.findAtFileName(names)
            
        # New names, less confusing
        atNoSentFileNodeName  = atNoSentinelsFileNodeName
        atNorefFileNodeName   = atRawFileNodeName
        atAsisFileNodeName     = atSilentFileNodeName
        #@nonl
        #@-node:ekr.20050826134701.12:at...FileNodeName
        #@+node:ekr.20050826134701.13:isAtAllNode
        def isAtAllNode (self):
        
            """Returns True if the receiver contains @others in its body at the start of a line."""
        
            flag, i = g.is_special(self.t.bodyString,0,"@all")
            return flag
        #@nonl
        #@-node:ekr.20050826134701.13:isAtAllNode
        #@+node:ekr.20050826134701.14:isAnyAtFileNode good
        def isAnyAtFileNode (self):
            
            """Return True if v is any kind of @file or related node."""
            
            # This routine should be as fast as possible.
            # It is called once for every vnode when writing a file.
        
            h = self.headString()
            return h and h[0] == '@' and self.anyAtFileNodeName()
        #@nonl
        #@-node:ekr.20050826134701.14:isAnyAtFileNode good
        #@+node:ekr.20050826134701.15:isAt...FileNode
        def isAtFileNode (self):
            return g.choose(self.atFileNodeName(),True,False)
            
        def isAtNoSentinelsFileNode (self):
            return g.choose(self.atNoSentinelsFileNodeName(),True,False)
        
        def isAtRawFileNode (self): # @file-noref
            return g.choose(self.atRawFileNodeName(),True,False)
        
        def isAtSilentFileNode (self): # @file-asis
            return g.choose(self.atSilentFileNodeName(),True,False)
        
        def isAtThinFileNode (self):
            return g.choose(self.atThinFileNodeName(),True,False)
            
        # New names, less confusing:
        isAtNoSentFileNode = isAtNoSentinelsFileNode
        isAtNorefFileNode  = isAtRawFileNode
        isAtAsisFileNode   = isAtSilentFileNode
        #@nonl
        #@-node:ekr.20050826134701.15:isAt...FileNode
        #@+node:ekr.20050826134701.16:isAtIgnoreNode
        def isAtIgnoreNode (self):
        
            """Returns True if the receiver contains @ignore in its body at the start of a line."""
        
            flag, i = g.is_special(self.t.bodyString, 0, "@ignore")
            return flag
        #@nonl
        #@-node:ekr.20050826134701.16:isAtIgnoreNode
        #@+node:ekr.20050826134701.17:isAtOthersNode
        def isAtOthersNode (self):
        
            """Returns True if the receiver contains @others in its body at the start of a line."""
        
            flag, i = g.is_special(self.t.bodyString,0,"@others")
            return flag
        #@nonl
        #@-node:ekr.20050826134701.17:isAtOthersNode
        #@+node:ekr.20050826134701.18:matchHeadline
        def matchHeadline (self,pattern):
        
            """Returns True if the headline matches the pattern ignoring whitespace and case.
            
            The headline may contain characters following the successfully matched pattern."""
        
            h = string.lower(self.headString())
            h = string.replace(h,' ','')
            h = string.replace(h,'\t','')
        
            s = string.lower(pattern)
            s = string.replace(s,' ','')
            s = string.replace(s,'\t','')
        
            # ignore characters in the headline following the match
            return s == h[0:len(s)]
        #@nonl
        #@-node:ekr.20050826134701.18:matchHeadline
        #@-node:ekr.20050826134701.9:v.Comparisons
        #@+node:ekr.20050826134701.19:Getters (vnode)
        #@+node:ekr.20050826134701.20:Tree Traversal getters
        #@+node:ekr.20050826134701.21:v.back
        # Compatibility routine for scripts
        
        def back (self):
        
            return self._back
        #@nonl
        #@-node:ekr.20050826134701.21:v.back
        #@+node:ekr.20050826134701.22:v.next
        # Compatibility routine for scripts
        # Used by p.findAllPotentiallyDirtyNodes.
        
        def next (self):
        
            return self._next
        #@nonl
        #@-node:ekr.20050826134701.22:v.next
        #@-node:ekr.20050826134701.20:Tree Traversal getters
        #@+node:ekr.20050826134701.23:Children
        #@+node:ekr.20050826134701.24:v.childIndex
        def childIndex(self):
            
            v = self
        
            if not v._back:
                return 0
        
            n = 0 ; v = v._back
            while v:
                n += 1
                v = v._back
            return n
        #@nonl
        #@-node:ekr.20050826134701.24:v.childIndex
        #@+node:ekr.20050826134701.25:v.firstChild (changed for 4.2)
        def firstChild (self):
            
            return self.t._firstChild
        #@nonl
        #@-node:ekr.20050826134701.25:v.firstChild (changed for 4.2)
        #@+node:ekr.20050826134701.26:v.hasChildren & hasFirstChild
        def hasChildren (self):
            
            v = self
            return v.firstChild()
        
        hasFirstChild = hasChildren
        #@nonl
        #@-node:ekr.20050826134701.26:v.hasChildren & hasFirstChild
        #@+node:ekr.20050826134701.27:v.lastChild
        def lastChild (self):
        
            child = self.firstChild()
            while child and child.next():
                child = child.next()
            return child
        #@nonl
        #@-node:ekr.20050826134701.27:v.lastChild
        #@+node:ekr.20050826134701.28:v.nthChild
        # childIndex and nthChild are zero-based.
        
        def nthChild (self, n):
        
            child = self.firstChild()
            if not child: return None
            while n > 0 and child:
                n -= 1
                child = child.next()
            return child
        #@nonl
        #@-node:ekr.20050826134701.28:v.nthChild
        #@+node:ekr.20050826134701.29:v.numberOfChildren (n)
        def numberOfChildren (self):
        
            n = 0
            child = self.firstChild()
            while child:
                n += 1
                child = child.next()
            return n
        #@nonl
        #@-node:ekr.20050826134701.29:v.numberOfChildren (n)
        #@-node:ekr.20050826134701.23:Children
        #@+node:ekr.20050826134701.30:Status Bits
        #@+node:ekr.20050826134701.31:v.isCloned (4.2)
        def isCloned (self):
            
            return len(self.t.vnodeList) > 1
        #@nonl
        #@-node:ekr.20050826134701.31:v.isCloned (4.2)
        #@+node:ekr.20050826134701.32:isDirty
        def isDirty (self):
        
            return self.t.isDirty()
        #@nonl
        #@-node:ekr.20050826134701.32:isDirty
        #@+node:ekr.20050826134701.33:isExpanded
        def isExpanded (self):
        
            return ( self.statusBits & self.expandedBit ) != 0
        #@nonl
        #@-node:ekr.20050826134701.33:isExpanded
        #@+node:ekr.20050826134701.34:isMarked
        def isMarked (self):
        
            return ( self.statusBits & vnode.markedBit ) != 0
        #@nonl
        #@-node:ekr.20050826134701.34:isMarked
        #@+node:ekr.20050826134701.35:isOrphan
        def isOrphan (self):
        
            return ( self.statusBits & vnode.orphanBit ) != 0
        #@nonl
        #@-node:ekr.20050826134701.35:isOrphan
        #@+node:ekr.20050826134701.36:isSelected
        def isSelected (self):
        
            return ( self.statusBits & vnode.selectedBit ) != 0
        #@nonl
        #@-node:ekr.20050826134701.36:isSelected
        #@+node:ekr.20050826134701.37:isTopBitSet
        def isTopBitSet (self):
        
            return ( self.statusBits & self.topBit ) != 0
        #@nonl
        #@-node:ekr.20050826134701.37:isTopBitSet
        #@+node:ekr.20050826134701.38:isVisited
        def isVisited (self):
        
            return ( self.statusBits & vnode.visitedBit ) != 0
        #@nonl
        #@-node:ekr.20050826134701.38:isVisited
        #@+node:ekr.20050826134701.39:status
        def status (self):
        
            return self.statusBits
        #@nonl
        #@-node:ekr.20050826134701.39:status
        #@-node:ekr.20050826134701.30:Status Bits
        #@+node:ekr.20050826134701.40:v.bodyString
        # Compatibility routine for scripts
        
        def bodyString (self):
        
            # This message should never be printed and we want to avoid crashing here!
            if not g.isUnicode(self.t.bodyString):
                s = "Leo internal error: not unicode:" + repr(self.t.bodyString)
                g.es_print(s,color="red")
        
            # Make _sure_ we return a unicode string.
            return g.toUnicode(self.t.bodyString,g.app.tkEncoding)
        #@-node:ekr.20050826134701.40:v.bodyString
        #@+node:ekr.20050826134701.41:v.currentVnode (and c.currentPosition 4.2)
        def currentPosition (self):
            return self.c.currentPosition()
                
        def currentVnode (self):
            return self.c.currentVnode()
        #@nonl
        #@-node:ekr.20050826134701.41:v.currentVnode (and c.currentPosition 4.2)
        #@+node:ekr.20050826134701.42:v.findRoot (4.2)
        def findRoot (self):
            
            return self.c.rootPosition()
        #@nonl
        #@-node:ekr.20050826134701.42:v.findRoot (4.2)
        #@+node:ekr.20050826134701.43:v.headString & v.cleanHeadString
        def headString (self):
            
            """Return the headline string."""
            
            # This message should never be printed and we want to avoid crashing here!
            if not g.isUnicode(self.t.headString):
                s = "Leo internal error: not unicode:" + repr(self.t.headString)
                g.es_print(s,color="red")
                
            # Make _sure_ we return a unicode string.
            return g.toUnicode(self.t.headString,g.app.tkEncoding)
        
        def cleanHeadString (self):
            
            s = self.headString()
            return g.toEncodedString(s,"ascii") # Replaces non-ascii characters by '?'
        #@nonl
        #@-node:ekr.20050826134701.43:v.headString & v.cleanHeadString
        #@+node:ekr.20050826134701.44:v.directParents (new method in 4.2)
        def directParents (self):
            
            """(New in 4.2) Return a list of all direct parent vnodes of a vnode.
            
            This is NOT the same as the list of ancestors of the vnode."""
            
            v = self
            
            if v._parent:
                return v._parent.t.vnodeList
            else:
                return []
        #@nonl
        #@-node:ekr.20050826134701.44:v.directParents (new method in 4.2)
        #@-node:ekr.20050826134701.19:Getters (vnode)
        #@+node:ekr.20050826134701.45:v.Link/Unlink/Insert methods (used by file read logic)
        # These remain in 4.2: the file read logic calls these before creating positions.
        #@nonl
        #@+node:ekr.20050826134701.46:v.insertAfter
        def insertAfter (self,t=None):
        
            """Inserts a new vnode after self"""
        
            if not t:
                t = tnode(headString="NewHeadline")
        
            v = vnode(self.c,t)
            v.linkAfter(self)
        
            return v
        #@nonl
        #@-node:ekr.20050826134701.46:v.insertAfter
        #@+node:ekr.20050826134701.47:v.insertAsNthChild
        def insertAsNthChild (self,n,t=None):
        
            """Inserts a new node as the the nth child of the receiver.
            The receiver must have at least n-1 children"""
        
            if not t:
                t = tnode(headString="NewHeadline")
        
            v = vnode(self.c,t)
            v.linkAsNthChild(self,n)
        
            return v
        #@nonl
        #@-node:ekr.20050826134701.47:v.insertAsNthChild
        #@+node:ekr.20050826134701.48:v.linkAfter
        def linkAfter (self,v):
        
            """Link self after v."""
            
            self._parent = v._parent
            self._back = v
            self._next = v._next
            v._next = self
            if self._next:
                self._next._back = self
        #@-node:ekr.20050826134701.48:v.linkAfter
        #@+node:ekr.20050826134701.49:v.linkAsNthChild
        def linkAsNthChild (self,pv,n):
        
            """Links self as the n'th child of vnode pv"""
        
            v = self
            # g.trace(v,pv,n)
            v._parent = pv
            if n == 0:
                v._back = None
                v._next = pv.t._firstChild
                if pv.t._firstChild:
                    pv.t._firstChild._back = v
                pv.t._firstChild = v
            else:
                prev = pv.nthChild(n-1) # zero based
                assert(prev)
                v._back = prev
                v._next = prev._next
                prev._next = v
                if v._next:
                    v._next._back = v
        #@nonl
        #@-node:ekr.20050826134701.49:v.linkAsNthChild
        #@+node:ekr.20050826134701.50:v.linkAsRoot
        def linkAsRoot (self,oldRoot):
            
            """Link a vnode as the root node and set the root _position_."""
        
            v = self ; c = v.c
        
            # Clear all links except the child link.
            v._parent = None
            v._back = None
            v._next = oldRoot
            
            # Add v to it's tnode's vnodeList. Bug fix: 5/02/04.
            if v not in v.t.vnodeList:
                v.t.vnodeList.append(v)
                v.t._p_changed = True # zodb support.
        
            # Link in the rest of the tree only when oldRoot != None.
            # Otherwise, we are calling this routine from init code and
            # we want to start with a pristine tree.
            if oldRoot: oldRoot._back = v
        
            newRoot = position(c,v,[])
            c.setRootPosition(newRoot)
        #@nonl
        #@-node:ekr.20050826134701.50:v.linkAsRoot
        #@+node:ekr.20050826134701.51:v.moveToRoot
        def moveToRoot (self,oldRoot=None):
        
            """Moves the receiver to the root position"""
        
            v = self
        
            v.unlink()
            v.linkAsRoot(oldRoot)
            
            return v
        #@nonl
        #@-node:ekr.20050826134701.51:v.moveToRoot
        #@+node:ekr.20050826134701.52:v.unlink
        def unlink (self):
        
            """Unlinks a vnode from the tree."""
        
            v = self ; c = v.c
        
            # g.trace(v._parent," child: ",v.t._firstChild," back: ", v._back, " next: ", v._next)
            
            # Special case the root.
            if v == c.rootPosition().v: # 3/11/04
                assert(v._next)
                newRoot = position(c,v._next,[])
                c.setRootPosition(newRoot)
        
            # Clear the links in other nodes.
            if v._back:
                v._back._next = v._next
            if v._next:
                v._next._back = v._back
        
            if v._parent and v == v._parent.t._firstChild:
                v._parent.t._firstChild = v._next
        
            # Clear the links in this node.
            v._parent = v._next = v._back = None
            # v.parentsList = []
        #@nonl
        #@-node:ekr.20050826134701.52:v.unlink
        #@-node:ekr.20050826134701.45:v.Link/Unlink/Insert methods (used by file read logic)
        #@+node:ekr.20050826134701.53:Setters
        #@+node:ekr.20050826134701.54: v.Status bits
        #@+node:ekr.20050826134701.55:clearClonedBit
        def clearClonedBit (self):
        
            self.statusBits &= ~ self.clonedBit
        #@nonl
        #@-node:ekr.20050826134701.55:clearClonedBit
        #@+node:ekr.20050826134701.56:clearDirty & clearDirtyJoined (redundant code)
        def clearDirty (self):
        
            v = self
            v.t.clearDirty()
        
        def clearDirtyJoined (self):
        
            g.trace()
            v = self ; c = v.c
            c.beginUpdate()
            v.t.clearDirty()
            c.endUpdate() # recomputes all icons
        #@nonl
        #@-node:ekr.20050826134701.56:clearDirty & clearDirtyJoined (redundant code)
        #@+node:ekr.20050826134701.57:v.clearMarked
        def clearMarked (self):
        
            self.statusBits &= ~ self.markedBit
        #@-node:ekr.20050826134701.57:v.clearMarked
        #@+node:ekr.20050826134701.58:clearOrphan
        def clearOrphan (self):
        
            self.statusBits &= ~ self.orphanBit
        #@nonl
        #@-node:ekr.20050826134701.58:clearOrphan
        #@+node:ekr.20050826134701.59:clearVisited
        def clearVisited (self):
        
            self.statusBits &= ~ self.visitedBit
        #@nonl
        #@-node:ekr.20050826134701.59:clearVisited
        #@+node:ekr.20050826134701.60:contract & expand & initExpandedBit
        def contract(self):
        
            self.statusBits &= ~ self.expandedBit
            
            # g.trace(self.statusBits)
        
        def expand(self):
        
            self.statusBits |= self.expandedBit
            
            # g.trace(self.statusBits)
        
        def initExpandedBit (self):
        
            self.statusBits |= self.expandedBit
        #@nonl
        #@-node:ekr.20050826134701.60:contract & expand & initExpandedBit
        #@+node:ekr.20050826134701.61:initStatus
        def initStatus (self, status):
        
            self.statusBits = status
        #@nonl
        #@-node:ekr.20050826134701.61:initStatus
        #@+node:ekr.20050826134701.62:setClonedBit & initClonedBit
        def setClonedBit (self):
        
            self.statusBits |= self.clonedBit
        
        def initClonedBit (self, val):
        
            if val:
                self.statusBits |= self.clonedBit
            else:
                self.statusBits &= ~ self.clonedBit
        #@nonl
        #@-node:ekr.20050826134701.62:setClonedBit & initClonedBit
        #@+node:ekr.20050826134701.63:v.setMarked & initMarkedBit
        def setMarked (self):
        
            self.statusBits |= self.markedBit
        
        def initMarkedBit (self):
        
            self.statusBits |= self.markedBit
        #@-node:ekr.20050826134701.63:v.setMarked & initMarkedBit
        #@+node:ekr.20050826134701.64:setOrphan
        def setOrphan (self):
        
            self.statusBits |= self.orphanBit
        #@nonl
        #@-node:ekr.20050826134701.64:setOrphan
        #@+node:ekr.20050826134701.65:setSelected (vnode)
        # This only sets the selected bit.
        
        def setSelected (self):
        
            self.statusBits |= self.selectedBit
        #@nonl
        #@-node:ekr.20050826134701.65:setSelected (vnode)
        #@+node:ekr.20050826134701.66:t.setVisited
        # Compatibility routine for scripts
        
        def setVisited (self):
        
            self.statusBits |= self.visitedBit
        #@nonl
        #@-node:ekr.20050826134701.66:t.setVisited
        #@-node:ekr.20050826134701.54: v.Status bits
        #@+node:ekr.20050826134701.67:v.computeIcon & setIcon
        def computeIcon (self):
        
            val = 0 ; v = self
            if v.t.hasBody(): val += 1
            if v.isMarked(): val += 2
            if v.isCloned(): val += 4
            if v.isDirty(): val += 8
            return val
            
        def setIcon (self):
        
            pass # Compatibility routine for old scripts
        #@nonl
        #@-node:ekr.20050826134701.67:v.computeIcon & setIcon
        #@+node:ekr.20050826134701.68:v.initHeadString
        def initHeadString (self,s,encoding="utf-8"):
            
            v = self
        
            s = g.toUnicode(s,encoding,reportErrors=True)
            v.t.headString = s
        #@nonl
        #@-node:ekr.20050826134701.68:v.initHeadString
        #@+node:ekr.20050826134701.69:v.setSelection
        def setSelection (self, start, length):
        
            self.t.setSelection ( start, length )
        #@nonl
        #@-node:ekr.20050826134701.69:v.setSelection
        #@+node:ekr.20050826134701.70:v.setTnodeText
        def setTnodeText (self,s,encoding="utf-8"):
            
            return self.t.setTnodeText(s,encoding)
        #@nonl
        #@-node:ekr.20050826134701.70:v.setTnodeText
        #@+node:ekr.20050826134701.71:v.trimTrailingLines
        def trimTrailingLines (self):
        
            """Trims trailing blank lines from a node.
            
            It is surprising difficult to do this during Untangle."""
        
            v = self
            body = v.bodyString()
            # g.trace(body)
            lines = string.split(body,'\n')
            i = len(lines) - 1 ; changed = False
            while i >= 0:
                line = lines[i]
                j = g.skip_ws(line,0)
                if j + 1 == len(line):
                    del lines[i]
                    i -= 1 ; changed = True
                else: break
            if changed:
                body = string.join(body,'') + '\n' # Add back one last newline.
                # g.trace(body)
                v.setBodyStringOrPane(body)
                # Don't set the dirty bit: it would just be annoying.
        #@-node:ekr.20050826134701.71:v.trimTrailingLines
        #@-node:ekr.20050826134701.53:Setters
        #@+node:ekr.20050826134701.72:v.Iterators
        #@+node:ekr.20050826134701.73:self_subtree_iter
        def subtree_iter(self):
        
            """Return all nodes of self's tree in outline order."""
            
            v = self
        
            if v:
                yield v
                child = v.t._firstChild
                while child:
                    for v1 in child.subtree_iter():
                        yield v1
                    child = child.next()
                    
        self_and_subtree_iter = subtree_iter
        #@nonl
        #@-node:ekr.20050826134701.73:self_subtree_iter
        #@+node:ekr.20050826134701.74:unique_subtree_iter
        def unique_subtree_iter(self,marks=None):
        
            """Return all vnodes in self's tree, discarding duplicates """
            
            v = self
        
            if marks == None: marks = {}
        
            if v and v not in marks:
                marks[v] = v
                yield v
                if v.t._firstChild:
                    for v1 in v.t._firstChild.unique_subtree_iter(marks):
                        yield v1
                v = v._next
                while v:
                    for v in v.unique_subtree_iter(marks):
                        yield v
                    v = v._next
                    
        self_and_unique_subtree_iter = unique_subtree_iter
        #@nonl
        #@-node:ekr.20050826134701.74:unique_subtree_iter
        #@-node:ekr.20050826134701.72:v.Iterators
        #@-node:ekr.20050826134701.1:class vnode
        #@-others

    return vnode
#@nonl
#@-node:ekr.20050826134701:buildVnodeClass
#@+node:ekr.20050826134701.75:buildPositionClass
def buildPositionClass (controller=None):
    
    class position (ZODB.Persistence.Persistent):
    
        """A class representing a position in a traversal of a tree containing shared tnodes."""
    
        #@        << about the position class >>
        #@+middle:ekr.20050826134701.76:class position
        #@+node:ekr.20050826134701.77:<< about the position class >>
        #@@killcolor
        
        #@+at 
        #@nonl
        # This class provides tree traversal methods that operate on 
        # positions, not vnodes.  Positions encapsulate the notion of present 
        # position within a traversal.
        # 
        # Positions consist of a vnode and a stack of parent nodes used to 
        # determine the next parent when a vnode has mutliple parents.
        # 
        # Calling, e.g., p.moveToThreadNext() results in p being an invalid 
        # position.  That is, p represents the position following the last 
        # node of the outline.  The test "if p" is the _only_ correct way to 
        # test whether a position p is valid.  In particular, tests like "if p 
        # is None" or "if p is not None" will not work properly.
        # 
        # The only changes to vnodes and tnodes needed to implement shared 
        # tnodes are:
        # 
        # - The firstChild field becomes part of tnodes.
        # - t.vnodes contains a list of all vnodes sharing the tnode.
        # 
        # The advantages of using shared tnodes:
        # 
        # - Leo no longer needs to create or destroy "dependent" trees when 
        # changing descendents of cloned trees.
        # - There is no need for join links and no such things as joined 
        # nodes.
        # 
        # These advantages are extremely important: Leo is now scalable to 
        # very large outlines.
        # 
        # An important complication is the need to avoid creating temporary 
        # positions while traversing trees:
        # - Several routines use p.vParentWithStack to avoid having to call 
        # tempPosition.moveToParent().
        #   These include p.level, p.isVisible and p.hasThreadNext.
        # - p.moveToLastNode and p.moveToThreadBack use new algorithms that 
        # don't use temporary data.
        # - Several lookahead routines compute whether a position exists 
        # without computing the actual position.
        #@-at
        #@nonl
        #@-node:ekr.20050826134701.77:<< about the position class >>
        #@-middle:ekr.20050826134701.76:class position
        #@nl
        #@        << positions may become invalid when outlines change >>
        #@+middle:ekr.20050826134701.76:class position
        #@+node:ekr.20050826134701.78:<< positions may become invalid when outlines change >>
        #@@killcolor
        
        #@+at 
        #@nonl
        # If a vnode has only one parent, v._parent is that parent. Otherwise,
        # v.t.vnodeList is the list of vnodes v2 such that v2._firstChild == 
        # v. Alas, this
        # means that positions can become invalid when vnodeList's change!
        # 
        # There is no use trying to solve the problem in p.moveToParent or
        # p.vParentWithStack: the invalidated positions simply don't have the 
        # stack
        # entries needed to compute parent fields properly. In short, changing 
        # t.vnodeList
        # may invalidate existing positions!
        #@-at
        #@nonl
        #@-node:ekr.20050826134701.78:<< positions may become invalid when outlines change >>
        #@-middle:ekr.20050826134701.76:class position
        #@nl
        
        #@        @+others
        #@+node:ekr.20050826134701.76:class position
        #@+node:ekr.20050826134701.79: ctor & other special methods...
        #@+node:ekr.20050826134701.80:p.__cmp__
        def __cmp__(self,p2):
        
            """Return 0 if two postions are equivalent."""
        
            # Use p.equal if speed is crucial.
            p1 = self
        
            if p2 is None: # Allow tests like "p == None"
                if p1.v: return 1 # not equal
                else:    return 0 # equal
        
            # Check entire stack quickly.
            # The stack contains vnodes, so this is not a recursive call.
            if p1.v != p2.v or p1.stack != p2.stack:
                return 1 # notEqual
        
            # This is slow: do this last!
            if p1.childIndex() != p2.childIndex():
                # Disambiguate clones having the same parents.
                return 1 # notEqual
        
            return 0 # equal
        #@nonl
        #@-node:ekr.20050826134701.80:p.__cmp__
        #@+node:ekr.20050826134701.81:p.__getattr__  ON:  must be ON if use_plugins
        if 1: # Good for compatibility, bad for finding conversion problems.
        
            def __getattr__ (self,attr):
                
                """Convert references to p.t into references to p.v.t.
                
                N.B. This automatically keeps p.t in synch with p.v.t."""
        
                if attr=="t":
                    return self.v.t
                else:
                    # New in 4.3: _silently_ raise the attribute error.
                    # This allows plugin code to use hasattr(p,attr) !
                    if 0:
                        print "unknown position attribute:",attr
                        import traceback ; traceback.print_stack()
                    raise AttributeError,attr
        #@nonl
        #@-node:ekr.20050826134701.81:p.__getattr__  ON:  must be ON if use_plugins
        #@+node:ekr.20050826134701.82:p.__init__
        def __init__ (self,c,v,stack,trace=True):
        
            """Create a new position."""
            
            self.c = c
            self.v = v
            assert(v is None or v.t)
            self.stack = stack[:] # Creating a copy here is safest and best.
        
            g.app.positions += 1
            
            if g.app.tracePositions and trace:
                g.trace("%-25s %-25s %s" % (
                    g.callerName(4),g.callerName(3),g.callerName(2)),align=10)
            
            # Note: __getattr__ implements p.t.
        #@-node:ekr.20050826134701.82:p.__init__
        #@+node:ekr.20050826134701.83:p.__nonzero__
        #@+at
        # Tests such as 'if p' or 'if not p' are the _only_ correct ways to 
        # test whether a position p is valid.
        # In particular, tests like 'if p is None' or 'if p is not None' will 
        # not work properly.
        #@-at
        #@@c
        
        def __nonzero__ ( self):
            
            """Return True if a position is valid."""
            
            # if g.app.trace: "__nonzero__",self.v
        
            return self.v is not None
        #@nonl
        #@-node:ekr.20050826134701.83:p.__nonzero__
        #@+node:ekr.20050826134701.84:p.__str__ and p.__repr__
        def __str__ (self):
            
            p = self
            
            if p.v:
                return "<pos %d lvl: %d [%d] %s>" % (id(p),p.level(),len(p.stack),p.cleanHeadString())
            else:
                return "<pos %d        [%d] None>" % (id(p),len(p.stack))
                
        __repr__ = __str__
        #@nonl
        #@-node:ekr.20050826134701.84:p.__str__ and p.__repr__
        #@+node:ekr.20050826134701.85:p.copy
        # Using this routine can generate huge numbers of temporary positions during a tree traversal.
        
        def copy (self):
            
            """"Return an independent copy of a position."""
            
            if g.app.tracePositions:
                g.trace("%-25s %-25s %s" % (
                    g.callerName(4),g.callerName(3),g.callerName(2)),align=10)
        
            return position(self.c,self.v,self.stack,trace=False)
        #@nonl
        #@-node:ekr.20050826134701.85:p.copy
        #@+node:ekr.20050826134701.86:p.dump & p.vnodeListIds
        def dumpLink (self,link):
        
            return g.choose(link,link,"<none>")
        
        def dump (self,label=""):
            
            p = self
            print '-'*10,label,p
            if p.v:
                p.v.dump() # Don't print a label
                
        def vnodeListIds (self):
            
            p = self
            return [id(v) for v in p.v.t.vnodeList]
        #@nonl
        #@-node:ekr.20050826134701.86:p.dump & p.vnodeListIds
        #@+node:ekr.20050826134701.87:p.equal & isEqual
        def equal(self,p2):
        
            """Return True if two postions are equivalent.
            
            Use this method when the speed comparisons is crucial
            
            N.B. Unlike __cmp__, p2 must not be None.
            """
        
            p1 = self
            # Check entire stack quickly.
            # The stack contains vnodes, so this does not call p.__cmp__.
            return (
                p1.v == p2.v and
                p1.stack == p2.stack and
                p1.childIndex() == p2.childIndex())
                
        isEqual = equal
        #@-node:ekr.20050826134701.87:p.equal & isEqual
        #@-node:ekr.20050826134701.79: ctor & other special methods...
        #@+node:ekr.20050826134701.88:Getters
        #@+node:ekr.20050826134701.89: vnode proxies
        #@+node:ekr.20050826134701.90:p.Comparisons
        def anyAtFileNodeName         (self): return self.v.anyAtFileNodeName()
        def atFileNodeName            (self): return self.v.atFileNodeName()
        def atNoSentinelsFileNodeName (self): return self.v.atNoSentinelsFileNodeName()
        def atRawFileNodeName         (self): return self.v.atRawFileNodeName()
        def atSilentFileNodeName      (self): return self.v.atSilentFileNodeName()
        def atThinFileNodeName        (self): return self.v.atThinFileNodeName()
        
        # New names, less confusing
        atNoSentFileNodeName  = atNoSentinelsFileNodeName
        atNorefFileNodeName   = atRawFileNodeName
        atAsisFileNodeName    = atSilentFileNodeName
        
        def isAnyAtFileNode         (self): return self.v.isAnyAtFileNode()
        def isAtAllNode             (self): return self.v.isAtAllNode()
        def isAtFileNode            (self): return self.v.isAtFileNode()
        def isAtIgnoreNode          (self): return self.v.isAtIgnoreNode()
        def isAtNoSentinelsFileNode (self): return self.v.isAtNoSentinelsFileNode()
        def isAtOthersNode          (self): return self.v.isAtOthersNode()
        def isAtRawFileNode         (self): return self.v.isAtRawFileNode()
        def isAtSilentFileNode      (self): return self.v.isAtSilentFileNode()
        def isAtThinFileNode        (self): return self.v.isAtThinFileNode()
        
        # New names, less confusing:
        isAtNoSentFileNode = isAtNoSentinelsFileNode
        isAtNorefFileNode  = isAtRawFileNode
        isAtAsisFileNode   = isAtSilentFileNode
        
        # Utilities.
        def matchHeadline (self,pattern): return self.v.matchHeadline(pattern)
        ## def afterHeadlineMatch (self,s): return self.v.afterHeadlineMatch(s)
        #@nonl
        #@-node:ekr.20050826134701.90:p.Comparisons
        #@+node:ekr.20050826134701.91:p.Extra Attributes
        def extraAttributes (self):
            
            return self.v.extraAttributes()
        
        def setExtraAttributes (self,data):
        
            return self.v.setExtraAttributes(data)
        #@nonl
        #@-node:ekr.20050826134701.91:p.Extra Attributes
        #@+node:ekr.20050826134701.92:p.Headline & body strings
        def bodyString (self):
            
            return self.v.bodyString()
        
        def headString (self):
            
            return self.v.headString()
            
        def cleanHeadString (self):
            
            return self.v.cleanHeadString()
        #@-node:ekr.20050826134701.92:p.Headline & body strings
        #@+node:ekr.20050826134701.93:p.Status bits
        def isDirty     (self): return self.v.isDirty()
        def isExpanded  (self): return self.v.isExpanded()
        def isMarked    (self): return self.v.isMarked()
        def isOrphan    (self): return self.v.isOrphan()
        def isSelected  (self): return self.v.isSelected()
        def isTopBitSet (self): return self.v.isTopBitSet()
        def isVisited   (self): return self.v.isVisited()
        def status      (self): return self.v.status()
        #@nonl
        #@-node:ekr.20050826134701.93:p.Status bits
        #@+node:ekr.20050826134701.94:p.edit_text
        def edit_widget (self):
            
            # New in 4.3 beta 3: let the tree classes do all the work.
            
            p = self ; c = p.c
            
            return c.frame.tree.edit_widget(p)
        #@nonl
        #@-node:ekr.20050826134701.94:p.edit_text
        #@+node:ekr.20050826134701.95:p.directParents
        def directParents (self):
            
            return self.v.directParents()
        #@-node:ekr.20050826134701.95:p.directParents
        #@+node:ekr.20050826134701.96:p.childIndex
        def childIndex(self):
            
            p = self ; v = p.v
            
            # This is time-critical code!
            
            # 3/25/04: Much faster code:
            if not v or not v._back:
                return 0
        
            n = 0 ; v = v._back
            while v:
                n += 1
                v = v._back
        
            return n
        #@nonl
        #@-node:ekr.20050826134701.96:p.childIndex
        #@-node:ekr.20050826134701.89: vnode proxies
        #@+node:ekr.20050826134701.97:children
        #@+node:ekr.20050826134701.98:p.hasChildren
        def hasChildren(self):
            
            p = self
            # g.trace(p,p.v)
            return p.v and p.v.t and p.v.t._firstChild
        #@nonl
        #@-node:ekr.20050826134701.98:p.hasChildren
        #@+node:ekr.20050826134701.99:p.numberOfChildren
        def numberOfChildren (self):
            
            return self.v.numberOfChildren()
        #@-node:ekr.20050826134701.99:p.numberOfChildren
        #@-node:ekr.20050826134701.97:children
        #@+node:ekr.20050826134701.100:p.exists
        def exists(self,c):
            
            """Return True if a position exists in c's tree"""
            
            p = self.copy()
        
            # This code must be fast.
            root = c.rootPosition()
        
            while p:
                # g.trace(p,'parent',p.parent(),'back',p.back())
                if p == root:
                    return True
                if p.hasParent():
                    p.moveToParent()
                else:
                    p.moveToBack()
                
            return False
        #@nonl
        #@-node:ekr.20050826134701.100:p.exists
        #@+node:ekr.20050826134701.101:p.findRoot
        def findRoot (self):
            
            return self.c.frame.rootPosition()
        #@nonl
        #@-node:ekr.20050826134701.101:p.findRoot
        #@+node:ekr.20050826134701.102:p.getX & vnode compatibility traversal routines
        # These methods are useful abbreviations.
        # Warning: they make copies of positions, so they should be used _sparingly_
        
        def getBack          (self): return self.copy().moveToBack()
        def getFirstChild    (self): return self.copy().moveToFirstChild()
        def getLastChild     (self): return self.copy().moveToLastChild()
        def getLastNode      (self): return self.copy().moveToLastNode()
        def getLastVisible   (self): return self.copy().moveToLastVisible()
        def getNext          (self): return self.copy().moveToNext()
        def getNodeAfterTree (self): return self.copy().moveToNodeAfterTree()
        def getNthChild    (self,n): return self.copy().moveToNthChild(n)
        def getParent        (self): return self.copy().moveToParent()
        def getThreadBack    (self): return self.copy().moveToThreadBack()
        def getThreadNext    (self): return self.copy().moveToThreadNext()
        def getVisBack       (self): return self.copy().moveToVisBack()
        def getVisNext       (self): return self.copy().moveToVisNext()
        
        # These are efficient enough now that iterators are the normal way to traverse the tree!
        
        back          = getBack
        firstChild    = getFirstChild
        lastChild     = getLastChild
        lastNode      = getLastNode
        lastVisible   = getLastVisible # New in 4.2 (was in tk tree code).
        next          = getNext
        nodeAfterTree = getNodeAfterTree
        nthChild      = getNthChild
        parent        = getParent
        threadBack    = getThreadBack
        threadNext    = getThreadNext
        visBack       = getVisBack
        visNext       = getVisNext
        #@nonl
        #@-node:ekr.20050826134701.102:p.getX & vnode compatibility traversal routines
        #@+node:ekr.20050826134701.103:p.hasX
        def hasBack(self):
            return self.v and self.v._back
        
        hasFirstChild = hasChildren
            
        def hasNext(self):
            return self.v and self.v._next
            
        def hasParent(self):
            return self.v and self.v._parent is not None
            
        def hasThreadBack(self):
            return self.hasParent() or self.hasBack() # Much cheaper than computing the actual value.
            
        hasVisBack = hasThreadBack
        #@nonl
        #@+node:ekr.20050826134701.104:hasThreadNext (the only complex hasX method)
        def hasThreadNext(self):
        
            p = self ; v = p.v
            if not p.v: return False
        
            if v.t._firstChild or v._next:
                return True
            else:
                n = len(p.stack)-1
                v,n = p.vParentWithStack(v,p.stack,n)
                while v:
                    if v._next:
                        return True
                    v,n = p.vParentWithStack(v,p.stack,n)
                return False
        
        hasVisNext = hasThreadNext
        #@nonl
        #@-node:ekr.20050826134701.104:hasThreadNext (the only complex hasX method)
        #@-node:ekr.20050826134701.103:p.hasX
        #@+node:ekr.20050826134701.105:p.isAncestorOf
        def isAncestorOf (self, p2):
            
            p = self
            
            if 0: # Avoid the copies made in the iterator.
                for p3 in p2.parents_iter():
                    if p3 == p:
                        return True
        
            # Avoid calling p.copy() or copying the stack.
            v2 = p2.v ; n = len(p2.stack)-1
                # Major bug fix 7/22/04: changed len(p.stack) to len(p2.stack.)
            v2,n = p2.vParentWithStack(v2,p2.stack,n)
            while v2:
                if v2 == p.v:
                    return True
                v2,n = p2.vParentWithStack(v2,p2.stack,n)
        
            return False
        #@nonl
        #@-node:ekr.20050826134701.105:p.isAncestorOf
        #@+node:ekr.20050826134701.106:p.isCurrentPosition & isRootPosition
        #@+node:ekr.20050826134701.107:isCurrentPosition
        def isCurrentPosition (self):
            
            p = self ; c = p.c
            
            return c.isCurrentPosition(p)
            
        #@-node:ekr.20050826134701.107:isCurrentPosition
        #@+node:ekr.20050826134701.108:isRootPosition
        def isRootPosition (self):
            
            p = self ; c = p.c
            
            return c.isRootPosition(p)
        #@nonl
        #@-node:ekr.20050826134701.108:isRootPosition
        #@-node:ekr.20050826134701.106:p.isCurrentPosition & isRootPosition
        #@+node:ekr.20050826134701.109:p.isCloned
        def isCloned (self):
            
            return len(self.v.t.vnodeList) > 1
        #@nonl
        #@-node:ekr.20050826134701.109:p.isCloned
        #@+node:ekr.20050826134701.110:p.isRoot
        def isRoot (self):
            
            p = self
        
            return not p.hasParent() and not p.hasBack()
        #@nonl
        #@-node:ekr.20050826134701.110:p.isRoot
        #@+node:ekr.20050826134701.111:p.isVisible
        def isVisible (self):
            
            """Return True if all of a position's parents are expanded."""
        
            # v.isVisible no longer exists.
            p = self
        
            # Avoid calling p.copy() or copying the stack.
            v = p.v ; n = len(p.stack)-1
        
            v,n = p.vParentWithStack(v,p.stack,n)
            while v:
                if not v.isExpanded():
                    return False
                v,n = p.vParentWithStack(v,p.stack,n)
        
            return True
        #@nonl
        #@-node:ekr.20050826134701.111:p.isVisible
        #@+node:ekr.20050826134701.112:p.lastVisible & oldLastVisible
        def oldLastVisible(self):
            """Move to the last visible node of the entire tree."""
            p = self.c.rootPosition()
            assert(p.isVisible())
            last = p.copy()
            while 1:
                if g.app.debug: g.trace(last)
                p.moveToVisNext()
                if not p: break
                last = p.copy()
            return last
                
        def lastVisible(self):
            """Move to the last visible node of the entire tree."""
            p = self.c.rootPosition()
            # Move to the last top-level node.
            while p.hasNext():
                if g.app.debug: g.trace(p)
                p.moveToNext()
            assert(p.isVisible())
            # Move to the last visible child.
            while p.hasChildren() and p.isExpanded():
                if g.app.debug: g.trace(p)
                p.moveToLastChild()
            if 0: # This assert is invalid.
                assert(p.isVisible())
            if g.app.debug: g.trace(p)
            return p
        #@nonl
        #@-node:ekr.20050826134701.112:p.lastVisible & oldLastVisible
        #@+node:ekr.20050826134701.113:p.level & simpleLevel
        def simpleLevel(self):
            
            return len([p for p in self.parents_iter()])
        
        def level(self,verbose=False):
            
            p = self ; level = 0
            if not p: return level
                
            # Avoid calling p.copy() or copying the stack.
            v = p.v ; n = len(p.stack)-1
            while 1:
                assert(p)
                v,n = p.vParentWithStack(v,p.stack,n)
                if v:
                    level += 1
                    if verbose: g.trace(level,"level %2d, n: %2d" % (level,n))
                else:
                    if verbose: g.trace(level,"level %2d, n: %2d" % (level,n))
                    # if g.app.debug: assert(level==self.simpleLevel())
                    break
            return level
        #@nonl
        #@-node:ekr.20050826134701.113:p.level & simpleLevel
        #@-node:ekr.20050826134701.88:Getters
        #@+node:ekr.20050826134701.114:Setters
        #@+node:ekr.20050826134701.115:vnode proxies
        #@+node:ekr.20050826134701.116: Status bits (position)
        # Clone bits are no longer used.
        # Dirty bits are handled carefully by the position class.
        
        def clearMarked  (self):
            self.v.clearMarked()
            g.doHook("clear-mark",c=self.c,p=self,v=self)
        
        def clearOrphan  (self): return self.v.clearOrphan()
        def clearVisited (self): return self.v.clearVisited()
        
        def contract (self): return self.v.contract()
        def expand   (self): return self.v.expand()
        
        def initExpandedBit    (self): return self.v.initExpandedBit()
        def initMarkedBit      (self): return self.v.initMarkedBit()
        def initStatus (self, status): return self.v.initStatus(status)
            
        def setMarked (self):
            self.v.setMarked()
            g.doHook("set-mark",c=self.c,p=self,v=self)
        
        def setOrphan   (self): return self.v.setOrphan()
        def setSelected (self): return self.v.setSelected()
        def setVisited  (self): return self.v.setVisited()
        #@nonl
        #@-node:ekr.20050826134701.116: Status bits (position)
        #@+node:ekr.20050826134701.117:p.computeIcon & p.setIcon
        def computeIcon (self):
            
            return self.v.computeIcon()
            
        def setIcon (self):
        
            pass # Compatibility routine for old scripts
        #@nonl
        #@-node:ekr.20050826134701.117:p.computeIcon & p.setIcon
        #@+node:ekr.20050826134701.118:p.setSelection
        def setSelection (self,start,length):
        
            return self.v.setSelection(start,length)
        #@nonl
        #@-node:ekr.20050826134701.118:p.setSelection
        #@+node:ekr.20050826134701.119:p.trimTrailingLines
        def trimTrailingLines (self):
        
            return self.v.trimTrailingLines()
        #@nonl
        #@-node:ekr.20050826134701.119:p.trimTrailingLines
        #@+node:ekr.20050826134701.120:p.setTnodeText
        def setTnodeText (self,s,encoding="utf-8"):
            
            return self.v.setTnodeText(s,encoding)
        #@nonl
        #@-node:ekr.20050826134701.120:p.setTnodeText
        #@-node:ekr.20050826134701.115:vnode proxies
        #@+node:ekr.20050826134701.121:Head & body text (position)
        #@+node:ekr.20050826134701.122:p.appendStringToBody
        def appendStringToBody (self,s,encoding="utf-8"):
            
            p = self
            if not s: return
            
            body = p.bodyString()
            assert(g.isUnicode(body))
            s = g.toUnicode(s,encoding)
        
            p.setBodyStringOrPane(body + s,encoding)
        #@nonl
        #@-node:ekr.20050826134701.122:p.appendStringToBody
        #@+node:ekr.20050826134701.123:p.setBodyStringOrPane & p.setBodyTextOrPane
        def setBodyStringOrPane (self,s,encoding="utf-8"):
        
            p = self ; v = p.v ; c = p.c
            if not c or not v: return
        
            s = g.toUnicode(s,encoding)
            current = c.currentPosition()
            # 1/22/05: Major change: the previous test was: 'if p == current:'
            # This worked because commands work on the presently selected node.
            # But setRecentFiles may change a _clone_ of the selected node!
            if current and p.v.t==current.v.t:
                # Revert to previous code, but force an empty selection.
                c.frame.body.setSelectionAreas(s,None,None)
                c.frame.body.setTextSelection(None)
                # This code destoys all tags, so we must recolor.
                c.recolor()
                
            # Keep the body text in the tnode up-to-date.
            if v.t.bodyString != s:
                v.setTnodeText(s)
                v.t.setSelection(0,0)
                p.setDirty()
                if not c.isChanged():
                    c.setChanged(True)
        
        setBodyTextOrPane = setBodyStringOrPane # Compatibility with old scripts
        #@nonl
        #@-node:ekr.20050826134701.123:p.setBodyStringOrPane & p.setBodyTextOrPane
        #@+node:ekr.20050826134701.124:p.setHeadString & p.initHeadString
        def setHeadString (self,s,encoding="utf-8"):
            
            p = self
            p.v.initHeadString(s,encoding)
            p.setDirty()
            
        def initHeadString (self,s,encoding="utf-8"):
            
            p = self
            p.v.initHeadString(s,encoding)
        #@-node:ekr.20050826134701.124:p.setHeadString & p.initHeadString
        #@+node:ekr.20050826134701.125:p.setHeadStringOrHeadline
        def setHeadStringOrHeadline (self,s,encoding="utf-8"):
        
            p = self ; t = p.edit_widget()
            
            p.initHeadString(s,encoding)
        
            if t:
                state = t.cget("state")
                # g.trace(state,s)
                t.configure(state="normal")
                t.delete("1.0","end")
                t.insert("end",s)
                t.configure(state=state)
        
            p.setDirty()
        #@nonl
        #@-node:ekr.20050826134701.125:p.setHeadStringOrHeadline
        #@+node:ekr.20050826134701.126:p.scriptSetBodyString
        def scriptSetBodyString (self,s,encoding="utf-8"):
            
            """Update the body string for the receiver.
            
            Should be called only from scripts: does NOT update body text."""
        
            self.v.t.bodyString = g.toUnicode(s,encoding)
        #@nonl
        #@-node:ekr.20050826134701.126:p.scriptSetBodyString
        #@-node:ekr.20050826134701.121:Head & body text (position)
        #@+node:ekr.20050826134701.127:Visited bits
        #@+node:ekr.20050826134701.128:p.clearAllVisited
        # Compatibility routine for scripts.
        
        def clearAllVisited (self):
            
            for p in self.allNodes_iter():
                p.clearVisited()
        #@nonl
        #@-node:ekr.20050826134701.128:p.clearAllVisited
        #@+node:ekr.20050826134701.129:p.clearVisitedInTree
        # Compatibility routine for scripts.
        
        def clearVisitedInTree (self):
            
            for p in self.self_and_subtree_iter():
                p.clearVisited()
        #@-node:ekr.20050826134701.129:p.clearVisitedInTree
        #@+node:ekr.20050826134701.130:p.clearAllVisitedInTree (4.2)
        def clearAllVisitedInTree (self):
            
            for p in self.self_and_subtree_iter():
                p.v.clearVisited()
                p.v.t.clearVisited()
                p.v.t.clearWriteBit()
        #@nonl
        #@-node:ekr.20050826134701.130:p.clearAllVisitedInTree (4.2)
        #@-node:ekr.20050826134701.127:Visited bits
        #@+node:ekr.20050826134701.131:p.Dirty bits
        #@+node:ekr.20050826134701.132:p.clearDirty
        def clearDirty (self):
        
            p = self
            p.v.clearDirty()
        #@nonl
        #@-node:ekr.20050826134701.132:p.clearDirty
        #@+node:ekr.20050826134701.133:p.findAllPotentiallyDirtyNodes
        def findAllPotentiallyDirtyNodes(self):
            
            p = self 
            
            # Start with all nodes in the vnodeList.
            nodes = []
            newNodes = p.v.t.vnodeList[:]
        
            # Add nodes until no more are added.
            while newNodes:
                addedNodes = []
                nodes.extend(newNodes)
                for v in newNodes:
                    for v2 in v.t.vnodeList:
                        if v2 not in nodes and v2 not in addedNodes:
                            addedNodes.append(v2)
                        for v3 in v2.directParents():
                            if v3 not in nodes and v3 not in addedNodes:
                                addedNodes.append(v3)
                newNodes = addedNodes[:]
        
            # g.trace(len(nodes))
            return nodes
        #@nonl
        #@-node:ekr.20050826134701.133:p.findAllPotentiallyDirtyNodes
        #@+node:ekr.20050826134701.134:p.setAllAncestorAtFileNodesDirty
        def setAllAncestorAtFileNodesDirty (self,setDescendentsDirty=False):
        
            p = self ; c = p.c
            dirtyVnodeList = []
            
            # Calculate all nodes that are joined to p or parents of such nodes.
            nodes = p.findAllPotentiallyDirtyNodes()
            
            if setDescendentsDirty:
                # N.B. Only mark _direct_ descendents of nodes.
                # Using the findAllPotentiallyDirtyNodes algorithm would mark way too many nodes.
                for p2 in p.subtree_iter():
                    # Only @thin nodes need to be marked.
                    if p2.v not in nodes and p2.isAtThinFileNode():
                        nodes.append(p2.v)
                        
            dirtyVnodeList = [v for v in nodes
                if not v.t.isDirty() and v.isAnyAtFileNode()]
            changed = len(dirtyVnodeList) > 0
        
            c.beginUpdate()
            for v in dirtyVnodeList:
                v.t.setDirty() # Do not call v.setDirty here!
            c.endUpdate(changed)
        
            return dirtyVnodeList
        #@nonl
        #@-node:ekr.20050826134701.134:p.setAllAncestorAtFileNodesDirty
        #@+node:ekr.20050826134701.135:p.setDirty
        # Ensures that all ancestor and descentent @file nodes are marked dirty.
        # It is much safer to do it this way.
        
        def setDirty (self,setDescendentsDirty=True):
        
            p = self ; c = p.c ; dirtyVnodeList = []
            # g.trace(g.app.count) ; g.app.count += 1
        
            c.beginUpdate()
            if 1: # update...
                if not p.v.t.isDirty():
                    p.v.t.setDirty()
                    dirtyVnodeList.append(p.v)
                # N.B. This must be called even if p.v is already dirty.
                # Typing can change the @ignore state!
                dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty(setDescendentsDirty)
                dirtyVnodeList.extend(dirtyVnodeList2)
                changed = len(dirtyVnodeList) > 0
            c.endUpdate(changed)
        
            return dirtyVnodeList
        #@nonl
        #@-node:ekr.20050826134701.135:p.setDirty
        #@+node:ekr.20050826134701.136:p.inAtIgnoreRange
        def inAtIgnoreRange (self):
            
            """Returns True if position p or one of p's parents is an @ignore node."""
            
            p = self
            
            for p in p.self_and_parents_iter():
                if p.isAtIgnoreNode():
                    return True
        
            return False
        #@nonl
        #@-node:ekr.20050826134701.136:p.inAtIgnoreRange
        #@-node:ekr.20050826134701.131:p.Dirty bits
        #@-node:ekr.20050826134701.114:Setters
        #@+node:ekr.20050826134701.137:File Conversion
        #@+at
        # - convertTreeToString and moreHead can't be vnode methods because 
        # they uses level().
        # - moreBody could be anywhere: it may as well be a postion method.
        #@-at
        #@+node:ekr.20050826134701.138:convertTreeToString
        def convertTreeToString (self):
            
            """Convert a positions  suboutline to a string in MORE format."""
        
            p = self ; level1 = p.level()
            
            array = []
            for p in p.self_and_subtree_iter():
                array.append(p.moreHead(level1)+'\n')
                body = p.moreBody()
                if body:
                    array.append(body +'\n')
        
            return ''.join(array)
        #@-node:ekr.20050826134701.138:convertTreeToString
        #@+node:ekr.20050826134701.139:moreHead
        def moreHead (self, firstLevel,useVerticalBar=False):
            
            """Return the headline string in MORE format."""
            
            # useVerticalBar is unused, but it would be useful in over-ridden methods.
            __pychecker__ = '--no-argsused'
        
            p = self
            level = self.level() - firstLevel
            plusMinus = g.choose(p.hasChildren(), "+", "-")
            
            return "%s%s %s" % ('\t'*level,plusMinus,p.headString())
        #@nonl
        #@-node:ekr.20050826134701.139:moreHead
        #@+node:ekr.20050826134701.140:moreBody
        #@+at 
        #     + test line
        #     - test line
        #     \ test line
        #     test line +
        #     test line -
        #     test line \
        #     More lines...
        #@-at
        #@@c
        
        def moreBody (self):
        
            """Returns the body string in MORE format.  
            
            Inserts a backslash before any leading plus, minus or backslash."""
        
            p = self ; array = []
            lines = string.split(p.bodyString(),'\n')
            for s in lines:
                i = g.skip_ws(s,0)
                if i < len(s) and s[i] in ('+','-','\\'):
                    s = s[:i] + '\\' + s[i:]
                array.append(s)
            return '\n'.join(array)
        #@nonl
        #@-node:ekr.20050826134701.140:moreBody
        #@-node:ekr.20050826134701.137:File Conversion
        #@+node:ekr.20050826134701.141:p.Iterators
        #@+at 
        #@nonl
        # 3/18/04: a crucial optimization:
        # 
        # Iterators make no copies at all if they would return an empty 
        # sequence.
        #@-at
        #@@c
        
        #@+others
        #@+node:ekr.20050826134701.142:p.tnodes_iter & unique_tnodes_iter
        def tnodes_iter(self):
            
            """Return all tnode's in a positions subtree."""
            
            p = self
            for p in p.self_and_subtree_iter():
                yield p.v.t
                
        def unique_tnodes_iter(self):
            
            """Return all unique tnode's in a positions subtree."""
            
            p = self
            marks = {}
            for p in p.self_and_subtree_iter():
                if p.v.t not in marks:
                    marks[p.v.t] = p.v.t
                    yield p.v.t
        #@nonl
        #@-node:ekr.20050826134701.142:p.tnodes_iter & unique_tnodes_iter
        #@+node:ekr.20050826134701.143:p.vnodes_iter & unique_vnodes_iter
        def vnodes_iter(self):
            
            """Return all vnode's in a positions subtree."""
            
            p = self
            for p in p.self_and_subtree_iter():
                yield p.v
                
        def unique_vnodes_iter(self):
            
            """Return all unique vnode's in a positions subtree."""
            
            p = self
            marks = {}
            for p in p.self_and_subtree_iter():
                if p.v not in marks:
                    marks[p.v] = p.v
                    yield p.v
        #@nonl
        #@-node:ekr.20050826134701.143:p.vnodes_iter & unique_vnodes_iter
        #@+node:ekr.20050826134701.144:p.allNodes_iter
        class allNodes_iter_class:
        
            """Returns a list of positions in the entire outline."""
        
            #@    @+others
            #@+node:ekr.20050826134701.145:__init__ & __iter__
            def __init__(self,p,copy):
            
                self.first = p.c.rootPosition().copy()
                self.p = None
                self.copy = copy
                
            def __iter__(self):
            
                return self
            #@-node:ekr.20050826134701.145:__init__ & __iter__
            #@+node:ekr.20050826134701.146:next
            def next(self):
                
                if self.first:
                    self.p = self.first
                    self.first = None
            
                elif self.p:
                    self.p.moveToThreadNext()
            
                if self.p:
                    if self.copy: return self.p.copy()
                    else:         return self.p
                else: raise StopIteration
            #@nonl
            #@-node:ekr.20050826134701.146:next
            #@-others
        
        def allNodes_iter (self,copy=False):
            
            return self.allNodes_iter_class(self,copy)
        #@nonl
        #@-node:ekr.20050826134701.144:p.allNodes_iter
        #@+node:ekr.20050826134701.147:p.subtree_iter
        class subtree_iter_class:
        
            """Returns a list of positions in a subtree, possibly including the root of the subtree."""
        
            #@    @+others
            #@+node:ekr.20050826134701.148:__init__ & __iter__
            def __init__(self,p,copy,includeSelf):
                
                if includeSelf:
                    self.first = p.copy()
                    self.after = p.nodeAfterTree()
                elif p.hasChildren():
                    self.first = p.copy().moveToFirstChild() 
                    self.after = p.nodeAfterTree()
                else:
                    self.first = None
                    self.after = None
            
                self.p = None
                self.copy = copy
                
            def __iter__(self):
            
                return self
            #@-node:ekr.20050826134701.148:__init__ & __iter__
            #@+node:ekr.20050826134701.149:next
            def next(self):
                
                if self.first:
                    self.p = self.first
                    self.first = None
            
                elif self.p:
                    self.p.moveToThreadNext()
            
                if self.p and self.p != self.after:
                    if self.copy: return self.p.copy()
                    else:         return self.p
                else:
                    raise StopIteration
            #@nonl
            #@-node:ekr.20050826134701.149:next
            #@-others
        
        def subtree_iter (self,copy=False):
            
            return self.subtree_iter_class(self,copy,includeSelf=False)
            
        def self_and_subtree_iter (self,copy=False):
            
            return self.subtree_iter_class(self,copy,includeSelf=True)
        #@nonl
        #@-node:ekr.20050826134701.147:p.subtree_iter
        #@+node:ekr.20050826134701.150:p.children_iter
        class children_iter_class:
        
            """Returns a list of children of a position."""
        
            #@    @+others
            #@+node:ekr.20050826134701.151:__init__ & __iter__
            def __init__(self,p,copy):
            
                if p.hasChildren():
                    self.first = p.copy().moveToFirstChild()
                else:
                    self.first = None
            
                self.p = None
                self.copy = copy
            
            def __iter__(self):
                
                return self
            #@-node:ekr.20050826134701.151:__init__ & __iter__
            #@+node:ekr.20050826134701.152:next
            def next(self):
                
                if self.first:
                    self.p = self.first
                    self.first = None
            
                elif self.p:
                    self.p.moveToNext()
            
                if self.p:
                    if self.copy: return self.p.copy()
                    else:         return self.p
                else: raise StopIteration
            #@nonl
            #@-node:ekr.20050826134701.152:next
            #@-others
        
        def children_iter (self,copy=False):
            
            return self.children_iter_class(self,copy)
        #@nonl
        #@-node:ekr.20050826134701.150:p.children_iter
        #@+node:ekr.20050826134701.153:p.parents_iter
        class parents_iter_class:
        
            """Returns a list of positions of a position."""
        
            #@    @+others
            #@+node:ekr.20050826134701.154:__init__ & __iter__
            def __init__(self,p,copy,includeSelf):
            
                if includeSelf:
                    self.first = p.copy()
                elif p.hasParent():
                    self.first = p.copy().moveToParent()
                else:
                    self.first = None
            
                self.p = None
                self.copy = copy
            
            def __iter__(self):
            
                return self
            #@nonl
            #@-node:ekr.20050826134701.154:__init__ & __iter__
            #@+node:ekr.20050826134701.155:next
            def next(self):
                
                if self.first:
                    self.p = self.first
                    self.first = None
            
                elif self.p:
                    self.p.moveToParent()
            
                if self.p:
                    if self.copy: return self.p.copy()
                    else:         return self.p
                else:
                    raise StopIteration
            #@-node:ekr.20050826134701.155:next
            #@-others
        
        def parents_iter (self,copy=False):
        
            return self.parents_iter_class(self,copy,includeSelf=False)
            
        def self_and_parents_iter(self,copy=False):
            
            return self.parents_iter_class(self,copy,includeSelf=True)
        #@nonl
        #@-node:ekr.20050826134701.153:p.parents_iter
        #@+node:ekr.20050826134701.156:p.siblings_iter
        class siblings_iter_class:
        
            '''Returns a list of siblings of a position, including the position itself!'''
        
            #@    @+others
            #@+node:ekr.20050826134701.157:__init__ & __iter__
            def __init__(self,p,copy,following):
                
                # We always include p, even if following is True.
                
                if following:
                    self.first = p.copy()
                else:
                    p = p.copy()
                    while p.hasBack():
                        p.moveToBack()
                    self.first = p
            
                self.p = None
                self.copy = copy
            
            def __iter__(self):
                
                return self
            
            #@-node:ekr.20050826134701.157:__init__ & __iter__
            #@+node:ekr.20050826134701.158:next
            def next(self):
                
                if self.first:
                    self.p = self.first
                    self.first = None
            
                elif self.p:
                    self.p.moveToNext()
            
                if self.p:
                    if self.copy: return self.p.copy()
                    else:         return self.p
                else: raise StopIteration
            #@nonl
            #@-node:ekr.20050826134701.158:next
            #@-others
        
        def siblings_iter (self,copy=False,following=False):
            
            return self.siblings_iter_class(self,copy,following)
            
        self_and_siblings_iter = siblings_iter
            
        def following_siblings_iter (self,copy=False):
            
            return self.siblings_iter_class(self,copy,following=True)
        #@nonl
        #@-node:ekr.20050826134701.156:p.siblings_iter
        #@-others
        #@nonl
        #@-node:ekr.20050826134701.141:p.Iterators
        #@+node:ekr.20050826134701.159:p.Moving, Inserting, Deleting, Cloning, Sorting (position)
        #@+node:ekr.20050826134701.160:p.doDelete
        #@+at 
        #@nonl
        # This is the main delete routine.  It deletes the receiver's entire 
        # tree from the screen.  Because of the undo command we never actually 
        # delete vnodes or tnodes.
        #@-at
        #@@c
        
        def doDelete (self,newPosition):
        
            """Deletes position p from the outline.  May be undone.
        
            Returns newPosition."""
        
            p = self ; c = p.c
        
            assert(newPosition != p)
            p.setDirty() # Mark @file nodes dirty!
            p.unlink()
            p.deleteLinksInTree()
            c.selectVnode(newPosition)
            
            return newPosition
        
        #@-node:ekr.20050826134701.160:p.doDelete
        #@+node:ekr.20050826134701.161:p.insertAfter
        def insertAfter (self,t=None):
        
            """Inserts a new position after self.
            
            Returns the newly created position."""
            
            p = self ; c = p.c
            p2 = self.copy()
        
            if not t:
                t = tnode(headString="NewHeadline")
        
            p2.v = vnode(c,t)
            p2.v.iconVal = 0
            p2.linkAfter(p)
        
            return p2
        #@nonl
        #@-node:ekr.20050826134701.161:p.insertAfter
        #@+node:ekr.20050826134701.162:p.insertAsLastChild
        def insertAsLastChild (self,t=None):
        
            """Inserts a new vnode as the last child of self.
            
            Returns the newly created position."""
            
            p = self
            n = p.numberOfChildren()
        
            if not t:
                t = tnode(headString="NewHeadline")
            
            return p.insertAsNthChild(n,t)
        #@nonl
        #@-node:ekr.20050826134701.162:p.insertAsLastChild
        #@+node:ekr.20050826134701.163:p.insertAsNthChild
        def insertAsNthChild (self,n,t=None):
        
            """Inserts a new node as the the nth child of self.
            self must have at least n-1 children.
            
            Returns the newly created position."""
            
            p = self ; c = p.c
            p2 = self.copy()
        
            if not t:
                t = tnode(headString="NewHeadline")
            
            p2.v = vnode(c,t)
            p2.v.iconVal = 0
            p2.linkAsNthChild(p,n)
        
            return p2
        #@nonl
        #@-node:ekr.20050826134701.163:p.insertAsNthChild
        #@+node:ekr.20050826134701.164:p.moveToRoot
        def moveToRoot (self,oldRoot=None):
        
            """Moves a position to the root position."""
        
            p = self # Do NOT copy the position!
            p.unlink()
            p.linkAsRoot(oldRoot)
            
            return p
        #@nonl
        #@-node:ekr.20050826134701.164:p.moveToRoot
        #@+node:ekr.20050826134701.165:p.clone
        def clone (self,back):
            
            """Create a clone of back.
            
            Returns the newly created position."""
            
            p = self ; c = p.c
            
            # g.trace(p,back)
        
            p2 = back.copy()
            p2.v = vnode(c,back.v.t)
            p2.linkAfter(back)
        
            return p2
        #@nonl
        #@-node:ekr.20050826134701.165:p.clone
        #@+node:ekr.20050826134701.166:p.copyTreeAfter, copyTreeTo
        # This is used by unit tests.
        
        def copyTreeAfter(self):
            p = self
            p2 = p.insertAfter()
            p.copyTreeFromSelfTo(p2)
            return p2
            
        def copyTreeFromSelfTo(self,p2):
            p = self
            p2.v.t.headString = p.headString()
            p2.v.t.bodyString = p.bodyString()
            for child in p.children_iter(copy=True):
                child2 = p2.insertAsLastChild()
                child.copyTreeFromSelfTo(child2)
        #@nonl
        #@-node:ekr.20050826134701.166:p.copyTreeAfter, copyTreeTo
        #@+node:ekr.20050826134701.167:p.moveAfter
        def moveAfter (self,a):
        
            """Move a position after position a."""
            
            p = self ; c = p.c # Do NOT copy the position!
            p.unlink()
            p.linkAfter(a)
            
            # Moving a node after another node can create a new root node.
            if not a.hasParent() and not a.hasBack():
                c.setRootPosition(a)
        
            return p
        #@nonl
        #@-node:ekr.20050826134701.167:p.moveAfter
        #@+node:ekr.20050826134701.168:p.moveToLastChildOf
        def moveToLastChildOf (self,parent):
        
            """Move a position to the last child of parent."""
        
            p = self # Do NOT copy the position!
        
            p.unlink()
            n = parent.numberOfChildren()
            p.linkAsNthChild(parent,n)
        
            # Moving a node can create a new root node.
            if not parent.hasParent() and not parent.hasBack():
                p.c.setRootPosition(parent)
                
            return p
        #@-node:ekr.20050826134701.168:p.moveToLastChildOf
        #@+node:ekr.20050826134701.169:p.moveToNthChildOf
        def moveToNthChildOf (self,parent,n):
        
            """Move a position to the nth child of parent."""
        
            p = self ; c = p.c # Do NOT copy the position!
            
            # g.trace(p,parent,n)
        
            p.unlink()
            p.linkAsNthChild(parent,n)
            
            # Moving a node can create a new root node.
            if not parent.hasParent() and not parent.hasBack():
                c.setRootPosition(parent)
        
            return p
        #@-node:ekr.20050826134701.169:p.moveToNthChildOf
        #@+node:ekr.20050826134701.170:p.validateOutlineWithParent
        # This routine checks the structure of the receiver's tree.
        
        def validateOutlineWithParent (self,pv):
            
            p = self
            result = True # optimists get only unpleasant surprises.
            parent = p.getParent()
            childIndex = p.childIndex()
            
            # g.trace(p,parent,pv)
            #@    << validate parent ivar >>
            #@+node:ekr.20050826134701.171:<< validate parent ivar >>
            if parent != pv:
                p.invalidOutline( "Invalid parent link: " + repr(parent))
            #@nonl
            #@-node:ekr.20050826134701.171:<< validate parent ivar >>
            #@nl
            #@    << validate childIndex ivar >>
            #@+node:ekr.20050826134701.172:<< validate childIndex ivar >>
            if pv:
                if childIndex < 0:
                    p.invalidOutline ( "missing childIndex" + childIndex )
                elif childIndex >= pv.numberOfChildren():
                    p.invalidOutline ( "missing children entry for index: " + childIndex )
            elif childIndex < 0:
                p.invalidOutline ( "negative childIndex" + childIndex )
            #@nonl
            #@-node:ekr.20050826134701.172:<< validate childIndex ivar >>
            #@nl
            #@    << validate x ivar >>
            #@+node:ekr.20050826134701.173:<< validate x ivar >>
            if not p.v.t and pv:
                self.invalidOutline ( "Empty t" )
            #@nonl
            #@-node:ekr.20050826134701.173:<< validate x ivar >>
            #@nl
        
            # Recursively validate all the children.
            for child in p.children_iter():
                r = child.validateOutlineWithParent(p)
                if not r: result = False
        
            return result
        #@nonl
        #@-node:ekr.20050826134701.170:p.validateOutlineWithParent
        #@+node:ekr.20050826134701.174:p.invalidOutline
        def invalidOutline (self, message):
            
            p = self
        
            if p.hasParent():
                node = p.parent()
            else:
                node = p
        
            g.alert("invalid outline: %s\n%s" % (message,node))
        #@nonl
        #@-node:ekr.20050826134701.174:p.invalidOutline
        #@-node:ekr.20050826134701.159:p.Moving, Inserting, Deleting, Cloning, Sorting (position)
        #@+node:ekr.20050826134701.175:p.moveToX
        #@+at
        # These routines change self to a new position "in place".
        # That is, these methods must _never_ call p.copy().
        # 
        # When moving to a nonexistent position, these routines simply set p.v 
        # = None,
        # leaving the p.stack unchanged. This allows the caller to "undo" the 
        # effect of
        # the invalid move by simply restoring the previous value of p.v.
        # 
        # These routines all return self on exit so the following kind of code 
        # will work:
        #     after = p.copy().moveToNodeAfterTree()
        #@-at
        #@nonl
        #@+node:ekr.20050826134701.176:p.moveToBack
        def moveToBack (self):
            
            """Move self to its previous sibling."""
            
            p = self
        
            p.v = p.v and p.v._back
            
            return p
        #@nonl
        #@-node:ekr.20050826134701.176:p.moveToBack
        #@+node:ekr.20050826134701.177:p.moveToFirstChild (pushes stack for cloned nodes)
        def moveToFirstChild (self):
        
            """Move a position to it's first child's position."""
            
            p = self
        
            if p:
                child = p.v.t._firstChild
                if child:
                    if p.isCloned():
                        p.stack.append(p.v)
                        # g.trace("push",p.v,p)
                    p.v = child
                else:
                    p.v = None
                
            return p
        
        #@-node:ekr.20050826134701.177:p.moveToFirstChild (pushes stack for cloned nodes)
        #@+node:ekr.20050826134701.178:p.moveToLastChild (pushes stack for cloned nodes)
        def moveToLastChild (self):
            
            """Move a position to it's last child's position."""
            
            p = self
        
            if p:
                if p.v.t._firstChild:
                    child = p.v.lastChild()
                    if p.isCloned():
                        p.stack.append(p.v)
                        # g.trace("push",p.v,p)
                    p.v = child
                else:
                    p.v = None
                    
            return p
        #@-node:ekr.20050826134701.178:p.moveToLastChild (pushes stack for cloned nodes)
        #@+node:ekr.20050826134701.179:p.moveToLastNode (Big improvement for 4.2)
        def moveToLastNode (self):
            
            """Move a position to last node of its tree.
            
            N.B. Returns p if p has no children."""
            
            p = self
            
            # Huge improvement for 4.2.
            while p.hasChildren():
                p.moveToLastChild()
        
            return p
        #@nonl
        #@-node:ekr.20050826134701.179:p.moveToLastNode (Big improvement for 4.2)
        #@+node:ekr.20050826134701.180:p.moveToNext
        def moveToNext (self):
            
            """Move a position to its next sibling."""
            
            p = self
            
            p.v = p.v and p.v._next
            
            return p
        #@nonl
        #@-node:ekr.20050826134701.180:p.moveToNext
        #@+node:ekr.20050826134701.181:p.moveToNodeAfterTree
        def moveToNodeAfterTree (self):
            
            """Move a position to the node after the position's tree."""
            
            p = self
            
            while p:
                if p.hasNext():
                    p.moveToNext()
                    break
                p.moveToParent()
        
            return p
        #@-node:ekr.20050826134701.181:p.moveToNodeAfterTree
        #@+node:ekr.20050826134701.182:p.moveToNthChild (pushes stack for cloned nodes)
        def moveToNthChild (self,n):
            
            p = self
            
            if p:
                child = p.v.nthChild(n) # Must call vnode method here!
                if child:
                    if p.isCloned():
                        p.stack.append(p.v)
                        # g.trace("push",p.v,p)
                    p.v = child
                else:
                    p.v = None
                    
            return p
        #@nonl
        #@-node:ekr.20050826134701.182:p.moveToNthChild (pushes stack for cloned nodes)
        #@+node:ekr.20050826134701.183:p.moveToParent (pops stack when multiple parents)
        def moveToParent (self):
            
            """Move a position to its parent position."""
            
            p = self
            
            if not p: return p
        
            if p.v._parent and len(p.v._parent.t.vnodeList) == 1:
                p.v = p.v._parent
            elif p.stack:
                p.v = p.stack.pop()
            else:
                p.v = None
            return p
        #@nonl
        #@-node:ekr.20050826134701.183:p.moveToParent (pops stack when multiple parents)
        #@+node:ekr.20050826134701.184:p.moveToThreadBack
        def moveToThreadBack (self):
            
            """Move a position to it's threadBack position."""
        
            p = self
        
            if p.hasBack():
                p.moveToBack()
                p.moveToLastNode()
            else:
                p.moveToParent()
        
            return p
        #@nonl
        #@-node:ekr.20050826134701.184:p.moveToThreadBack
        #@+node:ekr.20050826134701.185:p.moveToThreadNext
        def moveToThreadNext (self):
            
            """Move a position to the next a position in threading order."""
            
            p = self
        
            if p:
                if p.v.t._firstChild:
                    p.moveToFirstChild()
                elif p.v._next:
                    p.moveToNext()
                else:
                    p.moveToParent()
                    while p:
                        if p.v._next:
                            p.moveToNext()
                            break #found
                        p.moveToParent()
                    # not found.
                        
            return p
        #@nonl
        #@-node:ekr.20050826134701.185:p.moveToThreadNext
        #@+node:ekr.20050826134701.186:p.moveToVisBack
        def moveToVisBack (self):
            
            """Move a position to the position of the previous visible node."""
        
            p = self
            
            if p:
                p.moveToThreadBack()
                while p and not p.isVisible():
                    p.moveToThreadBack()
        
            assert(not p or p.isVisible())
            return p
        #@nonl
        #@-node:ekr.20050826134701.186:p.moveToVisBack
        #@+node:ekr.20050826134701.187:p.moveToVisNext
        def moveToVisNext (self):
            
            """Move a position to the position of the next visible node."""
        
            p = self
        
            p.moveToThreadNext()
            while p and not p.isVisible():
                p.moveToThreadNext()
                    
            return p
        #@nonl
        #@-node:ekr.20050826134701.187:p.moveToVisNext
        #@-node:ekr.20050826134701.175:p.moveToX
        #@+node:ekr.20050826134701.188:p.utils...
        #@+node:ekr.20050826134701.189:p.vParentWithStack
        # A crucial utility method.
        # The p.level(), p.isVisible() and p.hasThreadNext() methods show how to use this method.
        
        #@<< about the vParentWithStack utility method >>
        #@+node:ekr.20050826134701.190:<< about the vParentWithStack utility method >>
        #@+at 
        # This method allows us to simulate calls to p.parent() without 
        # generating any intermediate data.
        # 
        # For example, the code below will compute the same values for list1 
        # and list2:
        # 
        # # The first way depends on the call to p.copy:
        # list1 = []
        # p=p.copy() # odious.
        # while p:
        #     p = p.moveToParent()
        #     if p: list1.append(p.v)
        # 
        # # The second way uses p.vParentWithStack to avoid all odious 
        # intermediate data.
        # 
        # list2 = []
        # n = len(p.stack)-1
        # v,n = p.vParentWithStack(v,p.stack,n)
        # while v:
        #     list2.append(v)
        #     v,n = p.vParentWithStack(v,p.stack,n)
        # 
        #@-at
        #@-node:ekr.20050826134701.190:<< about the vParentWithStack utility method >>
        #@nl
        
        def vParentWithStack(self,v,stack,n):
            
            """A utility that allows the computation of p.v without calling p.copy().
            
            v,stack[:n] correspond to p.v,p.stack for some intermediate position p.
        
            Returns (v,n) such that v,stack[:n] correpond to the parent position of p."""
        
            if not v:
                return None,n
            elif v._parent and len(v._parent.t.vnodeList) == 1:
                return v._parent,n # don't change stack.
            elif stack and n >= 0:
                return self.stack[n],n-1 # simulate popping the stack.
            else:
                return None,n
        #@nonl
        #@-node:ekr.20050826134701.189:p.vParentWithStack
        #@+node:ekr.20050826134701.191:p.restoreLinksInTree
        def restoreLinksInTree (self):
        
            """Restore links when undoing a delete node operation."""
            
            root = p = self
        
            if p.v not in p.v.t.vnodeList:
                p.v.t.vnodeList.append(p.v)
                p.v.t._p_changed = True # zodb support.
                
            for p in root.children_iter():
                p.restoreLinksInTree()
        #@nonl
        #@-node:ekr.20050826134701.191:p.restoreLinksInTree
        #@+node:ekr.20050826134701.192:p.deleteLinksInTree & allies
        def deleteLinksInTree (self):
            
            """Delete and otherwise adjust links when deleting node."""
            
            root = self
        
            root.deleteLinksInSubtree()
            
            for p in root.children_iter():
                p.adjustParentLinksInSubtree(parent=root)
        #@nonl
        #@+node:ekr.20050826134701.193:p.deleteLinksInSubtree
        def deleteLinksInSubtree (self):
        
            root = p = self
        
            # Delete p.v from the vnodeList
            if p.v in p.v.t.vnodeList:
                p.v.t.vnodeList.remove(p.v)
                p.v.t._p_changed = True # zodb support.
                assert(p.v not in p.v.t.vnodeList)
                # g.trace("deleted",p.v,p.vnodeListIds())
            else:
                # g.trace("not in vnodeList",p.v,p.vnodeListIds())
                pass
        
            if len(p.v.t.vnodeList) == 0:
                # This node is not shared by other nodes.
                for p in root.children_iter():
                    p.deleteLinksInSubtree()
        #@nonl
        #@-node:ekr.20050826134701.193:p.deleteLinksInSubtree
        #@+node:ekr.20050826134701.194:p.adjustParentLinksInSubtree
        def adjustParentLinksInSubtree (self,parent):
            
            root = p = self
            
            assert(parent)
            
            if p.v._parent and parent.v.t.vnodeList and p.v._parent not in parent.v.t.vnodeList:
                p.v._parent = parent.v.t.vnodeList[0]
                
            for p in root.children_iter():
                p.adjustParentLinksInSubtree(parent=root)
        #@nonl
        #@-node:ekr.20050826134701.194:p.adjustParentLinksInSubtree
        #@-node:ekr.20050826134701.192:p.deleteLinksInTree & allies
        #@-node:ekr.20050826134701.188:p.utils...
        #@+node:ekr.20050826134701.195:p.Link/Unlink methods
        # These remain in 4.2:  linking and unlinking does not depend on position.
        
        # These are private routines:  the position class does not define proxies for these.
        #@nonl
        #@+node:ekr.20050826134701.196:p.linkAfter
        def linkAfter (self,after):
        
            """Link self after v."""
            
            p = self
            # g.trace(p,after)
            
            p.stack = after.stack[:] # 3/12/04
            p.v._parent = after.v._parent
            
            # Add v to it's tnode's vnodeList.
            if p.v not in p.v.t.vnodeList:
                p.v.t.vnodeList.append(p.v)
                p.v.t._p_changed = True # zodb support.
            
            p.v._back = after.v
            p.v._next = after.v._next
            
            after.v._next = p.v
            
            if p.v._next:
                p.v._next._back = p.v
        
            if 0:
                g.trace('-'*20,after)
                p.dump(label="p")
                after.dump(label="back")
                if p.hasNext(): p.next().dump(label="next")
        #@nonl
        #@-node:ekr.20050826134701.196:p.linkAfter
        #@+node:ekr.20050826134701.197:p.linkAsNthChild
        def linkAsNthChild (self,parent,n):
        
            """Links self as the n'th child of vnode pv"""
            
            # g.trace(self,parent,n)
            p = self
        
            # Recreate the stack using the parent.
            p.stack = parent.stack[:] 
            if parent.isCloned():
                p.stack.append(parent.v)
        
            p.v._parent = parent.v
        
            # Add v to it's tnode's vnodeList.
            if p.v not in p.v.t.vnodeList:
                p.v.t.vnodeList.append(p.v)
                p.v.t._p_changed = True # zodb support.
        
            if n == 0:
                child1 = parent.v.t._firstChild
                p.v._back = None
                p.v._next = child1
                if child1:
                    child1._back = p.v
                parent.v.t._firstChild = p.v
            else:
                prev = parent.nthChild(n-1) # zero based
                assert(prev)
                p.v._back = prev.v
                p.v._next = prev.v._next
                prev.v._next = p.v
                if p.v._next:
                    p.v._next._back = p.v
                    
            if 0:
                g.trace('-'*20)
                p.dump(label="p")
                parent.dump(label="parent")
        #@nonl
        #@-node:ekr.20050826134701.197:p.linkAsNthChild
        #@+node:ekr.20050826134701.198:p.linkAsRoot
        def linkAsRoot (self,oldRoot):
            
            """Link self as the root node."""
            
            # g.trace(self,oldRoot)
        
            p = self ; v = p.v
            if oldRoot: oldRootVnode = oldRoot.v
            else:       oldRootVnode = None
            
            p.stack = [] # Clear the stack.
            
            # Clear all links except the child link.
            v._parent = None
            v._back = None
            v._next = oldRootVnode # Bug fix: 3/12/04
            
            # Add v to it's tnode's vnodeList. Bug fix: 5/02/04.
            if v not in v.t.vnodeList:
                v.t.vnodeList.append(v)
                v.t._p_changed = True # zodb support.
        
            # Link in the rest of the tree only when oldRoot != None.
            # Otherwise, we are calling this routine from init code and
            # we want to start with a pristine tree.
            if oldRoot:
                oldRoot.v._back = v # Bug fix: 3/12/04
        
            p.c.setRootPosition(p)
            
            if 0:
                p.dump(label="root")
        #@-node:ekr.20050826134701.198:p.linkAsRoot
        #@+node:ekr.20050826134701.199:p.unlink
        def unlink (self):
        
            """Unlinks a position p from the tree before moving or deleting.
            
            The p.v._fistChild link does NOT change."""
            
            # Warning: p.parent() is NOT necessarily the same as p.v._parent!
        
            p = self ; v = p.v
            
            # g.trace('p.v._parent',p.v._parent," child:",v.t._firstChild," back:",v._back, " next:",v._next)
            
            # Special case the root.
            if p == p.c.rootPosition():
                assert(p.v._next)
                p.c.setRootPosition(p.next())
            
            # Remove v from it's tnode's vnodeList.
            vnodeList = v.t.vnodeList
            if v in vnodeList:
                vnodeList.remove(v)
                v.t._p_changed = True # zodb support.
            assert(v not in vnodeList)
            
            # Reset the firstChild link in its direct father.
            if p.v._parent:
                assert(p.v and p.v._parent in p.v.directParents())
                if p.v._parent.t._firstChild == v:
                    #g.trace('resetting _parent.v.t._firstChild to',v._next)
                    p.v._parent.t._firstChild = v._next
            else:
                parent = p.parent()
                if parent:
                    assert(parent.v in p.v.directParents())
                    if parent.v.t._firstChild == v:
                        #g.trace('resetting parent().v.t._firstChild to',v._next)
                        parent.v.t._firstChild = v._next
        
            # Do NOT delete the links in any child nodes.
        
            # Clear the links in other nodes.
            if v._back: v._back._next = v._next
            if v._next: v._next._back = v._back
        
            # Unlink _this_ node.
            v._parent = v._next = v._back = None
        
            if 0:
                g.trace('-'*20)
                p.dump(label="p")
                if parent: parent.dump(label="parent")
        #@nonl
        #@-node:ekr.20050826134701.199:p.unlink
        #@-node:ekr.20050826134701.195:p.Link/Unlink methods
        #@-node:ekr.20050826134701.76:class position
        #@-others

    return position
#@nonl
#@-node:ekr.20050826134701.75:buildPositionClass
#@-others
#@nonl
#@-node:ekr.20050825154553:@thin zodb.py
#@-leo
