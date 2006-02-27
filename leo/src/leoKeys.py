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

import compiler
import inspect
import parser
import re
import string
import sys
import types
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

#@+others
#@+node:ekr.20060131101205: docs
#@-node:ekr.20060131101205: docs
#@+node:ekr.20051126123249:class autoCompleterClass
class autoCompleterClass:
    
    '''A class that inserts autocompleted and calltip text in text widgets.
    This class shows alternatives in the tabbed log pane.
    
    The keyHandler class contains hooks to support these characters:
    invoke-autocompleter-character (default binding is '.')
    invoke-calltips-character (default binding is '(')
    '''

    #@    @+others
    #@+node:ekr.20051126123759.1: ctor (autocompleter)
    def __init__ (self,k):
        
        self.c = c = k.c
        self.k = k
        self.allClassesDict = {} # Will be completed after more classes exist.
        self.attrDictDict = {}  # Keys are languages (strings); values are anonymous attrDicts.
            # attrDicts: keys are strings; values are list of strings (attributes).
        self.calltips = {} # Keys are language, values are dicts: keys are ids, values are signatures.
        self.classScanner = self.classScannerClass(c)
        self.forgivingParser = self.forgivingParserClass(c)
        self.globalPythonFunctionsDict = {}
        self.language = None
        self.leadinWord = None
        self.membersList = None
        self.objectDict = {} # Created on first use of the autocompleter.
        self.selection = None # The selection range on entry to autocompleter or calltips.
        self.selectedText = None # The selected text on entry to autocompleter or calltips.
        self.selfClassName = None
        self.selfObjectsDict = {} # Keys are classNames, values are real proxy objects.
        self.selfTnodesDict = {} # Keys are tnodes, values are real proxy objects.
        self.prefix = None
        self.prevObjects = []
        self.tabList = []
        self.tabListIndex = -1
        self.tabName = None # The name of the main completion tab.
        self.object = None # The previously found object, for . chaining.
        self.trace = c.config.getBool('trace_autocompleter')
        self.verbose = False # True: print all members.
        self.watchwords = {} # Keys are ids, values are lists of ids that can follow a id dot.
        self.widget = None # The widget that should get focus after autocomplete is done.
    
    #@+node:ekr.20060223085549:defineClassesDict
    def defineClassesDict (self):
        
        self.allClassesDict = {}
        
        # gc may not exist.
        try: import gc
        except ImportError: return
    
        for z in gc.get_objects():
            t = type(z)
            if t == types.ClassType:
                name = z.__name__
            elif t == types.InstanceType:
                name = z.__class__.__name__
            elif repr(t).startswith('<class'): # A wretched kludge.
                name = z.__class__.__name__
            elif t == types.TypeType:
                name = z.__name__
            else:
                name = None
            if name:
                # if name == 'position': g.trace(t,z)
                self.allClassesDict [name] = z
            
        # g.printList(self.allClassesDict.keys(),tag='Classes',sort=True)
        # g.trace(len(self.allClassesDict.keys()))
        # g.trace('position:',self.allClassesDict.get('position'))
    #@-node:ekr.20060223085549:defineClassesDict
    #@+node:ekr.20060219171914:defineObjectDict
    def defineObjectDict (self):
        
        c = self.c ; k = c.k ; p = c.currentPosition()
    
        table = [
            # Python globals...
            (['aList','bList'],     'python','list'),
            (['aString'],           'object','aString'),    # An actual string object.
            (['c','old_c','new_c'], 'object',c),            # 'leoCommands','Commands'),
            (['d','d1','d2'],       'python','dict'),
            (['f'],                 'object',c.frame), # 'leoTkinterFrame','leoTkinterFrame'),
            (['g'],                 'object',g),       # 'leoGlobals',None),
            (['p','p1','p2'],       'object',p),       # 'leoNodes','position'),         
            (['s','s1','s2','ch'],  'object','aString'),
            (['string'],            'object',string),     # Python's string module.
            (['t','t1','t2'],       'object',p.v.t),   # 'leoNodes','tnode'),  
            (['v','v1','v2'],       'object',p.v),     # 'leoNodes','vnode'),
            (['w','widget'],        'Tkinter','Text'),
        ]
        
        if 0: # Not useful at this point.
            for key in __builtins__.keys():
                obj = __builtins__.get(key)
                if obj in (True,False,None): continue
                data = [key],'object',obj
                table.append(data)
        
        d = {'dict':{},'int':1,'list':[],'string':''}
    
        for idList,kind,nameOrObject in table:
            if kind == 'object':
                # Works, but hard to generalize for settings.
                obj = nameOrObject
            elif kind == 'python':
                className = nameOrObject
                o = d.get(className)
                obj = o is not None and o.__class__
            else:
                module = g.importModule (kind,verbose=True)
                if not module:
                    g.trace('Can not import ',nameOrObject)
                    continue
                self.appendToKnownObjects(module)
                if nameOrObject:
                    className = nameOrObject
                    obj = hasattr(module,className) and getattr(module,className) or None
                    if not obj:
                        g.trace('%s module has no class %s' % (kind,nameOrObject))
                    else:
                        self.appendToKnownObjects(getattr(module,className))
                else:
                    obj = module
            if not obj:
                g.trace('bad object',obj)
                continue
            for z in idList:
                self.objectDict[z]=obj
                # g.trace(obj)
    #@nonl
    #@-node:ekr.20060219171914:defineObjectDict
    #@-node:ekr.20051126123759.1: ctor (autocompleter)
    #@+node:ekr.20060219103046:Top level
    #@+node:ekr.20051126122952.1:autoComplete
    def autoComplete (self,event=None,force=False):
        
        '''An event handler called from k.masterKeyHanderlerHelper.'''
    
        c = self.c ; k = self.k
        w = event and event.widget or c.get_focus()
    
        # First, handle the invocation character as usual.
        k.masterCommand(event,func=None,stroke=None,commandName=None)
        
        # Don't allow autocompletion in headlines.
        if not c.widget_name(w).startswith('head'):
            self.language = g.scanForAtLanguage(c,c.currentPosition())
            if w and self.language == 'python' and (k.enable_autocompleter or force):
                self.start(event=event,w=w)
    
        return 'break'
    #@nonl
    #@-node:ekr.20051126122952.1:autoComplete
    #@+node:ekr.20060219103822:autoCompleteForce
    def autoCompleteForce (self,event=None):
        
        return self.autoComplete(event,force=True)
    #@nonl
    #@-node:ekr.20060219103822:autoCompleteForce
    #@+node:ekr.20060219170612:enable/disableAutocompleter/Calltips
    def disableAutocompleter (self,event=None):
        self.k.enable_autocompleter = False
        
    def disableCalltips (self,event=None):
        self.k.enable_calltips = False
        
    def enableAutocompleter (self,event=None):
        self.k.enable_autocompleter = True
        
    def enableCalltips (self,event=None):
        self.k.enable_calltips = True
    #@nonl
    #@-node:ekr.20060219170612:enable/disableAutocompleter/Calltips
    #@+node:ekr.20060219103046.1:showCalltips
    def showCalltips (self,event=None,force=False):
        
        c = self.c ; k = c.k
        
        w = event and event.widget or c.get_focus()
        
        # Insert the calltip if possible, but not in headlines.
        if (k.enable_calltips or force) and not c.widget_name(w).startswith('head'):
            self.widget = w
            self.prefix = ''
            self.selection = g.app.gui.getTextSelection(w)
            self.selectedText = g.app.gui.getSelectedText(w)
            # self.getLeadinWord(w)
            self.leadinWord = self.findCalltipWord(w)
            self.object = None
            self.membersList = None
            self.calltip()
        else:
            # Just insert the invocation character as usual.
            k.masterCommand(event,func=None,stroke=None,commandName=None)
            
        return 'break'
    #@nonl
    #@-node:ekr.20060219103046.1:showCalltips
    #@+node:ekr.20060219170043:showCalltipsForce
    def showCalltipsForce (self,event=None):
        
        return self.showCalltips(event,force=True)
    #@nonl
    #@-node:ekr.20060219170043:showCalltipsForce
    #@+node:ekr.20051126124705:autoCompleterStateHandler
    def autoCompleterStateHandler (self,event):
        
        c = self.c ; k = self.k
        tag = 'auto-complete' ; state = k.getState(tag)
        keysym = event and event.keysym
        ch = event and event.char or ''
        trace = self.trace and not g.app.unitTesting
        if trace: g.trace(repr(ch),repr(keysym),state)
    
        if state == 0:
            c.frame.log.clearTab(self.tabName)
            self.computeCompletionList()
            k.setState(tag,1,handler=self.autoCompleterStateHandler) 
        elif keysym in ('space','Return'):
            self.finish()
        elif keysym == 'Escape':
            self.abort()
        elif keysym == 'Tab':
            self.doTabCompletion()
        elif keysym == 'BackSpace':
            self.doBackSpace()
        elif keysym == 'period':
            self.chain()
        elif keysym == 'question':
            self.info()
        elif keysym == 'exclam':
            # Toggle between verbose and brief listing.
            self.verbose = not self.verbose
            if type(self.object) == types.DictType:
                self.membersList = self.object.keys()
            elif type(self.object) in (types.ListType,types.TupleType):
                self.membersList = self.object
            self.computeCompletionList(verbose=self.verbose)
        elif ch and ch in string.printable:
            self.insertNormalChar(ch,keysym)
        else:
            if trace: g.trace('ignore',repr(ch))
            return 'do-standard-keys'
    #@nonl
    #@-node:ekr.20051126124705:autoCompleterStateHandler
    #@-node:ekr.20060219103046:Top level
    #@+node:ekr.20060216160332.2:Helpers
    #@+node:ekr.20051127105431:abort & exit
    def abort (self):
        
        k = self.k
        k.keyboardQuit(event=None)
        self.exit(restore=True)
    
    def exit (self,restore=False): # Called from keyboard-quit.
        
        c = self.c ; w = self.widget
        for name in (self.tabName,'Modules','Info'):
            c.frame.log.deleteTab(name)
        c.widgetWantsFocusNow(w)
        i,j = g.app.gui.getTextSelection(w)
        if restore:
            w.delete(i,j)
            w.insert(i,self.selectedText)
        g.app.gui.setTextSelection(w,j,j,insert=j)
        
        self.clear()
        self.object = None
    #@nonl
    #@-node:ekr.20051127105431:abort & exit
    #@+node:ekr.20060219180034:append/begin/popTabName
    def appendTabName (self,word):
        
        self.setTabName(self.tabName + word + '.')
    
    def beginTabName (self,word):
    
        # g.trace(word,g.callers())
        if word == 'self' and self.selfClassName:
            word = '%s (%s)' % (word,self.selfClassName)
        self.setTabName('AutoComplete ' + word + '.')
        
    def clearTabName (self):
        
        self.setTabName('AutoComplete ')
        
    def popTabName (self):
        
        s = self.tabName
        i = s.rfind('.',0,-1)
        if i > -1:
            self.setTabName(s[0:i])
        
    # Underscores are not valid in Pmw tab names!
    def setTabName (self,s):
    
        c = self.c
        if self.tabName:
            c.frame.log.deleteTab(self.tabName)
        self.tabName = s.replace('_','') or ''
        c.frame.log.clearTab(self.tabName)
    #@nonl
    #@-node:ekr.20060219180034:append/begin/popTabName
    #@+node:ekr.20060221131304:appendToKnownObjects
    def appendToKnownObjects (self,obj):
        
        if 0:
            if type(obj) in (types.InstanceType,types.ModuleType,types):
                if hasattr(obj,'__name__'):
                    self.knownObjects[obj.__name__] = obj
                    # g.trace('adding',obj.__name__)
    #@nonl
    #@-node:ekr.20060221131304:appendToKnownObjects
    #@+node:ekr.20060220110302:calltip
    def calltip (self,obj=None):
        
        c = self.c ; w = self.widget
        isStringMethod = False ; s = None
        # g.trace(self.leadinWord,obj)
    
        if self.leadinWord and (not obj or type(obj) == types.BuiltinFunctionType):
            #@        << try to set s from a Python global function >>
            #@+node:ekr.20060224103829:<< try to set s from a Python global function >>
            # The first line of the docstring is good enough.
            f = __builtins__.get(self.leadinWord)
            doc = f and f.__doc__
            if doc:
                s = g.splitLines(doc)
                s = args = s and s[0] or ''
                i = s.find('(')
                if i > -1: s = s[i:]
                s = s and s.strip() or ''
            #@nonl
            #@-node:ekr.20060224103829:<< try to set s from a Python global function >>
            #@nl
    
        if not s:
            #@        << get s using inspect >>
            #@+node:ekr.20060224103829.1:<< get s using inspect >>
            isStringMethod = self.prevObjects and type(self.prevObjects[-1]) == types.StringType
            
            # g.trace(self.prevObjects)
            
            if isStringMethod:
                # A hack. String functions are builtins, and getargspec doesn't handle them.
                # Get the corresponding string function instead, and remove the s arg later.
                obj = getattr(string,obj.__name__)
            
            try:
                s1,s2,s3,s4 = inspect.getargspec(obj)
            except:
                # g.es('inspect failed:',repr(obj))
                self.extendSelection('(')
                self.finish()
                return # Not a function.  Just '('.
            
            s = args = inspect.formatargspec(s1,s2,s3,s4)
            #@nonl
            #@-node:ekr.20060224103829.1:<< get s using inspect >>
            #@nl
            
        #@    << remove 'self' from s, but not from args >>
        #@+node:ekr.20060224103829.2:<< remove 'self' from s, but not from args >>
        if g.match(s,1,'self,'):
            s = s[0] + s[6:].strip()
        elif g.match_word(s,1,'self'):
            s = s[0] + s[5:].strip()
        #@nonl
        #@-node:ekr.20060224103829.2:<< remove 'self' from s, but not from args >>
        #@nl
        if isStringMethod:
            #@        << remove 's' from s *and* args >>
            #@+node:ekr.20060224103829.3:<< remove 's' from s *and* args >>
            if g.match(s,1,'s,'):
                s = s[0] + s[3:]
                args = args[0] + args[3:]
            elif g.match_word(s,1,'s'):
                s = s[0] + s[2:]
                args = args[0] + args[2:]
            #@nonl
            #@-node:ekr.20060224103829.3:<< remove 's' from s *and* args >>
            #@nl
    
        s = s.rstrip(')') # Convenient.
        #@    << insert the text and set j1 and j2 >>
        #@+node:ekr.20060224103829.4:<< insert the text and set j1 and j2 >>
        if g.app.gui.hasSelection(w):
            i,j = g.app.gui.getSelectionRange(w)
        else:
            i = j = g.app.gui.getInsertPoint(w)
        w.insert(j,s)
        
        if 1:
            j1 = w.index('%s + 1c' % j)
            j2 = w.index('%s + %sc' % (j,len(s)))
        else:
            j1 = j2 = w.index('%s + 2c' % j)
        #@nonl
        #@-node:ekr.20060224103829.4:<< insert the text and set j1 and j2 >>
        #@nl
    
        # End autocompletion mode, restoring the selection.
        self.finish()
        c.widgetWantsFocusNow(w)
        g.app.gui.setSelectionRange(w,j1,j2,insert=j2)
        #@    << put the status line >>
        #@+node:ekr.20060224103829.5:<< put the status line >>
        c.frame.clearStatusLine()
        if obj:
            name = hasattr(obj,'__name__') and obj.__name__ or repr(obj)
        else:
            name = self.leadinWord
        c.frame.putStatusLine('%s %s' % (name,args))
        #@nonl
        #@-node:ekr.20060224103829.5:<< put the status line >>
        #@nl
    #@-node:ekr.20060220110302:calltip
    #@+node:ekr.20060220085402:chain
    def chain (self):
        
        c = self.c ; w = self.widget
        word = g.app.gui.getSelectedText(w)
        old_obj = self.object
    
        if word and old_obj and type(old_obj) == type([]) and old_obj == sys.modules:
            obj = old_obj.get(word)
            if obj:
                self.object = obj
                self.clearTabName()
        elif word and old_obj and self.hasAttr(old_obj,word):
            self.push(old_obj)
            self.object = obj = self.getAttr(old_obj,word)
        else: obj = None
    
        if obj:
            self.appendToKnownObjects(obj)
            self.leadinWord = word
            self.membersList = self.getMembersList(obj)
            self.appendTabName(word)
            self.extendSelection('.')
            i = g.app.gui.getInsertPoint(w)
            g.app.gui.setTextSelection(w,i,i,insert=i)
            # g.trace('chaining to',word,self.object)
            # Similar to start logic.
            self.prefix = ''
            self.selection = g.app.gui.getTextSelection(w)
            self.selectedText = g.app.gui.getSelectedText(w)
            if self.membersList:
                # self.autoCompleterStateHandler(event=None)
                self.computeCompletionList()
                return
        self.extendSelection('.')
        self.finish()
    #@-node:ekr.20060220085402:chain
    #@+node:ekr.20051126123149:computeCompletionList
    def computeCompletionList (self,verbose=False):
        
        c = self.c ; gui = g.app.gui ; w = self.widget
        c.widgetWantsFocus(w)
        s = gui.getSelectedText(w)
        self.tabList,common_prefix = g.itemsMatchingPrefixInList(
            s,self.membersList,matchEmptyPrefix=True)
    
        if not common_prefix:
            if verbose or len(self.tabList) < 25:
                self.tabList,common_prefix = g.itemsMatchingPrefixInList(
                    s,self.membersList,matchEmptyPrefix=True)
            else: # Show the possible starting letters.
                d = {}
                for z in self.tabList:
                    ch = z and z[0] or ''
                    if ch:
                        n = d.get(ch,0)
                        d[ch] = n + 1
                aList = [ch+'...%d' % (d.get(ch)) for ch in d.keys()] ; aList.sort()
                self.tabList = aList
           
        c.frame.log.clearTab(self.tabName) # Creates the tab if necessary.
        if self.tabList:
            self.tabListIndex = -1 # The next item will be item 0.
            self.setSelection(common_prefix)
        for name in self.tabList:
            g.es('%s' % (name),tabName=self.tabName)
    #@nonl
    #@-node:ekr.20051126123149:computeCompletionList
    #@+node:ekr.20051126131103:doBackSpace (autocompleter)
    def doBackSpace (self):
    
        '''Cut back to previous prefix.'''
        
        # g.trace(self.prefix,self.object,self.prevObjects)
        
        if self.prefix:
            self.prefix = self.prefix[:-1]
            self.setSelection(self.prefix)
            self.computeCompletionList()
        elif self.object:
            if self.prevObjects:
                obj = self.pop()
            else:
                obj = self.object
            # g.trace(self.object,obj)
            w = self.widget
            i,j = g.app.gui.getTextSelection(w)
            ch = w.get(i+'-1c')
            # g.trace(ch)
            if ch == '.':
                self.object = obj
                w.delete(i+'-1c')
                i = w.index(i+'-1c wordstart')
                j = w.index(i+' wordend')
                word = w.get(i,j)
                g.app.gui.setSelectionRange(w,i,j,insert=j)
                self.prefix = word
                self.popTabName()
                self.membersList = self.getMembersList(obj)
                # g.trace(len(self.membersList))
                if self.membersList:
                    self.computeCompletionList()
                else:
                    self.abort()
            else:
                self.abort() # should not happen.
        else:
            self.abort()
    #@nonl
    #@-node:ekr.20051126131103:doBackSpace (autocompleter)
    #@+node:ekr.20051126123249.1:doTabCompletion
    def doTabCompletion (self):
        
        '''Handle tab completion when the user hits a tab.'''
        
        c = self.c ; gui = g.app.gui ; w = self.widget
        s = gui.getSelectedText(w)
    
        if s.startswith(self.prefix) and self.tabList:
            # g.trace('cycle','prefix',repr(self.prefix),len(self.tabList),repr(s))
            # Set the label to the next item on the tab list.
            self.tabListIndex +=1
            if self.tabListIndex >= len(self.tabList):
               self.tabListIndex = 0
            self.setSelection(self.tabList[self.tabListIndex])
        else:
            self.computeCompletionList()
    
        c.widgetWantsFocusNow(w)
    #@nonl
    #@-node:ekr.20051126123249.1:doTabCompletion
    #@+node:ekr.20051127065601:extendSelection
    def extendSelection (self,s):
        
        c = self.c ; w = self.widget
        c.widgetWantsFocusNow(w)
        
        if g.app.gui.hasSelection(w):
            i,j = g.app.gui.getSelectionRange(w)
        else:
            i = j = g.app.gui.getInsertPoint(w)
        
        w.insert(j,s)
        j = w.index('%s + 1c' % (j))
        g.app.gui.setSelectionRange(w,i,j,insert=j)
    #@nonl
    #@-node:ekr.20051127065601:extendSelection
    #@+node:ekr.20060221104137:findAnchor
    def findAnchor (self,w):
        
        i = g.app.gui.getInsertPoint(w)
        
        while w.get(i + '-1c') == '.' and w.compare(i,'>','1.0'):
            i = w.index(i + '-2c wordstart')
    
        j = w.index(i+' wordend')
        word = w.get(i,j)
        
        if word == '.': word = None
        
        # g.trace(i,j,repr(word),w.get(j))
        return j,word
    #@nonl
    #@-node:ekr.20060221104137:findAnchor
    #@+node:ekr.20060224094501:findCalltipWord
    def findCalltipWord (self,w):
        
        i = g.app.gui.getInsertPoint(w)
        
        if w.compare(i,'>','1.0'):
            return w.get(i+'-1c wordstart',i+'-1c wordstart wordend')
        else:
            return ''
    #@nonl
    #@-node:ekr.20060224094501:findCalltipWord
    #@+node:ekr.20051127105102:finish
    def finish (self):
        
        c = self.c ; k = self.k
        
        k.keyboardQuit(event=None)
        
        for name in (self.tabName,'Modules','Info'):
            c.frame.log.deleteTab(name)
            
        c.frame.body.onBodyChanged('Typing')
        self.clear()
        self.object = None
    #@nonl
    #@-node:ekr.20051127105102:finish
    #@+node:ekr.20060223081914:getAttr and hasAttr
    # The values of self.attrDictDic are anonymous attrDict's.
    # attrDicts: keys are strings, values are lists of strings.
    
    def getAttr (self,obj,attr):
        
        '''Simulate getattr function, regardless of langauge.'''
        
        if self.language == 'python':
            return getattr(obj,attr)
        else:
            d = self.attrDictDict.get(self.language)
            aList = d.get(obj,[])
            return attr in aList and attr
    
    def hasAttr (self,obj,attr):
        
        '''Simulate hasattr function, regardless of langauge.'''
    
        if self.language == 'python':
            return hasattr(obj,attr)
        else:
            d = self.attrDictDict.get(self.language)
            aList = d.get(obj,[])
            return attr in aList
    #@nonl
    #@-node:ekr.20060223081914:getAttr and hasAttr
    #@+node:ekr.20060219111416:getLeadinWord
    def getLeadinWord (self,w):
        
        self.verbose = False # User must explicitly ask for verbose.
        self.leadinWord = None
        start = g.app.gui.getInsertPoint(w)
        start = w.index(start+'-1c')
        i,word = self.findAnchor(w)
        self.setObjectAndMembersList(word)
        
        # g.trace(word,self.object,len(self.membersList))
    
        if not word:
            return False
        elif not self.object:
            self.membersList = []
            return False
        else:
            self.beginTabName(word)
            while w.compare(i,'<',start):
                if w.get(i) != '.':
                    g.trace('oops: %s' % (repr(w.get(i))))
                    return False
                i = w.index(i+'+1c')
                j = w.index(i+' wordend')
                word = w.get(i,j)
                # g.trace(word,i,j,start)
                self.setObjectAndMembersList(word)
                if not self.object:
                    # g.trace('unknown',word)
                    return False
                self.appendTabName(word)
                i = j
            self.leadinWord = word
            return True
        
    #@nonl
    #@-node:ekr.20060219111416:getLeadinWord
    #@+node:ekr.20060219174642:getMembersList
    def getMembersList (self,obj):
        
        '''Return a list of possible autocompletions for self.leadinWord.'''
    
        if obj:
            aList = inspect.getmembers(obj)
            members = ['%s:%s' % (a,g.prettyPrintType(b))
                for a,b in aList if not a.startswith('__')]
            members.sort()
            return members
        else:
            return []
    #@nonl
    #@-node:ekr.20060219174642:getMembersList
    #@+node:ekr.20060220132026:info
    def info (self):
        
        c = self.c ; doc = None ; obj = self.object ; w = self.widget
    
        word = g.app.gui.getSelectedText(w)
        
        if not word:
            # Never gets called, but __builtin__.f will work.
            word = self.findCalltipWord(w)
            if word:
                # Try to get the docstring for the Python global.
                f = __builtins__.get(self.leadinWord)
                doc = f and f.__doc__
    
        if not doc:
            if not self.hasAttr(obj,word): return
            obj = self.getAttr(obj,word)
            doc = inspect.getdoc(obj)
    
        if doc:
            c.frame.log.clearTab('Info',wrap='word')
            g.es(doc,tabName='Info')
    #@nonl
    #@-node:ekr.20060220132026:info
    #@+node:ekr.20060220104902:insertNormalChar
    def insertNormalChar (self,ch,keysym):
        
        k = self.k ; w = self.widget
    
        if ch in (string.letters + string.digits + '_' ):
            # Look ahead to see if the character completes any item.
            s = g.app.gui.getSelectedText(w) + ch
            tabList,common_prefix = g.itemsMatchingPrefixInList(
                s,self.membersList,matchEmptyPrefix=True)
            if tabList:
                # Add the character.
                self.tabList = tabList
                self.extendSelection(ch)
                s = g.app.gui.getSelectedText(w)
                if s.startswith(self.prefix):
                    self.prefix = self.prefix + ch
                self.computeCompletionList()
        else:
            word = g.app.gui.getSelectedText(w)
            if keysym == 'parenleft':
                # Similar to chain logic.
                obj = self.object
                # g.trace(obj,word,self.hasAttr(obj,word))
                if self.hasAttr(obj,word):
                    obj = self.getAttr(obj,word)
                    self.push(self.object)
                    self.object = obj
                    self.leadinWord = word
                    self.membersList = self.getMembersList(obj)
                    if k.enable_calltips:
                        # This calls self.finish if the '(' is valid.
                        self.calltip(obj)
                        return
            self.extendSelection(ch)
            self.finish()
    #@nonl
    #@-node:ekr.20060220104902:insertNormalChar
    #@+node:ekr.20060222092243:push, pop, clear, stackNames
    def push (self,obj):
        
        if obj is not None:
            self.prevObjects.append(obj)
            # g.trace(self.stackNames())
            
    def pop (self):
        
        obj = self.prevObjects.pop()
        # g.trace(obj)
        return obj
        
    def clear (self):
        
        self.prevObjects = []
        # g.trace(g.callers())
        
    def stackNames (self):
        
        aList = []
        for z in self.prevObjects:
            if hasattr(z,'__name__'):
                aList.append(z.__name__)
            elif hasattr(z,'__class__'):
                aList.append(z.__class__.__name__)
            else:
                aList.append(str(z))
        return aList
    #@nonl
    #@-node:ekr.20060222092243:push, pop, clear, stackNames
    #@+node:ekr.20060221112937:setObjectAndMembersList & helpers
    def setObjectAndMembersList (self,word):
        
        c = self.c
        
        if not word:
            # Leading dot shows all classes.
            self.leadinWord = None
            self.object = sys.modules
            self.membersList = sys.modules.keys()
            self.beginTabName('Modules')
        elif word in ( "'",'"'):
            word = 'aString' # This is in the objectsDict.
            self.clear()
            self.push(self.object)
            self.object = 'aString'
            self.membersList = self.getMembersList(self.object)
        elif self.object:
            self.getObjectFromAttribute(word)
        elif word == 'self':
            self.completeSelf()
        else:
            obj = self.objectDict.get(word) or sys.modules.get(word)
            self.completeFromObject(obj)
    
        # g.trace(word,self.object,len(self.membersList))
    #@nonl
    #@+node:ekr.20060223124014:getObjectFromAttribute
    def getObjectFromAttribute (self,word):
        
        obj = self.object
    
        if obj and self.hasAttr(obj,word):
            self.push(self.object)
            self.object = self.getAttr(obj,word)
            self.appendToKnownObjects(self.object)
            self.membersList = self.getMembersList(self.object)
        else:
            # No special support for 'self' here.
            # Don't clear the stack here!
            self.membersList = []
            self.object = None
    #@nonl
    #@-node:ekr.20060223124014:getObjectFromAttribute
    #@+node:ekr.20060223124014.2:completeSelf
    def completeSelf (self):
        
        # This scan will be fast if an instant object already exists.
        className,obj,p,s = self.classScanner.scan()
        # g.trace(className,obj,p,s and len(s))
    
        # First, look up the className.
        if not obj and className:
            obj = self.allClassesDict.get(className)
            # if obj: g.trace('found in allClassesDict: %s = %s' % (className,obj))
    
        # Second, create the object from class definition.
        if not obj and s:
            theClass = self.computeClassObjectFromString(className,s)
            if theClass:
                obj = self.createProxyObjectFromClass(className,theClass)
                if obj:
                    self.selfObjectsDict [className] = obj
                    # This prevents future rescanning, even if the node moves.
                    self.selfTnodesDict [p.v.t] = obj
        if obj:
            self.selfClassName = className
            self.push(self.object)
            self.object = obj
            self.membersList = self.getMembersList(obj=obj)
        else:
            # No further action possible or desirable.
            self.selfClassName = None
            self.object = None
            self.clear()
            self.membersList = []
    #@nonl
    #@-node:ekr.20060223124014.2:completeSelf
    #@+node:ekr.20060223124014.3:completeFromObject
    def completeFromObject (self,obj):
    
        if obj:
            self.appendToKnownObjects(obj)
            self.push(self.object)
            self.object = obj
            self.membersList = self.getMembersList(obj=obj)
        else:
            self.object = None
            self.clear()
            self.membersList = []
    #@nonl
    #@-node:ekr.20060223124014.3:completeFromObject
    #@-node:ekr.20060221112937:setObjectAndMembersList & helpers
    #@+node:ekr.20051127070018:setSelection
    def setSelection (self,s):
        
        c = self.c ; w = self.widget
        c.widgetWantsFocusNow(w)
        
        if g.app.gui.hasSelection(w):
            i,j = g.app.gui.getSelectionRange(w)
            w.delete(i,j)
        else:
            i = g.app.gui.getInsertPoint(w)
            
        # Don't go past the ':' that separates the completion from the type.
        n = s.find(':')
        if n > -1: s = s[:n]
        
        w.insert(i,s)
        j = w.index('%s + %dc' % (i,len(s)))
        g.app.gui.setSelectionRange(w,i,j,insert=j)
    #@nonl
    #@-node:ekr.20051127070018:setSelection
    #@+node:ekr.20060220062710:start
    def start (self,event=None,w=None):
        
        if w: self.widget = w
        else: w = self.widget
        
        # We wait until now to define these dicts so that more classes and objects will exist.
        if not self.objectDict:
            self.defineClassesDict()
            self.defineObjectDict()
    
        self.prefix = ''
        self.selection = g.app.gui.getTextSelection(w)
        self.selectedText = g.app.gui.getSelectedText(w)
        flag = self.getLeadinWord(w)
        if self.membersList:
            if not flag:
                # Remove the (leading) invocation character.
                i = g.app.gui.getInsertPoint(w)
                if w.get(i+'-1c') == '.':
                    w.delete(i+'-1c')
                    
            self.autoCompleterStateHandler(event)
        else:
            self.abort()
    #@nonl
    #@-node:ekr.20060220062710:start
    #@-node:ekr.20060216160332.2:Helpers
    #@+node:ekr.20060216160332.1:Scanning
    # Not used at present, but soon.
    #@nonl
    #@+node:ekr.20060217132329:initialScan
    # Don't call this finishCreate: the startup logic would call it too soon.
    
    def initialScan (self):
        
        g.trace(g.callers())
        
        self.scan(thread=True)
    #@nonl
    #@-node:ekr.20060217132329:initialScan
    #@+node:ekr.20060216155558.1:scan
    def scan (self,event=None,verbose=True,thread=True):
        
        c = self.c
        if not c or not c.exists or c.frame.isNullFrame: return
        if g.app.unitTesting: return
        
        # g.trace('autocompleter')
        
        if 0: ## thread:
            # Use a thread to do the initial scan so as not to interfere with the user.            
            def scan ():
                #g.es( "This is for testing if g.es blocks in a thread", color = 'pink' )
                # During unit testing c gets destroyed before the scan finishes.
                if not g.app.unitTesting:
                    self.scanOutline(verbose=True)
        
            t = threading.Thread(target=scan)
            t.setDaemon(True)
            t.start()
        else:
            self.scanOutline(verbose=verbose)
    #@nonl
    #@-node:ekr.20060216155558.1:scan
    #@+node:ekr.20060216163305:definePatterns
    def definePatterns (self):
        
        self.space = r'[ \t\r\f\v ]+' # one or more whitespace characters.
        self.end = r'\w+\s*\([^)]*\)' # word (\w) ws ( any ) (can cross lines)
    
        # Define re patterns for various languages.
        # These patterns match method/function definitions.
        self.pats = {}
        self.pats ['python'] = re.compile(r'def\s+%s' % self.end)  # def ws word ( any ) # Can cross line boundaries.
        self.pats ['java'] = re.compile(
            r'((public\s+|private\s+|protected\s+)?(static%s|\w+%s){1,2}%s)' % (
                self.space,self.space,self.end))
        self.pats ['perl'] = re.compile(r'sub\s+%s' % self.end)
        self.pats ['c++'] = re.compile(r'((virtual\s+)?\w+%s%s)' % (self.space,self.end))
        self.pats ['c'] = re.compile(r'\w+%s%s' % (self.space,self.end))
        
        # Define self.okchars for getCleaString.
        okchars = {}
        for z in string.ascii_letters:
            okchars [z] = z
        okchars ['_'] = '_'
        self.okchars = okchars 
        
        if 0: # not used
            self.r  = string.punctuation.replace('(','').replace('.','') # punctuation except ( and .
            self.pt = string.digits + string.letters + self.r
            ripout = string.punctuation + string.whitespace + '\n'
            self.ripout = ripout.replace('_','') # punctuation except underscore.
    #@nonl
    #@-node:ekr.20060216163305:definePatterns
    #@+node:ekr.20060216161220:scanOutline
    def scanOutline (self,verbose=True):
    
        '''Traverse an outline and build the autocommander database.'''
        
        if verbose: g.es_print('Scanning for auto-completer...')
    
        c = self.c ; k = self.k ; count = 0
        for p in c.rootPosition().allNodes_iter():
            if verbose:
                count += 1 ;
                if (count % 200) == 0: g.es('.',newline=False)
            language = g.scanForAtLanguage(c,p)
            # g.trace('language',language,p.headString())
            s = p.bodyString()
            if k.enable_autocompleter:
                self.scanForAutoCompleter(s)
            if k.enable_calltips:
                self.scanForCallTip(s,language)
    
        if 0:
            g.trace('watchwords...\n\n')
            keys = self.watchwords.keys() ; keys.sort()
            for key in keys:
                aList = self.watchwords.get(key)
                g.trace('%s:\n\n' % (key), g.listToString(aList))
        if 0:
            g.trace('calltips...\n\n')
            keys = self.calltips.keys() ; keys.sort()
            for key in keys:
                d = self.calltips.get(key)
                if d:
                    g.trace('%s:\n\n' % (key), g.dictToString(d))
            
        if verbose:        
            g.es_print('\nauto-completer scan complete',color='blue')
    #@nonl
    #@-node:ekr.20060216161220:scanOutline
    #@+node:ekr.20060216161234:scanForCallTip
    def scanForCallTip (self,s,language):
    
        '''this function scans text for calltip info'''
    
        d = self.calltips.get(language,{})
        pat = self.pats.get(language or 'python')
        
        # Set results to a list of all the function/method defintions in s.
        results = pat and pat.findall(s) or []
    
        for z in results:
            if isinstance(z,tuple): z = z [0]
            pieces2 = z.split('(')
            # g.trace(pieces2)
            pieces2 [0] = pieces2 [0].split() [-1]
            a, b = pieces2 [0], pieces2 [1]
            aList = d.get(a,[])
            if str(z) not in aList:
                aList.append(str(z))
                d [a] = aList
        
        self.calltips [language] = d
    #@nonl
    #@-node:ekr.20060216161234:scanForCallTip
    #@+node:ekr.20060216161247:scanForAutoCompleter
    def scanForAutoCompleter (self,s):
    
        '''This function scans text for the autocompleter database.'''
    
        aList = [] ; t1 = s.split('.')
        
        if 1: # Slightly faster.
            t1 = s.split('.') ; 
            i = 0 ; n = len(t1)-1
            while i < n:
                self.makeAutocompletionList(t1[i],t1[i+1],aList)
                i += 1
        else:
            reduce(lambda a,b: self.makeAutocompletionList(a,b,aList),t1)
    
        if aList:
            for a, b in aList:
                z = self.watchwords.get(a,[])
                if str(b) not in z:
                    z.append(str(b))
                    self.watchwords [a] = z
    #@nonl
    #@+node:ekr.20051025144611.20:makeAutocompletionList
    def makeAutocompletionList (self,a,b,glist):
        
        '''We have seen a.b, where a and b are arbitrary strings.
        Append (a1.b1) to glist.
        To compute a1, scan backwards in a until finding whitespace.
        To compute b1, scan forwards in b until finding a char not in okchars.
        '''
        
        if 1: # Do everything inline.  It's a few percent faster.
    
            # Compute reverseFindWhitespace inline.
            i = len(a) -1
            while i >= 0:
                if a[i].isspace() or a [i] == '.':
                    a1 = a [i+1:] ; break
                i -= 1
            else:
                a1 = a
                
            # Compute getCleanString inline.
            i = 0
            for ch in b:
                if ch not in self.okchars:
                    b1 = b[:i] ; break
                i += 1
            else:
                b1 = b
    
            if b1:
                glist.append((a1,b1),)
                
            return b # Not needed unless we are using reduce.
        else:
            a1 = self.reverseFindWhitespace(a)
            if a1:
                b1 = self.getCleanString(b)
                if b1:
                    glist.append((a1,b1))
            return b 
    #@nonl
    #@+node:ekr.20060216161258:reverseFindWhitespace
    def reverseFindWhitespace (self,s):
    
        '''Return the longest tail of s containing no whitespace or period.'''
    
        i = len(s) -1
        while i >= 0:
            if s[i].isspace() or s [i] == '.': return s [i+1:]
            i -= 1
    
        return s
    #@nonl
    #@-node:ekr.20060216161258:reverseFindWhitespace
    #@+node:ekr.20060216161253:getCleanString
    def getCleanString (self,s):
        
        '''Return the prefix of s containing only chars in okchars.'''
        
        i = 0
        for ch in s:
            if ch not in self.okchars:
                return s[:i]
            i += 1
    
        return s
    #@nonl
    #@-node:ekr.20060216161253:getCleanString
    #@-node:ekr.20051025144611.20:makeAutocompletionList
    #@-node:ekr.20060216161247:scanForAutoCompleter
    #@-node:ekr.20060216160332.1:Scanning
    #@+node:ekr.20060223114802:Proxy classes and objects
    #@+node:ekr.20060223114802.1:createProxyObjectFromClass
    def createProxyObjectFromClass (self,className,theClass):
        
        '''Create a dummy instance object by instantiating theClass with a dummy ctor.'''
    
        if 0: # Calling the real ctor is way too dangerous.
            # Set args to the list of required arguments.
            args = inspect.getargs(theClass.__init__.im_func.func_code)
            args = args[0] ; n = len(args)-1
            args = [None for z in xrange(n)]
            
        def dummyCtor (self):
            pass
            
        try:
            obj = None
            old_init = hasattr(theClass,'__init__') and theClass.__init__
            theClass.__init__ = dummyCtor
            obj = theClass()
        finally:
            if old_init:
                theClass.__init__ = old_init
            else:
                delattr(theClass,'__init__')
            
        g.trace(type(theClass),obj)
    
        # Verify that it has all the proper attributes.
        # g.trace(g.listToString(dir(obj)))
        return obj
    #@nonl
    #@-node:ekr.20060223114802.1:createProxyObjectFromClass
    #@+node:ekr.20060223093358:createClassObjectFromString
    def computeClassObjectFromString (self,className,s):
    
        try:
            # Add the the class definition to the present environment.
            exec s
    
            # Get the newly created object from the locals dict.
            theClass = locals().get(className)
            return theClass
    
        except Exception:
            if 1: # Could be a weird kind of user error.
                g.es_print('unexpected exception in computeProxyObject')
                g.es_exception()
            return None
    #@nonl
    #@-node:ekr.20060223093358:createClassObjectFromString
    #@-node:ekr.20060223114802:Proxy classes and objects
    #@+node:ekr.20060223093117:class forgivingParserClass
    class forgivingParserClass:
        
        '''A class to create a valid class instances from
        a class definition that may contain syntax errors.'''
        
        #@    @+others
        #@+node:ekr.20060223093117.1:ctor (forgivingParserClass)
        def __init__ (self,c):
            
            self.c = c
            self.excludedTnodesList = []
            self.old_putBody = None # Set in parse for communication with newPutBody.
        #@nonl
        #@-node:ekr.20060223093117.1:ctor (forgivingParserClass)
        #@+node:ekr.20060223093117.2:parse
        def parse (self,p):
            
            '''The top-level parser method.
            
            It patches c.atFileCommands.putBody, calls the forgiving parser and finally
            restores c.atFileCommands.putBody.'''
            
            c = self.c
            
            # Create an ivar for communication with newPutBody.
            self.old_putBody = c.atFileCommands.putBody
            
            # Override atFile.putBody.
            c.atFileCommands.putBody = self.newPutBody
            
            try:
                s = None
                s = self.forgivingParser(p)
            finally:
                c.atFileCommands.putBody = self.old_putBody
                return s
        #@nonl
        #@-node:ekr.20060223093117.2:parse
        #@+node:ekr.20060223093117.3:forgivingParser
        def forgivingParser (self,p):
        
            c = self.c ; root = p.copy()
            self.excludedTnodesList = []
            s = g.getScript(c,root,useSelectedText=False)
            while s:
                try:
                    val = compiler.parse(s+'\n')
                    break
                except (parser.ParserError,SyntaxError):
                    fileName, n = g.getLastTracebackFileAndLineNumber()
                    p = self.computeErrorNode(c,root,n,lines=g.splitLines(s))
                    if not p or p == root:
                        g.es_print('Syntax error in class node: can not continue')
                        s = None ; break
                    else:
                        # g.es_print('Syntax error: deleting %s' % p.headString())
                        self.excludedTnodesList.append(p.v.t)
                        s = g.getScript(c,root,useSelectedText=False)
            return s or ''
        #@nonl
        #@-node:ekr.20060223093117.3:forgivingParser
        #@+node:ekr.20060223093117.4:computeErrorNode
        def computeErrorNode (self,c,root,n,lines):
        
            '''The from c.goToLineNumber that applies to scripts.
            Unlike c.gotoLineNumberOpen, this function returns a position.'''
        
            if n == 1 or n >= len(lines):
                return root
        
            vnodeName, junk, junk, junk, junk = c.convertLineToVnodeNameIndexLine(
                lines, n, root, scriptFind = True)
        
            if vnodeName:
                for p in root.self_and_subtree_iter():
                    if p.matchHeadline(vnodeName):
                        return p
        
            return None
        #@nonl
        #@-node:ekr.20060223093117.4:computeErrorNode
        #@+node:ekr.20060223093117.5:newPutBody
        def newPutBody (self,p,oneNodeOnly=False,fromString=''):
        
            if p.v.t in self.excludedTnodesList:
                pass
                # g.trace('ignoring',p.headString())
            else:
                self.old_putBody(p,oneNodeOnly,fromString)
        #@nonl
        #@-node:ekr.20060223093117.5:newPutBody
        #@-others
    #@nonl
    #@-node:ekr.20060223093117:class forgivingParserClass
    #@+node:ekr.20060222082041:class classScannerClass
    class classScannerClass:
        
        '''A class to find class definitions in a node or its parents.'''
        
        #@    @+others
        #@+node:ekr.20060222082041.1:ctor
        def __init__ (self,c):
            
            self.c = c
            
            # Ignore @root for now:
            # self.start_in_doc = c.config.getBool('at_root_bodies_start_in_doc_mode')
        
            self.start_in_doc = False
        #@nonl
        #@-node:ekr.20060222082041.1:ctor
        #@+node:ekr.20060223120755:scan
        def scan (self):
            
            c = self.c
        
            className,obj,p = self.findParentClass(c.currentPosition())
            # g.trace(className,obj,p)
        
            if p and not obj:
                parser = c.k.autoCompleter.forgivingParser
                s = parser.parse(p)
            else:
                s = None
                
            return className,obj,p,s
        #@nonl
        #@-node:ekr.20060223120755:scan
        #@+node:ekr.20060222082041.2:findParentClass
        def findParentClass (self,root):
            
            autoCompleter = self.c.k.autoCompleter
            
            # First, see if any parent has already been scanned.
            for p in root.self_and_parents_iter():
                obj = autoCompleter.selfTnodesDict.get(p.v.t)
                if obj:
                    # g.trace('found',obj,'in',p.headString())
                    return None,obj,p
            
            # Next, do a much slower scan.
            # g.trace('slow scanning...')
            for p in root.self_and_parents_iter():
                className = self.findClass(p)
                if className:
                    # g.trace('found',className,'in',p.headString())
                    return className,None,p
            
            return None,None,None
        #@nonl
        #@-node:ekr.20060222082041.2:findParentClass
        #@+node:ekr.20060222082041.3:findClass & helpers
        def findClass (self,p):
        
            lines = g.splitLines(p.bodyString())
            inDoc = self.start_in_doc
            # g.trace(p.headString())
            for s in lines:
                if inDoc:
                    if self.endsDoc(s):
                        inDoc = False
                else:
                    if self.startsDoc(s):
                        inDoc = True
                    else:
                        # Not a perfect scan: a triple-string could start with 'class',
                        # but perfection is not important.
                        className = self.startsClass(s)
                        if className: return className
            else:
                return None
        #@nonl
        #@+node:ekr.20060222082041.4:endsDoc
        def endsDoc (self,s):
            
            return s.startswith('@c')
        #@nonl
        #@-node:ekr.20060222082041.4:endsDoc
        #@+node:ekr.20060222082041.5:startsClass
        def startsClass (self,s):
            
            if s.startswith('class'):
                i = 5
                i = g.skip_ws(s,i)
                j = g.skip_id(s,i)
                word = s[i:j]
                # g.trace(word)
                return word
            else:
                return None
        #@nonl
        #@-node:ekr.20060222082041.5:startsClass
        #@+node:ekr.20060222082041.6:startsDoc
        def startsDoc (self,s):
        
            for s2 in ('@doc','@ ','@\n', '@r', '@\t'):
                if s.startswith(s2):
                    return True
            else:
                return False
        #@nonl
        #@-node:ekr.20060222082041.6:startsDoc
        #@-node:ekr.20060222082041.3:findClass & helpers
        #@-others
    #@nonl
    #@-node:ekr.20060222082041:class classScannerClass
    #@-others
