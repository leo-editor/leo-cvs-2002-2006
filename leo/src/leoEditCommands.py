#@+leo-ver=4-thin
#@+node:ekr.20050710142719:@thin leoEditCommands.py
'''Basic editor commands for Leo.r

Modelled after Emacs and Vim commands.'''

#@<< imports >>
#@+node:ekr.20050710151017:<< imports >>
import leoGlobals as g

import leoFind
import leoKeys
import leoNodes

import cPickle
import difflib
import os
import re
import string

subprocess     = g.importExtension('subprocess',    pluginName=None,verbose=False)
Pmw            = g.importExtension('Pmw',           pluginName=None,verbose=False)
Tk             = g.importExtension('Tkinter',       pluginName=None,verbose=False)
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
        self.k = self.keyHandler = None
        self.registers = {} # To keep pychecker happy.
        
    def finishCreate(self):
    
        # Class delegators.
        self.k = self.keyHandler = self.c.keyHandler
        
    def init (self):
        
        '''Called from k.keyboardQuit to init all classes.'''
        
        pass
    #@nonl
    #@-node:ekr.20050920084036.2: ctor, finishCreate, init (baseEditCommandsClass)
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
            g.callerName(2),
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
    def _chckSel (self,event,warning=''):
        
        k = self.k ; w = event.widget
    
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
    def getRectanglePoints (self,event):
    
        w = event.widget
        i = w.index('sel.first')
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
#@+node:ekr.20050920084036.13:class abbrevCommandsClass
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
#@-node:ekr.20050920084036.13:class abbrevCommandsClass
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
        self.bufferDict = {}
        self.positions = {}
        self.tnodes = {}
    #@nonl
    #@-node:ekr.20050920084036.32: ctor (bufferCommandsClass)
    #@+node:ekr.20050920084036.33: getPublicCommands
    def getPublicCommands (self):
    
        return {
            'append-to-buffer':     self.appendToBuffer,
            'copy-to-buffer':       self.copyToBuffer,
            'insert-to-buffer':     self.insertToBuffer,
            'kill-buffer' :         self.killBuffer,
            'list-buffers' :        self.listBuffers,
            'prepend-to-buffer':    self.prependToBuffer,
            'rename-buffer':        self.renameBuffer,
            'switch-to-buffer':     self.switchToBuffer,
        }
    #@nonl
    #@-node:ekr.20050920084036.33: getPublicCommands
    #@+node:ekr.20050920084036.34:Entry points
    #@+node:ekr.20050920084036.35:appendToBuffer/Finisher
    def appendToBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Append to buffer: ')
        self.getBufferName(event,self.appendToBufferFinisher)
    
    def appendToBufferFinisher (self,event,name):
    
        k = self.k ; w = event.widget
        txt = w.get('sel.first','sel.last')
        try:
            bdata = self.bufferDict [name]
            bdata = '%s%s' % (bdata,txt)
            self.setBufferData(event,name,bdata)
            k.commandName = 'Append to buffer: %s' % name
        except Exception:
            pass
    #@nonl
    #@-node:ekr.20050920084036.35:appendToBuffer/Finisher
    #@+node:ekr.20050920084036.36:copyToBuffer/Finisher
    def copyToBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Copy to buffer: ')
        self.getBufferName(event,self.copyToBufferFinisher)
    
    def copyToBufferFinisher (self,event,name):
    
        k = self.k ; w = event.widget
        try:
            txt = w.get('sel.first','sel.last')
            self.setBufferData(event,name,txt)
            k.commandName = 'Copy to buffer: %s' % name
        except Exception:
            pass
    #@nonl
    #@-node:ekr.20050920084036.36:copyToBuffer/Finisher
    #@+node:ekr.20050920084036.37:insertToBuffer/Finisher
    def insertToBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Insert to buffer: ')
        self.getBufferName(event,self.insertToBufferFinisher)
    
    def insertToBufferFinisher (self,event,name):
        
        k = self.k ; w = event.widget
        try:
            bdata = self.bufferDict [name]
            w.insert('insert',bdata)
            k.commandName = 'Insert to buffer: %s' % name
        except Exception:
            pass
    #@nonl
    #@-node:ekr.20050920084036.37:insertToBuffer/Finisher
    #@+node:ekr.20050920084036.38:killBuffer/Finisher  (not ready yet)
    def killBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Kill buffer: ')
        self.getBufferName(event,self.killBufferFinisher)
    
    def killBufferFinisher (self,event,name):
        
        k = self.k
        
        # w = event.widget
        # method = self.bufferDeletes[w]
        # method(name)
    
        pass ### Not ready yet.
        
        k.commandName = 'Kill buffer: %s' % name
    #@nonl
    #@-node:ekr.20050920084036.38:killBuffer/Finisher  (not ready yet)
    #@+node:ekr.20050920084036.42:listBuffers/Finisher (not ready yet)
    def listBuffers (self,event):
        
        k = self.k ; c = k.c
        
        names = {}
        for p in c.allNodes_iter():
            names [p.headString()] = None
    
        buffers = names.keys()
        buffers.sort()
        
        if 0: # This would be too much data for now...
            data = '\n'.join(buffers)
            k.setLabelGrey(data)
    #@nonl
    #@-node:ekr.20050920084036.42:listBuffers/Finisher (not ready yet)
    #@+node:ekr.20050920084036.39:prependToBuffer/Finisher
    def prependToBuffer (self,event):
        
        k = self.k
        k.setLabelBlue('Prepend to buffer: ')
        self.getBufferName(event,self.prependToBufferFinisher)
        
    def prependToBufferFinisher (self,event,name):
        
        k = self.k ; w = event.widget
        
        try:
            txt = w.get('sel.first','sel.last')
            bdata = self.bufferDict[name]
            bdata = '%s%s'%(txt,bdata)
            self.setBufferData(event,name,bdata)
            k.commandName = 'Prepend to buffer: %s' % name
        except Exception:
            pass
    #@nonl
    #@-node:ekr.20050920084036.39:prependToBuffer/Finisher
    #@+node:ekr.20050920084036.43:renameBuffer (not ready yet)
    def renameBuffer (self,event):
        
        k = self.k
        k.setLabelBlue('Rename buffer from: ')
        self.getBufferName(event,self.renameBufferFinisher1)
        
    def renameBufferFinisher1 (self,event,name):
        
        k = self.k
        k.setLabelBlue('Rename buffer from: %s to: ' % (name))
        self.fromName = name
        self.getBufferName(event,self.renameBufferFinisher2)
        
    def renameBufferFinisher2 (self,event,name):
    
        k = self.k
        
        # w = event.widget
        # self.renameBuffers[w](name)
    
        k.setLabelGrey('Renamed buffer %s to %s' % (self.fromName,name))
    #@nonl
    #@-node:ekr.20050920084036.43:renameBuffer (not ready yet)
    #@+node:ekr.20050920084036.40:switchToBuffer (not ready yet)
    def switchToBuffer (self,event):
        
        k = self.k
        k.setLabelBlue('Switch to buffer: ')
        self.getBufferName(event,self.switchToBufferFinisher)
        
    def switchToBufferFinisher (self,event,name):
        
        k = self.k
        
        ### To be removed.
        __pychecker__ = '--no-argsused' # name not used yet.
        
        # w = event.widget
        # method = self.bufferGotos[event.widget]
        # k.keyboardQuit(event)
        # method(name)
        
        pass ### Not ready yet.
    #@nonl
    #@-node:ekr.20050920084036.40:switchToBuffer (not ready yet)
    #@-node:ekr.20050920084036.34:Entry points
    #@+node:ekr.20050927093851:getBufferName
    def getBufferName (self,event,func=None):
        
        '''Get a buffer name into k.arg and call k.setState(kind,n,handler).'''
        
        k = self.k ; c = k.c ; state = k.getState('getBufferName')
        
        if state == 0:
            # Creating a helper dict is much faster than creating the list directly.
            names = {}
            for p in c.allNodes_iter():
                names [p.headString()] = None
            tabList = names.keys()
            self.getBufferNameFinisher = func
            prefix = k.getLabel()
            k.getArg(event,'getBufferName',1,self.getBufferName,prefix=prefix,tabList=tabList)
        else:
            k.resetLabel()
            k.clearState()
            # g.trace(repr(k.arg))
            func = self.getBufferNameFinisher
            self.getBufferNameFinisher = None
            if func:
                func(event,k.arg)
    #@nonl
    #@-node:ekr.20050927093851:getBufferName
    #@+node:ekr.20050927102133.1:Utils
    #@+node:ekr.20050927101829.3:setBufferData
    def setBufferData (self,event,name,data):
    
        c = self.c
        data = unicode(data)
        d = self.tnodes [c]
        if d.has_key(name):
            d [name].bodyString = data
    #@nonl
    #@-node:ekr.20050927101829.3:setBufferData
    #@+node:ekr.20050927101829.4:gotoNode (not used!)
    def gotoNode (self,name):
        
        c = self.c
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
                            self.gotoPosition(c,posis[cpos])
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
                    self.gotoPosition(c,pos)
            else:
                pos2 = c.currentPosition()
                tnd = leoNodes.tnode('',name)
                pos = pos2.insertAfter(tnd)
                self.gotoPosition(c,pos)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20050927101829.4:gotoNode (not used!)
    #@+node:ekr.20050927101829.5:gotoPosition
    def gotoPosition (self,c,pos):
    
        c.frame.tree.expandAllAncestors(pos)
        c.selectPosition(pos)
    #@nonl
    #@-node:ekr.20050927101829.5:gotoPosition
    #@+node:ekr.20050927101829.6:deleteNode (not used?)
    def deleteNode (self,name):
        
        c = self.c
    
        c.beginUpdate()
        try:
            if self.positions.has_key(name):
                pos = self.positions [name]
                cpos = c.currentPosition()
                pos.doDelete(cpos)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20050927101829.6:deleteNode (not used?)
    #@+node:ekr.20050927101829.7:renameNode (not used?)
    def renameNode (self,name):
        
        c = self.c
    
        c.beginUpdate()
        try:
            pos = c.currentPosition()
            pos.setHeadString(name)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20050927101829.7:renameNode (not used?)
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
            'iconfify-or-deiconify-frame':  self.iconifyOrDeiconifyFrame,
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
        
    iconifyOrDeiconifyFrame = suspend
    #@nonl
    #@-node:ekr.20050920084036.153:suspend & iconifyOrDeiconifyFrame
    #@-others
