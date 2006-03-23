#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3320:@thin leoNodes.py
#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< About the vnode and tnode classes >>
#@+node:ekr.20031218072017.2412:<< About the vnode and tnode classes >>
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
#@-node:ekr.20031218072017.2412:<< About the vnode and tnode classes >>
#@nl
#@<< About clones >>
#@+node:ekr.20031218072017.2408:<< About clones >>
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
#     + a' (1)
#     + a' (2)
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
#     + a'
#         + b
#     + a'
#         + b
# 
# The b nodes are structurally similar because the a' nodes are joined and 
# each b node is the first child of its parent.
# 
# Example 3
# 
# If we now clone either b, we will get:
# 
# + root
#     + a'
#         + b' (1)
#         + b' (2)
#     + a'
#         + b' (1)
#         + b' (2)
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
#@-node:ekr.20031218072017.2408:<< About clones >>
#@nl

from __future__ import generators # To make the code work in Python 2.2.

import leoGlobals as g

if g.app and g.app.use_psyco:
    # print "enabled psyco classes",__file__
    try: from psyco.classes import *
    except ImportError: pass

import string
import time

#@+others
#@+node:ekr.20031218072017.3321:class tnode
class baseTnode (object):
    """The base class of the tnode class."""
    #@    << tnode constants >>
    #@+node:ekr.20031218072017.3322:<< tnode constants >>
    dirtyBit    = 0x01
    richTextBit = 0x02 # Determines whether we use <bt> or <btr> tags.
    visitedBit  = 0x04
    writeBit    = 0x08 # Set: write the tnode.
    #@nonl
    #@-node:ekr.20031218072017.3322:<< tnode constants >>
    #@nl
    #@    @+others
    #@+node:ekr.20031218072017.2006:t.__init__
    # All params have defaults, so t = tnode() is valid.
    
    def __init__ (self,bodyString=None,headString=None):
    
        self.cloneIndex = 0 # For Pre-3.12 files.  Zero for @file nodes
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
    #@-node:ekr.20031218072017.2006:t.__init__
    #@+node:ekr.20031218072017.3323:t.__repr__ & t.__str__
    def __repr__ (self):
        
        return "<tnode %d>" % (id(self))
            
    __str__ = __repr__
    #@nonl
    #@-node:ekr.20031218072017.3323:t.__repr__ & t.__str__
    #@+node:ekr.20031218072017.3325:Getters
    #@+node:EKR.20040625161602:getBody
    def getBody (self):
    
        return self.bodyString
    #@nonl
    #@-node:EKR.20040625161602:getBody
    #@+node:ekr.20031218072017.3326:t.hasBody
    def hasBody (self):
        
        '''Return True if this tnode contains body text.'''
    
        s = self.bodyString
    
        return s and len(s) > 0
    #@nonl
    #@-node:ekr.20031218072017.3326:t.hasBody
    #@+node:ekr.20031218072017.3327:Status bits
    #@+node:ekr.20031218072017.3328:isDirty
    def isDirty (self):
    
        return (self.statusBits & self.dirtyBit) != 0
    #@nonl
    #@-node:ekr.20031218072017.3328:isDirty
    #@+node:ekr.20031218072017.3329:isRichTextBit
    def isRichTextBit (self):
    
        return (self.statusBits & self.richTextBit) != 0
    #@nonl
    #@-node:ekr.20031218072017.3329:isRichTextBit
    #@+node:ekr.20031218072017.3330:isVisited
    def isVisited (self):
    
        return (self.statusBits & self.visitedBit) != 0
    #@nonl
    #@-node:ekr.20031218072017.3330:isVisited
    #@+node:EKR.20040503094727:isWriteBit
    def isWriteBit (self):
    
        return (self.statusBits & self.writeBit) != 0
    #@nonl
    #@-node:EKR.20040503094727:isWriteBit
    #@-node:ekr.20031218072017.3327:Status bits
    #@-node:ekr.20031218072017.3325:Getters
    #@+node:ekr.20031218072017.3331:Setters
    #@+node:ekr.20031218072017.1484:Setting body text
    #@+node:ekr.20031218072017.1485:setTnodeText
    # This sets the text in the tnode from the given string.
    
    def setTnodeText (self,s,encoding="utf-8"):
        
        """Set the body text of a tnode to the given string."""
        
        s = g.toUnicode(s,encoding,reportErrors=True)
        
        if 0: # DANGEROUS:  This automatically converts everything when reading files.
        
            ## Self c does not exist yet.
            option = c.config.trailing_body_newlines
            
            if option == "one":
                s = s.rstrip() + '\n'
            elif option == "zero":
                s = s.rstrip()
        
        self.bodyString = s
        
        # g.trace(g.callers(5))
    #@nonl
    #@-node:ekr.20031218072017.1485:setTnodeText
    #@+node:ekr.20031218072017.1486:setSelection
    def setSelection (self,start,length):
    
        self.selectionStart = start
        self.selectionLength = length
    #@nonl
    #@-node:ekr.20031218072017.1486:setSelection
    #@-node:ekr.20031218072017.1484:Setting body text
    #@+node:ekr.20031218072017.3332:Status bits
    #@+node:ekr.20031218072017.3333:clearDirty
    def clearDirty (self):
    
        self.statusBits &= ~ self.dirtyBit
    #@nonl
    #@-node:ekr.20031218072017.3333:clearDirty
    #@+node:ekr.20031218072017.3334:clearRichTextBit
    def clearRichTextBit (self):
    
        self.statusBits &= ~ self.richTextBit
    #@nonl
    #@-node:ekr.20031218072017.3334:clearRichTextBit
    #@+node:ekr.20031218072017.3335:clearVisited
    def clearVisited (self):
    
        self.statusBits &= ~ self.visitedBit
    #@nonl
    #@-node:ekr.20031218072017.3335:clearVisited
    #@+node:EKR.20040503093844:clearWriteBit
    def clearWriteBit (self):
    
        self.statusBits &= ~ self.writeBit
    #@nonl
    #@-node:EKR.20040503093844:clearWriteBit
    #@+node:ekr.20031218072017.3336:setDirty
    def setDirty (self):
    
        self.statusBits |= self.dirtyBit
    #@nonl
    #@-node:ekr.20031218072017.3336:setDirty
    #@+node:ekr.20031218072017.3337:setRichTextBit
    def setRichTextBit (self):
    
        self.statusBits |= self.richTextBit
    #@nonl
    #@-node:ekr.20031218072017.3337:setRichTextBit
    #@+node:ekr.20031218072017.3338:setVisited
    def setVisited (self):
    
        self.statusBits |= self.visitedBit
    #@nonl
    #@-node:ekr.20031218072017.3338:setVisited
    #@+node:EKR.20040503094727.1:setWriteBit
    def setWriteBit (self):
    
        self.statusBits |= self.writeBit
    #@nonl
    #@-node:EKR.20040503094727.1:setWriteBit
    #@-node:ekr.20031218072017.3332:Status bits
    #@+node:ekr.20031218072017.3339:setCloneIndex (used in 3.x)
    def setCloneIndex (self, index):
    
        self.cloneIndex = index
    #@nonl
    #@-node:ekr.20031218072017.3339:setCloneIndex (used in 3.x)
    #@+node:ekr.20031218072017.3340:setFileIndex
    def setFileIndex (self, index):
    
        self.fileIndex = index
    #@nonl
    #@-node:ekr.20031218072017.3340:setFileIndex
    #@+node:ekr.20050418101546:setHeadString (new in 4.3)
    def setHeadString (self,s,encoding="utf-8"):
        
        t = self
    
        s = g.toUnicode(s,encoding,reportErrors=True)
        t.headString = s
    #@nonl
    #@-node:ekr.20050418101546:setHeadString (new in 4.3)
    #@-node:ekr.20031218072017.3331:Setters
    #@-others
    
class tnode (baseTnode):
    """A class that implements tnodes."""
    pass
