#! /usr/bin/env python
#@+leo
#@+node:0::@file leo.py 
#@+body
#@@first
# Entry point for Leo in Python.


#@@language python
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
#@-body
#@-node:1::<< Import pychecker >>

from leoGlobals import *
import leoApp,leoFrame
import os,string,sys,Tkinter


#@+others
#@+node:2::go
#@+body
# This is useful for reloading after a file has been changed.

def go(*args):

	if len(args) > 0 and type(args[0]) == type(("a","b")):
		args = args[0] # Strip the outer tuple.

	run(args)
#@-body
#@-node:2::go
#@+node:3::leo.leoOpen
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
	setApp(app)
	if not app.finishCreate(): # do this after gApp exists.
		root.destroy()
		return
	doHook("start1")
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
		es("File not found: " + fileName)
		# 10/6/02: Set the file's name if it doesn't exist.
		fileName = ensure_extension(fileName, ".leo")
		frame1.mFileName = fileName
		frame1.title = fileName
		frame1.top.title(fileName)
		frame1.commands.redraw() # Bug fix: 12/12/02
		frame = frame1
	init_sherlock(args)
	clear_stats()
	issueHookWarning()
	# Write any queued output generated before a log existed.
	app.writeWaitingLog() # 2/16/03
	c = frame.commands ; v = c.currentVnode() # 2/8/03
	doHook("start2",c=c,v=v,fileName=fileName)
	root.mainloop()
#@-body
#@-node:3::leo.leoOpen
#@+node:4::leo.run
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
	root.withdraw()
	# Initialize application globals
	app = leoApp.LeoApp(root)
	setApp(app)
	if not app.finishCreate(): # do this after gApp exists.
		root.destroy()
		return
	doHook("start1")
	# Create the first Leo window
	frame = leoFrame.LeoFrame()
	frame.top.deiconify() # 7/19/02
	frame.commands.redraw() # 9/1/02
	frame.startupWindow = true
	init_sherlock(args)
	issueHookWarning()
	# Write any queued output generated before a log existed.
	app.writeWaitingLog() # 2/16/03
	doHook("start2")
	root.mainloop()
#@-body
#@-node:4::leo.run
#@+node:5::profile
#@+body
#@+at
#  To gather statistics, do the following in a Python window, not idle:
# 
# import leo
# leo.profile()  (this runs leo)
# load leoDocs.leo (it is very slow)
# quit Leo.

#@-at
#@@c

def profile ():

	import profile, pstats
	
	name = "c:/prog/test/leoProfile.txt"
	profile.run('leo.run()',name)

	p = pstats.Stats(name)
	p.strip_dirs()
	p.sort_stats('cum','file','name')
	p.print_stats()
#@-body
#@-node:5::profile
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
