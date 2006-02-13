#@+leo-ver=4-thin
#@+node:ekr.20060213023839.3:@thin chapters2.py
#@<<docstring>>
#@+node:ekr.20060213023839.4:<<docstring>>
'''This plugin creates separate outlines called "chapters" within a single .leo file.  Clones work between Chapters.

**Warning**: This plugin must be considered **buggy** and **unsafe**.  Use with extreme caution.

Requires Python Mega Widgets and Leo 4.2 or above.

Numbered tabs at the top of the body pane represent each chapter.  Right clicking the tab will show a popup menu containing commands.  These commands allow you to:
    
- insert and delete chapters.
- add names to chapters.
- split the body pane to create multiple "editors".
- create a "trash barrel that hold all deleted nodes.
- import and export outlines and chapters.
- create a pdf file from your chapters (requires reportlab toolkit at http://www.reportlab.org).
- and more...
 
Warnings:
    
- This plugin makes substantial changes to Leo's core.
- Outlines containing multiple chapters are stored as a zipped file that can only be read when this plugin has been enabled.
'''
#@nonl
#@-node:ekr.20060213023839.4:<<docstring>>
#@nl

# To do:  Find/Change does not appear to work.
# To do: replace all v refs by p refs.
# ***Testing***.

#@@language python
#@@tabwidth -4

__version__ = "0.101"
#@<< version history >>
#@+node:ekr.20060213023839.5:<< version history >>
#@@nocolor

#@+at 
# v .101 EKR: 2-13-06 Created from chapters.py.
# This will be the new working version of the chapters plugin.
#@-at
#@nonl
#@-node:ekr.20060213023839.5:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20060213023839.7:<< imports >>
import leoGlobals as g
import leoColor
import leoCommands
import leoFileCommands
import leoFrame
import leoNodes
import leoPlugins
import leoTkinterFrame
import leoTkinterMenu
import leoTkinterTree

Tk  = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
Pmw = g.importExtension("Pmw",    pluginName=__name__,verbose=True)
   
from leoTkinterFrame import leoTkinterLog
from leoTkinterFrame import leoTkinterBody

import copy
import cStringIO
import os
import string
import sys
import time
import tkFileDialog
import tkFont
import zipfile
#@nonl
#@-node:ekr.20060213023839.7:<< imports >>
#@nl
#@<< remember the originals for decorated methods >>
#@+middle:ekr.20060213023839.8:Module level
#@+node:ekr.20060213023839.1:<< remember the originals for decorated methods >>
# Remember the originals of the 10 overridden methods...

# Define these at the module level so they are defined early in the load process.
old_createCanvas            = leoTkinterFrame.leoTkinterFrame.createCanvas
old_createControl           = leoTkinterFrame.leoTkinterBody.createControl
old_doDelete                = leoNodes.position.doDelete
old_editLabel               = leoTkinterTree.leoTkinterTree.endEditLabel
old_getLeoFile              = leoFileCommands.fileCommands.getLeoFile
old_open                    = leoFileCommands.fileCommands.open
old_os_path_dirname         = g.os_path_dirname
old_select                  = leoTkinterTree.leoTkinterTree.select
old_tree_init               = leoTkinterTree.leoTkinterTree.__init__
old_write_Leo_file          = leoFileCommands.fileCommands.write_Leo_file
#@nonl
#@-node:ekr.20060213023839.1:<< remember the originals for decorated methods >>
#@-middle:ekr.20060213023839.8:Module level
#@nl

# Solve problems with string.atoi...
import string
string.atoi = int

if 1:
    # The global data.
    controllers = {} # Keys are commanders, values are chapterControllers.
    iscStringIO = False # Used by g.os_path_dirname
    stringIOCommander = None # Used by g.os_path_dirname
else:
    #@    << globals >>
    #@+node:ekr.20060213023839.22:<< globals >>
    chapters = {}
    editorNames = {}
    frames = {}
    iscStringIO = False
    notebooks = {}
    pbodies = {}
    twidgets = {}
    #@nonl
    #@-node:ekr.20060213023839.22:<< globals >>
    #@nl

#@+others
#@+node:ekr.20060213023839.8:Module level
#@+node:ekr.20060213023839.9:init
def init ():
    
    # This code will work only on the 4.x code base.
    # Not for unit testing:  modifies core classes.
    ok = (
        hasattr(leoNodes,'position') and
        hasattr(leoNodes.position,'doDelete') and
        Pmw and not g.app.unitTesting
    )

    if ok:
        if g.app.gui is None: 
            g.app.createTkGui(__file__)
    
        if g.app.gui.guiName() == "tkinter":
            #@            << override various methods >>
            #@+node:ekr.20060213023839.10:<< override various methods >>
            # Override the 10 originals...
            
            leoTkinterFrame.leoTkinterFrame.createCanvas    = new_createCanvas
            leoTkinterFrame.leoTkinterBody.createControl    = new_createControl
            leoNodes.position.doDelete                      = new_doDelete
            leoTkinterTree.leoTkinterTree.endEditLabel      = new_endEditLabel
            leoFileCommands.fileCommands.getLeoFile         = new_getLeoFile
            leoFileCommands.fileCommands.open               = new_open
            leoTkinterTree.leoTkinterTree.select            = new_select
            leoTkinterTree.leoTkinterTree.__init__          = new_tree_init
            g.os_path_dirname                               = new_os_path_dirname
            leoFileCommands.fileCommands.write_Leo_file     = new_write_Leo_file
            #@nonl
            #@-node:ekr.20060213023839.10:<< override various methods >>
            #@nl
            g.plugin_signon( __name__ )
            
    return ok
#@nonl
#@-node:ekr.20060213023839.9:init
#@+node:ekr.20060213023839.11:decorated Leo functions
#@+at
# I prefer decorating Leo functions as opposed to patching them.  Patching 
# them leads to long term incompatibilites with Leo and the plugin.  Though 
# this happens anyway with code evolution/changes, this makes it worse.  Thats 
# my experience with it. :)
#@-at
#@@c
#@+others
#@+node:ekr.20060213023839.12:new_createCanvas (leoTkinterFrame)  (creates chapterControllers)
def new_createCanvas (self,parentFrame):
    
    # self is c.frame
    c = self.c
    if g.app.unitTesting:
        return old_createCanvas(self,page)
    else:
        global controllers
        controllers [c] = cc = chapterController(c,self,parentFrame)
        return cc.createCanvas(self,parentFrame)

    # else:
        # c = self.c
        # if c in frames:
            # notebook = notebooks.get(c)
        # else:
            # global controllers
            # controllers [c] = cc = chapterController(c,parentFrame)
            # frames [c] = self
            # notebook = createNoteBook(c,parentFrame)
#@nonl
#@-node:ekr.20060213023839.12:new_createCanvas (leoTkinterFrame)  (creates chapterControllers)
#@+node:ekr.20060213023839.13:new_os_path_dirname (leoGlobals) (ok)
def new_os_path_dirname (path,encoding=None):
    
    # These must be globals because they are used in g.os_path_dirname.
    global iscStringIO,stringIOCommander

    if iscStringIO:
        c = stringIOCommander
        return os.path.dirname(c.mFileName)
    else:
        global old_os_path_dirname
        return old_os_path_dirname(path,encoding)
#@nonl
#@-node:ekr.20060213023839.13:new_os_path_dirname (leoGlobals) (ok)
#@+node:ekr.20060213023839.14:new_createControl (leoTkinterBody) (revised)
def new_createControl (self,frame,parentFrame):

    # self is c.frame.body
    if g.app.unitTesting:
        return old_createControl(self,frame,parentFrame)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.createControl(self,frame,parentFrame)
#@nonl
#@-node:ekr.20060213023839.14:new_createControl (leoTkinterBody) (revised)
#@+node:ekr.20060213023839.15:new_doDelete (position) (revised)
def new_doDelete (self,newPosition):
    
    # self is position.
    if g.app.unitTesting:
        return old_doDelete(self,newPosition)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.doDelete(self,newPosition)
