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
import sys
#@nonl
#@-node:ekr.20050920094258:<< imports >>
#@nl
#@<< about 'internal' bindings >>
#@+middle:ekr.20060131101205: docs
#@+node:ekr.20060130103826:<< about 'internal' bindings >>
#@@nocolor
#@+at
# 
# k.strokeFromEvent must generate exactly the same keys as used in 
# k.bindingsDict.
# 
# Here are the rules for translating key bindings (in leoSettings.leo) into 
# keys for k.bindingsDict:
# 
# 1.  The case of plain letters is significant:  a is not A.
# 
# 2.  The Shift- prefix can be applied *only* to letters.  Leo will ignore 
# (with a warning) the shift prefix applied to any other binding, e.g., 
# Ctrl-Shift-(
# 
# 3.  The case of letters prefixed by Ctrl-, Alt-, Key- or Shift- is *not* 
# significant.  Thus, the Shift- prefix is required if you want an upper-case 
# letter (with the exception of 'bare' uppercase letters.)
# 
# The following table illustrates these rules.  In each row, the first entry 
# is the key (for k.bindingsDict) and the other entries are equivalents that 
# the user may specify in leoSettings.leo:
# 
# a, Key-a, Key-A
# A, Shift-A
# Alt-a, Alt-A
# Alt-A, Alt-Shift-a, Alt-Shift-A
# Ctrl-a, Ctrl-A
# Ctrl-A, Ctrl-Shift-a, Ctrl-Shift-A
# !, Key-!,Key-exclam,exclam
# 
# This table is consistent with how Leo already works (because it is 
# consistent with Tk's key-event specifiers).  It is also, I think, the least 
# confusing set of rules.
#@-at
#@nonl
#@-node:ekr.20060130103826:<< about 'internal' bindings >>
#@-middle:ekr.20060131101205: docs
#@nl
#@<< about key dicts >>
#@+middle:ekr.20060131101205: docs
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
# k.masterBindingsDict:
#     keys are scope names: 'all','text',etc. or mode names.
#     Values are dicts:  keys are strokes, values are 
# g.Bunch(commandName,func,pane,stroke)
# 
# k.settingsNameDict:
#     Keys are lowercase settings, values are 'real' Tk key specifiers.
#     Important: this table has no inverse.
# 
# not an ivar (computed by k.computeInverseBindingDict):
# 
# inverseBindingDict
#     keys are emacs command names, values are *lists* of shortcuts.
#@-at
#@nonl
#@-node:ekr.20051010062551.1:<< about key dicts >>
#@-middle:ekr.20060131101205: docs
#@nl

