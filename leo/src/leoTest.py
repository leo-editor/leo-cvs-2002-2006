#@+leo-ver=4
#@+node:@file leoTest.py
"""

Unit tests for Leo.

Run the unit tests in test.leo using the Execute Script command.

"""

from leoGlobals import *

import leoColor,leoCommands,leoFrame,leoGui,leoNodes,leoTkinterGui

import glob,os,sys,unittest

#@+others
#@+node: class testUtils
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
		v1 = v1.firstChild()
		v2 = v2.firstChild()
		ok = true
		while v2 and v1 != after1 and v2 != after2:
			ok = (
			v1.numberOfChildren() == v2.numberOfChildren() and
			v1.headString() == v2.headString() and
			v1.bodyString() == v2.bodyString() and
			v1.isCloned()   == v2.isCloned()   )
			if not ok: break
			v1 = v1.threadNext()
			v2 = v2.threadNext()
	
		ok = ok and v1 == after1 and v2 == after2
		if not ok:
			trace(v1,v2)
		return ok
	#@nonl
	#@-node:compareOutlines
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
	#@+node:replaceOutline
	def replaceOutline (self,c,outline1,outline2):
		
		u = self
		
		"""Replace outline1 by a copy of outline 2 if not equal."""
		
		trace()
		
		copy = outline2.copyTreeWithNewTnodes()
		copy.linkAfter(outline1)
		outline1.doDelete(newVnode=copy)
	#@-node:replaceOutline
	#@+node:validateOutline TODO
	def validateOutline (self,root):
		
		"""Checks an outline for consistency"""
		pass
	#@nonl
	#@-node:validateOutline TODO
	#@-others
#@nonl
#@-node: class testUtils
#@+node: fail
def fail ():
	
	"""Mark a unit test as having failed."""
	
	app.unitTestDict["fail"] = callerName(2)
