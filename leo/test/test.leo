<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="68" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="63" left="468" height="75" width="94"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1"><vh>Notes</vh>
<v t="T2"><vh>Quote from Alex Martelli</vh></v>
<v t="T3"><vh>Singleton sequences</vh></v>
<v t="T4"><vh>How to get screenshots</vh></v>
</v>
<v t="T5"><vh>Distribution scripts</vh></v>
<v t="T6"><vh>Previous tests</vh>
<v t="T7"><vh>@file c:\prog\test\tab_test.txt</vh></v>
<v t="T8"><vh>@image Icons/Leoapp.GIF</vh></v>
<v t="T9"><vh>alloc tests</vh></v>
<v t="T10"><vh>Assignment tests</vh></v>
<v t="T11"><vh>Coloring Test</vh>
<v t="T12"><vh>Colorizing Test</vh></v>
<v t="T13"><vh>Color test without images</vh></v>
<v t="T14"><vh>Color names test</vh></v>
</v>
<v t="T15"><vh>Copy/Clones test</vh>
<v t="T16" a="C"><vh>a Å</vh>
<v t="T17" a="C"><vh>b</vh>
<v t="T18"><vh>c</vh></v>
</v>
<v t="T17" a="C"><vh>b</vh>
<v t="T18"><vh>c</vh></v>
</v>
</v>
<v t="T16" a="C"><vh>a Å</vh>
<v t="T17" a="C"><vh>b</vh>
<v t="T18"><vh>c</vh></v>
</v>
<v t="T17" a="C"><vh>b</vh>
<v t="T18"><vh>c</vh></v>
</v>
</v>
</v>
<v t="T19"><vh>Dialog tests</vh>
<v t="T20"><vh>Test askOk</vh></v>
<v t="T21"><vh>Test aboutLeo</vh></v>
<v t="T22"><vh>Test askLeoID</vh></v>
<v t="T23"><vh>Test askOkCancelNumber</vh></v>
<v t="T24"><vh>Test askOkCancel</vh></v>
<v t="T25"><vh>Test askYesNo</vh></v>
<v t="T26"><vh>Test askYesNoCancel</vh></v>
</v>
<v t="T27"><vh>Icon bar</vh>
<v t="T28"><vh>add some buttons</vh></v>
<v t="T29"><vh>add all gif files</vh></v>
<v t="T30"><vh>clear</vh></v>
<v t="T31"><vh>hide</vh></v>
<v t="T32"><vh>configure</vh></v>
<v t="T33"><vh>show (puts at bottom)</vh></v>
</v>
<v t="T34"><vh>Ignore</vh>
<v t="T35"><vh>@lineending and @encoding tests</vh></v>
<v t="T36"><vh>@file test.py</vh>
<v t="T37"><vh>Outer</vh>
<v t="T38"><vh>A2</vh></v>
<v t="T39"><vh>B</vh></v>
</v>
</v>
<v t="T40"><vh>Check clones links</vh></v>
</v>
<v t="T41"><vh>New import</vh></v>
<v t="T42"><vh>Overriding core classes</vh></v>
<v t="T43"><vh>Status line</vh>
<v t="T44"><vh>put message</vh></v>
<v t="T45"><vh>clear</vh></v>
<v t="T46"><vh>tab width tests</vh>
<v t="T47"><vh>2</vh></v>
<v t="T48"><vh>4</vh></v>
<v t="T49"><vh>6</vh></v>
<v t="T50"><vh>8</vh></v>
</v>
</v>
<v t="T51"><vh>Test of recent sections &amp; clones</vh>
<v t="T52" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T53" a="C"><vh>hyper link test</vh>
<v t="T52" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T54"><vh>&lt;&lt; section b &gt;&gt;</vh></v>
</v>
<v t="T53" a="C"><vh>hyper link test</vh>
<v t="T52" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T54"><vh>&lt;&lt; section b &gt;&gt;</vh></v>
</v>
</v>
<v t="T55"><vh>timeit (in 2.3b1)</vh></v>
<v t="T56"><vh>Trailing newline in body</vh></v>
<v t="T57"><vh>Use xml.sax</vh></v>
<v t="T58"><vh>v.__repr__ and v.__str___</vh></v>
<v t="T59"><vh>wrap test</vh>
<v t="T60" a="E"><vh>@file c:\prog\test\wrap_test.txt</vh>
<v t="T61"><vh>wrap node</vh></v>
<v t="T62"><vh>nowrap node</vh></v>
</v>
</v>
<v t="T63"><vh>Write Missing @file nodes test</vh>
<v t="T64"><vh>@file ../test/missing_test.txt</vh></v>
</v>
</v>
<v t="T65" a="V"><vh>Spell test </vh>
<v t="T66"><vh>node two</vh></v>
<v t="T67"><vh>node two no misspellings</vh></v>
</v>
<v t="T68"><vh>Undo typing tests</vh></v>
</vnodes>
<tnodes>
<t tx="T1"></t>
<t tx="T2">@nocolor

