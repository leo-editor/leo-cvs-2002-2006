#@+leo-ver=4-thin
#@+node:ekr.20050710142719:@thin leoEditCommands.py
'''Basic editor commands for Leo.

Modelled after Emacs and Vim commands.'''

#@<< imports >>
#@+node:ekr.20050710151017:<< imports >>
import leoGlobals as g

if 0:
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
    
import leoColor
import leoPlugins
    
import re  
import string
import sys
#@nonl
#@-node:ekr.20050710151017:<< imports >>
#@nl

extensions = None
commandsFromPlugins = {}

#@+others
#@+node:ekr.20050722112023:class editCommands
class editCommands:

    #@    @+others
    #@+node:ekr.20050710142746:ctor
    def __init__ (self,c):
        
        self.c = c
    
        self.mode = 'default'
        self.modeStack = []
        
        self.defaultWordChars1, self.defaultWordChars2 = self.setDefaultWordChars()
        self.wordChars1 = self.defaultWordChars1
        self.wordChars2 = self.defaultWordChars2
    
        self.setDefaultOptions()
    #@nonl
    #@-node:ekr.20050710142746:ctor
    #@+node:ekr.20050710152854:Options...
    #@+node:ekr.20050710150930.6:setDefaultOptions
    def setDefaultOptions(self):
        
        self.options = {
            'extendMovesForward':   True,  # True: moving forward may cross node boundaries.
            'extendMovesBack':      True,  # True: moving back may cross node boundaries.
            'extendFindsForward':   True,   # True: find forward may cross node boundaries.
            'extendFindsBack':      True,   # True: find back may cross node boundaries.
        }
    #@nonl
    #@-node:ekr.20050710150930.6:setDefaultOptions
    #@+node:ekr.20050710150930.7:getOption
    def getOption (self,optionName):
        
        # This may change when modes get put in.
        return self.options.get(optionName)
    #@nonl
    #@-node:ekr.20050710150930.7:getOption
    #@-node:ekr.20050710152854:Options...
    #@+node:ekr.20050710150930:Word stuff...
    #@+node:ekr.20050710150930.1:findWordStart
    def findWordStart(self,s,i):
        
        while i < len(s):
            if s[i] in self.wordChars1:
                return i
            else:
                i += 1
        return i
    #@nonl
    #@-node:ekr.20050710150930.1:findWordStart
    #@+node:ekr.20050710150930.2:insideWord
    def insideWord (self,s,i):
        
        '''Return True if the char at s[i] is inside a word but does not start the word.'''
        
        return (
            0 < i < len(s) and
            s[i] in self.wordChars2 and
            s[i-1] in self.wordChars2
        )
    #@nonl
    #@-node:ekr.20050710150930.2:insideWord
    #@+node:ekr.20050710150930.3:skipWord
    def skipWord(self,s,i):
        
        while i < len(s) and s[i] in self.wordChars2:
            i += 1
        return i
    #@nonl
    #@-node:ekr.20050710150930.3:skipWord
    #@+node:ekr.20050710150930.4:startsWord
    def startsWord (self,s,i):
        
        '''Return True if the char at s[i] is inside a word but does not start the word.'''
        
        return (
            i < len(s) and 
            s[i] in self.wordChars1 and
            (i == 0 or s[i-1] not in self.wordChars1)
        )
    #@nonl
    #@-node:ekr.20050710150930.4:startsWord
    #@+node:ekr.20050710150930.5:setDefaultWordChars
    def setDefaultWordChars (self):
        
        chars1 = '_' + string.letters
        chars2 = '_' + string.letters + string.digits
        return chars1, chars2
    #@nonl
    #@-node:ekr.20050710150930.5:setDefaultWordChars
    #@-node:ekr.20050710150930:Word stuff...
    #@+node:ekr.20050710150930.8:Cursor movement
    #@+node:ekr.20050711042819:moveBackwardChar
    def moveBackwardChar (self):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        i = b.getPythonInsertionPoint(s=s)
        i -= 1
        if i >= 0:
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesBackward'): # Recursively look for words in previous nodes.
            p = c.currentPosition().moveToThreadBack()
            while p:
                s = p.bodyString()
                if len(s) > 0:
                    c.selectPosition(p)
                    b.setPythonInsertionPoint(len(s)-1)
                    return True
                else:
                    p.moveToThreadBack()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050711042819:moveBackwardChar
    #@+node:ekr.20050711043048:moveBackwardWord (Finish)
    def moveBackwardWord (self,i=None):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        if i is None: i = b.getPythonInsertionPoint(s=s)
    
        if self.startsWord(s,i) or self.insideWord(s,i):
            i = self.findWordStart(s,i)
        i = self.findWordStart(s,i) ###
        if self.startsWord(s,i): ###
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesBackward'): # Recursively look for words in previous nodes.
            p = c.currentPosition().moveToThreadBack()
            while p:
                c.selectPosition(p)
                if self.moveBackwardWord(0):
                    return True
                p.moveToThreadBack()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050711043048:moveBackwardWord (Finish)
    #@+node:ekr.20050710152152:moveForwardChar
    def moveForwardChar (self):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        i = b.getPythonInsertionPoint(s=s)
        i += 1
        if i < len(s):
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesForward'): # Recursively look for words in following nodes.
            p = c.currentPosition().moveToThreadNext()
            while p:
                if len(p.bodyString()) > 0:
                    c.selectPosition(p)
                    b.setPythonInsertionPoint(0)
                    return True
                else:
                    p.moveToThreadNext()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050710152152:moveForwardChar
    #@+node:ekr.20050710150930.9:moveForwardWord
    def moveForwardWord (self,i=None):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        if i is None: i = b.getPythonInsertionPoint(s=s)
    
        if self.startsWord(s,i) or self.insideWord(s,i):
            i = self.skipWord(s,i)
        i = self.findWordStart(s,i)
        if self.startsWord(s,i):
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesForward'): # Recursively look for words in following nodes.
            p = c.currentPosition().moveToThreadNext()
            while p:
                c.selectPosition(p)
                if self.moveForwardWord(0):
                    return True
                p.moveToThreadNext()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050710150930.9:moveForwardWord
    #@+node:ekr.20050711091931.2:selectWord
    #@-node:ekr.20050711091931.2:selectWord
    #@+node:ekr.20050710150930.10:selectForwordWord
    def selectForwardWord (self):
        
        c = self ; b = c.frame.body ; s = b.getAllText()
    
        i = i1 = b.getPythonInsertionPoint()
        
        if i < len(s) and g.is_c_id(s[i]):
            i = g.skip_c_id(s,i+1)
        
        while i < len(s) and not g.is_c_id(s[i]):
            i += 1
            
        if i < len(s) and g.is_c_id(s[i]):
            # b.setPythonTextSelection(i1,i)
            pass ### TODO
    #@nonl
    #@-node:ekr.20050710150930.10:selectForwordWord
    #@-node:ekr.20050710150930.8:Cursor movement
    #@-others
