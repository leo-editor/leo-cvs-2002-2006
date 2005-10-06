#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3748:@thin leoKeys.py
"""Gui-independent keystroke handling for Leo."""

#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< imports >>
#@+node:ekr.20050920094258:<< imports >>
import leoGlobals as g

import leoEditCommands
import leoNodes

Tk              = g.importExtension('Tkinter',pluginName=None,verbose=False)
tkFileDialog    = g.importExtension('tkFileDialog',pluginName=None,verbose=False)
tkFont          = g.importExtension('tkFileDialog',pluginName=None,verbose=False)

import string
#@nonl
#@-node:ekr.20050920094258:<< imports >>
#@nl

class keyHandlerClass:
    
    '''A class to support emacs-style commands.'''

    #@    << define class vars >>
    #@+node:ekr.20050924065520:<< define class vars >>
    global_killbuffer = []
        # Used only if useGlobalKillbuffer arg to Emacs ctor is True.
        # Otherwise, each Emacs instance has its own local kill buffer.
    
    global_registers = {}
        # Used only if useGlobalRegisters arg to Emacs ctor is True.
        # Otherwise each Emacs instance has its own set of registers.
    
    lossage = []
        # A case could be made for per-instance lossage, but this is not supported.
    #@nonl
    #@-node:ekr.20050924065520:<< define class vars >>
    #@nl

    #@    @+others
    #@+node:ekr.20050920085536.1: Birth
    #@+node:ekr.20050920085536.2: ctor (keyHandler)
    def __init__ (self,c,useGlobalKillbuffer=False,useGlobalRegisters=False):
        
        '''Create a key handler for c.
        c.frame.miniBufferWidget is a Tk.Label.
        
        useGlobalRegisters and useGlobalKillbuffer indicate whether to use
        global (class vars) or per-instance (ivars) for kill buffers and registers.'''
        
        self.c = c
        if not self.c.frame.miniBufferWidget:
            g.trace('no widget')
            return
            
        self.useGlobalKillbuffer = useGlobalKillbuffer
        self.useGlobalRegisters = useGlobalRegisters
    
        # Generalize...
        self.altX_prompt = 'full-command: '
        self.x_hasNumeric = ['sort-lines','sort-fields']
        self.fullCommandKey = 'Alt-x'
        self.universalArgKey = 'Control-u'
    
        #@    << define Tk ivars >>
        #@+node:ekr.20051006092617:<< define Tk ivars >>
        self.svars = {}
        self.widget  = c.frame.miniBufferWidget # A Tk Label widget.
        self.svar = Tk.StringVar()
        self.widget.configure(textvariable=self.svar)
        #@nonl
        #@-node:ekr.20051006092617:<< define Tk ivars >>
        #@nl
        #@    << define externally visible ivars >>
        #@+node:ekr.20051006092617.1:<< define externally visible ivars >>
        self.abbrevOn = False # True: abbreviations are on.
        self.arg = '' # The value returned by k.getArg.
        self.commandName = None
        self.negativeArg = False
        self.regx = g.bunch(iter=None,key=None)
        self.repeatCount = None
        self.state = g.bunch(kind=None,n=None,handler=None)
        #@nonl
        #@-node:ekr.20051006092617.1:<< define externally visible ivars >>
        #@nl
        #@    << define internal ivars >>
        #@+node:ekr.20050923213858:<< define internal ivars >>
        # Keepting track of the characters in the mini-buffer.
        self.mb_history = []
        self.mb_prefix = ''
        self.mb_tabListPrefix = ''
        self.mb_tabList = []
        self.mb_tabListIndex = -1
        self.mb_prompt = ''
        
        self.keysymHistory = []
        self.previous = []
        self.previousStroke = ''
        
        # For getArg...
        self.afterGetArgState = None
        self.argTabList = []
        #@nonl
        #@-node:ekr.20050923213858:<< define internal ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20050920085536.2: ctor (keyHandler)
    #@+node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    def finishCreate (self):
        
        # g.trace('keyHandler')
        k = self ; c = k.c
    
        self.cbDict = k.create_cbDict()
        k.setNegArgFunctions()
        k.setBufferStrokes(c.frame.bodyCtrl)
        self.abortAllModesKey = '<Control-g>' ### To do: generalize
        c.controlCommands.setShutdownHook(c.close)
        
        if 0:
            addTemacsExtensions(k)
            addTemacsAbbreviations(k)
            changeKeyStrokes(k,frame.bodyCtrl)
    
        k.setQuickCommandKeyBindings()
        k.add_ekr_altx_commands()
        
        # In c.commandsDict keys are command names, values are methods.
        # In k.inverseCommandsDict keys are methods, values are command names.
        # This is one reason we want unique method names without selector switches.
        k.inverseCommandsDict = {}
        for key in c.commandsDict.keys():
            val = c.commandsDict.get(key)
            k.inverseCommandsDict [val] = key
    #@nonl
    #@+node:ekr.20050920085536.11:add_ekr_altx_commands
    def add_ekr_altx_commands (self):
    
        #@    << define dict d of abbreviations >>
        #@+node:ekr.20050920085536.12:<< define dict d of abbreviations >>
        d = {
            'a':    'repeat-complex-command',
            'i':    'isearch-forward', 
            'ib':   'isearch-backward',      
            'ix':   'isearch-forward-regexp',
            'irx':  'isearch-backward-regexp',
            'ixr':  'isearch-backward-regexp',
            
            'r':    'replace-string',
            'rx':   'replace-regex',
        
            's':    'search-forward',
            'sb':   'search-backward',
            
            'sw':   'word-search-forward',    
            'sbw':  'word-search-backward',
            'swb':  'word-search-backward',
            
            #
            # 'a1'  'abbrev-on'
            # 'a0'  'abbrev-off'
         
            ## Don't put these in: they might conflict with other abbreviatsions.
            # 'fd':   'find-dialog',
            # 'od':   'options-dialog',
            
            # At present these would be Leo Find stuff.
            # 'f':    'find',
            # 'fr':   'find-reverse',
            # 'fx':   'find-regex',
            # 'frx':  'find-regex-reverse',
            # 'fxr':  'find-regex-reverse',
            # 'fw':   'find-word',
            # 'sf':   'set-find-text',
            # 'sr':   'set-find-replace',
            # 'ss':   'script-search',
            # 'ssr':  'script-search-reverse',
            
            ## These could be shared...
            # 'tfh':  'toggle-find-search-headline',
            # 'tfb':  'toggle-find-search-body',
            # 'tfw':  'toggle-find-word',
            # 'tfn':  'toggle-find-node-only',
            # 'tfi':  'toggle-find-ignore-case',
            # 'tfmc': 'toggle-find-mark-changes',
            # 'tfmf': 'toggle-find-mark-finds',
        }
        #@nonl
        #@-node:ekr.20050920085536.12:<< define dict d of abbreviations >>
        #@nl
    
        c = self.c
        keys = d.keys()
        keys.sort()
        for key in keys:
            val = d.get(key)
            func = c.commandsDict.get(val)
            if func:
                # g.trace(('%-4s' % key),val)
                c.commandsDict [key] = func
    #@nonl
    #@-node:ekr.20050920085536.11:add_ekr_altx_commands
    #@+node:ekr.20050920085536.16:bindKey
    def bindKey (self,w,evstring):
        
        k = self
    
        callback = k.cbDict.get(evstring)
        evstring = '<%s>' % evstring
    
        def f (event):
            # general = evstring == '<Key>'
            return k.masterCommand(event,callback,evstring)
    
        if evstring == '<Key>':
            w.bind(evstring,f,'+')
        else:
            w.bind(evstring,f)
    #@nonl
    #@-node:ekr.20050920085536.16:bindKey
    #@+node:ekr.20050920085536.13:create_cbDict (Generalize)
    def create_cbDict (self):
    
        '''Create callback dictionary for masterCommand.'''
    
        k = self ; c = k.c
        
        cbDict = {
        
        # The big ones...
            'Alt-x':            k.fullCommand,
            'Alt-c':            k.quickCommand, # Control keys conflict with XP cut/copy/paste.
                # Alt-c is usually bound to capitalizeWord.
            'Control-g':        k.keyboardQuit,
            'Control-u':        k.universalArgument,
            'Alt-minus':        k.negativeArgument,
            'Alt-exclam':       c.controlCommands.shellCommand,
            'Alt-bar':          c.controlCommands.shellCommandOnRegion,
            #'Control-z':        c.controlCommands.suspend,
    
        # Standard Emacs moves...
            'Alt-less':         c.editCommands.beginningOfBuffer,
            'Alt-greater':      c.editCommands.endOfBuffer,
            'Alt-a':            c.editCommands.backSentence,
            'Alt-e':            c.editCommands.forwardSentence,
            'Alt-f':            c.editCommands.forwardWord,
            'Alt-b':            c.editCommands.backwardWord,
            'Alt-braceright':   c.editCommands.moveParagraphRight,
            'Alt-braceleft':    c.editCommands.moveParagraphLeft,
            'Control-Right':    c.editCommands.forwardWord,
            'Control-Left':     c.editCommands.backwardWord,
            'Control-a':        c.editCommands.beginningOfLine,
            'Control-e':        c.editCommands.endOfLine,
            'Control-p':        c.editCommands.prevLine,
            'Control-n':        c.editCommands.nextLine,
            # 'Control-f':      c.editCommands.forwardCharacter, # Conflicts with Find panel.
            'Control-b':        c.editCommands.backCharacter,
            #'Alt-Up':          c.editCommands.lineStart,   # Conflicts with Leo outline moves.
            #'Alt-Down':        c.editCommands.lineEnd,     # Conflicts with Leo outline moves.
            # 'Control-v':      c.editCommands.scrollDown,
            # 'Alt-v':          c.editCommands.scrollUp,
        
        # Kill buffer...
            'Control-k':        c.killBufferCommands.killLine,
            'Alt-d':            c.killBufferCommands.killWord,
            'Alt-Delete':       c.killBufferCommands.backwardKillWord,
            "Alt-k":            c.killBufferCommands.killSentence,
            'Control-y':        c.killBufferCommands.yank,
            'Alt-y':            c.killBufferCommands.yankPop,
            # 'Control-w':      c.killBufferCommands.killRegion,
            # 'Alt-w':          c.killBufferCommands.killRegionSave,
        
        # Simple inserts & deletes...
            # 'Control-o':    c.editCommands.insertNewLine,
            # 'Control-d':      c.editCommands.deleteNextChar,
            # 'Alt-backslash':  c.editCommands.deleteSpaces,
            # 'Delete':         c.editCommands.backwardDeleteCharacter,
            # 'Control-Alt-o':      c.editCommands.insertNewLineIndent,
            # 'Control-j':          c.editCommands.insertNewLineAndTab,
        
        # Transpose & swap.
            # 'Alt-c':          c.editCommands.capitalizeWord,
            # 'Alt-u':          c.editCommands.upCaseWord,
            # 'Alt-l':          c.editCommands.downCaseWord,
            # 'Alt-t':          c.editCommands.transposeWords,
            # 'Control-t':      c.editCommands.swapCharacters,
        
        # Region, Paragraph, indent, & formatting.
            # 'Control-Shift-at':       c.editCommands.setRegion,
            # 'Alt-Control-backslash':  c.editCommands.indentRegion,
            # 'Alt-m':                  c.editCommands.backToIndentation,
            # 'Alt-asciicircum':        c.editCommands.deleteIndentation,
            # 'Alt-s':                  c.editCommands.centerLine,
            # 'Alt-q':                  c.editCommands.fillParagraph,
            # 'Alt-h':                  c.editCommands.selectParagraph,
            # 'Alt-equal':              c.editCommands.countRegion,
            # 'Alt-semicolon':          c.editCommands.indentToCommentColumn,
            
        # Parens.
            # 'Alt-parenleft':      c.editCommands.insertParentheses,
            # 'Alt-parenright':     c.editCommands.movePastClose,
            
        # Misc.
            # 'Control-s':          None,
            # 'Control-r':          None,
            # 'Control-l':          None,
            # 'Alt-z':              None,
            # 'Control-i':          None,
            # 'Alt-g':              None,
            # 'Alt-percent':        None,
            # 'Control-c':          None,
            # 'Control-Alt-w':      None,
            # 'Alt-slash':          c.editCommands.dynamicExpansion,
            # 'Control-Alt-slash':  c.editCommands.dynamicExpansion2,
            # 'Escape':             c.editCommands.watchEscape,
            # 'Alt-colon':          c.editCommands.startEvaluate,
            # 'Control-underscore': c.undoer.undo,
    
        # Searches.
            # 'Control-Alt-s':      c.searchCommands.isearchForwardRegexp,
            # 'Control-Alt-r':      c.searchCommands.isearchBackwardRegexp,
            # 'Control-Alt-percent': c.searchCommands.queryReplaceRegex,
    
        # Numbered commands: conflict with Leo's Expand to level commands, but so what...
            'Alt-0': k.numberCommand0,
            'Alt-1': k.numberCommand1,
            'Alt-2': k.numberCommand2,
            'Alt-3': k.numberCommand3,
            'Alt-4': k.numberCommand4,
            'Alt-5': k.numberCommand5,
            'Alt-6': k.numberCommand6,
            'Alt-7': k.numberCommand7,
            'Alt-8': k.numberCommand8,
            'Alt-9': k.numberCommand9,
        }
    
        return cbDict
    #@nonl
    #@-node:ekr.20050920085536.13:create_cbDict (Generalize)
    #@+node:ekr.20050920085536.17:setBufferStrokes
    def setBufferStrokes (self,w):
    
        '''Sets key bindings for Tk Text widget w.'''
        
        k = self
    
        # Create one binding for each entry in cbDict.
        for key in k.cbDict:
            k.bindKey(w,key)
    
        # Add a binding for <Key> events, so _all_ key events go through masterCommand.
        k.bindKey(w,'Key')
    #@nonl
    #@-node:ekr.20050920085536.17:setBufferStrokes
    #@+node:ekr.20050923214044:setNegArgFunctions (Generalize)
    def setNegArgFunctions (self):
    
        c = self.c
    
        self.negArgFunctions = {
            '<Alt-c>': c.editCommands.changePreviousWord,
            '<Alt-u>': c.editCommands.changePreviousWord,
            '<Alt-l>': c.editCommands.changePreviousWord,
        }
    #@nonl
    #@-node:ekr.20050923214044:setNegArgFunctions (Generalize)
    #@+node:ekr.20050923174229.1:setQuickCommandKeyBindings
    def setQuickCommandKeyBindings (self):
        
        '''Define the bindings used in quick-command mode.'''
        
        k = self ; c = k.c
        
        self.keystrokeFunctionDict = {
            '<Control-s>':      (2, c.searchCommands.startIncremental),
            '<Control-r>':      (2, c.searchCommands.startIncremental),
            '<Alt-g>':          (1, c.editCommands.gotoLine),
            '<Alt-z>':          (1, c.killBufferCommands.zapToCharacter),
            '<Alt-percent>':    (1, c.queryReplaceCommands.queryReplace),
            '<Control-Alt-w>':  (1, lambda event: 'break'),
        }
    
        self.abbreviationFuncDict = {
            'a':    c.abbrevCommands.addAbbreviation,
            'a i':  c.abbrevCommands.addInverseAbbreviation,
        }
        
        self.rCommandDict = {
            'space':    c.registerCommands.pointToRegister,
            'a':        c.registerCommands.appendToRegister,
            'i':        c.registerCommands.insertRegister,
            'j':        c.registerCommands.jumpToRegister,
            'n':        c.registerCommands.numberToRegister,
            'p':        c.registerCommands.prependToRegister,
            'r':        c.rectangleCommands.enterRectangleState,
            's':        c.registerCommands.copyToRegister,
            'v':        c.registerCommands.viewRegister,
            'plus':     c.registerCommands.incrementRegister,
        }
        
        self.variety_commands = {
            # Keys are Tk keysyms.
            'period':       c.editCommands.setFillPrefix,
            'parenleft':    c.macroCommands.startKbdMacro,
            'parenright':   c.macroCommands.endKbdMacro,
            'semicolon':    c.editCommands.setCommentColumn,
            'Tab':          c.editCommands.tabIndentRegion,
            'u':            c.undoer.undo,
            'equal':        c.editCommands.lineNumber,
            'h':            c.editCommands.selectAll,
            'f':            c.editCommands.setFillColumn,
            'b':            c.bufferCommands.switchToBuffer,
            'k':            c.bufferCommands.killBuffer,
        }
        
        self.xcommands = {
            '<Control-t>':  c.editCommands.transposeLines,
            '<Control-u>':  c.editCommands.upCaseRegion,
            '<Control-l>':  c.editCommands.downCaseRegion,
            '<Control-o>':  c.editCommands.removeBlankLines,
            '<Control-i>':  c.editFileCommands.insertFile,
            '<Control-s>':  c.editFileCommands.saveFile,
            '<Control-x>':  c.editCommands.exchangePointMark,
            '<Control-c>':  c.controlCommands.shutdown,
            '<Control-b>':  c.bufferCommands.listBuffers,
            '<Control-Shift-at>': lambda event: event.widget.selection_clear(),
            '<Delete>':     c.killBufferCommands.backwardKillSentence,
        }
    #@nonl
    #@-node:ekr.20050923174229.1:setQuickCommandKeyBindings
    #@-node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    #@-node:ekr.20050920085536.1: Birth
    #@+node:ekr.20051001051355:Dispatching...
    #@+node:ekr.20051002152108:Top-level
    # These must return 'break' unless more processing is needed.
    #@nonl
    #@+node:ekr.20050920085536.65: masterCommand & helpers
    def masterCommand (self,event,func,stroke):
    
        '''This is the central dispatching method.
        All commands and keystrokes pass through here.'''
    
        # Note: the _L symbols represent *either* special key.
        k = self ; c = k.c
        special = event.keysym in ('Control_L','Alt_L','Shift_L')
        general = stroke == '<Key>'
        k.stroke = stroke
        
        # g.trace('state kind',k.getStateKind(),'stroke',stroke,'keysym',event.keysym)
    
        inserted = not special or (
            not general and (len(k.keysymHistory)==0 or k.keysymHistory[0]!=event.keysym))
    
        if inserted:
            # g.trace('general',general,event.keysym)
            #@        << add character to history >>
            #@+node:ekr.20050920085536.67:<< add character to history >>
            # Don't add multiple special characters to history.
            
            k.keysymHistory.insert(0,event.keysym)
            
            if len(event.char) > 0:
                if len(keyHandlerClass.lossage) > 99:
                    keyHandlerClass.lossage.pop()
                keyHandlerClass.lossage.insert(0,event.char)
            
            if 0: # traces
                g.trace(event.keysym,stroke)
                g.trace(k.keysymHistory)
                g.trace(keyHandlerClass.lossage)
            #@nonl
            #@-node:ekr.20050920085536.67:<< add character to history >>
            #@nl
            
        # We *must not* interfere with the global state in the macro class.
        if c.macroCommands.recordingMacro:
            done = c.macroCommands.startKbdMacro(event)
            if done: return 'break'
    
        if stroke == k.abortAllModesKey: # '<Control-g>'
            k.previousStroke = stroke
            k.clearState()
            k.keyboardQuit(event)
            k.endCommand(event,'keyboard-quit')
            return 'break'
    
        if k.inState():
            k.previousStroke = stroke
            k.callStateFunction(event) # Calls end-command.
            return 'break'
    
        if k.keystrokeFunctionDict.has_key(stroke):
            k.previousStroke = stroke
            if k.callKeystrokeFunction(event): # Calls end-command
                return 'break'
    
        if k.regx.iter:
            try:
                k.regXKey = event.keysym
                k.regx.iter.next() # EKR: next() may throw StopIteration.
            finally:
                return 'break'
    
        if k.abbrevOn:
            expanded = c.abbrevCommands.expandAbbrev(event)
            if expanded: return 'break'
    
        if func: # Func is an argument.
            commandName = k.inverseCommandsDict.get(func)
            k.previousStroke = stroke
            func(event)
            k.endCommand(event,commandName,tag='masterCommand')
            return 'break'
    
        else:
            c.frame.body.onBodyKey(event)
            return None # Not 'break'
    #@nonl
    #@+node:ekr.20050923172809.1:callStateFunction
    def callStateFunction (self,event):
        
        k = self
        
        # g.trace(k.stateKind,k.state)
        
        if k.state.kind:
            if k.state.handler:
                k.state.handler(event)
                k.endCommand(event,k.commandName,tag='callStateFunction')
            else:
                g.es_print('no state function for %s' % (k.state.kind),color='red')
    #@nonl
    #@-node:ekr.20050923172809.1:callStateFunction
    #@+node:ekr.20050923174229.3:callKeystrokeFunction
    def callKeystrokeFunction (self,event):
        
        '''Handle a quick keystroke function.
        Return the function or None.'''
        
        k = self
        numberOfArgs, func = k.keystrokeFunctionDict [k.stroke]
    
        if func:
            func(event)
            commandName = k.inverseCommandsDict.get(func)
            k.endCommand(event,commandName,tag='callKeystrokeFunction')
        
        return func
        
        
    #@nonl
    #@-node:ekr.20050923174229.3:callKeystrokeFunction
    #@-node:ekr.20050920085536.65: masterCommand & helpers
    #@+node:ekr.20050920085536.41:fullCommand (alt-x) & helper
    def fullCommand (self,event):
        
        '''Handle 'full-command' (alt-x) mode.'''
    
        k = self ; c = k.c ; state = k.getState('altx')
        keysym = (event and event.keysym) or ''
        
        if state == 0:
            k.setState('altx',1,handler=k.fullCommand) 
            k.setLabelBlue('%s' % (k.altX_prompt),protect=True)
            # Init mb_ ivars. This prevents problems with an initial backspace.
            k.mb_prompt = k.mb_tabListPrefix = k.mb_prefix = k.altX_prompt
            k.mb_tabList = [] ; k.mb_tabListIndex = -1
        elif keysym == 'Return':
            k.callAltXFunction(event)
        elif keysym == 'Tab':
            k.doTabCompletion(c.commandsDict.keys())
        elif keysym == 'BackSpace':
            k.doBackSpace()
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.mb_tabList = []
            k.updateLabel(event)
            k.mb_tabListPrefix = k.getLabel()
            # g.trace('new prefix',k.mb_tabListPrefix)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.45:callAltXFunction
    def callAltXFunction (self,event):
        
        k = self ; c = k.c ; s = k.getLabel() ; w = event.widget
        k.mb_tabList = []
        commandName = s[len(k.mb_prefix):].strip()
        func = c.commandsDict.get(commandName)
    
        # These must be done *after* getting the command.
        k.clearState()
        k.resetLabel()
    
        if func:
            if commandName != 'repeat-complex-command':
                k.mb_history.insert(0,commandName)
            # if command in k.x_hasNumeric: func(event,aX)
            func(event)
            k.endCommand(event,commandName,tag='callAltXFunction')
        else:
            k.setLabel('Command does not exist: %s' % commandName)
    #@nonl
    #@-node:ekr.20050920085536.45:callAltXFunction
    #@-node:ekr.20050920085536.41:fullCommand (alt-x) & helper
    #@+node:ekr.20050920085536.58:quickCommand  (ctrl-c) & helpers
    def quickCommand (self,event):
        
        '''Handle 'quick-command' (control-c) mode.'''
        
        k = self ; stroke = k.stroke ; state = k.getState('quick-command')
        
        if state == 0:
            k.setState('quick-command',1,handler=k.quickCommand)
            k.setLabelBlue('quick command: ',protect=True)
        else:
            k.previous.insert(0,event.keysym)
            if len(k.previous) > 10: k.previous.pop()
            
            # g.trace('stroke',stroke,event.keysym)
            if stroke == '<Key>' and event.keysym == 'r':
                k.rCommand(event)
            elif stroke in ('<Key>','<Escape>'):
                if k.processKey(event): # Weird command-specific stuff.
                    k.clearState()
            elif stroke in k.xcommands:
                k.clearState()
                k.xcommands [stroke](event)
                
            k.endCommand(event,stroke,tag='quickCommand')
            
        return 'break'
    #@nonl
    #@+node:ekr.20051004102314:rCommand
    def rCommand (self,event):
        
        k = self ; state = k.getState('r-command') ; ch = event.keysym
        if state == 0:
            k.setLabel ('quick-command r: ',protect=True)
            k.setState('r-command',1,k.rCommand)
        elif ch in ('Control_L','Alt_L','Shift_L'):
            return
        else:
            k.clearState()
            
            # g.trace(repr(ch))
            func = k.rCommandDict.get(ch)
            if func:
                k.commandName = 'quick-command r: '
                k.resetLabel()
                func(event)
            else:
                k.setLabelGrey('Unknown r command: %s' % repr(ch))
    #@nonl
    #@-node:ekr.20051004102314:rCommand
    #@+node:ekr.20050923183943.4:processKey
    def processKey (self,event):
        
        '''Handle special keys in quickCommand mode.
        Return True if we should exit quickCommand mode.'''
    
        k = self ; c = k.c ; previous = k.previous
        
        if event.keysym in ('Shift_L','Shift_R'): return
        # g.trace(event.keysym)
    
        func = k.variety_commands.get(event.keysym)
        if func:
            k.keyboardQuit(event)
            func(event)
            return True
    
        if event.keysym in ('a','i','e'):
            if k.processAbbreviation(event):
                return False # 'a e' or 'a i e' typed.
            
        if event.keysym == 'g': # Execute the abbreviation in the minibuffer.
            s = k.getLabel(ignorePrompt=True)
            if k.abbreviationFuncDict.has_key(s):
                k.clearState()
                k.keyboardQuit(event)
                k.abbreviationFuncDict [s](event)
                return True
        
        if event.keysym == 'e': # Execute the last macro.
            k.keyboardQuit(event)
            c.macroCommands.callLastKeyboardMacro(event)
            return
    
        if event.keysym == 'x' and previous [1] not in ('Control_L','Control_R'):
            event.keysym = 's'
            k.setState('quick-command',1)
            c.registerCommands.setNextRegister(event)
            return True
    
        if event.keysym == 'Escape' and len(previous) > 1 and previous [1] == 'Escape':
            k.repeatComplexCommand(event)
            return True
    #@nonl
    #@+node:ekr.20050923183943.6:processAbbreviation
    def processAbbreviation (self,event):
        
        '''Handle a e or a i e.
        Return True when the 'e' has been seen.'''
        
        k = self ; char = event.char
    
        if k.getLabel() != 'a' and event.keysym == 'a':
            k.setLabel('a')
            return False
    
        elif k.getLabel() == 'a':
    
            if char == 'i':
                k.setLabel('a i')
                return False
            elif char == 'e':
                event.char = ''
                k.expandAbbrev(event)
                return True
    #@nonl
    #@-node:ekr.20050923183943.6:processAbbreviation
    #@-node:ekr.20050923183943.4:processKey
    #@-node:ekr.20050920085536.58:quickCommand  (ctrl-c) & helpers
    #@-node:ekr.20051002152108:Top-level
    #@+node:ekr.20051001050607:endCommand
    def endCommand (self,event,commandName,tag=''):
    
        '''Make sure Leo updates the widget following a command.
        
        Never changes the minibuffer label: individual commands must do that.
        '''
    
        k = self ; c = k.c ; w = event.widget
        if c.controlCommands.shuttingdown: return
            
        # Set the best possible undoType: prefer explicit commandName to k.commandName.
        commandName = commandName or k.commandName or ''
        k.commandName = k.commandName or commandName or ''
    
        # Call onBodyWillChange only if there is a proper command name.
        if commandName:
            p = c.currentPosition()
            c.frame.body.onBodyWillChange(p,undoType=commandName,oldSel=None,oldYview=None)
            if not k.inState():
                # g.trace('commandName:',commandName,'caller:',tag)
                k.commandName = None
                leoEditCommands.initAllEditCommanders(c)
                w.focus_force()
                w.tag_delete('color')
                w.tag_delete('color1')
    
        w.update_idletasks()
    #@nonl
    #@-node:ekr.20051001050607:endCommand
    #@-node:ekr.20051001051355:Dispatching...
    #@+node:ekr.20050920085536.32:Externally visible commands
    #@+node:ekr.20050930080419:digitArgument & universalArgument
    def universalArgument (self,event):
        
        '''Begin a numeric argument for the following command.'''
        
        k = self
        k.setLabelBlue('Universal Argument: ',protect=True)
        k.universalDispatcher(event)
        
    def digitArgument (self,event):
    
        k = self
        k.setLabelBlue('Digit Argument: ',protect=True)
        k.universalDispatcher(event)
    #@nonl
    #@-node:ekr.20050930080419:digitArgument & universalArgument
    #@+node:ekr.20050920085536.68:negativeArgument (redo?)
    def negativeArgument (self,event):
    
        k = self ; state = k.getState('neg-arg')
    
        if state == 0:
            k.setLabelBlue('Negative Argument: ',protect=True)
            k.setState('neg-arg',1,k.negativeArgument)
        else:
            k.clearState()
            k.resetLabel()
            func = k.negArgFunctions.get(k.stroke)
            if func:
                func(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.68:negativeArgument (redo?)
    #@+node:ekr.20050920085536.77:numberCommand
    def numberCommand (self,event,stroke,number):
    
        k = self ; k.stroke = stroke ; w = event.widget
    
        k.universalDispatcher(event)
        w.event_generate('<Key>',keysym=number)
    
        return 'break'
    
    def numberCommand0 (self,event): return self.numberCommand (event,None,0)
    def numberCommand1 (self,event): return self.numberCommand (event,None,1)
    def numberCommand2 (self,event): return self.numberCommand (event,None,2)
    def numberCommand3 (self,event): return self.numberCommand (event,None,3)
    def numberCommand4 (self,event): return self.numberCommand (event,None,4)
    def numberCommand5 (self,event): return self.numberCommand (event,None,5)
    def numberCommand6 (self,event): return self.numberCommand (event,None,6)
    def numberCommand7 (self,event): return self.numberCommand (event,None,7)
    def numberCommand8 (self,event): return self.numberCommand (event,None,8)
    def numberCommand9 (self,event): return self.numberCommand (event,None,9)
    #@nonl
    #@-node:ekr.20050920085536.77:numberCommand
    #@+node:ekr.20050920085536.48:repeatComplexCommand & helper
    def repeatComplexCommand (self,event):
    
        k = self
    
        if k.mb_history:
            k.setState('last-altx',1,handler=k.doLastAltX)
            k.setLabelBlue("Redo: %s" % k.mb_history[0])
        return 'break'
        
    def doLastAltX (self,event):
        
        k = self ; c = k.c
    
        if event.keysym == 'Return' and k.mb_history:
            last = k.mb_history [0]
            c.commandsDict [last](event)
            return 'break'
        else:
            return k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20050920085536.48:repeatComplexCommand & helper
    #@-node:ekr.20050920085536.32:Externally visible commands
    #@+node:ekr.20050920085536.73:universalDispatcher
    def universalDispatcher (self,event):
        
        '''Handle accumulation of universal argument.'''
        
        #@    << about repeat counts >>
        #@+node:ekr.20051006083627.1:<< about repeat counts >>
        #@@nocolor
        
        #@+at  
        #@nonl
        # Any Emacs command can be given a numeric argument. Some commands 
        # interpret the
        # argument as a repetition count. For example, giving an argument of 
        # ten to the
        # key C-f (the command forward-char, move forward one character) moves 
        # forward ten
        # characters. With these commands, no argument is equivalent to an 
        # argument of
        # one. Negative arguments are allowed. Often they tell a command to 
        # move or act
        # backwards.
        # 
        # If your keyboard has a META key, the easiest way to specify a 
        # numeric argument
        # is to type digits and/or a minus sign while holding down the the 
        # META key. For
        # example,
        # 
        # M-5 C-n
        # 
        # moves down five lines. The characters Meta-1, Meta-2, and so on, as 
        # well as
        # Meta--, do this because they are keys bound to commands 
        # (digit-argument and
        # negative-argument) that are defined to contribute to an argument for 
        # the next
        # command.
        # 
        # Another way of specifying an argument is to use the C-u 
        # (universal-argument)
        # command followed by the digits of the argument. With C-u, you can 
        # type the
        # argument digits without holding down shift keys. To type a negative 
        # argument,
        # start with a minus sign. Just a minus sign normally means -1. C-u 
        # works on all
        # terminals.
        # 
        # C-u followed by a character which is neither a digit nor a minus 
        # sign has the
        # special meaning of "multiply by four". It multiplies the argument 
        # for the next
        # command by four. C-u twice multiplies it by sixteen. Thus, C-u C-u 
        # C-f moves
        # forward sixteen characters. This is a good way to move forward 
        # "fast", since it
        # moves about 1/5 of a line in the usual size screen. Other useful 
        # combinations
        # are C-u C-n, C-u C-u C-n (move down a good fraction of a screen), 
        # C-u C-u C-o
        # (make "a lot" of blank lines), and C-u C-k (kill four lines).
        # 
        # Some commands care only about whether there is an argument and not 
        # about its
        # value. For example, the command M-q (fill-paragraph) with no 
        # argument fills
        # text; with an argument, it justifies the text as well. (See section 
        # Filling
        # Text, for more information on M-q.) Just C-u is a handy way of 
        # providing an
        # argument for such commands.
        # 
        # Some commands use the value of the argument as a repeat count, but 
        # do something
        # peculiar when there is no argument. For example, the command C-k 
        # (kill-line)
        # with argument n kills n lines, including their terminating newlines. 
        # But C-k
        # with no argument is special: it kills the text up to the next 
        # newline, or, if
        # point is right at the end of the line, it kills the newline itself. 
        # Thus, two
        # C-k commands with no arguments can kill a non-blank line, just like 
        # C-k with an
        # argument of one. (See section Deletion and Killing, for more 
        # information on
        # C-k.)
        # 
        # A few commands treat a plain C-u differently from an ordinary 
        # argument. A few
        # others may treat an argument of just a minus sign differently from 
        # an argument
        # of -1. These unusual cases will be described when they come up; they 
        # are always
        # to make the individual command more convenient to use.
        #@-at
        #@nonl
        #@-node:ekr.20051006083627.1:<< about repeat counts >>
        #@nl
    
        k = self ; state = k.getState('u-arg')
    
        if state == 0:
            # The call should set the label.
            k.setState('u-arg',1,k.universalDispatcher)
            k.repeatCount = 1
        elif state == 1:
            stroke = k.stroke ; keysym = event.keysym
                # Stroke is <Key> for plain keys, <Control-u> (k.universalArgKey)
            if stroke == k.universalArgKey:
                k.repeatCount = k.repeatCount * 4
            elif stroke == '<Key>' and keysym in string.digits + '-':
                k.updateLabel(event)
            elif stroke == '<Key>' and keysym in (
                'Alt_L','Alt_R','Shift_L','Shift_R','Control_L','Control_R'):
                 # g.trace('stroke',k.stroke,'keysym',keysym)
                 k.updateLabel(event)
            else:
                # *Anything* other than C-u, '-' or a numeral is taken to be a command.
                g.trace('stroke',k.stroke,'keysym',keysym)
                val = k.getLabel(ignorePrompt=True)
                try:                n = int(val) * k.repeatCount
                except ValueError:  n = 1
                g.trace('val',repr(val),'n',n,'k.repeatCount',k.repeatCount)
                k.clearState()
                k.executeNTimes(event,n)
                k.clearState()
                k.setLabelGrey()
                if 0: # Not ready yet.
                    # This takes us to macro state.
                    # For example Control-u Control-x ( will execute the last macro and begin editing of it.
                    if stroke == '<Control-x>':
                        k.setState('uC',2,k.universalDispatcher)
                        return k.doControlU(event,stroke)
        elif state == 2:
            k.doControlU(event,stroke)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.75:executeNTimes
    def executeNTimes (self,event,n):
        
        k = self ; stroke = k.stroke ; w = event.widget
        g.trace('stroke',stroke,'keycode',event.keycode,'n',n)
    
        if stroke == k.fullCommandKey:
            for z in xrange(n):
                k.fullCommand()
        else:
            stroke = stroke.lstrip('<').rstrip('>')
            method = k.cbDict.get(stroke)
            if method:
                g.trace('method',method)
                for z in xrange(n):
                    if 1: # No need to do this: commands never alter events.
                        ev = Tk.Event()
                        ev.widget = event.widget
                        ev.keysym = event.keysym
                        ev.keycode = event.keycode
                        ev.char = event.char
                    k.masterCommand(event,method,'<%s>' % stroke)
            else:
                for z in xrange(n):
                    w.event_generate('<Key>',keycode=event.keycode,keysym=event.keysym)
    #@nonl
    #@-node:ekr.20050920085536.75:executeNTimes
    #@+node:ekr.20050920085536.76:doControlU
    def doControlU (self,event,stroke):
        
        k = self
    
        k.setLabelBlue('Control-u %s' % stroke.lstrip('<').rstrip('>'))
    
        if event.keysym == 'parenleft': # Execute the macro.
    
            k.clearState()
            k.resetLabel()
            c.macroCommands.startKbdMacro(event)
            c.macroCommands.callLastKeyboardMacro(event)
    #@nonl
    #@-node:ekr.20050920085536.76:doControlU
    #@-node:ekr.20050920085536.73:universalDispatcher
    #@+node:ekr.20051006065121:Externally visible helpers
    #@+node:ekr.20050920085536.62:getArg
    def getArg (self,event,returnKind=None,returnState=None,handler=None,prefix=None,tabList=None):
        
        '''Accumulate an argument until the user hits return (or control-g).
        Enter the given return state when done.
        The prefix is does not form the arg.  The prefix defaults to the k.getLabel().
        '''
    
        k = self ; c = k.c ; state = k.getState('getArg')
        keysym = (event and event.keysym) or ''
        # g.trace('state',state,'keysym',keysym)
        if state == 0:
            k.arg = ''
            if tabList: k.argTabList = tabList[:]
            else:       k.argTabList = []
            if 0: # Don't do this: it would add the shortcut that started the command.
                k.updateLabel(event)
            #@        << init altX vars >>
            #@+node:ekr.20050928092516:<< init altX vars >>
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.mb_tabList = []
            
            if prefix:
                k.mb_tabListPrefix = prefix
                k.mb_prefix = prefix
                k.mb_prompt = prefix
            else:
                k.mb_tabListPrefix = k.mb_prefix = k.getLabel()
                k.mb_prompt = ''
            #@nonl
            #@-node:ekr.20050928092516:<< init altX vars >>
            #@nl
            # Set the states.
            k.afterGetArgState = (returnKind,returnState,handler)
            k.setState('getArg',1,k.getArg)
        elif keysym == 'Return':
            k.arg = k.getLabel(ignorePrompt=True)
            kind,n,handler = k.afterGetArgState
            if kind: k.setState(kind,n,handler)
            if handler: handler(event)
        elif keysym == 'Tab':
            k.doTabCompletion(k.argTabList)
        elif keysym == 'BackSpace':
            k.doBackSpace()
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.mb_tabList = []
            k.updateLabel(event)
            k.mb_tabListPrefix = k.getLabel()
    
        return 'break'
    #@-node:ekr.20050920085536.62:getArg
    #@+node:ekr.20050920085536.63:keyboardQuit
    def keyboardQuit (self,event=None):
    
        '''This method clears the state and the minibuffer label.
        
        k.endCommand handles all other end-of-command chores.'''
        
        k = self ; c = k.c
    
        if c.controlCommands.shuttingdown:
            return
            
        k.clearState()
        k.resetLabel()
    #@nonl
    #@-node:ekr.20050920085536.63:keyboardQuit
    #@+node:ekr.20050920085536.64:manufactureKeyPress
    def manufactureKeyPress (self,event,keysym):
        
        '''Implement a command by passing a keypress to Tkinter.'''
    
        w = event.widget
        w.event_generate('<Key>',keysym=keysym)
        self.endCommand(event,keysym,tag='manufactureKeyPress')
        
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.64:manufactureKeyPress
    #@-node:ekr.20051006065121:Externally visible helpers
    #@+node:ekr.20050924064254:Label...
    #@+at 
    #@nonl
    # There is something dubious about tracking states separately for separate 
    # commands.
    # In fact, there is only one mini-buffer, and it has only one state.
    # OTOH, maintaining separate states makes it impossible for one command to 
    # influence another.
    #@-at
    #@nonl
    #@+node:ekr.20050920085536.39:getLabel & setLabel & protectLabel
    def getLabel (self,ignorePrompt=False):
        
        k = self ; s = k.svar.get()
        if ignorePrompt:
            return s[len(k.mb_prefix):]
        else:
            return s
    
    def setLabel (self,s,protect=False):
        
        k = self
        k.svar.set(s)
        if protect:
            k.mb_prefix = s
            
    def protectLabel (self):
        
        k = self
        k.mb_prefix = s = k.svar.get()
    #@nonl
    #@-node:ekr.20050920085536.39:getLabel & setLabel & protectLabel
    #@+node:ekr.20050920085536.35:setLabelGrey
    def setLabelGrey (self,label=None):
    
        k = self
        k.widget.configure(background='lightgrey')
        if label is not None:
            k.setLabel(label)
            
    setLabelGray = setLabelGrey
    #@nonl
    #@-node:ekr.20050920085536.35:setLabelGrey
    #@+node:ekr.20050920085536.36:setLabelBlue
    def setLabelBlue (self,label=None,protect=False):
        
        k = self
    
        k.widget.configure(background='lightblue')
    
        if label is not None:
            k.setLabel(label,protect)
    #@nonl
    #@-node:ekr.20050920085536.36:setLabelBlue
    #@+node:ekr.20050920085536.37:resetLabel
    def resetLabel (self):
        
        k = self
        k.setLabelGrey('')
        k.mb_prefix = ''
    #@nonl
    #@-node:ekr.20050920085536.37:resetLabel
    #@+node:ekr.20050920085536.38:updateLabel
    def updateLabel (self,event):
    
        '''
        Alters the StringVar svar to represent the change in the event.
        This has the effect of changing the miniBuffer contents.
    
        It mimics what would happen with the keyboard and a Text editor
        instead of plain accumalation.'''
        
        k = self ; s = k.getLabel()
        ch = (event and event.char) or ''
        # g.trace(repr(s),repr(ch))
    
        if ch == '\b': # Handle backspace.
            # Don't backspace over the prompt.
            if len(s) <= k.mb_prefix:
                return 
            elif len(s) == 1: s = ''
            else: s = s [0:-1]
        elif ch and ch not in ('\n','\r'):
            # Add the character.
            s = s + ch
        
        k.setLabel(s)
    #@nonl
    #@-node:ekr.20050920085536.38:updateLabel
    #@-node:ekr.20050924064254:Label...
    #@+node:ekr.20051002152108.1:Shared helpers
    #@+node:ekr.20050920085536.46:doBackSpace
    # Used by getArg and fullCommand.
    
    def doBackSpace (self):
    
        '''Cut back to previous prefix and update prefix.'''
    
        k = self ; s = k.mb_tabListPrefix
    
        if len(s) > len(k.mb_prefix):
            k.mb_tabListPrefix = s [:-1]
            k.setLabel(k.mb_tabListPrefix,protect=False)
        else:
            k.mb_tabListPrefix = s
            k.setLabel(k.mb_tabListPrefix,protect=True)
    
        # g.trace('BackSpace: new mb_tabListPrefix',k.mb_tabListPrefix)
    
        # Force a recomputation of the commands list.
        k.mb_tabList = []
    #@nonl
    #@-node:ekr.20050920085536.46:doBackSpace
    #@+node:ekr.20050920085536.44:doTabCompletion
    # Used by getArg and fullCommand.
    
    def doTabCompletion (self,defaultTabList):
        
        '''Handle tab completion when the user hits a tab.'''
        
        k = self ; s = k.getLabel().strip()
        
        # g.trace(repr(k.mb_prompt))
        
        if k.mb_tabList and s.startswith(k.mb_tabListPrefix):
            # Set the label to the next item on the tab list.
            k.mb_tabListIndex +=1
            if k.mb_tabListIndex >= len(k.mb_tabList):
                k.mb_tabListIndex = 0
            k.setLabel(k.mb_prompt + k.mb_tabList [k.mb_tabListIndex])
        else:
            s = k.getLabel() # Always includes prefix, so command is well defined.
            k.mb_tabListPrefix = s
            command = s [len(k.mb_prompt):]
            k.mb_tabList,common_prefix = g.itemsMatchingPrefixInList(command,defaultTabList)
            k.mb_tabListIndex = 0
            if k.mb_tabList:
                if len(k.mb_tabList) > 1 and (
                    len(common_prefix) > (len(k.mb_tabListPrefix) - len(k.mb_prompt))
                ):
                    k.setLabel(k.mb_prompt + common_prefix)
                    k.mb_tabListPrefix = k.mb_prompt + common_prefix
                else:
                    # No common prefix, so show the first item.
                    k.setLabel(k.mb_prompt + k.mb_tabList [0])
            else:
                k.setLabel(k.mb_prompt,protect=True)
    #@nonl
    #@-node:ekr.20050920085536.44:doTabCompletion
    #@-node:ekr.20051002152108.1:Shared helpers
    #@+node:ekr.20050923172809:State...
    #@+node:ekr.20050923172814.1:clearState
    def clearState (self):
        
        k = self
        k.state.kind = None
        k.state.n = None
        k.state.handler = None
    #@nonl
    #@-node:ekr.20050923172814.1:clearState
    #@+node:ekr.20050923172814.2:getState
    def getState (self,kind):
        
        k = self
        val = g.choose(k.state.kind == kind,k.state.n,0)
        # g.trace(state,'returns',val)
        return val
    #@nonl
    #@-node:ekr.20050923172814.2:getState
    #@+node:ekr.20050923172814.5:getStateKind
    def getStateKind (self):
    
        return self.state.kind
        
    #@nonl
    #@-node:ekr.20050923172814.5:getStateKind
    #@+node:ekr.20050923172814.3:inState
    def inState (self,kind=None):
        
        k = self
        
        if kind:
            return k.state.kind == kind and k.state.n != None
        else:
            return k.state.kind and k.state.n != None
    #@nonl
    #@-node:ekr.20050923172814.3:inState
    #@+node:ekr.20050923172814.4:setState
    def setState (self,kind,n,handler=None):
        
        k = self
        if kind and n != None:
            k.state.kind = kind
            k.state.n = n
            if handler:
                k.state.handler = handler
        else:
            k.clearState()
    #@-node:ekr.20050923172814.4:setState
    #@-node:ekr.20050923172809:State...
    #@-others
#@nonl
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
