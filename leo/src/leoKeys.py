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

#@+others
#@+node:ekr.20051006121222:inputMode classes
#@<< baseInputMode class >>
#@+node:ekr.20051006121222.8: << baseInputMode class >>
class baseInputMode:
    
    """A class to represent an input mode in the status line and all related commands."""
    
    #@    @+others
    #@+node:ekr.20051006121222.9:ctor
    def __init__ (self,c,statusLine):
        
        self.c = c
        
        self.statusLine = statusLine
        self.signon = None
        self.name = "baseMode"
        self.clear = True
        self.keys = []
    #@nonl
    #@-node:ekr.20051006121222.9:ctor
    #@+node:ekr.20051006121222.10:doNothing
    def doNothing(self,event=None):
        
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.10:doNothing
    #@+node:ekr.20051006121222.11:enterMode
    def enterMode (self,event=None):
        
        # g.trace(self.name)
            
        self.initBindings()
        
        if self.clear:
            self.clearStatusLine()
    
        if self.signon:
            self.putStatusLine(self.signon,color="red")
            
        self.originalLine = self.getStatusLine()
        if self.originalLine and self.originalLine[-1] == '\n':
            self.originalLine = self.originalLine[:-1]
    
        # g.trace(repr(self.originalLine))
    
        self.enableStatusLine()
        self.setFocusStatusLine()
        
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.11:enterMode
    #@+node:ekr.20051006121222.12:exitMode
    def exitMode (self,event=None,nextMode=None):
        
        """Remove all key bindings for this mode."""
        
        # g.trace(self.name)
        
        self.unbindAll()
    
        if nextMode:
            nextMode.enterMode()
        else:
            self.clearStatusLine()
            self.disableStatusLine()
            self.c.frame.body.setFocus()
            self.c.frame.body.bodyCtrl.bind(
                "<Key-Escape>",self.statusLine.topMode.enterMode)
    
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.12:exitMode
    #@+node:ekr.20051006121222.13:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
        
        self.unbindAll()
    
        t.bind("<Key-Escape>",self.exitMode)
    #@nonl
    #@-node:ekr.20051006121222.13:initBindings
    #@+node:ekr.20051006121222.14:statusLine proxies
    def clearStatusLine (self):
        self.c.frame.clearStatusLine()
    
    def disableStatusLine (self):
        # g.trace()
        self.c.frame.disableStatusLine()
    
    def enableStatusLine (self):
        # g.trace()
        self.c.frame.enableStatusLine()
        
    def getStatusLine (self):
        return self.c.frame.getStatusLine()
    
    def putStatusLine(self,s,color="black"):
        self.c.frame.putStatusLine(s,color=color)
        
    def setFocusStatusLine(self):
        # g.trace()
        self.c.frame.setFocusStatusLine()
        
    def statusLineIsEnabled(self):
        return self.c.frame.statusLineIsEnabled()
    #@nonl
    #@-node:ekr.20051006121222.14:statusLine proxies
    #@+node:ekr.20051006121222.15:unbindAll
    def unbindAll (self):
        
        t = self.c.frame.statusText
        
        for b in t.bind():
            t.unbind(b)
    #@nonl
    #@-node:ekr.20051006121222.15:unbindAll
    #@-others
#@nonl
#@-node:ekr.20051006121222.8: << baseInputMode class >>
#@nl

#@+others
#@+node:ekr.20051006121222.16:class topInputMode (baseInputMode)
class topInputMode (baseInputMode):
    
    """A class to represent the top-level input mode in the status line."""
    
    #@    @+others
    #@+node:ekr.20051006121222.17:ctor
    def __init__(self,c,statusLineClass):
        
        baseInputMode.__init__(self,c,statusLineClass)
    
        self.name = "topInputMode"
        
        
    #@nonl
    #@-node:ekr.20051006121222.17:ctor
    #@+node:ekr.20051006121222.18:finishCreate
    def finishCreate(self):
        
        s = self.statusLine
        
        self.bindings = (
            ('c','Change',s.findChangeMode),
            ('e','Edit',None),
            ('f','Find',s.findMode),
            ('h','Help',None),
            ('o','Outline',None),
            ('p','oPtions',s.optionsMode),
        )
    
        signon = ["%s: " % (text) for ch,text,f in self.bindings]
        self.signon = ''.join(signon)
    #@nonl
    #@-node:ekr.20051006121222.18:finishCreate
    #@+node:ekr.20051006121222.19:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
    
        self.unbindAll()
        
        t.bind("<Key>",self.doNothing)
        t.bind("<Key-Escape>",self.exitMode)
        
        for ch,text,f in self.bindings:
    
            def inputModeCallback(event,self=self,ch=ch,text=text,f=f):
                return self.doKey(ch,text,f)
    
            t.bind("<Key-%s>" % ch, inputModeCallback)
    #@nonl
    #@-node:ekr.20051006121222.19:initBindings
    #@+node:ekr.20051006121222.20:doKey
    def doKey (self,ch,text,f):
        
        ch = ch.lower()
        
        if f is not None:
            self.exitMode(nextMode=f)
        else:
             g.trace(text)
             
        return "break"
        
        if ch == 'c':
            self.exitMode(nextMode=self.statusLine.findChangeMode)
        elif ch == 'f':
            self.exitMode(nextMode=self.statusLine.findMode)
        elif ch == 'p':
            self.exitMode(nextMode=self.statusLine.optionsMode)
        else:
            g.trace(text)
            # self.putStatusLine(text + ": ")
    
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.20:doKey
    #@-others
