#@+leo-ver=4
#@+node:@file leoTest.py
"""Unit tests for Leo"""

from leoGlobals import *
import unittest

import leoColor,leoCommands,leoFrame,leoNodes
import Tkinter
import os,sys
Tk = Tkinter

#@+others
#@+node: testUtils
class testUtils:
	
	"""Common utility routines used by unit tests."""

	#@	@+others
	#@+node:compareOutlines
	def compareOutlines (self,root1,root2):
		
		"""Compares two outlines, making sure that their topologies,
		content and join lists are equivent"""
	
		v1,v2 = root1,root2
		after1 = v1.nodeAfterTree()
		after2 = v2.nodeAfterTree()
		while v1 and v2 and v1 != after1 and v2 != after2:
			if v1.numberOfChildren() != v2.numberOfChildren():
				return false
			if v1.headString() != v2.headString():
				return false
			if v1.bodyString() != v2.bodyString():
				return false
			if v1.isCloned() != v2.isCloned():
				return false
			v1 = v1.threadNext()
			v2 = v2.threadNext()
		return v1 == None and v2 == None
	#@nonl
	#@-node:compareOutlines
	#@+node:createTestsForSubnodes (doesn't work)
	if 0: # Doesn't work
	
		def createTestsForSubnodes(self,name,testClass):
		
			u = self
			suite = unittest.makeSuite(unittest.TestCase)
			vList = u.findSubnodesOf(name)
			for v in vList:
				h = v.headString()
				test = testClass(v)
				suite.addTest(test)
			return suite,vList
	#@nonl
	#@-node:createTestsForSubnodes (doesn't work)
	#@+node:findChildrenOf & findSubnodesOf
	def findChildrenOf (self,headline):
		
		u = self ; c = top() ; v = c.currentVnode()
		root = u.findRootNode(v)
		parent = u.findNodeInTree(root,headline)
		v = parent.firstChild()
		vList = []
		while v:
			vList.append(v)
			v = v.next()
		return vList
	
	def findSubnodesOf (self,headline):
		
		u = self ; c = top() ; v = c.currentVnode()
		root = u.findRootNode(v)
		parent = u.findNodeInTree(root,headline)
		v = parent.firstChild()
		vList = []
		after = parent.nodeAfterTree()
		while v and v != after:
			vList.append(v)
			v = v.threadNext()
		return vList
	#@nonl
	#@-node:findChildrenOf & findSubnodesOf
	#@+node:findNodeInRootTree, findNodeInTree, findNodeAnywhere
	def findRootNode (self,v):
	
		"""Return the root of v's tree."""
		while v and v.parent():
			v = v.parent()
		return v
		
	def findNodeInTree(self,v,headline):
	
		"""Search for a node in v's tree matching the given headline."""
		if not headline: return None # This is valid.
		after = v.nodeAfterTree()
		while v and v != after:
			if v.headString().strip() == headline.strip():
				return v
			v = v.threadNext()
		return None
	
	def findNodeAnywhere(self,c,headline):
		
		if not headline: return None # This is valid.
		v = c.rootVnode()
		while v:
			if v.headString().strip() == headline.strip():
				return v
			v = v.threadNext()
		return None
	#@nonl
	#@-node:findNodeInRootTree, findNodeInTree, findNodeAnywhere
	#@+node:numberOfNodesInOutline, numberOfClonesInOutline
	def numberOfNodesInOutline (self,root):
		
		"""Returns the total number of nodes in an outline"""
		
		n = 0 ; v = root
		while v:
			n +=1
			v = v.threadNext()
		return n
		
	def numberOfClonesInOutline (self,root):
		
		"""Returns the number of cloned nodes in an outline"""
	
		n = 0 ; v = root
		while v:
			if v.isCloned():
				n += 1
			v = v.threadNext()
	#@nonl
	#@-node:numberOfNodesInOutline, numberOfClonesInOutline
	#@+node:validateOutline TODO
	def validateOutline (self,root):
		
		"""Checks an outline for consistency"""
		pass
	#@nonl
	#@-node:validateOutline TODO
	#@-others
#@nonl
#@-node: testUtils
#@+node:Node tests...
import leoNodes

class leoNodeError(Exception):
	pass
	
#@nonl
#@-node:Node tests...
#@+node:class cloneTests
class cloneTests(unittest.TestCase):
	
	"""tests of cloning and inserts and deletes involving clones"""
	
	#@	@+others
	#@+node:testCone
	def testCone(self):
		pass
	#@-node:testCone
	#@+node:testMoveIntoClone
	def testMoveIntoClone(self):
		pass
	#@-node:testMoveIntoClone
	#@+node:testMoveOutOfClone
	def testMoveOutOfClone(self):
		pass
	#@-node:testMoveOutOfClone
	#@+node:testInsertInsideClone
	def testInsertInsideClone(self):
		pass
	#@-node:testInsertInsideClone
	#@+node:testDeleteInsideClone
	def testDeleteInsideClone(self):
		pass
	#@-node:testDeleteInsideClone
	#@+node:testInsertInsideClone
	def testInsertInsideClone(self):
		pass
		
	#@-node:testInsertInsideClone
	#@+node:testDeleteInsideClone
	def testDeleteInsideClone(self):
		pass
	#@-node:testDeleteInsideClone
	#@-others
