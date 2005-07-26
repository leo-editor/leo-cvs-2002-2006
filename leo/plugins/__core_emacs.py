#@+leo-ver=4-thin
#@+node:ekr.20050723062822:@thin __core_emacs.py
''' A plugin to provide Emacs commands.
Will move to Leo's core eventually.'''

#@<< imports >>
#@+node:ekr.20050723062822.1:<< imports >>
import leoGlobals as g
import leoPlugins

if 0:
    #@    << SwingMacs imports >>
    #@+node:ekr.20050724075114:<< SwingMacs imports >>
    from __future__ import generators
    import javax.swing as swing
    import javax.swing.event as sevent
    import javax.swing.text as stext
    import java.awt.event as aevent
    import java.util.regex as regex
    import java.awt as awt
    import java.lang 
    import java.io
    
    from DefCallable import DefCallable
    import LeoUtilities
    #@nonl
    #@-node:ekr.20050724075114:<< SwingMacs imports >>
    #@nl
    
import leoColor
import leoPlugins
import leoNodes
import leoTkinterFrame

try:
    import Tkinter as Tk
    import ScrolledText
    import tkFileDialog
    import tkFont
except ImportError:
    Tk = None

import ConfigParser
import os
import re  
import string
import sys
import weakref
#@nonl
#@-node:ekr.20050723062822.1:<< imports >>
#@nl
#@<< modification log >>
#@+node:ekr.20050725074202:<< modification log >>
#@@nocolor

# This discusses changes made to usetemacs/temacs code bases.

#@+others
#@+node:ekr.20050725074202.1:Rewrote buildBufferList
#@+at 
#@nonl
# There may be bugs here.  The old code had definite strange aspects to it.
#@-at
#@nonl
#@-node:ekr.20050725074202.1:Rewrote buildBufferList
#@+node:ekr.20050725074202.2:Removed Emacs_instances class var
#@+at 
#@nonl
# createBindings now sets c.emacs, so modifyOnBodyKey just uses c.emacs.
#@-at
#@nonl
#@-node:ekr.20050725074202.2:Removed Emacs_instances class var
#@+node:ekr.20050725074607:Added c ivar to Emacs class
#@+at 
#@nonl
# This is an important addition:  it guarantees that the proper commander is 
# always used.
#@-at
#@nonl
#@-node:ekr.20050725074607:Added c ivar to Emacs class
#@+node:ekr.20050725075301:Removed labels class var
#@+at 
#@nonl
# This is not needed.  createBindings is called at most once per commander.
#@-at
#@nonl
#@-node:ekr.20050725075301:Removed labels class var
#@+node:ekr.20050725132137:Added baseCommands class
#@+at 
#@nonl
# Subclasses of baseCommands class should implement getPublicCommands.
# 
# This returns a dict whose keys are emacs command names and whose values are 
# bound methods.
#@-at
#@nonl
#@-node:ekr.20050725132137:Added baseCommands class
#@-others
#@nonl
#@-node:ekr.20050725074202:<< modification log >>
#@nl

USE_TEMACS = True  # False:  use SwingMacs code base  (will probably never happen).

if USE_TEMACS:
    #@    << define usetemacs globals >>
    #@+node:ekr.20050724080034:<< define usetemacs globals >>
    ### editors = weakref.WeakKeyDictionary()
    
    haveseen = weakref.WeakKeyDictionary()
    extensions = []
    new_keystrokes = {}
    leocommandnames = None
    
    # For buffer interaction methods.
    tnodes = {} # Keys are commanders.  Values are dicts.
    positions =  {}
    
    # Original versions of methods.
    orig_Bindings = None
    orig_OnBodyKey = None
    #@nonl
    #@-node:ekr.20050724080034:<< define usetemacs globals >>
    #@nl
else:
    extensions = []
    commandsFromPlugins = {}

#@+others
#@+node:ekr.20050723062822.2:init
def init ():
    
    ok = Tk and not g.app.unitTesting
    
    if ok:
        if g.app.gui is None: 
            g.app.createTkGui(__file__)
    
        ok = g.app.gui.guiName() == "tkinter"
        if ok:
            g.plugin_signon(__name__)
            if USE_TEMACS:
                #@                << override createBindings and onBodyKey >>
                #@+node:ekr.20050724080456:<< override createBindings and onBodyKey >>
                global orig_Bindings,orig_OnBodyKey
                
                orig_Bindings = leoTkinterFrame.leoTkinterBody.createBindings
                leoTkinterFrame.leoTkinterBody.createBindings = createBindings
                
                orig_OnBodyKey = leoTkinterFrame.leoTkinterBody.onBodyKey
                leoTkinterFrame.leoTkinterBody.onBodyKey = modifyOnBodyKey
                #@nonl
                #@-node:ekr.20050724080456:<< override createBindings and onBodyKey >>
                #@nl
                leoPlugins.registerHandler( ('open2', "new") , addMenu )
            else: 
                global extensions
                extensions = lookForExtensions()
                leoPlugins.registerHandler( ('open2', "new") , createEmacs )
            
    return ok
#@nonl
#@-node:ekr.20050723062822.2:init
#@+node:ekr.20050724074642.16:loadConfig (from usetemacs)
def loadConfig():
    '''Loads Emacs extensions and new keystrokes to be added to Emacs instances'''
    pth = os.path.split(g.app.loadDir)   
    aini = pth[0]+r"/plugins/usetemacs.ini"
    if os.path.exists( aini ):
        
        cp = ConfigParser.ConfigParser()
        cp.read( aini )
        section = None
        for z in cp.sections():
            if z.strip() == 'extensions':
                section = z
                break
        
        if section:
            for z in cp.options( section ):
                extension = cp.get( section, z )
                try:
                    ex = __import__( extension )
                    extensions.append( ex )
                except Exception, x:
                    g.es( "Could not load %s because of %s" % ( extension, x ), color = 'red' )
                
        kstroke_sec = None
        for z in cp.sections():
            if z.strip() == 'newkeystrokes':
                kstroke_sec = z
                break
        if kstroke_sec:
            for z in cp.options( kstroke_sec ):
                new_keystrokes[ z.capitalize() ] = cp.get( kstroke_sec, z )
#@nonl
#@-node:ekr.20050724074642.16:loadConfig (from usetemacs)
#@+node:ekr.20050724074619.1:Birth (From usetemacs)
# Based on version .57 EKR:
#@nonl
#@+node:ekr.20050724074642.17:usetemacs Hooks
#@+node:ekr.20050724074642.18:addMenu
def addMenu( tag, keywords ):

    '''Adds the Temacs Help option to Leo's Help menu'''
    
    c = keywords.get('c')
    if not c: return

    men = c.frame.menu.getMenu( 'Help' )
    men.add_separator()
    men.add_command( label = 'Temacs Help', command = seeHelp )
#@nonl
#@-node:ekr.20050724074642.18:addMenu
#@+node:ekr.20050724074642.19:seeHelp
def seeHelp():
    '''Opens a Help dialog that shows the Emac systems commands and keystrokes'''
    tl = Tk.Toplevel()
    ms = tl.maxsize()
    tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 )) #half the screen height, half the screen width
    tl.title( "Temacs Help" )
    fixedFont = tkFont.Font( family = 'Fixed', size = 14 )
    tc = ScrolledText.ScrolledText( tl, font = fixedFont, background = 'white', wrap = 'word' )
    sbar = Tk.Scrollbar( tc.frame, orient = 'horizontal' )
    sbar.configure( command = tc.xview )
    tc.configure( xscrollcommand = sbar.set )
    sbar.pack( side = 'bottom', fill = 'x' )
    for z in tc.frame.children.values():
        sbar.pack_configure( before = z )
    tc.insert( '1.0', Emacs.getHelpText() )
    lc='''\n---------Leo Commands-----------\n'''
    tc.insert( 'end', lc )
    leocommandnames.sort()
    lstring = '\n'.join( leocommandnames )
    tc.insert( 'end', lstring )
    #@    << define clz >>
    #@+node:ekr.20050724074642.20:<< define clz >>
    def clz( tl = tl ):
        tl.withdraw()
        tl.destroy()
    #@nonl
    #@-node:ekr.20050724074642.20:<< define clz >>
    #@nl
    g = Tk.Frame( tl )
    g.pack( side = 'bottom' )
    tc.pack( side = 'top' ,expand = 1, fill = 'both')
    e = Tk.Label( g, text = 'Search:' )
    e.pack( side = 'left' )
    ef = Tk.Entry( g, background = 'white', foreground = 'blue' )
    ef.pack( side = 'left' )
    #@    << define search >>
    #@+node:ekr.20050724074642.21:<< define search >>
    def search():
        
        #stext = ef.getvalue()
        stext = ef.get()
        #tc = t.component( 'text' )
        tc.tag_delete( 'found' )
        tc.tag_configure( 'found', background = 'red' )
        ins = tc.index( 'insert' )
        ind = tc.search( stext, 'insert', stopindex = 'end', nocase = True )
        if not ind:
            ind = tc.search( stext, '1.0', stopindex = 'end', nocase = True )
        if ind:
            tc.mark_set( 'insert', '%s +%sc' % ( ind , len( stext ) ) )
            tc.tag_add(  'found', 'insert -%sc' % len( stext ) , 'insert' )
            tc.see( ind )
    #@nonl
    #@-node:ekr.20050724074642.21:<< define search >>
    #@nl
    go = Tk.Button( g , text = 'Go', command = search )
    go.pack( side = 'left' )
    b = Tk.Button( g  , text = 'Close' , command = clz )
    b.pack( side = 'left' )
    #@    << define watch >>
    #@+node:ekr.20050724074642.22:<< define watch >>
    def watch( event ):
        search()
    #@nonl
    #@-node:ekr.20050724074642.22:<< define watch >>
    #@nl
    ef.bind( '<Return>', watch )
#@nonl
#@-node:ekr.20050724074642.19:seeHelp
#@-node:ekr.20050724074642.17:usetemacs Hooks
#@+node:ekr.20050724074642.23:Overridden methods
#@+node:ekr.20050724074642.24:modifyOnBodyKey
def modifyOnBodyKey (self,event):
    
    '''stops Return and Tab from being processed if the Emacs instance has state.'''
    
    # Self is an instance of leoTkinterBody, so self.c is defined.
    c = self.c

    if event.char.isspace(): 
        if c.emacs.mcStateManager.hasState():
           return None
    else:
        return orig_OnBodyKey(self,event)
#@nonl
#@-node:ekr.20050724074642.24:modifyOnBodyKey
#@+node:ekr.20050724074642.25:createBindings & helpers  (Creates Emacs instance)
def createBindings (self,frame):
    
    c = frame.c

    #@    << create a label for frame >>
    #@+node:ekr.20050724074642.26:<< create a label for frame >>
    group = Tk.Frame(frame.split2Pane2 , relief = 'ridge', borderwidth = 3 )
    
    f2 = Tk.Frame( group )
    f2.pack( side = 'top', fill = 'x')
    
    gtitle = Tk.Label(f2,
        text = 'mini-buffer',justify = 'left',anchor = 'nw',
        foreground='blue',background='white')
    
    group.pack( side = 'bottom', fill = 'x', expand = 1 )
    
    for z in frame.split2Pane2.children.values():
        group.pack_configure(before = z)
    
    label = Tk.Label(group,relief ='groove',justify ='left',anchor='w')
    label.pack( side = 'bottom', fill = 'both', expand = 1, padx = 2, pady = 2 )
      
    gtitle.pack( side = 'left' )
    #@nonl
    #@-node:ekr.20050724074642.26:<< create a label for frame >>
    #@nl
    orig_Bindings(self,frame)
    
    # EKR: set emacs ivar in the commander.
    c.emacs = emacs = Emacs(frame.c, frame.bodyCtrl, label, useGlobalKillbuffer = True, useGlobalRegisters = True )
    emacs.label = label
    emacs.setUndoer( frame.bodyCtrl, self.c.undoer.undo )
    #@    << define utTailEnd >>
    #@+node:ekr.20050724074642.27:<< define utTailEnd >>
    def utTailEnd( buffer,frame=frame):
        
        '''A method that Emacs will call with its _tailEnd method'''
    
        buffer.event_generate( '<Key>' )
        buffer.update_idletasks()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050724074642.27:<< define utTailEnd >>
    #@nl
    emacs.setTailEnd( frame.bodyCtrl,utTailEnd)
    emacs.setShutdownHook( self.c.close )
    addTemacsExtensions( emacs )
    addTemacsAbbreviations( emacs )
    addLeoCommands( self.c, emacs )
    changeKeyStrokes( emacs, frame.bodyCtrl )
    setBufferInteractionMethods( self.c, emacs, frame.bodyCtrl )
    orig_del = frame.bodyCtrl.delete
    #@    << define watchDelete >>
    #@+node:ekr.20050724074642.28:<< define watchDelete >>
    def watchDelete(i,j=None,emacs=emacs): ## ,Emacs=Emacs,orig_del=orig_del,frame=frame):
    
        '''Watches for complete text deletion.  If it occurs, turns off all state in the Emacs instance.'''
    
        if i == '1.0' and j == 'end':
            # g.trace()
            event = Tk.Event()
            event.widget = frame.bodyCtrl ## Text
            emacs.keyboardQuit( event )
    
        return orig_del( i, j )
    #@nonl
    #@-node:ekr.20050724074642.28:<< define watchDelete >>
    #@nl
    frame.bodyCtrl.delete = watchDelete
#@nonl
#@+node:ekr.20050724074642.29:addTemacsAbbreviations:  To do:  get stuff from confic
def addTemacsAbbreviations( Emacs ):
    
    '''Adds abbreviatios and kbd macros to an Emacs instance'''

    pth = os.path.split( g.app.loadDir ) 
    aini = pth[ 0 ] + os.sep + 'plugins' + os.sep

    if os.path.exists( aini + r'usetemacs.kbd' ):
        f = file( aini +  r'usetemacs.kbd', 'r' )
        Emacs._loadMacros( f )

    if os.path.exists( aini + r'usetemacs.abv' ):
        f = file( aini + r'usetemacs.abv', 'r' )
        Emacs._readAbbrevs( f )
#@nonl
#@-node:ekr.20050724074642.29:addTemacsAbbreviations:  To do:  get stuff from confic
#@+node:ekr.20050724074642.30:addTemacsExtensions
def addTemacsExtensions( Emacs ):
    
    '''Adds extensions to Emacs parameter.'''
    for z in extensions:
        try:
            if hasattr(z, 'getExtensions' ):
                ex_meths = z.getExtensions()
                for x in ex_meths.keys():
                    Emacs.extendAltX( x, ex_meths[ x ] )
            else:
                g.es( 'Module %s does not have a getExtensions function' % z , color = 'red' )

        except Exception, x:
            g.es( 'Could not add extension because of %s' % x, color = 'red' )
#@nonl
#@-node:ekr.20050724074642.30:addTemacsExtensions
#@+node:ekr.20050724074642.31:changeKeyStrokes
def changeKeyStrokes( Emacs, tbuffer ):
    
    for z in new_keystrokes.keys():
        Emacs.reconfigureKeyStroke( tbuffer, z, new_keystrokes[ z ] )
#@nonl
#@-node:ekr.20050724074642.31:changeKeyStrokes
#@+node:ekr.20050724074642.32:setBufferInteractionMethods & helpers
def setBufferInteractionMethods (c,emacs,buffer):

    '''This function configures the Emacs instance so that
       it can see all the nodes as buffers for its buffer commands.'''
       
    #@    @+others
    #@+node:ekr.20050724074642.33:OLDbuildBufferList
    def OLDbuildBufferList ():#This builds a buffer list from what is in the outline.  Worked surprisingly fast on LeoPy.
        if not tnodes.has_key(c):#I was worried that speed factors would make it unusable.
            tnodes[c] ={}
        tdict = tnodes[c]
        pos = c.rootPosition()
        utni = pos.allNodes_iter()
        bufferdict ={}
        tdict.clear()
        positions.clear()
        for z in utni:
        
           t = z.v.t 
           if positions.has_key(t.headString):
            positions[t.headString].append(z.copy())
           else:
            positions[t.headString] =[z.copy()]#not using a copy seems to have bad results.
           #positions[ t.headString ] = z
        
           bS = ''
           if t.bodyString:bS = t.bodyString 
    
           
           bufferdict[t.headString] = bS 
           tdict[t.headString] = t 
        
        return bufferdict 
    #@nonl
    #@-node:ekr.20050724074642.33:OLDbuildBufferList
    #@+node:ekr.20050725070621:buildBufferList  (MAY BE BUGGY)
    def buildBufferList (self):
        
        '''Build a buffer list from an outline.'''
        
        c = self.c ; global positions, tnodes 
    
        d = {} ; positions.clear()
    
        for p in c.allNodes_iter():
            t = p.v.t ; h = t.headString()
            theList = positions.get(h,[])
            theList.append(p.copy())
            self.positions[h] = theList 
            d[h] = t.bodyString()
            
        tnodes[c] = d
        return d 
    #@nonl
    #@-node:ekr.20050725070621:buildBufferList  (MAY BE BUGGY)
    #@+node:ekr.20050724074642.34:setBufferData
    def setBufferData (name,data):
        
        data = unicode(data)
        tdict = tnodes[c]
        if tdict.has_key(name):
            tdict[name].bodyString = data 
    #@nonl
    #@-node:ekr.20050724074642.34:setBufferData
    #@+node:ekr.20050724074642.35:gotoNode & gotoPosition
    def gotoNode (name):
        
        c.beginUpdate()
        if positions.has_key(name):
            posis = positions[name]
            if len(posis)>1:
                tl = Tk.Toplevel()
                #tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 ))
                tl.title("Select node by numeric position")
                fr = Tk.Frame(tl)
                fr.pack()
                header = Tk.Label(fr,text='select position')
                header.pack()
                lbox = Tk.Listbox(fr,background='white',foreground='blue')
                lbox.pack()
                for z in xrange(len(posis)):
                    lbox.insert(z,z+1)
                lbox.selection_set(0)
                def setPos (event):
                    cpos = int(lbox.nearest(event.y))
                    tl.withdraw()
                    tl.destroy()
                    if cpos!=None:
                        gotoPosition(c,posis[cpos])
                lbox.bind('<Button-1>',setPos)
                geometry = tl.geometry()
                geometry = geometry.split('+')
                geometry = geometry[0]
                width = tl.winfo_screenwidth()/3
                height = tl.winfo_screenheight()/3
                geometry = '+%s+%s'%(width,height)
                tl.geometry(geometry)
            else:
                pos = posis[0]
                gotoPosition(c,pos)
        else:
            pos2 = c.currentPosition()
            tnd = leoNodes.tnode('',name)
            pos = pos2.insertAfter(tnd)
            gotoPosition(c,pos)
        #c.frame.tree.expandAllAncestors( pos )
        #c.selectPosition( pos )
        #c.endUpdate()
    #@nonl
    #@+node:ekr.20050724074642.36:gotoPosition
    def gotoPosition (c,pos):
    
        c.frame.tree.expandAllAncestors(pos)
        c.selectPosition(pos)
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.36:gotoPosition
    #@-node:ekr.20050724074642.35:gotoNode & gotoPosition
    #@+node:ekr.20050724074642.37:deleteNode
    def deleteNode (name):
        
        c.beginUpdate()
        if positions.has_key(name):
            pos = positions[name]
            cpos = c.currentPosition()
            pos.doDelete(cpos)
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.37:deleteNode
    #@+node:ekr.20050724074642.38:renameNode
    def renameNode (name):
    
        c.beginUpdate()
        pos = c.currentPosition()
        pos.setHeadString(name)
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.38:renameNode
    #@-others

    # These add Leo-reated capabilities to the emacs instance.
    emacs.setBufferListGetter(buffer,buildBufferList)
    emacs.setBufferSetter(buffer,setBufferData)
    emacs.setBufferGoto(buffer,gotoNode)
    emacs.setBufferDelete(buffer,deleteNode)
    emacs.setBufferRename(buffer,renameNode)
#@nonl
#@-node:ekr.20050724074642.32:setBufferInteractionMethods & helpers
#@+node:ekr.20050724074642.39:addLeoCommands  (createBindings)
def addLeoCommands( c, emacs ):
    
    global leocommandnames
    f = c.frame
    
    commands = {
        'new': c.new,
        'open': c.open,
        'openWith': c.openWith,
        'close': c.close,
        'save': c.save,
        'saveAs': c.saveAs,
        'saveTo': c.saveTo,
        'revert': c.revert,
        'readOutlineOnly': c.readOutlineOnly,
        'readAtFileNodes': c.readAtFileNodes,
        'importDerivedFile': c.importDerivedFile,
        #'writeNewDerivedFiles': c.writeNewDerivedFiles,
        #'writeOldDerivedFiles': c.writeOldDerivedFiles,
        'tangle': c.tangle,
        'tangle all': c.tangleAll,
        'tangle marked': c.tangleMarked,
        'untangle': c.untangle,
        'untangle all': c.untangleAll,
        'untangle marked': c.untangleMarked,
        'export headlines': c.exportHeadlines,
        'flatten outline': c.flattenOutline,
        'import AtRoot': c.importAtRoot,
        'import AtFile': c.importAtFile,
        'import CWEB Files': c.importCWEBFiles,
        'import Flattened Outline': c.importFlattenedOutline,
        'import Noweb Files': c.importNowebFiles,
        'outline to Noweb': c.outlineToNoweb,
        'outline to CWEB': c.outlineToCWEB,
        'remove sentinels': c.removeSentinels,
        'weave': c.weave,
        'delete': c.delete,
        'execute script': c.executeScript,
        'go to line number': c.goToLineNumber,
        'set font': c.fontPanel,
        'set colors': c.colorPanel,
        'show invisibles': c.viewAllCharacters,
        'preferences': c.preferences,
        'convert all blanks': c.convertAllBlanks,
        'convert all tabs': c.convertAllTabs,
        'convert blanks': c.convertBlanks,
        'convert tabs': c.convertTabs,
        'indent': c.indentBody,
        'unindent': c.dedentBody,
        'reformat paragraph': c.reformatParagraph,
        'insert time': c.insertBodyTime,
        'extract section': c.extractSection,
        'extract names': c.extractSectionNames,
        'extract': c.extract,
        'match bracket': c.findMatchingBracket,
        'find panel': c.showFindPanel, ## c.findPanel,
        'find next': c.findNext,
        'find previous': c.findPrevious,
        'replace': c.replace,
        'replace then find': c.replaceThenFind,
        'edit headline': c.editHeadline,
        'toggle angle brackets': c.toggleAngleBrackets,
        'cut node': c.cutOutline,
        'copy node': c.copyOutline,
        'paste node': c.pasteOutline,
        'paste retaining clone': c.pasteOutlineRetainingClones,
        'hoist': c.hoist,
        'de-hoist': c.dehoist,
        'insert node': c.insertHeadline,
        'clone node': c.clone,
        'delete node': c.deleteOutline,
        'sort children': c.sortChildren,
        'sort siblings': c.sortSiblings,
        'demote': c.demote,
        'promote': c.promote,
        'move right': c.moveOutlineRight,
        'move left': c.moveOutlineLeft,
        'move up': c.moveOutlineUp,
        'move down': c.moveOutlineDown,
        'unmark all': c.unmarkAll,
        'mark clones': c.markClones,
        'mark': c.markHeadline,
        'mark subheads': c.markSubheads,
        'mark changed items': c.markChangedHeadlines,
        'mark changed roots': c.markChangedRoots,
        'contract all': c.contractAllHeadlines,
        'contract node': c.contractNode,
        'contract parent': c.contractParent,
        'expand to level 1': c.expandLevel1,
        'expand to level 2': c.expandLevel2,
        'expand to level 3': c.expandLevel3,
        'expand to level 4': c.expandLevel4,
        'expand to level 5': c.expandLevel5,
        'expand to level 6': c.expandLevel6,
        'expand to level 7': c.expandLevel7,
        'expand to level 8': c.expandLevel8,
        'expand to level 9': c.expandLevel9,
        'expand prev level': c.expandPrevLevel,
        'expand next level': c.expandNextLevel,
        'expand all': c.expandAllHeadlines,
        'expand node': c.expandNode,
        'check outline': c.checkOutline,
        'dump outline': c.dumpOutline,
        'check python code': c.checkPythonCode,
        'check all python code': c.checkAllPythonCode,
        'pretty print python code': c.prettyPrintPythonCode,
        'pretty print all python code': c.prettyPrintAllPythonCode,
        'goto parent': c.goToParent,
        'goto next sibling': c.goToNextSibling,
        'goto previous sibling': c.goToPrevSibling,
        'goto next clone': c.goToNextClone,
        'goto next marked': c.goToNextMarkedHeadline,
        'goto next changed': c.goToNextDirtyHeadline,
        'goto first': c.goToFirstNode,
        'goto last': c.goToLastNode,
        "go to prev visible":c.selectVisBack,
        "go to next visible" : c.selectVisNext,
        "go to prev node" : c.selectThreadBack,
        "go to next node" : c.selectThreadNext,
        'about leo...': c.about,
        #'apply settings': c.applyConfig,
        'open LeoConfig.leo': c.leoConfig,
        'open LeoDocs.leo': c.leoDocumentation,
        'open online home': c.leoHome,
        'open online tutorial': c.leoTutorial,
        'open compare window': c.openCompareWindow,
        'open Python window': c.openPythonWindow,
        "equal sized panes": f.equalSizedPanes,
        "toggle active pane": f.toggleActivePane,
        "toggle split direction": f.toggleSplitDirection,
        "resize to screen": f.resizeToScreen,
        "cascade": f.cascade,
        "minimize all": f.minimizeAll,
    }

    for z in commands.keys():
        #z2 = 'leo-%s' % z -- no need to do this, Leos command names dont clash with temacs so far
        emacs.extendAltX(z,commands[z])

    leocommandnames = commands.keys()
#@nonl
#@-node:ekr.20050724074642.39:addLeoCommands  (createBindings)
#@-node:ekr.20050724074642.25:createBindings & helpers  (Creates Emacs instance)
#@-node:ekr.20050724074642.23:Overridden methods
#@-node:ekr.20050724074619.1:Birth (From usetemacs)
#@+node:ekr.20050724075352.13:Helper classes
#@+others
#@+node:ekr.20050724075352.14:class ControlXHandler
class ControlXHandler:

    '''The ControlXHandler manages how the Control-X based commands operate on the
       Emacs instance.'''    
    
    #@    @+others
    #@+node:ekr.20050724075352.15:__init__
    def __init__( self, emacs ):
            
        self.emacs = emacs
        self.previous = []
        self.rect_commands = {
            'o': emacs.openRectangle,
            'c': emacs.clearRectangle,
            't': emacs.stringRectangle,
            'y': emacs.yankRectangle,
            'd': emacs.deleteRectangle,
            'k': emacs.killRectangle,
            'r': emacs.activateRectangleMethods,             
        }
        
        self.variety_commands = {
            'period': emacs.setFillPrefix,
            'parenleft': emacs.startKBDMacro,
            'parenright' : emacs.stopKBDMacro,
            'semicolon': emacs.setCommentColumn,
            'Tab': emacs.tabIndentRegion,
            'u': lambda event: emacs.doUndo( event, 2 ),
            'equal': emacs.lineNumber,
            'h': emacs.selectAll,
            'f': emacs.setFillColumn,
            'b': lambda event, which = 'switch-to-buffer': emacs.setInBufferMode( event, which ),
            'k': lambda event, which = 'kill-buffer': emacs.setInBufferMode( event, which ),
        }
        
        self.abbreviationDispatch = {    
            'a': lambda event: emacs.abbreviationDispatch( event, 1 ),
            'a i': lambda event: emacs.abbreviationDispatch( event, 2 ),    
        }
        
        self.register_commands ={    
            1: emacs.registerCommands.setNextRegister,
            2: emacs.registerCommands.executeRegister,        
        }
    #@nonl
    #@-node:ekr.20050724075352.15:__init__
    #@+node:ekr.20050724075352.16:__call__
    def __call__ (self,event,stroke):
        
        self.previous.insert(0,event.keysym)
        emacs = self.emacs 
        if len(self.previous)>10:self.previous.pop()
        if stroke in('<Key>','<Escape>'):
            return self.processKey(event)
        if stroke in emacs.xcommands:
            emacs.xcommands[stroke](event)
            if stroke!='<Control-b>':emacs.keyboardQuit(event)
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.16:__call__
    #@+node:ekr.20050724075352.17:processKey
    def processKey( self, event ):
            
        emacs = self.emacs 
        previous = self.previous
        if event.keysym in ( 'Shift_L', 'Shift_R' ):
            return
            
        if emacs.sRect:
            return emacs.stringRectangle( event )
            
        if ( event.keysym == 'r' and emacs.rectanglemode == 0 ) and not emacs.registermode:
            return self.processRectangle( event )
    
        if self.rect_commands.has_key( event.keysym ) and emacs.rectanglemode == 1:
            return self.processRectangle( event )
            
        if self.register_commands.has_key( emacs.registermode ):
            self.register_commands[ emacs.registermode ]( event )
            return 'break'
        
        if self.variety_commands.has_key( event.keysym ):
            emacs.stopControlX( event )
            return self.variety_commands[ event.keysym ]( event )
    
        if event.keysym in ( 'a', 'i' , 'e'):
            if self.processAbbreviation( event ): return 'break'
    
        if event.keysym == 'g':
            svar, label = emacs.getSvarLabel( event )
            l = svar.get()
            if self.abbreviationDispatch.has_key( l ):
                emacs.stopControlX( event )
                return self.abbreviationDispatch[ l ]( event )
    
        if event.keysym == 'e':
            emacs.stopControlX( event )
            return emacs.executeLastMacro( event )
    
        if event.keysym == 'x' and previous[ 1 ] not in ( 'Control_L', 'Control_R'):
            event.keysym = 's' 
            emacs.setNextRegister( event )
            return 'break'
        
        if event.keysym == 'Escape':
            if len( previous ) > 1:
                if previous[ 1 ] == 'Escape':
                    return emacs.repeatComplexCommand( event )
    #@nonl
    #@-node:ekr.20050724075352.17:processKey
    #@+node:ekr.20050724075352.18:processRectangle
    def processRectangle( self, event ):
        
        self.rect_commands[ event.keysym ]( event )
        return 'break'
        #if event.keysym == 'o':
        #    emacs.openRectangle( event )
        #    return 'break'
        #if event.keysym == 'c':
        #    emacs.clearRectangle( event )
        #    return 'break'
        #if event.keysym == 't':
        #    emacs.stringRectangle( event )
        #    return 'break'
        #if event.keysym == 'y':
        #    emacs.yankRectangle( event )
        #    return 'break'
        #if event.keysym == 'd':
        #    emacs.deleteRectangle( event )
        #    return 'break'
        #if event.keysym == 'k':
        #    emacs.killRectangle( event )
        #    return 'break'
    #@nonl
    #@-node:ekr.20050724075352.18:processRectangle
    #@+node:ekr.20050724075352.19:processAbbreviation
    def processAbbreviation( self, event ):
        
        emacs = self.emacs
        svar, label = emacs.getSvarLabel( event )
    
        if svar.get() != 'a' and event.keysym == 'a':
            svar.set( 'a' )
            return 'break'
    
        elif svar.get() == 'a':
            if event.char == 'i':
                svar.set( 'a i' )
            elif event.char == 'e':
                emacs.stopControlX( event )
                event.char = ''
                emacs.expandAbbrev( event )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.19:processAbbreviation
    #@-others