#@nonl
#@-node:ekr.20060213023839.15:new_doDelete (position) (revised)
#@+node:ekr.20060213023839.16:new_endEditLabel (leoTkinterTree) (revised)
def new_endEditLabel (self):
    
    # self is a c.frame.tree
    if g.app.unitTesting:
        return old_editLabel(self)
    else:
        cc = controllers.get(self.c)
        return cc.endEditLabel(self)
#@nonl
#@-node:ekr.20060213023839.16:new_endEditLabel (leoTkinterTree) (revised)
#@+node:ekr.20060213023839.17:new_getLeoFile (fileCommands) (revised)
def new_getLeoFile (self,fileName,readAtFileNodesFlag=True,silent=False):
    
    # self is c.fileCommands
    if g.app.unitTesting:
        return old_getLeoFile(self,fileName,readAtFileNodesFlag,silent)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.getLeoFile(self,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:ekr.20060213023839.17:new_getLeoFile (fileCommands) (revised)
#@+node:ekr.20060213023839.18:new_open (fileCommands) (revised)
def new_open (self,file,fileName,readAtFileNodesFlag=True,silent=False):
    
    # self = fileCommands
    if g.app.unitTesting:
        return old_open(fc,file,fileName,readAtFileNodesFlag,silent)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.open(self,file,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:ekr.20060213023839.18:new_open (fileCommands) (revised)
#@+node:ekr.20060213023839.19:new_select (leoTkinterTree) (revised)
def new_select (self,p,updateBeadList=True):
    
    # self is c.frame.tree
    if g.app.unitTesting:
        return old_select(self,p,updateBeadList)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.select(self,p,updateBeadList)
#@nonl
#@-node:ekr.20060213023839.19:new_select (leoTkinterTree) (revised)
#@+node:ekr.20060213023839.20:new_tree_init (leoTkinterTree) revised
def new_tree_init (self,c,frame,canvas):
    
    # self is c.frame.tree
    if g.app.unitTesting:
        return old_tree_init(self,c,frame,canvas)
    else:
        global controllers
        cc = controllers.get(c)
        return cc.treeInit(self,c,frame,canvas)
#@nonl
#@-node:ekr.20060213023839.20:new_tree_init (leoTkinterTree) revised
#@+node:ekr.20060213023839.21:new_write_Leo_file
def new_write_Leo_file (self,fileName,outlineOnlyFlag,singleChapter=False):
    
    # self is c.frame.tree
    if g.app.unitTesting:
        return old_write_Leo_file(self,fileName,outlineOnlyFlag)
    else:
        cc = controllers.get(self.c)
        return cc.write_Leo_file(self,fileName,outlineOnlyFlag,singleChapter=False)
#@nonl
#@-node:ekr.20060213023839.21:new_write_Leo_file
#@-others
#@nonl
#@-node:ekr.20060213023839.11:decorated Leo functions
#@-node:ekr.20060213023839.8:Module level
#@+node:ekr.20060213023839.23:class Chapter
class Chapter:
    '''The fundamental abstraction in the Chapters plugin.
       It enables the tracking of Chapters tree information.'''
       
    #@    @+others
    #@+node:ekr.20060213023839.24:__init__
    def __init__ (self,c,tree,frame,canvas):
        
        g.trace('Chapter',c.fileName())
    
        self.c = c
        self.tree = tree
        self.frame = frame
        self.canvas = canvas
        self.treeBar = frame.treeBar
    
        if hasattr(c,'cChapter'):
            t = leoNodes.tnode('','New Headline')
            v = leoNodes.vnode(c,t)
            p = leoNodes.position(c,v,[])
            self.cp = p.copy()
            self.rp = p.copy()
            self.tp = p.copy()
        else:
            c.cChapter = self
            self.cp = c._currentPosition or c.nullPosition()
            self.tp = c._topPosition or c.nullPosition()
            self.rp = c._rootPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20060213023839.24:__init__
    #@+node:ekr.20060213023839.25:_saveInfo
    def _saveInfo (self):
    
        c = self.c
        self.cp = c._currentPosition or c.nullPosition()
        self.rp = c._rootPosition or c.nullPosition()
        self.tp = c._topPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20060213023839.25:_saveInfo
    #@+node:ekr.20060213023839.26:setVariables
    def setVariables (self):
    
        c = self.c
        frame = self.frame
        frame.tree = self.tree
        frame.canvas = self.canvas
        frame.treeBar = self.treeBar
        c._currentPosition = self.cp
        c._rootPosition = self.rp
        c._topPosition = self.tp
    #@nonl
    #@-node:ekr.20060213023839.26:setVariables
    #@+node:ekr.20060213023839.27:makeCurrent
    def makeCurrent (self):
    
        c = self.c
        c.cChapter._saveInfo()
        c.cChapter = self
        self.setVariables()
        c.redraw()
        self.canvas.update_idletasks()
    #@nonl
    #@-node:ekr.20060213023839.27:makeCurrent
    #@-others
#@nonl
#@-node:ekr.20060213023839.23:class Chapter
#@+node:ekr.20060213023839.28:class chapterController
class chapterController:
    
    '''A per-commander controller.'''
    
    #@    @+others
    #@+node:ekr.20060213023839.29:Birth...
    #@+node:ekr.20060213023839.30: ctor chapterController
    def __init__ (self,c,frame,parentFrame):
        
        self.c = c
        self.frame = frame
        self.parentFrame = parentFrame
    
        self.chapters = {} # Keys are stringVars.
        self.editorNames = {}
        
        self.pbodies = {}
        self.rnframes = {}
        self.twidgets = {}
        
        # self.frames = {}
        # frames [c] = self
        # self.notebooks = {}
    
        self.nameMaker = self.makeNameMaker()
        self.createNoteBook(parentFrame) # sets self.nb
    #@nonl
    #@-node:ekr.20060213023839.30: ctor chapterController
    #@+node:ekr.20060213023839.31:addPage
    def addPage (self,name=None):
    
        c = self.c ; frame = self.frame ; nb = self.nb
    
        name = name or str(len(nb.pagenames())+1)
        o_chapter = c.cChapter
        g.trace(name)
        otree, page = self.constructTree(frame,name)
        c.cChapter.makeCurrent()
        o_chapter.makeCurrent()
        return page
    #@-node:ekr.20060213023839.31:addPage
    #@+node:ekr.20060213023839.32:constructTree
    def constructTree (self,frame,name):
    
        c = self.c ; nb = self.nb
        canvas = treeBar = tree = None
        if frame.canvas:
            canvas = frame.canvas
            treeBar = frame.treeBar
            tree = frame.tree
        sv = Tk.StringVar()
        sv.set(name)
        frame.canvas = canvas = frame.createCanvas(parentFrame=None)
        frame.tree = leoTkinterTree.leoTkinterTree(frame.c,frame,frame.canvas)
        frame.tree.setColorFromConfig()
        indx = nb.index(nb.pagenames()[-1])
        tab = nb.tab(indx)
        tnum = str(len(nb.pagenames()))
        tab.configure(text=tnum)
        hull = nb.component('hull')
        tab.bind('<Button-3>',lambda event,hull=hull: hull.tmenu.post(event.x_root,event.y_root))
        return tree, nb.page(nb.pagenames()[-1])
    #@nonl
    #@-node:ekr.20060213023839.32:constructTree
    #@+node:ekr.20060213023839.33:createBalloon
    def createBalloon (self,tab,sv):
    
        'Create a balloon for a widget.' ''
    
        balloon = Pmw.Balloon(tab,initwait=100)
        balloon.bind(tab,'')
        hull = balloon.component('hull')
        def blockExpose (event):
            if sv.get() == '':
                 hull.withdraw()
        hull.bind('<Expose>',blockExpose,'+')
        balloon._label.configure(textvariable=sv)
    #@nonl
    #@-node:ekr.20060213023839.33:createBalloon
    #@+node:ekr.20060213023839.34:createNoteBook
    def createNoteBook (self,parentFrame):
    
        '''Construct a NoteBook widget for a frame.'''
    
        c = self.c
        self.nb = nb = Pmw.NoteBook(parentFrame,borderwidth=1,pagemargin=0)
        hull = nb.component('hull')
        self.makeTabMenu(hull)
        def raiseCallback(name,self=self):
            return self.setTree(name)
        nb.configure(raisecommand=raiseCallback)
        
        def lowerCallback(name,self=self):
            return self.lowerPage(name)
        nb.configure(lowercommand=lowerCallback)
    
        nb.pack(fill='both',expand=1)
        nb.nameMaker = self.nameMaker
        return nb
    #@nonl
    #@-node:ekr.20060213023839.34:createNoteBook
    #@+node:ekr.20060213023839.35:createPanedWidget
    def createPanedWidget (self,parentFrame):
    
        '''Construct a new panedwidget for a frame.'''
    
        c = self.c
        pbody = Pmw.PanedWidget(parentFrame,orient='horizontal')
        pbody.pack(expand=1,fill='both')
        self.pbodies [c] = pbody
        parentFrame = self.newEditorPane()
        return parentFrame
    #@nonl
    #@-node:ekr.20060213023839.35:createPanedWidget
    #@+node:ekr.20060213023839.36:makeNameMaker
    def makeNameMaker (self):
    
        '''Create a numbering mechanism for tabs.'''
    
        def nameMaker ():
            i = 0
            while 1:
                if len(self.nb.pagenames())== 0: i = 0
                i += 1
                yield str(i)
    
        return nameMaker()
    #@nonl
    #@-node:ekr.20060213023839.36:makeNameMaker
    #@+node:ekr.20060213023839.37:newEditor
    def newEditor (self):
    
        c = self.c ; frame = self.frame ; nb = self.nb ; pbody = self.pbodies[c]
        zpane = self.newEditorPane()
        af = leoTkinterBody(frame,zpane)
        c.frame.bodyCtrl = af.bodyCtrl
        af.setFontFromConfig()
        af.createBindings()
        af.bodyCtrl.focus_set()
        cname = nb.getcurselection()
        af.l.configure(textvariable=self.getStringVar(cname))
        af.r.configure(text=c.currentPosition().headString())
    #@nonl
    #@-node:ekr.20060213023839.37:newEditor
    #@+node:ekr.20060213023839.38:newEditorPane
    def newEditorPane (self):
        
        c = self.c
        names = self.pbodies [c].panes()
        name = names and str(int(names[-1])+1) or '1'
        zpane = self.pbodies [c].add(name)
        self.editorNames [zpane] = name
        return zpane
    #@nonl
    #@-node:ekr.20060213023839.38:newEditorPane
    #@-node:ekr.20060213023839.29:Birth...
    #@+node:ekr.20060213023839.39:Called from decorated functions
    #@+node:ekr.20060213023839.40:createCanvas
    def createCanvas (self,frame,parentFrame):
        
        nb = self.nb
        pname = self.nameMaker.next()
        page = nb.add(pname)
        indx = nb.index(pname)
        tab = nb.tab(indx)
        if indx == 0:
            tab.configure(background='grey',foreground='white')
        canvas = old_createCanvas(frame,page) # Substitute page for parentFrame.
        hull = nb.component('hull')
        tab.bind('<Button-3>',lambda event: hull.tmenu.post(event.x_root,event.y_root))
        page.sv = sv = Tk.StringVar()
        self.createBalloon(tab,sv)
        canvas.name = pname
        return canvas
    #@nonl
    #@-node:ekr.20060213023839.40:createCanvas
    #@+node:ekr.20060213023839.41:createControl
    def createControl(self,body,frame,parentFrame):
    
        c = self.c ; nb = self.nb
        if c not in self.pbodies:
            parentFrame = self.createPanedWidget(parentFrame)
        pbody = self.pbodies [c]
        l, r = self.addHeading(parentFrame)
        ctrl = old_createControl(body,frame,parentFrame)
        def focusInCallback(event,self=self,frame=frame):
            return self.getGoodPage(event,frame.body)
        ctrl.bind("<FocusIn>",focusInCallback,'+')
        i = 1.0 / len(pbody.panes())
        for z in pbody.panes():
            pbody.configurepane(z,size=i)
        pbody.updatelayout()
        frame.body.l = l
        frame.body.r = r
        frame.body.editorName = self.editorNames [parentFrame]
        if frame not in self.twidgets:
            self.twidgets [frame] = []
        self.twidgets [frame].append(frame.body)
        l.configure(textvariable=self.getStringVar(nb.getcurselection()))
        return ctrl
    #@nonl
    #@-node:ekr.20060213023839.41:createControl
    #@+node:ekr.20060213023839.42:doDelete
    def doDelete (self,p,newPosition):
        
        c = self.c ; nb = self.nb ; pagenames = nb.pagenames()
        
        pagenames = [self.setStringVar(x).get().upper() for x in pagenames]
        nbnam = nb.getcurselection()
        if nbnam != None:
            name = self.getStringVar(nb.getcurselection()).get().upper()
        else: name = 'TRASH'
        tsh = 'TRASH'
        if name != tsh and tsh in pagenames:
            index = pagenames.index(tsh)
            trchapter = self.chapters [self.getStringVar(index)]
            trashnode = trchapter.rp
            trchapter.setVariables()
            p.moveAfter(trashnode)
            c.cChapter.setVariables()
            c.selectPosition(newPosition)
            return p
        return old_doDelete(p,newPosition)
    #@-node:ekr.20060213023839.42:doDelete
    #@+node:ekr.20060213023839.43:endEditLabel
    def endEditLabel (self,tree):
        
        c = self.c ; p = c.currentPosition() ; h = p.headString()
    
        if p and h and hasattr(c.frame.body,'r'):
             c.frame.body.r.configure(text=h)
    
        return old_editLabel(tree)
    #@nonl
    #@-node:ekr.20060213023839.43:endEditLabel
    #@+node:ekr.20060213023839.44:getLeoFile
    def getLeoFile (self,fc,fileName,readAtFileNodesFlag=True,silent=False):
        
        global iscStringIO # For communication with g.os_path_dirname
    
        if iscStringIO:
            def dontSetReadOnly (self,name,value):
                if name not in ('read_only','tnodesDict'):
                    self.__dict__ [name] = value
    
            self.read_only = False
            self.__class__.__setattr__ = dontSetReadOnly
    
        rt = old_getLeoFile(fc,fileName,readAtFileNodesFlag,silent)
    
        if iscStringIO:
            del self.__class__.__setattr__
    
        return rt
    #@nonl
    #@-node:ekr.20060213023839.44:getLeoFile
    #@+node:ekr.20060213023839.45:select
    def select (self,tree,p,updateBeadList=True):
    
        c = p.v.c ; h = p.headString() ; nb = self.nb
    
        c.frame.body.lastPosition = p
        return_val = old_select(tree,p,updateBeadList)
        c.frame.body.lastChapter = nb.getcurselection()
    
        if hasattr(p.c.frame.body,'r'):
            c.frame.body.r.configure(text=h)
    
        return return_val
    #@nonl
    #@-node:ekr.20060213023839.45:select
    #@+node:ekr.20060213023839.46:open
    def open (self,fc,file,fileName,readAtFileNodesFlag=True,silent=False):
    
        c = self.c
    
        if zipfile.is_zipfile(fileName):
            # Set globals for g.os_path_dirname
            global iscStringIO, stringIOCommander
            iscStringIO = True ; stringIOCommander = c
            chapters = openChaptersFile(fileName)
            g.es(str(len(chapters))+" Chapters To Read",color='blue')
            self.insertChapters(chapters)
            g.es("Finished Reading Chapters",color='blue')
            iscStringIO = False
            return True
        else:
            return old_open(fc,file,fileName,readAtFileNodesFlag,silent)
    #@nonl
    #@-node:ekr.20060213023839.46:open
    #@+node:ekr.20060213023839.47:treeInit
    def treeInit (self,tree,c,frame,canvas):
        
        sv = self.getStringVar(canvas.name)
        
        old_tree_init(tree,c,frame,canvas)
    
        self.chapters [sv] = Chapter(c,tree,frame,canvas)
    #@nonl
    #@-node:ekr.20060213023839.47:treeInit
    #@+node:ekr.20060213023839.48:write_Leo_file & helper
    def write_Leo_file (self,fc,fileName,outlineOnlyFlag,singleChapter=False):
    
        c = self.c ; nb = self.nb ; pagenames = nb.pagenames()
    
        if len(pagenames) > 1 and not singleChapter:
            chapList = []
            fc.__class__.__setattr__ = getMakeStringIO(chapList)
            rv = self.writeChapters(fc,fileName,pagenames,c,outlineOnlyFlag)
            if rv: zipChapters(fileName,pagenames,c,chapList)
            del self.__class__.__setattr__
            return rv
        else:
            global old_write_Leo_file
            return old_write_Leo_file(fc,fileName,outlineOnlyFlag)
    #@nonl
    #@+node:ekr.20060213023839.49:writeChapters
    def writeChapters (self,fc,fileName,pagenames,outlineOnlyFlag):
    
        '''Writes Chapters to StringIO instances.'''
        
        c = self.c
    
        for z in pagenames:
            sv = self.getStringVar(z)
            chapter = self.chapters [sv]
            chapter.setVariables()
            rv = old_write_Leo_file(fc,fileName,outlineOnlyFlag)
    
        c.cChapter.setVariables()
        return rv
    #@nonl
    #@-node:ekr.20060213023839.49:writeChapters
    #@-node:ekr.20060213023839.48:write_Leo_file & helper
    #@-node:ekr.20060213023839.39:Called from decorated functions
    #@+node:ekr.20060213023839.50:tab menu stuff
    #@+node:ekr.20060213023839.51:makeTabMenu
    def makeTabMenu (self,widget):
        '''Creates a tab menu.'''
        c = self.c ; nb = self.nb
        tmenu = Tk.Menu(widget,tearoff=0)
        widget.bind('<Button-3>',lambda event: tmenu.post(event.x_root,event.y_root))
        widget.tmenu = tmenu
        tmenu.add_command(command=tmenu.unpost)
        tmenu.add_separator()
        #ac = self.getAddChapter()
        #tmenu.add_command(label='Add Chapter',command=ac)
        tmenu.add_command(label='Add Chapter',command=self.addChapter)
        self.rmenu = rmenu = Tk.Menu(tmenu,tearoff=0)
        #remove = self.getRemove(rmenu)
        #rmenu.configure(postcommand=remove)
        rmenu.configure(postcommand=self.removeChapter)
        tmenu.add_cascade(menu=rmenu,label="Remove Chapter")
        #rename = self.getRename()
        #tmenu.add_command(label="Add/Change Title",command=rename)
        tmenu.add_command(label="Add/Change Title",command=self.renameChapter)
        opmenu = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(menu=opmenu,label='Node-Chapter Ops')
        cmenu = Tk.Menu(opmenu,tearoff=0)
        movmenu = Tk.Menu(opmenu,tearoff=0)
        copymenu = Tk.Menu(opmenu,tearoff=0)
        swapmenu = Tk.Menu(opmenu,tearoff=0)
        searchmenu = Tk.Menu(opmenu,tearoff=0)
        opmenu.add_cascade(menu=cmenu,label='Clone To Chapter')
        opmenu.add_cascade(menu=movmenu,label='Move To Chapter')
        opmenu.add_cascade(menu=copymenu,label='Copy To Chapter')
        opmenu.add_cascade(menu=swapmenu,label='Swap With Chapter')
        opmenu.add_cascade(menu=searchmenu,label='Search and Clone To')
        opmenu.add_command(label="Make Node Into Chapter",command=self.makeNodeIntoChapter)
        #mkTrash = self.getMakeTrash()
        #opmenu.add_command(label="Add Trash Barrel",command=self.mkTrash)
        opmenu.add_command(label="Add Trash Barrel",command=self.addTrashBarrel)
        #lambda c = c: mkTrash(c))
        opmenu.add_command(label='Empty Trash Barrel',command=self.emptyTrash)
    
        #lambda self=self: self.emptyTrash(notebook,c))
        # setupMenu = self.getSetupMenu()
        # cmenu.configure(
            # postcommand = lambda menu = cmenu, command = cloneToChapter: setupMenu(menu,command))
        # movmenu.configure(
            # postcommand = lambda menu = movmenu, command = moveToChapter: setupMenu(menu,command))
        # copymenu.configure(
            # postcommand = lambda menu = copymenu, command = copyToChapter: setupMenu(menu,command))
        #---
        def cloneToChapterCallback (self=self,menu=cmenu):
            self.setupMenu(menu,self.cloneToChapter)
        cmenu.configure(postcommand=cloneToChapterCallback)
    
        def moveToChapterCallback(self=self,menu=movmenu):
            self.setupMenu(menu,self.moveToChapter)
        movmenu.configure(postcommand=moveToChapterCallback)
        
        def copyToChapterCallback(self=self,menu=copymenu):
            self.setupMenu(menu,self.copyToChapter)
        copymenu.configure(postcommand=copyToChapterCallback)
        
        def swapChaptersCallback  (self=self,menu=swapmenu):
            self.setupMenu(menu,self.swapChapters)
        swapmenu.configure(postcommand=swapChaptersCallback)
        
        def searchChaptersCallback  (self=self,menu=searchmenu):
            self.setupMenu(menu,self.regexClone,all=True)
        searchmenu.configure(postcommand=searchChaptersCallback)
            
        edmenu = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label="Editor",menu=edmenu)
        edmenu.add_command(label="Add Editor",command=self.newEditor)
        edmenu.add_command(label="Remove Editor",command=self.removeEditor)
        conmenu = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(menu=conmenu,label='Conversion')
        conmenu.add_command(
            label = "Convert To Simple Outline",command=self.conversionToSimple)
        conmenu.add_command(
            label = "Convert Simple Outline into Chapters",command=self.conversionToChapters)
        iemenu = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label='Import/Export',menu=iemenu)
        iemenu.add_command(label="Import Leo File ",command=self.importLeoFile)
        iemenu.add_command(label="Export Chapter To Leo File",command=self.exportLeoFile)
        indmen = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label='Index',menu=indmen)
        indmen.add_command(label='Make Index',command=self.viewIndex)
        indmen.add_command(label='Make Regex Index',command=self.regexViewIndex)
        try:
            import reportlab
            tmenu.add_command(label='Convert To PDF',command=self.doPDFConversion)
        except Exception:
            g.es("no reportlab")
    #@nonl
    #@-node:ekr.20060213023839.51:makeTabMenu
    #@+node:ekr.20060213023839.52:tab callbacks
    #@+node:ekr.20060213023839.53:addChapter
    def addChapter (self,event=None):
        
        nb = self.nb
        cname = nb.getcurselection()
        self.addPage()
        self.renumber()
    #@-node:ekr.20060213023839.53:addChapter
    #@+node:ekr.20060213023839.54:removeChapter & helper
    def removeChapter (self,event=None):
    
        c = self.c ; nb = self.nb ; rmenu = self.rmenu
    
        rmenu.delete(0,'end')
        pn = nb.pagenames()
        for i, z in enumerate(pn):
            i += 1
            # self.removeOneChapter(z)
            rmenu.add_command(label=str(i),command=self.removeOneChapter)
    #@nonl
    #@+node:ekr.20060213023839.55:removeOneChapter
    def removeOneChapter (self,name):
        
        c = self.c ; nb = self.nb
        if len(nb.pagenames()) == 1: return
        sv = self.getStringVar(name)
        chapter = self.chapters [sv]
        tree = chapter.tree
        vnd = chapter.rp
        cvnd = c.cChapter.cp
        c.beginUpdate()
        try:
            otree = c.cChapter.tree
            c.frame.tree = tree
            if vnd:
                v = vnd
                nnd = vnd.next()
                if nnd == None:
                    nnd = vnd.insertAfter()
                    vnd = None
                v.doDelete(nnd)
            c.frame.tree = otree
        finally:
            c.endUpdate()
        nb.delete(name)
        if tree != otree:
            c.selectPosition(cvnd)
        if tree == otree:
            pnames = nb.pagenames()
            nb.selectpage(pnames[0])
            c.selectPosition(c.currentPosition())
            c.redraw()
        self.renumber()
    #@nonl
    #@-node:ekr.20060213023839.55:removeOneChapter
    #@-node:ekr.20060213023839.54:removeChapter & helper
    #@+node:ekr.20060213023839.56:renameChapter
    def renameChapter (self,event=None):
    
        c = self.c ; nb = self.nb
        name = nb.getcurselection()
        frame = nb.page(nb.index(name))
        fr = self.frame
        if not self.rnframes.has_key(frame):
            f = self.rnframes [frame] = Tk.Frame(frame)
            e = Tk.Entry(f,background='white',textvariable=frame.sv)
            b = Tk.Button(f,text="Close")
            e.pack(side='left')
            b.pack(side='right')
            def change ():
                f.pack_forget()
            b.configure(command=change)
        else:
            f = self.rnframes [frame]
            if f.winfo_viewable(): return None
        fr.canvas.pack_forget()
        f.pack(side='bottom')
        fr.canvas.pack(fill='both',expand=1)
    #@nonl
    #@-node:ekr.20060213023839.56:renameChapter
    #@+node:ekr.20060213023839.57:addTrashBarrel
    def addTrashBarrel (self,event=None):
    
        c = self.c ; nb = self.nb
        self.addPage('Trash')
        pnames = nb.pagenames()
        sv = self.getStringVar(pnames[-1])
        sv.set('Trash')
        self.renumber()
    #@nonl
    #@-node:ekr.20060213023839.57:addTrashBarrel
    #@+node:ekr.20060213023839.58:setupMenu
    def setupMenu (self,menu,command,all=False):
    
        '''A function that makes a function to populate a menu.'''
        
        c = self.c ; nb = self.nb
    
        menu.delete(0,Tk.END)
        current = self.nb.getcurselection()
        for i, name in enumerate(nb.pagenames()):
            i = i + 1
            if name == current and not all: continue
            menu.add_command(
                label=str(i),command=lambda c=c,name=name: command(c,name))
    #@nonl
    #@-node:ekr.20060213023839.58:setupMenu
    #@+node:ekr.20060213023839.59:importLeoFile
    def importLeoFile (self,event=None):
        
        c = self.c ; nb = self.nb
    
        name = tkFileDialog.askopenfilename()
    
        if name:
            page = self.addPage(name)
            nb.selectpage(nb.pagenames()[-1])
            c.fileCommands.open(file(name,'r'),name)
            c.cChapter.makeCurrent()
            self.renumber()
    #@nonl
    #@-node:ekr.20060213023839.59:importLeoFile
    #@+node:ekr.20060213023839.60:exportLeoFile
    def exportLeoFile (self,event=None):
    
        c = self.c
    
        name = tkFileDialog.asksaveasfilename()
    
        if name:
            if not name.endswith('.leo'): name = name + '.leo'
            c.fileCommands.write_LEO_file(name,False,singleChapter=True)
    #@nonl
    #@-node:ekr.20060213023839.60:exportLeoFile
    #@+node:ekr.20060213023839.61:doPDFConversion & helper
    # Requires reportlab toolkit at http://www.reportlab.org
    
    def doPDFConversion (self,event=None):
        c = self.c ; nb = self.nb
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.rl_config import defaultPageSize
        PAGE_HEIGHT = defaultPageSize [1]
        PAGE_WIDTH = defaultPageSize [0]
        maxlen = 100
        styles = getSampleStyleSheet()
        pinfo = c.frame.shortFileName()
        pinfo1 = pinfo.rstrip('.leo')
        cs = cStringIO.StringIO()
        doc = SimpleDocTemplate(cs,showBoundary=1)
        Story = [Spacer(1,2*inch)]
        pagenames = nb.pagenames()
        cChapter = c.cChapter
        for n, z in enumerate(pagenames):
            n = n + 1
            sv = self.getStringVar(z)
            chapter = self.chapters [sv]
            chapter.setVariables()
            p = chapter.rp
            if p:
                self._changeTreeToPDF(sv.get(),n,p,c,Story,styles,maxlen)
        #@    << define otherPages callback >>
        #@+node:ekr.20060213023839.62:<< define otherPages callback >>
        def otherPages (canvas,doc,pageinfo=pinfo):
        
            canvas.saveState()
            canvas.setFont('Times-Roman',9)
            canvas.drawString(inch,0.75*inch,"Page %d %s" % (doc.page,pageinfo))
            canvas.restoreState()
        #@nonl
        #@-node:ekr.20060213023839.62:<< define otherPages callback >>
        #@nl
        cChapter.setVariables()
            # This sets the nodes back to the cChapter.
            # If we didnt the makeCurrent would point to the wrong positions
        cChapter.makeCurrent()
        doc.build(Story,onLaterPages=otherPages)
        f = open('%s.pdf' % pinfo1,'w')
        cs.seek(0)
        f.write(cs.read())
        f.close()
        cs.close()
    #@nonl
    #@+node:ekr.20060213023839.63:_changeTreeToPDF
    def _changeTreeToPDF (self,name,num,p,Story,styles,maxlen):
        
        c = self.c ; nb = self.nb
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, XPreformatted
        from reportlab.lib.units import inch
        from reportlab.rl_config import defaultPageSize
        enc = c.importCommands.encoding
        hstyle = styles ['title']
        Story.append(Paragraph('Chapter %s: %s' % (num,name),hstyle))
        style = styles ['Normal']
        for p in p.allNodes_iter():
            head = p.moreHead(0)
            head = g.toEncodedString(head,enc,reportErrors=True)
            s = head + '\n'
            body = p2.moreBody() # Inserts escapes.
            if len(body) > 0:
                body = g.toEncodedString(body,enc,reportErrors=True)
                s = s + body
                s = s.split('\n')
                s2 = []
                for z in s:
                    if len(z) < maxlen:
                        s2.append(z)
                    else:
                        while 1:
                            s2.append(z[: maxlen])
                            if len(z[maxlen:]) > maxlen:
                                z = z [maxlen:]
                            else:
                                s2.append(z[maxlen:])
                                break
                s = '\n'.join(s2)
                s = s.replace('&','&amp;')
                s = s.replace('<','&lt;')
                s = s.replace('>','&gt;')
                s = s.replace('"','&quot;')
                s = s.replace("`",'&apos;')
                Story.append(XPreformatted(s,style))
                Story.append(Spacer(1,0.2*inch))
    
        Story.append(PageBreak())
    #@nonl
    #@-node:ekr.20060213023839.63:_changeTreeToPDF
    #@-node:ekr.20060213023839.61:doPDFConversion & helper
    #@-node:ekr.20060213023839.52:tab callbacks
    #@-node:ekr.20060213023839.50:tab menu stuff
    #@+node:ekr.20060213023839.64:Multi-Editor stuff
    #@+node:ekr.20060213023839.65:selectNodeForEditor
    def selectNodeForEditor (self,body):
    
        '''Select the next node for the editor.'''
        
        c = self.c
    
        if not hasattr(body,'lastPosition'):
            body.lastPosition = c.currentPosition()
    
        if body.lastPosition == c.currentPosition():
            return
        elif body.lastPosition.exists(c):
            g.trace('last position does not exist',color='red')
            c.selectPosition(body.lastPosition)
        else:
            c.selectPosition(c.rootPosition())
    
        body.lastPosition = c.currentPosition()
    #@nonl
    #@-node:ekr.20060213023839.65:selectNodeForEditor
    #@+node:ekr.20060213023839.66:activateEditor
    def activateEditor (self,body):
    
        '''Activate an editor.'''
        
        p = body.lastPosition ; h = p.headString()
        g.trace(h,body,hasattr(body,'r')and body.r,g.callers())
        body.r.configure(text=h)
        ip = body.lastPosition.t.insertSpot
        body.deleteAllText()
        body.insertAtEnd(p.bodyString())
        if ip: body.setInsertionPoint(ip)
        body.colorizer.colorize(p)
        body.bodyCtrl.update_idletasks()
    #@nonl
    #@-node:ekr.20060213023839.66:activateEditor
    #@+node:ekr.20060213023839.67:removeEditor
    def removeEditor (self):
        
        c = self.c
        pbody = self.pbodies [c]
        if len(pbody.panes()) == 1: return None
        body = c.frame.body
        pbody.delete(body.editorName)
        pbody.updatelayout()
        panes = pbody.panes()
        self.twidgets [c.frame].remove(body)
        nBody = self.twidgets [c.frame] [0]
        nBody.bodyCtrl.focus_set()
        nBody.bodyCtrl.update_idletasks()
    #@nonl
    #@-node:ekr.20060213023839.67:removeEditor
    #@+node:ekr.20060213023839.68:addHeading
    def addHeading (self,pane):
    
        f = Tk.Frame(pane)
        f.pack(side='top')
        l = Tk.Label(f)
        l.pack(side='left')
        r = Tk.Label(f)
        r.pack(side='right')
        return l, r
    #@nonl
    #@-node:ekr.20060213023839.68:addHeading
    #@-node:ekr.20060213023839.64:Multi-Editor stuff
    #@+node:ekr.20060213023839.69:Indexing
    #@+at
    # Indexing is complementary to find, it provides a gui Index of nodes.
    # 
    # In comparison to regular find which bounces you around the tree,
    # you can preview the node before you go to it.
    #@-at
    #@+node:ekr.20060213023839.70:viewIndex
    def viewIndex (c,nodes=None,tle=''):
        if nodes == None:
            nodes = [x for x in walkChapters(c,chapname=True)]
        def aN (a):
            n = a [0].headString()
            return n, a [0], a [1]
        nodes = map(aN,nodes)
        nodes.sort()
        tl = Tk.Toplevel()
        import time
        title = "%s Index of %s created at %s" % (tle,c.frame.shortFileName(),time.ctime())
        tl.title(title)
        f = Tk.Frame(tl)
        f.pack(side='bottom')
        l = Tk.Label(f,text='ScrollTo:')
        e = Tk.Entry(f,bg='white',fg='blue')
        l.pack(side='left')
        e.pack(side='left')
        b = Tk.Button(f,text='Close')
        b.pack(side='left')
        def rm (tl=tl):
            tl.withdraw()
            tl.destroy()
        b.configure(command=rm)
        sve = Tk.StringVar()
        e.configure(textvariable=sve)
        ms = tl.maxsize()
        tl.geometry('%sx%s+0+0' % (ms[0],(ms[1]/4)*3))
        sc = Pmw.ScrolledCanvas(tl,vscrollmode='static',hscrollmode='static',
        usehullsize = 1, borderframe = 1, hull_width = ms [0], hull_height = (ms[1]/4) * 3)
        sc.pack()
        can = sc.interior()
        can.configure(background='white')
        bal = Pmw.Balloon(can)
        tags = {}
        buildIndex(nodes,c,can,tl,bal,tags)
        sc.resizescrollregion()
        #@    << define scTo callback >>
        #@+node:ekr.20060213023839.71:<< define scTo callback >>
        def scTo (event,nodes=nodes,sve=sve,can=can,tags=tags):
        
            t = sve.get()
            if event.keysym == 'BackSpace':
                t = t [: -1]
            else:
                t = t + event.char
            if t == '': return
            for z in nodes:
                if z [0].startswith(t) and tags.has_key(z[1]):
                    tg = tags [z [1]]
                    eh = can.bbox(ltag) [1]
                    eh = (eh*1.0) / 100
                    bh = can.bbox(tg) [1]
                    ncor = (bh/eh) * .01
                    can.yview('moveto',ncor)
                    return
        #@nonl
        #@-node:ekr.20060213023839.71:<< define scTo callback >>
        #@nl
        e.bind('<Key>',scTo)
        e.focus_set()
    #@nonl
    #@-node:ekr.20060213023839.70:viewIndex
    #@+node:ekr.20060213023839.72:buildIndex
    def buildIndex (self,nodes,can,tl,bal,tags):
    
        c = self.c ; nb = self.nb
        f = tkFont.Font()
        f.configure(size=-20)
        ltag = None
        for i, z in enumerate(nodes):
            tg = 'abc' + str(i)
            parent = z [1].parent()
            if parent: parent = parent.headString()
            else:
                parent = 'No Parent'
            sv = self.getStringVar(c,z[2])
            if sv.get(): sv = ' - ' + sv.get()
            else: sv = ''
    
            tab = nb.tab(z[2])
            tv = tab.cget('text')
            isClone = z [1].isCloned()
            if isClone: clone = ' (Clone) '
            else:       clone = ''
            txt = '%s  , parent: %s , chapter: %s%s%s' % (z[0],parent,tv,sv,clone)
            ltag = tags [z [1]] = can.create_text(
                20,i*20+20,text=txt,fill='blue',font=f,anchor=Tk.W,tag=tg)
            bs = z [1].bodyString()
            if bs.strip() != '':
                bal.tagbind(can,tg,bs)
            #@        << def callbacks >>
            #@+node:ekr.20060213023839.73:<< def callbacks >>
            def goto (event,self=self,z=z,tl=tl):
                c = self.c ; nb = self.nb
                nb.selectpage(z[2])
                c.selectPosition(z[1])
                c.frame.outerFrame.update_idletasks()
                c.frame.outerFrame.event_generate('<Button-1>')
                c.frame.bringToFront()
                return 'break'
            
            def colorRd (event,tg=ltag,can=can):
                can.itemconfig(tg,fill='red')
            
            def colorBl (event,tg=ltag,can=can):
                can.itemconfig(tg,fill='blue')
            #@nonl
            #@-node:ekr.20060213023839.73:<< def callbacks >>
            #@nl
            can.tag_bind(tg,'<Button-1>',goto)
            can.tag_bind(tg,'<Enter>',colorRd,'+')
            can.tag_bind(tg,'<Leave>',colorBl,'+')
    #@nonl
    #@-node:ekr.20060213023839.72:buildIndex
    #@+node:ekr.20060213023839.74:regexViewIndex
    def regexViewIndex (self):
        
        c = self.c ; nb = self.nb
    
        def regexWalk (result,entry,widget):
            txt = entry.get()
            widget.deactivate()
            widget.destroy()
            if result == 'Cancel': return None
            nodes = [x for x in walkChapters(c,chapname=True)]
            import re
            regex = re.compile(txt)
            def search (nd,regex=regex):
                return regex.search(nd[0].bodyString())
            nodes = filter(search,nodes)
            viewIndex(c,nodes,'Regex( %s )' % txt)
            return
    
        sd = Pmw.PromptDialog(c.frame.top,
            title = 'Regex Index',
            buttons = ('Search','Cancel'),
            command = regexWalk,
        )
        entry = sd.component('entry')
        sd.configure(command=
            lambda result, entry = entry, widget = sd:
                regexWalk(result,entry,widget))
        sd.activate(geometry='centerscreenalways')
    #@nonl
    #@-node:ekr.20060213023839.74:regexViewIndex
    #@-node:ekr.20060213023839.69:Indexing
    #@+node:ekr.20060213023839.75:Chapter-Notebook ops
    #@+node:ekr.20060213023839.76:renumber
    def renumber (self):
        
        nb = self.nb ; pagenames = nb.pagenames()
        
        g.trace(pagenames)
    
        for i, z in enumerate(pagenames):
            i = i + 1
            tab = nb.tab(z)
            tab.configure(text=str(i))
    
    #@-node:ekr.20060213023839.76:renumber
    #@+node:ekr.20060213023839.77:getGoodPage & helper
    def getGoodPage (self,event,body):
        
        c = self.c ; nb = self.nb
    
        body.frame.body = body
        body.frame.bodyCtrl = body.bodyCtrl
        if not hasattr(body,'lastChapter'):
            body.lastChapter = nb.getcurselection()
        page = self.checkChapterValidity(body.lastChapter)
        if page != nb.getcurselection():
            body.lastChapter = page
            nb.selectpage(page)
        self.selectNodeForEditor(body)
        self.activateEditor(body)
    #@nonl
    #@+node:ekr.20060213023839.78:checkChapterValidity
    def checkChapterValidity (self,name):
        
        nb = self.nb
    
        try:
            nb.index(name)
            return name
        except:
            return nb.getcurselection()
    #@nonl
    #@-node:ekr.20060213023839.78:checkChapterValidity
    #@-node:ekr.20060213023839.77:getGoodPage & helper
    #@+node:ekr.20060213023839.79:getStringVar
    def getStringVar (self,name):
    
        '''return a Tk StrinVar that is a primary identifier.'''
        
        nb = self.nb
        index = nb.index(name)
        page  = nb.page(index)
        g.trace(name,page,hasattr(page,'sv') and page.sv or 'no sv')
        return page.sv
    #@nonl
    #@-node:ekr.20060213023839.79:getStringVar
    #@+node:ekr.20060213023839.2:setTree
    def setTree (self,name):
    
        c = self.c ; nb = self.nb
        pindex = nb.index(name)
        page = nb.page(pindex)
        if not hasattr(page,'sv'):
            # The page hasn't been fully created yet.
            g.trace('no sv attr for page',g.callers(),color='red')
            return None
        sv = page.sv
        chapter = chapters [sv]
        chapter.makeCurrent()
        frame = c.frame
        frame.body.lastChapter = name
        frame.body.lastPosition = chapter.cp
        frame.body.l.configure(textvariable=sv)
        tab = nb.tab(pindex)
        tab.configure(background='grey',foreground='white')
        self.activateEditor(frame.body)
    #@nonl
    #@-node:ekr.20060213023839.2:setTree
    #@+node:ekr.20060213023839.80:lowerPage
    def lowerPage (self,name):
    
        '''Set a lowered tabs color.'''
    
        nb = self.nb
        pindex = nb.index(name)
        tab = nb.tab(pindex)
        tab.configure(background='lightgrey',foreground='black')
    #@nonl
    #@-node:ekr.20060213023839.80:lowerPage
    #@+node:ekr.20060213023839.81:walkChapters
    def walkChapters (self,ignorelist=[],chapname=False):
    
        '''A generator that allows one to walk the chapters as one big tree.'''
    
        nb = self.nb ; pagenames = nb.pagenames()
    
        for z in pagenames:
            sv = self.getStringVar(z)
            chapter = chapters [sv]
            v = chapter.rp
            while v:
                if chapname:
                    if v not in ignorelist: yield v, z
                else:
                    if v not in ignorelist: yield v
                v = v.threadNext()
    #@nonl
    #@-node:ekr.20060213023839.81:walkChapters
    #@-node:ekr.20060213023839.75:Chapter-Notebook ops
    #@+node:ekr.20060213023839.82:opening and closing
    #@+at 
    #@nonl
    # We need to decorate and be tricky here, since a Chapters leo file is a 
    # zip file.
    # 
    # These functions are easy to break in my experience. :)
    #@-at
    #@nonl
    #@+node:ekr.20060213023839.83:opening
    #@+node:ekr.20060213023839.84:openChaptersFile
    def openChaptersFile (fileName):
    
        zf = zipfile.ZipFile(fileName)
        file = cStringIO.StringIO()
        name = zf.namelist()
        csfiles = [ [], []]
        for x in name:
            zi = zf.getinfo(x)
            csfiles [0].append(zi.comment)
            cs = cStringIO.StringIO()
            csfiles [1].append(cs)
            cs.write(zf.read(x))
            cs.seek(0)
        zf.close()
        csfiles = zip(csfiles[0],csfiles[1])
        return csfiles
    
    #@-node:ekr.20060213023839.84:openChaptersFile
    #@+node:ekr.20060213023839.85:insertChapters
    def insertChapters (self,chapters):
    
        c = self.c ; nb = self.nb ; pagenames = nb.pagenames()
    
        for num, tup in enumerate(chapters):
            x, y = tup
            if num > 0:
                sv = self.addPage(c,x).sv
                nb.nextpage()
                cselection = nb.getcurselection()
            else:
                cselection = nb.getcurselection()
                sv = self.getStringVar(cselection)
            sv.set(x)
            next = cselection
            self.setTree(c,next,nb)
            frame.c.fileCommands.open(y,sv.get())
            if num == 0: flipto = cselection
        self.setTree(flipto,nb,c)
        c.frame.canvas.update_idletasks()
    #@nonl
    #@-node:ekr.20060213023839.85:insertChapters
    #@-node:ekr.20060213023839.83:opening
    #@+node:ekr.20060213023839.86:closing
    #@+node:ekr.20060213023839.87:getMakeStringIO
    def getMakeStringIO (chapList):
    
        '''Insures that data is put in a StringIO instance.'''
    
        def makeStringIO (self,name,value,cList=chapList):
            if name == 'outputFile' and value != None:
                import StringIO
                cS = StringIO.StringIO()
                cS.close = lambda: None
                self.__dict__ [name] = cS
                cList.append(cS)
            elif name == 'outputFile' and value == None:
                self.__dict__ [name] = None
            else:
                self.__dict__ [name] = value
    
        return makeStringIO
    #@nonl
    #@-node:ekr.20060213023839.87:getMakeStringIO
    #@+node:ekr.20060213023839.88:zipChapters
    def zipChapters (fileName,pagenames,chapList):
    
        '''Writes StringIO instances to a zipped file.'''
    
        zf = zipfile.ZipFile(fileName,'w',zipfile.ZIP_DEFLATED)
    
        for x, fname in enumerate(pagenames):
            sv = self.getStringVar(fname)
            zif = zipfile.ZipInfo(str(x))
            zif.comment = sv.get()
            zif.compress_type = zipfile.ZIP_DEFLATED
            chapList [x].seek(0)
            zf.writestr(zif,chapList[x].read())
    
        zf.close()
    #@nonl
    #@-node:ekr.20060213023839.88:zipChapters
    #@-node:ekr.20060213023839.86:closing
    #@-node:ekr.20060213023839.82:opening and closing
    #@+node:ekr.20060213023839.89:operation( node ) to Chapter
    #@+node:ekr.20060213023839.90:cloneToChapter
    def cloneToChapter (self,name):
    
        c = self.c ; nb = self.nb
        page = nb.page(nb.index(name))
        c.beginUpdate()
        try:
            clone = vnd.clone(c.currentPosition())
            chapter = self.chapters [page.sv]
            p = chapter.cp
            clone.unlink()
            clone.linkAfter(p)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20060213023839.90:cloneToChapter
    #@+node:ekr.20060213023839.91:moveToChapter
    def moveToChapter (self,name):
        
        c = self.c ; nb = self.nb
        page = nb.page(nb.index(name))
        mvChapter = self.chapters [page.sv]
        c.beginUpdate()
        try:
            p = c.currentPosition()
            if not p.parent() and not p.back():
                c.endUpdate()
                return None
            vndm = mvChapter.cp
            p.unlink()
            p.linkAfter(vndm)
        finally:
            c.endUpdate()
        c.selectPosition(c.rootPosition())
    #@-node:ekr.20060213023839.91:moveToChapter
    #@+node:ekr.20060213023839.92:copyToChapter
    def copyToChapter (c,name):
    
        c = self.c ; nb = self.nb
        page = nb.page(nb.index(name))
        cpChapter = self.chapters [page.sv]
        c.beginUpdate()
        try:
            s = c.fileCommands.putLeoOutline()
            v = c.fileCommands.getLeoOutline(s)
            cpChapter.setVariables()
            mvnd = cpChapter.cp
            v.moveAfter(mvnd)
            c.cChapter.setVariables()
        finally:
            c.endUpdate()
    #@-node:ekr.20060213023839.92:copyToChapter
    #@+node:ekr.20060213023839.93:makeNodeIntoChapter
    def makeNodeIntoChapter (self,event=None,p=None):
        
        c = self.c
        renum = p
        if p == None: p = c.currentPosition()
        if p == c.rootPosition() and p.next() == None: return
        nxt = p.next()
        if nxt: p.doDelete(nxt)
    
        page = self.addPage(c)
        mnChapter = self.chapters [page.sv]
        c.beginUpdate()
        try:
            oChapter = c.cChapter
            mnChapter.makeCurrent()
            root = mnChapter.rp
            p.moveAfter(root)
            c.setRootPosition(p)
            oChapter.makeCurrent()
        finally:
            c.endUpdate()
        if not renum: self.renumber()
        c.selectPosition(oChapter.rp)
    #@nonl
    #@-node:ekr.20060213023839.93:makeNodeIntoChapter
    #@-node:ekr.20060213023839.89:operation( node ) to Chapter
    #@+node:ekr.20060213023839.94:Conversions
    #@+node:ekr.20060213023839.95:conversionToSimple
    def conversionToSimple (self):
        
        c = self.c ; nb = self.nb ; p = c.rootPosition()
        while 1:
            n = p.next()
            if n == None:   break
            else:           p = n
        pagenames = nb.pagenames()
        current = nb.getcurselection()
        pagenames.remove(current)
        c.beginUpdate()
        try:
            for z in pagenames:
                index = nb.index(z)
                page = nb.page(index)
                chapter = self.chapters [page.sv]
                rvNode = chapter.rp
                while 1:
                    nxt = rvNode.next()
                    rvNode.moveAfter(p)
                    if nxt: rvNode = nxt
                    else:   p = rvNode ; break
                nb.delete(z)
        finally:
            c.endUpdate()
        self.renumber(nb)
    #@nonl
    #@-node:ekr.20060213023839.95:conversionToSimple
    #@+node:ekr.20060213023839.96:conversionToChapters
    def conversionToChapters (self):
        
        c = self.c ; nb = self.nb ; p = c.rootPosition()
        
        while 1:
            nxt = p.next()
            if not nxt: break
            self.makeNodeIntoChapter(p=nxt)
    
        self.setTree(nb.pagenames()[0])
    #@nonl
    #@-node:ekr.20060213023839.96:conversionToChapters
    #@-node:ekr.20060213023839.94:Conversions
    #@+node:ekr.20060213023839.97:Misc
    #@+node:ekr.20060213023839.98:swapChapters
    def swapChapters (self,name):
    
        c = self.c ; nb = self.nb
        cselection = nb.getcurselection()
        tab1 = nb.tab(cselection)
        tab2 = nb.tab(name)
        tval1 = tab1.cget('text')
        tval2 = tab2.cget('text')
        tv1 = self.getStringVar(cselection)
        tv2 = self.getStringVar(name)
        chap1 = c.cChapter
        chap2 = self.chapters [tv2]
        rp, tp, cp = chap2.rp, chap2.tp, chap2.cp
        chap2.rp, chap2.tp, chap2.cp = chap1.rp, chap1.tp, chap1.cp
        chap1.rp, chap1.tp, chap1.cp = rp, tp, cp
        chap1.setVariables()
        c.redraw()
        chap1.canvas.update_idletasks()
        val1 = tv1.get()
        val2 = tv2.get()
        if val2.isdigit():
            tv1.set(nb.index(cselection)+1)
        else: tv1.set(val2)
        if val1.isdigit():
            tv2.set(nb.index(name)+1)
        else: tv2.set(val1)
    #@nonl
    #@-node:ekr.20060213023839.98:swapChapters
    #@+node:ekr.20060213023839.99:emptyTrash
    def emptyTrash (self):
        
        c = self.c ; nb = self.nb ; pagenames = nb.pagenames()
        pagenames = [self.getStringVar(x) for x in pagenames]
    
        for z in pagenames:
            if z.get().upper() == 'TRASH':
                trChapter = self.chapters [z]
                rvND = trChapter.rp
                c.beginUpdate()
                trChapter.setVariables()
                nRt = rvND.insertAfter()
                nRt.moveToRoot()
                trChapter.rp = c.rootPosition()
                trChapter.cp = c.currentPosition()
                trChapter.tp = c.topPosition()
                c.cChapter.setVariables()
                c.endUpdate(False)
                if c.cChapter == trChapter:
                    c.selectPosition(nRt)
                    c.redraw()
                    trChapter.canvas.update_idletasks()
                return
    #@nonl
    #@-node:ekr.20060213023839.99:emptyTrash
    #@+node:ekr.20060213023839.100:regexClone
    def regexClone (self,name):
    
        c = self.c ; nb = self.nb
        sv = self.getStringVar(c,name)
        chapter = self.chapters [sv]
        #@    << define cloneWalk callback >>
        #@+node:ekr.20060213023839.101:<< define cloneWalk callback >>
        def cloneWalk (result,entry,widget,self=self):
            c = self.c ; nb = self.nb
            txt = entry.get()
            widget.deactivate()
            widget.destroy()
            if result == 'Cancel': return None
            import re
            regex = re.compile(txt)
            rt = chapter.cp
            chapter.setVariables()
            stnode = leoNodes.tnode('',txt)
            snode = leoNodes.vnode(c,stnode)
            snode = leoNodes.position(c,snode,[])
            snode.moveAfter(rt)
            ignorelist = [snode]
            it = walkChapters(c,ignorelist=ignorelist)
            for z in it:
                f = regex.search(z.bodyString())
                if f:
                    clone = z.clone(z)
                    i = snode.numberOfChildren()
                    clone.moveToNthChildOf(snode,i)
                    ignorelist.append(clone)
            c.cChapter.setVariables()
            nb.selectpage(name)
            c.selectPosition(snode)
            snode.expand()
            c.redraw()
        #@nonl
        #@-node:ekr.20060213023839.101:<< define cloneWalk callback >>
        #@nl
        sd = Pmw.PromptDialog(c.frame.top,
            title = 'Search and Clone',
            buttons = ('Search','Cancel'),
            command = cloneWalk,
        )
        entry = sd.component('entry')
        sd.configure(command=
            lambda result, entry = entry, widget = sd:
                cloneWalk(result,entry,widget))
        sd.activate(geometry='centerscreenalways')
    #@nonl
    #@-node:ekr.20060213023839.100:regexClone
    #@-node:ekr.20060213023839.97:Misc
    #@-others
#@nonl
#@-node:ekr.20060213023839.28:class chapterController
#@-others
#@nonl
#@-node:ekr.20060213023839.3:@thin chapters2.py
#@-leo
