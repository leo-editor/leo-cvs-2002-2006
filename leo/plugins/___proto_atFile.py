#@+leo-ver=4-thin
#@+node:ekr.20040929104807.2:@thin ___proto_atFile.py
"""Classes to read and write @file nodes."""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20040929105133.1:<< imports >>
import leoGlobals as g

if g.app.config.use_psyco:
    # print "enabled psyco classes",__file__
    try: from psyco.classes import *
    except ImportError: pass
    
import leoColor
import leoNodes
import os
import string
import time
#@nonl
#@-node:ekr.20040929105133.1:<< imports >>
#@nl

#@+others
#@+node:ekr.20041001142542:getScript
def getScript (c,p,useSelectedText=True):

    if not p: p = c.currentPosition()
    old_body = p.bodyString()
    
    try:
        script = ""
        # Allow p not to be the present position.
        if p == c.currentPosition():
            if useSelectedText and c.frame.body.hasTextSelection():
                # Temporarily replace v's body text with just the selected text.
                s = c.frame.body.getSelectedText()
                p.v.setTnodeText(s)
            else:
                s = c.frame.body.getAllText()
        else:
            s = p.bodyString()
    
        if s.strip():
            g.app.scriptDict["script1"]=s
            
            if 1: df = c.atFileCommands
            else: df = c.atFileCommands.new_df

            df.scanAllDirectives(p,scripting=True)
            # Force Python comment delims.
            df.startSentinelComment = "#"
            df.endSentinelComment = None
            df.write(p.copy(),toString=True)
            script = df.stringOutput
            assert(p)
            g.app.scriptDict["script2"]=script
            error = len(script) == 0
    except:
        s = "unexpected exception"
        print s ; g.es(s)
        g.es_exception()
        script = ""

    p.v.setTnodeText(old_body)
    # g.trace(p,len(script))
    return script
