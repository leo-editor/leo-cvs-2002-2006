#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3748:@thin leoKeys.py
"""Gui-independent keystroke handling for Leo."""

#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< imports >>
#@+node:ekr.20050920094258:<< imports >>
import leoGlobals as g

import leoNodes

Tk              = g.importExtension('Tkinter',pluginName=None,verbose=False)
tkFileDialog    = g.importExtension('tkFileDialog',pluginName=None,verbose=False)
tkFont          = g.importExtension('tkFileDialog',pluginName=None,verbose=False)

import string
#@nonl
#@-node:ekr.20050920094258:<< imports >>
#@nl

#@+others
#@+node:ekr.20050920085536:class keyHandler
class keyHandlerClass:
    
    '''A class to support emacs-style commands.'''

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
    #@+node:ekr.20050920085536.1:Birth
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
        #@    << define regX ivars >>
        #@+node:ekr.20050923222924.2:<< define regX ivars >>
        # For communication between keystroke handlers and other classes.
        self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
        self.regXKey = None
        #@nonl
        #@-node:ekr.20050923222924.2:<< define regX ivars >>
        #@nl
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
        #@    << define keystroke ivars >>
        #@+node:ekr.20050923222924.1:<< define keystroke ivars >>
        self.keystrokes = {}
        #@nonl
        #@-node:ekr.20050923222924.1:<< define keystroke ivars >>
        #@nl
        #@    << define state ivars >>
        #@+node:ekr.20050923222924.3:<< define state ivars >>
        self.state = None
        self.states = {}
        #@nonl
        #@-node:ekr.20050923222924.3:<< define state ivars >>
        #@nl
        #@    << define minibuffer ivars >>
        #@+node:ekr.20050923213858:<< define minibuffer ivars >>
        self.altX_history = []
        self.altX_prefix = ''
        self.altX_tabListPrefix = ''
        self.altX_tabList = []
        self.altX_tabListIndex = -1
        self.keysymhistory = []
        self.previousStroke = ''
        self.svars = {}
        self.tailEnds = {} # functions to execute at the end of many Emacs methods.  Configurable by environment.
        
        # For accumlated args...
        self.arg = ''
        self.afterGetArgState = None
        
        # For negative arguments...
        self.negativeArg = False
        self.negArgs = {} # Set in finishCreate.
        
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
        
        k = self ; c = k.c ; frame = c.frame
    
        k.setMiniBufferFunctions(altX_commandsDict)
        k.setBufferStrokes(c.frame.bodyCtrl)
        k.setUndoer(c.frame.bodyCtrl,c.undoer.undo)
        
        #@    << define utTailEnd >>
        #@+node:ekr.20050920114619.1:<< define utTailEnd >>
        def utTailEnd (buffer,frame=frame):
        
            '''A method that Emacs will call with its _tailEnd method'''
        
            buffer.event_generate('<Key>')
            buffer.update_idletasks()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920114619.1:<< define utTailEnd >>
        #@nl
        k.setTailEnd(frame.bodyCtrl,utTailEnd)
        c.controlCommands.setShutdownHook(c.close)
        
        if 0:
            addTemacsExtensions(k)
            addTemacsAbbreviations(k)
            changeKeyStrokes(k,frame.bodyCtrl)
    
        if 1: # This is dubious.
            k.setBufferInteractionMethods(frame.bodyCtrl)
            
        k.setStateFunctions()
        k.setKeystrokeFunctions()
        k.setControlXFunctions()
        
    #@nonl
    #@+node:ekr.20050923174229:setStateFunctions
    def setStateFunctions (self):
        
        k = self ; c = k.c
    
        # EKR: used only below.
        def eA (event):
            if k.expandAbbrev(event):
                return 'break'
    
        self.stateCommands = { 
            # 1 == one parameter, 2 == all
            
            # Utility states...
            'getArg':    (2,k.getArg),
            
            # Command states...
            'uC':               (2,k.universalDispatch),
            'controlx':         (2,k.doControlX),
            'isearch':          (2,c.searchCommands.iSearch),
            'goto':             (1,c.editCommands.Goto),
            'zap':              (1,c.editCommands.zapTo),
            'howM':             (1,c.editCommands.howMany),
            'abbrevMode':       (1,c.abbrevCommands.abbrevCommand1),
            'altx':             (1,k.doAlt_X),
            'qlisten':          (1,c.queryReplaceCommands.masterQR),
            'rString':          (1,c.editCommands.replaceString),
            'negativeArg':      (2,k.negativeArgument),
            'abbrevOn':         (1,eA),
            'set-fill-column':  (1,c.editCommands.setFillColumn),
            'chooseBuffer':     (1,c.bufferCommands.chooseBuffer),
            'renameBuffer':     (1,c.bufferCommands.renameBuffer),
            're_search':        (1,c.searchCommands.re_search),
            'alterlines':       (1,c.editCommands.processLines),
            'make_directory':   (1,c.editFileCommands.makeDirectory),
            'remove_directory': (1,c.editFileCommands.removeDirectory),
            'delete_file':      (1,c.editFileCommands.deleteFile),
            'nonincr-search':   (2,c.searchCommands.nonincrSearch),
            'word-search':      (1,c.searchCommands.wordSearch),
            'last-altx':        (1,k.executeLastAltX),
            'escape':           (1,c.editCommands.watchEscape),
            'subprocess':       (1,c.controlCommands.subprocesser),
        }
    #@nonl
    #@-node:ekr.20050923174229:setStateFunctions
    #@+node:ekr.20050923174229.1:setKeystrokFunctions
    def setKeystrokeFunctions (self):
        
        k = self ; c = k.c
        
        self.keystrokes = {
            '<Control-s>':      ( 2, c.searchCommands.startIncremental ),
            '<Control-r>':      ( 2, c.searchCommands.startIncremental ),
            '<Alt-g>':          ( 1, c.editCommands.startGoto ),
            '<Alt-z>':          ( 1, c.editCommands.startZap ),
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
    
        self.negArgs = {
            '<Alt-c>': c.editCommands.changePreviousWord,
            '<Alt-u>': c.editCommands.changePreviousWord,
            '<Alt-l>': c.editCommands.changePreviousWord,
        }
    
        self.xcommands = {
            '<Control-t>': c.editCommands.transposeLines,
            '<Control-u>': lambda event, way = 'up': c.editCommands.upperLowerRegion(event,way),
            '<Control-l>': lambda event, way = 'low': c.editCommands.upperLowerRegion(event,way),
            '<Control-o>': c.editCommands.removeBlankLines,
            '<Control-i>': c.editFileCommands.insertFile,
            '<Control-s>': c.editFileCommands.saveFile,
            '<Control-x>': c.editCommands.exchangePointMark,
            '<Control-c>': c.controlCommands.shutdown,
            '<Control-b>': c.bufferCommands.listBuffers,
            '<Control-Shift-at>': lambda event: event.widget.selection_clear(),
            '<Delete>': lambda event, back = True: c.editCommands.killsentence(event,back),
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
    #@+node:ekr.20050920085536.13:addCallBackDict (miniBufferClass) MUST BE GENERALIZED
    def addCallBackDict (self):
    
        '''Create callback dictionary for masterCommand.'''
    
        k = self ; c = k.c
        
        cbDict = {
        
        # The big ones...
        'Alt-x':        k.alt_X,
        
        'Control-x':    k.startControlX, # Conflicts with XP cut.
        'Control-g':    k.keyboardQuit,
    
        # Standard Emacs moves...
        'Alt-less':     lambda event, spot = '1.0': c.editCommands.moveTo(event,spot),
        'Alt-greater':  lambda event, spot = 'end': c.editCommands.moveTo(event,spot),
        'Alt-a':        c.editCommands.backSentence,
        'Alt-e':        c.editCommands.forwardSentence,
        'Alt-f':       lambda event, way = 1: c.editCommands.moveword(event,way),
        'Alt-b':        lambda event, way = -1: c.editCommands.moveword(event,way),
        'Alt-braceright':   lambda event, which = 1: c.editCommands.movingParagraphs(event,which),
        'Alt-braceleft':    lambda event, which = 0: c.editCommands.movingParagraphs(event,which),
        'Control-Right':lambda event, way = 1: c.editCommands.moveword(event,way),
        'Control-Left': lambda event, way = -1: c.editCommands.moveword(event,way),
        'Control-a':    lambda event, spot = 'insert linestart': c.editCommands.moveTo(event,spot),
        'Control-e':    lambda event, spot = 'insert lineend': c.editCommands.moveTo(event,spot),
        'Control-p':    lambda event, which = 'Up': k.manufactureKeyPress(event,which),
        'Control-n':    lambda event, which = 'Down': k.manufactureKeyPress(event,which),
        # Conflicts with Find panel.
        # 'Control-f':    lambda event, which = 'Right': k.manufactureKeyPress(event,which),
        'Control-b':    lambda event, which = 'Left': k.manufactureKeyPress(event,which),
        
        # Standard Emacs deletes...
            # 'Control-d':        c.editCommands.deleteNextChar,
            # 'Alt-backslash':    c.editCommands.deleteSpaces,
            # 'Delete':       lambda event, which = 'BackSpace': k.manufactureKeyPress(event,which),
        
        # Kill buffer...
        'Control-k':    lambda event, frm = 'insert', to = 'insert lineend': k.kill(event,frm,to),
        'Alt-d':        lambda event, frm = 'insert wordstart', to = 'insert wordend': k.kill(event,frm,to),
        'Alt-Delete':   lambda event: c.editCommands.deletelastWord(event),
        "Alt-k":        lambda event: c.editCommands.killsentence(event),
        
        # Conflicts with Leo outline moves.
        #'Alt-Up':       lambda event, spot = 'insert linestart': c.editCommands.moveTo(event,spot),
        #'Alt-Down':     lambda event, spot = 'insert lineend': c.editCommands.moveTo(event,spot),
       
        # I wouldn't use these...
            # 'Control-o':    c.editCommands.insertNewLine,
            # "Control-y":    lambda event, frm = 'insert', which = 'c': c.walkKB(event,frm,which),
            # "Alt-y":        lambda event, frm = "insert", which = 'a': c.walkKB(event,frm,which),
            # 'Control-s':    None,
            # 'Control-r':    None,
            # 'Alt-c':        lambda event, which = 'cap': c.editCommands.capitalize(event,which),
            # 'Alt-u':        lambda event, which = 'up': c.editCommands.capitalize(event,which),
            # 'Alt-l':        lambda event, which = 'low': c.editCommands.capitalize(event,which),
            # 'Alt-t':        lambda event, sw = c.editCommands.swapSpots: c.editCommands.swapWords(event,sw),
        
        # Region stuff...
            # 'Control-Shift-at': c.editCommands.setRegion,
            # 'Control-w':    lambda event, which = 'd': c.editCommands.killRegion(event,which),
            # 'Alt-w':        lambda event, which = 'c': c.editCommands.killRegion(event,which),
            # 'Alt-Control-backslash': c.editCommands.indentRegion,
            # 'Alt-m':            c.editCommands.backToIndentation,
            # 'Alt-asciicircum':  c.editCommands.deleteIndentation,
    
        # Conflicts with swap panes.
            # 'Control-t':    c.editCommands.swapCharacters,
            
        # Misc.
            # 'Control-u':    None,
            # 'Control-l':    None,
            # 'Alt-z':        None,
            # 'Control-i':    None,
            # 'Alt-g':        None,
            # 'Control-v':    lambda event, way = 'south': c.editCommands.screenscroll(event,way),
            # 'Alt-v':        lambda event, way = 'north': c.editCommands.screenscroll(event,way),
            # 'Alt-equal':      c.editCommands.countRegion,
            # 'Alt-parenleft':  c.editCommands.insertParentheses,
            # 'Alt-parenright': c.editCommands.movePastClose,
            # 'Alt-percent':  None,
            # 'Control-c':    None,
            # 'Control-Alt-w': None,
            # 'Control-Alt-o': c.editCommands.insertNewLineIndent,
            # 'Control-j':    c.editCommands.insertNewLineAndTab,
            # 'Alt-minus':    k.negativeArgument,
            # 'Alt-slash':    c.editCommands.dynamicExpansion,
            # 'Control-Alt-slash':    c.editCommands.dynamicExpansion2,
            # 'Control-u':        lambda event, keystroke = '<Control-u>': k.universalDispatch(event,keystroke),
            # 'Alt-q':        c.editCommands.fillParagraph,
            # 'Alt-h':        c.editCommands.selectParagraph,
            # 'Alt-semicolon': c.editCommands.indentToCommentColumn,
            # 'Alt-s':            c.editCommands.centerLine,
            # 'Control-z':        c.controlCommands.suspend,
            # 'Control-Alt-s': c.searchCommands.isearchForwardRegexp,
                # ### Hmmm.  the lambda doesn't call keyboardQuit
                # # lambda event, stroke = '<Control-s>': k.startIncremental(event,stroke,which='regexp'),
            # 'Control-Alt-r': c.searchCommands.isearchBackwardRegexp,
                # # lambda event, stroke = '<Control-r>': k.startIncremental(event,stroke,which='regexp'),
            # 'Control-Alt-percent': lambda event: k.startRegexReplace()and k.masterQR(event),
            # 'Escape':       c.editCommands.watchEscape,
            # 'Alt-colon':    c.editCommands.startEvaluate,
            # 'Alt-exclam':   c.emacsControlCommands.startSubprocess,
            # 'Alt-bar':      lambda event: c.controlCommands.startSubprocess(event,which=1),
        
        # Numbered commands: conflict with Leo's Expand to level commands, but so what...
        'Alt-0': lambda event, stroke = '<Alt-0>', number = 0: k.numberCommand(event,stroke,number),
        'Alt-1': lambda event, stroke = '<Alt-1>', number = 1: k.numberCommand(event,stroke,number),
        'Alt-2': lambda event, stroke = '<Alt-2>', number = 2: k.numberCommand(event,stroke,number),
        'Alt-3': lambda event, stroke = '<Alt-3>', number = 3: k.numberCommand(event,stroke,number),
        'Alt-4': lambda event, stroke = '<Alt-4>', number = 4: k.numberCommand(event,stroke,number),
        'Alt-5': lambda event, stroke = '<Alt-5>', number = 5: k.numberCommand(event,stroke,number),
        'Alt-6': lambda event, stroke = '<Alt-6>', number = 6: k.numberCommand(event,stroke,number),
        'Alt-7': lambda event, stroke = '<Alt-7>', number = 7: k.numberCommand(event,stroke,number),
        'Alt-8': lambda event, stroke = '<Alt-8>', number = 8: k.numberCommand(event,stroke,number),
        'Alt-9': lambda event, stroke = '<Alt-9>', number = 9: k.numberCommand(event,stroke,number),
        
        # Emacs undo.
            # 'Control-underscore': k.doUndo,
        }
    
        return cbDict
    #@nonl
    #@-node:ekr.20050920085536.13:addCallBackDict (miniBufferClass) MUST BE GENERALIZED
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
    #@+node:ekr.20050920085536.16:bindKey (miniBufferHandlerClass)
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
    #@-node:ekr.20050920085536.16:bindKey (miniBufferHandlerClass)
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
    #@-node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    #@+node:ekr.20050920115444:setBufferInteractionMethods & helpers
    # Called by modified leoTkinterBody.createBindings.
    
    def setBufferInteractionMethods (self,buffer):
    
        '''This function configures the Emacs instance so that
           it can see all the nodes as buffers for its buffer commands.'''
           
        k = self ; c = k.c
    
        # These are actually methods of the bufferCommandsClass.
        #@    @+others
        #@+node:ekr.20050920115444.1:buildBufferList  (MAY BE BUGGY)
        def buildBufferList (self):
        
            '''Build a buffer list from an outline.'''
        
            d = {} ; self.positions.clear()
        
            for p in c.allNodes_iter():
                t = p.v.t ; h = t.headString()
                theList = self.positions.get(h,[])
                theList.append(p.copy())
                self.positions [h] = theList
                d [h] = t.bodyString()
        
            self.tnodes [c] = d
            return d
        #@nonl
        #@-node:ekr.20050920115444.1:buildBufferList  (MAY BE BUGGY)
        #@+node:ekr.20050920115444.2:setBufferData
        def setBufferData (name,data):
        
            data = unicode(data)
            tdict = self.tnodes [c]
            if tdict.has_key(name):
                tdict [name].bodyString = data
        #@nonl
        #@-node:ekr.20050920115444.2:setBufferData
        #@+node:ekr.20050920115444.3:gotoNode & gotoPosition
        def gotoNode (name):
        
            c.beginUpdate()
            try:
                if self.positions.has_key(name):
                    posis = self.positions [name]
                    if len(posis) > 1:
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
                            if cpos != None:
                                gotoPosition(c,posis[cpos])
                        lbox.bind('<Button-1>',setPos)
                        geometry = tl.geometry()
                        geometry = geometry.split('+')
                        geometry = geometry [0]
                        width = tl.winfo_screenwidth() / 3
                        height = tl.winfo_screenheight() / 3
                        geometry = '+%s+%s' % (width,height)
                        tl.geometry(geometry)
                    else:
                        pos = posis [0]
                        gotoPosition(c,pos)
                else:
                    pos2 = c.currentPosition()
                    tnd = leoNodes.tnode('',name)
                    pos = pos2.insertAfter(tnd)
                    gotoPosition(c,pos)
            finally:
                c.endUpdate()
        #@nonl
        #@+node:ekr.20050920115444.4:gotoPosition
        def gotoPosition (c,pos):
        
            c.frame.tree.expandAllAncestors(pos)
            c.selectPosition(pos)
        #@nonl
        #@-node:ekr.20050920115444.4:gotoPosition
        #@-node:ekr.20050920115444.3:gotoNode & gotoPosition
        #@+node:ekr.20050920115444.5:deleteNode
        def deleteNode (name):
        
            c.beginUpdate()
            try:
                if self.positions.has_key(name):
                    pos = self.positions [name]
                    cpos = c.currentPosition()
                    pos.doDelete(cpos)
            finally:
                c.endUpdate()
        #@nonl
        #@-node:ekr.20050920115444.5:deleteNode
        #@+node:ekr.20050920115444.6:renameNode
        def renameNode (name):
        
            c.beginUpdate()
            try:
                pos = c.currentPosition()
                pos.setHeadString(name)
            finally:
                c.endUpdate()
        #@nonl
        #@-node:ekr.20050920115444.6:renameNode
        #@-others
    
        # These add Leo-reated capabilities to the key handler.
        c.bufferCommands.setBufferListGetter(buffer,buildBufferList)
        c.bufferCommands.setBufferSetter(buffer,setBufferData)
        c.bufferCommands.setBufferGoto(buffer,gotoNode)
        c.bufferCommands.setBufferDelete(buffer,deleteNode)
        c.bufferCommands.setBufferRename(buffer,renameNode)
    #@nonl
    #@-node:ekr.20050920115444:setBufferInteractionMethods & helpers
    #@-node:ekr.20050920085536.1:Birth
    #@+node:ekr.20050920085536.4:undoer methods
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
    #@-node:ekr.20050920085536.4:undoer methods
    #@+node:ekr.20050923172809:State methods...
    #@+node:ekr.20050923172809.1:callStateFunction
    def callStateFunction (self,*args):
        
        k = self
    
        if k.state:
            flag, func = k.stateCommands [k.state]
    
            if flag == 1:
                return func(args[0])
            else:
                return func(*args)
    #@nonl
    #@-node:ekr.20050923172809.1:callStateFunction
    #@+node:ekr.20050923172814.1:clearState
    def clearState (self):
        
        k = self
    
        k.state = None
    
        for z in k.states.keys():
            k.states [z] = 0 # More useful than False.
    #@nonl
    #@-node:ekr.20050923172814.1:clearState
    #@+node:ekr.20050923172814.2:getState
    def getState (self,state):
        
        k = self
    
        return k.states.get(state,False)
    #@nonl
    #@-node:ekr.20050923172814.2:getState
    #@+node:ekr.20050923172814.3:hasState
    def hasState (self):
        
        k = self
    
        if k.state:
            return k.states [k.state]
    #@nonl
    #@-node:ekr.20050923172814.3:hasState
    #@+node:ekr.20050923172814.4:setState
    def setState (self,state,value):
        
        k = self
        k.state = state
        if state:
            k.states [state] = value
        else:
            k.clearState()
    #@nonl
    #@-node:ekr.20050923172814.4:setState
    #@+node:ekr.20050923172814.5:whichState
    def whichState (self):
        
        k = self
    
        return k.state
    #@nonl
    #@-node:ekr.20050923172814.5:whichState
    #@-node:ekr.20050923172809:State methods...
    #@+node:ekr.20050923174229.2:Keystroke methods
    #@+node:ekr.20050923174229.3:callKeystrokeFunction
    def callKeystrokeFunction (self,event,stroke):
        
        k = self
        
        numberOfArgs, func = k.keystrokes [stroke]
    
        if numberOfArgs == 1:
            return func(event)
        else:
            return func(event,stroke)
    #@nonl
    #@-node:ekr.20050923174229.3:callKeystrokeFunction
    #@+node:ekr.20050920085536.22:hasKeyStroke
    def hasKeyStroke (self,stroke):
        
        k = self
    
        return k.keystrokes.has_key(stroke)
    #@nonl
    #@-node:ekr.20050920085536.22:hasKeyStroke
    #@-node:ekr.20050923174229.2:Keystroke methods
    #@+node:ekr.20050920085536.57:ControlX methods
    #@+node:ekr.20050920085536.58:startControlX
    def startControlX (self,event):
    
        '''This method starts the Control-X command sequence.'''
        
        k = self
    
        k.setState('controlx',True)
        k.set('Control - X')
        k.setLabelBlue()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.58:startControlX
    #@+node:ekr.20050920085536.59:stopControlX
    def stopControlX (self,event): # event IS used.
    
        '''This method clears the state of the Emacs instance'''
        
        k = self ; c = k.c ; w = event.widget
    
        # This will all be migrated to keyboardQuit eventually.
        if c.controlCommands.shuttingdown:
            return
    
        c.rectangleCommands.sRect = False
        c.registerCommands.rectanglemode = 0
        
        k.clearState()
        w.tag_delete('color')
        w.tag_delete('color1')
    
        if c.registerCommands.registermode:
            c.registerCommands.deactivateRegister(event)
    
        k.bufferMode = None ### Correct???
        k.resetLabel()
        w.update_idletasks()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.59:stopControlX
    #@+node:ekr.20050920085536.60:doControlX
    def doControlX (self,event,stroke,previous=[]):
        
        k = self
        
        return k.callControlXFunction(event,stroke)
    #@nonl
    #@-node:ekr.20050920085536.60:doControlX
    #@+node:ekr.20050923183943.1:callControlXFunction
    def callControlXFunction (self,event,stroke):
        
        k = self
    
        k.previous.insert(0,event.keysym)
    
        if len(k.previous) > 10:
            k.previous.pop()
    
        if stroke in ('<Key>','<Escape>'):
            return k.processKey(event)  # Weird command-specific stuff.
    
        if stroke in k.xcommands:
            k.xcommands [stroke](event)
            if stroke != '<Control-b>':
                k.keyboardQuit(event)
    
        return 'break'
    #@-node:ekr.20050923183943.1:callControlXFunction
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
    #@+node:ekr.20050923183943.4:processKey (controlX_handlerClass) MUST BE GENERALIZED
    def processKey (self,event):
    
        k = self ; c = k.c ; previous = k.previous
        
        if event.keysym in ('Shift_L','Shift_R'):
            return
            
        g.trace(event.keysym)
    
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
            if k.processAbbreviation(event): return 'break'
    
        if event.keysym == 'g':
            l = k.get()
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
    #@-node:ekr.20050923183943.4:processKey (controlX_handlerClass) MUST BE GENERALIZED
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
    
        if k.get() != 'a' and event.keysym == 'a':
            k.set('a')
            return 'break'
    
        elif k.get() == 'a':
            if char == 'i':
                k.set('a i')
            elif char == 'e':
                k.stopControlX(event)
                event.char = ''
                k.expandAbbrev(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050923183943.6:processAbbreviation MUST BE GENERALIZED
    #@-node:ekr.20050920085536.57:ControlX methods
    #@+node:ekr.20050920085536.7:MiniBuffer methods
    #@+node:ekr.20050920085536.32: Entry points
    # These are user commands accessible via alt-x.
    
    def digitArgument (self,event):
        
        k = self
    
        return k.universalDispatch(event,'')
    
    def universalArgument (self,event):
        
        k = self
    
        return k.universalDispatch(event,'')
    #@nonl
    #@+node:ekr.20050920085536.73:universalDispatch
    def universalDispatch (self,event,stroke):
    
        k = self
        
        state = k.getState('uC')
        if state == 0:
            k.setState('uC',1)
            k.set('')
            k.setLabelBlue()
        elif state == 1:
            k.universalCommand1(event,stroke)
        elif state == 2:
            k.universalCommand3(event,stroke)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.73:universalDispatch
    #@+node:ekr.20050920085536.74:universalCommand1
    def universalCommand1 (self,event,stroke):
        
        k = self
    
        if event.char not in k.uCstring:
            return k.universalCommand2(event,stroke)
     
        k.update(event)
    
        if event.char != '\b':
            k.set('%s ' % k.get())
    #@nonl
    #@-node:ekr.20050920085536.74:universalCommand1
    #@+node:ekr.20050920085536.75:universalCommand2
    def universalCommand2 (self,event,stroke):
        
        k = self ; w = event.widget # event IS used.
        txt = k.get()
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
    #@-node:ekr.20050920085536.75:universalCommand2
    #@+node:ekr.20050920085536.76:universalCommand3
    def universalCommand3 (self,event,stroke):
        
        k = self
        k.set('Control-u %s' % stroke.lstrip('<').rstrip('>'))
        k.setLabelBlue()
    
        if event.keysym == 'parenleft':
            k.keyboardQuit(event)
            c.macroCommands.startKBDMacro(event)
            c.macroCommands.executeLastMacro(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920085536.76:universalCommand3
    #@+node:ekr.20050920085536.77:numberCommand
    def numberCommand (self,event,stroke,number): # event IS used.
    
        k = self
    
        k.universalDispatch(event,stroke)
        event.widget.event_generate('<Key>',keysym=number)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.77:numberCommand
    #@-node:ekr.20050920085536.32: Entry points
    #@+node:ekr.20050920085536.33: Getters & Setters
    #@+node:ekr.20050920085536.34:setEvent
    def setEvent (self,event,l):
    
        event.keysym = l
        return event
    #@nonl
    #@-node:ekr.20050920085536.34:setEvent
    #@+node:ekr.20050920085536.35:setLabelGrey
    def setLabelGrey (self):
        
        k = self
    
        k.widget.configure(background='lightgrey')
    #@nonl
    #@-node:ekr.20050920085536.35:setLabelGrey
    #@+node:ekr.20050920085536.36:setLabelBlue
    def setLabelBlue (self):
        
        k = self
    
        k.widget.configure(background='lightblue')
    #@nonl
    #@-node:ekr.20050920085536.36:setLabelBlue
    #@+node:ekr.20050920085536.37:resetLabel
    def resetLabel (self):
        
        k = self
    
        k.set('')
        k.setLabelGrey()
        k.altX_prefix = ''
    #@nonl
    #@-node:ekr.20050920085536.37:resetLabel
    #@+node:ekr.20050920085536.38:update
    def update (self,event):
    
        '''
        Alters the StringVar svar to represent the change in the event.
        This has the effect of changing the miniBuffer contents.
    
        It mimics what would happen with the keyboard and a Text editor
        instead of plain accumalation.'''
        
        k = self ; s = k.get() ; ch = event.char
    
        if ch == '\b': # Handle backspace.
            # Don't backspace over the prompt.
            if len(s) <= k.altX_prefix:
                return 
            elif len(s) == 1: s = ''
            else: s = s [0:-1]
        else:
            # Add the character.
            s = s + ch
    
        k.set(s)
    #@nonl
    #@-node:ekr.20050920085536.38:update
    #@-node:ekr.20050920085536.33: Getters & Setters
    #@+node:ekr.20050920085536.39:get & set
    def get (self,ignorePrompt=False):
        
        k = self ; s = k.svar.get()
        if ignorePrompt:
            return s[len(k.altX_prefix):]
        else:
            return s
    
    def set (self,s,protect=False):
        
        k = self
        k.svar.set(s)
        if protect:
            k.altX_prefix = s
    #@nonl
    #@-node:ekr.20050920085536.39:get & set
    #@+node:ekr.20050920085536.40:Alt_X methods
    #@+node:ekr.20050920085536.41:alt_X
    def alt_X (self,event=None,which=''):
    
        k = self
    
        k.setState('altx',which or 1) # Must be int, not True.
    
        if which:
            k.set('%s %s' % (which,k.alt_x_prompt),protect=True)
        else:
            k.set('%s' % (k.alt_x_prompt),protect=True)
    
        k.setLabelBlue()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.41:alt_X
    #@+node:ekr.20050920085536.42:doAlt_X & helpers
    def doAlt_X (self,event):
    
        '''This method executes the correct Alt-X command'''
        
        k = self ; c = k.c ; keysym = event.keysym
        # g.trace(keysym)
    
        if keysym == 'Return':
            #@        << dispatch the function >>
            #@+node:ekr.20050920085536.45:<< dispatch the function >>
            s = k.get()
            k.altX_tabList = []
            command = s[len(k.altX_prefix):].strip()
            func = c.commandsDict.get(command)
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
                k.set('Command does not exist')
            #@nonl
            #@-node:ekr.20050920085536.45:<< dispatch the function >>
            #@nl
        elif keysym == 'Tab':
            #@        << handle tab completion >>
            #@+node:ekr.20050920085536.44:<< handle tab completion >>
            s = k.get().strip()
            
            if k.altX_tabList and s.startswith(k.altX_tabListPrefix):
                k.altX_tabListIndex +=1
                if k.altX_tabListIndex >= len(k.altX_tabList):
                    k.altX_tabListIndex = 0
                k.set(k.alt_x_prompt + k.altX_tabList [k.altX_tabListIndex])
            else:
                s = k.get() # Always includes prefix, so command is well defined.
                k.altX_tabListPrefix = s
                command = s [len(k.alt_x_prompt):]
                k.altX_tabList,common_prefix = k._findMatch(command)
                k.altX_tabListIndex = 0
                if k.altX_tabList:
                    if len(k.altX_tabList) > 1 and (
                        len(common_prefix) > (len(k.altX_tabListPrefix) - len(k.alt_x_prompt))
                    ):
                        k.set(k.alt_x_prompt + common_prefix)
                        k.altX_tabListPrefix = k.alt_x_prompt + common_prefix
                    else:
                        # No common prefix, so show the first item.
                        k.set(k.alt_x_prompt + k.altX_tabList [0])
                else:
                    k.set(k.alt_x_prompt,protect=True)
            #@nonl
            #@-node:ekr.20050920085536.44:<< handle tab completion >>
            #@nl
        elif keysym == 'BackSpace':
            #@        << handle BackSpace >>
            #@+node:ekr.20050920085536.46:<< handle BackSpace >>
            # Cut back to previous prefix and update prefix.
            s = k.altX_tabListPrefix
            
            if len(s) > len(k.altX_prefix):
                k.altX_tabListPrefix = s[:-1]
                k.set(k.altX_tabListPrefix,protect=False)
            else:
                k.altX_tabListPrefix = s
                k.set(k.altX_tabListPrefix,protect=True)
                
            # g.trace('BackSpace: new altX_tabListPrefix',k.altX_tabListPrefix)
            
            # Force a recomputation of the commands list.
            k.altX_tabList = []
            #@nonl
            #@-node:ekr.20050920085536.46:<< handle BackSpace >>
            #@nl
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.altX_tabList = []
            k.update(event)
            k.altX_tabListPrefix = k.get()
            # g.trace('new prefix',k.altX_tabListPrefix)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.43:_findMatch
    def _findMatch (self,s,fdict=None):
        
        '''This method returns a sorted list of matches.'''
    
        k = self ; c = k.c
    
        if not fdict:
            fdict = c.commandsDict
    
        common_prefix = ''
    
        if s: pmatches = [a for a in fdict if a.startswith(s)]
        else: pmatches = []
            
        if pmatches:
            s = pmatches[0] ; done = False
            for i in xrange(len(s)):
                prefix = s[:i]
                for z in pmatches:
                    if not z.startswith(prefix):
                        done = True ; break
                if done:
                    break
                else:
                    common_prefix = prefix
            pmatches.sort()
    
        # g.trace(repr(s),len(pmatches))
        return pmatches,common_prefix
    #@nonl
    #@-node:ekr.20050920085536.43:_findMatch
    #@-node:ekr.20050920085536.42:doAlt_X & helpers
    #@+node:ekr.20050920085536.47:executeLastAltX
    def executeLastAltX (self,event):
        
        k = self ; c = k.c
    
        if event.keysym == 'Return' and k.altX_history:
            last = k.altX_history [0]
            c.commandsDict [last](event)
            return 'break'
        else:
            return k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20050920085536.47:executeLastAltX
    #@+node:ekr.20050920085536.48:repeatComplexCommand
    def repeatComplexCommand (self,event):
    
        k = self
    
        k.keyboardQuit(event)
    
        if k.altX_history:
            k.setLabelBlue()
            k.set("Redo: %s" % k.altX_history[0])
            k.setState('last-altx',True)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.48:repeatComplexCommand
    #@-node:ekr.20050920085536.40:Alt_X methods
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
    #@+node:ekr.20050920085536.62:getArg
    def getArg (self,event,returnStateKind=None,returnState=None):
        
        '''Accumulate an argument until the user hits return (or control-g).
        Enter the 'return' state when done.'''
        
        k = self ; stateKind = 'getArg'
        state = k.getState(stateKind)
        if not state:
            k.altX_prefix = len(k.get()) ; k.arg = ''
            k.afterGetArgState = (returnStateKind,returnState)
            k.setState(stateKind,1)
        elif event.keysym == 'Return':
            # Compute the actual arg.
            s = k.get() ; k.arg = s[len(k.altX_prefix):]
            # Immediately enter the caller's requested state.
            k.clearState()
            stateKind,state = k.afterGetArgState
            k.setState(stateKind,state)
            k.callStateFunction(event,None)
        else:
            k.update(event)
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.62:getArg
    #@+node:ekr.20050920085536.63:keyboardQuit
    def keyboardQuit (self,event):  # The event arg IS used.
    
        '''This method cleans the Emacs instance of state and ceases current operations.'''
        
        k = self
    
        return k.stopControlX(event) # This method will eventually contain the stopControlX code.
    #@nonl
    #@-node:ekr.20050920085536.63:keyboardQuit
    #@+node:ekr.20050920085536.64:manufactureKeyPress
    def manufactureKeyPress (self,event,which): # event **is** used.
    
        w = event.widget
        w.event_generate('<Key>',keysym=which)
        w.update_idletasks()
        
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.64:manufactureKeyPress
    #@+node:ekr.20050920085536.65:masterCommand (miniBufferHandlerClass)
    def masterCommand (self,event,method,stroke,general):
        
        '''This is the central routing method of the Emacs class.
        All commands and keystrokes pass through here.'''
        
        # Note: the _L symbols represent *either* special key.
        k = self ; c = k.c
        special = event.keysym in ('Control_L','Alt_L','Shift_L')
    
        inserted = not special or (
            not general and (len(k.keysymhistory) == 0 or k.keysymhistory [0] != event.keysym))
    
        if inserted:
            # g.trace(general,event.keysym)
            #@        << add character to history >>
            #@+node:ekr.20050920085536.67:<< add character to history >>
            # Don't add multiple special characters to history.
            
            k.keysymhistory.insert(0,event.keysym)
            
            if len(event.char) > 0:
                if len(keyHandlerClass.lossage) > 99:
                    keyHandlerClass.lossage.pop()
                keyHandlerClass.lossage.insert(0,event.char)
            
            if 0: # traces
                g.trace(event.keysym,stroke)
                g.trace(k.keysymhistory)
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
    
        # Important: This effectively over-rides the handling of most keystrokes with a state.
        if k.hasState():
            # g.trace('hasState')
            k.previousStroke = stroke
            return k.callStateFunction(event,stroke)
    
        if k.hasKeyStroke(stroke):
            g.trace('hasKeyStroke')
            k.previousStroke = stroke
            k.callKeystrokeFunction(event,stroke)
    
        if k.regXRpl: # EKR: a generator.
            try:
                k.regXKey = event.keysym
                k.regXRpl.next() # EKR: next() may throw StopIteration.
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
            # g.trace('default')
            return c.frame.body.onBodyKey(event)
    #@nonl
    #@-node:ekr.20050920085536.65:masterCommand (miniBufferHandlerClass)
    #@+node:ekr.20050920085536.68:negativeArgument
    def negativeArgument (self,event,stroke=None):
    
        k = self
    
        k.set("Negative Argument")
        k.setLabelBlue()
    
        state = k.getState('negativeArg')
        if state == 0:
            k.setState('negativeArg',1)
        else:
            func = k.negArgs.get(stroke)
            if func:
                func(event,stroke)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920085536.68:negativeArgument
    #@+node:ekr.20050920085536.69:tailEnd methods
    #@+node:ekr.20050920085536.70:_tailEnd
    def _tailEnd (self,w):
        
        '''This returns the tailEnd function that has been configure for the w parameter.'''
        
        k = self
        func = k.tailEnds.get(w)
        if func:
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
    #@-node:ekr.20050920085536.69:tailEnd methods
    #@-node:ekr.20050920085536.7:MiniBuffer methods
    #@-others
#@nonl
#@-node:ekr.20050920085536:class keyHandler
#@-others
#@nonl
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
