#@+leo-ver=4-thin
#@+node:ekr.20040303062846.2:@thin ../src/leoTest.py
"""

Unit tests for Leo.

Run the unit tests in test.leo using the Execute Script command.

"""

import leoGlobals as g
from leoGlobals import true,false

#@<< to do >>
#@+node:ekr.20040303062846.1:<< to do >>
#@+at
# 
# - Have log classes increment a count.
# 	Can be used to ensure that messages did or did not occcur.
# 
# - Have the nullGui create a nullUndoer by default
# 	But allow the possibility of leaving the full undoer in place.
#@-at
#@nonl
#@-node:ekr.20040303062846.1:<< to do >>
#@nl

import leoColor,leoCommands,leoFrame,leoGui,leoNodes,leoTkinterGui

import glob,os,sys,unittest

#@+others
#@+node:ekr.20040303062846.3: class testUtils
class testUtils:
	
	"""Common utility routines used by unit tests."""

	#@	@+others
	#@+node:ekr.20040303062846.4:compareOutlines
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
			g.trace(v1,v2)
		return ok
	#@nonl
	#@-node:ekr.20040303062846.4:compareOutlines
	#@+node:ekr.20040303062846.5:findChildrenOf & findSubnodesOf (revise)
	def findChildrenOf (self,headline):
		
		u = self ; c = g.top() ; v = c.currentVnode()
		root = u.findRootNode(v)
		parent = u.findNodeInTree(root,headline)
		v = parent.firstChild()
		vList = []
		while v:
			vList.append(v)
			v = v.next()
		return vList
	
	def findSubnodesOf (self,headline):
		
		u = self ; c = g.top() ; v = c.currentVnode()
		root = u.findRootNode(v)
		parent = u.findNodeInTree(root,headline)
		v = parent.firstChild()
		vList = []
		after = parent.nodeAfterTree()
		while v and v != after:
			vList.append(v)
			v = v.threadNext()
		return vList
	#@-node:ekr.20040303062846.5:findChildrenOf & findSubnodesOf (revise)
	#@+node:ekr.20040303062846.6:findNodeInRootTree, findNodeInTree, findNodeAnywhere
	def findRootNode (self,p):
	
		"""Return the root of v's tree."""
	
		while p and p.hasParent():
			p.moveToParent()
		return p
	
	def findNodeInTree(self,p,headline):
	
		"""Search for a node in v's tree matching the given headline."""
		
		c = p.c
		for p in p.subtree_iter():
			if p.headString().strip() == headline.strip():
				return p
		return c.nullPosition()
	
	def findNodeAnywhere(self,c,headline):
		
		for p in c.allNodes_iter():
			if p.headString().strip() == headline.strip():
				return p.copy()
		return c.nullPosition()
	#@nonl
	#@-node:ekr.20040303062846.6:findNodeInRootTree, findNodeInTree, findNodeAnywhere
	#@+node:ekr.20040303062846.7:numberOfNodesInOutline, numberOfClonesInOutline
	def numberOfNodesInOutline (self):
		
		"""Returns the total number of nodes in an outline"""
		
		c = g.top() ; n = 0
		for p in c.allNodes_iter():
			n += 1
		return n
		
	def numberOfClonesInOutline (self):
		
		"""Returns the number of cloned nodes in an outline"""
	
		c = g.top() ; n = 0
		for p in c.allNodes_iter():
			if v.isCloned():
				n += 1
		return n
	#@nonl
	#@-node:ekr.20040303062846.7:numberOfNodesInOutline, numberOfClonesInOutline
	#@+node:ekr.20040303062846.8:replaceOutline
	def replaceOutline (self,c,outline1,outline2):
		
		u = self
		
		"""Replace outline1 by a copy of outline 2 if not equal."""
		
		g.trace()
		
		copy = outline2.copyTreeWithNewTnodes()
		copy.linkAfter(outline1)
		outline1.doDelete(newVnode=copy)
	#@nonl
	#@-node:ekr.20040303062846.8:replaceOutline
	#@-others
#@nonl
#@-node:ekr.20040303062846.3: class testUtils
#@+node:ekr.20040303062846.10: fail
def fail ():
	
	"""Mark a unit test as having failed."""
	
	g.app.unitTestDict["fail"] = callerName(2)
#@nonl
#@-node:ekr.20040303062846.10: fail
#@+node:ekr.20040327115825:Batch mode tests
#@+node:ekr.20040327115832.1: makeBatchModeSuite
def makeBatchModeSuite (*args,**keys):
	
	"""Create a colorizer test for every descendant of testParentHeadline.."""
	
	return unittest.makeSuite(batchModeTestCase,'test')
#@nonl
#@-node:ekr.20040327115832.1: makeBatchModeSuite
#@+node:ekr.20040327115832.2:class batchModeTestCase
class batchModeTestCase(unittest.TestCase):
	
	"""unit tests for batch mode (--script)."""
	
	#@	@+others
	#@+node:ekr.20040327120228:test_1
	def test_1 (self):
	
		path = r"c:\prog\test\unittest\createdFile.txt"
		
		s = r"c:\python23\python c:\prog\LeoCVS\leo\src\leo.py -script c:\prog\test\unittest\batchTest.py"
		
		if os.path.exists(path):
			os.remove(path)
		
		os.system(s)
		
		assert(os.path.exists(path))
	#@nonl
	#@-node:ekr.20040327120228:test_1
	#@-others