Personally, I nominate timeit.py as THE outstanding enhancement of Python 2.3
-- I love many of the others (the performance improvement in particular), but
timeit.py is the one I find myself using all of the time -- seems to provide an
innocuous way for programmers' typical obsession with performance and
micro-optimization to discharge itself harmlessly, cleansing their souls to
choose idioms on the basis of clarity, maintainability and readability, as of
course SHOULD be done :-)</t>
<t tx="T3"># Empty tuples are constructed by an empty pair of parentheses.
# tuple with one item is constructed by following a value with a comma.
# Examples:

# empty = ()
# singleton = 'hello',    # &lt;-- note trailing comma

s = "abc",

for i in s:
	print `i`
	
s = {"x":1, "y":2},

for i in s:
	print `i`</t>
<t tx="T4">import ImageGrab,os # requires PIL 1.1.3 or later

path = os.path.join(app().loadDir,"../","test","screenshot.gif")

ImageGrab.grab().save(path)
</t>
<t tx="T5">@color

if 1: # Save all files and tangle leoConfig.leo
	from leoGlobals import importFromPath
	preSetup = importFromPath("preSetup","c:\prog\leoCvs\leo")
	preSetup.setup()

if 1: # Replace config settings and create .zip file.
	import os
	os.system(r"c:\python22\python c:\prog\leoCvs\leo\setup.py sdist --formats=zip")</t>
<t tx="T6"></t>
<t tx="T7">----*---*---*---*---*---*
	.	.	.	.	.	
                        
.   ..  ... ....    .   
        .   ..</t>
<t tx="T8"></t>
<t tx="T9">import gc,Tkinter

# gc.set_debug(gc.DEBUG_STATS)

lastObjectCount = 0

def printGarbage(s):
	global lastObjectCount
	n  = len(gc.garbage)
	n2 = len(gc.get_objects())
	fmt = "%8s garbage: %d, objects:%+6d =%6d"
	print fmt % (s,n,n2-lastObjectCount,n2)
	lastObjectCount = n2

gc.collect()
printGarbage("start 1")
# Create a canvas widget for experimentation.
top = Tkinter.Tk()
frame = Tkinter.Frame(top) ; frame.pack()
canvas = Tkinter.Canvas(frame) ; canvas.pack()
# Allocate and (try to) deallocate widgets in the canvas.
x,y = 10,10
printGarbage("start 2")
for i in xrange(5):
	t = Tkinter.Text(canvas)
	canvas.create_window(x,y,window=t)
	y += 40
	printGarbage(" loop 1")
	t.destroy()
	canvas.delete("all")
	gc.collect() # Nuts...
	printGarbage(" loop 2")
# See when objects are really freed.
top.destroy()
printGarbage("end 1") # Huh ???
gc.collect()
printGarbage("end 2")
top = frame = canvas = None
gc.collect()
printGarbage("end 3")</t>
<t tx="T10"># The output of this is 5 5 6
# This shows that o2 is merely an alias for o.

class obj:
	def __init__(self,n):
		self.n = n

o = obj(5) ; print o.n,
o2  = o    ; print o2.n,
o.n = 6    ; print o2.n</t>
<t tx="T11">@markup wiki</t>
<t tx="T12">@language python

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
<t tx="T13">""" continued
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
<t tx="T14">""" text~~red:some text~~more text"""

""" text~~#ee0ff:some text~~more text"""</t>
<t tx="T15"></t>
<t tx="T16"></t>
<t tx="T17"></t>
<t tx="T18"></t>
<t tx="T19"></t>
<t tx="T20">from leoGlobals import *
import leoDialog

if 1: # passed
	print leoDialog.askOk(
		"My Test Dialog",
		"Please hit return to test this dialog.",
		text="whoopee",
		resizeable=false).run(modal=true)
	
if 1: # passed
	message = "leo.py requires Python 2.1 or higher"
	print leoDialog.askOk("Python version error",message=message,text="Exit").run(modal=true)
	
if 1: # passed
	fileName = "xyzzy"
	print leoDialog.askOk("Read-only ouline",
		"Warning: the outline: " + fileName + " is read-only.").run(modal=true)</t>
<t tx="T21">from leoGlobals import *
import leoDialog

ver = "version 3.14159 "
build = "-3.8" 
version = "leo.py 4.0 alpha 2, Build " + build + ", June 13, 2003\n\n"
copyright = (
	"Copyright 1999-2003 by Edward K. Ream\n" +
	"All Rights Reserved\n" +
	"Leo is distributed under the Python License")
url = "http://webpages.charter.net/edreamleo/front.html"
email = "edreamleo@charter.net"

leoDialog.aboutLeo(version,copyright,url,email).run(modal=false)</t>
<t tx="T22">import leoDialog

print leoDialog.askLeoID().run(modal=1)</t>
<t tx="T23">import leoDialog

print leoDialog.askOkCancelNumber("Enter Line Number","Line number:").run(modal=1)
</t>
<t tx="T24">import leoDialog

print leoDialog.askOkCancel("Proceed?",
	"Read @file Nodes is not undoable.\nProceed?").run(modal=1)</t>
