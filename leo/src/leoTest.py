#@+leo
#@+node:0::@file leoTest.py
#@+body
"""Perform unit testing on Leo itself"""


#@+at
#  This module defines classes and scripts for testing Leo.
# 
# - This module will be moved into the 3.11 code base in order to generate 
# reference files in the ../test/ref folder.

#@-at
#@@c


import unittest
from leoGlobals import *


#@+others
#@+node:1::test outline operations
#@+body
import leoNodes

class LeoNodeError(Exception): pass


#@<< test functions >>
#@+node:1::<< test functions >>
#@+body
#@+at
#  These functions set up trees for testing and compare the result of a test 
# with the expected result.

#@-at
#@@c


#@+others
#@+node:1::numberOfNodesInOutline, numberOfClonesInOutline
#@+body
def numberOfNodesInOutline (root):
	
	"""Returns the total number of nodes in an outline"""
	
	n = 0 ; v = root
	while v:
		n +=1
		v = v.threadNext()
	return n
	
def numberOfClonesInOutline (root):
	
	"""Returns the number of cloned nodes in an outline"""

	n = 0 ; v = root
	while v:
		if v.isCloned():
			n += 1
		v = v.threadNext()
#@-body
#@-node:1::numberOfNodesInOutline, numberOfClonesInOutline
#@+node:2::createTestOutline
#@+body
def createTestOutline():
	
	"""Creates a complex outline suitable for testing clones"""
	pass
#@-body
#@-node:2::createTestOutline
#@+node:3::loadTestLeoFile
#@+body
def loadTestLeoFile (leoFileName):
	
	"""Loads a .leo file containing a test outline"""
#@-body
#@-node:3::loadTestLeoFile
#@+node:4::copyTestOutline
#@+body
def copyTestOutline ():
	
	"""Copies an outline so that all join Links are "equivalent" to the original"""
	pass
#@-body
#@-node:4::copyTestOutline
#@+node:5::compareTwoOutlines
#@+body
def compareTwoOutlines (root1,root2):
	
	"""Compares two outlines, making sure that their topologies,
	content and join lists are equivent"""
	pass
#@-body
#@-node:5::compareTwoOutlines
#@+node:6::compareLeoFiles
#@+body
def compareLeoFiles (commander1, commander2):
	
	"""Compares the outlines in two Leo files"""
	
	c1 = commander1 ; c2 = commander2
	root1 = c1.rootVnode()
	root2 = c2.rootVnode()

#@-body
#@-node:6::compareLeoFiles
#@+node:7::validateOutline
#@+body
def validateOutline (root):
	
	"""Checks an outline for consistency"""
	pass
#@-body
#@-node:7::validateOutline
#@-others
#@-body
#@-node:1::<< test functions >>


# Create before/after snapshots of operations:  How?????

class cloneCheck(unittest.TestCase):
	"""test cloning and inserts and deletes involving clones"""
	
	#@<< clone test cases >>
	#@+node:2::<< clone test cases >>
	#@+body
	#@+others
	#@+node:1::testCone
	#@+body
	def testCone(self):
		pass
	
	#@-body
	#@-node:1::testCone
	#@+node:2::testMoveIntoClone
	#@+body
	def testMoveIntoClone(self):
		pass
	
	#@-body
	#@-node:2::testMoveIntoClone
	#@+node:3::testMoveOutOfClone
	#@+body
	def testMoveOutOfClone(self):
		pass
	
	#@-body
	#@-node:3::testMoveOutOfClone
	#@+node:4::testInsertInsideClone
	#@+body
	def testInsertInsideClone(self):
		pass
	
	#@-body
	#@-node:4::testInsertInsideClone
	#@+node:5::testDeleteInsideClone
	#@+body
	def testDeleteInsideClone(self):
		pass
	
	#@-body
	#@-node:5::testDeleteInsideClone
	#@+node:6::testInsertInsideClone
	#@+body
	def testInsertInsideClone(self):
		pass
		
	
	#@-body
	#@-node:6::testInsertInsideClone
	#@+node:7::testDeleteInsideClone
	#@+body
	def testDeleteInsideClone(self):
		pass
	
	#@-body
	#@-node:7::testDeleteInsideClone
	#@-others
	
	#@-body
	#@-node:2::<< clone test cases >>


class moveCheck(unittest.TestCase):
	"""test that moves work properly, especially when clones are involved"""
	
	#@<< move test cases >>
	#@+node:3::<< move test cases >>
	#@+body
	pass # no tests yet
	#@-body
	#@-node:3::<< move test cases >>

	
class undoCheck(unittest.TestCase):
	"""test that undo works properly, especially when clones are involved"""
	
	#@<< undo test cases >>
	#@+node:4::<< undo test cases >>
	#@+body
	#@+others
	#@+node:1::testUndoMoveLeft
	#@+body
	def testUndoMoveLeft(self):
		pass
	
	#@-body
	#@-node:1::testUndoMoveLeft
	#@+node:2::testRedoMoveLeft
	#@+body
	def testRedoMoveLeft(self):
		pass
	#@-body
	#@-node:2::testRedoMoveLeft
	#@-others
	
	#@-body
	#@-node:4::<< undo test cases >>

	
