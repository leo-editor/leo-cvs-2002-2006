#@+leo-ver=4-thin
#@+node:ekr.20050710142719:@thin leoEditCommands.py
'''Basic editor commands for Leo.

Modelled after Emacs and Vim commands.'''

#@<< imports >>
#@+node:ekr.20050710151017:<< imports >>
import leoGlobals as g

import leoKeys
import leoPlugins

import cPickle
import difflib
import os
import re
import string
subprocess = g.importExtension('subprocess',pluginName=None,verbose=False)
import sys
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
        
    def finishCreate(self):
    
        # Class delegators.
        self.k = self.keyHandler = self.c.keyHandler
        
    def init (self):
        
        '''Called from k.stopControlX to init all classes.'''
        
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
    #@+node:ekr.20050920084036.8:range utilities
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
    #@+node:ekr.20050920084036.11:testinrange
    def testinrange (self,w):
    
        if not self.inRange(w,'sel') or not self.contRanges(w,'sel'):
            self.removeRKeys(w)
            return False
        else:
            return True
    #@nonl
    #@-node:ekr.20050920084036.11:testinrange
    #@-node:ekr.20050920084036.8:range utilities
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
    #@-others
#@nonl
#@-node:ekr.20050920084036.1:<< define class baseEditCommandsClass >>
#@nl

#@+others
#@+node:ekr.20050924100713: Module level...
#@+node:ekr.20050920084720:createEditCommanders (leoEditCommands module)
def createEditCommanders (self):
    
    '''Create edit classes in the commander.'''
    
    c = self ; global classesList
    
    d = {}

    for name, theClass in classesList:
        theInstance = theClass(c)# Create the class.
        setattr(c,name,theInstance)
        # g.trace(name,theInstance)
        d2 = theInstance.getPublicCommands()
        if d2:
            d.update(d2)
            if 0:
                keys = d2.keys()
                keys.sort()
                print '----- %s' % name
                for key in keys: print key
                
    return d
#@nonl
#@-node:ekr.20050920084720:createEditCommanders (leoEditCommands module)
#@+node:ekr.20050922104731:finishCreateEditCommanders (leoEditCommands module)
def finishCreateEditCommanders (c):
    
    '''Create edit classes in the commander.'''
    
    global classesList

    for name, theClass in classesList:
        theInstance = getattr(c,name)
        theInstance.finishCreate()
        theInstance.init()