#@nonl
#@-node:ekr.20050724075352.14:class ControlXHandler
#@+node:ekr.20050724075352.20:class MC_StateManager
class MC_StateManager:
    
    '''MC_StateManager manages the state that the Emacs instance has entered and
       routes key events to the right method, dependent upon the state in the MC_StateManager'''
       
    #@    @+others
    #@+node:ekr.20050724075352.21:__init__
    def __init__( self, emacs ):
            
        self.emacs = emacs
        self.state = None
        self.states = {}
    #@nonl
    #@-node:ekr.20050724075352.21:__init__
    #@+node:ekr.20050724075352.23:__call__
    def __call__( self, *args ):
            
        if self.state:
            which = self.stateCommands[ self.state ]
            
            # EKR: which[0] is a flag: 1 == one parameter, 2 == all
            # EKR: which[1] is the function.
            
            if which[ 0 ] == 1:
                return which[ 1 ]( args[ 0 ] )
            else:
                return which[ 1 ]( *args )
    #@nonl
    #@-node:ekr.20050724075352.23:__call__
    #@+node:ekr.20050725112958:setStateCommands
    def setStateCommands (self):
        
        emacs = self.emacs
        
        # EKR: used only below.
        def eA( event ):
            if self.emacs.expandAbbrev( event ) :
                return 'break'
        
        self.stateCommands = { #1 == one parameter, 2 == all
            'uC': ( 2, emacs.universalDispatch ),
            'controlx': ( 2, emacs.doControlX ),
            'isearch':( 2, emacs.searchCommands.iSearch ), ###
            'goto': ( 1, emacs.Goto ),
            'zap': ( 1, emacs.zapTo ),
            'howM': ( 1, emacs.howMany ),
            'abbrevMode': ( 1, emacs.abbrevCommands.abbrevCommand1 ), ###
            'altx': ( 1, emacs.doAlt_X ),
            'qlisten': ( 1, emacs.masterQR ),
            'rString': ( 1, emacs.replaceString ),
            'negativeArg':( 2, emacs.negativeArgument ),
            'abbrevOn': ( 1, eA ),
            'set-fill-column': ( 1, emacs.setFillColumn ),
            'chooseBuffer': ( 1, emacs.chooseBuffer ),
            'renameBuffer': ( 1, emacs.renameBuffer ),
            're_search': ( 1, emacs.searchCommands.re_search ), ###
            'alterlines': ( 1, emacs.processLines ),
            'make_directory': ( 1, emacs.makeDirectory ),
            'remove_directory': ( 1, emacs.removeDirectory ),
            'delete_file': ( 1, emacs.deleteFile ),
            'nonincr-search': ( 2, emacs.searchCommands.nonincrSearch ),
            'word-search':( 1, emacs.searchCommands.wordSearch ),
            'last-altx': ( 1, emacs.executeLastAltX ),
            'escape': ( 1, emacs.watchEscape ),
            'subprocess': ( 1, emacs.subprocesser ),
            }
        
    #@nonl
    #@-node:ekr.20050725112958:setStateCommands
    #@+node:ekr.20050724075352.24:setState
    def setState( self, state, value ):
            
        self.state = state
        self.states[ state ] = value
    #@nonl
    #@-node:ekr.20050724075352.24:setState
    #@+node:ekr.20050724075352.25:getState
    def getState( self, state ):
        
        return self.states.get(state,False)
    #@nonl
    #@-node:ekr.20050724075352.25:getState
    #@+node:ekr.20050724075352.26:hasState
    def hasState( self ):
    
        if self.state:
            return self.states[ self.state ]
    #@nonl
    #@-node:ekr.20050724075352.26:hasState
    #@+node:ekr.20050724075352.27:whichState
    def whichState( self ):
        
        return self.state
    #@nonl
    #@-node:ekr.20050724075352.27:whichState
    #@+node:ekr.20050724075352.28:clear
    def clear( self ):
            
        self.state = None
    
        for z in self.states.keys():
            self.states[ z ] = False
    #@nonl
    #@-node:ekr.20050724075352.28:clear
    #@-others
#@nonl
#@-node:ekr.20050724075352.20:class MC_StateManager
#@+node:ekr.20050724075352.29:class MC_KeyStrokeManager  (hard-coded keystrokes)
class MC_KeyStrokeManager:
    
    #@    @+others
    #@+node:ekr.20050724075352.30:__init__
    def __init__( self, emacs ):
        
        self.emacs = emacs
        
        #@    <<keystrokes>>
        #@+node:ekr.20050724075352.31:<<keystrokes>> (hard-coded keystrokes)
        self.keystrokes = {
            '<Control-s>': ( 2, emacs.searchCommands.startIncremental ), ###
            '<Control-r>': ( 2, emacs.searchCommands.startIncremental ), ###
            '<Alt-g>': ( 1, emacs.startGoto ),
            '<Alt-z>': ( 1, emacs.startZap ),
            '<Alt-percent>': ( 1,  emacs.masterQR ) ,
            '<Control-Alt-w>': ( 1, lambda event: 'break' ),
        }
        #@nonl
        #@-node:ekr.20050724075352.31:<<keystrokes>> (hard-coded keystrokes)
        #@nl
    #@nonl
    #@-node:ekr.20050724075352.30:__init__
    #@+node:ekr.20050724075352.32:__call__
    def __call__ (self,event,stroke):
        
        kstroke = self.keystrokes[stroke]
        numberOfArgs, func = self.keystrokes[stroke]
        
        if numberOfArgs==1:
            return func(event)
        else:
            return func(event,stroke)
    #@nonl
    #@-node:ekr.20050724075352.32:__call__
    #@+node:ekr.20050724075352.33:hasKeyStroke
    def hasKeyStroke (self,stroke):
        
        return self.keystrokes.has_key(stroke)
    #@nonl
    #@-node:ekr.20050724075352.33:hasKeyStroke
    #@-others
#@nonl
#@-node:ekr.20050724075352.29:class MC_KeyStrokeManager  (hard-coded keystrokes)
#@+node:ekr.20050724075352.34:class Tracker ( an iterator)
class Tracker:

    '''A class designed to allow the user to cycle through a list
       and to change the list as deemed appropiate.'''

    #@    @+others
    #@+node:ekr.20050724075352.35:init
    def __init__ (self):
        
        self.tablist = []
        self.prefix = None 
        self.ng = self._next()
    #@nonl
    #@-node:ekr.20050724075352.35:init
    #@+node:ekr.20050724075352.36:setTabList
    def setTabList (self,prefix,tlist):
        
        self.prefix = prefix 
        self.tablist = tlist 
    #@nonl
    #@-node:ekr.20050724075352.36:setTabList
    #@+node:ekr.20050724075352.37:_next
    def _next (self):
        
        while 1:
            tlist = self.tablist 
            if not tlist:yield ''
            for z in self.tablist:
                if tlist!=self.tablist:
                    break 
                yield z 
    #@nonl
    #@-node:ekr.20050724075352.37:_next
    #@+node:ekr.20050724075352.38:next
    def next (self):
        
        return self.ng.next()
    #@nonl
    #@-node:ekr.20050724075352.38:next
    #@+node:ekr.20050724075352.39:clear
    def clear (self):
    
        self.tablist = []
        self.prefix = None
    #@nonl
    #@-node:ekr.20050724075352.39:clear
    #@-others
