#@+leo-ver=4-thin
#@+node:ekr.20040915144649.2:@thin chapters.py

__version__ = '.2'
#@<< imports >>
#@+node:ekr.20040915144649.3:<< imports >>
import leoGlobals as g
import leoPlugins
from leoNodes import *
import leoTkinterFrame
import leoColor,leoFrame,leoNodes
import leoTkinterMenu,leoTkinterTree
from leoTkinterFrame import leoTkinterLog
from leoTkinterFrame import leoTkinterBody
import leoFileCommands
import leoTkinterTree
import leoGlobals

import os
import string
import sys
import time
import traceback

try:
    import Tkinter as Tk
    import tkFileDialog
    import tkFont
except ImportError:
    Tk = g.cantImport("Tk",__name__)

try:
    import Pmw
except:
    Pmw = g.cantImport("Pmw",__name__)

import zipfile
import time
#@nonl
#@-node:ekr.20040915144649.3:<< imports >>
#@nl
#@<< vars >>
#@+node:ekr.20040915144649.4:<< vars >>
notebooks = {}
frames = {}
scrollbars = {}
canvass = {}
yscrollbars = {}
iscStringIO = False
twidgets = {}
pbodies = {}
#@nonl
#@-node:ekr.20040915144649.4:<< vars >>
#@nl

#@+others
#@+node:ekr.20040915144649.5:getSV
def getSV( name, c = None ):

    if not c : c = g.top()
    notebook = notebooks[ c ]
    index = notebook.index( name )
    page = notebook.page( index )
    return page.sv
#@nonl
#@-node:ekr.20040915144649.5:getSV
#@+node:ekr.20040915144649.6:finishCreate
def finishCreate ( self, c):

    frame = self ; frame.c = c ; frame.trees = {}

    #@    << create the toplevel frame >>
    #@+node:ekr.20040915153428:<< create the toplevel frame >>
    frames[ c ] = frame
    gui = g.app.gui
    
    frame.top = top = Tk.Toplevel()
    gui.attachLeoIcon(top)
    top.title(frame.title)
    top.minsize(30,10) # In grid units.
    
    frame.top.protocol("WM_DELETE_WINDOW", frame.OnCloseLeoEvent)
    frame.top.bind("<Button-1>", frame.OnActivateLeoEvent)
    
    frame.top.bind("<Activate>", frame.OnActivateLeoEvent) # Doesn't work on windows.
    frame.top.bind("<Deactivate>", frame.OnDeactivateLeoEvent) # Doesn't work on windows.
    
    frame.top.bind("<Control-KeyPress>",frame.OnControlKeyDown)
    frame.top.bind("<Control-KeyRelease>",frame.OnControlKeyUp)
    
    # Create the outer frame.
    self.outerFrame = outerFrame = Tk.Frame(top)
    self.outerFrame.pack(expand=1,fill="both")
    self.createIconBar()
    #@nonl
    #@-node:ekr.20040915153428:<< create the toplevel frame >>
    #@nl
    #@    << create all the subframes >>
    #@+node:ekr.20040915153428.1:<< create all the subframes >>
    # Splitter 1 is the main splitter containing splitter2 and the body pane.
    f1,bar1,split1Pane1,split1Pane2 = self.createLeoSplitter(outerFrame, self.splitVerticalFlag)
    self.f1,self.bar1 = f1,bar1
    self.split1Pane1,self.split1Pane2 = split1Pane1,split1Pane2
    pbody = Pmw.PanedWidget( split1Pane2 , orient = 'horizontal' )
    pbody.pack( expand = 1 , fill = 'both')
    zpane = pbody.add( '1' )
    pbodies[ c ] = pbody
    
    # Splitter 2 is the secondary splitter containing the tree and log panes.
    f2,bar2,split2Pane1,split2Pane2 = self.createLeoSplitter( split1Pane1, not self.splitVerticalFlag)
    self.f2,self.bar2 = f2,bar2
    self.split2Pane1,self.split2Pane2 = split2Pane1,split2Pane2
    
    # Create the canvas, tree, log and body.
    notebooks[ c ] = notebook = Pmw.NoteBook( self.split2Pane1 )
    hull = notebook.component( 'hull' )
    makeTabMenu( hull, notebook, c )
    notebook.configure( raisecommand = lambda name, notebook = notebook : setTree( name , notebook ) )
    notebook.pack( fill = 'both' , expand = 1)
    def nameMaker():
        i = 0
        while 1:
            if len( notebook.pagenames() ) == 0: i = 0
            i += 1
            yield str( i )
    notebook.nameMaker = nameMaker()
    t, page = constructTree( frame , notebook , '1' )
    frame.log = leoTkinterLog(frame,self.split2Pane2)
    l, r =addHeading( zpane )
    frame.body = leoTkinterBody(frame,zpane)
    frame.body.bodyCtrl.bind( "<FocusIn>", lambda event, body = frame.body : editorHasFocus( event, body ) )
    frame.body.l =l
    frame.body.r =r
    
    frame.body.editorName = '1'
    twidgets[ frame.body.bodyCtrl ] = frame.body
    l.configure( textvariable = getSV( '1', c ) )
    # Yes, this an "official" ivar: this is a kludge.
    frame.bodyCtrl = frame.body.bodyCtrl
    
    # Configure. N.B. There may be Tk bugs here that make the order significant!
    frame.setTabWidth(c.tab_width)
    frame.tree.setTreeColorsFromConfig()
    self.reconfigurePanes()
    self.body.setFontFromConfig()
    
    if 0: # No longer done automatically.
        # Create the status line.
        self.createStatusLine()
        self.putStatusLine("Welcome to Leo")
    #@nonl
    #@-node:ekr.20040915153428.1:<< create all the subframes >>
    #@nl
    #@    << create the first tree node >>
    #@+node:ekr.20040915153428.2:<< create the first tree node >>
    t = leoNodes.tnode()
    v = leoNodes.vnode(c,t)
    p = leoNodes.position(v,[])
    v.initHeadString("NewHeadline")
    
    
    p.moveToRoot()
    c.beginUpdate()
    c.selectVnode(p)
    c.redraw()
    c.frame.getFocus()
    c.editPosition(p)
    c.endUpdate(False)
    #@nonl
    #@-node:ekr.20040915153428.2:<< create the first tree node >>
    #@nl

    self.menu = leoTkinterMenu.leoTkinterMenu(frame)

    v = c.currentVnode()

    if not g.doHook("menu1",c=c,v=v):
        frame.menu.createMenuBar(self)

    g.app.setLog(frame.log,"tkinterFrame.__init__") # the leoTkinterFrame containing the log

    g.app.windowList.append(frame)

    c.initVersion()
    c.signOnWithVersion()

    self.body.createBindings(frame)
