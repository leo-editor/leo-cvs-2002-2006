#! /usr/bin/env python
#@+leo-ver=4
#@+node:@file leo.py 
#@@first

"""Entry point for Leo in Python."""

#@@language python
#@<< Import pychecker >>
#@+node:<< Import pychecker >>
#@+at 
#@nonl
# pychecker is extremely useful, and it sometimes reports problems 
# erroneously.  In particular, the following warnings are invalid:
# 
# in leoFrame.py and leoNodes.py: warnings about the event param not being 
# used. pychecker doesn't understand that these routines are Tkinter 
# callbacks.
# 
# in leoApp.py and leoGlobals.py: pychecker doesn't seem to handle globals 
# very well.  There are spurious warnings about globals.
# 
# several files: pychecker complains about several routines being "too big", 
# i.e., pychecker doesn't understand about literate programming.
# 
#@-at
#@@c

if 0: # Set to 1 for lint-like testing.  This can also be done in idle.
	try:
		import pychecker.checker
	except: pass
#@nonl
#@-node:<< Import pychecker >>
#@nl

from leoGlobals import *
import leoApp,leoConfig,leoNodes
import os,string,sys,traceback

#@+others
#@+node:run & allies
def run(fileName=None,*args,**keywords):
	
	"""Initialize and run Leo"""
	
	if not isValidPython(): return
	# Create the application object.
	import leoGlobals
	leoGlobals.gApp = leoApp.LeoApp()

	app.loadDir = computeLoadDir() # Depends on app.tkEncoding: uses utf-8 for now.
	app.config = leoConfig.config()
	app.setEncoding() # 10/20/03: do this earlier
	
	# Load plugins. Plugins may create app.gui.
	doHook("start1")
	if app.killed: return # Support for app.forceShutdown.
	# Create the default gui if needed.
	if app.gui == None: app.createTkGui()
	if app.use_gnx:
		if not app.leoID: app.setLeoID() # Forces the user to set app.leoID.
		app.nodeIndices = leoNodes.nodeIndices()
	# Initialize tracing and statistics.
	init_sherlock(args)
	clear_stats()
	# Create the main frame.  Show it and all queued messages.
	c,frame = createFrame(fileName)
	if not frame: return
	app.writeWaitingLog()
	v = c.currentVnode()
	doHook("start2",c=c,v=v,fileName=fileName)
	frame.c.redraw()
	frame.body.setFocus()
	app.initing = false # "idle" hooks may now call app.forceShutdown.
	app.gui.runMainLoop()
#@nonl
#@-node:run & allies
#@+node:isValidPython
def isValidPython():
	
	message = """
Leo requires Python 2.1 or higher.
You may download Python 2.1 and Python 2.2 from http://python.org/download/
"""
	try:
		if not CheckVersion(sys.version, "2.1"):
			app.gui.runAskOkDialog("Python version error",message=message,text="Exit")
			return false
		else:
			return true
	except:
		print "exception getting Python version"
		traceback.print_exc()
		return false
#@nonl
#@-node:isValidPython
#@+node:computeLoadDir
def computeLoadDir():
	
	"""Returns the directory containing leo.py."""
	
	# trace(app.tkEncoding)
	
	try:
		import leo
		path = os.path.abspath(leo.__file__)
		# 11/07/03: "mbcs" exists only on Windows.
		if sys.platform=="win32":
			path = toUnicode(path,"mbcs")
		else:
			path = toUnicode(path,app.tkEncoding)
		if path:
			loadDir = os.path.dirname(path)
		else:
			loadDir = None
		if not loadDir:
			loadDir = os.path.abspath(os.getcwd())
			print "Using emergency loadDir:",`loadDir`

		loadDir = toUnicode(loadDir,app.tkEncoding) # 10/20/03
		return loadDir
	except:
		print "Exception getting load directory"
		print traceback.print_exc()
		return None
#@nonl
#@-node:computeLoadDir
#@+node:createFrame (leo.py)
def createFrame (fileName):
	
	"""Create a LeoFrame during Leo's startup process."""
	
	# trace(app.tkEncoding,fileName)
	
	# Try to create a frame for the file.
	if fileName:
		fileName = os.path.join(os.getcwd(),fileName)
		fileName = os.path.normpath(fileName)
		fileName = toUnicode(fileName,app.tkEncoding) # 10/20/03
		if os.path.exists(fileName):
			ok, frame = openWithFileName(fileName) # 7/13/03: the global routine.
			if ok:
				# print fileName
				return frame.c,frame
	
	# Create a new frame & indicate it is the startup window.
	c,frame = app.gui.newLeoCommanderAndFrame(fileName=None)
	frame.setInitialWindowGeometry()
	frame.startupWindow = true
	
	# Report the failure to open the file.
	if fileName:
		es("File not found: " + fileName)

	return c,frame
#@nonl
#@-node:createFrame (leo.py)
#@+node:profile
#@+at 
#@nonl
# To gather statistics, do the following in a Python window, not idle:
# 
# 	import leo
# 	leo.profile()  (this runs leo)
# 	load leoDocs.leo (it is very slow)
# 	quit Leo.
#@-at
#@@c

def profile ():
	
	"""Gather and print statistics about Leo"""

	import profile, pstats
	
	name = "c:/prog/test/leoProfile.txt"
	profile.run('leo.run()',name)

	p = pstats.Stats(name)
	p.strip_dirs()
	p.sort_stats('cum','file','name')
	p.print_stats()
#@nonl
#@-node:profile
#@-others

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.platform=="win32": # Windows
			fileName = string.join(sys.argv[1:],' ')
		else:
			fileName = sys.argv[1]
		run(fileName)
	else:
		run()



#@-node:@file leo.py 
#@-leo
