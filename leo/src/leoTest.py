#@+leo-ver=4-thin
#@+node:EKR.20040623200709:@thin ../src/leoTest.py
"""

Classes used for Leo's unit testing.

Run the unit tests in test.leo using the Execute Script command.

"""

#@@language python
#@@tabwidth -4

#@<< leoTest imports >>
#@+node:EKR.20040623200709.2:<< leoTest imports >>

import leoGlobals as g

import leoColor
import leoCommands
import leoFrame
import leoGui
import leoNodes
import leoTkinterGui

import glob
import os
import sys
import unittest
#@nonl
#@-node:EKR.20040623200709.2:<< leoTest imports >>
#@nl

#@+others
#@+node:EKR.20040623223148: class testUtils
class testUtils:
    
    """Common utility routines used by unit tests."""

    #@    @+others
    #@+node:EKR.20040623223148.1:compareOutlines
    def compareOutlines (self,root1,root2):
        
        """Compares two outlines, making sure that their topologies,
        content and join lists are equivent"""
        
        v1,v2 = root1,root2
        after1 = v1.nodeAfterTree()
        after2 = v2.nodeAfterTree()
        v1 = v1.firstChild()
        v2 = v2.firstChild()
        ok = True
        while v2 and v1 != after1 and v2 != after2:
            ok = (
                v1.numberOfChildren() == v2.numberOfChildren() and
                v1.headString() == v2.headString() and
                v1.bodyString() == v2.bodyString() and
                v1.isCloned()   == v2.isCloned()
            )
            if not ok: break
            v1 = v1.threadNext()
            v2 = v2.threadNext()
    
        ok = ok and ((not v1 and not v2) or (v1 == after1 and v2 == after2))
        if not ok:
            g.trace(v1,v2)
        return ok
    #@nonl
    #@-node:EKR.20040623223148.1:compareOutlines
    #@+node:EKR.20040623223148.2:Finding nodes...
    #@+node:EKR.20040623223148.3:fundChildrenOf
    def findChildrenOf (self,headline):
        
        u = self ; c = g.top() ; v = c.currentPosition()
        
        root = u.findRootNode(v)
        parent = u.findNodeInTree(root,headline)
        
        v = parent.firstChild()
        vList = []
        while v:
            vList.append(v)
            v = v.next()
        return vList
    #@nonl
    #@-node:EKR.20040623223148.3:fundChildrenOf
    #@+node:EKR.20040623223148.4:findSubnodesOf TO DO: Replace this
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
    #@nonl
    #@-node:EKR.20040623223148.4:findSubnodesOf TO DO: Replace this
    #@+node:EKR.20040623223148.5:findNodeInRootTree
    def findRootNode (self,p):
    
        """Return the root of p's tree."""
    
        while p and p.hasParent():
            p.moveToParent()
        return p
    #@nonl
    #@-node:EKR.20040623223148.5:findNodeInRootTree
    #@+node:EKR.20040623223148.6:findNodeInTree
    def findNodeInTree(self,p,headline):
    
        """Search for a node in p's tree matching the given headline."""
        
        c = p.c
        for p in p.subtree_iter():
            if p.headString().strip().lower() == headline.strip().lower():
                return p
        return c.nullPosition()
    #@nonl
    #@-node:EKR.20040623223148.6:findNodeInTree
    #@+node:EKR.20040623223148.7:findNodeAnywhere
    def findNodeAnywhere(self,c,headline):
        
        for p in c.allNodes_iter():
            if p.headString().strip() == headline.strip():
                return p.copy()
        return c.nullPosition()
    #@nonl
    #@-node:EKR.20040623223148.7:findNodeAnywhere
    #@+node:EKR.20040623223148.8:findUnitTestNode
    def findUnitTestNode (self,unitTestName):
        
        c = g.top() ; root = c.rootPosition()
        
        for p in root.self_and_siblings_iter():
            h = p.headString().lower()
            if g.match(h,0,"unit testing"):
                break
    
        if p:
            for p in p.children_iter():
                h = p.headString()
                if g.match(h,0,"Unit test scripts"):
                    break
                    
        if p:
            for p in p.children_iter():
                h = p.headString()
                if g.match(h,0,unitTestName):
                    return p
    
        return c.nullPosition()
    #@nonl
    #@-node:EKR.20040623223148.8:findUnitTestNode
    #@-node:EKR.20040623223148.2:Finding nodes...
    #@+node:EKR.20040623223148.9:numberOfClonesInOutline
    def numberOfClonesInOutline (self):
        
        """Returns the number of cloned nodes in an outline"""
    
        c = g.top() ; n = 0
        for p in c.allNodes_iter():
            if v.isCloned():
                n += 1
        return n
    #@nonl
    #@-node:EKR.20040623223148.9:numberOfClonesInOutline
    #@+node:EKR.20040623223148.10:numberOfNodesInOutline
    def numberOfNodesInOutline (self):
        
        """Returns the total number of nodes in an outline"""
        
        c = g.top() ; n = 0
        for p in c.allNodes_iter():
            n += 1
        return n
        
    #@-node:EKR.20040623223148.10:numberOfNodesInOutline
    #@+node:EKR.20040623223148.11:replaceOutline
    def replaceOutline (self,c,outline1,outline2):
        
        u = self
        
        """Replace outline1 by a copy of outline 2 if not equal."""
        
        g.trace()
        
        copy = outline2.copyTreeWithNewTnodes()
        copy.linkAfter(outline1)
        outline1.doDelete(newVnode=copy)
    #@nonl
    #@-node:EKR.20040623223148.11:replaceOutline
    #@-others
