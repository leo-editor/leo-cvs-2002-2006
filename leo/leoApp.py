#@+leo

#@+node:0::@file leoApp.py

#@+body
from leoGlobals import *
from leoUtils import *
import leo, leoFind, leoFrame, leoPrefs
import os

class LeoApp:

	#@+others

	#@+node:1:C=1:app.__init__

	#@+body
	def __init__(self, root, master=None):
	
		# These ivars are the global vars of this program.
		self.root = root # The hidden main window
		self.log = None # The LeoFrame containing the present log
		self.quitting = false # True if quitting.  Locks out some events.
		self.windowList = [] # Global list of all frames.  Does not include hidden root window.
		self.numberOfWindows = 0 # Number of opened windows.
		self.loadDir = None # The directory from which Leo was loaded.
		self.clipboard = None # A string used to cut, copy and paste trees.
		self.idle_imported = false # true: we have done an import idle
		
		# Global options...
		self.trace_list = [] # "Sherlock" argument list for tracing().
		self.deleteOnClose = true # true: delete frame objects when a frame closes.
		if 0: # app() is not accessible during shutdown!
			self.printDel = false # true: enable prints in __del__ routines
	
		# Set by finishCreate...
		self.prefsFrame = None
		self.findFrame = None
		self.pythonFrame = None
	#@-body

	#@-node:1:C=1:app.__init__

	#@+node:2:C=2:app.finishCreate

	#@+body
	# Called when the gApp global has been defined.
	
	def finishCreate(self):
	
		
	#@<< set loaddir >>

		#@+node:1:C=3:<< set loaddir >>

		#@+body
		# loaddir should be the directory that contains leo.py
		
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

		#@-node:1:C=3:<< set loaddir >>

		
		# Create the global windows
		self.findFrame = leoFind.LeoFind()
		self.findFrame.top.withdraw()
	
		self.prefsFrame = leoPrefs.LeoPrefs()
		self.prefsFrame.top.withdraw()
	#@-body

	#@-node:2:C=2:app.finishCreate

	#@+node:3::destroyAllGlobalWindows

	#@+body
	def destroyAllGlobalWindows (self):
	
		if self.findFrame:
			self.findFrame.top.destroy()
	
		if self.prefsFrame:
			self.prefsFrame.top.destroy()
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

	#@-others

#@-body

#@-node:0::@file leoApp.py

#@-leo