#@nonl
#@-node:class cloneTests
#@+node:class moveTests
class moveTests(unittest.TestCase):
	
	"""test that moves work properly, especially when clones are involved"""
	
	pass # no tests yet.
#@-node:class moveTests
#@+node:class nodeSanityTests
class nodeSanityTests(unittest.TestCase):

	"""Tests that links, joinLists and related getters are consistent"""
	
	#@	@+others
	#@+node:testNextBackLinks
	def testNextBackLinks(self):
		
		"""Sanity checks for v.mNext and v.mBack"""
		pass
	#@-node:testNextBackLinks
	#@+node:testParentChildLinks
	def testParentChildLinks(self):
		
		"""Sanity checks for v.mParent and v.mFirstChild"""
		pass
	#@-node:testParentChildLinks
	#@+node:testJoinLists
	def testJoinLists(self):
		
		"""Sanity checks for join lists"""
		pass
	#@nonl
	#@-node:testJoinLists
	#@+node:testThreadNextBack
	def testThreadNextBack(self):
		
		"""Sanity checks for v.threadNext() and v.threadBack()"""
		pass
	#@-node:testThreadNextBack
	#@+node:testNextBack
	def testNextBack(self):
		
		"""Sanity checks for v.vext() and v.vack()"""
		pass
	#@-node:testNextBack
	#@+node:testVisNextBack
	def testVisNextBack(self):
		
		"""Sanity checks for v.visNext() and v.visBack()"""
		pass
	#@-node:testVisNextBack
	#@+node:testFirstChildParent
	def testFirstChildParent(self):
		
		"""Sanity checks for v.firstChild() and v.parent()"""
		pass
	#@-node:testFirstChildParent
	#@-others
#@nonl
#@-node:class nodeSanityTests
#@+node:class statusBitsChecks
class statusBitsChecks(unittest.TestCase):
	
	"""Tests that status bits are handled properly"""
	
	#@	@+others
	#@+node:testDirtyBits
	def testDirtyBits(self):
		
		"""Test that dirty bits are set, especially in anscestor nodes and cloned nodes"""
		pass
	#@-node:testDirtyBits
	#@-others
#@nonl
#@-node:class statusBitsChecks
#@+node:class undoTests
class undoTests(unittest.TestCase):
	
	"""test that undo works properly, especially when clones are involved"""
	
	#@	@+others
	#@+node:testUndoMoveLeft
	def testUndoMoveLeft(self):
		pass
	#@-node:testUndoMoveLeft
	#@+node:testRedoMoveLeft
	def testRedoMoveLeft(self):
		pass
	#@nonl
	#@-node:testRedoMoveLeft
	#@-others
#@nonl
#@-node:class undoTests
#@+node:class fileTests
class fileTests(unittest.TestCase):
	
	"""Unit tests for Leo's file operations."""
	
	#@	@+others
	#@-others
#@nonl
#@-node:class fileTests
#@+node: makeColorSuite
def makeColorSuite(testParentHeadline,tempHeadline):
	
	"""Create a colorizer test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top() ; v = c.currentVnode()
	root = u.findRootNode(v)
	temp_v = u.findNodeInTree(root,tempHeadline)
	vList = u.findSubnodesOf(testParentHeadline)
	
	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		test = colorTestCase(c,v,temp_v)
		suite.addTest(test)

	return suite
#@nonl
#@-node: makeColorSuite
#@+node:class colorTestCase
class colorTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's colorizer."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,v,temp_v):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.c = c
		self.v = v
		self.temp_v = temp_v
		
		self.old_v = c.currentVnode()
	#@nonl
	#@-node:__init__
	#@+node:color
	def color (self):
		
		c = self.c
		val = c.frame.tree.colorizer.colorize(self.temp_v,incremental=false)
		assert(val=="ok")
	#@nonl
	#@-node:color
	#@+node:setUp
	def setUp(self,*args,**keys):
	
		# trace(args,keys)
	
		# Initialize the text in the temp node.
		text = self.v.bodyString()
		self.c.selectVnode(self.temp_v)
		self.temp_v.t.setTnodeText(text,app.tkEncoding)
		self.c.frame.body.setSelectionAreas(None,text,None)
	#@nonl
	#@-node:setUp
	#@+node:tearDown
	def tearDown (self):
		
		self.temp_v.t.setTnodeText("",app.tkEncoding)
		self.c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@+node:runTest
	def runTest(self):
	
		self.color()
	#@nonl
	#@-node:runTest
	#@-others
#@nonl
#@-node:class colorTestCase
#@+node: makeEditBodySuite
def makeEditBodySuite(testParentHeadline,tempHeadline):
	
	"""Create a colorizer test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top() ; v = c.currentVnode()
	root = u.findRootNode(v)
	temp_v = u.findNodeInTree(root,tempHeadline)
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		v1 = v.firstChild()
		v2 = v1.next()
		test = editBodyTestCase(c,v,v1,v2,temp_v)
		suite.addTest(test)

	return suite
