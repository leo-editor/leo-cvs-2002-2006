<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="19" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="65" left="214" height="75" width="117"/>
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
</v>
<v t="T4"><vh>Write Missing @file nodes test</vh>
<v t="T5"><vh>@file ../test/missing_test.txt</vh></v>
</v>
<v t="T6" a="E"><vh>Status line</vh>
<v t="T7"><vh>put message</vh></v>
<v t="T8"><vh>clear</vh></v>
<v t="T9"><vh>tab width tests</vh>
<v t="T10"><vh>2</vh></v>
<v t="T11"><vh>4</vh></v>
<v t="T12"><vh>6</vh></v>
<v t="T13"><vh>8</vh></v>
</v>
</v>
<v t="T14" a="E"><vh>Icon bar</vh>
<v t="T15" a="MV"><vh>add some buttons</vh></v>
<v t="T16"><vh>clear</vh></v>
<v t="T17"><vh>hide</vh></v>
<v t="T18"><vh>configure</vh></v>
<v t="T19"><vh>show (puts at bottom)</vh></v>
</v>
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
<t tx="T4">@ignore</t>
<t tx="T5"></t>
<t tx="T6"></t>
<t tx="T7">from leoGlobals import *
f = top().frame

f.clearStatusLine()

f.putStatusLine ("Hello")

for color in ("red","blue","yellow","green","orange"):
	f.putStatusLine (" %s " % (color),color=color)

f.putStatusLine(" World")</t>
<t tx="T8">from leoGlobals import *
f = top().frame

f.clearStatusLine()
</t>
<t tx="T9"></t>
<t tx="T10">@tabwidth 2

a
	b
		c	d</t>
<t tx="T11">@tabwidth 4

a
	b
		c	d</t>
<t tx="T12">@tabwidth 6

a
	b
		c	d</t>
<t tx="T13">@tabwidth 8

a
	b
		c	d</t>
<t tx="T14"></t>
<t tx="T15">from leoGlobals import *

top().frame.addIconButton(picture="c:/prog/leoCvs/leo/Icons/Leoapp.GIF")

top().frame.addIconButton(text="hi")

top().frame.addIconButton(picture="c:/prog/leoCvs/leo/Icons/Leodoc.GIF")</t>
<t tx="T16">from leoGlobals import *

top().frame.clearIconBar()</t>
<t tx="T17">from leoGlobals import *

top().frame.hideIconBar()</t>
<t tx="T18">from leoGlobals import *

top().frame.iconFrame.configure(height="15m")</t>
<t tx="T19">from leoGlobals import *

top().frame.showIconBar()</t>
</tnodes>
</leo_file>
