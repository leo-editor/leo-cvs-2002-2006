#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2620:@thin leoAtFile.py 
"""Classes to read and write @file nodes."""

#@@language python
#@@tabwidth -4

#@<< atFile imports >>
#@+node:EKR.20040620100737:<< atFile imports >>
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
#@-node:EKR.20040620100737:<< atFile imports >>
#@nl
#@<< global atFile constants >>
#@+node:ekr.20031218072017.2621:<< global atFile constants >>
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
    "@+others": startOthers, "@-others": endOthers }
#@nonl
#@-node:ekr.20031218072017.2621:<< global atFile constants >>
#@nl

class baseAtFile:
    """The base class for the top-level atFile subcommander."""
    #@    << class baseAtFile methods >>
    #@+node:ekr.20031218072017.2622:<< class baseAtFile methods >>
    #@+others
    #@+node:ekr.20031218072017.2623:atFile.__init__ & initIvars
    def __init__(self,c):
        
        self.c = c
        self.fileCommands = self.c.fileCommands
        
        # Create subcommanders to handler old and new format derived files.
        self.old_df = oldDerivedFile(c)
        self.new_df = newDerivedFile(c)
        
        self.initIvars()
        
    def initIvars(self):
        
        # Set by scanDefaultDirectory.
        self.default_directory = None
        self.errors = 0
    
        # Set by scanHeader when reading. Set by scanAllDirectives...
        self.encoding = g.app.config.default_derived_file_encoding
        self.endSentinelComment = ""
        self.startSentinelComment = ""
    #@nonl
    #@-node:ekr.20031218072017.2623:atFile.__init__ & initIvars
    #@+node:ekr.20031218072017.2624:top_df.error
    def error(self,message):
    
        g.es(message,color="red")
        print message
        self.errors += 1
    #@nonl
    #@-node:ekr.20031218072017.2624:top_df.error
    #@+node:ekr.20031218072017.2625:Reading
    #@+node:ekr.20031218072017.2626: top_df.readAll
    def readAll(self,root,partialFlag=False):
        
        """Scan vnodes, looking for @file nodes to read."""
    
        at = self ; c = at.c
        c.endEditing() # Capture the current headline.
        anyRead = False
        at.initIvars()
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
                if partialFlag:
                    # We are forcing the read.
                    at.read(p)
                else:
                    # if p is an orphan, we don't expect to see a derived file,
                    # and we shall read a derived file if it exists.
                    wasOrphan = p.isOrphan()
                    ok = at.read(p)
                    if wasOrphan and not ok:
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
    #@-node:ekr.20031218072017.2626: top_df.readAll
    #@+node:EKR.20040604155223.1:top_df.parseLeoSentinel
    def parseLeoSentinel (self,s):
        
        at = self
        new_df = False ; valid = True ; n = len(s)
        encoding_tag = "-encoding="
        version_tag = "-ver="
        tag = "@+leo"
        thin_tag = "-thin"
        #@    << set the opening comment delim >>
        #@+node:EKR.20040604155223:<< set the opening comment delim >>
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
        #@-node:EKR.20040604155223:<< set the opening comment delim >>
        #@nl
        #@    << make sure we have @+leo >>
        #@+node:ekr.20031218072017.2635:<< make sure we have @+leo >>
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
        #@-node:ekr.20031218072017.2635:<< make sure we have @+leo >>
        #@nl
        #@    << read optional version param >>
        #@+node:ekr.20031218072017.2636:<< read optional version param >>
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
        #@-node:ekr.20031218072017.2636:<< read optional version param >>
        #@nl
        #@    << read optional thin param >>
        #@+node:EKR.20040503105354:<< read optional thin param >>
        if g.match(s,i,thin_tag):
            i += len(tag)
        #@nonl
        #@-node:EKR.20040503105354:<< read optional thin param >>
        #@nl
        #@    << read optional encoding param >>
        #@+node:ekr.20031218072017.2637:<< read optional encoding param >>
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
        #@-node:ekr.20031218072017.2637:<< read optional encoding param >>
        #@nl
        #@    << set the closing comment delim >>
        #@+node:ekr.20031218072017.2638:<< set the closing comment delim >>
        # The closing comment delim is the trailing non-whitespace.
        i = j = g.skip_ws(s,i)
        while i < n and not g.is_ws(s[i]) and not g.is_nl(s,i):
            i += 1
        end = s[j:i]
        #@nonl
        #@-node:ekr.20031218072017.2638:<< set the closing comment delim >>
        #@nl
        return valid,new_df,start,end
    #@nonl
    #@-node:EKR.20040604155223.1:top_df.parseLeoSentinel
    #@+node:ekr.20031218072017.1812:top_df.read
    # The caller has enclosed this code in beginUpdate/endUpdate.
    
    def read(self,root,importFileName=None,thinFile=False):
        
        """Common read logic for any derived file."""
        
        at = self ; c = at.c
        at.errors = 0
        importing = importFileName is not None
        #@    << set fileName from root and importFileName >>
        #@+node:ekr.20031218072017.1813:<< set fileName from root and importFileName >>
        at.scanDefaultDirectory(root,importing=importing)
        if at.errors: return
        
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
        #@-node:ekr.20031218072017.1813:<< set fileName from root and importFileName >>
        #@nl
        #@    << open file or return False >>
        #@+node:ekr.20031218072017.1814:<< open file or return false >>
        fn = g.os_path_join(at.default_directory,fileName)
        fn = g.os_path_normpath(fn)
        
        try:
            # 11/4/03: open the file in binary mode to allow 0x1a in bodies & headlines.
            theFile = open(fn,'rb')
            if theFile:
                #@        << warn on read-only file >>
                #@+node:ekr.20031218072017.1815:<< warn on read-only file >>
                try:
                    read_only = not os.access(fn,os.W_OK)
                    if read_only:
                        g.es("read only: " + fn,color="red")
                except:
                    pass # os.access() may not exist on all platforms.
                #@nonl
                #@-node:ekr.20031218072017.1815:<< warn on read-only file >>
                #@nl
            else: return False
        except:
            at.error("Can not open: " + '"@file ' + fn + '"')
            root.setDirty()
            return False
        #@nonl
        #@-node:ekr.20031218072017.1814:<< open file or return false >>
        #@nl
        g.es("reading: " + root.headString())
        firstLines,read_new = at.scanHeader(theFile,fileName)
        df = g.choose(read_new,at.new_df,at.old_df)
        # g.trace(g.choose(df==at.new_df,"new","old"))
        #@    << copy ivars to df >>
        #@+node:ekr.20031218072017.1816:<< copy ivars to df >>
        # Telling what kind of file we are reading.
        df.importing = importFileName != None
        df.raw = False
        if importing and df == at.new_df:
            thinFile = True
        df.thinFile = thinFile
        
        # Set by scanHeader.
        df.encoding = at.encoding
        df.endSentinelComment = at.endSentinelComment
        df.startSentinelComment = at.startSentinelComment
        
        # Set other common ivars.
        df.errors = 0
        df.file = theFile
        df.importRootSeen = False
        df.indent = 0
        df.targetFileName = fileName
        df.root = root
        df.root_seen = False
        df.perfectImportRoot = None # Set only in readOpenFile.
        #@nonl
        #@-node:ekr.20031218072017.1816:<< copy ivars to df >>
        #@nl
        root.clearVisitedInTree()
        try:
            # 1/28/04: Don't set comment delims when importing.
            # 1/28/04: Call scanAllDirectives here, not in readOpenFile.
            importing = importFileName is not None
            df.scanAllDirectives(root,importing=importing,reading=True)
            df.readOpenFile(root,theFile,firstLines)
        except:
            at.error("Unexpected exception while reading derived file")
            g.es_exception()
        theFile.close()
        root.clearDirty() # May be set dirty below.
        after = root.nodeAfterTree()
        #@    << warn about non-empty unvisited nodes >>
        #@+node:ekr.20031218072017.1817:<< warn about non-empty unvisited nodes >>
        for p in root.self_and_subtree_iter():
        
            # g.trace(p)
            try: s = p.v.t.tempBodyString
            except: s = ""
            if s and not p.v.t.isVisited():
                at.error("Not in derived file:" + p.headString())
                p.v.t.setVisited() # One message is enough.
        #@nonl
        #@-node:ekr.20031218072017.1817:<< warn about non-empty unvisited nodes >>
        #@nl
        if df.errors == 0:
            if not df.importing:
                #@            << copy all tempBodyStrings to tnodes >>
                #@+node:ekr.20031218072017.1818:<< copy all tempBodyStrings to tnodes >>
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
                #@-node:ekr.20031218072017.1818:<< copy all tempBodyStrings to tnodes >>
                #@nl
        #@    << delete all tempBodyStrings >>
        #@+node:ekr.20031218072017.1819:<< delete all tempBodyStrings >>
        for p in c.allNodes_iter():
            
            if hasattr(p.v.t,"tempBodyString"):
                delattr(p.v.t,"tempBodyString")
        #@nonl
        #@-node:ekr.20031218072017.1819:<< delete all tempBodyStrings >>
        #@nl
        return df.errors == 0
    #@nonl
    #@-node:ekr.20031218072017.1812:top_df.read
    #@+node:ekr.20031218072017.2639:top_df.readLine
    def readLine (self,file):
    
        """Reads one line from file using the present encoding"""
        
        s = g.readlineForceUnixNewline(file)
        u = g.toUnicode(s,self.encoding)
        return u
    #@nonl
    #@-node:ekr.20031218072017.2639:top_df.readLine
    #@+node:ekr.20031218072017.2627:top_df.scanDefaultDirectory
    def scanDefaultDirectory(self,p,importing=False):
        
        """Set default_directory ivar by looking for @path directives."""
    
        at = self ; c = at.c
        at.default_directory = None
        #@    << Set path from @file node >>
        #@+node:ekr.20031218072017.2628:<< Set path from @file node >>  in df.scanDeafaultDirectory in leoAtFile.py
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
        #@-node:ekr.20031218072017.2628:<< Set path from @file node >>  in df.scanDeafaultDirectory in leoAtFile.py
        #@nl
        if at.default_directory:
            return
            
        for p in p.self_and_parents_iter():
            s = p.v.t.bodyString
            theDict = g.get_directives_dict(s)
            if theDict.has_key("path"):
                #@            << handle @path >>
                #@+node:ekr.20031218072017.2629:<< handle @path >> in df.scanDeafaultDirectory in leoAtFile.py
                # We set the current director to a path so future writes will go to that directory.
                
                k = theDict["path"]
                #@<< compute relative path from s[k:] >>
                #@+node:ekr.20031218072017.2630:<< compute relative path from s[k:] >>
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
                #@-node:ekr.20031218072017.2630:<< compute relative path from s[k:] >>
                #@nl
                
                if path and len(path) > 0:
                    base = g.getBaseDirectory() # returns "" on error.
                    path = g.os_path_join(base,path)
                    
                    if g.os_path_isabs(path):
                        #@        << handle absolute path >>
                        #@+node:ekr.20031218072017.2631:<< handle absolute path >>
                        # path is an absolute path.
                        
                        if g.os_path_exists(path):
                            at.default_directory = path
                        else:
                            at.default_directory = g.makeAllNonExistentDirectories(path)
                            if not at.default_directory:
                                at.error("invalid @path: " + path)
                        #@nonl
                        #@-node:ekr.20031218072017.2631:<< handle absolute path >>
                        #@nl
                    else:
                        at.error("ignoring bad @path: " + path)
                else:
                    at.error("ignoring empty @path")
                
                #@-node:ekr.20031218072017.2629:<< handle @path >> in df.scanDeafaultDirectory in leoAtFile.py
                #@nl
                return
    
        #@    << Set current directory >>
        #@+node:ekr.20031218072017.2632:<< Set current directory >>
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
        #@-node:ekr.20031218072017.2632:<< Set current directory >>
        #@nl
        if not at.default_directory and not importing:
            # This should never happen: c.openDirectory should be a good last resort.
            g.trace()
            at.error("No absolute directory specified anywhere.")
            at.default_directory = ""
    #@nonl
    #@-node:ekr.20031218072017.2627:top_df.scanDefaultDirectory
    #@+node:ekr.20031218072017.2633:top_df.scanHeader
    def scanHeader(self,theFile,fileName):
        
        """Scan the @+leo sentinel.
        
        Sets self.encoding, and self.start/endSentinelComment.
        
        Returns (firstLines,new_df) where:
        firstLines contains all @first lines,
        new_df is True if we are reading a new-format derived file."""
        
        at = self
        firstLines = [] # The lines before @+leo.
        tag = "@+leo"
        valid = True ; new_df = False
        #@    << skip any non @+leo lines >>
        #@+node:ekr.20031218072017.2634:<< skip any non @+leo lines >>
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
        #@-node:ekr.20031218072017.2634:<< skip any non @+leo lines >>
        #@nl
        if valid:
            valid,new_df,start,end = at.parseLeoSentinel(s)
        if valid:
            at.startSentinelComment = start
            at.endSentinelComment = end
        else:
            at.error("Bad @+leo sentinel in " + fileName)
        # g.trace("start,end",repr(at.startSentinelComment),repr(at.endSentinelComment))
        return firstLines, new_df
    #@nonl
    #@-node:ekr.20031218072017.2633:top_df.scanHeader
    #@-node:ekr.20031218072017.2625:Reading
    #@+node:ekr.20031218072017.2640:Writing
    #@+node:ekr.20031218072017.2015:top_df.writeAll
    def writeAll(self,writeAtFileNodesFlag=False,writeDirtyAtFileNodesFlag=False,toString=False):
        
        """Write @file nodes in all or part of the outline"""
    
        at = self ; c = at.c
        write_new = not g.app.config.write_old_format_derived_files
        df = g.choose(write_new,at.new_df,at.old_df)
        df.initIvars()
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
        #@+node:ekr.20031218072017.2016:<< Clear all orphan bits >>
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
        #@-node:ekr.20031218072017.2016:<< Clear all orphan bits >>
        #@nl
        while p and p != after:
            if p.isAnyAtFileNode() or p.isAtIgnoreNode():
                #@            << handle v's tree >>
                #@+node:ekr.20031218072017.2017:<< handle v's tree >>
                if p.v.isDirty() or writeAtFileNodesFlag or p.v.t in writtenFiles:
                
                    df.fileChangedFlag = False # 1/9/04
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
                
                    if df.fileChangedFlag and autoSave: # Set by replaceTargetFileIfDifferent.
                        mustAutoSave = True
                #@nonl
                #@-node:ekr.20031218072017.2017:<< handle v's tree >>
                #@nl
                p.moveToNodeAfterTree()
            else:
                p.moveToThreadNext()
    
        #@    << say the command is finished >>
        #@+node:ekr.20031218072017.2018:<< say the command is finished >>
        if writeAtFileNodesFlag or writeDirtyAtFileNodesFlag:
            if len(writtenFiles) > 0:
                g.es("finished")
            elif writeAtFileNodesFlag:
                g.es("no @file nodes in the selected tree")
            else:
                g.es("no dirty @file nodes")
        #@nonl
        #@-node:ekr.20031218072017.2018:<< say the command is finished >>
        #@nl
        return mustAutoSave
    #@nonl
    #@-node:ekr.20031218072017.2015:top_df.writeAll
    #@+node:ekr.20031218072017.2641:top_df.write, norefWrite, asisWrite
    def norefWrite (self,p,toString=False):
        at = self
        write_new = not g.app.config.write_old_format_derived_files
        df = g.choose(write_new,at.new_df,at.old_df)
        try:    df.norefWrite(p,toString=toString)
        except: at.writeException(p)
        
    rawWrite = norefWrite # Compatibility with old scripts.
        
    def asisWrite (self,p,toString=False):
        at = self
        try: at.old_df.asisWrite(p,toString=toString) # No new_df.asisWrite method.
        except: at.writeException(p)
        
    selentWrite = asisWrite # Compatibility with old scripts.
        
    def write (self,p,nosentinels=False,thinFile=False,toString=False,oneNodeOnly=False):
        at = self
        write_new = thinFile or not g.app.config.write_old_format_derived_files
        df = g.choose(write_new,at.new_df,at.old_df)
        try:    df.write(p,nosentinels=nosentinels,thinFile=thinFile,toString=toString,oneNodeOnly=oneNodeOnly)
        except: at.writeException(p)
    #@nonl
    #@-node:ekr.20031218072017.2641:top_df.write, norefWrite, asisWrite
    #@+node:ekr.20031218072017.2642:top_df.writeOld/NewDerivedFiles
    def writeOldDerivedFiles (self,toString=False):
        
        self.writeDerivedFiles(write_old=True,toString=toString)
    
    def writeNewDerivedFiles (self,toString=False):
    
        self.writeDerivedFiles(write_old=False,toString=toString)
        
    def writeDerivedFiles (self,write_old,toString=False):
        
        config = g.app.config
        old = config.write_old_format_derived_files
        config.write_old_format_derived_files = write_old
        self.writeAll(writeAtFileNodesFlag=True,toString=toString)
        config.write_old_format_derived_files = old
    #@nonl
    #@-node:ekr.20031218072017.2642:top_df.writeOld/NewDerivedFiles
    #@+node:ekr.20031218072017.2019:top_df.writeMissing
    def writeMissing(self,p,toString=False):
    
        at = self
    
        write_new = not g.app.config.write_old_format_derived_files
        df = g.choose(write_new,at.new_df,at.old_df)
        df.initIvars()
        writtenFiles = False ; changedFiles = False
    
        p = p.copy()
        after = p.nodeAfterTree()
        while p and p != after: # Don't use iterator.
            if p.isAtAsisFileNode() or (p.isAnyAtFileNode() and not p.isAtIgnoreNode()):
                missing = False ; valid = True
                df.targetFileName = p.anyAtFileNodeName()
                #@            << set missing if the file does not exist >>
                #@+node:ekr.20031218072017.2020:<< set missing if the file does not exist >>
                # This is similar, but not the same as, the logic in openWriteFile.
                
                valid = df.targetFileName and len(df.targetFileName) > 0
                
                if valid:
                    try:
                        # Creates missing directives if option is enabled.
                        df.scanAllDirectives(p)
                        valid = df.errors == 0
                    except:
                        g.es("exception in atFile.scanAllDirectives")
                        g.es_exception()
                        valid = False
                
                if valid:
                    try:
                        fn = df.targetFileName
                        df.shortFileName = fn # name to use in status messages.
                        df.targetFileName = g.os_path_join(df.default_directory,fn)
                        df.targetFileName = g.os_path_normpath(df.targetFileName)
                
                        path = df.targetFileName # Look for the full name, not just the directory.
                        valid = path and len(path) > 0
                        if valid:
                            missing = not g.os_path_exists(path)
                    except:
                        g.es("exception creating path:" + fn)
                        g.es_exception()
                        valid = False
                #@nonl
                #@-node:ekr.20031218072017.2020:<< set missing if the file does not exist >>
                #@nl
                if valid and missing:
                    #@                << create df.outputFile >>
                    #@+node:ekr.20031218072017.2021:<< create df.outputFile >>
                    if toString:
                        df.outputFileName = "<string: %s>" % df.targetFileName
                        df.outputFile = g.fileLikeObject()
                    else:
                        try:
                            df.outputFileName = df.targetFileName
                            df.outputFile = open(df.outputFileName,'wb')
                            if df.outputFile is None:
                                g.es("can not open " + df.outputFileName)
                        except IOError:
                            g.es("Can not open " + df.outputFileName)
                            g.es_exception()
                            df.outputFile = None
                    #@nonl
                    #@-node:ekr.20031218072017.2021:<< create df.outputFile >>
                    #@nl
                    if df.outputFile:
                        #@                    << write the @file node >>
                        #@+node:ekr.20031218072017.2022:<< write the @file node >>
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
                        
                        if df.fileChangedFlag: # Set by replaceTargetFileIfDifferent.
                            changedFiles = True
                        #@nonl
                        #@-node:ekr.20031218072017.2022:<< write the @file node >>
                        #@nl
                        df.closeWriteFile()
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
    #@-node:ekr.20031218072017.2019:top_df.writeMissing
    #@+node:EKR.20040620103353:top_df.writeException
    def writeException(self,p):
    
        self.error("Unexpected exception while writing " + p.headString())
        g.es_exception()
    #@nonl
    #@-node:EKR.20040620103353:top_df.writeException
    #@-node:ekr.20031218072017.2640:Writing
    #@-others
    #@nonl
    #@-node:ekr.20031218072017.2622:<< class baseAtFile methods >>
    #@nl
    
