#@+leo-ver=4-thin
#@+node:edream.110203113231.720:@file-thin outline_export.py
"""Modify the way exported outlines are displayed"""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

def onStart (tag,keywords):
	import leoNodes
	g.funcToMethod(newMoreHead,leoNodes.vnode,"moreHead")

#@+others
#@+node:edream.110203113231.721:newMoreHead
# Returns the headline string in MORE format.

def newMoreHead (self,firstLevel,useVerticalBar=true):

	useVerticalBar = true # Force the vertical bar

	v = self
	level = self.level() - firstLevel
	if level > 0:
		if useVerticalBar:
			s = " |\t" * level
		else:
			s = "\t"
	else:
		s = ""
	s += g.choose(v.hasChildren(), "+ ", "- ")
	s += v.headString()
	return s
#@-node:edream.110203113231.721:newMoreHead
#@-others

# Register the handlers...
leoPlugins.registerHandler("start2", onStart)

__version__ = "1.2" # Set version for the plugin handler.
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.720:@file-thin outline_export.py
#@-leo
