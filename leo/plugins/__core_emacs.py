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

USE_TEMACS = True

if USE_TEMACS:
    #@    << define usetemacs globals >>
    #@+node:ekr.20050724080034:<< define usetemacs globals >>
    labels = weakref.WeakKeyDictionary()
    editors = weakref.WeakKeyDictionary()
    haveseen = weakref.WeakKeyDictionary()
    extensions = []
    new_keystrokes = {}
    leocommandnames = None
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
#@+node:ekr.20050724074619:From Swingmacs  NOT USED YET
if 0:
    #@    @+others
    #@+node:ekr.20050723062822.11:lookForExtensions NOT READY YET
    def lookForExtensions():
        
        return [] ### Testing only.
       
        path,file = g.os_path_split(g.app.loadDir)
        try:
            if 1:  ## EKR
                pass ### Not ready yet.
            else: 
                tlevel = java.io.File( path )
                directories = tlevel.listFiles()
            exts = []
            for z in directories:
                if z.isDirectory() and z.getName() == 'swingmacs_exts':
                    sys.path.append( z.getAbsolutePath() )
                    files = z.listFiles()
                    for z1 in files:
                        if z1.isFile() and z1.getName().endswith( '.py' ):
                            exts.append( z1 ) 
                    break
        finally: pass
                
        mods = []
        for z in exts:
            try:
                name = z.getName()
                name = name[ : -3 ]
                mod = __import__( name )
                mods.append( mod )
            finally: pass
                
        return mods
    #@nonl
    #@-node:ekr.20050723062822.11:lookForExtensions NOT READY YET
    #@+node:ekr.20050723062822.4:addCommand
    def addCommand(  name, command ):
    
        global commandsFromPlugins
    
        commandsFromPlugins [ name ] = command
    #@nonl
    #@-node:ekr.20050723062822.4:addCommand
    #@+node:ekr.20050723062822.5:class emacsCommands  (from SwingMacs)
    class emacsCommands:
    
        '''A class that adds Emacs derived commands and keystrokes to Leo.'''
        
        #@    << how to write an extension for leoEmacs >>
        #@+node:ekr.20050723062822.6:<< how to write an extension for leoEmacs >>
        #@@nocolor
        #@+at
        # An extension is defined like so:
        # 1. a function called:
        #     getCommands()
        # returns a dictionary of command names and command classes, an 
        # example:
        #     return {  "j-library": JLibrary_Loc }
        # this in turn causes an instance of the command class to be 
        # instatiated.
        # Instantiation involves passing the emacs instance to the command via
        # the costructor
        # 
        #     returned_dict[ "akey" ]( self )   #self is the emacs instance
        # 
        # the instance is then asked for new commands via a call to its 
        # 'addToAltX' method,
        # which returns a list of commands:
        #     return [ 'zoom-to-home', 'release-window' ]
        # after this the command is queried to see if it has an 
        # 'addToKeyStrokes' method.  If so
        # it is called.  This is to return keystrokes that activate the 
        # command:
        #     return [ 'Ctrl W', ]
        # all commands and keystrokes that are bound to the command object 
        # result in a call to
        # its __call__ method which should be defined like so:
        #     def __call__( self, event, command ):
        #         ....code....
        #@-at
        #@nonl
        #@-node:ekr.20050723062822.6:<< how to write an extension for leoEmacs >>
        #@nl
    
        #@    @+others
        #@+node:ekr.20050723062822.7: ctor (emacsCommands)
        def __init__( self, c, minibuffer):
                ### editor=None, commandlabel=None, extracommands = None ):
            
            # global extensions
            # if extensions == None:
                # extensions = self.lookForExtensions()
                
            ## self.editor = editor
            ## self.commandlabel = commandlabel
            self.minibuffer = minibuffer
            self.c = c
            self.modeStrategies = []
            self.defineStrategyObjects()
            self.defineStrategiesForKeystrokes()
            
            self.kcb = self.KeyProcessor( self )
            ### self.editor.addKeyListener( self.kcb )
            #if g.app.config.getBool( c, "complete_tags" ):
            tm = self.TagMatcher( self )
            ### self.editor.addKeyListener( tm )
            
            self._stateManager = self.stateManager( self )
            self._stateManager2 = self.stateManager( self )
            self.command_help = []
            self.keystroke_help = []
            self.addCompleters()
        #@nonl
        #@-node:ekr.20050723062822.7: ctor (emacsCommands)
        #@+node:ekr.20050723062822.8:management listening
        #@+others
        #@+node:ekr.20050723062822.9:addCompleters
        def addCompleters( self ):
            
            return ###
            
            manager = g.app.config.manager
            manager.addNotificationDef( "complete-<", self.managementListener )
            manager.addNotificationDef( "complete-(", self.managementListener )
            manager.addNotificationDef( "complete-[", self.managementListener )
            manager.addNotificationDef( "complete-{", self.managementListener )
            manager.addNotificationDef( "complete-'", self.managementListener )
            manager.addNotificationDef( 'complete-"', self.managementListener )
        
        #@+at
        #     if config.getBool( self.c, "complete-<" ):
        #         self.swingmacs.addCompleter( "<", ">" )
        #     if config.getBool( self.c, "complete-(" ):
        #         self.swingmacs.addCompleter( "(", ")" )
        #     if config.getBool( self.c, "complete-[" ):
        #         self.swingmacs.addCompleter( "[", "]" )
        #     if config.getBool( self.c, "complete-{"):
        #         self.swingmacs.addCompleter( "{", "}" )
        #     if config.getBool( self.c, "complete-'" ):
        #         self.swingmacs.addCompleter( "'", "'" )
        #     if config.getBool( self.c, 'complete-"' ):
        #         self.swingmacs.addCompleter( '"', '"' )
        #     if config.getBool( self.c, "add_tab_for-:" ):
        #         self.swingmacs.addTabForColon( True )
        #@-at
        #@nonl
        #@-node:ekr.20050723062822.9:addCompleters
        #@+node:ekr.20050723062822.10:managementListener
        def managementListener( self, notification= None, handback = None ):
            
            source = notification.getSource().toString()
            source = source.lstrip( "MBean:name=" )
            use = g.app.config.getBool( self.c, source )
            completer = source[ -1 ]
            if use:
                completions = {
                    '(': ')',
                    '{': '}',
                    '<': '>',
                    '[':']',
                    '"': '"',
                    "'" : "'",        
                }
                self.kcb.addCompleter( completer, completions[ completer ] )
            else:
                self.kcb.removeCompleter( completer )
        #@nonl
        #@-node:ekr.20050723062822.10:managementListener
        #@-others
        #@nonl
        #@-node:ekr.20050723062822.8:management listening
        #@+node:ekr.20050723062822.12:addCompleter
        def addCompleter( self, ch, ch2 ):
            self.kcb.addCompleter( ch, ch2 )
            
        def addTabForColon( self, torf ):
            self.kcb.addTabForColon( torf )
        #@nonl
        #@-node:ekr.20050723062822.12:addCompleter
        #@+node:ekr.20050723062822.13:helper classes
        #@+others
        #@+node:ekr.20050723062822.14:stateManager
        class stateManager:
            
            def __init__( self, emacs):
                self.state = None
                self.emacs = emacs
                
                
            def hasState( self ):
                return self.state
                
            def setState( self, state ):
                self.state = state
                
            def filterTo( self, event, command ):
                return self.emacs.strategyObjects[ self.state ]( event, command )
                
            def clear( self ):
                self.state = None
        #@nonl
        #@-node:ekr.20050723062822.14:stateManager
        #@+node:ekr.20050723062822.15:KeyProcessor ( aevent.KeyListener )
        class KeyProcessor:  ## ( aevent.KeyListener ):
            
            '''KeyListener calls and newline analyzer.'''
        
            #@    @+others
            #@+node:ekr.20050723062822.16:__init__
            def __init__( self, emacs ):
            
                self.emacs = emacs
                self.kRconsume = False
                self.kTconsume = False
                self.completers = {}
                self.tab_for_colon = False  
                self.tab_width = g.app.config.getInt( emacs.c, "tab_width" )
            #@nonl
            #@-node:ekr.20050723062822.16:__init__
            #@+node:ekr.20050723062822.17:addCompleter
            def addCompleter( self, ch, ch2 ):
                self.completers[ ch ] = ch2
            
            def addTabForColon( self, torf ):
                self.tab_for_colon = torf
            #@nonl
            #@-node:ekr.20050723062822.17:addCompleter
            #@+node:ekr.20050723062822.18:removeCompleter
            def removeCompleter( self, ch ):
                del self.completers[ ch ]
            #@nonl
            #@-node:ekr.20050723062822.18:removeCompleter
            #@+node:ekr.20050723062822.19:keyReleased
            def keyReleased( self,event ):
                if self.kRconsume:
                    self.kRconsume = False
                    event.consume()
            #@nonl
            #@-node:ekr.20050723062822.19:keyReleased
            #@+node:ekr.20050723062822.20:keyTyped
            def keyTyped( self, event ):
                if self.kTconsume:
                    self.kTconsume = False
                    event.consume()
            #@nonl
            #@-node:ekr.20050723062822.20:keyTyped
            #@+node:ekr.20050723062822.21:keyPressed
            def keyPressed( self, event ):
                        
                modifiers = event.getModifiers()
                mtxt = event.getKeyModifiersText( modifiers )
                ktxt = event.getKeyText( event.getKeyCode() )
                if mtxt == ktxt:
                    command = mtxt
                else:
                    command = '%s %s' % ( mtxt, ktxt )
                    command = command.strip()
                    #print command
                #print command
                consume = self.emacs.masterCommand( event, command )
                #print "Consume %s %s" %( command, consume )
                if consume: #this blocks the event from going elsewhere, like the DocumentModel
                    self.kTconsume = True
                    self.kRconsume = True
                    event.consume()
                    return
                else:
                    self.kTconsume = self.kRconsume = False
                
                kc = event.getKeyChar()  
                if self.tab_for_colon and kc == '\n':
                    event.consume()
                    self.insertPreviousLeadAndNewline()
                    
                if self.completers.has_key( kc ):
                    editor = self.emacs.editor
                    doc = editor.getDocument()
                    pos = editor.getCaretPosition()
                    try:
                    
                        pc = doc.getText( pos -1, 1 )
                        if pc in ( '"', "'" ): return
                    
                    except:
                        pass
                    event.consume()
                    self.kTconsume = True
                    self.kRconsume = True
                    ac = self.completers[ kc ]
                    #editor = self.emacs.editor
                    doc.insertString( pos, '%s%s' %( kc, ac ), None )
                    editor.setCaretPosition( pos + 1 )
                    if hasattr( self.emacs.c.frame.body.editor, "autocompleter"):
                        self.emacs.c.frame.body.editor.autocompleter.hideAutoBox() 
                    return
                    
                if kc == '\t' and self.tab_width == -4:
                    self.kTconsume = True
                    self.kRconsume = True
                    event.consume()
                    editor = self.emacs.editor
                    doc = editor.getDocument()
                    pos = editor.getCaretPosition()
                    try:
                    
                        doc.insertString( pos, " " * 4, None )
                        return
                    
                    except:
                        pass
            #@nonl
            #@-node:ekr.20050723062822.21:keyPressed
            #@+node:ekr.20050723062822.22:insertPreviousLeadAndNewline -- for autoindentation on newline
            def insertPreviousLeadAndNewline( self ):
                #@    << why is this code here? >>
                #@+node:ekr.20050723062822.23:<< why is this code here? >>
                '''
                Originally this was in the leoSwingBody class.  This seemed right, it is core functionaliy.  But
                In light of SwingMacs I reconsidered where it should go.  Temacs was a plugin, SwingMacs is core.
                SwingMacs is responsible for processing key presses and such, consuming them if they are not to get
                to the DocumentModel.  By placing this method in leoSwingBody, the Key processing responsibilities get
                spread out.  Hence it makes more sense to move this method here, the responsibilites stay clearer.
                '''
                #@nonl
                #@-node:ekr.20050723062822.23:<< why is this code here? >>
                #@nl
                
                editor = self.emacs.editor
                doc = editor.getDocument()
                pos = editor.getCaretPosition()
                start_text = doc.getText( 0, pos )
                ind = start_text.rfind( '\n' )
            
                if ind > 0:
                    line = start_text[ ind: ].strip( '\n' )
                else:
                    line = start_text.strip( '\n' )
                
                i = len( line.lstrip() )
                
                if i == 0:
                        instring = line
                else:
                    instring = line[ : -i ]
            
                #instring = '\n%s' % instring
                #spaces = self.calculateExtraSpaces( line.lstrip() )
                #instring = "\n%s%s" %( spaces, instring )
                instring = '\n%s' % instring
                #printspaces
                #instring = "%s%s" %( spaces, instring )
                if line.strip().endswith( ":" ):
                    if self.tab_width == -4:
                        instring += " " * 4
                    else:
                        instring += "\t"
                doc.insertString( pos, instring, None )
            #@nonl
            #@-node:ekr.20050723062822.22:insertPreviousLeadAndNewline -- for autoindentation on newline
            #@+node:ekr.20050723062822.24:calculateExtraSpaces
            def calculateExtraSpaces( self, line ):
                
                
                endsWithColon = False
                hasUncompleteBracket = False
                
                count1 = 0
                for z in line:
                    if z == '[':
                        count += 1
                    elif z == ']':
                        count -= 1
                        
                
                count2 = 0
                last2 = None
                ll = len( line ) -1
                while ll >= 0:
                    char = line[ ll ]
                    if char == '(':
                        count2 += 1
                        last2 = ll
                    elif char == ')':
                        count2 -= 1
                        
                    ll -= 1
                        
                        
                if count2 > 0:
                    nwline = line[ : last2 ]
                    ws = []
                    for z in nwline:
                        if z.isspace():
                            ws.append( z )
                        else:
                            ws.append( ' ' )
                    
                    print "WS len is %s" % len( ws )
                    return ''.join( ws )
                    
                
                return ''    
                    
                #if count2 != 0:
                #    pass
            #@nonl
            #@-node:ekr.20050723062822.24:calculateExtraSpaces
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.15:KeyProcessor ( aevent.KeyListener )
        #@+node:ekr.20050723062822.25:TagMatcher ( aevent.KeyAdapter )
        class TagMatcher: ## ( aevent.KeyAdapter ):
            
            '''matches html/xml style tags.'''
            
            #@    @+others
            #@+node:ekr.20050723062822.26:ctor
            def __init__( self, emacs ):
            
                ### aevent.KeyAdapter.__init__( self )
                self.emacs = emacs 
                self.configureMatching()
                ### g.app.config.manager.addNotificationDef( "complete_tags", self.configureMatching )
            #@-node:ekr.20050723062822.26:ctor
            #@+node:ekr.20050723062822.27:configureMatching
            def configureMatching( self, notification = None, handback = None ):
                
                on = g.app.config.getBool( self.emacs.c, "complete_tags" )
                self.on = on
            #@nonl
            #@-node:ekr.20050723062822.27:configureMatching
            #@+node:ekr.20050723062822.28:keyPressed
            def keyPressed( self, event ):
            
                if not (self.on and event.getKeyChar() == ">"):
                    return
                    
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                start = stext.Utilities.getRowStart( editor, pos )
                doc = editor.getDocument()
                txt = doc.getText( start, pos - start )
            
                txt = list( txt )
                txt.reverse()
                matchone = 0
                matchtwo = 0
                data = []
                if txt:
                    if txt[ 0 ] == "/": return
                else:
                    return
                    
                for z in txt:    
                    if z == "<" and not matchone:
                        matchone = 1
                        data.append( z )
                        continue
                    elif z == "<" and matchone:
                        matchtwo = 1
                        break
                    elif matchone:
                        break
                    if not matchone:
                        data.append( z )
                
                if not data: return
                elif len( data ) == 1 and data[ 0 ] == "<": return
                elif len( data ) > 1 and not data[ -2 ].isalpha(): return
                
                if matchone and not matchtwo:
                    data.reverse()
                    data.insert( 1, "/" )
                    element = ''.join( data )
                    pieces = element.split()
                    endelement = "%s%s" % (  pieces[ 0 ], ">" )
                    doc.insertString( pos, endelement , None )
                    editor.setCaretPosition( pos )
            #@nonl
            #@-node:ekr.20050723062822.28:keyPressed
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.25:TagMatcher ( aevent.KeyAdapter )
        #@+node:ekr.20050723062822.29:TabCompleter
        class TabCompleter:
        
            def __init__( self, data ):
                self.data = data
                self.current = None
                self.current_iter = None
            
            def reset( self ):
                self.current = None
                
            def extend( self, data ):
                for z in data:
                    if z in self.data: continue
                    self.data.append( z )
                
            def lookFor( self, txt ):
                
                nwdata = []
                for z in self.data:
                    if z.startswith( txt ):
                        nwdata.append( z )
                        
                if len( nwdata ) > 0:
                    nwdata.sort()
                    self.current = nwdata 
                    self.current_iter = iter( nwdata )
                    return True
                else:
                    return False
        
            def getNext( self ):
                
                try:
                    return self.current_iter.next()        
                except:
                    
                    self.current_iter = iter( self.current )
                    return self.getNext()
        #@nonl
        #@-node:ekr.20050723062822.29:TabCompleter
        #@-others
        #@nonl
        #@-node:ekr.20050723062822.13:helper classes
        #@+node:ekr.20050723062822.30:Strategy stuff...
        #@+node:ekr.20050723062822.31:defineStrategyObjects
        def defineStrategyObjects( self ):
                
            self.strategyObjects = {
                'incremental': self.incremental( self ),
                'dynamic-abbrev' : self.dynamicabbrevs( self ),
                'formatter' : self.formatter( self ),
                'killbuffer': self.killbuffer( self ),
                'deleter': self.deleter( self ),
                 #'xcommand': self.alt_x_handler( self ),
                'rectangles': self.rectangles( self ),
                'zap': self.zap( self ),
                'comment': self.comment( self ),
                'movement': self.movement( self ),
                'transpose': self.transpose( self ),
                'capitalization': self.capitalization( self ),
                'replacement': self.replacement( self ),
                'sorters': self.sorters( self ),
                'lines': self.lines( self ),
                'tabs': self.tabs( self ),
                'registers': self.registers( self ),
                'selection': self.selection( self ),
                'completion': self.symbolcompletion( self ),
                'sexps': self.balanced_parentheses( self ),
                'tags': self.tags( self ),
            }
            
            self.strategyObjects[ 'xcommand' ] = self.alt_x_handler( self )
            self.strategyObjects[ 'ctrlx' ] = self.ctrl_x_handler( self )
            self.strategyObjects[ 'ctrlu' ] = self.ctrl_u_handler( self )
            
            for z in extensions:
                try:
                    add = z.getCommands()
                    for z in add.keys():
                        try:
                            sO = add[ z ]( self )
                            self.strategyObjects[ z ] = sO
                            ncommands = sO.addToAltX()
                            for z in ncommands:
                                self.strategyObjects[ 'xcommand' ].commands[ z ] = sO
                        finally: pass
                finally: pass    
        
            self.strategyObjects[ 'xcommand' ].createTabCompleter()
        #@nonl
        #@-node:ekr.20050723062822.31:defineStrategyObjects
        #@+node:ekr.20050723062822.32:defineStrategiesForKeystrokes
        def defineStrategiesForKeystrokes( self ):
            
            cmds = self.strategyObjects
            callbacks = {
                
                'Ctrl S': cmds[ 'incremental' ],
                'Ctrl R': cmds[ 'incremental' ],
                'Alt Slash': cmds[ 'dynamic-abbrev' ],
                'Ctrl+Alt Slash': cmds[ 'dynamic-abbrev' ],
                'Ctrl+Alt Back Slash': cmds[ 'formatter' ],
                'Alt Back Slash': cmds[ 'formatter' ],
                'Alt+Shift 6': cmds[ 'formatter' ],
                'Ctrl K': cmds[ 'killbuffer' ],
                'Alt Y': cmds[ 'killbuffer' ],
                'Ctrl Y': cmds[ 'killbuffer' ],
                'Ctrl W': cmds[ 'killbuffer' ],
                'Alt W': cmds[ 'killbuffer' ],
                'Delete': cmds[ 'deleter' ],
                'Ctrl D': cmds[ 'deleter' ],
                'Alt X': cmds[ 'xcommand' ],
                'Alt+Shift Period': cmds[ 'movement' ],
                'Alt+Shift Comma': cmds[ 'movement' ],
                'Ctrl Left': cmds[ 'movement'],
                'Ctrl Right': cmds[ 'movement'],
                'Alt M': cmds[ 'movement' ],
                'Ctrl A': cmds[ 'movement' ],
                'Ctrl E': cmds[ 'movement' ],
                'Alt Z': cmds[ 'zap' ],
                'Ctrl Space': cmds[ 'selection' ],
                'Ctrl X': cmds[ 'ctrlx' ],
                'Alt T': cmds[ 'transpose' ],
                'Ctrl+Alt I': cmds[ 'completion' ],
                'Ctrl+Alt F': cmds[ 'sexps' ],
                'Ctrl+Alt B': cmds[ 'sexps' ],
                'Ctrl+Alt K': cmds[ 'sexps' ],
                'Ctrl+Alt Delete': cmds[ 'sexps' ],
                'Alt Period': cmds[ 'tags' ],
                'Alt+Shift 8': cmds[ 'tags' ],
                'Ctrl U': cmds[ 'ctrlu' ],
                
                }
                
            for z in cmds.keys():
                sO = cmds[ z ]
                if hasattr( sO, 'addToKeyStrokes' ):
                    nstrokes = sO.addToKeyStrokes()
                    if nstrokes:
                        for z in nstrokes.keys():
                            callbacks[ z ] = nstrokes[ z ]
                
            self.callbacks = callbacks
        #@nonl
        #@-node:ekr.20050723062822.32:defineStrategiesForKeystrokes
        #@+node:ekr.20050723062822.33:addCommands
        def addCommands( self, command, commands ):
            
            xcommand = self.strategyObjects[ 'xcommand' ]
        
            for z in commands:
                xcommand.commands[ z ] = command
                xcommand.keys.append( z )
        
            self.strategyObjects[ command.getName() ] = command
        #@nonl
        #@-node:ekr.20050723062822.33:addCommands
        #@-node:ekr.20050723062822.30:Strategy stuff...
        #@+node:ekr.20050723062822.34:masterCommand -- all processing goes through here
        def masterCommand( self, event, command ):
            '''All processing goes through here.  'consume' is a flag to the
               KeyProcessor instance indicating if it should stop the event from
               propagating by consuming the event'''
        
            consume = False
        
            if command == 'Ctrl G':
                return self.keyboardQuit( event )
              
            if self._stateManager.hasState():
                return self._stateManager.filterTo( event, command )
                
            if self.callbacks.has_key( command ):
                consume = self.callbacks[ command ]( event, command )
                
            if self._stateManager2.hasState():
                self._stateManager2.filterTo( event, command )
            
            return consume
        #@nonl
        #@-node:ekr.20050723062822.34:masterCommand -- all processing goes through here
        #@+node:ekr.20050723062822.35:setCommandText
        def setCommandText( self, txt ):
            
            self.commandlabel.setText( txt )
        #@nonl
        #@-node:ekr.20050723062822.35:setCommandText
        #@+node:ekr.20050723062822.36:help
        def getHelp( self ):
            
            helptext ='''
            
            keystrokes:
            
            keyboard quit:
                Ctrl-g: quits any current command. 
            
            selecting:
                Ctrl-Spacebar : starts selecting.  To stop Ctrl-g.
            
            kill and yanking:
                Ctrl-k : kills to end of line and inserts data into killbuffer
                Ctrl-w: kills region and inserts data into killbuffer
                Alt-w: copys region and inserts data into killbuffer   
                Ctrl-y: inserts first item in the killbuffer
                Alt-y: inserts next item in the killbuffer; allows the user to cycle 
                   through the killbuffer, selecting the desired 'killed' text.
                   
                   
            deleting:    
                Ctrl-d: deletes next character.
                Delete: deletes previous character.
            
            
            dynamic abbreviations:
                Alt-/ : cycles through all words that match the starting word, which is used as a prefix.
                Ctrl-Alt-/ : takes current word, using it as a prefix and finds the common 
                            prefix among the matching prefix words. 'ea' with the words ( eat,
                            eats, eater ) will become 'eat' upon execution of this command.
                            
            symbol completion:
                Alt Ctrl I : takes the start of the current word and completes it if it matches a keyword
                             of the current language in effect.  The user can cycle through the matches if there
                             are multiple matches.  For example:
                                 d( Alt Ctrl I )
                                 del
                                 del( Alt Ctrl I )
                                 def
                         
                         
            incremental search:
                Ctrl-s : starts incremental search forward
                Ctrl-r : starts incremental search backward
            
            
            formating:
                Ctrl-Alt-\ : takes the current selection and formats each line so that it has the same indentation
                         as the first line in the selection.
                Alt-\: deletes the surrounding whitespace
                Alt-^: joins line to previous line. 
                
            transposing:
                Alt-t: marks a word for moving.  2nd execution on word, trades positions of 1rst word with 2nd word. 
                         
            movement:
                Alt-< (less then sign ): move to the beginning of buffer
                Alt-> (greater then sign ): move to the end of the buffer
                Ctrl a: move to the beginning of line
                Ctrl e: move to end of the line
                Alt m: move to the end of the indentation on the current line.
                
            balanced parentheses or sexps:
                Ctrl Alt f: moves forward to matching parentheses.
                Ctrl Alt b: moves backwards to matching parentheses 
                Ctrl Alt k: kills the sexp forward. Can subsequently be yanked
                Ctrl Alt Delete: kills the sexp backward. Can subsequently be yanked
            
            
            zapping:
                Alt-z: zaps to the character specified by the user.
            
            Ctrl x: This keystroke prepares SwingMacs for another keystroke.  These are:
                Ctrl o: This deletes blanklines surrounding the current line. 
                
            tags:
                tags are definitions of language constructs.  Language specific tags:
                    Python: def and class
                    Java: class and methods
                    
                keystrokes:
                    Alt-. : queries the user for the tag they wish to goto.  If Enter is typed
                            the current word is used for the tag
                    Ctrl-U Alt-. : goes to the next definition of a tag.  Useful if there are multiple
                                   definitions for a tag.
                    Alt-* : pops the buffer/node back to the last place Alt-. and friends were executed.
                            This can be executed multiple times, if Alt-. was executed multiple times,
                            taking the user back to where he started jumping.
            
            
            '''
            
            addstring = "\n".join( self.keystroke_help )
            
            helptext += addstring
            
            return helptext
        #@nonl
        #@-node:ekr.20050723062822.36:help
        #@+node:ekr.20050723062822.37:add*Help
        def addCommandHelp( self, chelp ):
        
            self.command_help.append( chelp )
            
        def addKeyStrokeHelp( self, kshelp ):
            
            self.keystroke_help.append( kshelp )
        #@nonl
        #@-node:ekr.20050723062822.37:add*Help
        #@+node:ekr.20050723062822.38:keyboardQuit
        def keyboardQuit( self, event=None ):
            
            self._stateManager.clear()
            self._stateManager2.clear()
            self.minibuffer.setText( '' )
            self.clearHighlights()
            sa = stext.SimpleAttributeSet()
            sa.addAttribute( 'dy-ab', 'dy-ab' )
            sa.addAttribute( 'kb', 'kb' )
            self.clearAttributes( sa )
            self.setCommandText( "" )
            for z in self.modeStrategies:
                z.mode = None
            
            cp = self.editor.getCaretPosition()
            self.editor.setCaretPosition( cp )
            return True
        #@nonl
        #@-node:ekr.20050723062822.38:keyboardQuit
        #@+node:ekr.20050723062822.39:beep
        def beep( self ):
            
            tk = awt.Toolkit.getDefaultToolkit()
            tk.beep()
        #@nonl
        #@-node:ekr.20050723062822.39:beep
        #@+node:ekr.20050723062822.40:determineLanguage
        def determineLanguage( self ):
            
            pos = self.c.currentPosition()
            language = g.scanForAtLanguage( self.c, pos )
            return language
        #@nonl
        #@-node:ekr.20050723062822.40:determineLanguage
        #@+node:ekr.20050723062822.41:getTabWidth
        def getTabWidth( self ):
            
            return abs( self.c.tab_width )
        #@nonl
        #@-node:ekr.20050723062822.41:getTabWidth
        #@+node:ekr.20050723062822.42:eventToMinibuffer
        def eventToMinibuffer( self, event ):
            
            code = event.getKeyCode()
            code = event.getKeyText( code )
            txt = self.minibuffer.getText()
            if code == 'Backspace':
                txt = txt[ : -1 ]
            else:
                char = event.getKeyChar()
                #if java.lang.Character.isLetterOrDigit( char ) or java.lang.Character.isWhitespace( char ):
                if java.lang.Character.isDefined( char ):
                    txt = '%s%s' %( txt, char )
            self.minibuffer.setText( txt )
            return txt
        #@nonl
        #@-node:ekr.20050723062822.42:eventToMinibuffer
        #@+node:ekr.20050723062822.43:text operations
        def getText( self ):
            
            doc = self.editor.getDocument()
            txt = doc.getText( 0, doc.getLength() )
            return txt
            
        def getTextSlice( self, frm, to ):
            
            txt = self.getText()
            return txt[ frm: to ]
            
        def replaceText( self, frm, to, txt ):
            
            doc = self.editor.getStyledDocument()
            doc.replace( frm, to - frm, txt, None )
        #@nonl
        #@-node:ekr.20050723062822.43:text operations
        #@+node:ekr.20050723062822.44:word operations
        def getWordStart( self ):
            
            pos = self.editor.getCaretPosition()
            #start = stext.Utilities.getWordStart( self.editor, pos ) --this method acts screwy
            doc = self.editor.getStyledDocument()
            txt = doc.getText( 0, pos )
            txtlines = txt.splitlines()
            try:
                line = txtlines[ -1 ]
                chunks = line.split()
                c2 = []
                for z in chunks[ : ]:
                    [ c2.append( x ) for x in z.split( '.' ) ]
                chunks = c2
                word = chunks[ -1 ]
                for z in xrange( len( word ) ):
                    w = word[ z ]
                    if w.isalnum() or w=='_': break
                
                word = word[ z: ]
            except:
                return None
            return word
            
        def getWordStartIndex( self, i = None ):
            
            pos = self.editor.getCaretPosition()
            doc = self.editor.getStyledDocument()
            txt = doc.getText( 0, pos )
            tlist = list( txt )
            tlist.reverse()
            for z in xrange( len( tlist ) ):
                if tlist[ z ] not in ( '_', '-' ) and ( tlist[ z ].isspace() or not tlist[ z ].isalnum() ):
                    break
            return pos - z
            #start = stext.Utilities.getWordStart( self.editor, pos ) ---this method acts screwy, thats why Im not using it.
            
            
        def getWordEndIndex( self, i = None ):
            pos = self.editor.getCaretPosition()
            doc = self.editor.getStyledDocument()
            txt = doc.getText( 0, doc.getLength())
            txt = txt[ pos: ]
            tlist = list( txt )
            z = 0
            for z in xrange( len( tlist ) ):
                if tlist[ z ] != '_' and ( tlist[ z ].isspace() or not tlist[ z ].isalnum() ):
                    break
            
            if z == 0:
                z = 1
            return pos + z
        #@nonl
        #@-node:ekr.20050723062822.44:word operations
        #@+node:ekr.20050723062822.45:findPre
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
        #@-node:ekr.20050723062822.45:findPre
        #@+node:ekr.20050723062822.46:attribute and highlight operations
        def getAttributeRanges( self, name ):
            
            dsd = self.editor.getStyledDocument()
            alen = dsd.getLength()
            range = []
            for z in xrange( alen ):
                element = dsd.getCharacterElement( z )
                as = element.getAttributes()
                if as.containsAttribute( name, name ):
                    range.append( z )
                    
            return range
            
        def addAttributeToRange( self, name, value, offset, length, color = None ):
        
            dsd = self.editor.getStyledDocument()
            sa = stext.SimpleAttributeSet()
            sa.addAttribute( name, value )
            dsd.setCharacterAttributes( offset, length, sa, True )
            if color != None:
                self.addHighlight( offset, length+offset, color )
        
        def clearAttributes( self, attrset ):
            dsd = self.editor.getStyledDocument()
            alen = dsd.getLength()
            for z in xrange( alen ):
                element = dsd.getCharacterElement( z )
                as = element.getAttributes()
                if as.containsAttributes( attrset ):
                    mas = stext.SimpleAttributeSet() #We have to make a clean one and copy the data into it!  The one returned is immutable
                    mas.addAttributes( as )
                    mas.removeAttributes( attrset ) #we remove the tag from here.
                    amount = as.getEndOffset() - as.getStartOffset() #very important to do it like this, giving each character an attribute caused colorization problems/doing the whole thing at once seems to have cleared those problems up.
                    dsd.setCharacterAttributes( z, amount, mas, True )            
            
        def clearAttribute( self, name ):
            dsd = self.editor.getStyledDocument()
            alen = dsd.getLength()
            for z in xrange( alen ):
                element = dsd.getCharacterElement( z )
                as = element.getAttributes()
                if as.containsAttribute( name, name ):
                    mas = stext.SimpleAttributeSet() #We have to make a clean one and copy the data into it!  The one returned is immutable
                    mas.addAttributes( as )
                    mas.removeAttribute( name ) #we remove the tag from here.
                    amount = as.getEndOffset() - as.getStartOffset() #very important to do it like this, giving each character an attribute caused colorization problems
                    dsd.setCharacterAttributes( z, amount, mas, True )
            
        def clearHighlights( self ):
            
            self.editor.getHighlighter().removeAllHighlights()    
            
        
        def addHighlight( self, start, end, color ):
            
            highlighter = self.editor.getHighlighter()
            painter = stext.DefaultHighlighter.DefaultHighlightPainter( color )
            highlighter.addHighlight( start, end, painter )
            
        def getHighlights( self ):
            
            highlighter = self.editor.getHighlighter()
            return highlighter.getHighlights()
            
            
        def removeTextWithAttribute( self, name ):
            
            arange = self.getAttributeRanges( name )
            dsd = self.editor.getStyledDocument()
            alen = len( arange )
            if alen:
                dsd.remove( arange[ 0 ], alen )
            
        def insertTextWithAttribute( self, txt, name ):
            
            sa = stext.SimpleAttributeSet()
            sa.addAttribute( name, name )
            pos = self.editor.getCaretPosition()
            dsd = self.editor.getStyledDocument()
            dsd.insertString( pos, txt, sa )
        #@nonl
        #@-node:ekr.20050723062822.46:attribute and highlight operations
        #@+node:ekr.20050723062822.47:addToKillBuffer
        def addToKillbuffer( self, text ):
            
            self.strategyObjects[ 'killbuffer' ].insertIntoKillbuffer( text )
        #@nonl
        #@-node:ekr.20050723062822.47:addToKillBuffer
        #@+node:ekr.20050723062822.48:Stategies for keystroke and commands
        #@<< about the strategy pattern >>
        #@+node:ekr.20050723062822.49:<< about the strategy pattern >>
        #@@killcolor
        #@+at
        # This node organizes the classes that implement a rough cut of the 
        # Strategy pattern for the keystrokes.
        # 
        # Each recognized keystroke goes to the masterCommand, but the 
        # masterCommand just decides on the code that
        # should be executed, in this case it delegates the call to a Strategy 
        # object that decides upon what methods
        # to process the key stroke.
        # 
        # This has these benefits:
        # 1. State is broken further from the container Object( Emacs ).
        # 2. Changes to the processing methods no longer has global 
        # consequences.  It is conceivable that a different Strategy could
        # be swapped in by configuration or some other means.  All a strategy 
        # has to do is implement the __call__ operator to have
        # the event and keystroke passed into it.
        # 
        # This design is based off of the lessons learned in the temacs plugin 
        # for CPython Leo.  Its evolution followed this pattern:
        # 1. It started as a flat function based module.  Though a useful 
        # learning experiment this grew too large and became
        # hard to think about.  Changes were becoming difficult.
        # 
        # 2. At this point it became apparent that more structure was needed.  
        # It was refactored( in Refactoring this is a 'Big Refactoring')
        # into a class, with some helper classes.  This eased the ability to 
        # reason about and modify the code.
        # 
        # 3. After working with this big class, it became apparent again that 
        # a further restructuring was needed.  The idea of breaking
        # the methods that were grouped under one rubric into further classes 
        # arose; the Strategy pattern seemed to be what was called for.
        # And here we are in SwingMacs making the first cut at this new 
        # decomposed design for the Jython port.
        #@-at
        #@nonl
        #@-node:ekr.20050723062822.49:<< about the strategy pattern >>
        #@nl
        
        #@+others
        #@+node:ekr.20050723062822.50:incremental search
        class incremental:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.iway = None
                
                if 0: ### Not ready yet.
                    i = java.lang.Integer.decode( '#63c6de' )
                    self.highlight = awt.Color( i )
            
            def __call__( self, event, command ):
                
                component = event.getSource()
                stxt = component.getText()
                pos = component.getCaretPosition()
                if command in ( 'Ctrl S', 'Ctrl R' ):
                    self.startIncremental( command )
                    if not self.emacs.minibuffer.getText():
                        return True
                elif command == 'Enter':
                    return self.emacs.keyboardQuit( event )
                else:
                    self.setMiniBuffer( event )
                
        
                if event.getKeyChar() == aevent.KeyEvent.CHAR_UNDEFINED :
                    return True
                
                source = event.getSource()
                wcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.WAIT_CURSOR )
                source.setCursor( wcursor )
                dc = DefCallable( lambda : self.incrementalSearch( event , command, stxt, pos) )
                swing.SwingUtilities.invokeLater( dc.wrappedAsFutureTask() )  
                #return self.incrementalSearch( event , command, stxt, pos)
                return True
                
            def setMiniBuffer( self, event ):
                self.emacs.eventToMinibuffer( event )
                
            #@    @+others
            #@+node:ekr.20050723062822.51:startIncremental
            def startIncremental( self, command ):
            
                if command == 'Ctrl S':
                    self.iway = 'forward'
                else:
                    self.iway = 'backward'
                self.emacs._stateManager.setState( 'incremental' )  
                self.emacs.setCommandText( "I-Search:" )
            #@nonl
            #@-node:ekr.20050723062822.51:startIncremental
            #@+node:ekr.20050723062822.52:incrementalSearch
            def incrementalSearch( self, event, command, stxt, pos ):
                    
                    #self.emacs.clearAttribute( 'incremental' ) 
                    self.emacs.clearHighlights()
                    txt = self.emacs.minibuffer.getText()
                    c = self.emacs.c
                    source = event.getSource()
                    #cursor = source.getCursor()
                    #wcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.WAIT_CURSOR )
                    #source.setCursor( wcursor )
                    # opos = source.getCaretPosition() 
            
                    if self.iway == 'forward':
                        if command != 'Ctrl S' and pos >= len( txt ):
                                pos = pos - len( txt )
                        i = self.forwardSearch( pos, txt, stxt )
                        if i != -1:
                            pos = pos + i + len( txt )
                        else: #start from beginning again
                            #i = self.forwardSearch( 0, txt, stxt )
                            #if i != -1:
                            #    pos = i + len( txt )
                            cp = c.currentPosition()
                            for z in c.currentPosition().fromSelfAllNodes_iter( copy = 1 ):
                                if z == cp: continue
                                i = self.forwardSearch( 0, txt, z.bodyString() )
                                if i != -1:
                                    pos = i + len( txt )
                                    c.beginUpdate()
                                    c.setCurrentPosition( z )
                                    c.endUpdate()
                                    break
                    else:
                        if command != 'Ctrl R' and ( pos + len( txt ) ) <= len( stxt ):
                                pos = pos + len( txt )
                        i = self.backwardSearch( pos, txt, stxt )
                        if i != -1:
                            pos = i
                        else: #start from the back again
                            #i = self.backwardSearch( source.getDocument().getLength(), txt , stxt )
                            #if i != -1:
                            #    pos = i
                            cp = c.currentPosition()
                            for z in c.currentPosition().fromSelfBackAllNodes_iter( copy = 1 ):
                                if z == cp: continue
                                i = self.backwardSearch( len( z.bodyString() ), txt, z.bodyString() )
                                if i != -1:
                                    pos = i
                                    c.beginUpdate()
                                    c.setCurrentPosition( z )
                                    c.endUpdate()
                                    break    
                    
                    #source.setCursor( self.old_cursor )
                    if i == -1: 
                        tcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.TEXT_CURSOR )
                        source.setCursor( tcursor )
                        swing.JOptionPane.showMessageDialog( None, "Can't find %s" % txt )
                        return True
                    dhl = self.deferedHighlight( source, pos, self.iway, self.highlight, len( txt ), self.emacs )   
                    swing.SwingUtilities.invokeLater( dhl )  
                    #source.setCaretPosition( pos )
                    #if self.iway == 'forward':
                    #    start = pos - len( txt )
                    #    self.emacs.addHighlight( start, start + len( txt ), self.highlight ) 
                    #else:
                    #    self.emacs.addHighlight( pos, pos + len( txt ), self.highlight )
                    return True
            #@nonl
            #@-node:ekr.20050723062822.52:incrementalSearch
            #@+node:ekr.20050723062822.53:forward/backwardSearch
            def forwardSearch( self, pos, txt, stxt ):
                
                _stxt = stxt[ pos : ]
                return _stxt.find( txt )
            
            def backwardSearch( self, pos, txt, stxt ):
            
                end = len( stxt ) - pos
                if end != 0:
                    stxt = stxt[ : -end ]
            
                return stxt.rfind( txt )
            #@nonl
            #@-node:ekr.20050723062822.53:forward/backwardSearch
            #@+node:ekr.20050723062822.54:class deferedHighlight ( java.lang.Runnable )
            class deferedHighlight: ## ( java.lang.Runnable ):
                
                def __init__( self, source, pos, iway, highlight, length, emacs ):
                    self.source = source
                    self.pos = pos
                    self.iway = iway
                    self.highlight = highlight
                    self.length = length
                    self.emacs = emacs
            
                def run( self ):
                    source = self.source; pos = self.pos
                    source.setCaretPosition( pos )
                    if self.iway == 'forward':
                        start = pos - self.length
                        self.emacs.addHighlight( start, start + self.length, self.highlight ) 
                    else:
                        self.emacs.addHighlight( pos, pos + self.length, self.highlight )
                    tcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.TEXT_CURSOR )
                    source.setCursor( tcursor )
            #@nonl
            #@-node:ekr.20050723062822.54:class deferedHighlight ( java.lang.Runnable )
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.50:incremental search
        #@+node:ekr.20050723062822.55:dynamic-abbrevs
        class dynamicabbrevs:
            
            #@    @+others
            #@+node:ekr.20050723062822.56:ctor
            def __init__( self, emacs ):
            
                self.emacs = emacs
                self.dynaregex = re.compile( r'[%s%s\-_]+' %( string.ascii_letters, string.digits ) ) #for dynamic abbreviations
                self.searchtext = None
                self.returnlist = []
                self.ind = 0 #last spot wordindex returned
                
                if 1:  ### Not ready yet.
                    self.dynamiclist = []
                else:
                    self.dynamiclist = java.util.TreeSet()
                    self.createDynamicList()
            #@nonl
            #@-node:ekr.20050723062822.56:ctor
            #@+node:ekr.20050723062822.57:__call__
            def __call__( self, event, command ):
            
                if command == 'Alt Slash':
                    self.dynamicExpansion( event )
                if command == 'Ctrl+Alt Slash':
                    self.dynamicExpansion2( event )
            #@nonl
            #@-node:ekr.20050723062822.57:__call__
            #@+node:ekr.20050723062822.58:dynamicExpansion
            def dynamicExpansion( self, event ):#, store = {'rlist': [], 'stext': ''} ):
                
                tag = 'dy-ab'
                word = self.emacs.getWordStart()
                ind = self.emacs.getWordStartIndex()
                
                if not word:
                    self.clearDynamic( tag )
                    return   
                elif word and self.searchtext == None:
                    self.searchtext = word
                    self.ind = ind
                elif not word.startswith( self.searchtext ) or self.ind != ind:
            
                    self.clearDynamic( tag )
                    self.searchtext = word
                    self.ind = ind
            
                
                if self.emacs.getAttributeRanges( tag ): #indicates that expansion has started
                    self.emacs.removeTextWithAttribute( tag )
                    if self.returnlist:
                        txt = self.returnlist.pop()
                        self.emacs.insertTextWithAttribute( txt, tag )
                    else:
                        self.getDynamicList( self.searchtext, self.returnlist )#rebuild
                        self.emacs.insertTextWithAttribute( self.searchtext , tag )
                    return   
                elif self.searchtext:
                    self.getDynamicList( self.searchtext, self.returnlist )
                    if self.returnlist:
                        start = self.emacs.getWordStartIndex()
                        ntxt = self.returnlist.pop()
                        self.emacs.replaceText( start, start + len( word ), ntxt )
                        self.emacs.addAttributeToRange( tag, tag, start, len( ntxt ) )
                        
            
                #tbuffer = event.widget
                #rlist = self.store[ 'rlist' ]
                #stext = self.store[ 'stext' ]
                #i = tbuffer.index( 'insert -1c wordstart' )
                #i2 = tbuffer.index( 'insert -1c wordend' )
                #txt = tbuffer.get( i, i2 )
                #dA = tbuffer.tag_ranges( 'dA' )
                #tbuffer.tag_delete( 'dA' )
                #def doDa( txt, from_ = 'insert -1c wordstart', to_ = 'insert -1c wordend' ):
                #
                #    tbuffer.delete( from_, to_ ) 
                #    tbuffer.insert( 'insert', txt, 'dA' )
                #    return self._tailEnd( tbuffer )
                    
                #if dA:
                #    dA1, dA2 = dA
                #    dtext = tbuffer.get( dA1, dA2 )
                #    if dtext.startswith( stext ) and i2 == dA2: #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
                #        if rlist:
                #            txt = rlist.pop()
                #        else:
                #            txt = stext
                #            tbuffer.delete( dA1, dA2 )
                #            dA2 = dA1 #since the text is going to be reread, we dont want to include the last dynamic abbreviation
                #            self.getDynamicList( tbuffer, txt, rlist )
                #        return doDa( txt, dA1, dA2 )
                #    else:
                #        dA = None
                        
                #if not dA:
                #    self.store[ 'stext' ] = txt
                #    self.store[ 'rlist' ] = rlist = []
                #    self.getDynamicList( tbuffer, txt, rlist )
                #    if not rlist:
                #        return 'break'
                #    txt = rlist.pop()
                #    return doDa( txt )
            #@nonl
            #@-node:ekr.20050723062822.58:dynamicExpansion
            #@+node:ekr.20050723062822.59:dynamicExpansion2
            def dynamicExpansion2( self, event ):
            
                #i = tbuffer.index( 'insert -1c wordstart' )
                #i2 = tbuffer.index( 'insert -1c wordend' )
                i = self.emacs.getWordStartIndex()
                i2 = self.emacs.getWordEndIndex()
                #txt = tbuffer.get( i, i2 )   
                txt = self.emacs.getTextSlice( i, i2 )
                rlist = []
                self.getDynamicList( txt, rlist )
                dEstring = reduce( self.emacs.findPre, rlist )
                if dEstring:
                    self.emacs.replaceText( i, i2, dEstring )
                    #tbuffer.delete( i , i2 )
                    #tbuffer.insert( i, dEstring )    
                    #return self._tailEnd( tbuffer )
            #@nonl
            #@-node:ekr.20050723062822.59:dynamicExpansion2
            #@+node:ekr.20050723062822.60:getDynamicList
            def getDynamicList( self, txt , rlist ):
            
                 ttext = self.emacs.getText()
                 items = self.dynaregex.findall( ttext )
                 for z in items:
                    self.dynamiclist.add( z )    
                        
                           
                            
                 started = 0
                 for z in self.dynamiclist:
                    if z.startswith( txt ):
                         if not started:
                             started = 1
                         rlist.append( z)
                         continue
                    if started:
                        break
                 
                 return rlist
            
            #@+at
            #      ttext = self.emacs.getText()
            #      items = self.dynaregex.findall( ttext ) #make a big list of 
            # what we are considering a 'word'
            #      if items:
            #          for word in items:
            #              if not word.startswith( txt ) or word == txt: 
            # continue #dont need words that dont match or == the pattern
            #              if word not in rlist:
            #                  rlist.append( word )
            #              else:
            #                  rlist.remove( word )
            #                  rlist.append( word )
            #@-at
            #@nonl
            #@-node:ekr.20050723062822.60:getDynamicList
            #@+node:ekr.20050723062822.61:clearDynamic
            def clearDynamic( self, tag  ):
            
                self.emacs.clearAttribute( tag )
                self.returnlist = []
                self.searchtext = None
                self.ind = None
            #@nonl
            #@-node:ekr.20050723062822.61:clearDynamic
            #@+node:ekr.20050723062822.62:createDynamicList
            def createDynamicList( self ):
                
                c = self.emacs.c
                class _buildDynamicList:
                    
                    def __init__( self, c, da ):
                        self.c = c
                        self.da = da
                        
                    def __call__( self ):
                        
                        rp = self.c.rootPosition().copy()
                        for z in rp.allNodes_iter( copy = 1 ):
                            btx = z.bodyString()
                            items = self.da.dynaregex.findall( btx )
                            self.da.dynamiclist.addAll( items )
            
                        g.es( "dynamic list built: dynamic abbreviations online" )
                        
                
                dc = DefCallable( _buildDynamicList( c, self ) )
                self.emacs.c.frame.gui.addStartupTask( dc.wrappedAsFutureTask() )
            #@nonl
            #@-node:ekr.20050723062822.62:createDynamicList
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.55:dynamic-abbrevs
        #@+node:ekr.20050723062822.63:symbolcompletion
        class symbolcompletion:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.start = -1
                self.end = -1
                self.segment = None
                self.commands = {
                    "Ctrl+Alt I" : self.complete
                }
        
                c_dict = dir( leoColor.baseColorizer )
                self.languages = {}
                for z in c_dict:
                    if z.endswith( '_keywords' ):
                        language = z.rstrip( '_keywords' )
                        self.languages[ language ] = getattr( leoColor.baseColorizer, z )
                
                
            def __call__( self, event, command ):
        
                self.commands[ command ]()
                return True
                
                
            def complete( self ):
                
                language = self.emacs.determineLanguage()
                if language == None or language not in self.languages:
                    m = self.languages[ 'python' ]
                else:
                    m = self.languages[ language ]
            
                editor = self.emacs.editor
                doc = editor.getDocument()
                cp = editor.getCaretPosition()
                word = self.emacs.getWordStart()
                if not word:
                    self.start = self.end = -1; self.segment = None
                    return
                lastword = word
                if self.start != -1:
        
                    if self.start == cp - len( word ):
                        word2 = doc.getText( self.start, self.end - self.start )
                        if word2 == self.segment:
                            word = word2
                            doc.replace( cp - len( lastword ), len( lastword ), word, None )
                            cp = editor.getCaretPosition()
                    
                self.start = self.end = -1; self.segment = None
                if word:
                    words = []
                    for z in m:
                        if z.startswith( word ):
                            words.append( z )
                        
                    if not words: return
                    if lastword in m:
                        spot = words.index( lastword )
            
                        if spot == 0 and len( words ) == 1:
                            pass 
                        elif spot + 1 == len( words ):
                            spot = 0
                        else:
                            spot += 1
                          
                        nword = words[ spot ]
                    else:
                        nword = words[ 0 ]
                    
                    doc.replace( cp - len( word ), len( word ), nword, None )
                    self.start = cp - len( word )
                    self.end = cp
                    self.segment = word
        #@nonl
        #@-node:ekr.20050723062822.63:symbolcompletion
        #@+node:ekr.20050723062822.64:formatter
        class formatter:
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.commands = {
                
                'Ctrl+Alt Back Slash': self.indentRegionToFirstLine,
                'indent-region': self.indentRegionToFirstLine,
                'indent-rigidly': self.indentRigidly,  
                'indent-relative': self.indentRelative,
                'Alt Back Slash': self.deleteSurroundingSpaces,
                'Alt+Shift 6': self.joinLineToPrevious,
                'Ctrl O': self.deleteBlankLines,
                
                }
                
            def __call__( self, event, command ):
                rval = self.commands[ command ]()        
                self.emacs.keyboardQuit( event )
                return rval
                        
            #@    @+others
            #@+node:ekr.20050723062822.65:indent-region
            def indentRegionToFirstLine( self ):
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start != end:
                    
                    sstart = stext.Utilities.getRowStart( editor, start )
                    send = stext.Utilities.getRowEnd( editor, end )
                    doc = editor.getStyledDocument()
                    txt = doc.getText( sstart, send - sstart )
                    lines = txt.splitlines()
                    firstline = lines[ 0 ]
                    ws_start = []
                    for z in firstline:
                        if z.isspace():
                            ws_start.append( z )
                        else:
                            break
                            
                    ws_segment = ''.join( ws_start )
                    nwlines = [ firstline, ]
                    for x in lines[ 1: ]:
                        x_nws = x.lstrip()
                        x_new = '%s%s' % ( ws_segment, x_nws )
                        nwlines.append( x_new )
                        
                    new_txt = '\n'.join( nwlines )
                    pos = editor.getCaretPosition()
                    doc.replace( sstart, send - sstart, new_txt, None )
                    
                return True
            #@nonl
            #@-node:ekr.20050723062822.65:indent-region
            #@+node:ekr.20050723062822.66:indent-rigidly
            def indentRigidly( self ):
                
                editor = self.emacs.editor
                txt = editor.getSelectedText()
                if txt == None: return True
                
                txtlines = txt.splitlines( True )
                ntxtlines = []
                for z in txtlines:
                    
                    nline = '\t%s' % z
                    ntxtlines.append( nline )
                    
                
                ntxt = ''.join( ntxtlines )
                pos = editor.getCaretPosition()
                editor.replaceSelection( ntxt )
                editor.setCaretPosition( pos )
                return True
            #@nonl
            #@-node:ekr.20050723062822.66:indent-rigidly
            #@+node:ekr.20050723062822.67:indent-relative
            def indentRelative( self ):
            
                editor = self.emacs.editor
                sd = editor.getStyledDocument()
                pos = editor.getCaretPosition()
                
                txt = editor.getText()
                
                
                plstart, plend = self.definePreviousLine()
                
                if plstart == -1 or plend == -1:
                    sd.insertString( pos, '\t', None )
                    return True         
                   
            
                ltxt = txt[ plstart: plend ]
            
                
                find = txt.rfind( '\n', 0, pos )
                find += 1
                rlpos = pos - find
                
                if rlpos > ( len( ltxt ) -1 ):
                    sd.insertString( pos, '\t', None )
                    return True
                    
                addon = []
                for z in ltxt[ : rlpos ]:
                    if z.isspace():
                        addon.append( z )
                    else:
                        addon.append( ' ' )
                        
                add = ''.join( addon )
                
                if ltxt[ rlpos ].isspace():
                    addon = []
                    for z in ltxt[ rlpos: ]:
                        if z.isspace():
                            addon.append( z )
                        else:
                            break
                    add = add + ''.join( addon )
                else:
                    addon = []
                    for z in ltxt[ rlpos: ]:
                        if z.isspace(): break
                        else:
                            addon.append( ' ' )
                    
                    add = add + ''.join( addon )
                    rlpos += len( addon )
                    addon = []
                    for z in ltxt[ rlpos: ]:
                        if z.isspace():
                            addon.append( z )
                        else:
                            break
                    add = add + ''.join( addon )
                if txt[ find: pos ].isspace():               
                    sd.replace( find, pos - find, '' , None )
                    sd.insertString( find, add, None )
                else:
                    atext = txt[ find: pos ]
                    atext = atext.rstrip()
                    atext = atext + add[ len( atext ) -1 : ]
                    sd.replace( find, pos - find, '', None )
                    sd.insertString( find, atext, None )
                     
                return True
            #@nonl
            #@-node:ekr.20050723062822.67:indent-relative
            #@+node:ekr.20050723062822.68:deleteSurroundingSpaces
            def deleteSurroundingSpaces( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()    
                if pos != -1:
                    
                    start = stext.Utilities.getRowStart( editor, pos )
                    end = stext.Utilities.getRowEnd( editor, pos )
                    doc = editor.getDocument()
                    txt = doc.getText( start, end - start )
                    rpos = pos - start
                    part1 = txt[ : rpos ]
                    part1 = part1.rstrip()
                    part2 = txt[ rpos: ]
                    part2 = part2.lstrip()
                    doc.replace( start, end - start, "%s%s" %( part1, part2 ), None )
                    editor.setCaretPosition( start + len( part1 ) )
            #@nonl
            #@-node:ekr.20050723062822.68:deleteSurroundingSpaces
            #@+node:ekr.20050723062822.69:joinLineToPrevious
            def joinLineToPrevious( self ):
                
                plstart, plend = self.definePreviousLine()
                if plstart == -1 or plend == -1:
                    return
                    
                editor = self.emacs.editor
                pos = editor.getCaretPosition() 
                if pos != -1:
                    
                    doc = editor.getDocument()
                    start = stext.Utilities.getRowStart( editor, pos )
                    end = stext.Utilities.getRowEnd( editor, pos )
                    txt = doc.getText( start, end - start )
                    txt = ' %s' % txt.lstrip()
                    doc.remove( start, end - start )
                    doc.insertString( plend, txt, None )
                    editor.setCaretPosition( plend )
            #@nonl
            #@-node:ekr.20050723062822.69:joinLineToPrevious
            #@+node:ekr.20050723062822.70:deleteBlankLines
            def deleteBlankLines( self ):
            
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != -1:
                    
                    doc = editor.getDocument()
                    start = stext.Utilities.getRowStart( editor, pos )
                    end = stext.Utilities.getRowEnd( editor, pos )
                    txt = doc.getText( 0, doc.getLength() )
                    cline = txt[ start: end ] + '\n'
                    
                    first = txt[ : start ]
                    lines = first.splitlines( 1 )
                    lines.reverse()
                    #line = lines[ 0 ]
                    #del lines[ 0 ]
                    #line = lines.pop()
                    cpos_minus = 0
                    if cline.isspace():
                        for z in xrange( len( lines )):
                            if lines[ 0 ].isspace() or lines[ 0 ] == "":                    
                                cpos_minus += len( lines[ 0 ] )
                                del lines[ 0 ]
                            else:
                                break
                    lines.reverse()
                    #lines.append( line )
                    
                    
                    end = txt[ end: ]
                    lines2 = end.splitlines( 1 )
                    #line = lines2[ 0 ]
                    #del lines2[ 0 ]
                    for z in xrange( len( lines2 ) ):
                        if lines2[ 0 ].isspace() or lines2[ 0 ] == "":
                            #lines2.pop()
                            del lines2[ 0 ]
                        else:
                            break
                    #lines2.insert( 0, line )
                    fpart = ''.join( lines )
                    spart = ''.join( lines2 )
                    nwtext = '%s%s%s' %( fpart, cline, spart )
                    doc.replace( 0, doc.getLength(), nwtext, None )
                    editor.setCaretPosition( pos - cpos_minus )
                    return True
            #@nonl
            #@-node:ekr.20050723062822.70:deleteBlankLines
            #@+node:ekr.20050723062822.71:definePreviousLine
            def definePreviousLine( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                
                txt = editor.getText()
                find = txt.rfind( '\n', 0, pos )
                if find == -1:
                    return -1, -1
                else:
                    find2 = txt.rfind( '\n', 0, find )
                    if ( find2 - 1 ) == find:
                        return -1, -1
                    elif find2 == -1:
                        find2 = 0
                    else:
                        find2 += 1    
            
                return find2, find
            #@nonl
            #@-node:ekr.20050723062822.71:definePreviousLine
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.64:formatter
        #@+node:ekr.20050723062822.72:killbuffer
        class killbuffer:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.killbuffer = []
                self.cliptext = None
                
                #for killbuffer
                self.last_clipboard = None
                self.kbiterator = self.iterateKillBuffer()
                self.reset = False
                self.lastKBSpot = None
        
            def __call__( self, event, command ):
                if command == 'Ctrl K':
                    self.killToEndOfLine()
                if command == 'Alt Y':
                    self.walkKB()
                if command == 'Ctrl Y':
                    self.yank()
                if command == 'Ctrl W':
                    self.killRegion()
                if command == 'Alt W':
                    self.copyRegion()
                   
                self.emacs.keyboardQuit( event )
                return True    
                
            #@    @+others
            #@+node:ekr.20050723062822.73:kill
            def kill( self, frm, end ):
                
                editor = self.emacs.editor
                doc = editor.getStyledDocument()
                if frm != end:
                    txt = doc.getText( frm, end - frm )
                    doc.replace( frm, end - frm, "", None )
                    self.insertIntoKillbuffer( txt )
                    g.app.gui.replaceClipboardWith( txt )
                else:
                    if frm != doc.getLength():
                        doc.replace( frm, 1, "", None )
            #@nonl
            #@-node:ekr.20050723062822.73:kill
            #@+node:ekr.20050723062822.74:insertIntoKillbuffer
            def insertIntoKillbuffer( self, txt ):
                
                self.killbuffer.insert( 0, txt )
                self.reset = True
            #@nonl
            #@-node:ekr.20050723062822.74:insertIntoKillbuffer
            #@+node:ekr.20050723062822.75:killToEndOfLine
            def killToEndOfLine( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                end = stext.Utilities.getRowEnd( editor, pos )
                self.kill( pos, end  )    
                return True
            #@nonl
            #@-node:ekr.20050723062822.75:killToEndOfLine
            #@+node:ekr.20050723062822.76:copyRegion
            def copyRegion( self ):
            
                region = self.getRegion()
                if region:
                    editor = self.emacs.editor
                    doc = editor.getStyledDocument()
                    start = region[ 0 ]
                    end = region[ 1 ]
                    txt = doc.getText( start, end-start )
                    self.insertIntoKillbuffer( txt )
                return True
            #@nonl
            #@-node:ekr.20050723062822.76:copyRegion
            #@+node:ekr.20050723062822.77:killRegion
            def killRegion( self ):
                
                region = self.getRegion()
                if region:
                    self.kill( *region )
                return True
            #@nonl
            #@-node:ekr.20050723062822.77:killRegion
            #@+node:ekr.20050723062822.78:getRegion
            def getRegion( self ):
            
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if end == start: return None
                else:
                    return start, end
            #@nonl
            #@-node:ekr.20050723062822.78:getRegion
            #@+node:ekr.20050723062822.79:walkKB
            def walkKB( self ): #, event , frm, which ):# kb = self.iterateKillBuffer() ):
            
                #tbuffer = event.widget
                #i = tbuffer.index( 'insert' )
                #t , t1 = i.split( '.' )
                pos = self.emacs.editor.getCaretPosition()
                if pos != self.lastKBSpot:
                    self.emacs.clearAttribute( 'kb' )
                self.lastKBSpot = pos
                clip_text = self.doesClipboardOfferNewData() #  self.getClipboard()  
                #clip_txt = g.app.gui.getTextFromClipboard().   
                if self.killbuffer or clip_text:
                        #if which == 'c':
                        #self.reset = True
                        if clip_text:
                            txt = clip_text
                        else:
                            txt = self.kbiterator.next()
                        self.emacs.removeTextWithAttribute( 'kb' )
                        self.emacs.insertTextWithAttribute( txt, 'kb' )
                        self.emacs.editor.setCaretPosition( pos )
                        #tbuffer.tag_delete( 'kb' )
                        #tbuffer.insert( frm, txt, ('kb') )
                        #tbuffer.mark_set( 'insert', i )
                        #else:
                        #if clip_text:
                        #    txt = clip_text
                        #else:
                        #    txt = self.kbiterator.next()
                        #t1 = str( int( t1 ) + len( txt ) )
                        #r = tbuffer.tag_ranges( 'kb' )
                        #if r and r[ 0 ] == i:
                        #    tbuffer.delete( r[ 0 ], r[ -1 ] )
                        #tbuffer.tag_delete( 'kb' )
                        #tbuffer.insert( frm, txt, ('kb') )
                        #tbuffer.mark_set( 'insert', i )
                        #return self._tailEnd( tbuffer )
                        
                return True
            #@nonl
            #@-node:ekr.20050723062822.79:walkKB
            #@+node:ekr.20050723062822.80:yank
            def yank( self ):
                self.reset = True
                return self.walkKB()
            #@nonl
            #@-node:ekr.20050723062822.80:yank
            #@+node:ekr.20050723062822.81:iterateKillBuffer
            def iterateKillBuffer( self ):
            
                while 1:
                    if self.killbuffer:
                        self.last_clipboard = None
                        for z in self.killbuffer:
                            if self.reset:
                                self.reset = False
                                break        
                            yield z
            #@nonl
            #@-node:ekr.20050723062822.81:iterateKillBuffer
            #@+node:ekr.20050723062822.82:doesClipboardOfferNewData
            def doesClipboardOfferNewData( self  ):
                
                ctxt = None
                try:
                    #ctxt = tbuffer.selection_get( selection='CLIPBOARD' )
                    ctxt = g.app.gui.getTextFromClipboard()
                    if ctxt != self.last_clipboard or not self.killbuffer:
                        self.last_clipboard = ctxt
                        if self.killbuffer and self.killbuffer[ 0 ] == ctxt:
                            return None
                        return ctxt
                    else:
                        return None
                    
                except:
                    return None
                    
                return None
            #@nonl
            #@-node:ekr.20050723062822.82:doesClipboardOfferNewData
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.72:killbuffer
        #@+node:ekr.20050723062822.83:deleter
        class deleter:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                
            def __call__( self, event, command ):
                if command == 'Delete':
                    return self.deletePreviousChar()
                if command == 'Ctrl D':
                    return self.deleteNextChar()
                    
            #@    @+others
            #@+node:ekr.20050723062822.84:deletePreviousChar
            def deletePreviousChar( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != 0:
                    doc = editor.getStyledDocument()
                    spos = pos -1
                    doc.replace( spos, 1 , "", None )
                return True
            #@nonl
            #@-node:ekr.20050723062822.84:deletePreviousChar
            #@+node:ekr.20050723062822.85:deleteNextChar
            def deleteNextChar( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                doc = editor.getStyledDocument()
                if pos != doc.getLength():
                    doc.replace( pos, 1 , "", None )
                return True
            #@nonl
            #@-node:ekr.20050723062822.85:deleteNextChar
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.83:deleter
        #@+node:ekr.20050723062822.86:alt_x_handler
        class alt_x_handler:
            
            #@    @+others
            #@+node:ekr.20050723062822.87: __call__
            def __call__( self, event, command ):
                
                if command == 'Alt X':
                    self.tbCompleter.reset()
                    self.last_command = None
                    self.emacs._stateManager.setState( 'xcommand' ) 
                    self.emacs.setCommandText( "Alt-x:" )
                    return True
                
                if command == 'Tab':
                    txt = self.emacs.minibuffer.getText()
                    if self.last_command == None or not txt.startswith( self.last_command ):
                        txt = self.emacs.minibuffer.getText()
                        fnd = self.tbCompleter.lookFor( txt )
                        if fnd:
                            self.last_command = txt
                            self.emacs.minibuffer.setText( self.tbCompleter.getNext() )
                    else :
                        self.emacs.minibuffer.setText( self.tbCompleter.getNext() )
                    return True
                
                if command == 'Enter':
                    return self.execute( event, command )
                else:
                    self.emacs.eventToMinibuffer( event )
                    return True    
            #@nonl
            #@-node:ekr.20050723062822.87: __call__
            #@+node:ekr.20050723062822.88: ctor
            def __init__( self, emacs ):
                self.emacs = emacs
                self.defineCommands()
                self.last_command = None
                self.keys = []
            #@-node:ekr.20050723062822.88: ctor
            #@+node:ekr.20050723062822.89:createTabCompleter
            def createTabCompleter( self ):
            
                self.keys = self.commands.keys()
                self.tbCompleter = self.emacs.TabCompleter( self.keys )
            #@nonl
            #@-node:ekr.20050723062822.89:createTabCompleter
            #@+node:ekr.20050723062822.90:defineCommands
            def defineCommands( self ):
                
                sO = self.emacs.strategyObjects
                self.commands = {
                'open-rectangle': sO[ 'rectangles' ],        
                'delete-rectangle': sO[ 'rectangles' ],
                'clear-rectangle': sO[ 'rectangles' ],
                'delete-whitespace-rectangle': sO[ 'rectangles' ],
                'string-insert-rectangle': sO[ 'rectangles' ],
                'string-rectangle': sO[ 'rectangles' ],
                'kill-rectangle': sO[ 'rectangles' ],
                'yank-rectangle': sO[ 'rectangles' ],
                'zap-to-char': sO[ 'zap' ],
                'comment-region': sO[ 'comment' ],
                'comment-kill': sO[ 'comment' ],
                'goto-line': sO[ 'movement' ],
                'goto-char': sO[ 'movement' ],
                'transpose-lines': sO[ 'transpose' ],
                'upcase-region': sO[ 'capitalization' ],
                'downcase-region': sO[ 'capitalization' ],
                'capitalize-region': sO[ 'capitalization' ],
                'capitalize-word': sO[ 'capitalization' ],
                 'downcase-word': sO[ 'capitalization' ],
                 'upcase-word': sO[ 'capitalization' ],
                'query-replace': sO[ 'replacement' ],
                'query-replace-regexp': sO[ 'replacement' ],
                'replace-string': sO[ 'replacement' ],
                'sort-lines': sO[ 'sorters' ],
                'reverse-region': sO[ 'transpose' ],
                'keep-lines': sO[ 'lines' ],
                'flush-lines': sO[ 'lines' ],
                'indent-rigidly': sO[ 'formatter' ],
                'indent-region': sO[ 'formatter' ],
                'indent-relative': sO[ 'formatter' ],
                'tabify': sO[ 'tabs' ],
                'untabify': sO[ 'tabs' ],
                'copy-to-register': sO[ 'registers' ],
                'insert-register': sO[ 'registers' ],
                'append-to-register': sO[ 'registers' ],
                'prepend-to-register': sO[ 'registers' ],
                }
            #@nonl
            #@-node:ekr.20050723062822.90:defineCommands
            #@+node:ekr.20050723062822.91:execute
            def execute( self, event, command ):
                
                txt = self.emacs.minibuffer.getText()
                if self.commands.has_key( txt ):
                    return self.commands[ txt ]( event, txt )
                else:
                    self.emacs.keyboardQuit( event )
                    self.emacs.setCommandText( "Command Not Defined" )
            #@nonl
            #@-node:ekr.20050723062822.91:execute
            #@+node:ekr.20050723062822.92:getCommandHelp
            def getCommandHelp( self ):
                
                commands = '''
                Commands are accessed by the Alt-X keystroke.  This will put the system in command mode.
                The user can type in the name of the command in the minibuffer and execute it with an Enter keypress.
                
                A shortcut to accessing commands is to type a prefix of the command in the minibuffer and hit Tab.
                
                For example:
                op(Tab press )
                could become:
                open-rectangle
                
                the user then just has to type Enter and the open-rectangle command is executed.  Also by repeatedly
                typing Tab the user will cycle through all commands that start with the entered prefix.  So if there
                were 5 commands, for example, that started with 'op' the user could cycle through them and choose the
                one that he wanted to execute.
                
                
                Rectangles
                -----------
                A Rectangle is defined by connecting 4 parallel points derived from
                the begining of the selction and the end of the selction.
                
                These commands operate on Rectangles:
                
                open-rectangle: inserts a whitespace equal to the rectangles width into each rectangle line.
                clear-rectangle: wipes out character content within the rectangle and replaces it with whitespace.
                delete-rectangle: removes characters within the rectangle.
                kill-rectangle: removes characters within the rectangle and stores the data in the kill rectangle
                yank-rectangle: inserts the data last stored by the kill-rectangle command
                delete-whitespace-rectangle: removes whitespace from the begining of each line in the rectangle.
                string-rectangle: replaces each section of the rectangle with a user specified string.
                string-insert-rectangle: inserts a user specified string into each section of the rectangle.
                
                
                Registers:
                ------------
                Registers are places, defined by the letters a-z, where the user can store data temporarily.  There
                are a variety of register commands:
                    
                copy-to-register: copy the selected text to a register specified by the user.
                append-to-register: copy the selected text to the end of a register.
                prepend-to-register: copy the selected text to the beginning of a register.
                insert-register: insert a register into the current buffer.
                
                Zapping
                --------
                Zapping queries for a character from the current caret position.  If it finds the character,
                all data between the caret and including that character is removed.
                
                commands:
                zap-to-char: zaps to the specified character.
                
                Comments:
                ---------
                
                commands:
                comment-region: comments the selected region with the comment character for the current language.  If a line
                                within the region is commented, it will remove the comments instead of commenting.
                comment-kill: removes the comment on the current line
                
                Movement:
                ---------
                goto-line: moves the caret to the line specified by the user.
                goto-char: moves the caret to the character specified by the user.
                
                
                Transposition:
                --------------
                
                transpose-lines: swaps the current line with the line above it.
                reverse-region: takes region and reverses the ordering of the lines, last becomes first, first last.
                
                
                Capitalization:
                ---------------
                
                upcase-region: Upper cases all the text in the selection.
                downcase-region: Lower cases all the text in the selection.
                capitalize-region: Capitalizes all the text in the selection.
                upcase-word: Upper cases the current word.
                downcase-word: Lower cases the current word.
                capitalize-word: Capitalizes the current word. 
                
                Querying and Replacing:
                -----------------------
                SwingMacs has several different query and replace commands.  Each asks the user
                for a search string/pattern and text to replace matches with.  Each has different
                levels of interactivity.
                
                commands:
                query-replace: asks the user for a string to match and a string to replace.  Is asked for each individual word
                               if replacement is desired. '!' replaces all.
                query-replace-regexp: asks the user for a regular expression to match and a string to replace.  Is asked for each individual word
                               if replacement is desired. '!' replaces all.  The regular expressions are executed from the java.util.regex
                               package, see details in javadoc.
                replace-string: asks user for a string to match and a replacement string.  Upon execution all matches are replaced.
                
                Sorting:
                --------
                
                sort-lines: sorts the selected lines of text. 
                
                Lines:
                ------
                
                flush-lines: removes lines that match a regular expression. The regular expressions are executed from the java.util.regex
                               package, see details in javadoc.
                               
                keep-lines: keeps lines that match a regular expression.  Same regular expression details as flush-lines.
                
                Indenting:
                ----------
                
                indent-region: indents region to the indentation of the first line in the region.
                indent-rigidly: indents region by a tab   
                indent-relative: indents by these rules:
                    1. If no previous line, indents by a tab
                    2. If a previous line, will indent to the first word of that line.  This process
                    continues from word to word on the previous line.
                
                Tabs:
                -----
                
                tabify: changes spaces in selected region into tabs.
                untabify: changes tabs in selected region into spaces.          
                
                '''
                
                more_help = '\n'.join( self.emacs.command_help )
                
                commands += more_help
                
                return commands
            #@nonl
            #@-node:ekr.20050723062822.92:getCommandHelp
            #@-others
        #@-node:ekr.20050723062822.86:alt_x_handler
        #@+node:ekr.20050723062822.93:ctrl_x_handler
        class ctrl_x_handler:
            
            #@    @+others
            #@+node:ekr.20050723062822.94: ctor
            def __init__( self, emacs ):
            
                self.emacs = emacs
                self.defineCommands()
                self.last_command = None
                self.keys = []
            #@nonl
            #@-node:ekr.20050723062822.94: ctor
            #@+node:ekr.20050723062822.95:defineCommands
            def defineCommands( self ):
                
                sO = self.emacs.strategyObjects
            
                self.commands = {
                    'Ctrl O': sO[ 'formatter' ],
                }
            #@nonl
            #@-node:ekr.20050723062822.95:defineCommands
            #@+node:ekr.20050723062822.96: __call__
            def __call__( self, event, command ):
            
                if command == 'Ctrl X':
                    #self.tbCompleter.reset()
                    self.last_command = None
                    self.emacs._stateManager.setState( 'ctrlx' ) 
                    self.emacs.setCommandText( "Ctrl-x:" )
                    return True
                    
                if command in self.commands:
                    return self.commands[ command ]( event, command )
            #@nonl
            #@-node:ekr.20050723062822.96: __call__
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.93:ctrl_x_handler
        #@+node:ekr.20050723062822.97:ctrl_u handler
        class ctrl_u_handler:
            
            #@    @+others
            #@+node:ekr.20050723062822.98:ctor
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.defineCommands()
                self.last_command = None
                self.keys = []
            #@nonl
            #@-node:ekr.20050723062822.98:ctor
            #@+node:ekr.20050723062822.99:defineCommands
            def defineCommands( self ):
                
                sO = self.emacs.strategyObjects
                
                self.commands = {
                    'Alt Period': sO[ 'tags' ],
                }
                
            #@nonl
            #@-node:ekr.20050723062822.99:defineCommands
            #@+node:ekr.20050723062822.100: __call__
            def __call__( self, event, command ):
                
                if command == 'Ctrl U':
                    #self.tbCompleter.reset()
                    self.last_command = None
                    self.emacs._stateManager.setState( 'ctrlu' ) 
                    self.emacs.setCommandText( "Ctrl-u:" )
                    return True
                    
                if command in self.commands:
                    return self.commands[ command ]( event, "Ctrl U %s" % command )
            #@nonl
            #@-node:ekr.20050723062822.100: __call__
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.97:ctrl_u handler
        #@+node:ekr.20050723062822.101:rectangles
        class rectangles:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.commands = {
                
                'open-rectangle': self.openRectangle,
                'delete-rectangle': self.deleteRectangle,
                'clear-rectangle': self.clearRectangle,
                'delete-whitespace-rectangle': self.deleteWhiteSpaceRectangle,
                'string-insert-rectangle': self.stringInsertRectangle,
                'string-rectangle': self.stringRectangle,
                'kill-rectangle': self.killRectangle,
                'yank-rectangle': self.yankRectangle,
                
                }
                
                self.mode = None
                emacs.modeStrategies.append( self )
                self.last_killed_rectangle = None      
                
            def __call__( self, event, command ):
                
                if self.mode:
                    if command == 'Enter':
                        if self.mode == 1:
                            self.stringInsertRectangle()
                            return self.emacs.keyboardQuit( event )
                        elif self.mode == 2:
                            self.stringRectangle()
                            return self.emacs.keyboardQuit( event )
                    else:
                        return  self.emacs.eventToMinibuffer( event )
                
                if command in self.commands:
                    quit = self.commands[ command ]()
                    if quit:
                        return self.emacs.keyboardQuit( event )
                    else: return True
                
            #@    @+others
            #@+node:ekr.20050723062822.102:definePoints
            def definePoints( self, start, end ):
            
                txt = self.emacs.editor.getText()
                rl_start = txt.rfind( '\n', 0, start )
                if rl_start == -1: rl_start = 0
                else: 
                    rl_start = rl_start + 1
                    
                pos = start - rl_start
                    
                rl_end = txt.rfind( '\n', 0, end )
                if rl_end == -1: rl_end = 0
                else:
                    rl_end = rl_end + 1  
                    
                pos2 = end - rl_end
                
                return pos, pos2, rl_start, rl_end
            #@nonl
            #@-node:ekr.20050723062822.102:definePoints
            #@+node:ekr.20050723062822.103:insertText
            def insertText( self, rl_start, end, ntxt ):
             
                sd = self.emacs.editor.getStyledDocument()
                sd.remove( rl_start, end - rl_start )
                sd.insertString( rl_start, ntxt, None ) 
                return True
            #@nonl
            #@-node:ekr.20050723062822.103:insertText
            #@+node:ekr.20050723062822.104:open-rectangle
            def openRectangle( self ):
                    
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )  
                    txt = txt[ rl_start: end ]
                
                    
                    insert = ' ' * ( pos2  - pos )
            
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                        else:
                            nwline = '%s%s%s' %( z[ :pos ], insert, z[ pos : ] )
                            ntxtlines.append( nwline )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    return self.insertText( rl_start, end, ntxt )
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None ) 
                    #return True
            #@nonl
            #@-node:ekr.20050723062822.104:open-rectangle
            #@+node:ekr.20050723062822.105:clear-rectangle
            def clearRectangle( self ):
                
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )
                    txt = txt[ rl_start: end ]
                
                    replace = ' ' * ( pos2  - pos )
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                        else:
                            nwline = '%s%s%s' %( z[ :pos ], replace, z[ pos2 : ] )
                            ntxtlines.append( nwline )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    return self.insertText( rl_start, end, txt )
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None )     
                    #return True
            #@nonl
            #@-node:ekr.20050723062822.105:clear-rectangle
            #@+node:ekr.20050723062822.106:kill-rectangle
            def killRectangle( self ):
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )
                    txt = txt[ rl_start: end ]
                
            
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    oldlines = []
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                            oldlines.append( z )
                        else:
                            nwline = '%s%s' %( z[ :pos ], z[ pos2 : ] )
                            ntxtlines.append( nwline )
                            oldlines.append( z[ pos: pos2 ] )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None )
                    self.last_killed_rectangle = oldlines  
                    return self.insertText( rl_start, end, ntxt )   
                    #return True
            #@nonl
            #@-node:ekr.20050723062822.106:kill-rectangle
            #@+node:ekr.20050723062822.107:yank-rectangle
            def yankRectangle( self ):
                
                if self.last_killed_rectangle == None: return True
                
                editor = self.emacs.editor
                start = editor.getCaretPosition()
                
                if start > -1:
                    
                    txt = editor.getText()
                    
                    rl_start = txt.rfind( '\n', 0, start )
                    if rl_start == -1: rl_start = 0
                    else: 
                        rl_start = rl_start + 1
                        
                    
                    pos = start - rl_start
                    
                    sd = editor.getStyledDocument()
                    start2 = rl_start
                    for itext in self.last_killed_rectangle:
                        
                        if sd.getLength() < start2:
                            sd.insertString( sd.getLength(), '%s%s' %( itext, '\n' ), None )
                            start2 += len( itext ) + 1
                        else:
                            if( sd.getText( start2 , 1 ) == '\n' ):
                                sd.insertString( start2, itext, None )
                                nspot = start2 + len( itext )
                            else:
                                sd.insertString( start2 + pos, itext, None )
                                nspot = start2 + pos + len( itext )
                  
                            ftxt = sd.getText( 0, sd.getLength() )
                            where = ftxt.find( '\n', nspot )
                            if where == -1:
                                sd.insertString( sd.getLength(), '\n', None )
                                start2 = sd.getLength() + 1
                            else:
                                start2 = where + 1   
                        
                    
                    return True
            #@nonl
            #@-node:ekr.20050723062822.107:yank-rectangle
            #@+node:ekr.20050723062822.108:delete-rectangle
            def deleteRectangle( self ):
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )
                    txt = txt[ rl_start: end ]
                
            
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                        else:
                            nwline = '%s%s' %( z[ :pos ], z[ pos2 : ] )
                            ntxtlines.append( nwline )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None )     
                    #return True 
                    return self.insertText( rl_start, end, ntxt )
            #@nonl
            #@-node:ekr.20050723062822.108:delete-rectangle
            #@+node:ekr.20050723062822.109:delete-whitespace-rectangle
            def deleteWhiteSpaceRectangle( self ):
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )
                    txt = txt[ rl_start: end ]
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                        else:
                            if z[ pos ].isspace():
                                space_text = z[ pos: pos2 ]
                                space_text = space_text.lstrip()
                                nwline = '%s%s%s' % ( z[ :pos ], space_text, z[ pos2 : ] )
                            else:
                                nwline = z
                            ntxtlines.append( nwline )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    return self.insertText( tl_start, end, ntxt )
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None )      
                    #return True
            #@nonl
            #@-node:ekr.20050723062822.109:delete-whitespace-rectangle
            #@+node:ekr.20050723062822.110:string-rectangle
            def stringRectangle( self ):
                
                if self.mode == None:
                    self.mode = 2
                    self.emacs.setCommandText( "string-rectangle" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( 'rectangles' )
                    return False
                    
                    
                self.mode = None
                string_txt = self.emacs.minibuffer.getText()
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )
                    txt = txt[ rl_start: end ]
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                        else:
                            nwline = '%s%s%s' % ( z[ :pos ], string_txt , z[ pos2 : ] )
                            ntxtlines.append( nwline )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    return self.insertText( rl_start, end, ntxt )
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None )         
                    #return True
            #@nonl
            #@-node:ekr.20050723062822.110:string-rectangle
            #@+node:ekr.20050723062822.111:string-insert-rectangle
            def stringInsertRectangle( self ):
                
                if self.mode == None:
                    self.mode = 1
                    self.emacs.setCommandText( "string-insert-rectangle" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( 'rectangles' )
                    return False
                    
                    
                self.mode = None
                string_txt = self.emacs.minibuffer.getText()
                
                editor = self.emacs.editor
                start = editor.getSelectionStart()
                end = editor.getSelectionEnd()
                if start > -1:
                    
                    txt = editor.getText()
                    
                    pos, pos2, rl_start, rl_end = self.definePoints( start, end )
                    txt = txt[ rl_start: end ]
                    txtline = txt.split( '\n' )
            
                    ntxtlines = [  ]
                    for z in txtline[ : ]:
                        if( len( z ) - 1 ) < pos:
                            ntxtlines.append( z )
                        else:
                            nwline = '%s%s%s' % ( z[ :pos ], string_txt , z[ pos : ] )
                            ntxtlines.append( nwline )
                    
                    if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
                    ntxt = '\n'.join( ntxtlines ) 
                    
                    return self.insertText( rl_start, end, ntxt )
                    #sd = editor.getStyledDocument()
                    #sd.remove( rl_start, end - rl_start )
                    #sd.insertString( rl_start, ntxt, None )         
                    #return True
            #@nonl
            #@-node:ekr.20050723062822.111:string-insert-rectangle
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.101:rectangles
        #@+node:ekr.20050723062822.112:zap
        class zap:
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.mode = None
                emacs.modeStrategies.append( self )
                
            def __call__( self, event, command ):
                
                if self.mode == None:
                    
                    self.mode = 1
                    self.emacs._stateManager.setState( 'zap' )
                    self.emacs.setCommandText( "Zap To Character:" )
                    self.emacs.minibuffer.setText( "" )
                    return True
                    
                if command == 'Enter':
                    c = self.emacs.minibuffer.getText()
                    if len( c ) > 1:
                        self.emacs.keyboardQuit( event )
                        self.emacs.setCommandText( "Text longer than one Character" )
                        return True
                    
                    self.zap( c )
                    return self.emacs.keyboardQuit( event )
                
                else:
                    kc = event.getKeyChar()
                    if java.lang.Character.isDefined( kc ):
                        message = self.zap( kc )
                        self.emacs.keyboardQuit( event )
                        if message:
                            self.emacs.setCommandText( message )
                        return True
                    else:
                        return True
                    
                    
            #@    @+others
            #@+node:ekr.20050723062822.113:zap
            def zap( self, c ):
                
                editor = self.emacs.editor
                doc = editor.getStyledDocument()
                pos = editor.getCaretPosition()
                txt = editor.getText( pos, ( doc.getLength() - 1 ) - pos  )
                ind = txt.find( c )
                if ind == -1:
                    self.emacs.beep()
                    return "Search Failed: '%s'" % c
                else:
                    doc.remove( pos, ind + 1 )
            #@nonl
            #@-node:ekr.20050723062822.113:zap
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.112:zap
        #@+node:ekr.20050723062822.114:comment
        class comment:
        
            def __init__( self, emacs ):
                self.emacs = emacs
                self.commands ={
                    'comment-region': self.commentRegion,
                    'comment-kill': self.commentKill,
                }
                
            def __call__( self, event, command ):
                
                message = self.commands[ command ]()
                if message:
                    self.emacs.keyboardQuit( event )
                    self.emacs.setCommandText( message )
                    self.emacs.beep()
                    return True
                else:
                    return self.emacs.keyboardQuit( event )
        
            #@    @+others
            #@+node:ekr.20050723062822.115:comment-region
            def commentRegion( self ):
                
                language = self.emacs.determineLanguage()
                delim1,delim2, delim3 = g.set_delims_from_language( language )
                
                editor = self.emacs.editor
                sel = editor.getSelectedText()
                if sel == None: return
                
                lines = sel.splitlines( True )
                nwlines = []
                for z in lines:
                    
                    if z.find( delim1 ) != -1:
                        nwline = z.replace( delim1, "" )
                        nwlines.append( nwline )
                    else:
                        z2 = z.lstrip()
                        ins = ( len( z ) - len( z2 ) )
                        if ins == -1: ins = 0
                        nwline = '%s%s%s' %( z[ : ins ], delim1, z[ ins: ] )
                        nwlines.append( nwline )
                    
                
                nwtext = ''.join( nwlines )
                editor.replaceSelection( nwtext )
            #@nonl
            #@-node:ekr.20050723062822.115:comment-region
            #@+node:ekr.20050723062822.116:comment-kill
            def commentKill( self ):
                
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos == -1: return "Invalid Caret position"
                else:
                    txt = editor.getText()
                    i = txt.rfind( '\n', 0, pos )
                    if i == -1: i = 0
                    else: i += 1
                    
                    i2 = txt.find( '\n', pos )
                    if i2 == -1: i2 = len( txt )
                    
                    line = txt[ i: i2 ]
                    language = self.emacs.determineLanguage()
                    delim1,delim2, delim3 = g.set_delims_from_language( language )
                    
                    where = line.find( delim1 )
                    if where == -1: return "No comment found"
                    
                    else:
                        nline = line[ :where ]
                        
                        sdoc = editor.getStyledDocument()
                        sdoc.replace( i, len( line ), nline, None )
                        if ( pos - i ) < where: editor.setCaretPosition( pos )
                        return
            #@nonl
            #@-node:ekr.20050723062822.116:comment-kill
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.114:comment
        #@+node:ekr.20050723062822.117:movement
        class movement:
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.commands = {
                    'Alt+Shift Comma': self.beginningOfBuffer,
                    'Alt+Shift Period': self.endOfBuffer,
                    'Ctrl A': self.beginningOfLine,
                    'Ctrl E': self.endOfLine,
                    'Ctrl Left': self.startOfWord,
                    'Ctrl Right': self.endOfWord,
                    'goto-line': self.goto,
                    'goto-char': self.gotoChar,
                    'Alt M': self.moveToIndentStart
                }
                self.mode = None
                self.emacs.modeStrategies.append ( self )
                
            def __call__( self, event, command ):
                
                if self.mode:
                    if command == 'Enter':
                        if self.mode == 1:
                            message = self.goto()
                        else:
                            message = self.gotoChar()
                            
                        if message:
                            self.emacs.keyboardQuit( event )
                            self.emacs.setCommandText( message )
                            self.emacs.beep()
                            return True
                        else:
                            return self.emacs.keyboardQuit( event )
                        
                    else:
                        return self.emacs.eventToMinibuffer( event )
                self.commands[ command ]()
                return True
                
            #@    @+others
            #@+node:ekr.20050723062822.118:beginning-of-buffer
            def beginningOfBuffer( self ):
            
                editor = self.emacs.editor
                editor.setCaretPosition( 0 )
            #@nonl
            #@-node:ekr.20050723062822.118:beginning-of-buffer
            #@+node:ekr.20050723062822.119:end-of-buffer
            def endOfBuffer( self ):
                
                editor = self.emacs.editor
                sdoc = editor.getStyledDocument()
                editor.setCaretPosition( sdoc.getLength() -1 )
            #@nonl
            #@-node:ekr.20050723062822.119:end-of-buffer
            #@+node:ekr.20050723062822.120:beginning-of-line
            def beginningOfLine( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != -1:
                    
                    txt = editor.getText()
                    where = txt.rfind( '\n', 0, pos )
                    if where == -1: where = 0
                    else: where +=1
                    #print stext.Utilities.getRowStart( editor, pos )
                    #print where
                    spot = stext.Utilities.getRowStart( editor, pos )
                    editor.setCaretPosition( spot )
                    
                    #editor.setCaretPosition( where )
            #@nonl
            #@-node:ekr.20050723062822.120:beginning-of-line
            #@+node:ekr.20050723062822.121:end-of-line
            def endOfLine( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != -1:
                    
                    txt = editor.getText()
                    where = txt.find( '\n', pos )
                    if where == -1: where = len( txt )
                    #elif where != 0:
                    #    where -= 1
                    #print stext.Utilities.getRowEnd( editor, pos )
                    #print where
                    spot = stext.Utilities.getRowEnd( editor, pos )
                    editor.setCaretPosition( spot )
                    
                    #editor.setCaretPosition( where )
            #@nonl
            #@-node:ekr.20050723062822.121:end-of-line
            #@+node:ekr.20050723062822.122:goto
            def goto( self ):
                
                if self.mode == None:
                    self.mode = 1
                    self.emacs._stateManager.setState( 'movement' )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs.setCommandText( "Goto Line:" )
                    return True
                    
                    
                    
                line = self.emacs.minibuffer.getText()
                if not line.isdigit(): 
                    return "Is Not a Number"
                   
                line = int( line )
                editor = self.emacs.editor
                
                txt = editor.getText()
                txtlines = txt.splitlines( True )
                if len( txtlines ) < line:
                    editor.setCaretPosition( len( txt ) )
                else:
                    txtlines = txtlines[ : line ]
                    length =  len( ''.join( txtlines ) )
                    editor.setCaretPosition( length - len( txtlines[ -1 ] ) )
            #@nonl
            #@-node:ekr.20050723062822.122:goto
            #@+node:ekr.20050723062822.123:gotoChar
            def gotoChar( self ):
                
                if self.mode == None:
                    self.mode = 2
                    self.emacs._stateManager.setState( 'movement' )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs.setCommandText( "Goto Char:" )
                    return True
                    
                line = self.emacs.minibuffer.getText()
                if not line.isdigit(): 
                    return "Is Not a Number"
                    
                    
                number = int( line )
                editor = self.emacs.editor
                ltxt = len( editor.getText() )
                if ltxt < number:
                    editor.setCaretPosition( ltxt )
                else:
                    editor.setCaretPosition( number )
            #@nonl
            #@-node:ekr.20050723062822.123:gotoChar
            #@+node:ekr.20050723062822.124:startOfWord
            def startOfWord( self):
                
                doc = self.emacs.editor.getDocument()
                cpos = self.emacs.editor.getCaretPosition()
                txt = doc.getText( 0, cpos )
                txt = list( txt)
                txt.reverse()
                if len( txt) == 0: return
                i = 0
                if not self.isWordCharacter( txt[ 0 ]):
                    for z in txt:
                        if not self.isWordCharacter( z ):
                            i += 1
                        else:
                            break
                
                for z in txt[ i: ]:
                    if not self.isWordCharacter( z ):
                        break
                    else:
                        i += 1
            
                cpos -= i
                self.emacs.editor.setCaretPosition( cpos )
            #@nonl
            #@-node:ekr.20050723062822.124:startOfWord
            #@+node:ekr.20050723062822.125:endOfWord
            def endOfWord( self ):
                
                doc = self.emacs.editor.getDocument()
                cpos = self.emacs.editor.getCaretPosition()
                txt = doc.getText( cpos, doc.getLength() - cpos )
                txt = list( txt)
                #txt.reverse()
                if len( txt) == 0: return
                i = 0
                if not self.isWordCharacter( txt[ 0 ]):
                    for z in txt:
                        if not self.isWordCharacter( z ):
                            i += 1
                        else:
                            break
                
                for z in txt[ i: ]:
                    if not self.isWordCharacter( z ):
                        break
                    else:
                        i += 1
            
                cpos += i
                self.emacs.editor.setCaretPosition( cpos )
            #@nonl
            #@-node:ekr.20050723062822.125:endOfWord
            #@+node:ekr.20050723062822.126:beginning of indentation
            def moveToIndentStart( self ):
            
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != -1:
                    
                    #txt = editor.getText()
                    start = stext.Utilities.getRowStart( editor, pos )
                    end = stext.Utilities.getRowEnd( editor, pos )
                    doc = editor.getDocument()
                    txt = doc.getText( start, end - start )
                    add = 0
                    for z in txt:
                        if not z.isspace():
                            break
                        else:
                            add +=1
                                    
                    editor.setCaretPosition( start + add )
            #@nonl
            #@-node:ekr.20050723062822.126:beginning of indentation
            #@+node:ekr.20050723062822.127:isWord
            def isWordCharacter( self, c ):
                
                if c in string.ascii_letters:
                    return True
                elif c in string.digits:
                    return True
                elif c in ( "_"):
                    return True
                return False
            #@nonl
            #@-node:ekr.20050723062822.127:isWord
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.117:movement
        #@+node:ekr.20050723062822.128:balanced parenthesis or sexp
        class balanced_parentheses:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.sexps = {
                
                    '(': ')',
                    ')':'(',
                    '[':']',
                    ']':'[',
                    '<':'>',
                    '>':'<',
                    '{':'}',
                    '}':'{',
                }
                
                self.forwards = ( "(", "<", "{", "[" )
                self.backwards = ( ")", ">", "}", "]" )
                
                self.commands = {
                    'Ctrl+Alt F': self.forwardSexp,
                    'Ctrl+Alt B': self.backwardSexp,
                    'Ctrl+Alt K': self.killSexpForward,
                    'Ctrl+Alt Delete': self.killSexpBackward,
                }
                
            def __call__( self, event , command ):
                
                self.commands[ command ]()
                return True
        
            def forwardSexp( self ):
                
                editor = self.emacs.editor
                doc = editor.getDocument()
                cp = editor.getCaretPosition()
                if cp + 1 == doc.getLength(): return
                txt = doc.getText( cp, doc.getLength() - cp )
                sp = txt[ 0 ]
                if sp not in self.forwards or len( txt ) == 1: return
                matcher = self.sexps[ sp ]
                i = 1
                i2 = 0
                for z in txt[ 1: ]:
                    i2 += 1
                    if z == sp:
                        i += 1
                        continue
                    elif z == matcher:
                        i -= 1
                    if i == 0: break
                if i == 0:
                    editor.setCaretPosition( cp + i2 )
            
            def backwardSexp( self ):
                
                editor = self.emacs.editor
                doc = editor.getDocument()
                cp = editor.getCaretPosition()
                txt = doc.getText( 0, cp + 1 )
                sexp = txt[ -1 ]
                if sexp not in self.backwards or len( txt ) == 1: return
                matcher = self.sexps[ sexp ]
                i = 1
                i2 = 0
                t2 = list( txt )
                t2.reverse()
                for z in t2[ 1: ]:
                    i2 += 1
                    if z == sexp:
                        i += 1
                        continue
                    elif z == matcher:
                        i -= 1
                    if i == 0:
                        break
                
                if i == 0:
                    editor.setCaretPosition( cp - i2 )
         
            #@    @+others
            #@+node:ekr.20050723062822.129:killSexpForward and Backward
            def killSexpForward( self ):
                
                editor = self.emacs.editor
                doc = editor.getDocument()
                cp = editor.getCaretPosition()
                self.forwardSexp()
                cp2 = editor.getCaretPosition()
                if cp != cp2:
                    txt = doc.getText( cp, ( cp2 - cp ) + 1 )
                    self.emacs.addToKillbuffer( txt )
                    doc.remove( cp, ( cp2 - cp ) + 1)
                    
            def killSexpBackward( self ):
                
                editor = self.emacs.editor
                doc = editor.getDocument()
                cp = editor.getCaretPosition()
                self.backwardSexp()
                cp2 = editor.getCaretPosition()
                if cp != cp2:
                    txt = doc.getText( cp2, ( cp - cp2 ) + 1)
                    self.emacs.addToKillbuffer( txt )
                    doc.remove( cp2, ( cp - cp2 ) + 1)
            #@nonl
            #@-node:ekr.20050723062822.129:killSexpForward and Backward
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.128:balanced parenthesis or sexp
        #@+node:ekr.20050723062822.130:tags ( java.lang.Runnable )
        class tags: ## ( java.lang.Runnable ):
            
            #tags_table = {}
                
            #@    @+others
            #@+node:ekr.20050723062822.131: ctor
            def __init__( self, emacs ):
                
                self.emacs = emacs
                #self.emacs.c.frame.tree.jtree.addTreeSelectionListener( self )
                self.last_tag = None
                self.pop_back = []
                self.positions = []
                self.tag_table = {}
                self.last_command = None
                self.__defineLanguageRecognizers()
                self.__defineLanguageMatchers()
                ### self.xs = java.util.concurrent.Executors.newSingleThreadScheduledExecutor()
                self.xs = None
            
                leoPlugins.registerHandler( "select1", self.valueChanged )
                self.mode = None
                emacs.modeStrategies.append( self )
                self.commands = {
                    'Alt Period': self.gotoTag,
                    'Ctrl U Alt Period': self.alternativeDefinition,
                    'Alt+Shift 8': self.popBack,
                }
                self.tab_completer = self.emacs.TabCompleter( [] )
                ### dc = DefCallable( self.defineTagsTable )
                ### g.app.gui.addStartupTask( dc )
            #@nonl
            #@-node:ekr.20050723062822.131: ctor
            #@+node:ekr.20050723062822.132:__call__
            def __call__( self, event, command ):
                
                if self.mode:
                    if command == 'Enter':
                        self.gotoTag()
                        return self.emacs.keyboardQuit( event )
                    elif command == 'Tab':
                    
                        txt = self.emacs.minibuffer.getText()
                        if self.last_command == None or not txt.startswith( self.last_command ):
                            txt = self.emacs.minibuffer.getText()                
                            fnd = self.tab_completer.lookFor( txt )
                            if fnd:
                                self.last_command = txt
                                self.emacs.minibuffer.setText( self.tab_completer.getNext() )
                        else :
                            self.emacs.minibuffer.setText( self.tab_completer.getNext() )
                        return True
                    else:
                        return self.emacs.eventToMinibuffer( event )   
                
                rv = self.commands[ command ]()
                self.tab_completer.reset()
                self.last_command = None
                if rv:
                    self.emacs.keyboardQuit( event )
                return True
            #@nonl
            #@-node:ekr.20050723062822.132:__call__
            #@+node:ekr.20050723062822.133:__defineLanguageMatchers
            def __defineLanguageMatchers( self ):
            
                if 1:  ### Not ready yet.
                    pass
                else:
                    reg1 = java.util.regex.Pattern.compile( java.lang.String( "^\s*(def\s+\w+\s*)" ) )
                    reg2 = java.util.regex.Pattern.compile( java.lang.String(  "^\s*(class\s+\w+\s*)" ) )
                    self.python_matchers = ( reg1.matcher( java.lang.String( "" ) ), reg2.matcher( java.lang.String( "" ) ) )
            #@nonl
            #@-node:ekr.20050723062822.133:__defineLanguageMatchers
            #@+node:ekr.20050723062822.134:__defineLanguageRecognizers
            def __defineLanguageRecognizers( self ):
                
                if 1: ### Not ready yet.
                    pass
            
                else:
                    sstring = java.lang.String( "" )
                    pattern = regex.Pattern.compile( "(class|interface)\s*(\w+)" )
                    self.java_class = pattern.matcher( sstring )
                    pattern = regex.Pattern.compile( "((public|private|protected)\s+)?(final\s+)?(static\s+)?(new\s+){0}\w+\s*(\w+)\s*\\(" )
                    self.java_method = pattern.matcher( sstring )
            #@nonl
            #@-node:ekr.20050723062822.134:__defineLanguageRecognizers
            #@+node:ekr.20050723062822.135:alternativeDefinition
            def alternativeDefinition( self ):
                
                if self.last_tag:
                    
                    tag , td = self.last_tag
                    tags = self.tag_table[ tag ]
                    i = tags.index( td )
                    if i + 1 == len( tags ):
                        i = 0
                    else:
                        i += 1
                    
                    td = tags[ i ]
                    self.last_tag = ( tag, td )
                    p = td[ -1 ]
                    c = self.emacs.c
                    cp = c.currentPosition()
                    self.pop_back.append( cp.copy() )
                    c.beginUpdate()
                    c.selectPosition( p.copy() )
                    c.endUpdate()
                    dgl = self.DeferedGotoLine( self.emacs.c, p, td[ 0 ] )
                    dc = DefCallable( dgl )
                    ft = dc.wrappedAsFutureTask()
                    java.awt.EventQueue.invokeLater( ft )
                    #self.emacs.keyboardQuit( event )
                    return True
            #@nonl
            #@-node:ekr.20050723062822.135:alternativeDefinition
            #@+node:ekr.20050723062822.136:class DeferedGotoLine
            class DeferedGotoLine:
                
                def __init__( self, c, pos, tag ):
                    self.c = c
                    self.pos = pos
                    self.tag = tag
                    
                def __call__( self ):
                    
                    bs = self.pos.bodyString()
                    where = bs.find( self.tag )
                    if where != -1:
                        self.c.frame.body.editor.editor.setCaretPosition( where )
            #@nonl
            #@-node:ekr.20050723062822.136:class DeferedGotoLine
            #@+node:ekr.20050723062822.137:defineTagsTable
            def defineTagsTable( self ):
            
                c = self.emacs.c
                cp = c.rootPosition()
                for z in cp.allNodes_iter( copy = True ):
                    tags = self.scanForTags( z )
                    if tags:
                        for x in tags:
                            if self.tag_table.has_key( x[ 1 ] ):
                                self.tag_table[ x[ 1 ] ].append( x )
                            else:                    
                                self.tag_table[ x[ 1 ] ] = []
                                self.tag_table[ x[ 1 ] ].append( x )
                                
                self.tab_completer.extend( self.tag_table.keys() ) 
                g.es( "tag table built" )
                self.xs.scheduleAtFixedRate( self, 30000, 30000, java.util.concurrent.TimeUnit.MILLISECONDS )
            #@nonl
            #@-node:ekr.20050723062822.137:defineTagsTable
            #@+node:ekr.20050723062822.138:gotoTag
            def gotoTag( self ):
                
                if self.mode == None:
                    self.emacs.setCommandText( "Goto tag:" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "tags" )    
                    self.mode = 1
                    return
                    
                if self.mode == 1:
                    
                    tag = self.emacs.minibuffer.getText()
                    if not tag:
                        wsi = self.emacs.getWordStartIndex()
                        wse = self.emacs.getWordEndIndex()
                        tag = self.emacs.getTextSlice( wsi, wse )
                    if tag in self.tag_table:
                        td = self.tag_table[ tag ]
                        self.last_tag = ( tag, td[ 0 ] )
                        p = td[ 0 ][ -1 ]
                        c = self.emacs.c
                        cp = c.currentPosition()
                        self.pop_back.append( cp.copy() )
                        c.beginUpdate()
                        c.selectPosition( p.copy() )
                        c.endUpdate()
                        dgl = self.DeferedGotoLine( self.emacs.c, p, td[ 0 ][ 0 ] )
                        dc = DefCallable( dgl )
                        ft = dc.wrappedAsFutureTask()
                        java.awt.EventQueue.invokeLater( ft )
                        #self.emacs.keyboardQuit( event )
                        return True
                    else:
                        g.es( "Could not find definition for %s" % tag )
                        #self.emacs.keyboardQuit( event)
                        return True
            #@nonl
            #@-node:ekr.20050723062822.138:gotoTag
            #@+node:ekr.20050723062822.139:popBack
            def popBack( self ):
            
                if self.pop_back:
                    p = self.pop_back.pop()
                    c = self.emacs.c
                    c.beginUpdate()
                    c.selectPosition( p )
                    c.endUpdate()
            #@nonl
            #@-node:ekr.20050723062822.139:popBack
            #@+node:ekr.20050723062822.140:run
            def run( self ):
                
                cp = self.emacs.c.currentPosition().copy()
                if cp not in self.positions:
                    self.positions.append( cp )
                    
                for z in self.positions:
                    tags = self.scanForTags( z )
                    if tags:
                        for x in tags:   
                            if self.tag_table.has_key( x[ 1 ] ):
                                self.tag_table[ x[ 1 ] ].append( x ) 
                            else:
                                self.tag_table[ x[ 1 ] ] = []
                                self.tag_table[ x[ 1 ] ].append( x )
                            self.tab_completer.extend( x[ 1 ] )
                                
                self.positions = []
            #@nonl
            #@-node:ekr.20050723062822.140:run
            #@+node:ekr.20050723062822.141:scanForTags
            def scanForTags( self, p ):
                #print "SCANNING FOR TAGS!"
                #language = g.scanForAtLanguage( self.emacs.c, p )
                language = LeoUtilities.scanForLanguage( p )
                if language == None: language = 'python'
                if language == 'python':
                    tags = []
                    try:
                        #reg1 = "^\s*(def\s+\w+\s*)"
                        #reg2 = "^\s*(class\s+\w+\s*)"
                        #regs = ( reg1, reg2 )
                        tnt = p.v.t._bodyString
                        matches = LeoUtilities.scanFor( self.python_matchers , tnt )
                        #print matches
                        for z in matches:
                            tags.append( ( z[ 0 ], z[ 1 ], p ) )
                        #bs = p.bodyString()
                        #data = bs.split( '\n' )
                        # tags = []
                        #for z in data:
                        #    txt = z.lstrip()
                        #    txtpieces = txt.split()
                        #    if len( txtpieces )> 1 and txtpieces[ 0 ] in ( "class", "def" ):
                        #        ntxt = txtpieces[ 1 ]
                        #        i1 = ntxt.find( "(" )
                        #        i2 = ntxt.find( ":" )
                        #        if i1 != -1: 
                        #            ntxt = ntxt[ : i1 ]
                        #        elif i2 != -1:
                        #            ntxt = ntxt[ : i2 ]
                        #        
                        #        tags.append( ( txt, ntxt, p ) )
                    except Exception, x:
                        print x
                    except java.lang.Exception, r:
                        print r            
                         
                    return tags
                elif language == 'java':
                    #@        <<java>>
                    #@+node:ekr.20050723062822.142:<<java>>
                    bs = p.bodyString()
                    data = bs.split( '\n' )
                    tags = []
                    for z in data:
                        #regex looking for methods
                        #regular scan for looking for class and interface
                        #class interface takes precedence over methods
                        try:
                            stxt = z.lstrip()
                            txt = java.lang.String( stxt )
                            self.java_class.reset( txt )
                            self.java_method.reset( txt )
                            start = end = -1
                            if self.java_class.find():
                                gc = self.java_class.groupCount()
                                ntxt = self.java_class.group( gc )
                            elif self.java_method.find():
                                gc = self.java_method.groupCount()
                                ntxt = self.java_method.group( gc )
                            else:
                                gc = 0
                            
                            if gc:
                                tags.append( (stxt, ntxt, p ) ) 
                        except Exception, x:
                            print x
                    
                    
                    return tags
                    #@nonl
                    #@-node:ekr.20050723062822.142:<<java>>
                    #@nl
                else:
                    return None
            #@nonl
            #@-node:ekr.20050723062822.141:scanForTags
            #@+node:ekr.20050723062822.143:valueChanged
            def valueChanged( self, *args ):
                
                values = args[ 1 ]
                self.positions.append( values[ 'new_p' ].copy() )
            #@nonl
            #@-node:ekr.20050723062822.143:valueChanged
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.130:tags ( java.lang.Runnable )
        #@+node:ekr.20050723062822.144:transpose
        class transpose:
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.commands = {
                    'transpose-lines': self.transposeLines,
                    'reverse-region': self.reverseRegion,
                    'Alt T': self.transposeWords,
                }
                
            def __call__( self, event, command ):
                
            
                if not self.commands[ command ]():
                    return self.emacs.keyboardQuit( event )  
                return True
                
                
            #@    @+others
            #@+node:ekr.20050723062822.145:transpose-lines
            def transposeLines( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != -1:
                    
                    txt = editor.getText()
                    start = txt.rfind( '\n', 0, pos )
                    if start == -1: start = 0
                    else:
                        if start != 0:
                            start = txt.rfind( '\n', 0, start )
                            if start == -1: start = 0
                            else: 
                                start += 1
                    
                    end = txt.find( '\n', pos )
                    if end == -1: end = len( txt )
                       
                
                    lines = txt[ start: end ]
                    lines_split = lines.split( '\n' )
                    if not len( lines_split ) == 2: return
                    l1, l2 = lines_split[ 0 ], lines_split[ 1 ]
                    
                    nwlines = '%s\n%s' %( l2, l1 )
                    sdoc = editor.getStyledDocument()
                    sdoc.replace( start, len( lines ), nwlines, None )
            #@nonl
            #@-node:ekr.20050723062822.145:transpose-lines
            #@+node:ekr.20050723062822.146:reverse-region
            def reverseRegion( self ):
                
                editor = self.emacs.editor
                txt = editor.getSelectedText()
                if txt == None: return
                txtlines = txt.splitlines( True )
                txtlines.reverse()
                if not txt.endswith( '\n' ):
                    txtlines[ 0 ] = '%s\n' % txtlines[ 0 ]
                ntxt = ''.join( txtlines )
                editor.replaceSelection( ntxt )
            #@nonl
            #@-node:ekr.20050723062822.146:reverse-region
            #@+node:ekr.20050723062822.147:transpose-words
            def transposeWords( self ):
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                if pos != -1:
                    
                    ranges = self.emacs.getAttributeRanges( "trans-word" )
                    if ranges:
                        start = self.emacs.getWordStartIndex()
                        end = self.emacs.getWordEndIndex()
                        doc = editor.getDocument()
                        w1 = doc.getText( start, end - start )
                        w2 = doc.getText( ranges[ 0 ], ranges[ -1 ] - ranges[ 0 ] )
                        doc.replace( ranges[ 0 ], ranges[ -1 ] - ranges[ 0 ], w1, None )
                        start = self.emacs.getWordStartIndex()
                        end = self.emacs.getWordEndIndex()
                        doc.replace( start, end - start, w2, None )
                        self.emacs.clearAttribute( "trans-word" )
                        return
                    
                    else:
                        start = self.emacs.getWordStartIndex()
                        end = self.emacs.getWordEndIndex()
                        self.emacs.addAttributeToRange( 'trans-word', "trans-word" , start, end-start, color = java.awt.Color.YELLOW )
            
                    return True
            #@nonl
            #@-node:ekr.20050723062822.147:transpose-words
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.144:transpose
        #@+node:ekr.20050723062822.148:capitalization
        class capitalization:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.commands ={
                    'capitalize-region': self.capitalizeRegion,
                    'upcase-region': self.upcaseRegion,
                    'downcase-region': self.downcaseRegion,
                    'capitalize-word': self.capitalizeWord,
                    'downcase-word': self.downcaseWord,
                    'upcase-word': self.upcaseWord,
                }
                
            def __call__( self, event, command ):
                
                message = self.commands[ command ]()
                if message:
                    self.emacs.keyboardQuit( event )
                    self.emacs.setCommandText( message )
                    self.emacs.beep()
                    return True
                    
                return self.emacs.keyboardQuit( event )
        
            #@    @+others
            #@+node:ekr.20050723062822.149:capitalize-region
            def capitalizeRegion( self ):
            
                editor = self.emacs.editor
                stext = editor.getSelectedText()
                if stext == None:
                    return "Region not selected"
                    
                ntext = []
                lc = ' '
                for z in stext:
                    if lc.isspace():
                        z2 = z.capitalize()
                        ntext.append( z2 )
                    else:
                        ntext.append( z )
                    lc = z
                    
                ntext = ''.join( ntext )
                editor.replaceSelection( ntext )
            #@nonl
            #@-node:ekr.20050723062822.149:capitalize-region
            #@+node:ekr.20050723062822.150:upcase-region
            def upcaseRegion( self ):
                
                editor = self.emacs.editor
                stext = editor.getSelectedText()
                if stext == None:
                    return "Region not selected"
                    
                ntext = stext.upper()
                editor.replaceSelection( ntext )
            #@nonl
            #@-node:ekr.20050723062822.150:upcase-region
            #@+node:ekr.20050723062822.151:downcase-region
            def downcaseRegion( self ):
            
                editor = self.emacs.editor
                stext = editor.getSelectedText()
                if stext == None:
                    return "Region not selected"
                    
                ntext = stext.lower()
                editor.replaceSelection( ntext )
            #@nonl
            #@-node:ekr.20050723062822.151:downcase-region
            #@+node:ekr.20050723062822.152:capitalize-word
            def capitalizeWord( self ):
                
                start, end = self.emacs.getWordStartIndex(), self.emacs.getWordEndIndex()
                
                if start != -1:
                    
                    sdoc = self.emacs.editor.getStyledDocument()
                    txt = sdoc.getText( start, end - start )
                    txt = txt.capitalize()
                    pos = self.emacs.editor.getCaretPosition()
                    sdoc.replace( start, len( txt ), txt, None )  
                    self.emacs.editor.setCaretPosition( pos )
            #@nonl
            #@-node:ekr.20050723062822.152:capitalize-word
            #@+node:ekr.20050723062822.153:upcase-word
            def upcaseWord( self ):
                
                start, end = self.emacs.getWordStartIndex(), self.emacs.getWordEndIndex()
                
                if start != -1:
                    
                    sdoc = self.emacs.editor.getStyledDocument()
                    txt = sdoc.getText( start, end - start )
                    txt = txt.upper()
                    pos = self.emacs.editor.getCaretPosition()
                    sdoc.replace( start, len( txt ), txt, None )
                    self.emacs.editor.setCaretPosition( pos )
            #@nonl
            #@-node:ekr.20050723062822.153:upcase-word
            #@+node:ekr.20050723062822.154:downcase-word
            def downcaseWord( self ):
            
                start, end = self.emacs.getWordStartIndex(), self.emacs.getWordEndIndex()
                
                if start != -1:
                    sdoc = self.emacs.editor.getStyledDocument()
                    txt = sdoc.getText( start, end - start )
                    txt = txt.lower()
                    pos = self.emacs.editor.getCaretPosition()
                    sdoc.replace( start, len( txt ), txt, None )
                    self.emacs.editor.setCaretPosition( pos )
            #@nonl
            #@-node:ekr.20050723062822.154:downcase-word
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.148:capitalization
        #@+node:ekr.20050723062822.155:replacement
        class replacement:
            ## import java.util.regex as regex
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.commands = {
                    'query-replace': self.queryReplace,
                    'query-replace-regexp': self.queryReplaceRegexp,
                    'replace-string': self.replaceString,
                }
        
                self.mode = None
                self.submode = None
                
                self.search = None
                self.replacement = None
                
                emacs.modeStrategies.append( self )
                
                
            def __call__( self, event, command ):
                
                if self.mode:
                    if self.mode in( 1, 2 ):
                        qcommand = g.choose( self.mode == 1, self.queryReplace, self.queryReplaceRegexp )
                        if self.submode in( 1, 2 ):
                            if command == 'Enter':
                                return qcommand()
                            else:
                                return self.emacs.eventToMinibuffer( event )   
                        if self.submode == 3:
                            message = self.doReplacement( event )
                            if message == None:
                                message = qcommand()
                            if message not in( True, False ) and message:
                                self.emacs.keyboardQuit( event )
                                self.emacs.minibuffer.setText( "" )
                                self.emacs.setCommandText( message )
                                return True
                            return True
                    elif self.mode == 3:
                        if command == 'Enter':
                            message = self.replaceString()
                            if message not in ( True, False ) and message:
                                self.emacs.keyboardQuit( event )
                                self.emacs.minibuffer.setText( "" )
                                self.emacs.setCommandText( message )
                                return True
                            else: return True
                        else:
                            return self.emacs.eventToMinibuffer( event )
                
                return self.commands[ command ]()
                
                
            #@    @+others
            #@+node:ekr.20050723062822.156:query-replace
            def queryReplace( self ):
                
                if self.mode == None:
                    self.mode = 1
                    self.submode = 1
                    self.emacs.setCommandText( "Query For:" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "replacement" )
                    return True
                
                if self.submode == 1:
                    
                    self.search = self.emacs.minibuffer.getText()
                    self.emacs.minibuffer.setText( "" )
                    self.emacs.setCommandText( "Replace With:" )
                    self.submode = 2
                    return True
                    
                if self.submode == 2:
                    
                    self.replacement = self.emacs.minibuffer.getText()
                    self.emacs.minibuffer.setText( "" )
                    self.submode = 3
                    
                    
                if self.submode == 3:
                    
                    editor = self.emacs.editor
                    pos = editor.getCaretPosition()
                    txt = editor.getText()
                    where = txt.find( self.search, pos )
                    if where == -1:
                        editor.setCaretPosition( editor.getSelectionEnd() )
                        return "No more matches found"
                    else:
                        editor.setSelectionStart( where )
                        editor.setSelectionEnd( where + len( self.search ) )
                        self.emacs.setCommandText( "Replace %s with %s ? y/n(! replaces all)" %( self.search, self.replacement ) )
                        return True
            #@nonl
            #@-node:ekr.20050723062822.156:query-replace
            #@+node:ekr.20050723062822.157:query-replace-regexp
            def queryReplaceRegexp( self ):
                
                if self.mode == None:
                    self.mode = 2
                    self.submode = 1
                    self.emacs.setCommandText( "Query For:" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "replacement" )
                    return True
                
                if self.submode == 1:
                    search = self.emacs.minibuffer.getText()
                    ## import java.util.regex
                    self.search = java.util.regex.Pattern.compile( search )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs.setCommandText( "Replace With:" )
                    self.submode = 2
                    return True
                    
                if self.submode == 2:
                    self.replacement = self.emacs.minibuffer.getText()
                    self.emacs.minibuffer.setText( "" )
                    self.submode = 3
            
                if self.submode == 3:
                    editor = self.emacs.editor
                    pos = editor.getCaretPosition()
                    txt = editor.getText()
                    
                    ## import java.lang.String
                    match = self.search.matcher( java.lang.String( txt[ pos: ] ) )
                    found = match.find()
                    if found:
                        start = match.start()
                        end = match.end()
                    else:
                        start = end = -1
                    if start == -1:
                        editor.setCaretPosition( editor.getSelectionEnd() )
                        return "No more matches found"
                    else:
                        editor.setSelectionStart( pos + start )
                        editor.setSelectionEnd( pos + end )
                        self.emacs.setCommandText( "Replace %s with %s ? y/n(! replaces all)" %( editor.getSelectedText(), self.replacement ) )
                        return True
            #@nonl
            #@-node:ekr.20050723062822.157:query-replace-regexp
            #@+node:ekr.20050723062822.158:replace-string
            def replaceString( self ):
            
                if self.mode == None:
                    self.mode = 3
                    self.submode = 1
                    self.emacs.setCommandText( "Replace String:" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "replacement" )
                    return True
                
                if self.submode == 1:
                    
                    self.search = self.emacs.minibuffer.getText()
                    self.emacs.minibuffer.setText( "" )
                    self.emacs.setCommandText( "Replace %s With:" % self.search )
                    self.submode = 2
                    return True    
                    
                if self.submode == 2:
                    
                    replacement = self.emacs.minibuffer.getText()
                    editor = self.emacs.editor
                    pos = editor.getCaretPosition()
                    txt = editor.getText()[ pos: ]
                    amount = txt.count( self.search )
                    ntxt = txt.replace( self.search, replacement )
                    sd = editor.getStyledDocument()
                    sd.replace( pos, len( txt ), ntxt, None )
                    editor.setCaretPosition( pos )
                    return "%s occurances of %s replaced with %s" %( amount, self.search, replacement )
            #@nonl
            #@-node:ekr.20050723062822.158:replace-string
            #@+node:ekr.20050723062822.159:doReplacement
            def doReplacement( self, event ):
                
                
                kc = event.getKeyChar()
                
                if not java.lang.Character.isDefined( kc ): return False
                elif kc == 'y':
                    self.emacs.editor.replaceSelection( self.replacement )
                    
                elif kc =='!':
                    return self.replaceAll()
                    
                else:
                    pass
            #@nonl
            #@-node:ekr.20050723062822.159:doReplacement
            #@+node:ekr.20050723062822.160:replaceAll
            def replaceAll( self ):
                
                editor = self.emacs.editor
                spos = editor.getSelectionStart()
                editor.setCaretPosition( spos )
                cp = editor.getCaretPosition()
                txt = editor.getText()[ cp : ]
                sd = editor.getStyledDocument()
                
                if self.mode == 1:
                    amount = txt.count( self.search )
                    ntxt = txt.replace( self.search, self.replacement )
                    sd.replace( cp, len( txt ), ntxt, None )
                    editor.setCaretPosition( spos )
                    return '%s instances of %s replaced with %s' %( amount, self.search, self.replacement )
                else:
                    ## import java.lang.String
                    txt_s = java.lang.String( txt )
                    scount = txt.count( self.replacement )
                    #natxt = self.search.split( txt_s )
                    #print "natxt len is %s" % len( natxt )
                    matcher = self.search.matcher( txt_s )
                    ntxt = matcher.replaceAll( self.replacement )
                    ncount = ntxt.count( self.replacement )
                    #ntxt = self.replacement.join( natxt )
                    sd.replace( cp, len( txt ), ntxt, None )
                    editor.setCaretPosition( spos )
                    return '%s instances of %s replaced with %s' %( ncount - scount, self.search.pattern(), self.replacement )
            #@nonl
            #@-node:ekr.20050723062822.160:replaceAll
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.155:replacement
        #@+node:ekr.20050723062822.161:sorters
        class sorters:
            
            def __init__( self, emacs ):
                self.emacs = emacs
                self.commands ={
                'sort-lines': self.sortLines
                }
                
            def __call__( self, event, command ):
                
                self.commands[ command ]()
                return self.emacs.keyboardQuit( event )
                
            #@    @+others
            #@+node:ekr.20050723062822.162:sort-lines
            def sortLines( self ):
                
                editor = self.emacs.editor
                txt = editor.getSelectedText()
                if txt == None: return
                txtlines = txt.splitlines()
                txtlines.sort()
                ntxt = '\n'.join( txtlines )
                if txt[ -1 ] == '\n': ntxt = '%s\n' % ntxt
                editor.replaceSelection( ntxt )
            #@nonl
            #@-node:ekr.20050723062822.162:sort-lines
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.161:sorters
        #@+node:ekr.20050723062822.163:lines
        class lines:
            ## import java.util.regex as regexp
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.mode = None
                self.commands= {
                    'keep-lines': self.keepLines,
                    'flush-lines': self.flushLines,
                }
                emacs.modeStrategies.append( self )
                
            def __call__( self, event, command ):
                
                if self.mode:
                    if self.mode in ( 1, 2 ):
                        if command == 'Enter':
                            if self.mode == 1:
                                self.keepLines()
                            else:
                                self.flushLines()
                            self.emacs.keyboardQuit( event )
                            return True
                        else:
                            return self.emacs.eventToMinibuffer( event )
        
                return self.commands[ command ]()
                
            #@    @+others
            #@+node:ekr.20050723062822.164:keep-lines
            def keepLines( self ):
                ## import java.util.regex as regexp
                if self.mode == None:
                    self.mode = 1
                    self.emacs.setCommandText( "Keep lines( containing match for regexp ):" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "lines" )
                    return True
                
                pattern = self.emacs.minibuffer.getText()
                regex = regexp.Pattern.compile( java.lang.String( pattern ) )
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                txt = editor.getText()
                start = txt.rfind( '\n', 0, pos )
                if start == -1: start = 0
                else: start += 1
                
                
                ntxt = txt[ start: ]
                ntxt_lines = ntxt.splitlines( True )
            
                matcher = regex.matcher( java.lang.String( ntxt_lines[ 0 ] ) )
                keepers = []
                for z in ntxt_lines:
                    matcher.reset( java.lang.String( z ) )
                    found = matcher.find()
                    if found: keepers.append( z )
                    
                    
                keeptxt = ''.join( keepers )
                
                sdoc = editor.getStyledDocument()
                sdoc.replace( start, len( ntxt ), keeptxt, None )
                if ( sdoc.getLength() - 1 ) >= pos:
                    editor.setCaretPosition( pos )
            #@nonl
            #@-node:ekr.20050723062822.164:keep-lines
            #@+node:ekr.20050723062822.165:flush-lines
            def flushLines( self ):
            
                ## import java.util.regex as regexp
                if self.mode == None:
                    self.mode = 2
                    self.emacs.setCommandText( "Flush lines( containing match for regexp ):" )
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "lines" )
                    return True
            
                pattern = self.emacs.minibuffer.getText()
                regex = regexp.Pattern.compile( java.lang.String( pattern ) )
                
                editor = self.emacs.editor
                pos = editor.getCaretPosition()
                txt = editor.getText()
                start = txt.rfind( '\n', 0, pos )
                if start == -1: start = 0
                else: start += 1
            
                ntxt = txt[ start: ]
                ntxt_lines = ntxt.splitlines( True )
            
                matcher = regex.matcher( java.lang.String( ntxt_lines[ 0 ] ) )
                keepers = []
                for z in ntxt_lines:
                    matcher.reset( java.lang.String( z ) )
                    found = matcher.find()
                    if found: continue
                    keepers.append( z )
            
                keeptxt = ''.join( keepers )
                
                sdoc = editor.getStyledDocument()
                sdoc.replace( start, len( ntxt ), keeptxt, None )
                if ( sdoc.getLength() - 1 ) >= pos:
                    editor.setCaretPosition( pos )
            #@nonl
            #@-node:ekr.20050723062822.165:flush-lines
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.163:lines
        #@+node:ekr.20050723062822.166:tabs
        class tabs:
            
            def __init__( self, emacs ):
                
                self.emacs = emacs
                self.commands ={
                    'tabify': self.tabify,
                    'untabify': self.untabify,
                }
                
            def __call__( self, event, command ):
        
                rval = self.commands[ command ]()
                self.emacs.keyboardQuit( event )
                return rval
                
            #@    @+others
            #@+node:ekr.20050723062822.167:tabify
            def tabify( self ):
            
                #tw = self.emacs.getTabWidth()
                editor = self.emacs.editor
                txt = editor.getSelectedText()
                if txt == None: return True
                
                #space_replace = ' ' * tw
                ntxt = txt.replace( ' ', '\t' )
                pos = editor.getCaretPosition()
                editor.replaceSelection( ntxt )
                editor.setCaretPosition( pos )
                return True
            #@nonl
            #@-node:ekr.20050723062822.167:tabify
            #@+node:ekr.20050723062822.168:untabify
            def untabify( self ):
                
                #tw = self.emacs.getTabWidth()
                editor = self.emacs.editor
                txt = editor.getSelectedText()
                if txt == None: return True
                
                #space_replace = ' ' * tw
                ntxt = txt.replace( '\t', ' ' )
                pos = editor.getCaretPosition()
                editor.replaceSelection( ntxt )
                editor.setCaretPosition( pos )
                return True
            #@nonl
            #@-node:ekr.20050723062822.168:untabify
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.166:tabs
        #@+node:ekr.20050723062822.169:registers
        class registers:
            
            #@    @+others
            #@+node:ekr.20050723062822.170:ctor
            def __init__( self, emacs ):
                    
                self.emacs = emacs
                self.mode = None
                self.submode = None
                emacs.modeStrategies.append( self )
                self.registers = {}
                self.commands = {
                    'copy-to-register': self.copyToRegister,
                    'insert-register': self.insertRegister,
                    'append-to-register': self.appendToRegister,
                    'prepend-to-register': self.prependToRegister,
                }
                self.mode_command ={
                    1: self.copyToRegister,
                    3: self.appendToRegister,
                    4: self.prependToRegister,
                }
            #@nonl
            #@-node:ekr.20050723062822.170:ctor
            #@+node:ekr.20050723062822.171:__call__
            def __call__( self, event, command ):
            
                if self.mode:
                    if self.mode in ( 1, 3, 4 ):
                        self.emacs.eventToMinibuffer( event )
                        message =   self.mode_command[ self.mode ]()           #self.copyToRegister()
                        if message not in ( True, False ) and message:
                            self.emacs.keyboardQuit( event )
                            self.emacs.setCommandText( message )
                            return True
                        else:
                            return self.emacs.keyboardQuit( event )
                    elif self.mode == 2:
                        self.emacs.eventToMinibuffer( event )
                        message = self.insertRegister()
                        if message not in( True, False ) and message:
                            self.emacs.keyboardQuit( event )
                            self.emacs.setCommandText( message )
                            return True
                        return self.emacs.keyboardQuit( event )
                
                return self.commands[ command ]()
                
            #@nonl
            #@-node:ekr.20050723062822.171:__call__
            #@+node:ekr.20050723062822.172:copy-to-register
            def copyToRegister( self ):
             
                if self.mode == None:
                    
                    self.mode = 1
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "registers" )
                    self.emacs.setCommandText( "Copy To Which Register( a-z )?" )
                    return True
                    
                    
                register = self.emacs.minibuffer.getText()
                self.emacs.minibuffer.setText( "" )
                if not java.lang.Character.isLetter( register ):
                    return 'Character is not a Letter'
                    
                register = register.lower()
                txt = self.emacs.editor.getSelectedText()
                if txt == None:
                    return 'Region not defined'
                    
                self.registers[ register ] = txt
                self.emacs.editor.setCaretPosition( self.emacs.editor.getCaretPosition() )
            #@nonl
            #@-node:ekr.20050723062822.172:copy-to-register
            #@+node:ekr.20050723062822.173:insert-register
            def insertRegister( self ):
             
                if self.mode == None:
                    
                    self.mode = 2
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "registers" )
                    self.emacs.setCommandText( "Insert From Which Register( a-z )?" )
                    return True
                    
                    
                
                
                register = self.emacs.minibuffer.getText()
                if not java.lang.Character.isLetter( register ):
                    return 'Character is not a Letter'
                    
                register = register.lower()
                if not self.registers.has_key( register ):
                    return 'Register %s empty' % register
                    
                data = self.registers[ register ]
                sdoc = self.emacs.editor.getStyledDocument()
                sdoc.insertString( self.emacs.editor.getCaretPosition(), data, None )
            #@nonl
            #@-node:ekr.20050723062822.173:insert-register
            #@+node:ekr.20050723062822.174:append-to-register
            def appendToRegister( self ):
            
                if self.mode == None:
                    
                    self.mode = 3
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "registers" )
                    self.emacs.setCommandText( "Append To Which Register( a-z )?" )
                    return True
                    
                    
                register = self.emacs.minibuffer.getText()
                self.emacs.minibuffer.setText( "" )
                if not java.lang.Character.isLetter( register ):
                    return 'Character is not a Letter'
                    
                register = register.lower()
                txt = self.emacs.editor.getSelectedText()
                if txt == None:
                    return 'Region not defined'
                    
                if self.registers.has_key( register ):
                    data = self.registers[ register ]
                    ndata = '%s%s' %( data, txt )
                    self.registers[ register ] = ndata
                else:
                    self.registers[ register ] = txt
                    
                self.emacs.editor.setCaretPosition( self.emacs.editor.getCaretPosition() )
            #@nonl
            #@-node:ekr.20050723062822.174:append-to-register
            #@+node:ekr.20050723062822.175:prepend-to-register
            def prependToRegister( self ):
            
                if self.mode == None:
                    
                    self.mode = 4
                    self.emacs.minibuffer.setText( "" )
                    self.emacs._stateManager.setState( "registers" )
                    self.emacs.setCommandText( "Prepend To Which Register( a-z )?" )
                    return True
                    
                    
                register = self.emacs.minibuffer.getText()
                self.emacs.minibuffer.setText( "" )
                if not java.lang.Character.isLetter( register ):
                    return 'Character is not a Letter'
                    
                register = register.lower()
                txt = self.emacs.editor.getSelectedText()
                if txt == None:
                    return 'Region not defined'
                    
                if self.registers.has_key( register ):
                    data = self.registers[ register ]
                    ndata = '%s%s' %( txt, data )
                    self.registers[ register ] = ndata
                else:
                    self.registers[ register ] = txt
                    
                self.emacs.editor.setCaretPosition( self.emacs.editor.getCaretPosition() )
            #@nonl
            #@-node:ekr.20050723062822.175:prepend-to-register
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.169:registers
        #@+node:ekr.20050723062822.176:selection (sevent.DocumentListener)
        class selection: ## ( sevent.DocumentListener ):
            
            #@    @+others
            #@+node:ekr.20050723062822.177:ctor & __call__
            def __init__( self, emacs ):
                
                self.emacs = emacs
                ### self.emacs.editor.getDocument().addDocumentListener( self )
                self.start = None
                self.commands = {
                    "Ctrl Space": self.startSelection,       
                }
            
            def __call__( self, event, command ):
                if self.commands.has_key( command ):
                    return self.commands[ command ]()
                elif self.emacs._stateManager2.hasState() == "selection":
                    self.select()
            #@nonl
            #@-node:ekr.20050723062822.177:ctor & __call__
            #@+node:ekr.20050723062822.178:startSelection
            def startSelection( self ):
                
                self.start = self.emacs.editor.getCaretPosition()
                self.emacs._stateManager2.setState( "selection" )
                return True
            #@nonl
            #@-node:ekr.20050723062822.178:startSelection
            #@+node:ekr.20050723062822.179:executeSelection
            def executeSelection( self ):
            
                if self.start != -1:
                    editor = self.emacs.editor
                    cp = editor.getCaretPosition()
                    editor.setCaretPosition( self.start )
                    editor.moveCaretPosition( cp )
                else:
                    self.emacs.keyboardQuit()
            #@nonl
            #@-node:ekr.20050723062822.179:executeSelection
            #@+node:ekr.20050723062822.180:select
            def select( self ):
                        
                dc = DefCallable( self.executeSelection )
                ft = dc.wrappedAsFutureTask()
                java.awt.EventQueue.invokeLater( ft )
            #@nonl
            #@-node:ekr.20050723062822.180:select
            #@+node:ekr.20050723062822.181:changedUpdate
            def changedUpdate( self, event ):
                pass
            #@-node:ekr.20050723062822.181:changedUpdate
            #@+node:ekr.20050723062822.182:insertUpdate
            def insertUpdate( self, event ):
                pass
            #@-node:ekr.20050723062822.182:insertUpdate
            #@+node:ekr.20050723062822.183:removeUpdate
            def removeUpdate( self, event ):
                self.start = -1
            #@nonl
            #@-node:ekr.20050723062822.183:removeUpdate
            #@-others
        #@nonl
        #@-node:ekr.20050723062822.176:selection (sevent.DocumentListener)
        #@-others
        #@nonl
        #@-node:ekr.20050723062822.48:Stategies for keystroke and commands
        #@+node:ekr.20050723062822.184:class vi_emulation
        class vi_emulation:
            
            def __init__( self, c ):
                self.c = c
                self.mode = None
                #@        <<define vi keystrokes>>
                #@+node:ekr.20050723062822.185:<<define vi keystrokes>>
                self.vi_keystrokes = {
                    'dd': self.deleteLine,
                    'i': self.insert,
                }
                #@nonl
                #@-node:ekr.20050723062822.185:<<define vi keystrokes>>
                #@nl
                
            def __call__( self, event, command ):
        
                if self.mode:
                    return self.mode( event, command )
                else:
                    return self.vi_keystrokes[ command ]( event, command )
        #@nonl
        #@+node:ekr.20050723062822.186:cut
        def cut( self, event ):
            pass
        #@nonl
        #@-node:ekr.20050723062822.186:cut
        #@+node:ekr.20050723062822.187:deleteLine
        def deleteLine( self, event, command ):
            pass
        #@nonl
        #@-node:ekr.20050723062822.187:deleteLine
        #@+node:ekr.20050723062822.188:insert
        def insert( self, event, command ):
            pass
        #@nonl
        #@-node:ekr.20050723062822.188:insert
        #@-node:ekr.20050723062822.184:class vi_emulation
        #@-others
    #@nonl
    #@-node:ekr.20050723062822.5:class emacsCommands  (from SwingMacs)
    #@-others
