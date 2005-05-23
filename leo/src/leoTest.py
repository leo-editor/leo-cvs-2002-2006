#@+leo-ver=4-thin
#@+node:ekr.20050415070840:@thin ../src/leoTest.py
'''Classes for Leo's unit testing.

Run the unit tests in test.leo using the Execute Script command.'''

#@@language python
#@@tabwidth -4

__pychecker__ = '--no-import --no-reimportself --no-reimport --no-constCond --no-constant1'
    # Disable all import warnings.
    # Disable warnings about if 1 and if 0.

#@<< leoTest imports >>
#@+node:ekr.20050415070840.1:<< leoTest imports >>
import leoGlobals as g

import leoColor
import leoCommands
import leoFrame
import leoGui
import leoNodes
import leoTkinterGui

import compiler
import doctest
import glob
import os
import profile
import pstats
import sys
import tabnanny
import tokenize
import unittest

try: import timeit
except ImportError: timeit = None

try: import gc
except ImportError: gc = None
#@nonl
#@-node:ekr.20050415070840.1:<< leoTest imports >>
#@nl

if g.app: # Make sure we can import this module stand-alone.
    import leoPlugins
    newAtFile = leoPlugins.isLoaded("___proto_atFile")
else:
    newAtFile = False

#@+others
#@+node:ekr.20050415070840.2:Support @profile, @suite, @test, @timer
#@+node:ekr.20050415070840.3:isSuiteNode and isTestNode
def isSuiteNode (p):
    h = p.headString().lower()
    return g.match_word(h,0,"@suite")

def isTestNode (p):
    h = p.headString().lower()
    return g.match_word(h,0,"@test")
#@nonl
#@-node:ekr.20050415070840.3:isSuiteNode and isTestNode
#@+node:ekr.20050415070840.4:doTests...
def doTests(all,verbosity=1):

    c = g.top() ; p1 = p = c.currentPosition()

    g.app.unitTestDict["fail"] = False

    if all: theIter = c.all_positions_iter()
    else:   theIter = p.self_and_subtree_iter()

    changed = c.isChanged()
    suite = unittest.makeSuite(unittest.TestCase)

    for p in theIter:
        if isTestNode(p):
            test = makeTestCase(c,p)
            if test: suite.addTest(test)
        elif isSuiteNode(p):
            test = makeTestSuite(c,p)
            if test: suite.addTest(test)

    # Verbosity: 1: print just dots.
    c.beginUpdate()
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    c.endUpdate()
    c.setChanged(changed) # Restore changed state.
    c.selectVnode(p1) # N.B. Restore the selected node.
#@nonl
#@+node:ekr.20050415070840.5:class generalTestCase
class generalTestCase(unittest.TestCase):

    """Create a unit test from a snippet of code."""

    #@    @+others
    #@+node:ekr.20050415070840.6:__init__
    def __init__ (self,c,p):
    
         # Init the base class.
        unittest.TestCase.__init__(self)
    
        self.c = c
        self.p = p.copy()
    #@-node:ekr.20050415070840.6:__init__
    #@+node:ekr.20050415070840.7: fail
    def fail (self,msg=None):
    
        """Mark a unit test as having failed."""
        
        __pychecker__ = '--no-argsused'
            #  msg needed so signature matches base class.
    
        import leoGlobals as g
    
        g.app.unitTestDict["fail"] = g.callerName(2)
    #@nonl
    #@-node:ekr.20050415070840.7: fail
    #@+node:ekr.20050415070840.8:setUp
    def setUp (self):
    
        c = self.c ; p = self.p
    
        g.app.unitTesting = True
        c.beginUpdate()
        c.selectVnode(p)
    #@nonl
    #@-node:ekr.20050415070840.8:setUp
    #@+node:ekr.20050415070840.9:tearDown
    def tearDown (self):
    
        g.app.unitTesting = False
        self.c.endUpdate(False)
        # To do: restore the outline.
    #@nonl
    #@-node:ekr.20050415070840.9:tearDown
    #@+node:ekr.20050415070840.10:runTest
    def runTest (self,define_g = True):
    
        c = self.c ; p = self.p.copy()
        script = g.getScript(c,p).strip()
        self.assert_(script)
    
        # Execute the script. Let unit test handle any errors!
        
        if define_g:
            # Execute the test in an environment containing c, g & p.
            exec script + '\n' in {'c':c,'g':g,'p':p}
        else:
            # Execute the test in a totally pristine environment.
            exec script + '\n' in {}
    #@nonl
    #@-node:ekr.20050415070840.10:runTest
    #@+node:ekr.20050415070840.11:shortDescription
    def shortDescription (self):
    
        return self.p.headString() + '\n'
    #@nonl
    #@-node:ekr.20050415070840.11:shortDescription
    #@-others
#@nonl
#@-node:ekr.20050415070840.5:class generalTestCase
#@+node:ekr.20050415070840.12:makeTestSuite
#@+at 
#@nonl
# This code executes the script in an @suite node.  This code assumes:
# - The script creates a one or more unit tests.
# - The script puts the result in g.app.scriptDict["suite"]
#@-at
#@@c

def makeTestSuite (c,p):

    """Create a suite of test cases by executing the script in an @suite node."""
    
    p = p.copy()

    h = p.headString()
    script = g.getScript(c,p).strip()
    if not script:
        print "no script in %s" % h
        return None

    try:
        exec script + '\n' in {'c':c,'g':g,'p':p} # 3/10/05.
        suite = g.app.scriptDict.get("suite")
        if not suite:
            print "%s script did not set g.app.scriptDict" % h
        return suite
    except:
        g.es_exception()
        return None
#@nonl
#@-node:ekr.20050415070840.12:makeTestSuite
#@+node:ekr.20050415070840.13:makeTestCase
def makeTestCase (c,p):
    
    p = p.copy()

    if p.bodyString().strip():
        return generalTestCase(c,p)
    else:
        return None
#@nonl
#@-node:ekr.20050415070840.13:makeTestCase
#@-node:ekr.20050415070840.4:doTests...
#@+node:ekr.20050415070840.14:runProfileOnNode Not used
def runProfileOnNode (p,outputPath,):

    s = p.bodyString().rstrip() + '\n'

    profile.run(s,outputPath)

    stats = pstats.Stats(outputPath)
    stats.strip_dirs()
    stats.sort_stats('cum','file','name')
    stats.print_stats()
