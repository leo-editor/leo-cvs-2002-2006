#@+leo-ver=4-thin
#@+node:edream.110203113231.734:@file-thin quit_leo.py
"""A plugin showing how to force Leo to quit."""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

def forceLeoToQuit(tag,keywords):
	if not g.app.initing:
		print "forceLeoToQuit",tag
		g.app.forceShutdown()

if 0: # Force a shutdown during startup.
	print "quitting during startup"
	g.app.forceShutdown()

if 1: # Force a shutdown at any other time, even "idle" time.

	# Exception: do not call g.app.forceShutdown in a "start2" hook.

	print __doc__
	leoPlugins.registerHandler("idle",forceLeoToQuit)

	__version__ = "1.2"
	g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.734:@file-thin quit_leo.py
#@-leo