#@nonl
#@-node:ekr.20031218072017.3321:class tnode
#@+node:ekr.20031218072017.3341:class vnode
class baseVnode (object):
    """The base class of the vnode class."""
    #@    << vnode constants >>
    #@+node:ekr.20031218072017.951:<< vnode constants >>
    # Define the meaning of status bits in new vnodes.
    
    # Archived...
    clonedBit   = 0x01 # True: vnode has clone mark.
    
    # not used = 0x02
    expandedBit = 0x04 # True: vnode is expanded.
    markedBit   = 0x08 # True: vnode is marked
    orphanBit   = 0x10 # True: vnode saved in .leo file, not derived file.
    selectedBit = 0x20 # True: vnode is current vnode.
    topBit      = 0x40 # True: vnode was top vnode when saved.
    
    # Not archived...
    dirtyBit    = 0x060
    richTextBit = 0x080 # Determines whether we use <bt> or <btr> tags.
    visitedBit  = 0x100
    #@-node:ekr.20031218072017.951:<< vnode constants >>
    #@nl
    #@    @+others
    #@+node:ekr.20031218072017.3342:Birth & death
    #@+node:ekr.20031218072017.3343:v.__cmp__ (not used)
    if 0: # not used
        def __cmp__(self,other):
            
            g.trace(self,other)
            return not (self is other) # Must return 0, 1 or -1
    #@nonl
    #@-node:ekr.20031218072017.3343:v.__cmp__ (not used)
    #@+node:ekr.20031218072017.3344:v.__init__
    def __init__ (self,c,t):
    
        assert(t)
        #@    << initialize vnode data members >>
        #@+node:ekr.20031218072017.1968:<< initialize vnode data members >>
        self.c = c # The commander for this vnode.
        self.t = t # The tnode.
        self.statusBits = 0 # status bits
        
        # Structure links.
        self._parent = self._next = self._back = None
        #@nonl
        #@-node:ekr.20031218072017.1968:<< initialize vnode data members >>
        #@nl
    #@nonl
    #@-node:ekr.20031218072017.3344:v.__init__
    #@+node:ekr.20031218072017.3345:v.__repr__ & v.__str__
    def __repr__ (self):
        
        if self.t:
            return "<vnode %d:'%s'>" % (id(self),self.cleanHeadString())
        else:
            return "<vnode %d:NULL tnode>" % (id(self))
            
    __str__ = __repr__
    #@nonl
    #@-node:ekr.20031218072017.3345:v.__repr__ & v.__str__
    #@+node:ekr.20040312145256:v.dump
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
        
        if 1:
            print "t",v.dumpLink(v.t)
            print "vnodeList"
            for v in v.t.vnodeList:
                print v
    #@nonl
    #@-node:ekr.20040312145256:v.dump
    #@-node:ekr.20031218072017.3342:Birth & death
    #@+node:ekr.20031218072017.3346:v.Comparisons
    #@+node:ekr.20040705201018:findAtFileName (new in 4.2 b3)
    def findAtFileName (self,names):
        
        """Return the name following one of the names in nameList.
        Return an empty string."""
    
        h = self.headString()
        
        if not g.match(h,0,'@'):
            return ""
        
        i = g.skip_id(h,1,'-')
        word = h[:i]
        if word in names and g.match_word(h,0,word):
            name = h[i:].strip()
            # g.trace(word,name)
            return name
        else:
            return ""
    #@nonl
    #@-node:ekr.20040705201018:findAtFileName (new in 4.2 b3)
    #@+node:ekr.20031218072017.3350:anyAtFileNodeName
    def anyAtFileNodeName (self):
        
        """Return the file name following an @file node or an empty string."""
    
        names = (
            "@file",
            "@thin",   "@file-thin",   "@thinfile",
            "@asis",   "@file-asis",   "@silentfile",
            "@noref",  "@file-noref",  "@rawfile",
            "@nosent", "@file-nosent", "@nosentinelsfile")
    
        return self.findAtFileName(names)
    #@nonl
    #@-node:ekr.20031218072017.3350:anyAtFileNodeName
    #@+node:ekr.20031218072017.3348:at...FileNodeName
    # These return the filename following @xxx, in v.headString.
    # Return the the empty string if v is not an @xxx node.
    
    def atFileNodeName (self):
        names = ("@file"),
        return self.findAtFileName(names)
    
    def atNoSentinelsFileNodeName (self):
        names = ("@nosent", "@file-nosent", "@nosentinelsfile")
        return self.findAtFileName(names)
    
    def atRawFileNodeName (self):
        names = ("@noref", "@file-noref", "@rawfile")
        return self.findAtFileName(names)
        
    def atSilentFileNodeName (self):
        names = ("@asis", "@file-asis", "@silentfile")
        return self.findAtFileName(names)
        
    def atThinFileNodeName (self):
        names = ("@thin", "@file-thin", "@thinfile")
        return self.findAtFileName(names)
        
    # New names, less confusing
    atNoSentFileNodeName  = atNoSentinelsFileNodeName
    atNorefFileNodeName   = atRawFileNodeName
    atAsisFileNodeName     = atSilentFileNodeName
    #@nonl
    #@-node:ekr.20031218072017.3348:at...FileNodeName
    #@+node:EKR.20040430152000:isAtAllNode
    def isAtAllNode (self):
    
        """Returns True if the receiver contains @others in its body at the start of a line."""
    
        flag, i = g.is_special(self.t.bodyString,0,"@all")
        return flag
    #@nonl
    #@-node:EKR.20040430152000:isAtAllNode
    #@+node:ekr.20040326031436:isAnyAtFileNode good
    def isAnyAtFileNode (self):
        
        """Return True if v is any kind of @file or related node."""
        
        # This routine should be as fast as possible.
        # It is called once for every vnode when writing a file.
    
        h = self.headString()
        return h and h[0] == '@' and self.anyAtFileNodeName()
    #@nonl
    #@-node:ekr.20040326031436:isAnyAtFileNode good
    #@+node:ekr.20040325073709:isAt...FileNode
    def isAtFileNode (self):
        return g.choose(self.atFileNodeName(),True,False)
        
    def isAtNoSentinelsFileNode (self):
        return g.choose(self.atNoSentinelsFileNodeName(),True,False)
    
    def isAtRawFileNode (self): # @file-noref
        return g.choose(self.atRawFileNodeName(),True,False)
    
    def isAtSilentFileNode (self): # @file-asis
        return g.choose(self.atSilentFileNodeName(),True,False)
    
    def isAtThinFileNode (self):
        return g.choose(self.atThinFileNodeName(),True,False)
        
    # New names, less confusing:
    isAtNoSentFileNode = isAtNoSentinelsFileNode
    isAtNorefFileNode  = isAtRawFileNode
    isAtAsisFileNode   = isAtSilentFileNode
    #@nonl
    #@-node:ekr.20040325073709:isAt...FileNode
    #@+node:ekr.20031218072017.3351:isAtIgnoreNode
    def isAtIgnoreNode (self):
    
        """Returns True if the receiver contains @ignore in its body at the start of a line."""
    
        flag, i = g.is_special(self.t.bodyString, 0, "@ignore")
        return flag
    #@nonl
    #@-node:ekr.20031218072017.3351:isAtIgnoreNode
    #@+node:ekr.20031218072017.3352:isAtOthersNode
    def isAtOthersNode (self):
    
        """Returns True if the receiver contains @others in its body at the start of a line."""
    
        flag, i = g.is_special(self.t.bodyString,0,"@others")
        return flag
    #@nonl
    #@-node:ekr.20031218072017.3352:isAtOthersNode
    #@+node:ekr.20031218072017.3353:matchHeadline
    def matchHeadline (self,pattern):
    
        """Returns True if the headline matches the pattern ignoring whitespace and case.
        
        The headline may contain characters following the successfully matched pattern."""
        
        v = self
        
        h = g.toUnicode(v.headString(),'utf-8')
        h = h.lower().replace(' ','').replace('\t','')
    
        pattern = g.toUnicode(pattern,'utf-8')
        pattern = pattern.lower().replace(' ','').replace('\t','')
        
        return h.startswith(pattern)
    #@nonl
    #@-node:ekr.20031218072017.3353:matchHeadline
    #@-node:ekr.20031218072017.3346:v.Comparisons
    #@+node:ekr.20031218072017.3359:Getters (vnode)
    #@+node:ekr.20040306214240:Tree Traversal getters
    #@+node:ekr.20031218072017.3406:v.back
    # Compatibility routine for scripts
    
    def back (self):
    
        return self._back
    #@nonl
    #@-node:ekr.20031218072017.3406:v.back
    #@+node:ekr.20031218072017.3409:v.next
    # Compatibility routine for scripts
    # Used by p.findAllPotentiallyDirtyNodes.
    
    def next (self):
    
        return self._next
    #@nonl
    #@-node:ekr.20031218072017.3409:v.next
    #@-node:ekr.20040306214240:Tree Traversal getters
    #@+node:ekr.20031218072017.3360:Children
    #@+node:ekr.20040303212445:v.childIndex
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
    #@-node:ekr.20040303212445:v.childIndex
    #@+node:ekr.20031218072017.3362:v.firstChild (changed for 4.2)
    def firstChild (self):
        
        return self.t._firstChild
    #@nonl
    #@-node:ekr.20031218072017.3362:v.firstChild (changed for 4.2)
    #@+node:ekr.20040307085922:v.hasChildren & hasFirstChild
    def hasChildren (self):
        
        v = self
        return v.firstChild()
    
    hasFirstChild = hasChildren
    #@nonl
    #@-node:ekr.20040307085922:v.hasChildren & hasFirstChild
    #@+node:ekr.20031218072017.3364:v.lastChild
    def lastChild (self):
    
        child = self.firstChild()
        while child and child.next():
            child = child.next()
        return child
    #@nonl
    #@-node:ekr.20031218072017.3364:v.lastChild
    #@+node:ekr.20031218072017.3365:v.nthChild
    # childIndex and nthChild are zero-based.
    
    def nthChild (self, n):
    
        child = self.firstChild()
        if not child: return None
        while n > 0 and child:
            n -= 1
            child = child.next()
        return child
    #@nonl
    #@-node:ekr.20031218072017.3365:v.nthChild
    #@+node:ekr.20031218072017.3366:v.numberOfChildren (n)
    def numberOfChildren (self):
    
        n = 0
        child = self.firstChild()
        while child:
            n += 1
            child = child.next()
        return n
    #@nonl
    #@-node:ekr.20031218072017.3366:v.numberOfChildren (n)
    #@-node:ekr.20031218072017.3360:Children
    #@+node:ekr.20031218072017.3367:Status Bits
    #@+node:ekr.20031218072017.3368:v.isCloned (4.2)
    def isCloned (self):
        
        return len(self.t.vnodeList) > 1
    #@nonl
    #@-node:ekr.20031218072017.3368:v.isCloned (4.2)
    #@+node:ekr.20031218072017.3369:isDirty
    def isDirty (self):
    
        return self.t.isDirty()
    #@nonl
    #@-node:ekr.20031218072017.3369:isDirty
    #@+node:ekr.20031218072017.3370:isExpanded
    def isExpanded (self):
    
        return ( self.statusBits & self.expandedBit ) != 0
    #@nonl
    #@-node:ekr.20031218072017.3370:isExpanded
    #@+node:ekr.20031218072017.3371:isMarked
    def isMarked (self):
    
        return ( self.statusBits & vnode.markedBit ) != 0
    #@nonl
    #@-node:ekr.20031218072017.3371:isMarked
    #@+node:ekr.20031218072017.3372:isOrphan
    def isOrphan (self):
    
        return ( self.statusBits & vnode.orphanBit ) != 0
    #@nonl
    #@-node:ekr.20031218072017.3372:isOrphan
    #@+node:ekr.20031218072017.3373:isSelected
    def isSelected (self):
    
        return ( self.statusBits & vnode.selectedBit ) != 0
    #@nonl
    #@-node:ekr.20031218072017.3373:isSelected
    #@+node:ekr.20031218072017.3374:isTopBitSet
    def isTopBitSet (self):
    
        return ( self.statusBits & self.topBit ) != 0
    #@nonl
    #@-node:ekr.20031218072017.3374:isTopBitSet
    #@+node:ekr.20031218072017.3376:isVisited
    def isVisited (self):
    
        return ( self.statusBits & vnode.visitedBit ) != 0
    #@nonl
    #@-node:ekr.20031218072017.3376:isVisited
    #@+node:ekr.20031218072017.3377:status
    def status (self):
    
        return self.statusBits
    #@nonl
    #@-node:ekr.20031218072017.3377:status
    #@-node:ekr.20031218072017.3367:Status Bits
    #@+node:ekr.20031218072017.3378:v.bodyString
    # Compatibility routine for scripts
    
    def bodyString (self):
    
        # This message should never be printed and we want to avoid crashing here!
        if not g.isUnicode(self.t.bodyString):
            s = "Leo internal error: not unicode:" + repr(self.t.bodyString)
            g.es_print(s,color="red")
    
        # Make _sure_ we return a unicode string.
        return g.toUnicode(self.t.bodyString,g.app.tkEncoding)
    #@-node:ekr.20031218072017.3378:v.bodyString
    #@+node:ekr.20031218072017.3379:v.currentVnode (and c.currentPosition 4.2)
    def currentPosition (self):
        return self.c.currentPosition()
            
    def currentVnode (self):
        return self.c.currentVnode()
    #@nonl
    #@-node:ekr.20031218072017.3379:v.currentVnode (and c.currentPosition 4.2)
    #@+node:ekr.20031218072017.3381:v.findRoot (4.2)
    def findRoot (self):
        
        return self.c.rootPosition()
    #@nonl
    #@-node:ekr.20031218072017.3381:v.findRoot (4.2)
    #@+node:ekr.20031218072017.1581:v.headString & v.cleanHeadString
    def headString (self):
        
        """Return the headline string."""
        
        # This message should never be printed and we want to avoid crashing here!
        if not g.isUnicode(self.t.headString):
            s = "Leo internal error: not unicode:" + repr(self.t.headString)
            g.es_print(s,color="red")
            
        # Make _sure_ we return a unicode string.
        return g.toUnicode(self.t.headString,g.app.tkEncoding)
    
    def cleanHeadString (self):
        
        s = self.headString()
        return g.toEncodedString(s,"ascii") # Replaces non-ascii characters by '?'
    #@nonl
    #@-node:ekr.20031218072017.1581:v.headString & v.cleanHeadString
    #@+node:ekr.20040323100443:v.directParents (new method in 4.2)
    def directParents (self):
        
        """(New in 4.2) Return a list of all direct parent vnodes of a vnode.
        
        This is NOT the same as the list of ancestors of the vnode."""
        
        v = self
        
        if v._parent:
            return v._parent.t.vnodeList
        else:
            return []
    #@nonl
    #@-node:ekr.20040323100443:v.directParents (new method in 4.2)
    #@-node:ekr.20031218072017.3359:Getters (vnode)
    #@+node:ekr.20040301071824:v.Link/Unlink/Insert methods (used by file read logic)
    # These remain in 4.2: the file read logic calls these before creating positions.
    #@nonl
    #@+node:ekr.20031218072017.3419:v.insertAfter
    def insertAfter (self,t=None):
    
        """Inserts a new vnode after self"""
    
        if not t:
            t = tnode(headString="NewHeadline")
    
        v = vnode(self.c,t)
        v.linkAfter(self)
    
        return v
    #@nonl
    #@-node:ekr.20031218072017.3419:v.insertAfter
    #@+node:ekr.20031218072017.3421:v.insertAsNthChild
    def insertAsNthChild (self,n,t=None):
    
        """Inserts a new node as the the nth child of the receiver.
        The receiver must have at least n-1 children"""
    
        if not t:
            t = tnode(headString="NewHeadline")
    
        v = vnode(self.c,t)
        v.linkAsNthChild(self,n)
    
        return v
    #@nonl
    #@-node:ekr.20031218072017.3421:v.insertAsNthChild
    #@+node:ekr.20031218072017.2355:v.linkAfter
    def linkAfter (self,v):
    
        """Link self after v."""
        
        self._parent = v._parent
        self._back = v
        self._next = v._next
        v._next = self
        if self._next:
            self._next._back = self
    #@-node:ekr.20031218072017.2355:v.linkAfter
    #@+node:ekr.20031218072017.3425:v.linkAsNthChild
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
    #@-node:ekr.20031218072017.3425:v.linkAsNthChild
    #@+node:ekr.20031218072017.3426:v.linkAsRoot
    def linkAsRoot (self,oldRoot):
        
        """Link a vnode as the root node and set the root _position_."""
    
        v = self ; c = v.c
    
        # Clear all links except the child link.
        v._parent = None
        v._back = None
        v._next = oldRoot
        
        # Add v to it's tnode's vnodeList. Bug fix: 5/02/04.
        if v not in v.t.vnodeList:
            v.t.vnodeList.append(v)
    
        # Link in the rest of the tree only when oldRoot != None.
        # Otherwise, we are calling this routine from init code and
        # we want to start with a pristine tree.
        if oldRoot: oldRoot._back = v
    
        newRoot = position(c,v,[])
        c.setRootPosition(newRoot)
    #@nonl
    #@-node:ekr.20031218072017.3426:v.linkAsRoot
    #@+node:ekr.20031218072017.3422:v.moveToRoot
    def moveToRoot (self,oldRoot=None):
    
        '''Moves a vnode to the root position.
        
        Important: oldRoot must the previous root vnode if it exists.'''
    
        v = self
    
        v.unlink()
        v.linkAsRoot(oldRoot)
        
        return v
    #@nonl
    #@-node:ekr.20031218072017.3422:v.moveToRoot
    #@+node:ekr.20031218072017.3438:v.unlink
    def unlink (self):
    
        """Unlinks a vnode from the tree."""
    
        v = self ; c = v.c
    
        # g.trace(v._parent," child: ",v.t._firstChild," back: ", v._back, " next: ", v._next)
        
        # Special case the root.
        if v == c.rootPosition().v: # 3/11/04
            assert(v._next)
            newRoot = position(c,v._next,[])
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
    #@-node:ekr.20031218072017.3438:v.unlink
    #@-node:ekr.20040301071824:v.Link/Unlink/Insert methods (used by file read logic)
    #@+node:ekr.20031218072017.3384:Setters
    #@+node:ekr.20031218072017.3386: v.Status bits
    #@+node:ekr.20031218072017.3389:clearClonedBit
    def clearClonedBit (self):
    
        self.statusBits &= ~ self.clonedBit
    #@nonl
    #@-node:ekr.20031218072017.3389:clearClonedBit
    #@+node:ekr.20031218072017.3390:clearDirty & clearDirtyJoined (redundant code)
    def clearDirty (self):
    
        v = self
        v.t.clearDirty()
    
    def clearDirtyJoined (self):
    
        g.trace()
        v = self ; c = v.c
        c.beginUpdate()
        try:
            v.t.clearDirty()
        finally:
            c.endUpdate() # recomputes all icons
    #@nonl
    #@-node:ekr.20031218072017.3390:clearDirty & clearDirtyJoined (redundant code)
    #@+node:ekr.20031218072017.3391:v.clearMarked
    def clearMarked (self):
    
        self.statusBits &= ~ self.markedBit
    #@-node:ekr.20031218072017.3391:v.clearMarked
    #@+node:ekr.20031218072017.3392:clearOrphan
    def clearOrphan (self):
    
        self.statusBits &= ~ self.orphanBit
    #@nonl
    #@-node:ekr.20031218072017.3392:clearOrphan
    #@+node:ekr.20031218072017.3393:clearVisited
    def clearVisited (self):
    
        self.statusBits &= ~ self.visitedBit
    #@nonl
    #@-node:ekr.20031218072017.3393:clearVisited
    #@+node:ekr.20031218072017.3395:contract & expand & initExpandedBit
    def contract(self):
    
        self.statusBits &= ~ self.expandedBit
        
        # g.trace(self.statusBits)
    
    def expand(self):
    
        self.statusBits |= self.expandedBit
        
        # g.trace(self.statusBits)
    
    def initExpandedBit (self):
    
        self.statusBits |= self.expandedBit
    #@nonl
    #@-node:ekr.20031218072017.3395:contract & expand & initExpandedBit
    #@+node:ekr.20031218072017.3396:initStatus
    def initStatus (self, status):
    
        self.statusBits = status
    #@nonl
    #@-node:ekr.20031218072017.3396:initStatus
    #@+node:ekr.20031218072017.3397:setClonedBit & initClonedBit
    def setClonedBit (self):
    
        self.statusBits |= self.clonedBit
    
    def initClonedBit (self, val):
    
        if val:
            self.statusBits |= self.clonedBit
        else:
            self.statusBits &= ~ self.clonedBit
    #@nonl
    #@-node:ekr.20031218072017.3397:setClonedBit & initClonedBit
    #@+node:ekr.20031218072017.3398:v.setMarked & initMarkedBit
    def setMarked (self):
    
        self.statusBits |= self.markedBit
    
    def initMarkedBit (self):
    
        self.statusBits |= self.markedBit
    #@-node:ekr.20031218072017.3398:v.setMarked & initMarkedBit
    #@+node:ekr.20031218072017.3399:setOrphan
    def setOrphan (self):
    
        self.statusBits |= self.orphanBit
    #@nonl
    #@-node:ekr.20031218072017.3399:setOrphan
    #@+node:ekr.20031218072017.3400:setSelected (vnode)
    # This only sets the selected bit.
    
    def setSelected (self):
    
        self.statusBits |= self.selectedBit
    #@nonl
    #@-node:ekr.20031218072017.3400:setSelected (vnode)
    #@+node:ekr.20031218072017.3401:t.setVisited
    # Compatibility routine for scripts
    
    def setVisited (self):
    
        self.statusBits |= self.visitedBit
    #@nonl
    #@-node:ekr.20031218072017.3401:t.setVisited
    #@-node:ekr.20031218072017.3386: v.Status bits
    #@+node:ekr.20031218072017.3385:v.computeIcon & setIcon
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
    #@-node:ekr.20031218072017.3385:v.computeIcon & setIcon
    #@+node:ekr.20040315032144:v.initHeadString
    def initHeadString (self,s,encoding="utf-8"):
        
        v = self
        s = g.toUnicode(s,encoding,reportErrors=True)
        v.t.headString = s
        
        # g.trace(g.callers(5))
    #@nonl
    #@-node:ekr.20040315032144:v.initHeadString
    #@+node:ekr.20031218072017.3402:v.setSelection
    def setSelection (self, start, length):
    
        self.t.setSelection ( start, length )
    #@nonl
    #@-node:ekr.20031218072017.3402:v.setSelection
    #@+node:ekr.20040315042106:v.setTnodeText
    def setTnodeText (self,s,encoding="utf-8"):
        
        return self.t.setTnodeText(s,encoding)
    #@nonl
    #@-node:ekr.20040315042106:v.setTnodeText
    #@+node:ekr.20031218072017.3404:v.trimTrailingLines
    def trimTrailingLines (self):
    
        """Trims trailing blank lines from a node.
        
        It is surprising difficult to do this during Untangle."""
    
        v = self
        body = v.bodyString()
        # g.trace(body)
        lines = string.split(body,'\n')
        i = len(lines) - 1 ; changed = False
        while i >= 0:
            line = lines[i]
            j = g.skip_ws(line,0)
            if j + 1 == len(line):
                del lines[i]
                i -= 1 ; changed = True
            else: break
        if changed:
            body = string.join(body,'') + '\n' # Add back one last newline.
            # g.trace(body)
            v.setBodyStringOrPane(body)
            # Don't set the dirty bit: it would just be annoying.
    #@-node:ekr.20031218072017.3404:v.trimTrailingLines
    #@-node:ekr.20031218072017.3384:Setters
    #@+node:EKR.20040528151551:v.Iterators
    #@+node:EKR.20040528151551.2:self_subtree_iter
    def subtree_iter(self):
    
        """Return all nodes of self's tree in outline order."""
        
        v = self
    
        if v:
            yield v
            child = v.t._firstChild
            while child:
                for v1 in child.subtree_iter():
                    yield v1
                child = child.next()
                
    self_and_subtree_iter = subtree_iter
    #@nonl
    #@-node:EKR.20040528151551.2:self_subtree_iter
    #@+node:EKR.20040528151551.3:unique_subtree_iter
    def unique_subtree_iter(self,marks=None):
    
        """Return all vnodes in self's tree, discarding duplicates """
        
        v = self
    
        if marks == None: marks = {}
    
        if v and v not in marks:
            marks[v] = v
            yield v
            if v.t._firstChild:
                for v1 in v.t._firstChild.unique_subtree_iter(marks):
                    yield v1
            v = v._next
            while v:
                for v in v.unique_subtree_iter(marks):
                    yield v
                v = v._next
                
    self_and_unique_subtree_iter = unique_subtree_iter
    #@nonl
    #@-node:EKR.20040528151551.3:unique_subtree_iter
    #@-node:EKR.20040528151551:v.Iterators
    #@-others
    