class atFile (baseAtFile):
    pass # May be overridden in plugins.
    
class baseOldDerivedFile:
    """The base class to read and write 3.x derived files."""
    #@    << class baseOldDerivedFile methods >>
    #@+node:ekr.20031218072017.2643:<< class baseOldDerivedFile methods >>
    #@+others
    #@+node:ekr.20031218072017.2644: old_df.__init__& initIvars
    def __init__(self,c):
    
        self.c = c # The commander for the current window.
        self.fileCommands = self.c.fileCommands
    
        self.initIvars()
    
    def initIvars(self):
    
        #@    << init atFile ivars >>
        #@+node:ekr.20031218072017.2645:<< init atFile ivars >>
        # errors is the number of errors seen while reading and writing.
        self.errors = 0
        
        # Initialized by atFile.scanAllDirectives.
        self.default_directory = None
        self.page_width = None
        self.tab_width  = None
        self.startSentinelComment = ""
        self.endSentinelComment = ""
        self.language = None
        
        #@+at 
        #@nonl
        # The files used by the output routines.  When tangling, we first 
        # write to a temporary output file.  After tangling is temporary 
        # file.  Otherwise we delete the old target file and rename the 
        # temporary file to be the target file.
        #@-at
        #@@c
        self.shortFileName = "" # short version of file name used for messages.
        self.targetFileName = u"" # EKR 1/21/03: now a unicode string
        self.outputFileName = u"" # EKR 1/21/03: now a unicode string
        self.outputFile = None # The temporary output file.
        self.toStringFlag = False # True if output eventually gets put in self.stringOutput
        self.stringOutput = None
        
        #@+at 
        #@nonl
        # The indentation used when outputting section references or at-others 
        # sections.  We add the indentation of the line containing the at-node 
        # directive and restore the old value when the
        # expansion is complete.
        #@-at
        #@@c
        self.indent = 0  # The unit of indentation is spaces, not tabs.
        
        # The root of tree being written.
        self.root = None
        
        # Ivars used to suppress newlines between sentinels.
        self.suppress_newlines = True # True: enable suppression of newlines.
        self.newline_pending = False # True: newline is pending on read or write.
        
        # Support of output_newline option
        self.output_newline = g.getOutputNewline()
        
        # Support of @raw
        self.raw = False # True: in @raw mode
        self.sentinels = True # True: output sentinels while expanding refs.
        
        # The encoding used to convert from unicode to a byte stream.
        self.encoding = g.app.config.default_derived_file_encoding
        
        # For interface between 3.x and 4.x read code.
        self.file = None
        self.importing = False
        self.importRootSeen = False
        
        # Set when a file has actually been updated.
        self.fileChangedFlag = False
        #@nonl
        #@-node:ekr.20031218072017.2645:<< init atFile ivars >>
        #@nl
    #@-node:ekr.20031218072017.2644: old_df.__init__& initIvars
    #@+node:ekr.20031218072017.2646:Reading (3.x)
    #@+node:ekr.20031218072017.1811:createImportedNode
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
    #@-node:ekr.20031218072017.1811:createImportedNode
    #@+node:ekr.20031218072017.2647:old_df.readOpenFile
    def readOpenFile(self,root,theFile,firstLines):
        
        """Read an open 3.x derived file."""
        
        at = self
    
        # Scan the file buffer
        lastLines = at.scanText(theFile,root,[],endLeo)
        root.v.t.setVisited() # Disable warning about set nodes.
    
        # Handle first and last lines.
        try: body = root.v.t.tempBodyString
        except: body = ""
        lines = body.split('\n')
        at.completeFirstDirectives(lines,firstLines)
        at.completeLastDirectives(lines,lastLines)
        s = '\n'.join(lines).replace('\r', '')
        root.v.t.tempBodyString = s
    #@nonl
    #@-node:ekr.20031218072017.2647:old_df.readOpenFile
    #@+node:ekr.20031218072017.2648:completeFirstDirectives
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
    #@-node:ekr.20031218072017.2648:completeFirstDirectives
    #@+node:ekr.20031218072017.2649:completeLastDirectives
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
    #@-node:ekr.20031218072017.2649:completeLastDirectives
    #@+node:ekr.20031218072017.2650:createNthChild 3.x
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
    def createNthChild(self,n,parent,headline):
        
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
            #@+node:ekr.20031218072017.2651:<< check the headlines >>
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
            #@-node:ekr.20031218072017.2651:<< check the headlines >>
            #@nl
        else:
            # This is using a dummy; we should already have bumped errors.
            result = parent.insertAsLastChild(leoNodes.tnode())
        result.initHeadString(headline)
        
        result.setVisited() # Suppress all other errors for this node.
        result.t.setVisited() # Suppress warnings about unvisited nodes.
        return result
    #@nonl
    #@-node:ekr.20031218072017.2650:createNthChild 3.x
    #@+node:ekr.20031218072017.2652:handleLinesFollowingSentinel
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
            #@+node:ekr.20031218072017.2653:<< remove the comment delims from s >>
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
            #@-node:ekr.20031218072017.2653:<< remove the comment delims from s >>
            #@nl
            
        # Undo the cweb hack: undouble @ signs if the opening comment delim ends in '@'.
        if start[-1:] == '@':
            s = s.replace('@@','@')
    
        return s
    #@nonl
    #@-node:ekr.20031218072017.2652:handleLinesFollowingSentinel
    #@+node:ekr.20031218072017.2654:readLine
    def readLine (self,theFile):
        """Reads one line from file using the present encoding"""
        
        s = g.readlineForceUnixNewline(theFile)
        u = g.toUnicode(s,self.encoding)
        return u
    
    #@-node:ekr.20031218072017.2654:readLine
    #@+node:ekr.20031218072017.2655:readLinesToNextSentinel
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
                # 5/1/03: looser test then calling sentinelKind.
                s = nextLine ; i = g.skip_ws(s,0)
                if g.match(s,i,start):
                    lines.append(nextLine)
                    nextLine = self.readLine(theFile)
                else: break
    
        return nextLine,lines
    #@nonl
    #@-node:ekr.20031218072017.2655:readLinesToNextSentinel
    #@+node:ekr.20031218072017.2656:scanDoc
    # Scans the doc part and appends the text out.
    # s,i point to the present line on entry.
    
    def scanDoc(self,theFile,s,i,out,kind):
    
        endKind = g.choose(kind ==startDoc,endDoc,endAt)
        single = len(self.endSentinelComment) == 0
        #@    << Skip the opening sentinel >>
        #@+node:ekr.20031218072017.2657:<< Skip the opening sentinel >>
        assert(g.match(s,i,g.choose(kind == startDoc, "+doc", "+at")))
        
        out.append(g.choose(kind == startDoc, "@doc", "@"))
        s = self.readLine(theFile)
        #@-node:ekr.20031218072017.2657:<< Skip the opening sentinel >>
        #@nl
        #@    << Skip an opening block delim >>
        #@+node:ekr.20031218072017.2658:<< Skip an opening block delim >>
        if not single:
            j = g.skip_ws(s,0)
            if g.match(s,j,self.startSentinelComment):
                s = self.readLine(theFile)
        #@nonl
        #@-node:ekr.20031218072017.2658:<< Skip an opening block delim >>
        #@nl
        nextLine = None ; kind = noSentinel
        while len(s) > 0:
            #@        << set kind, nextLine >>
            #@+node:ekr.20031218072017.2659:<< set kind, nextLine >>
            #@+at 
            #@nonl
            # For non-sentinel lines we look ahead to see whether the next 
            # line is a sentinel.
            #@-at
            #@@c
            
            assert(nextLine==None)
            
            kind = self.sentinelKind(s)
            
            if kind == noSentinel:
                j = g.skip_ws(s,0)
                blankLine = s[j] == '\n'
                nextLine = self.readLine(theFile)
                nextKind = self.sentinelKind(nextLine)
                if blankLine and nextKind == endKind:
                    kind = endKind # stop the scan now
            #@-node:ekr.20031218072017.2659:<< set kind, nextLine >>
            #@nl
            if kind == endKind: break
            #@        << Skip the leading stuff >>
            #@+node:ekr.20031218072017.2660:<< Skip the leading stuff >>
            # Point i to the start of the real line.
            
            if single: # Skip the opening comment delim and a blank.
                i = g.skip_ws(s,0)
                if g.match(s,i,self.startSentinelComment):
                    i += len(self.startSentinelComment)
                    if g.match(s,i," "): i += 1
            else:
                i = self.skipIndent(s,0, self.indent)
            #@-node:ekr.20031218072017.2660:<< Skip the leading stuff >>
            #@nl
            #@        << Append s to out >>
            #@+node:ekr.20031218072017.2661:<< Append s to out >>
            # Append the line with a newline if it is real
            
            line = s[i:-1] # remove newline for rstrip.
            
            if line == line.rstrip():
                # no trailing whitespace: the newline is real.
                out.append(line + '\n')
            else:
                # trailing whitespace: the newline is not real.
                out.append(line)
            #@-node:ekr.20031218072017.2661:<< Append s to out >>
            #@nl
            if nextLine:
                s = nextLine ; nextLine = None
            else: s = self.readLine(theFile)
        if kind != endKind:
            self.readError("Missing " + self.sentinelName(endKind) + " sentinel")
        #@    << Remove a closing block delim from out >>
        #@+node:ekr.20031218072017.2662:<< Remove a closing block delim from out >>
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
        #@-node:ekr.20031218072017.2662:<< Remove a closing block delim from out >>
        #@nl
    #@nonl
    #@-node:ekr.20031218072017.2656:scanDoc
    #@+node:ekr.20031218072017.2663:scanText (3.x)
    def scanText (self,theFile,p,out,endSentinelKind,nextLine=None):
        
        """Scan a 3.x derived file recursively."""
    
        at = self # 12/18/03
        lastLines = [] # The lines after @-leo
        lineIndent = 0 ; linep = 0 # Changed only for sentinels.
        while 1:
            #@        << put the next line into s >>
            #@+node:ekr.20031218072017.2664:<< put the next line into s >>
            if nextLine:
                s = nextLine ; nextLine = None
            else:
                s = self.readLine(theFile)
                if len(s) == 0: break
            #@nonl
            #@-node:ekr.20031218072017.2664:<< put the next line into s >>
            #@nl
            #@        << set kind, nextKind >>
            #@+node:ekr.20031218072017.2665:<< set kind, nextKind >>
            #@+at 
            #@nonl
            # For non-sentinel lines we look ahead to see whether the next 
            # line is a sentinel.  If so, the newline that ends a non-sentinel 
            # line belongs to the next sentinel.
            #@-at
            #@@c
            
            assert(nextLine==None)
            
            kind = self.sentinelKind(s)
            
            if kind == noSentinel:
                nextLine = self.readLine(theFile)
                nextKind = self.sentinelKind(nextLine)
            else:
                nextLine = nextKind = None
            
            # nextLine != None only if we have a non-sentinel line.
            # Therefore, nextLine == None whenever scanText returns.
            #@nonl
            #@-node:ekr.20031218072017.2665:<< set kind, nextKind >>
            #@nl
            if kind != noSentinel:
                #@            << set lineIndent, linep and leading_ws >>
                #@+node:ekr.20031218072017.2666:<< Set lineIndent, linep and leading_ws >>
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
                #@-node:ekr.20031218072017.2666:<< Set lineIndent, linep and leading_ws >>
                #@nl
                i = self.skipSentinelStart(s,0)
            #@        << handle the line in s >>
            #@+node:ekr.20031218072017.2668:<< handle the line in s >>
            if kind == noSentinel:
                #@    << append non-sentinel line >>
                #@+node:ekr.20031218072017.2669:<< append non-sentinel line >>
                # We don't output the trailing newline if the next line is a sentinel.
                if self.raw: # 10/15/02
                    i = 0
                else:
                    i = self.skipIndent(s,0,self.indent)
                
                assert(nextLine != None)
                
                if nextKind == noSentinel:
                    line = s[i:]
                    out.append(line)
                else:
                    line = s[i:-1] # don't output the newline
                    out.append(line)
                #@-node:ekr.20031218072017.2669:<< append non-sentinel line >>
                #@nl
            #@<< handle common sentinels >>
            #@+node:ekr.20031218072017.2670:<< handle common sentinels >>
            elif kind in (endAt, endBody,endDoc,endLeo,endNode,endOthers):
                    #@        << handle an ending sentinel >>
                    #@+node:ekr.20031218072017.2671:<< handle an ending sentinel >>
                    # g.trace("end sentinel:", self.sentinelName(kind))
                    
                    if kind == endSentinelKind:
                        if kind == endLeo:
                            # Ignore everything after @-leo.
                            # Such lines were presumably written by @last.
                            while 1:
                                s = self.readLine(theFile)
                                if len(s) == 0: break
                                lastLines.append(s) # Capture all trailing lines, even if empty.
                        elif kind == endBody:
                            self.raw = False
                        # nextLine != None only if we have a non-sentinel line.
                        # Therefore, nextLine == None whenever scanText returns.
                        assert(nextLine==None)
                        return lastLines # End the call to scanText.
                    else:
                        # Tell of the structure error.
                        name = self.sentinelName(kind)
                        expect = self.sentinelName(endSentinelKind)
                        self.readError("Ignoring " + name + " sentinel.  Expecting " + expect)
                    #@nonl
                    #@-node:ekr.20031218072017.2671:<< handle an ending sentinel >>
                    #@nl
            elif kind == startBody:
                #@    << scan @+body >>
                #@+node:ekr.20031218072017.2674:<< scan @+body >> 3.x
                assert(g.match(s,i,"+body"))
                
                child_out = [] ; child = p.copy() # Do not change out or p!
                oldIndent = self.indent ; self.indent = lineIndent
                self.scanText(theFile,child,child_out,endBody)
                
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
                #@-node:ekr.20031218072017.2674:<< scan @+body >> 3.x
                #@nl
            elif kind == startNode:
                #@    << scan @+node >>
                #@+node:ekr.20031218072017.2676:<< scan @+node >>
                assert(g.match(s,i,"+node:"))
                i += 6
                
                childIndex = 0 ; cloneIndex = 0
                #@<< Set childIndex >>
                #@+node:ekr.20031218072017.2677:<< Set childIndex >>
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
                #@-node:ekr.20031218072017.2677:<< Set childIndex >>
                #@nl
                #@<< Set cloneIndex >>
                #@+node:ekr.20031218072017.2678:<< Set cloneIndex >>
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
                #@-node:ekr.20031218072017.2678:<< Set cloneIndex >>
                #@nl
                headline = ""
                #@<< Set headline and ref >>
                #@+node:ekr.20031218072017.2679:<< Set headline and ref >>
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
                #@-node:ekr.20031218072017.2679:<< Set headline and ref >>
                #@nl
                
                # print childIndex,headline
                
                if childIndex == 0: # The root node.
                    if not at.importing:
                        #@        << Check the filename in the sentinel >>
                        #@+node:ekr.20031218072017.2680:<< Check the filename in the sentinel >>
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
                        #@-node:ekr.20031218072017.2680:<< Check the filename in the sentinel >>
                        #@nl
                    # Put the text of the root node in the current node.
                    self.scanText(theFile,p,out,endNode)
                    p.v.t.setCloneIndex(cloneIndex)
                    # if cloneIndex > 0: g.trace("clone index:",cloneIndex,p)
                else:
                    # NB: this call to createNthChild is the bottleneck!
                    child = self.createNthChild(childIndex,p,headline)
                    child.t.setCloneIndex(cloneIndex)
                    # if cloneIndex > 0: g.trace("cloneIndex,child:"cloneIndex,child)
                    self.scanText(theFile,child,out,endNode)
                
                #@<< look for sentinels that may follow a reference >>
                #@+node:ekr.20031218072017.2681:<< look for sentinels that may follow a reference >>
                s = self.readLine(theFile)
                kind = self.sentinelKind(s)
                
                if len(s) > 1 and kind == startVerbatimAfterRef:
                    s = self.readLine(theFile)
                    # g.trace("verbatim:",repr(s))
                    out.append(s)
                elif len(s) > 1 and self.sentinelKind(s) == noSentinel:
                    out.append(s)
                else:
                    nextLine = s # Handle the sentinel or blank line later.
                
                #@-node:ekr.20031218072017.2681:<< look for sentinels that may follow a reference >>
                #@nl
                #@nonl
                #@-node:ekr.20031218072017.2676:<< scan @+node >>
                #@nl
            elif kind == startRef:
                #@    << scan old ref >>
                #@+node:ekr.20031218072017.2672:<< scan old ref >> (3.0)
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
                #@-node:ekr.20031218072017.2672:<< scan old ref >> (3.0)
                #@nl
            elif kind == startAt:
                #@    << scan @+at >>
                #@+node:ekr.20031218072017.2673:<< scan @+at >>
                assert(g.match(s,i,"+at"))
                self.scanDoc(theFile,s,i,out,kind)
                #@nonl
                #@-node:ekr.20031218072017.2673:<< scan @+at >>
                #@nl
            elif kind == startDoc:
                #@    << scan @+doc >>
                #@+node:ekr.20031218072017.2675:<< scan @+doc >>
                assert(g.match(s,i,"+doc"))
                self.scanDoc(theFile,s,i,out,kind)
                #@nonl
                #@-node:ekr.20031218072017.2675:<< scan @+doc >>
                #@nl
            elif kind == startOthers:
                #@    << scan @+others >>
                #@+node:ekr.20031218072017.2682:<< scan @+others >>
                assert(g.match(s,i,"+others"))
                
                # Make sure that the generated at-others is properly indented.
                out.append(leading_ws + "@others")
                
                self.scanText(theFile,p,out,endOthers)
                #@nonl
                #@-node:ekr.20031218072017.2682:<< scan @+others >>
                #@nl
            #@nonl
            #@-node:ekr.20031218072017.2670:<< handle common sentinels >>
            #@nl
            #@<< handle rare sentinels >>
            #@+node:ekr.20031218072017.2683:<< handle rare sentinels >>
            elif kind == startComment:
                #@    << scan @comment >>
                #@+node:ekr.20031218072017.2686:<< scan @comment >>
                assert(g.match(s,i,"comment"))
                
                # We need do nothing more to ignore the comment line!
                #@-node:ekr.20031218072017.2686:<< scan @comment >>
                #@nl
            elif kind == startDelims:
                #@    << scan @delims >>
                #@+node:ekr.20031218072017.2687:<< scan @delims >>
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
                #@-node:ekr.20031218072017.2687:<< scan @delims >>
                #@nl
            elif kind == startDirective:
                #@    << scan @@ >>
                #@+node:ekr.20031218072017.2685:<< scan @@ >>
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
                #@-node:ekr.20031218072017.2685:<< scan @@ >>
                #@nl
            elif kind == startLeo:
                #@    << scan @+leo >>
                #@+node:ekr.20031218072017.2684:<< scan @+leo >>
                assert(g.match(s,i,"+leo"))
                self.readError("Ignoring unexpected @+leo sentinel")
                #@nonl
                #@-node:ekr.20031218072017.2684:<< scan @+leo >>
                #@nl
            elif kind == startVerbatim:
                #@    << scan @verbatim >>
                #@+node:ekr.20031218072017.2688:<< scan @verbatim >>
                assert(g.match(s,i,"verbatim"))
                
                # Skip the sentinel.
                s = self.readLine(theFile) 
                
                # Append the next line to the text.
                i = self.skipIndent(s,0,self.indent)
                out.append(s[i:])
                #@-node:ekr.20031218072017.2688:<< scan @verbatim >>
                #@nl
            #@nonl
            #@-node:ekr.20031218072017.2683:<< handle rare sentinels >>
            #@nl
            else:
                #@    << warn about unknown sentinel >>
                #@+node:ekr.20031218072017.2689:<< warn about unknown sentinel >>
                j = i
                i = g.skip_line(s,i)
                line = s[j:i]
                self.readError("Unknown sentinel: " + line)
                #@nonl
                #@-node:ekr.20031218072017.2689:<< warn about unknown sentinel >>
                #@nl
            #@nonl
            #@-node:ekr.20031218072017.2668:<< handle the line in s >>
            #@nl
        #@    << handle unexpected end of text >>
        #@+node:ekr.20031218072017.2667:<< handle unexpected end of text >>
        # Issue the error.
        name = self.sentinelName(endSentinelKind)
        self.readError("Unexpected end of file. Expecting " + name + "sentinel" )
        #@-node:ekr.20031218072017.2667:<< handle unexpected end of text >>
        #@nl
        assert(len(s)==0 and nextLine==None) # We get here only if readline fails.
        return lastLines # We get here only if there are problems.
    #@nonl
    #@-node:ekr.20031218072017.2663:scanText (3.x)
    #@-node:ekr.20031218072017.2646:Reading (3.x)
    #@+node:ekr.20031218072017.2690:Sentinels (3.x)
    #@+node:ekr.20031218072017.2691:nodeSentinelText 3.x
    # 4/5/03: config.write_clone_indices no longer used.
    
    def nodeSentinelText(self,p):
        
        if p == self.root or not p.hasParent():
            index = 0
        else:
            index = p.childIndex() + 1
    
        h = p.headString()
        #@    << remove comment delims from h if necessary >>
        #@+node:ekr.20031218072017.2692:<< remove comment delims from h if necessary >>
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
        
        start = self.startSentinelComment
        end = self.endSentinelComment
        
        if end and len(end) > 0:
            h = h.replace(start,"")
            h = h.replace(end,"")
        #@nonl
        #@-node:ekr.20031218072017.2692:<< remove comment delims from h if necessary >>
        #@nl
    
        return str(index) + '::' + h
    #@nonl
    #@-node:ekr.20031218072017.2691:nodeSentinelText 3.x
    #@+node:ekr.20031218072017.2693:putCloseNodeSentinel 3.x
    def putCloseNodeSentinel(self,p):
    
        s = self.nodeSentinelText(p)
        self.putSentinel("@-node:" + s)
    #@nonl
    #@-node:ekr.20031218072017.2693:putCloseNodeSentinel 3.x
    #@+node:ekr.20031218072017.2694:putCloseSentinels
    # root is an ancestor of p, or root == p.
    
    def putCloseSentinels(self,root,p):
        
        """call putCloseSentinel for position p up to, but not including, root."""
    
        self.putCloseNodeSentinel(p)
        assert(p.hasParent())
    
        for p in p.parents_iter():
            if p == root: break
            self.putCloseNodeSentinel(p)
    #@nonl
    #@-node:ekr.20031218072017.2694:putCloseSentinels
    #@+node:ekr.20031218072017.2695:putOpenLeoSentinel 3.x
    # This method is the same as putSentinel except we don't put an opening newline and leading whitespace.
    
    def putOpenLeoSentinel(self,s):
        
        """Put a +leo sentinel containing s."""
        
        if not self.sentinels:
            return # Handle @nosentinelsfile.
    
        self.os(self.startSentinelComment)
        self.os(s)
        encoding = self.encoding.lower()
        if encoding != "utf-8":
            self.os("-encoding=")
            self.os(encoding)
            # New in 4.2: encoding fields end in ",."
            # However, there is no point in changing things here.
            # We want to be as compatible as possible with the old versions of Leo.
            self.os(".")
        self.os(self.endSentinelComment)
        if self.suppress_newlines: # 9/27/02
            self.newline_pending = True # Schedule a newline.
        else:
            self.onl() # End of sentinel.
    #@-node:ekr.20031218072017.2695:putOpenLeoSentinel 3.x
    #@+node:ekr.20031218072017.2696:putOpenNodeSentinel
    def putOpenNodeSentinel(self,p):
    
        """Put an open node sentinel for node p."""
    
        if p.isAtFileNode() and p != self.root:
            self.writeError("@file not valid in: " + p.headString())
            return
        
        s = self.nodeSentinelText(p)
        self.putSentinel("@+node:" + s)
    #@nonl
    #@-node:ekr.20031218072017.2696:putOpenNodeSentinel
    #@+node:ekr.20031218072017.2697:putOpenSentinels 3.x
    # root is an ancestor of p, or root == p.
    
    def putOpenSentinels(self,root,p):
    
        """Call putOpenNodeSentinel on all the descendents of root which are the ancestors of p."""
    
        last = root
        while last != p:
            # Set node to p or the ancestor of p that is a child of last.
            node = p.copy()
            while node and node.parent() != last:
                node.moveToParent()
            assert(node)
            self.putOpenNodeSentinel(node)
            last = node
    #@nonl
    #@-node:ekr.20031218072017.2697:putOpenSentinels 3.x
    #@+node:ekr.20031218072017.2698:putSentinel (applies cweb hack)
    #@+at 
    #@nonl
    # All sentinels are eventually output by this method.
    # 
    # Sentinels include both the preceding and following newlines. This rule 
    # greatly simplies the code and has several important benefits:
    # 
    # 1. Callers never have to generate newlines before or after sentinels.  
    # Similarly, routines that expand code and doc parts never have to add 
    # "extra" newlines.
    # 2. There is no need for a "no-newline" directive.  If text follows a 
    # section reference, it will appear just after the newline that ends 
    # sentinel at the end of the expansion of the reference.  If no 
    # significant text follows a reference, there will be two newlines 
    # following the ending sentinel.
    # 
    # The only exception is that no newline is required before the opening 
    # "leo" sentinel. The putLeoSentinel and isLeoSentinel routines handle 
    # this minor exception.
    #@-at
    #@@c
    def putSentinel(self,s):
        
        """Put a sentinel containing s."""
        
        if not self.sentinels:
            return # Handle @nosentinelsfile.
    
        self.newline_pending = False # discard any pending newline.
        self.onl() ; self.putIndent(self.indent) # Start of sentinel.
        self.os(self.startSentinelComment)
    
        # 11/1/02: The cweb hack: if the opening comment delim ends in '@',
        # double all '@' signs except the first, which is "doubled" by the
        # trailing '@' in the opening comment delimiter.
        start = self.startSentinelComment
        if start and len(start) > 0 and start[-1] == '@':
            assert(s and len(s)>0 and s[0]=='@')
            s = s.replace('@','@@')[1:]
    
        self.os(s)
        self.os(self.endSentinelComment)
        if self.suppress_newlines:
            self.newline_pending = True # Schedule a newline.
        else:
            self.onl() # End of sentinel.
    #@nonl
    #@-node:ekr.20031218072017.2698:putSentinel (applies cweb hack)
    #@+node:ekr.20031218072017.2699:sentinelKind
    def sentinelKind(self,s):
    
        """This method tells what kind of sentinel appears in line s.
        
        Typically s will be an empty line before the actual sentinel,
        but it is also valid for s to be an actual sentinel line.
        
        Returns (kind, s, emptyFlag), where emptyFlag is True if
        kind == noSentinel and s was an empty line on entry."""
    
        i = g.skip_ws(s,0)
        if g.match(s,i,self.startSentinelComment):
            i += len(self.startSentinelComment)
        else:
            return noSentinel
    
        # 10/30/02: locally undo cweb hack here
        start = self.startSentinelComment
        if start and len(start) > 0 and start[-1] == '@':
            s = s[:i] + string.replace(s[i:],'@@','@')
    
        # Do not skip whitespace here!
        if g.match(s,i,"@<<"): return startRef
        if g.match(s,i,"@@"):   return startDirective
        if not g.match(s,i,'@'): return noSentinel
        j = i # start of lookup
        i += 1 # skip the at sign.
        if g.match(s,i,'+') or g.match(s,i,'-'):
            i += 1
        i = g.skip_c_id(s,i)
        key = s[j:i]
        if len(key) > 0 and sentinelDict.has_key(key):
            # g.trace("found:",key)
            return sentinelDict[key]
        else:
            # g.trace("not found:",key)
            return noSentinel
    #@nonl
    #@-node:ekr.20031218072017.2699:sentinelKind
    #@+node:ekr.20031218072017.2700:sentinelName
    # Returns the name of the sentinel for warnings.
    
    def sentinelName(self, kind):
    
        sentinelNameDict = {
            noSentinel:  "<no sentinel>",
            startAt:     "@+at",     endAt:     "@-at",
            startBody:   "@+body",   endBody:   "@-body", # 3.x only.
            startDoc:    "@+doc",    endDoc:    "@-doc",
            startLeo:    "@+leo",    endLeo:    "@-leo",
            startNode:   "@+node",   endNode:   "@-node",
            startOthers: "@+others", endOthers: "@-others",
            startAfterRef:  "@afterref", # 4.x
            startComment:   "@comment",
            startDelims:    "@delims",
            startDirective: "@@",
            startNl:        "@nl",   # 4.x
            startNonl:      "@nonl", # 4.x
            startRef:       "@<<",
            startVerbatim:  "@verbatim",
            startVerbatimAfterRef: "@verbatimAfterRef" } # 3.x only.
    
        return sentinelNameDict.get(kind,"<unknown sentinel!>")
    #@nonl
    #@-node:ekr.20031218072017.2700:sentinelName
    #@+node:ekr.20031218072017.2701:skipSentinelStart
    def skipSentinelStart(self,s,i):
    
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
    #@-node:ekr.20031218072017.2701:skipSentinelStart
    #@-node:ekr.20031218072017.2690:Sentinels (3.x)
    #@+node:ekr.20031218072017.2702:Utilites (3.x)
    #@+node:ekr.20031218072017.2703:directiveKind
    # Returns the kind of at-directive or noDirective.
    
    def directiveKind(self,s,i):
    
        n = len(s)
        if i >= n or s[i] != '@':
            return noDirective
    
        table = (
            ("@all",allDirective),
            ("@c",cDirective),
            ("@code",codeDirective),
            ("@doc",docDirective),
            ("@end_raw",endRawDirective),
            ("@others",othersDirective),
            ("@raw",rawDirective))
    
        # This code rarely gets executed, so simple code suffices.
        if i+1 >= n or g.match(s,i,"@ ") or g.match(s,i,"@\t") or g.match(s,i,"@\n"):
            # 10/25/02: @space is not recognized in cweb mode.
            # 11/15/02: Noweb doc parts are _never_ scanned in cweb mode.
            return g.choose(self.language=="cweb",
                noDirective,atDirective)
    
        # 10/28/02: @c and @(nonalpha) are not recognized in cweb mode.
        # We treat @(nonalpha) separately because @ is in the colorizer table.
        if self.language=="cweb" and (
            g.match_word(s,i,"@c") or
            i+1>= n or s[i+1] not in string.ascii_letters):
            return noDirective
    
        for name,directive in table:
            if g.match_word(s,i,name):
                return directive
        # 10/14/02: return miscDirective only for real directives.
        for name in leoColor.leoKeywords:
            if g.match_word(s,i,name):
                return miscDirective
    
        return noDirective
    #@nonl
    #@-node:ekr.20031218072017.2703:directiveKind
    #@+node:ekr.20031218072017.2704:error
    def error(self,message):
    
        g.es_error(message)
        self.errors += 1
    #@-node:ekr.20031218072017.2704:error
    #@+node:ekr.20031218072017.2705:readError
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
    #@-node:ekr.20031218072017.2705:readError
    #@+node:ekr.20031218072017.2387:old_df.scanAllDirectives
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
        #@+node:ekr.20031218072017.2388:<< Set ivars >>
        self.page_width = self.c.page_width
        self.tab_width  = self.c.tab_width
        
        self.default_directory = None # 8/2: will be set later.
        
        delim1, delim2, delim3 = g.set_delims_from_language(c.target_language)
        self.language = c.target_language
        
        self.encoding = g.app.config.default_derived_file_encoding
        self.output_newline = g.getOutputNewline() # 4/24/03: initialize from config settings.
        #@nonl
        #@-node:ekr.20031218072017.2388:<< Set ivars >>
        #@nl
        #@    << Set path from @file node >>
        #@+node:ekr.20031218072017.2389:<< Set path from @file node >> in scanDirectory in leoGlobals.py
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
        #@-node:ekr.20031218072017.2389:<< Set path from @file node >> in scanDirectory in leoGlobals.py
        #@nl
        old = {}
        for p in p.self_and_parents_iter():
            s = p.v.t.bodyString
            theDict = g.get_directives_dict(s)
            #@        << Test for @path >>
            #@+node:ekr.20031218072017.2394:<< Test for @path >>
            # We set the current director to a path so future writes will go to that directory.
            
            if not self.default_directory and not old.has_key("path") and theDict.has_key("path"):
            
                k = theDict["path"]
                #@    << compute relative path from s[k:] >>
                #@+node:ekr.20031218072017.2395:<< compute relative path from s[k:] >>
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
                #@-node:ekr.20031218072017.2395:<< compute relative path from s[k:] >>
                #@nl
                if path and len(path) > 0:
                    base = g.getBaseDirectory() # returns "" on error.
                    path = g.os_path_join(base,path)
                    if g.os_path_isabs(path):
                        #@            << handle absolute path >>
                        #@+node:ekr.20031218072017.2396:<< handle absolute path >>
                        # path is an absolute path.
                        
                        if g.os_path_exists(path):
                            self.default_directory = path
                        else: # 9/25/02
                            self.default_directory = g.makeAllNonExistentDirectories(path)
                            if not self.default_directory:
                                self.error("invalid @path: " + path)
                        #@-node:ekr.20031218072017.2396:<< handle absolute path >>
                        #@nl
                    else:
                        self.error("ignoring bad @path: " + path)
                else:
                    self.error("ignoring empty @path")
            #@nonl
            #@-node:ekr.20031218072017.2394:<< Test for @path >>
            #@nl
            #@        << Test for @encoding >>
            #@+node:ekr.20031218072017.2391:<< Test for @encoding >>
            if not old.has_key("encoding") and theDict.has_key("encoding"):
                
                e = g.scanAtEncodingDirective(s,theDict)
                if e:
                    self.encoding = e
            #@nonl
            #@-node:ekr.20031218072017.2391:<< Test for @encoding >>
            #@nl
            #@        << Test for @comment and @language >>
            #@+node:ekr.20031218072017.2390:<< Test for @comment and @language >>
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
            #@-node:ekr.20031218072017.2390:<< Test for @comment and @language >>
            #@nl
            #@        << Test for @header and @noheader >>
            #@+node:ekr.20031218072017.2392:<< Test for @header and @noheader >>
            # EKR: 10/10/02: perform the sames checks done by tangle.scanAllDirectives.
            if theDict.has_key("header") and theDict.has_key("noheader"):
                g.es("conflicting @header and @noheader directives")
            #@nonl
            #@-node:ekr.20031218072017.2392:<< Test for @header and @noheader >>
            #@nl
            #@        << Test for @lineending >>
            #@+node:ekr.20031218072017.2393:<< Test for @lineending >>
            if not old.has_key("lineending") and theDict.has_key("lineending"):
                
                lineending = g.scanAtLineendingDirective(s,theDict)
                if lineending:
                    self.output_newline = lineending
            #@-node:ekr.20031218072017.2393:<< Test for @lineending >>
            #@nl
            #@        << Test for @pagewidth >>
            #@+node:ekr.20031218072017.2397:<< Test for @pagewidth >>
            if theDict.has_key("pagewidth") and not old.has_key("pagewidth"):
                
                w = g.scanAtPagewidthDirective(s,theDict,issue_error_flag=True)
                if w and w > 0:
                    self.page_width = w
            #@nonl
            #@-node:ekr.20031218072017.2397:<< Test for @pagewidth >>
            #@nl
            #@        << Test for @tabwidth >>
            #@+node:ekr.20031218072017.2398:<< Test for @tabwidth >>
            if theDict.has_key("tabwidth") and not old.has_key("tabwidth"):
                
                w = g.scanAtTabwidthDirective(s,theDict,issue_error_flag=True)
                if w and w != 0:
                    self.tab_width = w
            
            #@-node:ekr.20031218072017.2398:<< Test for @tabwidth >>
            #@nl
            old.update(theDict)
        #@    << Set current directory >>
        #@+node:ekr.20031218072017.2399:<< Set current directory >>
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
        #@-node:ekr.20031218072017.2399:<< Set current directory >>
        #@nl
        if not importing and not reading:
            # 5/19/04: don't override comment delims when reading!
            #@        << Set comment strings from delims >>
            #@+node:ekr.20031218072017.2400:<< Set comment strings from delims >>
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
            #@-node:ekr.20031218072017.2400:<< Set comment strings from delims >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.2387:old_df.scanAllDirectives
    #@+node:ekr.20031218072017.2706:skipIndent
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
    #@-node:ekr.20031218072017.2706:skipIndent
    #@+node:ekr.20031218072017.2707:writeError
    def writeError(self,message):
    
        if self.errors == 0:
            g.es_error("errors writing: " + self.targetFileName)
    
        self.error(message)
        self.root.setOrphan()
        self.root.setDirty()
    #@nonl
    #@-node:ekr.20031218072017.2707:writeError
    #@-node:ekr.20031218072017.2702:Utilites (3.x)
    #@+node:ekr.20031218072017.2708:Writing (3.x) (Deprecated)
    #@+node:ekr.20031218072017.2709:Top level
    #@+node:ekr.20031218072017.2714:old_df.asisWrite
    def asisWrite(self,root,toString=False):
    
        c = self.c ; self.root = root
        self.errors = 0
        c.endEditing() # Capture the current headline.
        try:
            self.targetFileName = root.atAsisFileNodeName()
            ok = self.openWriteFile(root,toString)
            if not ok: return
            for p in root.self_and_subtree_iter():
                #@            << Write p's headline if it starts with @@ >>
                #@+node:ekr.20031218072017.2715:<< Write p's headline if it starts with @@ >>
                s = p.headString()
                
                if g.match(s,0,"@@"):
                    s = s[2:]
                    if s and len(s) > 0:
                        s = g.toEncodedString(s,self.encoding,reportErrors=True) # 3/7/03
                        self.outputFile.write(s)
                #@nonl
                #@-node:ekr.20031218072017.2715:<< Write p's headline if it starts with @@ >>
                #@nl
                #@            << Write p's body >>
                #@+node:ekr.20031218072017.2716:<< Write p's body >>
                s = p.bodyString()
                
                if s:
                    s = g.toEncodedString(s,self.encoding,reportErrors=True) # 3/7/03
                    self.outputStringWithLineEndings(s)
                #@nonl
                #@-node:ekr.20031218072017.2716:<< Write p's body >>
                #@nl
            self.closeWriteFile()
            self.replaceTargetFileIfDifferent()
            root.clearOrphan() ; root.clearDirty()
        except:
            self.handleWriteException(root)
            
    silentWrite = asisWrite # Compatibility with old scripts.
    #@nonl
    #@-node:ekr.20031218072017.2714:old_df.asisWrite
    #@+node:ekr.20031218072017.2710:old_df.norefWrite
    def norefWrite(self,root,toString=False):
    
        c = self.c ; self.root = root
        self.errors = 0
        self.sentinels = True # 10/1/03
        c.endEditing() # Capture the current headline.
        try:
            self.targetFileName = root.atNorefFileNodeName()
            ok = self.openWriteFile(root,toString)
            if not ok: return
            #@        << write root's tree >>
            #@+node:ekr.20031218072017.2711:<< write root's tree >>
            #@<< put all @first lines in root >>
            #@+node:ekr.20031218072017.2326:<< put all @first lines in root >> (3.x)
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
                # 21-SEP-2002 DTHEIN: write @first line, whether empty or not
                line = s[j:i]
                self.putBuffered(line) ; self.onl()
                i = g.skip_nl(s,i)
            #@nonl
            #@-node:ekr.20031218072017.2326:<< put all @first lines in root >> (3.x)
            #@nl
            self.putOpenLeoSentinel("@+leo")
            #@<< put optional @comment sentinel lines >>
            #@+node:ekr.20031218072017.2712:<< put optional @comment sentinel lines >>
            s2 = g.app.config.output_initial_comment
            if s2:
                lines = string.split(s2,"\\n")
                for line in lines:
                    line = line.replace("@date",time.asctime())
                    if len(line)> 0:
                        self.putSentinel("@comment " + line)
            #@-node:ekr.20031218072017.2712:<< put optional @comment sentinel lines >>
            #@nl
            
            for p in root.self_and_subtree_iter():
                #@    << Write p's node >>
                #@+node:ekr.20031218072017.2713:<< Write p's node >>
                self.putOpenNodeSentinel(p)
                    
                s = p.bodyString()
                if s and len(s) > 0:
                    self.putSentinel("@+body")
                    if self.newline_pending:
                        self.newline_pending = False
                        self.onl()
                    s = g.toEncodedString(s,self.encoding,reportErrors=True) # 3/7/03
                    self.outputStringWithLineEndings(s)
                    self.putSentinel("@-body")
                    
                self.putCloseNodeSentinel(p)
                #@-node:ekr.20031218072017.2713:<< Write p's node >>
                #@nl
            
            self.putSentinel("@-leo")
            #@<< put all @last lines in root >>
            #@+node:ekr.20031218072017.2328:<< put all @last lines in root >> (3.x)
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
                self.putBuffered(line[i:]) ; self.onl()
            #@nonl
            #@-node:ekr.20031218072017.2328:<< put all @last lines in root >> (3.x)
            #@nl
            #@nonl
            #@-node:ekr.20031218072017.2711:<< write root's tree >>
            #@nl
            self.closeWriteFile()
            self.replaceTargetFileIfDifferent()
            root.clearOrphan() ; root.clearDirty()
        except:
            self.handleWriteException(root)
            
    rawWrite = norefWrite
    #@nonl
    #@-node:ekr.20031218072017.2710:old_df.norefWrite
    #@+node:ekr.20031218072017.2322:old_df.write
    # This is the entry point to the write code.  root should be an @file vnode.
    
    def write(self,root,nosentinels=False,thinFile=False,toString=False,oneNodeOnly=False):
        
        if thinFile:
            self.error("@file-thin not supported before 4.2")
            return
        
        # Remove any old tnodeList.
        if hasattr(root.v.t,"tnodeList"):
            # g.trace("removing tnodeList for ",root)
            delattr(root.v.t,"tnodeList")
    
        c = self.c
        #@    << initialize >>
        #@+node:ekr.20031218072017.2323:<< initialize >>
        self.sentinels = not nosentinels
        self.raw = False
        
        self.errors = 0 # 9/26/02
        c.setIvarsFromPrefs()
        self.root = root
        c.endEditing() # Capture the current headline.
        #@nonl
        #@-node:ekr.20031218072017.2323:<< initialize >>
        #@nl
        try:
            #@        << open the file; return on error >>
            #@+node:ekr.20031218072017.2324:<< open the file; return on error >>
            if nosentinels:
                self.targetFileName = root.atNoSentFileNodeName()
            else:
                self.targetFileName = root.atFileNodeName()
            
            ok = self.openWriteFile(root,toString)
            if not ok: return
            #@nonl
            #@-node:ekr.20031218072017.2324:<< open the file; return on error >>
            #@nl
            root.clearAllVisitedInTree() # 1/28/04: clear both vnode and tnode bits.
            #@        << write then entire @file tree >>
            #@+node:ekr.20031218072017.2325:<< write then entire @file tree >> (3.x)
            next = root.nodeAfterTree()
            
            #@<< put all @first lines in root >>
            #@+node:ekr.20031218072017.2326:<< put all @first lines in root >> (3.x)
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
                # 21-SEP-2002 DTHEIN: write @first line, whether empty or not
                line = s[j:i]
                self.putBuffered(line) ; self.onl()
                i = g.skip_nl(s,i)
            #@nonl
            #@-node:ekr.20031218072017.2326:<< put all @first lines in root >> (3.x)
            #@nl
            #@<< write the derived file >>
            #@+node:ekr.20031218072017.2327:<< write the derived file>>
            tag1 = "@+leo"
            
            self.putOpenLeoSentinel(tag1)
            self.putInitialComment()
            self.putOpenNodeSentinel(root)
            self.putBodyPart(root)
            self.putCloseNodeSentinel(root)
            self.putSentinel("@-leo")
            #@nonl
            #@-node:ekr.20031218072017.2327:<< write the derived file>>
            #@nl
            #@<< put all @last lines in root >>
            #@+node:ekr.20031218072017.2328:<< put all @last lines in root >> (3.x)
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
                self.putBuffered(line[i:]) ; self.onl()
            #@nonl
            #@-node:ekr.20031218072017.2328:<< put all @last lines in root >> (3.x)
            #@nl
            
            root.setVisited()
            #@nonl
            #@-node:ekr.20031218072017.2325:<< write then entire @file tree >> (3.x)
            #@nl
            self.closeWriteFile()
            if not nosentinels:
                self.warnAboutOrphandAndIgnoredNodes()
            #@        << finish writing >>
            #@+node:ekr.20031218072017.2330:<< finish writing >>
            #@+at 
            #@nonl
            # We set the orphan and dirty flags if there are problems writing 
            # the file to force write_Leo_file to write the tree to the .leo 
            # file.
            #@-at
            #@@c
            
            if self.errors > 0 or self.root.isOrphan():
                root.setOrphan()
                root.setDirty() # 2/9/02: make _sure_ we try to rewrite this file.
                os.remove(self.outputFileName) # Delete the temp file.
                g.es("Not written: " + self.outputFileName)
            else:
                root.clearOrphan()
                root.clearDirty()
                self.replaceTargetFileIfDifferent()
            #@nonl
            #@-node:ekr.20031218072017.2330:<< finish writing >>
            #@nl
        except:
            self.handleWriteException()
    #@-node:ekr.20031218072017.2322:old_df.write
    #@+node:ekr.20031218072017.2717:Top level write helpers
    #@+node:ekr.20031218072017.2718:old_df.closeWriteFile
    def closeWriteFile (self):
        
        if not self.outputFile: return
    
        if self.suppress_newlines and self.newline_pending:
            self.newline_pending = False
            self.onl() # Make sure file ends with a newline.
    
        self.outputFile.flush()
        self.outputFile.close()
        self.outputFile = None
    #@nonl
    #@-node:ekr.20031218072017.2718:old_df.closeWriteFile
    #@+node:EKR.20040424085407:atFile.compareFilesIgnoringLineEndings
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
    #@-node:EKR.20040424085407:atFile.compareFilesIgnoringLineEndings
    #@+node:ekr.20031218072017.2719:atFile.handleWriteException
    def handleWriteException (self,root=None):
        
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
    #@-node:ekr.20031218072017.2719:atFile.handleWriteException
    #@+node:ekr.20031218072017.2720:atFile.openWriteFile (used by both old and new code)
    # Open files.  Set root.orphan and root.dirty flags and return on errors.
    
    def openWriteFile (self,root,toString):
        
        self.toStringFlag = toString
        self.errors = 0 # Bug fix: 6/25/04.
        self.root = root # Bug fix: 7/30/04: needed by error logic.
    
        try:
            self.scanAllDirectives(root)
            valid = self.errors == 0
        except:
            self.writeError("exception in atFile.scanAllDirectives")
            g.es_exception()
            valid = False
            
        if valid and toString:
            self.targetFileName = self.outputFileName = "<string-file>"
            self.outputFile = g.fileLikeObject()
            self.stringOutput = ""
            return valid
    
        if valid:
            try:
                fn = self.targetFileName
                self.shortFileName = fn # name to use in status messages.
                self.targetFileName = g.os_path_join(self.default_directory,fn)
                self.targetFileName = g.os_path_normpath(self.targetFileName)
                path = g.os_path_dirname(self.targetFileName)
                if not path or not g.os_path_exists(path):
                    self.writeError("path does not exist: " + path)
                    valid = False
            except:
                self.writeError("exception creating path:" + fn)
                g.es_exception()
                valid = False
    
        if valid and g.os_path_exists(self.targetFileName):
            try:
                if not os.access(self.targetFileName,os.W_OK):
                    self.writeError("can not create: read only: " + self.targetFileName)
                    valid = False
            except:
                pass # os.access() may not exist on all platforms.
            
        if valid:
            try:
                root.clearOrphan() # Bug fix: 5/25/04.
                self.outputFileName = self.targetFileName + ".tmp"
                self.outputFile = open(self.outputFileName,'wb')
                if self.outputFile is None:
                    self.writeError("can not create " + self.outputFileName)
                    valid = False
            except:
                g.es("exception creating:" + self.outputFileName)
                g.es_exception()
                valid = False
                self.outputFile = None # 3/22/04
    
        if not valid:
            root.setOrphan()
            root.setDirty()
            self.outputFile = None # 1/29/04
        
        return valid
    #@nonl
    #@-node:ekr.20031218072017.2720:atFile.openWriteFile (used by both old and new code)
    #@+node:ekr.20031218072017.2721:atFile.putInitialComment
    def putInitialComment (self):
        
        s2 = g.app.config.output_initial_comment
        if s2:
            lines = string.split(s2,"\\n")
            for line in lines:
                line = line.replace("@date",time.asctime())
                if len(line)> 0:
                    self.putSentinel("@comment " + line)
    #@nonl
    #@-node:ekr.20031218072017.2721:atFile.putInitialComment
    #@+node:ekr.20031218072017.2023:atFile.replaceTargetFileIfDifferent
    def replaceTargetFileIfDifferent (self):
        
        assert(self.outputFile is None)
        
        self.fileChangedFlag = False
        if g.os_path_exists(self.targetFileName):
            if self.compareFilesIgnoringLineEndings(
                self.outputFileName,self.targetFileName):
                #@            << delete the output file >>
                #@+node:ekr.20031218072017.2024:<< delete the output file >>
                try: # Just delete the temp file.
                    os.remove(self.outputFileName)
                except:
                    g.es("exception deleting:" + self.outputFileName)
                    g.es_exception()
                
                g.es("unchanged: " + self.shortFileName)
                #@nonl
                #@-node:ekr.20031218072017.2024:<< delete the output file >>
                #@nl
            else:
                #@            << replace the target file with the output file >>
                #@+node:ekr.20031218072017.2025:<< replace the target file with the output file >>
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
                #@-node:ekr.20031218072017.2025:<< replace the target file with the output file >>
                #@nl
        else:
            #@        << rename the output file to be the target file >>
            #@+node:ekr.20031218072017.2026:<< rename the output file to be the target file >>
            try:
                g.utils_rename(self.outputFileName,self.targetFileName)
                g.es("creating: " + self.targetFileName)
                self.fileChangedFlag = True
            except:
                self.writeError("exception renaming:" + self.outputFileName +
                    " to " + self.targetFileName)
                g.es_exception()
            #@nonl
            #@-node:ekr.20031218072017.2026:<< rename the output file to be the target file >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.2023:atFile.replaceTargetFileIfDifferent
    #@+node:ekr.20031218072017.2722:atFile.outputStringWithLineEndings
    # Write the string s as-is except that we replace '\n' with the proper line ending.
    
    def outputStringWithLineEndings (self,s):
    
        # Calling self.onl() runs afoul of queued newlines.
        self.os(s.replace('\n',self.output_newline))
    #@nonl
    #@-node:ekr.20031218072017.2722:atFile.outputStringWithLineEndings
    #@+node:ekr.20040128174042:atFile.warnAboutOrpanAndIgnoredNodes
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
    #@-node:ekr.20040128174042:atFile.warnAboutOrpanAndIgnoredNodes
    #@-node:ekr.20031218072017.2717:Top level write helpers
    #@-node:ekr.20031218072017.2709:Top level
    #@+node:ekr.20031218072017.2723:putBodyPart (3.x)
    def putBodyPart(self,p):
        
        """ Generate the body enclosed in sentinel lines."""
    
        s = p.v.t.bodyString
        i = g.skip_ws_and_nl(s, 0)
        if i >= len(s): return
    
        s = g.removeTrailingWs(s) # don't use string.rstrip!
        self.putSentinel("@+body")
        #@    << put code/doc parts and sentinels >>
        #@+node:ekr.20031218072017.2724:<< put code/doc parts and sentinels >> (3.x)
        i = 0 ; n = len(s)
        firstLastHack = 1
        
        if firstLastHack:
            #@    << initialize lookingForFirst/Last & initialLastDirective >>
            #@+node:ekr.20031218072017.2725:<< initialize lookingForFirst/Last & initialLastDirective >>
            # 14-SEP-2002 DTHEIN: If this is the root node, then handle all @first directives here
            lookingForLast = 0
            lookingForFirst = 0
            initialLastDirective = -1
            lastDirectiveCount = 0
            if (p == self.root):
                lookingForLast = 1
                lookingForFirst = 1
            #@nonl
            #@-node:ekr.20031218072017.2725:<< initialize lookingForFirst/Last & initialLastDirective >>
            #@nl
        while i < n:
            kind = self.directiveKind(s,i)
            if firstLastHack:
                #@        << set lookingForFirst/Last & initialLastDirective >>
                #@+node:ekr.20031218072017.2726:<< set lookingForFirst/Last & initialLastDirective >>
                # 14-SEP-2002 DTHEIN: If first directive isn't @first, then stop looking for @first
                if lookingForFirst:
                    if kind != miscDirective:
                        lookingForFirst = 0
                    elif not g.match_word(s,i,"@first"):
                        lookingForFirst = 0
                
                if lookingForLast:
                    if initialLastDirective == -1:
                        if (kind == miscDirective) and g.match_word(s,i,"@last"):
                            # mark the point where the last directive was found
                            initialLastDirective = i
                    else:
                        if (kind != miscDirective) or (not g.match_word(s,i,"@last")):
                            # found something after @last, so process the @last directives
                            # in 'ignore them' mode
                            i, initialLastDirective = initialLastDirective, -1
                            lastDirectiveCount = 0
                            kind = self.directiveKind(s,i)
                #@nonl
                #@-node:ekr.20031218072017.2726:<< set lookingForFirst/Last & initialLastDirective >>
                #@nl
            j = i
            if kind == docDirective or kind == atDirective:
                i = self.putDoc(s,i,kind)
            elif ( # 10/16/02
                kind == miscDirective or
                kind == rawDirective or
                kind == endRawDirective ):
                if firstLastHack:
                    #@            << handle misc directives >>
                    #@+node:ekr.20031218072017.2727:<< handle misc directives >>
                    if lookingForFirst: # DTHEIN: can only be True if it is @first directive
                        i = self.putEmptyDirective(s,i)
                    elif (initialLastDirective != -1) and g.match_word(s,i,"@last"):
                        # DTHEIN: can only be here if lookingForLast is True
                        # skip the last directive ... we'll output it at the end if it
                        # is truly 'last'
                        lastDirectiveCount += 1
                        i = g.skip_line(s,i)
                    else:
                        i = self.putDirective(s,i)
                    #@nonl
                    #@-node:ekr.20031218072017.2727:<< handle misc directives >>
                    #@nl
                else:
                    i = self.putDirective(s,i)
            elif kind == noDirective or kind == othersDirective:
                i = self.putCodePart(s,i,p)
            elif kind == cDirective or kind == codeDirective:
                i = self.putDirective(s,i)
                i = self.putCodePart(s,i,p)
            else: assert(False) # We must handle everything that directiveKind returns
            assert(n == len(s))
            assert(j < i) # We must make progress.
        
        if firstLastHack:
            #@    << put out the last directives, if any >>
            #@+node:ekr.20031218072017.2728:<< put out the last directives, if any >>
            # 14-SEP-2002 DTHEIN
            if initialLastDirective != -1:
                d = initialLastDirective
                for k in range(lastDirectiveCount):
                    d = self.putEmptyDirective(s,d)
            #@nonl
            #@-node:ekr.20031218072017.2728:<< put out the last directives, if any >>
            #@nl
        #@nonl
        #@-node:ekr.20031218072017.2724:<< put code/doc parts and sentinels >> (3.x)
        #@nl
        self.putSentinel("@-body")
    #@nonl
    #@-node:ekr.20031218072017.2723:putBodyPart (3.x)
    #@+node:ekr.20031218072017.2729:putDoc
    def putDoc(self,s,i,kind):
    
        """Outputs a doc section terminated by @code or end-of-text.
        
        All other interior directives become part of the doc part."""
    
        if kind == atDirective:
            i += 1 ; tag = "at"
        elif kind == docDirective:
            i += 4 ; tag = "doc"
        else: assert(False)
        # Set j to the end of the doc part.
        n = len(s) ; j = i
        while j < n:
            j = g.skip_line(s, j)
            kind = self.directiveKind(s, j)
            if kind == codeDirective or kind == cDirective:
                break
        self.putSentinel("@+" + tag)
        self.putDocPart(s[i:j])
        self.putSentinel("@-" + tag)
        return j
    #@-node:ekr.20031218072017.2729:putDoc
    #@+node:ekr.20031218072017.2730:putDocPart (3.x)
    # Puts a comment part in comments.
    # Note: this routine is _never_ called in cweb mode,
    # so noweb section references are _valid_ in cweb doc parts!
    
    def putDocPart(self,s):
    
        # j = g.skip_line(s,0) ; g.trace(s[:j])
        single = len(self.endSentinelComment) == 0
        if not single:
            self.putIndent(self.indent)
            self.os(self.startSentinelComment) ; self.onl()
        # Put all lines.
        i = 0 ; n = len(s)
        while i < n:
            self.putIndent(self.indent)
            leading = self.indent
            if single:
                self.os(self.startSentinelComment) ; self.oblank()
                leading += len(self.startSentinelComment) + 1
            #@        << copy words, splitting the line if needed >>
            #@+node:ekr.20031218072017.2731:<< copy words, splitting the line if needed >>
            #@+at 
            #@nonl
            # We remove trailing whitespace from lines that have _not_ been 
            # split so that a newline has been inserted by this routine if and 
            # only if it is preceded by whitespace.
            #@-at
            #@@c
            
            line = i # Start of the current line.
            while i < n:
                word = i # Start of the current word.
                # Skip the next word and trailing whitespace.
                i = g.skip_ws(s, i)
                while i < n and not g.is_nl(s,i) and not g.is_ws(s[i]):
                    i += 1
                i = g.skip_ws(s,i)
                # Output the line if no more is left.
                if i < n and g.is_nl(s,i):
                    break
                # Split the line before the current word if needed.
                lineLen = i - line
                if line == word or leading + lineLen < self.page_width:
                    word = i # Advance to the next word.
                else:
                    # Write the line before the current word and insert a newline.
                    theLine = s[line:word]
                    self.os(theLine)
                    self.onl() # This line must contain trailing whitespace.
                    line = i = word  # Put word on the next line.
                    break
            # Remove trailing whitespace and output the remainder of the line.
            theLine = string.rstrip(s[line:i]) # from right.
            self.os(theLine)
            if i < n and g.is_nl(s,i):
                i = g.skip_nl(s,i)
                self.onl() # No inserted newline and no trailing whitespace.
            #@nonl
            #@-node:ekr.20031218072017.2731:<< copy words, splitting the line if needed >>
            #@nl
        if not single:
            # This comment is like a sentinel.
            self.onl() ; self.putIndent(self.indent)
            self.os(self.endSentinelComment)
            self.onl() # Note: no trailing whitespace.
    #@nonl
    #@-node:ekr.20031218072017.2730:putDocPart (3.x)
    #@+node:ekr.20031218072017.2732:putCodePart & allies (3.x)
    def putCodePart(self,s,i,p):
    
        """Expands a code part, terminated by any at-directive except at-others.
        
        It expands references and at-others and outputs @verbatim sentinels as needed."""
    
        atOthersSeen = False # True: at-others has been expanded.
        while i < len(s):
            #@        << handle the start of a line >>
            #@+node:ekr.20031218072017.2733:<< handle the start of a line >>
            #@+at 
            #@nonl
            # The at-others directive is the only directive that is recognized 
            # following leading whitespace, so it is just a little tricky to 
            # recognize it.
            #@-at
            #@@c
            
            leading_nl = (s[i] == g.body_newline) # 9/27/02: look ahead before outputting newline.
            if leading_nl:
                i = g.skip_nl(s,i)
                self.onl() # 10/15/02: simpler to do it here.
            
            #leading_ws1 = i # 1/27/03
            j,delta = g.skip_leading_ws_with_indent(s,i,self.tab_width)
            #leading_ws2 = j # 1/27/03
            kind1 = self.directiveKind(s,i)
            kind2 = self.directiveKind(s,j)
            if self.raw:
                if kind1 == endRawDirective:
                    #@        << handle @end_raw >>
                    #@+node:ekr.20031218072017.2736:<< handle @end_raw >>
                    self.raw = False
                    self.putSentinel("@@end_raw")
                    i = g.skip_line(s,i)
                    #@nonl
                    #@-node:ekr.20031218072017.2736:<< handle @end_raw >>
                    #@nl
            else:
                if kind1 == othersDirective or kind2 == othersDirective:
                    #@        << handle @others >>
                    #@+node:ekr.20031218072017.2734:<< handle @others >>
                    # This skips all indent and delta whitespace, so putAtOthers must generate it all.
                    
                    if 0: # 9/27/02: eliminates the newline preceeding the @+others sentinel.
                        # This does not seem to be a good idea.
                        i = g.skip_line(s,i) 
                    else:
                        i = g.skip_to_end_of_line(s,i)
                    
                    if atOthersSeen:
                        self.writeError("@others already expanded in: " + p.headString())
                    else:
                        atOthersSeen = True
                        self.putAtOthers(p,delta)
                        
                        # 12/8/02: Skip the newline _after_ the @others.
                        if not self.sentinels and g.is_nl(s,i):
                            i = g.skip_nl(s,i)
                    #@-node:ekr.20031218072017.2734:<< handle @others >>
                    #@nl
                elif kind1 == rawDirective:
                    #@        << handle @raw >>
                    #@+node:ekr.20031218072017.2735:<< handle @raw >>
                    self.raw = True
                    self.putSentinel("@@raw")
                    i = g.skip_line(s,i)
                    #@nonl
                    #@-node:ekr.20031218072017.2735:<< handle @raw >>
                    #@nl
                elif kind1 == noDirective:
                    #@        << put @verbatim sentinel if necessary >>
                    #@+node:ekr.20031218072017.2737:<< put @verbatim sentinel if necessary >>
                    if g.match (s,i,self.startSentinelComment + '@'):
                        self.putSentinel("@verbatim") # Bug fix (!!): 9/20/03
                    #@nonl
                    #@-node:ekr.20031218072017.2737:<< put @verbatim sentinel if necessary >>
                    #@nl
                else:
                    break # all other directives terminate the code part.
            #@nonl
            #@-node:ekr.20031218072017.2733:<< handle the start of a line >>
            #@nl
            #@        << put the line >>
            #@+node:ekr.20031218072017.2738:<< put the line >>
            if not self.raw:
                # 12/8/02: Don't write trailing indentation if not writing sentinels.
                if self.sentinels or j < len(s):
                    self.putIndent(self.indent)
            
            newlineSeen = False
            # 12/8/02: we buffer characters here for two reasons:
            # 1) to make traces easier to read and 2) to increase speed.
            buf = i # Indicate the start of buffered characters.
            while i < len(s) and not newlineSeen:
                ch = s[i]
                if ch == g.body_newline:
                    break
                elif ch == g.body_ignored_newline:
                    i += 1
                elif ch == '<' and not self.raw:
                    #@        << put possible section reference >>
                    #@+node:ekr.20031218072017.2739:<< put possible section reference >>
                    isSection, j = self.isSectionName(s, i)
                    
                    if isSection:
                        # Output the buffered characters and clear the buffer.
                        s2 = s[buf:i] ; buf = i
                        # 7/9/03: don't output trailing indentation if we aren't generating sentinels.
                        if not self.sentinels:
                            while len(s2) and s2[-1] in (' ','\t'):
                                s2 = s2[:-1]
                        self.putBuffered(s2)
                        # Output the expansion.
                        name = s[i:j]
                        j,newlineSeen = self.putRef(name,p,s,j,delta)
                        assert(j > i) # isSectionName must have made progress
                        i = j ; buf = i
                    else:
                        # This is _not_ an error.
                        i += 1
                    #@nonl
                    #@-node:ekr.20031218072017.2739:<< put possible section reference >>
                    #@nl
                else:
                    i += 1
            # Output any buffered characters.
            self.putBuffered(s[buf:i])
            #@nonl
            #@-node:ekr.20031218072017.2738:<< put the line >>
            #@nl
    
        # Raw code parts can only end at the end of body text.
        self.raw = False
        return i
    #@+node:ekr.20031218072017.2740:inAtOthers
    def inAtOthers(self,p):
    
        """Returns True if p should be included in the expansion of the at-others directive in the body text of p's parent.
        
        p will not be included if it is a definition node or if its body text contains an @ignore directive.
        Previously, a "nested" @others directive would also inhibit the inclusion of p."""
    
        # Return False if this has been expanded previously.
        if  p.isVisited(): return False
    
        # Return False if this is a definition node.
        h = p.headString()
        i = g.skip_ws(h,0)
        isSection, j = self.isSectionName(h,i)
        if isSection: return False
    
        # Return False if p's body contains an @ignore or at-others directive.
        if 1: # 7/29/02: New code.  Amazingly, this appears to work!
            return not p.isAtIgnoreNode()
        else: # old & reliable code
            return not p.isAtIgnoreNode() and not p.isAtOthersNode()
    #@nonl
    #@-node:ekr.20031218072017.2740:inAtOthers
    #@+node:ekr.20031218072017.2741:isSectionName
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
    #@-node:ekr.20031218072017.2741:isSectionName
    #@+node:ekr.20031218072017.2742:putAtOthers
    #@+at 
    #@nonl
    # The at-others directive is recognized only at the start of the line.  
    # This code must generate all leading whitespace for the opening sentinel.
    #@-at
    #@@c
    def putAtOthers(self,p,delta):
        
        """Output code corresponding to an @others directive."""
    
        self.indent += delta
        self.putSentinel("@+others")
    
        for child in p.children_iter():
            if self.inAtOthers(child):
                self.putAtOthersChild(child)
    
        self.putSentinel("@-others")
        self.indent -= delta
    #@nonl
    #@-node:ekr.20031218072017.2742:putAtOthers
    #@+node:ekr.20031218072017.2743:putAtOthersChild
    def putAtOthersChild(self,p):
        
        # g.trace(self.indent,p)
        self.putOpenNodeSentinel(p)
        
        # Insert the expansion of p.
        p.v.setVisited() # Make sure it is never expanded again.
        self.putBodyPart(p)
    
        # Insert expansions of all children.
        for child in p.children_iter():
            if self.inAtOthers(child):
                self.putAtOthersChild(child)
    
        self.putCloseNodeSentinel(p)
    #@-node:ekr.20031218072017.2743:putAtOthersChild
    #@+node:ekr.20031218072017.2744:putRef
    def putRef (self,name,p,s,i,delta):
    
        newlineSeen = False
        ref = g.findReference(name,p)
        if not ref:
            self.writeError("undefined section: " + name +
                "\n\treferenced from: " + p.headString())
            return i,newlineSeen
    
        # g.trace(self.indent,delta,s[i:])
        #@    << Generate the expansion of the reference >>
        #@+node:ekr.20031218072017.2745:<< Generate the expansion of the reference >>
        # Adjust indent here so sentinel looks better.
        self.indent += delta
        
        self.putSentinel("@" + name)
        self.putOpenSentinels(p,ref)
        self.putBodyPart(ref)
        self.putCloseSentinels(p,ref)
        #@<< Add @verbatimAfterRef sentinel if required >>
        #@+node:ekr.20031218072017.2746:<< Add @verbatimAfterRef sentinel if required >>
        j = g.skip_ws(s,i)
        if j < len(s) and g.match(s,j,self.startSentinelComment + '@'):
            self.putSentinel("@verbatimAfterRef")
            # 9/27/02: Put the line immediately, before the @-node sentinel.
            k = g.skip_to_end_of_line(s,i)
            self.putBuffered(s[i:k])
            i = k ; newlineSeen = False
        #@nonl
        #@-node:ekr.20031218072017.2746:<< Add @verbatimAfterRef sentinel if required >>
        #@nl
        
        self.indent -= delta
        ref.setVisited()
        #@nonl
        #@-node:ekr.20031218072017.2745:<< Generate the expansion of the reference >>
        #@nl
    
        # The newlineSeen allows the caller to break out of the loop.
        return i,newlineSeen
    #@nonl
    #@-node:ekr.20031218072017.2744:putRef
    #@-node:ekr.20031218072017.2732:putCodePart & allies (3.x)
    #@+node:ekr.20031218072017.2747:Writing Utils
    #@+node:ekr.20031218072017.2748:putBuffered
    def putBuffered (self,s):
        
        """Put s, converting all tabs to blanks as necessary."""
        
        if s:
            w = self.tab_width
            if w < 0:
                lines = s.split('\n')
                for i in xrange(len(lines)):
                    line = lines[i]
                    line2 = ""
                    for j in xrange(len(line)):
                        ch = line[j]
                        if ch == '\t':
                            w2 = g.computeWidth(s[:j],w)
                            w3 = (abs(w) - (w2 % abs(w)))
                            line2 += ' ' * w3
                        else:
                            line2 += ch
                    lines[i] = line2
                s = string.join(lines,'\n')
            self.os(s)
    #@nonl
    #@-node:ekr.20031218072017.2748:putBuffered
    #@+node:ekr.20031218072017.2749:os, onl, etc. (leoAtFile)
    def oblank(self):
        self.os(' ')
    
    def oblanks(self,n):
        self.os(' ' * abs(n))
    
    def onl(self):
        self.os(self.output_newline)
    
    def os(self,s):
        if s is None or len(s) == 0: return
        if self.suppress_newlines and self.newline_pending:
            self.newline_pending = False
            s = self.output_newline + s
        if self.outputFile:
            try:
                s = g.toEncodedString(s,self.encoding,reportErrors=True)
                self.outputFile.write(s)
            except:
                g.es("exception writing:",s)
                g.es_exception()
    
    def otabs(self,n):
        self.os('\t' * abs(n))
    #@nonl
    #@-node:ekr.20031218072017.2749:os, onl, etc. (leoAtFile)
    #@+node:ekr.20031218072017.2750:putDirective  (handles @delims) 3.x
    # This method outputs s, a directive or reference, in a sentinel.
    
    def putDirective(self,s,i):
    
        tag = "@delims"
        assert(i < len(s) and s[i] == '@')
        k = i
        j = g.skip_to_end_of_line(s,i)
        directive = s[i:j]
    
        if g.match_word(s,k,tag):
            #@        << handle @delims >>
            #@+node:ekr.20031218072017.2751:<< handle @delims >>
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
            #@-node:ekr.20031218072017.2751:<< handle @delims >>
            #@nl
        else:
            self.putSentinel("@" + directive)
    
        i = g.skip_line(s,k)
        return i
    #@nonl
    #@-node:ekr.20031218072017.2750:putDirective  (handles @delims) 3.x
    #@+node:ekr.20031218072017.2752:putEmptyDirective (Dave Hein)
    # 14-SEP-2002 DTHEIN
    # added for use by putBodyPart()
    
    # This method outputs the directive without the parameter text
    def putEmptyDirective(self,s,i):
    
        assert(i < len(s) and s[i] == '@')
        
        endOfLine = s.find('\n',i)
        # 21-SEP-2002 DTHEIN: if no '\n' then just use line length
        if endOfLine == -1:
            endOfLine = len(s)
        token = s[i:endOfLine].split()
        directive = token[0]
        self.putSentinel("@" + directive)
    
        i = g.skip_line(s,i)
        return i
    #@nonl
    #@-node:ekr.20031218072017.2752:putEmptyDirective (Dave Hein)
    #@+node:ekr.20031218072017.2753:putIndent
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
    #@-node:ekr.20031218072017.2753:putIndent
    #@-node:ekr.20031218072017.2747:Writing Utils
    #@-node:ekr.20031218072017.2708:Writing (3.x) (Deprecated)
    #@-others
    #@nonl
    #@-node:ekr.20031218072017.2643:<< class baseOldDerivedFile methods >>
    #@nl
    