#@-node: makeEditBodySuite
#@+node:class editBodyTestCase
class editBodyTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's edit body commands."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,parent,v1,v2,temp_v):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.c = c
		self.parent = parent
		self.v1 = v1
		self.v2 = v2
		self.temp_v = temp_v
		
		self.old_v = c.currentVnode()
	#@nonl
	#@-node:__init__
	#@+node:editBody
	def editBody (self):
	
		# Compute the result in temp_v.bodyString()
		commandName = self.parent.headString()
		command = getattr(self.c,commandName)
		command()
		
		# Compare the computed result to the reference result.
		new_text = self.temp_v.bodyString()
		ref_text = self.v2.bodyString()
		if new_text != ref_text:
			print "test failed"
			trace("new",new_text)
			trace("ref",ref_text)
	
		assert(new_text == ref_text)
	#@nonl
	#@-node:editBody
	#@+node:setUp: TODO: set selection...
	def setUp(self,*args,**keys):
	
		# Initialize the text in the temp node.
		text = self.v1.bodyString()
		self.c.selectVnode(self.temp_v)
		self.temp_v.t.setTnodeText(text,app.tkEncoding)
		self.c.frame.body.setSelectionAreas(None,text,None)
	#@nonl
	#@-node:setUp: TODO: set selection...
	#@+node:tearDown
	def tearDown (self):
		
		self.temp_v.t.setTnodeText("",app.tkEncoding)
		self.c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@+node:runTest
	def runTest(self):
	
		self.editBody()
	#@nonl
	#@-node:runTest
	#@-others
#@nonl
#@-node:class editBodyTestCase
#@+node: makeOutlineSuite
def makeOutlineSuite(testParentHeadline):
	
	"""Create a colorizer test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top() ; v = c.currentVnode()
	
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		v1 = v.firstChild()
		v2 = v1.next()
		test = outlineTestCase(c,v,v1,v2,temp_v)
		suite.addTest(test)

	return suite
#@-node: makeOutlineSuite
#@+node:class outlineTestCase
class outlineTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's outline commands."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,parent,v1,v2,temp_v):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.c = c
		self.parent = parent
		self.v1 = v1
		self.v2 = v2
		self.temp_v = temp_v
		
		self.old_v = c.currentVnode()
	#@nonl
	#@-node:__init__
	#@+node:outlineCommand
	def outlineCommand (self):
	
		# Compute the result in temp_v.bodyString()
		commandName = self.parent.headString()
		command = getattr(self.c,commandName)
		command()
		
		# Compare the computed result to the reference result.
		u = testUtils()
		u.compareOutlines(self.v1,self.v2)
	#@-node:outlineCommand
	#@+node:runTest
	def runTest(self):
	
		self.outlineCommand()
	#@nonl
	#@-node:runTest
	#@+node:setUp
	def setUp(self,*args,**keys):
	
		pass
	#@nonl
	#@-node:setUp
	#@+node:tearDown
	def tearDown (self):
	
		self.undo()
		self.c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@+node:undo  TODO
	def undo (self):
		
		pass
	#@nonl
	#@-node:undo  TODO
	#@-others
#@nonl
#@-node:class outlineTestCase
#@+node: makeOutlineSuite
def makeTestLeoFilesSuite(testParentHeadline):
	
	"""Create a colorizer test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top()
	
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		test = leoFileTestCase(c,v.headString().strip())
		suite.addTest(test)

	return suite
#@-node: makeOutlineSuite
#@+node:class leoFileTestCase
class leoFileTestCase(unittest.TestCase):
	
	"""Data-driven unit tests to test .leo files."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,fileName):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.old_c = c
		self.c = None # set by setUp.
		self.fileName = fileName
		self.openFrames = app.windowList[:]
	#@nonl
	#@-node:__init__
	#@+node:runTest
	def runTest(self):
		
		"""Run the Check Outline command."""
	
		errors = self.c.checkOutline()
		assert(errors == 0)
	#@nonl
	#@-node:runTest
	#@+node:setUp
	def setUp(self):
	
		"""Open the .leo file."""
	
		c = self.old_c ; fileName = self.fileName
		assert(os_path_exists(fileName))
		ok, frame = openWithFileName(fileName,c)
		assert(ok)
		self.c = frame.c
	#@nonl
	#@-node:setUp
	#@+node:tearDown
	def tearDown (self):
	
		"""Close the .leo file if it was not already open."""
	
		frame = self.c.frame
		if frame not in self.openFrames:
			app.closeLeoWindow(frame)
	#@nonl
	#@-node:tearDown
	#@-others
#@nonl
#@-node:class leoFileTestCase
#@-others
#@nonl
#@-node:@file leoTest.py
#@-leo