#@nonl
#@-node:ekr.20040915144649.6:finishCreate
#@+node:ekr.20040915144649.7:constructTree
def constructTree( frame , notebook, name ):

    canvas = treeBar = tree = None
    if frame.canvas:
        canvas = frame.canvas
        treeBar = frame.treeBar
        tree = frame.tree
    pname = notebook.nameMaker.next()
    page = notebook.add( pname )
    indx = notebook.index( pname )
    tab = notebook.tab( indx )
    makeTabMenu( tab, notebook, frame.c )
    hull = notebook.component( 'hull' )
    tab.bind( '<Button-3>' , lambda event : hull.tmenu.post( event.x_root , event.y_root ) )
    x = notebook.component( pname +'-tab' )
    balloon = Pmw.Balloon( x, initwait = 100 )
    balloon.bind( x , '' )
    sv = Tk.StringVar()
    sv.set( name )
    page.sv = sv
    balloon._label.configure( textvariable = sv )
    frame.canvas = canvass[ sv ] = frame.createCanvas( page )
    frame.tree = frame.trees[ sv ] = leoTkinterTree.leoTkinterTree( frame.c ,frame, frame.canvas)
    frame.tree.setTreeColorsFromConfig()
    yscrollbars[ sv ] = frame.treeBar
    if canvas:
        frame.canvas = canvas
        frame.treeBar = treeBar
    else:
        tree = frame.tree
    return tree , page






#@-node:ekr.20040915144649.7:constructTree
#@+node:ekr.20040915144649.8:addPage
def addPage( c , name = None ):
    vnd = c.currentVnode()
    frame = frames[ c ]
    notebook = notebooks[ c ]
    if name == None : name = str( len( notebook.pagenames() ) + 1 )
    otree, page = constructTree( frame, notebook, name )
    t = leoNodes.tnode()
    v = leoNodes.vnode(c,t)
    v.initHeadString("NewHeadline")
    v.moveToRoot()

    c.beginUpdate()
    c.selectVnode(v)
    c.frame.getFocus()
    c.editVnode(v)
    c.endUpdate(False)
    frame.tree= otree
    c.selectVnode( vnd )
    return page

#@-node:ekr.20040915144649.8:addPage
#@+node:ekr.20040915144649.9:setTree
def setTree( name , notebook ):
    c = g.top()
    if c == None: return None
    page = notebook.page( notebook.index( name ) )
    if not hasattr( page, 'sv' ) : return None
    sv = page.sv
    frame = frames[ c ]
    frame.canvas = canvass[ sv ]
    frame.treeBar = yscrollbars[ sv ]
    tree = frame.trees[ sv ]
    frame.tree = tree
    frame.body.lastChapter = name
    frame.body.lastNode = frame.tree.currentPosition()
    frame.body.l.configure( textvariable = sv )
    frame.body.r.configure( text = frame.body.lastNode.headString() )
    c.selectVnode( tree.currentVnode() )
    c.redraw()