#@nonl
#@-node:ekr.20050724074619:From Swingmacs  NOT USED YET
#@+node:ekr.20050724080624:New classes NOT USED YET
if 0:
    #@    @+others
    #@+node:ekr.20050723063447:createEmacs
    def createEmacs (tag, keywords):
        
        c = keywords.get('c')
        if not c: return
        
        if 1: # Use usetemacs/temacs.
            pass
        else:
            minibuf = emacsMiniBuffer(c) # The widgets comprising the mini buffer.
            emacs = emacsCommands(c,minibuf) # The commands themselves.
            emacsMenus(c,emacs) # The emacs menus.
            emacsBindings(c,emacs,minibuf) # The emacs key bindings.
    #@nonl
    #@-node:ekr.20050723063447:createEmacs
    #@+node:ekr.20050723093904:class emacsMenus
    class emacsMenus:
        
        #@    @+others
        #@+node:ekr.20050723093904.1:ctor
        def __init__ (self,c,emacs):
            
            self.c = c
            self.emacs = emacs
            self.init()
        #@nonl
        #@-node:ekr.20050723093904.1:ctor
        #@+node:ekr.20050723094319:init
        def init (self):
            
            pass
        #@nonl
        #@-node:ekr.20050723094319:init
        #@-others
    #@nonl
    #@-node:ekr.20050723093904:class emacsMenus
    #@+node:ekr.20050723093904.2:class emacsBindings
    class emacsBindings:
        
        #@    @+others
        #@+node:ekr.20050723094319.1:ctor
        def __init__ (self,c,emacs,minibuffer):
            
            self.c = c
            self.emacs = emacs
            self.minibuffer = minibuffer
            self.init()
        #@nonl
        #@-node:ekr.20050723094319.1:ctor
        #@+node:ekr.20050723094319.2:init
        def init (self):
            
            c = self.c
            self.body = c.frame.body
            self.bodyCtrl = c.frame.bodyCtrl
            self.frame = c.frame
            
            # Used by setBufferInteractionMethods.
            self.tnodes = {}
            self.positions = {}
            
            leoCommandNames = {} # Set by addLeoCommands
            self.new_keystrokes = {}  # Set by loadConfig.
        
            self.oldCreateBindings = c.frame.body.createBindings
            c.frame.body.createBindings = self.createBindings
            
            self.oldOnBodyKey = c.frame.body.onBodyKey
            c.frame.body.onBodyKey = self.onBodyKey
            
            self.orig_del = self.frame.bodyCtrl.delete
        #@nonl
        #@-node:ekr.20050723094319.2:init
        #@+node:ekr.20050723100523:Overridden methods
        #@+node:ekr.20050723100523.1:onBodyKey
        def onBodyKey (self,event):
            
            '''stops Return and Tab from being processed if the Emacs instance has state.'''
        
            if event.char.isspace(): 
                # Emacs = temacs.Emacs.Emacs_instances [ event.widget ]
                Emacs = self.emacs.Emacs_instances [ event.widget ]
                if Emacs.mcStateManager.hasState():
                   return None
            else:
                return self.oldOnBodyKey(self.body,event)
        #@nonl
        #@-node:ekr.20050723100523.1:onBodyKey
        #@+node:ekr.20050723100523.2:createBindings & helpers
        def createBindings (self,frame): 
         
            c = self.c ; body = self.body ; bodyCtrl = self.bodyCtrl
        
            if not labels.has_key(frame):
                #@        << create a label for frame >>
                #@+node:ekr.20050723100523.3:<< create a label for frame >>
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
                #@-node:ekr.20050723100523.3:<< create a label for frame >>
                #@nl
                labels [ frame ] = label  
            else:
                label = labels [ frame ]
        
            self.oldCreateBindings(body,frame)
            Emacs = emacsCommands(bodyCtrl,label,useGlobalKillbuffer=True,useGlobalRegisters=True)
            Emacs.setUndoer(bodyCtrl,c.undoer.undo)
            #@    << define utTailEnd >>
            #@+node:ekr.20050723100523.4:<< define utTailEnd >>
            def utTailEnd( buffer,frame=frame):
                
                '''A method that Emacs will call with its _tailEnd method'''
            
                buffer.event_generate( '<Key>' )
                buffer.update_idletasks()
            
                return 'break'
            #@nonl
            #@-node:ekr.20050723100523.4:<< define utTailEnd >>
            #@nl
            Emacs.setTailEnd( frame.bodyCtrl,utTailEnd)
            Emacs.setShutdownHook(c.close)
            self.addTemacsExtensions()
            self.addTemacsAbbreviations()
            self.leoCommandNames = self.addLeoCommands()
            self.changeKeyStrokes(bodyCtrl)
            self.setBufferInteractionMethods(bodyCtrl)
            frame.bodyCtrl.delete = tkDeleteWrapper
        #@nonl
        #@+node:ekr.20050723100523.6:addTemacsAbbreviations:  To do:  get stuff from confic
        def addTemacsAbbreviations(self):
            
            '''Adds abbreviatios and kbd macros to an Emacs instance'''
            
            emacs = self.emacs
        
            pth = os.path.split( g.app.loadDir ) 
            aini = pth[ 0 ] + os.sep + 'plugins' + os.sep
        
            if os.path.exists( aini + r'usetemacs.kbd' ):
                f = file( aini +  r'usetemacs.kbd', 'r' )
                emacs._loadMacros( f )
        
            if os.path.exists( aini + r'usetemacs.abv' ):
                f = file( aini + r'usetemacs.abv', 'r' )
                emacs._readAbbrevs( f )
        #@nonl
        #@-node:ekr.20050723100523.6:addTemacsAbbreviations:  To do:  get stuff from confic
        #@+node:ekr.20050723100523.7:addTemacsExtensions
        def addTemacsExtensions(self):
            
            emacs = self.emacs
            
            '''Adds extensions to Emacs parameter.'''
            for z in extensions:
                try:
                    if hasattr(z, 'getExtensions' ):
                        ex_meths = z.getExtensions()
                        for x in ex_meths.keys():
                            emacs.extendAltX( x, ex_meths[ x ] )
                    else:
                        g.es( 'Module %s does not have a getExtensions function' % z , color = 'red' )
        
                except Exception, x:
                    g.es( 'Could not add extension because of %s' % x, color = 'red' )
        #@nonl
        #@-node:ekr.20050723100523.7:addTemacsExtensions
        #@+node:ekr.20050723100523.8:changeKeyStrokes
        def changeKeyStrokes(self,widget):
            
            emacs = self.emacs
            
            for z in self.new_keystrokes.keys():
        
                emacs.reconfigureKeyStroke(widget,z,self.new_keystrokes[z])
        #@nonl
        #@-node:ekr.20050723100523.8:changeKeyStrokes
        #@+node:ekr.20050723100523.9:setBufferInteractionMethods & helpers
        def setBufferInteractionMethods(self,buffer):
        
            '''This function configures the Emacs instance so that
               it can see all the nodes as buffers for its buffer commands.'''
               
            emacs = self.emacs
               
            #@    @+others
            #@+node:ekr.20050723100523.10:buildBufferList
            # Surprisingly fast on LeoPy.
            def buildBufferList(self):
                '''Build a buffer list from an outline.'''
                c = self.c
                # I was worried that speed factors would make it unusable.
                if not self.tnodes.has_key(c): #I was worried that speed factors would make it unusable.
                    self.tnodes[c] = {}
                ## tdict = self.tnodes.get(c,{})
                bufferdict = {}
                ## tdict.clear()
                self.positions.clear()
                for p in c.allNodes_iter():
                    t = p.v.t ; h = t.headString()
                    theList = self.positions.get(h,[])
                    theList.append(p.copy())
                    self.positions[h] = theList
                    bufferdict[h] = t.bodyString()
                    ## tdict[h] = t 
                
                return bufferdict
            #@nonl
            #@-node:ekr.20050723100523.10:buildBufferList
            #@+node:ekr.20050723100523.11:setBufferData
            def setBufferData (self,name,data):
                
                data = unicode( data )
                tdict = self.tnodes[c]
                if tdict.has_key(name):
                    tdict [ name ].bodyString = data
            #@nonl
            #@-node:ekr.20050723100523.11:setBufferData
            #@+node:ekr.20050723100523.12:gotoNode & gotoPosition
            def gotoNode (self,name):
                
                c = self.c
                
                c.beginUpdate()
                if 1: # update range...
                    if self.positions.has_key(name):
                        posis = self.positions[name]
                        if len(posis) > 1:
                            #@                << create a dialog t1 >>
                            #@+node:ekr.20050723105349:<< create a dialog t1 >>
                            tl = Tk.Toplevel()
                            #tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 ))
                            tl.title( "Select node by numeric position" )
                            fr = Tk.Frame( tl )
                            fr.pack()
                            header = Tk.Label( fr, text='select position' )
                            header.pack()
                            lbox = Tk.Listbox( fr, background='white', foreground='blue' )
                            lbox.pack()
                            for z in xrange( len( posis ) ):
                                lbox.insert( z, z + 1 )
                            lbox.selection_set( 0 )
                            
                            def setPos( event ):
                                cpos = int( lbox.nearest( event.y ) )
                                tl.withdraw()
                                tl.destroy()
                                if cpos != None:
                                    self.gotoPosition(c, posis[ cpos ] )
                            lbox.bind( '<Button-1>', setPos )
                            geometry = tl.geometry()
                            geometry = geometry.split( '+' )
                            geometry = geometry[ 0 ]
                            width = tl.winfo_screenwidth()/3
                            height = tl.winfo_screenheight()/3
                            geometry= '+%s+%s' %( width,height )
                            tl.geometry( geometry )
                            #@nonl
                            #@-node:ekr.20050723105349:<< create a dialog t1 >>
                            #@nl
                        else:
                            p = posis[0]
                            self.gotoPosition(p)
                    else:
                        t = leoNodes.tnode( '',name)
                        p = c.currentPosition().insertAfter(t)
                        self.gotoPosition(p)
                c.endUpdate()
            #@nonl
            #@+node:ekr.20050723100523.13:gotoPosition
            def gotoPosition(self,p):
                
                c = self.c
            
                c.frame.tree.expandAllAncestors(p)
                c.selectPosition(p)
            #@nonl
            #@-node:ekr.20050723100523.13:gotoPosition
            #@-node:ekr.20050723100523.12:gotoNode & gotoPosition
            #@+node:ekr.20050723100523.14:deleteNode
            def deleteNode(self,name):
                
                c = self.c ; current = c.currentPosition()
            
                p = self.positions.get(name)
                if p:
                    c.beginUpdate()
                    p.doDelete(current)
                    c.endUpdate()
            #@nonl
            #@-node:ekr.20050723100523.14:deleteNode
            #@+node:ekr.20050723100523.15:renameNode
            def renameNode(self,name):
            
                c = self.c
            
                c.beginUpdate()
                p = c.currentPosition()
                p.setHeadString(name)
                c.endUpdate()
            #@nonl
            #@-node:ekr.20050723100523.15:renameNode
            #@-others
        
            emacs.setBufferListGetter( buffer,self.buildBufferList )
                # Give the emacs the ability to get a buffer list
            emacs.setBufferSetter( buffer,self.setBufferData )
                # Give the emacs the ability to set a tnodes bodyString.
            emacs.setBufferGoto( buffer,self.gotoNode )
                # Give the emacs the ability t jump to a node
            emacs.setBufferDelete( buffer,self.deleteNode )
                # Give the emacs the ability t delete a node
            emacs.setBufferRename( buffer,self.renameNode )
                # Give the emacs the ability t rename the current node
        #@nonl
        #@-node:ekr.20050723100523.9:setBufferInteractionMethods & helpers
        #@+node:ekr.20050723100523.16:addLeoCommands
        def addLeoCommands(self):
            
            c = self.c ; emacs = self.emacs ; f = c.frame
            
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
                def coverdef( self, event, command=commands[ z ] ):
                    command()
                    emacs.keyboardQuit( event )
        
                emacs.extendAltX( z, coverdef )
        
            return commands.keys()
        #@nonl
        #@-node:ekr.20050723100523.16:addLeoCommands
        #@-node:ekr.20050723100523.2:createBindings & helpers
        #@+node:ekr.20050723105349.1:Methods called by new bindings
        #@+node:ekr.20050723100523.5:tkDeleteWrapper
        def tkDeleteWrapper(self,i,j=None):
        
            '''Watches for complete text deletion.  If it occurs, turns off all state in the Emacs instance.'''
            
            emacs = self.emacs ; bodyCtrl = self.bodyCtrl
        
            if i == '1.0' and j == 'end':
                event = Tk.Event()
                event.widget = bodyCtrl 
                self.emacs.keyboardQuit( event )
        
            return self.orig_del(bodyCtrl,i,j)
        #@nonl
        #@-node:ekr.20050723100523.5:tkDeleteWrapper
        #@-node:ekr.20050723105349.1:Methods called by new bindings
        #@-node:ekr.20050723100523:Overridden methods
        #@-others
    #@nonl
    #@-node:ekr.20050723093904.2:class emacsBindings
    #@+node:ekr.20050723115256.1:class emacsMiniBuffer
    class emacsMiniBuffer:
        
        '''A class to represent the widgets of the minibuffer.'''
        
        #@    @+others
        #@+node:ekr.20050723115256.2:ctor
        #@+at 
        #@nonl
        # If a Tkinter Text widget and Tkinter Label are passed in via the 
        # tbuffer and
        # minibuffer parameters, these are bound to. Otherwise an explicit 
        # call to
        # setBufferStrokes must be done. useGlobalRegisters set to True 
        # indicates that the
        # Emacs instance should use a class attribute that functions as a 
        # global register.
        # useGlobalKillbuffer set to True indicates that the Emacs instances 
        # should use a
        # class attribute that functions as a global killbuffer.
        #@-at
        #@@c
            
        def __init__ (self,c):
            
            self.c = c
            self.frame = c.frame
            
            self.mbuffers = {} # Keys are widgets, values are label widgets.
            self.svars = {} # Keys are widgets, values are Tk StringVars.
        #@nonl
        #@-node:ekr.20050723115256.2:ctor
        #@+node:ekr.20050723115256.3:init
        def init (self,c):
            
            self.c = c
        #@-node:ekr.20050723115256.3:init
        #@+node:ekr.20050723115903.1:Tk label methods
        #@+at 
        #@nonl
        # Svars are the internals of the minibuffer and the labels are the 
        # presentation of those internals
        #@-at
        #@nonl
        #@+node:ekr.20050723115903.2:setLabelGrey
        def setLabelGrey( self, label ):
        
            label.configure( background = 'lightgrey' )
        #@nonl
        #@-node:ekr.20050723115903.2:setLabelGrey
        #@+node:ekr.20050723115903.3:setLabelBlue
        def setLabelBlue( self ,label ):
        
            label.configure( background = 'lightblue' )
        #@nonl
        #@-node:ekr.20050723115903.3:setLabelBlue
        #@+node:ekr.20050723115903.4:reset (was resetMiniBuffer)
        def reset( self, event ):
        
            svar, label = self.getSvarLabel( event )
            svar.set( '' )
            label.configure( background = 'lightgrey' )
        #@nonl
        #@-node:ekr.20050723115903.4:reset (was resetMiniBuffer)
        #@-node:ekr.20050723115903.1:Tk label methods
        #@+node:ekr.20050723115903.5:Tk StringVar methods
        #@+at
        # These methods get and alter the Svar variable which is a Tkinter
        # StringVar.  This StringVar contains what is displayed in the 
        # minibuffer.
        #@-at
        #@@c
        #@+node:ekr.20050723115903.6:getSvarLabel
        def getSvarLabel( self, event ):
            
            '''returns the StringVar and Label( minibuffer ) for a specific Text editor'''
            
            w = event.widget
        
            svar = self.svars.get(w)
            label = self.mbuffers.get(w)
        
            return svar, label
        #@nonl
        #@-node:ekr.20050723115903.6:getSvarLabel
        #@+node:ekr.20050723115903.7:setSvar
        def setSvar( self, event, svar ):
        
            '''Alters the StringVar svar to represent the change in the event.
               It mimics what would happen with the keyboard and a Text editor
               instead of plain accumalation.'''
        
            t = svar.get()  
            if event.char == '\b':
               if len(t) == 1:
                   t = ''
               else:
                   t = t[0:-1]
               svar.set(t)
            else:
                t = t + event.char
                svar.set(t)
        #@nonl
        #@-node:ekr.20050723115903.7:setSvar
        #@-node:ekr.20050723115903.5:Tk StringVar methods
        #@-others
    #@nonl
    #@-node:ekr.20050723115256.1:class emacsMiniBuffer
    #@-others
