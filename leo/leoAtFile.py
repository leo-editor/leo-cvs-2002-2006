#@+leo

#@+node:0::@file leoAtFile.py
#@+body
#@@language python


#@+at
#  Class to read and write @file nodes.
# 
# This code uses readline() to get each line rather than reading the entire file into a buffer.  This is more memory efficient and 
# saves us from having to scan for the end of each line.  The result is cleaner and faster code.  This code also accumulates body 
# text line-by-line rather than character-by-character, a much faster way.

#@-at
#@@c

from leoGlobals import *
from leoUtils import *
import leoNodes, leoPrefs
import filecmp, os, os.path, time, traceback

class atFile:
	
	#@<< atFile constants >>
	#@+node:1::<< atFile constants >>
	#@+body
	# The kind of at_directives.
	
	noDirective		=  1 # not an at-directive.
	delimsDirective =  2 # @delims
	docDirective	=  3 # @doc.
	atDirective		=  4 # @<space> or @<newline>
	codeDirective	=  5 # @code
	cDirective		=  6 # @c<space> or @c<newline>
	othersDirective	=  7 # at-others
	miscDirective	=  8 # All other directive
	
	# The kind of sentinel line.
	noSentinel		=  9 # Not a sentinel
	endAt			= 10 # @-at
	endBody			= 11 # @-body
	endDoc			= 12 # @-doc
	endLeo			= 13 # @-leo
	endNode			= 14 # @-node
	endOthers		= 15 # @-others
	startAt			= 16 # @+at
	startBody		= 17 # @+body
	startDelims		= 18 # @delis
	startDoc		= 19 # @+doc
	startLeo		= 20 # @+leo
	startNode		= 21 # @+node
	startOthers		= 22 # @+others
	startRef		= 23 # @< < ... > >
	startVerbatim	= 24 # @verbatim
	startVerbatimAfterRef = 25 # @verbatimAfterRef
	startDirective	= 26 # @@
	#@-body
	#@-node:1::<< atFile constants >>


	#@+others
	#@+node:2:C=1:atFile ctor
	#@+body
	def __init__(self,theCommander):
	
		# trace("__init__", "atFile.__init__")
		self.commands = theCommander # The commander for the current window.
		self.initIvars()
	
	def initIvars(self):
	
		
		#@<< initialize atFile ivars >>
		#@+node:1::<< initialize atFile ivars >>
		#@+body
		#@+at
		#  errors is the number of errors seen while reading and writing.  structureErrors are errors reported by createNthChild.  
		# If structure errors are found we delete the outline tree and rescan.

		#@-at
		#@@c
		self.errors = 0
		self.structureErrors = 0
		

		#@+at
		#  Initialized by atFile.scanAllDirectives.  8/1/02: set all to None here.

		#@-at
		#@@c
		self.default_directory = None
		self.page_width = None
		self.tab_width  = None
		self.startSentinelComment = None
		self.endSentinelComment = None
		

		#@+at
		#  The files used by the output routines.  When tangling, we first write to a temporary output file.  After tangling is 
		# temporary file.  Otherwise we delete the old target file and rename the temporary file to be the target file.

		#@-at
		#@@c
		self.shortFileName = "" # short version of file name used for messages.
		self.targetFileName = ""
		self.outputFileName = ""
		self.outputFile = None # The temporary output file.
		

		#@+at
		#  The indentation used when outputting section references or at-others sections.  We add the indentation of the line 
		# containing the at-node directive and restore the old value when the
		# expansion is complete.

		#@-at
		#@@c
		self.indent = 0  # The unit of indentation is spaces, not tabs.
		
		# The root of tree being written.
		self.root = None
		
		# Ivars used to suppress newlines between sentinels.
		self.suppress_newlines = true # true: enable suppression of newlines.
		self.newline_pending = false # true: newline is pending on read or write.
		#@-body
		#@-node:1::<< initialize atFile ivars >>
	#@-body
	#@-node:2:C=1:atFile ctor
	#@+node:3::Sentinels
	#@+node:1::nodeSentinelText
	#@+body
	def nodeSentinelText(self,v):
	
		# A hack: zero indicates the root node so scanText won't create a child.
		if v != self.root and v.parent():
			index = v.childIndex() + 1
		else:
			index = 0
		cloneIndex = v.t.cloneIndex
		s = choose(cloneIndex > 0, "C=" + `cloneIndex`, "")
		return `index` + ':' + s + ':' + v.headString()
	#@-body
	#@-node:1::nodeSentinelText
	#@+node:2::putCloseNodeSentinel
	#@+body
	def putCloseNodeSentinel(self,v):
	
		s = self.nodeSentinelText(v)
		self.putSentinel("@-node:" + s)
	#@-body
	#@-node:2::putCloseNodeSentinel
	#@+node:3::putCloseSentinels
	#@+body
	#@+at
	#  root is an ancestor of v, or root == v.  We call putCloseSentinel for v up to, but not including, root.

	#@-at
	#@@c
	def putCloseSentinels(self,root,v):
	
		self.putCloseNodeSentinel(v)
		while 1:
			v = v.parent()
			assert(v) # root must be an ancestor of v.
			if  v == root: break
			self.putCloseNodeSentinel(v)
	#@-body
	#@-node:3::putCloseSentinels
	#@+node:4::putOpenLeoSentinel
	#@+body
	#@+at
	#  This method is the same as putSentinel except we don't put an opening newline and leading whitespace.

	#@-at
	#@@c
	def putOpenLeoSentinel(self,s):
	
		self.os(self.startSentinelComment)
		self.os(s)
		self.os(self.endSentinelComment)
		self.onl() # Ends of sentinel.
	#@-body
	#@-node:4::putOpenLeoSentinel
	#@+node:5::putOpenNodeSentinel
	#@+body
	#@+at
	#  This method puts an open node sentinel for node v.

	#@-at
	#@@c
	def putOpenNodeSentinel(self,v):
	
		if v.isAtFileNode() and v != self.root:
			self.writeError("@file not valid in: " + v.headString())
		else:
			s = self.nodeSentinelText(v)
			self.putSentinel("@+node:" + s)
	#@-body
	#@-node:5::putOpenNodeSentinel
	#@+node:6::putOpenSentinels
	#@+body
	#@+at
	#  root is an ancestor of v, or root == v.  We call putOpenNodeSentinel on all the descendents of root which are the ancestors 
	# of v.

	#@-at
	#@@c
	def putOpenSentinels(self,root,v):
	
		last = root
		while last != v:
			# Set node to v or the ancestor of v that is a child of last.
			node = v
			while node and node.parent() != last:
				node = node.parent()
			assert(node)
			self.putOpenNodeSentinel(node)
			last = node
	#@-body
	#@-node:6::putOpenSentinels
	#@+node:7:C=2:putSentinel
	#@+body
	#@+at
	#  All sentinels are eventually output by this method.
	# 
	# Sentinels include both the preceding and following newlines. This rule greatly simplies the code and has several important benefits:
	# 
	# 1. Callers never have to generate newlines before or after sentinels.  Similarly, routines that expand code and doc parts 
	# never have to add "extra" newlines.
	# 2. There is no need for a "no-newline" directive.  If text follows a section reference, it will appear just after the 
	# newline that ends sentinel at the end of the expansion of the reference.  If no significant text follows a reference, there 
	# will be two newlines following the ending sentinel.
	# 
	# The only exception is that no newline is required before the opening "leo" sentinel. The putLeoSentinel and isLeoSentinel 
	# routines handle this minor exception.

	#@-at
	#@@c
	def putSentinel(self,s):
	
		self.newline_pending = false # discard any pending newline.
		self.onl() ; self.putIndent(self.indent) # Start of sentinel.
		self.os(self.startSentinelComment)
		self.os(s)
		self.os(self.endSentinelComment)
		if self.suppress_newlines:
			self.newline_pending = true # Schedule a newline.
		else:
			self.onl() # End of sentinel.
	#@-body
	#@-node:7:C=2:putSentinel
	#@+node:8:C=3:sentinelKind
	#@+body
	#@+at
	#  This method tells what kind of sentinel appears in line s.  Typically s will be an empty line before the actual sentinel, 
	# but it is also valid for s to be an actual sentinel line.
	# 
	# Returns (kind, s, emptyFlag), where emptyFlag is true if kind == noSentinel and s was an empty line on entry.

	#@-at
	#@@c
	
	sentinelDict = {
		"@verbatim": startVerbatim,
		"@verbatimAfterRef": startVerbatimAfterRef,
		"@+at": startAt, "@-at": endAt,
		"@+body": startBody, "@-body": endBody,
		"@+doc": startDoc, "@-doc": endDoc,
		"@+leo": startLeo, "@-leo": endLeo,
		"@+node": startNode, "@-node": endNode,
		"@+others": startOthers, "@-others": endOthers }
	
	def sentinelKind(self,s):
	
		i = skip_ws(s,0)
		if match(s,i,self.startSentinelComment): 
			i += len(self.startSentinelComment)
		else:
			return atFile.noSentinel
		# Do not skip whitespace here!
		if match(s,i,"@<<"): return atFile.startRef
		if match(s,i,"@@"): return atFile.startDirective
		if not match(s,i,'@'): return atFile.noSentinel
		j = i # start of lookup
		i += 1 # skip the at sign.
		if match(s,i,'+') or match(s,i,'-'):
			i += 1
		i = skip_c_id(s,i)
		# trace(`s[j:i]`)
		key = s[j:i]
		if len(key) > 0 and atFile.sentinelDict.has_key(key):
			return atFile.sentinelDict[key]
		else:
			return atFile.noSentinel
	#@-body
	#@-node:8:C=3:sentinelKind
	#@+node:9::sentinelName
	#@+body
	# Returns the name of the sentinel for warnings.
	
	sentinelNameDict = {
		endAt: "@-at", endBody: "@-body",
		endDoc: "@-body", endLeo: "@-leo",
		endNode: "@-node", endOthers: "@-others",
		noSentinel: "<no sentinel>",
		startAt: "@+at", startBody: "@+body",
		startDirective: "@@", startDoc: "@+doc",
		startLeo: "@+leo", startNode: "@+node",
	 	startOthers: "@+others", startVerbatim: "@verbatim" }
	
	def sentinelName(self, kind):
		if atFile.sentinelNameDict.has_key(kind):
			return atFile.sentinelNameDict[kind]
		else:
			return "<unknown sentinel!>"
	#@-body
	#@-node:9::sentinelName
	#@+node:10::skipSentinelStart
	#@+body
	def skipSentinelStart(self,s,i):
	
		if is_nl(s,i): i = skip_nl(s,i)
		i = skip_ws(s,i)
		assert(match(s,i,self.startSentinelComment))
		i += len(self.startSentinelComment)
		# 7/8/02: Support for REM hack
		i = skip_ws(s,i)
		assert(i < len(s) and s[i] == '@')
		return i + 1
	#@-body
	#@-node:10::skipSentinelStart
	#@-node:3::Sentinels
	#@+node:4::Utilites
	#@+node:1:C=4:atFile.scanAllDirectives (calls writeError on errors)
	#@+body
	#@+at
	#  This code scans the node v and all of v's ancestors looking for directives.  If found, the corresponding Tangle/Untangle 
	# globals are set.
	# 
	# Once a directive is seen, no other related directives in nodes further up the tree have any effect.  For example, if an 
	# @color directive is seen in node x, no @color or @nocolor directives are examined in any ancestor of x.
	# 
	# This code is similar to Commands::scanAllDirectives, but it has been modified for use by the atFile class.

	#@-at
	#@@c
	
	def btest(self, b1, b2):
		return (b1 & b2) != 0
	
	def scanAllDirectives(self,v):
	
		c = self.commands
		bits = 0 ; old_bits = 0 ; val = 0
		
		#@<< Set ivars >>
		#@+node:1:C=5:<< Set ivars >>
		#@+body
		self.page_width = self.commands.page_width
		self.tab_width  = self.commands.tab_width
		
		self.default_directory = None # 8/2: will be set later.
		
		
		path_directory = None # 8/13: set when @file contains a path, possibly a partial path.
		
		delim1, delim2, delim3 = set_delims_from_language(c.target_language)
		#@-body
		#@-node:1:C=5:<< Set ivars >>

		
		#@<< Set path from @file node >>
		#@+node:2::<< Set path from @file node >>
		#@+body
		# An absolute path in an @file node over-rides everything else.
		# A relative path gets appended to the relative path by the open logic.
		
		name = v.atFileNodeName()
		dir = os.path.dirname(name)
		if dir and len(dir) > 0 and os.path.isabs(dir):
			if os.path.exists(dir):
				self.default_directory = dir
			else:
				self.error("Directory \"" + dir + "\" does not exist")
		#@-body
		#@-node:2::<< Set path from @file node >>

		while v:
			s = v.t.bodyString
			bits, dict = is_special_bits(s)
			
			#@<< Test for @path >>
			#@+node:4::<< Test for @path >>
			#@+body
			# We set the current director to a path so future writes will go to that directory.
			
			loadDir = app().loadDir
			
			if self.btest(path_bits, bits) and not self.default_directory and not self.btest(path_bits, old_bits):
				k = dict["path"]
				j = i = k + len("@path")
				i = skip_to_end_of_line(s,i)
				path = string.strip(s[j:i])
				# es(ftag + " path: " + path)
				# Remove leading and trailing delims if they exist.
				if len(path) > 2 and (
					(path[0]=='<' and path[-1] == '>') or
					(path[0]=='"' and path[-1] == '"') ):
					path = path[1:-1]
				path = string.strip(path)
				path = os.path.join(loadDir,path)
				if path and len(path) > 0:
					if os.path.isabs(path):
						if os.path.exists(path):
							self.default_directory = path
						else:
							self.error("invalid @path: " + path)
					else:
						self.error("ignoring relative @path: " + path)
				else:
					self.error("ignoring empty @path")
			#@-body
			#@-node:4::<< Test for @path >>

			
			#@<< Test for @comment or @language >>
			#@+node:3::<< Test for @comment or @language >>
			#@+body
			if self.btest(comment_bits, old_bits) or self.btest(language_bits, old_bits):
				pass # Do nothing more.
			
			elif self.btest(comment_bits, bits):
				k = dict["comment"] # 7/8/02, not "language!"
				d1, d2, d3 = set_delims_from_string(s[k:])
				if delim1:
					# @comment effectively disables Untangle.
					delim1, delim2, delim3 = d1, d2, d3
				
			elif self.btest(language_bits, bits):
				k = dict["language"]
				issue_error_flag = false
				language, d1, d2, d3 = set_language(s,k,issue_error_flag)
				# print `delim1`,`delim2`,`delim3`
				if delim1:
					delim1, delim2, delim3 = d1, d2, d3
			#@-body
			#@-node:3::<< Test for @comment or @language >>

			
			#@<< Test for @pagewidth and @tabwidth >>
			#@+node:5:C=6:<< Test for @pagewidth and @tabwidth >>
			#@+body
			if self.btest(page_width_bits, bits) and not self.btest(page_width_bits, old_bits):
				k = dict["page_width"]
				j = i = k + len("@pagewidth")
				i, val = skip_long(s,i)
				if val != None and val > 0:
					self.page_width = val
				else:
					i = skip_to_end_of_line(s,i)
					self.error("Ignoring " + s[k:i])
			
			if self.btest(tab_width_bits, bits) and not self.btest(tab_width_bits, old_bits):
				k = dict["tab_width"]
				j = i = k + len("@tabwidth")
				i, val = skip_long(s, i)
				if val != None and val != 0:
					self.tab_width = val
				else:
					i = skip_to_end_of_line(s,i)
					self.error("Ignoring " + s[k:i])
			#@-body
			#@-node:5:C=6:<< Test for @pagewidth and @tabwidth >>

			old_bits |= bits
			v = v.parent()
		
		#@<< Set current directory >>
		#@+node:6::<< Set current directory >>
		#@+body
		# This code is executed if no valid absolute path was specified in the @file node or in an @path directive.
		
		if c.frame and not self.default_directory:
			for dir in (c.tangle_directory,c.frame.openDirectory,c.openDirectory):
				if dir and len(dir) > 0 and os.path.isabs(dir) and os.path.exists(dir):
					self.default_directory = dir ; break
		
		if not self.default_directory:
			# This should never happen: c.openDirectory should be a good last resort.
			self.error("No absolute directory specified anywhere.")
			self.default_directory = ""

		#@-body
		#@-node:6::<< Set current directory >>

		
		#@<< Set comment Strings from delims >>
		#@+node:7::<< Set comment Strings from delims >>
		#@+body
		# Use single-line comments if we have a choice.
		# 8/2/01: delim1,delim2,delim3 now correspond to line,start,end
		if delim1:
			self.startSentinelComment = delim1
			self.endSentinelComment = "" # Must not be None.
		elif delim2 and delim3:
			self.startSentinelComment = delim2
			self.endSentinelComment = delim3
		else: # Emergency!
			assert(0)
			self.startSentinelComment = "#" # This should never happen!
			self.endSentinelComment = ""
		#@-body
		#@-node:7::<< Set comment Strings from delims >>
	#@-body
	#@-node:1:C=4:atFile.scanAllDirectives (calls writeError on errors)
	#@+node:2::directiveKind
	#@+body
	# Returns the kind of at-directive or noDirective.
	
	def directiveKind(self,s,i):
	
		n = len(s)
		if i >= n or s[i] != '@':
			return atFile.noDirective
		# This code rarely gets executed, so simple code suffices.
		if i+1 >= n or match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@\n"):
			return atFile.atDirective
		if match_word(s,i,"@c"):
			return atFile.cDirective
		elif match_word(s,i,"@code"):
			return atFile.codeDirective
		elif match_word(s,i,"@doc"):
			return atFile.docDirective
		elif match_word(s,i,"@others"):
			return atFile.othersDirective
		else:
			return atFile.miscDirective
	#@-body
	#@-node:2::directiveKind
	#@+node:3::error
	#@+body
	def error(self,message):
	
		es(message)
		self.errors += 1
	#@-body
	#@-node:3::error
	#@+node:4::skipIndent
	#@+body
	# Skip past whitespace equivalent to width spaces.
	
	def skipIndent(self,s,i,width):
	
		ws = 0 ; n = len(s)
		while i < n and ws < width:
			if   s[i] == '\t': ws += (abs(self.tab_width) - (ws % abs(self.tab_width)))
			elif s[i] == ' ':  ws += 1
			else: break
			i += 1
		return i
	#@-body
	#@-node:4::skipIndent
	#@+node:5::readError
	#@+body
	def readError(self,message):
	
		if 0: # This is more irritating than useful.
			if self.errors == 0:
				es("----- error reading @file " + self.targetFileName)
		self.error(message)
		self.root.setOrphan()
		self.root.setDirty()
	#@-body
	#@-node:5::readError
	#@+node:6::updateCloneIndices
	#@+body
	#@+at
	#  The new Leo2 computes clone indices differently from the old Leo2:
	# 
	# 1. The new Leo2 recomputes clone indices for every write.
	# 2. The new Leo2 forces the clone index of the @file node to be zero.
	# 
	# Also, the read logic ignores the clone index of @file nodes, thereby ensuring that we don't mistakenly join an @file node to 
	# another node.

	#@-at
	#@@c
	def updateCloneIndices(self,root,next):
	
		if root.isCloned():
			self.error("ignoring clone mark for " + root.headString())
			root.t.setCloneIndex(0)
		index = 0
		# 12/17/01: increment each cloneIndex at most once.
		v = root
		while v and v != next:
			v.t.cloneIndex = 0
			v = v.threadNext()
		v = root
		while v and v != next:
			vIs = v.isCloned()
			vShould = v.shouldBeClone() #verbose
			if 0: # vIs or vShould:
				es("update:"+`index`+" is:"+`vIs`+" should:"+`vShould`+`v`) ; enl()
			if v.t.cloneIndex == 0 and vIs and vShould:
				index += 1
				v.t.cloneIndex = index
			v = v.threadNext()
		# Make sure the root's clone index is zero.
		root.t.setCloneIndex(0)
	#@-body
	#@-node:6::updateCloneIndices
	#@+node:7::writeError
	#@+body
	def writeError(self,message):
	
		if self.errors == 0:
			es("errors writing: " + self.targetFileName)
		self.error(message)
		self.root.setOrphan()
		self.root.setDirty()
	#@-body
	#@-node:7::writeError
	#@-node:4::Utilites
	#@+node:5::Reading
	#@+node:1::createNthChild
	#@+body
	#@+at
	#  Sections appear in the derived file in reference order, not tree order.  Therefore, when we insert the nth child of the 
	# parent there is no guarantee that the previous n-1 children have already been inserted. And it won't work just to insert the 
	# nth child as the last child if there aren't n-1 previous siblings.  For example, if we insert the third child followed by 
	# the second child followed by the first child the second and third children will be out of order.
	# 
	# To ensure that nodes are placed in the correct location we create "dummy" children as needed as placeholders.  In the 
	# example above, we would insert two dummy children when inserting the third child.  When inserting the other two children we 
	# replace the previously inserted dummy child with the actual children.
	# 
	# vnode child indices are zero-based.  Here we use 1-based indices.
	# 
	# With the "mirroring" scheme it is a structure error if we ever have to create dummy vnodes.  Such structure errors cause a 
	# second pass to be made, with an empty root.  This second pass will generate other structure errors, which are ignored.

	#@-at
	#@@c
	def createNthChild(self,n,parent,headline):
	
		assert(n > 0)
	
		# Create any needed dummy children.
		dummies = n - parent.numberOfChildren() - 1
		if dummies > 0:
			es("dummy created")
			self.structureErrors += 1
		while dummies > 0:
			dummies -= 1
			dummy = parent.insertAsLastChild(leoNodes.tnode())
			# The user should never see this headline.
			dummy.initHeadString("Dummy")
	
		if n <= parent.numberOfChildren():
			result = parent.nthChild(n-1)
			resulthead = result.headString()
			if string.strip(headline) != string.strip(resulthead):
				es("headline mismatch:")
				es("head1:" + `string.strip(headline)`)
				es("head2:" + `string.strip(resulthead)`)
				self.structureErrors += 1
		else:
			# This is using a dummy; we should already have bumped structureErrors.
			result = parent.insertAsLastChild(leoNodes.tnode())
		result.initHeadString(headline)
		
		result.setVisited() # Suppress all other errors for this node.
		return result
	#@-body
	#@-node:1::createNthChild
	#@+node:2::joinTrees
	#@+body
	#@+at
	#  This function joins all nodes in the two trees which should have the same topology. This code makes no other assumptions 
	# about the two trees; some or all of the nodes may already have been joined.
	# 
	# There are several differences between this method and the similar vnode:joinTreeTo method.  First, we can not assert that 
	# the two trees have the same topology because the derived file could have been edited outside of Leo.  Second, this method 
	# also merges the tnodes of all joined nodes.

	#@-at
	#@@c
	def joinTrees(self,tree1,tree2):
	
		assert(tree1 and tree2)
		# Use a common tnode for both nodes.
		if tree1.t != tree2.t:
			tree1.setT(tree2.t)
		# Join the roots using the vnode class.
		tree1.joinNodeTo(tree2)
		# Recursively join all subtrees.
		child1 = tree1.firstChild()
		child2 = tree2.firstChild()
		while child1 and child2:
			self.joinTrees(child1, child2)
			child1 = child1.next()
			child2 = child2.next()
		if child1 or child2:
			self.readError("cloned nodes have different topologies")
	#@-body
	#@-node:2::joinTrees
	#@+node:3:C=7:atFile.read
	#@+body
	#@+at
	#  This is the entry point to the read code.  The root vnode should be an @file node.  If doErrorRecoveryFlag is false we are 
	# doing an update.  In that case it would be very unwise to do any error recovery which might clear clone links.  If 
	# doErrorRecoveryFlag is true and there are structure errors during the first pass we delete root's children and its body 
	# text, then rescan.  All other errors indicate potentially serious problems with sentinels.
	# 
	# The caller has enclosed this code in beginUpdate/endUpdate.

	#@-at
	#@@c
	def read(self,root):
	
		t1 = getTime()
		c = self.commands
		root.clearVisitedInTree() # Clear the list of nodes for orphans logic.
		self.targetFileName = root.atFileNodeName()
		self.root = root
		self.errors = self.structureErrors = 0
		
		#@<< open file >>
		#@+node:1::<< open file >>
		#@+body
		self.scanAllDirectives(root) # 1/30/02
		
		if not self.targetFileName or len(self.targetFileName) == 0:
			self.readError("Missing file name.  Restoring @file tree from .leo file.")
		else:
			# print `self.default_directory`, `self.targetFileName`
			fn = os.path.join(self.default_directory, self.targetFileName)
			fn = os.path.normpath(fn)
			try:
				file = open(fn,'r')
				if file:
					
					#@<< warn on read-only file >>
					#@+node:1::<< warn on read-only file >>
					#@+body
					# 8/13/02
					try:
						read_only = not os.access(fn,os.W_OK)
						if read_only:
							es("read only: " + fn)
					except: pass # os.access() may not exist on all platforms.
					#@-body
					#@-node:1::<< warn on read-only file >>

			except:
				self.readError("Can not open: " + '"@file ' + fn + '"')
		#@-body
		#@-node:1::<< open file >>

		if self.errors > 0: return 0
		es("reading: " + root.headString())
		
		#@<< Scan the file buffer >>
		#@+node:2::<< Scan the file buffer  >>
		#@+body
		self.indent = 0
		out = []
		self.scanHeader(file)
		self.scanText(file,root,out,atFile.endLeo)
		s = string.join(out, "")
		# 8/13/02: Remove cursed newlines.
		s = string.replace(s, '\r', '')
		root.setBodyStringOrPane(s)
		#@-body
		#@-node:2::<< Scan the file buffer  >>

		
		#@<< Bump mStructureErrors if any vnodes are unvisited >>
		#@+node:3::<< Bump mStructureErrors if any vnodes are unvisited >>
		#@+body
		#@+at
		#  createNthNode marks all nodes in the derived file as visited.  Any unvisited nodes are either dummies or nodes that 
		# don't exist in the derived file.

		#@-at
		#@@c
		
		next = root.nodeAfterTree()
		v = root.threadNext()
		while v and v != next:
			if not v.isVisited():
				es("unvisited node: " + v.headString())
				self.structureErrors += 1
			v = v.threadNext()

		#@-body
		#@-node:3::<< Bump mStructureErrors if any vnodes are unvisited >>

		next = root.nodeAfterTree()
		if self.structureErrors > 0:
			self.readError("-- Rereading file.  Clone links into this file will be lost.") ;
			self.errors = 0
			root.clearVisitedInTree() # Clear the list of nodes for orphans logic.
			
			#@<< Delete root's tree and body text >>
			#@+node:4::<< Delete root's tree and body text >>
			#@+body
			while root.firstChild():
				root.firstChild().doDelete(root)
			
			root.setBodyStringOrPane("")
			#@-body
			#@-node:4::<< Delete root's tree and body text >>

			file.seek(0)
			
			#@<< Scan the file buffer >>
			#@+node:2::<< Scan the file buffer  >>
			#@+body
			self.indent = 0
			out = []
			self.scanHeader(file)
			self.scanText(file,root,out,atFile.endLeo)
			s = string.join(out, "")
			# 8/13/02: Remove cursed newlines.
			s = string.replace(s, '\r', '')
			root.setBodyStringOrPane(s)
			#@-body
			#@-node:2::<< Scan the file buffer  >>

		file.close()
		if self.errors == 0:
			next = root.nodeAfterTree()
			root.clearAllVisitedInTree()
			
			#@<< Handle clone bits >>
			#@+node:5::<< Handle clone bits >>
			#@+body
			h = {}
			v = root
			while v and v != next:
				cloneIndex = v.t.cloneIndex
				# new Leo2: we skip the root node: @file nodes can not be cloned.
				if cloneIndex > 0 and v != root:
					if h.has_key(cloneIndex):
						t = h[cloneIndex]
						# v is a clone: share the previous tnode.
						v.setT(t)
						t.setVisited() # We will mark these clones later.
					else: h[cloneIndex] = v.t
				v = v.threadNext()
			
			# Set clone marks for all visited tnodes.
			v = root
			while v and v != next:
				if v.t.isVisited():
					if v == root:
						pass
					elif v.shouldBeClone():
						v.initClonedBit(true)
					else:
						# Not a serious error.
						es("clone links cleared for: " + v.headString())
						v.unjoinTree();
						t.setCloneIndex(0) # t is no longer cloned.
				v = v.threadNext()
			#@-body
			#@-node:5::<< Handle clone bits >>

			
			#@<< Join cloned trees >>
			#@+node:6::<< Join cloned trees >>
			#@+body
			#@+at
			#  In most cases, this code is not needed, because the outline already has been read and nodes joined.  However, there 
			# could be problems on read errors, so we also join nodes here.

			#@-at
			#@@c
			
			h = {}
			v = root
			while v and v != next:
				cloneIndex = v.t.cloneIndex
				# new Leo2: we skip the root node: @file nodes can not be cloned.
				if cloneIndex > 0 and v != root:
					if h.has_key(cloneIndex):
						clone = h[cloneIndex]
						if v.headString() == clone.headString():
							self.joinTrees(clone,v)
						else:
							# An extremely serious error.  Data may be lost.
							self.readError(
								"Outline corrupted: " +
								"different nodes have same clone index!\n\t" +
								v.headString() + "\n\t" + clone.headString())
					# Enter v so we can join the next clone to it.
					# The next call to lookup will find this v, not the previous.
					h[cloneIndex] = v
				v = v.threadNext()
			#@-body
			#@-node:6::<< Join cloned trees >>

			
			#@<< Handle all status bits >>
			#@+node:7::<< Handle all status bits >>
			#@+body
			current = None
			v = root
			while v and v != next:
				if v.isSelected():
					self.commands.tree.currentVnode = current = v
				if v.isTopBitSet():
					# Just tell the open code we have seen the top vnode.
					self.commands.tree.topVnode = v ;
				v = v.threadNext()
			
			if current:
				# Indicate what the current node will be.
				c.tree.currentVnode = current

			#@-body
			#@-node:7::<< Handle all status bits >>

		if self.errors > 0:
			# A serious error has occured that has not been corrected.
			self.readError("----- File may have damaged sentinels!")
			root.unjoinTree();
		else: root.clearDirty()
		# esDiffTime("read: exit", t1)
		return self.errors == 0
	#@-body
	#@-node:3:C=7:atFile.read
	#@+node:4::readAll (Leo2)
	#@+body
	#@+at
	#  This method scans all vnodes, calling read for every @file node found.  v should point to the root of the entire tree on entry.
	# 
	# Bug fix: 9/19/01 This routine clears all orphan status bits, so we must set the dirty bit of orphan @file nodes to force the 
	# writing of those nodes on saves.  If we didn't do this, a _second_ save of the .leo file would effectively wipe out bad 
	# @file nodes!
	# 
	# 10/19/01: With the "new" Leo2 there are no such problems, and setting the dirty bit here is still correct.

	#@-at
	#@@c
	
	def readAll(self,root,partialFlag):
	
		c = self.commands
		c.endEditing() # Capture the current headline.
		anyRead = false
		self.initIvars()
		v = root
		if partialFlag: after = v.nodeAfterTree()
		else: after = None
		while v and v != after:
			if v.isAtIgnoreNode():
				v = v.nodeAfterTree()
			elif v.isAtFileNode():
				anyRead = true
				if partialFlag:
					# We are forcing the read.
					self.read(v)
				else:
					# f v is an orphan, we don't expect to see a derived file,
					# and we shall read a derived file if it exists.
					wasOrphan = v.isOrphan()
					ok = self.read(v)
					if wasOrphan and not ok:
						# Remind the user to fix the problem.
						v.setDirty()
						c.setChanged(true)
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		# Clear all orphan bits.
		v = root
		while v:
			v.clearOrphan()
			v = v.threadNext()
			
		if partialFlag and not anyRead:
			es("no @file nodes in the selected tree")
	#@-body
	#@-node:4::readAll (Leo2)
	#@+node:5::scanDoc
	#@+body
	# Scans the doc part and appends the text out.
	# s,i point to the present line on entry.
	
	def scanDoc(self,file,s,i,out,kind):
	
		endKind = choose(kind == atFile.startDoc, atFile.endDoc, atFile.endAt)
		single = len(self.endSentinelComment) == 0
		
		#@<< Skip the opening sentinel >>
		#@+node:1::<< Skip the opening sentinel >>
		#@+body
		assert(match(s,i,choose(kind == atFile.startDoc, "+doc", "+at")))
		
		out.append(choose(kind == atFile.startDoc, "@doc", "@"))
		s = file.readline()

		#@-body
		#@-node:1::<< Skip the opening sentinel >>

		
		#@<< Skip an opening block delim >>
		#@+node:2::<< Skip an opening block delim >>
		#@+body
		if not single:
			j = skip_ws(s,0)
			if match(s,j,self.startSentinelComment):
				s = file.readline()
		#@-body
		#@-node:2::<< Skip an opening block delim >>

		nextLine = None ; kind = atFile.noSentinel
		while len(s) > 0:
			
			#@<< set kind, nextLine >>
			#@+node:3::<< set kind, nextLine >>
			#@+body
			#@+at
			#  For non-sentinel lines we look ahead to see whether the next line is a sentinel.

			#@-at
			#@@c
			
			assert(nextLine==None)
			
			kind = self.sentinelKind(s)
			
			if kind == atFile.noSentinel:
				j = skip_ws(s,0)
				blankLine = s[j] == '\n'
				nextLine = file.readline()
				nextKind = self.sentinelKind(nextLine)
				if blankLine and nextKind == endKind:
					kind = endKind # stop the scan now

			#@-body
			#@-node:3::<< set kind, nextLine >>

			if kind == endKind: break
			
			#@<< Skip the leading stuff >>
			#@+node:4::<< Skip the leading stuff >>
			#@+body
			# Point i to the start of the real line.
			
			if single: # Skip the opening comment delim and a blank.
				i = skip_ws(s,0)
				if match(s,i,self.startSentinelComment):
					i += len(self.startSentinelComment)
					if match(s,i," "): i += 1
			else:
				i = self.skipIndent(s,0, self.indent)

			#@-body
			#@-node:4::<< Skip the leading stuff >>

			
			#@<< Append s to out >>
			#@+node:5::<< Append s to out >>
			#@+body
			# Append the line with a newline if it is real
			
			line = s[i:-1] # remove newline for rstrip.
			
			if line == string.rstrip(line):
				# no trailing whitespace: the newline is real.
				out.append(line + '\n')
			else:
				# trailing whitespace: the newline is not real.
				out.append(line)

			#@-body
			#@-node:5::<< Append s to out >>

			if nextLine:
				s = nextLine ; nextLine = None
			else: s = file.readline()
		if kind != endKind:
			self.readError("Missing " + self.sentinelName(endKind) + " sentinel")
		
		#@<< Remove a closing block delim from out >>
		#@+node:6::<< Remove a closing block delim from out >>
		#@+body
		# This code will typically only be executed for HTML files.
		
		if 0: ## must be rewritten
			if not single:
				# Remove the ending block delimiter.
				delim = list('\n' + self.endSentinelComment + '\n')
				if out[-len(delim):] == delim:
					# Rewrite the stream.
					out = out[:-len(delim)]
		#@-body
		#@-node:6::<< Remove a closing block delim from out >>
	#@-body
	#@-node:5::scanDoc
	#@+node:6:C=8:scanHeader
	#@+body
	#@+at
	#  This method sets self.startSentinelComment and self.endSentinelComment based on the first @+leo sentinel line of the file.  
	# We can not call sentinelKind here because that depends on the comment delimiters we set here.  @first lines are written 
	# "verbatim", so nothing more needs to be done!
	# 
	# 7/8/02: Leading whitespace is now significant here before the @+leo.  This is part of the "REM hack".  We do this so that 
	# sentinelKind need not skip whitespace following self.startSentinelComment.  This is correct: we want to be as restrictive as 
	# possible about what is recognized as a sentinel.  This minimizes false matches.

	#@-at
	#@@c
	def scanHeader(self,file):
	
		valid = true ; tag = "@+leo"
		# Skip any non @+leo lines.
		s = file.readline()
		while len(s) > 0:
			j = string.find(s,tag)
			if j != -1: break
			s = file.readline()
		n = len(s)
		valid = n > 0
		# s contains the tag
		i = j = skip_ws(s,0)
		# The opening comment delim is the initial non-whitespace.
		# 7/8/02: The opening comment delim is the initial non-tag
		while i < n and not match(s,i,tag) and not is_nl(s,i): # and not is_ws(s[i]) :
			i += 1
		if j < i:
			self.startSentinelComment = s[j:i]
		else: valid = false
		# Make sure we have @+leo
		if 0:# 7/8/02: make leading whitespace significant.
			i = skip_ws(s, i)
		if match(s, i, tag):
			i += len(tag)
		else: valid = false
		# The closing comment delim is the trailing non-whitespace.
		i = j = skip_ws(s,i)
		while i < n and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		self.endSentinelComment = s[j:i]
		if not valid:
			self.readError("Bad @+leo sentinel in " + self.targetFileName)
	#@-body
	#@-node:6:C=8:scanHeader
	#@+node:7::scanText
	#@+body
	#@+at
	#  This method is the heart of the new read code.  It reads lines from the file until the given ending sentinel is found, and 
	# warns if any other ending sentinel is found instead.  It calls itself recursively to handle most nested sentinels.
	# 

	#@-at
	#@@c
	def scanText (self,file,v,out,endSentinelKind):
	
		c = self.commands
		lineIndent = 0 ; linep = 0 # Changed only for sentinels.
		nextLine = None
		while 1:
			if nextLine:
				s = nextLine ; nextLine = None
			else:
				s = file.readline()
				if len(s) == 0: break
			# trace(`s`)
			
			#@<< set kind, nextKind >>
			#@+node:1::<< set kind, nextKind >>
			#@+body
			#@+at
			#  For non-sentinel lines we look ahead to see whether the next line is a sentinel.  If so, the newline that ends a 
			# non-sentinel line belongs to the next sentinel.

			#@-at
			#@@c
			
			assert(nextLine==None)
			
			kind = self.sentinelKind(s)
			
			if kind == atFile.noSentinel:
				nextLine = file.readline()
				nextKind = self.sentinelKind(nextLine)
			else:
				nextLine = nextKind = None
			
			# nextLine != None only if we have a non-sentinel line.
			# Therefore, nextLine == None whenever scanText returns.
			#@-body
			#@-node:1::<< set kind, nextKind >>

			if kind != atFile.noSentinel:
				
				#@<< set lineIndent, linep and leading_ws >>
				#@+node:2::<< Set lineIndent, linep and leading_ws >>
				#@+body
				#@+at
				#  lineIndent is the total indentation on a sentinel line.  The first "self.indent" portion of that must be 
				# removed when recreating text.  leading_ws is the remainder of the leading whitespace.  linep points to the first 
				# "real" character of a line, the character following the "indent" whitespace.

				#@-at
				#@@c
				
				# Point linep past the first self.indent whitespace characters.
				linep = self.skipIndent(s,0,self.indent)
				
				# Set lineIndent to the total indentation on the line.
				lineIndent = 0 ; i = 0
				while i < len(s):
					if s[i] == '\t': lineIndent += (abs(self.tab_width) - (lineIndent % abs(self.tab_width)))
					elif s[i] == ' ': lineIndent += 1
					else: break
					i += 1
				# trace("lineIndent:" +`lineIndent` + ", " + `s`)
				
				# Set leading_ws to the additional indentation on the line.
				leading_ws = s[linep:i]
				#@-body
				#@-node:2::<< Set lineIndent, linep and leading_ws >>

				i = self.skipSentinelStart(s,0)
			# All cases must appear here so we can set the next line properly below.
			if kind == atFile.noSentinel:
				
				#@<< append non-sentinel line >>
				#@+node:3::<< append non-sentinel line >>
				#@+body
				# We don't output the trailing newline if the next line is a sentinel.
				
				i = self.skipIndent(s,0,self.indent)
				
				assert(nextLine != None)
				
				if nextKind == atFile.noSentinel:
					line = s[i:]
					out.append(line)
				else:
					line = s[i:-1] # don't output the newline
					out.append(line)

				#@-body
				#@-node:3::<< append non-sentinel line >>

			elif kind == atFile.startAt:
				
				#@<< scan @+at >>
				#@+node:6::start sentinels
				#@+node:1::<< scan @+at >>
				#@+body
				assert(match(s,i,"+at"))
				self.scanDoc(file,s,i,out,kind)
				#@-body
				#@-node:1::<< scan @+at >>
				#@-node:6::start sentinels

			elif kind == atFile.startBody:
				
				#@<< scan @+body >>
				#@+node:6::start sentinels
				#@+node:2::<< scan @+body >>
				#@+body
				assert(match(s,i,"+body"))
				self.scanText(file,v,out,atFile.endBody)
				#@-body
				#@-node:2::<< scan @+body >>
				#@-node:6::start sentinels

			elif kind == atFile.startDelims:
				
				#@<< scan @delims >>
				#@+node:7::unpaired sentinels
				#@+node:1::<< scan @delims >>
				#@+body
				assert(match(s,i,"@delims"));
				
				# Skip the keyword and whitespace.
				i0 = i
				i = skip_ws(s,i+7)
					
				# Get the first delim.
				i1 = i
				while i < len(s) and is_ws(s[i]) and not is_nl(s,i):
					i += 1
				if i1 < i:
					self.startSentinelComment = s[i1,i]
				
					# Get the optional second delim.
					i1 = i = skip_ws(s,i)
					while i < len(s) and not is_ws(*i) and not is_nl(*i):
						i += 1
					end = choose(i > i1, s[i1:i], "")
					i2 = skip_ws(s,i)
					if end == self.endSentinelComment and (i2 >= len(s) or is_nl(s,i2)):
						self.endSentinelComment = "" # Not really two params.
						line = s[i0:i1]
						line = string.rstrip(line)
						out.append(line)
					else:
						self.endSentinelComment = end
						line = s[i0:i]
						line = string.rstrip(line)
						out.append(line)
				else:
					self.readError("Bad @delims")
					# Append the bad @delims line to the body text.
					out.append("@delims")
				

				#@-body
				#@-node:1::<< scan @delims >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startDirective:
				
				#@<< scan @@ >>
				#@+node:7::unpaired sentinels
				#@+node:4::<< scan @@ >>
				#@+body
				assert(match(s,i,"@"))
				
				# The first '@' has already been eaten.
				if len(self.endSentinelComment) == 0:
					out.append(s[i:])
				else:
					k = string.find(s,self.endSentinelComment,i)
					if k == -1:
						out.append(s[i:])
					else:
						out.append(s[i:k] + '\n')

				#@-body
				#@-node:4::<< scan @@ >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startDoc:
				
				#@<< scan @+doc >>
				#@+node:6::start sentinels
				#@+node:3::<< scan @+doc >>
				#@+body
				assert(match(s,i,"+doc"))
				self.scanDoc(file,s,i,out,kind)
				#@-body
				#@-node:3::<< scan @+doc >>
				#@-node:6::start sentinels

			elif kind == atFile.startLeo:
				
				#@<< scan @+leo >>
				#@+node:6::start sentinels
				#@+node:4::<< scan @+leo >>
				#@+body
				assert(match(s,i,"+leo"))
				self.readError("Ignoring unexpected @+leo sentinel")
				#@-body
				#@-node:4::<< scan @+leo >>
				#@-node:6::start sentinels

			elif kind == atFile.startNode:
				
				#@<< scan @+node >>
				#@+node:6::start sentinels
				#@+node:5:C=9:<< scan @+node >>
				#@+body
				assert(match(s,i,"+node:"))
				i += 6
				
				childIndex = 0 ; cloneIndex = 0
				
				#@<< Set childIndex >>
				#@+node:1::<< Set childIndex >>
				#@+body
				i = skip_ws(s,i) ; j = i
				while i < len(s) and s[i] in string.digits:
					i += 1
				
				if j == i or not match(s,i,':'):
					self.readError("Bad child index in @+node")
				else:
					childIndex = int(s[j:i])
					i += 1 # Skip the ":".
				#@-body
				#@-node:1::<< Set childIndex >>

				
				#@<< Set cloneIndex >>
				#@+node:2::<< Set cloneIndex >>
				#@+body
				while i < len(s) and s[i] != ':' and not is_nl(s,i):
					if match(s,i,"C="):
						# set cloneIndex from the C=nnn, field
						i += 2 ; j = i
						while i < len(s) and s[i] in string.digits:
							i += 1
						if j < i:
							cloneIndex = int(s[j:i])
					else: i += 1 # Ignore unknown status bits.
				
				if match(s,i,":"):
					i += 1
				else:
					self.readError("Bad attribute field in @+node")
				#@-body
				#@-node:2::<< Set cloneIndex >>

				headline = ""
				
				#@<< Set headline and ref >>
				#@+node:3::<< Set headline and ref >>
				#@+body
				# Set headline to the rest of the line.
				if len(self.endSentinelComment) == 0:
					headline = string.strip(s[i:-1])
				else:
					k = string.find(s,self.endSentinelComment,i)
					headline = string.strip(s[i:k]) # works if k == -1
				
				# Set reference if it exists.
				i = skip_ws(s,i)
				
				if 0: # no longer used
					if match(s,i,"<<"):
						k = string.find(s,">>",i)
						if k != -1: ref = s[i:k+2]
				#@-body
				#@-node:3::<< Set headline and ref >>

				oldIndent = self.indent ; self.indent = lineIndent
				
				if childIndex == 0: # The root node.
					
					#@<< Check the filename in the sentinel >>
					#@+node:4::<< Check the filename in the sentinel >>
					#@+body
					fileName = string.strip(headline)
					
					if fileName[:5] == "@file":
						fileName = string.strip(fileName[5:])
						if fileName != self.targetFileName:
							self.readError("File name in @node sentinel does not match file's name")
					else:
						self.readError("Missing @file in root @node sentinel")
					#@-body
					#@-node:4::<< Check the filename in the sentinel >>

					# Put the text of the root node in the current node.
					self.scanText(file,v,out,atFile.endNode)
					v.t.setCloneIndex(cloneIndex)
					# if cloneIndex > 0: trace("clone index:" + `cloneIndex` + ", " + `v`)
					self.indent = oldIndent
				else:
					# NB: this call to createNthChild is the bottleneck!
					child = self.createNthChild(childIndex,v,headline)
					child.t.setCloneIndex(cloneIndex)
					# if cloneIndex > 0: trace("clone index:" + `cloneIndex` + ", " + `child`)
					child_out = []
					self.scanText(file,child,child_out,atFile.endNode)
					# If text followed the section reference in the outline,
					# that text will immediately follow the @-node sentinel.
					s = file.readline()
					# 2/24/02: when newlines are suppressed the next line could be a sentinel.
					if len(s) > 1 and self.sentinelKind(s) == atFile.startVerbatimAfterRef:
						s = file.readline()
						# trace("verbatim:"+`s`)
						out.append(s)
					elif len(s) > 1 and self.sentinelKind(s) == atFile.noSentinel: 
						out.append(s)
					else:
						nextLine = s
					if child.isOrphan():
						self.readError("Replacing body text of orphan: " + child.headString())
					body = string.join(child_out, "")
					# 8/13/02: Remove cursed newlines.
					body = string.replace(body, '\r', '')
					child.t.setTnodeText(body)
					self.indent = oldIndent
					if len(s) == 1: # don't discard newline
						continue
				#@-body
				#@-node:5:C=9:<< scan @+node >>
				#@-node:6::start sentinels

			elif kind == atFile.startOthers:
				
				#@<< scan @+others >>
				#@+node:6::start sentinels
				#@+node:6::<< scan @+others >>
				#@+body
				assert(match(s,i,"+others"))
				
				# Make sure that the generated at-others is properly indented.
				out.append(leading_ws + "@others")
				self.scanText(file,v,out,atFile.endOthers )
				#@-body
				#@-node:6::<< scan @+others >>
				#@-node:6::start sentinels

			elif kind == atFile.startRef:
				
				#@<< scan @ref >>
				#@+node:7::unpaired sentinels
				#@+node:2::<< scan @ref >>
				#@+body
				#@+at
				#  The sentinel contains an @ followed by a section name in angle brackets.  This code is different from the code 
				# for the @@ sentinel: the expansion of the reference does not include a trailing newline.

				#@-at
				#@@c
				
				assert(match(s,i,"<<"))
				
				if len(self.endSentinelComment) == 0:
					line = s[i:-1] # No trailing newline
				else:
					k = string.find(s,self.endSentinelComment,i)
					line = s[i:k] # No trailing newline, whatever k is.
					
				out.append(line)

				#@-body
				#@-node:2::<< scan @ref >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startVerbatim:
				
				#@<< scan @verbatim >>
				#@+node:7::unpaired sentinels
				#@+node:3::<< scan @verbatim >>
				#@+body
				assert(match(s,i,"verbatim"))
				
				# Skip the sentinel.
				s = file.readline() 
				
				# Append the next line to the text.
				i = self.skipIndent(s,0,self.indent)
				out.append(s[i:])

				#@-body
				#@-node:3::<< scan @verbatim >>
				#@-node:7::unpaired sentinels

			elif ( kind == atFile.endAt or kind == atFile.endBody or
				kind == atFile.endDoc or kind == atFile.endLeo or
				kind == atFile.endNode or kind == atFile.endOthers ):
				
				#@<< handle an ending sentinel >>
				#@+node:4::<< handle an ending sentinel >>
				#@+body
				if kind == endSentinelKind:
					if kind == atFile.endLeo:
						s = file.readline()
						if len(s) > 0:
							self.readError("Ignoring text after @-leo")
					# nextLine != None only if we have a non-sentinel line.
					# Therefore, nextLine == None whenever scanText returns.
					assert(nextLine==None)
					return
				else:
					# Tell of the structure error.
					name = self.sentinelName(kind)
					expect = self.sentinelName(endSentinelKind)
					self.readError("Ignoring " + name + " sentinel.  Expecting " + expect)
				#@-body
				#@-node:4::<< handle an ending sentinel >>

			else:
				
				#@<< warn about unknown sentinel >>
				#@+node:8::<< warn about unknown sentinel >>
				#@+body
				j = i
				i = skip_line(s,i)
				line = s[j:i]
				self.readError("Unknown sentinel: " + line)
				#@-body
				#@-node:8::<< warn about unknown sentinel >>

		
		#@<< handle unexpected end of text >>
		#@+node:5::<< handle unexpected end of text >>
		#@+body
		# Issue the error.
		name = self.sentinelName(endSentinelKind)
		self.readError("Unexpected end of file. Expecting " + name + "sentinel" )

		#@-body
		#@-node:5::<< handle unexpected end of text >>

		assert(len(s)==0 and nextLine==None) # We get here only if readline fails.

	#@-body
	#@+node:6::start sentinels
	#@-node:6::start sentinels
	#@+node:7::unpaired sentinels
	#@-node:7::unpaired sentinels
	#@-node:7::scanText
	#@-node:5::Reading
	#@+node:6::Writing
	#@+node:1:C=10:os, onl, etc. (leoAtFile)
	#@+body
	def oblank(self):
		self.os(' ')
	
	def oblanks(self,n):
		self.os(' ' * abs(n))
	
	def onl(self):
		self.os("\n")
	
	def os(self,s):
		if s is None or len(s) == 0: return
		if self.suppress_newlines and self.newline_pending:
			self.newline_pending = false
			s = "\n" + s
		if self.outputFile:
			try:
				try:
					self.outputFile.write(s)
				except UnicodeError: # This might never happen.
					xml_encoding = app().config.xml_version_string
					s = s.encode(xml_encoding)
					self.outputFile.write(s)
			except:
				traceback.print_exc()
				es("exception writing:" + `s`)
	
	def otabs(self,n):
		self.os('\t' * abs(n))
	#@-body
	#@-node:1:C=10:os, onl, etc. (leoAtFile)
	#@+node:2::putBody
	#@+body
	#@+at
	#  root is an ancestor of v, or root == v.  This puts the entire expansion of v's body text enclosed in sentinel lines.

	#@-at
	#@@c
	
	def putBody(self,root,v):
	
		self.putOpenSentinels(root, v)
		self.putBodyPart(v)
		v.setVisited()
		self.putCloseSentinels(root, v)

	#@-body
	#@-node:2::putBody
	#@+node:3::putBodyPart (removes trailing lines)
	#@+body
	#@+at
	#  We generate the body part only if it contains something besides whitespace. The check for at-ignore is made in atFile::write.

	#@-at
	#@@c
	def putBodyPart(self,v):
	
		s = v.t.bodyString
		i = skip_ws_and_nl(s, 0)
		if i >= len(s): return
		s = removeTrailingWs(s) # don't use string.rstrip!
		self.putSentinel("@+body")
		
		#@<< put code/doc parts and sentinels >>
		#@+node:1::<< put code/doc parts and sentinels >>
		#@+body
		i = 0 ; n = len(s)
		while i < n:
			kind = self.directiveKind(s,i)
			j = i
			if kind == atFile.docDirective or kind == atFile.atDirective:
				i = self.putDoc(s,i,kind)
			elif kind == atFile.miscDirective:
				i = self.putDirective(s,i)
			elif kind == atFile.noDirective or kind == atFile.othersDirective:
				i = self.putCodePart(s,i,v)
			elif kind == atFile.cDirective or kind == atFile.codeDirective:
				i = self.putDirective(s,i)
				i = self.putCodePart(s,i,v)
			else: assert(false) # We must handle everything that directiveKind returns
			assert(n == len(s))
			assert(j < i) # We must make progress.
		#@-body
		#@-node:1::<< put code/doc parts and sentinels >>

		self.putSentinel("@-body")
	#@-body
	#@-node:3::putBodyPart (removes trailing lines)
	#@+node:4:C=11:putCodePart & allies
	#@+body
	#@+at
	#  This method expands a code part, terminated by any at-directive except at-others.  It expands references and at-others and 
	# outputs @verbatim sentinels as needed.

	#@-at
	#@@c
	def putCodePart(self,s,i,v):
	
		c = self.commands
		atOthersSeen = false # true: at-others has been expanded.
		while i < len(s):
			
			#@<< handle the start of a line >>
			#@+node:1::<< handle the start of a line >>
			#@+body
			#@+at
			#  The at-others directive is the only directive that is recognized following leading whitespace, so it is just a 
			# little tricky to recognize it.

			#@-at
			#@@c
			
			j,delta = skip_leading_ws_with_indent(s,i,self.tab_width)
			kind1 = self.directiveKind(s,i)
			kind2 = self.directiveKind(s,j)
			if kind1 == atFile.othersDirective or kind2 == atFile.othersDirective:
				
				#@<< handle @others >>
				#@+node:1::<< handle @others >>
				#@+body
				# This skips all indent and delta whitespace, so putAtOthers must generate it all.
				i = skip_to_end_of_line(s,i)
				if atOthersSeen:
					self.writeError("@others already expanded in: " + v.headString())
				else:
					atOthersSeen = true
					self.putAtOthers(v, delta)
				#@-body
				#@-node:1::<< handle @others >>

			elif kind1 == atFile.noDirective:
				
				#@<< put @verbatim sentinel if necessary >>
				#@+node:2::<< put @verbatim sentinel if necessary >>
				#@+body
				if match (s, i, self.startSentinelComment + '@'):
					self.putSentinel("verbatim")
				#@-body
				#@-node:2::<< put @verbatim sentinel if necessary >>

			else:
				break # all other directives terminate the code part.

			#@-body
			#@-node:1::<< handle the start of a line >>

			
			#@<< put the line >>
			#@+node:2::<< put the line >>
			#@+body
			self.putIndent(self.indent)
			
			while i < len(s):
				ch = s[i]
				if ch == body_newline:
					self.onl()
					i = skip_nl(s, i)
					break
				elif ch == body_ignored_newline:
					i += 1
				elif ch == '<':
					
					#@<< put possible section reference >>
					#@+node:1::<< put possible section reference >>
					#@+body
					isSection, j = self.isSectionName(s, i)
					
					if isSection:
						# Output the expansion.
						name = s[i:j]
						self.putRef(name,v,s,j,delta)
						assert(j > i) # isSectionName must have made progress
						i = j
					else:
						self.os(s[i]) # This is _not_ an error.
						i += 1
					#@-body
					#@-node:1::<< put possible section reference >>

				else:
					self.os(ch)
					i += 1
			#@-body
			#@-node:2::<< put the line >>

		return i
	#@-body
	#@+node:3::isSectionName
	#@+body
	# returns (flag, end). end is the index of the character after the section name.
	
	def isSectionName(self,s,i):
	
		if not match(s,i,"<<"):
			return false, -1
		i = find_on_line(s,i,">>")
		if i:
			return true, i + 2
		else:
			return false, -1
	#@-body
	#@-node:3::isSectionName
	#@+node:4:C=12:inAtOthers
	#@+body
	#@+at
	#  Returns true if v should be included in the expansion of the at-others directive in the body text of v's parent.
	# 
	# 7/30/02: v will not be included if it is a definition node or if its body text contains an @ignore directive. Previously, a 
	# "nested" @others directive would also inhibit the inclusion of v.

	#@-at
	#@@c
	def inAtOthers(self,v):
	
		# Return false if this has been expanded previously.
		if  v.isVisited(): return false
		# Return false if this is a definition node.
		h = v.headString()
		i = skip_ws(h,0)
		isSection, j = self.isSectionName(h,i)
		if isSection: return false
		# Return false if v's body contains an @ignore or at-others directive.
		if 1: # 7/29/02: New code.  Amazingly, this appears to work!
			return not v.isAtIgnoreNode()
		else: # old & reliable code
			return not v.isAtIgnoreNode() and not v.isAtOthersNode()
	#@-body
	#@-node:4:C=12:inAtOthers
	#@+node:5:C=13:putAtOthers
	#@+body
	#@+at
	#  The at-others directive is recognized only at the start of the line.  This code must generate all leading whitespace for 
	# the opening sentinel.

	#@-at
	#@@c
	def putAtOthers(self,v,delta):
	
		self.indent += delta
		self.putSentinel("@+others")
		child = v.firstChild()
		while child:
			if self.inAtOthers( child ):
				self.putAtOthersChild( child )
			child = child.next()
		self.putSentinel("@-others")
		self.indent -= delta
	#@-body
	#@-node:5:C=13:putAtOthers
	#@+node:6:C=14:putAtOthersChild
	#@+body
	def putAtOthersChild(self,v):
	
		self.putOpenNodeSentinel(v)
		
		# Insert the expansion of v.
		v.setVisited() # Make sure it is never expanded again.
		self.putBodyPart(v)
	
		# Insert expansions of all children.
		child = v.firstChild()
		while child:
			if self.inAtOthers( child ):
				self.putAtOthersChild( child )
			child = child.next()
	
		self.putCloseNodeSentinel(v)
	#@-body
	#@-node:6:C=14:putAtOthersChild
	#@+node:7::putRef
	#@+body
	def putRef (self,name,v,s,i,delta):
	
		# trace(get_line(s[i:],0))
		ref = findReference(name, v)
		if ref:
			# 2/24/02: adjust indent here so sentinel looks better.
			self.indent += delta 
			self.putSentinel("@" + name)
			self.putBody(v, ref)
			self.indent -= delta
			# 2/25/02: Add a sentinel if required.
			j = skip_ws(s,i)
			if j < len(s) and match(s,j,self.startSentinelComment + '@'):
				self.putSentinel("@verbatimAfterRef")
		else:
			self.writeError("undefined section: " + name +
				"\n\treferenced from: " + v.headString())
	#@-body
	#@-node:7::putRef
	#@-node:4:C=11:putCodePart & allies
	#@+node:5::putDirective  (handles @delims)
	#@+body
	# This method outputs s, a directive or reference, in a sentinel.
	
	def putDirective(self,s,i):
	
		tag = "@delims"
		assert(i < len(s) and s[i] == '@')
		k = i
		j = skip_to_end_of_line(s,i)
		directive = s[i:j]
	
		if match_word(s,k,tag):
			
			#@<< handle @delims >>
			#@+node:1::<< handle @delims >>
			#@+body
			# Put a space to protect the last delim.
			self.putSentinel("@" + directive + " ")
			
			# Skip the keyword and whitespace.
			j = i = skip_ws(s,k+len(tag))
			
			# Get the first delim.
			while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
				i += 1
			if j < i:
				self.startSentinelComment = s[j:i]
				# Get the optional second delim.
				j = i = skip_ws(s,i)
				while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
					i += 1
				self.endSentinelComment = choose(j<i, s[j:i], "")
			else:
				self.writeError("Bad @delims directive")
			#@-body
			#@-node:1::<< handle @delims >>

		else:
			self.putSentinel("@" + directive)
	
		i = skip_line(s,k)
		return i
	#@-body
	#@-node:5::putDirective  (handles @delims)
	#@+node:6::putDoc
	#@+body
	#@+at
	#  This method outputs a doc section terminated by @code or end-of-text.  All other interior directives become part of the doc part.

	#@-at
	#@@c
	def putDoc(self,s,i,kind):
	
		if kind == atFile.atDirective:
			i += 1 ; tag = "at"
		elif kind == atFile.docDirective:
			i += 4 ; tag = "doc"
		else: assert(false)
		# Set j to the end of the doc part.
		n = len(s) ; j = i
		while j < n:
			j = skip_line(s, j)
			kind = self.directiveKind(s, j)
			if kind == atFile.codeDirective or kind == atFile.cDirective:
				break
		self.putSentinel("@+" + tag)
		self.putDocPart(s[i:j])
		self.putSentinel("@-" + tag)
		return j
	#@-body
	#@-node:6::putDoc
	#@+node:7:C=15:putDocPart
	#@+body
	# Puts a comment part in comments.
	
	def putDocPart(self,s):
	
		# j = skip_line(s,0) ; trace(`s[:j]`)
		c = self.commands
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
			
			#@<< copy words, splitting the line if needed >>
			#@+node:1::<< copy words, splitting the line if needed >>
			#@+body
			#@+at
			#  We remove trailing whitespace from lines that have _not_ been split so that a newline has been inserted by this 
			# routine if and only if it is preceded by whitespace.

			#@-at
			#@@c
			
			line = i # Start of the current line.
			while i < n:
				word = i # Start of the current word.
				# Skip the next word and trailing whitespace.
				i = skip_ws(s, i)
				while i < n and not is_nl(s,i) and not is_ws(s[i]):
					i += 1
				i = skip_ws(s,i)
				# Output the line if no more is left.
				if i < n and is_nl(s,i):
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
			if i < n and is_nl(s,i):
				i = skip_nl(s,i)
				self.onl() # No inserted newline and no trailing whitespace.
			#@-body
			#@-node:1::<< copy words, splitting the line if needed >>

		if not single:
			# This comment is like a sentinel.
			self.onl() ; self.putIndent(self.indent)
			self.os(self.endSentinelComment)
			self.onl() # Note: no trailing whitespace.
	#@-body
	#@-node:7:C=15:putDocPart
	#@+node:8:C=16:putIndent
	#@+body
	# Puts tabs and spaces corresponding to n spaces, assuming that we are at the start of a line.
	
	def putIndent(self,n):
	
		c = self.commands
		w = self.tab_width
		if w > 1:
			q,r = divmod(n,w) 
			self.otabs(q) 
			self.oblanks(r)
		else:
			self.oblanks(n)
	#@-body
	#@-node:8:C=16:putIndent
	#@+node:9:C=17:atFile.write
	#@+body
	#@+at
	#  This is the entry point to the write code.  root should be an @file vnode. We set the orphan and dirty flags if there are 
	# problems writing the file to force Commands::write_LEO_file to write the tree to the .leo file.

	#@-at
	#@@c
	def write(self,root):
	
		c = self.commands
		c.setIvarsFromPrefs()
		self.root = root
		c.endEditing() # Capture the current headline.
		self.targetFileName = root.atFileNodeName()
		try:
			
			#@<< Open files.  Set orphan and dirty flags and return on errors >>
			#@+node:1::<< Open files.  Set orphan and dirty flags and return on errors >>
			#@+body
			try:
				self.scanAllDirectives(root)
				valid = self.errors == 0
			except:
				es("exception in atFile.scanAllDirectives")
				traceback.print_exc()
				valid = false
			
			if valid:
				try:
					fn = root.atFileNodeName()
					self.shortFileName = fn # name to use in status messages.
					self.targetFileName = os.path.join(self.default_directory,fn)
					self.targetFileName = os.path.normpath(self.targetFileName)
					path = os.path.dirname(self.targetFileName)
					if len(path) > 0:
						valid = os.path.exists(path)
						if not valid:
							self.writeError("path does not exist: " + path)
					else:
						valid = false
				except:
					es("exception creating path:" + fn)
					traceback.print_exc()
					valid = false
			
			if valid:
				if os.path.exists(self.targetFileName):
					try: # 8/13/02
						read_only = not os.access(self.targetFileName,os.W_OK)
						if read_only:
							es("read only: " + self.targetFileName)
							valid = false
					except: pass # os.access() may not exist on all platforms.
				
			if valid:
				try:
					self.outputFileName = self.targetFileName + ".tmp"
					self.outputFile = open(self.outputFileName, 'w')
					valid = self.outputFile != None
					if not valid:
						self.writeError("can not open " + self.outputFileName)
				except:
					es("exception opening:" + self.outputFileName)
					traceback.print_exc()
					valid = false
			
			if not valid:
				root.setOrphan()
				root.setDirty()
				return
			#@-body
			#@-node:1::<< Open files.  Set orphan and dirty flags and return on errors >>

			# unvisited nodes will be orphans.
			root.clearVisitedInTree()
			next = root.nodeAfterTree()
			self.updateCloneIndices(root, next)
			
			#@<< put all @first lines in root >>
			#@+node:2::<< put all @first lines in root >>
			#@+body
			#@+at
			#  Write any @first lines to ms.  These lines are also converted to @verbatim lines, so the read logic simply ignores 
			# these lines.

			#@-at
			#@@c
			
			s = root.t.bodyString
			tag = "@first"
			i = 0
			while match(s,i,"@first"):
				i += len(tag)
				i = skip_ws(s,i)
				j = i
				i = skip_to_end_of_line(s,i)
				if i > j:
					line = s[j:i]
					self.os(line) ; self.onl()
				i = skip_nl(s,i)
			#@-body
			#@-node:2::<< put all @first lines in root >>

			if 1: # write the entire file
				self.putOpenLeoSentinel("@+leo")
				self.putOpenNodeSentinel(root)
				self.putBodyPart(root)
				root.setVisited()
				self.putCloseNodeSentinel(root)
				self.putSentinel("@-leo")
			if self.outputFile:
				if self.suppress_newlines and self.newline_pending:
					self.newline_pending = false
					self.onl() # Make sure file ends with a newline.
				self.outputFile.flush()
				self.outputFile.close()
				self.outputFile = None
			
			#@<< Warn about @ignored and orphans >>
			#@+node:3::<< Warn about @ignored and orphans  >>
			#@+body
			next = root.nodeAfterTree()
			v = root
			while v and v != next:
				if not v.isVisited():
					self.writeError("Orphan node:  " + v.headString())
				if v.isAtIgnoreNode():
					self.writeError("@ignore node: " + v.headString())
				v = v.threadNext()
			#@-body
			#@-node:3::<< Warn about @ignored and orphans  >>

			if self.errors > 0 or self.root.isOrphan():
				root.setOrphan()
				root.setDirty() # 2/9/02: make _sure_ we try to rewrite this file.
				os.remove(self.outputFileName) # Delete the temp file.
			else:
				root.clearOrphan()
				root.clearDirty()
				
				#@<< Replace the target with the temp file if different >>
				#@+node:4::<< Replace the target with the temp file if different >>
				#@+body
				assert(self.outputFile == None)
				
				if os.path.exists(self.targetFileName):
					if filecmp.cmp(self.outputFileName, self.targetFileName):
						try: # Just delete the temp file.
							os.remove(self.outputFileName)
						except:
							es("exception deleting:" + self.outputFileName)
							traceback.print_exc()
						es("unchanged: " + self.shortFileName)
					else:
						try: # Replace target file with temp file.
							os.remove(self.targetFileName)
							os.rename(self.outputFileName, self.targetFileName)
							es("writing: " + self.shortFileName)
						except:
							self.writeError("exception removing and renaming:" + self.outputFileName +
								" to " + self.targetFileName)
							traceback.print_exc()
				else:
					try:
						os.rename(self.outputFileName, self.targetFileName)
						es("creating: " + self.targetFileName)
					except:
						self.writeError("exception renaming:" + self.outputFileName +
							" to " + self.targetFileName)
						traceback.print_exc()
				#@-body
				#@-node:4::<< Replace the target with the temp file if different >>

		except:
			
			#@<< handle all exceptions during the write >>
			#@+node:5::<< handle all exceptions during the write >>
			#@+body
			es("exception writing:" + self.targetFileName)
			traceback.print_exc()
			
			if self.outputFile: # 8/2/02
				self.outputFile.close()
				self.outputFile = None
			
			if self.outputFileName != None:
				try: # Just delete the temp file.
					os.remove(self.outputFileName)
				except:
					es("exception deleting:" + self.outputFileName)
					traceback.print_exc()
			#@-body
			#@-node:5::<< handle all exceptions during the write >>
	#@-body
	#@-node:9:C=17:atFile.write
	#@+node:10::writeAll
	#@+body
	#@+at
	#  This method scans all vnodes, calling write for every @file node found.  If partialFlag is true we write all @file nodes in 
	# the selected outline.  Otherwise we write @file nodes in the entire outline.

	#@-at
	#@@c
	def writeAll(self,v,partialFlag):
	
		self.initIvars()
		# Kludge: look at whole tree if forceFlag is false;
		if partialFlag: after = v.nodeAfterTree()
		else: after = None
		
		#@<< Clear all orphan bits >>
		#@+node:1::<< Clear all orphan bits >>
		#@+body
		#@+at
		#  We must clear these bits because they may have been set on a previous write.  Calls to atFile::write may set the orphan 
		# bits in @file nodes.  If so, write_LEO_file will write the entire @file tree.

		#@-at
		#@@c
		
		v2 = v
		while v2 and v2 != after:
			v2.clearOrphan()
			v2 = v2.threadNext()
		#@-body
		#@-node:1::<< Clear all orphan bits >>

		written = false
		while v and v != after:
			if v.isAtIgnoreNode():
				v = v.nodeAfterTree()
			elif v.isAtFileNode():
				if v.isDirty() or partialFlag:
					self.write(v)
					written = true
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		if partialFlag and not written:
			es("no @file nodes in the selected tree")
	#@-body
	#@-node:10::writeAll
	#@-node:6::Writing
	#@+node:7::Testing
	#@+node:1::scanAll
	#@+body
	def scanAll (self):
	
		c = self.commands ; v = c.rootVnode()
		while v:
			if v.isAtIgnoreNode():
				v = v.nodeAfterTree()
			elif v.isAtFileNode():
				self.scanFile(v)
				v = v.nodeAfterTree()
			else: v = v.threadNext()
	#@-body
	#@-node:1::scanAll
	#@+node:2::scanFile
	#@+body
	def scanFile(self,root):
	
		es("scanning: " + root.headString())
		self.targetFileName = root.atFileNodeName()
		self.root = root
		self.errors = self.structureErrors = 0
		
		#@<< open file >>
		#@+node:1::<< open file >>
		#@+body
		if len(self.targetFileName) == 0:
			self.readError("Missing file name")
		else:
			try:
				file = open(self.targetFileName,'r')
			except:
				self.readError("Error reading file")

		#@-body
		#@-node:1::<< open file >>

		if self.errors > 0: return 0
		
		#@<< Scan the file buffer >>
		#@+node:2::<< Scan the file buffer  >>
		#@+body
		self.indent = 0
		out = []
		self.scanHeader(file)
		self.scanText(file,root,out,atFile.endLeo)
		s = string.join(out, "")
		root.setBodyStringOrPane(s)
		#@-body
		#@-node:2::<< Scan the file buffer  >>

		if self.structureErrors > 0:
			self.readError(`self.structureErrors` + " errors scanning file")
		return self.errors == 0

	#@-body
	#@-node:2::scanFile
	#@-node:7::Testing
	#@-others
#@-body
#@-node:0::@file leoAtFile.py
#@-leo
