#@+leo-ver=4
#@+node:@file leoNodes.py
#@@language python

#@<< About the vnode and tnode classes >>
#@+node:<< About the vnode and tnode classes >>
#@+at 
#@nonl
# The vnode and tnode classes represent most of the data contained in the 
# outline. These classes are Leo's fundamental Model classes.
# 
# A vnode (visual node) represents a headline at a particular location on the 
# screen. When a headline is cloned, vnodes must be copied. vnodes persist 
# even if they are not drawn on the screen. Commanders call vnode routines to 
# insert, delete and move headlines.
# 
# The vnode contains data associated with a headline, except the body text 
# data which is contained in tnodes. A vnode contains headline text, a link to 
# its tnode and other information. In leo.py, vnodes contain structure links: 
# parent, firstChild, next and back ivars. To insert, delete, move or clone a 
# vnode the vnode class just alters those links. The Commands class calls the 
# leoTree class to redraw the outline pane whenever it changes. The leoTree 
# class knows about these structure links; in effect, the leoTree and vnode 
# classes work together. The implementation of vnodes is quite different in 
# the Borland version of Leo. This does not affect the rest of the Leo. 
# Indeed, vnodes are designed to shield Leo from such implementation details.
# 
# A tnode, (text node) represents body text: a tnode is shared by all vnodes 
# that are clones of each other. In other words, tnodes are the unit of 
# sharing of body text. The tnode class is more private than the vnode class. 
# Most commanders deal only with vnodes, though there are exceptions.
# 
# Because leo.py has unlimited Undo commands, vnodes and tnodes can be deleted 
# only when the window containing them is closed. Nodes are deleted 
# indirectly.
# 
# Leo uses several kinds of node indices. Leo's XML file format uses tnode 
# indices to indicate which tnodes (t elements) belong to which vnodes (v 
# elements). Such indices are required. Even if we duplicated the body text of 
# shared tnodes within the file, the file format would still need an 
# unambiguous way to denote that tnodes are shared.
# 
# Present versions of Leo recompute these tnodes indices whenever Leo writes 
# any .leo file. Earlier versions of Leo remembered tnode indices and rewrote 
# the same indices whenever possible. Those versions of Leo recomputed indices 
# when executing the Save As and Save To commands, so using these commands was 
# a way of "compacting" indices. The main reason for not wanting to change 
# tnode indices in .leo files was to reduce the number of changes reported by 
# CVS and other Source Code Control Systems. I finally abandoned this goal in 
# the interest of simplifying the code. Also, CVS will likely report many 
# differences between two versions of the same .leo file, regardless of 
# whether tnode indices are conserved.
# 
# A second kind of node index is the clone index used in @+node sentinels in 
# files derived from @file trees. As with indices in .leo files, indices in 
# derived files are required so that Leo can know unambiguously which nodes 
# are cloned to each other.
# 
# It is imperative that clone indices be computed correctly, that is, that 
# tnode @+node sentinels have the same index if and only if the corresponding 
# vnodes are cloned. Early versions of leo.py had several bugs involving these 
# clone indices. Such bugs are extremely serious because they corrupt the 
# derived file and cause read errors when Leo reads the @file tree. Leo must 
# guarantee that clone indices are always recomputed properly. This is not as 
# simple as it might appear at first. In particular, Leo's commands must 
# ensure that @file trees are marked dirty whenever any changed is made that 
# affects cloned nodes within the tree. For example, a change made outside any 
# @file tree may make several @file trees dirty if the change is made to a 
# node with clones in those @file trees.
#@-at
#@-node:<< About the vnode and tnode classes >>
#@nl
#@<< About clones >>
#@+node:<< About clones >>
#@+at 
#@nonl
# This is the design document for clones in Leo. It covers all important 
# aspects of clones. Clones are inherently complex, and this paper will 
# include several different definitions of clones and related concepts.
# 
# The following is a definition of clones from the user's point of view.
# 
# Definition 1
# 
# A clone node is a copy of a node that changes when the original changes. 
# Changes to the children, grandchildren, etc. of a node are simultaneously 
# made to the corresponding nodes contained in all cloned nodes. Clones are 
# marked by a small clone arrow by its leader character.
# 
# As we shall see, this definition glosses over a number of complications. 
# Note that all cloned nodes (including the original node) are equivalent. 
# There is no such thing as a "master" node from which all clones are derived. 
# When the penultimate cloned node is deleted, the remaining node becomes an 
# ordinary node again.
# 
# Internally, the clone arrow is represented by a clone bit in the status 
# field of the vnode. The Clone Node command sets the clone bits of the 
# original and cloned vnodes when it creates the clone. Setting and clearing 
# clone bits properly when nodes are inserted, deleted or moved, is 
# non-trivial. We need the following machinery to do the job properly.
# 
# Two vnodes are joined if a) they share the same tnode (body text) and b) 
# changes to any subtree of either joined vnodes are made to the corresponding 
# nodes in all joined nodes.  For example, Definition 1 defines clones as 
# joined nodes that are marked with a clone arrow.  Leo links all vnodes 
# joined to each other in a circular list, called the join list. For any vnode 
# n, let J(n) denote the join list of n, that is, the set of all vnodes joined 
# to n. Again, maintaining the join lists in an outline is non-trivial.
# 
# The concept of structurally similar nodes provides an effective way of 
# determining when two joined nodes should also have their cloned bit set.  
# Two joined nodes are structurally similar if a) their parents are distinct 
# but joined and b) they are both the nth child of their (distinct) parents.  
# We can define cloned nodes using the concept of structurally similar nodes 
# as follows:
# 
# Definition 2
# 
# Clones are joined vnodes such that at least two of the vnodes of J(n) are 
# not structurally similar to each other. Non-cloned vnodes are vnodes such 
# that all of the vnodes of J(n) are structurally similar. In particular, n is 
# a non-cloned vnode if J(n) is empty.
# 
# Leo ensures that definitions 1 and 2 are consistent. Definition 1 says that 
# changes to the children, grandchildren, etc. of a node are simultaneously 
# made to the corresponding nodes contained in all cloned nodes. Making 
# "corresponding changes" to the non-cloned descendents of all cloned nodes 
# insures that the non-cloned joined nodes will be structurally similar. On 
# the other hand, cloned nodes are never structurally similar. They are 
# created as siblings, so they have the same parent with different "child 
# indices."  To see how this works in practice, let's look at some examples.
# 
# Example 1
# 
# + root
# 	+ a' (1)
# 	+ a' (2)
# 
# This example shows the simplest possible clone. A prime (') indicates a 
# cloned node.  Node a in position (1) has just been cloned to produce a' in 
# position (2). Clearly, these two cloned nodes are not structurally similar 
# because their parents are not distinct and they occupy different positions 
# relative to their common parent.
# 
# Example 2
# 
# If we add a node b to either a' node we get the following tree:
# 
# + root
# 	+ a'
# 		+ b
# 	+ a'
# 		+ b
# 
# The b nodes are structurally similar because the a' nodes are joined and 
# each b node is the first child of its parent.
# 
# Example 3
# 
# If we now clone either b, we will get:
# 
# + root
# 	+ a'
# 		+ b' (1)
# 		+ b' (2)
# 	+ a'
# 		+ b' (1)
# 		+ b' (2)
# 
# All b' nodes must be clones because the nodes marked (1) are not 
# structurally similar to the nodes marked (2).
# 
# Dependent nodes are nodes created or destroyed when corresponding linked 
# nodes are created or destroyed in another tree. For example, going from 
# example 1 to example 2 above, adding node b to either node a' causes another 
# (dependent) node to be created as the ancestor of the other node a'. 
# Similarly, going from example 2 to example 1, deleting node b from either 
# node a' causes the other (dependent) node b to be deleted from the other 
# node a'.  Cloned nodes may also be dependent nodes. In Example 3, all the b' 
# nodes are dependent on any of the other b' nodes.
# 
# We can now give simple rules for inserting and deleting dependent vnodes 
# when other vnodes are created, moved or destroyed. For the purposes of this 
# discussion, moving a node is handled exactly like deleting the node then 
# inserting the node; we need not consider moving nodes further.  We insert a 
# new node n as the nth child of a parent node p as follows. We insert n, then 
# for every node pi linked to p, we insert a dependent node ni as the nth 
# child of pi. Each ni is linked to n. Clearly, each ni is structurally 
# similar to n.  Similarly, it is easy to delete a node n that is the nth 
# child of a parent node p. We delete each dependent node ni that is the nth 
# child of any node pi linked to p. We then delete n.  When inserting or 
# deleting any vnode n we must update its join list, J(n). Updating the join 
# list is easy because the join list is circular: the entire list is 
# accessible from any of its members.
# 
# Inserting or deleting nodes can cause the clone bits of all joined nodes to 
# change in non-trivial ways. To see the problems that can arise, consider 
# deleting any of the b' nodes from Example 3. We would be left with the tree 
# in Example 2. There are two remaining b nodes, each with the clone bit set. 
# Unless we know that both b nodes are structurally similar, there would be no 
# way to conclude that we should clear the clone bits in each node. In order 
# to update clone links properly we could examine many special cases, but 
# there is an easier way. Because of definition 2, we can define a 
# shouldBeCloned function that checks J(n) to see whether all nodes of J(n) 
# are structurally similar.
# 
# Leo's XML file format does not contain join lists. This makes it easy to 
# change a Leo file "by hand." If join lists were a part of the file, as they 
# are in the Mac version of Leo, corrupting a join list would corrupt the 
# entire file. It is easy to recreate the join lists when reading a file using 
# a dedicated field in the tnode.  This field is the head of a list of all 
# vnodes that points to the tnode. After reading all nodes, Leo creates this 
# list with one pass through the vnodes.  Leo then converts each list to a 
# circular list with one additional pass through the tnodes.
#@-at
#@-node:<< About clones >>
#@nl