#@nonl
#@-node:ekr.20050415070840.14:runProfileOnNode Not used
#@+node:ekr.20050415070840.15:runTimerOnNode Not used
def runTimerOnNode (p,count):

    s = p.bodyString().rstrip() + '\n'
    t = timeit.Timer(s)

    try:
        if count is None:
            count = 1000000
        result = t.timeit(count)
        print "count: %d time: %f %s" % (count,result,p.headString())
    except:
        t.print_exc()
#@nonl
#@-node:ekr.20050415070840.15:runTimerOnNode Not used
#@-node:ekr.20050415070840.2:Support @profile, @suite, @test, @timer
#@+node:ekr.20050415070840.16:run gc
#@+node:ekr.20050415070840.17:runGC
lastObjectCount = 0
lastObjectsDict = {}
lastTypesDict = {}
lastFunctionsDict = {}

# Adapted from similar code in leoGlobals.g.
def runGc(disable=False):
    
    message = "runGC"

    if gc is None:
        print "@gc: can not import gc"
        return

    gc.enable()
    set_debugGc()
    gc.collect()
    printGc(message=message,onlyPrintChanges=False)
    if disable:
        gc.disable()
    # makeObjectList(message)

runGC = runGc
#@nonl
#@-node:ekr.20050415070840.17:runGC
#@+node:ekr.20050415070840.18:enableGc
def set_debugGc ():

    gc.set_debug(
        gc.DEBUG_STATS | # prints statistics.
        # gc.DEBUG_LEAK | # Same as all below.
        # gc.DEBUG_COLLECTABLE
        # gc.DEBUG_UNCOLLECTABLE
        gc.DEBUG_INSTANCES |
        gc.DEBUG_OBJECTS
        # gc.DEBUG_SAVEALL
    )
#@nonl
#@-node:ekr.20050415070840.18:enableGc
#@+node:ekr.20050415070840.19:makeObjectList
def makeObjectList(message):

    # WARNING: this id trick is not proper: newly allocated objects can have the same address as old objects.
    global lastObjectsDict
    objects = gc.get_objects()

    newObjects = [o for o in objects if not lastObjectsDict.has_key(id(o))]

    lastObjectsDict = {}
    for o in objects:
        lastObjectsDict[id(o)]=o

    print "%25s: %d new, %d total objects" % (message,len(newObjects),len(objects))
#@nonl
#@-node:ekr.20050415070840.19:makeObjectList
#@+node:ekr.20050415070840.20:printGc
def printGc(message=None,onlyPrintChanges=False):
    
    __pychecker__ = '--no-argsused' # onlyPrintChanges may be useful for debugging.

    if not message:
        message = g.callerName(n=2)

    global lastObjectCount

    n = len(gc.garbage)
    n2 = len(gc.get_objects())
    delta = n2-lastObjectCount

    print '-' * 30
    print "garbage: %d" % n
    print "%6d =%7d %s" % (delta,n2,"totals")

    #@    << print number of each type of object >>
    #@+node:ekr.20050415070840.21:<< print number of each type of object >>
    global lastTypesDict
    typesDict = {}
    
    for obj in gc.get_objects():
        n = typesDict.get(type(obj),0)
        typesDict[type(obj)] = n + 1
    
    # Create the union of all the keys.
    keys = typesDict.keys()
    for key in lastTypesDict.keys():
        if key not in keys:
            keys.append(key)
    
    keys.sort()
    for key in keys:
        n1 = lastTypesDict.get(key,0)
        n2 = typesDict.get(key,0)
        delta2 = n2-n1
        if delta2 != 0:
            print "%+6d =%7d %s" % (delta2,n2,key)
    
    lastTypesDict = typesDict
    typesDict = {}
    #@nonl
    #@-node:ekr.20050415070840.21:<< print number of each type of object >>
    #@nl
    if 0:
        #@        << print added functions >>
        #@+node:ekr.20050415070840.22:<< print added functions >>
        import types
        import inspect
        
        global lastFunctionsDict
        
        funcDict = {}
        
        for obj in gc.get_objects():
            if type(obj) == types.FunctionType:
                key = repr(obj) # Don't create a pointer to the object!
                funcDict[key]=None 
                if not lastFunctionsDict.has_key(key):
                    print ; print obj
                    args, varargs, varkw,defaults  = inspect.getargspec(obj)
                    print "args", args
                    if varargs: print "varargs",varargs
                    if varkw: print "varkw",varkw
                    if defaults:
                        print "defaults..."
                        for s in defaults: print s
        
        lastFunctionsDict = funcDict
        funcDict = {}
        #@nonl
        #@-node:ekr.20050415070840.22:<< print added functions >>
        #@nl

    lastObjectCount = n2
    return delta
#@nonl
#@-node:ekr.20050415070840.20:printGc
#@+node:ekr.20050415070840.23:printGcRefs
def printGcRefs (verbose=True):

    refs = gc.get_referrers(g.app.windowList[0])
    print '-' * 30

    if verbose:
        print "refs of", g.app.windowList[0]
        for ref in refs:
            print type(ref)
    else:
        print "%d referrers" % len(refs)