#@nonl
#@-node:EKR.20040623223148: class testUtils
#@+node:EKR.20040623200709.15: fail
def fail ():
    
    """Mark a unit test as having failed."""
    
    g.app.unitTestDict["fail"] = g.callerName(2)
#@nonl
#@-node:EKR.20040623200709.15: fail
#@+node:EKR.20040624113742:atFileTests
#@+node:EKR.20040624113742.1:makeAtFileSuite
def makeAtFileSuite(nodeName,*ignored):
    
    c = g.top()
    u = testUtils()
    p = u.findUnitTestNode(nodeName)
    p.c.selectVnode(p)

    # Create the suite and add all test cases.
    suite = unittest.makeSuite(unittest.TestCase)

    for child in p.children_iter():
        
        h = child.headString().strip()
        if g.match(h,0,"test"):
            output = u.findNodeInTree(child,"output")
            for child2 in child.children_iter():
                h2 = child2.headString().strip()
                if g.match(h2,0,"@@"):
                    test = atFileTests(
                        c=c,
                        root=child2.copy(),
                        expected=output.bodyString())
                    suite.addTest(test)
                    
    return suite
#@-node:EKR.20040624113742.1:makeAtFileSuite
#@+node:EKR.20040623200709.18:class atFileTests
# TO DO: create script to create expected output

class atFileTests(unittest.TestCase):
    
    """Data-driven unit tests to test .leo files."""
    
    #@    @+others
    #@+node:EKR.20040624105213:__init__
    def __init__ (self,c=None,root=None,expected=None):
        
        # Init the base class.
        unittest.TestCase.__init__(self)
        
        self.c = c
        self.root = root
        self.expected = expected
    #@nonl
    #@-node:EKR.20040624105213:__init__
    #@+node:EKR.20040623200709.21:runTest
    def runTest(self):
        
        """Run a test of @file, @thin, etc."""
        
        c = self.c ; at = c.atFileCommands
        root = self.root
        input = root.bodyString()
        expected = self.expected
    
        # Compute the type from root's headline.
        h = root.headString()
        assert(g.match(h,0,"@@"))
        j = g.skip_c_id(h,2)
        type = h[1:j]
        assert type in ("@file","@thin","@nosent","@noref","@asis"), "bad type: %s" % type
    
        thinFile = type == "@thin"
        nosentinels = type in ("@asis","@nosent")
        
        if type == "@asis":
            assert 0, "asis not ready yet"
            pass # Not ready yet.
            at.asisWrite(p,toString=toString)
            result = "asis tests not ready yet"
        else:
            at.write(root,thinFile=thinFile,nosentinels=nosentinels,toString=True)
            result = g.toUnicode(at.new_df.stringOutput,"ascii")
        
        if result != expected:
            print ; print '-' * 20
            print "result..."
            for line in g.splitLines(result):
                print "%3d" % len(line),repr(line)
            print '-' * 20
            print "expected..."
            for line in g.splitLines(expected):
                print "%3d" % len(line),repr(line)
            print '-' * 20
    
        self.assertEqual(result,expected)
    #@nonl
    #@-node:EKR.20040623200709.21:runTest
    #@-others
#@nonl
#@-node:EKR.20040623200709.18:class atFileTests
#@-node:EKR.20040624113742:atFileTests
#@+node:EKR.20040623200709.23:Batch mode tests
#@+node:EKR.20040623200709.24: makeBatchModeSuite
def makeBatchModeSuite (*args,**keys):
    
    """Create a colorizer test for every descendant of testParentHeadline.."""
    
    return unittest.makeSuite(batchModeTestCase,'test')
