#@+leo-ver=4
#@+node:@file leoTest.py
"""Unit tests for Leo"""

from leoGlobals import *
import unittest

#@+at 
#@nonl
# Run the unit tests from the "Leo Unit Tests" node in test/test.leo, like 
# this:
# 
# - update the tests here
# - save this file (LeoPy.leo)
# - rerun the tests immediately in test.leo using the Execute Script command.
# 
# The reload(leoTest) statement
#@-at
#@@c

#@+others
#@+node:tests of leoColor.py
#@+at 
#@nonl
# Changes made to get unit tests to work:
# 
# - vnodes now allow commands to be None.
# - colorizer now allows commands to be None.
# 
#@-at
#@@c

import leoColor,leoCommands,leoFrame,leoNodes
import Tkinter
Tk = Tkinter

#@+others
#@+node:class colorTests
class colorTests(unittest.TestCase):
	
	#@	@+others
	#@+node:color
	def color (self,language,text):
		
		self.text = text
		self.body.insert("1.0",text)
		self.colorizer.language = language
		val = self.colorizer.colorizeAnyLanguage(self.v,self.body)
		assert(val=="ok")
	#@-node:color
	#@+node:setUp
	def setUp(self):
	
		# 7/15/03: Hacked the vnode and colorizer classes to work if c == None.	
		c = None
		self.t = t = leoNodes.tnode()
		self.v = leoNodes.vnode(c,t)
		self.body = Tk.Text()
		self.colorizer = leoColor.colorizer(c)
		self.colorizer.incremental = false
	#@-node:setUp
	#@+node:tearDown
	def tearDown (self):
		
		self.body.destroy()
		self.body = None
		self.colorizer = None
		self.t = self.v = None
	#@nonl
	#@-node:tearDown
	#@+node:testC
	def testC (self):
		
		"""Test coloring for C."""
		
		self.color("c","""abc""")
	#@nonl
	#@-node:testC
	#@+node:testHTML1
	def testHTML1(self):
		
		"""Test coloring for HTML."""
		
		s = """@language html
	#@@color
	<HTML>
	<!-- Author: Edward K. Ream, edream@tds.net -->
	<HEAD>
	  <META NAME="GENERATOR" CONTENT="Microsoft FrontPage 4.0">
	  <TITLE> Leo's Home Page </TITLE>
	  <META NAME="description" CONTENT="This page describes Leo.
	Leo adds powerful outlines to the noweb and CWEB literate programming languages.">
	  <META NAME="keywords" CONTENT="LEO, LITERATE PROGRAMMING, OUTLINES, CWEB,
	NOWEB, OUTLINES, EDWARD K. REAM, DONALD E. KNUTH, SILVIO LEVY, OPEN SOFTWARE">
	</HEAD>
	<!-- Last Modified: May 12, 2002 -->
	<BODY BGCOLOR="#fffbdc">
	
	<H1 ALIGN=CENTER><a NAME="top"></a><IMG SRC="Blank.gif" width=
	"32" height="32" ALIGN="BOTTOM" NATURALSIZEFLAG="3"><IMG SRC="leo.gif" 
	WIDTH="32" HEIGHT="32" ALIGN="BOTTOM" NATURALSIZEFLAG="3"><a href="leo_TOC.html#top"><IMG SRC=
	"arrow_rt.gif" WIDTH="32" HEIGHT="32" ALIGN="BOTTOM" NATURALSIZEFLAG="3"></a> &nbsp;</H1>
	
	<H1 ALIGN=CENTER> Leo's Home Page</H1>
	
	<p align="center"><a href="http://www.python.org/"><img border="0" src="PythonPowered.gif" width="110" height="44"> </a> <A HREF="http://sourceforge.net/"><IMG SRC="http://sourceforge.net/sflogo.php?group_id=3458&type=1" NATURALSIZEFLAG="0" ALT="SourceForge Logo"></A>&nbsp;&nbsp;&nbsp;
	<A HREF="http://sourceforge.net/project/?group_id=3458">Leo at SourceForge</A>&nbsp;&nbsp;
	<a href="icons.html"><img border="0" src="LeoCodeGray.gif" width="77" height="42"></a>&nbsp;&nbsp;
	<a href="icons.html"><img border="0" src="LeoProse.gif" width="81" height="42"></a>&nbsp;&nbsp;&nbsp;&nbsp;
	
	<H3><A NAME="anchor127554"></A>Summary</H3>
	
	<UL>
	  <LI>Leo is a <i> programmer's editor</i>  and a flexible <i>browser</i> for
	    projects, programs, classes or data. Leo clarifies design, coding, debugging, testing
	  and maintenance.
	  <LI>Leo is an <i>outlining editor</i>. Outlines clarify the big picture while
	    providing unlimited space for details.
	  <LI>Leo
	    is a <a HREF="http://www.literateprogramming.com/"><i>literate
	    programming</i></a> tool, compatible with <A HREF="http://www.eecs.harvard.edu/~nr/noweb/">noweb</A>
	    and <a HREF="http://www-cs-faculty.stanford.edu/~knuth/cweb.html">CWEB</a>.
	    Leo enhances any text-based
	programming language, from assembly language and C to Java, Python and XML.
	  <LI>Leo is also a <i>data organizer</i>. A single Leo outline can generate complex
	    data spanning many different files.&nbsp; Leo has been used to manage web sites.
	  <LI>Leo is a <i> project manager</i>. Leo provides multiple views
	of a project within a single outline. Leo naturally represents tasks that remain
	    up-to-date.
	  <LI>Leo is fully <i> scriptable</i> using <A HREF="http://www.python.org/">Python</A>
	  and saves its files in <A HREF="http://www.w3.org/XML/">XML</A> format.
	  <LI>Leo is <i>portable</i>.&nbsp; Leo.py is 100% pure Python and will run on
	    any platform supporting <A HREF="http://www.python.org/">Python</A>
	    and <a href="http://tcl.activestate.com/">Tk/tcl</a>, including Windows,
	    Linux and MacOS X.&nbsp; Leo.exe runs on any Windows platform.
	  <LI>Leo is <a href="http://www.opensource.org/"> <i> Open Software</i></a>, distributed under
	    the <a href="http://www.python.org/doc/Copyright.html"> Python License</a>.
	</UL>
	
	<H3>More Information and downloads</H3>
	
	<ul>
	  <LI>An excellent <a href="http://www.3dtree.com/ev/e/sbooks/leo/sbframetoc_ie.htm">online
	    tutorial</a> and <A HREF="http://www.jserv.com/jk_orr/xml/leo.htm">Leo resource
	  page</A>, both written by <a href="http://www.jserv.com/jk_orr">Joe Orr</a>.
	  <LI>My brother's <a href="SpeedReam.html">slashdot
	    article about Leo</a>, the best description about why Leo is special.
	  <LI><A HREF="testimonials.html#anchor104391">What people are saying about Leo</A>
	  <LI><A HREF="leo_TOC.html#anchor964914">Complete users guide</A>
	    and
	    <A HREF="intro.html#anchor887874">tutorial introduction</A>  with
	  screen shots.
	  <li><a href="FAQ.html">FAQ</a> and <a href="http://sourceforge.net/forum/?group_id=3458">help and discussion
	    forums</a>, preferable to <A HREF="mailto:edream@tds.net">email</A> so others may join
	    in.</li>
	  <li><a href="icons.html">Icons</a> for bragging about Leo.</li>
	</ul>
	
	<a href="http://sourceforge.net/project/showfiles.php?group_id=3458">Download
	    Leo</a> from <A HREF="http://sourceforge.net/project/?group_id=3458">Leo's SourceForge
	site</A>.
	
	<P ALIGN=left>Leo's author is <A HREF="http://personalpages.tds.net/~edream/index.html">Edward
	  K. Ream</A> email: <A HREF="mailto:edream@tds.net">edream@tds.net</A> voice: (608) 231-0766
	
	<HR ALIGN=LEFT>
	
	<p align="center">
	
	<IMG SRC="Blank.gif" ALIGN="left" NATURALSIZEFLAG=
	"3" width="34" height="34"><IMG SRC="leo.gif" ALIGN="left" NATURALSIZEFLAG=
	"3" width="32" height="32"><a HREF="leo_TOC.html"><IMG SRC="arrow_rt.gif" WIDTH="32"
	HEIGHT="32" ALIGN="left" NATURALSIZEFLAG="3">
	
	</BODY>
	</HTML>"""
		
		self.color("html",s)
	#@nonl
	#@-node:testHTML1
	#@+node:testHTML2
	def testHTML2 (self):
		
		s = """@language html
	#@@color
	<? xml version="1.0">
	<!-- test -->
	<project name="Converter" default="dist">
	</project>"""
	
		self.color("html",s)
	#@nonl
	#@-node:testHTML2
	#@+node:testPHP
	def testPHP (self):
		
		s = """@language php
	#@+at 
	#@nonl
	# doc
	#@-at
	#@@c
	
	and or
	array
	array()
	this is a test.
	__CLASS__
	<?php and or array() ?>"""
	
		self.color("php",s)
	#@nonl
	#@-node:testPHP
	#@+node:testPython1
	def testPython1(self):
		
		"""Test python coloring 1."""
		
		s = '''"""python
	string"""d
	
	'this\
	is'''
	
		self.color("python",s)
	#@nonl
	#@-node:testPython1
	#@+node:testPython2
	def testPython2(self):
		
		s = """# This creates a free-floating copy of v's tree for undo.
	The copied trees must use different tnodes than the original."""
	
	def copyTree(self,root):
	
	    c = self
	    # Create the root vnode.
	    result = v = leoNodes.vnode(c,root.t)
	        # Copy the headline and icon values v.copyNode(root,v)
	        # Copy the rest of tree.
	        v.copyTree(root,v)
	    # Replace all tnodes in v by copies.
	    assert(v.nodeAfterTree() == None)
	    while v:
	        v.t = leoNodes.tnode(0, v.t.bodyString)
	        v = v.threadNext()
	    return result
	
		self.color("python",s)
	#@nonl
	#@-node:testPython2
	#@+node:testRebol
	def testRebol (self):
		
		s = """@language rebol
	
	; a comment
	about abs absolute add alert alias all alter and and~ any append arccosine arcsine arctangent array ask at  
	back bind boot-prefs break browse build-port build-tag  
	call caret-to-offset catch center-face change change-dir charset checksum choose clean-path clear clear-fields close comment complement compose compress confirm continue-post context copy cosine create-request crypt cvs-date cvs-version  
	debase decode-cgi decode-url decompress deflag-face dehex delete demo desktop detab dh-compute-key dh-generate-key dh-make-key difference dirize disarm dispatch divide do do-boot do-events do-face do-face-alt does dsa-generate-key dsa-make-key dsa-make-signature dsa-verify-signature  
	echo editor either else emailer enbase entab exclude exit exp extract 
	fifth find find-key-face find-window flag-face first flash focus for forall foreach forever form forskip fourth free func function  
	get get-modes get-net-info get-style  
	halt has head help hide hide-popup  
	if import-email in inform input insert insert-event-func intersect 
	join 
	last launch launch-thru layout license list-dir load load-image load-prefs load-thru log-10 log-2 log-e loop lowercase  
	make make-dir make-face max maximum maximum-of min minimum minimum-of mold multiply  
	negate net-error next not now  
	offset-to-caret open open-events or or~ 
	parse parse-email-addrs parse-header parse-header-date parse-xml path-thru pick poke power prin print probe protect protect-system  
	q query quit  
	random read read-io read-net read-thru reboot recycle reduce reform rejoin remainder remold remove remove-event-func rename repeat repend replace request request-color request-date request-download request-file request-list request-pass request-text resend return reverse rsa-encrypt rsa-generate-key rsa-make-key 
	save save-prefs save-user scroll-para second secure select send send-and-check set set-modes set-font set-net set-para set-style set-user set-user-name show show-popup sine size-text skip sort source split-path square-root stylize subtract switch  
	tail tangent textinfo third throw throw-on-error to to-binary to-bitset to-block to-char to-date to-decimal to-email to-event to-file to-get-word to-hash to-hex to-idate to-image to-integer to-issue to-list to-lit-path to-lit-word to-local-file to-logic to-money to-none to-pair to-paren to-path to-rebol-file to-refinement to-set-path to-set-word to-string to-tag to-time to-tuple to-url to-word trace trim try  
	unfocus union unique uninstall unprotect unset until unview update upgrade uppercase usage use  
	vbug view view-install view-prefs  
	wait what what-dir while write write-io  
	xor xor~  
	action! any-block! any-function! any-string! any-type! any-word!  
	binary! bitset! block!  
	char!  
	datatype! date! decimal! 
	email! error! event!  
	file! function!  
	get-word!  
	hash!  
	image! integer! issue!  
	library! list! lit-path! lit-word! logic!  
	money!  
	native! none! number!  
	object! op!  
	pair! paren! path! port!  
	refinement! routine!  
	series! set-path! set-word! string! struct! symbol!  
	tag! time! tuple!  
	unset! url!  
	word!  
	any-block? any-function? any-string? any-type? any-word?  
	binary? bitset? block?  
	char? connected? crypt-strength? 
	datatype? date? decimal? dir?  
	email? empty? equal? error? even? event? exists? exists-key?
	file? flag-face? found? function?  
	get-word? greater-or-equal? greater?  
	hash? head?  
	image? in-window? index? info? input? inside? integer? issue?  
	length? lesser-or-equal? lesser? library? link-app? link? list? lit-path? lit-word? logic?  
	modified? money?  
	native? negative? none? not-equal? number?  
	object? odd? offset? op? outside?  
	pair? paren? path? port? positive?  
	refinement? routine?  
	same? screen-offset? script? series? set-path? set-word? size? span? strict-equal? strict-not-equal? string? struct?  
	tag? tail? time? tuple? type?  
	unset? url?  
	value? view? 
	within? word?  
	zero?"""
	
		self.color("rebol",s)
	#@nonl
	#@-node:testRebol
	#@-others