#@nonl
#@-node:ekr.20050724080624:New classes NOT USED YET
#@+node:ekr.20050724074619.1:From usetemacs
# Based on version .57 EKR:
#@nonl
#@+node:ekr.20050724074642.14:USETEMACSinit NOT USED
if 0:
    def USETEMACSinit ():
    
        ok = temacs and Tk and not g.app.unitTesting
        
        if ok:
            if g.app.gui is None: 
                g.app.createTkGui(__file__)
        
            if g.app.gui.guiName() == "tkinter":
                #@                << override createBindings and onBodyKey >>
                #@+node:ekr.20050724074642.15:<< override createBindings and onBodyKey >>
                global orig_Bindings,orig_OnBodyKey
                
                orig_Bindings = leoTkinterFrame.leoTkinterBody.createBindings
                leoTkinterFrame.leoTkinterBody.createBindings = createBindings
                
                orig_OnBodyKey = leoTkinterFrame.leoTkinterBody.onBodyKey
                leoTkinterFrame.leoTkinterBody.onBodyKey = modifyOnBodyKey
                #@nonl
                #@-node:ekr.20050724074642.15:<< override createBindings and onBodyKey >>
                #@nl
                loadConfig()
                g.plugin_signon(__name__)
                leoPlugins.registerHandler( ('open2', "new") , addMenu )
                
        return ok