#@nonl
#@-node: fail
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
		val = c.frame.body.colorizer.colorize(self.temp_v,incremental=false)
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
	
	"""Create an Edit Body test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top() ; v = c.currentVnode()
	root = u.findRootNode(v)
	temp_v = u.findNodeInTree(root,tempHeadline)
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		before = u.findNodeInTree(v,"before")
		after  = u.findNodeInTree(v,"after")
		sel    = u.findNodeInTree(v,"selection")
		ins    = u.findNodeInTree(v,"insert")
		if before and after:
			test = editBodyTestCase(c,v,before,after,sel,ins,temp_v)
			suite.addTest(test)
		else:
			print 'missing "before" or "after" for', v.headString()

	return suite
#@nonl
#@-node: makeEditBodySuite
#@+node:class editBodyTestCase
class editBodyTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's edit body commands."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,parent,before,after,sel,ins,temp_v):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.c = c
		self.parent = parent
		self.before = before
		self.after  = after
		self.sel    = sel # Two lines giving the selection range in tk coordinates.
		self.ins    = ins # One line giveing the insert point in tk coordinate.
		self.temp_v = temp_v
		
		self.old_v = c.currentVnode()
		
		self.wasChanged = c.changed
	#@nonl
	#@-node:__init__
	#@+node:editBody
	def editBody (self):
		
		c = self.c ; temp_v = self.temp_v ; after = self.after
	
		# Compute the result in temp_v.bodyString()
		commandName = self.parent.headString()
		command = getattr(c,commandName)
		command()
		
		# Compare the computed result to the reference result.
		new_text = temp_v.bodyString().rstrip()
		ref_text = after.bodyString().rstrip()
	
		if new_text != ref_text:
			print ; print "test failed", commandName
			trace("new",new_text)
			trace("ref",ref_text)
			
		assert(new_text == ref_text)
		
		# Compare subtrees.
		
		assert(temp_v.numberOfChildren() == after.numberOfChildren())
		
		ref_child = after.firstChild()
		new_child = temp_v.firstChild()
		
		while new_child:
			new_text = new_child.bodyString().rstrip()
			ref_text = ref_child.bodyString().rstrip()
	
			if new_text != ref_text:
				print ; print "test failed", commandName
				trace("new",new_text)
				trace("ref",ref_text)
			
			assert(new_text == ref_text)
			
			new_child = new_child.next()
			ref_child = ref_child.next()
	#@nonl
	#@-node:editBody
	#@+node:tearDown
	def tearDown (self):
		
		c = self.c ; temp_v = self.temp_v
		
		temp_v.t.setTnodeText("",app.tkEncoding)
		temp_v.clearDirty()
		
		if not self.wasChanged:
			c.setChanged (false)
			
		# Delete all children of temp node.
		while temp_v.firstChild():
			temp_v.firstChild().doDelete(temp_v)
	
		c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@+node:setUp
	# Warning: this is Tk-specific code.
	
	def setUp(self,*args,**keys):
		
		c = self.c ; temp_v = self.temp_v
		
		# Delete all children of temp node.
		while temp_v.firstChild():
			temp_v.firstChild().doDelete(temp_v)
	
		text = self.before.bodyString()
		
		temp_v.t.setTnodeText(text,app.tkEncoding)
		c.selectVnode(self.temp_v)
		
		t = c.frame.body.bodyCtrl
		if self.sel:
			s = self.sel.bodyString()
			lines = s.split('\n')
			app.gui.setTextSelection(t,lines[0],lines[1])
	
		if self.ins:
			s = self.ins.bodyString()
			lines = s.split('\n')
			app.gui.setInsertPoint(t,lines[0])
			
		if not self.sel and not self.ins:
			app.gui.setInsertPoint(t,"1.0")
			app.gui.setTextSelection(t,"1.0","1.0")
	#@-node:setUp
	#@+node:runTest
	def runTest(self):
	
		self.editBody()
	#@nonl
	#@-node:runTest
	#@-others
#@nonl
#@-node:class editBodyTestCase
#@+node:Reformat Paragraph tests
# DTHEIN 2004.01.11: Added unit tests for reformatParagraph
#@nonl
#@-node:Reformat Paragraph tests
#@+node:makeReformatParagraphSuite
# DTHEIN 2004.01.11: Added method
def makeReformatParagraphSuite():
	
	"""makeReformatParagraphSuite() -> suite
	
	Create a Reformat Paragraph test for each of the 
	unit tests in the reformatParagraphTestCase class."""
	
	suite = unittest.TestSuite()
	suite.addTest(reformatParagraphTestCase("testNoTrailingNewline"))
	suite.addTest(reformatParagraphTestCase("testTrailingNewline"))
	suite.addTest(reformatParagraphTestCase("testMixedLineLengths"))
	suite.addTest(reformatParagraphTestCase("testMixedLinesWithLeadingWS"))
	suite.addTest(reformatParagraphTestCase("testNoChangeRequired"))
	suite.addTest(reformatParagraphTestCase("testHonorLeadingWS"))
	suite.addTest(reformatParagraphTestCase("testHonorLeadingWSVar1"))
	suite.addTest(reformatParagraphTestCase("testSimpleHangingIndent"))
	suite.addTest(reformatParagraphTestCase("testSimpleHangingIndentVar1"))
	suite.addTest(reformatParagraphTestCase("testSimpleHangingIndentVar2"))
	suite.addTest(reformatParagraphTestCase("testMultiParagraph"))
	suite.addTest(reformatParagraphTestCase("testMultiParagraphWithList"))
	suite.addTest(reformatParagraphTestCase("testDirectiveBreaksParagraph"))
	suite.addTest(reformatParagraphTestCase("testWithLeadingWSOnEmptyLines"))
	return suite
	#	suite = reformatParagraphTestCase().suite();
	#return suite
#@nonl
#@-node:makeReformatParagraphSuite
#@+node:class reformatParagraphTestCase
# DTHEIN 2004.01.11: Added class
class reformatParagraphTestCase(unittest.TestCase):
	
	"""Unit tests for Leo's reformat paragraph command."""
	
	#@	@+others
	#@+node:setUp
	# DTHEIN 2004.01.11: Added method
	def setUp(self):
	
		self.u = testUtils()
		self.c = top()
		self.current_v = self.c.currentVnode()
		self.old_v = self.c.currentVnode()
		root = self.u.findRootNode(self.current_v)
		self.temp_v = self.u.findNodeInTree(root,"tempNode")
		self.tempChild_v = None
		self.dataParent_v = self.u.findNodeInTree(root,"reformatParagraphsTests")
		self.before_v = None
		self.after_v = None
		self.case_v = None
		self.wasChanged = self.c.changed
		
	
	#@-node:setUp
	#@+node:tearDown
	# DTHEIN 2004.01.11: Added method
	def tearDown(self):
		
		# local variables for class fields, for ease
		# of reading and ease of typeing.
		#	
		c = self.c ; temp_v = self.temp_v
		
		# clear the temp node and mark it unchanged
		#
		temp_v.t.setTnodeText("",app.tkEncoding)
		temp_v.clearDirty()
		
		if not self.wasChanged:
			c.setChanged (false)
			
		# Delete all children of temp node.
		#
		while temp_v.firstChild():
			temp_v.firstChild().doDelete(temp_v)
	
		# make the original node the current node
		#
		c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@+node:testNoTrailingNewline
	# DTHEIN 2004.01.11: Added method
	def testNoTrailingNewline(self):
		
		self.singleParagraphTest("testNoTrailingNewline",2,24)
	#@-node:testNoTrailingNewline
	#@+node:testTrailingNewline
	# DTHEIN 2004.01.11: Added method
	def testTrailingNewline(self):
		
		self.singleParagraphTest("testTrailingNewline",3,0)
	#@-node:testTrailingNewline
	#@+node:testMixedLineLengths
	# DTHEIN 2004.01.11: Added method
	def testMixedLineLengths(self):
		
		self.singleParagraphTest("testMixedLineLengths",4,10)
	#@-node:testMixedLineLengths
	#@+node:testMixedLinesWithLeadingWS
	# DTHEIN 2004.01.11: Added method
	def testMixedLinesWithLeadingWS(self):
		
		self.singleParagraphTest("testMixedLinesWithLeadingWS",4,12)
	#@-node:testMixedLinesWithLeadingWS
	#@+node:testNoChangeRequired
	# DTHEIN 2004.01.11: Added method
	def testNoChangeRequired(self):
		
		self.singleParagraphTest("testNoChangeRequired",1,28)
	#@-node:testNoChangeRequired
	#@+node:testHonorLeadingWS
	# DTHEIN 2004.01.11: Added method
	def testHonorLeadingWS(self):
		
		self.singleParagraphTest("testHonorLeadingWS",5,16)
	#@-node:testHonorLeadingWS
	#@+node:testHonorLeadingWSVar1
	# DTHEIN 2004.01.11: Added method
	def testHonorLeadingWSVar1(self):
		
		self.singleParagraphTest("testHonorLeadingWSVar1",5,16)
	#@-node:testHonorLeadingWSVar1
	#@+node:testSimpleHangingIndent
	# DTHEIN 2004.01.11: Added method
	def testSimpleHangingIndent(self):
		
		self.singleParagraphTest("testSimpleHangingIndent",5,8)
	#@-node:testSimpleHangingIndent
	#@+node:testSimpleHangingIndentVar1
	# DTHEIN 2004.01.11: Added method
	def testSimpleHangingIndentVar1(self):
		
		self.singleParagraphTest("testSimpleHangingIndentVar1",5,8)
	#@-node:testSimpleHangingIndentVar1
	#@+node:testSimpleHangingIndentVar2
	# DTHEIN 2004.01.11: Added method
	def testSimpleHangingIndentVar2(self):
		
		self.singleParagraphTest("testSimpleHangingIndentVar2",5,8)
	#@-node:testSimpleHangingIndentVar2
	#@+node:testMultiParagraph
	# DTHEIN 2004.01.11: Added method
	def testMultiParagraph(self):
		
		# Locate the test data
		#
		self.getCaseDataNodes("testMultiParagraph")
		
		# Setup the temp node
		#
		self.copyBeforeToTemp()
		
		# reformat the paragraph and check insertion cursor position
		#
		self.c.reformatParagraph()
		self.checkPosition(13,0)
		
		# Keep going, in the same manner
		#
		self.c.reformatParagraph()
		self.checkPosition(25,0)
		self.c.reformatParagraph()
		self.checkPosition(32,11)
		
		# Compare the computed result to the reference result.
		self.checkText()
	#@-node:testMultiParagraph
	#@+node:testMultiParagraphWithList
	# DTHEIN 2004.01.11: Added method
	def testMultiParagraphWithList(self):
		
		# Locate the test data
		#
		self.getCaseDataNodes("testMultiParagraphWithList")
		
		# Setup the temp node
		#
		self.copyBeforeToTemp()
		
		# reformat the paragraph and check insertion cursor position
		#
		self.c.reformatParagraph()
		self.checkPosition(4,0)
		
		# Keep going, in the same manner
		#
		self.c.reformatParagraph()
		self.checkPosition(7,0)
		self.c.reformatParagraph()
		self.checkPosition(10,0)
		self.c.reformatParagraph()
		self.checkPosition(13,0)
		self.c.reformatParagraph()
		self.checkPosition(14,18)
		
		# Compare the computed result to the reference result.
		self.checkText()
	#@-node:testMultiParagraphWithList
	#@+node:testDirectiveBreaksParagraph
	# DTHEIN 2004.01.11: Added method
	def testDirectiveBreaksParagraph(self):
		
		# Locate the test data
		#
		self.getCaseDataNodes("testDirectiveBreaksParagraph")
		
		# Setup the temp node
		#
		self.copyBeforeToTemp()
		
		# reformat the paragraph and check insertion cursor position
		#
		self.c.reformatParagraph()
		self.checkPosition(13,0) # at next paragraph
		
		# Keep going, in the same manner
		#
		self.c.reformatParagraph()
		self.checkPosition(25,0) # at next paragraph
	
		self.c.reformatParagraph()
		self.checkPosition(32,11)
		
		# Compare the computed result to the reference result.
		self.checkText()
	#@-node:testDirectiveBreaksParagraph
	#@+node:testWithLeadingWSOnEmptyLines
	# DTHEIN 2004.01.11: Added method
	def testWithLeadingWSOnEmptyLines(self):
		
		# Locate the test data
		#
		self.getCaseDataNodes("testWithLeadingWSOnEmptyLines")
		
		# Setup the temp node
		#
		self.copyBeforeToTemp()
		
		# reformat the paragraph and check insertion cursor position
		#
		self.c.reformatParagraph()
		self.checkPosition(4,0)
		
		# Keep going, in the same manner
		#
		self.c.reformatParagraph()
		self.checkPosition(7,0)
		self.c.reformatParagraph()
		self.checkPosition(10,0)
		self.c.reformatParagraph()
		self.checkPosition(13,0)
		self.c.reformatParagraph()
		self.checkPosition(14,18)
		
		# Compare the computed result to the reference result.
		self.checkText()
	#@-node:testWithLeadingWSOnEmptyLines
	#@+node:singleParagraphTest
	# DTHEIN 2004.01.11: Added method
	def singleParagraphTest(self,caseName,finalRow,finalCol):
		
		# Locate the test data
		#
		self.getCaseDataNodes(caseName)
		
		# Setup the temp node
		#
		self.copyBeforeToTemp()
		
		# reformat the paragraph
		#
		self.c.reformatParagraph()
		
		# Compare the computed result to the reference result.
		self.checkText()
		self.checkPosition(finalRow,finalCol)
	
	#@-node:singleParagraphTest
	#@+node:checkPosition
	# DTHEIN 2004.01.11: Added method
	def checkPosition(self,expRow,expCol):
	
		row,col = self.getRowCol()
		self.failUnlessEqual(expCol,col,
			"Current position is (" + str(row) + "," + str(col) 
			+ ");  expected cursor to be at column " + str(expCol) + ".")
		self.failUnlessEqual(expRow,row,
			"Current position is (" + str(row) + "," + str(col) 
			+ ");  expected cursor to be at line " + str(expRow) + ".")
	#@-node:checkPosition
	#@+node:checkText
	# DTHEIN 2004.01.11: Added method
	def checkText(self):
	
		new_text = self.tempChild_v.bodyString()
		ref_text = self.after_v.bodyString()
		newLines = new_text.splitlines(1)
		refLines = ref_text.splitlines(1)
		newLinesCount = len(newLines)
		refLinesCount = len(refLines)
		for i in range(min(newLinesCount,refLinesCount)):
			self.failUnlessEqual(newLines[i],refLines[i],
				"Mismatch on line " + str(i) + "."
				+ "\nExpected text: " + `refLines[i]`
				+ "\n  Actual text: "	+ `newLines[i]`)
		self.failUnlessEqual(newLinesCount,refLinesCount,
			"Expected " + str(refLinesCount) + " lines, but "
			+ "received " + str(newLinesCount) + " lines.")
	#@nonl
	#@-node:checkText
	#@+node:copyBeforeToTemp
	# DTHEIN 2004.01.11: Added method
	# Warning: this is Tk-specific code.
	#
	def copyBeforeToTemp(self):
	
		# local variables for class fields, for ease
		# of reading and ease of typeing.
		#	
		c = self.c ; temp_v = self.temp_v
	
		# Delete all children of temp node.
		#
		while temp_v.firstChild():
			temp_v.firstChild().doDelete(temp_v)
	
		# Copy the test case node text to the temp node
		#
		text = self.case_v.bodyString()
		temp_v.t.setTnodeText(text,app.tkEncoding)
		
		# create the child node that holds the text
		#
		t = leoNodes.tnode(headString="tempChildNode")
		self.tempChild_v = self.temp_v.insertAsNthChild(0,t)
	
		# copy the before text to the temp text
		#
		text = self.before_v.bodyString()
		self.tempChild_v.t.setTnodeText(text,app.tkEncoding)
		
		# make the temp child node current, and put the
		# cursor at the beginning
		#
		c.selectVnode(self.tempChild_v)
		c.frame.body.setInsertPointToStartOfLine( 0 )
		c.frame.body.setTextSelection(None,None)
		#app.gui.setInsertPoint(t,"1.0")
		#app.gui.setTextSelection(t,"1.0","1.0")
	#@-node:copyBeforeToTemp
	#@+node:getCaseDataNodes
	# DTHEIN 2004.01.11: Added method
	def getCaseDataNodes(self,caseNodeName):
	
		self.case_v = self.u.findNodeInTree(self.dataParent_v,caseNodeName)
		self.before_v = self.u.findNodeInTree(self.case_v,"before")
		self.after_v  = self.u.findNodeInTree(self.case_v,"after")
	#@-node:getCaseDataNodes
	#@+node:getRowCol
	# DTHEIN 2004.01.11: Added method
	def getRowCol(self):
		
		# local variables for class fields, for ease
		# of reading and ease of typeing.
		#	
		c = self.c ; body = c.frame.body.bodyCtrl ; gui = app.gui
		tab_width = c.frame.tab_width
	
		# Get the Tkinter row col position of the insert cursor
		#	
		index = body.index("insert")
		row,col = gui.getindex(body,index)
		
		# Adjust col position for tabs
		#
		if col > 0:
			s = body.get("%d.0" % (row),index)
			s = toUnicode(s,app.tkEncoding)
			col = computeWidth(s,tab_width)
	
		return (row,col)
	#@-node:getRowCol
	#@-others
