#@+leo-ver=4-thin
#@+node:mork.20041018091414.1:@thin fastGotoNode.py
#@<< docstring >>
#@+node:ekr.20050226120947:<< docstring >>
''' A Leo plugin that adds quick Utility commands through a pop-up menu.

To summon Menu, type control-space.
To Unsummon, Right Click.

This plugin offers 3 main feature sets:
    
1. Movement. If a node has ancestors,siblings or children a menu option will
appear offering the user the ability to jump to the node from the current node.
This is an improvement over moving one node at a time with the keyboard
commands.

2. Inserting text. These menus offer the current language keywords, the
directives the body recognizes and any @file type headline directives. It offers
the new user easy access to the different directives and ways to write a file.

3. Moving Nodes( experimental feature ). You can quickly move a node to its
parent's parent or after a sibling, if they exist.'''
#@nonl
#@-node:ekr.20050226120947:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:mork.20041018091414.2:<< imports >>
from leoPlugins import *
from leoGlobals import *  
from leoNodes import *

import Tkinter
import tkFileDialog
import os 
#@nonl
#@-node:mork.20041018091414.2:<< imports >>
#@nl
__version__ = ".100"
#@<< version history >>
#@+node:ekr.20050226120947.1:<< version history >>
#@@killcolor

#@+at
# 
# .100 EKR:
#     - Added init functions.
#@-at
#@nonl
#@-node:ekr.20050226120947.1:<< version history >>
#@nl

#@+others
#@+node:ekr.20050226120947.2:init
def init ():
    
    calculateMenuSize()
    registerHandler( ('start2' , 'open2', 'new') , registerPopupMenu )
    plugin_signon(__name__)
    
    pth = os.path.split( app.loadDir )
    lkpm = pth[ 0 ] + r"/plugins/fgn.fgn"

    if os.path.exists( lkpm ):
        loadLanguages( lkpm )
#@nonl
#@-node:ekr.20050226120947.2:init
#@+node:mork.20041018091414.3:disappear
smenu = Tkinter.Menu( tearoff = 0, activeforeground = 'blue' , activebackground = 'white')   
maxmenu = 0
menus = []

def disappear( event , c):
    smenu.unpost()
    smenu.unbind_all("<Button-3>") 
    c.frame.body.bodyCtrl.focus_set()
#@-node:mork.20041018091414.3:disappear
#@+node:mork.20041018091414.4:pop
lastwidg = None
def pop( event , c ):
    clear()    
    needs_sep = needsSeparator( smenu )
    
    def addMenu( label , menu ):
        menus.append( menu )
        needs_sep.next()
        smenu.add_cascade( label = label, menu = menu )
        menu.configure( activeforeground = 'blue', activebackground = 'white' )
        def em( event ): 
            smenu.focus_set()
        menu.bind( '<Expose>', em ) 

    smenu.bind('<Left>', lambda event, c = c: disappear( event, c ) )
 
              
    ancmenu = getAncestorsMenu( smenu, c )
    if ancmenu:
        addMenu( 'Ancestors', ancmenu )
        
    sibmenu = getSiblingsMenu( smenu, c )
    if sibmenu:
        addMenu( 'Siblings', sibmenu )
        
    chimenu = getChildrenMenu( smenu, c )
    if chimenu:
        addMenu( 'Children', chimenu )
         
    winmenu = getWindowMenu( smenu, c )
    if winmenu:
        addMenu( 'Windows', winmenu )
                
    srmenu = getSectionReferenceMenu( smenu, c ) 
    if srmenu:
        addMenu( 'Insert '+ '<' +'< '+'>'+'>' , srmenu ) 
    
    menu , language = addLanguageMenu( smenu , c )
    if menu:
        addMenu( language, menu )
         
    dimenu = getDirectiveInsert( smenu, c )
    addMenu( 'Directives', dimenu ) 
    
    hmenu = getHeadlineMenu( smenu, c )
    addMenu( 'Headline', hmenu )
    
    mvamenu = getMoveAMenu( smenu, c )
    if mvamenu: addMenu( "Mv_Ancestor", mvamenu )
    
    mvsmenu = getMoveSMenu( smenu, c )
    if mvsmenu: addMenu( "Mv_Sibling", mvsmenu )
    

    smenu.bind_all("<Button-3>", lambda event, c = c :disappear( event, c )  ) 
    smenu.post( event.x_root , event.y_root)
    smenu.focus_set()
     
