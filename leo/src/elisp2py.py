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
    def __init__ (self,kind,val="",parseTree=None):
        
        self.kind = kind
        self.val = val
        self.parseTree = parseTree
    #@nonl
    #@-node:tok.__init__
    #@+node:tok.isParseTok
    def isParseTok (self):
        
        tok = self
        
        return type(tok.parseTree) == type([])
    #@nonl
    #@-node:tok.isParseTok
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
    #@nonl
    #@-node:tok.dump
    #@+node:tok.toString & allies
    def toString (self,verbose=2):
        
        tok = self
        
        if verbose < 2: return
        val = tok.val or ""
        val = g.toEncodedString(val,g.app.tkEncoding)
        
        if tok.isParseTok():
            parseTree = tok.parseTreeToString(tok.parseTree)
            if tok.val == "TREE":
                return "%s"% (parseTree)
            else:
                return "%s: %s"% (tok.val,parseTree)
        
        elif verbose == 2:
            if len(tok.kind) == 1:    return tok.kind
            elif tok.kind=="form-feed": return "\nform-feed\n"
            elif tok.kind=="comment":   return "<comment>"
            elif tok.kind=="string":    return "<string>"
            else:                       return val
        
        elif verbose == 3:
            if tok.kind == '\n':      return "%9s:" % "newline"
            elif tok.kind=="form-feed": return "%9s:" % "form-feed"
            elif len(tok.kind)==1:      return "%9s:" % tok.kind
            elif tok.kind == "ws":
                    return "%9s: %s" % (tok.kind,tok.wsToString(val))
            else:   return "%9s: <%s>" % (tok.kind,val)
    #@nonl
    #@+node:tok.wsToString
    def wsToString (self,ws):
        
        allBlanks = True
        for ch in ws:
            if ch != ' ':
                allBlanks = False
                
        if allBlanks:
           return "<' '*%d>" % len(ws)
        else:
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
    #@-node:tok.wsToString
    #@+node:tok.parseTreeToString
    def parseTreeToString (self,parseTree,level=0):
    
        dummy_tok = tok("dummy_tok")
        result = [] ; levelSpaces = ' '*2*level
    
        if parseTree is None:
            result.append("None")
    
        if type(parseTree) == type(dummy_tok):
            result.append(parseTree.toString(verbose=2)+' ')
    
        elif type(parseTree) == type([]):
            result.append('\n%s[' % levelSpaces)
            for item in parseTree:
                result.append(self.parseTreeToString(item,level+1))
            result.append(']')
    
        else:
            result.append("unknown type in parseTreeToString")
            
        return ''.join(result)
    #@nonl
    #@-node:tok.parseTreeToString
    #@-node:tok.toString & allies
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
        self.tabwidth = 4
    
        #@    << define elisp constants >>
        #@+node:<< define elisp constants >>
        self.constants = ("t","nil")
        #@nonl
        #@-node:<< define elisp constants >>
        #@nl
        #@    << define elisp statements >>
        #@+node:<< define elisp statements >>
        self.statements = (
            "defconst","defun","defsubst","defvar",
            "cond",
            "if",
            "let","let*",
            "prog","prog1","progn",
            "set","setq",
            "unless","when","while",
        )
        
        #@-node:<< define elisp statements >>
        #@nl
        #@    << define elisp functions >>
        #@+node:<< define elisp functions >>
        self.functions = (
            "and","or","not",
            "apply","eval",
            "cons","car","cdr",
            "error","princ",
            "eq","ne","equal","gt","ge","lt","le",
            "mapcar","type-of",
        )
        #@nonl
        #@-node:<< define elisp functions >>
        #@nl
        
        self.allStatements = list(self.statements)
        self.allStatements.extend(self.functions)
    #@nonl
    #@-node:e.__init__
    #@+node:Utils
    #@+node:deleteTokens
    def deleteTokens (self,tokens,delToken):
                
        return [tok for tok in tokens if not tok.match(delToken)]
    #@nonl
    #@-node:deleteTokens
    #@+node:dump
    def dump (self,tokens,verbose=2,tag=None):
        
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
            if tag:
                print tag
            else:
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
    
        tok1 = tokens[i] ; i += 1
        assert tok1.kind in "({["
       
        if   tok1.kind == '(': delim = ')'
        elif tok1.kind == '{': delim = '}'
        else:                  delim = ']'
    
        level = 1
        while i < len(tokens):
            tok = tokens[i]
            # g.trace(level,delim,tok.kind)
            i += 1
            if tok.kind == tok1.kind:
                level += 1
            elif tok.kind == delim:
                level -= 1
                if level == 0: return i-1
    
        self.warning("%s not matched by %s" % (tok1.kind,delim))
        return None
    #@nonl
    #@-node:findMatchingBracket
    #@+node:findTokens
    def findTokens(self,tokens,i,findTokens):
        
        """Search for a match with findTokens.
        Return i,i+len(findTokens) if found, or None,None otherwise."""
    
        e = self
        
        while i < len(tokens):
            
            if e.matchTokens(tokens,i,findTokens):
                return i,i+len(findTokens)
            else:
                i += 1
    
        return None,None # Not found
    #@nonl
    #@-node:findTokens
    #@+node:isMatchingBracket
    def isMatchingBracket(self,tokens,i,j):
        
        toki = tokens[i]
        tokj = tokens[j]
    
        f1 = "({[".find(toki.kind)
        f2 = ")}]".find(tokj.kind)
        
        # g.trace(f1,f2,repr(toki.kind),repr(tokj.kind))
        
        return f1 == f2 and f1 != -1
    #@nonl
    #@-node:isMatchingBracket
    #@+node:isStatement
    def isStatement (self,tokens,i):
        
        """Returns the statement or function f if (f is at tokens[i]."""
        
        e = self
        
        for s in e.allStatements:
            toks = [tok('('),tok('id',s)]
            if e.matchTokens(tokens,i,toks):
                return s
    
        return False
          
        
    #@-node:isStatement
    #@+node:matchTokens
    def matchTokens (self,tokens,i,findTokens):
        
        """Return True if tokens match findTokens at position i."""
    
        j = 0
        while j < len(findTokens):
            tok = tokens[i+j]
            ftok = findTokens[j]
            if not tok.match(ftok):
                return False
            j += 1
        return True
    #@nonl
    #@-node:matchTokens
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
                j = g.skip_id(s,i,chars='-*') # '-*' valid in elisp.
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
        e.tokens = e.parse(e.tokens)
    
        if 0: # Old code: superceded by parser.
            e.tokens = e.createPythonIndentation(e.tokens)
            e.tokens = e.removeBlankLines(e.tokens)
    #@nonl
    #@-node:convert (main line)
    #@+node:createPythonIndentation
    def createPythonIndentation (self,tokens,level=0):
        
        e = self ; p = e.p
        i = 0
        while i < len(tokens):
            if e.isStatement(tokens,i):
                # e.dump(tokens[i:i+2])
                j = e.findMatchingBracket(tokens,i)
                if j is not None:
                    assert e.isMatchingBracket(tokens,i,j)
                    # Strip off the matching brackets
                    newTokens = e.createIndentedBlock(tokens[i+1:j],level+1)
                    if newTokens:
                        # Recursively handle all inner statements.
                        newTokens = e.createPythonIndentation(newTokens,level+1)
                        tokens[i:j+1] = newTokens
                        assert not e.isStatement(tokens,i)
                        i = j # No need to rescan.
            else:
                i += 1
    
        return tokens
    #@nonl
    #@-node:createPythonIndentation
    #@+node:createIndentedBlock
    def createIndentedBlock (self,tokens,level):
        
        e = self ; p = e.p ; level1 = level
        
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.kind == '(':
                #@            << insert nl and ws tokens >>
                #@+node:<< insert nl and ws tokens >>
                ws = tok("ws",' '*e.tabwidth*level)
                nl = tok('\n','\n')
                tokens.insert(i,nl)
                tokens.insert(i+1,ws)
                #@nonl
                #@-node:<< insert nl and ws tokens >>
                #@nl
                level += 1
                i += 3
            elif t.kind == ')':
                level -= 1 ; i += 1
            elif t.kind == "string" and level == level1:
                #@            << insert nl and ws tokens >>
                #@+node:<< insert nl and ws tokens >>
                ws = tok("ws",' '*e.tabwidth*level)
                nl = tok('\n','\n')
                tokens.insert(i,nl)
                tokens.insert(i+1,ws)
                #@nonl
                #@-node:<< insert nl and ws tokens >>
                #@nl
                i += 3
            else:
                i += 1
    
        return tokens
    #@nonl
    #@-node:createIndentedBlock
    #@+node:removeBlankLines
    def removeBlankLines (self,tokens):
        
        e = self
        
        i = 0
        while i < len(tokens):
            
            if tokens[i].kind == '\n':
                j = i ; i += 1
                while i < len(tokens) and tokens[i].kind == "ws":
                    i += 1
                if i >= len(tokens) or tokens[i].kind == '\n':
                    del tokens[j:i]
                    i = j
                else: i += 1
            else: i += 1
                
        return tokens
    #@nonl
    #@-node:removeBlankLines
    #@-node:Converters
    #@+node:Parser & allies
    #@+node:parse
    def parse (self,tokens,topLevel=True):
        
        """A recursive-descent parser for elisp."""
        
        e = self
        i = 0
        while i < len(tokens):
            # g.trace(tokens[i].kind)
            if tokens[i].kind != '(':
                i += 1 ; continue
            j = e.findMatchingBracket(tokens,i)
            fTok = i+1 < len(tokens) and tokens[i+1]
            if j is None:
                #@            << give error message about mismatched parens >>
                #@+node:<< give error message about mismatched parens >>
                if fTok:
                    e.error("No (%s has no matching ')'" % fTok.kind)
                else:
                    e.error("Mismatched parens")
                #@nonl
                #@-node:<< give error message about mismatched parens >>
                #@nl
                i += 1 ; continue
            # Strip off the matching parens.
            block = tokens[i+1:j]
            parseTree = e.block(block)
            # A top-level token is helpful for dumping, etc.
            if topLevel: token = tok('TREE','TREE',parseTree)
            else:        token = parseTree
            tokens[i:j+1] = [token]
            # We are replacing everyting by a _single_ token.
            i = i + 1 
                
        return tokens
    #@nonl
    #@-node:parse
    #@+node:block
    def block (self,tokens):
        
        """Parse a block of tokens."""
        
        e = self
    
        i = 0 ; result = []
        while i < len(tokens):
            if tokens[i].kind == '(':
                j = e.findMatchingBracket(tokens,i)
                if j is None:
                    # To do: print error message.
                    i += 1
                else:
                    # Strip off the matching parens.
                    block = tokens[i+1:j]
                    # Recursively parse this block.
                    result.append(e.parse(block,topLevel=False))
                    i = j + 1
            else:
                result.append(tokens[i])
                i += 1
    
        return result
    #@nonl
    #@-node:block
    #@-node:Parser & allies
    #@-others
#@nonl
#@-node:class elisp2pyClass
#@-others
#@-node:@file ../src/elisp2py.py
#@-leo