#@nonl
#@-node:class reformatParagraphTestCase
#@+node:makeImportExportSuite
def makeImportExportSuite(testParentHeadline,tempHeadline):
	
	"""Create an Import/Export test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top() ; v = c.currentVnode()
	root = u.findRootNode(v)
	temp_v = u.findNodeInTree(root,tempHeadline)
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		dialog = u.findNodeInTree(v,"dialog")
		test = importExportTestCase(c,v,dialog,temp_v)
		suite.addTest(test)

	return suite
#@nonl
#@-node:makeImportExportSuite
#@+node:class importExportTestCase
class importExportTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's edit body commands."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,v,dialog,temp_v):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
		
		self.c = c
		self.dialog = dialog
		self.v = v
		self.temp_v = temp_v
		
		self.gui = None
		self.wasChanged = c.changed
		self.fileName = ""
	
		self.old_v = c.currentVnode()
	
	#@-node:__init__
	#@+node:importExport
	def importExport (self):
		
		c = self.c ; v = self.v
		
		app.unitTestDict = {}
	
		commandName = v.headString()
		command = getattr(c,commandName) # Will fail if command does not exist.
		command()
	
		failedMethod = app.unitTestDict.get("fail")
		self.failIf(failedMethod,failedMethod)
	#@nonl
	#@-node:importExport
	#@+node:runTest
	def runTest(self):
		
		# """Import Export Test Case"""
	
		self.importExport()
	#@nonl
	#@-node:runTest
	#@+node:setUp
	def setUp(self,*args,**keys):
		
		c = self.c ; temp_v = self.temp_v ; d = self.dialog
		
		temp_v.t.setTnodeText('',app.tkEncoding)
	
		# Create a node under temp_v.
		child = temp_v.insertAsLastChild()
		assert(child)
		child.setHeadString("import test: " + self.v.headString())
		c.selectVnode(child)
	
		assert(d)
		s = d.bodyString()
		lines = s.split('\n')
		name = lines[0]
		val = lines[1]
		self.fileName = val
		dict = {name: val}
		self.gui = leoGui.unitTestGui(dict,trace=false)
		
		
	#@nonl
	#@-node:setUp
	#@+node:shortDescription
	def shortDescription (self):
		
		try:
			return "ImportExportTestCase: %s %s" % (self.v.headString(),self.fileName)
		except:
			return "ImportExportTestCase"
	#@nonl
	#@-node:shortDescription
	#@+node:tearDown
	def tearDown (self):
		
		c = self.c ; temp_v = self.temp_v
		
		if self.gui:
			self.gui.destroySelf()
			self.gui = None
		
		temp_v.t.setTnodeText("",app.tkEncoding)
		temp_v.clearDirty()
		
		if not self.wasChanged:
			c.setChanged (false)
			
		if 1: # Delete all children of temp node.
			while temp_v.firstChild():
				temp_v.firstChild().doDelete(temp_v)
	
		c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@-others
#@nonl
#@-node:class importExportTestCase
#@+node:makeTestLeoFilesSuite
def makeTestLeoFilesSuite(testParentHeadline,unused=None):
	
	"""Create a .leo file test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top()
	
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		test = leoFileTestCase(c,v.headString().strip())
		suite.addTest(test)

	return suite