#@nonl
#@-node:ekr.20050724074642.14:USETEMACSinit NOT USED
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

    if event.char.isspace(): 
        emacs = Emacs.Emacs_instances [ event.widget ]   
        if emacs.mcStateManager.hasState():
           return None
    else:
        return orig_OnBodyKey(self,event)
#@nonl
#@-node:ekr.20050724074642.24:modifyOnBodyKey
#@+node:ekr.20050724074642.25:createBindings & helpers
def createBindings (self,frame): 
 
    if not labels.has_key(frame):
        #@        << create a label for frame >>
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
        labels [ frame ] = label  
    else:
        label = labels [ frame ]

    orig_Bindings(self,frame)
    emacs = Emacs( frame.bodyCtrl, label, useGlobalKillbuffer = True, useGlobalRegisters = True )
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
            g.trace()
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
tnodes = {}
positions =  {}

def setBufferInteractionMethods( c, emacs, buffer ):

    '''This function configures the Emacs instance so that
       it can see all the nodes as buffers for its buffer commands.'''
       
    #@    @+others
    #@+node:ekr.20050724074642.33:buildBufferList
    def buildBufferList(): #This builds a buffer list from what is in the outline.  Worked surprisingly fast on LeoPy.
        if not tnodes.has_key( c ): #I was worried that speed factors would make it unusable.
            tnodes[ c ] = {}
        tdict = tnodes[ c ]
        pos = c.rootPosition()
        utni = pos.allNodes_iter()
        bufferdict = {}
        tdict.clear()
        positions.clear()
        for z in utni:
        
           t = z.v.t
           if positions.has_key( t.headString ):
            positions[ t.headString ].append( z.copy() )
           else:
            positions[ t.headString ] = [ z.copy() ]#not using a copy seems to have bad results.
           #positions[ t.headString ] = z
        
           bS = ''
           if t.bodyString: bS = t.bodyString
    
           
           bufferdict[ t.headString ] = bS
           tdict[ t.headString ] = t 
        
        return bufferdict
    #@nonl
    #@-node:ekr.20050724074642.33:buildBufferList
    #@+node:ekr.20050724074642.34:setBufferData
    def setBufferData( name, data ):
        
        data = unicode( data )
        tdict = tnodes[ c ]
        if tdict.has_key( name ):
            tdict[ name ].bodyString = data
    #@nonl
    #@-node:ekr.20050724074642.34:setBufferData
    #@+node:ekr.20050724074642.35:gotoNode & gotoPosition
    def gotoNode( name ):
        
        c.beginUpdate()
        if positions.has_key( name ):
            posis = positions[ name ]
            if len( posis ) > 1:
                tl = Tk.Toplevel()
                #tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 ))
                tl.title( "Select node by numeric position" )
                fr = Tk.Frame( tl )
                fr.pack()
                header = Tk.Label( fr, text='select position' )
                header.pack()
                lbox = Tk.Listbox( fr, background='white', foreground='blue' )
                lbox.pack()
                for z in xrange( len( posis ) ):
                    lbox.insert( z, z + 1 )
                lbox.selection_set( 0 )
                def setPos( event ):
                    cpos = int( lbox.nearest( event.y ) )
                    tl.withdraw()
                    tl.destroy()
                    if cpos != None:
                        gotoPosition( c, posis[ cpos ] )
                lbox.bind( '<Button-1>', setPos )
                geometry = tl.geometry()
                geometry = geometry.split( '+' )
                geometry = geometry[ 0 ]
                width = tl.winfo_screenwidth()/3
                height = tl.winfo_screenheight()/3
                geometry= '+%s+%s' %( width,height )
                tl.geometry( geometry )
            else:
                pos = posis[ 0 ]
                gotoPosition( c, pos )
        else:
            pos2 = c.currentPosition()
            tnd = leoNodes.tnode( '', name )
            pos = pos2.insertAfter( tnd )
            gotoPosition( c, pos )
        #c.frame.tree.expandAllAncestors( pos )
        #c.selectPosition( pos )
        #c.endUpdate()
    #@nonl
    #@+node:ekr.20050724074642.36:gotoPosition
    def gotoPosition( c, pos ):
    
        c.frame.tree.expandAllAncestors( pos )
        c.selectPosition( pos )
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.36:gotoPosition
    #@-node:ekr.20050724074642.35:gotoNode & gotoPosition
    #@+node:ekr.20050724074642.37:deleteNode
    def deleteNode( name ):
        
        c.beginUpdate()
        if positions.has_key( name ):
            pos = positions[ name ]
            cpos = c.currentPosition()
            pos.doDelete( cpos )
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.37:deleteNode
    #@+node:ekr.20050724074642.38:renameNode
    def renameNode( name ):
    
        c.beginUpdate()
        pos = c.currentPosition()
        pos.setHeadString( name )
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.38:renameNode
    #@-others

    emacs.setBufferListGetter( buffer, buildBufferList ) #This gives the Emacs instance the ability to get a buffer list
    emacs.setBufferSetter( buffer, setBufferData )# This gives the Emacs instance the ability to set a tnodes bodyString
    emacs.setBufferGoto( buffer, gotoNode )# This gives the Emacs instance the ability to jump to a node
    emacs.setBufferDelete( buffer, deleteNode )# This gives the Emacs instance the ability to delete a node
    emacs.setBufferRename( buffer, renameNode )# This gives the Emacs instance the ability to rename the current node
