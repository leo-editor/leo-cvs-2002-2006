#@+leo-ver=4-thin
#@+node:mork.20040926105355.1:@thin chapters.py
#@<<docstring>>
#@+node:ekr.20041109123143:<<docstring>>
'''This plugin creates separate outlines called "chapters" within a single .leo file.  Clones work between Chapters.

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

#@@language python
#@@tabwidth -4

__version__ = "0.68"
#@<< version history >>
#@+node:ekr.20041103051117:<< version history >>
#@@killcolor
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

import os
import string
import sys
import time
import zipfile
#@nonl
#@-node:ekr.20041103050629:<< imports >>
#@nl
#@<< globals >>
#@+node:mork.20040926105355.2:<< globals >>
chapters = {}
notebooks = {}
frames = {}
iscStringIO = False
twidgets = {}
pbodies = {}

#@-node:mork.20040926105355.2:<< globals >>
#@nl

# Solve problems with string.atoi...
import string
string.atoi = int

#@+others
#@+node:mork.20040927092626:class Chapter
class Chapter:
    '''The fundamental abstraction in the Chapters plugin.
       It enables the tracking of Chapters tree information.'''
       
    #@    @+others
    #@+node:ekr.20041103051228:__init__
    def __init__( self, c, tree, frame, canvas ):
            
        self.c = c
        self.tree = tree
        self.frame = frame
        self.canvas = canvas
        self.treeBar = frame.treeBar
    
        if hasattr( c, 'cChapter' ):
            tn = leoNodes.tnode( '', 'New Headline' )
            vn = leoNodes.vnode( c, tn )
            pos = leoNodes.position( vn, [] )
            self.cp = pos.copy()
            self.rp = pos.copy()
            self.tp = pos.copy()
        else:
            c.cChapter = self
            self.cp = c._currentPosition or c.nullPosition()
            self.tp = c._topPosition or c.nullPosition()
            self.rp = c._rootPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20041103051228:__init__
    #@+node:ekr.20041103051228.1:_saveInfo
    def _saveInfo( self ):
        
        c = self.c
    
        self.cp = c._currentPosition or c.nullPosition()
        self.rp = c._rootPosition or c.nullPosition()
        self.tp = c._topPosition or c.nullPosition()
    #@nonl
    #@-node:ekr.20041103051228.1:_saveInfo
    #@+node:ekr.20041103051228.2:setVariables
    def setVariables( self ):
        
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
    def makeCurrent( self ):
        
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
#@+at
# This category deals with creating widgets and any support functions for 
# doing so.
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.21:newCreateControl
cControl = leoTkinterFrame.leoTkinterBody.createControl

def newCreateControl( self, frame, parentFrame  ):
    c = self.c
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    if c not in pbodies:
        parentFrame = createPanedWidget( parentFrame, c )
    pbody = pbodies[ c ]
    l, r =addHeading( parentFrame )
    ctrl = cControl( self, frame , parentFrame ) 
    ctrl.bind( "<FocusIn>", lambda event, body = frame.body : getGoodPage( event, body ), '+' )
    i = 1.0 / len( pbody.panes() )
    for z in pbody.panes():
        pbody.configurepane( z , size = i )
    pbody.updatelayout()
    frame.body.l =l
    frame.body.r =r 
    frame.body.editorName = editorNames[ parentFrame ]
    if frame not in twidgets:
        twidgets[ frame ] = []
    twidgets[ frame ].append( frame.body )
    l.configure( textvariable = getSV( notebook.getcurselection(), c ) )
    return ctrl
#@-node:mork.20040926105355.21:newCreateControl
#@+node:mork.20040929110556:createPanedWidget
def createPanedWidget( parentFrame, c ):
    #constructs a new panedwidget for a frame
    pbody = Pmw.PanedWidget( parentFrame , orient = 'horizontal' )
    pbody.pack( expand = 1 , fill = 'both')
    pbodies[ c ] = pbody
    parentFrame = newEditorPane( c )
    return parentFrame
#@nonl
#@-node:mork.20040929110556:createPanedWidget
#@+node:mork.20040926105355.22:newEditorPane
editorNames = {}

def newEditorPane( c ):
    names = pbodies[ c ].panes()
    if names:
        name  = str( int(names[ -1 ]) + 1 )
    else:
        name = '1'
    zpane = pbodies[ c ].add( name )
    editorNames[ zpane ] = name
    return zpane
#@-node:mork.20040926105355.22:newEditorPane
#@+node:mork.20040926105355.23:newCreateCanvas
def newCreateCanvas( self, parentFrame, createCanvas = leoTkinterFrame.leoTkinterFrame.createCanvas ):
    c = self.c
    
    if c not in frames:
        frames[ c ] = self
        notebook = createNoteBook( c, parentFrame )
    else:
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing
        
    pname = notebook.nameMaker.next()
    page = notebook.add( pname )
    indx = notebook.index( pname )
    tab = notebook.tab( indx )
    if indx == 0:
        tab.configure( background = 'grey', foreground = 'white' )
    canvas = createCanvas( self, page )
    
    hull = notebook.component( 'hull' )
    tab.bind( '<Button-3>' , lambda event : hull.tmenu.post( event.x_root , event.y_root ) )
    sv = Tk.StringVar()
    page.sv = sv
    createBalloon( tab, sv )
    canvas.name = pname
    
    # g.trace(repr(canvas.name),canvas)

    return canvas
#@nonl
#@-node:mork.20040926105355.23:newCreateCanvas
#@+node:mork.20040929120442:createBalloon
def createBalloon( tab, sv ):
    #creates a balloon for a widget
    balloon = Pmw.Balloon( tab , initwait = 100 )
    balloon.bind( tab , '' )
    hull = balloon.component( 'hull' )
    def blockExpose( event ):
        if sv.get() == '':
             hull.withdraw()
    hull.bind( '<Expose>', blockExpose, '+' )
    balloon._label.configure( textvariable = sv )
#@nonl
#@-node:mork.20040929120442:createBalloon
#@+node:mork.20040929102107:createNoteBook
def createNoteBook( c, parentFrame ):
    #constructs a NoteBook widget for a frame
    notebooks[ c ] = notebook = Pmw.NoteBook( parentFrame, borderwidth = 1, pagemargin = 0)
    hull = notebook.component( 'hull' ) 
    makeTabMenu( hull, notebook, c )
    notebook.configure( raisecommand = lambda name, notebook = notebook : setTree( name , notebook ) )
    notebook.configure( lowercommand = lambda name, notebook = notebook: lowerPage( name, notebook ) )
    notebook.pack( fill = 'both' , expand = 1)
    notebook.nameMaker = getNameMaker( notebook )
    return notebook
#@nonl
#@-node:mork.20040929102107:createNoteBook
#@+node:mork.20040929093051:getNameMaker
def getNameMaker( notebook ):
    #creates a numbering mechanism for tabs
    def nameMaker():
        i = 0
        while 1:
            if len( notebook.pagenames() ) == 0: i = 0
            i += 1
            yield str( i )
            
    return nameMaker()
#@nonl
#@-node:mork.20040929093051:getNameMaker
#@+node:mork.20040926105355.24:newTreeinit
def newTreeinit( self, c,frame,canvas, oinit = leoTkinterTree.leoTkinterTree.__init__ ):
    
    # g.trace(canvas)

    sv = getSV( canvas.name, c )
    oinit( self, c, frame, canvas )
    self.chapter = chapters[ sv ] = Chapter( c, self , frame, canvas )
#@-node:mork.20040926105355.24:newTreeinit
#@+node:mork.20040926105355.25:constructTree
def constructTree( frame , notebook, name ):
    
    canvas = treeBar = tree = None
    if frame.canvas:
        canvas = frame.canvas
        treeBar = frame.treeBar
        tree = frame.tree
    sv = Tk.StringVar()
    sv.set( name )
    canvas = frame.createCanvas( None )
    frame.canvas =  canvas
    frame.tree = leoTkinterTree.leoTkinterTree( frame.c ,frame, frame.canvas)
    frame.tree.setColorFromConfig()
    indx = notebook.index( notebook.pagenames()[ -1 ] )
    tab = notebook.tab( indx )
    tnum = str( len( notebook.pagenames() ) ) 
    tab.configure( text = tnum )
    hull = notebook.component( 'hull' )
    tab.bind( '<Button-3>' , lambda event ,hull = hull: hull.tmenu.post( event.x_root , event.y_root ) )
    return tree , notebook.page( notebook.pagenames()[ - 1 ] )
#@-node:mork.20040926105355.25:constructTree
#@+node:mork.20040926105355.26:addPage
def addPage( c , name = None ):

    frame = frames[ c ]
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    if name == None : name = str( len( notebook.pagenames() ) + 1 )
    o_chapter = c.cChapter
    otree, page  = constructTree( frame, notebook, name )
    c.cChapter.makeCurrent()
    o_chapter.makeCurrent()
    return page
#@-node:mork.20040926105355.26:addPage
#@+node:mork.20040926105355.35:newEditor
def newEditor( c ):
    
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    frame = frames[ c ]
    pbody = pbodies[ c ]
    zpane = newEditorPane( c )
    af = leoTkinterBody( frame, zpane )
    c.frame.bodyCtrl = af.bodyCtrl
    af.setFontFromConfig()
    af.createBindings( frame )
    af.bodyCtrl.focus_set()
    cname = notebook.getcurselection()
    af.l.configure( textvariable = getSV(cname , c ) )
    af.r.configure( text = c.currentVnode().headString() )

#@-node:mork.20040926105355.35:newEditor
#@-others
#@nonl
#@-node:mork.20040930090735:Creating widgets...
#@+node:mork.20040930091319:tab menu stuff
#@+at
# Tab menu and factory functions for the tab menu creation process.
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.41:makeTabMenu
def makeTabMenu( widget, notebook, c ):
    #creates the Menu that appears
    tmenu = Tk.Menu( widget, tearoff = 0 )
    widget.bind( '<Button-3>' , lambda event : tmenu.post( event.x_root , event.y_root ) )
    widget.tmenu = tmenu
    tmenu.add_command( command = tmenu.unpost )
    tmenu.add_separator()
    ac = getAddChapter( c, notebook )
    tmenu.add_command( label = 'Add Chapter', command = ac )
    rmenu = Tk.Menu( tmenu , tearoff = 0 )    
    remove = getRemove( notebook, c, rmenu )
    rmenu.configure( postcommand = remove )        
    tmenu.add_cascade( menu = rmenu, label = "Remove Chapter" )
    rename = getRename( notebook )
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
    opmenu.add_command( label ="Make Node Into Chapter", command = lambda c=c:  makeNodeIntoChapter( c ) )
    mkTrash = getMakeTrash( notebook )
    opmenu.add_command( label = "Add Trash Barrel", command =
    lambda c = c : mkTrash( c ))
    opmenu.add_command( label = 'Empty Trash Barrel', command =
    lambda notebook = notebooks.get(c), c = c: emptyTrash( notebook, c ) )
    setupMenu = getSetupMenu( c, notebook )
    cmenu.configure(
        postcommand = lambda menu = cmenu, command = cloneToChapter : setupMenu( menu, command ) )
    movmenu.configure(
        postcommand = lambda menu = movmenu, command = moveToChapter : setupMenu( menu, command ) )
    copymenu.configure(
        postcommand = lambda menu = copymenu, command = copyToChapter : setupMenu( menu, command ) ) 
    swapmenu.configure( postcommand = 
    lambda menu = swapmenu, command = swapChapters : setupMenu( menu, command ) )
    searchmenu.configure( postcommand = lambda menu = searchmenu,
    command = regexClone: setupMenu( menu, command, all = True ) )
    edmenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( label = "Editor", menu = edmenu )
    edmenu.add_command( label = "Add Editor" , command = lambda c =c : newEditor( c ) ) 
    edmenu.add_command( label = "Remove Editor", command = lambda c = c : removeEditor( c ) )
    conmenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( menu = conmenu, label = 'Conversion' )
    conmenu.add_command(
        label = "Convert To Simple Outline",
        command = lambda c =c : conversionToSimple( c ) )
    conmenu.add_command(
        label = "Convert Simple Outline into Chapters",
        command = lambda c= c : conversionToChapters( c ) )
    iemenu = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade(label = 'Import/Export', menu = iemenu )
    iemenu.add_command( label = "Import Leo File ", command = lambda c = c: importLeoFile(c ) )
    iemenu.add_command( label = "Export Chapter To Leo File", command = lambda c =c : exportLeoFile( c ) )
    indmen = Tk.Menu( tmenu, tearoff = 0 )
    tmenu.add_cascade( label = 'Index', menu = indmen )
    indmen.add_command( label = 'Make Index', command = lambda c =c : viewIndex( c ) )
    indmen.add_command( label = 'Make Regex Index', command = lambda c =c : regexViewIndex( c ) ) 
    try:
        import reportlab
        tmenu.add_command( label = 'Convert To PDF', command = lambda c = c: doPDFConversion( c ) )
    except Exception: 
        g.es( "no reportlab" )
#@nonl
#@-node:mork.20040926105355.41:makeTabMenu
#@+node:mork.20040930091319.1:function factories
#@+others
#@+node:mork.20040928224349:getAddChapter
def getAddChapter( c , notebook ):
    #a function that makes a function to add chapters  
    def ac( c = c ):
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing
        cname = notebook.getcurselection()
        addPage( c )        
        renumber( notebook)
    
    return ac
#@nonl
#@-node:mork.20040928224349:getAddChapter
#@+node:mork.20040928223221:getRemove
def getRemove( notebook, c , rmenu ):
    #a function that makes a function to remove chapters
    def remove():
        rmenu.delete( 0 , Tk.END )
        pn = notebook.pagenames()
        for i, z in enumerate( pn ):
            i = i + 1
            def rmz( name = z):
                if len( notebook.pagenames() ) == 1: return
                sv = getSV( name )
                chapter = chapters[ sv ]
                tree = chapter.tree
                vnd = chapter.rp
                cvnd = c.cChapter.cp
                c.beginUpdate()
                otree = c.cChapter.tree
                c.frame.tree = tree
                if vnd:
                    v = vnd                    
                    nnd = vnd.next()
                    if nnd == None:
                        nnd = vnd.insertAfter()
                        vnd = None
                    v.doDelete( nnd )
                c.frame.tree = otree
                c.endUpdate()
                notebook.delete( name )
                if tree != otree:
                    c.selectPosition( cvnd )
                if tree == otree:
                    pnames = notebook.pagenames()
                    notebook.selectpage( pnames[ 0 ] )
                    c.selectPosition( c.currentPosition() )
                    c.beginUpdate()
                    c.endUpdate()
                renumber( notebook )
            rmenu.add_command( label = str( i ) , command = rmz )  
              
    return remove
#@-node:mork.20040928223221:getRemove
#@+node:mork.20040928223738:getRename
def getRename( notebook ):
    #a function that makes a function to rename chapters
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

    return rename
#@nonl
#@-node:mork.20040928223738:getRename
#@+node:mork.20040928224049:getMakeTrash
def getMakeTrash( notebook ):
    #a function that makes a function to add a trash chapters
    def mkTrash( c ):
        notebook = notebooks.get(c)
        if not notebook: return # For unit testing
        addPage( c, 'Trash' )
        pnames = notebook.pagenames()
        sv = getSV( pnames[ - 1 ], c )
        sv.set( 'Trash' )
        renumber( notebook )
    
    return mkTrash    
#@-node:mork.20040928224049:getMakeTrash
#@+node:mork.20040928224621:getSetupMenu
def getSetupMenu( c, notebook ):
    #a function that makes a function to populate a menu
    def setupMenu( menu , command , all = False):
        menu.delete( 0 , Tk.END )
        current = notebook.getcurselection()
        for i, z in  enumerate( notebook.pagenames() ):
            i = i + 1
            if z == current and not all: continue
            menu.add_command( label = str( i ) , command = lambda c = c , name = z : command( c, name ) )
            
    return setupMenu
#@nonl
#@-node:mork.20040928224621:getSetupMenu
#@-others
#@nonl
#@-node:mork.20040930091319.1:function factories
#@-others
#@nonl
#@-node:mork.20040930091319:tab menu stuff
#@+node:mork.20040930092346:Multi-Editor stuff
#@+others
#@+node:mork.20040929104527:selectNodeForEditor
def selectNodeForEditor( c, body ):
    #sets the node for the new editor
    if not hasattr( body, 'lastNode' ):
        body.lastNode = c.currentPosition()

    if body.lastNode == c.currentPosition(): return    
    elif body.lastNode.exists( c ):
        c.selectPosition( body.lastNode )
    else:
        c.selectPosition( c.rootPosition() )

    body.lastNode = c.currentPosition()    
#@nonl
#@-node:mork.20040929104527:selectNodeForEditor
#@+node:mork.20040929105638:activateEditor
def activateEditor( body ):
    #performs functions that brings editor on line
    body.r.configure( text = body.lastNode.headString() )
    ip = body.lastNode.t.insertSpot
    txt = body.lastNode.bodyString()
    body.deleteAllText()
    body.insertAtEnd( txt )
    if ip : body.setInsertionPoint( ip )
    body.colorizer.colorize( body.lastNode )
    body.bodyCtrl.update_idletasks()
#@nonl
#@-node:mork.20040929105638:activateEditor
#@+node:mork.20040926105355.36:removeEditor
def removeEditor( c ):
    pbody = pbodies[ c ]
    if len( pbody.panes() ) == 1: return None
    body = c.frame.body
    pbody.delete( body.editorName )
    pbody.updatelayout()
    panes = pbody.panes()
    twidgets[ c.frame ].remove( body )
    nBody = twidgets[ c.frame ][ 0 ] 
    nBody.bodyCtrl.focus_set()
    nBody.bodyCtrl.update_idletasks()
#@-node:mork.20040926105355.36:removeEditor
#@+node:mork.20040926105355.44:addHeading
def addHeading( pane ):
    f = Tk.Frame( pane )
    f.pack( side = 'top' )
    l = Tk.Label( f )
    l.pack( side = 'left' )
    r = Tk.Label( f )
    r.pack( side = 'right' )
    return l , r
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
def viewIndex( c , nodes = None, tle = '' ):
    if nodes == None:
        nodes = [ x for x in walkChapters( c, chapname = True ) ]
    def aN( a ):
        n = a[ 0 ].headString()
        return n, a[ 0 ], a[ 1 ]
    nodes = map( aN, nodes )
    nodes.sort()
    tl = Tk.Toplevel()
    import time    
    title = "%s Index of %s created at %s" % ( tle, c.frame.shortFileName(), time.ctime())
    tl.title( title )
    f = Tk.Frame( tl )
    f.pack( side = 'bottom' )
    l = Tk.Label( f, text = 'ScrollTo:' )
    e = Tk.Entry( f , bg = 'white', fg = 'blue')
    l.pack( side = 'left' )
    e.pack( side ='left' )
    b = Tk.Button( f, text = 'Close' )
    b.pack( side = 'left' )
    def rm( tl = tl ):
        tl.withdraw()
        tl.destroy()
    b.configure( command = rm )
    sve = Tk.StringVar()
    e.configure( textvariable = sve )
    ms = tl.maxsize()
    tl.geometry( '%sx%s+0+0' % (ms[ 0 ], (ms[ 1 ]/4 )*3 ))
    sc = Pmw.ScrolledCanvas( tl , vscrollmode = 'static', hscrollmode = 'static', 
    usehullsize = 1, borderframe = 1, hull_width = ms[ 0 ], hull_height = (ms[ 1 ]/4 )*3 )
    sc.pack()
    can = sc.interior()
    can.configure( background = 'white' )
    bal = Pmw.Balloon( can )
    
    tags = {}
    #ltag = None
    buildIndex( nodes , c, can, tl, bal, tags)            
    sc.resizescrollregion()
    def scTo( event , nodes = nodes, sve = sve , can = can , tags = tags):
        t = sve.get()
        if event.keysym == 'BackSpace':
            t = t[ : -1 ]
        else:
            t = t + event.char
        if t == '': return
        for z in nodes:
            if z[ 0 ].startswith( t ) and tags.has_key( z[ 1 ] ):
                tg = tags[ z[ 1 ] ]
                eh = can.bbox( ltag )[ 1 ]
                eh = (eh *1.0)/100
                bh = can.bbox( tg )[ 1 ]
                ncor = (bh/ eh) * .01 
                can.yview( 'moveto' , ncor)
                return

    e.bind( '<Key>', scTo )
    e.focus_set()
#@-node:mork.20040926105355.3:viewIndex
#@+node:mork.20040929121409:buildIndex
def buildIndex( nodes , c , can, tl, bal, tags):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    import tkFont
    f = tkFont.Font()
    f.configure( size = -20 )
    ltag = None
    for i,z in enumerate(nodes):
        tg = 'abc' + str( i ) 
        parent = z[ 1 ].parent()
        if parent: parent = parent.headString()
        else:
            parent = 'No Parent'
        sv = getSV( z[ 2 ] )
        if sv.get(): sv = ' - ' + sv.get()
        else: sv = ''
        
        tab = notebook.tab( z[ 2 ] )
        tv = tab.cget( 'text' )
        isClone = z[ 1 ].isCloned()
        if isClone:
            clone = ' (Clone) '
        else:
            clone =''
        txt = '%s  , parent: %s , chapter: %s%s%s' %( z[ 0 ], parent, tv, sv, clone)
        ltag = tags[ z[1] ] = can.create_text( 20, i * 20 + 20, text = txt, fill = 'blue', font = f , anchor = Tk.W, tag = tg )
        bs = z[ 1 ].bodyString()
        if bs.strip() != '':
            bal.tagbind( can, tg, bs)
        def goto( event, z = z , c = c, tl = tl):
            notebook = notebooks.get(c)
            if not notebook: return # For unit testing
            notebook.selectpage( z[ 2 ] )
            c.selectVnode( z[ 1 ] )
            c.frame.outerFrame.update_idletasks()
            c.frame.outerFrame.event_generate( '<Button-1>' )
            c.frame.bringToFront()
            return 'break'
        def colorRd( event , tg = ltag , can = can ):
            can.itemconfig( tg, fill = 'red' )
        def colorBl( event , tg = ltag , can = can ):
            can.itemconfig( tg, fill = 'blue' )
        can.tag_bind( tg, '<Button-1>', goto )
        can.tag_bind( tg, '<Enter>', colorRd, '+' )
        can.tag_bind( tg, '<Leave>', colorBl, '+' )    
#@-node:mork.20040929121409:buildIndex
#@+node:mork.20040926105355.4:regexViewIndex
def regexViewIndex( c ):
    
    def regexWalk( result, entry, widget ):
        txt = entry.get()
        widget.deactivate()        
        widget.destroy()
        if result == 'Cancel': return None
        nodes = [ x for x in walkChapters( c, chapname = True ) ]
        import re
        regex = re.compile( txt )
        def search( nd, regex = regex ):
            return regex.search( nd[ 0 ].bodyString() )
        nodes = filter( search , nodes )
        viewIndex( c, nodes , 'Regex( %s )'%txt )
        return

    sd = Pmw.PromptDialog( c.frame.top,
    title = 'Regex Index',
    buttons = ( 'Search', 'Cancel' ),
    command =regexWalk )
    entry = sd.component( 'entry' )
    sd.configure( command = 
        lambda result, entry = entry, widget = sd:
            regexWalk( result, entry, widget ) )      
    sd.activate(  geometry = 'centerscreenalways' )   
#@-node:mork.20040926105355.4:regexViewIndex
#@-others
#@-node:mork.20040930090547:Indexing
#@+node:mork.20040930094729:Chapter-Notebook ops
#@+others
#@+node:mork.20040926105355.5:renumber
def renumber( notebook ):
    pagenames = notebook.pagenames()
    for i , z in enumerate(pagenames):
        i = i +1
        tab = notebook.tab( z )
        tab.configure( text = str( i ) )
#@-node:mork.20040926105355.5:renumber
#@+node:mork.20040926105355.6:getGoodPage
def getGoodPage( event , body ):
    global focusing
    c = body.c 
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    body.frame.body = body
    body.frame.bodyCtrl = body.bodyCtrl
    if not hasattr( body, 'lastChapter' ):
        body.lastChapter = notebook.getcurselection()
    page = checkChapterValidity( body.lastChapter, c )
    if page != notebook.getcurselection():
        body.lastChapter = page
        notebook.selectpage( page )
    selectNodeForEditor( c, body )         
    activateEditor( body )
#@nonl
#@-node:mork.20040926105355.6:getGoodPage
#@+node:mork.20040926105355.7:checkChapterValidity
def checkChapterValidity( name , c):
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    try:
        notebook.index( name )
    except:
        return notebook.getcurselection()            
    return name
#@-node:mork.20040926105355.7:checkChapterValidity
#@+node:mork.20040926105355.20:getSV
def getSV( name, c = None ):
    #returns a Tk StrinVar that is a primary identifier
    if not c : c = g.top()
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    index = notebook.index( name )
    page = notebook.page( index )
    return page.sv
#@-node:mork.20040926105355.20:getSV
#@+node:mork.20040926105355.27:setTree
def setTree( name , notebook , c = None ):

    if not c: 
        c = g.top()
        if not c: return None
    pindex = notebook.index( name )
    page = notebook.page( pindex )
    if not hasattr( page, 'sv' ) : return None
    sv = page.sv
    chapter = chapters[ sv ]
    chapter.makeCurrent()
    frame = c.frame
    frame.body.lastChapter = name
    frame.body.lastNode = chapter.cp
    frame.body.l.configure( textvariable = sv )
    tab = notebook.tab( pindex )
    tab.configure( background = 'grey', foreground = 'white' )
    activateEditor( frame.body )
#@-node:mork.20040926105355.27:setTree
#@+node:mork.20040929084846:lowerPage
def lowerPage( name, notebook):
    # a function that sets a lowered tabs color
    pindex = notebook.index( name )
    tab = notebook.tab( pindex )
    tab.configure( background = 'lightgrey', foreground = 'black' )
#@nonl
#@-node:mork.20040929084846:lowerPage
#@+node:mork.20040926105355.40:walkChapters
def walkChapters( c = None, ignorelist = [], chapname = False):
    # a generator that allows one to walk the chapters as one big tree
    if c == None : c = g.top()
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    pagenames = notebook.pagenames()
    for z in pagenames:
        sv = getSV( z , c)
        chapter = chapters[ sv ]
        v = chapter.rp
        while v:
            if chapname:
                if v not in ignorelist: yield v, z
            else:
                if v not in ignorelist:  yield v
            v = v.threadNext()
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
#@+others
#@+node:mork.20040926105355.28:newGetLeoFile
oldGetLeoFile =  leoFileCommands.fileCommands.getLeoFile

def newGetLeoFile(self, fileName,readAtFileNodesFlag=True,silent=False):
    if iscStringIO:
        def dontSetReadOnly( self, name, value ):
            if name == 'read_only': return
            elif name == 'tnodesDict': return
            else:
                self.__dict__[ name ] = value
        self.read_only = False
        self.__class__.__setattr__ = dontSetReadOnly
    rt = oldGetLeoFile(self,fileName,readAtFileNodesFlag,silent)
    if iscStringIO:
        del self.__class__.__setattr__       
    return rt
#@nonl
#@-node:mork.20040926105355.28:newGetLeoFile
#@+node:mork.20040926105355.29:newOpen
oldOpen = leoFileCommands.fileCommands.open

def newOpen( self,file,fileName,readAtFileNodesFlag=True,silent=False):

    global iscStringIO
    c = self.c
    
    if zipfile.is_zipfile( fileName ):
        iscStringIO = True
        chapters = openChaptersFile( fileName )
        g.es( str( len( chapters ) ) + " Chapters To Read", color = 'blue' )
        insertChapters( chapters, c.frame, c )
        g.es( "Finished Reading Chapters", color = 'blue' )
        iscStringIO = False
        return True

    return oldOpen(self,file,fileName,readAtFileNodesFlag,silent)
#@nonl
#@-node:mork.20040926105355.29:newOpen
#@+node:mork.20040926105355.9:openChaptersFile
def openChaptersFile( fileName ):
    zf = zipfile.ZipFile( fileName )
    import cStringIO
    file = cStringIO.StringIO()
    name = zf.namelist()
    csfiles = [ [], [] ]
    for x in name :
        zi = zf.getinfo( x )
        csfiles[ 0 ].append( zi.comment )
        cs = cStringIO.StringIO()
        csfiles[ 1 ].append( cs )           
        cs.write( zf.read( x ) )
        cs.seek( 0 )          
    zf.close()
    csfiles = zip( csfiles[ 0 ], csfiles[ 1 ] )
    return csfiles
#@-node:mork.20040926105355.9:openChaptersFile
#@+node:mork.20040926105355.8:insertChapters
def insertChapters( chapters, frame, c ):
     notebook = notebooks.get(c)
     if not notebook: return # For unit testing
     pagenames = notebook.pagenames()
     for num, tup  in enumerate( chapters ):
            x, y = tup
            if num > 0:
                sv = addPage( c, x ).sv
                notebook.nextpage()
                cselection = notebook.getcurselection()
            else:
                cselection = notebook.getcurselection()
                sv = getSV( cselection , c )
            sv.set( x )
            next = cselection
            setTree( next , notebook, c )
            frame.c.fileCommands.open( y, sv.get() )
            if num == 0:
                flipto = cselection
     setTree( flipto, notebook, c )
     c.frame.canvas.update_idletasks()
#@nonl
#@-node:mork.20040926105355.8:insertChapters
#@-others
#@nonl
#@-node:mork.20040930091035.1:opening
#@+node:mork.20040930091035.2:closing
#@+others
#@+node:mork.20040926105355.30:newWrite_LEO_file
def newWrite_LEO_file( self,fileName,outlineOnlyFlag, singleChapter = False):
    
    c = self.c
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    pagenames = notebook.pagenames()
    at = c.atFileCommands
    if len( pagenames ) > 1 and not singleChapter:        
        chapList = []
        self.__class__.__setattr__ =  getMakeStringIO( chapList )
        rv = writeChapters( self, fileName, pagenames, c , outlineOnlyFlag )
        if rv:
            zipChapters( fileName, pagenames, c, chapList )
        del self.__class__.__setattr__         
    else:
        rv = olWrite_LEO_file( self, fileName, outlineOnlyFlag )

    return rv
#@nonl
#@-node:mork.20040926105355.30:newWrite_LEO_file
#@+node:mork.20040929092231:getMakeStringIO
def getMakeStringIO( chapList ):
    #insures data is put in a StringIO instance
    def makeStringIO( self, name, value , cList = chapList):
        if name == 'outputFile' and value != None:
            import StringIO
            cS = StringIO.StringIO()
            cS.close = lambda : None
            self.__dict__[ name ] = cS
            cList.append( cS )
        elif name == 'outputFile' and value == None:
            self.__dict__[ name ] = None
        else:
            self.__dict__[ name ] = value 
            
    return makeStringIO
#@nonl
#@-node:mork.20040929092231:getMakeStringIO
#@+node:mork.20040929090525:writeChapters
def writeChapters( self, fileName, pagenames, c , outlineOnlyFlag):
    #goes over Chapters and puts info in StringIO instances
    for z in pagenames:
        sv = getSV( z, c )
        chapter = chapters[ sv ]
        chapter.setVariables()
        rv = olWrite_LEO_file( self, fileName, outlineOnlyFlag )    
    c.cChapter.setVariables()
    return rv
#@nonl
#@-node:mork.20040929090525:writeChapters
#@+node:mork.20040929090525.1:zipChapters
def zipChapters( fileName, pagenames, c, chapList ):
    #takes list of StringIO instances and zips them to a file
    zf = zipfile.ZipFile( fileName, 'w',  zipfile.ZIP_DEFLATED )
    for x ,fname in enumerate( pagenames ):
        sv = getSV( fname, c )
        zif = zipfile.ZipInfo( str( x ) )
        zif.comment = sv.get()
        zif.compress_type = zipfile.ZIP_DEFLATED
        chapList[ x ].seek( 0 )
        zf.writestr( zif ,chapList[ x ].read() )
    zf.close()
#@nonl
#@-node:mork.20040929090525.1:zipChapters
#@-others
#@nonl
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
#@+node:mork.20040926105355.34:newos_path_dirname
olos_pat_dirname  = g.os_path_dirname

def newos_path_dirname( path, encoding = None ):
    if iscStringIO:
        c = g.top()
        return os.path.dirname( c.mFileName )
    else:
        return olos_pat_dirname( path, encoding )
#@-node:mork.20040926105355.34:newos_path_dirname
#@+node:mork.20040926105355.45:newendEditLabel
olEditLabel = leoTkinterTree.leoTkinterTree.endEditLabel

def newendEditLabel( self ):
    
    c = self.c
    rv = olEditLabel( self )
    v = c.currentPosition()
    if v and hasattr( c.frame.body, 'r'): 
        hS = v.headString()
        if hS:
            c.frame.body.r.configure( text = v.headString() )
    return rv
#@-node:mork.20040926105355.45:newendEditLabel
#@+node:mork.20040926105355.52:newselect
def newselect (self, v , updateBeadList = True):
    
    self.frame.body.lastNode = v
    notebook = notebooks.get(v.c)
    if not notebook: return # For unit testing
    self.frame.body.lastChapter = notebook.getcurselection()
    rv = ol_select( self , v, updateBeadList )
    if hasattr( v.c.frame.body, 'r' ):
        v.c.frame.body.r.configure( text = v.headString() )
    return rv
#@nonl
#@-node:mork.20040926105355.52:newselect
#@+node:mork.20040926105355.49:newTrashDelete
if hasattr( leoNodes.vnode, 'doDelete' ):
    olDelete = leoNodes.vnode.doDelete
else:
    olDelete = leoNodes.position.doDelete

def newTrashDelete(  self, newVnode):
    c = self.c
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    pagenames = notebook.pagenames()
    pagenames = [ getSV( x, c ).get().upper() for x in pagenames ]
    nbnam = notebook.getcurselection()
    if nbnam != None:
        name = getSV( notebook.getcurselection() , c ).get().upper()
    else: name = 'TRASH'
    tsh = 'TRASH'
    if name != tsh and tsh in pagenames:
        index = pagenames.index( tsh )
        trchapter = chapters[ getSV( index, c ) ]
        trashnode = trchapter.rp
        trchapter.setVariables()
        self.moveAfter( trashnode )
        c.cChapter.setVariables()
        c.selectVnode( newVnode )        
        return self
    olDelete( self, newVnode )
#@-node:mork.20040926105355.49:newTrashDelete
#@-others
#@nonl
#@-node:mork.20040930091624:decorated Leo functions
#@+node:mork.20040930091759:operation( node ) to Chapter
#@+others
#@+node:mork.20040926105355.31:cloneToChapter
if hasattr( leoFileCommands.fileCommands, 'write_LEO_file' ):
    olWrite_LEO_file = leoFileCommands.fileCommands.write_LEO_file
else:
    olWrite_LEO_file = leoFileCommands.fileCommands.write_Leo_file
    

def cloneToChapter( c , name ):
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    page = notebook.page( notebook.index( name ) )
    c.beginUpdate()
    vnd = c.currentPosition()
    clo = vnd.clone( vnd )
    clChapter = chapters[ page.sv ]
    vndm = clChapter.cp
    clo.unlink()
    clo.linkAfter(vndm)
    c.endUpdate()
#@-node:mork.20040926105355.31:cloneToChapter
#@+node:mork.20040926105355.32:moveToChapter
def moveToChapter( c, name ):
    
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    page = notebook.page( notebook.index( name ) )
    mvChapter = chapters[ page.sv ]
    c.beginUpdate()
    vnd = c.currentVnode()
    if  not vnd.parent() and not vnd.back() :
        c.endUpdate()
        return None
    vndm = mvChapter.cp
    vnd.unlink()
    vnd.linkAfter(vndm)
    c.endUpdate()
    c.selectVnode( c.rootVnode() )

#@-node:mork.20040926105355.32:moveToChapter
#@+node:mork.20040926105355.33:copyToChapter
def copyToChapter( c, name ):
    
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    page = notebook.page( notebook.index( name ) )
    cpChapter = chapters[ page.sv ]
    c.beginUpdate()
    s = c.fileCommands.putLeoOutline()
    v = c.fileCommands.getLeoOutline( s )
    cpChapter.setVariables()
    mvnd = cpChapter.cp
    v.moveAfter( mvnd )
    c.cChapter.setVariables()
    c.endUpdate()

#@-node:mork.20040926105355.33:copyToChapter
#@+node:mork.20040926105355.39:makeNodeIntoChapter
def makeNodeIntoChapter( c, vnd = None ):
    renum = vnd
    if vnd == None:
        vnd = c.currentPosition()
    if vnd == c.rootPosition() and vnd.next() == None:
        return
    nxt = vnd.next()
    if nxt:
        vnd.doDelete( nxt )
        
    page = addPage( c )
    mnChapter = chapters[ page.sv ]
    c.beginUpdate()
    oChapter = c.cChapter
    mnChapter.makeCurrent()
    root = mnChapter.rp
    vnd.moveAfter( root )
    c.setRootPosition( vnd )
    oChapter.makeCurrent()
    c.endUpdate()
    if not renum:
        notebook = notebooks.get(c)
        if notebook: # For unit testing
            renumber(notebook)
    c.selectPosition( oChapter.rp )
#@-node:mork.20040926105355.39:makeNodeIntoChapter
#@-others
#@nonl
#@-node:mork.20040930091759:operation( node ) to Chapter
#@+node:mork.20040930092027:conversions
#@+others
#@+node:mork.20040926105355.37:conversionToSimple
def conversionToSimple( c ):
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
    pagenames.remove( current )
    c.beginUpdate()
    for z in pagenames:
        index = notebook.index( z )
        page = notebook.page( index )
        chapter = chapters[ page.sv ]
        rvNode = chapter.rp
        while 1:
            nxt = rvNode.next()
            rvNode.moveAfter( vnd )
            if nxt: rvNode = nxt
            else:
                vnd = rvNode 
                break
        notebook.delete( z )
    c.endUpdate()
    renumber( notebook )       
#@-node:mork.20040926105355.37:conversionToSimple
#@+node:mork.20040926105355.38:conversionToChapters
def conversionToChapters( c ):
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    vnd = c.rootPosition()
    while 1:
        nxt = vnd.next()
        if nxt:
            makeNodeIntoChapter(c , nxt )
        else:
            break
    setTree( notebook.pagenames()[ 0 ], notebook , c )     
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
    import tkFileDialog
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
def exportLeoFile( c ):
    import tkFileDialog
    name = tkFileDialog.asksaveasfilename()
    if name:
        if not name.endswith('.leo' ):
            name += '.leo'
        c.fileCommands.write_LEO_file( name, False, singleChapter = True )
#@-node:mork.20040926105355.48:exportLeoFile
#@-others
#@nonl
#@-node:mork.20040930092027.1:import/export
#@+node:mork.20040930092207:functions without classification
#@+at
# couldn't think of any parent node to group these under.
#@-at
#@@c
#@+others
#@+node:mork.20040926105355.46:swapChapters
def swapChapters( c, name ):

    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    cselection = notebook.getcurselection()
    tab1 = notebook.tab( cselection )
    tab2 = notebook.tab( name )
    tval1 = tab1.cget( 'text' )
    tval2 = tab2.cget( 'text' )
    tv1 = getSV( cselection, c )
    tv2 = getSV( name, c )
    chap1 = c.cChapter
    chap2 = chapters[ tv2 ]
    rp, tp, cp = chap2.rp, chap2.tp, chap2.cp
    chap2.rp, chap2.tp, chap2.cp = chap1.rp, chap1.tp, chap1.cp
    chap1.rp, chap1.tp, chap1.cp = rp, tp, cp
    chap1.setVariables()
    c.redraw()
    chap1.canvas.update_idletasks()
  
    val1 = tv1.get()
    val2 = tv2.get()
    if  val2.isdigit() :
        tv1.set( notebook.index( cselection ) + 1 ) 
    else: tv1.set( val2 )
    if val1.isdigit() :
        tv2.set( notebook.index( name ) + 1 )
    else: tv2.set( val1 )

#@-node:mork.20040926105355.46:swapChapters
#@+node:mork.20040926105355.50:emptyTrash
def emptyTrash( notebook  , c):
    pagenames = notebook.pagenames()
    pagenames = [ getSV( x, c ) for x in pagenames ]
    for z in pagenames:
        if z.get().upper() == 'TRASH':
            trChapter = chapters[ z ]
            rvND = trChapter.rp
            c.beginUpdate()
            trChapter.setVariables()
            nRt = rvND.insertAfter()
            nRt.moveToRoot()
            trChapter.rp = c.rootPosition()
            trChapter.cp = c.currentPosition()
            trChapter.tp = c.topPosition()
            c.cChapter.setVariables()
            c.endUpdate( False )
            if c.cChapter == trChapter:
                c.selectPosition( nRt )
                c.redraw()
                trChapter.canvas.update_idletasks()
            return
#@-node:mork.20040926105355.50:emptyTrash
#@+node:mork.20040926105355.51:regexClone
def regexClone( c , name ):
    if c == None: c = g.top()
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    sv = getSV( name, c )
    chapter = chapters[ sv ]
    
    def cloneWalk( result , entry, widget, c = c):
        txt = entry.get()
        widget.deactivate()        
        widget.destroy()
        if result == 'Cancel': return None
        import re
        regex = re.compile( txt )
        rt = chapter.cp
        chapter.setVariables()
        stnode = leoNodes.tnode( '', txt )
        snode = leoNodes.vnode( c, stnode)
        snode = leoNodes.position( snode, [] )
        snode.moveAfter( rt )
        ignorelist = [ snode ]
        it = walkChapters( c , ignorelist = ignorelist)
        for z in it:
            f = regex.search( z.bodyString() )
            if f:
                clone = z.clone( z )
                i = snode.numberOfChildren()
                clone.moveToNthChildOf( snode, i)
                ignorelist.append( clone )
                
        c.cChapter.setVariables()
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
    sd.activate(  geometry = 'centerscreenalways' ) 
#@-node:mork.20040926105355.51:regexClone
#@-others
#@nonl
#@-node:mork.20040930092207:functions without classification
#@+node:mork.20040930091624.1:PDF
# Requires reportlab toolkit at http://www.reportlab.org

#@+others
#@+node:mork.20040926105355.42:doPDFConversion
def doPDFConversion( c ):
    notebook = notebooks.get(c)
    if not notebook: return # For unit testing
    import cStringIO
    from reportlab.platypus import SimpleDocTemplate,  Paragraph , Spacer 
    from reportlab.lib.styles import getSampleStyleSheet 
    from reportlab.lib.units import inch
    from reportlab.rl_config import defaultPageSize
    PAGE_HEIGHT = defaultPageSize[ 1 ]
    PAGE_WIDTH = defaultPageSize[ 0 ]
    maxlen = 100
    styles = getSampleStyleSheet()
    pinfo = c.frame.shortFileName()
    pinfo1 = pinfo.rstrip( '.leo' )
    cs = cStringIO.StringIO()
    doc = SimpleDocTemplate( cs , showBoundary = 1)
    Story = [Spacer(1,2*inch)] 
    pagenames = notebook.pagenames()   
    cChapter = c.cChapter
    for n,z in enumerate( pagenames ):
        
        n = n + 1
        sv = getSV( z , c)
        chapter = chapters[ sv ]
        chapter.setVariables()
        p = chapter.rp
        if p:
            _changeTreeToPDF( sv.get(), n, p , c, Story, styles, maxlen)
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
    cChapter.setVariables()# This sets the nodes back to the cChapter, if we didnt the makeCurrent would point to the wrong positions
    cChapter.makeCurrent()
    doc.build(Story,  onLaterPages = otherPages)
    f = open( '%s.pdf' % pinfo1, 'w' )
    cs.seek( 0 )
    f.write( cs.read() )
    f.close()
    cs.close()
#@nonl
#@-node:mork.20040926105355.42:doPDFConversion
#@+node:mork.20040926105355.43:_changeTreeToPDF
def _changeTreeToPDF( name, num, p, c, Story, styles , maxlen):
    
    import copy
    from reportlab.platypus import SimpleDocTemplate,  Paragraph , Spacer, PageBreak, XPreformatted
    from reportlab.lib.units import inch
    from reportlab.rl_config import defaultPageSize
    enc = c.importCommands.encoding
    hstyle = styles[ 'title' ]
    Story.append( Paragraph( 'Chapter %s: %s' % ( num, name), hstyle ) )
    style = styles[ 'Normal' ]
    g.trace(p)
    for v in p.allNodes_iter(): #self_and_subtree_iter doesn't seem to work here????  Switched to allNodes_iter
    # while v:
        head = v.moreHead( 0 )
        head = g.toEncodedString(head,enc,reportErrors=True) 
        s = head +'\n'
        body = v.moreBody() # Inserts escapes.
        if len(body) > 0:
            body = g.toEncodedString(body,enc, reportErrors=True)
            s = s + body
            s = s.split( '\n' )
            s2 = []
            for z in s:
                if len( z ) < maxlen:
                    s2.append( z )
                else:
                    while 1:
                        s2.append( z[ : maxlen ] )
                        if len( z[ maxlen: ] ) > maxlen:
                            z = z[ maxlen: ]
                        else:
                            s2.append( z[ maxlen: ] )
                            break
            s = '\n'.join( s2 )
            s = s.replace( '&' ,'&amp;' )
            s = s.replace( '<', '&lt;' )
            s = s.replace( '>', '&gt;' )
            s = s.replace( '"', '&quot;' )
            s = s.replace( "`", '&apos;' )
            Story.append( XPreformatted( s, style ) )
            Story.append( Spacer( 1, 0.2 * inch ) )
        #v = v.threadNext() 
    Story.append( PageBreak() )
#@nonl
#@-node:mork.20040926105355.43:_changeTreeToPDF
#@-others
#@nonl
#@-node:mork.20040930091624.1:PDF
#@-others
    
ol_select = leoTkinterTree.leoTkinterTree.select

if Pmw and not g.app.unitTesting: # Not for unit testing:  modifies core classes.
    if g.app.gui is None: 
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        #@        << override various methods >>
        #@+node:ekr.20041103054545:<< override various methods >>
        leoTkinterFrame.leoTkinterFrame.createCanvas = newCreateCanvas
        leoTkinterFrame.leoTkinterBody.createControl = newCreateControl
        
        leoTkinterTree.leoTkinterTree.select = newselect
        leoTkinterTree.leoTkinterTree.endEditLabel = newendEditLabel
        leoTkinterTree.leoTkinterTree.__init__ = newTreeinit
        
        g.os_path_dirname = newos_path_dirname
        
        leoFileCommands.fileCommands.write_LEO_file = newWrite_LEO_file
        leoFileCommands.fileCommands.write_Leo_file = newWrite_LEO_file
        leoFileCommands.fileCommands.getLeoFile = newGetLeoFile
        leoFileCommands.fileCommands.open = newOpen
        
        if hasattr( leoNodes.vnode, 'doDelete' ):
            leoNodes.vnode.doDelete = newTrashDelete
        else:
            leoNodes.position.doDelete = newTrashDelete
        #@nonl
        #@-node:ekr.20041103054545:<< override various methods >>
        #@nl
        g.plugin_signon( __name__ )
#@nonl
#@-node:mork.20040926105355.1:@thin chapters.py
#@-leo
