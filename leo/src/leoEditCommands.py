#@+leo-ver=4-thin
#@+node:ekr.20050710142719:@thin leoEditCommands.py
'''Basic editor commands for Leo.

Modelled after Emacs and Vim commands.'''

#@<< imports >>
#@+node:ekr.20050710151017:<< imports >>
import leoGlobals as g
import leoPlugins

import string
#@nonl
#@-node:ekr.20050710151017:<< imports >>
#@nl

#@+others
#@+node:ekr.20050723064110:class editCommands ( to be moved into another class)
class editCommands:

    #@    @+others
    #@+node:ekr.20050723064110.1:ctor
    def __init__ (self,c):
        
        self.c = c
    
        self.mode = 'default'
        self.modeStack = []
        
        self.defaultWordChars1, self.defaultWordChars2 = self.setDefaultWordChars()
        self.wordChars1 = self.defaultWordChars1
        self.wordChars2 = self.defaultWordChars2
    
        self.setDefaultOptions()
    #@nonl
    #@-node:ekr.20050723064110.1:ctor
    #@+node:ekr.20050723064110.3:Options...
    #@+node:ekr.20050723064110.4:setDefaultOptions
    def setDefaultOptions(self):
        
        self.options = {
            'extendMovesForward':   True,  # True: moving forward may cross node boundaries.
            'extendMovesBack':      True,  # True: moving back may cross node boundaries.
            'extendFindsForward':   True,   # True: find forward may cross node boundaries.
            'extendFindsBack':      True,   # True: find back may cross node boundaries.
        }
    #@nonl
    #@-node:ekr.20050723064110.4:setDefaultOptions
    #@+node:ekr.20050723064110.5:getOption
    def getOption (self,optionName):
        
        # This may change when modes get put in.
        return self.options.get(optionName)
    #@nonl
    #@-node:ekr.20050723064110.5:getOption
    #@-node:ekr.20050723064110.3:Options...
    #@+node:ekr.20050723064110.6:Word stuff...
    #@+node:ekr.20050723064110.7:findWordStart
    def findWordStart(self,s,i):
        
        while i < len(s):
            if s[i] in self.wordChars1:
                return i
            else:
                i += 1
        return i
    #@nonl
    #@-node:ekr.20050723064110.7:findWordStart
    #@+node:ekr.20050723064110.8:insideWord
    def insideWord (self,s,i):
        
        '''Return True if the char at s[i] is inside a word but does not start the word.'''
        
        return (
            0 < i < len(s) and
            s[i] in self.wordChars2 and
            s[i-1] in self.wordChars2
        )
    #@nonl
    #@-node:ekr.20050723064110.8:insideWord
    #@+node:ekr.20050723064110.9:skipWord
    def skipWord(self,s,i):
        
        while i < len(s) and s[i] in self.wordChars2:
            i += 1
        return i
    #@nonl
    #@-node:ekr.20050723064110.9:skipWord
    #@+node:ekr.20050723064110.10:startsWord
    def startsWord (self,s,i):
        
        '''Return True if the char at s[i] is inside a word but does not start the word.'''
        
        return (
            i < len(s) and 
            s[i] in self.wordChars1 and
            (i == 0 or s[i-1] not in self.wordChars1)
        )
    #@nonl
    #@-node:ekr.20050723064110.10:startsWord
    #@+node:ekr.20050723064110.11:setDefaultWordChars
    def setDefaultWordChars (self):
        
        chars1 = '_' + string.letters
        chars2 = '_' + string.letters + string.digits
        return chars1, chars2
    #@nonl
    #@-node:ekr.20050723064110.11:setDefaultWordChars
    #@-node:ekr.20050723064110.6:Word stuff...
    #@+node:ekr.20050723064110.12:Cursor movement
    #@+node:ekr.20050723064110.13:moveBackwardChar
    def moveBackwardChar (self):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        i = b.getPythonInsertionPoint(s=s)
        i -= 1
        if i >= 0:
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesBackward'): # Recursively look for words in previous nodes.
            p = c.currentPosition().moveToThreadBack()
            while p:
                s = p.bodyString()
                if len(s) > 0:
                    c.selectPosition(p)
                    b.setPythonInsertionPoint(len(s)-1)
                    return True
                else:
                    p.moveToThreadBack()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050723064110.13:moveBackwardChar
    #@+node:ekr.20050723064110.14:moveBackwardWord (Finish)
    def moveBackwardWord (self,i=None):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        if i is None: i = b.getPythonInsertionPoint(s=s)
    
        if self.startsWord(s,i) or self.insideWord(s,i):
            i = self.findWordStart(s,i)
        i = self.findWordStart(s,i) ###
        if self.startsWord(s,i): ###
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesBackward'): # Recursively look for words in previous nodes.
            p = c.currentPosition().moveToThreadBack()
            while p:
                c.selectPosition(p)
                if self.moveBackwardWord(0):
                    return True
                p.moveToThreadBack()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050723064110.14:moveBackwardWord (Finish)
    #@+node:ekr.20050723064110.15:moveForwardChar
    def moveForwardChar (self):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        i = b.getPythonInsertionPoint(s=s)
        i += 1
        if i < len(s):
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesForward'): # Recursively look for words in following nodes.
            p = c.currentPosition().moveToThreadNext()
            while p:
                if len(p.bodyString()) > 0:
                    c.selectPosition(p)
                    b.setPythonInsertionPoint(0)
                    return True
                else:
                    p.moveToThreadNext()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050723064110.15:moveForwardChar
    #@+node:ekr.20050723064110.16:moveForwardWord
    def moveForwardWord (self,i=None):
        
        c = self.c ; b = c.frame.body ; s = b.getAllText()
        if i is None: i = b.getPythonInsertionPoint(s=s)
    
        if self.startsWord(s,i) or self.insideWord(s,i):
            i = self.skipWord(s,i)
        i = self.findWordStart(s,i)
        if self.startsWord(s,i):
            b.setPythonInsertionPoint(i)
            return True
        elif self.getOption('extendMovesForward'): # Recursively look for words in following nodes.
            p = c.currentPosition().moveToThreadNext()
            while p:
                c.selectPosition(p)
                if self.moveForwardWord(0):
                    return True
                p.moveToThreadNext()
            return False
        else:
            return False
    #@nonl
    #@-node:ekr.20050723064110.16:moveForwardWord
    #@+node:ekr.20050723064110.17:selectWord
    #@-node:ekr.20050723064110.17:selectWord
    #@+node:ekr.20050723064110.18:selectForwordWord
    def selectForwardWord (self):
        
        c = self ; b = c.frame.body ; s = b.getAllText()
    
        i = i1 = b.getPythonInsertionPoint()
        
        if i < len(s) and g.is_c_id(s[i]):
            i = g.skip_c_id(s,i+1)
        
        while i < len(s) and not g.is_c_id(s[i]):
            i += 1
            
        if i < len(s) and g.is_c_id(s[i]):
            # b.setPythonTextSelection(i1,i)
            pass ### TODO
    #@nonl
    #@-node:ekr.20050723064110.18:selectForwordWord
    #@-node:ekr.20050723064110.12:Cursor movement
    #@-others
#@nonl
#@-node:ekr.20050723064110:class editCommands ( to be moved into another class)
#@-others
#@nonl
#@-node:ekr.20050710142719:@thin leoEditCommands.py
#@-leo
