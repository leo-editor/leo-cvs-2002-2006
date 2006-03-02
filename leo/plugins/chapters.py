#@+leo-ver=4-thin
#@+node:mork.20040926105355.1:@thin chapters.py
#@<<docstring>>
#@+node:ekr.20041109123143:<<docstring>>
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
#@-node:ekr.20041109123143:<<docstring>>
#@nl

# To do:  Find/Change does not appear to work.
# To do: replace all v refs by p refs.
# ***Testing***.

#@@language python
#@@tabwidth -4

__version__ = "0.70"
#@<< version history >>
#@+node:ekr.20041103051117:<< version history >>
#@+others
#@+node:ekr.20060212112134:Before Leo 4.4
#@+at
# 
# v .2
# 
# 1. Trash. If there is a Chapter in the Leo project called 'Trash' all 
# deleted nodes are deposited there. Then when deleted in the 'Trash' chapter 
# it is finally removed. There is an option to quickly add a Trash barrel in 
# the menu.
# 2. Menu moved from Outline to being summoned by right clicking on a chapter 
# tab or in the area of the tabs.
# 3. Swapping Chapters. Swap one Chapter for another one.
# 4. Conversion ops. Take one Outline and turn each node into a Chapter. The 
# convers operation is also there, take each top level node in each Chapter 
# and add it to one Chapter.
# 5. Import/Export. You are now able to load leo files as Chapters. This 
# means, for example, that if you have 5 Outlines that you would like to bind 
# together as one Leo file but keep their separateness you can now import 
# those 5 Outlines into there own Chapters. You can also Export a single 
# Chapter into it's own separate Leo file.
# 6. Search and Clone. This functionality is very similar to the Filtered 
# Hoist concept. You decide which Chapter you want your search results to 
# appear in and a dialog will pop up. You can enter simple text or a more 
# complex regular expression and the function will search all the outlines and 
# create a node with the results as children.
# 7. Editors now have headlines indicating what Chapters and what node are 
# being worked on.
# 
# v .6 EKR: Based on version .5 by Leo User.
# 
# - Added g. before all functions in leoGlobals.py.
# - Right clicking on Chapter tab crashes.
# 
# .61 fixed up a couple of spots.
# 
# .62 EKR: Restored conditional call to g.app.createTkGui(__file__) in startup 
# code.
# 
# .63 EKR: Added long docstring.
# 
# .64 fixed cloneWalk and PDF Convertor.
# 
# .65 EKR: added new keyword args to newGetLeoFile and newOpen.
#     - This is needed because of changes to the corresponding method's in 
# Leo's core.
# 
# .66 EKR: use notebooks.get(c) throughout.
#     - c may not exist during unit testing.  Not a complete fix, not tested!
# 
# .67 EKR:
#     - Added 'silent' keywords to newGetLeoFile and newOpen.
# .68 EKR:
#     - Use 'c._xPosition. or c.nullPosition()' to init so that c._xPosition 
# is never None.
#@-at
#@nonl
#@-node:ekr.20060212112134:Before Leo 4.4
#@-others

#@@nocolor

#@+at 
#@nonl
# New in Leo 4.4b2:
# 
# v .70 EKR:
# - init returns proper status.
# - Code cleanup related to positions.
# v .71 EKR:
# - A few crashes fixed.
# 
#@-at
#@-node:ekr.20041103051117:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20041103050629:<< imports >>
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
#@-node:ekr.20041103050629:<< imports >>
#@nl
#@<< globals >>
#@+node:mork.20040926105355.2:<< globals >>
chapters = {}
editorNames = {}
frames = {}
iscStringIO = False
notebooks = {}
pbodies = {}
twidgets = {}

#@-node:mork.20040926105355.2:<< globals >>
#@nl
#@<< remember the originals for decorated methods >>
#@+node:ekr.20060212123927:<< remember the originals for decorated methods >>
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
#@-node:ekr.20060212123927:<< remember the originals for decorated methods >>
#@nl

# Solve problems with string.atoi...
import string
string.atoi = int

#@+others
#@+node:ekr.20060109063941:init
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
            #@+node:ekr.20041103054545:<< override various methods >>
            # Override the 10 originals...
            
            leoTkinterFrame.leoTkinterFrame.createCanvas    = newCreateCanvas
            leoTkinterFrame.leoTkinterBody.createControl    = newCreateControl
            leoNodes.position.doDelete                      = newDoDelete
            leoTkinterTree.leoTkinterTree.endEditLabel      = newEndEditLabel
            leoFileCommands.fileCommands.getLeoFile         = newGetLeoFile
            leoFileCommands.fileCommands.open               = newOpen
            leoTkinterTree.leoTkinterTree.select            = newSelect
            leoTkinterTree.leoTkinterTree.__init__          = newTreeinit
            g.os_path_dirname                               = new_os_path_dirname
            leoFileCommands.fileCommands.write_Leo_file     = newWrite_LEO_file
            #@nonl
            #@-node:ekr.20041103054545:<< override various methods >>
            #@nl
            g.plugin_signon( __name__ )
            
    return ok