#@nonl
#@-node:ekr.20050722112023:class editCommands
#@+node:ekr.20050722112023.1:addCommand
def addCommand(  name, command ):

    global commandsFromPlugins

    commandsFromPlugins [ name ] = command
#@nonl
#@-node:ekr.20050722112023.1:addCommand
#@+node:ekr.20050722112023.3:class leoEmacs
class leoEmacs:

    '''A class that adds Emacs derived commands and keystrokes to Leo.'''
    
    #@    << how to write an extension for leoEmacs >>
    #@+node:ekr.20050722130539:<< how to write an extension for leoEmacs >>
    #@@nocolor
    #@+at
    # An extension is defined like so:
    # 1. a function called:
    #     getCommands()
    # returns a dictionary of command names and command classes, an example:
    #     return {  "j-library": JLibrary_Loc }
    # this in turn causes an instance of the command class to be instatiated.
    # Instantiation involves passing the emacs instance to the command via
    # the costructor
    # 
    #     returned_dict[ "akey" ]( self )   #self is the emacs instance
    # 
    # the instance is then asked for new commands via a call to its 
    # 'addToAltX' method,
    # which returns a list of commands:
    #     return [ 'zoom-to-home', 'release-window' ]
    # after this the command is queried to see if it has an 'addToKeyStrokes' 
    # method.  If so
    # it is called.  This is to return keystrokes that activate the command:
    #     return [ 'Ctrl W', ]
    # all commands and keystrokes that are bound to the command object result 
    # in a call to
    # its __call__ method which should be defined like so:
    #     def __call__( self, event, command ):
    #         ....code....
    #@-at
    #@nonl
    #@-node:ekr.20050722130539:<< how to write an extension for leoEmacs >>
    #@nl

    #@    @+others
    #@+node:ekr.20050722112023.5:leoEmacs.ctor
    def __init__( self, editor, minibuffer, commandlabel, c , extracommands = None ):
        
        global extensions
        if extensions == None:
            extensions = self.lookForExtensions()
            
        self.editor = editor
        self.minibuffer = minibuffer
        self.commandlabel = commandlabel
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
    #@-node:ekr.20050722112023.5:leoEmacs.ctor
    #@+node:ekr.20050722112023.6:management listening
    #@+others
    #@+node:ekr.20050722112023.7:addCompleters
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
    #@-node:ekr.20050722112023.7:addCompleters
    #@+node:ekr.20050722112023.8:managementListener
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
    #@-node:ekr.20050722112023.8:managementListener
    #@-others
    #@nonl
    #@-node:ekr.20050722112023.6:management listening
    #@+node:ekr.20050722112023.9:lookForExtensions
    def lookForExtensions( self ):
        
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
    #@-node:ekr.20050722112023.9:lookForExtensions
    #@+node:ekr.20050722112023.10:addCompleter
    def addCompleter( self, ch, ch2 ):
        self.kcb.addCompleter( ch, ch2 )
        
    def addTabForColon( self, torf ):
        self.kcb.addTabForColon( torf )
    #@nonl
    #@-node:ekr.20050722112023.10:addCompleter
    #@+node:ekr.20050722112023.12:helper classes
    #@+others
    #@+node:ekr.20050722112023.13:stateManager
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
    #@-node:ekr.20050722112023.13:stateManager
    #@+node:ekr.20050722112023.14:KeyProcessor ( aevent.KeyListener ) 
    class KeyProcessor:  ## ( aevent.KeyListener ):
        
        '''KeyListener calls and newline analyzer.'''
    
        #@    @+others
        #@+node:ekr.20050722112023.15:__init__
        def __init__( self, emacs ):
        
            self.emacs = emacs
            self.kRconsume = False
            self.kTconsume = False
            self.completers = {}
            self.tab_for_colon = False  
            self.tab_width = g.app.config.getInt( emacs.c, "tab_width" )
        #@nonl
        #@-node:ekr.20050722112023.15:__init__
        #@+node:ekr.20050722112023.16:addCompleter
        def addCompleter( self, ch, ch2 ):
            self.completers[ ch ] = ch2
        
        def addTabForColon( self, torf ):
            self.tab_for_colon = torf
        #@nonl
        #@-node:ekr.20050722112023.16:addCompleter
        #@+node:ekr.20050722112023.17:removeCompleter
        def removeCompleter( self, ch ):
            del self.completers[ ch ]
        #@nonl
        #@-node:ekr.20050722112023.17:removeCompleter
        #@+node:ekr.20050722112023.18:keyReleased
        def keyReleased( self,event ):
            if self.kRconsume:
                self.kRconsume = False
                event.consume()
        #@nonl
        #@-node:ekr.20050722112023.18:keyReleased
        #@+node:ekr.20050722112023.19:keyTyped
        def keyTyped( self, event ):
            if self.kTconsume:
                self.kTconsume = False
                event.consume()
        #@nonl
        #@-node:ekr.20050722112023.19:keyTyped
        #@+node:ekr.20050722112023.20:keyPressed
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
        #@-node:ekr.20050722112023.20:keyPressed
        #@+node:ekr.20050722112023.21:insertPreviousLeadAndNewline -- for autoindentation on newline
        def insertPreviousLeadAndNewline( self ):
            #@    << why is this code here? >>
            #@+node:ekr.20050722112023.22:<< why is this code here? >>
            '''
            Originally this was in the leoSwingBody class.  This seemed right, it is core functionaliy.  But
            In light of SwingMacs I reconsidered where it should go.  Temacs was a plugin, SwingMacs is core.
            SwingMacs is responsible for processing key presses and such, consuming them if they are not to get
            to the DocumentModel.  By placing this method in leoSwingBody, the Key processing responsibilities get
            spread out.  Hence it makes more sense to move this method here, the responsibilites stay clearer.
            '''
            #@nonl
            #@-node:ekr.20050722112023.22:<< why is this code here? >>
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
        #@-node:ekr.20050722112023.21:insertPreviousLeadAndNewline -- for autoindentation on newline
        #@+node:ekr.20050722112023.23:calculateExtraSpaces
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
        #@-node:ekr.20050722112023.23:calculateExtraSpaces
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.14:KeyProcessor ( aevent.KeyListener ) 
    #@+node:ekr.20050722112023.24:TagMatcher ( aevent.KeyAdapter )
    class TagMatcher: ## ( aevent.KeyAdapter ):
        
        '''matches html/xml style tags.'''
        
        #@    @+others
        #@+node:ekr.20050722112314:ctor
        def __init__( self, emacs ):
        
            ### aevent.KeyAdapter.__init__( self )
            self.emacs = emacs 
            self.configureMatching()
            ### g.app.config.manager.addNotificationDef( "complete_tags", self.configureMatching )
        #@-node:ekr.20050722112314:ctor
        #@+node:ekr.20050722112314.1:configureMatching
        def configureMatching( self, notification = None, handback = None ):
            
            on = g.app.config.getBool( self.emacs.c, "complete_tags" )
            self.on = on
        #@nonl
        #@-node:ekr.20050722112314.1:configureMatching
        #@+node:ekr.20050722112314.2:keyPressed
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
        #@-node:ekr.20050722112314.2:keyPressed
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.24:TagMatcher ( aevent.KeyAdapter )
    #@+node:ekr.20050722112023.25:TabCompleter
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
    #@-node:ekr.20050722112023.25:TabCompleter
    #@-others
    #@nonl
    #@-node:ekr.20050722112023.12:helper classes
    #@+node:ekr.20050722112023.26:Strategy stuff...
    #@+node:ekr.20050722112023.27:defineStrategyObjects
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
    #@-node:ekr.20050722112023.27:defineStrategyObjects
    #@+node:ekr.20050722112023.28:defineStrategiesForKeystrokes
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
    #@-node:ekr.20050722112023.28:defineStrategiesForKeystrokes
    #@+node:ekr.20050722112023.29:addCommands
    def addCommands( self, command, commands ):
        
        xcommand = self.strategyObjects[ 'xcommand' ]
    
        for z in commands:
            xcommand.commands[ z ] = command
            xcommand.keys.append( z )
    
        self.strategyObjects[ command.getName() ] = command
    #@nonl
    #@-node:ekr.20050722112023.29:addCommands
    #@-node:ekr.20050722112023.26:Strategy stuff...
    #@+node:ekr.20050722112023.30:masterCommand -- all processing goes through here
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
    #@-node:ekr.20050722112023.30:masterCommand -- all processing goes through here
    #@+node:ekr.20050722112023.31:setCommandText
    def setCommandText( self, txt ):
        
        self.commandlabel.setText( txt )
    #@nonl
    #@-node:ekr.20050722112023.31:setCommandText
    #@+node:ekr.20050722112023.32:help
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
    #@-node:ekr.20050722112023.32:help
    #@+node:ekr.20050722112023.33:add*Help
    def addCommandHelp( self, chelp ):
    
        self.command_help.append( chelp )
        
    def addKeyStrokeHelp( self, kshelp ):
        
        self.keystroke_help.append( kshelp )
    #@nonl
    #@-node:ekr.20050722112023.33:add*Help
    #@+node:ekr.20050722112023.34:keyboardQuit
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
    #@-node:ekr.20050722112023.34:keyboardQuit
    #@+node:ekr.20050722112023.35:beep
    def beep( self ):
        
        tk = awt.Toolkit.getDefaultToolkit()
        tk.beep()
    #@nonl
    #@-node:ekr.20050722112023.35:beep
    #@+node:ekr.20050722112023.36:determineLanguage
    def determineLanguage( self ):
        
        pos = self.c.currentPosition()
        language = g.scanForAtLanguage( self.c, pos )
        return language
    #@nonl
    #@-node:ekr.20050722112023.36:determineLanguage
    #@+node:ekr.20050722112023.37:getTabWidth
    def getTabWidth( self ):
        
        return abs( self.c.tab_width )
    #@nonl
    #@-node:ekr.20050722112023.37:getTabWidth
    #@+node:ekr.20050722112023.38:eventToMinibuffer
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
    #@-node:ekr.20050722112023.38:eventToMinibuffer
    #@+node:ekr.20050722112023.39:text operations
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
    #@-node:ekr.20050722112023.39:text operations
    #@+node:ekr.20050722112023.40:word operations
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
    #@-node:ekr.20050722112023.40:word operations
    #@+node:ekr.20050722112023.41:findPre
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
    #@-node:ekr.20050722112023.41:findPre
    #@+node:ekr.20050722112023.42:attribute and highlight operations
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
    #@-node:ekr.20050722112023.42:attribute and highlight operations
    #@+node:ekr.20050722112023.43:addToKillBuffer
    def addToKillbuffer( self, text ):
        
        self.strategyObjects[ 'killbuffer' ].insertIntoKillbuffer( text )
    #@nonl
    #@-node:ekr.20050722112023.43:addToKillBuffer
    #@+node:ekr.20050722112023.44:Stategies for keystroke and commands
    #@<< about the strategy pattern >>
    #@+node:ekr.20050722131055:<< about the strategy pattern >>
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
    # 2. Changes to the processing methods no longer has global consequences.  
    # It is conceivable that a different Strategy could
    # be swapped in by configuration or some other means.  All a strategy has 
    # to do is implement the __call__ operator to have
    # the event and keystroke passed into it.
    # 
    # This design is based off of the lessons learned in the temacs plugin for 
    # CPython Leo.  Its evolution followed this pattern:
    # 1. It started as a flat function based module.  Though a useful learning 
    # experiment this grew too large and became
    # hard to think about.  Changes were becoming difficult.
    # 
    # 2. At this point it became apparent that more structure was needed.  It 
    # was refactored( in Refactoring this is a 'Big Refactoring')
    # into a class, with some helper classes.  This eased the ability to 
    # reason about and modify the code.
    # 
    # 3. After working with this big class, it became apparent again that a 
    # further restructuring was needed.  The idea of breaking
    # the methods that were grouped under one rubric into further classes 
    # arose; the Strategy pattern seemed to be what was called for.
    # And here we are in SwingMacs making the first cut at this new decomposed 
    # design for the Jython port.
    #@-at
    #@nonl
    #@-node:ekr.20050722131055:<< about the strategy pattern >>
    #@nl
    
    #@+others
    #@+node:ekr.20050722112023.45:incremental search
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
        #@+node:ekr.20050722112023.46:startIncremental
        def startIncremental( self, command ):
        
            if command == 'Ctrl S':
                self.iway = 'forward'
            else:
                self.iway = 'backward'
            self.emacs._stateManager.setState( 'incremental' )  
            self.emacs.setCommandText( "I-Search:" )
        #@nonl
        #@-node:ekr.20050722112023.46:startIncremental
        #@+node:ekr.20050722112023.47:incrementalSearch
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
        #@-node:ekr.20050722112023.47:incrementalSearch
        #@+node:ekr.20050722112023.48:forward/backwardSearch
        def forwardSearch( self, pos, txt, stxt ):
            
            _stxt = stxt[ pos : ]
            return _stxt.find( txt )
        
        def backwardSearch( self, pos, txt, stxt ):
        
            end = len( stxt ) - pos
            if end != 0:
                stxt = stxt[ : -end ]
        
            return stxt.rfind( txt )
        #@nonl
        #@-node:ekr.20050722112023.48:forward/backwardSearch
        #@+node:ekr.20050722112023.49:class deferedHighlight ( java.lang.Runnable )
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
        #@-node:ekr.20050722112023.49:class deferedHighlight ( java.lang.Runnable )
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.45:incremental search
    #@+node:ekr.20050722112023.50:dynamic-abbrevs
    class dynamicabbrevs:
        
        #@    @+others
        #@+node:ekr.20050722115854:ctor
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
        #@-node:ekr.20050722115854:ctor
        #@+node:ekr.20050722115854.1:__call__
        def __call__( self, event, command ):
        
            if command == 'Alt Slash':
                self.dynamicExpansion( event )
            if command == 'Ctrl+Alt Slash':
                self.dynamicExpansion2( event )
        #@nonl
        #@-node:ekr.20050722115854.1:__call__
        #@+node:ekr.20050722112023.51:dynamicExpansion
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
        #@-node:ekr.20050722112023.51:dynamicExpansion
        #@+node:ekr.20050722112023.52:dynamicExpansion2
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
        #@-node:ekr.20050722112023.52:dynamicExpansion2
        #@+node:ekr.20050722112023.53:getDynamicList
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
        #              if not word.startswith( txt ) or word == txt: continue 
        # #dont need words that dont match or == the pattern
        #              if word not in rlist:
        #                  rlist.append( word )
        #              else:
        #                  rlist.remove( word )
        #                  rlist.append( word )
        #@-at
        #@nonl
        #@-node:ekr.20050722112023.53:getDynamicList
        #@+node:ekr.20050722112023.54:clearDynamic
        def clearDynamic( self, tag  ):
        
            self.emacs.clearAttribute( tag )
            self.returnlist = []
            self.searchtext = None
            self.ind = None
        #@nonl
        #@-node:ekr.20050722112023.54:clearDynamic
        #@+node:ekr.20050722112023.55:createDynamicList
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
        #@-node:ekr.20050722112023.55:createDynamicList
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.50:dynamic-abbrevs
    #@+node:ekr.20050722112023.56:symbolcompletion
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
    #@-node:ekr.20050722112023.56:symbolcompletion
    #@+node:ekr.20050722112023.57:formatter
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
        #@+node:ekr.20050722112023.58:indent-region
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
        #@-node:ekr.20050722112023.58:indent-region
        #@+node:ekr.20050722112023.59:indent-rigidly
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
        #@-node:ekr.20050722112023.59:indent-rigidly
        #@+node:ekr.20050722112023.60:indent-relative
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
        #@-node:ekr.20050722112023.60:indent-relative
        #@+node:ekr.20050722112023.61:deleteSurroundingSpaces
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
        #@-node:ekr.20050722112023.61:deleteSurroundingSpaces
        #@+node:ekr.20050722112023.62:joinLineToPrevious
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
        #@-node:ekr.20050722112023.62:joinLineToPrevious
        #@+node:ekr.20050722112023.63:deleteBlankLines
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
        #@-node:ekr.20050722112023.63:deleteBlankLines
        #@+node:ekr.20050722112023.64:definePreviousLine
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
        #@-node:ekr.20050722112023.64:definePreviousLine
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.57:formatter
    #@+node:ekr.20050722112023.65:killbuffer
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
        #@+node:ekr.20050722112023.66:kill
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
        #@-node:ekr.20050722112023.66:kill
        #@+node:ekr.20050722112023.67:insertIntoKillbuffer
        def insertIntoKillbuffer( self, txt ):
            
            self.killbuffer.insert( 0, txt )
            self.reset = True
        #@nonl
        #@-node:ekr.20050722112023.67:insertIntoKillbuffer
        #@+node:ekr.20050722112023.68:killToEndOfLine
        def killToEndOfLine( self ):
            
            editor = self.emacs.editor
            pos = editor.getCaretPosition()
            end = stext.Utilities.getRowEnd( editor, pos )
            self.kill( pos, end  )    
            return True
        #@nonl
        #@-node:ekr.20050722112023.68:killToEndOfLine
        #@+node:ekr.20050722112023.69:copyRegion
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
        #@-node:ekr.20050722112023.69:copyRegion
        #@+node:ekr.20050722112023.70:killRegion
        def killRegion( self ):
            
            region = self.getRegion()
            if region:
                self.kill( *region )
            return True
        #@nonl
        #@-node:ekr.20050722112023.70:killRegion
        #@+node:ekr.20050722112023.71:getRegion
        def getRegion( self ):
        
            editor = self.emacs.editor
            start = editor.getSelectionStart()
            end = editor.getSelectionEnd()
            if end == start: return None
            else:
                return start, end
        #@nonl
        #@-node:ekr.20050722112023.71:getRegion
        #@+node:ekr.20050722112023.72:walkKB
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
        #@-node:ekr.20050722112023.72:walkKB
        #@+node:ekr.20050722112023.73:yank
        def yank( self ):
            self.reset = True
            return self.walkKB()
        #@nonl
        #@-node:ekr.20050722112023.73:yank
        #@+node:ekr.20050722112023.74:iterateKillBuffer
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
        #@-node:ekr.20050722112023.74:iterateKillBuffer
        #@+node:ekr.20050722112023.75:doesClipboardOfferNewData
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
        #@-node:ekr.20050722112023.75:doesClipboardOfferNewData
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.65:killbuffer
    #@+node:ekr.20050722112023.76:deleter
    class deleter:
        
        def __init__( self, emacs ):
            self.emacs = emacs
            
        def __call__( self, event, command ):
            if command == 'Delete':
                return self.deletePreviousChar()
            if command == 'Ctrl D':
                return self.deleteNextChar()
                
        #@    @+others
        #@+node:ekr.20050722112023.77:deletePreviousChar
        def deletePreviousChar( self ):
            
            editor = self.emacs.editor
            pos = editor.getCaretPosition()
            if pos != 0:
                doc = editor.getStyledDocument()
                spos = pos -1
                doc.replace( spos, 1 , "", None )
            return True
        #@nonl
        #@-node:ekr.20050722112023.77:deletePreviousChar
        #@+node:ekr.20050722112023.78:deleteNextChar
        def deleteNextChar( self ):
            
            editor = self.emacs.editor
            pos = editor.getCaretPosition()
            doc = editor.getStyledDocument()
            if pos != doc.getLength():
                doc.replace( pos, 1 , "", None )
            return True
        #@nonl
        #@-node:ekr.20050722112023.78:deleteNextChar
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.76:deleter
    #@+node:ekr.20050722112023.79:alt_x_handler
    class alt_x_handler:
        
        #@    @+others
        #@+node:ekr.20050722114622: __call__
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
        #@-node:ekr.20050722114622: __call__
        #@+node:ekr.20050722114622.1: ctor
        def __init__( self, emacs ):
            self.emacs = emacs
            self.defineCommands()
            self.last_command = None
            self.keys = []
        #@-node:ekr.20050722114622.1: ctor
        #@+node:ekr.20050722114622.2:createTabCompleter
        def createTabCompleter( self ):
        
            self.keys = self.commands.keys()
            self.tbCompleter = self.emacs.TabCompleter( self.keys )
        #@nonl
        #@-node:ekr.20050722114622.2:createTabCompleter
        #@+node:ekr.20050722114622.3:defineCommands
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
        #@-node:ekr.20050722114622.3:defineCommands
        #@+node:ekr.20050722114622.4:execute
        def execute( self, event, command ):
            
            txt = self.emacs.minibuffer.getText()
            if self.commands.has_key( txt ):
                return self.commands[ txt ]( event, txt )
            else:
                self.emacs.keyboardQuit( event )
                self.emacs.setCommandText( "Command Not Defined" )
        #@nonl
        #@-node:ekr.20050722114622.4:execute
        #@+node:ekr.20050722112023.80:getCommandHelp
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
        #@-node:ekr.20050722112023.80:getCommandHelp
        #@-others
    #@-node:ekr.20050722112023.79:alt_x_handler
    #@+node:ekr.20050722112023.81:ctrl_x_handler
    class ctrl_x_handler:
        
        #@    @+others
        #@+node:ekr.20050722114622.5: ctor
        def __init__( self, emacs ):
        
            self.emacs = emacs
            self.defineCommands()
            self.last_command = None
            self.keys = []
        #@nonl
        #@-node:ekr.20050722114622.5: ctor
        #@+node:ekr.20050722114622.6:defineCommands
        def defineCommands( self ):
            
            sO = self.emacs.strategyObjects
        
            self.commands = {
                'Ctrl O': sO[ 'formatter' ],
            }
        #@nonl
        #@-node:ekr.20050722114622.6:defineCommands
        #@+node:ekr.20050722114622.7: __call__
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
        #@-node:ekr.20050722114622.7: __call__
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.81:ctrl_x_handler
    #@+node:ekr.20050722112023.82:ctrl_u handler
    class ctrl_u_handler:
        
        #@    @+others
        #@+node:ekr.20050722114847:ctor
        def __init__( self, emacs ):
            
            self.emacs = emacs
            self.defineCommands()
            self.last_command = None
            self.keys = []
        #@nonl
        #@-node:ekr.20050722114847:ctor
        #@+node:ekr.20050722114847.1:defineCommands
        def defineCommands( self ):
            
            sO = self.emacs.strategyObjects
            
            self.commands = {
                'Alt Period': sO[ 'tags' ],
            }
            
        #@nonl
        #@-node:ekr.20050722114847.1:defineCommands
        #@+node:ekr.20050722114847.2: __call__
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
        #@-node:ekr.20050722114847.2: __call__
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.82:ctrl_u handler
    #@+node:ekr.20050722112023.83:rectangles
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
        #@+node:ekr.20050722112023.84:definePoints
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
        #@-node:ekr.20050722112023.84:definePoints
        #@+node:ekr.20050722112023.85:insertText
        def insertText( self, rl_start, end, ntxt ):
         
            sd = self.emacs.editor.getStyledDocument()
            sd.remove( rl_start, end - rl_start )
            sd.insertString( rl_start, ntxt, None ) 
            return True
        #@nonl
        #@-node:ekr.20050722112023.85:insertText
        #@+node:ekr.20050722112023.86:open-rectangle
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
        #@-node:ekr.20050722112023.86:open-rectangle
        #@+node:ekr.20050722112023.87:clear-rectangle
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
        #@-node:ekr.20050722112023.87:clear-rectangle
        #@+node:ekr.20050722112023.88:kill-rectangle
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
        #@-node:ekr.20050722112023.88:kill-rectangle
        #@+node:ekr.20050722112023.89:yank-rectangle
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
        #@-node:ekr.20050722112023.89:yank-rectangle
        #@+node:ekr.20050722112023.90:delete-rectangle
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
        #@-node:ekr.20050722112023.90:delete-rectangle
        #@+node:ekr.20050722112023.91:delete-whitespace-rectangle
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
        #@-node:ekr.20050722112023.91:delete-whitespace-rectangle
        #@+node:ekr.20050722112023.92:string-rectangle
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
        #@-node:ekr.20050722112023.92:string-rectangle
        #@+node:ekr.20050722112023.93:string-insert-rectangle
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
        #@-node:ekr.20050722112023.93:string-insert-rectangle
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.83:rectangles
    #@+node:ekr.20050722112023.94:zap
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
        #@+node:ekr.20050722112023.95:zap
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
        #@-node:ekr.20050722112023.95:zap
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.94:zap
    #@+node:ekr.20050722112023.96:comment
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
        #@+node:ekr.20050722112023.97:comment-region
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
        #@-node:ekr.20050722112023.97:comment-region
        #@+node:ekr.20050722112023.98:comment-kill
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
        #@-node:ekr.20050722112023.98:comment-kill
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.96:comment
    #@+node:ekr.20050722112023.99:movement
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
        #@+node:ekr.20050722112023.100:beginning-of-buffer
        def beginningOfBuffer( self ):
        
            editor = self.emacs.editor
            editor.setCaretPosition( 0 )
        #@nonl
        #@-node:ekr.20050722112023.100:beginning-of-buffer
        #@+node:ekr.20050722112023.101:end-of-buffer
        def endOfBuffer( self ):
            
            editor = self.emacs.editor
            sdoc = editor.getStyledDocument()
            editor.setCaretPosition( sdoc.getLength() -1 )
        #@nonl
        #@-node:ekr.20050722112023.101:end-of-buffer
        #@+node:ekr.20050722112023.102:beginning-of-line
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
        #@-node:ekr.20050722112023.102:beginning-of-line
        #@+node:ekr.20050722112023.103:end-of-line
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
        #@-node:ekr.20050722112023.103:end-of-line
        #@+node:ekr.20050722112023.104:goto
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
        #@-node:ekr.20050722112023.104:goto
        #@+node:ekr.20050722112023.105:gotoChar
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
        #@-node:ekr.20050722112023.105:gotoChar
        #@+node:ekr.20050722112023.106:startOfWord
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
        #@-node:ekr.20050722112023.106:startOfWord
        #@+node:ekr.20050722112023.107:endOfWord
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
        #@-node:ekr.20050722112023.107:endOfWord
        #@+node:ekr.20050722112023.108:beginning of indentation
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
        #@-node:ekr.20050722112023.108:beginning of indentation
        #@+node:ekr.20050722112023.109:isWord
        def isWordCharacter( self, c ):
            
            if c in string.ascii_letters:
                return True
            elif c in string.digits:
                return True
            elif c in ( "_"):
                return True
            return False
        #@nonl
        #@-node:ekr.20050722112023.109:isWord
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.99:movement
    #@+node:ekr.20050722112023.110:balanced parenthesis or sexp
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
        #@+node:ekr.20050722112023.111:killSexpForward and Backward
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
        #@-node:ekr.20050722112023.111:killSexpForward and Backward
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.110:balanced parenthesis or sexp
    #@+node:ekr.20050722112023.112:tags ( java.lang.Runnable )
    class tags: ## ( java.lang.Runnable ):
        
        #tags_table = {}
            
        #@    @+others
        #@+node:ekr.20050722120318: ctor
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
        #@-node:ekr.20050722120318: ctor
        #@+node:ekr.20050722120318.1:__call__
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
        #@-node:ekr.20050722120318.1:__call__
        #@+node:ekr.20050722120318.2:__defineLanguageMatchers
        def __defineLanguageMatchers( self ):
        
            if 1:  ### Not ready yet.
                pass
            else:
                reg1 = java.util.regex.Pattern.compile( java.lang.String( "^\s*(def\s+\w+\s*)" ) )
                reg2 = java.util.regex.Pattern.compile( java.lang.String(  "^\s*(class\s+\w+\s*)" ) )
                self.python_matchers = ( reg1.matcher( java.lang.String( "" ) ), reg2.matcher( java.lang.String( "" ) ) )
        #@nonl
        #@-node:ekr.20050722120318.2:__defineLanguageMatchers
        #@+node:ekr.20050722112023.113:__defineLanguageRecognizers
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
        #@-node:ekr.20050722112023.113:__defineLanguageRecognizers
        #@+node:ekr.20050722112023.115:alternativeDefinition
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
        #@-node:ekr.20050722112023.115:alternativeDefinition
        #@+node:ekr.20050722112023.122:class DeferedGotoLine
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
        #@-node:ekr.20050722112023.122:class DeferedGotoLine
        #@+node:ekr.20050722112023.117:defineTagsTable
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
        #@-node:ekr.20050722112023.117:defineTagsTable
        #@+node:ekr.20050722112023.114:gotoTag
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
        #@-node:ekr.20050722112023.114:gotoTag
        #@+node:ekr.20050722112023.116:popBack
        def popBack( self ):
        
            if self.pop_back:
                p = self.pop_back.pop()
                c = self.emacs.c
                c.beginUpdate()
                c.selectPosition( p )
                c.endUpdate()
        #@nonl
        #@-node:ekr.20050722112023.116:popBack
        #@+node:ekr.20050722112023.121:run
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
        #@-node:ekr.20050722112023.121:run
        #@+node:ekr.20050722112023.118:scanForTags
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
                #@+node:ekr.20050722112023.119:<<java>>
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
                #@-node:ekr.20050722112023.119:<<java>>
                #@nl
            else:
                return None
        #@nonl
        #@-node:ekr.20050722112023.118:scanForTags
        #@+node:ekr.20050722112023.120:valueChanged
        def valueChanged( self, *args ):
            
            values = args[ 1 ]
            self.positions.append( values[ 'new_p' ].copy() )
        #@nonl
        #@-node:ekr.20050722112023.120:valueChanged
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.112:tags ( java.lang.Runnable )
    #@+node:ekr.20050722112023.123:transpose
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
        #@+node:ekr.20050722112023.124:transpose-lines
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
        #@-node:ekr.20050722112023.124:transpose-lines
        #@+node:ekr.20050722112023.125:reverse-region
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
        #@-node:ekr.20050722112023.125:reverse-region
        #@+node:ekr.20050722112023.126:transpose-words
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
        #@-node:ekr.20050722112023.126:transpose-words
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.123:transpose
    #@+node:ekr.20050722112023.127:capitalization
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
        #@+node:ekr.20050722112023.128:capitalize-region
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
        #@-node:ekr.20050722112023.128:capitalize-region
        #@+node:ekr.20050722112023.129:upcase-region
        def upcaseRegion( self ):
            
            editor = self.emacs.editor
            stext = editor.getSelectedText()
            if stext == None:
                return "Region not selected"
                
            ntext = stext.upper()
            editor.replaceSelection( ntext )
        #@nonl
        #@-node:ekr.20050722112023.129:upcase-region
        #@+node:ekr.20050722112023.130:downcase-region
        def downcaseRegion( self ):
        
            editor = self.emacs.editor
            stext = editor.getSelectedText()
            if stext == None:
                return "Region not selected"
                
            ntext = stext.lower()
            editor.replaceSelection( ntext )
        #@nonl
        #@-node:ekr.20050722112023.130:downcase-region
        #@+node:ekr.20050722112023.131:capitalize-word
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
        #@-node:ekr.20050722112023.131:capitalize-word
        #@+node:ekr.20050722112023.132:upcase-word
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
        #@-node:ekr.20050722112023.132:upcase-word
        #@+node:ekr.20050722112023.133:downcase-word
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
        #@-node:ekr.20050722112023.133:downcase-word
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.127:capitalization
    #@+node:ekr.20050722112023.134:replacement
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
        #@+node:ekr.20050722112023.135:query-replace
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
        #@-node:ekr.20050722112023.135:query-replace
        #@+node:ekr.20050722112023.136:query-replace-regexp
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
        #@-node:ekr.20050722112023.136:query-replace-regexp
        #@+node:ekr.20050722112023.137:replace-string
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
        #@-node:ekr.20050722112023.137:replace-string
        #@+node:ekr.20050722112023.138:doReplacement
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
        #@-node:ekr.20050722112023.138:doReplacement
        #@+node:ekr.20050722112023.139:replaceAll
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
        #@-node:ekr.20050722112023.139:replaceAll
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.134:replacement
    #@+node:ekr.20050722112023.140:sorters
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
        #@+node:ekr.20050722112023.141:sort-lines
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
        #@-node:ekr.20050722112023.141:sort-lines
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.140:sorters
    #@+node:ekr.20050722112023.142:lines
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
        #@+node:ekr.20050722112023.143:keep-lines
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
        #@-node:ekr.20050722112023.143:keep-lines
        #@+node:ekr.20050722112023.144:flush-lines
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
        #@-node:ekr.20050722112023.144:flush-lines
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.142:lines
    #@+node:ekr.20050722112023.145:tabs
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
        #@+node:ekr.20050722112023.146:tabify
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
        #@-node:ekr.20050722112023.146:tabify
        #@+node:ekr.20050722112023.147:untabify
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
        #@-node:ekr.20050722112023.147:untabify
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.145:tabs
    #@+node:ekr.20050722112023.148:registers
    class registers:
        
        #@    @+others
        #@+node:ekr.20050722113219:ctor
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
        #@-node:ekr.20050722113219:ctor
        #@+node:ekr.20050722113219.1:__call__
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
        #@-node:ekr.20050722113219.1:__call__
        #@+node:ekr.20050722112023.149:copy-to-register
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
        #@-node:ekr.20050722112023.149:copy-to-register
        #@+node:ekr.20050722112023.150:insert-register
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
        #@-node:ekr.20050722112023.150:insert-register
        #@+node:ekr.20050722112023.151:append-to-register
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
        #@-node:ekr.20050722112023.151:append-to-register
        #@+node:ekr.20050722112023.152:prepend-to-register
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
        #@-node:ekr.20050722112023.152:prepend-to-register
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.148:registers
    #@+node:ekr.20050722112023.153:selection (sevent.DocumentListener)
    class selection: ## ( sevent.DocumentListener ):
        
        #@    @+others
        #@+node:ekr.20050722113038:ctor & __call__
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
        #@-node:ekr.20050722113038:ctor & __call__
        #@+node:ekr.20050722113038.2:startSelection
        def startSelection( self ):
            
            self.start = self.emacs.editor.getCaretPosition()
            self.emacs._stateManager2.setState( "selection" )
            return True
        #@nonl
        #@-node:ekr.20050722113038.2:startSelection
        #@+node:ekr.20050722113038.3:executeSelection
        def executeSelection( self ):
        
            if self.start != -1:
                editor = self.emacs.editor
                cp = editor.getCaretPosition()
                editor.setCaretPosition( self.start )
                editor.moveCaretPosition( cp )
            else:
                self.emacs.keyboardQuit()
        #@nonl
        #@-node:ekr.20050722113038.3:executeSelection
        #@+node:ekr.20050722113038.4:select
        def select( self ):
                    
            dc = DefCallable( self.executeSelection )
            ft = dc.wrappedAsFutureTask()
            java.awt.EventQueue.invokeLater( ft )
        #@nonl
        #@-node:ekr.20050722113038.4:select
        #@+node:ekr.20050722113038.5:changedUpdate
        def changedUpdate( self, event ):
            pass
        #@-node:ekr.20050722113038.5:changedUpdate
        #@+node:ekr.20050722113038.6:insertUpdate
        def insertUpdate( self, event ):
            pass
        #@-node:ekr.20050722113038.6:insertUpdate
        #@+node:ekr.20050722113038.7:removeUpdate
        def removeUpdate( self, event ):
            self.start = -1
        #@nonl
        #@-node:ekr.20050722113038.7:removeUpdate
        #@-others
    #@nonl
    #@-node:ekr.20050722112023.153:selection (sevent.DocumentListener)
    #@-others
    #@nonl
    #@-node:ekr.20050722112023.44:Stategies for keystroke and commands
    #@+node:ekr.20050722112023.154:class vi_emulation
    class vi_emulation:
        
        def __init__( self, c ):
            self.c = c
            self.mode = None
            #@        <<define vi keystrokes>>
            #@+node:ekr.20050722112023.155:<<define vi keystrokes>>
            self.vi_keystrokes = {
                'dd': self.deleteLine,
                'i': self.insert,
            }
            #@nonl
            #@-node:ekr.20050722112023.155:<<define vi keystrokes>>
            #@nl
            
        def __call__( self, event, command ):
    
            if self.mode:
                return self.mode( event, command )
            else:
                return self.vi_keystrokes[ command ]( event, command )
    #@nonl
    #@+node:ekr.20050722112023.156:cut
    def cut( self, event ):
        pass
    #@nonl
    #@-node:ekr.20050722112023.156:cut
    #@+node:ekr.20050722112023.157:deleteLine
    def deleteLine( self, event, command ):
        pass
    #@nonl
    #@-node:ekr.20050722112023.157:deleteLine
    #@+node:ekr.20050722112023.158:insert
    def insert( self, event, command ):
        pass
    #@nonl
    #@-node:ekr.20050722112023.158:insert
    #@-node:ekr.20050722112023.154:class vi_emulation
    #@-others
#@nonl
#@-node:ekr.20050722112023.3:class leoEmacs
#@-others
#@nonl
#@-node:ekr.20050710142719:@thin leoEditCommands.py
#@-leo
