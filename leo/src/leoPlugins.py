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

from leoGlobals import *

handlers = {}
count = 0 ; examined = 0

def doPlugins(tag,keywords):
	if app.killed:
		return
	if tag == "start1":
		loadHandlers()
	return doHandlersForTag(tag,keywords)
		
#@+others
#@+node:loadHandlers
def loadHandlers():

	"""Load all plugins from the plugins directory"""
	import glob,os
	global count
	
	path = os_path_join(app.loadDir,"..","plugins")
	files = glob.glob(os_path_join(path,"*.py"))
	files.sort()
	if files:
		for file in files:
			file = toUnicode(file,app.tkEncoding)
			importFromPath(file,path)
		es("%d plugins loaded, %d examined" % (count,len(files)), color="blue")
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
		es("*** Two exclusive handlers for '%s'" % tag)
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
		es("*** Two exclusive handlers for '%s'" % tag)
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
