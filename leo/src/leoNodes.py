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

import leoGlobals as g
from leoGlobals import true,false

import string,time,types

#@+others
#@+node:class tnode
class baseTnode (object):
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
		self.scrollBarSpot = None # Previous value of scrollbar position.
		self.selectionLength = 0 # The length of the selected body text.
		self.selectionStart = 0 # The start of the selected body text.
		self.statusBits = 0 # status bits
	
		# Convert everything to unicode...
		self.headString = g.toUnicode(headString,g.app.tkEncoding)
		self.bodyString = g.toUnicode(bodyString,g.app.tkEncoding)
		
		self.vnodeList = [] # List of all vnodes pointing to this tnode.
		self._firstChild = None
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
		
		s = g.toUnicode(s,encoding,reportErrors=true)
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
	#@+node:setCloneIndex (used in 3.x)
	def setCloneIndex (self, index):
	
		self.cloneIndex = index
	#@nonl
	#@-node:setCloneIndex (used in 3.x)
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
class baseVnode (object):
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
			
			g.trace(self,other)
			return not (self is other) # Must return 0, 1 or -1
	#@nonl
	#@-node:v.__cmp__ (not used)
	#@+node:v.__init__
	def __init__ (self,c,t):
	
		assert(t)
		#@	<< initialize vnode data members >>
		#@+node:<< initialize vnode data members >>
		self.c = c # The commander for this vnode.
		self.t = t # The tnode.
		self.statusBits = 0 # status bits
		
		# Structure links.
		self._parent = self._next = self._back = None
		#@nonl
		#@-node:<< initialize vnode data members >>
		#@nl
	#@-node:v.__init__
	#@+node:v.__repr__ & v.__str__
	def __repr__ (self):
		
		if self.t:
			return "<vnode %d:'%s'>" % (id(self),self.t.headString)
		else:
			return "<vnode %d:NULL tnode>" % (id(self))
			
	__str__ = __repr__
	#@nonl
	#@-node:v.__repr__ & v.__str__
	#@+node:v.dump
	def dumpLink (self,link):
		return g.choose(link,link,"<none>")
	
	def dump (self,label=""):
		
		v = self
	
		if label:
			print '-'*10,label,v
		else:
			print "self    ",v.dumpLink(v)
			print "len(vnodeList)",len(v.t.vnodeList)
		print "_back   ",v.dumpLink(v._back)
		print "_next   ",v.dumpLink(v._next)
		print "_parent ",v.dumpLink(v._parent)
		print "t._child",v.dumpLink(v.t._firstChild)
	#@nonl
	#@-node:v.dump
	#@+node:afterHeadlineFileTypeName
	def afterHeadlineFileTypeName(self,s):
		
		h = self.headString()
	
		if s != "@file" and g.match_word(h,0,s):
			# No options are valid.
			return s,string.strip(h[len(s):])
	
		elif g.match(h,0,"@file"):
			i,atFileType,junk = g.scanAtFileOptions(h)
			return atFileType,h[i:].strip()
	
		else:
			return None,None
	#@nonl
	#@-node:afterHeadlineFileTypeName
	#@+node:afterHeadlineMatch
	def afterHeadlineMatch(self,s):
		
		atFileType,fileName = self.afterHeadlineFileTypeName(s)
		if s == atFileType:
			return fileName
		else:
			return ""
	#@nonl
	#@-node:afterHeadlineMatch
	#@+node:anyAtFileNodeName
	def anyAtFileNodeName (self):
		
		"""Return the file name following an @file node or an empty string."""
		
		# New in 4.2: do the fastest possible tests.
		h = self.headString()
	
		if g.match(h,0,"@file"):
			type,name = self.afterHeadlineFileTypeName("@file")
			if type and name: return name
			else:             return ""
		elif g.match(h,0,"@nosentinelsfile"):
			return self.afterHeadlineMatch("@nosentinelsfile")
		elif g.match(h,0,"@rawfile"):
			return self.afterHeadlineMatch("@rawfile")
		elif g.match(h,0,"@silentfile"):
			return self.afterHeadlineMatch("@silentfile")
		elif g.match(h,0,"@thinfile"):
			return self.afterHeadlineMatch("@thinfile")
		else:
			return ""
	#@nonl
	#@-node:anyAtFileNodeName
	#@+node:at...FileNodeName
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
		
	def atThinFileNodeName (self):
		return self.afterHeadlineMatch("@thinfile")
		
	# New names, less confusing
	atNoSentFileNodeName  = atNoSentinelsFileNodeName
	atNorefFileNodeName   = atRawFileNodeName
	atAsisFileNodeName     = atSilentFileNodeName
	#@nonl
	#@-node:at...FileNodeName
	#@+node:isAnyAtFileNode
	def isAnyAtFileNode (self):
		
		"""Return true if v is any kind of @file or related node."""
		
		# This routine should be as fast as possible.
		# It is called once for every vnode when writing a file.
	
		h = self.headString()
		return h and h[0] == '@' and self.anyAtFileNodeName()
	#@nonl
	#@-node:isAnyAtFileNode
	#@+node:isAt...FileNode
	def isAtFileNode (self):
		return g.choose(self.atFileNodeName(),true,false)
		
	def isAtNoSentinelsFileNode (self):
		return g.choose(self.atNoSentinelsFileNodeName(),true,false)
	
	def isAtRawFileNode (self): # @file-noref
		return g.choose(self.atRawFileNodeName(),true,false)
	
	def isAtSilentFileNode (self): # @file-asis
		return g.choose(self.atSilentFileNodeName(),true,false)
	
	def isAtThinFileNode (self):
		return g.choose(self.atThinFileNodeName(),true,false)
		
	# New names, less confusing:
	isAtNoSentFileNode = isAtNoSentinelsFileNode
	isAtNorefFileNode  = isAtRawFileNode
	isAtAsisFileNode   = isAtSilentFileNode
	#@nonl
	#@-node:isAt...FileNode
	#@+node:isAtIgnoreNode
	def isAtIgnoreNode (self):
	
		"""Returns true if the receiver contains @ignore in its body at the start of a line."""
	
		flag, i = g.is_special(self.t.bodyString, 0, "@ignore")
		return flag
	#@nonl
	#@-node:isAtIgnoreNode
	#@+node:isAtOthersNode
	def isAtOthersNode (self):
	
		"""Returns true if the receiver contains @others in its body at the start of a line."""
	
		flag, i = g.is_special(self.t.bodyString,0,"@others")
		return flag
	#@nonl
	#@-node:isAtOthersNode
	#@+node:matchHeadline
	def matchHeadline (self,pattern):
	
		"""Returns true if the headline matches the pattern ignoring whitespace and case.
		
		The headline may contain characters following the successfully matched pattern."""
	
		h = string.lower(self.headString())
		h = string.replace(h,' ','')
		h = string.replace(h,'\t','')
	
		s = string.lower(pattern)
		s = string.replace(s,' ','')
		s = string.replace(s,'\t','')
	
		# ignore characters in the headline following the match
		return s == h[0:len(s)]
	#@nonl
	#@-node:matchHeadline
	#@+node:Tree Traversal getters
	# These aren't very useful.
	#@nonl
	#@-node:Tree Traversal getters
	#@+node:v.back
	# Compatibility routine for scripts
	
	def back (self):
	
		return self._back
	#@nonl
	#@-node:v.back
	#@+node:v.next
	# Compatibility routine for scripts
	
	def next (self):
	
		return self._next
	#@nonl
	#@-node:v.next
	#@+node:v.childIndex
	def childIndex(self):
		
		v = self
	
		if not v._back:
			return 0
	
		n = 0 ; v = v._back
		while v:
			n += 1
			v = v._back
		return n
	#@nonl
	#@-node:v.childIndex
	#@+node:v.firstChild (changed for 4.2)
	def firstChild (self):
		
		return self.t._firstChild
	#@nonl
	#@-node:v.firstChild (changed for 4.2)
	#@+node:v.hasChildren
	def hasChildren (self):
	
		return self.firstChild() != None
	#@nonl
	#@-node:v.hasChildren
	#@+node:v.hasChildren & hasFirstChild
	def hasChildren (self):
		
		v = self
		return v.firstChild()
	
	hasFirstChild = hasChildren
	#@nonl
	#@-node:v.hasChildren & hasFirstChild
	#@+node:v.lastChild
	def lastChild (self):
	
		child = self.firstChild()
		while child and child.next():
			child = child.next()
		return child
	#@nonl
	#@-node:v.lastChild
	#@+node:v.nthChild
	# childIndex and nthChild are zero-based.
	
	def nthChild (self, n):
	
		child = self.firstChild()
		if not child: return None
		while n > 0 and child:
			n -= 1
			child = child.next()
		return child
	#@nonl
	#@-node:v.nthChild
	#@+node:v.numberOfChildren (n)
	def numberOfChildren (self):
	
		n = 0
		child = self.firstChild()
		while child:
			n += 1
			child = child.next()
		return n
	#@nonl
	#@-node:v.numberOfChildren (n)
	#@+node:v.isCloned (4.2)
	def isCloned (self):
		
		return len(self.t.vnodeList) > 1
	#@nonl
	#@-node:v.isCloned (4.2)
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
	#@+node:v.bodyString
	# Compatibility routine for scripts
	
	def bodyString (self):
	
		# This message should never be printed and we want to avoid crashing here!
		if not g.isUnicode(self.t.bodyString):
			s = "Leo internal error: not unicode:" + repr(self.t.bodyString)
			print s ; g.es(s,color="red")
	
		# Make _sure_ we return a unicode string.
		return g.toUnicode(self.t.bodyString,g.app.tkEncoding)
	#@-node:v.bodyString
	#@+node:v.currentVnode (and c.currentPosition 4.2)
	def currentPosition (self):
		return self.c.currentPosition()
			
	def currentVnode (self):
		return self.c.currentVnode()
	#@nonl
	#@-node:v.currentVnode (and c.currentPosition 4.2)
	#@+node:v.edit_text TO BE DELETED
	def edit_text (self):
	
		v = self ; c = v.c ; p = c.currentPosition()
		
		g.trace("ooooops")
		#import traceback ; traceback.print_stack()
		
		pairs = self.c.frame.tree.getEditTextDict(v)
		for p2,t2 in pairs:
			if p.equal(p2):
				# g.trace("found",t2)
				return t2
				
		return None
	#@nonl
	#@-node:v.edit_text TO BE DELETED
	#@+node:v.findRoot (4.2)
	def findRoot (self):
		
		return self.c.rootPosition()
	#@nonl
	#@-node:v.findRoot (4.2)
	#@+node:v.headString & v.cleanHeadString
	def headString (self):
		
		"""Return the headline string."""
		
		# This message should never be printed and we want to avoid crashing here!
		if not g.isUnicode(self.t.headString):
			s = "Leo internal error: not unicode:" + repr(self.t.headString)
			print s ; g.es(s,color="red")
			
		# Make _sure_ we return a unicode string.
		return g.toUnicode(self.t.headString,g.app.tkEncoding)
	
	def cleanHeadString (self):
		
		s = self.headString()
		return g.toEncodedString(s,"ascii") # Replaces non-ascii characters by '?'
	#@nonl
	#@-node:v.headString & v.cleanHeadString
	#@+node:v.directParents (new method in 4.2)
	def directParents (self):
		
		"""(New in 4.2) Return a list of all direct parent vnodes of a vnode.
		
		This is NOT the same as the list of ancestors of the vnode."""
		
		v = self
		
		if v._parent:
			return v._parent.t.vnodeList
		else:
			return []
	#@nonl
	#@-node:v.directParents (new method in 4.2)
	#@+node:v.Link/Unlink/Insert methods (used by file read logic)
	# These remain in 4.2: the file read logic calls these before creating positions.
	#@nonl
	#@-node:v.Link/Unlink/Insert methods (used by file read logic)
	#@+node:v.insertAfter
	def insertAfter (self,t=None):
	
		"""Inserts a new vnode after self"""
	
		if not t:
			t = tnode(headString="NewHeadline")
	
		v = vnode(self.c,t)
		v.linkAfter(self)
	
		return v
	#@nonl
	#@-node:v.insertAfter
	#@+node:v.insertAsNthChild
	def insertAsNthChild (self,n,t=None):
	
		"""Inserts a new node as the the nth child of the receiver.
		The receiver must have at least n-1 children"""
	
		if not t:
			t = tnode(headString="NewHeadline")
	
		v = vnode(self.c,t)
		v.linkAsNthChild(self,n)
	
		return v
	#@nonl
	#@-node:v.insertAsNthChild
	#@+node:v.linkAfter
	def linkAfter (self,v):
	
		"""Link self after v."""
		
		self._parent = v._parent
		self._back = v
		self._next = v._next
		v._next = self
		if self._next:
			self._next._back = self
	#@-node:v.linkAfter
	#@+node:v.linkAsNthChild
	def linkAsNthChild (self,pv,n):
	
		"""Links self as the n'th child of vnode pv"""
	
		v = self
		# g.trace(v,pv,n)
		v._parent = pv
		if n == 0:
			v._back = None
			v._next = pv.t._firstChild
			if pv.t._firstChild:
				pv.t._firstChild._back = v
			pv.t._firstChild = v
		else:
			prev = pv.nthChild(n-1) # zero based
			assert(prev)
			v._back = prev
			v._next = prev._next
			prev._next = v
			if v._next:
				v._next._back = v
	#@nonl
	#@-node:v.linkAsNthChild
	#@+node:v.linkAsRoot
	def linkAsRoot(self, oldRoot = None):
		
		"""Link a vnode as the root node and set the root _position_."""
	
		v = self ; c = v.c
	
		# Clear all links except the child link.
		v._parent = None
		v._back = None
		v._next = oldRoot
	
		# Link in the rest of the tree only when oldRoot != None.
		# Otherwise, we are calling this routine from init code and
		# we want to start with a pristine tree.
		if oldRoot: oldRoot._back = v
	
		newRoot = position(v,[])
		c.setRootPosition(newRoot)
	#@nonl
	#@-node:v.linkAsRoot
	#@+node:v.moveToRoot
	def moveToRoot (self, oldRoot = None):
	
		"""Moves the receiver to the root position"""
	
		v = self
	
		v.unlink()
		v.linkAsRoot(oldRoot)
		
		return v
	#@nonl
	#@-node:v.moveToRoot
	#@+node:v.unlink
	def unlink (self):
	
		"""Unlinks a vnode from the tree."""
	
		v = self ; c = v.c
	
		# g.trace(v._parent," child: ",v.t._firstChild," back: ", v._back, " next: ", v._next)
		
		# Special case the root.
		if v == c.rootPosition().v: # 3/11/04
			assert(v._next)
			newRoot = position(v._next,[])
			c.setRootPosition(newRoot)
	
		# Clear the links in other nodes.
		if v._back:
			v._back._next = v._next
		if v._next:
			v._next._back = v._back
	
		if v._parent and v == v._parent.t._firstChild:
			v._parent.t._firstChild = v._next
	
		# Clear the links in this node.
		v._parent = v._next = v._back = None
		# v.parentsList = []
	#@nonl
	#@-node:v.unlink
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
	
		g.trace()
		v = self ; c = v.c
		c.beginUpdate()
		v.t.clearDirty()
		c.endUpdate() # recomputes all icons
	#@nonl
	#@-node:clearDirty & clearDirtyJoined (redundant code)
	#@+node:clearMarked
	def clearMarked (self):
	
		self.statusBits &= ~ self.markedBit
		g.doHook("clear-mark",c=self.c,v=self)
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
	#@+node:setMarked & initMarkedBit
	def setMarked (self):
	
		self.statusBits |= self.markedBit
		g.doHook("set-mark",c=self.c,v=self)
	
	def initMarkedBit (self):
	
		self.statusBits |= self.markedBit
	#@-node:setMarked & initMarkedBit
	#@+node:setOrphan
	def setOrphan (self):
	
		self.statusBits |= self.orphanBit
	#@nonl
	#@-node:setOrphan
	#@+node:setSelected (vnode)
	# This only sets the selected bit.
	
	def setSelected (self):
	
		self.statusBits |= self.selectedBit
	#@nonl
	#@-node:setSelected (vnode)
	#@+node:t.setVisited
	# Compatibility routine for scripts
	
	def setVisited (self):
	
		self.statusBits |= self.visitedBit
	#@nonl
	#@-node:t.setVisited
	#@+node:v.computeIcon & setIcon
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
	#@-node:v.computeIcon & setIcon
	#@+node:v.initHeadString
	def initHeadString (self,s,encoding="utf-8"):
		
		v = self
	
		s = g.toUnicode(s,encoding,reportErrors=true)
		v.t.headString = s
	#@nonl
	#@-node:v.initHeadString
	#@+node:v.setSelection
	def setSelection (self, start, length):
	
		self.t.setSelection ( start, length )
	#@nonl
	#@-node:v.setSelection
	#@+node:v.setTnodeText
	def setTnodeText (self,s,encoding="utf-8"):
		
		return self.t.setTnodeText(s,encoding)
	#@nonl
	#@-node:v.setTnodeText
	#@+node:v.trimTrailingLines
	def trimTrailingLines (self):
	
		"""Trims trailing blank lines from a node.
		
		It is surprising difficult to do this during Untangle."""
	
		v = self
		body = v.bodyString()
		# g.trace(body)
		lines = string.split(body,'\n')
		i = len(lines) - 1 ; changed = false
		while i >= 0:
			line = lines[i]
			j = g.skip_ws(line,0)
			if j + 1 == len(line):
				del lines[i]
				i -= 1 ; changed = true
			else: break
		if changed:
			body = string.join(body,'') + '\n' # Add back one last newline.
			# g.trace(body)
			v.setBodyStringOrPane(body)
			# Don't set the dirty bit: it would just be annoying.
	#@-node:v.trimTrailingLines
	#@+node:v.extraAttributes & setExtraAttributes
	def extraAttributes (self):
	
		# New in 4.2: tnode list is in tnode.
		try:    tnodeList = self.t.tnodeList
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
	#@-others
	
