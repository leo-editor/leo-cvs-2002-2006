#@+leo-ver=4-thin
#@+node:ekr.20041021120118:@thin pretty_print.py
"""A plugin that helps customize pretty printing.

Creates a do-nothing subclass of the default pretty printer. To customize,
simply override in this file the methods of the base prettyPrinter class in
leoCommands.py.

You would typically want to override putNormalToken or its allies. Templates for
these methods have been provided. You may, however, override any methods you
like. You could even define your own class entirely, provided you implement the
prettyPrintNode method.
"""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20041021120859:<< imports >>
import leoGlobals as g

import leoCommands
import leoPlugins
#@nonl
#@-node:ekr.20041021120859:<< imports >>
#@nl

oldPrettyPrinter = leoCommands.Commands.prettyPrinter

#@+others
#@+node:ekr.20041021120454:class myPrettyPrinter
class myPrettyPrinter(leoCommands.Commands.prettyPrinter):

    #@    @+others
    #@+node:ekr.20041021123018:myPrettyPrinter.__init__
    def __init__ (self,c):
            
        # Init the base class.
        oldPrettyPrinter.__init__(self,c)
        self.tracing = False
        
        print "Overriding class leoCommands.prettyPrinter"
    #@nonl
    #@-node:ekr.20041021123018:myPrettyPrinter.__init__
    #@+node:ekr.20041021123018.1:putNormalToken & allies
    if 0: # The orignal code...
    
        def putNormalToken (self,token5tuple):
        
            t1,t2,t3,t4,t5 = token5tuple
            self.name = token.tok_name[t1].lower() # The token type
            self.val = t2  # the token string
            self.srow,self.scol = t3 # row & col where the token begins in the source.
            self.erow,self.ecol = t4 # row & col where the token ends in the source.
            self.s = t5 # The line containing the token.
            self.startLine = self.line != self.srow
            self.line = self.srow
        
            if self.startLine:
                self.doStartLine()
        
            # Dispatch a helper function.
            f = self.dispatchDict.get(self.name,self.oops)
            self.trace()
            f()
    #@nonl
    #@-node:ekr.20041021123018.1:putNormalToken & allies
    #@+node:ekr.20041021123018.2:doEndMarker
    if 0: # The orignal code...
    
        def doEndMarker (self):
            
            self.putArray()
    #@nonl
    #@-node:ekr.20041021123018.2:doEndMarker
    #@+node:ekr.20041021123018.3:doErrorToken
    if 0: # The orignal code...
    
        def doErrorToken (self):
            
            self.array.append(self.val)
        
            if self.val == '@':
                # Preserve whitespace after @.
                i = g.skip_ws(self.s,self.scol+1)
                ws = self.s[self.scol+1:i]
                if ws:
                    self.array.append(ws)
    #@nonl
    #@-node:ekr.20041021123018.3:doErrorToken
    #@+node:ekr.20041021123018.4:doIndent & doDedent
    if 0: # The orignal code...
    
        def doDedent (self):
            
            pass
            
        def doIndent (self):
            
            self.array.append(self.val)
        
    #@nonl
    #@-node:ekr.20041021123018.4:doIndent & doDedent
    #@+node:ekr.20041021123018.5:doMultiLine
    if 0: # The orignal code...
    
        def doMultiLine (self):
            
            # These may span lines, so duplicate the end-of-line logic.
            lines = g.splitLines(self.val)
            for line in lines:
                self.array.append(line)
                if line and line[-1] == '\n':
                    self.putArray()
                    
            # Suppress start-of-line logic.
            self.line = self.erow
    #@nonl
    #@-node:ekr.20041021123018.5:doMultiLine
    #@+node:ekr.20041021123018.6:doName
    if 0: # The orignal code...
    
        def doName(self):
        
            self.array.append("%s " % self.val)
            if self.prevName == "def": # A personal idiosyncracy.
                self.array.append(' ') # Retain the blank before '('.
            self.prevName = self.val
    #@nonl
    #@-node:ekr.20041021123018.6:doName
    #@+node:ekr.20041021123018.7:doNewline
    if 0: # The orignal code...
    
        def doNewline (self):
            
            self.array.append('\n')
            self.putArray()
    #@nonl
    #@-node:ekr.20041021123018.7:doNewline
    #@+node:ekr.20041021123018.8:doNumber
    if 0: # The orignal code...
    
        def doNumber (self):
        
            self.array.append(self.val)
        
    #@nonl
    #@-node:ekr.20041021123018.8:doNumber
    #@+node:ekr.20041021123018.9:doOp
    if 0: # The orignal code...
    
        def doOp (self):
            
            val = self.val
        
            if val == '(':
                self.parenLevel += 1
                self.put(val)
            elif val == ')':
                self.parenLevel -= 1
                self.put(val)
            elif val == '=':
                if self.parenLevel > 0: self.put('=')
                else:                   self.put(' = ')
            elif val == ',':
                if self.parenLevel > 0: self.put(',')
                else:                   self.put(', ')
            elif val == ';':
                self.put(" ; ")
            else:
                self.put(val)
    #@nonl
    #@-node:ekr.20041021123018.9:doOp
    #@+node:ekr.20041021123018.10:doStartLine
    if 0: # The orignal code...
    
        def doStartLine (self):
            
            before = self.s[0:self.scol]
            i = g.skip_ws(before,0)
            self.ws = self.s[0:i]
             
            if self.ws:
                self.array.append(self.ws)
    #@nonl
    #@-node:ekr.20041021123018.10:doStartLine
    #@+node:ekr.20041021123018.11:oops
    if 0: # The orignal code...
    
        def oops(self):
            
            print "unknown PrettyPrinting code: %s" % (self.name)
    #@nonl
    #@-node:ekr.20041021123018.11:oops
    #@+node:ekr.20041021123018.12:trace
    if 0: # The orignal code...
    
        def trace(self):
            
            if self.tracing:
        
                g.trace("%10s: %s" % (
                    self.name,
                    repr(g.toEncodedString(self.val,"utf-8"))
                ))
    #@nonl
    #@-node:ekr.20041021123018.12:trace
    #@-others
#@nonl
#@-node:ekr.20041021120454:class myPrettyPrinter
#@-others

if not g.app.unitTesting: # Not for unit testing:  modifies core.

    leoCommands.Commands.prettyPrinter = myPrettyPrinter

    __version__ = "1.0"
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20041021120118:@thin pretty_print.py
#@-leo