#@nonl
#@-node:EKR.20040623200709.24: makeBatchModeSuite
#@+node:EKR.20040623200709.25:class batchModeTestCase
class batchModeTestCase(unittest.TestCase):
    
    """unit tests for batch mode (--script)."""
    
    #@    @+others
    #@+node:EKR.20040623200709.26:test_1
    def test_1 (self):
    
        path = r"c:\prog\test\unittest\createdFile.txt"
        
        s = r"c:\python23\python c:\prog\LeoCVS\leo\src\leo.py -script c:\prog\test\unittest\batchTest.py"
        
        if os.path.exists(path):
            os.remove(path)
        
        os.system(s)
        
        assert(os.path.exists(path))
    #@nonl
    #@-node:EKR.20040623200709.26:test_1
    #@-others
#@nonl
#@-node:EKR.20040623200709.25:class batchModeTestCase
#@-node:EKR.20040623200709.23:Batch mode tests
#@+node:EKR.20040623200709.27:Colorizer tests
#@+node:EKR.20040623200709.28: makeColorSuite
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
#@-node:EKR.20040623200709.28: makeColorSuite
#@+node:EKR.20040623200709.29:class colorTestCase
class colorTestCase(unittest.TestCase):
    
    """Data-driven unit tests for Leo's colorizer."""
    
    #@    @+others
    #@+node:EKR.20040623200709.30:__init__
    def __init__ (self,c,v,temp_v):
        
        # Init the base class.
        unittest.TestCase.__init__(self)
    
        self.c = c
        self.v = v
        self.temp_v = temp_v
        
        self.old_v = c.currentVnode()
    #@nonl
    #@-node:EKR.20040623200709.30:__init__
    #@+node:EKR.20040623200709.31:color
    def color (self):
        
        c = self.c
        val = c.frame.body.colorizer.colorize(self.temp_v,incremental=False)
        assert(val=="ok")
    #@nonl
    #@-node:EKR.20040623200709.31:color
    #@+node:EKR.20040623200709.32:setUp
    def setUp(self,*args,**keys):
    
        # g.trace(args,keys)
    
        # Initialize the text in the temp node.
        text = self.v.bodyString()
        self.c.selectVnode(self.temp_v)
        self.temp_v.setTnodeText(text,g.app.tkEncoding)
        self.c.frame.body.setSelectionAreas(None,text,None)
    #@nonl
    #@-node:EKR.20040623200709.32:setUp
    #@+node:EKR.20040623200709.33:tearDown
    def tearDown (self):
        
        self.temp_v.setTnodeText("",g.app.tkEncoding)
        self.c.selectVnode(self.old_v)
    #@nonl
    #@-node:EKR.20040623200709.33:tearDown
    #@+node:EKR.20040623200709.34:runTest
    def runTest(self):
    
        self.color()
    #@nonl
    #@-node:EKR.20040623200709.34:runTest
    #@-others
#@nonl
#@-node:EKR.20040623200709.29:class colorTestCase
#@-node:EKR.20040623200709.27:Colorizer tests
#@+node:EKR.20040623200709.35:Edit body tests
#@+node:EKR.20040623200709.36: makeEditBodySuite
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
#@-node:EKR.20040623200709.36: makeEditBodySuite
#@+node:EKR.20040623200709.37:class editBodyTestCase
class editBodyTestCase(unittest.TestCase):
    
    """Data-driven unit tests for Leo's edit body commands."""
    
    #@    @+others
    #@+node:EKR.20040623200709.38:__init__
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
        
        self.u = testUtils()
    #@nonl
    #@-node:EKR.20040623200709.38:__init__
    #@+node:EKR.20040623200709.39:editBody
    def editBody (self):
        
        c = self.c ; u = self.u
    
        # Compute the result in temp_v.bodyString()
        commandName = self.parent.headString()
        command = getattr(c,commandName)
        command()
        
        if 1:
            assert(u.compareOutlines(self.temp_v,self.after))
            c.undoer.undo()
            assert(u.compareOutlines(self.temp_v,self.before))
            c.undoer.redo()
            assert(u.compareOutlines(self.temp_v,self.after))
            c.undoer.undo()
            assert(u.compareOutlines(self.temp_v,self.before))
        else:
            #@        << compare new, ref trees >>
            #@+node:EKR.20040623200709.40:<< compare new, ref trees >>
            temp_v = self.temp_v ; after = self.after
            
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
            #@-node:EKR.20040623200709.40:<< compare new, ref trees >>
            #@nl
    #@nonl
    #@-node:EKR.20040623200709.39:editBody
    #@+node:EKR.20040623200709.41:tearDown
    def tearDown (self):
        
        c = self.c ; temp_v = self.temp_v
        
        temp_v.setTnodeText("",g.app.tkEncoding)
        temp_v.clearDirty()
        
        if not self.wasChanged:
            c.setChanged (False)
            
        # Delete all children of temp node.
        while temp_v.firstChild():
            temp_v.firstChild().doDelete(temp_v)
    
        c.selectVnode(self.old_v)
    #@nonl
    #@-node:EKR.20040623200709.41:tearDown
    #@+node:EKR.20040623200709.42:setUp
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
    #@-node:EKR.20040623200709.42:setUp
    #@+node:EKR.20040623200709.43:runTest
    def runTest(self):
    
        self.editBody()
    #@nonl
    #@-node:EKR.20040623200709.43:runTest
    #@-others
