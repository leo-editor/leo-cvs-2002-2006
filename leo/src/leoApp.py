#@+leo
#@+node:0::@file leoApp.py
#@+body
#@@language python

from leoGlobals import *
import leo,leoConfig,leoDialog,leoFind
import os,sys,Tkinter

class LeoApp:

	#@+others
	#@+node:1::app.__init__
	#@+body
	def __init__(self, root):
	
		# These ivars are the global vars of this program.
		self.commandName = None # The name of the command being executed.
		self.config = None # The leoConfig instance.
		self.deleteOnClose = true # true: delete frame objects when a frame closes.
		self.hookError = false # true: suppress further calls to hooks.
		self.hookFunction = None # Application wide hook function.
		self.idle_imported = false # true: we have done an import idle
		self.idleTimeDelay = 100 # Delay in msec between calls to "idle time" hook.
		self.idleTimeHook = false # true: the global idleTimeHookHandler will reshedule itself.
		self.leoID = None # Set by setLeoID().  The id for all global node indices.
		self.loadDir = None # The directory from which Leo was loaded.
		self.log = None # The LeoFrame containing the present log.
		self.logWaiting = [] # List of messages waiting to go to a log.
		self.menuWarningsGiven = false # true: supress warnings in menu code.
		self.nodeIndices = None # Initialized in finishCreate.
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
		self.use_gnx = false # true: enable 4.x code.
		self.windowList = [] # Global list of all frames.  Does not include hidden root window.
	
		if 0: # app() is not accessible during shutdown!
			self.printDel = false # true: enable prints in __del__ routines
	
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
			"shell" : "#",  # shell scripts
			"tcltk" : "#",
			"unknown" : "#" } # Set when @comment is seen.
			
		self.language_extension_dict = {
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
			"shell" : "txt",
			"tex" : "tex",
			"tcltk" : "tcl",
			"unknown" : "txt" } # Set when @comment is seen.
		
		#@-body
		#@-node:2::<< define global data structures >>
	#@-body
	#@-node:1::app.__init__
	#@+node:2::app.destroyAllGlobalWindows
	#@+body
	def destroyAllGlobalWindows (self):
	
		if self.findFrame:
			self.findFrame.top.destroy()
	#@-body
	#@-node:2::app.destroyAllGlobalWindows
	#@+node:3::app.finishCreate
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
			if not CheckVersion(sys.version, "2.1"):
				d = leoDialog.leoDialog()
				d.askOk("Python version error",
		"""
		leo.py requires Python 2.1 or higher.
		
		You may download Python 2.1 and Python 2.2 from http://python.org/download/
		""",
					text="Exit")
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
		self.setLeoID()
		self.nodeIndices = leoNodes.nodeIndices()
		
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
		self.findFrame = leoFind.LeoFind()
		self.findFrame.top.withdraw()
		attachLeoIcon(self.findFrame.top)
		return true # all went well.
	#@-body
	#@-node:3::app.finishCreate
	#@+node:4::app.get/setRealMenuName & setRealMenuNamesFromTable
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
	#@-node:4::app.get/setRealMenuName & setRealMenuNamesFromTable
	#@+node:5::app.setLeoID
	#@+body
	def setLeoID (self):
		
		if not self.use_gnx:
			return # Used only in 4.x.
			
		tag = ".leoID.txt"
		loadDir = app().loadDir
		configDir = app().config.configDir
		
		#@<< return if we can set self.leoID from sys.leoID >>
		#@+node:1::<< return if we can set self.leoID from sys.leoID>>
		#@+body
		# This would be set by in Python's sitecustomize.py file.
		try:
			self.leoID = sys.leoID
			es("leoID = " + self.leoID, color="blue")
			return
		except:
			self.leoID = None
		#@-body
		#@-node:1::<< return if we can set self.leoID from sys.leoID>>

		
		#@<< return if we can set self.leoID from "leoID.txt" >>
		#@+node:2::<< return if we can set self.leoID from "leoID.txt" >>
		#@+body
		for dir in (configDir,loadDir):
			try:
				fn = os.path.join(dir, tag)
				f = open(fn,'r')
				if f:
					s = f.readline()
					f.close()
					if s and len(s) > 0:
						self.leoID = s
						es("leoID = " + self.leoID, color="blue")
						return
					else:
						es("empty " + tag + " in " + dir, color = "red")
			except: self.leoID = None
				
		if configDir == loadDir:
			es(tag + " not found in " + loadDir, color="red")
		else:
			es(tag + " not found in " + configDir + " or " + loadDir, color="red")
		
		#@-body
		#@-node:2::<< return if we can set self.leoID from "leoID.txt" >>

		
		#@<< put up a dialog requiring a valid id >>
		#@+node:3::<< put up a dialog requiring a valid id >>
		#@+body
		message = (
			"leoID.txt not found\n\n" +
			"Please enter an id that identifies you uniquely.\n" +
			"Your cvs login name is a good choice.\n" +
			"Your id must contain only letters and numbers\n" +
			"and must be at least 4 characters in length.")
		
		d = leoDialog.leoDialog()
		self.leoID = d.askLeoID("Enter unique id", message)
		
		es("leoID = " + `self.leoID`, color="blue")
		
		#@-body
		#@-node:3::<< put up a dialog requiring a valid id >>

		
		#@<< attempt to create leoID.txt >>
		#@+node:4::<< attempt to create leoID.txt >>
		#@+body
		for dir in (configDir,loadDir):
			try:
				# Look in configDir first.
				fn = os.path.join(dir, tag)
				f = open(fn,'w')
				if f:
					f.write(self.leoID)
					f.close()
					es("created leoID.txt in " + dir, color="red")
					return
			except: pass
			
		if configDir == loadDir:
			es("can not create leoID.txt in " + loadDir, color="red")
		else:
			es("can not create leoID.txt in " + configDir + " or " + loadDir, color="red")
		
		
		#@-body
		#@-node:4::<< attempt to create leoID.txt >>
	#@-body
	#@-node:5::app.setLeoID
	#@+node:6::app.handleOpenTempFiles
	#@+body
	#@+at
	#  Try to remove temp files created with the Open With command.  This may 
	# fail if the files are still open.
	# 
	# We can't use es here because the log stream no longer exists.

	#@-at
	#@@c 

	def handleOpenTempFiles (self):
		
		for dict in self.openWithFiles:
			path = dict.get("path")
			if path and os.path.exists(path):
				try:
					os.remove(path)
					print "deleting temp file:", shortFileName(path)
				except:
					print "can not delete temp file:", path
	#@-body
	#@-node:6::app.handleOpenTempFiles
	#@+node:7::app.quit
	#@+body
	def quit(self):
	
		# Wait until everything is quiet before really quitting.
		handleLeoHook("end1")
	
		self.destroyAllGlobalWindows()
		self.handleOpenTempFiles()
	
		if 1: # leaves Python window open.
			self.root.destroy()
		else: # closes Python window.
			self.root.quit()
	#@-body
	#@-node:7::app.quit
	#@+node:8::app.writeWaitingLog
	#@+body
	def writeWaitingLog (self):
	
		if self.log:
			for s,color in self.logWaiting:
				es(s,color=color,newline=0) # The caller must write the newlines.
			self.logWaiting = []
	
	#@-body
	#@-node:8::app.writeWaitingLog
	#@-others
#@-body
#@-node:0::@file leoApp.py
#@-leo
