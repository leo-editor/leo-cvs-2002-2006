#! /usr/bin/env python
#@+leo-ver=4
#@+node:@file leo.py 
#@@first #! /usr/bin/env python

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
import leoApp,leoConfig,leoFrame,leoGui
import os,string,sys

#@+others
#@+node:runMainLoop
def runMainLoop(root):
	
	"""A function that runs root.mainloop()
	
	LeoN may replace this fuction entirely."""
	
	root.mainloop()
#@-node:runMainLoop
#@+node:run & allies
def run(fileName=None,*args,**keywords):
	
	"""Initialize and run Leo"""
	
	# Create the application object.
	app = leoApp.LeoApp()
	if not app: return
	setApp(app)
	if not app.startCreate(): return
	app.runMainLoop = runMainLoop # For LeoN.
	
	app.config = leoConfig.config() # No longer contains gui code.
	
	# Create default gui and the gui's main window.
	app.gui = gui = leoGui.tkinterGuiClass()
	app.root = gui.createRootWindow()
	gui.unknownMethod() # Unknown methods shouldn't cause crashes.

	# To do: plugins should test app.gui.
	doHook("start1") # Load plugins.

	gui.setDefaultIcon()
	gui.getDefaultConfigFont(app.config)
	gui.setEncoding()
	app.finishCreate() # No longer contains gui code.

	initSherlock(app,args)
	frame = createFrame(app,fileName)
	if not frame: return

	# Write queued output and redraw the screen.
	app.writeWaitingLog()

	c = frame.commands ; v = c.currentVnode()
	doHook("start2",c=c,v=v,fileName=fileName)

	frame.commands.redraw()
	set_focus(frame.commands,frame.body)

	app.runMainLoop(app.root)
#@-node:run & allies
#@+node:createFrame (leo.py)
def createFrame (app,fileName):
	
	"""Step 2 of Leo startup process:
		
	Create a Leo Frame."""
	
	# Try to create a frame for the file.
	if fileName:
		fileName = os.path.join(os.getcwd(),fileName)
		fileName = os.path.normpath(fileName)
		if os.path.exists(fileName):
			ok, frame = openWithFileName(fileName) # 7/13/03: the global routine.
			if ok:
				# print fileName
				return frame
	
	# Create a new frame & indicate it is the startup window.
	frame = leoFrame.LeoFrame()
	frame.setInitialWindowGeometry()
	frame.startupWindow = true
	
	# Report the failure to open the file.
	if fileName:
		es("File not found: " + fileName)

	return frame
#@nonl
#@-node:createFrame (leo.py)
#@+node:initSherlock
def initSherlock (app,args):
	
	"""Initialize Sherlock."""
	
	# Initialze Sherlock & stats.
	init_sherlock(args)
	clear_stats()
#@nonl
#@-node:initSherlock
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