#@nonl
#@-node:ekr.20041001142542:getScript
#@+node:ekr.20041001142542.1:class newAtFile
class newAtFile:
    
    #@    << define class constants >>
    #@+node:ekr.20040929105133.2:<< define class constants >>
    # These constants must be global to this module because they are shared by several classes.
    
    # The kind of at_directives.
    noDirective		   =  1 # not an at-directive.
    allDirective    =  2 # at-all (4.2)
    docDirective	   =  3 # @doc.
    atDirective		   =  4 # @<space> or @<newline>
    codeDirective	  =  5 # @code
    cDirective		    =  6 # @c<space> or @c<newline>
    othersDirective	=  7 # at-others
    miscDirective	  =  8 # All other directives
    rawDirective    =  9 # @raw
    endRawDirective = 10 # @end_raw
    
    # The kind of sentinel line.
    noSentinel		 = 20 # Not a sentinel
    endAt			 = 21 # @-at
    endBody			 = 22 # @-body
    # not used   = 23
    endDoc			 = 24 # @-doc
    endLeo			 = 25 # @-leo
    endNode			 = 26 # @-node
    endOthers		  = 27 # @-others
    
    # not used     = 40
    startAt			   = 41 # @+at
    startBody		    = 42 # @+body
    startDoc		     = 43 # @+doc
    startLeo		     = 44 # @+leo
    startNode		    = 45 # @+node
    startOthers		  = 46 # @+others
    
    startComment   = 60 # @comment
    startDelims		  = 61 # @delims
    startDirective	= 62 # @@
    startRef		     = 63 # @< < ... > >
    startVerbatim	 = 64 # @verbatim
    startVerbatimAfterRef = 65 # @verbatimAfterRef (3.0 only)
    
    # New in 4.x. Paired
    endAll         = 70 # at-all (4.2)
    endMiddle      = 71 # at-middle (4.2)
    startAll       = 72 # at+all (4.2)
    startMiddle    = 73 # at+middle (4.2)
    
    # New in 4.x.  Unpaired.
    startAfterRef  = 80 # @afterref (4.0)
    startClone     = 81 # @clone (4.2)
    startNl        = 82 # @nl (4.0)
    startNonl      = 83 # @nonl (4.0)
    #@nonl
    #@-node:ekr.20040929105133.2:<< define class constants >>
    #@nl
    #@    << define sentinelDict >>
    #@+node:ekr.20040929220155:<< define sentinelDict >>
    sentinelDict = {
    
        # Unpaired sentinels: 3.x and 4.x.
        "@comment" : startComment,
        "@delims" :  startDelims,
        "@verbatim": startVerbatim,
    
        # Unpaired sentinels: 3.x only.
        "@verbatimAfterRef": startVerbatimAfterRef,
    
        # Unpaired sentinels: 4.x only.
        "@afterref" : startAfterRef,
        "@clone"    : startClone,
        "@nl"       : startNl,
        "@nonl"     : startNonl,
    
        # Paired sentinels: 3.x only.
        "@+body":   startBody,   "@-body":   endBody,
    
        # Paired sentinels: 3.x and 4.x.
        "@+all":    startAll,    "@-all":    endAll,
        "@+at":     startAt,     "@-at":     endAt,
        "@+doc":    startDoc,    "@-doc":    endDoc,
        "@+leo":    startLeo,    "@-leo":    endLeo,
        "@+middle": startMiddle, "@-middle": endMiddle,
        "@+node":   startNode,   "@-node":   endNode,
        "@+others": startOthers, "@-others": endOthers,
    }
    #@nonl
    #@-node:ekr.20040929220155:<< define sentinelDict >>
    #@nl
    
    """The class implementing the atFile subcommander."""

    #@    @+others
    #@+node:ekr.20040929151734:Birth & init
    #@+node:ekr.20040929105133.4:atFile.__init__ & initIvars
    def __init__(self,c):
        
        at = self
        
        at.c = c
        at.fileCommands = at.c.fileCommands
        at.testing = True # True: enable additional checks.
    
        #@    << define the dispatch dictionary used by scanText4 >>
        #@+node:ekr.20040929110302:<< define the dispatch dictionary used by scanText4 >>
        at.dispatch_dict = {
            # Plain line.
            at.noSentinel: at.readNormalLine,
            # Starting sentinels...
            at.startAll:    at.readStartAll,
            at.startAt:     at.readStartAt,
            at.startDoc:    at.readStartDoc,
            at.startLeo:    at.readStartLeo,
            at.startMiddle: at.readStartMiddle,
            at.startNode:   at.readStartNode,
            at.startOthers: at.readStartOthers,
            # Ending sentinels...
            at.endAll:    at.readEndAll,
            at.endAt:     at.readEndAt,
            at.endDoc:    at.readEndDoc,
            at.endLeo:    at.readEndLeo,
            at.endMiddle: at.readEndMiddle,
            at.endNode:   at.readEndNode,
            at.endOthers: at.readEndOthers,
            # Non-paired sentinels.
            at.startAfterRef:  at.readAfterRef,
            at.startClone:     at.readClone,
            at.startComment:   at.readComment,
            at.startDelims:    at.readDelims,
            at.startDirective: at.readDirective,
            at.startNl:        at.readNl,
            at.startNonl:      at.readNonl,
            at.startRef:       at.readRef,
            at.startVerbatim:  at.readVerbatim,
            # Ignored 3.x sentinels
            at.endBody:               at.ignoreOldSentinel,
            at.startBody:             at.ignoreOldSentinel,
            at.startVerbatimAfterRef: at.ignoreOldSentinel }
        #@nonl
        #@-node:ekr.20040929110302:<< define the dispatch dictionary used by scanText4 >>
        #@nl
    #@nonl
    #@-node:ekr.20040929105133.4:atFile.__init__ & initIvars
    #@+node:ekr.20040929211438:initCommonIvars
    def initCommonIvars (self):
        
        """Init ivars common to both reading and writing.
        
        The defaults set here may be changed later."""
        
        at = self
        
        if self.testing:
            # Save "permanent" ivars
            c = at.c
            fileCommands = at.fileCommands
            dispatch_dict = at.dispatch_dict
            # Clear all ivars.
            g.clearAllIvars(self)
            # Restore permanent ivars
            at.testing = True
            at.c = c
            at.fileCommands = fileCommands
            at.dispatch_dict = dispatch_dict
    
        #@    << set defaults for arguments and options >>
        #@+node:ekr.20040929211438.1:<< set defaults for arguments and options >>
        # These may be changed in initReadIvars or initWriteIvars.
        
        # Support of output_newline option.
        self.output_newline = g.getOutputNewline()
        
        # Set by scanHeader when reading and scanAllDirectives when writing.
        self.encoding = g.app.config.default_derived_file_encoding
        self.endSentinelComment = ""
        self.startSentinelComment = ""
        
        # Set by scanAllDirectives when writing.
        self.default_directory = None
        self.page_width = None
        self.tab_width  = None
        self.startSentinelComment = ""
        self.endSentinelComment = ""
        self.language = None
        #@nonl
        #@-node:ekr.20040929211438.1:<< set defaults for arguments and options >>
        #@nl
        #@    << init common ivars >>
        #@+node:ekr.20040929111515.1:<< init common ivars >>
        # These may be set by initReadIvars or initWriteIvars.
        
        self.errors = 0
        self.inCode = True
        self.indent = 0  # The unit of indentation is spaces, not tabs.
        self.pending = []
        self.raw = False # True: in @raw mode
        self.root = None # The root of tree being read or written.
        self.root_seen = False # True: root vnode has been handled in this file.
        self.toString = False # True: sring-oriented read or write.
        #@nonl
        #@-node:ekr.20040929111515.1:<< init common ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20040929211438:initCommonIvars
    #@+node:ekr.20040929151859:initReadIvars
    def initReadIvars(self,root,fileName,
        importFileName=None,
        perfectImportRoot=None,
        thinFile=False):
            
        importing = importFileName is not None
    
        self.initCommonIvars()
        
        #@    << init ivars for reading >>
        #@+node:ekr.20040929211908:<< init ivars for reading >>
        self.cloneSibCount = 0 # n > 1: Make sure n cloned sibs exists at next @+node sentinel
        self.docOut = [] # The doc part being accumulated.
        self.done = False # True when @-leo seen.
        self.endSentinelStack = []
        self.importing = False
        self.importRootSeen = False
        self.indentStack = []
        self.inputFile = None
        self.lastLines = [] # The lines after @-leo
        self.lastThinNode = None # Used by createThinChild4.
        self.leadingWs = ""
        self.out = None
        self.outStack = []
        self.tnodeList = []
        self.tnodeListIndex = 0
        self.t = None
        self.tStack = []
        self.thinNodeStack = [] # Used by createThinChild4.
        self.updateWarningGiven = False
        #@-node:ekr.20040929211908:<< init ivars for reading >>
        #@nl
        
        self.scanDefaultDirectory(root,importing=importing)
        if self.errors: return
    
        # Init state from arguments.
        self.perfectImportRoot = perfectImportRoot
        self.importing = importing
        self.targetFileName = fileName
        self.thinFile = thinFile
    #@-node:ekr.20040929151859:initReadIvars
    #@+node:ekr.20040929151859.1:initWriteIvars
    def initWriteIvars(self,root,targetFileName,
        nosentinels=False,
        thinFile=False,
        toString=False):
    
        self.initCommonIvars()
    
        #@    << init ivars for writing >>
        #@+node:ekr.20040929212827:<< init ivars for writing >>>
        #@+at
        # When tangling, we first write to a temporary output file. After 
        # tangling is
        # temporary file. Otherwise we delete the old target file and rename 
        # the temporary
        # file to be the target file.
        #@-at
        #@@c
        
        self.docKind = None
        self.fileChangedFlag = False # True: the file has actually been updated.
        self.shortFileName = "" # short version of file name used for messages.
        self.thinFile = False
        
        if toString:
            self.outputFile = g.fileLikeObject()
            self.stringOutput = ""
            self.targetFileName = self.outputFileName = "<string-file>"
        else:
            self.outputFile = None # The temporary output file.
            self.stringOutput = None
            self.targetFileName = self.outputFileName = u""
        #@nonl
        #@-node:ekr.20040929212827:<< init ivars for writing >>>
        #@nl
        
        self.scanAllDirectives(root)
        if self.errors: return
        
        # Init state from arguments.
        self.targetFileName = targetFileName
        self.sentinels = not nosentinels
        self.thinFile = thinFile
        self.toString = toString
        self.root = root
        self.root.v.t.tnodeList = []
    #@nonl
    #@-node:ekr.20040929151859.1:initWriteIvars
    #@-node:ekr.20040929151734:Birth & init
    #@+node:ekr.20040930080842:Reading...
    #@+node:ekr.20040929105133.6:Reading (top level)
    #@+node:ekr.20040929162145:openFileForReading
    def openFileForReading(self,fileName):
        
        at = self
    
        fn = g.os_path_join(at.default_directory,fileName)
        fn = g.os_path_normpath(fn)
        
        try:
            # Open the file in binary mode to allow 0x1a in bodies & headlines.
            at.inputFile = open(fn,'rb')
            #@        << warn on read-only file >>
            #@+node:ekr.20040929105133.18:<< warn on read-only file >>
            # os.access() may not exist on all platforms.
            try:
                read_only = not os.access(fn,os.W_OK)
            except AttributeError:
                read_only = False 
                
            if read_only:
                g.es("read only: " + fn,color="red")
            #@nonl
            #@-node:ekr.20040929105133.18:<< warn on read-only file >>
            #@nl
    
        except IOError:
            at.error("can not open: '@file %s'" % (fn))
            at.inputFile = None
    #@nonl
    #@-node:ekr.20040929162145:openFileForReading
    #@+node:ekr.20040929105133.15:read
    # The caller must enclose this code in beginUpdate/endUpdate.
    
    def read(self,root,importFileName=None,thinFile=False):
        
        """Read any derived file."""
    
        at = self ; c = at.c
        #@    << set fileName >>
        #@+node:ekr.20040929105133.16:<< set fileName >>
        if importFileName:
            fileName = importFileName
        elif root.isAnyAtFileNode():
            fileName = root.anyAtFileNodeName()
        else:
            fileName = None
        
        if not fileName:
            at.error("Missing file name.  Restoring @file tree from .leo file.")
            return False
        #@nonl
        #@-node:ekr.20040929105133.16:<< set fileName >>
        #@nl
        self.initReadIvars(root,fileName,importFileName=importFileName,thinFile=thinFile)
        if at.errors: return False
        self.openFileForReading(fileName)
        if not at.inputFile: return False
        g.es("reading: " + root.headString())
        root.clearVisitedInTree()
        at.scanAllDirectives(root,importing=at.importing,reading=True)
        at.readOpenFile(root,at.inputFile,fileName)
        at.inputFile.close()
        root.clearDirty() # May be set dirty below.
        after = root.nodeAfterTree()
        #@    << warn about non-empty unvisited nodes >>
        #@+node:ekr.20040929105133.20:<< warn about non-empty unvisited nodes >>
        for p in root.self_and_subtree_iter():
        
            # g.trace(p)
            try: s = p.v.t.tempBodyString
            except: s = ""
            if s and not p.v.t.isVisited():
                at.error("Not in derived file:" + p.headString())
                p.v.t.setVisited() # One message is enough.
        #@nonl
        #@-node:ekr.20040929105133.20:<< warn about non-empty unvisited nodes >>
        #@nl
        if at.errors == 0 and not at.importing:
            #@        << copy all tempBodyStrings to tnodes >>
            #@+node:ekr.20040929105133.21:<< copy all tempBodyStrings to tnodes >>
            for p in root.self_and_subtree_iter():
                try: s = p.v.t.tempBodyString
                except: s = ""
                if s != p.bodyString():
                    if 0: # For debugging.
                        print ; print "changed: " + p.headString()
                        print ; print "new:",s
                        print ; print "old:",p.bodyString()
                    if thinFile:
                        p.v.setTnodeText(s)
                        if p.v.isDirty():
                            p.setAllAncestorAtFileNodesDirty()
                    else:
                        p.setBodyStringOrPane(s) # Sets v and v.c dirty.
                        
                    if not thinFile or (thinFile and p.v.isDirty()):
                        g.es("changed: " + p.headString(),color="blue")
                        p.setMarked()
            #@nonl
            #@-node:ekr.20040929105133.21:<< copy all tempBodyStrings to tnodes >>
            #@nl
        #@    << delete all tempBodyStrings >>
        #@+node:ekr.20040929105133.22:<< delete all tempBodyStrings >>
        for p in c.allNodes_iter():
            
            if hasattr(p.v.t,"tempBodyString"):
                delattr(p.v.t,"tempBodyString")
        #@nonl
        #@-node:ekr.20040929105133.22:<< delete all tempBodyStrings >>
        #@nl
        return at.errors == 0
    #@nonl
    #@-node:ekr.20040929105133.15:read
    #@+node:ekr.20040929105133.7:readAll
    def readAll(self,root,partialFlag=False):
        
        """Scan vnodes, looking for @file nodes to read."""
    
        at = self ; c = at.c
        c.endEditing() # Capture the current headline.
        anyRead = False
        p = root.copy()
        if partialFlag: after = p.nodeAfterTree()
        else: after = c.nullPosition()
        while p and not p.equal(after): # Don't use iterator.
            if p.isAtIgnoreNode():
                p.moveToNodeAfterTree()
            elif p.isAtThinFileNode():
                anyRead = True
                at.read(p,thinFile=True)
                p.moveToNodeAfterTree()
            elif p.isAtFileNode() or p.isAtNorefFileNode():
                anyRead = True
                wasOrphan = p.isOrphan()
                ok = at.read(p)
                if wasOrphan and not partialFlag and not ok:
                    # Remind the user to fix the problem.
                    p.setDirty()
                    c.setChanged(True)
                p.moveToNodeAfterTree()
            else: p.moveToThreadNext()
        # Clear all orphan bits.
        for p in c.allNodes_iter():
            p.v.clearOrphan()
            
        if partialFlag and not anyRead:
            g.es("no @file nodes in the selected tree")
    #@nonl
    #@-node:ekr.20040929105133.7:readAll
    #@+node:ekr.20040929105133.188:readOpenFile
    def readOpenFile(self,root,theFile,fileName):
        
        """Read an open derived file, either 3.x or 4.x."""
        
        at = self
    
        firstLines,read_new,isThinDerivedFile = at.scanHeader(theFile,fileName)
    
        if read_new:
            lastLines = at.scanText4(theFile,root)
        else:
            lastLines = at.scanText3(theFile,root,[],at.endLeo)
            
        root.v.t.setVisited() # Disable warning about set nodes.
    
        #@    << handle first and last lines >>
        #@+node:ekr.20040930084044:<< handle first and last lines >>
        try:
            body = root.v.t.tempBodyString
        except:
            body = ""
        
        lines = body.split('\n')
        at.completeFirstDirectives(lines,firstLines)
        at.completeLastDirectives(lines,lastLines)
        s = '\n'.join(lines).replace('\r', '')
        root.v.t.tempBodyString = s
        #@nonl
        #@-node:ekr.20040930084044:<< handle first and last lines >>
        #@nl
    #@nonl
    #@-node:ekr.20040929105133.188:readOpenFile
    #@-node:ekr.20040929105133.6:Reading (top level)
    #@+node:ekr.20040929105133.46:Reading (3.x)
    #@+node:ekr.20040929105133.51:createNthChild3
    #@+at 
    #@nonl
    # Sections appear in the derived file in reference order, not tree order.  
    # Therefore, when we insert the nth child of the parent there is no 
    # guarantee that the previous n-1 children have already been inserted. And 
    # it won't work just to insert the nth child as the last child if there 
    # aren't n-1 previous siblings.  For example, if we insert the third child 
    # followed by the second child followed by the first child the second and 
    # third children will be out of order.
    # 
    # To ensure that nodes are placed in the correct location we create 
    # "dummy" children as needed as placeholders.  In the example above, we 
    # would insert two dummy children when inserting the third child.  When 
    # inserting the other two children we replace the previously inserted 
    # dummy child with the actual children.
    # 
    # vnode child indices are zero-based.  Here we use 1-based indices.
    # 
    # With the "mirroring" scheme it is a structure error if we ever have to 
    # create dummy vnodes.  Such structure errors cause a second pass to be 
    # made, with an empty root.  This second pass will generate other 
    # structure errors, which are ignored.
    #@-at
    #@@c
    def createNthChild3(self,n,parent,headline):
        
        """Create the nth child of the parent."""
    
        at = self
        assert(n > 0)
        
        if at.importing:
            return at.createImportedNode(at.root,at.c,headline)
    
        # Create any needed dummy children.
        dummies = n - parent.numberOfChildren() - 1
        if dummies > 0:
            if 0: # CVS produces to many errors for this to be useful.
                g.es("dummy created")
            self.errors += 1
        while dummies > 0:
            dummies -= 1
            dummy = parent.insertAsLastChild(leoNodes.tnode())
            # The user should never see this headline.
            dummy.initHeadString("Dummy")
    
        if n <= parent.numberOfChildren():
            #@        << check the headlines >>
            #@+node:ekr.20040929105133.52:<< check the headlines >>
            # 1/24/03: A kludgy fix to the problem of headlines containing comment delims.
            
            result = parent.nthChild(n-1)
            resulthead = result.headString()
            
            if headline.strip() != resulthead.strip():
                start = self.startSentinelComment
                end = self.endSentinelComment
                if end and len(end) > 0:
                    # 1/25/03: The kludgy fix.
                    # Compare the headlines without the delims.
                    h1 =   headline.replace(start,"").replace(end,"")
                    h2 = resulthead.replace(start,"").replace(end,"")
                    if h1.strip() == h2.strip():
                        # 1/25/03: Another kludge: use the headline from the outline, not the derived file.
                        headline = resulthead
                    else:
                        self.errors += 1
                else:
                    self.errors += 1
            #@-node:ekr.20040929105133.52:<< check the headlines >>
            #@nl
        else:
            # This is using a dummy; we should already have bumped errors.
            result = parent.insertAsLastChild(leoNodes.tnode())
        result.initHeadString(headline)
        
        result.setVisited() # Suppress all other errors for this node.
        result.t.setVisited() # Suppress warnings about unvisited nodes.
        return result
    #@nonl
    #@-node:ekr.20040929105133.51:createNthChild3
    #@+node:ekr.20040929105133.53:handleLinesFollowingSentinel
    def handleLinesFollowingSentinel (self,lines,sentinel,comments = True):
        
        """convert lines following a sentinel to a single line"""
        
        m = " following" + sentinel + " sentinel"
        start = self.startSentinelComment
        end   = self.endSentinelComment
        
        if len(lines) == 1: # The expected case.
            s = lines[0]
        elif len(lines) == 5:
            self.readError("potential cvs conflict" + m)
            s = lines[1]
            g.es("using " + s)
        else:
            self.readError("unexpected lines" + m)
            g.es(len(lines), " lines" + m)
            s = "bad " + sentinel
            if comments: s = start + ' ' + s
    
        if comments:
            #@        << remove the comment delims from s >>
            #@+node:ekr.20040929105133.54:<< remove the comment delims from s >>
            # Remove the starting comment and the blank.
            # 5/1/03: The starting comment now looks like a sentinel, to warn users from changing it.
            comment = start + '@ '
            if g.match(s,0,comment):
                s = s[len(comment):]
            else:
                self.readError("expecting comment" + m)
            
            # Remove the trailing comment.
            if len(end) == 0:
                s = string.strip(s[:-1])
            else:
                k = s.rfind(end)
                s = string.strip(s[:k]) # works even if k == -1
            #@nonl
            #@-node:ekr.20040929105133.54:<< remove the comment delims from s >>
            #@nl
            
        # Undo the cweb hack: undouble @ signs if the opening comment delim ends in '@'.
        if start[-1:] == '@':
            s = s.replace('@@','@')
    
        return s
    #@nonl
    #@-node:ekr.20040929105133.53:handleLinesFollowingSentinel
    #@+node:ekr.20040929105133.56:readLinesToNextSentinel
    # We expect only a single line, and more may exist if cvs detects a conflict.
    # We accept the first line even if it looks like a sentinel.
    # 5/1/03: The starting comment now looks like a sentinel, to warn users from changing it.
    
    def readLinesToNextSentinel (self,theFile):
        
        """	read lines following multiline sentinels"""
        
        lines = []
        start = self.startSentinelComment + '@ '
        nextLine = self.readLine(theFile)
        while nextLine and len(nextLine) > 0:
            if len(lines) == 0:
                lines.append(nextLine)
                nextLine = self.readLine(theFile)
            else:
                # 5/1/03: looser test then calling sentinelKind3.
                s = nextLine ; i = g.skip_ws(s,0)
                if g.match(s,i,start):
                    lines.append(nextLine)
                    nextLine = self.readLine(theFile)
                else: break
    
        return nextLine,lines
    #@nonl
    #@-node:ekr.20040929105133.56:readLinesToNextSentinel
    #@+node:ekr.20040929105133.57:scanDoc3
    # Scans the doc part and appends the text out.
    # s,i point to the present line on entry.
    
    def scanDoc3(self,theFile,s,i,out,kind):
    
        endKind = g.choose(kind ==at.startDoc,at.endDoc,at.endAt)
        single = len(self.endSentinelComment) == 0
        #@    << Skip the opening sentinel >>
        #@+node:ekr.20040929105133.58:<< Skip the opening sentinel >>
        assert(g.match(s,i,g.choose(kind == at.startDoc, "+doc", "+at")))
        
        out.append(g.choose(kind == at.startDoc, "@doc", "@"))
        s = self.readLine(theFile)
        #@-node:ekr.20040929105133.58:<< Skip the opening sentinel >>
        #@nl
        #@    << Skip an opening block delim >>
        #@+node:ekr.20040929105133.59:<< Skip an opening block delim >>
        if not single:
            j = g.skip_ws(s,0)
            if g.match(s,j,self.startSentinelComment):
                s = self.readLine(theFile)
        #@nonl
        #@-node:ekr.20040929105133.59:<< Skip an opening block delim >>
        #@nl
        nextLine = None ; kind = at.noSentinel
        while len(s) > 0:
            #@        << set kind, nextLine >>
            #@+node:ekr.20040929105133.60:<< set kind, nextLine >>
            #@+at 
            #@nonl
            # For non-sentinel lines we look ahead to see whether the next 
            # line is a sentinel.
            #@-at
            #@@c
            
            assert(nextLine==None)
            
            kind = self.sentinelKind3(s)
            
            if kind == at.noSentinel:
                j = g.skip_ws(s,0)
                blankLine = s[j] == '\n'
                nextLine = self.readLine(theFile)
                nextKind = self.sentinelKind3(nextLine)
                if blankLine and nextKind == endKind:
                    kind = endKind # stop the scan now
            #@-node:ekr.20040929105133.60:<< set kind, nextLine >>
            #@nl
            if kind == endKind: break
            #@        << Skip the leading stuff >>
            #@+node:ekr.20040929105133.61:<< Skip the leading stuff >>
            # Point i to the start of the real line.
            
            if single: # Skip the opening comment delim and a blank.
                i = g.skip_ws(s,0)
                if g.match(s,i,self.startSentinelComment):
                    i += len(self.startSentinelComment)
                    if g.match(s,i," "): i += 1
            else:
                i = self.skipIndent(s,0, self.indent)
            #@-node:ekr.20040929105133.61:<< Skip the leading stuff >>
            #@nl
            #@        << Append s to out >>
            #@+node:ekr.20040929105133.62:<< Append s to out >>
            # Append the line with a newline if it is real
            
            line = s[i:-1] # remove newline for rstrip.
            
            if line == line.rstrip():
                # no trailing whitespace: the newline is real.
                out.append(line + '\n')
            else:
                # trailing whitespace: the newline is not real.
                out.append(line)
            #@-node:ekr.20040929105133.62:<< Append s to out >>
            #@nl
            if nextLine:
                s = nextLine ; nextLine = None
            else: s = self.readLine(theFile)
        if kind != endKind:
            self.readError("Missing " + self.sentinelName(endKind) + " sentinel")
        #@    << Remove a closing block delim from out >>
        #@+node:ekr.20040929105133.63:<< Remove a closing block delim from out >>
        # This code will typically only be executed for HTML files.
        
        if not single:
        
            delim = self.endSentinelComment
            n = len(delim)
            
            # Remove delim and possible a leading newline.
            s = string.join(out,"")
            s = s.rstrip()
            if s[-n:] == delim:
                s = s[:-n]
            if s[-1] == '\n':
                s = s[:-1]
                
            # Rewrite out in place.
            del out[:]
            out.append(s)
        #@-node:ekr.20040929105133.63:<< Remove a closing block delim from out >>
        #@nl
    #@nonl
    #@-node:ekr.20040929105133.57:scanDoc3
    #@+node:ekr.20040929105133.64:scanText3
    def scanText3 (self,theFile,p,out,endSentinelKind,nextLine=None):
        
        """Scan a 3.x derived file recursively."""
    
        at = self # 12/18/03
        lastLines = [] # The lines after @-leo
        lineIndent = 0 ; linep = 0 # Changed only for sentinels.
        while 1:
            #@        << put the next line into s >>
            #@+node:ekr.20040929105133.65:<< put the next line into s >>
            if nextLine:
                s = nextLine ; nextLine = None
            else:
                s = self.readLine(theFile)
                if len(s) == 0: break
            #@nonl
            #@-node:ekr.20040929105133.65:<< put the next line into s >>
            #@nl
            #@        << set kind, nextKind >>
            #@+node:ekr.20040929105133.66:<< set kind, nextKind >>
            #@+at 
            #@nonl
            # For non-sentinel lines we look ahead to see whether the next 
            # line is a sentinel.  If so, the newline that ends a non-sentinel 
            # line belongs to the next sentinel.
            #@-at
            #@@c
            
            assert(nextLine==None)
            
            kind = self.sentinelKind3(s)
            
            if kind == at.noSentinel:
                nextLine = self.readLine(theFile)
                nextKind = self.sentinelKind3(nextLine)
            else:
                nextLine = nextKind = None
            
            # nextLine != None only if we have a non-sentinel line.
            # Therefore, nextLine == None whenever scanText3 returns.
            #@nonl
            #@-node:ekr.20040929105133.66:<< set kind, nextKind >>
            #@nl
            if kind != at.noSentinel:
                #@            << set lineIndent, linep and leading_ws >>
                #@+node:ekr.20040929105133.67:<< Set lineIndent, linep and leading_ws >>
                #@+at 
                #@nonl
                # lineIndent is the total indentation on a sentinel line.  The 
                # first "self.indent" portion of that must be removed when 
                # recreating text.  leading_ws is the remainder of the leading 
                # whitespace.  linep points to the first "real" character of a 
                # line, the character following the "indent" whitespace.
                #@-at
                #@@c
                
                # Point linep past the first self.indent whitespace characters.
                if self.raw: # 10/15/02
                    linep =0
                else:
                    linep = self.skipIndent(s,0,self.indent)
                
                # Set lineIndent to the total indentation on the line.
                lineIndent = 0 ; i = 0
                while i < len(s):
                    if s[i] == '\t': lineIndent += (abs(self.tab_width) - (lineIndent % abs(self.tab_width)))
                    elif s[i] == ' ': lineIndent += 1
                    else: break
                    i += 1
                # g.trace("lineIndent,s:",lineIndent,s)
                
                # Set leading_ws to the additional indentation on the line.
                leading_ws = s[linep:i]
                #@nonl
                #@-node:ekr.20040929105133.67:<< Set lineIndent, linep and leading_ws >>
                #@nl
                i = self.skipSentinelStart3(s,0)
            #@        << handle the line in s >>
            #@+node:ekr.20040929105133.68:<< handle the line in s >>
            if kind == at.noSentinel:
                #@    << append non-sentinel line >>
                #@+node:ekr.20040929105133.69:<< append non-sentinel line >>
                # We don't output the trailing newline if the next line is a sentinel.
                if self.raw: # 10/15/02
                    i = 0
                else:
                    i = self.skipIndent(s,0,self.indent)
                
                assert(nextLine != None)
                
                if nextKind == at.noSentinel:
                    line = s[i:]
                    out.append(line)
                else:
                    line = s[i:-1] # don't output the newline
                    out.append(line)
                #@-node:ekr.20040929105133.69:<< append non-sentinel line >>
                #@nl
            #@<< handle common sentinels >>
            #@+node:ekr.20040929105133.70:<< handle common sentinels >>
            elif kind in (at.endAt, at.endBody,at.endDoc,at.endLeo,at.endNode,at.endOthers):
                    #@        << handle an ending sentinel >>
                    #@+node:ekr.20040929105133.71:<< handle an ending sentinel >>
                    # g.trace("end sentinel:", self.sentinelName(kind))
                    
                    if kind == endSentinelKind:
                        if kind == at.endLeo:
                            # Ignore everything after @-leo.
                            # Such lines were presumably written by @last.
                            while 1:
                                s = self.readLine(theFile)
                                if len(s) == 0: break
                                lastLines.append(s) # Capture all trailing lines, even if empty.
                        elif kind == at.endBody:
                            self.raw = False
                        # nextLine != None only if we have a non-sentinel line.
                        # Therefore, nextLine == None whenever scanText3 returns.
                        assert(nextLine==None)
                        return lastLines # End the call to scanText3.
                    else:
                        # Tell of the structure error.
                        name = self.sentinelName(kind)
                        expect = self.sentinelName(endSentinelKind)
                        self.readError("Ignoring " + name + " sentinel.  Expecting " + expect)
                    #@nonl
                    #@-node:ekr.20040929105133.71:<< handle an ending sentinel >>
                    #@nl
            elif kind == at.startBody:
                #@    << scan @+body >>
                #@+node:ekr.20040929105133.72:<< scan @+body >> 3.x
                assert(g.match(s,i,"+body"))
                
                child_out = [] ; child = p.copy() # Do not change out or p!
                oldIndent = self.indent ; self.indent = lineIndent
                self.scanText3(theFile,child,child_out,at.endBody)
                
                # Set the body, removing cursed newlines.
                # This must be done here, not in the @+node logic.
                body = string.join(child_out, "")
                body = body.replace('\r', '')
                body = g.toUnicode(body,g.app.tkEncoding) # 9/28/03
                
                if self.importing:
                    child.t.bodyString = body
                else:
                    child.t.tempBodyString = body
                
                self.indent = oldIndent
                #@nonl
                #@-node:ekr.20040929105133.72:<< scan @+body >> 3.x
                #@nl
            elif kind == at.startNode:
                #@    << scan @+node >>
                #@+node:ekr.20040929105133.73:<< scan @+node >>
                assert(g.match(s,i,"+node:"))
                i += 6
                
                childIndex = 0 ; cloneIndex = 0
                #@<< Set childIndex >>
                #@+node:ekr.20040929105133.74:<< Set childIndex >>
                i = g.skip_ws(s,i) ; j = i
                while i < len(s) and s[i] in string.digits:
                    i += 1
                
                if j == i:
                    self.readError("Implicit child index in @+node")
                    childIndex = 0
                else:
                    childIndex = int(s[j:i])
                
                if g.match(s,i,':'):
                    i += 1 # Skip the ":".
                else:
                    self.readError("Bad child index in @+node")
                #@nonl
                #@-node:ekr.20040929105133.74:<< Set childIndex >>
                #@nl
                #@<< Set cloneIndex >>
                #@+node:ekr.20040929105133.75:<< Set cloneIndex >>
                while i < len(s) and s[i] != ':' and not g.is_nl(s,i):
                    if g.match(s,i,"C="):
                        # set cloneIndex from the C=nnn, field
                        i += 2 ; j = i
                        while i < len(s) and s[i] in string.digits:
                            i += 1
                        if j < i:
                            cloneIndex = int(s[j:i])
                    else: i += 1 # Ignore unknown status bits.
                
                if g.match(s,i,":"):
                    i += 1
                else:
                    self.readError("Bad attribute field in @+node")
                #@nonl
                #@-node:ekr.20040929105133.75:<< Set cloneIndex >>
                #@nl
                headline = ""
                #@<< Set headline and ref >>
                #@+node:ekr.20040929105133.76:<< Set headline and ref >>
                # Set headline to the rest of the line.
                # 6/22/03: don't strip leading whitespace.
                if len(self.endSentinelComment) == 0:
                    headline = s[i:-1].rstrip()
                else:
                    # 10/24/02: search from the right, not the left.
                    k = s.rfind(self.endSentinelComment,i)
                    headline = s[i:k].rstrip() # works if k == -1
                    
                # 10/23/02: The cweb hack: undouble @ signs if the opening comment delim ends in '@'.
                if self.startSentinelComment[-1:] == '@':
                    headline = headline.replace('@@','@')
                
                # Set reference if it exists.
                i = g.skip_ws(s,i)
                
                if 0: # no longer used
                    if g.match(s,i,"<<"):
                        k = s.find(">>",i)
                        if k != -1: ref = s[i:k+2]
                #@nonl
                #@-node:ekr.20040929105133.76:<< Set headline and ref >>
                #@nl
                
                # print childIndex,headline
                
                if childIndex == 0: # The root node.
                    if not at.importing:
                        #@        << Check the filename in the sentinel >>
                        #@+node:ekr.20040929105133.77:<< Check the filename in the sentinel >>
                        h = headline.strip()
                        
                        if h[:5] == "@file":
                            i,junk,junk = g.scanAtFileOptions(h)
                            fileName = string.strip(h[i:])
                            if fileName != self.targetFileName:
                                self.readError("File name in @node sentinel does not match file's name")
                        elif h[:8] == "@rawfile":
                            fileName = string.strip(h[8:])
                            if fileName != self.targetFileName:
                                self.readError("File name in @node sentinel does not match file's name")
                        else:
                            self.readError("Missing @file in root @node sentinel")
                        #@-node:ekr.20040929105133.77:<< Check the filename in the sentinel >>
                        #@nl
                    # Put the text of the root node in the current node.
                    self.scanText3(theFile,p,out,at.endNode)
                    p.v.t.setCloneIndex(cloneIndex)
                    # if cloneIndex > 0: g.trace("clone index:",cloneIndex,p)
                else:
                    # NB: this call to createNthChild3 is the bottleneck!
                    child = self.createNthChild3(childIndex,p,headline)
                    child.t.setCloneIndex(cloneIndex)
                    # if cloneIndex > 0: g.trace("cloneIndex,child:"cloneIndex,child)
                    self.scanText3(theFile,child,out,at.endNode)
                
                #@<< look for sentinels that may follow a reference >>
                #@+node:ekr.20040929105133.78:<< look for sentinels that may follow a reference >>
                s = self.readLine(theFile)
                kind = self.sentinelKind3(s)
                
                if len(s) > 1 and kind == at.startVerbatimAfterRef:
                    s = self.readLine(theFile)
                    # g.trace("verbatim:",repr(s))
                    out.append(s)
                elif len(s) > 1 and self.sentinelKind3(s) == at.noSentinel:
                    out.append(s)
                else:
                    nextLine = s # Handle the sentinel or blank line later.
                
                #@-node:ekr.20040929105133.78:<< look for sentinels that may follow a reference >>
                #@nl
                #@nonl
                #@-node:ekr.20040929105133.73:<< scan @+node >>
                #@nl
            elif kind == at.startRef:
                #@    << scan old ref >>
                #@+node:ekr.20040929105133.79:<< scan old ref >> (3.0)
                #@+at 
                #@nonl
                # The sentinel contains an @ followed by a section name in 
                # angle brackets.  This code is different from the code for 
                # the @@ sentinel: the expansion of the reference does not 
                # include a trailing newline.
                #@-at
                #@@c
                
                assert(g.match(s,i,"<<"))
                
                if len(self.endSentinelComment) == 0:
                    line = s[i:-1] # No trailing newline
                else:
                    k = s.find(self.endSentinelComment,i)
                    line = s[i:k] # No trailing newline, whatever k is.
                        
                # 10/30/02: undo cweb hack here
                start = self.startSentinelComment
                if start and len(start) > 0 and start[-1] == '@':
                    line = line.replace('@@','@')
                
                out.append(line)
                #@nonl
                #@-node:ekr.20040929105133.79:<< scan old ref >> (3.0)
                #@nl
            elif kind == at.startAt:
                #@    << scan @+at >>
                #@+node:ekr.20040929105133.80:<< scan @+at >>
                assert(g.match(s,i,"+at"))
                self.scanDoc3(theFile,s,i,out,kind)
                #@nonl
                #@-node:ekr.20040929105133.80:<< scan @+at >>
                #@nl
            elif kind == at.startDoc:
                #@    << scan @+doc >>
                #@+node:ekr.20040929105133.81:<< scan @+doc >>
                assert(g.match(s,i,"+doc"))
                self.scanDoc3(theFile,s,i,out,kind)
                #@nonl
                #@-node:ekr.20040929105133.81:<< scan @+doc >>
                #@nl
            elif kind == at.startOthers:
                #@    << scan @+others >>
                #@+node:ekr.20040929105133.82:<< scan @+others >>
                assert(g.match(s,i,"+others"))
                
                # Make sure that the generated at-others is properly indented.
                out.append(leading_ws + "@others")
                
                self.scanText3(theFile,p,out,at.endOthers)
                #@nonl
                #@-node:ekr.20040929105133.82:<< scan @+others >>
                #@nl
            #@nonl
            #@-node:ekr.20040929105133.70:<< handle common sentinels >>
            #@nl
            #@<< handle rare sentinels >>
            #@+node:ekr.20040929105133.83:<< handle rare sentinels >>
            elif kind == at.startComment:
                #@    << scan @comment >>
                #@+node:ekr.20040929105133.84:<< scan @comment >>
                assert(g.match(s,i,"comment"))
                
                # We need do nothing more to ignore the comment line!
                #@-node:ekr.20040929105133.84:<< scan @comment >>
                #@nl
            elif kind == at.startDelims:
                #@    << scan @delims >>
                #@+node:ekr.20040929105133.85:<< scan @delims >>
                assert(g.match(s,i-1,"@delims"));
                
                # Skip the keyword and whitespace.
                i0 = i-1
                i = g.skip_ws(s,i-1+7)
                    
                # Get the first delim.
                j = i
                while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
                    i += 1
                
                if j < i:
                    self.startSentinelComment = s[j:i]
                    # print "delim1:", self.startSentinelComment
                
                    # Get the optional second delim.
                    j = i = g.skip_ws(s,i)
                    while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
                        i += 1
                    end = g.choose(j<i,s[j:i],"")
                    i2 = g.skip_ws(s,i)
                    if end == self.endSentinelComment and (i2 >= len(s) or g.is_nl(s,i2)):
                        self.endSentinelComment = "" # Not really two params.
                        line = s[i0:j]
                        line = line.rstrip()
                        out.append(line+'\n')
                    else:
                        self.endSentinelComment = end
                        # print "delim2:",end
                        line = s[i0:i]
                        line = line.rstrip()
                        out.append(line+'\n')
                else:
                    self.readError("Bad @delims")
                    # Append the bad @delims line to the body text.
                    out.append("@delims")
                #@nonl
                #@-node:ekr.20040929105133.85:<< scan @delims >>
                #@nl
            elif kind == at.startDirective:
                #@    << scan @@ >>
                #@+node:ekr.20040929105133.86:<< scan @@ >>
                # The first '@' has already been eaten.
                assert(g.match(s,i,"@"))
                
                if g.match_word(s,i,"@raw"):
                    self.raw = True
                elif g.match_word(s,i,"@end_raw"):
                    self.raw = False
                
                e = self.endSentinelComment
                s2 = s[i:]
                if len(e) > 0:
                    k = s.rfind(e,i)
                    if k != -1:
                        s2 = s[i:k] + '\n'
                    
                start = self.startSentinelComment
                if start and len(start) > 0 and start[-1] == '@':
                    s2 = s2.replace('@@','@')
                out.append(s2)
                # g.trace(s2)
                #@nonl
                #@-node:ekr.20040929105133.86:<< scan @@ >>
                #@nl
            elif kind == at.startLeo:
                #@    << scan @+leo >>
                #@+node:ekr.20040929105133.87:<< scan @+leo >>
                assert(g.match(s,i,"+leo"))
                self.readError("Ignoring unexpected @+leo sentinel")
                #@nonl
                #@-node:ekr.20040929105133.87:<< scan @+leo >>
                #@nl
            elif kind == at.startVerbatim:
                #@    << scan @verbatim >>
                #@+node:ekr.20040929105133.88:<< scan @verbatim >>
                assert(g.match(s,i,"verbatim"))
                
                # Skip the sentinel.
                s = self.readLine(theFile) 
                
                # Append the next line to the text.
                i = self.skipIndent(s,0,self.indent)
                out.append(s[i:])
                #@-node:ekr.20040929105133.88:<< scan @verbatim >>
                #@nl
            #@nonl
            #@-node:ekr.20040929105133.83:<< handle rare sentinels >>
            #@nl
            else:
                #@    << warn about unknown sentinel >>
                #@+node:ekr.20040929105133.89:<< warn about unknown sentinel >>
                j = i
                i = g.skip_line(s,i)
                line = s[j:i]
                self.readError("Unknown sentinel: " + line)
                #@nonl
                #@-node:ekr.20040929105133.89:<< warn about unknown sentinel >>
                #@nl
            #@nonl
            #@-node:ekr.20040929105133.68:<< handle the line in s >>
            #@nl
        #@    << handle unexpected end of text >>
        #@+node:ekr.20040929105133.90:<< handle unexpected end of text >>
        # Issue the error.
        name = self.sentinelName(endSentinelKind)
        self.readError("Unexpected end of file. Expecting " + name + "sentinel" )
        #@-node:ekr.20040929105133.90:<< handle unexpected end of text >>
        #@nl
        assert(len(s)==0 and nextLine==None) # We get here only if readline fails.
        return lastLines # We get here only if there are problems.
    #@nonl
    #@-node:ekr.20040929105133.64:scanText3
    #@+node:ekr.20040929105133.100:sentinelKind3
    def sentinelKind3(self,s):
    
        """This method tells what kind of sentinel appears in line s.
        
        Typically s will be an empty line before the actual sentinel,
        but it is also valid for s to be an actual sentinel line.
        
        Returns (kind, s, emptyFlag), where emptyFlag is True if
        kind == at.noSentinel and s was an empty line on entry."""
    
        i = g.skip_ws(s,0)
        if g.match(s,i,self.startSentinelComment):
            i += len(self.startSentinelComment)
        else:
            return at.noSentinel
    
        # 10/30/02: locally undo cweb hack here
        start = self.startSentinelComment
        if start and len(start) > 0 and start[-1] == '@':
            s = s[:i] + string.replace(s[i:],'@@','@')
    
        # Do not skip whitespace here!
        if g.match(s,i,"@<<"): return at.startRef
        if g.match(s,i,"@@"):   return at.startDirective
        if not g.match(s,i,'@'): return at.noSentinel
        j = i # start of lookup
        i += 1 # skip the at sign.
        if g.match(s,i,'+') or g.match(s,i,'-'):
            i += 1
        i = g.skip_c_id(s,i)
        key = s[j:i]
        if len(key) > 0 and at.sentinelDict.has_key(key):
            # g.trace("found:",key)
            return at.sentinelDict[key]
        else:
            # g.trace("not found:",key)
            return at.noSentinel
    #@nonl
    #@-node:ekr.20040929105133.100:sentinelKind3
    #@+node:ekr.20040929105133.102:skipSentinelStart3
    def skipSentinelStart3(self,s,i):
        
        """Skip the start of a sentinel."""
    
        start = self.startSentinelComment
        assert(start and len(start)>0)
    
        if g.is_nl(s,i): i = g.skip_nl(s,i)
    
        i = g.skip_ws(s,i)
        assert(g.match(s,i,start))
        i += len(start)
    
        # 7/8/02: Support for REM hack
        i = g.skip_ws(s,i)
        assert(i < len(s) and s[i] == '@')
        return i + 1
    #@-node:ekr.20040929105133.102:skipSentinelStart3
    #@-node:ekr.20040929105133.46:Reading (3.x)
    #@+node:ekr.20040929105133.186:Reading (4.x)
    #@+node:ekr.20040929105133.187:createThinChild4
    def createThinChild4 (self,gnxString,headline):
    
        """Find or create a new vnode whose parent is at.lastThinNode."""
    
        at = self ; v = at.root.v ; c = at.c ; indices = g.app.nodeIndices
        last = at.lastThinNode ; lastIndex = last.t.fileIndex
        gnx = indices.scanGnx(gnxString,0)
        #g.trace("last",last,last.t.fileIndex)
        #g.trace("args",indices.areEqual(gnx,last.t.fileIndex),gnxString,headline)
        
        # See if there is already a child with the proper index.
        child = at.lastThinNode.firstChild()
        while child and not indices.areEqual(gnx,child.t.fileIndex):
            child = child.next()
    
        if at.cloneSibCount > 1:
            n = at.cloneSibCount ; at.cloneSibCount = 0
            if child: clonedSibs,junk = at.scanForClonedSibs(child)
            else: clonedSibs = 0
            copies = n - clonedSibs
            # g.trace(copies,headline)
        else:
            if indices.areEqual(gnx,lastIndex):
                return last
            if child:
                return child
            copies = 1 # Create exactly one copy.
    
        while copies > 0:
            copies -= 1
            # Create the tnode only if it does not already exist.
            tnodesDict = c.fileCommands.tnodesDict
            t = tnodesDict.get(gnxString)
            if t:
                assert(indices.areEqual(t.fileIndex,gnx))
            else:
                t = leoNodes.tnode(bodyString=None,headString=headline)
                t.fileIndex = gnx
                tnodesDict[gnxString] = t
            parent = at.lastThinNode
            child = leoNodes.vnode(c,t)
            t.vnodeList.append(child)
            child.linkAsNthChild(parent,parent.numberOfChildren())
            # g.trace("creating node",child,gnx)
    
        return child
    #@nonl
    #@-node:ekr.20040929105133.187:createThinChild4
    #@+node:ekr.20040929105133.189:findChild4
    def findChild4 (self,headline):
        
        """Return the next tnode in at.root.t.tnodeList."""
    
        at = self ; v = at.root.v
    
        if not hasattr(v.t,"tnodeList"):
            at.readError("no tnodeList for " + repr(v))
            g.es("Write the @file node or use the Import Derived File command")
            g.trace("no tnodeList for ",v)
            return None
            
        if at.tnodeListIndex >= len(v.t.tnodeList):
            at.readError("bad tnodeList index: %d, %s" % (at.tnodeListIndex,repr(v)))
            g.trace("bad tnodeList index",at.tnodeListIndex,len(v.t.tnodeList),v)
            return None
            
        t = v.t.tnodeList[at.tnodeListIndex]
        assert(t)
        at.tnodeListIndex += 1
    
        # Get any vnode joined to t.
        try:
            v = t.vnodeList[0]
        except:
            at.readError("No vnodeList for tnode: %s" % repr(t))
            g.trace(at.tnodeListIndex)
            return None
            
        # Don't check the headline.  It simply causes problems.
        t.setVisited() # Supress warning about unvisited node.
        return t
    #@nonl
    #@-node:ekr.20040929105133.189:findChild4
    #@+node:ekr.20040929105133.190:scanText4 & allies
    def scanText4 (self,theFile,p):
        
        """Scan a 4.x derived file non-recursively."""
    
        at = self
        #@    << init ivars for scanText4 >>
        #@+node:ekr.20040929105133.191:<< init ivars for scanText4 >>
        # Unstacked ivars...
        at.cloneSibCount = 0
        at.done = False
        at.inCode = True
        at.indent = 0 # Changed only for sentinels.
        at.lastLines = [] # The lines after @-leo
        at.leadingWs = ""
        at.root = p
        at.rootSeen = False
        at.updateWarningGiven = False
        
        # Stacked ivars...
        at.endSentinelStack = [at.endLeo] # We have already handled the @+leo sentinel.
        at.out = [] ; at.outStack = []
        at.t = p.v.t ; at.tStack = []
        at.lastThinNode = p.v ; at.thinNodeStack = [p.v]
        
        if 0: # Useful for debugging.
            if hasattr(p.v.t,"tnodeList"):
                g.trace("len(tnodeList)",len(p.v.t.tnodeList),p.v)
            else:
                g.trace("no tnodeList",p.v)
                
        # g.trace(at.startSentinelComment)
        #@nonl
        #@-node:ekr.20040929105133.191:<< init ivars for scanText4 >>
        #@nl
        while at.errors == 0 and not at.done:
            s = at.readLine(theFile)
            if len(s) == 0: break
            kind = at.sentinelKind4(s)
            # g.trace(at.sentinelName(kind),s.strip())
            if kind == at.noSentinel:
                i = 0
            else:
                i = at.skipSentinelStart4(s,0)
            func = at.dispatch_dict[kind]
            func(s,i)
    
        if at.errors == 0 and not at.done:
            #@        << report unexpected end of text >>
            #@+node:ekr.20040929105133.192:<< report unexpected end of text >>
            assert(at.endSentinelStack)
            
            at.readError(
                "Unexpected end of file. Expecting %s sentinel" %
                at.sentinelName(at.endSentinelStack[-1]))
            #@nonl
            #@-node:ekr.20040929105133.192:<< report unexpected end of text >>
            #@nl
    
        return at.lastLines
    #@+node:ekr.20040929105133.193:readNormalLine
    def readNormalLine (self,s,i):
    
        at = self
        
        if at.inCode:
            if not at.raw:
                s = g.removeLeadingWhitespace(s,at.indent,at.tab_width)
            at.out.append(s)
        else:
            #@        << Skip the leading stuff >>
            #@+node:ekr.20040929105133.194:<< Skip the leading stuff >>
            if len(at.endSentinelComment) == 0:
                # Skip the single comment delim and a blank.
                i = g.skip_ws(s,0)
                if g.match(s,i,at.startSentinelComment):
                    i += len(at.startSentinelComment)
                    if g.match(s,i," "): i += 1
            else:
                i = at.skipIndent(s,0,at.indent)
            
            #@-node:ekr.20040929105133.194:<< Skip the leading stuff >>
            #@nl
            #@        << Append s to docOut >>
            #@+node:ekr.20040929105133.195:<< Append s to docOut >>
            line = s[i:-1] # remove newline for rstrip.
            
            if line == line.rstrip():
                # no trailing whitespace: the newline is real.
                at.docOut.append(line + '\n')
            else:
                # trailing whitespace: the newline is fake.
                at.docOut.append(line)
            #@nonl
            #@-node:ekr.20040929105133.195:<< Append s to docOut >>
            #@nl
    #@nonl
    #@-node:ekr.20040929105133.193:readNormalLine
    #@+node:ekr.20040929105133.196:start sentinels
    #@+node:ekr.20040929105133.197:readStartAll (4.2)
    def readStartAll (self,s,i):
        
        """Read an @+all sentinel."""
    
        at = self
        j = g.skip_ws(s,i)
        leadingWs = s[i:j]
        if leadingWs:
            assert(g.match(s,j,"@+all"))
        else:
            assert(g.match(s,j,"+all"))
    
        # Make sure that the generated at-all is properly indented.
        at.out.append(leadingWs + "@all\n")
        
        at.endSentinelStack.append(at.endAll)
    #@nonl
    #@-node:ekr.20040929105133.197:readStartAll (4.2)
    #@+node:ekr.20040929105133.198:readStartAt & readStartDoc
    def readStartAt (self,s,i):
        """Read an @+at sentinel."""
        at = self ; assert(g.match(s,i,"+at"))
        if 0:# new code: append whatever follows the sentinel.
            i += 3 ; j = self.skipToEndSentinel(s,i) ; follow = s[i:j]
            at.out.append('@' + follow) ; at.docOut = []
        else:
            i += 3 ; j = g.skip_ws(s,i) ; ws = s[i:j]
            at.docOut = ['@' + ws + '\n'] # This newline may be removed by a following @nonl
        at.inCode = False
        at.endSentinelStack.append(at.endAt)
        
    def readStartDoc (self,s,i):
        """Read an @+doc sentinel."""
        at = self ; assert(g.match(s,i,"+doc"))
        if 0: # new code: append whatever follows the sentinel.
            i += 4 ; j = self.skipToEndSentinel(s,i) ; follow = s[i:j]
            at.out.append('@' + follow) ; at.docOut = []
        else:
            i += 4 ; j = g.skip_ws(s,i) ; ws = s[i:j]
            at.docOut = ["@doc" + ws + '\n'] # This newline may be removed by a following @nonl
        at.inCode = False
        at.endSentinelStack.append(at.endDoc)
        
    def skipToEndSentinel(self,s,i):
        end = self.endSentinelComment
        if end:
            j = s.find(end,i)
            if j == -1:
                return g.skip_to_end_of_line(s,i)
            else:
                return j
        else:
            return g.skip_to_end_of_line(s,i)
    #@nonl
    #@-node:ekr.20040929105133.198:readStartAt & readStartDoc
    #@+node:ekr.20040929105133.199:readStartLeo
    def readStartLeo (self,s,i):
        
        """Read an unexpected @+leo sentinel."""
    
        at = self
        assert(g.match(s,i,"+leo"))
        at.readError("Ignoring unexpected @+leo sentinel")
    #@nonl
    #@-node:ekr.20040929105133.199:readStartLeo
    #@+node:ekr.20040929105133.200:readStartMiddle
    def readStartMiddle (self,s,i):
        
        """Read an @+middle sentinel."""
        
        at = self
        
        at.readStartNode(s,i,middle=True)
    #@nonl
    #@-node:ekr.20040929105133.200:readStartMiddle
    #@+node:ekr.20040929105133.201:readStartNode (4.x)
    def readStartNode (self,s,i,middle=False):
        
        """Read an @+node or @+middle sentinel."""
        
        at = self
        if middle:
            assert(g.match(s,i,"+middle:"))
            i += 8
        else:
            assert(g.match(s,i,"+node:"))
            i += 6
        
        if at.thinFile:
            #@        << set gnx and bump i >>
            #@+node:ekr.20040929105133.202:<< set gnx and bump i >>
            # We have skipped past the opening colon of the gnx.
            j = s.find(':',i)
            if j == -1:
                g.trace("no closing colon",g.get_line(s,i))
                at.readError("Expecting gnx in @+node sentinel")
                return # 5/17/04
            else:
                gnx = s[i:j]
                i = j + 1 # Skip the i
            #@nonl
            #@-node:ekr.20040929105133.202:<< set gnx and bump i >>
            #@nl
        #@    << Set headline, undoing the CWEB hack >>
        #@+node:ekr.20040929105133.203:<< Set headline, undoing the CWEB hack >>
        # Set headline to the rest of the line.
        # Don't strip leading whitespace."
        
        if len(at.endSentinelComment) == 0:
            headline = s[i:-1].rstrip()
        else:
            k = s.rfind(at.endSentinelComment,i)
            headline = s[i:k].rstrip() # works if k == -1
        
        # Undo the CWEB hack: undouble @ signs if the opening comment delim ends in '@'.
        if at.startSentinelComment[-1:] == '@':
            headline = headline.replace('@@','@')
        #@nonl
        #@-node:ekr.20040929105133.203:<< Set headline, undoing the CWEB hack >>
        #@nl
        if not at.root_seen:
            at.root_seen = True
            #@        << Check the filename in the sentinel >>
            #@+node:ekr.20040929105133.204:<< Check the filename in the sentinel >>
            if 0: # This doesn't work so well in cooperative environments.
                if not at.importing:
            
                    h = headline.strip()
                    
                    if h[:5] == "@file":
                        i,junk,junk = g.scanAtFileOptions(h)
                        fileName = string.strip(h[i:])
                        if fileName != at.targetFileName:
                            at.readError("File name in @node sentinel does not match file's name")
                    elif h[:8] == "@rawfile":
                        fileName = string.strip(h[8:])
                        if fileName != at.targetFileName:
                            at.readError("File name in @node sentinel does not match file's name")
                    else:
                        at.readError("Missing @file in root @node sentinel")
            #@nonl
            #@-node:ekr.20040929105133.204:<< Check the filename in the sentinel >>
            #@nl
    
        i,newIndent = g.skip_leading_ws_with_indent(s,0,at.tab_width)
        at.indentStack.append(at.indent) ; at.indent = newIndent
        
        at.outStack.append(at.out) ; at.out = []
        at.tStack.append(at.t)
    
        if at.importing:
            p = at.createImportedNode(at.root,at.c,headline)
            at.t = p.v.t
        elif at.thinFile:
            at.thinNodeStack.append(at.lastThinNode)
            at.lastThinNode = v = at.createThinChild4(gnx,headline)
            at.t = v.t
        else:
            at.t = at.findChild4(headline)
        
        at.endSentinelStack.append(at.endNode)
    #@nonl
    #@-node:ekr.20040929105133.201:readStartNode (4.x)
    #@+node:ekr.20040929105133.205:readStartOthers
    def readStartOthers (self,s,i):
        
        """Read an @+others sentinel."""
    
        at = self
        j = g.skip_ws(s,i)
        leadingWs = s[i:j]
        if leadingWs:
            assert(g.match(s,j,"@+others"))
        else:
            assert(g.match(s,j,"+others"))
    
        # Make sure that the generated at-others is properly indented.
        at.out.append(leadingWs + "@others\n")
        
        at.endSentinelStack.append(at.endOthers)
    #@nonl
    #@-node:ekr.20040929105133.205:readStartOthers
    #@-node:ekr.20040929105133.196:start sentinels
    #@+node:ekr.20040929105133.206:end sentinels
    #@+node:ekr.20040929105133.207:readEndAll (4.2)
    def readEndAll (self,s,i):
        
        """Read an @-all sentinel."""
        
        at = self
        at.popSentinelStack(at.endAll)
    #@nonl
    #@-node:ekr.20040929105133.207:readEndAll (4.2)
    #@+node:ekr.20040929105133.208:readEndAt & readEndDoc
    def readEndAt (self,s,i):
        
        """Read an @-at sentinel."""
    
        at = self
        at.readLastDocLine("@")
        at.popSentinelStack(at.endAt)
        at.inCode = True
            
    def readEndDoc (self,s,i):
        
        """Read an @-doc sentinel."""
    
        at = self
        at.readLastDocLine("@doc")
        at.popSentinelStack(at.endDoc)
        at.inCode = True
    #@nonl
    #@-node:ekr.20040929105133.208:readEndAt & readEndDoc
    #@+node:ekr.20040929105133.209:readEndLeo
    def readEndLeo (self,s,i):
        
        """Read an @-leo sentinel."""
        
        at = self
    
        # Ignore everything after @-leo.
        # Such lines were presumably written by @last.
        while 1:
            s = at.readLine(at.inputFile)
            if len(s) == 0: break
            at.lastLines.append(s) # Capture all trailing lines, even if empty.
    
        at.done = True
    #@nonl
    #@-node:ekr.20040929105133.209:readEndLeo
    #@+node:ekr.20040929105133.210:readEndMiddle
    def readEndMiddle (self,s,i):
        
        """Read an @-middle sentinel."""
        
        at = self
        
        at.readEndNode(s,i,middle=True)
    #@nonl
    #@-node:ekr.20040929105133.210:readEndMiddle
    #@+node:ekr.20040929105133.211:readEndNode (4.x)
    def readEndNode (self,s,i,middle=False):
        
        """Handle end-of-node processing for @-others and @-ref sentinels."""
    
        at = self ; c = self.c
        
        # End raw mode.
        at.raw = False
        
        # Set the temporary body text.
        s = ''.join(at.out)
        s = g.toUnicode(s,g.app.tkEncoding) # 9/28/03
    
        if at.importing:
            at.t.bodyString = s
        elif middle: 
            pass # Middle sentinels never alter text.
        else:
            if hasattr(at.t,"tempBodyString") and s != at.t.tempBodyString:
                old = at.t.tempBodyString
            elif at.t.hasBody() and s != at.t.getBody():
                old = at.t.getBody()
            else:
                old = None
            # 9/4/04: Suppress this warning for the root: @first complicates matters.
            if old and not g.app.unitTesting and at.t != at.root.t:
                #@            << indicate that the node has been changed >>
                #@+node:ekr.20040929105133.212:<< indicate that the node has been changed >>
                if at.perfectImportRoot:
                    #@    << bump at.correctedLines and tell about the correction >>
                    #@+node:ekr.20040929105133.213:<< bump at.correctedLines and tell about the correction >>
                    # Report the number of corrected nodes.
                    at.correctedLines += 1
                    
                    found = False
                    for p in at.perfectImportRoot.self_and_subtree_iter():
                        if p.v.t == at.t:
                            found = True ; break
                    
                    if found:
                        if 0: # Not needed: we mark all corrected nodes.
                            g.es("Correcting %s" % p.headString(),color="blue")
                        if 0: # For debugging.
                            print ; print '-' * 40
                            print "old",len(old)
                            for line in g.splitLines(old):
                                #line = line.replace(' ','< >').replace('\t','<TAB>')
                                print repr(str(line))
                            print ; print '-' * 40
                            print "new",len(s)
                            for line in g.splitLines(s):
                                #line = line.replace(' ','< >').replace('\t','<TAB>')
                                print repr(str(line))
                            print ; print '-' * 40
                    else:
                        # This should never happen.
                        g.es("Correcting hidden node: t=%s" % repr(at.t),color="red")
                    #@nonl
                    #@-node:ekr.20040929105133.213:<< bump at.correctedLines and tell about the correction >>
                    #@nl
                    # p.setMarked()
                    at.t.bodyString = s # Just etting at.t.tempBodyString won't work here.
                    at.t.setDirty() # Mark the node dirty.  Ancestors will be marked dirty later.
                    at.c.setChanged(True)
                else:
                    if not at.updateWarningGiven:
                        at.updateWarningGiven = True
                        # print "***",at.t,at.root.t
                        g.es("Warning: updating changed text in %s" %
                            (at.root.headString()),color="blue")
                    # g.es("old...\n%s\n" % old)
                    # g.es("new...\n%s\n" % s)
                    # Just set the dirty bit. Ancestors will be marked dirty later.
                    at.t.setDirty()
                    if 1: # We must avoid the full setChanged logic here!
                        c.changed = True
                    else: # Far too slow for mass changes.
                        at.c.setChanged(True)
                #@nonl
                #@-node:ekr.20040929105133.212:<< indicate that the node has been changed >>
                #@nl
            at.t.tempBodyString = s
    
        # Indicate that the tnode has been set in the derived file.
        at.t.setVisited()
    
        # End the previous node sentinel.
        at.indent = at.indentStack.pop()
        at.out = at.outStack.pop()
        at.t = at.tStack.pop()
        if at.thinFile and not at.importing:
            at.lastThinNode = at.thinNodeStack.pop()
    
        at.popSentinelStack(at.endNode)
    #@nonl
    #@-node:ekr.20040929105133.211:readEndNode (4.x)
    #@+node:ekr.20040929105133.214:readEndOthers
    def readEndOthers (self,s,i):
        
        """Read an @-others sentinel."""
        
        at = self
        at.popSentinelStack(at.endOthers)
    #@nonl
    #@-node:ekr.20040929105133.214:readEndOthers
    #@+node:ekr.20040929105133.215:readLastDocLine
    def readLastDocLine (self,tag):
        
        """Read the @c line that terminates the doc part.
        tag is @doc or @."""
        
        at = self
        end = at.endSentinelComment
        start = at.startSentinelComment
        s = ''.join(at.docOut)
        
        # Remove the @doc or @space.  We'll add it back at the end.
        if g.match(s,0,tag):
            s = s[len(tag):]
        else:
            at.readError("Missing start of doc part")
            return
    
        if end:
            # 9/3/04: Remove leading newline.
            if s[0] == '\n': s = s[1:]
            # Remove opening block delim.
            if g.match(s,0,start):
                s = s[len(start):]
            else:
                at.readError("Missing open block comment")
                g.trace(s)
                return
            # Remove trailing newline.
            if s[-1] == '\n': s = s[:-1]
            # Remove closing block delim.
            if s[-len(end):] == end:
                s = s[:-len(end)]
            else:
                at.readError("Missing close block comment")
                return
    
        at.out.append(tag + s)
        at.docOut = []
        
    #@nonl
    #@-node:ekr.20040929105133.215:readLastDocLine
    #@-node:ekr.20040929105133.206:end sentinels
    #@+node:ekr.20040929105133.216:Unpaired sentinels
    #@+node:ekr.20040929105133.217:ignoreOldSentinel
    def  ignoreOldSentinel (self,s,i):
        
        """Ignore an 3.x sentinel."""
        
        g.es("Ignoring 3.x sentinel: " + s.strip(), color="blue")
    #@nonl
    #@-node:ekr.20040929105133.217:ignoreOldSentinel
    #@+node:ekr.20040929105133.218:readAfterRef
    def  readAfterRef (self,s,i):
        
        """Read an @afterref sentinel."""
        
        at = self
        assert(g.match(s,i,"afterref"))
        
        # Append the next line to the text.
        s = at.readLine(at.inputFile)
        at.out.append(s)
    #@nonl
    #@-node:ekr.20040929105133.218:readAfterRef
    #@+node:ekr.20040929105133.219:readClone
    def readClone (self,s,i):
        
        at = self ; tag = "clone"
    
        assert(g.match(s,i,tag))
        
        # Skip the tag and whitespace.
        i = g.skip_ws(s,i+len(tag))
        
        # Get the clone count.
        junk,val = g.skip_long(s,i)
        
        if val == None:
            at.readError("Invalid count in @clone sentinel")
        else:
            at.cloneSibCount	 = val
    #@nonl
    #@-node:ekr.20040929105133.219:readClone
    #@+node:ekr.20040929105133.220:readComment
    def readComment (self,s,i):
        
        """Read an @comment sentinel."""
    
        assert(g.match(s,i,"comment"))
    
        # Just ignore the comment line!
    #@-node:ekr.20040929105133.220:readComment
    #@+node:ekr.20040929105133.221:readDelims
    def readDelims (self,s,i):
        
        """Read an @delims sentinel."""
        
        at = self
        assert(g.match(s,i-1,"@delims"));
    
        # Skip the keyword and whitespace.
        i0 = i-1
        i = g.skip_ws(s,i-1+7)
            
        # Get the first delim.
        j = i
        while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
            i += 1
        
        if j < i:
            at.startSentinelComment = s[j:i]
            # print "delim1:", at.startSentinelComment
        
            # Get the optional second delim.
            j = i = g.skip_ws(s,i)
            while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
                i += 1
            end = g.choose(j<i,s[j:i],"")
            i2 = g.skip_ws(s,i)
            if end == at.endSentinelComment and (i2 >= len(s) or g.is_nl(s,i2)):
                at.endSentinelComment = "" # Not really two params.
                line = s[i0:j]
                line = line.rstrip()
                at.out.append(line+'\n')
            else:
                at.endSentinelComment = end
                # print "delim2:",end
                line = s[i0:i]
                line = line.rstrip()
                at.out.append(line+'\n')
        else:
            at.readError("Bad @delims")
            # Append the bad @delims line to the body text.
            at.out.append("@delims")
    #@nonl
    #@-node:ekr.20040929105133.221:readDelims
    #@+node:ekr.20040929105133.222:readDirective
    def readDirective (self,s,i):
        
        """Read an @@sentinel."""
        
        at = self
        assert(g.match(s,i,"@")) # The first '@' has already been eaten.
        
        if g.match_word(s,i,"@raw"):
            at.raw = True
        elif g.match_word(s,i,"@end_raw"):
            at.raw = False
        
        e = at.endSentinelComment
        s2 = s[i:]
        if len(e) > 0:
            k = s.rfind(e,i)
            if k != -1:
                s2 = s[i:k] + '\n'
            
        start = at.startSentinelComment
        if start and len(start) > 0 and start[-1] == '@':
            s2 = s2.replace('@@','@')
            
        if g.match_word(s,i,"@language"):
            #@        << handle @language >>
            #@+node:ekr.20040929105133.223:<< handle @language >>
            # Skip the keyword and whitespace.
            i += len("@language")
            i = g.skip_ws(s,i)
            j = g.skip_c_id(s,i)
            language = s[i:j]
            
            delim1,delim2,delim3 = g.set_delims_from_language(language)
            
            #g.trace(g.get_line(s,i))
            #g.trace(delim1,delim2,delim3)
            
            # Returns a tuple (single,start,end) of comment delims
            if delim1:
                at.startSentinelComment = delim1
                at.endSentinelComment = "" # Must not be None.
            elif delim2 and delim3:
                at.startSentinelComment = delim2
                at.endSentinelComment = delim3
            else:
                line = g.get_line(s,i)
                g.es("Ignoring bad @@language sentinel: %s" % line,color="red")
            #@nonl
            #@-node:ekr.20040929105133.223:<< handle @language >>
            #@nl
        elif g.match_word(s,i,"@comment"):
            #@        << handle @comment >>
            #@+node:ekr.20040929105133.224:<< handle @comment >>
            j = g.skip_line(s,i)
            line = s[i:j]
            delim1,delim2,delim3 = g.set_delims_from_string(line)
            
            #g.trace(g.get_line(s,i))
            #g.trace(delim1,delim2,delim3)
            
            # Returns a tuple (single,start,end) of comment delims
            if delim1:
                self.startSentinelComment = delim1
                self.endSentinelComment = "" # Must not be None.
            elif delim2 and delim3:
                self.startSentinelComment = delim2
                self.endSentinelComment = delim3
            else:
                line = g.get_line(s,i)
                g.es("Ignoring bad @comment sentinel: %s" % line,color="red")
            #@nonl
            #@-node:ekr.20040929105133.224:<< handle @comment >>
            #@nl
    
        at.out.append(s2)
    #@nonl
    #@-node:ekr.20040929105133.222:readDirective
    #@+node:ekr.20040929105133.225:readNl
    def readNl (self,s,i):
        
        """Handle an @nonl sentinel."""
        
        at = self
        assert(g.match(s,i,"nl"))
        
        if at.inCode:
            at.out.append('\n')
        else:
            at.docOut.append('\n')
    #@nonl
    #@-node:ekr.20040929105133.225:readNl
    #@+node:ekr.20040929105133.226:readNonl
    def readNonl (self,s,i):
        
        """Handle an @nonl sentinel."""
        
        at = self
        assert(g.match(s,i,"nonl"))
        
        if at.inCode:
            s = ''.join(at.out)
            if s and s[-1] == '\n':
                at.out = [s[:-1]]
            else:
                g.trace("out:",s)
                at.readError("unexpected @nonl directive in code part")	
        else:
            s = ''.join(at.pending)
            if s:
                if s and s[-1] == '\n':
                    at.pending = [s[:-1]]
                else:
                    g.trace("docOut:",s)
                    at.readError("unexpected @nonl directive in pending doc part")
            else:
                s = ''.join(at.docOut)
                if s and s[-1] == '\n':
                    at.docOut = [s[:-1]]
                else:
                    g.trace("docOut:",s)
                    at.readError("unexpected @nonl directive in doc part")
    #@nonl
    #@-node:ekr.20040929105133.226:readNonl
    #@+node:ekr.20040929105133.227:readRef
    #@+at 
    #@nonl
    # The sentinel contains an @ followed by a section name in angle 
    # brackets.  This code is different from the code for the @@ sentinel: the 
    # expansion of the reference does not include a trailing newline.
    #@-at
    #@@c
    
    def readRef (self,s,i):
        
        """Handle an @<< sentinel."""
        
        at = self
        j = g.skip_ws(s,i)
        assert(g.match(s,j,"<<"))
        
        if len(at.endSentinelComment) == 0:
            line = s[i:-1] # No trailing newline
        else:
            k = s.find(at.endSentinelComment,i)
            line = s[i:k] # No trailing newline, whatever k is.
                
        # Undo the cweb hack.
        start = at.startSentinelComment
        if start and len(start) > 0 and start[-1] == '@':
            line = line.replace('@@','@')
    
        at.out.append(line)
    #@-node:ekr.20040929105133.227:readRef
    #@+node:ekr.20040929105133.228:readVerbatim
    def readVerbatim (self,s,i):
        
        """Read an @verbatim sentinel."""
        
        at = self
        assert(g.match(s,i,"verbatim"))
        
        # Append the next line to the text.
        s = at.readLine(at.inputFile) 
        i = at.skipIndent(s,0,at.indent)
        at.out.append(s[i:])
    #@nonl
    #@-node:ekr.20040929105133.228:readVerbatim
    #@-node:ekr.20040929105133.216:Unpaired sentinels
    #@+node:ekr.20040929105133.229:badEndSentinel, push/popSentinelStack
    def badEndSentinel (self,expectedKind):
        
        """Handle a mismatched ending sentinel."""
    
        at = self
        assert(at.endSentinelStack)
        at.readError("Ignoring %s sentinel.  Expecting %s" %
            (at.sentinelName(at.endSentinelStack[-1]),
             at.sentinelName(expectedKind)))
             
    def popSentinelStack (self,expectedKind):
        
        """Pop an entry from endSentinelStack and check it."""
        
        at = self
        if at.endSentinelStack and at.endSentinelStack[-1] == expectedKind:
            at.endSentinelStack.pop()
        else:
            at.badEndSentinel(expectedKind)
    #@nonl
    #@-node:ekr.20040929105133.229:badEndSentinel, push/popSentinelStack
    #@-node:ekr.20040929105133.190:scanText4 & allies
    #@+node:ekr.20040929105133.239:sentinelKind4
    def sentinelKind4(self,s):
        
        """Return the kind of sentinel at s."""
        
        at = self
    
        i = g.skip_ws(s,0)
        if g.match(s,i,at.startSentinelComment): 
            i += len(at.startSentinelComment)
        else:
            return at.noSentinel
    
        # Locally undo cweb hack here
        start = at.startSentinelComment
        if start and len(start) > 0 and start[-1] == '@':
            s = s[:i] + string.replace(s[i:],'@@','@')
            
        # 4.0: Look ahead for @[ws]@others and @[ws]<<
        if g.match(s,i,"@"):
            j = g.skip_ws(s,i+1)
            if j > i+1:
                # g.trace(ws,s)
                if g.match(s,j,"@+others"):
                    return at.startOthers
                elif g.match(s,j,"<<"):
                    return at.startRef
                else:
                    # No other sentinels allow whitespace following the '@'
                    return at.noSentinel
    
        # Do not skip whitespace here!
        if g.match(s,i,"@<<"): return at.startRef
        if g.match(s,i,"@@"):   return at.startDirective
        if not g.match(s,i,'@'): return at.noSentinel
        j = i # start of lookup
        i += 1 # skip the at sign.
        if g.match(s,i,'+') or g.match(s,i,'-'):
            i += 1
        i = g.skip_c_id(s,i)
        key = s[j:i]
        if len(key) > 0 and at.sentinelDict.has_key(key):
            return at.sentinelDict[key]
        else:
            return at.noSentinel
    #@nonl
    #@-node:ekr.20040929105133.239:sentinelKind4
    #@+node:ekr.20040929105133.240:skipSentinelStart4
    def skipSentinelStart4(self,s,i):
        
        """Skip the start of a sentinel."""
    
        start = self.startSentinelComment
        assert(start and len(start)>0)
    
        i = g.skip_ws(s,i)
        assert(g.match(s,i,start))
        i += len(start)
    
        # 7/8/02: Support for REM hack
        i = g.skip_ws(s,i)
        assert(i < len(s) and s[i] == '@')
        return i + 1
    #@-node:ekr.20040929105133.240:skipSentinelStart4
    #@-node:ekr.20040929105133.186:Reading (4.x)
    #@+node:ekr.20040930081343.1:Reading utils...
    #@+node:ekr.20040929105133.49:completeFirstDirectives
    # 14-SEP-2002 DTHEIN: added for use by atFile.read()
    
    # this function scans the lines in the list 'out' for @first directives
    # and appends the corresponding line from 'firstLines' to each @first 
    # directive found.  NOTE: the @first directives must be the very first
    # lines in 'out'.
    def completeFirstDirectives(self,out,firstLines):
    
        tag = "@first"
        foundAtFirstYet = 0
        outRange = range(len(out))
        j = 0
        for k in outRange:
            # skip leading whitespace lines
            if (not foundAtFirstYet) and (len(out[k].strip()) == 0): continue
            # quit if something other than @first directive
            i = 0
            if not g.match(out[k],i,tag): break;
            foundAtFirstYet = 1
            # quit if no leading lines to apply
            if j >= len(firstLines): break
            # make the new @first directive
            #18-SEP-2002 DTHEIN: remove trailing newlines because they are inserted later
            # 21-SEP-2002 DTHEIN: no trailing whitespace on empty @first directive
            leadingLine = " " + firstLines[j]
            out[k] = tag + leadingLine.rstrip() ; j += 1
    #@-node:ekr.20040929105133.49:completeFirstDirectives
    #@+node:ekr.20040929105133.50:completeLastDirectives
    # 14-SEP-2002 DTHEIN: added for use by atFile.read()
    
    # this function scans the lines in the list 'out' for @last directives
    # and appends the corresponding line from 'lastLines' to each @last 
    # directive found.  NOTE: the @last directives must be the very last
    # lines in 'out'.
    def completeLastDirectives(self,out,lastLines):
    
        tag = "@last"
        foundAtLastYet = 0
        outRange = range(-1,-len(out),-1)
        j = -1
        for k in outRange:
            # skip trailing whitespace lines
            if (not foundAtLastYet) and (len(out[k].strip()) == 0): continue
            # quit if something other than @last directive
            i = 0
            if not g.match(out[k],i,tag): break;
            foundAtLastYet = 1
            # quit if no trailing lines to apply
            if j < -len(lastLines): break
            # make the new @last directive
            #18-SEP-2002 DTHEIN: remove trailing newlines because they are inserted later
            # 21-SEP-2002 DTHEIN: no trailing whitespace on empty @last directive
            trailingLine = " " + lastLines[j]
            out[k] = tag + trailingLine.rstrip() ; j -= 1
    #@nonl
    #@-node:ekr.20040929105133.50:completeLastDirectives
    #@+node:ekr.20040929105133.47:createImportedNode
    def createImportedNode (self,root,c,headline):
        
        at = self
    
        if at.importRootSeen:
            p = root.insertAsLastChild()
            p.initHeadString(headline)
        else:
            # Put the text into the already-existing root node.
            p = root
            at.importRootSeen = True
            
        p.v.t.setVisited() # Suppress warning about unvisited node.
        return p
    #@nonl
    #@-node:ekr.20040929105133.47:createImportedNode
    #@+node:ekr.20041001080852:parseLeoSentinel
    def parseLeoSentinel (self,s):
        
        at = self
        new_df = False ; valid = True ; n = len(s)
        isThinDerivedFile = False
        encoding_tag = "-encoding="
        version_tag = "-ver="
        tag = "@+leo"
        thin_tag = "-thin"
        #@    << set the opening comment delim >>
        #@+node:ekr.20041001080852.1:<< set the opening comment delim >>
        # s contains the tag
        i = j = g.skip_ws(s,0)
        
        # The opening comment delim is the initial non-tag
        while i < n and not g.match(s,i,tag) and not g.is_nl(s,i):
            i += 1
        
        if j < i:
            start = s[j:i]
        else:
            valid = False
        #@nonl
        #@-node:ekr.20041001080852.1:<< set the opening comment delim >>
        #@nl
        #@    << make sure we have @+leo >>
        #@+node:ekr.20041001080852.2:<< make sure we have @+leo >>
        #@+at 
        #@nonl
        # REM hack: leading whitespace is significant before the @+leo.  We do 
        # this so that sentinelKind need not skip whitespace following 
        # self.startSentinelComment.  This is correct: we want to be as 
        # restrictive as possible about what is recognized as a sentinel.  
        # This minimizes false matches.
        #@-at
        #@@c
        
        if 0: # Make leading whitespace significant.
            i = g.skip_ws(s,i)
        
        if g.match(s,i,tag):
            i += len(tag)
        else: valid = False
        #@nonl
        #@-node:ekr.20041001080852.2:<< make sure we have @+leo >>
        #@nl
        #@    << read optional version param >>
        #@+node:ekr.20041001080852.3:<< read optional version param >>
        new_df = g.match(s,i,version_tag)
        
        if new_df:
            # Skip to the next minus sign or end-of-line
            i += len(version_tag)
            j = i
            while i < len(s) and not g.is_nl(s,i) and s[i] != '-':
                i += 1
        
            if j < i:
                pass # version = s[j:i]
            else:
                valid = False
        #@-node:ekr.20041001080852.3:<< read optional version param >>
        #@nl
        #@    << read optional thin param >>
        #@+node:ekr.20041001080852.4:<< read optional thin param >>
        if g.match(s,i,thin_tag):
            i += len(tag)
            isThinDerivedFile = True
        #@nonl
        #@-node:ekr.20041001080852.4:<< read optional thin param >>
        #@nl
        #@    << read optional encoding param >>
        #@+node:ekr.20041001080852.5:<< read optional encoding param >>
        # Set the default encoding
        at.encoding = g.app.config.default_derived_file_encoding
        
        if g.match(s,i,encoding_tag):
            # Read optional encoding param, e.g., -encoding=utf-8,
            i += len(encoding_tag)
            # Skip to the next end of the field.
            j = s.find(",.",i)
            if j > -1:
                # The encoding field was written by 4.2 or after:
                encoding = s[i:j]
                i = j + 1 # 6/8/04
            else:
                # The encoding field was written before 4.2.
                j = s.find('.',i)
                if j > -1:
                    encoding = s[i:j]
                    i = j + 1 # 6/8/04
                else:
                    encoding = None
            # g.trace("encoding:",encoding)
            if encoding:
                if g.isValidEncoding(encoding):
                    at.encoding = encoding
                else:
                    print "bad encoding in derived file:",encoding
                    g.es("bad encoding in derived file:",encoding)
            else:
                valid = False
        #@-node:ekr.20041001080852.5:<< read optional encoding param >>
        #@nl
        #@    << set the closing comment delim >>
        #@+node:ekr.20041001080852.6:<< set the closing comment delim >>
        # The closing comment delim is the trailing non-whitespace.
        i = j = g.skip_ws(s,i)
        while i < n and not g.is_ws(s[i]) and not g.is_nl(s,i):
            i += 1
        end = s[j:i]
        #@nonl
        #@-node:ekr.20041001080852.6:<< set the closing comment delim >>
        #@nl
        return valid,new_df,start,end,isThinDerivedFile
    #@nonl
    #@-node:ekr.20041001080852:parseLeoSentinel
    #@+node:ekr.20040929105133.106:readError
    def readError(self,message):
    
        # This is useful now that we don't print the actual messages.
        if self.errors == 0:
            g.es_error("----- error reading @file " + self.targetFileName)
            self.error(message) # 9/10/02: we must increment self.errors!
            
        print message
    
        if 0: # CVS conflicts create too many messages.
            self.error(message)
        
        self.root.setOrphan()
        self.root.setDirty()
    #@nonl
    #@-node:ekr.20040929105133.106:readError
    #@+node:ekr.20040929105133.55:readLine
    def readLine (self,theFile):
        
        """Reads one line from file using the present encoding"""
        
        s = g.readlineForceUnixNewline(theFile)
        u = g.toUnicode(s,self.encoding)
        return u
    
    
    #@-node:ekr.20040929105133.55:readLine
    #@+node:ekr.20041001080926:scanHeader  (3.x and 4.x)
    def scanHeader(self,theFile,fileName):
        
        """Scan the @+leo sentinel.
        
        Sets self.encoding, and self.start/endSentinelComment.
        
        Returns (firstLines,new_df) where:
        firstLines contains all @first lines,
        new_df is True if we are reading a new-format derived file."""
        
        at = self
        firstLines = [] # The lines before @+leo.
        tag = "@+leo"
        valid = True ; new_df = False ; isThinDerivedFile = False
        #@    << skip any non @+leo lines >>
        #@+node:ekr.20041001080926.1:<< skip any non @+leo lines >>
        #@+at 
        #@nonl
        # Queue up the lines before the @+leo.  These will be used to add as 
        # parameters to the @first directives, if any.  Empty lines are 
        # ignored (because empty @first directives are ignored). NOTE: the 
        # function now returns a list of the lines before @+leo.
        # 
        # We can not call sentinelKind here because that depends on the 
        # comment delimiters we set here.  @first lines are written 
        # "verbatim", so nothing more needs to be done!
        #@-at
        #@@c
        
        s = at.readLine(theFile)
        while len(s) > 0:
            j = s.find(tag)
            if j != -1: break
            firstLines.append(s) # Queue the line
            s = at.readLine(theFile)
            
        n = len(s)
        valid = n > 0
        #@-node:ekr.20041001080926.1:<< skip any non @+leo lines >>
        #@nl
        if valid:
            valid,new_df,start,end,isThinDerivedFile = at.parseLeoSentinel(s)
        if valid:
            at.startSentinelComment = start
            at.endSentinelComment = end
        else:
            at.error("Bad @+leo sentinel in " + fileName)
        # g.trace("start,end",repr(at.startSentinelComment),repr(at.endSentinelComment))
        return firstLines,new_df,isThinDerivedFile
    #@nonl
    #@-node:ekr.20041001080926:scanHeader  (3.x and 4.x)
    #@+node:ekr.20040929105133.121:skipIndent
    # Skip past whitespace equivalent to width spaces.
    
    def skipIndent(self,s,i,width):
    
        ws = 0 ; n = len(s)
        while i < n and ws < width:
            if   s[i] == '\t': ws += (abs(self.tab_width) - (ws % abs(self.tab_width)))
            elif s[i] == ' ':  ws += 1
            else: break
            i += 1
        return i
    #@nonl
    #@-node:ekr.20040929105133.121:skipIndent
    #@-node:ekr.20040930081343.1:Reading utils...
    #@-node:ekr.20040930080842:Reading...
    #@+node:ekr.20040930080842.1:Writing...
    #@+node:ekr.20040929105133.32:Writing (top level)
    #@+at
    # 
    # All writing eventually goes through the asisWrite or writeOpenFile 
    # methods, so
    # plugins should need only to override these two methods. In particular, 
    # plugins
    # should not need to override the write, writeAll or writeMissing methods.
    #@-at
    #@nonl
    #@+node:ekr.20040929105133.125:asisWrite
    def asisWrite(self,root,toString=False):
    
        at = self ; c = at.c
        c.endEditing() # Capture the current headline.
    
        try:
            targetFileName = root.atAsisFileNodeName()
            at.initWriteIvars(root,targetFileName,toString=toString)
            if at.errors: return
            if not at.openFileForWriting(root,targetFileName,toString): return
            for p in root.self_and_subtree_iter():
                #@            << Write p's headline if it starts with @@ >>
                #@+node:ekr.20040929105133.126:<< Write p's headline if it starts with @@ >>
                s = p.headString()
                
                if g.match(s,0,"@@"):
                    s = s[2:]
                    if s and len(s) > 0:
                        s = g.toEncodedString(s,at.encoding,reportErrors=True) # 3/7/03
                        at.outputFile.write(s)
                #@nonl
                #@-node:ekr.20040929105133.126:<< Write p's headline if it starts with @@ >>
                #@nl
                #@            << Write p's body >>
                #@+node:ekr.20040929105133.127:<< Write p's body >>
                s = p.bodyString()
                
                if s:
                    s = g.toEncodedString(s,at.encoding,reportErrors=True) # 3/7/03
                    at.outputStringWithLineEndings(s)
                #@nonl
                #@-node:ekr.20040929105133.127:<< Write p's body >>
                #@nl
            at.closeWriteFile()
            at.replaceTargetFileIfDifferent()
            root.clearOrphan() ; root.clearDirty()
        except:
            at.writeException(root)
            
    silentWrite = asisWrite # Compatibility with old scripts.
    #@nonl
    #@-node:ekr.20040929105133.125:asisWrite
    #@+node:ekr.20040929105133.243:closeWriteFile
    # 4.0: Don't use newline-pending logic.
    
    def closeWriteFile (self):
        
        at = self
    
        if at.outputFile:
            at.outputFile.flush()
            if self.toString:
                self.stringOutput = self.outputFile.get()
            at.outputFile.close()
            at.outputFile = None
    #@nonl
    #@-node:ekr.20040929105133.243:closeWriteFile
    #@+node:ekr.20040929105133.251:norefWrite
    def norefWrite(self,root,toString=False):
    
        at = self ; c = at.c
        c.endEditing() # Capture the current headline.
    
        try:
            targetFileName = root.atNorefFileNodeName()
            at.initWriteIvars(root,targetFileName,nosentinels=False,toString=toString)
            if at.errors: return
            if not at.openFileForWriting(root,targetFileName,toString):
                return
            #@        << write root's tree >>
            #@+node:ekr.20040929105133.252:<< write root's tree >>
            #@<< put all @first lines in root >>
            #@+node:ekr.20040929105133.253:<< put all @first lines in root >>
            #@+at 
            #@nonl
            # Write any @first lines.  These lines are also converted to 
            # @verbatim lines, so the read logic simply ignores lines 
            # preceding the @+leo sentinel.
            #@-at
            #@@c
            
            s = root.v.t.bodyString
            tag = "@first"
            i = 0
            while g.match(s,i,tag):
                i += len(tag)
                i = g.skip_ws(s,i)
                j = i
                i = g.skip_to_end_of_line(s,i)
                # Write @first line, whether empty or not
                line = s[j:i]
                at.putBuffered(line) ; at.onl()
                i = g.skip_nl(s,i)
            #@nonl
            #@-node:ekr.20040929105133.253:<< put all @first lines in root >>
            #@nl
            at.putOpenLeoSentinel("@+leo-ver=4")
            #@<< put optional @comment sentinel lines >>
            #@+node:ekr.20040929105133.254:<< put optional @comment sentinel lines >>
            s2 = g.app.config.output_initial_comment
            if s2:
                lines = string.split(s2,"\\n")
                for line in lines:
                    line = line.replace("@date",time.asctime())
                    if len(line)> 0:
                        at.putSentinel("@comment " + line)
            #@-node:ekr.20040929105133.254:<< put optional @comment sentinel lines >>
            #@nl
            
            for p in root.self_and_subtree_iter():
                #@    << Write p's node >>
                #@+node:ekr.20040929105133.255:<< Write p's node >>
                at.putOpenNodeSentinel(p,inAtOthers=True)
                
                s = p.bodyString()
                if s and len(s) > 0:
                    s = g.toEncodedString(s,at.encoding,reportErrors=True) # 3/7/03
                    at.outputStringWithLineEndings(s)
                    
                # Put an @nonl sentinel if s does not end in a newline.
                if s and s[-1] != '\n':
                    at.onl_sent() ; at.putSentinel("@nonl")
                
                at.putCloseNodeSentinel(p,inAtOthers=True)
                #@nonl
                #@-node:ekr.20040929105133.255:<< Write p's node >>
                #@nl
            
            at.putSentinel("@-leo")
            #@<< put all @last lines in root >>
            #@+node:ekr.20040929105133.256:<< put all @last lines in root >>
            #@+at 
            #@nonl
            # Write any @last lines.  These lines are also converted to 
            # @verbatim lines, so the read logic simply ignores lines 
            # following the @-leo sentinel.
            #@-at
            #@@c
            
            tag = "@last"
            lines = string.split(root.v.t.bodyString,'\n')
            n = len(lines) ; j = k = n - 1
            # Don't write an empty last line.
            if j >= 0 and len(lines[j])==0:
                j = k = n - 2
            # Scan backwards for @last directives.
            while j >= 0:
                line = lines[j]
                if g.match(line,0,tag): j -= 1
                else: break
            # Write the @last lines.
            for line in lines[j+1:k+1]:
                i = len(tag) ; i = g.skip_ws(line,i)
                at.putBuffered(line[i:]) ; at.onl()
            #@nonl
            #@-node:ekr.20040929105133.256:<< put all @last lines in root >>
            #@nl
            #@nonl
            #@-node:ekr.20040929105133.252:<< write root's tree >>
            #@nl
            at.closeWriteFile()
            at.replaceTargetFileIfDifferent()
            root.clearOrphan() ; root.clearDirty()
        except:
            at.writeException(root)
            
    rawWrite = norefWrite
    #@-node:ekr.20040929105133.251:norefWrite
    #@+node:ekr.20040929105133.144:openFileForWriting & openFileForWritingHelper
    def openFileForWriting (self,root,fileName,toString):
    
        at = self
        at.outputFile = None
        
        if toString:
            at.shortFileName = g.shortFileName(fileName)
            at.outputFileName = "<string: %s>" % at.shortFileName
            at.outputFile = g.fileLikeObject()
        else:
            at.openFileForWritingHelper(fileName,toString)
    
        if at.outputFile:
            root.clearOrphan()
        else:
            root.setOrphan()
            root.setDirty()
        
        return at.outputFile is not None
    #@nonl
    #@+node:ekr.20040929155554:openFileForWritingHelper
    def openFileForWritingHelper (self,fileName,toString):
        
        at = self
    
        try:
            at.shortFileName = g.shortFileName(fileName)
            fileName = g.os_path_join(at.default_directory,fileName)
            at.targetFileName = g.os_path_normpath(fileName)
            path = g.os_path_dirname(at.targetFileName)
            if not path or not g.os_path_exists(path):
                at.writeError("path does not exist: " + path)
                return
        except:
            at.exception("exception creating path:" + fn)
            return
    
        if g.os_path_exists(at.targetFileName):
            try:
                if not os.access(at.targetFileName,os.W_OK):
                    at.writeError("can not create: read only: " + at.targetFileName)
                    return
            except AttributeError: pass # os.access() may not exist on all platforms.
    
        try:
            at.outputFileName = at.targetFileName + ".tmp"
            at.outputFile = open(at.outputFileName,'wb')
            if not at.outputFile:
                at.writeError("can not create " + at.outputFileName)
        except:
            at.exception("exception creating:" + at.outputFileName)
    #@nonl
    #@-node:ekr.20040929155554:openFileForWritingHelper
    #@-node:ekr.20040929105133.144:openFileForWriting & openFileForWritingHelper
    #@+node:ekr.20040929105133.244:write
    # This is the entry point to the write code.  root should be an @file vnode.
    
    def write(self,root,nosentinels=False,thinFile=False,toString=False):
        
        """Write a 4.x derived file."""
        
        at = self ; c = at.c
        c.endEditing() # Capture the current headline.
        #@    << set at.targetFileName >>
        #@+node:ekr.20040929105133.245:<< set at.targetFileName >>
        if toString:
            at.targetFileName = "<new_df.write string-file>"
        elif nosentinels:
            at.targetFileName = root.atNoSentFileNodeName()
        elif thinFile:
            at.targetFileName = root.atThinFileNodeName()
        else:
            at.targetFileName = root.atFileNodeName()
        #@nonl
        #@-node:ekr.20040929105133.245:<< set at.targetFileName >>
        #@nl
        at.initWriteIvars(root,at.targetFileName,thinFile=thinFile,toString=toString)
        if not at.openFileForWriting(root,at.targetFileName,toString):
            return
    
        try:
            at.writeOpenFile(root,nosentinels=nosentinels,toString=toString)
            if toString:
                at.closeWriteFile()
                # Major bug: failure to clear this wipes out headlines!
                # Minor bug: sometimes this causes slight problems...
                at.root.v.t.tnodeList = [] 
            else:
                at.closeWriteFile()
                #@            << set dirty and orphan bits on error >>
                #@+node:ekr.20040929105133.246:<< set dirty and orphan bits on error >>
                # Setting the orphan and dirty flags tells Leo to write the tree..
                
                if at.errors > 0 or at.root.isOrphan():
                    root.setOrphan()
                    root.setDirty() # Make _sure_ we try to rewrite this file.
                    os.remove(at.outputFileName) # Delete the temp file.
                    g.es("Not written: " + at.outputFileName)
                else:
                    root.clearOrphan()
                    root.clearDirty()
                    at.replaceTargetFileIfDifferent()
                #@nonl
                #@-node:ekr.20040929105133.246:<< set dirty and orphan bits on error >>
                #@nl
        except:
            if toString:
                at.exception("exception preprocessing script")
                at.root.v.t.tnodeList = []
            else:
                at.writeException() # Sets dirty and orphan bits.
    #@-node:ekr.20040929105133.244:write
    #@+node:ekr.20040929105133.33:writeAll
    def writeAll(self,writeAtFileNodesFlag=False,writeDirtyAtFileNodesFlag=False,toString=False):
        
        """Write @file nodes in all or part of the outline"""
    
        at = self ; c = at.c
        writtenFiles = [] # Files that might be written again.
        mustAutoSave = False
    
        if writeAtFileNodesFlag:
            # Write all nodes in the selected tree.
            p = c.currentPosition()
            after = p.nodeAfterTree()
        else:
            # Write dirty nodes in the entire outline.
            p =  c.rootPosition()
            after = c.nullPosition()
    
        #@    << Clear all orphan bits >>
        #@+node:ekr.20040929105133.34:<< Clear all orphan bits >>
        #@+at 
        #@nonl
        # We must clear these bits because they may have been set on a 
        # previous write.
        # Calls to atFile::write may set the orphan bits in @file nodes.
        # If so, write_Leo_file will write the entire @file tree.
        #@-at
        #@@c
            
        for v2 in p.self_and_subtree_iter():
            v2.clearOrphan()
        #@nonl
        #@-node:ekr.20040929105133.34:<< Clear all orphan bits >>
        #@nl
        while p and p != after:
            if p.isAnyAtFileNode() or p.isAtIgnoreNode():
                #@            << handle v's tree >>
                #@+node:ekr.20040929105133.35:<< handle v's tree >>
                if p.v.isDirty() or writeAtFileNodesFlag or p.v.t in writtenFiles:
                
                    at.fileChangedFlag = False
                    autoSave = False
                    
                    # Tricky: @ignore not recognised in @silentfile nodes.
                    if p.isAtAsisFileNode():
                        at.asisWrite(p,toString=toString)
                        writtenFiles.append(p.v.t) ; autoSave = True
                    elif p.isAtIgnoreNode():
                        pass
                    elif p.isAtNorefFileNode():
                        at.norefWrite(p,toString=toString)
                        writtenFiles.append(p.v.t) ; autoSave = True
                    elif p.isAtNoSentFileNode():
                        at.write(p,nosentinels=True,toString=toString)
                        writtenFiles.append(p.v.t) # No need for autosave
                    elif p.isAtThinFileNode():
                        at.write(p,thinFile=True,toString=toString)
                        writtenFiles.append(p.v.t) # No need for autosave.
                    elif p.isAtFileNode():
                        at.write(p,toString=toString)
                        writtenFiles.append(p.v.t) ; autoSave = True
                
                    if at.fileChangedFlag and autoSave: # Set by replaceTargetFileIfDifferent.
                        mustAutoSave = True
                #@nonl
                #@-node:ekr.20040929105133.35:<< handle v's tree >>
                #@nl
                p.moveToNodeAfterTree()
            else:
                p.moveToThreadNext()
    
        #@    << say the command is finished >>
        #@+node:ekr.20040929105133.36:<< say the command is finished >>
        if writeAtFileNodesFlag or writeDirtyAtFileNodesFlag:
            if len(writtenFiles) > 0:
                g.es("finished")
            elif writeAtFileNodesFlag:
                g.es("no @file nodes in the selected tree")
            else:
                g.es("no dirty @file nodes")
        #@nonl
        #@-node:ekr.20040929105133.36:<< say the command is finished >>
        #@nl
        return mustAutoSave
    #@nonl
    #@-node:ekr.20040929105133.33:writeAll
    #@+node:ekr.20040929105133.38:writeMissing
    def writeMissing(self,p,toString=False):
    
        at = self
        writtenFiles = False ; changedFiles = False
    
        p = p.copy()
        after = p.nodeAfterTree()
        while p and p != after: # Don't use iterator.
            if p.isAtAsisFileNode() or (p.isAnyAtFileNode() and not p.isAtIgnoreNode()):
                missing = False ; valid = True
                at.targetFileName = p.anyAtFileNodeName()
                if at.targetFileName:
                    at.targetFileName = g.os_path_join(self.default_directory,at.targetFileName)
                    at.targetFileName = g.os_path_normpath(at.targetFileName)
                    if not g.os_path_exists(at.targetFileName):
                        at.openFileForWriting(p,at.targetFileName,toString)
                        if at.outputFile:
                            #@                        << write the @file node >>
                            #@+node:ekr.20040929105133.41:<< write the @file node >>
                            if p.isAtAsisFileNode():
                                at.asisWrite(p)
                            elif p.isAtNorefFileNode():
                                at.norefWrite(p)
                            elif p.isAtNoSentFileNode():
                                at.write(p,nosentinels=True)
                            elif p.isAtFileNode():
                                at.write(p)
                            else: assert(0)
                            
                            writtenFiles = True
                            
                            if at.fileChangedFlag: # Set by replaceTargetFileIfDifferent.
                                changedFiles = True
                            #@nonl
                            #@-node:ekr.20040929105133.41:<< write the @file node >>
                            #@nl
                            at.closeWriteFile()
                p.moveToNodeAfterTree()
            elif p.isAtIgnoreNode():
                p.moveToNodeAfterTree()
            else:
                p.moveToThreadNext()
        
        if writtenFiles > 0:
            g.es("finished")
        else:
            g.es("no missing @file node in the selected tree")
            
        return changedFiles # So caller knows whether to do an auto-save.
    #@nonl
    #@-node:ekr.20040929105133.38:writeMissing
    #@+node:ekr.20040929105133.247:writeOpenFile
    # New in 4.3: must be inited before calling this method.
    
    def writeOpenFile(self,root,nosentinels=False,toString=False):
    
        """Do all writes except asis writes."""
        
        at = self ; c = at.c
    
        c.setIvarsFromPrefs()
        root.clearAllVisitedInTree() # Clear both vnode and tnode bits.
        root.clearVisitedInTree()
    
        #@    << put all @first lines in root >>
        #@+node:ekr.20040929105133.249:<< put all @first lines in root >> (4.x)
        #@+at 
        #@nonl
        # Write any @first lines.  These lines are also converted to @verbatim 
        # lines, so the read logic simply ignores lines preceding the @+leo 
        # sentinel.
        #@-at
        #@@c
        
        s = root.v.t.bodyString
        tag = "@first"
        i = 0
        while g.match(s,i,tag):
            i += len(tag)
            i = g.skip_ws(s,i)
            j = i
            i = g.skip_to_end_of_line(s,i)
            # Write @first line, whether empty or not
            line = s[j:i]
            at.os(line) ; at.onl()
            i = g.skip_nl(s,i)
        #@nonl
        #@-node:ekr.20040929105133.249:<< put all @first lines in root >> (4.x)
        #@nl
    
        # Put the main part of the file.
        at.putOpenLeoSentinel("@+leo-ver=4")
        at.putInitialComment()
        at.putOpenNodeSentinel(root)
        at.putBody(root)
        at.putCloseNodeSentinel(root)
        at.putSentinel("@-leo")
        root.setVisited()
        
        #@    << put all @last lines in root >>
        #@+node:ekr.20040929105133.250:<< put all @last lines in root >> (4.x)
        #@+at 
        #@nonl
        # Write any @last lines.  These lines are also converted to @verbatim 
        # lines, so the read logic simply ignores lines following the @-leo 
        # sentinel.
        #@-at
        #@@c
        
        tag = "@last"
        
        # 4/17/04 Use g.splitLines to preserve trailing newlines.
        lines = g.splitLines(root.v.t.bodyString)
        n = len(lines) ; j = k = n - 1
        
        # Scan backwards for @last directives.
        while j >= 0:
            line = lines[j]
            if g.match(line,0,tag): j -= 1
            elif not line.strip():
                j -= 1
            else: break
            
        # Write the @last lines.
        for line in lines[j+1:k+1]:
            if g.match(line,0,tag):
                i = len(tag) ; i = g.skip_ws(line,i)
                at.os(line[i:])
        #@nonl
        #@-node:ekr.20040929105133.250:<< put all @last lines in root >> (4.x)
        #@nl
        
        if not toString and not nosentinels:
            at.warnAboutOrphandAndIgnoredNodes()
    #@nonl
    #@-node:ekr.20040929105133.247:writeOpenFile
    #@-node:ekr.20040929105133.32:Writing (top level)
    #@+node:ekr.20040929105133.241:Writing 4.x
    #@+node:ekr.20040929105133.257:putBody
    # oneNodeOnly is no longer used.
    
    def putBody(self,p,putCloseSentinel=True,oneNodeOnly=False):
        
        """ Generate the body enclosed in sentinel lines."""
    
        at = self ; s = p.bodyString()
        
        p.v.t.setVisited() # Suppress orphans check.
        p.v.setVisited() # Make sure v is never expanded again.
        if not at.thinFile:
            p.v.t.setWriteBit() # Mark the tnode to be written.
            
        if not at.thinFile and not s: return
        inCode = True
        #@    << Make sure all lines end in a newline >>
        #@+node:ekr.20040929105133.258:<< Make sure all lines end in a newline >>
        # 11/20/03: except in nosentinel mode.
        # 1/30/04: and especially in scripting mode.
        # If we add a trailing newline, we'll generate an @nonl sentinel below.
        
        if s:
            trailingNewlineFlag = s and s[-1] == '\n'
            if at.sentinels and not trailingNewlineFlag:
                s = s + '\n'
        else:
            trailingNewlineFlag = True # don't need to generate an @nonl
        #@nonl
        #@-node:ekr.20040929105133.258:<< Make sure all lines end in a newline >>
        #@nl
        i = 0
        while i < len(s):
            next_i = g.skip_line(s,i)
            assert(next_i > i)
            kind = at.directiveKind4(s,i)
            #@        << handle line at s[i] >>
            #@+node:ekr.20040929105133.259:<< handle line at s[i]  >>
            if kind == at.noDirective:
                if not oneNodeOnly:
                    if inCode:
                        hasRef,n1,n2 = at.findSectionName(s,i)
                        if hasRef and not at.raw:
                            at.putRefLine(s,i,n1,n2,p)
                        else:
                            at.putCodeLine(s,i)
                    else:
                        at.putDocLine(s,i)
            elif kind in (at.docDirective,at.atDirective):
                assert(not at.pending)
                at.putStartDocLine(s,i,kind)
                inCode = False
            elif kind in (at.cDirective,at.codeDirective):
                # Only @c and @code end a doc part.
                if not inCode:
                    at.putEndDocLine() 
                at.putDirective(s,i)
                inCode = True
            elif kind == at.allDirective:
                if not oneNodeOnly:
                    if inCode: at.putAtAllLine(s,i,p)
                    else: at.putDocLine(s,i)
            elif kind == at.othersDirective:
                if not oneNodeOnly:
                    if inCode: at.putAtOthersLine(s,i,p)
                    else: at.putDocLine(s,i)
            elif kind == at.rawDirective:
                at.raw = True
                at.putSentinel("@@raw")
            elif kind == at.endRawDirective:
                at.raw = False
                at.putSentinel("@@end_raw")
                i = g.skip_line(s,i)
            elif kind == at.miscDirective:
                at.putDirective(s,i)
            else:
                assert(0) # Unknown directive.
            #@nonl
            #@-node:ekr.20040929105133.259:<< handle line at s[i]  >>
            #@nl
            i = next_i
        if not inCode:
            at.putEndDocLine()
        if at.sentinels and not trailingNewlineFlag:
            at.putSentinel("@nonl")
    #@nonl
    #@-node:ekr.20040929105133.257:putBody
    #@+node:ekr.20040929105133.260:writing code lines...
    #@+node:ekr.20040929105133.261:@all
    #@+node:ekr.20040929105133.262:putAtAllLine
    def putAtAllLine (self,s,i,p):
        
        """Put the expansion of @others."""
        
        at = self
        j,delta = g.skip_leading_ws_with_indent(s,i,at.tab_width)
        at.putLeadInSentinel(s,i,j,delta)
    
        at.indent += delta
        if at.leadingWs:
            at.putSentinel("@" + at.leadingWs + "@+all")
        else:
            at.putSentinel("@+all")
        
        for child in p.children_iter():
            at.putAtAllChild(child)
    
        at.putSentinel("@-all")
        at.indent -= delta
    #@nonl
    #@-node:ekr.20040929105133.262:putAtAllLine
    #@+node:ekr.20040929105133.263:putatAllBody
    def putAtAllBody(self,p,putCloseSentinel=True):
        
        """ Generate the body enclosed in sentinel lines."""
    
        at = self ; s = p.bodyString()
        
        p.v.setVisited()   # Make sure v is never expanded again.
        p.v.t.setVisited() # Use the tnode for the orphans check.
        if not at.thinFile and not s: return
        inCode = True
        #@    << Make sure all lines end in a newline >>
        #@+node:ekr.20040929105133.264:<< Make sure all lines end in a newline >>
        # 11/20/03: except in nosentinel mode.
        # 1/30/04: and especially in scripting mode.
        # If we add a trailing newline, we'll generate an @nonl sentinel below.
        
        if s:
            trailingNewlineFlag = s and s[-1] == '\n'
            if at.sentinels and not trailingNewlineFlag:
                s = s + '\n'
        else:
            trailingNewlineFlag = True # don't need to generate an @nonl
        #@nonl
        #@-node:ekr.20040929105133.264:<< Make sure all lines end in a newline >>
        #@nl
        i = 0
        while i < len(s):
            next_i = g.skip_line(s,i)
            assert(next_i > i)
            if inCode:
                # Use verbatim sentinels to write all directives.
                at.putCodeLine(s,i)
            else:
                at.putDocLine(s,i)
            i = next_i
    
        if not inCode:
            at.putEndDocLine()
        if at.sentinels and not trailingNewlineFlag:
            at.putSentinel("@nonl")
    #@nonl
    #@-node:ekr.20040929105133.263:putatAllBody
    #@+node:ekr.20040929105133.265:putAtAllChild
    #@+at
    # This code puts only the first of two or more cloned siblings, preceding 
    # the
    # clone with an @clone n sentinel.
    # 
    # This is a debatable choice: the cloned tree appears only once in the 
    # derived
    # file. This should be benign; the text created by @all is likely to be 
    # used only
    # for recreating the outline in Leo. The representation in the derived 
    # file
    # doesn't matter much.
    #@-at
    #@@c
    
    def putAtAllChild(self,p):
        
        at = self
        
        clonedSibs,thisClonedSibIndex = at.scanForClonedSibs(p.v)
        if clonedSibs > 1:
            if thisClonedSibIndex == 1:
                at.putSentinel("@clone %d" % (clonedSibs))
            else: return # Don't write second or greater trees.
    
        at.putOpenNodeSentinel(p,inAtAll=True) # Suppress warnings about @file nodes.
        at.putAtAllBody(p) 
        
        for child in p.children_iter():
            at.putAtAllChild(child)
    
        at.putCloseNodeSentinel(p,inAtAll=True)
    #@nonl
    #@-node:ekr.20040929105133.265:putAtAllChild
    #@-node:ekr.20040929105133.261:@all
    #@+node:ekr.20040929105133.266:@others
    #@+node:ekr.20040929105133.267:inAtOthers
    def inAtOthers(self,p):
        
        """Returns True if p should be included in the expansion of the at-others directive
        
        in the body text of p's parent."""
    
        # Return False if this has been expanded previously.
        if  p.v.isVisited():
            # g.trace("previously visited",p.v)
            return False
        
        # Return False if this is a definition node.
        h = p.headString() ; i = g.skip_ws(h,0)
        isSection,junk = self.isSectionName(h,i)
        if isSection:
            # g.trace("is section",p)
            return False
    
        # Return False if p's body contains an @ignore directive.
        if p.isAtIgnoreNode():
            # g.trace("is @ignore",p)
            return False
        else:
            # g.trace("ok",p)
            return True
    #@nonl
    #@-node:ekr.20040929105133.267:inAtOthers
    #@+node:ekr.20040929105133.268:putAtOthersChild
    def putAtOthersChild(self,p):
        
        at = self
    
        clonedSibs,thisClonedSibIndex = at.scanForClonedSibs(p.v)
        if clonedSibs > 1 and thisClonedSibIndex == 1:
            at.writeError("Cloned siblings are not valid in @thin trees")
    
        at.putOpenNodeSentinel(p,inAtOthers=True)
        at.putBody(p) 
        
        # Insert expansions of all children.
        for child in p.children_iter():
            if at.inAtOthers(child):
                at.putAtOthersChild(child)
                
        at.putCloseNodeSentinel(p,inAtOthers=True)
    #@nonl
    #@-node:ekr.20040929105133.268:putAtOthersChild
    #@+node:ekr.20040929105133.269:putAtOthersLine
    def putAtOthersLine (self,s,i,p):
        
        """Put the expansion of @others."""
        
        at = self
        j,delta = g.skip_leading_ws_with_indent(s,i,at.tab_width)
        at.putLeadInSentinel(s,i,j,delta)
    
        at.indent += delta
        if at.leadingWs:
            at.putSentinel("@" + at.leadingWs + "@+others")
        else:
            at.putSentinel("@+others")
        
        for child in p.children_iter():
            if at.inAtOthers(child):
                at.putAtOthersChild(child)
    
        at.putSentinel("@-others")
        at.indent -= delta
    #@nonl
    #@-node:ekr.20040929105133.269:putAtOthersLine
    #@-node:ekr.20040929105133.266:@others
    #@+node:ekr.20040929105133.270:putCodeLine
    def putCodeLine (self,s,i):
        
        """Put a normal code line."""
        
        at = self
        
        # Put @verbatim sentinel if required.
        k = g.skip_ws(s,i)
        if g.match(s,k,self.startSentinelComment + '@'):
            self.putSentinel("@verbatim")
    
        j = g.skip_line(s,i)
        line = s[i:j]
    
        # g.app.config.write_strips_blank_lines
        if 0: # 7/22/04: Don't put any whitespace in otherwise blank lines.
            if line.strip(): # The line has non-empty content.
                if not at.raw:
                    at.putIndent(at.indent)
            
                if line[-1:]=="\n":
                    at.os(line[:-1])
                    at.onl()
                else:
                    at.os(line)
            elif line and line[-1] == '\n':
                at.onl()
            else:
                g.trace("Can't happen: completely empty line")
        else:
            # 1/29/04: Don't put leading indent if the line is empty!
            if line and not at.raw:
                at.putIndent(at.indent)
        
            if line[-1:]=="\n":
                at.os(line[:-1])
                at.onl()
            else:
                at.os(line)
    #@nonl
    #@-node:ekr.20040929105133.270:putCodeLine
    #@+node:ekr.20040929105133.271:putRefLine & allies
    #@+node:ekr.20040929105133.272:putRefLine
    def putRefLine(self,s,i,n1,n2,p):
        
        """Put a line containing one or more references."""
        
        at = self
        
        # Compute delta only once.
        delta = self.putRefAt(s,i,n1,n2,p,delta=None)
        if delta is None: return # 11/23/03
        
        while 1:
            i = n2 + 2
            hasRef,n1,n2 = at.findSectionName(s,i)
            if hasRef:
                self.putAfterMiddleRef(s,i,n1,delta)
                self.putRefAt(s,n1,n1,n2,p,delta)
            else:
                break
        
        self.putAfterLastRef(s,i,delta)
    #@-node:ekr.20040929105133.272:putRefLine
    #@+node:ekr.20040929105133.273:putRefAt
    def putRefAt (self,s,i,n1,n2,p,delta):
        
        """Put a reference at s[n1:n2+2] from p."""
        
        at = self ; name = s[n1:n2+2]
    
        ref = g.findReference(name,p)
        if not ref:
            if not at.perfectImportRoot: # A kludge: we shouldn't be importing derived files here!
                at.writeError(
                    "undefined section: %s\n\treferenced from: %s" %
                    ( name,p.headString()))
            return None
        
        # Expand the ref.
        if not delta:
            junk,delta = g.skip_leading_ws_with_indent(s,i,at.tab_width)
    
        at.putLeadInSentinel(s,i,n1,delta)
        
        inBetween = []
        if at.thinFile: # @+-middle used only in thin files.
            parent = ref.parent()
            while parent != p:
                inBetween.append(parent)
                parent = parent.parent()
            
        at.indent += delta
        
        if at.leadingWs:
            at.putSentinel("@" + at.leadingWs + name)
        else:
            at.putSentinel("@" + name)
            
        if inBetween:
            for p2 in inBetween:
                at.putOpenNodeSentinel(p2,middle=True)
            
        at.putOpenNodeSentinel(ref)
        at.putBody(ref)
        at.putCloseNodeSentinel(ref)
        
        if inBetween:
            inBetween.reverse()
            for p2 in inBetween:
                at.putCloseNodeSentinel(p2,middle=True)
        
        at.indent -= delta
        
        return delta
    #@nonl
    #@-node:ekr.20040929105133.273:putRefAt
    #@+node:ekr.20040929105133.274:putAfterLastRef
    def putAfterLastRef (self,s,start,delta):
        
        """Handle whatever follows the last ref of a line."""
        
        at = self
        
        j = g.skip_ws(s,start)
        
        if j < len(s) and s[j] != '\n':
            end = g.skip_line(s,start)
            after = s[start:end] # Ends with a newline only if the line did.
            # Temporarily readjust delta to make @afterref look better.
            at.indent += delta
            at.putSentinel("@afterref")
            at.os(after)
            if at.sentinels and after and after[-1] != '\n':
                at.onl() # Add a newline if the line didn't end with one.
            at.indent -= delta
        else:
            # Temporarily readjust delta to make @nl look better.
            at.indent += delta
            at.putSentinel("@nl")
            at.indent -= delta
    #@nonl
    #@-node:ekr.20040929105133.274:putAfterLastRef
    #@+node:ekr.20040929105133.275:putAfterMiddleef
    def putAfterMiddleRef (self,s,start,end,delta):
        
        """Handle whatever follows a ref that is not the last ref of a line."""
        
        at = self
        
        if start < end:
            after = s[start:end]
            at.indent += delta
            at.putSentinel("@afterref")
            at.os(after) ; at.onl_sent() # Not a real newline.
            at.putSentinel("@nonl")
            at.indent -= delta
    #@nonl
    #@-node:ekr.20040929105133.275:putAfterMiddleef
    #@-node:ekr.20040929105133.271:putRefLine & allies
    #@-node:ekr.20040929105133.260:writing code lines...
    #@+node:ekr.20040929105133.276:writing doc lines...
    #@+node:ekr.20040929105133.277:putBlankDocLine
    def putBlankDocLine (self):
        
        at = self
        
        at.putPending(split=False)
    
        if not at.endSentinelComment:
            at.putIndent(at.indent)
            at.os(at.startSentinelComment) ; at.oblank()
    
        at.onl()
    #@nonl
    #@-node:ekr.20040929105133.277:putBlankDocLine
    #@+node:ekr.20040929105133.278:putStartDocLine
    def putStartDocLine (self,s,i,kind):
        
        """Write the start of a doc part."""
        
        at = self ; at.docKind = kind
        
        sentinel = g.choose(kind == at.docDirective,"@+doc","@+at")
        directive = g.choose(kind == at.docDirective,"@doc","@")
        
        if 0: # New code: put whatever follows the directive in the sentinel
            # Skip past the directive.
            i += len(directive)
            j = g.skip_to_end_of_line(s,i)
            follow = s[i:j]
        
            # Put the opening @+doc or @-doc sentinel, including whatever follows the directive.
            at.putSentinel(sentinel + follow)
    
            # Put the opening comment if we are using block comments.
            if at.endSentinelComment:
                at.putIndent(at.indent)
                at.os(at.startSentinelComment) ; at.onl()
        else: # old code.
            # Skip past the directive.
            i += len(directive)
        
            # Get the trailing whitespace.
            j = g.skip_ws(s,i)
            ws = s[i:j]
            
            # Put the opening @+doc or @-doc sentinel, including trailing whitespace.
            at.putSentinel(sentinel + ws)
        
            # Put the opening comment.
            if at.endSentinelComment:
                at.putIndent(at.indent)
                at.os(at.startSentinelComment) ; at.onl()
        
            # Put an @nonl sentinel if there is significant text following @doc or @.
            if not g.is_nl(s,j):
                # Doesn't work if we are using block comments.
                at.putSentinel("@nonl")
                at.putDocLine(s,j)
    #@nonl
    #@-node:ekr.20040929105133.278:putStartDocLine
    #@+node:ekr.20040929105133.279:putDocLine
    def putDocLine (self,s,i):
        
        """Handle one line of a doc part.
        
        Output complete lines and split long lines and queue pending lines.
        Inserted newlines are always preceded by whitespace."""
        
        at = self
        j = g.skip_line(s,i)
        s = s[i:j]
    
        if at.endSentinelComment:
            leading = at.indent
        else:
            leading = at.indent + len(at.startSentinelComment) + 1
    
        if not s or s[0] == '\n':
            # A blank line.
            at.putBlankDocLine()
        else:
            #@        << append words to pending line, splitting the line if needed >>
            #@+node:ekr.20040929105133.280:<< append words to pending line, splitting the line if needed >>
            #@+at 
            #@nonl
            # All inserted newlines are preceeded by whitespace:
            # we remove trailing whitespace from lines that have not been 
            # split.
            #@-at
            #@@c
            
            i = 0
            while i < len(s):
            
                # Scan to the next word.
                word1 = i # Start of the current word.
                word2 = i = g.skip_ws(s,i)
                while i < len(s) and s[i] not in (' ','\t'):
                    i += 1
                word3 = i = g.skip_ws(s,i)
                # g.trace(s[word1:i])
                
                if leading + word3 - word1 + len(''.join(at.pending)) >= at.page_width:
                    if at.pending:
                        # g.trace("splitting long line.")
                        # Ouput the pending line, and start a new line.
                        at.putPending(split=True)
                        at.pending = [s[word2:word3]]
                    else:
                        # Output a long word on a line by itself.
                        # g.trace("long word:",s[word2:word3])
                        at.pending = [s[word2:word3]]
                        at.putPending(split=True)
                else:
                    # Append the entire word to the pending line.
                    # g.trace("appending",s[word1:word3])
                    at.pending.append(s[word1:word3])
                        
            # Output the remaining line: no more is left.
            at.putPending(split=False)
            #@nonl
            #@-node:ekr.20040929105133.280:<< append words to pending line, splitting the line if needed >>
            #@nl
    #@-node:ekr.20040929105133.279:putDocLine
    #@+node:ekr.20040929105133.281:putEndDocLine
    def putEndDocLine (self):
        
        """Write the conclusion of a doc part."""
        
        at = self
        
        at.putPending(split=False)
        
        # Put the closing delimiter if we are using block comments.
        if at.endSentinelComment:
            at.putIndent(at.indent)
            at.os(at.endSentinelComment)
            at.onl() # Note: no trailing whitespace.
    
        sentinel = g.choose(at.docKind == at.docDirective,"@-doc","@-at")
        at.putSentinel(sentinel)
    #@nonl
    #@-node:ekr.20040929105133.281:putEndDocLine
    #@+node:ekr.20040929105133.282:putPending
    def putPending (self,split):
        
        """Write the pending part of a doc part.
        
        We retain trailing whitespace iff the split flag is True."""
        
        at = self ; s = ''.join(at.pending) ; at.pending = []
        
        # g.trace("split",s)
        
        # Remove trailing newline temporarily.  We'll add it back later.
        if s and s[-1] == '\n':
            s = s[:-1]
    
        if not split:
            s = s.rstrip()
            if not s:
                return
    
        at.putIndent(at.indent)
    
        if not at.endSentinelComment:
            at.os(at.startSentinelComment) ; at.oblank()
    
        at.os(s) ; at.onl()
    #@nonl
    #@-node:ekr.20040929105133.282:putPending
    #@-node:ekr.20040929105133.276:writing doc lines...
    #@-node:ekr.20040929105133.241:Writing 4.x
    #@+node:ekr.20040929105133.230:Writing 4,x sentinels...
    #@+node:ekr.20040929105133.231:nodeSentinelText 4.x
    def nodeSentinelText(self,p):
        
        """Return the text of a @+node or @-node sentinel for p."""
        
        at = self ; h = p.headString()
        #@    << remove comment delims from h if necessary >>
        #@+node:ekr.20040929105133.232:<< remove comment delims from h if necessary >>
        #@+at 
        #@nonl
        # Bug fix 1/24/03:
        # 
        # If the present @language/@comment settings do not specify a 
        # single-line comment we remove all block comment delims from h.  This 
        # prevents headline text from interfering with the parsing of node 
        # sentinels.
        #@-at
        #@@c
        
        start = at.startSentinelComment
        end = at.endSentinelComment
        
        if end and len(end) > 0:
            h = h.replace(start,"")
            h = h.replace(end,"")
        #@nonl
        #@-node:ekr.20040929105133.232:<< remove comment delims from h if necessary >>
        #@nl
        
        if at.thinFile:
            gnx = g.app.nodeIndices.toString(p.v.t.fileIndex)
            return "%s:%s" % (gnx,h)
        else:
            return h
    #@nonl
    #@-node:ekr.20040929105133.231:nodeSentinelText 4.x
    #@+node:ekr.20040929105133.233:putLeadInSentinel 4.x
    def putLeadInSentinel (self,s,i,j,delta):
        
        """Generate @nonl sentinels as needed to ensure a newline before a group of sentinels.
        
        Set at.leadingWs as needed for @+others and @+<< sentinels.
    
        i points at the start of a line.
        j points at @others or a section reference.
        delta is the change in at.indent that is about to happen and hasn't happened yet."""
    
        at = self
        at.leadingWs = "" # Set the default.
        if i == j:
            return # The @others or ref starts a line.
    
        k = g.skip_ws(s,i)
        if j == k:
            # Only whitespace before the @others or ref.
            at.leadingWs = s[i:j] # Remember the leading whitespace, including its spelling.
        else:
            # g.trace("indent",self.indent)
            self.putIndent(self.indent) # 1/29/04: fix bug reported by Dan Winkler.
            at.os(s[i:j]) ; at.onl_sent() # 10/21/03
            at.indent += delta # Align the @nonl with the following line.
            at.putSentinel("@nonl")
            at.indent -= delta # Let the caller set at.indent permanently.
    #@nonl
    #@-node:ekr.20040929105133.233:putLeadInSentinel 4.x
    #@+node:ekr.20040929105133.234:putCloseNodeSentinel 4.x
    def putCloseNodeSentinel(self,p,inAtAll=False,inAtOthers=False,middle=False):
        
        at = self
        
        s = self.nodeSentinelText(p)
        
        if middle:
            at.putSentinel("@-middle:" + s)
        else:
            at.putSentinel("@-node:" + s)
    #@nonl
    #@-node:ekr.20040929105133.234:putCloseNodeSentinel 4.x
    #@+node:ekr.20040929105133.235:putOpenLeoSentinel 4.x
    def putOpenLeoSentinel(self,s):
        
        """Write @+leo sentinel."""
    
        at = self
        
        if not at.sentinels:
            return # Handle @nosentinelsfile.
            
        if at.thinFile:
            s = s + "-thin"
    
        encoding = at.encoding.lower()
        if encoding != "utf-8":
            # New in 4.2: encoding fields end in ",."
            s = s + "-encoding=%s,." % (encoding)
        
        at.putSentinel(s)
    #@nonl
    #@-node:ekr.20040929105133.235:putOpenLeoSentinel 4.x
    #@+node:ekr.20040929105133.236:putOpenNodeSentinel (sets tnodeList) 4.x
    def putOpenNodeSentinel(self,p,inAtAll=False,inAtOthers=False,middle=False):
        
        """Write @+node sentinel for p."""
        
        at = self
    
        if not inAtAll and p.isAtFileNode() and p != at.root:
            at.writeError("@file not valid in: " + p.headString())
            return
            
        # g.trace(at.thinFile,p)
            
        s = at.nodeSentinelText(p)
        
        if middle:
            at.putSentinel("@+middle:" + s)
        else:
            at.putSentinel("@+node:" + s)
        
        if not at.thinFile:
            # Append the n'th tnode to the root's tnode list.
            at.root.v.t.tnodeList.append(p.v.t)
    #@nonl
    #@-node:ekr.20040929105133.236:putOpenNodeSentinel (sets tnodeList) 4.x
    #@+node:ekr.20040929105133.237:putSentinel (applies cweb hack) 4.x
    # This method outputs all sentinels.
    
    def putSentinel(self,s):
    
        "Write a sentinel whose text is s, applying the CWEB hack if needed."
        
        at = self
    
        if not at.sentinels:
            return # Handle @file-nosent
    
        at.putIndent(at.indent)
        at.os(at.startSentinelComment)
        #@    << apply the cweb hack to s >>
        #@+node:ekr.20040929105133.238:<< apply the cweb hack to s >>
        #@+at 
        #@nonl
        # The cweb hack:
        # 
        # If the opening comment delim ends in '@', double all '@' signs 
        # except the first, which is "doubled" by the trailing '@' in the 
        # opening comment delimiter.
        #@-at
        #@@c
        
        start = at.startSentinelComment
        if start and start[-1] == '@':
            assert(s and s[0]=='@')
            s = s.replace('@','@@')[1:]
        #@nonl
        #@-node:ekr.20040929105133.238:<< apply the cweb hack to s >>
        #@nl
        at.os(s)
        if at.endSentinelComment:
            at.os(at.endSentinelComment)
        at.onl()
    #@nonl
    #@-node:ekr.20040929105133.237:putSentinel (applies cweb hack) 4.x
    #@-node:ekr.20040929105133.230:Writing 4,x sentinels...
    #@+node:ekr.20040930081343.2:Writing 4.x utils...
    #@+node:ekr.20040929105133.142:compareFilesIgnoringLineEndings
    # This routine is needed to handle cvs stupidities.
    
    def compareFilesIgnoringLineEndings (self,path1,path2):
    
        """Compare two text files ignoring line endings."""
        
        try:
            # Opening both files in text mode converts all line endings to '\n'.
            f1 = open(path1) ; f2 = open(path2)
            equal = f1.read() == f2.read()
            f1.close() ; f2.close()
            return equal
        except:
            return False
    #@nonl
    #@-node:ekr.20040929105133.142:compareFilesIgnoringLineEndings
    #@+node:ekr.20040929105133.284:directiveKind4
    def directiveKind4(self,s,i):
        
        """Return the kind of at-directive or noDirective."""
    
        at = self
        n = len(s)
        if i >= n or s[i] != '@':
            j = g.skip_ws(s,i)
            if g.match_word(s,j,"@others"):
                return at.othersDirective
            elif g.match_word(s,j,"@all"):
                return at.allDirective
            else:
                return at.noDirective
    
        table = (
            ("@all",at.allDirective),
            ("@c",at.cDirective),
            ("@code",at.codeDirective),
            ("@doc",at.docDirective),
            ("@end_raw",at.endRawDirective),
            ("@others",at.othersDirective),
            ("@raw",at.rawDirective))
    
        # This code rarely gets executed, so simple code suffices.
        if i+1 >= n or g.match(s,i,"@ ") or g.match(s,i,"@\t") or g.match(s,i,"@\n"):
            # 10/25/02: @space is not recognized in cweb mode.
            # Noweb doc parts are _never_ scanned in cweb mode.
            return g.choose(at.language=="cweb",
                at.noDirective,at.atDirective)
    
        # @c and @(nonalpha) are not recognized in cweb mode.
        # We treat @(nonalpha) separately because @ is in the colorizer table.
        if at.language=="cweb" and (
            g.match_word(s,i,"@c") or
            i+1>= n or s[i+1] not in string.ascii_letters):
            return at.noDirective
    
        for name,directive in table:
            if g.match_word(s,i,name):
                return directive
    
        # Return miscDirective only for real directives.
        for name in leoColor.leoKeywords:
            if g.match_word(s,i,name):
                return at.miscDirective
    
        return at.noDirective
    #@nonl
    #@-node:ekr.20040929105133.284:directiveKind4
    #@+node:ekr.20040929105133.285:hasSectionName
    def findSectionName(self,s,i):
        
        end = s.find('\n',i)
        if end == -1:
            n1 = s.find("<<",i)
            n2 = s.find(">>",i)
        else:
            n1 = s.find("<<",i,end)
            n2 = s.find(">>",i,end)
    
        return -1 < n1 < n2, n1, n2
    #@nonl
    #@-node:ekr.20040929105133.285:hasSectionName
    #@+node:ekr.20040929105133.170:isSectionName
    # returns (flag, end). end is the index of the character after the section name.
    
    def isSectionName(self,s,i):
    
        if not g.match(s,i,"<<"):
            return False, -1
        i = g.find_on_line(s,i,">>")
        if i:
            return True, i + 2
        else:
            return False, -1
    #@nonl
    #@-node:ekr.20040929105133.170:isSectionName
    #@+node:ekr.20040929105133.286:os and allies
    # Note:  self.outputFile may be either a fileLikeObject or a real file.
    
    #@+node:ekr.20040929105133.287:oblank, oblanks & otabs
    def oblank(self):
        self.os(' ')
    
    def oblanks (self,n):
        self.os(' ' * abs(n))
        
    def otabs(self,n):
        self.os('\t' * abs(n))
    #@nonl
    #@-node:ekr.20040929105133.287:oblank, oblanks & otabs
    #@+node:ekr.20040929105133.288:onl & onl_sent
    def onl(self):
        
        """Write a newline to the output stream."""
    
        self.os(self.output_newline)
        
    def onl_sent(self):
        
        """Write a newline to the output stream, provided we are outputting sentinels."""
    
        if self.sentinels:
            self.onl()
    #@nonl
    #@-node:ekr.20040929105133.288:onl & onl_sent
    #@+node:ekr.20040929105133.289:os
    def os (self,s):
        
        """Write a string to the output stream.
        
        All output produced by leoAtFile module goes here."""
        
        at = self
        
        if s and at.outputFile:
            try:
                s = g.toEncodedString(s,at.encoding,reportErrors=True)
                at.outputFile.write(s)
            except:
                at.exception("exception writing:" + s)
    #@nonl
    #@-node:ekr.20040929105133.289:os
    #@-node:ekr.20040929105133.286:os and allies
    #@+node:ekr.20040929105133.150:outputStringWithLineEndings
    # Write the string s as-is except that we replace '\n' with the proper line ending.
    
    def outputStringWithLineEndings (self,s):
    
        # Calling self.onl() runs afoul of queued newlines.
        self.os(s.replace('\n',self.output_newline))
    #@nonl
    #@-node:ekr.20040929105133.150:outputStringWithLineEndings
    #@+node:ekr.20040929105133.290:putDirective  (handles @delims,@comment,@language) 4.x
    #@+at 
    #@nonl
    # It is important for PHP and other situations that @first and @last 
    # directives get translated to verbatim lines that do _not_ include what 
    # follows the @first & @last directives.
    #@-at
    #@@c
    
    def putDirective(self,s,i):
        
        """Output a sentinel a directive or reference s."""
    
        tag = "@delims"
        assert(i < len(s) and s[i] == '@')
        k = i
        j = g.skip_to_end_of_line(s,i)
        directive = s[i:j]
    
        if g.match_word(s,k,"@delims"):
            #@        << handle @delims >>
            #@+node:ekr.20040929105133.291:<< handle @delims >>
            # Put a space to protect the last delim.
            self.putSentinel(directive + " ") # 10/23/02: put @delims, not @@delims
            
            # Skip the keyword and whitespace.
            j = i = g.skip_ws(s,k+len(tag))
            
            # Get the first delim.
            while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
                i += 1
            if j < i:
                self.startSentinelComment = s[j:i]
                # Get the optional second delim.
                j = i = g.skip_ws(s,i)
                while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
                    i += 1
                self.endSentinelComment = g.choose(j<i, s[j:i], "")
            else:
                self.writeError("Bad @delims directive")
            #@nonl
            #@-node:ekr.20040929105133.291:<< handle @delims >>
            #@nl
        elif g.match_word(s,k,"@language"):
            #@        << handle @language >>
            #@+node:ekr.20040929105133.292:<< handle @language >>
            self.putSentinel("@" + directive)
            
            # Skip the keyword and whitespace.
            i = k + len("@language")
            i = g.skip_ws(s,i)
            j = g.skip_c_id(s,i)
            language = s[i:j]
            
            delim1,delim2,delim3 = g.set_delims_from_language(language)
            
            # g.trace(delim1,delim2,delim3)
            
            # Returns a tuple (single,start,end) of comment delims
            if delim1:
                self.startSentinelComment = delim1
                self.endSentinelComment = ""
            elif delim2 and delim3:
                self.startSentinelComment = delim2
                self.endSentinelComment = delim3
            else:
                line = g.get_line(s,i)
                g.es("Ignoring bad @language directive: %s" % line,color="blue")
            #@nonl
            #@-node:ekr.20040929105133.292:<< handle @language >>
            #@nl
        elif g.match_word(s,k,"@comment"):
            #@        << handle @comment >>
            #@+node:ekr.20040929105133.293:<< handle @comment >>
            self.putSentinel("@" + directive)
            
            j = g.skip_line(s,i)
            line = s[i:j]
            delim1,delim2,delim3 = g.set_delims_from_string(line)
            
            # g.trace(delim1,delim2,delim3)
            
            # Returns a tuple (single,start,end) of comment delims
            if delim1:
                self.startSentinelComment = delim1
                self.endSentinelComment = None
            elif delim2 and delim3:
                self.startSentinelComment = delim2
                self.endSentinelComment = delim3
            else:
                g.es("Ignoring bad @comment directive: %s" % line,color="blue")
            #@nonl
            #@-node:ekr.20040929105133.293:<< handle @comment >>
            #@nl
        elif g.match_word(s,k,"@last"):
            self.putSentinel("@@last") # 10/27/03: Convert to an verbatim line _without_ anything else.
        elif g.match_word(s,k,"@first"):
            self.putSentinel("@@first") # 10/27/03: Convert to an verbatim line _without_ anything else.
        else:
            self.putSentinel("@" + directive)
    
        i = g.skip_line(s,k)
        return i
    #@nonl
    #@-node:ekr.20040929105133.290:putDirective  (handles @delims,@comment,@language) 4.x
    #@+node:ekr.20040929105133.182:putIndent
    def putIndent(self,n):
        
        """Put tabs and spaces corresponding to n spaces, assuming that we are at the start of a line."""
    
        if n != 0:
            w = self.tab_width
            if w > 1:
                q,r = divmod(n,w) 
                self.otabs(q) 
                self.oblanks(r)
            else:
                self.oblanks(n)
    #@nonl
    #@-node:ekr.20040929105133.182:putIndent
    #@+node:ekr.20040929105133.145:putInitialComment
    def putInitialComment (self):
        
        s2 = g.app.config.output_initial_comment
        if s2:
            lines = string.split(s2,"\\n")
            for line in lines:
                line = line.replace("@date",time.asctime())
                if len(line)> 0:
                    self.putSentinel("@comment " + line)
    #@nonl
    #@-node:ekr.20040929105133.145:putInitialComment
    #@+node:ekr.20040929105133.146:replaceTargetFileIfDifferent
    def replaceTargetFileIfDifferent (self):
        
        assert(self.outputFile is None)
        
        self.fileChangedFlag = False
        if g.os_path_exists(self.targetFileName):
            if self.compareFilesIgnoringLineEndings(
                self.outputFileName,self.targetFileName):
                #@            << delete the output file >>
                #@+node:ekr.20040929105133.147:<< delete the output file >>
                try: # Just delete the temp file.
                    os.remove(self.outputFileName)
                except:
                    g.es("exception deleting:" + self.outputFileName)
                    g.es_exception()
                
                g.es("unchanged: " + self.shortFileName)
                #@nonl
                #@-node:ekr.20040929105133.147:<< delete the output file >>
                #@nl
            else:
                #@            << replace the target file with the output file >>
                #@+node:ekr.20040929105133.148:<< replace the target file with the output file >>
                try:
                    # 10/6/02: retain the access mode of the previous file,
                    # removing any setuid, setgid, and sticky bits.
                    mode = (os.stat(self.targetFileName))[0] & 0777
                except:
                    mode = None
                
                try: # Replace target file with temp file.
                    os.remove(self.targetFileName)
                    try:
                        g.utils_rename(self.outputFileName,self.targetFileName)
                        if mode != None: # 10/3/02: retain the access mode of the previous file.
                            try:
                                os.chmod(self.targetFileName,mode)
                            except:
                                g.es("exception in os.chmod(%s)" % (self.targetFileName))
                        g.es("writing: " + self.shortFileName)
                        self.fileChangedFlag = True
                    except:
                        # 6/28/03
                        self.writeError("exception renaming: %s to: %s" % (self.outputFileName,self.targetFileName))
                        g.es_exception()
                except:
                    self.writeError("exception removing:" + self.targetFileName)
                    g.es_exception()
                    try: # Delete the temp file when the deleting the target file fails.
                        os.remove(self.outputFileName)
                    except:
                        g.es("exception deleting:" + self.outputFileName)
                        g.es_exception()
                #@nonl
                #@-node:ekr.20040929105133.148:<< replace the target file with the output file >>
                #@nl
        else:
            #@        << rename the output file to be the target file >>
            #@+node:ekr.20040929105133.149:<< rename the output file to be the target file >>
            try:
                g.utils_rename(self.outputFileName,self.targetFileName)
                g.es("creating: " + self.targetFileName)
                self.fileChangedFlag = True
            except:
                self.writeError("exception renaming:" + self.outputFileName +
                    " to " + self.targetFileName)
                g.es_exception()
            #@nonl
            #@-node:ekr.20040929105133.149:<< rename the output file to be the target file >>
            #@nl
    #@nonl
    #@-node:ekr.20040929105133.146:replaceTargetFileIfDifferent
    #@+node:ekr.20040929105133.151:warnAboutOrpanAndIgnoredNodes
    def warnAboutOrphandAndIgnoredNodes (self):
        
        # Always warn, even when language=="cweb"
        at = self ; root = at.root
    
        for p in root.self_and_subtree_iter():
            if not p.v.t.isVisited(): # Check tnode bit, not vnode bit.
                at.writeError("Orphan node:  " + p.headString())
                if p.isCloned() and p.hasParent():
                    g.es("parent node: " + p.parent().headString(),color="blue")
                if not at.thinFile and p.isAtIgnoreNode():
                    at.writeError("@ignore node: " + p.headString())
                    
        if at.thinFile:
            p = root.copy() ; after = p.nodeAfterTree()
            while p and p != after:
                if p.isAtAllNode():
                    p.moveToNodeAfterTree()
                else:
                    if p.isAtIgnoreNode():
                        at.writeError("@ignore node: " + p.headString())
                    p.moveToThreadNext()
    #@nonl
    #@-node:ekr.20040929105133.151:warnAboutOrpanAndIgnoredNodes
    #@+node:ekr.20040929105133.122:writeError
    def writeError(self,message):
    
        if self.errors == 0:
            g.es_error("errors writing: " + self.targetFileName)
    
        self.error(message)
        self.root.setOrphan()
        self.root.setDirty()
    #@nonl
    #@-node:ekr.20040929105133.122:writeError
    #@+node:ekr.20040929105133.143:writeException
    def writeException (self,root=None):
        
        g.es("exception writing:" + self.targetFileName,color="red")
        g.es_exception()
    
        if self.outputFile:
            self.outputFile.flush()
            self.outputFile.close()
            self.outputFile = None
        
        if self.outputFileName != None:
            try: # Just delete the temp file.
                os.remove(self.outputFileName)
            except:
                g.es("exception deleting:" + self.outputFileName,color="red")
                g.es_exception()
    
        if root:
            # Make sure we try to rewrite this file.
            root.setOrphan()
            root.setDirty()
    #@nonl
    #@-node:ekr.20040929105133.143:writeException
    #@-node:ekr.20040930081343.2:Writing 4.x utils...
    #@-node:ekr.20040930080842.1:Writing...
    #@+node:ekr.20040929105133.103:Uilites...
    #@+node:ekr.20040929105133.105:error
    def error(self,message):
    
        g.es_error(message)
        self.errors += 1
    #@nonl
    #@-node:ekr.20040929105133.105:error
    #@+node:ekr.20040929162647:exception
    def exception (self,message):
        
        self.error(message)
        g.es_exception()
    #@nonl
    #@-node:ekr.20040929162647:exception
    #@+node:ekr.20040929105133.107:scanAllDirectives
    #@+at 
    #@nonl
    # Once a directive is seen, no other related directives in nodes further 
    # up the tree have any effect.  For example, if an @color directive is 
    # seen in node p, no @color or @nocolor directives are examined in any 
    # ancestor of p.
    # 
    # This code is similar to Commands.scanAllDirectives, but it has been 
    # modified for use by the atFile class.
    #@-at
    #@@c
    
    def scanAllDirectives(self,p,scripting=False,importing=False,reading=False):
        
        """Scan position p and p's ancestors looking for directives,
        setting corresponding atFile ivars.
        """
    
        c = self.c
        #@    << Set ivars >>
        #@+node:ekr.20040929105133.108:<< Set ivars >>
        self.page_width = self.c.page_width
        self.tab_width  = self.c.tab_width
        
        self.default_directory = None # 8/2: will be set later.
        
        delim1, delim2, delim3 = g.set_delims_from_language(c.target_language)
        self.language = c.target_language
        
        self.encoding = g.app.config.default_derived_file_encoding
        self.output_newline = g.getOutputNewline() # 4/24/03: initialize from config settings.
        #@nonl
        #@-node:ekr.20040929105133.108:<< Set ivars >>
        #@nl
        #@    << Set path from @file node >>
        #@+node:ekr.20040929105133.109:<< Set path from @file node >> in scanDirectory in leoGlobals.py
        # An absolute path in an @file node over-rides everything else.
        # A relative path gets appended to the relative path by the open logic.
        
        name = p.anyAtFileNodeName() # 4/28/04
        
        theDir = g.choose(name,g.os_path_dirname(name),None)
        
        if theDir and len(theDir) > 0 and g.os_path_isabs(theDir):
            if g.os_path_exists(theDir):
                self.default_directory = theDir
            else: # 9/25/02
                self.default_directory = g.makeAllNonExistentDirectories(theDir)
                if not self.default_directory:
                    self.error("Directory \"" + theDir + "\" does not exist")
        #@nonl
        #@-node:ekr.20040929105133.109:<< Set path from @file node >> in scanDirectory in leoGlobals.py
        #@nl
        old = {}
        for p in p.self_and_parents_iter():
            s = p.v.t.bodyString
            theDict = g.get_directives_dict(s)
            #@        << Test for @path >>
            #@+node:ekr.20040929105133.114:<< Test for @path >>
            # We set the current director to a path so future writes will go to that directory.
            
            if not self.default_directory and not old.has_key("path") and theDict.has_key("path"):
            
                k = theDict["path"]
                #@    << compute relative path from s[k:] >>
                #@+node:ekr.20040929105133.115:<< compute relative path from s[k:] >>
                j = i = k + len("@path")
                i = g.skip_to_end_of_line(s,i)
                path = string.strip(s[j:i])
                
                # Remove leading and trailing delims if they exist.
                if len(path) > 2 and (
                    (path[0]=='<' and path[-1] == '>') or
                    (path[0]=='"' and path[-1] == '"') ):
                    path = path[1:-1]
                path = path.strip()
                
                if 0: # 11/14/02: we want a _relative_ path, not an absolute path.
                    path = g.os_path_join(g.app.loadDir,path)
                #@nonl
                #@-node:ekr.20040929105133.115:<< compute relative path from s[k:] >>
                #@nl
                if path and len(path) > 0:
                    base = g.getBaseDirectory() # returns "" on error.
                    path = g.os_path_join(base,path)
                    if g.os_path_isabs(path):
                        #@            << handle absolute path >>
                        #@+node:ekr.20040929105133.116:<< handle absolute path >>
                        # path is an absolute path.
                        
                        if g.os_path_exists(path):
                            self.default_directory = path
                        else: # 9/25/02
                            self.default_directory = g.makeAllNonExistentDirectories(path)
                            if not self.default_directory:
                                self.error("invalid @path: " + path)
                        #@-node:ekr.20040929105133.116:<< handle absolute path >>
                        #@nl
                    else:
                        self.error("ignoring bad @path: " + path)
                else:
                    self.error("ignoring empty @path")
            #@nonl
            #@-node:ekr.20040929105133.114:<< Test for @path >>
            #@nl
            #@        << Test for @encoding >>
            #@+node:ekr.20040929105133.111:<< Test for @encoding >>
            if not old.has_key("encoding") and theDict.has_key("encoding"):
                
                e = g.scanAtEncodingDirective(s,theDict)
                if e:
                    self.encoding = e
            #@nonl
            #@-node:ekr.20040929105133.111:<< Test for @encoding >>
            #@nl
            #@        << Test for @comment and @language >>
            #@+node:ekr.20040929105133.110:<< Test for @comment and @language >>
            # 10/17/02: @language and @comment may coexist in @file trees.
            # For this to be effective the @comment directive should follow the @language directive.
            
            if not old.has_key("comment") and theDict.has_key("comment"):
                k = theDict["comment"]
                # 11/14/02: Similar to fix below.
                delim1, delim2, delim3 = g.set_delims_from_string(s[k:])
            
            # Reversion fix: 12/06/02: We must use elif here, not if.
            elif not old.has_key("language") and theDict.has_key("language"):
                k = theDict["language"]
                # 11/14/02: Fix bug reported by J.M.Gilligan.
                self.language,delim1,delim2,delim3 = g.set_language(s,k)
            #@nonl
            #@-node:ekr.20040929105133.110:<< Test for @comment and @language >>
            #@nl
            #@        << Test for @header and @noheader >>
            #@+node:ekr.20040929105133.112:<< Test for @header and @noheader >>
            # EKR: 10/10/02: perform the sames checks done by tangle.scanAllDirectives.
            if theDict.has_key("header") and theDict.has_key("noheader"):
                g.es("conflicting @header and @noheader directives")
            #@nonl
            #@-node:ekr.20040929105133.112:<< Test for @header and @noheader >>
            #@nl
            #@        << Test for @lineending >>
            #@+node:ekr.20040929105133.113:<< Test for @lineending >>
            if not old.has_key("lineending") and theDict.has_key("lineending"):
                
                lineending = g.scanAtLineendingDirective(s,theDict)
                if lineending:
                    self.output_newline = lineending
            #@-node:ekr.20040929105133.113:<< Test for @lineending >>
            #@nl
            #@        << Test for @pagewidth >>
            #@+node:ekr.20040929105133.117:<< Test for @pagewidth >>
            if theDict.has_key("pagewidth") and not old.has_key("pagewidth"):
                
                w = g.scanAtPagewidthDirective(s,theDict,issue_error_flag=True)
                if w and w > 0:
                    self.page_width = w
            #@nonl
            #@-node:ekr.20040929105133.117:<< Test for @pagewidth >>
            #@nl
            #@        << Test for @tabwidth >>
            #@+node:ekr.20040929105133.118:<< Test for @tabwidth >>
            if theDict.has_key("tabwidth") and not old.has_key("tabwidth"):
                
                w = g.scanAtTabwidthDirective(s,theDict,issue_error_flag=True)
                if w and w != 0:
                    self.tab_width = w
            
            #@-node:ekr.20040929105133.118:<< Test for @tabwidth >>
            #@nl
            old.update(theDict)
        #@    << Set current directory >>
        #@+node:ekr.20040929105133.119:<< Set current directory >>
        # This code is executed if no valid absolute path was specified in the @file node or in an @path directive.
        
        if c.frame and not self.default_directory:
            base = g.getBaseDirectory() # returns "" on error.
            for theDir in (c.tangle_directory,c.frame.openDirectory,c.openDirectory):
                if theDir and len(theDir) > 0:
                    theDir = g.os_path_join(base,theDir)
                    if g.os_path_isabs(theDir): # Errors may result in relative or invalid path.
                        if g.os_path_exists(theDir):
                            self.default_directory = theDir ; break
                        else: # 9/25/02
                            self.default_directory = g.makeAllNonExistentDirectories(theDir)
        
        if not self.default_directory and not scripting and not importing:
            # This should never happen: c.openDirectory should be a good last resort.
            g.trace()
            self.error("No absolute directory specified anywhere.")
            self.default_directory = ""
        #@-node:ekr.20040929105133.119:<< Set current directory >>
        #@nl
        if not importing and not reading:
            # 5/19/04: don't override comment delims when reading!
            #@        << Set comment strings from delims >>
            #@+node:ekr.20040929105133.120:<< Set comment strings from delims >>
            if scripting:
                # Force Python language.
                delim1,delim2,delim3 = g.set_delims_from_language("python")
                self.language = "python"
                
            # Use single-line comments if we have a choice.
            # 8/2/01: delim1,delim2,delim3 now correspond to line,start,end
            
            if delim1:
                self.startSentinelComment = delim1
                self.endSentinelComment = "" # Must not be None.
            elif delim2 and delim3:
                self.startSentinelComment = delim2
                self.endSentinelComment = delim3
            else: # Emergency!
                # assert(0)
                g.es("Unknown language: using Python comment delimiters")
                g.es("c.target_language:",c.target_language)
                g.es("delim1,delim2,delim3:",delim1,delim2,delim3)
                self.startSentinelComment = "#" # This should never happen!
                self.endSentinelComment = ""
                
            # g.trace(repr(self.startSentinelComment),repr(self.endSentinelComment))
            #@nonl
            #@-node:ekr.20040929105133.120:<< Set comment strings from delims >>
            #@nl
    #@nonl
    #@-node:ekr.20040929105133.107:scanAllDirectives
    #@+node:ekr.20040929105133.24:scanDefaultDirectory
    def scanDefaultDirectory(self,p,importing=False):
        
        """Set default_directory ivar by looking for @path directives."""
    
        at = self ; c = at.c
        at.default_directory = None
        #@    << Set path from @file node >>
        #@+node:ekr.20040929105133.25:<< Set path from @file node >>  in df.scanDeafaultDirectory in leoAtFile.py
        # An absolute path in an @file node over-rides everything else.
        # A relative path gets appended to the relative path by the open logic.
        
        name = p.anyAtFileNodeName() # 4/28/04
            
        theDir = g.choose(name,g.os_path_dirname(name),None)
        
        if theDir and g.os_path_isabs(theDir):
            if g.os_path_exists(theDir):
                at.default_directory = theDir
            else:
                at.default_directory = g.makeAllNonExistentDirectories(theDir)
                if not at.default_directory:
                    at.error("Directory \"" + theDir + "\" does not exist")
        #@nonl
        #@-node:ekr.20040929105133.25:<< Set path from @file node >>  in df.scanDeafaultDirectory in leoAtFile.py
        #@nl
        if at.default_directory:
            return
            
        for p in p.self_and_parents_iter():
            s = p.v.t.bodyString
            theDict = g.get_directives_dict(s)
            if theDict.has_key("path"):
                #@            << handle @path >>
                #@+node:ekr.20040929105133.26:<< handle @path >> in df.scanDeafaultDirectory in leoAtFile.py
                # We set the current director to a path so future writes will go to that directory.
                
                k = theDict["path"]
                #@<< compute relative path from s[k:] >>
                #@+node:ekr.20040929105133.27:<< compute relative path from s[k:] >>
                j = i = k + len("@path")
                i = g.skip_to_end_of_line(s,i)
                path = string.strip(s[j:i])
                
                # Remove leading and trailing delims if they exist.
                if len(path) > 2 and (
                    (path[0]=='<' and path[-1] == '>') or
                    (path[0]=='"' and path[-1] == '"') ):
                    path = path[1:-1]
                
                path = path.strip()
                #@nonl
                #@-node:ekr.20040929105133.27:<< compute relative path from s[k:] >>
                #@nl
                
                if path and len(path) > 0:
                    base = g.getBaseDirectory() # returns "" on error.
                    path = g.os_path_join(base,path)
                    
                    if g.os_path_isabs(path):
                        #@        << handle absolute path >>
                        #@+node:ekr.20040929105133.28:<< handle absolute path >>
                        # path is an absolute path.
                        
                        if g.os_path_exists(path):
                            at.default_directory = path
                        else:
                            at.default_directory = g.makeAllNonExistentDirectories(path)
                            if not at.default_directory:
                                at.error("invalid @path: " + path)
                        #@nonl
                        #@-node:ekr.20040929105133.28:<< handle absolute path >>
                        #@nl
                    else:
                        at.error("ignoring bad @path: " + path)
                else:
                    at.error("ignoring empty @path")
                
                #@-node:ekr.20040929105133.26:<< handle @path >> in df.scanDeafaultDirectory in leoAtFile.py
                #@nl
                return
    
        #@    << Set current directory >>
        #@+node:ekr.20040929105133.29:<< Set current directory >>
        # This code is executed if no valid absolute path was specified in the @file node or in an @path directive.
        
        assert(not at.default_directory)
        
        if c.frame :
            base = g.getBaseDirectory() # returns "" on error.
            for theDir in (c.tangle_directory,c.frame.openDirectory,c.openDirectory):
                if theDir and len(theDir) > 0:
                    theDir = g.os_path_join(base,theDir)
                    if g.os_path_isabs(theDir): # Errors may result in relative or invalid path.
                        if g.os_path_exists(theDir):
                            at.default_directory = theDir ; break
                        else:
                            at.default_directory = g.makeAllNonExistentDirectories(theDir)
        #@-node:ekr.20040929105133.29:<< Set current directory >>
        #@nl
        if not at.default_directory and not importing:
            # This should never happen: c.openDirectory should be a good last resort.
            g.trace()
            at.error("No absolute directory specified anywhere.")
            at.default_directory = ""
    #@nonl
    #@-node:ekr.20040929105133.24:scanDefaultDirectory
    #@+node:ekr.20040929105133.294:scanForClonedSibs (reading & writing)
    def scanForClonedSibs (self,v):
        
        """Scan the siblings of vnode v looking for clones of v.
        Return the number of cloned sibs and n where p is the n'th cloned sibling."""
    
        clonedSibs = 0 # The number of cloned siblings of p, including p.
        thisClonedSibIndex = 0 # Position of p in list of cloned siblings.
    
        if v and v.isCloned():
            sib = v
            while sib.back():
                sib = sib.back()
            while sib:
                if sib.t == v.t:
                    clonedSibs += 1
                    if sib == v:
                        thisClonedSibIndex = clonedSibs
                sib = sib.next()
                
        # g.trace(clonedSibs,thisClonedSibIndex)
    
        return clonedSibs,thisClonedSibIndex
    #@nonl
    #@-node:ekr.20040929105133.294:scanForClonedSibs (reading & writing)
    #@+node:ekr.20040929105133.101:sentinelName
    # Returns the name of the sentinel for warnings.
    
    def sentinelName(self, kind):
        
        at = self
    
        sentinelNameDict = {
            at.noSentinel:    "<no sentinel>",
            at.startAt:       "@+at",     at.endAt:     "@-at",
            at.startBody:     "@+body",   at.endBody:   "@-body", # 3.x only.
            at.startDoc:      "@+doc",    at.endDoc:    "@-doc",
            at.startLeo:      "@+leo",    at.endLeo:    "@-leo",
            at.startNode:     "@+node",   at.endNode:   "@-node",
            at.startOthers:   "@+others", at.endOthers: "@-others",
            at.startAll:      "@+all",    at.endAll:    "@-all", # 4.x
            at.startMiddle:   "@+middle", at.endMiddle: "@-middle", # 4.x
            at.startAfterRef: "@afterref", # 4.x
            at.startComment:  "@comment",
            at.startDelims:   "@delims",
            at.startDirective:"@@",
            at.startNl:       "@nl",   # 4.x
            at.startNonl:     "@nonl", # 4.x
            at.startClone:    "@clone", # 4.2
            at.startRef:      "@<<",
            at.startVerbatim: "@verbatim",
            at.startVerbatimAfterRef: "@verbatimAfterRef" } # 3.x only.
    
        return sentinelNameDict.get(kind,"<unknown sentinel!>")
    #@nonl
    #@-node:ekr.20040929105133.101:sentinelName
    #@-node:ekr.20040929105133.103:Uilites...
    #@-others
#@nonl
#@-node:ekr.20041001142542.1:class newAtFile
#@-others

if 1:
    import leoAtFile
    leoAtFile.atFile = newAtFile
    print "New atFile class installed"

    import leoGlobals
    leoGlobals.getScript = getScript
    print "g.getScript installed"
    
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040929104807.2:@thin ___proto_atFile.py
#@-leo