#@nonl
#@-node:ekr.20040327115832.2:class batchModeTestCase
#@-node:ekr.20040327115825:Batch mode tests
#@+node:ekr.20040303062846.11:Colorizer tests
#@+node:ekr.20040303062846.12: makeColorSuite
def makeColorSuite(testParentHeadline,tempHeadline):
	
	"""Create a colorizer test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = g.top() ; v = c.currentVnode()
	root = u.findRootNode(v)
	temp_v = u.findNodeInTree(root,tempHeadline)
	vList = u.findSubnodesOf(testParentHeadline)
	
	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		test = colorTestCase(c,v,temp_v)
		suite.addTest(test)

	return suite
#@-node:ekr.20040303062846.12: makeColorSuite
#@+node:ekr.20040303062846.13:class colorTestCase
class colorTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's colorizer."""
	
	#@	@+others
	#@+node:ekr.20040303062846.14:__init__
	def __init__ (self,c,v,temp_v):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.c = c
		self.v = v
		self.temp_v = temp_v
		
		self.old_v = c.currentVnode()
	#@nonl
	#@-node:ekr.20040303062846.14:__init__
	#@+node:ekr.20040303062846.15:color
	def color (self):
		
		c = self.c
		val = c.frame.body.colorizer.colorize(self.temp_v,incremental=false)
		assert(val=="ok")
	#@nonl
	#@-node:ekr.20040303062846.15:color
	#@+node:ekr.20040303062846.16:setUp
	def setUp(self,*args,**keys):
	
		# g.trace(args,keys)
	
		# Initialize the text in the temp node.
		text = self.v.bodyString()
		self.c.selectVnode(self.temp_v)
		self.temp_v.setTnodeText(text,g.app.tkEncoding)
		self.c.frame.body.setSelectionAreas(None,text,None)
	#@nonl
	#@-node:ekr.20040303062846.16:setUp
	#@+node:ekr.20040303062846.17:tearDown
	def tearDown (self):
		
		self.temp_v.setTnodeText("",g.app.tkEncoding)
		self.c.selectVnode(self.old_v)
	#@nonl
	#@-node:ekr.20040303062846.17:tearDown
	#@+node:ekr.20040303062846.18:runTest
	def runTest(self):
	
		self.color()
	#@nonl
	#@-node:ekr.20040303062846.18:runTest
	#@-others
#@nonl
#@-node:ekr.20040303062846.13:class colorTestCase
#@-node:ekr.20040303062846.11:Colorizer tests
#@+node:ekr.20040303062846.19:Edit body tests
#@+node:ekr.20040303062846.20: makeEditBodySuite
def makeEditBodySuite(testParentHeadline,tempHeadline):
	
	"""Create an Edit Body test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = g.top() ; v = c.currentVnode()
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
#@-node:ekr.20040303062846.20: makeEditBodySuite
#@+node:ekr.20040303062846.21:class editBodyTestCase
class editBodyTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's edit body commands."""
	
	#@	@+others
	#@+node:ekr.20040303062846.22:__init__
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
	#@-node:ekr.20040303062846.22:__init__
	#@+node:ekr.20040303062846.23:editBody
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
			g.trace("new",new_text)
			g.trace("ref",ref_text)
			
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
				g.trace("new",new_text)
				g.trace("ref",ref_text)
			
			assert(new_text == ref_text)
			
			new_child = new_child.next()
			ref_child = ref_child.next()
	#@nonl
	#@-node:ekr.20040303062846.23:editBody
	#@+node:ekr.20040303062846.24:tearDown
	def tearDown (self):
		
		c = self.c ; temp_v = self.temp_v
		
		temp_v.setTnodeText("",g.app.tkEncoding)
		temp_v.clearDirty()
		
		if not self.wasChanged:
			c.setChanged (false)
			
		# Delete all children of temp node.
		while temp_v.firstChild():
			temp_v.firstChild().doDelete(temp_v)
	
		c.selectVnode(self.old_v)
	#@nonl
	#@-node:ekr.20040303062846.24:tearDown
	#@+node:ekr.20040303062846.25:setUp
	# Warning: this is Tk-specific code.
	
	def setUp(self,*args,**keys):
		
		c = self.c ; temp_v = self.temp_v
		
		# Delete all children of temp node.
		while temp_v.firstChild():
			temp_v.firstChild().doDelete(temp_v)
	
		text = self.before.bodyString()
		
		temp_v.setTnodeText(text,g.app.tkEncoding)
		c.selectVnode(self.temp_v)
		
		t = c.frame.body.bodyCtrl
		if self.sel:
			s = str(self.sel.bodyString()) # Can't be unicode.
			lines = s.split('\n')
			g.app.gui.setTextSelection(t,lines[0],lines[1])
	
		if self.ins:
			s = str(self.ins.bodyString()) # Can't be unicode.
			lines = s.split('\n')
			g.trace(lines)
			g.app.gui.setInsertPoint(t,lines[0])
			
		if not self.sel and not self.ins:
			g.app.gui.setInsertPoint(t,"1.0")
			g.app.gui.setTextSelection(t,"1.0","1.0")
	#@nonl
	#@-node:ekr.20040303062846.25:setUp
	#@+node:ekr.20040303062846.26:runTest
	def runTest(self):
	
		self.editBody()
	#@nonl
	#@-node:ekr.20040303062846.26:runTest
	#@-others
