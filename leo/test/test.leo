<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="42" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="43" left="329" height="75" width="127"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1"><vh>Previous tests</vh>
<v t="T2"><vh>Coloring Test</vh>
<v t="T3"><vh>Colorizing Test</vh></v>
<v t="T4"><vh>Color test without images</vh></v>
<v t="T5"><vh>Color names test</vh></v>
</v>
<v t="T6"><vh>Write Missing @file nodes test</vh>
<v t="T7"><vh>@file ../test/missing_test.txt</vh></v>
</v>
<v t="T8"><vh>Icon bar</vh>
<v t="T9"><vh>add some buttons</vh></v>
<v t="T10"><vh>add all gif files</vh></v>
<v t="T11"><vh>clear</vh></v>
<v t="T12"><vh>hide</vh></v>
<v t="T13"><vh>configure</vh></v>
<v t="T14"><vh>show (puts at bottom)</vh></v>
</v>
<v t="T15"><vh>Status line</vh>
<v t="T16"><vh>put message</vh></v>
<v t="T17"><vh>clear</vh></v>
<v t="T18"><vh>tab width tests</vh>
<v t="T19"><vh>2</vh></v>
<v t="T20"><vh>4</vh></v>
<v t="T21"><vh>6</vh></v>
<v t="T22"><vh>8</vh></v>
</v>
</v>
<v t="T23"><vh>Test of recent sections &amp; clones</vh>
<v t="T24" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T25" a="CE"><vh>hyper link test</vh>
<v t="T24" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T26"><vh>&lt;&lt; section b &gt;&gt;</vh></v>
</v>
<v t="T25" a="C"><vh>hyper link test</vh>
<v t="T24" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T26"><vh>&lt;&lt; section b &gt;&gt;</vh></v>
</v>
</v>
<v t="T27"><vh>Copy/Clones test</vh>
<v t="T28" a="C"><vh>a Å</vh>
<v t="T29" a="CE"><vh>b</vh>
<v t="T30"><vh>c</vh></v>
</v>
<v t="T29" a="C"><vh>b</vh>
<v t="T30"><vh>c</vh></v>
</v>
</v>
<v t="T28" a="CE"><vh>a Å</vh>
<v t="T29" a="C"><vh>b</vh>
<v t="T30"><vh>c</vh></v>
</v>
<v t="T29" a="C"><vh>b</vh>
<v t="T30"><vh>c</vh></v>
</v>
</v>
</v>
<v t="T31"><vh>Ignore</vh>
<v t="T32"><vh>@lineending and @encoding tests</vh></v>
<v t="T33"><vh>@file test.py</vh>
<v t="T34"><vh>Outer</vh>
<v t="T35"><vh>A2</vh></v>
<v t="T36"><vh>B</vh></v>
</v>
</v>
<v t="T37"><vh>Check clones links</vh></v>
</v>
</v>
<v t="T38"><vh>New import</vh></v>
<v t="T39"><vh>timeit (in 2.3b1)</vh></v>
<v t="T40"><vh>Use xml.sax</vh></v>
<v t="T41"><vh>Screenshots</vh></v>
<v t="T42" a="V"><vh>Assingment tests</vh></v>
</vnodes>
<tnodes>
<t tx="T1"></t>
<t tx="T2">@markup wiki</t>
<t tx="T3">@language python

""" {picture file=../Icons/Leoapp.GIF}this """ # Problems with correct indexing following a graphic.

""" {picture file=../Icons/Leoapp.GIF}this """ # two copies work.

abc

""" {picture file=../Icons/Leodoc.GIF} """ # xyz


""" continued
string"""

@ ''ab'' __xxx__ ''wx'' __xyz__
@c

# /* ''ab'' __xxx__ ''wx'' __xyz__ */

# Test

""" ''' """ ''' """'''  # Leo handles the common cases correctly.

''' ''ab'' __xxx__ ''wx'' __xyz__ ''' # No wiki markup in ''' strings.

""" ''ab'' __xxx__ ''wx'' __xyz__ """

# ''ab'' __xxx__ ''wx'' __xyz__

""" ''y'' """

""" text~~#ff00ff:some text~~more text""

and if

from leoGlobals import * ; print app().loadDir</t>
<t tx="T4">""" continued
string"""

@ ''ab'' __xxx__ ''wx'' __xyz__  __''bolditalic''__ and ''__italicbold__''
@c

# /* ''ab'' __xxx__ ''wx'' __xyz__ */

__abc__ 

# Test

""" ''' """ ''' """'''  # Leo handles the __b__ common cases correctly.

''' ''ab'' __xxx__ ''wx'' __xyz__ ''' # No wiki markup in ''' strings.

""" ''ab'' __xxx__ ''wx'' __xyz__ """

# ''ab'' __xxx__ ''wx'' __xyz__

""" ''y'' """

""" text~~#ee00ff:some text~~more text"""



and if

from leoGlobals import * ; print app().loadDir
</t>
<t tx="T5">""" text~~red:some text~~more text"""

""" text~~#ee0ff:some text~~more text"""</t>
<t tx="T6">@ignore</t>
<t tx="T7"></t>
<t tx="T8"></t>
<t tx="T9">from leoGlobals import *

top().frame.addIconButton(imagefile="../Icons/Leoapp.gif")

top().frame.addIconButton(text="hi")

top().frame.addIconButton(imagefile="../Icons/Leodoc.gif")</t>
<t tx="T10">from leoGlobals import *
import glob,os

f = top().frame