class vnode (baseVnode):
    """A class that implements vnodes."""
    pass
#@nonl
#@-node:ekr.20031218072017.3341:class vnode
#@+node:ekr.20031218072017.1991:class nodeIndices
# Indices are Python dicts containing 'id','loc','time' and 'n' keys.

class nodeIndices (object):
    
    """A class to implement global node indices (gnx's)."""
    
    #@    @+others
    #@+node:ekr.20031218072017.1992:nodeIndices.__init__
    def __init__ (self,id):
        
        """ctor for nodeIndices class"""
    
        self.userId = id
        self.defaultId = id
        self.lastIndex = None
        self.timeString = None
    #@nonl
    #@-node:ekr.20031218072017.1992:nodeIndices.__init__
    #@+node:ekr.20031218072017.1993:areEqual
    def areEqual (self,gnx1,gnx2):
        
        """Return True if all fields of gnx1 and gnx2 are equal"""
    
        # works whatever the format of gnx1 and gnx2.
        # This should never throw an exception.
        return gnx1 == gnx2
        
        id1,time1,n1 = gnx1
        id2,time2,n2 = gnx2
        # g.trace(id1==id2 and time1==time2 and n1==n2,gnx1,gnx2)
        return id1==id2 and time1==time2 and n1==n2
    #@nonl
    #@-node:ekr.20031218072017.1993:areEqual
    #@+node:ekr.20031218072017.1994:get/setDefaultId
    # These are used by the fileCommands read/write code.
    
    def getDefaultId (self):
        
        """Return the id to be used by default in all gnx's"""
        return self.defaultId
        
    def setDefaultId (self,theId):
        
        """Set the id to be used by default in all gnx's"""
        self.defaultId = theId
    #@-node:ekr.20031218072017.1994:get/setDefaultId
    #@+node:ekr.20031218072017.1995:getNewIndex
    def getNewIndex (self):
        
        """Create a new gnx using self.timeString and self.lastIndex"""
        
        theId = self.userId # Bug fix 5/1/03: always use the user's id for new ids!
        t = self.timeString
        assert(t)
        n = None
    
        # Set n if id and time match the previous index.
        last = self.lastIndex
        if last:
            lastId,lastTime,lastN = last
            if theId==lastId and t==lastTime:
                if lastN == None: n = 1
                else: n = lastN + 1
    
        d = (theId,t,n)
        self.lastIndex = d
        # g.trace(d)
        return d
    #@nonl
    #@-node:ekr.20031218072017.1995:getNewIndex
    #@+node:ekr.20031218072017.1996:isGnx
    def isGnx (self,gnx):
        try:
            theId,t,n = gnx
            return t != None
        except:
            return False
    #@nonl
    #@-node:ekr.20031218072017.1996:isGnx
    #@+node:ekr.20031218072017.1997:scanGnx
    def scanGnx (self,s,i):
        
        """Create a gnx from its string representation"""
        
        if type(s) not in (type(""),type(u"")):
            g.es("scanGnx: unexpected index type:",type(s),s,color="red")
            return None,None,None
            
        s = s.strip()
    
        theId,t,n = None,None,None
        i,theId = g.skip_to_char(s,i,'.')
        if g.match(s,i,'.'):
            i,t = g.skip_to_char(s,i+1,'.')
            if g.match(s,i,'.'):
                i,n = g.skip_to_char(s,i+1,'.')
        # Use self.defaultId for missing id entries.
        if theId == None or len(theId) == 0:
            theId = self.defaultId
        # Convert n to int.
        if n:
            try: n = int(n)
            except: pass
    
        return theId,t,n
    #@nonl
    #@-node:ekr.20031218072017.1997:scanGnx
    #@+node:ekr.20031218072017.1998:setTimeStamp
    def setTimestamp (self):
    
        """Set the timestamp string to be used by getNewIndex until further notice"""
    
        self.timeString = time.strftime(
            "%Y%m%d%H%M%S", # Help comparisons; avoid y2k problems.
            time.localtime())
    #@nonl
    #@-node:ekr.20031218072017.1998:setTimeStamp
    #@+node:ekr.20031218072017.1999:toString
    def toString (self,index,removeDefaultId=False):
        
        """Convert a gnx (a tuple) to its string representation"""
    
        theId,t,n = index
    
        if removeDefaultId and theId == self.defaultId:
            theId = ""
    
        if not n: # None or ""
            return "%s.%s" % (theId,t)
        else:
            return "%s.%s.%d" % (theId,t,n)
    #@nonl
    #@-node:ekr.20031218072017.1999:toString
    #@-others