#@nonl
#@-node:ekr.20060109063941:init
#@+node:mork.20040927092626:class Chapter
class Chapter:
    '''The fundamental abstraction in the Chapters plugin.
       It enables the tracking of Chapters tree information.'''
       
    #@    @+others
    #@+node:ekr.20041103051228:__init__
    def __init__ (self,c,tree,frame,canvas):
    
        self.c = c
        self.tree = tree
        self.frame = frame
        self.canvas = canvas
        self.treeBar = frame.treeBar
    
        if hasattr(c,'cChapter'):
            tn = leoNodes.tnode('','New Headline')
            vn = leoNodes.vnode(c,tn)
            p = leoNodes.position(c,vn,[])
            self.cp = p.copy()
            self.rp = p.copy()
            self.tp = p.copy()
        else:
            c.cChapter = self
            self.cp = c._currentPosition or c.nullPosition()
            self.tp = c._topPosition or c.nullPosition()
            self.rp = c._rootPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20041103051228:__init__
    #@+node:ekr.20041103051228.1:_saveInfo
    def _saveInfo (self):
    
        c = self.c
        self.cp = c._currentPosition or c.nullPosition()
        self.rp = c._rootPosition or c.nullPosition()
        self.tp = c._topPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20041103051228.1:_saveInfo
    #@+node:ekr.20041103051228.2:setVariables
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
    #@-node:ekr.20041103051228.2:setVariables
    #@+node:ekr.20041103051228.3:makeCurrent
    def makeCurrent (self):
    
        c = self.c
        c.cChapter._saveInfo()
        c.cChapter = self
        self.setVariables()
        c.redraw()
        self.canvas.update_idletasks()
    #@nonl
    #@-node:ekr.20041103051228.3:makeCurrent
    #@-others
#@nonl
#@-node:mork.20040927092626:class Chapter
#@+node:mork.20040930090735:Creating widgets...
# This category deals with creating widgets and any support functions for doing so.
#@nonl
#@+node:mork.20040926105355.21:newCreateControl
def newCreateControl (self,frame,parentFrame):
    
    c = self.c ; notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    if c not in pbodies:
        parentFrame = createPanedWidget(parentFrame,c)
    pbody = pbodies [c]
    l, r = addHeading(parentFrame)
    ctrl = old_createControl(self,frame,parentFrame)
    ctrl.bind("<FocusIn>",lambda event,body=frame.body: getGoodPage(event,body),'+')
    i = 1.0 / len(pbody.panes())
    for z in pbody.panes():
        pbody.configurepane(z,size=i)
    pbody.updatelayout()
    frame.body.l = l
    frame.body.r = r
    frame.body.editorName = editorNames [parentFrame]
    if frame not in twidgets:
        twidgets [frame] = []
    twidgets [frame].append(frame.body)
    l.configure(textvariable=getSV(c,notebook.getcurselection()))
    return ctrl
#@nonl
#@-node:mork.20040926105355.21:newCreateControl
#@+node:mork.20040929110556:createPanedWidget
def createPanedWidget (parentFrame,c):

    '''Construct a new panedwidget for a frame.'''

    pbody = Pmw.PanedWidget(parentFrame,orient='horizontal')
    pbody.pack(expand=1,fill='both')
    pbodies [c] = pbody
    parentFrame = newEditorPane(c)
    return parentFrame
#@-node:mork.20040929110556:createPanedWidget
#@+node:mork.20040926105355.22:newEditorPane
def newEditorPane (c):

    names = pbodies [c].panes()
    if names:
        name = str(int(names[-1])+1)
    else:
        name = '1'
    zpane = pbodies [c].add(name)
    editorNames [zpane] = name
    return zpane

#@-node:mork.20040926105355.22:newEditorPane
#@+node:mork.20040926105355.23:newCreateCanvas
def newCreateCanvas (self,parentFrame):

    c = self.c
    if c in frames:
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing
    else:
        frames [c] = self
        notebook = createNoteBook(c,parentFrame)

    pname = notebook.nameMaker.next()
    page = notebook.add(pname)
    indx = notebook.index(pname)
    tab = notebook.tab(indx)
    if indx == 0:
        tab.configure(background='grey',foreground='white')
    canvas = old_createCanvas(self,page)
    hull = notebook.component('hull')
    tab.bind('<Button-3>',lambda event: hull.tmenu.post(event.x_root,event.y_root))
    sv = Tk.StringVar()
    page.sv = sv
    createBalloon(tab,sv)
    canvas.name = pname
    return canvas
#@-node:mork.20040926105355.23:newCreateCanvas
#@+node:mork.20040929120442:createBalloon
def createBalloon (tab,sv):

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
#@-node:mork.20040929120442:createBalloon
#@+node:mork.20040929102107:createNoteBook
def createNoteBook (c,parentFrame):

    '''Construct a NoteBook widget for a frame.'''

    notebooks [c] = notebook = Pmw.NoteBook(parentFrame,borderwidth=1,pagemargin=0)
    hull = notebook.component('hull')
    makeTabMenu(hull,notebook,c)
    notebook.configure(raisecommand=lambda name,notebook=notebook: setTree(c,name,notebook))
    notebook.configure(lowercommand=lambda name,notebook=notebook: lowerPage(name,notebook))
    notebook.pack(fill='both',expand=1)
    notebook.nameMaker = getNameMaker(notebook)
    return notebook
#@nonl
#@-node:mork.20040929102107:createNoteBook
#@+node:mork.20040929093051:getNameMaker
def getNameMaker (notebook):

    '''Create a numbering mechanism for tabs.'''

    def nameMaker ():
        i = 0
        while 1:
            if len(notebook.pagenames())== 0: i = 0
            i += 1
            yield str(i)

    return nameMaker()
#@nonl
#@-node:mork.20040929093051:getNameMaker
#@+node:mork.20040926105355.24:newTreeinit
def newTreeinit (self,c,frame,canvas):

    sv = getSV(c,canvas.name)
    
    global old_tree_init
    old_tree_init(self,c,frame,canvas)

    self.chapter = chapters [sv] = Chapter(c,self,frame,canvas)
#@nonl
#@-node:mork.20040926105355.24:newTreeinit
#@+node:mork.20040926105355.25:constructTree
def constructTree (frame,notebook,name):

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
    indx = notebook.index(notebook.pagenames()[-1])
    tab = notebook.tab(indx)
    tnum = str(len(notebook.pagenames()))
    tab.configure(text=tnum)
    hull = notebook.component('hull')
    tab.bind('<Button-3>',lambda event,hull=hull: hull.tmenu.post(event.x_root,event.y_root))
    return tree, notebook.page(notebook.pagenames()[-1])
