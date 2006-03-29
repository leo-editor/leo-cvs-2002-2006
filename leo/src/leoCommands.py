#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2810:@thin leoCommands.py
#@@language python
#@@tabwidth -4
#@@pagewidth 80

from __future__ import generators # To make the code work in Python 2.2.

__pychecker__ = '--no-constCond -- no-constant1'
    # Disable checks for constant conditionals.

#@<< imports >>
#@+node:ekr.20040712045933:<< imports  >> (leoCommands)
import leoGlobals as g

if g.app and g.app.use_psyco:
    # print "enabled psyco classes",__file__
    try: from psyco.classes import *
    except ImportError: pass

import leoAtFile
import leoConfig
import leoEditCommands
import leoFileCommands
import leoKeys
import leoImport
import leoNodes
import leoTangle
import leoUndo

import compiler # for Check Python command
import keyword
import os
import parser # needed only for weird Python 2.2 parser errors.
import string

Pmw        = g.importExtension("Pmw",pluginName=None,verbose=False)
subprocess = g.importExtension('subprocess',None,verbose=False)

import sys
import tempfile

import tabnanny # for Check Python command
import tokenize # for Check Python command
import Tkinter as Tk

# The following import _is_ used.
__pychecker__ = '--no-import'
import token    # for Check Python command
#@nonl
#@-node:ekr.20040712045933:<< imports  >> (leoCommands)
#@nl