class sanityCheck(unittest.TestCase):
	"""Tests that links, joinLists and related getters are consistent"""
	
	#@<< sanity checks >>
	#@+node:5::<< sanity checks >>
	#@+body
	#@+others
	#@+node:1::testNextBackLinks
	#@+body
	def testNextBackLinks(self):
		
		"""Sanity checks for v.mNext and v.mBack"""
		pass
	
	#@-body
	#@-node:1::testNextBackLinks
	#@+node:2::testParentChildLinks
	#@+body
	def testParentChildLinks(self):
		
		"""Sanity checks for v.mParent and v.mFirstChild"""
		pass
	
	#@-body
	#@-node:2::testParentChildLinks
	#@+node:3::testJoinLists
	#@+body
	def testJoinLists(self):
		
		"""Sanity checks for join lists"""
		pass
	#@-body
	#@-node:3::testJoinLists
	#@+node:4::testThreadNextBack
	#@+body
	def testThreadNextBack(self):
		
		"""Sanity checks for v.threadNext() and v.threadBack()"""
		pass
	
	#@-body
	#@-node:4::testThreadNextBack
	#@+node:5::testNextBack
	#@+body
	def testNextBack(self):
		
		"""Sanity checks for v.vext() and v.vack()"""
		pass
	
	#@-body
	#@-node:5::testNextBack
	#@+node:6::testVisNextBack
	#@+body
	def testVisNextBack(self):
		
		"""Sanity checks for v.visNext() and v.visBack()"""
		pass
	
	#@-body
	#@-node:6::testVisNextBack
	#@+node:7::testFirstChildParent
	#@+body
	def testFirstChildParent(self):
		
		"""Sanity checks for v.firstChild() and v.parent()"""
		pass
	
	#@-body
	#@-node:7::testFirstChildParent
	#@-others
	
	#@-body
	#@-node:5::<< sanity checks >>

	
class statusBitsCheck(unittest.TestCase):
	"""Tests that status bits are handled properly"""
	
	#@<< status bits checks >>
	#@+node:6::<< status bits checks >>
	#@+body
	#@+others
	#@+node:1::testDirtyBits
	#@+body
	def testDirtyBits(self):
		
		"""Test that dirty bits are set, especially in anscestor nodes and cloned nodes"""
		pass
	
	#@-body
	#@-node:1::testDirtyBits
	#@-others
	
	#@-body
	#@-node:6::<< status bits checks >>


#@-body
#@-node:1::test outline operations
#@+node:2::check consistency of Leo files
#@+body
import unittest

class LeoOutlineError(Exception): pass

class outlineCheck(unittest.TestCase):
	"""test the consistency of .leo files"""
	pass

#@-body
#@-node:2::check consistency of Leo files
#@+node:3::Scripts for checking clones
#@+node:1::checkForMismatchedJoinedNodes
#@+body
def checkForMismatchedJoinedNodes (c=None):
	
	"""Checks outline for possible broken join lists"""

	if not c: c = top()
	d = {} # Keys are tnodes, values are headlines.
	v = c.rootVnode()
	while v:
		aTuple = d.get(v.t)
		if aTuple:
			head,body = aTuple
			if v.headString()!= head:
				es("headline mismatch in joined nodes",`v`)
			if v.bodyString()!= body:
				es("body mismatch in joined nodes",`v`)
		else:
			d[v.t] = (v.headString(),v.bodyString())
		v = v.threadNext()

	es("end of checkForMismatchedJoinedNodes")

#@-body
#@-node:1::checkForMismatchedJoinedNodes
#@+node:2::checkForPossiblyBrokenLinks
#@+body
def checkForPossiblyBrokenLinks (c=None):
	
	"""Checks outline for possible broken join lists"""
	
	if not c: c = top()
	d = {} # Keys are headlines, values are (tnodes,parent) tuples
	v = c.rootVnode()
	while v:
		h = v.headString()
		parent = v.parent()
		aTuple = d.get(h)
		if aTuple:
			t,p = aTuple
			if (t != v.t and p and parent and p.t != parent.t and
				p.headString() == parent.headString() and
				len(h) > 1 and h != "NewHeadline"):
				es("different tnodes with same headline and parent headlines: " + v.headString())
		else:
			d[h] = (v.t,parent)
		v = v.threadNext()

#@-body
#@-node:2::checkForPossiblyBrokenLinks
#@+node:3::checkTopologiesOfLinkedNodes
#@+body
def checkTopologiesOfLinkedNodes(c=None):
	
	if not c: c = top()
	d = {} # Keys are tnodes, values are topology lists.
	v = c.rootVnode()
	count = 0
	while v:
		top1 = createTopologyList(c=c,root=v)
		top2 = d.get(v.t)
		if top2:
			count += 1
			if top1 != top1:
				es("mismatched topologies for two vnodes with the same tnode!",`v`)
		else:
			d[v.t] = top1
		v = v.threadNext()
	es("end of checkTopologiesOfLinkedNodes. Checked nodes: " + `count`)

#@-body
#@-node:3::checkTopologiesOfLinkedNodes
#@+node:4::checkLinksOfNodesWithSameTopologies (to do)
#@+body
#@+at
#  Nodes with the same topologies should be joined PROVIDED:
# 	- Topologies are non-trivial.
# 	- Topologies include tnodes somehow.
# 	- Topologies include headlines somehow.

#@-at
#@-body
#@-node:4::checkLinksOfNodesWithSameTopologies (to do)
#@-node:3::Scripts for checking clones
#@-others


if 0:
	checkForMismatchedJoinedNodes()
	
	print createTopologyList(c=top(),root=top().currentVnode().parent(),useHeadlines=false)
	
	checkTopologiesOfLinkedNodes()
	
	checkForPossiblyBrokenLinks()

#@-body
#@-node:0::@file leoTest.py
#@-leo
