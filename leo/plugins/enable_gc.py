#@+leo-ver=4-thin
#@+node:edream.110203113231.732:@file-thin enable_gc.py
"""Enable debugging for garbage collector"""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

#@+others
#@+node:edream.110203113231.733:onStart
def onStart (tag,keywords):

	try:
		import gc
		gc.set_debug(gc.DEBUG_LEAK)
	except: pass
#@nonl
#@-node:edream.110203113231.733:onStart
#@-others

# Register the handlers...
leoPlugins.registerHandler("start2", onStart)

__version__ = "1.2"
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.732:@file-thin enable_gc.py
#@-leo
