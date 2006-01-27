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

Tk = g.importExtension('Tkinter',pluginName=None,verbose=False)

import string
#@nonl
#@-node:ekr.20050920094258:<< imports >>
#@nl
#@<< about key dicts >>
#@+node:ekr.20051010062551.1:<< about key dicts >>
#@@nocolor
#@+at
# 
# ivars:
# 
# c.commandsDict:
#     keys are emacs command names, values are functions f.
# 
# k.inverseCommandsDict:
#     keys are f.__name__, values are emacs command names.
# 
# k.bindingsDict:
#     keys are shortcuts, values are *lists* of 
# g.bunch(func,name,warningGiven)
# 
# g.app.keysym_numberDict:
#     Keys are keysym_num's.  Values are strokes.
# 
# g.app.keysym_numberInverseDict
#     Keys are strokes, values are keysym_num's.
# 
# not an ivar (computed by computeInverseBindingDict):
# 
# inverseBindingDict
#     keys are emacs command names, values are *lists* of shortcuts.
#@-at
#@nonl
#@-node:ekr.20051010062551.1:<< about key dicts >>
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
    #@+node:ekr.20050920085536.1: Birth (keyHandler)
    #@+node:ekr.20050920085536.2: ctor (keyHandler)
    def __init__ (self,c,useGlobalKillbuffer=False,useGlobalRegisters=False):
        
        '''Create a key handler for c.
        c.frame.miniBufferWidget is a Tk.Label.
        
        useGlobalRegisters and useGlobalKillbuffer indicate whether to use
        global (class vars) or per-instance (ivars) for kill buffers and registers.'''
        
        self.c = c
        self.widget = c.frame.miniBufferWidget
        self.useTextWidget = c.useTextMinibuffer
            # A Tk Label or Text widget.
            # Exists even if c.showMinibuffer is False.
        self.useGlobalKillbuffer = useGlobalKillbuffer
        self.useGlobalRegisters = useGlobalRegisters
    
        # Generalize...
        self.x_hasNumeric = ['sort-lines','sort-fields']
    
        self.altX_prompt = 'full-command: '
        #@    << define Tk ivars >>
        #@+node:ekr.20051006092617:<< define Tk ivars >>
        if self.useTextWidget:
            self.svar = None
        else:
            if self.widget:
                self.svar = Tk.StringVar()
                self.widget.configure(textvariable=self.svar)
                
            else:
                self.svar = None
        #@nonl
        #@-node:ekr.20051006092617:<< define Tk ivars >>
        #@nl
        #@    << define externally visible ivars >>
        #@+node:ekr.20051006092617.1:<< define externally visible ivars >>
        self.abbrevOn = False # True: abbreviations are on.
        self.arg = '' # The value returned by k.getArg.
        self.commandName = None # The name of the command being executed.
        self.funcReturn = None # For k.simulateCommand
        self.inputModeBindings = {}
        self.inputModeName = '' # The name of the input mode, or None.
        self.inverseCommandsDict = {}
            # Completed in k.finishCreate, but leoCommands.getPublicCommands adds entries first.
        self.keysym_numberDict = {}
            # Keys are keysym_num's.  Values are strokes.
        self.keysym_numberInverseDict = {}
            # Keys are strokes, values are keysym_num's.
        ### self.leoCallbackDict = {}
            # Completed in leoCommands.getPublicCommands.
            # Keys are *raw* functions wrapped by the leoCallback, values are emacs command names.
        self.negativeArg = False
        self.regx = g.bunch(iter=None,key=None)
        self.repeatCount = None
        self.state = g.bunch(kind=None,n=None,handler=None)
        self.setDefaultUnboundKeyAction()
        #@nonl
        #@-node:ekr.20051006092617.1:<< define externally visible ivars >>
        #@nl
        #@    << define internal ivars >>
        #@+node:ekr.20050923213858:<< define internal ivars >>
        self.abbreviationsDict = {} # Abbreviations created by @alias nodes.
        
        # Previously defined bindings.
        self.bindingsDict = {}
            # Keys are Tk key names, values are lists of g.bunch(pane,func,commandName)
        # Previously defined binding tags.
        self.bindtagsDict = {}
            # Keys are strings (the tag), values are 'True'
        
        # Special bindings for k.fullCommand.
        self.mb_copyKey = None
        self.mb_pasteKey = None
        self.mb_cutKey = None
        
        self.abortAllModesKey = None
        self.fullCommandKey = None
        self.universalArgKey = None
        
        # Keepting track of the characters in the mini-buffer.
        self.arg_completion = True
        self.mb_history = []
        self.mb_prefix = ''
        self.mb_tabListPrefix = ''
        self.mb_tabList = []
        self.mb_tabListIndex = -1
        self.mb_prompt = ''
        
        self.func = None
        self.keysymHistory = []
        self.previous = []
        self.stroke = None
        
        # For getArg...
        self.afterGetArgState = None
        self.argTabList = []
        
        # For onIdleTime
        self.idleCount = 0
        
        # For modes
        self.modeBunch = None
        #@nonl
        #@-node:ekr.20050923213858:<< define internal ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20050920085536.2: ctor (keyHandler)
    #@+node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    def finishCreate (self):
        
        '''Complete the construction of the keyHandler class.
        c.commandsDict has been created when this is called.'''
        
        k = self ; c = k.c
       
        k.createInverseCommandsDict()
        
        if not c.miniBufferWidget:
            # Does not exist for leoSettings.leo files.
            return
            
        # g.trace('keyHandler')
    
        # Important: bindings exist even if c.showMiniBuffer is False.
        k.makeAllBindings()
        
        c.frame.log.setTabBindings('Log')
        c.frame.tree.setBindings()
        if 0: # Hurray.  This was a massive kludge.
            g.enableIdleTimeHook(250)
    
        k.setInputState(self.unboundKeyAction)
    #@nonl
    #@+node:ekr.20051008082929:createInverseCommandsDict
    def createInverseCommandsDict (self):
        
        '''Add entries to k.inverseCommandsDict using c.commandDict,
        except when c.commandDict.get(key) refers to the leoCallback function.
        leoCommands.getPublicCommands has already added an entry in this case.
        
        In c.commandsDict        keys are command names, values are funcions f.
        In k.inverseCommandsDict keys are f.__name__, values are emacs-style command names.
        '''
    
        k = self ; c = k.c
    
        for name in c.commandsDict.keys():
            f = c.commandsDict.get(name)
            try:
                # 'leoCallback' callback created by leoCommands.getPublicCommands.
                if f.__name__ == 'leoCallback':
                    g.trace('oops: f.__name__ == leoCallback')
                else:
                    k.inverseCommandsDict [f.__name__] = name
                    # g.trace('%24s = %s' % (f.__name__,name))
                    
            except Exception:
                g.es_exception()
                g.trace(repr(name),repr(f),g.callers())
                
    #@nonl
    #@-node:ekr.20051008082929:createInverseCommandsDict
    #@-node:ekr.20050920094633:finishCreate (keyHandler) & helpers
    #@+node:ekr.20060115195302:setDefaultUnboundKeyAction
    def setDefaultUnboundKeyAction (self):
        
        k = self ; c = k.c
    
        defaultAction = c.config.getString('top_level_unbound_key_action') or 'insert'
        defaultAction.lower()
        if defaultAction in ('ignore','insert','overwrite'):
            self.unboundKeyAction = defaultAction
        else:
            g.trace('ignoring top_level_unbound_key_action setting: %s' % defaultAction)
            self.unboundKeyAction = 'insert'
            
        k.setInputState(self.unboundKeyAction)
    #@nonl
    #@-node:ekr.20060115195302:setDefaultUnboundKeyAction
    #@-node:ekr.20050920085536.1: Birth (keyHandler)
    #@+node:ekr.20051006125633:Binding (keyHandler)
    #@+node:ekr.20050920085536.16:bindKey
    def bindKey (self,pane,shortcut,callback,commandName):
    
        '''Bind the indicated shortcut (a Tk keystroke) to the callback.
        callback calls commandName (for error messages).'''
        
        k = self ; c = k.c
    
        # g.trace(pane,shortcut,commandName)
    
        if not shortcut:
            # g.trace('No shortcut for %s' % commandName)
            return
        bunchList = k.bindingsDict.get(shortcut,[])
        k.computeKeysym_numDicts(shortcut)
        #@    << give warning and return if there is a serious redefinition >>
        #@+node:ekr.20060114115648:<< give warning and return if there is a serious redefinition >>
        for bunch in bunchList:
            if ( bunch and
                # (not bunch.pane.endswith('-mode') and not pane.endswith('-mode')) and
                (bunch.pane == pane or pane == 'all' or bunch.pane == 'all') and
                commandName != bunch.commandName
            ):
                # shortcut, junk = c.frame.menu.canonicalizeShortcut(shortcut)
                g.es_print('Ignoring redefinition of %s from %s to %s in %s' % (
                    k.prettyPrintKey(shortcut),
                    bunch.commandName,commandName,pane),
                    color='blue')
                return
        #@nonl
        #@-node:ekr.20060114115648:<< give warning and return if there is a serious redefinition >>
        #@nl
        #@    << trace bindings if enabled in leoSettings.leo >>
        #@+node:ekr.20060114110141:<< trace bindings if enabled in leoSettings.leo >>
        if c.config.getBool('trace_bindings'):
            theFilter = c.config.getString('trace_bindings_filter') or ''
            # g.trace(repr(theFilter))
            if not theFilter or shortcut.find(theFilter) != -1:
                pane_filter = c.config.getString('trace_bindings_pane_filter')
                if not pane_filter or pane_filter.lower() == pane:
                    g.trace(pane,k.prettyPrintKey(shortcut),commandName)
        #@nonl
        #@-node:ekr.20060114110141:<< trace bindings if enabled in leoSettings.leo >>
        #@nl
        try:
            k.bindKeyHelper(pane,shortcut,callback,commandName)
            bunchList.append(
                g.bunch(pane=pane,func=callback,commandName=commandName))
            shortcut = '<%s>' % shortcut.lstrip('<').rstrip('>')
            k.bindingsDict [shortcut] = bunchList
            return True
    
        except Exception: # Could be a user error.
            if not g.app.menuWarningsGiven:
                g.es_print('Exception binding %s to %s' % (shortcut,commandName))
                g.es_exception()
                g.app.menuWarningsGiven = True
    
            return False
    #@nonl
    #@+node:ekr.20051022094136:bindKeyHelper
    def bindKeyHelper(self,pane,shortcut,callback,commandName):
    
        k = self ; c = k.c
        
        body = c.frame.body.bodyCtrl
        log  = c.frame.log.logCtrl
        menu = c.frame.menu
        minibuffer = c.miniBufferWidget
        tree = c.frame.tree.canvas
        
        d = {
            'all':  [body,log,tree], # Probably not wise: menu
            'body': [body],
            'log':  [log],
            'menu': [menu],         # Not used, and probably dubious.
            'mini': [minibuffer],   # Needed so ctrl-g will work in the minibuffer!
            'text': [body,log],
            'tree': [tree],
        }
        
        # if pane: g.trace('%4s %20s %s' % (pane, shortcut,commandName))
        
        widgets = d.get((pane or '').lower(),[])
        
        # Binding to 'menu' causes problems with multiple pastes in the Find Tab.
        # There should only be one binding for the minibuffer: the <Key>+ binding.
        if shortcut == '<Key>':
            # Important.  We must make this binding if the minibuffer can ever get focus.
            if self.useTextWidget:
                widgets.append(minibuffer)
            for w in widgets:
                w.bind(shortcut,callback,'+')
        else:
            # Put *everything* in a bindtag set specific to this commander.
            if 0: # Support plain-key bindings.
                tag = k.plainKeyTag()
                body.bind_class(tag,shortcut,callback)
            
            # Put everything *except* plain keys in a normal binding.
            if not k.isPlainKey(shortcut):
                for w in widgets:
                    w.bind(shortcut,callback)
                # Get rid of the default binding in the menu. (E.g., Alt-f)
                menu.bind(shortcut,lambda e: 'break')
    #@nonl
    #@-node:ekr.20051022094136:bindKeyHelper
    #@+node:ekr.20060120082630:plainKeyTag
    def plainKeyTag (self):
        
        return '%s-%s' % ('plain-key',self.c.fileName())
    #@nonl
    #@-node:ekr.20060120082630:plainKeyTag
    #@-node:ekr.20050920085536.16:bindKey
    #@+node:ekr.20051008135051.1:bindOpenWith
    def bindOpenWith (self,shortcut,name,data):
        
        '''Make a binding for the Open With command.'''
        
        k = self ; c = k.c
        
        # The first parameter must be event, and it must default to None.
        def openWithCallback(event=None,self=self,data=data):
            __pychecker__ = '--no-argsused' # event must be present.
            return self.c.openWith(data=data)
        
        if c.simple_bindings:
            return k.bindKey('all',shortcut,openWithCallback,'open-with')
        else:
        
            bind_shortcut, menu_shortcut = c.frame.menu.canonicalizeShortcut(shortcut)
        
            def keyCallback (event,func=openWithCallback,stroke=bind_shortcut):
                return k.masterCommand(event,func,stroke)
                    
            return k.bindKey('all',bind_shortcut,keyCallback,'open-with')
    #@nonl
    #@-node:ekr.20051008135051.1:bindOpenWith
    #@+node:ekr.20051006125633.1:bindShortcut
    def bindShortcut (self,pane,shortcut,command,commandName):
        
        '''Bind one shortcut from a menu table.'''
        
        k = self ; shortcut = str(shortcut)
        
        # if k.isPlainKey(shortcut):
            # g.trace('Ignoring plain key binding of %s to %s' % (shortcut,commandName))
            # return
    
        if command.__name__ == 'leoCallback':
            
            g.trace('oops: should not happen: leoCallback used')
            # Get the function wrapped by *this* leoCallback function.
            func = k.leoCallbackDict.get(command)
            commandName = k.inverseCommandsDict.get(func.__name__)
            
            # No need for a second layer of callback.
            def keyCallback1 (event,k=k,func=command,stroke=shortcut):
                return k.masterCommand(event,func,stroke)
                
            keyCallback = keyCallback1
        else:
            
            # g.trace(commandName,shortcut,g.callers())
    
            def menuFuncCallback (event,command=command,commandName=commandName):
                return command(event)
    
            def keyCallback2 (event,k=k,func=menuFuncCallback,stroke=shortcut):
                return k.masterCommand(event,func,stroke,commandName=commandName)
                
            keyCallback = keyCallback2
            
        return k.bindKey(pane,shortcut,keyCallback,commandName)
    #@nonl
    #@-node:ekr.20051006125633.1:bindShortcut
    #@+node:ekr.20051011103654:checkBindings
    def checkBindings (self):
        
        '''Print warnings if commands do not have any @shortcut entry.
        The entry may be `None`, of course.'''
        
        k = self ; c = k.c
        
        names = c.commandsDict.keys() ; names.sort()
        
        for name in names:
            abbrev = k.abbreviationsDict.get(name)
            key = c.frame.menu.canonicalizeMenuName(abbrev or name)
            key = key.replace('&','')
            if not g.app.config.exists(c,key,'shortcut'):
                if abbrev:
                     g.trace('No shortcut for abbrev %s -> %s = %s' % (
                        name,abbrev,key))
                else:
                    g.trace('No shortcut for %s = %s' % (name,key))
    #@nonl
    #@-node:ekr.20051011103654:checkBindings
    #@+node:ekr.20060119063223.1:computeKeysym_numDicts
    def computeKeysym_numDicts (self,shortcut):
        
        k = self
        
        if shortcut == '<Key>': return
        
        n = k.keysym_numberInverseDict.get(shortcut)
        if n is not None:
            # print 'keysym_num for %s = %d' % (shortcut,n)
            return
            
        def callback (event,shortcut=shortcut):
            n = event.keysym_num
            # Trace causes problems.
            print '%5d = %s' % (n,shortcut)
            k.keysym_numberDict [n] = shortcut
            k.keysym_numberInverseDict [shortcut] = n
            
        if 0:  # This causes all sorts of problems.
            t = Tk.Text(k.c.frame.outerFrame)
            t = k.c.frame.body.bodyCtrl
            t.bind(shortcut,callback)
            t.event_generate(shortcut)
            # t.update()
            # t.unbind(shortcut)
    #@nonl
    #@-node:ekr.20060119063223.1:computeKeysym_numDicts
    #@+node:ekr.20051023182326:k.copyBindingsToWidget & helper
    def copyBindingsToWidget (self,paneOrPanes,w):
        
        '''Copy all bindings for the given panes to widget w.
        
        paneOrPanes may be  pane name (a string) or a list of pane names in priority order.'''
        
        # g.trace(paneOrPanes,g.app.gui.widget_name(w),g.callers())
    
        k = self ; d = k.bindingsDict
        bindings = {}
        keys = d.keys() ; keys.sort()
        if type(paneOrPanes) == type('abc'):
            panes = [paneOrPanes] # list(paneOrPanes) does not work.
        else:
            panes = paneOrPanes
        # g.trace(panes)
    
        for shortcut in keys:
            # Do not copy plain key bindings.
            if not k.isPlainKey(shortcut):
                shortcutsBunchList = []
                for pane in panes:
                    old_panes = bindings.get(shortcut,[])
                    assert(type(old_panes)==type([]))
                    if old_panes and pane in old_panes:
                        # This should have been caught earlier, but another check doesn't hurt.
                        g.trace('*** redefining %s in %s' % (shortcut,pane))
                    else:
                        bunchList = d.get(shortcut,[])
                        for bunch in bunchList:
                            if bunch.pane == pane:
                                shortcutsBunchList.append(bunch)
                                old_panes.append(pane)
                                bindings [shortcut] = old_panes
                # Create bindings for the shortcut in all panes.
                if shortcutsBunchList:
                    self.copyBindingsHelper(shortcutsBunchList,shortcut,w)        
                                    
        # Bind all other keys to k.masterCommand.
        def generalTextKeyCallback (event,k=self):
            k.masterCommand(event,func=None,stroke='<Key>',commandName=None)
    
        w.bind('<Key>',generalTextKeyCallback)
    #@nonl
    #@+node:ekr.20060113062832.1:copyBindingsHelper
    def copyBindingsHelper(self,bunchList,shortcut,w):
    
        k = self ; c = k.c
    
        textBunch = treeBunch = None
        for bunch in bunchList:
            if bunch.pane == 'tree' and treeBunch is None:
                treeBunch = bunch
                k.traceBinding (bunch,shortcut,w)
            elif bunch.pane != 'tree' and textBunch is None:
                textBunch = bunch
                k.traceBinding (bunch,shortcut,w)
            elif c.config.getBool('trace_bindings'):
                g.trace('ignoring %s in %s' % (shortcut,bunch.pane))
                
        if textBunch and treeBunch:
            def textAndTreeKeyCallback(event,c=c,
                textFunc=textBunch.func,treeFunc=treeBunch.func):
                w = c.currentPosition().edit_widget()
                if w and w.cget('state') == 'disabled':
                    treeFunc(event)
                else:
                    textFunc(event)
                return 'break'
    
            w.bind(shortcut,textAndTreeKeyCallback)
            
        elif textBunch or treeBunch:
    
            def textOrTreeKeyCallback(event,func=bunch.func):
                func(event)
                return 'break'
    
            w.bind(shortcut,textOrTreeKeyCallback)
    #@nonl
    #@-node:ekr.20060113062832.1:copyBindingsHelper
    #@-node:ekr.20051023182326:k.copyBindingsToWidget & helper
    #@+node:ekr.20060120071949:isPlainKey
    def isPlainKey (self,shortcut):
        
        '''Return true if the shortcut refers to a plain key.'''
        
        shortcut = shortcut or ''
        shortcut1 = shortcut[:]
    
        shift = 'Shift-'
        shortcut = shortcut or ''
        if shortcut.startswith('<'):   shortcut = shortcut[1:]
        if shortcut.endswith('>'):     shortcut = shortcut[:-1]
        if shortcut.startswith(shift): shortcut = shortcut[len(shift):]
        
        # if len(shortcut) == 1:
            # g.trace(shortcut1)
    
        return len(shortcut) == 1
    #@nonl
    #@-node:ekr.20060120071949:isPlainKey
    #@+node:ekr.20051007080058:makeAllBindings
    def makeAllBindings (self):
        
        k = self ; c = k.c
    
        k.bindingsDict = {}
        k.makeSpecialBindings()
        k.addModeCommands() 
        k.makeBindingsFromCommandsDict()
        if k.useTextWidget:
            k.copyBindingsToWidget(['text','mini','all'],c.miniBufferWidget)
        k.checkBindings()
        
        if 0:
            # Print the keysym_num dicts.
            d = k.keysym_numberInverseDict
            keys = d.keys() ; keys.sort()
            for key in key():
                n = d.get(key)
                # print 'keysym_num for %s = %d' % (key,n)
    #@nonl
    #@-node:ekr.20051007080058:makeAllBindings
    #@+node:ekr.20060104154937:addModeCommands
    def addModeCommands (self):
        
        '''Add commands created by @mode settings to c.commandsDict and k.inverseCommandsDict.'''
    
        k = self ; c = k.c
        d = g.app.config.modeCommandsDict
        
        # Create the callback functions and update c.commandsDict and k.inverseCommandsDict.
        for key in d.keys():
    
            def enterModeCallback (event=None,name=key):
                k.enterNamedMode(event,name)
    
            c.commandsDict[key] = f = enterModeCallback
            k.inverseCommandsDict [f.__name__] = key
    #@nonl
    #@-node:ekr.20060104154937:addModeCommands
    #@+node:ekr.20051008152134:makeSpecialBindings (also binds to 'Key')
    def makeSpecialBindings (self):
        
        '''Make the bindings and set ivars for sepcial keystrokes.'''
        
        k = self ; c = k.c
        
        # These defaults may be overridden.
        for pane,stroke,ivar,commandName,func in (
            ('all', 'Alt-x',  'fullCommandKey',  'full-command',  k.fullCommand),
            ('all', 'Ctrl-g', 'abortAllModesKey','keyboard-quit', k.keyboardQuit),
            ('all', 'Ctrl-u', 'universalArgKey', 'universal-argument', k.universalArgument),
            #('all', 'Ctrl-c', 'quickCommandKey', 'quick-command', k.quickCommand),
            # These bindings for inside the minibuffer are strange beasts.
            # They are sent directly to k.fullcommand with a special callback.
            # ('mini', 'Alt-x',  None,'full-command',  k.fullCommand),
            # ('mini', 'Ctrl-g', None,'keyboard-quit', k.keyboardQuit),
            # ('mini', 'Ctrl-c', 'mb_copyKey', 'copy-text', f.copyText),
            # ('mini', 'Ctrl-v', 'mb_pasteKey','paste-text',f.pasteText),
            # ('mini', 'Ctrl-x', 'mb_cutKey',  'cut-text',  f.cutText),
        ):
            # Get the user shortcut *before* creating the callbacks.
            junk, bunchList = c.config.getShortcut(commandName)
            # g.trace(commandName,bunchList)
            if bunchList:
                for bunch in bunchList:
                    accel = (bunch and bunch.val)
                    shortcut, junk = c.frame.menu.canonicalizeShortcut(accel)
                    self.makeSpecialBinding(commandName,func,ivar,pane,shortcut,stroke)
            else:
                accel = stroke
                shortcut, junk = c.frame.menu.canonicalizeShortcut(accel)
                self.makeSpecialBinding(commandName,func,ivar,pane,shortcut,stroke)
    
        # Add a binding for <Key> events, so all key events go through masterCommand.
        def allKeysCallback (event):
            return k.masterCommand(event,func=None,stroke='<Key>')
    
        k.bindKey('all','<Key>',allKeysCallback,'master-command')
    #@nonl
    #@+node:ekr.20051220083410:makeSpecialBinding
    def makeSpecialBinding (self,commandName,func,ivar,pane,shortcut,stroke):
        
        k = self
        
        # g.trace(commandName,shortcut,stroke)
        
        if pane == 'mini' and func != k.keyboardQuit:
            if 0:
                # Call a strange callback that bypasses k.masterCommand.
                def minibufferKeyCallback(event,func=func,shortcut=shortcut):
                    k.fullCommand(event,specialStroke=shortcut,specialFunc=func)
        
                k.bindKey(pane,shortcut,minibufferKeyCallback,commandName)
        else:
                # Create two-levels of callbacks.
                def specialCallback (event,func=func):
                    return func(event)
        
                def keyCallback (event,func=specialCallback,stroke=shortcut):
                    return k.masterCommand(event,func,stroke)
        
                k.bindKey(pane,shortcut,keyCallback,commandName)
        
        if ivar:
            setattr(k,ivar,shortcut)
    #@nonl
    #@-node:ekr.20051220083410:makeSpecialBinding
    #@-node:ekr.20051008152134:makeSpecialBindings (also binds to 'Key')
    #@+node:ekr.20051008134059:makeBindingsFromCommandsDict
    def makeBindingsFromCommandsDict (self):
        
        '''Add bindings for all entries in c.commandDict.'''
    
        k = self ; c = k.c
        keys = c.commandsDict.keys() ; keys.sort()
    
        for commandName in keys:
            command = c.commandsDict.get(commandName)
            key, bunchList = c.config.getShortcut(commandName)
            for bunch in bunchList:
                accel = bunch.val
                if accel:
                    bind_shortcut, menu_shortcut = c.frame.menu.canonicalizeShortcut(accel)
                    k.bindShortcut(bunch.pane,bind_shortcut,command,commandName)
                    if 0:
                        if bunch: g.trace('%s %s %s' % (commandName,bunch.pane,bunch.val))
                        else:     g.trace(commandName)
    #@nonl
    #@-node:ekr.20051008134059:makeBindingsFromCommandsDict
    #@-node:ekr.20051006125633:Binding (keyHandler)
    #@+node:ekr.20051001051355:Dispatching...
    #@+node:ekr.20050920085536.65:masterCommand & helpers
    def masterCommand (self,event,func,stroke,commandName=None):
    
        '''This is the central dispatching method.
        All commands and keystrokes pass through here.'''
    
        k = self ; c = k.c
        c.setLog()
        trace = c.config.getBool('trace_masterCommand')
      
        c.startRedrawCount = c.frame.tree.redrawCount
        k.stroke = stroke # Set this global for general use.
        keysym = event and event.keysym or ''
        ch = event and event.char or ''
        w = event and event.widget
        state = event and hasattr(event,'state') and event.state or 0
        k.func = func
        k.funcReturn = None # For unit testing.
        if commandName is None:
            commandName = k.ultimateFuncName(func)
        special = keysym in (
            'Control_L','Alt_L','Shift_L','Control_R','Alt_R','Shift_R')
        interesting = func is not None or ch != '' # or stroke != '<Key>'
        interesting = not special
        
        if trace and interesting:
            g.trace(
                'stroke: ',stroke,'state:','%4x' % state,'ch:',repr(ch),'keysym:',repr(keysym),'\n',
                'stroke2:',c.frame.menu.convertEventToStroke(event),
                'widget:',w and g.app.gui.widget_name(w),'func:',func and func.__name__
            )
    
        # if interesting: g.trace(stroke,commandName,k.getStateKind())
    
        inserted = not special or (
            stroke != '<Key>' and (len(k.keysymHistory)==0 or k.keysymHistory[0]!=keysym))
    
        if inserted:
            # g.trace(stroke,keysym)
            #@        << add character to history >>
            #@+node:ekr.20050920085536.67:<< add character to history >>
            # Don't add multiple special characters to history.
            
            k.keysymHistory.insert(0,keysym)
            
            if len(ch) > 0:
                if len(keyHandlerClass.lossage) > 99:
                    keyHandlerClass.lossage.pop()
                keyHandlerClass.lossage.insert(0,ch)
            
            if 0: # traces
                g.trace(keysym,stroke)
                g.trace(k.keysymHistory)
                g.trace(keyHandlerClass.lossage)
            #@nonl
            #@-node:ekr.20050920085536.67:<< add character to history >>
            #@nl
            
        # We *must not* interfere with the global state in the macro class.
        if c.macroCommands.recordingMacro:
            done = c.macroCommands.startKbdMacro(event)
            if done: return 'break'
            
        # g.trace(stroke,k.abortAllModesKey)
    
        if k.abortAllModesKey and stroke == k.abortAllModesKey: # 'Control-g'
            k.clearState()
            k.keyboardQuit(event)
            k.endCommand(event,commandName)
            return 'break'
            
        if special: # Don't pass these on.
            return 'break' 
    
        if k.inState():
            val = k.callStateFunction(event) # Calls end-command.
            if val != 'do-func': return 'break'
            g.trace('Executing key outside of mode')
    
        if k.regx.iter:
            try:
                k.regXKey = keysym
                k.regx.iter.next() # EKR: next() may throw StopIteration.
            finally:
                return 'break'
    
        if k.abbrevOn:
            expanded = c.abbrevCommands.expandAbbrev(event)
            if expanded: return 'break'
    
        if func: # Func is an argument.
            if trace: g.trace('command',commandName)
            ### if commandName.startswith('leoCallback') or 
            if commandName.startswith('specialCallback'):
                # The callback function will call c.doCommand
                val = func(event)
                # k.simulateCommand uses k.funcReturn.
                k.funcReturn = k.funcReturn or val # For unit tests.
            else:
                # Call c.doCommand directly
                c.doCommand(func,commandName,event=event)
            k.endCommand(event,commandName)
            return 'break'
        else:
            val = k.handleDefaultChar(event)
            return val
    #@nonl
    #@+node:ekr.20050923172809.1:callStateFunction
    def callStateFunction (self,event):
        
        k = self ; val = None
        
        # g.trace(k.state.kind)
        
        if k.state.kind:
            if k.state.handler:
                val = k.state.handler(event)
                if val != 'continue':
                    k.endCommand(event,k.commandName)
            else:
                g.es_print('no state function for %s' % (k.state.kind),color='red')
                
        return val
    #@nonl
    #@-node:ekr.20050923172809.1:callStateFunction
    #@+node:ekr.20050923174229.3:callKeystrokeFunction (not used)
    def callKeystrokeFunction (self,event):
        
        '''Handle a quick keystroke function.
        Return the function or None.'''
        
        k = self
        numberOfArgs, func = k.keystrokeFunctionDict [k.stroke]
    
        if func:
            func(event)
            commandName = k.inverseCommandsDict.get(func) # Get the emacs command name.
            k.endCommand(event,commandName)
        
        return func
    #@nonl
    #@-node:ekr.20050923174229.3:callKeystrokeFunction (not used)
    #@+node:ekr.20051026083544:handleDefaultChar
    def handleDefaultChar(self,event):
        
        k = self ; c = k.c
        w = event and event.widget
        name = g.app.gui.widget_name(w)
        trace = c.config.getBool('trace_masterCommand')
        
        if trace: g.trace(name)
    
        if name.startswith('body') or name.startswith('head'):
            # For Leo 4.4a4: allow Tk defaults.
            # But this is dangerous, and should be removed.
            action = k.unboundKeyAction
            if action in ('insert','overwrite'):
                c.editCommands.selfInsertCommand(event,action=action)
            else:
                pass ; g.trace('ignoring key')
            return 'break'
        # elif name.startswith('head'):
            # g.trace("can't happen: %s" % (name),color='red')
            # c.frame.tree.updateHead(event,w)
            # return 'break'
        else:
            # Let tkinter handle the event.
            # ch = event and event.char ; g.trace('to tk:',name,repr(ch))
            return None
    #@nonl
    #@-node:ekr.20051026083544:handleDefaultChar
    #@-node:ekr.20050920085536.65:masterCommand & helpers
    #@+node:ekr.20050920085536.41:fullCommand (alt-x) & helper
    def fullCommand (self,event,specialStroke=None,specialFunc=None):
        
        '''Handle 'full-command' (alt-x) mode.'''
    
        k = self ; c = k.c ; f = c.frame ; state = k.getState('full-command')
        keysym = (event and event.keysym) or ''
        ch = (event and event.char) or ''
        g.trace('state',state,keysym)
        if state == 0:
            k.completionFocusWidget = g.app.gui.get_focus(c.frame)
            k.setState('full-command',1,handler=k.fullCommand) 
            k.setLabelBlue('%s' % (k.altX_prompt),protect=True)
            # Init mb_ ivars. This prevents problems with an initial backspace.
            k.mb_prompt = k.mb_tabListPrefix = k.mb_prefix = k.altX_prompt
            k.mb_tabList = [] ; k.mb_tabListIndex = -1
            f.minibufferWantsFocus()
        elif keysym == 'Return':
            c.frame.log.deleteTab('Completion')
            c.frame.widgetWantsFocus(k.completionFocusWidget) # Important, so cut-text works, e.g.
            k.callAltXFunction(event)
        elif keysym == 'Tab':
            k.doTabCompletion(c.commandsDict.keys())
            f.minibufferWantsFocus()
        elif keysym == 'BackSpace':
            k.doBackSpace(c.commandsDict.keys())
            f.minibufferWantsFocus()
        elif ch not in string.printable:
            if specialStroke:
                g.trace(specialStroke)
                specialFunc()
            f.minibufferWantsFocus()
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.mb_tabList = []
            k.updateLabel(event)
            k.mb_tabListPrefix = k.getLabel()
            f.minibufferWantsFocus()
            # g.trace('new prefix',k.mb_tabListPrefix)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.45:callAltXFunction
    def callAltXFunction (self,event):
        
        k = self ; c = k.c ; s = k.getLabel()
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
            k.endCommand(event,commandName)
        else:
            k.setLabel('Command does not exist: %s' % commandName)
    #@nonl
    #@-node:ekr.20050920085536.45:callAltXFunction
    #@-node:ekr.20050920085536.41:fullCommand (alt-x) & helper
    #@+node:ekr.20051001050607:endCommand
    def endCommand (self,event,commandName):
    
        '''Make sure Leo updates the widget following a command.
        
        Never changes the minibuffer label: individual commands must do that.
        '''
    
        k = self ; c = k.c
        # The command may have closed the window.
        if g.app.quitting or not c.exists: return
    
        # Set the best possible undoType: prefer explicit commandName to k.commandName.
        commandName = commandName or k.commandName or ''
        k.commandName = k.commandName or commandName or ''
        if commandName:
            bodyCtrl = c.frame.body.bodyCtrl
            if not k.inState():
                __pychecker__ = '--no-classattr --no-objattrs'
                    # initAllEditCommanders *does* exist.
                k.commandName = None
                leoEditCommands.initAllEditCommanders(c)
                try:
                    bodyCtrl.tag_delete('color')
                    bodyCtrl.tag_delete('color1')
                except Exception:
                    pass
            if 0: # Do *not* call this by default.  It interferes with undo.
                c.frame.body.onBodyChanged(undoType='Typing')
    #@nonl
    #@-node:ekr.20051001050607:endCommand
    #@-node:ekr.20051001051355:Dispatching...
    #@+node:ekr.20060115103349:Modes & input states
    #@+node:ekr.20060102135349.2:enterNamedMode
    def enterNamedMode (self,event,commandName):
        
        k = self ; c = k.c
        modeName = commandName[6:]
        
        k.generalModeHandler(event,modeName=modeName)
    #@-node:ekr.20060102135349.2:enterNamedMode
    #@+node:ekr.20060121104301:exitNamedMode
    def exitNamedMode (self,event):
        
        k = self
    
        if k.inState():
            k.endMode(event)
        
        k.showStateAndMode()
    #@-node:ekr.20060121104301:exitNamedMode
    #@+node:ekr.20060104164523:modeHelp
    def modeHelp (self,event):
    
        '''The mode-help command.
        
        A possible convention would be to bind <Tab> to this command in most modes,
        by analogy with tab completion.'''
        
        k = self ; c = k.c
        
        c.endEditing(restoreFocus=True)
        
        if k.inputModeName:
            d = g.app.config.modeCommandsDict.get('enter-'+k.inputModeName)
            k.modeHelpHelper(d)
        # else:
            # k.printBindings(event,brief=True)
    
        return 'break'
    #@nonl
    #@+node:ekr.20060104125946:modeHelpHelper
    def modeHelpHelper (self,d):
        
        k = self ; c = k.c ; tabName = 'Mode'
        c.frame.log.clearTab(tabName)
        keys = d.keys() ; keys.sort()
    
        data = [] ; n = 20
        for key in keys:
            bunchList = d.get(key)
            for bunch in bunchList:
                shortcut = bunch.val
                if shortcut not in (None,'None'):
                    s1 = key
                    s2 = k.prettyPrintKey(shortcut)
                    n = max(n,len(s1))
                    data.append((s1,s2),)
                    
        data.sort()
        
        g.es('%s\n\n' % (k.inputModeName),tabName=tabName)
            
        # This isn't perfect in variable-width fonts.
        for s1,s2 in data:
            g.es('%*s %s' % (n,s1,s2),tabName=tabName)
    #@nonl
    #@-node:ekr.20060104125946:modeHelpHelper
    #@-node:ekr.20060104164523:modeHelp
    #@+node:ekr.20060104110233:generalModeHandler & helpers
    def generalModeHandler (self,event,
        bunch=None,commandName=None,func=None,modeName=None):
        
        '''Handle a mode defined by an @mode node in leoSettings.leo.'''
    
        k = self ; c = k.c
        state = k.getState(modeName)
        w = g.app.gui.get_focus(c.frame)
        trace = c.config.getBool('trace_modes')
        
        if trace: g.trace(modeName,state)
       
        if state == 0:
            self.initMode(event,modeName)
            k.setState(modeName,1,handler=k.generalModeHandler)
            if c.config.getBool('showHelpWhenEnteringModes'):
                k.modeHelp(event)
            else:
                c.frame.log.deleteTab('Mode')
                c.frame.widgetWantsFocus(w)
        elif not func:
            g.trace('No func: improper key binding')
            return 'break'
        else:
            if trace: g.trace(modeName,state,commandName)
            if commandName == 'mode-help':
                func(event)
            else:
                nextMode = bunch.nextMode
                self.endMode(event)
                func(event)
                if nextMode == 'none':
                    # Do *not* clear k.inputModeName or the focus here.
                    # func may have put us in *another* mode.
                    pass
                elif nextMode == 'same':
                    self.initMode(event,modeName) # Re-enter this mode.
                    k.setState(modeName,1,handler=k.generalModeHandler)
                else:
                    self.initMode(event,nextMode) # Enter another mode.
    
        return 'break'
    #@nonl
    #@+node:ekr.20060117202916:badMode
    def badMode(self,modeName):
        
        k = self
    
        k.clearState()
        if modeName.endswith('-mode'): modeName = modeName[:-5]
        k.setLabelGrey('@mode %s is not defined (or is empty)' % modeName)
    #@nonl
    #@-node:ekr.20060117202916:badMode
    #@+node:ekr.20060119150624:createModeBindings
    def createModeBindings (self,modeName,tagName,d):
        
        k = self ; c = k.c ; t = c.frame.body.bodyCtrl
        
        for commandName in d.keys():
            func = c.commandsDict.get(commandName)
            if func:
                bunchList = d.get(commandName,[])
                for bunch in bunchList:
                    shortcut = bunch.val
                    if shortcut and shortcut not in ('None','none',None):
                        stroke, junk = c.frame.menu.canonicalizeShortcut(shortcut)
                        # g.trace(stroke,shortcut)
                        #@                    << define modeCallback >>
                        #@+node:ekr.20060118181341:<< define modeCallback >>
                        # g.trace('Mode %s: binding %s to %s' % (modeName,stroke,commandName))
                        
                        def modeCallback (event,k=k,
                            bunch=bunch,commandName=commandName,func=func,modeName=modeName,stroke=stroke):
                                
                            __pychecker__ = '--no-argsused' # stroke
                            
                            # g.trace(stroke)
                            return k.generalModeHandler(event,bunch,commandName,func,modeName)
                        
                        # k.bindKey('all',stroke,modeCallback,commandName)
                        
                        t.bind_class(tagName,stroke,modeCallback)
                        #@nonl
                        #@-node:ekr.20060118181341:<< define modeCallback >>
                        #@nl
            else:
                g.trace('No such command: %s' % commandName)
    
        #@    << define modeHelpCallback >>
        #@+node:ekr.20060119145631:<< define modeHelpCallback >>
        def modeHelpCallback (event,k=k):
            
            if event and event.char != '':
                return k.modeHelp(event)
            else:
                return 'break'
        
        # k.bindKey('all',stroke,modeHelpCallback,commandName)
        
        t.bind_class(tagName,'<Key>',modeHelpCallback,'+')
        #@nonl
        #@-node:ekr.20060119145631:<< define modeHelpCallback >>
        #@nl
    #@nonl
    #@-node:ekr.20060119150624:createModeBindings
    #@+node:ekr.20060117202916.1:initMode
    def initMode (self,event,modeName):
    
        k = self ; c = k.c
        
        if not modeName:
            g.trace('No mode name')
            return
    
        k.inputModeName = modeName
        d = g.app.config.modeCommandsDict.get('enter-'+modeName)
        if not d:
            self.badMode(modeName)
            return
    
        t = k.modeWidget = g.app.gui.get_focus(c.frame)        
        # t = c.frame.body.bodyCtrl
        k.savedBindtags = t.bindtags()
        tagName = '%s-%s' % (modeName,c.fileName())
        t.bindtags(tuple([tagName]))
        # g.trace(modeName,tagName,t.bindtags())
            
        # Note: we much create separate bindings for each commander.
        modeBindings = k.bindtagsDict.get(tagName)
        if not modeBindings:
            # g.trace('created mode bindings: %s' % (tagName))
            k.createModeBindings(modeName,tagName,d)
            k.bindtagsDict[tagName] = True
    
        k.setLabelBlue(modeName+': ',protect=True)
        k.showStateAndMode()
        # Do *not* change the focus here!
    #@nonl
    #@-node:ekr.20060117202916.1:initMode
    #@+node:ekr.20060117202916.2:endMode
    def endMode(self,event):
        
        k = self ; c = k.c
        
        w = g.app.gui.get_focus(c.frame)
    
        # Restore the bind tags.
        # t = c.frame.body.bodyCtrl
        t = k.modeWidget
        t.bindtags(k.savedBindtags)
        k.savedBindtags = None
        
        c.frame.log.deleteTab('Mode')
    
        k.endCommand(event,k.stroke)
        k.inputModeName = None
        k.clearState()
        k.resetLabel()
        k.showStateAndMode()
    
        # k.setLabelGrey('top-level mode')
        
        # Do *not* change the focus: the command may have changed it.
        c.frame.widgetWantsFocus(w)
    #@nonl
    #@-node:ekr.20060117202916.2:endMode
    #@-node:ekr.20060104110233:generalModeHandler & helpers
    #@+node:ekr.20060105132013:set-xxx-State & setInputState
    def setIgnoreState (self,event):
    
        self.setInputState('ignore',showState=True)
    
    def setInsertState (self,event):
    
        self.setInputState('insert',showState=True)
    
    def setOverwriteState (self,event):
    
        self.setInputState('overwrite',showState=True)
    
    #@+node:ekr.20060120200818:setInputState
    def setInputState (self,state,showState=False):
    
        k = self ; c = k.c
        
        w = g.app.gui.get_focus(c.frame)
        
        if 0: # Support for plain-key bindings.
            tag = k.plainKeyTag()
                       
            try: # Will fail for nullBody.
                # t = c.frame.top
                t = c.frame.body.bodyCtrl
                tags = list(t.bindtags())
                
            except AttributeError:
                tags = [] ; t = w = None
    
            if tags:
                if state == 'ignore':
                    if tag not in tags:
                        tags.insert(0,tag)
                        t.bindtags(tuple(tags))
                else:
                    if tag in tags:
                        tags.remove(tag)
                        t.bindtags(tuple(tags))
    
            g.trace('%s-state' % (state),'plain key functions are',
                g.choose(tag in tags,'enabled','disabled')) # ,tags)
    
        k.unboundKeyAction = state
        if state != 'insert' or showState:
            k.showStateAndMode()
       
        # These commands never change focus.
        w and c.frame.widgetWantsFocus(w)
    #@nonl
    #@-node:ekr.20060120200818:setInputState
    #@-node:ekr.20060105132013:set-xxx-State & setInputState
    #@+node:ekr.20060120193743:showStateAndMode
    def showStateAndMode(self):
        
        k = self ; frame = k.c.frame
        state = k.unboundKeyAction
        mode = k.getStateKind()
       
        if hasattr(frame,'clearStatusLine'):
            frame.clearStatusLine()
            put = frame.putStatusLine
            if state != 'insert':
                put('state: ',color='blue')
                put(state)
            if mode:
                put(' mode: ',color='blue')
                put(mode)
    #@-node:ekr.20060120193743:showStateAndMode
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
            
        # k.showStateAndMode()
    #@-node:ekr.20050923172814.4:setState
    #@-node:ekr.20050923172809:State...
    #@-node:ekr.20060115103349:Modes & input states
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
    #@+node:ekr.20051014170754:k.help
    def help (self,event):
        
        k = self ; c = k.c
        commands = (
            k.fullCommand,
            k.quickCommand,
            k.universalArgument,
            k.keyboardQuit,
            # negative-argument
            # repeat-complex-command
        )
        shortcuts = [
            k.getShortcutForCommand(command)
            for command in commands]
    
        # A bug in Leo: triple quotes puts indentation before each line.
        s = '''
    The mini-buffer is intended to be like the Emacs buffer:
    
    %s: Just like Emacs Alt-x: starts minibuffer. The prompt is 'full-command' Type a
    full command name, then hit <Return> to execute the command. Tab completion
    works, but not for file names.
    
    %s: Like Emacs Control-C: (Ctrl-C conflicts with XP cut). starts minibuffer.
    The prompt is 'quick-command'. This mode is not completed, but stuff like
    `Ctrl-C r` and `Ctrl r r` do work.
    
    %s: Like Emacs Ctrl-u: (Ctrl-u conflicts with move-outline-up). Add a repeat
    count for later command. Ctrl-u 999 a adds 999 a's, but many features remain
    unfinished.
    
    %s: Just like Emacs Ctrl-g: Closes the mini-buffer.
    '''
    
        s = g.adjustTripleString(s,c.tab_width)
            # Remove indentation from indentation of this function.
        s = s % (shortcuts[0],shortcuts[1],shortcuts[2],shortcuts[3])
        g.es_print(s)
    #@nonl
    #@-node:ekr.20051014170754:k.help
    #@+node:ekr.20051014155551:k.show/hide/toggleMinibuffer
    def hideMinibuffer (self,event):
        
        k = self ; c = k.c
        
        c.frame.hideMinibuffer()
        
        g.es('Minibuffer hidden',color='red')
    
        for commandName in ('show-mini-buffer','toggle-mini-buffer'):
            shortcut = k.getShortcutForCommandName(commandName)
            if shortcut:
                g.es('%s is bound to: %s' % (commandName,shortcut))
        
        
    def showMinibuffer (self,event):
        
        k = self ; c = k.c
        
        c.frame.showMinibuffer()
        
    def toggleMinibuffer (self,event):
        
        k = self ; c = k.c
        
        if c.frame.minibufferVisible:
            k.hideMinibuffer(event)
        else:
            k.showMinibuffer(event)
    #@nonl
    #@-node:ekr.20051014155551:k.show/hide/toggleMinibuffer
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
    #@+node:ekr.20051012201831:printBindings
    def printBindings (self,event,brief=False):
    
        '''Print all the bindings presently in effect.'''
    
        k = self ; c = k.c
        d = k.bindingsDict ; tabName = 'Bindings'
        keys = d.keys() ; keys.sort()
        c.frame.log.clearTab(tabName)
    
        data = [] ; n = 20
        for key in keys:
            bunchList = d.get(key,[])
            for b in bunchList:
                if not brief or k.isPlainKey(key):
                    pane = g.choose(b.pane=='all','',' [%s]' % (b.pane))
                    s1 = k.prettyPrintKey(key) + pane
                    s2 = b.commandName
                    n = max(n,len(s1))
                    data.append((s1,s2),)
        
        # This isn't perfect in variable-width fonts.
        for s1,s2 in data:
            g.es('%*s\t%s' % (-(n+1),s1,s2),tabName=tabName)
                       
        state = k.unboundKeyAction 
        k.showStateAndMode()
    #@nonl
    #@-node:ekr.20051012201831:printBindings
    #@+node:ekr.20051014061332:printCommands
    def printCommands (self,event):
    
        '''Print all the known commands and their bindings, if any.'''
    
        k = self ; c = k.c ; tabName = 'Commands'
        
        c.frame.log.clearTab(tabName)
        
        inverseBindingDict = k.computeInverseBindingDict()
        commandNames = c.commandsDict.keys() ; commandNames.sort()
    
        data = [] ; n = 20
        for commandName in commandNames:
            shortcutList = inverseBindingDict.get(commandName,[''])
            for shortcut in shortcutList:
                s1 = commandName
                s2 = k.prettyPrintKey(shortcut)
                n = max(n,len(s1))
                data.append((s1,s2),)
                    
        # This isn't perfect in variable-width fonts.
        for s1,s2 in data:
            g.es('%*s\t%s' % (-(n+1),s1,s2),tabName=tabName)
    #@-node:ekr.20051014061332:printCommands
    #@+node:ekr.20050920085536.48:repeatComplexCommand & helper
    def repeatComplexCommand (self,event):
    
        k = self
    
        if k.mb_history:
            k.setState('last-full-command',1,handler=k.doLastAltX)
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
    #@+node:ekr.20050920085536.73:universalDispatcher & helpers
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
            # g.trace(state,stroke)
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
                # g.trace('stroke',k.stroke,'keysym',keysym)
                val = k.getLabel(ignorePrompt=True)
                try:                n = int(val) * k.repeatCount
                except ValueError:  n = 1
                # g.trace('val',repr(val),'n',n,'k.repeatCount',k.repeatCount)
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
        
        __pychecker__ = '--no-local' # z is used just for a repeat count.
        
        k = self ; stroke = k.stroke ; w = event.widget
        g.trace('stroke',stroke,'keycode',event.keycode,'n',n)
    
        if stroke == k.fullCommandKey:
            for z in xrange(n):
                k.fullCommand()
        else:
            stroke = stroke.lstrip('<').rstrip('>')
            bunchList = k.bindingsDict.get(stroke,[])
            if bunchList:
                b = bunchList[0]
                g.trace('method',b.f)
                for z in xrange(n):
                    if 1: # No need to do this: commands never alter events.
                        ev = Tk.Event()
                        ev.widget = event.widget
                        ev.keysym = event.keysym
                        ev.keycode = event.keycode
                        ev.char = event.char
                    k.masterCommand(event,b.f,'<%s>' % stroke)
            else:
                for z in xrange(n):
                    w.event_generate('<Key>',keycode=event.keycode,keysym=event.keysym)
    #@nonl
    #@-node:ekr.20050920085536.75:executeNTimes
    #@+node:ekr.20050920085536.76:doControlU
    def doControlU (self,event,stroke):
        
        k = self ; c = k.c
    
        k.setLabelBlue('Control-u %s' % stroke.lstrip('<').rstrip('>'))
    
        if event.keysym == 'parenleft': # Execute the macro.
    
            k.clearState()
            k.resetLabel()
            c.macroCommands.startKbdMacro(event)
            c.macroCommands.callLastKeyboardMacro(event)
    #@nonl
    #@-node:ekr.20050920085536.76:doControlU
    #@-node:ekr.20050920085536.73:universalDispatcher & helpers
    #@+node:ekr.20051006065121:Externally visible helpers
    #@+node:ekr.20050920085536.64:manufactureKeyPressForCommandName
    def manufactureKeyPressForCommandName (self,w,commandName):
        
        '''Implement a command by passing a keypress to Tkinter.'''
    
        k = self
        
        shortcut = k.getShortcutForCommandName(commandName)
        
        if shortcut and w:
            w.event_generate(shortcut)
        else:
             g.trace('no shortcut for %s' % (commandName),color='red')
    #@nonl
    #@-node:ekr.20050920085536.64:manufactureKeyPressForCommandName
    #@+node:ekr.20051105155441:simulateCommand
    def simulateCommand (self,commandName):
        
        k = self ; c = k.c
        
        func = c.commandsDict.get(commandName)
        
        if func:
            # g.trace(commandName,func.__name__)
            stroke = None
            ### if commandName.startswith('leoCallback') or 
            if commandName.startswith('specialCallback'):
                event = None # A legacy function.
            else: # Create a dummy event as a signal.
                event = g.bunch(keysym = '',char = '',widget = None)
            k.masterCommand(event,func,stroke)
            return k.funcReturn
        else:
            g.trace('no command for %s' % (commandName),color='red')
            if g.app.unitTesting: raise AttributeError
    #@nonl
    #@-node:ekr.20051105155441:simulateCommand
    #@+node:ekr.20050920085536.62:getArg
    def getArg (self,event,
        returnKind=None,returnState=None,handler=None,
        prefix=None,tabList=None,completion=True):
        
        '''Accumulate an argument until the user hits return (or control-g).
        Enter the given return state when done.
        The prefix is does not form the arg.  The prefix defaults to the k.getLabel().
        '''
    
        k = self ; c = k.c ; state = k.getState('getArg')
        keysym = (event and event.keysym) or ''
        # g.trace('state',state,'keysym',keysym,'completion',completion)
        if state == 0:
            k.arg = '' ; k.arg_completion = completion
            if tabList: k.argTabList = tabList[:]
            else:       k.argTabList = []
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
            bodyCtrl = c.frame.body.bodyCtrl
            c.frame.widgetWantsFocus(bodyCtrl)
            k.afterGetArgState=returnKind,returnState,handler
            k.setState('getArg',1,k.getArg)
            k.afterArgWidget = event and event.widget or c.frame.body.bodyCtrl
        elif keysym == 'Return':
            k.arg = k.getLabel(ignorePrompt=True)
            kind,n,handler = k.afterGetArgState
            if kind: k.setState(kind,n,handler)
            c.frame.log.deleteTab('Completion')
            if handler: handler(event)
            c.frame.widgetWantsFocus(k.afterArgWidget)
        elif keysym == 'Tab':
            k.doTabCompletion(k.argTabList,k.arg_completion)
        elif keysym == 'BackSpace':
            k.doBackSpace(k.argTabList,k.arg_completion)
            c.frame.minibufferWantsFocus()
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.mb_tabList = []
            k.updateLabel(event)
            k.mb_tabListPrefix = k.getLabel()
    
        return 'break'
    #@-node:ekr.20050920085536.62:getArg
    #@+node:ekr.20050920085536.63:keyboardQuit
    def keyboardQuit (self,event):
    
        '''This method clears the state and the minibuffer label.
        
        k.endCommand handles all other end-of-command chores.'''
        
        k = self ; c = k.c
    
        if g.app.quitting:
            return
    
        c.frame.log.deleteTab('Completion')
        c.frame.log.deleteTab('Mode')
        
        # Completely clear the mode.
        if k.inputModeName:
            k.endMode()
    
        # Complete clear the state.
        k.state.kind = None
        k.state.n = None
            
        k.clearState()
        k.resetLabel()
        
        k.setDefaultUnboundKeyAction()
        k.showStateAndMode()
        c.endEditing()
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920085536.63:keyboardQuit
    #@+node:ekr.20051015110547:k.registerCommand
    def registerCommand (self,commandName,shortcut,func,pane='all',verbose=True):
        
        '''Make the function available as a minibuffer command,
        and optionally attempt to bind a shortcut.
        
        You can wrap any method in a callback function, so the
        restriction to functions is not significant.'''
        
        k = self ; c = k.c
        
        f = c.commandsDict.get(commandName)
        if f:
            g.es_trace('Redefining %s' % (commandName), color='red')
            
        c.commandsDict [commandName] = func
        k.inverseCommandsDict [func.__name__] = commandName
        
        if shortcut:
            # Retain the original spelling of the shortcut for the message.
            shortcut, junk = c.frame.menu.canonicalizeShortcut(shortcut)
            ok = k.bindShortcut (pane,shortcut,func,commandName)
            if verbose and ok:
                 g.es_print('Registered %s bound to %s' % (
                    commandName,k.prettyPrintKey(shortcut)),color='blue')
        else:
            if verbose:
                g.es_print('Registered %s' % (commandName), color='blue')
    #@nonl
    #@-node:ekr.20051015110547:k.registerCommand
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
    #@+node:ekr.20060125175103:k.minibufferWantsFocus
    def minibufferWantsFocus(self):
        
        c = self.c
        
        if self.useTextWidget:
            # Important! We must preserve body selection!
            c.frame.widgetWantsFocus(c.miniBufferWidget)
        else:
            c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20060125175103:k.minibufferWantsFocus
    #@+node:ekr.20051023132350:getLabel
    def getLabel (self,ignorePrompt=False):
        
        k = self ; w = self.widget
        if not w: return ''
        
        if self.useTextWidget:
            w.update_idletasks()
            s = w and w.get('1.0','end')
            # Remove the cursed Tk newline.
            while s.endswith('\n') or s.endswith('\r'):
                s = s[:-1]
            # g.trace(repr(s))
        else:
            s = k.svar and k.svar.get()
    
        if ignorePrompt:
            return s[len(k.mb_prefix):]
        else:
            return s or ''
    
    #@-node:ekr.20051023132350:getLabel
    #@+node:ekr.20051023132350.2:protectLabel
    def protectLabel (self):
        
        k = self ; w = self.widget
        if not w: return
    
        if self.useTextWidget:
            w.update_idletasks()
            k.mb_prefix = w.get('1.0','end')
        else:
            if k.svar:
                k.mb_prefix = k.svar.get()
    #@nonl
    #@-node:ekr.20051023132350.2:protectLabel
    #@+node:ekr.20050920085536.37:resetLabel
    def resetLabel (self):
        
        k = self
        k.setLabelGrey('')
        k.mb_prefix = ''
    #@nonl
    #@-node:ekr.20050920085536.37:resetLabel
    #@+node:ekr.20051023132350.1:setLabel
    def setLabel (self,s,protect=False):
    
        k = self ; w = self.widget
        if not w: return
    
        # g.trace(repr(s))
    
        if self.useTextWidget:
            k.c.frame.minibufferWantsFocus()
            # w.update_idletasks()
            w.delete('1.0','end')
            w.insert('1.0',s)
        else:
            if k.svar: k.svar.set(s)
    
        if protect:
            k.mb_prefix = s
    #@nonl
    #@-node:ekr.20051023132350.1:setLabel
    #@+node:ekr.20050920085536.36:setLabelBlue
    def setLabelBlue (self,label=None,protect=False):
        
        k = self ; w = k.widget
        if not w: return
        
        w.configure(background='lightblue')
    
        if label is not None:
            k.setLabel(label,protect)
    #@nonl
    #@-node:ekr.20050920085536.36:setLabelBlue
    #@+node:ekr.20050920085536.35:setLabelGrey
    def setLabelGrey (self,label=None):
    
        k = self ; w = self.widget
        if not w: return
        
        w.configure(background='lightgrey')
        if label is not None:
            k.setLabel(label)
    
    setLabelGray = setLabelGrey
    #@nonl
    #@-node:ekr.20050920085536.35:setLabelGrey
    #@+node:ekr.20050920085536.38:updateLabel
    def updateLabel (self,event,suppressControlChars=True):
    
        '''Mimic what would happen with the keyboard and a Text editor
        instead of plain accumalation.'''
        
        k = self ; s = k.getLabel()
        ch = (event and event.char) or ''
        keysym = (event and event.keysym) or ''
        
        # g.trace(repr(s),ch,keysym,k.stroke)
        
        if ch == '\b': # Handle backspace.
            # Don't backspace over the prompt.
            if len(s) <= k.mb_prefix:
                return 
            elif len(s) == 1: s = ''
            else: s = s [0:-1]
        elif suppressControlChars and ch not in string.printable:
            return
        elif ch and ch not in ('\n','\r'):
            s = s + ch # Add the character.
        
        k.setLabel(s)
    #@nonl
    #@-node:ekr.20050920085536.38:updateLabel
    #@-node:ekr.20050924064254:Label...
    #@+node:ekr.20051002152108.1:Shared helpers
    #@+node:ekr.20051017212452:computeCompletionList
    # Important: this code must not change mb_tabListPrefix.  Only doBackSpace should do that.
    
    def computeCompletionList (self,defaultTabList,backspace):
        
        k = self ; c = k.c ; s = k.getLabel() 
        command = s [len(k.mb_prompt):]
            # s always includes prefix, so command is well defined.
    
        k.mb_tabList,common_prefix = g.itemsMatchingPrefixInList(command,defaultTabList)
    
        c.frame.log.clearTab('Completion') # Creates the tab if necessary.
    
        if k.mb_tabList:
            k.mb_tabListIndex = -1 # The next item will be item 0.
    
            if not backspace:
                k.setLabel(k.mb_prompt + common_prefix)
                
            inverseBindingDict = k.computeInverseBindingDict()
            for commandName in k.mb_tabList:
                shortcutList = inverseBindingDict.get(commandName,[''])
                for shortcut in shortcutList:
                    g.es('%s %s' % (commandName,k.prettyPrintKey(shortcut)),tabName='Completion')
    
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051017212452:computeCompletionList
    #@+node:ekr.20051018070524:computeInverseBindingDict
    def computeInverseBindingDict (self):
    
        k = self ; d = {}
        
        # keys are minibuffer command names, values are shortcuts.
        for shortcut in k.bindingsDict.keys():
            bunchList = k.bindingsDict.get(shortcut,[])
            for b in bunchList:
                shortcutList = d.get(b.commandName,[])
                bunchList = k.bindingsDict.get(shortcut,[g.Bunch(pane='all')])
                for b in bunchList:
                    # g.trace(shortcut,repr(b.pane))
                    pane = g.choose(b.pane=='all','','[%s]' % (b.pane))
                    s = '%s %s' % (k.prettyPrintKey(shortcut),pane)
                    if s not in shortcutList:
                        shortcutList.append(s)
                d [b.commandName] = shortcutList
    
        return d
    #@nonl
    #@-node:ekr.20051018070524:computeInverseBindingDict
    #@+node:ekr.20050920085536.46:doBackSpace
    # Used by getArg and fullCommand.
    
    def doBackSpace (self,defaultCompletionList,redraw=True):
    
        '''Cut back to previous prefix and update prefix.'''
    
        k = self ; c = k.c
    
        if len(k.mb_tabListPrefix) > len(k.mb_prefix):
    
            k.mb_tabListPrefix = k.mb_tabListPrefix [:-1]
            k.setLabel(k.mb_tabListPrefix)
    
        if redraw:
            k.computeCompletionList(defaultCompletionList,backspace=True)
    #@nonl
    #@-node:ekr.20050920085536.46:doBackSpace
    #@+node:ekr.20050920085536.44:doTabCompletion
    # Used by getArg and fullCommand.
    
    def doTabCompletion (self,defaultTabList,redraw=True):
        
        '''Handle tab completion when the user hits a tab.'''
        
        k = self ; c = k.c ; s = k.getLabel().strip()
        
        if k.mb_tabList and s.startswith(k.mb_tabListPrefix):
            # g.trace('cycle',repr(s))
            # Set the label to the next item on the tab list.
            k.mb_tabListIndex +=1
            if k.mb_tabListIndex >= len(k.mb_tabList):
                k.mb_tabListIndex = 0
            k.setLabel(k.mb_prompt + k.mb_tabList [k.mb_tabListIndex])
        else:
            if redraw:
                k.computeCompletionList(defaultTabList,backspace=False)
    
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920085536.44:doTabCompletion
    #@+node:ekr.20051014170754.1:getShortcutForCommand/Name (should return lists)
    def getShortcutForCommandName (self,commandName):
        
        k = self ; c = k.c
    
        command = c.commandsDict.get(commandName)
    
        if command:
            for key in k.bindingsDict:
                bunchList = k.bindingsDict.get(key,[])
                for b in bunchList:
                    if b.commandName == commandName:
                        return '<%s>' % key.lstrip('<').rstrip('>')
        return ''
        
    def getShortcutForCommand (self,command):
        
        k = self ; c = k.c
        
        if command:
            for key in k.bindingsDict:
                bunchList = k.bindingsDict.get(key,[])
                for b in bunchList:
                    if b.commandName == command.__name__:
                         return '<%s>' % key.lstrip('<').rstrip('>')
        return ''
    #@nonl
    #@-node:ekr.20051014170754.1:getShortcutForCommand/Name (should return lists)
    #@+node:ekr.20051122104219:prettyPrintKey
    def prettyPrintKey (self,key):
        
        '''Print a shortcut in a pleasing way.'''
        
        return self.c.frame.menu.canonicalizeShortcut(key)[1] or ''
        
        # s = self.c.frame.menu.canonicalizeShortcut(key)[1] or ''
        # return len(s) == 1 and 'Key+' + s or s
    #@nonl
    #@-node:ekr.20051122104219:prettyPrintKey
    #@+node:ekr.20051010063452:ultimateFuncName
    def ultimateFuncName (self,func):
        
        '''Return func.__name__ unless it is 'leoCallback.
        In that case, return the name in k.leoCallbackDict.get(func).'''
        
        k = self
        
        if not func:
            return '<no function>'
            
        if func.__name__ != 'leoCallback':
            return func.__name__
            
        g.trace('oops: leoCallback seen')
            
        # Get the function wrapped by this particular leoCallback function.
        calledFunc = k.leoCallbackDict.get(func)
        if calledFunc:
            return 'leoCallback -> %s' % calledFunc.__name__ 
        else:
            return '<no leoCallback name>'
    #@nonl
    #@-node:ekr.20051010063452:ultimateFuncName
    #@+node:ekr.20060114171910:traceBinding
    def traceBinding (self,bunch,shortcut,w):
    
        k = self ; c = k.c
    
        if not c.config.getBool('trace_bindings'): return
        
        theFilter = c.config.getString('trace_bindings_filter') or ''
        if theFilter and shortcut.lower().find(theFilter.lower()) == -1: return
        
        pane_filter = c.config.getString('trace_bindings_pane_filter')
        
        if not pane_filter or pane_filter.lower() == bunch.pane:
             g.trace(bunch.pane,k.prettyPrintKey(shortcut),bunch.commandName,w._name)
    #@nonl
    #@-node:ekr.20060114171910:traceBinding
    #@-node:ekr.20051002152108.1:Shared helpers
    #@-others
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
