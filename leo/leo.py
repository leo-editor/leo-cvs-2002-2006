#@+leo

#@+node:0::@file leo.py
#@+body
# Top level of leo.py


#@<< Import pychecker >>
#@+node:1::<< Import pychecker >>
#@+body
#@+at
#  pychecker is extremely useful, and it sometimes reports problems erroneously.  In particular, the following warnings are invalid:
# 
# in leoFrame.py and leoNodes.py: warnings about the event param not being used. pychecker doesn't understand that these routines 
# are Tkinter callbacks.
# 
# in leoApp.py and leoUtils.py: pychecker doesn't seem to handle globals very well.  There are spurious warnings about globals.
# 
# several files: pychecker complains about several routines being "too big", i.e., pychecker doesn't understand about literate programming.
# 

#@-at
#@@c

if 0: # Set to 1 for lint-like testing.  This can also be done in idle.
	try:
		import pychecker.checker
	except: pass
#@-body
#@-node:1::<< Import pychecker >>

import leoGlobals # Can't import * here: app() is not defined yet!
import leoApp, leoFrame, leoUtils, Tkinter
import os, string, sys

app = leoGlobals.app
	

#@+others
#@+node:2::Functions for scripts
#@+body
def windows():
	return app().windowList
	
def getCommands():
	c = []
	for w in windows():
		c.append(w.commands)
		
def topCommands():
	import leoGlobals
	return leoGlobals.top()
#@-body
#@-node:2::Functions for scripts
#@+node:3::go
#@+body
# This is useful for reloading after a file has been changed.

def go(*args):

	reload_all()
	if len(args) > 0 and type(args[0]) == type(("a","b")):
		args = args[0] # Strip the outer tuple.
	run(args)
#@-body
#@-node:3::go
#@+node:4::init_sherlock
#@+body
def init_sherlock (args):
	
	leoUtils.init_trace(args)
	# leoUtils.trace("argv", "sys.argv: " + `sys.argv`)
#@-body
#@-node:4::init_sherlock
#@+node:5::open
#@+body
def open(fileName=None,*args):
	
	if fileName == None:
		run()
		return

	reload_all()

	# Create a hidden main window: this window never becomes visible!
	root = Tkinter.Tk()
	
	#@<< set the icon image >>
	#@+node:1:C=1:<< set the icon image >>
	#@+body
	if 0: # not yet
		fullname = r"c:\prog\LeoPy\Icons\box05.GIF"
		image = Tkinter.PhotoImage(file=fullname)
		trace(`image`)
		image = Tkinter.BitmapImage(image)
		trace(`image`)
		image = Tkinter.BitmapImage("stop")
		trace(`image`)
		root.iconbitmap(image)
	#@-body
	#@-node:1:C=1:<< set the icon image >>

	root.title("Leo Main Window")
	root.withdraw()
	# Initialize application globals
	app = leoApp.LeoApp(root)
	leoGlobals.setApp(app)
	app.finishCreate() # do this after gApp exists.
	# Create the first Leo window
	frame1 = leoFrame.LeoFrame()
	frame1.top.withdraw()
	# Now open the second Leo window
	fileName = os.path.join(os.getcwd(), fileName)
	fileName = os.path.normpath(fileName)
	if os.path.exists(fileName):
		ok, frame = frame1.OpenWithFileName(fileName)
	else: ok = 0
	if ok:
		app.windowList.remove(frame1)
		frame1.destroy() # force the window to go away now.
		app.log = frame # Sets the log stream for es()
	else:
		frame1.top.deiconify()
		app.log = frame1
		leoGlobals.es("File not found: " + fileName)
	init_sherlock(args)
	root.mainloop()
#@-body
#@-node:5::open
#@+node:6:C=2:reload_all
#@+body
def reload_all ():

	return ##

	modules = [ "", "App", "AtFile", "Color", "Commands", "Compare",
		"Dialog", "FileCommands", "Frame", "Find", "Globals",
		"Import", "Nodes", "Prefs", "Tangle", "Tree", "Undo", "Utils" ]
	
	print "reloading all modules"
	for m in modules:
		exec("import leo%s" % m)
		exec("reload(leo%s)" % m)
		

#@+at
#  Warning: Python version 2.2 warns if import * is done outside the module level.  Alas, for reasons that are not clear to me, it 
# appears necessary to do an import * whenever leoGlobals or leoUtils change.  The workaround is to quit Python and then reload 
# leo.py from scratch.  Sigh.

#@-at
#@@c 
	if 0: # invalid past 2.1: import * must be at the module level.
		from leoGlobals import *
		from leoUtils import *
#@-body
#@-node:6:C=2:reload_all
#@+node:7:C=3:run
#@+body
def run(*args):

	# Create a hidden main window: this window never becomes visible!
	root = Tkinter.Tk()
	
	#@<< set the icon image >>
	#@+node:1:C=1:<< set the icon image >>
	#@+body
	if 0: # not yet
		fullname = r"c:\prog\LeoPy\Icons\box05.GIF"
		image = Tkinter.PhotoImage(file=fullname)
		trace(`image`)
		image = Tkinter.BitmapImage(image)
		trace(`image`)
		image = Tkinter.BitmapImage("stop")
		trace(`image`)
		root.iconbitmap(image)
	#@-body
	#@-node:1:C=1:<< set the icon image >>

	root.title("Leo Main Window")
	root.withdraw()
	# Initialize application globals
	app = leoApp.LeoApp(root)
	leoGlobals.setApp(app)
	app.finishCreate() # do this after gApp exists.
	# Create the first Leo window
	frame = leoFrame.LeoFrame()
	frame.startupWindow = leoGlobals.true
	init_sherlock(args)
	root.mainloop()
#@-body
#@-node:7:C=3:run
#@-others


if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.platform=="win32": # Windows
			fileName = string.join(sys.argv[1:],' ')
		else:
			fileName = sys.argv[1]
		open(fileName)
	else:
		run()
#@-body
#@-node:0::@file leo.py
#@-leo