#@nonl
#@-node:ekr.20051126123249:class autoCompleterClass
#@+node:ekr.20060219100201:class keyHandlerClass
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
        'Caps_Lock','Num_Lock', # New in 4.4b3.
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
        
        self.enable_autocompleter           = c.config.getBool('enable_autocompleter')
        self.enable_calltips                = c.config.getBool('enable_calltips')
        self.ignore_caps_lock               = c.config.getBool('ignore_caps_lock')
        self.ignore_unbound_non_ascii_keys  = c.config.getBool('ignore_unbound_non_ascii_keys')
        self.swap_mac_keys                  = c.config.getBool('swap_mac_keys')
        self.trace_key_event                = c.config.getBool('trace_key_event')
        self.trace_minibuffer               = c.config.getBool('trace_minibuffer')
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
        
        self.autoCompleter = autoCompleterClass(self)
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
    #@+node:ekr.20060216074643:k.completeAllBindings
    def completeAllBindings (self):
        
        '''New in 4.4b3: make an actual binding in *all* the standard places.
        
        The event will go to k.masterKeyHandler as always, so nothing really changes.
        except that k.masterKeyHandler will know the proper stroke.'''
        
        k = self ; c = k.c ; f = c.frame
        bodyCtrl = f.body and hasattr(f.body,'bodyCtrl') and f.body.bodyCtrl or None
        canvas   = f.tree and hasattr(f.tree,'canvas')   and f.tree.canvas   or None
        bindingWidget = f.tree and hasattr(f.tree,'bindingWidget') and f.tree.bindingWidget or None
        if not bodyCtrl or not canvas: return
        
        for w in (c.miniBufferWidget,bodyCtrl,canvas,bindingWidget):
            self.completeAllBindingsForWidget(w)
            
            
            # for stroke in  k.bindingsDict.keys():
            # 
                # def bindKeyCallback (event,k=k,stroke=stroke):
                    # return k.masterKeyHandler(event,stroke=stroke)
                # bindStroke = k.tkbindingFromStroke(stroke)
                # try:
                    # # g.trace(bindStroke,c.widget_name(w))
                    # w.bind(bindStroke,bindKeyCallback)
                # except Exception:
                    # g.es_print('exception binding %s to %s' % (
                        # bindStroke,c.widget_name(w)),color='blue')
    #@nonl
    #@+node:ekr.20060221141535:completeAllBindingsForWidget
    def completeAllBindingsForWidget (self,w):
        
        k = self ; c = k.c
        
        for stroke in  k.bindingsDict.keys():
        
            def bindKeyCallback (event,k=k,stroke=stroke):
                return k.masterKeyHandler(event,stroke=stroke)
            bindStroke = k.tkbindingFromStroke(stroke)
    
            try:
                # g.trace(bindStroke,c.widget_name(w))
                w.bind(bindStroke,bindKeyCallback)
            except Exception:
                g.es_print('exception binding %s to %s' % (
                    bindStroke,c.widget_name(w)),color='blue')
    #@nonl
    #@-node:ekr.20060221141535:completeAllBindingsForWidget
    #@-node:ekr.20060216074643:k.completeAllBindings
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
        k.completeAllBindings()
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
            # g.trace('leoCommands %24s = %s' % (f.__name__,key))
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
            'Caps_Lock','Num_Lock','Control_L','Alt_L','Shift_L','Control_R','Alt_R','Shift_R')
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
    
        if k.abortAllModesKey and g.safeStringCompare(stroke,k.abortAllModesKey): # 'Control-g'
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
        elif k.ignore_unbound_non_ascii_keys and len(ch) > 1:
            # g.trace('non-ascii')
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
        prefix=None,tabList=[],completion=True):
        
        '''Accumulate an argument until the user hits return (or control-g).
        Enter the given return state when done.
        The prefix is does not form the arg.  The prefix defaults to the k.getLabel().
        '''
    
        k = self ; c = k.c ; state = k.getState('getArg')
        keysym = (event and event.keysym) or ''
        trace = c.config.getBool('trace_modes') and not g.app.unitTesting
        if trace: g.trace(
            'state',state,'keysym',keysym,
            'completion', state==0 and completion or state!=0 and k.arg_completion)
        if state == 0:
            k.arg = ''
            
            #@        << init altX vars >>
            #@+node:ekr.20050928092516:<< init altX vars >>
            k.argTabList = tabList and tabList[:] or []
            k.arg_completion = completion
            
            k.mb_prefix = prefix or k.getLabel()
            k.mb_prompt = prefix or ''
            k.mb_tabList = []
            
            # Clear the list: any non-tab indicates that a new prefix is in effect.
            k.mb_tabListPrefix = k.getLabel()
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
            trace and g.trace('kind',kind,'n',n,'handler',handler and handler.__name__)
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
    #@nonl
    #@-node:ekr.20050920085536.62:getArg
    #@+node:ekr.20050920085536.63:keyboardQuit
    def keyboardQuit (self,event):
    
        '''This method clears the state and the minibuffer label.
        
        k.endCommand handles all other end-of-command chores.'''
        
        k = self ; c = k.c
    
        if g.app.quitting:
            return
        
        k.autoCompleter.exit()
        c.frame.log.deleteTab('Mode')
        c.frame.log.hideTab('Completion')
        
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
        # g.trace('leoCommands %24s = %s' % (func.__name__,commandName))
        
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
    # 
    # trace = self.trace_minibuffer and not g.app.unitTesting
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
        trace = self.trace_minibuffer and not g.app.unitTesting
        
        if self.useTextWidget:
            w.update_idletasks()
            s = w and w.get('1.0','end')
            # Remove the cursed Tk newline.
            while s.endswith('\n') or s.endswith('\r'):
                s = s[:-1]
            
        else:
            s = k.svar and k.svar.get()
            
        trace and g.trace(repr(s))
    
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
        trace = self.trace_minibuffer and not g.app.unitTesting
    
        trace and g.trace(repr(s),g.callers())
    
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
        trace = self.trace_minibuffer and not g.app.unitTesting
        
        trace and g.trace(repr(s))
        if not s: return
    
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
    def updateLabel (self,event):
    
        '''Mimic what would happen with the keyboard and a Text editor
        instead of plain accumalation.'''
        
        k = self ; c = k.c ; w = self.widget
        ch = (event and event.char) or ''
        keysym = (event and event.keysym) or ''
        trace = self.trace_minibuffer and not g.app.unitTesting
    
        trace and g.trace('ch',ch,'keysym',keysym,'k.stroke',k.stroke)
        
        if ch and ch not in ('\n','\r'):
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
        # trace = self.trace_minibuffer and not g.app.unitTesting
        
        s = w.get('1.0','end')
        while s.endswith('\n') or s.endswith('\r'):
            s = s[:-1] ; n += 1
            
        i = w.index('1.%d' % len(k.mb_prefix))
        j = w.index('end -%dc' % n)
        
        # if trace: g.trace(i,j)
        return i,j
    #@-node:ekr.20060210141604.1:getEditableTextRange
    #@-node:ekr.20050924064254:Label...
    #@+node:ekr.20060129052538.1:Master event handlers (keyHandler)
    #@+node:ekr.20060127183752:masterKeyHandler & helper
    master_key_count = 0
    
    def masterKeyHandler (self,event,stroke=None):
        
        '''In the new binding scheme, there is only one key binding.
        
        This is the handler for that binding.'''
        
        k = self ; c = k.c
        val = self.masterKeyHandlerHelper(event,stroke)
        if val and c and c.exists: # Ignore special keys.
            c.frame.updateStatusLine()
            c.masterFocusHandler()
        return val
    #@nonl
    #@+node:ekr.20060205221734:masterKeyHandlerHelper
    def masterKeyHandlerHelper (self,event,stroke):
    
        k = self ; c = k.c
        w = event and event.widget
        w_name = c.widget_name(w)
        trace = c.config.getBool('trace_masterKeyHandler') and not g.app.unitTesting
        keysym = event.keysym or ''
        if keysym in (
            'Caps_Lock', 'Num_Lock', 'Control_L', 'Alt_L',
            'Shift_L', 'Control_R', 'Alt_R','Shift_R','Win_L','Win_R'):
            return None
            
        self.master_key_count += 1
        if trace and (self.master_key_count % 100) == 0:
            g.printGcSummary(trace=True)
    
        if 0:
            if stroke is None:
                if trace: g.trace('no stroke: using strokeFromEvent')
                stroke = k.strokeFromEvent(event)
    
        # Pass keyboard-quit to k.masterCommand for macro recording.
        if k.abortAllModesKey and stroke == k.abortAllModesKey:
            return k.masterCommand(event,k.keyboardQuit,stroke,'keyboard-quit')
            
        state = k.state.kind
        if trace: g.trace(repr(stroke),'state',state)
        if k.inState():
            # First: honor the 'mini' bindings, but *not* in auto-complete state.
            if not state.startswith('auto-'):
                d = k.masterBindingsDict.get('mini')
                b = d.get(stroke)
                if b:
                    if trace: g.trace(repr(stroke),'mini binding',b.commandName)
                    # Pass this on for macro recording.
                    k.masterCommand(event,b.func,stroke,b.commandName)
                    c.minibufferWantsFocus()
                    return 'break'
            # Second, pass keys to getArg or full-command modes if they are active.
            if state == 'getArg':
                return k.getArg(event)
            elif state in ('full-command','auto-complete'):
                # Do the default state action.
                if trace: g.trace('calling state function')
                val = k.callStateFunction(event) # Calls end-command.
                if val != 'do-standard-keys':
                    return 'break'
                g.trace('do-standard-keys',w_name,stroke)
            # Third, pass keys to the general mode handler.
            else:
                d =  k.masterBindingsDict.get(state)
                if d:
                    # A typical state
                    b = d.get(stroke)
                    # g.trace(d.keys())
                    if b:
                        if trace: g.trace('calling generalModeHandler')
                        k.generalModeHandler (event,
                            commandName=b.commandName,func=b.func,
                            modeName=state,nextMode=b.nextMode)
                        return 'break'
                    else:
                        if trace: g.trace('calling modeHelp')
                        k.modeHelp(event)
                        return 'break'
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
            ('text','log'),
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
    
        if k.ignore_unbound_non_ascii_keys and len(event.char) > 1:
            # (stroke.find('Alt+') > -1 or stroke.find('Ctrl+') > -1)):
            if trace: g.trace('ignoring unbound non-ascii key')
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
        trace = c.config.getBool('trace_masterClickHandler') and not g.app.unitTesting
    
        if trace: g.trace(wname,func and func.__name__)
            
        # A click outside the minibuffer terminates any state.
        if k.inState() and c.useTextMinibuffer and w != c.frame.miniBufferWidget:
            if not c.widget_name(w).startswith('log'):
                k.keyboardQuit(event)
                w and c.widgetWantsFocusNow(w)
                return 'break'
    
        # Update the selection point immediately for updateStatusLine.
        if wname.startswith('body'):
            i = w.index('@%s,%s' % (event.x,event.y))
            g.app.gui.setTextSelection(w,i,i,insert=i)
            c.editCommands.setMoveCol(i)
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
        
        if stroke: # New in 4.4a6:
            return k.masterKeyHandler(event,stroke=stroke)
        else:
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
    #@+node:ekr.20050920085536.46:k.doBackSpace
    # Used by getArg and fullCommand.
    
    def doBackSpace (self,defaultCompletionList,completion=True):
    
        '''Cut back to previous prefix and update prefix.'''
    
        k = self ; c = k.c
        
        if 0:
            g.trace('completion',completion,
                len(k.mb_tabListPrefix) > len(k.mb_prefix),
                repr(k.mb_tabListPrefix),repr(k.mb_prefix))
        
        if completion:
            if len(k.mb_tabListPrefix) > len(k.mb_prefix):
                k.mb_tabListPrefix = k.mb_tabListPrefix [:-1]
                k.setLabel(k.mb_tabListPrefix)
                k.computeCompletionList(defaultCompletionList,backspace=True)
            # else:
                # k.keyboardQuit(event=None)
        else:
            s = k.getLabel(ignorePrompt=False)
            # g.trace(repr(s),repr(k.mb_prefix))
            if s and len(s) > len(k.mb_prefix):
                k.setLabel(s[:-1])
    #@nonl
    #@-node:ekr.20050920085536.46:k.doBackSpace
    #@+node:ekr.20050920085536.44:k.doTabCompletion
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
    
        c.minibufferWantsFocusNow()
    #@nonl
    #@-node:ekr.20050920085536.44:k.doTabCompletion
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
        
        k = self
    
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
        #@nonl
        #@-node:ekr.20060201065809:<< define cmd, ctrl, alt, shift >>
        #@nl
        if k.swap_mac_keys and sys.platform == "darwin":
            #@        << swap cmd and ctrl keys >>
            #@+node:ekr.20060215104239:<< swap cmd and ctrl keys >>
            if ctrl and not cmd:
                cmd = True ; ctrl = False
            if alt and not ctrl:
                ctrl = True ; alt = False
            #@nonl
            #@-node:ekr.20060215104239:<< swap cmd and ctrl keys >>
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
            last2 = k.tkBindNamesDict.get(last) # Fix new bug introduced in 4.4b2.
            if last2:
                last = last2 ; shift = False # Ignore the shift state for these special chars.
            else:
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
            (cmd, 'Command+'),
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
        
        k = self
        if event is None: return ''
        trace = k.trace_key_event and not g.app.unitTesting
        state = event.state or 0
        keysym = event.keysym or ''
        ch = event.char
        result = []
        shift = (state & 1) == 1 # Not used for alpha chars.
        caps  = (state & 2) == 2
        ctrl  = (state & 4) == 4
        # Linux uses, 8 and 0x80, XP uses 0x20000.
        if sys.platform=='darwin':
            alt = (state&0x10) == 0x10
            #num = False
        elif sys.platform.startswith('win'):
            alt = (state & 0x20000) == 0x20000
            #num = (state & 8) == 8
        else:
            #num = False # ???
            alt = (state & 8) == 8 or (state & 0x80) == 0x80
        plain = len(keysym) == 1 # E.g., for ctrl-v the keysym is 'v' but ch is empty.
        
        if trace: g.trace('ch',repr(ch),'keysym',repr(keysym),'state: %x' % state)
        
        # Undo the effect of the caps-lock key.
        if caps:
            if alt or ctrl or k.ignore_caps_lock:
                if shift:
                    ch = ch.upper() ; keysym = keysym.upper()
                    event.char=event.char.upper()
                    event.keysym=event.keysym.upper()
                else:
                    ch = ch.lower() ; keysym = keysym.lower()
                    event.char=event.char.lower()
                    event.keysym=event.keysym.lower()
        
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
                pass # There are lots of keysyms that Leo may not know about.
                # g.trace('*'*30,'unknown keysym',repr(keysym))
        
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
        
        '''Convert a stroke (key to k.bindingsDict) to an actual Tk binding.'''
        
        stroke = stroke.lstrip('<').rstrip('>')
        
        for a,b in (
            ('Alt+','Alt-'),
            ('Ctrl+','Control-'),
            ('Shift+','Shift-'),
            ('Command+','Command-'),
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
#@-node:ekr.20060219100201:class keyHandlerClass
#@-others
#@nonl
#@-node:ekr.20031218072017.3748:@thin leoKeys.py
#@-leo
