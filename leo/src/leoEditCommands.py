# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:ekr.20050710142719:@thin leoEditCommands.py
#@@first

'''Basic editor commands for Leo.

Modelled after Emacs and Vim commands.'''

from __future__ import generators # To make Leo work with Python 2.2

#@<< imports >>
#@+node:ekr.20050710151017:<< imports >>
import leoGlobals as g

import leoFind
import leoKeys
import leoTest

import cPickle
import difflib
import os
import re
import string
import sys
import threading
import Tkinter as Tk

subprocess     = g.importExtension('subprocess',    pluginName=None,verbose=False)
Pmw            = g.importExtension('Pmw',           pluginName=None,verbose=False)
tkColorChooser = g.importExtension('tkColorChooser',pluginName=None,verbose=False)
tkFileDialog   = g.importExtension('tkFileDialog',  pluginName=None,verbose=False)
tkFont         = g.importExtension('tkFont',        pluginName=None,verbose=False)
#@nonl
#@-node:ekr.20050710151017:<< imports >>
#@nl

#@<< define class baseEditCommandsClass >>
#@+node:ekr.20050920084036.1:<< define class baseEditCommandsClass >>
class baseEditCommandsClass:

    '''The base class for all edit command classes'''

    #@    @+others
    #@+node:ekr.20050920084036.2: ctor, finishCreate, init (baseEditCommandsClass)
    def __init__ (self,c):
    
        self.c = c
        self.k = self.k = None
        self.registers = {} # To keep pychecker happy.
        self.undoData = None
        
    def finishCreate(self):
    
        # Class delegators.
        self.k = self.k = self.c.k
        try:
            self.w = self.c.frame.body.bodyCtrl # New in 4.4a4.
        except AttributeError:
            self.w = None
        
    def init (self):
        
        '''Called from k.keyboardQuit to init all classes.'''
        
        pass
    #@nonl
    #@-node:ekr.20050920084036.2: ctor, finishCreate, init (baseEditCommandsClass)
    #@+node:ekr.20051214132256:begin/endCommand
    #@+node:ekr.20051214133130:beginCommand  & beginCommandWithEvent
    def beginCommand (self,undoType='Typing'):
        
        '''Do the common processing at the start of each command.'''
    
        return self.beginCommandHelper(ch='',undoType=undoType,w=self.w)
    
    def beginCommandWithEvent (self,event,undoType='Typing'):
        
        '''Do the common processing at the start of each command.'''
        
        return self.beginCommandHelper(ch=event.char,undoType=undoType,w=event.widget)
    #@nonl
    #@+node:ekr.20051215102349:beingCommandHelper
    def beginCommandHelper (self,ch,undoType,w):
    
        c = self.c ; p = c.currentPosition()
        name = c.widget_name(w)
        
        # Don't do this in headlines!
        if name.startswith('body'):
            oldSel =  g.app.gui.getTextSelection(w)
            oldText = p.bodyString()
            self.undoData = g.Bunch(
                ch=ch,name=name,oldSel=oldSel,oldText=oldText,w=w,undoType=undoType)
            
        return w
    #@nonl
    #@-node:ekr.20051215102349:beingCommandHelper
    #@-node:ekr.20051214133130:beginCommand  & beginCommandWithEvent
    #@+node:ekr.20051214133130.1:endCommand
    def endCommand(self,label=None,changed=True,setLabel=True):
        
        '''Do the common processing at the end of each command.'''
        
        c = self.c ; b = self.undoData ; k = self.k
    
        if b:
            name = b.name
            if name.startswith('body'):
                if changed:
                    c.frame.body.onBodyChanged(undoType=b.undoType,
                        oldSel=b.oldSel,oldText=b.oldText,oldYview=None)
            elif name.startswith('head'):
                g.trace('Should not happen: endCommand does not support undo in headlines')
            else: pass
            
        self.undoData = None # Bug fix: 1/6/06 (after a5 released).
    
        k.clearState()
        
        # Warning: basic editing commands **must not** set the label.
        if setLabel:
            if label:
                k.setLabelGrey(label)
            else:
                k.resetLabel()
    #@nonl
    #@-node:ekr.20051214133130.1:endCommand
    #@-node:ekr.20051214132256:begin/endCommand
    #@+node:ekr.20050920084036.5:getPublicCommands & getStateCommands
    def getPublicCommands (self):
    
        '''Return a dict describing public commands implemented in the subclass.
        Keys are untranslated command names.  Values are methods of the subclass.'''
    
        return {}
    #@nonl
    #@-node:ekr.20050920084036.5:getPublicCommands & getStateCommands
    #@+node:ekr.20050920084036.6:getWSString
    def getWSString (self,txt):
    
        if 1:
            ntxt = [g.choose(ch=='\t',ch,' ') for ch in txt]
        else:
            ntxt = []
            for z in txt:
                if z == '\t':
                    ntxt.append(z)
                else:
                    ntxt.append(' ')
    
        return ''.join(ntxt)
    #@nonl
    #@-node:ekr.20050920084036.6:getWSString
    #@+node:ekr.20050920084036.7:oops
    def oops (self):
    
        print("baseEditCommandsClass oops:",
            g.callers(),
            "must be overridden in subclass")
    #@nonl
    #@-node:ekr.20050920084036.7:oops
    #@+node:ekr.20050920084036.12:removeRKeys (baseCommandsClass)
    def removeRKeys (self,w):
    
        mrk = 'sel'
        w.tag_delete(mrk)
        w.unbind('<Left>')
        w.unbind('<Right>')
        w.unbind('<Up>')
        w.unbind('<Down>')
    #@nonl
    #@-node:ekr.20050920084036.12:removeRKeys (baseCommandsClass)
    #@+node:ekr.20050929161635:Helpers
    #@+node:ekr.20050920084036.249:_chckSel
    def _chckSel (self,event,warning='no selection'):
    
        c = self.c ; k = self.k
        
        w = event and event.widget
    
        val = 'sel' in w.tag_names() and w.tag_ranges('sel')
        
        if warning and not val:
            k.setLabelGrey(warning)
        
        return val
    #@nonl
    #@-node:ekr.20050920084036.249:_chckSel
    #@+node:ekr.20050920084036.250:_checkIfRectangle
    def _checkIfRectangle (self,event):
    
        k = self.k ; key = event.keysym.lower()
        
        val = self.registers.get(key)
    
        if val and type(val) == type([]):
            k.clearState()
            k.setLabelGrey("Register contains Rectangle, not text")
            return True
    
        return False
    #@nonl
    #@-node:ekr.20050920084036.250:_checkIfRectangle
    #@+node:ekr.20050920084036.10:contRanges
    def contRanges (self,w,range):
    
        ranges = w.tag_ranges(range)
        t1 = w.get(ranges[0],ranges[-1])
        t2 = []
        for z in xrange(0,len(ranges),2):
            z1 = z + 1
            t2.append(w.get(ranges[z],ranges[z1]))
        t2 = '\n'.join(t2)
        return t1 == t2
    #@-node:ekr.20050920084036.10:contRanges
    #@+node:ekr.20050920084036.233:getRectanglePoints
    def getRectanglePoints (self):
    
        c = self.c ; w = self.w
        c.bodyWantsFocus()
    
        i  = w.index('sel.first')
        i2 = w.index('sel.last')
        r1, r2 = i.split('.')
        r3, r4 = i2.split('.')
    
        return int(r1), int(r2), int(r3), int(r4)
    #@nonl
    #@-node:ekr.20050920084036.233:getRectanglePoints
    #@+node:ekr.20050920084036.9:inRange
    def inRange (self,w,range,l='',r=''):
    
        ranges = w.tag_ranges(range)
        for z in xrange(0,len(ranges),2):
            z1 = z + 1
            l1 = 'insert%s' % l
            r1 = 'insert%s' % r
            if w.compare(l1,'>=',ranges[z]) and w.compare(r1,'<=',ranges[z1]):
                return True
        return False
    #@nonl
    #@-node:ekr.20050920084036.9:inRange
    #@+node:ekr.20051002090441:keyboardQuit
    def keyboardQuit (self,event):
        
        return self.k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20051002090441:keyboardQuit
    #@+node:ekr.20050920084036.11:testinrange
    def testinrange (self,w):
    
        if not self.inRange(w,'sel') or not self.contRanges(w,'sel'):
            self.removeRKeys(w)
            return False
        else:
            return True
    #@nonl
    #@-node:ekr.20050920084036.11:testinrange
    #@-node:ekr.20050929161635:Helpers
    #@-others
#@nonl
#@-node:ekr.20050920084036.1:<< define class baseEditCommandsClass >>
#@nl

#@+others
#@+node:ekr.20050924100713: Module level...
#@+node:ekr.20050920084720:createEditCommanders (leoEditCommands module)
def createEditCommanders (c):
    
    '''Create edit classes in the commander.'''
    
    global classesList

    for name, theClass in classesList:
        theInstance = theClass(c)# Create the class.
        setattr(c,name,theInstance)
        # g.trace(name,theInstance)
#@nonl
#@-node:ekr.20050920084720:createEditCommanders (leoEditCommands module)
#@+node:ekr.20050922104731:finishCreateEditCommanders (leoEditCommands module)
def finishCreateEditCommanders (c):
    
    '''Finish creating edit classes in the commander.
    
    Return the commands dictionary for all the classes.'''
    
    global classesList
    
    d = {}

    for name, theClass in classesList:
        theInstance = getattr(c,name)
        theInstance.finishCreate()
        theInstance.init()
        d2 = theInstance.getPublicCommands()
        if d2:
            d.update(d2)
            if 0:
                keys = d2.keys()
                keys.sort()
                print '----- %s' % name
                for key in keys: print
                
    return d
#@nonl
#@-node:ekr.20050922104731:finishCreateEditCommanders (leoEditCommands module)
#@+node:ekr.20050924100713.1:initAllEditCommanders
def initAllEditCommanders (c):
    
    '''Re-init classes in the commander.'''
    
    global classesList

    for name, theClass in classesList:
        theInstance = getattr(c,name)
        theInstance.init()
#@nonl
#@-node:ekr.20050924100713.1:initAllEditCommanders
#@-node:ekr.20050924100713: Module level...
#@+node:ekr.20050920085536.84:class  Tracker (an iterator)
class Tracker:

    '''An iterator class to allow the user to cycle through and change a list.'''

    #@    @+others
    #@+node:ekr.20050920085536.85:init
    def __init__ (self):
        
        self.tablist = []
        self.prefix = None 
        self.ng = self._next()
    #@nonl
    #@-node:ekr.20050920085536.85:init
    #@+node:ekr.20050920085536.86:setTabList
    def setTabList (self,prefix,tlist):
        
        self.prefix = prefix 
        self.tablist = tlist 
    #@nonl
    #@-node:ekr.20050920085536.86:setTabList
    #@+node:ekr.20050920085536.87:_next
    def _next (self):
        
        while 1:
            tlist = self.tablist 
            if not tlist:yield ''
            for z in self.tablist:
                if tlist!=self.tablist:
                    break 
                yield z 
    #@nonl
    #@-node:ekr.20050920085536.87:_next
    #@+node:ekr.20050920085536.88:next
    def next (self):
        
        return self.ng.next()
    #@nonl
    #@-node:ekr.20050920085536.88:next
    #@+node:ekr.20050920085536.89:clear
    def clear (self):
    
        self.tablist = []
        self.prefix = None
    #@nonl
    #@-node:ekr.20050920085536.89:clear
    #@-others
#@nonl
#@-node:ekr.20050920085536.84:class  Tracker (an iterator)
#@+node:ekr.20050920084036.13:class abbrevCommandsClass (test)
#@+at
# 
# type some text, set its abbreviation with Control-x a i g, type the text for 
# abbreviation expansion
# type Control-x a e ( or Alt-x expand-abbrev ) to expand abbreviation
# type Alt-x abbrev-on to turn on automatic abbreviation expansion
# Alt-x abbrev-on to turn it off
# 
# an example:
# type:
# frogs
# after typing 's' type Control-x a i g.  This will turn the miniBuffer blue, 
# type in your definition. For example: turtles.
# 
# Now in the buffer type:
# frogs
# after typing 's' type Control-x a e.  This will turn the 'frogs' into:
# turtles
#@-at
#@@c

