#@+leo-ver=4
#@+node:@file leoTest.py
"""

Unit tests for Leo.

Run the unit tests in test.leo using the Execute Script command.

"""

from leoGlobals import *

import leoColor,leoCommands,leoFrame,leoGui,leoNodes

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
		app.gui = leoGui.nullGui("nullGui")
	
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
	#@-others
#@nonl
#@-node:class outlineTestCase
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
	#@+node:__init__
	def __init__ (self,fileName,verbose):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.fileName = fileName
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
	
		pass
	#@nonl
	#@-node:setUp
	#@+node:shortDescription
	def shortDescription (self):
		
		return "pluginTestCase: " + self.fileName
	#@nonl
	#@-node:shortDescription
	#@+node:tearDown
	def tearDown (self):
	
		pass
	#@nonl
	#@-node:tearDown
	#@-others
#@nonl
#@-node:class pluginTestCase
#@-others
#@nonl
#@-node:@file leoTest.py
#@-leo
