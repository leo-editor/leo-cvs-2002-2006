#@+leo-ver=4-thin
#@+node:edream.110203113231.735:@file-thin trace_gc.py
"""Trace changes to objects at idle time"""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

import leoGlobals
leoGlobals.debugGC = true # Force debugging on.

def printIdleRefs(tag,keywords):
	g.printGcRefs(verbose=false)
	
gcCount = 0

def printIdleGC(tag,keywords):
	
	# Calling printGc is too expensive to do on every idle call.
	if tag == "idle":
		global gcCount ; gcCount += 1
		if (gcCount % 20) == 0:
			g.printGc(tag,onlyPrintChanges=true)
	else:
		g.printGc(tag,onlyPrintChanges=false)

# Register the handlers...
if 1: # Very effective.
	leoPlugins.registerHandler("idle", printIdleGC)
else: # Very precise.
	leoPlugins.registerHandler("all", printIdleGC)
if 0: # Another idea.
	leoPlugins.registerHandler("command2", printIdleRefs)

__version__ = "1.3"
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.735:@file-thin trace_gc.py
#@-leo
