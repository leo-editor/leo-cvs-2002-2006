#@+leo-ver=4
#@+node:@file ../src/elisp2py.py
import leoGlobals as g
import string

tabWidth = 4 # how many blanks in a tab.
printFlag = False
doLeoTranslations,dontDoLeoTranslations = True,False

gClassName = "" # The class name for the present function.  Used to modify ivars.
gIvars = [] # List of ivars to be converted to self.ivar

#@+others
#@+node:class tok
class tok:
    
    """ A class representing an elisp or python token"""
    
    #@    @+others
    #@+node:tok.__init__
    def __init__ (self,kind,val=""):
        
        self.kind = kind
        self.val = val
    #@nonl
    #@-node:tok.__init__
    #@+node:tok.copy
    def copy (self,token):
        
        return tok(self.kind,self.val)
    #@nonl
    #@-node:tok.copy
    #@+node:tok.match
    def match (self,tok2):
        
        tok1 = self
        
        val = (
            tok2 is not None and
            tok1.kind == tok2.kind and
            (not tok1.val or not tok2.val or (tok1.val == tok2.val)))
            
        if 0:
            if tok1.kind==tok2.kind:
                g.trace(val,tok1.kind,repr(tok1.val),tok2.kind)
            
        return val
    #@nonl
    #@-node:tok.match
    #@+node:tok.dump
    def dump (self,verbose=2):
        
        tok = self
    
        if verbose == 2:
            print tok.toString(verbose=verbose)
        else:
            print tok.toString(verbose=verbose),
        
        return ##
        
        if verbose == 2:
            val = g.toEncodedString(tok.val,g.app.tkEncoding)
            if   tok.kind == '\n':      print "%9s:" % "newline"
            elif tok.kind=="form-feed": print "%9s:" % "form-feed"
            elif len(tok.kind)==1:      print "%9s:" % tok.kind
            elif tok.kind == "ws":
                    print "%9s: %s" % (tok.kind,self.dumpWs(tok.val))
            else:   print "%9s: <%s>" % (tok.kind, val)
    
        else:
            val = g.toEncodedString(tok.val,g.app.tkEncoding)
            if tok.kind == '\n':        print
            elif len(tok.kind) == 1:    print tok.kind,
            elif tok.kind=="form-feed":
                print ; print "form-feed" ; print
            else: print val,
    #@nonl
    #@-node:tok.dump
    #@+node:tok.dumpWs
    def dumpWs (self,ws):
        
        result = ["<"]
        for ch in ws:
            if ch == ' ':
                result.append(" ")
            elif ch == '\t':
                result.append("tab")
            elif ch == '\f':
                result.append("feed")
            else:
                result.append("<%s>" % repr(ch)) # should never happen.
        
        result.append(">")
        return ''.join(result)
    #@nonl
    #@-node:tok.dumpWs
    #@+node:tok.toString
    def toString (self,verbose=2):
        
        tok = self
        
        if verbose < 2:
            return
        
        val = tok.val or ""
        val = g.toEncodedString(val,g.app.tkEncoding)
        
        if verbose == 2:
            if len(tok.kind) == 1:      return tok.kind
            elif tok.kind=="form-feed": return "\nform-feed\n"
            else:                       return val
        
        elif verbose == 3:
            if   tok.kind == '\n':      return "%9s:" % "newline"
            elif tok.kind=="form-feed": return "%9s:" % "form-feed"
            elif len(tok.kind)==1:      return "%9s:" % tok.kind
            elif tok.kind == "ws":
                    return "%9s: %s" % (tok.kind,self.dumpWs(val))
            else:   return "%9s: <%s>" % (tok.kind,val)
    #@-node:tok.toString
    #@-others