class vnode (baseVnode):
	"""A class that implements vnodes."""
	pass
#@-node:class vnode
#@+node:class nodeIndices
# Indices are Python dicts containing 'id','loc','time' and 'n' keys.

class nodeIndices (object):
	
	"""A class to implement global node indices (gnx's)."""
	
	#@	@+others
	#@+node:nodeIndices.__init__
	def __init__ (self):
		
		"""ctor for nodeIndices class"""
	
		self.userId = g.app.leoID # 5/1/03: This never changes.
		self.defaultId = g.app.leoID # This probably will change.
		self.lastIndex = None
		self.timeString = None
	#@nonl
	#@-node:nodeIndices.__init__
	#@+node:areEqual
	def areEqual (self,gnx1,gnx2):
		
		"""Return true if all fields of gnx1 and gnx2 are equal"""
	
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
		# g.trace(d)
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
		
		if type(s) not in (type(""),type(u"")):
			g.es("scanGnx: unexpected index type:",type(s),s,color="red")
			return None,None,None
			
		s = s.strip()
	
		id,t,n = None,None,None
		i,id = g.skip_to_char(s,i,'.')
		if g.match(s,i,'.'):
			i,t = g.skip_to_char(s,i+1,'.')
			if g.match(s,i,'.'):
				i,n = g.skip_to_char(s,i+1,'.')
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
	#@+node:setTimeStamp
	def setTimestamp (self):
	
		"""Set the timestamp string to be used by getNewIndex until further notice"""
	
		self.timeString = time.strftime(
			"%Y%m%d%H%M%S", # Help comparisons; avoid y2k problems.
			time.localtime())
	#@nonl
	#@-node:setTimeStamp
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
#@-node:class nodeIndices
#@+node:class position
# Warning: this code implies substantial changes to code that uses them, both core and scripts.

