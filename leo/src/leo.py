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
#@+node:2::run & allies
#@+body
def run(fileName=None,*args,**keywords):
	
	"""Initialize and run Leo"""

	app,root = doStep1() # Create app object and call app().finishCreate.
	if root:
		doHook("start1") # Load plugins before doing step 2.
		frame = doStep2(app,fileName)
		if frame:
			doStep3(app,frame,args)
			root.mainloop()

#@-body
#@+node:1::doStep1
#@+body
def doStep1 ():
	
	"""Step 1 of Leo startup process:
	
	Create a hidden Tk root window and the app object"""
	
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

	# Create the application object.
	app = leoApp.LeoApp(root)
	setApp(app)
	
	# do this after gApp exists.
	if not app.finishCreate(): 
		root.destroy()
		root = None
	
	return app,root
#@-body
#@-node:1::doStep1
#@+node:2::doStep2
#@+body
def doStep2 (app,fileName):
	
	"""Step 2 of Leo startup process:
		
	Create a frame, and optionally read a file into it"""
	
	# Create the first frame.
	frame1 = leoFrame.LeoFrame()
	
	if fileName:
		
		#@<< open frame2. return frame2 or frame1 on failure >>
		#@+node:1::<< open frame2.  return frame2 or frame1 on failure >>
		#@+body
		# Hide the first frame.
		frame1.top.withdraw()
		frame1.top.update()
		
		fileName = os.path.join(os.getcwd(), fileName)
		fileName = os.path.normpath(fileName)
		if os.path.exists(fileName):
			ok, frame2 = frame1.OpenWithFileName(fileName)
		else: ok = 0
		if ok:
			app.windowList.remove(frame1)
			frame1.destroy() # force the window to go away now.
			app.log = frame2 # Sets the log stream for es()
			return frame2
		else:
			frame1.top.deiconify()
			app.log = frame1
			es("File not found: " + fileName)
			fileName = ensure_extension(fileName, ".leo")
			frame1.mFileName = fileName
			frame1.title = fileName
			frame1.top.title(fileName)
			return frame1
		#@-body
		#@-node:1::<< open frame2.  return frame2 or frame1 on failure >>

	else:
		# Show the first frame & indicate it is the startup window.
		frame1.top.deiconify()
		frame1.startupWindow = true
		return frame1
#@-body
#@-node:2::doStep2
#@+node:3::doStep3
#@+body
def doStep3 (app,frame,args):
	
	"""Step 3 of Leo startup process:
		
	Initialize Sherlock and reddraw the screen."""
	
	# Initialze Sherlock & stats.
	init_sherlock(args)
	clear_stats()

	# Write queued output and redraw the screen.
	app.writeWaitingLog()
	doHook("start2")
	frame.commands.redraw()

#@-body
#@-node:3::doStep3
#@-node:2::run & allies
#@+node:3::profile
#@+body
#@+at
#  To gather statistics, do the following in a Python window, not idle:
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
#@-body
#@-node:3::profile
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



#@-body
#@-node:0::@file leo.py 
#@-leo