#@nonl
#@-node:ekr.20040303062846.21:class editBodyTestCase
#@-node:ekr.20040303062846.19:Edit body tests
#@+node:ekr.20040315202201:Find Command tests
#@+node:ekr.20040315202250: makeFindCommandSuite
def makeFindCommandSuite(arg=None,all=true,verbose=false):
	
	return unittest.makeSuite(findCommandTestCase,'test')
#@nonl
#@-node:ekr.20040315202250: makeFindCommandSuite
#@+node:ekr.20040315202314:class findCommandTestCase
class findCommandTestCase(unittest.TestCase):
	
	"""Unit tests for Leo's find commands."""
	
	#@	@+others
	#@+node:ekr.20040315202314.1:setUp
	def setUp(self,*args,**keys):
		
		import leoGlobals as g
		
		u = testUtils()
		
		self.c = c = g.top()
	
		self.verbose = true
		
		self.root = c.rootPosition()
		
		self.find_p = u.findNodeAnywhere(c,"findTests")
		
		assert(self.find_p)
		
		c.selectPosition(self.find_p)
	#@-node:ekr.20040315202314.1:setUp
	#@+node:ekr.20040315202347:testFindCommand
	def testFindCommand (self):
		
		g.trace(self.find_p)
	#@nonl
	#@-node:ekr.20040315202347:testFindCommand
	#@+node:ekr.20040315202718:testFindWordCommand
	def testFindWordCommand (self):
		
		pass
	#@nonl
	#@-node:ekr.20040315202718:testFindWordCommand
	#@+node:ekr.20040315202718.1:testFindIgnoreCaseCommand
	def testFindIgnoreCaseCommand (self):
		
		pass
	#@nonl
	#@-node:ekr.20040315202718.1:testFindIgnoreCaseCommand
	#@-others
#@nonl
#@-node:ekr.20040315202314:class findCommandTestCase
#@-node:ekr.20040315202201:Find Command tests
#@+node:ekr.20040303062846.27:Import/Export tests
#@+node:ekr.20040303062846.28:makeImportExportSuite
def makeImportExportSuite(testParentHeadline,tempHeadline):
	
	"""Create an Import/Export test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = g.top() ; v = c.currentVnode()
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
#@-node:ekr.20040303062846.28:makeImportExportSuite
#@+node:ekr.20040303062846.29:class importExportTestCase
class importExportTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's edit body commands."""
	
	#@	@+others
	#@+node:ekr.20040303062846.30:__init__
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
	
	#@-node:ekr.20040303062846.30:__init__
	#@+node:ekr.20040303062846.31:importExport
	def importExport (self):
		
		c = self.c ; v = self.v
		
		g.app.unitTestDict = {}
	
		commandName = v.headString()
		command = getattr(c,commandName) # Will fail if command does not exist.
		command()
	
		failedMethod = g.app.unitTestDict.get("fail")
		self.failIf(failedMethod,failedMethod)
	#@nonl
	#@-node:ekr.20040303062846.31:importExport
	#@+node:ekr.20040303062846.32:runTest
	def runTest(self):
		
		# """Import Export Test Case"""
	
		self.importExport()
	#@nonl
	#@-node:ekr.20040303062846.32:runTest
	#@+node:ekr.20040303062846.33:setUp
	def setUp(self,*args,**keys):
		
		c = self.c ; temp_v = self.temp_v ; d = self.dialog
		
		temp_v.setTnodeText('',g.app.tkEncoding)
	
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
	#@-node:ekr.20040303062846.33:setUp
	#@+node:ekr.20040303062846.34:shortDescription
	def shortDescription (self):
		
		try:
			return "ImportExportTestCase: %s %s" % (self.v.headString(),self.fileName)
		except:
			return "ImportExportTestCase"
	#@nonl
	#@-node:ekr.20040303062846.34:shortDescription
	#@+node:ekr.20040303062846.35:tearDown
	def tearDown (self):
		
		c = self.c ; temp_v = self.temp_v
		
		if self.gui:
			self.gui.destroySelf()
			self.gui = None
		
		temp_v.setTnodeText("",g.app.tkEncoding)
		temp_v.clearDirty()
		
		if not self.wasChanged:
			c.setChanged (false)
			
		if 1: # Delete all children of temp node.
			while temp_v.firstChild():
				temp_v.firstChild().doDelete(temp_v)
	
		c.selectVnode(self.old_v)
	#@nonl
	#@-node:ekr.20040303062846.35:tearDown
	#@-others