#@nonl
#@-node:ekr.20050415070840.23:printGcRefs
#@-node:ekr.20050415070840.16:run gc
#@+node:ekr.20050415070840.24: class testUtils
class testUtils:

    """Common utility routines used by unit tests."""

    #@    @+others
    #@+node:ekr.20050415070840.25:compareOutlines
    def compareOutlines (self,root1,root2,compareHeadlines=True,tag=''):
    
        """Compares two outlines, making sure that their topologies,
        content and join lists are equivalent"""
    
        p2 = root2.copy() ; ok = True
        for p1 in root1.self_and_subtree_iter():
            ok = (
                p1 and p2 and
                p1.numberOfChildren() == p2.numberOfChildren() and
                (not compareHeadlines or (p1.headString() == p2.headString())) and
                p1.bodyString() == p2.bodyString() and
                p1.isCloned()   == p2.isCloned()
            )
            if not ok: break
            p2.moveToThreadNext()
    
        if not ok:
            print 'compareOutlines failed',
            if tag: print 'tag:',tag
            else: print
            if p1: print 'p1',p1,p1.v
            if p2: print 'p2',p2,p2.v
            if not p1 or not p2:
                print 'p1 and p2'
            if p1.numberOfChildren() != p2.numberOfChildren():
                print 'p1.numberOfChildren()=%d, p2.numberOfChildren()=%d' % (
                    p1.numberOfChildren(),p2.numberOfChildren())
            if compareHeadlines and (p1.headString() != p2.headString()):
                print 'p1.head', p1.headString()
                print 'p2.head', p2.headString()
            if p1.bodyString() != p2.bodyString():
                print 'p1.body'
                print repr(p1.bodyString())
                print 'p2.body'
                print repr(p2.bodyString())
            if p1.isCloned() != p2.isCloned():
                print 'p1.isCloned() == p2.isCloned()'
    
        return ok
    #@nonl
    #@-node:ekr.20050415070840.25:compareOutlines
    #@+node:ekr.20050415070840.26:Finding nodes...
    #@+node:ekr.20050415070840.27:findChildrenOf
    def findChildrenOf (self,root):
    
        return [p.copy() for p in root.children_iter()]
    #@-node:ekr.20050415070840.27:findChildrenOf
    #@+node:ekr.20050415070840.28:findSubnodesOf
    def findSubnodesOf (self,root):
    
        return [p.copy() for p in root.subtree_iter()]
    #@nonl
    #@-node:ekr.20050415070840.28:findSubnodesOf
    #@+node:ekr.20050415070840.29:findNodeInRootTree
    def findRootNode (self,p):
    
        """Return the root of p's tree."""
    
        while p and p.hasParent():
            p.moveToParent()
        return p
    #@nonl
    #@-node:ekr.20050415070840.29:findNodeInRootTree
    #@+node:ekr.20050415070840.30:findNodeInTree
    def findNodeInTree(self,p,headline):
    
        """Search for a node in p's tree matching the given headline."""
    
        c = p.c
        for p in p.subtree_iter():
            h = headline.strip().lower()
            if p.headString().strip().lower() == h:
                return p.copy()
        return c.nullPosition()
    #@nonl
    #@-node:ekr.20050415070840.30:findNodeInTree
    #@+node:ekr.20050415070840.31:findNodeAnywhere
    def findNodeAnywhere(self,c,headline):
    
        for p in c.allNodes_iter():
            h = headline.strip().lower()
            if p.headString().strip().lower() == h:
                return p.copy()
        return c.nullPosition()
    #@nonl
    #@-node:ekr.20050415070840.31:findNodeAnywhere
    #@+node:ekr.20050415070840.32:findUnitTestNode (To Be Deleted)
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
    #@-node:ekr.20050415070840.32:findUnitTestNode (To Be Deleted)
    #@-node:ekr.20050415070840.26:Finding nodes...
    #@+node:ekr.20050415070840.33:numberOfClonesInOutline
    def numberOfClonesInOutline (self):
    
        """Returns the number of cloned nodes in an outline"""
    
        c = g.top() ; n = 0
        for p in c.allNodes_iter():
            if p.isCloned():
                n += 1
        return n
    #@nonl
    #@-node:ekr.20050415070840.33:numberOfClonesInOutline
    #@+node:ekr.20050415070840.34:numberOfNodesInOutline
    def numberOfNodesInOutline (self):
    
        """Returns the total number of nodes in an outline"""
    
        c = g.top()
        
        return len([p for p in c.allNodes_iter()])
    #@nonl
    #@-node:ekr.20050415070840.34:numberOfNodesInOutline
    #@+node:ekr.20050415070840.35:replaceOutline
    def replaceOutline (self,outline1,outline2):
    
        """Replace outline1 by a copy of outline 2,
    
        retaining the headline of outline1."""
    
        h = outline1.headString()
        copy = outline2.copyTreeAfter()
        copy.initHeadString(h)
        copy.unlink()
        copy.linkAfter(outline1)
        outline1.doDelete(copy)
    #@nonl
    #@-node:ekr.20050415070840.35:replaceOutline
    #@+node:ekr.20050415070840.36:testUtils.writeNode/sToNode
    #@+node:ekr.20050415070840.37:writeNodesToNode
    def writeNodesToNode (self,c,input,output,sentinels=True):
    
        result = []
        for p in input.self_and_subtree_iter():
            s = self.writeNodeToString(c,p,sentinels)
            result.append(s)
        result = ''.join(result)
        output.scriptSetBodyString (result)
    #@nonl
    #@-node:ekr.20050415070840.37:writeNodesToNode
    #@+node:ekr.20050415070840.38:writeNodeToNode
    def writeNodeToNode (self,c,input,output,sentinels=True):
    
        """Do an atFile.write the input tree to the body text of the output node."""
    
        s = self.writeNodeToString(c,input,sentinels)
    
        output.scriptSetBodyString (s)
    #@nonl
    #@-node:ekr.20050415070840.38:writeNodeToNode
    #@+node:ekr.20050415070840.39:writeNodeToString
    def writeNodeToString (self,c,input,sentinels):
    
        """Return an atFile.write of the input tree to a string."""
    
        df = c.atFileCommands
        nodeIndices = g.app.nodeIndices
    
        # Assign input.v.t.fileIndex
        nodeIndices.setTimestamp()
        for p in input.self_and_subtree_iter():
            try:
                theId,time,n = p.v.t.fileIndex
            except TypeError:
                p.v.t.fileIndex = nodeIndices.getNewIndex()
    
        # Write the file to a string.
        df.write(input,thinFile=True,nosentinels= not sentinels,toString=True)
        s = df.stringOutput
    
        return s
    #@nonl
    #@-node:ekr.20050415070840.39:writeNodeToString
    #@-node:ekr.20050415070840.36:testUtils.writeNode/sToNode
    #@+node:ekr.20050415070840.40:testUtils.compareIgnoringNodeNames
    def compareIgnoringNodeNames (self,s1,s2,delims,verbose=False):
    
        # Compare text containing sentinels, but ignore differences in @+-nodes.
    
        ## if marker[-1] == '@': marker = marker[:-1]
    
        delim1,delim2,delim3 = delims
    
        lines1 = g.splitLines(s1)
        lines2 = g.splitLines(s2)
        if len(lines1) != len(lines2):
            if verbose: g.trace("Different number of lines")
            return False
    
        for i in xrange(len(lines2)):
            line1 = lines1[i]
            line2 = lines2[i]
            if line1 == line2:
                continue
            else:
                n1 = g.skip_ws(line1,0)
                n2 = g.skip_ws(line2,0)
                if (
                    not g.match(line1,n1,delim1) or
                    not g.match(line2,n2,delim1)
                ):
                    if verbose: g.trace("Mismatched non-sentinel lines")
                    return False
                n1 += len(delim1)
                n2 += len(delim1)
                if g.match(line1,n1,"@+node") and g.match(line2,n2,"@+node"):
                    continue
                if g.match(line1,n1,"@-node") and g.match(line2,n2,"@-node"):
                    continue
                else:
                    if verbose:
                        g.trace("Mismatched sentinel lines",delim1)
                        g.trace("line1:",repr(line1))
                        g.trace("line2:",repr(line2))
                    return False
        return True
    #@nonl
    #@-node:ekr.20050415070840.40:testUtils.compareIgnoringNodeNames
    #@-others