#@nonl
#@-node:EKR.20040623200709.37:class editBodyTestCase
#@-node:EKR.20040623200709.35:Edit body tests
#@+node:EKR.20040623200709.44:Find Command tests
#@+node:EKR.20040623200709.45: makeFindCommandSuite
def makeFindCommandSuite(arg=None,all=True,verbose=False):
    
    return unittest.makeSuite(findCommandTestCase,'test')
#@nonl
#@-node:EKR.20040623200709.45: makeFindCommandSuite
#@+node:EKR.20040623200709.46:class findCommandTestCase
class findCommandTestCase(unittest.TestCase):
    
    """Unit tests for Leo's find commands."""
    
    #@    @+others
    #@+node:EKR.20040623200709.47:setUp
    def setUp(self,*args,**keys):
        
        import leoGlobals as g
        
        u = testUtils()
        
        self.c = c = g.top()
    
        self.verbose = True
        
        self.root = c.rootPosition()
        
        self.find_p = u.findNodeAnywhere(c,"findTests")
        
        assert(self.find_p)
        
        c.selectPosition(self.find_p)
    #@-node:EKR.20040623200709.47:setUp
    #@+node:EKR.20040623200709.48:testFindCommand
    def testFindCommand (self):
        
        g.trace(self.find_p)
    #@nonl
    #@-node:EKR.20040623200709.48:testFindCommand
    #@+node:EKR.20040623200709.49:testFindWordCommand
    def testFindWordCommand (self):
        
        pass
    #@nonl
    #@-node:EKR.20040623200709.49:testFindWordCommand
    #@+node:EKR.20040623200709.50:testFindIgnoreCaseCommand
    def testFindIgnoreCaseCommand (self):
        
        pass
    #@nonl
    #@-node:EKR.20040623200709.50:testFindIgnoreCaseCommand
    #@-others
#@nonl
#@-node:EKR.20040623200709.46:class findCommandTestCase
#@-node:EKR.20040623200709.44:Find Command tests
#@+node:EKR.20040623200709.51:Import/Export tests
#@+node:EKR.20040623200709.52:makeImportExportSuite
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
#@-node:EKR.20040623200709.52:makeImportExportSuite
#@+node:EKR.20040623200709.53:class importExportTestCase
class importExportTestCase(unittest.TestCase):
    
    """Data-driven unit tests for Leo's edit body commands."""
    
    #@    @+others
    #@+node:EKR.20040623200709.54:__init__
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
    
    #@-node:EKR.20040623200709.54:__init__
    #@+node:EKR.20040623200709.55:importExport
    def importExport (self):
        
        c = self.c ; v = self.v
        
        g.app.unitTestDict = {}
    
        commandName = v.headString()
        command = getattr(c,commandName) # Will fail if command does not exist.
        command()
    
        failedMethod = g.app.unitTestDict.get("fail")
        self.failIf(failedMethod,failedMethod)
    #@nonl
    #@-node:EKR.20040623200709.55:importExport
    #@+node:EKR.20040623200709.56:runTest
    def runTest(self):
        
        # """Import Export Test Case"""
    
        self.importExport()
    #@nonl
    #@-node:EKR.20040623200709.56:runTest
    #@+node:EKR.20040623200709.57:setUp
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
        self.gui = leoGui.unitTestGui(dict,trace=False)
        
        
    #@nonl
    #@-node:EKR.20040623200709.57:setUp
    #@+node:EKR.20040623200709.58:shortDescription
    def shortDescription (self):
        
        try:
            return "ImportExportTestCase: %s %s" % (self.v.headString(),self.fileName)
        except:
            return "ImportExportTestCase"
    #@nonl
    #@-node:EKR.20040623200709.58:shortDescription
    #@+node:EKR.20040623200709.59:tearDown
    def tearDown (self):
        
        c = self.c ; temp_v = self.temp_v
        
        if self.gui:
            self.gui.destroySelf()
            self.gui = None
        
        temp_v.setTnodeText("",g.app.tkEncoding)
        temp_v.clearDirty()
        
        if not self.wasChanged:
            c.setChanged (False)
            
        if 1: # Delete all children of temp node.
            while temp_v.firstChild():
                temp_v.firstChild().doDelete(temp_v)
    
        c.selectVnode(self.old_v)
    #@nonl
    #@-node:EKR.20040623200709.59:tearDown
    #@-others