#@nonl
#@-node:class colorTests
#@-others
#@nonl
#@-node:tests of leoColor.py
#@+node:tests of leoNodes.py
import leoNodes
#@nonl
#@-node:tests of leoNodes.py
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
#@+node:class LeoNodeError
class leoNodeError(Exception):
	pass
	

#@-node:class LeoNodeError
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
#@+node:class outlineConsistencyTests
class LeoOutlineError(Exception):
	pass

class outlineConsistencyTests(unittest.TestCase):
	
	"""test the consistency of .leo files"""

	pass # No tests yet.
#@-node:class outlineConsistencyTests
#@+node:functions
#@+at 
#@nonl
# These functions set up trees for testing and compare the result of a test 
# with the expected result.
#@-at
#@-node:functions
#@+node:numberOfNodesInOutline, numberOfClonesInOutline
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
#@nonl
#@-node:numberOfNodesInOutline, numberOfClonesInOutline
#@+node:createTestOutline
def createTestOutline():
	
	"""Creates a complex outline suitable for testing clones"""
	pass
#@nonl
#@-node:createTestOutline
#@+node:loadTestLeoFile
def loadTestLeoFile (leoFileName):
	
	"""Loads a .leo file containing a test outline"""
#@nonl
#@-node:loadTestLeoFile
#@+node:copyTestOutline
def copyTestOutline ():
	
	"""Copies an outline so that all join Links are "equivalent" to the original"""
	pass