#@nonl
#@-node:ekr.20040303062846.29:class importExportTestCase
#@-node:ekr.20040303062846.27:Import/Export tests
#@+node:ekr.20040303062846.36:LeoFiles tests
#@+node:ekr.20040303062846.37:makeTestLeoFilesSuite
def makeTestLeoFilesSuite(testParentHeadline,unused=None):
	
	"""Create a .leo file test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = g.top()
	
	vList = u.findChildrenOf(testParentHeadline)

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	for v in vList:
		test = leoFileTestCase(c,v.headString().strip())
		suite.addTest(test)

	return suite

#@-node:ekr.20040303062846.37:makeTestLeoFilesSuite
#@+node:ekr.20040303062846.38:class leoFileTestCase
class leoFileTestCase(unittest.TestCase):
	
	"""Data-driven unit tests to test .leo files."""
	
	#@	@+others
	#@+node:ekr.20040303062846.39:__init__
	def __init__ (self,c,fileName):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.old_c = c
		self.c = None # set by setUp.
		self.fileName = fileName
		self.gui = None # set by setUp
		self.openFrames = g.app.windowList[:]
	#@nonl
	#@-node:ekr.20040303062846.39:__init__
	#@+node:ekr.20040303062846.40:runTest
	def runTest(self):
		
		"""Run the Check Outline command."""
	
		errors = self.c.checkOutline(verbose=false,unittest=true)
		assert(errors == 0)
	#@nonl
	#@-node:ekr.20040303062846.40:runTest
	#@+node:ekr.20040303062846.41:setUp
	def setUp(self):
	
		"""Open the .leo file."""
		
	
		c = self.old_c ; fileName = self.fileName
		assert(g.os_path_exists(fileName))
		
		self.oldGui = g.app.gui
		# g.app.gui = leoGui.nullGui("nullGui")
	
		ok, frame = g.openWithFileName(fileName,c,enableLog=false)
		assert(ok)
		self.c = frame.c
	#@nonl
	#@-node:ekr.20040303062846.41:setUp
	#@+node:ekr.20040303062846.42:tearDown
	def tearDown (self):
	
		"""Close the .leo file if it was not already open."""
	
		frame = self.c.frame
		if frame not in self.openFrames:
			g.app.closeLeoWindow(frame)
	
		g.app.gui = self.oldGui
	#@nonl
	#@-node:ekr.20040303062846.42:tearDown
	#@-others
#@nonl
#@-node:ekr.20040303062846.38:class leoFileTestCase
#@-node:ekr.20040303062846.36:LeoFiles tests
#@+node:ekr.20040303062846.63:Outline tests
#@+node:ekr.20040303062846.64: makeOutlineSuite
def makeOutlineSuite(testParentHeadline,unused=None):
	
	"""Create an outline test for every descendant of testParentHeadline.."""
	
	u = testUtils() ; c = g.top() ; v = c.currentVnode()
	
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
#@-node:ekr.20040303062846.64: makeOutlineSuite
#@+node:ekr.20040303062846.65:class outlineTestCase
class outlineTestCase(unittest.TestCase):
	
	"""Data-driven unit tests for Leo's outline commands."""
	
	#@	@+others
	#@+node:ekr.20040303062846.66:__init__
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
	#@-node:ekr.20040303062846.66:__init__
	#@+node:ekr.20040303062846.67:outlineCommand
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
	#@-node:ekr.20040303062846.67:outlineCommand
	#@+node:ekr.20040303062846.68:runTest
	def runTest(self):
	
		self.outlineCommand()
	#@nonl
	#@-node:ekr.20040303062846.68:runTest
	#@+node:ekr.20040303062846.69:setUp
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
	#@-node:ekr.20040303062846.69:setUp
	#@+node:ekr.20040303062846.70:tearDown
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
	#@-node:ekr.20040303062846.70:tearDown
	#@-others
#@nonl
#@-node:ekr.20040303062846.65:class outlineTestCase
#@-node:ekr.20040303062846.63:Outline tests
#@+node:ekr.20040303062846.72:Plugin tests
#@+node:ekr.20040303062846.71: makePluginsSuite
def makePluginsSuite(verbose=false,*args,**keys):
	
	"""Create an plugins test for every .py file in the plugins directory."""
	
	plugins_path = g.os_path_join(g.app.loadDir,"..","plugins")
	
	files = glob.glob(g.os_path_join(plugins_path,"*.py"))
	files = [g.os_path_abspath(file) for file in files]
	files.sort()

	# Create the suite and add all test cases.
	suite = unittest.makeSuite(unittest.TestCase)
	
	for file in files:
		test = pluginTestCase(file,verbose)
		suite.addTest(test)

	return suite