#@nonl
#@-node:ekr.20050724074642.32:setBufferInteractionMethods & helpers
#@+node:ekr.20050724074642.39:addLeoCommands
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
#@-node:ekr.20050724074642.39:addLeoCommands
#@-node:ekr.20050724074642.25:createBindings & helpers
#@-node:ekr.20050724074642.23:Overridden methods
#@-node:ekr.20050724074619.1:From usetemacs
#@+node:ekr.20050724075341:From temacs
#@+node:ekr.20050724075352.13:Emacs helper classes
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
        1: emacs.setNextRegister,
        2: emacs.executeRegister,        
        }
    #@nonl
    #@-node:ekr.20050724075352.15:__init__
    #@+node:ekr.20050724075352.16:__call__
    def __call__( self, event , stroke ):
        
        self.previous.insert( 0, event.keysym )
        emacs = self.emacs 
        if len( self.previous ) > 10: self.previous.pop()
        if stroke in ('<Key>', '<Escape>' ):
            return self.processKey( event )
        if stroke in emacs.xcommands:
            emacs.xcommands[ stroke ]( event )
            if stroke != '<Control-b>': emacs.keyboardQuit( event )
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
        elif self.rect_commands.has_key( event.keysym ) and emacs.rectanglemode == 1:
            return self.processRectangle( event )
            
        if self.register_commands.has_key( emacs.registermode ):
            self.register_commands[ emacs.registermode ]( event )
            return 'break'
        
        if self.variety_commands.has_key( event.keysym ):
            emacs.stopControlX( event )
            return self.variety_commands[ event.keysym ]( event )
            
        
        #if emacs.sRect:
        #    return emacs.stringRectangle( event )
        #    #return 'break'
        if event.keysym in ( 'a', 'i' , 'e'):
            if self.processAbbreviation( event ): return 'break'
    
        if event.keysym == 'g':
            svar, label = emacs.getSvarLabel( event )
            l = svar.get()
            if self.abbreviationDispatch.has_key( l ):
                emacs.stopControlX( event )
                return self.abbreviationDispatch[ l ]( event )
            #if l == 'a':
            #    emacs.stopControlX( event )
            #    return emacs.abbreviationDispatch( event, 1 )
            #elif l == 'a i':
            #    emacs.stopControlX( event )
            #    return emacs.abbreviationDispatch( event, 2 )
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
        #if event.keysym == 'r':
        #    return emacs.activateRectangleMethods( event )
        #if self.rect_commands.has_key( event.keysym ):# and emacs.registermode == 1:
        #    return self.processRectangle( event )
         
        #if emacs.registermode == 1:
        #    emacs.setNextRegister( event )
        #    return 'break'
        #elif emacs.registermode == 2:
        #    emacs.executeRegister( event )
        #    return 'break'
        #if self.register_commands.has_key( emacs.registermode ):
        #    print 'register commands'
        #    self.register_commands[ emacs.registermode ]( event )
        #    return 'break'
        #if event.keysym == 'r':
        #    return emacs.activateRectangleMethods( event )
        #    emacs.registermode = 1
        #    svar = emacs.svars[ event.widget ]
        #    svar.set( 'C - x r' )
        #    return 'break'
        #if event.keysym== 'h':
        #    emacs.stopControlX( event )
        #    event.widget.tag_add( 'sel', '1.0', 'end' )
        #tag_add( 'sel', '1.0', 'end' )    return 'break' 
        #if event.keysym == 'equal':
        #    emacs.lineNumber( event )
        #    return 'break'
        #if event.keysym == 'u':
        #    emacs.stopControlX( event )
        #    return emacs.doUndo( event, 2 )
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
        #@    <<statecommands>>
        #@+node:ekr.20050724075352.22:<<statecommands>>
        # EKR: used only below.
        def eA( event ):
            if self.emacs.expandAbbrev( event ) :
                return 'break'
        
        self.stateCommands = { #1 == one parameter, 2 == all
            'uC': ( 2, emacs.universalDispatch ),
            'controlx': ( 2, emacs.doControlX ),
            'isearch':( 2, emacs.iSearch ),
            'goto': ( 1, emacs.Goto ),
            'zap': ( 1, emacs.zapTo ),
            'howM': ( 1, emacs.howMany ),
            'abbrevMode': ( 1, emacs.abbrevCommand1 ),
            'altx': ( 1, emacs.doAlt_X ),
            'qlisten': ( 1, emacs.masterQR ),
            'rString': ( 1, emacs.replaceString ),
            'negativeArg':( 2, emacs.negativeArgument ),
            'abbrevOn': ( 1, eA ),
            'set-fill-column': ( 1, emacs.setFillColumn ),
            'chooseBuffer': ( 1, emacs.chooseBuffer ),
            'renameBuffer': ( 1, emacs.renameBuffer ),
            're_search': ( 1, emacs.re_search ),
            'alterlines': ( 1, emacs.processLines ),
            'make_directory': ( 1, emacs.makeDirectory ),
            'remove_directory': ( 1, emacs.removeDirectory ),
            'delete_file': ( 1, emacs.deleteFile ),
            'nonincr-search': ( 2, emacs.nonincrSearch ),
            'word-search':( 1, emacs.wordSearch ),
            'last-altx': ( 1, emacs.executeLastAltX ),
            'escape': ( 1, emacs.watchEscape ),
            'subprocess': ( 1, emacs.subprocesser ),
            }
        #@nonl
        #@-node:ekr.20050724075352.22:<<statecommands>>
        #@nl
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
        
            '<Control-s>': ( 2, emacs.startIncremental ), 
            '<Control-r>': ( 2, emacs.startIncremental ),
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
    def __call__( self, event, stroke ):
        
        kstroke = self.keystrokes[ stroke ]
        
        if 0: # EKR: this would be better:
            numberOfArgs,func = self.keystrokes[ stroke ]
            if numberOfArgs == 1:
                return func(event)
            else:
                return func(event,stroke)
        
        # EKR: which[0] is the number of params.
        # EKR: which[1] is the function.
    
        if kstroke[ 0 ] == 1:
            return kstroke[ 1 ]( event )
        else:
            return kstroke[ 1 ]( event, stroke )
    #@nonl
    #@-node:ekr.20050724075352.32:__call__
    #@+node:ekr.20050724075352.33:hasKeyStroke
    def hasKeyStroke( self, stroke ):
        
        return self.keystrokes.has_key( stroke )
    #@nonl
    #@-node:ekr.20050724075352.33:hasKeyStroke
    #@-others