#@nonl
#@-node:ekr.20050415070840.24: class testUtils
#@+node:ekr.20050415070840.41: fail
def fail ():

    """Mark a unit test as having failed."""
    
    __pychecker__ = '--no-argsused'
        #  msg needed so signature matches base class.

    import leoGlobals as g

    g.app.unitTestDict["fail"] = g.callerName(2)
#@nonl
#@-node:ekr.20050415070840.41: fail
#@+node:ekr.20050415070840.42:leoTest.runLeoTest
def runLeoTest(path,verbose=False,full=False):

    c = g.top() ; frame = None ; ok = False
    old_gui = g.app.gui

    try:
        g.app.unitTesting = True
        ok, frame = g.openWithFileName(path,c,enableLog=False)
        assert(ok and frame)
        errors = frame.c.checkOutline(verbose=verbose,unittest=True,full=full)
        assert(errors == 0)
        ok = True
    finally:
        g.app.gui = old_gui
        if frame and frame.c != c:
            g.app.closeLeoWindow(frame.c.frame)
        g.app.unitTesting = False
        c.frame.top.update()

    if not ok: raise
#@nonl
#@-node:ekr.20050415070840.42:leoTest.runLeoTest
#@+node:ekr.20050415070840.43:Specific to particular unit tests...
#@+node:ekr.20050415070840.44:at-File test code (leoTest.py)
def runAtFileTest(c,p):

    """Common code for testing output of @file, @thin, etc."""

    at = c.atFileCommands
    child1 = p.firstChild()
    child2 = child1.next()
    h1 = child1.headString().lower().strip()
    h2 = child2.headString().lower().strip()
    assert(g.match(h1,0,"#@"))
    assert(g.match(h2,0,"output"))
    expected = child2.bodyString()

    # Compute the type from child1's headline.
    j = g.skip_c_id(h1,2)
    theType = h1[1:j]
    assert theType in ("@file","@thin","@nosent","@noref","@asis"), "bad type: %s" % type

    thinFile = theType == "@thin"
    nosentinels = theType in ("@asis","@nosent")

    if theType == "@asis":
        at.asisWrite(child1,toString=True)
    elif theType == "@noref":
        at.norefWrite(child1,toString=True)
    else:
        at.write(child1,thinFile=thinFile,nosentinels=nosentinels,toString=True)
    try:
        result = g.toUnicode(at.stringOutput,"ascii")
        assert(result == expected)
    except AssertionError:
        #@        << dump result and expected >>
        #@+node:ekr.20050415070840.45:<< dump result and expected >>
        print ; print '-' * 20
        print "result..."
        for line in g.splitLines(result):
            print "%3d" % len(line),repr(line)
        print '-' * 20
        print "expected..."
        for line in g.splitLines(expected):
            print "%3d" % len(line),repr(line)
        print '-' * 20
        #@nonl
        #@-node:ekr.20050415070840.45:<< dump result and expected >>
        #@nl
        raise
#@nonl
#@-node:ekr.20050415070840.44:at-File test code (leoTest.py)
#@+node:ekr.20050417095020:Reformat Paragraph test code (leoTest.py)
# DTHEIN 2004.01.11: Added unit tests for reformatParagraph
#@nonl
#@+node:ekr.20050417114404:class reformatParagraphTest
class reformatParagraphTest:
    
    '''A class to work around stupidities of the Unittest classes.'''
    
    #@    @+others
    #@+node:ekr.20050417121256:__init__
    def __init__ (self,c,p):
        
        self.c = c
        self.p = p.copy()
    
        self.go()
    #@nonl
    #@-node:ekr.20050417121256:__init__
    #@+node:ekr.20050417120717:go
    def go (self):
        
        ok = True
        try:
            try:
                self.setUp()
                self.runTest()
            except Exception:
                g.es_exception()
                ok = False
        finally:
            self.tearDown()
        if not ok:
            raise
    #@nonl
    #@-node:ekr.20050417120717:go
    #@+node:ekr.20050417105607.2:checkPosition
    def checkPosition(self,expRow,expCol):
    
        row,col = self.getRowCol()
    
        assert expCol == col,	"Got column %d.  Expected %d" % (col,expCol)
    
        assert expRow == row, "Got row %d.  Expected %d" % (row,expRow)
    #@nonl
    #@-node:ekr.20050417105607.2:checkPosition
    #@+node:ekr.20050417105607.3:checkText
    def checkText(self):
    
        new_text = self.tempChild.bodyString()
        ref_text = self.after.bodyString()
        newLines = new_text.splitlines(1)
        refLines = ref_text.splitlines(1)
        newLinesCount = len(newLines)
        refLinesCount = len(refLines)
        for i in range(min(newLinesCount,refLinesCount)):
            assert newLines[i] == refLines[i], \
                "Mismatch on line " + str(i) + "." \
                + "\nExpected text: " + `refLines[i]` \
                + "\n  Actual text: "	+ `newLines[i]`
                
        assert newLinesCount == refLinesCount, \
            "Expected " + str(refLinesCount) + " lines, but " \
            + "received " + str(newLinesCount) + " lines."
    #@nonl
    #@-node:ekr.20050417105607.3:checkText
    #@+node:ekr.20050417105607.4:copyBeforeToTemp
    def copyBeforeToTemp(self):
    
        c = self.c ; tempNode = self.tempNode
    
        # Delete all children of temp node.
        while tempNode.firstChild():
            tempNode.firstChild().doDelete(tempNode)
    
        # Copy the before node text to the temp node.
        text = self.before.bodyString()
        tempNode.setTnodeText(text,g.app.tkEncoding)
    
        # create the child node that holds the text.
        t = leoNodes.tnode(headString="tempChildNode")
        self.tempChild = self.tempNode.insertAsNthChild(0,t)
    
        # copy the before text to the temp text.
        text = self.before.bodyString()
        self.tempChild.setTnodeText(text,g.app.tkEncoding)
    
        # Make the temp child node current, and put the cursor at the beginning.
        c.selectVnode(self.tempChild)
        c.frame.body.setInsertPointToStartOfLine( 0 )
        c.frame.body.setTextSelection(None,None)
    #@nonl
    #@-node:ekr.20050417105607.4:copyBeforeToTemp
    #@+node:ekr.20050417105607.6:getRowCol
    def getRowCol(self):
    
        c = self.c ; body = c.frame.body.bodyCtrl ; gui = g.app.gui
        tab_width = c.frame.tab_width
    
        # Get the Tkinter row col position of the insert cursor.
        index = body.index("insert")
        row,col = gui.getindex(body,index)
    
        # Adjust col position for tabs.
        if col > 0:
            s = body.get("%d.0" % (row),index)
            s = g.toUnicode(s,g.app.tkEncoding)
            col = g.computeWidth(s,tab_width)
    
        return row,col
    #@nonl
    #@-node:ekr.20050417105607.6:getRowCol
    #@+node:ekr.20050417120717.1:runTest
    def runTest(self):
        
        g.trace('must be overridden in subclasses')
    #@nonl
    #@-node:ekr.20050417120717.1:runTest
    #@+node:ekr.20050417102531:setUp
    def setUp(self):
        
        p = self.p
        u = self.u = testUtils()
    
        self.before = u.findNodeInTree(p,"before")
        self.after  = u.findNodeInTree(p,"after")
        self.tempNode   = u.findNodeInTree(p,"tempNode")
        if not self.tempNode: print 'no tempNode: p = ',p.headString()
        assert(self.tempNode)
        self.tempChild = None
    
        self.copyBeforeToTemp()
    #@nonl
    #@-node:ekr.20050417102531:setUp
    #@+node:ekr.20050417103035.1:tearDown
    def tearDown(self):
    
        tempNode = self.tempNode
    
        # clear the temp node and mark it unchanged
        tempNode.setTnodeText("",g.app.tkEncoding)
        tempNode.clearDirty()
    
        # Delete all children of temp node.
        while tempNode.firstChild():
            tempNode.firstChild().doDelete(tempNode)
    #@nonl
    #@-node:ekr.20050417103035.1:tearDown
    #@-others