#@-node:ekr.20040915144649.9:setTree
#@+node:ekr.20040915144649.10:openWithFileNamez
def openWithFileNamez(fileName,old_c,enableLog=True, samewindow = True):

    """Create a Leo Frame for the indicated fileName if the file exists."""
    # trace(fileName)
    assert(g.app.config)

    if not fileName or len(fileName) == 0:
        return False, None
    # Create a full normalized path name.
    # Display the file name with case intact.
    fileName = g.os_path_join(os.getcwd(), fileName)
    fileName = g.os_path_normpath(fileName)
    oldFileName = fileName
    fileName = g.os_path_normcase(fileName)

    # If the file is already open just bring its window to the front.
    list = g.app.windowList
    for frame in list:
        fn = g.os_path_normcase(frame.c.mFileName)
        fn = g.os_path_normpath(fn)
        if fileName == fn:
            frame.deiconify()
            g.app.setLog(frame.log,"openWithFileName")
            # g.es("This window already open")
            if samewindow: return True, frame
    fileName = oldFileName # Use the idiosyncratic file name.
    try:
        file = None
        iszip = False
        if zipfile.is_zipfile( fileName ):
            zf = zipfile.ZipFile( fileName )
            import cStringIO
            file = cStringIO.StringIO()
            name = zf.namelist()
            csfiles = {}
            for x in name:
                cs = csfiles[ x ] = cStringIO.StringIO()
                cs.write( zf.read( x ) )
                cs.seek( 0 )
            zf.close()
            iszip = True


        # 11/4/03: open the file in binary mode to allow 0x1a in bodies & headlines.
        else:
            file = open(fileName,'rb')
        if file:
            if samewindow:
                c,frame = g.app.gui.newLeoCommanderAndFrame(fileName)
            else:
                c = old_c
                frame = c.frame
            frame.log.enable(enableLog)
            if not g.doHook("open1",old_c=old_c,new_c=c,fileName=fileName):
                g.app.setLog(frame.log,"openWithFileName")
                g.app.lockLog()
                if iszip:
                    c.frame.tree.drag_v = True
                    notebook = notebooks[ c ]
                    notebook.delete( '1' )
                    global iscStringIO
                    iscStringIO = True
                    g.es( str( len( name ) ) + " Chapters To Read", color = 'blue' )
                    for x in name:
                        sv = addPage( c, x ).sv
                        frame.tree = frame.trees[ sv ]
                        frame.treeBar = yscrollbars[ sv ]
                        frame.canvas = canvass[ sv ]
                        cf = csfiles[ x ]
                        frame.c.fileCommands.open( cf, sv.get() )
                    g.es( "Finished Reading Chapters", color = 'blue' )
                    iscStringIO = False
                    c.frame.tree.drag_v = None
                    setTree( notebook.index( 0 ) )

                else: frame.c.fileCommands.open(file,fileName) # closes file.
                g.app.unlockLog()
            frame.openDirectory = g.os_path_dirname(fileName)
            g.doHook("open2",old_c=old_c,new_c=frame.c,fileName=fileName)
            return True, frame
        else:
            g.es("can not open: " + fileName,color="red")
            return False, None
    except IOError:
        g.es("can not open: " + fileName, color="blue")
        return False, None
    except:
        if 1:
            print "exceptions opening:", fileName
            traceback.print_exc()
        else:
            g.es("exceptions opening: " + fileName,color="red")
            g.es_exception()
        return False, None


#@-node:ekr.20040915144649.10:openWithFileNamez
#@+node:ekr.20040915144649.11:getLeoFile
# The caller should enclose this in begin/endUpdate.

def getLeoFile (self,fileName,atFileNodesFlag=True ):

    c = self.c
    c.setChanged(False) # 10/1/03: May be set when reading @file nodes.
    try:
        if not iscStringIO:
            self.read_only = False
            self.read_only = not os.access(fileName,os.W_OK)
            if self.read_only:
                g.es("read only: " + fileName,color="red")
    except:
        if 0: # testing only: access may not exist on all platforms.
            g.es("exception getting file access")
            g.es_exception()
    self.mFileName = c.mFileName
    #self.tnodesDict = {}
    ok = True
    c.loading = True # disable c.changed
    try:
        self.getXmlVersionTag()
        self.getXmlStylesheetTag()
        self.getTag("<leo_file>")
        self.getLeoHeader()
        self.getGlobals()
        self.getPrefs()
        self.getFindPanelSettings()

        # Causes window to appear.
        c.frame.resizePanesToRatio(c.frame.ratio,c.frame.secondary_ratio)
        g.es("reading: " + fileName)

        self.getVnodes()
        self.getTnodes()
        self.getCloneWindows()
        self.getTag("</leo_file>")
    except BadLeoFile, message:
        # All other exceptions are Leo bugs.

        g.es_exception()
        alert(self.mFileName + " is not a valid Leo file: " + `message`)
        ok = False
        
    c.frame.tree.redraw_now(scroll=False)

    if ok and atFileNodesFlag:
        c.atFileCommands.readAll(c.rootVnode(),partialFlag=False)

    if not c.currentPosition():
        c.setCurrentPosition(c.rootPosition())

    c.selectVnode(c.setCurrentPosition(c.rootPosition()))
    c.loading = False # reenable c.changed
    c.setChanged(c.changed) # Refresh the changed marker.
    #self.tnodesDict = {}
    return ok, self.ratio
