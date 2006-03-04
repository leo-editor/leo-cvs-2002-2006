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

#@@language python
#@@tabwidth -4

__version__ = "0.106"
#@<< version history >>
#@+node:ekr.20060213023839.5:<< version history >>
#@@nocolor

#@+at 
# v .101 EKR: 2-13-06 Created from chapters.py.
# - This will be the new working version of the chapters plugin.
# 
# v .102 EKR: A major simplification of the previously horrible init logic.
# - Only cc.createCanvas calls cc.createTab.
#   This is similar to Brian's original code.
# - cc.createCanvas sets cc ivars for initTree.
#   This eliminates the need for hard-to-get-right params.
# - Only cc.treeInit creates Chapters instances.
#   Again, this is similar to Brian's original code.
# - Chapters.init now creates all 'special' bindings and injects all ivars.
#   This puts all the weird stuff in one place.
# - cc.addPage now just calls cc.constructTree.
# 
# v .103 EKR:
# - Simplied and clarified the code for multiple editors and made it work.
# 
# v .104 EKR:
# - Zipped file logic now works and is compatible with original chapters 
# plugin.
# 
# v .105 EKR
# - Created bindings in second and other canvases.
# - Only show editor label if there is more than one editor.
#   Alas, it is difficult to get labels back once unpacked.
# - Clicking on a tab puts focus in body.
# 
# v .106 EKR:
# - Moved sv var into Chapters class.
#     - chapter.sv replaces cc.stringVars dict.
#     - replaced cc.getStringVar(name) by cc.getChapter(name).sv
# - Removed nextPageName.
# 
# v .107 EKR:
# - Made rename work as in old plugin.
#     - Removed computeNodeLabel.
#     - Use stringvar in editor label.
#@-at
#@nonl
#@-node:ekr.20060213023839.5:<< version history >>
#@nl
#@<< imports >>
#@+middle:ekr.20060213023839.8:Module level
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
import string ; string.atoi = int # Solve problems with string.atoi...
import sys
import time
import tkFileDialog
import tkFont
import zipfile
#@nonl
#@-node:ekr.20060213023839.7:<< imports >>
#@-middle:ekr.20060213023839.8:Module level
#@nl
#@<< remember the originals for decorated methods >>
#@+middle:ekr.20060213023839.8:Module level
#@+node:ekr.20060213023839.1:<< remember the originals for decorated methods >>
# Remember the originals of the 10 overridden methods...

# Define these at the module level so they are defined early in the load process.
old_createCanvas            = leoTkinterFrame.leoTkinterFrame.createCanvas
old_createControl           = leoTkinterFrame.leoTkinterBody.createControl
old_doDelete                = leoNodes.position.doDelete
# old_editLabel               = leoTkinterTree.leoTkinterTree.endEditLabel
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

# The global data.
controllers = {} # Keys are commanders, values are chapterControllers.
iscStringIO = False # Used by g.os_path_dirname
stringIOCommander = None # Used by g.os_path_dirname

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
            leoTkinterFrame.leoTkinterFrame.createCanvas    = new_createCanvas
            leoTkinterFrame.leoTkinterBody.createControl    = new_createControl
            leoNodes.position.doDelete                      = new_doDelete
            # leoTkinterTree.leoTkinterTree.endEditLabel      = new_endEditLabel
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
#@+node:ekr.20060213023839.12:new_createCanvas (tkFrame)  (chapterControllers & tabs)
def new_createCanvas (self,parentFrame,pageName='1'):
    
    # self is c.frame
    c = self.c
    if g.app.unitTesting:
        # global old_createCanvas
        return old_createCanvas(self,parentFrame)
    else:
        global controllers
        cc = controllers.get(c)
        if not cc:
            controllers [c] = cc = chapterController(c,self,parentFrame)
            # g.trace('created controller',cc)
        return cc.createCanvas(self,parentFrame,pageName)
#@nonl
#@-node:ekr.20060213023839.12:new_createCanvas (tkFrame)  (chapterControllers & tabs)
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
#@+node:ekr.20060213023839.14:new_createControl (leoTkinterBody)
def new_createControl (self,frame,parentFrame):

    # self is c.frame.body
    if g.app.unitTesting:
        # global old_createControl
        return old_createControl(self,frame,parentFrame)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.createControl(self,frame,parentFrame)
#@nonl
#@-node:ekr.20060213023839.14:new_createControl (leoTkinterBody)
#@+node:ekr.20060213023839.15:new_doDelete (position)
def new_doDelete (self):
    
    # self is position.
    if g.app.unitTesting:
        # global old_doDelete
        return old_doDelete(self)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.doDelete(self)