#@nonl
#@-node:ekr.20050417114404:class reformatParagraphTest
#@+node:ekr.20050417102526:class singleParagraphTest (reformatParagraphTest)
class singleParagraphTest (reformatParagraphTest):
    
    '''A class to work around stupidities of the Unittest classes.'''
    
    #@    @+others
    #@+node:ekr.20050417102526.1:__init__
    def __init__ (self,c,p,finalRow,finalCol):
        
        self.finalCol = finalCol
        self.finalRow = finalRow
        
        # Call the base class.
        reformatParagraphTest.__init__(self,c,p)
    #@nonl
    #@-node:ekr.20050417102526.1:__init__
    #@+node:ekr.20050417103035:runTest
    def runTest(self):
    
        # Reformat the paragraph
        self.c.reformatParagraph()
    
        # Compare the computed result to the reference result.
        self.checkText()
        self.checkPosition(self.finalRow,self.finalCol)
    #@nonl
    #@-node:ekr.20050417103035:runTest
    #@-others
#@nonl
#@-node:ekr.20050417102526:class singleParagraphTest (reformatParagraphTest)
#@+node:ekr.20050417095020.16:class multiParagraphTest (reformatParagraphTest)
class multiParagraphTest (reformatParagraphTest):
    
    #@    @+others
    #@+node:ekr.20050417120312:runTest
    def runTest(self):
    
        self.c.reformatParagraph()
        self.checkPosition(13,0)
    
        # Keep going, in the same manner
        self.c.reformatParagraph()
        self.checkPosition(25,0)
        self.c.reformatParagraph()
        self.checkPosition(32,11)
    
        # Compare the computed result to the reference result.
        self.checkText()
    #@nonl
    #@-node:ekr.20050417120312:runTest
    #@-others
#@nonl
#@-node:ekr.20050417095020.16:class multiParagraphTest (reformatParagraphTest)
#@+node:ekr.20050417095020.17:class multiParagraphWithListTest (reformatParagraphTest)
class multiParagraphWithListTest (reformatParagraphTest):
    
    #@    @+others
    #@+node:ekr.20050417120955:runTest
    def runTest(self):
    
        # reformat the paragraph and check insertion cursor position
        self.c.reformatParagraph()
        self.checkPosition(4,0)
    
        # Keep going, in the same manner.
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
    #@nonl
    #@-node:ekr.20050417120955:runTest
    #@-others
#@nonl
#@-node:ekr.20050417095020.17:class multiParagraphWithListTest (reformatParagraphTest)
#@+node:ekr.20050417095020.19:class leadingWSOnEmptyLinesTest (reformatParagraphTest)
class leadingWSOnEmptyLinesTest (reformatParagraphTest):
    
    #@    @+others
    #@+node:ekr.20050417121745:runTest
    def runTest(self):
    
        # reformat the paragraph and check insertion cursor position
        self.c.reformatParagraph()
        self.checkPosition(4,0)
    
        # Keep going, in the same manner
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
    #@nonl
    #@-node:ekr.20050417121745:runTest
    #@-others
#@nonl
#@-node:ekr.20050417095020.19:class leadingWSOnEmptyLinesTest (reformatParagraphTest)
#@+node:ekr.20050417095020.18:class testDirectiveBreaksParagraph (reformatParagraphTest)
class directiveBreaksParagraphTest (reformatParagraphTest):
    
    #@    @+others
    #@+node:ekr.20050417122215:runTest
    def runTest(self):
    
        # reformat the paragraph and check insertion cursor position
        self.c.reformatParagraph()
        self.checkPosition(13,0) # at next paragraph
    
        # Keep going, in the same manner
        self.c.reformatParagraph()
        self.checkPosition(25,0) # at next paragraph
        self.c.reformatParagraph()
        self.checkPosition(32,11)
    
        # Compare the computed result to the reference result.
        self.checkText()
    #@nonl
    #@-node:ekr.20050417122215:runTest
    #@-others
#@nonl
#@-node:ekr.20050417095020.18:class testDirectiveBreaksParagraph (reformatParagraphTest)
#@-node:ekr.20050417095020:Reformat Paragraph test code (leoTest.py)
#@+node:ekr.20050415070840.72:Edit Body test code (leoTest.py)
#@+node:ekr.20050415070840.73: makeEditBodySuite
def makeEditBodySuite():

    """Create an Edit Body test for every descendant of testParentHeadline.."""

    c = g.top() ; p = c.currentPosition()
    u = testUtils()
    data_p = u.findNodeInTree(p,"editBodyTests")
    assert(data_p)
    temp_p = u.findNodeInTree(data_p,"tempNode")
    assert(temp_p)

    # Create the suite and add all test cases.
    suite = unittest.makeSuite(unittest.TestCase)

    for p in data_p.children_iter():
        if p.headString()=="tempNode": continue # TempNode now in data tree.
        before = u.findNodeInTree(p,"before")
        after  = u.findNodeInTree(p,"after")
        sel    = u.findNodeInTree(p,"selection")
        ins    = u.findNodeInTree(p,"insert")
        if before and after:
            test = editBodyTestCase(c,p,before,after,sel,ins,temp_p)
            suite.addTest(test)
        else:
            print 'missing "before" or "after" for', p.headString()

    return suite