pattern = "c:/prog/leoCVS/leo/Icons/*.gif"
files = glob.glob(pattern)
files.sort()

f.clearIconBar()
for file in files:
	f.addIconButton(imagefile=file,bg="lightBlue")</t>
<t tx="T11">from leoGlobals import *

top().frame.clearIconBar()</t>
<t tx="T12">from leoGlobals import *

top().frame.hideIconBar()</t>
<t tx="T13">from leoGlobals import *

top().frame.iconFrame.configure(height="15m")</t>
<t tx="T14">from leoGlobals import *

top().frame.showIconBar()</t>
<t tx="T15"></t>
<t tx="T16">from leoGlobals import *
f = top().frame

f.clearStatusLine()

f.putStatusLine ("Hello")

for color in ("red","blue","yellow","green","orange"):
	f.putStatusLine (" %s " % (color),color=color)

f.putStatusLine(" World")</t>
<t tx="T17">from leoGlobals import *
f = top().frame

f.clearStatusLine()
</t>
<t tx="T18"></t>
<t tx="T19">@tabwidth 2

a
	b
		c	d</t>
<t tx="T20">@tabwidth 4

a
	b
		c	d</t>
<t tx="T21">@tabwidth 6

a
	b
		c	d</t>
<t tx="T22">@tabwidth 8

a
	b
		c	d</t>
<t tx="T23"></t>
<t tx="T24">This is section a.</t>
<t tx="T25">&lt;&lt; section a &gt;&gt;</t>
<t tx="T26"></t>
<t tx="T27"></t>
<t tx="T28"></t>
<t tx="T29"></t>
<t tx="T30"></t>
<t tx="T31">@ignore</t>
<t tx="T32">@lineending nl         (the default, Linux)
@lineending cr         (Mac)
@lineending crlf       (Windows)
@lineending lf          (same as nl, not recommended)
@lineending platform (same as platform value for output_newline setting in leoConfig.txt)

@encoding utf-8</t>
<t tx="T33"># Test file for cut/paste operations.

@others</t>
<t tx="T34"></t>
<t tx="T35">node A Text</t>
<t tx="T36">node B text</t>
<t tx="T37">from leoGlobals import *

checkClones2Links(verbose=true)</t>
<t tx="T38"># This shows that Python programs _could_ use .xpy files (xml files containing Leo/Python code).

from leoGlobals import *
import imp
import sys

old_import = __import__ # Get the global function

def leo_import(name,old_import,globals=None, locals=None, fromlist=None):
	try:
		mod = sys.modules.get(name)
		if mod:
			es("Leo import: module exists: " + name, color="blue")
		else:
			mod = old_import(name,globals,locals,fromlist)
			es("Leo import: " + name,color="blue")
	except ImportError:
		es("Leo import: not found: " + name,color="blue")
		mod = None
	return mod
		
m = leo_import("leoTest",__import__)
es(m,color="red")</t>
<t tx="T39">import timeit</t>
<t tx="T40">from leoGlobals import *
import gc,os,time,leoNodes
from xml.sax import saxutils, make_parser
from xml.sax.xmlreader import InputSource

path = os.path.join(app().loadDir,"../","test","test2.leo")
path = os.path.join(app().loadDir,"LeoPy.leo")
path = os.path.normpath(path)

verbose = false
tnodes = vnodes = 0
start = None

def clean(s): return toEncodedString(s,"ascii")

class trace_parse(saxutils.XMLGenerator):
	def startDocument(self):
		if 0: # Doesn't smooth things out.
			gc.collect() 
		global start ; start = time.clock()
		if verbose:
			print ; print ; print '*' * 30 + " dump " + '*' * 30 ; print
			trace()
	def endDocument(self):
		global start ; print "total time" + "%6.3f" % (time.clock()-start)
		if verbose: trace()
	def startElement(self,name,atts):
		global vnodes,tnodes
		if verbose: print '&lt;' + clean(name).strip() + '&gt;',
		if name == "v":
			vnodes += 1 ; v = leoNodes.vnode(top(),leoNodes.tnode())
		elif name == "t":
			tnodes += 1 ; t = leoNodes.tnode()
	def endElement(self,name):
		if verbose: print '&lt;/' + clean(name).strip() + '&gt;'
	def characters(self,content):
		content = content.replace('\r','')
		if verbose and content.strip(): print clean(content)
	def ignorableWhitespace(self):                trace()
	def processingInstruction (self,target,data): trace()
	def skippedEntity(self,name):                 trace(name)
	def startElementNS(self,name,qname,attrs):    trace(name)
	def endElementNS(self,name,qname):            trace(name)
	
try:
	f = None
	try:
		print path
		if 1: # not needed, and it works.
			source = InputSource(path)
			# source.setEncoding(app().tkEncoding)
		else:
			source = f = open(path)
		parser = make_parser()
		parser.setContentHandler(trace_parse())
		parser.parse(source)
		print "vnodes,tnodes:",`vnodes`,`tnodes`
	except: es_exception()
finally:
	if f: f.close()</t>
<t tx="T41">import ImageGrab,os # requires PIL 1.1.3 or later

path = os.path.join(app().loadDir,"../","test","screenshot.gif")

ImageGrab.grab().save(path)
</t>
<t tx="T42"># The output of this is 5 5 6
# This shows that o2 is merely an alias for o.

class obj:
	def __init__(self,n):
		self.n = n

o = obj(5) ; print o.n,
o2  = o    ; print o2.n,
o.n = 6    ; print o2.n</t>
</tnodes>
</leo_file>