#@-node:mork.20041018091414.4:pop
#@+node:mork.20041018091414.5:getSectionReferenceMenu
def getSectionReferenceMenu( pmenu, c ):
    pos = c.currentPosition()
    nc = pos.numberOfChildren()
    import re
    reg = re.compile( "^<"+"<.+?>"+">$")
    srefs = []
    for z in xrange( nc ):
        chi = pos.nthChild( z )
        hl = chi.headString()
        if reg.match( hl ):
            srefs.append( hl )
    
    srmenu = None       
    if len( srefs ):
        srefs.sort() 
        srmenu = Tkinter.Menu( pmenu, tearoff= 0 )
        sb = shouldBreak()
        for z in srefs:
            srmenu.add_command( 
                label = z , 
                command = lambda label = z ,c = c :
                paster( label , c , ''), columnbreak = sb.next() )
                
    return srmenu
#@-node:mork.20041018091414.5:getSectionReferenceMenu
#@+node:mork.20041018091414.6:getWindowMenu
def getWindowMenu( pmenu , c ):
    import copy
    wl = copy.copy( windows() )
    wl.remove( c.frame )
    winmenu = None
    if len( wl ) != 0:
        winmenu = Tkinter.Menu( pmenu, tearoff = 0 )
        def bTF( frame ):
            frame.bringToFront()
            app.setLog( frame.log )
            frame.bodyCtrl.focus_set()
            clear()
        sb = shouldBreak()
        for z in wl:
            winmenu.add_command( 
                label = z.getTitle(), 
                command = lambda frame = z: bTF( frame ) , 
                columnbreak = sb.next() )
    return winmenu
#@-node:mork.20041018091414.6:getWindowMenu
#@+node:mork.20041018091414.7:getChildrenMenu
def getChildrenMenu( pmenu, c ):
    pos = c.currentPosition()
    nchildren = pos.numberOfChildren()
    chimenu = None
    if nchildren > 0 :
        chimenu = Tkinter.Menu( pmenu, tearoff = 0 ) 
        sb = shouldBreak() 
        childnames = []
        children = {}
        for z in xrange( pos.numberOfChildren() ):
            child = pos.nthChild( z )
            hs = child.headString()
            childnames.append( hs )
            children[ hs ] = child
        childnames.sort()
        def adder( a ):
            hs = a
            child = children[ hs ]
            chimenu.add_command( 
                label = hs , 
                command = lambda pos = child, c = c:
                jumpto(pos , c ) , 
                columnbreak = sb.next() )
        map( adder, childnames )        
    return chimenu
#@-node:mork.20041018091414.7:getChildrenMenu
#@+node:mork.20041018091414.8:getSiblingsMenu
def getSiblingsMenu( pmenu, c ):
    siblings = []
    pos = c.currentPosition()
    siblings = getSiblingList( pos)
    sibmenu = None
    def sorSibs( a, b ):
        if a.headString() > b.headString() : return 1
        elif a.headString() < b.headString() : return -1
        return 0
    siblings.sort( sorSibs )
    if len( siblings ) != 0:        
        sibmenu = Tkinter.Menu(pmenu, tearoff = 0)  
        sb = shouldBreak()
        for z in siblings:
            hs = z.headString()
            sibmenu.add_command( 
                label = hs , 
                command = lambda pos = z, c = c:
                jumpto( pos, c ) , 
                columnbreak = sb.next() )
                
    return sibmenu    
#@-node:mork.20041018091414.8:getSiblingsMenu
#@+node:mork.20041018113134:getSiblingList
def getSiblingList( pos ):
    
    siblings = []
    pnod = pos.back()
    while pnod:
        siblings.append( pnod )
        pnod = pnod.back()
    siblings.reverse()
    nnod = pos.next()
    while nnod:
        siblings.append( nnod )
        nnod = nnod.next()
    return siblings
#@nonl
#@-node:mork.20041018113134:getSiblingList
#@+node:mork.20041018091414.9:getAncestorsMenu
def getAncestorsMenu( pmenu, c ):
        ancmenu = None
        alist = getAncestorList( c.currentPosition() )
        if alist:
            ancmenu = Tkinter.Menu( pmenu, tearoff = 0 )
            sb = shouldBreak()
            for z in alist:
                hs = z.headString()
                ancmenu.add_command( 
                    label = hs , 
                    command = lambda  parent = z, c = c: 
                    jumpto( parent , c ), 
                    columnbreak = sb.next() )

        return ancmenu
#@-node:mork.20041018091414.9:getAncestorsMenu
#@+node:mork.20041018114908:getAncestorList
def getAncestorList( p ):
    
    alist = []
    parent = p.parent()
    while parent:
        alist.append( parent )        
        parent = parent.parent()
    return alist