#@nonl
#@-node:ekr.20050922104731:finishCreateEditCommanders (leoEditCommands module)
#@+node:ekr.20050924100713.1:initAllEditCommanders
def initAllEditCommanders (self):
    
    '''Re-init classes in the commander.'''
    
    c = self ; global classesList

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
    
        # Set ivars in emacs.
        self.keyHandler.abbrevMode = False 
        self.keyHandler.abbrevOn = False # determines if abbreviations are on for masterCommand and toggle abbreviations.
    #@nonl
    #@-node:ekr.20050920084036.14: ctor & finishCreate
    #@+node:ekr.20050920084036.15: getPublicCommands & getStateCommands
    def getPublicCommands (self):
        
        return {
            'abbrev-mode':              self.toggleAbbrevMode,
            'expand-abbrev':            self.expandAbbrev,
            'expand-region-abbrevs':    self.regionalExpandAbbrev,
            'kill-all-abbrevs':         self.killAllAbbrevs,
            'list-abbrevs':             self.listAbbrevs,
            'read-abbrev-file':         self.readAbbreviations,
            'write-abbrev-file':        self.writeAbbreviations,
        }
    #@nonl
    #@-node:ekr.20050920084036.15: getPublicCommands & getStateCommands
    #@+node:ekr.20050920084036.16: Entry points
    #@+node:ekr.20050920084036.17:expandAbbrev
    def expandAbbrev (self,event):
        
        k = self.k
    
        return k.keyboardQuit(event) and self._expandAbbrev(event)
    
    #@-node:ekr.20050920084036.17:expandAbbrev
    #@+node:ekr.20050920084036.18:killAllAbbrevs
    def killAllAbbrevs (self,event):
    
        k = self.k
        self.abbrevs = {}
        return k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20050920084036.18:killAllAbbrevs
    #@+node:ekr.20050920084036.19:listAbbrevs
    def listAbbrevs (self,event):
    
        k = self.k
        txt = ''
        for z in self.abbrevs:
            txt = '%s%s=%s\n' % (txt,z,self.abbrevs[z])
        k.setLabel(txt)
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.19:listAbbrevs
    #@+node:ekr.20050920084036.20:readAbbreviations
    def readAbbreviations (self,event):
    
        f = tkFileDialog.askopenfile()
        if f == None:
            return 'break'
        else:
            return self._readAbbrevs(f)
    #@nonl
    #@-node:ekr.20050920084036.20:readAbbreviations
    #@+node:ekr.20050920084036.21:regionalExpandAbbrev
    def regionalExpandAbbrev( self, event ):
        
        if not self._chckSel( event ):
            return
        
        k = self.k
        w = event.widget
        i1 = w.index( 'sel.first' )
        i2 = w.index( 'sel.last' ) 
        ins = w.index( 'insert' )
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
                        if self.regXKey == 'y':
                            ind = w.index('%s wordstart' % i1)
                            w.delete('%s wordstart' % i1,'%s wordend' % i1)
                            w.insert(ind,self.abbrevs[word])
                    i1 = '%s wordend' % i1
            w.mark_set('insert',ins)
            w.selection_clear()
            w.tag_delete('sXR')
            w.tag_delete('found')
            k.setLabelGrey('')
            self._setRAvars()
        #@-node:ekr.20050920084036.22:<< define a new generator searchXR >>
        #@nl
        # EKR: the 'result' of calling searchXR is a generator object.
        k.regx.iter = searchXR( i1, i2, ins, event)
        k.regx.iter.next() # Call it the first time.
        return 'break'
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
    
        f = tkFileDialog.asksaveasfile()
        if f == None:
            return 'break'
        else:
            return self._writeAbbrevs(f)
    #@nonl
    #@-node:ekr.20050920084036.24:writeAbbreviations
    #@-node:ekr.20050920084036.16: Entry points
    #@+node:ekr.20050920084036.25:abbreviationDispatch (Probably wrong)
    def abbreviationDispatch (self,event,which):
        
        k = self.k
        state = k.getState('abbrevMode')
    
        if state == 0:
            k.setState('abbrevMode',which,handler=self.abbrevCommand1)
            k.setLabelBlue('')
        else:
            self.abbrevCommand1(event)
            
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.25:abbreviationDispatch (Probably wrong)
    #@+node:ekr.20050920084036.26:abbrevCommand1
    def abbrevCommand1 (self,event):
    
        k = self.k ; w = event.widget
    
        if event.keysym == 'Return':
            word = w.get('insert -1c wordstart','insert -1c wordend')
            if word == ' ': return
            state = k.getState('abbrevMode')
            if state == 1:
                self.abbrevs [k.getLabel()] = word
            elif state == 2:
                self.abbrevs [word] = k.getLabel()
            k.keyboardQuit(event)
            k.resetLabel()
        else:
            k.updateLabel(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.26:abbrevCommand1
    #@+node:ekr.20050920084036.27:_expandAbbrev
    def _expandAbbrev (self,event):
    
        k = self.k ; w = event.widget 
        
        word = w.get('insert -1c wordstart','insert -1c wordend')
        ch = event.char.strip()
    
        if ch:
            # We must do this: expandAbbrev is called from Alt-x and Control-x,
            # we get two differnt types of data and w states.
            word = '%s%s'% (word,event.char)
            
        if self.abbrevs.has_key(word):
            w.delete('insert -1c wordstart','insert -1c wordend')
            w.insert('insert',self.abbrevs[word])
            return k._tailEnd(w)
        else:
            return False 
    
    
    #@-node:ekr.20050920084036.27:_expandAbbrev
    #@+node:ekr.20050920084036.28:_setRAvars
    def _setRAvars( self ):
    
        self.k.regx.iter = self.k.regXKey = None
    #@nonl
    #@-node:ekr.20050920084036.28:_setRAvars
    #@+node:ekr.20050920084036.29:_readAbbrevs
    def _readAbbrevs (self,f):
    
        for x in f:
            a, b = x.split('=')
            b = b[:-1]
            self.abbrevs[a] = b 
        f.close()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.29:_readAbbrevs
    #@+node:ekr.20050920084036.30:_writeAbbrevs
    def _writeAbbrevs( self, f ):
    
        for x in self.abbrevs:
            f.write( '%s=%s\n' %( x, self.abbrevs[ x ] ) )
        f.close()
     
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.30:_writeAbbrevs
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

class bufferCommandsClass  (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.32: ctor (bufferCommandsClass)
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.fromName = '' # Saved name from getBufferName.
    #@nonl
    #@-node:ekr.20050920084036.32: ctor (bufferCommandsClass)
    #@+node:ekr.20050920084036.33: getPublicCommands
    def getPublicCommands (self):
    
        return {
            'append-to-buffer':     self.appendToBuffer,
            'copy-to-buffer':       self.copyToBuffer,
            'insert-to-buffer':       self.insertToBuffer,
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
        self.getBufferName(self.appendToBufferFinisher)
        return 'break'
    
    def appendToBufferFinisher (self,name):
    
        txt = w.get('sel.first','sel.last')
        try:
            bdata = self.bufferDict [name]
            bdata = '%s%s' % (bdata,txt)
            self.setBufferData(event,name,bdata)
        except Exception:
            pass
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.35:appendToBuffer/Finisher
    #@+node:ekr.20050920084036.36:copyToBuffer/Finisher
    def copyToBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Copy to buffer: ')
        self.getBufferName(self.copyToBufferFinisher)
        return 'break'
    
    def copyToBufferFinisher (self,name):
    
        try:
            txt = w.get('sel.first','sel.last')
            self.setBufferData(event,name,txt)
        except Exception:
            pass
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.36:copyToBuffer/Finisher
    #@+node:ekr.20050920084036.37:insertToBuffer/Finisher
    def insertToBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Insert to buffer: ')
        self.getBufferName(self.insertToBufferFinisher)
        return 'break'
    
    def insertToBufferFinisher (self,name):
    
        try:
            bdata = self.bufferDict [name]
            w.insert('insert',bdata)
            k._tailEnd(w)
        except Exception:
            pass
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.37:insertToBuffer/Finisher
    #@+node:ekr.20050920084036.38:killBuffer/Finisher  (not ready yet)
    def killBuffer (self,event):
    
        k = self.k
        k.setLabelBlue('Kill buffer: ')
        self.getBufferName(self.killBufferFinisher)
        return 'break'
    
    def killBufferFinisher (self,name):
    
        # method = self.bufferDeletes[event.widget]
        # method(name)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.38:killBuffer/Finisher  (not ready yet)
    #@+node:ekr.20050920084036.39:prependToBuffer/Finisher
    def prependToBuffer (self,event):
        
        k = self.k
        k.setLabelBlue('Prepend to buffer: ')
        self.getBufferName(self.prependToBufferFinisher)
        return 'break'
        
    def prependToBufferFinisher (self,name):
        
        try:
            txt = w.get('sel.first','sel.last')
            bdata = self.bufferDict[name]
            bdata = '%s%s'%(txt,bdata)
            self.setBufferData(event,name,bdata)
        except Exception:
            pass
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.39:prependToBuffer/Finisher
    #@+node:ekr.20050920084036.40:switchToBuffer (not ready yet)
    def switchToBuffer (self,event):
        
        k = self.k
        k.setLabelBlue('Switch to buffer: ')
        self.getBufferName(self.switchToBufferFinisher)
        return 'break'
        
    def switchToBufferFinisher (self,name):
     
        # method = self.bufferGotos[event.widget]
        # k.keyboardQuit(event)
        # method(name)
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.40:switchToBuffer (not ready yet)
    #@+node:ekr.20050920084036.42:listBuffers/Finisher
    def listBuffers (self,event):
        
        k = self.k
        bdict = self.getBufferDict(event)
        list = bdict.keys()
        list.sort()
        data = '\n'.join(list)
        k.keyboardQuit(event)
        k.setLabel(data)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.42:listBuffers/Finisher
    #@+node:ekr.20050920084036.43:renameBuffer (not ready yet)
    def renameBuffer (self,event):
        
        k = self.k
        k.setLabelBlue('Rename buffer from: ')
        self.getBufferName(self.renameBufferFinisher1)
        return 'break'
        
    def renameBufferFinisher1 (self,name):
        
        k = self.k
        k.setLabelBlue('Rename buffer from: %s to: ' % (name))
        self.fromName = name
        self.getBufferName(self.renameBufferFinisher2)
        return 'break'
        
    def renameBufferFinisher2 (self,name):
    
        k = self.k
        # self.renameBuffers[w](name)
        k.setLabelGrey('Renamed buffer %s to %s' % (self.fromName,name))
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.43:renameBuffer (not ready yet)
    #@-node:ekr.20050920084036.34:Entry points 
    #@+node:ekr.20050927093851:getBufferName
    def getBufferName (self,func=None):
        
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
            k.getArg(None,'getBufferName',1,self.getBufferName,prefix=prefix,tabList=tabList)
        else:
            k.resetLabel()
            k.clearState()
            # g.trace(repr(k.arg))
            func = self.getBufferNameFinisher
            self.getBufferNameFinisher = None
            if func:
                func(k.arg)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050927093851:getBufferName
    #@+node:ekr.20050927102133.1:Utils
    #@+node:ekr.20050927101829.3:setBufferData
    def setBufferData (name,data):
    
        data = unicode(data)
        tdict = self.tnodes [c]
        if tdict.has_key(name):
            tdict [name].bodyString = data
    #@nonl
    #@-node:ekr.20050927101829.3:setBufferData
    #@+node:ekr.20050927101829.4:gotoNode
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
    #@-node:ekr.20050927101829.4:gotoNode
    #@+node:ekr.20050927101829.5:gotoPosition
    def gotoPosition (c,pos):
    
        c.frame.tree.expandAllAncestors(pos)
        c.selectPosition(pos)
    #@nonl
    #@-node:ekr.20050927101829.5:gotoPosition
    #@+node:ekr.20050927101829.6:deleteNode
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
    #@-node:ekr.20050927101829.6:deleteNode
    #@+node:ekr.20050927101829.7:renameNode
    def renameNode (name):
    
        c.beginUpdate()
        try:
            pos = c.currentPosition()
            pos.setHeadString(name)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20050927101829.7:renameNode
    #@-node:ekr.20050927102133.1:Utils
    #@+node:ekr.20050927101829.2:buildBufferList (not used)
    def buildBufferList (self):
    
        '''Build a buffer list from an outline.'''
        
        self.positions =  {}
        self.tnodes = {}
    
        for p in c.allNodes_iter():
        
            t = p.v.t ; h = t.headString()
            
            theList = self.positions.get(h,[])
            theList.append(p.copy())
            self.positions [h] = theList
            
            self.tnodes [h] = t.bodyString()
    #@nonl
    #@-node:ekr.20050927101829.2:buildBufferList (not used)
    #@+node:ekr.20050920084036.41:bufferList (to be deleted)
    def bufferList (self,event):
        
        k = self.k
        state = k.getState('bufferList')
        if state.startswith('start'):
            state = state[5:]
            k.setState('bufferList',state)
            k.setLabel('')
        if event.keysym=='Tab':
            stext = k.getLabel().strip()
            if self.bufferTracker.prefix and stext.startswith(self.bufferTracker.prefix):
                k.setLabel(self.bufferTracker.next())#get next in iteration
            else:
                prefix = k.getLabel()
                pmatches =[]
                for z in self.bufferDict.keys():
                    if z.startswith(prefix):
                        pmatches.append(z)
                self.bufferTracker.setTabList(prefix,pmatches)
                k.setLabel(self.bufferTracker.next())#begin iteration on new lsit
            return 'break'
        elif event.keysym=='Return':
           bMode = k.getState('bufferList')
           return self.commandsDict[bMode](event,k.getLabel())
        else:
            self.update(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.41:bufferList (to be deleted)
    #@-others
#@nonl
#@-node:ekr.20050920084036.31:class bufferCommandsClass
#@+node:ekr.20050920084036.53:class editCommandsClass
class editCommandsClass (baseEditCommandsClass):
    
    '''Contains editing commands with little or no state.'''

    #@    @+others
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
    #@nonl
    #@-node:ekr.20050920084036.54: ctor
    #@+node:ekr.20050920084036.55: getPublicCommands
    def getPublicCommands (self):
    
        k = self.k
    
        return {
            'back-to-indentation': lambda event: self.backToIndentation(event) and k.keyboardQuit(event),
            'backward-delete-char': lambda event, which = 'BackSpace': self.manufactureKeyPress(event,which) and k.keyboardQuit(event),
            'backward-char': lambda event, which = 'Left': k.keyboardQuit(event) and self.manufactureKeyPress(event,which),
            'backward-kill-paragraph': self.backwardKillParagraph,
            'beginning-of-buffer': lambda event, spot = '1.0': self.moveTo(event,spot) and k.keyboardQuit(event),
            'beginning-of-line': lambda event, spot = 'insert linestart': self.moveTo(event,spot) and k.keyboardQuit(event),
            'capitalize-word': lambda event, which = 'cap': self.capitalize(event,which) and k.keyboardQuit(event),
            'center-line': lambda event: self.centerLine(event) and k.keyboardQuit(event),
            'center-region': lambda event: self.centerRegion(event) and k.keyboardQuit(event),
            'dabbrev-completion': lambda event: self.dynamicExpansion2(event) and k.keyboardQuit(event),
            'dabbrev-expands': lambda event: self.dynamicExpansion(event) and k.keyboardQuit(event),
            'delete-char': lambda event: self.deleteNextChar(event) and k.keyboardQuit(event),
            'delete-indentation': lambda event: self.deleteIndentation(event) and k.keyboardQuit(event),
            'downcase-region': lambda event: self.upperLowerRegion(event,'low') and k.keyboardQuit(event),
            'downcase-word': lambda event, which = 'low': self.capitalize(event,which) and k.keyboardQuit(event),
            'end-of-buffer': lambda event, spot = 'end': self.moveTo(event,spot) and k.keyboardQuit(event),
            'end-of-line': lambda event, spot = 'insert lineend': self.moveTo(event,spot) and k.keyboardQuit(event),
            'eval-expression': self.startEvaluate,
            'fill-region-as-paragraph': self.fillRegionAsParagraph,
            'fill-region': self.fillRegion,
            'flush-lines': lambda event: self.flushLines,
            'forward-char': lambda event, which = 'Right': k.keyboardQuit(event) and self.manufactureKeyPress(event,which),
            'goto-char': lambda event: self.startGoto(event,True),
            'goto-line': lambda event: self.startGoto(event),
            'how-many': self.startHowMany, ### Change name?
            'indent-region': lambda event: self.indentRegion(event) and k.keyboardQuit(event),
            'indent-rigidly': lambda event: self.tabIndentRegion(event) and k.keyboardQuit(event),
            'indent-relative': self.indentRelative,
            'insert-file': lambda event: self.insertFile(event) and k.keyboardQuit(event),
            'keep-lines': self.keepLines,
            'kill-paragraph': self.killParagraph,
            'newline-and-indent': lambda event: self.insertNewLineAndTab(event) and k.keyboardQuit(event),
            'next-line': lambda event, which = 'Down': k.keyboardQuit(event) and self.manufactureKeyPress(event,which),
            'previous-line': lambda event, which = 'Up': k.keyboardQuit(event) and self.manufactureKeyPress(event,which),
            'replace-regex': lambda event: self.activateReplaceRegex() and self.replaceString(event),
            'replace-string': self.replaceString,
            'reverse-region': self.reverseRegion,
            'save-buffer': lambda event: self.saveFile(event) and k.keyboardQuit(event),
            'scroll-down': lambda event, way = 'south': self.screenscroll(event,way) and k.keyboardQuit(event),
            'scroll-up': lambda event, way = 'north': self.screenscroll(event,way) and k.keyboardQuit(event),
            'set-fill-column': self.setFillColumn,
            'set-fill-prefix': self.setFillPrefix,
            'set-mark-command': lambda event: self.setRegion(event) and k.keyboardQuit(event),
            'sort-columns': self.sortColumns,
            'sort-fields': self.sortFields,
            'sort-lines': self.sortLines,
            'split-line': lambda event: self.insertNewLineIndent(event) and k.keyboardQuit(event),
            'tabify': self.tabify,
            'transpose-chars': lambda event: self.swapCharacters(event) and k.keyboardQuit(event),
            'transpose-words': lambda event, sw = self.swapSpots: self.swapWords(event,sw) and k.keyboardQuit(event),
            'transpose-lines': lambda event: self.transposeLines(event) and k.keyboardQuit(event),
            'untabify': self.untabify,
            'upcase-region': lambda event: self.upperLowerRegion(event,'up') and k.keyboardQuit(event),
            'upcase-word': lambda event, which = 'up': self.capitalize(event,which) and k.keyboardQuit(event),
            'view-lossage': self.viewLossage,
            'what-line': self.whatLine,
    
            # Added by EKR:
            'back-sentence': self.backSentence,
            'delete-spaces': self.deleteSpaces,
            'forward-sentence': self.forwardSentence,
            'exchange-point-mark': self.exchangePointMark,
            'indent-to-comment-column': self.indentToCommentColumn,
            'insert-newline': self.insertNewline,
            'insert-parentheses': self.insertParentheses,
            'line-number': self.lineNumber,
            'move-past-close': self.movePastClose,
            'remove-blank-lines': self.removeBlankLines,
            'select-all': self.selectAll,
            'set-comment-column': self.setCommentColumn,
        }
    #@nonl
    #@-node:ekr.20050920084036.55: getPublicCommands
    #@+node:ekr.20050920084036.56: Entry points
    #@+node:ekr.20050920084036.57:capitalize
    def capitalize( self, event, which ):
        w = event.widget
        text = w.get( 'insert wordstart', 'insert wordend' )
        i = w.index( 'insert' )
        if text == ' ': return 'break'
        w.delete( 'insert wordstart', 'insert wordend' )
        if which == 'cap':
            text = text.capitalize() 
        if which == 'low':
            text = text.lower()
        if which == 'up':
            text = text.upper()
        w.insert( 'insert', text )
        w.mark_set( 'insert', i )    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.57:capitalize
    #@+node:ekr.20050920084036.58:dynamic abbreviation...
    #@+node:ekr.20050920084036.59:dynamicExpansion
    def dynamicExpansion( self, event ):#, store = {'rlist': [], 'stext': ''} ):
        
        k = self.k ; w = event.widget
        rlist = self.store[ 'rlist' ]
        stext = self.store[ 'stext' ]
        i = w.index( 'insert -1c wordstart' )
        i2 = w.index( 'insert -1c wordend' )
        txt = w.get( i, i2 )
        dA = w.tag_ranges( 'dA' )
        w.tag_delete( 'dA' )
        def doDa( txt, from_ = 'insert -1c wordstart', to_ = 'insert -1c wordend' ):
            w.delete( from_, to_ ) 
            w.insert( 'insert', txt, 'dA' )
            return k._tailEnd( w )
            
        if dA:
            dA1, dA2 = dA
            dtext = w.get( dA1, dA2 )
            if dtext.startswith( stext ) and i2 == dA2:
                #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
                if rlist:
                    txt = rlist.pop()
                else:
                    txt = stext
                    w.delete( dA1, dA2 )
                    dA2 = dA1 #since the text is going to be reread, we dont want to include the last dynamic abbreviation
                    self.getDynamicList( w, txt, rlist )
                return doDa( txt, dA1, dA2 )
            else:
                dA = None
                
        if not dA:
            self.store[ 'stext' ] = txt
            self.store[ 'rlist' ] = rlist = []
            self.getDynamicList( w, txt, rlist )
            if not rlist:
                return 'break'
            txt = rlist.pop()
            return doDa( txt )
    #@-node:ekr.20050920084036.59:dynamicExpansion
    #@+node:ekr.20050920084036.60:dynamicExpansion2
    def dynamicExpansion2( self, event ):
        
        k = self.k ; w = event.widget
        i = w.index( 'insert -1c wordstart' )
        i2 = w.index( 'insert -1c wordend' )
        txt = w.get( i, i2 )   
        rlist = []
        self.getDynamicList( w, txt, rlist )
        dEstring = reduce( g.longestCommonPrefix, rlist )
        if dEstring:
            w.delete( i , i2 )
            w.insert( i, dEstring )    
            return k._tailEnd( w )
    #@-node:ekr.20050920084036.60:dynamicExpansion2
    #@+node:ekr.20050920084036.61:getDynamicList (helper)
    def getDynamicList( self, w, txt , rlist ):
    
         ttext = w.get( '1.0', 'end' )
         items = self.dynaregex.findall( ttext ) #make a big list of what we are considering a 'word'
         if items:
             for word in items:
                 if not word.startswith( txt ) or word == txt: continue #dont need words that dont match or == the pattern
                 if word not in rlist:
                     rlist.append( word )
                 else:
                     rlist.remove( word )
                     rlist.append( word )
    #@nonl
    #@-node:ekr.20050920084036.61:getDynamicList (helper)
    #@-node:ekr.20050920084036.58:dynamic abbreviation...
    #@+node:ekr.20050920084036.62:esc methods for Python evaluation
    #@+node:ekr.20050920084036.63:watchEscape
    def watchEscape (self,event):
    
        k = self.k ; w = event.widget
        if not k.inState():
            k.setState('escape','start')
            k.setLabelBlue('Esc')
            return 'break'
    
        if k.getStateKind() == 'escape':
            state = k.getState('escape')
            hi1 = self.keysymHistory [0]
            hi2 = self.keysymHistory [1]
            if state == 'esc esc' and event.keysym == 'colon':
                return self.startEvaluate(event)
            elif state == 'evaluate':
                return self.escEvaluate(event)
            elif hi1 == hi2 == 'Escape':
                k.setState('escape','esc esc')
                k.setLabel('Esc Esc -')
                return 'break'
            elif event.keysym in ('Shift_L','Shift_R'):
                return
            else:
                return k.keyboardQuit(event)
    #@-node:ekr.20050920084036.63:watchEscape
    #@+node:ekr.20050920084036.64:escEvaluate
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
                return k._tailEnd(w)
        else:
            k.updateLabel(event)
            return 'break'
    #@-node:ekr.20050920084036.64:escEvaluate
    #@+node:ekr.20050920084036.65:startEvaluate
    def startEvaluate (self,event):
    
        k = self.k
    
        k.setLabelBlue('Eval:')
        k.setState('escape','evaluate')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.65:startEvaluate
    #@-node:ekr.20050920084036.62:esc methods for Python evaluation
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
    def centerLine( self, event ):
        '''Centers line within current fillColumn'''
        
        k = self.k ; w = event.widget
        ind = w.index( 'insert linestart' )
        txt = w.get( 'insert linestart', 'insert lineend' )
        txt = txt.strip()
        if len( txt ) >= self.fillColumn: return k._tailEnd( w )
        amount = ( self.fillColumn - len( txt ) ) / 2
        ws = ' ' * amount
        col, nind = ind.split( '.' )
        ind = w.search( '\w', 'insert linestart', regexp = True, stopindex = 'insert lineend' )
        if not ind: return 'break'
        w.delete( 'insert linestart', '%s' % ind )
        w.insert( 'insert linestart', ws )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.67:centerLine
    #@+node:ekr.20050920084036.68:setFillColumn
    def setFillColumn (self,event):
    
        k = self.k ; state = k.getState('set-fill-column')
        
        if state == 0:
            k.setLabelBlue('Set Fill Column: ')
            k.getArg(event,'set-fill-column',1,self.setFillColumn)
        else:
            try:
                n = int(k.arg)
                k.setLabelGrey('fill column is: %d' % n)
            except ValueError:
                k.resetLabel()
            k.clearState()
    
        return 'break'
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
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.69:centerRegion
    #@+node:ekr.20050920084036.70:setFillPrefix
    def setFillPrefix( self, event ):
    
        w = event.widget
        txt = w.get( 'insert linestart', 'insert' )
        self.fillPrefix = txt
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.70:setFillPrefix
    #@+node:ekr.20050920084036.71:_addPrefix
    def _addPrefix( self, ntxt ):
            ntxt = ntxt.split( '.' )
            ntxt = map( lambda a: self.fillPrefix+a, ntxt )
            ntxt = '.'.join( ntxt )               
            return ntxt
    #@nonl
    #@-node:ekr.20050920084036.71:_addPrefix
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.66:fill column and centering
    #@+node:ekr.20050920084036.72:goto...
    #@+node:ekr.20050920084036.73:startGoto
    def startGoto (self,event,ch=False):
    
        k = self.k
    
        k.setState('goto',k.getState()+1,handler=self.Goto)
        k.setLabelBlue('')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.73:startGoto
    #@+node:ekr.20050920084036.143:Goto
    def Goto (self,event):
    
        k = self.k ; w = event.widget
        if event.keysym == 'Return':
            i = k.getLabel()
            k.resetLabel()
            state = k.getState('goto')
            k.setState('goto',0)
            if i.isdigit():
                if state == 1:
                    widget.mark_set('insert','%s.0' % i)
                elif state == 2:
                    widget.mark_set('insert','1.0 +%sc' % i)
                widget.event_generate('<Key>')
                widget.update_idletasks()
                widget.see('insert')
        else:
            k.updateLabel(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.143:Goto
    #@-node:ekr.20050920084036.72:goto...
    #@+node:ekr.20050920084036.74:indent...
    #@+node:ekr.20050920084036.75:backToIndentation
    def backToIndentation( self, event ):
    
        w = event.widget
        i = w.index( 'insert linestart' )
        i2 = w.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
        w.mark_set( 'insert', i2 )
        w.update_idletasks()
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.75:backToIndentation
    #@+node:ekr.20050920084036.76:deleteIndentation
    def deleteIndentation( self, event ):
    
        k = self.k ; w = event.widget
        txt = w.get( 'insert linestart' , 'insert lineend' )
        txt = ' %s' % txt.lstrip()
        w.delete( 'insert linestart' , 'insert lineend +1c' )    
        i  = w.index( 'insert - 1c' )
        w.insert( 'insert -1c', txt )
        w.mark_set( 'insert', i )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.76:deleteIndentation
    #@+node:ekr.20050920084036.77:insertNewLineIndent
    def insertNewLineIndent( self, event ):
        w =  event.widget
        txt = w.get( 'insert linestart', 'insert lineend' )
        txt = self.getWSString( txt )
        i = w.index( 'insert' )
        w.insert( i, txt )
        w.mark_set( 'insert', i )    
        return self.insertNewLine( event )
    #@nonl
    #@-node:ekr.20050920084036.77:insertNewLineIndent
    #@+node:ekr.20050920084036.78:indentRelative
    def indentRelative( self, event ):
        
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        l,c = i.split( '.' )
        c2 = int( c )
        l2 = int( l ) - 1
        if l2 < 1: return k.keyboardQuit( event )
        txt = w.get( '%s.%s' % (l2, c2 ), '%s.0 lineend' % l2 )
        if len( txt ) <= len( w.get( 'insert', 'insert lineend' ) ):
            w.insert(  'insert', '\t' )
        else:
            reg = re.compile( '(\s+)' )
            ntxt = reg.split( txt )
            replace_word = re.compile( '\w' )
            for z in ntxt:
                if z.isspace():
                    w.insert( 'insert', z )
                    break
                else:
                    z = replace_word.subn( ' ', z )
                    w.insert( 'insert', z[ 0 ] )
                    w.update_idletasks()
            
            
        k.keyboardQuit( event )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.78:indentRelative
    #@-node:ekr.20050920084036.74:indent...
    #@+node:ekr.20050920084036.79:info...
    #@+node:ekr.20050920084036.80:howMany
    def howMany (self,event):
    
        k = self.k ; w = event.widget
        if event.keysym == 'Return':
            txt = w.get('1.0','end')
            reg1 = k.getLabel()
            reg = re.compile(reg1)
            i = reg.findall(txt)
            k.setLabelGrey('%s occurances found of %s' % (len(i),reg1))
            k.setState('howM',0,handler=self.howMany)
        else:
            k.updateLabel(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.80:howMany
    #@+node:ekr.20050920084036.81:lineNumber
    def lineNumber (self,event):
    
        k = self.k
        w = event.widget
        k.stopControlX(event)
        i = w.index('insert')
        i1, i2 = i.split('.')
        c = w.get('insert','insert + 1c')
        txt = w.get('1.0','end')
        txt2 = w.get('1.0','insert')
        perc = len(txt) * .01
        perc = int(len(txt2)/perc)
        k.setLabel('Char: %s point %s of %s(%s%s)  Column %s' % (c,len(txt2),len(txt),perc,'%',i1))
    
        return 'break'
    
    #@-node:ekr.20050920084036.81:lineNumber
    #@+node:ekr.20050920084036.82:startHowMany
    def startHowMany (self,event):
    
        k = self.k
    
        k.setState('howM',1)
        k.setLabelBlue('')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.82:startHowMany
    #@+node:ekr.20050920084036.83:viewLossage
    def viewLossage (self,event):
    
        k = self.k
        loss = ''.join(leoKeys.kClass.lossage)
        k.keyboardQuit(event)
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
    #@-node:ekr.20050920084036.84:whatLine
    #@-node:ekr.20050920084036.79:info...
    #@+node:ekr.20050920084036.85:Insert/delete...
    #@+node:ekr.20050920084036.86:insertNewLineAndTab
    def insertNewLineAndTab( self, event ):
        
        '''Insert a newline and tab'''
        
        k = self.k ; w = event.widget
        self.insertNewLine( event )
        i = w.index( 'insert +1c' )
        w.insert( i, '\t' )
        w.mark_set( 'insert', '%s lineend' % i )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.86:insertNewLineAndTab
    #@+node:ekr.20050920084036.87:deleteNextChar
    def deleteNextChar( self,event ):
    
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        w.delete( i, '%s +1c' % i )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.87:deleteNextChar
    #@-node:ekr.20050920084036.85:Insert/delete...
    #@+node:ekr.20050920084036.88:line...
    #@+node:ekr.20050920084036.89: Entries
    #@+node:ekr.20050920084036.90:flushLines
    def flushLines (self,event):
    
        '''Delete each line that contains a match for regexp, operating on the text after point.
    
        In Transient Mark mode, if the region is active, the command operates on the region instead.'''
    
        return self.startLines(event,which='flush')
    #@nonl
    #@-node:ekr.20050920084036.90:flushLines
    #@+node:ekr.20050920084036.91:keepLines
    def keepLines (self,event):
    
        '''Delete each line that does not contain a match for regexp, operating on the text after point.
    
        In Transient Mark mode, if the region is active, the command operates on the region instead.'''
    
        return self.startLines(event,which='keep')
    #@nonl
    #@-node:ekr.20050920084036.91:keepLines
    #@-node:ekr.20050920084036.89: Entries
    #@+node:ekr.20050920084036.92:alterLines
    def alterLines( self, event, which ):
        
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        end = 'end'
        if w.tag_ranges( 'sel' ):
            i = w.index( 'sel.first' )
            end = w.index( 'sel.last' )
        txt = w.get( i, end )
        tlines = txt.splitlines( True )
        if which == 'flush':    keeplines = list( tlines )
        else:                   keeplines = []
        pattern = k.getLabel()
        try:
            regex = re.compile( pattern )
            for n , z in enumerate( tlines ):
                f = regex.findall( z )
                if which == 'flush' and f:
                    keeplines[ n ] = None
                elif f:
                    keeplines.append( z )
        except Exception,x:
            return
        if which == 'flush':
            keeplines = [ x for x in keeplines if x != None ]
        w.delete( i, end )
        w.insert( i, ''.join( keeplines ) )
        w.mark_set( 'insert', i )
        k._tailEnd( w )
    #@-node:ekr.20050920084036.92:alterLines
    #@+node:ekr.20050920084036.93:processLines
    def processLines (self,event):
    
        k = self.k
        state = k.getState('alterlines')
    
        if state.startswith('start'):
            state = state [5:]
            k.setState('alterlines',state)
            k.setLabel('')
    
        if event.keysym == 'Return':
            self.alterLines(event,state)
            return k.keyboardQuit(event)
        else:
            k.updateLabel(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.93:processLines
    #@+node:ekr.20050920084036.94:startLines
    def startLines (self,event,which='flush'):
    
        k = self.k
    
        k.keyboardQuit(event)
        k.setState('alterlines','start%s' % which)
        k.setLabelBlue()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.94:startLines
    #@-node:ekr.20050920084036.88:line...
    #@+node:ekr.20050920084036.95:paragraph...
    #@+others
    #@+node:ekr.20050920084036.96:selectParagraph
    def selectParagraph( self, event ):
    
        k = self.k ; w = event.widget
        txt = w.get( 'insert linestart', 'insert lineend' )
        txt = txt.lstrip().rstrip()
        i = w.index( 'insert' )
        if not txt:
            while 1:
                i = w.index( '%s + 1 lines' % i )
                txt = w.get( '%s linestart' % i, '%s lineend' % i )
                txt = txt.lstrip().rstrip()
                if txt:
                    self._selectParagraph( w, i )
                    break
                if w.index( '%s lineend' % i ) == w.index( 'end' ):
                    return 'break'
        if txt:
            while 1:
                i = w.index( '%s - 1 lines' % i )
                txt = w.get( '%s linestart' % i, '%s lineend' % i )
                txt = txt.lstrip().rstrip()
                if not txt or w.index( '%s linestart' % i ) == w.index( '1.0' ):
                    if not txt:
                        i = w.index( '%s + 1 lines' % i )
                    self._selectParagraph( w, i )
                    break     
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.96:selectParagraph
    #@+node:ekr.20050920084036.97:_selectParagraph
    def _selectParagraph( self, w, start ):
        i2 = start
        while 1:
            txt = w.get( '%s linestart' % i2, '%s lineend' % i2 )
            if w.index( '%s lineend' % i2 )  == w.index( 'end' ):
                break
            txt = txt.lstrip().rstrip()
            if not txt: break
            else:
                i2 = w.index( '%s + 1 lines' % i2 )
        w.tag_add( 'sel', '%s linestart' % start, '%s lineend' % i2 )
        w.mark_set( 'insert', '%s lineend' % i2 )
    #@nonl
    #@-node:ekr.20050920084036.97:_selectParagraph
    #@+node:ekr.20050920084036.98:killParagraph
    def killParagraph( self, event ):
        
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        txt = w.get( 'insert linestart', 'insert lineend' )
        if not txt.rstrip().lstrip():
            i = w.search( r'\w', i, regexp = True, stopindex = 'end' )
        self._selectParagraph( w, i )
        i2 = w.index( 'insert' )
        self.kill( event, i, i2 )
        w.mark_set( 'insert', i )
        w.selection_clear()
        return k._tailEnd( w )
    
    #@-node:ekr.20050920084036.98:killParagraph
    #@+node:ekr.20050920084036.99:backwardKillParagraph
    def backwardKillParagraph( self, event ):
     
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        i2 = i
        txt = w.get( 'insert linestart', 'insert lineend' )
        if not txt.rstrip().lstrip():
            self.movingParagraphs( event, -1 )
            i2 = w.index( 'insert' )
        self.selectParagraph( event )
        i3 = w.index( 'sel.first' )
        self.kill( event, i3, i2 )
        w.mark_set( 'insert', i )
        w.selection_clear()
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.99:backwardKillParagraph
    #@+node:ekr.20050920084036.100:fillRegion
    def fillRegion (self,event):
    
        k = self.k ; w = event.widget
        if not self._chckSel(event):
            return
        s1 = w.index('sel.first')
        s2 = w.index('sel.last')
        w.mark_set('insert',s1)
        self.movingParagraphs(event,-1)
        if w.index('insert linestart') == '1.0':
            self.fillParagraph(event)
        while 1:
            self.movingParagraphs(event,1)
            if w.compare('insert','>',s2):
                break
            self.fillParagraph(event)
        return k._tailEnd(w)
    #@-node:ekr.20050920084036.100:fillRegion
    #@+node:ekr.20050920084036.101:UNTESTED
    #@+at
    # 
    # untested as of yet for .5 conversion.
    # 
    #@-at
    #@@c
    
    
    #@+others
    #@+node:ekr.20050920084036.102:movingParagraphs
    def movingParagraphs( self, event, way ):
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        if way == 1:
            while 1:
                txt = w.get( '%s linestart' % i, '%s lineend' %i )
                txt = txt.rstrip().lstrip()
                if not txt:
                    i = w.search( r'\w', i, regexp = True, stopindex = 'end' )
                    i = '%s' %i
                    break
                else:
                    i = w.index( '%s + 1 lines' % i )
                    if w.index( '%s linestart' % i ) == w.index( 'end' ):
                        i = w.search( r'\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                        i = '%s + 1c' % i
                        break
        else:
            while 1:
                txt = w.get( '%s linestart' % i, '%s lineend' %i )
                txt = txt.rstrip().lstrip()
                if not txt:
                    i = w.search( r'\w', i, backwards = True, regexp = True, stopindex = '1.0' )
                    i = '%s +1c' %i
                    break
                else:
                    i = w.index( '%s - 1 lines' % i )
                    if w.index( '%s linestart' % i ) == '1.0':
                        i = w.search( r'\w', '1.0', regexp = True, stopindex = 'end' )
                        break
        if i : 
            w.mark_set( 'insert', i )
            w.see( 'insert' )
            return k._tailEnd( w )
        return 'break'
    #@-node:ekr.20050920084036.102:movingParagraphs
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
            return k._tailEnd( w )
    #@-node:ekr.20050920084036.103:fillParagraph
    #@+node:ekr.20050920084036.104:fillRegionAsParagraph
    def fillRegionAsParagraph( self, event ):
        
        k = self.k ; w = event.widget
        if not self._chckSel( event ):
            return
        i1 = w.index( 'sel.first linestart' )
        i2 = w.index( 'sel.last lineend' )
        txt = w.get(  i1,  i2 )
        txt = self._addPrefix( txt )
        w.delete( i1, i2 )
        w.insert( i1, txt )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.104:fillRegionAsParagraph
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.101:UNTESTED
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.95:paragraph...
    #@+node:ekr.20050920084036.105:region...
    #@+others
    #@+node:ekr.20050920084036.106:setRegion
    def setRegion( self, event ):
    
        mrk = 'sel'
        w = event.widget
        def extend( event ):
            widget = event.widget
            widget.mark_set( 'insert', 'insert + 1c' )
            if self.inRange( widget, mrk ):
                widget.tag_remove( mrk, 'insert -1c' )
            else:
                widget.tag_add( mrk, 'insert -1c' )
                widget.tag_configure( mrk, background = 'lightgrey' )
                self.testinrange( widget )
            return 'break'
            
        def truncate( event ):
            widget = event.widget
            widget.mark_set( 'insert', 'insert -1c' )
            if self.inRange( widget, mrk ):
                self.testinrange( widget )
                widget.tag_remove( mrk, 'insert' )
            else:
                widget.tag_add( mrk, 'insert' )
                widget.tag_configure( mrk, background = 'lightgrey' )
                self.testinrange( widget  )
            return 'break'
            
        def up( event ):
            widget = event.widget
            if not self.testinrange( widget ):
                return 'break'
            widget.tag_add( mrk, 'insert linestart', 'insert' )
            i = widget.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = str( int( i1 ) - 1 )
            widget.mark_set( 'insert', i1+'.'+i2)
            widget.tag_add( mrk, 'insert', 'insert lineend + 1c' )
            if self.inRange( widget, mrk ,l = '-1c', r = '+1c') and widget.index( 'insert' ) != '1.0':
                widget.tag_remove( mrk, 'insert', 'end' )  
            return 'break'
            
        def down( event ):
            widget = event.widget
            if not self.testinrange( widget ):
                return 'break'
            widget.tag_add( mrk, 'insert', 'insert lineend' )
            i = widget.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = str( int( i1 ) + 1 )
            widget.mark_set( 'insert', i1 +'.'+i2 )
            widget.tag_add( mrk, 'insert linestart -1c', 'insert' )
            if self.inRange( widget, mrk , l = '-1c', r = '+1c' ): 
                widget.tag_remove( mrk, '1.0', 'insert' )
            return 'break'
            
        extend( event )   
        w.bind( '<Right>', extend, '+' )
        w.bind( '<Left>', truncate, '+' )
        w.bind( '<Up>', up, '+' )
        w.bind( '<Down>', down, '+' )
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.106:setRegion
    #@+node:ekr.20050920084036.107:indentRegion
    def indentRegion( self, event ):
        w = event.widget
        mrk = 'sel'
        trange = w.tag_ranges( mrk )
        if len( trange ) != 0:
            ind = w.search( '\w', '%s linestart' % trange[ 0 ], stopindex = 'end', regexp = True )
            if not ind : return
            text = w.get( '%s linestart' % ind ,  '%s lineend' % ind)
            sstring = text.lstrip()
            sstring = sstring[ 0 ]
            ws = text.split( sstring )
            if len( ws ) > 1:
                ws = ws[ 0 ]
            else:
                ws = ''
            s , s1 = trange[ 0 ].split( '.' )
            e , e1 = trange[ -1 ].split( '.' )
            s = int( s )
            s = s + 1
            e = int( e ) + 1
            for z in xrange( s , e ):
                t2 = w.get( '%s.0' %z ,  '%s.0 lineend'%z)
                t2 = t2.lstrip()
                t2 = ws + t2
                w.delete( '%s.0' % z ,  '%s.0 lineend' %z)
                w.insert( '%s.0' % z, t2 )
            w.event_generate( '<Key>' )
            w.update_idletasks()
        self.removeRKeys( w )
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.107:indentRegion
    #@+node:ekr.20050920084036.108:tabIndentRegion
    def tabIndentRegion( self,event ):
    
        k = self.k ; w = event.widget
        if not self._chckSel( event ):
            return
        i = w.index( 'sel.first' )
        i2 = w.index( 'sel.last' )
        i = w.index( '%s linestart' %i )
        i2 = w.index( '%s linestart' % i2)
        while 1:
            w.insert( i, '\t' )
            if i == i2: break
            i = w.index( '%s + 1 lines' % i )    
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.108:tabIndentRegion
    #@+node:ekr.20050920084036.109:countRegion
    def countRegion (self,event):
    
        k = self.k ; w = event.widget
        txt = w.get('sel.first','sel.last')
        lines = 1 ; chars = 0
        for z in txt:
            if z == '\n':   lines = lines + 1
            else:           chars = chars + 1
    
        k.setLabel('Region has %s lines, %s characters' % (lines,chars))
        return 'break'
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
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.110:reverseRegion
    #@+node:ekr.20050920084036.111:upperLowerRegion
    def upperLowerRegion( self, event, way ):
    
        w = event.widget
        mrk = 'sel'
        trange = w.tag_ranges( mrk )
        if len( trange ) != 0:
            text = w.get( trange[ 0 ] , trange[ -1 ] )
            i = w.index( 'insert' )
            if text == ' ': return 'break'
            w.delete( trange[ 0 ], trange[ -1 ] )
            if way == 'low':
                text = text.lower()
            if way == 'up':
                text = text.upper()
            w.insert( 'insert', text )
            w.mark_set( 'insert', i ) 
        self.removeRKeys( w )
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.111:upperLowerRegion
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.105:region...
    #@+node:ekr.20050920084036.112:replace...
    #@+node:ekr.20050920084036.113:replaceString
    def replaceString (self,event):
        
        k = self.k ; w = event.widget
        # This should not be here.
        if event.keysym in ('Control_L','Control_R'): return
        state = k.getState('rString')
        regex = self._useRegex
        prompt = 'Replace ' + g.choose(regex,'Regex','String')
        if state == 0:
            self._sString = self._rpString = ''
            s = '%s: ' % prompt
            k.setLabel(s)
            # Get arg and enter state 1.
            return k.getArg(event,'rString',1,self.replaceStringStateHandler) 
        elif state == 1:
            self._sString = k.arg
            s = '%s: %s With: ' % (prompt,self._sString)
            k.setLabel(s)
            # Get arg and enter state 2.
            return k.getArg(event,'rString',2,self.replaceStringStateHandler)
        elif state == 2:
            self._rpString = k.arg
            #@        << do the replace >>
            #@+node:ekr.20050920084036.114:<< do the replace >>
            # g.es('%s %s by %s' % (prompt,repr(self._sString),repr(self._rpString)),color='blue')
            i = 'insert' ; end = 'end' ; count = 0
            if w.tag_ranges('sel'):
                i = w.index('sel.first')
                end = w.index('sel.last')
            if regex:
                txt = w.get(i,end)
                try:
                    pattern = re.compile(self._sString)
                except:
                    k.keyboardQuit(event)
                    k.setLabel("Illegal regular expression")
                    return 'break'
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
            k.setLabelGrey('Replaced %s occurances' % count)
            k.clearState()
            self._useRegex = False
            return k._tailEnd(w)
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
    #@+node:ekr.20050920084036.116:screenscroll
    def screenscroll (self,event,way='north'):
    
        k = self.k ; w = event.widget
        chng = self.measure(w)
        i = w.index('insert')
    
        if way == 'north':
            i1, i2 = i.split('.')
            i1 = int(i1) - chng [0]
        else:
            i1, i2 = i.split('.')
            i1 = int(i1) + chng [0]
    
        w.mark_set('insert','%s.%s' % (i1,i2))
        w.see('insert')
        return k._tailEnd(w)
    #@-node:ekr.20050920084036.116:screenscroll
    #@+node:ekr.20050920084036.117:sort...
    #@+node:ekr.20050920084036.118:sortLines
    def sortLines( self, event , which = None ): # event IS used.
    
        k = self.k ; w = event.widget  
        if not self._chckSel( event ):
            return k.keyboardQuit( event )
        i = w.index( 'sel.first' )
        i2 = w.index( 'sel.last' )
        is1 = i.split( '.' )
        is2 = i2.split( '.' )
        txt = w.get( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
        ins = w.index( 'insert' )
        txt = txt.split( '\n' )
        w.delete( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
        txt.sort()
        if which:
            txt.reverse()
        inum = int(is1[ 0 ])
        for z in txt:
            w.insert( '%s.0' % inum, '%s\n' % z ) 
            inum = inum + 1
        w.mark_set( 'insert', ins )
        k.keyboardQuit( event )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.118:sortLines
    #@+node:ekr.20050920084036.119:sortColumns
    def sortColumns( self, event ):
    
        k = self.k ; w = event.widget
        if not self._chckSel( event ):
            return k.keyboardQuit( event )
            
        ins = w.index( 'insert' )
        is1 = w.index( 'sel.first' )
        is2 = w.index( 'sel.last' )   
        sint1, sint2 = is1.split( '.' )
        sint2 = int( sint2 )
        sint3, sint4 = is2.split( '.' )
        sint4 = int( sint4 )
        txt = w.get( '%s.0' % sint1, '%s.0 lineend' % sint3 )
        w.delete( '%s.0' % sint1, '%s.0 lineend' % sint3 )
        columns = []
        i = int( sint1 )
        i2 = int( sint3 )
        while i <= i2:
            t = w.get( '%s.%s' %( i, sint2 ), '%s.%s' % ( i, sint4 ) )
            columns.append( t )
            i = i + 1
        txt = txt.split( '\n' )
        zlist = zip( columns, txt )
        zlist.sort()
        i = int( sint1 )      
        for z in xrange( len( zlist ) ):
             w.insert( '%s.0' % i, '%s\n' % zlist[ z ][ 1 ] ) 
             i = i + 1
        w.mark_set( 'insert', ins )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.119:sortColumns
    #@+node:ekr.20050920084036.120:sortFields
    def sortFields( self, event, which = None ):
        
        k = self.k ; w = event.widget
        if not self._chckSel( event ):
            return k.keyboardQuit( event )
        ins = w.index( 'insert' )
        is1 = w.index( 'sel.first' )
        is2 = w.index( 'sel.last' )
        txt = w.get( '%s linestart' % is1, '%s lineend' % is2 )
        txt = txt.split( '\n' )
        fields = []
        import re
        fn = r'\w+'
        frx = re.compile( fn )
        for z in txt:
            f = frx.findall( z )
            if not which:
                fields.append( f[ 0 ] )
            else:
                i =  int( which )
                if len( f ) < i:
                    return k._tailEnd( w )
                i = i - 1            
                fields.append( f[ i ] )
        nz = zip( fields, txt )
        nz.sort()
        w.delete( '%s linestart' % is1, '%s lineend' % is2 )
        i = is1.split( '.' )
        int1 = int( i[ 0 ] )
        for z in nz:
            w.insert( '%s.0' % int1, '%s\n'% z[1] )
            int1 = int1 + 1
        w.mark_set( 'insert' , ins )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.120:sortFields
    #@-node:ekr.20050920084036.117:sort...
    #@+node:ekr.20050920084036.121:swap/transpose...
    #@+node:ekr.20050920084036.122:transposeLines
    def transposeLines( self, event ):
    
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = str( int( i1 ) -1 )
        if i1 != '0':
            l2 = w.get( 'insert linestart', 'insert lineend' )
            w.delete( 'insert linestart-1c', 'insert lineend' )
            w.insert( i1+'.0', l2 +'\n')
        else:
            l2 = w.get( '2.0', '2.0 lineend' )
            w.delete( '2.0', '2.0 lineend' )
            w.insert( '1.0', l2 + '\n' )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.122:transposeLines
    #@+node:ekr.20050920084036.123:swapWords
    def swapWords( self, event , swapspots ):
        w = event.widget
        txt = w.get( 'insert wordstart', 'insert wordend' )
        if txt == ' ' : return 'break'
        i = w.index( 'insert wordstart' )
        if len( swapspots ) != 0:
            def swp( find, ftext, lind, ltext ):
                w.delete( find, '%s wordend' % find )
                w.insert( find, ltext )
                w.delete( lind, '%s wordend' % lind )
                w.insert( lind, ftext )
                swapspots.pop()
                swapspots.pop()
                return 'break'
            if w.compare( i , '>', swapspots[ 1 ] ):
                return swp( i, txt, swapspots[ 1 ], swapspots[ 0 ] )
            elif w.compare( i , '<', swapspots[ 1 ] ):
                return swp( swapspots[ 1 ], swapspots[ 0 ], i, txt )
            else:
                return 'break'
        else:
            swapspots.append( txt )
            swapspots.append( i )
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.123:swapWords
    #@+node:ekr.20050920084036.124:swapCharacters
    def swapCharacters( self, event ):
    
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        c1 = w.get( 'insert', 'insert +1c' )
        c2 = w.get( 'insert -1c', 'insert' )
        w.delete( 'insert -1c', 'insert' )
        w.insert( 'insert', c1 )
        w.delete( 'insert', 'insert +1c' )
        w.insert( 'insert', c2 )
        w.mark_set( 'insert', i )
        return k._tailEnd( w )
    #@-node:ekr.20050920084036.124:swapCharacters
    #@-node:ekr.20050920084036.121:swap/transpose...
    #@+node:ekr.20050920084036.125:tabify...
    def tabify (self,event):
        return self._tabify (event,which='tabify')
        
    def untabify (self,event):
        return self._tabify (event,which='untabify')
    #@nonl
    #@+node:ekr.20050920084036.126:_tabify
    def _tabify (self,event,which='tabify'):
    
        k = self.k ; w = event.widget
        if w.tag_ranges('sel'):
            i = w.index('sel.first')
            end = w.index('sel.last')
            txt = w.get(i,end)
            if which == 'tabify':
                pattern = re.compile(' {4,4}')
                ntxt = pattern.sub('\t',txt)
            else:
                pattern = re.compile('\t')
                ntxt = pattern.sub('    ',txt)
            w.delete(i,end)
            w.insert(i,ntxt)
            k.keyboardQuit(event)
            return k._tailEnd(w)
    
        k.keyboardQuit(event)
    #@-node:ekr.20050920084036.126:_tabify
    #@-node:ekr.20050920084036.125:tabify...
    #@-node:ekr.20050920084036.56: Entry points
    #@+node:ekr.20050920084036.130:New Entry points
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
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.131:backSentence
    #@+node:ekr.20050920084036.132:comment column methods
    #@+node:ekr.20050920084036.133:setCommentColumn
    def setCommentColumn (self,event):
    
        cc = event.widget.index('insert')
        cc1, cc2 = cc.split('.')
        self.ccolumn = cc2
        return 'break'
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
    
        return k._tailEnd(w)
    #@-node:ekr.20050920084036.134:indentToCommentColumn
    #@-node:ekr.20050920084036.132:comment column methods
    #@+node:ekr.20050920084036.135:deleteSpaces
    def deleteSpaces (self,event,insertspace=False):
    
        k = self.k ; w = event.widget
        char = w.get('insert','insert + 1c ')
    
        if char.isspace():
            i = w.index('insert')
            wf = w.search(r'\w',i,stopindex='%s lineend' % i,regexp=True)
            wb = w.search(r'\w',i,stopindex='%s linestart' % i,regexp=True,backwards=True)
            if '' in (wf,wb):
                return 'break'
            w.delete('%s +1c' % wb,wf)
            if insertspace:
                w.insert('insert',' ')
    
        return k._tailEnd(w)
    
    #@-node:ekr.20050920084036.135:deleteSpaces
    #@+node:ekr.20050920084036.136:exchangePointMark
    def exchangePointMark (self,event):
    
        if not self._chckSel(event): return
        k = self.k ; w = event.widget
        s1 = w.index('sel.first')
        s2 = w.index('sel.last')
        i = w.index('insert')
    
        if i == s1:
            w.mark_set('insert',s2)
        else:
            w.mark_set('insert',s1)
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.136:exchangePointMark
    #@+node:ekr.20050920084036.137:forwardSentence
    def forwardSentence (self,event,way):
    
        k = self.k ; w = event.widget
    
        i = w.search('.','insert',stopindex='end')
        if i:
            w.mark_set('insert','%s +1c' % i)
        else:
            w.mark_set('insert','end')
    
        return k._tailEnd(w)
    #@-node:ekr.20050920084036.137:forwardSentence
    #@+node:ekr.20050920084036.138:insertNewLine
    def insertNewLine (self,event):
    
        k = self.k ; w = event.widget
        i = w.index('insert')
        w.insert('insert','\n')
        w.mark_set('insert',i)
        return k._tailEnd(w)
    
    insertNewline = insertNewLine
    #@-node:ekr.20050920084036.138:insertNewLine
    #@+node:ekr.20050920084036.139:insertParentheses
    def insertParentheses (self,event):
    
        k = self.k ; w = event.widget
        w.insert('insert','()')
        w.mark_set('insert','insert -1c')
        return k._tailEnd(w)
    #@-node:ekr.20050920084036.139:insertParentheses
    #@+node:ekr.20050920084036.140:movePastClose
    def movePastClose (self,event):
    
        k = self.k ; w = event.widget
        i = w.search('(','insert',backwards=True,stopindex='1.0')
        icheck = w.search(')','insert',backwards=True,stopindex='1.0')
    
        if '' == i:
            return 'break'
        if icheck:
            ic = w.compare(i,'<',icheck)
            if ic:
                return 'break'
        i2 = w.search(')','insert',stopindex='end')
        i2check = w.search('(','insert',stopindex='end')
        if '' == i2:
            return 'break'
        if i2check:
            ic2 = w.compare(i2,'>',i2check)
            if ic2:
                return 'break'
        ib = w.index('insert')
        w.mark_set('insert','%s lineend +1c' % i2)
        if w.index('insert') == w.index('%s lineend' % ib):
            w.insert('insert','\n')
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.140:movePastClose
    #@+node:ekr.20050920084036.141:removeBlankLines
    def removeBlankLines( self, event ):
        w = event.widget
        i = w.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = int( i1 )
        dindex = []
        if w.get( 'insert linestart', 'insert lineend' ).strip() == '':
            while 1:
                if str( i1 )+ '.0'  == '1.0' :
                    break 
                i1 = i1 - 1
                txt = w.get( '%s.0' % i1, '%s.0 lineend' % i1 )
                txt = txt.strip()
                if len( txt ) == 0:
                    dindex.append( '%s.0' % i1)
                    dindex.append( '%s.0 lineend' % i1 )
                elif dindex:
                    w.delete( '%s-1c' % dindex[ -2 ], dindex[ 1 ] )
                    w.event_generate( '<Key>' )
                    w.update_idletasks()
                    break
                else:
                    break
        i = w.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = int( i1 )
        dindex = []
        while 1:
            if w.index( '%s.0 lineend' % i1 ) == w.index( 'end' ):
                break
            i1 = i1 + 1
            txt = w.get( '%s.0' % i1, '%s.0 lineend' % i1 )
            txt = txt.strip() 
            if len( txt ) == 0:
                dindex.append( '%s.0' % i1 )
                dindex.append( '%s.0 lineend' % i1 )
            elif dindex:
                w.delete( '%s-1c' % dindex[ 0 ], dindex[ -1 ] )
                w.event_generate( '<Key>' )
                w.update_idletasks()
                break
            else:
                break
    #@nonl
    #@-node:ekr.20050920084036.141:removeBlankLines
    #@+node:ekr.20050920084036.142:selectAll
    def selectAll( event ):
    
        event.widget.tag_add( 'sel', '1.0', 'end' )
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.142:selectAll
    #@-node:ekr.20050920084036.130:New Entry points
    #@+node:ekr.20050920084036.144:Used by neg argss
    #@+node:ekr.20050920084036.145:changePreviousWord
    def changePreviousWord (self,event):
    
        k = self.k ; stroke = k.stroke ; w = event.widget
        i = w.index('insert')
    
        self.moveword(event,-1)
        if stroke == '<Alt-c>':
            self.capitalize(event,'cap')
        elif stroke == '<Alt-u>':
             self.capitalize(event,'up')
        elif stroke == '<Alt-l>':
            self.capitalize(event,'low')
        w.mark_set('insert',i)
        self.stopControlX(event)
    
        return k._tailEnd(w)
    #@-node:ekr.20050920084036.145:changePreviousWord
    #@-node:ekr.20050920084036.144:Used by neg argss
    #@+node:ekr.20050920084036.146:Utilities
        
    #@nonl
    #@+node:ekr.20050920084036.147:measure
    def measure( self, w ):
        i = w.index( 'insert' )
        i1, i2 = i.split( '.' )
        start = int( i1 )
        watch = 0
        ustart = start
        pone = 1
        top = i
        bottom = i
        while pone:
            ustart = ustart - 1
            if ustart < 0:
                break
            ds = '%s.0' % ustart
            pone = w.dlineinfo( ds )
            if pone:
                top = ds
                watch = watch  + 1
        
        pone = 1
        ustart = start
        while pone:
            ustart = ustart +1
            ds = '%s.0' % ustart
            pone = w.dlineinfo( ds )
            if pone:
                bottom = ds
                watch = watch + 1
                
        return watch , top, bottom
    #@nonl
    #@-node:ekr.20050920084036.147:measure
    #@+node:ekr.20050920084036.148:moveTo
    def moveTo( self, event, spot ):
        w = event.widget
        w.mark_set( Tk.INSERT, spot )
        w.see( spot )
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.148:moveTo
    #@+node:ekr.20050920084036.149:moveword (used by many entires)  TO DO: split into forward/backward versions
    def moveword( self, event, way  ):
        
        '''This function moves the cursor to the next word, direction dependent on the way parameter'''
        
        w = event.widget
        ind = w.index( 'insert' )
    
        if way == 1:
             ind = w.search( '\w', 'insert', stopindex = 'end', regexp=True )
             if ind:
                nind = '%s wordend' % ind
             else:
                nind = 'end'
        else:
             ind = w.search( '\w', 'insert -1c', stopindex= '1.0', regexp = True, backwards = True )
             if ind:
                nind = '%s wordstart' % ind 
             else:
                nind = '1.0'
        w.mark_set( 'insert', nind )
        w.see( 'insert' )
        w.event_generate( '<Key>' )
        w.update_idletasks()
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.149:moveword (used by many entires)  TO DO: split into forward/backward versions
    #@-node:ekr.20050920084036.146:Utilities
    #@-others
#@nonl
#@-node:ekr.20050920084036.53:class editCommandsClass
#@+node:ekr.20050920084036.150:class controlCommandsClass
class controlCommandsClass (baseEditCommandsClass):
    
    #@    @+others
    #@+node:ekr.20050920084036.151: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.shutdownhook = None # If this is set via setShutdownHook, it is executed instead of sys.exit on Control-x Control-c.
        self.shuttingdown = False # Indicates that the Emacs instance is shutting down and no work needs to be done.
    #@nonl
    #@-node:ekr.20050920084036.151: ctor
    #@+node:ekr.20050920084036.152: getPublicCommands
    def getPublicCommands (self):
        
        k = self
        
        if 1:
            return {
                'advertised-undo':              self.advertizedUndo,
                'iconfify-or-deiconify-frame':  self.iconifyOrDeiconifyFrame,
                'keyboard-quit':                self.keyboardQuit,
                'save-buffers-kill-emacs':      self.saveBuffersKillEmacs,
                'shell-command':                self.startSubprocess,
                'shell-command-on-region':      self.shellCommandOnRegion,
                'suspend':                      self.suspend,
            }
            
        else: # old
    
            return {
                'advertised-undo':              lambda event: self.doUndo( event ) and k.keyboardQuit( event ),
                'iconfify-or-deiconify-frame':  lambda event: self.suspend( event ) and k.keyboardQuit( event ),
                'keyboard-quit':                k.keyboardQuit,
                'save-buffers-kill-emacs':      lambda event: k.keyboardQuit( event ) and self.shutdown( event ),
                'shell-command':                self.startSubprocess,
                'shell-command-on-region':      lambda event: self.startSubprocess( event, which=1 ),
                
                # Added by ekr.
                'suspend':                      lambda event: self.suspend( event ) and k.keyboardQuit( event ),
            }
    #@nonl
    #@-node:ekr.20050920084036.152: getPublicCommands
    #@+node:ekr.20050922110030:Entry points
    def advertizedUndo (self,event):
        return self.doUndo(event) and self.k.keyboardQuit(event)
    
    def iconifyOrDeiconifyFrame (self,event):
        return self._suspend(event) and self.k.keyboardQuit(event)
    
    def keyboardQuit (self,event):
        return self.k.keyboardQuite(event)
    
    def saveBuffersKillEmacs (self,event):
        return self.k.keyboardQuit(event) and self.shutdown(event)
    
    def shellCommandOnRegion (self,event):
        return self.startSubprocess(event,which=1)
    
    def suspend (self,event):
        return self._suspend(event) and self.k.keyboardQuit(event)
    #@-node:ekr.20050922110030:Entry points
    #@+node:ekr.20050920084036.153:_suspend
    def _suspend( self, event ):
        
        widget = event.widget
        widget.winfo_toplevel().iconify()
    #@nonl
    #@-node:ekr.20050920084036.153:_suspend
    #@+node:ekr.20050920084036.154:shutdown methods
    #@+node:ekr.20050920084036.155:shutdown
    def shutdown( self, event ):
        
        self.shuttingdown = True
    
        if self.shutdownhook:
            self.shutdownhook()
        else:
            sys.exit( 0 )
    #@nonl
    #@-node:ekr.20050920084036.155:shutdown
    #@+node:ekr.20050920084036.156:setShutdownHook
    def setShutdownHook( self, hook ):
            
        self.shutdownhook = hook
    #@nonl
    #@-node:ekr.20050920084036.156:setShutdownHook
    #@-node:ekr.20050920084036.154:shutdown methods
    #@+node:ekr.20050920084036.157:subprocess
    #@+node:ekr.20050920084036.158:startSubprocess
    def startSubprocess (self,event,which=0):
    
        k = self.k ; w = event.widget
        statecontents = {'state': 'start', 'payload': None}
    
        k.setState('subprocess',statecontents)
    
        if which:
            k.setLabelBlue('Shell command on region:')
            is1 = is2 = None
            try:
                is1 = w.index('sel.first')
                is2 = w.index('sel.last')
            finally:
                if is1:
                    statecontents ['payload'] = w.get(is1,is2)
                    k.setState('subprocess',statecontents)
                else:
                    return k.keyboardQuit(event)
        else:
            k.setLabelBlue("Alt - !:")
    
        return 'break'
    #@-node:ekr.20050920084036.158:startSubprocess
    #@+node:ekr.20050920084036.159:subprocess
    def subprocesser (self,event):
    
        k = self.k
        state = k.getState('subprocess')
    
        if state ['state'] == 'start':
            state ['state'] = 'watching'
            k.setLabel('')
    
        if event.keysym == "Return":
            cmdline = k.getLabel()
            return self.executeSubprocess(event,cmdline,input=state['payload'])
        else:
            k.updateLabel(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.159:subprocess
    #@+node:ekr.20050920084036.160:executeSubprocess
    def executeSubprocess (self,event,command,input=None):
        k = self.k
        try:
            try:
                out, err = os.tmpnam(), os.tmpnam()
                ofile = open(out,'wt+')
                efile = open(err,'wt+')
                process = subprocess.Popen(command,bufsize=-1,
                    stdout = ofile.fileno(), stderr = ofile.fileno(),
                    stdin = subprocess.PIPE, shell = True)
                if input:
                    process.communicate(input)
                process.wait()
                w = event.widget
                efile.seek(0)
                errinfo = efile.read()
                if errinfo:
                    w.insert('insert',errinfo)
                ofile.seek(0)
                okout = ofile.read()
                if okout:
                    w.insert('insert',okout)
            except Exception, x:
                w = event.widget
                w.insert('insert',x)
        finally:
            os.remove(out)
            os.remove(err)
        k.keyboardQuit(event)
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.160:executeSubprocess
    #@-node:ekr.20050920084036.157:subprocess
    #@-others
#@nonl
#@-node:ekr.20050920084036.150:class controlCommandsClass
#@+node:ekr.20050920084036.161:class editFileCommandsClass
class editFileCommandsClass (baseEditCommandsClass):
    
    '''A class to load files into buffers and save buffers to files.'''
    
    #@    @+others
    #@+node:ekr.20050920084036.162: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
    #@nonl
    #@-node:ekr.20050920084036.162: ctor
    #@+node:ekr.20050920084036.163: getPublicCommands
    def getPublicCommands (self):
        
        k = self.k
    
        return {
            'delete-file':      self.deleteFile,
            'diff':             self.diff, 
            'insert-file':      lambda event: self.insertFile( event ) and k.keyboardQuit( event ),
            'make-directory':   self.makeDirectory,
            'remove-directory': self.removeDirectory,
            'save-file':        self.saveFile
        }
    #@nonl
    #@-node:ekr.20050920084036.163: getPublicCommands
    #@+node:ekr.20050920084036.164:deleteFile
    def deleteFile (self,event):
    
        k = self.k ; state = k.getState('delete_file')
    
        if state == 0:
            prefix = 'Remove File: '
            k.setLabelBlue('%s%s%s' % (prefix,os.getcwd(),os.sep))
            k.getArg(event,'delete_file',1,
                returnStateHandler=self.deleteFile,prefix=prefix)
        else:
            k.keyboardQuit(event)
            k.clearState()
            try:
                os.remove(k.arg)
                k.setLabel('deleted %s' % k.arg)
            except:
                k.setLabel('deleted not delete %s' % k.arg)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.164:deleteFile
    #@+node:ekr.20050920084036.165:diff
    def diff( self, event ):
        
        '''the diff command, accessed by Alt-x diff.
        Creates a buffer and puts the diff between 2 files into it.'''
        
        k = self.k ; w = event.widget
    
        try:
            f, name = self.getReadableTextFile()
            txt1 = f.read()
            f.close()
            
            f2, name2 = self.getReadableTextFile()
            txt2 = f2.read()
            f2.close()
        except:
            return k.keyboardQuit( event )
    
        self.switchToBuffer( event, "*diff* of ( %s , %s )" %( name, name2 ) )
        data = difflib.ndiff( txt1, txt2 )
        idata = []
        for z in data:
            idata.append( z )
        w.delete( '1.0', 'end' )
        w.insert( '1.0', ''.join( idata ) )
        k._tailEnd( w )
    
        return k.keyboardQuit( event )
    #@-node:ekr.20050920084036.165:diff
    #@+node:ekr.20050920084036.166:getReadableFile
    def getReadableTextFile( self ):
        
        fname = tkFileDialog.askopenfilename()
        if fname == None: return None, None
        f = open( fname, 'rt' )
        return f, fname
    #@nonl
    #@-node:ekr.20050920084036.166:getReadableFile
    #@+node:ekr.20050920084036.167:insertFile
    def insertFile (self,event):
    
        k = self.k ; w = event.widget
        f, name = self.getReadableTextFile()
        if not f: return None
        txt = f.read()
        f.close()
        w.insert('insert',txt)
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.167:insertFile
    #@+node:ekr.20050920084036.168:makeDirectory
    def makeDirectory (self,event):
    
        k = self.k ; state = k.getState('make_directory')
    
        if state == 0:
            prefix = 'Make Directory: '
            k.setLabelBlue('%s%s%s' % (prefix,os.getcwd(),os.sep))
            k.getArg(event,'make_directory',1,
                returnStateHandler=self.makeDirectory,prefix=prefix)
        else:
            k.keyboardQuit(event)
            k.clearState()
            try:
                os.mkdir(k.arg)
                k.setLabel("created %s" % k.arg)
            except:
                k.setLabel("can not create %s" % k.arg)
                
        return 'break'
    #@-node:ekr.20050920084036.168:makeDirectory
    #@+node:ekr.20050920084036.169:removeDirectory
    def removeDirectory (self,event):
    
        k = self.k ; state = k.getState('remove_directory')
    
        if state == 0:
            prefix = 'Remove Directory: '
            k.setLabelBlue('%s%s%s' % (prefix,os.getcwd(),os.sep))
            k.getArg(event,'remove_directory',1,
                returnStateHandler=self.removeDirectory,prefix=prefix)
        else:
            k.keyboardQuit(event)
            k.clearState()
            try:
                os.rmdir(k.arg)
                k.setLabel('removed %s' % k.arg)
            except:
                k.setLabel('Can not remove %s' % k.arg)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.169:removeDirectory
    #@+node:ekr.20050920084036.170:saveFile
    def saveFile( self, event ):
    
        w = event.widget
        txt = w.get( '1.0', 'end' )
        f = tkFileDialog.asksaveasfile()
        if f:
            f.write( txt )
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
    #@-node:ekr.20050920084036.172: ctor
    #@+node:ekr.20050920084036.173:getPublicCommands
    def getPublicCommands (self):
        
        return {
            'digit-argument':           self.digitArgument,
            'repeat-complex-command':   self.repeatComplexCommand,
            'universal-argument':       self.universalArgument,
        }
    #@nonl
    #@-node:ekr.20050920084036.173:getPublicCommands
    #@+node:ekr.20050922110452:Entry points
    def digitArgument (self,event):
        return self.k.digitArgument(event)
    
    def repeatComplexCommand (self,event):
        return self.k.repeatComplexCommand(event)
    
    def universalArgument (self,event):
        return self.k.universalArgument(event)
    #@nonl
    #@-node:ekr.20050922110452:Entry points
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
    
        self.killbuffer = [] # May be changed in finishCreate.
        self.kbiterator = self.iterateKillBuffer()
        self.last_clipboard = None # For interacting with system clipboard.
        self.reset = False 
    
    def finishCreate (self):
        
        baseEditCommandsClass.finishCreate(self)
            # Call the base finishCreate.
            # This sets self.k
        
        if self.k.useGlobalKillbuffer:
            self.killbuffer = leoKeys.keyHandlerClass.global_killbuffer
    #@nonl
    #@-node:ekr.20050920084036.175: ctor & finishCreate
    #@+node:ekr.20050920084036.176:getPublicCommands
    def getPublicCommands (self):
        
        return {
            'backward-kill-sentence':   self.backwardKillSentence,
            'backward-kill-word':       self.backwardKillWord,
            'kill-line':                self.killLine,
            'kill-word':                self.killWord,
            'kill-sentence':            self.killSentence,
            'kill-region':              self.killRegion,
            'yank':                     self.yank,
            'yank-pop':                 self.yankPop,
            'zap-to-character':         self.zapToCharacter,
        }
    #@nonl
    #@-node:ekr.20050920084036.176:getPublicCommands
    #@+node:ekr.20050920084036.177:Entry points
    # backwardKillParagraph is in paragraph class.
    
    def backwardKillSentence (self,event):
        return self.k.keyboardQuit(event) and self._killSentence(event,back=True)
        
    def backwardKillWord (self,event):
        return self.deletelastWord(event) and self.k.keyboardQuit(event)
        
    def killLine (self,event):
        self.kill(event,frm='insert',to='insert lineend') and self.k.keyboardQuit(event)
        
    def killRegion (self,event):
        return self._killRegion(event,which='d') and self.k.keyboardQuit(event)
        
    # killParagraph is in paragraph class.
    
    def killSentence (self,event):
        return self.killsentence(event) and self.k.keyboardQuit(event)
        
    def killWord (self,event):
        return self.kill(event,frm='insert wordstart',to='insert wordend') and self.k.keyboardQuit(event)
        
    def yank (self,event):
        return self.walkKB(event,frm='insert',which='c') and self.k.keyboardQuit(event)
        
    def yankPop (self,event):
        return self.walkKB(event,frm="insert",which='a') and self.k.keyboardQuit(event)
    #@nonl
    #@-node:ekr.20050920084036.177:Entry points
    #@+node:ekr.20050920084036.178:kill
    def kill( self, event, frm, to  ):
    
        k = self.k ; w = event.widget
        text = w.get( frm, to )
        self.addToKillBuffer( text )
        w.clipboard_clear()
        w.clipboard_append( text )   
     
        if frm == 'insert' and to =='insert lineend' and w.index( frm ) == w.index( to ):
            w.delete( 'insert', 'insert lineend +1c' )
            self.addToKillBuffer( '\n' )
        else:
            w.delete( frm, to )
    
        return k._tailEnd( w )
    #@nonl
    #@-node:ekr.20050920084036.178:kill
    #@+node:ekr.20050920084036.179:walkKB
    def walkKB( self, event, frm, which ):# kb = self.iterateKillBuffer() ):
    
        k = self.k ; w = event.widget
        i = w.index( 'insert' )
        t , t1 = i.split( '.' )
        clip_text = self.getClipboard( w )    
        if self.killbuffer or clip_text:
            if which == 'c':
                self.reset = True
                if clip_text:
                    txt = clip_text
                else:
                    txt = self.kbiterator.next()
                w.tag_delete( 'kb' )
                w.insert( frm, txt, ('kb') )
                w.mark_set( 'insert', i )
            else:
                if clip_text:
                    txt = clip_text
                else:
                    txt = self.kbiterator.next()
                t1 = str( int( t1 ) + len( txt ) )
                r = w.tag_ranges( 'kb' )
                if r and r[ 0 ] == i:
                    w.delete( r[ 0 ], r[ -1 ] )
                w.tag_delete( 'kb' )
                w.insert( frm, txt, ('kb') )
                w.mark_set( 'insert', i )
        return k._tailEnd( w )
    #@nonl
    #@-node:ekr.20050920084036.179:walkKB
    #@+node:ekr.20050920084036.180:deletelastWord
    def deletelastWord( self, event ):
        
        self.editCommands.moveword( event, -1 )
        self.kill( event, 'insert', 'insert wordend')
        self.editCommands.moveword( event ,1 )
        return 'break'
    #@-node:ekr.20050920084036.180:deletelastWord
    #@+node:ekr.20050920084036.181:_killSentence
    def killsentence( self, event, back = False ):
        w = event.widget
        i = w.search( '.' , 'insert', stopindex = 'end' )
        if back:
            i = w.search( '.' , 'insert', backwards = True, stopindex = '1.0' ) 
            if i == '':
                return 'break'
            i2 = w.search( '.' , i, backwards = True , stopindex = '1.0' )
            if i2 == '':
                i2 = '1.0'
            return self.kill( event, i2, '%s + 1c' % i )
            #return self.kill( event , '%s +1c' % i, 'insert' )
        else:
            i = w.search( '.' , 'insert', stopindex = 'end' )
            i2 = w.search( '.', 'insert', backwards = True, stopindex = '1.0' )
        if i2 == '':
           i2 = '1.0'
        else:
           i2 = i2 + ' + 1c '
        if i == '': return 'break'
        return self.kill( event, i2, '%s + 1c' % i )
    #@nonl
    #@-node:ekr.20050920084036.181:_killSentence
    #@+node:ekr.20050920084036.182:_killRegion
    def killRegion( self, event, which ):
        mrk = 'sel'
        w = event.widget
        trange = w.tag_ranges( mrk )
        if len( trange ) != 0:
            txt = w.get( trange[ 0 ] , trange[ -1 ] )
            if which == 'd':
                w.delete( trange[ 0 ], trange[ -1 ] )   
            self.addToKillBuffer( txt )
            w.clipboard_clear()
            w.clipboard_append( txt )
        self.removeRKeys( w )
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.182:_killRegion
    #@+node:ekr.20050920084036.183:addToKillBuffer
    def addToKillBuffer( self, text ):
        
        k = self.k
        self.reset = True 
        
        if (
            k.previousStroke in (
                '<Control-k>', '<Control-w>' ,
                '<Alt-d>', '<Alt-Delete', '<Alt-z>', '<Delete>',
                '<Control-Alt-w>' )
            and len(self.killbuffer)
        ):
            self.killbuffer[ 0 ] = self.killbuffer[ 0 ] + text
            return
    
        self.killbuffer.insert( 0, text )
    #@nonl
    #@-node:ekr.20050920084036.183:addToKillBuffer
    #@+node:ekr.20050920084036.184:iterateKillBuffer
    def iterateKillBuffer( self ):
        
        while 1:
            if self.killbuffer:
                self.last_clipboard = None
                for z in self.killbuffer:
                    if self.reset:
                        self.reset = False
                        break        
                    yield z
    #@-node:ekr.20050920084036.184:iterateKillBuffer
    #@+node:ekr.20050920084036.185:getClipboard
    def getClipboard (self,w):
    
        try:
            ctxt = w.selection_get(selection='CLIPBOARD')
            if not self.killbuffer or ctxt != self.last_clipboard:
                self.last_clipboard = ctxt
                if not self.killbuffer or self.killbuffer [0] != ctxt:
                    return ctxt
        except: pass
    
        return None
    #@nonl
    #@-node:ekr.20050920084036.185:getClipboard
    #@+node:ekr.20050920084036.128:zapToCharacter
    def zapToCharacter (self,event):
    
        k = self.k ; state = k.getState('zapToCharacter')
    
        if state == 0:
            k.setState('zapToCharacter',1,handler=self.zapToCharacter)
            k.setLabelBlue('Zap To Character: ')
        else:
            c = k.c ; w = event.widget ; ch = event.char
            if (
                len(event.char) != 0 and
                ch in (string.ascii_letters + string.digits + string.punctuation)
            ):
                k.setState('zap',0)
                i = w.search(ch,'insert',stopindex='end')
                if i:
                    t = w.get('insert','%s+1c' % i)
                    self.addToKillBuffer(t)
                    w.delete('insert','%s+1c' % i)
                    k.resetLabel()
                    k.clearState()
    
        return 'break'
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
    #@+node:ekr.20050920084036.188:getPublicCommands
    def getPublicCommands (self):
        
        leoCommandsDict = {}
        
        #@    << define dictionary d of names and Leo commands >>
        #@+node:ekr.20050920084036.189:<< define dictionary d of names and Leo commands >>
        c = self.c ; f = c.frame
        
        d = {
            'new':                  c.new,
            'open':                 c.open,
            'openWith':             c.openWith,
            'close':                c.close,
            'save':                 c.save,
            'saveAs':               c.saveAs,
            'saveTo':               c.saveTo,
            'revert':               c.revert,
            'readOutlineOnly':      c.readOutlineOnly,
            'readAtFileNodes':      c.readAtFileNodes,
            'importDerivedFile':    c.importDerivedFile,
            #'writeNewDerivedFiles': c.writeNewDerivedFiles,
            #'writeOldDerivedFiles': c.writeOldDerivedFiles,
            'tangle':               c.tangle,
            'tangle all':           c.tangleAll,
            'tangle marked':        c.tangleMarked,
            'untangle':             c.untangle,
            'untangle all':         c.untangleAll,
            'untangle marked':      c.untangleMarked,
            'export headlines':     c.exportHeadlines,
            'flatten outline':      c.flattenOutline,
            'import AtRoot':        c.importAtRoot,
            'import AtFile':        c.importAtFile,
            'import CWEB Files':    c.importCWEBFiles,
            'import Flattened Outline': c.importFlattenedOutline,
            'import Noweb Files':   c.importNowebFiles,
            'outline to Noweb':     c.outlineToNoweb,
            'outline to CWEB':      c.outlineToCWEB,
            'remove sentinels':     c.removeSentinels,
            'weave':                c.weave,
            'delete':               c.delete,
            'execute script':       c.executeScript,
            'go to line number':    c.goToLineNumber,
            'set font':             c.fontPanel,
            'set colors':           c.colorPanel,
            'show invisibles':      c.viewAllCharacters,
            'preferences':          c.preferences,
            'convert all blanks':   c.convertAllBlanks,
            'convert all tabs':     c.convertAllTabs,
            'convert blanks':       c.convertBlanks,
            'convert tabs':         c.convertTabs,
            'indent':               c.indentBody,
            'unindent':             c.dedentBody,
            'reformat paragraph':   c.reformatParagraph,
            'insert time':          c.insertBodyTime,
            'extract section':      c.extractSection,
            'extract names':        c.extractSectionNames,
            'extract':              c.extract,
            'match bracket':        c.findMatchingBracket,
            'find panel':           c.showFindPanel, ## c.findPanel,
            'find next':            c.findNext,
            'find previous':        c.findPrevious,
            'replace':              c.replace,
            'replace then find':    c.replaceThenFind,
            'edit headline':        c.editHeadline,
            'toggle angle brackets': c.toggleAngleBrackets,
            'cut node':             c.cutOutline,
            'copy node':            c.copyOutline,
            'paste node':           c.pasteOutline,
            'paste retaining clone': c.pasteOutlineRetainingClones,
            'hoist':                c.hoist,
            'de-hoist':             c.dehoist,
            'insert node':          c.insertHeadline,
            'clone node':           c.clone,
            'delete node':          c.deleteOutline,
            'sort children':        c.sortChildren,
            'sort siblings':        c.sortSiblings,
            'demote':               c.demote,
            'promote':              c.promote,
            'move right':           c.moveOutlineRight,
            'move left':            c.moveOutlineLeft,
            'move up':              c.moveOutlineUp,
            'move down':            c.moveOutlineDown,
            'unmark all':           c.unmarkAll,
            'mark clones':          c.markClones,
            'mark':                 c.markHeadline,
            'mark subheads':        c.markSubheads,
            'mark changed items':   c.markChangedHeadlines,
            'mark changed roots':   c.markChangedRoots,
            'contract all':         c.contractAllHeadlines,
            'contract node':        c.contractNode,
            'contract parent':      c.contractParent,
            'expand to level 1':    c.expandLevel1,
            'expand to level 2':    c.expandLevel2,
            'expand to level 3':    c.expandLevel3,
            'expand to level 4':    c.expandLevel4,
            'expand to level 5':    c.expandLevel5,
            'expand to level 6':    c.expandLevel6,
            'expand to level 7':    c.expandLevel7,
            'expand to level 8':    c.expandLevel8,
            'expand to level 9':    c.expandLevel9,
            'expand prev level':    c.expandPrevLevel,
            'expand next level':    c.expandNextLevel,
            'expand all':           c.expandAllHeadlines,
            'expand node':          c.expandNode,
            'check outline':        c.checkOutline,
            'dump outline':         c.dumpOutline,
            'check python code':    c.checkPythonCode,
            'check all python code': c.checkAllPythonCode,
            'pretty print python code': c.prettyPrintPythonCode,
            'pretty print all python code': c.prettyPrintAllPythonCode,
            'goto parent':          c.goToParent,
            'goto next sibling':    c.goToNextSibling,
            'goto previous sibling': c.goToPrevSibling,
            'goto next clone':      c.goToNextClone,
            'goto next marked':     c.goToNextMarkedHeadline,
            'goto next changed':    c.goToNextDirtyHeadline,
            'goto first':           c.goToFirstNode,
            'goto last':            c.goToLastNode,
            "go to prev visible":   c.selectVisBack,
            "go to next visible":   c.selectVisNext,
            "go to prev node":      c.selectThreadBack,
            "go to next node":      c.selectThreadNext,
            'about leo...':         c.about,
            #'apply settings':      c.applyConfig,
            'open LeoConfig.leo':   c.leoConfig,
            'open LeoDocs.leo':     c.leoDocumentation,
            'open online home':     c.leoHome,
            'open online tutorial': c.leoTutorial,
            'open compare window':  c.openCompareWindow,
            'open Python window':   c.openPythonWindow,
            "equal sized panes":    f.equalSizedPanes,
            "toggle active pane":   f.toggleActivePane,
            "toggle split direction": f.toggleSplitDirection,
            "resize to screen":     f.resizeToScreen,
            "cascade":              f.cascade,
            "minimize all":         f.minimizeAll,
        }
        #@nonl
        #@-node:ekr.20050920084036.189:<< define dictionary d of names and Leo commands >>
        #@nl
        
        # Create a callback for each item in d.
        for key in d.keys():
            f = d.get(key)
            def leoCallback (event,f=f):
                f()
            leoCommandsDict [key] = leoCallback
            ### To do: not all these keys are valid Python function names.
            setattr(self,key,f) # Make the key available.
            
        return leoCommandsDict
    #@nonl
    #@-node:ekr.20050920084036.188:getPublicCommands
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
        self.macroing = False
    #@nonl
    #@-node:ekr.20050920084036.191: ctor
    #@+node:ekr.20050920084036.192: getPublicCommands
    def getPublicCommands (self):
    
        return {
            'name-last-kbd-macro':      self.nameLastMacro,
            'load-file':                self.loadMacros,
            'insert-keyboard-macro' :   self.getMacroName,
        }
    #@nonl
    #@-node:ekr.20050920084036.192: getPublicCommands
    #@+node:ekr.20050920084036.193:Entry points
    #@+node:ekr.20050920084036.194:getMacroName (calls saveMacros)
    def getMacroName (self,event):
    
        '''A method to save your macros to file.'''
    
        k = self.k
    
        if not self.macroing:
            self.macroing = 3
            k.setLabelBlue('')
        elif event.keysym == 'Return':
            self.macroing = False
            self.saveMacros(event,k.getLabel()) 
        elif event.keysym == 'Tab':
            s = k.getLabel()
            k.setLabel(self.findFirstMatchFromList(s,self.namedMacros))
        else:
            k.updateLabel(event)
    
        return 'break'
    #@nonl
    #@+node:ekr.20050920084036.195:findFirstMatchFromList
    def findFirstMatchFromList (self,s,aList=None):
    
        '''This method finds the first match it can find in a sorted list'''
    
        k = self.k
    
        if alist is not None:
            aList = c.commandsDict.keys()
    
        pmatches = [item for item in aList if item.startswith(s)]
        pmatches.sort()
        if pmatches:
            mstring = reduce(g.longestCommonPrefix,pmatches)
            return mstring
    
        return s
    #@nonl
    #@-node:ekr.20050920084036.195:findFirstMatchFromList
    #@-node:ekr.20050920084036.194:getMacroName (calls saveMacros)
    #@+node:ekr.20050920084036.196:loadMacros & helpers
    def loadMacros (self,event):
    
        '''Asks for a macro file name to load.'''
    
        f = tkFileDialog.askopenfile()
    
        if f:
            return self._loadMacros(f)
        else:
            return 'break'
    #@nonl
    #@+node:ekr.20050920084036.197:_loadMacros
    def _loadMacros( self, f ):
    
        '''Loads a macro file into the macros dictionary.'''
    
        k = self.k
        macros = cPickle.load( f )
        for z in macros:
            k.addToDoAltX( z, macros[ z ] )
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.197:_loadMacros
    #@-node:ekr.20050920084036.196:loadMacros & helpers
    #@+node:ekr.20050920084036.198:nameLastMacro
    def nameLastMacro (self,event):
    
        '''Names the last macro defined.'''
    
        k = self.k
    
        if not self.macroing:
            self.macroing = 2
            k.setLabelBlue('')
        elif event.keysym == 'Return':
            name = k.getLabel()
            k.addToDoAltX(name,self.lastMacro)
            k.setLabelBlue('')
            self.macroing = False
            k.stopControlX(event)
        else:
            k.updateLabel(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.198:nameLastMacro
    #@+node:ekr.20050920084036.199:saveMacros & helper
    def saveMacros( self, event, macname ):
        
        '''Asks for a file name and saves it.'''
    
        name = tkFileDialog.asksaveasfilename()
        if name:
            f = file( name, 'a+' )
            f.seek( 0 )
            if f:
                self._saveMacros( f, macname )
    
        return 'break'
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
    #@-node:ekr.20050920084036.193:Entry points
    #@+node:ekr.20050920084036.201:Called from keystroke handlers
    #@+node:ekr.20050920084036.202:executeLastMacro & helper (called from universal command)
    def executeLastMacro( self, event ):
    
        w = event.widget
        if self.lastMacro:
            return self._executeMacro( self.lastMacro, w )
        return 'break'
    #@nonl
    #@+node:ekr.20050920084036.203:_executeMacro
    def _executeMacro( self, macro, w ):
        
        k = self.k
        
        for z in macro:
            if len( z ) == 2:
                w.event_generate( '<Key>', keycode = z[ 0 ], keysym = z[ 1 ] ) 
            else:
                meth = z[ 0 ].lstrip( '<' ).rstrip( '>' )
                method = self.cbDict[ meth ]
                ev = Tk.Event()
                ev.widget = w
                ev.keycode = z[ 1 ]
                ev.keysym = z[ 2 ]
                ev.char = z[ 3 ]
                self.masterCommand( ev , method, '<%s>' % meth )
    
        return k._tailEnd( w )
    #@nonl
    #@-node:ekr.20050920084036.203:_executeMacro
    #@-node:ekr.20050920084036.202:executeLastMacro & helper (called from universal command)
    #@+node:ekr.20050920084036.204:startKBDMacro
    def startKBDMacro( self, event ):
    
        k = self.k
    
        k.setLabelBlue('Recording Keyboard Macro')
        self.macroing = True
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.204:startKBDMacro
    #@+node:ekr.20050920084036.205:recordKBDMacro
    def recordKBDMacro( self, event ):
        
        k = self.k ; stroke = k.stroke
        
        if stroke != '<Key>':
            self.macro.append( (stroke, event.keycode, event.keysym, event.char) )
        elif stroke == '<Key>':
            if event.keysym != '??':
                self.macro.append( ( event.keycode, event.keysym ) )
    #@nonl
    #@-node:ekr.20050920084036.205:recordKBDMacro
    #@+node:ekr.20050920084036.206:stopKBDMacro
    def stopKBDMacro (self,event):
    
        k = self.k
    
        if self.macro:
            self.macro = self.macro [: -4]
            self.macs.insert(0,self.macro)
            self.lastMacro = self.macro
            self.macro = []
    
        self.macroing = False
        k.setLabelBlue('Keyboard macro defined')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.206:stopKBDMacro
    #@-node:ekr.20050920084036.201:Called from keystroke handlers
    #@-others
#@nonl
#@-node:ekr.20050920084036.190:class macroCommandsClass
#@+node:ekr.20050920084036.207:class queryReplaceCommandsClass
class queryReplaceCommandsClass (baseEditCommandsClass):
    
    '''A class to handle query replace commands.'''

    #@    @+others
    #@+node:ekr.20050920084036.208: ctor
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.qQ = None
        self.qR = None
        self.qgetQuery = False
        self.qgetReplace = False
        self.qrexecute = False
        self.querytype = 'normal'
    #@nonl
    #@-node:ekr.20050920084036.208: ctor
    #@+node:ekr.20050920084036.209: getPublicCommands
    def getPublicCommands (self):
    
        return {
            'query-replace':                self.queryReplace,
            'query-replace-regex':          self.queryReplaceRegex,
            'inverse-add-global-abbrev':    self.inverseAddGlobalAbbrev,
        }
    #@nonl
    #@-node:ekr.20050920084036.209: getPublicCommands
    #@+node:ekr.20050920084036.210:Entry points
    def queryReplace (self,event):
        return self.masterQR(event)
    
    def queryReplaceRegex (self,event):
        return self.startRegexReplace() and self.masterQR(event)
    
    def inverseAddGlobalAbbrev (self,event):
        return self.abbreviationDispatch(event,2)
    #@nonl
    #@-node:ekr.20050920084036.210:Entry points
    #@+node:ekr.20050920084036.211:qreplace
    def qreplace( self, event ):
    
        if event.keysym == 'y':
            self._qreplace( event )
            return
        elif event.keysym in ( 'q', 'Return' ):
            self.quitQSearch( event )
        elif event.keysym == 'exclam':
            while self.qrexecute:
                self._qreplace( event )
        elif event.keysym in ( 'n', 'Delete'):
            #i = event.widget.index( 'insert' )
            event.widget.mark_set( 'insert', 'insert +%sc' % len( self.qQ ) )
            self.qsearch( event )
    
        event.widget.see( 'insert' )
    #@nonl
    #@-node:ekr.20050920084036.211:qreplace
    #@+node:ekr.20050920084036.212:_qreplace
    def _qreplace( self, event ):
        
        i = event.widget.tag_ranges( 'qR' )
        event.widget.delete( i[ 0 ], i[ 1 ] )
        event.widget.insert( 'insert', self.qR )
        self.qsearch( event )
    #@-node:ekr.20050920084036.212:_qreplace
    #@+node:ekr.20050920084036.213:getQuery
    def getQuery (self,event):
    
        k = self.k
    
        if event.keysym == 'Return':
            self.qgetQuery = False
            self.qgetReplace = True
            self.qQ = k.getLabel()
            k.setLabel("Replace with:")
            k.setState('qlisten','replace-caption')
            return
    
        if k.getState('qlisten') == 'replace-caption':
            k.setLabel('')
            k.setState('qlisten',1)
    
        k.updateLabel(event)
    #@nonl
    #@-node:ekr.20050920084036.213:getQuery
    #@+node:ekr.20050920084036.214:getReplace
    def getReplace (self,event):
    
        k = self.k ; w = event.widget
        prompt = 'Replace %s with %s y/n(! for all )'
    
        if event.keysym == 'Return':
            self.qgetReplace = False
            self.qR = k.getLabel()
            self.qrexecute = True
            ok = self.qsearch(event)
            if self.querytype == 'regex' and ok:
                range = w.tag_ranges('qR')
                s = w.get(range[0],range[1])
                k.setLabel(prompt % (s,self.qR))
            elif ok:
                k.setLabel(prompt % (self.qQ,self.qR))
            return
    
        if k.getState('qlisten') == 'replace-caption':
            k.setLabel('')
            k.setState('qlisten',1)
    
        k.updateLabel(event)
    #@nonl
    #@-node:ekr.20050920084036.214:getReplace
    #@+node:ekr.20050920084036.215:masterQR
    def masterQR (self,event):
    
        if self.qgetQuery:
            self.getQuery(event)
        elif self.qgetReplace:
            self.getReplace(event)
        elif self.qrexecute:
            self.qreplace(event)
        else:
            self.listenQR(event)
    
        return 'break'
    #@-node:ekr.20050920084036.215:masterQR
    #@+node:ekr.20050920084036.216:startRegexReplace
    def startRegexReplace( self ):
        
        self.querytype = 'regex'
        return True
    #@nonl
    #@-node:ekr.20050920084036.216:startRegexReplace
    #@+node:ekr.20050920084036.217:query search methods
    #@+others
    #@+node:ekr.20050920084036.218:listenQR
    def listenQR (self,event):
    
        k = self.k
    
        k.setState('qlisten','replace-caption')
        k.setLabelBlue(
            g.choose(self.querytype=='regex',
                'Regex Query with:','Query with:'))
    
        self.qgetQuery = True
    #@nonl
    #@-node:ekr.20050920084036.218:listenQR
    #@+node:ekr.20050920084036.219:qsearch
    def qsearch( self, event ):
        
        k = self.k ; w = event.widget
        if self.qQ:
            w.tag_delete( 'qR' )
            if self.querytype == 'regex':
                try:
                    regex = re.compile( self.qQ )
                except:
                    k.keyboardQuit( event )
                    k.setLabel( "Illegal regular expression" )
                txt = w.get( 'insert', 'end' )
                match = regex.search( txt )
                if match:
                    start = match.start()
                    end = match.end()
                    length = end - start
                    w.mark_set( 'insert', 'insert +%sc' % start )
                    w.update_idletasks()
                    w.tag_add( 'qR', 'insert', 'insert +%sc' % length )
                    w.tag_config( 'qR', background = 'lightblue' )
                    txt = w.get( 'insert', 'insert +%sc' % length )
                    k.setLabel( "Replace %s with %s? y/n(! for all )" % ( txt, self.qR ) )
                    return True
            else:
                i = w.search( self.qQ, 'insert', stopindex = 'end' )
                if i:
                    w.mark_set( 'insert', i )
                    w.update_idletasks()
                    w.tag_add( 'qR', 'insert', 'insert +%sc'% len( self.qQ ) )
                    w.tag_config( 'qR', background = 'lightblue' )
                    k._tailEnd( w )
                    return True
            self.quitQSearch( event )
            return False
    #@-node:ekr.20050920084036.219:qsearch
    #@+node:ekr.20050920084036.220:quitQSearch
    def quitQSearch (self,event):
    
        k = self.k ; w = event.widget
    
        w.tag_delete('qR')
        self.qQ = None
        self.qR = None
        k.setState('qlisten',0)
        self.qrexecute = False
        k.setLabelGrey('')
        self.querytype = 'normal'
        k._tailEnd(event.widget)
    #@nonl
    #@-node:ekr.20050920084036.220:quitQSearch
    #@-others
    #@nonl
    #@-node:ekr.20050920084036.217:query search methods
    #@-others
#@nonl
#@-node:ekr.20050920084036.207:class queryReplaceCommandsClass
#@+node:ekr.20050920084036.221:class rectangleCommandsClass
class rectangleCommandsClass (baseEditCommandsClass):

    #@    @+others
    #@+node:ekr.20050920084036.222: ctor & init
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
    def init (self):
        
        self.sRect = False # State indicating string rectangle.  May be moved to stateManagerClass
        self.krectangle = None # The kill rectangle
        self.rectanglemode = False # Determines what state the rectangle system is in.
    #@nonl
    #@-node:ekr.20050920084036.222: ctor & init
    #@+node:ekr.20050920084036.223:getPublicCommands
    def getPublicCommands (self):
    
        return {
            'clear-rectangle':  self.clearRectangle,
            'close-rectangle':  self.closeRectangle,
            'delete-rectangle': self.deleteRectangle,
            'kill-rectangle':   self.killRectangle,
            'open-rectangle':   self.openRectangle,
            'yank-rectangle':   self.yankRectangle,
        }
    #@nonl
    #@-node:ekr.20050920084036.223:getPublicCommands
    #@+node:ekr.20050920084036.224:Entry points
    #@+node:ekr.20050920084036.225:clearRectangle
    def clearRectangle( self, event ):
        
        if not self._chckSel( event ):
            return
    
        k = self.k ; w = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        lth = ' ' * ( r4 - r2 )
        self.stopControlX( event )
        while r1 <= r3:
            w.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
            w.insert( '%s.%s' % ( r1, r2 ) , lth)
            r1 = r1 + 1
    
        return k._tailEnd( w )
    #@nonl
    #@-node:ekr.20050920084036.225:clearRectangle
    #@+node:ekr.20050920084036.226:closeRectangle
    def closeRectangle (self,event):
    
        if not self._chckSel(event):
            return
    
        k = self.k ; w = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints(event)
        ar1 = r1
        txt = []
        while ar1 <= r3:
            txt.append(w.get('%s.%s' % (ar1,r2),'%s.%s' % (ar1,r4)))
            ar1 = ar1 + 1
        for z in txt:
            if z.lstrip().rstrip():
                return
        while r1 <= r3:
            w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
            r1 = r1 + 1
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.226:closeRectangle
    #@+node:ekr.20050920084036.227:deleteRectangle
    def deleteRectangle (self,event):
    
        if not self._chckSel(event):
            return
    
        k = self.k ; w = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints(event)
        #lth = ' ' * ( r4 - r2 )
        self.stopControlX(event)
        while r1 <= r3:
            w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
            r1 = r1 + 1
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.227:deleteRectangle
    #@+node:ekr.20050920084036.228:killRectangle
    def killRectangle (self,event):
    
        if not self._chckSel(event):
            return
    
        k = self.k ; w = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints(event)
    
        self.stopControlX(event)
        self.krectangle = []
        while r1 <= r3:
            txt = w.get('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
            self.krectangle.append(txt)
            w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
            r1 = r1 + 1
    
        return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.228:killRectangle
    #@+node:ekr.20050920084036.229:yankRectangle
    def yankRectangle( self, event , krec = None ):
        self.stopControlX( event )
        if not krec:
            krec = self.krectangle
        if not krec:
            return 'break'
        k = self.k ; w = event.widget
        txt = w.get( 'insert linestart', 'insert' )
        txt = self.getWSString( txt )
        i = w.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = int( i1 )
        for z in krec:        
            txt2 = w.get( '%s.0 linestart' % i1, '%s.%s' % ( i1, i2 ) )
            if len( txt2 ) != len( txt ):
                amount = len( txt ) - len( txt2 )
                z = txt[ -amount : ] + z
            w.insert( '%s.%s' %( i1, i2 ) , z )
            if w.index( '%s.0 lineend +1c' % i1 ) == w.index( 'end' ):
                w.insert( '%s.0 lineend' % i1, '\n' )
            i1 = i1 + 1
        return k._tailEnd( w )
    #@nonl
    #@-node:ekr.20050920084036.229:yankRectangle
    #@+node:ekr.20050920084036.230:openRectangle
    def openRectangle( self, event ):
    
        if not self._chckSel( event ):
            return
    
        k = self.k ; w = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        lth = ' ' * ( r4 - r2 )
        self.stopControlX( event )
        while r1 <= r3:
            w.insert( '%s.%s' % ( r1, r2 ) , lth)
            r1 = r1 + 1
        return k._tailEnd( w )
    #@nonl
    #@-node:ekr.20050920084036.230:openRectangle
    #@-node:ekr.20050920084036.224:Entry points
    #@+node:ekr.20050920084036.231:activateRectangleMethods
    def activateRectangleMethods (self,event):
    
        k = self.k
    
        self.rectanglemode = 1
        k.setLabel('C - x r')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.231:activateRectangleMethods
    #@+node:ekr.20050920084036.232:stringRectangle (called from processKey)
    def stringRectangle (self,event):
    
        k = self.k ; w = event.widget
        if not self.sRect:
            self.sRect = 1
            k.setLabelBlue('String rectangle :')
            return 'break'
        if event.keysym == 'Return':
            self.sRect = 3
        if self.sRect == 1:
            k.setLabel('')
            self.sRect = 2
        if self.sRect == 2:
            k.updateLabel(event)
            return 'break'
        if self.sRect == 3:
            if not self._chckSel(event):
                k.stopControlX(event)
                return
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            lth = k.getLabel()
            while r1 <= r3:
                w.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                w.insert('%s.%s' % (r1,r2),lth)
                r1 = r1 + 1
            k.stopControlX(event)
            return k._tailEnd(w)
    #@nonl
    #@-node:ekr.20050920084036.232:stringRectangle (called from processKey)
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
    #@-others
#@nonl
#@-node:ekr.20050920084036.221:class rectangleCommandsClass
#@+node:ekr.20050920084036.234:class registerCommandsClass
class registerCommandsClass (baseEditCommandsClass):

    '''A class to represent registers a-z and the corresponding Emacs commands.'''

    #@    @+others
    #@+node:ekr.20050920084036.235: ctor, finishCreate & init
    def __init__ (self,c):
        
        baseEditCommandsClass.__init__(self,c) # init the base class.
    
        self.method = None 
        self.methodDict, self.helpDict = self.addRegisterItems()
        self.registermode = 0 # Must be an int.
        
    def finishCreate (self):
        
        baseEditCommandsClass.finishCreate(self) # finish the base class.
        
        if self.k.useGlobalRegisters:
            self.registers = leoKeys.keyHandlerClass.global_registers
        else:
            self.registers = {}
            
    def init (self):
    
        if self.registermode:
            self.deactivateRegister()
        self.registermode = 0
            
        
    #@nonl
    #@-node:ekr.20050920084036.235: ctor, finishCreate & init
    #@+node:ekr.20050920084036.236: Entry points
    def setEvent (self,event,l):
        event.keysym = l ; return event
    
    def copyToRegister (self,event):
        return self.setEvent(event,'s') and self.setNextRegister(event)
        
    def copyRectangleToRegister (self,event):
        return self.setEvent(event,'r') and self.setNextRegister(event)
        
    def incrementRegister (self,event):
        return self.setEvent(event,'plus') and self.setNextRegister(event)
        
    def insertRegister (self,event):
        return self.setEvent(event,'i') and self.setNextRegister(event)
        
    def jumpToRegister (self,event):
        return self.setEvent(event,'j') and self.setNextRegister(event)
        
    def numberToRegister (self,event):
        return self.setEvent(event,'n') and self.setNextRegister(event)
        
    def pointToRegister (self,event):
        return self.setEvent(event,'space') and self.setNextRegister(event)
        
    def viewRegister (self,event):
        return self.setEvent(event,'view') and self.setNextRegister(event)
    #@+node:ekr.20050920084036.237:appendToRegister
    def appendToRegister (self,event):
    
        k = self.k
        event.keysym = 'a'
        self.setNextRegister(event)
        k.setState('controlx',1)
    #@nonl
    #@-node:ekr.20050920084036.237:appendToRegister
    #@+node:ekr.20050920084036.238:prependToRegister
    def prependToRegister (self,event):
    
        k = self.k
        event.keysym = 'p'
        self.setNextRegister(event)
        k.setState('controlx',0)
    #@-node:ekr.20050920084036.238:prependToRegister
    #@+node:ekr.20050920084036.239:_copyRectangleToRegister
    def _copyRectangleToRegister (self,event):
        
        if not self._chckSel(event):
            return 
        if event.keysym in string.letters:
            event.keysym = event.keysym.lower()
            w = event.widget 
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            rect =[]
            while r1<=r3:
                txt = w.get('%s.%s'%(r1,r2),'%s.%s'%(r1,r4))
                rect.append(txt)
                r1 = r1+1
            self.registers[event.keysym] = rect 
        self.stopControlX(event)
    #@-node:ekr.20050920084036.239:_copyRectangleToRegister
    #@+node:ekr.20050920084036.240:_copyToRegister
    def _copyToRegister (self,event):
    
        if not self._chckSel(event):
            return 
    
        if event.keysym in string.letters:
            event.keysym = event.keysym.lower()
            w = event.widget 
            txt = w.get('sel.first','sel.last')
            self.registers[event.keysym] = txt 
            return 
    
        self.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.240:_copyToRegister
    #@+node:ekr.20050920084036.241:_incrementRegister
    def _incrementRegister (self,event):
        
        if self.registers.has_key(event.keysym):
            if self._checkIfRectangle(event):
                return 
            if self.registers[event.keysym]in string.digits:
                i = self.registers[event.keysym]
                i = str(int(i)+1)
                self.registers[event.keysym] = i 
            else:
                self.invalidRegister(event,'number')
                return 
        self.stopControlX(event)
    #@-node:ekr.20050920084036.241:_incrementRegister
    #@+node:ekr.20050920084036.242:_insertRegister
    def _insertRegister (self,event):
        
        w = event.widget 
        if self.registers.has_key(event.keysym):
            if isinstance(self.registers[event.keysym],list):
                self.yankRectangle(event,self.registers[event.keysym])
            else:
                w.insert('insert',self.registers[event.keysym])
                w.event_generate('<Key>')
                w.update_idletasks()
    
        self.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.242:_insertRegister
    #@+node:ekr.20050920084036.243:_jumpToRegister
    def _jumpToRegister (self,event):
        if event.keysym in string.letters:
            if self._checkIfRectangle(event):
                return 
            w = event.widget 
            i = self.registers[event.keysym.lower()]
            i2 = i.split('.')
            if len(i2)==2:
                if i2[0].isdigit()and i2[1].isdigit():
                    pass 
                else:
                    self.invalidRegister(event,'index')
                    return 
            else:
                self.invalidRegister(event,'index')
                return 
            w.mark_set('insert',i)
            w.event_generate('<Key>')
            w.update_idletasks()
        self.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.243:_jumpToRegister
    #@+node:ekr.20050920084036.244:_numberToRegister
    def _numberToRegister (self,event):
        if event.keysym in string.letters:
            self.registers[event.keysym.lower()] = str(0)
        self.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.244:_numberToRegister
    #@+node:ekr.20050920084036.245:_pointToRegister
    def _pointToRegister (self,event):
        if event.keysym in string.letters:
            w = event.widget 
            self.registers[event.keysym.lower()] = w.index('insert')
        self.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.245:_pointToRegister
    #@+node:ekr.20050920084036.246:_viewRegister
    def _viewRegister (self,event):
        
        k = self.k
    
        s = self.registers.get(event.keysym.lower())
        if s:
            k.setLabel(s)
    #@nonl
    #@-node:ekr.20050920084036.246:_viewRegister
    #@-node:ekr.20050920084036.236: Entry points
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
    #@+node:ekr.20050920084036.248:Helpers
    #@+node:ekr.20050920084036.249:_chckSel
    def _chckSel (self,event):
        
        w = event.widget
    
        return 'sel' in w.tag_names() and w.tag_ranges('sel')
    
        if 0: # old code
            if not 'sel' in event.widget.tag_names():
                return False
            if not event.widget.tag_ranges('sel'):
                return False
            return True
    #@nonl
    #@-node:ekr.20050920084036.249:_chckSel
    #@+node:ekr.20050920084036.250:_checkIfRectangle
    def _checkIfRectangle (self,event):
    
        k = self.k
    
        if self.registers.has_key(event.keysym):
            if isinstance(self.registers[event.keysym],list):
                k.stopControlX(event)
                k.setLabel("Register contains Rectangle, not text")
                return True
    
        return False
    #@nonl
    #@-node:ekr.20050920084036.250:_checkIfRectangle
    #@+node:ekr.20050920084036.251:_ToReg
    def _ToReg( self, event , which):
    
        if not self._chckSel( event ):
            return
        if self._checkIfRectangle( event ):
            return
    
        if event.keysym in string.letters:
            event.keysym = event.keysym.lower()
            w = event.widget
            if not self.registers.has_key( event.keysym ):
                self.registers[ event.keysym ] = ''
            txt = w.get( 'sel.first', 'sel.last' )
            rtxt = self.registers[ event.keysym ]
            if self.which == 'p':
                txt = txt + rtxt
            else:
                txt = rtxt + txt
            self.registers[ event.keysym ] = txt
            return
    #@nonl
    #@-node:ekr.20050920084036.251:_ToReg
    #@+node:ekr.20050920084036.252:addRegisterItems (registerCommandsClass)
    def addRegisterItems( self ):
        
        methodDict = {
            's':        self._copyToRegister,
            'i':        self._insertRegister,
            'n':        self._numberToRegister,
            'plus':     self._incrementRegister,
            'space':    self._pointToRegister,
            'j':        self._jumpToRegister,
            'a':        lambda event,which='a': self._ToReg(event,which), # _appendToRegister
            'p':        lambda event,which='p': self._ToReg(event,which), # _prependToRegister
            'r':        self._copyRectangleToRegister,
            'view' :    self._viewRegister,
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
            'view': 'view register',
        }
    
        return methodDict, helpDict
    #@nonl
    #@-node:ekr.20050920084036.252:addRegisterItems (registerCommandsClass)
    #@+node:ekr.20050920084036.253:deactivateRegister
    def deactivateRegister (self,event=None): # Event not used.
    
        k = self.k
    
        k.setLabelGrey('')
        self.registermode = 0
        self.method = None
    #@nonl
    #@-node:ekr.20050920084036.253:deactivateRegister
    #@+node:ekr.20050920084036.254:invalidRegister
    def invalidRegister (self,event,what):
    
        k = self.k
    
        self.deactivateRegister(event)
        k.setLabel('Register does not contain valid %s' % what)
    #@nonl
    #@-node:ekr.20050920084036.254:invalidRegister
    #@+node:ekr.20050920084036.255:setNextRegister
    def setNextRegister (self,event):
        
        k = self.k
    
        if event.keysym=='Shift':
            return 
    
        if self.methodDict.has_key(event.keysym):
            k.setState('controlx',1)
            self.method = self.methodDict[event.keysym]
            self.registermode = 2
            k.setLabel(self.helpDict[event.keysym])
        else:
            k.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.255:setNextRegister
    #@+node:ekr.20050920084036.256:executeRegister
    def executeRegister (self,event):
        
        k = self.k
    
        self.method(event)
        if self.registermode:
            k.stopControlX(event)
    #@nonl
    #@-node:ekr.20050920084036.256:executeRegister
    #@-node:ekr.20050920084036.248:Helpers
    #@-others
#@nonl
#@-node:ekr.20050920084036.234:class registerCommandsClass
#@+node:ekr.20050920084036.257:class searchCommandsClass
class searchCommandsClass (baseEditCommandsClass):
    
    '''Implements many kinds of searches.'''

    #@    @+others
    #@+node:ekr.20050920084036.258: ctor
    def __init__ (self,c):
    
        baseEditCommandsClass.__init__(self,c) # init the base class.
        
        self.csr = { '<Control-s>': 'for', '<Control-r>':'bak' }
        self.pref = None
    
        # For replace-string and replace-regex
        self._sString = ''
        self._rpString = ''
    #@nonl
    #@-node:ekr.20050920084036.258: ctor
    #@+node:ekr.20050920084036.259:getPublicCommands
    def getPublicCommands (self):
        
        return {
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
    #@-node:ekr.20050920084036.259:getPublicCommands
    #@+node:ekr.20050920084036.260:Entry points
    # Incremental...
    def isearchForward (self,event):
        g.trace()
        return self.k.keyboardQuit(event) and self.startIncremental(event,'<Control-s>')
        
    def isearchBackward (self,event):
        g.trace()
        return self.k.keyboardQuit(event) and self.startIncremental(event,'<Control-r>')
        
    def isearchForwardRegexp (self,event):
        g.trace()
        return self.k.keyboardQuit(event) and self.startIncremental(event,'<Control-s>',which='regexp')
        
    def isearchBackwardRegexp (self,event):
        g.trace()
        return self.k.keyboardQuit(event) and self.startIncremental(event,'<Control-r>',which='regexp')
    
    # Non-incremental...
    def reSearchBackward (self,event):
        return self.reStart(event,which='backward')
    
    def searchForward (self,event):
        return self.startNonIncrSearch(event,'for')
        
    def searchBackward (self,event):
        return self.startNonIncrSearch(event,'bak')
        
    def wordSearchForward (self,event):
        return self.startWordSearch(event,'for')
        
    def wordSearchBackward (self,event):
        return self.startWordSearch(event,'bak')
    #@nonl
    #@-node:ekr.20050920084036.260:Entry points
    #@+node:ekr.20050920084036.261:incremental search methods
    #@+node:ekr.20050920084036.262:startIncremental
    def startIncremental (self,event,kind='<Control-s>',which='normal'):
    
        k = self.k # kind is '<Control-s>' or '<Control-r>'
    
        state = k.getState('isearch')
        
        g.trace(kind,state)
        
        if state == 0:
            self.pref = self.csr [kind]
            k.setState('isearch',which,handler=self.iSearchStateHandler)
            k.setLabelBlue('isearch:',protect=True)
        else:
            self.search(event,way=self.csr[kind],useregex=self.useRegex())
            self.pref = self.csr [kind]
            self.scolorizer(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.262:startIncremental
    #@+node:ekr.20050920084036.263:search
    def search (self,event,way,useregex=False):
    
        '''This method moves the insert spot to position that matches the pattern in the miniBuffer'''
        
        k = self.k ; w = event.widget
        s = k.getLabel(ignorePrompt=True)
        g.trace(way,repr(s))
        if s:
            try:
                if way == 'bak': # Search backwards.
                    i = w.search(s,'insert',backwards=True,stopindex='1.0',regexp=useregex)
                    if not i:
                        # Start again at the bottom of the buffer.
                        i = w.search(s,'end',backwards=True,stopindex='insert',regexp=useregex)
                else: # Search forwards.
                    i = w.search(s,"insert + 1c",stopindex='end',regexp=useregex)
                    if not i:
                        # Start again at the top of the buffer.
                        i = w.search(s,'1.0',stopindex='insert',regexp=useregex)
            except: pass
    
            if i and not i.isspace():
                w.mark_set('insert',i)
                w.see('insert')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.263:search
    #@+node:ekr.20050920084036.264:iSearchStateHandler
    # Called when from the state manager when the state is 'isearch'
    
    def iSearchStateHandler (self,event):
    
        k = self.k ; stroke = k.stroke ; w = event.widget
        if not event.char: return
    
        g.trace(event.keysym)
    
        if stroke in self.csr:
            return self.startIncremental(event,stroke)
    
        if event.keysym == 'Return':
            s = k.getLabel(ignorePrompt=True)
            if s:
                return k.stopControlX(event)
            else:
                return self.startNonIncrSearch(event,self.pref)
    
        k.updateLabel(event)
        if event.char == '\b':
            g.trace('backspace not handled yet')
        else:
           s = k.getLabel(ignorePrompt=True)
           z = w.search(s,'insert',stopindex='insert +%sc' % len(s))
           if not z:
               self.search(event,self.pref,useregex=self.useRegex())
        self.scolorizer(event)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.264:iSearchStateHandler
    #@+node:ekr.20050920084036.265:scolorizer
    def scolorizer (self,event):
    
        k = self.k ; w = event.widget
    
        stext = k.getLabel(ignorePrompt=True)
        w.tag_delete('color')
        w.tag_delete('color1')
        if stext == '': return 'break'
        ind = '1.0'
        while ind:
            try:
                ind = w.search(stext,ind,stopindex='end',regexp=self.useRegex())
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
    #@+node:ekr.20050920084036.266:useRegex
    def useRegex (self):
    
        k = self.k
    
        return k.getState('isearch') != 'normal'
    #@nonl
    #@-node:ekr.20050920084036.266:useRegex
    #@-node:ekr.20050920084036.261:incremental search methods
    #@+node:ekr.20050920084036.267:non-incremental search methods
    #@+at
    # Accessed by Control-s Enter or Control-r Enter.
    # Alt-x forward-search or backward-search, just looks for words...
    #@-at
    #@nonl
    #@+node:ekr.20050920084036.268:nonincrSearchStateHandler
    def nonincrSearchStateHandler (self,event):
    
        k = self.k ; stroke = k.stroke ; w = event.widget
    
        if event.keysym in ('Control_L','Control_R'): return
        state = k.getState('nonincr-search')
        if state.startswith('start'):
            state = state [5:]
            k.setState('nonincr-search',state)
            k.setLabel('')
    
        if k.getLabel() == '' and stroke == '<Control-w>':
            return self.startWordSearch(event,state)
    
        if event.keysym == 'Return':
            i = w.index('insert')
            word = k.getLabel()
            if state == 'for':
                try:
                    s = w.search(word,i,stopindex='end')
                except Exception: # Can throw an exception.
                    s = None
                if s: s = w.index('%s +%sc' % (s,len(word)))
            else: s = w.search(word,i,stopindex='1.0',backwards=True)
            if s: w.mark_set('insert',s)
            k.keyboardQuit(event)
            return k._tailEnd(w)
        else:
            k.updateLabel(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.268:nonincrSearchStateHandler
    #@+node:ekr.20050920084036.269:startNonIncrSearch
    def startNonIncrSearch (self,event,which):
    
        k = self.k
    
        k.keyboardQuit(event)
        k.setState('nonincr-search','start%s' % which,
            handler=self.nonincrSearchStateHandler)
        k.setLabelBlue('Search:')
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.269:startNonIncrSearch
    #@-node:ekr.20050920084036.267:non-incremental search methods
    #@+node:ekr.20050920084036.270:word search methods
    #@+at
    # 
    # Control-s(r) Enter Control-w words Enter, pattern entered is treated as 
    # a regular expression.
    # 
    # for example in the buffer we see:
    #     cats......................dogs
    # 
    # if we are after this and we enter the backwards look, search for 'cats 
    # dogs' if will take us to the match.
    #@-at
    #@nonl
    #@+node:ekr.20050920084036.271:startWordSearch
    def startWordSearch (self,event,which):
    
        k = self.k
    
        k.keyboardQuit(event)
        k.setState('word-search','start%s' % which,
            handler=self.wordSearchStateHandler)
        k.setLabelBlue('Word Search %s:' %
            g.choose(which=='bak','Backward','Forward'),protect=True)
    
        return 'break'
    #@nonl
    #@-node:ekr.20050920084036.271:startWordSearch
    #@+node:ekr.20050920084036.272:wordSearchStateHandler
    def wordSearchStateHandler (self,event):
    
        k = self.k ; w = event.widget
        state = k.getState('word-search')
        if state.startswith('start'): # pathetic hack.
            state = state [5:]
            k.setState('word-search',state,
                handler=self.wordSearchStateHandler)
        if event.keysym == 'Return':
            i = w.index('insert')
            words = k.getLabel().split()
            sep = '[%s%s]+' % (string.punctuation,string.whitespace)
            pattern = sep.join(words)
            cpattern = re.compile(pattern)
            if state == 'for':
                txt = w.get('insert','end')
                match = cpattern.search(txt)
                if not match: return k.keyboardQuit(event)
                end = match.end()
            else:
                txt = w.get('1.0','insert') #initially the reverse words formula for Python Cookbook was going to be used.
                a = re.split(pattern,txt) #that didnt quite work right.  This one apparently does.
                if len(a) > 1:
                    b = re.findall(pattern,txt)
                    end = len(a[-1]) + len(b[-1])
                else: return k.keyboardQuit(event)
            wdict = {'for': 'insert +%sc', 'bak': 'insert -%sc'}
            w.mark_set('insert',wdict[state] % end)
            w.see('insert')
            k.keyboardQuit(event)
            return k._tailEnd(w)
        else:
            k.updateLabel(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.272:wordSearchStateHandler
    #@-node:ekr.20050920084036.270:word search methods
    #@+node:ekr.20050920084036.273:re-search methods
    # For the re-search-backward and re-search-forward Alt-x commands
    #@nonl
    #@+node:ekr.20050920084036.274:reStart
    def reStart (self,event,which='forward'):
    
        k = self.k
    
        k.keyboardQuit(event)
        k.setState('re_search','start%s' % which,
            handler=self.reSearchStateHandler)
        k.setLabelBlue('RE Search:')
    
        return 'break'
    
    reSearchForward = reStart
    #@nonl
    #@-node:ekr.20050920084036.274:reStart
    #@+node:ekr.20050920084036.275:reSearchStateHandler
    def reSearchStateHandler (self,event):
    
        k = self.k ; w = event.widget
        state = k.getState('re_search')
        if state.startswith('start'):
            state = state [5:] # pathetic hack.
            k.setState('re_search',state,
                handler=self.reSearchStateHandler)
            k.setLabel('')
        if event.keysym == 'Return':
            pattern = k.getLabel()
            cpattern = re.compile(pattern)
            end = None
            if state == 'forward':
                txt = w.get('insert','end')
                match = cpattern.search(txt)
                end = match.end()
            else:
                txt = w.get('1.0','insert') #initially the reverse words formula for Python Cookbook was going to be used.
                a = re.split(pattern,txt) #that didnt quite work right.  This one apparently does.
                if len(a) > 1:
                    b = re.findall(pattern,txt)
                    end = len(a[-1]) + len(b[-1])
            if end:
                wdict = {'forward': 'insert +%sc', 'backward': 'insert -%sc'}
                w.mark_set('insert',wdict[state] % end)
                k._tailEnd(w)
                w.see('insert')
            return k.keyboardQuit(event)
        else:
            k.updateLabel(event)
            return 'break'
    #@nonl
    #@-node:ekr.20050920084036.275:reSearchStateHandler
    #@-node:ekr.20050920084036.273:re-search methods
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