class abbrevCommandsClass (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.14: ctor & finishCreate
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        # Set local ivars.
        self.abbrevs ={}
        
    def finishCreate(self):
        
        baseEditCommandsClass.finishCreate(self)
    
        
    #@nonl
    #@-node:ekr.20050920084036.14: ctor & finishCreate
    #@+node:ekr.20050920084036.15: getPublicCommands & getStateCommands
    def getPublicCommands (self):
        
        return {
            'abbrev-mode':                  self.toggleAbbrevMode,
            'add-global-abbrev':            self.addAbbreviation,
            'expand-abbrev':                self.expandAbbrev,
            'expand-region-abbrevs':        self.regionalExpandAbbrev,
            'inverse-add-global-abbrev':    self.addInverseAbbreviation,
            'kill-all-abbrevs':             self.killAllAbbrevs,
            'list-abbrevs':                 self.listAbbrevs,
            'read-abbrev-file':             self.readAbbreviations,
            'write-abbrev-file':            self.writeAbbreviations,
        }
    #@nonl
    #@-node:ekr.20050920084036.15: getPublicCommands & getStateCommands
    #@+node:ekr.20050920084036.25:addAbbreviation
    def addAbbreviation (self,event):
        
        '''A small new feature: also sets abbreviations on.'''
                
        k = self.k ; state = k.getState('add-abbr')
    
        if state == 0:
            k.setLabelBlue('Add Abbreviation: ',protect=True)
            k.getArg(event,'add-abbr',1,self.addAbbreviation)
            
        else:
            w = event.widget
            k.clearState()
            k.resetLabel()
            word = w.get('insert -1c wordstart','insert -1c wordend')
            if k.arg.strip():
                self.abbrevs [k.arg] = word
                k.abbrevOn = True
                k.setLabelGrey(
                    "Abbreviations are on.\nAbbreviation: '%s' = '%s'" % (
                    k.arg,word))
    #@nonl
    #@-node:ekr.20050920084036.25:addAbbreviation
    #@+node:ekr.20051004080550:addInverseAbbreviation
    def addInverseAbbreviation (self,event):
        
        k = self.k ; state = k.getState('add-inverse-abbr')
    
        if state == 0:
            k.setLabelBlue('Add Inverse Abbreviation: ',protect=True)
            k.getArg(event,'add-inverse-abbr',1,self.addInverseAbbreviation)
            
        else:
            w = event.widget
            k.clearState()
            k.resetLabel()
            word = w.get('insert -1c wordstart','insert -1c wordend').strip()
            if word:
                self.abbrevs [word] = k.arg
    #@nonl
    #@-node:ekr.20051004080550:addInverseAbbreviation
    #@+node:ekr.20050920084036.27:expandAbbrev
    def expandAbbrev (self,event):
        
        '''Not a command.  Called from k.masterCommand to expand
        abbreviations in event.widget.'''
    
        k = self.k ; ch = event.char.strip() ; w = event.widget 
        word = w.get('insert -1c wordstart','insert -1c wordend')
        
        g.trace('ch',repr(ch),'word',repr(word))
        
        if ch:
            # We must do this: expandAbbrev is called from Alt-x and Control-x,
            # we get two differnt types of data and w states.
            word = '%s%s'% (word,ch)
            
        val = self.abbrevs.get(word)
        if val is not None:
            w.delete('insert -1c wordstart','insert -1c wordend')
            w.insert('insert',val)
            
        return val is not None
    #@nonl
    #@-node:ekr.20050920084036.27:expandAbbrev
    #@+node:ekr.20050920084036.18:killAllAbbrevs
    def killAllAbbrevs (self,event):
    
        self.abbrevs = {}
    #@nonl
    #@-node:ekr.20050920084036.18:killAllAbbrevs
    #@+node:ekr.20050920084036.19:listAbbrevs
    def listAbbrevs (self,event):
    
        k = self.k
        
        if self.abbrevs:
            k.setLabelGrey('\n'.join(
                ['%s=%s' % (z,self.abbrevs[z]) for z in self.abbrevs]))
    #@nonl
    #@-node:ekr.20050920084036.19:listAbbrevs
    #@+node:ekr.20050920084036.20:readAbbreviations
    def readAbbreviations (self,event):
    
        f = tkFileDialog and tkFileDialog.askopenfile()
        if not f: return
    
        for x in f:
            a, b = x.split('=')
            b = b [:-1]
            self.abbrevs [a] = b
        f.close()
    #@nonl
    #@-node:ekr.20050920084036.20:readAbbreviations
    #@+node:ekr.20050920084036.21:regionalExpandAbbrev
    def regionalExpandAbbrev (self,event):
    
        if not self._chckSel(event):
            return
    
        k = self.k
        w = event.widget
        i1 = w.index('sel.first')
        i2 = w.index('sel.last')
        ins = w.index('insert')
        #@    << define a new generator searchXR >>
        #@+node:ekr.20050920084036.22:<< define a new generator searchXR >>
        #@+at 
        #@nonl
        # This is a generator (it contains a yield).
        # To make this work we must define a new generator for each call to 
        # regionalExpandAbbrev.
        #@-at
        #@@c
        def searchXR (i1,i2,ins,event):
            k = self.k ; w = event.widget
            w.tag_add('sXR',i1,i2)
            while i1:
                tr = w.tag_ranges('sXR')
                if not tr: break
                i1 = w.search(r'\w',i1,stopindex=tr[1],regexp=True)
                if i1:
                    word = w.get('%s wordstart' % i1,'%s wordend' % i1)
                    w.tag_delete('found')
                    w.tag_add('found','%s wordstart' % i1,'%s wordend' % i1)
                    w.tag_config('found',background='yellow')
                    if self.abbrevs.has_key(word):
                        k.setLabel('Replace %s with %s? y/n' % (word,self.abbrevs[word]))
                        yield None
                        if k.regXKey == 'y':
                            ind = w.index('%s wordstart' % i1)
                            w.delete('%s wordstart' % i1,'%s wordend' % i1)
                            w.insert(ind,self.abbrevs[word])
                    i1 = '%s wordend' % i1
            w.mark_set('insert',ins)
            w.selection_clear()
            w.tag_delete('sXR')
            w.tag_delete('found')
            k.setLabelGrey('')
            self.k.regx = g.bunch(iter=None,key=None)
        #@nonl
        #@-node:ekr.20050920084036.22:<< define a new generator searchXR >>
        #@nl
        # EKR: the 'result' of calling searchXR is a generator object.
        k.regx.iter = searchXR(i1,i2,ins,event)
        k.regx.iter.next() # Call it the first time.
    #@nonl
    #@-node:ekr.20050920084036.21:regionalExpandAbbrev
    #@+node:ekr.20050920084036.23:toggleAbbrevMode
    def toggleAbbrevMode (self,event):
     
        k = self.k
        k.abbrevOn = not k.abbrevOn
        k.keyboardQuit(event)
        k.setLabel('Abbreviations are ' + g.choose(k.abbrevOn,'On','Off'))
    #@nonl
    #@-node:ekr.20050920084036.23:toggleAbbrevMode
    #@+node:ekr.20050920084036.24:writeAbbreviations
    def writeAbbreviations (self,event):
    
        f = tkFileDialog and tkFileDialog.asksaveasfile()
        if not f: return
    
        for x in self.abbrevs:
            f.write('%s=%s\n' % (x,self.abbrevs[x]))
        f.close()
    #@nonl
    #@-node:ekr.20050920084036.24:writeAbbreviations
    #@-others
#@nonl
#@-node:ekr.20050920084036.13:class abbrevCommandsClass (test)
#@+node:ekr.20050920084036.31:class bufferCommandsClass
#@+at 
#@nonl
# An Emacs instance does not have knowledge of what is considered a buffer in 
# the environment.
# 
# The call to setBufferInteractionMethods calls the buffer configuration 
# methods.
#@-at
#@@c

class bufferCommandsClass (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.32: ctor (bufferCommandsClass)
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.fromName = '' # Saved name from getBufferName.
        self.nameList = [] # [n: <headline>]
        self.names = {}
        self.tnodes = {} # Keys are n: <headline>, values are tnodes.
        
        try:
            self.w = c.frame.body.bodyCtrl
        except AttributeError:
            self.w = None
    #@nonl
    #@-node:ekr.20050920084036.32: ctor (bufferCommandsClass)
    #@+node:ekr.20050920084036.33: getPublicCommands
    def getPublicCommands (self):
    
        return {
        
            # These do not seem useful.
                # 'copy-to-buffer':               self.copyToBuffer,
                # 'insert-to-buffer':             self.insertToBuffer,
           
            'append-to-buffer':             self.appendToBuffer,
            'kill-buffer' :                 self.killBuffer,
            'list-buffers' :                self.listBuffers,
            'list-buffers-alphabetically':  self.listBuffersAlphabetically,
            'prepend-to-buffer':            self.prependToBuffer,
            'rename-buffer':                self.renameBuffer,
            'switch-to-buffer':             self.switchToBuffer,
        }
    #@nonl
    #@-node:ekr.20050920084036.33: getPublicCommands
    #@+node:ekr.20050920084036.34:Entry points
    #@+node:ekr.20050920084036.35:appendToBuffer
    def appendToBuffer (self,event):
    
        self.k.setLabelBlue('Append to buffer: ')
        self.getBufferName(self.appendToBufferFinisher)
    
    def appendToBufferFinisher (self,name):
    
        c = self.c ; k = self.k ; w = self.w
        s = g.app.gui.getSelectedText(w)
        p = self.findBuffer(name)
        if s and p:
            c.beginUpdate()
            try:
                c.selectPosition(p)
                self.beginCommand('append-to-buffer: %s' % p.headString())
                w.insert('end',s)
                w.mark_set('insert','end')
                w.see('end')
                self.endCommand()
            finally:
                c.endUpdate()
                c.recolor_now()
    #@nonl
    #@-node:ekr.20050920084036.35:appendToBuffer
    #@+node:ekr.20050920084036.38:killBuffer
    def killBuffer (self,event):
    
        self.k.setLabelBlue('Kill buffer: ')
        self.getBufferName(self.killBufferFinisher)
    
    def killBufferFinisher (self,name):
    
        c = self.c ; p = self.findBuffer(name)
        if p:
            h = p.headString()
            current = c.currentPosition()
            c.selectPosition(p)
            c.deleteOutline (op_name='kill-buffer: %s' % h)
            c.selectPosition(current)
            self.k.setLabelBlue('Killed buffer: %s' % h)
    #@nonl
    #@-node:ekr.20050920084036.38:killBuffer
    #@+node:ekr.20050920084036.42:listBuffers & listBuffersAlphabetically
    def listBuffers (self,event):
        
        self.computeData()
        
        g.es('Buffers...')
        for name in self.nameList:
            g.es(name)
            
    def listBuffersAlphabetically (self,event):
        
        self.computeData()
        names = self.nameList[:] ; names.sort()
        
        g.es('Buffers...')
        for name in names:
            g.es(name)
    #@nonl
    #@-node:ekr.20050920084036.42:listBuffers & listBuffersAlphabetically
    #@+node:ekr.20050920084036.39:prependToBuffer (test)
    def prependToBuffer (self,event):
    
        self.k.setLabelBlue('Prepend to buffer: ')
        self.getBufferName(self.prependToBufferFinisher)
        
    def prependToBufferFinisher (self,event,name):
        
        c = self.c ; k = self.k ; w = self.w
        s = g.app.gui.getSelectedText(w)
        p = self.findBuffer(name)
        if s and p:
            c.beginUpdate()
            try:
                c.selectPosition(p)
                self.beginCommand('prepend-to-buffer: %s' % p.headString())
                w.insert('1.0',s)
                w.mark_set('insert','1.0')
                w.see('1.0')
                self.endCommand()
            finally:
                c.endUpdate()
                c.recolor_now()
    #@nonl
    #@-node:ekr.20050920084036.39:prependToBuffer (test)
    #@+node:ekr.20050920084036.43:renameBuffer
    def renameBuffer (self,event):
        
        self.k.setLabelBlue('Rename buffer from: ')
        self.getBufferName(self.renameBufferFinisher1)
        
    def renameBufferFinisher1 (self,name):
        
        self.fromName = name
        self.k.setLabelBlue('Rename buffer from: %s to: ' % (name))
        self.getBufferName(self.renameBufferFinisher2)
        
    def renameBufferFinisher2 (self,name):
        
        c = self.c ; p = self.findBuffer(self.fromName)
        if p:
            c.frame.tree.editLabel(p)
            w = p.edit_widget()
            if w:
                w.delete("1.0","end")
                w.insert("1.0",name)
                c.endEditing()
    #@nonl
    #@-node:ekr.20050920084036.43:renameBuffer
    #@+node:ekr.20050920084036.40:switchToBuffer
    def switchToBuffer (self,event):
    
        self.k.setLabelBlue('Switch to buffer: ')
        self.getBufferName(self.switchToBufferFinisher)
        
    def switchToBufferFinisher (self,name):
        
        c = self.c ; p = self.findBuffer(name)
        if p:
            c.beginUpdate()
            try:
                c.selectPosition(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20050920084036.40:switchToBuffer
    #@+node:ekr.20051216080913:Not ready, and not very useful
    # These commands are disabled in getPublicCommands.
    #@nonl
    #@+node:ekr.20050920084036.36:copyToBuffer (what should this do?)
    def copyToBuffer (self,event):
    
        self.k.setLabelBlue('Copy to buffer: ')
        self.getBufferName(self.copyToBufferFinisher)
    
    def copyToBufferFinisher (self,event,name):
    
        c = self.c ; k = self.k ; w = self.w
        s = g.app.gui.getSelectedText(w)
        p = self.findBuffer(name)
        if s and p:
            c.beginUpdate()
            try:
                c.selectPosition(p)
                self.beginCommand('copy-to-buffer: %s' % p.headString())
                w.insert('end',s)
                w.mark_set('insert','end')
                w.see('end')
                self.endCommand()
            finally:
                c.endUpdate()
                c.recolor_now()
    #@nonl
    #@-node:ekr.20050920084036.36:copyToBuffer (what should this do?)
    #@+node:ekr.20050920084036.37:insertToBuffer (test)
    def insertToBuffer (self,event):
    
        self.k.setLabelBlue('Insert to buffer: ')
        self.getBufferName(self.insertToBufferFinisher)
    
    def insertToBufferFinisher (self,event,name):
        
        c = self.c ; k = self.k ; w = self.w
        s = g.app.gui.getSelectedText(w)
        p = self.findBuffer(name)
        if s and p:
            c.beginUpdate()
            try:
                c.selectPosition(p)
                self.beginCommand('insert-to-buffer: %s' % p.headString())
                w.insert('insert',s)
                w.see('insert')
                self.endCommand()
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20050920084036.37:insertToBuffer (test)
    #@-node:ekr.20051216080913:Not ready, and not very useful
    #@-node:ekr.20050920084036.34:Entry points
    #@+node:ekr.20050927102133.1:Utils
    #@+node:ekr.20051215121416:computeData
    def computeData (self):
        
        counts = {} ; self.nameList = []
        self.names = {} ; self.tnodes = {}
       
        for p in self.c.allNodes_iter():
            h = p.headString().strip()
            t = p.v.t
            n = counts.get(t,0) + 1
            counts[t] = n
            if n == 1: # Only make one entry per set of clones.
                nameList = self.names.get(h,[])
                if nameList:
                    if p.parent():
                        key = '%s, parent: %s' % (h,p.parent().headString())
                    else:
                        key = '%s, child index: %d' % (h,p.childIndex())
                else:
                    key = h
                self.nameList.append(key)
                self.tnodes[key] = t
                nameList.append(key)
                self.names[h] = nameList
    #@nonl
    #@-node:ekr.20051215121416:computeData
    #@+node:ekr.20051215164823:findBuffer
    def findBuffer (self,name):
        
        t = self.tnodes.get(name)
    
        for p in self.c.allNodes_iter():
            if p.v.t == t:
                return p
               
        g.trace("Can't happen",name)
        return None
    #@nonl
    #@-node:ekr.20051215164823:findBuffer
    #@+node:ekr.20050927093851:getBufferName
    def getBufferName (self,finisher):
        
        '''Get a buffer name into k.arg and call k.setState(kind,n,handler).'''
        
        k = self.k ; c = k.c ; state = k.getState('getBufferName')
        
        if state == 0:
            self.computeData()
            self.getBufferNameFinisher = finisher
            prefix = k.getLabel() ; event = None
            k.getArg(event,'getBufferName',1,self.getBufferName,
                prefix=prefix,tabList=self.nameList)
        else:
            k.resetLabel()
            k.clearState()
            finisher = self.getBufferNameFinisher
            self.getBufferNameFinisher = None
            finisher(k.arg)
    #@nonl
    #@-node:ekr.20050927093851:getBufferName
    #@-node:ekr.20050927102133.1:Utils
    #@-others
#@nonl
#@-node:ekr.20050920084036.31:class bufferCommandsClass
#@+node:ekr.20050920084036.150:class controlCommandsClass
class controlCommandsClass (baseEditCommandsClass):
    
    #@    @+others
    #@+node:ekr.20050920084036.151: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.payload = None
    #@nonl
    #@-node:ekr.20050920084036.151: ctor
    #@+node:ekr.20050920084036.152: getPublicCommands
    def getPublicCommands (self):
        
        k = self
    
        return {
            'advertised-undo':              self.advertizedUndo,
            'iconify-frame':                self.iconifyFrame, # Same as suspend.
            'keyboard-quit':                self.keyboardQuit,
            'save-buffers-kill-leo':        self.saveBuffersKillLeo,
            'shell-command':                self.shellCommand,
            'shell-command-on-region':      self.shellCommandOnRegion,
            'suspend':                      self.suspend,
        }
    #@nonl
    #@-node:ekr.20050920084036.152: getPublicCommands
    #@+node:ekr.20050922110030:advertizedUndo
    def advertizedUndo (self,event):
    
        self.c.undoer.undo()
    #@nonl
    #@-node:ekr.20050922110030:advertizedUndo
    #@+node:ekr.20050920084036.160:executeSubprocess
    def executeSubprocess (self,event,command,input):
        
        k = self.k ; w = event.widget
        k.setLabelBlue('started  shell-command: %s' % command)
    
        try:
            ofile = os.tmpfile()
            efile = os.tmpfile()
            process = subprocess.Popen(command,bufsize=-1,
                stdout = ofile.fileno(), stderr = ofile.fileno(),
                stdin = subprocess.PIPE, shell = True)
            if input: process.communicate(input)
            process.wait()
            efile.seek(0)
            errinfo = efile.read()
            if errinfo: w.insert('insert',errinfo)
            ofile.seek(0)
            okout = ofile.read()
            if okout: w.insert('insert',okout)
        except Exception, x:
            w = event.widget
            w.insert('insert',x)
            
        k.setLabelGrey('finished shell-command: %s' % command)
    #@nonl
    #@-node:ekr.20050920084036.160:executeSubprocess
    #@+node:ekr.20050920084036.158:shellCommand
    def shellCommand (self,event):
    
        if subprocess:
            k = self.k ; state = k.getState('shell-command')
        
            if state == 0:
                k.setLabelBlue('shell-command: ',protect=True)
                k.getArg(event,'shell-command',1,self.shellCommand)
            else:
                command = k.arg
                k.commandName = 'shell-command: %s' % command
                k.clearState()
                self.executeSubprocess(event,command,input=None)
        else:
            k.setLabelGrey('can not execute shell-command: can not import subprocess')
    #@nonl
    #@-node:ekr.20050920084036.158:shellCommand
    #@+node:ekr.20050930112126:shellCommandOnRegion
    def shellCommandOnRegion (self,event):
    
        if subprocess:
            k = self.k ; is1,is2 = None,None ; w = event.widget
            try:
                is1 = w.index('sel.first')
                is2 = w.index('sel.last')
            finally:
                if is1:
                    command = w.get(is1,is2)
                    k.commandName = 'shell-command: %s' % command
                    self.executeSubprocess(event,command,input=None)
                else:
                    k.clearState()
                    k.resetLabel()
        else:
            k.setLabelGrey('can not execute shell-command: can not import subprocess')
        
    #@nonl
    #@-node:ekr.20050930112126:shellCommandOnRegion
    #@+node:ekr.20050920084036.155:shutdown, saveBuffersKillEmacs & setShutdownHook
    def shutdown (self,event):
        
        g.app.onQuit()
            
    saveBuffersKillLeo = shutdown
    #@nonl
    #@-node:ekr.20050920084036.155:shutdown, saveBuffersKillEmacs & setShutdownHook
    #@+node:ekr.20050920084036.153:suspend & iconifyOrDeiconifyFrame
    def suspend (self,event):
    
        w = event.widget
        w.winfo_toplevel().iconify()
        
    # Must be a separate function so that k.inverseCommandsDict will be a true inverse.
        
    def iconifyFrame (self,event):
        self.suspend(event)
    #@-node:ekr.20050920084036.153:suspend & iconifyOrDeiconifyFrame
    #@-others
#@nonl
#@-node:ekr.20050920084036.150:class controlCommandsClass
#@+node:ekr.20060127162818.1:class debugCommandsClass
class debugCommandsClass (baseEditCommandsClass):
    
    #@    @+others
    #@+node:ekr.20060127162921: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    #@nonl
    #@-node:ekr.20060127162921: ctor
    #@+node:ekr.20060205050659:collectGarbage
    def collectGarbage (self,event=None):
        
        g.collectGarbage()
    #@nonl
    #@-node:ekr.20060205050659:collectGarbage
    #@+node:ekr.20060127163325: getPublicCommands
    def getPublicCommands (self):
        
        k = self
    
        return {
            'collect-garbage':      self.collectGarbage,
            'disable-gc-trace':     self.disableGcTrace,
            'dump-all-objects':     self.dumpAllObjects,
            'dump-new-objects':     self.dumpNewObjects,
            'enable-gc-trace':      self.enableGcTrace,
            'free-tree-widgets':    self.freeTreeWidgets,
            'print-focus':          self.printFocus,
            'print-stats':          self.printStats,
            'print-gc-summary':     self.printGcSummary,
            'run-unit-tests':       self.runUnitTests,
            'verbose-dump-objects': self.verboseDumpObjects,
        }
    #@nonl
    #@-node:ekr.20060127163325: getPublicCommands
    #@+node:ekr.20060202160523:dumpAll/New/VerboseObjects
    def dumpAllObjects (self,event=None):
        
        old = g.app.trace_gc
        g.app.trace_gc = True
        g.printGcAll()
        g.app.trace_gc = old
        
    def dumpNewObjects (self,event=None):
    
        old = g.app.trace_gc
        g.app.trace_gc = True
        g.printGcObjects()
        g.app.trace_gc = old
        
    def verboseDumpObjects (self,event=None):
        
        old = g.app.trace_gc
        g.app.trace_gc = True
        g.printGcVerbose()
        g.app.trace_gc = old
    #@-node:ekr.20060202160523:dumpAll/New/VerboseObjects
    #@+node:ekr.20060127163325.1:enable/disableGcTrace
    def disableGcTrace (self,event=None):
        
        g.app.trace_gc = False
        
    def enableGcTrace (self,event=None):
        
        g.app.trace_gc = True
        g.app.trace_gc_inited = False
        g.enable_gc_debug()
    #@nonl
    #@-node:ekr.20060127163325.1:enable/disableGcTrace
    #@+node:ekr.20060202154734:freeTreeWidgets
    def freeTreeWidgets (self,event=None):
        
        c = self.c
        
        c.frame.tree.destroyWidgets()
        c.redraw_now()
    #@nonl
    #@-node:ekr.20060202154734:freeTreeWidgets
    #@+node:ekr.20060210100432:printFocus
    # Doesn't work if the focus isn't in a pane with bindings!
    
    def printFocus (self,event=None):
        
        c = self.c
        
        g.es_print('      hasFocusWidget: %s' % c.widget_name(c.hasFocusWidget))
        g.es_print('requestedFocusWidget: %s' % c.widget_name(c.requestedFocusWidget))
        g.es_print('           get_focus: %s' % c.widget_name(c.get_focus()))
    #@nonl
    #@-node:ekr.20060210100432:printFocus
    #@+node:ekr.20060205043324.3:printGcSummary
    def printGcSummary (self,event=None):
    
        g.printGcSummary()
    #@nonl
    #@-node:ekr.20060205043324.3:printGcSummary
    #@+node:ekr.20060202133313:printStats
    def printStats (self,event=None):
        
        c = self.c
        c.frame.tree.showStats()
        self.dumpAllObjects()
    #@nonl
    #@-node:ekr.20060202133313:printStats
    #@+node:ekr.20060328121145:runUnitTest
    def runUnitTests (self,event=None):
        
        '''Run all unit tests contained in the presently selected outline.'''
        
        c = self.c
    
        leoTest.doTests(c,all=False)
    #@nonl
    #@-node:ekr.20060328121145:runUnitTest
    #@-others
#@nonl
#@-node:ekr.20060127162818.1:class debugCommandsClass
#@+node:ekr.20050920084036.53:class editCommandsClass
class editCommandsClass (baseEditCommandsClass):
    
    '''Contains editing commands with little or no state.'''

    #@    @+others
    #@+node:ekr.20050929155208: birth
    #@+node:ekr.20050920084036.54: ctor (editCommandsClass)
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.ccolumn = '0'   # For comment column functions.
        self.dynaregex = re.compile(r'[%s%s\-_]+'%(string.ascii_letters,string.digits))
            # For dynamic abbreviations
        self.extendMode = False # True: all cursor move commands extend the selection.
        self.fillPrefix = '' # For fill prefix functions.
        self.fillColumn = 70 # For line centering.
        self.moveSpotNode = None # A tnode.
        self.moveSpot = None # For retaining preferred column when moving up or down.
        self.moveCol = None # For retaining preferred column when moving up or down.
        self.store ={'rlist':[], 'stext':''} # For dynamic expansion.
        self.swapSpots = []
        self._useRegex = False # For replace-string
        self.widget = None # For use by state handlers.
    #@nonl
    #@-node:ekr.20050920084036.54: ctor (editCommandsClass)
    #@+node:ekr.20050920084036.55: getPublicCommands (editCommandsClass)
    def getPublicCommands (self):        
    
        c = self.c ; k = self.k
    
        return {
            'activate-cmds-menu':                   self.activateCmdsMenu,
            'activate-edit-menu':                   self.activateEditMenu,
            'activate-file-menu':                   self.activateFileMenu,
            'activate-help-menu':                   self.activateHelpMenu,
            'activate-outline-menu':                self.activateOutlineMenu,
            'activate-plugins-menu':                self.activatePluginsMenu,
            'activate-window-menu':                 self.activateWindowMenu,        
            'back-to-indentation':                  self.backToIndentation,
            'back-char':                            self.backCharacter,
            'back-char-extend-selection':           self.backCharacterExtendSelection,
            'back-paragraph':                       self.backwardParagraph,
            'back-paragraph-extend-selection':      self.backwardParagraphExtendSelection,
            'back-sentence':                        self.backSentence,
            'back-sentence-extend-selection':       self.backSentenceExtendSelection,
            'back-word':                            self.backwardWord,
            'back-word-extend-selection':           self.backwardWordExtendSelection,
            'backward-delete-char':                 self.backwardDeleteCharacter,
            'backward-kill-paragraph':              self.backwardKillParagraph,
            'beginning-of-buffer':                  self.beginningOfBuffer,
            'beginning-of-buffer-extend-selection': self.beginningOfBufferExtendSelection,
            'beginning-of-line':                    self.beginningOfLine,
            'beginning-of-line-extend-selection':   self.beginningOfLineExtendSelection,
            'capitalize-word':                      self.capitalizeWord,
            'center-line':                          self.centerLine,
            'center-region':                        self.centerRegion,
            'clear-extend-mode':                    self.clearExtendMode,
            'click-click-box':                      self.clickClickBox,
            'click-headline':                       self.clickHeadline,
            'click-icon-box':                       self.clickIconBox,
            'contract-body-pane':                   c.frame.contractBodyPane,
            'contract-log-pane':                    c.frame.contractLogPane,
            'contract-outline-pane':                c.frame.contractOutlinePane,
            'contract-pane':                        c.frame.contractPane,
            'count-region':                         self.countRegion,
            'cycle-focus':                          self.cycleFocus,
            'dabbrev-completion':                   self.dynamicExpansion2,
            'dabbrev-expands':                      self.dynamicExpansion,
            'delete-char':                          self.deleteNextChar,
            'delete-indentation':                   self.deleteIndentation,
            'delete-spaces':                        self.deleteSpaces,
            'downcase-region':                      self.downCaseRegion,
            'downcase-word':                        self.downCaseWord,
            'double-click-headline':                self.doubleClickHeadline,
            'double-click-icon-box':                self.doubleClickIconBox,
            'end-of-buffer':                        self.endOfBuffer,
            'end-of-buffer-extend-selection':       self.endOfBufferExtendSelection,
            'end-of-line':                          self.endOfLine,
            'end-of-line-extend-selection':         self.endOfLineExtendSelection,
            'escape':                               self.watchEscape,
            'eval-expression':                      self.evalExpression,
            'exchange-point-mark':                  self.exchangePointMark,
            'expand-body-pane':                     c.frame.expandBodyPane,
            'expand-log-pane':                      c.frame.expandLogPane,
            'expand-outline-pane':                  c.frame.expandOutlinePane,
            'expand-pane':                          c.frame.expandPane,
            'fill-paragraph':                       self.fillParagraph,
            'fill-region':                          self.fillRegion,
            'fill-region-as-paragraph':             self.fillRegionAsParagraph,
            'flush-lines':                          self.flushLines,
            'focus-to-body':                        self.focusToBody,
            'focus-to-log':                         self.focusToLog,
            'focus-to-minibuffer':                  self.focusToMinibuffer,
            'focus-to-tree':                        self.focusToTree,
            'forward-char':                         self.forwardCharacter,
            'forward-char-extend-selection':        self.forwardCharacterExtendSelection,
            'forward-paragraph':                    self.forwardParagraph,
            'forward-paragraph-extend-selection':   self.forwardParagraphExtendSelection,
            'forward-sentence':                     self.forwardSentence,
            'forward-sentence-extend-selection':    self.forwardSentenceExtendSelection,
            'forward-word':                         self.forwardWord,
            'forward-word-extend-selection':        self.forwardWordExtendSelection,
            'fully-expand-body-pane':               c.frame.fullyExpandBodyPane,
            'fully-expand-log-pane':                c.frame.fullyExpandLogPane,
            'fully-expand-pane':                    c.frame.fullyExpandPane,
            'fully-expand-outline-pane':            c.frame.fullyExpandOutlinePane,
            'goto-char':                            self.gotoCharacter,
            'goto-line':                            self.gotoLine,
            'hide-body-pane':                       c.frame.hideBodyPane,
            'hide-log-pane':                        c.frame.hideLogPane,
            'hide-pane':                            c.frame.hidePane,
            'hide-outline-pane':                    c.frame.hideOutlinePane,
            'how-many':                             self.howMany,
            # Use indentBody in leoCommands.py
            'indent-relative':                      self.indentRelative,
            'indent-rigidly':                       self.tabIndentRegion,
            'indent-to-comment-column':             self.indentToCommentColumn,
            'insert-newline':                       self.insertNewline,
            'insert-parentheses':                   self.insertParentheses,
            'keep-lines':                           self.keepLines,
            'kill-paragraph':                       self.killParagraph,
            'line-number':                          self.lineNumber,
            'move-past-close':                      self.movePastClose,
            'move-past-close-extend-selection':     self.movePastCloseExtendSelection,
            'newline-and-indent':                   self.insertNewLineAndTab,
            'next-line':                            self.nextLine,
            'next-line-extend-selection':           self.nextLineExtendSelection,
            'previous-line':                        self.prevLine,
            'previous-line-extend-selection':       self.prevLineExtendSelection,
            'remove-blank-lines':                   self.removeBlankLines,
            'reverse-region':                       self.reverseRegion,
            'scroll-down':                          self.scrollDown,
            'scroll-down-extend-selection':         self.scrollDownExtendSelection,
            'scroll-outline-down-line':             self.scrollOutlineDownLine,
            'scroll-outline-down-page':             self.scrollOutlineDownPage,
            'scroll-outline-up-line':               self.scrollOutlineUpLine,
            'scroll-outline-up-page':               self.scrollOutlineUpPage,
            'scroll-up':                            self.scrollUp,
            'scroll-up-extend-selection':           self.scrollUpExtendSelection,
            'select-paragraph':                     self.selectParagraph,
            # Exists, but can not be executed via the minibuffer.
            # 'self-insert-command':                self.selfInsertCommand,
            'set-comment-column':                   self.setCommentColumn,
            'set-extend-mode':                      self.setExtendMode,
            'set-fill-column':                      self.setFillColumn,
            'set-fill-prefix':                      self.setFillPrefix,
            'set-mark-command':                     self.setRegion,
            'show-colors':                          self.showColors,
            'show-fonts':                           self.showFonts,
            'simulate-begin-drag':                  self.simulateBeginDrag,
            'simulate-end-drag':                    self.simulateEndDrag,
            'sort-columns':                         self.sortColumns,
            'sort-fields':                          self.sortFields,
            'sort-lines':                           self.sortLines,
            'split-line':                           self.insertNewLineIndent,
            'tabify':                               self.tabify,
            'toggle-extend-mode':                   self.toggleExtendMode,
            'transpose-chars':                      self.transposeCharacters,
            'transpose-lines':                      self.transposeLines,
            'transpose-words':                      self.transposeWords,
            'untabify':                             self.untabify,
            'upcase-region':                        self.upCaseRegion,
            'upcase-word':                          self.upCaseWord,
            'view-lossage':                         self.viewLossage,
            'what-line':                            self.whatLine,
        }
    #@-node:ekr.20050920084036.55: getPublicCommands (editCommandsClass)
    #@-node:ekr.20050929155208: birth
    #@+node:ekr.20050920084036.57:capitalization & case
    #@+node:ekr.20051015114221:capitalizeWord & up/downCaseWord
    def capitalizeWord (self,event):
        self.capitalizeHelper(event,'cap')
    
    def downCaseWord (self,event):
        self.capitalizeHelper(event,'low')
    
    def upCaseWord (self,event):
        self.capitalizeHelper(event,'up')
    #@nonl
    #@-node:ekr.20051015114221:capitalizeWord & up/downCaseWord
    #@+node:ekr.20050920084036.145:changePreviousWord
    def changePreviousWord (self,event):
    
        k = self.k ; stroke = k.stroke ; w = event.widget
        i = w.index('insert')
    
        self.moveWordHelper(event,extend=False,forward=False)
    
        if stroke == '<Alt-c>':
            self.capitalizeWord(event)
        elif stroke == '<Alt-u>':
             self.upCaseWord(event)
        elif stroke == '<Alt-l>':
            self.downCaseWord(event)
    
        w.mark_set('insert',i)
    #@nonl
    #@-node:ekr.20050920084036.145:changePreviousWord
    #@+node:ekr.20051015114221.1:capitalizeHelper
    def capitalizeHelper (self,event,which):
    
        w = event.widget
        text = w.get('insert wordstart','insert wordend')
        i = w.index('insert')
        if text == ' ': return
        w.delete('insert wordstart','insert wordend')
        if which == 'cap':
            text = text.capitalize()
        if which == 'low':
            text = text.lower()
        if which == 'up':
            text = text.upper()
        w.insert('insert',text)
        w.mark_set('insert',i)
        
    #@-node:ekr.20051015114221.1:capitalizeHelper
    #@-node:ekr.20050920084036.57:capitalization & case
    #@+node:ekr.20051022142249:clicks and focus (editCommandsClass)
    #@+node:ekr.20060211100905:activate-x-menu & activateMenu (editCommandsClass)
    def activateCmdsMenu    (self,event=None): self.activateMenu('Cmds')
    def activateEditMenu    (self,event=None): self.activateMenu('Edit')
    def activateFileMenu    (self,event=None): self.activateMenu('File')
    def activateHelpMenu    (self,event=None): self.activateMenu('Help')
    def activateOutlineMenu (self,event=None): self.activateMenu('Outline')
    def activatePluginsMenu (self,event=None): self.activateMenu('Plugins')
    def activateWindowMenu  (self,event=None): self.activateMenu('Window')
    
    def activateMenu (self,menuName):
        c = self.c
        c.frame.menu.activateMenu(menuName)
    #@nonl
    #@-node:ekr.20060211100905:activate-x-menu & activateMenu (editCommandsClass)
    #@+node:ekr.20051022144825.1:cycleFocus
    def cycleFocus (self,event):
    
        c = self.c
        
        body = c.frame.body.bodyCtrl
        log  = c.frame.log.logCtrl
        tree = c.frame.tree.canvas
    
        panes = [body,log,tree]
    
        for w in panes:
            if w == event.widget:
                i = panes.index(w)
                if i >= len(panes) - 1:
                    i = 0
                else:
                    i += 1
                pane = panes[i] ; break
        else:
            # Assume we were somewhere in the tree.
            pane = body
            
        # g.trace(pane)
        c.set_focus(pane)
    #@nonl
    #@-node:ekr.20051022144825.1:cycleFocus
    #@+node:ekr.20051022144825:focusTo...
    def focusToBody (self,event):
        
        self.c.bodyWantsFocus()
    
    def focusToLog (self,event):
    
        self.c.logWantsFocus()
        
    def focusToMinibuffer (self,event):
        
        self.c.minibufferWantsFocus()
    
    def focusToTree (self,event):
        
        self.c.treeWantsFocus()
    #@nonl
    #@-node:ekr.20051022144825:focusTo...
    #@+node:ekr.20060211063744.1:clicks in the headline
    # These call the actual event handlers so as to trigger hooks.
    
    def clickHeadline (self,event=None):
    
        '''Simulate a click in the icon box of the presently selected headline.'''
        c = self.c ; p = c.currentPosition()
        c.frame.tree.onHeadlineClick(event,p=p)
        
    def doubleClickHeadline (self,event=None):
        return self.clickHeadline(event)
    
    def rightClickHeadline (self,event=None):
    
        '''Simulate a double-click in the icon box of the presently selected headline.'''
        c = self.c ; p = c.currentPosition()
        c.frame.tree.onHeadlineRightClick(event,p=p)
    #@nonl
    #@-node:ekr.20060211063744.1:clicks in the headline
    #@+node:ekr.20060211055455:clicks in the icon box
    # These call the actual event handlers so as to trigger hooks.
    
    def clickIconBox (self,event=None):
    
        '''Simulate a click in the icon box of the presently selected headline.'''
        c = self.c ; p = c.currentPosition()
        c.frame.tree.onIconBoxClick(event,p=p)
    
    def doubleClickIconBox (self,event=None):
    
        '''Simulate a double-click in the icon box of the presently selected headline.'''
        c = self.c ; p = c.currentPosition()
        c.frame.tree.onIconBoxDoubleClick(event,p=p)
    
    def rightClickIconBox (self,event=None):
    
        '''Simulate a right click in the icon box of the presently selected headline.'''
        c = self.c ; p = c.currentPosition()
        c.frame.tree.onIconBoxRightClick(event,p=p)
    #@nonl
    #@-node:ekr.20060211055455:clicks in the icon box
    #@+node:ekr.20060211062025:clickClickBox
    # Call the actual event handlers so as to trigger hooks.
    
    def clickClickBox (self,event=None):
    
        '''Simulate a click in the click box (+- box) of the presently selected headline.'''
    
        c = self.c ; p = c.currentPosition()
        c.frame.tree.onClickBoxClick(event,p=p)
    #@nonl
    #@-node:ekr.20060211062025:clickClickBox
    #@+node:ekr.20060211063744.2:simulate...Drag
    # These call the drag setup methods which in turn trigger hooks.
    
    def simulateBeginDrag (self,event=None):
    
        '''Simulate the start of a drag in the presently selected headline.'''
        c = self.c ; p = c.currentPosition()
        c.frame.tree.startDrag(event,p=p)
    
    def simulateEndDrag (self,event=None):
    
        '''Simulate the end of a drag in the presently selected headline.'''
        c = self.c
        
        # Note: this assumes that tree.startDrag has already been called.
        c.frame.tree.endDrag(event)
    #@nonl
    #@-node:ekr.20060211063744.2:simulate...Drag
    #@-node:ekr.20051022142249:clicks and focus (editCommandsClass)
    #@+node:ekr.20051019183105:color & font
    #@+node:ekr.20051019183105.1:show-colors
    def showColors (self,event):
        
        c = self.c ; log = c.frame.log ; tabName = 'Colors'
        
        #@    << define colors >>
        #@+node:ekr.20051019183105.2:<< define colors >>
        colors = (
            "gray60", "gray70", "gray80", "gray85", "gray90", "gray95",
            "snow1", "snow2", "snow3", "snow4", "seashell1", "seashell2",
            "seashell3", "seashell4", "AntiqueWhite1", "AntiqueWhite2", "AntiqueWhite3",
            "AntiqueWhite4", "bisque1", "bisque2", "bisque3", "bisque4", "PeachPuff1",
            "PeachPuff2", "PeachPuff3", "PeachPuff4", "NavajoWhite1", "NavajoWhite2",
            "NavajoWhite3", "NavajoWhite4", "LemonChiffon1", "LemonChiffon2",
            "LemonChiffon3", "LemonChiffon4", "cornsilk1", "cornsilk2", "cornsilk3",
            "cornsilk4", "ivory1", "ivory2", "ivory3", "ivory4", "honeydew1", "honeydew2",
            "honeydew3", "honeydew4", "LavenderBlush1", "LavenderBlush2",
            "LavenderBlush3", "LavenderBlush4", "MistyRose1", "MistyRose2",
            "MistyRose3", "MistyRose4", "azure1", "azure2", "azure3", "azure4",
            "SlateBlue1", "SlateBlue2", "SlateBlue3", "SlateBlue4", "RoyalBlue1",
            "RoyalBlue2", "RoyalBlue3", "RoyalBlue4", "blue1", "blue2", "blue3", "blue4",
            "DodgerBlue1", "DodgerBlue2", "DodgerBlue3", "DodgerBlue4", "SteelBlue1",
            "SteelBlue2", "SteelBlue3", "SteelBlue4", "DeepSkyBlue1", "DeepSkyBlue2",
            "DeepSkyBlue3", "DeepSkyBlue4", "SkyBlue1", "SkyBlue2", "SkyBlue3",
            "SkyBlue4", "LightSkyBlue1", "LightSkyBlue2", "LightSkyBlue3",
            "LightSkyBlue4", "SlateGray1", "SlateGray2", "SlateGray3", "SlateGray4",
            "LightSteelBlue1", "LightSteelBlue2", "LightSteelBlue3",
            "LightSteelBlue4", "LightBlue1", "LightBlue2", "LightBlue3",
            "LightBlue4", "LightCyan1", "LightCyan2", "LightCyan3", "LightCyan4",
            "PaleTurquoise1", "PaleTurquoise2", "PaleTurquoise3", "PaleTurquoise4",
            "CadetBlue1", "CadetBlue2", "CadetBlue3", "CadetBlue4", "turquoise1",
            "turquoise2", "turquoise3", "turquoise4", "cyan1", "cyan2", "cyan3", "cyan4",
            "DarkSlateGray1", "DarkSlateGray2", "DarkSlateGray3",
            "DarkSlateGray4", "aquamarine1", "aquamarine2", "aquamarine3",
            "aquamarine4", "DarkSeaGreen1", "DarkSeaGreen2", "DarkSeaGreen3",
            "DarkSeaGreen4", "SeaGreen1", "SeaGreen2", "SeaGreen3", "SeaGreen4",
            "PaleGreen1", "PaleGreen2", "PaleGreen3", "PaleGreen4", "SpringGreen1",
            "SpringGreen2", "SpringGreen3", "SpringGreen4", "green1", "green2",
            "green3", "green4", "chartreuse1", "chartreuse2", "chartreuse3",
            "chartreuse4", "OliveDrab1", "OliveDrab2", "OliveDrab3", "OliveDrab4",
            "DarkOliveGreen1", "DarkOliveGreen2", "DarkOliveGreen3",
            "DarkOliveGreen4", "khaki1", "khaki2", "khaki3", "khaki4",
            "LightGoldenrod1", "LightGoldenrod2", "LightGoldenrod3",
            "LightGoldenrod4", "LightYellow1", "LightYellow2", "LightYellow3",
            "LightYellow4", "yellow1", "yellow2", "yellow3", "yellow4", "gold1", "gold2",
            "gold3", "gold4", "goldenrod1", "goldenrod2", "goldenrod3", "goldenrod4",
            "DarkGoldenrod1", "DarkGoldenrod2", "DarkGoldenrod3", "DarkGoldenrod4",
            "RosyBrown1", "RosyBrown2", "RosyBrown3", "RosyBrown4", "IndianRed1",
            "IndianRed2", "IndianRed3", "IndianRed4", "sienna1", "sienna2", "sienna3",
            "sienna4", "burlywood1", "burlywood2", "burlywood3", "burlywood4", "wheat1",
            "wheat2", "wheat3", "wheat4", "tan1", "tan2", "tan3", "tan4", "chocolate1",
            "chocolate2", "chocolate3", "chocolate4", "firebrick1", "firebrick2",
            "firebrick3", "firebrick4", "brown1", "brown2", "brown3", "brown4", "salmon1",
            "salmon2", "salmon3", "salmon4", "LightSalmon1", "LightSalmon2",
            "LightSalmon3", "LightSalmon4", "orange1", "orange2", "orange3", "orange4",
            "DarkOrange1", "DarkOrange2", "DarkOrange3", "DarkOrange4", "coral1",
            "coral2", "coral3", "coral4", "tomato1", "tomato2", "tomato3", "tomato4",
            "OrangeRed1", "OrangeRed2", "OrangeRed3", "OrangeRed4", "red1", "red2", "red3",
            "red4", "DeepPink1", "DeepPink2", "DeepPink3", "DeepPink4", "HotPink1",
            "HotPink2", "HotPink3", "HotPink4", "pink1", "pink2", "pink3", "pink4",
            "LightPink1", "LightPink2", "LightPink3", "LightPink4", "PaleVioletRed1",
            "PaleVioletRed2", "PaleVioletRed3", "PaleVioletRed4", "maroon1",
            "maroon2", "maroon3", "maroon4", "VioletRed1", "VioletRed2", "VioletRed3",
            "VioletRed4", "magenta1", "magenta2", "magenta3", "magenta4", "orchid1",
            "orchid2", "orchid3", "orchid4", "plum1", "plum2", "plum3", "plum4",
            "MediumOrchid1", "MediumOrchid2", "MediumOrchid3", "MediumOrchid4",
            "DarkOrchid1", "DarkOrchid2", "DarkOrchid3", "DarkOrchid4", "purple1",
            "purple2", "purple3", "purple4", "MediumPurple1", "MediumPurple2",
            "MediumPurple3", "MediumPurple4", "thistle1", "thistle2", "thistle3",
            "thistle4" )
        #@nonl
        #@-node:ekr.20051019183105.2:<< define colors >>
        #@nl
        
        if log.frameDict.get(tabName):
            log.selectTab(tabName)
        else:
            log.selectTab(tabName)
            t = log.textDict.get(tabName)
            t.pack_forget()
            f = log.frameDict.get(tabName)
            self.createColorPicker(f,colors)
    #@+node:ekr.20051019183105.3:createColorPicker
    def createColorPicker (self,parent,colors):
        
        colors = list(colors)
        bg = parent.cget('background')
        
        outer = Tk.Frame(parent,background=bg)
        outer.pack(side='top',fill='both',expand=1,pady=10)
        
        f = Tk.Frame(outer)
        f.pack(side='top',expand=0,fill='x')
        f1 = Tk.Frame(f) ; f1.pack(side='top',expand=0,fill='x')
        f2 = Tk.Frame(f) ; f2.pack(side='top',expand=1,fill='x')
        f3 = Tk.Frame(f) ; f3.pack(side='top',expand=1,fill='x')
        
        label = Tk.Text(f1,height=1,width=20)
        label.insert('1.0','Color name or value...')
        label.pack(side='left',pady=6)
    
        #@    << create optionMenu and callback >>
        #@+node:ekr.20051019183105.4:<< create optionMenu and callback >>
        colorBox = Pmw.ComboBox(f2,scrolledlist_items=colors)
        colorBox.pack(side='left',pady=4)
        
        def colorCallback (newName): 
            label.delete('1.0','end')
            label.insert('1.0',newName)
            try:
                for theFrame in (parent,outer,f,f1,f2,f3):
                    theFrame.configure(background=newName)
            except: pass # Ignore invalid names.
        
        colorBox.configure(selectioncommand=colorCallback)
        #@nonl
        #@-node:ekr.20051019183105.4:<< create optionMenu and callback >>
        #@nl
        #@    << create picker button and callback >>
        #@+node:ekr.20051019183105.5:<< create picker button and callback >>
        def pickerCallback ():
            rgb,val = tkColorChooser.askcolor(parent=parent,initialcolor=f.cget('background'))
            if rgb or val:
                # label.configure(text=val)
                label.delete('1.0','end')
                label.insert('1.0',val)
                for theFrame in (parent,outer,f,f1,f2,f3):
                    theFrame.configure(background=val)
        
        b = Tk.Button(f3,text="Color Picker...",
            command=pickerCallback,background=bg)
        b.pack(side='left',pady=4)
        #@nonl
        #@-node:ekr.20051019183105.5:<< create picker button and callback >>
        #@nl
    #@nonl
    #@-node:ekr.20051019183105.3:createColorPicker
    #@-node:ekr.20051019183105.1:show-colors
    #@+node:ekr.20051019201809:show-fonts & helpers
    def showFonts (self,event):
    
        c = self.c ; log = c.frame.log ; tabName = 'Fonts'
    
        if log.frameDict.get(tabName):
            log.selectTab(tabName)
        else:
            log.selectTab(tabName)
            f = log.frameDict.get(tabName)
            t = log.textDict.get(tabName)
            t.pack_forget()
            self.createFontPicker(f)
    #@nonl
    #@+node:ekr.20051019201809.1:createFontPicker
    def createFontPicker (self,parent):
    
        bg = parent.cget('background')
        font = self.getFont()
        #@    << create the frames >>
        #@+node:ekr.20051019202139:<< create the frames >>
        f = Tk.Frame(parent,background=bg) ; f.pack (side='top',expand=0,fill='both')
        f1 = Tk.Frame(f,background=bg)     ; f1.pack(side='top',expand=1,fill='x')
        f2 = Tk.Frame(f,background=bg)     ; f2.pack(side='top',expand=1,fill='x')
        f3 = Tk.Frame(f,background=bg)     ; f3.pack(side='top',expand=1,fill='x')
        f4 = Tk.Frame(f,background=bg)     ; f4.pack(side='top',expand=1,fill='x')
        #@nonl
        #@-node:ekr.20051019202139:<< create the frames >>
        #@nl
        #@    << create the family combo box >>
        #@+node:ekr.20051019201809.2:<< create the family combo box >>
        names = tkFont.families()
        names = list(names)
        names.sort()
        names.insert(0,'<None>')
        
        familyBox = Pmw.ComboBox(f1,
            labelpos="we",label_text='Family:',label_width=10,
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=names)
        
        familyBox.selectitem(0)
        familyBox.pack(side="left",padx=2,pady=2)
        #@nonl
        #@-node:ekr.20051019201809.2:<< create the family combo box >>
        #@nl
        #@    << create the size entry >>
        #@+node:ekr.20051019201809.3:<< create the size entry >>
        Tk.Label(f2,text="Size:",width=10,background=bg).pack(side="left")
        
        sizeEntry = Tk.Entry(f2,width=4) ##,textvariable=sv)
        sizeEntry.pack(side="left",padx=2,pady=2)
        #@-node:ekr.20051019201809.3:<< create the size entry >>
        #@nl
        #@    << create the weight combo box >>
        #@+node:ekr.20051019201809.4:<< create the weight combo box >>
        weightBox = Pmw.ComboBox(f3,
            labelpos="we",label_text="Weight:",label_width=10,
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=['<None>','normal','bold'])
        
        weightBox.selectitem(0)
        weightBox.pack(side="left",padx=2,pady=2)
        #@nonl
        #@-node:ekr.20051019201809.4:<< create the weight combo box >>
        #@nl
        #@    << create the slant combo box >>
        #@+node:ekr.20051019201809.5:<< create the slant combo box>>
        slantBox = Pmw.ComboBox(f4,
            labelpos="we",label_text="Slant:",label_width=10,
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=['<None>','roman','italic'])
        
        slantBox.selectitem(0)
        slantBox.pack(side="left",padx=2,pady=2)
        #@nonl
        #@-node:ekr.20051019201809.5:<< create the slant combo box>>
        #@nl
        #@    << create the sample text widget >>
        #@+node:ekr.20051019202139.1:<< create the sample text widget >>
        sample = Tk.Text(f,height=20,width=80,font=font)
        sample.pack(side='left')
        
        s = 'The quick brown fox\njumped over the lazy dog.\n0123456789'
        sample.insert('1.0',s)
        #@nonl
        #@-node:ekr.20051019202139.1:<< create the sample text widget >>
        #@nl
        #@    << create and bind the callbacks >>
        #@+node:ekr.20051019202328:<< create and bind the callbacks >>
        def fontCallback(event=None):
            self.setFont(familyBox,sizeEntry,slantBox,weightBox,sample)
        
        for w in (familyBox,slantBox,weightBox):
            w.configure(selectioncommand=fontCallback)
        
        sizeEntry.bind('<Return>',fontCallback)
        #@nonl
        #@-node:ekr.20051019202328:<< create and bind the callbacks >>
        #@nl
    #@nonl
    #@-node:ekr.20051019201809.1:createFontPicker
    #@+node:ekr.20051019201809.6:getFont
    def getFont(self,family=None,size=12,slant='roman',weight='normal'):
        
        try:
            return tkFont.Font(family=family,size=size,slant=slant,weight=weight)
        except Exception:
            g.es("exception setting font")
            g.es("family,size,slant,weight:",family,size,slant,weight)
            # g.es_exception() # This just confuses people.
            return g.app.config.defaultFont
    #@nonl
    #@-node:ekr.20051019201809.6:getFont
    #@+node:ekr.20051019201809.7:setFont
    def setFont(self,familyBox,sizeEntry,slantBox,weightBox,label):
        
        d = {}
        for box,key in (
            (familyBox, 'family'),
            (None,      'size'),
            (slantBox,  'slant'),
            (weightBox, 'weight'),
        ):
            if box: val = box.get()
            else:
                val = sizeEntry.get().strip() or ''
                try: int(val)
                except ValueError: val = None
            if val and val.lower() not in ('none','<none>',):
                d[key] = val
    
        family=d.get('family',None)
        size=d.get('size',12)
        weight=d.get('weight','normal')
        slant=d.get('slant','roman')
        font = self.getFont(family,size,slant,weight)
        label.configure(font=font)
    #@nonl
    #@-node:ekr.20051019201809.7:setFont
    #@-node:ekr.20051019201809:show-fonts & helpers
    #@-node:ekr.20051019183105:color & font
    #@+node:ekr.20050920084036.132:comment column...
    #@+node:ekr.20050920084036.133:setCommentColumn
    def setCommentColumn (self,event):
    
        cc = event.widget.index('insert')
        cc1, cc2 = cc.split('.')
        self.ccolumn = cc2
    #@nonl
    #@-node:ekr.20050920084036.133:setCommentColumn
    #@+node:ekr.20050920084036.134:indentToCommentColumn
    def indentToCommentColumn (self,event):
    
        k = self.k ; w = event.widget
    
        i = w.index('insert lineend')
        i1, i2 = i.split('.')
        i2 = int(i2)
        c1 = int(self.ccolumn)
    
        if i2 < c1:
            wsn = c1- i2
            w.insert('insert lineend',' '*wsn)
        if i2 >= c1:
            w.insert('insert lineend',' ')
        w.mark_set('insert','insert lineend')
    #@nonl
    #@-node:ekr.20050920084036.134:indentToCommentColumn
    #@-node:ekr.20050920084036.132:comment column...
    #@+node:ekr.20050920084036.58:dynamic abbreviation...
    #@+node:ekr.20050920084036.59:dynamicExpansion
    def dynamicExpansion (self,event): #, store = {'rlist': [], 'stext': ''} ):
    
        k = self.k ; w = event.widget
        rlist = self.store ['rlist']
        stext = self.store ['stext']
        i = w.index('insert -1c wordstart')
        i2 = w.index('insert -1c wordend')
        txt = w.get(i,i2)
        dA = w.tag_ranges('dA')
        w.tag_delete('dA')
        def doDa (txt,from_='insert -1c wordstart',to_='insert -1c wordend'):
            w.delete(from_,to_)
            w.insert('insert',txt,'dA')
    
        if dA:
            dA1, dA2 = dA
            dtext = w.get(dA1,dA2)
            if dtext.startswith(stext) and i2 == dA2:
                #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
                if rlist:
                    txt = rlist.pop()
                else:
                    txt = stext
                    w.delete(dA1,dA2)
                    dA2 = dA1 # since the text is going to be reread, we dont want to include the last dynamic abbreviation
                    self.getDynamicList(w,txt,rlist)
                doDa(txt,dA1,dA2) ; return
            else: dA = None
    
        if not dA:
            self.store ['stext'] = txt
            self.store ['rlist'] = rlist = []
            self.getDynamicList(w,txt,rlist)
            if not rlist: return
            txt = rlist.pop()
            doDa(txt)
    #@-node:ekr.20050920084036.59:dynamicExpansion
    #@+node:ekr.20050920084036.60:dynamicExpansion2
    def dynamicExpansion2 (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert -1c wordstart')
        i2 = w.index('insert -1c wordend')
        txt = w.get(i,i2)
        rlist = []
        self.getDynamicList(w,txt,rlist)
        dEstring = reduce(g.longestCommonPrefix,rlist)
        if dEstring:
            w.delete(i,i2)
            w.insert(i,dEstring)
    #@nonl
    #@-node:ekr.20050920084036.60:dynamicExpansion2
    #@+node:ekr.20050920084036.61:getDynamicList (helper)
    def getDynamicList (self,w,txt,rlist):
    
         ttext = w.get('1.0','end')
         items = self.dynaregex.findall(ttext) #make a big list of what we are considering a 'word'
         if items:
             for word in items:
                 if not word.startswith(txt) or word == txt: continue #dont need words that dont match or == the pattern
                 if word not in rlist:
                     rlist.append(word)
                 else:
                     rlist.remove(word)
                     rlist.append(word)
    #@nonl
    #@-node:ekr.20050920084036.61:getDynamicList (helper)
    #@-node:ekr.20050920084036.58:dynamic abbreviation...
    #@+node:ekr.20050920084036.62:esc methods for Python evaluation
    #@+node:ekr.20050920084036.63:watchEscape (Revise)
    def watchEscape (self,event):
    
        k = self.k
    
        if not k.inState():
            k.setState('escape','start',handler=self.watchEscape)
            k.setLabelBlue('Esc ')
        elif k.getStateKind() == 'escape':
            state = k.getState('escape')
            hi1 = k.keysymHistory [0]
            hi2 = k.keysymHistory [1]
            if state == 'esc esc' and event.keysym == 'colon':
                self.evalExpression(event)
            elif state == 'evaluate':
                self.escEvaluate(event)
            elif hi1 == hi2 == 'Escape':
                k.setState('escape','esc esc')
                k.setLabel('Esc Esc -')
            elif event.keysym not in ('Shift_L','Shift_R'):
                k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20050920084036.63:watchEscape (Revise)
    #@+node:ekr.20050920084036.64:escEvaluate (Revise)
    def escEvaluate (self,event):
    
        k = self.k ; w = event.widget
    
        if k.getLabel() == 'Eval:':
            k.setLabel('')
    
        if event.keysym == 'Return':
            expression = k.getLabel()
            try:
                ok = False
                result = eval(expression,{},{})
                result = str(result)
                w.insert('insert',result)
                ok = True
            finally:
                k.keyboardQuit(event)
                if not ok:
                    k.setLabel('Error: Invalid Expression')
        else:
            k.updateLabel(event)
    #@nonl
    #@-node:ekr.20050920084036.64:escEvaluate (Revise)
    #@-node:ekr.20050920084036.62:esc methods for Python evaluation
    #@+node:ekr.20050920084036.65:evalExpression
    def evalExpression (self,event):
    
        k = self.k ; state = k.getState('eval-expression')
        
        if state == 0:
            k.setLabelBlue('Eval: ',protect=True)
            k.getArg(event,'eval-expression',1,self.evalExpression)
        else:
            k.clearState()
            try:
                e = k.arg
                result = str(eval(e,{},{}))
                k.setLabelGrey('Eval: %s -> %s' % (e,result))
            except Exception:
                k.setLabelGrey('Invalid Expression: %s' % e)
    #@nonl
    #@-node:ekr.20050920084036.65:evalExpression
    #@+node:ekr.20050920084036.66:fill column and centering
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
    #@+node:ekr.20050920084036.67:centerLine
    def centerLine (self,event):
    
        '''Centers line within current fillColumn'''
    
        k = self.k ; w = event.widget
    
        ind = w.index('insert linestart')
        txt = w.get('insert linestart','insert lineend')
        txt = txt.strip()
        if len(txt) >= self.fillColumn: return
    
        amount = (self.fillColumn-len(txt)) / 2
        ws = ' ' * amount
        col, nind = ind.split('.')
        ind = w.search('\w','insert linestart',regexp=True,stopindex='insert lineend')
        if ind:
            w.delete('insert linestart','%s' % ind)
            w.insert('insert linestart',ws)
    #@nonl
    #@-node:ekr.20050920084036.67:centerLine
    #@+node:ekr.20050920084036.68:setFillColumn
    def setFillColumn (self,event):
    
        k = self.k ; state = k.getState('set-fill-column')
        
        if state == 0:
            k.setLabelBlue('Set Fill Column: ')
            k.getArg(event,'set-fill-column',1,self.setFillColumn)
        else:
            k.clearState()
            try:
                n = int(k.arg)
                k.setLabelGrey('fill column is: %d' % n)
                k.commandName = 'set-fill-column %d' % n
            except ValueError:
                k.resetLabel()
    #@nonl
    #@-node:ekr.20050920084036.68:setFillColumn
    #@+node:ekr.20050920084036.69:centerRegion
    def centerRegion( self, event ):
    
        '''This method centers the current region within the fill column'''
    
        k = self.k ; w = event.widget
        start = w.index( 'sel.first linestart' )
        sindex , x = start.split( '.' )
        sindex = int( sindex )
        end = w.index( 'sel.last linestart' )
        eindex , x = end.split( '.' )
        eindex = int( eindex )
        while sindex <= eindex:
            txt = w.get( '%s.0 linestart' % sindex , '%s.0 lineend' % sindex )
            txt = txt.strip()
            if len( txt ) >= self.fillColumn:
                sindex = sindex + 1
                continue
            amount = ( self.fillColumn - len( txt ) ) / 2
            ws = ' ' * amount
            ind = w.search( '\w', '%s.0' % sindex, regexp = True, stopindex = '%s.0 lineend' % sindex )
            if not ind: 
                sindex = sindex + 1
                continue
            w.delete( '%s.0' % sindex , '%s' % ind )
            w.insert( '%s.0' % sindex , ws )
            sindex = sindex + 1
    #@nonl
    #@-node:ekr.20050920084036.69:centerRegion
    #@+node:ekr.20050920084036.70:setFillPrefix
    def setFillPrefix( self, event ):
    
        w = event.widget
        txt = w.get( 'insert linestart', 'insert' )
        self.fillPrefix = txt
    #@nonl
    #@-node:ekr.20050920084036.70:setFillPrefix
    #@+node:ekr.20050920084036.71:_addPrefix
    def _addPrefix (self,ntxt):
    
        ntxt = ntxt.split('.')
        ntxt = map(lambda a: self.fillPrefix+a,ntxt)
        ntxt = '.'.join(ntxt)
        return ntxt
    #@nonl
    #@-node:ekr.20050920084036.71:_addPrefix
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.66:fill column and centering
    #@+node:ekr.20050920084036.72:goto...
    #@+node:ekr.20050929115226:gotoCharacter
    def gotoCharacter (self,event):
        
        '''Put the cursor at the n'th character of the buffer.'''
    
        k = self.k ; state = k.getState('goto-char')
    
        if state == 0:
            self.widget = event.widget
            k.setLabelBlue('Goto character: ')
            k.getArg(event,'goto-char',1,self.gotoCharacter)
        else:
            n = k.arg ; w = self.widget
            if n.isdigit():
                w.mark_set('insert','1.0 +%sc' % n)
                w.see('insert')
            k.resetLabel()
            k.clearState()
    #@nonl
    #@-node:ekr.20050929115226:gotoCharacter
    #@+node:ekr.20050929124234:gotoLine
    def gotoLine (self,event):
        
        '''Put the cursor at the n'th line of the buffer.'''
    
        k = self.k ; state = k.getState('goto-line')
        
        if state == 0:
            self.widget = event.widget
            k.setLabelBlue('Goto line: ')
            k.getArg(event,'goto-line',1,self.gotoLine)
        else:
            n = k.arg ;  w = self.widget
            if n.isdigit():
                w.mark_set('insert','%s.0' % n)
                w.see('insert')
            k.resetLabel()
            k.clearState()
    #@nonl
    #@-node:ekr.20050929124234:gotoLine
    #@-node:ekr.20050920084036.72:goto...
    #@+node:ekr.20050920084036.74:indent... (To do: undo)
    #@+node:ekr.20050920084036.75:backToIndentation
    def backToIndentation (self,event):
        
        '''The back-to-indentation command, given anywhere on a line,
        positions the point at the first non-blank character on the line.'''
    
        w = event.widget
        i = w.index('insert linestart')
        i2 = w.search(r'\w',i,stopindex='%s lineend' % i,regexp=True)
        w.mark_set('insert',i2)
    #@nonl
    #@-node:ekr.20050920084036.75:backToIndentation
    #@+node:ekr.20050920084036.76:deleteIndentation
    def deleteIndentation (self,event):
    
        k = self.k ; w = event.widget
    
        txt = w.get('insert linestart','insert lineend')
        txt = ' %s' % txt.lstrip()
        w.delete('insert linestart','insert lineend +1c')
        i = w.index('insert - 1c')
        w.insert('insert -1c',txt)
        w.mark_set('insert',i)
    #@nonl
    #@-node:ekr.20050920084036.76:deleteIndentation
    #@+node:ekr.20050920084036.77:insertNewLineIndent
    def insertNewLineIndent (self,event):
    
        w = event.widget
        txt = w.get('insert linestart','insert lineend')
        txt = self.getWSString(txt)
        i = w.index('insert')
        w.insert(i,txt)
        w.mark_set('insert',i)
        self.insertNewLine(event)
    #@-node:ekr.20050920084036.77:insertNewLineIndent
    #@+node:ekr.20050920084036.78:indentRelative
    def indentRelative (self,event):
        
        '''The indent-relative command indents at the point based on the previous
        line (actually, the last non-empty line.) It inserts whitespace at the
        point, moving point, until it is underneath an indentation point in the
        previous line.
        
        An indentation point is the end of a sequence of whitespace or the end of
        the line. If the point is farther right than any indentation point in the
        previous line, the whitespace before point is deleted and the first
        indentation point then applicable is used. If no indentation point is
        applicable even then whitespace equivalent to a single tab is inserted.'''
        
        c = self.c ; undoType = 'Indent Relative'
        
        k = self.k ; w = event.widget
        i = w.index('insert')
        oldSel = (i,i)
        line, col = i.split('.')
        c2 = int(col)
        l2 = int(line) -1
        if l2 < 1: return
        txt = w.get('%s.%s' % (l2,c2),'%s.0 lineend' % l2)
        if len(txt) <= len(w.get('insert','insert lineend')):
            w.insert('insert','\t')
        else:
            reg = re.compile('(\s+)')
            ntxt = reg.split(txt)
            replace_word = re.compile('\w')
            for z in ntxt:
                if z.isspace():
                    w.insert('insert',z)
                    break
                else:
                    z = replace_word.subn(' ',z)
                    w.insert('insert',z[0])
                    
        i = w.index('insert')
        result = w.get('1.0','end')
        head = tail = oldYview = None
        c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview)
        w.mark_set('insert',i)
    #@nonl
    #@-node:ekr.20050920084036.78:indentRelative
    #@-node:ekr.20050920084036.74:indent... (To do: undo)
    #@+node:ekr.20050920084036.85:insert & delete...
    #@+node:ekr.20051026092433.1:backwardDeleteCharacter
    def backwardDeleteCharacter (self,event=None):
        
        c = self.c ; p = c.currentPosition()
        w = event and event.widget
        if not g.app.gui.isTextWidget(w):
            g.trace('*'*40,'Not a text widget',c.widget_name(w))
            return
        
        wname = c.widget_name(w)
        i,j = g.app.gui.getTextSelection(w)
        # g.trace(wname,i,j)
    
        if wname.startswith('body'):
            self.beginCommand()
            d = g.scanDirectives(c,p)
            tab_width = d.get("tabwidth",c.tab_width)
            changed = True
            if i != j:
                w.delete(i,j)
            elif i == '1.0':
                changed = False # Bug fix: 1/6/06 (after a5 released).
            elif tab_width > 0:
                w.delete('insert-1c')
            else:
                #@            << backspace with negative tab_width >>
                #@+node:ekr.20051026092746:<< backspace with negative tab_width >>
                s = prev = w.get("insert linestart","insert")
                n = len(prev)
                abs_width = abs(tab_width)
                
                # Delete up to this many spaces.
                n2 = (n % abs_width) or abs_width
                n2 = min(n,n2) ; count = 0
                
                while n2 > 0:
                    n2 -= 1
                    ch = prev[n-count-1]
                    if ch != ' ': break
                    else: count += 1
                
                # Make sure we actually delete something.
                w.delete("insert -%dc" % (max(1,count)),"insert")
                #@nonl
                #@-node:ekr.20051026092746:<< backspace with negative tab_width >>
                #@nl
            self.endCommand(changed=True,setLabel=False) # Necessary to make text changes stick.
        else:
            # No undo in this widget.
            if i != j:
                w.delete(i,j)
            elif i != '1.0':
                # Bug fix: 1/6/06 (after a5 released).
                # Do nothing at the start of the headline.
                w.delete('insert-1c')
    #@nonl
    #@-node:ekr.20051026092433.1:backwardDeleteCharacter
    #@+node:ekr.20050920084036.87:deleteNextChar
    def deleteNextChar (self,event):
    
        c = self.c ; w = event and event.widget
        if not g.app.gui.isTextWidget(w): return
    
        name = c.widget_name(w)
        i,j = g.app.gui.getTextSelection(w)
        end = w.index('end-1c')
        # g.trace(i,j,'end',w.index('end-1c'))
        
        if name.startswith('body'):
            self.beginCommand()
    
        changed = True
        if i != j:
            w.delete(i,j)
        elif j != end:
            w.delete(i)
        else:
            changed = False
            
        if name.startswith('body'):
            self.endCommand(changed=changed,setLabel=False)
    #@nonl
    #@-node:ekr.20050920084036.87:deleteNextChar
    #@+node:ekr.20050920084036.135:deleteSpaces
    def deleteSpaces (self,event,insertspace=False):
    
        c = self.c ; w = event and event.widget
        if not g.app.gui.isTextWidget(w): return
    
        name = c.widget_name(w)
        char = w.get('insert','insert + 1c ')
        if not char.isspace(): return
        
        if name.startswith('body'):
            oldText = w.get('1.0','end')
            oldSel = g.app.gui.getTextSelection(w)
            i = w.index('insert')
            wf = w.search(r'\w',i,stopindex='%s lineend' % i,regexp=True)
            wb = w.search(r'\w',i,stopindex='%s linestart' % i,regexp=True,backwards=True)
            if '' in (wf,wb): return
            w.delete('%s +1c' % wb,wf)
            if insertspace: w.insert('insert',' ')
            
            c.frame.body.onBodyChanged(undoType='delete-spaces',
                oldSel=oldSel,oldText=oldText,oldYview=None)
    #@nonl
    #@-node:ekr.20050920084036.135:deleteSpaces
    #@+node:ekr.20050920084036.141:removeBlankLines
    def removeBlankLines (self,event):
        
        '''The remove-blank-lines command removes lines containing nothing but
        whitespace. If there is a text selection, only lines within the selected
        text are affected; otherwise all blank lines in the selected node are
        affected.'''
        
        c = self.c ; undoType = 'Remove Blank Lines' ; p = c.currentPosition()
        result = []
        body = p.bodyString()
        hasSelection = c.frame.body.hasTextSelection()
        
        if hasSelection:
            head,lines,tail,oldSel,oldYview = c.getBodyLines()
            joinChar = '\n'
        else:
            head = tail = oldYview = None
            lines = g.splitLines(body)
            oldSel = ('1.0','1.0')
            joinChar = ''
    
        for line in lines:
            if line.strip():
                result.append(line)
    
        result = joinChar.join(result)
        
        if result != body:
            c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview)
    #@nonl
    #@-node:ekr.20050920084036.141:removeBlankLines
    #@+node:ekr.20050920084036.138:insertNewLine (not undoable)
    def insertNewLine (self,event):
    
        w = event.widget
        wname = g.app.gui.widget_name(w)
        
        if not wname.startswith('head'):
            w.insert('insert','\n')
    
    insertNewline = insertNewLine
    #@nonl
    #@-node:ekr.20050920084036.138:insertNewLine (not undoable)
    #@+node:ekr.20050920084036.86:insertNewLineAndTab
    def insertNewLineAndTab (self,event):
    
        '''Insert a newline and tab'''
    
        w = event.widget
        wname = g.app.gui.widget_name(w)
        
        if not wname.startswith('head'):
            w.insert('insert','\n\t')
    #@-node:ekr.20050920084036.86:insertNewLineAndTab
    #@+node:ekr.20050920084036.139:insertParentheses
    def insertParentheses (self,event):
    
        w = event.widget
        w.insert('insert','()')
        w.mark_set('insert','insert -1c')
    #@nonl
    #@-node:ekr.20050920084036.139:insertParentheses
    #@+node:ekr.20051125080855:selfInsertCommand
    def selfInsertCommand(self,event,action='insert'):
        
        '''Insert a character in the body pane.
        
        This is the default binding for all keys in the body pane.'''
        
        c = self.c ; p = c.currentPosition()
        ch = event and event.char or ''
        w = event and event.widget
        name = c.widget_name(w)
        oldSel =  name.startswith('body') and g.app.gui.getTextSelection(w)
        oldText = name.startswith('body') and p.bodyString()
        removeTrailing = None # A signal to compute it later.
        undoType = 'Typing'
        trace = c.config.getBool('trace_masterCommand')
        
        if trace: g.trace(name)
        
        if g.doHook("bodykey1",c=c,p=p,v=p,ch=ch,oldSel=oldSel,undoType=undoType):
            return "break" # The hook claims to have handled the event.
            
        if ch == '\t':
            removeTrailing = self.updateTab(p,w)
        elif ch == '\b':
            # This is correct: we only come here if there no bindngs for this key. 
            self.backwardDeleteCharacter(event)
        elif ch in ('\r','\n'):
            ch = '\n'
            #@        << handle newline >>
            #@+node:ekr.20051026171121:<< handle newline >>
            i,j = oldSel
            
            if i != j:
                # No auto-indent if there is selected text.
                w.delete(i,j)
                w.insert(i,ch)
            else:
                w.insert(i,ch)
                if c.frame.body.colorizer.useSyntaxColoring(p) and undoType != "Change":
                    # No auto-indent if in @nocolor mode or after a Change command.
                    removeTrailing = self.updateAutoIndent(p)
            #@nonl
            #@-node:ekr.20051026171121:<< handle newline >>
            #@nl
        elif ch in ('(',')','[',']','{','}') and c.config.getBool('autocomplete-brackets'):
            self.updateAutomatchBracket(p,w,ch,oldSel)
        elif ch: # Null chars must not delete the selection.
            i,j = oldSel
            if i != j:                  w.delete(i,j)
            elif action == 'overwrite': w.delete(i,'%s+1c' % i)
            w.insert(i,ch)                     
        else:
            return 'break' # New in 4.4a5: this method *always* returns 'break'
    
        # Update the text and handle undo.
        newText = g.app.gui.getAllText(w) # New in 4.4b3: converts to unicode.
        w.see(w.index('insert'))
        if newText != oldText:
            c.frame.body.onBodyChanged(undoType=undoType,
                oldSel=oldSel,oldText=oldText,oldYview=None,removeTrailing=removeTrailing)
                
        g.doHook("bodykey2",c=c,p=p,v=p,ch=ch,oldSel=oldSel,undoType=undoType)
        return 'break'
    #@nonl
    #@+node:ekr.20051027172949:updateAutomatchBracket
    def updateAutomatchBracket (self,p,w,ch,oldSel):
        
        # assert ch in ('(',')','[',']','{','}')
        
        c = self.c ; d = g.scanDirectives(c,p) ; i,j = oldSel
        language = d.get('language')
        
        if ch in ('(','[','{',):
            automatch = language not in ('plain',)
            if automatch:
                ch = ch + {'(':')','[':']','{':'}'}.get(ch)
            if i != j:
                w.delete(i,j)
            w.insert(i,ch)
            if automatch:
                w.mark_set('insert','insert-1c')
        else:
            ch2 = w.get('insert')
            if ch2 in (')',']','}'):
                w.mark_set('insert','insert+1c')
            else:
                if i != j:
                    w.delete(i,j)
                w.insert(i,ch)
    #@nonl
    #@-node:ekr.20051027172949:updateAutomatchBracket
    #@+node:ekr.20051026171121.1:udpateAutoIndent
    # By David McNab:
    def updateAutoIndent (self,p):
    
        c = self.c ; d = g.scanDirectives(c,p)
        tab_width = d.get("tabwidth",c.tab_width) # Get the previous line.
        s = c.frame.bodyCtrl.get("insert linestart - 1 lines","insert linestart -1c")
        # Add the leading whitespace to the present line.
        junk, width = g.skip_leading_ws_with_indent(s,0,tab_width)
        if s and len(s) > 0 and s [ -1] == ':':
            # For Python: increase auto-indent after colons.
            if c.frame.body.colorizer.scanColorDirectives(p) == "python":
                width += abs(tab_width)
        if c.config.getBool("smart_auto_indent"):
            # Determine if prev line has unclosed parens/brackets/braces
            brackets = [width] ; tabex = 0
            for i in range(0,len(s)):
                if s [i] == '\t':
                    tabex += tab_width-1
                if s [i] in '([{':
                    brackets.append(i+tabex+1)
                elif s [i] in '}])' and len(brackets) > 1:
                    brackets.pop()
            width = brackets.pop()
        ws = g.computeLeadingWhitespace(width,tab_width)
        if ws:
            c.frame.bodyCtrl.insert("insert",ws)
            removeTrailing = False
        else:
            removeTrailing = None
        return removeTrailing
    #@nonl
    #@-node:ekr.20051026171121.1:udpateAutoIndent
    #@+node:ekr.20051026092433:updateTab
    def updateTab (self,p,w):
    
        c = self.c ; d = g.scanDirectives(c,p)
        tab_width = d.get("tabwidth",c.tab_width)
        
        i,j = g.app.gui.getTextSelection(w)
        if i != j:
            w.delete(i,j)
        if tab_width > 0:
            w.insert("insert",'\t')
        else:
            # Get the preceeding characters.
            s = w.get("insert linestart","insert")
        
            # Compute n, the number of spaces to insert.
            width = g.computeWidth(s,tab_width)
            n = abs(tab_width) - (width % abs(tab_width))
            w.insert("insert",' ' * n)
    #@nonl
    #@-node:ekr.20051026092433:updateTab
    #@-node:ekr.20051125080855:selfInsertCommand
    #@-node:ekr.20050920084036.85:insert & delete...
    #@+node:ekr.20050920084036.79:info...
    #@+node:ekr.20050920084036.80:howMany
    def howMany (self,event):
        
        k = self.k ; w = event.widget ; state = k.getState('how-many')
        
        if state == 0:
            k.setLabelBlue('How many: ',protect = True)
            k.getArg(event,'how-many',1,self.howMany)
        else:
            k.clearState()
            s = w.get('1.0','end')
            reg = re.compile(k.arg)
            i = reg.findall(s)
            k.setLabelGrey('%s occurances of %s' % (len(i),k.arg))
    #@nonl
    #@-node:ekr.20050920084036.80:howMany
    #@+node:ekr.20050920084036.81:lineNumber
    def lineNumber (self,event):
    
        k = self.k ; w = event.widget
    
        i = w.index('insert')
        i1, i2 = i.split('.')
        c = w.get('insert','insert + 1c')
        txt = w.get('1.0','end')
        txt2 = w.get('1.0','insert')
        perc = len(txt) * .01
        perc = int(len(txt2)/perc)
        k.setLabelGrey('Char: %s point %s of %s(%s%s)  Column %s' % (c,len(txt2),len(txt),perc,'%',i1))
    #@nonl
    #@-node:ekr.20050920084036.81:lineNumber
    #@+node:ekr.20050920084036.83:viewLossage
    def viewLossage (self,event):
    
        k = self.k
        loss = ''.join(leoKeys.keyHandlerClass.lossage)
        k.setLabel(loss)
    #@nonl
    #@-node:ekr.20050920084036.83:viewLossage
    #@+node:ekr.20050920084036.84:whatLine
    def whatLine (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        i1, i2 = i.split('.')
        k.keyboardQuit(event)
        k.setLabel("Line %s" % i1)
    #@nonl
    #@-node:ekr.20050920084036.84:whatLine
    #@-node:ekr.20050920084036.79:info...
    #@+node:ekr.20050920084036.88:line...
    #@+node:ekr.20050920084036.90:flushLines
    def flushLines (self,event):
    
        '''Delete each line that contains a match for regexp, operating on the text after point.
    
        In Transient Mark mode, if the region is active, the command operates on the region instead.'''
    
        k = self.k ; state = k.getState('flush-lines')
        
        if state == 0:
            k.setLabelBlue('Flush lines regexp: ',protect=True)
            k.getArg(event,'flush-lines',1,self.flushLines)
        else:
            k.clearState()
            k.resetLabel()
            self.linesHelper(event,k.arg,'flush')
            k.commandName = 'flush-lines %s' % k.arg
    #@nonl
    #@-node:ekr.20050920084036.90:flushLines
    #@+node:ekr.20051002095724:keepLines
    def keepLines (self,event):
    
        '''Delete each line that does not contain a match for regexp, operating on the text after point.
    
        In Transient Mark mode, if the region is active, the command operates on the region instead.'''
    
        k = self.k ; state = k.getState('keep-lines')
        
        if state == 0:
            k.setLabelBlue('Keep lines regexp: ',protect=True)
            k.getArg(event,'keep-lines',1,self.keepLines)
        else:
            k.clearState()
            k.resetLabel()
            self.linesHelper(event,k.arg,'keep')
            k.commandName = 'keep-lines %s' % k.arg
    #@nonl
    #@-node:ekr.20051002095724:keepLines
    #@+node:ekr.20050920084036.92:linesHelper
    def linesHelper (self,event,pattern,which):
    
        k = self.k ; w = event.widget
       
        if w.tag_ranges('sel'):
            i = w.index('sel.first') ; end = w.index('sel.last')
        else:
             i = w.index('insert') ; end = 'end'
        txt = w.get(i,end)
        tlines = txt.splitlines(True)
        if which == 'flush':    keeplines = list(tlines)
        else:                   keeplines = []
    
        try:
            regex = re.compile(pattern)
            for n, z in enumerate(tlines):
                f = regex.findall(z)
                if which == 'flush' and f:
                    keeplines [n] = None
                elif f:
                    keeplines.append(z)
        except Exception, x:
            return
        if which == 'flush':
            keeplines = [x for x in keeplines if x != None]
        w.delete(i,end)
        w.insert(i,''.join(keeplines))
        w.mark_set('insert',i)
    #@nonl
    #@-node:ekr.20050920084036.92:linesHelper
    #@-node:ekr.20050920084036.88:line...
    #@+node:ekr.20050920084036.147:measure
    def measure (self,w):
        i = w.index('insert')
        i1, i2 = i.split('.')
        start = int(i1)
        watch = 0
        ustart = start
        pone = 1
        top = i
        bottom = i
        while pone:
            ustart = ustart-1
            if ustart < 0:
                break
            ds = '%s.0' % ustart
            pone = w.dlineinfo(ds)
            if pone:
                top = ds
                watch = watch + 1
        pone = 1
        ustart = start
        while pone:
            ustart = ustart + 1
            ds = '%s.0' % ustart
            pone = w.dlineinfo(ds)
            if pone:
                bottom = ds
                watch = watch + 1
    
        return watch, top, bottom
    #@nonl
    #@-node:ekr.20050920084036.147:measure
    #@+node:ekr.20050929114218:move... (leoEditCommands)
    #@+node:ekr.20051218170358: helpers
    #@+node:ekr.20060113130510:extendHelper
    def extendHelper (self,w,extend,ins1,spot,setSpot=True):
    
        '''Handle the details of extending the selection.
        
        extend: Clear the selection unless this is True.
        ins1:   The *previous* insert point.
        spot:   The *new* insert point.
        '''
        c = self.c ; p = c.currentPosition()
        moveSpot = self.moveSpot
        if extend or self.extendMode:
            i, j = g.app.gui.getTextSelection(w)
            if (
                not moveSpot or p.v.t != self.moveSpotNode or
                i == j or # A cute trick
                (not w.compare(moveSpot,'==',i) and
                 not w.compare(moveSpot,'==',j))
            ):
                self.moveSpotNode = p.v.t
                self.moveSpot = w.index(ins1)
                self.moveCol = int(ins1.split('.')[1])
                # g.trace('reset moveSpot',self.moveSpot)
            moveSpot = self.moveSpot
            # g.trace(spot,moveSpot)
            if w.compare(spot,'<',moveSpot):
                g.app.gui.setTextSelection(w,spot,moveSpot,insert=None)
            else:
                g.app.gui.setTextSelection(w,moveSpot,spot,insert=None)
        else:
            # Don't change the moveCol while extending: that would mess up the selection.
            if setSpot or not moveSpot:
                self.setMoveCol(spot)
            g.app.gui.setTextSelection(w,spot,spot,insert=None)
    #@nonl
    #@-node:ekr.20060113130510:extendHelper
    #@+node:ekr.20060113105246.1:moveUpOrDownHelper
    def moveUpOrDownHelper (self,event,direction,extend):
    
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
        # Make the insertion cursor visible so bbox won't return an empty list.
        w.see('insert')
        # Remember the original insert point.  This may become the moveSpot.
        ins1 = w.index('insert')
        # Compute the new spot.
        row1,col1 = ins1.split('.')
        row1 = int(row1) ; col1 = int(col1)
        # Find the coordinates of the cursor and set the new height.
        # There may be roundoff errors because character postions may not match exactly.
        x, y, junk, textH = w.bbox('insert')
        bodyW, bodyH = w.winfo_width(), w.winfo_height()
        junk, maxy, junk, junk = w.bbox("@%d,%d" % (bodyW,bodyH))
        # Make sure y is within text boundaries.
        if direction == "up":
            if y <= textH:  w.yview("scroll",-1,"units")
            else:           y = max(y-textH,0)
        else:
            if y >= maxy:   w.yview("scroll",1,"units")
            else:           y = min(y+textH,maxy)
        # Position the cursor on the proper side of the characters.
        newx, newy, width, junk = w.bbox("@%d,%d" % (x,y))
        if x > newx + width / 2: x = newx + width + 1
        # Move to the new row.
        spot = w.index("@%d,%d" % (x,y))
        row,col = spot.split('.')
        row = int(row) ; col = int(col)
        w.mark_set('insert',spot)
        # Adjust the column in the *new* row, but only if we have actually gone to a new row.
        if self.moveSpot:
            if col != self.moveCol and row != row1:
                s = w.get('insert linestart','insert lineend')
                col = min(len(s),self.moveCol)
                if col >= 0:
                    w.mark_set('insert','%d.%d' % (row,col))
                    spot = w.index('insert')
                    w.see('insert')
        # Handle the extension.
        self.extendHelper(w,extend,ins1,spot,setSpot=False)
    #@nonl
    #@-node:ekr.20060113105246.1:moveUpOrDownHelper
    #@+node:ekr.20051218122116:moveToHelper
    def moveToHelper (self,event,spot,extend):
    
        '''Common helper method for commands the move the cursor
        in a way that can be described by a Tk Text expression.'''
    
        c = self.c ; k = c.k ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocusNow(w)
    
        wname = c.widget_name(w)
        if wname.startswith('mini'):
            # Put the request in the proper range.
            i, j = k.getEditableTextRange()
            ins1 = w.index('insert')
            spot = w.index(spot)
            if w.compare(spot,'<',i):
                spot = i
            elif w.compare(spot,'>',j):
                spot = j
            w.mark_set('insert',spot)
            self.extendHelper(w,extend,ins1,spot,setSpot=False)
            w.see(spot)
        else:
            # Remember the original insert point.  This may become the moveSpot.
            ins1 = w.index('insert')
    
            # Move to the spot.
            w.mark_set('insert',spot)
            spot = w.index('insert')
    
            # Handle the selection.
            self.extendHelper(w,extend,ins1,spot,setSpot=True)
            w.see(spot)
    #@nonl
    #@-node:ekr.20051218122116:moveToHelper
    #@+node:ekr.20051218121447:moveWordHelper
    def moveWordHelper (self,event,extend,forward):
    
        '''This function moves the cursor to the next word, direction dependent on the way parameter'''
    
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
        
        c.widgetWantsFocus(w)
        if forward:
             ind = w.search('\w','insert',stopindex='end',regexp=True)
             if ind: nind = '%s wordend' % ind
             else:   nind = 'end'
        else:
             ind = w.search('\w','insert -1c',stopindex='1.0',regexp=True,backwards=True)
             if ind: nind = '%s wordstart' % ind
             else:   nind = '1.0'
        self.moveToHelper(event,nind,extend)
    #@nonl
    #@-node:ekr.20051218121447:moveWordHelper
    #@+node:ekr.20051218171457:movePastCloseHelper
    def movePastCloseHelper (self,event,extend):
    
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
        i = w.search('(','insert',backwards=True,stopindex='1.0')
        if '' == i: return
    
        icheck = w.search(')','insert',backwards=True,stopindex='1.0')
        if icheck:
            ic = w.compare(i,'<',icheck)
            if ic: return
    
        i2 = w.search(')','insert',stopindex='end')
        if '' == i2: return
    
        i2check = w.search('(','insert',stopindex='end')
        if i2check:
            ic2 = w.compare(i2,'>',i2check)
            if ic2: return
        
        ins = '%s+1c' % i2
        self.moveToHelper(event,ins,extend)
    #@nonl
    #@-node:ekr.20051218171457:movePastCloseHelper
    #@+node:ekr.20051213094517:backSentenceHelper
    def backSentenceHelper (self,event,extend):
    
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
        i = w.search('.','insert',backwards=True,stopindex='1.0')
        if i:
            i2 = w.search('.',i,backwards=True,stopindex='1.0')
            if i2:
                ins = w.search('\w',i2,stopindex=i,regexp=True) or i2
            else:
                ins = '1.0'
        else:
            ins = '1.0'
        if ins:
            self.moveToHelper(event,ins,extend)
    #@nonl
    #@-node:ekr.20051213094517:backSentenceHelper
    #@+node:ekr.20050920084036.137:forwardSentenceHelper
    def forwardSentenceHelper (self,event,extend):
    
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
        ins = w.index('insert')
        # sel_i,sel_j = g.app.gui.getTextSelection(w)
        i = w.search('.','insert',stopindex='end')
        ins = i and '%s +1c' % i or 'end'
        self.moveToHelper(event,ins,extend)
    #@nonl
    #@-node:ekr.20050920084036.137:forwardSentenceHelper
    #@+node:ekr.20051218133207.1:forwardParagraphHelper
    def forwardParagraphHelper (self,event,extend):
        
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
        i = w.index('insert')
        while 1:
            txt = w.get('%s linestart' % i,'%s lineend' % i).strip()
            if txt:
                i = w.index('%s + 1 lines' % i)
                if w.index('%s linestart' % i) == w.index('end'):
                    i = w.search(r'\w','end',backwards=True,regexp=True,stopindex='1.0')
                    i = '%s + 1c' % i
                    break
            else:
                i = w.search(r'\w',i,regexp=True,stopindex='end')
                i = '%s' % i
                break
        if i:
            self.moveToHelper(event,i,extend)
    #@nonl
    #@-node:ekr.20051218133207.1:forwardParagraphHelper
    #@+node:ekr.20051218133207:backwardParagraphHelper
    def backwardParagraphHelper (self,event,extend):
        
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
        i = w.index('insert')
        while 1:
            s = w.get('%s linestart' % i,'%s lineend' % i).strip()
            if s:
                i = w.index('%s - 1 lines' % i)
                if w.index('%s linestart' % i) == '1.0':
                    i = w.search(r'\w','1.0',regexp=True,stopindex='end')
                    break
            else:
                i = w.search(r'\w',i,backwards=True,regexp=True,stopindex='1.0')
                i = '%s +1c' % i
                break
        if i:
            self.moveToHelper(event,i,extend)
    #@nonl
    #@-node:ekr.20051218133207:backwardParagraphHelper
    #@+node:ekr.20060209095101:setMoveCol
    def setMoveCol (self,spot):
        
        self.moveSpot = spot
        self.moveCol = int(spot.split('.')[1])
    
        # g.trace('spot',self.moveSpot,'col',self.moveCol)
    #@nonl
    #@-node:ekr.20060209095101:setMoveCol
    #@-node:ekr.20051218170358: helpers
    #@+node:ekr.20050920084036.136:exchangePointMark
    def exchangePointMark (self,event):
        
        c = self.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
        i,j = g.app.gui.getTextSelection(w,sort=False)
        if i != j:
            ins = w.index('insert')
            ins = g.choose(ins==i,j,i)
            g.app.gui.setInsertPoint(w,ins)
            g.app.gui.setTextSelection(w,i,j,insert=None)
    #@nonl
    #@-node:ekr.20050920084036.136:exchangePointMark
    #@+node:ekr.20051218174113:extendMode
    def clearExtendMode (self,event):
        
        self.extendMode = False
        
        c = self.c ; w = event.widget
        c.widgetWantsFocus(w)
    
    def setExtendMode (self,event):
        
        self.extendMode = True
        
        c = self.c ; w = event.widget
        c.widgetWantsFocus(w)
        
    def toggleExtendMode (self,event):
        
        self.extendMode = not self.extendMode
        
        c = self.c ; w = event.widget
        c.widgetWantsFocus(w)
    #@nonl
    #@-node:ekr.20051218174113:extendMode
    #@+node:ekr.20050920084036.148:buffers
    def beginningOfBuffer (self,event):
        
        self.moveToHelper(event,'1.0',extend=False)
        
    def beginningOfBufferExtendSelection (self,event):
        
        self.moveToHelper(event,'1.0',extend=True)
    
    def endOfBuffer (self,event):
        
        self.moveToHelper(event,'end',extend=False)
        
    def endOfBufferExtendSelection (self,event):
        
        self.moveToHelper(event,'end',extend=True)
    #@-node:ekr.20050920084036.148:buffers
    #@+node:ekr.20051213080533:characters
    def backCharacter (self,event):
        
        self.moveToHelper(event,'insert-1c',extend=False)
        
    def backCharacterExtendSelection (self,event):
        
        self.moveToHelper(event,'insert-1c',extend=True)
        
    def forwardCharacter (self,event):
        
        self.moveToHelper (event,'insert+1c',extend=False)
        
    def forwardCharacterExtendSelection (self,event):
        
        self.moveToHelper (event,'insert+1c',extend=True)
    #@-node:ekr.20051213080533:characters
    #@+node:ekr.20051218141237:lines
    def beginningOfLine (self,event):
        self.moveToHelper(event,'insert linestart',extend=False)
        
    def beginningOfLineExtendSelection (self,event):
        self.moveToHelper(event,'insert linestart',extend=True)
        
    def endOfLine (self,event):
        self.moveToHelper(event,'insert lineend',extend=False)
        
    def endOfLineExtendSelection (self,event):
        self.moveToHelper(event,'insert lineend',extend=True)
    
    def nextLine (self,event):
        self.moveUpOrDownHelper(event,'down',extend=False)
        
    def nextLineExtendSelection (self,event):
        self.moveUpOrDownHelper(event,'down',extend=True)
        
    def prevLine (self,event):
        self.moveUpOrDownHelper(event,'up',extend=False)
        
    def prevLineExtendSelection (self,event):
        self.moveUpOrDownHelper(event,'up',extend=True)
    #@nonl
    #@-node:ekr.20051218141237:lines
    #@+node:ekr.20050920084036.140:movePastClose (test)
    def movePastClose (self,event):
        
        self.movePastCloseHelper(event,extend=False)
        
    def movePastCloseExtendSelection (self,event):
        
        self.movePastCloseHelper(event,extend=True)
    #@nonl
    #@-node:ekr.20050920084036.140:movePastClose (test)
    #@+node:ekr.20050920084036.102:paragraphs
    def backwardParagraph (self,event):
        
        self.backwardParagraphHelper (event,extend=False)
        
    def backwardParagraphExtendSelection (self,event):
        
        self.backwardParagraphHelper (event,extend=True)
        
    def forwardParagraph (self,event):
    
        self.forwardParagraphHelper(event,extend=False)
        
    def forwardParagraphExtendSelection (self,event):
        
        self.forwardParagraphHelper(event,extend=True)
    #@nonl
    #@-node:ekr.20050920084036.102:paragraphs
    #@+node:ekr.20050920084036.131:sentences
    def backSentence (self,event):
        
        self.backSentenceHelper(event,extend=False)
        
    def backSentenceExtendSelection (self,event):
        
        self.backSentenceHelper(event,extend=True)
        
    def forwardSentence (self,event):
        
        self.forwardSentenceHelper(event,extend=False)
        
    def forwardSentenceExtendSelection (self,event):
        
        self.forwardSentenceHelper(event,extend=True)
    #@nonl
    #@-node:ekr.20050920084036.131:sentences
    #@+node:ekr.20050920084036.149:words
    def backwardWord (self,event):
        
        self.moveWordHelper(event,extend=False,forward=False)
        
    def backwardWordExtendSelection (self,event):
        
        self.moveWordHelper(event,extend=True,forward=False)
    
    def forwardWord (self,event):
        
        self.moveWordHelper(event,extend=False,forward=True)
        
    def forwardWordExtendSelection (self,event):
        
        self.moveWordHelper(event,extend=True,forward=True)
    #@-node:ekr.20050920084036.149:words
    #@-node:ekr.20050929114218:move... (leoEditCommands)
    #@+node:ekr.20050920084036.95:paragraph...
    #@+others
    #@+node:ekr.20050920084036.99:backwardKillParagraph
    def backwardKillParagraph (self,event):
    
        k = self.k ; c = k.c ; w = event.widget
        i = w.index('insert')
        i2 = i
        txt = w.get('insert linestart','insert lineend')
        if not txt.rstrip().lstrip():
            self.backwardParagraph(event)
            i2 = w.index('insert')
        self.selectParagraph(event)
        i3 = w.index('sel.first')
        c.killBufferCommands.kill(event,i3,i2)
        w.mark_set('insert',i)
        w.selection_clear()
    #@nonl
    #@-node:ekr.20050920084036.99:backwardKillParagraph
    #@+node:ekr.20050920084036.103:fillParagraph
    def fillParagraph( self, event ):
        k = self.k ; w = event.widget
        txt = w.get( 'insert linestart', 'insert lineend' )
        txt = txt.lstrip().rstrip()
        if txt:
            i = w.index( 'insert' )
            i2 = i
            txt2 = txt
            while txt2:
                pi2 = w.index( '%s - 1 lines' % i2)
                txt2 = w.get( '%s linestart' % pi2, '%s lineend' % pi2 )
                if w.index( '%s linestart' % pi2 ) == '1.0':
                    i2 = w.search( '\w', '1.0', regexp = True, stopindex = 'end' )
                    break
                if txt2.lstrip().rstrip() == '': break
                i2 = pi2
            i3 = i
            txt3 = txt
            while txt3:
                pi3 = w.index( '%s + 1 lines' %i3 )
                txt3 = w.get( '%s linestart' % pi3, '%s lineend' % pi3 )
                if w.index( '%s lineend' % pi3 ) == w.index( 'end' ):
                    i3 = w.search( '\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                    break
                if txt3.lstrip().rstrip() == '': break
                i3 = pi3
            ntxt = w.get( '%s linestart' %i2, '%s lineend' %i3 )
            ntxt = self._addPrefix( ntxt )
            w.delete( '%s linestart' %i2, '%s lineend' % i3 )
            w.insert( i2, ntxt )
            w.mark_set( 'insert', i )
    #@nonl
    #@-node:ekr.20050920084036.103:fillParagraph
    #@+node:ekr.20050920084036.100:fillRegion
    def fillRegion (self,event):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event): return
    
        s1 = w.index('sel.first')
        s2 = w.index('sel.last')
        w.mark_set('insert',s1)
        self.backwardParagraph(event)
        if w.index('insert linestart') == '1.0':
            self.fillParagraph(event)
        while 1:
            self.forwardParagraph(event)
            if w.compare('insert','>',s2):
                break
            self.fillParagraph(event)
    #@nonl
    #@-node:ekr.20050920084036.100:fillRegion
    #@+node:ekr.20050920084036.104:fillRegionAsParagraph
    def fillRegionAsParagraph (self,event):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event): return
    
        i1 = w.index('sel.first linestart')
        i2 = w.index('sel.last lineend')
        txt = w.get(i1,i2)
        txt = self._addPrefix(txt)
        w.delete(i1,i2)
        w.insert(i1,txt)
    #@nonl
    #@-node:ekr.20050920084036.104:fillRegionAsParagraph
    #@+node:ekr.20050920084036.98:killParagraph (Test)
    def killParagraph (self,event):
    
        k = self.k ; c = k.c ; w = event.widget
        i = w.index('insert')
        txt = w.get('insert linestart','insert lineend')
    
        if not txt.rstrip().lstrip():
            i = w.search(r'\w',i,regexp=True,stopindex='end')
    
        self.selectParagraphHelper(w,i)
        i2 = w.index('insert')
        c.killBufferCommands.kill(event,i,i2)
        w.mark_set('insert',i)
        w.selection_clear()
    #@nonl
    #@-node:ekr.20050920084036.98:killParagraph (Test)
    #@+node:ekr.20050920084036.96:selectParagraph & helper
    def selectParagraph (self,event):
    
        k = self.k ; w = event.widget
        txt = w.get('insert linestart','insert lineend')
        txt = txt.lstrip().rstrip()
        i = w.index('insert')
    
        if not txt:
            while 1:
                i = w.index('%s + 1 lines' % i)
                txt = w.get('%s linestart' % i,'%s lineend' % i)
                txt = txt.lstrip().rstrip()
                if txt:
                    self.selectParagraphHelper(w,i) ; break
                if w.index('%s lineend' % i) == w.index('end'):
                    return
    
        if txt:
            while 1:
                i = w.index('%s - 1 lines' % i)
                txt = w.get('%s linestart' % i,'%s lineend' % i)
                txt = txt.lstrip().rstrip()
                if not txt or w.index('%s linestart' % i) == w.index('1.0'):
                    if not txt: i = w.index('%s + 1 lines' % i)
                    self.selectParagraphHelper(w,i)
                    break
    #@nonl
    #@+node:ekr.20050920084036.97:selectParagraphHelper
    def selectParagraphHelper (self,w,start):
    
        i2 = start
        while 1:
            txt = w.get('%s linestart' % i2,'%s lineend' % i2)
            if w.index('%s lineend' % i2) == w.index('end'):
                break
            txt = txt.lstrip().rstrip()
            if not txt: break
            else:
                i2 = w.index('%s + 1 lines' % i2)
    
        w.tag_add('sel','%s linestart' % start,'%s lineend' % i2)
        w.mark_set('insert','%s lineend' % i2)
    #@nonl
    #@-node:ekr.20050920084036.97:selectParagraphHelper
    #@-node:ekr.20050920084036.96:selectParagraph & helper
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.95:paragraph...
    #@+node:ekr.20050920084036.105:region...
    #@+others
    #@+node:ekr.20050920084036.106:setRegion
    def setRegion (self,event):
    
        mrk = 'sel'
        w = event.widget
    
        #@    @+others
        #@+node:ekr.20051002102410:down
        def down (event):
        
            w = event.widget
        
            if self.testinrange(w):
                w.tag_add(mrk,'insert','insert lineend')
                i = w.index('insert')
                i1, i2 = i.split('.')
                i1 = str(int(i1)+1)
                w.mark_set('insert',i1+'.'+i2)
                w.tag_add(mrk,'insert linestart -1c','insert')
                if self.inRange(w,mrk,l='-1c',r='+1c'):
                    w.tag_remove(mrk,'1.0','insert')
        
            return 'break'
        #@nonl
        #@-node:ekr.20051002102410:down
        #@+node:ekr.20051002102410.1:extend
        def extend (event):
        
            w = event.widget
            w.mark_set('insert','insert + 1c')
        
            if self.inRange(w,mrk):
                w.tag_remove(mrk,'insert -1c')
            else:
                w.tag_add(mrk,'insert -1c')
                w.tag_configure(mrk,background='lightgrey')
                self.testinrange(w)
        
            return 'break'
        
        #@-node:ekr.20051002102410.1:extend
        #@+node:ekr.20051002102410.2:truncate
        def truncate (event):
        
            w = event.widget
            w.mark_set('insert','insert -1c')
        
            if self.inRange(w,mrk):
                self.testinrange(w)
                w.tag_remove(mrk,'insert')
            else:
                w.tag_add(mrk,'insert')
                w.tag_configure(mrk,background='lightgrey')
                self.testinrange(w)
        
            return 'break'
        #@nonl
        #@-node:ekr.20051002102410.2:truncate
        #@+node:ekr.20051002102410.3:up
        def up (event):
        
            w = event.widget
        
            if self.testinrange(w):
                w.tag_add(mrk,'insert linestart','insert')
                i = w.index('insert')
                i1, i2 = i.split('.')
                i1 = str(int(i1)-1)
                w.mark_set('insert',i1+'.'+i2)
                w.tag_add(mrk,'insert','insert lineend + 1c')
                if self.inRange(w,mrk,l='-1c',r='+1c') and w.index('insert') != '1.0':
                    w.tag_remove(mrk,'insert','end')
        
            return 'break'
        #@nonl
        #@-node:ekr.20051002102410.3:up
        #@-others
    
        extend(event)
        w.bind('<Right>',extend,'+')
        w.bind('<Left>',truncate,'+')
        w.bind('<Up>',up,'+')
        w.bind('<Down>',down,'+')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.106:setRegion
    #@+node:ekr.20050920084036.107:indentRegion
    def indentRegion (self,event):
        w = event.widget
        mrk = 'sel'
        trange = w.tag_ranges(mrk)
        if len(trange) != 0:
            ind = w.search('\w','%s linestart' % trange[0],stopindex='end',regexp=True)
            if not ind: return
            text = w.get('%s linestart' % ind,'%s lineend' % ind)
            sstring = text.lstrip()
            sstring = sstring [0]
            ws = text.split(sstring)
            if len(ws) > 1:
                ws = ws [0]
            else:
                ws = ''
            s, s1 = trange [0].split('.')
            e, e1 = trange [ -1].split('.')
            s = int(s)
            s = s + 1
            e = int(e) + 1
            for z in xrange(s,e):
                t2 = w.get('%s.0' % z,'%s.0 lineend' % z)
                t2 = t2.lstrip()
                t2 = ws + t2
                w.delete('%s.0' % z,'%s.0 lineend' % z)
                w.insert('%s.0' % z,t2)
            ### w.event_generate('<Key>')
            ### w.update_idletasks()
        self.removeRKeys(w)
    #@nonl
    #@-node:ekr.20050920084036.107:indentRegion
    #@+node:ekr.20050920084036.108:tabIndentRegion
    def tabIndentRegion (self,event):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event): return
    
        i = w.index('sel.first')
        i2 = w.index('sel.last')
        i = w.index('%s linestart' % i)
        i2 = w.index('%s linestart' % i2)
        while 1:
            w.insert(i,'\t')
            if i == i2: break
            i = w.index('%s + 1 lines' % i)
    #@nonl
    #@-node:ekr.20050920084036.108:tabIndentRegion
    #@+node:ekr.20050920084036.109:countRegion
    def countRegion (self,event):
    
        k = self.k ; w = event.widget
    
        txt = w.get('sel.first','sel.last')
        lines = 1 ; chars = 0
        for z in txt:
            if z == '\n': lines += 1
            else:         chars += 1
    
        k.setLabelGrey('Region has %s lines, %s character%s' % (
            lines,chars,g.choose(chars==1,'','s')))
    #@nonl
    #@-node:ekr.20050920084036.109:countRegion
    #@+node:ekr.20050920084036.110:reverseRegion
    def reverseRegion (self,event):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event): return
    
        ins = w.index('insert')
        is1 = w.index('sel.first')
        is2 = w.index('sel.last')
        txt = w.get('%s linestart' % is1,'%s lineend' % is2)
        w.delete('%s linestart' % is1,'%s lineend' % is2)
        txt = txt.split('\n')
        txt.reverse()
        istart = is1.split('.')
        istart = int(istart[0])
        for z in txt:
            w.insert('%s.0' % istart,'%s\n' % z)
            istart = istart + 1
        w.mark_set('insert',ins)
        k.clearState()
        k.resetLabel()
    #@nonl
    #@-node:ekr.20050920084036.110:reverseRegion
    #@+node:ekr.20050920084036.111:up/downCaseRegion & helper
    def downCaseRegion (self,event):
        self.caseHelper(event,'low')
    
    def upCaseRegion (self,event):
        self.caseHelper(event,'up')
    
    def caseHelper (self,event,way):
    
        w = event.widget ; trange = w.tag_ranges('sel')
    
        if len(trange) != 0:
            text = w.get(trange[0],trange[-1])
            i = w.index('insert')
            if text == ' ': return
            w.delete(trange[0],trange[-1])
            if way == 'low': text = text.lower()
            if way == 'up':  text = text.upper()
            w.insert('insert',text)
            w.mark_set('insert',i)
    
        self.removeRKeys(w)
    #@nonl
    #@-node:ekr.20050920084036.111:up/downCaseRegion & helper
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.105:region...
    #@+node:ekr.20060309060654:scrolling...
    #@+node:ekr.20050920084036.116:scrollUp/Down/extendSelection
    def scrollDown (self,event):
        self.scrollHelper(event,'down',extend=False)
    
    def scrollDownExtendSelection (self,event):
        self.scrollHelper(event,'down',extend=True)
    
    def scrollUp (self,event):
        self.scrollHelper(event,'up',extend=False)
    
    def scrollUpExtendSelection (self,event):
        self.scrollHelper(event,'up',extend=True)
    #@nonl
    #@+node:ekr.20060113082917:scrollHelper
    def scrollHelper (self,event,direction,extend):
    
        k = self.k ; c = k.c ; w = event.widget
        if not g.app.gui.isTextWidget(w): return
    
        c.widgetWantsFocus(w)
    
        # Remember the original insert point.  This may become the moveSpot.
        ins1 = w.index('insert')
        row, col = ins1.split('.') ; row = int(row) ; col = int(col)
    
        # Compute the spot.
        chng = self.measure(w) ; delta = chng [0]
        row1 = g.choose(direction=='down',row+delta,row-delta)
        spot = w.index('%d.%d' % (row1,col))
        w.mark_set('insert',spot)
    
        # Handle the extension.
        self.extendHelper(w,extend,ins1,spot,setSpot=False)
        w.see('insert')
    #@nonl
    #@-node:ekr.20060113082917:scrollHelper
    #@-node:ekr.20050920084036.116:scrollUp/Down/extendSelection
    #@+node:ekr.20060309060654.1:scrollOutlineUp/Down/Line/Page
    def scrollOutlineDownLine (self,event=None):
        self.c.frame.tree.canvas.yview_scroll(1,"unit")
        
    def scrollOutlineDownPage (self,event=None):
        self.c.frame.tree.canvas.yview_scroll(1,"page")
    
    def scrollOutlineUpLine (self,event=None):
        self.c.frame.tree.canvas.yview_scroll(-1,"unit")
    
    def scrollOutlineUpPage (self,event=None):
        self.c.frame.tree.canvas.yview_scroll(-1,"page")
    
    
    #@-node:ekr.20060309060654.1:scrollOutlineUp/Down/Line/Page
    #@-node:ekr.20060309060654:scrolling...
    #@+node:ekr.20050920084036.117:sort...
    '''XEmacs provides several commands for sorting text in a buffer.  All
    operate on the contents of the region (the text between point and the
    mark).  They divide the text of the region into many "sort records",
    identify a "sort key" for each record, and then reorder the records
    using the order determined by the sort keys.  The records are ordered so
    that their keys are in alphabetical order, or, for numerical sorting, in
    numerical order.  In alphabetical sorting, all upper-case letters `A'
    through `Z' come before lower-case `a', in accordance with the ASCII
    character sequence.
    
       The sort commands differ in how they divide the text into sort
    records and in which part of each record they use as the sort key.
    Most of the commands make each line a separate sort record, but some
    commands use paragraphs or pages as sort records.  Most of the sort
    commands use each entire sort record as its own sort key, but some use
    only a portion of the record as the sort key.
    
    `M-x sort-lines'
         Divide the region into lines and sort by comparing the entire text
         of a line.  A prefix argument means sort in descending order.
    
    `M-x sort-paragraphs'
         Divide the region into paragraphs and sort by comparing the entire
         text of a paragraph (except for leading blank lines).  A prefix
         argument means sort in descending order.
    
    `M-x sort-pages'
         Divide the region into pages and sort by comparing the entire text
         of a page (except for leading blank lines).  A prefix argument
         means sort in descending order.
    
    `M-x sort-fields'
         Divide the region into lines and sort by comparing the contents of
         one field in each line.  Fields are defined as separated by
         whitespace, so the first run of consecutive non-whitespace
         characters in a line constitutes field 1, the second such run
         constitutes field 2, etc.
    
         You specify which field to sort by with a numeric argument: 1 to
         sort by field 1, etc.  A negative argument means sort in descending
         order.  Thus, minus 2 means sort by field 2 in reverse-alphabetical
         order.
    
    `M-x sort-numeric-fields'
         Like `M-x sort-fields', except the specified field is converted to
         a number for each line and the numbers are compared.  `10' comes
         before `2' when considered as text, but after it when considered
         as a number.
    
    `M-x sort-columns'
         Like `M-x sort-fields', except that the text within each line used
         for comparison comes from a fixed range of columns.  An explanation
         is given below.
    
       For example, if the buffer contains:
    
         On systems where clash detection (locking of files being edited) is
         implemented, XEmacs also checks the first time you modify a buffer
         whether the file has changed on disk since it was last visited or
         saved.  If it has, you are asked to confirm that you want to change
         the buffer.
    
    then if you apply `M-x sort-lines' to the entire buffer you get:
    
         On systems where clash detection (locking of files being edited) is
         implemented, XEmacs also checks the first time you modify a buffer
         saved.  If it has, you are asked to confirm that you want to change
         the buffer.
         whether the file has changed on disk since it was last visited or
    
    where the upper case `O' comes before all lower case letters.  If you
    apply instead `C-u 2 M-x sort-fields' you get:
    
         saved.  If it has, you are asked to confirm that you want to change
         implemented, XEmacs also checks the first time you modify a buffer
         the buffer.
         On systems where clash detection (locking of files being edited) is
         whether the file has changed on disk since it was last visited or
    
    where the sort keys were `If', `XEmacs', `buffer', `systems', and `the'.
    
       `M-x sort-columns' requires more explanation.  You specify the
    columns by putting point at one of the columns and the mark at the other
    column.  Because this means you cannot put point or the mark at the
    beginning of the first line to sort, this command uses an unusual
    definition of `region': all of the line point is in is considered part
    of the region, and so is all of the line the mark is in.
    
       For example, to sort a table by information found in columns 10 to
    15, you could put the mark on column 10 in the first line of the table,
    and point on column 15 in the last line of the table, and then use this
    command.  Or you could put the mark on column 15 in the first line and
    point on column 10 in the last line.
    
       This can be thought of as sorting the rectangle specified by point
    and the mark, except that the text on each line to the left or right of
    the rectangle moves along with the text inside the rectangle.  *Note
    Rectangles::.
    
    '''
    #@+node:ekr.20050920084036.118:sortLines
    def sortLines (self,event,which=None):
    
        c = self.c ; k = c.k ; w = event.widget
        g.trace(c.widget_name(w))
        if not self._chckSel(event): return
        self.beginCommand()
        i = w.index('sel.first')
        i2 = w.index('sel.last')
        is1 = i.split('.')
        is2 = i2.split('.')
        txt = w.get('%s.0' % is1[0],'%s.0 lineend' % is2[0])
        ins = w.index('insert')
        txt = txt.split('\n')
        w.delete('%s.0' % is1[0],'%s.0 lineend' % is2[0])
        txt.sort()
        if which:
            txt.reverse()
        inum = int(is1[0])
        for z in txt:
            w.insert('%s.0' % inum,'%s\n' % z)
            inum = inum + 1
        w.mark_set('insert',ins)
        self.endCommand(changed=True,setLabel=False)
    #@nonl
    #@-node:ekr.20050920084036.118:sortLines
    #@+node:ekr.20050920084036.119:sortColumns
    def sortColumns (self,event):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event): return
    
        ins = w.index('insert')
        is1 = w.index('sel.first')
        is2 = w.index('sel.last')
        sint1, sint2 = is1.split('.')
        sint2 = int(sint2)
        sint3, sint4 = is2.split('.')
        sint4 = int(sint4)
        txt = w.get('%s.0' % sint1,'%s.0 lineend' % sint3)
        w.delete('%s.0' % sint1,'%s.0 lineend' % sint3)
        columns = []
        i = int(sint1)
        i2 = int(sint3)
        while i <= i2:
            t = w.get('%s.%s' % (i,sint2),'%s.%s' % (i,sint4))
            columns.append(t)
            i = i + 1
        txt = txt.split('\n')
        zlist = zip(columns,txt)
        zlist.sort()
        i = int(sint1)
        for z in xrange(len(zlist)):
             w.insert('%s.0' % i,'%s\n' % zlist[z][1])
             i = i + 1
        w.mark_set('insert',ins)
    #@nonl
    #@-node:ekr.20050920084036.119:sortColumns
    #@+node:ekr.20050920084036.120:sortFields
    def sortFields (self,event,which=None):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event): return
    
        ins = w.index('insert')
        is1 = w.index('sel.first')
        is2 = w.index('sel.last')
        txt = w.get('%s linestart' % is1,'%s lineend' % is2)
        txt = txt.split('\n')
        fields = []
        fn = r'\w+'
        frx = re.compile(fn)
        for z in txt:
            f = frx.findall(z)
            if not which:
                fields.append(f[0])
            else:
                i = int(which)
                if len(f) < i: return
                i = i-1
                fields.append(f[i])
        nz = zip(fields,txt)
        nz.sort()
        w.delete('%s linestart' % is1,'%s lineend' % is2)
        i = is1.split('.')
        int1 = int(i[0])
        for z in nz:
            w.insert('%s.0' % int1,'%s\n' % z[1])
            int1 = int1 + 1
        w.mark_set('insert',ins)
    #@nonl
    #@-node:ekr.20050920084036.120:sortFields
    #@-node:ekr.20050920084036.117:sort...
    #@+node:ekr.20050920084036.121:swap/transpose...
    #@+node:ekr.20050920084036.122:transposeLines
    def transposeLines (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        i1, i2 = i.split('.')
        i1 = str(int(i1)-1)
    
        if i1 != '0':
            l2 = w.get('insert linestart','insert lineend')
            w.delete('insert linestart-1c','insert lineend')
            w.insert(i1+'.0',l2+'\n')
        else:
            l2 = w.get('2.0','2.0 lineend')
            w.delete('2.0','2.0 lineend')
            w.insert('1.0',l2+'\n')
    #@nonl
    #@-node:ekr.20050920084036.122:transposeLines
    #@+node:ekr.20050920084036.123:swapWords & transposeWords
    def swapWords (self,event,swapspots):
    
        w = event.widget
        txt = w.get('insert wordstart','insert wordend')
        if txt == ' ': return
        i = w.index('insert wordstart')
        if len(swapspots) != 0:
            if w.compare(i,'>',swapspots[1]):
                self.swapHelper(w,i,txt,swapspots[1],swapspots[0])
            elif w.compare(i,'<',swapspots[1]):
                self.swapHelper(w,swapspots[1],swapspots[0],i,txt)
        else:
            swapspots.append(txt)
            swapspots.append(i)
    
    def transposeWords (self,event):
        self.swapWords(event,self.swapSpots)
    
    def swapHelper (self,w,find,ftext,lind,ltext):
        w.delete(find,'%s wordend' % find)
        w.insert(find,ltext)
        w.delete(lind,'%s wordend' % lind)
        w.insert(lind,ftext)
        self.swapSpots.pop()
        self.swapSpots.pop()
    #@-node:ekr.20050920084036.123:swapWords & transposeWords
    #@+node:ekr.20050920084036.124:swapCharacters & transeposeCharacters
    def swapCharacters (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        c1 = w.get('insert','insert +1c')
        c2 = w.get('insert -1c','insert')
        w.delete('insert -1c','insert')
        w.insert('insert',c1)
        w.delete('insert','insert +1c')
        w.insert('insert',c2)
        w.mark_set('insert',i)
    
    transposeCharacters = swapCharacters
    #@nonl
    #@-node:ekr.20050920084036.124:swapCharacters & transeposeCharacters
    #@-node:ekr.20050920084036.121:swap/transpose...
    #@+node:ekr.20050920084036.126:tabify & untabify
    def tabify (self,event):
        self.tabifyHelper (event,which='tabify')
        
    def untabify (self,event):
        self.tabifyHelper (event,which='untabify')
    
    def tabifyHelper (self,event,which):
    
        k = self.k ; w = event.widget
        if w.tag_ranges('sel'):
            i = w.index('sel.first')
            end = w.index('sel.last')
            txt = w.get(i,end)
            if which == 'tabify':
                pattern = re.compile(' {4,4}') # Huh?
                ntxt = pattern.sub('\t',txt)
            else:
                pattern = re.compile('\t')
                ntxt = pattern.sub('    ',txt)
            w.delete(i,end)
            w.insert(i,ntxt)
    #@nonl
    #@-node:ekr.20050920084036.126:tabify & untabify
    #@-others
#@nonl
#@-node:ekr.20050920084036.53:class editCommandsClass
#@+node:ekr.20050920084036.161:class editFileCommandsClass
class editFileCommandsClass (baseEditCommandsClass):
    
    '''A class to load files into buffers and save buffers to files.'''
    
    #@    @+others
    #@+node:ekr.20050920084036.162: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    #@nonl
    #@-node:ekr.20050920084036.162: ctor
    #@+node:ekr.20050920084036.163: getPublicCommands (editFileCommandsClass)
    def getPublicCommands (self):
        
        k = self.k
    
        return {
            'delete-file':      self.deleteFile,
            'diff':             self.diff, 
            'insert-file':      self.insertFile,
            'make-directory':   self.makeDirectory,
            'remove-directory': self.removeDirectory,
            'save-file':        self.saveFile
        }
    #@nonl
    #@-node:ekr.20050920084036.163: getPublicCommands (editFileCommandsClass)
    #@+node:ekr.20050920084036.164:deleteFile
    def deleteFile (self,event):
    
        k = self.k ; state = k.getState('delete_file')
    
        if state == 0:
            prefix = 'Delete File: '
            k.setLabelBlue('%s%s%s' % (prefix,os.getcwd(),os.sep))
            k.getArg(event,'delete_file',1,self.deleteFile,prefix=prefix)
        else:
            k.keyboardQuit(event)
            k.clearState()
            try:
                os.remove(k.arg)
                k.setLabel('Deleted: %s' % k.arg)
            except:
                k.setLabel('Not Deleted: %s' % k.arg)
    #@nonl
    #@-node:ekr.20050920084036.164:deleteFile
    #@+node:ekr.20050920084036.165:diff (revise)
    def diff (self,event):
    
        '''the diff command, accessed by Alt-x diff.
        Creates a buffer and puts the diff between 2 files into it.'''
    
        k = self.k ; w = event.widget
    
        try:
            f, name = self.getReadableTextFile()
            txt1 = f.read() ; f.close()
            f2, name2 = self.getReadableTextFile()
            txt2 = f2.read() ; f2.close()
        except IOError: return
    
        ### self.switchToBuffer(event,"*diff* of ( %s , %s )" % (name,name2))
        data = difflib.ndiff(txt1,txt2)
        idata = []
        for z in data:
            idata.append(z)
        w.delete('1.0','end')
        w.insert('1.0',''.join(idata))
    #@nonl
    #@-node:ekr.20050920084036.165:diff (revise)
    #@+node:ekr.20050920084036.166:getReadableTextFile
    def getReadableTextFile (self):
    
        fname = tkFileDialog and tkFileDialog.askopenfilename()
        if fname == None:
            return None, None
        else:
            f = open(fname,'rt')
            return f, fname
    #@nonl
    #@-node:ekr.20050920084036.166:getReadableTextFile
    #@+node:ekr.20050920084036.167:insertFile
    def insertFile (self,event):
    
        k = self.k ; c = k.c ; w = event.widget
        f, name = self.getReadableTextFile()
        if f:
            txt = f.read()
            f.close()
            w.insert('insert',txt)
            w.see('1.0')
    #@nonl
    #@-node:ekr.20050920084036.167:insertFile
    #@+node:ekr.20050920084036.168:makeDirectory
    def makeDirectory (self,event):
    
        k = self.k ; state = k.getState('make_directory')
    
        if state == 0:
            prefix = 'Make Directory: '
            k.setLabelBlue('%s%s%s' % (prefix,os.getcwd(),os.sep))
            k.getArg(event,'make_directory',1,self.makeDirectory,prefix=prefix)
        else:
            k.keyboardQuit(event)
            k.clearState()
            try:
                os.mkdir(k.arg)
                k.setLabel("Created: %s" % k.arg)
            except:
                k.setLabel("Not Create: %s" % k.arg)
    #@nonl
    #@-node:ekr.20050920084036.168:makeDirectory
    #@+node:ekr.20050920084036.169:removeDirectory
    def removeDirectory (self,event):
    
        k = self.k ; state = k.getState('remove_directory')
    
        if state == 0:
            prefix = 'Remove Directory: '
            k.setLabelBlue('%s%s%s' % (prefix,os.getcwd(),os.sep))
            k.getArg(event,'remove_directory',1,self.removeDirectory,prefix=prefix)
        else:
            k.keyboardQuit(event)
            k.clearState()
            try:
                os.rmdir(k.arg)
                k.setLabel('Removed: %s' % k.arg)
            except:
                k.setLabel('Not Remove: %s' % k.arg)
    #@nonl
    #@-node:ekr.20050920084036.169:removeDirectory
    #@+node:ekr.20050920084036.170:saveFile
    def saveFile (self,event):
    
        w = event.widget
        txt = w.get('1.0','end')
        f = tkFileDialog and tkFileDialog.asksaveasfile()
        if f:
            f.write(txt)
            f.close()
    #@nonl
    #@-node:ekr.20050920084036.170:saveFile
    #@-others
#@nonl
#@-node:ekr.20050920084036.161:class editFileCommandsClass
#@+node:ekr.20060205164707:class helpCommandsClass
class helpCommandsClass (baseEditCommandsClass):
    
    '''A class to load files into buffers and save buffers to files.'''
    
    #@    @+others
    #@+node:ekr.20060205165501:getPublicCommands (helpCommands)
    def getPublicCommands (self):
        
        return {
            'help':                     self.help,
            'apropos-autocompletion':   self.aproposAutocompletion,
            'apropos-bindings':         self.aproposBindings,
            'apropos-find-commands':    self.aproposFindCommands,
        }
    #@nonl
    #@-node:ekr.20060205165501:getPublicCommands (helpCommands)
    #@+node:ekr.20051014170754:help
    def help (self,event=None):
    
        # A bug in Leo: triple quotes puts indentation before each line.
        c = self.c
        s = '''
    The mini-buffer is intended to be like the Emacs buffer:
    
    full-command: (default shortcut: Alt-x) Puts the focus in the minibuffer. Type a
    full command name, then hit <Return> to execute the command. Tab completion
    works, but not yet for file names.
    
    quick-command-mode (default shortcut: Alt-x). Like Emacs Control-C. This mode is
    defined in leoSettings.leo. It is useful for commonly-used commands.
    
    universal-argument (default shortcut: Alt-u). Like Emacs Ctrl-u. Adds a repeat
    count for later command. Ctrl-u 999 a adds 999 a's. Many features remain
    unfinished.
    
    keyboard-quit (default shortcut: Ctrl-g) Exits any minibuffer mode and puts
    the focus in the body pane.'''
    
        s = g.adjustTripleString(s,c.tab_width)
            # Remove indentation from indentation of this function.
        # s = s % (shortcuts[0],shortcuts[1],shortcuts[2],shortcuts[3])
        
        if not g.app.unitTesting:
            g.es_print(s)
    #@nonl
    #@+node:ekr.20060205165654:test_help
    def test_help(self):
        
        c.helpCommands.help()
    #@nonl
    #@-node:ekr.20060205165654:test_help
    #@-node:ekr.20051014170754:help
    #@+node:ekr.20060226131603.1:aproposAutocompletion
    def aproposAutocompletion (self,event=None):
        
        c = self.c ; s = '''
    This documentation describes both autocompletion and calltips.
    
    Typing a period when @language python is in effect starts autocompletion. Typing
    '(' during autocompletion shows the calltip. Typing Return or Control-g
    (keyboard-quit) exits autocompletion or calltips.
    
    Autocompletion
        
    Autocompletion shows what may follow a period in code. For example, after typing
    g. Leo will show a list of all the global functions in leoGlobals.py.
    Autocompletion works much like tab completion in the minibuffer. Unlike the
    minibuffer, the presently selected completion appears directly in the body
    pane.
    
    A leading period brings up 'Autocomplete Modules'. (The period goes away.) You
    can also get any module by typing its name. If more than 25 items would appear
    in the Autocompleter tab, Leo shows only the valid starting characters. At this
    point, typing an exclamation mark shows the complete list. Thereafter, typing
    further exclamation marks toggles between full and abbreviated modes.
    
    If x is a list 'x.!' shows all its elements, and if x is a Python dictionary,
    'x.!' shows x.keys(). For example, 'sys.modules.!' Again, further exclamation
    marks toggles between full and abbreviated modes.
    
    During autocompletion, typing a question mark shows the docstring for the
    object. For example: 'g.app?' shows the docstring for g.app. This doesn't work
    (yet) directly for Python globals, but '__builtin__.f?' does. Example:
    '__builtin__.pow?' shows the docstring for pow.
    
    Autocompletion works in the Find tab; you can use <Tab> to cycle through the
    choices. The 'Completion' tab appears while you are doing this; the Find tab
    reappears once the completion is finished.
    
    Calltips
    
    Calltips appear after you type an open parenthesis in code. Calltips shows the
    expected arguments to a function or method. Calltips work for any Python
    function or method, including Python's global function. Examples:
    
    a)  'g.toUnicode('  gives 'g.toUnicode(s, encoding, reportErrors=False'
    b) 'c.widgetWantsFocusNow' gives 'c.widgetWantsFocusNow(w'
    c) 'reduce(' gives 'reduce(function, sequence[, initial]) -> value'
    
    The calltips appear directly in the text and the argument list is highlighted so
    you can just type to replace it. The calltips appear also in the status line for
    reference after you have started to replace the args.
    
    Options
    
    Both autocompletion and calltips are initially enabled or disabled by the
    enable_autocompleter and enable_calltips settings in leoSettings.leo. You may
    enable or disable these features at any time with these commands:
    enable-auto-completer-command, enable-calltips-command,
    disable-auto-completer-command and disable-calltips-command.
    '''
    
        if not g.app.unitTesting:
            # Remove indentation from indentation of this function.
            s = g.adjustTripleString(s,c.tab_width)
            g.es_print(s)
    #@nonl
    #@+node:ekr.20060226132000:test_aproposAutocompletion
    def test_aproposAutocompletion (self):
    
        c.helpCommands.aproposAutocompletion()
    #@nonl
    #@-node:ekr.20060226132000:test_aproposAutocompletion
    #@-node:ekr.20060226131603.1:aproposAutocompletion
    #@+node:ekr.20060205170335:aproposBindings
    def aproposBindings (self,event=None):
        
        c = self.c
        s = '''
    A shortcut specification has the form:
        
    command-name = shortcutSpecifier
    
    or
    
    command-name ! pane = shortcutSpecifier
    
    The first form creates a binding for all panes except the minibuffer. The second
    form creates a binding for one or more panes. The possible values for 'pane'
    are:
    
    pane    bound panes
    ----    -----------
    all     body,log,tree
    body    body
    log     log
    mini    minibuffer
    text    body,log
    tree    tree
        
    You may use None as the specifier. Otherwise, a shortcut specifier consists of a
    head followed by a tail. The head may be empty, or may be a concatenation of the
    following: (All entries in each row are equivalent).
        
    Shift+ Shift-
    Alt+ or Alt-
    Control+, Control-, Ctrl+ or Ctrl-
    
    Notes:
    
    1. The case of plain letters is significant:  a is not A.
    
    2. The Shift- (or Shift+) prefix can be applied *only* to letters or
    multi-letter tails. Leo will ignore (with a warning) the shift prefix applied to
    other single letters, e.g., Ctrl-Shift-(
    
    3. The case of letters prefixed by Ctrl-, Alt-, Key- or Shift- is *not*
    significant.
    
    The following table illustrates these rules.  In each row, the first entry is the key (for k.bindingsDict) and the other entries are equivalents that the user may specify in leoSettings.leo:
    
    a, Key-a, Key-A
    A, Shift-A
    Alt-a, Alt-A
    Alt-A, Alt-Shift-a, Alt-Shift-A
    Ctrl-a, Ctrl-A
    Ctrl-A, Ctrl-Shift-a, Ctrl-Shift-A
    !, Key-!,Key-exclam,exclam
    '''
    
        s = g.adjustTripleString(s,c.tab_width)
            # Remove indentation from indentation of this function.
            
        if not g.app.unitTesting:
            g.es_print(s)
    #@nonl
    #@+node:ekr.20060205170435:test_apropos_bindings
    def test_apropos_bindings (self):
    
        c.helpCommands.aproposBindings()
    #@nonl
    #@-node:ekr.20060205170435:test_apropos_bindings
    #@-node:ekr.20060205170335:aproposBindings
    #@+node:ekr.20060205170335.1:aproposFindCommands
    def aproposFindCommands (self, event=None):
        
        c = self.c
        
        #@    << define s >>
        #@+node:ekr.20060209082023.1:<< define s >>
        s = '''
        Important: all minibuffer search commands, with the exception of the isearch (incremental) commands, simply provide a minibuffer interface to Leo's legacy find commands.  This means that all the powerful features of Leo's legacy commands are available to the minibuffer search commands.
        
        Note: all bindings shown are the default bindings for these commands.  You may change any of these bindings using @shortcut nodes in leoSettings.leo.
        
        Settings
        
        leoSettings.leo now contains several settings related to the Find tab:
        
        - @bool show_only_find_tab_options = True
        
        When True (recommended), the Find tab does not show the 'Find', 'Change', 'Change, Then Find', 'Find All' and 'Change All' buttons.
        
        - @bool minibufferSearchesShowFindTab = True
        
        When True, Leo shows the Find tab when executing most of the commands discussed below.  It's not necessary for it to be visible, but I think it provides good feedback about what search-with-present-options does.  YMMY.  When True, the sequence Control-F, Control-G is one way to show the Find Tab.
        
        Basic find commands
        
        - The open-find-tab command makes the Find tab visible.  The Find tab does **not** need to be visible to execute any search command discussed below.
        
        - The hide-find-tab commands hides the Find tab, but retains all the present settings.
        
        - The search-with-present-options command (Control-F) prompts for a search string.  Typing the <Return> key puts the search string in the Find tab and executes a search based on all the settings in the Find tab.   This command is my 'workhorse' search command.
        
        Coming in 4.4b3: the search-with-present-options will copy the present value of the 'find' string in the Find tab to the minibuffer.  This will make Control-f <Return> equivalent to F3 (find-tab-find).
        
        - The show-search-options command shows the present search options in the status line.  At present, this command also shows the Find tab.
        
        Search again commands
        
        - The find-tab-find command (F3) is the same as the search-with-present-options command, except that it uses the search string in the find-tab.  This is what I use as my default 'search again' command.
        
        - Similarly, the find-tab-find-previous command (F2) repeats the command specified by the Find tab, but in reverse.
        
        - The find-again command a combination of the search-with-present-options and find-tab-find command.  It is the same as the find-tab-find command if a search pattern other than '<find pattern here>' exists in the Find tab.  Otherwise, the find-again is the same as the search-with-present-options command.
        
        Setting find options
        
        - Several minibuffer commands toggle the checkboxes and radio buttons in the Find tab, and thus affect the operation of the search-with-present-options command. Some may want to bind these commands to keys. Others, will prefer to toggle options in a mode.
        
        
        Here are the commands that toggle checkboxes: toggle-find-ignore-case-option, toggle-find-in-body-option, toggle-find-in-headline-option, toggle-find-mark-changes-option, toggle-find-mark-finds-option, toggle-find-regex-option, toggle-find-reverse-option, toggle-find-word-option, and toggle-find-wrap-around-option.
        
        Here are the commands that set radio buttons: set-find-everywhere, set-find-node-only, and set-find-suboutline-only.
        
        - The enter-find-options-mode (Ctrl-Shift-F) enters a mode in which you may change all checkboxes and radio buttons in the Find tab with plain keys.  As always, you can use the mode-help (Tab) command to see a list of key bindings in effect for the mode.
        
        Search commands that set options as a side effect
        
        The following commands set an option in the Find tab, then work exactly like the search-with-present-options command.
        
        - The search-backward and search-forward commands set the 'Whole Word' checkbox to False.
        
        - The word-search-backward and word-search-forward set the 'Whole Word' checkbox to True.
        
        - The re-search-forward and re-search-backward set the 'Regexp' checkbox to True.
        
        Find all commands
        
        - The find-all command prints all matches in the log pane.
        
        - The clone-find-all command replaces the previous 'Clone Find' checkbox.  It prints all matches in the log pane, and creates a node at the beginning of the outline containing clones of all nodes containing the 'find' string.  Only one clone is made of each node, regardless of how many clones the node has, or of how many matches are found in each node.
        
        Note: the radio buttons in the Find tab (Entire Outline, Suboutline Only and Node only) control how much of the outline is affected by the find-all and clone-find-all commands.
        
        Search and replace commands
        
        The replace-string prompts for a search string.  Type <Return> to end the search string.  The command will then prompt for the replacement string.  Typing a second <Return> key will place both strings in the Find tab and executes a **find** command, that is, the search-with-present-options command.
        
        So the only difference between the replace-string and search-with-present-options commands is that the replace-string command has the side effect of setting 'change' string in the Find tab.  However, this is an extremely useful side effect, because of the following commands...
        
        - The find-tab-change command (Ctrl-=) replaces the selected text with the 'change' text in the Find tab.
        
        - The find-tab-change-then-find (Ctrl--) replaces the selected text with the 'change' text in the Find tab, then executes the find command again.
        
        The find-tab-find, find-tab-change and find-tab-change-then-find commands can simulate any kind of query-replace command.  **Important**: Leo presently has separate query-replace and query-replace-regex commands, but they are buggy and 'under-powered'.  Fixing these commands has low priority.
        
        - The find-tab-change-all command changes all occurrences of the 'find' text with the 'change' text.  Important: the radio buttons in the Find tab (Entire Outline, Suboutline Only and Node only) control how much of the outline is affected by this command.
        
        Incremental search commands
        
        Leo's incremental search commands are completely separate from Leo's legacy search commands.  At present, incremental search commands do not cross node boundaries: they work only in the body text of single node.
        
        Coming in Leo 4.4b3: the incremental commands will maintain a list of previous matches.  This allows for
        
        a) support for backspace and
        b) an incremental-search-again command.
        
        Furthermore, this list makes it easy to detect the end of a wrapped incremental search.
        
        Here is the list of incremental find commands: isearch-backward, isearch-backward-regexp, isearch-forward and
        isearch-forward-regexp.'''
        #@nonl
        #@-node:ekr.20060209082023.1:<< define s >>
        #@nl
    
        # Remove indentation from s: a workaround of a Leo bug.
        s = g.adjustTripleString(s,c.tab_width)
    
        if not g.app.unitTesting:
            g.es_print(s)
    #@nonl
    #@+node:ekr.20060205170552:test_apropos_find_commands
    def test_apropos_find_commands (self):
    
        c.helpCommands.aproposFindCommands()
    #@nonl
    #@-node:ekr.20060205170552:test_apropos_find_commands
    #@-node:ekr.20060205170335.1:aproposFindCommands
    #@-others
#@nonl
#@-node:ekr.20060205164707:class helpCommandsClass
#@+node:ekr.20050920084036.171:class keyHandlerCommandsClass
class keyHandlerCommandsClass (baseEditCommandsClass):
    
    '''User commands to access the keyHandler class.'''
    
    #@    @+others
    #@+node:ekr.20050920084036.172: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    #@nonl
    #@-node:ekr.20050920084036.172: ctor
    #@+node:ekr.20050920084036.173:getPublicCommands (keyHandler)
    def getPublicCommands (self):
        
        k = self.k
        
        return {
            'auto-complete':            k.autoCompleter.autoComplete,
            'auto-complete-force':      k.autoCompleter.autoCompleteForce,
            'digit-argument':           k.digitArgument,
            'disable-auto-completer-command':   k.autoCompleter.disableAutocompleter,
            'disable-calltips-command':         k.autoCompleter.disableCalltips,
            'enable-auto-completer-command':    k.autoCompleter.enableAutocompleter,
            'enable-calltips-command':          k.autoCompleter.enableCalltips,
            'exit-named-mode':          k.exitNamedMode,
            'full-command':             k.fullCommand, # For menu.
            'hide-mini-buffer':         k.hideMinibuffer,
            'mode-help':                k.modeHelp,
            'negative-argument':        k.negativeArgument,
            'number-command':           k.numberCommand,
            'number-command-0':         k.numberCommand0,
            'number-command-1':         k.numberCommand1,
            'number-command-2':         k.numberCommand2,
            'number-command-3':         k.numberCommand3,
            'number-command-4':         k.numberCommand4,
            'number-command-5':         k.numberCommand5,
            'number-command-6':         k.numberCommand6,
            'number-command-7':         k.numberCommand7,
            'number-command-8':         k.numberCommand8,
            'number-command-9':         k.numberCommand9,
            'print-bindings':           k.printBindings,
            'print-commands':           k.printCommands,
            'repeat-complex-command':   k.repeatComplexCommand,
            # 'scan-for-autocompleter':   k.autoCompleter.scan,
            'set-ignore-state':         k.setIgnoreState,
            'set-insert-state':         k.setInsertState,
            'set-overwrite-state':      k.setOverwriteState,
            'show-calltips':            k.autoCompleter.showCalltips,
            'show-calltips-force':      k.autoCompleter.showCalltipsForce,
            'show-mini-buffer':         k.showMinibuffer,
            'toggle-mini-buffer':       k.toggleMinibuffer,
            'universal-argument':       k.universalArgument,
        }
    #@nonl
    #@-node:ekr.20050920084036.173:getPublicCommands (keyHandler)
    #@-others
#@nonl
#@-node:ekr.20050920084036.171:class keyHandlerCommandsClass
#@+node:ekr.20050920084036.174:class killBufferCommandsClass
class killBufferCommandsClass (baseEditCommandsClass):
    
    '''A class to manage the kill buffer.'''

    #@    @+others
    #@+node:ekr.20050920084036.175: ctor & finishCreate
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    
        self.killBuffer = [] # May be changed in finishCreate.
        self.kbiterator = self.iterateKillBuffer()
        self.last_clipboard = None # For interacting with system clipboard.
        self.reset = False
        try:
            self.widget = c.frame.body.bodyCtrl
        except AttributeError:
            self.widget = None
    
    def finishCreate (self):
        
        baseEditCommandsClass.finishCreate(self)
            # Call the base finishCreate.
            # This sets self.k
        
        if self.k.useGlobalKillbuffer:
            self.killBuffer = leoKeys.keyHandlerClass.global_killbuffer
    #@nonl
    #@-node:ekr.20050920084036.175: ctor & finishCreate
    #@+node:ekr.20050920084036.176: getPublicCommands
    def getPublicCommands (self):
        
        return {
            'backward-kill-sentence':   self.backwardKillSentence,
            'backward-kill-word':       self.backwardKillWord,
            'clear-kill-ring':          self.clearKillRing,
            'kill-line':                self.killLine,
            'kill-word':                self.killWord,
            'kill-sentence':            self.killSentence,
            'kill-region':              self.killRegion,
            'kill-region-save':         self.killRegionSave,
            'yank':                     self.yank,
            'yank-pop':                 self.yankPop,
            'zap-to-character':         self.zapToCharacter,
        }
    #@nonl
    #@-node:ekr.20050920084036.176: getPublicCommands
    #@+node:ekr.20050920084036.183:addToKillBuffer
    def addToKillBuffer (self,text):
        
        killKeys =(
            '<Control-k>', '<Control-w>',
            '<Alt-d>', '<Alt-Delete', '<Alt-z>', '<Delete>',
            '<Control-Alt-w>')
    
        k = self.k
        self.reset = True
    
        g.trace(repr(text))
    
        if self.killBuffer and k.stroke in killKeys:
            self.killBuffer [0] = self.killBuffer [0] + text
        else:
            self.killBuffer.insert(0,text)
    #@nonl
    #@-node:ekr.20050920084036.183:addToKillBuffer
    #@+node:ekr.20050920084036.181:backwardKillSentence
    def backwardKillSentence (self,event):
        
        w = event.widget
        i = w.search('.','insert',backwards=True,stopindex='1.0')
    
        if i:
            i2 = w.search('.',i,backwards=True,stopindex='1.0')
            i2 = g.choose(i2=='','1.0',i2+'+1c ')
            self.kill(event,i2,'%s + 1c' % i)
    #@nonl
    #@-node:ekr.20050920084036.181:backwardKillSentence
    #@+node:ekr.20050920084036.180:backwardKillWord
    def backwardKillWord (self,event):
    
        c = self.c
        c.editCommands.backwardWord(event)
        self.killWord(event)
        self.killWs(event)
        c.editCommands.backwardWord(event)
    #@nonl
    #@-node:ekr.20050920084036.180:backwardKillWord
    #@+node:ekr.20051216151811:clearKillRing
    def clearKillRing (self,event=None):
        
        self.killBuffer = []
    #@nonl
    #@-node:ekr.20051216151811:clearKillRing
    #@+node:ekr.20050920084036.185:getClipboard
    def getClipboard (self,w):
    
        try:
            ctxt = w.selection_get(selection='CLIPBOARD')
            if not self.killBuffer or ctxt != self.last_clipboard:
                self.last_clipboard = ctxt
                if not self.killBuffer or self.killBuffer [0] != ctxt:
                    return ctxt
        except: pass
    
        return None
    #@nonl
    #@-node:ekr.20050920084036.185:getClipboard
    #@+node:ekr.20050920084036.184:iterateKillBuffer
    def iterateKillBuffer( self ):
        
        while 1:
            if self.killBuffer:
                self.last_clipboard = None
                for z in self.killBuffer:
                    if self.reset:
                        self.reset = False
                        break        
                    yield z
    #@-node:ekr.20050920084036.184:iterateKillBuffer
    #@+node:ekr.20050920084036.178:kill, killLine, killWord
    def kill (self,event,frm,to):
    
        k = self.k ; w = event.widget ; s = w.get(frm,to)
        self.addToKillBuffer(s)
        w.clipboard_clear()
        w.clipboard_append(s)
        w.delete(frm,to)
    
    def killLine (self,event):
        
        self.kill(event,'insert linestart','insert lineend+1c')
    
    def killWord (self,event):
        
        self.kill(event,'insert wordstart','insert wordend')
        self.killWs(event)
    #@-node:ekr.20050920084036.178:kill, killLine, killWord
    #@+node:ekr.20050920084036.182:killRegion & killRegionSave & helper
    def killRegion (self,event):
        self.killRegionHelper(event,deleteFlag=True)
        
    def killRegionSave (self,event):
        self.killRegionHelper(event,deleteFlag=False)
    
    def killRegionHelper (self,event,deleteFlag):
    
        w = event.widget ; theRange = w.tag_ranges('sel')
    
        if len(theRange) != 0:
            s = w.get(theRange[0],theRange[-1])
            if deleteFlag:
                w.delete(theRange[0],theRange[-1])
            self.addToKillBuffer(s)
            w.clipboard_clear()
            w.clipboard_append(s)
    
        self.removeRKeys(w)
    #@nonl
    #@-node:ekr.20050920084036.182:killRegion & killRegionSave & helper
    #@+node:ekr.20050930095323.1:killSentence
    def killSentence (self,event):
    
        w = event.widget
        i  = w.search('.','insert',stopindex='end')
        if i:
            i2 = w.search('.','insert',backwards=True,stopindex='1.0')
            i2 = g.choose(i2=='','1.0',i2+'+1c ')
            self.kill(event,i2,'%s + 1c' % i)
    #@nonl
    #@-node:ekr.20050930095323.1:killSentence
    #@+node:ekr.20050930100733:killWs
    def killWs (self,event):
        
        ws = '' ; w = event.widget
    
        while 1:
            s = w.get('insert')
            if s in (' ','\t'):
                w.delete('insert')
                ws = ws + s
            else:
                break
                
        if ws:
            self.addToKillBuffer(ws)
    #@nonl
    #@-node:ekr.20050930100733:killWs
    #@+node:ekr.20050930091642.1:yank
    def yank (self,event):
    
        k = self.k ; w = self.w
        i = w.index('insert')
        clip_text = self.getClipboard(w)
    
        if self.killBuffer or clip_text:
            self.reset = True
            s = clip_text or self.kbiterator.next()
            w.tag_delete('kb')
            w.insert('insert',s,('kb'))
            w.mark_set('insert',i)
    #@nonl
    #@-node:ekr.20050930091642.1:yank
    #@+node:ekr.20050930091642.2:yankPop
    def yankPop (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert') ; t, t1 = i.split('.')
        clip_text = self.getClipboard(w)
    
        if self.killBuffer or clip_text:
            if clip_text: s = clip_text
            else:         s = self.kbiterator.next()
            t1 = str(int(t1)+len(s))
            r = w.tag_ranges('kb')
            if r and r [0] == i:
                w.delete(r[0],r[-1])
            w.tag_delete('kb')
            w.insert('insert',s,('kb'))
            w.mark_set('insert',i)
    #@nonl
    #@-node:ekr.20050930091642.2:yankPop
    #@+node:ekr.20050920084036.128:zapToCharacter
    def zapToCharacter (self,event):
    
        k = self.k ; state = k.getState('zap-to-char')
    
        if state == 0:
            k.setLabelBlue('Zap To Character: ',protect=True)
            k.setState('zap-to-char',1,handler=self.zapToCharacter)
        else:
            c = k.c ; w = event.widget ; ch = event.char
            k.resetLabel()
            k.clearState()
            if (
                len(event.char) != 0 and
                ch in (string.ascii_letters + string.digits + string.punctuation)
            ):
                i = w.search(ch,'insert',stopindex='end')
                if i:
                    t = w.get('insert','%s+1c' % i)
                    self.addToKillBuffer(t)
                    w.delete('insert','%s+1c' % i)
    #@nonl
    #@-node:ekr.20050920084036.128:zapToCharacter
    #@-others
#@nonl
#@-node:ekr.20050920084036.174:class killBufferCommandsClass
#@+node:ekr.20050920084036.186:class leoCommandsClass
class leoCommandsClass (baseEditCommandsClass):
    
    #@    @+others
    #@+node:ekr.20050920084036.187: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    #@nonl
    #@-node:ekr.20050920084036.187: ctor
    #@+node:ekr.20050920084036.188:leoCommands.getPublicCommands
    def getPublicCommands (self):
        
        '''(leoCommands) Return a dict of the 'legacy' Leo commands.'''
        
        k = self.k ; d2 = {}
        
        #@    << define dictionary d of names and Leo commands >>
        #@+node:ekr.20050920084036.189:<< define dictionary d of names and Leo commands >>
        c = self.c ; f = c.frame
        
        d = {
            'abort-edit-headline':          f.abortEditLabelCommand,
            'about-leo':                    c.about,
            'add-comments':                 c.addComments,     
            'cascade-windows':              f.cascade,
            'clear-recent-files':           c.clearRecentFiles,
            'close-window':                 c.close,
            'contract-or-go-left':          c.contractNodeOrGoToParent,
            'check-python-code':            c.checkPythonCode,
            'check-all-python-code':        c.checkAllPythonCode,
            'check-outline':                c.checkOutline,
            'clear-recent-files':           c.clearRecentFiles,
            'clone-node':                   c.clone,
            'contract-node':                c.contractNode,
            'contract-all':                 c.contractAllHeadlines,
            'contract-parent':              c.contractParent,
            'convert-all-blanks':           c.convertAllBlanks,
            'convert-all-tabs':             c.convertAllTabs,
            'convert-blanks':               c.convertBlanks,
            'convert-tabs':                 c.convertTabs,
            'copy-node':                    c.copyOutline,
            'copy-text':                    f.copyText,
            'cut-node':                     c.cutOutline,
            'cut-text':                     f.cutText,
            'de-hoist':                     c.dehoist,
            'delete-comments':              c.deleteComments,
            'delete-node':                  c.deleteOutline,
            'demote':                       c.demote,
            'dump-outline':                 c.dumpOutline,
            'edit-headline':                c.editHeadline,
            'end-edit-headline':            f.endEditLabelCommand,
            'equal-sized-panes':            f.equalSizedPanes,
            'execute-script':               c.executeScript,
            'exit-leo':                     g.app.onQuit,
            'expand-all':                   c.expandAllHeadlines,
            'expand-next-level':            c.expandNextLevel,
            'expand-node':                  c.expandNode,
            'expand-and-go-right':          c.expandNodeAndGoToFirstChild,
            'expand-or-go-right':           c.expandNodeOrGoToFirstChild,
            'expand-prev-level':            c.expandPrevLevel,
            'expand-to-level-1':            c.expandLevel1,
            'expand-to-level-2':            c.expandLevel2,
            'expand-to-level-3':            c.expandLevel3,
            'expand-to-level-4':            c.expandLevel4,
            'expand-to-level-5':            c.expandLevel5,
            'expand-to-level-6':            c.expandLevel6,
            'expand-to-level-7':            c.expandLevel7,
            'expand-to-level-8':            c.expandLevel8,
            'expand-to-level-9':            c.expandLevel9,
            'export-headlines':             c.exportHeadlines,
            'extract':                      c.extract,
            'extract-names':                c.extractSectionNames,
            'extract-section':              c.extractSection,
            'flatten-outline':              c.flattenOutline,
            'go-back':                      c.goPrevVisitedNode,
            'go-forward':                   c.goNextVisitedNode,
            'goto-first-node':              c.goToFirstNode,
            'goto-first-sibling':           c.goToFirstSibling,
            'goto-last-node':               c.goToLastNode,
            'goto-last-sibling':            c.goToLastSibling,
            'goto-last-visible':            c.goToLastVisibleNode,
            'goto-line-number':             c.goToLineNumber,
            'goto-next-changed':            c.goToNextDirtyHeadline,
            'goto-next-clone':              c.goToNextClone,
            'goto-next-marked':             c.goToNextMarkedHeadline,
            'goto-next-node':               c.selectThreadNext,
            'goto-next-sibling':            c.goToNextSibling,
            'goto-next-visible':            c.selectVisNext,
            'goto-parent':                  c.goToParent,
            'goto-prev-node':               c.selectThreadBack,
            'goto-prev-sibling':            c.goToPrevSibling,
            'goto-prev-visible':            c.selectVisBack,
            'hoist':                        c.hoist,
            'import-at-file':               c.importAtFile,
            'import-at-root':               c.importAtRoot,
            'import-cweb-files':            c.importCWEBFiles,
            'import-derived-file':          c.importDerivedFile,
            'import-flattened-outline':     c.importFlattenedOutline,
            'import-noweb-files':           c.importNowebFiles,
            'indent-region':                c.indentBody,
            'insert-node':                  c.insertHeadline,
            'insert-body-time':             c.insertBodyTime,
            'insert-headline-time':         f.insertHeadlineTime,
            'mark':                         c.markHeadline,
            'mark-changed-items':           c.markChangedHeadlines,
            'mark-changed-roots':           c.markChangedRoots,
            'mark-clones':                  c.markClones,
            'mark-subheads':                c.markSubheads,
            'match-bracket':                c.findMatchingBracket,
            'minimize-all':                 f.minimizeAll,
            'move-outline-down':            c.moveOutlineDown,
            'move-outline-left':            c.moveOutlineLeft,
            'move-outline-right':           c.moveOutlineRight,
            'move-outline-up':              c.moveOutlineUp,
            'new':                          c.new,
            'open-compare-window':          c.openCompareWindow,
            'open-find-dialog':             c.showFindPanel, # Deprecated.
            'open-leoDocs-leo':             c.leoDocumentation,
            'open-leoPlugins-leo':          c.openLeoPlugins,
            'open-leoSettings-leo':         c.openLeoSettings,
            'open-online-home':             c.leoHome,
            'open-online-tutorial':         c.leoTutorial,
            'open-offline-tutorial':        f.leoHelp,
            'open-outline':                 c.open,
            'open-python-window':           c.openPythonWindow,
            'open-with':                    c.openWith,
            'outline-to-CWEB':              c.outlineToCWEB,
            'outline-to-noweb':             c.outlineToNoweb,
            'paste-node':                   c.pasteOutline,
            'paste-retaining-clones':       c.pasteOutlineRetainingClones,
            'paste-text':                   f.pasteText,
            'pretty-print-all-python-code': c.prettyPrintAllPythonCode,
            'pretty-print-python-code':     c.prettyPrintPythonCode,
            'promote':                      c.promote,
            'read-at-file-nodes':           c.readAtFileNodes,
            'read-outline-only':            c.readOutlineOnly,
            'redo':                         c.undoer.redo,
            'reformat-paragraph':           c.reformatParagraph,
            'remove-sentinels':             c.removeSentinels,
            'resize-to-screen':             f.resizeToScreen,
            'revert':                       c.revert,
            'save-file':                    c.save,
            'save-file-as':                 c.saveAs,
            'save-file-to':                 c.saveTo,
            'select-all':                   f.body.selectAllText,
            'settings':                     c.preferences,
            'set-colors':                   c.colorPanel,
            'set-font':                     c.fontPanel,
            'show-invisibles':              c.viewAllCharacters,
            'sort-children':                c.sortChildren,
            'sort-siblings':                c.sortSiblings,
            'tangle':                       c.tangle,
            'tangle-all':                   c.tangleAll,
            'tangle-marked':                c.tangleMarked,
            'toggle-active-pane':           f.toggleActivePane,
            'toggle-angle-brackets':        c.toggleAngleBrackets,
            'toggle-split-direction':       f.toggleSplitDirection,
            'undo':                         c.undoer.undo,
            'unindent-region':              c.dedentBody,
            'unmark-all':                   c.unmarkAll,
            'untangle':                     c.untangle,
            'untangle-all':                 c.untangleAll,
            'untangle-marked':              c.untangleMarked,
            'weave':                        c.weave,
            'write-at-file-nodes':          c.fileCommands.writeAtFileNodes,
            'write-dirty-at-file-nodes':    c.fileCommands.writeDirtyAtFileNodes,
            'write-missing-at-file-nodes':  c.fileCommands.writeMissingAtFileNodes,
            'write-outline-only':           c.fileCommands.writeOutlineOnly,
        }
        #@nonl
        #@-node:ekr.20050920084036.189:<< define dictionary d of names and Leo commands >>
        #@nl
        
        # Create a callback for each item in d.
        keys = d.keys() ; keys.sort()
        for name in keys:
            f = d.get(name)
            d2 [name] = f
            k.inverseCommandsDict [f.__name__] = name
            # g.trace('leoCommands %24s = %s' % (f.__name__,name))
            
        return d2
    #@nonl
    #@-node:ekr.20050920084036.188:leoCommands.getPublicCommands
    #@-others
#@nonl
#@-node:ekr.20050920084036.186:class leoCommandsClass
#@+node:ekr.20050920084036.190:class macroCommandsClass
class macroCommandsClass (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.191: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    
        self.lastMacro = None
        self.macs = []
        self.macro = []
        self.namedMacros = {}
        
        # Important: we must not interfere with k.state in startKbdMacro!
        self.recordingMacro = False
    #@nonl
    #@-node:ekr.20050920084036.191: ctor
    #@+node:ekr.20050920084036.192: getPublicCommands
    def getPublicCommands (self):
    
        return {
            # 'call-last-keyboard-macro': self.callLastKeyboardMacro,
            # 'end-kbd-macro':            self.endKbdMacro,
            # 'name-last-kbd-macro':      self.nameLastKbdMacro,
            # 'load-file':                self.loadFile,
            # 'insert-keyboard-macro' :   self.insertKeyboardMacro,
            # 'start-kbd-macro':          self.startKbdMacro,
        }
    #@nonl
    #@-node:ekr.20050920084036.192: getPublicCommands
    #@+node:ekr.20050920084036.193:Entry points
    #@+node:ekr.20050920084036.194:insertKeyboardMacro
    def insertKeyboardMacro (self,event):
    
        '''A method to save your macros to file.'''
    
        k = self.k ; state = k.getState('macro-name')
        prompt = 'Macro name: '
    
        if state == 0:
            k.setLabelBlue(prompt,protect=True)
            k.getArg(event,'macro-name',1,self.insertKeyboardMacro)
        else:
            ch = event.keysym ; s = s = k.getLabel(ignorePrompt=True)
            g.trace(repr(ch),repr(s))
            if ch == 'Return':
                k.clearState()
                self.saveMacros(event,s)
            elif ch == 'Tab':
                k.setLabel('%s%s' % (
                    prompt,self.findFirstMatchFromList(s,self.namedMacros)),
                    prompt=prompt,protect=True)
            else:
                k.updateLabel(event)
    #@nonl
    #@+node:ekr.20050920084036.195:findFirstMatchFromList
    def findFirstMatchFromList (self,s,aList=None):
    
        '''This method finds the first match it can find in a sorted list'''
    
        k = self.k ; c = k.c
    
        if aList is not None:
            aList = c.commandsDict.keys()
    
        pmatches = [item for item in aList if item.startswith(s)]
        pmatches.sort()
        if pmatches:
            mstring = reduce(g.longestCommonPrefix,pmatches)
            return mstring
    
        return s
    #@nonl
    #@-node:ekr.20050920084036.195:findFirstMatchFromList
    #@-node:ekr.20050920084036.194:insertKeyboardMacro
    #@+node:ekr.20050920084036.196:loadFile & helpers
    def loadFile (self,event):
    
        '''Asks for a macro file name to load.'''
    
        f = tkFileDialog and tkFileDialog.askopenfile()
        if f:
            self._loadMacros(f)
    #@nonl
    #@+node:ekr.20050920084036.197:_loadMacros
    def _loadMacros (self,f):
    
        '''Loads a macro file into the macros dictionary.'''
    
        k = self.k
        macros = cPickle.load(f)
        for z in macros:
            k.addToDoAltX(z,macros[z])
    #@nonl
    #@-node:ekr.20050920084036.197:_loadMacros
    #@-node:ekr.20050920084036.196:loadFile & helpers
    #@+node:ekr.20050920084036.198:nameLastKbdMacro
    def nameLastKbdMacro (self,event):
    
        '''Names the last macro defined.'''
    
        k = self.k ; state = k.getState('name-macro')
        
        if state == 0:
            k.setLabelBlue('Name of macro: ',protect=True)
            k.getArg(event,'name-macro',1,self.nameLastKbdMacro)
        else:
            k.clearState()
            name = k.arg
            k.addToDoAltX(name,self.lastMacro)
            k.setLabelGrey('Macro defined: %s' % name)
    #@nonl
    #@-node:ekr.20050920084036.198:nameLastKbdMacro
    #@+node:ekr.20050920084036.199:saveMacros & helper
    def saveMacros (self,event,macname):
    
        '''Asks for a file name and saves it.'''
    
        name = tkFileDialog and tkFileDialog.asksaveasfilename()
        if name:
            f = file(name,'a+')
            f.seek(0)
            if f:
                self._saveMacros(f,macname)
    #@nonl
    #@+node:ekr.20050920084036.200:_saveMacros
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
    #@-node:ekr.20050920084036.200:_saveMacros
    #@-node:ekr.20050920084036.199:saveMacros & helper
    #@+node:ekr.20050920084036.204:startKbdMacro
    def startKbdMacro (self,event):
    
        k = self.k
        
        if not self.recordingMacro:
            self.recordingMacro = True
            k.setLabelBlue('Recording keyboard macro...',protect=True)
        else:
            stroke = k.stroke ; keysym = event.keysym
            if stroke == '<Key>' and keysym in ('Control_L','Alt_L','Shift_L'):
                return False
            g.trace('stroke',stroke,'keysym',keysym)
            if stroke == '<Key>' and keysym =='parenright':
                self.endKbdMacro(event)
                return True
            elif stroke == '<Key>':
                self.macro.append((event.keycode,event.keysym))
                return True
            else:
                self.macro.append((stroke,event.keycode,event.keysym,event.char))
                return True
    #@nonl
    #@-node:ekr.20050920084036.204:startKbdMacro
    #@+node:ekr.20050920084036.206:endKbdMacro
    def endKbdMacro (self,event):
    
        k = self.k ; self.recordingMacro = False
    
        if self.macro:
            self.macro = self.macro [: -4]
            self.macs.insert(0,self.macro)
            self.lastMacro = self.macro[:]
            self.macro = []
            k.setLabelGrey('Keyboard macro defined, not named')
        else:
            k.setLabelGrey('Empty keyboard macro')
    #@nonl
    #@-node:ekr.20050920084036.206:endKbdMacro
    #@+node:ekr.20050920084036.202:callLastKeyboardMacro & helper (called from universal command)
    def callLastKeyboardMacro (self,event):
    
        w = event.widget
    
        if self.lastMacro:
            self._executeMacro(self.lastMacro,w)
    #@nonl
    #@+node:ekr.20050920084036.203:_executeMacro (revise)
    def _executeMacro (self,macro,w):
    
        k = self.k
    
        for z in macro:
            if len(z) == 2:
                w.event_generate('<Key>',keycode=z[0],keysym=z[1])
            else:
                meth = z [0].lstrip('<').rstrip('>')
                bunchList = k.bindingsDict.get(meth,[])  ### Probably should not strip < and >
                if bunchList:
                    b = bunchList[0]
                    ev = Tk.Event()
                    ev.widget = w
                    ev.keycode = z [1]
                    ev.keysym = z [2]
                    ev.char = z [3]
                    k.masterCommand(ev,b.f,'<%s>' % meth)
    #@nonl
    #@-node:ekr.20050920084036.203:_executeMacro (revise)
    #@-node:ekr.20050920084036.202:callLastKeyboardMacro & helper (called from universal command)
    #@-node:ekr.20050920084036.193:Entry points
    #@+node:ekr.20051006065746:Common Helpers
    #@+node:ekr.20050920085536.15:addToDoAltX
    # Called from loadFile and nameLastKbdMacro.
    
    def addToDoAltX (self,name,macro):
    
        '''Adds macro to Alt-X commands.'''
        
        k= self ; c = k.c
    
        if c.commandsDict.has_key(name):
            return False
    
        def func (event,macro=macro):
            return self._executeMacro(macro,event.widget)
    
        c.commandsDict [name] = func
        self.namedMacros [name] = macro
        return True
    #@nonl
    #@-node:ekr.20050920085536.15:addToDoAltX
    #@-node:ekr.20051006065746:Common Helpers
    #@-others
#@nonl
#@-node:ekr.20050920084036.190:class macroCommandsClass
#@+node:ekr.20050920084036.207:class queryReplaceCommandsClass (limited to single node)
class queryReplaceCommandsClass (baseEditCommandsClass):
    
    '''A class to handle query replace commands.'''

    #@    @+others
    #@+node:ekr.20050920084036.208: ctor & init
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
        self.regexp = False # True: do query-replace-regexp.  Set in stateHandler.
        
    def init (self):
        
        self.qQ = None
        self.qR = None
        self.replaced = 0 # The number of replacements.
    #@-node:ekr.20050920084036.208: ctor & init
    #@+node:ekr.20050920084036.209: getPublicCommands
    def getPublicCommands (self):
    
        return {
            'query-replace':        self.queryReplace,
            'query-replace-regex':  self.queryReplaceRegex,
        }
    #@nonl
    #@-node:ekr.20050920084036.209: getPublicCommands
    #@+node:ekr.20050920084036.210:Entry points
    def queryReplace (self,event):
    
        self.regexp = False
        self.stateHandler(event)
    
    def queryReplaceRegex (self,event):
        
        self.regexp = True
        self.stateHandler(event)
    #@-node:ekr.20050920084036.210:Entry points
    #@+node:ekr.20051005151838:Helpers
    #@+node:ekr.20050920084036.212:doOneReplace
    def doOneReplace (self,event):
    
        i = event.widget.tag_ranges('qR')
        event.widget.delete(i[0],i[1])
        event.widget.insert('insert',self.qR)
        self.replaced += 1
    #@nonl
    #@-node:ekr.20050920084036.212:doOneReplace
    #@+node:ekr.20050920084036.219:findNextMatch
    def findNextMatch (self,event):
        
        '''Find the next match and select it.
        Return True if a match was found.
        Otherwise, call quitSearch and return False.'''
    
        k = self.k ; w = event.widget
        
        w.tag_delete('qR')
    
        if self.regexp:
            #@        << handle regexp >>
            #@+node:ekr.20051005155611:<< handle regexp >>
            try:
                regex = re.compile(self.qQ)
            except:
                self.quitSearch(event,'Illegal regular expression')
                return False
            
            txt = w.get('insert','end')
            match = regex.search(txt)
            
            if match:
                start = match.start()
                end = match.end()
                length = end - start
                w.mark_set('insert','insert +%sc' % start)
                ### w.update_idletasks()
                w.tag_add('qR','insert','insert +%sc' % length)
                w.tag_config('qR',background='lightblue')
                txt = w.get('insert','insert +%sc' % length)
                return True
            else:
                self.quitSearch(event)
                return False
            #@nonl
            #@-node:ekr.20051005155611:<< handle regexp >>
            #@nl
        else:
            #@        << handle plain search >>
            #@+node:ekr.20051005160923:<< handle plain search >>
            i = w.search(self.qQ,'insert',stopindex='end')
            if i:
                w.mark_set('insert',i)
                ###w.update_idletasks()
                w.tag_add('qR','insert','insert +%sc' % len(self.qQ))
                w.tag_config('qR',background='lightblue')
                return True
            else:
                self.quitSearch(event)
                return False
            #@nonl
            #@-node:ekr.20051005160923:<< handle plain search >>
            #@nl
    #@nonl
    #@-node:ekr.20050920084036.219:findNextMatch
    #@+node:ekr.20050920084036.211:getUserResponse
    def getUserResponse (self,event):
        
        w = event.widget
        # g.trace(event.keysym)
    
        if event.keysym == 'y':
            self.doOneReplace(event)
            if not self.findNextMatch(event):
                self.quitSearch(event)
        elif event.keysym in ('q','Return'):
            self.quitSearch(event)
        elif event.keysym == 'exclam':
            while self.findNextMatch(event):
                self.doOneReplace(event)
        elif event.keysym in ('n','Delete'):
            # Skip over the present match.
            w.mark_set('insert','insert +%sc' % len(self.qQ))
            if not self.findNextMatch(event):
                self.quitSearch(event)
    
        w.see('insert')
    #@nonl
    #@-node:ekr.20050920084036.211:getUserResponse
    #@+node:ekr.20050920084036.220:quitSearch
    def quitSearch (self,event,message=None):
    
        k = self.k ; w = event.widget
        w.tag_delete('qR')
        k.clearState()
        if message is None:
            message = 'Replaced %d occurences' % self.replaced
        k.setLabelGrey(message)
    #@nonl
    #@-node:ekr.20050920084036.220:quitSearch
    #@+node:ekr.20050920084036.215:stateHandler
    def stateHandler (self,event):
        
        k = self.k ; state = k.getState('query-replace')
        
        prompt = g.choose(self.regexp,'Query replace regexp','Query replace')
        
        if state == 0: # Get the first arg.
            self.init()
            k.setLabelBlue(prompt + ': ',protect=True)
            k.getArg(event,'query-replace',1,self.stateHandler)
        elif state == 1: # Get the second arg.
            self.qQ = k.arg
            if len(k.arg) > 0:
                prompt = '%s %s with: ' % (prompt,k.arg)
                k.setLabelBlue(prompt)
                k.getArg(event,'query-replace',2,self.stateHandler)
            else:
                k.resetLabel()
                k.clearState()
        elif state == 2: # Set the prompt and find the first match.
            self.qR = k.arg # Null replacement arg is ok.
            k.setLabelBlue('Query replacing %s with %s\n' % (self.qQ,self.qR) +
                'y: replace, (n or Delete): skip, !: replace all, (q or Return): quit',
                protect=True)
            k.setState('query-replace',3,self.stateHandler)
            self.findNextMatch(event)
        elif state == 3:
            self.getUserResponse(event)
    #@nonl
    #@-node:ekr.20050920084036.215:stateHandler
    #@-node:ekr.20051005151838:Helpers
    #@-others
#@nonl
#@-node:ekr.20050920084036.207:class queryReplaceCommandsClass (limited to single node)
#@+node:ekr.20050920084036.221:class rectangleCommandsClass
class rectangleCommandsClass (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.222: ctor & finishCreate
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.theKillRectangle = [] # Do not re-init this!
        self.stringRect = None
        
    def finishCreate(self):
        
        baseEditCommandsClass.finishCreate(self)
        
        self.commandsDict = {
            'c': ('clear-rectangle',    self.clearRectangle),
            'd': ('delete-rectangle',   self.deleteRectangle),
            'k': ('kill-rectangle',     self.killRectangle),
            'o': ('open-rectangle',     self.openRectangle),
            'r': ('copy-rectangle-to-register',
                self.c.registerCommands.copyRectangleToRegister),
            't': ('string-rectangle',   self.stringRectangle),
            'y': ('yank-rectangle',     self.yankRectangle),
        }
    #@-node:ekr.20050920084036.222: ctor & finishCreate
    #@+node:ekr.20051004112630:check
    def check (self,event=None,warning='No rectangle selected'):
        
        '''Return True if there is a selection.
        Otherwise, return False and issue a warning.'''
    
        return self._chckSel(event,warning)
    #@nonl
    #@-node:ekr.20051004112630:check
    #@+node:ekr.20050920084036.223:getPublicCommands
    def getPublicCommands (self):
    
        return {
            'clear-rectangle':  self.clearRectangle,
            'close-rectangle':  self.closeRectangle,
            'delete-rectangle': self.deleteRectangle,
            'kill-rectangle':   self.killRectangle,
            'open-rectangle':   self.openRectangle,
            'string-rectangle': self.stringRectangle,
            'yank-rectangle':   self.yankRectangle,
        }
    #@nonl
    #@-node:ekr.20050920084036.223:getPublicCommands
    #@+node:ekr.20051215103053:beginCommand & beginCommandWithEvent (rectangle)
    def beginCommand (self,undoType='Typing'):
    
        w = baseEditCommandsClass.beginCommand(self,undoType)
    
        r1, r2, r3, r4 = self.getRectanglePoints()
    
        return w, r1, r2, r3, r4
        
    def beginCommandWithEvent (self,event,undoType='Typing'):
        
        '''Do the common processing at the start of each command.'''
        
        w = baseEditCommandsClass.beginCommandWithEvent(self,event,undoType)
        
        r1, r2, r3, r4 = self.getRectanglePoints()
    
        return w, r1, r2, r3, r4
    #@nonl
    #@-node:ekr.20051215103053:beginCommand & beginCommandWithEvent (rectangle)
    #@+node:ekr.20050920084036.224:Entries
    #@+node:ekr.20050920084036.225:clearRectangle
    def clearRectangle (self,event):
    
        if not self.check(): return
        
        w,r1,r2,r3,r4 = self.beginCommand('clear-rectangle')
    
        # Change the text.
        
        s = ' ' * (r4-r2)
        for r in xrange(r1,r3+1):
            w.delete('%s.%s' % (r,r2),'%s.%s' % (r,r4))
            w.insert('%s.%s' % (r,r2),s)
            
        self.endCommand()
    #@nonl
    #@-node:ekr.20050920084036.225:clearRectangle
    #@+node:ekr.20050920084036.226:closeRectangle
    def closeRectangle (self,event):
        
        '''Delete the rectangle if it contains nothing but whitespace..'''
    
        if not self.check(): return
    
        w,r1,r2,r3,r4 = self.beginCommand('close-rectangle')
      
        # Return if any part of the selection contains something other than whitespace.
        for r in xrange(r1,r3+1):
            s = w.get('%s.%s' % (r,r2),'%s.%s' % (r,r4))
            if s.strip(): return
    
        # Change the text.
        for r in xrange(r1,r3+1):
            w.delete('%s.%s' % (r,r2),'%s.%s' % (r,r4))
            
        self.endCommand()
    #@nonl
    #@-node:ekr.20050920084036.226:closeRectangle
    #@+node:ekr.20050920084036.227:deleteRectangle
    def deleteRectangle (self,event):
    
        if not self.check(): return
        
        w,r1,r2,r3,r4 = self.beginCommand('delete-rectangle')
    
        for r in xrange(r1,r3+1):
            w.delete('%s.%s' % (r,r2),'%s.%s' % (r,r4))
            
        self.endCommand()
    #@nonl
    #@-node:ekr.20050920084036.227:deleteRectangle
    #@+node:ekr.20050920084036.228:killRectangle
    def killRectangle (self,event):
    
        if not self.check(event): return
        
        w,r1,r2,r3,r4 = self.beginCommand('kill-rectangle')
    
        self.theKillRectangle = []
        for r in xrange(r1,r3+1):
            s = w.get('%s.%s' % (r,r2),'%s.%s' % (r,r4))
            self.theKillRectangle.append(s)
            w.delete('%s.%s' % (r,r2),'%s.%s' % (r,r4))
    
        if self.theKillRectangle:
            w.mark_set('sel.start','insert')
            w.mark_set('sel.end','insert')
            
        self.endCommand()
    #@nonl
    #@-node:ekr.20050920084036.228:killRectangle
    #@+node:ekr.20050920084036.230:openRectangle
    def openRectangle (self,event):
        
        '''Insert blank space to fill the space of the region-rectangle.
        This pushes the previous contents of the region-rectangle rightward. '''
    
        if not self.check(event): return
        
        w,r1,r2,r3,r4 = self.beginCommand('open-rectangle')
        
        s = ' ' * (r4-r2)
        for r in xrange(r1,r3+1):
            w.insert('%s.%s' % (r,r2),s)
            
        self.endCommand()
    #@nonl
    #@-node:ekr.20050920084036.230:openRectangle
    #@+node:ekr.20050920084036.229:yankRectangle
    def yankRectangle (self,event,killRect=None):
        
        c = self.c ; k = self.k ; w = self.w
    
        killRect = killRect or self.theKillRectangle
        if not killRect:
            k.setLabelGrey('No kill rect')
            return
            
        w,r1,r2,r3,r4 = self.beginCommand('yank-rectangle')
        
        # Change the text.
        txt = w.get('insert linestart','insert')
        txt = self.getWSString(txt)
        i = w.index('insert')
        i1, i2 = i.split('.')
        i1 = int(i1)
        for z in killRect:
            txt2 = w.get('%s.0 linestart' % i1,'%s.%s' % (i1,i2))
            if len(txt2) != len(txt):
                amount = len(txt) - len(txt2)
                z = txt [-amount:] + z
            w.insert('%s.%s' % (i1,i2),z)
            if w.index('%s.0 lineend +1c' % i1) == w.index('end'):
                w.insert('%s.0 lineend' % i1,'\n')
            i1 += 1
    
        self.endCommand()
    #@nonl
    #@-node:ekr.20050920084036.229:yankRectangle
    #@+node:ekr.20050920084036.232:stringRectangle
    def stringRectangle (self,event):
        
        '''Replace the contents of a rectangle with a string on each line.'''
    
        c = self.c ; k = self.k ; w = self.w
        state = k.getState('string-rect')
        if state == 0:
            if not self.check(): return
            self.stringRect = self.getRectanglePoints()
            k.setLabelBlue('String rectangle: ',protect=True)
            k.getArg(event,'string-rect',1,self.stringRectangle)
        else:
            k.clearState()
            k.resetLabel()
            self.beginCommand('string-rectangle')
            r1, r2, r3, r4 = self.stringRect
            w.mark_set('sel.start','%d.%d' % (r1,r2))
            w.mark_set('sel.end',  '%d.%d' % (r3,r4))
            c.bodyWantsFocus()
            for r in xrange(r1,r3+1):
                w.delete('%s.%s' % (r,r2),'%s.%s' % (r,r4))
                w.insert('%s.%s' % (r,r2),k.arg)
            self.endCommand()
    #@-node:ekr.20050920084036.232:stringRectangle
    #@-node:ekr.20050920084036.224:Entries
    #@-others
#@nonl
#@-node:ekr.20050920084036.221:class rectangleCommandsClass
#@+node:ekr.20050920084036.234:class registerCommandsClass
class registerCommandsClass (baseEditCommandsClass):

    '''A class to represent registers a-z and the corresponding Emacs commands.'''

    #@    @+others
    #@+node:ekr.20051004095209:Birth
    #@+node:ekr.20050920084036.235: ctor, finishCreate & init
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
    
        self.methodDict, self.helpDict = self.addRegisterItems()
        self.init()
        
    def finishCreate (self):
        
        baseEditCommandsClass.finishCreate(self) # finish the base class.
        
        if self.k.useGlobalRegisters:
            self.registers = leoKeys.keyHandlerClass.global_registers
        else:
            self.registers = {}
            
    def init (self):
    
        self.method = None 
        self.registerMode = 0 # Must be an int.
    #@nonl
    #@-node:ekr.20050920084036.235: ctor, finishCreate & init
    #@+node:ekr.20050920084036.247: getPublicCommands
    def getPublicCommands (self):
        
        return {
            'append-to-register':           self.appendToRegister,
            'copy-rectangle-to-register':   self.copyRectangleToRegister,
            'copy-to-register':             self.copyToRegister,
            'increment-register':           self.incrementRegister,
            'insert-register':              self.insertRegister,
            'jump-to-register':             self.jumpToRegister,
            # 'number-to-register':           self.numberToRegister,
            'point-to-register':            self.pointToRegister,
            'prepend-to-register':          self.prependToRegister,
            'view-register':                self.viewRegister,
        }
    #@nonl
    #@-node:ekr.20050920084036.247: getPublicCommands
    #@+node:ekr.20050920084036.252:addRegisterItems (Not used!)
    def addRegisterItems( self ):
        
        methodDict = {
            'plus':     self.incrementRegister,
            'space':    self.pointToRegister,
            'a':        self.appendToRegister,
            'i':        self.insertRegister,
            'j':        self.jumpToRegister,
            # 'n':        self.numberToRegister,
            'p':        self.prependToRegister,
            'r':        self.copyRectangleToRegister,
            's':        self.copyToRegister,
            'v' :       self.viewRegister,
        }    
        
        helpDict = {
            's':    'copy to register',
            'i':    'insert from register',
            'plus': 'increment register',
            'n':    'number to register',
            'p':    'prepend to register',
            'a':    'append to register',
            'space':'point to register',
            'j':    'jump to register',
            'r':    'rectangle to register',
            'v': 'view register',
        }
    
        return methodDict, helpDict
    #@nonl
    #@-node:ekr.20050920084036.252:addRegisterItems (Not used!)
    #@-node:ekr.20051004095209:Birth
    #@+node:ekr.20051004123217:checkBodySelection
    def checkBodySelection (self,warning='No text selected'):
        
        return self._chckSel(event=None,warning=warning)
    #@nonl
    #@-node:ekr.20051004123217:checkBodySelection
    #@+node:ekr.20050920084036.236:Entries...
    #@+node:ekr.20050920084036.238:appendToRegister
    def appendToRegister (self,event):
    
        c = self.c ; k = self.k ; state = k.getState('append-to-reg')
        
        if state == 0:
            k.setLabelBlue('Append to register: ',protect=True)
            k.setState('append-to-reg',1,self.appendToRegister)
        else:
            k.clearState()
            if self.checkBodySelection():
                if event.keysym in string.letters:
                    w = c.frame.body.bodyCtrl
                    c.bodyWantsFocus()
                    key = event.keysym.lower()
                    val = self.registers.get(key,'')
                    try:
                        val = val + w.get('sel.first','sel.last')
                    except Exception:
                        pass
                    self.registers[key] = val
                    k.setLabelGrey('Register %s = %s' % (key,repr(val)))
                else:
                    k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.238:appendToRegister
    #@+node:ekr.20050920084036.237:prependToRegister
    def prependToRegister (self,event):
        
        c = self.c ; k = self.k ; state = k.getState('prepend-to-reg')
        
        if state == 0:
            k.setLabelBlue('Prepend to register: ',protect=True)
            k.setState('prepend-to-reg',1,self.prependToRegister)
        else:
            k.clearState()
            if self.checkBodySelection():
                if event.keysym in string.letters:
                    w = c.frame.body.bodyCtrl
                    c.bodyWantsFocus()
                    key = event.keysym.lower()
                    val = self.registers.get(key,'')
                    try:
                        val = w.get('sel.first','sel.last') + val
                    except Exception:
                        pass
                    self.registers[key] = val
                    k.setLabelGrey('Register %s = %s' % (key,repr(val)))
                else:
                    k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.237:prependToRegister
    #@+node:ekr.20050920084036.239:copyRectangleToRegister
    def copyRectangleToRegister (self,event):
    
        c = self.c ; k = self.k ; state = k.getState('copy-rect-to-reg')
    
        if state == 0:
            k.commandName = 'copy-rectangle-to-register'
            k.setLabelBlue('Copy Rectangle To Register: ',protect=True)
            k.setState('copy-rect-to-reg',1,self.copyRectangleToRegister)
        elif self.checkBodySelection('No rectangle selected'):
            k.clearState()
            if event.keysym in string.letters:
                key = event.keysym.lower()
                w = c.frame.body.bodyCtrl
                c.bodyWantsFocus()
                r1, r2, r3, r4 = self.getRectanglePoints()
                rect = []
                while r1 <= r3:
                    txt = w.get('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                    rect.append(txt)
                    r1 = r1 + 1
                self.registers [key] = rect
                k.setLabelGrey('Register %s = %s' % (key,repr(rect)))
            else:
                k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.239:copyRectangleToRegister
    #@+node:ekr.20050920084036.240:copyToRegister
    def copyToRegister (self,event):
        
        c = self.c ; k = self.k ; state = k.getState('copy-to-reg')
        
        if state == 0:
            k.commandName = 'copy-to-register'
            k.setLabelBlue('Copy to register: ',protect=True)
            k.setState('copy-to-reg',1,self.copyToRegister)
        else:
            k.clearState()
            if self.checkBodySelection():
                if event.keysym in string.letters:
                    key = event.keysym.lower()
                    w = c.frame.body.bodyCtrl
                    c.bodyWantsFocus()
                    try:
                        val = w.get('sel.first','sel.last')
                    except Exception:
                        g.es_exception()
                        val = ''
                    self.registers[key] = val
                    k.setLabelGrey('Register %s = %s' % (key,repr(val)))
                else:
                    k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.240:copyToRegister
    #@+node:ekr.20050920084036.241:incrementRegister
    def incrementRegister (self,event):
        
        c = self.c ; k = self.k ; state = k.getState('increment-reg')
        
        if state == 0:
            k.setLabelBlue('Increment register: ',protect=True)
            k.setState('increment-reg',1,self.incrementRegister)
        else:
            k.clearState()
            if self._checkIfRectangle(event):
                pass # Error message is in the label.
            elif event.keysym in string.letters:
                key = event.keysym.lower()
                val = self.registers.get(key,0)
                try:
                    val = str(int(val)+1)
                    self.registers[key] = val
                    k.setLabelGrey('Register %s = %s' % (key,repr(val)))
                except ValueError:
                    k.setLabelGrey("Can't increment register %s = %s" % (key,val))
            else:
                k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@-node:ekr.20050920084036.241:incrementRegister
    #@+node:ekr.20050920084036.242:insertRegister
    def insertRegister (self,event):
        
        c = self.c ; k = self.k ; state = k.getState('insert-reg')
        
        if state == 0:
            k.commandName = 'insert-register'
            k.setLabelBlue('Insert register: ',protect=True)
            k.setState('insert-reg',1,self.insertRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                w = c.frame.body.bodyCtrl
                c.bodyWantsFocus()
                key = event.keysym.lower()
                val = self.registers.get(key)
                if val:
                    if type(val)==type([]):
                        c.rectangleCommands.yankRectangle(val)
                    else:
                        w.insert('insert',val)
                    k.setLabelGrey('Inserted register %s' % key)
                else:
                    k.setLabelGrey('Register %s is empty' % key)
            else:
                k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.242:insertRegister
    #@+node:ekr.20050920084036.243:jumpToRegister
    def jumpToRegister (self,event):
    
        c = self.c ; k = self.k ; state = k.getState('jump-to-reg')
    
        if state == 0:
            k.setLabelBlue('Jump to register: ',protect=True)
            k.setState('jump-to-reg',1,self.jumpToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                if self._checkIfRectangle(event): return
                key = event.keysym.lower()
                val = self.registers.get(key)
                w = c.frame.body.bodyCtrl
                c.bodyWantsFocus()
                if val:
                    try:
                        w.mark_set('insert',val)
                        k.setLabelGrey('At %s' % repr(val))
                    except Exception:
                        k.setLabelGrey('Register %s is not a valid location' % key)
                else:
                    k.setLabelGrey('Register %s is empty' % key)
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.243:jumpToRegister
    #@+node:ekr.20050920084036.244:numberToRegister (not used)
    #@+at
    # C-u number C-x r n reg
    #     Store number into register reg (number-to-register).
    # C-u number C-x r + reg
    #     Increment the number in register reg by number (increment-register).
    # C-x r g reg
    #     Insert the number from register reg into the buffer.
    #@-at
    #@@c
    
    def numberToRegister (self,event):
        
        k = self.k ; state = k.getState('number-to-reg')
        
        if state == 0:
            k.commandName = 'number-to-register'
            k.setLabelBlue('Number to register: ',protect=True)
            k.setState('number-to-reg',1,self.numberToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                # self.registers[event.keysym.lower()] = str(0)
                k.setLabelGrey('number-to-register not ready yet.')
            else:
                k.setLabelGrey('Register must be a letter')
    #@-node:ekr.20050920084036.244:numberToRegister (not used)
    #@+node:ekr.20050920084036.245:pointToRegister
    def pointToRegister (self,event):
        
        c = self.c ; k = self.k ; state = k.getState('point-to-reg')
        
        if state == 0:
            k.commandName = 'point-to-register'
            k.setLabelBlue('Point to register: ',protect=True)
            k.setState('point-to-reg',1,self.pointToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                w = c.frame.body.bodyCtrl
                c.bodyWantsFocus()
                key = event.keysym.lower()
                val = w.index('insert')
                self.registers[key] = val
                k.setLabelGrey('Register %s = %s' % (key,repr(val)))
            else:
                k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.245:pointToRegister
    #@+node:ekr.20050920084036.246:viewRegister
    def viewRegister (self,event):
    
        c = self.c ; k = self.k ; state = k.getState('view-reg')
        
        if state == 0:
            k.commandName = 'view-register'
            k.setLabelBlue('View register: ',protect=True)
            k.setState('view-reg',1,self.viewRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                key = event.keysym.lower()
                val = self.registers.get(key)
                k.setLabelGrey('Register %s = %s' % (key,repr(val)))
            else:
                k.setLabelGrey('Register must be a letter')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.246:viewRegister
    #@-node:ekr.20050920084036.236:Entries...
    #@-others
#@nonl
#@-node:ekr.20050920084036.234:class registerCommandsClass
#@+node:ekr.20051023094009:Search classes
#@+node:ekr.20060123125256:class minibufferFind (the findHandler)
class minibufferFind:

    '''An adapter class that implements minibuffer find commands using the (hidden) Find Tab.'''

    #@    @+others
    #@+node:ekr.20060123125317.2: ctor (minibufferFind)
    def __init__(self,c,finder):
    
        self.c = c
        self.k = c.k
        self.w = None
        self.finder = finder
        self.findTextList = []
        self.changeTextList = []
    #@nonl
    #@-node:ekr.20060123125317.2: ctor (minibufferFind)
    #@+node:ekr.20060124140114: Options
    #@+node:ekr.20060124123133:setFindScope
    def setFindScope(self,where):
        
        '''Set the find-scope radio buttons.
        
        `where` must be in ('node-only','entire-outline','suboutline-only'). '''
        
        h = self.finder
        
        if where in ('node-only','entire-outline','suboutline-only'):
            var = h.dict['radio-search-scope'].get()
            if var:
                h.dict["radio-search-scope"].set(where)
        else:
            g.trace('oops: bad `where` value: %s' % where)
    #@nonl
    #@-node:ekr.20060124123133:setFindScope
    #@+node:ekr.20060124122844:setOption
    def setOption (self, ivar, val):
        
        h = self.finder
    
        if ivar in h.intKeys:
            if val is not None:
                var = h.dict.get(ivar)
                var.set(val)
                # g.trace('%s = %s' % (ivar,val))
    
        elif not g.app.unitTesting:
            g.trace('oops: bad find ivar %s' % ivar)
    #@nonl
    #@-node:ekr.20060124122844:setOption
    #@+node:ekr.20060125082510:getOption
    def getOption (self,ivar,verbose=False):
        
        h = self.finder
        
        var = h.dict.get(ivar)
        if var:
            val = var.get()
            verbose and g.trace('%s = %s' % (ivar,val))
            return val
        else:
            g.trace('bad ivar name: %s' % ivar)
            return None
    #@nonl
    #@-node:ekr.20060125082510:getOption
    #@+node:ekr.20060125074939:showFindOptions
    def showFindOptions (self):
        
        '''Show the present find options in the status line.'''
        
        frame = self.c.frame ; z = []
        # Set the scope field.
        head  = self.getOption('search_headline')
        body  = self.getOption('search_body')
        scope = self.getOption('radio-search-scope')
        d = {'entire-outline':'all','suboutline-only':'tree','node-only':'node'}
        scope = d.get(scope) or ''
        head = g.choose(head,'head','')
        body = g.choose(body,'body','')
        sep = g.choose(head and body,'+','')
    
        frame.clearStatusLine()
        s = '%s%s%s %s  ' % (head,sep,body,scope)
        frame.putStatusLine(s,color='blue')
    
        # Set the type field.
        script = self.getOption('script_search')
        regex  = self.getOption('pattern_match')
        change = self.getOption('script_change')
        if script:
            s1 = '*Script-find'
            s2 = g.choose(change,'-change*','*')
            z.append(s1+s2)
        elif regex: z.append('regex')
        
        table = (
            ('reverse',         'reverse'),
            ('ignore_case',     'noCase'),
            ('whole_word',      'word'),
            ('wrap',            'wrap'),
            ('mark_changes',    'markChg'),
            ('mark_finds',      'markFnd'),
        )
            
        for ivar,s in table:
            val = self.getOption(ivar)
            if val: z.append(s)
    
        frame.putStatusLine(' '.join(z))
    #@nonl
    #@-node:ekr.20060125074939:showFindOptions
    #@+node:ekr.20060124135401:toggleOption
    def toggleOption (self, ivar):
        
        h = self.finder
    
        if ivar in h.intKeys:
            var = h.dict.get(ivar)
            val = not var.get()
            var.set(val)
            # g.trace('%s = %s' % (ivar,val),var)
        else:
            g.trace('oops: bad find ivar %s' % ivar)
    #@nonl
    #@-node:ekr.20060124135401:toggleOption
    #@+node:ekr.20060205105950:setupChangePattern
    def setupChangePattern (self,pattern):
        
        h = self.finder ; t = h.change_ctrl
        
        s = g.toUnicode(pattern,g.app.tkEncoding)
        
        t.delete('1.0','end')
        t.insert('1.0',s)
        
        h.update_ivars()
    #@nonl
    #@-node:ekr.20060205105950:setupChangePattern
    #@+node:ekr.20060125091234:setupSearchPattern
    def setupSearchPattern (self,pattern):
        
        h = self.finder ; t = h.find_ctrl
        
        s = g.toUnicode(pattern,g.app.tkEncoding)
        
        t.delete('1.0','end')
        t.insert('1.0',s)
        
        h.update_ivars()
    #@nonl
    #@-node:ekr.20060125091234:setupSearchPattern
    #@-node:ekr.20060124140114: Options
    #@+node:ekr.20060210180352:addChangeStringToLabel
    def addChangeStringToLabel (self,protect=True):
        
        c = self.c ; k = c.k ; h = self.finder ; t = h.change_ctrl
        
        c.frame.log.selectTab('Find')
        c.minibufferWantsFocusNow()
        
        s = t.get('1.0','end')
    
        while s.endswith('\n') or s.endswith('\r'):
            s = s[:-1]
    
        k.extendLabel(s,select=True,protect=protect)
    #@-node:ekr.20060210180352:addChangeStringToLabel
    #@+node:ekr.20060210164421:addFindStringToLabel
    def addFindStringToLabel (self,protect=True):
        
        c = self.c ; k = c.k ; h = self.finder ; t = h.find_ctrl
        
        c.frame.log.selectTab('Find')
        c.minibufferWantsFocusNow()
    
        s = t.get('1.0','end')
        while s.endswith('\n') or s.endswith('\r'):
            s = s[:-1]
    
        k.extendLabel(s,select=True,protect=protect)
    #@-node:ekr.20060210164421:addFindStringToLabel
    #@+node:ekr.20060128080201:cloneFindAll
    def cloneFindAll (self,event):
    
        k = self.k ; tag = 'clone-find-all'
        state = k.getState(tag)
    
        if state == 0:
            self.w = event and event.widget
            self.setupArgs(forward=None,regexp=None,word=None)
            k.setLabelBlue('Clone Find All: ',protect=True)
            k.getArg(event,tag,1,self.cloneFindAll)
        else:
            k.clearState()
            k.resetLabel()
            k.showStateAndMode()
            self.generalSearchHelper(k.arg,cloneFindAll=True)
    #@nonl
    #@-node:ekr.20060128080201:cloneFindAll
    #@+node:ekr.20060204120158:findAgain
    def findAgain (self,event):
    
        f = self.finder
        
        f.p = self.c.currentPosition()
        f.v = self.finder.p.v
    
        # This handles the reverse option.
        return f.findAgainCommand()
            
    #@nonl
    #@-node:ekr.20060204120158:findAgain
    #@+node:ekr.20060209064140:findAll
    def findAll (self,event):
    
        k = self.k ; state = k.getState('find-all')
        if state == 0:
            self.w = event and event.widget
            self.setupArgs(forward=True,regexp=False,word=True)
            k.setLabelBlue('Find All: ',protect=True)
            k.getArg(event,'find-all',1,self.findAll)
        else:
            k.clearState()
            k.resetLabel()
            k.showStateAndMode()
            self.generalSearchHelper(k.arg,findAll=True)
    #@nonl
    #@-node:ekr.20060209064140:findAll
    #@+node:ekr.20060205105950.1:generalChangeHelper
    def generalChangeHelper (self,find_pattern,change_pattern):
        
        # g.trace(repr(change_pattern))
        
        c = self.c
    
        self.setupSearchPattern(find_pattern)
        self.setupChangePattern(change_pattern)
        c.widgetWantsFocusNow(self.w)
    
        self.finder.p = self.c.currentPosition()
        self.finder.v = self.finder.p.v
    
        # This handles the reverse option.
        self.finder.findNextCommand()
    #@nonl
    #@-node:ekr.20060205105950.1:generalChangeHelper
    #@+node:ekr.20060124181213.4:generalSearchHelper
    def generalSearchHelper (self,pattern,cloneFindAll=False,findAll=False):
        
        c = self.c
        
        self.setupSearchPattern(pattern)
        c.widgetWantsFocusNow(self.w)
    
        self.finder.p = self.c.currentPosition()
        self.finder.v = self.finder.p.v
    
        if findAll:
             self.finder.findAllCommand()
        elif cloneFindAll:
             self.finder.cloneFindAllCommand()
        else:
            # This handles the reverse option.
            self.finder.findNextCommand()
    #@nonl
    #@-node:ekr.20060124181213.4:generalSearchHelper
    #@+node:ekr.20060210174441:lastStateHelper
    def lastStateHelper (self):
        
        k = self.k
        k.clearState()
        k.resetLabel()
        k.showStateAndMode()
    #@nonl
    #@-node:ekr.20060210174441:lastStateHelper
    #@+node:ekr.20050920084036.113:replaceString
    def replaceString (self,event):
    
        k = self.k ; tag = 'replace-string' ; state = k.getState(tag)
        pattern_match = self.getOption ('pattern_match')
        prompt = 'Replace ' + g.choose(pattern_match,'Regex','String')
        if state == 0:
            self.setupArgs(forward=None,regexp=None,word=None)
            prefix = '%s: ' % prompt
            self.stateZeroHelper(event,tag,prefix,self.replaceString)
        elif state == 1:
            self._sString = k.arg
            self.updateFindList(k.arg)
            s = '%s: %s With: ' % (prompt,self._sString)
            k.setLabelBlue(s,protect=True)
            self.addChangeStringToLabel()
            k.getArg(event,'replace-string',2,self.replaceString,completion=False,prefix=s)
        elif state == 2:
            self.updateChangeList(k.arg)
            self.lastStateHelper()
            self.generalChangeHelper(self._sString,k.arg)
    #@-node:ekr.20050920084036.113:replaceString
    #@+node:ekr.20060124140224.3:reSearchBackward/Forward
    def reSearchBackward (self,event):
    
        k = self.k ; tag = 're-search-backward' ; state = k.getState(tag)
        
        if state == 0:
            self.setupArgs(forward=False,regexp=True,word=None)
            self.stateZeroHelper(event,tag,'Regexp Search Backward:',self.reSearchBackward)
        else:
            self.updateFindList(k.arg)
            self.lastStateHelper()
            self.generalSearchHelper(k.arg)
    
    def reSearchForward (self,event):
    
        k = self.k ; tag = 're-search-forward' ; state = k.getState(tag)
        if state == 0:
            self.setupArgs(forward=True,regexp=True,word=None)
            self.stateZeroHelper(event,tag,'Regexp Search:',self.reSearchForward)
        else:
            self.updateFindList(k.arg)
            self.lastStateHelper()
            self.generalSearchHelper(k.arg)
    #@nonl
    #@-node:ekr.20060124140224.3:reSearchBackward/Forward
    #@+node:ekr.20060124140224.1:seachForward/Backward
    def searchBackward (self,event):
    
        k = self.k ; tag = 'search-backward' ; state = k.getState(tag)
    
        if state == 0:
            self.setupArgs(forward=False,regexp=False,word=False)
            self.stateZeroHelper(event,tag,'Search Backward: ',self.searchBackward)
        else:
            self.updateFindList(k.arg)
            self.lastStateHelper()
            self.generalSearchHelper(k.arg)
    
    def searchForward (self,event):
    
        k = self.k ; tag = 'search-forward' ; state = k.getState(tag)
    
        if state == 0:
            self.setupArgs(forward=True,regexp=False,word=False)
            self.stateZeroHelper(event,tag,'Search: ',self.searchForward)
        else:
            self.updateFindList(k.arg)
            self.lastStateHelper()
            self.generalSearchHelper(k.arg)
    #@nonl
    #@-node:ekr.20060124140224.1:seachForward/Backward
    #@+node:ekr.20060125093807:searchWithPresentOptions
    def searchWithPresentOptions (self,event):
    
        k = self.k ; tag = 'search-with-present-options'
        state = k.getState(tag)
    
        if state == 0:
            self.setupArgs(forward=None,regexp=None,word=None)
            self.stateZeroHelper(event,tag,'Search: ',self.searchWithPresentOptions)
        else:
            self.updateFindList(k.arg)
            k.clearState()
            k.resetLabel()
            k.showStateAndMode()
            self.generalSearchHelper(k.arg)
    #@nonl
    #@-node:ekr.20060125093807:searchWithPresentOptions
    #@+node:ekr.20060124134356:setupArgs
    def setupArgs (self,forward=False,regexp=False,word=False):
        
        h = self.finder ; k = self.k
        
        if forward is None:
            reverse = None
        else:
            reverse = not forward
    
        for ivar,val,in (
            ('reverse', reverse),
            ('pattern_match',regexp),
            ('whole_word',word),
        ):
            if val is not None:
                self.setOption(ivar,val)
                
        h.p = p = self.c.currentPosition()
        h.v = p.v
        h.update_ivars()
        self.showFindOptions()
    #@nonl
    #@-node:ekr.20060124134356:setupArgs
    #@+node:ekr.20060210173041:stateZeroHelper
    def stateZeroHelper (self,event,tag,prefix,handler):
    
        k = self.k
        self.w = event and event.widget
        k.setLabelBlue(prefix,protect=True)
        self.addFindStringToLabel(protect=False)
        
        k.getArg(event,tag,1,handler,
            tabList=self.findTextList,completion=True,prefix=prefix)
    #@nonl
    #@-node:ekr.20060210173041:stateZeroHelper
    #@+node:ekr.20060224171851:updateChange/FindList
    def updateChangeList (self,s):
    
        if s not in self.changeTextList:
            self.changeTextList.append(s)
            
    def updateFindList (self,s):
    
        if s not in self.findTextList:
            self.findTextList.append(s)
    #@nonl
    #@-node:ekr.20060224171851:updateChange/FindList
    #@+node:ekr.20060124140224.2:wordSearchBackward/Forward
    def wordSearchBackward (self,event):
    
        k = self.k ; tag = 'word-search-backward' ; state = k.getState(tag)
    
        if state == 0:
            self.setupArgs(forward=False,regexp=False,word=True)
            self.stateZeroHelper(event,tag,'Word Search Backward: ',self.wordSearchBackward)
        else:
            self.lastStateHelper()
            self.generalSearchHelper(k.arg)
    
    def wordSearchForward (self,event):
    
        k = self.k ; tag = 'word-search-forward' ; state = k.getState(tag)
        
        if state == 0:
            self.setupArgs(forward=True,regexp=False,word=True)
            self.stateZeroHelper(event,tag,'Word Search: ',self.wordSearchForward)
        else:
            self.lastStateHelper()
            self.generalSearchHelper(k.arg)
    #@nonl
    #@-node:ekr.20060124140224.2:wordSearchBackward/Forward
    #@-others
#@nonl
#@-node:ekr.20060123125256:class minibufferFind (the findHandler)
#@+node:ekr.20051020120306.6:class findTab (leoFind.leoFind)
class findTab (leoFind.leoFind):
    
    '''An adapter class that implements Leo's Find tab.'''

    #@    @+others
    #@+node:ekr.20051020120306.10:Birth & death
    #@+node:ekr.20051020120306.11:__init__
    def __init__(self,c,parentFrame):
        
        # g.trace('findTab')
    
        # Init the base class...
        leoFind.leoFind.__init__(self,c,title='Find Tab')
        self.c = c
        self.frame = self.outerFrame = self.top = None
        
        #@    << create the tkinter intVars >>
        #@+node:ekr.20051020120306.12:<< create the tkinter intVars >>
        self.dict = {}
        
        for key in self.intKeys:
            self.dict[key] = Tk.IntVar()
        
        for key in self.newStringKeys:
            self.dict[key] = Tk.StringVar()
            
        self.s_ctrl = Tk.Text() # Used by find.search()
        #@nonl
        #@-node:ekr.20051020120306.12:<< create the tkinter intVars >>
        #@nl
        
        self.optionsOnly = c.config.getBool('show_only_find_tab_options')
        
        # These are created later.
        self.find_ctrl = None
        self.change_ctrl = None 
        self.outerScrolledFrame = None
    
        self.createFrame(parentFrame)
        self.createBindings()
        
        self.init(c) # New in 4.3: init only once.
    #@nonl
    #@-node:ekr.20051020120306.11:__init__
    #@+node:ekr.20051023181449:createBindings (findTab)
    def createBindings (self):
        
        c = self.c ; k = c.k
        
        def resetWrapCallback(event,self=self,k=k):
            self.resetWrap(event)
            return k.masterKeyHandler(event)
            
        def findButtonBindingCallback(event=None,self=self):
            self.findButton()
            return 'break'
            
        if 0: # No longer needed.
            def findTabClickCallback(event,self=self):
                c = self.c ; k = c.k ; w = event.widget
                k.keyboardQuit(event)
                w and c.widgetWantsFocusNow(w)
                return k.masterClickHandler(event)
    
        table = (
            ('<Button-1>',  k.masterClickHandler),
            ('<Double-1>',  k.masterClickHandler),
            ('<Button-3>',  k.masterClickHandler),
            ('<Double-3>',  k.masterClickHandler),
            ('<Key>',       resetWrapCallback),
            ('<Return>',    findButtonBindingCallback),
            ("<Escape>",    self.hideTab),
        )
    
        for w in (self.find_ctrl,self.change_ctrl):
            for event, callback in table:
                w.bind(event,callback)
    #@nonl
    #@-node:ekr.20051023181449:createBindings (findTab)
    #@+node:ekr.20051020120306.13:createFrame (findTab)
    def createFrame (self,parentFrame):
        
        c = self.c
        
        # g.trace('findTab')
        
        #@    << Create the outer frames >>
        #@+node:ekr.20051020120306.14:<< Create the outer frames >>
        configName = 'log_pane_Find_tab_background_color'
        bg = c.config.getColor(configName) or 'MistyRose1'
        
        parentFrame.configure(background=bg)
        
        self.top = Tk.Frame(parentFrame,background=bg)
        self.top.pack(side='top',expand=0,fill='both',pady=5)
            # Don't expand, so the frame goes to the top.
        
        self.outerScrolledFrame = Pmw.ScrolledFrame(
            parentFrame,usehullsize = 1)
        
        self.outerFrame = outer = self.outerScrolledFrame.component('frame')
        self.outerFrame.configure(background=bg)
        
        for z in ('borderframe','clipper','frame','hull'):
            self.outerScrolledFrame.component(z).configure(relief='flat',background=bg)
        #@nonl
        #@-node:ekr.20051020120306.14:<< Create the outer frames >>
        #@nl
        #@    << Create the Find and Change panes >>
        #@+node:ekr.20051020120306.15:<< Create the Find and Change panes >>
        fc = Tk.Frame(outer, bd="1m",background=bg)
        fc.pack(anchor="n", fill="x", expand=1)
        
        # Removed unused height/width params: using fractions causes problems in some locales!
        fpane = Tk.Frame(fc, bd=1,background=bg)
        cpane = Tk.Frame(fc, bd=1,background=bg)
        
        fpane.pack(anchor="n", expand=1, fill="x")
        cpane.pack(anchor="s", expand=1, fill="x")
        
        # Create the labels and text fields...
        flab = Tk.Label(fpane, width=8, text="Find:",background=bg)
        clab = Tk.Label(cpane, width=8, text="Change:",background=bg)
        
        if self.optionsOnly:
            # Use one-line boxes.
            self.find_ctrl = ftxt = Tk.Text(
                fpane,bd=1,relief="groove",height=1,width=25,name='find-text')
            self.change_ctrl = ctxt = Tk.Text(
                cpane,bd=1,relief="groove",height=1,width=25,name='change-text')
        else:
            # Use bigger boxes for scripts.
            self.find_ctrl = ftxt = Tk.Text(
                fpane,bd=1,relief="groove",height=3,width=15,name='find-text')
            self.change_ctrl = ctxt = Tk.Text(
                cpane,bd=1,relief="groove",height=3,width=15,name='change-text')
        #@<< Bind Tab and control-tab >>
        #@+node:ekr.20051020120306.16:<< Bind Tab and control-tab >>
        def setFocus(w):
            c = self.c
            c.widgetWantsFocus(w)
            g.app.gui.setSelectionRange(w,"1.0","1.0")
            return "break"
            
        def toFind(event,w=ftxt): return setFocus(w)
        def toChange(event,w=ctxt): return setFocus(w)
            
        def insertTab(w):
            data = g.app.gui.getSelectionRange(w)
            if data: start,end = data
            else: start = end = g.app.gui.getInsertPoint(w)
            g.app.gui.replaceSelectionRangeWithText(w,start,end,"\t")
            return "break"
        
        def insertFindTab(event,w=ftxt): return insertTab(w)
        def insertChangeTab(event,w=ctxt): return insertTab(w)
        
        ftxt.bind("<Tab>",toChange)
        ctxt.bind("<Tab>",toFind)
        ftxt.bind("<Control-Tab>",insertFindTab)
        ctxt.bind("<Control-Tab>",insertChangeTab)
        #@nonl
        #@-node:ekr.20051020120306.16:<< Bind Tab and control-tab >>
        #@nl
        
        if 0: # Add scrollbars.
            fBar = Tk.Scrollbar(fpane,name='findBar')
            cBar = Tk.Scrollbar(cpane,name='changeBar')
            
            for bar,txt in ((fBar,ftxt),(cBar,ctxt)):
                txt['yscrollcommand'] = bar.set
                bar['command'] = txt.yview
                bar.pack(side="right", fill="y")
                
        if self.optionsOnly:
            flab.pack(side="left") ; ftxt.pack(side="left")
            clab.pack(side="left") ; ctxt.pack(side="left")
        else:
            flab.pack(side="left") ; ftxt.pack(side="right", expand=1, fill="x")
            clab.pack(side="left") ; ctxt.pack(side="right", expand=1, fill="x")
        #@nonl
        #@-node:ekr.20051020120306.15:<< Create the Find and Change panes >>
        #@nl
        #@    << Create two columns of radio and checkboxes >>
        #@+node:ekr.20051020120306.17:<< Create two columns of radio and checkboxes >>
        columnsFrame = Tk.Frame(outer,relief="groove",bd=2,background=bg)
        
        columnsFrame.pack(expand=0,padx="7p",pady="2p")
        
        numberOfColumns = 2 # Number of columns
        columns = [] ; radioLists = [] ; checkLists = []
        for i in xrange(numberOfColumns):
            columns.append(Tk.Frame(columnsFrame,bd=1))
            radioLists.append([])
            checkLists.append([])
        
        for i in xrange(numberOfColumns):
            columns[i].pack(side="left",padx="1p") # fill="y" Aligns to top. padx expands columns.
        
        radioLists[0] = []
        
        checkLists[0] = [
            # ("Scrip&t Change",self.dict["script_change"]),
            ("Whole &Word", self.dict["whole_word"]),
            ("&Ignore Case",self.dict["ignore_case"]),
            ("Wrap &Around",self.dict["wrap"]),
            ("&Reverse",    self.dict["reverse"]),
            ('Rege&xp',     self.dict['pattern_match']),
            ("Mark &Finds", self.dict["mark_finds"]),
        ]
        
        radioLists[1] = [
            (self.dict["radio-search-scope"],"&Entire Outline","entire-outline"),
            (self.dict["radio-search-scope"],"&Suboutline Only","suboutline-only"),  
            (self.dict["radio-search-scope"],"&Node Only","node-only"),
        ]
        
        checkLists[1] = [
            ("Search &Headline", self.dict["search_headline"]),
            ("Search &Body",     self.dict["search_body"]),
            ("Mark &Changes",    self.dict["mark_changes"]),
        ]
        
        for i in xrange(numberOfColumns):
            for var,name,val in radioLists[i]:
                box = self.underlinedTkButton(
                    "radio",columns[i],anchor="w",text=name,variable=var,value=val,background=bg)
                box.button.pack(fill="x")
                box.button.bind("<Button-1>", self.resetWrap)
                if val == None: box.button.configure(state="disabled")
                box.bindHotKey(ftxt)
                box.bindHotKey(ctxt)
            for name,var in checkLists[i]:
                box = self.underlinedTkButton(
                    "check",columns[i],anchor="w",text=name,variable=var,background=bg)
                box.button.pack(fill="x")
                box.button.bind("<Button-1>", self.resetWrap)
                box.bindHotKey(ftxt)
                box.bindHotKey(ctxt)
                if var is None: box.button.configure(state="disabled")
        #@nonl
        #@-node:ekr.20051020120306.17:<< Create two columns of radio and checkboxes >>
        #@nl
        
        if  self.optionsOnly:
            buttons = []
        else:
            #@        << Create two columns of buttons >>
            #@+node:ekr.20051020120306.18:<< Create two columns of buttons >>
            # Create the alignment panes.
            buttons  = Tk.Frame(outer,background=bg)
            buttons1 = Tk.Frame(buttons,bd=1,background=bg)
            buttons2 = Tk.Frame(buttons,bd=1,background=bg)
            buttons.pack(side='top',expand=1)
            buttons1.pack(side='left')
            buttons2.pack(side='right')
            
            width = 15 ; defaultText = 'Find' ; buttons = []
            
            for text,boxKind,frame,callback in (
                # Column 1...
                ('Find','button',buttons1,self.findButtonCallback),
                # ('Incremental','check', buttons1,None),
                    ## variable=self.dict['incremental'])
                    ## May affect the file format.
                ('Find All','button',buttons1,self.findAllButton),
                # Column 2...
                ('Change','button',buttons2,self.changeButton),
                ('Change, Then Find','button',buttons2,self.changeThenFindButton),
                ('Change All','button',buttons2,self.changeAllButton),
            ):
                w = self.underlinedTkButton(boxKind,frame,
                    text=text,command=callback)
                buttons.append(w)
                if text == defaultText:
                    w.button.configure(width=width-1,bd=4)
                elif boxKind != 'check':
                    w.button.configure(width=width)
                w.button.pack(side='top',anchor='w',pady=2,padx=2)
            #@nonl
            #@-node:ekr.20051020120306.18:<< Create two columns of buttons >>
            #@nl
        
        # Pack this last so buttons don't get squashed when frame is resized.
        self.outerScrolledFrame.pack(side='top',expand=1,fill='both',padx=2,pady=2)
        
        if 0: # These dont work in the new binding scheme.  Use shortcuts or mode bindings instead.
            for w in buttons:
                w.bindHotKey(ftxt)
                w.bindHotKey(ctxt)
    #@nonl
    #@-node:ekr.20051020120306.13:createFrame (findTab)
    #@+node:ekr.20051020120306.19:find.init
    def init (self,c):
        
        # g.trace('Find Tab')
    
        # N.B.: separate c.ivars are much more convenient than a dict.
        for key in self.intKeys:
            # New in 4.3: get ivars from @settings.
            val = c.config.getBool(key)
            setattr(self,key,val)
            val = g.choose(val,1,0) # Work around major Tk problem.
            self.dict[key].set(val)
            # g.trace(key,val)
    
        #@    << set find/change widgets >>
        #@+node:ekr.20051020120306.20:<< set find/change widgets >>
        self.find_ctrl.delete("1.0","end")
        self.change_ctrl.delete("1.0","end")
        
        # New in 4.3: Get setting from @settings.
        for w,setting,defaultText in (
            (self.find_ctrl,"find_text",'<find pattern here>'),
            (self.change_ctrl,"change_text",''),
        ):
            s = c.config.getString(setting)
            if not s: s = defaultText
            w.insert("end",s)
        #@nonl
        #@-node:ekr.20051020120306.20:<< set find/change widgets >>
        #@nl
        #@    << set radio buttons from ivars >>
        #@+node:ekr.20051020120306.21:<< set radio buttons from ivars >>
        found = False
        for var,setting in (
            ("pattern_match","pattern-search"),
            #("script_search","script-search")
        ):
            val = self.dict[var].get()
            if val:
                self.dict["radio-find-type"].set(setting)
                found = True ; break
        if not found:
            self.dict["radio-find-type"].set("plain-search")
            
        found = False
        for var,setting in (
            ("suboutline_only","suboutline-only"),
            ("node_only","node-only"),
            # ("selection_only","selection-only")
        ):
            val = self.dict[var].get()
            if val:
                self.dict["radio-search-scope"].set(setting)
                found = True ; break
        if not found:
            self.dict["radio-search-scope"].set("entire-outline")
        #@nonl
        #@-node:ekr.20051020120306.21:<< set radio buttons from ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20051020120306.19:find.init
    #@-node:ekr.20051020120306.10:Birth & death
    #@+node:ekr.20051020120306.22:find.update_ivars
    def update_ivars (self):
        
        """Called just before doing a find to update ivars from the find panel."""
    
        self.p = self.c.currentPosition()
        self.v = self.p.v
    
        for key in self.intKeys:
            val = self.dict[key].get()
            setattr(self, key, val)
            # g.trace(key,val)
    
        search_scope = self.dict["radio-search-scope"].get()
        self.suboutline_only = g.choose(search_scope == "suboutline-only",1,0)
        self.node_only       = g.choose(search_scope == "node-only",1,0)
    
        # The caller is responsible for removing most trailing cruft.
        # Among other things, this allows Leo to search for a single trailing space.
        s = self.find_ctrl.get("1.0","end")
        s = g.toUnicode(s,g.app.tkEncoding)
        if s and s[-1] in ('\r','\n'):
            s = s[:-1]
        self.find_text = s
    
        s = self.change_ctrl.get("1.0","end")
        if s and s[-1] in ('\r','\n'):
            s = s[:-1]
        s = g.toUnicode(s,g.app.tkEncoding)
        self.change_text = s
    #@nonl
    #@-node:ekr.20051020120306.22:find.update_ivars
    #@+node:ekr.20060221074900:Callbacks
    #@+node:ekr.20060221074900.1:findButtonCallback
    def findButtonCallback(self,event=None):
        
        self.findButton()
        return 'break'
    #@nonl
    #@-node:ekr.20060221074900.1:findButtonCallback
    #@+node:ekr.20051020120306.25:hideTab
    def hideTab (self,event=None):
        
        c = self.c
        c.frame.log.selectTab('Log')
        c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051020120306.25:hideTab
    #@-node:ekr.20060221074900:Callbacks
    #@+node:ekr.20051024192602: Top level
    #@+node:ekr.20060209064832:findAllCommand
    def findAllCommand (self,event=None):
    
        self.setup_command()
        self.findAll()
    #@nonl
    #@-node:ekr.20060209064832:findAllCommand
    #@+node:ekr.20060204120158.1:findAgainCommand
    def findAgainCommand (self):
        
        s = self.find_ctrl.get("1.0","end")
        s = g.toUnicode(s,g.app.tkEncoding)
        if s.endswith('\n'): s = s[:-1]
        
        if s and s != '<find pattern here>':
            self.findNextCommand()
            return True
        else:
            # Tell the caller that to get the find args.
            return False
    #@-node:ekr.20060204120158.1:findAgainCommand
    #@+node:ekr.20060128075225:cloneFindAllCommand
    def cloneFindAllCommand (self,event=None):
        
        self.setup_command()
        self.clone_find_all = True
        self.findAll()
        self.clone_find_all = False
    #@-node:ekr.20060128075225:cloneFindAllCommand
    #@+node:ekr.20051024192642.2:findNext/PrefCommand
    def findNextCommand (self,event=None):
    
        self.setup_command()
        self.findNext()
        
    def findPrevCommand (self,event=None):
        
        self.setup_command()
        self.reverse = not self.reverse
        self.findNext()
        self.reverse = not self.reverse
    #@nonl
    #@-node:ekr.20051024192642.2:findNext/PrefCommand
    #@+node:ekr.20051024192642.3:change/ThenFindCommand
    def changeCommand (self,event=None):
    
        self.setup_command()
        self.change()
        
    def changeAllCommand (self,event=None):
    
        self.setup_command()
        self.changeAll()
        
    def changeThenFindCommand(self,event=None):
        
        self.setup_command()
        self.changeThenFind()
    #@nonl
    #@-node:ekr.20051024192642.3:change/ThenFindCommand
    #@-node:ekr.20051024192602: Top level
    #@+node:ekr.20051020120306.26:bringToFront
    def bringToFront (self):
    
        """Bring the Find Tab to the front and select the entire find text."""
    
        c = self.c ; t = self.find_ctrl
            
        # The widget must have focus before we can adjust the text.
        c.widgetWantsFocus(t)
        
        # Delete one trailing newline.
        s = t.get('1.0','end')
        if s and s[-1] in ('\n','\r'):
            t.delete('end-1c','end')
    
        # Don't highlight the added trailing newline!
        g.app.gui.setTextSelection (t,"1.0","end-1c") # Thanks Rich.
        
        # This is also needed.
        c.widgetWantsFocus(t)
    #@nonl
    #@-node:ekr.20051020120306.26:bringToFront
    #@+node:ekr.20051020120306.27:selectAllFindText
    def selectAllFindText (self,event=None):
        
        __pychecker__ = '--no-argsused' # event
    
        w = self.frame.focus_get()
        if g.app.gui.isTextWidget(w):
            g.app.gui.setTextSelection(w,"1.0","end")
    
        return "break"
    #@nonl
    #@-node:ekr.20051020120306.27:selectAllFindText
    #@+node:ekr.20051020120306.28:Tkinter wrappers (leoTkinterFind)
    def gui_search (self,t,*args,**keys):
        return t.search(*args,**keys)
    
    def init_s_ctrl (self,s):
        t = self.s_ctrl
        t.delete("1.0","end")
        t.insert("end",s)
        t.mark_set("insert",g.choose(self.reverse,"end","1.0"))
        return t
    #@nonl
    #@-node:ekr.20051020120306.28:Tkinter wrappers (leoTkinterFind)
    #@+node:ekr.20051020120306.1:class underlinedTkButton
    class underlinedTkButton:
        
        #@    @+others
        #@+node:ekr.20051020120306.2:__init__
        def __init__(self,buttonType,parent_widget,**keywords):
        
            self.buttonType = buttonType
            self.parent_widget = parent_widget
            self.hotKey = None
            text = keywords['text']
        
            #@    << set self.hotKey if '&' is in the string >>
            #@+node:ekr.20051020120306.3:<< set self.hotKey if '&' is in the string >>
            index = text.find('&')
            
            if index > -1:
            
                if index == len(text)-1:
                    # The word ends in an ampersand.  Ignore it; there is no hot key.
                    text = text[:-1]
                else:
                    self.hotKey = text [index + 1]
                    text = text[:index] + text[index+1:]
            #@nonl
            #@-node:ekr.20051020120306.3:<< set self.hotKey if '&' is in the string >>
            #@nl
        
            # Create the button...
            if self.hotKey:
                keywords['text'] = text
                keywords['underline'] = index
        
            if buttonType.lower() == "button":
                self.button = Tk.Button(parent_widget,keywords)
            elif buttonType.lower() == "check":
                self.button = Tk.Checkbutton(parent_widget,keywords)
            elif buttonType.lower() == "radio":
                self.button = Tk.Radiobutton(parent_widget,keywords)
            else:
                g.trace("bad buttonType")
            
            self.text = text # for traces
        #@nonl
        #@-node:ekr.20051020120306.2:__init__
        #@+node:ekr.20051020120306.4:bindHotKey
        def bindHotKey (self,widget):
            
            if self.hotKey:
                for key in (self.hotKey.lower(),self.hotKey.upper()):
                    widget.bind("<Alt-%s>" % key,self.buttonCallback)
        #@nonl
        #@-node:ekr.20051020120306.4:bindHotKey
        #@+node:ekr.20051020120306.5:buttonCallback
        # The hot key has been hit.  Call the button's command.
        
        def buttonCallback (self, event=None):
            
            __pychecker__ = '--no-argsused' # the event param must be present.
        
            # g.trace(self.text)
        
            self.button.invoke ()
            
            # See if this helps.
            return 'break'
        #@-node:ekr.20051020120306.5:buttonCallback
        #@-others
    #@nonl
    #@-node:ekr.20051020120306.1:class underlinedTkButton
    #@-others
#@nonl
#@-node:ekr.20051020120306.6:class findTab (leoFind.leoFind)
#@+node:ekr.20050920084036.257:class searchCommandsClass
class searchCommandsClass (baseEditCommandsClass):
    
    '''Implements many kinds of searches.'''

    #@    @+others
    #@+node:ekr.20050920084036.258: ctor
    def __init__ (self,c):
        
        # g.trace('searchCommandsClass')
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.findTabHandler = None
        self.minibufferFindHandler = None
        
        try:
            self.w = c.frame.body.bodyCtrl
        except AttributeError:
            self.w = None
    #@nonl
    #@-node:ekr.20050920084036.258: ctor
    #@+node:ekr.20050920084036.259:getPublicCommands (searchCommandsClass)
    def getPublicCommands (self):
        
        return {
            'clone-find-all':                       self.cloneFindAll,
            'find-tab-find-all':                    self.findAll,
            
            # Thin wrappers on Find tab
            'find-tab-find':                        self.findTabFindNext,
            'find-tab-find-prev':                   self.findTabFindPrev,
            'find-tab-change':                      self.findTabChange,
            'find-tab-change-all':                  self.findTabChangeAll,
            'find-tab-change-then-find':            self.findTabChangeThenFind,
                        
            'hide-find-tab':                        self.hideFindTab,
                
            'isearch-forward':                      self.isearchForward,
            'isearch-backward':                     self.isearchBackward,
            'isearch-forward-regexp':               self.isearchForwardRegexp,
            'isearch-backward-regexp':              self.isearchBackwardRegexp,
                        
            'open-find-tab':                        self.openFindTab,
        
            'replace-string':                       self.replaceString,
                        
            're-search-forward':                    self.reSearchForward,
            're-search-backward':                   self.reSearchBackward,
    
            'search-again':                         self.findAgain,
            # Uses existing search pattern.
            
            'search-forward':                       self.searchForward,
            'search-backward':                      self.searchBackward,
            'search-with-present-options':          self.searchWithPresentOptions,
            # Prompts for search pattern.
    
            'set-find-everywhere':                  self.setFindScopeEveryWhere,
            'set-find-node-only':                   self.setFindScopeNodeOnly,
            'set-find-suboutline-only':             self.setFindScopeSuboutlineOnly,
            
            'show-find-options':                    self.showFindOptions,
    
            'toggle-find-ignore-case-option':       self.toggleIgnoreCaseOption,
            'toggle-find-in-body-option':           self.toggleSearchBodyOption,
            'toggle-find-in-headline-option':       self.toggleSearchHeadlineOption,
            'toggle-find-mark-changes-option':      self.toggleMarkChangesOption,
            'toggle-find-mark-finds-option':        self.toggleMarkFindsOption,
            'toggle-find-regex-option':             self.toggleRegexOption,
            'toggle-find-reverse-option':           self.toggleReverseOption,
            'toggle-find-word-option':              self.toggleWholeWordOption,
            'toggle-find-wrap-around-option':       self.toggleWrapSearchOption,
            
            'word-search-forward':                  self.wordSearchForward,
            'word-search-backward':                 self.wordSearchBackward,
        }
    #@nonl
    #@-node:ekr.20050920084036.259:getPublicCommands (searchCommandsClass)
    #@+node:ekr.20060123131421:Top-level methods
    #@+node:ekr.20051020120306:openFindTab
    def openFindTab (self,event=None,show=True):
    
        c = self.c ; log = c.frame.log ; tabName = 'Find'
        
        wasOpen = log.frameDict.get(tabName)
    
        if wasOpen:
            log.selectTab(tabName)
        else:
            log.selectTab(tabName)
            f = log.frameDict.get(tabName)
            t = log.textDict.get(tabName)
            t.pack_forget()
            self.findTabHandler = findTab(c,f)
    
        if show or wasOpen or c.config.getBool('minibufferSearchesShowFindTab'):
            pass # self.findTabHandler.bringToFront()
        else:
            log.hideTab(tabName)
    #@nonl
    #@-node:ekr.20051020120306:openFindTab
    #@+node:ekr.20051022212004:Find Tab commands
    # Just open the Find tab if it has never been opened.
    # For minibuffer commands, it would be good to force the Find tab to be visible.
    # However, this leads to unfortunate confusion when executed from a shortcut.
    
    def findTabChange(self,event=None):
    
        if self.findTabHandler:
            self.findTabHandler.changeCommand()
        else:
            self.openFindTab()
            
    def findTabChangeAll(self,event=None):
    
        if self.findTabHandler:
            self.findTabHandler.changeAllCommand()
        else:
            self.openFindTab()
    
    def findTabChangeThenFind(self,event=None):
    
        if self.findTabHandler:
            self.findTabHandler.changeThenFindCommand()
        else:
            self.openFindTab()
            
    def findTabFindAll(self,event=None):
    
        if self.findTabHandler:
            self.findTabHandler.findAllCommand()
        else:
            self.openFindTab()
    
    def findTabFindNext (self,event=None):
        
        if self.findTabHandler:
            self.findTabHandler.findNextCommand()
        else:
            self.openFindTab()
    
    def findTabFindPrev (self,event=None):
        
        if self.findTabHandler:
            self.findTabHandler.findPrevCommand()
        else:
            self.openFindTab()
            
    def hideFindTab (self,event=None):
        if self.findTabHandler:
            self.c.frame.log.selectTab('Log')
    #@nonl
    #@-node:ekr.20051022212004:Find Tab commands
    #@+node:ekr.20060124115801:getHandler
    def getHandler(self,show=False):
        
        '''Return the minibuffer handler, creating it if necessary.'''
        
        c = self.c
        
        self.openFindTab(show=show)
            # sets self.findTabHandler,
            # but *not* minibufferFindHandler.
        
        if not self.minibufferFindHandler:
            self.minibufferFindHandler = minibufferFind(c,self.findTabHandler)
    
        return self.minibufferFindHandler
    #@nonl
    #@-node:ekr.20060124115801:getHandler
    #@+node:ekr.20060123115459:Find options wrappers
    def setFindScopeEveryWhere     (self, event): return self.setFindScope('entire-outline')
    def setFindScopeNodeOnly       (self, event): return self.setFindScope('node-only')
    def setFindScopeSuboutlineOnly (self, event): return self.setFindScope('suboutline-only')
    
    def setFindScope (self, where): self.getHandler().setFindScope(where)
    
    def showFindOptions      (self,event): self.getHandler().showFindOptions()
    
    def toggleIgnoreCaseOption     (self, event): return self.toggleOption('ignore_case')
    def toggleMarkChangesOption    (self, event): return self.toggleOption('mark_changes')
    def toggleMarkFindsOption      (self, event): return self.toggleOption('mark_finds')
    def toggleRegexOption          (self, event): return self.toggleOption('pattern_match')
    def toggleReverseOption        (self, event): return self.toggleOption('reverse')
    def toggleSearchBodyOption     (self, event): return self.toggleOption('search_body')
    def toggleSearchHeadlineOption (self, event): return self.toggleOption('search_headline')
    def toggleWholeWordOption      (self, event): return self.toggleOption('whole_word')
    def toggleWrapSearchOption     (self, event): return self.toggleOption('wrap')
    
    def toggleOption (self, ivar): self.getHandler().toggleOption(ivar)
    #@nonl
    #@-node:ekr.20060123115459:Find options wrappers
    #@+node:ekr.20060124093828:Find wrappers
    def cloneFindAll       (self,event): self.getHandler().cloneFindAll(event)
    def findAll            (self,event): self.getHandler().findAll(event)
    
    def replaceString      (self,event): self.getHandler().replaceString(event)
    def reSearchBackward   (self,event): self.getHandler().reSearchBackward(event)
    def reSearchForward    (self,event): self.getHandler().reSearchForward(event)
    def searchBackward     (self,event): self.getHandler().searchBackward(event)
    def searchForward      (self,event): self.getHandler().searchForward(event)
    def wordSearchBackward (self,event): self.getHandler().wordSearchBackward(event)
    def wordSearchForward  (self,event): self.getHandler().wordSearchForward(event)
    
    def searchWithPresentOptions (self,event):
        self.getHandler().searchWithPresentOptions(event)
    #@nonl
    #@-node:ekr.20060124093828:Find wrappers
    #@+node:ekr.20060204120158.2:findAgain
    def findAgain (self,event):
        
        h = self.getHandler()
        
        # h.findAgain returns False if there is no search pattern.
        # In that case, we revert to find-with-present-options.
        if not h.findAgain(event):
            h.searchWithPresentOptions(event)
    #@nonl
    #@-node:ekr.20060204120158.2:findAgain
    #@-node:ekr.20060123131421:Top-level methods
    #@+node:ekr.20050920084036.261:incremental search...
    def isearchForward (self,event):
        self.startIncremental(event,forward=True,regexp=False)
        
    def isearchBackward (self,event):
        self.startIncremental(event,forward=False,regexp=False)
        
    def isearchForwardRegexp (self,event):
        self.startIncremental(event,forward=True,regexp=True)
        
    def isearchBackwardRegexp (self,event):
        self.startIncremental(event,forward=False,regexp=True)
    #@nonl
    #@+node:ekr.20050920084036.262:startIncremental
    def startIncremental (self,event,forward,regexp):
    
        c = self.c ; k = self.k
        
        self.forward = forward
        self.regexp = regexp
        k.setLabelBlue('isearch: ',protect=True)
        k.setState('isearch',1,handler=self.iSearchStateHandler)
        c.minibufferWantsFocus()
    #@nonl
    #@-node:ekr.20050920084036.262:startIncremental
    #@+node:ekr.20050920084036.264:iSearchStateHandler & helper
    # Called when from the state manager when the state is 'isearch'
    
    def iSearchStateHandler (self,event):
    
        c = self.c ; k = self.k ; w = self.w
        
        if not event:
            g.trace('no event',g.callers())
            return
        keysym = event.keysym
        ch = event.char
        if keysym == 'Control_L': return
        
        c.bodyWantsFocus()
        
        # g.trace('keysym',keysym,'stroke',k.stroke)
        
        if 0: # Useful, but presently conflicts with other bindings.
            if k.stroke == '<Control-s>':
                self.startIncremental(event,forward=True,regexp=False)
            elif k.stroke == '<Control-r>':
                self.startIncremental(event,forward=False,regexp=False)
    
        if keysym == 'Return':
            s = self.searchString
            i = w.index('insert')
            j = w.index('insert +%sc' % len(s))
            if not self.forward: i,j = j,i
            self.endSearch(i,j)
            return
    
        if ch == '\b':
            g.trace('backspace not handled yet')
            return
        
        if ch:
            k.updateLabel(event)
            s = k.getLabel(ignorePrompt=True)
            i = w.search(s,'insert',stopindex='insert +%sc' % len(s))
            if i:
                self.searchString = s
            else:
               self.iSearchHelper(event,self.forward,self.regexp)
            self.scolorizer(event)
    #@nonl
    #@-node:ekr.20050920084036.264:iSearchStateHandler & helper
    #@+node:ekr.20050920084036.265:scolorizer
    def scolorizer (self,event):
    
        k = self.k ; w = self.w
    
        stext = k.getLabel(ignorePrompt=True)
        w.tag_delete('color')
        w.tag_delete('color1')
        if stext == '': return
        ind = '1.0'
        while ind:
            try:
                ind = w.search(stext,ind,stopindex='end',regexp=self.regexp)
            except:
                break
            if ind:
                i, d = ind.split('.')
                d = str(int(d)+len(stext))
                index = w.index('insert')
                if ind == index:
                    w.tag_add('color1',ind,'%s.%s' % (i,d))
                w.tag_add('color',ind,'%s.%s' % (i,d))
                ind = i + '.' + d
    
        w.tag_config('color',foreground='red')
        w.tag_config('color1',background='lightblue')
    #@nonl
    #@-node:ekr.20050920084036.265:scolorizer
    #@+node:ekr.20050920084036.263:iSearchHelper
    def iSearchHelper (self,event,forward,regexp):
    
        '''This method moves the insert spot to position that matches the pattern in the miniBuffer'''
        
        k = self.k ; w = self.w
        pattern = k.getLabel(ignorePrompt=True)
        if not pattern: return
        
        self.searchString = pattern
        self.incremental = True
        self.forward = forward
        self.regexp = regexp
       
        try:
            i = None
            if forward:
                i = w.search(pattern,"insert + 1c",stopindex='end',regexp=regexp)
                if 0: # Not so useful when searches can cross buffer boundaries.
                    if not i: # Start again at the top of the buffer.
                        i = w.search(pattern,'1.0',stopindex='insert',regexp=regexp)
            else:
                i = w.search(pattern,'insert',backwards=True,stopindex='1.0',regexp=regexp)
                if 0: # Not so useful when searches can cross buffer boundaries.
                    if not i: # Start again at the bottom of the buffer.
                        i = w.search(pattern,'end',backwards=True,stopindex='insert',regexp=regexp)
        except: pass
            
        # Don't call endSearch here.  We'll do that when the user hits return.
        if i and not i.isspace():
            w.mark_set('insert',i)
            w.see('insert')
    #@nonl
    #@-node:ekr.20050920084036.263:iSearchHelper
    #@+node:ekr.20060203072636:endSearch
    def endSearch (self,i,j):
    
        g.app.gui.setTextSelection (self.w,i,j,insert='sel.end')
        self.k.keyboardQuit(event=None)
    #@nonl
    #@-node:ekr.20060203072636:endSearch
    #@-node:ekr.20050920084036.261:incremental search...
    #@-others
#@nonl
#@-node:ekr.20050920084036.257:class searchCommandsClass
#@-node:ekr.20051023094009:Search classes
#@+node:ekr.20051025071455:Spell classes (ok)
#@+others
#@+node:ekr.20051025071455.6:class Aspell
class Aspell:
    
    """A wrapper class for Aspell spell checker"""
    
    #@    @+others
    #@+node:ekr.20051025071455.7:Birth & death
    #@+node:ekr.20051025071455.8:__init__
    def __init__ (self,c,local_dictionary_file,local_language_code):
    
        """Ctor for the Aspell class."""
    
        self.c = c
    
        self.aspell_dir = c.config.getString('aspell_dir')
        self.aspell_bin_dir = c.config.getString('aspell_bin_dir')
    
        try:
            import aspell
        except ImportError:
            # Specify the path to the top-level Aspell directory.
            theDir = g.choose(sys.platform=='darwin',self.aspell_dir,self.aspell_bin_dir)
            aspell = g.importFromPath('aspell',theDir,pluginName=__name__,verbose=True)
            
        self.aspell = aspell
        if aspell:
            self.sc = aspell.spell_checker(prefix=self.aspell_dir,lang=local_language_code)
            self.local_language_code = local_language_code
            self.local_dictionary_file = local_dictionary_file
            self.local_dictionary = "%s.wl" % os.path.splitext(local_dictionary_file) [0]
    #@nonl
    #@-node:ekr.20051025071455.8:__init__
    #@-node:ekr.20051025071455.7:Birth & death
    #@+node:ekr.20051025071455.10:processWord
    def processWord(self, word):
        """Pass a word to aspell and return the list of alternatives.
        OK: 
        * 
        Suggestions: 
        & «original» «count» «offset»: «miss», «miss», ... 
        None: 
        # «original» «offset» 
        simplifyed to not create the string then make a list from it    
        """
    
        if self.sc.check(word):
            return None
        else:
            return self.sc.suggest(word)
    #@nonl
    #@-node:ekr.20051025071455.10:processWord
    #@+node:ekr.20051025071455.11:updateDictionary
    def updateDictionary(self):
    
        """Update the aspell dictionary from a list of words.
        
        Return True if the dictionary was updated correctly."""
    
        try:
            # Create master list
            basename = os.path.splitext(self.local_dictionary)[0]
            cmd = (
                "%s --lang=%s create master %s.wl < %s.txt" %
                (self.aspell_bin_dir, self.local_language_code, basename,basename))
            os.popen(cmd)
            return True
    
        except Exception, err:
            g.es_print("Unable to update local aspell dictionary: %s" % err)
            return False
    #@nonl
    #@-node:ekr.20051025071455.11:updateDictionary
    #@-others

#@-node:ekr.20051025071455.6:class Aspell
#@+node:ekr.20051025071455.1:class spellCommandsClass
class spellCommandsClass (baseEditCommandsClass):
    
    '''Commands to support the Spell Tab.'''

    #@    @+others
    #@+node:ekr.20051025080056:ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.handler = None
        
        # All the work happens when we first open the frame.
    #@nonl
    #@-node:ekr.20051025080056:ctor
    #@+node:ekr.20051025080420:getPublicCommands (searchCommandsClass)
    def getPublicCommands (self):
        
        return {
            'open-spell-tab':           self.openSpellTab,
            'spell-find':               self.find,
            'spell-change':             self.change,
            'spell-change-then-find':   self.changeThenFind,
            'spell-ignore':             self.ignore,
            'hide-spell-tab':           self.hide,
        }
    #@nonl
    #@-node:ekr.20051025080420:getPublicCommands (searchCommandsClass)
    #@+node:ekr.20051025080633:openSpellTab
    def openSpellTab (self,event=None):
    
        c = self.c ; log = c.frame.log ; tabName = 'Spell'
    
        if log.frameDict.get(tabName):
            log.selectTab(tabName)
        elif self.handler:
            if self.handler.loaded:
                self.handler.bringToFront()
        else:
            log.selectTab(tabName)
            f = log.frameDict.get(tabName)
            t = log.textDict.get(tabName)
            t.pack_forget()
            self.handler = spellTab(c,f)
            
        self.handler.bringToFront()
    #@nonl
    #@-node:ekr.20051025080633:openSpellTab
    #@+node:ekr.20051025080420.1:commands...
    # Just open the Spell tab if it has never been opened.
    # For minibuffer commands, we must also force the Spell tab to be visible.
    
    def find (self,event=None):
    
        if self.handler:
            self.openSpellTab()
            self.handler.find()
        else:
            self.openSpellTab()
    
    def change(self,event=None):
    
        if self.handler:
            self.openSpellTab()
            self.handler.change()
        else:
            self.openSpellTab()
            
    def changeAll(self,event=None):
    
        if self.handler:
            self.openSpellTab()
            self.handler.changeAll()
        else:
            self.openSpellTab()
    
    def changeThenFind (self,event=None):
        
        if self.handler:
            self.openSpellTab()
            self.handler.changeThenFind()
        else:
            self.openSpellTab()
            
    def hide (self,event=None):
        
        if self.handler:
            self.c.frame.log.selectTab('Log')
            self.c.bodyWantsFocus()
    
    def ignore (self,event=None):
        
        if self.handler:
            self.openSpellTab()
            self.handler.ignore()
        else:
            self.openSpellTab()
    #@nonl
    #@-node:ekr.20051025080420.1:commands...
    #@-others
#@nonl
#@-node:ekr.20051025071455.1:class spellCommandsClass
#@+node:ekr.20051025071455.18:class spellTab (leoFind.leoFind)
class spellTab(leoFind.leoFind):

    """A class to create and manage Leo's Spell Check dialog."""
    
    #@    @+others
    #@+node:ekr.20051025071455.19:Birth & death
    #@+node:ekr.20051025071455.20:spellTab.__init__
    def __init__(self,c,parentFrame):
        
        """Ctor for the Leo Spelling dialog."""
    
        leoFind.leoFind.__init__(self,c) # Call the base ctor.
    
        self.c = c
        self.body = c.frame.body
        self.currentWord = None
        self.suggestions = []
        self.messages = [] # List of message to be displayed when hiding the tab.
        self.outerScrolledFrame = None
        self.workCtrl = Tk.Text(None) # A text widget for scanning.
        
        self.loaded = self.init_aspell(c)
        if self.loaded:
            self.createSpellTab(parentFrame)
            self.createBindings()
    #@nonl
    #@-node:ekr.20051025071455.20:spellTab.__init__
    #@+node:ekr.20051025094004:init_aspell
    def init_aspell (self,c):
    
        '''Init aspell and related ivars.  Return True if all went well.'''
    
        self.local_language_code = c.config.getString('spell_local_language_code') or 'en'
    
        self.dictionaryFileName = dictionaryFileName = (
            c.config.getString('spell_local_dictionary') or
            os.path.join(g.app.loadDir,"../","plugins",'spellpyx.txt'))
        
        if not dictionaryFileName or not g.os_path_exists(dictionaryFileName):
            g.es_print('Can not open dictionary file: %s' % (
                dictionaryFileName), color='red')
            return False
    
        self.aspell = Aspell(c,dictionaryFileName,self.local_language_code)
        
        if not self.aspell.aspell:
            g.es_print('Can not open Aspell',color='red')
            return False
            
        self.dictionary = self.readDictionary(dictionaryFileName)
        return True
    #@-node:ekr.20051025094004:init_aspell
    #@+node:ekr.20051025071455.22:createSpellTab
    def createSpellTab(self,parentFrame):
    
        """Create the Spell tab."""
        
        c = self.c
        
        # Set the common background color.
        bg = c.config.getColor('log_pane_Spell_tab_background_color') or 'LightSteelBlue2'
        
        #@    << Create the outer frames >>
        #@+node:ekr.20051113090322:<< Create the outer frames >>
        self.outerScrolledFrame = Pmw.ScrolledFrame(
            parentFrame,usehullsize = 1)
        
        self.outerFrame = outer = self.outerScrolledFrame.component('frame')
        self.outerFrame.configure(background=bg)
        
        for z in ('borderframe','clipper','frame','hull'):
            self.outerScrolledFrame.component(z).configure(
                relief='flat',background=bg)
        #@nonl
        #@-node:ekr.20051113090322:<< Create the outer frames >>
        #@nl
        #@    << Create the text and suggestion panes >>
        #@+node:ekr.20051025071455.23:<< Create the text and suggestion panes >>
        f2 = Tk.Frame(outer,bg=bg)
        f2.pack(side='top',expand=0,fill='x')
        
        self.wordLabel = Tk.Label(f2,text="Suggestions for:")
        self.wordLabel.pack(side='left')
        self.wordLabel.configure(font=('verdana',10,'bold'))
        
        fpane = Tk.Frame(outer,bg=bg,bd=2)
        fpane.pack(side='top',expand=1,fill='both')
        
        self.listBox = Tk.Listbox(fpane,height=6,width=10,selectmode="single")
        self.listBox.pack(side='left',expand=1,fill='both')
        self.listBox.configure(font=('verdana',11,'normal'))
        
        listBoxBar = Tk.Scrollbar(fpane,name='listBoxBar')
        
        bar, txt = listBoxBar, self.listBox
        txt ['yscrollcommand'] = bar.set
        bar ['command'] = txt.yview
        bar.pack(side='right',fill='y')
        #@nonl
        #@-node:ekr.20051025071455.23:<< Create the text and suggestion panes >>
        #@nl
        #@    << Create the spelling buttons >>
        #@+node:ekr.20051025071455.24:<< Create the spelling buttons >>
        # Create the alignment panes
        buttons1 = Tk.Frame(outer,bd=1,bg=bg)
        buttons2 = Tk.Frame(outer,bd=1,bg=bg)
        buttons3 = Tk.Frame(outer,bd=1,bg=bg)
        for w in (buttons1,buttons2,buttons3):
            w.pack(side='top',expand=0,fill='x')
        
        buttonList = [] ; font = ('verdana',9,'normal') ; width = 12
        for frame, text, command in (
            (buttons1,"Find",self.onFindButton),
            (buttons1,"Add",self.onAddButton),
            (buttons2,"Change",self.onChangeButton),
            (buttons2,"Change, Find",self.onChangeThenFindButton),
            (buttons3,"Ignore",self.onIgnoreButton),
            (buttons3,"Hide",self.onHideButton),
        ):
            b = Tk.Button(frame,font=font,width=width,text=text,command=command)
            b.pack(side='left',expand=0,fill='none')
            buttonList.append(b)
        
        # Used to enable or disable buttons.
        (self.findButton,self.addButton,
         self.changeButton, self.changeFindButton,
         self.ignoreButton, self.hideButton) = buttonList
        #@nonl
        #@-node:ekr.20051025071455.24:<< Create the spelling buttons >>
        #@nl
        
        # Pack last so buttons don't get squished.
        self.outerScrolledFrame.pack(expand=1,fill='both',padx=2,pady=2)
        
        self.fillbox([])
        self.listBox.bind("<Double-1>",self.onChangeThenFindButton)
        self.listBox.bind("<Button-1>",self.onSelectListBox)
        self.listBox.bind("<Map>",self.onMap)
    #@nonl
    #@-node:ekr.20051025071455.22:createSpellTab
    #@+node:ekr.20051025120920:createBindings (spellTab)
    def createBindings (self):
        
        c = self.c ; k = c.k
        widgets = (self.listBox, self.outerFrame)
    
        for w in widgets:
    
            # Bind shortcuts for the following commands...
            for commandName,func in (
                ('full-command',            k.fullCommand),
                ('hide-spell-tab',          self.hide),
                ('spell-add',               self.add),
                ('spell-find',              self.find),
                ('spell-ignore',            self.ignore),
                ('spell-change-then-find',  self.changeThenFind),
            ):
                junk, bunchList = c.config.getShortcut(commandName)
                for bunch in bunchList:
                    accel = bunch.val
                    shortcut = k.shortcutFromSetting(accel)
                    if shortcut:
                        # g.trace(shortcut,commandName)
                        w.bind(shortcut,func)
               
    #@nonl
    #@-node:ekr.20051025120920:createBindings (spellTab)
    #@+node:ekr.20051025071455.16:readDictionary
    def readDictionary (self,fileName):
    
        """Read the dictionary of words which we use as a local dictionary
        
        Although Aspell itself has the functionality to handle this kind of things
        we duplicate it here so that we can also use it for the "ignore" functionality
        and so that in future a Python only solution could be developed."""
        
        d = {}
    
        try:
            f = open(fileName,"r")
        except IOError:
            g.es("Unable to open local dictionary '%s' - using a blank one instead" % fileName)
            return d
    
        try:
            # Create the dictionary - there are better ways to do this
            # in later Python's but we stick with this method for compatibility
            for word in f.readlines():
                d [word.strip().lower()] = 0
        finally:
            f.close()
    
        return d
    #@nonl
    #@-node:ekr.20051025071455.16:readDictionary
    #@-node:ekr.20051025071455.19:Birth & death
    #@+node:ekr.20051025071455.29:Buttons
    #@+node:ekr.20051025071455.30:onAddButton
    def onAddButton(self):
        """Handle a click in the Add button in the Check Spelling dialog."""
    
        self.add()
    #@nonl
    #@-node:ekr.20051025071455.30:onAddButton
    #@+node:ekr.20051025071455.31:onIgnoreButton
    def onIgnoreButton(self,event=None):
    
        """Handle a click in the Ignore button in the Check Spelling dialog."""
    
        self.ignore()
    #@nonl
    #@-node:ekr.20051025071455.31:onIgnoreButton
    #@+node:ekr.20051025071455.32:onChangeButton & onChangeThenFindButton
    def onChangeButton(self,event=None):
    
        """Handle a click in the Change button in the Spell tab."""
    
        self.change()
        self.updateButtons()
        
    
    def onChangeThenFindButton(self,event=None):
        
        """Handle a click in the "Change, Find" button in the Spell tab."""
    
        if self.change():
            self.find()
        self.updateButtons()
    #@-node:ekr.20051025071455.32:onChangeButton & onChangeThenFindButton
    #@+node:ekr.20051025071455.33:onFindButton
    def onFindButton(self):
    
        """Handle a click in the Find button in the Spell tab."""
    
        c = self.c
        self.find()
        self.updateButtons()
        c.invalidateFocus()
        c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20051025071455.33:onFindButton
    #@+node:ekr.20051025071455.34:onHideButton
    def onHideButton(self):
        
        """Handle a click in the Hide button in the Spell tab."""
        
        self.hide()
    #@nonl
    #@-node:ekr.20051025071455.34:onHideButton
    #@-node:ekr.20051025071455.29:Buttons
    #@+node:ekr.20051025071455.36:Commands
    #@+node:ekr.20051025071455.37:add
    def add(self,event=None):
        """Add the selected suggestion to the dictionary."""
        
        try:
            f = None
            try:
                # Rewrite the dictionary in alphabetical order.
                f = open(self.dictionaryFileName, "r")
                words = f.readlines()
                f.close()
                words = [word.strip() for word in words]
                words.append(self.currentWord)
                words.sort()
                f = open(self.dictionaryFileName, "w")
                for word in words:
                    f.write("%s\n" % word)
                f.flush()
                f.close()
                if 1:
                    s = 'Spell: added %s' % self.currentWord
                    self.messages.append(s)
                else: # Too distracting.
                    g.es("Adding ", color= "blue", newline= False) 
                    g.es('%s' % self.currentWord)
            except IOError:
                g.es("Can not add %s to dictionary" % self.currentWord, color="red")
        finally:
            if f: f.close()
            
        self.dictionary[self.currentWord.lower()] = 0
        self.onFindButton()
    #@nonl
    #@-node:ekr.20051025071455.37:add
    #@+node:ekr.20051025071455.38:change
    def change(self,event=None):
        """Make the selected change to the text"""
    
        __pychecker__ = '--no-override --no-argsused'
             # event param is not used, required, and different from base class.
    
        c = self.c ; body = self.body ; t = body.bodyCtrl
        
        selection = self.getSuggestion()
        if selection:
            start,end = oldSel = g.app.gui.getTextSelection(t)
            if start:
                if t.compare(start, ">", end):
                    start,end = end,start
                t.delete(start,end)
                t.insert(start,selection)
                g.app.gui.setTextSelection(t,start,start + "+%dc" % (len(selection)))
                c.frame.body.onBodyChanged("Change",oldSel=oldSel)
                c.invalidateFocus()
                c.bodyWantsFocusNow()
                return True
    
        # The focus must never leave the body pane.
        c.invalidateFocus()
        c.bodyWantsFocusNow()
        return False
    #@nonl
    #@-node:ekr.20051025071455.38:change
    #@+node:ekr.20051025071455.40:find
    def find (self,event=None):
        """Find the next unknown word."""
    
        c = self.c ; body = c.frame.body ; bodyCtrl = body.bodyCtrl
    
        # Reload the work pane from the present node.
        s = bodyCtrl.get("1.0","end").rstrip()
        self.workCtrl.delete("1.0","end")
        self.workCtrl.insert("end",s)
    
        # Reset the insertion point of the work widget.
        ins = bodyCtrl.index("insert")
        self.workCtrl.mark_set("insert",ins)
    
        alts, word = self.findNextMisspelledWord()
        self.currentWord = word # Need to remember this for 'add' and 'ignore'
    
        if alts:
            self.fillbox(alts,word)
            c.invalidateFocus()
            c.bodyWantsFocusNow()
            # Copy the working selection range to the body pane
            start, end = g.app.gui.getTextSelection(self.workCtrl)
            g.app.gui.setTextSelection(bodyCtrl,start,end)
            bodyCtrl.see(start)
        else:
            g.es("no more misspellings")
            self.fillbox([])
            c.invalidateFocus()
            c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20051025071455.40:find
    #@+node:ekr.20051025121408:hide
    def hide (self,event=None):
        
        self.c.frame.log.selectTab('Log')
        
        for message in self.messages:
            g.es(message,color='blue')
            
        self.messages = []
    #@nonl
    #@-node:ekr.20051025121408:hide
    #@+node:ekr.20051025071455.41:ignore
    def ignore(self,event=None):
    
        """Ignore the incorrect word for the duration of this spell check session."""
        
        if 1: # Somewhat helpful: applies until the tab is destroyed.
            s = 'Spell: ignore %s' % self.currentWord
            self.messages.append(s)
    
        if 0: # Too distracting
            g.es("Ignoring ", color= "blue", newline= False)
            g.es('%s' % self.currentWord)
    
        self.dictionary[self.currentWord.lower()] = 0
        self.onFindButton()
    #@nonl
    #@-node:ekr.20051025071455.41:ignore
    #@-node:ekr.20051025071455.36:Commands
    #@+node:ekr.20051025071455.42:Helpers
    #@+node:ekr.20051025071455.43:bringToFront
    def bringToFront (self):
        
        self.c.frame.log.selectTab('Spell')
    #@nonl
    #@-node:ekr.20051025071455.43:bringToFront
    #@+node:ekr.20051025071455.44:fillbox
    def fillbox(self, alts, word=None):
        """Update the suggestions listbox in the Check Spelling dialog."""
        
        self.suggestions = alts
        
        if not word:
            word = ""
    
        self.wordLabel.configure(text= "Suggestions for: " + word)
        self.listBox.delete(0, "end")
    
        for i in xrange(len(self.suggestions)):
            self.listBox.insert(i, self.suggestions[i])
        
        # This doesn't show up because we don't have focus.
        if len(self.suggestions):
            self.listBox.select_set(1) 
    
    #@-node:ekr.20051025071455.44:fillbox
    #@+node:ekr.20051025071455.45:findNextMisspelledWord
    def findNextMisspelledWord(self):
        """Find the next unknown word."""
        
        c = self.c ; p = c.currentPosition()
        aspell = self.aspell ; alts = None ; word = None
       
        try:
            while 1:
                p, word = self.findNextWord(p) 
                if not p or not word:
                    alts = None
                    break
                #@            << Skip word if ignored or in local dictionary >>
                #@+node:ekr.20051025071455.46:<< Skip word if ignored or in local dictionary >>
                #@+at 
                #@nonl
                # We don't bother to call apell if the word is in our 
                # dictionary. The dictionary contains both locally 'allowed' 
                # words and 'ignored' words. We put the test before aspell 
                # rather than after aspell because the cost of checking aspell 
                # is higher than the cost of checking our local dictionary. 
                # For small local dictionaries this is probably not True and 
                # this code could easily be located after the aspell call
                #@-at
                #@@c
                
                if self.dictionary.has_key(word.lower()):
                    continue
                #@nonl
                #@-node:ekr.20051025071455.46:<< Skip word if ignored or in local dictionary >>
                #@nl
                alts = aspell.processWord(word)
                if alts:
                    c.beginUpdate()
                    c.frame.tree.expandAllAncestors(p)
                    c.selectPosition(p)
                    c.endUpdate()
                    break
        except:
            g.es_exception()
        return alts, word
    #@nonl
    #@-node:ekr.20051025071455.45:findNextMisspelledWord
    #@+node:ekr.20051025071455.47:findNextWord
    # Unicode characters may cause index problems.
    
    def findNextWord(self,p):
    
        """Scan for the next word, leaving the result in the work widget"""
    
        t = self.workCtrl
    
        # Allow quotes and underscores in the middle of words, but not at the beginning or end.
        # This breaks words at non-ascii 'letters' such as é.  I don't know what the solution is.
        word_start = string.letters
        word_end   = string.letters + string.digits
        word_chars = string.letters + string.digits + "`" + "'" + "_"
        while 1:
            line = t.get('insert wordstart','insert lineend')
            # g.trace('insert',t.index('insert'),'insert wordstart',t.index('insert wordstart'))
            # g.trace(repr(line))
            # Start the word at the first letter.
            i = 0
            while i < len(line) and line[i] not in word_start:
                i += 1
            if i < len(line):
                # A non-empty word has been found.
                line = t.get('insert wordstart','insert lineend')
                j = i
                while j < len(line) and line[j] in word_chars:
                    j += 1
                word = line[i:j]
                while word and word[-1] not in word_end:
                    word = word[:-1]
                # This trace is important: it verifies that all words have actually been checked.
                # g.trace(repr(word))
                x1 = t.index('insert + %dc' % (i))
                x2 = t.index('insert + %dc' % (i+len(word)))
                g.app.gui.setTextSelection(t,x1,x2)
                return p, word
            else:
                # End of the line. Bug fix: 9/8/05.
                t.mark_set('insert','insert lineend + 1c')
                if t.compare("insert",">=", "end - 1c"):
                    p.moveToThreadNext()
                    if not p: return None,None
                    t.delete("1.0", "end")
                    t.insert("end", p.bodyString())
                    t.mark_set("insert", "1.0")
                    
        __pychecker__ = '--no-implicitreturns' # This is not really an implicit return.
    #@nonl
    #@-node:ekr.20051025071455.47:findNextWord
    #@+node:ekr.20051025071455.48:getSuggestion
    def getSuggestion(self):
        """Return the selected suggestion from the listBox."""
        
        # Work around an old Python bug.  Convert strings to ints.
        items = self.listBox.curselection()
        try:
            items = map(int, items)
        except ValueError: pass
    
        if items:
            n = items[0]
            suggestion = self.suggestions[n]
            return suggestion
        else:
            return None
    #@nonl
    #@-node:ekr.20051025071455.48:getSuggestion
    #@+node:ekr.20051025071455.49:onMap
    def onMap (self, event=None):
        """Respond to a Tk <Map> event."""
        
        self.update(show= False, fill= False)
    #@nonl
    #@-node:ekr.20051025071455.49:onMap
    #@+node:ekr.20051025071455.50:onSelectListBox
    def onSelectListBox(self, event=None):
        """Respond to a click in the selection listBox."""
        
        c = self.c
        self.updateButtons()
        c.bodyWantsFocus()
    #@-node:ekr.20051025071455.50:onSelectListBox
    #@+node:ekr.20051025071455.51:update
    def update(self,show=True,fill=False):
        
        """Update the Spell Check dialog."""
        
        c = self.c
        
        if fill:
            self.fillbox([])
    
        self.updateButtons()
    
        if show:
            self.bringToFront()
            c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051025071455.51:update
    #@+node:ekr.20051025071455.52:updateButtons
    def updateButtons (self):
    
        """Enable or disable buttons in the Check Spelling dialog."""
    
        c = self.c
    
        start, end = g.app.gui.getTextSelection(c.frame.body.bodyCtrl)
        state = g.choose(self.suggestions and start,"normal","disabled")
    
        self.changeButton.configure(state=state)
        self.changeFindButton.configure(state=state)
    
        # state = g.choose(self.c.undoer.canRedo(),"normal","disabled")
        # self.redoButton.configure(state=state)
        # state = g.choose(self.c.undoer.canUndo(),"normal","disabled")
        # self.undoButton.configure(state=state)
    
        self.addButton.configure(state='normal')
        self.ignoreButton.configure(state='normal')
    #@nonl
    #@-node:ekr.20051025071455.52:updateButtons
    #@-node:ekr.20051025071455.42:Helpers
    #@-others
#@nonl
#@-node:ekr.20051025071455.18:class spellTab (leoFind.leoFind)
#@-others
#@-node:ekr.20051025071455:Spell classes (ok)
#@-others

#@<< define classesList >>
#@+node:ekr.20050922104213:<< define classesList >>
classesList = [
    ('abbrevCommands',      abbrevCommandsClass),
    ('bufferCommands',      bufferCommandsClass),
    ('editCommands',        editCommandsClass),
    ('controlCommands',     controlCommandsClass),
    ('debugCommands',       debugCommandsClass),
    ('editFileCommands',    editFileCommandsClass),
    ('helpCommands',        helpCommandsClass),
    ('keyHandlerCommands',  keyHandlerCommandsClass),
    ('killBufferCommands',  killBufferCommandsClass),
    ('leoCommands',         leoCommandsClass),
    ('macroCommands',       macroCommandsClass),
    ('queryReplaceCommands',queryReplaceCommandsClass),
    ('rectangleCommands',   rectangleCommandsClass),
    ('registerCommands',    registerCommandsClass),
    ('searchCommands',      searchCommandsClass),
    ('spellCommands',       spellCommandsClass),
]
#@nonl
#@-node:ekr.20050922104213:<< define classesList >>
#@nl
#@nonl
#@-node:ekr.20050710142719:@thin leoEditCommands.py
#@-leo
