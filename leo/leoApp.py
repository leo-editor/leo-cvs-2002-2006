#@+leo

#@+node:0::@file leoApp.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *
import leo,leoConfig,leoDialog,leoFind
import os, sys, Tkinter, traceback

class LeoApp:

	#@+others
	#@+node:1:C=1:app.__init__
	#@+body
	def __init__(self, root):
	
		# These ivars are the global vars of this program.
		self.root = root # The hidden main window
		self.log = None # The LeoFrame containing the present log
		self.quitting = false # True if quitting.  Locks out some events.
		self.windowList = [] # Global list of all frames.  Does not include hidden root window.
		self.numberOfWindows = 0 # Number of opened windows.
		self.loadDir = None # The directory from which Leo was loaded.
		self.configDir = None # The directory containing configuration info.
		self.config = None # The leoConfig instance.
		self.idle_imported = false # true: we have done an import idle
		
		# Global options...
		self.trace_list = [] # "Sherlock" argument list for tracing().
		self.deleteOnClose = true # true: delete frame objects when a frame closes.
		if 0: # app() is not accessible during shutdown!
			self.printDel = false # true: enable prints in __del__ routines
	
		# Global panels.  Destroyed when Leo ends.
		self.findFrame = None
		self.pythonFrame = None
	#@-body
	#@-node:1:C=1:app.__init__
	#@+node:2:C=2:app.finishCreate
	#@+body
	# Called when the gApp global has been defined.
	
	def finishCreate(self):
	
		
		#@<< return false if not v2.2 or above >>
		#@+node:1::<< return false if not v2.2 or above >>
		#@+body
		try:
			version = sys.version
			vlist = string.split(version,".")
			v0 = int(vlist[0])
			v1 = int(vlist[1])
			v22 = v0 > 2 or (v0 == 2 and v1 > 1)
		except:
			print "exception getting version"
			traceback.print_exc()
			v22 = true # Just hope
			
		if not v22:
			d = leoDialog.leoDialog()
			d.askOk("Python version error",
		"""
		leo.py requires Python 2.2 or higher.
		
		You may download Python 2.2 from http://python.org/download/
		""",
				text="Exit")
			return false
		#@-body
		#@-node:1::<< return false if not v2.2 or above >>

		
		#@<< set loadDir >>
		#@+node:2:C=3:<< set loadDir >>
		#@+body
		# loadDir should be the directory that contains leo.py
		
		try:
			self.loadDir = os.path.dirname(leo.__file__)
		except:
			# Emergency defaults.  Hopefully we will never have to use them.
			if sys.platform=="win32": # Windows
				self.loadDir = "c:\\prog\\LeoPy\\"
			else: # Linux, or whatever.
				self.loadDir = "LeoPy"
			print "Setting load directory to:", self.loadDir
		
		# Trace hasn't been enabled yet.
		# print `self.loadDir`
		#@-body
		#@-node:2:C=3:<< set loadDir >>

		
		#@<< set the default Leo icon >>
		#@+node:3::<< set the default Leo icon >>
		#@+body
		try: # 6/2/02: Try to set the default bitmap.
			bitmap_name = os.path.join(self.loadDir,"Icons","LeoApp.ico")
			bitmap = Tkinter.BitmapImage(bitmap_name)
		except:
			print "exception creating bitmap"
			traceback.print_exc()
		
		try:
			version = self.root.getvar("tk_patchLevel")
			# print "tcl version:" + `version`
			
			#@<< set v834 if version is 8.3.4 or greater >>
			#@+node:1::<< set v834 if version is 8.3.4 or greater >>
			#@+body
			# A compare version utility would be good.
			
			# Tk version is of the form 9.9.9, or 9.9b9,
			# or 9.9.9b9.  The "9b9" form is used for beta
			# releases.  This string splitting logic handles
			# both normal and beta releases.
			vlist = string.split(version,".")
			v0 = int(vlist[0])
			vlistb = string.split(vlist[1], "b")
			v1 = int(vlistb[0])
			if len(vlist) > 2: 
				vlistb = string.split(vlist[2], "b")
				v2 = int(vlistb[0])
			else:
				v2 = 0
			
			v834 = v0 > 8 or (
				(v0 == 8 and v1 > 3) or (
				(v0 == 8 and v1 == 3 and v2 >= 4 )))
			#@-body
			#@-node:1::<< set v834 if version is 8.3.4 or greater >>

		except:
			print "exception getting version"
			traceback.print_exc()
			v834 = None # 6/18/02
			
		if v834:
			try:
				if sys.platform=="win32": # Windows
					top.wm_iconbitmap(bitmap,default=1)
				else:
					top.wm_iconbitmap(bitmap)
			except:
				if 0: # Let's ignore this for now until I understand the issues better.
					es("exception setting bitmap")
					traceback.print_exc()
		#@-body
		#@-node:3::<< set the default Leo icon >>

		self.config = leoConfig.config()
		
		# Create the global windows
		self.findFrame = leoFind.LeoFind()
		self.findFrame.top.withdraw()
		return true # all went well.
	#@-body
	#@-node:2:C=2:app.finishCreate
	#@+node:3::destroyAllGlobalWindows
	#@+body
	def destroyAllGlobalWindows (self):
	
		if self.findFrame:
			self.findFrame.top.destroy()
	#@-body
	#@-node:3::destroyAllGlobalWindows
	#@+node:4:C=4:app.quit
	#@+body
	def quit(self):
	
		# Wait until everything is quiet before really quitting.
		self.destroyAllGlobalWindows()
		if 1: # leaves Python window open.
			self.root.destroy()
		else: # closes Python window.
			self.root.quit()
	#@-body
	#@-node:4:C=4:app.quit
	#@+node:5::app.testDialogs
	#@+body
	def testDialogs (self):
	
		import leoDialog
		d = leoDialog.leoDialog()
		d.testDialogs()
	#@-body
	#@-node:5::app.testDialogs
	#@-others
#@-body
#@-node:0::@file leoApp.py
#@-leo