<t tx="T25">import leoDialog

if 1: # passed
	message = "Replace changed outline with external changes?"
	print leoDialog.askYesNo("Conflict!",message).run(modal=1)
	
if 1: # passed
	print leoDialog.askYesNo("Revert",
		"Revert to previous version of xyzzy?").run(modal=1)
		
if 1: # passed
	print leoDialog.askYesNo(
		"Download Tutorial?",
		"Download tutorial (sbooks.chm) from SourceForge?").run(modal=1)</t>
<t tx="T26">import leoDialog

if 1: # passed
	print leoDialog.askYesNoCancel("Confirm",
		'Save changes to xyzzy before crashing?').run(modal=1)
		
if 1: # passed
	message = (
		"Conflicting changes in outline and temp file\n\n" +
		"Do you want to use the code in the outline or the temp file?\n\n")
	
	print leoDialog.askYesNoCancel(
		"Conflict!", message,
		yesMessage = "Outline",
		noMessage = "File",
		defaultButton = "Cancel").run(modal=1)</t>
<t tx="T27"></t>
<t tx="T28">from leoGlobals import *

top().frame.addIconButton(imagefile="../Icons/Leoapp.gif")

top().frame.addIconButton(text="hi")

top().frame.addIconButton(imagefile="../Icons/Leodoc.gif")</t>
<t tx="T29">from leoGlobals import *
import glob,os

f = top().frame

pattern = "c:/prog/leoCVS/leo/Icons/*.gif"
files = glob.glob(pattern)
files.sort()

f.clearIconBar()
for file in files:
	f.addIconButton(imagefile=file,bg="lightBlue")</t>
<t tx="T30">from leoGlobals import *

top().frame.clearIconBar()</t>
<t tx="T31">from leoGlobals import *

top().frame.hideIconBar()</t>
<t tx="T32">from leoGlobals import *

top().frame.iconFrame.configure(height="15m")</t>
<t tx="T33">from leoGlobals import *

top().frame.showIconBar()</t>
<t tx="T34">@ignore</t>
<t tx="T35">@lineending nl         (the default, Linux)
@lineending cr         (Mac)
@lineending crlf       (Windows)
@lineending lf          (same as nl, not recommended)
@lineending platform (same as platform value for output_newline setting in leoConfig.txt)

@encoding utf-8</t>
<t tx="T36"># Test file for cut/paste operations.

@others</t>
<t tx="T37"></t>
<t tx="T38">node A Text</t>
<t tx="T39">node B text</t>
<t tx="T40">from leoGlobals import *

checkClones2Links(verbose=true)</t>
<t tx="T41"># This shows that Python programs _could_ use .xpy files (xml files containing Leo/Python code).

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
<t tx="T42">import leoFrame
print "%d leoFrame instances" % leoFrame.LeoFrame.instances</t>
<t tx="T43"></t>
<t tx="T44">from leoGlobals import *
f = top().frame

f.clearStatusLine()

f.putStatusLine ("Hello")

for color in ("red","blue","yellow","green","orange"):
	f.putStatusLine (" %s " % (color),color=color)

f.putStatusLine(" World")</t>
<t tx="T45">from leoGlobals import *
f = top().frame

f.clearStatusLine()
</t>
<t tx="T46"></t>
<t tx="T47">@tabwidth 2

a
	b
		c	d</t>
<t tx="T48">@tabwidth 4

a
	b
		c	d</t>
<t tx="T49">@tabwidth 6

a
	b
		c	d</t>
<t tx="T50">@tabwidth 8

a
	b
		c	d</t>
<t tx="T51"></t>
<t tx="T52">This is section a.</t>
<t tx="T53">&lt;&lt; section a &gt;&gt;</t>
<t tx="T54"></t>
<t tx="T55">import timeit</t>
<t tx="T56">ab
</t>
<t tx="T57">from leoGlobals import *
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
<t tx="T58">from leoGlobals import *
c = top() ; v = c.currentVnode()
print v
print `v`</t>
<t tx="T59"></t>
<t tx="T60">@others</t>
<t tx="T61">@wrap

this should wrap aaaaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbbbbbb cccccccccccccccccc ddddddddddddddddddd eeeeeeeeeeeeeeeeeeeeee ffffffffffffffffffff</t>
<t tx="T62">@nowrap

this should NOT wrap aaaaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbbbbbb cccccccccccccccccc ddddddddddddddddddd eeeeeeeeeeeeeeeeeeeeee ffffffffffffffffffff</t>
<t tx="T63">@ignore</t>
<t tx="T64"></t>
<t tx="T65">a b leoDialogs leoFind leoAtFile leoFileCommands leoGlobals modal end
line tooo changed 9
</t>
<t tx="T66">this is another test.

hello there jkk this is werg
		
the cht sat on the marh
the cat was sitting phew, another day. by zz z z 
two initabc
</t>
<t tx="T67">everything good.</t>
<t tx="T68">test one</t>
</tnodes>
</leo_file>