#@nonl
#@-node:mork.20040926105355.25:constructTree
#@+node:mork.20040926105355.26:addPage
def addPage (c,name=None):

    frame = frames [c] ; notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    if name == None: name = str(len(notebook.pagenames())+1)
    o_chapter = c.cChapter
    otree, page = constructTree(frame,notebook,name)
    c.cChapter.makeCurrent()
    o_chapter.makeCurrent()
    return page
#@-node:mork.20040926105355.26:addPage
#@+node:mork.20040926105355.35:newEditor
def newEditor (c):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    frame = frames [c]
    pbody = pbodies [c]
    zpane = newEditorPane(c)
    af = leoTkinterBody(frame,zpane)
    c.frame.bodyCtrl = af.bodyCtrl
    af.setFontFromConfig()
    af.createBindings() # .71
    af.bodyCtrl.focus_set()
    cname = notebook.getcurselection()
    af.l.configure(textvariable=getSV(c,cname))
    af.r.configure(text=c.currentPosition().headString())
#@nonl
#@-node:mork.20040926105355.35:newEditor
#@-node:mork.20040930090735:Creating widgets...
#@+node:mork.20040930091319:tab menu stuff
#@+at
# Tab menu and factory functions for the tab menu creation process.
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.41:makeTabMenu
def makeTabMenu (widget,notebook,c):
    '''Creates a tab menu.'''
    tmenu = Tk.Menu(widget,tearoff=0)
    widget.bind('<Button-3>',lambda event: tmenu.post(event.x_root,event.y_root))
    widget.tmenu = tmenu
    tmenu.add_command(command=tmenu.unpost)
    tmenu.add_separator()
    ac = getAddChapter(c,notebook)
    tmenu.add_command(label='Add Chapter',command=ac)
    rmenu = Tk.Menu(tmenu,tearoff=0)
    remove = getRemove(notebook,c,rmenu)
    rmenu.configure(postcommand=remove)
    tmenu.add_cascade(menu=rmenu,label="Remove Chapter")
    rename = getRename(c,notebook)
    tmenu.add_command(label="Add/Change Title",command=rename)
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
    opmenu.add_command(label="Make Node Into Chapter",command=lambda c=c: makeNodeIntoChapter(c))
    mkTrash = getMakeTrash(notebook)
    opmenu.add_command(label="Add Trash Barrel",command=
    lambda c = c: mkTrash(c))
    opmenu.add_command(label='Empty Trash Barrel',command=
    lambda notebook = notebooks.get(c), c = c: emptyTrash(notebook,c))
    setupMenu = getSetupMenu(c,notebook)
    cmenu.configure(
        postcommand = lambda menu = cmenu, command = cloneToChapter: setupMenu(menu,command))
    movmenu.configure(
        postcommand = lambda menu = movmenu, command = moveToChapter: setupMenu(menu,command))
    copymenu.configure(
        postcommand = lambda menu = copymenu, command = copyToChapter: setupMenu(menu,command))
    swapmenu.configure(postcommand=
    lambda menu = swapmenu, command = swapChapters: setupMenu(menu,command))
    searchmenu.configure(postcommand=lambda menu=searchmenu,
    command = regexClone: setupMenu(menu,command,all=True))
    edmenu = Tk.Menu(tmenu,tearoff=0)
    tmenu.add_cascade(label="Editor",menu=edmenu)
    edmenu.add_command(label="Add Editor",command=lambda c=c: newEditor(c))
    edmenu.add_command(label="Remove Editor",command=lambda c=c: removeEditor(c))
    conmenu = Tk.Menu(tmenu,tearoff=0)
    tmenu.add_cascade(menu=conmenu,label='Conversion')
    conmenu.add_command(
        label = "Convert To Simple Outline",
        command = lambda c = c: conversionToSimple(c))
    conmenu.add_command(
        label = "Convert Simple Outline into Chapters",
        command = lambda c = c: conversionToChapters(c))
    iemenu = Tk.Menu(tmenu,tearoff=0)
    tmenu.add_cascade(label='Import/Export',menu=iemenu)
    iemenu.add_command(label="Import Leo File ",command=lambda c=c: importLeoFile(c))
    iemenu.add_command(label="Export Chapter To Leo File",command=lambda c=c: exportLeoFile(c))
    indmen = Tk.Menu(tmenu,tearoff=0)
    tmenu.add_cascade(label='Index',menu=indmen)
    indmen.add_command(label='Make Index',command=lambda c=c: viewIndex(c))
    indmen.add_command(label='Make Regex Index',command=lambda c=c: regexViewIndex(c))
    try:
        import reportlab
        tmenu.add_command(label='Convert To PDF',command=lambda c=c: doPDFConversion(c))
    except Exception:
        g.es("no reportlab")
#@nonl
#@-node:mork.20040926105355.41:makeTabMenu
#@+node:mork.20040930091319.1:function factories
#@+node:mork.20040928224349:getAddChapter
def getAddChapter (c,notebook):

    '''A function that makes a function to add chapters.'''

    def ac (c=c):
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing
        cname = notebook.getcurselection()
        addPage(c)
        renumber(notebook)

    return ac
#@-node:mork.20040928224349:getAddChapter
#@+node:mork.20040928223221:getRemove
def getRemove (notebook,c,rmenu):
    
    '''A function that makes a function to remove chapters.'''

    def remove ():
        rmenu.delete(0,Tk.END)
        pn = notebook.pagenames()
        for i, z in enumerate(pn):
            i += 1
            #@            << define rmz callback >>
            #@+node:ekr.20060212130134:<< define rmz callback >>
            def rmz (name=z):
                if len(notebook.pagenames()) == 1: return
                sv = getSV(c,name)
                chapter = chapters [sv]
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
                notebook.delete(name)
                if tree != otree:
                    c.selectPosition(cvnd)
                if tree == otree:
                    pnames = notebook.pagenames()
                    notebook.selectpage(pnames[0])
                    c.selectPosition(c.currentPosition())
                    c.redraw()
                renumber(notebook)
            #@nonl
            #@-node:ekr.20060212130134:<< define rmz callback >>
            #@nl
            rmenu.add_command(label=str(i),command=rmz)

    return remove
