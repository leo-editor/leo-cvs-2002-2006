#@+leo

#@+node:0::@file leo.py

#@+body
# Top level of leo.py

import leoGlobals # Can't import * here: app() is not defined yet!
import leoApp, leoFrame, leoUtils, Tkinter
import os, sys

app = leoGlobals.app
	

#@+others

#@+node:1::Functions for scripts

#@+body
def windows():
	return app().windowList
	
def getCommands():
	c = []
	for w in windows():
		c.append(w.commands)
		
def topCommands():
	return top() # defined in leoGlobals.
#@-body

#@-node:1::Functions for scripts

#@+node:2::go

#@+body
# This is useful for reloading after a file has been changed.

def go(*args):

	reload_all()
	if len(args) > 0 and type(args[0]) == type(("a","b")):
		args = args[0] # Strip the outer tuple.
	run(args)
#@-body

#@-node:2::go

#@+node:3::open

#@+body
def open(fileName="c:\prog\LeoPy\LeoPy.leo",*args):

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

	# Initialize "Sherlock"
	leoUtils.init_trace(args)
	# leoUtils.trace("argv", "sys.argv: " + `sys.argv`)
	root.mainloop()
#@-body

#@-node:3::open

#@+node:4:C=2:leo.run

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
	# Initialize "Sherlock"
	leoUtils.init_trace(args)
	leoUtils.trace("argv", "sys.argv: " + `sys.argv`)
	root.mainloop()
#@-body

#@-node:4:C=2:leo.run

#@+node:5::reload_all

#@+body
def reload_all ():

	mods = [ "", "App", "AtFile", "Color", "Commands", "Compare",
		"Dialog", "FileCommands", "Frame", "Find", "Globals",
		"Nodes", "Prefs", "Tangle", "Tree", "Utils" ]
	
	print "reloading all modules"
	for m in mods:
		exec("import leo%s" % m)
		exec("reload(leo%s)" % m)

	from leoGlobals import *
	from leoUtils import *
#@-body

#@-node:5::reload_all

#@-others


if __name__ == "__main__":
	run()
#@-body

#@-node:0::@file leo.py

#@-leo