from leoGlobals import *
import time,types

#@+others
#@+node:class tnode
class baseTnode:
	"""The base class of the tnode class."""
	#@	<< tnode constants >>
	#@+node:<< tnode constants >>
	dirtyBit =		0x01
	richTextBit =	0x02 # Determines whether we use <bt> or <btr> tags.
	visitedBit =	0x04
	#@nonl
	#@-node:<< tnode constants >>
	#@nl
	#@	@+others
	#@+node:t.__init__
	# All params have defaults, so t = tnode() is valid.
	
	def __init__ (self,bodyString=None,headString=None):
	
		self.cloneIndex = 0 # or Pre-3.12 files.  Zero for @file nodes
		self.fileIndex = None # The immutable file index for this tnode.
		self.insertSpot = None # Location of previous insert point.
		self.joinList = [] # New in 3.12: vnodes on the same joinlist are updated together.
		self.scrollBarSpot = None # Previous value of scrollbar position.
		self.selectionLength = 0 # The length of the selected body text.
		self.selectionStart = 0 # The start of the selected body text.
		self.statusBits = 0 # status bits
	
		# Convert everything to unicode...
		self.headString = toUnicode(headString,app.tkEncoding)
		self.bodyString = toUnicode(bodyString,app.tkEncoding)
	#@nonl
	#@-node:t.__init__
	#@+node:t.__repr__ & t.__str__
	def __repr__ (self):
		
		return "<tnode %d>" % (id(self))
			
	__str__ = __repr__
	#@nonl
	#@-node:t.__repr__ & t.__str__
	#@+node:t.extraAttributes & setExtraAttributes
	def extraAttributes (self):
	
		try:    return self.unknownAttributes
		except: return None
		
	def setExtraAttributes (self,attributes):
		
		if attributes != None:
			self.unknownAttributes = attributes
	#@nonl
	#@-node:t.extraAttributes & setExtraAttributes
	#@+node:hasBody
	def hasBody (self):
	
		return self.bodyString and len(self.bodyString) > 0
	#@nonl
	#@-node:hasBody
	#@+node:loadBodyPaneFromTnode
	def loadBodyPaneFromTnode(self, body):
	
		s = self.bodyString
		if s and len(s) > 0:
			body.delete(1,"end")
			body.insert(1,s)
		else:
			body.delete(1,"end")
	#@nonl
	#@-node:loadBodyPaneFromTnode
	#@+node:isDirty
	def isDirty (self):
	
		return (self.statusBits & self.dirtyBit) != 0
	#@nonl
	#@-node:isDirty
	#@+node:isRichTextBit
	def isRichTextBit (self):
	
		return (self.statusBits & self.richTextBit) != 0
	#@nonl
	#@-node:isRichTextBit
	#@+node:isVisited
	def isVisited (self):
	
		return (self.statusBits & self.visitedBit) != 0
	#@nonl
	#@-node:isVisited
	#@+node:setTnodeText
	# This sets the text in the tnode from the given string.
	
	def setTnodeText (self,s,encoding="utf-8"):
		
		s = toUnicode(s,encoding,reportErrors=true)
		self.bodyString = s
	#@-node:setTnodeText
	#@+node:setSelection
	def setSelection (self,start,length):
	
		self.selectionStart = start
		self.selectionLength = length
	#@nonl
	#@-node:setSelection
	#@+node:clearDirty
	def clearDirty (self):
	
		self.statusBits &= ~ self.dirtyBit
	#@nonl
	#@-node:clearDirty
	#@+node:clearRichTextBit
	def clearRichTextBit (self):
	
		self.statusBits &= ~ self.richTextBit
	#@nonl
	#@-node:clearRichTextBit
	#@+node:clearVisited
	def clearVisited (self):
	
		self.statusBits &= ~ self.visitedBit
	#@nonl
	#@-node:clearVisited
	#@+node:setDirty
	def setDirty (self):
	
		self.statusBits |= self.dirtyBit
	#@nonl
	#@-node:setDirty
	#@+node:setRichTextBit
	def setRichTextBit (self):
	
		self.statusBits |= self.richTextBit
	#@nonl
	#@-node:setRichTextBit
	#@+node:setVisited
	def setVisited (self):
	
		self.statusBits |= self.visitedBit
	#@nonl
	#@-node:setVisited
	#@+node:setCloneIndex
	def setCloneIndex (self, index):
	
		self.cloneIndex = index
	#@nonl
	#@-node:setCloneIndex
	#@+node:setFileIndex
	def setFileIndex (self, index):
	
		self.fileIndex = index
	#@nonl
	#@-node:setFileIndex
	#@-others
	
class tnode (baseTnode):
	"""A class that implements tnodes."""
	pass