#@nonl
#@-node:mork.20040928223221:getRemove
#@+node:mork.20040928223738:getRename
def getRename (c,notebook):

    '''A function that makes a function to rename chapters.'''

    def rename (rnframes={}):
        name = notebook.getcurselection()
        frame = notebook.page(notebook.index(name))
        fr = frames [c]
        if not rnframes.has_key(frame):
            f = rnframes [frame] = Tk.Frame(frame)
            e = Tk.Entry(f,background='white',textvariable=frame.sv)
            b = Tk.Button(f,text="Close")
            e.pack(side='left')
            b.pack(side='right')
            def change ():
                f.pack_forget()
            b.configure(command=change)
        else:
            f = rnframes [frame]
            if f.winfo_viewable(): return None
        fr.canvas.pack_forget()
        f.pack(side='bottom')
        fr.canvas.pack(fill='both',expand=1)

    return rename
#@nonl
#@-node:mork.20040928223738:getRename
#@+node:mork.20040928224049:getMakeTrash
def getMakeTrash (notebook):
    
    '''A function that makes a function to add a trash chapters.'''

    def mkTrash (c):
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing
        addPage(c,'Trash')
        pnames = notebook.pagenames()
        sv = getSV(c,pnames[-1])
        sv.set('Trash')
        renumber(notebook)

    return mkTrash
#@-node:mork.20040928224049:getMakeTrash
#@+node:mork.20040928224621:getSetupMenu
def getSetupMenu (c,notebook):

    '''A function that makes a function to populate a menu.'''

    def setupMenu (menu,command,all=False):
        menu.delete(0,Tk.END)
        current = notebook.getcurselection()
        for i, z in enumerate(notebook.pagenames()):
            i = i + 1
            if z == current and not all: continue
            menu.add_command(label=str(i),command=lambda c=c,name=z: command(c,name))

    return setupMenu
#@nonl
#@-node:mork.20040928224621:getSetupMenu
#@-node:mork.20040930091319.1:function factories
#@-others
#@nonl
#@-node:mork.20040930091319:tab menu stuff
#@+node:mork.20040930092346:Multi-Editor stuff
#@+others
#@+node:mork.20040929104527:selectNodeForEditor
def selectNodeForEditor (c,body):

    '''Select the next node for the editor.'''

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
#@-node:mork.20040929104527:selectNodeForEditor
#@+node:mork.20040929105638:activateEditor
def activateEditor (body):

    'Activate an editor.' ''

    body.r.configure(text=body.lastPosition.headString())
    ip = body.lastPosition.t.insertSpot
    txt = body.lastPosition.bodyString()
    body.deleteAllText()
    body.insertAtEnd(txt)
    if ip: body.setInsertionPoint(ip)
    body.colorizer.colorize(body.lastPosition)
    body.bodyCtrl.update_idletasks()
#@nonl
#@-node:mork.20040929105638:activateEditor
#@+node:mork.20040926105355.36:removeEditor
def removeEditor (c):

    pbody = pbodies [c]
    if len(pbody.panes()) == 1: return None
    body = c.frame.body
    pbody.delete(body.editorName)
    pbody.updatelayout()
    panes = pbody.panes()
    twidgets [c.frame].remove(body)
    nBody = twidgets [c.frame] [0]
    nBody.bodyCtrl.focus_set()
    nBody.bodyCtrl.update_idletasks()

#@-node:mork.20040926105355.36:removeEditor
#@+node:mork.20040926105355.44:addHeading
def addHeading (pane):

    f = Tk.Frame(pane)
    f.pack(side='top')
    l = Tk.Label(f)
    l.pack(side='left')
    r = Tk.Label(f)
    r.pack(side='right')
    return l, r

#@-node:mork.20040926105355.44:addHeading
#@-others
#@nonl
#@-node:mork.20040930092346:Multi-Editor stuff
#@+node:mork.20040930090547:Indexing
#@+at
# Indexing is complementary to find, it provides a gui Index of nodes.  In 
# comparison to regular find which bounces you around the tree, you can 
# preview the node before you go to it.
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.3:viewIndex
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
    #@+node:ekr.20060212130454:<< define scTo callback >>
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
    #@-node:ekr.20060212130454:<< define scTo callback >>
    #@nl
    e.bind('<Key>',scTo)
    e.focus_set()
#@nonl
#@-node:mork.20040926105355.3:viewIndex
#@+node:mork.20040929121409:buildIndex
def buildIndex (nodes,c,can,tl,bal,tags):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    f = tkFont.Font()
    f.configure(size=-20)
    ltag = None
    for i, z in enumerate(nodes):
        tg = 'abc' + str(i)
        parent = z [1].parent()
        if parent: parent = parent.headString()
        else:
            parent = 'No Parent'
        sv = getSV(c,z[2])
        if sv.get(): sv = ' - ' + sv.get()
        else: sv = ''

        tab = notebook.tab(z[2])
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
        #@+node:ekr.20060212131649:<< def callbacks >>
        def goto (event,z=z,c=c,tl=tl):
            notebook = notebooks.get(c)
            if not notebook: return # For unit testing
            notebook.selectpage(z[2])
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
        #@-node:ekr.20060212131649:<< def callbacks >>
        #@nl
        can.tag_bind(tg,'<Button-1>',goto)
        can.tag_bind(tg,'<Enter>',colorRd,'+')
        can.tag_bind(tg,'<Leave>',colorBl,'+')