#@nonl
#@-node:ekr.20050415070840.73: makeEditBodySuite
#@+node:ekr.20050415070840.74:class editBodyTestCase
class editBodyTestCase(unittest.TestCase):

    """Data-driven unit tests for Leo's edit body commands."""

    #@    @+others
    #@+node:ekr.20050415070840.75: __init__
    def __init__ (self,c,parent,before,after,sel,ins,tempNode):
    
        # Init the base class.
        unittest.TestCase.__init__(self)
    
        self.u = testUtils()
    
        self.c = c
        self.parent = parent.copy()
        self.before = before.copy()
        self.after  = after.copy()
        self.sel    = sel.copy() # Two lines giving the selection range in tk coordinates.
        self.ins    = ins.copy() # One line giving the insert point in tk coordinate.
        self.tempNode = tempNode.copy()
        
        if 0:
            g.trace('parent',parent)
            g.trace('before',before)
            g.trace('after',after)
    #@nonl
    #@-node:ekr.20050415070840.75: __init__
    #@+node:ekr.20050415070840.76: fail
    def fail (self,msg=None):
    
        """Mark a unit test as having failed."""
        
        __pychecker__ = '--no-argsused'
            #  msg needed so signature matches base class.
    
        import leoGlobals as g
    
        g.app.unitTestDict["fail"] = g.callerName(2)
    #@-node:ekr.20050415070840.76: fail
    #@+node:ekr.20050415070840.77:editBody
    def editBody (self):
    
        c = self.c ; u = self.u
        
        if not g.app.enableUnitTest: return
    
        # Blank stops the command name.
        commandName = self.parent.headString()
        i = commandName.find(' ')
        if i > -1:
            commandName = commandName[:i] 
        # g.trace(commandName)
        
        # Compute the result in tempNode.bodyString()
        command = getattr(c,commandName)
        command()
    
        if 1:
            assert(u.compareOutlines(self.tempNode,self.after,compareHeadlines=False,tag='before undo1'))
            c.undoer.undo()
            assert(u.compareOutlines(self.tempNode,self.before,compareHeadlines=False,tag='after undo1'))
            c.undoer.redo()
            assert(u.compareOutlines(self.tempNode,self.after,compareHeadlines=False,tag='after redo'))
            c.undoer.undo()
            assert(u.compareOutlines(self.tempNode,self.before,compareHeadlines=False,tag='after undo2'))
            # c.frame.tree.redraw_now()
    #@-node:ekr.20050415070840.77:editBody
    #@+node:ekr.20050415070840.80:runTest
    def runTest(self):
    
        self.editBody()
    #@nonl
    #@-node:ekr.20050415070840.80:runTest
    #@+node:ekr.20050415070840.79:setUp
    def setUp(self):
    
        c = self.c ; tempNode = self.tempNode
        
        if not g.app.enableUnitTest: return
    
        # Delete all children of temp node.
        while tempNode.firstChild():
            tempNode.firstChild().doDelete(tempNode)
    
        text = self.before.bodyString()
    
        tempNode.setTnodeText(text,g.app.tkEncoding)
        c.selectPosition(self.tempNode)
    
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
    #@-node:ekr.20050415070840.79:setUp
    #@+node:ekr.20050415070840.78:tearDown
    def tearDown (self):
    
        c = self.c ; tempNode = self.tempNode
        
    
    
        c.selectVnode(tempNode)
        tempNode.setTnodeText("",g.app.tkEncoding)
    
        # Delete all children of temp node.
        while tempNode.firstChild():
            tempNode.firstChild().doDelete(tempNode)
            
        tempNode.clearDirty()
    #@nonl
    #@-node:ekr.20050415070840.78:tearDown
    #@-others
#@nonl
#@-node:ekr.20050415070840.74:class editBodyTestCase
#@-node:ekr.20050415070840.72:Edit Body test code (leoTest.py)
#@+node:ekr.20050415070840.81:Import/Export test code (leoTest.py)
#@+node:ekr.20050415070840.82:makeImportExportSuite
def makeImportExportSuite(parentHeadline,doImport):

    """Create an Import/Export test for every descendant of testParentHeadline.."""

    c = g.top() ; u = testUtils()

    parent = u.findNodeAnywhere(c,parentHeadline)
    assert(parent)
    temp = u.findNodeInTree(parent,"tempNode")
    assert(temp)

    # Create the suite and add all test cases.
    suite = unittest.makeSuite(unittest.TestCase)

    for p in parent.children_iter(copy=True):
        if p == temp: continue
        dialog = u.findNodeInTree(p,"dialog")
        assert(dialog)
        test = importExportTestCase(c,p,dialog,temp,doImport)
        suite.addTest(test)

    return suite