#@+others
#@+node:ekr.20041118104831:class commands
class baseCommands:
    """The base class for Leo's main commander."""
    #@    @+others
    #@+node:ekr.20031218072017.2811: c.Birth & death
    #@+node:ekr.20031218072017.2812:c.__init__
    def __init__(self,frame,fileName):
    
        c = self
        
        # g.trace('Commands')
        
        c.exists = True # Indicate that this class exists and has not been destroyed.
            # Do this early in the startup process so we can call hooks.
        
        # Init ivars with self.x instead of c.x to keep Pychecker happy
        self.frame = frame
        self.mFileName = fileName
            # Do _not_ use os_path_norm: it converts an empty path to '.' (!!)
    
        # g.trace(c) # Do this after setting c.mFileName.
        c.initIvars()
    
        self.useTextMinibuffer = c.config.getBool('useTextMinibuffer')
        self.showMinibuffer = c.config.getBool('useMinibuffer')
        self.stayInTree = c.config.getBool('stayInTreeAfterSelect')
    
        # initialize the sub-commanders.
        # c.finishCreate creates the sub-commanders for edit commands.
        self.fileCommands   = leoFileCommands.fileCommands(c)
        self.atFileCommands = leoAtFile.atFile(c)
        self.importCommands = leoImport.leoImportCommands(c)
        self.tangleCommands = leoTangle.tangleCommands(c)
        leoEditCommands.createEditCommanders(c)
    
        if 0 and g.debugGC:
            print ; print "*** using Null undoer ***" ; print
            self.undoer = leoUndo.nullUndoer(self)
        else:
            self.undoer = leoUndo.undoer(self)
    #@nonl
    #@-node:ekr.20031218072017.2812:c.__init__
    #@+node:ekr.20040731071037:c.initIvars
    def initIvars(self):
    
        c = self
        #@    << initialize ivars >>
        #@+node:ekr.20031218072017.2813:<< initialize ivars >> (commands)
        self._currentPosition = self.nullPosition()
        self._rootPosition    = self.nullPosition()
        self._topPosition     = self.nullPosition()
        
        # Delayed focus.
        self.hasFocusWidget = None
        self.requestedFocusWidget = None
        
        # Official ivars.
        self.gui = g.app.gui
        
        # Interlocks to prevent premature closing of a window.
        self.inCommand = False
        self.requestCloseWindow = False
        
        # For emacs/vim key handling.
        self.commandsDict = None
        self.keyHandler = self.k = None
        self.miniBufferWidget = None
        
        # per-document info...
        self.disableCommandsMessage = ''
            # The presence of this message disables all commands.
        self.hookFunction = None
        self.openDirectory = None
        
        self.expansionLevel = 0  # The expansion level of this outline.
        self.expansionNode = None # The last node we expanded or contracted.
        self.changed = False # True if any data has been changed since the last save.
        self.loading = False # True if we are loading a file: disables c.setChanged()
        self.outlineToNowebDefaultFileName = "noweb.nw" # For Outline To Noweb dialog.
        self.promptingForClose = False # To lock out additional closing dialogs.
        
        # For tangle/untangle
        self.tangle_errors = 0
        
        # Global options
        self.page_width = 132
        self.tab_width = -4
        self.tangle_batch_flag = False
        self.untangle_batch_flag = False
        # Default Tangle options
        self.tangle_directory = ""
        self.use_header_flag = False
        self.output_doc_flag = False
        # Default Target Language
        self.target_language = "python" # Required if leoConfig.txt does not exist.
        
        # These are defined here, and updated by the tree.select()
        self.beadList = [] # list of vnodes for the Back and Forward commands.
        self.beadPointer = -1 # present item in the list.
        self.visitedList = [] # list of positions for the Nodes dialog.
        
        # For hoist/dehoist commands.
        self.hoistStack = []
            # Stack of nodes to be root of drawn tree.
            # Affects drawing routines and find commands.
        self.recentFiles = [] # List of recent files
        #@nonl
        #@-node:ekr.20031218072017.2813:<< initialize ivars >> (commands)
        #@nl
        self.config = configSettings(c)
        g.app.config.setIvarsFromSettings(c)
    #@nonl
    #@-node:ekr.20040731071037:c.initIvars
    #@+node:ekr.20031218072017.2814:c.__repr__ & __str__
    def __repr__ (self):
        
        return "Commander %d: %s" % (id(self),repr(self.mFileName))
            
    __str__ = __repr__
    
    #@-node:ekr.20031218072017.2814:c.__repr__ & __str__
    #@+node:ekr.20041130173135:c.hash
    def hash (self):
    
        c = self
        if c.mFileName:
            return g.os_path_abspath(c.mFileName).lower()
        else:
            return 0
    #@nonl
    #@-node:ekr.20041130173135:c.hash
    #@+node:ekr.20050920093543:c.finishCreate & helper
    def finishCreate (self):  # New in 4.4.
        
        '''Finish creating the commander after frame.finishCreate.
        
        Important: this is the last step in the startup process.'''
        
        c = self ; p = c.currentPosition()
        c.miniBufferWidget = c.frame.miniBufferWidget
        # g.trace('Commands',c.fileName()) # g.callers())
        
        # Create a keyHandler even if there is no miniBuffer.
        c.keyHandler = c.k = k = leoKeys.keyHandlerClass(c,
            useGlobalKillbuffer=True,
            useGlobalRegisters=True)
    
        if g.app.config and g.app.config.inited:
            # A 'real' .leo file.
            c.commandsDict = leoEditCommands.finishCreateEditCommanders(c)
            k.finishCreate()
        else:
            # A leoSettings.leo file.
            c.commandsDict = {}
    
        # Create the menu last so that we can use the key handler for shortcuts.
        if not g.doHook("menu1",c=c,p=p,v=p):
            c.frame.menu.createMenuBar(c.frame)
            
        c.bodyWantsFocusNow()
    #@nonl
    #@+node:ekr.20051007143620:printCommandsDict
    def printCommandsDict (self):
        
        c = self
        
        print 'Commands...'
        keys = c.commandsDict.keys()
        keys.sort()
        for key in keys:
            command = c.commandsDict.get(key)
            print '%30s = %s' % (key,g.choose(command,command.__name__,'<None>'))
        print
    #@nonl
    #@-node:ekr.20051007143620:printCommandsDict
    #@-node:ekr.20050920093543:c.finishCreate & helper
    #@-node:ekr.20031218072017.2811: c.Birth & death
    #@+node:ekr.20031218072017.2817: doCommand
    command_count = 0
    
    def doCommand (self,command,label,event=None):
    
        """Execute the given command, invoking hooks and catching exceptions.
        
        The code assumes that the "command1" hook has completely handled the command if
        g.doHook("command1") returns False.
        This provides a simple mechanism for overriding commands."""
        
        c = self ; p = c.currentPosition()
        commandName = command and command.__name__
        c.setLog()
    
        self.command_count += 1
        if not g.app.unitTesting and c.config.getBool('trace_doCommand'):
            g.trace(commandName)
    
        # The presence of this message disables all commands.
        if c.disableCommandsMessage:
            g.es(c.disableCommandsMessage,color='blue')
            return 'break' # Inhibit all other handlers.
    
        if label and event is None: # Do this only for legacy commands.
            if label == "cantredo": label = "redo"
            if label == "cantundo": label = "undo"
            g.app.commandName = label
    
        if not g.doHook("command1",c=c,p=p,v=p,label=label):
            try:
                c.inCommand = True
                val = command(event)
                c.inCommand = False
                if c and c.exists: # Be careful: the command could destroy c.
                    c.k.funcReturn = val
            except:
                c.inCommand = False
                if g.app.unitTesting:
                    raise
                else:
                    g.es("exception executing command")
                    print "exception executing command"
                    g.es_exception(c=c)
                    if c and c.exists and hasattr(c,'frame'):
                        c.redraw_now()
                        
            if c and c.exists and c.requestCloseWindow:
                g.trace('Closing window after command')
                c.requestCloseWindow = False
                g.app.closeLeoWindow(c.frame)
    
        # Be careful: the command could destroy c.
        if c and c.exists:
            p = c.currentPosition()
            g.doHook("command2",c=c,p=p,v=p,label=label)
                
        return "break" # Inhibit all other handlers.
    #@nonl
    #@-node:ekr.20031218072017.2817: doCommand
    #@+node:ekr.20031218072017.2582: version & signon stuff
    #@+node:ekr.20040629121554:getBuildNumber
    def getBuildNumber(self):
        c = self
        return c.ver[10:-1] # Strip off "(dollar)Revision" and the trailing "$"
    #@nonl
    #@-node:ekr.20040629121554:getBuildNumber
    #@+node:ekr.20040629121554.1:getSignOnLine (Contains hard-coded version info)
    def getSignOnLine (self):
        c = self
        return "Leo 4.4 a7, build %s, February 28, 2006" % c.getBuildNumber()
    #@nonl
    #@-node:ekr.20040629121554.1:getSignOnLine (Contains hard-coded version info)
    #@+node:ekr.20040629121554.2:initVersion
    def initVersion (self):
        c = self
        c.ver = "$Revision$" # CVS updates this.
    #@nonl
    #@-node:ekr.20040629121554.2:initVersion
    #@+node:ekr.20040629121554.3:c.signOnWithVersion
    def signOnWithVersion (self):
    
        c = self
        color = c.config.getColor("log_error_color")
        signon = c.getSignOnLine()
        n1,n2,n3,junk,junk=sys.version_info
        tkLevel = c.frame.top.getvar("tk_patchLevel")
        
        if sys.platform.startswith('win'):
            version = 'Windows '
            try:
                v = os.sys.getwindowsversion()
                version += ', '.join([str(z) for z in v])
            except Exception:
                pass
                
        else: version = sys.platform
        
        g.es("Leo Log Window...",color=color)
        g.es(signon)
        g.es("Python %d.%d.%d, Tk %s, Pmw %s\n%s" % (n1,n2,n3,tkLevel,Pmw.version(),version))
        g.enl()
    #@nonl
    #@-node:ekr.20040629121554.3:c.signOnWithVersion
    #@-node:ekr.20031218072017.2582: version & signon stuff
    #@+node:ekr.20040312090934:c.iterators
    #@+node:EKR.20040529091232:c.all_positions_iter == allNodes_iter
    def allNodes_iter(self,copy=False):
        
        c = self
        return c.rootPosition().allNodes_iter(copy)
        
    all_positions_iter = allNodes_iter
    #@nonl
    #@-node:EKR.20040529091232:c.all_positions_iter == allNodes_iter
    #@+node:EKR.20040529091232.1:c.all_tnodes_iter
    def all_tnodes_iter(self):
        
        c = self
        for p in c.all_positions_iter():
            yield p.v.t
    
        # return c.rootPosition().all_tnodes_iter(all=True)
    #@nonl
    #@-node:EKR.20040529091232.1:c.all_tnodes_iter
    #@+node:EKR.20040529091232.2:c.all_unique_tnodes_iter
    def all_unique_tnodes_iter(self):
        
        c = self ; marks = {}
        
        for p in c.all_positions_iter():
            if not p.v.t in marks:
                marks[p.v.t] = p.v.t
                yield p.v.t
    #@nonl
    #@-node:EKR.20040529091232.2:c.all_unique_tnodes_iter
    #@+node:EKR.20040529091232.3:c.all_vnodes_iter
    def all_vnodes_iter(self):
        
        c = self
        for p in c.all_positions_iter():
            yield p.v
    #@nonl
    #@-node:EKR.20040529091232.3:c.all_vnodes_iter
    #@+node:EKR.20040529091232.4:c.all_unique_vnodes_iter
    def all_unique_vnodes_iter(self):
        
        c = self ; marks = {}
        for p in c.all_positions_iter():
            if not p.v in marks:
                marks[p.v] = p.v
                yield p.v
    #@nonl
    #@-node:EKR.20040529091232.4:c.all_unique_vnodes_iter
    #@-node:ekr.20040312090934:c.iterators
    #@+node:ekr.20051106040126:c.executeMinibufferCommand
    def executeMinibufferCommand (self,commandName):
        
        c = self ; k = c.k
        
        func = c.commandsDict.get(commandName)
        
        if func:
            event = g.Bunch(char='',keysym=None,widget=c.frame.body.bodyCtrl)
            stroke = None
            k.masterCommand(event,func,stroke)
            return k.funcReturn
        else:
            g.trace('no such command: %s' % (commandName),color='red')
            return None
    #@nonl
    #@-node:ekr.20051106040126:c.executeMinibufferCommand
    #@+node:ekr.20031218072017.2818:Command handlers...
    #@+node:ekr.20031218072017.2819:File Menu
    #@+node:ekr.20031218072017.2820:top level
    #@+node:ekr.20031218072017.1623:new
    def new (self,event=None):
    
        c,frame = g.app.newLeoCommanderAndFrame(fileName=None)
        
        # Needed for plugins.
        g.doHook("new",old_c=self,c=c,new_c=c)
        # Use the config params to set the size and location of the window.
        c.beginUpdate()
        try:
            frame.setInitialWindowGeometry()
            frame.deiconify()
            frame.lift()
            frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio) # Resize the _new_ frame.
            t = leoNodes.tnode()
            v = leoNodes.vnode(c,t)
            p = leoNodes.position(c,v,[])
            v.initHeadString("NewHeadline")
            v.moveToRoot()
            c.editPosition(p)
        finally:
            c.endUpdate()
            frame.body.setFocus()
        return c # For unit test.
    #@nonl
    #@-node:ekr.20031218072017.1623:new
    #@+node:ekr.20031218072017.2821:open
    def open (self,event=None):
    
        c = self
        #@    << Set closeFlag if the only open window is empty >>
        #@+node:ekr.20031218072017.2822:<< Set closeFlag if the only open window is empty >>
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
        #@-node:ekr.20031218072017.2822:<< Set closeFlag if the only open window is empty >>
        #@nl
    
        fileName = g.app.gui.runOpenFileDialog(
            title = "Open",
            filetypes = [("Leo files","*.leo"), ("All files","*")],
            defaultextension = ".leo")
    
        if fileName and len(fileName) > 0:
            ok, frame = g.openWithFileName(fileName,c)
            if ok:
                g.setGlobalOpenDir(fileName)
            if ok and closeFlag:
                g.app.destroyWindow(c.frame)
        else:
            c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20031218072017.2821:open
    #@+node:ekr.20031218072017.2823:openWith and allies
    def openWith(self,event=None,data=None):
    
        """This routine handles the items in the Open With... menu.
    
        These items can only be created by createOpenWithMenuFromTable().
        Typically this would be done from the "open2" hook.
        
        New in 4.3: The "os.spawnv" now works. You may specify arguments to spawnv
        using a list, e.g.:
            
        openWith("os.spawnv", ["c:/prog.exe","--parm1","frog","--switch2"], None)
        """
        
        c = self ; p = c.currentPosition()
        n = data and len(data) or 0
        if n != 3:
            g.trace('bad data, length must be 3, got %d' % n)
            return
        try:
            openType,arg,ext=data
            if not g.doHook("openwith1",c=c,p=p,v=p.v,openType=openType,arg=arg,ext=ext):
                enableIdleTimeHook(idleTimeDelay=100)
                #@            << set ext based on the present language >>
                #@+node:ekr.20031218072017.2824:<< set ext based on the present language >>
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
                #@-node:ekr.20031218072017.2824:<< set ext based on the present language >>
                #@nl
                #@            << create or reopen temp file, testing for conflicting changes >>
                #@+node:ekr.20031218072017.2825:<< create or reopen temp file, testing for conflicting changes >>
                theDict = None ; path = None
                #@<< set dict and path if a temp file already refers to p.v.t >>
                #@+node:ekr.20031218072017.2826:<<set dict and path if a temp file already refers to p.v.t >>
                searchPath = c.openWithTempFilePath(p,ext)
                
                if g.os_path_exists(searchPath):
                    for theDict in g.app.openWithFiles:
                        if p.v == theDict.get('v') and searchPath == theDict.get("path"):
                            path = searchPath
                            break
                #@-node:ekr.20031218072017.2826:<<set dict and path if a temp file already refers to p.v.t >>
                #@nl
                if path:
                    #@    << create or recreate temp file as needed >>
                    #@+node:ekr.20031218072017.2827:<< create or recreate temp file as needed >>
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
                        #@+node:ekr.20031218072017.2828:<< Raise dialog about conflict and set result >>
                        message = (
                            "Conflicting changes in outline and temp file\n\n" +
                            "Do you want to use the code in the outline or the temp file?\n\n")
                        
                        result = g.app.gui.runAskYesNoCancelDialog(c,
                            "Conflict!", message,
                            yesMessage = "Outline",
                            noMessage = "File",
                            defaultButton = "Cancel")
                        #@nonl
                        #@-node:ekr.20031218072017.2828:<< Raise dialog about conflict and set result >>
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
                    #@-node:ekr.20031218072017.2827:<< create or recreate temp file as needed >>
                    #@nl
                else:
                    path = c.createOpenWithTempFile(p,ext)
                
                if not path:
                    return # An error has occured.
                #@nonl
                #@-node:ekr.20031218072017.2825:<< create or reopen temp file, testing for conflicting changes >>
                #@nl
                #@            << execute a command to open path in external editor >>
                #@+node:ekr.20031218072017.2829:<< execute a command to open path in external editor >>
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
                        vtuple.insert(0, filename)
                            # add the name of the program as the first argument.
                            # Change suggested by Jim Sizelove.
                        vtuple.append(path)
                        command = "os.spawnv(%s,%s)" % (arg[0],repr(vtuple))
                        apply(os.spawnv,(os.P_NOWAIT,arg[0],vtuple))
                    # This clause by Jim Sizelove.
                    elif openType == "subprocess.Popen":
                        if isinstance(arg, basestring):
                            vtuple = arg + " " + path
                        elif isinstance(arg, (list, tuple)):
                            vtuple = arg[:]
                            vtuple.append(path)
                        command = "subprocess.Popen(%s)" % repr(vtuple)
                        if subprocess:
                            subprocess.Popen(vtuple)
                        else:
                            g.grace('Can not import subprocess.  Skipping: "%s"' % command)
                    else:
                        command="bad command:"+str(openType)
                        g.trace(command)
                except Exception:
                    g.es("exception executing: "+command)
                    g.es_exception()
                #@nonl
                #@-node:ekr.20031218072017.2829:<< execute a command to open path in external editor >>
                #@nl
            g.doHook("openwith2",c=c,p=p,v=p.v,openType=openType,arg=arg,ext=ext)
        except Exception:
            g.es("unexpected exception in c.openWith")
            g.es_exception()
    
        return "break"
    #@+node:ekr.20031218072017.2830:createOpenWithTempFile
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
            #@+node:ekr.20031218072017.2831:<< remove previous entry from app.openWithFiles if it exists >>
            for d in g.app.openWithFiles[:]:
                p2 = d.get("p")
                if p.v.t == p2.v.t:
                    # print "removing previous entry in g.app.openWithFiles for",p.headString()
                    g.app.openWithFiles.remove(d)
            #@nonl
            #@-node:ekr.20031218072017.2831:<< remove previous entry from app.openWithFiles if it exists >>
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
    #@-node:ekr.20031218072017.2830:createOpenWithTempFile
    #@+node:ekr.20031218072017.2832:c.openWithTempFilePath
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
    #@-node:ekr.20031218072017.2832:c.openWithTempFilePath
    #@-node:ekr.20031218072017.2823:openWith and allies
    #@+node:ekr.20031218072017.2833:close
    def close (self,event=None):
        
        """Handle the File-Close command."""
    
        g.app.closeLeoWindow(self.frame)
    #@nonl
    #@-node:ekr.20031218072017.2833:close
    #@+node:ekr.20031218072017.2834:save
    def save (self,event=None):
    
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
        else:
            fileName = g.app.gui.runSaveFileDialog(
                initialfile = c.mFileName,
                title="Save",
                filetypes=[("Leo files", "*.leo")],
                defaultextension=".leo")
            if fileName:
                # Don't change mFileName until the dialog has suceeded.
                c.mFileName = g.ensure_extension(fileName, ".leo")
                c.frame.title = c.mFileName
                c.frame.setTitle(g.computeWindowTitle(c.mFileName))
                c.frame.openDirectory = g.os_path_dirname(c.mFileName) # Bug fix in 4.4b2.
                c.fileCommands.save(c.mFileName)
                c.updateRecentFiles(c.mFileName)
    #@nonl
    #@-node:ekr.20031218072017.2834:save
    #@+node:ekr.20031218072017.2835:saveAs
    def saveAs (self,event=None):
        
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
            c.frame.openDirectory = g.os_path_dirname(c.mFileName) # Bug fix in 4.4b2.
            # Calls c.setChanged(False) if no error.
            c.fileCommands.saveAs(c.mFileName)
            c.updateRecentFiles(c.mFileName)
    #@nonl
    #@-node:ekr.20031218072017.2835:saveAs
    #@+node:ekr.20031218072017.2836:saveTo
    def saveTo (self,event=None):
        
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
    #@-node:ekr.20031218072017.2836:saveTo
    #@+node:ekr.20031218072017.2837:revert
    def revert (self,event=None):
        
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
    #@-node:ekr.20031218072017.2837:revert
    #@-node:ekr.20031218072017.2820:top level
    #@+node:ekr.20031218072017.2079:Recent Files submenu & allies
    #@+node:ekr.20031218072017.2080:clearRecentFiles
    def clearRecentFiles (self,event=None):
        
        """Clear the recent files list, then add the present file."""
    
        c = self ; f = c.frame ; u = c.undoer
        
        bunch = u.beforeClearRecentFiles()
        
        recentFilesMenu = f.menu.getMenu("Recent Files...")
        f.menu.delete_range(recentFilesMenu,0,len(c.recentFiles))
        
        c.recentFiles = []
        g.app.config.recentFiles = [] # New in Leo 4.3.
        f.menu.createRecentFilesMenuItems()
        c.updateRecentFiles(c.fileName())
        
        g.app.config.appendToRecentFiles(c.recentFiles)
        
        u.afterClearRecentFiles(bunch)
    #@nonl
    #@-node:ekr.20031218072017.2080:clearRecentFiles
    #@+node:ekr.20031218072017.2081:openRecentFile
    def openRecentFile(self,name=None):
        
        if not name: return
    
        c = self ; v = c.currentVnode()
        #@    << Set closeFlag if the only open window is empty >>
        #@+node:ekr.20031218072017.2082:<< Set closeFlag if the only open window is empty >>
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
        #@-node:ekr.20031218072017.2082:<< Set closeFlag if the only open window is empty >>
        #@nl
        
        fileName = name
        if not g.doHook("recentfiles1",c=c,p=v,v=v,fileName=fileName,closeFlag=closeFlag):
            ok, frame = g.openWithFileName(fileName,c)
            if ok and closeFlag:
                g.app.destroyWindow(c.frame) # 12/12/03
                c = frame.c # Switch to the new commander so the "recentfiles2" hook doesn't crash.
                c.setLog() # Sets the log stream for g.es()
    
        g.doHook("recentfiles2",c=c,p=v,v=v,fileName=fileName,closeFlag=closeFlag)
    #@-node:ekr.20031218072017.2081:openRecentFile
    #@+node:ekr.20031218072017.2083:c.updateRecentFiles
    def updateRecentFiles (self,fileName):
        
        """Create the RecentFiles menu.  May be called with Null fileName."""
        
        if g.app.unitTesting: return
        
        def munge(name):
            name = name or ''
            return g.os_path_normpath(name).lower()
    
        # Update the recent files list in all windows.
        if fileName:
            compareFileName = munge(fileName)
            # g.trace(fileName)
            for frame in g.app.windowList:
                c = frame.c
                # Remove all versions of the file name.
                for name in c.recentFiles:
                    if compareFileName == munge(name):
                        c.recentFiles.remove(name)
                c.recentFiles.insert(0,fileName)
                # g.trace(fileName)
                # Recreate the Recent Files menu.
                frame.menu.createRecentFilesMenuItems()
        else:
            for frame in g.app.windowList:
                frame.menu.createRecentFilesMenuItems()
    #@nonl
    #@-node:ekr.20031218072017.2083:c.updateRecentFiles
    #@-node:ekr.20031218072017.2079:Recent Files submenu & allies
    #@+node:ekr.20031218072017.2838:Read/Write submenu
    #@+node:ekr.20031218072017.2839:readOutlineOnly
    def readOutlineOnly (self,event=None):
    
        fileName = g.app.gui.runOpenFileDialog(
            title="Read Outline Only",
            filetypes=[("Leo files", "*.leo"), ("All files", "*")],
            defaultextension=".leo")
    
        if not fileName:
            return
    
        try:
            theFile = open(fileName,'r')
            c,frame = g.app.newLeoCommanderAndFrame(fileName)
            frame.deiconify()
            frame.lift()
            g.app.root.update() # Force a screen redraw immediately.
            c.fileCommands.readOutlineOnly(theFile,fileName) # closes file.
        except:
            g.es("can not open:" + fileName)
    #@nonl
    #@-node:ekr.20031218072017.2839:readOutlineOnly
    #@+node:ekr.20031218072017.1839:readAtFileNodes (commands)
    def readAtFileNodes (self,event=None):
    
        c = self ; u = c.undoer ; p = c.currentPosition()
    
        c.beginUpdate()
        try:
            undoData = u.beforeChangeTree(p)
            c.fileCommands.readAtFileNodes()
            u.afterChangeTree(p,'Read @file Nodes',undoData)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.1839:readAtFileNodes (commands)
    #@+node:ekr.20031218072017.1809:importDerivedFile
    def importDerivedFile (self,event=None):
        
        """Create a new outline from a 4.0 derived file."""
        
        c = self ; p = c.currentPosition()
        
        types = [
            ("All files","*"),
            ("C/C++ files","*.c"),
            ("C/C++ files","*.cpp"),
            ("C/C++ files","*.h"),
            ("C/C++ files","*.hpp"),
            ("Java files","*.java"),
            ("Lua files", "*.lua"),
            ("Pascal files","*.pas"),
            ("Python files","*.py") ]
        
        names = g.app.gui.runOpenFileDialog(
            title="Import Derived File",
            filetypes=types,
            defaultextension=".py",
            multiple=True)
    
        if names:
            c.importCommands.importDerivedFiles(parent=p,paths=names)
    #@nonl
    #@-node:ekr.20031218072017.1809:importDerivedFile
    #@-node:ekr.20031218072017.2838:Read/Write submenu
    #@+node:ekr.20031218072017.2841:Tangle submenu
    #@+node:ekr.20031218072017.2842:tangleAll
    def tangleAll (self,event=None):
        
        c = self
        c.tangleCommands.tangleAll()
    #@-node:ekr.20031218072017.2842:tangleAll
    #@+node:ekr.20031218072017.2843:tangleMarked
    def tangleMarked (self,event=None):
    
        c = self
        c.tangleCommands.tangleMarked()
    #@-node:ekr.20031218072017.2843:tangleMarked
    #@+node:ekr.20031218072017.2844:tangle
    def tangle (self,event=None):
    
        c = self
        c.tangleCommands.tangle()
    #@nonl
    #@-node:ekr.20031218072017.2844:tangle
    #@-node:ekr.20031218072017.2841:Tangle submenu
    #@+node:ekr.20031218072017.2845:Untangle submenu
    #@+node:ekr.20031218072017.2846:untangleAll
    def untangleAll (self,event=None):
    
        c = self
        c.tangleCommands.untangleAll()
        c.undoer.clearUndoState()
    #@-node:ekr.20031218072017.2846:untangleAll
    #@+node:ekr.20031218072017.2847:untangleMarked
    def untangleMarked (self,event=None):
    
        c = self
        c.tangleCommands.untangleMarked()
        c.undoer.clearUndoState()
    #@-node:ekr.20031218072017.2847:untangleMarked
    #@+node:ekr.20031218072017.2848:untangle
    def untangle (self,event=None):
    
        c = self
        c.tangleCommands.untangle()
        c.undoer.clearUndoState()
    #@-node:ekr.20031218072017.2848:untangle
    #@-node:ekr.20031218072017.2845:Untangle submenu
    #@+node:ekr.20031218072017.2849:Import&Export submenu
    #@+node:ekr.20031218072017.2850:exportHeadlines
    def exportHeadlines (self,event=None):
        
        c = self
    
        filetypes = [("Text files", "*.txt"),("All files", "*")]
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile="headlines.txt",
            title="Export Headlines",
            filetypes=filetypes,
            defaultextension=".txt")
    
        if fileName and len(fileName) > 0:
            g.setGlobalOpenDir(fileName)
            c.importCommands.exportHeadlines(fileName)
    
    #@-node:ekr.20031218072017.2850:exportHeadlines
    #@+node:ekr.20031218072017.2851:flattenOutline
    def flattenOutline (self,event=None):
        
        c = self
    
        filetypes = [("Text files", "*.txt"),("All files", "*")]
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile="flat.txt",
            title="Flatten Outline",
            filetypes=filetypes,
            defaultextension=".txt")
    
        if fileName and len(fileName) > 0:
            g.setGlobalOpenDir(fileName)
            c.importCommands.flattenOutline(fileName)
    
    #@-node:ekr.20031218072017.2851:flattenOutline
    #@+node:ekr.20031218072017.2852:importAtRoot
    def importAtRoot (self,event=None):
        
        c = self
        
        types = [
            ("All files","*"),
            ("C/C++ files","*.c"),
            ("C/C++ files","*.cpp"),
            ("C/C++ files","*.h"),
            ("C/C++ files","*.hpp"),
            ("Java files","*.java"),
            ("Lua files", "*.lua"),
            ("Pascal files","*.pas"),
            ("Python files","*.py") ]
    
        names = g.app.gui.runOpenFileDialog(
            title="Import To @root",
            filetypes=types,
            defaultextension=".py",
            multiple=True)
    
        if names:
            c.importCommands.importFilesCommand (names,"@root")
    #@-node:ekr.20031218072017.2852:importAtRoot
    #@+node:ekr.20031218072017.2853:importAtFile
    def importAtFile (self,event=None):
        
        c = self
    
        types = [
            ("All files","*"),
            ("C/C++ files","*.c"),
            ("C/C++ files","*.cpp"),
            ("C/C++ files","*.h"),
            ("C/C++ files","*.hpp"),
            ("Java files","*.java"),
            ("Lua files", "*.lua"),
            ("Pascal files","*.pas"),
            ("Python files","*.py") ]
    
        names = g.app.gui.runOpenFileDialog(
            title="Import To @file",
            filetypes=types,
            defaultextension=".py",
            multiple=True)
    
        if names:
            c.importCommands.importFilesCommand(names,"@file")
    #@nonl
    #@-node:ekr.20031218072017.2853:importAtFile
    #@+node:ekr.20031218072017.2854:importCWEBFiles
    def importCWEBFiles (self,event=None):
        
        c = self
        
        filetypes = [
            ("CWEB files", "*.w"),
            ("Text files", "*.txt"),
            ("All files", "*")]
    
        names = g.app.gui.runOpenFileDialog(
            title="Import CWEB Files",
            filetypes=filetypes,
            defaultextension=".w",
            multiple=True)
    
        if names:
            c.importCommands.importWebCommand(names,"cweb")
    #@-node:ekr.20031218072017.2854:importCWEBFiles
    #@+node:ekr.20031218072017.2855:importFlattenedOutline
    def importFlattenedOutline (self,event=None):
        
        c = self
        
        types = [("Text files","*.txt"), ("All files","*")]
    
        names = g.app.gui.runOpenFileDialog(
            title="Import MORE Text",
            filetypes=types,
            defaultextension=".py",
            multiple=True)
    
        if names:
            c.importCommands.importFlattenedOutline(names)
    #@-node:ekr.20031218072017.2855:importFlattenedOutline
    #@+node:ekr.20031218072017.2856:importNowebFiles
    def importNowebFiles (self,event=None):
        
        c = self
    
        filetypes = [
            ("Noweb files", "*.nw"),
            ("Text files", "*.txt"),
            ("All files", "*")]
    
        names = g.app.gui.runOpenFileDialog(
            title="Import Noweb Files",
            filetypes=filetypes,
            defaultextension=".nw",
            multiple=True)
    
        if names:
            c.importCommands.importWebCommand(names,"noweb")
    #@-node:ekr.20031218072017.2856:importNowebFiles
    #@+node:ekr.20031218072017.2857:outlineToCWEB
    def outlineToCWEB (self,event=None):
        
        c = self
    
        filetypes=[
            ("CWEB files", "*.w"),
            ("Text files", "*.txt"),
            ("All files", "*")]
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile="cweb.w",
            title="Outline To CWEB",
            filetypes=filetypes,
            defaultextension=".w")
    
        if fileName and len(fileName) > 0:
            g.setGlobalOpenDir(fileName)
            c.importCommands.outlineToWeb(fileName,"cweb")
    
    #@-node:ekr.20031218072017.2857:outlineToCWEB
    #@+node:ekr.20031218072017.2858:outlineToNoweb
    def outlineToNoweb (self,event=None):
        
        c = self
        
        filetypes=[
            ("Noweb files", "*.nw"),
            ("Text files", "*.txt"),
            ("All files", "*")]
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile=self.outlineToNowebDefaultFileName,
            title="Outline To Noweb",
            filetypes=filetypes,
            defaultextension=".nw")
    
        if fileName and len(fileName) > 0:
            g.setGlobalOpenDir(fileName)
            c.importCommands.outlineToWeb(fileName,"noweb")
            c.outlineToNowebDefaultFileName = fileName
    
    #@-node:ekr.20031218072017.2858:outlineToNoweb
    #@+node:ekr.20031218072017.2859:removeSentinels
    def removeSentinels (self,event=None):
        
        c = self
        
        types = [
            ("All files","*"),
            ("C/C++ files","*.c"),
            ("C/C++ files","*.cpp"),
            ("C/C++ files","*.h"),
            ("C/C++ files","*.hpp"),
            ("Java files","*.java"),
            ("Lua files", "*.lua"),
            ("Pascal files","*.pas"),
            ("Python files","*.py") ]
    
        names = g.app.gui.runOpenFileDialog(
            title="Remove Sentinels",
            filetypes=types,
            defaultextension=".py",
            multiple=True)
    
        if names:
            c.importCommands.removeSentinelsCommand (names)
    #@nonl
    #@-node:ekr.20031218072017.2859:removeSentinels
    #@+node:ekr.20031218072017.2860:weave
    def weave (self,event=None):
        
        c = self
    
        filetypes = [("Text files", "*.txt"),("All files", "*")]
    
        fileName = g.app.gui.runSaveFileDialog(
            initialfile="weave.txt",
            title="Weave",
            filetypes=filetypes,
            defaultextension=".txt")
    
        if fileName and len(fileName) > 0:
            g.setGlobalOpenDir(fileName)
            c.importCommands.weave(fileName)
    #@-node:ekr.20031218072017.2860:weave
    #@-node:ekr.20031218072017.2849:Import&Export submenu
    #@-node:ekr.20031218072017.2819:File Menu
    #@+node:ekr.20031218072017.2861:Edit Menu...
    #@+node:ekr.20031218072017.2862:Edit top level
    #@+node:ekr.20031218072017.2140:c.executeScript
    def executeScript(self,event=None,p=None,script=None,
        useSelectedText=True,define_g=True,define_name='__main__',silent=False):
    
        """This executes body text as a Python script.
        
        We execute the selected text, or the entire body text if no text is selected."""
        
        c = self ; script1 = script
        if not script:
            script = g.getScript(c,p,useSelectedText=useSelectedText)
        #@    << redirect output >>
        #@+node:ekr.20031218072017.2143:<< redirect output >>
        if c.config.redirect_execute_script_output_to_log_pane:
        
            g.redirectStdout() # Redirect stdout
            g.redirectStderr() # Redirect stderr
        #@nonl
        #@-node:ekr.20031218072017.2143:<< redirect output >>
        #@nl
        try:
            if script.strip():
                sys.path.insert(0,c.frame.openDirectory)
                script += '\n' # Make sure we end the script properly.
                try:
                    p = c.currentPosition()
                    d = g.choose(define_g,{'c':c,'g':g,'p':p},{})
                    if define_name: d['__name__'] = define_name
                    # g.trace(script)
                    exec script in d
                    if not script1 and not silent:
                        g.es("end of script",color="purple")
                except Exception:
                    #@                << handle an exception in the script >>
                    #@+node:ekr.20050505104140:<< handle an exception in the script >>
                    g.es("exception executing script",color='blue')
                    
                    if 0:
                        print 'script...'
                        for line in g.splitLines(script):
                            print repr(line)
                    
                    fileName,n = g.es_exception(full=True,c=c)
                    if p and not script1 and fileName == "<string>":
                        c.goToScriptLineNumber(p,script,n)
                    
                    #@<< dump the lines near the error >>
                    #@+node:EKR.20040612215018:<< dump the lines near the error >>
                    if g.os_path_exists(fileName):
                        f = file(fileName)
                        lines = f.readlines()
                        f.close()
                    else:
                        lines = g.splitLines(script)
                    
                    s = '-' * 20
                    g.es_print(s)
                    
                    if 0:
                        # Just print the error line.
                        try:
                            s = "%s line %d: %s" % (fileName,n,lines[n-1])
                            g.es(s,newline=False)
                        except IndexError:
                            s = "%s line %d" % (fileName,n)
                            g.es(s,newline=False)
                    else: # Print surrounding lines.
                        i = max(0,n-2)
                        j = min(n+2,len(lines))
                        # g.trace(n,i,j)
                        while i < j:
                            ch = g.choose(i==n-1,'*',' ')
                            s = "%s line %d: %s" % (ch,i+1,lines[i])
                            g.es(s,newline=False)
                            i += 1
                    #@nonl
                    #@-node:EKR.20040612215018:<< dump the lines near the error >>
                    #@nl
                    #@nonl
                    #@-node:ekr.20050505104140:<< handle an exception in the script >>
                    #@nl
                del sys.path[0]
            else:
                g.es("no script selected",color="blue")
        finally: # New in 4.3 beta 2: unredirect output last.
            #@        << unredirect output >>
            #@+node:EKR.20040627100424:<< unredirect output >>
            if c.exists and c.config.redirect_execute_script_output_to_log_pane:
            
                g.restoreStderr()
                g.restoreStdout()
            #@nonl
            #@-node:EKR.20040627100424:<< unredirect output >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.2140:c.executeScript
    #@+node:ekr.20031218072017.2864:goToLineNumber & allies
    def goToLineNumber (self,event=None,root=None,lines=None,n=None,scriptFind=False):
        
        __pychecker__ = 'maxlines=400'
    
        c = self ; p = c.currentPosition()
        root1 = root
        if root is None:
            #@        << set root >>
            #@+node:ekr.20031218072017.2865:<< set root >>
            # First look for ancestor @file node.
            fileName = None
            for p in p.self_and_parents_iter():
                fileName = p.anyAtFileNodeName()
                if fileName: break
            
            # New in 4.2: Search the entire tree for joined nodes.
            if not fileName:
                p1 = c.currentPosition()
                for p in c.all_positions_iter():
                    if p.v.t == p1.v.t and p != p1:
                        # Found a joined position.
                        for p in p.self_and_parents_iter():
                            fileName = p.anyAtFileNodeName()
                            # New in 4.2 b3: ignore @all nodes.
                            if fileName and not p.isAtAllNode(): break
                    if fileName: break
            
            if fileName:
                root = p.copy()
            else:
                # New in 4.2.1: assume the c.currentPosition is the root of a script.
                root = c.currentPosition()
                g.es("No ancestor @file node: using script line numbers", color="blue")
                scriptFind = True
                lines = g.getScript (c,root,useSelectedText=False)
                lines = g.splitLines(lines)
                if 0:
                    for line in lines:
                        print line,
            #@nonl
            #@-node:ekr.20031218072017.2865:<< set root >>
            #@nl
        if lines is None:
            #@        << read the file into lines >>
            #@+node:ekr.20031218072017.2866:<< read the file into lines >>
            # 1/26/03: calculate the full path.
            d = g.scanDirectives(c)
            path = d.get("path")
            
            fileName = g.os_path_join(path,fileName)
            
            try:
                lines=self.gotoLineNumberOpen(fileName) # bwm
            except:
                g.es("not found: " + fileName)
                return
            #@nonl
            #@-node:ekr.20031218072017.2866:<< read the file into lines >>
            #@nl
        if n is None:
            #@        << get n, the line number, from a dialog >>
            #@+node:ekr.20031218072017.2867:<< get n, the line number, from a dialog >>
            n = g.app.gui.runAskOkCancelNumberDialog(c,"Enter Line Number","Line number:")
            if n == -1:
                return
            #@nonl
            #@-node:ekr.20031218072017.2867:<< get n, the line number, from a dialog >>
            #@nl
            n = self.applyLineNumberMappingIfAny(n) #bwm
        if n==1:
            p = root ; n2 = 1 ; found = True
        elif n >= len(lines):
            p = root ; found = False
            n2 = p.bodyString().count('\n')
        elif root.isAtAsisFileNode():
            #@        << count outline lines, setting p,n2,found >>
            #@+node:ekr.20031218072017.2868:<< count outline lines, setting p,n2,found >> (@file-nosent only)
            p = lastv = root
            prev = 0 ; found = False
            
            for p in p.self_and_subtree_iter():
                lastv = p.copy()
                s = p.bodyString()
                lines = s.count('\n')
                if len(s) > 0 and s[-1] != '\n':
                    lines += 1
                # print lines,prev,p
                if prev + lines >= n:
                    found = True ; break
                prev += lines
            
            p = lastv
            n2 = max(1,n-prev)
            #@nonl
            #@-node:ekr.20031218072017.2868:<< count outline lines, setting p,n2,found >> (@file-nosent only)
            #@nl
        else:
            vnodeName,childIndex,gnx,n2,delim = self.convertLineToVnodeNameIndexLine(lines,n,root,scriptFind)
            found = True
            if not vnodeName:
                g.es("error handling: " + root.headString())
                return
            #@        << set p to the node given by vnodeName, etc. >>
            #@+node:ekr.20031218072017.2869:<< set p to the node given by vnodeName, etc. >>
            if scriptFind:
                #@    << just scan for the node name >>
                #@+node:ekr.20041111093404:<< just scan for the node name >>
                # This is safe enough because clones are not much of an issue.
                found = False
                for p in root.self_and_subtree_iter():
                    if p.matchHeadline(vnodeName):
                        found = True ; break
                #@nonl
                #@-node:ekr.20041111093404:<< just scan for the node name >>
                #@nl
            elif gnx:
                #@    << 4.2: get node from gnx >>
                #@+node:EKR.20040609110138:<< 4.2: get node from gnx >>
                found = False
                gnx = g.app.nodeIndices.scanGnx(gnx,0)
                
                # g.trace(vnodeName)
                # g.trace(gnx)
                
                for p in root.self_and_subtree_iter():
                    if p.matchHeadline(vnodeName):
                        # g.trace(p.v.t.fileIndex)
                        if p.v.t.fileIndex == gnx:
                            found = True ; break
                
                if not found:
                    g.es("not found: " + vnodeName, color="red")
                    return
                #@nonl
                #@-node:EKR.20040609110138:<< 4.2: get node from gnx >>
                #@nl
            elif childIndex == -1:
                #@    << 4.x: scan for the node using tnodeList and n >>
                #@+node:ekr.20031218072017.2870:<< 4.x: scan for the node using tnodeList and n >>
                # This is about the best that can be done without replicating the entire atFile write logic.
                
                ok = True
                
                if not hasattr(root.v.t,"tnodeList"):
                    s = "no child index for " + root.headString()
                    g.es_print(s, color="red")
                    ok = False
                
                if ok:
                    tnodeList = root.v.t.tnodeList
                    #@    << set tnodeIndex to the number of +node sentinels before line n >>
                    #@+node:ekr.20031218072017.2871:<< set tnodeIndex to the number of +node sentinels before line n >>
                    tnodeIndex = -1 # Don't count the @file node.
                    scanned = 0 # count of lines scanned.
                    
                    for s in lines:
                        if scanned >= n:
                            break
                        i = g.skip_ws(s,0)
                        if g.match(s,i,delim):
                            i += len(delim)
                            if g.match(s,i,"+node"):
                                # g.trace(tnodeIndex,s.rstrip())
                                tnodeIndex += 1
                        scanned += 1
                    #@nonl
                    #@-node:ekr.20031218072017.2871:<< set tnodeIndex to the number of +node sentinels before line n >>
                    #@nl
                    tnodeIndex = max(0,tnodeIndex)
                    #@    << set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = False >>
                    #@+node:ekr.20031218072017.2872:<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
                    #@+at 
                    #@nonl
                    # We use the tnodeList to find a _tnode_ corresponding to 
                    # the proper node, so the user will for sure be editing 
                    # the proper text, even if several nodes happen to have 
                    # the same headline.  This is really all that we need.
                    # 
                    # However, this code has no good way of distinguishing 
                    # between different cloned vnodes in the file: they all 
                    # have the same tnode.  So this code just picks p = 
                    # t.vnodeList[0] and leaves it at that.
                    # 
                    # The only way to do better is to scan the outline, 
                    # replicating the write logic to determine which vnode 
                    # created the given line.  That's way too difficult, and 
                    # it would create an unwanted dependency in this code.
                    #@-at
                    #@@c
                    
                    # g.trace("tnodeIndex",tnodeIndex)
                    if tnodeIndex < len(tnodeList):
                        t = tnodeList[tnodeIndex]
                        # Find the first vnode whose tnode is t.
                        found = False
                        for p in root.self_and_subtree_iter():
                            if p.v.t == t:
                                found = True ; break
                        if not found:
                            s = "tnode not found for " + vnodeName
                            g.es_print(s, color="red") ; ok = False
                        elif p.headString().strip() != vnodeName:
                            if 0: # Apparently this error doesn't prevent a later scan for working properly.
                                s = "Mismatched vnodeName\nExpecting: %s\n got: %s" % (p.headString(),vnodeName)
                                g.es_print(s, color="red")
                            ok = False
                    else:
                        if root1 is None: # Kludge: disable this message when called by goToScriptLineNumber.
                            s = "Invalid computed tnodeIndex: %d" % tnodeIndex
                            g.es_print(s, color = "red")
                        ok = False
                    #@nonl
                    #@-node:ekr.20031218072017.2872:<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
                    #@nl
                            
                if not ok:
                    # Fall back to the old logic.
                    #@    << set p to the first node whose headline matches vnodeName >>
                    #@+node:ekr.20031218072017.2873:<< set p to the first node whose headline matches vnodeName >>
                    found = False
                    for p in root.self_and_subtree_iter():
                        if p.matchHeadline(vnodeName):
                            found = True ; break
                    
                    if not found:
                        s = "not found: " + vnodeName
                        g.es_print(s, color="red")
                        return
                    #@nonl
                    #@-node:ekr.20031218072017.2873:<< set p to the first node whose headline matches vnodeName >>
                    #@nl
                #@nonl
                #@-node:ekr.20031218072017.2870:<< 4.x: scan for the node using tnodeList and n >>
                #@nl
            else:
                #@    << 3.x: scan for the node with the given childIndex >>
                #@+node:ekr.20031218072017.2874:<< 3.x: scan for the node with the given childIndex >>
                found = False
                for p in root.self_and_subtree_iter():
                    if p.matchHeadline(vnodeName):
                        if childIndex <= 0 or p.childIndex() + 1 == childIndex:
                            found = True ; break
                
                if not found:
                    g.es("not found: " + vnodeName, color="red")
                    return
                #@nonl
                #@-node:ekr.20031218072017.2874:<< 3.x: scan for the node with the given childIndex >>
                #@nl
            #@nonl
            #@-node:ekr.20031218072017.2869:<< set p to the node given by vnodeName, etc. >>
            #@nl
        #@    << select p and make it visible >>
        #@+node:ekr.20031218072017.2875:<< select p and make it visible >>
        c.beginUpdate()
        try:
            c.frame.tree.expandAllAncestors(p)
            c.selectVnode(p)
        finally:
            c.endUpdate()
        #@nonl
        #@-node:ekr.20031218072017.2875:<< select p and make it visible >>
        #@nl
        #@    << put the cursor on line n2 of the body text >>
        #@+node:ekr.20031218072017.2876:<< put the cursor on line n2 of the body text >>
        if found:
            c.frame.body.setInsertPointToStartOfLine(n2-1)
        else:
            c.frame.body.setInsertionPointToEnd()
            g.es("%d lines" % len(lines), color="blue")
        
        c.bodyWantsFocus()
        c.frame.body.makeInsertPointVisible()
        #@nonl
        #@-node:ekr.20031218072017.2876:<< put the cursor on line n2 of the body text >>
        #@nl
    #@nonl
    #@+node:ekr.20031218072017.2877:convertLineToVnodeNameIndexLine
    #@+at 
    #@nonl
    # We count "real" lines in the derived files, ignoring all sentinels that 
    # do not arise from source lines.  When the indicated line is found, we 
    # scan backwards for an @+body line, get the vnode's name from that line 
    # and set p to the indicated vnode.  This will fail if vnode names have 
    # been changed, and that can't be helped.
    # 
    # Returns (vnodeName,offset)
    # 
    # vnodeName: the name found in the previous @+body sentinel.
    # offset: the offset within p of the desired line.
    #@-at
    #@@c
    
    def convertLineToVnodeNameIndexLine (self,lines,n,root,scriptFind):
        
        """Convert a line number n to a vnode name, (child index or gnx) and line number."""
        
        c = self ; at = c.atFileCommands
        childIndex = 0 ; gnx = None ; newDerivedFile = False
        thinFile = root.isAtThinFileNode()
        #@    << set delim, leoLine from the @+leo line >>
        #@+node:ekr.20031218072017.2878:<< set delim, leoLine from the @+leo line >>
        # Find the @+leo line.
        tag = "@+leo"
        i = 0 
        while i < len(lines) and lines[i].find(tag)==-1:
            i += 1
        leoLine = i # Index of the line containing the leo sentinel
        
        if leoLine < len(lines):
            s = lines[leoLine]
            valid,newDerivedFile,start,end,derivedFileIsThin = at.parseLeoSentinel(s)
            if valid: delim = start + '@'
            else:     delim = None
        else:
            delim = None
        #@-node:ekr.20031218072017.2878:<< set delim, leoLine from the @+leo line >>
        #@nl
        if not delim:
            g.es("bad @+leo sentinel")
            return None,None,None,None,None
        #@    << scan back to @+node, setting offset,nodeSentinelLine >>
        #@+node:ekr.20031218072017.2879:<< scan back to  @+node, setting offset,nodeSentinelLine >>
        offset = 0 # This is essentially the Tk line number.
        nodeSentinelLine = -1
        line = n - 1
        while line >= 0:
            s = lines[line]
            # g.trace(s)
            i = g.skip_ws(s,0)
            if g.match(s,i,delim):
                #@        << handle delim while scanning backward >>
                #@+node:ekr.20031218072017.2880:<< handle delim while scanning backward >>
                if line == n:
                    g.es("line "+str(n)+" is a sentinel line")
                i += len(delim)
                
                if g.match(s,i,"-node"):
                    # The end of a nested section.
                    line = self.skipToMatchingNodeSentinel(lines,line,delim)
                elif g.match(s,i,"+node"):
                    nodeSentinelLine = line
                    break
                elif g.match(s,i,"<<") or g.match(s,i,"@first"):
                    offset += 1 # Count these as a "real" lines.
                #@nonl
                #@-node:ekr.20031218072017.2880:<< handle delim while scanning backward >>
                #@nl
            else:
                offset += 1 # Assume the line is real.  A dubious assumption.
            line -= 1
        #@nonl
        #@-node:ekr.20031218072017.2879:<< scan back to  @+node, setting offset,nodeSentinelLine >>
        #@nl
        if nodeSentinelLine == -1:
            # The line precedes the first @+node sentinel
            # g.trace("before first line")
            return root.headString(),0,gnx,1,delim # 10/13/03
        s = lines[nodeSentinelLine]
        # g.trace(s)
        #@    << set vnodeName and (childIndex or gnx) from s >>
        #@+node:ekr.20031218072017.2881:<< set vnodeName and (childIndex or gnx) from s >>
        if scriptFind:
            # The vnode name follows the first ':'
            i = s.find(':',i)
            if i > -1:
                vnodeName = s[i+1:].strip()
            childIndex = -1
        elif newDerivedFile:
            i = 0
            if thinFile:
                # gnx is lies between the first and second ':':
                i = s.find(':',i)
                if i > 0:
                    i += 1
                    j = s.find(':',i)
                    if j > 0:
                        gnx = s[i:j]
                    else: i = len(s)
                else: i = len(s)
            # vnode name is everything following the first or second':'
            # childIndex is -1 as a flag for later code.
            i = s.find(':',i)
            if i > -1: vnodeName = s[i+1:].strip()
            else: vnodeName = None
            childIndex = -1
        else:
            # vnode name is everything following the third ':'
            i = 0 ; colons = 0
            while i < len(s) and colons < 3:
                if s[i] == ':':
                    colons += 1
                    if colons == 1 and i+1 < len(s) and s[i+1] in string.digits:
                        junk,childIndex = g.skip_long(s,i+1)
                i += 1
            vnodeName = s[i:].strip()
            
        # g.trace("gnx",gnx,"vnodeName:",vnodeName)
        if not vnodeName:
            vnodeName = None
            g.es("bad @+node sentinel")
        #@nonl
        #@-node:ekr.20031218072017.2881:<< set vnodeName and (childIndex or gnx) from s >>
        #@nl
        # g.trace("childIndex,offset",childIndex,offset,vnodeName)
        return vnodeName,childIndex,gnx,offset,delim
    #@-node:ekr.20031218072017.2877:convertLineToVnodeNameIndexLine
    #@+node:ekr.20031218072017.2882:skipToMatchingNodeSentinel
    def skipToMatchingNodeSentinel (self,lines,n,delim):
        
        s = lines[n]
        i = g.skip_ws(s,0)
        assert(g.match(s,i,delim))
        i += len(delim)
        if g.match(s,i,"+node"):
            start="+node" ; end="-node" ; delta=1
        else:
            assert(g.match(s,i,"-node"))
            start="-node" ; end="+node" ; delta=-1
        # Scan to matching @+-node delim.
        n += delta ; level = 0
        while 0 <= n < len(lines):
            s = lines[n] ; i = g.skip_ws(s,0)
            if g.match(s,i,delim):
                i += len(delim)
                if g.match(s,i,start):
                    level += 1
                elif g.match(s,i,end):
                    if level == 0: break
                    else: level -= 1
            n += delta
            
        # g.trace(n)
        return n
    #@nonl
    #@-node:ekr.20031218072017.2882:skipToMatchingNodeSentinel
    #@-node:ekr.20031218072017.2864:goToLineNumber & allies
    #@+node:bwmulder.20041231211219:gotoLineNumberOpen
    def gotoLineNumberOpen(self, *args, **kw):
        """
        Hook for mod_shadow plugin.
        """
        theFile = open(*args, **kw)
        lines = theFile.readlines()
        theFile.close()
        return lines
    #@nonl
    #@-node:bwmulder.20041231211219:gotoLineNumberOpen
    #@+node:bwmulder.20041231211219.1:applyLineNumberMappingIfAny
    def applyLineNumberMappingIfAny(self, n):
        """
        Hook for mod_shadow plugin.
        """
        return n
    #@nonl
    #@-node:bwmulder.20041231211219.1:applyLineNumberMappingIfAny
    #@+node:EKR.20040612232221:goToScriptLineNumber
    def goToScriptLineNumber (self,root,script,n):
    
        """Go to line n of a script."""
    
        c = self
        
        # g.trace(n,root)
        
        lines = g.splitLines(script)
        c.goToLineNumber(root=root,lines=lines,n=n,scriptFind=True)
    #@nonl
    #@-node:EKR.20040612232221:goToScriptLineNumber
    #@+node:ekr.20031218072017.2088:fontPanel
    def fontPanel (self,event=None):
        
        c = self ; frame = c.frame
    
        if not frame.fontPanel:
            frame.fontPanel = g.app.gui.createFontPanel(c)
            
        frame.fontPanel.bringToFront()
    #@nonl
    #@-node:ekr.20031218072017.2088:fontPanel
    #@+node:ekr.20031218072017.2090:colorPanel
    def colorPanel (self,event=None):
        
        c = self ; frame = c.frame
    
        if not frame.colorPanel:
            frame.colorPanel = g.app.gui.createColorPanel(c)
            
        frame.colorPanel.bringToFront()
    #@nonl
    #@-node:ekr.20031218072017.2090:colorPanel
    #@+node:ekr.20031218072017.2883:viewAllCharacters
    def viewAllCharacters (self,event=None):
    
        c = self ; frame = c.frame
        p = c.currentPosition()
        colorizer = frame.body.getColorizer()
    
        colorizer.showInvisibles = g.choose(colorizer.showInvisibles,0,1)
    
        # It is much easier to change the menu name here than in the menu updater.
        menu = frame.menu.getMenu("Edit")
        if colorizer.showInvisibles:
            frame.menu.setMenuLabel(menu,"Show Invisibles","Hide Invisibles")
        else:
            frame.menu.setMenuLabel(menu,"Hide Invisibles","Show Invisibles")
    
        c.frame.body.recolor_now(p)
    #@nonl
    #@-node:ekr.20031218072017.2883:viewAllCharacters
    #@+node:ekr.20031218072017.2086:preferences
    def preferences (self,event=None):
        
        '''Handle the preferences command.'''
        
        c = self
        c.openLeoSettings()
    #@nonl
    #@-node:ekr.20031218072017.2086:preferences
    #@-node:ekr.20031218072017.2862:Edit top level
    #@+node:ekr.20031218072017.2884:Edit Body submenu
    #@+node:ekr.20031218072017.1704:convertAllBlanks
    def convertAllBlanks (self,event=None):
        
        c = self ; u = c.undoer ; undoType = 'Convert All Blanks'
        current = c.currentPosition()
    
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
        
        d = g.scanDirectives(c)
        tabWidth  = d.get("tabwidth")
        c.beginUpdate()
        try: # In update...
            count = 0 ; dirtyVnodeList = []
            u.beforeChangeGroup(current,undoType)
            for p in current.self_and_subtree_iter():
                # g.trace(p.headString(),tabWidth)
                innerUndoData = u.beforeChangeNodeContents(p)
                if p == current:
                    changed,dirtyVnodeList2 = c.convertBlanks(event)
                    if changed:
                        count += 1
                        dirtyVnodeList.extend(dirtyVnodeList2)
                else:
                    changed = False ; result = []
                    text = p.t.bodyString
                    assert(g.isUnicode(text))
                    lines = string.split(text, '\n')
                    for line in lines:
                        i,w = g.skip_leading_ws_with_indent(line,0,tabWidth)
                        s = g.computeLeadingWhitespace(w,abs(tabWidth)) + line[i:] # use positive width.
                        if s != line: changed = True
                        result.append(s)
                    if changed:
                        count += 1
                        dirtyVnodeList2 = p.setDirty()
                        dirtyVnodeList.extend(dirtyVnodeList2)
                        result = string.join(result,'\n')
                        p.setTnodeText(result)
                        u.afterChangeNodeContents(p,undoType,innerUndoData)
            u.afterChangeGroup(current,undoType,dirtyVnodeList=dirtyVnodeList)
            g.es("blanks converted to tabs in %d nodes" % count) # Must come before c.endUpdate().
        finally:
            c.endUpdate(count > 0)
    #@nonl
    #@-node:ekr.20031218072017.1704:convertAllBlanks
    #@+node:ekr.20031218072017.1705:convertAllTabs
    def convertAllTabs (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Convert All Tabs'
        current = c.currentPosition()
    
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
        theDict = g.scanDirectives(c)
        tabWidth  = theDict.get("tabwidth")
        c.beginUpdate()
        try: # In update:
            count = 0 ; dirtyVnodeList = []
            u.beforeChangeGroup(current,undoType)
            for p in current.self_and_subtree_iter():
                undoData = u.beforeChangeNodeContents(p)
                if p == current:
                    changed,dirtyVnodeList2 = self.convertTabs(event)
                    if changed:
                        count += 1
                        dirtyVnodeList.extend(dirtyVnodeList2)
                else:
                    result = [] ; changed = False
                    text = p.t.bodyString
                    assert(g.isUnicode(text))
                    lines = string.split(text, '\n')
                    for line in lines:
                        i,w = g.skip_leading_ws_with_indent(line,0,tabWidth)
                        s = g.computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
                        if s != line: changed = True
                        result.append(s)
                    if changed:
                        count += 1
                        dirtyVnodeList2 = p.setDirty()
                        dirtyVnodeList.extend(dirtyVnodeList2)
                        result = string.join(result,'\n')
                        p.setTnodeText(result)
                        u.afterChangeNodeContents(p,undoType,undoData)
            u.afterChangeGroup(current,undoType,dirtyVnodeList=dirtyVnodeList)
            g.es("tabs converted to blanks in %d nodes" % count)
        finally:
            c.endUpdate(count > 0)
    #@nonl
    #@-node:ekr.20031218072017.1705:convertAllTabs
    #@+node:ekr.20031218072017.1821:convertBlanks
    def convertBlanks (self,event=None):
    
        c = self ; undoType = 'Convert Blanks'
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return False
    
        head,lines,tail,oldSel,oldYview = c.getBodyLines(expandSelection=True)
        result = [] ; changed = False
    
        # Use the relative @tabwidth, not the global one.
        theDict = g.scanDirectives(c)
        tabWidth  = theDict.get("tabwidth")
        if not tabWidth: return False
    
        for line in lines:
            s = g.optimizeLeadingWhitespace(line,abs(tabWidth)) # Use positive width.
            if s != line: changed = True
            result.append(s)
    
        if changed:
            result = string.join(result,'\n')
            dirtyVnodeList = c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
        else:
            dirtyVnodeList = []
    
        return changed,dirtyVnodeList
    #@nonl
    #@-node:ekr.20031218072017.1821:convertBlanks
    #@+node:ekr.20031218072017.1822:convertTabs
    def convertTabs (self,event=None):
    
        c = self ; undoType = 'Convert Tabs'
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return False
    
        head,lines,tail,oldSel,oldYview = self.getBodyLines(expandSelection=True)
        result = [] ; changed = False
        
        # Use the relative @tabwidth, not the global one.
        theDict = g.scanDirectives(c)
        tabWidth  = theDict.get("tabwidth")
        if not tabWidth: return False,None
    
        for line in lines:
            i,w = g.skip_leading_ws_with_indent(line,0,tabWidth)
            s = g.computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
            if s != line: changed = True
            result.append(s)
    
        if changed:
            result = string.join(result,'\n')
            dirtyVnodeList = c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
        else:
            dirtyVnodeList = []
            
        return changed,dirtyVnodeList
    #@nonl
    #@-node:ekr.20031218072017.1822:convertTabs
    #@+node:ekr.20031218072017.1823:createLastChildNode
    def createLastChildNode (self,parent,headline,body):
        
        '''A helper function for the three extract commands.'''
        
        c = self
        
        if body and len(body) > 0:
            body = string.rstrip(body)
        if not body or len(body) == 0:
            body = ""
    
        p = parent.insertAsLastChild()
        p.initHeadString(headline)
        p.setTnodeText(body)
        p.setDirty()
        c.validateOutline()
        return p
    #@nonl
    #@-node:ekr.20031218072017.1823:createLastChildNode
    #@+node:ekr.20031218072017.1824:dedentBody
    def dedentBody (self,event=None):
        
        c = self ; undoType = 'Unindent' ; current = c.currentPosition()
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
    
        d = g.scanDirectives(c,current) # Support @tab_width directive properly.
        tab_width = d.get("tabwidth",c.tab_width)
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
        
        result = [] ; changed = False
        for line in lines:
            i, width = g.skip_leading_ws_with_indent(line,0,tab_width)
            s = g.computeLeadingWhitespace(width-abs(tab_width),tab_width) + line[i:]
            if s != line: changed = True
            result.append(s)
    
        if changed:
            result = string.join(result,'\n')
            c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview)
    #@nonl
    #@-node:ekr.20031218072017.1824:dedentBody
    #@+node:ekr.20031218072017.1706:extract
    def extract (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Extract'
        current = c.currentPosition()
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
        
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
        if not lines: return
        headline = lines[0].strip() ; del lines[0]
        
        if not lines:
            g.es("Nothing follows section name",color="blue")
            return
    
        # Remove leading whitespace from all body lines.
        junk, ws = g.skip_leading_ws_with_indent(lines[0],0,c.tab_width)
        strippedLines = [g.removeLeadingWhitespace(line,ws,c.tab_width)
            for line in lines]
        newBody = string.join(strippedLines,'\n')
        if head: head = head.rstrip()
    
        c.beginUpdate()
        try: # In update...
            u.beforeChangeGroup(current,undoType)
            if 1: # In group...
                undoData = u.beforeInsertNode(current)
                p = c.createLastChildNode(current,headline,newBody)
                u.afterInsertNode(p,undoType,undoData)
                c.updateBodyPane(head,None,tail,undoType,oldSel,oldYview,setSel=False)
            u.afterChangeGroup(current,undoType)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.1706:extract
    #@+node:ekr.20031218072017.1708:extractSection
    def extractSection (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Extract Section'
        current = c.currentPosition()
    
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
        if not lines: return
    
        line1 = '\n' + lines[0]
        headline = lines[0].strip() ; del lines[0]
        #@    << Set headline for extractSection >>
        #@+node:ekr.20031218072017.1709:<< Set headline for extractSection >>
        if len(headline) < 5:
            oops = True
        else:
            head1 = headline[0:2] == '<<'
            head2 = headline[0:2] == '@<'
            tail1 = headline[-2:] == '>>'
            tail2 = headline[-2:] == '@>'
            oops = not (head1 and tail1) and not (head2 and tail2)
        
        if oops:
            g.es("Selected text should start with a section name",color="blue")
            return
        #@nonl
        #@-node:ekr.20031218072017.1709:<< Set headline for extractSection >>
        #@nl
        
        if not lines:
            g.es("Nothing follows section name",color="blue")
            return
        
        # Remove leading whitespace from all body lines.
        junk, ws = g.skip_leading_ws_with_indent(lines[0],0,c.tab_width)
        strippedLines = [g.removeLeadingWhitespace(line,ws,c.tab_width)
            for line in lines]
        newBody = string.join(strippedLines,'\n')
        if head: head = head.rstrip()
    
        c.beginUpdate()
        try: # In update...
            u.beforeChangeGroup(current,undoType)
            if 1: # In group...
                undoData = u.beforeInsertNode(current)
                p = c.createLastChildNode(current,headline,newBody)
                u.afterInsertNode(p,undoType,undoData)
                c.updateBodyPane(head+line1,None,tail,undoType,oldSel,oldYview,setSel=False)
            u.afterChangeGroup(current,undoType)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.1708:extractSection
    #@+node:ekr.20031218072017.1710:extractSectionNames
    def extractSectionNames(self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Extract Section Names'
        body = c.frame.body ; current = c.currentPosition()
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
        if not lines: return
    
        c.beginUpdate()
        try: # In update...
            u.beforeChangeGroup(current,undoType)
            if 1: # In group...
                found = False
                for s in lines:
                    #@                << Find the next section name >>
                    #@+node:ekr.20031218072017.1711:<< Find the next section name >>
                    head1 = string.find(s,"<<")
                    if head1 > -1:
                        head2 = string.find(s,">>",head1)
                    else:
                        head1 = string.find(s,"@<")
                        if head1 > -1:
                            head2 = string.find(s,"@>",head1)
                            
                    if head1 == -1 or head2 == -1 or head1 > head2:
                        name = None
                    else:
                        name = s[head1:head2+2]
                    #@nonl
                    #@-node:ekr.20031218072017.1711:<< Find the next section name >>
                    #@nl
                    if name:
                        undoData = u.beforeInsertNode(current)
                        p = self.createLastChildNode(current,name,None)
                        u.afterInsertNode(p,undoType,undoData)
                        found = True
                c.selectPosition(current)
                c.validateOutline()
                if not found:
                    g.es("Selected text should contain one or more section names",color="blue")
            u.afterChangeGroup(current,undoType)
        finally:
            c.endUpdate()
    
        # Restore the selection.
        body.setTextSelection(oldSel)
        body.setFocus()
    #@nonl
    #@-node:ekr.20031218072017.1710:extractSectionNames
    #@+node:ekr.20031218072017.1825:findBoundParagraph
    def findBoundParagraph (self,event=None):
        
        c = self
        head,ins,tail = c.frame.body.getInsertLines()
    
        if not ins or ins.isspace() or ins[0] == '@':
            return None,None,None,None # DTHEIN 18-JAN-2004
            
        head_lines = g.splitLines(head)
        tail_lines = g.splitLines(tail)
    
        if 0:
            #@        << trace head_lines, ins, tail_lines >>
            #@+node:ekr.20031218072017.1826:<< trace head_lines, ins, tail_lines >>
            if 0:
                print ; print "head_lines"
                for line in head_lines: print line
                print ; print "ins", ins
                print ; print "tail_lines"
                for line in tail_lines: print line
            else:
                g.es("head_lines: ",head_lines)
                g.es("ins: ",ins)
                g.es("tail_lines: ",tail_lines)
            #@nonl
            #@-node:ekr.20031218072017.1826:<< trace head_lines, ins, tail_lines >>
            #@nl
    
        # Scan backwards.
        i = len(head_lines)
        while i > 0:
            i -= 1
            line = head_lines[i]
            if len(line) == 0 or line.isspace() or line[0] == '@':
                i += 1 ; break
    
        pre_para_lines = head_lines[:i]
        para_head_lines = head_lines[i:]
    
        # Scan forwards.
        i = 0
        trailingNL = False # DTHEIN 18-JAN-2004: properly capture terminating NL
        while i < len(tail_lines):
            line = tail_lines[i]
            if len(line) == 0 or line.isspace() or line[0] == '@':
                trailingNL = line.endswith(u'\n') or line.startswith(u'@') # DTHEIN 21-JAN-2004
                break
            i += 1
            
    #   para_tail_lines = tail_lines[:i]
        para_tail_lines = tail_lines[:i]
        post_para_lines = tail_lines[i:]
        
        head = g.joinLines(pre_para_lines)
        result = para_head_lines 
        result.extend([ins])
        result.extend(para_tail_lines)
        tail = g.joinLines(post_para_lines)
    
        # DTHEIN 18-JAN-2004: added trailingNL to return value list
        return head,result,tail,trailingNL # string, list, string, bool
    #@nonl
    #@-node:ekr.20031218072017.1825:findBoundParagraph
    #@+node:ekr.20031218072017.1827:findMatchingBracket
    def findMatchingBracket (self,event=None):
        
        c = self ; body = c.frame.body
        
        if g.app.batchMode:
            c.notValidInBatchMode("Match Brackets")
            return
    
        brackets = "()[]{}<>"
        ch1 = body.getCharBeforeInsertPoint()
        ch2 = body.getCharAtInsertPoint()
    
        # Prefer to match the character to the left of the cursor.
        if ch1 in brackets:
            ch = ch1 ; index = body.getBeforeInsertionPoint()
        elif ch2 in brackets:
            ch = ch2 ; index = body.getInsertionPoint()
        else:
            return
        
        index2 = self.findSingleMatchingBracket(ch,index)
        if index2:
            if body.compareIndices(index,"<=",index2):
                adj_index = body.adjustIndex(index2,1)
                body.setTextSelection(index,adj_index)
            else:
                adj_index = body.adjustIndex(index,1)
                body.setTextSelection(index2,adj_index)
            adj_index = body.adjustIndex(index2,1)
            body.setInsertionPoint(adj_index)
            body.makeIndexVisible(adj_index)
        else:
            g.es("unmatched '%s'",ch)
    #@nonl
    #@+node:ekr.20031218072017.1828:findMatchingBracket
    # To do: replace comments with blanks before scanning.
    # Test  unmatched())
    def findSingleMatchingBracket(self,ch,index):
        
        c = self ; body = c.frame.body
        open_brackets  = "([{<" ; close_brackets = ")]}>"
        brackets = open_brackets + close_brackets
        matching_brackets = close_brackets + open_brackets
        forward = ch in open_brackets
        # Find the character matching the initial bracket.
        for n in xrange(len(brackets)):
            if ch == brackets[n]:
                match_ch = matching_brackets[n]
                break
        level = 0
        while 1:
            if forward and body.compareIndices(index,">=","end"):
                # g.trace("not found")
                return None
            ch2 = body.getCharAtIndex(index)
            if ch2 == ch:
                level += 1 #; g.trace(level,index)
            if ch2 == match_ch:
                level -= 1 #; g.trace(level,index)
                if level <= 0:
                    return index
            if not forward and body.compareIndices(index,"<=","1.0"):
                # g.trace("not found")
                return None
            adj = g.choose(forward,1,-1)
            index = body.adjustIndex(index,adj)
        return 0 # unreachable: keeps pychecker happy.
    # Test  (
    # ([(x){y}]))
    # Test  ((x)(unmatched
    #@nonl
    #@-node:ekr.20031218072017.1828:findMatchingBracket
    #@-node:ekr.20031218072017.1827:findMatchingBracket
    #@+node:ekr.20031218072017.1829:getBodyLines
    def getBodyLines (self,expandSelection=False):
    
        c = self ; body = c.frame.body
        oldVview = body.getYScrollPosition()
        oldSel   = body.getTextSelection()
    
        if expandSelection: # 12/3/03
            lines = body.getAllText()
            head = tail = None
        else:
            # Note: lines is the entire line containing the insert point if no selection.
            head,lines,tail = body.getSelectionLines()
    
        lines = string.split(lines,'\n') # It would be better to use splitLines.
    
        return head,lines,tail,oldSel,oldVview
    #@nonl
    #@-node:ekr.20031218072017.1829:getBodyLines
    #@+node:ekr.20031218072017.1830:indentBody
    def indentBody (self,event=None):
        
        '''The indent-region command indents each line of the selected body text,
        or each line of a node if there is no selected text. The @tabwidth directive
        in effect determines amount of indentation. (not yet) A numeric argument
        specifies the column to indent to.'''
    
        c = self ; undoType = 'Indent Region' ; current = c.currentPosition()
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
    
        d = g.scanDirectives(c,current) # Support @tab_width directive properly.
        tab_width = d.get("tabwidth",c.tab_width)
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
    
        result = [] ; changed = False
        for line in lines:
            i, width = g.skip_leading_ws_with_indent(line,0,tab_width)
            s = g.computeLeadingWhitespace(width+abs(tab_width),tab_width) + line[i:]
            if s != line: changed = True
            result.append(s)
    
        if changed:
            result = string.join(result,'\n')
            c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview)
    #@nonl
    #@-node:ekr.20031218072017.1830:indentBody
    #@+node:ekr.20031218072017.1831:insertBodyTime & allies
    def insertBodyTime (self,event=None):
        
        c = self ; undoType = 'Insert Body Time'
        
        if g.app.batchMode:
            c.notValidInBatchMode(undoType)
            return
        
        oldSel = c.frame.body.getTextSelection()
        c.frame.body.deleteTextSelection() # Works if nothing is selected.
        s = self.getTime(body=True)
    
        c.frame.body.insertAtInsertPoint(s)
        c.frame.body.onBodyChanged(undoType,oldSel=oldSel)
    #@nonl
    #@+node:ekr.20031218072017.1832:getTime & test
    def getTime (self,body=True):
    
        c = self
        default_format =  "%m/%d/%Y %H:%M:%S" # E.g., 1/30/2003 8:31:55
        
        # Try to get the format string from leoConfig.txt.
        if body:
            format = c.config.getString("body_time_format_string")
            gmt    = c.config.getBool("body_gmt_time")
        else:
            format = c.config.getString("headline_time_format_string")
            gmt    = c.config.getBool("headline_gmt_time")
    
        if format == None:
            format = default_format
    
        try:
            import time
            if gmt:
                s = time.strftime(format,time.gmtime())
            else:
                s = time.strftime(format,time.localtime())
        except (ImportError, NameError):
            g.es("time.strftime not available on this platform",color="blue")
            return ""
        except:
            g.es_exception() # Probably a bad format string in leoSettings.leo.
            s = time.strftime(default_format,time.gmtime())
        return s
    #@-node:ekr.20031218072017.1832:getTime & test
    #@-node:ekr.20031218072017.1831:insertBodyTime & allies
    #@+node:ekr.20050312114529:insert/removeComments
    #@+node:ekr.20050312114529.1:addComments
    def addComments (self,event=None):
    
        c = self ; undoType = 'Add Comments' ; p = c.currentPosition()
        
        d = g.scanDirectives(c,p)
        # d1 is the line delim.
        d1,d2,d3 = d.get('delims')
    
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
        result = []
        if not lines:
            g.es('No text selected',color='blue')
            return
        
        if d1:
            # Append the single-line comment delim in front of each line
            for line in lines:
                i = g.skip_ws(line,0)
                result.append('%s%s %s' % (line[0:i],d1,line[i:]))
        else:
            n = len(lines)
            for i in xrange(n):
                line = lines[i]
                if i not in (0,n-1):
                    result.append(line)
                if i == 0:
                    j = g.skip_ws(line,0)
                    result.append('%s%s %s' % (line[0:j],d2,line[j:]))
                if i == n-1:
                    j = len(line.rstrip())
                    result.append('%s %s' % (line[0:j],d3))
    
        result = string.join(result,'\n')
        c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview)
    #@nonl
    #@-node:ekr.20050312114529.1:addComments
    #@+node:ekr.20050312114529.2:deleteComments
    def deleteComments (self,event=None):
    
        c = self ; undoType = 'Delete Comments' ; p = c.currentPosition()
        
        d = g.scanDirectives(c,p)
        # d1 is the line delim.
        d1,d2,d3 = d.get('delims')
    
        head,lines,tail,oldSel,oldYview = self.getBodyLines()
        result = []
        if not lines:
            g.es('No text selected',color='blue')
            return
        
        if d1:
            # Append the single-line comment delim in front of each line
            for line in lines:
                i = g.skip_ws(line,0)
                if g.match(line,i,d1):
                    j = g.skip_ws(line,i + len(d1))
                    result.append(line[0:i] + line[j:])
                else:
                    result.append(line)
        else:
            n = len(lines)
            for i in xrange(n):
                line = lines[i]
                if i not in (0,n-1):
                    result.append(line)
                if i == 0:
                    j = g.skip_ws(line,0)
                    if g.match(line,j,d2):
                        k = g.skip_ws(line,j + len(d2))
                        result.append(line[0:j] + line[k:])
                    else:
                        g.es("'%s' not found" % (d2),color='blue')
                        return
                if i == n-1:
                    if i == 0:
                        line = result[0] ; result = []
                    s = line.rstrip()
                    if s.endswith(d3):
                        result.append(s[:-len(d3)].rstrip())
                    else:
                        g.es("'%s' not found" % (d3),color='blue')
                        return
    
        result = string.join(result,'\n')
        c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview)
    #@nonl
    #@-node:ekr.20050312114529.2:deleteComments
    #@-node:ekr.20050312114529:insert/removeComments
    #@+node:ekr.20031218072017.1833:reformatParagraph
    def reformatParagraph (self,event=None):
    
        """Reformat a text paragraph in a Tk.Text widget
    
    Wraps the concatenated text to present page width setting. Leading tabs are
    sized to present tab width setting. First and second line of original text is
    used to determine leading whitespace in reformatted text. Hanging indentation
    is honored.
    
    Paragraph is bound by start of body, end of body, blank lines, and lines
    starting with "@". Paragraph is selected by position of current insertion
    cursor."""
    
        c = self ; body = c.frame.body
        
        if g.app.batchMode:
            c.notValidInBatchMode("xxx")
            return
    
        if body.hasTextSelection():
            g.es("Text selection inhibits Reformat Paragraph",color="blue")
            return
    
        #@    << compute vars for reformatParagraph >>
        #@+node:ekr.20031218072017.1834:<< compute vars for reformatParagraph >>
        theDict = g.scanDirectives(c)
        pageWidth = theDict.get("pagewidth")
        tabWidth  = theDict.get("tabwidth")
        
        original = body.getAllText()
        oldSel   = body.getTextSelection()
        oldYview = body.getYScrollPosition()
        head,lines,tail,trailingNL = c.findBoundParagraph() # DTHEIN 18-JAN-2004: add trailingNL
        #@nonl
        #@-node:ekr.20031218072017.1834:<< compute vars for reformatParagraph >>
        #@nl
        if lines:
            #@        << compute the leading whitespace >>
            #@+node:ekr.20031218072017.1835:<< compute the leading whitespace >>
            indents = [0,0] ; leading_ws = ["",""]
            
            for i in (0,1):
                if i < len(lines):
                    # Use the original, non-optimized leading whitespace.
                    leading_ws[i] = ws = g.get_leading_ws(lines[i])
                    indents[i] = g.computeWidth(ws,tabWidth)
                    
            indents[1] = max(indents)
            if len(lines) == 1:
                leading_ws[1] = leading_ws[0]
            #@-node:ekr.20031218072017.1835:<< compute the leading whitespace >>
            #@nl
            #@        << compute the result of wrapping all lines >>
            #@+node:ekr.20031218072017.1836:<< compute the result of wrapping all lines >>
            # Remember whether the last line ended with a newline.
            lastLine = lines[-1]
            if 0: # DTHEIN 18-JAN-2004: removed because findBoundParagraph now gives trailingNL
                trailingNL = lastLine and lastLine[-1] == '\n'
            
            # Remove any trailing newlines for wraplines.
            lines = [line[:-1] for line in lines[:-1]]
            if lastLine and not trailingNL:
                lastLine = lastLine[:-1]
            lines.extend([lastLine])
            
            # Wrap the lines, decreasing the page width by indent.
            result = g.wrap_lines(lines,
                pageWidth-indents[1],
                pageWidth-indents[0])
            
            # DTHEIN 18-JAN-2004
            # prefix with the leading whitespace, if any
            paddedResult = []
            paddedResult.append(leading_ws[0] + result[0])
            for line in result[1:]:
                paddedResult.append(leading_ws[1] + line)
            
            # Convert the result to a string.
            result = '\n'.join(paddedResult) # DTHEIN 18-JAN-2004: use paddedResult
            if 0: # DTHEIN 18-JAN-2004:  No need to do this.
                if trailingNL:
                    result += '\n'
            #@-node:ekr.20031218072017.1836:<< compute the result of wrapping all lines >>
            #@nl
            #@        << update the body, selection & undo state >>
            #@+node:ekr.20031218072017.1837:<< update the body, selection & undo state >>
            sel_start, sel_end = body.setSelectionAreas(head,result,tail)
            
            changed = original != head + result + tail
            undoType = g.choose(changed,"Reformat Paragraph",None)
            body.onBodyChanged(undoType,oldSel=oldSel,oldYview=oldYview)
            
            # Advance the selection to the next paragraph.
            newSel = sel_end, sel_end
            body.setTextSelection(newSel)
            body.makeIndexVisible(sel_end)
            
            c.recolor()
            #@nonl
            #@-node:ekr.20031218072017.1837:<< update the body, selection & undo state >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.1833:reformatParagraph
    #@+node:ekr.20031218072017.1838:updateBodyPane (handles changeNodeContents)
    def updateBodyPane (self,head,middle,tail,undoType,oldSel,oldYview,setSel=True):
        
        c = self ; body = c.frame.body ; p = c.currentPosition()
        
        # g.trace(undoType)
    
        # Update the text and notify the event handler.
        body.setSelectionAreas(head,middle,tail)
    
        if setSel and oldSel:
            body.setTextSelection(oldSel)
    
        # This handles the undo.
        body.onBodyChanged(undoType,oldSel=oldSel,oldYview=oldYview)
    
        # Update the changed mark and icon.
        c.beginUpdate()
        try: # In update...
            c.setChanged(True)
            if p.isDirty():
                dirtyVnodeList = []
            else:
                dirtyVnodeList = p.setDirty()
        finally:
            c.endUpdate()
    
        # Scroll as necessary.
        if oldYview:
            body.setYScrollPosition(oldYview)
        else:
            body.makeInsertPointVisible()
    
        body.setFocus()
        c.recolor()
        return dirtyVnodeList
    #@nonl
    #@-node:ekr.20031218072017.1838:updateBodyPane (handles changeNodeContents)
    #@-node:ekr.20031218072017.2884:Edit Body submenu
    #@+node:ekr.20031218072017.2885:Edit Headline submenu
    #@+node:ekr.20031218072017.2886:editHeadline
    def editHeadline (self,event=None):
        
        c = self ; k = c.k ; tree = c.frame.tree
        
        if g.app.batchMode:
            c.notValidInBatchMode("Edit Headline")
            return
            
        if k:
            k.setDefaultUnboundKeyAction()
            k.showStateAndMode()
    
        tree.editLabel(c.currentPosition())
    #@nonl
    #@-node:ekr.20031218072017.2886:editHeadline
    #@+node:ekr.20031218072017.2290:toggleAngleBrackets
    def toggleAngleBrackets (self,event=None):
        
        c = self ; v = c.currentVnode()
        
        if g.app.batchMode:
            c.notValidInBatchMode("Toggle Angle Brackets")
            return
            
        c.endEditing()
    
        s = v.headString().strip()
        if (s[0:2] == "<<"
            or s[-2:] == ">>"): # Must be on separate line.
            if s[0:2] == "<<": s = s[2:]
            if s[-2:] == ">>": s = s[:-2]
            s = s.strip()
        else:
            s = g.angleBrackets(' ' + s + ' ')
        
        c.frame.tree.editLabel(v)
        w = v.edit_widget()
        if w:
            w.delete("1.0","end")
            w.insert("1.0",s)
            c.frame.tree.onHeadChanged(v,'Toggle Angle Brackets')
    #@nonl
    #@-node:ekr.20031218072017.2290:toggleAngleBrackets
    #@-node:ekr.20031218072017.2885:Edit Headline submenu
    #@+node:ekr.20031218072017.2887:Find submenu (frame methods)
    #@+node:ekr.20051013084200:dismissFindPanel
    def dismissFindPanel (self,event=None):
        
        c = self
        
        if c.frame.findPanel:
            c.frame.findPanel.dismiss()
    #@nonl
    #@-node:ekr.20051013084200:dismissFindPanel
    #@+node:ekr.20031218072017.2888:showFindPanel
    def showFindPanel (self,event=None):
    
        c = self
        
        if not c.frame.findPanel:
            c.frame.findPanel = g.app.gui.createFindPanel(c)
    
        c.frame.findPanel.bringToFront()
    #@nonl
    #@-node:ekr.20031218072017.2888:showFindPanel
    #@+node:ekr.20031218072017.2889:findNext
    def findNext (self,event=None):
    
        c = self
        
        if not c.frame.findPanel:
            c.frame.findPanel = g.app.gui.createFindPanel(c)
    
        c.frame.findPanel.findNextCommand(c)
    #@-node:ekr.20031218072017.2889:findNext
    #@+node:ekr.20031218072017.2890:findPrevious
    def findPrevious (self,event=None):
    
        c = self
        
        if not c.frame.findPanel:
            c.frame.findPanel = g.app.gui.createFindPanel(c)
    
        c.frame.findPanel.findPreviousCommand(c)
    #@-node:ekr.20031218072017.2890:findPrevious
    #@+node:ekr.20031218072017.2891:replace
    def replace (self,event=None):
    
        c = self
        
        if not c.frame.findPanel:
            c.frame.findPanel = g.app.gui.createFindPanel(c)
    
        c.frame.findPanel.changeCommand(c)
    #@-node:ekr.20031218072017.2891:replace
    #@+node:ekr.20031218072017.2892:replaceThenFind
    def replaceThenFind (self,event=None):
    
        c = self
        
        if not c.frame.findPanel:
            c.frame.findPanel = g.app.gui.createFindPanel(c)
    
        c.frame.findPanel.changeThenFindCommand(c)
    #@-node:ekr.20031218072017.2892:replaceThenFind
    #@+node:ekr.20051013083241:replaceAll
    def replaceAll (self,event=None):
    
        c = self
        
        if not c.frame.findPanel:
            c.frame.findPanel = g.app.gui.createFindPanel(c)
    
        c.frame.findPanel.changeAllCommand(c)
    #@-node:ekr.20051013083241:replaceAll
    #@-node:ekr.20031218072017.2887:Find submenu (frame methods)
    #@+node:ekr.20031218072017.2893:notValidInBatchMode
    def notValidInBatchMode(self, commandName):
        
        g.es("%s command is not valid in batch mode" % commandName)
    #@-node:ekr.20031218072017.2893:notValidInBatchMode
    #@-node:ekr.20031218072017.2861:Edit Menu...
    #@+node:ekr.20031218072017.2894:Outline menu...
    #@+node:ekr.20031218072017.2895: Top Level... (Commands)
    #@+node:ekr.20031218072017.1548:Cut & Paste Outlines
    #@+node:ekr.20031218072017.1549:cutOutline
    def cutOutline (self,event=None):
    
        c = self
        if c.canDeleteHeadline():
            c.copyOutline()
            c.deleteOutline("Cut Node")
            c.recolor()
    #@nonl
    #@-node:ekr.20031218072017.1549:cutOutline
    #@+node:ekr.20031218072017.1550:copyOutline
    def copyOutline (self,event=None):
    
        # Copying an outline has no undo consequences.
        c = self
        c.endEditing()
        c.fileCommands.assignFileIndices()
        s = c.fileCommands.putLeoOutline()
        g.app.gui.replaceClipboardWith(s)
    #@nonl
    #@-node:ekr.20031218072017.1550:copyOutline
    #@+node:ekr.20031218072017.1551:pasteOutline
    # To cut and paste between apps, just copy into an empty body first, then copy to Leo's clipboard.
    
    def pasteOutline(self,event=None,reassignIndices=True):
    
        c = self ; u = c.undoer ; current = c.currentPosition()
        s = g.app.gui.getTextFromClipboard()
        pasteAsClone = not reassignIndices
        undoType = g.choose(reassignIndices,'Paste Node','Paste As Clone')
        
        c.endEditing()
    
        if not s or not c.canPasteOutline(s):
            return # This should never happen.
    
        isLeo = g.match(s,0,g.app.prolog_prefix_string)
        tnodeInfoDict = {}
        if pasteAsClone:
            #@        << remember all data for undo/redo Paste As Clone >>
            #@+node:ekr.20050418084539:<< remember all data for undo/redo Paste As Clone >>
            #@+at
            # 
            # We don't know yet which nodes will be affected by the paste, so 
            # we remember
            # everything. This is expensive, but foolproof.
            # 
            # The alternative is to try to remember the 'before' values of 
            # tnodes in the
            # fileCommands read logic. Several experiments failed, and the 
            # code is very ugly.
            # In short, it seems wise to do things the foolproof way.
            # 
            #@-at
            #@@c
            
            for p in c.allNodes_iter():
                t = p.v.t
                if t not in tnodeInfoDict.keys():
                    tnodeInfoDict[t] = g.Bunch(
                        t=t,head=p.headString(),body=p.bodyString())
            #@nonl
            #@-node:ekr.20050418084539:<< remember all data for undo/redo Paste As Clone >>
            #@nl
    
        if isLeo:
            pasted = c.fileCommands.getLeoOutline(s,reassignIndices)
        else:
            pasted = c.importCommands.convertMoreStringToOutlineAfter(s,current)
        if not pasted: return
    
        c.beginUpdate()
        try:
            copiedBunchList = []
            if pasteAsClone:
                #@            << put only needed info in copiedBunchList >>
                #@+node:ekr.20050418084539.2:<< put only needed info in copiedBunchList >>
                # Create a dict containing only copied tnodes.
                copiedTnodeDict = {}
                for p in pasted.self_and_subtree_iter():
                    if p.v.t not in copiedTnodeDict:
                        copiedTnodeDict[p.v.t] = p.v.t
                        
                # g.trace(copiedTnodeDict.keys())
                
                for t in tnodeInfoDict.keys():
                    bunch = tnodeInfoDict.get(t)
                    if copiedTnodeDict.get(t):
                        copiedBunchList.append(bunch)
                
                # g.trace('copiedBunchList',copiedBunchList)
                #@nonl
                #@-node:ekr.20050418084539.2:<< put only needed info in copiedBunchList >>
                #@nl
            undoData = u.beforeInsertNode(current,
            pasteAsClone=pasteAsClone,copiedBunchList=copiedBunchList)
            c.endEditing()
            c.validateOutline()
            c.selectPosition(pasted)
            pasted.setDirty()
            c.setChanged(True)
            # paste as first child if back is expanded.
            back = pasted.back()
            if back and back.isExpanded():
                pasted.moveToNthChildOf(back,0)
            u.afterInsertNode(pasted,undoType,undoData)
        finally:
            c.endUpdate(scroll=True)
            c.recolor()
    #@nonl
    #@-node:ekr.20031218072017.1551:pasteOutline
    #@+node:EKR.20040610130943:pasteOutlineRetainingClones
    def pasteOutlineRetainingClones (self,event=None):
        
        c = self
    
        return c.pasteOutline(reassignIndices=False)
    #@nonl
    #@-node:EKR.20040610130943:pasteOutlineRetainingClones
    #@-node:ekr.20031218072017.1548:Cut & Paste Outlines
    #@+node:ekr.20031218072017.2028:Hoist & dehoist
    def dehoist (self,event=None):
    
        c = self ; p = c.currentPosition()
        if p and c.canDehoist():
            bunch = c.hoistStack.pop()
            c.beginUpdate()
            try:
                if bunch.expanded: p.expand()
                else:              p.contract()
            finally:
                c.endUpdate()
            c.frame.clearStatusLine()
            if c.hoistStack:
                bunch = c.hoistStack[-1]
                c.frame.putStatusLine("Hoist: " + bunch.p.headString())
            else:
                c.frame.putStatusLine("No hoist")
            c.undoer.afterDehoist(p,'DeHoist')
    
    def hoist (self,event=None):
    
        c = self ; p = c.currentPosition()
        if p and c.canHoist():
            # Remember the expansion state.
            bunch = g.Bunch(p=p.copy(),expanded=p.isExpanded())
            c.hoistStack.append(bunch)
            c.beginUpdate()
            try:
                p.expand()
            finally:
                c.endUpdate()
            c.frame.clearStatusLine()
            c.frame.putStatusLine("Hoist: " + p.headString())
            c.undoer.afterHoist(p,'Hoist')
    #@nonl
    #@-node:ekr.20031218072017.2028:Hoist & dehoist
    #@+node:ekr.20031218072017.1759:Insert, Delete & Clone (Commands)
    #@+node:ekr.20031218072017.1760:c.checkMoveWithParentWithWarning
    def checkMoveWithParentWithWarning (self,root,parent,warningFlag):
        
        """Return False if root or any of root's descedents is a clone of
        parent or any of parents ancestors."""
    
        message = "Illegal move or drag: no clone may contain a clone of itself"
    
        # g.trace("root",root,"parent",parent)
        clonedTnodes = {}
        for ancestor in parent.self_and_parents_iter():
            if ancestor.isCloned():
                t = ancestor.v.t
                clonedTnodes[t] = t
    
        if not clonedTnodes:
            return True
    
        for p in root.self_and_subtree_iter():
            if p.isCloned() and clonedTnodes.get(p.v.t):
                if warningFlag:
                    g.alert(message)
                return False
        return True
    #@nonl
    #@-node:ekr.20031218072017.1760:c.checkMoveWithParentWithWarning
    #@+node:ekr.20031218072017.1193:c.deleteOutline
    def deleteOutline (self,event=None,op_name="Delete Node"):
        
        """Deletes the current position.
        
        Does nothing if the outline would become empty."""
    
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
    
        if p.hasVisBack(): newNode = p.visBack()
        else: newNode = p.next() # _not_ p.visNext(): we are at the top level.
        if not newNode: return
    
        c.beginUpdate()
        try:
           c.endEditing() # Make sure we capture the headline for Undo.
           undoData = u.beforeDeleteNode(p)
           dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
           p.doDelete()
           c.selectPosition(newNode)
           c.setChanged(True)
           u.afterDeleteNode(newNode,op_name,undoData,dirtyVnodeList=dirtyVnodeList)
        finally:
            c.endUpdate()
    
        c.validateOutline()
    #@nonl
    #@-node:ekr.20031218072017.1193:c.deleteOutline
    #@+node:ekr.20031218072017.1761:c.insertHeadline
    def insertHeadline (self,event=None,op_name="Insert Node"):
        
        '''Insert a node after the presently selected node.'''
    
        c = self ; u = c.undoer
        current = c.currentPosition()
        
        if not current: return
    
        c.beginUpdate()
        try:
            undoData = c.undoer.beforeInsertNode(current)
            # Make sure the new node is visible when hoisting.
            if ((current.hasChildren() and current.isExpanded()) or
                (c.hoistStack and current == c.hoistStack[-1].p)):
                p = current.insertAsNthChild(0)
            else:
                p = current.insertAfter()
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            c.setChanged(True)
            u.afterInsertNode(p,op_name,undoData,dirtyVnodeList=dirtyVnodeList)
        finally:
            c.endUpdate(False,scroll=True)
            c.editPosition(p)
    
        return p # for mod_labels plugin.
    #@nonl
    #@-node:ekr.20031218072017.1761:c.insertHeadline
    #@+node:ekr.20031218072017.1762:c.clone
    def clone (self,event=None):
    
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
        
        c.beginUpdate()
        try: # In update...
            undoData = c.undoer.beforeCloneNode(p)
            clone = p.clone(p)
            dirtyVnodeList = clone.setAllAncestorAtFileNodesDirty()
            c.setChanged(True)
            if c.validateOutline():
                u.afterCloneNode(clone,'Clone Node',undoData,dirtyVnodeList=dirtyVnodeList)
                c.selectPosition(clone)
        finally:
            c.endUpdate()
    
        return clone # For mod_labels and chapters plugins.
    #@nonl
    #@-node:ekr.20031218072017.1762:c.clone
    #@+node:ekr.20031218072017.1765:c.validateOutline
    # Makes sure all nodes are valid.
    
    def validateOutline (self,event=None):
    
        c = self
        
        if not g.app.debug:
            return True
    
        root = c.rootPosition()
        parent = c.nullPosition()
    
        if root:
            return root.validateOutlineWithParent(parent)
        else:
            return True
    #@nonl
    #@-node:ekr.20031218072017.1765:c.validateOutline
    #@-node:ekr.20031218072017.1759:Insert, Delete & Clone (Commands)
    #@+node:ekr.20050415134809:c.sortChildren
    def sortChildren (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Sort Children'
        p = c.currentPosition()
        if not p or not p.hasChildren(): return
    
        c.beginUpdate()
        try: # In update
            c.endEditing()
            u.beforeChangeGroup(p,undoType)
            c.sortChildrenHelper(p)
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            c.setChanged(True)
            u.afterChangeGroup(p,undoType,dirtyVnodeList=dirtyVnodeList)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20050415134809:c.sortChildren
    #@+node:ekr.20040303175026.12:c.sortChildrenHelper
    def sortChildrenHelper (self,p):
        
        c = self ; u = c.undoer
    
        # Create a list of tuples sorted on headlines.
        pairs = [(child.headString().lower(),child.copy()) for child in p.children_iter()]
        pairs.sort()
    
        # Move the children.
        index = 0
        for headline,child in pairs:
            undoData = u.beforeMoveNode(child)
            child.moveToNthChildOf(p,index)
            u.afterMoveNode(child,'Sort',undoData)
            index += 1
    #@nonl
    #@-node:ekr.20040303175026.12:c.sortChildrenHelper
    #@+node:ekr.20050415134809.1:c.sortSiblings
    def sortSiblings (self,event=None):
        
        c = self ; u = c.undoer ; undoType = 'Sort Siblings'
        p = c.currentPosition()
        if not p: return
    
        parent = p.parent()
        if not parent:
            c.sortTopLevel()
        else:
            c.beginUpdate()
            try: # In update...
                c.endEditing()
                u.beforeChangeGroup(p,undoType)
                c.sortChildrenHelper(parent)
                dirtyVnodeList = parent.setAllAncestorAtFileNodesDirty()
                c.setChanged(True)
                u.afterChangeGroup(p,'Sort Siblings',dirtyVnodeList=dirtyVnodeList)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20050415134809.1:c.sortSiblings
    #@+node:ekr.20031218072017.2896:c.sortTopLevel
    def sortTopLevel (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Sort Siblings'
        root = c.rootPosition()
        if not root: return
    
        # Create a list of tuples sorted by headlines.
        pairs = [(p.headString().lower(),p.copy())
            for p in root.self_and_siblings_iter()]
        pairs.sort()
     
        c.beginUpdate()
        try: # In update...
            dirtyVnodeList = []
            u.beforeChangeGroup(root,undoType)
            if 1: # In group...
                h,p = pairs[0]
                if p != root:
                    undoData = u.beforeMoveNode(p)
                    dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                    dirtyVnodeList.extend(dirtyVnodeList2)
                    p.moveToRoot(oldRoot=root)
                    dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                    dirtyVnodeList.extend(dirtyVnodeList2)
                    u.afterMoveNode(p,'Sort',undoData)
                for h,next in pairs[1:]:
                    undoData = u.beforeMoveNode(next)
                    next.moveAfter(p)
                    u.afterMoveNode(next,'Sort',undoData)
                    p = next
            u.afterChangeGroup(root,undoType,dirtyVnodeList=dirtyVnodeList)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2896:c.sortTopLevel
    #@-node:ekr.20031218072017.2895: Top Level... (Commands)
    #@+node:ekr.20040711135959.2:Check Outline submenu...
    #@+node:ekr.20031218072017.2072:c.checkOutline
    def checkOutline (self,event=None,verbose=True,unittest=False,full=True):
        
        """Report any possible clone errors in the outline.
        
        Remove any unused tnodeLists."""
        
        c = self ; count = 1 ; errors = 0
        isTkinter = g.app.gui and g.app.gui.guiName() == "tkinter"
    
        if full and not unittest:
            g.es("all tests enabled: this may take awhile",color="blue")
    
        p = c.rootPosition()
        #@    << assert equivalence of lastVisible methods >>
        #@+node:ekr.20040314062338:<< assert equivalence of lastVisible methods >>
        if 0:
            g.app.debug = True
        
            p1 = p.oldLastVisible()
            p2 = p.lastVisible()
            
            if p1 != p2:
                print "oldLastVisible",p1
                print "   lastVisible",p2
            
            assert p1 and p2 and p1 == p2, "oldLastVisible==lastVisible"
            assert p1.isVisible() and p2.isVisible(), "p1.isVisible() and p2.isVisible()"
            
            g.app.debug = False
        #@nonl
        #@-node:ekr.20040314062338:<< assert equivalence of lastVisible methods >>
        #@nl
        for p in c.allNodes_iter():
            try:
                count += 1
                #@            << remove unused tnodeList >>
                #@+node:ekr.20040313150633:<< remove unused tnodeList >>
                # Empty tnodeLists are not errors.
                v = p.v
                
                # New in 4.2: tnode list is in tnode.
                if hasattr(v.t,"tnodeList") and len(v.t.tnodeList) > 0 and not v.isAnyAtFileNode():
                    if 0:
                        s = "deleting tnodeList for " + repr(v)
                        print ; g.es_print(s,color="blue")
                    delattr(v.t,"tnodeList")
                #@nonl
                #@-node:ekr.20040313150633:<< remove unused tnodeList >>
                #@nl
                if full: # Unit tests usually set this false.
                    #@                << do full tests >>
                    #@+node:ekr.20040323155951:<< do full tests >>
                    if not unittest:
                        if count % 100 == 0:
                            g.es('.',newline=False)
                        if count % 2000 == 0:
                            g.enl()
                    
                    #@+others
                    #@+node:ekr.20040314035615:assert consistency of threadNext & threadBack links
                    threadBack = p.threadBack()
                    threadNext = p.threadNext()
                    
                    if threadBack:
                        assert p == threadBack.threadNext(), "p==threadBack.threadNext"
                    
                    if threadNext:
                        assert p == threadNext.threadBack(), "p==threadNext.threadBack"
                    #@nonl
                    #@-node:ekr.20040314035615:assert consistency of threadNext & threadBack links
                    #@+node:ekr.20040314035615.1:assert consistency of next and back links
                    back = p.back()
                    next = p.next()
                    
                    if back:
                        assert p == back.next(), "p==back.next"
                            
                    if next:
                        assert p == next.back(), "p==next.back"
                    #@nonl
                    #@-node:ekr.20040314035615.1:assert consistency of next and back links
                    #@+node:ekr.20040314035615.2:assert consistency of parent and child links
                    if p.hasParent():
                        n = p.childIndex()
                        assert p == p.parent().moveToNthChild(n), "p==parent.moveToNthChild"
                        
                    for child in p.children_iter():
                        assert p == child.parent(), "p==child.parent"
                    
                    if p.hasNext():
                        assert p.next().parent() == p.parent(), "next.parent==parent"
                        
                    if p.hasBack():
                        assert p.back().parent() == p.parent(), "back.parent==parent"
                    #@nonl
                    #@-node:ekr.20040314035615.2:assert consistency of parent and child links
                    #@+node:ekr.20040323155951.1:assert consistency of directParents and parent
                    if p.hasParent():
                        t = p.parent().v.t
                        for v in p.directParents():
                            try:
                                assert v.t == t
                            except:
                                print "p",p
                                print "p.directParents",p.directParents()
                                print "v",v
                                print "v.t",v.t
                                print "t = p.parent().v.t",t
                                raise AssertionError,"v.t == t"
                    #@-node:ekr.20040323155951.1:assert consistency of directParents and parent
                    #@+node:ekr.20040323161837:assert consistency of p.v.t.vnodeList, & v.parents for cloned nodes
                    if p.isCloned():
                        parents = p.v.t.vnodeList
                        for child in p.children_iter():
                            vparents = child.directParents()
                            assert len(parents) == len(vparents), "len(parents) == len(vparents)"
                            for parent in parents:
                                assert parent in vparents, "parent in vparents"
                            for parent in vparents:
                                assert parent in parents, "parent in parents"
                    #@nonl
                    #@-node:ekr.20040323161837:assert consistency of p.v.t.vnodeList, & v.parents for cloned nodes
                    #@+node:ekr.20040323162707:assert that clones actually share subtrees
                    if p.isCloned() and p.hasChildren():
                        childv = p.firstChild().v
                        assert childv == p.v.t._firstChild, "childv == p.v.t._firstChild"
                        assert id(childv) == id(p.v.t._firstChild), "id(childv) == id(p.v.t._firstChild)"
                        for v in p.v.t.vnodeList:
                            assert v.t._firstChild == childv, "v.t._firstChild == childv"
                            assert id(v.t._firstChild) == id(childv), "id(v.t._firstChild) == id(childv)"
                    #@nonl
                    #@-node:ekr.20040323162707:assert that clones actually share subtrees
                    #@+node:ekr.20040314043623:assert consistency of vnodeList
                    vnodeList = p.v.t.vnodeList
                        
                    for v in vnodeList:
                        
                        try:
                            assert v.t == p.v.t
                        except AssertionError:
                            print "p",p
                            print "v",v
                            print "p.v",p.v
                            print "v.t",v.t
                            print "p.v.t",p.v.t
                            raise AssertionError, "v.t == p.v.t"
                    
                        if p.v.isCloned():
                            assert v.isCloned(), "v.isCloned"
                            assert len(vnodeList) > 1, "len(vnodeList) > 1"
                        else:
                            assert not v.isCloned(), "not v.isCloned"
                            assert len(vnodeList) == 1, "len(vnodeList) == 1"
                    #@nonl
                    #@-node:ekr.20040314043623:assert consistency of vnodeList
                    #@+node:ekr.20040731053740:assert that p.headString() matches p.edit_text.get
                    # Not a great test: it only tests visible nodes.
                    # This test may fail if a joined node is being editred.
                    
                    if isTkinter:
                        t = p.edit_widget()
                        if t:
                            s = t.get("1.0","end")
                            assert p.headString().strip() == s.strip(), "May fail if joined node is being edited"
                    #@nonl
                    #@-node:ekr.20040731053740:assert that p.headString() matches p.edit_text.get
                    #@-others
                    #@nonl
                    #@-node:ekr.20040323155951:<< do full tests >>
                    #@nl
            except AssertionError,message:
                errors += 1
                #@            << give test failed message >>
                #@+node:ekr.20040314044652:<< give test failed message >>
                s = "test failed: %s %s" % (message,repr(p))
                print s ; g.es_print(s,color="red")
                #@nonl
                #@-node:ekr.20040314044652:<< give test failed message >>
                #@nl
        if verbose or not unittest:
            #@        << print summary message >>
            #@+node:ekr.20040314043900:<<print summary message >>
            if full:
                print
                g.enl()
            
            s = "%d nodes checked, %d errors" % (count,errors)
            if errors or verbose:
                g.es_print(s,color="red")
            elif verbose:
                g.es(s,color="green")
            #@nonl
            #@-node:ekr.20040314043900:<<print summary message >>
            #@nl
        return errors
    #@nonl
    #@-node:ekr.20031218072017.2072:c.checkOutline
    #@+node:ekr.20040723094220:Check Outline commands & allies
    #@+node:ekr.20040723094220.1:checkAllPythonCode
    def checkAllPythonCode(self,event=None,unittest=False,ignoreAtIgnore=True):
        
        c = self ; count = 0 ; result = "ok"
    
        for p in c.all_positions_iter():
            
            count += 1
            if not unittest:
                #@            << print dots >>
                #@+node:ekr.20040723094220.2:<< print dots >>
                if count % 100 == 0:
                    g.es('.',newline=False)
                
                if count % 2000 == 0:
                    g.enl()
                #@nonl
                #@-node:ekr.20040723094220.2:<< print dots >>
                #@nl
    
            if g.scanForAtLanguage(c,p) == "python":
                if not g.scanForAtSettings(p) and (not ignoreAtIgnore or not g.scanForAtIgnore(c,p)):
                    try:
                        c.checkPythonNode(p,unittest)
                    except (SyntaxError,tokenize.TokenError,tabnanny.NannyNag):
                        result = "error" # Continue to check.
                    except:
                        import traceback ; traceback.print_exc()
                        return "surprise" # abort
                    if unittest and result != "ok":
                        print "Syntax error in %s" % p.cleanHeadString()
                        return result # End the unit test: it has failed.
                
        if not unittest:
            g.es("Check complete",color="blue")
            
        return result
    #@nonl
    #@-node:ekr.20040723094220.1:checkAllPythonCode
    #@+node:ekr.20040723094220.3:checkPythonCode
    def checkPythonCode (self,event=None,unittest=False,ignoreAtIgnore=True,suppressErrors=False):
        
        c = self ; count = 0 ; result = "ok"
        
        if not unittest:
            g.es("checking Python code   ")
        
        for p in c.currentPosition().self_and_subtree_iter():
            
            count += 1
            if not unittest:
                #@            << print dots >>
                #@+node:ekr.20040723094220.4:<< print dots >>
                if count % 100 == 0:
                    g.es('.',newline=False)
                
                if count % 2000 == 0:
                    g.enl()
                #@nonl
                #@-node:ekr.20040723094220.4:<< print dots >>
                #@nl
    
            if g.scanForAtLanguage(c,p) == "python":
                if not ignoreAtIgnore or not g.scanForAtIgnore(c,p):
                    try:
                        c.checkPythonNode(p,unittest,suppressErrors)
                    except (parser.ParserError,SyntaxError,tokenize.TokenError,tabnanny.NannyNag):
                        result = "error" # Continue to check.
                    except:
                        g.es("surprise in checkPythonNode")
                        g.es_exception()
                        return "surprise" # abort
    
        if not unittest:
            g.es("Check complete",color="blue")
            
        # We _can_ return a result for unit tests because we aren't using doCommand.
        return result
    #@nonl
    #@-node:ekr.20040723094220.3:checkPythonCode
    #@+node:ekr.20040723094220.5:checkPythonNode
    def checkPythonNode (self,p,unittest=False,suppressErrors=False):
    
        c = self
        
        h = p.headString()
        # We must call getScript so that we can ignore directives and section references.
        body = g.getScript(c,p.copy())
        if not body: return
    
        try:
            compiler.parse(body + '\n')
        except (parser.ParserError,SyntaxError):
            if not suppressErrors:
                s = "Syntax error in: %s" % h
                g.es_print(s,color="blue")
            if unittest: raise
            else:
                g.es_exception(full=False,color="black")
                p.setMarked()
    
        c.tabNannyNode(p,h,body,unittest,suppressErrors)
    #@nonl
    #@-node:ekr.20040723094220.5:checkPythonNode
    #@+node:ekr.20040723094220.6:tabNannyNode
    # This code is based on tabnanny.check.
    
    def tabNannyNode (self,p,headline,body,unittest=False,suppressErrors=False):
    
        """Check indentation using tabnanny."""
    
        try:
            # readline = g.readLinesGenerator(body).next
            readline = g.readLinesClass(body).next
            tabnanny.process_tokens(tokenize.generate_tokens(readline))
            return
            
        except parser.ParserError, msg:
            if not suppressErrors:
                g.es("ParserError in %s" % headline,color="blue")
                g.es(str(msg))
            
        except tokenize.TokenError, msg:
            if not suppressErrors:
                g.es("TokenError in %s" % headline,color="blue")
                g.es(str(msg))
    
        except tabnanny.NannyNag, nag:
            if not suppressErrors:
                badline = nag.get_lineno()
                line    = nag.get_line()
                message = nag.get_msg()
                g.es("Indentation error in %s, line %d" % (headline, badline),color="blue")
                g.es(message)
                g.es("offending line:\n%s" % repr(str(line))[1:-1])
            
        except:
            g.trace("unexpected exception")
            g.es_exception()
    
        if unittest: raise
        else: p.setMarked()
    #@nonl
    #@-node:ekr.20040723094220.6:tabNannyNode
    #@-node:ekr.20040723094220:Check Outline commands & allies
    #@+node:ekr.20040412060927:c.dumpOutline
    def dumpOutline (self,event=None):
        
        """ Dump all nodes in the outline."""
        
        c = self
    
        for p in c.allNodes_iter():
            p.dump()
    #@nonl
    #@-node:ekr.20040412060927:c.dumpOutline
    #@+node:ekr.20040711135959.1:Pretty Print commands
    #@+node:ekr.20040712053025:prettyPrintAllPythonCode
    def prettyPrintAllPythonCode (self,event=None,dump=False):
    
        c = self ; pp = c.prettyPrinter(c)
    
        for p in c.all_positions_iter():
            
            # Unlike scanDirectives, scanForAtLanguage ignores @comment.
            if g.scanForAtLanguage(c,p) == "python":
    
                pp.prettyPrintNode(p,dump=dump)
                
        pp.endUndo()
    #@nonl
    #@-node:ekr.20040712053025:prettyPrintAllPythonCode
    #@+node:ekr.20040712053025.1:prettyPrintPythonCode
    def prettyPrintPythonCode (self,event=None,p=None,dump=False):
    
        c = self
        
        if p: root = p.copy()
        else: root = c.currentPosition();
        
        pp = c.prettyPrinter(c)
        
        for p in root.self_and_subtree_iter():
            
            # Unlike scanDirectives, scanForAtLanguage ignores @comment.
            if g.scanForAtLanguage(c,p) == "python":
        
                pp.prettyPrintNode(p,dump=dump)
              
        pp.endUndo()
    #@nonl
    #@-node:ekr.20040712053025.1:prettyPrintPythonCode
    #@+node:ekr.20050729211526:prettyPrintPythonNode
    def prettyPrintPythonNode (self,p=None,dump=False):
    
        c = self
        
        if not p:
            p = c.currentPosition()
        
        pp = c.prettyPrinter(c)
    
        # Unlike scanDirectives, scanForAtLanguage ignores @comment.
        if g.scanForAtLanguage(c,p) == "python":
            pp.prettyPrintNode(p,dump=dump)
              
        pp.endUndo()
    #@nonl
    #@-node:ekr.20050729211526:prettyPrintPythonNode
    #@+node:ekr.20040711135244.5:class prettyPrinter
    class prettyPrinter:
        
        #@    @+others
        #@+node:ekr.20040711135244.6:__init__
        def __init__ (self,c):
            
            self.array = []
                # List of strings comprising the line being accumulated.
                # Important: this list never crosses a line.
            self.bracketLevel = 0
            self.c = c
            self.changed = False
            self.dumping = False
            self.erow = self.ecol = 0 # The ending row/col of the token.
            self.lastName = None # The name of the previous token type.
            self.line = 0 # Same as self.srow
            self.lineParenLevel = 0
            self.lines = [] # List of lines.
            self.name = None
            self.p = c.currentPosition()
            self.parenLevel = 0
            self.prevName = None
            self.s = None # The string containing the line.
            self.squareBracketLevel = 0
            self.srow = self.scol = 0 # The starting row/col of the token.
            self.startline = True # True: the token starts a line.
            self.tracing = False
            #@    << define dispatch dict >>
            #@+node:ekr.20041021100850:<< define dispatch dict >>
            self.dispatchDict = {
                
                "comment":    self.doMultiLine,
                "dedent":     self.doDedent,
                "endmarker":  self.doEndMarker,
                "errortoken": self.doErrorToken,
                "indent":     self.doIndent,
                "name":       self.doName,
                "newline":    self.doNewline,
                "nl" :        self.doNewline,
                "number":     self.doNumber,
                "op":         self.doOp,
                "string":     self.doMultiLine,
            }
            #@nonl
            #@-node:ekr.20041021100850:<< define dispatch dict >>
            #@nl
        #@nonl
        #@-node:ekr.20040711135244.6:__init__
        #@+node:ekr.20040713093048:clear
        def clear (self):
            self.lines = []
        #@nonl
        #@-node:ekr.20040713093048:clear
        #@+node:ekr.20040713064323:dumpLines
        def dumpLines (self,p,lines):
        
            encoding = g.app.tkEncoding
            
            print ; print '-'*10, p.cleanHeadString()
        
            if 0:
                for line in lines:
                    line2 = g.toEncodedString(line,encoding,reportErrors=True)
                    print line2, # Don't add a trailing newline!
            else:
                for i in xrange(len(lines)):
                    line = lines[i]
                    line = g.toEncodedString(line,encoding,reportErrors=True)
                    print "%3d" % i, repr(lines[i])
        #@nonl
        #@-node:ekr.20040713064323:dumpLines
        #@+node:ekr.20040711135244.7:dumpToken
        def dumpToken (self,token5tuple):
        
            t1,t2,t3,t4,t5 = token5tuple
            srow,scol = t3 ; erow,ecol = t4
            line = str(t5) # can fail
            name = token.tok_name[t1].lower()
            val = str(t2) # can fail
        
            startLine = self.line != srow
            if startLine:
                print "----- line",srow,repr(line)
            self.line = srow
        
            print "%10s (%2d,%2d) %-8s" % (name,scol,ecol,repr(val))
        #@nonl
        #@-node:ekr.20040711135244.7:dumpToken
        #@+node:ekr.20040713091855:endUndo
        def endUndo (self):
            
            c = self.c ; u = c.undoer ; undoType = 'Pretty Print'
            current = c.currentPosition()
            
            if self.changed:
                # Tag the end of the command.
                u.afterChangeGroup(current,undoType,dirtyVnodeList=self.dirtyVnodeList)
        #@nonl
        #@-node:ekr.20040713091855:endUndo
        #@+node:ekr.20040711135244.8:get
        def get (self):
            
            if self.lastName != 'newline' and self.lines:
                # Strip the trailing whitespace from the last line.
                self.lines[-1] = self.lines[-1].rstrip()
            
            return self.lines
        #@nonl
        #@-node:ekr.20040711135244.8:get
        #@+node:ekr.20040711135244.4:prettyPrintNode
        def prettyPrintNode(self,p,dump):
        
            c = self.c
            h = p.headString()
            s = p.bodyString()
            if not s: return
            
            readlines = g.readLinesGenerator(s).next
        
            try:
                self.clear()
                for token5tuple in tokenize.generate_tokens(readlines):
                    self.putToken(token5tuple)
                lines = self.get()
        
            except tokenize.TokenError:
                g.es("Error pretty-printing %s.  Not changed." % h, color="blue")
                return
        
            if dump:
                self.dumpLines(p,lines)
            else:
                self.replaceBody(p,lines)
        #@nonl
        #@-node:ekr.20040711135244.4:prettyPrintNode
        #@+node:ekr.20040711135244.9:put
        def put (self,s,strip=True):
            
            """Put s to self.array, and strip trailing whitespace if strip is True."""
            
            if self.array and strip:
                prev = self.array[-1]
                if len(self.array) == 1:
                    if prev.rstrip():
                        # Stripping trailing whitespace doesn't strip leading whitespace.
                        self.array[-1] = prev.rstrip()
                else:
                    # The previous entry isn't leading whitespace, so we can strip whitespace.
                    self.array[-1] = prev.rstrip()
        
            self.array.append(s)
        #@nonl
        #@-node:ekr.20040711135244.9:put
        #@+node:ekr.20041021104237:putArray
        def putArray (self):
            
            """Add the next text by joining all the strings is self.array"""
            
            self.lines.append(''.join(self.array))
            self.array = []
            self.lineParenLevel = 0
        #@nonl
        #@-node:ekr.20041021104237:putArray
        #@+node:ekr.20040711135244.10:putNormalToken & allies
        def putNormalToken (self,token5tuple):
        
            t1,t2,t3,t4,t5 = token5tuple
            self.name = token.tok_name[t1].lower() # The token type
            self.val = t2  # the token string
            self.srow,self.scol = t3 # row & col where the token begins in the source.
            self.erow,self.ecol = t4 # row & col where the token ends in the source.
            self.s = t5 # The line containing the token.
            self.startLine = self.line != self.srow
            self.line = self.srow
        
            if self.startLine:
                self.doStartLine()
        
            f = self.dispatchDict.get(self.name,self.oops)
            self.trace()
            f()
            self.lastName = self.name
        #@nonl
        #@+node:ekr.20041021102938:doEndMarker
        def doEndMarker (self):
            
            self.putArray()
        #@nonl
        #@-node:ekr.20041021102938:doEndMarker
        #@+node:ekr.20041021102340.1:doErrorToken
        def doErrorToken (self):
            
            self.array.append(self.val)
        
            # This code is executed for versions of Python earlier than 2.4
            if self.val == '@':
                # Preserve whitespace after @.
                i = g.skip_ws(self.s,self.scol+1)
                ws = self.s[self.scol+1:i]
                if ws:
                    self.array.append(ws)
        #@nonl
        #@-node:ekr.20041021102340.1:doErrorToken
        #@+node:ekr.20041021102340.2:doIndent & doDedent
        def doDedent (self):
            
            pass
            
        def doIndent (self):
            
            self.array.append(self.val)
        #@-node:ekr.20041021102340.2:doIndent & doDedent
        #@+node:ekr.20041021102340:doMultiLine (strings, etc).
        def doMultiLine (self):
        
            # Ensure a blank before comments not preceded entirely by whitespace.
            
            if self.val.startswith('#') and self.array:
                prev = self.array[-1]
                if prev and prev[-1] != ' ':
                    self.put(' ') 
        
            # These may span lines, so duplicate the end-of-line logic.
            lines = g.splitLines(self.val)
            for line in lines:
                self.array.append(line)
                if line and line[-1] == '\n':
                    self.putArray()
            
            # Add a blank after the string if there is something in the last line.
            if self.array:
                line = self.array[-1]
                if line.strip():
                    self.put(' ')
                    
            # Suppress start-of-line logic.
            self.line = self.erow
        #@nonl
        #@-node:ekr.20041021102340:doMultiLine (strings, etc).
        #@+node:ekr.20041021101911.5:doName
        def doName(self):
            
            # Ensure whitespace or start-of-line precedes the name.
            if self.array:
                last = self.array[-1]
                ch = last[-1]
                outer = self.parenLevel == 0 and self.squareBracketLevel == 0
                chars = '@ \t{([.'
                if not outer: chars += ',=<>*-+&|/'
                if ch not in chars:
                    self.array.append(' ')
        
            self.array.append("%s " % self.val)
        
            if self.prevName == "def": # A personal idiosyncracy.
                self.array.append(' ') # Retain the blank before '('.
        
            self.prevName = self.val
        #@nonl
        #@-node:ekr.20041021101911.5:doName
        #@+node:ekr.20041021101911.3:doNewline
        def doNewline (self):
        
            # Remove trailing whitespace.
            # This never removes trailing whitespace from multi-line tokens.
            if self.array:
                self.array[-1] = self.array[-1].rstrip()
        
            self.array.append('\n')
            self.putArray()
        #@nonl
        #@-node:ekr.20041021101911.3:doNewline
        #@+node:ekr.20041021101911.6:doNumber
        def doNumber (self):
        
            self.array.append(self.val)
        #@-node:ekr.20041021101911.6:doNumber
        #@+node:ekr.20040711135244.11:doOp
        def doOp (self):
            
            val = self.val
            outer = self.lineParenLevel <= 0 or (self.parenLevel == 0 and self.squareBracketLevel == 0)
            # New in Python 2.4: '@' is an operator, not an error token.
            if self.val == '@':
                self.array.append(self.val)
                # Preserve whitespace after @.
                i = g.skip_ws(self.s,self.scol+1)
                ws = self.s[self.scol+1:i]
                if ws: self.array.append(ws)
            elif val == '(':
                # Nothing added; strip leading blank before function calls but not before Python keywords.
                strip = self.lastName=='name' and not keyword.iskeyword(self.prevName)
                self.put('(',strip=strip)
                self.parenLevel += 1 ; self.lineParenLevel += 1
            elif val in ('=','==','+=','-=','!=','<=','>=','<','>','<>','*','**','+','&','|','/','//'):
                # Add leading and trailing blank in outer mode.
                s = g.choose(outer,' %s ','%s')
                self.put(s % val)
            elif val in ('^','~','{','['):
                # Add leading blank in outer mode.
                s = g.choose(outer,' %s','%s')
                self.put(s % val)
                if val == '[': self.squareBracketLevel += 1
            elif val in (',',':','}',']',')'):
                # Add trailing blank in outer mode.
                s = g.choose(outer,'%s ','%s')
                self.put(s % val)
                if val == ']': self.squareBracketLevel -= 1
                if val == ')':
                    self.parenLevel -= 1 ; self.lineParenLevel -= 1
            # ----- no difference between outer and inner modes ---
            elif val in (';','%'):
                # Add leading and trailing blank.
                self.put(' %s ' % val)
            elif val == '>>':
                # Add leading blank.
                self.put(' %s' % val)
            elif val == '<<':
                # Add trailing blank.
                self.put('%s ' % val)
            elif val in ('-'):
                # Could be binary or unary.  Or could be a hyphen in a section name.
                # Add preceding blank only for non-id's.
                if outer:
                    if self.array:
                        prev = self.array[-1].rstrip()
                        if prev and prev[-1] not in string.digits + string.letters:
                            self.put(' %s' % val)
                        else: self.put(val)
                    else: self.put(val) # Try to leave whitespace unchanged.
                else:
                    self.put(val)
            else:
                self.put(val)
        #@nonl
        #@-node:ekr.20040711135244.11:doOp
        #@+node:ekr.20041021112219:doStartLine
        def doStartLine (self):
            
            before = self.s[0:self.scol]
            i = g.skip_ws(before,0)
            self.ws = self.s[0:i]
             
            if self.ws:
                self.array.append(self.ws)
        #@nonl
        #@-node:ekr.20041021112219:doStartLine
        #@+node:ekr.20041021101911.1:oops
        def oops(self):
            
            print "unknown PrettyPrinting code: %s" % (self.name)
        #@nonl
        #@-node:ekr.20041021101911.1:oops
        #@+node:ekr.20041021101911.2:trace
        def trace(self):
            
            if self.tracing:
        
                g.trace("%10s: %s" % (
                    self.name,
                    repr(g.toEncodedString(self.val,"utf-8"))
                ))
        #@nonl
        #@-node:ekr.20041021101911.2:trace
        #@-node:ekr.20040711135244.10:putNormalToken & allies
        #@+node:ekr.20040711135244.12:putToken
        def putToken (self,token5tuple):
            
            if self.dumping:
                self.dumpToken(token5tuple)
            else:
                self.putNormalToken(token5tuple)
        #@nonl
        #@-node:ekr.20040711135244.12:putToken
        #@+node:ekr.20040713070356:replaceBody
        def replaceBody (self,p,lines):
            
            c = self.c ; u = c.undoer ; undoType = 'Pretty Print'
            
            sel = c.frame.body.getInsertionPoint()
            oldBody = p.bodyString()
            body = string.join(lines,'')
            
            if oldBody != body:
                if not self.changed:
                    # Start the group.
                    u.beforeChangeGroup(p,undoType)
                    self.changed = True
                    self.dirtyVnodeList = []
                undoData = u.beforeChangeNodeContents(p)
                p.setBodyStringOrPane(body)
                dirtyVnodeList2 = p.setDirty()
                self.dirtyVnodeList.extend(dirtyVnodeList2)
                u.afterChangeNodeContents(p,undoType,undoData,dirtyVnodeList=self.dirtyVnodeList)
            
        #@nonl
        #@-node:ekr.20040713070356:replaceBody
        #@-others
    #@nonl
    #@-node:ekr.20040711135244.5:class prettyPrinter
    #@-node:ekr.20040711135959.1:Pretty Print commands
    #@-node:ekr.20040711135959.2:Check Outline submenu...
    #@+node:ekr.20031218072017.2898:Expand & Contract...
    #@+node:ekr.20031218072017.2899:Commands
    #@+node:ekr.20031218072017.2900:contractAllHeadlines
    def contractAllHeadlines (self,event=None):
    
        c = self
        
        c.beginUpdate()
        try: # update...
            for p in c.allNodes_iter():
                p.contract()
            # Select the topmost ancestor of the presently selected node.
            p = c.currentPosition()
            while p and p.hasParent():
                p.moveToParent()
            c.selectVnode(p)
        finally:
            c.endUpdate()
    
        c.expansionLevel = 1 # Reset expansion level.
    #@nonl
    #@-node:ekr.20031218072017.2900:contractAllHeadlines
    #@+node:ekr.20031218072017.2901:contractNode
    def contractNode (self,event=None):
        
        c = self ; v = c.currentVnode()
        
        c.beginUpdate()
        try:
            v.contract()
        finally:
            c.endUpdate()
    #@-node:ekr.20031218072017.2901:contractNode
    #@+node:ekr.20040930064232:contractNodeOrGoToParent
    def contractNodeOrGoToParent (self,event=None):
        
        """Simulate the left Arrow Key in folder of Windows Explorer."""
    
        c = self ; p = c.currentPosition()
     
        if p.hasChildren() and p.isExpanded():
            c.contractNode()
        elif p.hasParent():
            c.goToParent()
    #@nonl
    #@-node:ekr.20040930064232:contractNodeOrGoToParent
    #@+node:ekr.20031218072017.2902:contractParent
    def contractParent (self,event=None):
        
        c = self ; v = c.currentVnode()
        parent = v.parent()
        if not parent: return
        
        c.beginUpdate()
        try:
            c.selectVnode(parent)
            parent.contract()
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2902:contractParent
    #@+node:ekr.20031218072017.2903:expandAllHeadlines
    def expandAllHeadlines (self,event=None):
    
        c = self ; v = root = c.rootVnode()
        c.beginUpdate()
        try:
            while v:
                c.expandSubtree(v)
                v = v.next()
            c.selectVnode(root)
        finally:
            c.endUpdate()
        c.expansionLevel = 0 # Reset expansion level.
    #@nonl
    #@-node:ekr.20031218072017.2903:expandAllHeadlines
    #@+node:ekr.20031218072017.2904:expandAllSubheads
    def expandAllSubheads (self,event=None):
    
        c = self ; v = c.currentVnode()
        if not v: return
    
        child = v.firstChild()
        c.beginUpdate()
        try:
            c.expandSubtree(v)
            while child:
                c.expandSubtree(child)
                child = child.next()
            c.selectVnode(v)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2904:expandAllSubheads
    #@+node:ekr.20031218072017.2905:expandLevel1..9
    def expandLevel1 (self,event=None): self.expandToLevel(1)
    def expandLevel2 (self,event=None): self.expandToLevel(2)
    def expandLevel3 (self,event=None): self.expandToLevel(3)
    def expandLevel4 (self,event=None): self.expandToLevel(4)
    def expandLevel5 (self,event=None): self.expandToLevel(5)
    def expandLevel6 (self,event=None): self.expandToLevel(6)
    def expandLevel7 (self,event=None): self.expandToLevel(7)
    def expandLevel8 (self,event=None): self.expandToLevel(8)
    def expandLevel9 (self,event=None): self.expandToLevel(9)
    #@-node:ekr.20031218072017.2905:expandLevel1..9
    #@+node:ekr.20031218072017.2906:expandNextLevel
    def expandNextLevel (self,event=None):
    
        c = self ; v = c.currentVnode()
        
        # 1/31/02: Expansion levels are now local to a particular tree.
        if c.expansionNode != v:
            c.expansionLevel = 1
            c.expansionNode = v
            
        self.expandToLevel(c.expansionLevel + 1)
    #@-node:ekr.20031218072017.2906:expandNextLevel
    #@+node:ekr.20031218072017.2907:expandNode
    def expandNode (self,event=None):
        
        c = self ; v = c.currentVnode()
        
        c.beginUpdate()
        try:
            v.expand()
        finally:
            c.endUpdate()
    
    #@-node:ekr.20031218072017.2907:expandNode
    #@+node:ekr.20040930064232.1:expandNodeAnd/OrGoToFirstChild
    def expandNodeAndGoToFirstChild (self,event=None):
        
        """If a node has children, expand it if needed and go to the first child."""
    
        c = self ; p = c.currentPosition()
        if not p.hasChildren():
            return
    
        if not p.isExpanded():
            c.expandNode()
            
        c.beginUpdate()
        try:
            c.selectVnode(p.firstChild())
        finally:
            c.endUpdate()
            
    def expandNodeOrGoToFirstChild (self,event=None):
        
        """Simulate the Right Arrow Key in folder of Windows Explorer."""
    
        c = self ; p = c.currentPosition()
        if not p.hasChildren(): return
    
        if not p.isExpanded():
            c.expandNode()
        else:
            c.beginUpdate()
            try:
                c.selectVnode(p.firstChild())
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20040930064232.1:expandNodeAnd/OrGoToFirstChild
    #@+node:ekr.20031218072017.2908:expandPrevLevel
    def expandPrevLevel (self,event=None):
    
        c = self ; v = c.currentVnode()
        
        # 1/31/02: Expansion levels are now local to a particular tree.
        if c.expansionNode != v:
            c.expansionLevel = 1
            c.expansionNode = v
            
        self.expandToLevel(max(1,c.expansionLevel - 1))
    #@-node:ekr.20031218072017.2908:expandPrevLevel
    #@-node:ekr.20031218072017.2899:Commands
    #@+node:ekr.20031218072017.2909:Utilities
    #@+node:ekr.20031218072017.2910:contractSubtree
    def contractSubtree (self,p):
    
        for p in p.subtree_iter():
            p.contract()
    #@nonl
    #@-node:ekr.20031218072017.2910:contractSubtree
    #@+node:ekr.20031218072017.2911:expandSubtree
    def expandSubtree (self,v):
    
        c = self
        last = v.lastNode()
    
        c.beginUpdate()
        try:
            while v and v != last:
                v.expand()
                v = v.threadNext()
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2911:expandSubtree
    #@+node:ekr.20031218072017.2912:expandToLevel (rewritten in 4.4)
    def expandToLevel (self,level):
    
        c = self
        c.beginUpdate()
        try:
            current = c.currentPosition()
            n = current.level()
            for p in current.self_and_subtree_iter():
                if p.level() - n + 1 < level:
                    p.expand()
                else:
                    p.contract()
            c.expansionLevel = level
            c.expansionNode = c.currentPosition()
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2912:expandToLevel (rewritten in 4.4)
    #@-node:ekr.20031218072017.2909:Utilities
    #@-node:ekr.20031218072017.2898:Expand & Contract...
    #@+node:ekr.20031218072017.2913:Goto
    #@+node:ekr.20031218072017.1628:goNextVisitedNode
    def goNextVisitedNode (self,event=None):
        
        c = self
    
        while c.beadPointer + 1 < len(c.beadList):
            c.beadPointer += 1
            v = c.beadList[c.beadPointer]
            if v.exists(c):
                c.beginUpdate()
                try:
                    c.frame.tree.expandAllAncestors(v)
                    c.selectVnode(v,updateBeadList=False)
                finally:
                    c.endUpdate()
                return
    #@nonl
    #@-node:ekr.20031218072017.1628:goNextVisitedNode
    #@+node:ekr.20031218072017.1627:goPrevVisitedNode
    def goPrevVisitedNode (self,event=None):
        
        c = self
    
        while c.beadPointer > 0:
            c.beadPointer -= 1
            v = c.beadList[c.beadPointer]
            if v.exists(c):
                c.beginUpdate()
                try:
                    c.frame.tree.expandAllAncestors(v)
                    c.selectVnode(v,updateBeadList=False)
                finally:
                    c.endUpdate()
                return
    #@-node:ekr.20031218072017.1627:goPrevVisitedNode
    #@+node:ekr.20031218072017.2914:goToFirstNode
    def goToFirstNode (self,event=None):
        
        c = self
        p = c.rootPosition()
        if p:
            c.beginUpdate()
            try:
                c.selectVnode(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2914:goToFirstNode
    #@+node:ekr.20051012092453:goToFirstSibling (New in 4.4)
    def goToFirstSibling (self,event=None):
        
        c = self ; p = c.currentPosition()
        
        if p.hasBack():
            while p.hasBack():
                p.moveToBack()
    
            c.beginUpdate()
            try:
                c.selectVnode(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20051012092453:goToFirstSibling (New in 4.4)
    #@+node:ekr.20031218072017.2915:goToLastNode (Bug fix in 4.4)
    def goToLastNode (self,event=None):
        
        c = self ; p = c.rootPosition()
        while p and p.hasThreadNext(): # Bug fix: 10/12/05: was p.hasNext.
            p.moveToThreadNext()
    
        if p:
            c.beginUpdate()
            try:
                c.frame.tree.expandAllAncestors(p)
                c.selectVnode(p)
            finally:
                c.endUpdate()
    
    #@-node:ekr.20031218072017.2915:goToLastNode (Bug fix in 4.4)
    #@+node:ekr.20051012092847.1:goToLastSibling (New in 4.4)
    def goToLastSibling (self,event=None):
        
        c = self ; p = c.currentPosition()
        
        if p.hasNext():
            while p.hasNext():
                p.moveToNext()
    
            c.beginUpdate()
            try:
                c.selectVnode(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20051012092847.1:goToLastSibling (New in 4.4)
    #@+node:ekr.20050711153537:goToLastVisibleNode
    def goToLastVisibleNode (self,event=None):
        
        c = self ; p = c.rootPosition()
        
        while p.hasNext():
            p.moveToNext()
            
        while p and p.isExpanded():
            p.moveToLastChild()
    
        if p:
            c.beginUpdate()
            try:
                c.frame.tree.expandAllAncestors(p)
                c.selectVnode(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20050711153537:goToLastVisibleNode
    #@+node:ekr.20031218072017.2916:goToNextClone
    def goToNextClone (self,event=None):
    
        c = self ; current = c.currentVnode()
        if not current: return
        if not current.isCloned(): return
    
        v = current.threadNext()
        while v and v.t != current.t:
            v = v.threadNext()
            
        if not v:
            # Wrap around.
            v = c.rootVnode()
            while v and v != current and v.t != current.t:
                v = v.threadNext()
    
        if v:
            c.beginUpdate()
            try:
                c.endEditing()
                c.selectVnode(v)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2916:goToNextClone
    #@+node:ekr.20031218072017.2917:goToNextDirtyHeadline
    def goToNextDirtyHeadline (self,event=None):
    
        c = self ; p = c.currentPosition()
        if not p: return
    
        p.moveToThreadNext()
        while p and not p.isDirty():
            p.moveToThreadNext()
    
        if not p:
            # Wrap around.
            p = c.rootPosition()
            while p and not p.isDirty():
                p.moveToThreadNext()
    
        if p:
            c.beginUpdate()
            try:
                c.endEditing()
                c.selectPosition(p)
            finally:
                c.endUpdate()
        else:
            g.es("done",color="blue")
    #@nonl
    #@-node:ekr.20031218072017.2917:goToNextDirtyHeadline
    #@+node:ekr.20031218072017.2918:goToNextMarkedHeadline
    def goToNextMarkedHeadline (self,event=None):
    
        c = self ; p = c.currentPosition()
        if not p: return
    
        p.moveToThreadNext()
        while p and not p.isMarked():
            p.moveToThreadNext()
    
        if p:
            c.beginUpdate()
            try:
                c.endEditing()
                c.selectPosition(p)
            finally:
                c.endUpdate()
        else:
            g.es("done",color="blue")
    #@nonl
    #@-node:ekr.20031218072017.2918:goToNextMarkedHeadline
    #@+node:ekr.20031218072017.2919:goToNextSibling
    def goToNextSibling (self,event=None):
        
        c = self
        v = c.currentVnode()
        if not v: return
        next = v.next()
        if next:
            c.beginUpdate()
            try:
                c.selectVnode(next)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2919:goToNextSibling
    #@+node:ekr.20031218072017.2920:goToParent
    def goToParent (self,event=None):
        
        c = self
        v = c.currentVnode()
        if not v: return
        p = v.parent()
        if p:
            c.beginUpdate()
            try:
                c.selectVnode(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2920:goToParent
    #@+node:ekr.20031218072017.2921:goToPrevSibling
    def goToPrevSibling (self,event=None):
        
        c = self
        v = c.currentVnode()
        if not v: return
        back = v.back()
        if back:
            c.beginUpdate()
            try:
                c.selectVnode(back)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2921:goToPrevSibling
    #@+node:ekr.20031218072017.2994:selectThreadNext
    def selectThreadNext (self,event=None):
    
        c = self ; current = c.currentPosition()
        if not current: return
    
        p = current.threadNext()
        if p:
            c.beginUpdate()
            try:
                c.selectPosition(p)
            finally:
                c.endUpdate()
            c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20031218072017.2994:selectThreadNext
    #@+node:ekr.20031218072017.2993:selectThreadBack
    def selectThreadBack (self,event=None):
    
        c = self ; current = c.currentVnode()
        if not current: return
        
        v = current.threadBack()
        if v:
            c.beginUpdate()
            try:
                c.selectVnode(v)
            finally:
                c.endUpdate()
    #@-node:ekr.20031218072017.2993:selectThreadBack
    #@+node:ekr.20031218072017.2995:selectVisBack
    # This has an up arrow for a control key.
    
    def selectVisBack (self,event=None):
    
        c = self ; current = c.currentVnode()
        if not current: return
    
        v = current.visBack()
        if v:
            c.beginUpdate()
            try:
                c.selectVnode(v)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2995:selectVisBack
    #@+node:ekr.20031218072017.2996:selectVisNext
    def selectVisNext (self,event=None):
    
        c = self ; current = c.currentVnode()
        if not current: return
        
        v = current.visNext()
        if v:
            c.beginUpdate()
            try:
                c.selectVnode(v)
            finally:
                c.endUpdate()
    #@-node:ekr.20031218072017.2996:selectVisNext
    #@-node:ekr.20031218072017.2913:Goto
    #@+node:ekr.20031218072017.2922:Mark...
    #@+node:ekr.20031218072017.2923:markChangedHeadlines
    def markChangedHeadlines (self,event=None): 
    
        c = self ; u = c.undoer ; undoType = 'Mark Changed'
        current = c.currentPosition()
        
        c.beginUpdate()
        try:
            u.beforeChangeGroup(current,undoType)
            for p in c.allNodes_iter():
                if p.isDirty()and not p.isMarked():
                    bunch = u.beforeMark(p,undoType)
                    p.setMarked()
                    c.setChanged(True)
                    u.afterMark(p,undoType,bunch)
            u.afterChangeGroup(current,undoType)
            g.es("done",color="blue")
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2923:markChangedHeadlines
    #@+node:ekr.20031218072017.2924:markChangedRoots
    def markChangedRoots (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Mark Changed'
        current = c.currentPosition()
    
        c.beginUpdate()
        try:
            u.beforeChangeGroup(current,undoType)
            for p in c.allNodes_iter():
                if p.isDirty()and not p.isMarked():
                    s = p.bodyString()
                    flag, i = g.is_special(s,0,"@root")
                    if flag:
                        bunch = u.beforeMark(p,undoType)
                        p.setMarked()
                        c.setChanged(True)
                        u.afterMark(p,undoType,bunch)
            u.afterChangeGroup(current,undoType)
            g.es("done",color="blue")
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2924:markChangedRoots
    #@+node:ekr.20031218072017.2925:markAllAtFileNodesDirty (not used)
    def markAllAtFileNodesDirty (self,event=None):
    
        c = self ; p = c.rootPosition()
    
        c.beginUpdate()
        try: # In update...
            while p:
                if p.isAtFileNode()and not p.isDirty():
                    p.setDirty()
                    c.setChanged(True)
                    p.moveToNodeAfterTree()
                else:
                    p.moveToThreadNext()
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2925:markAllAtFileNodesDirty (not used)
    #@+node:ekr.20031218072017.2926:markAtFileNodesDirty (not used)
    def markAtFileNodesDirty (self,event=None):
    
        c = self
        p = c.currentPosition()
        if not p: return
    
        after = p.nodeAfterTree()
        c.beginUpdate()
        try: # In update...
            while p and p != after:
                if p.isAtFileNode() and not p.isDirty():
                    p.setDirty()
                    c.setChanged(True)
                    p.moveToNodeAfterTree()
                else:
                    p.moveToThreadNext()
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2926:markAtFileNodesDirty (not used)
    #@+node:ekr.20031218072017.2927:markClones
    def markClones (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Mark Clones'
        current = c.currentPosition()
        if not current or not current.isCloned():
            g.es('The current node is not a clone',color='blue')
            return
    
        c.beginUpdate()
        u.beforeChangeGroup(current,undoType)
        try: # In update...
            dirtyVnodeList = []
            for p in c.allNodes_iter():
                if p.v.t == current.v.t:
                    bunch = u.beforeMark(p,undoType)
                    p.setMarked()
                    c.setChanged(True)
                    dirtyVnodeList2 = p.setDirty()
                    dirtyVnodeList.extend(dirtyVnodeList2)
                    u.afterMark(p,undoType,bunch)
        finally:
            u.afterChangeGroup(current,undoType,dirtyVnodeList=dirtyVnodeList)
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2927:markClones
    #@+node:ekr.20031218072017.2928:markHeadline
    def markHeadline (self,event=None):
    
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
    
        c.beginUpdate()
        try: # In update...
            undoType = g.choose(p.isMarked(),'Unmark','Mark')
            bunch = u.beforeMark(p,undoType)
            if p.isMarked():
                p.clearMarked()
            else:
                p.setMarked()
            dirtyVnodeList = p.setDirty()
            c.setChanged(True)
            u.afterMark(p,undoType,bunch,dirtyVnodeList=dirtyVnodeList)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2928:markHeadline
    #@+node:ekr.20031218072017.2929:markSubheads
    def markSubheads (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Mark Subheads'
        current = c.currentPosition()
        if not current: return
    
        c.beginUpdate()
        u.beforeChangeGroup(current,undoType)
        try: # In update...
            dirtyVnodeList = []
            for p in current.children_iter():
                if not p.isMarked():
                    bunch = u.beforeMark(p,undoType)
                    p.setMarked()
                    dirtyVnodeList2 = p.setDirty()
                    dirtyVnodeList.extend(dirtyVnodeList2)
                    c.setChanged(True)
                    u.afterMark(p,undoType,bunch)
        finally:
            u.afterChangeGroup(current,undoType,dirtyVnodeList=dirtyVnodeList)
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2929:markSubheads
    #@+node:ekr.20031218072017.2930:unmarkAll
    def unmarkAll (self,event=None):
    
        c = self ; u = c.undoer ; undoType = 'Unmark All'
        current = c.currentPosition()
        if not current: return
        
        c.beginUpdate()
        u.beforeChangeGroup(current,undoType)
        try: # In update...
            dirtyVnodeList = []
            for p in c.allNodes_iter():
                if p.isMarked():
                    bunch = u.beforeMark(p,undoType)
                    p.clearMarked()
                    dirtyVnodeList2 = p.setDirty()
                    dirtyVnodeList.extend(dirtyVnodeList2)
                    c.setChanged(True)
                    u.afterMark(p,undoType,bunch)
        finally:
            u.afterChangeGroup(current,undoType,dirtyVnodeList=dirtyVnodeList)
            c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.2930:unmarkAll
    #@-node:ekr.20031218072017.2922:Mark...
    #@+node:ekr.20031218072017.1766:Move... (Commands)
    #@+node:ekr.20031218072017.1767:demote
    def demote (self,event=None):
    
        c = self ; u = c.undoer
        current = c.currentPosition()
        command = 'Demote'
        if not current or not current.hasNext(): return
    
        # Make sure all the moves will be valid.
        for child in current.children_iter():
            if not c.checkMoveWithParentWithWarning(child,current,True):
                return
        c.beginUpdate()
        try: # update...
            c.endEditing()
            u.beforeChangeGroup(current,command)
            p = current.copy()
            while p.hasNext(): # Do not use iterator here.
                child = p.next()
                undoData = u.beforeMoveNode(child)
                child.moveToNthChildOf(p,p.numberOfChildren())
                u.afterMoveNode(child,command,undoData)
            p.expand()
            # Even if p is an @ignore node there is no need to mark the demoted children dirty.
            dirtyVnodeList = current.setAllAncestorAtFileNodesDirty()
            c.setChanged(True)
            u.afterChangeGroup(current,command,dirtyVnodeList=dirtyVnodeList)
            c.selectPosition(current)
        finally:
            c.endUpdate(scroll=True)
        c.updateSyntaxColorer(current) # Moving can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.1767:demote
    #@+node:ekr.20031218072017.1768:moveOutlineDown
    #@+at 
    #@nonl
    # Moving down is more tricky than moving up; we can't move p to be a child 
    # of itself.  An important optimization:  we don't have to call 
    # checkMoveWithParentWithWarning() if the parent of the moved node remains 
    # the same.
    #@-at
    #@@c
    
    def moveOutlineDown (self,event=None):
    
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
    
        if not c.canMoveOutlineDown(): # 11/4/03: Support for hoist.
            if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
            return
            
        inAtIgnoreRange = p.inAtIgnoreRange()
        # Set next to the node after which p will be moved.
        next = p.visNext()
        while next and p.isAncestorOf(next):
            next = next.visNext()
        if not next: return
        c.beginUpdate()
        try: # update...
            c.endEditing()
            undoData = u.beforeMoveNode(p)
            #@        << Move p down & set moved if successful >>
            #@+node:ekr.20031218072017.1769:<< Move p down & set moved if successful >>
            if next.hasChildren() and next.isExpanded():
                # Attempt to move p to the first child of next.
                moved = c.checkMoveWithParentWithWarning(p,next,True)
                if moved:
                    dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
                    p.moveToNthChildOf(next,0)
                    
            else:
                # Attempt to move p after next.
                moved = c.checkMoveWithParentWithWarning(p,next.parent(),True)
                if moved:
                    dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
                    p.moveAfter(next)
            #@nonl
            #@-node:ekr.20031218072017.1769:<< Move p down & set moved if successful >>
            #@nl
            if moved:
                if inAtIgnoreRange and not p.inAtIgnoreRange():
                    # The moved nodes have just become newly unignored.
                    p.setDirty() # Mark descendent @thin nodes dirty.
                else: # No need to mark descendents dirty.
                    dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                    dirtyVnodeList.extend(dirtyVnodeList2)
                c.setChanged(True)
                u.afterMoveNode(p,'Move Down',undoData,dirtyVnodeList)
                c.selectPosition(p)
        finally:
            c.endUpdate(scroll=True)
        c.updateSyntaxColorer(p) # Moving can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.1768:moveOutlineDown
    #@+node:ekr.20031218072017.1770:moveOutlineLeft
    def moveOutlineLeft (self,event=None):
        
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
        if not c.canMoveOutlineLeft(): # 11/4/03: Support for hoist.
            if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
            return
        if not p.hasParent(): return
    
        inAtIgnoreRange = p.inAtIgnoreRange()
        parent = p.parent()
        c.beginUpdate()
        try: # In update...
            c.endEditing()
            undoData = u.beforeMoveNode(p)
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            p.moveAfter(parent)
            if inAtIgnoreRange and not p.inAtIgnoreRange():
                # The moved nodes have just become newly unignored.
                p.setDirty() # Mark descendent @thin nodes dirty.
            else: # No need to mark descendents dirty.
                dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                dirtyVnodeList.extend(dirtyVnodeList2)
            c.setChanged(True)
            u.afterMoveNode(p,'Move Left',undoData,dirtyVnodeList)
            c.selectPosition(p)
        finally:
            c.endUpdate(scroll=True)
        c.updateSyntaxColorer(p) # Moving can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.1770:moveOutlineLeft
    #@+node:ekr.20031218072017.1771:moveOutlineRight
    def moveOutlineRight (self,event=None):
        
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
        if not c.canMoveOutlineRight(): # 11/4/03: Support for hoist.
            if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
            return
        if not p.hasBack: return
        back = p.back()
        if not c.checkMoveWithParentWithWarning(p,back,True): return
    
        c.beginUpdate()
        try: # update...
            c.endEditing()
            undoData = u.beforeMoveNode(p)
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            n = back.numberOfChildren()
            p.moveToNthChildOf(back,n)
            # g.trace(p,p.parent())
            # Moving an outline right can never bring it outside the range of @ignore.
            dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
            dirtyVnodeList.extend(dirtyVnodeList2)
            c.setChanged(True)
            u.afterMoveNode(p,'Move Right',undoData,dirtyVnodeList)
            c.selectPosition(p)
        finally:
            c.endUpdate(scroll=True)
        c.updateSyntaxColorer(p) # Moving can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.1771:moveOutlineRight
    #@+node:ekr.20031218072017.1772:moveOutlineUp
    def moveOutlineUp (self,event=None):
    
        c = self ; u = c.undoer ; p = c.currentPosition()
        if not p: return
        if not c.canMoveOutlineUp(): # Support for hoist.
            if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
            return
        back = p.visBack()
        if not back: return
        inAtIgnoreRange = p.inAtIgnoreRange()
        back2 = back.visBack()
        if back2 and p.v in back2.v.t.vnodeList:
            # A weird special case: just select back2.
            c.selectPosition(back2)
            return
    
        c.beginUpdate()
        try: # update...
            c.endEditing()
            undoData = u.beforeMoveNode(p)
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            #@        << Move p up >>
            #@+node:ekr.20031218072017.1773:<< Move p up >>
            if 0:
                g.trace("visBack",back)
                g.trace("visBack2",back2)
                g.trace("oldParent",oldParent)
                g.trace("back2.hasChildren",back2.hasChildren())
                g.trace("back2.isExpanded",back2.isExpanded())
            
            if not back2:
                # p will be the new root node
                moved = True
                p.moveToRoot(c.rootPosition())
            
            elif back2.hasChildren() and back2.isExpanded():
                if c.checkMoveWithParentWithWarning(p,back2,True):
                    moved = True
                    p.moveToNthChildOf(back2,0)
            
            else:
                if c.checkMoveWithParentWithWarning(p,back2.parent(),True):
                    moved = True
                    p.moveAfter(back2)
            #@nonl
            #@-node:ekr.20031218072017.1773:<< Move p up >>
            #@nl
            if moved:
                if inAtIgnoreRange and not p.inAtIgnoreRange():
                    # The moved nodes have just become newly unignored.
                    dirtyVnodeList2 = p.setDirty() # Mark descendent @thin nodes dirty.
                else: # No need to mark descendents dirty.
                    dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                dirtyVnodeList.extend(dirtyVnodeList2)
                c.setChanged(True)
                u.afterMoveNode(p,'Move Right',undoData,dirtyVnodeList)
                c.selectPosition(p)
        finally:
            c.endUpdate(scroll=True)
        c.updateSyntaxColorer(p) # Moving can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.1772:moveOutlineUp
    #@+node:ekr.20031218072017.1774:promote
    def promote (self,event=None):
    
        c = self ; u = c.undoer ; p = c.currentPosition()
        command = 'Promote'
        if not p or not p.hasChildren(): return
    
        isAtIgnoreNode = p.isAtIgnoreNode()
        inAtIgnoreRange = p.inAtIgnoreRange()
        c.beginUpdate()
        try: # In update...
            c.endEditing()
            u.beforeChangeGroup(p,command)
            after = p
            while p.hasChildren(): # Don't use an iterator.
                child = p.firstChild()
                undoData = u.beforeMoveNode(child)
                child.moveAfter(after)
                after = child
                u.afterMoveNode(child,command,undoData)
            c.setChanged(True)
            if not inAtIgnoreRange and isAtIgnoreNode:
                # The promoted nodes have just become newly unignored.
                dirtyVnodeList = p.setDirty() # Mark descendent @thin nodes dirty.
            else: # No need to mark descendents dirty.
                dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            u.afterChangeGroup(p,command,dirtyVnodeList=dirtyVnodeList)
            c.selectPosition(p)
        finally:
            c.endUpdate(scroll=True)
        c.updateSyntaxColorer(p) # Moving can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.1774:promote
    #@-node:ekr.20031218072017.1766:Move... (Commands)
    #@-node:ekr.20031218072017.2894:Outline menu...
    #@+node:ekr.20031218072017.2931:Window Menu
    #@+node:ekr.20031218072017.2092:openCompareWindow
    def openCompareWindow (self,event=None):
        
        c = self ; frame = c.frame
        
        if not frame.comparePanel:
            frame.comparePanel = g.app.gui.createComparePanel(c)
    
        frame.comparePanel.bringToFront()
    #@nonl
    #@-node:ekr.20031218072017.2092:openCompareWindow
    #@+node:ekr.20031218072017.2932:openPythonWindow (Dave Hein)
    def openPythonWindow (self,event=None):
    
        if sys.platform == "linux2":
            #@        << open idle in Linux >>
            #@+node:ekr.20031218072017.2933:<< open idle in Linux >>
            # 09-SEP-2002 DHEIN: Open Python window under linux
            
            try:
                pathToLeo = g.os_path_join(g.app.loadDir,"leo.py")
                sys.argv = [pathToLeo]
                from idlelib import idle
                if g.app.idle_imported:
                    reload(idle)
                g.app.idle_imported = True
            except:
                try:
                    g.es("idlelib could not be imported.")
                    g.es("Probably IDLE is not installed.")
                    g.es("Run Tools/idle/setup.py to build idlelib.")
                    g.es("Can not import idle")
                    g.es_exception() # This can fail!!
                except: pass
            #@-node:ekr.20031218072017.2933:<< open idle in Linux >>
            #@nl
        else:
            #@        << open idle in Windows >>
            #@+node:ekr.20031218072017.2934:<< open idle in Windows >>
            # Initialize argv: the -t option sets the title of the Idle interp window.
            sys.argv = ["leo"] # ,"-t","Leo"]
            
            ok = False
            if g.CheckVersion(sys.version,"2.3"):
                #@    << Try to open idle in Python 2.3 systems >>
                #@+node:ekr.20031218072017.2936:<< Try to open idle in Python 2.3 systems >>
                try:
                    idle_dir = None
                    
                    import idlelib.PyShell
                
                    if g.app.idle_imported:
                        reload(idle)
                        g.app.idle_imported = True
                        
                    idlelib.PyShell.main()
                    ok = True
                
                except:
                    ok = False
                    g.es_exception()
                #@nonl
                #@-node:ekr.20031218072017.2936:<< Try to open idle in Python 2.3 systems >>
                #@nl
            else:
                #@    << Try to open idle in Python 2.2 systems >>
                #@+node:ekr.20031218072017.2935:<< Try to open idle in Python 2.2 systems>>
                try:
                    executable_dir = g.os_path_dirname(sys.executable)
                    idle_dir = g.os_path_join(executable_dir,"Tools","idle")
                
                    # 1/29/04: sys.path doesn't handle unicode in 2.2.
                    idle_dir = str(idle_dir) # May throw an exception.
                
                    # 1/29/04: must add idle_dir to sys.path even when using importFromPath.
                    if idle_dir not in sys.path:
                        sys.path.insert(0,idle_dir)
                
                    if 1:
                        import PyShell
                    else: # Works, but is not better than import.
                        PyShell = g.importFromPath("PyShell",idle_dir)
                
                    if g.app.idle_imported:
                        reload(idle)
                        g.app.idle_imported = True
                        
                    if 1: # Mostly works, but causes problems when opening other .leo files.
                        PyShell.main()
                    else: # Doesn't work: destroys all of Leo when Idle closes.
                        self.leoPyShellMain()
                    ok = True
                except ImportError:
                    ok = False
                    g.es_exception()
                #@nonl
                #@-node:ekr.20031218072017.2935:<< Try to open idle in Python 2.2 systems>>
                #@nl
            
            if not ok:
                g.es("Can not import idle")
                if idle_dir and idle_dir not in sys.path:
                    g.es("Please add '%s' to sys.path" % idle_dir)
            #@nonl
            #@-node:ekr.20031218072017.2934:<< open idle in Windows >>
            #@nl
    #@+node:ekr.20031218072017.2937:leoPyShellMain
    #@+at 
    #@nonl
    # The key parts of Pyshell.main(), but using Leo's root window instead of 
    # a new Tk root window.
    # 
    # This does _not_ work well.  Using Leo's root window means that Idle will 
    # shut down Leo without warning when the Idle window is closed!
    #@-at
    #@@c
    
    def leoPyShellMain(self):
        
        import PyShell
        root = g.app.root
        PyShell.fixwordbreaks(root)
        flist = PyShell.PyShellFileList(root)
        shell = PyShell.PyShell(flist)
        flist.pyshell = shell
        shell.begin()
    #@nonl
    #@-node:ekr.20031218072017.2937:leoPyShellMain
    #@-node:ekr.20031218072017.2932:openPythonWindow (Dave Hein)
    #@-node:ekr.20031218072017.2931:Window Menu
    #@+node:ekr.20031218072017.2938:Help Menu
    #@+node:ekr.20031218072017.2939:about (version number & date)
    def about (self,event=None):
        
        c = self
        
        # Don't use triple-quoted strings or continued strings here.
        # Doing so would add unwanted leading tabs.
        version = c.getSignOnLine() + "\n\n"
        theCopyright = (
            "Copyright 1999-2006 by Edward K. Ream\n" +
            "All Rights Reserved\n" +
            "Leo is distributed under the Python License")
        url = "http://webpages.charter.net/edreamleo/front.html"
        email = "edreamleo@charter.net"
    
        g.app.gui.runAboutLeoDialog(c,version,theCopyright,url,email)
    #@nonl
    #@-node:ekr.20031218072017.2939:about (version number & date)
    #@+node:ekr.20031218072017.2943:leoConfig
    def openLeoSettings (self,event=None):
    
        c = self
        name = 'leoSettings.leo'
        homeDir = g.app.homeDir
        loadDir = g.app.loadDir
        configDir = g.app.globalConfigDir
    
        # Look in configDir first.
        fileName = g.os_path_join(configDir,name)
    
        # Look in homeDir second.
        ok, frame = g.openWithFileName(fileName,c)
        if not ok:
            if configDir == loadDir:
                g.es("%s not found in %s" % (name,configDir))
            else:
                fileName = g.os_path_join(homeDir,name)
                ok, frame = g.openWithFileName(fileName,c)
                if not ok:
                    g.es("%s not found in %s or %s" % (name,configDir,homeDir))
    #@nonl
    #@-node:ekr.20031218072017.2943:leoConfig
    #@+node:ekr.20031218072017.2940:leoDocumentation
    def leoDocumentation (self,event=None):
        
        c = self ; name = "LeoDocs.leo"
    
        fileName = g.os_path_join(g.app.loadDir,"..","doc",name)
        ok,frame = g.openWithFileName(fileName,c)
        if not ok:
            g.es("not found: %s" % name)
    #@-node:ekr.20031218072017.2940:leoDocumentation
    #@+node:ekr.20031218072017.2941:leoHome
    def leoHome (self,event=None):
        
        import webbrowser
    
        url = "http://webpages.charter.net/edreamleo/front.html"
        try:
            webbrowser.open_new(url)
        except:
            g.es("not found: " + url)
    #@nonl
    #@-node:ekr.20031218072017.2941:leoHome
    #@+node:ekr.20050130152008:leoPlugins
    def openLeoPlugins (self,event=None):
        
        c = self ; name = "leoPlugins.leo"
        fileName = g.os_path_join(g.app.loadDir,"..","plugins",name)
        ok,frame = g.openWithFileName(fileName,c)
        if not ok:
            g.es("not found: %s" % name)
    #@nonl
    #@-node:ekr.20050130152008:leoPlugins
    #@+node:ekr.20031218072017.2942:leoTutorial (version number)
    def leoTutorial (self,event=None):
        
        import webbrowser
    
        if 1: # new url
            url = "http://www.3dtree.com/ev/e/sbooks/leo/sbframetoc_ie.htm"
        else:
            url = "http://www.evisa.com/e/sbooks/leo/sbframetoc_ie.htm"
        try:
            webbrowser.open_new(url)
        except:
            g.es("not found: " + url)
    #@nonl
    #@-node:ekr.20031218072017.2942:leoTutorial (version number)
    #@-node:ekr.20031218072017.2938:Help Menu
    #@-node:ekr.20031218072017.2818:Command handlers...
    #@+node:ekr.20031218072017.2945:Dragging (commands)
    #@+node:ekr.20031218072017.2353:c.dragAfter
    def dragAfter(self,p,after):
    
        c = self ; u = self.undoer ; undoType = 'Drag'
        current = c.currentPosition()
        inAtIgnoreRange = p.inAtIgnoreRange()
        if not c.checkMoveWithParentWithWarning(p,after.parent(),True): return
    
        c.beginUpdate()
        try: # In update...
            c.endEditing()
            undoData = u.beforeMoveNode(current)
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty() # 1/12/04
            p.moveAfter(after)
            if inAtIgnoreRange and not p.inAtIgnoreRange():
                # The moved nodes have just become newly unignored.
                dirtyVnodeList2 = p.setDirty() # Mark descendent @thin nodes dirty.
                dirtyVnodeList.extend(dirtyVnodeList2)
            else: # No need to mark descendents dirty.
                dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                dirtyVnodeList.extend(dirtyVnodeList2)
            c.setChanged(True)
            u.afterMoveNode(p,undoType,undoData,dirtyVnodeList=dirtyVnodeList)
            c.selectPosition(p)
        finally:
            c.endUpdate()
        c.updateSyntaxColorer(p) # Dragging can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.2353:c.dragAfter
    #@+node:ekr.20031218072017.2946:c.dragCloneToNthChildOf
    def dragCloneToNthChildOf (self,p,parent,n):
    
        c = self ; u = c.undoer ; undoType = 'Clone Drag'
        current = c.currentPosition()
        inAtIgnoreRange = p.inAtIgnoreRange()
        
        c.beginUpdate()
        try: # In update...
            # g.trace("p,parent,n:",p.headString(),parent.headString(),n)
            clone = p.clone(p) # Creates clone & dependents, does not set undo.
            if not c.checkMoveWithParentWithWarning(clone,parent,True):
                clone.doDelete() # Destroys clone and makes p the current node.
                c.selectPosition(p)
                c.endUpdate(False) # Nothing has changed.
                return
            c.endEditing()
            undoData = u.beforeInsertNode(current)
            dirtyVnodeList = clone.setAllAncestorAtFileNodesDirty()
            clone.moveToNthChildOf(parent,n)
            if inAtIgnoreRange and not p.inAtIgnoreRange():
                # The moved nodes have just become newly unignored.
                dirtyVnodeList2 = p.setDirty() # Mark descendent @thin nodes dirty.
                dirtyVnodeList.extend(dirtyVnodeList2)
            else: # No need to mark descendents dirty.
               dirtyVnodeList2 =  p.setAllAncestorAtFileNodesDirty()
               dirtyVnodeList.extend(dirtyVnodeList2)
            c.setChanged(True)
            u.afterInsertNode(clone,undoType,undoData,dirtyVnodeList=dirtyVnodeList)
            c.selectPosition(clone)
        finally:
            c.endUpdate()
        c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.2946:c.dragCloneToNthChildOf
    #@+node:ekr.20031218072017.2947:c.dragToNthChildOf
    def dragToNthChildOf(self,p,parent,n):
    
        c = self ; u = c.undoer ; undoType = 'Drag'
        current = c.currentPosition()
        inAtIgnoreRange = p.inAtIgnoreRange()
        if not c.checkMoveWithParentWithWarning(p,parent,True): return
    
        c.beginUpdate()
        try: # In update...
            c.endEditing()
            undoData = u.beforeMoveNode(current)
            dirtyVnodeList = p.setAllAncestorAtFileNodesDirty()
            p.moveToNthChildOf(parent,n)
            if inAtIgnoreRange and not p.inAtIgnoreRange():
                # The moved nodes have just become newly unignored.
                dirtyVnodeList2 = p.setDirty() # Mark descendent @thin nodes dirty.
                dirtyVnodeList.extend(dirtyVnodeList2)
            else: # No need to mark descendents dirty.
                dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty()
                dirtyVnodeList.extend(dirtyVnodeList2)
            c.setChanged(True)
            u.afterMoveNode(p,undoType,undoData,dirtyVnodeList=dirtyVnodeList)
            c.selectPosition(p)
        finally:
            c.endUpdate()
        c.updateSyntaxColorer(p) # Dragging can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.2947:c.dragToNthChildOf
    #@+node:ekr.20031218072017.2948:c.dragCloneAfter
    def dragCloneAfter (self,p,after):
    
        c = self ; u = c.undoer ; undoType = 'Clone Drag'
        current = c.currentPosition()
    
        c.beginUpdate()
        try: # In update...
            clone = p.clone(p) # Creates clone.  Does not set undo.
            # g.trace("p,after:",p.headString(),after.headString())
            if not c.checkMoveWithParentWithWarning(clone,after.parent(),True):
                # g.trace("invalid clone drag")
                clone.doDelete()
                c.selectPosition(p)
                c.endUpdate(False) # Nothing has changed.
                return
            inAtIgnoreRange = clone.inAtIgnoreRange()
            c.endEditing()
            undoData = u.beforeInsertNode(current)
            dirtyVnodeList = clone.setAllAncestorAtFileNodesDirty()
            clone.moveAfter(after)
            if inAtIgnoreRange and not clone.inAtIgnoreRange():
                # The moved node have just become newly unignored.
                dirtyVnodeList2 = clone.setDirty() # Mark descendent @thin nodes dirty.
                dirtyVnodeList.extend(dirtyVnodeList2)
            else: # No need to mark descendents dirty.
                dirtyVnodeList2 = clone.setAllAncestorAtFileNodesDirty()
                dirtyVnodeList.extend(dirtyVnodeList2)
            c.setChanged(True)
            u.afterInsertNode(clone,undoType,undoData,dirtyVnodeList=dirtyVnodeList)
            c.selectPosition(clone)
        finally:
            c.endUpdate()
        c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
    #@nonl
    #@-node:ekr.20031218072017.2948:c.dragCloneAfter
    #@-node:ekr.20031218072017.2945:Dragging (commands)
    #@+node:ekr.20031218072017.2949:Drawing Utilities (commands)
    #@+node:ekr.20031218072017.2950:c.begin/endUpdate
    #@+at
    # **Important** These methods ensure that exactly zero or one (depending 
    # on the
    # argument to endUpdate) redraws exist within the section of code bounded 
    # by
    # c.beginUpdate and c.endUpdate. This greatly simplifies and clarifies the 
    # code.
    # 
    # Callers should ensure that every beginUpdate is matched with an 
    # endUpdate by
    # using the following pattern:
    #     c.beginUpdate()
    #     try:
    #         << whatever >>
    #     finally:
    #         c.endUpdate()
    #@-at
    #@@c
    
    def beginUpdate(self):
        
        '''Suppress redraws of the tree (except for explict calls to c.redraw_now)
        until the matching call to endUpdate.'''
        
        c = self
        c.frame.tree.beginUpdate()
        
    def endUpdate(self,flag=True,scroll=False):
        
        '''Redraw the screen if flag is True.'''
    
        c = self
        c.frame.tree.endUpdate(flag,scroll=scroll)
    
    BeginUpdate = beginUpdate # Compatibility with old scripts
    EndUpdate = endUpdate # Compatibility with old scripts
    #@-node:ekr.20031218072017.2950:c.begin/endUpdate
    #@+node:ekr.20031218072017.2951:c.bringToFront
    def bringToFront(self):
    
        self.frame.deiconify()
    
    BringToFront = bringToFront # Compatibility with old scripts
    #@nonl
    #@-node:ekr.20031218072017.2951:c.bringToFront
    #@+node:ekr.20060205103842:c.get/request/set_focus
    def get_focus (self):
        
        c = self
        return g.app.gui.get_focus(c)
        
    def get_requested_focus (self):
        
        c = self
        return c.requestedFocusWidget or c.hasFocusWidget or g.app.gui.get_focus(c)
        
    def request_focus(self,w):
    
        c = self
        if w: c.requestedFocusWidget = w
        c.traceFocus(w)
        
    def set_focus (self,w):
        
        c = self
        
        if 1: # An optimization.
            c.requestedFocusWidget = w
            c.masterFocusHandler()
        
        else: # Safer, perhaps.
            c.hasFocusWidget = c.requestedFocusWidget = w
            g.app.gui.set_focus(c,w)
    #@nonl
    #@-node:ekr.20060205103842:c.get/request/set_focus
    #@+node:ekr.20060210103358:c.invalidateFocus
    def invalidateFocus (self):
        
        '''Indicate that the focus is in an invalid location, or is unknown.'''
        
        c = self
        c.requestedFocusWidget = None
        c.hasFocusWidget = None
        # g.trace(g.callers())
        
    #@-node:ekr.20060210103358:c.invalidateFocus
    #@+node:ekr.20060207140352:c.masterFocusHandler
    def masterFocusHandler (self):
        
        c = self ; 
        trace = not g.app.unitTesting and c.config.getBool('trace_masterFocusHandler')
        
        # Give priority to later requests, but default to previously set widget.
        w = c.requestedFocusWidget or c.hasFocusWidget
        
        if trace: g.trace(
            'requested',c.widget_name(c.requestedFocusWidget),
            'present',c.widget_name(c.hasFocusWidget),
            g.callers())
        
        if c.hasFocusWidget and (
            not c.requestedFocusWidget or c.requestedFocusWidget == c.hasFocusWidget):
            # if trace: g.trace('no change.',c.widget_name(w))
            c.requestedFocusWidget = None
        elif w:
            # Ignore whatever g.app.gui.get_focus might say.
            ok = g.app.gui.set_focus(c,w)
            if ok: c.hasFocusWidget = w
            c.requestedFocusWidget = None
        else:
            # This is not an error: it can arise because of a call to k.invalidateFocus.
            # g.trace('*'*20,'oops: moving to body pane.')
            c.bodyWantsFocusNow()
    
    restoreRequestedFocus = masterFocusHandler
    #@nonl
    #@-node:ekr.20060207140352:c.masterFocusHandler
    #@+node:ekr.20031218072017.2953:c.recolor & requestRecolor
    def recolor(self):
    
        c = self
        c.frame.body.recolor(c.currentPosition())
        
    def requestRecolor (self):
        
        c = self
        c.frame.requestRecolorFlag = True
    #@nonl
    #@-node:ekr.20031218072017.2953:c.recolor & requestRecolor
    #@+node:ekr.20051216171520:c.recolor_now
    def recolor_now(self,p=None,incremental=False):
    
        c = self
        if p is None:
            p = c.currentPosition()
    
        c.frame.body.colorizer.colorize(p,incremental)
    #@nonl
    #@-node:ekr.20051216171520:c.recolor_now
    #@+node:ekr.20031218072017.2954:c.redraw and c.redraw_now
    def redraw (self):
        c = self
        c.beginUpdate()
        c.endUpdate()
    
    def redraw_now (self):
        
        c = self
        
        if g.app.quitting or not c.exists or not hasattr(c.frame,'top'):
            return # nullFrame's do not have a top frame.
    
        c.frame.tree.redraw_now()
        c.frame.top.update_idletasks()
        
        if c.frame.requestRecolorFlag:
            c.frame.requestRecolorFlag = False
            c.recolor()
    
    # Compatibility with old scripts
    force_redraw = redraw_now
    #@nonl
    #@-node:ekr.20031218072017.2954:c.redraw and c.redraw_now
    #@+node:ekr.20060208143543:c.restoreFocus
    def restoreFocus (self):
        
        '''Ensure that the focus eventually gets restored.'''
        
        c =self
        trace = not g.app.unitTesting and c.config.getBool('trace_focus')
    
        if c.requestedFocusWidget:
            c.hasFocusWidget = None # Force an update
        elif c.hasFocusWidget:
            c.requestedFocusWidget = c.hasFocusWidget
            c.hasFocusWidget = None # Force an update
        else:
            # Should not happen, except during unit testing.
            # c.masterFocusHandler sets c.hasFocusWidget,
            # so if it is not set here it is because this method cleared it.
            if not g.app.unitTesting: g.trace('oops: no requested or present widget.')
            c.bodyWantsFocusNow()
        
        if c.inCommand:
            if trace: g.trace('expecting later call to c.masterFocusHandler')
            pass # A call to c.masterFocusHandler will surely happen.
        else:
            c.masterFocusHandler() # Do it now.
    #@nonl
    #@-node:ekr.20060208143543:c.restoreFocus
    #@+node:ekr.20060207142332:c.traceFocus
    trace_focus_count = 0
    
    def traceFocus (self,w):
        
        c = self
    
        if not g.app.unitTesting and c.config.getBool('trace_focus'):
            c.trace_focus_count += 1
            g.trace('%4d' % (c.trace_focus_count),
                c.widget_name(w),g.callers(8))
    #@nonl
    #@-node:ekr.20060207142332:c.traceFocus
    #@+node:ekr.20060205111103:c.widget_name
    def widget_name (self,widget):
        
        c = self
        
        return c.gui.widget_name(widget)
    #@nonl
    #@-node:ekr.20060205111103:c.widget_name
    #@+node:ekr.20050120092028:c.xWantsFocus
    def bodyWantsFocus(self):
        c = self ; body = c.frame.body
        c.request_focus(body and body.bodyCtrl)
        
    def headlineWantsFocus(self,p):
        c = self
        c.request_focus(p and p.edit_widget())
        
    def logWantsFocus(self):
        c = self ; log = c.frame.log
        c.request_focus(log and log.logCtrl)
        
    def minibufferWantsFocus(self):
        c = self ; k = c.k
        k and k.minibufferWantsFocus()
        
    def treeWantsFocus(self):
        c = self ; tree = c.frame.tree
        c.request_focus(tree and tree.canvas)
        
    def widgetWantsFocus(self,w):
        c = self ; c.request_focus(w)
    #@nonl
    #@-node:ekr.20050120092028:c.xWantsFocus
    #@+node:ekr.20060210102201:c.xWantsFocusNow
    def bodyWantsFocusNow(self):
        c = self ; body = c.frame.body
        c.set_focus(body and body.bodyCtrl)
        
    def headlineWantsFocusNow(self,p):
        c = self
        c.set_focus(p and p.edit_widget())
        
    def logWantsFocusNow(self):
        c = self ; log = c.frame.log
        c.set_focus(log and log.logCtrl)
    
    def minibufferWantsFocusNow(self):
        c = self ; k = c.k
        k and k.minibufferWantsFocusNow()
        
    def treeWantsFocusNow(self):
        c = self ; tree = c.frame.tree
        c.set_focus(tree and tree.canvas)
        
    def widgetWantsFocusNow(self,w):
        c = self ; c.set_focus(w)
    #@-node:ekr.20060210102201:c.xWantsFocusNow
    #@-node:ekr.20031218072017.2949:Drawing Utilities (commands)
    #@+node:ekr.20031218072017.2955:Enabling Menu Items
    #@+node:ekr.20040323172420:Slow routines: no longer used
    #@+node:ekr.20031218072017.2966:canGoToNextDirtyHeadline (slow)
    def canGoToNextDirtyHeadline (self):
        
        c = self ; current = c.currentPosition()
    
        for p in c.allNodes_iter():
            if p != current and p.isDirty():
                return True
        
        return False
    #@nonl
    #@-node:ekr.20031218072017.2966:canGoToNextDirtyHeadline (slow)
    #@+node:ekr.20031218072017.2967:canGoToNextMarkedHeadline (slow)
    def canGoToNextMarkedHeadline (self):
        
        c = self ; current = c.currentPosition()
            
        for p in c.allNodes_iter():
            if p != current and p.isMarked():
                return True
    
        return False
    #@-node:ekr.20031218072017.2967:canGoToNextMarkedHeadline (slow)
    #@+node:ekr.20031218072017.2968:canMarkChangedHeadline (slow)
    def canMarkChangedHeadlines (self):
        
        c = self
        
        for p in c.allNodes_iter():
            if p.isDirty():
                return True
        
        return False
    #@nonl
    #@-node:ekr.20031218072017.2968:canMarkChangedHeadline (slow)
    #@+node:ekr.20031218072017.2969:canMarkChangedRoots (slow)
    def canMarkChangedRoots (self):
        
        c = self
        
        for p in c.allNodes_iter():
            if p.isDirty and p.isAnyAtFileNode():
                return True
    
        return False
    #@nonl
    #@-node:ekr.20031218072017.2969:canMarkChangedRoots (slow)
    #@-node:ekr.20040323172420:Slow routines: no longer used
    #@+node:ekr.20040131170659:canClone (new for hoist)
    def canClone (self):
    
        c = self
        
        if c.hoistStack:
            current = c.currentPosition()
            bunch = c.hoistStack[-1]
            return current != bunch.p
        else:
            return True
    #@nonl
    #@-node:ekr.20040131170659:canClone (new for hoist)
    #@+node:ekr.20031218072017.2956:canContractAllHeadlines
    def canContractAllHeadlines (self):
        
        c = self
        
        for p in c.allNodes_iter():
            if p.isExpanded():
                return True
    
        return False
    #@nonl
    #@-node:ekr.20031218072017.2956:canContractAllHeadlines
    #@+node:ekr.20031218072017.2957:canContractAllSubheads
    def canContractAllSubheads (self):
    
        c = self ; current = c.currentPosition()
        
        for p in current.subtree_iter():
            if p != current and p.isExpanded():
                return True
    
        return False
    #@nonl
    #@-node:ekr.20031218072017.2957:canContractAllSubheads
    #@+node:ekr.20031218072017.2958:canContractParent
    def canContractParent (self):
    
        c = self
        return c.currentPosition().parent()
    #@nonl
    #@-node:ekr.20031218072017.2958:canContractParent
    #@+node:ekr.20031218072017.2959:canContractSubheads
    def canContractSubheads (self):
        
        c = self ; current = c.currentPosition()
    
        for child in current.children_iter():
            if child.isExpanded():
                return True
            
        return False
    #@nonl
    #@-node:ekr.20031218072017.2959:canContractSubheads
    #@+node:ekr.20031218072017.2960:canCutOutline & canDeleteHeadline
    def canDeleteHeadline (self):
        
        c = self ; p = c.currentPosition()
    
        return p.hasParent() or p.hasThreadBack() or p.hasNext()
    
    canCutOutline = canDeleteHeadline
    #@nonl
    #@-node:ekr.20031218072017.2960:canCutOutline & canDeleteHeadline
    #@+node:ekr.20031218072017.2961:canDemote
    def canDemote (self):
    
        c = self
        return c.currentPosition().hasNext()
    #@nonl
    #@-node:ekr.20031218072017.2961:canDemote
    #@+node:ekr.20031218072017.2962:canExpandAllHeadlines
    def canExpandAllHeadlines (self):
        
        c = self
        
        for p in c.allNodes_iter():
            if not p.isExpanded():
                return True
    
        return False
    #@-node:ekr.20031218072017.2962:canExpandAllHeadlines
    #@+node:ekr.20031218072017.2963:canExpandAllSubheads
    def canExpandAllSubheads (self):
    
        c = self
        
        for p in c.currentPosition().subtree_iter():
            if not p.isExpanded():
                return True
            
        return False
    #@nonl
    #@-node:ekr.20031218072017.2963:canExpandAllSubheads
    #@+node:ekr.20031218072017.2964:canExpandSubheads
    def canExpandSubheads (self):
    
        c = self ; current = c.currentPosition()
        
        for p in current.children_iter():
            if p != current and not p.isExpanded():
                return True
    
        return False
    #@nonl
    #@-node:ekr.20031218072017.2964:canExpandSubheads
    #@+node:ekr.20031218072017.2287:canExtract, canExtractSection & canExtractSectionNames
    def canExtract (self):
    
        c = self ; body = c.frame.body
        return body and body.hasTextSelection()
        
    canExtractSectionNames = canExtract
            
    def canExtractSection (self):
        
        __pychecker__ = '--no-implicitreturns' # Suppress bad warning.
    
        c = self ; body = c.frame.body
        if not body: return False
        
        s = body.getSelectedText()
        if not s: return False
    
        line = g.get_line(s,0)
        i1 = line.find("<<")
        j1 = line.find(">>")
        i2 = line.find("@<")
        j2 = line.find("@>")
        return -1 < i1 < j1 or -1 < i2 < j2
    #@nonl
    #@-node:ekr.20031218072017.2287:canExtract, canExtractSection & canExtractSectionNames
    #@+node:ekr.20031218072017.2965:canFindMatchingBracket
    def canFindMatchingBracket (self):
        
        c = self ; brackets = "()[]{}"
        c1 = c.frame.body.getCharAtInsertPoint()
        c2 = c.frame.body.getCharBeforeInsertPoint()
        return (c1 and c1 in brackets) or (c2 and c2 in brackets)
    #@nonl
    #@-node:ekr.20031218072017.2965:canFindMatchingBracket
    #@+node:ekr.20040303165342:canHoist & canDehoist
    def canDehoist(self):
        
        return len(self.hoistStack) > 0
            
    def canHoist(self):
        
        c = self
        
        # N.B.  This is called at idle time, so minimizing positions is crucial!
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            return bunch.p and not bunch.p.isCurrentPosition()
        elif c.currentPositionIsRootPosition():
            return c.currentPositionHasNext()
        else:
            return True
    #@nonl
    #@-node:ekr.20040303165342:canHoist & canDehoist
    #@+node:ekr.20031218072017.2970:canMoveOutlineDown
    def canMoveOutlineDown (self):
    
        c = self ; current = c.currentPosition()
            
        p = current.visNext()
        while p and current.isAncestorOf(p):
            p.moveToVisNext()
    
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            return p and p != bunch.p and bunch.p.isAncestorOf(p)
        else:
            return p
    #@nonl
    #@-node:ekr.20031218072017.2970:canMoveOutlineDown
    #@+node:ekr.20031218072017.2971:canMoveOutlineLeft
    def canMoveOutlineLeft (self):
    
        c = self ; p = c.currentPosition()
    
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            if p and p.hasParent():
                p.moveToParent()
                return p != bunch.p and bunch.p.isAncestorOf(p)
            else:
                return False
        else:
            return p and p.hasParent()
    #@nonl
    #@-node:ekr.20031218072017.2971:canMoveOutlineLeft
    #@+node:ekr.20031218072017.2972:canMoveOutlineRight
    def canMoveOutlineRight (self):
    
        c = self ; p = c.currentPosition()
        
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            return p and p.hasBack() and p != bunch.p
        else:
            return p and p.hasBack()
    #@nonl
    #@-node:ekr.20031218072017.2972:canMoveOutlineRight
    #@+node:ekr.20031218072017.2973:canMoveOutlineUp
    def canMoveOutlineUp (self):
    
        c = self ; p = c.currentPosition()
        if not p: return False
        
        pback = p.visBack()
        if not pback: return False
    
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            return bunch.p != p and bunch.p.isAncestorOf(pback)
        else:
            return True
    #@nonl
    #@-node:ekr.20031218072017.2973:canMoveOutlineUp
    #@+node:ekr.20031218072017.2974:canPasteOutline
    def canPasteOutline (self,s=None):
    
        c = self
        if s == None:
            s = g.app.gui.getTextFromClipboard()
        if not s:
            return False
    
        # g.trace(s)
        if g.match(s,0,g.app.prolog_prefix_string):
            return True
        elif len(s) > 0:
            return c.importCommands.stringIsValidMoreFile(s)
        else:
            return False
    #@nonl
    #@-node:ekr.20031218072017.2974:canPasteOutline
    #@+node:ekr.20031218072017.2975:canPromote
    def canPromote (self):
    
        c = self ; v = c.currentVnode()
        return v and v.hasChildren()
    #@nonl
    #@-node:ekr.20031218072017.2975:canPromote
    #@+node:ekr.20031218072017.2976:canRevert
    def canRevert (self):
    
        # c.mFileName will be "untitled" for unsaved files.
        c = self
        return (c.frame and c.mFileName and c.isChanged())
    #@nonl
    #@-node:ekr.20031218072017.2976:canRevert
    #@+node:ekr.20031218072017.2977:canSelect....
    # 7/29/02: The shortcuts for these commands are now unique.
    
    def canSelectThreadBack (self):
        c = self ; p = c.currentPosition()
        return p.hasThreadBack()
        
    def canSelectThreadNext (self):
        c = self ; p = c.currentPosition()
        return p.hasThreadNext()
    
    def canSelectVisBack (self):
        c = self ; p = c.currentPosition()
        return p.hasVisBack()
        
    def canSelectVisNext (self):
        c = self ; p = c.currentPosition()
        return p.hasVisNext()
    #@nonl
    #@-node:ekr.20031218072017.2977:canSelect....
    #@+node:ekr.20031218072017.2978:canShiftBodyLeft/Right
    def canShiftBodyLeft (self):
    
        c = self ; body = c.frame.body
        return body and body.getAllText()
    
    canShiftBodyRight = canShiftBodyLeft
    #@nonl
    #@-node:ekr.20031218072017.2978:canShiftBodyLeft/Right
    #@+node:ekr.20031218072017.2979:canSortChildren, canSortSiblings
    def canSortChildren (self):
        
        c = self ; p = c.currentPosition()
        return p and p.hasChildren()
    
    def canSortSiblings (self):
    
        c = self ; p = c.currentPosition()
        return p and (p.hasNext() or p.hasBack())
    #@nonl
    #@-node:ekr.20031218072017.2979:canSortChildren, canSortSiblings
    #@+node:ekr.20031218072017.2980:canUndo & canRedo
    def canUndo (self):
    
        c = self
        return c.undoer.canUndo()
        
    def canRedo (self):
    
        c = self
        return c.undoer.canRedo()
    #@nonl
    #@-node:ekr.20031218072017.2980:canUndo & canRedo
    #@+node:ekr.20031218072017.2981:canUnmarkAll
    def canUnmarkAll (self):
        
        c = self
        
        for p in c.allNodes_iter():
            if p.isMarked():
                return True
    
        return False
    #@nonl
    #@-node:ekr.20031218072017.2981:canUnmarkAll
    #@-node:ekr.20031218072017.2955:Enabling Menu Items
    #@+node:ekr.20031218072017.2982:Getters & Setters
    #@+node:ekr.20031218072017.2984:c.clearAllMarked
    def clearAllMarked (self):
    
        c = self
    
        for p in c.allNodes_iter():
            p.v.clearMarked()
    #@nonl
    #@-node:ekr.20031218072017.2984:c.clearAllMarked
    #@+node:ekr.20031218072017.2985:c.clearAllVisited
    def clearAllVisited (self):
    
        c = self
    
        for p in c.allNodes_iter():
            p.v.clearVisited()
            p.v.t.clearVisited()
            p.v.t.clearWriteBit()
    #@-node:ekr.20031218072017.2985:c.clearAllVisited
    #@+node:ekr.20031218072017.2983:c.currentPosition & c.setCurrentPosition
    #@+node:ekr.20040803140033:currentPosition
    def currentPosition (self,copy=True):
        
        """Return the presently selected position."""
        
        c = self
        
        if c._currentPosition:
            if copy:
                return c._currentPosition.copy() # Must make a second copy now.
            else:
                # The caller MUST copy the position if it is passed to any other method.
                # At present no core method uses copy = False.
                g.trace("copy=False")
                return c._currentPosition
        else:
            return c.nullPosition()
        
    # For compatibiility with old scripts.
    currentVnode = currentPosition
    #@nonl
    #@-node:ekr.20040803140033:currentPosition
    #@+node:ekr.20040803140033.1:setCurrentPosition
    def setCurrentPosition (self,p):
        
        """Set the presently selected position."""
        
        c = self
        
        if p:
            if p.equal(c._currentPosition):
                pass # We have already made a copy.
            else: # Must make a copy _now_
                c._currentPosition = p.copy()
        else:
            c._currentPosition = None
        
    # For compatibiility with old scripts.
    setCurrentVnode = setCurrentPosition
    #@nonl
    #@-node:ekr.20040803140033.1:setCurrentPosition
    #@-node:ekr.20031218072017.2983:c.currentPosition & c.setCurrentPosition
    #@+node:ekr.20031218072017.2986:c.fileName & shortFileName
    # Compatibility with scripts
    
    def fileName (self):
    
        return self.mFileName
    
    def shortFileName (self):
        
        return g.shortFileName(self.mFileName)
    
    shortFilename = shortFileName
    #@nonl
    #@-node:ekr.20031218072017.2986:c.fileName & shortFileName
    #@+node:ekr.20031218072017.2987:c.isChanged
    def isChanged (self):
    
        return self.changed
    #@nonl
    #@-node:ekr.20031218072017.2987:c.isChanged
    #@+node:ekr.20040803112200:c.is...Position
    #@+node:ekr.20040803155551:c.currentPositionIsRootPosition
    def currentPositionIsRootPosition (self):
        
        """Return True if the current position is the root position.
        
        This method is called during idle time, so not generating positions
        here fixes a major leak.
        """
        
        c = self
        
        return (
            c._currentPosition and c._rootPosition and
            c._currentPosition == c._rootPosition)
    #@nonl
    #@-node:ekr.20040803155551:c.currentPositionIsRootPosition
    #@+node:ekr.20040803160656:c.currentPositionHasNext
    def currentPositionHasNext (self):
        
        """Return True if the current position is the root position.
        
        This method is called during idle time, so not generating positions
        here fixes a major leak.
        """
        
        c = self ; current = c._currentPosition 
        
        return current and current.hasNext()
    #@nonl
    #@-node:ekr.20040803160656:c.currentPositionHasNext
    #@+node:ekr.20040803112450:c.isCurrentPosition
    def isCurrentPosition (self,p):
        
        c = self
        
        if p is None or c._currentPosition is None:
            return False
        else:
            return p.isEqual(c._currentPosition)
    #@nonl
    #@-node:ekr.20040803112450:c.isCurrentPosition
    #@+node:ekr.20040803112450.1:c.isRootPosition
    def isRootPosition (self,p):
        
        c = self
        
        if p is None or c._rootPosition is None:
            return False
        else:
            return p.isEqual(c._rootPosition)
    #@nonl
    #@-node:ekr.20040803112450.1:c.isRootPosition
    #@-node:ekr.20040803112200:c.is...Position
    #@+node:ekr.20040311094927:c.nullPosition
    def nullPosition (self):
        
        c = self ; v = None
        return leoNodes.position(c,v,[])
    #@nonl
    #@-node:ekr.20040311094927:c.nullPosition
    #@+node:ekr.20031218072017.2988:c.rootPosition & c.setRootPosition
    #@+node:ekr.20040803140033.2:rootPosition
    def rootPosition(self):
        
        """Return the root position."""
        
        c = self
        
        if self._rootPosition:
            return self._rootPosition.copy()
        else:
            return  c.nullPosition()
    
    # For compatibiility with old scripts.
    rootVnode = rootPosition
    #@nonl
    #@-node:ekr.20040803140033.2:rootPosition
    #@+node:ekr.20040803140033.3:setRootPosition
    def setRootPosition(self,p):
        
        """Set the root positioin."""
    
        c = self
        
        if p:
            if p.equal(c._rootPosition):
                pass # We have already made a copy.
            else:
                # We must make a copy _now_.
                c._rootPosition = p.copy()
        else:
            c._rootPosition = None
        
    # For compatibiility with old scripts.
    setRootVnode = setRootPosition
    #@nonl
    #@-node:ekr.20040803140033.3:setRootPosition
    #@-node:ekr.20031218072017.2988:c.rootPosition & c.setRootPosition
    #@+node:ekr.20031218072017.2989:c.setChanged
    def setChanged (self,changedFlag):
    
        c = self
        if not c.frame: return
    
        # Clear all dirty bits _before_ setting the caption.
        # Clear all dirty bits except orphaned @file nodes
        if not changedFlag:
            # g.trace("clearing all dirty bits")
            for p in c.allNodes_iter():
                if p.isDirty() and not (p.isAtFileNode() or p.isAtNorefFileNode()):
                    p.clearDirty()
    
        # Update all derived changed markers.
        c.changed = changedFlag
        s = c.frame.getTitle()
        if len(s) > 2 and not c.loading: # don't update while loading.
            if changedFlag:
                if s [0] != '*': c.frame.setTitle("* " + s)
            else:
                if s[0:2]=="* ": c.frame.setTitle(s[2:])
    #@nonl
    #@-node:ekr.20031218072017.2989:c.setChanged
    #@+node:ekr.20060109164136:c.setLog
    def setLog (self):
        
        c = self
    
        if c.exists:
            try:
                # c.frame or c.frame.log may not exist.
                g.app.setLog(c.frame.log)
            except AttributeError:
                pass
    #@nonl
    #@-node:ekr.20060109164136:c.setLog
    #@+node:ekr.20040311173238:c.topPosition & c.setTopPosition
    def topPosition(self):
        
        """Return the root position."""
        
        c = self
        
        if c._topPosition:
            return c._topPosition.copy()
        else:
            return c.nullPosition()
    
    def setTopPosition(self,p):
        
        """Set the root positioin."""
        
        c = self
    
        if p:
            c._topPosition = p.copy()
        else:
            c._topPosition = None
        
    # Define these for compatibiility with old scripts.
    topVnode = topPosition
    setTopVnode = setTopPosition
    #@nonl
    #@-node:ekr.20040311173238:c.topPosition & c.setTopPosition
    #@-node:ekr.20031218072017.2982:Getters & Setters
    #@+node:ekr.20031218072017.2990:Selecting & Updating (commands)
    #@+node:ekr.20031218072017.2991:c.editPosition
    # Selects v: sets the focus to p and edits p.
    
    def editPosition(self,p):
    
        c = self ; k = c.k
    
        if p:
            c.selectPosition(p)
            c.frame.tree.editLabel(p)
            
            if k:
                k.setDefaultUnboundKeyAction()
                k.showStateAndMode()
    #@nonl
    #@-node:ekr.20031218072017.2991:c.editPosition
    #@+node:ekr.20031218072017.2992:c.endEditing (calls tree.endEditLabel)
    # Ends the editing in the outline.
    
    def endEditing(self):
        
        c = self
        c.frame.tree.endEditLabel()
    #@nonl
    #@-node:ekr.20031218072017.2992:c.endEditing (calls tree.endEditLabel)
    #@+node:ekr.20031218072017.2997:c.selectPosition
    def selectPosition(self,p,updateBeadList=True):
        
        """Select a new position."""
    
        c = self
    
        c.frame.tree.select(p,updateBeadList)
    
    selectVnode = selectPosition
    #@nonl
    #@-node:ekr.20031218072017.2997:c.selectPosition
    #@+node:ekr.20031218072017.2998:selectVnodeWithEditing
    # Selects the given node and enables editing of the headline if editFlag is True.
    
    def selectVnodeWithEditing(self,v,editFlag):
    
        c = self
        if editFlag:
            c.editPosition(v)
        else:
            c.selectVnode(v)
    
    selectPositionWithEditing = selectVnodeWithEditing
    #@nonl
    #@-node:ekr.20031218072017.2998:selectVnodeWithEditing
    #@-node:ekr.20031218072017.2990:Selecting & Updating (commands)
    #@+node:ekr.20031218072017.2999:Syntax coloring interface
    #@+at 
    #@nonl
    # These routines provide a convenient interface to the syntax colorer.
    #@-at
    #@+node:ekr.20031218072017.3000:updateSyntaxColorer
    def updateSyntaxColorer(self,v):
    
        self.frame.body.updateSyntaxColorer(v)
    #@-node:ekr.20031218072017.3000:updateSyntaxColorer
    #@-node:ekr.20031218072017.2999:Syntax coloring interface
    #@-others

class Commands (baseCommands):
    """A class that implements most of Leo's commands."""
    pass
#@nonl
#@-node:ekr.20041118104831:class commands
#@+node:ekr.20041118104831.1:class configSettings
class configSettings:
    
    """A class to hold config settings for commanders."""
    
    #@    @+others
    #@+node:ekr.20041118104831.2:configSettings.__init__
    def __init__ (self,c):
        
        self.c = c
        
        self.defaultBodyFontSize = g.app.config.defaultBodyFontSize
        self.defaultLogFontSize  = g.app.config.defaultLogFontSize
        self.defaultTreeFontSize = g.app.config.defaultTreeFontSize
        
        for key in g.app.config.encodingIvarsDict.keys():
            if key != '_hash':
                self.initEncoding(key)
            
        for key in g.app.config.ivarsDict.keys():
            if key != '_hash':
                self.initIvar(key)
    #@nonl
    #@+node:ekr.20041118104240:initIvar
    def initIvar(self,key):
        
        c = self.c
        
        # N.B. The key is munged.
        bunch = g.app.config.ivarsDict.get(key)
        ivarName = bunch.ivar
        val = g.app.config.get(c,ivarName,kind=None) # kind is ignored anyway.
    
        if val or not hasattr(self,ivarName):
            # g.trace('c.configSettings',c.shortFileName(),ivarName,val)
            setattr(self,ivarName,val)
    #@nonl
    #@-node:ekr.20041118104240:initIvar
    #@+node:ekr.20041118104414:initEncoding
    def initEncoding (self,key):
        
        c = self.c
        
        # N.B. The key is munged.
        bunch = g.app.config.encodingIvarsDict.get(key)
        encodingName = bunch.ivar
        encoding = g.app.config.get(c,encodingName,kind='string')
        
        # New in 4.4b3: use the global setting as a last resort.
        if encoding:
            # g.trace('c.configSettings',c.shortFileName(),encodingName,encoding)
            setattr(self,encodingName,encoding)
        else:
            encoding = getattr(g.app.config,encodingName)
            # g.trace('g.app.config',c.shortFileName(),encodingName,encoding)
            setattr(self,encodingName,encoding)
    
        if encoding and not g.isValidEncoding(encoding):
            g.es("bad %s: %s" % (encodingName,encoding))
    #@nonl
    #@-node:ekr.20041118104414:initEncoding
    #@-node:ekr.20041118104831.2:configSettings.__init__
    #@+node:ekr.20041118053731:Getters
    def getFontFromParams(self,family,size,slant,weight,defaultSize=12):
        return g.app.config.getFontFromParams(self.c,
            family,size,slant,weight,defaultSize=defaultSize)
    
    def getRecentFiles (self):
        return g.app.config.getRecentFiles()
    
    def get(self,setting,theType):
        return g.app.config.get(self.c,setting,theType)
    
    def getBool      (self,setting): return g.app.config.getBool     (self.c,setting)
    def getColor     (self,setting): return g.app.config.getColor    (self.c,setting)
    def getDirectory (self,setting): return g.app.config.getDirectory(self.c,setting)
    def getInt       (self,setting): return g.app.config.getInt      (self.c,setting)
    def getFloat     (self,setting): return g.app.config.getFloat    (self.c,setting)
    def getFontDict  (self,setting): return g.app.config.getFontDict (self.c,setting)
    def getLanguage  (self,setting): return g.app.config.getLanguage (self.c,setting)
    def getRatio     (self,setting): return g.app.config.getRatio    (self.c,setting)
    def getShortcut  (self,setting,):return g.app.config.getShortcut (self.c,setting)
    def getString    (self,setting): return g.app.config.getString   (self.c,setting)
    #@nonl
    #@-node:ekr.20041118053731:Getters
    #@+node:ekr.20041118195812:Setters... (c.configSettings)
    #@+node:ekr.20041118195812.3:setRecentFiles (c.configSettings)
    def setRecentFiles (self,files):
        
        '''Update the recent files list.'''
    
        # Append the files to the global list.
        g.app.config.appendToRecentFiles(files)
    #@nonl
    #@-node:ekr.20041118195812.3:setRecentFiles (c.configSettings)
    #@+node:ekr.20041118195812.2:set & setString
    def set (self,p,setting,val):
        
        __pychecker__ = '--no-argsused' # p not used.
        
        return g.app.config.setString(self.c,setting,val)
        
    setString = set
    #@nonl
    #@-node:ekr.20041118195812.2:set & setString
    #@-node:ekr.20041118195812:Setters... (c.configSettings)
    #@-others
#@nonl
#@-node:ekr.20041118104831.1:class configSettings
#@-others
#@nonl
#@-node:ekr.20031218072017.2810:@thin leoCommands.py
#@-leo
