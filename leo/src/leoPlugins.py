#@+leo-ver=4
#@+node:@file leoPlugins.py
"""Install and run Leo plugins.

On startup:
- doPlugins() calls loadHandlers() to import all
  mod_XXXX.py files in the Leo directory.

- Imported files should register hook handlers using the
  registerHandler and registerExclusiveHandler functions.
  Only one "exclusive" function is allowed per hook.

After startup:
- doPlugins() calls doHandlersForTag() to handle the hook.
- The first non-None return is sent back to Leo.
"""

import leoGlobals as g
from leoGlobals import true,false

handlers = {}

def doPlugins(tag,keywords):
	if g.app.killed:
		return
	if tag == "start1":
		loadHandlers()
	return doHandlersForTag(tag,keywords)
		
#@+others
#@+node:loadHandlers
def loadHandlers(loadAllFlag=false):

	"""Load all enabled plugins from the plugins directory"""
	import glob,os
	
	plugins_path = g.os_path_join(g.app.loadDir,"..","plugins")
	manager_path = g.os_path_join(plugins_path,"pluginsManager.txt")
	
	files = glob.glob(g.os_path_join(plugins_path,"*.py"))
	files = [g.os_path_abspath(file) for file in files]

	if loadAllFlag:
		files.sort()
		enabled_files = files
	else:
		#@		<< set enabled_files from pluginsManager.txt >>
		#@+node:<< set enabled_files from pluginsManager.txt >>
		if not g.os_path_exists(manager_path):
			return
		
		enabled_files = []
		try:
			file = open(manager_path)
			lines = file.readlines()
			for s in lines:
				s = s.strip()
				if s and not g.match(s,0,"#"):
					enabled_files.append(g.os_path_join(plugins_path,s))
			file.close()
		except:
			g.es("Can not open: " + manager_path)
			import leoTest ; leoTest.fail()
			return
		#@nonl
		#@-node:<< set enabled_files from pluginsManager.txt >>
		#@nl
		enabled_files = [g.os_path_abspath(file) for file in enabled_files]
	
	# Load plugins in the order they appear in the enabled_files list.
	g.app.loadedPlugins = []
	if files and enabled_files:
		for file in enabled_files:
			if file in files:
				file = g.toUnicode(file,g.app.tkEncoding)
				g.importFromPath(file,plugins_path)
	if g.app.loadedPlugins and not loadAllFlag:
		g.es("%d plugins loaded" % (len(g.app.loadedPlugins)), color="blue")
		if 0:
			for name in g.app.loadedPlugins:
				print name
#@nonl
#@-node:loadHandlers
#@+node:doHandlersForTag
def doHandlersForTag (tag,keywords):
	
	"""Execute all handlers for a given tag, in alphabetical order"""

	global handlers

	if handlers.has_key(tag):
		handle_fns = handlers[tag]
		handle_fns.sort()
		for handle_fn in handle_fns:
			ret = handle_fn(tag,keywords)
			if ret is not None:
				return ret

	if handlers.has_key("all"):
		handle_fns = handlers["all"]
		handle_fns.sort()
		for handle_fn in handle_fns:
			ret = handle_fn(tag,keywords)
			if ret is not None:
				return ret
	return None
#@nonl
#@-node:doHandlersForTag
#@+node:registerHandler
def registerHandler(tags,fn):
	
	""" Register one or more handlers"""
	
	import types

	if type(tags) in (types.TupleType,types.ListType):
		for tag in tags:
			registerOneHandler(tag,fn)
	else:
		registerOneHandler(tags,fn)

def registerOneHandler(tag,fn):
	
	"""Register one handler"""

	global handlers

	existing = handlers.setdefault(tag,[])
	try:
		existing.append(fn)
	except AttributeError:
		g.es("*** Two exclusive handlers for '%s'" % tag)
#@-node:registerHandler
#@+node:registerExclusiveHandler
def registerExclusiveHandler(tags, fn):
	
	""" Register one or more exclusive handlers"""
	
	import types
	
	if type(tags) in (types.TupleType,types.ListType):
		for tag in tags:
			registerOneExclusiveHandler(tag,fn)
	else:
		registerOneExclusiveHandler(tags,fn)
			
def registerOneExclusiveHandler(tag, fn):
	
	"""Register one exclusive handler"""
	
	global handlers
	
	if handlers.has_key(tag):
		g.es("*** Two exclusive handlers for '%s'" % tag)
	else:
		handlers[tag] = (fn,)
#@-node:registerExclusiveHandler
#@+node:funcToMethod
#@+at 
#@nonl
# The following is taken from page 188 of the Python Cookbook.
# 
# The following method allows you to add a function as a method of any class.  
# That is, it converts the function to a method of the class.  The method just 
# added is available instantly to all existing instances of the class, and to 
# all instances created in the future.
# 
# The function's first argument should be self.
# 
# The newly created method has the same name as the function unless the 
# optional name argument is supplied, in which case that name is used as the 
# method name.
#@-at
#@@c

def funcToMethod(f,theClass,name=None):
	
	"""Converts the function f to a method of theClass with the given optional name."""

	setattr(theClass,name or f.__name__,f)
	
# That's all!
#@nonl
#@-node:funcToMethod
#@-others
#@nonl
#@-node:@file leoPlugins.py
#@-leo