#@nonl
#@-node:mork.20041018114908:getAncestorList
#@+node:mork.20041018091414.10:addLanguageMenu
def addLanguageMenu( pmenu , c , haveseen = {}):
    colorizer = c.frame.body.getColorizer()
    if colorizer.language:
        if not haveseen.has_key( colorizer.language ): 
            lk = colorizer.language + '_keywords'
            kwords = list( getattr( colorizer , lk ) )
            if langdict.has_key( colorizer.language ):
                l = langdict[ colorizer.language ]
                for z in l:
                    kwords.append( z )
                kwords.sort()
        else:
            kwords = haveseen[ colorizer.language ] 
        lmenu = Tkinter.Menu( pmenu, tearoff = 0 ) 
        sb = shouldBreak()
        for z in kwords:
            lmenu.add_command( 
                label = z , 
                command = lambda keyword = z , c = c : 
                paster( keyword , c ) ,
                columnbreak = sb.next() )
                
        return lmenu , colorizer.language
    else: return None , None
#@-node:mork.20041018091414.10:addLanguageMenu
#@+node:mork.20041018120620:getMoveAMenu
def getMoveAMenu( pmenu, c ):
    
    mvmenu = None

    def mvchild( p, p2 , c = c ):
        c.beginUpdate()
        p.moveToNthChildOf( p2, 0 )
        c.endUpdate()
        
    pos = c.currentPosition()
    alist = getAncestorList( pos )
    if alist: alist.pop( 0 )
    if alist:
        mvmenu = Tkinter.Menu( pmenu, tearoff = 0 )
        sb = shouldBreak()
        for z in alist:    
            hs = z.headString()
            mvmenu.add_command( 
                label = hs , 
                command = lambda p = pos, p2 = z: 
                mvchild( p, p2 ),
                columnbreak = sb.next() )
    return mvmenu
#@-node:mork.20041018120620:getMoveAMenu
#@+node:mork.20041018120620.1:getMoveSMenu
def getMoveSMenu( pmenu , c):
    
    smenu = None
    pos = c.currentPosition()
    sibs = getSiblingList( pos )
    bk = pos.back()
    if bk: sibs.remove( bk )
    def mafter( p, p2, c = c ):
        c.beginUpdate()
        p.moveAfter( p2 )
        c.endUpdate()
    if sibs:
        smenu = Tkinter.Menu( pmenu, tearoff = 0 )
        sb = shouldBreak()
        for z in sibs:
            smenu.add_command( label = z.headString(), 
                            command = lambda p = pos, p2 = z: mafter( p, p2 ),
                            columnbreak = sb.next() ) 

    return smenu
#@nonl
#@-node:mork.20041018120620.1:getMoveSMenu
#@+node:mork.20041018091414.11:needsSeparator
def needsSeparator( menu ):
    yield None
    while 1:
        menu.add_separator()
        yield None
#@-node:mork.20041018091414.11:needsSeparator
#@+node:mork.20041018091414.12:shouldBreak
def shouldBreak():
    i = 0
    while 1:
        i += 1
        if i == maxmenu:
            i = 0
            yield True
        else: yield False
#@-node:mork.20041018091414.12:shouldBreak
#@+node:mork.20041018091414.13:getDirectiveInsert
def getDirectiveInsert( pm, c , directives = [], directives2= []):
    m = Tkinter.Menu( pm, tearoff = 0 )
    sb = shouldBreak()
    if len( directives ) == 0:
        import leoColor 
        for z in leoColor.leoKeywords:
            directives.append( z )
        directives.sort()                                      
    for z in directives:
       m.add_command( 
          label = z , 
          columnbreak = sb.next(),  
          command = lambda label = z, c = c: 
          paster( label , c ) )

    return m
#@-node:mork.20041018091414.13:getDirectiveInsert
#@+node:mork.20041018092814:getHeadlineMenu
def getHeadlineMenu( pmenu, c ):
    
    pos = c.currentPosition()
    v = pos.v
    def getValue( names, self = v ):
        return names
    olFindAtFileName = v.findAtFileName
    v.findAtFileName = getValue
    names = v.anyAtFileNodeName()
    v.findAtFileName = olFindAtFileName
    names = list( names )
    names.sort()
    hmenu = Tkinter.Menu( pmenu , tearoff = 0)
    hmenu.add_command( 
        label = 'add <'+'<'+'>'+'>', 
        command = lambda c = c: addGL( c ) )
    hmenu.add_separator()
    for z in names:
        hmenu.add_command( label = z, 
                            command = lambda c = c, d = z , nm = names:
                                setFileDirective( c, d, nm ) )
    hmenu.add_separator()
    hmenu.add_command( label = 'remove @', command = lambda c = c, nm = names:
                                            removeFileDirective( c, nm ) )
    return hmenu

#@-node:mork.20041018092814:getHeadlineMenu
#@+node:mork.20041018095448:setFileDirective
def setFileDirective( c , directive, names ):
    
    pos = c.currentPosition()
    hS = pos.headString()
    hS = getCleanHeadString( hS, names )
    hS = directive + " " + hS
    c.beginUpdate()
    pos.setHeadString( hS )
    c.frame.body.bodyCtrl.focus_set()  
    c.frame.body.bodyCtrl.update_idletasks() 
    c.endUpdate()
    
   