class oldDerivedFile(baseOldDerivedFile):
    pass # May be overridden in plugins.
    
class baseNewDerivedFile(oldDerivedFile):
    """The base class to read and write 4.x derived files."""
    #@    << class baseNewDerivedFile methods >>
    #@+node:ekr.20031218072017.2754:<< class baseNewDerivedFile methods >>
    #@+others
    #@+node:ekr.20031218072017.2755:newDerivedFile.__init__
    def __init__(self,c):
        
        """Ctor for 4.x atFile class."""
        
        at = self
    
        # Initialize the base class.
        oldDerivedFile.__init__(self,c) 
    
        # For 4.x reading & writing...
        at.inCode = True
        at.thinFile = False
        at.cloneSibCount = 0 # n > 1: Make sure n cloned sibs exists at next @+node sentinel
    
        # For 4.x writing...
        at.docKind = None
        at.pending = [] # Doc part that remains to be written.
    
        # For 4.x reading...
        at.docOut = [] # The doc part being accumulated.
        at.done = False # True when @-leo seen.
        at.endSentinelStack = []
        at.importing = False
        at.indent = 0 ; at.indentStack = []
        at.lastLines = [] # The lines after @-leo
        at.leadingWs = ""
        at.out = None ; at.outStack = []
        at.root_seen = False # True: root vnode has been handled in this file.
        at.tnodeList = [] ; at.tnodeListIndex = 0
        at.t = None ; at.tStack = []
        at.updateWarningGiven = False
        
        # For reading thin derived files.
        at.lastThinNode = None ; at.thinNodeStack = [] # Used by createThinChild.
        at.perfectImportRoot = None # The root of the perfect import command.
    
        #@    << Create the dispatch dictionary used by scanText4 >>
        #@+node:EKR.20040427134616:<< Create the dispatch dictionary used by scanText4 >>
        at.dispatch_dict = {
            # Plain line.
            noSentinel: at.readNormalLine,
            # Starting sentinels...
            startAll:    at.readStartAll,
            startAt:     at.readStartAt,
            startDoc:    at.readStartDoc,
            startLeo:    at.readStartLeo,
            startMiddle: at.readStartMiddle,
            startNode:   at.readStartNode,
            startOthers: at.readStartOthers,
            # Ending sentinels...
            endAll:    at.readEndAll,
            endAt:     at.readEndAt,
            endDoc:    at.readEndDoc,
            endLeo:    at.readEndLeo,
            endMiddle: at.readEndMiddle,
            endNode:   at.readEndNode,
            endOthers: at.readEndOthers,
            # Non-paired sentinels.
            startAfterRef:  at.readAfterRef,
            startClone:     at.readClone,
            startComment:   at.readComment,
            startDelims:    at.readDelims,
            startDirective: at.readDirective,
            startNl:        at.readNl,
            startNonl:      at.readNonl,
            startRef:       at.readRef,
            startVerbatim:  at.readVerbatim,
            # Ignored 3.x sentinels
            endBody:               at.ignoreOldSentinel,
            startBody:             at.ignoreOldSentinel,
            startVerbatimAfterRef: at.ignoreOldSentinel }
        #@nonl
        #@-node:EKR.20040427134616:<< Create the dispatch dictionary used by scanText4 >>
        #@nl
    #@nonl
    #@-node:ekr.20031218072017.2755:newDerivedFile.__init__
    #@+node:ekr.20031218072017.2756:Reading (4.x)
    #@+node:ekr.20040321064134.5:createThinChild (4.2: @thin only)
    def createThinChild (self,gnxString,headline):
    
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
    #@-node:ekr.20040321064134.5:createThinChild (4.2: @thin only)
    #@+node:ekr.20031218072017.2757:new_df.readOpenFile
    def readOpenFile(self,root,theFile,firstLines,perfectImportRoot=None):
        
        """Read an open 4.x thick or thin derived file."""
        
        at = self
        
        # This is safe (just barely) because only this method calls scanText4>
        at.perfectImportRoot = perfectImportRoot
    
        # Scan the 4.x file.
        at.tnodeListIndex = 0
        # at.thinFile tells scanText4 whether this is a thin file or not.
        lastLines = at.scanText4(theFile,root)
        root.v.t.setVisited() # Disable warning about set nodes.
        
        # Handle first and last lines.
        try: body = root.v.t.tempBodyString
        except: body = ""
        lines = body.split('\n')
        at.completeFirstDirectives(lines,firstLines)
        at.completeLastDirectives(lines,lastLines)
        s = '\n'.join(lines).replace('\r', '')
        root.v.t.tempBodyString = s
    #@nonl
    #@-node:ekr.20031218072017.2757:new_df.readOpenFile
    #@+node:ekr.20031218072017.2007:findChild 4.x (@file only)
    def findChild (self,headline):
        
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
    #@-node:ekr.20031218072017.2007:findChild 4.x (@file only)
    #@+node:ekr.20031218072017.2758:scanText4 & allies
    def scanText4 (self,theFile,p):
        
        """Scan a 4.x derived file non-recursively."""
    
        at = self
        #@    << init ivars for scanText4 >>
        #@+node:ekr.20031218072017.2759:<< init ivars for scanText4 >>
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
        at.endSentinelStack = [endLeo] # We have already handled the @+leo sentinel.
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
        #@-node:ekr.20031218072017.2759:<< init ivars for scanText4 >>
        #@nl
        while at.errors == 0 and not at.done:
            s = at.readLine(theFile)
            if len(s) == 0: break
            kind = at.sentinelKind(s)
            # g.trace(at.sentinelName(kind),s.strip())
            if kind == noSentinel:
                i = 0
            else:
                i = at.skipSentinelStart(s,0)
            func = at.dispatch_dict[kind]
            func(s,i)
    
        if at.errors == 0 and not at.done:
            #@        << report unexpected end of text >>
            #@+node:ekr.20031218072017.2760:<< report unexpected end of text >>
            assert(at.endSentinelStack)
            
            at.readError(
                "Unexpected end of file. Expecting %s sentinel" %
                at.sentinelName(at.endSentinelStack[-1]))
            #@nonl
            #@-node:ekr.20031218072017.2760:<< report unexpected end of text >>
            #@nl
    
        return at.lastLines
    #@+node:ekr.20031218072017.2761:readNormalLine
    def readNormalLine (self,s,i):
    
        at = self
        
        if at.inCode:
            if not at.raw:
                s = g.removeLeadingWhitespace(s,at.indent,at.tab_width)
            at.out.append(s)
        else:
            #@        << Skip the leading stuff >>
            #@+node:ekr.20031218072017.2762:<< Skip the leading stuff >>
            if len(at.endSentinelComment) == 0:
                # Skip the single comment delim and a blank.
                i = g.skip_ws(s,0)
                if g.match(s,i,at.startSentinelComment):
                    i += len(at.startSentinelComment)
                    if g.match(s,i," "): i += 1
            else:
                i = at.skipIndent(s,0,at.indent)
            
            #@-node:ekr.20031218072017.2762:<< Skip the leading stuff >>
            #@nl
            #@        << Append s to docOut >>
            #@+node:ekr.20031218072017.2763:<< Append s to docOut >>
            line = s[i:-1] # remove newline for rstrip.
            
            if line == line.rstrip():
                # no trailing whitespace: the newline is real.
                at.docOut.append(line + '\n')
            else:
                # trailing whitespace: the newline is fake.
                at.docOut.append(line)
            #@nonl
            #@-node:ekr.20031218072017.2763:<< Append s to docOut >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.2761:readNormalLine
    #@+node:ekr.20031218072017.2764:start sentinels
    #@+node:EKR.20040430081719:readStartAll (4.2)
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
        
        at.endSentinelStack.append(endAll)
    #@nonl
    #@-node:EKR.20040430081719:readStartAll (4.2)
    #@+node:ekr.20031218072017.1752:readStartAt & readStartDoc
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
        at.endSentinelStack.append(endAt)
        
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
        at.endSentinelStack.append(endDoc)
        
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
    #@-node:ekr.20031218072017.1752:readStartAt & readStartDoc
    #@+node:ekr.20031218072017.2765:readStartLeo
    def readStartLeo (self,s,i):
        
        """Read an unexpected @+leo sentinel."""
    
        at = self
        assert(g.match(s,i,"+leo"))
        at.readError("Ignoring unexpected @+leo sentinel")
    #@nonl
    #@-node:ekr.20031218072017.2765:readStartLeo
    #@+node:EKR.20040524070500:readStartMiddle
    def readStartMiddle (self,s,i):
        
        """Read an @+middle sentinel."""
        
        at = self
        
        at.readStartNode(s,i,middle=True)
    #@nonl
    #@-node:EKR.20040524070500:readStartMiddle
    #@+node:ekr.20031218072017.2766:readStartNode (4.x)
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
            #@+node:EKR.20040427105350:<< set gnx and bump i >>
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
            #@-node:EKR.20040427105350:<< set gnx and bump i >>
            #@nl
        #@    << Set headline, undoing the CWEB hack >>
        #@+node:ekr.20031218072017.2767:<< Set headline, undoing the CWEB hack >>
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
        #@-node:ekr.20031218072017.2767:<< Set headline, undoing the CWEB hack >>
        #@nl
        if not at.root_seen:
            at.root_seen = True
            #@        << Check the filename in the sentinel >>
            #@+node:ekr.20031218072017.2768:<< Check the filename in the sentinel >>
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
            #@-node:ekr.20031218072017.2768:<< Check the filename in the sentinel >>
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
            at.lastThinNode = v = at.createThinChild(gnx,headline)
            at.t = v.t
        else:
            at.t = at.findChild(headline)
        
        at.endSentinelStack.append(endNode)
    #@nonl
    #@-node:ekr.20031218072017.2766:readStartNode (4.x)
    #@+node:ekr.20031218072017.2769:readStartOthers
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
        
        at.endSentinelStack.append(endOthers)
    #@nonl
    #@-node:ekr.20031218072017.2769:readStartOthers
    #@-node:ekr.20031218072017.2764:start sentinels
    #@+node:ekr.20031218072017.2770:end sentinels
    #@+node:EKR.20040430081719.1:readEndAll (4.2)
    def readEndAll (self,s,i):
        
        """Read an @-all sentinel."""
        
        at = self
        at.popSentinelStack(endAll)
    #@nonl
    #@-node:EKR.20040430081719.1:readEndAll (4.2)
    #@+node:ekr.20031218072017.1954:readEndAt & readEndDoc
    def readEndAt (self,s,i):
        
        """Read an @-at sentinel."""
    
        at = self
        at.readLastDocLine("@")
        at.popSentinelStack(endAt)
        at.inCode = True
            
    def readEndDoc (self,s,i):
        
        """Read an @-doc sentinel."""
    
        at = self
        at.readLastDocLine("@doc")
        at.popSentinelStack(endDoc)
        at.inCode = True
    #@nonl
    #@-node:ekr.20031218072017.1954:readEndAt & readEndDoc
    #@+node:ekr.20031218072017.2771:readEndLeo
    def readEndLeo (self,s,i):
        
        """Read an @-leo sentinel."""
        
        at = self
    
        # Ignore everything after @-leo.
        # Such lines were presumably written by @last.
        while 1:
            s = at.readLine(at.file)
            if len(s) == 0: break
            at.lastLines.append(s) # Capture all trailing lines, even if empty.
    
        at.done = True
    #@nonl
    #@-node:ekr.20031218072017.2771:readEndLeo
    #@+node:EKR.20040524071414:readEndMiddle
    def readEndMiddle (self,s,i):
        
        """Read an @-middle sentinel."""
        
        at = self
        
        at.readEndNode(s,i,middle=True)
    #@nonl
    #@-node:EKR.20040524071414:readEndMiddle
    #@+node:ekr.20031218072017.2772:readEndNode (4.x)
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
                #@+node:ekr.20040904081433:<< indicate that the node has been changed >>
                if at.perfectImportRoot:
                    #@    << bump at.correctedLines and tell about the correction >>
                    #@+node:ekr.20040717133944:<< bump at.correctedLines and tell about the correction >>
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
                    #@-node:ekr.20040717133944:<< bump at.correctedLines and tell about the correction >>
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
                #@-node:ekr.20040904081433:<< indicate that the node has been changed >>
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
    
        at.popSentinelStack(endNode)
    #@nonl
    #@-node:ekr.20031218072017.2772:readEndNode (4.x)
    #@+node:ekr.20031218072017.2773:readEndOthers
    def readEndOthers (self,s,i):
        
        """Read an @-others sentinel."""
        
        at = self
        at.popSentinelStack(endOthers)
    #@nonl
    #@-node:ekr.20031218072017.2773:readEndOthers
    #@+node:ekr.20031218072017.1753:readLastDocLine
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
    #@-node:ekr.20031218072017.1753:readLastDocLine
    #@-node:ekr.20031218072017.2770:end sentinels
    #@+node:ekr.20031218072017.2774:Unpaired sentinels
    #@+node:ekr.20031218072017.2775:ignoreOldSentinel
    def  ignoreOldSentinel (self,s,i):
        
        """Ignore an 3.x sentinel."""
        
        g.es("Ignoring 3.x sentinel: " + s.strip(), color="blue")
    #@nonl
    #@-node:ekr.20031218072017.2775:ignoreOldSentinel
    #@+node:ekr.20031218072017.2776:readAfterRef
    def  readAfterRef (self,s,i):
        
        """Read an @afterref sentinel."""
        
        at = self
        assert(g.match(s,i,"afterref"))
        
        # Append the next line to the text.
        s = at.readLine(at.file)
        at.out.append(s)
    #@nonl
    #@-node:ekr.20031218072017.2776:readAfterRef
    #@+node:EKR.20040520093903:readClone
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
    #@-node:EKR.20040520093903:readClone
    #@+node:ekr.20031218072017.2777:readComment
    def readComment (self,s,i):
        
        """Read an @comment sentinel."""
    
        assert(g.match(s,i,"comment"))
    
        # Just ignore the comment line!
    #@-node:ekr.20031218072017.2777:readComment
    #@+node:ekr.20031218072017.2778:readDelims
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
    #@-node:ekr.20031218072017.2778:readDelims
    #@+node:ekr.20031218072017.2779:readDirective
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
            #@+node:EKR.20040625104908:<< handle @language >>
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
            #@-node:EKR.20040625104908:<< handle @language >>
            #@nl
        elif g.match_word(s,i,"@comment"):
            #@        << handle @comment >>
            #@+node:EKR.20040625104908.1:<< handle @comment >>
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
            #@-node:EKR.20040625104908.1:<< handle @comment >>
            #@nl
    
        at.out.append(s2)
    #@nonl
    #@-node:ekr.20031218072017.2779:readDirective
    #@+node:ekr.20031218072017.2780:readNl
    def readNl (self,s,i):
        
        """Handle an @nonl sentinel."""
        
        at = self
        assert(g.match(s,i,"nl"))
        
        if at.inCode:
            at.out.append('\n')
        else:
            at.docOut.append('\n')
    #@nonl
    #@-node:ekr.20031218072017.2780:readNl
    #@+node:ekr.20031218072017.2781:readNonl
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
    #@-node:ekr.20031218072017.2781:readNonl
    #@+node:ekr.20031218072017.2782:readRef
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
    #@-node:ekr.20031218072017.2782:readRef
    #@+node:ekr.20031218072017.2783:readVerbatim
    def readVerbatim (self,s,i):
        
        """Read an @verbatim sentinel."""
        
        at = self
        assert(g.match(s,i,"verbatim"))
        
        # Append the next line to the text.
        s = at.readLine(at.file) 
        i = at.skipIndent(s,0,at.indent)
        at.out.append(s[i:])
    #@nonl
    #@-node:ekr.20031218072017.2783:readVerbatim
    #@-node:ekr.20031218072017.2774:Unpaired sentinels
    #@+node:ekr.20031218072017.2784:badEndSentinel, push/popSentinelStack
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
    #@-node:ekr.20031218072017.2784:badEndSentinel, push/popSentinelStack
    #@-node:ekr.20031218072017.2758:scanText4 & allies
    #@-node:ekr.20031218072017.2756:Reading (4.x)
    #@+node:ekr.20031218072017.2785:Sentinels (4.x)
    #@+node:ekr.20031218072017.2786:nodeSentinelText 4.x
    def nodeSentinelText(self,p):
        
        """Return the text of a @+node or @-node sentinel for p."""
        
        at = self ; h = p.headString()
        #@    << remove comment delims from h if necessary >>
        #@+node:ekr.20031218072017.2787:<< remove comment delims from h if necessary >>
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
        #@-node:ekr.20031218072017.2787:<< remove comment delims from h if necessary >>
        #@nl
        
        if at.thinFile:
            gnx = g.app.nodeIndices.toString(p.v.t.fileIndex)
            return "%s:%s" % (gnx,h)
        else:
            return h
    #@nonl
    #@-node:ekr.20031218072017.2786:nodeSentinelText 4.x
    #@+node:ekr.20031218072017.2788:putLeadInSentinel
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
    #@-node:ekr.20031218072017.2788:putLeadInSentinel
    #@+node:EKR.20040427095028:putCloseNodeSentinel 4.x
    def putCloseNodeSentinel(self,p,inAtAll=False,inAtOthers=False,middle=False):
        
        at = self
        
        s = self.nodeSentinelText(p)
        
        if middle:
            at.putSentinel("@-middle:" + s)
        else:
            at.putSentinel("@-node:" + s)
    #@nonl
    #@-node:EKR.20040427095028:putCloseNodeSentinel 4.x
    #@+node:ekr.20031218072017.2789:putOpenLeoSentinel 4.x
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
    #@-node:ekr.20031218072017.2789:putOpenLeoSentinel 4.x
    #@+node:ekr.20031218072017.2001:putOpenNodeSentinel (sets tnodeList) 4.x
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
    #@-node:ekr.20031218072017.2001:putOpenNodeSentinel (sets tnodeList) 4.x
    #@+node:ekr.20031218072017.2790:putSentinel (applies cweb hack)
    # This method outputs all sentinels.
    
    def putSentinel(self,s):
    
        "Write a sentinel whose text is s, applying the CWEB hack if needed."
        
        at = self
    
        if not at.sentinels:
            return # Handle @file-nosent
    
        at.putIndent(at.indent)
        at.os(at.startSentinelComment)
        #@    << apply the cweb hack to s >>
        #@+node:ekr.20031218072017.2791:<< apply the cweb hack to s >>
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
        #@-node:ekr.20031218072017.2791:<< apply the cweb hack to s >>
        #@nl
        at.os(s)
        if at.endSentinelComment:
            at.os(at.endSentinelComment)
        at.onl()
    #@nonl
    #@-node:ekr.20031218072017.2790:putSentinel (applies cweb hack)
    #@+node:ekr.20031218072017.2793:sentinelKind
    def sentinelKind(self,s):
        
        """Return the kind of sentinel at s."""
        
        at = self
    
        i = g.skip_ws(s,0)
        if g.match(s,i,at.startSentinelComment): 
            i += len(at.startSentinelComment)
        else:
            return noSentinel
    
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
                    return startOthers
                elif g.match(s,j,"<<"):
                    return startRef
                else:
                    # No other sentinels allow whitespace following the '@'
                    return noSentinel
    
        # Do not skip whitespace here!
        if g.match(s,i,"@<<"): return startRef
        if g.match(s,i,"@@"):   return startDirective
        if not g.match(s,i,'@'): return noSentinel
        j = i # start of lookup
        i += 1 # skip the at sign.
        if g.match(s,i,'+') or g.match(s,i,'-'):
            i += 1
        i = g.skip_c_id(s,i)
        key = s[j:i]
        if len(key) > 0 and sentinelDict.has_key(key):
            return sentinelDict[key]
        else:
            return noSentinel
    #@nonl
    #@-node:ekr.20031218072017.2793:sentinelKind
    #@+node:ekr.20031218072017.2792:skipSentinelStart
    def skipSentinelStart(self,s,i):
        
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
    #@-node:ekr.20031218072017.2792:skipSentinelStart
    #@-node:ekr.20031218072017.2785:Sentinels (4.x)
    #@+node:ekr.20031218072017.2111:Writing (4.x)
    #@+node:ekr.20031218072017.2112:Top level
    #@+node:ekr.20031218072017.2113:new_df.closeWriteFile
    # 4.0: Don't use newline-pending logic.
    
    def closeWriteFile (self):
        
        at = self
        if at.outputFile:
            at.outputFile.flush()
            if self.toStringFlag:
                self.stringOutput = self.outputFile.get()
            at.outputFile.close()
            at.outputFile = None
    #@nonl
    #@-node:ekr.20031218072017.2113:new_df.closeWriteFile
    #@+node:ekr.20031218072017.2114:new_df.write
    # This is the entry point to the write code.  root should be an @file vnode.
    
    def write(self,root,nosentinels=False,thinFile=False,toString=False,oneNodeOnly=False):
        
        """Write a 4.x derived file."""
        
        at = self ; c = at.c
    
        #@    << open the file; return on error >>
        #@+node:ekr.20031218072017.2116:<< open the file; return on error >>
        if toString:
            at.targetFileName = "<new_df.write string-file>"
        elif nosentinels:
            at.targetFileName = root.atNoSentFileNodeName()
        elif thinFile:
            at.targetFileName = root.atThinFileNodeName()
        else:
            at.targetFileName = root.atFileNodeName()
            
        ok = at.openWriteFile(root,toString)
            
        if not ok:
            return
        #@nonl
        #@-node:ekr.20031218072017.2116:<< open the file; return on error >>
        #@nl
        try:
            self.writeOpenFile(root,nosentinels,thinFile,toString,oneNodeOnly)
            if toString:
                at.closeWriteFile()
                # Major bug: failure to clear this wipes out headlines!
                # Minor bug: sometimes this causes slight problems...
                at.root.v.t.tnodeList = [] 
            else:
                at.closeWriteFile()
                #@            << set dirty and orphan bits on error >>
                #@+node:ekr.20031218072017.2121:<< set dirty and orphan bits on error >>
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
                #@-node:ekr.20031218072017.2121:<< set dirty and orphan bits on error >>
                #@nl
        except:
            if toString:
                g.es("exception preprocessing script",color="blue")
                g.es_exception(full=False)
                at.root.v.t.tnodeList = []
            else:
                at.handleWriteException() # Sets dirty and orphan bits.
    #@nonl
    #@-node:ekr.20031218072017.2114:new_df.write
    #@+node:EKR.20040506075328:new_df.writeOpenFile
    def writeOpenFile(self,root,nosentinels=False,thinFile=False,toString=False,oneNodeOnly=False):
        
        at = self ; c = at.c
        
        #@    << init atFile ivars for writing >>
        #@+node:EKR.20040506075328.1:<< init atFile ivars for writing >>
        # Set flags telling what kind of writing we are doing.
        at.sentinels = not nosentinels
        at.thinFile = thinFile
        at.raw = False
        assert(at.toStringFlag == toString) # Must have been set earlier.
        
        # Init other ivars.
        at.errors = 0
        c.setIvarsFromPrefs()
        at.root = root
        at.root.v.t.tnodeList = []
        
        c.endEditing() # Capture the current headline.
        #@nonl
        #@-node:EKR.20040506075328.1:<< init atFile ivars for writing >>
        #@nl
        root.clearAllVisitedInTree() # Clear both vnode and tnode bits.
        root.clearVisitedInTree()
    
        #@    << put all @first lines in root >>
        #@+node:ekr.20031218072017.2118:<< put all @first lines in root >> (4.x)
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
            self.os(line) ; self.onl()
            i = g.skip_nl(s,i)
        #@nonl
        #@-node:ekr.20031218072017.2118:<< put all @first lines in root >> (4.x)
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
        #@+node:ekr.20031218072017.2119:<< put all @last lines in root >> (4.x)
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
                self.os(line[i:])
        #@nonl
        #@-node:ekr.20031218072017.2119:<< put all @last lines in root >> (4.x)
        #@nl
        
        if not toString and not nosentinels:
            at.warnAboutOrphandAndIgnoredNodes()
    #@nonl
    #@-node:EKR.20040506075328:new_df.writeOpenFile
    #@+node:ekr.20031218072017.2122:new_df.norefWrite
    def norefWrite(self,root,toString=False):
    
        at = self
    
        c = at.c ; at.root = root
        at.errors = 0
        at.root.t.tnodeList = [] # 9/26/03: after beta 1 release.
        at.sentinels = True # 10/1/03
        at.thinFile = False # 5/17/04
        c.endEditing() # Capture the current headline.
        try:
            at.targetFileName = root.atNorefFileNodeName()
            ok = at.openWriteFile(root,toString)
            if not ok: return
            #@        << write root's tree >>
            #@+node:ekr.20031218072017.2123:<< write root's tree >>
            #@<< put all @first lines in root >>
            #@+node:ekr.20031218072017.2124:<< put all @first lines in root >>
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
            #@-node:ekr.20031218072017.2124:<< put all @first lines in root >>
            #@nl
            at.putOpenLeoSentinel("@+leo-ver=4")
            #@<< put optional @comment sentinel lines >>
            #@+node:ekr.20031218072017.2125:<< put optional @comment sentinel lines >>
            s2 = g.app.config.output_initial_comment
            if s2:
                lines = string.split(s2,"\\n")
                for line in lines:
                    line = line.replace("@date",time.asctime())
                    if len(line)> 0:
                        at.putSentinel("@comment " + line)
            #@-node:ekr.20031218072017.2125:<< put optional @comment sentinel lines >>
            #@nl
            
            for p in root.self_and_subtree_iter():
                #@    << Write p's node >>
                #@+node:ekr.20031218072017.2126:<< Write p's node >>
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
                #@-node:ekr.20031218072017.2126:<< Write p's node >>
                #@nl
            
            at.putSentinel("@-leo")
            #@<< put all @last lines in root >>
            #@+node:ekr.20031218072017.2127:<< put all @last lines in root >>
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
            #@-node:ekr.20031218072017.2127:<< put all @last lines in root >>
            #@nl
            #@nonl
            #@-node:ekr.20031218072017.2123:<< write root's tree >>
            #@nl
            at.closeWriteFile()
            at.replaceTargetFileIfDifferent()
            root.clearOrphan() ; root.clearDirty()
        except:
            at.handleWriteException(root)
            
    rawWrite = norefWrite
    #@-node:ekr.20031218072017.2122:new_df.norefWrite
    #@-node:ekr.20031218072017.2112:Top level
    #@+node:ekr.20031218072017.2128:putBody (4.x)
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
        #@+node:EKR.20040429084140:<< Make sure all lines end in a newline >>
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
        #@-node:EKR.20040429084140:<< Make sure all lines end in a newline >>
        #@nl
        i = 0
        while i < len(s):
            next_i = g.skip_line(s,i)
            assert(next_i > i)
            kind = at.directiveKind(s,i)
            #@        << handle line at s[i] >>
            #@+node:ekr.20031218072017.2129:<< handle line at s[i]  >> (4.x)
            if kind == noDirective:
                if not oneNodeOnly:
                    if inCode:
                        hasRef,n1,n2 = at.findSectionName(s,i)
                        if hasRef and not at.raw:
                            at.putRefLine(s,i,n1,n2,p)
                        else:
                            at.putCodeLine(s,i)
                    else:
                        at.putDocLine(s,i)
            elif kind in (docDirective,atDirective):
                assert(not at.pending)
                at.putStartDocLine(s,i,kind)
                inCode = False
            elif kind in (cDirective,codeDirective):
                # Only @c and @code end a doc part.
                if not inCode:
                    at.putEndDocLine() 
                at.putDirective(s,i)
                inCode = True
            elif kind == allDirective:
                if not oneNodeOnly:
                    if inCode: at.putAtAllLine(s,i,p)
                    else: at.putDocLine(s,i)
            elif kind == othersDirective:
                if not oneNodeOnly:
                    if inCode: at.putAtOthersLine(s,i,p)
                    else: at.putDocLine(s,i) # 12/7/03
            elif kind == rawDirective:
                at.raw = True
                at.putSentinel("@@raw")
            elif kind == endRawDirective:
                at.raw = False
                at.putSentinel("@@end_raw")
                i = g.skip_line(s,i)
            elif kind == miscDirective:
                at.putDirective(s,i)
            else:
                assert(0) # Unknown directive.
            #@nonl
            #@-node:ekr.20031218072017.2129:<< handle line at s[i]  >> (4.x)
            #@nl
            i = next_i
        if not inCode:
            at.putEndDocLine()
        if at.sentinels and not trailingNewlineFlag:
            at.putSentinel("@nonl")
    #@nonl
    #@-node:ekr.20031218072017.2128:putBody (4.x)
    #@+node:ekr.20031218072017.2130:code lines... (4.x)
    #@+node:EKR.20040430081109.1:@all
    #@+node:EKR.20040430080943.1:putAtAllLine
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
    #@-node:EKR.20040430080943.1:putAtAllLine
    #@+node:EKR.20040430104717:putatAllBody
    def putAtAllBody(self,p,putCloseSentinel=True):
        
        """ Generate the body enclosed in sentinel lines."""
    
        at = self ; s = p.bodyString()
        
        p.v.setVisited()   # Make sure v is never expanded again.
        p.v.t.setVisited() # Use the tnode for the orphans check.
        if not at.thinFile and not s: return
        inCode = True
        #@    << Make sure all lines end in a newline >>
        #@+node:EKR.20040430104717.1:<< Make sure all lines end in a newline >>
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
        #@-node:EKR.20040430104717.1:<< Make sure all lines end in a newline >>
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
    #@-node:EKR.20040430104717:putatAllBody
    #@+node:EKR.20040430080943.2:putAtAllChild
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
    #@-node:EKR.20040430080943.2:putAtAllChild
    #@-node:EKR.20040430081109.1:@all
    #@+node:EKR.20040430081109.2:@others
    #@+node:ekr.20031218072017.2131:inAtOthers
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
    #@-node:ekr.20031218072017.2131:inAtOthers
    #@+node:ekr.20031218072017.2132:putAtOthersChild
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
    #@-node:ekr.20031218072017.2132:putAtOthersChild
    #@+node:ekr.20031218072017.2133:putAtOthersLine
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
    #@-node:ekr.20031218072017.2133:putAtOthersLine
    #@-node:EKR.20040430081109.2:@others
    #@+node:ekr.20031218072017.2134:putCodeLine
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
    #@-node:ekr.20031218072017.2134:putCodeLine
    #@+node:ekr.20031218072017.2106:putRefLine & allies
    #@+node:EKR.20040430081109:putRefLine
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
    #@-node:EKR.20040430081109:putRefLine
    #@+node:ekr.20031218072017.2107:putRefAt
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
    #@-node:ekr.20031218072017.2107:putRefAt
    #@+node:ekr.20031218072017.2108:putAfterLastRef
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
    #@-node:ekr.20031218072017.2108:putAfterLastRef
    #@+node:ekr.20031218072017.2109:putAfterMiddleef
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
    #@-node:ekr.20031218072017.2109:putAfterMiddleef
    #@-node:ekr.20031218072017.2106:putRefLine & allies
    #@-node:ekr.20031218072017.2130:code lines... (4.x)
    #@+node:ekr.20031218072017.1745:doc lines... (write)
    #@+node:ekr.20031218072017.1746:putBlankDocLine
    def putBlankDocLine (self):
        
        at = self
        
        at.putPending(split=False)
    
        if not at.endSentinelComment:
            at.putIndent(at.indent)
            at.os(at.startSentinelComment) ; at.oblank()
    
        at.onl()
    #@nonl
    #@-node:ekr.20031218072017.1746:putBlankDocLine
    #@+node:ekr.20031218072017.1747:putStartDocLine
    def putStartDocLine (self,s,i,kind):
        
        """Write the start of a doc part."""
        
        at = self ; at.docKind = kind
        
        sentinel = g.choose(kind == docDirective,"@+doc","@+at")
        directive = g.choose(kind == docDirective,"@doc","@")
        
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
    #@-node:ekr.20031218072017.1747:putStartDocLine
    #@+node:ekr.20031218072017.1748:putDocLine
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
            #@+node:ekr.20031218072017.1749:<< append words to pending line, splitting the line if needed >>
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
            #@-node:ekr.20031218072017.1749:<< append words to pending line, splitting the line if needed >>
            #@nl
    #@-node:ekr.20031218072017.1748:putDocLine
    #@+node:ekr.20031218072017.1750:putEndDocLine
    def putEndDocLine (self):
        
        """Write the conclusion of a doc part."""
        
        at = self
        
        at.putPending(split=False)
        
        # Put the closing delimiter if we are using block comments.
        if at.endSentinelComment:
            at.putIndent(at.indent)
            at.os(at.endSentinelComment)
            at.onl() # Note: no trailing whitespace.
    
        sentinel = g.choose(at.docKind == docDirective,"@-doc","@-at")
        at.putSentinel(sentinel)
    #@nonl
    #@-node:ekr.20031218072017.1750:putEndDocLine
    #@+node:ekr.20031218072017.1751:putPending
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
    #@-node:ekr.20031218072017.1751:putPending
    #@-node:ekr.20031218072017.1745:doc lines... (write)
    #@+node:ekr.20031218072017.2135:Writing Utils...
    #@+node:ekr.20031218072017.2136:directiveKind (4.x)
    # Returns the kind of at-directive or noDirective.
    
    def directiveKind(self,s,i):
    
        at = self
        n = len(s)
        if i >= n or s[i] != '@':
            j = g.skip_ws(s,i)
            if g.match_word(s,j,"@others"):
                return othersDirective
            elif g.match_word(s,j,"@all"):
                return allDirective
            else:
                return noDirective
    
        table = (
            ("@all",allDirective),
            ("@c",cDirective),
            ("@code",codeDirective),
            ("@doc",docDirective),
            ("@end_raw",endRawDirective),
            ("@others",othersDirective),
            ("@raw",rawDirective))
    
        # This code rarely gets executed, so simple code suffices.
        if i+1 >= n or g.match(s,i,"@ ") or g.match(s,i,"@\t") or g.match(s,i,"@\n"):
            # 10/25/02: @space is not recognized in cweb mode.
            # 11/15/02: Noweb doc parts are _never_ scanned in cweb mode.
            return g.choose(at.language=="cweb",
                noDirective,atDirective)
    
        # 10/28/02: @c and @(nonalpha) are not recognized in cweb mode.
        # We treat @(nonalpha) separately because @ is in the colorizer table.
        if at.language=="cweb" and (
            g.match_word(s,i,"@c") or
            i+1>= n or s[i+1] not in string.ascii_letters):
            return noDirective
    
        for name,directive in table:
            if g.match_word(s,i,name):
                return directive
    
        # 10/14/02: return miscDirective only for real directives.
        for name in leoColor.leoKeywords:
            if g.match_word(s,i,name):
                return miscDirective
    
        return noDirective
    #@nonl
    #@-node:ekr.20031218072017.2136:directiveKind (4.x)
    #@+node:ekr.20031218072017.2137:hasSectionName
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
    #@-node:ekr.20031218072017.2137:hasSectionName
    #@+node:ekr.20031218072017.2138:os and allies
    # Note:  self.outputFile may be either a fileLikeObject or a real file.
    
    #@+node:EKR.20040620094529:oblank, oblanks & otabs
    def oblank(self):
        self.os(' ')
    
    def oblanks (self,n):
        self.os(' ' * abs(n))
        
    def otabs(self,n):
        self.os('\t' * abs(n))
    #@nonl
    #@-node:EKR.20040620094529:oblank, oblanks & otabs
    #@+node:EKR.20040620094529.1:onl & onl_sent
    def onl(self):
        
        """Write a newline to the output stream."""
    
        self.os(self.output_newline)
        
    def onl_sent(self):
        
        """Write a newline to the output stream, provided we are outputting sentinels."""
    
        if self.sentinels:
            self.onl()
    #@nonl
    #@-node:EKR.20040620094529.1:onl & onl_sent
    #@+node:EKR.20040620094529.2:os
    def os (self,s):
        
        """Write a string to the output stream.
        
        All output produced by leoAtFile module goes here."""
        
        if s and self.outputFile:
            try:
                s = g.toEncodedString(s,self.encoding,reportErrors=True)
                self.outputFile.write(s)
            except:
                g.es("exception writing:",s)
                g.es_exception(full=True)
    #@nonl
    #@-node:EKR.20040620094529.2:os
    #@-node:ekr.20031218072017.2138:os and allies
    #@+node:ekr.20031218072017.1921:putDirective  (handles @delims,@comment,@language) 4.x
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
            #@+node:ekr.20031218072017.1922:<< handle @delims >>
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
            #@-node:ekr.20031218072017.1922:<< handle @delims >>
            #@nl
        elif g.match_word(s,k,"@language"):
            #@        << handle @language >>
            #@+node:EKR.20040625103148:<< handle @language >>
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
            #@-node:EKR.20040625103148:<< handle @language >>
            #@nl
        elif g.match_word(s,k,"@comment"):
            #@        << handle @comment >>
            #@+node:EKR.20040625103148.1:<< handle @comment >>
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
            #@-node:EKR.20040625103148.1:<< handle @comment >>
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
    #@-node:ekr.20031218072017.1921:putDirective  (handles @delims,@comment,@language) 4.x
    #@-node:ekr.20031218072017.2135:Writing Utils...
    #@-node:ekr.20031218072017.2111:Writing (4.x)
    #@+node:EKR.20040523104815:scanForClonedSibs
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
    #@-node:EKR.20040523104815:scanForClonedSibs
    #@-others
    #@nonl
    #@-node:ekr.20031218072017.2754:<< class baseNewDerivedFile methods >>
    #@nl

class newDerivedFile(baseNewDerivedFile):
    pass # May be overridden in plugins.
#@nonl
#@-node:ekr.20031218072017.2620:@thin leoAtFile.py 
#@-leo