#@nonl
#@-node:ekr.20050415070840.82:makeImportExportSuite
#@+node:ekr.20050415070840.83:class importExportTestCase
class importExportTestCase(unittest.TestCase):

    """Data-driven unit tests for Leo's edit body commands."""

    #@    @+others
    #@+node:ekr.20050415070840.84:__init__
    def __init__ (self,c,v,dialog,temp_v,doImport):
    
        # Init the base class.
        unittest.TestCase.__init__(self)
    
        self.c = c
        self.dialog = dialog
        self.v = v
        self.temp_v = temp_v
    
        self.gui = None
        self.oldGui = None
        self.wasChanged = c.changed
        self.fileName = ""
        self.doImport = doImport
    
        self.old_v = c.currentVnode()
    #@nonl
    #@-node:ekr.20050415070840.84:__init__
    #@+node:ekr.20050415070840.85: fail
    def fail (self,msg=None):
    
        """Mark a unit test as having failed."""
        
        __pychecker__ = '--no-argsused'
            #  msg needed so signature matches base class.
    
        import leoGlobals as g
    
        g.app.unitTestDict["fail"] = g.callerName(2)
    #@nonl
    #@-node:ekr.20050415070840.85: fail
    #@+node:ekr.20050415070840.86:importExport
    def importExport (self):
    
        c = self.c ; v = self.v
    
        g.app.unitTestDict = {}
    
        commandName = v.headString()
        command = getattr(c,commandName) # Will fail if command does not exist.
        command()
    
        failedMethod = g.app.unitTestDict.get("fail")
        self.failIf(failedMethod,failedMethod)
    #@nonl
    #@-node:ekr.20050415070840.86:importExport
    #@+node:ekr.20050415070840.87:runTest
    def runTest(self):
    
        # """Import Export Test Case"""
    
        self.importExport()
    #@nonl
    #@-node:ekr.20050415070840.87:runTest
    #@+node:ekr.20050415070840.88:setUp
    def setUp(self):
    
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
        fileName = lines[1]
        
        # Replace '\\' by os.path.sep in fileName
        try:
            # os.path.sep does not exist in Python 2.2.x.
            sep = os.path.sep
            fileName = fileName.replace('\\',sep)
        except AttributeError:
            fileName = g.os_path_normpath(fileName)
    
        self.fileName = fileName = g.os_path_join(g.app.loadDir,"..",fileName)
    
        if self.doImport:
            theDict = {name: [fileName]}
        else:
            theDict = {name: fileName}
    
        g.app.unitTesting = True
        self.oldGui = g.app.gui
        self.gui = leoGui.unitTestGui(theDict,trace=False)
    #@nonl
    #@-node:ekr.20050415070840.88:setUp
    #@+node:ekr.20050415070840.89:shortDescription
    def shortDescription (self):
    
        try:
            return "ImportExportTestCase: %s %s" % (self.v.headString(),self.fileName)
        except:
            return "ImportExportTestCase"
    #@nonl
    #@-node:ekr.20050415070840.89:shortDescription
    #@+node:ekr.20050415070840.90:tearDown
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
                
        g.app.gui = self.oldGui
    
        c.selectVnode(self.old_v)
        g.app.unitTesting = False
    #@nonl
    #@-node:ekr.20050415070840.90:tearDown
    #@-others
#@nonl
#@-node:ekr.20050415070840.83:class importExportTestCase
#@-node:ekr.20050415070840.81:Import/Export test code (leoTest.py)
#@+node:ekr.20050415070840.91:Perfect Import test code (leoTest.py)
#@+node:ekr.20050415070840.92:About the Perfect Import tests
#@@killcolor
#@+at
# 
# This code assumes that the test code contains child nodes with the following 
# headlines:
# 
# -input          Contains the "before" tree, without sentinels
# -input-after    Contains the "after" tree, without sentinels.
# 
# These two nodes define what the test means.
# 
# The following nodes must also exist.  The test code sets their contents as 
# follows:
# 
# -output-sent        The result of writing the -input tree, with sentinels.
# -output-after-sent  The result of writing the -input-after tree, with 
# sentinels.
# -i_lines            The i_lines list created by mu.create_mapping
# -j_lines            The j_lines list created by stripping sentinels from 
# -input-after's tree.
# -result             The result of running mu.propagateDiffsToSentinelsLines, 
# containing sentinels.
# 
# A test passes if and only if the body of -result matches the body of 
# output-after-sent, ignoring the details of @+node and @-node sentinels.
#@-at
#@nonl
#@-node:ekr.20050415070840.92:About the Perfect Import tests
#@+node:ekr.20050415070840.93:runPerfectImportTest
def runPerfectImportTest(c,p,
    testing=False,verbose=False,
    ignoreSentinelsInCompare=False):
        
    __pychecker__ = '--no-shadowbuiltin' # input is a builtin.

    # The contents of the "-input" and "-input-after" nodes define the changes.

    c = g.top() ; p = c.currentPosition()
    u = testUtils()

    input           = u.findNodeInTree(p,"-input")              # i file: before the change.
    input_ins       = u.findNodeInTree(p,"-input-after")        # j file: after the change.
    output_sent     = u.findNodeInTree(p,"-output-sent")        # fat file -> i file.
    out_after_sent  = u.findNodeInTree(p,"-output-after-sent")  # Should match result.
    result          = u.findNodeInTree(p,"-result")
    ilines          = u.findNodeInTree(p,"-i_lines")
    jlines          = u.findNodeInTree(p,"-j_lines")

    # Create the output nodes containing sentinels from the original input.
    u.writeNodesToNode(c,input,output_sent,sentinels=True)
    u.writeNodesToNode(c,input_ins,out_after_sent,sentinels=True)

    mu = g.mulderUpdateAlgorithm(testing=testing,verbose=verbose)
    delims = g.comment_delims_from_extension("foo.py")

    fat_lines = g.splitLines(output_sent.bodyString())
    i_lines,mapping = mu.create_mapping(fat_lines,delims)
    if input_ins.hasChildren():
        # Get the lines by stripping sentinels from -output-after-sent node.
        lines = g.splitLines(out_after_sent.bodyString()) 
        j_lines = mu.removeSentinelsFromLines(lines,delims)
    else:
        j_lines = g.splitLines(input_ins.bodyString()) 

    # For viewing...
    ilines.scriptSetBodyString(''.join(i_lines))
    jlines.scriptSetBodyString(''.join(j_lines))
    if ilines.bodyString() != input.bodyString():
        if not ignoreSentinelsInCompare:
            print "i_lines != input !"

    # Put the resulting lines (with sentinels) into the -result node.
    lines = mu.propagateDiffsToSentinelsLines(i_lines,j_lines,fat_lines,mapping)
    result.scriptSetBodyString(''.join(lines))

    if ignoreSentinelsInCompare:
        sList = []
        for s in (result.bodyString(),out_after_sent.bodyString()):
            lines = g.splitLines(s)
            lines = mu.removeSentinelsFromLines(lines,delims)
            sList.append(''.join(lines))
        return sList[0] == sList[1]
    else:
        return u.compareIgnoringNodeNames(
            result.bodyString(),
            out_after_sent.bodyString(),
            delims,verbose=True)
#@nonl
#@-node:ekr.20050415070840.93:runPerfectImportTest
#@-node:ekr.20050415070840.91:Perfect Import test code (leoTest.py)
#@+node:ekr.20050415070840.94:Plugin tests... (leoTest.py)
#@+node:ekr.20050415070840.95:getAllPluginFilenames
def getAllPluginFilenames ():

    path = g.os_path_join(g.app.loadDir,"..","plugins")

    files = glob.glob(g.os_path_join(path,"*.py"))
    files = [g.os_path_abspath(f) for f in files]
    files.sort()
    return files
