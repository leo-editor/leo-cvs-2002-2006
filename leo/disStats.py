#@+leo

#@+node:0::@file disStats.py
#@+body
# routines to gather static statistics about opcodes based on dis module.

import compiler,dis,os,string,sys,types,traceback


#@+others
#@+node:+1::go
#@+body
def go():
	
	dir = "c:/prog/leoCVS/leo/"
	modules = getModules(dir)
	stats = [0] * 256
	try:
		# Importing these might start leo itself and hang idle.
		modules.remove("leo")
		modules.remove("openLeo")
		modules.remove("openEkr")
		modules.remove("setup")
	except: pass
	# print modules
	
	for m in modules:
		try:
			print "module:", m
			exec("import " + m)
			a = eval(m)
			any(a,stats)
		except:
			traceback.print_exc()
			print "----- no matching class in", `m`
			
	print_stats(stats)
#@-body
#@-node:+0::go
#@+node:+1::getFiles
#@+body
def getFiles (dir):

	# Generate the list of modules.
	allFiles = os.listdir(dir)
	files = []
	for f in allFiles:
		head,tail = os.path.split(f)
		root,ext = os.path.splitext(tail)
		if ext==".py":
			files.append(os.path.join(dir,f))
			
	return files
#@-body
#@-node:+0::getFiles
#@+node:+1::getModules
#@+body
def getModules (dir):
	
	"""Return the list of Python files in dir."""
	
	files = []
	
	try:
		allFiles = os.listdir(dir)
		for f in allFiles:
			head,tail = os.path.split(f)
			fn,ext = os.path.splitext(tail)
			if ext==".py":
				files.append(fn)
	except: pass
			
	return files
#@-body
#@-node:+0::getModules
#@+node:+1::any
#@+body
def any(x,stats,printName = 0):
	# based on dis.dis()
	"""Gathers statistics for classes, methods, functions, or code."""
	if not x:
		return
	if type(x) is types.InstanceType:
		x = x.__class__
	if hasattr(x, 'im_func'):
		x = x.im_func
	if hasattr(x, 'func_code'):
		x = x.func_code
	if hasattr(x, '__dict__'):
		items = x.__dict__.items()
		items.sort()
		for name, x1 in items:
			if type(x1) in (types.MethodType,
							types.FunctionType,
							types.CodeType):
				if printName: print name
				try:
					any(x1,stats)
				except TypeError, msg:
					print "Sorry:", msg
	elif hasattr(x, 'co_code'):
		code(x,stats)
	else:
		raise TypeError, \
			  "don't know how to disassemble %s objects" % \
			  type(x).__name__
#@-body
#@-node:+0::any
#@+node:+1::code
#@+body
def code (co, stats):
	"""Gather static count statistics for a code object."""

	codeList = co.co_code
	# Count the number of occurances of each opcode.
	i = 0 ;  n = len(codeList)
	while i < n:
		c = codeList[i]
		op = ord(c)
		stats[op] += 1
		i = i+1
		if op >= dis.HAVE_ARGUMENT:
			i = i+2
#@-body
#@-node:+0::code
#@+node:+1::print_stats
#@+body
def print_stats (stats):

	stats2 = [] ; total = 0
	for i in xrange(0,256):
		if stats[i] > 0:
			stats2.append((stats[i],i))
		total += stats[i]

	stats2.sort()
	stats2.reverse()
	for stat,i in stats2:
		print string.rjust(`stat`,6), dis.opname[i]
	print "total", `total`
#@-body
#@-node:+0::print_stats
#@-others


#@-body
#@-node:0::@file disStats.py
#@-leo