#@nonl
#@-node:class tok
#@+node:class elisp2pyClass
class elisp2pyClass:
    
    """A class to convert elisp programs into Python syntax."""
    
    #@    @+others
    #@+node:e.__init__
    def __init__ (self,c,p,*args,**keys):
        
        self.c = c
        self.p = p
    
        self.statementLevel = 0
    #@nonl
    #@-node:e.__init__
    #@+node:Utils
    #@+node:deleteTokens
    def deleteTokens (self,tokens,delToken):
                
        return [tok for tok in tokens if not tok.match(delToken)]
    #@nonl
    #@-node:deleteTokens
    #@+node:dump
    def dump (self,tokens,verbose=1):
        
        e = self ; p = e.p ; v2 = verbose >= 2
        
        if verbose == 0:
            return
        elif verbose == 1:
            vals = [tok.val for tok in tokens]
            s = ''.join(vals)
            s = g.toEncodedString(s,g.app.tkEncoding)
            print s
        elif verbose in (2,3):
            #@        << print headline >>
            #@+node:<< print headline >>
            print
            print ; print '-' * 40
            print p.headString()
            print '-' * 40
            print
            #@nonl
            #@-node:<< print headline >>
            #@nl
            if verbose == 2:
                for tok in tokens:
                    print tok.toString(verbose=verbose),
            else:
                for tok in tokens:
                    print tok.toString(verbose=verbose)
    #@nonl
    #@-node:dump
    #@+node:error & warning
    def warning (self,message):
        
        print "Error:", message
    
    def warning (self,message):
        
        print "Warning:", message
    #@-node:error & warning
    #@+node:findMatchingBracket
    def findMatchingBracket(self,tokens,i):
    
        tok = tokens[i] ; i += 1
        ch1 = tok.kind
        assert ch1 in "({["
       
        if   ch1 == '(': delim = ')'
        elif ch1 == '{': delim = '}'
        else:            delim = ']'
    
        level = 0
        while i < len(tokens):
            tok = tokens[i]
            i += 1
            if tok.kind == ch1:
                level += 1
            elif tok.kind == delim:
                level -= 1
                if level == 0: return i-1
    
        self.warning("%s not matched by %s", ch1,delim)
        return None
    #@nonl
    #@-node:findMatchingBracket
    #@+node:findTokens
    def findTokens(self,tokens,i,fTokens):
    
        progress = i-1
        while i < len(tokens):
            assert progress < i
            progress = i
    
            found = True
            for j in xrange(len(fTokens)):
                tok = tokens[i+j]
                ftok = fTokens[j]
                if not tok.match(ftok):
                    found = False; break
            if found: return i,i+j
            else: i += 1
    
        return None,None # Not found
    #@nonl
    #@-node:findTokens
    #@+node:replaceAll (not used yet)
    def replaceAll (self,tokens,findKind,changeTok):
        
        self = e
    
        result = []
        for token in tokens:
            if token.kind == findKind:
                result.append(changeTok.copy())
            else:
                result.append(token)
    #@nonl
    #@-node:replaceAll (not used yet)
    #@+node:tokenize & allies
    def tokenize (self,s):
        
        e = self
        name1 = string.letters + '_'
        result = []
        if not s.strip():
            return result
    
        i = 0 ; n = len(s) ; progress = -1
        while i < n:
            assert(i > progress)
            progress = i
            ch = s[i]
            if ch == '\r':
                i += 1
            elif ch in "@'()[]{}<>\n": # Handle single-quote here?
                result.append(tok(ch,ch))
                i += 1
            elif ch in "\ \t":
                j = g.skip_ws(s,i) # Doesn't handle ff, so ff loops.
                ws = s[i:j]
                result.append(tok("ws",ws))
                i = j
            elif ch == '\f':
                result.append(tok("form-feed",'\f'))
                i += 1
            elif ch == '"':
                j = e.skipString(s,i)
                val = s[i:j]
                result.append(tok("string",val))
                i = j
            elif ch in name1:
                j = g.skip_id(s,i,chars='-') # '-' valid in elisp.
                val = s[i:j]
                result.append(tok("id",val))
                i = j
            elif ch in string.digits:
                j,value = g.skip_long(s,i)
                val = s[i:j]
                result.append(tok("number",val))
                i = j
            elif ch == ';':
                j = g.skip_to_end_of_line(s,i)
                val = s[i:j]
                result.append(tok("comment",val))
                i = j
            else:
                result.append(tok("misc",ch))
                i += 1
                
        return result
    #@nonl
    #@+node:skipString
    def skipString(self,s,i):
    
        # Skip the opening double quote.
        i1 = i
        ch = s[i]
        i += 1
        assert(ch == '"')
    
        while i < len(s):
            ch = s[i]
            i += 1
            if ch == '"': return i
            elif ch == '\\': i += 1
    
        self.warning("run-on elisp string:", g.get_line(s[i1:]))
        return i
    #@nonl
    #@-node:skipString
    #@-node:tokenize & allies
    #@-node:Utils
    #@+node:Converters
    #@+node:convert (main line)
    def convert (self):
        
        e = self ; p = e.p
    
        e.tokens = e.tokenize(p.bodyString())
        e.tokens = e.deleteTokens(e.tokens,tok("ws"))
        e.tokens = e.deleteTokens(e.tokens,tok('\n'))
        # e.dump(e.tokens,verbose=3)
        e.createPythonIndentation(e.tokens)
    #@nonl
    #@-node:convert (main line)
    #@+node:createPythonIndentation
    def createPythonIndentation (self,tokens):
        
        e = self ; p = e.p
    
        # Whitespace has been deleted.
        findToks = [tok('('),tok("id","defun"),tok("id"),tok("(")] 
        
        i = 0 ; progress = -1
        while i < len(tokens):
            assert(progress < i)
            progress = i
            i,j = e.findTokens(tokens,i,findToks)
            if i is not None:
                s = [str(tokens[k].toString()) for k in xrange(i,j+1)]
                print "found:",' '.join(s)
                k = e.findMatchingBracket(tokens,i)
                if k is None:
                    print "No matching bracket!"
                     i = j + 1
                else:
                    # print "found matching bracket",k,str(tokens[k].toString())
                    e.statementLevel += 1
                    e.createIndentedBlock(tokens[1:k])
                    e.statementLevel -= 1
                    ### This isn't right: we will have to replace the token list and start again.
                    i = k + 1
            else:
                break
    #@nonl
    #@-node:createPythonIndentation
    #@+node:createIndentedBlock
    def createIndentedBlock (self,tokens):
        
        return ## not ready yet.
        
        e = self ; p = e.p
    
        # Whitespace has been deleted.
        findToks = [tok('('),tok("id","defun"),tok("id"),tok("(")] 
        
        i = 0 ; progress = -1
        while i < len(tokens):
            assert(progress < i)
            progress = i
            i,j = e.findTokens(tokens,i,findToks)
            if i is not None:
                s = [str(tokens[k].toString()) for k in xrange(i,j+1)]
                print "found:",' '.join(s)
                k = e.findMatchingBracket(tokens,i)
                if k is None: print "No matching bracket!"
                else:
                    # print "found matching bracket",k,str(tokens[k].toString())
                    e.statementLevel += 1
                    e.createIndentedBlock(tokens[1:k])
                    e.statementLevel -= 1
                i = j + 1
            else:
                break
    #@nonl
    #@-node:createIndentedBlock
    #@+node:handleAllKeywords (old)
    # converts if ( x ) to if x:
    # converts while ( x ) to while x:
    def handleAllKeywords(codeList):
    
        # print "handAllKeywords:", listToString(codeList)
        i = 0
        while i < len(codeList):
            if isStringOrComment(codeList,i):
                i = skipStringOrComment(codeList,i)
            elif ( matchWord(codeList,i,"if") or
                matchWord(codeList,i,"while") or
                matchWord(codeList,i,"for") or
                matchWord(codeList,i,"elif") ):
                i = handleKeyword(codeList,i)
            else:
                i += 1
        # print "handAllKeywords2:", listToString(codeList)
    #@nonl
    #@+node:handleKeyword
    def handleKeyword(codeList,i):
    
        isFor = False
        if (matchWord(codeList,i,"if")):
            i += 2
        elif (matchWord(codeList,i,"elif")):
            i += 4
        elif (matchWord(codeList,i,"while")):
            i += 5
        elif (matchWord(codeList,i,"for")):
            i += 3
            isFor = True
        else: assert(0)
        # Make sure one space follows the keyword
        k = i
        i = skipWs(codeList,i)
        if k == i:
            c = codeList[i]
            codeList[i:i+1] = [ ' ', c ]
            i += 1
        # Remove '(' and matching ')' and add a ':'
        if codeList[i] == "(":
            j = removeMatchingBrackets(codeList,i)
            if j > i and j < len(codeList):
                c = codeList[j]
                codeList[j:j+1] = [":", " ", c]
                j = j + 2
            return j
        return i
    #@nonl
    #@-node:handleKeyword
    #@-node:handleAllKeywords (old)
    #@-node:Converters
    #@-others
#@nonl
#@-node:class elisp2pyClass
#@-others
#@-node:@file ../src/elisp2py.py
#@-leo
