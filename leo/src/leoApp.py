# -*- coding: utf-8 -*-
#@+leo
#@+node:0::@file leoApp.py
#@+body
#@@first
#@@language python

from leoGlobals import *
import leo,leoConfig,leoDialog,leoFind
import os,sys,Tkinter

class LeoApp:

	"""A class representing the Leo application itself.
	
	Ivars of this class are Leo's global variables."""
	

	#@+others
	#@+node:1::app.__init__
	#@+body
	def __init__(self, root):
	
		# These ivars are the global vars of this program.
		self.afterHandler = None
		self.commandName = None # The name of the command being executed.
		self.config = None # The leoConfig instance.
		self.globalWindows = []
		self.hasOpenWithMenu = false # True: open with plugin has been loaded.
		self.hookError = false # true: suppress further calls to hooks.
		self.hookFunction = None # Application wide hook function.
		self.idle_imported = false # true: we have done an import idle
		self.idleTimeDelay = 100 # Delay in msec between calls to "idle time" hook.
		self.idleTimeHook = false # true: the global idleTimeHookHandler will reshedule itself.
		self.killed = false # true: we are about to destroy the root window.
		self.loadDir = None # The directory from which Leo was loaded.
		self.log = None # The LeoFrame containing the present log.
		self.logIsLocked = false # true: no changes to log are allowed.
		self.logWaiting = [] # List of messages waiting to go to a log.
		self.menuWarningsGiven = false # true: supress warnings in menu code.
		self.numberOfWindows = 0 # Number of opened windows.
		self.openWithFiles = [] # List of data used by Open With command.
		self.openWithFileNum = 0 # Used to generate temp file names for Open With command.
		self.openWithTable = None # The table passed to createOpenWithMenuFromTable.
		self.quitting = false # True if quitting.  Locks out some events.
		self.realMenuNameDict = {} # Contains translations of menu names and menu item names.
		self.root = root # The hidden main window
		self.trace_list = [] # "Sherlock" argument list for tracing().
		self.tkEncoding = "utf-8" # Set by finishCreate
		self.unicodeErrorGiven = false # true: suppres unicode tracebacks.
		self.windowList = [] # Global list of all frames.  Does not include hidden root window.
	
		# Global panels.  Destroyed when Leo ends.
		self.findFrame = None
		self.pythonFrame = None
		
		
		#@<< Define global constants >>
		#@+node:1::<< define global constants >>
		#@+body
		self.prolog_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		
		# New in leo.py 3.0
		self.prolog_prefix_string = "<?xml version=\"1.0\" encoding="
		self.prolog_postfix_string = "?>"
		
		# leo.py 3.11
		self.use_unicode = true # true: use new unicode logic.
		
		#@-body
		#@-node:1::<< define global constants >>

		
		#@<< Define global data structures >>
		#@+node:2::<< define global data structures >>
		#@+body
		# Internally, lower case is used for all language names.
		self.language_delims_dict = {
			"actionscript" : "// /* */", #jason 2003-07-03
			"c" : "// /* */", # C, C++ or objective C.
			"cweb" : "@q@ @>", # Use the "cweb hack"
			"forth" : "_\\_ _(_ _)_", # Use the "REM hack"
			"fortran" : "C",
			"fortran90" : "!",
			"html" : "<!-- -->",
			"java" : "// /* */",
			"latex" : "%",
			"pascal" : "// { }",
			"perl" : "#",
			"perlpod" : "# __=pod__ __=cut__", # 9/25/02: The perlpod hack.
			"php" : "//",
			"plain" : "#", # We must pick something.
			"python" : "#",
			"rebol" : ";", #jason 2003-07-03
			"shell" : "#",  # shell scripts
			"tcltk" : "#",
			"unknown" : "#" } # Set when @comment is seen.
			
		self.language_extension_dict = {
			"actionscript" : "as", #jason 2003-07-03
			"c" : "c", 
			"cweb" : "w",
			"forth" : "forth",
			"fortran" : "f",
			"fortran90" : "f",
			"html" : "html",
			"java" : "java",
			"latex" : "latex",
			"noweb" : "nw",
			"pascal" : "p",
			"perl" : "perl",
			"perlpod" : "perl", 
			"php" : "php",
			"plain" : "txt",
			"python" : "py",
			"rebol" : "r",  #jason 2003-07-03
			"shell" : "txt",
			"tex" : "tex",
			"tcltk" : "tcl",
			"unknown" : "txt" } # Set when @comment is seen.
		
		#@-body
		#@-node:2::<< define global data structures >>
	#@-body
	#@-node:1::app.__init__
	#@+node:2::app.closeLeoWindow
	#@+body
	def closeLeoWindow (self,frame):
		
		"""Attempt to close a Leo window.
		
		Return false if the user veto's the close."""
		
		a = self ; c = frame.commands
	
		if c.changed:
			veto = frame.promptForSave()
			# print "veto",veto
			if veto: return false
	
		app().setLog(None) # no log until we reactive a window.
		
		doHook("close-frame",c=c) # This may remove frame from the window list.
		
		if frame in a.windowList:
			a.destroyWindow(frame)
		
		if a.windowList:
			# Pick a window to activate so we can set the log.
			w = a.windowList[0]
			w.top.deiconify()
			w.top.lift()
			a.setLog(w)
		else:
			a.finishQuit()
	
		return true # The window has been closed.
	
	#@-body
	#@-node:2::app.closeLeoWindow
	#@+node:3::app.destroyAllGlobalWindows
	#@+body
	def destroyAllGlobalWindows (self):
		
		for w in self.globalWindows:
			w.top.destroy()
			
		self.globalWindows = []
		
		self.findFrame = None
		self.pythonFrame = None
			
		doHook("destroy-all-global-windows")
	
	#@-body
	#@-node:3::app.destroyAllGlobalWindows
	#@+node:4::app.destroyAllOpenWithFiles
	#@+body
	#@+at
	#  Try to remove temp files created with the Open With command.  This may 
	# fail if the files are still open.
	# 
	# We can't use es here because the log stream no longer exists.

	#@-at
	#@@c 

	def destroyAllOpenWithFiles (self):
		
		a = self
	
		for dict in self.openWithFiles[:]: # 7/10/03.
			a.destroyOpenWithFileWithDict(dict)
			
		# Delete the list so the gc can recycle Leo windows!
		a.openWithFiles = []
	#@-body
	#@-node:4::app.destroyAllOpenWithFiles
	#@+node:5::app.destroyAllWindowObjects
	#@+body
	# Objects must not be "destroyed" more than once; only this method calls destroy routines.
	
	def destroyAllWindowObjects (self,frame):
	
		"""Clear all links to objects in a Leo window."""
		
		# print "app.destroyAllNodes", frame
		
		# Do this first.
		
		#@<< clear all vnodes and tnodes in the tree >>
		#@+node:1::<< clear all vnodes and tnodes in the tree>>
		#@+body
		# Using a dict here is essential for adequate speed.
		vList = [] ; tDict = {}
		
		v = frame.commands.rootVnode()
		while v:
			vList.append(v)
			if v.t:
				key = id(v.t)
				if not tDict.has_key(key):
					tDict[key] = v.t
			v = v.threadNext()
			
		for key in tDict.keys():
			clearAllIvars(tDict[key])
		
		for v in vList:
			clearAllIvars(v)
		
		vList = [] ; tList = [] # Remove these references immediately.
		#@-body
		#@-node:1::<< clear all vnodes and tnodes in the tree>>

		
		# Destroy all subcommanders.
		clearAllIvars(frame.commands.atFileCommands)
		clearAllIvars(frame.commands.fileCommands)
		clearAllIvars(frame.commands.importCommands)
		clearAllIvars(frame.commands.tangleCommands)
		clearAllIvars(frame.commands.undoer)
		
		# Destroy the commander.
		clearAllIvars(frame.commands)
	
		clearAllIvars(frame.tree.colorizer)
		clearAllIvars(frame.tree)
		
		# Finally, destroy the frame itself.
		frame.destroyAllPanels()
		clearAllIvars(frame)
		
		# Note: pointers to frame still exist in the caller!
	#@-body
	#@-node:5::app.destroyAllWindowObjects
	#@+node:6::app.destroyOpenWithFilesForFrame
	#@+body
	def destroyOpenWithFilesForFrame (self,frame):
		
		"""Close all "Open With" files associated with frame"""
		
		a = self
		
		# Make a copy of the list: it may change in the loop.
		openWithFiles = a.openWithFiles
	
		for dict in openWithFiles[:]: # 6/30/03
			c = dict.get("c")
			if c.frame == frame:
				a.destroyOpenWithFileWithDict(dict)
	
	#@-body
	#@-node:6::app.destroyOpenWithFilesForFrame
	#@+node:7::app.destroyOpenWithFileWithDict
	#@+body
	def destroyOpenWithFileWithDict (self,dict):
		
		a = self
		
		path = dict.get("path")
		if path and os.path.exists(path):
			try:
				os.remove(path)
				print "deleting temp file:", shortFileName(path)
			except:
				print "can not delete temp file:", path
				
		# Remove dict from the list so the gc can recycle the Leo window!
		a.openWithFiles.remove(dict)
	#@-body
	#@-node:7::app.destroyOpenWithFileWithDict
	#@+node:8::app.destroyWindow
	#@+body
	def destroyWindow (self,frame):
		
		a = self
		top = frame.top # Remember this.
			
		a.destroyOpenWithFilesForFrame(frame)
		
		# 8/27/03: Recycle only if more than one window open
		if len(a.windowList) > 1:
			a.destroyAllWindowObjects(frame)
	
		a.windowList.remove(frame)
	
		top.destroy() # force the window to go away now.
	#@-body
	#@-node:8::app.destroyWindow
	#@+node:9::app.finishCreate
	#@+body
	# Called when the gApp global has been defined.
	
	def finishCreate(self):
	
		import locale,sys
		import leoNodes
		
		#@<< return false if not v2.1 or above >>
		#@+node:1::<< return false if not v2.1 or above >>
		#@+body
		# Python 2.1 support.
		
		try:
			# 04-SEP-2002 DHEIN: simplify version check
			message = """
		leo.py requires Python 2.1 or higher.
		
		You may download Python 2.1 and Python 2.2 from http://python.org/download/
		"""
		
			if not CheckVersion(sys.version, "2.1"):
				leoDialog.askOk("Python version error",message=message,text="Exit").run(modal=true)
				return false
		except:
			print "exception getting version"
			import traceback
			traceback.print_exc()
		#@-body
		#@-node:1::<< return false if not v2.1 or above >>

		
		#@<< set loadDir >>
		#@+node:2::<< set loadDir >>
		#@+body
		# loadDir should be the directory that contains leo.py
		
		try:
			self.loadDir = os.path.dirname(leo.__file__)
			if self.loadDir in (None,""):
				self.loadDir = os.getcwd()
			self.loadDir = os.path.abspath(self.loadDir)
		except:
			# Emergency defaults.  Hopefully we will never have to use them.
			if sys.platform=="win32": # Windows
				self.loadDir = "c:\\prog\\LeoPy\\"
			else: # Linux, or whatever.
				self.loadDir = "LeoPy"
			print "Setting load directory to:", self.loadDir
		
		#@-body
		#@-node:2::<< set loadDir >>

		
		#@<< set the default Leo icon >>
		#@+node:3::<< set the default Leo icon >>
		#@+body
		try: # 6/2/02: Try to set the default bitmap.
			bitmap_name = os.path.join(self.loadDir,"..","Icons","LeoApp.ico")
			bitmap = Tkinter.BitmapImage(bitmap_name)
		except:
			print "exception creating bitmap"
			import traceback
			traceback.print_exc()
		
		try:
			version = self.root.getvar("tk_patchLevel")
			# print "tcl version:", version
			
			#@<< set v834 if version is 8.3.4 or greater >>
			#@+node:1::<< set v834 if version is 8.3.4 or greater >>
			#@+body
			# 04-SEP-2002 DHEIN: simplify version check
			# 04-SEP-2002 Stephen P. Schaefer: make sure v834 is set
			v834 = CheckVersion(version, "8.3.4")
			
			#@-body
			#@-node:1::<< set v834 if version is 8.3.4 or greater >>

		except:
			print "exception getting version"
			import traceback
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
					es_exception()
		#@-body
		#@-node:3::<< set the default Leo icon >>

		self.config = leoConfig.config()
		
		#@<< set app.tkEncoding >>
		#@+node:4::<< set app.tkEncoding >>
		#@+body
		#@+at
		#  According to Martin v. Löwis, getdefaultlocale() is broken, and 
		# cannot be fixed. The workaround is to copy the 
		# getpreferredencoding() function from locale.py in Python 2.3a2.  
		# This function is now in leoGlobals.py.

		#@-at
		#@@c

		for (encoding,src) in (
			(self.config.tkEncoding,"config"),
			#(locale.getdefaultlocale()[1],"locale"),
			(getpreferredencoding(),"locale"),
			(sys.getdefaultencoding(),"sys"),
			("utf-8","default")):
		
			if isValidEncoding (encoding): # 3/22/03
				self.tkEncoding = encoding
				# print self.tkEncoding,src
				break
			elif encoding and len(encoding) > 0:
				print "ignoring invalid " + src + " encoding: " + `encoding`
		
		
		#@-body
		#@-node:4::<< set app.tkEncoding >>

	
		# Create the global windows
		self.findFrame = leoFind.leoFind()
		self.findFrame.top.withdraw()
		self.globalWindows.append(self.findFrame)
	
		return true # all went well.
	#@-body
	#@-node:9::app.finishCreate
	#@+node:10::app.finishQuit
	#@+body
	def finishQuit(self):
		
		self.killed = true # Disable after events.
		
		if self.afterHandler != None:
			# print "finishQuit: cancelling",self.afterHandler
			self.root.after_cancel(self.afterHandler)
			self.afterHandler = None
	
		# Wait until everything is quiet before really quitting.
		doHook("end1")
	
		self.destroyAllGlobalWindows()
		
		self.destroyAllOpenWithFiles()
	
		if 0: # Works in Python 2.1 and 2.2.  Leaves Python window open.
			self.root.destroy()
			
		else: # Works in Python 2.3.  Closes Python window.
			self.root.quit()
	#@-body
	#@-node:10::app.finishQuit
	#@+node:11::app.get/setRealMenuName & setRealMenuNamesFromTable
	#@+body
	# Returns the translation of a menu name or an item name.
	
	def getRealMenuName (self,menuName):
		
		cmn = canonicalizeTranslatedMenuName(menuName)
		return self.realMenuNameDict.get(cmn,menuName)
		
	def setRealMenuName (self,untrans,trans):
		
		cmn = canonicalizeTranslatedMenuName(untrans)
		self.realMenuNameDict[cmn] = trans
	
	def setRealMenuNamesFromTable (self,table):
	
		for untrans,trans in table:
			self.setRealMenuName(untrans,trans)
	
	#@-body
	#@-node:11::app.get/setRealMenuName & setRealMenuNamesFromTable
	#@+node:12::app.onQuit
	#@+body
	def onQuit (self):
		
		a = self
		
		a.quitting = true
		
		while a.windowList:
			w = a.windowList[0]
			if not a.closeLeoWindow(w):
				break
	
		a.quitting = false # If we get here the quit has been disabled.
	
	
	
	#@-body
	#@-node:12::app.onQuit
	#@+node:13::app.setLog, lockLog, unlocklog
	#@+body
	def setLog (self,log,tag=""):
		"""set the frame to which log messages will go"""
		
		# print "setLog:",tag,"locked:",self.logIsLocked,`log`
		if not self.logIsLocked:
			self.log = log
			
	def lockLog(self):
		"""Disable changes to the log"""
		self.logIsLocked = true
		
	def unlockLog(self):
		"""Enable changes to the log"""
		self.logIsLocked = false
	#@-body
	#@-node:13::app.setLog, lockLog, unlocklog
	#@+node:14::app.writeWaitingLog
	#@+body
	def writeWaitingLog (self):
	
		if self.log:
			for s,color in self.logWaiting:
				es(s,color=color,newline=0) # The caller must write the newlines.
			self.logWaiting = []
	
	#@-body
	#@-node:14::app.writeWaitingLog
	#@-others


#@-body
#@-node:0::@file leoApp.py
#@-leo