#@-node:mork.20041018095448:setFileDirective
#@+node:mork.20041018100044:removeFileDirective
def removeFileDirective( c , names ):

    pos = c.currentPosition()
    hS = pos.headString()
    hS = getCleanHeadString( hS , names )
    c.beginUpdate()
    pos.setHeadString( hS )
    c.frame.body.bodyCtrl.focus_set()  
    c.frame.body.bodyCtrl.update_idletasks() 
    c.endUpdate()
#@-node:mork.20041018100044:removeFileDirective
#@+node:mork.20041018100044.1:getCleanHeadString
def getCleanHeadString( hS, names ):

    def sT( a, b ):
        if len( a ) > len( b ): return -1
        if len( a ) < len( b ): return 1
        return 0
    names = list( names )
    names.sort( sT )
    for z in names:
        hS2 = hS.lstrip()
        if hS2.startswith( z ):
            hS = hS2.lstrip( z )
            hS = hS.lstrip()
            return hS
    return hS
#@nonl
#@-node:mork.20041018100044.1:getCleanHeadString
#@+node:mork.20041018091414.14:addGL
def addGL( c ):
    vnode = c.currentVnode()
    hs = vnode.headString()
    nhs = "<"+"<" + hs + ">"+">"
    c.beginUpdate()
    vnode.setHeadString( nhs )
    c.frame.body.bodyCtrl.focus_set()  
    c.frame.body.bodyCtrl.update_idletasks() 
    c.endUpdate()

#@-node:mork.20041018091414.14:addGL
#@+node:mork.20041018091414.15:insertHeadline
def insertHeadline( directive , c ):
    vnode = c.currentVnode()
    hs = vnode.headString()
    nhs = directive + " " + hs
    c.beginUpdate()
    vnode.setHeadString( nhs )
    c.endUpdate()
#@-node:mork.20041018091414.15:insertHeadline
#@+node:mork.20041018091414.16:paster
def paster( directive , c ,  end = ' ' ):
    bdy = c.frame.body
    c.beginUpdate()
    bdy.insertAtInsertPoint( directive + end)
    bdy.onBodyChanged( c.currentVnode() , None ) 
    bdy.bodyCtrl.focus_set()  
    bdy.bodyCtrl.update_idletasks() 
    c.endUpdate()                        
    bdy.bodyCtrl.focus_set()
#@nonl
#@-node:mork.20041018091414.16:paster
#@+node:mork.20041018091414.17:clear
def clear():
    global menus
    smenu.delete( 0 , Tkinter.END )
    for z in menus:
        z.destroy()
    menus = []
#@-node:mork.20041018091414.17:clear
#@+node:mork.20041018091414.18:jumpto
def jumpto( vnode, c):    
    smenu.unpost()
    c.beginUpdate()
    c.frame.tree.expandAllAncestors( vnode )
    c.selectVnode( vnode )
    c.endUpdate()
#@-node:mork.20041018091414.18:jumpto
#@+node:mork.20041018091414.19:registerPopupMenu
def registerPopupMenu( tag, keywords):
    c = top()
    def popper( event , c = c ):
        pop( event, c )
    c.frame.top.bind( binder , popper)
#@-node:mork.20041018091414.19:registerPopupMenu
#@+node:mork.20041018091414.20:calculateMenuSize
def calculateMenuSize():
    global maxmenu
    x = Tkinter.Menu()
    h = ( x.winfo_screenheight() *.90 ) / 25
    maxmenu = int( h )
    x.destroy()
#@-node:mork.20041018091414.20:calculateMenuSize
#@+node:mork.20041018091414.21:loadLanguages
langdict = {}  
binder = '<Control-space>' 
def loadLanguages( lkpm):
    global binder
    import ConfigParser
    cp = ConfigParser.ConfigParser()
    cp.read( lkpm )
    which = ''
    sec = cp.sections()
    for z in sec:
        if z.strip() == 'language':
            which = z
            break
    if cp.has_section( which ):
        op = cp.options( which )
        for z in op:
            z2 = cp.get( which, z ).split(',')
            z2 = [ x.strip() for x in z2 ]
            langdict[ z ] = z2
    for z in sec:
        if z.strip() == 'fgnconfig':
            which2 = z
            break
    if cp.has_section( which2 ):
        op2 = cp.options( which2 )
        for z2 in op2:
            if z2.strip() == 'binder':
                binder = cp.get( which2, z2 )
                break
#@-node:mork.20041018091414.21:loadLanguages
#@-others
#@nonl
#@-node:mork.20041018091414.1:@thin fastGotoNode.py
#@-leo