#@nonl
#@-node:mork.20040929121409:buildIndex
#@+node:mork.20040926105355.4:regexViewIndex
def regexViewIndex (c):

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
#@-node:mork.20040926105355.4:regexViewIndex
#@-others
#@-node:mork.20040930090547:Indexing
#@+node:mork.20040930094729:Chapter-Notebook ops
#@+others
#@+node:mork.20040926105355.5:renumber
def renumber (notebook):

    pagenames = notebook.pagenames()

    for i, z in enumerate(pagenames):
        i = i + 1
        tab = notebook.tab(z)
        tab.configure(text=str(i))

#@-node:mork.20040926105355.5:renumber
#@+node:mork.20040926105355.6:getGoodPage
def getGoodPage (event,body):

    global focusing
    c = body.c ; notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    body.frame.body = body
    body.frame.bodyCtrl = body.bodyCtrl
    if not hasattr(body,'lastChapter'):
        body.lastChapter = notebook.getcurselection()
    page = checkChapterValidity(body.lastChapter,c)
    if page != notebook.getcurselection():
        body.lastChapter = page
        notebook.selectpage(page)
    selectNodeForEditor(c,body)
    activateEditor(body)
#@nonl
#@-node:mork.20040926105355.6:getGoodPage
#@+node:mork.20040926105355.7:checkChapterValidity
def checkChapterValidity (name,c):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    try:
        notebook.index(name)
    except:
        return notebook.getcurselection()
    return name
#@-node:mork.20040926105355.7:checkChapterValidity
#@+node:mork.20040926105355.20:getSV
def getSV (c,name):

    '''return a Tk StrinVar that is a primary identifier.'''

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    index = notebook.index(name)
    page = notebook.page(index)
    return page.sv
#@-node:mork.20040926105355.20:getSV
#@+node:mork.20040926105355.27:setTree
def setTree (c,name,notebook):

    if not c or not c.exists:
        g.trace('c does not exist',color='red')
        return None
    pindex = notebook.index(name)
    page = notebook.page(pindex)
    if not hasattr(page,'sv'):
        g.trace('no sv attr for page',color='red')
        return None
    sv = page.sv
    chapter = chapters [sv]
    chapter.makeCurrent()
    frame = c.frame
    frame.body.lastChapter = name
    frame.body.lastPosition = chapter.cp
    frame.body.l.configure(textvariable=sv)
    tab = notebook.tab(pindex)
    tab.configure(background='grey',foreground='white')
    activateEditor(frame.body)
#@nonl
#@-node:mork.20040926105355.27:setTree
#@+node:mork.20040929084846:lowerPage
def lowerPage (name,notebook):

    '''Set a lowered tabs color.'''

    pindex = notebook.index(name)
    tab = notebook.tab(pindex)
    tab.configure(background='lightgrey',foreground='black')
#@nonl
#@-node:mork.20040929084846:lowerPage
#@+node:mork.20040926105355.40:walkChapters
def walkChapters (c,ignorelist=[],chapname=False):

    '''A generator that allows one to walk the chapters as one big tree.'''

    if not c or not c.exists: return
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    pagenames = notebook.pagenames()
    for z in pagenames:
        sv = getSV(c,z)
        chapter = chapters [sv]
        v = chapter.rp
        while v:
            if chapname:
                if v not in ignorelist: yield v, z
            else:
                if v not in ignorelist: yield v
            v = v.threadNext()
#@nonl
#@-node:mork.20040926105355.40:walkChapters
#@-others
#@nonl
#@-node:mork.20040930094729:Chapter-Notebook ops
#@+node:mork.20040930091035:opening and closing (to be moved into Leo's core?)
#@+at
# This category is for opening and closing of Leo files.  We need to decorate 
# and be tricky here, since a Chapters leo file is a zip file.  These 
# functions are easy to break in my experience. :)
#@-at
#@@c
#@+others
#@+node:mork.20040930091035.1:opening
#@+node:mork.20040926105355.28:newGetLeoFile
def newGetLeoFile (self,fileName,readAtFileNodesFlag=True,silent=False):

    global iscStringIO

    if iscStringIO:
        def dontSetReadOnly (self,name,value):
            if name not in ('read_only','tnodesDict'):
                self.__dict__ [name] = value
        self.read_only = False
        self.__class__.__setattr__ = dontSetReadOnly

    rt = old_getLeoFile(self,fileName,readAtFileNodesFlag,silent)
    if iscStringIO:
        del self.__class__.__setattr__

    return rt
