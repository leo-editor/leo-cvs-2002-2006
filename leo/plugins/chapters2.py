#@+leo-ver=4-thin
#@+node:ekr.20060306151759.1:@thin chapters2.py
#@<<docstring>>
#@+node:ekr.20060306151759.2:<<docstring>>
'''This plugin creates separate outlines called chapters within a single .leo file.

Requires Leo 4.2 or above.

Numbered tabs at the top of the body pane represent each chapter. Right clicking
the tab will show a popup menu containing commands to:
    
- insert and delete chapters.
- move nodes between chapters.
- split the body pane into multiple editors.
- create a trash barrel that hold all deleted nodes.
- import and export outlines and chapters.
- create a pdf file from your chapters (requires reportlab toolkit at http://www.reportlab.org).
- and more...
 
Warning: Outlines containing multiple chapters are stored as a zipped file that
can only be read when this plugin has been enabled.
'''
#@nonl
#@-node:ekr.20060306151759.2:<<docstring>>
#@nl

# To do: Test doPDFConversion.

#@@language python
#@@tabwidth -4

__version__ = "0.203"
#@<< version history >>
#@+node:ekr.20060306151759.3:<< version history >>
#@@nocolor

#@<< Before version .200 >>
#@+node:ekr.20060306151759.4:<< Before version .200 >>
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
# - Call nb.selectpage in Chapter.makeCurrent so the proper pane is selected 
# on startup.
# - Eliminated extra redraws on startup.
# 
# v .108 EKR:
# - Complete indexing so scrolling works.
#   This appears to have been a bug in the original chapters plugin.
# 
# v .109 EKR:
# - Replaced Remove Chapter submenu by Remove This Chapter menu item.
# - Created separate Trash submenu.
# - Trash now works.
# - Convert operations now work.
# - Added support for @color selected_chapter_tab_color setting.
# - Improved how chapter tabs get colored.
# 
# v .110 EKR:
# - All Node and Chapter ops appear to work.
# - Clone Find All works, and applies to the present chapter.
# - The 'Search' button is now the deafult button in the Clone Find All 
# dialog.
# - All ops that change the outline call c.setChanged(True)
# - Support foreground/background/selected/unselected tab colors.
# - Pychecker reports no problems.
# 
# v .111 EKR:
# - Made all editors functional by connecting FocusIn callback in 
# tkBody.createControl.
#   Editors now act as in original plugin, and in an intuitive manner.
# 
# v .112 EKR:
# - Removed call to activateEditor in onFocusIn so successful Find sets focus 
# properly.
# - Call body.setColorFromConfig and k.completeAllBindingsForWidget in 
# newEditor.
# - ** No known bugs remain!
#@-at
#@nonl
#@-node:ekr.20060306151759.4:<< Before version .200 >>
#@nl

#@+at
# v .200 EKR:
# - Removed all enumerates for compatibility with Python 2.2.
# - Made balloons work.
# v .201 EKR:
# - Supported @color editor_label_foreground/background_color
# - Call chapter._saveInfo in select. This solves a problem with changed 
# selections after a save.
# v .202 EKR:
# - Improved doc string.
# - Moved the code back into leoPlugins.leo.
# v .203 EKR:
# - Chapter.makeCurrent now calls self.rp.v.linkAsRoot to properly anchor the 
# root node.
#   This was the cause of the move-outline-right problems.
#@-at
#@nonl
#@-node:ekr.20060306151759.3:<< version history >>
#@nl
#@<< imports >>
#@+middle:ekr.20060306151759.5:Module level
#@+node:ekr.20060306151759.6:<< imports >>
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
import re
import string ; string.atoi = int # Solve problems with string.atoi...
import sys
import time
import tkFileDialog
import tkFont
import zipfile
#@nonl
#@-node:ekr.20060306151759.6:<< imports >>
#@-middle:ekr.20060306151759.5:Module level
#@nl
#@<< remember the originals for decorated methods >>
#@+middle:ekr.20060306151759.5:Module level
#@+node:ekr.20060306151759.7:<< remember the originals for decorated methods >>
# Remember the originals of the 10 overridden methods...

# Define these at the module level so they are defined early in the load process.
old_createCanvas            = leoTkinterFrame.leoTkinterFrame.createCanvas
old_createControl           = leoTkinterFrame.leoTkinterBody.createControl
old_doDelete                = leoNodes.position.doDelete
old_getLeoFile              = leoFileCommands.fileCommands.getLeoFile
old_open                    = leoFileCommands.fileCommands.open
old_os_path_dirname         = g.os_path_dirname
old_select                  = leoTkinterTree.leoTkinterTree.select
old_tree_init               = leoTkinterTree.leoTkinterTree.__init__
old_write_Leo_file          = leoFileCommands.fileCommands.write_Leo_file
#@nonl
#@-node:ekr.20060306151759.7:<< remember the originals for decorated methods >>
#@-middle:ekr.20060306151759.5:Module level
#@nl

# The global data.
controllers = {} # Keys are commanders, values are chapterControllers.
iscStringIO = False # Used by g.os_path_dirname
stringIOCommander = None # Used by g.os_path_dirname

#@+others
#@+node:ekr.20060306151759.5:Module level
#@+node:ekr.20060306151759.8:init
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
            #@+node:ekr.20060306151759.9:<< override various methods >>
            leoTkinterFrame.leoTkinterFrame.createCanvas    = new_createCanvas
            leoTkinterFrame.leoTkinterBody.createControl    = new_createControl
            leoNodes.position.doDelete                      = new_doDelete
            leoFileCommands.fileCommands.getLeoFile         = new_getLeoFile
            leoFileCommands.fileCommands.open               = new_open
            leoTkinterTree.leoTkinterTree.select            = new_select
            leoTkinterTree.leoTkinterTree.__init__          = new_tree_init
            g.os_path_dirname                               = new_os_path_dirname
            leoFileCommands.fileCommands.write_Leo_file     = new_write_Leo_file
            #@nonl
            #@-node:ekr.20060306151759.9:<< override various methods >>
            #@nl
            g.plugin_signon( __name__ )
            
    return ok
#@nonl
#@-node:ekr.20060306151759.8:init
#@+node:ekr.20060306151759.10:decorated Leo functions
#@+node:ekr.20060306151759.11:new_createCanvas (tkFrame)  (chapterControllers & tabs)
def new_createCanvas (self,parentFrame,pageName='1'):
    
    # self is c.frame
    c = self.c

    if 0: # g.app.unitTesting:
        global old_createCanvas
        return old_createCanvas(self,parentFrame)
    else:
        global controllers
        cc = controllers.get(c)
        if not cc:
            controllers [c] = cc = chapterController(c,self,parentFrame)
            # g.trace('created controller',cc)
        return cc.createCanvas(self,parentFrame,pageName)