#@nonl
#@-node:class tnode
#@+node:class vnode
class baseVnode:
	"""The base class of the vnode class."""
	#@	<< vnode constants >>
	#@+node:<< vnode constants >>
	# Define the meaning of status bits in new vnodes.
	
	# Archived...
	clonedBit	  = 0x01 # true: vnode has clone mark.
	# not used	 = 0x02
	expandedBit = 0x04 # true: vnode is expanded.
	markedBit	  = 0x08 # true: vnode is marked
	orphanBit	  = 0x10 # true: vnode saved in .leo file, not derived file.
	selectedBit = 0x20 # true: vnode is current vnode.
	topBit		    = 0x40 # true: vnode was top vnode when saved.
	
	# Not archived...
	dirtyBit    =	0x060
	richTextBit =	0x080 # Determines whether we use <bt> or <btr> tags.
	visitedBit	 = 0x100
	#@-node:<< vnode constants >>
	#@nl
	#@	@+others
	#@+node:v.__cmp__ (not used)
	if 0: # not used
		def __cmp__(self,other):
			
			trace(`self` + "," + `other`)
			return not (self is other) # Must return 0, 1 or -1
	#@nonl
	#@-node:v.__cmp__ (not used)
	#@+node:v.__init__
	def __init__ (self,commands,t):
	
		assert(t)
		
		# commands may be None for testing.
		# assert(commands)
	
		#@	<< initialize vnode data members >>
		#@+node:<< initialize vnode data members >>
		self.commands = commands # The commander for this vnode.
		self.t = t # The tnode, i.e., the body text.
		self.statusBits = 0 # status bits
		
		# Structure links
		self.mParent = self.mFirstChild = self.mNext = self.mBack = None
		
		# The icon index. -1 forces an update of icon.
		self.iconVal = -1 
		
		if 0: # Injected by the leoTkinterTree class.
			self.iconx, self.icony = 0,0 # Coords of icon so icon can be redrawn separately.
		#@nonl
		#@-node:<< initialize vnode data members >>
		#@nl
	#@-node:v.__init__
	#@+node:v.__repr__ & v.__str__
	def __repr__ (self):
		
		if self.t:
			return "<vnode %d:%s>" % (id(self),`self.t.headString`)
		else:
			return "<vnode %d:NULL tnode>" % (id(self))
			
	__str__ = __repr__
	#@-node:v.__repr__ & v.__str__
	#@+node:afterHeadlineMatch
	# 12/03/02: We now handle @file options here.
	
	def afterHeadlineMatch(self,s):
		
		h = self.headString()
	
		if s != "@file" and match_word(h,0,s):
			# No options are valid.
			return string.strip(h[len(s):])
		elif match(h,0,"@file"):
			i,atFileType,junk = scanAtFileOptions(h)
			if s == atFileType:
				# print "s,h:",s,h
				return string.strip(h[i:])
			else: return ""
		else: return ""
	#@-node:afterHeadlineMatch
	#@+node:at/../NodeName
	#@+at 
	#@nonl
	# Returns the filename following @file or @rawfile, in the receivers's 
	# headline, or the empty string if the receiver is not an @file node.
	#@-at
	#@@c
	
	def atFileNodeName (self):
		return self.afterHeadlineMatch("@file")
		
	def atNoSentinelsFileNodeName (self):
		return self.afterHeadlineMatch("@nosentinelsfile")
		
	def atRawFileNodeName (self):
		return self.afterHeadlineMatch("@rawfile")
		
	def atSilentFileNodeName (self):
		return self.afterHeadlineMatch("@silentfile")
	#@-node:at/../NodeName
	#@+node:isAt/../Node
	# Returns true if the receiver's headline starts with @file.
	def isAtFileNode (self):
		s = self.atFileNodeName()
		return len(s) > 0
		
	# Returns true if the receiver's headline starts with @rawfile.
	def isAtNoSentinelsFileNode (self):
		s = self.atNoSentinelsFileNodeName()
		return len(s) > 0
		
	# Returns true if the receiver's headline starts with @rawfile.
	def isAtRawFileNode (self):
		s = self.atRawFileNodeName()
		return len(s) > 0
	
	# Returns true if the receiver's headline starts with @silentfile.
	def isAtSilentFileNode (self):
		s = self.atSilentFileNodeName()
		return len(s) > 0
	#@-node:isAt/../Node
	#@+node:isAnyAtFileNode & isAnyAtFileNodeName
	def isAnyAtFileNode (self):
	
		return (
			self.isAtFileNode() or
			self.isAtNoSentinelsFileNode() or
			self.isAtRawFileNode() or
			self.isAtSilentFileNode())
			
	def anyAtFileNodeName (self):
	
		if self.isAtFileNode():
			return self.atFileNodeName()
		elif self.isAtNoSentinelsFileNode():
			return self.atNoSentinelsFileNodeName()
		elif self.isAtRawFileNode():
			return self.atRawFileNodeName()
		elif self.isAtSilentFileNode():
			return self.atSilentFileNodeName()
		else:
			return ""
	#@-node:isAnyAtFileNode & isAnyAtFileNodeName
	#@+node:isAtIgnoreNode
	#@+at 
	#@nonl
	# Returns true if the receiver contains @ignore in its body at the start 
	# of a line.
	#@-at
	#@@c
	
	def isAtIgnoreNode (self):
	
		flag, i = is_special(self.t.bodyString, 0, "@ignore")
		return flag
	#@nonl
	#@-node:isAtIgnoreNode
	#@+node:isAtOthersNode
	#@+at 
	#@nonl
	# Returns true if the receiver contains @others in its body at the start 
	# of a line.
	#@-at
	#@@c
	
	def isAtOthersNode (self):
	
		flag, i = is_special(self.t.bodyString,0,"@others")
		return flag
	#@nonl
	#@-node:isAtOthersNode
	#@+node:matchHeadline
	#@+at 
	#@nonl
	# Returns true if the headline matches the pattern ignoring whitespace and 
	# case.  The headline may contain characters following the successfully 
	# matched pattern.
	#@-at
	#@@c
	
	def matchHeadline (self,pattern):
	
		h = string.lower(self.headString())
		h = string.replace(h,' ','')
		h = string.replace(h,'\t','')
	
		p = string.lower(pattern)
		p = string.replace(p,' ','')
		p = string.replace(p,'\t','')
	
		# ignore characters in the headline following the match
		return p == h[0:len(p)]
	#@nonl
	#@-node:matchHeadline
	#@+node:convertTreeToString
	# Converts the outline to a string in "MORE" format
	
	def convertTreeToString (self):
	
		v = self
		level1 = v.level()
		after = v.nodeAfterTree()
		s = ""
		while v and v != after:
			s += v.moreHead(level1) + "\n"
			body = v.moreBody()
			if len(body) > 0:
				s += body + "\n"
			v = v.threadNext()
		return s
	#@nonl
	#@-node:convertTreeToString
	#@+node:moreHead
	# Returns the headline string in MORE format.
	
	def moreHead (self, firstLevel,useVerticalBar=false):
	
		v = self
		level = self.level() - firstLevel
		if level > 0: s = "\t" * level
		else: s = ""
		s += choose(v.hasChildren(), "+ ", "- ")
		s += v.headString()
		return s
	#@nonl
	#@-node:moreHead
	#@+node:v.moreBody
	#@+at 
	#@nonl
	# Returns the body string in MORE format.  It inserts a backslash before 
	# any leading plus, minus or backslash.
	# 
	# + test line
	# - test line
	# \ test line
	# test line +
	# test line -
	# test line \
	# 
	# More lines...
	#@-at
	#@@c
	
	def moreBody (self):
	
		v = self ; list = []
		
		if 1: # new code: only escape the first non-blank character of the line.
			s =  v.t.bodyString ; result = []
			lines = string.split(s,'\n')
			for s in lines:
				i = skip_ws(s,0)
				if i < len(s):
					ch = s[i]
					if ch == '+' or ch == '-' or ch == '\\':
						s = s[:i] + '\\' + s[i:]
				result.append(s)
			return string.join(result,'\n')
	
		else: # pre 3.1 code.
			for ch in v.t.bodyString:
				if ch == '+' or ch == '-' or ch == '\\':
					list.append('\\')
				list.append(ch)
			return string.join(list,'')
	#@nonl
	#@-node:v.moreBody
	#@+node:v.extraAttributes & setExtraAttributes
	def extraAttributes (self):
	
		try:    tnodeList = self.tnodeList
		except: tnodeList = None
		
		try:    unknownAttributes = self.unknownAttributes
		except: unknownAttributes = None
	
		return tnodeList, unknownAttributes
		
	def setExtraAttributes (self,data):
		
		tnodeList, unknownAttributes = data
	
		if tnodeList != None:
			self.tnodeList = tnodeList
	
		if unknownAttributes != None:
			self.unknownAttributes = unknownAttributes
	#@nonl
	#@-node:v.extraAttributes & setExtraAttributes
	#@+node:childIndex
	# childIndex and nthChild are zero-based.
	
	def childIndex (self):
	
		parent=self.parent()
		if not parent: return 0
	
		child = parent.firstChild()
		n = 0
		while child:
			if child == self: return n
			n += 1 ; child = child.next()
		assert(false)
	#@nonl
	#@-node:childIndex
	#@+node:firstChild
	# Compatibility routine for scripts
	
	def firstChild (self):
	
		return self.mFirstChild
	#@nonl
	#@-node:firstChild
	#@+node:hasChildren
	def hasChildren (self):
	
		return self.firstChild() != None
	#@nonl
	#@-node:hasChildren
	#@+node:lastChild
	# Compatibility routine for scripts
	
	def lastChild (self):
	
		child = self.firstChild()
		while child and child.next():
			child = child.next()
		return child
	#@nonl
	#@-node:lastChild
	#@+node:nthChild
	# childIndex and nthChild are zero-based.
	
	def nthChild (self, n):
	
		child = self.firstChild()
		if not child: return None
		while n > 0 and child:
			n -= 1
			child = child.next()
		return child
	#@nonl
	#@-node:nthChild
	#@+node:numberOfChildren (n)
	def numberOfChildren (self):
	
		n = 0
		child = self.firstChild()
		while child:
			n += 1
			child = child.next()
		return n
	#@nonl
	#@-node:numberOfChildren (n)
	#@+node:isCloned
	def isCloned (self):
	
		return ( self.statusBits & vnode.clonedBit ) != 0
	#@nonl
	#@-node:isCloned
	#@+node:isDirty
	def isDirty (self):
	
		return self.t.isDirty()
	#@nonl
	#@-node:isDirty
	#@+node:isExpanded
	def isExpanded (self):
	
		return ( self.statusBits & self.expandedBit ) != 0
	#@nonl
	#@-node:isExpanded
	#@+node:isMarked
	def isMarked (self):
	
		return ( self.statusBits & vnode.markedBit ) != 0
	#@nonl
	#@-node:isMarked
	#@+node:isOrphan
	def isOrphan (self):
	
		return ( self.statusBits & vnode.orphanBit ) != 0
	#@nonl
	#@-node:isOrphan
	#@+node:isSelected
	def isSelected (self):
	
		return ( self.statusBits & vnode.selectedBit ) != 0
	#@nonl
	#@-node:isSelected
	#@+node:isTopBitSet
	def isTopBitSet (self):
	
		return ( self.statusBits & self.topBit ) != 0
	#@nonl
	#@-node:isTopBitSet
	#@+node:isVisible
	# Returns true if all parents are expanded.
	
	def isVisible (self):
	
		v = self.parent()
		while v:
			if not v.isExpanded():
				return false
			v = v.parent()
		return true
	#@nonl
	#@-node:isVisible
	#@+node:isVisited
	def isVisited (self):
	
		return ( self.statusBits & vnode.visitedBit ) != 0
	#@nonl
	#@-node:isVisited
	#@+node:status
	def status (self):
	
		return self.statusBits
	#@nonl
	#@-node:status
	#@+node:bodyString
	# Compatibility routine for scripts
	
	def bodyString (self):
	
		# This message should never be printed and we want to avoid crashing here!
		if not isUnicode(self.t.bodyString):
			s = "Leo internal error: not unicode:" + `self.t.bodyString`
			print s ; es(s,color="red")
	
		# Make _sure_ we return a unicode string.
		return toUnicode(self.t.bodyString,app.tkEncoding)
	#@nonl
	#@-node:bodyString
	#@+node:currentVnode (vnode)
	# Compatibility routine for scripts
	
	def currentVnode (self):
	
		return self.commands.frame.currentVnode()
	#@nonl
	#@-node:currentVnode (vnode)
	#@+node:edit_text
	def edit_text (self):
	
		v = self
		return self.commands.frame.getEditTextDict(v)
	#@nonl
	#@-node:edit_text
	#@+node:findRoot
	# Compatibility routine for scripts
	
	def findRoot (self):
	
		return self.commands.frame.rootVnode()
	#@-node:findRoot
	#@+node:headString & cleanHeadString
	def headString (self):
		
		"""Return the headline string."""
		
		# This message should never be printed and we want to avoid crashing here!
		if not isUnicode(self.t.headString):
			s = "Leo internal error: not unicode:" + `self.t.headString`
			print s ; es(s,color="red")
			
		# Make _sure_ we return a unicode string.
		return toUnicode(self.t.headString,app.tkEncoding)
	
	def cleanHeadString (self):
		
		s = self.headString()
		return toEncodedString(s,"ascii") # Replaces non-ascii characters by '?'
	#@nonl
	#@-node:headString & cleanHeadString
	#@+node:isAncestorOf
	def isAncestorOf (self, v):
	
		if not v:
			return false
		v = v.parent()
		while v:
			if v == self:
				return true
			v = v.parent()
		return false
	#@nonl
	#@-node:isAncestorOf
	#@+node:isRoot
	def isRoot (self):
	
		return not self.parent() and not self.back()
	#@nonl
	#@-node:isRoot
	#@+node:v.exists
	def exists(self,c):
		
		"""Return true if v exists in c's tree"""
		
		v = self ; c = v.commands
		
		# This code must be fast.
		root = c.rootVnode()
		while v:
			if v == root:
				return true
			p = v.parent()
			if p:
				v = p
			else:
				v = v.back()
			
		return false
	#@nonl
	#@-node:v.exists
	#@+node:appendStringToBody
	def appendStringToBody (self,s,encoding="utf-8"):
	
		if not s: return
		
		# Make sure the following concatenation doesn't fail.
		assert(isUnicode(self.t.bodyString)) # 9/28/03
		s = toUnicode(s,encoding) # 9/28/03
	
		body = self.t.bodyString + s
		self.setBodyStringOrPane(body,encoding)
	#@-node:appendStringToBody
	#@+node:setBodyStringOrPane & setBodyTextOrPane
	def setBodyStringOrPane (self,s,encoding="utf-8"):
	
		v = self ; c = v.commands
		if not c or not v: return
		
		s = toUnicode(s,encoding)
		if v == c.currentVnode():
			# This code destoys all tags, so we must recolor.
			c.frame.bodyCtrl.delete("1.0","end")
			c.frame.bodyCtrl.insert("1.0",s) # Replace the body text with s.
			c.recolor()
			
		# Keep the body text in the tnode up-to-date.
		if v.t.bodyString != s:
			v.t.setTnodeText(s)
			v.t.setSelection(0,0)
			v.setDirty()
			if not c.isChanged():
				c.setChanged(true)
	
	setBodyTextOrPane = setBodyStringOrPane # Compatibility with old scripts
	#@nonl
	#@-node:setBodyStringOrPane & setBodyTextOrPane
	#@+node:setHeadString & initHeadString
	def setHeadString (self,s,encoding="utf-8"):
	
		self.initHeadString(s,encoding) # 6/28/03
		self.setDirty()
	
	def initHeadString (self,s,encoding="utf-8"):
	
		s = toUnicode(s,encoding,reportErrors=true)
		self.t.headString = s
	#@-node:setHeadString & initHeadString
	#@+node:setHeadStringOrHeadline
	# Compatibility routine for scripts
	
	def setHeadStringOrHeadline (self,s,encoding="utf-8"):
	
		c = self.commands
		c.endEditing()
		self.setHeadString(s,encoding)
	#@-node:setHeadStringOrHeadline
	#@+node:computeIcon & setIcon
	def computeIcon (self):
	
		val = 0 ; v = self
		if v.t.hasBody(): val += 1
		if v.isMarked(): val += 2
		if v.isCloned(): val += 4
		if v.isDirty(): val += 8
		return val
		
	def setIcon (self):
	
		pass # Compatibility routine for old scripts
	#@nonl
	#@-node:computeIcon & setIcon
	#@+node:clearAllVisited
	# Compatibility routine for scripts
	
	def clearAllVisited (self):
		
		self.commands.clearAllVisited()
	#@-node:clearAllVisited
	#@+node:clearAllVisitedInTree
	def clearAllVisitedInTree (self):
	
		v = self ; c = v.commands
		after = v.nodeAfterTree()
		
		c.beginUpdate()
		while v and v != after:
			v.clearVisited()
			v.t.clearVisited()
			v = v.threadNext()
		c.endUpdate()
	#@-node:clearAllVisitedInTree
	#@+node:clearClonedBit
	def clearClonedBit (self):
	
		self.statusBits &= ~ self.clonedBit
	#@nonl
	#@-node:clearClonedBit
	#@+node:clearDirty & clearDirtyJoined (redundant code)
	def clearDirty (self):
	
		v = self
		v.t.clearDirty()
	
	def clearDirtyJoined (self):
	
		# trace()
		v = self ; c = v.commands
		c.beginUpdate()
		v.t.clearDirty()
		c.endUpdate() # recomputes all icons
	#@nonl
	#@-node:clearDirty & clearDirtyJoined (redundant code)
	#@+node:clearMarked
	def clearMarked (self):
	
		self.statusBits &= ~ self.markedBit
		doHook("clear-mark",c=self.commands,v=self)
	#@nonl
	#@-node:clearMarked
	#@+node:clearOrphan
	def clearOrphan (self):
	
		self.statusBits &= ~ self.orphanBit
	#@nonl
	#@-node:clearOrphan
	#@+node:clearVisited
	def clearVisited (self):
	
		self.statusBits &= ~ self.visitedBit
	#@nonl
	#@-node:clearVisited
	#@+node:clearVisitedInTree
	def clearVisitedInTree (self):
	
		after = self.nodeAfterTree()
		v = self
		while v and v != after:
			v.clearVisited()
			v = v.threadNext()
	#@nonl
	#@-node:clearVisitedInTree
	#@+node:contract & expand & initExpandedBit
	def contract(self):
	
		self.statusBits &= ~ self.expandedBit
	
	def expand(self):
	
		self.statusBits |= self.expandedBit
	
	def initExpandedBit (self):
	
		self.statusBits |= self.expandedBit
	#@nonl
	#@-node:contract & expand & initExpandedBit
	#@+node:initStatus
	def initStatus (self, status):
	
		self.statusBits = status
	#@nonl
	#@-node:initStatus
	#@+node:setAncestorsOfClonedNodesInTreeDirty
	#@+at 
	#@nonl
	# This is called from the key-event handler, so we must not force a redraw 
	# of the screen here. We avoid redraw in most cases by passing redraw_flag 
	# to the caller.
	# 
	# This marks v dirty and all cloned nodes in v's tree.
	# 
	# 2/1/03: I don't see how this can possibly be correct.
	# Why is it needed?? If it is needed, what about undo??
	#@-at
	#@@c
	def setAncestorsOfClonedNodesInTreeDirty(self):
	
		# Look up the tree for an ancestor @file node.
		v = self ; redraw_flag = false
		
		if v == None:
			return redraw_flag
			
		flag = v.setAncestorAtFileNodeDirty()
		if flag: redraw_flag = true
			
		next = v.nodeAfterTree()
		v = v.threadNext()
		while v and v != next:
			if v.isCloned() and not v.isDirty():
				flag = v.setAncestorAtFileNodeDirty()
				if flag: redraw_flag = true
				for v2 in v.t.joinList:
					if v2 != v:
						flag = v2.setAncestorAtFileNodeDirty()
						if flag: redraw_flag = true
			v = v.threadNext()
	
		return redraw_flag
	#@nonl
	#@-node:setAncestorsOfClonedNodesInTreeDirty
	#@+node:setAncestorAtFileNodeDirty
	#@+at 
	#@nonl
	# This is called from the key-event handler, so we must not force a redraw 
	# of the screen here. We avoid redraw in most cases by passing redraw_flag 
	# to c.endUpdate().
	# 
	# This is called from v.setDirty, so we avoid further calls to v.setDirty 
	# here.  The caller, that is, v.setDirty itself, handles all clones.
	# 
	#@-at
	#@@c
	def setAncestorAtFileNodeDirty(self):
	
		# Look up the tree for an ancestor @file node.
		v = self ; c = v.commands
		redraw_flag = false
		c.beginUpdate()
		while v:
			if not v.isDirty() and v.isAnyAtFileNode():
				# trace(v)
				redraw_flag = true
				v.t.setDirty() # Do not call v.setDirty here!
			v = v.parent()
		c.endUpdate(redraw_flag) # A crucial optimization: does nothing if inside nested begin/endUpdate.
		return redraw_flag # Allow caller to do the same optimization.
	#@nonl
	#@-node:setAncestorAtFileNodeDirty
	#@+node:setClonedBit & initClonedBit
	def setClonedBit (self):
	
		self.statusBits |= self.clonedBit
	
	def initClonedBit (self, val):
	
		if val:
			self.statusBits |= self.clonedBit
		else:
			self.statusBits &= ~ self.clonedBit
	#@nonl
	#@-node:setClonedBit & initClonedBit
	#@+node:setDirty, setDirtyDeleted & initDirtyBit (redundant code)
	#@+at 
	#@nonl
	# v.setDirty now ensures that all cloned nodes are marked dirty and that 
	# all ancestor @file nodes are marked dirty.  It is much safer to do it 
	# this way.
	#@-at
	#@@c
	
	def setDirty (self):
	
		v = self ; c = v.commands
		# trace(`v`)
		changed = false
		c.beginUpdate()
		if not v.t.isDirty():
			v.t.setDirty()
			changed = true
		# This must _always_ be called, even if v is already dirty.
		if v.setAncestorAtFileNodeDirty():
			changed = true
		for v2 in v.t.joinList:
			if v2 != v:
				assert(v2.t.isDirty())
				# Again, must always be called.
				if v2.setAncestorAtFileNodeDirty():
					changed = true
		c.endUpdate(changed)
		return changed
		
	def setDirtyDeleted (self):
		self.setDirty()
		return
	
	def initDirtyBit (self):
		self.t.setDirty()
	#@nonl
	#@-node:setDirty, setDirtyDeleted & initDirtyBit (redundant code)
	#@+node:setMarked & initMarkedBit
	def setMarked (self):
	
		self.statusBits |= self.markedBit
		doHook("set-mark",c=self.commands,v=self)
	
	def initMarkedBit (self):
	
		self.statusBits |= self.markedBit
	#@nonl
	#@-node:setMarked & initMarkedBit
	#@+node:setOrphan
	def setOrphan (self):
	
		self.statusBits |= self.orphanBit
	#@nonl
	#@-node:setOrphan
	#@+node:setSelected (vnode, new)
	# This only sets the selected bit.
	
	def setSelected (self):
	
		self.statusBits |= self.selectedBit
	#@nonl
	#@-node:setSelected (vnode, new)
	#@+node:setVisited
	# Compatibility routine for scripts
	
	def setVisited (self):
	
		self.statusBits |= self.visitedBit
	#@nonl
	#@-node:setVisited
	#@+node:setSelection
	def setSelection (self, start, length):
	
		self.t.setSelection ( start, length )
	#@nonl
	#@-node:setSelection
	#@+node:setT
	def setT (self, t):
	
		if t != self:
			del self.t
			self.t = t
	#@nonl
	#@-node:setT
	#@+node:trimTrailingLines
	#@+at 
	#@nonl
	# This trims trailing blank lines from a node.  It is surprising difficult 
	# to do this during Untangle.
	#@-at
	#@@c
	
	def trimTrailingLines (self):
	
		v = self
		body = v.bodyString()
		# trace(`body`)
		lines = string.split(body,'\n')
		i = len(lines) - 1 ; changed = false
		while i >= 0:
			line = lines[i]
			j = skip_ws(line,0)
			if j + 1 == len(line):
				del lines[i]
				i -= 1 ; changed = true
			else: break
		if changed:
			body = string.join(body,'') + '\n' # Add back one last newline.
			# trace(`body`)
			v.setBodyStringOrPane(body)
			# Don't set the dirty bit: it would just be annoying.
	#@nonl
	#@-node:trimTrailingLines
	#@+node:back
	# Compatibility routine for scripts
	
	def back (self):
	
		return self.mBack
	#@nonl
	#@-node:back
	#@+node:lastNode
	def lastNode (self):
	
		v = self
		level = self.level()
		result = None
	
		while v:
			result = v
			v = v.threadNext()
			if not v or v.level() <= level:
				break
	
		return result
	#@nonl
	#@-node:lastNode
	#@+node:level
	#@+at 
	#@nonl
	# This function returns the indentation level of the receiver. The root 
	# nodes have level 0, their children have level 1, and so on.
	#@-at
	#@@c
	
	def level (self):
	
		level = 0 ; parent = self.parent()
		while parent:
			level += 1
			parent = parent.parent()
		return level
	#@nonl
	#@-node:level
	#@+node:next
	# Compatibility routine for scripts
	
	def next (self):
	
		return self.mNext
	#@nonl
	#@-node:next
	#@+node:nodeAfterTree
	# Returns the vnode following the tree whose root is the receiver.
	
	def nodeAfterTree (self):
	
		next = self.next()
		p = self.parent()
	
		while not next and p:
			next = p.next()
			p = p.parent()
	
		return next
	#@nonl
	#@-node:nodeAfterTree
	#@+node:parent
	# Compatibility routine for scripts
	
	def parent (self):
	
		return self.mParent
	#@nonl
	#@-node:parent
	#@+node:threadBack
	def threadBack (self):
		
		"""Returns the previous element of the outline, or None if at the start of the outline"""
	
		back = self.back()
		if back:
			lastChild = back.lastChild()
			if lastChild:
				return lastChild.lastNode()
			else:
				return back
		else:
			return self.parent()
	#@nonl
	#@-node:threadBack
	#@+node:threadNext
	def threadNext (self):
	
		"""Returns node following the receiver in "threadNext" order"""
	
		# stat()
		v = self
		if v.firstChild():
			return v.firstChild()
		elif v.next():
			return v.next()
		else:
			p = v.parent()
			while p:
				if p.next():
					return p.next()
				p = p.parent()
			return None
	#@nonl
	#@-node:threadNext
	#@+node:visBack
	def visBack (self):
	
		v = self.threadBack()
		while v and not v.isVisible():
			v = v.threadBack()
		return v
	#@nonl
	#@-node:visBack
	#@+node:visNext
	def visNext (self):
	
		v = self.threadNext()
		while v and not v.isVisible():
			v = v.threadNext()
		return v
	#@nonl
	#@-node:visNext
	#@+node:doDelete
	#@+at 
	#@nonl
	# This is the main delete routine.  It deletes the receiver's entire tree 
	# from the screen.  Because of the undo command we never actually delete 
	# vnodes or tnodes.
	#@-at
	#@@c
	
	def doDelete (self, newVnode):
	
		"""Unlinks the receiver, but does not destroy it. May be undone"""
	
		v = self ; c = v.commands
		v.setDirty() # 1/30/02: mark @file nodes dirty!
		v.destroyDependents()
		v.unjoinTree()
		v.unlink()
		# Bug fix: 1/18/99: we must set the currentVnode here!
		c.selectVnode(newVnode)
		# Update all clone bits.
		c.initAllCloneBits()
		return self # We no longer need dvnodes: vnodes contain all needed info.
	#@nonl
	#@-node:doDelete
	#@+node:insertAfter
	def insertAfter (self,t=None):
	
		"""Inserts a new vnode after the receiver"""
	
		if not t:
			t = tnode(headString="NewHeadline")
		v = vnode(self.commands,t)
		v.iconVal = 0
		v.linkAfter(self)
		return v
	#@nonl
	#@-node:insertAfter
	#@+node:insertAsLastChild
	def insertAsLastChild (self,t=None):
	
		"""Inserts a new vnode as the last child of the receiver"""
	
		n = self.numberOfChildren()
		if not t:
			t = tnode(headString="NewHeadline")
		return self.insertAsNthChild(n,t)
	#@nonl
	#@-node:insertAsLastChild
	#@+node:insertAsNthChild
	def insertAsNthChild (self,n,t=None):
	
		"""Inserts a new node as the the nth child of the receiver.
		The receiver must have at least n-1 children"""
		
		# trace(`n` + `self`)
		if not t:
			t = tnode(headString="NewHeadline")
		v = vnode(self.commands,t)
		v.iconVal = 0
		v.linkAsNthChild(self,n)
		return v
	#@nonl
	#@-node:insertAsNthChild
	#@+node:moveToRoot
	def moveToRoot (self, oldRoot = None):
	
		"""Moves the receiver to the root position"""
	
		v = self
		v.destroyDependents()
		v.unlink()
		v.linkAsRoot(oldRoot)
		v.createDependents()
	#@nonl
	#@-node:moveToRoot
	#@+node:restoreOutlineFromDVnodes (test)
	# Restores (relinks) the dv tree in the position described by back and parent.
	
	def restoreOutlineFromDVnodes (self, dv, parent, back):
	
		if back:
			dv.linkAfter(back)
		elif parent:
			dv.linkAsNthChild(parent, 0)
		else:
			dv.linkAsRoot()
		return dv
	#@nonl
	#@-node:restoreOutlineFromDVnodes (test)
	#@+node:v.clone
	# Creates a clone of back and insert it as the next sibling of back.
	
	def clone (self,back):
		
		clone = self.cloneTree(back)
		clone.createDependents()
	
		# Set the clone bit in all nodes joined to back.
		# This is not nearly enough.
		clone.setClonedBit()
		back.setClonedBit()
		for v in back.t.joinList:
			v.setClonedBit()
	
		return clone
	#@nonl
	#@-node:v.clone
	#@+node:v.linkAfter
	# Links the receiver after v.
	
	def linkAfter (self,v):
	
		# stat()
		self.mParent = v.mParent
		self.mBack = v
		self.mNext = v.mNext
		v.mNext = self
		if self.mNext:
			self.mNext.mBack = self
	#@nonl
	#@-node:v.linkAfter
	#@+node:v.linkAsNthChild
	def linkAsNthChild (self, p, n):
	
		"""Links the receiver as the n'th child of p"""
	
		v = self
		# stat() ; # trace(`v` + ", " + `p` + ", " + `n`)
		v.mParent = p
		if n == 0:
			v.mBack = None
			v.mNext = p.mFirstChild
			if p.mFirstChild:
				p.mFirstChild.mBack = v
			p.mFirstChild = v
		else:
			prev = p.nthChild(n-1) # zero based
			assert(prev)
			v.mBack = prev
			v.mNext = prev.mNext
			prev.mNext = v
			if v.mNext:
				v.mNext.mBack = v
	#@nonl
	#@-node:v.linkAsNthChild
	#@+node:v.linkAsRoot
	#@+at 
	#@nonl
	# Bug fix: 5/27/02.  We link in the rest of the tree only when oldRoot != 
	# None.  Otherwise, we are calling this routine from init code and we want 
	# to start with a pristine tree.
	#@-at
	#@@c
	def linkAsRoot(self, oldRoot = None):
	
		v = self ; c = v.commands
		# stat() ; # trace(`v`)
		# Bug fix 3/16/02:
		# Clear all links except the child link.
		# This allows a node with children to be moved up properly to the root position.
		# v.mFirstChild = None
		v.mParent = None
		v.mBack = None
		# 5/27/02
		if oldRoot: oldRoot.mBack = v
		v.mNext = oldRoot
		c.frame.setRootVnode(v)
	#@nonl
	#@-node:v.linkAsRoot
	#@+node:v.moveAfter
	# Used by scripts
	
	def moveAfter (self,a):
	
		"""Moves the receiver after a"""
	
		v = self ; c = self.commands
		v.destroyDependents()
		v.unlink()
		v.linkAfter(a)
		v.createDependents()
		
		# 5/27/02: Moving a node after another node can create a new root node.
		if not a.parent() and not a.back():
			c.frame.setRootVnode(a)
	#@nonl
	#@-node:v.moveAfter
	#@+node:v.moveToNthChildOf
	# Compatibility routine for scripts
	
	def moveToNthChildOf (self, p, n):
	
		"""Moves the receiver to the nth child of p"""
	
		v = self ; c = self.commands
	
		v.destroyDependents()
		v.unlink()
		v.linkAsNthChild(p, n)
		v.createDependents()
		
		# 5/27/02: Moving a node can create a new root node.
		if not p.parent() and not p.back():
			c.frame.setRootVnode(p)
	#@nonl
	#@-node:v.moveToNthChildOf
	#@+node:v.sortChildren
	def sortChildren (self):
	
		# Create a list of (headline,vnode) tuples
		v = self ; pairs = []
		child = v.firstChild()
		if not child: return
		while child:
			pairs.append((string.lower(child.headString()), child))
			child = child.next()
		# Sort the list on the headlines.
		pairs.sort()
		# Move the children.
		index = 0
		for headline,child in pairs:
			child.moveToNthChildOf(v,index)
			index += 1
	#@nonl
	#@-node:v.sortChildren
	#@+node:v.addTreeToJoinLists (new in 3.12 beta 2)
	def addTreeToJoinLists (self):
		
		"""Add each v of v's entire tree to v.t.joinList."""
		
		v = self ; after = v.nodeAfterTree()
		
		while v and v != after:
			if not v in v.t.joinList:
				v.t.joinList.append(v)
			v = v.threadNext()
	#@nonl
	#@-node:v.addTreeToJoinLists (new in 3.12 beta 2)
	#@+node:v.cloneTree
	def cloneTree (self, oldTree):
		
		"""Create a cloned tree after oldTree."""
	
		# Create a new tree following oldTree.
		newTree = oldTree.copyTree()
		newTree.linkAfter(oldTree)
		# Join the trees and copy clone bits.
		oldTree.joinTreeTo(newTree)
		oldTree.copyCloneBitsTo(newTree)
		return newTree
	#@nonl
	#@-node:v.cloneTree
	#@+node:v.copyCloneBitsTo
	# This methods propagates clone bits from the receiver's tree to tree2.
	
	def copyCloneBitsTo (self, tree2):
	
		tree1 = self
		assert(tree2)
		# Set the bit in the root.
		if tree1.isCloned():
			tree2.setClonedBit()
		else:
			tree2.clearClonedBit()
		# Recursively set the bits in all subtrees.
		child1 = tree1.firstChild()
		child2 = tree2.firstChild()
		while child1:
			assert(child2)
			if child1.isCloned():
				child2.setClonedBit()
			else:
				child2.clearClonedBit()
			child1 = child1.next()
			child2 = child2.next()
		assert(child2 == None)
	#@nonl
	#@-node:v.copyCloneBitsTo
	#@+node:v.copyTree
	# Rewritten 7/11/03.
	
	def copyTree (self):
		
		"""Returns a free-standing copy of a vnode and all its descendents.
		
		The new tree uses the same tnodes as the old,
		but the new vnodes are _not_ joined to the old nodes.
		That is, the new vnodes v do not appear on v.t.joinList."""
		
		c = self.commands ; old_v = self
		
		# trace(self)
		
		# Copy all fields of the root.
		new_v = vnode(c,old_v.t)
		new_v.t.headString = old_v.t.headString
		new_v.iconVal = old_v.iconVal
		assert(new_v not in new_v.t.joinList)
	
		# Recursively copy and link all children.
		old_child = old_v.firstChild()
		n = 0
		while old_child:
			new_child = old_child.copyTree()
			new_child.linkAsNthChild(new_v,n)
			assert(new_child not in new_child.t.joinList)
			n += 1
			old_child = old_child.next()
			
		return new_v
	#@-node:v.copyTree
	#@+node:v.copyTreeWithNewTnodes (new after 3.11.1) (not used at present)
	def copyTreeWithNewTnodes (self):
		
		"""Return a copy of self with all new tnodes"""
		
		c = self.commands
		# trace(`self`)
		
		# Create the root node.
		old_v = self
		new_v = vnode(c,tnode())
		new_v.t.headString = old_v.t.headString
		new_v.t.bodyString = old_v.t.bodyString
		
		# Recursively create all descendents.
		old_child = old_v.firstChild() ; n = 0
		while old_child:
			new_child = old_child.copyTreeWithNewTnodes()
			new_child.linkAsNthChild (new_v, n)
			n += 1
			old_child = old_child.next()
			
		# Return the root of the new tree.
		return new_v
	#@nonl
	#@-node:v.copyTreeWithNewTnodes (new after 3.11.1) (not used at present)
	#@+node:v.createDependents
	# This method creates all nodes that depend on the receiver.
	def createDependents (self):
	
		v = self ; parent = v.parent()
		if not parent: return
	
		# Copy v as the nth child of all nodes joined to parent.
		n = v.childIndex()
		
		# 7/11/03: work on copy of join list.
		joinList = parent.t.joinList[:]
		if parent in joinList:
			joinList.remove(parent)
	
		for p in joinList:
			# trace(n,p)
			copy = v.copyTree()
			copy.linkAsNthChild(p,n)
			v.joinTreeTo(copy)
	#@nonl
	#@-node:v.createDependents
	#@+node:v.destroyDependents
	# Destroys all dependent vnodes and tree nodes associated with the receiver.
	
	def destroyDependents (self):
		
		"""Destroy the nth child of all nodes joined to the receiver's parent.."""
	
		parent = self.parent()
		if not parent:
			# trace("no parent",self)
			return
	
		n = self.childIndex()
		
		# 7/11/03: work on copy of join list.
		joinList = parent.t.joinList[:]
		if parent in joinList:
			joinList.remove(parent)
		#trace(parent,joinList)
	
		for join in joinList:
			# trace(n,join)
			child = join.nthChild(n)
			if child:
				child.unjoinTree()
				child.unlink()
				child.destroyTree()
	#@nonl
	#@-node:v.destroyDependents
	#@+node:v.destroyTree (does nothing!)(Called only from destroy dependents)
	#@+at 
	#@nonl
	# This method destroys (irrevocably deletes) a vnode tree.
	# 
	# This code should be called only when it is no longer possible to undo a 
	# previous delete.  It is always valid to destroy dependent trees.
	#@-at
	#@@c
	
	def destroyTree (self):
	
		pass
	#@nonl
	#@-node:v.destroyTree (does nothing!)(Called only from destroy dependents)
	#@+node:v.invalidOutline
	def invalidOutline (self, message):
	
		s = "invalid outline: " + message + "\n"
		parent = self.parent()
	
		if parent:
			s += `parent`
		else:
			s += `self`
	
		alert ( s )
	#@nonl
	#@-node:v.invalidOutline
	#@+node:v.joinNodeTo (rewritten for 4.0)
	def joinNodeTo (self, v2):
		
		"""Add self or v2 to their common join list"""
	
		v1 = self
		assert(v1.t==v2.t)
		j = v1.t.joinList
		
		if v1 not in j:
			j.append(v1)
			
		if v2 not in j:
			j.append(v2)
	#@nonl
	#@-node:v.joinNodeTo (rewritten for 4.0)
	#@+node:v.joinTreeTo
	#@+at 
	#@nonl
	# This function joins all nodes in the receiver and tree2.  This code 
	# makes no assumptions about the two trees, and some or all of the nodes 
	# may already have been joined.  The assert's guarantee that both trees 
	# have the same topology.
	#@-at
	#@@c
	
	def joinTreeTo (self, tree2):
	
		tree1 = self
		assert(tree2)
		# Join the roots.
		tree1.joinNodeTo ( tree2 )
		# Recursively join all subtrees.
		child1 = tree1.firstChild()
		child2 = tree2.firstChild()
		while child1:
			assert(child2)
			child1.joinTreeTo(child2)
			child1 = child1.next()
			child2 = child2.next()
		assert(child2 == None)
	#@nonl
	#@-node:v.joinTreeTo
	#@+node:v.shouldBeClone
	#@+at 
	#@nonl
	# The receiver is a clone if and only it is structurally _dissimilar_ to a 
	# node joined to it.
	# 
	# Structurally _similar_ joined nodes have non-null, distinct and joined 
	# parents, and have the same child indices.
	#@-at
	#@@c
	
	def shouldBeClone (self):
		
		"""Returns True if the receiver should be a clone"""
		p = self.parent()
		n = self.childIndex()
	
		for v in self.t.joinList:
			if v != self:
				vp = v.parent()
				# self and v are structurally dissimilar if...
				if( (not p or not vp) or  # they are at the top level, or
					vp == p or  # have the same parent, or
					p.t != vp.t or  # have unjoined parents, or
					(v.childIndex() != n)): # have different child indices.
	
					# trace("true",v)
					return true
	
		# The receiver is structurally similar to all nodes joined to it.
		# trace("false",v)
		return false
	#@nonl
	#@-node:v.shouldBeClone
	#@+node:v.unjoinTree
	def unjoinTree (self):
	
		"""Remove all v and all its descendents v from v.t.joinList."""
	
		v = self
		after = self.nodeAfterTree()
		while v and v != after:
			if v in v.t.joinList:
				v.t.joinList.remove(v)
			v = v.threadNext()
	#@nonl
	#@-node:v.unjoinTree
	#@+node:v.unlink
	def unlink (self):
	
		"""Unlinks the receiver from the tree before moving or deleting.
		
		The mFistChild link is not affected in the receiver."""
	
		v = self ; c = v.commands
	
		# stat() # trace(`v.mParent`+", child:"+`v.mFirstChild`+", back:"+`v.mBack`+", next:"+`v.mNext`)
		
		# Special case the root
		if v == c.frame.rootVnode():
			if not v.mNext: return # Should never happen.
			c.frame.setRootVnode(v.mNext)
	
		# Clear the links in other nodes
		if v.mBack:
			v.mBack.mNext = v.mNext
		if v.mNext:
			v.mNext.mBack = v.mBack
		if v.mParent and v == v.mParent.mFirstChild:
			v.mParent.mFirstChild = v.mNext
	
		# Clear the links in this node
		v.mParent = v.mNext = v.mBack = None
	#@nonl
	#@-node:v.unlink
	#@+node:validateOutlineWithParent
	# This routine checks the structure of the receiver's tree.
	
	def validateOutlineWithParent (self, p):
	
		result = true # optimists get only unpleasant surprises.
		parent = self.parent()
		childIndex = self.childIndex()
		#@	<< validate parent ivar >>
		#@+node:<< validate parent ivar >>
		if parent != p:
			self.invalidOutline ( "Invalid parent link: " + parent.description() )
		#@nonl
		#@-node:<< validate parent ivar >>
		#@nl
		#@	<< validate childIndex ivar >>
		#@+node:<< validate childIndex ivar >>
		if p:
			if childIndex < 0:
				self.invalidOutline ( "missing childIndex" + childIndex )
			elif childIndex >= p.numberOfChildren():
				self.invalidOutline ( "missing children entry for index: " + childIndex )
		elif childIndex < 0:
			self.invalidOutline ( "negative childIndex" + childIndex )
		#@nonl
		#@-node:<< validate childIndex ivar >>
		#@nl
		#@	<< validate x ivar >>
		#@+node:<< validate x ivar >>
		if not self.t and p:
			self.invalidOutline ( "Empty t" )
		#@nonl
		#@-node:<< validate x ivar >>
		#@nl
	
		# Recursively validate all the children.
		child = self.firstChild()
		while child:
			r = child.validateOutlineWithParent ( self )
			if not r: result = false
			child = child.next()
		return result
	#@nonl
	#@-node:validateOutlineWithParent
	#@-others
	
