#@+leo-ver=4
#@+node:@file add_directives.py
"""Support new @direcives"""

#@@language python

from leoPlugins import *
from leoGlobals import *

if 1:
	directives = "markup", # A tuple with one string.
else:
	directives = ("markup","markup2")
	
#@+others
#@+node:addPluginDirectives
def addPluginDirectives (tag,keywords):
	
	"""Add all new directives to globalDirectivesList"""
	
	global directives

	if 0:
		s = ""
		for d in directives:
			s += '@' + d + ' '
		es(s,color="blue")

	for d in directives:
		if d not in globalDirectiveList:
			globalDirectiveList.append(d)
#@nonl
#@-node:addPluginDirectives
#@+node:scanPluginDirectives
def scanPluginDirectives (tag, keywords):
	
	"""Add a tuple (d,v,s,k) to list for every directive d found"""
	
	global directives

	keys = ("c","v","s","old_dict","dict","pluginsList")
	c,v,s,old_dict,dict,pluginsList = [keywords.get(key) for key in keys]

	for d in directives:
		if not old_dict.has_key(d) and dict.has_key(d):
			# Point k at whatever follows the directive.
			k = dict[d]
			k += 1 + len(d) # Skip @directive
			k = skip_ws(s,k) # Skip whitespace
			# trace(`d`,`k`)
			pluginsList.append((d,v,s,k),)
#@-node:scanPluginDirectives
#@-others

# Register the handlers...
registerHandler("start1",addPluginDirectives)
registerHandler("scan-directives",scanPluginDirectives)

__version__ = "1.1"
plugin_signon(__name__)
#@nonl
#@-node:@file add_directives.py
#@-leo