#@nonl
#@-node:ekr.20050724075352.29:class MC_KeyStrokeManager  (hard-coded keystrokes)
#@+node:ekr.20050724075352.34:class Tracker
class Tracker:

    '''A class designed to allow the user to cycle through a list
       and to change the list as deemed appropiate.'''

    #@    @+others
    #@+node:ekr.20050724075352.35:init
    def __init__( self ):
        
        self.tablist = []
        self.prefix = None
        self.ng = self._next()
    #@nonl
    #@-node:ekr.20050724075352.35:init
    #@+node:ekr.20050724075352.36:setTabList
    def setTabList( self, prefix, tlist ):
        
        self.prefix = prefix
        self.tablist = tlist
    #@nonl
    #@-node:ekr.20050724075352.36:setTabList
    #@+node:ekr.20050724075352.37:_next
    def _next( self ):
        
        while 1:
            tlist = self.tablist
            if not tlist: yield ''
            for z in self.tablist:
                if tlist != self.tablist:
                    break
                yield z
    #@nonl
    #@-node:ekr.20050724075352.37:_next
    #@+node:ekr.20050724075352.38:next
    def next( self ):
        
        return self.ng.next()
    #@nonl
    #@-node:ekr.20050724075352.38:next
    #@+node:ekr.20050724075352.39:clear
    def clear( self ):
    
        self.tablist = []
        self.prefix = None
    #@nonl
    #@-node:ekr.20050724075352.39:clear
    #@-others