#@-node:ekr.20040303062846.71: makePluginsSuite
#@+node:ekr.20040303062846.73:class pluginTestCase
class pluginTestCase(unittest.TestCase):
	
	"""Unit tests for one Leo plugin."""
	
	#@	@+others
	#@+node:ekr.20040303062846.74:__init__
	def __init__ (self,fileName,verbose):
		
		# Init the base class.
		unittest.TestCase.__init__(self)
	
		self.fileName = fileName
		self.oldGui = None
		self.verbose = verbose
	#@nonl
	#@-node:ekr.20040303062846.74:__init__
	#@+node:ekr.20040303062846.75:pluginTest
	def pluginTest (self):
		
		# Duplicate the import logic in leoPlugins.py.
		
		fileName = g.toUnicode(self.fileName,g.app.tkEncoding)
		path = g.os_path_join(g.app.loadDir,"..","plugins")
		
		if self.verbose:
			g.trace(str(g.shortFileName(fileName)))
	
		module = g.importFromPath(fileName,path)
		assert(module)
		
		# Run any unit tests in the module itself.
		if hasattr(module,"unitTest"):
			
			if self.verbose:
				g.trace("Executing unitTest in %s..." % str(g.shortFileName(fileName)))
	
			module.unitTest()
	#@nonl
	#@-node:ekr.20040303062846.75:pluginTest
	#@+node:ekr.20040303062846.76:runTest
	def runTest(self):
	
		self.pluginTest()
	#@nonl
	#@-node:ekr.20040303062846.76:runTest
	#@+node:ekr.20040303062846.77:setUp
	def setUp(self,*args,**keys):
	
		self.oldGui = g.app.gui
		# g.app.gui = leoTkinterGui.tkinterGui()
	#@nonl
	#@-node:ekr.20040303062846.77:setUp
	#@+node:ekr.20040303062846.78:shortDescription
	def shortDescription (self):
		
		return "pluginTestCase: " + self.fileName
	#@nonl
	#@-node:ekr.20040303062846.78:shortDescription
	#@+node:ekr.20040303062846.79:tearDown
	def tearDown (self):
	
		g.app.gui = self.oldGui
	#@nonl
	#@-node:ekr.20040303062846.79:tearDown
	#@-others
#@nonl
#@-node:ekr.20040303062846.73:class pluginTestCase
#@-node:ekr.20040303062846.72:Plugin tests
#@+node:ekr.20040303063644:Position tests
#@+node:ekr.20040303064013: makePositionSuite
def makePositionSuite(arg=None,all=true,verbose=false):
	
	if all: # Include everything.
	
		suite = unittest.makeSuite(positionTestCase,'test')
		
	else: # Include listed testss.

		names = (
			"testFullTraverse",
			"testParentChildLinks",
			"testNextBack",
			"testVnodeList",
			"testThreadBackNext",
			"testParentChildLevel")
		
		suite = unittest.makeSuite(unittest.TestCase)
		for name in names:
			suite.addTest(positionTestCase(name))

	return suite
