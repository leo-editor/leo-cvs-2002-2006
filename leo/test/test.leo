<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="35" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="78" left="89" height="75" width="114"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1"><vh>Coloring Test</vh>
<v t="T2"><vh>Colorizing Test</vh></v>
<v t="T3"><vh>Color test without images</vh></v>
<v t="T4"><vh>Color names test</vh></v>
</v>
<v t="T5"><vh>Write Missing @file nodes test</vh>
<v t="T6"><vh>@file ../test/missing_test.txt</vh></v>
</v>
<v t="T7"><vh>Icon bar</vh>
<v t="T8"><vh>add some buttons</vh></v>
<v t="T9"><vh>add all gif files</vh></v>
<v t="T10"><vh>clear</vh></v>
<v t="T11"><vh>hide</vh></v>
<v t="T12"><vh>configure</vh></v>
<v t="T13"><vh>show (puts at bottom)</vh></v>
</v>
<v t="T14"><vh>Status line</vh>
<v t="T15"><vh>put message</vh></v>
<v t="T16"><vh>clear</vh></v>
<v t="T17"><vh>tab width tests</vh>
<v t="T18"><vh>2</vh></v>
<v t="T19"><vh>4</vh></v>
<v t="T20"><vh>6</vh></v>
<v t="T21"><vh>8</vh></v>
</v>
</v>
<v t="T22"><vh>Test of recent sections &amp; clones</vh>
<v t="T23" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T24" a="CE"><vh>hyper link test</vh>
<v t="T23" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T25"><vh>&lt;&lt; section b &gt;&gt;</vh></v>
</v>
<v t="T24" a="C"><vh>hyper link test</vh>
<v t="T23" a="C"><vh>&lt;&lt; section a &gt;&gt;</vh></v>
<v t="T25"><vh>&lt;&lt; section b &gt;&gt;</vh></v>
</v>
</v>
<v t="T26" a="E"><vh>Copy/Clones test</vh>
<v t="T27" a="C"><vh>a Å</vh>
<v t="T28" a="CE"><vh>b</vh>
<v t="T29"><vh>c</vh></v>
</v>
<v t="T28" a="C"><vh>b</vh>
<v t="T29"><vh>c</vh></v>
</v>
</v>
<v t="T27" a="CE"><vh>a Å</vh>
<v t="T28" a="C"><vh>b</vh>
<v t="T29"><vh>c</vh></v>
</v>
<v t="T28" a="C"><vh>b</vh>
<v t="T29"><vh>c</vh></v>
</v>
</v>
</v>
<v t="T30"><vh>@lineending and @encoding tests</vh></v>
<v t="T31" a="V"><vh>@file test.py</vh>
<v t="T32"><vh>Outer</vh>
<v t="T33"><vh>A2</vh></v>
<v t="T34"><vh>B</vh></v>
</v>
</v>
<v t="T35"><vh>Check clones links</vh></v>
</vnodes>
<tnodes>
<t tx="T1">@markup wiki</t>
<t tx="T2">@language python

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
<t tx="T3">""" continued
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
<t tx="T4">""" text~~red:some text~~more text"""

""" text~~#ee0ff:some text~~more text"""</t>
<t tx="T5">@ignore</t>
<t tx="T6"></t>
<t tx="T7"></t>
<t tx="T8">from leoGlobals import *

top().frame.addIconButton(imagefile="../Icons/Leoapp.gif")

top().frame.addIconButton(text="hi")

top().frame.addIconButton(imagefile="../Icons/Leodoc.gif")</t>
<t tx="T9">from leoGlobals import *
import glob,os

f = top().frame

pattern = "c:/prog/leoCVS/leo/Icons/*.gif"
files = glob.glob(pattern)
files.sort()

f.clearIconBar()
for file in files:
	f.addIconButton(imagefile=file,bg="lightBlue")</t>
<t tx="T10">from leoGlobals import *

top().frame.clearIconBar()</t>
<t tx="T11">from leoGlobals import *

top().frame.hideIconBar()</t>
<t tx="T12">from leoGlobals import *

top().frame.iconFrame.configure(height="15m")</t>
<t tx="T13">from leoGlobals import *

top().frame.showIconBar()</t>
<t tx="T14"></t>
<t tx="T15">from leoGlobals import *
f = top().frame

f.clearStatusLine()

f.putStatusLine ("Hello")

for color in ("red","blue","yellow","green","orange"):
	f.putStatusLine (" %s " % (color),color=color)

f.putStatusLine(" World")</t>
<t tx="T16">from leoGlobals import *
f = top().frame

f.clearStatusLine()
</t>
<t tx="T17"></t>
<t tx="T18">@tabwidth 2

a
	b
		c	d</t>
<t tx="T19">@tabwidth 4

a
	b
		c	d</t>
<t tx="T20">@tabwidth 6

a
	b
		c	d</t>
<t tx="T21">@tabwidth 8

a
	b
		c	d</t>
<t tx="T22"></t>
<t tx="T23">This is section a.</t>
<t tx="T24">&lt;&lt; section a &gt;&gt;</t>
<t tx="T25"></t>
<t tx="T26"></t>
<t tx="T27"></t>
<t tx="T28"></t>
<t tx="T29"></t>
<t tx="T30">@lineending nl         (the default, Linux)
@lineending cr         (Mac)
@lineending crlf       (Windows)
@lineending lf          (same as nl, not recommended)
@lineending platform (same as platform value for output_newline setting in leoConfig.txt)

@encoding utf-8</t>
<t tx="T31"># Test file for cut/paste operations.

@others</t>
<t tx="T32"></t>
<t tx="T33">node A Text</t>
<t tx="T34">node B text</t>
<t tx="T35">from leoGlobals import *

checkClones2Links(verbose=true)</t>
</tnodes>
</leo_file>