#@nonl
#@-node:ekr.20060213023839.15:new_doDelete (position)
#@+node:ekr.20060213023839.17:new_getLeoFile (fileCommands)
def new_getLeoFile (self,fileName,readAtFileNodesFlag=True,silent=False):
    
    # self is c.fileCommands
    if g.app.unitTesting:
        # global old_getLeoFile
        return old_getLeoFile(self,fileName,readAtFileNodesFlag,silent)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.getLeoFile(self,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:ekr.20060213023839.17:new_getLeoFile (fileCommands)
#@+node:ekr.20060213023839.18:new_open (fileCommands)
def new_open (self,file,fileName,readAtFileNodesFlag=True,silent=False):
    
    # self = fileCommands
    c = self.c
    if g.app.unitTesting:
        # global old_open
        return old_open(fc,file,fileName,readAtFileNodesFlag,silent)
    else:
        global controllers
        cc = controllers.get(c)
        if cc:
            return cc.open(self,file,fileName,readAtFileNodesFlag,silent)
        else:
            # Surprisingly, this works.
            # The file has not been opened completely.
            # This may be the settings file.
            # The controller will be created later in new_createCanvas.
            return
#@nonl
#@-node:ekr.20060213023839.18:new_open (fileCommands)
#@+node:ekr.20060213023839.19:new_select (leoTkinterTree)
def new_select (self,p,updateBeadList=True):
    
    # self is c.frame.tree
    if g.app.unitTesting:
        # global old_select
        return old_select(self,p,updateBeadList)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.select(self,p,updateBeadList)
#@nonl
#@-node:ekr.20060213023839.19:new_select (leoTkinterTree)
#@+node:ekr.20060213023839.20:new_tree_init (tkTree)
def new_tree_init (self,c,frame,canvas):
    
    # self is c.frame.tree
    if g.app.unitTesting:
        # global old_tree_init
        return old_tree_init(self,c,frame,canvas)
    else:
        global controllers
        cc = controllers.get(c)
        return cc.treeInit(self,c,frame,canvas)
#@nonl
#@-node:ekr.20060213023839.20:new_tree_init (tkTree)
#@+node:ekr.20060213023839.21:new_write_Leo_file
def new_write_Leo_file (self,fileName,outlineOnlyFlag,singleChapter=False):
    
    # self is c.frame.tree
    if g.app.unitTesting:
        # global old_write_Leo_file
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
    #@+node:ekr.20060213023839.24: ctor: Chapter
    def __init__ (self,cc,c,tree,frame,canvas,page,pageName):
        
        g.trace('Chapter',pageName,id(canvas))
    
        # Set the ivars.
        self.c = c 
        self.cc = cc
        self.canvas = canvas
        self.frame = frame
        self.pageName = pageName
        self.page = page # The Pmw.NoteBook page.
        self.tree = tree
        self.treeBar = frame.treeBar
        
        # The name of the page.
        self.sv = Tk.StringVar()
        self.sv.set(pageName)
        
        self.initTree()
        self.init()
    #@nonl
    #@-node:ekr.20060213023839.24: ctor: Chapter
    #@+node:ekr.20060304102720:__str__ and __repr__: Chapter
    def __str__ (self):
        
        return '<Chapter %s at %d>' % (self.sv.get(),id(self))
        
    __repr__ = __str__
    #@nonl
    #@-node:ekr.20060304102720:__str__ and __repr__: Chapter
    #@+node:ekr.20060302083318:init
    def init (self):
        
        '''Complete the initialization of a chapter
        by creating bindings and injecting ivars.
        
        Doing this here greatly simplifies the init logic.'''
    
        c = self.c ; cc = self.cc ; nb = cc.nb
        pageName = self.pageName ; page = self.page
        
        hull = nb.component('hull')
        tab = nb.tab(pageName)
        tab.bind('<Button-3>',lambda event,hull=hull: hull.tmenu.post(event.x_root,event.y_root))
        cc.createBalloon(page,self.sv)
     
        # The keyhandler won't be defined for the first chapter,
        # but that's ok: we only need to do this for later chapters.
        if c.k:
            # Same logic as in completeAllBindings, but for the new tree.
            c.k and self.tree.setBindings()
            for w in (self.canvas,self.tree.bindingWidget):
                c.k.completeAllBindingsForWidget(w)
    #@nonl
    #@-node:ekr.20060302083318:init
    #@+node:ekr.20060302083318.1:initTree
    def initTree (self):
        
        '''Initialize the tree for this chapter.'''
        
        cc = self.cc ; c = cc.c
        
        if cc.currentChapter:
            # We are creating a *second* or following chapter.
            t = leoNodes.tnode('','New Headline')
            v = leoNodes.vnode(c,t)
            p = leoNodes.position(c,v,[])
            self.cp = p.copy()
            self.rp = p.copy()
            self.tp = p.copy()
        else:
            cc.currentChapter = self
            self.cp = c._currentPosition or c.nullPosition()
            self.tp = c._topPosition or c.nullPosition()
            self.rp = c._rootPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20060302083318.1:initTree
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
        
        '''Switch variables in Leo's core to represent this chapter.'''
    
        c = self.c
        # g.trace(self.pageName,id(self.canvas),g.callers())
    
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
    
        # g.trace(self.pageName)
    
        c = self.c ; cc = self.cc
        cc.currentChapter._saveInfo()
        cc.currentChapter = self
        self.setVariables()
        self.updateHeadingSV(self.sv)
        c.redraw()
        c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20060213023839.27:makeCurrent
    #@+node:ekr.20060304125815:updateHeadingSV
    def updateHeadingSV (self,sv):
        
        body = self.c.frame.body
        
        if hasattr(body,'editorLeftLabel'):
            g.trace(self)
            body.editorLeftLabel.configure(textvariable=sv)
    #@nonl
    #@-node:ekr.20060304125815:updateHeadingSV
    #@-others
#@nonl
#@-node:ekr.20060213023839.23:class Chapter
#@+node:ekr.20060213023839.28:class chapterController
class chapterController:
    
    '''A per-commander controller.'''
    
    #@    @+others
    #@+node:ekr.20060303073451:Birth
    #@+node:ekr.20060213023839.30: ctor: chapterController
    def __init__ (self,c,frame,parentFrame):
        
        self.c = c
        self.frame = frame
        self.parentFrame = parentFrame
        
        # Ivars for communication between cc.createCanvas and cc.treeInit.
        # This greatly simplifies the init logic.
        self.newCanvas = None
        self.newPageName = None
        self.newPage = None
        
        # General ivars.
        self.chapters = {} # Keys are tab names, values are Chapter objects.
        self.currentChapter = None
        self.editorBodies = {} # Keys are panes, values are leoTkinterBodies.
        self.numberOfEditors = 0
        self.panedBody = None # The present Tk.PanedWidget.
    
        self.createNoteBook(parentFrame) # sets self.nb
    #@nonl
    #@-node:ekr.20060213023839.30: ctor: chapterController
    #@+node:ekr.20060213023839.29:Create widgets
    #@+node:ekr.20060213023839.32:constructTree
    def constructTree (self,frame,pageName):
        
        g.trace(pageName)
    
        cc = self ; c = self.c ; nb = self.nb
        canvas = treeBar = tree = None
        if frame.canvas:
            canvas = frame.canvas
            treeBar = frame.treeBar
            tree = frame.tree
        
        frame.canvas = canvas = frame.createCanvas(parentFrame=None,pageName=pageName)
        frame.tree = leoTkinterTree.leoTkinterTree(frame.c,frame,frame.canvas)
        frame.tree.setColorFromConfig()
    
        return tree, cc.newPage
    #@nonl
    #@-node:ekr.20060213023839.32:constructTree
    #@+node:ekr.20060213023839.33:createBalloon
    def createBalloon (self,tab,sv):
    
        '''Create a balloon for a widget.'''
        
        return
    
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
    #@+node:ekr.20060213023839.38:createEditorPane
    def createEditorPane (self):
        
        '''Create a new pane with a unique name.'''
    
        cc = self
        cc.numberOfEditors += 1
        name = str(cc.numberOfEditors)
        pane = self.panedBody.add(name)
        
        # g.trace(pane)
        return pane
    #@nonl
    #@-node:ekr.20060213023839.38:createEditorPane
    #@+node:ekr.20060213023839.34:createNoteBook
    def createNoteBook (self,parentFrame):
    
        '''Construct a NoteBook widget for a frame.'''
    
        c = self.c
        self.nb = nb = Pmw.NoteBook(parentFrame,borderwidth=1,pagemargin=0)
        hull = nb.component('hull')
        self.makeTabMenu(hull)
        
        def lowerCallback(name,self=self):
            return self.lowerPage(name)
        nb.configure(lowercommand=lowerCallback)
        
        def raiseCallback(name,self=self):
            return self.raisePage(name)
        nb.configure(raisecommand=raiseCallback)
    
        nb.pack(fill='both',expand=1)
        return nb
    #@nonl
    #@-node:ekr.20060213023839.34:createNoteBook
    #@+node:ekr.20060213023839.35:createPanedWidget
    def createPanedWidget (self,parentFrame):
    
        '''Construct a new panedwidget for a frame.'''
    
        c = self.c
        self.panedBody = panedBody = Pmw.PanedWidget(parentFrame,orient='horizontal')
        # g.trace('creating',panedBody)
        panedBody.pack(expand=1,fill='both')
    #@nonl
    #@-node:ekr.20060213023839.35:createPanedWidget
    #@+node:ekr.20060302083318.2:createTab
    def createTab (self,tabName):
        
        cc = self ; nb = cc.nb
    
        page = nb.add(tabName) # page is a Tk.Frame.
        button = nb.tab(tabName) # tab is a Tk.Button.
        button.configure(background='grey',foreground='white')
        
        # g.trace(tabName,page,button)
        return page,button
    #@nonl
    #@-node:ekr.20060302083318.2:createTab
    #@+node:ekr.20060213023839.51:makeTabMenu
    def makeTabMenu (self,widget):
        '''Creates a tab menu.'''
        c = self.c ; nb = self.nb
        tmenu = Tk.Menu(widget,tearoff=0)
        widget.bind('<Button-3>',lambda event: tmenu.post(event.x_root,event.y_root))
        widget.tmenu = tmenu
        tmenu.add_command(command=tmenu.unpost)
        tmenu.add_separator()
        tmenu.add_command(label='Add Chapter',command=self.addChapter)
        self.rmenu = rmenu = Tk.Menu(tmenu,tearoff=0)
        rmenu.configure(postcommand=self.removeChapter)
        tmenu.add_cascade(menu=rmenu,label="Remove Chapter")
        tmenu.add_command(label="Rename Chapter",command=self.renameChapter)
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
    #@-node:ekr.20060213023839.29:Create widgets
    #@+node:ekr.20060303090708:Callbacks
    #@+node:ekr.20060213023839.80:lowerPage
    def lowerPage (self,name):
    
        '''Set a lowered tabs color.'''
    
        cc = self ; c = cc.c ; tab = cc.nb.tab(name)
    
        tab.configure(background='lightgrey',foreground='black')
    #@nonl
    #@-node:ekr.20060213023839.80:lowerPage
    #@+node:ekr.20060303105217:raisePage
    def raisePage (self,name):
        
        cc = self ; c = cc.c
        
        # This must be called before queuing up the callback.
        self.setTree(name)
        
        # This can not be called immediately
        def idleCallback(event=None,c=c):
            c.invalidateFocus()
            c.bodyWantsFocusNow()
            
        w = c.frame.body and c.frame.body.bodyCtrl
        w and w.after_idle(idleCallback)
    #@nonl
    #@-node:ekr.20060303105217:raisePage
    #@+node:ekr.20060213023839.2:setTree
    def setTree (self,name):
    
        cc = self ; c = cc.c
    
        chapter = self.getChapter(name)
        sv = chapter and chapter.sv
        if not sv:
            # The page hasn't been fully created yet.
            # This is *not* an error.
            # g.trace('******* no sv attr for page',name,color='red')
            return None
    
        chapter.makeCurrent()
        
        # Set body ivars.
        body = c.frame.body
        body.lastChapter = name
        body.lastPosition = chapter.cp
        
        # Configure the tab.
        tab = cc.nb.tab(name)
        tab.configure(background='grey',foreground='white')
        self.activateEditor(c.frame.body)
    #@nonl
    #@-node:ekr.20060213023839.2:setTree
    #@-node:ekr.20060303090708:Callbacks
    #@-node:ekr.20060303073451:Birth
    #@+node:ekr.20060213023839.75:Chapter ops
    #@+node:ekr.20060213023839.31:addPage
    def addPage (self,pageName=None):
    
        cc = self ; c = cc.c
        if not pageName:
            pageName = str(len(cc.nb.pagenames()) + 1)
        
        # g.trace(pageName,cc.chapters.keys())
        
        old_chapter = cc.currentChapter
        junk, page = cc.constructTree(self.frame,pageName)
            # Creates a canvas, new tab and a new tree.
    
        old_chapter.makeCurrent()
        return page,pageName
    #@nonl
    #@-node:ekr.20060213023839.31:addPage
    #@+node:ekr.20060213023839.99:emptyTrash
    def emptyTrash (self):
        
        cc = self ; c = cc.c ; nb = cc.nb
        pagenames = [self.getChapter(x).sv for x in nb.pagenames()]
    
        for z in pagenames:
            if z.get().upper() == 'TRASH':
                trChapter = self.getChapter(z)
                rvND = trChapter.rp
                c.beginUpdate()
                trChapter.setVariables()
                nRt = rvND.insertAfter()
                nRt.moveToRoot()
                trChapter.rp = c.rootPosition()
                trChapter.cp = c.currentPosition()
                trChapter.tp = c.topPosition()
                cc.currentChapter.setVariables()
                c.endUpdate(False)
                if cc.currentChapter == trChapter:
                    c.selectPosition(nRt)
                    c.redraw()
                    trChapter.canvas.update_idletasks()
                return
    #@nonl
    #@-node:ekr.20060213023839.99:emptyTrash
    #@+node:ekr.20060213023839.100:regexClone
    def regexClone (self,name):
    
        c = self.c ; nb = self.nb
    
        chapter = self.getChapter(name)
        #@    << define cloneWalk callback >>
        #@+node:ekr.20060213023839.101:<< define cloneWalk callback >>
        def cloneWalk (result,entry,widget,self=self):
            cc = self ; c = cc.c ; nb = cc.nb
            txt = entry.get()
            widget.deactivate()
            widget.destroy()
            if result == 'Cancel': return None
            regex = re.compile(txt)
            rt = chapter.cp
            chapter.setVariables()
            stnode = leoNodes.tnode('',txt)
            snode = leoNodes.vnode(c,stnode)
            snode = leoNodes.position(c,snode,[])
            snode.moveAfter(rt)
            ignorelist = [snode]
            it = self.walkChapters(ignorelist=ignorelist)
            for z in it:
                f = regex.search(z.bodyString())
                if f:
                    clone = z.clone(z)
                    i = snode.numberOfChildren()
                    clone.moveToNthChildOf(snode,i)
                    ignorelist.append(clone)
            cc.currentChapter.setVariables()
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
    #@+node:ekr.20060213023839.76:renumber
    def renumber (self):
        
        cc = self ; nb = cc.nb
            
        i = 0
        for name in nb.pagenames():
            i += 1
            tab = nb.tab(name)
            tab.configure(text=str(i))
    #@nonl
    #@-node:ekr.20060213023839.76:renumber
    #@+node:ekr.20060213023839.98:swapChapters
    def swapChapters (self,name):
    
        cc = self ; c = cc.c ; nb = cc.nb
        cselection = nb.getcurselection()
        tab1 = nb.tab(cselection)
        tab2 = nb.tab(name)
        tval1 = tab1.cget('text')
        tval2 = tab2.cget('text')
        tv1 = cc.getChapter(cselection).sv
        tv2 = cc.getChapter(name).sv
        chap1 = cc.currentChapter
        chap2 = self.getChapter(name)
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
    #@-node:ekr.20060213023839.75:Chapter ops
    #@+node:ekr.20060303143328:Utils
    #@+node:ekr.20060228123056.1:getChapter
    def getChapter (self,pageName=None):
        
        cc = self
        
        if not pageName:
            pageName = cc.nb.getcurselection()
    
        return self.chapters.get(pageName)
    #@nonl
    #@-node:ekr.20060228123056.1:getChapter
    #@+node:ekr.20060213023839.81:walkChapters
    def walkChapters (self,ignorelist=[],chapname=False):
    
        '''A generator that allows one to walk the chapters as one big tree.'''
    
        for z in self.nb.pagenames():
            chapter = self.getChapter(z)
            for p in chapter.rp.allNodes_iter():
                if chapname:
                    if p not in ignorelist: yield p.copy(), z
                else:
                    if p not in ignorelist: yield p.copy()
    #@nonl
    #@-node:ekr.20060213023839.81:walkChapters
    #@-node:ekr.20060303143328:Utils
    #@+node:ekr.20060213023839.52:Commands
    #@+node:ekr.20060213023839.53:addChapter
    def addChapter (self,event=None):
        
        cc = self
        cc.addPage()
        cc.renumber()
    #@nonl
    #@-node:ekr.20060213023839.53:addChapter
    #@+node:ekr.20060213023839.54:removeChapter & helper
    def removeChapter (self,event=None):
    
        c = self.c ; nb = self.nb ; rmenu = self.rmenu
    
        rmenu.delete(0,'end')
        pn = nb.pagenames()
        for i, z in enumerate(pn):
            i += 1
            def removeCallback(self=self,z=z):
                self.removeOneChapter(name=z)
            rmenu.add_command(label=str(i),command=removeCallback)
    #@nonl
    #@+node:ekr.20060213023839.55:removeOneChapter
    def removeOneChapter (self,name):
        
        cc = self ; c = self.c ; nb = cc.nb
        if len(nb.pagenames()) == 1: return
        
        chapter = self.getChapter(name)
        # g.trace(name,chapter)
        p = chapter.rp
        tree = chapter.tree
        old_tree = cc.currentChapter.tree
        current = cc.currentChapter.cp
        c.beginUpdate()
        try:
            c.frame.tree = chapter.tree
            newNode = p and (p.visBack() or p.next()) # *not* p.visNext(): we are at the top level.
            if newNode:
                p.doDelete()
                c.selectPosition(newNode)
            c.frame.tree = old_tree
        finally:
            c.endUpdate()
        nb.delete(name)
    
        if tree == old_tree:
            pnames = nb.pagenames()
            nb.selectpage(pnames[0])
            c.selectPosition(c.currentPosition())
            c.redraw()
        else:
            c.selectPosition(current)
        self.renumber()
    #@nonl
    #@-node:ekr.20060213023839.55:removeOneChapter
    #@-node:ekr.20060213023839.54:removeChapter & helper
    #@+node:ekr.20060213023839.56:renameChapter
    def renameChapter (self,event=None):
        
        '''Insert a entry widget linked to chapter.sv.
        Changing this Tk.StringVar immediately changes all the chapter's labels.'''
    
        cc = self ; c = cc.c ; nb = cc.nb
        name = nb.getcurselection()
        index = nb.index(name)
        frame = nb.page(name)
        tab = nb.tab(name)
        chapter = cc.chapters.get(name)
        g.trace(chapter)
        f = Tk.Frame(frame)
        # Elegant code.  Setting e's textvariable to chapter.sv
        # immediately updates the chapter labels as e changes.
        e = Tk.Entry(f,background='white',textvariable=chapter.sv)
        b = Tk.Button(f,text="Close")
        f.pack(side='top')
        e.pack(side='left')
        b.pack(side='right')
        def changeCallback (event=None,f=f):
            f.pack_forget()
        e.bind('<Return>',changeCallback)
        e.selection_range(0,'end')
        b.configure(command=changeCallback)
        c.widgetWantsFocusNow(e)
    #@nonl
    #@-node:ekr.20060213023839.56:renameChapter
    #@+node:ekr.20060213023839.57:addTrashBarrel
    def addTrashBarrel (self,event=None):
    
        c = self.c ; nb = self.nb
        self.addPage('Trash')
        pnames = nb.pagenames()
        sv = self.getChapter(pnames[-1]).sv
        sv.set('Trash')
        self.renumber()
    #@nonl
    #@-node:ekr.20060213023839.57:addTrashBarrel
    #@+node:ekr.20060213023839.58:setupMenu
    def setupMenu (self,menu,command,all=False):
    
        '''A function that makes a function to populate a menu.'''
        
        c = self.c ; nb = self.nb
    
        menu.delete(0,'end')
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
        
        cc = self ; c = cc.c ; nb = cc.nb
    
        fileName = tkFileDialog.askopenfilename()
    
        if fileName:
            ## page,pageName = cc.addPage(pageName)
            cc.addPage()
            ###cc.nb.selectpage(nb.pagenames()[-1])
            ###cc.nb.selectpage(pageName)
            c.fileCommands.open(file(fileName,'r'),fileName)
            cc.currentChapter.makeCurrent()
            cc.renumber()
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
        cc = self ; c = cc.c ; nb = cc.nb
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
        cChapter = cc.currentChapter
        for n, z in enumerate(pagenames):
            n = n + 1
            chapter = self.getChapter(z)
            chapter.setVariables()
            p = chapter.rp
            if p:
                self._changeTreeToPDF(chapter.sv.get(),n,p,c,Story,styles,maxlen)
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
    #@-node:ekr.20060213023839.52:Commands
    #@+node:ekr.20060213023839.89:Conversions
    #@+node:ekr.20060213023839.90:cloneToChapter
    def cloneToChapter (self,name):
    
        cc = self ; c = cc.c ; nb = cc.nb
        page = nb.page(nb.index(name))
    
        c.beginUpdate()
        try:
            clone = c.currentPosition().clone()
            chapter = self.getChapter(name)
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
        mvChapter = self.getChapter(page)
        
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
    
        cc = self ; c = cc.c ; nb = cc.nb
        page = nb.page(nb.index(name))
        cpChapter = cc.getChapter(name)
    
        c.beginUpdate()
        try:
            s = c.fileCommands.putLeoOutline()
            v = c.fileCommands.getLeoOutline(s)
            cpChapter.setVariables()
            mvnd = cpChapter.cp
            v.moveAfter(mvnd)
            cc.currentChapter.setVariables()
        finally:
            c.endUpdate()
    #@-node:ekr.20060213023839.92:copyToChapter
    #@+node:ekr.20060213023839.93:makeNodeIntoChapter
    def makeNodeIntoChapter (self,event=None,p=None):
        
        cc = self ; c = cc.c
        renum = p.copy()
        if p == None: p = c.currentPosition()
        if p == c.rootPosition() and p.next() == None: return
        nxt = p.next()
        if nxt: p.doDelete(nxt)
    
        page,pageName = self.addPage()
        mnChapter = self.getChapter(pageName)
        c.beginUpdate()
        try:
            old_chapter = cc.currentChapter
            mnChapter.makeCurrent()
            root = mnChapter.rp
            p.moveAfter(root)
            c.setRootPosition(p)
            old_Chapter.makeCurrent()
        finally:
            c.endUpdate()
        if not renum: self.renumber()
        c.selectPosition(oChapter.rp)
    #@nonl
    #@-node:ekr.20060213023839.93:makeNodeIntoChapter
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
                chapter = self.getChapter(z)
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
    #@-node:ekr.20060213023839.89:Conversions
    #@+node:ekr.20060213023839.64:Editor
    #@+node:ekr.20060213023839.68:...Heading
    #@+node:ekr.20060304122235:addHeading
    def addHeading (self,parentFrame):
        '''Create a two-part editor label.
        - The left label tracks the chapter name using a chapter.sv.
        - The right label is the node's healine.'''
        
        cc = self
        f = Tk.Frame(parentFrame) ; f.pack(side='top')
        lt_label = Tk.Label(f)    ; lt_label.pack(side='left')
        rt_label = Tk.Label(f)    ; rt_label.pack(side='right')
        
        # The lt_label tracks the present chapter name.
        # chapter.updateHeadingSV changes this textvariable when chapters change.
        chapter = cc.getChapter()
        lt_label.configure(textvariable=chapter.sv)
        return lt_label, rt_label, f
    #@nonl
    #@-node:ekr.20060304122235:addHeading
    #@+node:ekr.20060304122235.1:hide/showHeading
    def showHeading (self,body):
        if 0:
            body.editorLeftLabel.pack(side='left')
            body.editorRightLabel.pack(side='right')
    
    def hideHeading (self,body):
        if 0:
            # If we unpack the frame we won't be able to repack it easily.
            # Setting the height to zero also does not seem to work.
            body.editorLabel.pack_forget()
    #@nonl
    #@-node:ekr.20060304122235.1:hide/showHeading
    #@-node:ekr.20060213023839.68:...Heading
    #@+node:ekr.20060213023839.66:activateEditor
    def activateEditor (self,body):
    
        '''Activate an editor.'''
    
        p = body.lastPosition
        h = p and p.headString() or ''
        body.editorRightLabel.configure(text=h)
        ip = body.lastPosition.t.insertSpot
        body.deleteAllText()
        body.insertAtEnd(p.bodyString())
        if ip: body.setInsertionPoint(ip)
        body.colorizer.colorize(p)
        body.bodyCtrl.update_idletasks()
    #@nonl
    #@-node:ekr.20060213023839.66:activateEditor
    #@+node:ekr.20060213023839.37:newEditor
    def newEditor (self):
    
        cc = self ; c = cc.c
        
        pane = self.createEditorPane()
        body = leoTkinterBody(self.frame,pane)
        c.frame.bodyCtrl = body.bodyCtrl # Make body the 'official' body.
        body.setFontFromConfig()
        body.createBindings()
        body.bodyCtrl.focus_set()
        body.lastPosition = c.currentPosition()
        cc.activateEditor(body)
    
        # Configure the generic editor label for this chapter and position.
        chapter = cc.getChapter()
        body.editorLeftLabel.configure(textvariable=chapter.sv)
        body.editorRightLabel.configure(text=c.currentPosition().headString())
    #@nonl
    #@-node:ekr.20060213023839.37:newEditor
    #@+node:ekr.20060213023839.67:removeEditor
    def removeEditor (self):
        
        cc = self ; c = cc.c
        panedBody = cc.panedBody
        panes = panedBody.panes()
        if not panes: return
        
        pane = panes[0]
        frame = panedBody.pane(pane)
        panedBody.delete(pane)
        panedBody.updatelayout()
        del cc.editorBodies[frame]
        
        # Hide the label if there is only one editor left.
        if len(cc.editorBodies.keys())==1:
            panes = panedBody.panes()
            frame = panedBody.pane(panes[0])
            body = cc.editorBodies.get(frame)
            cc.hideHeading(body)
        
        g.trace(pane,frame)
        g.trace(cc.editorBodies.keys())
    #@nonl
    #@-node:ekr.20060213023839.67:removeEditor
    #@-node:ekr.20060213023839.64:Editor
    #@+node:ekr.20060213023839.82:Files
    #@+at 
    #@nonl
    # We need to decorate and be tricky here, since a Chapters leo file is a 
    # zip file.
    # 
    # These functions are easy to break in my experience. :)
    #@-at
    #@nonl
    #@+node:ekr.20060213023839.83:Reading
    #@+node:ekr.20060213023839.84:openChaptersFile
    def openChaptersFile (self,fileName):
    
        zf = zipfile.ZipFile(fileName)
        file = cStringIO.StringIO()
        name = zf.namelist()
        csfiles = [[], []]
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
    
        cc = self ; c = cc.c ; nb = cc.nb ; pagenames = nb.pagenames()
        flipto = None
        for num, tup in enumerate(chapters):
            x, y = tup
            if num > 0:
                page,pageName = self.addPage(x)
                sv = cc.getChapter(pageName).sv
                nb.nextpage()
                cselection = nb.getcurselection()
            else:
                cselection = nb.getcurselection()
                sv = cc.getChapter(cselection).sv
            sv.set(x)
            next = cselection
            self.setTree(next)
            c.fileCommands.open(y,sv.get())
            if num == 0: flipto = cselection
        flipto and self.setTree(flipto)
    #@-node:ekr.20060213023839.85:insertChapters
    #@-node:ekr.20060213023839.83:Reading
    #@+node:ekr.20060213023839.86:Writing
    #@+node:ekr.20060213023839.49:writeChapters
    def writeChapters (self,fc,fileName,pagenames,outlineOnlyFlag):
    
        '''Writes Chapters to StringIO instances.'''
        
        cc = self ; chapterList = []
        global old_write_Leo_file
    
        for z in pagenames:
            chapter = self.getChapter(z)
            chapter.setVariables()
            rv = old_write_Leo_file(fc,fileName,outlineOnlyFlag,toString=True)
            chapterList.append(g.app.write_Leo_file_string)
            # g.trace(len(g.app.write_Leo_file_string))
    
        cc.currentChapter.setVariables()
        return rv,chapterList
    #@nonl
    #@-node:ekr.20060213023839.49:writeChapters
    #@+node:ekr.20060213023839.88:zipChapters
    def zipChapters (self,fileName,pagenames,chapList):
    
        '''Writes StringIO instances to a zipped file.'''
        
        cc = self
    
        zf = zipfile.ZipFile(fileName,'w',zipfile.ZIP_DEFLATED)
    
        for x, fname in enumerate(pagenames):
            sv = cc.getChapter(fname).sv
            zif = zipfile.ZipInfo(str(x))
            zif.comment = sv.get() or ''
            zif.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zif,chapList[x])
    
        zf.close()
    #@nonl
    #@-node:ekr.20060213023839.88:zipChapters
    #@-node:ekr.20060213023839.86:Writing
    #@-node:ekr.20060213023839.82:Files
    #@+node:ekr.20060213023839.69:Indexing
    #@+at
    # Indexing is complementary to find, it provides a gui Index of nodes.
    # 
    # In comparison to regular find which bounces you around the tree,
    # you can preview the node before you go to it.
    #@-at
    #@+node:ekr.20060213023839.70:viewIndex
    def viewIndex (self,nodes=None,tle=''):
        c = self.c
        if nodes == None:
            nodes = [x for x in self.walkChapters(chapname=True)]
        nodes = [(a[0].headString(),a[0],a[1]) for a in nodes]
        nodes.sort()
        if 1:
            tl = Tk.Toplevel()
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
            sc = Pmw.ScrolledCanvas(
                tl,vscrollmode='static',hscrollmode='static',
                usehullsize = 1, borderframe = 1, hull_width = ms [0],
                hull_height = (ms[1]/4) * 3)
            sc.pack()
            can = sc.interior()
            can.configure(background='white')
            bal = Pmw.Balloon(can)
            tags = {}
            self.buildIndex(nodes,can,tl,bal,tags)
            sc.resizescrollregion()
            #@        << define scTo callback >>
            #@+node:ekr.20060213023839.71:<< define scTo callback >>
            def scTo (event,nodes=nodes,sve=sve,can=can,tags=tags):
                
                return ## Not ready yet.
            
                t = sve.get()
                if event.keysym == 'BackSpace':
                    t = t [: -1]
                else:
                    t = t + event.char
                if t:
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
    #@-node:ekr.20060213023839.70:viewIndex
    #@+node:ekr.20060213023839.72:buildIndex
    def buildIndex (self,nodes,can,tl,bal,tags):
    
        cc = self ; c = cc.c ; nb = cc.nb
        f = tkFont.Font()
        f.configure(size=-20)
        ltag = None
        for i, z in enumerate(nodes):
            tg = 'abc' + str(i)
            parent = z [1].parent()
            if parent: parent = parent.headString()
            else: parent = 'No Parent'
            sv = cc.getChapter(z[2]).sv
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
            nodes = [x for x in self.walkChapters(chapname=True)]
            import re
            regex = re.compile(txt)
            def search (nd,regex=regex):
                return regex.search(nd[0].bodyString())
            nodes = filter(search,nodes)
            self.viewIndex(nodes,'Regex( %s )' % txt)
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
    #@+node:ekr.20060302173735:Overrides
    #@+node:ekr.20060213023839.40:createCanvas
    def createCanvas (self,frame,parentFrame,pageName):
        
        cc = self
                
        # Set ivars for cc.treeInit.
        page,button = cc.createTab(pageName)
        cc.newPageName = pageName
        cc.newPage = page
    
        # Create the canvas with page as the parentFrame.
        cc.newCanvas = canvas = old_createCanvas(frame,page) 
    
        g.trace(pageName,id(canvas))
    
        return canvas
    #@nonl
    #@-node:ekr.20060213023839.40:createCanvas
    #@+node:ekr.20060213023839.41:createControl (tkBody)
    def createControl(self,body,frame,parentFrame):
        
        '''Override for tkBody.createControl.
        
        This called for the 'main' body and once for each added editor. '''
    
        cc = self ; c = cc.c ; nb = cc.nb
        # assert(body == frame.body)
        
        if self.panedBody:
            pane = parentFrame
        else:
            self.createPanedWidget(parentFrame)
            pane = self.createEditorPane()
        panedBody = self.panedBody
        
        # **Important**: addHeading creates a heading that works for *all* chapters.
        lt_label,rt_label,label_frame = cc.addHeading(pane)
    
        # Inject editor ivars into the leoTkinterBody.
        body.editorRightLabel = rt_label
        body.editorLeftLabel =  lt_label
        body.editorLabelFrame = label_frame
    
        ctrl = old_createControl(body,frame,pane)
        
        if 0: # Create a focus-in event to keep the generic label widget in synch.
            def focusInCallback(event,self=self,frame=frame):
                return self.getGoodPage(event,frame.body)
            ctrl.bind("<FocusIn>",focusInCallback,'+')
        
        i = 1.0 / len(panedBody.panes())
        for z in panedBody.panes():
            panedBody.configurepane(z,size=i)
        panedBody.updatelayout()
        
        cc.editorBodies [pane] = body
    
        if len(panedBody.panes()) > 1:
            # Show the labels of all frames.
            for pane in cc.editorBodies.keys():
                body = cc.editorBodies.get(pane)
                cc.showHeading(body)
    
        return ctrl
    #@nonl
    #@-node:ekr.20060213023839.41:createControl (tkBody)
    #@+node:ekr.20060213023839.42:doDelete
    def doDelete (self,p):
        
        cc = self ; c = cc.c ; nb = cc.nb
        
        newNode = p and (p.visBack() or p.next())
            # *not* p.visNext(): we are at the top level.
        
        if not newNode: return
        
        # pagenames = [self.setStringVar(x).get().upper() for x in pagenames]
        # nbnam = nb.getcurselection()
        # if nbnam != None:
            # name = self.getStringVar(nb.getcurselection()).get().upper()
        # else: name = 'TRASH'
        # tsh = 'TRASH'
        
        name = nb.getcurselection()
        
        trash = 'Trash'
        # if name != tsh and tsh in pagenames:
        if name != trash and trash in nb.pagenames():
            index = pagenames.index(tsh)
            ### trchapter = self.chapters [self.getStringVar(index)]
            trchapter = self.getChapter(trash)
            trashnode = trchapter.rp
            trchapter.setVariables()
            p.moveAfter(trashnode)
            cc.currentChapter.setVariables()
            c.selectPosition(newNode)
            return p
        else:
            return old_doDelete(p)
    #@nonl
    #@-node:ekr.20060213023839.42:doDelete
    #@+node:ekr.20060213023839.43:endEditLabel (to be removed)
    def endEditLabel (self,tree):
        
        c = self.c ; p = c.currentPosition() ; h = p.headString()
        
        if 0:
    
            if p and h and hasattr(c.frame.body,'editorLabel'):
                c.frame.body.editorLabel.configure(text=h)
    
        return old_editLabel(tree)
    #@nonl
    #@-node:ekr.20060213023839.43:endEditLabel (to be removed)
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
    
        cc = self ; c = p.v.c ; h = p.headString() ; nb = cc.nb
        
        # g.trace(p.headString(),tree)
    
        c.frame.body.lastPosition = p
        return_val = old_select(tree,p,updateBeadList)
        c.frame.body.lastChapter = n = nb.getcurselection()
    
        if hasattr(p.c.frame.body,'editorRightLabel'):
            # n = cc.nb.getcurselection()
            # chapter = cc.chapters.get(n)
            # s = cc.computeNodeLabel(chapter,p)
            h = p.headString() or ''
            c.frame.body.editorRightLabel.configure(text=h)
    
        return return_val
    #@nonl
    #@-node:ekr.20060213023839.45:select
    #@+node:ekr.20060213023839.46:open
    def open (self,fc,file,fileName,readAtFileNodesFlag=True,silent=False):
    
        cc = self ; c = cc.c
    
        if zipfile.is_zipfile(fileName):
            # Set globals for g.os_path_dirname
            global iscStringIO, stringIOCommander
            iscStringIO = True ; stringIOCommander = c
            chapters = cc.openChaptersFile(fileName)
            g.es(str(len(chapters))+" Chapters To Read",color='blue')
            cc.insertChapters(chapters)
            g.es("Finished Reading Chapters",color='blue')
            iscStringIO = False
            return True
        else:
            return old_open(fc,file,fileName,readAtFileNodesFlag,silent)
    #@nonl
    #@-node:ekr.20060213023839.46:open
    #@+node:ekr.20060213023839.47:treeInit (creates Chapter)
    def treeInit (self,tree,c,frame,canvas):
        
        cc = self
        
        assert canvas == cc.newCanvas
        
        # These ivars are set in cc.createCanvas.
        pageName = cc.newPageName
        page = cc.newPage
        canvas = cc.newCanvas
        
        old_tree_init(tree,c,frame,canvas)
        cc.chapters [pageName] = Chapter(cc,c,tree,frame,canvas,page,pageName)
        
        # g.trace(pageName,id(canvas),cc.chapters.keys())
    #@-node:ekr.20060213023839.47:treeInit (creates Chapter)
    #@+node:ekr.20060213023839.48:write_Leo_file
    def write_Leo_file (self,fc,fileName,outlineOnlyFlag,singleChapter=False):
    
        cc = self ; c = cc.c ; nb = cc.nb ; pagenames = nb.pagenames()
    
        if len(pagenames) > 1 and not singleChapter:
            rv,chapterList = cc.writeChapters(fc,fileName,pagenames,outlineOnlyFlag)
            if rv: cc.zipChapters(fileName,pagenames,chapterList)
            return rv
        else:
            global old_write_Leo_file
            return old_write_Leo_file(fc,fileName,outlineOnlyFlag)
    #@nonl
    #@-node:ekr.20060213023839.48:write_Leo_file
    #@-node:ekr.20060302173735:Overrides
    #@-others
#@nonl
#@-node:ekr.20060213023839.28:class chapterController
#@-others
#@nonl
#@-node:ekr.20060213023839.3:@thin chapters2.py
#@-leo