class vnode (baseVnode):
	"""A class that implements vnodes."""
	pass
#@nonl
#@-node:class vnode
#@+node:class nodeIndices
# Indices are Python dicts containing 'id','loc','time' and 'n' keys.

class nodeIndices:
	
	"""A class to implement global node indices (gnx's)."""
	
	#@	@+others
	#@+node:nodeIndices.__init__
	def __init__ (self):
		
		"""ctor for nodeIndices class"""
	
		self.userId = app.leoID # 5/1/03: This never changes.
		self.defaultId = app.leoID # This probably will change.
		self.lastIndex = None
		self.timeString = None
	#@nonl
	#@-node:nodeIndices.__init__
	#@+node:areEqual
	def areEqual (self,gnx1,gnx2):
		
		"""Return True if all fields of gnx1 and gnx2 are equal"""
	
		id1,time1,n1 = gnx1
		id2,time2,n2 = gnx2
		return id1==id2 and time1==time2 and n1==n2
	#@nonl
	#@-node:areEqual
	#@+node:get/setDefaultId
	# These are used by the fileCommands read/write code.
	
	def getDefaultId (self):
		
		"""Return the id to be used by default in all gnx's"""
		return self.defaultId
		
	def setDefaultId (self,id):
		
		"""Set the id to be used by default in all gnx's"""
		self.defaultId = id
	#@-node:get/setDefaultId
	#@+node:getNewIndex
	def getNewIndex (self):
		
		"""Create a new gnx using self.timeString and self.lastIndex"""
		
		id = self.userId # Bug fix 5/1/03: always use the user's id for new ids!
		t = self.timeString
		assert(t)
		n = None
	
		# Set n if id and time match the previous index.
		last = self.lastIndex
		if last:
			lastId,lastTime,lastN = last
			if id==lastId and t==lastTime:
				if lastN == None: n = 1
				else: n = lastN + 1
	
		d = (id,t,n)
		self.lastIndex = d
		# trace(d)
		return d
	#@nonl
	#@-node:getNewIndex
	#@+node:isGnx
	def isGnx (self,gnx):
		try:
			id,t,n = gnx
			return t != None
		except:
			return false
	#@nonl
	#@-node:isGnx
	#@+node:scanGnx
	def scanGnx (self,s,i):
		
		"""Create a gnx from its string representation"""
		
		if type(s) != type("s"):
			return None,None,None
			
		s = s.strip()
	
		id,t,n = None,None,None
		i,id = skip_to_char(s,i,'.')
		if match(s,i,'.'):
			i,t = skip_to_char(s,i+1,'.')
			if match(s,i,'.'):
				i,n = skip_to_char(s,i+1,'.')
		# Use self.defaultId for missing id entries.
		if id == None or len(id) == 0:
			id = self.defaultId
		# Convert n to int.
		if n:
			try: n = int(n)
			except: pass
	
		return id,t,n
	#@nonl
	#@-node:scanGnx
	#@+node:setTimeString
	def setTimestamp (self):
	
		"""Set the timestamp string to be used by getNewIndex until further notice"""
	
		self.timeString = time.strftime(
			"%m%d%y%H%M%S", time.localtime()) # compact timestamp is best
	#@nonl
	#@-node:setTimeString
	#@+node:toString
	def toString (self,index,removeDefaultId=false):
		
		"""Convert a gnx (a tuple) to its string representation"""
	
		id,t,n = index
	
		if removeDefaultId and id == self.defaultId:
			id = ""
	
		if not n: # None or ""
			return "%s.%s" % (id,t)
		else:
			return "%s.%s.%d" % (id,t,n)
	#@nonl
	#@-node:toString
	#@-others
#@nonl
#@-node:class nodeIndices
#@-others
#@nonl
#@-node:@file leoNodes.py
#@-leo