#@nonl
#@-node:copyTestOutline
#@+node:compareTwoOutlines
def compareTwoOutlines (root1,root2):
	
	"""Compares two outlines, making sure that their topologies,
	content and join lists are equivent"""
	pass
#@nonl
#@-node:compareTwoOutlines
#@+node:compareLeoFiles
def compareLeoFiles (commander1, commander2):
	
	"""Compares the outlines in two Leo files"""
	
	c1 = commander1 ; c2 = commander2
	root1 = c1.rootVnode()
	root2 = c2.rootVnode()
#@-node:compareLeoFiles
#@+node:validateOutline
def validateOutline (root):
	
	"""Checks an outline for consistency"""
	pass
#@nonl
#@-node:validateOutline
#@+node:Scripts for checking clones
if 0:
	checkForMismatchedJoinedNodes()
	
	print createTopologyList(c=top(),root=top().currentVnode().parent(),useHeadlines=false)
	
	checkTopologiesOfLinkedNodes()
	
	checkForPossiblyBrokenLinks()
#@nonl
#@-node:Scripts for checking clones
#@+node:checkForMismatchedJoinedNodes
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
#@-node:checkForMismatchedJoinedNodes
#@+node:checkForPossiblyBrokenLinks
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
#@-node:checkForPossiblyBrokenLinks
#@+node:checkTopologiesOfLinkedNodes
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
#@-node:checkTopologiesOfLinkedNodes
#@+node:checkLinksOfNodesWithSameTopologies (to do)
#@+at 
#@nonl
# Nodes with the same topologies should be joined PROVIDED:
# 	- Topologies are non-trivial.
# 	- Topologies include tnodes somehow.
# 	- Topologies include headlines somehow.
#@-at
#@-node:checkLinksOfNodesWithSameTopologies (to do)
#@-others
#@nonl
#@-node:@file leoTest.py
#@-leo
