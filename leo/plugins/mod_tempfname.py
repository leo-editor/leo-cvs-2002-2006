#@+leo-ver=4-thin
#@+node:EKR.20040517075715.1:@file-thin mod_tempfname.py
"""Replace Commands.openWithTempFilePath so Leo opens temporary
files with a filename that begins with the headline text, and
located in a "username_Leo" subdirectory of the temporary
directory. The "LeoTemp" prefix is omitted.  This makes it easier to
see which temporary file is related to which outline node."""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

import leoCommands
import getpass,os,tempfile

#@+others
#@+node:EKR.20040517075715.2:onStart
def onStart (tag,keywords):

	# g.trace("replacing openWithTempFilePath")

	g.funcToMethod(openWithTempFilePath,leoCommands.Commands,"openWithTempFilePath")
#@-node:EKR.20040517075715.2:onStart
#@+node:EKR.20040517075715.3:openWithTempFilePath
def openWithTempFilePath (self,v,ext):

	"""Return the path to the temp file corresponding to v and ext.

	Replaces the Commands method."""    

	try:
		leoTempDir = getpass.getuser() + "_" + "Leo"
	except:
		leoTempDir = "LeoTemp"
		g.es("Could not retrieve your user name.")
		g.es("Temporary files will be stored in: %s" % leoTempDir)

	td = os.path.join(os.path.abspath(tempfile.gettempdir()), leoTempDir)
	if not os.path.exists(td):
		os.mkdir(td)

	name = g.sanitize_filename(v.headString()) + '_' + str(id(v.t))  + ext
	path = os.path.join(td,name)
	return path
#@nonl
#@-node:EKR.20040517075715.3:openWithTempFilePath
#@-others

# Register the handlers...
leoPlugins.registerHandler("start2", onStart)

__version__ = "1.3"
g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517075715.1:@file-thin mod_tempfname.py
#@-leo
