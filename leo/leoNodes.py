#@+leo
#@+node:0::@file leoNodes.py
#@+body
#@@language python


#@<< About the vnode and tnode classes >>
#@+node:1::<< About the vnode and tnode classes >>
#@+body
#@+at
#  The vnode and tnode classes represent most of the data contained in the 
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
# indirectly. Several classes, including the vnode, tnode, leoFrame and 
# leoTree classes, have destroy() routines. These destroy() routines merely 
# clear links so that Python's and Tkinter's reference counting mechanisms 
# will eventually delete vnodes, tnodes and other data when a window closes.
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
#@-body
#@-node:1::<< About the vnode and tnode classes >>


#@<< About clones >>
#@+node:2::<< About clones >>
#@+body
#@+at
#  This is the design document for clones in Leo. It covers all important 
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
# list with one pass through the vnodes.  Leo then convert each list to a 
# circular list with one additional pass through the tnodes.

#@-at
#@-body
#@-node:2::<< About clones >>


from leoGlobals import *
import types


#@+others
#@+node:3::class tnode
#@+body
class tnode:
	
	#@<< tnode constants >>
	#@+node:1::<< tnode constants >>
	#@+body
	dirtyBit =		0x01
	richTextBit =	0x02 # Determines whether we use <bt> or <btr> tags.
	visitedBit =	0x04
	#@-body
	#@-node:1::<< tnode constants >>


	#@+others
	#@+node:2::t.__init__
	#@+body
	# All params have defaults, so t = tnode() is valid.
	
	def __init__ (self, index = 0, bodyString = None):
	
		self.bodyString = choose(bodyString, bodyString, "")
		self.joinHead = None # The head of the join list while a file is being read.
		self.statusBits = 0 # status bits
		self.fileIndex = index # The immutable file index for self tnode.
		self.selectionStart = 0 # The start of the selected body text.
		self.selectionLength = 0 # The length of the selected body text.
		self.cloneIndex = 0 # Zero for @file nodes
		self.insertSpot = None # Location of previous insert point.
		self.scrollBarSpot = None # Previous value of scrollbar position.
	#@-body
	#@-node:2::t.__init__
	#@+node:3::t.__del__
	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "t.__del__"
		pass
	#@-body
	#@-node:3::t.__del__
	#@+node:4::t.destroy
	#@+body
	def destroy (self):
	
		self.joinHead = None
	#@-body
	#@-node:4::t.destroy
	#@+node:5::Getters
	#@+node:1::hasBody
	#@+body
	def hasBody (self):
	
		return self.bodyString and len(self.bodyString) > 0
	#@-body
	#@-node:1::hasBody
	#@+node:2::loadBodyPaneFromTnode
	#@+body
	def loadBodyPaneFromTnode(self, body):
	
		s = self.bodyString
		if s and len(s) > 0:
			body.delete(1,"end")
			body.insert(1,s)
		else:
			body.delete(1,"end")
	#@-body
	#@-node:2::loadBodyPaneFromTnode
	#@+node:3::Status bits
	#@+node:1::isDirty
	#@+body
	def isDirty (self):
	
		return (self.statusBits & self.dirtyBit) != 0
	#@-body
	#@-node:1::isDirty
	#@+node:2::isRichTextBit
	#@+body
	def isRichTextBit (self):
	
		return (self.statusBits & self.richTextBit) != 0
	#@-body
	#@-node:2::isRichTextBit
	#@+node:3::isVisited
	#@+body
	def isVisited (self):
	
		return (self.statusBits & self.visitedBit) != 0
	#@-body
	#@-node:3::isVisited
	#@-node:3::Status bits
	#@-node:5::Getters
	#@+node:6::Setters
	#@+node:1::Setting body text
	#@+node:1::saveBodyPaneToTnode
	#@+body
	def saveBodyPaneToTnode (self, body):
	
		self.bodyString = body.GetValue()
		# Set the selection.
		i, j = body.GetSelection()
		if i > j:
			temp = i
			i = j
			j = temp
		self.selectionStart = i
		self.selectionLength = j - i
	#@-body
	#@-node:1::saveBodyPaneToTnode
	#@+node:2::setTnodeText
	#@+body
	# This sets the text in the tnode from the given string.
	
	def setTnodeText (self,s):
	
		s,junk = convertUnicodeToString(s)
		self.bodyString = s
	#@-body
	#@-node:2::setTnodeText
	#@+node:3::setSelection
	#@+body
	def setSelection (self, start, length):
	
		self.selectionStart = start
		self.selectionLength = length
	#@-body
	#@-node:3::setSelection
	#@-node:1::Setting body text
	#@+node:2::Status bits
	#@+node:1::clearDirty
	#@+body
	def clearDirty (self):
	
		self.statusBits &= ~ self.dirtyBit
	#@-body
	#@-node:1::clearDirty
	#@+node:2::clearRichTextBit
	#@+body
	def clearRichTextBit (self):
	
		self.statusBits &= ~ self.richTextBit
	#@-body
	#@-node:2::clearRichTextBit
	#@+node:3::clearVisited
	#@+body
	def clearVisited (self):
	
		self.statusBits &= ~ self.visitedBit
	#@-body
	#@-node:3::clearVisited
	#@+node:4::setDirty
	#@+body
	def setDirty (self):
	
		self.statusBits |= self.dirtyBit
	#@-body
	#@-node:4::setDirty
	#@+node:5::setRichTextBit
	#@+body
	def setRichTextBit (self):
	
		self.statusBits |= self.richTextBit
	#@-body
	#@-node:5::setRichTextBit
	#@+node:6::setVisited
	#@+body
	def setVisited (self):
	
		self.statusBits |= self.visitedBit
	#@-body
	#@-node:6::setVisited
	#@-node:2::Status bits
	#@+node:3::setCloneIndex
	#@+body
	def setCloneIndex (self, index):
	
		self.cloneIndex = index
	#@-body
	#@-node:3::setCloneIndex
	#@+node:4::setFileIndex
	#@+body
	def setFileIndex (self, index):
	
		self.fileIndex = index
	#@-body
	#@-node:4::setFileIndex
	#@+node:5::setJoinHead
	#@+body
	def setJoinHead (self, v):
	
		self.joinHead = v
	#@-body
	#@-node:5::setJoinHead
	#@-node:6::Setters
	#@-others
