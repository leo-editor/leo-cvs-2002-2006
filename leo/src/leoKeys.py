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
#@+node:ekr.20050920085536:class keyHandler (replaces Emacs class)
class keyHandlerClass:
    
    '''A class to support emacs-style commands.  Creates a Tk Text widget for the minibufer.'''

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
        c.frame.
        
        Use tbuffer (a Tk Text widget) and miniBufferWidget (a Tk Label) if provided.
        Otherwise, the caller must call setBufferStrokes.
        
        useGlobalRegisters and useGlobalKillbuffer indicate whether to use
        global (class vars) or per-instance (ivars) for kill buffers and registers.'''
    
        # g.trace('keyHandler',self)
        
        self.c = c
        if not self.c.frame.miniBufferWidget:
            g.trace('no widget')
            return
    
        self.tbuffer = c.frame.miniBufferWidget
    
        self.undoers = {} # Emacs instance tracks undoers given to it.
        self.useGlobalKillbuffer = useGlobalKillbuffer
        self.useGlobalRegisters = useGlobalRegisters
    
        # For communication between keystroke handlers and other classes.
        self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
        self.regXKey = None
       
        # Create helper classes.  Order is important here...
        self.miniBufferHandler = self.miniBufferHandlerClass(self,c.frame.miniBufferWidget)
    
        # Define delegators before calling finishCreate.
        self.stateManager = self.miniBufferHandler.stateManager
        self.kstrokeManager = self.miniBufferHandler.kstrokeManager
        self.keyboardQuit   = self.miniBufferHandler.keyboardQuit
        self.setEvent       = self.miniBufferHandler.setEvent
    #@nonl
    #@-node:ekr.20050920085536.2: ctor (keyHandler)
    #@+node:ekr.20050920094633:finishCreate (keyHandler)
    def finishCreate (self,altX_commandsDict):
        
        # g.trace('keyHandler')
        
        keyHandler = self ; b = self.miniBufferHandler
        c = self.c ; frame = c.frame
    
        b.finishCreate(altX_commandsDict)
        b.setBufferStrokes(c.frame.bodyCtrl)
        self.setUndoer(c.frame.bodyCtrl,c.undoer.undo)
        
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
        b.setTailEnd(frame.bodyCtrl,utTailEnd)
        c.controlCommands.setShutdownHook(c.close)
        
        if 0:
            addTemacsExtensions(keyHandler)
            addTemacsAbbreviations(keyHandler)
            changeKeyStrokes(keyHandler,frame.bodyCtrl)
    
        if 1: # This is dubious.
            keyHandler.setBufferInteractionMethods(frame.bodyCtrl)
    #@nonl
    #@-node:ekr.20050920094633:finishCreate (keyHandler)
    #@+node:ekr.20050920115444:setBufferInteractionMethods & helpers
    # Called by modified leoTkinterBody.createBindings.
    
    def setBufferInteractionMethods (self,buffer):
    
        '''This function configures the Emacs instance so that
           it can see all the nodes as buffers for its buffer commands.'''
           
        c = self.c
    
        # These are actually methods of the bufferCommandsClass.
        #@    @+others
        #@+node:ekr.20050920115444.1:buildBufferList  (MAY BE BUGGY)
        def buildBufferList (self):
        
            '''Build a buffer list from an outline.'''
        
            c = self.c
        
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
    #@+node:ekr.20050920085536.4:undoer methods
    #@+at
    # Emacs requires an undo mechanism be added from the environment.
    # If there is no undo mechanism added, there will be no undo functionality 
    # in the instance.
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050920085536.5:setUndoer
    def setUndoer (self,tbuffer,undoer):
        '''This method sets the undoer method for the Emacs instance.'''
        self.undoers [tbuffer] = undoer
    #@nonl
    #@-node:ekr.20050920085536.5:setUndoer
    #@+node:ekr.20050920085536.6:doUndo
    def doUndo (self,event,amount=1):
        
        tbuffer = event.widget
        if self.undoers.has_key(tbuffer):
            for z in xrange(amount):
                self.undoers [tbuffer] ()
        return 'break'
    #@-node:ekr.20050920085536.6:doUndo
    #@-others
    #@nonl
    #@-node:ekr.20050920085536.4:undoer methods
    #@-node:ekr.20050920085536.1:Birth
    #@+node:ekr.20050920085536.7:class miniBufferHandlerClass
    class miniBufferHandlerClass:
    
        #@    @+others
        #@+node:ekr.20050920085536.8: Birth
        #@+node:ekr.20050920085536.9: ctor (miniBuffer)
        def __init__ (self,keyHandler,widget):
        
            self.keyHandler = keyHandler
            self.c = keyHandler.c
            self.widget = widget # A Tk Label widget.
            # Permanently associate a Tk.StringVar with the widget.
            self.svar = Tk.StringVar()
            self.widget.configure(textvariable=self.svar)
        
            # Ivars.
            self.altX_history = []
            self.altX_prefix = ''
            self.altX_tabListPrefix = ''
            self.altX_tabList = []
            self.altX_tabListIndex = -1
            self.keysymhistory = []
            self.previousStroke = ''
            self.svars = {}
            self.tailEnds = {} # functions to execute at the end of many Emac methods.  Configurable by environment.
            
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
        
            self.stateManager = self.stateManagerClass(keyHandler) # Manages state for the master command
            self.kstrokeManager = self.keyStrokeManagerClass(keyHandler) # Manages some keystroke state for the master command.
            self.cxHandler = self.controlX_handlerClass(keyHandler) # Create the handler for Control-x commands
            
            # Delegators.  These will go away if the state helper class goes away.
            self.getState = self.stateManager.getState
            self.setState = self.stateManager.setState
            self.hasState = self.stateManager.hasState
            self.whichState = self.stateManager.whichState
        #@nonl
        #@-node:ekr.20050920085536.9: ctor (miniBuffer)
        #@+node:ekr.20050920085536.10: finishCreate (miniBufferClass) MUST BE GENERALIZED
        def finishCreate (self,altX_commandsDict):
            
            # g.trace('miniBufferClass')
        
            c = self.c ; keyHandler = self.keyHandler
        
            # Finish creating the helper classes.
            self.stateManager.finishCreate()
            self.kstrokeManager.finishCreate()
            self.cxHandler.finishCreate()
        
            # Finish this class.
            self.add_ekr_altx_commands()
        
            # Command bindings.
            self.cbDict = self.addCallBackDict() # Creates callback dictionary, primarily used in the master command
        
            self.negArgs = {
                '<Alt-c>': self.c.editCommands.changePreviousWord,
                '<Alt-u>': self.c.editCommands.changePreviousWord,
                '<Alt-l>': self.c.editCommands.changePreviousWord,
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
        #@-node:ekr.20050920085536.10: finishCreate (miniBufferClass) MUST BE GENERALIZED
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
        
            b = self ; c = self.c
            
            if 0:
                #@        << old cbDict >>
                #@+node:ekr.20050920085536.14:<< old cbDict >>
                cbDict = {
                    # These are very hard to get right.
                        #'KeyRelease-Alt_L':        self.alt_X, # Bare alt keys 
                        #'KeyRelease-Control_L':    self.alt_X, # Bare control keys
                    'Alt-less':     lambda event, spot = '1.0': c.editCommands.moveTo(event,spot),
                    'Alt-greater':  lambda event, spot = 'end': c.editCommands.moveTo(event,spot),
                    'Control-Right': lambda event, way = 1: c.editCommands.moveword(event,way),
                    'Control-Left': lambda event, way = -1: c.editCommands.moveword(event,way),
                    'Control-a':    lambda event, spot = 'insert linestart': c.editCommands.moveTo(event,spot),
                    'Control-e':    lambda event, spot = 'insert lineend': c.editCommands.moveTo(event,spot),
                    'Alt-Up':       lambda event, spot = 'insert linestart': c.editCommands.moveTo(event,spot),
                    'Alt-Down':     lambda event, spot = 'insert lineend': c.editCommands.moveTo(event,spot),
                    'Alt-f':        lambda event, way = 1: c.editCommands.moveword(event,way),
                    'Alt-b':        lambda event, way = -1: c.editCommands.moveword(event,way),
                    'Control-o':    c.editCommands.insertNewLine,
                    'Control-k':    lambda event, frm = 'insert', to = 'insert lineend': b.kill(event,frm,to),
                    'Alt-d':        lambda event, frm = 'insert wordstart', to = 'insert wordend': b.kill(event,frm,to),
                    'Alt-Delete':   lambda event: c.killBufferCommands.deletelastWord(event),
                    "Control-y":    lambda event, frm = 'insert', which = 'c': b.walkKB(event,frm,which),
                    "Alt-y":        lambda event, frm = "insert", which = 'a': b.walkKB(event,frm,which),
                    "Alt-k":        lambda event: c.killsentence(event),
                    'Control-s':    None,
                    'Control-r':    None,
                    'Alt-c':        lambda event, which = 'cap': c.editCommands.capitalize(event,which),
                    'Alt-u':        lambda event, which = 'up': c.editCommands.capitalize(event,which),
                    'Alt-l':        lambda event, which = 'low': c.editCommands.capitalize(event,which),
                    'Alt-t':        lambda event, sw = c.editCommands.swapSpots: c.editCommands.swapWords(event,sw),
                    'Alt-x':        self.alt_X,
                    'Control-x':    self.startControlX,
                    'Control-g':    b.keyboardQuit,
                    'Control-Shift-at': c.editCommands.setRegion,
                    'Control-w':    lambda event, which = 'd': c.editCommands.killRegion(event,which),
                    'Alt-w':        lambda event, which = 'c': c.editCommands.killRegion(event,which),
                    'Control-t':    c.editCommands.swapCharacters,
                    'Control-u':    None,
                    'Control-l':    None,
                    'Alt-z':        None,
                    'Control-i':    None,
                    'Alt-Control-backslash': c.editCommands.indentRegion,
                    'Alt-m':            c.editCommands.backToIndentation,
                    'Alt-asciicircum':  c.editCommands.deleteIndentation,
                    'Control-d':        c.editCommands.deleteNextChar,
                    'Alt-backslash':    c.editCommands.deleteSpaces,
                    'Alt-g':        None,
                    'Control-v':    lambda event, way = 'south': c.editCommands.screenscroll(event,way),
                    'Alt-v':        lambda event, way = 'north': c.editCommands.screenscroll(event,way),
                    'Alt-equal':    c.editCommands.countRegion,
                    'Alt-parenleft':    c.editCommands.insertParentheses,
                    'Alt-parenright':   c.editCommands.movePastClose,
                    'Alt-percent':  None,
                    'Control-c':    None,
                    'Delete':       lambda event, which = 'BackSpace': self.manufactureKeyPress(event,which),
                    'Control-p':    lambda event, which = 'Up': self.manufactureKeyPress(event,which),
                    'Control-n':    lambda event, which = 'Down': self.manufactureKeyPress(event,which),
                    'Control-f':    lambda event, which = 'Right': self.manufactureKeyPress(event,which),
                    'Control-b':    lambda event, which = 'Left': self.manufactureKeyPress(event,which),
                    'Control-Alt-w': None,
                    'Alt-a':        c.editCommands.backSentence,
                    'Alt-e':        c.editCommands.forwardSentence,
                    'Control-Alt-o': c.editCommands.insertNewLineIndent,
                    'Control-j':    c.editCommands.insertNewLineAndTab,
                    'Alt-minus':    self.negativeArgument,
                    'Alt-slash':    c.editCommands.dynamicExpansion,
                    'Control-Alt-slash':    c.editCommands.dynamicExpansion2,
                    'Control-u':        lambda event, keystroke = '<Control-u>': self.universalDispatch(event,keystroke),
                    'Alt-braceright':   lambda event, which = 1: c.editCommands.movingParagraphs(event,which),
                    'Alt-braceleft':    lambda event, which = 0: c.editCommands.editCommandscs.movingParagraphs(event,which),
                    'Alt-q':        c.editCommands.fillParagraph,
                    'Alt-h':        c.editCommands.selectParagraph,
                    'Alt-semicolon': c.editCommands.indentToCommentColumn,
                    'Alt-0': lambda event, stroke = '<Alt-0>', number = 0: b.numberCommand(event,stroke,number),
                    'Alt-1': lambda event, stroke = '<Alt-1>', number = 1: b.numberCommand(event,stroke,number),
                    'Alt-2': lambda event, stroke = '<Alt-2>', number = 2: b.numberCommand(event,stroke,number),
                    'Alt-3': lambda event, stroke = '<Alt-3>', number = 3: b.numberCommand(event,stroke,number),
                    'Alt-4': lambda event, stroke = '<Alt-4>', number = 4: b.numberCommand(event,stroke,number),
                    'Alt-5': lambda event, stroke = '<Alt-5>', number = 5: b.numberCommand(event,stroke,number),
                    'Alt-6': lambda event, stroke = '<Alt-6>', number = 6: b.numberCommand(event,stroke,number),
                    'Alt-7': lambda event, stroke = '<Alt-7>', number = 7: b.numberCommand(event,stroke,number),
                    'Alt-8': lambda event, stroke = '<Alt-8>', number = 8: b.numberCommand(event,stroke,number),
                    'Alt-9': lambda event, stroke = '<Alt-9>', number = 9: b.numberCommand(event,stroke,number),
                    'Control-underscore': c.editCommands.doUndo,
                    'Alt-s':            c.editCommands.centerLine,
                    'Control-z':        c.controlCommands.suspend,
                    'Control-Alt-s': c.searchCommands.isearchForwardRegexp,
                        ### Hmmm.  the lambda doesn't call keyboardQuit
                        # lambda event, stroke = '<Control-s>': b.startIncremental(event,stroke,which='regexp'),
                    'Control-Alt-r': c.searchCommands.isearchBackwardRegexp,
                        # lambda event, stroke = '<Control-r>': b.startIncremental(event,stroke,which='regexp'),
                    'Control-Alt-percent': lambda event: b.startRegexReplace()and b.masterQR(event),
                    'Escape':       c.editCommands.watchEscape,
                    'Alt-colon':    c.editCommands.startEvaluate,
                    'Alt-exclam':   c.controlCommands.startSubprocess,
                    'Alt-bar':      lambda event: c.controlCommands.startSubprocess(event,which=1),
                }
                #@nonl
                #@-node:ekr.20050920085536.14:<< old cbDict >>
                #@nl
            
            cbDict = {
            
            # The big ones...
            'Alt-x':        self.alt_X,
            
            'Control-x':    self.startControlX, # Conflicts with XP cut.
            'Control-g':    b.keyboardQuit,
        
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
            'Control-p':    lambda event, which = 'Up': b.manufactureKeyPress(event,which),
            'Control-n':    lambda event, which = 'Down': b.manufactureKeyPress(event,which),
            # Conflicts with Find panel.
            # 'Control-f':    lambda event, which = 'Right': self.manufactureKeyPress(event,which),
            'Control-b':    lambda event, which = 'Left': self.manufactureKeyPress(event,which),
            
            # Standard Emacs deletes...
                # 'Control-d':        c.editCommands.deleteNextChar,
                # 'Alt-backslash':    c.editCommands.deleteSpaces,
                # 'Delete':       lambda event, which = 'BackSpace': self.manufactureKeyPress(event,which),
            
            # Kill buffer...
            'Control-k':    lambda event, frm = 'insert', to = 'insert lineend': b.kill(event,frm,to),
            'Alt-d':        lambda event, frm = 'insert wordstart', to = 'insert wordend': b.kill(event,frm,to),
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
                # 'Alt-minus':    b.negativeArgument,
                # 'Alt-slash':    c.editCommands.dynamicExpansion,
                # 'Control-Alt-slash':    c.editCommands.dynamicExpansion2,
                # 'Control-u':        lambda event, keystroke = '<Control-u>': b.universalDispatch(event,keystroke),
                # 'Alt-q':        c.editCommands.fillParagraph,
                # 'Alt-h':        c.editCommands.selectParagraph,
                # 'Alt-semicolon': c.editCommands.indentToCommentColumn,
                # 'Alt-s':            c.editCommands.centerLine,
                # 'Control-z':        c.controlCommands.suspend,
                # 'Control-Alt-s': c.searchCommands.isearchForwardRegexp,
                    # ### Hmmm.  the lambda doesn't call keyboardQuit
                    # # lambda event, stroke = '<Control-s>': b.startIncremental(event,stroke,which='regexp'),
                # 'Control-Alt-r': c.searchCommands.isearchBackwardRegexp,
                    # # lambda event, stroke = '<Control-r>': b.startIncremental(event,stroke,which='regexp'),
                # 'Control-Alt-percent': lambda event: b.startRegexReplace()and b.masterQR(event),
                # 'Escape':       c.editCommands.watchEscape,
                # 'Alt-colon':    c.editCommands.startEvaluate,
                # 'Alt-exclam':   c.emacsControlCommands.startSubprocess,
                # 'Alt-bar':      lambda event: c.controlCommands.startSubprocess(event,which=1),
            
            # Numbered commands: conflict with Leo's Expand to level commands, but so what...
            'Alt-0': lambda event, stroke = '<Alt-0>', number = 0: b.numberCommand(event,stroke,number),
            'Alt-1': lambda event, stroke = '<Alt-1>', number = 1: b.numberCommand(event,stroke,number),
            'Alt-2': lambda event, stroke = '<Alt-2>', number = 2: b.numberCommand(event,stroke,number),
            'Alt-3': lambda event, stroke = '<Alt-3>', number = 3: b.numberCommand(event,stroke,number),
            'Alt-4': lambda event, stroke = '<Alt-4>', number = 4: b.numberCommand(event,stroke,number),
            'Alt-5': lambda event, stroke = '<Alt-5>', number = 5: b.numberCommand(event,stroke,number),
            'Alt-6': lambda event, stroke = '<Alt-6>', number = 6: b.numberCommand(event,stroke,number),
            'Alt-7': lambda event, stroke = '<Alt-7>', number = 7: b.numberCommand(event,stroke,number),
            'Alt-8': lambda event, stroke = '<Alt-8>', number = 8: b.numberCommand(event,stroke,number),
            'Alt-9': lambda event, stroke = '<Alt-9>', number = 9: b.numberCommand(event,stroke,number),
            
            # Emacs undo.
                # 'Control-underscore': b.doUndo,
            }
        
            return cbDict
        #@nonl
        #@-node:ekr.20050920085536.13:addCallBackDict (miniBufferClass) MUST BE GENERALIZED
        #@+node:ekr.20050920085536.15:addToDoAltX
        def addToDoAltX (self,name,macro):
        
            '''Adds macro to Alt-X commands.'''
            
            c = self.c
        
            if c.commandsDict.has_key(name):
                return False
        
            def exe (event,macro=macro):
                self.stopControlX(event)
                return self._executeMacro(macro,event.widget)
        
            c.commandsDict [name] = exe
            self.namedMacros [name] = macro
            return True
        #@nonl
        #@-node:ekr.20050920085536.15:addToDoAltX
        #@+node:ekr.20050920085536.16:bindKey (miniBufferHandlerClass)
        def bindKey (self,tbuffer,evstring):
        
            callback = self.cbDict.get(evstring)
            evstring = '<%s>' % evstring
            
            # g.trace(evstring)
        
            def f (event):
                general = evstring == '<Key>'
                return self.masterCommand(event,callback,evstring,general)
        
            if evstring == '<Key>':
                tbuffer.bind(evstring,f,'+')
            else:
                tbuffer.bind(evstring,f)
        #@nonl
        #@-node:ekr.20050920085536.16:bindKey (miniBufferHandlerClass)
        #@+node:ekr.20050920085536.17:setBufferStrokes  (creates svars & <key> bindings)
        def setBufferStrokes (self,tbuffer):
        
            '''Sets key bindings for a Tk Text widget.'''
        
            # Create one binding for each entry in cbDict.
            for key in self.cbDict:
                self.bindKey(tbuffer,key)
        
            # Add a binding for <Key> events, so _all_ key events go through masterCommand.
            self.bindKey(tbuffer,'Key')
        #@nonl
        #@-node:ekr.20050920085536.17:setBufferStrokes  (creates svars & <key> bindings)
        #@-node:ekr.20050920085536.8: Birth
        #@+node:ekr.20050920085536.49: class controlX_handlerClass MUST BE GENERALIZED
        class controlX_handlerClass:
        
            '''The ControlXHandler manages how the Control-X based commands operate on the
               Emacs instance.'''    
            
            #@    @+others
            #@+node:ekr.20050920085536.50:__init__
            def __init__ (self,keyHandler):
            
                self.c = keyHandler.c
                self.keyHandler = keyHandler
                self.previous = []
            
                # These are set in miniBuffer.finishCreate.
                self.rect_commands = {}
                self.variety_commands = {}
                self.abbreviationDispatch = {}
                self.register_commands = {}
            #@nonl
            #@-node:ekr.20050920085536.50:__init__
            #@+node:ekr.20050920085536.51:__call__
            def __call__ (self,event,stroke):
                
                keyHandler = self.keyHandler
            
                self.previous.insert(0,event.keysym)
            
                if len(self.previous) > 10:
                    self.previous.pop()
            
                if stroke in ('<Key>','<Escape>'):
                    return self.processKey(event)  # Weird command-specific stuff.
            
                if stroke in self.miniBufferHandler.xcommands:
                    keyHandler.xcommands [stroke](event)
                    if stroke != '<Control-b>':
                        keyHandler.keyboardQuit(event)
            
                return 'break'
            #@-node:ekr.20050920085536.51:__call__
            #@+node:ekr.20050920085536.52:finishCreate (controlX_handlerClass)  MUST BE GENERALIZED
            def finishCreate (self):
                
                # g.trace('controlX_handlerClass')
            
                c = self.c ; keyHandler = self.keyHandler
            
                self.abbreviationDispatch = {
                    'a':    lambda event: keyHandler.abbreviationDispatch(event,1),
                    'a i':  lambda event: keyHandler.abbreviationDispatch(event,2),
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
                    'u':            lambda event: keyHandler.doUndo(event,2),
                    'equal':        c.editCommands.lineNumber,
                    'h':            c.editCommands.selectAll,
                    'f':            c.editCommands.setFillColumn,
                    'b':            lambda event, which = 'switch-to-buffer': keyHandler.setInBufferMode(event,which),
                    'k':            lambda event, which = 'kill-buffer': emakeyHandlers.setInBufferMode(event,which),
                }
            #@nonl
            #@-node:ekr.20050920085536.52:finishCreate (controlX_handlerClass)  MUST BE GENERALIZED
            #@+node:ekr.20050920085536.53:get/set
            def get (self,ignorePrompt=False):
                
                return self.keyHandler.miniBufferHandler.get(ignorePrompt)
                
            def set (self,s,protect=False):
            
                return self.keyHandler.miniBufferHandler.set(s,protect)
            #@nonl
            #@-node:ekr.20050920085536.53:get/set
            #@+node:ekr.20050920085536.54:processKey (controlX_handlerClass) MUST BE GENERALIZED
            def processKey (self,event):
            
                b = self ; c = self.c ; previous = self.previous
                
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
                    return self.processRectangle(event)
            
                if (
                    c.rect_commands.has_key(event.keysym) and
                    c.rectangleCommands.rectanglemode == 1
                ):
                    return self.processRectangle(event)
            
                if self.register_commands.has_key(c.registerCommands.registermode):
                    self.register_commands [c.registerCommands.registermode] (event)
                    return 'break'
            
                func = self.variety_commands.get(event.keysym)
                if func:
                    b.keyHandler.stopControlX(event)
                    return func(event)
            
                if event.keysym in ('a','i','e'):
                    if self.processAbbreviation(event): return 'break'
            
                if event.keysym == 'g':
                    l = b.get()
                    if self.abbreviationDispatch.has_key(l):
                        b.keyHandler.stopControlX(event)
                        return self.abbreviationDispatch [l](event)
            
                if event.keysym == 'e':
                    b.keyHandler.stopControlX(event)
                    return c.macroCommands.executeLastMacro(event)
            
                if event.keysym == 'x' and previous [1] not in ('Control_L','Control_R'):
                    event.keysym = 's'
                    b.keyHandler.setNextRegister(event)
                    return 'break'
            
                if event.keysym == 'Escape':
                    if len(previous) > 1:
                        if previous [1] == 'Escape':
                            return b.keyHandler.repeatComplexCommand(event)
            #@nonl
            #@-node:ekr.20050920085536.54:processKey (controlX_handlerClass) MUST BE GENERALIZED
            #@+node:ekr.20050920085536.55:processRectangle
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
                
                func = self.rect_commands.get(event.keysym)
                func(event)
                return 'break'
            #@-node:ekr.20050920085536.55:processRectangle
            #@+node:ekr.20050920085536.56:processAbbreviation MUST BE GENERALIZED
            def processAbbreviation (self,event):
                
                b = self ; char = event.char
            
                if b.get() != 'a' and event.keysym == 'a':
                    b.set('a')
                    return 'break'
            
                elif b.get() == 'a':
                    if char == 'i':
                        b.set('a i')
                    elif char == 'e':
                        b.stopControlX(event)
                        event.char = ''
                        self.keyHandler.expandAbbrev(event)
                    return 'break'
            #@nonl
            #@-node:ekr.20050920085536.56:processAbbreviation MUST BE GENERALIZED
            #@-others
        #@nonl
        #@-node:ekr.20050920085536.49: class controlX_handlerClass MUST BE GENERALIZED
        #@+node:ekr.20050920085536.18: class keyStrokeManagerClass
        class keyStrokeManagerClass:
        
            #@    @+others
            #@+node:ekr.20050920085536.19:__init__
            def __init__ (self,keyHandler):
                
                self.c = keyHandler.c
                self.keyHandler = keyHandler
            
                self.keystrokes = {} # Defined later by finishCreate.
            #@nonl
            #@-node:ekr.20050920085536.19:__init__
            #@+node:ekr.20050920085536.20:__call__ (keyStrokeManagerClass)
            def __call__ (self,event,stroke):
            
                numberOfArgs, func = self.keystrokes [stroke]
            
                if numberOfArgs == 1:
                    return func(event)
                else:
                    return func(event,stroke)
            #@nonl
            #@-node:ekr.20050920085536.20:__call__ (keyStrokeManagerClass)
            #@+node:ekr.20050920085536.21:finishCreate (keyStrokeManagerClass) MUST BE GENERALIZED
            def finishCreate (self):
                
                # g.trace('keyStrokeManagerClass')
                
                c = self.c
                
                self.keystrokes = {
                    '<Control-s>':      ( 2, c.searchCommands.startIncremental ),
                    '<Control-r>':      ( 2, c.searchCommands.startIncremental ),
                    '<Alt-g>':          ( 1, c.editCommands.startGoto ),
                    '<Alt-z>':          ( 1, c.editCommands.startZap ),
                    '<Alt-percent>':    ( 1, c.queryReplaceCommands.masterQR ),
                    '<Control-Alt-w>':  ( 1, lambda event: 'break' ),
                }
            #@nonl
            #@-node:ekr.20050920085536.21:finishCreate (keyStrokeManagerClass) MUST BE GENERALIZED
            #@+node:ekr.20050920085536.22:hasKeyStroke
            def hasKeyStroke (self,stroke):
            
                return self.keystrokes.has_key(stroke)
            #@nonl
            #@-node:ekr.20050920085536.22:hasKeyStroke
            #@-others
        #@nonl
        #@-node:ekr.20050920085536.18: class keyStrokeManagerClass
        #@+node:ekr.20050920085536.23: class stateManagerClass
        class stateManagerClass:
            
            '''This class manages the state that the Emacs instance has entered and
               routes key events to the right method, dependent upon the state in the stateManagerClass'''
               
            #@    @+others
            #@+node:ekr.20050920085536.24:__init__
            def __init__ (self,keyHandler):
            
                self.c = keyHandler.c
                self.keyHandler = keyHandler
            
                self.state = None
                self.states = {}
            #@nonl
            #@-node:ekr.20050920085536.24:__init__
            #@+node:ekr.20050920085536.25:__call__(state manager)
            def __call__ (self,*args):
            
                if self.state:
                    flag, func = self.stateCommands [self.state]
            
                    if flag == 1:
                        return func(args[0])
                    else:
                        return func(*args)
            #@nonl
            #@-node:ekr.20050920085536.25:__call__(state manager)
            #@+node:ekr.20050920085536.26:finishCreate (stateManagerClass) MUST BE GENERALIZED
            def finishCreate (self):
            
                c = self.c ; keyHandler = self.keyHandler ; b = keyHandler.miniBufferHandler
            
                # EKR: used only below.
                def eA (event):
                    if keyHandler.expandAbbrev(event):
                        return 'break'
            
                self.stateCommands = { 
                    # 1 == one parameter, 2 == all
                    
                    # Utility states...
                    'getArg':    (2,keyHandler.miniBufferHandler.getArg),
                    
                    # Command states...
                    'uC':               (2,b.universalDispatch),
                    'controlx':         (2,b.doControlX),
                    'isearch':          (2,c.searchCommands.iSearch),
                    'goto':             (1,c.editCommands.Goto),
                    'zap':              (1,c.editCommands.zapTo),
                    'howM':             (1,c.editCommands.howMany),
                    'abbrevMode':       (1,c.abbrevCommands.abbrevCommand1),
                    'altx':             (1,b.doAlt_X),
                    'qlisten':          (1,c.queryReplaceCommands.masterQR),
                    'rString':          (1,c.editCommands.replaceString),
                    'negativeArg':      (2,b.negativeArgument),
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
                    'last-altx':        (1,b.executeLastAltX),
                    'escape':           (1,c.editCommands.watchEscape),
                    'subprocess':       (1,c.controlCommands.subprocesser),
                }
            #@nonl
            #@-node:ekr.20050920085536.26:finishCreate (stateManagerClass) MUST BE GENERALIZED
            #@+node:ekr.20050920085536.27:setState
            def setState (self,state,value):
            
                self.state = state
                self.states [state] = value
            #@nonl
            #@-node:ekr.20050920085536.27:setState
            #@+node:ekr.20050920085536.28:getState
            def getState (self,state):
            
                return self.states.get(state,False)
            #@nonl
            #@-node:ekr.20050920085536.28:getState
            #@+node:ekr.20050920085536.29:hasState
            def hasState (self):
            
                if self.state:
                    return self.states [self.state]
            #@nonl
            #@-node:ekr.20050920085536.29:hasState
            #@+node:ekr.20050920085536.30:whichState
            def whichState (self):
            
                return self.state
            #@nonl
            #@-node:ekr.20050920085536.30:whichState
            #@+node:ekr.20050920085536.31:clear
            def clear (self):
            
                self.state = None
            
                for z in self.states.keys():
                    self.states [z] = 0 # More useful than False.
            #@nonl
            #@-node:ekr.20050920085536.31:clear
            #@-others
        #@nonl
        #@-node:ekr.20050920085536.23: class stateManagerClass
        #@+node:ekr.20050920085536.32: Entry points
        # These are user commands accessible via alt-x.
        
        def digitArgument (self,event):
            return self.universalDispatch(event,'')
        
        def universalArgument (self,event):
            return self.universalDispatch(event,'')
        #@nonl
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
        
            self.widget.configure(background='lightgrey')
        #@nonl
        #@-node:ekr.20050920085536.35:setLabelGrey
        #@+node:ekr.20050920085536.36:setLabelBlue
        def setLabelBlue (self):
        
            self.widget.configure(background='lightblue')
        #@nonl
        #@-node:ekr.20050920085536.36:setLabelBlue
        #@+node:ekr.20050920085536.37:reset
        def reset (self):
            
            b = self
        
            b.set('')
            b.setLabelGrey()
            b.altX_prefix = ''
        #@nonl
        #@-node:ekr.20050920085536.37:reset
        #@+node:ekr.20050920085536.38:update
        def update (self,event):
        
            '''
            Alters the StringVar svar to represent the change in the event.
            This has the effect of changing the miniBuffer contents.
        
            It mimics what would happen with the keyboard and a Text editor
            instead of plain accumalation.'''
            
            b = self ; s = b.get() ; ch = event.char
        
            if ch == '\b': # Handle backspace.
                # Don't backspace over the prompt.
                if len(s) <= b.altX_prefix:
                    return 
                elif len(s) == 1: s = ''
                else: s = s [0:-1]
            else:
                # Add the character.
                s = s + ch
        
            b.set(s)
        #@nonl
        #@-node:ekr.20050920085536.38:update
        #@+node:ekr.20050920085536.39:get & set
        def get (self,ignorePrompt=False):
        
            s = self.svar.get()
            # g.trace(s)
            if ignorePrompt:
                return s[len(self.altX_prefix):]
            else:
                return s
        
        def set (self,s,protect=False):
            
            self.svar.set(s)
            if protect:
                # g.trace('protecting',repr(s))
                self.altX_prefix = s
        #@nonl
        #@-node:ekr.20050920085536.39:get & set
        #@-node:ekr.20050920085536.33: Getters & Setters
        #@+node:ekr.20050920085536.40:Alt_X methods (miniBufferHandlerClass)
        #@+node:ekr.20050920085536.41:alt_X
        def alt_X (self,event=None,which=''):
        
            b = self
        
            b.setState('altx',which or 1) # Must be int, not True.
        
            if which:
                b.set('%s %s' % (which,self.alt_x_prompt),protect=True)
            else:
                b.set('%s' % (self.alt_x_prompt),protect=True)
        
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.41:alt_X
        #@+node:ekr.20050920085536.42:doAlt_X & helpers
        def doAlt_X (self,event):
        
            '''This method executes the correct Alt-X command'''
            
            b = self ; c = self.c ; keysym = event.keysym
            # g.trace(keysym)
        
            if keysym == 'Return':
                #@        << dispatch the function >>
                #@+node:ekr.20050920085536.45:<< dispatch the function >>
                s = b.get()
                b.altX_tabList = []
                s = s[len(b.altX_prefix):].strip()
                func = c.commandsDict.get(s)
                if func:
                    if s != 'repeat-complex-command': b.altX_history.insert(0,s)
                    aX = b.getState('altx')
                    if (type(aX) == type(1) or aX.isdigit()) and s in b.x_hasNumeric:
                        func(event,aX)
                    else:
                        func(event)
                else:
                    b.keyboardQuit(event)
                    b.set('Command does not exist')
                #@nonl
                #@-node:ekr.20050920085536.45:<< dispatch the function >>
                #@nl
            elif keysym == 'Tab':
                #@        << handle tab completion >>
                #@+node:ekr.20050920085536.44:<< handle tab completion >>
                s = b.get().strip()
                
                if b.altX_tabList and s.startswith(b.altX_tabListPrefix):
                    b.altX_tabListIndex +=1
                    if b.altX_tabListIndex >= len(b.altX_tabList):
                        b.altX_tabListIndex = 0
                    b.set(b.alt_x_prompt + b.altX_tabList [b.altX_tabListIndex])
                else:
                    s = b.get() # Always includes prefix, so command is well defined.
                    b.altX_tabListPrefix = s
                    command = s [len(b.alt_x_prompt):]
                    b.altX_tabList,common_prefix = b._findMatch(command)
                    b.altX_tabListIndex = 0
                    if b.altX_tabList:
                        if len(b.altX_tabList) > 1 and (
                            len(common_prefix) > (len(b.altX_tabListPrefix) - len(b.alt_x_prompt))
                        ):
                            b.set(b.alt_x_prompt + common_prefix)
                            b.altX_tabListPrefix = b.alt_x_prompt + common_prefix
                        else:
                            # No common prefix, so show the first item.
                            b.set(b.alt_x_prompt + b.altX_tabList [0])
                    else:
                        b.set(b.alt_x_prompt,protect=True)
                #@nonl
                #@-node:ekr.20050920085536.44:<< handle tab completion >>
                #@nl
            elif keysym == 'BackSpace':
                #@        << handle BackSpace >>
                #@+node:ekr.20050920085536.46:<< handle BackSpace >>
                # Cut back to previous prefix and update prefix 
                
                s = b.altX_tabListPrefix
                
                if len(s) > len(b.altX_prefix):
                    b.altX_tabListPrefix = s[:-1]
                    b.set(b.altX_tabListPrefix,protect=False)
                else:
                    b.altX_tabListPrefix = s
                    b.set(b.altX_tabListPrefix,protect=True)
                    
                g.trace('BackSpace: new altX_tabListPrefix',b.altX_tabListPrefix)
                
                ### b.startIteration()
                
                b.altX_tabList = []
                #@nonl
                #@-node:ekr.20050920085536.46:<< handle BackSpace >>
                #@nl
            else:
                # Clear the list, any other character besides tab indicates that a new prefix is in effect.
                b.altX_tabList = []
                b.update(event)
                b.altX_tabListPrefix = b.get()
                # g.trace('new prefix',b.altX_tabListPrefix)
        
            return 'break'
        #@nonl
        #@+node:ekr.20050920085536.43:_findMatch
        def _findMatch (self,s,fdict=None):
            
            '''This method returns a sorted list of matches.'''
        
            c = self.c
        
            if not fdict:
                fdict = c.commandsDict
        
            common_prefix = ''
        
            if s:
                pmatches = [a for a in fdict if a.startswith(s)]
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
            else:
                pmatches = []
        
            pmatches.sort()
        
            # g.trace(repr(s),len(pmatches))
            return pmatches,common_prefix
        #@nonl
        #@-node:ekr.20050920085536.43:_findMatch
        #@-node:ekr.20050920085536.42:doAlt_X & helpers
        #@+node:ekr.20050920085536.47:executeLastAltX
        def executeLastAltX (self,event):
            
            b = self ; c = self.c
        
            if event.keysym == 'Return' and b.altX_history:
                last = self.altX_history [0]
                c.commandsDict [last](event)
                return 'break'
            else:
                return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050920085536.47:executeLastAltX
        #@+node:ekr.20050920085536.48:repeatComplexCommand
        def repeatComplexCommand (self,event):
        
            b = self
        
            b.keyboardQuit(event)
        
            if self.altX_history:
                self.setLabelBlue()
                b.set("Redo: %s" % b.altX_history[0])
                b.setState('last-altx',True)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.48:repeatComplexCommand
        #@-node:ekr.20050920085536.40:Alt_X methods (miniBufferHandlerClass)
        #@+node:ekr.20050920085536.57:ControlX methods
        #@+node:ekr.20050920085536.58:startControlX
        def startControlX (self,event):
        
            '''This method starts the Control-X command sequence.'''
            
            b = self
        
            b.setState('controlx',True)
            b.set('Control - X')
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.58:startControlX
        #@+node:ekr.20050920085536.59:stopControlX
        def stopControlX (self,event): # event IS used.
        
            '''This method clears the state of the Emacs instance'''
            
            b = self ; c = self.c ; widget = event.widget
        
            # This will all be migrated to keyboardQuit eventually.
            if c.controlCommands.shuttingdown:
                return
        
            c.rectangleCommands.sRect = False
            c.registerCommands.rectanglemode = 0
            
            b.stateManager.clear()
            widget.tag_delete('color')
            widget.tag_delete('color1')
        
            if c.registerCommands.registermode:
                c.registerCommands.deactivateRegister(event)
        
            self.bufferMode = None ### Correct???
            b.reset()
            widget.update_idletasks()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.59:stopControlX
        #@+node:ekr.20050920085536.60:doControlX
        def doControlX (self,event,stroke,previous=[]):
        
            return self.cxHandler(event,stroke)
        #@nonl
        #@-node:ekr.20050920085536.60:doControlX
        #@-node:ekr.20050920085536.57:ControlX methods
        #@+node:ekr.20050920085536.61:extendAltX
        def extendAltX (self,name,function):
        
            '''A simple method that extends the functions Alt-X offers.'''
        
            # Important: f need not be a method of the emacs class.
            
            b = self ; c = self.c
        
            def f (event,aX=None,self=self,command=function):
                # g.trace(event,self,command)
                command()
                b.keyboardQuit(event)
        
            c.commandsDict [name] = f
        #@nonl
        #@-node:ekr.20050920085536.61:extendAltX
        #@+node:ekr.20050920085536.62:getArg
        def getArg (self,event,returnStateKind=None,returnState=None):
            
            '''Accumulate an argument until the user hits return (or control-g).
            Enter the 'return' state when done.'''
            
            b = self ; stateKind = 'getArg'
            state = b.getState(stateKind)
            if not state:
                b.altX_prefix = len(b.get()) ; b.arg = ''
                b.afterGetArgState = (returnStateKind,returnState)
                b.setState(stateKind,1)
            elif event.keysym == 'Return':
                # Compute the actual arg.
                s = b.get() ; b.arg = s[len(b.altX_prefix):]
                # Immediately enter the caller's requested state.
                b.stateManager.clear()
                stateKind,state = self.afterGetArgState
                b.setState(stateKind,state)
                b.stateManager(event,None) # Invoke the stateManager __call__ method.
            else:
                b.update(event)
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.62:getArg
        #@+node:ekr.20050920085536.63:keyboardQuit
        def keyboardQuit (self,event):  # The event arg IS used.
        
            '''This method cleans the Emacs instance of state and ceases current operations.'''
        
            return self.stopControlX(event) # This method will eventually contain the stopControlX code.
        #@nonl
        #@-node:ekr.20050920085536.63:keyboardQuit
        #@+node:ekr.20050920085536.64:manufactureKeyPress
        def manufactureKeyPress (self,event,which): # event **is** used.
        
            tbuffer = event.widget
            tbuffer.event_generate('<Key>',keysym=which)
            tbuffer.update_idletasks()
            
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.64:manufactureKeyPress
        #@+node:ekr.20050920085536.65:masterCommand (miniBufferHandlerClass)
        def masterCommand (self,event,method,stroke,general):
            
            '''This is the central routing method of the Emacs class.
            All commands and keystrokes pass through here.'''
            
            # Note: the _L symbols represent *either* special key.
            b = self ; c = self.c
            special = event.keysym in ('Control_L','Alt_L','Shift_L')
        
            inserted = not special or (
                not general and (len(self.keysymhistory) == 0 or self.keysymhistory [0] != event.keysym))
        
            if inserted:
                g.trace(general,event.keysym)
                #@        << add character to history >>
                #@+node:ekr.20050920085536.67:<< add character to history >>
                # Don't add multiple special characters to history.
                
                self.keysymhistory.insert(0,event.keysym)
                
                if len(event.char) > 0:
                    if len(keyHandlerClass.lossage) > 99:
                        keyHandlerClass.lossage.pop()
                    keyHandlerClass.lossage.insert(0,event.char)
                
                if 0: # traces
                    g.trace(event.keysym,stroke)
                    g.trace(self.keysymhistory)
                    g.trace(keyHandlerClass.lossage)
                #@nonl
                #@-node:ekr.20050920085536.67:<< add character to history >>
                #@nl
        
            if c.macroCommands.macroing:
                #@        << handle macro >>
                #@+node:ekr.20050920085536.66:<< handle macro >>
                if c.macroCommands.macroing == 2 and stroke != '<Control-x>':
                    return self.nameLastMacro(event)
                    
                elif c.macroCommands.macroing == 3 and stroke != '<Control-x>':
                    return self.getMacroName(event)
                    
                else:
                   self.recordKBDMacro(event,stroke)
                #@nonl
                #@-node:ekr.20050920085536.66:<< handle macro >>
                #@nl
        
            if stroke == '<Control-g>':
                b.previousStroke = stroke
                return b.keyboardQuit(event)
        
            # Important: This effectively over-rides the handling of most keystrokes with a state.
            if b.stateManager.hasState():
                # g.trace('hasState')
                b.previousStroke = stroke
                return b.stateManager(event,stroke) # Invoke the __call__ method.
        
            if b.kstrokeManager.hasKeyStroke(stroke):
                g.trace('hasKeyStroke')
                b.previousStroke = stroke
                return b.kstrokeManager(event,stroke) # Invoke the __call__ method.
        
            if b.keyHandler.regXRpl: # EKR: a generator.
                try:
                    b.keyHandler.regXKey = event.keysym
                    b.keyHandler.regXRpl.next() # EKR: next() may throw StopIteration.
                finally:
                    return 'break'
        
            if b.keyHandler.abbrevOn:
                if c.abbrevCommands._expandAbbrev(event):
                    return 'break'
        
            if method:
                rt = method(event)
                b.previousStroke = stroke
                return rt
            else:
                # g.trace('default')
                return c.frame.body.onBodyKey(event)
        #@nonl
        #@-node:ekr.20050920085536.65:masterCommand (miniBufferHandlerClass)
        #@+node:ekr.20050920085536.68:negativeArgument
        def negativeArgument (self,event,stroke=None):
        
            b = self
        
            b.set("Negative Argument")
            b.setLabelBlue()
        
            state = b.getState('negativeArg')
            if state == 0:
                b.setState('negativeArg',1)
            else:
                func = b.negArgs.get(stroke)
                if func:
                    func(event,stroke)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.68:negativeArgument
        #@+node:ekr.20050920085536.69:tailEnd methods
        #@+node:ekr.20050920085536.70:_tailEnd
        def _tailEnd (self,tbuffer):
            
            '''This returns the tailEnd function that has been configure for the tbuffer parameter.'''
            
            func = self.tailEnds.get(tbuffer)
            if func:
                return func(tbuffer)
            else:
                return 'break'
        #@-node:ekr.20050920085536.70:_tailEnd
        #@+node:ekr.20050920085536.71:setTailEnd
        def setTailEnd (self,tbuffer,tailCall):
        
            '''This method sets a ending call that is specific for a particular Text widget.
               Some environments require that specific end calls be made after a keystroke
               or command is executed.'''
        
            self.tailEnds [tbuffer] = tailCall
        #@-node:ekr.20050920085536.71:setTailEnd
        #@-node:ekr.20050920085536.69:tailEnd methods
        #@+node:ekr.20050920085536.72:universal dispatch methods
        #@+others
        #@+node:ekr.20050920085536.73:universalDispatch
        def universalDispatch (self,event,stroke):
        
            b = self
            
            state = b.getState('uC')
            if state == 0:
                b.setState('uC',1)
                b.set('')
                b.setLabelBlue()
            elif state == 1:
                b.universalCommand1(event,stroke)
            elif state == 2:
                b.universalCommand3(event,stroke)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.73:universalDispatch
        #@+node:ekr.20050920085536.74:universalCommand1
        def universalCommand1 (self,event,stroke):
            
            b = self
        
            if event.char not in b.uCstring:
                return b.universalCommand2(event,stroke)
         
            b.update(event)
        
            if event.char != '\b':
                b.set('%s ' % b.get())
        #@nonl
        #@-node:ekr.20050920085536.74:universalCommand1
        #@+node:ekr.20050920085536.75:universalCommand2
        def universalCommand2 (self,event,stroke):
            
            b = self ; tbuffer = event.widget # event IS used.
            txt = b.get()
            b.keyboardQuit(event)
            txt = txt.replace(' ','')
            b.reset()
            if not txt.isdigit():
                # This takes us to macro state.
                # For example Control-u Control-x ( will execute the last macro and begin editing of it.
                if stroke == '<Control-x>':
                    b.setState('uC',2)
                    return b.universalCommand3(event,stroke)
                return b._tailEnd(event.widget)
            if b.uCdict.has_key(stroke): # This executes the keystroke 'n' number of times.
                b.uCdict [stroke](event,txt)
            else:
                i = int(txt)
                stroke = stroke.lstrip('<').rstrip('>')
                if b.cbDict.has_key(stroke):
                    for z in xrange(i):
                        method = self.cbDict [stroke]
                        ev = Tk.Event()
                        ev.widget = event.widget
                        ev.keysym = event.keysym
                        ev.keycode = event.keycode
                        ev.char = event.char
                        b.masterCommand(ev,method,'<%s>' % stroke)
                else:
                    for z in xrange(i):
                        tbuffer.event_generate('<Key>',keycode=event.keycode,keysym=event.keysym)
                        b._tailEnd(tbuffer)
        #@-node:ekr.20050920085536.75:universalCommand2
        #@+node:ekr.20050920085536.76:universalCommand3
        def universalCommand3 (self,event,stroke):
            
            b = self
            b.set('Control-u %s' % stroke.lstrip('<').rstrip('>'))
            b.setLabelBlue()
        
            if event.keysym == 'parenleft':
                b.keyboardQuit(event)
                c.macroCommands.startKBDMacro(event)
                c.macroCommands.executeLastMacro(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050920085536.76:universalCommand3
        #@+node:ekr.20050920085536.77:numberCommand
        def numberCommand (self,event,stroke,number): # event IS used.
        
            self.universalDispatch(event,stroke)
            event.widget.event_generate('<Key>',keysym=number)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050920085536.77:numberCommand
        #@-others
        #@nonl
        #@-node:ekr.20050920085536.72:universal dispatch methods
        #@-others
    #@nonl
    #@-node:ekr.20050920085536.7:class miniBufferHandlerClass
    #@-others
#@nonl
#@-node:ekr.20050920085536:class keyHandler (replaces Emacs class)
#@-others
#@nonl
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