#@nonl
#@-node:ekr.20040303064013: makePositionSuite
#@+node:ekr.20040303063118:class positionTestCase
class positionTestCase(unittest.TestCase):
	
	"""Unit tests for Leo's position class."""
	
	#@	@+others
	#@+node:ekr.20040303063118.4:setUp
	def setUp(self,*args,**keys):
		
		import leoGlobals as g
		
		self.c = c = g.top()
	
		self.verbose = true
		
		self.root = c.rootPosition()
	#@nonl
	#@-node:ekr.20040303063118.4:setUp
	#@+node:ekr.20040309105731:testComparisons
	def testComparisons (self):
		
		p = self.root
		assert(p == p.copy())
		assert(p != p.threadNext())
	#@nonl
	#@-node:ekr.20040309105731:testComparisons
	#@+node:ekr.20040323163413:testThatClonesShareSubtrees
	def testThatClonesShareSubtrees (self):
		
		"""Test that cloned nodes actually share subtrees."""
	
		for p in self.root.allNodes_iter():
			if p.isCloned() and p.hasChildren():
				childv = p.firstChild().v
				assert(childv == p.v.t._firstChild)
				assert(id(childv) == id(p.v.t._firstChild))
				for v in p.v.t.vnodeList:
					assert(v.t._firstChild == childv)
					assert(id(v.t._firstChild) == id(childv))
	#@nonl
	#@-node:ekr.20040323163413:testThatClonesShareSubtrees
	#@+node:ekr.20040312101853:Consistency tests...
	#@+node:ekr.20040309101454.15:testConsistencyOfAllNodesThreadNext
	def testConsistencyOfAllNodesThreadNextWithCopy(self):
		self.doConsistencyOfAllNodesThreadNext(true)
		
	def testConsistencyOfAllNodesThreadNext(self):
		self.doConsistencyOfAllNodesThreadNext(false)
	
	def doConsistencyOfAllNodesThreadNext (self,copy):
		
		"""Test consistency of p.moveToThreadNext and p.allNodes_iter."""
	
		root = self.c.rootPosition()
		p2 = root.copy()
	
		for p in root.allNodes_iter(copy=copy):
	
			if p != p2: print p,p2
			assert(p==p2)
			p2.moveToThreadNext()
			
		if p2: print p2
		assert(not p2)
	#@-node:ekr.20040309101454.15:testConsistencyOfAllNodesThreadNext
	#@+node:ekr.20040309101454.17:testConsistencyOfFirstChildAndChildrenIter
	def testConsistencyOfFirstChildAndChildrenIterWithCopy(self):
		self.doConsistencyOfFirstChildAndChildrenIter(true)
		
	def testConsistencyOfFirstChildAndChildrenIter(self):
		self.doConsistencyOfFirstChildAndChildrenIter(false)
	
	def doConsistencyOfFirstChildAndChildrenIter (self,copy):
		
		"""Test consistency of p.moveToFirstChild/Next and p.children_iter."""
	
		root = self.c.rootPosition()
	
		for p in root.allNodes_iter(copy=copy):
			
			p2 = p.firstChild()
			for p3 in p.children_iter(copy=copy):
				
				if p3 != p2: print p3,p2
				assert(p3==p2)
				p2.moveToNext()
	
		if p2: print p2
		assert(not p2)
	#@nonl
	#@-node:ekr.20040309101454.17:testConsistencyOfFirstChildAndChildrenIter
	#@+node:ekr.20040309101454.13:testConsistencyOfLevel
	def testConsistencyOfLevel (self):
		
		"""Test consistency of p.level."""
	
		for p in self.root.allNodes_iter():
			
			if p.hasParent():
				assert(p.parent().level() == p.level() - 1)
		
			if p.hasChildren():
				assert(p.firstChild().level() == p.level() + 1)
				
			if p.hasNext():
				assert(p.next().level() == p.level())
		
			if p.hasBack():
				assert(p.back().level() == p.level())
	#@-node:ekr.20040309101454.13:testConsistencyOfLevel
	#@+node:ekr.20040303064020.5:testConsistencyOfNextBack
	def testConsistencyOfNextBack (self):
		
		"""Test consistency of p.next and p.back."""
	
		for p in self.root.allNodes_iter():
			
			back = p.back()
			next = p.next()
			if back: assert(back.getNext() == p)
			if next: assert(next.getBack() == p)
	#@nonl
	#@-node:ekr.20040303064020.5:testConsistencyOfNextBack
	#@+node:ekr.20040309101454.16:testConsistencyOfParentAndParentsIter
	def testConsistencyOfParentAndParentsIterWithCopy(self):
		self.doConsistencyOfParentAndParentsIter(true)
		
	def testConsistencyOfParentAndParentsIter(self):
		self.doConsistencyOfParentAndParentsIter(false)
	
	def doConsistencyOfParentAndParentsIter (self,copy):
		
		"""Test consistency of p.parent and p.parents_iter."""
	
		root = self.c.rootPosition()
	
		for p in root.allNodes_iter():
			
			p2 = p.parent()
			for p3 in p.parents_iter(copy=copy):
				
				if p3 != p2: print p3,p2
				assert(p3==p2)
				p2.moveToParent()
		
			if p2: print p2
			assert(not p2)
	#@nonl
	#@-node:ekr.20040309101454.16:testConsistencyOfParentAndParentsIter
	#@+node:ekr.20040309101454.14:testConsistencyOfParentChild
	def testConsistencyOfParentChild (self):
		
		"""Test consistency of p.parent, p.next, p.back and p.firstChild."""
		
		root = self.c.rootPosition()
	
		for p in root.allNodes_iter():
			
			if p.hasParent():
				n = p.childIndex()
				assert(p == p.parent().moveToNthChild(n))
				
			for child in p.children_iter():
				assert(p == child.parent())
		
			if p.hasNext():
				assert(p.next().parent() == p.parent())
				
			if p.hasBack():
				assert(p.back().parent() == p.parent())
	#@nonl
	#@-node:ekr.20040309101454.14:testConsistencyOfParentChild
	#@+node:ekr.20040303064020.7:testConsistencyOfThreadBackNext
	def testConsistencyOfThreadBackNext (self):
	
		for p in self.root.allNodes_iter():
	
			threadBack = p.threadBack()
			threadNext = p.threadNext()
	
			if threadBack:
				assert(p == threadBack.getThreadNext())
		
			if threadNext:
				assert(p == threadNext.getThreadBack())
	#@nonl
	#@-node:ekr.20040303064020.7:testConsistencyOfThreadBackNext
	#@+node:ekr.20040323163643:testConsistencyOfVnodeListAndParents
	def testConsistencyOfVnodeListAndParents (self):
	
		for p in self.root.allNodes_iter():
			if p.isCloned():
				parents = p.v.t.vnodeList
				for child in p.children_iter():
					vparents = child.v.directParents()
					assert(len(parents) == len(vparents))
					for parent in parents:
						assert(parent in vparents)
					for parent in vparents:
						assert(parent in parents)
	#@nonl
	#@-node:ekr.20040323163643:testConsistencyOfVnodeListAndParents
	#@+node:ekr.20040303091606:testHasNextBack
	def testHasNextBack (self):
		
		for p in self.root.allNodes_iter():
	
			back = p.back()
			next = p.next()
	
			assert(
				(back and p.hasBack()) or
				(not back and not p.hasBack()))
					
			assert(
				(next and p.hasNext()) or
				(not next and not p.hasNext()))
	#@nonl
	#@-node:ekr.20040303091606:testHasNextBack
	#@+node:ekr.20040303092153:testHasParentChild
	def testHasParentChild (self):
		
		for p in self.root.allNodes_iter():
	
			child = p.firstChild()
			parent = p.parent()
	
			assert(
				(child and p.hasFirstChild()) or
				(not child and not p.hasFirstChild()))
					
			assert(
				(parent and p.hasParent()) or
				(not parent and not p.hasParent()))
	#@nonl
	#@-node:ekr.20040303092153:testHasParentChild
	#@+node:ekr.20040303092153.1:testHasThreadNextBack
	def testHasThreadNextBack(self):
	
		for p in self.root.allNodes_iter():
	
			threadBack = p.getThreadBack()
			threadNext = p.getThreadNext()
	
			assert(
				(threadBack and p.hasThreadBack()) or
				(not threadBack and not p.hasThreadBack()))
					
			assert(
				(threadNext and p.hasThreadNext()) or
				(not threadNext and not p.hasThreadNext()))
	#@nonl
	#@-node:ekr.20040303092153.1:testHasThreadNextBack
	#@+node:ekr.20040303064020.6:testVnodeList
	def testVnodeList (self):
		
		for p in self.root.allNodes_iter():
	
			vnodeList = p.v.t.vnodeList
		
			for v in vnodeList:
	
				assert(v.t == p.v.t)
				if p.v.isCloned():
					assert(v.isCloned())
					assert(len(vnodeList) > 1)
				else:
					assert(not v.isCloned())
					assert(len(vnodeList) == 1)
	#@nonl
	#@-node:ekr.20040303064020.6:testVnodeList
	#@-node:ekr.20040312101853:Consistency tests...
	#@-others