#@nonl
#@-node:ekr.20050724075352.34:class Tracker
#@-others
#@nonl
#@-node:ekr.20050724075352.13:Emacs helper classes
#@+node:ekr.20050724075352.40:class Emacs
class Emacs:
    '''The Emacs class binds to a Tkinter Text widget and adds Emac derived keystrokes and commands
       to it.'''
    
    Emacs_instances = weakref.WeakKeyDictionary()
    global_killbuffer = []
    global_registers = {}
    lossage = [] ### EKR: list( ' ' * 100 )

    #@    @+others
    #@+node:ekr.20050724075352.41:Emacs.__init__
    def __init__( self , tbuffer = None , minibuffer = None, useGlobalKillbuffer = False, useGlobalRegisters = False):
        '''Sets up Emacs instance.
        
        If a Tkinter Text widget and Tkinter Label are passed in
        via the tbuffer and minibuffer parameters, these are bound to.
        Otherwise an explicit call to setBufferStrokes must be done.
        useGlobalRegisters set to True indicates that the Emacs instance should use a class attribute that functions
        as a global register.
        useGlobalKillbuffer set to True indicates that the Emacs instances should use a class attribute that functions
        as a global killbuffer.'''
        
        self.mbuffers = {} 
        self.svars = {}
    
        #self.isearch = False
        self.tailEnds = {} #functions to execute at the end of many Emac methods.  Configurable by environment.
        self.undoers = {} #Emacs instance tracks undoers given to it.
        self.store = {'rlist': [], 'stext': ''} 
        
        #macros
        self.lastMacro = None 
        self.macs = []
        self.macro = []
        self.namedMacros = {}
        self.macroing = False
        self.dynaregex = re.compile( r'[%s%s\-_]+' %( string.ascii_letters, string.digits ) ) #for dynamic abbreviations
        self.altx_history = []
        self.keysymhistory = [] 
        
        #This section sets up the buffer data structures
        self.bufferListGetters = {}
        self.bufferSetters = {}
        self.bufferGotos = {}
        self.bufferDeletes = {}
        self.renameBuffers = {}
        self.bufferDict = None
        self.bufferTracker = Tracker()
        self.bufferCommands = {
        
        'append-to-buffer': self.appendToBuffer,
        'prepend-to-buffer': self.prependToBuffer,
        'copy-to-buffer': self.copyToBuffer,
        'insert-buffer': self.insertToBuffer,
        'switch-to-buffer': self.switchToBuffer,
         'kill-buffer': self.killBuffer,   
        }
        
        self.swapSpots = []
        self.ccolumn = '0'
        #self.howM = False
        self.reset = False
        if useGlobalKillbuffer:
            self.killbuffer = Emacs.global_killbuffer
        else:
            self.killbuffer = []
        self.kbiterator = self.iterateKillBuffer()
        
        #self.controlx = False
        self.csr = { '<Control-s>': 'for', '<Control-r>':'bak' }
        self.pref = None
        #self.zap = False
        #self.goto = False
        self.previousStroke = ''
        if useGlobalRegisters:
            self.registers = Emacs.global_registers
        else:
            self.registers = {}
        
        #registers
        self.regMeth = None
        self.regMeths, self.regText = self.addRegisterItems()
    
        #Abbreviations
        self.abbrevMode = False 
        self.abbrevOn = False # determines if abbreviations are on for masterCommand and toggle abbreviations
        self.abbrevs = {}
        
        self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
        self.regXKey = None
        
        self.fillPrefix = '' #for fill prefix functions
        self.fillColumn = 70 #for line centering
        self.registermode = False #for rectangles and registers
        
        self.qQ = None
        self.qR = None
        #self.qlisten = False
        #self.lqR = Tk.StringVar()
        #self.lqR.set( 'Query with: ' ) # replaced with using the svar and self.mcStateManager
        self.qgetQuery = False
        #self.lqQ = Tk.StringVar()
        #self.lqQ.set( 'Replace with:' )# replaced with using the svar and self.mcStateManager
        self.qgetReplace = False
        self.qrexecute = False
        self.querytype = 'normal'
        
        #self.rString = False
        #These attributes are for replace-string and replace-regex
        self._sString = ''
        self._rpString = ''
        self._useRegex = False
        
        self.sRect = False  #State indicating string rectangle.  May be moved to MC_StateManager
        self.krectangle = None #The kill rectangle
        self.rectanglemode = 0 #Determines what state the rectangle system is in.
        
        self.last_clipboard = None #For interacting with system clipboard.
        
        self.negativeArg = False 
        self.negArgs = { '<Alt-c>': self.changePreviousWord,
        '<Alt-u>' : self.changePreviousWord,
        '<Alt-l>': self.changePreviousWord } #For negative argument functionality
        
        #self.altx = False
        #Alt-X commands.
        self.doAltX = self.addAltXCommands()
        self.axTabList = Tracker()
        self.x_hasNumeric = [ 'sort-lines' , 'sort-fields']
        
        #self.uC = False
        #These attributes are for the universal command functionality.
        self.uCstring = string.digits + '\b'
        self.uCdict = { '<Alt-x>' : self.alt_X }
        
        self.cbDict = self.addCallBackDict()# Creates callback dictionary, primarily used in the master command
        self.xcommands = self.addXCommands() # Creates the X commands dictionary
        self.cxHandler = ControlXHandler( self ) #Creates the handler for Control-x commands
        self.mcStateManager = MC_StateManager( self ) #Manages state for the master command
        self.kstrokeManager = MC_KeyStrokeManager( self ) #Manages some keystroke state for the master command.
        self.shutdownhook = None #If this is set via setShutdownHook, it is executed instead of sys.exit when Control-x Control-c is fired
        self.shuttingdown = False #indicates that the Emacs instance is shutting down and no work needs to be done.
        
        if tbuffer and minibuffer:
            self.setBufferStrokes( tbuffer, minibuffer )
    #@nonl
    #@-node:ekr.20050724075352.41:Emacs.__init__
    #@+node:ekr.20050724075352.42:getHelpText
    def getHelpText():
        '''This returns a string that describes what all the
        keystrokes do with a bound Text widget.'''
        help_t = [ 'Buffer Keyboard Commands:',
        '----------------------------------------\n',
        '<Control-p>: move up one line',
        '<Control-n>: move down one line',
        '<Control-f>: move forward one char',
        '<Conftol-b>: move backward one char',
        '<Control-o>: insert newline',
        '<Control-Alt-o> : insert newline and indent',
        '<Control-j>: insert newline and tab',
        '<Alt-<> : move to start of Buffer',
        '<Alt- >' +' >: move to end of Buffer',
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
        '<Control-x a e>: Expand the abbrev before point (expand-abbrev). This is effective even when Abbrev mode is not enabled',
        '<Control-x a g>: Define an abbreviation for previous word',
        '<Control-x a i g>: Define a word as abbreviation for word before point, or in point',                        
        '----------------------------------------\n',
        '<Control s>: forward search, using pattern in Mini buffer.\n',
        '<Control r>: backward search, using pattern in Mini buffer.\n' ,
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
        '<Control-x Control-o>: delete blank lines' ,
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
        'delete-char - delete character under cursor' , 
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
        
        return '\n'.join( help_t )
    
    getHelpText = staticmethod( getHelpText )
    #@nonl
    #@-node:ekr.20050724075352.42:getHelpText
    #@+node:ekr.20050724075352.43:masterCommand
    #self.controlx = False
    #self.csr = { '<Control-s>': 'for', '<Control-r>':'bak' }
    #self.pref = None
    #self.zap = False
    #self.goto = False
    #self.previousStroke = ''
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
            
            if 1: # traces
                g.trace(event.keysym,stroke)
                #g.trace(self.keysymhistory)
                #g.trace(Emacs.lossage)
        if 0:
            #@        << old insert code >>
            #@+node:ekr.20050724075352.46:<< old insert code >>
            Emacs.lossage.reverse()
            Emacs.lossage.append( event.char ) #Then we add the new char.  Hopefully this will keep Python from allocating a new array each time.
            Emacs.lossage.reverse()
            
            self.keysymhistory.reverse()
            self.keysymhistory.append( event.keysym )
            self.keysymhistory.reverse()
            #@nonl
            #@-node:ekr.20050724075352.46:<< old insert code >>
            #@nl
    
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
    
        #@    << old code >>
        #@+node:ekr.20050724075352.44:<< old code >>
        
        #if self.uC:
        #    self.previousStroke = stroke
        #    return self.universalDispatch( event, stroke )
        
        #if self.controlx:
        #    self.previousStroke = stroke
        #     return self.doControlX( event, stroke )
        
        
        #if stroke in ('<Control-s>', '<Control-r>' ): 
        #    self.previousStroke = stroke
        #    return self.startIncremental( event, stroke )
        
        #if self.isearch:
        #   return self.iSearch( event )
        
        #if stroke == '<Alt-g>':
        #    self.previousStroke = stroke
        #    return self.startGoto( event )
        #if self.goto:
        #    return self.Goto( event )
        
        #if stroke == '<Alt-z>':
        #    self.previousStroke = stroke
        #    return self.startZap( event )
        
        #if self.zap:
        #    return self.zapTo( event )
        #@nonl
        #@-node:ekr.20050724075352.44:<< old code >>
        #@nl
        if self.regXRpl: # EKR: a generator.
            try:
                self.regXKey = event.keysym
                self.regXRpl.next() # EKR: next() may throw StopIteration.
            finally:
                return 'break'
    
        #@    << old code 2 >>
        #@+node:ekr.20050724075352.45:<< old code 2 >>
        
            #if self.howM:
            #    return self.howMany( event )
                
            #if self.abbrevMode:
            #    return self.abbrevCommand1( event )
                
            #if self.altx:
            #    return self.doAlt_X( event )
        
            #if stroke == '<Alt-percent>':
            #    self.previousStroke = stroke
            #    return self.masterQR( event )  
            #if self.qlisten:
            #    return self.masterQR( event )
                
            #if self.rString:
            #    return self.replaceString( event )
             
            #if self.negativeArg:
            #    return self.negativeArgument( event, stroke )
            
            #if stroke == '<Control-Alt-w>':
            #    self.previousStroke = '<Control-Alt-w>'   
            #    return 'break'
        #@nonl
        #@-node:ekr.20050724075352.45:<< old code 2 >>
        #@nl
        if self.abbrevOn:
            if self.expandAbbrev( event ) :
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
    
        return self.stopControlX( event ) #This method will eventually contain the stopControlX code.
    #@nonl
    #@-node:ekr.20050724075352.47:keyboardQuit
    #@+node:ekr.20050724075352.48:add command dictionary methods
    #@+at
    # These methods create the dispatch dictionarys that the
    # Emacs instance uses to execute specific keystrokes and commands.
    # Dont mess with it if you dont understand this section, without these 
    # dictionarys
    # the Emacs system cant work.
    #@-at
    #@@c
    
    #@+others
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
        
        #many of the simpler methods need self.keyboardQuit( event ) appended to the end to stop the Alt-x mode.
        doAltX= {
        'prepend-to-register': self.prependToRegister,
        'append-to-register': self.appendToRegister,
        'replace-string': self.replaceString,
        'replace-regex': lambda event:  self.activateReplaceRegex() and self.replaceString( event ),
        'sort-lines': self.sortLines,
        'sort-columns': self.sortColumns,
        'reverse-region': self.reverseRegion,
        'sort-fields': self.sortFields,
        'abbrev-mode': self.toggleAbbrevMode,
        'kill-all-abbrevs': self.killAllAbbrevs,
        'expand-region-abbrevs': self.regionalExpandAbbrev,
        'write-abbrev-file': self.writeAbbreviations,
        'read-abbrev-file': self.readAbbreviations,
        'fill-region-as-paragraph': self.fillRegionAsParagraph,
        'fill-region': self.fillRegion,
        'close-rectangle': self.closeRectangle,
        'how-many': self.startHowMany,
        'kill-paragraph': self.killParagraph,
        'backward-kill-paragraph': self.backwardKillParagraph,
        'backward-kill-sentence': lambda event: self.keyboardQuit( event ) and self.killsentence( event, back = True ),
        'name-last-kbd-macro': self.nameLastMacro,
        'load-file': self.loadMacros,
        'insert-keyboard-macro' : self.getMacroName,
        'list-abbrevs': self.listAbbrevs,
        'kill-word': lambda event, frm = 'insert wordstart', to = 'insert wordend': self.kill( event,frm, to ) and self.keyboardQuit( event ),
        'kill-line': lambda event, frm = 'insert', to = 'insert lineend': self.kill( event, frm, to) and self.keyboardQuit( event ), 
        'kill-sentence': lambda event : self.killsentence( event ) and self.keyboardQuit( event ),
        'kill-region': lambda event, which = 'd' :self.killRegion( event, which ) and self.keyboardQuit( event ),
        'yank': lambda event, frm = 'insert', which = 'c': self.walkKB( event, frm, which) and self.keyboardQuit( event ),
        'yank-pop' : lambda event , frm = "insert", which = 'a': self.walkKB( event, frm, which ) and self.keyboardQuit( event ),
        'backward-kill-word': lambda event: self.deletelastWord( event ) and self.keyboardQuit( event ),
        'backward-delete-char':lambda event, which = 'BackSpace': self.manufactureKeyPress( event, which ) and self.keyboardQuit( event ),
        'delete-char': lambda event: self.deleteNextChar( event ) and self.keyboardQuit( event ) , 
        'isearch-forward': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '<Control-s>' ),
        'isearch-backward': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '<Control-r>' ),
        'isearch-forward-regexp': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '<Control-s>', which = 'regexp' ),
        'isearch-backward-regexp': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '<Control-r>', which = 'regexp' ),
        'capitalize-word': lambda event, which = 'cap' : self.capitalize( event, which ) and self.keyboardQuit( event ),
        'upcase-word': lambda event, which = 'up' : self.capitalize( event, which ) and self.keyboardQuit( event ),
        'downcase-word': lambda event, which = 'low' : self.capitalize( event, which ) and self.keyboardQuit( event ),
        'indent-region': lambda event: self.indentRegion( event ) and self.keyboardQuit( event ),
        'indent-rigidly': lambda event: self.tabIndentRegion( event ) and self.keyboardQuit( event ),
        'indent-relative': self.indent_relative,
        'set-mark-command': lambda event: self.setRegion( event ) and self.keyboardQuit( event ),
        'kill-rectangle': lambda event: self.killRectangle( event ),
        'delete-rectangle': lambda event: self.deleteRectangle( event ),
        'yank-rectangle': lambda event: self.yankRectangle( event ),
        'open-rectangle': lambda event: self.openRectangle( event ),
        'clear-rectangle': lambda event: self.clearRectangle( event ),
        'copy-to-register': lambda event: self.setEvent( event, 's' ) and self.setNextRegister( event ),
        'insert-register': lambda event: self.setEvent( event, 'i' ) and self.setNextRegister( event ),
        'copy-rectangle-to-register': lambda event: self.setEvent( event, 'r' ) and self.setNextRegister( event ),
        'jump-to-register': lambda event: self.setEvent( event, 'j' ) and self.setNextRegister( event ),
        'point-to-register': lambda event: self.setEvent( event, 'space' ) and self.setNextRegister( event ),
        'number-to-register': lambda event: self.setEvent( event, 'n' ) and self.setNextRegister( event ),
        'increment-register': lambda event: self.setEvent( event, 'plus' ) and self.setNextRegister( event ),
        'view-register': lambda event: self.setEvent( event, 'view' ) and self.setNextRegister( event ),
        'beginning-of-line': lambda event, spot = 'insert linestart': self.moveTo( event, spot ) and self.keyboardQuit( event ),
        'end-of-line': lambda event, spot = 'insert lineend': self.moveTo( event, spot ) and self.keyboardQuit( event ),
        'keyboard-quit': lambda event: self.keyboardQuit( event ),
        'advertised-undo': lambda event: self.doUndo( event ) and self.keyboardQuit( event ),
        'back-to-indentation': lambda event: self.backToIndentation( event ) and self.keyboardQuit( event ),
        'delete-indentation': lambda event: self.deleteIndentation( event ) and self.keyboardQuit( event ),    
        'view-lossage': lambda event: self.viewLossage( event ),
         'transpose-chars': lambda event : self.swapCharacters( event ) and self.keyboardQuit( event ),
         'transpose-words': lambda event, sw = self.swapSpots: self.swapWords( event, sw ) and self.keyboardQuit( event ),
         'transpose-lines': lambda event: self.transposeLines( event ) and self.keyboardQuit( event ),
         'insert-file' : lambda event: self.insertFile( event ) and self.keyboardQuit( event ),
         'save-buffer' : lambda event: self.saveFile( event ) and self.keyboardQuit( event ),
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
         'copy-to-buffer': lambda event, which = 'copy-to-buffer': self.setInBufferMode( event, which ),
         'insert-buffer': lambda event, which = 'insert-buffer': self.setInBufferMode( event, which ),
         'append-to-buffer': lambda event , which = 'append-to-buffer':  self.setInBufferMode( event, which ),
         'prepend-to-buffer': lambda event, which = 'prepend-to-buffer': self.setInBufferMode( event, which ),
         'switch-to-buffer': lambda event, which = 'switch-to-buffer': self.setInBufferMode( event, which ),
         'list-buffers' : lambda event: self.listBuffers( event ),
         'kill-buffer' : lambda event, which = 'kill-buffer': self.setInBufferMode( event, which ),
         'rename-buffer': lambda event: self.renameBuffer( event ),
         'query-replace': lambda event: self.masterQR( event ), 
         'query-replace-regex': lambda event: self.startRegexReplace() and self.masterQR( event ),
         'inverse-add-global-abbrev': lambda event: self.abbreviationDispatch( event, 2 ) ,  
         'expand-abbrev': lambda event : self.keyboardQuit( event ) and self.expandAbbrev( event ), 
         'iconfify-or-deiconify-frame': lambda event: self.suspend( event ) and self.keyboardQuit( event ),
         'save-buffers-kill-emacs': lambda event: self.keyboardQuit( event ) and self.shutdown( event ),
         're-search-forward': lambda event: self.reStart( event ),
         're-search-backward': lambda event: self.reStart( event, which = 'backward' ),
         'diff': self.diff, 
         'what-line': self.whatLine,
         'flush-lines': lambda event: self.startLines( event ),
         'keep-lines': lambda event: self.startLines( event, which = 'keep' ),
         'make-directory': lambda event: self.makeDirectory( event ),
         'remove-directory': lambda event: self.removeDirectory( event ),
         'delete-file': lambda event: self.deleteFile( event ),
         'search-forward': lambda event: self.startNonIncrSearch( event, 'for' ),
         'search-backward': lambda event: self.startNonIncrSearch( event, 'bak' ),
         'word-search-forward': lambda event : self.startWordSearch( event, 'for' ),
         'word-search-backward': lambda event: self.startWordSearch( event, 'bak' ),
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
    #@nonl
    #@-node:ekr.20050724075352.51:addAltXCommands
    #@+node:ekr.20050724075352.52:addRegisterItems
    def addRegisterItems( self ):
        
        regMeths = {
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
        
        regText = {
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
        
        return regMeths, regText
    #@nonl
    #@-node:ekr.20050724075352.52:addRegisterItems
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.48:add command dictionary methods
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
    #@+node:ekr.20050724075352.97:Label( minibuffer ) and svar methods
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
    #@-node:ekr.20050724075352.97:Label( minibuffer ) and svar methods
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
    #mbuffers = {}
    #svars = {}
    def setBufferStrokes( self, tbuffer, label ):
        '''setBufferStrokes takes a Tk Text widget called 'tbuffer'. 'stext' is a function or method
        that when called will return the value of the search text. 'rtext' is a function or method
        that when called will return the value of the replace text.  It is this method and
        getHelpText that users of the temacs module should call.  The rest are callback functions
        that enable the Emacs emulation.'''
        
        g.trace(tbuffer,label)
    
        Emacs.Emacs_instances[ tbuffer ] = self
        #@    << define cb callback >>
        #@+node:ekr.20050724075352.113:<< define cb callback >>
        
        def cb( evstring ):
            _cb = None
            if self.cbDict.has_key( evstring ):
                _cb = self.cbDict[ evstring ]
            evstring = '<%s>' % evstring
            if evstring != '<Key>':
                # g.trace(evstring)
                tbuffer.bind( evstring,  lambda event, meth = _cb: self.masterCommand( event, meth , evstring) )
            else:
                # g.trace('+',evstring)
                tbuffer.bind( evstring,  lambda event, meth = _cb: self.masterCommand( event, meth , evstring), '+' )
        #@nonl
        #@-node:ekr.20050724075352.113:<< define cb callback >>
        #@nl
        # EKR: create one binding for each entry in cbDict.
        for z in self.cbDict:
            cb( z )
        self.mbuffers[ tbuffer ] = label
        self.svars[ tbuffer ] = Tk.StringVar()
        #@    << define setVar callback >>
        #@+node:ekr.20050724075352.114:<< define setVar callback >>
        def setVar( event ):
            label = self.mbuffers[ event.widget ]
            svar = self.svars[ event.widget ]
            label.configure( textvariable = svar )
        #@nonl
        #@-node:ekr.20050724075352.114:<< define setVar callback >>
        #@nl
        tbuffer.bind( '<FocusIn>', setVar, '+' )
        def scrollTo( event ):
            event.widget.see( 'insert' )
        #tbuffer.bind( '<Enter>', scrollTo, '+' )
        
        # EKR: This adds a binding for all <Key> events, so _all_ key events go through masterCommand.
        cb( 'Key' )
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
    #@+node:ekr.20050724075352.137:macro methods
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
    #@-node:ekr.20050724075352.137:macro methods
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
    #@nonl
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
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.156:paragraph methods
    #@+node:ekr.20050724075352.161:kill methods
    #@+at
    # These methods add text to the killbuffer.
    #@-at
    #@@c
    
    #@+others
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
    #@nonl
    #@-node:ekr.20050724075352.164:deletelastWord
    #@+node:ekr.20050724075352.165:killsentence
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
    #@-node:ekr.20050724075352.165:killsentence
    #@+node:ekr.20050724075352.166:killRegion
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
    #@-node:ekr.20050724075352.166:killRegion
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
    def getClipboard( self, tbuffer ):
        
        ctxt = None
        try:
            ctxt = tbuffer.selection_get( selection='CLIPBOARD' )
            if ctxt != self.last_clipboard or not self.killbuffer:
                self.last_clipboard = ctxt
                if self.killbuffer and self.killbuffer[ 0 ] == ctxt:
                    return None
                return ctxt
            else:
                return None
            
        except:
            return None
            
        return None
    #@nonl
    #@-node:ekr.20050724075352.169:getClipboard
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.161:kill methods
    #@+node:ekr.20050724075352.170:register methods
    #@+at
    # These methods add things to the registers( a-z )
    # 
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.171:copyToRegister
    #self.registers = {}
    
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
    #@+node:ekr.20050724075352.173:prependToRegister
    def prependToRegister( self, event ):
        #global regMeth, registermode, controlx, registermode
        event.keysym = 'p'
        self.setNextRegister( event )
        self.mcStateManager.setState( 'controlx', False )
        #self.controlx = True
    #@nonl
    #@-node:ekr.20050724075352.173:prependToRegister
    #@+node:ekr.20050724075352.174:appendToRegister
    def appendToRegister( self, event ):
        #global regMeth, registermode, controlx
        event.keysym = 'a'
        self.setNextRegister( event )
        self.mcStateManager.setState( 'controlx', True )
        #self.controlx = True
    #@nonl
    #@-node:ekr.20050724075352.174:appendToRegister
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
    #@+node:ekr.20050724075352.183:invalidRegister
    def invalidRegister( self, event, what ):
        self.deactivateRegister( event )
        svar, label = self.getSvarLabel( event )
        svar.set( 'Register does not contain valid %s'  % what)
        return
    #@nonl
    #@-node:ekr.20050724075352.183:invalidRegister
    #@+node:ekr.20050724075352.184:setNextRegister
    def setNextRegister( self, event ):
        #global regMeth, registermode
        if event.keysym == 'Shift':
            return
        if self.regMeths.has_key( event.keysym ):
            self.mcStateManager.setState( 'controlx', True )
            self.regMeth = self.regMeths[ event.keysym ]
            self.registermode = 2
            svar = self.svars[ event.widget ]
            svar.set( self.regText[ event.keysym ] )
            return
        self.stopControlX( event )
    #@nonl
    #@-node:ekr.20050724075352.184:setNextRegister
    #@+node:ekr.20050724075352.185:executeRegister
    def executeRegister( self, event ):
        self.regMeth( event )
        if self.registermode: 
            self.stopControlX( event )
        return
    #@nonl
    #@-node:ekr.20050724075352.185:executeRegister
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
    #@-node:ekr.20050724075352.170:register methods
    #@+node:ekr.20050724075352.188:abbreviation methods
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
    # 
    # 
    # 
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.189:abbreviationDispatch
    #self.abbrevMode = False
    #self.abbrevOn = False
    #self.abbrevs = {}
    def abbreviationDispatch( self, event, which ):
        #global abbrevMode
        #if not self.abbrevMode:
        aM = self.mcStateManager.getState( 'abbrevMode' )
        if not aM:
            #self.abbrevMode = which
            self.mcStateManager.setState( 'abbrevMode', which )
            svar, label = self.getSvarLabel( event )
            svar.set( '' )
            self.setLabelBlue( label )
            return 'break'
        if aM:
            self.abbrevCommand1( event )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.189:abbreviationDispatch
    #@+node:ekr.20050724075352.190:abbrevCommand1
    def abbrevCommand1( self, event ):
        #global abbrevMode
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
            #self.abbrevMode = False
            #self.mcStateManager.setState( 'abbrevMode', False )
            self.keyboardQuit( event )
            self.resetMiniBuffer( event )
            return 'break'
        svar, label = self.getSvarLabel( event )
        self.setSvar( event, svar )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.190:abbrevCommand1
    #@+node:ekr.20050724075352.191:expandAbbrev
    def expandAbbrev( self,event ):
        tbuffer = event.widget
        word = tbuffer.get( 'insert -1c wordstart', 'insert -1c wordend' )
        c = event.char.strip()
        if c: #We have to do this because this method is called from Alt-x and Control-x, we get two differnt types of data and tbuffer states.
            word = '%s%s' %( word, event.char )
        if self.abbrevs.has_key( word ):
            tbuffer.delete( 'insert -1c wordstart', 'insert -1c wordend' )
            tbuffer.insert( 'insert', self.abbrevs[ word ] ) 
            return self._tailEnd( tbuffer )
            #return True
        else: return False
    #@nonl
    #@-node:ekr.20050724075352.191:expandAbbrev
    #@+node:ekr.20050724075352.192:regionalExpandAbbrev
    #self.regXRpl = None
    #self.regXKey = None
    def regionalExpandAbbrev( self, event ):
        #global regXRpl
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
        self.regXRpl = searchXR( i1, i2, ins, event)
        self.regXRpl.next() # Call it the first time.
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.192:regionalExpandAbbrev
    #@+node:ekr.20050724075352.194:_setRAvars
    def _setRAvars( self ):
        #global regXRpl, regXKey
        self.regXRpl = self.regXKey = None
    #@nonl
    #@-node:ekr.20050724075352.194:_setRAvars
    #@+node:ekr.20050724075352.195:killAllAbbrevs
    def killAllAbbrevs( self, event ):
        #global abbrevs
        self.abbrevs = {}
        return self.keyboardQuit( event )
    #@nonl
    #@-node:ekr.20050724075352.195:killAllAbbrevs
    #@+node:ekr.20050724075352.196:toggleAbbrevMode
    def toggleAbbrevMode( self, event ):
        #global abbrevOn
        #aO = self.mcStateManager.getState( 'abbrevOn' )
        svar, label = self.getSvarLabel( event )
        if self.abbrevOn:
            self.abbrevOn = False
            self.keyboardQuit( event )
            svar.set( "Abbreviations are Off" )  
            #self.mcStateManager.setState( 'abbrevOn', False ) #This doesnt work too well with the mcStateManager
        else:
            self.abbrevOn = True
            self.keyboardQuit( event )
            svar.set( "Abbreviations are On" )
            #self.mcStateManager.setState( 'abbrevOn', True )
    #@nonl
    #@-node:ekr.20050724075352.196:toggleAbbrevMode
    #@+node:ekr.20050724075352.197:listAbbrevs
    def listAbbrevs( self, event ):
        svar, label = self.getSvarLabel( event )
        txt = ''
        for z in self.abbrevs:
            txt = '%s%s=%s\n' %( txt, z, self.abbrevs[ z ] )
        svar.set( '' )
        svar.set( txt )
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.197:listAbbrevs
    #@+node:ekr.20050724075352.198:readAbbreviations
    def readAbbreviations( self, event ):
        import tkFileDialog
        f = tkFileDialog.askopenfile()
        if f == None: return 'break'        
        return self._readAbbrevs( f )
    #@nonl
    #@-node:ekr.20050724075352.198:readAbbreviations
    #@+node:ekr.20050724075352.199:_readAbbrevs
    def _readAbbrevs( self, f ):
        for x in f:
            a, b = x.split( '=' )
            b = b[ : -1 ]
            self.abbrevs[ a ] = b
        f.close()        
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.199:_readAbbrevs
    #@+node:ekr.20050724075352.200:writeAbbreviations
    def writeAbbreviations( self, event ):
        import tkFileDialog
        f = tkFileDialog.asksaveasfile() 
        if f == None: return 'break' 
        return self._writeAbbrevs( f )
    #@nonl
    #@-node:ekr.20050724075352.200:writeAbbreviations
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
    #@-node:ekr.20050724075352.188:abbreviation methods
    #@+node:ekr.20050724075352.202:paragraph methods
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
    #@-node:ekr.20050724075352.202:paragraph methods
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
    #@+node:ekr.20050724075352.221:searching
    #@+at
    # A tremendous variety of searching methods are available.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050724075352.222:incremental search methods
    #@+at
    # These methods enable the incremental search functionality.
    # 
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.223:startIncremental
    def startIncremental( self, event, stroke, which='normal' ):
        #global isearch, pref
        #widget = event.widget
        #if self.isearch:
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
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.222:incremental search methods
    #@+node:ekr.20050724075352.228:non-incremental search methods
    #@+at
    # Accessed by Control-s Enter or Control-r Enter.  Alt-x forward-search or 
    # backward-search, just looks for words...
    # 
    # 
    #@-at
    #@@c
    
    
    #@+others
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
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.228:non-incremental search methods
    #@+node:ekr.20050724075352.231:word search methods
    #@+at
    # 
    # Control-s(r) Enter Control-w words Enter, pattern entered is treated as 
    # a regular expression.
    # 
    # for example in the buffer we see:
    #     cats......................dogs
    # if we are after this and we enter the backwards look, search for 'cats 
    # dogs' if will take us to the match.
    # 
    #@-at
    #@@c
    
    #@+others
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
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.231:word search methods
    #@+node:ekr.20050724075352.234:re-search methods
    #@+at
    # For the re-search-backward and re-search-forward Alt-x commands
    # 
    #@-at
    #@@c
    
    
    
    #@+others
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
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.234:re-search methods
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.221:searching
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
    #@+node:ekr.20050724075352.254:query replace methods
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
    #@-node:ekr.20050724075352.254:query replace methods
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
                g.trace(aX)
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
    #@-others
#@nonl
#@-node:ekr.20050724075352.40:class Emacs
#@-node:ekr.20050724075341:From temacs
#@-others
#@nonl
#@-node:ekr.20050723062822:@thin __core_emacs.py
#@-leo