#@nonl
#@-node:ekr.20050415070840.95:getAllPluginFilenames
#@+node:ekr.20050415070840.96:testPlugin (no longer used)
def oldTestPlugin (fileName,verbose=False):
        
    path = g.os_path_join(g.app.loadDir,"..","plugins")
    path = g.os_path_abspath(path)
    
    g.app.unitTesting = True
    
    try:

        module = g.importFromPath(fileName,path)
        assert module, "Can not import %s" % path
        
        # Run any unit tests in the module itself.
        if hasattr(module,"unitTest"):
            if verbose:
                g.trace("Executing unitTest in plugins/%s..." % fileName)
    
            module.unitTest(verbose=verbose)
            
    finally:
        g.app.unitTesting = False
#@nonl
#@-node:ekr.20050415070840.96:testPlugin (no longer used)
#@+node:ekr.20050415070840.97:checkFileSyntax
def checkFileSyntax (fileName,s):
    
    try:
        compiler.parse(s + '\n')
    except SyntaxError:
        g.es("Syntax error in: %s" % fileName,color="blue")
        g.es_exception(full=False,color="black")
        raise
#@nonl
#@-node:ekr.20050415070840.97:checkFileSyntax
#@+node:ekr.20050415070840.98:checkFileTabs
def checkFileTabs (fileName,s):

    try:
        readline = g.readLinesClass(s).next
        tabnanny.process_tokens(tokenize.generate_tokens(readline))

    except tokenize.TokenError, msg:
        s = "Token error in %s" % fileName
        print s ; g.es(s,color="blue")
        s = str(msg)
        print s ; g.es(s)
        assert 0, "test failed"

    except tabnanny.NannyNag, nag:
        badline = nag.get_lineno()
        line    = nag.get_line()
        message = nag.get_msg()
        s = "Indentation error in %s, line %d" % (fileName, badline)
        print s ; g.es(s,color="blue")
        print message ; g.es(message)
        s = "offending line:\n%s" % repr(str(line))[1:-1]
        print s ; g.es(s)
        assert 0, "test failed"

    except:
        s = "unexpected exception"
        print s ; g.trace(s)
        g.es_exception()
        assert 0, "test failed"
#@nonl
#@-node:ekr.20050415070840.98:checkFileTabs
#@-node:ekr.20050415070840.94:Plugin tests... (leoTest.py)
#@+node:ekr.20050415070840.99:throwAssertionError
def throwAssertionError():
    
    assert 0, 'assert(0) as a test of catching assertions'
#@nonl
#@-node:ekr.20050415070840.99:throwAssertionError
#@-node:ekr.20050415070840.43:Specific to particular unit tests...
#@+node:ekr.20050415070840.100:Test of doctest
#@+node:ekr.20050415070840.101:factorial
def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    If the result is small enough to fit in an int, return an int.
    Else return a long.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> [factorial(long(n)) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000L
    >>> factorial(30L)
    265252859812191058636308480000000L
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000L

    It must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ...
    OverflowError: n too large
    """

    import math
    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        try:
            result *= factor
        except OverflowError:
            result *= long(factor)
        factor += 1
    return result
#@nonl
#@-node:ekr.20050415070840.101:factorial
#@-node:ekr.20050415070840.100:Test of doctest
#@+node:ekr.20050415070840.102:Docutils stuff
#@+node:ekr.20050415070840.103:createUnitTestsFromDoctests
def createUnitTestsFromDoctests (modules,verbose=True):

    created = False # True if suite is non-empty.

    suite = unittest.makeSuite(unittest.TestCase)

    for module in list(modules):
        # New in Python 4.2: n may be zero.
        try:
            test = doctest.DocTestSuite(module)
            n = test.countTestCases()
            if n > 0:
                suite.addTest(test)
                created = True
                if verbose:
                    print "found %2d doctests for %s" % (n,module.__name__)
        except ValueError:
            pass # No tests found.

    return g.choose(created,suite,None)
#@nonl
#@-node:ekr.20050415070840.103:createUnitTestsFromDoctests
#@+node:ekr.20050415070840.104:findAllAtFileNodes
def findAllAtFileNodes(c):

    paths = []

    for p in c.all_positions_iter():
        name = p.anyAtFileNodeName()
        if name:
            head,tail = g.os_path_split(name)
            filename,ext = g.os_path_splitext(tail)
            if ext == ".py":
                path = g.os_path_join(g.app.loadDir,name)
                path = g.os_path_abspath(path)
                paths.append(path)

    return paths
#@nonl
#@-node:ekr.20050415070840.104:findAllAtFileNodes
#@+node:ekr.20050415070840.105:importAllModulesInPathList
def importAllModulesInPathList(paths):

    paths = list(paths)
    modules = []

    for path in paths:
        module = safeImportModule(path)
        if module:
            modules.append(module)

    return modules
#@-node:ekr.20050415070840.105:importAllModulesInPathList
#@+node:ekr.20050415070840.106:importAllModulesInPath
def importAllModulesInPath (path):

    path = g.os_path_abspath(path)

    if not g.os_path_exists(path):
        g.es("path does not exist: %s" % path)
        return []

    path2 = g.os_path_join(path,"leo*.py")
    files = glob.glob(path2)
    modules = []

    for theFile in files:
        module = safeImportModule(theFile)
        if module:
            modules.append(module)

    return modules
#@-node:ekr.20050415070840.106:importAllModulesInPath
#@+node:ekr.20050415070840.107:safeImportModule
#@+at 
#@nonl
# Warning: do NOT use g.importFromPath here!
# 
# g.importFromPath uses imp.load_module, and that is equivalent to reload!
# reloading Leo files while running will crash Leo.
#@-at
#@@c

def safeImportModule (fileName):

    fileName = g.os_path_abspath(fileName)
    head,tail = g.os_path_split(fileName)
    moduleName,ext = g.os_path_splitext(tail)

    if ext == ".py":
        try:
            return __import__(moduleName)
        except ImportError:
            return None
    else:
        print "Not a .py file:",fileName
        return None
#@nonl
#@-node:ekr.20050415070840.107:safeImportModule
#@-node:ekr.20050415070840.102:Docutils stuff
#@+node:ekr.20050415070840.108:Test of doTestRoutinesInModule
#@+node:ekr.20050415070840.109:test_dummy & dummyTestCase
def test_dummy():
    import leoGlobals as g
    g.trace()
    # raise SyntaxError

class dummyTestClass: # NOT a TestCase.
    def test_one (self):
        import leoGlobals as g
        g.trace(self)
#@nonl
#@-node:ekr.20050415070840.109:test_dummy & dummyTestCase
#@-node:ekr.20050415070840.108:Test of doTestRoutinesInModule
#@-others
#@nonl
#@-node:ekr.20050415070840:@thin ../src/leoTest.py
#@-leo
