#@+leo-ver=4-thin
#@+node:edream.110203113231.924:@file-thin redirect_to_log.py
"""Send all output to the log pane"""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

def onStart (tag,keywords):
	from leoGlobals import redirectStdout,redirectStderr
	g.redirectStdout() # Redirect stdout
	g.redirectStderr() # Redirect stderr

# Register the handlers...
leoPlugins.registerHandler("start2", onStart)

__version__ = "1.3"
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.924:@file-thin redirect_to_log.py
#@-leo