#@nonl
#@-node:ekr.20050724075352.34:class Tracker ( an iterator)
#@-others
#@nonl
#@-node:ekr.20050724075352.13:Helper classes
#@+node:ekr.20050724075352.40:class Emacs
class Emacs:
    
    '''A class to support emacs commands.  Creates a Tk Text widget for the minibufer.'''

    # Define class vars...
    global_killbuffer = []
        # Used only if useGlobalKillbuffer arg to Emacs ctor is True.
        # Otherwise, each Emacs instance has its own local kill buffer.

    global_registers = {}
        # Used only if useGlobalRegisters arg to Emacs ctor is True.
        # Otherwise each Emacs instance has its own set of registers.

    lossage = []
        # A case could be made for per-instance lossage, but this is not supported.

    #@    @+others
    #@+node:ekr.20050724075352.41:Emacs.__init__
    def __init__ (self,c,tbuffer=None,minibuffer=None,useGlobalKillbuffer=False,useGlobalRegisters=False):
        '''Sets up Emacs instance.
        
        Use tbuffer (a Tk Text widget) and minibuffer (a Tk Label) if provided.
        Otherwise, the caller must call setBufferStrokes.
        
        useGlobalRegisters and useGlobalKillbuffer indicate whether to use
        global (class vars) or per-instance (ivars) for kill buffers and registers.'''
        
        self.c = c
        self.useGlobalKillbuffer = useGlobalKillbuffer
        self.useGlobalRegisters = useGlobalRegisters
    
        #@    << init general ivars >>
        #@+node:ekr.20050725123449:<< init general ivars >>
        self.mbuffers ={}
        self.svars ={}
        self.tailEnds ={} # functions to execute at the end of many Emac methods.  Configurable by environment.
        self.undoers ={} # Emacs instance tracks undoers given to it.
        self.store ={'rlist':[], 'stext':''}
        self.shutdownhook = None # If this is set via setShutdownHook, it is executed instead of sys.exit when Control-x Control-c is fired
        self.shuttingdown = False # Indicates that the Emacs instance is shutting down and no work needs to be done.
        self.swapSpots =[]
        self.ccolumn = '0'
        self.reset = False 
        self.previousStroke = ''
        
        # For communication between keystroke handlers and other classes.
        self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
        self.regXKey = None
        #@nonl
        #@-node:ekr.20050725123449:<< init general ivars >>
        #@nl
    
        # Create helper classes.  Order is important here...
        self.mcStateManager = MC_StateManager(self) # Manages state for the master command
        self.createCommandsClasses()
        self.kstrokeManager = MC_KeyStrokeManager(self) # Manages some keystroke state for the master command.
        self.mcStateManager.setStateCommands() # Do this after defining command classes.
        
        # Macros...
        self.lastMacro = None 
        self.macs =[]
        self.macro =[]
        self.namedMacros ={}
        self.macroing = False 
        self.dynaregex = re.compile(r'[%s%s\-_]+'%(string.ascii_letters,string.digits))#for dynamic abbreviations
        self.altx_history =[]
        self.keysymhistory =[]
        
        # This section sets up the buffer data structures
        self.bufferListGetters ={}
        self.bufferSetters ={}
        self.bufferGotos ={}
        self.bufferDeletes ={}
        self.renameBuffers ={}
        self.bufferDict = None 
        self.bufferTracker = Tracker()
        self.bufferCommands ={
            'append-to-buffer': self.appendToBuffer, 
            'prepend-to-buffer':self.prependToBuffer, 
            'copy-to-buffer':   self.copyToBuffer, 
            'insert-buffer':    self.insertToBuffer, 
            'switch-to-buffer': self.switchToBuffer, 
             'kill-buffer':     self.killBuffer, 
        }
        
        self.fillPrefix = ''#for fill prefix functions
        self.fillColumn = 70#for line centering
        self.registermode = False #for rectangles and registers
        
        self.sRect = False #State indicating string rectangle.  May be moved to MC_StateManager
        self.krectangle = None #The kill rectangle
        self.rectanglemode = 0#Determines what state the rectangle system is in.
        
        self.last_clipboard = None #For interacting with system clipboard.
        
        self.negativeArg = False
        self.negArgs ={'<Alt-c>':self.changePreviousWord, 
        '<Alt-u>':self.changePreviousWord, 
        '<Alt-l>':self.changePreviousWord}#For negative argument functionality
    
        #Alt-X commands.
        ### Now done in createCommandsClasses
        ### self.doAltX = self.addAltXCommands()
        self.axTabList = Tracker()
        self.x_hasNumeric =['sort-lines', 'sort-fields']
        
        # Command bindings.
        self.cbDict = self.addCallBackDict() # Creates callback dictionary, primarily used in the master command
        self.xcommands = self.addXCommands() # Creates the X commands dictionary
        self.cxHandler = ControlXHandler(self)# Creates the handler for Control-x commands
        
        #These attributes are for the universal command functionality.
        self.uCstring = string.digits+'\b'
        self.uCdict ={'<Alt-x>':self.alt_X}
      
        if tbuffer and minibuffer:
            self.setBufferStrokes(tbuffer,minibuffer)
    #@nonl
    #@-node:ekr.20050724075352.41:Emacs.__init__
    #@+node:ekr.20050724075352.42:getHelpText
    def getHelpText ():
        '''This returns a string that describes what all the
        keystrokes do with a bound Text widget.'''
        help_t =['Buffer Keyboard Commands:', 
        '----------------------------------------\n', 
        '<Control-p>: move up one line', 
        '<Control-n>: move down one line', 
        '<Control-f>: move forward one char', 
        '<Conftol-b>: move backward one char', 
        '<Control-o>: insert newline', 
        '<Control-Alt-o> : insert newline and indent', 
        '<Control-j>: insert newline and tab', 
        '<Alt-<> : move to start of Buffer', 
        '<Alt- >'+' >: move to end of Buffer', 
        '<Control a>: move to start of line', 
        '<Control e> :move to end of line', 
        '<Alt-Up>: move to start of line', 
        '<Alt-Down>: move to end of line', 
        '<Alt b>: move one word backward', 
        '<Alt f> : move one word forward', 
        '<Control - Right Arrow>: move one word forward', 
        '<Control - Left Arrow>: move one word backwards', 
        '<Alt-m> : move to beginning of indentation', 
        '<Alt-g> : goto line number', 
        '<Control-v>: scroll forward one screen', 
        '<Alt-v>: scroll up one screen', 
        '<Alt-a>: move back one sentence', 
        '<Alt-e>: move forward one sentence', 
        '<Alt-}>: move forward one paragraph', 
        '<Alt-{>: move backwards one paragraph', 
        '<Alt-:> evaluate a Python expression in the minibuffer and insert the value in the current buffer', 
        'Esc Esc : evaluate a Python expression in the minibuffer and insert the value in the current buffer', 
        '<Control-x . >: set fill prefix', 
        '<Alt-q>: fill paragraph', 
        '<Alt-h>: select current or next paragraph', 
        '<Control-x Control-@>: pop global mark', 
        '<Control-u>: universal command, repeats the next command n times.', 
        '<Alt -n > : n is a number.  Processes the next command n times.', 
        '<Control-x (>: start definition of kbd macro', 
        '<Control-x ) > : stop definition of kbd macro', 
        '<Control-x e : execute last macro defined', 
        '<Control-u Control-x ( >: execute last macro and edit', 
        '<Control-x Esc Esc >: execute last complex command( last Alt-x command', 
        '<Control-x Control-c >: save buffers kill Emacs', 
        '''<Control-x u > : advertised undo.   This function utilizes the environments.
        If the buffer is not configure explicitly, there is no operation.''', 
        '<Control-_>: advertised undo.  See above', 
        '<Control-z>: iconfify frame', 
        '----------------------------------------\n', 
        '<Delete> : delete previous character', 
        '<Control d>: delete next character', 
        '<Control k> : delete from cursor to end of line. Text goes to kill buffer', 
        '<Alt d>: delete word. Word goes to kill buffer', 
        '<Alt Delete>: delete previous word. Word goes to kill buffer', 
        '<Alt k >: delete current sentence. Sentence goes to kill buffer', 
        '<Control x Delete>: delete previous sentence. Sentence goes to kill buffer', 
        '<Control y >: yank last deleted text segment from\n kill buffer and inserts it.', 
        '<Alt y >: cycle and yank through kill buffer.\n', 
        '<Alt z >: zap to typed letter. Text goes to kill buffer', 
        '<Alt-^ >: join this line to the previous one', 
        '<Alt-\ >: delete surrounding spaces', 
        '<Alt-s> >: center line in current fill column', 
        '<Control-Alt-w>: next kill is appended to kill buffer\n'
        
        '----------------------------------------\n', 
        '<Alt c>: Capitalize the word the cursor is under.', 
        '<Alt u>: Uppercase the characters in the word.', 
        '<Alt l>: Lowercase the characters in the word.', 
        '----------------------------------------\n', 
        '<Alt t>: Mark word for word swapping.  Marking a second\n word will swap this word with the first', 
        '<Control-t>: Swap characters', 
        '<Ctrl-@>: Begin marking region.', 
        '<Ctrl-W>: Kill marked region', 
        '<Alt-W>: Copy marked region', 
        '<Ctrl-x Ctrl-u>: uppercase a marked region', 
        '<Ctrl-x Ctrl-l>: lowercase a marked region', 
        '<Ctrl-x h>: mark entire buffer', 
        '<Alt-Ctrl-backslash>: indent region to indentation of line 1 of the region.', 
        '<Ctrl-x tab> : indent region by 1 tab', 
        '<Control-x Control-x> : swap point and mark', 
        '<Control-x semicolon>: set comment column', 
        '<Alt-semicolon>: indent to comment column', 
        '----------------------------------------\n', 
        'M-! cmd -- Run the shell command line cmd and display the output', 
        'M-| cmd -- Run the shell command line cmd with region contents as input', 
        '----------------------------------------\n', 
        '<Control-x a e>: Expand the abbrev before point (expand-abbrev), even when Abbrev mode is not enabled', 
        '<Control-x a g>: Define an abbreviation for previous word', 
        '<Control-x a i g>: Define a word as abbreviation for word before point, or in point', 
        '----------------------------------------\n', 
        '<Control s>: forward search, using pattern in Mini buffer.\n', 
        '<Control r>: backward search, using pattern in Mini buffer.\n', 
        '<Control s Enter>: search forward for a word, nonincremental\n', 
        '<Control r Enter>: search backward for a word, nonincremental\n', 
        '<Control s Enter Control w>: Search for words, ignoring details of punctuation', 
        '<Control r Enter Control w>: Search backward for words, ignoring details of punctuation', 
        '<Control-Alt s>: forward regular expression search, using pattern in Mini buffer\n', 
        '<Control-Alt r>: backward regular expression search, using pattern in Mini buffer\n', 
        '''<Alt-%>: begin query search/replace. n skips to next match. y changes current match.  
        q or Return exits. ! to replace all remaining matches with no more questions''', 
        '''<Control Alt %> begin regex search replace, like Alt-%''', 
        '<Alt-=>: count lines and characters in regions', 
        '<Alt-( >: insert parentheses()', 
        '<Alt-) >:  move past close', 
        '<Control-x Control-t>: transpose lines.', 
        '<Control-x Control-o>: delete blank lines', 
        '<Control-x r s>: save region to register', 
        '<Control-x r i>: insert to buffer from register', 
        '<Control-x r +>: increment register', 
        '<Control-x r n>: insert number 0 to register', 
        '<Control-x r space > : point insert point to register', 
        '<Control-x r j > : jump to register', 
        '<Control-x x>: save region to register', 
        '<Control-x r r> : save rectangle to register', 
        '<Control-x r o>: open up rectangle', 
        '<Control-x r c> : clear rectangle', 
        '<Control-x r d> : delete rectangle', 
        '<Control-x r t> : replace rectangle with string', 
        '<Control-x r k> : kill rectangle', 
        '<Control-x r y> : yank rectangle', 
        '<Control-g> : keyboard quit\n', 
        '<Control-x = > : position of cursor', 
        '<Control-x . > : set fill prefix', 
        '<Control-x f > : set the fill column', 
        '<Control-x Control-b > : display the buffer list', 
        '<Control-x b > : switch to buffer', 
        '<Control-x k > : kill the specified buffer', 
        '----------------------------------------\n', 
        '<Alt - - Alt-l >: lowercase previous word', 
        '<Alt - - Alt-u>: uppercase previous word', 
        '<Alt - - Alt-c>: capitalise previous word', 
        '----------------------------------------\n', 
        '<Alt-/ >: dynamic expansion', 
        '<Control-Alt-/>: dynamic expansion.  Expands to common prefix in buffer\n'
        '----------------------------------------\n', 
        'Alt-x commands:\n', 
        '(Pressing Tab will result in auto completion of the options if an appropriate match is found', 
        'replace-string  -  replace string with string', 
        'replace-regex - replace python regular expression with string', 
        'append-to-register  - append region to register', 
        'prepend-to-register - prepend region to register\n'
        'sort-lines - sort selected lines', 
        'sort-columns - sort by selected columns', 
        'reverse-region - reverse selected lines', 
        'sort-fields  - sort by fields', 
        'abbrev-mode - toggle abbrev mode on/off', 
        'kill-all-abbrevs - kill current abbreviations', 
        'expand-region-abbrevs - expand all abrevs in region', 
        'read-abbrev-file - read abbreviations from file', 
        'write-abbrev-file - write abbreviations to file', 
        'list-abbrevs   - list abbrevs in minibuffer', 
        'fill-region-as-paragraph - treat region as one paragraph and add fill prefix', 
        'fill-region - fill paragraphs in region with fill prefix', 
        'close-rectangle  - close whitespace rectangle', 
        'how-many - counts occurances of python regular expression', 
        'kill-paragraph - delete from cursor to end of paragraph', 
        'backward-kill-paragraph - delete from cursor to start of paragraph', 
        'backward-kill-sentence - delete from the cursor to the start of the sentence', 
        'name-last-kbd-macro - give the last kbd-macro a name', 
        'insert-keyboard-macro - save macros to file', 
        'load-file - load a macro file', 
        'kill-word - delete the word the cursor is on', 
        'kill-line - delete form the cursor to end of the line', 
        'kill-sentence - delete the sentence the cursor is on', 
        'kill-region - delete a marked region', 
        'yank - restore what you have deleted', 
        'backward-kill-word - delete previous word', 
        'backward-delete-char - delete previous character', 
        'delete-char - delete character under cursor', 
        'isearch-forward - start forward incremental search', 
        'isearch-backward - start backward incremental search', 
        'isearch-forward-regexp - start forward regular expression incremental search', 
        'isearch-backward-regexp - start backward return expression incremental search', 
        'capitalize-word - capitalize the current word', 
        'upcase-word - switch word to upper case', 
        'downcase-word - switch word to lower case', 
        'indent-region - indent region to first line in region', 
        'indent-rigidly - indent region by a tab', 
        'indent-relative - Indent from point to under an indentation point in the previous line', 
        'set-mark-command - mark the beginning or end of a region', 
         'kill-rectangle - kill the rectangle', 
        'delete-rectangle - delete the rectangle', 
        'yank-rectangle - yank the rectangle', 
        'open-rectangle - open the rectangle', 
        'clear-rectangle - clear the rectangle', 
        'copy-to-register - copy selection to register', 
        'insert-register - insert register into buffer', 
        'copy-rectangle-to-register - copy buffer rectangle to register', 
        'jump-to-register - jump to position in register', 
        'point-to-register - insert point into register', 
        'number-to-register - insert number into register', 
        'increment-register - increment number in register', 
        'view-register - view what register contains', 
        'beginning-of-line - move to the beginning of the line', 
        'end-of-line - move to the end of the line', 
        'beginning-of-buffer - move to the beginning of the buffer', 
        'end-of-buffer - move to the end of the buffer', 
        'newline-and-indent - insert a newline and tab', 
        'keyboard-quit - abort current command', 
        'iconify-or-deiconify-frame - iconfiy current frame', 
        'advertised-undo - undo the last operation', 
        'back-to-indentation - move to first non-blank character of line', 
        'delete-indentation - join this line to the previous one', 
        'view-lossage - see the last 100 characters typed', 
        'transpose-chars - transpose two letters', 
        'transpose-words - transpose two words', 
        'transpose-line - transpose two lines', 
        'flush-lines - delete lines that match regex', 
        'keep-lines - keep lines that only match regex', 
        'insert-file - insert file at current position', 
        'save-buffer - save file', 
        'split-line - split line at cursor. indent to column of cursor', 
        'upcase-region - Upper case region', 
        'downcase-region - lower case region', 
        'goto-line - goto a line in the buffer', 
        'what-line - display what line the cursor is on', 
        'goto-char - goto a char in the buffer', 
        'set-fill-column - sets the fill column', 
        'center-line - centers the current line within the fill column', 
        'center-region - centers the current region within the fill column', 
        'forward-char - move the cursor forward one char', 
        'backward-char - move the cursor backward one char', 
        'previous-line - move the cursor up one line', 
        'next-line - move the cursor down one line', 
        'universal-argument - Repeat the next command "n" times', 
        'digit-argument - Repeat the next command "n" times', 
        'set-fill-prefix - Sets the prefix from the insert point to the start of the line', 
        'scroll-up - scrolls up one screen', 
        'scroll-down - scrolls down one screen', 
        'append-to-buffer - Append region to a specified buffer', 
        'prepend-to-buffer - Prepend region to a specified buffer', 
        'copy-to-buffer - Copy region to a specified buffer, deleting the previous contents', 
        'insert-buffer - Insert the contents of a specified buffer into current buffer at point', 
        'list-buffers - Display the buffer list', 
        'switch-to-buffer - switch to a different buffer, if it does not exits, it is created.', 
        'kill-buffer - kill the specified buffer', 
        'rename-buffer - rename the buffer', 
        'query-replace - query buffer for pattern and replace it.  The user will be asked for a pattern, and for text to replace the pattern with.', 
        'query-replace-regex - query buffer with regex and replace it.  The user will be asked for a pattern, and for text to replace the regex matches with.', 
        'inverse-add-global-abbrev - add global abbreviation from previous word.  Will ask user for word to expand to', 
        'expand-abbrev - Expand the abbrev before point. This is effective even when Abbrev mode is not enabled', 
        're-search-forward - do a python regular expression search forward', 
        're-search-backward - do a python regular expression search backward', 
        'diff - compares two files, displaying the differences in an Emacs buffer named *diff*', 
        'make-directory - create a new directory', 
        'remove-directory - remove an existing directory if its empty', 
        'delete-file - remove an existing file', 
        'search-forward - search forward for a word', 
        'search-backward - search backward for a word', 
        'word-search-forward - Search for words, ignoring details of punctuation.', 
        'word-search-backward - Search backward for words, ignoring details of punctuation', 
        'repeat-complex-command - repeat the last Alt-x command', 
        'eval-expression - evaluate a Python expression and put the value in the current buffer', 
        'tabify - turn the selected text\'s spaces into tabs', 
        'untabify - turn the selected text\'s tabs into spaces', 
        'shell-command -Run the shell command line cmd and display the output', 
        'shell-command-on-region -Run the shell command line cmd with region contents as input', 
        ]
        
        return '\n'.join(help_t)
    
    getHelpText = staticmethod(getHelpText)
    #@nonl
    #@-node:ekr.20050724075352.42:getHelpText
    #@+node:ekr.20050725094519:createCommandsClasses
    def createCommandsClasses (self):
        
        self.commandClasses = [
            ('searchCommands',      self.searchCommandsClass),
            ('killBufferCommands',  self.killBufferCommandsClass),
            ('abbrevCommands',      self.abbrevCommandsClass),
            ('registerCommands',    self.registerCommandsClass),
        ]
        
        # Create the initial table.  (This may go away).
        self.doAltX = self.addAltXCommands()
    
        for name, theClass in self.commandClasses:
            theInstance = theClass(self)# Create the class.
            setattr(self,name,theInstance)
            # g.trace(getattr(self,name))
            d = theInstance.getPublicCommands()
            if d:
                self.doAltX.update(d)
                if 1:
                    keys = d.keys()
                    keys.sort()
                    print '----- adding from %s ----' % name
                    for key in keys: print key
    #@nonl
    #@-node:ekr.20050725094519:createCommandsClasses
    #@+node:ekr.20050724075352.43:masterCommand
    def masterCommand( self, event, method , stroke):
        '''The masterCommand is the central routing method of the Emacs method.
           All commands and keystrokes pass through here.'''
           
        special = event.keysym in ('Control_L','Control_R','Alt_L','Alt-R','Shift_L','Shift_R')
        inserted = not special or len(self.keysymhistory) == 0 or self.keysymhistory[0] != event.keysym
    
        # Don't add multiple special characters to history.
        if inserted:
            self.keysymhistory.insert(0,event.keysym)
            if len(event.char) > 0:
                if len(Emacs.lossage) > 99: Emacs.lossage.pop()
                Emacs.lossage.insert(0,event.char)
            
            if 0: # traces
                g.trace(event.keysym,stroke)
                #g.trace(self.keysymhistory)
                #g.trace(Emacs.lossage)
    
        if self.macroing:
            if self.macroing == 2 and stroke != '<Control-x>':
                return self.nameLastMacro( event )
            elif self.macroing == 3 and stroke != '<Control-x>':
                return self.getMacroName( event )
            else:
               self.recordKBDMacro( event, stroke )
             
        if  stroke == '<Control-g>':
            self.previousStroke = stroke
            return self.keyboardQuit( event )
            
        if self.mcStateManager.hasState():
            self.previousStroke = stroke
            return self.mcStateManager( event, stroke ) # EKR: Invoke the __call__ method.
            
        if self.kstrokeManager.hasKeyStroke( stroke ):
            self.previousStroke = stroke
            return self.kstrokeManager( event, stroke ) # EKR: Invoke the __call__ method.
    
        if self.regXRpl: # EKR: a generator.
            try:
                self.regXKey = event.keysym
                self.regXRpl.next() # EKR: next() may throw StopIteration.
            finally:
                return 'break'
    
        if self.abbrevOn:
            if self._expandAbbrev( event ) :
                return 'break'       
    
        if method:
            rt = method( event )
            self.previousStroke = stroke
            return rt
    #@nonl
    #@-node:ekr.20050724075352.43:masterCommand
    #@+node:ekr.20050724075352.47:keyboardQuit
    def keyboardQuit( self, event ):
        
        '''This method cleans the Emacs instance of state and ceases current operations.'''
    
        return self.stopControlX( event ) # This method will eventually contain the stopControlX code.
    #@nonl
    #@-node:ekr.20050724075352.47:keyboardQuit
    #@+node:ekr.20050724075352.48:add command dictionary methods
    #@+at
    # These methods create the dispatch dictionarys for keystrokes and 
    # commands.
    # 
    # Dont mess with it if you dont understand this section.
    #@-at
    #@nonl
    #@+node:ekr.20050724075352.49:addCallBackDict (creates cbDict)
    def addCallBackDict( self ):
        
    
        '''This method adds a dictionary to the Emacs instance through which the masterCommand can
           call the specified method.'''
    
        cbDict = {
        'Alt-less' : lambda event, spot = '1.0' : self.moveTo( event, spot ),
        'Alt-greater': lambda event, spot = 'end' : self.moveTo( event, spot ),
        'Control-Right': lambda event, way = 1: self.moveword( event, way ),
        'Control-Left': lambda event, way = -1: self.moveword( event, way ),
        'Control-a': lambda event, spot = 'insert linestart': self.moveTo( event, spot ),
        'Control-e': lambda event, spot = 'insert lineend': self.moveTo( event, spot ),
        'Alt-Up': lambda event, spot = 'insert linestart': self.moveTo( event, spot ),
        'Alt-Down': lambda event, spot = 'insert lineend': self.moveTo( event, spot ),
        'Alt-f': lambda event, way = 1: self.moveword( event, way ),
        'Alt-b' : lambda event, way = -1: self.moveword( event, way ),
        'Control-o': self.insertNewLine,
        'Control-k': lambda event, frm = 'insert', to = 'insert lineend': self.kill( event, frm, to) ,
        'Alt-d': lambda event, frm = 'insert wordstart', to = 'insert wordend': self.kill( event,frm, to ),
        'Alt-Delete': lambda event: self.deletelastWord( event ),
        "Control-y": lambda event, frm = 'insert', which = 'c': self.walkKB( event, frm, which),
        "Alt-y": lambda event , frm = "insert", which = 'a': self.walkKB( event, frm, which ),
        "Alt-k": lambda event : self.killsentence( event ),
        'Control-s' : None,
        'Control-r' : None,
        'Alt-c': lambda event, which = 'cap' : self.capitalize( event, which ),
        'Alt-u': lambda event, which = 'up' : self.capitalize( event, which ),
        'Alt-l': lambda event, which = 'low' : self.capitalize( event, which ),
        'Alt-t': lambda event, sw = self.swapSpots: self.swapWords( event, sw ),
        'Alt-x': self.alt_X,
        'Control-x': self.startControlX,
        'Control-g': self.keyboardQuit,
        'Control-Shift-at': self.setRegion,
        'Control-w': lambda event, which = 'd' :self.killRegion( event, which ),
        'Alt-w': lambda event, which = 'c' : self.killRegion( event, which ),
        'Control-t': self.swapCharacters,
        'Control-u': None,
        'Control-l': None,
        'Alt-z': None,
        'Control-i': None,
        'Alt-Control-backslash': self.indentRegion,
        'Alt-m' : self.backToIndentation,
        'Alt-asciicircum' : self.deleteIndentation,
        'Control-d': self.deleteNextChar,
        'Alt-backslash': self.deleteSpaces, 
        'Alt-g': None,
        'Control-v' : lambda event, way = 'south': self.screenscroll( event, way ),
        'Alt-v' : lambda event, way = 'north' : self.screenscroll( event, way ),
        'Alt-equal': self.countRegion,
        'Alt-parenleft': self.insertParentheses,
        'Alt-parenright': self.movePastClose,
        'Alt-percent' : None,
        'Control-c': None,
        'Delete': lambda event, which = 'BackSpace': self.manufactureKeyPress( event, which ),
        'Control-p': lambda event, which = 'Up': self.manufactureKeyPress( event, which ),
        'Control-n': lambda event, which = 'Down': self.manufactureKeyPress( event, which ),
        'Control-f': lambda event, which = 'Right':self.manufactureKeyPress( event, which ),
        'Control-b': lambda event, which = 'Left': self.manufactureKeyPress( event, which ),
        'Control-Alt-w': None,
        'Alt-a': lambda event, which = 'bak': self.prevNexSentence( event, which ),
        'Alt-e': lambda event, which = 'for': self.prevNexSentence( event, which ),
        'Control-Alt-o': self.insertNewLineIndent,
        'Control-j': self.insertNewLineAndTab,
        'Alt-minus': self.negativeArgument,
        'Alt-slash': self.dynamicExpansion,
        'Control-Alt-slash': self.dynamicExpansion2,
        'Control-u': lambda event, keystroke = '<Control-u>': self.universalDispatch( event, keystroke ),
        'Alt-braceright': lambda event, which = 1: self.movingParagraphs( event, which ),
        'Alt-braceleft': lambda event , which = 0: self.movingParagraphs( event, which ),
        'Alt-q': self.fillParagraph,
        'Alt-h': self.selectParagraph,
        'Alt-semicolon': self.indentToCommentColumn,
        'Alt-0': lambda event, stroke = '<Alt-0>', number = 0: self.numberCommand( event, stroke, number ) ,
        'Alt-1': lambda event, stroke = '<Alt-1>', number = 1: self.numberCommand( event, stroke, number ) ,
        'Alt-2': lambda event, stroke = '<Alt-2>', number = 2: self.numberCommand( event, stroke, number ) ,
        'Alt-3': lambda event, stroke = '<Alt-3>', number = 3: self.numberCommand( event, stroke, number ) ,
        'Alt-4': lambda event, stroke = '<Alt-4>', number = 4: self.numberCommand( event, stroke, number ) ,
        'Alt-5': lambda event, stroke = '<Alt-5>', number = 5: self.numberCommand( event, stroke, number ) ,
        'Alt-6': lambda event, stroke = '<Alt-6>', number = 6: self.numberCommand( event, stroke, number ) ,
        'Alt-7': lambda event, stroke = '<Alt-7>', number = 7: self.numberCommand( event, stroke, number ) ,
        'Alt-8': lambda event, stroke = '<Alt-8>', number = 8: self.numberCommand( event, stroke, number ) ,
        'Alt-9': lambda event, stroke = '<Alt-9>', number = 9: self.numberCommand( event, stroke, number ) ,
        'Control-underscore': self.doUndo,
        'Alt-s': self.centerLine,
        'Control-z': self.suspend, 
        'Control-Alt-s': lambda event, stroke='<Control-s>': self.startIncremental( event, stroke, which='regexp' ),
        'Control-Alt-r': lambda event, stroke='<Control-r>': self.startIncremental( event, stroke, which='regexp' ),
        'Control-Alt-percent': lambda event: self.startRegexReplace() and self.masterQR( event ),
        'Escape': self.watchEscape,
        'Alt-colon': self.startEvaluate,
        'Alt-exclam': self.startSubprocess,
        'Alt-bar': lambda event: self.startSubprocess( event, which = 1 ),
        }
        
        return cbDict
    #@nonl
    #@-node:ekr.20050724075352.49:addCallBackDict (creates cbDict)
    #@+node:ekr.20050724075352.50:addXCommands
    def addXCommands( self ):
        
        xcommands = {
            '<Control-t>': self.transposeLines, 
            '<Control-u>': lambda event , way ='up': self.upperLowerRegion( event, way ),
            '<Control-l>':  lambda event , way ='low': self.upperLowerRegion( event, way ),
            '<Control-o>': self.removeBlankLines,
            '<Control-i>': self.insertFile,
            '<Control-s>': self.saveFile,
            '<Control-x>': self.exchangePointMark,
            '<Control-c>': self.shutdown,
            '<Control-b>': self.listBuffers,
            '<Control-Shift-at>': lambda event: event.widget.selection_clear(),
            '<Delete>' : lambda event, back = True: self.killsentence( event, back ),
        }
        
        return xcommands
    #@nonl
    #@-node:ekr.20050724075352.50:addXCommands
    #@+node:ekr.20050724075352.51:addAltXCommands
    def addAltXCommands( self ):
        
        # The various getPublicCommands methods add more entries.
        
        # many of the simpler methods need self.keyboardQuit( event ) appended to the end to stop the Alt-x mode.
        doAltX= {
            #@        << now set by entries in dicts returned by getPublicCommands >>
            #@+node:ekr.20050725132636:<< now set by entries in dicts returned by getPublicCommands >>
            # Abbreviations...
            # 'abbrev-mode': self.toggleAbbrevMode,
            # 'expand-abbrev': self.expandAbbrev,
            # 'kill-all-abbrevs': self.killAllAbbrevs,
            # 'expand-region-abbrevs': self.regionalExpandAbbrev,
            # 'write-abbrev-file': self.writeAbbreviations,
            # 'read-abbrev-file': self.readAbbreviations,
            # 'list-abbrevs': self.listAbbrevs,
            
            # Isearch
            # 'isearch-forward':          self.searchCommands.isearchForward,
            # 'isearch-backward':         self.searchCommands.isearchBackward,
            # 'isearch-forward-regexp':   self.searchCommands.isearchForwardRegexp,
            # 'isearch-backward-regexp':  self.searchCommands.isearchBackwardRegexp,
            
            # Registers
            # 'prepend-to-register': self.prependToRegister,
            # 'append-to-register': self.appendToRegister,
            # 'copy-to-register': lambda event: self.setEvent( event, 's' ) and self.setNextRegister( event ),
            # 'insert-register': lambda event: self.setEvent( event, 'i' ) and self.setNextRegister( event ),
            # 'copy-rectangle-to-register': lambda event: self.setEvent( event, 'r' ) and self.setNextRegister( event ),
            # 'jump-to-register': lambda event: self.setEvent( event, 'j' ) and self.setNextRegister( event ),
            # 'point-to-register': lambda event: self.setEvent( event, 'space' ) and self.setNextRegister( event ),
            # 'number-to-register': lambda event: self.setEvent( event, 'n' ) and self.setNextRegister( event ),
            # 'increment-register': lambda event: self.setEvent( event, 'plus' ) and self.setNextRegister( event ),
            # 'view-register': lambda event: self.setEvent( event, 'view' ) and self.setNextRegister( event ),
            
            # Search
            # 'search-forward': lambda event: self.startNonIncrSearch( event, 'for' ),
            # 'search-backward': lambda event: self.startNonIncrSearch( event, 'bak' ),
            # 'word-search-forward': lambda event : self.startWordSearch( event, 'for' ),
            # 'word-search-backward': lambda event: self.startWordSearch( event, 'bak' ),
            
            # Kill and yank (in kill class)
            # 'backward-kill-sentence': lambda event: self.keyboardQuit( event ) and self.killsentence( event, back = True ),
            # 'backward-kill-word': lambda event: self.deletelastWord( event ) and self.keyboardQuit( event ),
            # 'kill-word': lambda event, frm = 'insert wordstart', to = 'insert wordend': self.kill( event,frm, to ) and self.keyboardQuit( event ),
            # 'kill-line': lambda event, frm = 'insert', to = 'insert lineend': self.kill( event, frm, to) and self.keyboardQuit( event ), 
            # 'kill-sentence': lambda event : self.killsentence( event ) and self.keyboardQuit( event ),
            # 'kill-region': lambda event, which = 'd' :self.killRegion( event, which ) and self.keyboardQuit( event ),
            # 'yank': lambda event, frm = 'insert', which = 'c': self.walkKB( event, frm, which) and self.keyboardQuit( event ),
            # 'yank-pop' : lambda event , frm = "insert", which = 'a': self.walkKB( event, frm, which ) and self.keyboardQuit( event ),
            #@nonl
            #@-node:ekr.20050725132636:<< now set by entries in dicts returned by getPublicCommands >>
            #@nl
            
            'replace-string': self.replaceString,
            'replace-regex': lambda event:  self.activateReplaceRegex() and self.replaceString( event ),
            
            # Sort.
            'sort-lines': self.sortLines,
            'sort-columns': self.sortColumns,
            'reverse-region': self.reverseRegion,
            'sort-fields': self.sortFields,
            
            'fill-region-as-paragraph': self.fillRegionAsParagraph,
            'fill-region': self.fillRegion,
            'close-rectangle': self.closeRectangle,
            
            'how-many': self.startHowMany,
            
            # Macros.
            'name-last-kbd-macro': self.nameLastMacro,
            'load-file': self.loadMacros,
            'insert-keyboard-macro' : self.getMacroName,
            
            # Kill and yank (in paragraph class)
            'backward-kill-paragraph': self.backwardKillParagraph,
            'kill-paragraph': self.killParagraph,
            
            'backward-delete-char':lambda event, which = 'BackSpace': self.manufactureKeyPress( event, which ) and self.keyboardQuit( event ),
            'delete-char': lambda event: self.deleteNextChar( event ) and self.keyboardQuit( event ) ,
            
            # Case
            'capitalize-word': lambda event, which = 'cap' : self.capitalize( event, which ) and self.keyboardQuit( event ),
            'upcase-word': lambda event, which = 'up' : self.capitalize( event, which ) and self.keyboardQuit( event ),
            'downcase-word': lambda event, which = 'low' : self.capitalize( event, which ) and self.keyboardQuit( event ),
            
            # Indent
            'indent-region': lambda event: self.indentRegion( event ) and self.keyboardQuit( event ),
            'indent-rigidly': lambda event: self.tabIndentRegion( event ) and self.keyboardQuit( event ),
            'indent-relative': self.indent_relative,
            
            'set-mark-command': lambda event: self.setRegion( event ) and self.keyboardQuit( event ),
            
            # Rectangle.
            'kill-rectangle': lambda event: self.killRectangle( event ),
            'delete-rectangle': lambda event: self.deleteRectangle( event ),
            'yank-rectangle': lambda event: self.yankRectangle( event ),
            'open-rectangle': lambda event: self.openRectangle( event ),
            'clear-rectangle': lambda event: self.clearRectangle( event ),
            
            'keyboard-quit': lambda event: self.keyboardQuit( event ),
            'advertised-undo': lambda event: self.doUndo( event ) and self.keyboardQuit( event ),
            'view-lossage': lambda event: self.viewLossage( event ),
        
            # Lines & chars.
            'beginning-of-line': lambda event, spot = 'insert linestart': self.moveTo( event, spot ) and self.keyboardQuit( event ),
            'end-of-line': lambda event, spot = 'insert lineend': self.moveTo( event, spot ) and self.keyboardQuit( event ),
            'back-to-indentation': lambda event: self.backToIndentation( event ) and self.keyboardQuit( event ),
            'delete-indentation': lambda event: self.deleteIndentation( event ) and self.keyboardQuit( event ),    
            'transpose-chars': lambda event : self.swapCharacters( event ) and self.keyboardQuit( event ),
            'transpose-words': lambda event, sw = self.swapSpots: self.swapWords( event, sw ) and self.keyboardQuit( event ),
            'transpose-lines': lambda event: self.transposeLines( event ) and self.keyboardQuit( event ),
            'split-line' : lambda event: self.insertNewLineIndent( event ) and self.keyboardQuit( event ),
            'upcase-region': lambda event: self.upperLowerRegion( event, 'up' ) and self.keyboardQuit( event ),
            'downcase-region': lambda event: self.upperLowerRegion( event , 'low' ) and self.keyboardQuit( event ),
            'dabbrev-expands': lambda event: self.dynamicExpansion( event ) and self.keyboardQuit( event ),
            'dabbrev-completion': lambda event: self.dynamicExpansion2( event ) and self.keyboardQuit( event ),
            'goto-line': lambda event: self.startGoto( event ),
            'goto-char': lambda event: self.startGoto( event, True ),
            'set-fill-prefix': lambda event: self.setFillPrefix( event ) and self.keyboardQuit( event ),
            'set-fill-column': lambda event: self.setFillColumn( event ),
            'center-line': lambda event: self.centerLine( event ) and self.keyboardQuit( event ),
            'center-region': lambda event: self.centerRegion( event ) and self.keyboardQuit( event ),
            'forward-char': lambda event, which = 'Right': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
            'backward-char': lambda event, which = 'Left': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
            'previous-line': lambda event, which = 'Up': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
            'next-line': lambda event, which = 'Down': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
            'digit-argument': lambda event: self.universalDispatch( event, '' ),
            'universal-argument': lambda event: self.universalDispatch( event, '' ),   
            'newline-and-indent': lambda event: self.insertNewLineAndTab( event ) and self.keyboardQuit( event ),
            'beginning-of-buffer': lambda event, spot = '1.0' : self.moveTo( event, spot ) and self.keyboardQuit( event ),
            'end-of-buffer': lambda event, spot = 'end' : self.moveTo( event, spot ) and self.keyboardQuit( event ),
            'scroll-up': lambda event, way = 'north' : self.screenscroll( event, way ) and self.keyboardQuit( event ),
            'scroll-down': lambda event, way = 'south': self.screenscroll( event, way ) and self.keyboardQuit( event ),
            
            # Buffers.
            'copy-to-buffer': lambda event, which = 'copy-to-buffer': self.setInBufferMode( event, which ),
            'insert-buffer': lambda event, which = 'insert-buffer': self.setInBufferMode( event, which ),
            'append-to-buffer': lambda event , which = 'append-to-buffer':  self.setInBufferMode( event, which ),
            'prepend-to-buffer': lambda event, which = 'prepend-to-buffer': self.setInBufferMode( event, which ),
            'switch-to-buffer': lambda event, which = 'switch-to-buffer': self.setInBufferMode( event, which ),
            'list-buffers' : lambda event: self.listBuffers( event ),
            'kill-buffer' : lambda event, which = 'kill-buffer': self.setInBufferMode( event, which ),
            'rename-buffer': lambda event: self.renameBuffer( event ),
            
            # Query-replace.
            'query-replace': lambda event: self.masterQR( event ), 
            'query-replace-regex': lambda event: self.startRegexReplace() and self.masterQR( event ),
            'inverse-add-global-abbrev': lambda event: self.abbreviationDispatch( event, 2 ) , 
            
            # Re search.
            're-search-forward': lambda event: self.reStart( event ),
            're-search-backward': lambda event: self.reStart( event, which = 'backward' ), 
            
            'iconfify-or-deiconify-frame': lambda event: self.suspend( event ) and self.keyboardQuit( event ),
            'save-buffers-kill-emacs': lambda event: self.keyboardQuit( event ) and self.shutdown( event ),
            
            'diff': self.diff, 
            'what-line': self.whatLine,
            'flush-lines': lambda event: self.startLines( event ),
            'keep-lines': lambda event: self.startLines( event, which = 'keep' ),
            
            # Files and directories.
            'make-directory': lambda event: self.makeDirectory( event ),
            'remove-directory': lambda event: self.removeDirectory( event ),
            'delete-file': lambda event: self.deleteFile( event ),
            'insert-file' : lambda event: self.insertFile( event ) and self.keyboardQuit( event ),
            'save-buffer' : lambda event: self.saveFile( event ) and self.keyboardQuit( event ),
            
            'repeat-complex-command': lambda event: self.repeatComplexCommand( event ),
            'eval-expression': self.startEvaluate,
            'tabify': self.tabify,
            'untabify': lambda event: self.tabify( event, which = 'untabify' ),
            'shell-command': self.startSubprocess,
            'shell-command-on-region': lambda event: self.startSubprocess( event, which=1 ),
        }
        
        #Note: if we are reusing some of the cbDict lambdas we need to alter many by adding: self.keyboardQuit( event )
        #Otherwise the darn thing just sits in Alt-X land.  Putting the 'and self.keyboardQuit( event )' part in the killbuffer
        #and yanking it out for each new item, works well.  Adding it to a register might be good to.
        return doAltX
    #@-node:ekr.20050724075352.51:addAltXCommands
    #@-node:ekr.20050724075352.48:add command dictionary methods
    #@+node:ekr.20050725133033:outer emacs methods
    #@+node:ekr.20050724075352.283:Alt_X methods
    #@+at
    # These methods control the Alt-x command functionality.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.284:alt_X
    #self.altx = False
    def alt_X( self, event , which = None):
        #global altx
        if which:
            self.mcStateManager.setState( 'altx', which )
        else:
            self.mcStateManager.setState( 'altx', 'True' )
    
        svar, label = self.getSvarLabel( event )
        if which:
            svar.set( '%s M-x:' % which )
        else:
            svar.set( 'M-x:' )
        self.setLabelBlue( label )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.284:alt_X
    #@+node:ekr.20050724075352.285:doAlt_X
    def doAlt_X( self, event ):
        '''This method executes the correct Alt-X command'''
        svar, label = self.getSvarLabel( event )
        if svar.get().endswith( 'M-x:' ): 
            self.axTabList.clear() #clear the list, new Alt-x command is in effect
            svar.set( '' )
        if event.keysym == 'Return':
            txt = svar.get()
            if self.doAltX.has_key( txt ):
                if txt != 'repeat-complex-command':
                    self.altx_history.reverse()
                    self.altx_history.append( txt )
                    self.altx_history.reverse()
                aX = self.mcStateManager.getState( 'altx' )
                if aX.isdigit() and txt in self.x_hasNumeric:
                    self.doAltX [ txt]( event, aX )
                else:
                    self.doAltX [ txt ]( event )
            else:
                self.keyboardQuit( event )
                svar.set('Command does not exist' )
    
            #self.altx = False
            #self.mcStateManager.setState( 'altx', False )
            return 'break'
        if event.keysym == 'Tab':
            
            stext = svar.get().strip()
            if self.axTabList.prefix and stext.startswith( self.axTabList.prefix ):
                svar.set( self.axTabList.next() ) #get next in iteration
            else:
                prefix = svar.get()
                pmatches = self._findMatch2( svar )
                self.axTabList.setTabList( prefix, pmatches )
                svar.set( self.axTabList.next() ) #begin iteration on new lsit
            return 'break'   
        else:
            self.axTabList.clear() #clear the list, any other character besides tab indicates that a new prefix is in effect.    
        self.setSvar( event, svar )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.285:doAlt_X
    #@+node:ekr.20050724075352.286:execute last altx methods
    #@+others
    #@+node:ekr.20050724075352.287:executeLastAltX
    def executeLastAltX( self, event ):
        
        if event.keysym == 'Return' and self.altx_history:
            last = self.altx_history[ 0 ]
            self.doAltX[ last ]( event )
            return 'break'
        else:
            return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.287:executeLastAltX
    #@+node:ekr.20050724075352.288:repeatComplexCommand
    def repeatComplexCommand( self, event ):
    
        self.keyboardQuit( event )
        if self.altx_history:
            svar, label = self.getSvarLabel( event )
            self.setLabelBlue( label )
            svar.set( "Redo: %s" % self.altx_history[ 0 ] )
            self.mcStateManager.setState( 'last-altx', True )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.288:repeatComplexCommand
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.286:execute last altx methods
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.283:Alt_X methods
    #@+node:ekr.20050724075352.150:comment column methods
    #@+others
    #@+node:ekr.20050724075352.151:setCommentColumn
    #self.ccolumn = '0'
    def setCommentColumn( self, event ):
        #global ccolumn
        cc= event.widget.index( 'insert' )
        cc1, cc2 = cc.split( '.' )
        self.ccolumn = cc2
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.151:setCommentColumn
    #@+node:ekr.20050724075352.152:indentToCommentColumn
    def indentToCommentColumn( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert lineend' )
        i1, i2 = i.split( '.' )
        i2 = int( i2 )
        c1 = int( self.ccolumn )
        if i2 < c1:
            wsn = c1 - i2
            tbuffer.insert( 'insert lineend', ' '* wsn )
        if i2 >= c1:
            tbuffer.insert( 'insert lineend', ' ')
        tbuffer.mark_set( 'insert', 'insert lineend' )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.152:indentToCommentColumn
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.150:comment column methods
    #@+node:ekr.20050724075352.105:configurable methods
    #@+at
    # These methods contain methods by which an Emacs instance is extended, 
    # changed, added to , etc...
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.106:tailEnd methods
    #@+others
    #@+node:ekr.20050724075352.107:_tailEnd
    def _tailEnd( self, tbuffer ):
        '''This returns the tailEnd function that has been configure for the tbuffer parameter.'''
        if self.tailEnds.has_key( tbuffer ):
            return self.tailEnds[ tbuffer ]( tbuffer )
        else:
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.107:_tailEnd
    #@+node:ekr.20050724075352.108:setTailEnd
    #self.tailEnds = {}
    def setTailEnd( self, tbuffer , tailCall ):
        '''This method sets a ending call that is specific for a particular Text widget.
           Some environments require that specific end calls be made after a keystroke
           or command is executed.'''
        self.tailEnds[ tbuffer ] = tailCall
    #@nonl
    #@-node:ekr.20050724075352.108:setTailEnd
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.106:tailEnd methods
    #@+node:ekr.20050724075352.109:undoer methods
    #@+at
    # Emacs requires an undo mechanism be added from the environment.
    # If there is no undo mechanism added, there will be no undo functionality 
    # in the instance.
    #@-at
    #@@c
    
    
    
    #@+others
    #@+node:ekr.20050724075352.110:setUndoer
    #self.undoers = {}
    def setUndoer( self, tbuffer, undoer ):
        '''This method sets the undoer method for the Emacs instance.'''
        self.undoers[ tbuffer ] = undoer
    #@nonl
    #@-node:ekr.20050724075352.110:setUndoer
    #@+node:ekr.20050724075352.111:doUndo
    def doUndo(  self, event, amount = 1 ):
        tbuffer = event.widget
        if self.undoers.has_key( tbuffer ):
            for z in xrange( amount ):
                self.undoers[ tbuffer ]()
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.111:doUndo
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.109:undoer methods
    #@+node:ekr.20050724075352.112:setBufferStrokes  (creates all bindings)
    def setBufferStrokes (self,tbuffer,label):
    
        '''setBufferStrokes takes a Tk Text widget called 'tbuffer'. 'stext' is a function or method
        that when called will return the value of the search text. 'rtext' is a function or method
        that when called will return the value of the replace text.  It is this method and
        getHelpText that users of the temacs module should call.  The rest are callback functions
        that enable the Emacs emulation.'''
        
        # g.trace(tbuffer,label)
        #@    <<define cb callback>>
        #@+node:ekr.20050724075352.113:<< define cb callback >>
        
        def cb (evstring):
            _cb = None 
            if self.cbDict.has_key(evstring):
                _cb = self.cbDict[evstring]
            evstring = '<%s>'%evstring 
            if evstring!='<Key>':
                # g.trace(evstring)
                tbuffer.bind(evstring,lambda event,meth=_cb:self.masterCommand(event,meth,evstring))
            else:
                # g.trace('+',evstring)
                tbuffer.bind(evstring,lambda event,meth=_cb:self.masterCommand(event,meth,evstring),'+')
        #@nonl
        #@-node:ekr.20050724075352.113:<< define cb callback >>
        #@nl
        # EKR: create one binding for each entry in cbDict.
        for z in self.cbDict:
            cb(z)
        self.mbuffers[tbuffer] = label 
        self.svars[tbuffer] = Tk.StringVar()
        #@    <<define setVar callback>>
        #@+node:ekr.20050724075352.114:<< define setVar callback >>
        def setVar (event):
            label = self.mbuffers[event.widget]
            svar = self.svars[event.widget]
            label.configure(textvariable=svar)
        #@nonl
        #@-node:ekr.20050724075352.114:<< define setVar callback >>
        #@nl
        tbuffer.bind('<FocusIn>',setVar,'+')
        def scrollTo (event):
            event.widget.see('insert')
        #tbuffer.bind( '<Enter>', scrollTo, '+' )
        
        # EKR: This adds a binding for all <Key> events, so _all_ key events go through masterCommand.
        cb('Key')
    #@nonl
    #@-node:ekr.20050724075352.112:setBufferStrokes  (creates all bindings)
    #@+node:ekr.20050724075352.115:extendAltX
    def extendAltX( self, name, function ):
    
        '''A simple method that extends the functions Alt-X offers.'''
        
        # Important: f need not be a method of the emacs class.
    
        def f (event,aX=None,self=self,command=function):
            # g.trace(event,self,command)
            command()
            self.keyboardQuit(event)
    
        self.doAltX [ name ] = f
    #@nonl
    #@-node:ekr.20050724075352.115:extendAltX
    #@+node:ekr.20050724075352.116:reconfigureKeyStroke
    def reconfigureKeyStroke( self, tbuffer, keystroke , set_to ):
        
        '''This method allows the user to reconfigure what a keystroke does.
           This feature is alpha at best, and untested.'''
    
        if self.cbDict.has_key( set_to ):
            
            command = self.cbDict[ set_to ]
            self.cbDict[ keystroke ] = command
            evstring = '<%s>' % keystroke
            tbuffer.bind( evstring,  lambda event, meth = command: self.masterCommand( event, meth , evstring)  )
    #@nonl
    #@-node:ekr.20050724075352.116:reconfigureKeyStroke
    #@+node:ekr.20050724075352.117:buffer recognition and alterers
    #@+at
    # an Emacs instance does not have knowledge of what is considered a buffer 
    # in the environment.
    # It must be configured by the user so that it can operate on the other 
    # buffers.  Otherwise
    # these methods will be useless.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.118:configure buffer methods
    #@+others
    #@+node:ekr.20050724075352.119:setBufferGetter
    def setBufferListGetter( self, buffer, method ):
        #Sets a method that returns a buffer name and its text, and its insert position.
        self.bufferListGetters[ buffer ] = method
    #@nonl
    #@-node:ekr.20050724075352.119:setBufferGetter
    #@+node:ekr.20050724075352.120:setBufferSetter
    def setBufferSetter( self, buffer, method ):
        #Sets a method that takes a buffer name and the new contents.
        self.bufferSetters[ buffer ] = method
    #@nonl
    #@-node:ekr.20050724075352.120:setBufferSetter
    #@+node:ekr.20050724075352.121:getBufferDict
    def getBufferDict( self, event ):
        
        tbuffer = event.widget
        meth = self.bufferListGetters[ tbuffer ]
        return meth()
    #@nonl
    #@-node:ekr.20050724075352.121:getBufferDict
    #@+node:ekr.20050724075352.122:setBufferData
    def setBufferData( self, event, name, data ):
        
        tbuffer = event.widget
        meth = self.bufferSetters[ tbuffer ]
        meth( name, data )
    #@nonl
    #@-node:ekr.20050724075352.122:setBufferData
    #@+node:ekr.20050724075352.123:setBufferGoto
    def setBufferGoto( self, tbuffer, method ):
        self.bufferGotos[ tbuffer ] = method
    #@nonl
    #@-node:ekr.20050724075352.123:setBufferGoto
    #@+node:ekr.20050724075352.124:setBufferDelete
    def setBufferDelete( self, tbuffer, method ):
        
        self.bufferDeletes[ tbuffer ] = method
    #@nonl
    #@-node:ekr.20050724075352.124:setBufferDelete
    #@+node:ekr.20050724075352.125:setBufferRename
    def setBufferRename( self, buffer, method ):
        
        self.renameBuffers[ buffer ] = method
    #@nonl
    #@-node:ekr.20050724075352.125:setBufferRename
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.118:configure buffer methods
    #@+node:ekr.20050724075352.126:buffer operations
    #@+others
    #@+node:ekr.20050724075352.127:appendToBuffer
    def appendToBuffer( self, event, name ):
    
        tbuffer = event.widget
        try:
            txt = tbuffer.get( 'sel.first', 'sel.last' )
            bdata = self.bufferDict[ name ]
            bdata = '%s%s' % ( bdata, txt )
            self.setBufferData( event, name, bdata )
        except Exception, x:
            pass
        return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.127:appendToBuffer
    #@+node:ekr.20050724075352.128:prependToBuffer
    def prependToBuffer( self, event, name ):
        
        tbuffer = event.widget
        try:
            txt = tbuffer.get( 'sel.first', 'sel.last' )
            bdata = self.bufferDict[ name ]
            bdata = '%s%s' % ( txt, bdata )
            self.setBufferData( event, name, bdata )
        except Exception, x:
            pass
        return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.128:prependToBuffer
    #@+node:ekr.20050724075352.129:insertToBuffer
    def insertToBuffer( self, event, name ):
    
        tbuffer = event.widget
        bdata = self.bufferDict[ name ]
        tbuffer.insert( 'insert', bdata )
        self._tailEnd( tbuffer )
        return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.129:insertToBuffer
    #@+node:ekr.20050724075352.130:listBuffers
    def listBuffers( self, event ):
        
        bdict  = self.getBufferDict( event )
        list = bdict.keys()
        list.sort()
        svar, label = self.getSvarLabel( event )
        data = '\n'.join( list )
        self.keyboardQuit( event )
        svar.set( data )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.130:listBuffers
    #@+node:ekr.20050724075352.131:copyToBuffer
    def copyToBuffer( self, event, name ):
        
        tbuffer = event.widget
        try:
            txt = tbuffer.get( 'sel.first', 'sel.last' )
            self.setBufferData( event, name, txt )
        except Exception, x:
            pass
        return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.131:copyToBuffer
    #@+node:ekr.20050724075352.132:switchToBuffer
    def switchToBuffer( self, event, name ):
        
        method = self.bufferGotos[ event.widget ]
        self.keyboardQuit( event )
        method( name )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.132:switchToBuffer
    #@+node:ekr.20050724075352.133:killBuffer
    def killBuffer( self, event, name ):
        
        method = self.bufferDeletes[ event.widget ]
        self.keyboardQuit( event )
        method( name )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.133:killBuffer
    #@+node:ekr.20050724075352.134:renameBuffer
    def renameBuffer( self, event ):
        
        svar, label = self.getSvarLabel( event )
        if not self.mcStateManager.getState( 'renameBuffer' ):
            self.mcStateManager.setState( 'renameBuffer', True )
            svar.set( '' )
            label.configure( background = 'lightblue' )
            return 'break'
        if event.keysym == 'Return':
           
           nname = svar.get()
           self.keyboardQuit( event )
           self.renameBuffers[ event.widget ]( nname )
            
            
        else:
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.134:renameBuffer
    #@+node:ekr.20050724075352.135:chooseBuffer
    def chooseBuffer( self, event ):
        
        svar, label = self.getSvarLabel( event )
    
        state = self.mcStateManager.getState( 'chooseBuffer' )
        if state.startswith( 'start' ):
            state = state[ 5: ]
            self.mcStateManager.setState( 'chooseBuffer', state )
            svar.set( '' )
        if event.keysym == 'Tab':
            
            stext = svar.get().strip()
            if self.bufferTracker.prefix and stext.startswith( self.bufferTracker.prefix ):
                svar.set( self.bufferTracker.next() ) #get next in iteration
            else:
                prefix = svar.get()
                pmatches = []
                for z in self.bufferDict.keys():
                    if z.startswith( prefix ):
                        pmatches.append( z )
                self.bufferTracker.setTabList( prefix, pmatches )
                svar.set( self.bufferTracker.next() ) #begin iteration on new lsit
            return 'break'        
    
            
        elif event.keysym == 'Return':
           
           bMode = self.mcStateManager.getState( 'chooseBuffer' )
           return self.bufferCommands[ bMode ]( event, svar.get() )
            
            
        else:
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.135:chooseBuffer
    #@+node:ekr.20050724075352.136:setInBufferMode
    def setInBufferMode( self, event, which ):
        
        self.keyboardQuit( event )
        tbuffer = event.widget
        self.mcStateManager.setState( 'chooseBuffer', 'start%s' % which )
        svar, label = self.getSvarLabel( event )
        label.configure( background = 'lightblue' )
        svar.set( 'Choose Buffer Name:' )
        self.bufferDict = self.getBufferDict( event )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.136:setInBufferMode
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.126:buffer operations
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.117:buffer recognition and alterers
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.105:configurable methods
    #@+node:ekr.20050724075352.242:ControlX methods
    #@+others
    #@+node:ekr.20050724075352.243:startControlX
    def startControlX( self, event ):
        '''This method starts the Control-X command sequence.'''  
        #global controlx
        #self.controlx = True
        self.mcStateManager.setState( 'controlx', True )
        svar, label = self.getSvarLabel( event )
        svar.set( 'Control - X' )
        label.configure( background = 'lightblue' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.243:startControlX
    #@+node:ekr.20050724075352.244:stopControlX
    def stopControlX( self, event ):
        
        '''This method clears the state of the Emacs instance'''
        
        # This will all be migrated to keyboardQuit eventually.
        if self.shuttingdown: return
        self.sRect = False
        self.mcStateManager.clear()
        event.widget.tag_delete( 'color' )
        event.widget.tag_delete( 'color1' )
        if self.registermode:
            self.deactivateRegister( event )
        self.rectanglemode = 0
        self.bufferMode = None
        self.resetMiniBuffer( event )
        event.widget.update_idletasks()     
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.244:stopControlX
    #@+node:ekr.20050724075352.245:doControlX
    #self.registermode = False
    def doControlX( self, event, stroke, previous = [] ):
        #global registermode
        """previous.insert( 0, event.keysym )
        if len( previous ) > 10: previous.pop()
        if stroke == '<Key>':
            if event.keysym in ( 'Shift_L', 'Shift_R' ):
                return
            if event.keysym == 'period':
                self.stopControlX( event )
                return self.setFillPrefix( event )
            if event.keysym == 'parenleft':
                self.stopControlX( event )
                return self.startKBDMacro( event )
            if event.keysym == 'parenright':
                self.stopControlX( event )
                return self.stopKBDMacro( event )
            if event.keysym == 'semicolon':
                self.stopControlX( event )
                return self.setCommentColumn( event )
            if event.keysym == 'Tab':
                self.stopControlX( event )
                return self.tabIndentRegion( event )
            if self.sRect:
                self.stringRectangle( event )
                return 'break'
            if event.keysym in ( 'a', 'i' , 'e'):
                svar, label = self.getSvarLabel( event )
                if svar.get() != 'a' and event.keysym == 'a':
                    svar.set( 'a' )
                    return 'break'
                elif svar.get() == 'a':
                    if event.char == 'i':
                        svar.set( 'a i' )
                    elif event.char == 'e':
                        self.stopControlX( event )
                        event.char = ''
                        self.expandAbbrev( event )
                    return 'break'
            if event.keysym == 'g':
                svar, label = self.getSvarLabel( event )
                l = svar.get()
                if l == 'a':
                    self.stopControlX( event )
                    return self.abbreviationDispatch( event, 1 )
                elif l == 'a i':
                    self.stopControlX( event )
                    return self.abbreviationDispatch( event, 2 )
            if event.keysym == 'e':
                self.stopControlX( event )
                return self.executeLastMacro( event )
            if event.keysym == 'x' and previous[ 1 ] not in ( 'Control_L', 'Control_R'):
                event.keysym = 's' 
                self.setNextRegister( event )
                return 'break'
            if event.keysym == 'o' and self.registermode == 1:
                self.openRectangle( event )
                return 'break'
            if event.keysym == 'c' and self.registermode == 1:
                self.clearRectangle( event )
                return 'break'
            if event.keysym == 't' and self.registermode == 1:
                self.stringRectangle( event )
                return 'break'
            if event.keysym == 'y' and self.registermode == 1:
                self.yankRectangle( event )
                return 'break'
            if event.keysym == 'd' and self.registermode == 1:
                self.deleteRectangle( event )
                return 'break'
            if event.keysym == 'k' and self.registermode == 1:
                self.killRectangle( event )
                return 'break'       
            if self.registermode == 1:
                self.setNextRegister( event )
                return 'break'
            elif self.registermode == 2:
                self.executeRegister( event )
                return 'break'
            if event.keysym == 'r':
                self.registermode = 1
                svar = self.svars[ event.widget ]
                svar.set( 'C - x r' )
                return 'break'
            if event.keysym== 'h':
               self.stopControlX( event )
               event.widget.tag_add( 'sel', '1.0', 'end' )
               return 'break' 
            if event.keysym == 'equal':
                self.lineNumber( event )
                return 'break'
            if event.keysym == 'u':
                self.stopControlX( event )
                return self.doUndo( event, 2 )
        if stroke in self.xcommands:
            self.xcommands[ stroke ]( event )
            self.stopControlX( event )
        return 'break' """
        return self.cxHandler( event, stroke )
    #@nonl
    #@-node:ekr.20050724075352.245:doControlX
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.242:ControlX methods
    #@+node:ekr.20050724075352.250:delete methods
    #@+others
    #@+node:ekr.20050724075352.251:deleteIndentation
    def deleteIndentation( self, event ):
        tbuffer = event.widget
        txt = tbuffer.get( 'insert linestart' , 'insert lineend' )
        txt = ' %s' % txt.lstrip()
        tbuffer.delete( 'insert linestart' , 'insert lineend +1c' )    
        i  = tbuffer.index( 'insert - 1c' )
        tbuffer.insert( 'insert -1c', txt )
        tbuffer.mark_set( 'insert', i )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.251:deleteIndentation
    #@+node:ekr.20050724075352.252:deleteNextChar
    def deleteNextChar( self,event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        tbuffer.delete( i, '%s +1c' % i )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.252:deleteNextChar
    #@+node:ekr.20050724075352.253:deleteSpaces
    def deleteSpaces( self, event , insertspace = False):
        tbuffer = event.widget
        char = tbuffer.get( 'insert', 'insert + 1c ' )
        if char.isspace():
            i = tbuffer.index( 'insert' )
            wf = tbuffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
            wb = tbuffer.search( r'\w', i, stopindex = '%s linestart' % i, regexp = True, backwards = True )
            if '' in ( wf, wb ):
                return 'break'
            tbuffer.delete( '%s +1c' %wb, wf )
            if insertspace:
                tbuffer.insert( 'insert', ' ' )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.253:deleteSpaces
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.250:delete methods
    #@+node:ekr.20050724075352.237:diff methods
    #@+at
    # the diff command, accessed by Alt-x diff.  Creates a buffer and puts the 
    # diff between 2 files into it.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.238:diff
    def diff( self, event ):
        
        try:
            f, name = self.getReadableTextFile()
            txt1 = f.read()
            f.close()
            
            f2, name2 = self.getReadableTextFile()
            txt2 = f2.read()
            f2.close()
        except:
            return self.keyboardQuit( event )
        
        
        self.switchToBuffer( event, "*diff* of ( %s , %s )" %( name, name2 ) )
        import difflib
        data = difflib.ndiff( txt1, txt2 )
        idata = []
        for z in data:
            idata.append( z )
        tbuffer = event.widget
        tbuffer.delete( '1.0', 'end' )
        tbuffer.insert( '1.0', ''.join( idata ) )
        self._tailEnd( tbuffer )
        return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.238:diff
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.237:diff methods
    #@+node:ekr.20050724075352.302:directory methods
    #@+others
    #@+node:ekr.20050724075352.303:makeDirectory
    def makeDirectory( self, event ):
        
        svar,label = self.getSvarLabel( event )
        state = self.mcStateManager.getState( 'make_directory' )
        if not state:
            self.mcStateManager.setState( 'make_directory', True )
            self.setLabelBlue( label )
            directory = os.getcwd()
            svar.set( '%s%s' %( directory, os.sep ) )
            return 'break'
        
        if event.keysym == 'Return':
            
            ndirectory = svar.get()
            self.keyboardQuit( event )
            try:
                os.mkdir( ndirectory )
            except:
                svar.set( "Could not make %s%" % ndirectory  )
            return 'break'
        else:
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.303:makeDirectory
    #@+node:ekr.20050724075352.304:removeDirectory
    def removeDirectory( self, event ):
        
        svar,label = self.getSvarLabel( event )
        state = self.mcStateManager.getState( 'remove_directory' )
        if not state:
            self.mcStateManager.setState( 'remove_directory', True )
            self.setLabelBlue( label )
            directory = os.getcwd()
            svar.set( '%s%s' %( directory, os.sep ) )
            return 'break'
        
        if event.keysym == 'Return':
            
            ndirectory = svar.get()
            self.keyboardQuit( event )
            try:
                os.rmdir( ndirectory )
            except:
                svar.set( "Could not remove %s%" % ndirectory  )
            return 'break'
        else:
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.304:removeDirectory
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.302:directory methods
    #@+node:ekr.20050724075352.275:dynamic abbreviations methods
    #@+others
    #@+node:ekr.20050724075352.276:dynamicExpansion
    def dynamicExpansion( self, event ):#, store = {'rlist': [], 'stext': ''} ):
        tbuffer = event.widget
        rlist = self.store[ 'rlist' ]
        stext = self.store[ 'stext' ]
        i = tbuffer.index( 'insert -1c wordstart' )
        i2 = tbuffer.index( 'insert -1c wordend' )
        txt = tbuffer.get( i, i2 )
        dA = tbuffer.tag_ranges( 'dA' )
        tbuffer.tag_delete( 'dA' )
        def doDa( txt, from_ = 'insert -1c wordstart', to_ = 'insert -1c wordend' ):
    
            tbuffer.delete( from_, to_ ) 
            tbuffer.insert( 'insert', txt, 'dA' )
            return self._tailEnd( tbuffer )
            
        if dA:
            dA1, dA2 = dA
            dtext = tbuffer.get( dA1, dA2 )
            if dtext.startswith( stext ) and i2 == dA2: #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
                if rlist:
                    txt = rlist.pop()
                else:
                    txt = stext
                    tbuffer.delete( dA1, dA2 )
                    dA2 = dA1 #since the text is going to be reread, we dont want to include the last dynamic abbreviation
                    self.getDynamicList( tbuffer, txt, rlist )
                return doDa( txt, dA1, dA2 )
            else:
                dA = None
                
        if not dA:
            self.store[ 'stext' ] = txt
            self.store[ 'rlist' ] = rlist = []
            self.getDynamicList( tbuffer, txt, rlist )
            if not rlist:
                return 'break'
            txt = rlist.pop()
            return doDa( txt )
    #@nonl
    #@-node:ekr.20050724075352.276:dynamicExpansion
    #@+node:ekr.20050724075352.277:dynamicExpansion2
    def dynamicExpansion2( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert -1c wordstart' )
        i2 = tbuffer.index( 'insert -1c wordend' )
        txt = tbuffer.get( i, i2 )   
        rlist = []
        self.getDynamicList( tbuffer, txt, rlist )
        dEstring = reduce( self.findPre, rlist )
        if dEstring:
            tbuffer.delete( i , i2 )
            tbuffer.insert( i, dEstring )    
            return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.277:dynamicExpansion2
    #@+node:ekr.20050724075352.278:getDynamicList
    def getDynamicList( self, tbuffer, txt , rlist ):
    
         ttext = tbuffer.get( '1.0', 'end' )
         items = self.dynaregex.findall( ttext ) #make a big list of what we are considering a 'word'
         if items:
             for word in items:
                 if not word.startswith( txt ) or word == txt: continue #dont need words that dont match or == the pattern
                 if word not in rlist:
                     rlist.append( word )
                 else:
                     rlist.remove( word )
                     rlist.append( word )
    #@nonl
    #@-node:ekr.20050724075352.278:getDynamicList
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.275:dynamic abbreviations methods
    #@+node:ekr.20050724075352.310:Esc methods for Python evaluation
    #@+others
    #@+node:ekr.20050724075352.311:watchEscape
    def watchEscape( self, event ):
        
        svar, label = self.getSvarLabel( event )
        if not self.mcStateManager.hasState():
            self.mcStateManager.setState( 'escape' , 'start' )
            self.setLabelBlue( label )
            svar.set( 'Esc' )
            return 'break'
        if self.mcStateManager.whichState() == 'escape':
            
            state = self.mcStateManager.getState( 'escape' )
            hi1 = self.keysymhistory[ 0 ]
            hi2 = self.keysymhistory[ 1 ]
            if state == 'esc esc' and event.keysym == 'colon':
                return self.startEvaluate( event )
            elif state == 'evaluate':
                return self.escEvaluate( event )    
            elif hi1 == hi2 == 'Escape':
                self.mcStateManager.setState( 'escape', 'esc esc' )
                svar.set( 'Esc Esc -' )
                return 'break'
            elif event.keysym in ( 'Shift_L', 'Shift_R' ):
                return
            else:
                return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.311:watchEscape
    #@+node:ekr.20050724075352.312:escEvaluate
    def escEvaluate( self, event ):
        
        svar, label = self.getSvarLabel( event )
        if svar.get() == 'Eval:':
            svar.set( '' )
        
        if event.keysym =='Return':
        
            expression = svar.get()
            try:
                ok = False
                tbuffer = event.widget
                result = eval( expression, {}, {} )
                result = str( result )
                tbuffer.insert( 'insert', result )
                ok = True
            finally:
                self.keyboardQuit( event )
                if not ok:
                    svar.set( 'Error: Invalid Expression' )
                return self._tailEnd( tbuffer )
            
            
        else:
            
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.312:escEvaluate
    #@+node:ekr.20050724075352.313:startEvaluate
    def startEvaluate( self, event ):
        
        svar, label = self.getSvarLabel( event )
        self.setLabelBlue( label )
        svar.set( 'Eval:' )
        self.mcStateManager.setState( 'escape', 'evaluate' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.313:startEvaluate
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.310:Esc methods for Python evaluation
    #@+node:ekr.20050724075352.305:file methods
    #@+at
    # These methods load files into buffers and save buffers to files
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.306:deleteFile
    def deleteFile( self, event ):
    
        svar,label = self.getSvarLabel( event )
        state = self.mcStateManager.getState( 'delete_file' )
        if not state:
            self.mcStateManager.setState( 'delete_file', True )
            self.setLabelBlue( label )
            directory = os.getcwd()
            svar.set( '%s%s' %( directory, os.sep ) )
            return 'break'
        
        if event.keysym == 'Return':
            
            dfile = svar.get()
            self.keyboardQuit( event )
            try:
                os.remove( dfile )
            except:
                svar.set( "Could not delete %s%" % dfile  )
            return 'break'
        else:
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.306:deleteFile
    #@+node:ekr.20050724075352.307:insertFile
    def insertFile( self, event ):
        tbuffer = event.widget
        f, name = self.getReadableTextFile()
        if not f: return None
        txt = f.read()
        f.close()
        tbuffer.insert( 'insert', txt )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.307:insertFile
    #@+node:ekr.20050724075352.308:saveFile
    def saveFile( self, event ):
        tbuffer = event.widget
        import tkFileDialog
        txt = tbuffer.get( '1.0', 'end' )
        f = tkFileDialog.asksaveasfile()
        if f == None : return None
        f.write( txt )
        f.close()
    #@nonl
    #@-node:ekr.20050724075352.308:saveFile
    #@+node:ekr.20050724075352.309:getReadableFile
    def getReadableTextFile( self ):
        
        import tkFileDialog
        fname = tkFileDialog.askopenfilename()
        if fname == None: return None, None
        f = open( fname, 'rt' )
        return f, fname
    #@nonl
    #@-node:ekr.20050724075352.309:getReadableFile
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.305:file methods
    #@+node:ekr.20050724075352.209:fill column and centering
    #@+at
    # These methods are currently just used in tandem to center the line or 
    # region within the fill column.
    # for example, dependent upon the fill column, this text:
    # 
    # cats
    # raaaaaaaaaaaats
    # mats
    # zaaaaaaaaap
    # 
    # may look like
    # 
    #                                  cats
    #                            raaaaaaaaaaaats
    #                                  mats
    #                              zaaaaaaaaap
    # after an center-region command via Alt-x.
    # 
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.210:centerLine
    def centerLine( self, event ):
        '''Centers line within current fillColumn'''
        
        tbuffer = event.widget
        ind = tbuffer.index( 'insert linestart' )
        txt = tbuffer.get( 'insert linestart', 'insert lineend' )
        txt = txt.strip()
        if len( txt ) >= self.fillColumn: return self._tailEnd( tbuffer )
        amount = ( self.fillColumn - len( txt ) ) / 2
        ws = ' ' * amount
        col, nind = ind.split( '.' )
        ind = tbuffer.search( '\w', 'insert linestart', regexp = True, stopindex = 'insert lineend' )
        if not ind: return 'break'
        tbuffer.delete( 'insert linestart', '%s' % ind )
        tbuffer.insert( 'insert linestart', ws )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.210:centerLine
    #@+node:ekr.20050724075352.211:centerRegion
    def centerRegion( self, event ):
        '''This method centers the current region within the fill column'''
        tbuffer = event.widget
        start = tbuffer.index( 'sel.first linestart' )
        sindex , x = start.split( '.' )
        sindex = int( sindex )
        end = tbuffer.index( 'sel.last linestart' )
        eindex , x = end.split( '.' )
        eindex = int( eindex )
        while sindex <= eindex:
            txt = tbuffer.get( '%s.0 linestart' % sindex , '%s.0 lineend' % sindex )
            txt = txt.strip()
            if len( txt ) >= self.fillColumn:
                sindex = sindex + 1
                continue
            amount = ( self.fillColumn - len( txt ) ) / 2
            ws = ' ' * amount
            ind = tbuffer.search( '\w', '%s.0' % sindex, regexp = True, stopindex = '%s.0 lineend' % sindex )
            if not ind: 
                sindex = sindex + 1
                continue
            tbuffer.delete( '%s.0' % sindex , '%s' % ind )
            tbuffer.insert( '%s.0' % sindex , ws )
            sindex = sindex + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.211:centerRegion
    #@+node:ekr.20050724075352.212:setFillColumn
    def setFillColumn( self, event ):
        
        if self.mcStateManager.getState( 'set-fill-column' ):
            
            if event.keysym == 'Return':
                svar, label = self.getSvarLabel( event )
                value = svar.get()
                if value.isdigit():
                    self.fillColumn = int( value )
                return self.keyboardQuit( event )
            elif event.char.isdigit() or event.char == '\b':
                svar, label = self.getSvarLabel( event )
                self.setSvar( event, svar )
                return 'break'
            return 'break'
            
            
            
        else:
            self.mcStateManager.setState( 'set-fill-column', 1 )
            svar, label = self.getSvarLabel( event )
            svar.set( '' )
            label.configure( background = 'lightblue' )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.212:setFillColumn
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.209:fill column and centering
    #@+node:ekr.20050724075352.206:fill prefix methods
    #@+others
    #@+node:ekr.20050724075352.207:setFillPrefix
    #self.fillPrefix = ''
    def setFillPrefix( self, event ):
        #global fillPrefix
        tbuffer = event.widget
        txt = tbuffer.get( 'insert linestart', 'insert' )
        self.fillPrefix = txt
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.207:setFillPrefix
    #@+node:ekr.20050724075352.208:_addPrefix
    def _addPrefix( self, ntxt ):
            ntxt = ntxt.split( '.' )
            ntxt = map( lambda a: self.fillPrefix+a, ntxt )
            ntxt = '.'.join( ntxt )               
            return ntxt
    #@nonl
    #@-node:ekr.20050724075352.208:_addPrefix
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.206:fill prefix methods
    #@+node:ekr.20050724075352.53:general utility methods
    #@+at
    # These methods currently do not have a specific class that they belong 
    # to.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.54:buffer altering methods
    #@+others
    #@+node:ekr.20050724075352.55:moveTo
    def moveTo( self, event, spot ):
        tbuffer = event.widget
        tbuffer.mark_set( Tk.INSERT, spot )
        tbuffer.see( spot )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.55:moveTo
    #@+node:ekr.20050724075352.56:moveword
    def moveword( self, event, way  ):
        '''This function moves the cursor to the next word, direction dependent on the way parameter'''
        
        tbuffer = event.widget
        #i = way
        
        ind = tbuffer.index( 'insert' )
        if way == 1:
             ind = tbuffer.search( '\w', 'insert', stopindex = 'end', regexp=True )
             if ind:
                nind = '%s wordend' % ind
             else:
                nind = 'end'
        else:
             ind = tbuffer.search( '\w', 'insert -1c', stopindex= '1.0', regexp = True, backwards = True )
             if ind:
                nind = '%s wordstart' % ind 
             else:
                nind = '1.0'
        tbuffer.mark_set( 'insert', nind )
        tbuffer.see( 'insert' )
        tbuffer.event_generate( '<Key>' )
        tbuffer.update_idletasks()
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.56:moveword
    #@+node:ekr.20050724075352.57:capitalize
    def capitalize( self, event, which ):
        tbuffer = event.widget
        text = tbuffer.get( 'insert wordstart', 'insert wordend' )
        i = tbuffer.index( 'insert' )
        if text == ' ': return 'break'
        tbuffer.delete( 'insert wordstart', 'insert wordend' )
        if which == 'cap':
            text = text.capitalize() 
        if which == 'low':
            text = text.lower()
        if which == 'up':
            text = text.upper()
        tbuffer.insert( 'insert', text )
        tbuffer.mark_set( 'insert', i )    
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.57:capitalize
    #@+node:ekr.20050724075352.58:swapWords
    def swapWords( self, event , swapspots ):
        tbuffer = event.widget
        txt = tbuffer.get( 'insert wordstart', 'insert wordend' )
        if txt == ' ' : return 'break'
        i = tbuffer.index( 'insert wordstart' )
        if len( swapspots ) != 0:
            def swp( find, ftext, lind, ltext ):
                tbuffer.delete( find, '%s wordend' % find )
                tbuffer.insert( find, ltext )
                tbuffer.delete( lind, '%s wordend' % lind )
                tbuffer.insert( lind, ftext )
                swapspots.pop()
                swapspots.pop()
                return 'break'
            if tbuffer.compare( i , '>', swapspots[ 1 ] ):
                return swp( i, txt, swapspots[ 1 ], swapspots[ 0 ] )
            elif tbuffer.compare( i , '<', swapspots[ 1 ] ):
                return swp( swapspots[ 1 ], swapspots[ 0 ], i, txt )
            else:
                return 'break'
        else:
            swapspots.append( txt )
            swapspots.append( i )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.58:swapWords
    #@+node:ekr.20050724075352.59:insertParentheses
    def insertParentheses( self, event ):
        tbuffer = event.widget
        tbuffer.insert( 'insert', '()' )
        tbuffer.mark_set( 'insert', 'insert -1c' )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.59:insertParentheses
    #@+node:ekr.20050724075352.60:replace-string and replace-regex
    #@+at
    # both commands use the replaceString method, differentiated by a state 
    # variable
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.61:replaceString
    #self.rString = False
    #self._sString = ''
    #self._rpString = ''
    def replaceString( self, event ):
        
        svar, label = self.getSvarLabel( event )
        if event.keysym in ( 'Control_L', 'Control_R' ):
            return
        rS = self.mcStateManager.getState( 'rString' )
        regex = self._useRegex
        if not rS:
            #self.rString = 1
            self.mcStateManager.setState( 'rString', 1 )
            self._sString = ''
            self._rpString = ''
            if regex:
                svar.set( 'Replace Regex' )
            else:
                svar.set( 'Replace String' )
            return
        if event.keysym == 'Return':
            #self.rString = self.rString + 1
            rS = rS + 1
            self.mcStateManager.setState( 'rString', rS  )
            #return 'break'
        if rS == 1:
            svar.set( '' )
            #self.rString = self.rString + 1
            rS = rS + 1
            self.mcStateManager.setState( 'rString', rS )
        if rS == 2:
            self.setSvar( event, svar )
            self._sString = svar.get()
            return 'break'
        if rS == 3:
            if regex:
                svar.set( 'Replace regex %s with:' % self._sString )
            else:
                svar.set( 'Replace string %s with:' % self._sString )
            self.mcStateManager.setState( 'rString',rS + 1 )
            #self.rString = self.rString + 1
            return 'break'
        if rS == 4:
            svar.set( '' )
            #self.rString = self.rString + 1
            rS = rS + 1
            self.mcStateManager.setState( 'rString', rS )
        if rS == 5:
            self.setSvar( event, svar )
            self._rpString = svar.get()
            return 'break'
        if rS == 6:
            tbuffer = event.widget
            i = 'insert'
            end = 'end'
            ct = 0
            if tbuffer.tag_ranges( 'sel' ):
                i = tbuffer.index( 'sel.first' )
                end = tbuffer.index( 'sel.last' )
            if regex:
                txt = tbuffer.get( i, end )
                try:
                    pattern = re.compile( self._sString )
                except:
                    self.keyboardQuit( event )
                    svar.set( "Illegal regular expression" )
                    return 'break'
                ct = len( pattern.findall( txt ) )
                if ct:
                    ntxt = pattern.sub( self._rpString, txt )
                    tbuffer.delete( i, end )
                    tbuffer.insert( i, ntxt )
            else:
                txt = tbuffer.get( i, end )
                ct = txt.count( self._sString )
                if ct:
                    ntxt = txt.replace( self._sString, self._rpString )
                    tbuffer.delete( i, end )
                    tbuffer.insert( i, ntxt )
                    
            svar.set( 'Replaced %s occurances' % ct )
            #label.configure( background = 'lightgrey' )
            self.setLabelGrey( label ) 
            #self.rString = False
            self.mcStateManager.clear()
            self._useRegex = False
            #self.mcStateManager.setState( 'rString', False )
            return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.61:replaceString
    #@+node:ekr.20050724075352.62:activateReplaceRegex
    def activateReplaceRegex( self ):
        '''This method turns regex replace on for replaceString'''
        self._useRegex = True
        return True
    #@nonl
    #@-node:ekr.20050724075352.62:activateReplaceRegex
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.60:replace-string and replace-regex
    #@+node:ekr.20050724075352.63:swapCharacters
    def swapCharacters( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        c1 = tbuffer.get( 'insert', 'insert +1c' )
        c2 = tbuffer.get( 'insert -1c', 'insert' )
        tbuffer.delete( 'insert -1c', 'insert' )
        tbuffer.insert( 'insert', c1 )
        tbuffer.delete( 'insert', 'insert +1c' )
        tbuffer.insert( 'insert', c2 )
        tbuffer.mark_set( 'insert', i )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.63:swapCharacters
    #@+node:ekr.20050724075352.64:insert new line methods
    #@+others
    #@+node:ekr.20050724075352.65:insertNewLine
    def insertNewLine( self,event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        tbuffer.insert( 'insert', '\n' )
        tbuffer.mark_set( 'insert', i )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.65:insertNewLine
    #@+node:ekr.20050724075352.66:insertNewLineIndent
    #self.negArgs = { '<Alt-c>': changePreviousWord,
    #'<Alt-u>' : changePreviousWord,
    #'<Alt-l>': changePreviousWord }
    
    
    
    def insertNewLineIndent( self, event ):
        tbuffer =  event.widget
        txt = tbuffer.get( 'insert linestart', 'insert lineend' )
        txt = self.getWSString( txt )
        i = tbuffer.index( 'insert' )
        tbuffer.insert( i, txt )
        tbuffer.mark_set( 'insert', i )    
        return self.insertNewLine( event )
    #@nonl
    #@-node:ekr.20050724075352.66:insertNewLineIndent
    #@+node:ekr.20050724075352.67:insertNewLineAndTab
    def insertNewLineAndTab( self, event ):
        '''Insert a newline and tab'''
        tbuffer = event.widget
        self.insertNewLine( event )
        i = tbuffer.index( 'insert +1c' )
        tbuffer.insert( i, '\t' )
        tbuffer.mark_set( 'insert', '%s lineend' % i )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.67:insertNewLineAndTab
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.64:insert new line methods
    #@+node:ekr.20050724075352.68:transposeLines
    def transposeLines( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = str( int( i1 ) -1 )
        if i1 != '0':
            l2 = tbuffer.get( 'insert linestart', 'insert lineend' )
            tbuffer.delete( 'insert linestart-1c', 'insert lineend' )
            tbuffer.insert( i1+'.0', l2 +'\n')
        else:
            l2 = tbuffer.get( '2.0', '2.0 lineend' )
            tbuffer.delete( '2.0', '2.0 lineend' )
            tbuffer.insert( '1.0', l2 + '\n' )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.68:transposeLines
    #@+node:ekr.20050724075352.69:changePreviousWord
    def changePreviousWord( self, event, stroke ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        self.moveword( event, -1  )
        if stroke == '<Alt-c>': 
            self.capitalize( event, 'cap' )
        elif stroke =='<Alt-u>':
             self.capitalize( event, 'up' )
        elif stroke == '<Alt-l>': 
            self.capitalize( event, 'low' )
        tbuffer.mark_set( 'insert', i )
        self.stopControlX( event )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.69:changePreviousWord
    #@+node:ekr.20050724075352.70:removeBlankLines
    def removeBlankLines( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = int( i1 )
        dindex = []
        if tbuffer.get( 'insert linestart', 'insert lineend' ).strip() == '':
            while 1:
                if str( i1 )+ '.0'  == '1.0' :
                    break 
                i1 = i1 - 1
                txt = tbuffer.get( '%s.0' % i1, '%s.0 lineend' % i1 )
                txt = txt.strip()
                if len( txt ) == 0:
                    dindex.append( '%s.0' % i1)
                    dindex.append( '%s.0 lineend' % i1 )
                elif dindex:
                    tbuffer.delete( '%s-1c' % dindex[ -2 ], dindex[ 1 ] )
                    tbuffer.event_generate( '<Key>' )
                    tbuffer.update_idletasks()
                    break
                else:
                    break
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = int( i1 )
        dindex = []
        while 1:
            if tbuffer.index( '%s.0 lineend' % i1 ) == tbuffer.index( 'end' ):
                break
            i1 = i1 + 1
            txt = tbuffer.get( '%s.0' % i1, '%s.0 lineend' % i1 )
            txt = txt.strip() 
            if len( txt ) == 0:
                dindex.append( '%s.0' % i1 )
                dindex.append( '%s.0 lineend' % i1 )
            elif dindex:
                tbuffer.delete( '%s-1c' % dindex[ 0 ], dindex[ -1 ] )
                tbuffer.event_generate( '<Key>' )
                tbuffer.update_idletasks()
                break
            else:
                break
    #@nonl
    #@-node:ekr.20050724075352.70:removeBlankLines
    #@+node:ekr.20050724075352.71:screenscroll
    def screenscroll( self, event, way = 'north' ):
        tbuffer = event.widget
        chng = self.measure( tbuffer )
        i = tbuffer.index( 'insert' )
        
        if way == 'north':
            #top = chng[ 1 ]
            i1, i2 = i.split( '.' )
            i1 = int( i1 ) - chng[ 0 ]
        else:
            #bottom = chng[ 2 ]
            i1, i2 = i.split( '.' )
            i1 = int( i1 ) + chng[ 0 ]
            
        tbuffer.mark_set( 'insert', '%s.%s' % ( i1, i2 ) )
        tbuffer.see( 'insert' )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.71:screenscroll
    #@+node:ekr.20050724075352.72:exchangePointMark
    def exchangePointMark( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        s1 = tbuffer.index( 'sel.first' )
        s2 = tbuffer.index( 'sel.last' )
        i = tbuffer.index( 'insert' )
        if i == s1:
            tbuffer.mark_set( 'insert', s2 )
        else:
            tbuffer.mark_set('insert', s1 )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.72:exchangePointMark
    #@+node:ekr.20050724075352.73:backToIndentation
    def backToIndentation( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert linestart' )
        i2 = tbuffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
        tbuffer.mark_set( 'insert', i2 )
        tbuffer.update_idletasks()
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.73:backToIndentation
    #@+node:ekr.20050724075352.74:indent-relative
    def indent_relative( self, event ):
        
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        l,c = i.split( '.' )
        c2 = int( c )
        l2 = int( l ) - 1
        if l2 < 1: return self.keyboardQuit( event )
        txt = tbuffer.get( '%s.%s' % (l2, c2 ), '%s.0 lineend' % l2 )
        if len( txt ) <= len( tbuffer.get( 'insert', 'insert lineend' ) ):
            tbuffer.insert(  'insert', '\t' )
        else:
            reg = re.compile( '(\s+)' )
            ntxt = reg.split( txt )
            replace_word = re.compile( '\w' )
            for z in ntxt:
                if z.isspace():
                    tbuffer.insert( 'insert', z )
                    break
                else:
                    z = replace_word.subn( ' ', z )
                    tbuffer.insert( 'insert', z[ 0 ] )
                    tbuffer.update_idletasks()
            
            
        self.keyboardQuit( event )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.74:indent-relative
    #@+node:ekr.20050724075352.75:negativeArgument
    #self.negativeArg = False
    def negativeArgument( self, event, stroke = None ):
        #global negativeArg
        svar, label = self.getSvarLabel( event )
        svar.set( "Negative Argument" )
        label.configure( background = 'lightblue' )
        nA = self.mcStateManager.getState( 'negativeArg' )
        if not nA:
            self.mcStateManager.setState( 'negativeArg', True )
            #self.negativeArg = True
        if nA:
            if self.negArgs.has_key( stroke ):
                self.negArgs[ stroke ]( event , stroke)
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.75:negativeArgument
    #@+node:ekr.20050724075352.76:movePastClose
    def movePastClose( self, event ):
        tbuffer = event.widget
        i = tbuffer.search( '(', 'insert' , backwards = True ,stopindex = '1.0' )
        icheck = tbuffer.search( ')', 'insert',  backwards = True, stopindex = '1.0' )
        if ''  ==  i:
            return 'break'
        if icheck:
            ic = tbuffer.compare( i, '<', icheck )
            if ic: 
                return 'break'
        i2 = tbuffer.search( ')', 'insert' ,stopindex = 'end' )
        i2check = tbuffer.search( '(', 'insert', stopindex = 'end' )
        if '' == i2:
            return 'break'
        if i2check:
            ic2 = tbuffer.compare( i2, '>', i2check )
            if ic2:
                return 'break'
        ib = tbuffer.index( 'insert' )
        tbuffer.mark_set( 'insert', '%s lineend +1c' % i2 )
        if tbuffer.index( 'insert' ) == tbuffer.index( '%s lineend' % ib ):
            tbuffer.insert( 'insert' , '\n')
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.76:movePastClose
    #@+node:ekr.20050724075352.77:prevNexSentence
    def prevNexSentence( self, event , way ):
        tbuffer = event.widget
        if way == 'bak':
            i = tbuffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
            if i:
                i2 = tbuffer.search( '.', i, backwards = True, stopindex = '1.0' )
                if not i2:
                    i2 = '1.0'
                if i2:
                    i3 = tbuffer.search( '\w', i2, stopindex = i, regexp = True )
                    if i3:
                        tbuffer.mark_set( 'insert', i3 )
            else:
                tbuffer.mark_set( 'insert', '1.0' )
        else:
            i = tbuffer.search( '.', 'insert', stopindex = 'end' )
            if i:
                tbuffer.mark_set( 'insert', '%s +1c' %i )
            else:
                tbuffer.mark_set( 'insert', 'end' )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.77:prevNexSentence
    #@+node:ekr.20050724075352.78:selectAll
    def selectAll( event ):
    
        event.widget.tag_add( 'sel', '1.0', 'end' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.78:selectAll
    #@+node:ekr.20050724075352.79:suspend
    def suspend( self, event ):
        
        widget = event.widget
        widget.winfo_toplevel().iconify()
    #@nonl
    #@-node:ekr.20050724075352.79:suspend
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.54:buffer altering methods
    #@+node:ekr.20050724075352.80:informational methods
    #@+others
    #@+node:ekr.20050724075352.81:lineNumber
    def lineNumber( self, event ):
        self.stopControlX( event )
        svar, label = self.getSvarLabel( event )
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        c = tbuffer.get( 'insert', 'insert + 1c' )
        txt = tbuffer.get( '1.0', 'end' )
        txt2 = tbuffer.get( '1.0', 'insert' )
        perc = len( txt ) * .01
        perc = int( len( txt2 ) / perc )
        svar.set( 'Char: %s point %s of %s(%s%s)  Column %s' %( c, len( txt2), len( txt), perc,'%', i1 ) )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.81:lineNumber
    #@+node:ekr.20050724075352.82:viewLossage
    def viewLossage( self, event ):
        
        svar, label = self.getSvarLabel( event )
        loss = ''.join( Emacs.lossage )
        self.keyboardQuit( event )
        svar.set( loss )
    #@nonl
    #@-node:ekr.20050724075352.82:viewLossage
    #@+node:ekr.20050724075352.83:whatLine
    def whatLine( self, event ):
        
        tbuffer = event.widget
        svar, label = self.getSvarLabel( event )
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        self.keyboardQuit( event )
        svar.set( "Line %s" % i1 )
    #@nonl
    #@-node:ekr.20050724075352.83:whatLine
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.80:informational methods
    #@+node:ekr.20050724075352.84:pure utility methods
    #@+others
    #@+node:ekr.20050724075352.85:setEvent
    def setEvent( self, event, l ):
        event.keysym = l
        return event
    #@nonl
    #@-node:ekr.20050724075352.85:setEvent
    #@+node:ekr.20050724075352.86:getWSString
    def getWSString( self, txt ):
        ntxt = []
        for z in txt:
            if z == '\t':
                ntxt.append( z )
            else:
                ntxt.append( ' ' )
        return ''.join( ntxt )
    #@nonl
    #@-node:ekr.20050724075352.86:getWSString
    #@+node:ekr.20050724075352.87:findPre
    def findPre( self, a, b ):
        st = ''
        for z in a:
            st1 = st + z
            if b.startswith( st1 ):
                st = st1
            else:
                return st
        return st
    #@nonl
    #@-node:ekr.20050724075352.87:findPre
    #@+node:ekr.20050724075352.88:measure
    def measure( self, tbuffer ):
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        start = int( i1 )
        watch = 0
        ustart = start
        pone = 1
        top = i
        bottom = i
        while pone:
            ustart = ustart - 1
            if ustart < 0:
                break
            ds = '%s.0' % ustart
            pone = tbuffer.dlineinfo( ds )
            if pone:
                top = ds
                watch = watch  + 1
        
        pone = 1
        ustart = start
        while pone:
            ustart = ustart +1
            ds = '%s.0' % ustart
            pone = tbuffer.dlineinfo( ds )
            if pone:
                bottom = ds
                watch = watch + 1
                
        return watch , top, bottom
    #@nonl
    #@-node:ekr.20050724075352.88:measure
    #@+node:ekr.20050724075352.89:manufactureKeyPress
    def manufactureKeyPress( self, event, which ):
    
        tbuffer = event.widget
        tbuffer.event_generate( '<Key>',  keysym = which  )
        tbuffer.update_idletasks()
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.89:manufactureKeyPress
    #@+node:ekr.20050724075352.90:changecbDict
    def changecbDict( self, changes ):
        for z in changes:
            if self.cbDict.has_key( z ):
                self.cbDict[ z ] = self.changes[ z ]
    #@nonl
    #@-node:ekr.20050724075352.90:changecbDict
    #@+node:ekr.20050724075352.91:removeRKeys
    def removeRKeys( self, widget ):
        mrk = 'sel'
        widget.tag_delete( mrk )
        widget.unbind( '<Left>' )
        widget.unbind( '<Right>' )
        widget.unbind( '<Up>' )
        widget.unbind( '<Down>' )
    #@nonl
    #@-node:ekr.20050724075352.91:removeRKeys
    #@+node:ekr.20050724075352.92:_findMatch2
    def _findMatch2( self, svar, fdict = None ):#, fdict = self.doAltX ):
        '''This method returns a sorted list of matches.'''
        if not fdict:
            fdict = self.doAltX
        txt = svar.get()
        if not txt.isspace() and txt != '':
            txt = txt.strip()
            pmatches = filter( lambda a : a.startswith( txt ), fdict )
        else:
            pmatches = []
        pmatches.sort()
        return pmatches
        #if pmatches:
        #    #mstring = reduce( self.findPre, pmatches )
        #    #return mstring
        #return txt
    #@nonl
    #@-node:ekr.20050724075352.92:_findMatch2
    #@+node:ekr.20050724075352.93:_findMatch
    def _findMatch( self, svar, fdict = None ):#, fdict = self.doAltX ):
        '''This method finds the first match it can find in a sorted list'''
        if not fdict:
            fdict = self.doAltX
        txt = svar.get()
        pmatches = filter( lambda a : a.startswith( txt ), fdict )
        pmatches.sort()
        if pmatches:
            mstring = reduce( self.findPre, pmatches )
            return mstring
        return txt
    #@nonl
    #@-node:ekr.20050724075352.93:_findMatch
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.84:pure utility methods
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.53:general utility methods
    #@+node:ekr.20050724075352.299:goto methods
    #@+at
    # These methods take the user to a specific line or a specific character 
    # in the buffer
    # 
    # 
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.300:startGoto
    def startGoto( self, event , ch = False):
        #global goto
        #self.goto = True
        if not ch:
            self.mcStateManager.setState( 'goto', 1 )
        else:
            self.mcStateManager.setState( 'goto', 2 )
        #label = self.mbuffers[ event.widget ] 
        svar , label = self.getSvarLabel( event )
        svar.set( '' )
        label.configure( background = 'lightblue' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.300:startGoto
    #@+node:ekr.20050724075352.301:Goto
    def Goto( self, event ):
        #global goto
        widget = event.widget
        svar, label = self.getSvarLabel( event )
        if event.keysym == 'Return':
              i = svar.get()
              self.resetMiniBuffer( event )
              #self.goto = False
              state = self.mcStateManager.getState( 'goto' )
              self.mcStateManager.setState( 'goto', False )
              if i.isdigit():
                  
                  if state == 1:
                    widget.mark_set( 'insert', '%s.0' % i )
                  elif state == 2:
                    widget.mark_set( 'insert', '1.0 +%sc' % i )
                  widget.event_generate( '<Key>' )
                  widget.update_idletasks()
                  widget.see( 'insert' )
              return 'break'
        t = svar.get()
        if event.char == '\b':
               if len( t ) == 1:
                   t = ''
               else:
                   t = t[ 0 : -1 ]
               svar.set( t )
        else:
                t = t + event.char
                svar.set( t )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.301:Goto
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.299:goto methods
    #@+node:ekr.20050724075352.153:how many methods
    #@+others
    #@+node:ekr.20050724075352.154:howMany
    #self.howM = False
    def howMany( self, event ):
        #global howM
        svar, label = self.getSvarLabel( event )
        if event.keysym == 'Return':
            tbuffer = event.widget
            txt = tbuffer.get( '1.0', 'end' )
            import re
            reg1 = svar.get()
            reg = re.compile( reg1 )
            i = reg.findall( txt )
            svar.set( '%s occurances found of %s' % (len(i), reg1 ) )
            self.setLabelGrey( label )
            #self.howM = False
            self.mcStateManager.setState( 'howM', False )
            return 'break'
        self.setSvar( event, svar )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.154:howMany
    #@+node:ekr.20050724075352.155:startHowMany
    def startHowMany( self, event ):
        #global howM
        #self.howM = True
        self.mcStateManager.setState( 'howM', True )
        svar, label = self.getSvarLabel( event )
        svar.set( '' )
        self.setLabelBlue( label )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.155:startHowMany
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.153:how many methods
    #@+node:ekr.20050724075352.97:Label ( minibuffer ) and svar methods
    #@+at
    # Two closely related categories under this one heading.  Svars are the 
    # internals of the minibuffer
    # and the labels are the presentation of those internals
    # 
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.98:label( minibuffer ) methods
    #@+node:ekr.20050724075352.99:setLabelGrey
    def setLabelGrey( self, label ):
        label.configure( background = 'lightgrey' )
    #@nonl
    #@-node:ekr.20050724075352.99:setLabelGrey
    #@+node:ekr.20050724075352.100:setLabelBlue
    def setLabelBlue( self ,label ):
        label.configure( background = 'lightblue' )
    #@nonl
    #@-node:ekr.20050724075352.100:setLabelBlue
    #@+node:ekr.20050724075352.101:resetMiniBuffer
    def resetMiniBuffer( self, event ):
        svar, label = self.getSvarLabel( event )
        svar.set( '' )
        label.configure( background = 'lightgrey' )
    #@nonl
    #@-node:ekr.20050724075352.101:resetMiniBuffer
    #@-node:ekr.20050724075352.98:label( minibuffer ) methods
    #@+node:ekr.20050724075352.102:svar methods
    #@+at
    # These methods get and alter the Svar variable which is a Tkinter
    # StringVar.  This StringVar contains what is displayed in the minibuffer.
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.103:getSvarLabel
    def getSvarLabel( self, event ):
        
        '''returns the StringVar and Label( minibuffer ) for a specific Text editor'''
        svar = self.svars[ event.widget ]
        label = self.mbuffers[ event.widget ]
        return svar, label
    #@nonl
    #@-node:ekr.20050724075352.103:getSvarLabel
    #@+node:ekr.20050724075352.104:setSvar
    def setSvar( self, event, svar ):
        '''Alters the StringVar svar to represent the change in the event.
           It mimics what would happen with the keyboard and a Text editor
           instead of plain accumalation.''' 
        t = svar.get()  
        if event.char == '\b':
               if len( t ) == 1:
                   t = ''
               else:
                   t = t[ 0 : -1 ]
               svar.set( t )
        else:
                t = t + event.char
                svar.set( t )
    #@nonl
    #@-node:ekr.20050724075352.104:setSvar
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.102:svar methods
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.97:Label ( minibuffer ) and svar methods
    #@+node:ekr.20050724075352.295:line methods
    #@+at
    # 
    # flush-lines
    # Delete each line that contains a match for regexp, operating on the text 
    # after point. In Transient Mark mode, if the region is active, the 
    # command operates on the region instead.
    # 
    # 
    # keep-lines
    # Delete each line that does not contain a match for regexp, operating on 
    # the text after point. In Transient Mark mode, if the region is active, 
    # the command operates on the region instead.
    # 
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.296:alterLines
    def alterLines( self, event, which ):
        
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        end = 'end'
        if tbuffer.tag_ranges( 'sel' ):
            i = tbuffer.index( 'sel.first' )
            end = tbuffer.index( 'sel.last' )
            
        txt = tbuffer.get( i, end )
        tlines = txt.splitlines( True )
        if which == 'flush':
            keeplines = list( tlines )
        else:
            keeplines = []
        svar, label = self.getSvarLabel( event )
        pattern = svar.get()
        try:
            regex = re.compile( pattern )
            for n , z in enumerate( tlines ):
                f = regex.findall( z )
                if which == 'flush' and f:
                    keeplines[ n ] = None
                elif f:
                    keeplines.append( z )
        except Exception,x:
            return
        
        if which == 'flush':
            keeplines = [ x for x in keeplines if x != None ]
        tbuffer.delete( i, end )
        tbuffer.insert( i, ''.join( keeplines ) )
        tbuffer.mark_set( 'insert', i )
        self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.296:alterLines
    #@+node:ekr.20050724075352.297:processLines
    def processLines( self, event ):
        svar, label = self.getSvarLabel( event )
    
        state = self.mcStateManager.getState( 'alterlines' )
        if state.startswith( 'start' ):
            state = state[ 5: ]
            self.mcStateManager.setState( 'alterlines', state )
            svar.set( '' )
           
    
            
        if event.keysym == 'Return':
           
            self.alterLines( event, state )
                
            return self.keyboardQuit( event )    
            
            
        else:
            self.setSvar( event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.297:processLines
    #@+node:ekr.20050724075352.298:startLines
    def startLines( self , event, which = 'flush' ):
    
        self.keyboardQuit( event )
        tbuffer = event.widget
        self.mcStateManager.setState( 'alterlines', 'start%s' % which )
        svar, label = self.getSvarLabel( event )
        label.configure( background = 'lightblue' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.298:startLines
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.295:line methods
    #@+node:ekr.20050724075352.156:paragraph methods
    #@+others
    #@+node:ekr.20050724075352.157:selectParagraph
    def selectParagraph( self, event ):
        tbuffer = event.widget
        txt = tbuffer.get( 'insert linestart', 'insert lineend' )
        txt = txt.lstrip().rstrip()
        i = tbuffer.index( 'insert' )
        if not txt:
            while 1:
                i = tbuffer.index( '%s + 1 lines' % i )
                txt = tbuffer.get( '%s linestart' % i, '%s lineend' % i )
                txt = txt.lstrip().rstrip()
                if txt:
                    self._selectParagraph( tbuffer, i )
                    break
                if tbuffer.index( '%s lineend' % i ) == tbuffer.index( 'end' ):
                    return 'break'
        if txt:
            while 1:
                i = tbuffer.index( '%s - 1 lines' % i )
                txt = tbuffer.get( '%s linestart' % i, '%s lineend' % i )
                txt = txt.lstrip().rstrip()
                if not txt or tbuffer.index( '%s linestart' % i ) == tbuffer.index( '1.0' ):
                    if not txt:
                        i = tbuffer.index( '%s + 1 lines' % i )
                    self._selectParagraph( tbuffer, i )
                    break     
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.157:selectParagraph
    #@+node:ekr.20050724075352.158:_selectParagraph
    def _selectParagraph( self, tbuffer, start ):
        i2 = start
        while 1:
            txt = tbuffer.get( '%s linestart' % i2, '%s lineend' % i2 )
            if tbuffer.index( '%s lineend' % i2 )  == tbuffer.index( 'end' ):
                break
            txt = txt.lstrip().rstrip()
            if not txt: break
            else:
                i2 = tbuffer.index( '%s + 1 lines' % i2 )
        tbuffer.tag_add( 'sel', '%s linestart' % start, '%s lineend' % i2 )
        tbuffer.mark_set( 'insert', '%s lineend' % i2 )
    #@nonl
    #@-node:ekr.20050724075352.158:_selectParagraph
    #@+node:ekr.20050724075352.159:killParagraph
    def killParagraph( self, event ):
        
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        txt = tbuffer.get( 'insert linestart', 'insert lineend' )
        if not txt.rstrip().lstrip():
            i = tbuffer.search( r'\w', i, regexp = True, stopindex = 'end' )
        self._selectParagraph( tbuffer, i )
        i2 = tbuffer.index( 'insert' )
        self.kill( event, i, i2 )
        tbuffer.mark_set( 'insert', i )
        tbuffer.selection_clear()
        return self._tailEnd( tbuffer )
    #@-node:ekr.20050724075352.159:killParagraph
    #@+node:ekr.20050724075352.160:backwardKillParagraph
    def backwardKillParagraph( self, event ):   
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        i2 = i
        txt = tbuffer.get( 'insert linestart', 'insert lineend' )
        if not txt.rstrip().lstrip():
            self.movingParagraphs( event, -1 )
            i2 = tbuffer.index( 'insert' )
        self.selectParagraph( event )
        i3 = tbuffer.index( 'sel.first' )
        self.kill( event, i3, i2 )
        tbuffer.mark_set( 'insert', i )
        tbuffer.selection_clear()
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.160:backwardKillParagraph
    #@+node:ekr.20050724075352.202:UNTESTED
    #@+at
    # 
    # untested as of yet for .5 conversion.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.203:movingParagraphs
    def movingParagraphs( self, event, way ):
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        
        if way == 1:
            while 1:
                txt = tbuffer.get( '%s linestart' % i, '%s lineend' %i )
                txt = txt.rstrip().lstrip()
                if not txt:
                    i = tbuffer.search( r'\w', i, regexp = True, stopindex = 'end' )
                    i = '%s' %i
                    break
                else:
                    i = tbuffer.index( '%s + 1 lines' % i )
                    if tbuffer.index( '%s linestart' % i ) == tbuffer.index( 'end' ):
                        i = tbuffer.search( r'\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                        i = '%s + 1c' % i
                        break
        else:
            while 1:
                txt = tbuffer.get( '%s linestart' % i, '%s lineend' %i )
                txt = txt.rstrip().lstrip()
                if not txt:
                    i = tbuffer.search( r'\w', i, backwards = True, regexp = True, stopindex = '1.0' )
                    i = '%s +1c' %i
                    break
                else:
                    i = tbuffer.index( '%s - 1 lines' % i )
                    if tbuffer.index( '%s linestart' % i ) == '1.0':
                        i = tbuffer.search( r'\w', '1.0', regexp = True, stopindex = 'end' )
                        break
        if i : 
            tbuffer.mark_set( 'insert', i )
            tbuffer.see( 'insert' )
            return self._tailEnd( tbuffer )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.203:movingParagraphs
    #@+node:ekr.20050724075352.204:fillParagraph
    def fillParagraph( self, event ):
        tbuffer = event.widget
        txt = tbuffer.get( 'insert linestart', 'insert lineend' )
        txt = txt.lstrip().rstrip()
        if txt:
            i = tbuffer.index( 'insert' )
            i2 = i
            txt2 = txt
            while txt2:
                pi2 = tbuffer.index( '%s - 1 lines' % i2)
                txt2 = tbuffer.get( '%s linestart' % pi2, '%s lineend' % pi2 )
                if tbuffer.index( '%s linestart' % pi2 ) == '1.0':
                    i2 = tbuffer.search( '\w', '1.0', regexp = True, stopindex = 'end' )
                    break
                if txt2.lstrip().rstrip() == '': break
                i2 = pi2
            i3 = i
            txt3 = txt
            while txt3:
                pi3 = tbuffer.index( '%s + 1 lines' %i3 )
                txt3 = tbuffer.get( '%s linestart' % pi3, '%s lineend' % pi3 )
                if tbuffer.index( '%s lineend' % pi3 ) == tbuffer.index( 'end' ):
                    i3 = tbuffer.search( '\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                    break
                if txt3.lstrip().rstrip() == '': break
                i3 = pi3
            ntxt = tbuffer.get( '%s linestart' %i2, '%s lineend' %i3 )
            ntxt = self._addPrefix( ntxt )
            tbuffer.delete( '%s linestart' %i2, '%s lineend' % i3 )
            tbuffer.insert( i2, ntxt )
            tbuffer.mark_set( 'insert', i )
            return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.204:fillParagraph
    #@+node:ekr.20050724075352.205:fillRegionAsParagraph
    def fillRegionAsParagraph( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        i1 = tbuffer.index( 'sel.first linestart' )
        i2 = tbuffer.index( 'sel.last lineend' )
        txt = tbuffer.get(  i1,  i2 )
        txt = self._addPrefix( txt )
        tbuffer.delete( i1, i2 )
        tbuffer.insert( i1, txt )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.205:fillRegionAsParagraph
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.202:UNTESTED
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.156:paragraph methods
    #@+node:ekr.20050724075352.246:range methods
    #@+others
    #@+node:ekr.20050724075352.247:inRange
    def inRange( self, widget, range, l = '', r = '' ):
        ranges = widget.tag_ranges( range )
        #i = widget.index( 'insert' )
        for z in xrange( 0,  len( ranges) , 2 ):
            z1 = z + 1
            l1 = 'insert%s' %l
            r1 = 'insert%s' % r
            if widget.compare( l1, '>=', ranges[ z ]) and widget.compare( r1, '<=', ranges[ z1] ):
                return True
        return False
    #@nonl
    #@-node:ekr.20050724075352.247:inRange
    #@+node:ekr.20050724075352.248:contRanges
    def contRanges( self, widget, range ):
        ranges = widget.tag_ranges( range)
        t1 = widget.get( ranges[ 0 ], ranges[ -1 ] )
        t2 = []
        for z in xrange( 0,  len( ranges) , 2 ):
            z1 = z + 1
            t2.append( widget.get( ranges[ z ], ranges[ z1 ] ) )
        t2 = '\n'.join( t2 )
        return t1 == t2
    #@nonl
    #@-node:ekr.20050724075352.248:contRanges
    #@+node:ekr.20050724075352.249:testinrange
    def testinrange( self, widget ):
        mrk = 'sel'
        #ranges = widget.tag_ranges( mrk)
        if not self.inRange( widget , mrk) or not self.contRanges( widget, mrk ):
            self.removeRKeys( widget )
            return False
        return True
    #@nonl
    #@-node:ekr.20050724075352.249:testinrange
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.246:range methods
    #@+node:ekr.20050724075352.265:Rectangles methods
    #@+others
    #@+node:ekr.20050724075352.266:activateRectangleMethods
    def activateRectangleMethods( self, event ):
        
        self.rectanglemode = 1
        svar = self.svars[ event.widget ]
        svar.set( 'C - x r' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.266:activateRectangleMethods
    #@+node:ekr.20050724075352.267:openRectangle
    def openRectangle( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        lth = ' ' * ( r4 - r2 )
        self.stopControlX( event )
        while r1 <= r3:
            tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth)
            r1 = r1 + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.267:openRectangle
    #@+node:ekr.20050724075352.268:clearRectangle
    def clearRectangle( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        lth = ' ' * ( r4 - r2 )
        self.stopControlX( event )
        while r1 <= r3:
            tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
            tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth)
            r1 = r1 + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.268:clearRectangle
    #@+node:ekr.20050724075352.269:deleteRectangle
    def deleteRectangle( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        #lth = ' ' * ( r4 - r2 )
        self.stopControlX( event )
        while r1 <= r3:
            tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
            r1 = r1 + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.269:deleteRectangle
    #@+node:ekr.20050724075352.270:stringRectangle
    #self.sRect = False   
    def stringRectangle( self, event ):
        #global sRect
        svar, label = self.getSvarLabel( event )
        if not self.sRect:
            self.sRect = 1
            svar.set( 'String rectangle :' )
            self.setLabelBlue( label )
            return 'break'
        if event.keysym == 'Return':
            self.sRect = 3
        if self.sRect == 1:
            svar.set( '' )
            self.sRect = 2
        if self.sRect == 2:
            self.setSvar( event, svar )
            return 'break'
        if self.sRect == 3:
            if not self._chckSel( event ):
                self.stopControlX( event )
                return
            tbuffer = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints( event )
            lth = svar.get()
            #self.stopControlX( event )
            while r1 <= r3:
                tbuffer.delete( '%s.%s' % ( r1, r2 ),  '%s.%s' % ( r1, r4 ) )
                tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth )
                r1 = r1 + 1
            #i = tbuffer.index( 'insert' )
            #tbuffer.mark_set( 'insert', 'insert wordend' )
            #tbuffer.tag_remove( 'sel', '1.0', 'end' )
            #return self._tailEnd( tbuffer )
            self.stopControlX( event )
            return self._tailEnd( tbuffer )
            #return 'break'
            #return 'break'
            #tbuffer.mark_set( 'insert', i )
            #return 'break'
    #@nonl
    #@-node:ekr.20050724075352.270:stringRectangle
    #@+node:ekr.20050724075352.271:killRectangle
    #self.krectangle = None       
    def killRectangle( self, event ):
        #global krectangle
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        #lth = ' ' * ( r4 - r2 )
        self.stopControlX( event )
        self.krectangle = []
        while r1 <= r3:
            txt = tbuffer.get( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
            self.krectangle.append( txt )
            tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
            r1 = r1 + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.271:killRectangle
    #@+node:ekr.20050724075352.272:closeRectangle
    def closeRectangle( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event ) 
        ar1 = r1
        txt = []
        while ar1 <= r3:
            txt.append( tbuffer.get( '%s.%s' %( ar1, r2 ), '%s.%s' %( ar1, r4 ) ) )
            ar1 = ar1 + 1 
        for z in txt:
            if z.lstrip().rstrip():
                return
        while r1 <= r3:
            tbuffer.delete( '%s.%s' %(r1, r2 ), '%s.%s' %( r1, r4 ) )
            r1 = r1 + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.272:closeRectangle
    #@+node:ekr.20050724075352.273:yankRectangle
    def yankRectangle( self, event , krec = None ):
        self.stopControlX( event )
        if not krec:
            krec = self.krectangle
        if not krec:
            return 'break'
        tbuffer = event.widget
        txt = tbuffer.get( 'insert linestart', 'insert' )
        txt = self.getWSString( txt )
        i = tbuffer.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = int( i1 )
        for z in krec:        
            txt2 = tbuffer.get( '%s.0 linestart' % i1, '%s.%s' % ( i1, i2 ) )
            if len( txt2 ) != len( txt ):
                amount = len( txt ) - len( txt2 )
                z = txt[ -amount : ] + z
            tbuffer.insert( '%s.%s' %( i1, i2 ) , z )
            if tbuffer.index( '%s.0 lineend +1c' % i1 ) == tbuffer.index( 'end' ):
                tbuffer.insert( '%s.0 lineend' % i1, '\n' )
            i1 = i1 + 1
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.273:yankRectangle
    #@+node:ekr.20050724075352.274:getRectanglePoints
    def getRectanglePoints( self, event ):
        tbuffer = event.widget
        i = tbuffer.index( 'sel.first' )
        i2 = tbuffer.index( 'sel.last' )
        r1, r2 = i.split( '.' )
        r3, r4 = i2.split( '.' )
        r1 = int( r1 )
        r2 = int( r2 )
        r3 = int( r3 )
        r4 = int( r4 )
        return r1, r2, r3, r4
    #@nonl
    #@-node:ekr.20050724075352.274:getRectanglePoints
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.265:Rectangles methods
    #@+node:ekr.20050724075352.213:region methods
    #@+others
    #@+node:ekr.20050724075352.214:fillRegion
    def fillRegion( self, event ):
        if not self._chckSel( event ):
            return
        tbuffer = event.widget
        #i = tbuffer.index( 'insert' ) 
        s1 = tbuffer.index( 'sel.first' )
        s2 = tbuffer.index( 'sel.last' )
        tbuffer.mark_set( 'insert', s1 )
        self.movingParagraphs( event, -1 )
        if tbuffer.index( 'insert linestart' ) == '1.0':
            self.fillParagraph( event )
        while 1:
            self.movingParagraphs( event, 1 )
            if tbuffer.compare( 'insert', '>', s2 ):
                break
            self.fillParagraph( event )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.214:fillRegion
    #@+node:ekr.20050724075352.215:setRegion
    def setRegion( self, event ):   
        mrk = 'sel'
        tbuffer = event.widget
        def extend( event ):
            widget = event.widget
            widget.mark_set( 'insert', 'insert + 1c' )
            if self.inRange( widget, mrk ):
                widget.tag_remove( mrk, 'insert -1c' )
            else:
                widget.tag_add( mrk, 'insert -1c' )
                widget.tag_configure( mrk, background = 'lightgrey' )
                self.testinrange( widget )
            return 'break'
            
        def truncate( event ):
            widget = event.widget
            widget.mark_set( 'insert', 'insert -1c' )
            if self.inRange( widget, mrk ):
                self.testinrange( widget )
                widget.tag_remove( mrk, 'insert' )
            else:
                widget.tag_add( mrk, 'insert' )
                widget.tag_configure( mrk, background = 'lightgrey' )
                self.testinrange( widget  )
            return 'break'
            
        def up( event ):
            widget = event.widget
            if not self.testinrange( widget ):
                return 'break'
            widget.tag_add( mrk, 'insert linestart', 'insert' )
            i = widget.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = str( int( i1 ) - 1 )
            widget.mark_set( 'insert', i1+'.'+i2)
            widget.tag_add( mrk, 'insert', 'insert lineend + 1c' )
            if self.inRange( widget, mrk ,l = '-1c', r = '+1c') and widget.index( 'insert' ) != '1.0':
                widget.tag_remove( mrk, 'insert', 'end' )  
            return 'break'
            
        def down( event ):
            widget = event.widget
            if not self.testinrange( widget ):
                return 'break'
            widget.tag_add( mrk, 'insert', 'insert lineend' )
            i = widget.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = str( int( i1 ) + 1 )
            widget.mark_set( 'insert', i1 +'.'+i2 )
            widget.tag_add( mrk, 'insert linestart -1c', 'insert' )
            if self.inRange( widget, mrk , l = '-1c', r = '+1c' ): 
                widget.tag_remove( mrk, '1.0', 'insert' )
            return 'break'
            
        extend( event )   
        tbuffer.bind( '<Right>', extend, '+' )
        tbuffer.bind( '<Left>', truncate, '+' )
        tbuffer.bind( '<Up>', up, '+' )
        tbuffer.bind( '<Down>', down, '+' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.215:setRegion
    #@+node:ekr.20050724075352.216:indentRegion
    def indentRegion( self, event ):
        tbuffer = event.widget
        mrk = 'sel'
        trange = tbuffer.tag_ranges( mrk )
        if len( trange ) != 0:
            ind = tbuffer.search( '\w', '%s linestart' % trange[ 0 ], stopindex = 'end', regexp = True )
            if not ind : return
            text = tbuffer.get( '%s linestart' % ind ,  '%s lineend' % ind)
            sstring = text.lstrip()
            sstring = sstring[ 0 ]
            ws = text.split( sstring )
            if len( ws ) > 1:
                ws = ws[ 0 ]
            else:
                ws = ''
            s , s1 = trange[ 0 ].split( '.' )
            e , e1 = trange[ -1 ].split( '.' )
            s = int( s )
            s = s + 1
            e = int( e ) + 1
            for z in xrange( s , e ):
                t2 = tbuffer.get( '%s.0' %z ,  '%s.0 lineend'%z)
                t2 = t2.lstrip()
                t2 = ws + t2
                tbuffer.delete( '%s.0' % z ,  '%s.0 lineend' %z)
                tbuffer.insert( '%s.0' % z, t2 )
            tbuffer.event_generate( '<Key>' )
            tbuffer.update_idletasks()
        self.removeRKeys( tbuffer )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.216:indentRegion
    #@+node:ekr.20050724075352.217:tabIndentRegion
    def tabIndentRegion( self,event ):
        tbuffer = event.widget
        if not self._chckSel( event ):
            return
        i = tbuffer.index( 'sel.first' )
        i2 = tbuffer.index( 'sel.last' )
        i = tbuffer.index( '%s linestart' %i )
        i2 = tbuffer.index( '%s linestart' % i2)
        while 1:
            tbuffer.insert( i, '\t' )
            if i == i2: break
            i = tbuffer.index( '%s + 1 lines' % i )    
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.217:tabIndentRegion
    #@+node:ekr.20050724075352.218:countRegion
    def countRegion( self, event ):
        tbuffer = event.widget
        txt = tbuffer.get( 'sel.first', 'sel.last')
        svar = self.svars[ tbuffer ]
        lines = 1
        chars = 0
        for z in txt:
            if z == '\n': lines = lines + 1
            else:
                chars = chars + 1       
        svar.set( 'Region has %s lines, %s characters' %( lines, chars ) )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.218:countRegion
    #@+node:ekr.20050724075352.219:reverseRegion
    def reverseRegion( self, event ):
        tbuffer = event.widget
        if not self._chckSel( event ):
            return
        ins = tbuffer.index( 'insert' )
        is1 = tbuffer.index( 'sel.first' )
        is2 = tbuffer.index( 'sel.last' )    
        txt = tbuffer.get( '%s linestart' % is1, '%s lineend' %is2 )
        tbuffer.delete( '%s linestart' % is1, '%s lineend' %is2  )
        txt = txt.split( '\n' )
        txt.reverse()
        istart = is1.split( '.' )
        istart = int( istart[ 0 ] )
        for z in txt:
            tbuffer.insert( '%s.0' % istart, '%s\n' % z )
            istart = istart + 1
        tbuffer.mark_set( 'insert', ins )
        self.mcStateManager.clear()
        self.resetMiniBuffer( event )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.219:reverseRegion
    #@+node:ekr.20050724075352.220:upperLowerRegion
    def upperLowerRegion( self, event, way ):
        tbuffer = event.widget
        mrk = 'sel'
        trange = tbuffer.tag_ranges( mrk )
        if len( trange ) != 0:
            text = tbuffer.get( trange[ 0 ] , trange[ -1 ] )
            i = tbuffer.index( 'insert' )
            if text == ' ': return 'break'
            tbuffer.delete( trange[ 0 ], trange[ -1 ] )
            if way == 'low':
                text = text.lower()
            if way == 'up':
                text = text.upper()
            tbuffer.insert( 'insert', text )
            tbuffer.mark_set( 'insert', i ) 
        self.removeRKeys( tbuffer )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.220:upperLowerRegion
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.213:region methods
    #@+node:ekr.20050724075352.316:shell and subprocess
    #@+others
    #@+node:ekr.20050724075352.317:def startSubprocess
    def startSubprocess( self, event, which = 0 ):
        
        svar, label = self.getSvarLabel( event )
        statecontents = { 'state':'start', 'payload': None }
        self.mcStateManager.setState( 'subprocess', statecontents )
        if which:
            tbuffer = event.widget
            svar.set( "Shell command on region:" )
            is1 = is2 = None
            try:
                is1 = tbuffer.index( 'sel.first' )
                is2 = tbuffer.index( 'sel.last' )
            finally:
                if is1:
                    statecontents[ 'payload' ] = tbuffer.get( is1, is2 )
                else:
                    return self.keyboardQuit( event )
        else:
            svar.set( "Alt - !:" )
        self.setLabelBlue( label )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.317:def startSubprocess
    #@+node:ekr.20050724075352.318:subprocess
    def subprocesser( self, event ):
        
        state = self.mcStateManager.getState( 'subprocess' )
        svar, label = self.getSvarLabel( event )
        if state[ 'state' ] == 'start':
            state[ 'state' ] = 'watching'
            svar.set( "" )
        
        if event.keysym == "Return":
            #cmdline = svar.get().split()
            cmdline = svar.get()
            return self.executeSubprocess( event, cmdline, input=state[ 'payload' ] )
           
        else:
            self.setSvar(  event, svar )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.318:subprocess
    #@+node:ekr.20050724075352.319:executeSubprocess
    def executeSubprocess( self, event, command  ,input = None ):
        import subprocess
        try:
            try:
                out ,err = os.tmpnam(), os.tmpnam()
                ofile = open( out, 'wt+' ) 
                efile = open( err, 'wt+' )
                process = subprocess.Popen( command, bufsize=-1, 
                                            stdout = ofile.fileno(), 
                                            stderr= ofile.fileno(), 
                                            stdin=subprocess.PIPE,
                                            shell=True )
                if input:
                    process.communicate( input )
                process.wait()   
                tbuffer = event.widget
                efile.seek( 0 )
                errinfo = efile.read()
                if errinfo:
                    tbuffer.insert( 'insert', errinfo )
                ofile.seek( 0 )
                okout = ofile.read()
                if okout:
                    tbuffer.insert( 'insert', okout )
            except Exception, x:
                tbuffer = event.widget
                tbuffer.insert( 'insert', x )
        finally:
            os.remove( out )
            os.remove( err )
        self.keyboardQuit( event )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.319:executeSubprocess
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.316:shell and subprocess
    #@+node:ekr.20050724075352.94:shutdown methods
    #@+others
    #@+node:ekr.20050724075352.95:shutdown
    def shutdown( self, event ):
        
        self.shuttingdown = True
        if self.shutdownhook:
            self.shutdownhook()
        else:
            sys.exit( 0 )
    #@nonl
    #@-node:ekr.20050724075352.95:shutdown
    #@+node:ekr.20050724075352.96:setShutdownHook
    def setShutdownHook( self, hook ):
            
        self.shutdownhook = hook
    #@nonl
    #@-node:ekr.20050724075352.96:setShutdownHook
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.94:shutdown methods
    #@+node:ekr.20050724075352.279:sort methods
    #@+others
    #@+node:ekr.20050724075352.280:sortLines
    def sortLines( self, event , which = None ):
        tbuffer = event.widget  
        if not self._chckSel( event ):
            return self.keyboardQuit( event )
    
        i = tbuffer.index( 'sel.first' )
        i2 = tbuffer.index( 'sel.last' )
        is1 = i.split( '.' )
        is2 = i2.split( '.' )
        txt = tbuffer.get( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
        ins = tbuffer.index( 'insert' )
        txt = txt.split( '\n' )
        tbuffer.delete( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
        txt.sort()
        if which:
            txt.reverse()
        inum = int(is1[ 0 ])
        for z in txt:
            tbuffer.insert( '%s.0' % inum, '%s\n' % z ) 
            inum = inum + 1
        tbuffer.mark_set( 'insert', ins )
        self.keyboardQuit( event )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.280:sortLines
    #@+node:ekr.20050724075352.281:sortColumns
    def sortColumns( self, event ):
        tbuffer = event.widget
        if not self._chckSel( event ):
            return self.keyboardQuit( event )
            
        ins = tbuffer.index( 'insert' )
        is1 = tbuffer.index( 'sel.first' )
        is2 = tbuffer.index( 'sel.last' )   
        sint1, sint2 = is1.split( '.' )
        sint2 = int( sint2 )
        sint3, sint4 = is2.split( '.' )
        sint4 = int( sint4 )
        txt = tbuffer.get( '%s.0' % sint1, '%s.0 lineend' % sint3 )
        tbuffer.delete( '%s.0' % sint1, '%s.0 lineend' % sint3 )
        columns = []
        i = int( sint1 )
        i2 = int( sint3 )
        while i <= i2:
            t = tbuffer.get( '%s.%s' %( i, sint2 ), '%s.%s' % ( i, sint4 ) )
            columns.append( t )
            i = i + 1
        txt = txt.split( '\n' )
        zlist = zip( columns, txt )
        zlist.sort()
        i = int( sint1 )      
        for z in xrange( len( zlist ) ):
             tbuffer.insert( '%s.0' % i, '%s\n' % zlist[ z ][ 1 ] ) 
             i = i + 1
        tbuffer.mark_set( 'insert', ins )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.281:sortColumns
    #@+node:ekr.20050724075352.282:sortFields
    def sortFields( self, event, which = None ):
        tbuffer = event.widget
        if not self._chckSel( event ):
            return self.keyboardQuit( event )
    
        ins = tbuffer.index( 'insert' )
        is1 = tbuffer.index( 'sel.first' )
        is2 = tbuffer.index( 'sel.last' )
        
        txt = tbuffer.get( '%s linestart' % is1, '%s lineend' % is2 )
        txt = txt.split( '\n' )
        fields = []
        import re
        fn = r'\w+'
        frx = re.compile( fn )
        for z in txt:
            f = frx.findall( z )
            if not which:
                fields.append( f[ 0 ] )
            else:
                i =  int( which )
                if len( f ) < i:
                    return self._tailEnd( tbuffer )
                i = i - 1            
                fields.append( f[ i ] )
        nz = zip( fields, txt )
        nz.sort()
        tbuffer.delete( '%s linestart' % is1, '%s lineend' % is2 )
        i = is1.split( '.' )
        #i2 = is2.split( '.' )
        int1 = int( i[ 0 ] )
        for z in nz:
            tbuffer.insert( '%s.0' % int1, '%s\n'% z[1] )
            int1 = int1 + 1
        tbuffer.mark_set( 'insert' , ins )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.282:sortFields
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.279:sort methods
    #@+node:ekr.20050724075352.314:tabify/untabify
    #@+at
    # For the tabify and untabify Alt-x commands.  Turns tabs to spaces and 
    # spaces to tabs in the selection
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.315:tabify
    def tabify( self, event, which='tabify' ):
        
        tbuffer = event.widget
        if tbuffer.tag_ranges( 'sel' ):
            i = tbuffer.index( 'sel.first' )
            end = tbuffer.index( 'sel.last' )
            txt = tbuffer.get( i, end )
            if which == 'tabify':
                
                pattern = re.compile( ' {4,4}' )
                ntxt = pattern.sub( '\t', txt )
    
            else:
                
                pattern = re.compile( '\t' )
                ntxt = pattern.sub( '    ', txt )
            tbuffer.delete( i, end )
            tbuffer.insert( i , ntxt )
            self.keyboardQuit( event )
            return self._tailEnd( tbuffer )
        self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.315:tabify
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.314:tabify/untabify
    #@+node:ekr.20050724075352.289:universal methods
    #@+others
    #@+node:ekr.20050724075352.290:universalDispatch
    #self.uC = False
    def universalDispatch( self, event, stroke ):
        #global uC    
        uC = self.mcStateManager.getState( 'uC' )
        if not uC:
            #self.uC = 1
            self.mcStateManager.setState( 'uC', 1 )
            svar, label = self.getSvarLabel( event )
            svar.set( '' )
            self.setLabelBlue( label ) 
        elif uC == 1:
            self.universalCommand1( event, stroke )
        elif uC == 2:
            self.universalCommand3( event, stroke )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.290:universalDispatch
    #@+node:ekr.20050724075352.291:universalCommand1
    #import string
    #self.uCstring = string.digits + '\b'
    
    def universalCommand1( self, event, stroke ):
        #global uC
        if event.char not in self.uCstring:
            return self.universalCommand2( event, stroke )
        svar, label = self.getSvarLabel( event )
        self.setSvar( event, svar )
        if event.char != '\b':
            svar.set( '%s ' %svar.get() )
    #@nonl
    #@-node:ekr.20050724075352.291:universalCommand1
    #@+node:ekr.20050724075352.292:universalCommand2
    def universalCommand2(  self, event , stroke ):
        #global uC
        #self.uC = False
        #self.mcStateManager.setState( 'uC', False )
        svar, label = self.getSvarLabel( event )
        txt = svar.get()
        self.keyboardQuit( event )
        txt = txt.replace( ' ', '' )
        self.resetMiniBuffer( event )
        if not txt.isdigit(): #This takes us to macro state.  For example Control-u Control-x (  will execute the last macro and begin editing of it.
            if stroke == '<Control-x>':
                #self.uC = 2
                self.mcStateManager.setState( 'uC', 2 )
                return self.universalCommand3( event, stroke )
            return self._tailEnd( event.widget )
        if self.uCdict.has_key( stroke ): #This executes the keystroke 'n' number of times.
                self.uCdict[ stroke ]( event , txt )
        else:
            tbuffer = event.widget
            i = int( txt )
            stroke = stroke.lstrip( '<' ).rstrip( '>' )
            if self.cbDict.has_key( stroke ):
                for z in xrange( i ):
                    method = self.cbDict[ stroke ]
                    ev = Tk.Event()
                    ev.widget = event.widget
                    ev.keysym = event.keysym
                    ev.keycode = event.keycode
                    ev.char = event.char
                    self.masterCommand( ev , method, '<%s>' % stroke )
            else:
                for z in xrange( i ):
                    tbuffer.event_generate( '<Key>', keycode = event.keycode, keysym = event.keysym )
                    self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.292:universalCommand2
    #@+node:ekr.20050724075352.293:universalCommand3
    #self.uCdict = { '<Alt-x>' : alt_X }
    def universalCommand3( self, event, stroke ):
        svar, label = self.getSvarLabel( event )
        svar.set( 'Control-u %s' % stroke.lstrip( '<' ).rstrip( '>' ) )
        self.setLabelBlue( label )
        if event.keysym == 'parenleft':
            self.keyboardQuit( event )
            self.startKBDMacro( event )
            self.executeLastMacro( event )
            return 'break'
    #@nonl
    #@-node:ekr.20050724075352.293:universalCommand3
    #@+node:ekr.20050724075352.294:numberCommand
    def numberCommand( self, event, stroke, number ):
        self.universalDispatch( event, stroke )
        tbuffer = event.widget
        tbuffer.event_generate( '<Key>', keysym = number )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.294:numberCommand
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.289:universal methods
    #@+node:ekr.20050724075352.239:Zap methods
    #@+at
    # These methods start and execute the Zap to functionality.
    #@-at
    #@@c
    
    
    
    #@+others
    #@+node:ekr.20050724075352.240:startZap
    def startZap( self, event ):
        #global zap
        #self.zap = True
        self.mcStateManager.setState( 'zap', True )
        svar, label = self.getSvarLabel( event )
        label.configure( background = 'lightblue' )
        svar.set( 'Zap To Character' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.240:startZap
    #@+node:ekr.20050724075352.241:zapTo
    def zapTo( self, event ):
            #global zap
    
            widget = event.widget
            s = string.ascii_letters + string.digits + string.punctuation
            if len( event.char ) != 0 and event.char in s:
                #self.zap = False
                self.mcStateManager.setState( 'zap', False )
                i = widget.search( event.char , 'insert',  stopindex = 'end' )
                self.resetMiniBuffer( event )
                if i:
                    t = widget.get( 'insert', '%s+1c'% i )
                    self.addToKillBuffer( t )
                    widget.delete( 'insert', '%s+1c' % i)
                    return 'break'
            else:
                return 'break'
    #@nonl
    #@-node:ekr.20050724075352.241:zapTo
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.239:Zap methods
    #@-node:ekr.20050725133033:outer emacs methods
    #@+node:ekr.20050725091822:emacs commands classes
    #@<< define class baseCommands >>
    #@+node:ekr.20050725091822.1:<< define class baseCommands >>
    class baseCommands:
        
        '''The base class for all emacs command classes'''
        
        def init (self,emacs):
            pass
        
        def oops (self):
            print ("emacs baseCommands oops:",
                g.callerName(2),
                "must be overridden in subclass")
                
        def getPublicCommands (self):
            '''Return a dict describing public commands implemented in the subclass.
            Keys are untranslated command names.  Values are methods of the subclass.'''
    
            self.oops()
            return {}
    #@nonl
    #@-node:ekr.20050725091822.1:<< define class baseCommands >>
    #@nl
    
    #@+others
    #@+node:ekr.20050724075352.188:class abbrevCommandsClass
    #@+at
    # 
    # type some text, set its abbreviation with Control-x a i g, type the text 
    # for abbreviation expansion
    # type Control-x a e ( or Alt-x expand-abbrev ) to expand abbreviation
    # type Alt-x abbrev-on to turn on automatic abbreviation expansion
    # Alt-x abbrev-on to turn it off
    # 
    # an example:
    # type:
    # frogs
    # after typing 's' type Control-x a i g.  This will turn the minibuffer 
    # blue, type in your definition. For example: turtles.
    # 
    # Now in the buffer type:
    # frogs
    # after typing 's' type Control-x a e.  This will turn the 'frogs' into:
    # turtles
    #@-at
    #@@c
    
    class abbrevCommandsClass (baseCommands):
    
        #@    @+others
        #@+node:ekr.20050725125153: ctor
        def __init__ (self,emacs):
            
            self.emacs = emacs
        
            # Delegators...
            self.keyboardQuit = emacs.keyboardQuit
            self.mcStateManager = emacs.mcStateManager
            self.getSvarLabel = emacs.getSvarLabel
            self.setSvar = emacs.setSvar
        
            # Set ivars in emacs.
            self.emacs.abbrevMode = False 
            self.emacs.abbrevOn = False # determines if abbreviations are on for masterCommand and toggle abbreviations.
        
            # Set local ivars.
            self.abbrevs ={}
        #@nonl
        #@-node:ekr.20050725125153: ctor
        #@+node:ekr.20050725130925.1: getPublicCommands
        def getPublicCommands (self):
            
            return {
                'abbrev-mode':              self.toggleAbbrevMode,
                'expand-abbrev':            self.expandAbbrev,
                'expand-region-abbrevs':    self.regionalExpandAbbrev,
                'kill-all-abbrevs':         self.killAllAbbrevs,
                'list-abbrevs':             self.listAbbrevs,
                'read-abbrev-file':         self.readAbbreviations,
                'write-abbrev-file':        self.writeAbbreviations,
            }
        #@nonl
        #@-node:ekr.20050725130925.1: getPublicCommands
        #@+node:ekr.20050725130925: Entry points
        #@+node:ekr.20050725135621:expandAbbrev
        def expandAbbrev (self,event):
            
            return self.keyboardQuit(event) and self._expandAbbrev(event)
        #@-node:ekr.20050725135621:expandAbbrev
        #@+node:ekr.20050724075352.195:killAllAbbrevs
        def killAllAbbrevs (self,event):
        
            self.abbrevs = {}
            return self.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.195:killAllAbbrevs
        #@+node:ekr.20050724075352.197:listAbbrevs
        def listAbbrevs (self,event):
        
            svar, label = self.getSvarLabel(event)
            txt = ''
            for z in self.abbrevs:
                txt = '%s%s=%s\n' % (txt,z,self.abbrevs[z])
            svar.set('')
            svar.set(txt)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.197:listAbbrevs
        #@+node:ekr.20050724075352.198:readAbbreviations
        def readAbbreviations (self,event):
        
            f = tkFileDialog.askopenfile()
            if f == None:
                return 'break'
            else:
                return self._readAbbrevs(f)
        #@nonl
        #@-node:ekr.20050724075352.198:readAbbreviations
        #@+node:ekr.20050724075352.192:regionalExpandAbbrev
        def regionalExpandAbbrev( self, event ):
            
            if not self._chckSel( event ):
                return
            
            tbuffer = event.widget
            i1 = tbuffer.index( 'sel.first' )
            i2 = tbuffer.index( 'sel.last' ) 
            ins = tbuffer.index( 'insert' )
            #@    << define a new generator searchXR >>
            #@+node:ekr.20050724075352.193:<< define a new generator searchXR >>
            # EKR: This is a generator (it contains a yield).
            # EKR: To make this work we must define a new generator for each call to regionalExpandAbbrev.
            def searchXR( i1 , i2, ins, event ):
                tbuffer.tag_add( 'sXR', i1, i2 )
                while i1:
                    tr = tbuffer.tag_ranges( 'sXR' )
                    if not tr: break
                    i1 = tbuffer.search( r'\w', i1, stopindex = tr[ 1 ] , regexp = True )
                    if i1:
                        word = tbuffer.get( '%s wordstart' % i1, '%s wordend' % i1 )
                        tbuffer.tag_delete( 'found' )
                        tbuffer.tag_add( 'found',  '%s wordstart' % i1, '%s wordend' % i1 )
                        tbuffer.tag_config( 'found', background = 'yellow' )
                        if self.abbrevs.has_key( word ):
                            svar, label = self.getSvarLabel( event )
                            svar.set( 'Replace %s with %s? y/n' % ( word, self.abbrevs[ word ] ) )
                            yield None
                            if self.regXKey == 'y':
                                ind = tbuffer.index( '%s wordstart' % i1 )
                                tbuffer.delete( '%s wordstart' % i1, '%s wordend' % i1 )
                                tbuffer.insert( ind, self.abbrevs[ word ] )
                        i1 = '%s wordend' % i1
                tbuffer.mark_set( 'insert', ins )
                tbuffer.selection_clear()
                tbuffer.tag_delete( 'sXR' )
                tbuffer.tag_delete( 'found' )
                svar, label = self.getSvarLabel( event )
                svar.set( '' )
                self.setLabelGrey( label )
                self._setRAvars()
            #@nonl
            #@-node:ekr.20050724075352.193:<< define a new generator searchXR >>
            #@nl
            # EKR: the 'result' of calling searchXR is a generator object.
            self.emacs.regXRpl = searchXR( i1, i2, ins, event)
            self.emacs.regXRpl.next() # Call it the first time.
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.192:regionalExpandAbbrev
        #@+node:ekr.20050724075352.196:toggleAbbrevMode
        def toggleAbbrevMode (self,event):
         
            svar, label = self.getSvarLabel(event)
            self.emacs.abbrevOn = not self.emacs.abbrevOn 
            self.keyboardQuit(event)
            svar.set('Abbreviations are ' + g.choose(self.emacs.abbrevOn,'On','Off'))
        #@nonl
        #@-node:ekr.20050724075352.196:toggleAbbrevMode
        #@+node:ekr.20050724075352.200:writeAbbreviations
        def writeAbbreviations (self,event):
        
            f = tkFileDialog.asksaveasfile()
            if f == None:
                return 'break'
            else:
                return self._writeAbbrevs(f)
        #@nonl
        #@-node:ekr.20050724075352.200:writeAbbreviations
        #@-node:ekr.20050725130925: Entry points
        #@+node:ekr.20050724075352.189:abbreviationDispatch
        def abbreviationDispatch (self,event,which):
        
            aM = self.mcStateManager.getState('abbrevMode')
        
            if not aM:
                self.mcStateManager.setState('abbrevMode',which)
                svar, label = self.getSvarLabel(event)
                svar.set('')
                self.setLabelBlue(label)
                return 'break'
            if aM:
                self.abbrevCommand1(event)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.189:abbreviationDispatch
        #@+node:ekr.20050724075352.190:abbrevCommand1
        def abbrevCommand1( self, event ):
        
            if event.keysym == 'Return':
                tbuffer = event.widget
                word = tbuffer.get( 'insert -1c wordstart', 'insert -1c wordend' )
                if word == ' ': return
                svar, label = self.getSvarLabel( event )
                aM = self.mcStateManager.getState( 'abbrevMode' )
                if aM == 1:
                    self.abbrevs[ svar.get() ] = word
                elif aM == 2:
                    self.abbrevs[ word ] = svar.get()
                self.keyboardQuit( event )
                self.resetMiniBuffer( event )
                return 'break'
        
            svar, label = self.getSvarLabel( event )
            self.setSvar( event, svar )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.190:abbrevCommand1
        #@+node:ekr.20050724075352.191:_expandAbbrev
        def _expandAbbrev (self,event):
        
            tbuffer = event.widget 
            word = tbuffer.get('insert -1c wordstart','insert -1c wordend')
            ch = event.char.strip()
        
            if ch: # We must do this: expandAbbrev is called from Alt-x and Control-x, we get two differnt types of data and tbuffer states.
                word = '%s%s'% (word,event.char)
                
            if self.abbrevs.has_key(word):
                tbuffer.delete('insert -1c wordstart','insert -1c wordend')
                tbuffer.insert('insert',self.abbrevs[word])
                return self._tailEnd(tbuffer)
            else:
                return False 
        #@-node:ekr.20050724075352.191:_expandAbbrev
        #@+node:ekr.20050724075352.194:_setRAvars
        def _setRAvars( self ):
        
            self.emacs.regXRpl = self.emacs.regXKey = None
        #@nonl
        #@-node:ekr.20050724075352.194:_setRAvars
        #@+node:ekr.20050724075352.199:_readAbbrevs
        def _readAbbrevs (self,f):
        
            for x in f:
                a, b = x.split('=')
                b = b[:-1]
                self.abbrevs[a] = b 
            f.close()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.199:_readAbbrevs
        #@+node:ekr.20050724075352.201:_writeAbbrevs
        def _writeAbbrevs( self, f ):
        
            for x in self.abbrevs:
                f.write( '%s=%s\n' %( x, self.abbrevs[ x ] ) )
            f.close()
         
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.201:_writeAbbrevs
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.188:class abbrevCommandsClass
    #@+node:ekr.20050724075352.161:class killBufferCommandsClass
    class killBufferCommandsClass (baseCommands):
        
        '''A class to manage the kill buffer.'''
    
        #@    @+others
        #@+node:ekr.20050725115600: ctor
        def __init__ (self,emacs):
            
            self.emacs = emacs
            
            if emacs.useGlobalKillbuffer:
                self.killbuffer = Emacs.global_killbuffer 
            else:
                self.killbuffer = []
                
            self.kbiterator = self.iterateKillBuffer()
            
            # Delegators...
            self.keyboardQuit = emacs.keyboardQuit
            if 0:
                self.mcStateManager = emacs.mcStateManager
                self.getSvarLabel = emacs.getSvarLabel
                self.setSvar = emacs.setSvar
        #@nonl
        #@-node:ekr.20050725115600: ctor
        #@+node:ekr.20050725121247:getPublicCommands
        def getPublicCommands (self):
            
            # 'kill-paragraph':             self.paragraphCommands.killParagraph,
            # 'backward-kill-paragraph':    self.paragraphCommands.backwardKillParagraph,
            
            return {
                'backward-kill-sentence':   self.backwardKillSentence,
                'backward-kill-word':       self.backwardKillWord,
                'kill-line':                self.killLine,
                'kill-word':                self.killWord,
                'kill-sentence':            self.killSentence,
                'kill-region':              self.killRegion,
                'yank':                     self.yank,
                'yank-pop':                 self.yankPop,
            }
        #@nonl
        #@-node:ekr.20050725121247:getPublicCommands
        #@+node:ekr.20050725120303:Entry points
        # backwardKillParagraph is in paragraph class.
        
        def backwardKillSentence (self,event):
            return self.keyboardQuit(event) and self._killSentence(event,back=True)
            
        def backwardKillWord (self,event):
            return self.deletelastWord(event) and self.keyboardQuit(event)
            
        def killLine (self,event):
            self.kill(event,frm='insert',to='insert lineend') and self.keyboardQuit(event)
            
        def killRegion (self,event):
            return self._killRegion(event,which='d') and self.keyboardQuit(event)
            
        # killParagraph is in paragraph class.
        
        def killSentence (self,event):
            return self.killsentence(event) and self.keyboardQuit(event)
            
        def killWord (self,event):
            return self.kill(event,frm='insert wordstart',to='insert wordend') and self.keyboardQuit(event)
            
        def yank (self,event):
            return self.walkKB(event,frm='insert',which='c') and self.keyboardQuit(event)
            
        def yankPop (self,event):
            return self.walkKB(event,frm="insert",which='a') and self.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050725120303:Entry points
        #@+node:ekr.20050724075352.162:kill
        def kill( self, event, frm, to  ):
        
            tbuffer = event.widget
            text = tbuffer.get( frm, to )
            self.addToKillBuffer( text )
            tbuffer.clipboard_clear()
            tbuffer.clipboard_append( text )   
         
            if frm == 'insert' and to =='insert lineend' and tbuffer.index( frm ) == tbuffer.index( to ):
                tbuffer.delete( 'insert', 'insert lineend +1c' )
                self.addToKillBuffer( '\n' )
            else:
                tbuffer.delete( frm, to )
        
            return self._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.162:kill
        #@+node:ekr.20050724075352.163:walkKB
        def walkKB( self, event, frm, which ):# kb = self.iterateKillBuffer() ):
                #if not kb1:
                #    kb1.append( self.iterateKillBuffer() )
                #kb = kb1[ 0 ]
                #global reset
            tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            t , t1 = i.split( '.' )
            clip_text = self.getClipboard( tbuffer )    
            if self.killbuffer or clip_text:
                if which == 'c':
                    self.reset = True
                    if clip_text:
                        txt = clip_text
                    else:
                        txt = self.kbiterator.next()
                    tbuffer.tag_delete( 'kb' )
                    tbuffer.insert( frm, txt, ('kb') )
                    tbuffer.mark_set( 'insert', i )
                else:
                    if clip_text:
                        txt = clip_text
                    else:
                        txt = self.kbiterator.next()
                    t1 = str( int( t1 ) + len( txt ) )
                    r = tbuffer.tag_ranges( 'kb' )
                    if r and r[ 0 ] == i:
                        tbuffer.delete( r[ 0 ], r[ -1 ] )
                    tbuffer.tag_delete( 'kb' )
                    tbuffer.insert( frm, txt, ('kb') )
                    tbuffer.mark_set( 'insert', i )
            return self._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.163:walkKB
        #@+node:ekr.20050724075352.164:deletelastWord
        def deletelastWord( self, event ):
            
            #tbuffer = event.widget
            #i = tbuffer.get( 'insert' )
            self.moveword( event, -1 )
            self.kill( event, 'insert', 'insert wordend')
            self.moveword( event ,1 )
            return 'break'
        #@-node:ekr.20050724075352.164:deletelastWord
        #@+node:ekr.20050724075352.165:_killSentence
        def killsentence( self, event, back = False ):
            tbuffer = event.widget
            i = tbuffer.search( '.' , 'insert', stopindex = 'end' )
            if back:
                i = tbuffer.search( '.' , 'insert', backwards = True, stopindex = '1.0' ) 
                if i == '':
                    return 'break'
                i2 = tbuffer.search( '.' , i, backwards = True , stopindex = '1.0' )
                if i2 == '':
                    i2 = '1.0'
                return self.kill( event, i2, '%s + 1c' % i )
                #return self.kill( event , '%s +1c' % i, 'insert' )
            else:
                i = tbuffer.search( '.' , 'insert', stopindex = 'end' )
                i2 = tbuffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
            if i2 == '':
               i2 = '1.0'
            else:
               i2 = i2 + ' + 1c '
            if i == '': return 'break'
            return self.kill( event, i2, '%s + 1c' % i )
        #@nonl
        #@-node:ekr.20050724075352.165:_killSentence
        #@+node:ekr.20050724075352.166:_killRegion
        def killRegion( self, event, which ):
            mrk = 'sel'
            tbuffer = event.widget
            trange = tbuffer.tag_ranges( mrk )
            if len( trange ) != 0:
                txt = tbuffer.get( trange[ 0 ] , trange[ -1 ] )
                if which == 'd':
                    tbuffer.delete( trange[ 0 ], trange[ -1 ] )   
                self.addToKillBuffer( txt )
                tbuffer.clipboard_clear()
                tbuffer.clipboard_append( txt )
            self.removeRKeys( tbuffer )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.166:_killRegion
        #@+node:ekr.20050724075352.167:addToKillBuffer
        #self.killbuffer = []
        def addToKillBuffer( self, text ):
            #global reset
            self.reset = True 
            if self.previousStroke in ( '<Control-k>', '<Control-w>' ,
             '<Alt-d>', '<Alt-Delete', '<Alt-z>', '<Delete>',
             '<Control-Alt-w>' ) and len( self.killbuffer):
                self.killbuffer[ 0 ] = self.killbuffer[ 0 ] + text
                return
            self.killbuffer.insert( 0, text )
        #@nonl
        #@-node:ekr.20050724075352.167:addToKillBuffer
        #@+node:ekr.20050724075352.168:iterateKillBuffer
        #self.reset = False
        
        def iterateKillBuffer( self ):
            #global reset
            while 1:
                if self.killbuffer:
                    self.last_clipboard = None
                    for z in self.killbuffer:
                        if self.reset:
                            self.reset = False
                            break        
                        yield z
        #@nonl
        #@-node:ekr.20050724075352.168:iterateKillBuffer
        #@+node:ekr.20050724075352.169:getClipboard
        def getClipboard (self,tbuffer):
            
            ctxt = None 
            
            try:
                ctxt = tbuffer.selection_get(selection='CLIPBOARD')
                if ctxt!=self.last_clipboard or not self.killbuffer:
                    self.last_clipboard = ctxt 
                    if self.killbuffer and self.killbuffer[0]==ctxt:
                        return None 
                    return ctxt 
                else:
                    return None 
                
            except:
                return None 
                
            return None 
        #@-node:ekr.20050724075352.169:getClipboard
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.161:class killBufferCommandsClass
    #@+node:ekr.20050724075352.221:class searchCommandsClass
    class searchCommandsClass (baseCommands):
        
        '''Implements many kinds of searches.'''
    
        #@    @+others
        #@+node:ekr.20050725091822.2: ctor
        def __init__ (self,emacs):
            
            self.emacs = emacs
            
            # Delegators...
            self.keyboardQuit = emacs.keyboardQuit
            self.mcStateManager = emacs.mcStateManager
            self.getSvarLabel = emacs.getSvarLabel
            self.setSvar = emacs.setSvar
            
            self.csr = { '<Control-s>': 'for', '<Control-r>':'bak' }
            self.pref = None
            
            self.qQ = None
            self.qR = None
            self.qgetQuery = False
            self.qgetReplace = False
            self.qrexecute = False
            self.querytype = 'normal'
        
            # For replace-string and replace-regex
            self._sString = ''
            self._rpString = ''
            self._useRegex = False
        #@nonl
        #@-node:ekr.20050725091822.2: ctor
        #@+node:ekr.20050725093156:getPublicCommands
        def getPublicCommands (self):
            
            return {
                'isearch-forward':          self.isearchForward,
                'isearch-backward':         self.isearchBackward,
                'isearch-forward-regexp':   self.isearchForwardRegexp,
                'isearch-backward-regexp':  self.isearchBackwardRegexp,
                
                'search-forward':           self.searchForward,
                'search-backward':          self.searchBackward,
                'word-search-forward':      self.wordSearchForward,
                'word-search-backward':     self.wordSearchBackward,
            }
        #@nonl
        #@-node:ekr.20050725093156:getPublicCommands
        #@+node:ekr.20050725093537:Entry points
        # Incremental...
        def isearchForward (self,event):
            return self.keyboardQuit(event) and self.startIncremental(event,'<Control-s>')
            
        def isearchBackward (self,event):
            return self.keyboardQuit(event) and self.startIncremental(event,'<Control-r>')
            
        def isearchForwardRegexp (self,event):
            return self.keyboardQuit(event) and self.startIncremental(event,'<Control-s>',which='regexp')
            
        def isearchBackwardRegexp (self,event):
            return self.keyboardQuit(event) and self.startIncremental(event,'<Control-r>',which='regexp')
        
        # Non-incremental...
        def searchForward (self,event):
            return self.startNonIncrSearch(event,'for')
            
        def searchBackward (self,event):
            return self.startNonIncrSearch(event,'bak')
            
        def wordSearchForward (self,event):
            return self.startWordSearch(event,'for')
            
        def wordSearchBackward (self,event):
            return self.startWordSearch(event,'bak')
        #@nonl
        #@-node:ekr.20050725093537:Entry points
        #@+node:ekr.20050724075352.222:incremental search methods
        #@+node:ekr.20050724075352.223:startIncremental
        def startIncremental( self, event, stroke, which='normal' ):
            
            isearch = self.mcStateManager.getState( 'isearch' )
        
            if isearch:
                self.search( event, way = self.csr[ stroke ], useregex = self.useRegex() )
                self.pref = self.csr[ stroke ]
                self.scolorizer( event )
                return 'break'
            else:
                svar, label = self.getSvarLabel( event )
                #self.isearch = True'
                self.mcStateManager.setState( 'isearch', which )
                self.pref = self.csr[ stroke ]
                label.configure( background = 'lightblue' )
                label.configure( textvariable = svar )
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.223:startIncremental
        #@+node:ekr.20050724075352.224:search
        def search( self, event, way , useregex=False):
            '''This method moves the insert spot to position that matches the pattern in the minibuffer'''
            tbuffer = event.widget
            svar, label = self.getSvarLabel( event )
            stext = svar.get()
            if stext == '': return 'break'
            try:
                if way == 'bak': #Means search backwards.
                    i = tbuffer.search( stext, 'insert', backwards = True,  stopindex = '1.0' , regexp = useregex )
                    if not i: #If we dont find one we start again at the bottom of the buffer. 
                        i = tbuffer.search( stext, 'end', backwards = True, stopindex = 'insert', regexp = useregex)
                else: #Since its not 'bak' it means search forwards.
                    i = tbuffer.search(  stext, "insert + 1c", stopindex = 'end', regexp = useregex ) 
                    if not i: #If we dont find one we start at the top of the buffer. 
                        i = tbuffer.search( stext, '1.0', stopindex = 'insert', regexp = useregex )
            except:
                return 'break'
            if not i or i.isspace(): return 'break'
            tbuffer.mark_set( 'insert', i )
            tbuffer.see( 'insert' )
        #@nonl
        #@-node:ekr.20050724075352.224:search
        #@+node:ekr.20050724075352.225:iSearch
        def iSearch( self, event, stroke ):
            if len( event.char ) == 0: return
            
            if stroke in self.csr: return self.startIncremental( event, stroke )
            svar, label = self.getSvarLabel( event )
            if event.keysym == 'Return':
                  if svar.get() == '':
                      return self.startNonIncrSearch( event, self.pref )
                  else:
                    return self.stopControlX( event )
                  #return self._tailEnd( event.widget )
            widget = event.widget
            label.configure( textvariable = svar )
            #if event.keysym == 'Return':
            #      return self.stopControlX( event )
            self.setSvar( event, svar )
            if event.char != '\b':
               stext = svar.get()
               z = widget.search( stext , 'insert' , stopindex = 'insert +%sc' % len( stext ) )
               if not z:
                   self.search( event, self.pref, useregex= self.useRegex() )
            self.scolorizer( event )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.225:iSearch
        #@+node:ekr.20050724075352.226:scolorizer
        def scolorizer( self, event ):
        
            tbuffer = event.widget
            svar, label = self.getSvarLabel( event )
            stext = svar.get()
            tbuffer.tag_delete( 'color' )
            tbuffer.tag_delete( 'color1' )
            if stext == '': return 'break'
            ind = '1.0'
            while ind:
                try:
                    ind = tbuffer.search( stext, ind, stopindex = 'end', regexp = self.useRegex() )
                except:
                    break
                if ind:
                    i, d = ind.split('.')
                    d = str(int( d ) + len( stext ))
                    index = tbuffer.index( 'insert' )
                    if ind == index:
                        tbuffer.tag_add( 'color1', ind, '%s.%s' % (i,d) )
                    tbuffer.tag_add( 'color', ind, '%s.%s' % (i, d) )
                    ind = i +'.'+d
            tbuffer.tag_config( 'color', foreground = 'red' ) 
            tbuffer.tag_config( 'color1', background = 'lightblue' )
        #@nonl
        #@-node:ekr.20050724075352.226:scolorizer
        #@+node:ekr.20050724075352.227:useRegex
        def useRegex( self ):
        
            isearch = self.mcStateManager.getState( 'isearch' )
            risearch = False
            if isearch != 'normal':
                risearch=True
            return risearch
        #@nonl
        #@-node:ekr.20050724075352.227:useRegex
        #@-node:ekr.20050724075352.222:incremental search methods
        #@+node:ekr.20050724075352.228:non-incremental search methods
        #@+at
        # Accessed by Control-s Enter or Control-r Enter.
        # Alt-x forward-search or backward-search, just looks for words...
        #@-at
        #@nonl
        #@+node:ekr.20050724075352.229:nonincrSearch
        def nonincrSearch( self, event, stroke ):
            
            if event.keysym in ('Control_L', 'Control_R' ): return
        
            state = self.mcStateManager.getState( 'nonincr-search' )
            svar, label = self.getSvarLabel( event )
            if state.startswith( 'start' ):
                state = state[ 5: ]
                self.mcStateManager.setState( 'nonincr-search', state )
                svar.set( '' )
                
            if svar.get() == '' and stroke=='<Control-w>':
                return self.startWordSearch( event, state )
            
            if event.keysym == 'Return':
                
                tbuffer = event.widget
                i = tbuffer.index( 'insert' )
                word = svar.get()
                if state == 'for':
                    s = tbuffer.search( word, i , stopindex = 'end' )
                    if s:
                        s = tbuffer.index( '%s +%sc' %( s, len( word ) ) )
                else:            
                    s = tbuffer.search( word,i, stopindex = '1.0', backwards = True )
                    
                if s:
                    tbuffer.mark_set( 'insert', s )    
                self.keyboardQuit( event )
                return self._tailEnd( tbuffer )        
                    
            else:
                self.setSvar( event, svar )
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.229:nonincrSearch
        #@+node:ekr.20050724075352.230:startNonIncrSearch
        def startNonIncrSearch( self, event, which ):
            
            self.keyboardQuit( event )
            tbuffer = event.widget
            self.mcStateManager.setState( 'nonincr-search', 'start%s' % which )
            svar, label = self.getSvarLabel( event )
            self.setLabelBlue( label )
            svar.set( 'Search:' )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.230:startNonIncrSearch
        #@-node:ekr.20050724075352.228:non-incremental search methods
        #@+node:ekr.20050724075352.231:word search methods
        #@+at
        # 
        # Control-s(r) Enter Control-w words Enter, pattern entered is treated 
        # as a regular expression.
        # 
        # for example in the buffer we see:
        #     cats......................dogs
        # 
        # if we are after this and we enter the backwards look, search for 
        # 'cats dogs' if will take us to the match.
        #@-at
        #@nonl
        #@+node:ekr.20050724075352.232:startWordSearch
        def startWordSearch( self, event, which ):
        
            self.keyboardQuit( event )
            tbuffer = event.widget
            self.mcStateManager.setState( 'word-search', 'start%s' % which )
            svar, label = self.getSvarLabel( event )
            self.setLabelBlue( label )
            if which == 'bak':
                txt = 'Backward'
            else:
                txt = 'Forward'
            svar.set( 'Word Search %s:' % txt ) 
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.232:startWordSearch
        #@+node:ekr.20050724075352.233:wordSearch
        def wordSearch( self, event ):
        
            state = self.mcStateManager.getState( 'word-search' )
            svar, label = self.getSvarLabel( event )
            if state.startswith( 'start' ):
                state = state[ 5: ]
                self.mcStateManager.setState( 'word-search', state )
                svar.set( '' )
                
            
            if event.keysym == 'Return':
                
                tbuffer = event.widget
                i = tbuffer.index( 'insert' )
                words = svar.get().split()
                sep = '[%s%s]+' %( string.punctuation, string.whitespace )
                pattern = sep.join( words )
                cpattern = re.compile( pattern )
                if state == 'for':
                    
                    txt = tbuffer.get( 'insert', 'end' )
                    match = cpattern.search( txt )
                    if not match: return self.keyboardQuit( event )
                    end = match.end()
                    
                else:            
                    txt = tbuffer.get( '1.0', 'insert' ) #initially the reverse words formula for Python Cookbook was going to be used.
                    a = re.split( pattern, txt )         #that didnt quite work right.  This one apparently does.   
                    if len( a ) > 1:
                        b = re.findall( pattern, txt )
                        end = len( a[ -1 ] ) + len( b[ -1 ] )
                    else:
                        return self.keyboardQuit( event )
                    
                wdict ={ 'for': 'insert +%sc', 'bak': 'insert -%sc' }
                
                tbuffer.mark_set( 'insert', wdict[ state ] % end )                                
                tbuffer.see( 'insert' )    
                self.keyboardQuit( event )
                return self._tailEnd( tbuffer )        
                    
            else:
                self.setSvar( event, svar )
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.233:wordSearch
        #@-node:ekr.20050724075352.231:word search methods
        #@+node:ekr.20050724075352.234:re-search methods
        # For the re-search-backward and re-search-forward Alt-x commands
        #@nonl
        #@+node:ekr.20050724075352.235:reStart
        def reStart( self, event, which='forward' ):
            self.keyboardQuit( event )
            tbuffer = event.widget
            self.mcStateManager.setState( 're_search', 'start%s' % which )
            svar, label = self.getSvarLabel( event )
            label.configure( background = 'lightblue' )
            svar.set( 'RE Search:' )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.235:reStart
        #@+node:ekr.20050724075352.236:re_search
        def re_search( self, event ):
            svar, label = self.getSvarLabel( event )
        
            state = self.mcStateManager.getState( 're_search' )
            if state.startswith( 'start' ):
                state = state[ 5: ]
                self.mcStateManager.setState( 're_search', state )
                svar.set( '' )
               
        
                
            if event.keysym == 'Return':
               
                tbuffer = event.widget
                pattern = svar.get()
                cpattern = re.compile( pattern )
                end = None
                if state == 'forward':
                    
                    txt = tbuffer.get( 'insert', 'end' )
                    match = cpattern.search( txt )
                    end = match.end()
                
                else:
        
                    txt = tbuffer.get( '1.0', 'insert' ) #initially the reverse words formula for Python Cookbook was going to be used.
                    a = re.split( pattern, txt )         #that didnt quite work right.  This one apparently does.   
                    if len( a ) > 1:
                        b = re.findall( pattern, txt )
                        end = len( a[ -1 ] ) + len( b[ -1 ] )
                
                if end:
                    
                    wdict ={ 'forward': 'insert +%sc', 'backward': 'insert -%sc' }
                        
                    tbuffer.mark_set( 'insert', wdict[ state ] % end )                                
                    self._tailEnd( tbuffer )
                    tbuffer.see( 'insert' )
                    
                return self.keyboardQuit( event )    
                
                
            else:
                self.setSvar( event, svar )
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.236:re_search
        #@-node:ekr.20050724075352.234:re-search methods
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.221:class searchCommandsClass
    #@+node:ekr.20050724075352.170:class registerCommandsClass FINISH
    class registerCommandsClass (baseCommands):
    
        '''A class to represent registers a-z and the corresponding Emacs commands.'''
    
        #@    @+others
        #@+node:ekr.20050725134243: ctor
        def __init__ (self,emacs):
            
            self.emacs = emacs
            
            # Delegators...
            self.keyboardQuit = emacs.keyboardQuit
            self.mcStateManager = emacs.mcStateManager
            self.getSvarLabel = emacs.getSvarLabel
            self.setSvar = emacs.setSvar
            
            #registers
            if emacs.useGlobalRegisters:
                self.registers = Emacs.global_registers 
            else:
                self.registers = {}
        
            self.regMeth = None 
            self.methodKeys, self.keyText = self.addRegisterItems()
        #@nonl
        #@-node:ekr.20050725134243: ctor
        #@+node:ekr.20050724075352.52:addRegisterItems
        def addRegisterItems( self ):
            
            methodKeys = {
                's' : self.copyToRegister,
                'i' : self.insertFromRegister,
                'n': self.numberToRegister,
                'plus': self.incrementRegister,
                'space': self.pointToRegister,
                'j': self.jumpToRegister,
                'a': lambda event , which = 'a': self._ToReg( event, which ),
                'p': lambda event , which = 'p': self._ToReg( event, which ),
                'r': self.copyRectangleToRegister,
                'view' : self.viewRegister,
            }    
            
            keyText = {
                's' : 'copy to register',
                'i' : 'insert from register',
                'plus': 'increment register',
                'n' : 'number to register',
                'p' : 'prepend to register',
                'a' : 'append to register',
                'space' : 'point to register',
                'j': 'jump to register',
                'r': 'rectangle to register',
                'view': 'view register',
            }
            
            return methodKeys, keyText
        #@nonl
        #@-node:ekr.20050724075352.52:addRegisterItems
        #@+node:ekr.20050725134243.1: getPublicCommands  FINISH
        def getPublicCommands (self):
            
            return {
                'append-to-register':   self.appendToRegister,
                'prepend-to-register':  self.prependToRegister,
                'copy-to-register': lambda event: self.setEvent( event, 's' ) and self.setNextRegister( event ),
                'insert-register': lambda event: self.setEvent( event, 'i' ) and self.setNextRegister( event ),
                'copy-rectangle-to-register': lambda event: self.setEvent( event, 'r' ) and self.setNextRegister( event ),
                'jump-to-register': lambda event: self.setEvent( event, 'j' ) and self.setNextRegister( event ),
                'point-to-register': lambda event: self.setEvent( event, 'space' ) and self.setNextRegister( event ),
                'number-to-register': lambda event: self.setEvent( event, 'n' ) and self.setNextRegister( event ),
                'increment-register': lambda event: self.setEvent( event, 'plus' ) and self.setNextRegister( event ),
                'view-register': lambda event: self.setEvent( event, 'view' ) and self.setNextRegister( event ),
            }
        #@nonl
        #@-node:ekr.20050725134243.1: getPublicCommands  FINISH
        #@+node:ekr.20050725135621.1: Entry points
        # 'copy-to-register': lambda event: self.setEvent( event, 's' ) and self.setNextRegister( event ),
        # 'insert-register': lambda event: self.setEvent( event, 'i' ) and self.setNextRegister( event ),
        # 'copy-rectangle-to-register': lambda event: self.setEvent( event, 'r' ) and self.setNextRegister( event ),
        # 'jump-to-register': lambda event: self.setEvent( event, 'j' ) and self.setNextRegister( event ),
        # 'point-to-register': lambda event: self.setEvent( event, 'space' ) and self.setNextRegister( event ),
        # 'number-to-register': lambda event: self.setEvent( event, 'n' ) and self.setNextRegister( event ),
        # 'increment-register': lambda event: self.setEvent( event, 'plus' ) and self.setNextRegister( event ),
        # 'view-register': lambda event: self.setEvent( event, 'view' ) and self.setNextRegister( event ),
        #@nonl
        #@-node:ekr.20050725135621.1: Entry points
        #@+node:ekr.20050724075352.176:_chckSel
        def _chckSel( self, event ):
             if not 'sel' in event.widget.tag_names():
                return False
             if not event.widget.tag_ranges( 'sel' ):
                return False  
             return True
        #@nonl
        #@-node:ekr.20050724075352.176:_chckSel
        #@+node:ekr.20050724075352.177:_checkIfRectangle
        def _checkIfRectangle( self, event ):
            if self.registers.has_key( event.keysym ):
                if isinstance( self.registers[ event.keysym ], list ):
                    svar, label = self.getSvarLabel( event )
                    self.stopControlX( event )
                    svar.set( "Register contains Rectangle, not text" )
                    return True
            return False
        #@nonl
        #@-node:ekr.20050724075352.177:_checkIfRectangle
        #@+node:ekr.20050724075352.175:_ToReg
        def _ToReg( self, event , which):
            if not self._chckSel( event ):
                return
            if self._checkIfRectangle( event ):
                return
            if event.keysym in string.letters:
                event.keysym = event.keysym.lower()
                tbuffer = event.widget
                if not self.registers.has_key( event.keysym ):
                    self.registers[ event.keysym ] = ''
                txt = tbuffer.get( 'sel.first', 'sel.last' )
                rtxt = self.registers[ event.keysym ]
                if self.which == 'p':
                    txt = txt + rtxt
                else:
                    txt = rtxt + txt
                self.registers[ event.keysym ] = txt
                return
        #@nonl
        #@-node:ekr.20050724075352.175:_ToReg
        #@+node:ekr.20050724075352.174:appendToRegister
        def appendToRegister( self, event ):
        
            event.keysym = 'a'
            self.setNextRegister( event )
            self.mcStateManager.setState( 'controlx', True )
        #@nonl
        #@-node:ekr.20050724075352.174:appendToRegister
        #@+node:ekr.20050724075352.172:copyRectangleToRegister
        def copyRectangleToRegister( self, event ):
            if not self._chckSel( event ):
                return
            if event.keysym in string.letters:
                event.keysym = event.keysym.lower()
                tbuffer = event.widget
                r1, r2, r3, r4 = self.getRectanglePoints( event )
                rect = []
                while r1 <= r3:
                    txt = tbuffer.get( '%s.%s' %( r1, r2 ), '%s.%s' %( r1, r4 ) )
                    rect.append( txt )
                    r1 = r1 +1
                self.registers[ event.keysym ] = rect
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.172:copyRectangleToRegister
        #@+node:ekr.20050724075352.171:copyToRegister
        def copyToRegister( self, event ):
        
            if not self._chckSel( event ):
                return
                
            if event.keysym in string.letters:
                event.keysym = event.keysym.lower()
                tbuffer = event.widget
                txt = tbuffer.get( 'sel.first', 'sel.last' )
                self.registers[ event.keysym ] = txt
                return
        
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.171:copyToRegister
        #@+node:ekr.20050724075352.186:deactivateRegister
        def deactivateRegister( self, event ):
            #global registermode, regMeth
            svar, label = self.getSvarLabel( event )
            svar.set( '' )
            self.setLabelGrey( label )
            self.registermode = False
            self.regMeth = None
        #@nonl
        #@-node:ekr.20050724075352.186:deactivateRegister
        #@+node:ekr.20050724075352.185:executeRegister
        def executeRegister( self, event ):
            self.regMeth( event )
            if self.registermode: 
                self.stopControlX( event )
            return
        #@nonl
        #@-node:ekr.20050724075352.185:executeRegister
        #@+node:ekr.20050724075352.179:incrementRegister
        def incrementRegister( self, event ):
            if self.registers.has_key( event.keysym ):
                if self._checkIfRectangle( event ):
                    return
                if self.registers[ event.keysym ] in string.digits:
                    i = self.registers[ event.keysym ]
                    i = str( int( i ) + 1 )
                    self.registers[ event.keysym ] = i
                else:
                    self.invalidRegister( event, 'number' )
                    return
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.179:incrementRegister
        #@+node:ekr.20050724075352.178:insertFromRegister
        def insertFromRegister( self, event ):
            tbuffer = event.widget
            if self.registers.has_key( event.keysym ):
                if isinstance( self.registers[ event.keysym ], list ):
                    self.yankRectangle( event, self.registers[ event.keysym ] )
                else:
                    tbuffer.insert( 'insert', self.registers[ event.keysym ] )
                    tbuffer.event_generate( '<Key>' )
                    tbuffer.update_idletasks()
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.178:insertFromRegister
        #@+node:ekr.20050724075352.183:invalidRegister
        def invalidRegister( self, event, what ):
            self.deactivateRegister( event )
            svar, label = self.getSvarLabel( event )
            svar.set( 'Register does not contain valid %s'  % what)
            return
        #@nonl
        #@-node:ekr.20050724075352.183:invalidRegister
        #@+node:ekr.20050724075352.182:jumpToRegister
        def jumpToRegister( self, event ):
            if event.keysym in string.letters:
                if self._checkIfRectangle( event ):
                    return
                tbuffer = event.widget
                i = self.registers[ event.keysym.lower() ]
                i2 = i.split( '.' )
                if len( i2 ) == 2:
                    if i2[ 0 ].isdigit() and i2[ 1 ].isdigit():
                        pass
                    else:
                        self.invalidRegister( event, 'index' )
                        return
                else:
                    self.invalidRegister( event, 'index' )
                    return
                tbuffer.mark_set( 'insert', i )
                tbuffer.event_generate( '<Key>' )
                tbuffer.update_idletasks() 
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.182:jumpToRegister
        #@+node:ekr.20050724075352.180:numberToRegister
        def numberToRegister( self, event ):
            if event.keysym in string.letters:
                self.registers[ event.keysym.lower() ] = str( 0 )
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.180:numberToRegister
        #@+node:ekr.20050724075352.181:pointToRegister
        def pointToRegister( self, event ):
            if event.keysym in string.letters:
                tbuffer = event.widget
                self.registers[ event.keysym.lower() ] = tbuffer.index( 'insert' )
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.181:pointToRegister
        #@+node:ekr.20050724075352.173:prependToRegister
        def prependToRegister( self, event ):
        
            event.keysym = 'p'
            self.setNextRegister( event )
            self.mcStateManager.setState( 'controlx', False )
        #@-node:ekr.20050724075352.173:prependToRegister
        #@+node:ekr.20050724075352.184:setNextRegister
        def setNextRegister( self, event ):
        
            if event.keysym == 'Shift':
                return
        
            if self.methodKeys.has_key( event.keysym ):
                self.mcStateManager.setState( 'controlx', True )
                self.regMeth = self.methodKeys[ event.keysym ]
                self.registermode = 2
                svar = self.svars[ event.widget ]
                svar.set( self.keyText[ event.keysym ] )
                return
        
            self.stopControlX( event )
        #@nonl
        #@-node:ekr.20050724075352.184:setNextRegister
        #@+node:ekr.20050724075352.187:viewRegister
        def viewRegister( self, event ):
            
            self.stopControlX( event )
            if event.keysym in string.letters:
                text = self.registers[ event.keysym.lower() ]
                svar, label = self.getSvarLabel( event )
                svar.set( text )
        #@nonl
        #@-node:ekr.20050724075352.187:viewRegister
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.170:class registerCommandsClass FINISH
    #@+node:ekr.20050724075352.137:macro methods DO NEXT
    #@+at
    # general macro methods.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.138:startKBDMacro
    #self.lastMacro = None
    #self.macs = []
    #self.macro = []
    #self.namedMacros = {}
    #self.macroing = False
    def startKBDMacro( self, event ):
    
        svar, label = self.getSvarLabel( event )
        svar.set( 'Recording Keyboard Macro' )
        label.configure( background = 'lightblue' )
        self.macroing = True
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.138:startKBDMacro
    #@+node:ekr.20050724075352.139:recordKBDMacro
    def recordKBDMacro( self, event, stroke ):
        if stroke != '<Key>':
            self.macro.append( (stroke, event.keycode, event.keysym, event.char) )
        elif stroke == '<Key>':
            if event.keysym != '??':
                self.macro.append( ( event.keycode, event.keysym ) )
        return
    #@nonl
    #@-node:ekr.20050724075352.139:recordKBDMacro
    #@+node:ekr.20050724075352.140:stopKBDMacro
    def stopKBDMacro( self, event ):
        #global macro, lastMacro, macroing
        if self.macro:
            self.macro = self.macro[ : -4 ]
            self.macs.insert( 0, self.macro )
            self.lastMacro = self.macro
            self.macro = []
    
        self.macroing = False
        svar, label = self.getSvarLabel( event )
        svar.set( 'Keyboard macro defined' )
        label.configure( background = 'lightgrey' )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.140:stopKBDMacro
    #@+node:ekr.20050724075352.141:_executeMacro
    def _executeMacro( self, macro, tbuffer ):
        
        for z in macro:
            if len( z ) == 2:
                tbuffer.event_generate( '<Key>', keycode = z[ 0 ], keysym = z[ 1 ] ) 
            else:
                meth = z[ 0 ].lstrip( '<' ).rstrip( '>' )
                method = self.cbDict[ meth ]
                ev = Tk.Event()
                ev.widget = tbuffer
                ev.keycode = z[ 1 ]
                ev.keysym = z[ 2 ]
                ev.char = z[ 3 ]
                self.masterCommand( ev , method, '<%s>' % meth )
        return self._tailEnd( tbuffer )
    #@nonl
    #@-node:ekr.20050724075352.141:_executeMacro
    #@+node:ekr.20050724075352.142:executeLastMacro
    def executeLastMacro( self, event ):
        tbuffer = event.widget
        if self.lastMacro:
            return self._executeMacro( self.lastMacro, tbuffer )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.142:executeLastMacro
    #@+node:ekr.20050724075352.143:nameLastMacro
    def nameLastMacro( self, event ):
        '''Names the last macro defined.'''
        #global macroing
        svar, label = self.getSvarLabel( event )    
        if not self.macroing :
            self.macroing = 2
            svar.set( '' )
            self.setLabelBlue( label )
            return 'break'
        if event.keysym == 'Return':
            name = svar.get()
            self._addToDoAltX( name, self.lastMacro )
            svar.set( '' )
            self.setLabelBlue( label )
            self.macroing = False
            self.stopControlX( event )
            return 'break'
        self.setSvar( event, svar )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.143:nameLastMacro
    #@+node:ekr.20050724075352.144:_addToDoAltX
    def _addToDoAltX( self, name, macro ):
        '''Adds macro to Alt-X commands.'''
        if not self.doAltX.has_key( name ):
            def exe( event, macro = macro ):
                self.stopControlX( event )
                return self._executeMacro( macro, event.widget )
            self.doAltX[ name ] = exe
            self.namedMacros[ name ] = macro
            return True
        else:
            return False
    #@nonl
    #@-node:ekr.20050724075352.144:_addToDoAltX
    #@+node:ekr.20050724075352.145:loadMacros
    def loadMacros( self,event ):
        '''Asks for a macro file name to load.'''
        import tkFileDialog
        f = tkFileDialog.askopenfile()
        if f == None: return 'break'
        else:
            return self._loadMacros( f )
    #@nonl
    #@-node:ekr.20050724075352.145:loadMacros
    #@+node:ekr.20050724075352.146:_loadMacros
    def _loadMacros( self, f ):
        '''Loads a macro file into the macros dictionary.'''
        import cPickle
        macros = cPickle.load( f )
        for z in macros:
            self._addToDoAltX( z, macros[ z ] )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.146:_loadMacros
    #@+node:ekr.20050724075352.147:getMacroName
    def getMacroName( self, event ):
        '''A method to save your macros to file.'''
        #global macroing
        svar, label = self.getSvarLabel( event )
        if not self.macroing:
            self.macroing = 3
            svar.set('')
            self.setLabelBlue( label )
            return 'break'
        if event.keysym == 'Return':
            self.macroing = False
            self.saveMacros( event, svar.get() )
            return 'break'
        if event.keysym == 'Tab':
            svar.set( self._findMatch( svar, self.namedMacros ) )
            return 'break'        
        self.setSvar( event, svar )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.147:getMacroName
    #@+node:ekr.20050724075352.148:saveMacros
    def saveMacros( self, event, macname ):
        '''Asks for a file name and saves it.'''
        import tkFileDialog
        name = tkFileDialog.asksaveasfilename()
        if name:
            f = file( name, 'a+' )
            f.seek( 0 )
            if f:
                self._saveMacros( f, macname ) 
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.148:saveMacros
    #@+node:ekr.20050724075352.149:_saveMacros
    def _saveMacros( self, f , name ):
        '''Saves the macros as a pickled dictionary'''
        import cPickle
        fname = f.name
        try:
            macs = cPickle.load( f )
        except:
            macs = {}
        f.close()
        if self.namedMacros.has_key( name ):
            macs[ name ] = self.namedMacros[ name ]
            f = file( fname, 'w' )
            cPickle.dump( macs, f )
            f.close()
    #@nonl
    #@-node:ekr.20050724075352.149:_saveMacros
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.137:macro methods DO NEXT
    #@+node:ekr.20050724075352.254:query replace methods DO NEXT
    #@+at
    # These methods handle the query-replace and query-replace-regex 
    # commands.  They need to be fully migrated
    # to the self.mcStateManager mechanism, which should simplify things 
    # greatly, or at least the amount of variables its required
    # so far.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.255:qreplace
    def qreplace( self, event ):
    
        if event.keysym == 'y':
            self._qreplace( event )
            return
        elif event.keysym in ( 'q', 'Return' ):
            self.quitQSearch( event )
        elif event.keysym == 'exclam':
            while self.qrexecute:
                self._qreplace( event )
        elif event.keysym in ( 'n', 'Delete'):
            #i = event.widget.index( 'insert' )
            event.widget.mark_set( 'insert', 'insert +%sc' % len( self.qQ ) )
            self.qsearch( event )
        event.widget.see( 'insert' )
    #@nonl
    #@-node:ekr.20050724075352.255:qreplace
    #@+node:ekr.20050724075352.256:_qreplace
    def _qreplace( self, event ):
        i = event.widget.tag_ranges( 'qR' )
        event.widget.delete( i[ 0 ], i[ 1 ] )
        event.widget.insert( 'insert', self.qR )
        self.qsearch( event )
    #@nonl
    #@-node:ekr.20050724075352.256:_qreplace
    #@+node:ekr.20050724075352.257:getQuery
    #self.qgetQuery = False
    #self.lqQ = Tk.StringVar()
    #self.lqQ.set( 'Replace with:' )    
      
    def getQuery( self, event ):
        #global qQ, qgetQuery, qgetReplace
        l = event.keysym
        svar, label = self.getSvarLabel( event )
        label.configure( textvariable = svar )
        if l == 'Return':
            self.qgetQuery = False
            self.qgetReplace = True
            self.qQ = svar.get()
            svar.set( "Replace with:" )
            self.mcStateManager.setState( 'qlisten', 'replace-caption' )
            #label.configure( textvariable = self.lqQ)
            return
        if self.mcStateManager.getState( 'qlisten' ) == 'replace-caption':
            svar.set( '' )
            self.mcStateManager.setState( 'qlisten', True )
        self.setSvar( event, svar )
    #@nonl
    #@-node:ekr.20050724075352.257:getQuery
    #@+node:ekr.20050724075352.258:getReplace
    #self.qgetReplace = False
    def getReplace( self, event ):
        #global qR, qgetReplace, qrexecute
        l = event.keysym
        svar, label = self.getSvarLabel( event )
        label.configure( textvariable = svar )
        if l == 'Return':
            self.qgetReplace = False
            self.qR = svar.get()
            self.qrexecute = True
            ok = self.qsearch( event )
            if self.querytype == 'regex' and ok:
                tbuffer = event.widget
                range = tbuffer.tag_ranges( 'qR' )
                txt = tbuffer.get( range[ 0 ], range[ 1 ] )
                svar.set( 'Replace %s with %s y/n(! for all )' %( txt, self.qR ) )
            elif ok:
                svar.set( 'Replace %s with %s y/n(! for all )' %( self.qQ, self.qR ) )
            #self.qrexecute = True
            #ok = self.qsearch( event )
            return
        if self.mcStateManager.getState( 'qlisten' ) == 'replace-caption':
            svar.set( '' )
            self.mcStateManager.setState( 'qlisten', True )
        self.setSvar( event, svar )
    #@nonl
    #@-node:ekr.20050724075352.258:getReplace
    #@+node:ekr.20050724075352.259:masterQR
    #self.qrexecute = False   
    def masterQR( self, event ):
    
        if self.qgetQuery:
            self.getQuery( event )
        elif self.qgetReplace:
            self.getReplace( event )
        elif self.qrexecute:
            self.qreplace( event )
        else:
            #svar, label = self.getSvarLabel( event )
            #svar.set( '' )
            self.listenQR( event )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.259:masterQR
    #@+node:ekr.20050724075352.260:startRegexReplace
    def startRegexReplace( self ):
        
        self.querytype = 'regex'
        return True
    #@nonl
    #@-node:ekr.20050724075352.260:startRegexReplace
    #@+node:ekr.20050724075352.261:query search methods
    #@+others
    #@+node:ekr.20050724075352.262:listenQR
    #self.qQ = None
    #self.qR = None
    #self.qlisten = False
    #self.lqR = Tk.StringVar()
    #self.lqR.set( 'Query with: ' )
    def listenQR( self, event ):
        #global qgetQuery, qlisten
        #self.qlisten = True
        self.mcStateManager.setState( 'qlisten', 'replace-caption' )
        #tbuffer = event.widget
        svar, label = self.getSvarLabel( event )
        self.setLabelBlue( label )
        if self.querytype == 'regex':
            svar.set( "Regex Query with:" )
        else:
            svar.set( "Query with:" )
        #label.configure( background = 'lightblue' , textvariable = self.lqR)
        self.qgetQuery = True
    #@nonl
    #@-node:ekr.20050724075352.262:listenQR
    #@+node:ekr.20050724075352.263:qsearch
    def qsearch( self, event ):
        if self.qQ:
            tbuffer = event.widget
            tbuffer.tag_delete( 'qR' )
            svar, label = self.getSvarLabel( event )
            if self.querytype == 'regex':
                try:
                    regex = re.compile( self.qQ )
                except:
                    self.keyboardQuit( event )
                    svar.set( "Illegal regular expression" )
                    
                txt = tbuffer.get( 'insert', 'end' )
                match = regex.search( txt )
                if match:
                    start = match.start()
                    end = match.end()
                    length = end - start
                    tbuffer.mark_set( 'insert', 'insert +%sc' % start )
                    tbuffer.update_idletasks()
                    tbuffer.tag_add( 'qR', 'insert', 'insert +%sc' % length )
                    tbuffer.tag_config( 'qR', background = 'lightblue' )
                    txt = tbuffer.get( 'insert', 'insert +%sc' % length )
                    svar.set( "Replace %s with %s? y/n(! for all )" % ( txt, self.qR ) )
                    return True
            else:
                i = tbuffer.search( self.qQ, 'insert', stopindex = 'end' )
                if i:
                    tbuffer.mark_set( 'insert', i )
                    tbuffer.update_idletasks()
                    tbuffer.tag_add( 'qR', 'insert', 'insert +%sc'% len( self.qQ ) )
                    tbuffer.tag_config( 'qR', background = 'lightblue' )
                    self._tailEnd( tbuffer )
                    return True
            self.quitQSearch( event )
            return False
    #@nonl
    #@-node:ekr.20050724075352.263:qsearch
    #@+node:ekr.20050724075352.264:quitQSearch
    def quitQSearch( self,event ):
        #global qQ, qR, qlisten, qrexecute
        event.widget.tag_delete( 'qR' )
        self.qQ = None
        self.qR = None
        #self.qlisten = False
        self.mcStateManager.setState( 'qlisten', False )
        self.qrexecute = False
        svar, label = self.getSvarLabel( event )
        svar.set( '' )
        label.configure( background = 'lightgrey' )
        #self.keyboardQuit( event )
        self.querytype = 'normal'
        self._tailEnd( event.widget )
        #event.widget.event_generate( '<Key>' )
        #event.widget.update_idletasks()
    #@nonl
    #@-node:ekr.20050724075352.264:quitQSearch
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.261:query search methods
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.254:query replace methods DO NEXT
    #@-others
    #@nonl
    #@-node:ekr.20050725091822:emacs commands classes
    #@-others
#@nonl
#@-node:ekr.20050724075352.40:class Emacs
#@-others
#@nonl
#@-node:ekr.20050723062822:@thin __core_emacs.py
#@-leo
