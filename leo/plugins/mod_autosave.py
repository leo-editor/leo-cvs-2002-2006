#@+leo-ver=4-thin
#@+node:edream.110203113231.724:@file-thin mod_autosave.py
"""Autosave the Leo document every so often"""

#@@language python

# By Paul Paterson.
import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

import ConfigParser
import time, os

#@+others
#@+node:edream.110203113231.725:applyConfiguration
def applyConfiguration(config=None):
	
	"""Called when the user presses the "Apply" button on the Properties form"""

	global LAST_AUTOSAVE, ACTIVE, AUTOSAVE_INTERVAL

	if config is None:
		fileName = os.path.join(g.app.loadDir,"../","plugins","mod_autosave.ini")
		config = ConfigParser.ConfigParser()
		config.read(fileName)

	ACTIVE = config.get("Main", "Active")
	AUTOSAVE_INTERVAL = int(config.get("Main", "Interval"))
#@nonl
#@-node:edream.110203113231.725:applyConfiguration
#@+node:edream.110203113231.726:autosave
def autosave(tag, keywords):
	
	"""Save the current document if it has a name"""

	global LAST_AUTOSAVE
	
	if g.app.killed: return # Work around a Tk bug.

	if ACTIVE == "Yes":
		if time.time() - LAST_AUTOSAVE > AUTOSAVE_INTERVAL:
			c = g.top()
			if c.mFileName and c.changed:
				g.es("Autosave: %s" % time.ctime(),color="orange")
				c.fileCommands.save(c.mFileName)
			LAST_AUTOSAVE = time.time()
#@nonl
#@-node:edream.110203113231.726:autosave
#@-others

# Register the handlers...
AUTOSAVE_INTERVAL = 600
ACTIVE = "Yes"
LAST_AUTOSAVE = time.time()
applyConfiguration()

# Register the handlers...
leoPlugins.registerHandler("idle", autosave)

__version__ = "0.2"
g.es("auto save enabled",color="orange")
#@nonl
#@-node:edream.110203113231.724:@file-thin mod_autosave.py
#@-leo