#@nonl
#@-node:ekr.20051006121222.16:class topInputMode (baseInputMode)
#@+node:ekr.20051006121222.21:class optionsInputMode (baseInputMode)
class optionsInputMode (baseInputMode):
    
    """An input mode to set find/change options."""
    
    #@    @+others
    #@+node:ekr.20051006121222.22:ctor
    def __init__(self,c,statusLineClass):
        
        baseInputMode.__init__(self,c,statusLineClass)
        
        self.name = "optionsMode"
        self.clear = True
        self.findFrame = g.app.findFrame
        
        self.bindings = (
            ('a','Around','wrap'),
            ('b','Body','search_body'),
            ('e','Entire',None),
            ('h','Head','search_headline'),
            ('i','Ignore','ignore_case'),
            ('n','Node','node_only'),
            ('r','Reverse','reverse'),
            ('s','Suboutline','suboutline_only'),
            ('w','Word','whole_word'),
        )
        
        signon = ["%s " % (text) for ch,text,ivar in self.bindings]
        self.signon = ''.join(signon)
    #@nonl
    #@-node:ekr.20051006121222.22:ctor
    #@+node:ekr.20051006121222.23:enterMode
    def enterMode (self,event=None):
        
        baseInputMode.enterMode(self,event)
        
        # self.findFrame.top.withdraw()
        
        self.findFrame.bringToFront()
        
        # We need a setting that will cause the row/col update not to mess with the focus.
        # Or maybe we can just disable the row-col update.
        
        ### self.disableStatusLine()
    
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.23:enterMode
    #@+node:ekr.20051006121222.24:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
    
        self.unbindAll()
        
        t.bind("<Key>",self.doNothing)
        t.bind("<Key-Escape>",self.doEsc)
        t.bind("<Return>",self.doFindChange)
        t.bind("<Linefeed>",self.doFindChange)
    
        for ch,text,ivar in self.bindings:
    
            def initBindingsCallback(event,self=self,ch=ch,text=text,ivar=ivar):
                return self.doKey(ch,text,ivar)
    
            t.bind("<Key-%s>" % ch, initBindingsCallback)
    #@nonl
    #@-node:ekr.20051006121222.24:initBindings
    #@+node:ekr.20051006121222.25:doFindChange
    def doFindChange (self,event=None):
        
        g.trace(self.name)
    
        self.exitMode(nextMode=self.statusLine.topMode)
    
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.25:doFindChange
    #@+node:ekr.20051006121222.26:doEsc
    def doEsc (self,event=None):
        
        # g.trace(self.name)
    
        self.exitMode(nextMode=self.statusLine.topMode)
    
        return "break"
    #@-node:ekr.20051006121222.26:doEsc
    #@+node:ekr.20051006121222.27:doKey
    def doKey (self,ch,text,ivar):
        
        if ivar:
            intVar = self.findFrame.dict.get(ivar)
            if intVar:
                val = intVar.get()
                g.trace(text,val)
                # Toggle the value.
                intVar.set(g.choose(val,0,1))
                
            # self.findFrame.bringToFront()
    
        return "break"
    #@nonl
    #@-node:ekr.20051006121222.27:doKey
    #@-others