#@nonl
#@-node:ekr.20040303063118:class positionTestCase
#@-node:ekr.20040303063644:Position tests
#@+node:ekr.20040303062846.80:Reformat Paragraph tests
# DTHEIN 2004.01.11: Added unit tests for reformatParagraph
#@nonl
#@+node:ekr.20040303062846.81:makeReformatParagraphSuite
# DTHEIN 2004.01.11: Added method
def makeReformatParagraphSuite(*args,**keys):
	
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
#@-node:ekr.20040303062846.81:makeReformatParagraphSuite
#@+node:ekr.20040303062846.82:class reformatParagraphTestCase
# DTHEIN 2004.01.11: Added class
class reformatParagraphTestCase(unittest.TestCase):
	
	"""Unit tests for Leo's reformat paragraph command."""
	
	#@	@+others
	#@+node:ekr.20040303062846.83:setUp
	# DTHEIN 2004.01.11: Added method
	def setUp(self):
	
		self.u = testUtils()
		self.c = g.top()
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
		
	
	
	#@-node:ekr.20040303062846.83:setUp
	#@+node:ekr.20040303062846.84:tearDown
	# DTHEIN 2004.01.11: Added method
	def tearDown(self):
		
		# local variables for class fields, for ease
		# of reading and ease of typeing.
		#	
		c = self.c ; temp_v = self.temp_v
		
		# clear the temp node and mark it unchanged
		#
		temp_v.setTnodeText("",g.app.tkEncoding)
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
	#@-node:ekr.20040303062846.84:tearDown
	#@+node:ekr.20040303062846.85:testNoTrailingNewline
	# DTHEIN 2004.01.11: Added method
	def testNoTrailingNewline(self):
		
		self.singleParagraphTest("testNoTrailingNewline",2,24)
	#@-node:ekr.20040303062846.85:testNoTrailingNewline
	#@+node:ekr.20040303062846.86:testTrailingNewline
	# DTHEIN 2004.01.11: Added method
	def testTrailingNewline(self):
		
		self.singleParagraphTest("testTrailingNewline",3,0)
	#@-node:ekr.20040303062846.86:testTrailingNewline
	#@+node:ekr.20040303062846.87:testMixedLineLengths
	# DTHEIN 2004.01.11: Added method
	def testMixedLineLengths(self):
		
		self.singleParagraphTest("testMixedLineLengths",4,10)
	#@-node:ekr.20040303062846.87:testMixedLineLengths
	#@+node:ekr.20040303062846.88:testMixedLinesWithLeadingWS
	# DTHEIN 2004.01.11: Added method
	def testMixedLinesWithLeadingWS(self):
		
		self.singleParagraphTest("testMixedLinesWithLeadingWS",4,12)
	#@-node:ekr.20040303062846.88:testMixedLinesWithLeadingWS
	#@+node:ekr.20040303062846.89:testNoChangeRequired
	# DTHEIN 2004.01.11: Added method
	def testNoChangeRequired(self):
		
		self.singleParagraphTest("testNoChangeRequired",1,28)
	#@-node:ekr.20040303062846.89:testNoChangeRequired
	#@+node:ekr.20040303062846.90:testHonorLeadingWS
	# DTHEIN 2004.01.11: Added method
	def testHonorLeadingWS(self):
		
		self.singleParagraphTest("testHonorLeadingWS",5,16)
	#@-node:ekr.20040303062846.90:testHonorLeadingWS
	#@+node:ekr.20040303062846.91:testHonorLeadingWSVar1
	# DTHEIN 2004.01.11: Added method
	def testHonorLeadingWSVar1(self):
		
		self.singleParagraphTest("testHonorLeadingWSVar1",5,16)
	#@-node:ekr.20040303062846.91:testHonorLeadingWSVar1
	#@+node:ekr.20040303062846.92:testSimpleHangingIndent
	# DTHEIN 2004.01.11: Added method
	def testSimpleHangingIndent(self):
		
		self.singleParagraphTest("testSimpleHangingIndent",5,8)
	#@-node:ekr.20040303062846.92:testSimpleHangingIndent
	#@+node:ekr.20040303062846.93:testSimpleHangingIndentVar1
	# DTHEIN 2004.01.11: Added method
	def testSimpleHangingIndentVar1(self):
		
		self.singleParagraphTest("testSimpleHangingIndentVar1",5,8)
	#@-node:ekr.20040303062846.93:testSimpleHangingIndentVar1
	#@+node:ekr.20040303062846.94:testSimpleHangingIndentVar2
	# DTHEIN 2004.01.11: Added method
	def testSimpleHangingIndentVar2(self):
		
		self.singleParagraphTest("testSimpleHangingIndentVar2",5,8)
	#@-node:ekr.20040303062846.94:testSimpleHangingIndentVar2
	#@+node:ekr.20040303062846.95:testMultiParagraph
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
	#@-node:ekr.20040303062846.95:testMultiParagraph
	#@+node:ekr.20040303062846.96:testMultiParagraphWithList
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
	#@-node:ekr.20040303062846.96:testMultiParagraphWithList
	#@+node:ekr.20040303062846.97:testDirectiveBreaksParagraph
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
	#@-node:ekr.20040303062846.97:testDirectiveBreaksParagraph
	#@+node:ekr.20040303062846.98:testWithLeadingWSOnEmptyLines
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
	#@-node:ekr.20040303062846.98:testWithLeadingWSOnEmptyLines
	#@+node:ekr.20040303062846.99:singleParagraphTest
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
	
	#@-node:ekr.20040303062846.99:singleParagraphTest
	#@+node:ekr.20040303062846.100:checkPosition
	# DTHEIN 2004.01.11: Added method
	def checkPosition(self,expRow,expCol):
	
		row,col = self.getRowCol()
		self.failUnlessEqual(expCol,col,
			"Current position is (" + str(row) + "," + str(col) 
			+ ");  expected cursor to be at column " + str(expCol) + ".")
		self.failUnlessEqual(expRow,row,
			"Current position is (" + str(row) + "," + str(col) 
			+ ");  expected cursor to be at line " + str(expRow) + ".")
	#@-node:ekr.20040303062846.100:checkPosition
	#@+node:ekr.20040303062846.101:checkText
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
	#@-node:ekr.20040303062846.101:checkText
	#@+node:ekr.20040303062846.102:copyBeforeToTemp
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
		temp_v.setTnodeText(text,g.app.tkEncoding)
		
		# create the child node that holds the text
		#
		t = leoNodes.tnode(headString="tempChildNode")
		self.tempChild_v = self.temp_v.insertAsNthChild(0,t)
	
		# copy the before text to the temp text
		#
		text = self.before_v.bodyString()
		self.tempChild_v.setTnodeText(text,g.app.tkEncoding)
		
		# make the temp child node current, and put the
		# cursor at the beginning
		#
		c.selectVnode(self.tempChild_v)
		c.frame.body.setInsertPointToStartOfLine( 0 )
		c.frame.body.setTextSelection(None,None)
		#g.app.gui.setInsertPoint(t,"1.0")
		#g.app.gui.setTextSelection(t,"1.0","1.0")
	#@-node:ekr.20040303062846.102:copyBeforeToTemp
	#@+node:ekr.20040303062846.103:getCaseDataNodes
	# DTHEIN 2004.01.11: Added method
	def getCaseDataNodes(self,caseNodeName):
	
		self.case_v = self.u.findNodeInTree(self.dataParent_v,caseNodeName)
		self.before_v = self.u.findNodeInTree(self.case_v,"before")
		self.after_v  = self.u.findNodeInTree(self.case_v,"after")
	#@-node:ekr.20040303062846.103:getCaseDataNodes
	#@+node:ekr.20040303062846.104:getRowCol
	# DTHEIN 2004.01.11: Added method
	def getRowCol(self):
		
		# local variables for class fields, for ease
		# of reading and ease of typeing.
		#	
		c = self.c ; body = c.frame.body.bodyCtrl ; gui = g.app.gui
		tab_width = c.frame.tab_width
	
		# Get the Tkinter row col position of the insert cursor
		#	
		index = body.index("insert")
		row,col = gui.getindex(body,index)
		
		# Adjust col position for tabs
		#
		if col > 0:
			s = body.get("%d.0" % (row),index)
			s = g.toUnicode(s,g.app.tkEncoding)
			col = g.computeWidth(s,tab_width)
	
		return (row,col)
	#@-node:ekr.20040303062846.104:getRowCol
	#@-others
#@nonl
#@-node:ekr.20040303062846.82:class reformatParagraphTestCase
#@-node:ekr.20040303062846.80:Reformat Paragraph tests
#@-others
#@-node:ekr.20040303062846.2:@thin ../src/leoTest.py
#@-leo
