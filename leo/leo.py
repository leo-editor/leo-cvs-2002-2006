#@+leo
#@+node:0::@file leo.py 
#@+body
#@@language python

# Top level of leo.py


#@<< Import pychecker >>
#@+node:1::<< Import pychecker >>
#@+body
#@+at
#  pychecker is extremely useful, and it sometimes reports problems 
# erroneously.  In particular, the following warnings are invalid:
# 
# in leoFrame.py and leoNodes.py: warnings about the event param not being 
# used. pychecker doesn't understand that these routines are Tkinter callbacks.
# 
# in leoApp.py and leoUtils.py: pychecker doesn't seem to handle globals very 
# well.  There are spurious warnings about globals.
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
	
topCommand = topCommands
#@-body
#@-node:2::Functions for scripts
#@+node:3::go
#@+body
# This is useful for reloading after a file has been changed.

def go(*args):

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
#@+node:5::leoOpen (leo.py)
#@+body
def leoOpen(fileName=None,*args):
	
	if fileName == None:
		run()
		return

	# Create a hidden main window: this window never becomes visible!
	root = Tkinter.Tk()
	
	#@<< set the icon image >>
	#@+node:1::<< set the icon image >>
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
	#@-node:1::<< set the icon image >>

	root.title("Leo Main Window")
	root.withdraw()
	# Initialize application globals
	app = leoApp.LeoApp(root)
	leoGlobals.setApp(app)
	if not app.finishCreate(): # do this after gApp exists.
		root.destroy()
		return
	leoGlobals.handleStartHook("start1")
	# Create the first Leo window
	frame1 = leoFrame.LeoFrame()
	frame1.top.withdraw()
	frame1.top.update()
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
		# 10/6/02: Set the file's name if it doesn't exist.
		fileName = leoUtils.ensure_extension(fileName, ".leo")
		frame1.mFileName = fileName
		frame1.title = fileName
		frame1.top.title(fileName)
	init_sherlock(args)
	leoGlobals.handleStartHook("start2")
	root.mainloop()
#@-body
#@-node:5::leoOpen (leo.py)
#@+node:6::run (leo.py)
#@+body
def run(*args):

	# Create a hidden main window: this window never becomes visible!
	root = Tkinter.Tk()
	
	#@<< set the icon image >>
	#@+node:1::<< set the icon image >>
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
	#@-node:1::<< set the icon image >>

	root.title("Leo Main Window")
	if 1:
		root.withdraw()
	else: # Works badly in Idle, not at all from the console window.
		root.deiconify()
		root.protocol("WM_DELETE_WINDOW", onKillLeoEvent)
	# Initialize application globals
	app = leoApp.LeoApp(root)
	leoGlobals.setApp(app)
	if not app.finishCreate(): # do this after gApp exists.
		root.destroy()
		return
	leoGlobals.handleStartHook("start1")
	# Create the first Leo window
	frame = leoFrame.LeoFrame()
	frame.top.deiconify() # 7/19/02
	frame.commands.redraw() # 9/1/02
	frame.startupWindow = leoGlobals.true
	init_sherlock(args)
	leoGlobals.handleStartHook("start2")
	root.mainloop()
#@-body
#@-node:6::run (leo.py)
#@+node:7::onKillLeoEvent
#@+body
# Apparently the value returned from this routine is ignored.

def onKillLeoEvent (event=None):
	
	print "onKillLeoEvent"
	import leoDialog
	d = leoDialog.leoDialog()
	answer = d.askYesNo("Save Before Shutdown?", "Save files before shutting down")
	if answer == "yes":
		print "0"
		return 0
	else:
		print "1"
		return 1
#@-body
#@-node:7::onKillLeoEvent
#@+node:8::profile
#@+body
def profile ():

	import profile, pstats
	
	name = "c:/prog/test/leoProfile.txt"
	profile.run('leo.run()',name)

	p = pstats.Stats(name)
	p.strip_dirs()
	p.sort_stats('cum','file','name')
	p.print_stats()
#@-body
#@-node:8::profile
#@-others


if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.platform=="win32": # Windows
			fileName = string.join(sys.argv[1:],' ')
		else:
			fileName = sys.argv[1]
		leoOpen(fileName)
	else:
		run()



#@-body
#@-node:0::@file leo.py 
#@-leo