#@-node:ekr.20031218072017.1991:class nodeIndices
#@+node:ekr.20031218072017.889:class position
# Warning: this code implies substantial changes to code that uses them, both core and scripts.

class position (object):
    
    """A class representing a position in a traversal of a tree containing shared tnodes."""

    #@    << about the position class >>
    #@+node:ekr.20031218072017.890:<< about the position class >>
    #@@killcolor
    
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
    #   These include p.level, p.isVisible and p.hasThreadNext.
    # - p.moveToLastNode and p.moveToThreadBack use new algorithms that don't 
    # use temporary data.
    # - Several lookahead routines compute whether a position exists without 
    # computing the actual position.
    #@-at
    #@nonl
    #@-node:ekr.20031218072017.890:<< about the position class >>
    #@nl
    #@    << positions may become invalid when outlines change >>
    #@+node:ekr.20050524082843:<< positions may become invalid when outlines change >>
    #@@killcolor
    
    #@+at 
    #@nonl
    # If a vnode has only one parent, v._parent is that parent. Otherwise,
    # v.t.vnodeList is the list of vnodes v2 such that v2._firstChild == v. 
    # Alas, this
    # means that positions can become invalid when vnodeList's change!
    # 
    # There is no use trying to solve the problem in p.moveToParent or
    # p.vParentWithStack: the invalidated positions simply don't have the 
    # stack
    # entries needed to compute parent fields properly. In short, changing 
    # t.vnodeList
    # may invalidate existing positions!
    #@-at
    #@nonl
    #@-node:ekr.20050524082843:<< positions may become invalid when outlines change >>
    #@nl
    
    #@    @+others
    #@+node:ekr.20040228094013: ctor & other special methods...
    #@+node:ekr.20031218072017.893:p.__cmp__
    def __cmp__(self,p2):
    
        """Return 0 if two postions are equivalent."""
    
        # Use p.equal if speed is crucial.
        p1 = self
        
        # g.trace(p1.headString(),p2 and p2.headString())
    
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
    #@-node:ekr.20031218072017.893:p.__cmp__
    #@+node:ekr.20040117170612:p.__getattr__  ON:  must be ON if use_plugins
    if 1: # Good for compatibility, bad for finding conversion problems.
    
        def __getattr__ (self,attr):
            
            """Convert references to p.t into references to p.v.t.
            
            N.B. This automatically keeps p.t in synch with p.v.t."""
    
            if attr=="t":
                return self.v.t
            else:
                # New in 4.3: _silently_ raise the attribute error.
                # This allows plugin code to use hasattr(p,attr) !
                if 0:
                    print "unknown position attribute:",attr
                    import traceback ; traceback.print_stack()
                raise AttributeError,attr
    #@nonl
    #@-node:ekr.20040117170612:p.__getattr__  ON:  must be ON if use_plugins
    #@+node:ekr.20031218072017.892:p.__init__
    def __init__ (self,c,v,stack,trace=True):
    
        """Create a new position."""
        
        __pychecker__ = '--no-argsused' # trace not used.
    
        self.c = c
        self.v = v
        # assert(v is None or v.t)
        self.stack = stack[:] # Creating a copy here is safest and best.
        g.app.positions += 1
        
        # if g.app.tracePositions and trace: g.trace(g.callers())
        
        # Note: __getattr__ implements p.t.
    #@nonl
    #@-node:ekr.20031218072017.892:p.__init__
    #@+node:ekr.20040117173448:p.__nonzero__
    #@+at
    # Tests such as 'if p' or 'if not p' are the _only_ correct ways to test 
    # whether a position p is valid.
    # In particular, tests like 'if p is None' or 'if p is not None' will not 
    # work properly.
    #@-at
    #@@c
    
    def __nonzero__ ( self):
        
        """Return True if a position is valid."""
        
        # if g.app.trace: "__nonzero__",self.v
    
        return self.v is not None
    #@nonl
    #@-node:ekr.20040117173448:p.__nonzero__
    #@+node:ekr.20040301205720:p.__str__ and p.__repr__
    def __str__ (self):
        
        p = self
        
        if p.v:
            return "<pos %d lvl: %d [%d] %s>" % (id(p),p.level(),len(p.stack),p.cleanHeadString())
        else:
            return "<pos %d        [%d] None>" % (id(p),len(p.stack))
            
    __repr__ = __str__
    #@nonl
    #@-node:ekr.20040301205720:p.__str__ and p.__repr__
    #@+node:ekr.20040117171654:p.copy
    # Using this routine can generate huge numbers of temporary positions during a tree traversal.
    
    def copy (self):
        
        """"Return an independent copy of a position."""
        
        # if g.app.tracePositions: g.trace(g.callers())
    
        return position(self.c,self.v,self.stack,trace=False)
    #@nonl
    #@-node:ekr.20040117171654:p.copy
    #@+node:ekr.20040310153624:p.dump & p.vnodeListIds
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
    #@-node:ekr.20040310153624:p.dump & p.vnodeListIds
    #@+node:ekr.20040325142015:p.equal & isEqual
    def equal(self,p2):
    
        """Return True if two postions are equivalent.
        
        Use this method when the speed comparisons is crucial
        
        N.B. Unlike __cmp__, p2 must not be None.
        """
    
        p1 = self
    
        # Check entire stack quickly.
        # The stack contains vnodes, so this does not call p.__cmp__.
        return (
            p1.v == p2.v and
            p1.stack == p2.stack and
            p1.childIndex() == p2.childIndex())
            
    isEqual = equal
    #@nonl
    #@-node:ekr.20040325142015:p.equal & isEqual
    #@+node:ekr.20060202090907:p.key (new in 4.4b2)
    def key (self):
        
        p = self
    
        return '%s:%d.%s' % (
            id(p.v),
            p.childIndex(),
            ','.join([str(id(v)) for v in p.stack])
        )
    #@nonl
    #@-node:ekr.20060202090907:p.key (new in 4.4b2)
    #@-node:ekr.20040228094013: ctor & other special methods...
    #@+node:ekr.20040306212636:Getters
    #@+node:ekr.20040306210951: vnode proxies
    #@+node:ekr.20040306211032:p.Comparisons
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
    def isAtAllNode             (self): return self.v.isAtAllNode()
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
    ## def afterHeadlineMatch (self,s): return self.v.afterHeadlineMatch(s)
    #@nonl
    #@-node:ekr.20040306211032:p.Comparisons
    #@+node:ekr.20040306212151:p.Extra Attributes
    def extraAttributes (self):
        
        return self.v.extraAttributes()
    
    def setExtraAttributes (self,data):
    
        return self.v.setExtraAttributes(data)
    #@nonl
    #@-node:ekr.20040306212151:p.Extra Attributes
    #@+node:ekr.20040306220230:p.Headline & body strings
    def bodyString (self):
        
        return self.v.bodyString()
    
    def headString (self):
        
        return self.v.headString()
        
    def cleanHeadString (self):
        
        return self.v.cleanHeadString()
    #@-node:ekr.20040306220230:p.Headline & body strings
    #@+node:ekr.20040306214401:p.Status bits
    def isDirty     (self): return self.v.isDirty()
    def isExpanded  (self): return self.v.isExpanded()
    def isMarked    (self): return self.v.isMarked()
    def isOrphan    (self): return self.v.isOrphan()
    def isSelected  (self): return self.v.isSelected()
    def isTopBitSet (self): return self.v.isTopBitSet()
    def isVisited   (self): return self.v.isVisited()
    def status      (self): return self.v.status()
    #@nonl
    #@-node:ekr.20040306214401:p.Status bits
    #@+node:ekr.20040306220230.1:p.edit_widget
    def edit_widget (self):
        
        # New in 4.3 beta 3: let the tree classes do all the work.
        
        p = self ; c = p.c
        
        return p and c.frame.tree.edit_widget(p)
        
    edit_text = edit_widget # For compatibility.
    #@nonl
    #@-node:ekr.20040306220230.1:p.edit_widget
    #@+node:ekr.20040323160302:p.directParents
    def directParents (self):
        
        return self.v.directParents()
    #@-node:ekr.20040323160302:p.directParents
    #@+node:ekr.20040326064330:p.childIndex
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
    #@-node:ekr.20040326064330:p.childIndex
    #@-node:ekr.20040306210951: vnode proxies
    #@+node:ekr.20040306214240.2:children
    #@+node:ekr.20040306214240.3:p.hasChildren
    def hasChildren(self):
        
        p = self
        # g.trace(p,p.v)
        return p.v and p.v.t and p.v.t._firstChild
    #@nonl
    #@-node:ekr.20040306214240.3:p.hasChildren
    #@+node:ekr.20040306212636.1:p.numberOfChildren
    def numberOfChildren (self):
        
        return self.v.numberOfChildren()
    #@-node:ekr.20040306212636.1:p.numberOfChildren
    #@-node:ekr.20040306214240.2:children
    #@+node:ekr.20040307104131.3:p.exists
    def exists(self,c):
        
        """Return True if a position exists in c's tree"""
        
        p = self.copy()
    
        # This code must be fast.
        root = c.rootPosition()
    
        while p:
            # g.trace(p.headString(),'parent',p.parent(),'back',p.back())
            if p.equal(root):
                return True
            if p.hasParent():
                p.moveToParent()
            else:
                p.moveToBack()
            
        # g.trace('does not exist in root:',root.headString())
        return False
    #@nonl
    #@-node:ekr.20040307104131.3:p.exists
    #@+node:ekr.20040306215548:p.findRoot
    def findRoot (self):
        
        return self.c.frame.rootPosition()
    #@nonl
    #@-node:ekr.20040306215548:p.findRoot
    #@+node:ekr.20031218072017.915:p.getX & vnode compatibility traversal routines
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
    #@-node:ekr.20031218072017.915:p.getX & vnode compatibility traversal routines
    #@+node:ekr.20040227212621:p.hasX
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
    #@+node:ekr.20040227224946:hasThreadNext (the only complex hasX method)
    def hasThreadNext(self):
    
        p = self ; v = p.v
        if not p.v: return False
    
        if v.t._firstChild or v._next:
            return True
        else:
            n = len(p.stack)-1
            v,n = p.vParentWithStack(v,p.stack,n)
            while v:
                if v._next:
                    return True
                v,n = p.vParentWithStack(v,p.stack,n)
            return False
    
    hasVisNext = hasThreadNext
    #@nonl
    #@-node:ekr.20040227224946:hasThreadNext (the only complex hasX method)
    #@-node:ekr.20040227212621:p.hasX
    #@+node:ekr.20040307104131.1:p.isAncestorOf
    def isAncestorOf (self, p2):
        
        p = self
        
        if 0: # Avoid the copies made in the iterator.
            for p3 in p2.parents_iter():
                if p3 == p:
                    return True
    
        # Avoid calling p.copy() or copying the stack.
        v2 = p2.v ; n = len(p2.stack)-1
            # Major bug fix 7/22/04: changed len(p.stack) to len(p2.stack.)
        v2,n = p2.vParentWithStack(v2,p2.stack,n)
        while v2:
            if v2 == p.v:
                return True
            v2,n = p2.vParentWithStack(v2,p2.stack,n)
    
        return False
    #@nonl
    #@-node:ekr.20040307104131.1:p.isAncestorOf
    #@+node:ekr.20040803111240:p.isCurrentPosition & isRootPosition
    #@+node:ekr.20040803140033.4:isCurrentPosition
    def isCurrentPosition (self):
        
        p = self ; c = p.c
        
        return c.isCurrentPosition(p)
        
    #@-node:ekr.20040803140033.4:isCurrentPosition
    #@+node:ekr.20040803140033.5:isRootPosition
    def isRootPosition (self):
        
        p = self ; c = p.c
        
        return c.isRootPosition(p)
    #@nonl
    #@-node:ekr.20040803140033.5:isRootPosition
    #@-node:ekr.20040803111240:p.isCurrentPosition & isRootPosition
    #@+node:ekr.20040306215056:p.isCloned
    def isCloned (self):
        
        return len(self.v.t.vnodeList) > 1
    #@nonl
    #@-node:ekr.20040306215056:p.isCloned
    #@+node:ekr.20040307104131.2:p.isRoot
    def isRoot (self):
        
        p = self
    
        return not p.hasParent() and not p.hasBack()
    #@nonl
    #@-node:ekr.20040307104131.2:p.isRoot
    #@+node:ekr.20040117162509.16:p.isVisible
    def isVisible (self):
        
        """Return True if all of a position's parents are expanded."""
    
        # v.isVisible no longer exists.
        p = self
    
        # Avoid calling p.copy() or copying the stack.
        v = p.v ; n = len(p.stack)-1
    
        v,n = p.vParentWithStack(v,p.stack,n)
        while v:
            if not v.isExpanded():
                return False
            v,n = p.vParentWithStack(v,p.stack,n)
    
        return True
    #@nonl
    #@-node:ekr.20040117162509.16:p.isVisible
    #@+node:ekr.20031218072017.4146:p.lastVisible & oldLastVisible
    def oldLastVisible(self):
        """Move to the last visible node of the entire tree."""
        p = self.c.rootPosition()
        assert(p.isVisible())
        last = p.copy()
        while 1:
            if g.app.debug: g.trace(last)
            p.moveToVisNext()
            if not p: break
            last = p.copy()
        return last
            
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
        if 0: # This assert is invalid.
            assert(p.isVisible())
        if g.app.debug: g.trace(p)
        return p
    #@nonl
    #@-node:ekr.20031218072017.4146:p.lastVisible & oldLastVisible
    #@+node:ekr.20040227214711:p.level & simpleLevel
    def simpleLevel(self):
        
        return len([p for p in self.parents_iter()])
    
    def level(self,verbose=False):
        
        p = self ; level = 0
        if not p: return level
            
        # Avoid calling p.copy() or copying the stack.
        v = p.v ; n = len(p.stack)-1
        while 1:
            assert(p)
            v,n = p.vParentWithStack(v,p.stack,n)
            if v:
                level += 1
                if verbose: g.trace(level,"level %2d, n: %2d" % (level,n))
            else:
                if verbose: g.trace(level,"level %2d, n: %2d" % (level,n))
                # if g.app.debug: assert(level==self.simpleLevel())
                break
        return level
    #@nonl
    #@-node:ekr.20040227214711:p.level & simpleLevel
    #@-node:ekr.20040306212636:Getters
    #@+node:ekr.20040305222924:Setters
    #@+node:ekr.20040306220634:vnode proxies
    #@+node:ekr.20040306220634.9: Status bits (position)
    # Clone bits are no longer used.
    # Dirty bits are handled carefully by the position class.
    
    def clearMarked  (self):
        self.v.clearMarked()
        g.doHook("clear-mark",c=self.c,p=self,v=self)
    
    def clearOrphan  (self): return self.v.clearOrphan()
    def clearVisited (self): return self.v.clearVisited()
    
    def contract (self): return self.v.contract()
    def expand   (self): return self.v.expand()
    
    def initExpandedBit    (self): return self.v.initExpandedBit()
    def initMarkedBit      (self): return self.v.initMarkedBit()
    def initStatus (self, status): return self.v.initStatus(status)
        
    def setMarked (self):
        self.v.setMarked()
        g.doHook("set-mark",c=self.c,p=self,v=self)
    
    def setOrphan   (self): return self.v.setOrphan()
    def setSelected (self): return self.v.setSelected()
    def setVisited  (self): return self.v.setVisited()
    #@nonl
    #@-node:ekr.20040306220634.9: Status bits (position)
    #@+node:ekr.20040306220634.8:p.computeIcon & p.setIcon
    def computeIcon (self):
        
        return self.v.computeIcon()
        
    def setIcon (self):
    
        pass # Compatibility routine for old scripts
    #@nonl
    #@-node:ekr.20040306220634.8:p.computeIcon & p.setIcon
    #@+node:ekr.20040306220634.29:p.setSelection
    def setSelection (self,start,length):
    
        return self.v.setSelection(start,length)
    #@nonl
    #@-node:ekr.20040306220634.29:p.setSelection
    #@+node:ekr.20040306220634.31:p.trimTrailingLines
    def trimTrailingLines (self):
    
        return self.v.trimTrailingLines()
    #@nonl
    #@-node:ekr.20040306220634.31:p.trimTrailingLines
    #@+node:ekr.20040315034158:p.setTnodeText
    def setTnodeText (self,s,encoding="utf-8"):
        
        return self.v.setTnodeText(s,encoding)
    #@nonl
    #@-node:ekr.20040315034158:p.setTnodeText
    #@-node:ekr.20040306220634:vnode proxies
    #@+node:ekr.20040315031401:Head & body text (position)
    #@+node:ekr.20040315032503:p.appendStringToBody
    def appendStringToBody (self,s,encoding="utf-8"):
        
        p = self
        if not s: return
        
        body = p.bodyString()
        assert(g.isUnicode(body))
        s = g.toUnicode(s,encoding)
    
        p.setBodyStringOrPane(body + s,encoding)
    #@nonl
    #@-node:ekr.20040315032503:p.appendStringToBody
    #@+node:ekr.20040305223522:p.setBodyStringOrPane & setBodyString
    def setBodyStringOrPane (self,s,encoding="utf-8"):
    
        p = self ; v = p.v ; c = p.c
        if not c or not v: return
    
        s = g.toUnicode(s,encoding)
        current = c.currentPosition()
        # 1/22/05: Major change: the previous test was: 'if p == current:'
        # This worked because commands work on the presently selected node.
        # But setRecentFiles may change a _clone_ of the selected node!
        if current and p.v.t==current.v.t:
            # Revert to previous code, but force an empty selection.
            c.frame.body.setSelectionAreas(s,None,None)
            c.frame.body.setTextSelection(None)
            # This code destoys all tags, so we must recolor.
            c.recolor()
            
        # Keep the body text in the tnode up-to-date.
        if v.t.bodyString != s:
            v.setTnodeText(s)
            v.t.setSelection(0,0)
            p.setDirty()
            if not c.isChanged():
                c.setChanged(True)
    
    setBodyTextOrPane = setBodyStringOrPane # Compatibility with old scripts
    setBodyString = setBodyStringOrPane
    #@-node:ekr.20040305223522:p.setBodyStringOrPane & setBodyString
    #@+node:ekr.20040305222924.1:p.setHeadString & p.initHeadString
    def setHeadString (self,s,encoding="utf-8"):
        
        p = self
        p.v.initHeadString(s,encoding)
        p.setDirty()
        
    def initHeadString (self,s,encoding="utf-8"):
        
        p = self
        p.v.initHeadString(s,encoding)
    #@-node:ekr.20040305222924.1:p.setHeadString & p.initHeadString
    #@+node:ekr.20040305223225:p.setHeadStringOrHeadline
    def setHeadStringOrHeadline (self,s,encoding="utf-8"):
    
        p = self ; t = p.edit_widget()
        
        p.initHeadString(s,encoding)
    
        if t:
            state = t.cget("state")
            # g.trace(state,s)
            t.configure(state="normal")
            t.delete("1.0","end")
            t.insert("end",s)
            t.configure(state=state)
    
        p.setDirty()
    #@nonl
    #@-node:ekr.20040305223225:p.setHeadStringOrHeadline
    #@+node:ekr.20040315031445:p.scriptSetBodyString
    def scriptSetBodyString (self,s,encoding="utf-8"):
        
        """Update the body string for the receiver.
        
        Should be called only from scripts: does NOT update body text."""
    
        self.v.t.bodyString = g.toUnicode(s,encoding)
    #@nonl
    #@-node:ekr.20040315031445:p.scriptSetBodyString
    #@-node:ekr.20040315031401:Head & body text (position)
    #@+node:ekr.20040312015908:Visited bits
    #@+node:ekr.20040312015705:p.clearAllVisited
    # Compatibility routine for scripts.
    
    def clearAllVisited (self):
        
        for p in self.allNodes_iter():
            p.clearVisited()
    #@nonl
    #@-node:ekr.20040312015705:p.clearAllVisited
    #@+node:ekr.20040306220634.17:p.clearVisitedInTree
    # Compatibility routine for scripts.
    
    def clearVisitedInTree (self):
        
        for p in self.self_and_subtree_iter():
            p.clearVisited()
    #@-node:ekr.20040306220634.17:p.clearVisitedInTree
    #@+node:ekr.20031218072017.3388:p.clearAllVisitedInTree (4.2)
    def clearAllVisitedInTree (self):
        
        for p in self.self_and_subtree_iter():
            p.v.clearVisited()
            p.v.t.clearVisited()
            p.v.t.clearWriteBit()
    #@nonl
    #@-node:ekr.20031218072017.3388:p.clearAllVisitedInTree (4.2)
    #@-node:ekr.20040312015908:Visited bits
    #@+node:ekr.20040305162628:p.Dirty bits
    #@+node:ekr.20040311113514:p.clearDirty
    def clearDirty (self):
    
        p = self
        p.v.clearDirty()
    #@nonl
    #@-node:ekr.20040311113514:p.clearDirty
    #@+node:ekr.20040318125934:p.findAllPotentiallyDirtyNodes
    def findAllPotentiallyDirtyNodes(self):
        
        p = self 
        
        # Start with all nodes in the vnodeList.
        nodes = []
        newNodes = p.v.t.vnodeList[:]
    
        # Add nodes until no more are added.
        while newNodes:
            addedNodes = []
            nodes.extend(newNodes)
            for v in newNodes:
                for v2 in v.t.vnodeList:
                    if v2 not in nodes and v2 not in addedNodes:
                        addedNodes.append(v2)
                    for v3 in v2.directParents():
                        if v3 not in nodes and v3 not in addedNodes:
                            addedNodes.append(v3)
            newNodes = addedNodes[:]
    
        # g.trace(len(nodes))
        return nodes
    #@nonl
    #@-node:ekr.20040318125934:p.findAllPotentiallyDirtyNodes
    #@+node:ekr.20040303214038:p.setAllAncestorAtFileNodesDirty
    def setAllAncestorAtFileNodesDirty (self,setDescendentsDirty=False):
    
        p = self ; c = p.c
        dirtyVnodeList = []
        
        # Calculate all nodes that are joined to p or parents of such nodes.
        nodes = p.findAllPotentiallyDirtyNodes()
        
        if setDescendentsDirty:
            # N.B. Only mark _direct_ descendents of nodes.
            # Using the findAllPotentiallyDirtyNodes algorithm would mark way too many nodes.
            for p2 in p.subtree_iter():
                # Only @thin nodes need to be marked.
                if p2.v not in nodes and p2.isAtThinFileNode():
                    nodes.append(p2.v)
                    
        dirtyVnodeList = [v for v in nodes
            if not v.t.isDirty() and v.isAnyAtFileNode()]
        changed = len(dirtyVnodeList) > 0
    
        c.beginUpdate()
        try:
            for v in dirtyVnodeList:
                v.t.setDirty() # Do not call v.setDirty here!
        finally:
            c.endUpdate(changed)
    
        return dirtyVnodeList
    #@nonl
    #@-node:ekr.20040303214038:p.setAllAncestorAtFileNodesDirty
    #@+node:ekr.20040303163330:p.setDirty
    def setDirty (self,setDescendentsDirty=True):
        
        '''Mark a node and all ancestor @file nodes dirty.'''
    
        p = self ; c = p.c ; dirtyVnodeList = []
    
        if not p.v.t.isDirty():
            p.v.t.setDirty()
            dirtyVnodeList.append(p.v)
    
        # Important: this must be called even if p.v is already dirty.
        # Typing can change the @ignore state!
        dirtyVnodeList2 = p.setAllAncestorAtFileNodesDirty(setDescendentsDirty)
        dirtyVnodeList.extend(dirtyVnodeList2)
       
        return dirtyVnodeList
    #@nonl
    #@-node:ekr.20040303163330:p.setDirty
    #@+node:ekr.20040702104823:p.inAtIgnoreRange
    def inAtIgnoreRange (self):
        
        """Returns True if position p or one of p's parents is an @ignore node."""
        
        p = self
        
        for p in p.self_and_parents_iter():
            if p.isAtIgnoreNode():
                return True
    
        return False
    #@nonl
    #@-node:ekr.20040702104823:p.inAtIgnoreRange
    #@-node:ekr.20040305162628:p.Dirty bits
    #@-node:ekr.20040305222924:Setters
    #@+node:ekr.20040315023430:File Conversion
    #@+at
    # - convertTreeToString and moreHead can't be vnode methods because they 
    # uses level().
    # - moreBody could be anywhere: it may as well be a postion method.
    #@-at
    #@+node:ekr.20040315023430.1:convertTreeToString
    def convertTreeToString (self):
        
        """Convert a positions  suboutline to a string in MORE format."""
    
        p = self ; level1 = p.level()
        
        array = []
        for p in p.self_and_subtree_iter():
            array.append(p.moreHead(level1)+'\n')
            body = p.moreBody()
            if body:
                array.append(body +'\n')
    
        return ''.join(array)
    #@-node:ekr.20040315023430.1:convertTreeToString
    #@+node:ekr.20040315023430.2:moreHead
    def moreHead (self, firstLevel,useVerticalBar=False):
        
        """Return the headline string in MORE format."""
        
        # useVerticalBar is unused, but it would be useful in over-ridden methods.
        __pychecker__ = '--no-argsused'
    
        p = self
        level = self.level() - firstLevel
        plusMinus = g.choose(p.hasChildren(), "+", "-")
        
        return "%s%s %s" % ('\t'*level,plusMinus,p.headString())
    #@nonl
    #@-node:ekr.20040315023430.2:moreHead
    #@+node:ekr.20040315023430.3:moreBody
    #@+at 
    #     + test line
    #     - test line
    #     \ test line
    #     test line +
    #     test line -
    #     test line \
    #     More lines...
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
    #@-node:ekr.20040315023430.3:moreBody
    #@-node:ekr.20040315023430:File Conversion
    #@+node:ekr.20040305162628.1:p.Iterators
    #@+at 
    #@nonl
    # 3/18/04: a crucial optimization:
    # 
    # Iterators make no copies at all if they would return an empty sequence.
    #@-at
    #@@c
    
    #@+others
    #@+node:EKR.20040529103843:p.tnodes_iter & unique_tnodes_iter
    def tnodes_iter(self):
        
        """Return all tnode's in a positions subtree."""
        
        p = self
        for p in p.self_and_subtree_iter():
            yield p.v.t
            
    def unique_tnodes_iter(self):
        
        """Return all unique tnode's in a positions subtree."""
        
        p = self
        marks = {}
        for p in p.self_and_subtree_iter():
            if p.v.t not in marks:
                marks[p.v.t] = p.v.t
                yield p.v.t
    #@nonl
    #@-node:EKR.20040529103843:p.tnodes_iter & unique_tnodes_iter
    #@+node:EKR.20040529103945:p.vnodes_iter & unique_vnodes_iter
    def vnodes_iter(self):
        
        """Return all vnode's in a positions subtree."""
        
        p = self
        for p in p.self_and_subtree_iter():
            yield p.v
            
    def unique_vnodes_iter(self):
        
        """Return all unique vnode's in a positions subtree."""
        
        p = self
        marks = {}
        for p in p.self_and_subtree_iter():
            if p.v not in marks:
                marks[p.v] = p.v
                yield p.v
    #@nonl
    #@-node:EKR.20040529103945:p.vnodes_iter & unique_vnodes_iter
    #@+node:ekr.20040305171133:p.allNodes_iter
    class allNodes_iter_class:
    
        """Returns a list of positions in the entire outline."""
    
        #@    @+others
        #@+node:ekr.20040305171133.1:__init__ & __iter__
        def __init__(self,p,copy):
        
            self.first = p.c.rootPosition().copy()
            self.p = None
            self.copy = copy
            
        def __iter__(self):
        
            return self
        #@-node:ekr.20040305171133.1:__init__ & __iter__
        #@+node:ekr.20040305171133.3:next
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
        #@-node:ekr.20040305171133.3:next
        #@-others
    
    def allNodes_iter (self,copy=False):
        
        return self.allNodes_iter_class(self,copy)
    #@nonl
    #@-node:ekr.20040305171133:p.allNodes_iter
    #@+node:ekr.20040305173559:p.subtree_iter
    class subtree_iter_class:
    
        """Returns a list of positions in a subtree, possibly including the root of the subtree."""
    
        #@    @+others
        #@+node:ekr.20040305173559.1:__init__ & __iter__
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
        #@-node:ekr.20040305173559.1:__init__ & __iter__
        #@+node:ekr.20040305173559.2:next
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
        #@-node:ekr.20040305173559.2:next
        #@-others
    
    def subtree_iter (self,copy=False):
        
        return self.subtree_iter_class(self,copy,includeSelf=False)
        
    def self_and_subtree_iter (self,copy=False):
        
        return self.subtree_iter_class(self,copy,includeSelf=True)
    #@nonl
    #@-node:ekr.20040305173559:p.subtree_iter
    #@+node:ekr.20040305172211.1:p.children_iter
    class children_iter_class:
    
        """Returns a list of children of a position."""
    
        #@    @+others
        #@+node:ekr.20040305172211.2:__init__ & __iter__
        def __init__(self,p,copy):
        
            if p.hasChildren():
                self.first = p.copy().moveToFirstChild()
            else:
                self.first = None
        
            self.p = None
            self.copy = copy
        
        def __iter__(self):
            
            return self
        #@-node:ekr.20040305172211.2:__init__ & __iter__
        #@+node:ekr.20040305172211.3:next
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
        #@-node:ekr.20040305172211.3:next
        #@-others
    
    def children_iter (self,copy=False):
        
        return self.children_iter_class(self,copy)
    #@nonl
    #@-node:ekr.20040305172211.1:p.children_iter
    #@+node:ekr.20040305172855:p.parents_iter
    class parents_iter_class:
    
        """Returns a list of positions of a position."""
    
        #@    @+others
        #@+node:ekr.20040305172855.1:__init__ & __iter__
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
        #@-node:ekr.20040305172855.1:__init__ & __iter__
        #@+node:ekr.20040305172855.2:next
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
        #@-node:ekr.20040305172855.2:next
        #@-others
    
    def parents_iter (self,copy=False):
    
        return self.parents_iter_class(self,copy,includeSelf=False)
        
    def self_and_parents_iter(self,copy=False):
        
        return self.parents_iter_class(self,copy,includeSelf=True)
    #@nonl
    #@-node:ekr.20040305172855:p.parents_iter
    #@+node:ekr.20040305173343:p.siblings_iter
    class siblings_iter_class:
    
        '''Returns a list of siblings of a position, including the position itself!'''
    
        #@    @+others
        #@+node:ekr.20040305173343.1:__init__ & __iter__
        def __init__(self,p,copy,following):
            
            # We always include p, even if following is True.
            
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
        
        #@-node:ekr.20040305173343.1:__init__ & __iter__
        #@+node:ekr.20040305173343.2:next
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
        #@-node:ekr.20040305173343.2:next
        #@-others
    
    def siblings_iter (self,copy=False,following=False):
        
        return self.siblings_iter_class(self,copy,following)
        
    self_and_siblings_iter = siblings_iter
        
    def following_siblings_iter (self,copy=False):
        
        return self.siblings_iter_class(self,copy,following=True)
    #@nonl
    #@-node:ekr.20040305173343:p.siblings_iter
    #@-others
    #@nonl
    #@-node:ekr.20040305162628.1:p.Iterators
    #@+node:ekr.20040303175026:p.Moving, Inserting, Deleting, Cloning, Sorting (position)
    #@+node:ekr.20040303175026.2:p.doDelete
    #@+at 
    #@nonl
    # This is the main delete routine.  It deletes the receiver's entire tree 
    # from the screen.  Because of the undo command we never actually delete 
    # vnodes or tnodes.
    #@-at
    #@@c
    
    def doDelete (self):
    
        """Deletes position p from the outline.  May be undone.
    
        Returns newPosition."""
    
        p = self ; c = p.c
        p.setDirty() # Mark @file nodes dirty!
        p.unlink()
        p.deleteLinksInTree()
    #@nonl
    #@-node:ekr.20040303175026.2:p.doDelete
    #@+node:ekr.20040303175026.3:p.insertAfter
    def insertAfter (self,t=None):
    
        """Inserts a new position after self.
        
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
    #@-node:ekr.20040303175026.3:p.insertAfter
    #@+node:ekr.20040303175026.4:p.insertAsLastChild
    def insertAsLastChild (self,t=None):
    
        """Inserts a new vnode as the last child of self.
        
        Returns the newly created position."""
        
        p = self
        n = p.numberOfChildren()
    
        if not t:
            t = tnode(headString="NewHeadline")
        
        return p.insertAsNthChild(n,t)
    #@nonl
    #@-node:ekr.20040303175026.4:p.insertAsLastChild
    #@+node:ekr.20040303175026.5:p.insertAsNthChild
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
    #@-node:ekr.20040303175026.5:p.insertAsNthChild
    #@+node:ekr.20040303175026.6:p.moveToRoot
    def moveToRoot (self,oldRoot=None):
    
        '''Moves a position to the root position.
        
        Important: oldRoot must the previous root position if it exists.'''
    
        p = self # Do NOT copy the position!
        p.unlink()
        p.linkAsRoot(oldRoot)
        
        return p
    #@nonl
    #@-node:ekr.20040303175026.6:p.moveToRoot
    #@+node:ekr.20040303175026.8:p.clone
    def clone (self,back):
        
        """Create a clone of back.
        
        Returns the newly created position."""
        
        p = self ; c = p.c
        
        # g.trace(p,back)
    
        p2 = back.copy()
        p2.v = vnode(c,back.v.t)
        p2.linkAfter(back)
    
        return p2
    #@nonl
    #@-node:ekr.20040303175026.8:p.clone
    #@+node:ekr.20040303175026.9:p.copyTreeAfter, copyTreeTo
    # This is used by unit tests.
    
    def copyTreeAfter(self):
        p = self
        p2 = p.insertAfter()
        p.copyTreeFromSelfTo(p2)
        return p2
        
    def copyTreeFromSelfTo(self,p2):
        p = self
        p2.v.t.headString = p.headString()
        p2.v.t.bodyString = p.bodyString()
        for child in p.children_iter(copy=True):
            child2 = p2.insertAsLastChild()
            child.copyTreeFromSelfTo(child2)
    #@nonl
    #@-node:ekr.20040303175026.9:p.copyTreeAfter, copyTreeTo
    #@+node:ekr.20040303175026.10:p.moveAfter
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
    #@-node:ekr.20040303175026.10:p.moveAfter
    #@+node:ekr.20040306060312:p.moveToLastChildOf
    def moveToLastChildOf (self,parent):
    
        """Move a position to the last child of parent."""
    
        p = self # Do NOT copy the position!
    
        p.unlink()
        n = parent.numberOfChildren()
        p.linkAsNthChild(parent,n)
    
        # Moving a node can create a new root node.
        if not parent.hasParent() and not parent.hasBack():
            p.c.setRootPosition(parent)
            
        return p
    #@-node:ekr.20040306060312:p.moveToLastChildOf
    #@+node:ekr.20040303175026.11:p.moveToNthChildOf
    def moveToNthChildOf (self,parent,n):
    
        """Move a position to the nth child of parent."""
    
        p = self ; c = p.c # Do NOT copy the position!
        
        # g.trace(p,parent,n)
    
        p.unlink()
        p.linkAsNthChild(parent,n)
        
        # Moving a node can create a new root node.
        if not parent.hasParent() and not parent.hasBack():
            if not parent.equal(c.rootPosition()):
                # g.trace('old root',c.rootPosition(),'new root',parent())
                c.setRootPosition(parent)
    
        return p
    #@-node:ekr.20040303175026.11:p.moveToNthChildOf
    #@+node:ekr.20040303175026.13:p.validateOutlineWithParent
    # This routine checks the structure of the receiver's tree.
    
    def validateOutlineWithParent (self,pv):
        
        p = self
        result = True # optimists get only unpleasant surprises.
        parent = p.getParent()
        childIndex = p.childIndex()
        
        # g.trace(p,parent,pv)
        #@    << validate parent ivar >>
        #@+node:ekr.20040303175026.14:<< validate parent ivar >>
        if parent != pv:
            p.invalidOutline( "Invalid parent link: " + repr(parent))
        #@nonl
        #@-node:ekr.20040303175026.14:<< validate parent ivar >>
        #@nl
        #@    << validate childIndex ivar >>
        #@+node:ekr.20040303175026.15:<< validate childIndex ivar >>
        if pv:
            if childIndex < 0:
                p.invalidOutline ( "missing childIndex" + childIndex )
            elif childIndex >= pv.numberOfChildren():
                p.invalidOutline ( "missing children entry for index: " + childIndex )
        elif childIndex < 0:
            p.invalidOutline ( "negative childIndex" + childIndex )
        #@nonl
        #@-node:ekr.20040303175026.15:<< validate childIndex ivar >>
        #@nl
        #@    << validate x ivar >>
        #@+node:ekr.20040303175026.16:<< validate x ivar >>
        if not p.v.t and pv:
            self.invalidOutline ( "Empty t" )
        #@nonl
        #@-node:ekr.20040303175026.16:<< validate x ivar >>
        #@nl
    
        # Recursively validate all the children.
        for child in p.children_iter():
            r = child.validateOutlineWithParent(p)
            if not r: result = False
    
        return result
    #@nonl
    #@-node:ekr.20040303175026.13:p.validateOutlineWithParent
    #@+node:ekr.20040310062332.1:p.invalidOutline
    def invalidOutline (self, message):
        
        p = self
    
        if p.hasParent():
            node = p.parent()
        else:
            node = p
    
        g.alert("invalid outline: %s\n%s" % (message,node))
    #@nonl
    #@-node:ekr.20040310062332.1:p.invalidOutline
    #@-node:ekr.20040303175026:p.Moving, Inserting, Deleting, Cloning, Sorting (position)
    #@+node:ekr.20031218072017.928:p.moveToX
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
    #     after = p.copy().moveToNodeAfterTree()
    #@-at
    #@nonl
    #@+node:ekr.20031218072017.930:p.moveToBack
    def moveToBack (self):
        
        """Move self to its previous sibling."""
        
        p = self
    
        p.v = p.v and p.v._back
        
        return p
    #@nonl
    #@-node:ekr.20031218072017.930:p.moveToBack
    #@+node:ekr.20031218072017.931:p.moveToFirstChild (pushes stack for cloned nodes)
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
    
    #@-node:ekr.20031218072017.931:p.moveToFirstChild (pushes stack for cloned nodes)
    #@+node:ekr.20031218072017.932:p.moveToLastChild (pushes stack for cloned nodes)
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
    #@-node:ekr.20031218072017.932:p.moveToLastChild (pushes stack for cloned nodes)
    #@+node:ekr.20031218072017.933:p.moveToLastNode (Big improvement for 4.2)
    def moveToLastNode (self):
        
        """Move a position to last node of its tree.
        
        N.B. Returns p if p has no children."""
        
        p = self
        
        # Huge improvement for 4.2.
        while p.hasChildren():
            p.moveToLastChild()
    
        return p
    #@nonl
    #@-node:ekr.20031218072017.933:p.moveToLastNode (Big improvement for 4.2)
    #@+node:ekr.20031218072017.934:p.moveToNext
    def moveToNext (self):
        
        """Move a position to its next sibling."""
        
        p = self
        
        p.v = p.v and p.v._next
        
        return p
    #@nonl
    #@-node:ekr.20031218072017.934:p.moveToNext
    #@+node:ekr.20031218072017.935:p.moveToNodeAfterTree
    def moveToNodeAfterTree (self):
        
        """Move a position to the node after the position's tree."""
        
        p = self
        
        while p:
            if p.hasNext():
                p.moveToNext()
                break
            p.moveToParent()
    
        return p
    #@-node:ekr.20031218072017.935:p.moveToNodeAfterTree
    #@+node:ekr.20031218072017.936:p.moveToNthChild (pushes stack for cloned nodes)
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
    #@-node:ekr.20031218072017.936:p.moveToNthChild (pushes stack for cloned nodes)
    #@+node:ekr.20031218072017.937:p.moveToParent (pops stack when multiple parents)
    def moveToParent (self):
        
        """Move a position to its parent position."""
        
        p = self
        
        if not p: return p
    
        if p.v._parent and len(p.v._parent.t.vnodeList) == 1:
            p.v = p.v._parent
        elif p.stack:
            p.v = p.stack.pop()
        else:
            p.v = None
        return p
    #@nonl
    #@-node:ekr.20031218072017.937:p.moveToParent (pops stack when multiple parents)
    #@+node:ekr.20031218072017.938:p.moveToThreadBack
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
    #@-node:ekr.20031218072017.938:p.moveToThreadBack
    #@+node:ekr.20031218072017.939:p.moveToThreadNext
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
    #@-node:ekr.20031218072017.939:p.moveToThreadNext
    #@+node:ekr.20031218072017.940:p.moveToVisBack
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
    #@-node:ekr.20031218072017.940:p.moveToVisBack
    #@+node:ekr.20031218072017.941:p.moveToVisNext
    def moveToVisNext (self):
        
        """Move a position to the position of the next visible node."""
    
        p = self
    
        p.moveToThreadNext()
        while p and not p.isVisible():
            p.moveToThreadNext()
                
        return p
    #@nonl
    #@-node:ekr.20031218072017.941:p.moveToVisNext
    #@-node:ekr.20031218072017.928:p.moveToX
    #@+node:ekr.20040228094013.1:p.utils...
    #@+node:ekr.20040228060340:p.vParentWithStack
    # A crucial utility method.
    # The p.level(), p.isVisible() and p.hasThreadNext() methods show how to use this method.
    
    #@<< about the vParentWithStack utility method >>
    #@+node:ekr.20040228060340.1:<< about the vParentWithStack utility method >>
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
    #     p = p.moveToParent()
    #     if p: list1.append(p.v)
    # 
    # # The second way uses p.vParentWithStack to avoid all odious 
    # intermediate data.
    # 
    # list2 = []
    # n = len(p.stack)-1
    # v,n = p.vParentWithStack(v,p.stack,n)
    # while v:
    #     list2.append(v)
    #     v,n = p.vParentWithStack(v,p.stack,n)
    # 
    #@-at
    #@-node:ekr.20040228060340.1:<< about the vParentWithStack utility method >>
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
    #@-node:ekr.20040228060340:p.vParentWithStack
    #@+node:ekr.20040409203454:p.restoreLinksInTree
    def restoreLinksInTree (self):
    
        """Restore links when undoing a delete node operation."""
        
        root = p = self
    
        if p.v not in p.v.t.vnodeList:
            p.v.t.vnodeList.append(p.v)
            
        for p in root.children_iter():
            p.restoreLinksInTree()
    #@nonl
    #@-node:ekr.20040409203454:p.restoreLinksInTree
    #@+node:ekr.20040409203454.1:p.deleteLinksInTree & allies
    def deleteLinksInTree (self):
        
        """Delete and otherwise adjust links when deleting node."""
        
        root = self
    
        root.deleteLinksInSubtree()
        
        for p in root.children_iter():
            p.adjustParentLinksInSubtree(parent=root)
    #@nonl
    #@+node:ekr.20040410170806:p.deleteLinksInSubtree
    def deleteLinksInSubtree (self):
    
        root = p = self
    
        # Delete p.v from the vnodeList
        if p.v in p.v.t.vnodeList:
            p.v.t.vnodeList.remove(p.v)
            assert(p.v not in p.v.t.vnodeList)
            # g.trace("deleted",p.v,p.vnodeListIds())
        else:
            # g.trace("not in vnodeList",p.v,p.vnodeListIds())
            pass
    
        if len(p.v.t.vnodeList) == 0:
            # This node is not shared by other nodes.
            for p in root.children_iter():
                p.deleteLinksInSubtree()
    #@nonl
    #@-node:ekr.20040410170806:p.deleteLinksInSubtree
    #@+node:ekr.20040410170806.1:p.adjustParentLinksInSubtree
    def adjustParentLinksInSubtree (self,parent):
        
        root = p = self
        
        assert(parent)
        
        if p.v._parent and parent.v.t.vnodeList and p.v._parent not in parent.v.t.vnodeList:
            p.v._parent = parent.v.t.vnodeList[0]
            
        for p in root.children_iter():
            p.adjustParentLinksInSubtree(parent=root)
    #@nonl
    #@-node:ekr.20040410170806.1:p.adjustParentLinksInSubtree
    #@-node:ekr.20040409203454.1:p.deleteLinksInTree & allies
    #@-node:ekr.20040228094013.1:p.utils...
    #@+node:ekr.20040310062332:p.Link/Unlink methods
    # These remain in 4.2:  linking and unlinking does not depend on position.
    
    # These are private routines:  the position class does not define proxies for these.
    #@nonl
    #@+node:ekr.20040310062332.2:p.linkAfter
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
    #@-node:ekr.20040310062332.2:p.linkAfter
    #@+node:ekr.20040310062332.3:p.linkAsNthChild
    def linkAsNthChild (self,parent,n):
    
        """Links self as the n'th child of vnode pv"""
        
        # g.trace(self,parent,n,parent.v)
    
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
    #@-node:ekr.20040310062332.3:p.linkAsNthChild
    #@+node:ekr.20040310062332.4:p.linkAsRoot
    def linkAsRoot (self,oldRoot):
        
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
        
        # Add v to it's tnode's vnodeList. Bug fix: 5/02/04.
        if v not in v.t.vnodeList:
            v.t.vnodeList.append(v)
    
        # Link in the rest of the tree only when oldRoot != None.
        # Otherwise, we are calling this routine from init code and
        # we want to start with a pristine tree.
        if oldRoot:
            oldRoot.v._back = v # Bug fix: 3/12/04
    
        p.c.setRootPosition(p)
        
        if 0:
            p.dump(label="root")
    #@-node:ekr.20040310062332.4:p.linkAsRoot
    #@+node:ekr.20040310062332.5:p.unlink
    def unlink (self):
    
        """Unlinks a position p from the tree before moving or deleting.
        
        The p.v._fistChild link does NOT change."""
        
        # Warning: p.parent() is NOT necessarily the same as p.v._parent!
    
        p = self ; v = p.v
        
        # g.trace('p.v._parent',p.v._parent," child:",v.t._firstChild," back:",v._back, " next:",v._next)
        
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
        if p.v._parent:
            if 0: # This can fail.  I have no idea why it was present.
                assert(p.v and p.v._parent in p.v.directParents())
            if p.v._parent.t._firstChild == v:
                #g.trace('resetting _parent.v.t._firstChild to',v._next)
                p.v._parent.t._firstChild = v._next
        else:
            parent = p.parent()
            if parent:
                if 0: # This can fail.  I have no idea why it was present.
                    assert(parent.v in p.v.directParents())
                if parent.v.t._firstChild == v:
                    #g.trace('resetting parent().v.t._firstChild to',v._next)
                    parent.v.t._firstChild = v._next
    
        # Do NOT delete the links in any child nodes.
    
        # Clear the links in other nodes.
        if v._back: v._back._next = v._next
        if v._next: v._next._back = v._back
    
        # Unlink _this_ node.
        v._parent = v._next = v._back = None
    
        if 0:
            g.trace('-'*20)
            p.dump(label="p")
            if parent: parent.dump(label="parent")
    #@nonl
    #@-node:ekr.20040310062332.5:p.unlink
    #@-node:ekr.20040310062332:p.Link/Unlink methods
    #@-others
#@nonl
#@-node:ekr.20031218072017.889:class position
#@-others
#@nonl
#@-node:ekr.20031218072017.3320:@thin leoNodes.py
#@-leo
