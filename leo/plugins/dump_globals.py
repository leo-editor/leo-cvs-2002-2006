#@+leo-ver=4-thin
#@+node:edream.110203113231.730:@file-thin dump_globals.py
"""Dump globals at startup"""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

#@+others
#@+node:edream.110203113231.731:onStart
def onStart (tag,keywords):

	print "\nglobals..."
	for s in globals():
		if s not in __builtins__:
			print s
	
	print "\nlocals..."
	for s in locals():
		if s not in __builtins__:
			print s
#@-node:edream.110203113231.731:onStart
#@-others

# Register the handlers...
leoPlugins.registerHandler("start2", onStart)

__version__ = "1.2"
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.730:@file-thin dump_globals.py
#@-leo