#@nonl
#@-node:ekr.20060306151759.11:new_createCanvas (tkFrame)  (chapterControllers & tabs)
#@+node:ekr.20060306151759.12:new_os_path_dirname (leoGlobals) (ok)
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
#@-node:ekr.20060306151759.12:new_os_path_dirname (leoGlobals) (ok)
#@+node:ekr.20060306151759.13:new_createControl (leoTkinterBody)
def new_createControl (self,frame,parentFrame):

    # self is c.frame.body

    if 0: # g.app.unitTesting:
        global old_createControl
        return old_createControl(self,frame,parentFrame)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.createControl(self,frame,parentFrame)
#@nonl
#@-node:ekr.20060306151759.13:new_createControl (leoTkinterBody)
#@+node:ekr.20060306151759.14:new_doDelete (position)
def new_doDelete (self):
    
    # self is position.

    if 0: # g.app.unitTesting:
        global old_doDelete
        return old_doDelete(self)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.doDelete(self)
#@nonl
#@-node:ekr.20060306151759.14:new_doDelete (position)
#@+node:ekr.20060306151759.15:new_getLeoFile (fileCommands)
def new_getLeoFile (self,fileName,readAtFileNodesFlag=True,silent=False):
    
    # self is c.fileCommands

    if 0: # g.app.unitTesting:
        global old_getLeoFile
        return old_getLeoFile(self,fileName,readAtFileNodesFlag,silent)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.getLeoFile(self,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:ekr.20060306151759.15:new_getLeoFile (fileCommands)
#@+node:ekr.20060306151759.16:new_open (fileCommands)
def new_open (self,file,fileName,readAtFileNodesFlag=True,silent=False):
    
    # self = fileCommands
    fc = self ; c = fc.c

    if 0: # g.app.unitTesting:
        global old_open
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
            # g.trace('controller not created',g.callers())
            return
#@nonl
#@-node:ekr.20060306151759.16:new_open (fileCommands)
#@+node:ekr.20060306151759.17:new_select (leoTkinterTree)
def new_select (self,p,updateBeadList=True):
    
    # self is c.frame.tree

    if 0: # g.app.unitTesting:
        global old_select
        return old_select(self,p,updateBeadList)
    else:
        global controllers
        cc = controllers.get(self.c)
        return cc.select(self,p,updateBeadList)
#@nonl
#@-node:ekr.20060306151759.17:new_select (leoTkinterTree)
#@+node:ekr.20060306151759.18:new_tree_init (tkTree)
def new_tree_init (self,c,frame,canvas):
    
    # self is c.frame.tree

    if 0: # g.app.unitTesting:
        global old_tree_init
        return old_tree_init(self,c,frame,canvas)
    else:
        global controllers
        cc = controllers.get(c)
        return cc.treeInit(self,c,frame,canvas)
#@nonl
#@-node:ekr.20060306151759.18:new_tree_init (tkTree)
#@+node:ekr.20060306151759.19:new_write_Leo_file
def new_write_Leo_file (self,fileName,outlineOnlyFlag,singleChapter=False):
    
    # self is c.frame.tree

    if 0: # g.app.unitTesting:
        global old_write_Leo_file
        return old_write_Leo_file(self,fileName,outlineOnlyFlag)
    else:
        cc = controllers.get(self.c)
        return cc.write_Leo_file(self,fileName,outlineOnlyFlag,singleChapter=singleChapter)
#@nonl
#@-node:ekr.20060306151759.19:new_write_Leo_file
#@-node:ekr.20060306151759.10:decorated Leo functions
#@-node:ekr.20060306151759.5:Module level
#@+node:ekr.20060306151759.20:class Chapter
class Chapter:
    '''The fundamental abstraction in the Chapters plugin.
       It enables the tracking of Chapters tree information.'''
       
    #@    @+others
    #@+node:ekr.20060306151759.21: ctor: Chapter
    def __init__ (self,cc,c,tree,frame,canvas,page,pageName):
        
        # g.trace('Chapter',pageName,id(canvas))
    
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
    #@-node:ekr.20060306151759.21: ctor: Chapter
    #@+node:ekr.20060306151759.22:__str__ and __repr__: Chapter
    def __str__ (self):
        
        return '<Chapter %s at %d>' % (self.sv.get(),id(self))
        
    __repr__ = __str__
    #@nonl
    #@-node:ekr.20060306151759.22:__str__ and __repr__: Chapter
    #@+node:ekr.20060306151759.23:init
    def init (self):
        
        '''Complete the initialization of a chapter
        by creating bindings and injecting ivars.
        
        Doing this here greatly simplifies the init logic.'''
    
        c = self.c ; cc = self.cc ; nb = cc.nb
        pageName = self.pageName ; page = self.page
        
        hull = nb.component('hull')
        tab = nb.tab(pageName)
        tab.bind('<Button-3>',lambda event,hull=hull: hull.tmenu.post(event.x_root,event.y_root))
        cc.createBalloon(tab,self.sv)
     
        # The keyhandler won't be defined for the first chapter,
        # but that's ok: we only need to do this for later chapters.
        if c.k:
            # Same logic as in k.completeAllBindings, but for the new tree.
            c.k and self.tree.setBindings()
            for w in (self.canvas,self.tree.bindingWidget):
                c.k.completeAllBindingsForWidget(w)
    #@nonl
    #@-node:ekr.20060306151759.23:init
    #@+node:ekr.20060306151759.24:initTree
    def initTree (self):
        
        '''Initialize the tree for this chapter.'''
        
        cc = self.cc ; c = cc.c
        
        if cc.currentChapter:
            g.trace()
            # We are creating a *second* or following chapter.
            t = leoNodes.tnode('','New Headline')
            v = leoNodes.vnode(c,t)
            # v.linkAsRoot(oldRoot=None)
            p = leoNodes.position(c,v,[])
            self.cp = p.copy()
            self.rp = p.copy()
            self.tp = p.copy()
        else:
            cc.currentChapter = self
            self.cp = c._currentPosition and c._currentPosition.copy() or c.nullPosition()
            self.tp = c._topPosition and c._topPosition.copy() or c.nullPosition()
            self.rp = c._rootPosition and c._rootPosition.copy() or c.nullPosition()
    #@nonl
    #@-node:ekr.20060306151759.24:initTree
    #@+node:ekr.20060306151759.25:_saveInfo
    def _saveInfo (self):
    
        c = self.c
        self.cp = c._currentPosition and c._currentPosition.copy() or c.nullPosition()
        self.rp = c._rootPosition and c._rootPosition.copy() or c.nullPosition()
        self.tp = c._topPosition and c._topPosition.copy() or c.nullPosition()
        
        # g.trace(self.cp)
    #@nonl
    #@-node:ekr.20060306151759.25:_saveInfo
    #@+node:ekr.20060306151759.26:setVariables
    def setVariables (self):
        
        '''Switch variables in Leo's core to represent this chapter.'''
    
        c = self.c
    
        # g.trace(self.pageName,'canvas:',id(self.canvas),self.cp.headString())
    
        frame = self.frame
        frame.tree = self.tree
        frame.canvas = self.canvas
        frame.treeBar = self.treeBar
    
        c._currentPosition = self.cp and self.cp.copy() or c.nullPosition()
        c._rootPosition    = self.rp and self.rp.copy() or c.nullPosition()
        c._topPosition     = self.tp and self.tp.copy() or c.nullPosition()
        
        # g.trace(self.cp)
    #@nonl
    #@-node:ekr.20060306151759.26:setVariables
    #@+node:ekr.20060306151759.27:makeCurrent
    def makeCurrent (self):
    
        c = self.c ; cc = self.cc
        
        # g.trace(self.pageName)
        cc.nb.selectpage(self.pageName)
        cc.currentChapter._saveInfo()
        cc.currentChapter = self
        self.setVariables()
        self.updateHeadingSV(self.sv)
        self.rp.v.linkAsRoot(oldRoot=self.rp.v._next)
        c.redraw()
        c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20060306151759.27:makeCurrent
    #@+node:ekr.20060306151759.28:updateHeadingSV
    def updateHeadingSV (self,sv):
        
        body = self.c.frame.body
        
        if hasattr(body,'editorLeftLabel'):
            # g.trace(self)
            body.editorLeftLabel.configure(textvariable=sv)
    #@nonl
    #@-node:ekr.20060306151759.28:updateHeadingSV
    #@-others
#@nonl
#@-node:ekr.20060306151759.20:class Chapter
#@+node:ekr.20060306151759.29:class chapterController
class chapterController:
    
    '''A per-commander controller.'''
    
    #@    @+others
    #@+node:ekr.20060306151759.30:Birth
    #@+node:ekr.20060306151759.31: ctor: chapterController
    def __init__ (self,c,frame,parentFrame):
        
        self.c = c
        self.frame = frame
        self.parentFrame = parentFrame
        
        self.editorLabelBackgroundColor = c.config.getColor(
            'editor_label_background_color') or 'lightgrey'
        self.editorLabelForegroundColor = c.config.getColor(
            'editor_label_foreground_color') or 'black'
        self.selectedTabBackgroundColor = c.config.getColor(
            'selected_chapter_tab_background_color') or 'LightSteelBlue2'
        self.selectedTabForegroundColor = c.config.getColor(
            'selected_chapter_tab_foreground_color') or 'black'
        self.unselectedTabBackgroundColor = c.config.getColor(
            'unselected_chapter_tab_background_color') or 'lightgrey'
        self.unselectedTabForegroundColor = c.config.getColor(
            'unselected_chapter_tab_foreground_color') or 'black'
        
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
    #@-node:ekr.20060306151759.31: ctor: chapterController
    #@+node:ekr.20060306151759.32:Create widgets
    #@+node:ekr.20060306151759.33:constructTree
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
    #@-node:ekr.20060306151759.33:constructTree
    #@+node:ekr.20060306151759.34:createBalloon
    def createBalloon (self,tab,sv):
    
        '''Create a balloon showing the present chapter name for a tab.'''
        
        # g.trace(tab,sv.get())
    
        balloon = Pmw.Balloon(tab,initwait=100)
        balloon.bind(tab,'')
        hull = balloon.component('hull')
        def blockExpose (event):
            if sv.get() == '':
                 hull.withdraw()
        hull.bind('<Expose>',blockExpose,'+')
        balloon._label.configure(textvariable=sv)
    #@nonl
    #@-node:ekr.20060306151759.34:createBalloon
    #@+node:ekr.20060306151759.35:createEditorPane
    def createEditorPane (self):
        
        '''Create a new pane with a unique name.'''
    
        cc = self
        cc.numberOfEditors += 1
        name = str(cc.numberOfEditors)
        pane = self.panedBody.add(name)
        
        # g.trace(pane)
        return pane
    #@nonl
    #@-node:ekr.20060306151759.35:createEditorPane
    #@+node:ekr.20060306151759.36:createNoteBook
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
    #@-node:ekr.20060306151759.36:createNoteBook
    #@+node:ekr.20060306151759.37:createPanedWidget
    def createPanedWidget (self,parentFrame):
    
        '''Construct a new panedwidget for a frame.'''
    
        c = self.c
        self.panedBody = panedBody = Pmw.PanedWidget(parentFrame,orient='horizontal')
        # g.trace('creating',panedBody)
        panedBody.pack(expand=1,fill='both')
    #@nonl
    #@-node:ekr.20060306151759.37:createPanedWidget
    #@+node:ekr.20060306151759.38:createTab
    def createTab (self,tabName):
        
        cc = self ; nb = cc.nb
    
        page = nb.add(tabName) # page is a Tk.Frame.
        button = nb.tab(tabName) # tab is a Tk.Button.
    
        button.configure(
            background=cc.selectedTabBackgroundColor,
            foreground=cc.selectedTabForegroundColor)
        
        # g.trace(tabName,page,button)
        return page,button
    #@nonl
    #@-node:ekr.20060306151759.38:createTab
    #@-node:ekr.20060306151759.32:Create widgets
    #@+node:ekr.20060306151759.39:makeTabMenu & helpers
    def makeTabMenu (self,widget):
        
        '''Create a tab menu.'''
    
        cc = self
        tmenu = Tk.Menu(widget,tearoff=0)
        widget.bind('<Button-3>',lambda event: tmenu.post(event.x_root,event.y_root))
        widget.tmenu = tmenu
        
        # Huh?
        # tmenu.add_command(command=tmenu.unpost)
    
        cc.createTopLevelMenuItems(tmenu)
        tmenu.add_separator()
    
        cc.createConvertMenu(tmenu)
        cc.createEditorMenu(tmenu)
        cc.createImportExportMenu(tmenu)
        cc.createIndexMenu(tmenu)
        cc.createNodeMenu(tmenu)
        cc.createTrashMenu(tmenu)
    #@nonl
    #@+node:ekr.20060306151759.40:createTopLevelMenuItems
    def createTopLevelMenuItems (self,tmenu):
        
        cc = self
        tmenu.add_command(label='Add Chapter',command=cc.addChapter)
        
        if 1: # 'Remove This Chapter'
            def removeChapterCallback(event=None,cc=cc):
                return cc.removeChapter(cc.nb.getcurselection())
            tmenu.add_command(label='Remove This Chapter',command=removeChapterCallback)
        else: # Create submenu of all chapters.
            cc.rmenu = rmenu = Tk.Menu(tmenu,tearoff=0)
            rmenu.configure(postcommand=cc.createRemoveChapterMenu)
            tmenu.add_cascade(menu=rmenu,label="Remove This Chapter")
    
        tmenu.add_command(
            label="Rename This Chapter",
            command=cc.renameChapter)
            
        swapmenu = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(menu=swapmenu,label='Swap With Chapter')
            
        def swapChaptersCallback  (cc=cc,menu=swapmenu):
            cc.setupMenu(menu,cc.swapChapters)
        swapmenu.configure(postcommand=swapChaptersCallback)
        
        tmenu.add_command(
            label="Clone Find All",
            command=cc.regexClone)
    #@nonl
    #@-node:ekr.20060306151759.40:createTopLevelMenuItems
    #@+node:ekr.20060306151759.41:createConvertMenu
    def createConvertMenu (self,tmenu):
    
        cc = self ; m = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(menu=m,label='Convert')
    
        m.add_command(
            label="Convert Node To Chapter",
            command=cc.makeNodeIntoChapter)
        m.add_command(
            label = "Convert Chapters To Simple Outline",
            command=cc.conversionToSimple)
        m.add_command(
            label = "Convert Top Nodes to Chapters",
            command=cc.convertTopLevelToChapters)
        try:
            import reportlab
            tmenu.add_command(label='Convert To PDF',command=cc.doPDFConversion)
        except Exception:
            pass
            # g.es("no reportlab")
    #@nonl
    #@-node:ekr.20060306151759.41:createConvertMenu
    #@+node:ekr.20060306151759.42:createEditorMenu
    def createEditorMenu (self,tmenu):
    
        cc = self
    
        m = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label="Editor",menu=m)
    
        m.add_command(label="Add Editor",command=cc.newEditor)
        m.add_command(label="Remove Editor",command=cc.removeEditor)
    #@nonl
    #@-node:ekr.20060306151759.42:createEditorMenu
    #@+node:ekr.20060306151759.43:createImportExportMenu
    def createImportExportMenu (self,tmenu):
    
        cc = self
    
        m = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label='Import/Export',menu=m)
    
        m.add_command(label="Import Leo File To Chapter",command=cc.importLeoFile)
        m.add_command(label="Export Chapter to Leo File",command=cc.exportLeoFile)
    #@nonl
    #@-node:ekr.20060306151759.43:createImportExportMenu
    #@+node:ekr.20060306151759.44:createIndexMenu
    def createIndexMenu (self,tmenu):
    
        cc = self
    
        m = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label='Index',menu=m)
    
        m.add_command(label='Make Index',command=cc.viewIndex)
        m.add_command(label='Make Regex Index',command=cc.regexViewIndex)
    #@-node:ekr.20060306151759.44:createIndexMenu
    #@+node:ekr.20060306151759.45:createNodeMenu
    def createNodeMenu (self,tmenu):
    
        cc = self
        opmenu = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(menu=opmenu,label='Node')
        
        cmenu = Tk.Menu(opmenu,tearoff=0)
        movmenu = Tk.Menu(opmenu,tearoff=0)
        copymenu = Tk.Menu(opmenu,tearoff=0)
        searchmenu = Tk.Menu(opmenu,tearoff=0)
        
        opmenu.add_cascade(menu=cmenu,label='Clone To Chapter')
        opmenu.add_cascade(menu=movmenu,label='Move To Chapter')
        opmenu.add_cascade(menu=copymenu,label='Copy To Chapter')
    
        def cloneToChapterCallback (cc=cc,menu=cmenu):
            cc.setupMenu(menu,cc.cloneToChapter)
        cmenu.configure(postcommand=cloneToChapterCallback)
    
        def moveToChapterCallback(cc=cc,menu=movmenu):
            cc.setupMenu(menu,cc.moveToChapter)
        movmenu.configure(postcommand=moveToChapterCallback)
        
        def copyToChapterCallback(cc=cc,menu=copymenu):
            cc.setupMenu(menu,cc.copyToChapter)
        copymenu.configure(postcommand=copyToChapterCallback)
    #@nonl
    #@-node:ekr.20060306151759.45:createNodeMenu
    #@+node:ekr.20060306151759.46:createTrashMenu
    def createTrashMenu (self,tmenu):
    
        cc = self
    
        m = Tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(menu=m,label='Trash')
        
        m.add_command(label="Add Trash Barrel",command=cc.addTrashBarrel)
        m.add_command(label='Empty Trash Barrel',command=cc.emptyTrash)
    #@nonl
    #@-node:ekr.20060306151759.46:createTrashMenu
    #@+node:ekr.20060306151759.47:setupMenu
    def setupMenu (self,menu,command,all=False):
    
        '''Create a menu.'''
        
        cc = self ; nb = cc.nb
    
        menu.delete(0,'end')
        current = nb.getcurselection()
    
        i = 0
        for name in nb.pagenames():
            i = i + 1
            if name == current and not all: continue
            menu.add_command(
                label=str(i),command=lambda name=name: command(name))
    #@nonl
    #@-node:ekr.20060306151759.47:setupMenu
    #@-node:ekr.20060306151759.39:makeTabMenu & helpers
    #@-node:ekr.20060306151759.30:Birth
    #@+node:ekr.20060306151759.48:Callbacks
    #@+node:ekr.20060306151759.49:lowerPage
    def lowerPage (self,name):
    
        '''Set a lowered tabs color.'''
    
        cc = self ; tab = cc.nb.tab(name)
        
        tab.configure(
            background=cc.unselectedTabBackgroundColor,
            foreground=cc.unselectedTabForegroundColor)
    #@nonl
    #@-node:ekr.20060306151759.49:lowerPage
    #@+node:ekr.20060306151759.50:onFocusIn & helpers
    def onFocusIn (self,event,body,bodyCtrl):
        
        '''Set the focus to the proper body and bodyCtrl.'''
        
        cc = self ; c = cc.c ; nb = cc.nb
        
        # g.trace(event,id(body),id(bodyCtrl))
        
        changeCtrl = body.frame.bodyCtrl != bodyCtrl
        
        # Switch the injected ivars.
        body.frame.body = body
        body.frame.bodyCtrl = body.bodyCtrl
    
        if not hasattr(body,'lastChapter'):
            body.lastChapter = nb.getcurselection()
            
        # Select body.lastChapter if it exists, or the present chapter otherwise.
        pageName = cc.getValidChapterName(body.lastChapter)
        changePage = pageName != nb.getcurselection()
        if changePage:
            body.lastChapter = pageName
            nb.selectpage(pageName)
        
        cc.selectNodeForEditor(body)
        if changePage or changeCtrl:
            # Do this only if necessary: it interferes with the Find command.
            cc.activateEditor(body)
    #@nonl
    #@+node:ekr.20060306151759.51:getValidChapterName
    def getValidChapterName (self,name):
        
        '''Return name if its chapter still exists.
        Otherwise return the name of the presently selected tab.'''
        
        cc = self ; nb = cc.nb
    
        try:
            nb.index(name)
        except:
            name = nb.getcurselection()
            
        # g.trace(name)
        return name
    #@nonl
    #@-node:ekr.20060306151759.51:getValidChapterName
    #@+node:ekr.20060306151759.52:selectNodeForEditor
    def selectNodeForEditor (self,body):
    
        '''Select the next node for the editor.'''
        
        cc = self ; c = cc.c
    
        if not hasattr(body,'lastPosition'):
            body.lastPosition = c.currentPosition()
    
        if body.lastPosition == c.currentPosition():
            pass
        elif body.lastPosition.exists(c):
            c.selectPosition(body.lastPosition)
        else:
            g.trace('last position does not exist',color='red')
            c.selectPosition(c.rootPosition())
    
        body.lastPosition = c.currentPosition()
        # g.trace(body.lastPosition.headString())
    #@nonl
    #@-node:ekr.20060306151759.52:selectNodeForEditor
    #@-node:ekr.20060306151759.50:onFocusIn & helpers
    #@+node:ekr.20060306151759.53:raisePage
    def raisePage (self,name):
        
        cc = self ; c = cc.c ; tab = cc.nb.tab(name)
    
        tab.configure(
            background=cc.selectedTabBackgroundColor,
            foreground=cc.selectedTabForegroundColor)
        
        # This must be called before queuing up the callback.
        self.setTree(name)
        
        # This can not be called immediately
        def idleCallback(event=None,c=c):
            c.invalidateFocus()
            c.bodyWantsFocusNow()
            
        w = c.frame.body and c.frame.body.bodyCtrl
        w and w.after_idle(idleCallback)
    #@-node:ekr.20060306151759.53:raisePage
    #@+node:ekr.20060306151759.54:setTree
    def setTree (self,name):
    
        cc = self ; c = cc.c
        chapter = self.getChapter(name)
        sv = chapter and chapter.sv
        
        # g.trace(name,g.callers())
        
        if not sv:
            # The page hasn't been fully created yet.  This is *not* an error.
            return None
    
        chapter.makeCurrent()
        
        # Set body ivars.
        body = c.frame.body
        body.lastChapter = name
        body.lastPosition = chapter.cp
        
        # Configure the tab.
        tab = cc.nb.tab(name)
        self.activateEditor(c.frame.body)
    #@nonl
    #@-node:ekr.20060306151759.54:setTree
    #@-node:ekr.20060306151759.48:Callbacks
    #@+node:ekr.20060306151759.55:Commands
    #@+node:ekr.20060306151759.56:Trash
    #@+node:ekr.20060306151759.57:addTrashBarrel
    def addTrashBarrel (self,event=None):
    
        c = self.c ; trash = 'Trash'
        
        if self.getChapter(trash):
            return
    
        self.addPage(trash)
        chapter = self.getChapter(trash)
        chapter.sv.set(trash)
        chapter.rp.setHeadString(trash+' barrel')
        self.renumber()
    #@nonl
    #@-node:ekr.20060306151759.57:addTrashBarrel
    #@+node:ekr.20060306151759.58:emptyTrash
    def emptyTrash (self):
        
        cc = self ; c = cc.c ; trash = 'Trash'
        
        chapter = self.getChapter(trash)
        if not chapter: return
    
        root = chapter.rp
        chapter.setVariables()
        p = root.insertAfter()
        p.moveToRoot()
        p.setHeadString(trash+' barrel')
        chapter.rp = c.rootPosition()
        chapter.cp = c.currentPosition()
        chapter.tp = c.topPosition()
        cc.currentChapter.setVariables()
        
        c.beginUpdate()
        try:
            c.selectPosition(p)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20060306151759.58:emptyTrash
    #@-node:ekr.20060306151759.56:Trash
    #@+node:ekr.20060306151759.59:Chapter ops
    #@+node:ekr.20060306151759.60:addChapter
    def addChapter (self,event=None):
        
        cc = self ; c = cc.c
        cc.addPage()
        cc.renumber()
        c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20060306151759.60:addChapter
    #@+node:ekr.20060306151759.61:convertTopLevelToChapters
    def convertTopLevelToChapters (self):
        
        cc = self ; c = cc.c
    
        # It's more intuitive to leave the root position where it is.
        p = c.rootPosition().next()
        
        # Dont' use an iterator here! makeNodeIntoChapter deletes nodes.
        while p:
            next = p.next()
            # g.trace(p.headString())
            self.makeNodeIntoChapter(p=p,redraw=False)
            p = next
    
        cc.setTree(cc.nb.pagenames()[0])
        c.redraw_now()
    #@nonl
    #@-node:ekr.20060306151759.61:convertTopLevelToChapters
    #@+node:ekr.20060306151759.62:conversionToSimple
    def conversionToSimple (self):
        
        cc = self ; c = cc.c ; nb = cc.nb
        
        # Set last to the last top-level node.
        for p in c.rootPosition().self_and_siblings_iter():
            last = p.copy()
    
        pagenames = nb.pagenames()
        current = nb.getcurselection()
        pagenames.remove(current)
       
        for pageName in pagenames:
            chapter = self.getChapter(pageName)
            # We can't use an iterator here because we are moving nodes.
            p = chapter.rp
            while p:
                next = p.next()
                p.moveAfter(last)
                last = p.copy() ; p = next
            nb.delete(pageName)
        
        nb.selectpage(current)
        self.renumber()
        c.redraw_now()
    #@nonl
    #@-node:ekr.20060306151759.62:conversionToSimple
    #@+node:ekr.20060306151759.63:doPDFConversion & helper
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
        n = 0
        for z in pagenames:
            chapter = self.getChapter(z)
            chapter.setVariables()
            p = chapter.rp
            if p:
                self._changeTreeToPDF(chapter.sv.get(),n,p,c,Story,styles,maxlen)
            n += 1
        #@    << define otherPages callback >>
        #@+node:ekr.20060306151759.64:<< define otherPages callback >>
        def otherPages (canvas,doc,pageinfo=pinfo):
        
            canvas.saveState()
            canvas.setFont('Times-Roman',9)
            canvas.drawString(inch,0.75*inch,"Page %d %s" % (doc.page,pageinfo))
            canvas.restoreState()
        #@nonl
        #@-node:ekr.20060306151759.64:<< define otherPages callback >>
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
    #@+node:ekr.20060306151759.65:_changeTreeToPDF
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
    #@-node:ekr.20060306151759.65:_changeTreeToPDF
    #@-node:ekr.20060306151759.63:doPDFConversion & helper
    #@+node:ekr.20060306151759.66:exportLeoFile
    def exportLeoFile (self,event=None):
    
        c = self.c
    
        name = tkFileDialog.asksaveasfilename()
    
        if name:
            if not name.endswith('.leo'): name = name + '.leo'
            c.fileCommands.write_Leo_file(name,False,singleChapter=True)
    #@nonl
    #@-node:ekr.20060306151759.66:exportLeoFile
    #@+node:ekr.20060306151759.67:importLeoFile
    def importLeoFile (self,event=None):
        
        cc = self ; c = cc.c ; nb = cc.nb
    
        fileName = tkFileDialog.askopenfilename()
    
        if fileName:
            cc.addPage()
            c.fileCommands.open(file(fileName,'r'),fileName)
            cc.currentChapter.makeCurrent()
            cc.renumber()
    #@nonl
    #@-node:ekr.20060306151759.67:importLeoFile
    #@+node:ekr.20060306151759.68:makeNodeIntoChapter
    def makeNodeIntoChapter (self,p=None,redraw=True):
        
        cc = self ; c = cc.c
        renum = p and p.copy()
        if not p: p = c.currentPosition()
        
        if p == c.rootPosition() and not p.next(): return
        
        c.beginUpdate()
        try:
            p.doDelete()
        finally:
            c.endUpdate(False)
        
        page,pageName = self.addPage()
        mnChapter = self.getChapter(pageName)
        oldChapter = cc.currentChapter
        mnChapter.makeCurrent()
        root = mnChapter.rp
        p.moveAfter(root)
        c.setRootPosition(p)
        oldChapter.makeCurrent()
       
        c.beginUpdate()
        try:
            if not renum: self.renumber()
            c.selectPosition(oldChapter.rp)
        finally:
            c.endUpdate(redraw)
            if redraw: cc.nb.selectpage(pageName)
    #@nonl
    #@-node:ekr.20060306151759.68:makeNodeIntoChapter
    #@+node:ekr.20060306151759.69:removeChapter
    def removeChapter (self,name):
    
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
    #@-node:ekr.20060306151759.69:removeChapter
    #@+node:ekr.20060306151759.70:renameChapter
    def renameChapter (self,event=None):
        
        '''Insert a entry widget linked to chapter.sv.
        Changing this Tk.StringVar immediately changes all the chapter's labels.'''
    
        cc = self ; c = cc.c ; nb = cc.nb
        name = nb.getcurselection()
        index = nb.index(name)
        frame = nb.page(name)
        tab = nb.tab(name)
        chapter = cc.chapters.get(name)
        # g.trace(chapter)
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
    #@-node:ekr.20060306151759.70:renameChapter
    #@+node:ekr.20060306151759.71:swapChapters
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
        c.redraw_now()
        val1 = tv1.get()
        val2 = tv2.get()
        if val2.isdigit():
            tv1.set(nb.index(cselection)+1)
        else: tv1.set(val2)
        if val1.isdigit():
            tv2.set(nb.index(name)+1)
        else: tv2.set(val1)
    #@nonl
    #@-node:ekr.20060306151759.71:swapChapters
    #@-node:ekr.20060306151759.59:Chapter ops
    #@+node:ekr.20060306151759.72:Indexing
    #@+at
    # Indexing is complementary to find, it provides a gui Index of nodes.
    # 
    # In comparison to regular find which bounces you around the tree,
    # you can preview the node before you go to it.
    #@-at
    #@+node:ekr.20060306151759.73:viewIndex
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
            #@+node:ekr.20060306151759.74:<< define scTo callback >>
            def scTo (event,nodes=nodes,sve=sve,can=can,tags=tags):
            
                t = sve.get()
                if event.keysym == 'BackSpace':
                    t = t [: -1]
                else:
                    t = t + event.char
                if t:
                    for z in nodes:
                        if z [0].startswith(t) and tags.has_key(z[1]):
                            tg = tags [z [1]]
                            eh = can.bbox(self.ltag) [1]
                            eh = (eh*1.0) / 100
                            bh = can.bbox(tg) [1]
                            ncor = (bh/eh) * .01
                            can.yview('moveto',ncor)
                            return
            #@nonl
            #@-node:ekr.20060306151759.74:<< define scTo callback >>
            #@nl
            e.bind('<Key>',scTo)
            e.focus_set()
    #@nonl
    #@-node:ekr.20060306151759.73:viewIndex
    #@+node:ekr.20060306151759.75:buildIndex
    def buildIndex (self,nodes,can,tl,bal,tags):
    
        cc = self ; c = cc.c ; nb = cc.nb
        f = tkFont.Font()
        f.configure(size=-20)
        ltag = None
        i = 0
        for z in nodes:
            i += 1
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
            self.ltag = ltag = tags [z [1]] = can.create_text(
                20,i*20+20,text=txt,fill='blue',font=f,anchor=Tk.W,tag=tg)
            bs = z [1].bodyString()
            if bs.strip() != '':
                bal.tagbind(can,tg,bs)
            #@        << def callbacks >>
            #@+node:ekr.20060306151759.76:<< def callbacks >>
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
            #@-node:ekr.20060306151759.76:<< def callbacks >>
            #@nl
            can.tag_bind(tg,'<Button-1>',goto)
            can.tag_bind(tg,'<Enter>',colorRd,'+')
            can.tag_bind(tg,'<Leave>',colorBl,'+')
    #@nonl
    #@-node:ekr.20060306151759.75:buildIndex
    #@+node:ekr.20060306151759.77:regexViewIndex
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
    #@-node:ekr.20060306151759.77:regexViewIndex
    #@-node:ekr.20060306151759.72:Indexing
    #@+node:ekr.20060306151759.78:Node ops
    #@+node:ekr.20060306151759.79:cloneToChapter
    def cloneToChapter (self,name):
    
        cc = self ; c = cc.c ; p = c.currentPosition()
    
        chapter = self.getChapter(name)
        back = p.back()
        if back:
            clone = p.clone(back)
            p2 = chapter.cp
            clone.unlink()
            clone.linkAfter(p2)
            chapter.makeCurrent()
        
            # Warning: c.begin/endUpdate not valid spanning chapter.makeCurrent()
            c.beginUpdate()
            try:
                c.selectPosition(clone)
                c.setChanged(True)
            finally:
                c.endUpdate()
    #@-node:ekr.20060306151759.79:cloneToChapter
    #@+node:ekr.20060306151759.80:copyToChapter
    def copyToChapter (self,name):
    
        cc = self ; c = cc.c ; nb = cc.nb
        page = nb.page(nb.index(name))
        chapter = cc.getChapter(name)
        s = c.fileCommands.putLeoOutline()
        p = c.fileCommands.getLeoOutline(s)
        chapter.setVariables()
        p2 = chapter.cp
        p.moveAfter(p2)
        cc.currentChapter.setVariables()
        chapter.makeCurrent()
    
        # Warning: c.begin/endUpdate not valid spanning chapter.makeCurrent()
        c.beginUpdate()
        try:
            c.selectPosition(p)
            c.setChanged(True)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20060306151759.80:copyToChapter
    #@+node:ekr.20060306151759.81:moveToChapter
    def moveToChapter (self,name):
        
        cc = self ; c = cc.c
        chapter = cc.getChapter(name)
        
        p = c.currentPosition()
        if p.hasParent() or p.hasBack():
            p2 = chapter.cp
            p.unlink()
            p.linkAfter(p2)
            chapter.makeCurrent()
            
            # Warning: c.begin/endUpdate not valid spanning chapter.makeCurrent()
            c.beginUpdate()
            try:
                c.selectPosition(p)
                c.setChanged(True)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20060306151759.81:moveToChapter
    #@+node:ekr.20060306151759.82:regexClone & helper
    def regexClone (self,name=None):
    
        cc = self ; c = cc.c ; nb = cc.nb
    
        chapter = self.getChapter(name)
    
        d = Pmw.PromptDialog(c.frame.top,
            title = 'Search and Clone',
            buttons = ('Search','Cancel'),
            defaultbutton = 'Search',
        )
        e = d.component('entry')
        e.bind
    
        def regexCloneCallback (result,cc=cc,e=e,d=d,chapter=chapter):
            s = e.get() # Do this before destroying d.d
            d.deactivate() ; d.destroy()
            if result != 'Cancel':
                cc.cloneWalk(chapter,s)
    
        d.configure(command=regexCloneCallback)
        d.activate(geometry='centerscreenalways')
    #@+node:ekr.20060306151759.83:cloneWalk
    def cloneWalk (self,chapter,s):
        cc = self ; c = cc.c ; nb = cc.nb
        regex = re.compile(s)
        root = chapter.cp
        chapter.setVariables()
        t = leoNodes.tnode('',s)
        v = leoNodes.vnode(c,t)
        p = leoNodes.position(c,v,[])
        p.moveAfter(root)
        ignorelist = [p.v.t]
        it = self.walkChapters(ignorelist=ignorelist)
        for z in it:
            f = regex.search(z.bodyString())
            if f:
                clone = z.clone(z)
                i = p.numberOfChildren()
                clone.moveToNthChildOf(p,i)
                ignorelist.append(clone.v.t)
        cc.currentChapter.setVariables()
        nb.selectpage(chapter.pageName)
        c.beginUpdate()
        try:
            p.moveToRoot(root)
            c.setChanged(True)
            c.selectPosition(p)
            p.expand()
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20060306151759.83:cloneWalk
    #@-node:ekr.20060306151759.82:regexClone & helper
    #@-node:ekr.20060306151759.78:Node ops
    #@-node:ekr.20060306151759.55:Commands
    #@+node:ekr.20060306151759.84:Editor
    #@+node:ekr.20060306151759.85:...Heading
    #@+node:ekr.20060306151759.86:addHeading
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
        
        for w in (lt_label,rt_label,f,parentFrame):
            w.configure(bg=cc.editorLabelBackgroundColor)
        for w in (lt_label,rt_label):
             w.configure(fg=cc.editorLabelForegroundColor)
    
        return lt_label, rt_label, f
    #@nonl
    #@-node:ekr.20060306151759.86:addHeading
    #@+node:ekr.20060306151759.87:hide/showHeading
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
    #@-node:ekr.20060306151759.87:hide/showHeading
    #@-node:ekr.20060306151759.85:...Heading
    #@+node:ekr.20060306151759.88:activateEditor
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
        # g.trace(id(body.bodyCtrl),p.headString())
    #@nonl
    #@-node:ekr.20060306151759.88:activateEditor
    #@+node:ekr.20060306151759.89:newEditor
    def newEditor (self):
    
        cc = self ; c = cc.c
        
        pane = self.createEditorPane()
        body = leoTkinterBody(self.frame,pane)
        c.frame.bodyCtrl = body.bodyCtrl # Make body the 'official' body.
        body.setFontFromConfig()
        body.setColorFromConfig()
        body.createBindings()
        c.k.completeAllBindingsForWidget(body.bodyCtrl)
        body.bodyCtrl.focus_set()
        body.lastPosition = c.currentPosition()
        cc.activateEditor(body)
    
        # Configure the generic editor label for this chapter and position.
        chapter = cc.getChapter()
        body.editorLeftLabel.configure(textvariable=chapter.sv)
        body.editorRightLabel.configure(text=c.currentPosition().headString())
    #@nonl
    #@-node:ekr.20060306151759.89:newEditor
    #@+node:ekr.20060306151759.90:removeEditor
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
    #@nonl
    #@-node:ekr.20060306151759.90:removeEditor
    #@-node:ekr.20060306151759.84:Editor
    #@+node:ekr.20060306151759.91:Files
    #@+at 
    #@nonl
    # We need to decorate and be tricky here, since a Chapters leo file is a 
    # zip file.
    # 
    # These functions are easy to break in my experience. :)
    #@-at
    #@nonl
    #@+node:ekr.20060306151759.92:Reading
    #@+node:ekr.20060306151759.93:openChaptersFile
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
    
    #@-node:ekr.20060306151759.93:openChaptersFile
    #@+node:ekr.20060306151759.94:insertChapters
    def insertChapters (self,chapters):
    
        cc = self ; c = cc.c ; nb = cc.nb ; pagenames = nb.pagenames()
        flipto = None
        c.beginUpdate()
        try:
            i = 0
            for tup in chapters:
                x, y = tup
                if i > 0:
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
                if i == 0: flipto = cselection
                i += 1
            self.setTree(flipto)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20060306151759.94:insertChapters
    #@-node:ekr.20060306151759.92:Reading
    #@+node:ekr.20060306151759.95:Writing
    #@+node:ekr.20060306151759.96:writeChapters
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
    #@-node:ekr.20060306151759.96:writeChapters
    #@+node:ekr.20060306151759.97:zipChapters
    def zipChapters (self,fileName,pagenames,chapList):
    
        '''Writes StringIO instances to a zipped file.'''
        
        cc = self
    
        zf = zipfile.ZipFile(fileName,'w',zipfile.ZIP_DEFLATED)
    
        i = 0
        for pageName in pagenames:
            sv = cc.getChapter(pageName).sv
            zif = zipfile.ZipInfo(str(i))
            zif.comment = sv.get() or ''
            zif.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zif,chapList[i])
            i += 1
    
        zf.close()
    #@nonl
    #@-node:ekr.20060306151759.97:zipChapters
    #@-node:ekr.20060306151759.95:Writing
    #@-node:ekr.20060306151759.91:Files
    #@+node:ekr.20060306151759.98:Overrides
    #@+node:ekr.20060306151759.99:createCanvas (injects ivars for treeInit)
    def createCanvas (self,frame,parentFrame,pageName):
        
        cc = self
                
        # Set ivars for cc.treeInit.
        page,button = cc.createTab(pageName)
        cc.newPageName = pageName
        cc.newPage = page
    
        # Create the canvas with page as the parentFrame.
        cc.newCanvas = canvas = old_createCanvas(frame,page) 
    
        # g.trace(pageName,id(canvas))
        return canvas
    #@nonl
    #@-node:ekr.20060306151759.99:createCanvas (injects ivars for treeInit)
    #@+node:ekr.20060306151759.100:createControl (tkBody)
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
        
        # Create a focus-in event to keep the generic label widget in synch.
        def focusInCallback(event,self=self,frame=frame):
            return self.onFocusIn(event,body,ctrl)
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
    #@-node:ekr.20060306151759.100:createControl (tkBody)
    #@+node:ekr.20060306151759.101:doDelete
    def doDelete (self,p):
        
        '''Override p.doDelete to add nodes to the trash if it exists.'''
        
        cc = self ; c = cc.c ; nb = cc.nb ;  trash = 'Trash'
        
        # Do nothing if the node can't be deleted.
        newNode = p and (p.visBack() or p.next()) # *not* p.visNext()
        if not newNode: return
        
        name = nb.getcurselection()
        if name != trash and trash in nb.pagenames():
            chapter = self.getChapter(trash)
            trashnode = chapter.rp
            chapter.setVariables()
            p.moveAfter(trashnode)
            cc.currentChapter.setVariables()
            c.selectPosition(newNode)
            return p
        else:
            return old_doDelete(p)
    #@nonl
    #@-node:ekr.20060306151759.101:doDelete
    #@+node:ekr.20060306151759.102:getLeoFile
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
    #@-node:ekr.20060306151759.102:getLeoFile
    #@+node:ekr.20060306151759.103:select
    def select (self,tree,p,updateBeadList=True):
    
        cc = self ; c = p.v.c ; h = p.headString() ; nb = cc.nb
    
        c.frame.body.lastPosition = p.copy()
        return_val = old_select(tree,p,updateBeadList)
    
        c.frame.body.lastChapter = n = nb.getcurselection()
        chapter = cc.getChapter(n)
        chapter._saveInfo()
    
        if hasattr(p.c.frame.body,'editorRightLabel'):
            h = p.headString() or ''
            c.frame.body.editorRightLabel.configure(text=h)
    
        return return_val
    #@nonl
    #@-node:ekr.20060306151759.103:select
    #@+node:ekr.20060306151759.104:open
    def open (self,fc,file,fileName,readAtFileNodesFlag=True,silent=False):
    
        cc = self ; c = cc.c
    
        if zipfile.is_zipfile(fileName):
            c.beginUpdate()
            try:
                # Set globals for g.os_path_dirname
                global iscStringIO, stringIOCommander
                iscStringIO = True ; stringIOCommander = c
                chapters = cc.openChaptersFile(fileName)
                g.es(str(len(chapters))+" Chapters To Read",color='blue')
                cc.insertChapters(chapters)
                g.es("Finished Reading Chapters",color='blue')
                iscStringIO = False
            finally:
                c.endUpdate()
            return True
        else:
            return old_open(fc,file,fileName,readAtFileNodesFlag,silent)
    #@nonl
    #@-node:ekr.20060306151759.104:open
    #@+node:ekr.20060306151759.105:treeInit (creates Chapter)
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
    #@-node:ekr.20060306151759.105:treeInit (creates Chapter)
    #@+node:ekr.20060306151759.106:write_Leo_file
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
    #@-node:ekr.20060306151759.106:write_Leo_file
    #@-node:ekr.20060306151759.98:Overrides
    #@+node:ekr.20060306151759.107:Utils
    #@+node:ekr.20060306151759.108:addPage
    def addPage (self,pageName=None):
    
        cc = self ; c = cc.c
        if not pageName:
            pageName = str(len(cc.nb.pagenames()) + 1)
        
        # g.trace(pageName,cc.chapters.keys())
        
        old_chapter = cc.currentChapter
        junk, page = cc.constructTree(self.frame,pageName)
            # Creates a canvas, new tab and a new tree.
    
        old_chapter.makeCurrent() # Essential to capture the present values.
        chapter = cc.getChapter(cc.newPageName)
        chapter.makeCurrent()
        return page,pageName
    #@nonl
    #@-node:ekr.20060306151759.108:addPage
    #@+node:ekr.20060306151759.109:getChapter
    def getChapter (self,pageName=None):
        
        cc = self
    
        return self.chapters.get(pageName or cc.nb.getcurselection())
    #@nonl
    #@-node:ekr.20060306151759.109:getChapter
    #@+node:ekr.20060306151759.110:renumber
    def renumber (self):
        
        cc = self ; nb = cc.nb
            
        i = 0
        for name in nb.pagenames():
            i += 1
            tab = nb.tab(name)
            tab.configure(text=str(i))
    #@nonl
    #@-node:ekr.20060306151759.110:renumber
    #@+node:ekr.20060306151759.111:walkChapters
    def walkChapters (self,ignorelist=[],chapname=False):
    
        '''A generator that allows one to walk the chapters as one big tree.'''
    
        for z in self.nb.pagenames():
            chapter = self.getChapter(z)
            for p in chapter.rp.allNodes_iter():
                if chapname:
                    if p not in ignorelist: yield p.copy(), z
                else:
                    if p.v.t not in ignorelist: yield p.copy()
    #@nonl
    #@-node:ekr.20060306151759.111:walkChapters
    #@-node:ekr.20060306151759.107:Utils
    #@-others
#@nonl
#@-node:ekr.20060306151759.29:class chapterController
#@-others
#@nonl
#@-node:ekr.20060306151759.1:@thin chapters2.py
#@-leo