#@-node:makeTestLeoFilesSuite
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
		self.gui = None # set by setUp
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
		
		self.oldGui = app.gui
		# app.gui = leoGui.nullGui("nullGui")
	
		ok, frame = openWithFileName(fileName,c,enableLog=false)
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
	
		app.gui = self.oldGui
	#@nonl
	#@-node:tearDown
	#@-others
#@nonl
#@-node:class leoFileTestCase
#@+node: makeOutlineSuite
def makeOutlineSuite(testParentHeadline,unused=None):
	
	"""Create an outline test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = top() ; v = c.currentVnode()
	
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		before = u.findNodeInTree(v,"before")
		after  = u.findNodeInTree(v,"after")
		ref    = u.findNodeInTree(v,"ref")
		if before and after and ref:
			test = outlineTestCase(c,v,before,after,ref)
			suite.addTest(test)

	return suite
#@-node: makeOutlineSuite
#@+node:class outlineTestCase
class outlineTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's outline commands."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c,parent,before,after,ref):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.c = c
		self.parent = parent
		self.before = before
		self.after = after
		self.ref    = ref
		
		self.old_v = c.currentVnode()
		
		self.u = testUtils()
	#@nonl
	#@-node:__init__
	#@+node:outlineCommand
	def outlineCommand (self):
		
		c = self.c ; u = self.u ; tree = c.frame.tree
		
		move = u.findNodeInTree(self.before,"move")
		assert(move)
		
		c.selectVnode(move)
		
		commandName = self.parent.headString()
		command = getattr(c,commandName)
		command()
	
		assert(u.compareOutlines(self.before,self.after))
		c.undoer.undo()
		assert(u.compareOutlines(self.before,self.ref))
		c.undoer.redo()
		assert(u.compareOutlines(self.before,self.after))
		c.undoer.undo()
		assert(u.compareOutlines(self.before,self.ref))
	#@nonl
	#@-node:outlineCommand
	#@+node:runTest
	def runTest(self):
	
		self.outlineCommand()
	#@nonl
	#@-node:runTest
	#@+node:setUp
	def setUp(self,*args,**keys):
	
		assert(self.before)
		assert(self.after)
		assert(self.ref)
		assert(self.u.compareOutlines(self.before,self.ref))
		
		# Batch mode bugs: meaning of move may depend on visibility.
		self.parent.parent().expand()
		self.parent.expand()
		self.before.expand()
		self.after.expand()
	#@nonl
	#@-node:setUp
	#@+node:tearDown
	def tearDown (self):
	
		c = self.c ; u = self.u
	
		if not u.compareOutlines(self.before,self.ref):
			u.replaceOutline(c,self.before,self.ref)
	
		self.before.contract()
		self.after.contract()
		self.parent.contract()
		self.parent.parent().contract()
	
		self.c.selectVnode(self.old_v)
	#@nonl
	#@-node:tearDown
	#@+node: makePluginsSuite
	def makePluginsSuite(verbose=false,*args,**keys):
		
		"""Create an plugins test for every .py file in the plugins directory."""
		
		plugins_path = os_path_join(app.loadDir,"..","plugins")
		
		files = glob.glob(os_path_join(plugins_path,"*.py"))
		files = [os_path_abspath(file) for file in files]
		files.sort()
	
		# Create the suite and add all test cases.
		suite = unittest.makeSuite(unittest.TestCase)
		
		for file in files:
			test = pluginTestCase(file,verbose)
			suite.addTest(test)
	
		return suite
	#@-node: makePluginsSuite
	#@+node:class pluginTestCase
	class pluginTestCase(unittest.TestCase):
		
		"""Unit tests for one Leo plugin."""
		
		#@	@+others
		#@-others
	#@nonl
	#@-node:class pluginTestCase
	#@+node:__init__
	def __init__ (self,fileName,verbose):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.fileName = fileName
		self.oldGui = None
		self.verbose = verbose
	#@nonl
	#@-node:__init__
	#@+node:pluginTest
	def pluginTest (self):
		
		# Duplicate the import logic in leoPlugins.py.
		
		fileName = toUnicode(self.fileName,app.tkEncoding)
		path = os_path_join(app.loadDir,"..","plugins")
		
		if self.verbose:
			trace(str(shortFileName(fileName)))
	
		module = importFromPath(fileName,path)
		assert(module)
		
		# Run any unit tests in the module itself.
		if hasattr(module,"unitTest"):
			
			if self.verbose:
				trace("Executing unitTest in %s..." % str(shortFileName(fileName)))
	
			module.unitTest()
	#@nonl
	#@-node:pluginTest
	#@+node:runTest
	def runTest(self):
	
		self.pluginTest()
	#@nonl
	#@-node:runTest
	#@+node:setUp
	def setUp(self,*args,**keys):
	
		self.oldGui = app.gui
		# app.gui = leoTkinterGui.tkinterGui()
	#@nonl
	#@-node:setUp
	#@+node:shortDescription
	def shortDescription (self):
		
		return "pluginTestCase: " + self.fileName
	#@nonl
	#@-node:shortDescription
	#@+node:tearDown
	def tearDown (self):
	
		app.gui = self.oldGui
	#@nonl
	#@-node:tearDown
	#@-others
#@nonl
#@-node:class outlineTestCase
#@-others
#@nonl
#@-node:@file leoTest.py
#@-leo