#@-body
#@-node:3::class tnode
#@+node:4::class vnode
#@+body
class vnode:
	
	#@<< vnode constants >>
	#@+node:1::<< vnode constants >>
	#@+body
	# Define the meaning of vnode status bits.
	
	# Archived...
	clonedBit	 = 0x01 # true: vnode has clone mark.
	# not used	 = 0x02
	expandedBit  = 0x04 # true: vnode is expanded.
	markedBit	 = 0x08 # true: vnode is marked
	orphanBit	 = 0x10 # true: vnode saved in .leo file, not derived file.
	selectedBit  = 0x20 # true: vnode is current vnode.
	topBit		 = 0x40 # true: vnode was top vnode when saved.
	
	# Not archived
	visitedBit	 = 0x80
	#@-body
	#@-node:1::<< vnode constants >>


	#@+others
	#@+node:2::v.__init__
	#@+body
	def __init__ (self, commands, t):
	
		assert(t and commands)
		
		#@<< initialize vnode data members >>
		#@+node:1::<< initialize vnode data members >>
		#@+body
		self.commands = commands # The commander for this vnode.
		self.joinList = None # vnodes on the same joinlist are updated together.
		self.t = t # The tnode, i.e., the body text.
		self.statusBits = 0 # status bits
		self.iconVal = -1 # The icon index.  -1 forces an update of icon.
		self.mHeadString = "" # The headline text.
		
		# Structure links
		self.mParent = self.mFirstChild = self.mNext = self.mBack = None
		
		# Canvas items.  Set by tree.redraw
		self.iconx, self.icony = 0,0 # Coords of icon so icon can be redrawn separately.
		self.edit_text = None # Essential: used by many parts of tree code.
		
		if 1:
			self.icon_id = None # 6/15/02: Now cleared in __del__
		
		if 0: # These links are harmful: they prevent old tree items from being recycled properly.
			self.box_id = None
			self.edit_text_id = None # The editable text field for this vnode.
		#@-body
		#@-node:1::<< initialize vnode data members >>

		if app().deleteOnClose:
			self.commands.tree.vnode_alloc_list.append(self)
	#@-body
	#@-node:2::v.__init__
	#@+node:3::v.__del__
	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "v.__del__" + `self`
		try:
			self.icon_id = None
		except: pass
	#@-body
	#@-node:3::v.__del__
	#@+node:4::vnode.__repr__
	#@+body
	def __repr__ (self):
	
		return "v: " + `self.mHeadString`
	#@-body
	#@-node:4::vnode.__repr__
	#@+node:5::vnode.__cmp__ (not used)
	#@+body
	if 0: # not used
		def __cmp__(self,other):
			
			trace(`self` + "," + `other`)
			return not (self is other) # Must return 0, 1 or -1
	#@-body
	#@-node:5::vnode.__cmp__ (not used)
	#@+node:6::v.destroy
	#@+body
	#@+at
	#  This routine immediately removes all links from this node to other 
	# objects.  We expect this routine to be called only from tree.destroy 
	# when a window is being closed.

	#@-at
	#@@c

	def destroy (self):
	
		# Can't trace while destroying.
		# print "v.destroy"
		self.commands = None
		self.joinList = None
		self.t.destroy()
		self.t = None
		self.mParent = self.mFirstChild = self.mNext = self.mBack = None
		self.edit_text = None
		if 0: # These no longer exist
			self.box_id = self.icon_id = self.edit_text_id = None
	#@-body
	#@-node:6::v.destroy
	#@+node:7::v.Callbacks
	#@+body
	#@+at
	#  These callbacks are vnode methods so we can pass the vnode back to the 
	# tree class.

	#@-at
	#@-body
	#@+node:1::OnBoxClick, OnIconDoubleClick
	#@+body
	# Called when the box is clicked.
	
	def OnBoxClick(self,event=None):
	
		self.commands.tree.OnBoxClick(self)
		
	# Called when the icon is double-clicked.
		
	def OnIconDoubleClick(self,event=None):
	
		self.commands.tree.OnIconDoubleClick(self)
	#@-body
	#@-node:1::OnBoxClick, OnIconDoubleClick
	#@+node:2::OnDrag
	#@+body
	def OnDrag(self,event=None):
		
		self.commands.tree.OnDrag(self,event)
	
	#@-body
	#@-node:2::OnDrag
	#@+node:3::OnEndDrag
	#@+body
	def OnEndDrag(self,event=None):
		
		self.commands.tree.OnEndDrag(self,event)
	
	#@-body
	#@-node:3::OnEndDrag
	#@+node:4::OnHeadlineClick & OnHeadlinePopup
	#@+body
	def OnHeadlineClick(self,event=None):
	
		self.commands.tree.OnActivate(self)
		
	def OnHeadlinePopup(self,event=None):
	
		self.commands.tree.OnActivate(self)
		self.commands.tree.OnPopup(self,event)
	
	#@-body
	#@-node:4::OnHeadlineClick & OnHeadlinePopup
	#@+node:5::OnHeadlineKey
	#@+body
	def OnHeadlineKey (self,event):
	
		self.commands.tree.OnHeadlineKey(self,event)
	#@-body
	#@-node:5::OnHeadlineKey
	#@+node:6::OnHyperLinkControlClick
	#@+body
	def OnHyperLinkControlClick (self,event):
	
		c = self.commands ; v = self
		c.beginUpdate()
		c.selectVnode(v)
		c.endUpdate()
		c.body.mark_set("insert","1.0")
	#@-body
	#@-node:6::OnHyperLinkControlClick
	#@+node:7::OnHyperLinkEnter
	#@+body
	def OnHyperLinkEnter (self,event):
	
		if 0: # This works, and isn't very useful.
			c = self.commands ; v = self
			c.body.tag_config(v.tagName,background="green")
	#@-body
	#@-node:7::OnHyperLinkEnter
	#@+node:8::OnHyperLinkLeave
	#@+body
	def OnHyperLinkLeave (self,event):
	
		if 0: # This works, and isn't very useful.
			c = self.commands ; v = self
			c.body.tag_config(v.tagName,background="white")
	#@-body
	#@-node:8::OnHyperLinkLeave
	#@+node:9::v.OnIconClick
	#@+body
	def OnIconClick(self,event=None):
		
		self.commands.tree.OnIconClick(self,event)
	
	#@-body
	#@-node:9::v.OnIconClick
	#@-node:7::v.Callbacks
	#@+node:8::Comparisons (vnode)
	#@+node:1::afterHeadlineMatch
	#@+body
	# 12/03/02: We now handle @file options here.
	
	def afterHeadlineMatch(self,s):
		
		h = self.mHeadString
		
		if 1: # New code
			if s != "@file" and match_word(h,0,s):
				# No options are valid.
				return string.strip(h[len(s):])
			elif match(h,0,"@file"):
				i,atFileType = scanAtFileOptions(h)
				if s == atFileType:
					# print "s,h:",s,h
					return string.strip(h[i:])
				else: return ""
			else: return ""
		else:
			if match(h,0,s):
				return string.strip(h[len(s):])
			else:
				return ""
	
	#@-body
	#@-node:1::afterHeadlineMatch
	#@+node:2::at/../NodeName
	#@+body
	#@+at
	#  Returns the filename following @file or @rawfile, in the receivers's 
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
	
	#@-body
	#@-node:2::at/../NodeName
	#@+node:3::isAt/../Node
	#@+body
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
	
	#@-body
	#@-node:3::isAt/../Node
	#@+node:4::isAtIgnoreNode
	#@+body
	#@+at
	#  Returns true if the receiver contains @ignore in its body at the start 
	# of a line.

	#@-at
	#@@c

	def isAtIgnoreNode (self):
	
		flag, i = is_special(self.t.bodyString, 0, "@ignore")
		return flag
	#@-body
	#@-node:4::isAtIgnoreNode
	#@+node:5::isAtOthersNode
	#@+body
	#@+at
	#  Returns true if the receiver contains @others in its body at the start 
	# of a line.

	#@-at
	#@@c

	def isAtOthersNode (self):
	
		flag, i = is_special(self.t.bodyString,0,"@others")
		return flag
	#@-body
	#@-node:5::isAtOthersNode
	#@+node:6::matchHeadline
	#@+body
	#@+at
	#  Returns true if the headline matches the pattern ignoring whitespace 
	# and case.  The headline may contain characters following the 
	# successfully matched pattern.

	#@-at
	#@@c

	def matchHeadline (self,pattern):
	
		h = string.lower(self.mHeadString)
		h = string.replace(h,' ','')
		h = string.replace(h,'\t','')
	
		p = string.lower(pattern)
		p = string.replace(p,' ','')
		p = string.replace(p,'\t','')
	
		# ignore characters in the headline following the match
		return p == h[0:len(p)]
	#@-body
	#@-node:6::matchHeadline
	#@-node:8::Comparisons (vnode)
	#@+node:9::File Conversion (vnode)
	#@+node:1::convertTreeToString
	#@+body
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
	#@-body
	#@-node:1::convertTreeToString
	#@+node:2::moreHead
	#@+body
	# Returns the headline string in MORE format.
	
	def moreHead (self, firstLevel):
	
		v = self
		level = self.level() - firstLevel
		if level > 0: s = "\t" * level
		else: s = ""
		s += choose(v.hasChildren(), "+ ", "- ")
		s += v.headString()
		return s
	#@-body
	#@-node:2::moreHead
	#@+node:3::v.moreBody
	#@+body
	#@+at
	#  Returns the body string in MORE format.  It inserts a backslash before 
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
	#@-body
	#@-node:3::v.moreBody
	#@-node:9::File Conversion (vnode)
	#@+node:10::Getters
	#@+node:1::bodyString
	#@+body
	# Compatibility routine for scripts
	
	def bodyString (self):
	
		return self.t.bodyString
	#@-body
	#@-node:1::bodyString
	#@+node:2::Children
	#@+node:1::childIndex
	#@+body
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
	#@-body
	#@-node:1::childIndex
	#@+node:2::firstChild
	#@+body
	# Compatibility routine for scripts
	
	def firstChild (self):
	
		return self.mFirstChild
	#@-body
	#@-node:2::firstChild
	#@+node:3::hasChildren
	#@+body
	def hasChildren (self):
	
		return self.firstChild() != None
	#@-body
	#@-node:3::hasChildren
	#@+node:4::lastChild
	#@+body
	# Compatibility routine for scripts
	
	def lastChild (self):
	
		child = self.firstChild()
		while child and child.next():
			child = child.next()
		return child
	#@-body
	#@-node:4::lastChild
	#@+node:5::nthChild
	#@+body
	# childIndex and nthChild are zero-based.
	
	def nthChild (self, n):
	
		child = self.firstChild()
		if not child: return None
		while n > 0 and child:
			n -= 1
			child = child.next()
		return child
	#@-body
	#@-node:5::nthChild
	#@+node:6::numberOfChildren (n)
	#@+body
	def numberOfChildren (self):
	
		n = 0
		child = self.firstChild()
		while child:
			n += 1
			child = child.next()
		return n
	#@-body
	#@-node:6::numberOfChildren (n)
	#@-node:2::Children
	#@+node:3::currentVnode (vnode)
	#@+body
	# Compatibility routine for scripts
	
	def currentVnode (self):
	
		return self.commands.tree.currentVnode
	#@-body
	#@-node:3::currentVnode (vnode)
	#@+node:4::findRoot
	#@+body
	# Compatibility routine for scripts
	
	def findRoot (self):
	
		return self.commands.tree.rootVnode
	
	#@-body
	#@-node:4::findRoot
	#@+node:5::getJoinList
	#@+body
	def getJoinList (self):
	
		return self.joinList
	#@-body
	#@-node:5::getJoinList
	#@+node:6::headString
	#@+body
	# Compatibility routine for scripts
	
	def headString (self):
	
		return self.mHeadString
	
	
	#@-body
	#@-node:6::headString
	#@+node:7::isAncestorOf
	#@+body
	def isAncestorOf (self, v):
	
		if not v:
			return false
		v = v.parent()
		while v:
			if v == self:
				return true
			v = v.parent()
		return false
	#@-body
	#@-node:7::isAncestorOf
	#@+node:8::isRoot
	#@+body
	def isRoot (self):
	
		return not self.parent() and not self.back()
	#@-body
	#@-node:8::isRoot
	#@+node:9::Status Bits
	#@+node:1::isCloned
	#@+body
	def isCloned (self):
	
		return ( self.statusBits & vnode.clonedBit ) != 0
	#@-body
	#@-node:1::isCloned
	#@+node:2::isDirty
	#@+body
	def isDirty (self):
	
		return self.t.isDirty()
	#@-body
	#@-node:2::isDirty
	#@+node:3::isExpanded
	#@+body
	def isExpanded (self):
	
		return ( self.statusBits & self.expandedBit ) != 0
	#@-body
	#@-node:3::isExpanded
	#@+node:4::isMarked
	#@+body
	def isMarked (self):
	
		return ( self.statusBits & vnode.markedBit ) != 0
	#@-body
	#@-node:4::isMarked
	#@+node:5::isOrphan
	#@+body
	def isOrphan (self):
	
		return ( self.statusBits & vnode.orphanBit ) != 0
	#@-body
	#@-node:5::isOrphan
	#@+node:6::isSelected
	#@+body
	def isSelected (self):
	
		return ( self.statusBits & vnode.selectedBit ) != 0
	#@-body
	#@-node:6::isSelected
	#@+node:7::isTopBitSet
	#@+body
	def isTopBitSet (self):
	
		return ( self.statusBits & self.topBit ) != 0
	#@-body
	#@-node:7::isTopBitSet
	#@+node:8::isVisible
	#@+body
	# Returns true if all parents are expanded.
	
	def isVisible (self):
	
		v = self.parent()
		while v:
			if not v.isExpanded():
				return false
			v = v.parent()
		return true
	#@-body
	#@-node:8::isVisible
	#@+node:9::isVisited
	#@+body
	def isVisited (self):
	
		return ( self.statusBits & vnode.visitedBit ) != 0
	#@-body
	#@-node:9::isVisited
	#@+node:10::status
	#@+body
	def status (self):
	
		return self.statusBits
	#@-body
	#@-node:10::status
	#@-node:9::Status Bits
	#@+node:10::Structure Links
	#@+node:1::back
	#@+body
	# Compatibility routine for scripts
	
	def back (self):
	
		return self.mBack
	#@-body
	#@-node:1::back
	#@+node:2::lastNode
	#@+body
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
	#@-body
	#@-node:2::lastNode
	#@+node:3::level
	#@+body
	#@+at
	#  This function returns the indentation level of the receiver. The root 
	# nodes have level 0, their children have level 1, and so on.

	#@-at
	#@@c

	def level (self):
	
		level = 0 ; parent = self.parent()
		while parent:
			level += 1
			parent = parent.parent()
		return level
	#@-body
	#@-node:3::level
	#@+node:4::next
	#@+body
	# Compatibility routine for scripts
	
	def next (self):
	
		return self.mNext
	#@-body
	#@-node:4::next
	#@+node:5::nodeAfterTree
	#@+body
	# Returns the vnode following the tree whose root is the receiver.
	
	def nodeAfterTree (self):
	
		next = self.next()
		p = self.parent()
	
		while not next and p:
			next = p.next()
			p = p.parent()
	
		return next
	#@-body
	#@-node:5::nodeAfterTree
	#@+node:6::parent
	#@+body
	# Compatibility routine for scripts
	
	def parent (self):
	
		return self.mParent
	#@-body
	#@-node:6::parent
	#@+node:7::threadBack
	#@+body
	# Returns the previous element of the outline, or None if at the start of the outline.
	
	def threadBack (self):
	
		back = self.back()
		if back:
			lastChild = back.lastChild()
			if lastChild:
				return lastChild.lastNode()
			else:
				return back
		else:
			return self.parent()
	#@-body
	#@-node:7::threadBack
	#@+node:8::threadNext
	#@+body
	def threadNext (self):
	
		"""Returns node following the receiver in "threadNext" order.
		This should be called whenever v's links change"""
		
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
	#@-body
	#@-node:8::threadNext
	#@+node:9::visBack
	#@+body
	def visBack (self):
	
		v = self.threadBack()
		while v and not v.isVisible():
			v = v.threadBack()
		return v
	#@-body
	#@-node:9::visBack
	#@+node:10::visNext
	#@+body
	def visNext (self):
	
		v = self.threadNext()
		while v and not v.isVisible():
			v = v.threadNext()
		return v
	#@-body
	#@-node:10::visNext
	#@-node:10::Structure Links
	#@-node:10::Getters
	#@+node:11::Setters
	#@+node:1::Head and body text
	#@+node:1::appendStringToBody
	#@+body
	def appendStringToBody (self, s):
	
		if len(s) == 0: return
		body = self.t.bodyString + s
		self.setBodyStringOrPane(body)
	#@-body
	#@-node:1::appendStringToBody
	#@+node:2::setBodyStringOrPane & setBodyTextOrPane
	#@+body
	def setBodyStringOrPane (self,s):
	
		v = self ; c = v.commands
		if not c or not v: return
	
		if v == c.currentVnode():
			# This code destoys all tags, so we must recolor.
			c.frame.body.delete("1.0","end")
			c.frame.body.insert("1.0", s) # Replace the body text with s.
			c.recolor()
			
		if type(s) == types.UnicodeType: # 10/9/02
			xml_encoding = app().config.xml_version_string
			s = s.encode(xml_encoding) # result is a string.
		assert(type(s)==types.StringType)
	
		# Keep the body text in the tnode up-to-date.
		if v.t.bodyString != s: # 3/4/02
			v.t.setTnodeText(s)
			v.t.setSelection(0,0)
			v.setDirty()
			if not c.isChanged():
				c.setChanged(true)
	
	setBodyTextOrPane = setBodyStringOrPane # Compatibility with old scripts
	#@-body
	#@-node:2::setBodyStringOrPane & setBodyTextOrPane
	#@+node:3::setHeadString & initHeadString
	#@+body
	def setHeadString(self, s):
		s,junk = convertUnicodeToString(s)
		self.mHeadString = s
		self.setDirty()
	
	def initHeadString (self, s):
		s,junk = convertUnicodeToString(s)
		self.mHeadString = s
	
	#@-body
	#@-node:3::setHeadString & initHeadString
	#@+node:4::setHeadStringOrHeadline
	#@+body
	# Compatibility routine for scripts
	
	def setHeadStringOrHeadline (self, s):
	
		c = self.commands
		c.endEditing()
		self.setHeadString(s)
	#@-body
	#@-node:4::setHeadStringOrHeadline
	#@-node:1::Head and body text
	#@+node:2::computeIcon & setIcon
	#@+body
	def computeIcon (self):
	
		val = 0 ; v = self
		if v.t.hasBody(): val += 1
		if v.isMarked(): val += 2
		if v.isCloned(): val += 4
		if v.isDirty(): val += 8
		return val
		
	def setIcon (self):
	
		pass # Compatibility routine for old scripts
	#@-body
	#@-node:2::computeIcon & setIcon
	#@+node:3::Status bits
	#@+node:1::clearAllVisited
	#@+body
	# Compatibility routine for scripts
	
	def clearAllVisited (self):
		
		self.commands.clearAllVisited()
	
	#@-body
	#@-node:1::clearAllVisited
	#@+node:2::clearAllVisitedInTree
	#@+body
	def clearAllVisitedInTree (self):
	
		v = self ; c = v.commands
		after = v.nodeAfterTree()
		
		c.beginUpdate()
		while v and v != after:
			v.clearVisited()
			v.t.clearVisited()
			v = v.threadNext()
		c.endUpdate()
	
	#@-body
	#@-node:2::clearAllVisitedInTree
	#@+node:3::clearClonedBit
	#@+body
	def clearClonedBit (self):
	
		self.statusBits &= ~ self.clonedBit
	#@-body
	#@-node:3::clearClonedBit
	#@+node:4::clearDirty & clearDirtyJoined
	#@+body
	def clearDirty (self):
	
		v = self
		v.t.clearDirty()
	
	def clearDirtyJoined (self):
	
		v = self ; c = v.commands
		c.beginUpdate()
		if 1: # update range
			v.t.clearDirty()
			v2 = v.getJoinList()
			while v2 and v2 != self:
				v2.t.clearDirty()
				v2 = v2.getJoinList()
		c.endUpdate() # recomputes all icons
	#@-body
	#@-node:4::clearDirty & clearDirtyJoined
	#@+node:5::clearMarked
	#@+body
	def clearMarked (self):
	
		self.statusBits &= ~ self.markedBit
	#@-body
	#@-node:5::clearMarked
	#@+node:6::clearOrphan
	#@+body
	def clearOrphan (self):
	
		self.statusBits &= ~ self.orphanBit
	#@-body
	#@-node:6::clearOrphan
	#@+node:7::clearVisited
	#@+body
	def clearVisited (self):
	
		self.statusBits &= ~ self.visitedBit
	#@-body
	#@-node:7::clearVisited
	#@+node:8::clearVisitedInTree
	#@+body
	def clearVisitedInTree (self):
	
		after = self.nodeAfterTree()
		v = self
		while v and v != after:
			v.clearVisited()
			v = v.threadNext()
	#@-body
	#@-node:8::clearVisitedInTree
	#@+node:9::contract & expand & initExpandedBit
	#@+body
	def contract(self):
	
		self.statusBits &= ~ self.expandedBit
	
	def expand(self):
	
		self.statusBits |= self.expandedBit
	
	def initExpandedBit (self):
	
	    self.statusBits |= self.expandedBit
	#@-body
	#@-node:9::contract & expand & initExpandedBit
	#@+node:10::initStatus
	#@+body
	def initStatus (self, status):
	
		self.statusBits = status
	#@-body
	#@-node:10::initStatus
	#@+node:11::setAncestorsOfClonedNodesInTreeDirty
	#@+body
	#@+at
	#  This is called from the key-event handler, so we must not force a 
	# redraw of the screen here. We avoid redraw in most cases by passing 
	# redraw_flag to the caller.
	# 
	# This marks v dirty and all cloned nodes in v's tree.

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
				v2 = v.getJoinList()
				while v2 and v2 != v:
					flag = v2.setAncestorAtFileNodeDirty()
					if flag: redraw_flag = true
					v2 = v2.getJoinList()
			v = v.threadNext()
	
		return redraw_flag
	#@-body
	#@-node:11::setAncestorsOfClonedNodesInTreeDirty
	#@+node:12::setAncestorAtFileNodeDirty
	#@+body
	#@+at
	#  This is called from the key-event handler, so we must not force a 
	# redraw of the screen here. We avoid redraw in most cases by passing 
	# redraw_flag to c.endUpdate().
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
			if not v.isDirty() and (
				v.isAtFileNode() or v.isAtRawFileNode() or v.isAtNoSentinelsFileNode()):
				redraw_flag = true
				v.t.setDirty() # Do not call v.setDirty here!
			v = v.parent()
		c.endUpdate(redraw_flag) # A crucial optimization!
		return redraw_flag # Allow caller to do the same optimization.
	#@-body
	#@-node:12::setAncestorAtFileNodeDirty
	#@+node:13::setClonedBit & initClonedBit
	#@+body
	def setClonedBit (self):
	
		self.statusBits |= self.clonedBit
	
	def initClonedBit (self, val):
	
		if val:
			self.statusBits |= self.clonedBit
		else:
			self.statusBits &= ~ self.clonedBit
	#@-body
	#@-node:13::setClonedBit & initClonedBit
	#@+node:14::setDirty, setDirtyDeleted & initDirtyBit
	#@+body
	#@+at
	#  v.setDirty now ensures that all cloned nodes are marked dirty and that 
	# all ancestor @file nodes are marked dirty.  It is much safer to do it 
	# this way.
	# 
	# v.setDirtyDeleted is used only when a node is deleted.

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
		v2 = v.getJoinList()
		while v2 and v2 != v: 
			if not v2.t.isDirty():
				v2.t.setDirty()
				changed = true
			# Again, must always be called.
			if v2.setAncestorAtFileNodeDirty():
				changed = true
			v2 = v2.getJoinList()
		c.endUpdate(changed)
		return changed
		
	def setDirtyDeleted (self):
	
		v = self ; c = v.commands
		# trace(`v`)
		changed = false
		c.beginUpdate()
		if not v.t.isDirty():
			v.t.setDirty()
			changed = true
		# This must _always_ be called, even if v is already dirty.
		if v.setAncestorsOfClonedNodesInTreeDirty():
			changed = true
		v2 = v.getJoinList()
		while v2 and v2 != v: 
			if not v2.t.isDirty():
				v2.t.setDirty()
				changed = true
			# Again, must always be called.
			if v2.setAncestorsOfClonedNodesInTreeDirty():
				changed = true
			v2 = v2.getJoinList()
		c.endUpdate(changed)
		return changed
	
	def initDirtyBit (self):
		self.t.setDirty()
	#@-body
	#@-node:14::setDirty, setDirtyDeleted & initDirtyBit
	#@+node:15::setMarked & initMarkedBit
	#@+body
	def setMarked (self):
	
		self.statusBits |= self.markedBit
	
	def initMarkedBit (self):
	
		self.statusBits |= self.markedBit
	#@-body
	#@-node:15::setMarked & initMarkedBit
	#@+node:16::setOrphan
	#@+body
	def setOrphan (self):
	
		self.statusBits |= self.orphanBit
	#@-body
	#@-node:16::setOrphan
	#@+node:17::setSelected (vnode, new)
	#@+body
	# This only sets the selected bit.
	
	def setSelected (self):
	
		self.statusBits |= self.selectedBit
	#@-body
	#@-node:17::setSelected (vnode, new)
	#@+node:18::setVisited
	#@+body
	# Compatibility routine for scripts
	
	def setVisited (self):
	
		self.statusBits |= self.visitedBit
	#@-body
	#@-node:18::setVisited
	#@-node:3::Status bits
	#@+node:4::setJoinList
	#@+body
	def setJoinList (self, v):
	
		assert(not self.joinList)
		self.joinList = v
	#@-body
	#@-node:4::setJoinList
	#@+node:5::setSelection
	#@+body
	def setSelection (self, start, length):
	
		self.t.setSelection ( start, length )
	#@-body
	#@-node:5::setSelection
	#@+node:6::setT
	#@+body
	def setT (self, t):
	
		if t != self:
			del self.t
			self.t = t
	#@-body
	#@-node:6::setT
	#@+node:7::v.sortChildren
	#@+body
	def sortChildren (self):
		
		# Create a list of vnode, headline tuples
		v = self ; pairs = []
		child = v.firstChild()
		if not child: return
		while child:
			pairs.append((string.lower(child.headString()), child))
			child = child.next()
		# Sort the list on the headlines.
		sortedChildren = sortSequence(pairs,0)
		# Move the children.
		index = 0
		for headline,child in sortedChildren:
			child.moveToNthChildOf(v,index)
			index += 1
	#@-body
	#@-node:7::v.sortChildren
	#@+node:8::trimTrailingLines
	#@+body
	#@+at
	#  This trims trailing blank lines from a node.  It is surprising 
	# difficult to do this during Untangle.

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
	#@-body
	#@-node:8::trimTrailingLines
	#@-node:11::Setters
	#@+node:12::Moving, Inserting, Deleting, Cloning
	#@+node:1::Entry Points (vnode)
	#@+node:1::v.clone
	#@+body
	# Creates a clone of back and insert it as the next sibling of back.
	
	def clone (self,back):
	
		clone = self.cloneTree(back)
		clone.createDependents()
		# Set the clone bit in all nodes joined to back.
		clone.setClonedBit()
		back.setClonedBit()
		v = back.joinList
		while v and v != back:
			v.setClonedBit()
			v = v.joinList
		return clone
	#@-body
	#@-node:1::v.clone
	#@+node:2::doDelete
	#@+body
	#@+at
	#  This is the main delete routine.  It deletes the receiver's entire tree 
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
	#@-body
	#@-node:2::doDelete
	#@+node:3::insertAfter
	#@+body
	def insertAfter (self, t = None):
	
		"""Inserts a new vnode after the receiver"""
	
		if not t: t = tnode()
		v = vnode(self.commands,t)
		v.mHeadString = "NewHeadline"
		v.iconVal = 0
		v.linkAfter(self)
		return v
	#@-body
	#@-node:3::insertAfter
	#@+node:4::insertAsLastChild
	#@+body
	def insertAsLastChild (self,t = None):
	
		"""Inserts a new vnode as the last child of the receiver"""
	
		n = self.numberOfChildren()
		if not t:
			t = tnode()
		return self.insertAsNthChild(n,t)
	#@-body
	#@-node:4::insertAsLastChild
	#@+node:5::insertAsNthChild
	#@+body
	def insertAsNthChild (self, n, t=None):
	
		"""Inserts a new node as the the nth child of the receiver.
		The receiver must have at least n-1 children"""
	
		# trace(`n` + `self`)
		if not t: t = tnode()
		v = vnode(self.commands,t)
		v.mHeadString = "NewHeadline"
		v.iconVal = 0
		v.linkAsNthChild(self,n)
		return v
	#@-body
	#@-node:5::insertAsNthChild
	#@+node:6::moveAfter
	#@+body
	# Used by scripts
	
	def moveAfter (self,a):
	
		"""Moves the receiver after a"""
	
		v = self ; c = self.commands
		# trace(`v`)
		v.destroyDependents()
		v.unlink()
		v.linkAfter(a)
		v.createDependents()
		
		# 5/27/02: Moving a node after another node can create a new root node.
		if not a.parent() and not a.back():
			c.tree.rootVnode = a
	#@-body
	#@-node:6::moveAfter
	#@+node:7::moveToRoot
	#@+body
	def moveToRoot (self, oldRoot = None):
	
		"""Moves the receiver to the root position"""
	
		v = self
		# trace(`v`)
		v.destroyDependents()
		v.unlink()
		v.linkAsRoot(oldRoot)
		v.createDependents()
	#@-body
	#@-node:7::moveToRoot
	#@+node:8::moveToNthChildOf
	#@+body
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
			c.tree.rootVnode = p
	#@-body
	#@-node:8::moveToNthChildOf
	#@+node:9::restoreOutlineFromDVnodes (test)
	#@+body
	# Restores (relinks) the dv tree in the position described by back and parent.
	
	def restoreOutlineFromDVnodes (self, dv, parent, back):
	
		if back:
			dv.linkAfter(back)
		elif parent:
			dv.linkAsNthChild(parent, 0)
		else:
			dv.linkAsRoot()
		return dv
	#@-body
	#@-node:9::restoreOutlineFromDVnodes (test)
	#@+node:10::swap_links
	#@+body
	# 7/5/02: New for undo.
	# On entry, linked is linked into a tree and unlinked is not.
	# On exit,  unlinked is linked into a tree and linked is not.
	
	# Warning: caller is responsible for hanling join links properly.
	
	def swap_links (self,unlinked,linked):
	
		assert(unlinked and linked)
		assert(unlinked.mParent == None)
		assert(unlinked.mBack == None)
		assert(unlinked.mNext == None)
		assert(unlinked.joinList == None)
		#print "swap_links:unlinked.last,linked.last",`unlinked.lastChild()`,`linked.lastChild()`
	
		# Copy links to unlinked.
		unlinked.mParent = linked.mParent
		unlinked.mBack = linked.mBack
		unlinked.mNext = linked.mNext
		# Caller is responsible for handling join links.
		unlinked.joinList = None 
		
		# Change links to linked from other nodes.
		if linked.mParent and linked.mParent.mFirstChild == linked:
			linked.mParent.mFirstChild = unlinked
		if linked.mBack:
			linked.mBack.mNext = unlinked
		if linked.mNext:
			linked.mNext.mBack = unlinked
			
		# Clear links in linked.
		linked.mParent = linked.mBack = linked.mNext = linked.joinList = None
	#@-body
	#@-node:10::swap_links
	#@-node:1::Entry Points (vnode)
	#@+node:2::Public helper functions
	#@+node:1::v.copyTree
	#@+body
	#@+at
	#  This method copies all subtrees of oldRoot to the subtrees of newRoot.  
	# The caller is responsible for copying the headline text from oldRoot to newRoot.
	# 
	# This method must be given the new root as well as the old:  the 
	# wxWindows classes do not allow us to create an unattached outline.

	#@-at
	#@@c

	def copyTree (self, oldTree, newTree):
	
		old_v = oldTree.firstChild()
		if not old_v: return
		# Copy the first child of oldTree to the first child of newTree.
		new_v = newTree.insertAsNthChild (0, old_v.t)
		self.copyNode(old_v, new_v)
		# Copy all other children of oldTree after the first child of newTree.
		old_v = old_v.next()
		while old_v:
			new_v = new_v.insertAfter(old_v.t)
			self.copyNode(old_v, new_v)
			old_v = old_v.next()
		# Recursively copy all descendents of oldTree.
		new_v = newTree.firstChild()
		old_v = oldTree.firstChild()
		while old_v:
			assert(new_v)
			self.copyTree(old_v, new_v)
			old_v = old_v.next()
			new_v = new_v.next()
		assert(new_v == None)
	#@-body
	#@-node:1::v.copyTree
	#@+node:2::joinTreeTo
	#@+body
	#@+at
	#  This function joins all nodes in the receiver and tree2.  This code 
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
	#@-body
	#@-node:2::joinTreeTo
	#@+node:3::shouldBeClone
	#@+body
	#@+at
	#  This function returns true if the receiver should be a clone.  This can 
	# be done quickly using the receiver's join list.
	# 
	# The receiver is a clone if and only it is structurally _dissimilar_ to a 
	# node joined to it.  Structurally _similar_ joined nodes have non-null, 
	# distinct and joined parents, and have the same child indices.
	# 
	# 9/16/99 We now return the node that proves that the receiver should be a 
	# clone.  This allows us to dispense with the old "survivor" logic in commands::deleteHeadline.

	#@-at
	#@@c

	def shouldBeClone (self,verbose=0):
	
		p = self.parent()
		n = self.childIndex()
		if verbose:
			v = self.joinList
			es("shouldBeClone: self,self.parent():"+`self`+","+`self.parent()`)
			es("shouldBeClone: joinlist of self:")
			while v and v != self:
				es("v,v.parent():"+`v`+","+`v.parent()`)
				v=v.joinList
	
		v = self.joinList
		while v and v != self:
			vp = v.parent()
			if 0: # verbose:
				es("shouldBeClone:" + `v`)
				es("shouldBeClone: p,vp:" + `p` + "," + `vp`)
				es("shouldBeClone: join:" + `p.isJoinedTo(vp)`)
				es("shouldBeClone: indices:" + `n` + "," + `v.childIndex()`)
			if ( # self and v are sturcturally dissimilar if...
				(not p or not vp) or  # they are at the top level, or
				vp == p or  # have the same parent, or
				not p.isJoinedTo(vp) or  # have unjoined parents, or
				(v.childIndex() != n)): # have different child indices.
				if verbose: es("shouldBeClone returns true")
				return true
			v = v.joinList
	
		# The receiver is structurally similar to all nodes joined to it.
		if verbose: es("shouldBeClone returns false")
		return false
	#@-body
	#@-node:3::shouldBeClone
	#@+node:4::validateOutlineWithParent
	#@+body
	# This routine checks the structure of the receiver's tree.
	
	def validateOutlineWithParent (self, p):
	
		result = true # optimists get only unpleasant surprises.
		parent = self.parent()
		childIndex = self.childIndex()
		
		#@<< validate parent ivar >>
		#@+node:1::<< validate parent ivar >>
		#@+body
		if parent != p:
			self.invalidOutline ( "Invalid parent link: " + parent.description() )
		#@-body
		#@-node:1::<< validate parent ivar >>

		
		#@<< validate childIndex ivar >>
		#@+node:2::<< validate childIndex ivar >>
		#@+body
		if p:
			if childIndex < 0:
				self.invalidOutline ( "missing childIndex" + childIndex )
			elif childIndex >= p.numberOfChildren():
				self.invalidOutline ( "missing children entry for index: " + childIndex )
		elif childIndex < 0:
			self.invalidOutline ( "negative childIndex" + childIndex )
		#@-body
		#@-node:2::<< validate childIndex ivar >>

		
		#@<< validate x ivar >>
		#@+node:3::<< validate x ivar >>
		#@+body
		if not self.t and p:
			self.invalidOutline ( "Empty t" )
		#@-body
		#@-node:3::<< validate x ivar >>

	
		# Recursively validate all the children.
		child = self.firstChild()
		while child:
			r = child.validateOutlineWithParent ( self )
			if not r: result = false
			child = child.next()
		return result
	#@-body
	#@-node:4::validateOutlineWithParent
	#@-node:2::Public helper functions
	#@+node:3::Private helper functions
	#@+node:1::cloneTree
	#@+body
	# This method creates a cloned tree after oldTree.
	
	def cloneTree (self, oldTree):
		# Create a new tree following oldTree.
		newTree = self.insertAfter(oldTree.t)
		newTree.initHeadString (oldTree.mHeadString)
		self.copyTree(oldTree, newTree)
		# Join the trees and copy clone bits.
		oldTree.joinTreeTo(newTree)
		oldTree.copyCloneBitsTo(newTree)
		return newTree
	#@-body
	#@-node:1::cloneTree
	#@+node:2::copyCloneBitsTo
	#@+body
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
	#@-body
	#@-node:2::copyCloneBitsTo
	#@+node:3::v.copyNode
	#@+body
	def copyNode (self, old_node, new_node):
	
		new_node.mHeadString = old_node.mHeadString
		new_node.iconVal = old_node.iconVal
	#@-body
	#@-node:3::v.copyNode
	#@+node:4::createDependents (bug fix: 4/22/01)
	#@+body
	# This method creates all nodes that depend on the receiver.
	def createDependents (self):
	
		v = self ; t = v.t ; parent = v.parent()
		if not parent: return
		# Copy v as the nth child of all nodes joined to parent.
		n = v.childIndex()
		# trace(`n` + ", " + `v`)
		p = parent.joinList
		while p and p != parent:
			copy = p.insertAsNthChild(n, t)
			copy.mHeadString = v.mHeadString
			copy.iconWithVal = v.iconVal
			self.copyTree(v, copy)
			v.joinTreeTo(copy)
			p = p.joinList
	#@-body
	#@-node:4::createDependents (bug fix: 4/22/01)
	#@+node:5::destroyDependents
	#@+body
	# Destroys all dependent vnodes and tree nodes associated with the receiver.
	
	def destroyDependents (self):
	
		parent = self.parent()
		if not parent: return
		# Destroy the nth child of all nodes joined to the receiver's parent.
		n = self.childIndex()
		join = parent.joinList
		# trace(`n` + ", " + `self`)
		while join and join != parent:
			child = join.nthChild(n)
			if child:
				child.unjoinTree()
				child.unlink()
				child.destroyTree()
			join = join.joinList
	#@-body
	#@-node:5::destroyDependents
	#@+node:6::destroyTree (does nothing!)
	#@+body
	#@+at
	#  This method destroys (irrevocably deletes) a vnode tree.
	# 
	# This code should be called only when it is no longer possible to undo a 
	# previous delete.  It is always valid to destroy dependent trees.

	#@-at
	#@@c

	def destroyTree (self):
	
		pass
	#@-body
	#@-node:6::destroyTree (does nothing!)
	#@+node:7::invalidOutline
	#@+body
	def invalidOutline (self, message):
	
		s = "invalid outline: " + message + "\n"
		parent = self.parent()
	
		if parent:
			s += `parent`
		else:
			s += `self`
	
		alert ( s )
	#@-body
	#@-node:7::invalidOutline
	#@+node:8::isJoinedTo
	#@+body
	def isJoinedTo (self, v):
	
		return v and self.t == v.t
	#@-body
	#@-node:8::isJoinedTo
	#@+node:9::isOnJoinListOf
	#@+body
	# Returns true if the nodes v1 and v2 are on the same join list.
	def isOnJoinListOf (self, v2):
	
		v1 = self
		assert(v2 and v1.t and v2.t)
		
		# v1 and v2 must share the same tnode.
		if v1.t != v2.t: return false
		
		# v1 and v2 must have join lists.
		if not v1.joinList or not v2.joinList: return false
		
		# Return true if v2 is on v1's join list.
		v = v1.joinList
		while v and v != v1:
			if v == v2: return true
			v = v.joinList
	
		return false
	#@-body
	#@-node:9::isOnJoinListOf
	#@+node:10::joinNodeTo
	#@+body
	#@+at
	#  This method joins the receiver to v2 if the two nodes have not already 
	# been joined. Joining involves placing each vnode on the others join list.

	#@-at
	#@@c

	def joinNodeTo (self, v2):
	
		v1 = self
		if v1.isOnJoinListOf(v2): return # 12/17/01: fix same bug as in LeoCB
	
		j1 = v1.joinList
		j2 = v2.joinList
		if j1 and j2:
			# Swapping pointers joins the two cycles.
			v1.joinList = j2  # Neither join list is None.
			v2.joinList = j1
		elif j1:
			v2.joinList = j1  # Link v2 after v1.
			v1.joinList = v2
		elif j2:
			v1.joinList = j2  # Link v1 after v2.
			v2.joinList = v1
		else:
			v1.joinList = v2  # point v1 and v2 at each other.
			v2.joinList = v1
		assert(v1.joinList and v2.joinList)
	#@-body
	#@-node:10::joinNodeTo
	#@+node:11::linkAfter
	#@+body
	# Links the receiver after v.
	
	def linkAfter (self, v):
	
		# trace(`v`)
		self.mParent = v.mParent
		self.mBack = v
		self.mNext = v.mNext
		v.mNext = self
		if self.mNext:
			self.mNext.mBack = self
	#@-body
	#@-node:11::linkAfter
	#@+node:12::linkAsNthChild
	#@+body
	def linkAsNthChild (self, p, n):
	
		"""Links the receiver as the n'th child of p"""
	
		v = self
		# trace(`v` + ", " + `p` + ", " + `n`)
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
	#@-body
	#@-node:12::linkAsNthChild
	#@+node:13::linkAsRoot
	#@+body
	#@+at
	#  Bug fix: 5/27/02.  We link in the rest of the tree only when oldRoot != 
	# None.  Otherwise, we are calling this routine from init code and we want 
	# to start with a pristine tree.

	#@-at
	#@@c
	def linkAsRoot(self, oldRoot = None):
	
		v = self ; c = v.commands ; tree = c.tree
		# trace(`v`)
		# Bug fix 3/16/02:
		# Clear all links except the child link.
		# This allows a node with children to be moved up properly to the root position.
		# v.mFirstChild = None
		v.mParent = None
		v.mBack = None
		# 5/27/02
		if oldRoot: oldRoot.mBack = v
		v.mNext = oldRoot
		tree.rootVnode = v
	
	#@-body
	#@-node:13::linkAsRoot
	#@+node:14::unlink
	#@+body
	def unlink (self):
	
		"""Unlinks the receiver from the tree before moving or deleting."""
		v = self ; c = v.commands ; tree = c.tree
		
		# trace(`v.mParent`+", child:"+`v.mFirstChild`+", back:"+`v.mBack`+", next:"+`v.mNext`)
		
		# Special case the root
		if v == tree.rootVnode:
			if not v.mNext: return # Should never happen.
			tree.rootVnode = v.mNext
	
		# Clear the links in other nodes
		if v.mBack:
			v.mBack.mNext = v.mNext
		if v.mNext:
			v.mNext.mBack = v.mBack
		if v.mParent and v == v.mParent.mFirstChild:
			v.mParent.mFirstChild = v.mNext
	
		# Clear the links in this node
		v.mParent = v.mNext = v.mBack = None
	#@-body
	#@-node:14::unlink
	#@+node:15::unjoinNode
	#@+body
	#@+at
	#  This code carefully unlinks the receiver from its join list.  We can 
	# not assume that all such links will eventually be cleared.

	#@-at
	#@@c

	def unjoinNode (self):
	
		next = self.joinList
		if not next: return
	
		if next.joinList == self:
			# The list contains only two elements.
			next.joinList = None
			self.joinList = None
		else:
			prev = None
			
			#@<< Set prev to the node that points to self >>
			#@+node:1::<< Set prev to the node that points to self >>
			#@+body
			#@+at
			#  We guard against any cycles in the join list, which would cause 
			# self loop to hang.  It's much better to cause an assert to fail.

			#@-at
			#@@c

			self.commands.clearAllVisited()
			
			prev = next
			while prev and prev.joinList != self:
				assert(not prev.isVisited())
				prev.setVisited()
				prev = prev.joinList
			#@-body
			#@-node:1::<< Set prev to the node that points to self >>

			# Remove self from the join list.
			prev.joinList = next
			self.joinList = None
	#@-body
	#@-node:15::unjoinNode
	#@+node:16::unjoinTree
	#@+body
	# This function unjoins all nodes of the receiver's tree.
	
	def unjoinTree (self):
	
		v = self
		after = self.nodeAfterTree()
		while v and v != after:
			v.unjoinNode()
			v = v.threadNext()
	#@-body
	#@-node:16::unjoinTree
	#@-node:3::Private helper functions
	#@-node:12::Moving, Inserting, Deleting, Cloning
	#@-others
#@-body
#@-node:4::class vnode
#@-others
#@-body
#@-node:0::@file leoNodes.py
#@-leo