#@nonl
#@-node:mork.20040926105355.28:newGetLeoFile
#@+node:mork.20040926105355.29:newOpen
def newOpen (self,file,fileName,readAtFileNodesFlag=True,silent=False):

    global iscStringIO, stringIOCommander
    c = self.c

    if zipfile.is_zipfile(fileName):
        iscStringIO = True
        stringIOCommander = c
        chapters = openChaptersFile(fileName)
        g.es(str(len(chapters))+" Chapters To Read",color='blue')
        insertChapters(chapters,c.frame,c)
        g.es("Finished Reading Chapters",color='blue')
        iscStringIO = False
        return True

    return old_open(self,file,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:mork.20040926105355.29:newOpen
#@+node:mork.20040926105355.9:openChaptersFile
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

#@-node:mork.20040926105355.9:openChaptersFile
#@+node:mork.20040926105355.8:insertChapters
def insertChapters (chapters,frame,c):

     notebook = notebooks.get(c)
     if not notebook: return # For unit testing
     pagenames = notebook.pagenames()
     for num, tup in enumerate(chapters):
            x, y = tup
            if num > 0:
                sv = addPage(c,x).sv
                notebook.nextpage()
                cselection = notebook.getcurselection()
            else:
                cselection = notebook.getcurselection()
                sv = getSV(c,cselection)
            sv.set(x)
            next = cselection
            setTree(c,next,notebook)
            frame.c.fileCommands.open(y,sv.get())
            if num == 0:
                flipto = cselection
     setTree(flipto,notebook,c)
     c.frame.canvas.update_idletasks()
#@nonl
#@-node:mork.20040926105355.8:insertChapters
#@-node:mork.20040930091035.1:opening
#@+node:mork.20040930091035.2:closing
#@+node:mork.20040926105355.30:newWrite_LEO_file
def newWrite_LEO_file (self,fileName,outlineOnlyFlag,singleChapter=False):

    c = self.c ; at = c.atFileCommands
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    print singleChapter,fileName

    pagenames = notebook.pagenames()
    if len(pagenames) > 1 and not singleChapter:
        chapList = []
        self.__class__.__setattr__ = getMakeStringIO(chapList)
        rv = writeChapters(self,fileName,pagenames,c,outlineOnlyFlag)
        if rv:
            zipChapters(fileName,pagenames,c,chapList)
        del self.__class__.__setattr__
    else:
        rv = old_write_Leo_file(self,fileName,outlineOnlyFlag)

    return rv
#@nonl
#@-node:mork.20040926105355.30:newWrite_LEO_file
#@+node:mork.20040929092231:getMakeStringIO
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
#@-node:mork.20040929092231:getMakeStringIO
#@+node:mork.20040929090525:writeChapters
def writeChapters (self,fileName,pagenames,c,outlineOnlyFlag):

    '''Writes Chapters to StringIO instances.'''

    for z in pagenames:
        sv = getSV(c,z)
        chapter = chapters [sv]
        chapter.setVariables()
        rv = old_write_Leo_file(self,fileName,outlineOnlyFlag)

    c.cChapter.setVariables()
    return rv
#@nonl
#@-node:mork.20040929090525:writeChapters
#@+node:mork.20040929090525.1:zipChapters
def zipChapters (fileName,pagenames,c,chapList):

    '''Writes StringIO instances to a zipped file.'''

    zf = zipfile.ZipFile(fileName,'w',zipfile.ZIP_DEFLATED)

    for x, fname in enumerate(pagenames):
        sv = getSV(c,fname)
        zif = zipfile.ZipInfo(str(x))
        zif.comment = sv.get()
        zif.compress_type = zipfile.ZIP_DEFLATED
        chapList [x].seek(0) ; g.trace(chapList[x])
        zf.writestr(zif,chapList[x].read())

    zf.close()
#@nonl
#@-node:mork.20040929090525.1:zipChapters
#@-node:mork.20040930091035.2:closing
#@-others
#@nonl
#@-node:mork.20040930091035:opening and closing (to be moved into Leo's core?)
#@+node:mork.20040930091624:decorated Leo functions
#@+at
# I prefer decorating Leo functions as opposed to patching them.  Patching 
# them leads to long term incompatibilites with Leo and the plugin.  Though 
# this happens anyway with code evolution/changes, this makes it worse.  Thats 
# my experience with it. :)
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.34:new_os_path_dirname
def new_os_path_dirname (path,encoding=None):

    global iscStringIO, stringIOCommander

    if iscStringIO:
        c = stringIOCommander
        return os.path.dirname(c.mFileName)
    else:
        global old_os_path_dirname
        return old_os_path_dirname(path,encoding)
#@nonl
#@-node:mork.20040926105355.34:new_os_path_dirname
#@+node:mork.20040926105355.45:newendEditLabel
def newEndEditLabel (self):

    c = self.c ; p = c.currentPosition() ; h = p.headString()

    if p and h and hasattr(c.frame.body,'r'):
         c.frame.body.r.configure(text=h)

    return old_editLabel(self)
#@nonl
#@-node:mork.20040926105355.45:newendEditLabel
#@+node:mork.20040926105355.52:newselect
def newSelect (self,p,updateBeadList=True):

    c = p.v.c ; h = p.headString()
    g.trace(h)

    self.frame.body.lastPosition = p
    return_val = old_select(self,p,updateBeadList)

    notebook = notebooks.get(c)
    if notebook: # May be None for unit testing.

        self.frame.body.lastChapter = notebook.getcurselection()

        if hasattr(p.c.frame.body,'r'):
            c.frame.body.r.configure(text=h)

    return return_val
#@nonl
#@-node:mork.20040926105355.52:newselect
#@+node:mork.20040926105355.49:newTrashDelete
def newDoDelete (self,newPosition):

    c = self.c ; notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    pagenames = notebook.pagenames()
    pagenames = [getSV(c,x).get().upper() for x in pagenames]
    nbnam = notebook.getcurselection()
    if nbnam != None:
        name = getSV(c,notebook.getcurselection()).get().upper()
    else: name = 'TRASH'
    tsh = 'TRASH'
    g.trace(name)
    if name != tsh and tsh in pagenames:
        index = pagenames.index(tsh)
        trchapter = chapters [getSV(c,index)]
        trashnode = trchapter.rp
        trchapter.setVariables()
        self.moveAfter(trashnode)
        c.cChapter.setVariables()
        c.selectPosition(newPosition)
        return self
    old_doDelete(newPosition) # .71
#@nonl
#@-node:mork.20040926105355.49:newTrashDelete
#@+node:mork.20040926105355.21:newCreateControl
def newCreateControl (self,frame,parentFrame):
    
    c = self.c ; notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    if c not in pbodies:
        parentFrame = createPanedWidget(parentFrame,c)
    pbody = pbodies [c]
    l, r = addHeading(parentFrame)
    ctrl = old_createControl(self,frame,parentFrame)
    ctrl.bind("<FocusIn>",lambda event,body=frame.body: getGoodPage(event,body),'+')
    i = 1.0 / len(pbody.panes())
    for z in pbody.panes():
        pbody.configurepane(z,size=i)
    pbody.updatelayout()
    frame.body.l = l
    frame.body.r = r
    frame.body.editorName = editorNames [parentFrame]
    if frame not in twidgets:
        twidgets [frame] = []
    twidgets [frame].append(frame.body)
    l.configure(textvariable=getSV(c,notebook.getcurselection()))
    return ctrl
#@nonl
#@-node:mork.20040926105355.21:newCreateControl
#@+node:mork.20040926105355.28:newGetLeoFile
def newGetLeoFile (self,fileName,readAtFileNodesFlag=True,silent=False):

    global iscStringIO

    if iscStringIO:
        def dontSetReadOnly (self,name,value):
            if name not in ('read_only','tnodesDict'):
                self.__dict__ [name] = value
        self.read_only = False
        self.__class__.__setattr__ = dontSetReadOnly

    rt = old_getLeoFile(self,fileName,readAtFileNodesFlag,silent)
    if iscStringIO:
        del self.__class__.__setattr__

    return rt
#@nonl
#@-node:mork.20040926105355.28:newGetLeoFile
#@+node:mork.20040926105355.29:newOpen
def newOpen (self,file,fileName,readAtFileNodesFlag=True,silent=False):

    global iscStringIO, stringIOCommander
    c = self.c

    if zipfile.is_zipfile(fileName):
        iscStringIO = True
        stringIOCommander = c
        chapters = openChaptersFile(fileName)
        g.es(str(len(chapters))+" Chapters To Read",color='blue')
        insertChapters(chapters,c.frame,c)
        g.es("Finished Reading Chapters",color='blue')
        iscStringIO = False
        return True

    return old_open(self,file,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:mork.20040926105355.29:newOpen
#@+node:mork.20040926105355.24:newTreeinit
def newTreeinit (self,c,frame,canvas):

    sv = getSV(c,canvas.name)
    
    global old_tree_init
    old_tree_init(self,c,frame,canvas)

    self.chapter = chapters [sv] = Chapter(c,self,frame,canvas)
#@nonl
#@-node:mork.20040926105355.24:newTreeinit
#@-others
#@nonl
#@-node:mork.20040930091624:decorated Leo functions
#@+node:mork.20040930091759:operation( node ) to Chapter
#@+others
#@+node:mork.20040926105355.31:cloneToChapter
def cloneToChapter (c,name):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    page = notebook.page(notebook.index(name))
    c.beginUpdate()
    try:
        clone = vnd.clone(c.currentPosition())
        global chapters
        chapter = chapters [page.sv]
        p = chapter.cp
        clone.unlink()
        clone.linkAfter(p)
    finally:
        c.endUpdate()
#@nonl
#@-node:mork.20040926105355.31:cloneToChapter
#@+node:mork.20040926105355.32:moveToChapter
def moveToChapter (c,name):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    page = notebook.page(notebook.index(name))
    mvChapter = chapters [page.sv]
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
#@-node:mork.20040926105355.32:moveToChapter
#@+node:mork.20040926105355.33:copyToChapter
def copyToChapter (c,name):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    page = notebook.page(notebook.index(name))
    cpChapter = chapters [page.sv]
    c.beginUpdate()
    s = c.fileCommands.putLeoOutline()
    v = c.fileCommands.getLeoOutline(s)
    cpChapter.setVariables()
    mvnd = cpChapter.cp
    v.moveAfter(mvnd)
    c.cChapter.setVariables()
    c.endUpdate()

#@-node:mork.20040926105355.33:copyToChapter
#@+node:mork.20040926105355.39:makeNodeIntoChapter
def makeNodeIntoChapter (c,vnd=None):

    renum = vnd
    if vnd == None:
        vnd = c.currentPosition()
    if vnd == c.rootPosition() and vnd.next() == None:
        return
    nxt = vnd.next()
    if nxt:
        vnd.doDelete(nxt)

    page = addPage(c)
    mnChapter = chapters [page.sv]
    c.beginUpdate()
    oChapter = c.cChapter
    mnChapter.makeCurrent()
    root = mnChapter.rp
    vnd.moveAfter(root)
    c.setRootPosition(vnd)
    oChapter.makeCurrent()
    c.endUpdate()
    if not renum:
        notebook = notebooks.get(c)
        if notebook: # For unit testing
            renumber(notebook)
    c.selectPosition(oChapter.rp)
#@nonl
#@-node:mork.20040926105355.39:makeNodeIntoChapter
#@+node:mork.20040926105355.30:newWrite_LEO_file
def newWrite_LEO_file (self,fileName,outlineOnlyFlag,singleChapter=False):

    c = self.c ; at = c.atFileCommands
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    pagenames = notebook.pagenames()
    if len(pagenames) > 1 and not singleChapter:
        chapList = []
        self.__class__.__setattr__ = getMakeStringIO(chapList)
        rv = writeChapters(self,fileName,pagenames,c,outlineOnlyFlag)
        if rv:
            zipChapters(fileName,pagenames,c,chapList)
        del self.__class__.__setattr__
    else:
        rv = old_write_Leo_file(self,fileName,outlineOnlyFlag)

    return rv
#@nonl
#@-node:mork.20040926105355.30:newWrite_LEO_file
#@-others
#@nonl
#@-node:mork.20040930091759:operation( node ) to Chapter
#@+node:mork.20040930092027:conversions
#@+others
#@+node:mork.20040926105355.37:conversionToSimple
def conversionToSimple (c):
    
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    vnd = c.rootPosition()
    while 1:
        n = vnd.next()
        if n == None:
            break
        else:
            vnd = n
    pagenames = notebook.pagenames()
    current = notebook.getcurselection()
    pagenames.remove(current)
    c.beginUpdate()
    for z in pagenames:
        index = notebook.index(z)
        page = notebook.page(index)
        chapter = chapters [page.sv]
        rvNode = chapter.rp
        while 1:
            nxt = rvNode.next()
            rvNode.moveAfter(vnd)
            if nxt: rvNode = nxt
            else:
                vnd = rvNode
                break
        notebook.delete(z)
    c.endUpdate()
    renumber(notebook)
#@nonl
#@-node:mork.20040926105355.37:conversionToSimple
#@+node:mork.20040926105355.38:conversionToChapters
def conversionToChapters (c):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    vnd = c.rootPosition()
    while 1:
        nxt = vnd.next()
        if nxt:
            makeNodeIntoChapter(c,nxt)
        else:
            break
    setTree(notebook.pagenames()[0],notebook,c)
#@-node:mork.20040926105355.38:conversionToChapters
#@-others
#@nonl
#@-node:mork.20040930092027:conversions
#@+node:mork.20040930092027.1:import/export
#@+at
# Import a Leo file as a Chapter(s).  Export a Chapter as a single Leo file.  
# Kinda handy.
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.47:importLeoFile
def importLeoFile( c ):

    name = tkFileDialog.askopenfilename()
    if name:
        page = addPage( c , name )
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing       
        notebook.selectpage( notebook.pagenames()[ - 1 ] )
        c.fileCommands.open( file( name, 'r' ), name )
        c.cChapter.makeCurrent()
        renumber( notebook )
#@-node:mork.20040926105355.47:importLeoFile
#@+node:mork.20040926105355.48:exportLeoFile
def exportLeoFile (c):

    name = tkFileDialog.asksaveasfilename()
    if name:
        if not name.endswith('.leo'):
            name += '.leo'
        c.fileCommands.write_LEO_file(name,False,singleChapter=True)
#@-node:mork.20040926105355.48:exportLeoFile
#@-others
#@nonl
#@-node:mork.20040930092027.1:import/export
#@+node:mork.20040930092207:functions without classification
#@+node:mork.20040926105355.46:swapChapters
def swapChapters (c,name):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

    cselection = notebook.getcurselection()
    tab1 = notebook.tab(cselection)
    tab2 = notebook.tab(name)
    tval1 = tab1.cget('text')
    tval2 = tab2.cget('text')
    tv1 = getSV(c,cselection)
    tv2 = getSV(c,name)
    chap1 = c.cChapter
    chap2 = chapters [tv2]
    rp, tp, cp = chap2.rp, chap2.tp, chap2.cp
    chap2.rp, chap2.tp, chap2.cp = chap1.rp, chap1.tp, chap1.cp
    chap1.rp, chap1.tp, chap1.cp = rp, tp, cp
    chap1.setVariables()
    c.redraw()
    chap1.canvas.update_idletasks()

    val1 = tv1.get()
    val2 = tv2.get()
    if val2.isdigit():
        tv1.set(notebook.index(cselection)+1)
    else: tv1.set(val2)
    if val1.isdigit():
        tv2.set(notebook.index(name)+1)
    else: tv2.set(val1)


#@-node:mork.20040926105355.46:swapChapters
#@+node:mork.20040926105355.50:emptyTrash
def emptyTrash (notebook,c):

    pagenames = notebook.pagenames()
    pagenames = [getSV(c,x) for x in pagenames]
    for z in pagenames:
        if z.get().upper() == 'TRASH':
            trChapter = chapters [z]
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
#@-node:mork.20040926105355.50:emptyTrash
#@+node:mork.20040926105355.51:regexClone
def regexClone (c,name):
    if not c or not c.exists: return
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    sv = getSV(c,name)
    chapter = chapters [sv]
    #@    << define cloneWalk callback >>
    #@+node:ekr.20060212131649.1:<< define cloneWalk callback >>
    def cloneWalk (result,entry,widget,c=c):
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
        notebook.selectpage(name)
        c.selectPosition(snode)
        snode.expand()
        c.beginUpdate()
        c.endUpdate()
    #@nonl
    #@-node:ekr.20060212131649.1:<< define cloneWalk callback >>
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
#@-node:mork.20040926105355.51:regexClone
#@-node:mork.20040930092207:functions without classification
#@+node:mork.20040930091624.1:PDF
# Requires reportlab toolkit at http://www.reportlab.org

#@+others
#@+node:mork.20040926105355.42:doPDFConversion
def doPDFConversion (c):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing

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
    pagenames = notebook.pagenames()
    cChapter = c.cChapter
    for n, z in enumerate(pagenames):

        n = n + 1
        sv = getSV(c,z)
        chapter = chapters [sv]
        chapter.setVariables()
        p = chapter.rp
        if p:
            _changeTreeToPDF(sv.get(),n,p,c,Story,styles,maxlen)
    #@    << define otherPages callback >>
    #@+node:ekr.20041109120739:<< define otherPages callback >>
    def otherPages( canvas, doc , pageinfo = pinfo):
    
        canvas.saveState()
        canvas.setFont('Times-Roman',9) 
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo)) 
        canvas.restoreState()
    #@nonl
    #@-node:ekr.20041109120739:<< define otherPages callback >>
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
#@-node:mork.20040926105355.42:doPDFConversion
#@+node:mork.20040926105355.43:_changeTreeToPDF
def _changeTreeToPDF (name,num,p,c,Story,styles,maxlen):

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, XPreformatted
    from reportlab.lib.units import inch
    from reportlab.rl_config import defaultPageSize
    enc = c.importCommands.encoding
    hstyle = styles ['title']
    Story.append(Paragraph('Chapter %s: %s' % (num,name),hstyle))
    style = styles ['Normal']
    for v in p.allNodes_iter():
        head = v.moreHead(0)
        head = g.toEncodedString(head,enc,reportErrors=True)
        s = head + '\n'
        body = v.moreBody() # Inserts escapes.
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
#@-node:mork.20040926105355.43:_changeTreeToPDF
#@-others
#@nonl
#@-node:mork.20040930091624.1:PDF
#@-others
#@-node:mork.20040926105355.1:@thin chapters.py
#@-leo