#@nonl
#@-node:ekr.20051006121222.21:class optionsInputMode (baseInputMode)
#@+node:ekr.20051006121222.28:class textInputMode (baseInputMode):
class textInputMode (baseInputMode):
    
    """An input mode to set the find/change string."""
    
    #@    @+others
    #@+node:ekr.20051006121222.29:ctor
    def __init__(self,c,statusLineClass,change=False,willChange=False):
        
        baseInputMode.__init__(self,c,statusLineClass)
        
        if willChange:
            self.name = "findChangeTextMode"
            self.signon = "Replace: "
            self.clear = True
        elif change:
            self.name = "changeTextMode"
            self.signon = " By: "
            self.clear = False
        else:
            self.name = "findTextMode"
            self.signon = "Find: "
            self.clear = True
    
        self.change = change
        self.willChange = willChange
    #@-node:ekr.20051006121222.29:ctor
    #@+node:ekr.20051006121222.30:doFindChange
    def doFindChange (self,event=None):
        
        c = self.c
        
        # g.trace(self.name)
        
        s = self.getStatusLine()
        newText = s[len(self.originalLine):]
        if newText and newText[-1] == '\n':
            newText = newText [:-1]
        
        if self.change:
            self.statusLine.changeText = newText
        else:
            self.statusLine.findText = newText
    
        if self.willChange:
            nextMode = self.statusLine.changeMode
        elif self.change:
            g.trace("CHANGE",repr(self.statusLine.findText),"TO",repr(self.statusLine.changeText))
            nextMode = None
        else:
            f = g.app.findFrame
            g.trace("FIND",repr(self.statusLine.findText))
            if 0:
                f.setFindText(findText)
            else:
                f.find_text.delete("1.0","end")
                f.find_text.insert("end",self.statusLine.findText)
            f.findNextCommand(self.c)
            nextMode = None
    
        self.exitMode(nextMode=nextMode)
    
        return "break"
    #@-node:ekr.20051006121222.30:doFindChange
    #@+node:ekr.20051006121222.31:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
        
        self.unbindAll()
    
        t.bind("<Key-Return>",self.doFindChange)
        t.bind("<Key-Linefeed>",self.doFindChange)
        t.bind("<Key-Escape>",self.doEsc)
        t.bind("<Key>",self.doKey)
    #@nonl
    #@-node:ekr.20051006121222.31:initBindings
    #@+node:ekr.20051006121222.32:doEsc
    def doEsc (self,event=None):
        
        # g.trace(self.name)
    
        self.exitMode(nextMode=self.statusLine.topMode)
    
        return "break"
    #@-node:ekr.20051006121222.32:doEsc
    #@+node:ekr.20051006121222.33:doKey
    def doKey (self,event=None):
        
        if event and event.keysym == "BackSpace":
            
            # t = self.c.frame.statusText
            s = self.getStatusLine()
            
            # This won't work if we click in the frame.
            # Maybe we can disable the widget??
            if len(s) <= len(self.originalLine):
                return "break"
        
        return "continue"
    #@nonl
    #@-node:ekr.20051006121222.33:doKey
    #@-others
