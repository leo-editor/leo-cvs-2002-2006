# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoApp.py
#@@first # -*- coding: utf-8 -*-
#@@language python

from leoGlobals import *
import leoConfig,leoDialog,leoFind,leoGui,leoNodes
import locale,os,sys

class LeoApp:

	"""A class representing the Leo application itself.
	
	Ivars of this class are Leo's global variables."""
	
	#@	@+others
	#@+node:app.__init__
	def __init__(self):
	
		# These ivars are the global vars of this program.
		self.afterHandler = None
		self.commandName = None # The name of the command being executed.
		self.config = None # The leoConfig instance.
		self.globalWindows = []
		self.gui = None # The gui class.
		self.guiDispatcher = None # Class used to dispatch gui calls to proper object.
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
		self.nodeIndices = None # Singleton node indices instance.
		self.numberOfWindows = 0 # Number of opened windows.
		self.openWithFiles = [] # List of data used by Open With command.
		self.openWithFileNum = 0 # Used to generate temp file names for Open With command.
		self.openWithTable = None # The table passed to createOpenWithMenuFromTable.
		self.quitting = false # True if quitting.  Locks out some events.
		self.realMenuNameDict = {} # Contains translations of menu names and menu item names.
		self.root = None # The hidden main window. Set later.
		self.trace_list = [] # "Sherlock" argument list for tracing().
		self.tkEncoding = "utf-8" # Set by finishCreate
		self.unicodeErrorGiven = false # true: suppres unicode tracebacks.
		self.windowList = [] # Global list of all frames.  Does not include hidden root window.
	
		# Global panels.  Destroyed when Leo ends.
		self.findFrame = None
		self.pythonFrame = None
		
		#@	<< Define global constants >>
		#@+node:<< define global constants >>
		self.prolog_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		
		# New in leo.py 3.0
		self.prolog_prefix_string = "<?xml version=\"1.0\" encoding="
		self.prolog_postfix_string = "?>"
		
		# leo.py 3.11
		self.use_unicode = true # true: use new unicode logic.
		#@-node:<< define global constants >>
		#@nl
		#@	<< Define global data structures >>
		#@+node:<< define global data structures >>
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
		#@-node:<< define global data structures >>
		#@nl
	#@nonl
	#@-node:app.__init__
	#@+node:app.closeLeoWindow
	def closeLeoWindow (self,frame):
		
		"""Attempt to close a Leo window.
		
		Return false if the user veto's the close."""
		
		app = self ; c = frame.commands
	
		if c.changed:
			veto = frame.promptForSave()
			# print "veto",veto
			if veto: return false
	
		app.setLog(None) # no log until we reactive a window.
		
		doHook("close-frame",c=c) # This may remove frame from the window list.
		
		if frame in app.windowList:
			app.destroyWindow(frame)
		
		if app.windowList:
			# Pick a window to activate so we can set the log.
			w = app.windowList[0]
			w.top.deiconify()
			w.top.lift()
			app.setLog(w)
		else:
			app.finishQuit()
	
		return true # The window has been closed.
	#@-node:app.closeLeoWindow
	#@+node:app.createTkGui
	def createTkGui (self):
		
		app = self
		
		app.gui = leoGui.tkinterGui()
		app.root = app.gui.createRootWindow()
	#@nonl
	#@-node:app.createTkGui
	#@+node:app.destroyAllGlobalWindows
	def destroyAllGlobalWindows (self):
		
		for w in self.globalWindows:
			w.top.destroy()
			
		self.globalWindows = []
		
		self.findFrame = None
		self.pythonFrame = None
			
		doHook("destroy-all-global-windows")
	#@-node:app.destroyAllGlobalWindows
	#@+node:app.destroyAllOpenWithFiles
	#@+at 
	#@nonl
	# Try to remove temp files created with the Open With command.  This may 
	# fail if the files are still open.
	# 
	# We can't use es here because the log stream no longer exists.
	#@-at
	#@@c 
	
	def destroyAllOpenWithFiles (self):
		
		app = self
	
		for dict in self.openWithFiles[:]: # 7/10/03.
			app.destroyOpenWithFileWithDict(dict)
			
		# Delete the list so the gc can recycle Leo windows!
		app.openWithFiles = []
	#@nonl
	#@-node:app.destroyAllOpenWithFiles
	#@+node:app.destroyAllWindowObjects
	# Objects must not be "destroyed" more than once; only this method calls destroy routines.
	
	def destroyAllWindowObjects (self,frame):
	
		"""Clear all links to objects in a Leo window."""
		
		# print "app.destroyAllNodes", frame
		
		# Do this first.
		#@	<< clear all vnodes and tnodes in the tree >>
		#@+node:<< clear all vnodes and tnodes in the tree>>
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
		#@nonl
		#@-node:<< clear all vnodes and tnodes in the tree>>
		#@nl
		
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
	#@nonl
	#@-node:app.destroyAllWindowObjects
	#@+node:app.destroyOpenWithFilesForFrame
	def destroyOpenWithFilesForFrame (self,frame):
		
		"""Close all "Open With" files associated with frame"""
		
		app = self
		
		# Make a copy of the list: it may change in the loop.
		openWithFiles = app.openWithFiles
	
		for dict in openWithFiles[:]: # 6/30/03
			c = dict.get("c")
			if c.frame == frame:
				app.destroyOpenWithFileWithDict(dict)
	#@-node:app.destroyOpenWithFilesForFrame
	#@+node:app.destroyOpenWithFileWithDict
	def destroyOpenWithFileWithDict (self,dict):
		
		app = self
		
		path = dict.get("path")
		if path and os.path.exists(path):
			try:
				os.remove(path)
				print "deleting temp file:", shortFileName(path)
			except:
				print "can not delete temp file:", path
				
		# Remove dict from the list so the gc can recycle the Leo window!
		app.openWithFiles.remove(dict)
	#@nonl
	#@-node:app.destroyOpenWithFileWithDict
	#@+node:app.destroyWindow
	def destroyWindow (self,frame):
		
		app = self ; top = frame.top # Remember this.
			
		app.destroyOpenWithFilesForFrame(frame)
		
		# 8/27/03: Recycle only if more than one window open
		if len(app.windowList) > 1:
			app.destroyAllWindowObjects(frame)
	
		app.windowList.remove(frame)
	
		top.destroy() # force the window to go away now.
	#@nonl
	#@-node:app.destroyWindow
	#@+node:app.finishCreate
	# Called when the gApp global has been defined.
	
	def finishCreate(self):
		
		app = self
		
		# New 4.0 stuff.
		if 0: # Not using leoID.txt is more convenient for the user.
			app.setLeoID()
			app.nodeIndices = leoNodes.nodeIndices()
	#@nonl
	#@-node:app.finishCreate
	#@+node:app.finishQuit
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
	#@nonl
	#@-node:app.finishQuit
	#@+node:app.get/setRealMenuName & setRealMenuNamesFromTable
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
	#@-node:app.get/setRealMenuName & setRealMenuNamesFromTable
	#@+node:app.onQuit
	def onQuit (self):
		
		app = self
		
		app.quitting = true
		
		while app.windowList:
			w = app.windowList[0]
			if not app.closeLeoWindow(w):
				break
	
		app.quitting = false # If we get here the quit has been disabled.
	
	
	#@-node:app.onQuit
	#@+node:app.setLeoID (not used)
	def setLeoID (self):
		
		tag = ".leoID.txt"
		loadDir = app.loadDir
		configDir = app.config.configDir
		#@	<< return if we can set self.leoID from sys.leoID >>
		#@+node:<< return if we can set self.leoID from sys.leoID>>
		# This would be set by in Python's sitecustomize.py file.
		try:
			app.leoID = sys.leoID
			es("leoID = " + app.leoID, color="blue")
			return
		except:
			app.leoID = None
		#@nonl
		#@-node:<< return if we can set self.leoID from sys.leoID>>
		#@nl
		#@	<< return if we can set self.leoID from "leoID.txt" >>
		#@+node:<< return if we can set self.leoID from "leoID.txt" >>
		for dir in (configDir,loadDir):
			try:
				fn = os.path.join(dir, tag)
				f = open(fn,'r')
				if f:
					s = f.readline()
					f.close()
					if s and len(s) > 0:
						app.leoID = s
						es("leoID = " + app.leoID, color="blue")
						return
					else:
						es("empty " + tag + " in " + dir, color = "red")
			except:
				app.leoID = None
				
		if configDir == loadDir:
			es(tag + " not found in " + loadDir, color="red")
		else:
			es(tag + " not found in " + configDir + " or " + loadDir, color="red")
		
		#@-node:<< return if we can set self.leoID from "leoID.txt" >>
		#@nl
		#@	<< put up a dialog requiring a valid id >>
		#@+node:<< put up a dialog requiring a valid id >>
		app.leoID = leoDialog.askLeoID().run(modal=true)
		
		es("leoID = " + `app.leoID`, color="blue")
		#@nonl
		#@-node:<< put up a dialog requiring a valid id >>
		#@nl
		#@	<< attempt to create leoID.txt >>
		#@+node:<< attempt to create leoID.txt >>
		for dir in (configDir,loadDir):
			try:
				# Look in configDir first.
				fn = os.path.join(dir, tag)
				f = open(fn,'w')
				if f:
					f.write(app.leoID)
					f.close()
					es("created leoID.txt in " + dir, color="red")
					return
			except: pass
			
		if configDir == loadDir:
			es("can not create leoID.txt in " + loadDir, color="red")
		else:
			es("can not create leoID.txt in " + configDir + " or " + loadDir, color="red")
		
		#@-node:<< attempt to create leoID.txt >>
		#@nl
	#@nonl
	#@-node:app.setLeoID (not used)
	#@+node:app.setLog, lockLog, unlocklog
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
	#@nonl
	#@-node:app.setLog, lockLog, unlocklog
	#@+node:app.writeWaitingLog
	def writeWaitingLog (self):
	
		if self.log:
			for s,color in self.logWaiting:
				es(s,color=color,newline=0) # The caller must write the newlines.
			self.logWaiting = []
	#@-node:app.writeWaitingLog
	#@-others
#@-node:@file leoApp.py
#@-leo
