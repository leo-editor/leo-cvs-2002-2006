#@+leo
#@+node:0::@file customizeLeo.py
#@+body
"""Customize Leo using modules that register hooks.

On startup:
- customizeLeo() calls loadHandlers() to import all
  mod_XXXX.py files in the Leo directory.

- Imported files should register hook handlers using the
  registerHandler and registerExclusiveHandler functions.
  Only one "exclusive" function is allowed per hook.

After startup:
- customizeLeo() calls doHandlersForTag() to handle the hook.
- The first non-None return is sent back to Leo.
"""

from leoGlobals import *

handlers = {}

def customizeLeo(tag,keywords):
	if tag == "start2":
		es("customizeLeo loaded")
		loadHandlers()
	return doHandlersForTag(tag,keywords)
		

#@+others
#@+node:1::loadHandlers
#@+body
def loadHandlers():
	"""Load all plugins from the plugins directory"""
	import glob,os,sys
	oldpath = sys.path
	try: # Make sure we restore sys.path.
		files = glob.glob(os.path.join("plugins","mod_*.py"))
		if len(files) > 0:
			es("Loading plugins:")
			sys.path.append(os.path.join(os.getcwd(),"plugins"))
			for file in files:
				try:
					fn = shortFileName(file)
					module,ext = os.path.splitext(fn)
					exec ("import " + module)
				except:
					es("Exception importing " + module)
					es_exception()
	finally:
		sys.path = oldpath


#@-body
#@-node:1::loadHandlers
#@+node:2::doHandlersForTag
#@+body
def doHandlersForTag (tag,keywords):

	global handlers
	if handlers.has_key(tag):
		handle_fns = handlers[tag]
		for handle_fn in handle_fns:
			ret = handle_fn(tag,keywords)
			if ret is not None:
				return ret
	if handlers.has_key("all"):
		handle_fns = handlers["all"]
		for handle_fn in handle_fns:
			ret = handle_fn(tag,keywords)
			if ret is not None:
				return ret
	return None
#@-body
#@-node:2::doHandlersForTag
#@+node:3::registerHandler
#@+body
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
#@-body
#@-node:3::registerHandler
#@+node:4::registerExclusiveHandler
#@+body
def registerExclusiveHandler(tag, fn):
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

#@-body
#@-node:4::registerExclusiveHandler
#@+node:5::funcToMethod
#@+body
#@+at
#  The following is taken from page 188 of the Python Cookbook.
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
	setattr(theClass,name or f.__name__,f)
	
# That's all!
#@-body
#@-node:5::funcToMethod
#@-others
#@-body
#@-node:0::@file customizeLeo.py
#@-leo
