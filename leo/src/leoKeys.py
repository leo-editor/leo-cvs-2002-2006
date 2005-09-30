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
    
        self.widget  = c.frame.miniBufferWidget # A Tk Label widget.
        # Permanently associate a Tk.StringVar with the widget.
        self.svar = Tk.StringVar()
        self.widget.configure(textvariable=self.svar)
    
        self.undoers = {} # Emacs instance tracks undoers given to it.
        self.useGlobalKillbuffer = useGlobalKillbuffer
        self.useGlobalRegisters = useGlobalRegisters
        
        self.keystrokes = {}
        self.regx = g.bunch(iter=None,key=None)
        self.state = g.bunch(kind=None,n=None,handler=None)
        #@    << define control-x ivars >>
        #@+node:ekr.20050923222924:<< define control-x ivars >>
        self.previous = []
        self.rect_commands = {}
        self.variety_commands = {}
        self.abbreviationDispatch = {}
        self.register_commands = {}
        #@nonl
        #@-node:ekr.20050923222924:<< define control-x ivars >>
        #@nl
        #@    << define minibuffer ivars >>
        #@+node:ekr.20050923213858:<< define minibuffer ivars >>
        self.altX_history = []
        self.altX_prefix = ''
        self.altX_tabListPrefix = ''
        self.altX_tabList = []
        self.altX_tabListIndex = -1
        self.keysymHistory = []
        self.previousStroke = ''
        self.svars = {}
        self.tailEnds = {} # functions to execute at the end of many Emacs methods.  Configurable by environment.
        
        # For getArg...
        self.arg = ''
        self.afterGetArgState = None
        self.argTabList = []
        # # self.argTabListPrefix = None
        # # self.argTabListIndex = 0
        
        # For negative arguments...
        self.negativeArg = False
        
        # For alt-X commands...
        self.xcommands = None       # Done in finishCreate.
        self.alt_x_prompt = 'full-command: '
        self.x_hasNumeric = ['sort-lines','sort-fields']
        
        # For universal commands...
        self.uCstring = string.digits + '\b'
        self.uCdict = {
            '<Alt-x>': self.alt_X
        }
        #@nonl
        #@-node:ekr.20050923213858:<< define minibuffer ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20050920085536.2: ctor (keyHandler)
    #@+node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    def finishCreate (self,altX_commandsDict):
        
        # g.trace('keyHandler')
        
        k = self ; c = k.c ; w = c.frame.bodyCtrl
    
        k.setMiniBufferFunctions(altX_commandsDict)
        k.setBufferStrokes(w)
        k.setUndoer(w,c.undoer.undo)
        k.setTailEnd(w,self.utTailEnd)
        c.controlCommands.setShutdownHook(c.close)
        
        if 0:
            addTemacsExtensions(k)
            addTemacsAbbreviations(k)
            changeKeyStrokes(k,frame.bodyCtrl)
    
        k.setKeystrokeFunctions()
        k.setControlXFunctions()
        
    #@nonl
    #@+node:ekr.20050923174229.1:setKeystrokFunctions
    def setKeystrokeFunctions (self):
        
        k = self ; c = k.c
        
        self.keystrokes = {
            '<Control-s>':      ( 2, c.searchCommands.startIncremental ),
            '<Control-r>':      ( 2, c.searchCommands.startIncremental ),
            '<Alt-g>':          ( 1, c.editCommands.gotoLine ),
            '<Alt-z>':          ( 1, c.killBufferCommands.zapToCharacter ),
            '<Alt-percent>':    ( 1, c.queryReplaceCommands.masterQR ),
            '<Control-Alt-w>':  ( 1, lambda event: 'break' ),
        }
    #@-node:ekr.20050923174229.1:setKeystrokFunctions
    #@+node:ekr.20050923183932:setControlXFunctions
    def setControlXFunctions (self):
    
        k = self ; c = k.c
    
        self.abbreviationDispatch = {
            'a':    lambda event: k.abbreviationDispatch(event,1),
            'a i':  lambda event: k.abbreviationDispatch(event,2),
        }
    
        self.rect_commands = {
            'o': c.rectangleCommands.openRectangle,
            'c': c.rectangleCommands.clearRectangle,
            't': c.rectangleCommands.stringRectangle,
            'y': c.rectangleCommands.yankRectangle,
            'd': c.rectangleCommands.deleteRectangle,
            'k': c.rectangleCommands.killRectangle,
            'r': c.rectangleCommands.activateRectangleMethods,
        }
    
        self.register_commands = {
            1: c.registerCommands.setNextRegister,
            2: c.registerCommands.executeRegister,
        }
    
        self.variety_commands = {
            'period':       c.editCommands.setFillPrefix,
            'parenleft':    c.macroCommands.startKBDMacro,
            'parenright':   c.macroCommands.stopKBDMacro,
            'semicolon':    c.editCommands.setCommentColumn,
            'Tab':          c.editCommands.tabIndentRegion,
            'u':            lambda event: k.doUndo(event,2),
            'equal':        c.editCommands.lineNumber,
            'h':            c.editCommands.selectAll,
            'f':            c.editCommands.setFillColumn,
            'b':            lambda event, which = 'switch-to-buffer': k.setInBufferMode(event,which),
            'k':            lambda event, which = 'kill-buffer': emakeyHandlers.setInBufferMode(event,which),
        }
    #@nonl
    #@-node:ekr.20050923183932:setControlXFunctions
    #@+node:ekr.20050923214044: setMiniBufferFunctions & helpers
    def setMiniBufferFunctions (self,altX_commandsDict):
        
        # g.trace('miniBufferClass')
    
        k = self ; c = k.c
    
        # Finish this class.
        k.add_ekr_altx_commands()
    
        # Command bindings.
        self.cbDict = k.addCallBackDict() # Creates callback dictionary, primarily used in the master command
    
        self.negArgFunctions = {
            '<Alt-c>': c.editCommands.changePreviousWord,
            '<Alt-u>': c.editCommands.changePreviousWord,
            '<Alt-l>': c.editCommands.changePreviousWord,
        }
    
        self.xcommands = {
            '<Control-t>': c.editCommands.transposeLines,
            '<Control-u>': c.editCommands.upCaseRegion,
            '<Control-l>': c.editCommands.downCaseRegion,
            '<Control-o>': c.editCommands.removeBlankLines,
            '<Control-i>': c.editFileCommands.insertFile,
            '<Control-s>': c.editFileCommands.saveFile,
            '<Control-x>': c.editCommands.exchangePointMark,
            '<Control-c>': c.controlCommands.shutdown,
            '<Control-b>': c.bufferCommands.listBuffers,
            '<Control-Shift-at>': lambda event: event.widget.selection_clear(),
            '<Delete>':     c.killBufferCommands.backwardKillSentence,
        }
    #@nonl
    #@+node:ekr.20050920085536.11:add_ekr_altx_commands
    def add_ekr_altx_commands (self):
    
        #@    << define dict d of abbreviations >>
        #@+node:ekr.20050920085536.12:<< define dict d of abbreviations >>
        d = {
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
    #@+node:ekr.20050920085536.13:addCallBackDict MUST BE GENERALIZED
    def addCallBackDict (self):
    
        '''Create callback dictionary for masterCommand.'''
    
        k = self ; c = k.c
        
        cbDict = {
        
        # The big ones...
        'Alt-x':            k.alt_X,
        #'Control-x':       k.startControlX, # Conflicts with XP cut.
        'Control-c':        k.startControlX, # Conflicts with XP copy.
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
            # 'Control-underscore': k.doUndo,
    
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
    #@-node:ekr.20050920085536.13:addCallBackDict MUST BE GENERALIZED
    #@+node:ekr.20050920085536.15:addToDoAltX
    def addToDoAltX (self,name,macro):
    
        '''Adds macro to Alt-X commands.'''
        
        k= self ; c = k.c
    
        if c.commandsDict.has_key(name):
            return False
    
        def exe (event,macro=macro):
            k.stopControlX(event)
            return k._executeMacro(macro,event.widget)
    
        c.commandsDict [name] = exe
        k.namedMacros [name] = macro
        return True
    #@nonl
    #@-node:ekr.20050920085536.15:addToDoAltX
    #@+node:ekr.20050920085536.16:bindKey
    def bindKey (self,w,evstring):
        
        k = self
    
        callback = k.cbDict.get(evstring)
        evstring = '<%s>' % evstring
        
        # g.trace(evstring)
    
        def f (event):
            general = evstring == '<Key>'
            return k.masterCommand(event,callback,evstring,general)
    
        if evstring == '<Key>':
            w.bind(evstring,f,'+')
        else:
            w.bind(evstring,f)
    #@nonl
    #@-node:ekr.20050920085536.16:bindKey
    #@+node:ekr.20050920085536.17:setBufferStrokes  (creates svars & <key> bindings)
    def setBufferStrokes (self,w):
    
        '''Sets key bindings for Tk Text widget w.'''
        
        k = self
    
        # Create one binding for each entry in cbDict.
        for key in k.cbDict:
            k.bindKey(w,key)
    
        # Add a binding for <Key> events, so _all_ key events go through masterCommand.
        k.bindKey(w,'Key')
    #@nonl
    #@-node:ekr.20050920085536.17:setBufferStrokes  (creates svars & <key> bindings)
    #@-node:ekr.20050923214044: setMiniBufferFunctions & helpers
    #@+node:ekr.20050920085536.64:manufactureKeyPress
    def manufactureKeyPress (self,event,keysym):
    
        w = event.widget
        w.event_generate('<Key>',keysym=keysym)
        w.update_idletasks()
        
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.64:manufactureKeyPress
    #@-node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    #@-node:ekr.20050920085536.1: Birth
    #@+node:ekr.20050920085536.32: Entry points
    #@+node:ekr.20050930082638:Repeating commands
    #@@nocolor
    #@+at
    # 
    # Repeating Commands
    # 
    # ESC-5 C-f
    #     move forward 5 chars
    # 
    # C-u (the universal argument command)
    #     Just like Esc-n, but does not need an argument -> in which case the 
    # default of 4 is used. eg:
    # 
    # C-u C-u -> repeat 16 times
    #@-at
    #@nonl
    #@-node:ekr.20050930082638:Repeating commands
    #@+node:ekr.20050930081539:Apropos universal
    #@@nocolor
    #@+at
    # 
    # universal-argument
    #   Command: Begin a numeric argument for the following command.
    # universal-argument-map
    #   Variable: Keymap used while processing \[universal-argument].
    #   Plist: 1 property (variable-documentation)
    # universal-argument-minus
    #   Command: (not documented)
    # universal-argument-more
    #   Command: (not documented)
    # universal-argument-num-events
    #   Variable: Number of argument-specifying events read by 
    # `universal-argument'.
    #   Plist: 1 property (variable-documentation)
    # universal-argument-other-key
    #   Command: (not documented)
    # universal-coding-system-argument
    #   Command: Execute an I/O command using the specified coding system.
    #@-at
    #@-node:ekr.20050930081539:Apropos universal
    #@+node:ekr.20050930082638.1:Emacs docs prefix command arguments
    #@@nocolor
    #@+at
    # 
    # Most Emacs commands can use a prefix argument, a number specified before 
    # the
    # command itself. (Don't confuse prefix arguments with prefix keys.) The 
    # prefix
    # argument is at all times represented by a value, which may be nil, 
    # meaning there
    # is currently no prefix argument. Each command may use the prefix 
    # argument or
    # ignore it.
    # 
    # There are two representations of the prefix argument: raw and numeric. 
    # The
    # editor command loop uses the raw representation internally, and so do 
    # the Lisp
    # variables that store the information, but commands can request either
    # representation.
    # 
    # Here are the possible values of a raw prefix argument:
    # 
    # - nil, meaning there is no prefix argument. Its numeric value is 1, but 
    # numerous
    #   commands make a distinction between nil and the integer 1.
    # 
    # - An integer, which stands for itself.
    # 
    # - A list of one element, which is an integer. This form of prefix 
    # argument
    #   results from one or a succession of C-u's with no digits. The numeric 
    # value is
    #   the integer in the list, but some commands make a distinction between 
    # such a
    #   list and an integer alone.
    # 
    # - The symbol -. This indicates that M-- or C-u - was typed, without 
    # following
    # digits. The equivalent numeric value is -1, but some commands make a 
    # distinction
    # between the integer -1 and the symbol -.
    # 
    # We illustrate these possibilities by calling the following function with 
    # various prefixes:
    # 
    #   (defun display-prefix (arg)
    #     "Display the value of the raw prefix arg."
    #     (interactive "P")
    #     (message "%s" arg))
    # 
    # Here are the results of calling display-prefix with various raw prefix 
    # arguments:
    # 
    #         M-x display-prefix  -| nil
    # C-u     M-x display-prefix  -| (4)
    # C-u C-u M-x display-prefix  -| (16)
    # C-u 3   M-x display-prefix  -| 3
    # M-3     M-x display-prefix  -| 3      ; (Same as C-u 3.)
    # C-u -   M-x display-prefix  -| -
    # M--     M-x display-prefix  -| -      ; (Same as C-u -.)
    # C-u - 7 M-x display-prefix  -| -7
    # M-- 7   M-x display-prefix  -| -7     ; (Same as C-u -7.)
    # 
    # Emacs uses two variables to store the prefix argument: prefix-arg and
    # current-prefix-arg. Commands such as universal-argument that set up 
    # prefix
    # arguments for other commands store them in prefix-arg. In contrast,
    # current-prefix-arg conveys the prefix argument to the current command, 
    # so
    # setting it has no effect on the prefix arguments for future commands.
    # 
    # Normally, commands specify which representation to use for the prefix 
    # argument,
    # either numeric or raw, in the interactive declaration. (See section 
    # 21.2.1 Using
    # interactive.) Alternatively, functions may look at the value of the 
    # prefix
    # argument directly in the variable current-prefix-arg, but this is less 
    # clean.
    # 
    # Function: prefix-numeric-value arg
    # 
    # This function returns the numeric meaning of a valid raw prefix argument 
    # value,
    # arg. The argument may be a symbol, a number, or a list. If it is nil, 
    # the value
    # 1 is returned; if it is -, the value -1 is returned; if it is a number, 
    # that
    # number is returned; if it is a list, the CAR of that list (which should 
    # be a
    # number) is returned.
    # 
    # Variable: current-prefix-arg
    #     This variable holds the raw prefix argument for the current command. 
    # Commands
    #     may examine it directly, but the usual method for accessing it is 
    # with
    #     (interactive "P").
    # 
    # Variable: prefix-arg
    #     The value of this variable is the raw prefix argument for the next 
    # editing
    #     command. Commands such as universal-argument that specify prefix 
    # arguments for
    #     the following command work by setting this variable.
    # 
    # Variable: last-prefix-arg
    #     The raw prefix argument value used by the previous command.
    # 
    # The following commands exist to set up prefix arguments for the 
    # following
    # command. Do not call them for any other reason.
    # 
    # Command: universal-argument
    #     This command reads input and specifies a prefix argument for the 
    # following
    #     command. Don't call this command yourself unless you know what you 
    # are doing.
    # 
    # Command: digit-argument arg
    #     This command adds to the prefix argument for the following command. 
    # The argument
    #     arg is the raw prefix argument as it was before this command; it is 
    # used to
    #     compute the updated prefix argument. Don't call this command 
    # yourself unless you
    #     know what you are doing.
    # 
    # Command: negative-argument arg
    #     This command adds to the numeric argument for the next command. The 
    # argument arg
    #     is the raw prefix argument as it was before this command; its value 
    # is negated
    #     to form the new prefix argument. Don't call this command yourself 
    # unless you
    #     know what you are doing.
    #@-at
    #@nonl
    #@-node:ekr.20050930082638.1:Emacs docs prefix command arguments
    #@+node:ekr.20050930080419:digitArgument & universalArgument
    def digitArgument (self,event):
        
        k = self ; k.stroke = ''
    
        return k.universalDispatchStateHelper(event)
    
    def universalArgument (self,event):
        
        k = self ; k.stroke = ''
    
        return k.universalDispatchStateHelper(event)
    #@nonl
    #@-node:ekr.20050930080419:digitArgument & universalArgument
    #@+node:ekr.20050920085536.68:negativeArgument
    def negativeArgument (self,event):
    
        k = self ; state = k.getState('negativeArg')
        
        k.setLabelBlue('Negative Argument: ',protect=True)
    
        if state == 0:
            k.setState('negativeArg',1)
        else:
            k.clearState()
            func = k.negArgFunctions.get(k.stroke)
            if func:
                func(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.68:negativeArgument
    #@+node:ekr.20050920085536.77:numberCommand
    def numberCommand (self,event,stroke,number):
    
        k = self ; k.stroke = stroke ; w = event.widget
    
        k.universalDispatchStateHelper(event)
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
    
        if k.altX_history:
            k.setState('last-altx',1,handler=k.doLastAltX)
            k.setLabelBlue("Redo: %s" % k.altX_history[0])
        return 'break'
        
    def doLastAltX (self,event):
        
        k = self ; c = k.c
    
        if event.keysym == 'Return' and k.altX_history:
            last = k.altX_history [0]
            c.commandsDict [last](event)
            return 'break'
        else:
            return k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20050920085536.48:repeatComplexCommand & helper
    #@+node:ekr.20050920085536.63:keyboardQuit
    def keyboardQuit (self,event):
    
        '''This method cleans the Emacs instance of state and ceases current operations.'''
        
        k = self
    
        return k.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920085536.63:keyboardQuit
    #@+node:ekr.20050920085536.73:universalDispatchHelper
    def universalDispatchStateHelper (self,event):
    
        k = self ; stroke = k.stroke ; state = k.getState('uC')
    
        if state == 0:
            k.setState('uC',1,handler=k.universalDispatchStateHelper)
            k.setLabelBlue('')
        elif state == 1:
            k.universalCommand1(event,stroke)
        elif state == 2:
            k.universalCommand3(event,stroke)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.74:universalCommand1
    def universalCommand1 (self,event,stroke):
        
        k = self
    
        if event.char not in k.uCstring:
            return k.universalCommand2(event,stroke)
     
        k.updateLabel(event)
    
        if event.char != '\b':
            k.setLabel('%s ' % k.getLabel())
    #@nonl
    #@-node:ekr.20050920085536.74:universalCommand1
    #@+node:ekr.20050920085536.75:universalCommand2 (Called from universalCommand2)
    def universalCommand2 (self,event,stroke):
        
        k = self ; w = event.widget
        txt = k.getLabel()
        k.keyboardQuit(event)
        txt = txt.replace(' ','')
        k.resetLabel()
        if not txt.isdigit():
            # This takes us to macro state.
            # For example Control-u Control-x ( will execute the last macro and begin editing of it.
            if stroke == '<Control-x>':
                k.setState('uC',2)
                return k.universalCommand3(event,stroke)
            return k._tailEnd(w)
    
        if k.uCdict.has_key(stroke): # This executes the keystroke 'n' number of times.
            k.uCdict [stroke](event,txt)
        else:
            i = int(txt)
            stroke = stroke.lstrip('<').rstrip('>')
            if k.cbDict.has_key(stroke):
                for z in xrange(i):
                    method = k.cbDict [stroke]
                    ev = Tk.Event()
                    ev.widget = event.widget
                    ev.keysym = event.keysym
                    ev.keycode = event.keycode
                    ev.char = event.char
                    k.masterCommand(ev,method,'<%s>' % stroke)
            else:
                for z in xrange(i):
                    w.event_generate('<Key>',keycode=event.keycode,keysym=event.keysym)
                    k._tailEnd(w)
    #@-node:ekr.20050920085536.75:universalCommand2 (Called from universalCommand2)
    #@+node:ekr.20050920085536.76:universalCommand3
    def universalCommand3 (self,event,stroke):
        
        k = self
        k.setLabelBlue('Control-u %s' % stroke.lstrip('<').rstrip('>'))
    
        if event.keysym == 'parenleft':
            k.keyboardQuit(event)
            c.macroCommands.startKBDMacro(event)
            c.macroCommands.executeLastMacro(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920085536.76:universalCommand3
    #@-node:ekr.20050920085536.73:universalDispatchHelper
    #@-node:ekr.20050920085536.32: Entry points
    #@+node:ekr.20050920085536.61:extendAltX
    def extendAltX (self,name,function):
    
        '''A simple method that extends the functions Alt-X offers.'''
    
        # Important: f need not be a method of the emacs class.
        
        k = self ; c = k.c
    
        def f (event,aX=None,self=self,command=function):
            # g.trace(event,self,command)
            command()
            k.keyboardQuit(event)
    
        c.commandsDict [name] = f
    #@nonl
    #@-node:ekr.20050920085536.61:extendAltX
    #@+node:ekr.20050920085536.65: masterCommand
    def masterCommand (self,event,method,stroke,general):
        
        '''This is the central routing method of the Emacs class.
        All commands and keystrokes pass through here.'''
        
        # Note: the _L symbols represent *either* special key.
        k = self ; c = k.c
        special = event.keysym in ('Control_L','Alt_L','Shift_L')
        k.stroke = stroke
    
        inserted = not special or (
            not general and (len(k.keysymHistory) == 0 or k.keysymHistory [0] != event.keysym))
    
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
    
        if c.macroCommands.macroing:
            #@        << handle macro >>
            #@+node:ekr.20050920085536.66:<< handle macro >>
            if c.macroCommands.macroing == 2 and stroke != '<Control-x>':
                return k.nameLastMacro(event)
                
            elif c.macroCommands.macroing == 3 and stroke != '<Control-x>':
                return k.getMacroName(event)
                
            else:
               k.recordKBDMacro(event,stroke)
            #@nonl
            #@-node:ekr.20050920085536.66:<< handle macro >>
            #@nl
    
        if stroke == '<Control-g>':
            k.previousStroke = stroke
            return k.keyboardQuit(event)
    
        if k.inState():
            k.previousStroke = stroke
            return k.callStateFunction(event)
    
        if k.hasKeyStroke(stroke):
            g.trace('hasKeyStroke')
            k.previousStroke = stroke
            k.callKeystrokeFunction(event)
    
        if k.regx.iter:
            try:
                k.regXKey = event.keysym
                k.regx.iter.next() # EKR: next() may throw StopIteration.
            finally:
                return 'break'
    
        if k.abbrevOn:
            if c.abbrevCommands._expandAbbrev(event):
                return 'break'
    
        if method:
            rt = method(event)
            k.previousStroke = stroke
            return rt
        
        else:
            c.frame.body.onBodyKey(event)
            return None # Not 'break'
    #@-node:ekr.20050920085536.65: masterCommand
    #@+node:ekr.20050920085536.41:alt_X & helpers
    def alt_X (self,event=None,which=''):
    
        k = self
    
        k.setState('altx',which or 1,handler=k.doAlt_X) 
    
        if which:
            k.setLabelBlue('%s %s' % (which,k.alt_x_prompt),protect=True)
        else:
            k.setLabelBlue('%s' % (k.alt_x_prompt),protect=True)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.42:doAlt_X
    def doAlt_X (self,event):
    
        '''This method executes the correct Alt-X command'''
        
        k = self ; c = k.c ; keysym = event.keysym
        # g.trace(keysym)
    
        if keysym == 'Return':
            k.dispatchAltXFunction(event)
        elif keysym == 'Tab':
            k.doTabCompletion(c.commandsDict.keys())
        elif keysym == 'BackSpace':
            k.doBackSpace()
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.altX_tabList = []
            k.updateLabel(event)
            k.altX_tabListPrefix = k.getLabel()
            # g.trace('new prefix',k.altX_tabListPrefix)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.42:doAlt_X
    #@+node:ekr.20050920085536.45:dispatchAltXFunction
    def dispatchAltXFunction (self,event):
        
        k = self ; c = k.c ; s = k.getLabel()
        k.altX_tabList = []
        command = s[len(k.altX_prefix):].strip()
        func = c.commandsDict.get(command)
        
        # These must be done *after* getting the command.
        k.clearState()
        k.keyboardQuit(event)
        
        if func:
            if command != 'repeat-complex-command': k.altX_history.insert(0,command)
            aX = k.getState('altx')
            if (type(aX) == type(1) or aX.isdigit()) and command in k.x_hasNumeric:
                func(event,aX)
            else:
                func(event)
        else:
            k.setLabel('Command does not exist')
    #@nonl
    #@-node:ekr.20050920085536.45:dispatchAltXFunction
    #@-node:ekr.20050920085536.41:alt_X & helpers
    #@+node:ekr.20050920085536.62:getArg
    def getArg (self,event,returnKind=None,returnState=None,handler=None,prefix=None,tabList=None):
        
        '''Accumulate an argument until the user hits return (or control-g).
        Enter the given return state when done.
        The prefix is does not form the arg.  The prefix defaults to the k.getLabel().
        '''
        
        # Similar, but not the same as the code in doAlt_X.
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
            k.altX_tabList = []
            
            if prefix:
                k.altX_tabListPrefix = prefix
                k.altX_prefix = prefix
                k.alt_x_prompt = prefix
            else:
                k.altX_tabListPrefix = k.altX_prefix = k.getLabel()
                k.alt_x_prompt = ''
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
            k.altX_tabList = []
            k.updateLabel(event)
            k.altX_tabListPrefix = k.getLabel()
    
        return 'break'
    #@-node:ekr.20050920085536.62:getArg
    #@+node:ekr.20050920085536.57:ControlX...  (actually bound to control-c for now)
    #@+node:ekr.20050920085536.58:startControlX
    def startControlX (self,event):
    
        '''This method starts the Control-X command sequence.'''
        
        k = self
    
        k.setState('controlx',True,handler=k.controlX_stateHandler)
        k.setLabelBlue('Control - X')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.58:startControlX
    #@+node:ekr.20050920085536.59:stopControlX
    def stopControlX (self,event):
    
        '''This method clears the state of the Emacs instance'''
        
        k = self ; c = k.c ; w = event.widget
    
        # This will all be migrated to keyboardQuit eventually.
        if c.controlCommands.shuttingdown:
            return
            
        leoEditCommands.initAllEditCommanders(c)
    
        k.clearState()
        w.tag_delete('color')
        w.tag_delete('color1')
        k.resetLabel()
        w.update_idletasks()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.59:stopControlX
    #@+node:ekr.20050923183943.1:controlX_stateHandler
    def controlX_stateHandler (self,event):
        
        k = self ; stroke = k.stroke
    
        k.previous.insert(0,event.keysym)
    
        if len(k.previous) > 10:
            k.previous.pop()
            
        g.trace(stroke)
    
        if stroke in ('<Key>','<Escape>'):
            return k.processKey(event)  # Weird command-specific stuff.
            
        #  k.xcommands:
        # '<Control-t>': c.editCommands.transposeLines,
        # '<Control-u>': lambda event, way = 'up': c.editCommands.upperLowerRegion(event,way),
        # '<Control-l>': lambda event, way = 'low': c.editCommands.upperLowerRegion(event,way),
        # '<Control-o>': c.editCommands.removeBlankLines,
        # '<Control-i>': c.editFileCommands.insertFile,
        # '<Control-s>': c.editFileCommands.saveFile,
        # '<Control-x>': c.editCommands.exchangePointMark,
        # '<Control-c>': c.controlCommands.shutdown,
        # '<Control-b>': c.bufferCommands.listBuffers,
        # '<Control-Shift-at>': lambda event: event.widget.selection_clear(),
        # '<Delete>':   c.killBufferCommands.backwardKillSentence,
    
        if stroke in k.xcommands:
            k.xcommands [stroke](event)
            if stroke != '<Control-b>':
                k.keyboardQuit(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050923183943.1:controlX_stateHandler
    #@+node:ekr.20050923183943.2:setControlXFunctions MUST BE GENERALIZED
    def setControlXFunctions (self):
    
        k = self ; c = k.c
    
        self.abbreviationDispatch = {
            'a':    lambda event: k.abbreviationDispatch(event,1),
            'a i':  lambda event: k.abbreviationDispatch(event,2),
        }
    
        self.rect_commands = {
            'o': c.rectangleCommands.openRectangle,
            'c': c.rectangleCommands.clearRectangle,
            't': c.rectangleCommands.stringRectangle,
            'y': c.rectangleCommands.yankRectangle,
            'd': c.rectangleCommands.deleteRectangle,
            'k': c.rectangleCommands.killRectangle,
            'r': c.rectangleCommands.activateRectangleMethods,
        }
    
        self.register_commands = {
            1: c.registerCommands.setNextRegister,
            2: c.registerCommands.executeRegister,
        }
    
        self.variety_commands = {
            'period':       c.editCommands.setFillPrefix,
            'parenleft':    c.macroCommands.startKBDMacro,
            'parenright':   c.macroCommands.stopKBDMacro,
            'semicolon':    c.editCommands.setCommentColumn,
            'Tab':          c.editCommands.tabIndentRegion,
            'u':            lambda event: k.doUndo(event,2),
            'equal':        c.editCommands.lineNumber,
            'h':            c.editCommands.selectAll,
            'f':            c.editCommands.setFillColumn,
            'b':            lambda event, which = 'switch-to-buffer': k.setInBufferMode(event,which),
            'k':            lambda event, which = 'kill-buffer': emakeyHandlers.setInBufferMode(event,which),
        }
    #@nonl
    #@-node:ekr.20050923183943.2:setControlXFunctions MUST BE GENERALIZED
    #@+node:ekr.20050923183943.4:processKey MUST BE GENERALIZED
    def processKey (self,event):
    
        k = self ; c = k.c ; previous = k.previous
        
        if event.keysym in ('Shift_L','Shift_R'):
            return
            
        # g.trace(event.keysym)
    
        if c.rectangleCommands.sRect:
            return c.stringRectangle(event)
    
        if (
            event.keysym == 'r' and
            c.rectangleCommands.rectanglemode == 0
            and not c.registerCommands.registermode
        ):
            return k.processRectangle(event)
    
        if (
            k.rect_commands.has_key(event.keysym) and
            c.rectangleCommands.rectanglemode == 1
        ):
            return k.processRectangle(event)
    
        if k.register_commands.has_key(c.registerCommands.registermode):
            k.register_commands [c.registerCommands.registermode] (event)
            return 'break'
    
        func = k.variety_commands.get(event.keysym)
        if func:
            k.stopControlX(event)
            return func(event)
    
        if event.keysym in ('a','i','e'):
            if k.processAbbreviation(event):
                return 'break'
            else:
                g.trace('no abbreviation for %s' % event.keysym)
    
        if event.keysym == 'g':
            l = k.getLabel()
            if k.abbreviationDispatch.has_key(l):
                k.stopControlX(event)
                return k.abbreviationDispatch [l](event)
    
        if event.keysym == 'e':
            k.stopControlX(event)
            return c.macroCommands.executeLastMacro(event)
    
        if event.keysym == 'x' and previous [1] not in ('Control_L','Control_R'):
            event.keysym = 's'
            k.setNextRegister(event)
            return 'break'
    
        if event.keysym == 'Escape':
            if len(previous) > 1:
                if previous [1] == 'Escape':
                    return k.repeatComplexCommand(event)
    #@nonl
    #@-node:ekr.20050923183943.4:processKey MUST BE GENERALIZED
    #@+node:ekr.20050923183943.5:processRectangle
    if 0: # Reference: actually defined in finishCreate.
    
        self.rect_commands = {
            'o': c.rectangleCommands.openRectangle,
            'c': c.rectangleCommands.clearRectangle,
            't': c.rectangleCommands.stringRectangle,
            'y': c.rectangleCommands.yankRectangle,
            'd': c.rectangleCommands.deleteRectangle,
            'k': c.rectangleCommands.killRectangle,
            'r': c.rectangleCommands.activateRectangleMethods,
        }
    
    def processRectangle (self,event):
        
        k = self
        
        func = k.rect_commands.get(event.keysym)
        func(event)
        return 'break'
    #@-node:ekr.20050923183943.5:processRectangle
    #@+node:ekr.20050923183943.6:processAbbreviation MUST BE GENERALIZED
    def processAbbreviation (self,event):
        
        k = self ; char = event.char
    
        if k.getLabel() != 'a' and event.keysym == 'a':
            k.setLabel('a')
            return 'break'
    
        elif k.getLabel() == 'a':
            if char == 'i':
                k.setLabel('a i')
            elif char == 'e':
                k.stopControlX(event)
                event.char = ''
                k.expandAbbrev(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050923183943.6:processAbbreviation MUST BE GENERALIZED
    #@-node:ekr.20050920085536.57:ControlX...  (actually bound to control-c for now)
    #@+node:ekr.20050923174229.2:Keystroke...
    #@+node:ekr.20050923174229.3:callKeystrokeFunction
    def callKeystrokeFunction (self,event):
        
        k = self
        
        numberOfArgs, func = k.keystrokes [k.stroke]
    
        return func(event)
    #@nonl
    #@-node:ekr.20050923174229.3:callKeystrokeFunction
    #@+node:ekr.20050920085536.22:hasKeyStroke
    def hasKeyStroke (self,stroke):
    
        return self.keystrokes.has_key(stroke)
    #@nonl
    #@-node:ekr.20050920085536.22:hasKeyStroke
    #@-node:ekr.20050923174229.2:Keystroke...
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
    #@+node:ekr.20050920085536.39:getLabel & setLabel
    def getLabel (self,ignorePrompt=False):
        
        k = self ; s = k.svar.get()
        if ignorePrompt:
            return s[len(k.altX_prefix):]
        else:
            return s
    
    def setLabel (self,s,protect=False):
        
        k = self
        k.svar.set(s)
        if protect:
            k.altX_prefix = s
    #@nonl
    #@-node:ekr.20050920085536.39:getLabel & setLabel
    #@+node:ekr.20050920085536.35:setLabelGrey
    def setLabelGrey (self,label=None):
    
        k = self
        k.widget.configure(background='lightgrey')
        if label is not None:
            k.setLabel(label)
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
        k.altX_prefix = ''
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
            if len(s) <= k.altX_prefix:
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
    #@+node:ekr.20050923172809:State...
    #@+node:ekr.20050923172809.1:callStateFunction
    def callStateFunction (self,event):
        
        k = self
        
        # g.trace(k.stateKind,k.state)
        
        if k.state.kind:
            if k.state.handler:
                return k.state.handler(event)
            else:
                g.es_print('no state function for %s' % (k.state.kind),color='red')
                return 'break'
    #@nonl
    #@-node:ekr.20050923172809.1:callStateFunction
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
    def inState (self):
        
        k = self
        
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
    #@+node:ekr.20050928082315:Special characters in the mini-buffer...
    #@+node:ekr.20050920085536.46:doBackSpace
    def doBackSpace (self):
    
        '''Cut back to previous prefix and update prefix.'''
    
        k = self ; s = k.altX_tabListPrefix
    
        if len(s) > len(k.altX_prefix):
            k.altX_tabListPrefix = s [:-1]
            k.setLabel(k.altX_tabListPrefix,protect=False)
        else:
            k.altX_tabListPrefix = s
            k.setLabel(k.altX_tabListPrefix,protect=True)
    
        # g.trace('BackSpace: new altX_tabListPrefix',k.altX_tabListPrefix)
    
        # Force a recomputation of the commands list.
        k.altX_tabList = []
    #@nonl
    #@-node:ekr.20050920085536.46:doBackSpace
    #@+node:ekr.20050920085536.44:doTabCompletion
    def doTabCompletion (self,defaultTabList):
        
        '''Handle tab completion when the user hits a tab.'''
        
        k = self ; s = k.getLabel().strip()
        
        # g.trace(len(k.altX_tabList),repr(k.alt_x_prompt))
        
        if k.altX_tabList and s.startswith(k.altX_tabListPrefix):
            # Set the label to the next item on the tab list.
            k.altX_tabListIndex +=1
            if k.altX_tabListIndex >= len(k.altX_tabList):
                k.altX_tabListIndex = 0
            k.setLabel(k.alt_x_prompt + k.altX_tabList [k.altX_tabListIndex])
        else:
            s = k.getLabel() # Always includes prefix, so command is well defined.
            k.altX_tabListPrefix = s
            command = s [len(k.alt_x_prompt):]
            k.altX_tabList,common_prefix = g.itemsMatchingPrefixInList(command,defaultTabList)
            k.altX_tabListIndex = 0
            if k.altX_tabList:
                if len(k.altX_tabList) > 1 and (
                    len(common_prefix) > (len(k.altX_tabListPrefix) - len(k.alt_x_prompt))
                ):
                    k.setLabel(k.alt_x_prompt + common_prefix)
                    k.altX_tabListPrefix = k.alt_x_prompt + common_prefix
                else:
                    # No common prefix, so show the first item.
                    k.setLabel(k.alt_x_prompt + k.altX_tabList [0])
            else:
                k.setLabel(k.alt_x_prompt,protect=True)
    #@nonl
    #@-node:ekr.20050920085536.44:doTabCompletion
    #@-node:ekr.20050928082315:Special characters in the mini-buffer...
    #@+node:ekr.20050920085536.69:tailEnd... (to be removed?)
    #@+node:ekr.20050920114619.1:utTailEnd
    def utTailEnd (self,event=None):
    
        '''A method that Emacs will call with its _tailEnd method'''
        
        k = self ; c = k.c ; w = c.frame.bodyCtrl
    
        # w.event_generate('<Key>')
        w.focus_force()
        w.update_idletasks()
        # c.frame.bodyWantsFocus(w,later=True,tag='utTailEnd')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920114619.1:utTailEnd
    #@+node:ekr.20050920085536.70:_tailEnd
    def _tailEnd (self,w):
        
        '''This returns the tailEnd function that has been configure for the w parameter.'''
        
        k = self
        func = k.tailEnds.get(w)
        if func:
            # g.trace(func)
            return func(w)
        else:
            return 'break'
    #@-node:ekr.20050920085536.70:_tailEnd
    #@+node:ekr.20050920085536.71:setTailEnd
    def setTailEnd (self,w,tailCall):
    
        '''This method sets a ending call that is specific for a particular Text widget.
           Some environments require that specific end calls be made after a keystroke
           or command is executed.'''
    
        k = self
    
        k.tailEnds [w] = tailCall
    #@-node:ekr.20050920085536.71:setTailEnd
    #@-node:ekr.20050920085536.69:tailEnd... (to be removed?)
    #@+node:ekr.20050920085536.4:Undoer...
    #@+at
    # Emacs requires an undo mechanism be added from the environment.
    # If there is no undo mechanism added, there will be no undo functionality 
    # in the instance.
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050920085536.5:setUndoer
    def setUndoer (self,w,undoer):
        '''This method sets the undoer method for the Emacs instance.'''
        
        k = self
        
        k.undoers [w] = undoer
    #@nonl
    #@-node:ekr.20050920085536.5:setUndoer
    #@+node:ekr.20050920085536.6:doUndo
    def doUndo (self,event,amount=1):
        
        k = self ; w = event.widget
        
        if k.undoers.has_key(w):
            for z in xrange(amount):
                k.undoers [w] ()
        return 'break'
    
    #@-node:ekr.20050920085536.6:doUndo
    #@-others
    #@nonl
    #@-node:ekr.20050920085536.4:Undoer...
    #@-others
#@nonl
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