class keyHandlerClass:
    
    '''A class to support emacs-style commands.'''

    #@    << define class vars >>
    #@+middle:ekr.20060131101205.1: constants and dicts
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
    #@-middle:ekr.20060131101205.1: constants and dicts
    #@nl
    #@    << define list of special names >>
    #@+middle:ekr.20060131101205.1: constants and dicts
    #@+node:ekr.20060131101205.2:<< define list of special names >>
    tkNamesList = (
        'space',
        'BackSpace','Begin','Break','Clear',
        'Delete','Down',
        'End','Escape',
        'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
        'Home','Left','Linefeed',
        'Next',
        #'PageDn','PageUp',
        'Prior',
        'Return','Right',
        'Tab','Up',
    )
    
    #@+at  
    #@nonl
    # The following are not translated, so what appears in the menu is the 
    # same as what is passed to Tk.  Case is significant.
    # 
    # Note: the Tk documentation states that not all of these may be available 
    # on all platforms.
    # 
    # Num_Lock, Pause, Scroll_Lock, Sys_Req,
    # KP_Add, KP_Decimal, KP_Divide, KP_Enter, KP_Equal,
    # KP_Multiply, KP_Separator,KP_Space, KP_Subtract, KP_Tab,
    # KP_F1,KP_F2,KP_F3,KP_F4,
    # KP_0,KP_1,KP_2,KP_3,KP_4,KP_5,KP_6,KP_7,KP_8,KP_9
    #@-at
    #@nonl
    #@-node:ekr.20060131101205.2:<< define list of special names >>
    #@-middle:ekr.20060131101205.1: constants and dicts
    #@nl
    #@    << define dict of special names >>
    #@+middle:ekr.20060131101205.1: constants and dicts
    #@+node:ekr.20031218072017.2101:<< define dict of special names >>
    # These keys settings that may be specied in leoSettings.leo.
    # Keys are lowercase, so that case is not significant *for these items only* in leoSettings.leo.
    
    
    settingsNameDict = {
        'bksp'    : 'BackSpace',
        'dnarrow' : 'Down',
        'esc'     : 'Escape',
        'ltarrow' : 'Left',
        'pageup'  : 'Prior',
        'pagedn'  : 'Next',
        'rtarrow' : 'Right',
        'uparrow' : 'Up',
    }
    
    # Add lowercase version of special keys.
    for s in tkNamesList:
        settingsNameDict [s.lower()] = s
    #@nonl
    #@-node:ekr.20031218072017.2101:<< define dict of special names >>
    #@-middle:ekr.20060131101205.1: constants and dicts
    #@nl
    #@    << define dict of Tk bind names >>
    #@+middle:ekr.20060131101205.1: constants and dicts
    #@+node:ekr.20031218072017.2100:<< define dict of Tk bind names >>
    # These are defined at http://tcl.activestate.com/man/tcl8.4/TkCmd/keysyms.htm.
    
    # Important: only the inverse dict is actually used in the new key binding scheme.
    
    # Tk may return the *values* of this dict in event.keysym fields.
    # Leo will warn if it gets a event whose keysym not in values of this table.
    
    tkBindNamesDict = {
        "!" : "exclam",
        '"' : "quotedbl",
        "#" : "numbersign",
        "$" : "dollar",
        "%" : "percent",
        "&" : "ampersand",
        "'" : "quoteright",
        "(" : "parenleft",
        ")" : "parenright",
        "*" : "asterisk",
        "+" : "plus",
        "," : "comma",
        "-" : "minus",
        "." : "period",
        "/" : "slash",
        ":" : "colon",
        ";" : "semicolon",
        "<" : "less",
        "=" : "equal",
        ">" : "greater",
        "?" : "question",
        "@" : "at",
        "[" : "bracketleft",
        "\\": "backslash",
        "]" : "bracketright",
        "^" : "asciicircum",
        "_" : "underscore",
        "`" : "quoteleft",
        "{" : "braceleft",
        "|" : "bar",
        "}" : "braceright",
        "~" : "asciitilde",
    }
    
    # No translation: these suppress a warning in k.strokeFromEvent.
    for s in tkNamesList:
        tkBindNamesDict[s] = s
        
    # Create the inverse dict.
    tkBindNamesInverseDict = {}
    for key in tkBindNamesDict.keys():
        tkBindNamesInverseDict [tkBindNamesDict.get(key)] = key
    #@nonl
    #@-node:ekr.20031218072017.2100:<< define dict of Tk bind names >>
    #@-middle:ekr.20060131101205.1: constants and dicts
    #@nl

    #@    @+others
    #@+node:ekr.20060131101205: docs
    #@-node:ekr.20060131101205: docs
    #@+node:ekr.20060131101205.1: constants and dicts
    #@-node:ekr.20060131101205.1: constants and dicts
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
            
        self.masterBindingsDict = {}
            # keys are scope names: 'all','text',etc. or mode names.
            # Values are dicts: keys are strokes, values are g.bunch(commandName,func,pane,stroke)
        
        # Special bindings for k.fullCommand.
        self.mb_copyKey = None
        self.mb_pasteKey = None
        self.mb_cutKey = None
        
        self.abortAllModesKey = None
        self.fullCommandKey = None
        self.universalArgKey = None
        
        # Keepting track of the characters in the mini-buffer.
        self.arg_completion = True
        self.mb_event = None
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
        
        # For onIdleTime
        self.idleCount = 0
        
        # For modes
        self.afterGetArgState = None
        self.argTabList = []
        self.modeBindingsDict = {}
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
        
        # g.trace('keyHandler')
       
        k.createInverseCommandsDict()
        
        if not c.miniBufferWidget:
            # Does not exist for leoSettings.leo files.
            return
    
        # Important: bindings exist even if c.showMiniBuffer is False.
        k.makeAllBindings()
    
        k.setInputState(self.unboundKeyAction)
    #@nonl
    #@+node:ekr.20051008082929:createInverseCommandsDict
    def createInverseCommandsDict (self):
        
        '''Add entries to k.inverseCommandsDict using c.commandDict.
        
        c.commandsDict:        keys are command names, values are funcions f.
        k.inverseCommandsDict: keys are f.__name__, values are minibuffer command names.
        '''
    
        k = self ; c = k.c
    
        for name in c.commandsDict.keys():
            f = c.commandsDict.get(name)
            try:
                k.inverseCommandsDict [f.__name__] = name
                # g.trace('%24s = %s' % (f.__name__,name))
                    
            except Exception:
                g.es_exception()
                g.trace(repr(name),repr(f),g.callers())
    #@nonl
    #@-node:ekr.20051008082929:createInverseCommandsDict
    #@-node:ekr.20050920094633:k.finishCreate & helpers
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
            return False
        if pane.endswith('-mode'):
            g.trace('oops: ignoring mode binding',shortcut,commandName,g.callers())
            return False
        bunchList = k.bindingsDict.get(shortcut,[])
        #@    << give warning and return if there is a serious redefinition >>
        #@+node:ekr.20060114115648:<< give warning and return if there is a serious redefinition >>
        for bunch in bunchList:
            if ( bunch and
                # (not bunch.pane.endswith('-mode') and not pane.endswith('-mode')) and
                bunch.pane != 'mini' and # Minibuffer bindings are completely separate.
                (bunch.pane == pane or pane == 'all' or bunch.pane == 'all') and
                commandName != bunch.commandName
            ):
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
                    g.trace(pane,shortcut,commandName)
        #@nonl
        #@-node:ekr.20060114110141:<< trace bindings if enabled in leoSettings.leo >>
        #@nl
        try:
            k.bindKeyToDict(pane,shortcut,callback,commandName)
            bunchList.append(
                g.bunch(pane=pane,func=callback,commandName=commandName))
            shortcut = shortcut.strip().lstrip('<').rstrip('>')
            # if shortcut.startswith('<Shift'): g.trace('ooops',shortcut,g.callers())
            k.bindingsDict [shortcut] = bunchList
            return True
        except Exception: # Could be a user error.
            if not g.app.menuWarningsGiven:
                g.es_print('Exception binding %s to %s' % (shortcut,commandName))
                g.es_exception()
                g.app.menuWarningsGiven = True
            return False
            
    bindShortcut = bindKey # For compatibility
    #@nonl
    #@-node:ekr.20050920085536.16:bindKey
    #@+node:ekr.20060130093055:bindKeyToDict
    def bindKeyToDict (self,pane,stroke,func,commandName):
        
        k = self
        d =  k.masterBindingsDict.get(pane,{})
        
        stroke = stroke.lstrip('<').rstrip('>')
        
        if 0:
            g.trace('%-4s %-18s %-40s %s' % (
                pane,repr(stroke),commandName,func and func.__name__)) # ,len(d.keys()))
    
        if d.get(stroke):
            g.es('ignoring duplicate definition of %s to %s in %s' % (
                stroke,commandName,pane), color='blue')
        else:
            d [stroke] = g.Bunch(commandName=commandName,func=func,pane=pane,stroke=stroke)
            k.masterBindingsDict [pane] = d
    #@nonl
    #@-node:ekr.20060130093055:bindKeyToDict
    #@+node:ekr.20051008135051.1:bindOpenWith
    def bindOpenWith (self,shortcut,name,data):
        
        '''Make a binding for the Open With command.'''
        
        k = self ; c = k.c
        
        # The first parameter must be event, and it must default to None.
        def openWithCallback(event=None,self=self,data=data):
            __pychecker__ = '--no-argsused' # event must be present.
            return self.c.openWith(data=data)
        
        return k.bindKey('all',shortcut,openWithCallback,'open-with')
    #@nonl
    #@-node:ekr.20051008135051.1:bindOpenWith
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
    #@+node:ekr.20051007080058:k.makeAllBindings
    def makeAllBindings (self):
        
        k = self ; c = k.c
    
        k.bindingsDict = {}
        
        k.addModeCommands() 
        k.makeBindingsFromCommandsDict()
        k.initSpecialIvars()
        c.frame.body.createBindings()
        c.frame.log.setTabBindings('Log')
        c.frame.tree.setBindings()
        c.frame.setMinibufferBindings()
        k.checkBindings()
    #@nonl
    #@-node:ekr.20051007080058:k.makeAllBindings
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
    #@+node:ekr.20051008152134:initSpecialIvars
    def initSpecialIvars (self):
        
        '''Set ivars for special keystrokes from previously-existing bindings.'''
    
        k = self ; c = k.c ; trace = c.config.getBool('trace_bindings')
        
        for ivar,commandName in (
            ('fullCommandKey',  'full-command'),
            ('abortAllModesKey','keyboard-quit'),
            ('universalArgKey', 'universal-argument'),
        ):
            junk, bunchList = c.config.getShortcut(commandName)
            bunchList = bunchList or [] ; found = False
            for pane in ('text','all'):
                for bunch in bunchList:
                    if bunch.pane == pane:
                        stroke = k.strokeFromSetting(bunch.val)
                        if trace: g.trace(commandName,stroke)
                        setattr(k,ivar,stroke) ; found = True ;break
            if not found:
                g.trace('no setting for %s' % commandName)
    #@nonl
    #@-node:ekr.20051008152134:initSpecialIvars
    #@+node:ekr.20051008134059:makeBindingsFromCommandsDict
    def makeBindingsFromCommandsDict (self):
        
        '''Add bindings for all entries in c.commandDict.'''
    
        k = self ; c = k.c
        keys = c.commandsDict.keys() ; keys.sort()
    
        for commandName in keys:
            command = c.commandsDict.get(commandName)
            key, bunchList = c.config.getShortcut(commandName)
            for bunch in bunchList:
                accel = bunch.val ; pane = bunch.pane
                if accel and not pane.endswith('-mode'):
                    shortcut = k.shortcutFromSetting(accel)
                    k.bindKey(pane,shortcut,command,commandName)
    #@nonl
    #@-node:ekr.20051008134059:makeBindingsFromCommandsDict
    #@-node:ekr.20051006125633:Binding (keyHandler)
    #@+node:ekr.20051001051355:Dispatching (keyHandler)
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
        commandName = commandName or func and func.__name__ or '<no function>'
        special = keysym in (
            'Control_L','Alt_L','Shift_L','Control_R','Alt_R','Shift_R')
        interesting = func is not None
        
        if trace and interesting:
            g.trace(
                # 'stroke: ',stroke,'state:','%x' % state,'ch:',repr(ch),'keysym:',repr(keysym),
                'w:',w and c.widget_name(w),'func:',func and func.__name__
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
            k.keyboardQuit(event)
            k.endCommand(event,commandName)
            return 'break'
            
        if special: # Don't pass these on.
            return 'break' 
    
        if 0: # *** This is now handled by k.masterKeyHandler.
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
        elif k.inState():
            return 'break' # New in 4.4b2: ignore unbound keys in a state.
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
        name = c.widget_name(w)
    
        if name.startswith('body'):
            action = k.unboundKeyAction
            if action in ('insert','overwrite'):
                c.editCommands.selfInsertCommand(event,action=action)
            else:
                pass ; g.trace('ignoring key')
            return 'break'
        elif name.startswith('head'):
            c.frame.tree.onHeadlineKey(event)
            return 'break'
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
    
        k = self ; c = k.c ; state = k.getState('full-command')
        keysym = (event and event.keysym) or ''
        ch = (event and event.char) or ''
        trace = c.config.getBool('trace_modes')
        if trace: g.trace('state',state,keysym)
        if state == 0:
            k.mb_event = event # Save the full event for later.
            k.setState('full-command',1,handler=k.fullCommand) 
            k.setLabelBlue('%s' % (k.altX_prompt),protect=True)
            # Init mb_ ivars. This prevents problems with an initial backspace.
            k.mb_prompt = k.mb_tabListPrefix = k.mb_prefix = k.altX_prompt
            k.mb_tabList = [] ; k.mb_tabListIndex = -1
            c.minibufferWantsFocus()
        elif keysym == 'Return':
            c.frame.log.deleteTab('Completion')
            k.callAltXFunction(k.mb_event)
        elif keysym == 'Tab':
            k.doTabCompletion(c.commandsDict.keys())
            c.minibufferWantsFocus()
        elif keysym == 'BackSpace':
            k.doBackSpace(c.commandsDict.keys())
            c.minibufferWantsFocus()
        elif ch not in string.printable:
            if specialStroke:
                g.trace(specialStroke)
                specialFunc()
            c.minibufferWantsFocus()
        else:
            # Clear the list, any other character besides tab indicates that a new prefix is in effect.
            k.mb_tabList = []
            k.updateLabel(event)
            k.mb_tabListPrefix = k.getLabel()
            c.minibufferWantsFocus()
            # g.trace('new prefix',k.mb_tabListPrefix)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920085536.45:callAltXFunction
    def callAltXFunction (self,event):
        
        k = self ; c = k.c ; s = k.getLabel()
        k.mb_tabList = []
        commandName = s[len(k.mb_prefix):].strip()
        func = c.commandsDict.get(commandName)
    
        if func:
            # These must be done *after* getting the command.
            k.clearState()
            k.resetLabel()
            if commandName != 'repeat-complex-command':
                k.mb_history.insert(0,commandName)
            c.widgetWantsFocusNow(event.widget) # Important, so cut-text works, e.g.
            func(event)
            k.endCommand(event,commandName)
        else:
            if 1: # Useful.
                k.doTabCompletion(c.commandsDict.keys())
            else: # Annoying.
                k.keyboardQuit(event)
                k.setLabel('Command does not exist: %s' % commandName)
                c.bodyWantsFocus()
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
    #@-node:ekr.20051001051355:Dispatching (keyHandler)
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
    
        data = [] ; n1 = 4 ; n2 = 20
        for key in keys:
            bunchList = d.get(key,[])
            for b in bunchList:
                if not brief or k.isPlainKey(key):
                    pane = g.choose(b.pane=='all','',' %s:' % (b.pane))
                    s1 = pane
                    s2 = k.prettyPrintKey(key)
                    s3 = b.commandName
                    n1 = max(n1,len(s1))
                    n2 = max(n2,len(s2))
                    data.append((s1,s2,s3),)
        # This isn't perfect in variable-width fonts.
        for s1,s2,s3 in data:
            g.es('%*s %*s %s' % (-n1,s1,-(min(12,n2)),s2,s3),tabName=tabName)
                       
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
    
        data = [] ; n1 = 4 ; n2 = 20
        for commandName in commandNames:
            dataList = inverseBindingDict.get(commandName,[('',''),])
            for z in dataList:
                pane, key = z
                s1 = pane
                s2 = k.prettyPrintKey(key)
                s3 = commandName
                n1 = max(n1,len(s1))
                n2 = max(n2,len(s2))
                data.append((s1,s2,s3),)
                    
        # This isn't perfect in variable-width fonts.
        for s1,s2,s3 in data:
            g.es('%*s %*s %s' % (-n1,s1,-(min(12,n2)),s2,s3),tabName=tabName)
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
    #@+node:ekr.20051006065121:Externally visible helpers
    #@+node:ekr.20050920085536.64:manufactureKeyPressForCommandName
    def manufactureKeyPressForCommandName (self,w,commandName):
        
        '''Implement a command by passing a keypress to Tkinter.'''
    
        k = self ; c = k.c
        
        stroke = k.getShortcutForCommandName(commandName)
        
        if stroke and w:
            # g.trace(c.widget_name(w))
            w.event_generate(stroke)
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
            if commandName.startswith('specialCallback'):
                event = None # A legacy function.
            else: # Create a dummy event as a signal.
                event = g.bunch(keysym = '',char = '',widget = None)
            k.masterCommand(event,func,stroke)
            return k.funcReturn
        else:
            g.trace('no command for %s' % (commandName),color='red')
            if g.app.unitTesting:
                raise AttributeError
            else:
                return None
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
        trace = c.config.getBool('trace_modes')
        if trace: g.trace('state',state,'keysym',keysym,'completion',completion)
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
            c.widgetWantsFocus(bodyCtrl)
            k.afterGetArgState=returnKind,returnState,handler
            k.setState('getArg',1,k.getArg)
            k.afterArgWidget = event and event.widget or c.frame.body.bodyCtrl
            if k.useTextWidget: c.minibufferWantsFocus()
        elif keysym == 'Return':
            k.arg = k.getLabel(ignorePrompt=True)
            kind,n,handler = k.afterGetArgState
            if kind: k.setState(kind,n,handler)
            c.frame.log.deleteTab('Completion')
            if handler: handler(event)
        elif keysym == 'Tab':
            k.doTabCompletion(k.argTabList,k.arg_completion)
        elif keysym == 'BackSpace':
            k.doBackSpace(k.argTabList,k.arg_completion)
            c.minibufferWantsFocus()
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
            k.endMode(event)
    
        # Complete clear the state.
        k.state.kind = None
        k.state.n = None
            
        k.clearState()
        k.resetLabel()
        
        k.setDefaultUnboundKeyAction()
        k.showStateAndMode()
        c.endEditing()
        c.bodyWantsFocus()
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
            shortcut = k.shortcutFromSetting(shortcut)
            ok = k.bindKey (pane,shortcut,func,commandName)
            if verbose and ok:
                 g.es_print('Registered %s bound to %s' % (commandName,shortcut),
                    color='blue')
        else:
            if verbose:
                g.es_print('Registered %s' % (commandName), color='blue')
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
    #@+node:ekr.20060125175103:k.minibufferWantsFocus/Now
    def minibufferWantsFocus(self):
        
        c = self.c
        if self.useTextWidget:
            c.widgetWantsFocus(c.miniBufferWidget)
        else:
            c.bodyWantsFocus()
    
    def minibufferWantsFocusNow(self):
        
        c = self.c
        if self.useTextWidget:
            c.widgetWantsFocusNow(c.miniBufferWidget)
        else:
            c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20060125175103:k.minibufferWantsFocus/Now
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
    
        k = self ; c = k.c ; w = self.widget
        if not w: return
    
        # g.trace(repr(s))
    
        if self.useTextWidget:
            w.delete('1.0','end')
            w.insert('1.0',s)
            c.masterFocusHandler() # Restore to the previously requested focus.
        else:
            if k.svar: k.svar.set(s)
    
        if protect:
            k.mb_prefix = s
    #@nonl
    #@-node:ekr.20051023132350.1:setLabel
    #@+node:ekr.20060206064635:extendLabel
    def extendLabel(self,s,select=False,protect=False):
        
        k = self ; c = k.c ; w = self.widget
        if not w: return
    
        if self.useTextWidget:
            c.widgetWantsFocusNow(w)
            w.insert('end',s)
            if select:
                i,j = k.getEditableTextRange()
                g.app.gui.setTextSelection(w,i,j,insert=j)
            if protect:
                k.protectLabel()
    #@-node:ekr.20060206064635:extendLabel
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
        
        k = self ; c = k.c ; w = self.widget
        ch = (event and event.char) or ''
        keysym = (event and event.keysym) or ''
    
        # g.trace(ch,keysym,k.stroke)
        
        if ch == '\b': # Handle backspace.
            # Don't backspace over the prompt.
            if len(s) <= k.mb_prefix:
                return 
            elif len(s) == 1: s = ''
            else: s = s [0:-1]
        elif suppressControlChars and ch not in string.printable:
            return
        elif ch and ch not in ('\n','\r'):
            if self.useTextWidget:
                c.widgetWantsFocusNow(w)
                i,j = g.app.gui.getTextSelection(w)
                if i != j:
                    w.delete(i,j)
                i = w.index('insert')
                w.insert(i,ch)
                # g.trace(k.mb_prefix)       
            else:
                # Just add the character.
                k.setLabel(k.getLabel() + ch)
    #@-node:ekr.20050920085536.38:updateLabel
    #@+node:ekr.20060210141604.1:getEditableTextRange
    def getEditableTextRange (self):
        
        k = self ; w = self.widget ; n = 0
        
        s = w.get('1.0','end')
        while s.endswith('\n') or s.endswith('\r'):
            s = s[:-1] ; n += 1
            
        i = w.index('1.%d' % len(k.mb_prefix))
        j = w.index('end -%dc' % n)
        
        # g.trace(i,j)
        return i,j
    #@-node:ekr.20060210141604.1:getEditableTextRange
    #@-node:ekr.20050924064254:Label...
    #@+node:ekr.20060129052538.1:Master event handlers (keyHandler)
    #@+node:ekr.20060127183752:masterKeyHandler & helper
    master_key_count = 0
    
    def masterKeyHandler (self,event):
        
        '''In the new binding scheme, there is only one key binding.
        
        This is the handler for that binding.'''
        
        k = self ; c = k.c
        val = self.masterKeyHandlerHelper(event)
        if val and c and c.exists: # Ignore special keys.
            c.frame.updateStatusLine()
            c.masterFocusHandler()
        return val
    #@nonl
    #@+node:ekr.20060205221734:masterKeyHandlerHelper
    def masterKeyHandlerHelper (self,event):
    
        k = self ; c = k.c
        w = event and event.widget
        w_name = c.widget_name(w)
        trace = c.config.getBool('trace_masterKeyHandler') and not g.app.unitTesting
        keysym = event.keysym or ''
        if keysym in ('Control_L','Alt_L','Shift_L','Control_R','Alt_R','Shift_R','Win_L','Win_R'):
            return None
            
        self.master_key_count += 1
        if not g.app.unitTesting and c.config.getBool('trace_gc'):
            if (self.master_key_count % 100) == 0:
                g.printGcSummary(trace=True)
    
        stroke = k.strokeFromEvent(event)
    
        # Pass keyboard-quit to k.masterCommand for macro recording.
        if k.abortAllModesKey and stroke == k.abortAllModesKey:
            return k.masterCommand(event,k.keyboardQuit,stroke,'keyboard-quit')
            
        state = k.state.kind
        if trace: g.trace(repr(stroke),'state',state)
        if k.inState():
            # First: honor the 'mini' bindings.
            d = k.masterBindingsDict.get('mini')
            b = d.get(stroke)
            if b:
                # if trace: g.trace(repr(stroke),'mini binding',b.commandName)
                # Pass this on for macro recording.
                k.masterCommand(event,b.func,stroke,b.commandName)
                c.minibufferWantsFocus()
                return 'break'
            # Second, pass keys to getArg or full-command modes if they are active.
            if state == 'getArg':
                return k.getArg(event)
            elif state == 'full-command':
                d = k.masterBindingsDict.get('mini')
                b = d.get(stroke)
                if b:
                    # Pass this on for macro recording.
                    k.masterCommand(event,b.func,stroke,b.commandName)
                    c.minibufferWantsFocus()
                    return 'break'
                else:
                    # Do the default state action.
                    k.callStateFunction(event) # Calls end-command.
                    return 'break'
            # Third, pass keys to the general mode handler.
            d =  k.masterBindingsDict.get(state)
            if d:
                # A typical state
                b = d.get(stroke)
                g.trace(d.keys())
                if b:
                    return k.generalModeHandler (event,
                        commandName=b.commandName,func=b.func,
                        modeName=state,nextMode=b.nextMode)
                else:
                    return k.modeHelp(event)
            else:
                g.trace('No state dictionary for %s' % state)
                return 'break'
        
        for key,name in (
            # Order here is similar to bindtags order.
            ('body','body'),
            ('text','head'), # Important: text bindings in head before tree bindings.
            ('tree','head'),
            ('tree','canvas'),
            ('log', 'log'),
            ('text',None), ('all',None),
        ):
            if (
                name and w_name.startswith(name) or
                key == 'text' and g.app.gui.isTextWidget(w) or
                key == 'all'
            ):
                d = k.masterBindingsDict.get(key)
                # g.trace(key,name,d and len(d.keys()))
                if d:
                    b = d.get(stroke)
                    if b:
                        if trace: g.trace('%s found %s = %s' % (key,b.stroke,b.commandName))
                        return k.masterCommand(event,b.func,b.stroke,b.commandName)
    
        if stroke.find('Alt+') > -1 or stroke.find('Ctrl+') > -1:
            if trace: g.trace('ignoring unbound special key')
            return 'break'
        else:
            if trace: g.trace(repr(stroke),'no func')
            return k.masterCommand(event,func=None,stroke=stroke,commandName=None)
    #@nonl
    #@-node:ekr.20060205221734:masterKeyHandlerHelper
    #@-node:ekr.20060127183752:masterKeyHandler & helper
    #@+node:ekr.20060129052538.2:masterClickHandler
    def masterClickHandler (self,event,func=None):
    
        k = self ; c = k.c
        if not event: return
        w = event.widget ; wname = c.widget_name(w)
    
        if c.config.getBool('trace_masterClickHandler'):
            g.trace(wname,func and func.__name__)
    
        if k.inState('full-command') and c.useTextMinibuffer and w != c.frame.miniBufferWidget:
            g.es_print('Ignoring click outside active minibuffer',color='blue')
            c.minibufferWantsFocus()
            return 'break'
    
        # Update the selection point immediately for updateStatusLine.
        if wname.startswith('body'):
            i = w.index('@%s,%s' % (event.x,event.y))
            g.app.gui.setTextSelection(w,i,i,insert=i)
            c.editCommands.setMoveCol(w,i)
            c.frame.updateStatusLine()
        elif wname.startswith('mini'):
            x = w.index('@%s,%s' % (event.x,event.y))
            i, j = k.getEditableTextRange()
            xcol = int(x.split('.')[1])
            icol = int(i.split('.')[1])
            jcol = int(j.split('.')[1])
            # g.trace(xcol,icol,jcol,icol <= xcol <= jcol)
            if icol <= xcol <= jcol:
                g.app.gui.setTextSelection(w,x,x,insert=x)
            else: return 'break'
    
        if event and func:
            # Don't even *think* of overriding this.
            val = func(event)
            c.masterFocusHandler()
            return val
        else:
            # All tree callbacks have a func, so we can't be in the tree.
            # g.trace('*'*20,'auto-deactivate tree: %s' % wname)
            c.frame.tree.OnDeactivate()
            c.widgetWantsFocusNow(w)
            return None
    
    masterClick3Handler = masterClickHandler
    masterDoubleClick3Handler = masterClickHandler
    #@nonl
    #@-node:ekr.20060129052538.2:masterClickHandler
    #@+node:ekr.20060131084938:masterDoubleClickHandler
    def masterDoubleClickHandler (self,event,func=None):
        
        k = self ; c = k.c ; w = event and event.widget
        
        if c.config.getBool('trace_masterClickHandler'):
            g.trace(c.widget_name(w),func and func.__name__)
    
        if event and func:
            # Don't event *think* of overriding this.
            return func(event)
        else:
            i = w.index("@%d,%d" % (event.x,event.y))
            g.app.gui.setTextSelection(w,i+' wordstart',i+' wordend')
            return 'break'
    #@nonl
    #@-node:ekr.20060131084938:masterDoubleClickHandler
    #@+node:ekr.20060128090219:masterMenuHandler
    def masterMenuHandler (self,stroke,func,commandName):
        
        k = self ; c = k.c ; w = c.frame.getFocus()
        
        # Create a minimal event for commands that require them.
        event = g.Bunch(char='',keysym='',widget=w)
        # g.trace(c.widget_name(w))
        
        return k.masterCommand(event,func,stroke,commandName)
    #@nonl
    #@-node:ekr.20060128090219:masterMenuHandler
    #@-node:ekr.20060129052538.1:Master event handlers (keyHandler)
    #@+node:ekr.20060115103349:Modes
    #@+node:ekr.20060117202916:badMode
    def badMode(self,modeName):
        
        k = self
    
        k.clearState()
        if modeName.endswith('-mode'): modeName = modeName[:-5]
        k.setLabelGrey('@mode %s is not defined (or is empty)' % modeName)
    #@nonl
    #@-node:ekr.20060117202916:badMode
    #@+node:ekr.20060119150624:createModeBindings
    def createModeBindings (self,modeName,d):
        
        k = self ; c = k.c
    
        for commandName in d.keys():
            func = c.commandsDict.get(commandName)
            if not func:
                g.trace('No such command: %s' % commandName) ; continue
            bunchList = d.get(commandName,[])
            for bunch in bunchList:
                stroke = bunch.val
                # Important: bunch.val is a stroke returned from k.strokeFromSetting.
                # Do not call k.strokeFromSetting again here!
                if stroke and stroke not in ('None','none',None):
                    if 0:
                        g.trace(
                            modeName,
                            '%10s' % (stroke),
                            '%20s' % (commandName),
                            bunch.nextMode)
                    d2 = k.masterBindingsDict.get(modeName,{})
                    d2 [stroke] = g.Bunch(
                        commandName=commandName,
                        func=func,
                        nextMode=bunch.nextMode,
                        stroke=stroke)
                    k.masterBindingsDict [ modeName ] = d2
    #@nonl
    #@-node:ekr.20060119150624:createModeBindings
    #@+node:ekr.20060117202916.2:endMode
    def endMode(self,event):
        
        k = self ; c = k.c
    
        c.frame.log.deleteTab('Mode')
    
        k.endCommand(event,k.stroke)
        k.inputModeName = None
        k.clearState()
        k.resetLabel()
        k.showStateAndMode() # Restores focus.
    #@nonl
    #@-node:ekr.20060117202916.2:endMode
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
    #@+node:ekr.20060104110233:generalModeHandler
    def generalModeHandler (self,event,
        commandName=None,func=None,modeName=None,nextMode=None):
        
        '''Handle a mode defined by an @mode node in leoSettings.leo.'''
    
        k = self ; c = k.c
        state = k.getState(modeName)
        trace = c.config.getBool('trace_modes')
        
        if trace: g.trace(modeName,state)
       
        if state == 0:
            self.initMode(event,modeName)
            k.inputModeName = modeName
            k.setState(modeName,1,handler=k.generalModeHandler)
            if c.config.getBool('showHelpWhenEnteringModes'):
                k.modeHelp(event)
            else:
                c.frame.log.hideTab('Mode')
            if k.useTextWidget:
                c.minibufferWantsFocus()
            else:
                c.restoreRequestedFocus()
        elif not func:
            g.trace('No func: improper key binding')
            return 'break'
        else:
            if trace: g.trace(modeName,state,commandName)
            if commandName == 'mode-help':
                func(event)
            else:
                savedModeName = k.inputModeName # Remember this: it may be cleared.
                # nextMode = bunch.nextMode
                self.endMode(event)
                if c.config.getBool('trace_doCommand'):
                    g.trace(func.__name__)
                func(event)
                if nextMode in (None,'none'):
                    # Do *not* clear k.inputModeName or the focus here.
                    # func may have put us in *another* mode.
                    pass
                elif nextMode == 'same':
                    self.reinitMode(modeName) # Re-enter this mode.
                    k.setState(modeName,1,handler=k.generalModeHandler)
                else:
                    self.initMode(event,nextMode) # Enter another mode.
    
        return 'break'
    #@nonl
    #@-node:ekr.20060104110233:generalModeHandler
    #@+node:ekr.20060117202916.1:initMode
    def initMode (self,event,modeName):
    
        k = self ; c = k.c
    
        if not modeName:
            g.trace('oops: no modeName')
            return
    
        d = g.app.config.modeCommandsDict.get('enter-'+modeName)
        if not d:
            self.badMode(modeName)
            return
        else:
            k.modeBindingsDict = d
            
        k.inputModeName = modeName
        
        if k.masterBindingsDict.get(modeName) is None:
            k.createModeBindings(modeName,d)
       
        k.setLabelBlue(modeName+': ',protect=True)
        k.showStateAndMode()
        if k.useTextWidget:
            c.minibufferWantsFocus()
        else:
            pass # Do *not* change the focus here!
    #@nonl
    #@-node:ekr.20060117202916.1:initMode
    #@+node:ekr.20060204140416:reinitMode
    def reinitMode (self,modeName):
        
        k = self ; c = k.c
    
        d = k.modeBindingsDict
        
        k.inputModeName = modeName
        k.createModeBindings(modeName,d)
        
        # Do not set the status line here.
        k.setLabelBlue(modeName+': ',protect=True)
    
        if k.useTextWidget:
            c.minibufferWantsFocus()
        else:
            pass # Do *not* change the focus here!
    #@nonl
    #@-node:ekr.20060204140416:reinitMode
    #@+node:ekr.20060104164523:modeHelp
    def modeHelp (self,event):
    
        '''The mode-help command.
        
        A possible convention would be to bind <Tab> to this command in most modes,
        by analogy with tab completion.'''
        
        k = self ; c = k.c
    
        c.endEditing()
        
        # g.trace(k.inputModeName)
        
        if k.inputModeName:
            d = g.app.config.modeCommandsDict.get('enter-'+k.inputModeName)
            k.modeHelpHelper(d)
            
        if k.useTextWidget:
            c.minibufferWantsFocus()
    
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
                    s1 = key ; s2 = k.prettyPrintKey(shortcut)
                    n = max(n,len(s1))
                    data.append((s1,s2),)
                    
        data.sort()
        
        # g.es('%s\n\n' % (k.inputModeName),tabName=tabName)
            
        # This isn't perfect in variable-width fonts.
        for s1,s2 in data:
            g.es('%*s %s' % (n,s1,s2),tabName=tabName)
    #@nonl
    #@-node:ekr.20060104125946:modeHelpHelper
    #@-node:ekr.20060104164523:modeHelp
    #@+node:ekr.20060105132013:set-xxx-State
    def setIgnoreState (self,event):
    
        self.setInputState('ignore',showState=True)
    
    def setInsertState (self,event):
    
        self.setInputState('insert',showState=True)
    
    def setOverwriteState (self,event):
    
        self.setInputState('overwrite',showState=True)
    
    #@-node:ekr.20060105132013:set-xxx-State
    #@+node:ekr.20060120200818:setInputState
    def setInputState (self,state,showState=False):
    
        k = self ; c = k.c
    
        k.unboundKeyAction = state
        if state != 'insert' or showState:
            k.showStateAndMode()
    #@nonl
    #@-node:ekr.20060120200818:setInputState
    #@+node:ekr.20060120193743:showStateAndMode
    def showStateAndMode(self):
        
        k = self ; c = k.c ; frame = c.frame
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
                
            # Restore the focus.
            c.restoreFocus()
    #@nonl
    #@-node:ekr.20060120193743:showStateAndMode
    #@-node:ekr.20060115103349:Modes
    #@+node:ekr.20051002152108.1:Shared helpers
    #@+node:ekr.20051017212452:computeCompletionList
    # Important: this code must not change mb_tabListPrefix.  Only doBackSpace should do that.
    
    def computeCompletionList (self,defaultTabList,backspace):
        
        k = self ; c = k.c ; s = k.getLabel() ; tabName = 'Completion'
        command = s [len(k.mb_prompt):]
            # s always includes prefix, so command is well defined.
    
        k.mb_tabList,common_prefix = g.itemsMatchingPrefixInList(command,defaultTabList)
        c.frame.log.clearTab(tabName)
    
        if k.mb_tabList:
            k.mb_tabListIndex = -1 # The next item will be item 0.
    
            if not backspace:
                k.setLabel(k.mb_prompt + common_prefix)
                
            inverseBindingDict = k.computeInverseBindingDict()
            data = [] ; n1 = 20; n2 = 4
            for commandName in k.mb_tabList:
                dataList = inverseBindingDict.get(commandName,[('',''),])
                for z in dataList:
                    pane,key = z
                    s1 = commandName
                    s2 = pane
                    s3 = k.prettyPrintKey(key)
                    n1 = max(n1,len(s1))
                    n2 = max(n2,len(s2))
                    data.append((s1,s2,s3),)
            for s1,s2,s3 in data:
                g.es('%*s %*s %s' % (-(min(20,n1)),s1,n2,s2,s3),tabName=tabName)
    
        c.bodyWantsFocus()
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
                    #pane = g.choose(b.pane=='all','','%s:' % (b.pane))
                    pane = '%s:' % (b.pane)
                    data = (pane,shortcut)
                    if data not in shortcutList:
                        shortcutList.append(data)
            
                d [b.commandName] = shortcutList
    
        return d
    #@nonl
    #@-node:ekr.20051018070524:computeInverseBindingDict
    #@+node:ekr.20050920085536.46:doBackSpace
    # Used by getArg and fullCommand.
    
    def doBackSpace (self,defaultCompletionList,completion=True):
    
        '''Cut back to previous prefix and update prefix.'''
    
        k = self ; c = k.c
        
        # g.trace('completion',completion)
        
        if completion:
            if len(k.mb_tabListPrefix) > len(k.mb_prefix):
                k.mb_tabListPrefix = k.mb_tabListPrefix [:-1]
                k.setLabel(k.mb_tabListPrefix)
                k.computeCompletionList(defaultCompletionList,backspace=True)
        else:
            s = k.getLabel(ignorePrompt=False)
            # g.trace(repr(s),repr(k.mb_prefix))
            if s and len(s) > len(k.mb_prefix):
                k.setLabel(s[:-1])
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
    
        c.bodyWantsFocus()
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
                        return k.tkbindingFromStroke(key)
        return ''
        
    def getShortcutForCommand (self,command):
        
        k = self ; c = k.c
        
        if command:
            for key in k.bindingsDict:
                bunchList = k.bindingsDict.get(key,[])
                for b in bunchList:
                    if b.commandName == command.__name__:
                         return k.tkbindingFromStroke(key)
        return ''
    #@nonl
    #@-node:ekr.20051014170754.1:getShortcutForCommand/Name (should return lists)
    #@+node:ekr.20060114171910:traceBinding
    def traceBinding (self,bunch,shortcut,w):
    
        k = self ; c = k.c
    
        if not c.config.getBool('trace_bindings'): return
        
        theFilter = c.config.getString('trace_bindings_filter') or ''
        if theFilter and shortcut.lower().find(theFilter.lower()) == -1: return
        
        pane_filter = c.config.getString('trace_bindings_pane_filter')
        
        if not pane_filter or pane_filter.lower() == bunch.pane:
             g.trace(bunch.pane,shortcut,bunch.commandName,w._name)
    #@nonl
    #@-node:ekr.20060114171910:traceBinding
    #@-node:ekr.20051002152108.1:Shared helpers
    #@+node:ekr.20060128092340:Shortcuts (keyHandler)
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
    
        return len(shortcut) == 1
    #@nonl
    #@-node:ekr.20060120071949:isPlainKey
    #@+node:ekr.20060128081317:shortcutFromSetting
    def shortcutFromSetting (self,setting):
    
        if not setting:
            return None
    
        s = setting.strip()
        #@    << define cmd, ctrl, alt, shift >>
        #@+node:ekr.20060201065809:<< define cmd, ctrl, alt, shift >>
        s2 = s.lower()
        
        cmd   = s2.find("cmd") >= 0     or s2.find("command") >= 0
        ctrl  = s2.find("control") >= 0 or s2.find("ctrl") >= 0
        alt   = s2.find("alt") >= 0
        shift = s2.find("shift") >= 0   or s2.find("shft") >= 0
        
        if sys.platform == "darwin":
            if ctrl and not cmd:
                cmd = True ; ctrl = False
            if alt and not ctrl:
                ctrl = True ; alt = False
        #@nonl
        #@-node:ekr.20060201065809:<< define cmd, ctrl, alt, shift >>
        #@nl
        #@    << convert minus signs to plus signs >>
        #@+node:ekr.20060128103640.1:<< convert minus signs to plus signs >>
        # Replace all minus signs by plus signs, except a trailing minus:
        if s.endswith('-'):
            s = s[:-1].replace('-','+') + '-'
        else:
            s = s.replace('-','+')
        #@nonl
        #@-node:ekr.20060128103640.1:<< convert minus signs to plus signs >>
        #@nl
        #@    << compute the last field >>
        #@+node:ekr.20060128103640.2:<< compute the last field >>
        if s.endswith('+'):
            last = '+'
        else:
            fields = s.split('+') # Don't lower this field.
            last = fields and fields[-1]
            if not last:
                if not g.app.menuWarningsGiven:
                    print "bad shortcut specifier:", s
                return None
        
        if len(last) == 1:
            if shift:
                last = last.upper()
                shift = False
            else:
                last = last.lower()
        else:
            # Translate from a made-up (or lowercase) name to 'official' Tk binding name.
            # This is a *one-way* translation, done only here.
            d = self.settingsNameDict
            last = d.get(last.lower(),last)
        #@nonl
        #@-node:ekr.20060128103640.2:<< compute the last field >>
        #@nl
        #@    << compute shortcut >>
        #@+node:ekr.20060128103640.4:<< compute shortcut >>
        table = (
            (alt, 'Alt+'),
            (ctrl,'Ctrl+'),
            (cmd, 'Cmnd+'),
            (shift,'Shift+'),
            (True,last),
        )
            
        shortcut = ''.join([val for flag,val in table if flag])
        #@nonl
        #@-node:ekr.20060128103640.4:<< compute shortcut >>
        #@nl
        return shortcut
        
    canonicalizeShortcut = shortcutFromSetting # For compatibility.
    strokeFromSetting    = shortcutFromSetting
    #@nonl
    #@-node:ekr.20060128081317:shortcutFromSetting
    #@+node:ekr.20060126163152.2:k.strokeFromEvent
    # The keys to k.bindingsDict must be consistent with what this method returns.
    # See 'about internal bindings' for details.
     
    def strokeFromEvent (self,event):
        
        c = self.c ; k = c.k
        if event is None: return ''
        state = event.state or 0
        keysym = event.keysym or ''
        ch = event.char
        result = []
        shift = (state & 1) == 1 # Not used for alpha chars.
        caps  = (state & 2) == 2 # Not used at all.
        ctrl  = (state & 4) == 4
        # Linux uses, 8 and 0x80, XP uses 0x20000.
        alt   = (state & 0x20000) == 0x20000 or (state & 8) == 8 or (state & 0x80) == 0x80
        plain = len(keysym) == 1 # E.g., for ctrl-v the keysym is 'v' but ch is empty.
        
        # g.trace('ch',repr(ch),'keysym',repr(keysym),'state: %x' % state)
        
        # The big aha: we can ignore the shift state.
        if plain:
            if shift and ch.isalpha() and ch.islower():
                g.trace('oops: inconsistent shift state. shift: %s, ch: %s' % (shift,ch))
            ch = keysym
            shift = False
        else:
            ch2 = k.tkBindNamesInverseDict.get(keysym)
            if ch2:
                ch = ch2
                if len(ch) == 1: shift = False
            else:
                # Just use the unknown keysym.
                g.trace('*'*30,'unknown keysym',repr(keysym))
        
        if alt: result.append('Alt+')
        if ctrl: result.append('Ctrl+')
        if shift: result.append('Shift+')
        result.append(ch)
        result = ''.join(result)
        # g.trace('state',state,'keysym',keysym,'result',repr(result))
        return result
    #@nonl
    #@-node:ekr.20060126163152.2:k.strokeFromEvent
    #@+node:ekr.20060131075440:k.tkbindingFromStroke
    def tkbindingFromStroke (self,stroke):
        
        '''Convert a stroke (key to k.bindingsDict) to an actual Tk binding.
        
        Used only to simulate keystrokes.'''
        
        stroke = stroke.lstrip('<').rstrip('>')
        
        for a,b in (
            ('Alt+','Alt-'),
            ('Ctrl+','Control-'),
            ('Shift+','Shift-'),
        ):
            stroke = stroke.replace(a,b)
            
        return '<%s>' % stroke
    #@nonl
    #@-node:ekr.20060131075440:k.tkbindingFromStroke
    #@+node:ekr.20060201083154:k.prettyPrintKey
    def prettyPrintKey (self,stroke):
        
        s = stroke and stroke.strip().lstrip('<').rstrip('>')
        if not s: return ''
    
        shift = s.find("shift") >= 0 or s.find("shft") >= 0
        
        # Replace all minus signs by plus signs, except a trailing minus:
        if s.endswith('-'): s = s[:-1].replace('-','+') + '-'
        else:               s = s.replace('-','+')
        fields = s.split('+')
        last = fields and fields[-1]
    
        if last and len(last) == 1:
            prev = s[:-1]
            if last.isalpha():
                if last.isupper():
                    if not shift:
                        s = prev + 'Shift+' + last
                elif last.islower():
                    if not prev:
                        s = 'Key+' + last.upper()
                    else:
                        s = prev + last.upper()
    
        return '<%s>' % s
    #@nonl
    #@-node:ekr.20060201083154:k.prettyPrintKey
    #@-node:ekr.20060128092340:Shortcuts (keyHandler)
    #@+node:ekr.20050923172809:States
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
    #@-node:ekr.20050923172809:States
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
    #@-others
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