class position (object):
	
	"""A class representing a position in a traversal of a tree containing shared tnodes."""

	#@	<< about the position class >>
	#@+node:<< about the position class >>
	#@+at 
	#@nonl
	# This class provides tree traversal methods that operate on positions, 
	# not vnodes.  Positions encapsulate the notion of present position within 
	# a traversal.
	# 
	# Positions consist of a vnode and a stack of parent nodes used to 
	# determine the next parent when a vnode has mutliple parents.
	# 
	# Calling, e.g., p.moveToThreadNext() results in p being an invalid 
	# position.  That is, p represents the position following the last node of 
	# the outline.  The test "if p" is the _only_ correct way to test whether 
	# a position p is valid.  In particular, tests like "if p is None" or "if 
	# p is not None" will not work properly.
	# 
	# The only changes to vnodes and tnodes needed to implement shared tnodes 
	# are:
	# 
	# - The firstChild field becomes part of tnodes.
	# - t.vnodes contains a list of all vnodes sharing the tnode.
	# 
	# The advantages of using shared tnodes:
	# 
	# - Leo no longer needs to create or destroy "dependent" trees when 
	# changing descendents of cloned trees.
	# - There is no need for join links and no such things as joined nodes.
	# 
	# These advantages are extremely important: Leo is now scalable to very 
	# large outlines.
	# 
	# An important complication is the need to avoid creating temporary 
	# positions while traversing trees:
	# - Several routines use p.vParentWithStack to avoid having to call 
	# tempPosition.moveToParent().
	#   These include p.level, p.isVisible, p.hasThreadNext and p.vThreadNext.
	# - p.moveToLastNode and p.moveToThreadBack use new algorithms that don't 
	# use temporary data.
	# - Several lookahead routines compute whether a position exists without 
	# computing the actual position.
	#@-at
	#@nonl
	#@-node:<< about the position class >>
	#@nl
	
	#@	@+others
	#@+node:p.__init__
	def __init__ (self,v,stack):
	
		"""Create a new position."""
		
		if v: self.c = v.c
		else: self.c = g.top()
		self.v = v
		assert(v is None or v.t)
		self.stack = stack[:] # Creating a copy here is safest and best.
		
		# Note: __getattr__ implements p.t.
	#@nonl
	#@-node:p.__init__
	#@+node:p.__cmp__
	def __cmp__(self,p2):
	
		"""Return 0 if two postions are equivalent."""
	
		# Use p.equal if speed is crucial.
		p1 = self
	
		if p2 is None: # Allow tests like "p == None"
			if p1.v: return 1 # not equal
			else:    return 0 # equal
	
		# Check entire stack quickly.
		# The stack contains vnodes, so this is not a recursive call.
		if p1.v != p2.v or p1.stack != p2.stack:
			return 1 # notEqual
	
		# This is slow: do this last!
		if p1.childIndex() != p2.childIndex():
			# Disambiguate clones having the same parents.
			return 1 # notEqual
	
		return 0 # equal
	#@nonl
	#@-node:p.__cmp__
	#@+node:p.equal
	def equal(self,p2):
	
		"""Return true if two postions are equivalent.
		
		Use this method when the speed comparisons is crucial
		
		N.B. Unlike __cmp__, p2 must not be None."""
	
		p1 = self
		
		# if g.app.trace: "equal",p1.v,p2.v
	
		# Check entire stack quickly.
		# The stack contains vnodes, so this does not call p.__cmp__.
		return (
			p1.v == p2.v and
			p1.stack == p2.stack and
			p1.childIndex() == p2.childIndex())
	#@nonl
	#@-node:p.equal
	#@+node:p.__getattr__  ON:  must be ON if use_plugins
	if 1: # Good for compatibility, bad for finding conversion problems.
	
		def __getattr__ (self,attr):
			
			"""Convert references to p.t into references to p.v.t.
			
			N.B. This automatically keeps p.t in synch with p.v.t."""
	
			if attr=="t":
				return self.v.t
			else:
				# Only called when normal lookup fails.
				raise AttributeError
	#@nonl
	#@-node:p.__getattr__  ON:  must be ON if use_plugins
	#@+node:p.__nonzero__
	#@+at
	# The test "if p" is the _only_ correct way to test whether a position p 
	# is valid.
	# In particular, tests like "if p is None" or "if p is not None" will not 
	# work properly.
	#@-at
	#@@c
	
	def __nonzero__ ( self):
		
		"""Return true if a position is valid."""
		
		# if g.app.trace: "__nonzero__",self.v
	
		return self.v is not None
	#@nonl
	#@-node:p.__nonzero__
	#@+node:p.__str__ and p.__repr__
	def __str__ (self):
		
		p = self
		
		if p.v:
			return "<pos %d lvl: %d [%d] %s>" % (id(p),p.level(),len(p.stack),p.v.headString())
		else:
			return "<pos %d        [%d] None>" % (id(p),len(p.stack))
			
	__repr__ = __str__
	#@nonl
	#@-node:p.__str__ and p.__repr__
	#@+node:p.dump & p.vnodeListIds
	def dumpLink (self,link):
	
		return g.choose(link,link,"<none>")
	
	def dump (self,label=""):
		
		p = self
	
		print '-'*10,label,p
	
		if p.v:
			p.v.dump() # Don't print a label
			
	def vnodeListIds (self):
		
		p = self
		return [id(v) for v in p.v.t.vnodeList]
	#@nonl
	#@-node:p.dump & p.vnodeListIds
	#@+node:p.Comparisons
	def anyAtFileNodeName         (self): return self.v.anyAtFileNodeName()
	def atFileNodeName            (self): return self.v.atFileNodeName()
	def atNoSentinelsFileNodeName (self): return self.v.atNoSentinelsFileNodeName()
	def atRawFileNodeName         (self): return self.v.atRawFileNodeName()
	def atSilentFileNodeName      (self): return self.v.atSilentFileNodeName()
	def atThinFileNodeName        (self): return self.v.atThinFileNodeName()
	
	# New names, less confusing
	atNoSentFileNodeName  = atNoSentinelsFileNodeName
	atNorefFileNodeName   = atRawFileNodeName
	atAsisFileNodeName    = atSilentFileNodeName
	
	def isAnyAtFileNode         (self): return self.v.isAnyAtFileNode()
	def isAtFileNode            (self): return self.v.isAtFileNode()
	def isAtIgnoreNode          (self): return self.v.isAtIgnoreNode()
	def isAtNoSentinelsFileNode (self): return self.v.isAtNoSentinelsFileNode()
	def isAtOthersNode          (self): return self.v.isAtOthersNode()
	def isAtRawFileNode         (self): return self.v.isAtRawFileNode()
	def isAtSilentFileNode      (self): return self.v.isAtSilentFileNode()
	def isAtThinFileNode        (self): return self.v.isAtThinFileNode()
	
	# New names, less confusing:
	isAtNoSentFileNode = isAtNoSentinelsFileNode
	isAtNorefFileNode  = isAtRawFileNode
	isAtAsisFileNode   = isAtSilentFileNode
	
	# Utilities.
	def matchHeadline (self,pattern): return self.v.matchHeadline(pattern)
	def afterHeadlineMatch (self,s): return self.v.afterHeadlineMatch(s)
	#@nonl
	#@-node:p.Comparisons
	#@+node:p.Extra Attributes
	def extraAttributes (self):
		
		return self.v.extraAttributes()
	
	def setExtraAttributes (self,data):
	
		return self.v.setExtraAttributes(data)
	#@nonl
	#@-node:p.Extra Attributes
	#@+node:p.Headline & body strings
	def bodyString (self):
		
		return self.v.bodyString()
	
	def headString (self):
		
		return self.v.headString()
		
	def cleanHeadString (self):
		
		return self.v.cleanHeadString()
	#@-node:p.Headline & body strings
	#@+node:p.Status bits
	def isDirty     (self): return self.v.isDirty()
	def isExpanded  (self): return self.v.isExpanded()
	def isMarked    (self): return self.v.isMarked()
	def isOrphan    (self): return self.v.isOrphan()
	def isSelected  (self): return self.v.isSelected()
	def isTopBitSet (self): return self.v.isTopBitSet()
	def isVisited   (self): return self.v.isVisited()
	def status      (self): return self.v.status()
	#@nonl
	#@-node:p.Status bits
	#@+node:p.edit_text
	def edit_text (self):
		
		p = self
		
		if self.c:
			# New in 4.2: the dictionary is a list of pairs(p,v)
			pairs = self.c.frame.tree.getEditTextDict(p.v)
			for p2,t2 in pairs:
				if p.equal(p2):
					# g.trace("found",t2)
					return t2
			return None
		else:
			return None
	#@nonl
	#@-node:p.edit_text
	#@+node:p.directParents
	def directParents (self):
		
		return self.v.directParents()
	#@-node:p.directParents
	#@+node:p.childIndex
	def childIndex(self):
		
		p = self ; v = p.v
		
		# This is time-critical code!
		
		# 3/25/04: Much faster code:
		if not v or not v._back:
			return 0
	
		n = 0 ; v = v._back
		while v:
			n += 1
			v = v._back
	
		return n
	#@nonl
	#@-node:p.childIndex
	#@+node:p.hasChildren
	def hasChildren(self):
		
		p = self
		# g.trace(p,p.v)
		return p.v and p.v.t and p.v.t._firstChild
	#@nonl
	#@-node:p.hasChildren
	#@+node:p.numberOfChildren
	def numberOfChildren (self):
		
		return self.v.numberOfChildren()
	#@-node:p.numberOfChildren
	#@+node:p.exists
	def exists(self,c):
		
		"""Return true if a position exists in c's tree"""
		
		p = self.copy()
		
		# This code must be fast.
		root = c.rootPosition()
		while p:
			if p == root:
				return true
			if p.hasParent():
				p.moveToParent()
			else:
				p.moveToBack()
			
		return false
	#@nonl
	#@-node:p.exists
	#@+node:p.findRoot
	def findRoot (self):
		
		return self.c.frame.rootPosition()
	#@nonl
	#@-node:p.findRoot
	#@+node:p.getX & vnode compatibility traversal routines
	# These methods are useful abbreviations.
	# Warning: they make copies of positions, so they should be used _sparingly_
	
	def getBack          (self): return self.copy().moveToBack()
	def getFirstChild    (self): return self.copy().moveToFirstChild()
	def getLastChild     (self): return self.copy().moveToLastChild()
	def getLastNode      (self): return self.copy().moveToLastNode()
	def getLastVisible   (self): return self.copy().moveToLastVisible()
	def getNext          (self): return self.copy().moveToNext()
	def getNodeAfterTree (self): return self.copy().moveToNodeAfterTree()
	def getNthChild    (self,n): return self.copy().moveToNthChild(n)
	def getParent        (self): return self.copy().moveToParent()
	def getThreadBack    (self): return self.copy().moveToThreadBack()
	def getThreadNext    (self): return self.copy().moveToThreadNext()
	def getVisBack       (self): return self.copy().moveToVisBack()
	def getVisNext       (self): return self.copy().moveToVisNext()
	
	# These are efficient enough now that iterators are the normal way to traverse the tree!
	
	back          = getBack
	firstChild    = getFirstChild
	lastChild     = getLastChild
	lastNode      = getLastNode
	lastVisible   = getLastVisible # New in 4.2 (was in tk tree code).
	next          = getNext
	nodeAfterTree = getNodeAfterTree
	nthChild      = getNthChild
	parent        = getParent
	threadBack    = getThreadBack
	threadNext    = getThreadNext
	visBack       = getVisBack
	visNext       = getVisNext
	#@nonl
	#@-node:p.getX & vnode compatibility traversal routines
	#@+node:p.hasX 
	def hasBack(self):
		return self.v and self.v._back
	
	hasFirstChild = hasChildren
		
	def hasNext(self):
		return self.v and self.v._next
		
	def hasParent(self):
		return self.v and self.v._parent is not None
		
	def hasThreadBack(self):
		return self.hasParent() or self.hasBack() # Much cheaper than computing the actual value.
		
	hasVisBack = hasThreadBack
	#@nonl
	#@-node:p.hasX 
	#@+node:hasThreadNext (the only complex hasX method)
	def hasThreadNext(self):
	
		p = self ; v = p.v
		if not p.v: return false
	
		if v.t._firstChild or v._next:
			return true
		else:
			n = len(p.stack)-1
			v,n = p.vParentWithStack(v,p.stack,n)
			while v:
				if v._next:
					return true
				v,n = p.vParentWithStack(v,p.stack,n)
			return false
	
	hasVisNext = hasThreadNext
	#@nonl
	#@-node:hasThreadNext (the only complex hasX method)
	#@+node:p.isAncestorOf
	def isAncestorOf (self, p2):
		
		p = self
		
		if 0: # Avoid the copies made in the iterator.
			for p3 in p2.parents_iter():
				if p3 == p:
					return true
	
		# Avoid calling p.copy() or copying the stack.
	 	v2 = p2.v ; n = len(p.stack)-1
		v2,n = p2.vParentWithStack(v2,p2.stack,n)
		while v2:
			if v2 == p.v:
				return true
			v2,n = p2.vParentWithStack(v2,p2.stack,n)
	
		return false
	#@nonl
	#@-node:p.isAncestorOf
	#@+node:p.isCloned
	def isCloned (self):
		
		return len(self.v.t.vnodeList) > 1
	#@nonl
	#@-node:p.isCloned
	#@+node:p.isRoot
	def isRoot (self):
		
		p = self
	
		return not p.hasParent() and not p.hasBack()
	#@nonl
	#@-node:p.isRoot
	#@+node:p.isVisible
	def isVisible (self):
		
		"""Return true if all of a position's parents are expanded."""
	
		# v.isVisible no longer exists.
		p = self
	
		# Avoid calling p.copy() or copying the stack.
		v = p.v ; n = len(p.stack)-1
	
		v,n = p.vParentWithStack(v,p.stack,n)
		while v:
			if not v.isExpanded():
				return false
			v,n = p.vParentWithStack(v,p.stack,n)
	
		return true
	#@nonl
	#@-node:p.isVisible
	#@+node:p.lastVisible & oldLastVisible
	def oldLastVisible(self):
		"""Move to the last visible node of the entire tree."""
		p = self.c.rootPosition()
		assert(p.isVisible())
		last = p.copy()
		while 1:
			if g.app.debug: g.trace(last)
			p.moveToVisNext()
			if not p: return last
			last = p.copy()
			
	def lastVisible(self):
		"""Move to the last visible node of the entire tree."""
		p = self.c.rootPosition()
		# Move to the last top-level node.
		while p.hasNext():
			if g.app.debug: g.trace(p)
			p.moveToNext()
		assert(p.isVisible())
		# Move to the last visible child.
		while p.hasChildren() and p.isExpanded():
			if g.app.debug: g.trace(p)
			p.moveToLastChild()
		assert(p.isVisible())
		if g.app.debug: g.trace(p)
		return p
	#@nonl
	#@-node:p.lastVisible & oldLastVisible
	#@+node:p.level & simpleLevel
	def simpleLevel(self):
		
		p = self ; level = 0
		for parent in p.parents_iter():
			level += 1
		return level
	
	def level(self,verbose=false):
		
		# if g.app.debug: simpleLevel = self.simpleLevel()
		
		p = self ; level = 0
		if not p: return level
			
		# Avoid calling p.copy() or copying the stack.
		v = p.v ; n = len(p.stack)-1
		while 1:
			assert(p)
			v,n = p.vParentWithStack(v,p.stack,n)
			if v:
				level += 1
				if verbose: g.trace(level,"level,n: %2d" % (level,n))
			else:
				if verbose: g.trace(level,"level,n: %2d" % (level,n))
				# if g.app.debug: assert(level==simpleLevel)
				return level
	#@nonl
	#@-node:p.level & simpleLevel
	#@+node: Status bits
	# Clone bits are no longer used.
	# Dirty bits are handled carefully by the position class.
	
	def clearMarked  (self): return self.v.clearMarked()
	def clearOrphan  (self): return self.v.clearOrphan()
	def clearVisited (self): return self.v.clearVisited()
	
	def contract (self): return self.v.contract()
	def expand   (self): return self.v.expand()
	
	def initExpandedBit    (self): return self.v.initExpandedBit()
	def initMarkedBit      (self): return self.v.initMarkedBit()
	def initStatus (self, status): return self.v.initStatus()
		
	def setMarked   (self): return self.v.setMarked()
	def setOrphan   (self): return self.v.setOrphan()
	def setSelected (self): return self.v.setSelected()
	def setVisited  (self): return self.v.setVisited()
	#@nonl
	#@-node: Status bits
	#@+node:p.computeIcon & p.setIcon
	def computeIcon (self):
		
		return self.v.computeIcon()
		
	def setIcon (self):
	
		pass # Compatibility routine for old scripts
	#@nonl
	#@-node:p.computeIcon & p.setIcon
	#@+node:p.setSelection
	def setSelection (self,start,length):
	
		return self.v.setSelection(start,length)
	#@nonl
	#@-node:p.setSelection
	#@+node:p.trimTrailingLines
	def trimTrailingLines (self):
	
		return self.v.trimTrailingLines()
	#@nonl
	#@-node:p.trimTrailingLines
	#@+node:p.setTnodeText
	def setTnodeText (self,s,encoding="utf-8"):
		
		return self.v.setTnodeText(s,encoding)
	#@nonl
	#@-node:p.setTnodeText
	#@+node:p.appendStringToBody
	def appendStringToBody (self,s,encoding="utf-8"):
		
		p = self
		if not s: return
		
		body = p.bodyString()
		assert(g.isUnicode(body))
		s = g.toUnicode(s,encoding)
	
		p.setBodyStringOrPane(body + s,encoding)
	#@nonl
	#@-node:p.appendStringToBody
	#@+node:p.setBodyStringOrPane & p.setBodyTextOrPane
	def setBodyStringOrPane (self,s,encoding="utf-8"):
	
		p = self ; v = p.v ; c = p.c
		if not c or not v: return
	
		s = g.toUnicode(s,encoding)
		if p == c.currentPosition():
			# This code destoys all tags, so we must recolor.
			c.frame.body.setSelectionAreas(s,None,None)
			c.recolor()
			
		# Keep the body text in the tnode up-to-date.
		if v.t.bodyString != s:
			v.setTnodeText(s)
			v.t.setSelection(0,0)
			p.setDirty()
			if not c.isChanged():
				c.setChanged(true)
	
	setBodyTextOrPane = setBodyStringOrPane # Compatibility with old scripts
	#@nonl
	#@-node:p.setBodyStringOrPane & p.setBodyTextOrPane
	#@+node:p.setHeadString & p.initHeadString
	def setHeadString (self,s,encoding="utf-8"):
		
		p = self
		p.v.initHeadString(s,encoding)
		p.setDirty()
		
	def initHeadString (self,s,encoding="utf-8"):
		
		p = self
		p.v.initHeadString(s,encoding)
	#@-node:p.setHeadString & p.initHeadString
	#@+node:p.setHeadStringOrHeadline
	def setHeadStringOrHeadline (self,s,encoding="utf-8"):
	
		p = self
	
		p.c.endEditing()
		p.v.initHeadString(s,encoding)
		p.setDirty()
	#@nonl
	#@-node:p.setHeadStringOrHeadline
	#@+node:p.scriptSetBodyString
	def scriptSetBodyString (self,s,encoding="utf-8"):
		
		"""Update the body string for the receiver.
		
		Should be called only from scripts: does NOT update body text."""
	
		self.v.t.bodyString = g.toUnicode(s,encoding)
	#@nonl
	#@-node:p.scriptSetBodyString
	#@+node:p.clearAllVisited
	# Compatibility routine for scripts.
	
	def clearAllVisited (self):
		
		for p in self.allNodes_iter():
			p.clearVisited()
	#@nonl
	#@-node:p.clearAllVisited
	#@+node:p.clearVisitedInTree
	# Compatibility routine for scripts.
	
	def clearVisitedInTree (self):
		
		for p in self.self_and_subtree_iter():
			p.clearVisited()
	#@-node:p.clearVisitedInTree
	#@+node:clearAllVisitedInTree TO POSITION
	def clearAllVisitedInTree (self):
		
		for p in self.self_and_subtree_iter():
			p.v.clearVisited()
			p.v.t.clearVisited()
	#@nonl
	#@-node:clearAllVisitedInTree TO POSITION
	#@+node:p.clearDirty
	def clearDirty (self):
	
		p = self
		p.v.clearDirty()
	#@nonl
	#@-node:p.clearDirty
	#@+node:p.isDirty
	def isDirty (self):
		
		p = self
		return p.v and p.v.isDirty()
	#@nonl
	#@-node:p.isDirty
	#@+node:p.findAllPotentiallyDirtyNodes
	def findAllPotentiallyDirtyNodes(self):
		
		p = self
		
		# Start with all nodes in the vnodeList.
		nodes = []
		newNodes = p.v.t.vnodeList[:]
	
		# Add nodes until no more are added.
		while newNodes:
			# g.trace(len(newNodes))
			addedNodes = []
			nodes.extend(newNodes)
			for v in newNodes:
				for v2 in v.t.vnodeList:
					if v2 not in nodes and v2 not in addedNodes:
						addedNodes.append(v2)
					for v3 in v2.directParents(): # 3/23/04
						if v3 not in nodes and v3 not in addedNodes:
							addedNodes.append(v3)
			newNodes = addedNodes[:]
	
		# g.trace(nodes)
		return nodes
	#@nonl
	#@-node:p.findAllPotentiallyDirtyNodes
	#@+node:p.setAllAncestorAtFileNodesDirty
	def setAllAncestorAtFileNodesDirty (self):
	
		p = self ; c = p.c
		changed = false
		
		# Calculate all nodes that are joined to v or parents of such nodes.
		nodes = p.findAllPotentiallyDirtyNodes()
		
		c.beginUpdate()
		if 1: # update...
			for v in nodes:
				# g.trace(v.isAnyAtFileNode(),v.t.isDirty(),v)
				if not v.t.isDirty() and v.isAnyAtFileNode():
					changed = true
					v.t.setDirty() # Do not call v.setDirty here!
		c.endUpdate(changed)
		return changed
	#@nonl
	#@-node:p.setAllAncestorAtFileNodesDirty
	#@+node:p.setDirty
	# Ensures that all ancestor @file nodes are marked dirty.
	# It is much safer to do it this way.
	
	def setDirty (self):
	
		p = self ; c = p.c
	
		c.beginUpdate()
		if 1: # update...
			changed = false
			if not p.v.t.isDirty():
				p.v.t.setDirty()
				changed = true
			# This must be called even if p.v is already dirty.
			if p.setAllAncestorAtFileNodesDirty():
				changed = true
		c.endUpdate(changed)
	
		return changed
	#@nonl
	#@-node:p.setDirty
	#@+node:File Conversion
	#@+at
	# - convertTreeToString and moreHead can't be vnode methods because they 
	# uses level().
	# - moreBody could be anywhere: it may as well be a postion method.
	#@-at
	#@-node:File Conversion
	#@+node:convertTreeToString
	def convertTreeToString (self):
		
		"""Convert a positions  suboutline to a string in MORE format."""
	
		p = self ; level1 = p.level()
		
		g.trace()
		
		array = []
		for p in p.self_and_subtree_iter():
			array.append(p.moreHead(level1)+'\n')
			body = p.moreBody()
			if body:
				array.append(body +'\n')
	
		return ''.join(array)
	#@-node:convertTreeToString
	#@+node:moreHead
	def moreHead (self, firstLevel,useVerticalBar=false):
		
		"""Return the headline string in MORE format."""
	
		p = self
	
		level = self.level() - firstLevel
		plusMinus = g.choose(p.hasChildren(), "+", "-")
		
		return "%s%s %s" % ('\t'*level,plusMinus,p.headString())
	#@nonl
	#@-node:moreHead
	#@+node:moreBody
	#@+at 
	# 	+ test line
	# 	- test line
	# 	\ test line
	# 	test line +
	# 	test line -
	# 	test line \
	# 	More lines...
	#@-at
	#@@c
	
	def moreBody (self):
	
		"""Returns the body string in MORE format.  
		
		Inserts a backslash before any leading plus, minus or backslash."""
	
		p = self ; array = []
		lines = string.split(p.bodyString(),'\n')
		for s in lines:
			i = g.skip_ws(s,0)
			if i < len(s) and s[i] in ('+','-','\\'):
				s = s[:i] + '\\' + s[i:]
			array.append(s)
		return '\n'.join(array)
	#@nonl
	#@-node:moreBody
	#@+node:p.Iterators
	#@+at 
	#@nonl
	# 3/18/04: a crucial optimization:
	# 
	# Iterators make no copies at all if they would return an empty sequence.
	#@-at
	#@@c
	
	#@+others
	#@+node:allNodes_iter
	class allNodes_iter_class:
	
		"""Returns a list of positions in the entire outline."""
	
		#@	@+others
		#@+node:__init__ & __iter__
		def __init__(self,p,copy):
		
			self.first = p.c.rootPosition().copy()
			self.p = None
			self.copy = copy
			
		def __iter__(self):
		
			return self
		#@-node:__init__ & __iter__
		#@+node:next
		def next(self):
			
			if self.first:
				self.p = self.first
				self.first = None
		
			elif self.p:
				self.p.moveToThreadNext()
		
			if self.p:
				if self.copy: return self.p.copy()
				else:         return self.p
			else: raise StopIteration
		#@nonl
		#@-node:next
		#@-others
	
	def allNodes_iter (self,copy=false):
		
		return self.allNodes_iter_class(self,copy)
	#@nonl
	#@-node:allNodes_iter
	#@+node:subtree_iter
	class subtree_iter_class:
	
		"""Returns a list of positions in a subtree, possibly including the root of the subtree."""
	
		#@	@+others
		#@+node:__init__ & __iter__
		def __init__(self,p,copy,includeSelf):
			
			if includeSelf:
				self.first = p.copy()
				self.after = p.nodeAfterTree()
			elif p.hasChildren():
				self.first = p.copy().moveToFirstChild() 
				self.after = p.nodeAfterTree()
			else:
				self.first = None
				self.after = None
		
			self.p = None
			self.copy = copy
			
		def __iter__(self):
		
			return self
		#@-node:__init__ & __iter__
		#@+node:next
		def next(self):
			
			if self.first:
				self.p = self.first
				self.first = None
		
			elif self.p:
				self.p.moveToThreadNext()
		
			if self.p and self.p != self.after:
				if self.copy: return self.p.copy()
				else:         return self.p
			else:
				raise StopIteration
		#@nonl
		#@-node:next
		#@-others
	
	def subtree_iter (self,copy=false):
		
		return self.subtree_iter_class(self,copy,includeSelf=false)
		
	def self_and_subtree_iter (self,copy=false):
		
		return self.subtree_iter_class(self,copy,includeSelf=true)
	#@nonl
	#@-node:subtree_iter
	#@+node:children_iter
	class children_iter_class:
	
		"""Returns a list of children of a position."""
	
		#@	@+others
		#@+node:__init__ & __iter__
		def __init__(self,p,copy):
		
			if p.hasChildren():
				self.first = p.copy().moveToFirstChild()
			else:
				self.first = None
		
			self.p = None
			self.copy = copy
		
		def __iter__(self):
			
			return self
		#@-node:__init__ & __iter__
		#@+node:next
		def next(self):
			
			if self.first:
				self.p = self.first
				self.first = None
		
			elif self.p:
				self.p.moveToNext()
		
			if self.p:
				if self.copy: return self.p.copy()
				else:         return self.p
			else: raise StopIteration
		#@nonl
		#@-node:next
		#@-others
	
	def children_iter (self,copy=false):
		
		return self.children_iter_class(self,copy)
	#@nonl
	#@-node:children_iter
	#@+node:parents_iter
	class parents_iter_class:
	
		"""Returns a list of positions of a position."""
	
		#@	@+others
		#@+node:__init__ & __iter__
		def __init__(self,p,copy,includeSelf):
		
			if includeSelf:
				self.first = p.copy()
			elif p.hasParent():
				self.first = p.copy().moveToParent()
			else:
				self.first = None
		
			self.p = None
			self.copy = copy
		
		def __iter__(self):
		
			return self
		#@nonl
		#@-node:__init__ & __iter__
		#@+node:next
		def next(self):
			
			if self.first:
				self.p = self.first
				self.first = None
		
			elif self.p:
				self.p.moveToParent()
		
			if self.p:
				if self.copy: return self.p.copy()
				else:         return self.p
			else:
				raise StopIteration
		#@-node:next
		#@-others
	
	def parents_iter (self,copy=false):
		
		p = self
	
		return self.parents_iter_class(self,copy,includeSelf=false)
		
	def self_and_parents_iter(self,copy=false):
		
		return self.parents_iter_class(self,copy,includeSelf=true)
	#@nonl
	#@-node:parents_iter
	#@+node:siblings_iter
	class siblings_iter_class:
	
		"""Returns a list of siblings of a position."""
	
		#@	@+others
		#@+node:__init__ & __iter__
		def __init__(self,p,copy,following):
			
			# We always include p, even if following is true.
			
			if following:
				self.first = p.copy()
			else:
				p = p.copy()
				while p.hasBack():
					p.moveToBack()
				self.first = p
		
			self.p = None
			self.copy = copy
		
		def __iter__(self):
			
			return self
		
		#@-node:__init__ & __iter__
		#@+node:next
		def next(self):
			
			if self.first:
				self.p = self.first
				self.first = None
		
			elif self.p:
				self.p.moveToNext()
		
			if self.p:
				if self.copy: return self.p.copy()
				else:         return self.p
			else: raise StopIteration
		#@nonl
		#@-node:next
		#@-others
	
	def siblings_iter (self,copy=false,following=false):
		
		return self.siblings_iter_class(self,copy,following)
		
	self_and_siblings_iter = siblings_iter
		
	def following_siblings_iter (self,copy=false):
		
		return self.siblings_iter_class(self,copy,following=true)
	#@nonl
	#@-node:siblings_iter
	#@-others
	#@nonl
	#@-node:p.Iterators
	#@+node:p.doDelete
	#@+at 
	#@nonl
	# This is the main delete routine.  It deletes the receiver's entire tree 
	# from the screen.  Because of the undo command we never actually delete 
	# vnodes or tnodes.
	#@-at
	#@@c
	
	def doDelete (self,newPosition):
	
		"""Deletes position p from the outline.  May be undone.
	
		Returns newPosition."""
	
		p = self ; c = p.c
	
		assert(newPosition != p)
		p.setDirty() # Mark @file nodes dirty!
		p.unlink()
		p.deleteLinksInTree()
		c.selectVnode(newPosition)
		
		return newPosition
	
	#@-node:p.doDelete
	#@+node:p.insertAfter
	def insertAfter (self,t=None):
	
		"""Inserts a new vnode after self.
		
		Returns the newly created position."""
		
		p = self ; c = p.c
		p2 = self.copy()
	
		if not t:
			t = tnode(headString="NewHeadline")
	
		p2.v = vnode(c,t)
		p2.v.iconVal = 0
		p2.linkAfter(p)
	
		return p2
	#@nonl
	#@-node:p.insertAfter
	#@+node:p.insertAsLastChild
	def insertAsLastChild (self,t=None):
	
		"""Inserts a new vnode as the last child of self.
		
		Returns the newly created position."""
		
		p = self
		n = p.numberOfChildren()
	
		if not t:
			t = tnode(headString="NewHeadline")
		
		return p.insertAsNthChild(n,t)
	#@nonl
	#@-node:p.insertAsLastChild
	#@+node:p.insertAsNthChild
	def insertAsNthChild (self,n,t=None):
	
		"""Inserts a new node as the the nth child of self.
		self must have at least n-1 children.
		
		Returns the newly created position."""
		
		p = self ; c = p.c
		p2 = self.copy()
	
		if not t:
			t = tnode(headString="NewHeadline")
		
		p2.v = vnode(c,t)
		p2.v.iconVal = 0
		p2.linkAsNthChild(p,n)
	
		return p2
	#@nonl
	#@-node:p.insertAsNthChild
	#@+node:p.moveToRoot
	def moveToRoot (self,oldRoot=None):
	
		"""Moves a position to the root position."""
	
		p = self # Do NOT copy the position!
		p.unlink()
		p.linkAsRoot(oldRoot)
		
		return p
	#@nonl
	#@-node:p.moveToRoot
	#@+node:p.clone
	def clone (self,back):
		
		"""Create a clone of back.
		
		Returns the newly created position."""
		
		p = self ; c = p.c
		
		p2 = back.copy()
		p2.v = vnode(c,back.v.t)
		p2.linkAfter(back)
	
		return p2
	#@nonl
	#@-node:p.clone
	#@+node:p.copyTreeWithNewTnodes: used by unit tests TO DO
	if 0: # Not yet.
	
		def copyTreeWithNewTnodes (self):
			
			"""Return a copy of self with all new tnodes"""
			
			c = self.c
			
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
	#@-node:p.copyTreeWithNewTnodes: used by unit tests TO DO
	#@+node:p.moveAfter
	def moveAfter (self,a):
	
		"""Move a position after position a."""
		
		p = self ; c = p.c # Do NOT copy the position!
		p.unlink()
		p.linkAfter(a)
		
		# Moving a node after another node can create a new root node.
		if not a.hasParent() and not a.hasBack():
			c.setRootPosition(a)
	
		return p
	#@nonl
	#@-node:p.moveAfter
	#@+node:p.moveToLastChildOf
	def moveToLastChildOf (self,parent):
	
		"""Move a position to the last child of parent."""
	
		p = self # Do NOT copy the position!
	
		p.unlink()
		n = p.numberOfChildren()
		p.linkAsNthChild(parent,n)
	
		# Moving a node can create a new root node.
		if not parent.hasParent() and not parent.hasBack():
			p.c.setRootPosition(parent)
			
		return p
	#@-node:p.moveToLastChildOf
	#@+node:p.moveToNthChildOf
	def moveToNthChildOf (self,parent,n):
	
		"""Move a position to the nth child of parent."""
	
		p = self ; c = p.c # Do NOT copy the position!
		
		# g.trace(p,parent,n)
	
		p.unlink()
		p.linkAsNthChild(parent,n)
		
		# Moving a node can create a new root node.
		if not parent.hasParent() and not parent.hasBack():
			c.setRootPosition(parent)
			
		return p
	#@nonl
	#@-node:p.moveToNthChildOf
	#@+node:p.sortChildren
	def sortChildren (self):
		
		p = self
	
		# Create a list of (headline,position) tuples
		pairs = []
		for child in p.children_iter():
			pairs.append((string.lower(child.headString()),child.copy())) # do we need to copy?
	
		# Sort the list on the headlines.
		pairs.sort()
	
		# Move the children.
		index = 0
		for headline,child in pairs:
			child.moveToNthChildOf(p,index)
			index += 1
	#@nonl
	#@-node:p.sortChildren
	#@+node:p.validateOutlineWithParent
	# This routine checks the structure of the receiver's tree.
	
	def validateOutlineWithParent (self,pv):
		
		p = self
		result = true # optimists get only unpleasant surprises.
		parent = p.getParent()
		childIndex = p.childIndex()
		
		# g.trace(p,parent,pv)
		#@	<< validate parent ivar >>
		#@+node:<< validate parent ivar >>
		if parent != pv:
			p.invalidOutline( "Invalid parent link: " + repr(parent))
		#@nonl
		#@-node:<< validate parent ivar >>
		#@nl
		#@	<< validate childIndex ivar >>
		#@+node:<< validate childIndex ivar >>
		if pv:
			if childIndex < 0:
				p.invalidOutline ( "missing childIndex" + childIndex )
			elif childIndex >= pv.numberOfChildren():
				p.invalidOutline ( "missing children entry for index: " + childIndex )
		elif childIndex < 0:
			p.invalidOutline ( "negative childIndex" + childIndex )
		#@nonl
		#@-node:<< validate childIndex ivar >>
		#@nl
		#@	<< validate x ivar >>
		#@+node:<< validate x ivar >>
		if not p.v.t and pv:
			self.invalidOutline ( "Empty t" )
		#@nonl
		#@-node:<< validate x ivar >>
		#@nl
	
		# Recursively validate all the children.
		for child in p.children_iter():
			r = child.validateOutlineWithParent(p)
			if not r: result = false
	
		return result
	#@nonl
	#@-node:p.validateOutlineWithParent
	#@+node:p.invalidOutline
	def invalidOutline (self, message):
	
		s = "invalid outline: " + message + "\n"
		parent = self.getParent()
	
		if parent:
			s += repr(parent)
		else:
			s += repr(self)
	
		g.alert(s)
	#@nonl
	#@-node:p.invalidOutline
	#@+node:p.moveToX
	#@+at
	# These routines change self to a new position "in place".
	# That is, these methods must _never_ call p.copy().
	# 
	# When moving to a nonexistent position, these routines simply set p.v = 
	# None,
	# leaving the p.stack unchanged. This allows the caller to "undo" the 
	# effect of
	# the invalid move by simply restoring the previous value of p.v.
	# 
	# These routines all return self on exit so the following kind of code 
	# will work:
	# 	after = p.copy().moveToNodeAfterTree()
	#@-at
	#@nonl
	#@-node:p.moveToX
	#@+node:p.moveToBack
	def moveToBack (self):
		
		"""Move self to its previous sibling."""
		
		p = self
	
		p.v = p.v and p.v._back
		
		return p
	#@nonl
	#@-node:p.moveToBack
	#@+node:p.moveToFirstChild (pushes stack for cloned nodes)
	def moveToFirstChild (self):
	
		"""Move a position to it's first child's position."""
		
		p = self
	
		if p:
			child = p.v.t._firstChild
			if child:
				if p.isCloned():
					p.stack.append(p.v)
					# g.trace("push",p.v,p)
				p.v = child
			else:
				p.v = None
			
		return p
	
	#@-node:p.moveToFirstChild (pushes stack for cloned nodes)
	#@+node:p.moveToLastChild (pushes stack for cloned nodes)
	def moveToLastChild (self):
		
		"""Move a position to it's last child's position."""
		
		p = self
	
		if p:
			if p.v.t._firstChild:
				child = p.v.lastChild()
				if p.isCloned():
					p.stack.append(p.v)
					# g.trace("push",p.v,p)
				p.v = child
			else:
				p.v = None
				
		return p
	#@-node:p.moveToLastChild (pushes stack for cloned nodes)
	#@+node:p.moveToLastNode (Big improvement for 4.2)
	def moveToLastNode (self):
		
		"""Move a position to last node of its tree.
		
		N.B. Returns p if p has no children."""
		
		p = self
		
		# Huge improvement for 4.2.
		while p.hasChildren():
			p.moveToLastChild()
	
		return p
	#@nonl
	#@-node:p.moveToLastNode (Big improvement for 4.2)
	#@+node:p.moveToNext
	def moveToNext (self):
		
		"""Move a position to its next sibling."""
		
		p = self
		
		p.v = p.v and p.v._next
		
		return p
	#@nonl
	#@-node:p.moveToNext
	#@+node:p.moveToNodeAfterTree
	def moveToNodeAfterTree (self):
		
		"""Move a position to the node after the position's tree."""
		
		p = self
		
		while p:
			if p.hasNext():
				p.moveToNext()
				break
			p.moveToParent()
	
		return p
	#@-node:p.moveToNodeAfterTree
	#@+node:p.moveToNthChild (pushes stack for cloned nodes)
	def moveToNthChild (self,n):
		
		p = self
		
		if p:
			child = p.v.nthChild(n) # Must call vnode method here!
			if child:
				if p.isCloned():
					p.stack.append(p.v)
					# g.trace("push",p.v,p)
				p.v = child
			else:
				p.v = None
				
		return p
	#@nonl
	#@-node:p.moveToNthChild (pushes stack for cloned nodes)
	#@+node:p.moveToParent (pops stack when multiple parents)
	def moveToParent (self):
		
		"""Move a position to its parent position."""
		
		p = self
	
		if p.v._parent and len(p.v._parent.t.vnodeList) == 1:
			p.v = p.v._parent
		elif p.stack:
			p.v = p.stack.pop()
			# g.trace("pop",p.v,p)
		else:
			p.v = None
	
		return p
	#@nonl
	#@-node:p.moveToParent (pops stack when multiple parents)
	#@+node:p.moveToThreadBack
	def moveToThreadBack (self):
		
		"""Move a position to it's threadBack position."""
	
		p = self
	
		if p.hasBack():
			p.moveToBack()
			p.moveToLastNode()
		else:
			p.moveToParent()
	
		return p
	#@nonl
	#@-node:p.moveToThreadBack
	#@+node:p.moveToThreadNext
	def moveToThreadNext (self):
		
		"""Move a position to the next a position in threading order."""
		
		p = self
	
		if p:
			if p.v.t._firstChild:
				p.moveToFirstChild()
			elif p.v._next:
				p.moveToNext()
			else:
				p.moveToParent()
				while p:
					if p.v._next:
						p.moveToNext()
						break #found
					p.moveToParent()
				# not found.
					
		return p
	#@nonl
	#@-node:p.moveToThreadNext
	#@+node:p.moveToVisBack 
	def moveToVisBack (self):
		
		"""Move a position to the position of the previous visible node."""
	
		p = self
		
		if p:
			p.moveToThreadBack()
			while p and not p.isVisible():
				p.moveToThreadBack()
	
		assert(not p or p.isVisible())
		return p
	#@nonl
	#@-node:p.moveToVisBack 
	#@+node:p.moveToVisNext
	def moveToVisNext (self):
		
		"""Move a position to the position of the next visible node."""
	
		p = self
	
		p.moveToThreadNext()
		while p and not p.isVisible():
			p.moveToThreadNext()
				
		return p
	#@nonl
	#@-node:p.moveToVisNext
	#@+node:p.copy
	# Using this routine can generate huge numbers of temporary positions during a tree traversal.
	
	def copy (self):
		
		""""Return an independent copy of a position."""
		
		g.app.copies += 1
	
		return position(self.v,self.stack)
	#@nonl
	#@-node:p.copy
	#@+node:p.vParentWithStack
	# A crucial utility method.
	# The p.level(), p.isVisible() and p.hasThreadNext() methods show how to use this method.
	
	#@<< about the vParentWithStack utility method >>
	#@+node:<< about the vParentWithStack utility method >>
	#@+at 
	# This method allows us to simulate calls to p.parent() without generating 
	# any intermediate data.
	# 
	# For example, the code below will compute the same values for list1 and 
	# list2:
	# 
	# # The first way depends on the call to p.copy:
	# list1 = []
	# p=p.copy() # odious.
	# while p:
	# 	p = p.moveToParent()
	# 	if p: list1.append(p.v)
	# # The second way uses p.vParentWithStack to avoid all odious 
	# intermediate data.
	# 
	# list2 = []
	# n = len(p.stack)-1
	# v,n = p.vParentWithStack(v,p.stack,n)
	# while v:
	# 	list2.append(v)
	# 	v,n = p.vParentWithStack(v,p.stack,n)
	# 
	#@-at
	#@-node:<< about the vParentWithStack utility method >>
	#@nl
	
	def vParentWithStack(self,v,stack,n):
		
		"""A utility that allows the computation of p.v without calling p.copy().
		
		v,stack[:n] correspond to p.v,p.stack for some intermediate position p.
	
		Returns (v,n) such that v,stack[:n] correpond to the parent position of p."""
	
		if not v:
			return None,n
		elif v._parent and len(v._parent.t.vnodeList) == 1:
			return v._parent,n # don't change stack.
		elif stack and n >= 0:
			return self.stack[n],n-1 # simulate popping the stack.
		else:
			return None,n
	#@nonl
	#@-node:p.vParentWithStack
	#@+node:p.restoreLinksInTree
	def restoreLinksInTree (self):
	
		"""Restore links when undoing a delete node operation."""
		
		root = p = self
	
		if p.v not in p.v.t.vnodeList:
			p.v.t.vnodeList.append(p.v)
			
		for p in root.children_iter():
			p.restoreLinksInTree()
	#@nonl
	#@-node:p.restoreLinksInTree
	#@+node:p.deleteLinksInTree & allies
	def deleteLinksInTree (self):
		
		"""Delete and otherwise adjust links when deleting node."""
		
		root = self
	
		root.deleteLinksInSubtree()
		
		for p in root.children_iter():
			p.adjustParentLinksInSubtree(parent=root)
	#@nonl
	#@-node:p.deleteLinksInTree & allies
	#@+node:p.deleteLinksInSubtree
	def deleteLinksInSubtree (self):
	
		root = p = self
	
		# Delete p.v from the vnodeList
		if p.v in p.v.t.vnodeList:
			p.v.t.vnodeList.remove(p.v)
			assert(p.v not in p.v.t.vnodeList)
			g.trace("deleted",p.v,p.vnodeListIds())
		else:
			g.trace("not in vnodeList",p.v,p.vnodeListIds())
			pass
	
		if len(p.v.t.vnodeList) == 0:
			# This node is not shared by other nodes.
			for p in root.children_iter():
				p.deleteLinksInSubtree()
	#@nonl
	#@-node:p.deleteLinksInSubtree
	#@+node:p.adjustParentLinksInSubtree
	def adjustParentLinksInSubtree (self,parent):
		
		root = p = self
		
		assert(parent)
		
		if p.v._parent and parent.v.t.vnodeList and p.v._parent not in parent.v.t.vnodeList:
			p.v._parent = parent.v.t.vnodeList[0]
			
		for p in root.children_iter():
			p.adjustParentLinksInSubtree(parent=root)
	#@nonl
	#@-node:p.adjustParentLinksInSubtree
	#@+node:p.Link/Unlink methods
	# These remain in 4.2:  linking and unlinking does not depend on position.
	
	# These are private routines:  the position class does not define proxies for these.
	#@nonl
	#@-node:p.Link/Unlink methods
	#@+node:p.invalidOutline
	def invalidOutline (self, message):
		
		p = self
	
		if p.hasParent():
			node = p.parent()
		else:
			node = p
	
		g.alert("invalid outline: %s\n%s" % (message,node))
	#@nonl
	#@-node:p.invalidOutline
	#@+node:p.linkAfter
	def linkAfter (self,after):
	
		"""Link self after v."""
		
		p = self
		# g.trace(p,after)
		
		p.stack = after.stack[:] # 3/12/04
		p.v._parent = after.v._parent
		
		# Add v to it's tnode's vnodeList.
		if p.v not in p.v.t.vnodeList:
			p.v.t.vnodeList.append(p.v)
		
		p.v._back = after.v
		p.v._next = after.v._next
		
		after.v._next = p.v
		
		if p.v._next:
			p.v._next._back = p.v
	
		if 0:
			g.trace('-'*20,after)
			p.dump(label="p")
			after.dump(label="back")
			if p.hasNext(): p.next().dump(label="next")
	#@nonl
	#@-node:p.linkAfter
	#@+node:p.linkAsNthChild
	def linkAsNthChild (self,parent,n):
	
		"""Links self as the n'th child of vnode pv"""
		
		# g.trace(self,parent,n)
		p = self
	
		# Recreate the stack using the parent.
		p.stack = parent.stack[:] 
		if parent.isCloned():
			p.stack.append(parent.v)
	
		p.v._parent = parent.v
	
		# Add v to it's tnode's vnodeList.
		if p.v not in p.v.t.vnodeList:
			p.v.t.vnodeList.append(p.v)
	
		if n == 0:
			child1 = parent.v.t._firstChild
			p.v._back = None
			p.v._next = child1
			if child1:
				child1._back = p.v
			parent.v.t._firstChild = p.v
		else:
			prev = parent.nthChild(n-1) # zero based
			assert(prev)
			p.v._back = prev.v
			p.v._next = prev.v._next
			prev.v._next = p.v
			if p.v._next:
				p.v._next._back = p.v
				
		if 0:
			g.trace('-'*20)
			p.dump(label="p")
			parent.dump(label="parent")
	#@nonl
	#@-node:p.linkAsNthChild
	#@+node:p.linkAsRoot
	def linkAsRoot(self,oldRoot=None):
		
		"""Link self as the root node."""
		
		# g.trace(self,oldRoot)
	
		p = self ; v = p.v
		if oldRoot: oldRootVnode = oldRoot.v
		else:       oldRootVnode = None
		
		p.stack = [] # Clear the stack.
		
		# Clear all links except the child link.
		v._parent = None
		v._back = None
		v._next = oldRootVnode # Bug fix: 3/12/04
	
		# Link in the rest of the tree only when oldRoot != None.
		# Otherwise, we are calling this routine from init code and
		# we want to start with a pristine tree.
		if oldRoot:
			oldRoot.v._back = v # Bug fix: 3/12/04
	
		p.c.setRootPosition(p)
		
		if 0:
			p.dump(label="root")
	#@-node:p.linkAsRoot
	#@+node:p.unlink
	def unlink (self):
	
		"""Unlinks a position p from the tree before moving or deleting.
		
		The p.v._fistChild link does NOT change."""
	
		p = self ; v = p.v ; parent = p.parent()
		
		# Note:  p.parent() is not necessarily the same as v._parent.
		
		if parent:
			assert(p.v and p.v._parent in p.v.directParents())
			assert(parent.v in p.v.directParents())
	
		# g.trace("parent",parent," child:",v.t._firstChild," back:",v._back, " next:",v._next)
		
		# Special case the root.
		if p == p.c.rootPosition():
			assert(p.v._next)
			p.c.setRootPosition(p.next())
		
		# Remove v from it's tnode's vnodeList.
		vnodeList = v.t.vnodeList
		if v in vnodeList:
			vnodeList.remove(v)
		assert(v not in vnodeList)
		
		# Reset the firstChild link in its direct father.
		if parent and parent.v.t._firstChild == v:
			parent.v.t._firstChild = v._next
	
		# Do _not_ delete the links in any child nodes.
	
		# Clear the links in other nodes.
		if v._back: v._back._next = v._next
		if v._next: v._next._back = v._back
	
		# Unlink _this_ node.
		v._parent = v._next = v._back = None
	
		if 0:
			g.trace('-'*20)
			p.dump(label="p")
			if parent: parent.dump(label="parent")
	#@-node:p.unlink
	#@-others
#@-node:class position
#@-others
#@nonl
#@-node:@file leoNodes.py
#@-leo