#@nonl
#@-node:EKR.20040623200709.53:class importExportTestCase
#@-node:EKR.20040623200709.51:Import/Export tests
#@+node:EKR.20040623200709.62:class leoFileTests
class leoFileTests(unittest.TestCase):
    
    """Data-driven unit tests to test .leo files."""
    
    #@    @+others
    #@+node:EKR.20040623200709.64:runTest
    def runTest(self,path):
        
        """Run the Check Outline command."""
        
        self.c = None
        self.old_c = c = g.top()
        self.old_gui = g.app.gui
        
        # print path
        
        ok, frame = g.openWithFileName(path,c,enableLog=False)
        assert(ok)
    
        self.c = frame.c
    
        errors = self.c.checkOutline(verbose=False,unittest=True)
    
        assert(errors == 0)
    #@nonl
    #@-node:EKR.20040623200709.64:runTest
    #@+node:EKR.20040623200709.66:tearDown
    def tearDown (self):
    
        """Close the .leo file if it was not already open."""
    
        if self.c and self.c != self.old_c:
            g.app.closeLeoWindow(self.c.frame)
    
        g.app.gui = self.old_gui
    #@nonl
    #@-node:EKR.20040623200709.66:tearDown
    #@+node:EKR.20040623215308:Tests
    #@+node:ekr.20040303063549.121:test test.leo
    def test1 (self):
    
        path = g.os_path_join(g.app.loadDir,"..","test","test.leo")
    
        self.runTest(path)
    #@nonl
    #@-node:ekr.20040303063549.121:test test.leo
    #@+node:ekr.20040303063549.122:test LeoPy.leo
    def test2 (self):
        
        path = g.os_path_join(g.app.loadDir,"LeoPy.leo")
    
        self.runTest(path)
    #@nonl
    #@-node:ekr.20040303063549.122:test LeoPy.leo
    #@+node:ekr.20040303063549.123:test leoPlugins.leo
    def test3 (self):
        
        path = g.os_path_join(g.app.loadDir,"..","plugins","leoPlugins.leo")
        
        self.runTest(path)
    #@nonl
    #@-node:ekr.20040303063549.123:test leoPlugins.leo
    #@+node:ekr.20040303063549.124:test LeoDocs.leo
    def test4 (self):
        
        path = g.os_path_join(g.app.loadDir,"..","doc","LeoDocs.leo")
        
        self.runTest(path)
    #@nonl
    #@-node:ekr.20040303063549.124:test LeoDocs.leo
    #@-node:EKR.20040623215308:Tests
    #@-others
#@nonl
#@-node:EKR.20040623200709.62:class leoFileTests
#@+node:EKR.20040623200709.67:Outline tests (tests undo)
#@+node:EKR.20040623200709.68: makeOutlineSuite
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
#@-node:EKR.20040623200709.68: makeOutlineSuite
#@+node:EKR.20040623200709.69:class outlineTestCase
class outlineTestCase(unittest.TestCase):
    
    """Data-driven unit tests for Leo's outline commands."""
    
    #@    @+others
    #@+node:EKR.20040623200709.70:__init__
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
    #@-node:EKR.20040623200709.70:__init__
    #@+node:EKR.20040623200709.71:outlineCommand
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
    #@-node:EKR.20040623200709.71:outlineCommand
    #@+node:EKR.20040623200709.72:runTest
    def runTest(self):
    
        self.outlineCommand()
    #@nonl
    #@-node:EKR.20040623200709.72:runTest
    #@+node:EKR.20040623200709.73:setUp
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
    #@-node:EKR.20040623200709.73:setUp
    #@+node:EKR.20040623200709.74:tearDown
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
    #@-node:EKR.20040623200709.74:tearDown
    #@-others