#@nonl
#@-node:ekr.20050920084036.150:class controlCommandsClass
#@+node:ekr.20050920084036.53:class editCommandsClass
class editCommandsClass (baseEditCommandsClass):
    
    '''Contains editing commands with little or no state.'''

    #@    @+others
    #@+node:ekr.20050929155208: birth
    #@+node:ekr.20050920084036.54: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.ccolumn = '0'   # For comment column functions.
        self.dynaregex = re.compile(r'[%s%s\-_]+'%(string.ascii_letters,string.digits))
            # For dynamic abbreviations
        self.fillPrefix = '' # For fill prefix functions.
        self.fillColumn = 70 # For line centering.
        self.store ={'rlist':[], 'stext':''} # For dynamic expansion.
        self.swapSpots = []
        self._useRegex = False # For replace-string and replace-regex
        self.widget = None # For use by state handlers.
    #@nonl
    #@-node:ekr.20050920084036.54: ctor
    #@+node:ekr.20050920084036.55: getPublicCommands (editCommandsClass)
    def getPublicCommands (self):
    
        k = self.k
    
        return {
            'back-sentence':        self.backSentence,
            'back-to-indentation':  self.backToIndentation,
            'backward-char':        self.backCharacter,
            'backward-delete-char': self.backwardDeleteCharacter,
            'backward-kill-paragraph': self.backwardKillParagraph,
            'backward-paragraph':   self.backwardParagraph,
            'backward-word':        self.backwardWord,
            'beginning-of-buffer':  self.beginningOfBuffer,
            'beginning-of-line':    self.beginningOfLine,
            'capitalize-word':      self.capitalizeWord,
            'center-line':          self.centerLine,
            'center-region':        self.centerRegion,
            'count-region':         self.countRegion,
            'cycle-focus':          self.cycleFocus,
            'dabbrev-completion':   self.dynamicExpansion2,
            'dabbrev-expands':      self.dynamicExpansion,
            'delete-char':          self.deleteNextChar,
            'delete-indentation':   self.deleteIndentation,
            'delete-spaces':        self.deleteSpaces,
            'downcase-region':      self.downCaseRegion,
            'downcase-word':        self.downCaseWord,
            'end-of-buffer':        self.endOfBuffer,
            'end-of-line':          self.endOfLine,
            'escape':               self.watchEscape,
            'eval-expression':      self.evalExpression,
            'exchange-point-mark':  self.exchangePointMark,
            'fill-paragraph':       self.fillParagraph,
            'fill-region':          self.fillRegion,
            'fill-region-as-paragraph': self.fillRegionAsParagraph,
            'flush-lines':          self.flushLines,
            'focus-to-body':        self.focusToBody,
            'focus-to-log':         self.focusToLog,
            'focus-to-tree':        self.focusToTree,
            'forward-char':         self.forwardCharacter,
            'forward-paragraph':    self.forwardParagraph,
            'forward-sentence':     self.forwardSentence,
            'forward-word':         self.forwardWord,
            'goto-char':            self.gotoCharacter,
            'goto-line':            self.gotoLine,
            'how-many':             self.howMany,
            'indent-region':        self.indentRegion,
            'indent-relative':      self.indentRelative,
            'indent-rigidly':       self.tabIndentRegion,
            'indent-to-comment-column': self.indentToCommentColumn,
            'insert-newline':       self.insertNewline,
            'insert-parentheses':   self.insertParentheses,
            'keep-lines':           self.keepLines,
            'kill-paragraph':       self.killParagraph,
            'line-number':          self.lineNumber,
            'move-past-close':      self.movePastClose,
            'newline-and-indent':   self.insertNewLineAndTab,
            'next-line':            self.nextLine,
            'previous-line':        self.prevLine,
            'remove-blank-lines':   self.removeBlankLines,
            'replace-regex':        self.activateReplaceRegex,
            'replace-string':       self.replaceString,
            'reverse-region':       self.reverseRegion,
            'scroll-down':          self.scrollDown,
            'scroll-up':            self.scrollUp,
            'select-paragraph':     self.selectParagraph,
            'set-comment-column':   self.setCommentColumn,
            'set-fill-column':      self.setFillColumn,
            'set-fill-prefix':      self.setFillPrefix,
            'set-mark-command':     self.setRegion,
            'show-colors':          self.showColors,
            'show-fonts':           self.showFonts,
            # 'save-buffer':        self.saveFile,
            'sort-columns':         self.sortColumns,
            'sort-fields':          self.sortFields,
            'sort-lines':           self.sortLines,
            'split-line':           self.insertNewLineIndent,
            'tabify':               self.tabify,
            'transpose-chars':      self.transposeCharacters,
            'transpose-lines':      self.transposeLines,
            'transpose-words':      self.transposeWords,
            'untabify':             self.untabify,
            'upcase-region':        self.upCaseRegion,
            'upcase-word':          self.upCaseWord,
            'view-lossage':         self.viewLossage,
            'what-line':            self.whatLine,
        }
    #@nonl
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
    
        self.moveWordHelper(event,-1)
    
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
        except:
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
    #@+node:ekr.20050920084036.85:delete...
    #@+node:ekr.20050929163010:backwardDeleteCharacter
    def backwardDeleteCharacter (self,event):
    
        try:
            w = event.widget
            i = w.index('insert')
            w.delete('%s-1c' % (i), '%s' % (i))
        except Exception:
            pass #  w might not be a text widget.
    #@nonl
    #@-node:ekr.20050929163010:backwardDeleteCharacter
    #@+node:ekr.20050920084036.87:deleteNextChar
    def deleteNextChar (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        w.delete(i,'%s +1c' % i)
    #@nonl
    #@-node:ekr.20050920084036.87:deleteNextChar
    #@+node:ekr.20050920084036.135:deleteSpaces
    def deleteSpaces (self,event,insertspace=False):
    
        k = self.k ; w = event.widget
        char = w.get('insert','insert + 1c ')
        if not char.isspace(): return
        
        i = w.index('insert')
        wf = w.search(r'\w',i,stopindex='%s lineend' % i,regexp=True)
        wb = w.search(r'\w',i,stopindex='%s linestart' % i,regexp=True,backwards=True)
        if '' in (wf,wb): return
        w.delete('%s +1c' % wb,wf)
        if insertspace: w.insert('insert',' ')
    #@nonl
    #@-node:ekr.20050920084036.135:deleteSpaces
    #@+node:ekr.20050920084036.141:removeBlankLines
    def removeBlankLines (self,event):
        
        w = event.widget
        i = w.index('insert')
        i1, i2 = i.split('.')
        i1 = int(i1) ; dindex = []
        if w.get('insert linestart','insert lineend').strip() == '':
            while str(i1) + '.0' != '1.0':
                i1 -= 1
                g.trace('loop1',i1)
                s = w.get('%s.0' % i1,'%s.0 lineend' % i1).strip()
                if not s:
                    dindex.append('%s.0' % i1)
                    dindex.append('%s.0 lineend' % i1)
                elif dindex:
                    w.delete('%s-1c' % dindex[-2],dindex[1])
                    w.event_generate('<Key>')
                    w.update_idletasks() # Needed to continue the loop.
                    break
                else:
                    break
        i = w.index('insert')
        i1, i2 = i.split('.')
        i1 = int(i1) ; dindex = []
        while w.index('%s.0 lineend' % i1) != w.index('end'):
            i1 += 1
            g.trace('loop1',i1)
            s = w.get('%s.0' % i1,'%s.0 lineend' % i1).strip()
            if not s:
                dindex.append('%s.0' % i1)
                dindex.append('%s.0 lineend' % i1)
            elif dindex:
                w.delete('%s-1c' % dindex[0],dindex[-1])
                w.event_generate('<Key>')
                w.update_idletasks() # Needed to continue the loop.
                break
            else:
                break
    #@nonl
    #@-node:ekr.20050920084036.141:removeBlankLines
    #@-node:ekr.20050920084036.85:delete...
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
    #@+node:ekr.20050920084036.136:exchangePointMark
    def exchangePointMark (self,event):
    
        if not self._chckSel(event): return
    
        k = self.k ; w = event.widget
        s1 = w.index('sel.first')
        s2 = w.index('sel.last')
        i = w.index('insert')
        w.mark_set('insert',g.choose(i==s1,s2,s1))
    #@nonl
    #@-node:ekr.20050920084036.136:exchangePointMark
    #@+node:ekr.20051022142249:focus (editCommandsClass)
    #@+node:ekr.20051022144825:focusToBody/Log/Tree
    def focusToBody (self,event):
        frame = self.c.frame
        return frame.set_focus(frame.body.bodyCtrl,later=True)
    
    def focusToLog (self,event):
        frame = self.c.frame
        return frame.set_focus(frame.log.logCtrl,later=True)
    
    def focusToTree (self,event):
        frame = self.c.frame
        return frame.set_focus(frame.tree.canvas,later=True)
        
    #@-node:ekr.20051022144825:focusToBody/Log/Tree
    #@+node:ekr.20051022144825.1:cycleFocus
    def cycleFocus (self,event):
    
        c = self.c ; frame = c.frame
        
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
        frame.set_focus(pane,later=True)
    #@nonl
    #@-node:ekr.20051022144825.1:cycleFocus
    #@-node:ekr.20051022142249:focus (editCommandsClass)
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
    #@+node:ekr.20050920084036.74:indent...
    #@+node:ekr.20050920084036.75:backToIndentation
    def backToIndentation (self,event):
    
        w = event.widget
    
        i = w.index('insert linestart')
        i2 = w.search(r'\w',i,stopindex='%s lineend' % i,regexp=True)
        w.mark_set('insert',i2)
        ### w.update_idletasks()
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
    
        k = self.k ; w = event.widget
    
        i = w.index('insert')
        l, c = i.split('.')
        c2 = int(c)
        l2 = int(l) -1
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
                    ###w.update_idletasks()
    #@nonl
    #@-node:ekr.20050920084036.78:indentRelative
    #@-node:ekr.20050920084036.74:indent...
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
    #@+node:ekr.20050930102304:insert...
    #@+node:ekr.20050920084036.138:insertNewLine
    def insertNewLine (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        w.insert('insert','\n')
        w.mark_set('insert',i)
    
    insertNewline = insertNewLine
    #@-node:ekr.20050920084036.138:insertNewLine
    #@+node:ekr.20050920084036.86:insertNewLineAndTab
    def insertNewLineAndTab (self,event):
    
        '''Insert a newline and tab'''
    
        k = self.k ; w = event.widget
        self.insertNewLine(event)
        i = w.index('insert +1c')
        w.insert(i,'\t')
        w.mark_set('insert','%s lineend' % i)
    #@nonl
    #@-node:ekr.20050920084036.86:insertNewLineAndTab
    #@+node:ekr.20050920084036.139:insertParentheses
    def insertParentheses (self,event):
    
        k = self.k ; w = event.widget
        w.insert('insert','()')
        w.mark_set('insert','insert -1c')
    #@nonl
    #@-node:ekr.20050920084036.139:insertParentheses
    #@-node:ekr.20050930102304:insert...
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
    #@+node:ekr.20050929114218:move...
    #@+node:ekr.20050920084036.140:movePastClose
    def movePastClose (self,event):
    
        k = self.k ; w = event.widget
    
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
    
        ib = w.index('insert')
        w.mark_set('insert','%s lineend +1c' % i2)
        if w.index('insert') == w.index('%s lineend' % ib):
            w.insert('insert','\n')
    #@nonl
    #@-node:ekr.20050920084036.140:movePastClose
    #@+node:ekr.20050929115226.1:forward/backCharacter
    def backCharacter (self,event):
    
        try:
            w = event.widget
            i = w.index('insert')
            w.mark_set('insert','%s - 1c' % i)
        except Exception:
            pass #  w might not be a text widget.
        
    def forwardCharacter (self,event):
    
        try:
            w = event.widget
            i = w.index('insert')
            w.mark_set('insert','%s + 1c' % i)
        except Exception:
            pass #  w might not be a text widget.
    #@-node:ekr.20050929115226.1:forward/backCharacter
    #@+node:ekr.20050920084036.148:moveTo, beginnning/endOfBuffer/Line
    def moveTo (self,event,spot):
        w = event.widget
        w.mark_set(Tk.INSERT,spot)
        w.see(spot)
    
    def beginningOfBuffer (self,event):
        self.moveTo(event,'1.0')
    
    def beginningOfLine (self,event):
        self.moveTo(event,'insert linestart')
    
    def endOfBuffer (self,event):
        self.moveTo(event,'end')
    
    def endOfLine (self,event):
        self.moveTo(event,'insert lineend')
    #@nonl
    #@-node:ekr.20050920084036.148:moveTo, beginnning/endOfBuffer/Line
    #@+node:ekr.20050920084036.149:back/forwardWord & helper
    def moveWordHelper (self,event,forward=True):
    
        '''This function moves the cursor to the next word, direction dependent on the way parameter'''
    
        w = event.widget
        
        if forward:
             ind = w.search('\w','insert',stopindex='end',regexp=True)
             if ind: nind = '%s wordend' % ind
             else:   nind = 'end'
        else:
             ind = w.search('\w','insert -1c',stopindex='1.0',regexp=True,backwards=True)
             if ind: nind = '%s wordstart' % ind
             else:   nind = '1.0'
    
        w.mark_set('insert',nind)
        w.see('insert')
        ### w.event_generate('<Key>')
        ### w.update_idletasks()
    
    def backwardWord (self,event):
        self.moveWordHelper(event,forward=False)
    
    def forwardWord (self,event):
        self.moveWordHelper(event,forward=True)
    #@nonl
    #@-node:ekr.20050920084036.149:back/forwardWord & helper
    #@+node:ekr.20050920084036.131:backSentence
    def backSentence (self,event):
    
        k = self.k ; w = event.widget
        i = w.search('.','insert',backwards=True,stopindex='1.0')
    
        if i:
            i2 = w.search('.',i,backwards=True,stopindex='1.0')
            if not i2:
                i2 = '1.0'
            if i2:
                i3 = w.search('\w',i2,stopindex=i,regexp=True)
                if i3:
                    w.mark_set('insert',i3)
        else:
            w.mark_set('insert','1.0')
    #@nonl
    #@-node:ekr.20050920084036.131:backSentence
    #@+node:ekr.20050920084036.137:forwardSentence
    def forwardSentence (self,event):
    
        k = self.k ; w = event.widget
    
        i = w.search('.','insert',stopindex='end')
        if i:
            w.mark_set('insert','%s +1c' % i)
        else:
            w.mark_set('insert','end')
    #@nonl
    #@-node:ekr.20050920084036.137:forwardSentence
    #@+node:ekr.20050929163210:next/prevLine
    def nextLine (self,event):
    
        try:
            w = event.widget
            i = w.index('insert')
            w.mark_set('insert','%s + 1l' % i) # 1Line
        except Exception:
            pass #  w might not be a text widget.
    
    def prevLine (self,event):
    
        try:
            w = event.widget
            i = w.index('insert')
            w.mark_set('insert','%s - 1l' % i) # 1Line
        except Exception:
            pass #  w might not be a text widget.
    #@nonl
    #@-node:ekr.20050929163210:next/prevLine
    #@-node:ekr.20050929114218:move...
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
    #@+node:ekr.20050920084036.102:backwardParagraph
    def backwardParagraph (self,event):
    
        k = self.k ; w = event.widget ; i = w.index('insert')
    
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
            w.mark_set('insert',i)
            w.see('insert')
    #@-node:ekr.20050920084036.102:backwardParagraph
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
    #@+node:ekr.20051002100905:forwardParagraph
    def forwardParagraph (self,event):
        
        k = self.k ; w = event.widget ; i = w.index('insert')
    
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
            w.mark_set('insert',i) ; w.see('insert')
    #@nonl
    #@-node:ekr.20051002100905:forwardParagraph
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
    #@+node:ekr.20050920084036.112:replace...
    #@+node:ekr.20050920084036.113:replaceString
    def replaceString (self,event):
    
        k = self.k ; state = k.getState('replace-string')
        prompt = 'Replace ' + g.choose(self._useRegex,'Regex','String')
    
        if state == 0:
            self.widget = event.widget
            self._sString = self._rpString = ''
            s = '%s: ' % prompt
            k.setLabelBlue(s,protect=True)
            k.getArg(event,'replace-string',1,self.replaceString)
        elif state == 1:
            self._sString = k.arg
            s = '%s: %s With: ' % (prompt,self._sString)
            k.setLabelBlue(s,protect=True)
            k.getArg(event,'replace-string',2,self.replaceString)
        elif state == 2:
            k.clearState()
            self._rpString = k.arg ; w = self.widget
            #@        << do the replace >>
            #@+node:ekr.20050920084036.114:<< do the replace >>
            # g.es('%s %s by %s' % (prompt,repr(self._sString),repr(self._rpString)),color='blue')
            i = 'insert' ; end = 'end' ; count = 0
            if w.tag_ranges('sel'):
                i = w.index('sel.first')
                end = w.index('sel.last')
            if self._useRegex:
                txt = w.get(i,end)
                try:
                    pattern = re.compile(self._sString)
                except:
                    k.keyboardQuit(event)
                    k.setLabel("Illegal regular expression")
                    return
                count = len(pattern.findall(txt))
                if count:
                    ntxt = pattern.sub(self._rpString,txt)
                    w.delete(i,end)
                    w.insert(i,ntxt)
            else:
                # Problem: adds newline at end of text.
                txt = w.get(i,end)
                count = txt.count(self._sString)
                if count:
                    ntxt = txt.replace(self._sString,self._rpString)
                    w.delete(i,end)
                    w.insert(i,ntxt)
            #@nonl
            #@-node:ekr.20050920084036.114:<< do the replace >>
            #@nl
            k.setLabelGrey('Replaced %s occurance%s' % (count,g.choose(count==1,'','s')))
            self._useRegex = False
    #@nonl
    #@-node:ekr.20050920084036.113:replaceString
    #@+node:ekr.20050920084036.115:activateReplaceRegex
    def activateReplaceRegex( self ):
        
        '''This method turns regex replace on for replaceString'''
    
        self._useRegex = True
        return True
    #@nonl
    #@-node:ekr.20050920084036.115:activateReplaceRegex
    #@-node:ekr.20050920084036.112:replace...
    #@+node:ekr.20050920084036.116:scrollUp/Down
    def scrollDown (self,event):
    
        k = self.k ; w = event.widget
        chng = self.measure(w)
        i = w.index('insert')
        i1, i2 = i.split('.')
        i1 = int(i1) + chng [0]
        w.mark_set('insert','%s.%s' % (i1,i2))
        w.see('insert')
    
    def scrollUp (self,event):
    
        k = self.k ; w = event.widget
        chng = self.measure(w)
        i = w.index('insert')
        i1, i2 = i.split('.')
        i1 = int(i1) - chng [0]
        w.mark_set('insert','%s.%s' % (i1,i2))
        w.see('insert')
    #@nonl
    #@-node:ekr.20050920084036.116:scrollUp/Down
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
    def sortLines (self,event,which=None): # event IS used.
    
        k = self.k ; w = event.widget
        if not self._chckSel(event):
            return
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
#@+node:ekr.20050920084036.171:class keyHandlerCommandsClass
class keyHandlerCommandsClass (baseEditCommandsClass):
    
    '''User commands to access the keyHandler class.'''
    
    #@    @+others
    #@+node:ekr.20050920084036.172: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    #@nonl
    #@-node:ekr.20050920084036.172: ctor
    #@+node:ekr.20050920084036.173:getPublicCommands (for keyHandler)
    def getPublicCommands (self):
        
        k = self.k
        
        return {
            'digit-argument':           k.digitArgument,
            'help':                     k.help,
            'hide-mini-buffer':         k.hideMinibuffer,
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
            'show-mini-buffer':         k.showMinibuffer,
            'toggle-mini-buffer':       k.toggleMinibuffer,
            'universal-argument':       k.universalArgument,
        }
    #@nonl
    #@-node:ekr.20050920084036.173:getPublicCommands (for keyHandler)
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
            'kill-line':                self.killLine,
            'kill-word':                self.killWord,
            'kill-sentence':            self.killSentence,
            'kill-region':              self.killRegion,
            'kill-region-save':         self.killRegionSave, # Should this be kill-ring-save?
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
    
        if self.killBuffer and k.previousStroke in killKeys:
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
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        clip_text = self.getClipboard(w)
    
        if self.killBuffer or clip_text:
            self.reset = True
            if clip_text:   s = clip_text
            else:           s = self.kbiterator.next()
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
    #@+node:ekr.20050920084036.188:leoCommands.getPublicCommands (sets inversCommandDict & leoCallbackDict)
    def getPublicCommands (self):
        
        '''(leoCommands) Return a dict of the 'legacy' Leo commands.
        A special case used only by this class.
        Put the *raw* command name into the inverse dict, *not* 'leoCallback'.
        
        Also creates k.leoCallBackDict.  Keys are *raw* functions, values are emacs command names.'''
        
        k = self.k ; d2 = {}
        k.leoCallbackDict = {}
        
        #@    << define dictionary d of names and Leo commands >>
        #@+node:ekr.20050920084036.189:<< define dictionary d of names and Leo commands >>
        c = self.c ; f = c.frame
        
        d = {
            'abort-edit-headline':  f.abortEditLabelCommand,
            'about-leo':            c.about,
            'add-comments':         c.addComments,     
            'cascade-windows':      f.cascade,
            #'check-spelling':      None,                   # Create this command.
            'clear-recent-files':   c.clearRecentFiles,
            'close-window':         c.close,
            'contract-or-go-left':  c.contractNodeOrGoToParent,
            'check-python-code':    c.checkPythonCode,
            'check-all-python-code':c.checkAllPythonCode,
            'check-outline':        c.checkOutline,
            'clear-recent-files':   c.clearRecentFiles,
            'clone-node':           c.clone,
            'contract-node':        c.contractNode,
            'contract-all':         c.contractAllHeadlines,
            'contract-parent':      c.contractParent,
            'convert-all-blanks':   c.convertAllBlanks,
            'convert-all-tabs':     c.convertAllTabs,
            'convert-blanks':       c.convertBlanks,
            'convert-tabs':         c.convertTabs,
            'copy-node':            c.copyOutline,
            'copy-text':            f.copyText,
            'cut-node':             c.cutOutline,
            'cut-text':             f.cutText,
            'de-hoist':             c.dehoist,
            'delete':               c.delete,
            'delete-comments':      c.deleteComments,
            'delete-node':          c.deleteOutline,
            'delete-text':          c.delete,
            'demote':               c.demote,
            'dump-outline':         c.dumpOutline,
            'edit-headline':        c.editHeadline,
            'end-edit-headline':    f.endEditLabelCommand,
            'equal-sized-panes':    f.equalSizedPanes,
            'execute-script':       c.executeScript,
            'exit-leo':             g.app.onQuit,
            'expand-all':           c.expandAllHeadlines,
            'expand-next-level':    c.expandNextLevel,
            'expand-node':          c.expandNode,
            'expand-and-go-right':  c.expandNodeAndGoToFirstChild,
            'expand-or-go-right':   c.expandNodeOrGoToFirstChild,
            'expand-prev-level':    c.expandPrevLevel,
            'expand-to-level-1':    c.expandLevel1,
            'expand-to-level-2':    c.expandLevel2,
            'expand-to-level-3':    c.expandLevel3,
            'expand-to-level-4':    c.expandLevel4,
            'expand-to-level-5':    c.expandLevel5,
            'expand-to-level-6':    c.expandLevel6,
            'expand-to-level-7':    c.expandLevel7,
            'expand-to-level-8':    c.expandLevel8,
            'expand-to-level-9':    c.expandLevel9,
            'export-headlines':     c.exportHeadlines,
            'extract':              c.extract,
            'extract-names':        c.extractSectionNames,
            'extract-section':      c.extractSection,
            'flatten-outline':      c.flattenOutline,
            'go-back':              c.goPrevVisitedNode,
            'go-forward':           c.goNextVisitedNode,
            'goto-first-node':      c.goToFirstNode,
            'goto-first-sibling':   c.goToFirstSibling,
            'goto-last-node':       c.goToLastNode,
            'goto-last-sibling':    c.goToLastSibling,
            'goto-last-visible':    c.goToLastVisibleNode,
            'goto-line-number':     c.goToLineNumber,
            'goto-next-changed':    c.goToNextDirtyHeadline,
            'goto-next-clone':      c.goToNextClone,
            'goto-next-marked':     c.goToNextMarkedHeadline,
            'goto-next-node':       c.selectThreadNext,
            'goto-next-sibling':    c.goToNextSibling,
            'goto-next-visible':    c.selectVisNext,
            'goto-parent':          c.goToParent,
            'goto-prev-node':       c.selectThreadBack,
            'goto-prev-sibling':    c.goToPrevSibling,
            'goto-prev-visible':    c.selectVisBack,
            'hoist':                c.hoist,
            'import-at-file':       c.importAtFile,
            'import-at-root':       c.importAtRoot,
            'import-cweb-files':    c.importCWEBFiles,
            'import-derived-file':      c.importDerivedFile,
            'import-flattened-outline': c.importFlattenedOutline,
            'import-noweb-files':       c.importNowebFiles,
            'indent':                   c.indentBody,
            'insert-node':              c.insertHeadline,
            'insert-body-time':         c.insertBodyTime,
            'insert-headline-time':     f.insertHeadlineTime,
            # Leo find panel stuff.  It's not clear what will happen to these.
            'dismiss-leo-find-panel':   c.dismissFindPanel,
            'leo-change':               c.replace,
            'leo-change-then-find':     c.replaceThenFind,
            'leo-change-all':           c.replaceAll,
            'leo-find':                 c.findNext,
            'leo-find-panel':           c.showFindPanel,
            'leo-find-previous':        c.findPrevious,
            'mark':                     c.markHeadline,
            'mark-changed-items':       c.markChangedHeadlines,
            'mark-changed-roots':       c.markChangedRoots,
            'mark-clones':              c.markClones,
            'mark-subheads':            c.markSubheads,
            'match-bracket':            c.findMatchingBracket,
            'minimize-all':             f.minimizeAll,
            'move-outline-down':        c.moveOutlineDown,
            'move-outline-left':        c.moveOutlineLeft,
            'move-outline-right':       c.moveOutlineRight,
            'move-outline-up':          c.moveOutlineUp,
            'new':                      c.new,
            'open-compare-window':      c.openCompareWindow,
            'open-leoconfig-leo':       c.openLeoSettings,
            'open-leodocs-leo':         c.leoDocumentation,
            'open-leoplugins-leo':      c.openLeoPlugins,
            'open-online-home':         c.leoHome,
            'open-online-tutorial':     c.leoTutorial,
            'open-offline-tutorial':    f.leoHelp,
            'open-outline':             c.open,
            'open-python-window':       c.openPythonWindow,
            'open-with':                c.openWith,
            'outline-to-CWEB':          c.outlineToCWEB,
            'outline-to-noweb':         c.outlineToNoweb,
            'paste-node':               c.pasteOutline,
            'paste-retaining-clones':   c.pasteOutlineRetainingClones,
            'paste-text':               f.pasteText,
            'pretty-print-all-python-code': c.prettyPrintAllPythonCode,
            'pretty-print-python-code':     c.prettyPrintPythonCode,
            'promote':                  c.promote,
            'read-at-file-nodes':       c.readAtFileNodes,
            'read-outline-only':        c.readOutlineOnly,
            'redo':                     c.undoer.redo,
            'reformat-paragraph':       c.reformatParagraph,
            'remove-sentinels':         c.removeSentinels,
            'replace':                  c.replace,
            'replace-then-find':        c.replaceThenFind,
            'resize-to-screen':         f.resizeToScreen,
            'revert':                   c.revert,
            'save-file':                c.save,
            'save-file-as':             c.saveAs,
            'save-file-to':             c.saveTo,
            'select-all':               f.body.selectAllText,
            'settings':                 c.preferences,
            'set-colors':               c.colorPanel,
            'set-font':                 c.fontPanel,
            'show-invisibles':          c.viewAllCharacters,
            'sort-children':            c.sortChildren,
            'sort-siblings':            c.sortSiblings,
            'tangle':                   c.tangle,
            'tangle-all':               c.tangleAll,
            'tangle-marked':            c.tangleMarked,
            'toggle-active-pane':       f.toggleActivePane,
            'toggle-angle-brackets':    c.toggleAngleBrackets,
            'toggle-split-direction':   f.toggleSplitDirection,
            'undo':                     c.undoer.undo,
            'unindent':                 c.dedentBody,
            'unmark-all':               c.unmarkAll,
            'untangle':                 c.untangle,
            'untangle-all':             c.untangleAll,
            'untangle-marked':          c.untangleMarked,
            'weave':                    c.weave,
            'write-at-file-nodes':      c.fileCommands.writeAtFileNodes,
            'write-dirty-at-file-nodes':    c.fileCommands.writeDirtyAtFileNodes,
            'write-missing-at-file-nodes':  c.fileCommands.writeMissingAtFileNodes,
            'write-outline-only':       c.fileCommands.writeOutlineOnly,
        }
        #@nonl
        #@-node:ekr.20050920084036.189:<< define dictionary d of names and Leo commands >>
        #@nl
        
        # Create a callback for each item in d.
        keys = d.keys() ; keys.sort()
        for name in keys:
            f = d.get(name)
            # Warning: k.createInverseCommandsDict uses the name of this callback.
            def leoCallback (event,f=f,self=self,name=name):
                self.c.doCommand(f,name)
            d2 [name] = leoCallback
            k.leoCallbackDict [leoCallback] = f
            k.inverseCommandsDict [f.__name__] = name
            # g.trace('leoCommands %24s = %s' % (f.__name__,name))
            
        return d2
    #@nonl
    #@-node:ekr.20050920084036.188:leoCommands.getPublicCommands (sets inversCommandDict & leoCallbackDict)
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
            'call-last-keyboard-macro': self.callLastKeyboardMacro,
            'end-kbd-macro':            self.endKbdMacro,
            'name-last-kbd-macro':      self.nameLastKbdMacro,
            'load-file':                self.loadFile,
            'insert-keyboard-macro' :   self.insertKeyboardMacro,
            'start-kbd-macro':          self.startKbdMacro,
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
                b = k.bindingsDict.get(meth)  ### Probably should not strip < and >
                if b:
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
#@+node:ekr.20050920084036.207:class queryReplaceCommandsClass
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
        
        # self.qgetQuery = False
        # self.qgetReplace = False
        # self.qrexecute = False
    #@nonl
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
#@-node:ekr.20050920084036.207:class queryReplaceCommandsClass
#@+node:ekr.20050920084036.221:class rectangleCommandsClass
class rectangleCommandsClass (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.222: ctor & finishCreate
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.theKillRectangle = [] # Do not re-init this!
        
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
    def check (self,event,warning='No rectangle selected'):
        
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
    #@+node:ekr.20050920084036.224:Entries
    #@+node:ekr.20050920084036.231: enterRectangleState
    def enterRectangleState (self,event):
    
        k = self.k ; state = k.getState('rect-mode')
    
        if state == 0:
            k.setLabelBlue('quick-command r r: ')
            k.setState('rect-mode',1,self.enterRectangleState)
        else:
            ch = event.keysym
            k.clearState()
            k.resetLabel()
            data = self.commandsDict.get(ch)
            if data:
                k.commandName,func = data
                # g.trace(ch,func)
                func(event)
            else:
                k.setLabelGrey('Unknown rectangle command: %s' % repr(k.arg))
    #@nonl
    #@-node:ekr.20050920084036.231: enterRectangleState
    #@+node:ekr.20050920084036.225:clearRectangle
    def clearRectangle (self,event):
    
        if self.check(event):
            k = self.k ; w = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            lth = ' ' * (r4-r2)
            while r1 <= r3:
                w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                w.insert('%s.%s' % (r1,r2),lth)
                r1 = r1 + 1
    #@nonl
    #@-node:ekr.20050920084036.225:clearRectangle
    #@+node:ekr.20050920084036.226:closeRectangle
    def closeRectangle (self,event):
        
        '''Delete all whitespace following a specified column in each line.'''
    
        if self.check(event):
            k = self.k ; w = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            ar1 = r1
            txt = []
            while ar1 <= r3:
                txt.append(w.get('%s.%s' % (ar1,r2),'%s.%s' % (ar1,r4)))
                ar1 = ar1 + 1
            # for z in txt:
                # if z.strip():
                    # return
            while r1 <= r3:
                w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                r1 = r1 + 1
    #@nonl
    #@-node:ekr.20050920084036.226:closeRectangle
    #@+node:ekr.20050920084036.227:deleteRectangle
    def deleteRectangle (self,event):
    
        if self.check(event):
            k = self.k ; w = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            while r1 <= r3:
                w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                r1 = r1 + 1
    #@nonl
    #@-node:ekr.20050920084036.227:deleteRectangle
    #@+node:ekr.20050920084036.228:killRectangle
    def killRectangle (self,event):
    
        if self.check(event):
            k = self.k ; w = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            self.theKillRectangle = []
            while r1 <= r3:
                s = w.get('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                self.theKillRectangle.append(s)
                w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                r1 = r1 + 1
            if self.theKillRectangle:
                w.mark_set('sel.start','insert')
                w.mark_set('sel.end','insert')
    #@nonl
    #@-node:ekr.20050920084036.228:killRectangle
    #@+node:ekr.20050920084036.230:openRectangle
    def openRectangle (self,event):
        
        '''Insert blank space to fill the space of the region-rectangle.
        This pushes the previous contents of the region-rectangle rightward. '''
    
        if self.check(event):
            k = self.k ; w = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            lth = ' ' * (r4-r2)
            while r1 <= r3:
                w.insert('%s.%s' % (r1,r2),lth)
                r1 = r1 + 1
    #@nonl
    #@-node:ekr.20050920084036.230:openRectangle
    #@+node:ekr.20050920084036.229:yankRectangle
    def yankRectangle (self,event,killRect=None):
        
        k = self.k ; w = event.widget
        
        if not killRect: killRect = self.theKillRectangle
    
        if killRect:
            txt = w.get('insert linestart','insert')
            txt = self.getWSString(txt)
            i = w.index('insert')
            i1, i2 = i.split('.')
            i1 = int(i1)
            for z in killRect:
                txt2 = w.get('%s.0 linestart' % i1,'%s.%s' % (i1,i2))
                if len(txt2) != len(txt):
                    amount = len(txt) - len(txt2)
                    z = txt [ -amount:] + z
                w.insert('%s.%s' % (i1,i2),z)
                if w.index('%s.0 lineend +1c' % i1) == w.index('end'):
                    w.insert('%s.0 lineend' % i1,'\n')
                i1 = i1 + 1
        else:
            k.setLabelGrey('No kill rect')
    #@nonl
    #@-node:ekr.20050920084036.229:yankRectangle
    #@+node:ekr.20050920084036.232:stringRectangle
    def stringRectangle (self,event):
        
        '''Replace the contents of a region-rectangle with a string on each line.'''
    
        k = self.k ; state = k.getState('string-rect') ; 
        
        if state == 0:
            self.sRect = 1
            k.setLabelBlue('String rectangle: ',protect=True)
            k.getArg(event,'string-rect',1,k.stringRectangle)
        else:
            k.clearState()
            k.resetLabel()
            if self.check(event):
                w = event.widget
                r1, r2, r3, r4 = self.getRectanglePoints(event)
                while r1 <= r3:
                    w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                    w.insert('%s.%s' % (r1,r2),k.arg)
                    r1 = r1 + 1
    #@nonl
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
            'number-to-register':           self.numberToRegister,
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
            'n':        self.numberToRegister,
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
    #@+node:ekr.20051004123217:check
    def check (self,event,warning='No text selected'):
    
        return self._chckSel(event,warning)
    #@nonl
    #@-node:ekr.20051004123217:check
    #@+node:ekr.20050920084036.236:Entries...
    #@+node:ekr.20050920084036.238:appendToRegister
    def appendToRegister (self,event):
    
        k = self.k ; state = k.getState('append-to-reg')
        
        if state == 0:
            k.setLabelBlue('Append to register: ',protect=True)
            k.setState('append-to-reg',1,self.appendToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                w = event.widget
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
    #@nonl
    #@-node:ekr.20050920084036.238:appendToRegister
    #@+node:ekr.20050920084036.237:prependToRegister
    def prependToRegister (self,event):
        
        k = self.k ; state = k.getState('prepend-to-reg')
        
        if state == 0:
            k.setLabelBlue('Prepend to register: ',protect=True)
            k.setState('prepend-to-reg',1,self.prependToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                w = event.widget
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
    #@nonl
    #@-node:ekr.20050920084036.237:prependToRegister
    #@+node:ekr.20050920084036.239:copyRectangleToRegister
    def copyRectangleToRegister (self,event):
    
        k = self.k ; state = k.getState('copy-rect-to-reg')
    
        if state == 0:
            k.commandName = 'copy-rectangle-to-register'
            k.setLabelBlue('Copy Rectangle To Register: ',protect=True)
            k.setState('copy-rect-to-reg',1,self.copyRectangleToRegister)
        elif self.check(event,'No rectangle selected'):
            k.clearState()
            if event.keysym in string.letters:
                key = event.keysym.lower() ; w = event.widget
                r1, r2, r3, r4 = self.getRectanglePoints(event)
                rect = []
                while r1 <= r3:
                    txt = w.get('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                    rect.append(txt)
                    r1 = r1 + 1
                self.registers [key] = rect
                k.setLabelGrey('Register %s = %s' % (key,repr(rect)))
            else:
                k.setLabelGrey('Register must be a letter')
        else:
            k.clearState()
    #@nonl
    #@-node:ekr.20050920084036.239:copyRectangleToRegister
    #@+node:ekr.20050920084036.240:copyToRegister
    def copyToRegister (self,event):
        
        k = self.k ; state = k.getState('copy-to-reg')
        
        if state == 0:
            k.commandName = 'copy-to-register'
            k.setLabelBlue('Copy to register: ',protect=True)
            k.setState('copy-to-reg',1,self.copyToRegister)
        else:
            k.clearState()
            if self.check(event):
                if event.keysym in string.letters:
                    key = event.keysym.lower()
                    w = event.widget
                    try:
                        val = w.get('sel.first','sel.last')
                    except Exception:
                        val = ''
                    self.registers[key] = val
                    k.setLabelGrey('Register %s = %s' % (key,repr(val)))
                else:
                    k.setLabelGrey('Register must be a letter')
    #@nonl
    #@-node:ekr.20050920084036.240:copyToRegister
    #@+node:ekr.20050920084036.241:incrementRegister
    def incrementRegister (self,event):
        
        k = self.k ; state = k.getState('increment-reg')
        
        if state == 0:
            k.setLabelBlue('Increment register: ',protect=True)
            k.setState('increment-reg',1,self.incrementRegister)
        else:
            k.clearState()
            if self._checkIfRectangle(event):
                k.resetLabel()
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
    #@-node:ekr.20050920084036.241:incrementRegister
    #@+node:ekr.20050920084036.242:insertRegister
    def insertRegister (self,event):
        
        k = self.k ; c = k.c ; state = k.getState('insert-reg')
        
        if state == 0:
            k.commandName = 'insert-register'
            k.setLabelBlue('Insert register: ',protect=True)
            k.setState('insert-reg',1,self.insertRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                w = event.widget
                key = event.keysym.lower()
                val = self.registers.get(key)
                if val:
                    if type(val)==type([]):
                        c.rectangleCommands.yankRectangle(event,val)
                    else:
                        w.insert('insert',val)
                else:
                    k.setLabelGrey('Register %s is empty' % key)
            else:
                k.setLabelGrey('Register must be a letter')
    #@nonl
    #@-node:ekr.20050920084036.242:insertRegister
    #@+node:ekr.20050920084036.243:jumpToRegister
    def jumpToRegister (self,event):
    
        k = self.k ; state = k.getState('jump-to-reg')
    
        if state == 0:
            k.setLabelBlue('Jump to register: ',protect=True)
            k.setState('jump-to-reg',1,self.jumpToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                if self._checkIfRectangle(event): return
                key = event.keysym.lower()
                val = self.registers.get(key)
                if val:
                    try:
                        event.widget.mark_set('insert',val)
                        # event.widget.mark_set('insert.end',val)
                        k.setLabelGrey('At %s' % repr(val))
                    except Exception:
                        k.setLabelGrey('Register %s is not a valid location' % key)
                else:
                    k.setLabelGrey('Register %s is empty' % key)
            else:
                k.setLabelGrey('Register must be a letter')
    #@nonl
    #@-node:ekr.20050920084036.243:jumpToRegister
    #@+node:ekr.20050920084036.244:numberToRegister (not ready yet)
    #@+at
    # C-u number C-x r n reg
    #     Store number into register reg (number-to-register).
    # C-u number C-x r + reg
    #     Increment the number in register reg by number (increment-register). 
    # C-x r g reg
    #     Insert the number from register reg into the buffer.
    # 
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
    #@-node:ekr.20050920084036.244:numberToRegister (not ready yet)
    #@+node:ekr.20050920084036.245:pointToRegister
    def pointToRegister (self,event):
        
        k = self.k ; state = k.getState('point-to-reg')
        
        if state == 0:
            k.commandName = 'point-to-register'
            k.setLabelBlue('Point to register: ',protect=True)
            k.setState('point-to-reg',1,self.pointToRegister)
        else:
            k.clearState()
            if event.keysym in string.letters:
                w = event.widget
                key = event.keysym.lower()
                val = w.index('insert')
                self.registers[key] = val
                k.setLabelGrey('Register %s = %s' % (key,repr(val)))
            else:
                k.setLabelGrey('Register must be a letter')
    #@nonl
    #@-node:ekr.20050920084036.245:pointToRegister
    #@+node:ekr.20050920084036.246:viewRegister
    def viewRegister (self,event):
    
        k = self.k ; state = k.getState('view-reg')
        
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
    #@nonl
    #@-node:ekr.20050920084036.246:viewRegister
    #@-node:ekr.20050920084036.236:Entries...
    #@-others
#@nonl
#@-node:ekr.20050920084036.234:class registerCommandsClass
#@+node:ekr.20050920084036.257:class searchCommandsClass
class searchCommandsClass (baseEditCommandsClass):
    
    '''Implements many kinds of searches.'''

    #@    @+others
    #@+node:ekr.20050920084036.258: ctor
    def __init__ (self,c):
        
        # g.trace('searchCommandsClass')
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.findTabHandler = None
        
        self.forward = True
        self.regexp = False
    
        # For replace-string and replace-regexp
        self._sString = ''
        self._rpString = ''
    #@nonl
    #@-node:ekr.20050920084036.258: ctor
    #@+node:ekr.20050920084036.259:getPublicCommands (searchCommandsClass)
    def getPublicCommands (self):
        
        return {
            # The new find tab replaces the find dialog.
            'open-find-tab':            self.openFindTab,
            'find-tab-find':            self.findTabFindNext,
            'find-tab-find-prev':       self.findTabFindPrev,
    
            'isearch-forward':          self.isearchForward,
            'isearch-backward':         self.isearchBackward,
            'isearch-forward-regexp':   self.isearchForwardRegexp,
            'isearch-backward-regexp':  self.isearchBackwardRegexp,
            
            're-search-forward':        self.reSearchForward,
            're-search-backward':       self.reSearchBackward,
            
            'search-forward':           self.searchForward,
            'search-backward':          self.searchBackward,
            'word-search-forward':      self.wordSearchForward,
            'word-search-backward':     self.wordSearchBackward,
        }
    #@nonl
    #@-node:ekr.20050920084036.259:getPublicCommands (searchCommandsClass)
    #@+node:ekr.20051022211617:find tab...
    #@+node:ekr.20051020120306:openFindTab & helper classes
    def openFindTab (self,event):
    
        c = self.c ; log = c.frame.log ; tabName = 'Find'
    
        g.trace()
        if log.frameDict.get(tabName):
            log.selectTab(tabName)
        else:
            g.trace('creating findTabHandler')
            log.selectTab(tabName)
            f = log.frameDict.get(tabName)
            t = log.textDict.get(tabName)
            t.pack_forget()
            self.findTabHandler = self.leoTkinterFindTab(c,f)
    #@nonl
    #@+node:ekr.20051020120306.6:class leoTkinterFindTab (leoFind.leoFind)
    class leoTkinterFindTab (leoFind.leoFind):
    
        """A class that implements Leo's tkinter find tab."""
    
        #@    @+others
        #@+node:ekr.20051020120306.10:Birth & death
        #@+node:ekr.20051020120306.11:__init__
        def __init__(self,c,parentFrame):
        
            # Init the base class...
            leoFind.leoFind.__init__(self,c,title='Find Tab')
            self.c = c
            
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
            
            # These are created later.
            self.find_ctrl = None
            self.change_ctrl = None 
        
            self.createFrame(parentFrame)
            
            self.init(c) # New in 4.3: init only once.
        #@nonl
        #@-node:ekr.20051020120306.11:__init__
        #@+node:ekr.20051020120306.13:find.createFrame
        def createFrame (self,parentFrame):
            
            c = self.c
            
            #@    << Create the outer frames >>
            #@+node:ekr.20051020120306.14:<< Create the outer frames >>
            configName = 'log_pane_Find_tab_background_color'
            bg = c.config.getColor(configName) or 'MistyRose1'
            
            parentFrame.configure(background=bg)
            
            self.top = Tk.Frame(parentFrame,background=bg)
            self.frame = Tk.Frame(self.top,background=bg)
            outer = Tk.Frame(self.frame,background=bg)
            
            self.top.pack   (side='top',expand=0,fill='x',pady=5)
                # Don't expand, so the frame goes to the top.
            
            self.frame.pack (side="top",expand=1,fill='x')
            outer.pack      (side='top',expand=1,fill='x',padx=2,pady=2,)
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
            
            # Use bigger boxes for scripts.
            self.find_ctrl   = ftxt = Tk.Text(fpane,bd=1,relief="groove",height=3,width=15) # was height=4,width=20
            self.change_ctrl = ctxt = Tk.Text(cpane,bd=1,relief="groove",height=3,width=15) # was height=4,width=20
            #@<< Bind Tab and control-tab >>
            #@+node:ekr.20051020120306.16:<< Bind Tab and control-tab >>
            def setFocus(w):
                w.focus_set()
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
            
            flab.pack(side="left")
            clab.pack(side="left")
            ctxt.pack(side="right", expand=1, fill="x") 
            ftxt.pack(side="right", expand=1, fill="x")
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
                
            # HotKeys used for check/radio buttons:  a,b,c,e,h,i,l,m,n,o,p,r,s,t,w
            
            radioLists[0] = [
                #(self.dict["radio-find-type"],"P&Lain Search","plain-search"),  
                #(self.dict["radio-find-type"],"&Pattern Match Search","pattern-search"),
                # (self.dict["radio-find-type"],"&Script Search","script-search"),
            ]
            checkLists[0] = [
                # ("Scrip&t Change",self.dict["script_change"]),
                ("Whole Word",      self.dict["whole_word"]),
                ("Ignore Case",     self.dict["ignore_case"]),
                ("Wrap Around",     self.dict["wrap"]),
                ("Reverse",         self.dict["reverse"]),
                ('Regexp',          self.dict["radio-find-type"]=='pattern-search'),
                ("Search Headline", self.dict["search_headline"]),
                ("Search Body",     self.dict["search_body"]),
            ]
            
            radioLists[1] = [
                (self.dict["radio-search-scope"],"&Entire Outline","entire-outine"),
                (self.dict["radio-search-scope"],"Suboutline &Only","suboutline-only"),  
                (self.dict["radio-search-scope"],"&Node Only","node-only"),
                # I don't know what selection-only is supposed to do.
                (self.dict["radio-search-scope"],"Selection Only",None), #,"selection-only")
            ]
            checkLists[1] = [
                ("&Mark Finds",           self.dict["mark_finds"]),
                ("Mark &Changes",         self.dict["mark_changes"]),
                ('Show Context',          self.dict['batch']),
            ]
            
            for i in xrange(numberOfColumns):
                for var,name,val in radioLists[i]:
                    box = self.underlinedTkButton(
                        "radio",columns[i],anchor="w",text=name,variable=var,value=val,background=bg)
                    box.button.pack(fill="x")
                    box.button.bind("<1>", self.resetWrap)
                    if val == None: box.button.configure(state="disabled")
                    box.bindHotKey(ftxt)
                    box.bindHotKey(ctxt)
                for name,var in checkLists[i]:
                    box = self.underlinedTkButton(
                        "check",columns[i],anchor="w",text=name,variable=var,background=bg)
                    box.button.pack(fill="x")
                    box.button.bind("<1>", self.resetWrap)
                    box.bindHotKey(ftxt)
                    box.bindHotKey(ctxt)
                    if var is None: box.button.configure(state="disabled")
            #@nonl
            #@-node:ekr.20051020120306.17:<< Create two columns of radio and checkboxes >>
            #@nl
            #@    << Create two columns of buttons >>
            #@+node:ekr.20051020120306.18:<< Create two columns of buttons >>
            # Create the alignment panes.
            buttons  = Tk.Frame(outer,background=bg)
            buttons1 = Tk.Frame(buttons,bd=1,background=bg)
            buttons2 = Tk.Frame(buttons,bd=1,background=bg)
            buttons.pack(side='top',expand=1)
            buttons1.pack(side='left')
            buttons2.pack(side='right')
            
            def findButtonCallback(event=None):
                __pychecker__ = '--no-argsused'
                self.findButton()
                return 'break'
                    
            width = 15 ; defaultText = 'Find' ; buttons = []
            
            for text,boxKind,frame,callback in (
                # Column 1...
                ('Find','button',buttons1,findButtonCallback),
                ('Incremental','check', buttons1,None),
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
            
            for w in buttons:
                w.bindHotKey(ftxt)
                w.bindHotKey(ctxt)
            
            for w in (self.find_ctrl, self.change_ctrl):
                w.bind ("<1>",  self.resetWrap)
                w.bind("<Key>", self.resetWrap)
                w.bind("<Control-a>",self.selectAllFindText)
            
            for w in (outer, self.find_ctrl, self.change_ctrl):
                w.bind("<Key-Return>", findButtonCallback)
                w.bind("<Key-Escape>", self.onCloseWindow)
        #@nonl
        #@-node:ekr.20051020120306.13:find.createFrame
        #@+node:ekr.20051020120306.19:find.init
        def init (self,c):
        
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
                ("selection_only","selection-only")): # 11/9/03
                val = self.dict[var].get()
                if val:
                    self.dict["radio-search-scope"].set(setting)
                    found = True ; break
            if not found:
                self.dict["radio-search-scope"].set("entire-outine")
            #@nonl
            #@-node:ekr.20051020120306.21:<< set radio buttons from ivars >>
            #@nl
        #@nonl
        #@-node:ekr.20051020120306.19:find.init
        #@-node:ekr.20051020120306.10:Birth & death
        #@+node:ekr.20051020120306.22:find.update_ivars
        def update_ivars (self):
            
            """Called just before doing a find to update ivars from the find panel."""
        
            for key in self.intKeys:
                val = self.dict[key].get()
                setattr(self, key, val) # No more _flag hack.
                # g.trace(key,val)
        
            # Set ivars from radio buttons. Convert these to 1 or 0.
            find_type = self.dict["radio-find-type"].get()
            self.pattern_match = g.choose(find_type == "pattern-search",1,0)
            self.script_search = g.choose(find_type == "script-search",1,0)
        
            search_scope = self.dict["radio-search-scope"].get()
            self.suboutline_only = g.choose(search_scope == "suboutline-only",1,0)
            self.node_only       = g.choose(search_scope == "node-only",1,0)
            self.selection       = g.choose(search_scope == "selection-only",1,0) # 11/9/03
        
            # New in 4.3: The caller is responsible for removing most trailing cruft.
            # Among other things, this allows Leo to search for a single trailing space.
            s = self.find_ctrl.get("1.0","end")
            s = g.toUnicode(s,g.app.tkEncoding)
            # g.trace(repr(s))
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
        #@+node:ekr.20051020120306.23:tkFind.adjust_find_text
        def adjust_find_text(self,s):
            
            w = self.find_ctrl
            
            w.delete("1.0","end")
            w.insert("end",s)
        #@nonl
        #@-node:ekr.20051020120306.23:tkFind.adjust_find_text
        #@+node:ekr.20051020120306.24:onCloseWindow
        def onCloseWindow(self,event=None):
            
            __pychecker__ = '--no-argsused' # the event param must be present.
        
            self.top.withdraw()
        #@nonl
        #@-node:ekr.20051020120306.24:onCloseWindow
        #@+node:ekr.20051020120306.25:dismiss
        def dismiss (self):
            
            self.top.withdraw()
        #@nonl
        #@-node:ekr.20051020120306.25:dismiss
        #@+node:ekr.20051020120306.26:bringToFront
        def bringToFront (self):
            
            """Bring the tkinter Find Panel to the front."""
            
            c = self.c ; t = self.find_ctrl ; gui = g.app.gui
                    
            self.top.withdraw() # Helps bring the window to the front.
            self.top.deiconify()
            self.top.lift()
        
            gui.set_focus(c,t,tag='bringToFront')
            
            # Apparently, the text can not be adjusted unless the widget has focus...
            s = t.get('1.0','end')
            if s and s[-1] in ('\n','\r'):
                t.delete('end-1c','end')
        
            # New in 4.3: don't highlight the stupid added trailing newline!
            gui.setTextSelection (t,"1.0","end-1c") # Thanks Rich.
            
            def setFocusCallback():
                # g.trace()
                gui.set_focus(c,t,tag='tkFind.bringToFront')
            
            # We must do this after other callbacks.  Sheesh.
            self.top.after(500,setFocusCallback)
        #@-node:ekr.20051020120306.26:bringToFront
        #@+node:ekr.20051020120306.27:selectAllFindText
        def selectAllFindText (self,event=None):
            
            __pychecker__ = '--no-argsused' # the event param must be present.
        
            try:
                w = self.frame.focus_get()
                g.app.gui.setTextSelection(w,"1.0","end")
                return "break"
            except:
                return None # To keep pychecker happy.
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
    #@-node:ekr.20051020120306.6:class leoTkinterFindTab (leoFind.leoFind)
    #@-node:ekr.20051020120306:openFindTab & helper classes
    #@+node:ekr.20051022212004:findTabFindNext/Pref
    def findTabFindNext (self,event):
        
        c = self.c
        self.openFindTab()
        self.findTabHandler.setup_command(c)
        self.findTabHandler.findNext()
        
    def findTabFindPrev (self,event):
        
        c = self.c
        self.openFindTab()
        self.findTabHandler.setup_command(c)
        self.findTabHandler.findPrev()
    #@nonl
    #@-node:ekr.20051022212004:findTabFindNext/Pref
    #@-node:ekr.20051022211617:find tab...
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
    
        k = self.k
        
        self.forward = forward
        self.regexp = regexp
        k.setLabelBlue('isearch: ',protect=True)
        k.setState('isearch',1,handler=self.iSearchStateHandler)
    #@nonl
    #@-node:ekr.20050920084036.262:startIncremental
    #@+node:ekr.20050920084036.264:iSearchStateHandler & helper
    # Called when from the state manager when the state is 'isearch'
    
    def iSearchStateHandler (self,event):
    
        k = self.k ; w = event.widget ; keysym = event.keysym
        if keysym == 'Control_L': return
        
        g.trace('keysym',keysym,'stroke',k.stroke)
        
        if 0: # Useful, but presently conflicts with other bindings.
            if k.stroke == '<Control-s>':
                self.startIncremental(event,forward=True,regexp=False)
            elif k.stroke == '<Control-r>':
                self.startIncremental(event,forward=False,regexp=False)
    
        if keysym == 'Return':
            if 0: # Doesn't do anything at present.
                #@            << do a non-incremental search >>
                #@+node:ekr.20051002120125:<< do a non-incremental search >>
                s = k.getLabel(ignorePrompt=True)
                
                if s:
                    if self.forward:
                        if self.regexp: self.reSearchForward(event)
                        else:           self.searchForward(event)
                    else:
                        if self.regexp: self.reSearchBackward(event)
                        else:           self.searchBackward(event)
                #@nonl
                #@-node:ekr.20051002120125:<< do a non-incremental search >>
                #@nl
            k.resetLabel()
            k.clearState()
            return
    
        if event.char == '\b':
            g.trace('backspace not handled yet')
            return
        
        if event.char:
            k.updateLabel(event)
            s = k.getLabel(ignorePrompt=True)
            z = w.search(s,'insert',stopindex='insert +%sc' % len(s))
            if not z:
               self.iSearchHelper(event,self.forward,self.regexp)
            self.scolorizer(event)
    #@nonl
    #@+node:ekr.20050920084036.263:iSearchHelper
    def iSearchHelper (self,event,forward,regexp):
    
        '''This method moves the insert spot to position that matches the pattern in the miniBuffer'''
        
        k = self.k ; w = event.widget
        s = k.getLabel(ignorePrompt=True)
        g.trace(forward,repr(s))
        if s:
            try:
                if forward:
                    i = w.search(s,"insert + 1c",stopindex='end',regexp=regexp)
                    if not i:
                        # Start again at the top of the buffer.
                        i = w.search(s,'1.0',stopindex='insert',regexp=regexp)
                else:
                    i = w.search(s,'insert',backwards=True,stopindex='1.0',regexp=regexp)
                    if not i:
                        # Start again at the bottom of the buffer.
                        i = w.search(s,'end',backwards=True,stopindex='insert',regexp=regexp)
                
            except: pass
    
            if i and not i.isspace():
                w.mark_set('insert',i)
                w.see('insert')
    #@nonl
    #@-node:ekr.20050920084036.263:iSearchHelper
    #@-node:ekr.20050920084036.264:iSearchStateHandler & helper
    #@+node:ekr.20050920084036.265:scolorizer
    def scolorizer (self,event):
    
        k = self.k ; w = event.widget
    
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
    #@-node:ekr.20050920084036.261:incremental search...
    #@+node:ekr.20050920084036.267:non-incremental search...
    #@+node:ekr.20050920084036.269:seachForward/Backward & helper
    def searchBackward (self,event):
    
        k = self.k ; state = k.getState('search-backward')
        if state == 0:
            k.setLabelBlue('Search Backward: ',protect=True)
            k.getArg(event,'search-backward',1,self.searchBackward)
        else:
            k.clearState()
            k.resetLabel()
            self.plainSearchHelper(event,k.arg,forward=False)
    
    def searchForward (self,event):
    
        k = self.k ; state = k.getState('search-forward')
        if state == 0:
            k.setLabelBlue('Search: ',protect=True)
            k.getArg(event,'search-forward',1,self.searchForward)
        else:
            k.clearState()
            k.resetLabel()
            self.plainSearchHelper(event,k.arg,forward=True)
    #@nonl
    #@+node:ekr.20050920084036.268:plainSearchHelper
    def plainSearchHelper (self,event,pattern,forward):
    
        k = self.k ; w = event.widget ; i = w.index('insert')
    
        try:
            if forward:
                s = w.search(pattern,i,stopindex='end')
                if s: s = w.index('%s +%sc' % (s,len(pattern)))
            else:
                s = w.search(pattern,i,stopindex='1.0',backwards=True)
        except Exception:
            return
    
        if s:
            w.mark_set('insert',s)
    #@nonl
    #@-node:ekr.20050920084036.268:plainSearchHelper
    #@-node:ekr.20050920084036.269:seachForward/Backward & helper
    #@+node:ekr.20051002111614:wordSearchBackward/Forward & helper
    def wordSearchBackward (self,event):
    
        k = self.k ; state = k.getState('word-search-backward')
        if state == 0:
            k.setLabelBlue('Word Search Backward: ',protect=True)
            k.getArg(event,'word-search-backward',1,self.wordSearchBackward)
        else:
            k.clearState()
            k.resetLabel()
            self.wordSearchHelper(event,k.arg,forward=False)
    
    def wordSearchForward (self,event):
    
        k = self.k ; state = k.getState('word-search-forward')
        if state == 0:
            k.setLabelBlue('Word Search: ',protect=True)
            k.getArg(event,'word-search-forward',1,self.wordSearchForward)
        else:
            k.clearState()
            k.resetLabel()
            self.wordSearchHelper(event,k.arg,forward=True)
    #@nonl
    #@+node:ekr.20050920084036.272:wordSearchHelper
    def wordSearchHelper (self,event,pattern,forward):
    
        k = self.k ; w = event.widget ; i = w.index('insert')
        words = pattern.split()
        sep = '[%s%s]+' % (string.punctuation,string.whitespace)
        pattern = sep.join(words)
        cpattern = re.compile(pattern)
        if forward:
            txt = w.get('insert','end')
            match = cpattern.search(txt)
            if not match: return
            end = match.end()
        else:
            txt = w.get('1.0','insert') #initially the reverse words formula for Python Cookbook was going to be used.
            a = re.split(pattern,txt) #that didnt quite work right.  This one apparently does.
            if len(a) > 1:
                b = re.findall(pattern,txt)
                end = len(a[-1]) + len(b[-1])
            else: return
            
        s = g.choose(forward,'insert +%sc','insert -%sc')
        w.mark_set('insert',s % end)
        w.see('insert')
    #@-node:ekr.20050920084036.272:wordSearchHelper
    #@-node:ekr.20051002111614:wordSearchBackward/Forward & helper
    #@+node:ekr.20050920084036.274:reSearchBackward/Forward & helper
    def reSearchBackward (self,event):
    
        k = self.k ; state = k.getState('re-search-backward')
        if state == 0:
            k.setLabelBlue('Regexp Search backward:',protect=True)
            k.getArg(event,'re-search-backward',1,self.reSearchBackward)
        else:
            k.clearState()
            k.resetLabel()
            self.reSearchHelper(event,k.arg,forward=False)
    
    def reSearchForward (self,event):
    
        k = self.k ; state = k.getState('re-search-forward')
        if state == 0:
            k.setLabelBlue('Regexp Search:',protect=True)
            k.getArg(event,'re-search-forward',1,self.reSearchForward)
        else:
            k.clearState()
            k.resetLabel()
            self.reSearchHelper(event,k.arg,forward=True)
    #@nonl
    #@+node:ekr.20050920084036.275:reSearchHelper
    def reSearchHelper (self,event,pattern,forward):
    
        k = self.k ; w = event.widget
        cpattern = re.compile(pattern)
    
        if forward:
            txt = w.get('insert','end')
            match = cpattern.search(txt)
            end = match.end()
        else:
            # The reverse words formula for Python Cookbook didn't quite work.
            txt = w.get('1.0','insert') 
            a = re.split(pattern,txt)
            if len(a) > 1:
                b = re.findall(pattern,txt)
                end = len(a[-1]) + len(b[-1])
            else: return
    
        if end:
            s = g.choose(forward,'insert +%sc','insert -%sc')
            w.mark_set('insert',s % end)
            w.see('insert')
    #@nonl
    #@-node:ekr.20050920084036.275:reSearchHelper
    #@-node:ekr.20050920084036.274:reSearchBackward/Forward & helper
    #@-node:ekr.20050920084036.267:non-incremental search...
    #@-others
#@nonl
#@-node:ekr.20050920084036.257:class searchCommandsClass
#@-others

#@<< define classesList >>
#@+node:ekr.20050922104213:<< define classesList >>
classesList = [
    ('abbrevCommands',      abbrevCommandsClass),
    ('bufferCommands',      bufferCommandsClass),
    ('editCommands',        editCommandsClass),
    ('controlCommands',     controlCommandsClass),
    ('editFileCommands',    editFileCommandsClass),
    ('keyHandlerCommands',  keyHandlerCommandsClass),
    ('killBufferCommands',  killBufferCommandsClass),
    ('leoCommands',         leoCommandsClass),
    ('macroCommands',       macroCommandsClass),
    ('queryReplaceCommands',queryReplaceCommandsClass),
    ('rectangleCommands',   rectangleCommandsClass),
    ('registerCommands',    registerCommandsClass),
    ('searchCommands',      searchCommandsClass),
]
#@nonl
#@-node:ekr.20050922104213:<< define classesList >>
#@nl
#@nonl
#@-node:ekr.20050710142719:@thin leoEditCommands.py
#@-leo