#@-node:ekr.20040915144649.11:getLeoFile
#@+node:ekr.20040915144649.12:write_LEO_filez
def write_LEO_filez(self,fileName,outlineOnlyFlag, singleChapter = False):

    c = self.c ; config = g.app.config

    if not outlineOnlyFlag:
        try:
            pagenames = notebooks[ c ].pagenames()
            at = c.atFileCommands
            if len( pagenames ) > 1 and not singleChapter:
                otree = c.frame.tree
                for z in pagenames:
                    sv = getSV( z )
                    c.frame.tree = c.frame.trees[ sv ]
                    at.writeAll()
                c.frame.tree = otree
            # Leo2: write all @file nodes and set orphan bits.
            else:
                at.writeAll()
        except:
            es_error("exception writing derived files")
            g.es_exception()
            return False

    # 1/29/03: self.read_only is not valid for Save As and Save To commands.
    if g.os_path_exists(fileName):
        try:
            if not os.access(fileName,os.W_OK):
                self.writeError("can not create: read only: " + self.targetFileName)
                return False
        except:
            pass # os.access() may not exist on all platforms.

    try:
        # rename fileName to fileName.bak if fileName exists.
        if g.os_path_exists(fileName):
            try:
                backupName = g.os_path_join(g.app.loadDir,fileName)
                backupName = fileName + ".bak"
                if g.os_path_exists(backupName):
                    os.unlink(backupName)
                # os.rename(fileName,backupName)
                utils_rename(fileName,backupName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception creating backup file: " + backupName)
                    g.es_exception()
                return False
            except:
                g.es("exception creating backup file: " + backupName)
                g.es_exception()
                backupName = None
                return False
        else:
            backupName = None
        self.mFileName = fileName
        iszip = False
        if len( pagenames ) > 1 and not singleChapter:
            import cStringIO
            names = notebooks[ c ].pagenames()
            cnames = {}
            for nms in names:
                cnames[ nms ] = cStringIO.StringIO()
            self.outputFile = cStringIO.StringIO()
            iszip = True
        else:
            self.outputFile = open(fileName, 'wb') # 9/18/02
        if not self.outputFile:
            g.es("can not open " + fileName)
            if backupName and g.os_path_exists(backupName):
                try:
                    os.unlink(backupName)
                except OSError:
                    if self.read_only:
                        g.es("read only",color="red")
                    else:
                        g.es("exception deleting backup file:" + backupName)
                        g.es_exception()
                    return False
                except:
                    g.es("exception deleting backup file:" + backupName)
                    g.es_exception()
                    return False

            return False

        # 8/6/02: Update leoConfig.txt completely here.
        if iszip:
            sname = notebooks[ c ].getcurselection()
            for x in names:
                sv = getSV( x )
                c.frame.tree = c.frame.trees[ sv ]
                self.outputFile = cnames[ x ]
                performWrite( self, c, config )
                self.outputFile.seek( 0 )
            setTree( sname , notebooks[ c ])
        else:
            performWrite( self, c , config )
        # raise BadLeoFile # testing
    except:
        g.es("exception writing: " + fileName)
        g.es_exception()
        if self.outputFile:
            try:
                self.outputFile.close()
                self.outputFile = None
            except:
                g.es("exception closing: " + fileName)
                g.es_exception()
        g.es("error writing " + fileName)

        if fileName and g.os_path_exists(fileName):
            try:
                os.unlink(fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception deleting: " + fileName)
                    g.es_exception()
            except:
                g.es("exception deleting: " + fileName)
                g.es_exception()

        if backupName:
            g.es("restoring " + fileName + " from " + backupName)
            try:
                utils_rename(backupName, fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception renaming " + backupName + " to " + fileName)
                    g.es_exception()
            except:
                g.es("exception renaming " + backupName + " to " + fileName)
                g.es_exception()
        return False

    if self.outputFile:
        try:
            if iszip:
                zf = zipfile.ZipFile( fileName, 'w', zipfile.ZIP_DEFLATED )
                for fname in names:
                    sv = getSV( fname )
                    zif = zipfile.ZipInfo( sv.get() )
                    zif.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr( zif ,cnames[ fname ].read() )
                zf.close()
            else:
                self.outputFile.close()
                self.outputFile = None
        except:
            g.es("exception closing: " + fileName)
            g.es_exception()
        if backupName and g.os_path_exists(backupName):
            try:
                os.unlink(backupName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception deleting backup file:" + backupName)
                    g.es_exception()
                return False
            except:
                g.es("exception deleting backup file:" + backupName)
                g.es_exception()
                return False

        return True
    else: # This probably will never happen because errors should raise exceptions.
        g.es("error writing " + fileName)

        if fileName and g.os_path_exists(fileName):
            try:
                os.unlink(fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception deleting: " + fileName)
                    g.es_exception()
            except:
                g.es("exception deleting: " + fileName)
                g.es_exception()

        if backupName:
            g.es("restoring " + fileName + " from " + backupName)
            try:
                utils_rename(backupName, fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception renaming " + backupName + " to " + fileName)
                    g.es_exception()
            except:
                g.es("exception renaming " + backupName + " to " + fileName)
                g.es_exception()
        return False
#@-node:ekr.20040915144649.12:write_LEO_filez
#@+node:ekr.20040915144649.13:performWrite
def performWrite(self, c , config ):
        # self in this case is a self pased in by a caller, it is not an object self
        self.assignFileIndices()
        c.setIvarsFromFind()
        config.setConfigFindIvars(c)
        c.setIvarsFromPrefs()
        config.setCommandsIvars(c)
        config.update()
        self.putProlog()
        self.putHeader()
        self.putGlobals()
        self.putPrefs()
        self.putFindSettings()
        self.putVnodes()
        self.putTnodes()
        self.putPostlog()
#@-node:ekr.20040915144649.13:performWrite
#@+node:ekr.20040915144649.14:cloneToChapter
def cloneToChapter( c , name ):
    notebook = notebooks[ c ]
    page = notebook.page( notebook.index( name ) )
    tree = c.frame.trees[ page.sv ]
    c.beginUpdate()
    vnd = c.currentVnode()
    clo = vnd.clone( vnd )
    vndm = tree.currentVnode()
    clo.destroyDependents()
    clo.unlink()
    clo.linkAfter(vndm)
    clo.createDependents()
    c.endUpdate()
#@nonl
#@-node:ekr.20040915144649.14:cloneToChapter
#@+node:ekr.20040915144649.15:moveToChapter
def moveToChapter( c, name ):
    notebook = notebooks[ c ]
    page = notebook.page( notebook.index( name ) )
    tree = c.frame.trees[ page.sv ]
    c.beginUpdate()
    vnd = c.currentVnode()
    if not vnd.parent() and not vnd.back() :
        c.endUpdate()
        return None
    vndm = tree.currentVnode()
    vnd.destroyDependents()
    vnd.unlink()
    vnd.linkAfter(vndm)
    vnd.createDependents()
    c.endUpdate()
#@nonl
#@-node:ekr.20040915144649.15:moveToChapter
#@+node:ekr.20040915144649.16:copyToChapter
def copyToChapter( c, name ):
    notebook = notebooks[ c ]
    page = notebook.page( notebook.index( name ) )
    tree = c.frame.trees[ page.sv ]
    c.beginUpdate()
    vnd = c.currentVnode()
    mvnd = tree.currentVnode()
    mvnd.insertAfter( tnode( vnd.bodyString(), vnd.headString() ) )
    c.endUpdate()
#@nonl
#@-node:ekr.20040915144649.16:copyToChapter
#@+node:ekr.20040915145407:os_path_dirname
def os_path_dirname(path,encoding=None):

    """Normalize the path and convert it to an absolute path."""

    if iscStringIO:
        c = g.top()
        return os.path.dirname( c.mFileName )
    else:
        path = g.toUnicodeFileEncoding(path,encoding)
        path = os.path.dirname(path)
        path = g.toUnicodeFileEncoding(path,encoding)

    return path
#@nonl
#@-node:ekr.20040915145407:os_path_dirname
#@+node:ekr.20040915145407.1:editorHasFocus
def editorHasFocus( event , body ):

    c = body.c ; notebook = notebooks[ c ]
    
    if not hasattr( body, 'lastNode' ):
        body.lastNode = c.currentPosition()
        body.lastChapter = notebook.getcurselection()
    body.frame.body = body
    body.frame.bodyCtrl = body.bodyCtrl
    txt = body.lastNode.bodyString()
    if body.lastChapter != notebook.getcurselection():
        notebook.selectpage( body.lastChapter )
    if body.lastNode != c.currentPosition():
        body.frame.tree.select( body.lastNode )
    ip = body.lastNode.t.insertSpot
    body.deleteAllText()
    body.insertAtEnd( txt )
    if ip : body.setInsertionPoint( ip )
    body.colorizer.colorize( body.lastNode )
#@-node:ekr.20040915145407.1:editorHasFocus
#@+node:ekr.20040915145407.2:newEditor
def newEditor( c ):

    frame = frames[ c ]
    pbody = pbodies[ c ]
    name = str( len( pbody.panes() ) + 1 )
    zpane = pbody.add( name )
    panes = pbody.panes()
    i = 1.0 / len( panes )
    for z in pbody.panes():
        pbody.configurepane( z , size = i )
    pbody.updatelayout()
    l , r = addHeading( zpane )
    af = leoTkinterBody( frame, zpane )
    af.l = l
    af.r = r
    af.editorName = name
    twidgets[ af.bodyCtrl ] = af
    af.bodyCtrl.bind( "<FocusIn>", lambda event, body = af : editorHasFocus( event, body ) )
    af.setFontFromConfig()
    af.createBindings( frame )
    af.bodyCtrl.focus_set()
    cname = notebooks[ c ].getcurselection()
    af.l.configure( textvariable = getSV(cname , c ) )
    af.r.configure( text = c.currentVnode().headString() )
#@nonl
#@-node:ekr.20040915145407.2:newEditor
#@+node:ekr.20040915145407.3:removeEditor
def removeEditor( c ):

    pbody = pbodies[ c ]
    if len( pbody.panes() ) == 1: return None
    body = c.frame.body
    pbody.delete( body.editorName )
    pbody.updatelayout()

#@-node:ekr.20040915145407.3:removeEditor
#@+node:ekr.20040915145407.4:conversionToSimple
def conversionToSimple( c ):

    notebook = notebooks[ c ]
    vnd = c.rootVnode()
    while 1:
        n = vnd.next()
        if n == None:
            break
        else:
            vnd = n
    pagenames = notebook.pagenames()
    current = notebook.getcurselection()
    pagenames.remove( current )
    c.beginUpdate()
    for z in pagenames:
        index = notebook.index( z )
        page = notebook.page( index )
        tree = c.frame.trees[ page.sv ]
        rvNode = tree.rootVnode()
        while 1:
            nxt = rvNode.next()
            rvNode.moveAfter( vnd )
            if nxt: rvNode = nxt
            else:
                vnd = rvNode
                break
        notebook.delete( z )
    c.endUpdate()
#@-node:ekr.20040915145407.4:conversionToSimple
#@+node:ekr.20040915145407.5:conversionToChapters
def conversionToChapters( c ):

    notebook = notebooks[ c ]
    vnd = c.rootVnode()
    while 1:
        nxt = vnd.next()
        if nxt:
            makeNodeIntoChapter(c , nxt )
        else:
            break
#@-node:ekr.20040915145407.5:conversionToChapters
#@+node:ekr.20040915145407.6:makeNodeIntoChapter
def makeNodeIntoChapter( c, vnd = None ):

    if vnd == None:
        vnd = c.currentVnode()
    page = addPage( c )
    tree = c.frame.trees[ page.sv ]
    otree = c.frame.tree
    c.beginUpdate()
    c.frame.tree = tree
    root = tree.rootVnode()
    vnd.moveAfter( root )
    tree.setRootVnode( vnd )
    c.frame.tree = otree
    c.endUpdate()
#@nonl
#@-node:ekr.20040915145407.6:makeNodeIntoChapter
#@+node:ekr.20040915145407.7:openz
def openz(self,file,fileName):

    c = self.c ; frame = c.frame

    # Read the entire file into the buffer
    isZip = False
    if zipfile.is_zipfile( fileName ):
        isZip = True
        leoGlobals.openWithFileName( fileName, c , samewindow = False)
    else:
        self.fileBuffer = file.read()
        self.fileIndex = 0
    file.close()
    dir = g.os_path_dirname(fileName)
    if len(dir) > 0:
        c.openDirectory = dir
    self.topVnode = None

    c.beginUpdate()
    if not isZip:
        ok, ratio = self.getLeoFile(fileName,atFileNodesFlag=True)
    c.endUpdate()

    # delete the file buffer
    self.fileBuffer = ""
    if isZip: return True
    return ok
#@nonl
#@-node:ekr.20040915145407.7:openz
#@+node:ekr.20040915145407.8:walkChapters
def walkChapters( c = None, ignorelist = []):

    if c == None : c = g.top()
    pagenames = notebooks[ c ].pagenames()

    for z in pagenames:
        sv = getSV( z , c)
        tree = c.frame.trees[ sv ]
        v = tree.rootVnode()
        while v:
            if v not in ignorelist: yield v
            v = v.threadNext()
#@-node:ekr.20040915145407.8:walkChapters
#@+node:ekr.20040915145407.9:makeTabMenu & callbacks
def makeTabMenu( widget, notebook, c ):
    
    tmenu = Tk.Menu( widget, tearoff = 0 )
    widget.bind( '<Button-3>' , lambda event : tmenu.post( event.x_root , event.y_root ) )
    widget.tmenu = tmenu
    tmenu.add_command( command = tmenu.unpost )
    tmenu.add_separator()
    tmenu.add_command( label = 'Add Chapter', command = lambda c = c: addPage( c ) )
    rmenu = Tk.Menu( tmenu , tearoff = 0 )

    #@    @+others
    #@+node:ekr.20040915150738:remove
    def remove():
        rmenu.delete( 0 , Tk.END )
        pn = notebook.pagenames()
        for z in pn:
            def rmz( name = z):
                if len( notebook.pagenames() ) == 1: return
                sv = getSV( name )
                tree = c.frame.trees[ sv ]
                vnd = tree.rootVnode()
                cvnd = c.currentVnode()
                c.beginUpdate()
                otree = c.frame.tree
                c.frame.tree = tree
    
                while vnd:
                    v = vnd
                    nnd = vnd.next()
                    if nnd == None:
                        nnd = cvnd
                        vnd = None
                    else:
                        vnd = nnd
                    v.doDelete( nnd )
                c.frame.tree = otree
                c.endUpdate()
                notebook.delete( name )
    
            rmenu.add_command( label = z , command = rmz )
    #@nonl
    #@-node:ekr.20040915150738:remove
    #@+node:ekr.20040915150738.1:rename
    def rename( rnframes = {} ):
        name = notebook.getcurselection()
        frame = notebook.page( notebook.index( name ) )
        fr = frames[ g.top() ]
        if not rnframes.has_key( frame ):
            f = rnframes[ frame ] = Tk.Frame( frame )
            e = Tk.Entry( f , background = 'white', textvariable = frame.sv )
            b = Tk.Button( f , text = "Close" )
            e.pack( side = 'left' )
            b.pack( side = 'right' )
            def change():
                f.pack_forget()
            b.configure( command = change )
        else:
            f = rnframes[ frame ]
            if f.winfo_viewable() : return None
        fr.canvas.pack_forget()
        f.pack( side = 'bottom' )
        fr.canvas.pack( fill = 'both', expand = 1 )
    #@nonl
    #@-node:ekr.20040915150738.1:rename
    #@+node:ekr.20040915150738.2:setupMenu
    def setupMenu( menu , command , all = False):
            menu.delete( 0 , Tk.END )
            current = notebook.getcurselection()
            for z in notebook.pagenames():
                if z == current and not all: continue
                menu.add_command( label = z , command = lambda c = c , name = z : command( c, name ) )
    #@nonl
    #@-node:ekr.20040915150738.2:setupMenu
    #@-others
    
    rmenu.configure( postcommand = remove )
    #men.createMenuItemsFromTable( "Outline" , table )
    tmenu.add_cascade( menu = rmenu, label = "Remove Chapter" )
    tmenu.add_command( label = "Add/Change Title" , command = rename )
    
    opmenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( menu = opmenu , label = 'Node-Chapter Ops' )
    
    cmenu = Tk.Menu( opmenu, tearoff = 0 )
    movmenu = Tk.Menu( opmenu, tearoff = 0 )
    copymenu = Tk.Menu( opmenu, tearoff = 0 )
    swapmenu = Tk.Menu( opmenu, tearoff = 0 )
    searchmenu = Tk.Menu( opmenu, tearoff = 0 )
    
    opmenu.add_cascade( menu = cmenu, label = 'Clone To Chapter' )
    opmenu.add_cascade( menu = movmenu, label = 'Move To Chapter' )
    opmenu.add_cascade( menu = copymenu, label = 'Copy To Chapter' )
    opmenu.add_cascade( menu = swapmenu, label = 'Swap With Chapter' )
    opmenu.add_cascade( menu = searchmenu, label = 'Search and Clone To' )
    opmenu.add_command( label ="Make Node Into Chapter", command = lambda c=c: makeNodeIntoChapter( c ) )
    opmenu.add_command( label = "Add Trash Barrel", command = lambda c = c : addPage( c, "Trash" ) )
    
    cmenu.configure(
        postcommand = lambda menu = cmenu, command = cloneToChapter : setupMenu( menu, command ) )
    movmenu.configure(
        postcommand = lambda menu = movmenu, command = moveToChapter : setupMenu( menu, command ) )
    copymenu.configure(
        postcommand = lambda menu = copymenu, command = copyToChapter : setupMenu( menu, command ) )
    swapmenu.configure(
        postcommand = lambda menu = swapmenu, command = swapChapters : setupMenu( menu, command ) )
    searchmenu.configure(
        postcommand = lambda menu = searchmenu, command = regexClone: setupMenu( menu, command, all = True ) )

    edmenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( label = "Editor", menu = edmenu )
    edmenu.add_command( label = "Add Editor" , command = lambda c =c : newEditor( c ) )
    edmenu.add_command( label = "Remove Editor", command = lambda c = c : removeEditor( c ) )

    conmenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( menu = conmenu, label = 'Conversion' )
    conmenu.add_command( label = "Convert To Simple Outline", command = lambda c =c : conversionToSimple( c ) )
    conmenu.add_command( label = "Convert Simple Outline into Chapters", command = lambda c= c : conversionToChapters( c ) )

    iemenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( label = 'Import/Export', menu = iemenu )
    iemenu.add_command( label = "Import Leo File ", command = lambda c = c: importLeoFile(c ) )
    iemenu.add_command( label = "Export Chapter To Leo File", command = lambda c =c : exportLeoFile( c ) )
#@-node:ekr.20040915145407.9:makeTabMenu & callbacks
#@+node:ekr.20040915145407.10:addHeading
def addHeading( pane ):

    f = Tk.Frame( pane )
    f.pack( side = 'top' )
    l = Tk.Label( f )
    l.pack( side = 'left' )
    r = Tk.Label( f )
    r.pack( side = 'right' )
    return l , r
#@-node:ekr.20040915145407.10:addHeading
#@+node:ekr.20040915145407.11:endEditLabel
def endEditLabel (self):

    """End editing for self.editText."""

    c = self.c ; gui = g.app.gui
    p = self.editPosition()

    if p and p.edit_text():
        self.setUnselectedLabelState(p)
        self.setEditPosition(None)

    if p: # Redraw ancestor headlines.
        self.force_redraw() # Force a redraw of joined and ancestor headlines.
        c.frame.body.r.configure(text = p.headString())

    gui.set_focus(c,c.frame.bodyCtrl)
#@nonl
#@-node:ekr.20040915145407.11:endEditLabel
#@+node:ekr.20040915145407.12:swapChapters
def swapChapters( c, name ):

    tree = c.frame.tree
    tvnode = tree.rootVnode()
    notebook = notebooks[ c ]
    tree2 = c.frame.trees[ getSV( name, c ) ]
    t2vnode = tree2.rootVnode()
    tree2.setRootVnode( tvnode )
    tree.setRootVnode( t2vnode )
    c.beginUpdate()
    c.endUpdate()
    notebook = notebooks[ c ]
    cselection = notebook.getcurselection()
    tab1 = notebook.tab( cselection )
    tab2 = notebook.tab( name )
    tval1 = tab1.cget( 'text' )
    tval2 = tab2.cget( 'text' )
    tv1 = getSV( cselection, c )
    tv2 = getSV( name, c )
    val1 = tv1.get()
    val2 = tv2.get()
    if val2.isdigit() :
        tv1.set( notebook.index( cselection ) + 1 )
    else: tv1.set( val2 )
    if val1.isdigit() :
        tv2.set( notebook.index( name ) + 1 )
    else:
        tv2.set( val1 )

#@-node:ekr.20040915145407.12:swapChapters
#@+node:ekr.20040915145407.13:importLeoFile
def importLeoFile( c ):

    name = tkFileDialog.askopenfilename()
    if name:
        page = addPage( c , name )
        notebook = notebooks[ c ]
        notebook.selectpage( notebook.pagenames()[ - 1 ] )
        openWithFileNamez(name ,c , samewindow = False )
#@-node:ekr.20040915145407.13:importLeoFile
#@+node:ekr.20040915145407.14:exportLeoFile
def exportLeoFile( c ):
    import tkFileDialog
    name = tkFileDialog.asksaveasfilename()
    if name:
        if not name.endswith('.leo' ):
            name += '.leo'
        c.fileCommands.write_LEO_file( name, False, singleChapter = True )
#@-node:ekr.20040915145407.14:exportLeoFile
#@+node:ekr.20040915145407.15:trashDelete
#@+at 
#@nonl
# This is the main delete routine. It deletes the receiver's entire tree from 
# the screen. Because of the undo command we never actually delete vnodes or 
# tnodes.
#@-at
#@@c

def trashDelete (self, newVnode):

    """Unlinks the receiver, but does not destroy it. May be undone."""
    v = self ; c = v.c
    notebook = notebooks[ c ]
    pagenames = notebook.pagenames()
    pagenames = [ getSV( x, c ).get().upper() for x in pagenames ]
    name = getSV( notebook.getcurselection() , c ).get().upper()
    tsh = 'TRASH'
    if name != tsh and tsh in pagenames:
        index = pagenames.index( tsh )
        tree = c.frame.trees[ getSV( index, c )]
        trashnode = tree.rootVnode()
        otree = c.frame.tree
        c.frame.tree = tree
        self.moveAfter( trashnode )
        c.frame.tree = otree
        c.selectVnode( newVnode )
        return self

    v.setDirty() # 1/30/02: mark @file nodes dirty!
    v.destroyDependents()
    v.unjoinTree()
    v.unlink()
    # Bug fix: 1/18/99: we must set the currentVnode here!
    c.selectVnode(newVnode)
    # Update all clone bits.
    c.initAllCloneBits()
    return self # We no longer need dvnodes: vnodes contain all needed info.
#@-node:ekr.20040915145407.15:trashDelete
#@+node:ekr.20040915145407.16:regexClone
def regexClone( c , name ):

    if c == None: c = g.top()
    sv = getSV( name, c )
    tree = c.frame.trees[ sv ]

    def cloneWalk( result , entry, widget, c = c):
        txt = entry.get()
        widget.deactivate()
        widget.destroy()
        if result == 'Cancel': return None
        import re
        regex = re.compile( txt )
        rt = tree.rootVnode()
        stnode = tnode( '', txt )
        otree = c.frame.tree
        c.frame.tree = tree
        snode = vnode( c, stnode)
        snode.moveAfter( rt )
        ignorelist = [ snode ]
        it = walkChapters( c , ignorelist = ignorelist)
        for z in it:
            f = regex.match( z.bodyString() )
            if f:
                clone = z.clone( z )
                i = snode.numberOfChildren()
                clone.moveToNthChildOf( snode, i)
                ignorelist.append( clone )

        c.frame.tree = otree
        notebook = notebooks[ c ]
        notebook.selectpage( name )
        c.selectVnode( snode )
        snode.expand()
        c.beginUpdate()
        c.endUpdate()

    sd = Pmw.PromptDialog( c.frame.top,
    title = 'Search and Clone',
    buttons = ( 'Search', 'Cancel' ),
    command =cloneWalk )
    entry = sd.component( 'entry' )
    sd.configure( command =
        lambda result, entry = entry, widget = sd:
            cloneWalk( result, entry, widget ) )
    sd.activate( geometry = 'centerscreenalways' )






#@-node:ekr.20040915145407.16:regexClone
#@+node:ekr.20040915145407.17:select
def select (self,p,updateBeadList=True):
    
    if not p: return
    
    c = p.c
    self.frame.body.lastNode = p
    self.frame.body.lastChapter = notebooks[c].getcurselection()
    c.frame.body.r.configure( text = p.headString() )

    return old_select(self,p,updateBeadList )
#@nonl
#@-node:ekr.20040915145407.17:select
#@-others

old_select = leoTkinterTree.leoTkinterTree.select

if Pmw and Tk:
    #@    << override Leo's core methods >>
    #@+node:ekr.20040915145728:<< override Leo's core methods >>
    leoTkinterFrame.leoTkinterFrame.finishCreate = finishCreate
    leoTkinterTree.leoTkinterTree.select = select
    leoTkinterTree.leoTkinterTree.endEditLabel = endEditLabel
    
    leoGlobals.openWithFileName = openWithFileNamez
    leoGlobals.os_path_dirname = os_path_dirname
    
    leoFileCommands.fileCommands.write_LEO_file = write_LEO_filez
    leoFileCommands.fileCommands.getLeoFile = getLeoFile
    leoFileCommands.fileCommands.open = openz
    
    leoNodes.vnode.doDelete = trashDelete
    #@nonl
    #@-node:ekr.20040915145728:<< override Leo's core methods >>
    #@nl
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040915144649.2:@thin chapters.py
#@-leo