#@nonl
#@-node:EKR.20040623200709.69:class outlineTestCase
#@-node:EKR.20040623200709.67:Outline tests (tests undo)
#@+node:EKR.20040623200709.75:Plugin tests
#@+node:EKR.20040623200709.76: makePluginsSuite
def makePluginsSuite(verbose=False,*args,**keys):
    
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
#@-node:EKR.20040623200709.76: makePluginsSuite
#@+node:EKR.20040623200709.77:class pluginTestCase
class pluginTestCase(unittest.TestCase):
    
    """Unit tests for one Leo plugin."""
    
    #@    @+others
    #@+node:EKR.20040623200709.78:__init__
    def __init__ (self,fileName,verbose):
        
        # Init the base class.
        unittest.TestCase.__init__(self)
    
        self.fileName = fileName
        self.oldGui = None
        self.verbose = verbose
    #@nonl
    #@-node:EKR.20040623200709.78:__init__
    #@+node:EKR.20040623200709.79:pluginTest
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
    #@-node:EKR.20040623200709.79:pluginTest
    #@+node:EKR.20040623200709.80:runTest
    def runTest(self):
    
        self.pluginTest()
    #@nonl
    #@-node:EKR.20040623200709.80:runTest
    #@+node:EKR.20040623200709.81:setUp
    def setUp(self,*args,**keys):
    
        self.oldGui = g.app.gui
        # g.app.gui = leoTkinterGui.tkinterGui()
    #@nonl
    #@-node:EKR.20040623200709.81:setUp
    #@+node:EKR.20040623200709.82:shortDescription
    def shortDescription (self):
        
        return "pluginTestCase: " + self.fileName
    #@nonl
    #@-node:EKR.20040623200709.82:shortDescription
    #@+node:EKR.20040623200709.83:tearDown
    def tearDown (self):
    
        g.app.gui = self.oldGui
    #@nonl
    #@-node:EKR.20040623200709.83:tearDown
    #@-others
#@nonl
#@-node:EKR.20040623200709.77:class pluginTestCase
#@-node:EKR.20040623200709.75:Plugin tests
#@+node:EKR.20040623200709.84:Position tests
#@+node:EKR.20040623200709.85: makePositionSuite
def makePositionSuite(arg=None,all=True,verbose=False):
    
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
#@-node:EKR.20040623200709.85: makePositionSuite
#@+node:EKR.20040623200709.86:class positionTestCase
class positionTestCase(unittest.TestCase):
    
    """Unit tests for Leo's position class."""
    
    #@    @+others
    #@+node:EKR.20040623200709.87:setUp
    def setUp(self,*args,**keys):
        
        import leoGlobals as g
        
        self.c = c = g.top()
    
        self.verbose = True
        
        self.root = c.rootPosition()
    #@nonl
    #@-node:EKR.20040623200709.87:setUp
    #@+node:EKR.20040623200709.88:testComparisons
    def testComparisons (self):
        
        p = self.root
        assert(p == p.copy())
        assert(p != p.threadNext())
    #@nonl
    #@-node:EKR.20040623200709.88:testComparisons
    #@+node:EKR.20040623200709.89:testThatClonesShareSubtrees
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
    #@-node:EKR.20040623200709.89:testThatClonesShareSubtrees
    #@+node:EKR.20040623200709.90:Consistency tests...
    #@+node:EKR.20040623200709.91:testConsistencyOfAllNodesThreadNext
    def testConsistencyOfAllNodesThreadNextWithCopy(self):
        self.doConsistencyOfAllNodesThreadNext(True)
        
    def testConsistencyOfAllNodesThreadNext(self):
        self.doConsistencyOfAllNodesThreadNext(False)
    
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
    #@-node:EKR.20040623200709.91:testConsistencyOfAllNodesThreadNext
    #@+node:EKR.20040623200709.92:testConsistencyOfFirstChildAndChildrenIter
    def testConsistencyOfFirstChildAndChildrenIterWithCopy(self):
        self.doConsistencyOfFirstChildAndChildrenIter(True)
        
    def testConsistencyOfFirstChildAndChildrenIter(self):
        self.doConsistencyOfFirstChildAndChildrenIter(False)
    
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
    #@-node:EKR.20040623200709.92:testConsistencyOfFirstChildAndChildrenIter
    #@+node:EKR.20040623200709.93:testConsistencyOfLevel
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
    #@-node:EKR.20040623200709.93:testConsistencyOfLevel
    #@+node:EKR.20040623200709.94:testConsistencyOfNextBack
    def testConsistencyOfNextBack (self):
        
        """Test consistency of p.next and p.back."""
    
        for p in self.root.allNodes_iter():
            
            back = p.back()
            next = p.next()
            if back: assert(back.getNext() == p)
            if next: assert(next.getBack() == p)
    #@nonl
    #@-node:EKR.20040623200709.94:testConsistencyOfNextBack
    #@+node:EKR.20040623200709.95:testConsistencyOfParentAndParentsIter
    def testConsistencyOfParentAndParentsIterWithCopy(self):
        self.doConsistencyOfParentAndParentsIter(True)
        
    def testConsistencyOfParentAndParentsIter(self):
        self.doConsistencyOfParentAndParentsIter(False)
    
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
    #@-node:EKR.20040623200709.95:testConsistencyOfParentAndParentsIter
    #@+node:EKR.20040623200709.96:testConsistencyOfParentChild
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
    #@-node:EKR.20040623200709.96:testConsistencyOfParentChild
    #@+node:EKR.20040623200709.97:testConsistencyOfThreadBackNext
    def testConsistencyOfThreadBackNext (self):
    
        for p in self.root.allNodes_iter():
    
            threadBack = p.threadBack()
            threadNext = p.threadNext()
    
            if threadBack:
                assert(p == threadBack.getThreadNext())
        
            if threadNext:
                assert(p == threadNext.getThreadBack())
    #@nonl
    #@-node:EKR.20040623200709.97:testConsistencyOfThreadBackNext
    #@+node:EKR.20040623200709.98:testConsistencyOfVnodeListAndParents
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
    #@-node:EKR.20040623200709.98:testConsistencyOfVnodeListAndParents
    #@+node:EKR.20040623200709.99:testHasNextBack
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
    #@-node:EKR.20040623200709.99:testHasNextBack
    #@+node:EKR.20040623200709.100:testHasParentChild
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
    #@-node:EKR.20040623200709.100:testHasParentChild
    #@+node:EKR.20040623200709.101:testHasThreadNextBack
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
    #@-node:EKR.20040623200709.101:testHasThreadNextBack
    #@+node:EKR.20040623200709.102:testVnodeList
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
    #@-node:EKR.20040623200709.102:testVnodeList
    #@-node:EKR.20040623200709.90:Consistency tests...
    #@-others