#@nonl
#@-node:ekr.20051006121222.28:class textInputMode (baseInputMode):
#@-others
#@nonl
#@-node:ekr.20051006121222:inputMode classes
#@+node:ekr.20051006121539:class keyHandlerClass
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
        self.commandName = None
        self.funcReturn = None # For k.simulateCommand
        self.inverseCommandsDict = {}
            # Completed in k.finishCreate, but leoCommands.getPublicCommands adds entries first.
        self.leoCallbackDict = {}
            # Completed in leoCommands.getPublicCommands.
            # Keys are *raw* functions wrapped by the leoCallback, values are emacs command names.
        self.negativeArg = False
        self.regx = g.bunch(iter=None,key=None)
        self.repeatCount = None
        self.state = g.bunch(kind=None,n=None,handler=None)
        
        #@-node:ekr.20051006092617.1:<< define externally visible ivars >>
        #@nl
        #@    << define internal ivars >>
        #@+node:ekr.20050923213858:<< define internal ivars >>
        # Previously defined bindings.
        self.bindingsDict = {}
            # Keys are Tk key names, values are g.bunch(pane,func,commandName)
        
        # Special bindings for k.fullCommand.
        self.mb_copyKey = None
        self.mb_pasteKey = None
        self.mb_cutKey = None
        
        # Keepting track of the characters in the mini-buffer.
        self.mb_history = []
        self.mb_prefix = ''
        self.mb_tabListPrefix = ''
        self.mb_tabList = []
        self.mb_tabListIndex = -1
        self.mb_prompt = ''
        
        self.func = None
        self.keysymHistory = []
        self.previous = []
        
        # For getArg...
        self.afterGetArgState = None
        self.argTabList = []
        
        # For onIdleTime
        self.idleCount = 0
        #@nonl
        #@-node:ekr.20050923213858:<< define internal ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20050920085536.2: ctor (keyHandler)
    #@+node:ekr.20050920094633:k.finishCreate & helpers
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
        
        if 0:
            addTemacsExtensions(k)
            addTemacsAbbreviations(k)
            changeKeyStrokes(k,f.bodyCtrl)
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
            
            # 'leoCallback' callback created by leoCommands.getPublicCommands.
            if f.__name__ != 'leoCallback':
                k.inverseCommandsDict [f.__name__] = name
                # g.trace('%24s = %s' % (f.__name__,name))
    #@nonl
    #@-node:ekr.20051008082929:createInverseCommandsDict
    #@-node:ekr.20050920094633:k.finishCreate & helpers
    #@-node:ekr.20050920085536.1: Birth (keyHandler)
    #@+node:ekr.20051006125633:Binding (keyHandler)
    #@+node:ekr.20050920085536.11:add_ekr_altx_commands
    def add_ekr_altx_commands (self):
    
        #@    << define dict d of abbreviations >>
        #@+node:ekr.20050920085536.12:<< define dict d of abbreviations >>
        d = {
            'again':'repeat-complex-command',
            
            # Leo searches.
            # It's not possible to use Alt-x while the find-panel is frontmost.
            # On XP you can use Alt-F4 to dismiss or Alt-tab to switch panes, then dismiss.
            # (Or I could add a 'close' button with Alt-something hotkey :-)
            'fx':   'dismiss-leo-find-panel',
            'f':    'leo-find-panel',
            'ff':   'leo-find-button',  
            'fp':   'leo-find-previous',
            'fc':   'leo-find-change-button',
            'fcf':  'leo-find-change-then-find-button',
        
            'i':    'isearch-forward', 
            'ib':   'isearch-backward',      
            'ix':   'isearch-forward-regexp',
            'irx':  'isearch-backward-regexp',
            'ixr':  'isearch-backward-regexp',
            
            'r':    'replace-string',
            'rx':   'replace-regex',
        
            's':    'search-forward',
            'sb':   'search-backward',
            'sv':   'save-file',
            
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
    
        k = self ; c = k.c
        k.abbreviationsDict = {}
    
        keys = d.keys()
        keys.sort()
        for key in keys:
            val = d.get(key)
            func = c.commandsDict.get(val)
            if func:
                # g.trace(('%-4s' % key),val)
                c.commandsDict [key] = func
                k.abbreviationsDict [key] = val
                
    #@nonl
    #@-node:ekr.20050920085536.11:add_ekr_altx_commands
    #@+node:ekr.20050920085536.16:bindKey
    def bindKey (self,pane,shortcut,callback,commandName):
    
        '''Bind the indicated shortcut (a Tk keystroke) to the callback.
        callback calls commandName (for error messages).'''
        
        k = self ; c = k.c 
    
        if not shortcut: g.trace('No shortcut for %s' % commandName)
        ## if shortcut == '<None>': return
        bunch = k.bindingsDict.get(shortcut)
        if bunch and bunch.pane == pane:
            # g.trace('Not bound',shortcut)
            if commandName != bunch.commandName:
                g.es_print('Ignoring redefinition of %s from %s to %s in %s' % (
                    shortcut,bunch.commandName,commandName,pane),color='blue')
            return
            
        # g.trace(pane,shortcut,commandName)
    
        try:
            #@        << bind callback to shortcut in pane >>
            #@+node:ekr.20051022094136:<< bind callback to shortcut in pane >>
            # Binding to 'menu' causes problems with multiple pastes in the Find Tab.
            # There should only be one binding for the minibuffer: the <Key>+ binding.
            body = c.frame.body.bodyCtrl
            log  = c.frame.log.logCtrl
            menu = c.frame.menu
            minibuffer = c.miniBufferWidget
            tree = c.frame.tree.canvas
            
            d = {
                'all':  [body,log,tree], # Probably not wise: menu
                'body': [body],
                'log':  [log],
                'menu': [menu], # Not used, and probably dubious.
                'mini': [minibuffer], # Needed so ctrl-g will work in the minibuffer!
                'text': [body,log],
                'tree': [tree],
            }
            
            if 0: # A useful trace.
                if pane and pane != 'all':
                    g.trace('%4s %20s %s' % (pane, shortcut,commandName))
            
            widgets = d.get((pane or '').lower(),[])
            
            if shortcut == '<Key>':
                # Important.  We must make this binding if the minibuffer can ever get focus.
                if self.useTextWidget:
                    widgets.append(minibuffer)
                for w in widgets:
                    w.bind(shortcut,callback,'+')
            else:
                for w in widgets:
                    w.bind(shortcut,callback)
                # Get rid of the default binding in the menu. (E.g., Alt-f)
                menu.bind(shortcut,lambda e: 'break')
            #@nonl
            #@-node:ekr.20051022094136:<< bind callback to shortcut in pane >>
            #@nl
    
            k.bindingsDict [shortcut] = g.bunch(
                pane=pane,func=callback,commandName=commandName)
    
            return True
    
        except Exception: # Could be a user error.
            if not g.app.menuWarningsGiven:
                g.es_print('Exception binding %s to %s' % (shortcut,commandName))
                g.es_exception()
                # g.printStack()
                g.app.menuWarningsGiven = True
    
            return False
    #@nonl
    #@-node:ekr.20050920085536.16:bindKey
    #@+node:ekr.20051008135051.1:bindOpenWith
    def bindOpenWith (self,shortcut,name,data):
        
        '''Make a binding for the Open With command.'''
        
        k = self ; c = k.c ;
        
        bind_shortcut, menu_shortcut = c.frame.menu.canonicalizeShortcut(shortcut)
        
        # g.trace(bind_shortcut,name,data)
    
        # The first parameter must be event, and it must default to None.
        def openWithCallback(event=None,self=self,data=data):
            __pychecker__ = '--no-argsused' # event must be present.
            return self.c.openWith(data=data)
    
        def keyCallback (event,func=openWithCallback,stroke=bind_shortcut):
            return k.masterCommand(event,func,stroke)
                
        return k.bindKey('all',bind_shortcut,keyCallback,'open-with')
    #@nonl
    #@-node:ekr.20051008135051.1:bindOpenWith
    #@+node:ekr.20051006125633.1:bindShortcut
    def bindShortcut (self,pane,shortcut,command,commandName):
        
        '''Bind one shortcut from a menu table.'''
        
        k = self ; shortcut = str(shortcut)
    
        if command.__name__ == 'leoCallback':
            # Get the function wrapped by *this* leoCallback function.
            func = k.leoCallbackDict.get(command)
            commandName = k.inverseCommandsDict.get(func.__name__)
            
            # No need for a second layer of callback.
            def keyCallback1 (event,func=command,stroke=shortcut):
                return k.masterCommand(event,func,stroke)
                
            keyCallback = keyCallback1
        else:
            def menuFuncCallback (event,command=command):
                return command(event)
    
            def keyCallback2 (event,func=menuFuncCallback,stroke=shortcut):
                return k.masterCommand(event,func,stroke)
                
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
    #@+node:ekr.20051023182326:copyBindingsToWidget & textBindingsRedirectionCallback
    def copyBindingsToWidget (self,paneOrPanes,widget):
        
        '''Copy all bindings for the given panes to widget.
        
        paneOrPanes may be a single pane name or a list of pane names.'''
    
        k = self ; d = k.bindingsDict
        keys = d.keys() ; keys.sort()
        if type(paneOrPanes) == type('abc'):
            panes = [paneOrPanes] # list(paneOrPanes) does not work.
        else:
            panes = paneOrPanes
    
        # Keys are requests, values are list of panes that match.
        matchingPanesDict = {
            'all':  ['all','body','log','mini','text','tree'],
            'body': ['all','body'],
            'log':  ['all','log'],
            # 'menu': [menu], # Not used.  Probably dubious.
            'mini': ['all','mini'],                   
            'text': ['all','body','log','text'],  # Text = body+log
            'tree': ['all','tree'],
        }
    
        matchingPanes = []
        for pane in panes:
            matches = matchingPanesDict.get(pane,[])
            for match in matches:
                if match not in matchingPanes:
                    matchingPanes.append(match)
    
        # g.trace(widget._name,'matchingPanes',matchingPanes,g.callers(3))
        
        for shortcut in keys:
            bunch = d.get(shortcut)
            if bunch.pane in matchingPanes:
                func = bunch.func
                commandName = bunch.commandName
                # g.trace('**binding',bunch.pane,shortcut,commandName,widget._name)
                
                # This callback executes the command in the given widget.
                def textBindingsRedirectionCallback(event,
                    func=func,widget=widget,commandName=commandName):
                    __pychecker__ = '--no-argsused' # widget and commandName.
                    # g.trace(commandName,func,g.app.gui.widget_name(widget))
                    func(event)
                    return 'break'
    
                widget.bind(shortcut,textBindingsRedirectionCallback)
                
        # New in 4.4a5: create the all-purpose binding.
        # This allows Leo always to return 'break' in key handlers.
        widget.bind('<Key>',k.onTextWidgetKey)
    #@nonl
    #@-node:ekr.20051023182326:copyBindingsToWidget & textBindingsRedirectionCallback
    #@+node:ekr.20051007080058:makeAllBindings
    def makeAllBindings (self):
        
        k = self ; c = k.c
        
        k.bindingsDict = {}
        k.makeHardBindings()
        k.makeSpecialBindings()
        k.makeBindingsFromCommandsDict()
        k.add_ekr_altx_commands()
        k.checkBindings()
    #@nonl
    #@-node:ekr.20051007080058:makeAllBindings
    #@+node:ekr.20050923174229.1:makeHardBindings
    def makeHardBindings (self):
        
        '''Define the bindings used in quick-command mode.'''
        
        k = self ; c = k.c
        
        self.negArgFunctions = {
            '<Alt-c>': c.editCommands.changePreviousWord,
            '<Alt-u>': c.editCommands.changePreviousWord,
            '<Alt-l>': c.editCommands.changePreviousWord,
        }
        
        # No longer used.  Very weird.
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
            'h':            c.frame.body.selectAllText,
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
    #@-node:ekr.20050923174229.1:makeHardBindings
    #@+node:ekr.20051008152134:makeSpecialBindings (also binds to 'Key')
    def makeSpecialBindings (self):
        
        '''Make the bindings and set ivars for sepcial keystrokes.'''
        
        k = self ; c = k.c ; f = c.frame
        
        # These defaults may be overridden.
        for pane,stroke,ivar,commandName,func in (
            ('all', 'Alt-x',  'fullCommandKey',  'full-command',  k.fullCommand),
            ('all', 'Ctrl-g', 'abortAllModesKey','keyboard-quit', k.keyboardQuit),
            ('all', 'Ctrl-u', 'universalArgKey', 'universal-argument', k.universalArgument),
            ('all', 'Ctrl-c', 'quickCommandKey', 'quick-command', k.quickCommand),
            # These bindings for inside the minibuffer are strange beasts.
            # They are sent directly to k.fullcommand with a special callback.
            ('mini', 'Alt-x',  None,'full-command',  k.fullCommand),
            ('mini', 'Ctrl-g', None,'keyboard-quit', k.keyboardQuit),
            ('mini', 'Ctrl-c', 'mb_copyKey', 'copy-text', f.copyText),
            ('mini', 'Ctrl-v', 'mb_pasteKey','paste-text',f.pasteText),
            ('mini', 'Ctrl-x', 'mb_cutKey',  'cut-text',  f.cutText),
        ):
            # Get the user shortcut *before* creating the callbacks.
            if 1:
                junk, bunchList = c.config.getShortcut(commandName)
                if bunchList:
                    for bunch in bunchList:
                        accel = (bunch and bunch.val)
                        shortcut, junk = c.frame.menu.canonicalizeShortcut(accel)
                        self.makeSpecialBinding(commandName,func,ivar,pane,shortcut,stroke)
                else:
                    accel = stroke
                    shortcut, junk = c.frame.menu.canonicalizeShortcut(accel)
                    self.makeSpecialBinding(commandName,func,ivar,pane,shortcut,stroke)
            else:
                junk, bunch = c.config.getShortcut(commandName)
                accel = (bunch and bunch.val) or stroke
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
        
        # g.trace(stroke,accel,shortcut,func.__name__)
        if pane == 'mini' and func != k.keyboardQuit:
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
            if 1:
                key, bunchList = c.config.getShortcut(commandName)
                for bunch in bunchList:
                    accel = bunch.val
                    if accel:
                        bind_shortcut, menu_shortcut = c.frame.menu.canonicalizeShortcut(accel)
                        k.bindShortcut(bunch.pane,bind_shortcut,command,commandName)
                        if 0:
                            if bunch: g.trace('%s %s %s' % (commandName,bunch.pane,bunch.val))
                            else:     g.trace(commandName)
            else:
                key, bunch = c.config.getShortcut(commandName)
                accel = bunch and bunch.val
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
    #@+node:ekr.20050920085536.65: masterCommand & helpers
    def masterCommand (self,event,func,stroke):
    
        '''This is the central dispatching method.
        All commands and keystrokes pass through here.'''
    
        k = self ; c = k.c
        c.startRedrawCount = c.frame.tree.redrawCount
        k.stroke = stroke # Set this global for general use.
        keysym = event and event.keysym or ''
        ch = event and event.char or ''
        k.func = func
        k.funcReturn = None # For unit testing.
        commandName = k.ultimateFuncName(func)
        special = keysym in (
            'Control_L','Alt_L','Shift_L','Control_R','Alt_R','Shift_R')
        interesting = func or stroke != '<Key>'
        
        if c.config.getBool('trace_masterCommand'):
            g.trace('stroke',stroke,'ch',repr(ch),'keysym',repr(keysym))
    
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
    
        if stroke == k.abortAllModesKey: # 'Control-g'
            k.clearState()
            k.keyboardQuit(event)
            k.endCommand(event,commandName)
            return 'break'
    
        if k.inState():
            if not special: # Don't pass these on.
                k.callStateFunction(event) # Calls end-command.
                c.setFocusHelper()
            return 'break'
    
        # if k.keystrokeFunctionDict.has_key(stroke):
            # if k.callKeystrokeFunction(event): # Calls end-command
                # return 'break'
    
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
            # g.trace('executing func',commandName)
            # forceFocus = func.__name__ != 'leoCallback'
            # if forceFocus: c.frame.bodyWantsFocus()
            val = func(event)
            k.funcReturn = k.funcReturn or val # For unit tests.
            k.endCommand(event,commandName)
            c.setFocusHelper()
            return 'break'
        else:
            val = k.handleDefaultChar(event)
            c.setFocusHelper()
            return val
    #@nonl
    #@+node:ekr.20050923172809.1:callStateFunction
    def callStateFunction (self,event):
        
        k = self ; val = None
        
        # g.trace(k.state.kind,k.state)
        
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
            # forceFocus = func.__name__ != 'leoCallback'
            k.endCommand(event,commandName)
        
        return func
    #@nonl
    #@-node:ekr.20050923174229.3:callKeystrokeFunction (not used)
    #@+node:ekr.20051026083544:handleDefaultChar
    def handleDefaultChar(self,event):
        
        c = self.c
        ch = event and event.char
        w = event and event.widget
        name = g.app.gui.widget_name(w)
       
        if name.startswith('body'):
            # For Leo 4.4a4: allow Tk defaults.
            # But this is dangerous, and should be removed.
            return c.editCommands.selfInsertCommand(event)
        elif name.startswith('head'):
            g.trace("can't happen: %s" % (name),color='red')
            c.frame.tree.updateHead(event,w)
            return 'break'
        else:
            # Let tkinter handle the event.
            # g.trace('to tk:',name,repr(ch))
            return None
    #@nonl
    #@-node:ekr.20051026083544:handleDefaultChar
    #@-node:ekr.20050920085536.65: masterCommand & helpers
    #@+node:ekr.20050920085536.41:fullCommand (alt-x) & helper
    def fullCommand (self,event,specialStroke=None,specialFunc=None):
        
        '''Handle 'full-command' (alt-x) mode.'''
    
        k = self ; c = k.c ; f = c.frame ; state = k.getState('altx')
        keysym = (event and event.keysym) or ''
        ch = (event and event.char) or ''
        # g.trace('state',state,keysym)
        if state == 0:
            k.completionFocusWidget = g.app.gui.get_focus(c.frame)
            k.setState('altx',1,handler=k.fullCommand) 
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
    
            k.endCommand(event,stroke)
            
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
        
        if event.keysym in ('Shift_L','Shift_R'): return False
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
            return True
    
        if event.keysym == 'x' and previous [1] not in ('Control_L','Control_R'):
            event.keysym = 's'
            k.setState('quick-command',1)
            c.registerCommands.setNextRegister(event)
            return True
    
        if event.keysym == 'Escape' and len(previous) > 1 and previous [1] == 'Escape':
            k.repeatComplexCommand(event)
            return True
            
        else:
            return False
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
                
        return False
    #@nonl
    #@-node:ekr.20050923183943.6:processAbbreviation
    #@-node:ekr.20050923183943.4:processKey
    #@-node:ekr.20050920085536.58:quickCommand  (ctrl-c) & helpers
    #@+node:ekr.20051001050607:endCommand
    def endCommand (self,event,commandName):
    
        '''Make sure Leo updates the widget following a command.
        
        Never changes the minibuffer label: individual commands must do that.
        '''
    
        k = self ; c = k.c
        # The command may have closed the window.
        if g.app.quitting or not hasattr(c,'currentPosition'): return
    
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
    def printBindings (self,event):
    
        '''Print all the bindings presently in effect.'''
    
        k = self ; c = k.c
        keys = k.bindingsDict.keys() ; keys.sort()
    
        c.frame.log.clearTab('Command')
        for key in keys:
            b = k.bindingsDict.get(key)
            g.es('[%s]' % b.pane,k.prettyPrintKey(key),b.commandName,tabName='Command')
    #@nonl
    #@-node:ekr.20051012201831:printBindings
    #@+node:ekr.20051014061332:printCommands
    def printCommands (self,event):
    
        '''Print all the known commands and their bindings, if any.'''
    
        k = self ; c = k.c
        
        c.frame.log.clearTab('Command')
        
        inverseBindingDict = k.computeInverseBindingDict()
        commandNames = c.commandsDict.keys() ; commandNames.sort()
    
        for commandName in commandNames:
            shortcut = inverseBindingDict.get(commandName,'')
            g.es('%s %s' % (commandName,k.prettyPrintKey(shortcut)),tabName='Command')
    #@nonl
    #@-node:ekr.20051014061332:printCommands
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
            b = k.bindingsDict.get(stroke)
            if b:
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
            event = stroke = None
            k.masterCommand(event,func,stroke)
            return k.funcReturn
        else:
            g.trace('no command for %s' % (commandName),color='red')
            raise AttributeError
    #@nonl
    #@-node:ekr.20051105155441:simulateCommand
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
            if handler: handler(event)
            c.frame.widgetWantsFocus(k.afterArgWidget)
        elif keysym == 'Tab':
            k.doTabCompletion(k.argTabList)
        elif keysym == 'BackSpace':
            k.doBackSpace(k.argTabList)
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
            
        k.clearState()
        k.resetLabel()
        
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920085536.63:keyboardQuit
    #@+node:ekr.20051015110547:registerCommand
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
                
        if verbose:
            if shortcut and ok:
                g.es_print('Registered %s bound to %s' % (
                    commandName,shortcut),color='blue')
            else:
                g.es_print('Registered %s' % (commandName), color='blue')
    #@nonl
    #@-node:ekr.20051015110547:registerCommand
    #@+node:ekr.20051025150224:onIdleTime
    def onIdleTime (self):
        
        '''Set the focus to the body pane if the focus is in limbo.
        
        We must allow dialogs and the outer window frame to retain focus.'''
        
        k = self ; c = k.c
        if g.app.quitting: return # Essential.
        
        w = g.app.gui.get_focus(c.frame)
        if w:
            # Allow clicks in enclosing window frame or in dialogs.
            name = hasattr(w,'_name') and w._name or ''
            ok = (
                name and name[0] in string.letters # A known Leo frame.
                or w == c.frame.top # The top of the Leo window
                or g.app.dialogs > 0 # A dialog.
                or isinstance(w,Tk.Text)
                or isinstance(w,Tk.Entry)
                # or isinstance(w,Tk.Button)
            )
            if not ok:
                # Not a name created by Leo.
                 g.trace(self.idleCount,name,w)
                 c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051025150224:onIdleTime
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
    #@+node:ekr.20051023132350:getLabel
    def getLabel (self,ignorePrompt=False):
        
        k = self ; w = self.widget
        
        if self.useTextWidget:
            w.update_idletasks()
            s = w and w.get('1.0','end')
            # Remove the cursed Tk newline.
            if s.endswith('\n') or s.endswith('\r'): s = s[:-1]
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
    
        if self.useTextWidget:
            if w:
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
    
        # g.trace(repr(s))
    
        if self.useTextWidget:
            if w:
                k.c.frame.minibufferWantsFocus()
                w.update_idletasks()
                w.delete('1.0','end') ; w.insert('1.0',s)
        else:
            if k.svar: k.svar.set(s)
    
        if protect:
            k.mb_prefix = s
    #@nonl
    #@-node:ekr.20051023132350.1:setLabel
    #@+node:ekr.20050920085536.36:setLabelBlue
    def setLabelBlue (self,label=None,protect=False):
        
        k = self
    
        k.widget.configure(background='lightblue')
    
        if label is not None:
            k.setLabel(label,protect)
    #@nonl
    #@-node:ekr.20050920085536.36:setLabelBlue
    #@+node:ekr.20050920085536.35:setLabelGrey
    def setLabelGrey (self,label=None):
    
        k = self
        k.widget.configure(background='lightgrey')
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
                shortcut = inverseBindingDict.get(commandName,'')
                g.es('%s %s' % (commandName,shortcut),tabName='Completion')
    
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051017212452:computeCompletionList
    #@+node:ekr.20051018070524:computeInverseBindingDict
    def computeInverseBindingDict (self):
    
        k = self ; d = {}
        
        # keys are minibuffer command names, values are shortcuts.
        for shortcut in k.bindingsDict.keys():
            b = k.bindingsDict.get(shortcut)
            d [b.commandName] = shortcut
    
        return d
    #@nonl
    #@-node:ekr.20051018070524:computeInverseBindingDict
    #@+node:ekr.20050920085536.46:doBackSpace
    # Used by getArg and fullCommand.
    
    def doBackSpace (self,defaultCompletionList):
    
        '''Cut back to previous prefix and update prefix.'''
    
        k = self
    
        if len(k.mb_tabListPrefix) > len(k.mb_prefix):
    
            k.mb_tabListPrefix = k.mb_tabListPrefix [:-1]
            k.setLabel(k.mb_tabListPrefix)
    
        k.computeCompletionList(defaultCompletionList,backspace=True)
    #@nonl
    #@-node:ekr.20050920085536.46:doBackSpace
    #@+node:ekr.20050920085536.44:doTabCompletion
    # Used by getArg and fullCommand.
    
    def doTabCompletion (self,defaultTabList):
        
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
            k.computeCompletionList(defaultTabList,backspace=False)
    
        c.frame.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920085536.44:doTabCompletion
    #@+node:ekr.20051014170754.1:getShortcutForCommand/Name
    def getShortcutForCommandName (self,commandName):
        
        k = self ; c = k.c
    
        command = c.commandsDict.get(commandName)
    
        if command:
            for key in k.bindingsDict:
                b = k.bindingsDict.get(key)
                if b.commandName == commandName:
                    return key
        
        return ''
        
    def getShortcutForCommand (self,command):
        
        k = self ; c = k.c
        
        if command:
            for key in k.bindingsDict:
                b = k.bindingsDict.get(key)
                if b.commandName == command.__name__:
                    return key
        
        return ''
    #@nonl
    #@-node:ekr.20051014170754.1:getShortcutForCommand/Name
    #@+node:ekr.20051122104219:prettyPrintKey
    def prettyPrintKey (self,key):
        
        '''Convert whatever-Z to whatever-Shift-Z'''
        
        if not key:
            return ''
            
        ch = key[-2]
    
        if ch in string.ascii_uppercase:
            return '%sShift-%s>' % (key[:-2],ch.lower())
        else:
            return key
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
            
        # Get the function wrapped by this particular leoCallback function.
        calledFunc = k.leoCallbackDict.get(func)
        if calledFunc:
            return 'leoCallback -> %s' % calledFunc.__name__ 
        else:
            return '<no leoCallback name>'
    #@nonl
    #@-node:ekr.20051010063452:ultimateFuncName
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
    #@+node:ekr.20051214113546.1:k.onTextWidgetKey & insertString
    def onTextWidgetKey (self,event):
        
        '''This is the default key handler for all text widgets.
        It should never be called for keys bound to any command.'''
    
        ch = event and event.char or ''
        w  = event and event.widget
    
        if w and ch:
            i,j = g.app.gui.getTextSelection(w)
            if i != j:
                w.delete(i,j)
            w.insert(i,ch)
    
        return 'break'
    #@nonl
    #@-node:ekr.20051214113546.1:k.onTextWidgetKey & insertString
    #@-others
#@nonl
#@-node:ekr.20051006121539:class keyHandlerClass
#@-others
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