#@nonl
#@-node:EKR.20040623200709.86:class positionTestCase
#@-node:EKR.20040623200709.84:Position tests
#@+node:EKR.20040623200709.103:Reformat Paragraph tests
# DTHEIN 2004.01.11: Added unit tests for reformatParagraph
#@nonl
#@+node:EKR.20040623200709.104:makeReformatParagraphSuite
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
#@-node:EKR.20040623200709.104:makeReformatParagraphSuite
#@+node:EKR.20040623200709.105:class reformatParagraphTestCase
# DTHEIN 2004.01.11: Added class
class reformatParagraphTestCase(unittest.TestCase):
    
    """Unit tests for Leo's reformat paragraph command."""
    
    #@    @+others
    #@+node:EKR.20040623200709.106:setUp
    # DTHEIN 2004.01.11: Added method
    def setUp(self):
    
        self.u = testUtils()
        self.c = g.top()
        self.current_v = self.c.currentVnode()
        self.old_v = self.c.currentVnode()
        root = self.u.findRootNode(self.current_v)
        self.temp_v = self.u.findNodeInTree(root,"tempNode")
        assert(self.temp_v)
        self.tempChild_v = None
        self.dataParent_v = self.u.findNodeInTree(root,"reformatParagraphsTests")
        assert(self.dataParent_v)
        self.before_v = None
        self.after_v = None
        self.case_v = None
        self.wasChanged = self.c.changed
        
    
    
    #@-node:EKR.20040623200709.106:setUp
    #@+node:EKR.20040623200709.107:tearDown
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
            c.setChanged (False)
            
        # Delete all children of temp node.
        #
        while temp_v.firstChild():
            temp_v.firstChild().doDelete(temp_v)
    
        # make the original node the current node
        #
        c.selectVnode(self.old_v)
    #@nonl
    #@-node:EKR.20040623200709.107:tearDown
    #@+node:EKR.20040623200709.108:testNoTrailingNewline
    # DTHEIN 2004.01.11: Added method
    def testNoTrailingNewline(self):
        
        self.singleParagraphTest("testNoTrailingNewline",2,24)
    #@-node:EKR.20040623200709.108:testNoTrailingNewline
    #@+node:EKR.20040623200709.109:testTrailingNewline
    # DTHEIN 2004.01.11: Added method
    def testTrailingNewline(self):
        
        self.singleParagraphTest("testTrailingNewline",3,0)
    #@-node:EKR.20040623200709.109:testTrailingNewline
    #@+node:EKR.20040623200709.110:testMixedLineLengths
    # DTHEIN 2004.01.11: Added method
    def testMixedLineLengths(self):
        
        self.singleParagraphTest("testMixedLineLengths",4,10)
    #@-node:EKR.20040623200709.110:testMixedLineLengths
    #@+node:EKR.20040623200709.111:testMixedLinesWithLeadingWS
    # DTHEIN 2004.01.11: Added method
    def testMixedLinesWithLeadingWS(self):
        
        self.singleParagraphTest("testMixedLinesWithLeadingWS",4,12)
    #@-node:EKR.20040623200709.111:testMixedLinesWithLeadingWS
    #@+node:EKR.20040623200709.112:testNoChangeRequired
    # DTHEIN 2004.01.11: Added method
    def testNoChangeRequired(self):
        
        self.singleParagraphTest("testNoChangeRequired",1,28)
    #@-node:EKR.20040623200709.112:testNoChangeRequired
    #@+node:EKR.20040623200709.113:testHonorLeadingWS
    # DTHEIN 2004.01.11: Added method
    def testHonorLeadingWS(self):
        
        self.singleParagraphTest("testHonorLeadingWS",5,16)
    #@-node:EKR.20040623200709.113:testHonorLeadingWS
    #@+node:EKR.20040623200709.114:testHonorLeadingWSVar1
    # DTHEIN 2004.01.11: Added method
    def testHonorLeadingWSVar1(self):
        
        self.singleParagraphTest("testHonorLeadingWSVar1",5,16)
    #@-node:EKR.20040623200709.114:testHonorLeadingWSVar1
    #@+node:EKR.20040623200709.115:testSimpleHangingIndent
    # DTHEIN 2004.01.11: Added method
    def testSimpleHangingIndent(self):
        
        self.singleParagraphTest("testSimpleHangingIndent",5,8)
    #@-node:EKR.20040623200709.115:testSimpleHangingIndent
    #@+node:EKR.20040623200709.116:testSimpleHangingIndentVar1
    # DTHEIN 2004.01.11: Added method
    def testSimpleHangingIndentVar1(self):
        
        self.singleParagraphTest("testSimpleHangingIndentVar1",5,8)
    #@-node:EKR.20040623200709.116:testSimpleHangingIndentVar1
    #@+node:EKR.20040623200709.117:testSimpleHangingIndentVar2
    # DTHEIN 2004.01.11: Added method
    def testSimpleHangingIndentVar2(self):
        
        self.singleParagraphTest("testSimpleHangingIndentVar2",5,8)
    #@-node:EKR.20040623200709.117:testSimpleHangingIndentVar2
    #@+node:EKR.20040623200709.118:testMultiParagraph
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
    #@-node:EKR.20040623200709.118:testMultiParagraph
    #@+node:EKR.20040623200709.119:testMultiParagraphWithList
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
    #@-node:EKR.20040623200709.119:testMultiParagraphWithList
    #@+node:EKR.20040623200709.120:testDirectiveBreaksParagraph
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
    #@-node:EKR.20040623200709.120:testDirectiveBreaksParagraph
    #@+node:EKR.20040623200709.121:testWithLeadingWSOnEmptyLines
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
    #@-node:EKR.20040623200709.121:testWithLeadingWSOnEmptyLines
    #@+node:EKR.20040623200709.122:singleParagraphTest
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
    
    #@-node:EKR.20040623200709.122:singleParagraphTest
    #@+node:EKR.20040623200709.123:checkPosition
    # DTHEIN 2004.01.11: Added method
    def checkPosition(self,expRow,expCol):
    
        row,col = self.getRowCol()
        self.failUnlessEqual(expCol,col,
            "Current position is (" + str(row) + "," + str(col) 
            + ");  expected cursor to be at column " + str(expCol) + ".")
        self.failUnlessEqual(expRow,row,
            "Current position is (" + str(row) + "," + str(col) 
            + ");  expected cursor to be at line " + str(expRow) + ".")
    #@-node:EKR.20040623200709.123:checkPosition
    #@+node:EKR.20040623200709.124:checkText
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
    #@-node:EKR.20040623200709.124:checkText
    #@+node:EKR.20040623200709.125:copyBeforeToTemp
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
    #@-node:EKR.20040623200709.125:copyBeforeToTemp
    #@+node:EKR.20040623200709.126:getCaseDataNodes
    # DTHEIN 2004.01.11: Added method
    def getCaseDataNodes(self,caseNodeName):
    
        self.case_v = self.u.findNodeInTree(self.dataParent_v,caseNodeName)
        self.before_v = self.u.findNodeInTree(self.case_v,"before")
        self.after_v  = self.u.findNodeInTree(self.case_v,"after")
    #@-node:EKR.20040623200709.126:getCaseDataNodes
    #@+node:EKR.20040623200709.127:getRowCol
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
    #@-node:EKR.20040623200709.127:getRowCol
    #@-others
#@nonl
#@-node:EKR.20040623200709.105:class reformatParagraphTestCase
#@-node:EKR.20040623200709.103:Reformat Paragraph tests
#@-others
#@nonl
#@-node:EKR.20040623200709:@thin ../src/leoTest.py
#@-leo
