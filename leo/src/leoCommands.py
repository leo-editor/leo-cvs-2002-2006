#@+leo-ver=4
#@+node:@file leoCommands.py
#@@language python

from leoGlobals import *

import leoAtFile,leoFileCommands,leoImport,leoNodes,leoTangle,leoUndo
import tempfile

class baseCommands:
	"""The base class for Leo's main commander."""
	#@	@+others
	#@+node:c.__init__, initIvars
	def __init__(self,frame,fileName):
		
		# trace("Commands",fileName)
	
		self.frame = frame
		self.mFileName = fileName
		self.initIvars()
	
		# initialize the sub-commanders
		self.fileCommands = leoFileCommands.fileCommands(self)
		self.atFileCommands = leoAtFile.atFile(self)
		self.importCommands = leoImport.leoImportCommands(self)
		self.tangleCommands = leoTangle.tangleCommands(self)
		self.undoer = leoUndo.undoer(self)
	
	def initIvars(self):
	
		#@	<< initialize ivars >>
		#@+node:<< initialize ivars >>
		# per-document info...
		self.hookFunction = None
		self.openDirectory = None # 7/2/02
		
		self.expansionLevel = 0  # The expansion level of this outline.
		self.expansionNode = None # The last node we expanded or contracted.
		self.changed = false # true if any data has been changed since the last save.
		self.loading = false # true if we are loading a file: disables c.setChanged()
		self.outlineToNowebDefaultFileName = "noweb.nw" # For Outline To Noweb dialog.
		
		# For tangle/untangle
		self.tangle_errrors = 0
		
		# Global options
		self.page_width = 132
		self.tab_width = 4
		self.tangle_batch_flag = false
		self.untangle_batch_flag = false
		# Default Tangle options
		self.tangle_directory = ""
		self.use_header_flag = false
		self.output_doc_flag = false
		# Default Target Language
		self.target_language = "python" # 8/11/02: Required if leoConfig.txt does not exist.
		
		# These are defined here, and updated by the tree.select()
		self.beadList = [] # list of vnodes for the Back and Forward commands.
		self.beadPointer = -1 # present item in the list.
		self.visitedList = [] # list of vnodes for the Nodes dialog.
		
		# 4.1: for hoist/dehoist commands.
		self.hoistStack = [] # Stack of nodes to be root of drawn tree.  Affects only drawing routines.
		
		self.recentFiles = [] # 4.1: moved to commands class.  List of recent files
		#@nonl
		#@-node:<< initialize ivars >>
		#@nl
		self.setIvarsFromFind()
	#@nonl
	#@-node:c.__init__, initIvars
	#@+node:c.__repr__ & __str__
	def __repr__ (self):
		
		try:
			return "Commander: " + self.mFileName
		except:
			return "Commander: bad mFileName"
			
	__str__ = __repr__
	#@-node:c.__repr__ & __str__
	#@+node:c.setIvarsFromFind
	# This should be called whenever we need to use find values:
	# i.e., before reading or writing
	
	def setIvarsFromFind (self):
	
		c = self ; find = app.findFrame
		if find != None:
			find.set_ivars(c)
	#@-node:c.setIvarsFromFind
	#@+node:c.setIvarsFromPrefs
	#@+at 
	#@nonl
	# This should be called whenever we need to use preference:
	# i.e., before reading, writing, tangling, untangling.
	# 
	# 7/2/02: We no longer need this now that the Prefs dialog is modal.
	#@-at
	#@@c
	
	def setIvarsFromPrefs (self):
	
		pass
	#@nonl
	#@-node:c.setIvarsFromPrefs
	#@+node: doCommand
	def doCommand (self,command,label,event=None):
	
		"""Execute the given command, invoking hooks and catching exceptions.
		
		The code assumes that the "command1" hook has completely handled the command if
		doHook("command1") returns false.
		This provides a simple mechanism for overriding commands."""
		
		c = self ; v = c.currentVnode()
	
		# A horrible kludge: set app.log to cover for a possibly missing activate event.
		app.setLog(c.frame.log,"doCommand")
	
		if label == "cantredo": label = "redo"
		if label == "cantundo": label = "undo"
		app.commandName = label
	
		if not doHook("command1",c=c,v=v,label=label):
			try:
				command()
			except:
				es("exception executing command")
				print "exception executing command"
				es_exception(c=c)
				c.redraw() # 11/23/03
		
		doHook("command2",c=c,v=v,label=label)
				
		return "break" # Inhibit all other handlers.
	#@nonl
	#@-node: doCommand
	#@+node: version & signon stuff
	def getBuildNumber(self):
		c = self
		return c.ver[10:-1] # Strip off "(dollar)Revision" and the trailing "$"
	
	def getSignOnLine (self):
		c = self
		return "Leo 4.1 rc3, build %s, December 19, 2003" % c.getBuildNumber()
		
	def initVersion (self):
		c = self
		c.ver = "$Revision$" # CVS will update this.
		
	def signOnWithVersion (self):
	
		c = self
		color = app.config.getWindowPref("log_error_color")
		signon = c.getSignOnLine()
		n1,n2,n3,junk,junk=sys.version_info
		tkLevel = c.frame.top.getvar("tk_patchLevel")
		
		es("Leo Log Window...",color=color)
		es(signon)
		es("Python %d.%d.%d, Tk %s, %s" % (n1,n2,n3,tkLevel,sys.platform))
		enl()
	#@nonl
	#@-node: version & signon stuff
	#@+node:new
	def new (self):
	
		c,frame = app.gui.newLeoCommanderAndFrame(fileName=None)
		
		# 5/16/03: Needed for hooks.
		doHook("new",old_c=self,new_c=c)
		
		# Use the config params to set the size and location of the window.
		frame.setInitialWindowGeometry()
		frame.deiconify()
		frame.lift()
		frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio) # Resize the _new_ frame.
		
		c.beginUpdate()
		if 1: # within update
			t = leoNodes.tnode()
			v = leoNodes.vnode(c,t)
			v.initHeadString("NewHeadline")
			v.moveToRoot()
			c.editVnode(v)
		c.endUpdate()
	
		frame.body.setFocus()
	#@nonl
	#@-node:new
	#@+node:open
	def open(self):
	
		c = self
		#@	<< Set closeFlag if the only open window is empty >>
		#@+node:<< Set closeFlag if the only open window is empty >>
		#@+at 
		#@nonl
		# If this is the only open window was opened when the app started, and 
		# the window has never been written to or saved, then we will 
		# automatically close that window if this open command completes 
		# successfully.
		#@-at
		#@@c
			
		closeFlag = (
			c.frame.startupWindow==true and # The window was open on startup
			c.changed==false and c.frame.saved==false and # The window has never been changed
			app.numberOfWindows == 1) # Only one untitled window has ever been opened
		#@-node:<< Set closeFlag if the only open window is empty >>
		#@nl
	
		fileName = app.gui.runOpenFileDialog(
			title="Open",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if fileName and len(fileName) > 0:
			ok, frame = openWithFileName(fileName,c)
			if ok and closeFlag:
				app.destroyWindow(c.frame)
	#@nonl
	#@-node:open
	#@+node:openWith and allies
	def openWith(self,data=None):
	
		"""This routine handles the items in the Open With... menu.
	
		These items can only be created by createOpenWithMenuFromTable().
		Typically this would be done from the "open2" hook."""
		
		c = self ; v = c.currentVnode()
		if not data or len(data) != 3: return # 6/22/03
		try:
			openType,arg,ext=data
			if not doHook("openwith1",c=c,v=v,openType=openType,arg=arg,ext=ext):
				#@			<< set ext based on the present language >>
				#@+node:<< set ext based on the present language >>
				if not ext:
					dict = scanDirectives(c)
					language = dict.get("language")
					ext = app.language_extension_dict.get(language)
					# print language,ext
					if ext == None:
						ext = "txt"
					
				if ext[0] != ".":
					ext = "."+ext
					
				# print "ext",`ext`
				#@nonl
				#@-node:<< set ext based on the present language >>
				#@nl
				#@			<< create or reopen temp file, testing for conflicting changes >>
				#@+node:<< create or reopen temp file, testing for conflicting changes >>
				dict = None ; path = None
				#@<< set dict and path if a temp file already refers to v.t >>
				#@+node:<<set dict and path if a temp file already refers to v.t >>
				searchPath = c.openWithTempFilePath(v,ext)
				
				if os_path_exists(searchPath):
					for dict in app.openWithFiles:
						if v.t == dict.get("v") and searchPath == dict.get("path"):
							path = searchPath
							break
				#@-node:<<set dict and path if a temp file already refers to v.t >>
				#@nl
				if path:
					#@	<< create or recreate temp file as needed >>
					#@+node:<< create or recreate temp file as needed >>
					#@+at 
					#@nonl
					# We test for changes in both v and the temp file:
					# 
					# - If only v's body text has changed, we recreate the 
					# temp file.
					# - If only the temp file has changed, do nothing here.
					# - If both have changed we must prompt the user to see 
					# which code to use.
					#@-at
					#@@c
					
					encoding = dict.get("encoding")
					old_body = dict.get("body")
					new_body = v.bodyString()
					new_body = toEncodedString(new_body,encoding,reportErrors=true)
					
					old_time = dict.get("time")
					try:
						new_time = os_path_getmtime(path)
					except:
						new_time = None
						
					body_changed = old_body != new_body
					temp_changed = old_time != new_time
					
					if body_changed and temp_changed:
						#@	<< Raise dialog about conflict and set result >>
						#@+node:<< Raise dialog about conflict and set result >>
						message = (
							"Conflicting changes in outline and temp file\n\n" +
							"Do you want to use the code in the outline or the temp file?\n\n")
						
						result = app.gui.runAskYesNoCancelDialog(
							"Conflict!", message,
							yesMessage = "Outline",
							noMessage = "File",
							defaultButton = "Cancel")
						#@nonl
						#@-node:<< Raise dialog about conflict and set result >>
						#@nl
						if result == "cancel": return
						rewrite = result == "outline"
					else:
						rewrite = body_changed
							
					if rewrite:
						path = c.createOpenWithTempFile(v,ext)
					else:
						es("reopening: " + shortFileName(path),color="blue")
					#@nonl
					#@-node:<< create or recreate temp file as needed >>
					#@nl
				else:
					path = c.createOpenWithTempFile(v,ext)
				
				if not path:
					return # An error has occured.
				#@nonl
				#@-node:<< create or reopen temp file, testing for conflicting changes >>
				#@nl
				#@			<< execute a command to open path in external editor >>
				#@+node:<< execute a command to open path in external editor >>
				try:
					if arg == None: arg = ""
					shortPath = path # shortFileName(path)
					if openType == "os.system":
						command  = "os.system("+arg+shortPath+")"
						os.system(arg+path)
					elif openType == "os.startfile":
						command    = "os.startfile("+arg+shortPath+")"
						os.startfile(arg+path)
					elif openType == "exec":
						command    = "exec("+arg+shortPath+")"
						exec arg+path in {} # 12/11/02
					elif openType == "os.spawnl":
						filename = os_path_basename(arg)
						command = "os.spawnl("+arg+","+filename+','+ shortPath+")"
						apply(os.spawnl,(os.P_NOWAIT,arg,filename,path))
					elif openType == "os.spawnv":
						filename = os_path_basename(arg)
						command = "os.spawnv("+arg+",("+filename+','+ shortPath+"))"
						apply(os.spawnl,(os.P_NOWAIT,arg,(filename,path)))
					else:
						command="bad command:"+str(openType)
					# This seems a bit redundant.
					# es(command)
				except:
					es("exception executing: "+command)
					es_exception()
				#@nonl
				#@-node:<< execute a command to open path in external editor >>
				#@nl
			doHook("openwith2",c=c,v=v,openType=openType,arg=arg,ext=ext)
		except:
			es("exception in openWith")
			es_exception()
	
		return "break"
	#@nonl
	#@-node:openWith and allies
	#@+node:createOpenWithTempFile
	def createOpenWithTempFile (self, v, ext):
		
		c = self
		path = c.openWithTempFilePath(v,ext)
		try:
			if os_path_exists(path):
				es("recreating:  " + shortFileName(path),color="red")
			else:
				es("creating:  " + shortFileName(path),color="blue")
			file = open(path,"w")
			# 3/7/03: convert s to whatever encoding is in effect.
			s = v.bodyString()
			dict = scanDirectives(c,v=v)
			encoding = dict.get("encoding",None)
			if encoding == None:
				encoding = app.config.default_derived_file_encoding
			s = toEncodedString(s,encoding,reportErrors=true) 
			file.write(s)
			file.flush()
			file.close()
			try:    time = os_path_getmtime(path)
			except: time = None
			# es("time: " + str(time))
			# 4/22/03: add body and encoding entries to dict for later comparisons.
			dict = {"body":s, "c":c, "encoding":encoding, "f":file, "path":path, "time":time, "v":v}
			#@		<< remove previous entry from app.openWithFiles if it exists >>
			#@+node:<< remove previous entry from app.openWithFiles if it exists >>
			for d in app.openWithFiles[:]: # 6/30/03
				v2 = d.get("v")
				if v.t == v2.t:
					print "removing previous entry in app.openWithFiles for",v
					app.openWithFiles.remove(d)
			#@nonl
			#@-node:<< remove previous entry from app.openWithFiles if it exists >>
			#@afterref
 # 4/22/03
			app.openWithFiles.append(dict)
			return path
		except:
			file = None
			es("exception creating temp file",color="red")
			es_exception()
			return None
	#@nonl
	#@-node:createOpenWithTempFile
	#@+node:openWithTempFilePath
	def openWithTempFilePath (self,v,ext):
		
		"""Return the path to the temp file corresponding to v and ext."""
	
		name = "LeoTemp_" + str(id(v.t)) + '_' + sanitize_filename(v.headString()) + ext
		name = toUnicode(name,app.tkEncoding) # 10/20/03
	
		td = os_path_abspath(tempfile.gettempdir())
		path = os_path_join(td,name)
		
		# print "openWithTempFilePath",path
		return path
	#@nonl
	#@-node:openWithTempFilePath
	#@+node:close
	def close(self):
		
		"""Handle the File-Close command."""
	
		app.closeLeoWindow(self.frame)
	#@nonl
	#@-node:close
	#@+node:save
	def save(self):
	
		c = self
		
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			c.frame.title = ""
			c.mFileName = ""
	
		if c.mFileName != "":
			c.fileCommands.save(c.mFileName)
			c.setChanged(false)
			return
	
		fileName = app.gui.runSaveFileDialog(
			initialfile = c.mFileName,
			title="Save",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if fileName:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			c.mFileName = ensure_extension(fileName, ".leo")
			c.frame.title = c.mFileName
			c.frame.setTitle(computeWindowTitle(c.mFileName))
			c.fileCommands.save(c.mFileName)
			c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:save
	#@+node:saveAs
	def saveAs(self):
		
		c = self
	
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			c.frame.title = ""
	
		fileName = app.gui.runSaveFileDialog(
			initialfile = c.mFileName,
			title="Save As",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if fileName:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			c.mFileName = ensure_extension(fileName, ".leo")
			c.frame.title = c.mFileName
			c.frame.setTitle(computeWindowTitle(c.mFileName))
			c.fileCommands.saveAs(c.mFileName)
			c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:saveAs
	#@+node:saveTo
	def saveTo(self):
		
		c = self
	
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			c.frame.title = ""
	
		# set local fileName, _not_ c.mFileName
		fileName = app.gui.runSaveFileDialog(
			initialfile = c.mFileName,
			title="Save To",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if fileName:
			fileName = ensure_extension(fileName, ".leo")
			c.fileCommands.saveTo(fileName)
			c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:saveTo
	#@+node:revert
	def revert(self):
		
		c = self
	
		# Make sure the user wants to Revert.
		if not c.mFileName:
			return
			
		reply = app.gui.runAskYesNoDialog("Revert",
			"Revert to previous version of " + c.mFileName + "?")
	
		if reply=="no":
			return
	
		# Kludge: rename this frame so openWithFileName won't think it is open.
		fileName = c.mFileName ; c.mFileName = ""
	
		# Create a new frame before deleting this frame.
		ok, frame = openWithFileName(fileName,c)
		if ok:
			frame.deiconify()
			app.destroyWindow(c.frame)
		else:
			c.mFileName = fileName
	#@-node:revert
	#@+node:clearRecentFiles
	def clearRecentFiles (self):
		
		"""Clear the recent files list, then add the present file."""
	
		c = self ; f = c.frame
		
		recentFilesMenu = f.menu.getMenu("Recent Files...")
		f.menu.delete_range(recentFilesMenu,0,len(c.recentFiles))
		
		c.recentFiles = []
		f.menu.createRecentFilesMenuItems()
		c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:clearRecentFiles
	#@+node:openRecentFile
	def openRecentFile(self,name=None):
		
		if not name: return
	
		c = self ; v = c.currentVnode()
		#@	<< Set closeFlag if the only open window is empty >>
		#@+node:<< Set closeFlag if the only open window is empty >>
		#@+at 
		#@nonl
		# If this is the only open window was opened when the app started, and 
		# the window has never been written to or saved, then we will 
		# automatically close that window if this open command completes 
		# successfully.
		#@-at
		#@@c
			
		closeFlag = (
			c.frame.startupWindow==true and # The window was open on startup
			c.changed==false and c.frame.saved==false and # The window has never been changed
			app.numberOfWindows == 1) # Only one untitled window has ever been opened
		#@nonl
		#@-node:<< Set closeFlag if the only open window is empty >>
		#@nl
		
		fileName = name
		if not doHook("recentfiles1",c=c,v=v,fileName=fileName,closeFlag=closeFlag):
			ok, frame = openWithFileName(fileName,c)
			if ok and closeFlag:
				app.destroyWindow(c.frame) # 12/12/03
				app.setLog(frame.log,"openRecentFile") # Sets the log stream for es()
	
		doHook("recentfiles2",c=c,v=v,fileName=fileName,closeFlag=closeFlag)
	#@nonl
	#@-node:openRecentFile
	#@+node:updateRecentFiles
	def updateRecentFiles (self,fileName):
		
		"""Create the RecentFiles menu.  May be called with Null fileName."""
		
		# trace(fileName)
		
		# Update the recent files list in all windows.
		if fileName:
			normFileName = os_path_norm(fileName)
			for frame in app.windowList:
				c = frame.c
				# Remove all versions of the file name.
				for name in c.recentFiles:
					if normFileName == os_path_norm(name):
						c.recentFiles.remove(name)
				c.recentFiles.insert(0,fileName)
				# Recreate the Recent Files menu.
				frame.menu.createRecentFilesMenuItems()
		else: # 12/01/03
			for frame in app.windowList:
				frame.menu.createRecentFilesMenuItems()
			
		# Update the config file.
		app.config.setRecentFiles(self.recentFiles) # Use self, _not_ c.
		app.config.update()
	#@nonl
	#@-node:updateRecentFiles
	#@+node:readOutlineOnly
	def readOutlineOnly (self):
	
		fileName = app.gui.runOpenFileDialog(
			title="Read Outline Only",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if not fileName:
			return
	
		try:
			file = open(fileName,'r')
			c,frame = app.gui.newLeoCommanderAndFrame(fileName)
			frame.deiconify()
			frame.lift()
			app.root.update() # Force a screen redraw immediately.
			c.fileCommands.readOutlineOnly(file,fileName) # closes file.
		except:
			es("can not open:" + fileName)
	#@nonl
	#@-node:readOutlineOnly
	#@+node:readAtFileNodes
	def readAtFileNodes (self):
	
		c = self ; v = c.currentVnode()
	
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = c.frame.body.getAllText()
		oldSel = c.frame.body.getTextSelection()
	
		c.fileCommands.readAtFileNodes()
	
		newText = c.frame.body.getAllText()
		newSel = c.frame.body.getTextSelection()
	
		c.undoer.setUndoParams("Read @file Nodes",
			v,select=v,oldTree=v_copy,
			oldText=oldText,newText=newText,
			oldSel=oldSel,newSel=newSel)
	#@nonl
	#@-node:readAtFileNodes
	#@+node:importDerivedFile
	def importDerivedFile (self):
		
		"""Create a new outline from a 4.0 derived file."""
		
		c = self ; frame = c.frame ; v = c.currentVnode()
		
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
		
		fileName = app.gui.runOpenFileDialog(
			title="Import Derived File",
			filetypes=types,
			defaultextension=".leo")
	
		if fileName:
			c.importCommands.importDerivedFiles(v,fileName)
		
		if 0: # old code: very non-intuitive.
			if v.isAtFileNode():
				fileName = v.atFileNodeName()
				c.importCommands.importDerivedFiles(v,fileName)
			else:
				es("not an @file node",color="blue")
	#@nonl
	#@-node:importDerivedFile
	#@+node:writeNew/OldDerivedFiles
	def writeNewDerivedFiles (self):
		
		c = self
		c.atFileCommands.writeNewDerivedFiles()
		es("auto-saving outline",color="blue")
		c.save() # Must be done to preserve tnodeList.
		
	def writeOldDerivedFiles (self):
		
		c = self
		c.atFileCommands.writeOldDerivedFiles()
		es("auto-saving outline",color="blue")
		c.save() # Must be done to clear tnodeList.
	#@nonl
	#@-node:writeNew/OldDerivedFiles
	#@+node:tangleAll
	def tangleAll(self):
		
		c = self
		c.tangleCommands.tangleAll()
	#@-node:tangleAll
	#@+node:tangleMarked
	def tangleMarked(self):
	
		c = self
		c.tangleCommands.tangleMarked()
	#@-node:tangleMarked
	#@+node:tangle
	def tangle (self):
	
		c = self
		c.tangleCommands.tangle()
	#@nonl
	#@-node:tangle
	#@+node:untangleAll
	def untangleAll(self):
	
		c = self
		c.tangleCommands.untangleAll()
		c.undoer.clearUndoState()
	#@-node:untangleAll
	#@+node:untangleMarked
	def untangleMarked(self):
	
		c = self
		c.tangleCommands.untangleMarked()
		c.undoer.clearUndoState()
	#@-node:untangleMarked
	#@+node:untangle
	def untangle(self):
	
		c = self
		c.tangleCommands.untangle()
		c.undoer.clearUndoState()
	#@-node:untangle
	#@+node:exportHeadlines
	def exportHeadlines (self):
		
		c = self
	
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = app.gui.runSaveFileDialog(
			initialfile="headlines.txt",
			title="Export Headlines",
			filetypes=filetypes,
			defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c.importCommands.exportHeadlines(fileName)
	
	#@-node:exportHeadlines
	#@+node:flattenOutline
	def flattenOutline (self):
		
		c = self
	
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = app.gui.runSaveFileDialog(
			initialfile="flat.txt",
			title="Flatten Outline",
			filetypes=filetypes,
			defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c.importCommands.flattenOutline(fileName)
	
	#@-node:flattenOutline
	#@+node:importAtRoot
	def importAtRoot (self):
		
		c = self
		
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
	
		fileName = app.gui.runOpenFileDialog(
			title="Import To @root",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFilesCommand (paths,"@root")
	
	#@-node:importAtRoot
	#@+node:importAtFile
	def importAtFile (self):
		
		c = self
	
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
	
		fileName = app.gui.runOpenFileDialog(
			title="Import To @file",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFilesCommand (paths,"@file")
	#@nonl
	#@-node:importAtFile
	#@+node:importCWEBFiles
	def importCWEBFiles (self):
		
		c = self
		
		filetypes = [
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = app.gui.runOpenFileDialog(
			title="Import CWEB Files",
			filetypes=filetypes,
			defaultextension=".w")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importWebCommand(paths,"cweb")
	#@-node:importCWEBFiles
	#@+node:importFlattenedOutline
	def importFlattenedOutline (self):
		
		c = self
		
		types = [("Text files","*.txt"), ("All files","*")]
	
		fileName = app.gui.runOpenFileDialog(
			title="Import MORE Text",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFlattenedOutline(paths)
	#@-node:importFlattenedOutline
	#@+node:importNowebFiles
	def importNowebFiles (self):
		
		c = self
	
		filetypes = [
			("Noweb files", "*.nw"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = app.gui.runOpenFileDialog(
			title="Import Noweb Files",
			filetypes=filetypes,
			defaultextension=".nw")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importWebCommand(paths,"noweb")
	
	#@-node:importNowebFiles
	#@+node:outlineToCWEB
	def outlineToCWEB (self):
		
		c = self
	
		filetypes=[
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = app.gui.runSaveFileDialog(
			initialfile="cweb.w",
			title="Outline To CWEB",
			filetypes=filetypes,
			defaultextension=".w")
	
		if fileName and len(fileName) > 0:
			c.importCommands.outlineToWeb(fileName,"cweb")
	
	#@-node:outlineToCWEB
	#@+node:outlineToNoweb
	def outlineToNoweb (self):
		
		c = self
		
		filetypes=[
			("Noweb files", "*.nw"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = app.gui.runSaveFileDialog(
			initialfile=self.outlineToNowebDefaultFileName,
			title="Outline To Noweb",
			filetypes=filetypes,
			defaultextension=".nw")
	
		if fileName and len(fileName) > 0:
			c.importCommands.outlineToWeb(fileName,"noweb")
			c.outlineToNowebDefaultFileName = fileName
	
	#@-node:outlineToNoweb
	#@+node:removeSentinels
	def removeSentinels (self):
		
		c = self
		
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
	
		fileName = app.gui.runOpenFileDialog(
			title="Remove Sentinels",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			# alas, askopenfilename returns only a single name.
			c.importCommands.removeSentinelsCommand (fileName)
	
	#@-node:removeSentinels
	#@+node:weave
	def weave (self):
		
		c = self
	
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = app.gui.runSaveFileDialog(
			initialfile="weave.txt",
			title="Weave",
			filetypes=filetypes,
			defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c.importCommands.weave(fileName)
	#@-node:weave
	#@+node:delete
	def delete(self):
	
		c = self ; v = c.currentVnode()
	
		if c.frame.body.hasTextSelection():
			oldSel = c.frame.body.getTextSelection()
			c.frame.body.deleteTextSelection()
			c.frame.body.onBodyChanged(v,"Delete",oldSel=oldSel)
	#@nonl
	#@-node:delete
	#@+node:executeScript
	def executeScript(self,v=None,script=None):
	
		"""This executes body text as a Python script.
		
		We execute the selected text, or the entire body text if no text is selected."""
		
		error = false
		c = self ; s = None
	
		if script:
			s = script
		else:
			#@		<< define class fileLikeObject >>
			#@+node:<< define class fileLikeObject >>
			class fileLikeObject:
				
				def __init__(self):
					self.s = ""
					
				def clear (self):
					self.s = ""
					
				def close (self):
					pass
					
				def flush (self):
					pass
					
				def get (self):
					return self.s
					
				def write (self,s):
					if s:
						self.s = self.s + s
			#@nonl
			#@-node:<< define class fileLikeObject >>
			#@nl
			#@		<< get script into s >>
			#@+node:<< get script into s >>
			try:
				if v is None:
					v = c.currentVnode()
				old_body = v.bodyString()
				
				if c.frame.body.hasTextSelection():
					# Temporarily replace v's body text with just the selected text.
					s = c.frame.body.getSelectedText()
					v.t.setTnodeText(s) 
				else:
					s = c.frame.body.getAllText()
			
				if s.strip():
					app.scriptDict["script1"]=s
					df = c.atFileCommands.new_df
					df.scanAllDirectives(v,scripting=true)
					# Force Python comment delims.
					df.startSentinelComment = "#"
					df.endSentinelComment = None
					# Write the "derived file" into fo.
					fo = fileLikeObject()
					df.write(v,nosentinels=true,scriptFile=fo)
					s = fo.get()
					app.scriptDict["script2"]=s
					error = len(s) == 0
			
			finally:
				v.t.setTnodeText(old_body)
			#@-node:<< get script into s >>
			#@nl
		#@	<< redirect output if redirect_execute_script_output_to_log_pane >>
		#@+node:<< redirect output if redirect_execute_script_output_to_log_pane >>
		if app.config.redirect_execute_script_output_to_log_pane:
		
			from leoGlobals import redirectStdout,redirectStderr
			redirectStdout() # Redirect stdout
			redirectStderr() # Redirect stderr
		#@nonl
		#@-node:<< redirect output if redirect_execute_script_output_to_log_pane >>
		#@nl
		s = s.strip()
		if s:
			s += '\n' # Make sure we end the script properly.
			try:
				exec s in {} # Use {} to get a pristine environment!
			except:
				es("exception executing script")
				es_exception(full=false,c=c)
		elif not error:
			es("no script selected",color="blue")
	#@nonl
	#@-node:executeScript
	#@+node:goToLineNumber & allies
	def goToLineNumber (self):
	
		c = self ; v = c.currentVnode()
		#@	<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		#@+node:<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		# Search the present node first.
		j = v.t.joinList
		if v in j:
			j.remove(v)
		j.insert(0,v)
		
		# 10/15/03: search joined nodes if first search fails.
		root = None ; fileName = None
		for v in j:
			while v and not fileName:
				if v.isAtFileNode():
					fileName = v.atFileNodeName()
				elif v.isAtSilentFileNode():
					fileName = v.atSilentFileNodeName()
				elif v.isAtRawFileNode():
					fileName = v.atRawFileNodeName()
				else:
					v = v.parent()
			if fileName:
				root = v
				# trace("root,fileName",root,fileName)
				break # Bug fix: 10/25/03
		if not root:
			es("Go to line number: ancestor must be @file node", color="blue")
			return
		#@nonl
		#@-node:<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		#@nl
		#@	<< read the file into lines >>
		#@+node:<< read the file into lines >> in OnGoToLineNumber
		# 1/26/03: calculate the full path.
		d = scanDirectives(c)
		path = d.get("path")
		
		fileName = os_path_join(path,fileName)
		
		try:
			file=open(fileName)
			lines = file.readlines()
			file.close()
		except:
			es("not found: " + fileName)
			return
			
		#@-node:<< read the file into lines >> in OnGoToLineNumber
		#@nl
		#@	<< get n, the line number, from a dialog >>
		#@+node:<< get n, the line number, from a dialog >>
		n = app.gui.runAskOkCancelNumberDialog("Enter Line Number","Line number:")
		if n == -1:
			return
		#@nonl
		#@-node:<< get n, the line number, from a dialog >>
		#@nl
		# trace("n:"+`n`)
		if n==1:
			v = root ; n2 = 1 ; found = true
		elif n >= len(lines):
			v = root ; found = false
			n2 = v.bodyString().count('\n')
		elif root.isAtSilentFileNode():
			#@		<< count outline lines, setting v,n2,found >>
			#@+node:<< count outline lines, setting v,n2,found >> (@file-nosent only)
			v = lastv = root ; after = root.nodeAfterTree()
			prev = 0 ; found = false
			while v and v != after:
				lastv = v
				s = v.bodyString()
				lines = s.count('\n')
				if len(s) > 0 and s[-1] != '\n':
					lines += 1
				# print lines,prev,v
				if prev + lines >= n:
					found = true ; break
				prev += lines
				v = v.threadNext()
			
			v = lastv
			n2 = max(1,n-prev)
			#@nonl
			#@-node:<< count outline lines, setting v,n2,found >> (@file-nosent only)
			#@nl
		else:
			vnodeName,childIndex,n2,delim = self.convertLineToVnodeNameIndexLine(lines,n,root)
			found = true
			if not vnodeName:
				es("invalid derived file: " + fileName)
				return
			#@		<< set v to the node given by vnodeName and childIndex or n >>
			#@+node:<< set v to the node given by vnodeName and childIndex or n >>
			after = root.nodeAfterTree()
			
			if childIndex == -1:
				#@	<< 4.x: scan for the node using tnodeList and n >>
				#@+node:<< 4.x: scan for the node using tnodeList and n >>
				# This is about the best that can be done without replicating the entire atFile write logic.
				
				ok = true
				
				if not hasattr(root,"tnodeList"):
					s = "no child index for " + root.headString()
					print s ; es(s, color="red")
					ok = false
				
				if ok:
					tnodeList = root.tnodeList
					#@	<< set tnodeIndex to the number of +node sentinels before line n >>
					#@+node:<< set tnodeIndex to the number of +node sentinels before line n >>
					tnodeIndex = -1 # Don't count the @file node.
					scanned = 0 # count of lines scanned.
					
					for s in lines:
						if scanned >= n:
							break
						i = skip_ws(s,0)
						if match(s,i,delim):
							i += len(delim)
							if match(s,i,"+node"):
								# trace(tnodeIndex,s.rstrip())
								tnodeIndex += 1
						scanned += 1
					#@nonl
					#@-node:<< set tnodeIndex to the number of +node sentinels before line n >>
					#@nl
					tnodeIndex = max(0,tnodeIndex)
					#@	<< set v to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
					#@+node:<< set v to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
					#@+at 
					#@nonl
					# We use the tnodeList to find a _tnode_ corresponding to 
					# the proper node, so the user will for sure be editing 
					# the proper text, even if several nodes happen to have 
					# the same headline.  This is really all that we need.
					# 
					# However, this code has no good way of distinguishing 
					# between different cloned vnodes in the file: they all 
					# have the same tnode.  So this code just picks v = 
					# t.joinList[0] and leaves it at that.
					# 
					# The only way to do better is to scan the outline, 
					# replicating the write logic to determine which vnode 
					# created the given line.  That's way too difficult, and 
					# it would create an unwanted dependency in this code.
					#@-at
					#@@c
					
					# trace("tnodeIndex",tnodeIndex)
					if tnodeIndex < len(tnodeList):
						t = tnodeList[tnodeIndex]
						# Find the first vnode whose tnode is t.
						v = root
						while v and v != after:
							if v.t == t:
								break
							v = v.threadNext()
						if not v:
							s = "tnode not found for " + vnodeName
							print s ; es(s, color="red") ; ok = false
						elif v.headString().strip() != vnodeName:
							if 0: # Apparently this error doesn't prevent a later scan for working properly.
								s = "Mismatched vnodeName\nExpecting: %s\n got: %s" % (v.headString(),vnodeName)
								print s ; es(s, color="red")
							ok = false
					else:
						s = "Invalid computed tnodeIndex: %d" % tnodeIndex
						print s ; es(s, color = "red") ; ok = false
					#@nonl
					#@-node:<< set v to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
					#@nl
							
				if not ok:
					# Fall back to the old logic.
					#@	<< set v to the first node whose headline matches vnodeName >>
					#@+node:<< set v to the first node whose headline matches vnodeName >>
					v = root
					while v and v != after:
						if v.matchHeadline(vnodeName):
							break
						v = v.threadNext()
					
					if not v or v == after:
						s = "not found: " + vnodeName
						print s ; es(s, color="red")
						return
					#@nonl
					#@-node:<< set v to the first node whose headline matches vnodeName >>
					#@nl
				#@nonl
				#@-node:<< 4.x: scan for the node using tnodeList and n >>
				#@nl
			else:
				#@	<< 3.x: scan for the node with the given childIndex >>
				#@+node:<< 3.x: scan for the node with the given childIndex >>
				v = root
				while v and v != after:
					if v.matchHeadline(vnodeName):
						if childIndex <= 0 or v.childIndex() + 1 == childIndex:
							break
					v = v.threadNext()
				
				if not v or v == after:
					es("not found: " + vnodeName, color="red")
					return
				#@nonl
				#@-node:<< 3.x: scan for the node with the given childIndex >>
				#@nl
			#@nonl
			#@-node:<< set v to the node given by vnodeName and childIndex or n >>
			#@nl
		#@	<< select v and make it visible >>
		#@+node:<< select v and make it visible >>
		c.beginUpdate()
		c.frame.tree.expandAllAncestors(v)
		c.selectVnode(v)
		c.endUpdate()
		#@nonl
		#@-node:<< select v and make it visible >>
		#@nl
		#@	<< put the cursor on line n2 of the body text >>
		#@+node:<< put the cursor on line n2 of the body text >>
		if found:
			c.frame.body.setInsertPointToStartOfLine(n2-1)
		else:
			c.frame.body.setInsertionPointToEnd()
			es("%d lines" % len(lines), color="blue")
		
		c.frame.body.makeInsertPointVisible()
		#@nonl
		#@-node:<< put the cursor on line n2 of the body text >>
		#@nl
	#@nonl
	#@-node:goToLineNumber & allies
	#@+node:convertLineToVnodeNameIndexLine
	#@+at 
	#@nonl
	# We count "real" lines in the derived files, ignoring all sentinels that 
	# do not arise from source lines.  When the indicated line is found, we 
	# scan backwards for an @+body line, get the vnode's name from that line 
	# and set v to the indicated vnode.  This will fail if vnode names have 
	# been changed, and that can't be helped.
	# 
	# Returns (vnodeName,offset)
	# 
	# vnodeName: the name found in the previous @+body sentinel.
	# offset: the offset within v of the desired line.
	#@-at
	#@@c
	
	def convertLineToVnodeNameIndexLine (self,lines,n,root):
		
		"""Convert a line number n to a vnode name, child index and line number."""
		
		childIndex = 0 ; newDerivedFile = false
		#@	<< set delim, leoLine from the @+leo line >>
		#@+node:<< set delim, leoLine from the @+leo line >>
		# Find the @+leo line.
		tag = "@+leo"
		i = 0 
		while i < len(lines) and lines[i].find(tag)==-1:
			i += 1
		leoLine = i # Index of the line containing the leo sentinel
		# trace("leoLine:"+`leoLine`)
		
		delim = None # All sentinels start with this.
		if leoLine < len(lines):
			# The opening comment delim is the initial non-whitespace.
			s = lines[leoLine]
			i = skip_ws(s,0)
			j = s.find(tag)
			newDerivedFile = match(s,j,"@+leo-ver=4")
			delim = s[i:j]
			if len(delim)==0:
				delim=None
			else:
				delim += '@'
		#@nonl
		#@-node:<< set delim, leoLine from the @+leo line >>
		#@nl
		if not delim:
			es("bad @+leo sentinel")
			return None,None,None,None
		#@	<< scan back to @+node, setting offset,nodeSentinelLine >>
		#@+node:<< scan back to  @+node, setting offset,nodeSentinelLine >>
		offset = 0 # This is essentially the Tk line number.
		nodeSentinelLine = -1
		line = n - 1
		while line >= 0:
			s = lines[line]
			# trace(`s`)
			i = skip_ws(s,0)
			if match(s,i,delim):
				#@		<< handle delim while scanning backward >>
				#@+node:<< handle delim while scanning backward >>
				if line == n:
					es("line "+str(n)+" is a sentinel line")
				i += len(delim)
				
				if match(s,i,"-node"):
					# The end of a nested section.
					line = self.skipToMatchingNodeSentinel(lines,line,delim)
				elif match(s,i,"+node"):
					nodeSentinelLine = line
					break
				elif match(s,i,"<<") or match(s,i,"@first"):
					offset += 1 # Count these as a "real" lines.
				#@nonl
				#@-node:<< handle delim while scanning backward >>
				#@nl
			else:
				offset += 1 # Assume the line is real.  A dubious assumption.
			line -= 1
		#@nonl
		#@-node:<< scan back to  @+node, setting offset,nodeSentinelLine >>
		#@nl
		if nodeSentinelLine == -1:
			# The line precedes the first @+node sentinel
			# trace("before first line")
			return root.headString(),0,1,delim # 10/13/03
		s = lines[nodeSentinelLine]
		# trace(s)
		#@	<< set vnodeName and childIndex from s >>
		#@+node:<< set vnodeName and childIndex from s >>
		if newDerivedFile:
			# vnode name is everything following the first ':'
			# childIndex is -1 as a flag for later code.
			i = s.find(':')
			if i > -1: vnodeName = s[i+1:].strip()
			else: vnodeName = None
			childIndex = -1
		else:
			# vnode name is everything following the third ':'
			i = 0 ; colons = 0
			while i < len(s) and colons < 3:
				if s[i] == ':':
					colons += 1
					if colons == 1 and i+1 < len(s) and s[i+1] in string.digits:
						junk,childIndex = skip_long(s,i+1)
				i += 1
			vnodeName = s[i:].strip()
			
		# trace("vnodeName:",vnodeName)
		if not vnodeName:
			vnodeName = None
			es("bad @+node sentinel")
		#@-node:<< set vnodeName and childIndex from s >>
		#@nl
		# trace("childIndex,offset",childIndex,offset,vnodeName)
		return vnodeName,childIndex,offset,delim
	#@nonl
	#@-node:convertLineToVnodeNameIndexLine
	#@+node:skipToMatchingNodeSentinel
	def skipToMatchingNodeSentinel (self,lines,n,delim):
		
		s = lines[n]
		i = skip_ws(s,0)
		assert(match(s,i,delim))
		i += len(delim)
		if match(s,i,"+node"):
			start="+node" ; end="-node" ; delta=1
		else:
			assert(match(s,i,"-node"))
			start="-node" ; end="+node" ; delta=-1
		# Scan to matching @+-node delim.
		n += delta ; level = 0
		while 0 <= n < len(lines):
			s = lines[n] ; i = skip_ws(s,0)
			if match(s,i,delim):
				i += len(delim)
				if match(s,i,start):
					level += 1
				elif match(s,i,end):
					if level == 0: break
					else: level -= 1
			n += delta # bug fix: 1/30/02
			
		# trace(n)
		return n
	#@nonl
	#@-node:skipToMatchingNodeSentinel
	#@+node:fontPanel
	def fontPanel(self):
		
		c = self ; frame = c.frame
	
		if not frame.fontPanel:
			frame.fontPanel = app.gui.createFontPanel(c)
			
		frame.fontPanel.bringToFront()
	#@nonl
	#@-node:fontPanel
	#@+node:colorPanel
	def colorPanel(self):
		
		c = self ; frame = c.frame
	
		if not frame.colorPanel:
			frame.colorPanel = app.gui.createColorPanel(c)
			
		frame.colorPanel.bringToFront()
	#@nonl
	#@-node:colorPanel
	#@+node:viewAllCharacters
	def viewAllCharacters (self, event=None):
	
		c = self ; frame = c.frame ; v = c.currentVnode()
	
		colorizer = frame.body.getColorizer()
		colorizer.showInvisibles = choose(colorizer.showInvisibles,0,1)
	
		# It is much easier to change the menu name here than in the menu updater.
		menu = frame.menu.getMenu("Edit")
		if colorizer.showInvisibles:
			frame.menu.setMenuLabel(menu,"Show Invisibles","Hide Invisibles")
		else:
			frame.menu.setMenuLabel(menu,"Hide Invisibles","Show Invisibles")
	
		c.frame.body.recolor_now(v)
	#@nonl
	#@-node:viewAllCharacters
	#@+node:preferences
	def preferences(self):
		
		"""Show the Preferences Panel, creating it if necessary."""
		
		c = self ; frame = c.frame
	
		if not frame.prefsPanel:
			frame.prefsPanel = app.gui.createPrefsPanel(c)
			
		frame.prefsPanel.bringToFront()
	#@nonl
	#@-node:preferences
	#@+node:convertAllBlanks
	def convertAllBlanks (self):
		
		c = self ; body = c.frame.body ; v = current = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("Convert All Blanks")
			return
	
		next = v.nodeAfterTree()
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		count = 0
		while v and v != next:
			vChanged = false
			if v == current:
				if c.convertBlanks(setUndoParams=false):
					count += 1
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				assert(isUnicode(text))
				lines = string.split(text, '\n')
				for line in lines:
					s = optimizeLeadingWhitespace(line,tabWidth)
					if s != line:
						changed = true
						if not vChanged:
							count += 1 ; vChanged = true
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
		if count > 0:
			newText = body.getAllText()
			newSel = body.getTextSelection()
			c.undoer.setUndoParams("Convert All Blanks",
				current,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		es("blanks converted to tabs in %d nodes" % count)
	#@-node:convertAllBlanks
	#@+node:convertAllTabs
	def convertAllTabs (self):
	
		c = self ; body = c.frame.body ; v = current = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("Convert All Tabs")
			return
	
		next = v.nodeAfterTree()
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		count = 0
		while v and v != next:
			vChanged = false
			if v == current:
				if self.convertTabs(setUndoParams=false):
					count += 1
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				assert(isUnicode(text))
				lines = string.split(text, '\n')
				for line in lines:
					i,w = skip_leading_ws_with_indent(line,0,tabWidth)
					s = computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
					if s != line:
						changed = true
						if not vChanged:
							count += 1 ; vChanged = true
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
		if count > 0:
			newText = body.getAllText()
			newSel = body.getTextSelection() # 7/11/03
			c.undoer.setUndoParams("Convert All Tabs",
				current,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		es("tabs converted to blanks in %d nodes" % count)
	#@nonl
	#@-node:convertAllTabs
	#@+node:convertBlanks
	def convertBlanks (self,setUndoParams=true):
	
		c = self ; body = c.frame.body
		
		if app.batchMode:
			c.notValidInBatchMode("Convert Blanks")
			return false
	
		head,lines,tail,oldSel,oldYview = c.getBodyLines(expandSelection=true)
		result = [] ; changed = false
	
		# Use the relative @tabwidth, not the global one.
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		if not tabWidth: return false
	
		for line in lines:
			s = optimizeLeadingWhitespace(line,tabWidth)
			if s != line: changed = true
			result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			undoType = choose(setUndoParams,"Convert Blanks",None)
			c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
	
		return changed
	#@nonl
	#@-node:convertBlanks
	#@+node:convertTabs
	def convertTabs (self,setUndoParams=true):
	
		c = self ; body = c.frame.body
		
		if app.batchMode:
			c.notValidInBatchMode("Convert Tabs")
			return false
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines(expandSelection=true)
		result = [] ; changed = false
		
		# Use the relative @tabwidth, not the global one.
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		if not tabWidth: return false
	
		for line in lines:
			i,w = skip_leading_ws_with_indent(line,0,tabWidth)
			s = computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
			if s != line: changed = true
			result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			undoType = choose(setUndoParams,"Convert Tabs",None)
			c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
			
		return changed
	#@-node:convertTabs
	#@+node:createLastChildNode
	def createLastChildNode (self,parent,headline,body):
		
		c = self
		if body and len(body) > 0:
			body = string.rstrip(body)
		if not body or len(body) == 0:
			body = ""
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		v.t.setTnodeText(body)
		v.createDependents() # To handle effects of clones.
		v.setDirty()
		c.validateOutline()
	#@nonl
	#@-node:createLastChildNode
	#@+node:dedentBody
	def dedentBody (self):
		
		c = self
		
		if app.batchMode:
			c.notValidInBatchMode("Unindent")
			return
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width-abs(c.tab_width),c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Undent",oldSel,oldYview)
	#@nonl
	#@-node:dedentBody
	#@+node:extract
	def extract(self):
		
		c = self ; body = c.frame.body ; current = v = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("Extract")
			return
		
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		#@	<< Set headline for extract >>
		#@+node:<< Set headline for extract >>
		headline = string.strip(headline)
		while len(headline) > 0 and headline[0] == '/':
			headline = headline[1:]
		headline = string.strip(headline)
		#@nonl
		#@-node:<< Set headline for extract >>
		#@nl
		# Remove leading whitespace from all body lines.
		result = []
		for line in lines:
			# Remove the whitespace on the first line
			line = removeLeadingWhitespace(line,ws,c.tab_width)
			result.append(line)
		# Create a new node from lines.
		newBody = string.join(result,'\n') # 11/23/03
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		if 1: # update range...
			c.createLastChildNode(v,headline,newBody) # 11/23/03
			undoType =  "Can't Undo" # 12/8/02: None enables further undoes, but there are bugs now.
			c.updateBodyPane(head,None,tail,undoType,oldSel,oldYview,setSel=false)
			newText = body.getAllText()
			newSel = body.getTextSelection() # 7/11/03
			c.undoer.setUndoParams("Extract",
				v,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		c.endUpdate()
	#@nonl
	#@-node:extract
	#@+node:extractSection
	def extractSection(self):
	
		c = self ; body = c.frame.body ; current = v = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("Extract Section")
			return
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		line1 = "\n" + headline
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		# trace("v:     " + `v`)
		# trace("v_copy:" + `v_copy`)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		#@	<< Set headline for extractSection >>
		#@+node:<< Set headline for extractSection >>
		if 0: # I have no idea why this was being done.
			while len(headline) > 0 and headline[0] == '/':
				headline = headline[1:]
		
		headline = headline.strip()
		
		if len(headline) < 5:
			oops = true
		else:
			head1 = headline[0:2] == '<<'
			head2 = headline[0:2] == '@<'
			tail1 = headline[-2:] == '>>'
			tail2 = headline[-2:] == '@>'
			oops = not (head1 and tail1) and not (head2 and tail2)
		
		if oops:
			es("Selected text should start with a section name",color="blue")
			return
		#@nonl
		#@-node:<< Set headline for extractSection >>
		#@nl
		# Remove leading whitespace from all body lines.
		result = []
		for line in lines:
			# Remove the whitespace on the first line
			line = removeLeadingWhitespace(line,ws,c.tab_width)
			result.append(line)
		# Create a new node from lines.
		newBody = string.join(result,'\n')  # 11/23/03
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		if 1: # update range...
			c.createLastChildNode(v,headline,newBody)  # 11/23/03
			undoType = None # Set undo params later.
			c.updateBodyPane(head+line1,None,tail,undoType,oldSel,oldYview,setSel=false)
			newText = body.getAllText()
			newSel = body.getTextSelection()
			c.undoer.setUndoParams("Extract Section",v,
				select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		c.endUpdate()
	#@nonl
	#@-node:extractSection
	#@+node:extractSectionNames
	def extractSectionNames(self):
	
		c = self ; body = c.frame.body ; current = v = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("Extract Section Names")
			return
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		# No change to body or selection of this node.
		oldText = newText = body.getAllText()
		i, j = oldSel = newSel = body.getTextSelection()
		c.beginUpdate()
		if 1: # update range...
			found = false
			for s in lines:
				#@			<< Find the next section name >>
				#@+node:<< Find the next section name >>
				head1 = string.find(s,"<<")
				if head1 > -1:
					head2 = string.find(s,">>",head1)
				else:
					head1 = string.find(s,"@<")
					if head1 > -1:
						head2 = string.find(s,"@>",head1)
						
				if head1 == -1 or head2 == -1 or head1 > head2:
					name = None
				else:
					name = s[head1:head2+2]
				#@nonl
				#@-node:<< Find the next section name >>
				#@nl
				if name:
					self.createLastChildNode(v,name,None)
					found = true
			c.selectVnode(v)
			c.validateOutline()
			if not found:
				es("Selected text should contain one or more section names",color="blue")
		c.endUpdate()
		# No change to body or selection
		c.undoer.setUndoParams("Extract Names",
			v,select=current,oldTree=v_copy,
			oldText=oldText,newText=newText,
			oldSel=oldSel,newSel=newSel)
		# Restore the selection.
		body.setTextSelection(oldSel)
		body.setFocus()
	#@nonl
	#@-node:extractSectionNames
	#@+node:findBoundParagraph
	def findBoundParagraph (self):
		
		c = self
		head,ins,tail = c.frame.body.getInsertLines()
	
		if not ins or ins.isspace() or ins[0] == '@':
			return None,None,None,None # DTHEIN 18-JAN-2004
			
		head_lines = splitLines(head)
		tail_lines = splitLines(tail)
	
		if 0:
			#@		<< trace head_lines, ins, tail_lines >>
			#@+node:<< trace head_lines, ins, tail_lines >>
			if 0:
				print ; print "head_lines"
				for line in head_lines: print `line`
				print ; print "ins", `ins`
				print ; print "tail_lines"
				for line in tail_lines: print `line`
			else:
				es("head_lines: " + `head_lines`)
				es("ins: ", `ins`)
				es("tail_lines: " + `tail_lines`)
			#@-node:<< trace head_lines, ins, tail_lines >>
			#@nl
	
		# Scan backwards.
		i = len(head_lines)
		while i > 0:
			i -= 1
			line = head_lines[i]
			if len(line) == 0 or line.isspace() or line[0] == '@':
				i += 1 ; break
	
		pre_para_lines = head_lines[:i]
		para_head_lines = head_lines[i:]
	
		# Scan forwards.
		i = 0
		trailingNL = False # DTHEIN 18-JAN-2004: properly capture terminating NL
		while i < len(tail_lines):
			line = tail_lines[i]
			if len(line) == 0 or line.isspace() or line[0] == '@':
				trailingNL = line.endswith(u'\n') or line.startswith(u'@') # DTHEIN 21-JAN-2004
				break
			i += 1
			
	#	para_tail_lines = tail_lines[:i]
		para_tail_lines = tail_lines[:i]
		post_para_lines = tail_lines[i:]
		
		head = joinLines(pre_para_lines)
		result = para_head_lines 
		result.extend([ins])
		result.extend(para_tail_lines)
		tail = joinLines(post_para_lines)
	
		# DTHEIN 18-JAN-2004: added trailingNL to return value list
		return head,result,tail,trailingNL # string, list, string, bool
	#@nonl
	#@-node:findBoundParagraph
	#@+node:findMatchingBracket
	def findMatchingBracket (self):
		
		c = self ; body = c.frame.body
		
		if app.batchMode:
			c.notValidInBatchMode("Match Brackets")
			return
	
		brackets = "()[]{}<>"
		ch1 = body.getCharBeforeInsertPoint()
		ch2 = body.getCharAtInsertPoint()
	
		# Prefer to match the character to the left of the cursor.
		if ch1 in brackets:
			ch = ch1 ; index = body.getBeforeInsertionPoint()
		elif ch2 in brackets:
			ch = ch2 ; index = body.getInsertionPoint()
		else:
			return
		
		index2 = self.findSingleMatchingBracket(ch,index)
		if index2:
			if body.compareIndices(index,"<=",index2):
				adj_index = body.adjustIndex(index2,1)
				body.setTextSelection(index,adj_index)
			else:
				adj_index = body.adjustIndex(index,1)
				body.setTextSelection(index2,adj_index)
			adj_index = body.adjustIndex(index2,1)
			body.setInsertionPoint(adj_index)
			body.makeIndexVisible(adj_index)
		else:
			es("unmatched " + `ch`)
	#@nonl
	#@-node:findMatchingBracket
	#@+node:findMatchingBracket
	# To do: replace comments with blanks before scanning.
	# Test  unmatched())
	def findSingleMatchingBracket(self,ch,index):
		
		c = self ; body = c.frame.body
		open_brackets  = "([{<" ; close_brackets = ")]}>"
		brackets = open_brackets + close_brackets
		matching_brackets = close_brackets + open_brackets
		forward = ch in open_brackets
		# Find the character matching the initial bracket.
		for n in xrange(len(brackets)):
			if ch == brackets[n]:
				match_ch = matching_brackets[n]
				break
		level = 0
		while 1:
			if forward and body.compareIndices(index,">=","end"):
				# trace("not found")
				return None
			ch2 = body.getCharAtIndex(index)
			if ch2 == ch:
				level += 1 #; trace(level,index)
			if ch2 == match_ch:
				level -= 1 #; trace(level,index)
				if level <= 0:
					return index
			if not forward and body.compareIndices(index,"<=","1.0"):
				# trace("not found")
				return None
			adj = choose(forward,1,-1)
			index = body.adjustIndex(index,adj)
		return 0 # unreachable: keeps pychecker happy.
	# Test  (
	# ([(x){y}]))
	# Test  ((x)(unmatched
	#@nonl
	#@-node:findMatchingBracket
	#@+node:getBodyLines
	def getBodyLines (self,expandSelection=false):
	
		c = self ; body = c.frame.body
		oldVview = body.getYScrollPosition()
		oldSel   = body.getTextSelection()
	
		if expandSelection: # 12/3/03
			lines = body.getAllText()
			head = tail = None
		else:
			# Note: lines is the entire line containing the insert point if no selection.
			head,lines,tail = body.getSelectionLines()
	
		lines = string.split(lines,'\n') # It would be better to use splitLines.
	
		return head,lines,tail,oldSel,oldVview
	#@nonl
	#@-node:getBodyLines
	#@+node:indentBody
	def indentBody (self):
	
		c = self
		
		if app.batchMode:
			c.notValidInBatchMode("Indent")
			return
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width+abs(c.tab_width),c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Indent",oldSel,oldYview)
	#@nonl
	#@-node:indentBody
	#@+node:insertBodyTime & allies
	def insertBodyTime (self):
		
		c = self ; v = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("xxx")
			return
		
		oldSel = c.frame.body.getTextSelection()
		c.frame.body.deleteTextSelection() # Works if nothing is selected.
		s = self.getTime(body=true)
		c.frame.body.insertAtInsertPoint(s)
		c.frame.body.onBodyChanged(v,"Typing",oldSel=oldSel)
	#@nonl
	#@-node:insertBodyTime & allies
	#@+node:getTime
	def getTime (self,body=true):
	
		config = app.config
		default_format =  "%m/%d/%Y %H:%M:%S" # E.g., 1/30/2003 8:31:55
		
		# Try to get the format string from leoConfig.txt.
		if body:
			format = config.getWindowPref("body_time_format_string")
			gmt = config.getBoolWindowPref("body_gmt_time")
		else:
			format = config.getWindowPref("headline_time_format_string")
			gmt = config.getBoolWindowPref("headline_gmt_time")
	
		if format == None:
			format = default_format
	
		try:
			if gmt:
				s = time.strftime(format,time.gmtime())
			else:
				s = time.strftime(format,time.localtime())
		except:
			es_exception() # Probably a bad format string in leoConfig.txt.
			s = time.strftime(default_format,time.gmtime())
		return s
	#@-node:getTime
	#@+node:reformatParagraph
	def reformatParagraph(self):
	
		"""Reformat a text paragraph in a Tk.Text widget
	
	Wraps the concatenated text to present page width setting. Leading tabs are
	sized to present tab width setting. First and second line of original text is
	used to determine leading whitespace in reformatted text. Hanging indentation
	is honored.
	
	Paragraph is bound by start of body, end of body, blank lines, and lines
	starting with "@". Paragraph is selected by position of current insertion
	cursor."""
	
		c = self ; body = c.frame.body ; v = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("xxx")
			return
	
		if body.hasTextSelection():
			es("Text selection inhibits Reformat Paragraph",color="blue")
			return
	
		#@	<< compute vars for reformatParagraph >>
		#@+node:<< compute vars for reformatParagraph >>
		dict = scanDirectives(c)
		pageWidth = dict.get("pagewidth")
		tabWidth  = dict.get("tabwidth")
		
		original = body.getAllText()
		oldSel   = body.getTextSelection()
		oldYview = body.getYScrollPosition()
		head,lines,tail,trailingNL = c.findBoundParagraph() # DTHEIN 18-JAN-2004: add trailingNL
		#@nonl
		#@-node:<< compute vars for reformatParagraph >>
		#@nl
		if lines:
			#@		<< compute the leading whitespace >>
			#@+node:<< compute the leading whitespace >>
			indents = [0,0] ; leading_ws = ["",""]
			
			for i in (0,1):
				if i < len(lines):
					# Use the original, non-optimized leading whitespace.
					leading_ws[i] = ws = get_leading_ws(lines[i])
					indents[i] = computeWidth(ws,tabWidth)
					
			indents[1] = max(indents)
			if len(lines) == 1:
				leading_ws[1] = leading_ws[0]
			#@-node:<< compute the leading whitespace >>
			#@nl
			#@		<< compute the result of wrapping all lines >>
			#@+node:<< compute the result of wrapping all lines >>
			# Remember whether the last line ended with a newline.
			lastLine = lines[-1]
			if 0: # DTHEIN 18-JAN-2004: removed because findBoundParagraph now gives trailingNL
				trailingNL = lastLine and lastLine[-1] == '\n'
			
			# Remove any trailing newlines for wraplines.
			lines = [line[:-1] for line in lines[:-1]]
			if lastLine and not trailingNL:
				lastLine = lastLine[:-1]
			lines.extend([lastLine])
			
			# Wrap the lines, decreasing the page width by indent.
			result = wrap_lines(lines,
				pageWidth-indents[1],
				pageWidth-indents[0])
			
			# DTHEIN 	18-JAN-2004
			# prefix with the leading whitespace, if any
			paddedResult = []
			paddedResult.append(leading_ws[0] + result[0])
			for line in result[1:]:
				paddedResult.append(leading_ws[1] + line)
			
			# Convert the result to a string.
			result = '\n'.join(paddedResult) # DTHEIN 	18-JAN-2004: use paddedResult
			if 0: # DTHEIN 18-JAN-2004:  No need to do this.
				if trailingNL:
					result += '\n'
			#@-node:<< compute the result of wrapping all lines >>
			#@nl
			#@		<< update the body, selection & undo state >>
			#@+node:<< update the body, selection & undo state >>
			sel_start, sel_end = body.setSelectionAreas(head,result,tail)
			
			changed = original != head + result + tail
			undoType = choose(changed,"Reformat Paragraph",None)
			body.onBodyChanged(v,undoType,oldSel=oldSel,oldYview=oldYview)
			
			# Advance the selection to the next paragraph.
			newSel = sel_end, sel_end
			body.setTextSelection(newSel)
			body.makeIndexVisible(sel_end)
			
			c.recolor()
			#@nonl
			#@-node:<< update the body, selection & undo state >>
			#@nl
	#@nonl
	#@-node:reformatParagraph
	#@+node:updateBodyPane (handles undo)
	def updateBodyPane (self,head,middle,tail,undoType,oldSel,oldYview,setSel=true):
		
		c = self ; body = c.frame.body ; v = c.currentVnode()
	
		# Update the text and notify the event handler.
		body.setSelectionAreas(head,middle,tail)
	
		if setSel:
			body.setTextSelection(oldSel)
	
		body.onBodyChanged(v,undoType,oldSel=oldSel,oldYview=oldYview)
	
		# Update the changed mark and icon.
		c.setChanged(true)
		c.beginUpdate()
		if not v.isDirty():
			v.setDirty()
		c.endUpdate()
	
		# Scroll as necessary.
		if oldYview:
			body.setYScrollPosition(oldYview)
		else:
			body.makeInsertPointVisible()
	
		body.setFocus()
		c.recolor()
	#@nonl
	#@-node:updateBodyPane (handles undo)
	#@+node:editHeadline
	def editHeadline(self):
		
		c = self ; tree = c.frame.tree
		
		if app.batchMode:
			c.notValidInBatchMode("Edit Headline")
			return
	
		tree.editLabel(tree.currentVnode())
	#@nonl
	#@-node:editHeadline
	#@+node:toggleAngleBrackets
	def toggleAngleBrackets (self):
		
		c = self ; v = c.currentVnode()
		
		if app.batchMode:
			c.notValidInBatchMode("Toggle Angle Brackets")
			return
	
		s = v.headString().strip()
		if (s[0:2] == "<<"
			or s[-2:] == ">>"): # Must be on separate line.
			if s[0:2] == "<<": s = s[2:]
			if s[-2:] == ">>": s = s[:-2]
			s = s.strip()
		else:
			s = angleBrackets(' ' + s + ' ')
		
		c.frame.tree.editLabel(v)
		if v.edit_text():
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("1.0",s)
			c.frame.tree.onHeadChanged(v)
	#@-node:toggleAngleBrackets
	#@+node:findPanel
	def findPanel(self):
	
		c = self
	
		find = app.findFrame
		find.bringToFront()
		find.c = self
	#@-node:findPanel
	#@+node:findNext
	def findNext(self):
	
		c = self
		app.findFrame.findNextCommand(c)
	#@-node:findNext
	#@+node:findPrevious
	def findPrevious(self):
	
		c = self
		app.findFrame.findPreviousCommand(c)
	#@-node:findPrevious
	#@+node:replace
	def replace(self):
	
		c = self
		app.findFrame.changeCommand(c)
	#@-node:replace
	#@+node:replaceThenFind
	def replaceThenFind(self):
	
		c = self
		app.findFrame.changeThenFindCommand(c)
	#@-node:replaceThenFind
	#@+node:notValidInBatchMode
	def notValidInBatchMode(self, commandName):
		
		es("%s command is not valid in batch mode" % commandName)
	#@-node:notValidInBatchMode
	#@+node:cutOutline
	def cutOutline(self):
	
		c = self
		if c.canDeleteHeadline():
			c.copyOutline()
			c.deleteOutline("Cut Node")
			c.recolor()
	#@nonl
	#@-node:cutOutline
	#@+node:copyOutline
	def copyOutline(self):
	
		# Copying an outline has no undo consequences.
		c = self
		c.endEditing()
		c.fileCommands.assignFileIndices()
		s = c.fileCommands.putLeoOutline()
		app.gui.replaceClipboardWith(s)
	#@nonl
	#@-node:copyOutline
	#@+node:pasteOutline
	# To cut and paste between apps, just copy into an empty body first, then copy to Leo's clipboard.
	
	def pasteOutline(self):
	
		c = self ; current = c.currentVnode()
		
		s = app.gui.getTextFromClipboard()
		
		if 0: # old code
			try:
				s = app.root.selection_get(selection="CLIPBOARD")
			except:
				s = None # This should never happen.
	
		if not s or not c.canPasteOutline(s):
			return # This should never happen.
	
		isLeo = match(s,0,app.prolog_prefix_string)
	
		# trace(`s`)
		if isLeo:
			v = c.fileCommands.getLeoOutline(s)
		else:
			v = c.importCommands.convertMoreStringToOutlineAfter(s,current)
		if v:
			c.endEditing()
			c.beginUpdate()
			if 1: # inside update...
				v.createDependents()# To handle effects of clones.
				c.validateOutline()
				c.selectVnode(v)
				v.setDirty()
				c.setChanged(true)
				# paste as first child if back is expanded.
				back = v.back()
				if back and back.isExpanded():
					v.moveToNthChildOf(back,0)
				c.undoer.setUndoParams("Paste Node",v)
			c.endUpdate()
			c.recolor()
		else:
			es("The clipboard is not a valid " + choose(isLeo,"Leo","MORE") + " file")
	#@nonl
	#@-node:pasteOutline
	#@+node:c.checkOutline
	def checkOutline (self):
		
		"""Report any possible clone errors in the outline.
		
		Remove any unused tnodeLists."""
		
		c = self ; v = c.rootVnode()
		
		checkTopologyOfAllClones(c,verbose=false)
		
		nodes = 0 ; errors = 0
		while v:
			nodes += 1
			# 12/13/03: Empty tnodeLists are not errors.
			if hasattr(v,"tnodeList") and len(v.tnodeList) > 0 and not v.isAnyAtFileNode():
				s = "deleting tnodeList for " + `v`
				print s ; es(s,color="blue")
				delattr(v,"tnodeList")
				errors += 1
	
			v = v.threadNext()
	
		es("%d nodes checked" % nodes)
		return errors
	#@nonl
	#@-node:c.checkOutline
	#@+node:Hoist & dehoist & enablers
	def dehoist(self):
	
		c = self ; v = c.currentVnode()
		if v and c.canDehoist():
			c.undoer.setUndoParams("De-Hoist",v)
			c.hoistStack.pop()
			v.contract()
			c.redraw()
			c.frame.clearStatusLine()
			if c.hoistStack:
				h = c.hoistStack[-1]
				c.frame.putStatusLine("Hoist: " + h.headString())
			else:
				c.frame.putStatusLine("No hoist")
	
	def hoist(self):
	
		c = self ; v = c.currentVnode()
		if v and c.canHoist():
			c.undoer.setUndoParams("Hoist",v)
			c.hoistStack.append(v)
			v.expand()
			c.redraw()
			c.frame.clearStatusLine()
			c.frame.putStatusLine("Hoist: " + v.headString())
	
	def canDehoist(self):
		
		return len(self.hoistStack) > 0
			
	def canHoist(self):
		
		c = self ; v = c.currentVnode()
		if v == c.rootVnode():
			return v.next() != None
		elif not c.hoistStack:
			return true
		else:
			return c.hoistStack[-1] != v
	#@nonl
	#@-node:Hoist & dehoist & enablers
	#@+node:c.checkMoveWithParentWithWarning
	# Returns false if any node of tree is a clone of parent or any of parents ancestors.
	
	def checkMoveWithParentWithWarning (self,root,parent,warningFlag):
	
		clone_message = "Illegal move or drag: no clone may contain a clone of itself"
		drag_message  = "Illegal drag: Can't drag a node into its own tree"
	
		# 10/25/02: Create dictionaries for faster checking.
		parents = {} ; clones = {}
		while parent:
			parents [parent.t] = parent.t
			if parent.isCloned():
				clones [parent.t] = parent.t
			parent = parent.parent()
		
		# 10/25/02: Scan the tree only once.
		v = root ; next = root.nodeAfterTree()
		while v and v != next:
			ct = clones.get(v.t)
			if ct != None and ct == v.t:
				if warningFlag:
					alert(clone_message)
				return false
			v = v.threadNext()
	
		pt = parents.get(root.t)
		if pt == None:
			return true
		else:
			if warningFlag:
				alert(drag_message)
			return false
	#@-node:c.checkMoveWithParentWithWarning
	#@+node:c.deleteOutline
	# Deletes the current vnode and dependent nodes. Does nothing if the outline would become empty.
	
	def deleteOutline (self,op_name="Delete Outline"):
	
		c = self ; v = c.currentVnode()
		if not v: return
		vBack = v.visBack()
		# Bug fix: 1/18/00: if vBack is NULL we are at the top level,
		# the next node should be v.next(), _not_ v.visNext();
		if vBack: newNode = vBack
		else: newNode = v.next()
		if not newNode: return
		c.endEditing()# Make sure we capture the headline for Undo.
		c.beginUpdate()
		v.setDirtyDeleted() # 8/3/02: Mark @file nodes dirty for all clones in subtree.
		# Reinsert v after back, or as the first child of parent, or as the root.
		c.undoer.setUndoParams(op_name,v,select=newNode)
		v.doDelete(newNode) # doDelete destroys dependents.
		c.setChanged(true)
		c.endUpdate()
		c.validateOutline()
	#@nonl
	#@-node:c.deleteOutline
	#@+node:c.insertHeadline
	# Inserts a vnode after the current vnode.  All details are handled by the vnode class.
	
	def insertHeadline (self,op_name="Insert Outline"):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		c.beginUpdate()
		if 1: # inside update...
			if current.hasChildren() and current.isExpanded():
				v = current.insertAsNthChild(0)
			else:
				v = current.insertAfter()
			c.undoer.setUndoParams(op_name,v,select=current)
			v.createDependents() # To handle effects of clones.
			c.selectVnode(v)
			c.editVnode(v)
			v.setDirty() # Essential in Leo2.
			c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:c.insertHeadline
	#@+node:c.clone
	def clone (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
		c.beginUpdate()
		clone = v.clone(v)
		c.initAllCloneBitsInTree(v) # 10/14/03
		clone.setDirty() # essential in Leo2
		c.setChanged(true)
		if c.validateOutline():
			c.selectVnode(clone)
			c.undoer.setUndoParams("Clone",clone)
		c.endUpdate() # updates all icons
	#@nonl
	#@-node:c.clone
	#@+node:initAllCloneBits & initAllCloneBitsInTree
	def initAllCloneBits (self):
		
		"""Initialize all clone bits in the entire outline"""
	
		c=self
		c.clearAllVisited()
		v = self.rootVnode()
		c.beginUpdate()
		while v:
			if not v.t.isVisited():
				v.t.setVisited() # Inhibit visits to all joined nodes.
				c.initJoinedCloneBits(v)
			v = v.threadNext()
		c.endUpdate()
		
	def initAllCloneBitsInTree (self,v):
		
		"""Initialize all clone bits in the v's subtree"""
	
		c=self
		v.clearAllVisitedInTree()
		after = v.nodeAfterTree()
		c.beginUpdate()
		while v and v != after:
			if not v.t.isVisited():
				v.t.setVisited() # Inhibit visits to all joined nodes.
				c.initJoinedCloneBits(v)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:initAllCloneBits & initAllCloneBitsInTree
	#@+node:c.initJoinedClonedBits (changed in 3.11.1)
	# Initializes all clone bits in the all nodes joined to v.
	
	def initJoinedCloneBits (self,v):
		
		if 0:
			if not self.loading:
				trace(len(v.t.joinList),v)
	
		c = self
		c.beginUpdate()
		mark = v.shouldBeClone()
		if mark:
			# Set clone bit in v and all joined nodes.
			v.setClonedBit()
			for v2 in v.t.joinList:
				v2.setClonedBit()
		else:
			# Set clone bit in v and all joined nodes.
			v.clearClonedBit()
			for v2 in v.t.joinList:
				v2.clearClonedBit()
		c.endUpdate()
	#@-node:c.initJoinedClonedBits (changed in 3.11.1)
	#@+node:validateOutline
	# Makes sure all nodes are valid.
	
	def validateOutline (self):
	
		c = self ; root = c.rootVnode()
		if root:
			return root.validateOutlineWithParent(None)
		else:
			return true
	#@nonl
	#@-node:validateOutline
	#@+node:c.sortChildren, sortSiblings
	def sortChildren(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.hasChildren(): return
		#@	<< Set the undo info for sortChildren >>
		#@+node:<< Set the undo info for sortChildren >>
		# Get the present list of children.
		children = []
		child = v.firstChild()
		while child:
			children.append(child)
			child = child.next()
		c.undoer.setUndoParams("Sort Children",v,sort=children)
		#@nonl
		#@-node:<< Set the undo info for sortChildren >>
		#@nl
		c.beginUpdate()
		c.endEditing()
		v.sortChildren()
		v.setDirty()
		c.setChanged(true)
		c.endUpdate()
		
	def sortSiblings (self):
		
		c = self ; v = c.currentVnode()
		if not v: return
		parent = v.parent()
		if not parent:
			c.sortTopLevel()
		else:
			#@		<< Set the undo info for sortSiblings >>
			#@+node:<< Set the undo info for sortSiblings >>
			# Get the present list of siblings.
			sibs = []
			sib = parent.firstChild()
			while sib:
				sibs.append(sib)
				sib = sib.next()
			c.undoer.setUndoParams("Sort Siblings",v,sort=sibs)
			#@nonl
			#@-node:<< Set the undo info for sortSiblings >>
			#@nl
			c.beginUpdate()
			c.endEditing()
			parent.sortChildren()
			parent.setDirty()
			c.setChanged(true)
			c.endUpdate()
	#@nonl
	#@-node:c.sortChildren, sortSiblings
	#@+node:c.sortTopLevel
	def sortTopLevel (self):
		
		# Create a list of vnode, headline tuples
		c = self ; v = root = c.rootVnode()
		if not v: return
		#@	<< Set the undo info for sortTopLevel >>
		#@+node:<< Set the undo info for sortTopLevel >>
		# Get the present list of children.
		sibs = []
		sib = c.rootVnode()
		while sib:
			sibs.append(sib)
			sib = sib.next()
		c.undoer.setUndoParams("Sort Top Level",v,sort=sibs)
		#@nonl
		#@-node:<< Set the undo info for sortTopLevel >>
		#@nl
		pairs = []
		while v:
			pairs.append((v.headString().lower(), v))
			v = v.next()
		# Sort the list on the headlines.
		pairs.sort()
		sortedNodes = pairs
		# Move the nodes
		c.beginUpdate()
		h,v = sortedNodes[0]
		if v != root:
			v.moveToRoot(oldRoot=root)
		for h,next in sortedNodes[1:]:
			next.moveAfter(v)
			v = next
		c.endUpdate()
	#@nonl
	#@-node:c.sortTopLevel
	#@+node:contractAllHeadlines
	def contractAllHeadlines (self):
	
		c = self ; current = c.currentVnode()
		v = c.rootVnode()
		c.beginUpdate()
	
		while v:
			c.contractSubtree(v)
			v = v.next()
	
		if not current.isVisible():
			# 1/31/03: Select the topmost ancestor of the presently selected node.
			v = current
			while v and v.parent():
				v = v.parent()
			c.selectVnode(v)
	
		c.endUpdate()
		c.expansionLevel = 1 # Reset expansion level.
	#@nonl
	#@-node:contractAllHeadlines
	#@+node:contractNode
	def contractNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.contract()
		c.endUpdate()
	#@-node:contractNode
	#@+node:contractParent
	def contractParent (self):
		
		c = self ; v = c.currentVnode()
		parent = v.parent()
		if not parent: return
		
		c.beginUpdate()
		c.selectVnode(parent)
		parent.contract()
		c.endUpdate()
	#@nonl
	#@-node:contractParent
	#@+node:expandAllHeadlines
	def expandAllHeadlines(self):
	
		c = self ; v = root = c.rootVnode()
		c.beginUpdate()
		while v:
			c.expandSubtree(v)
			v = v.next()
		c.selectVnode(root)
		c.endUpdate()
		c.expansionLevel = 0 # Reset expansion level.
	#@nonl
	#@-node:expandAllHeadlines
	#@+node:expandAllSubheads
	def expandAllSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		c.expandSubtree(v)
		while child:
			c.expandSubtree(child)
			child = child.next()
		c.selectVnode(v)
		c.endUpdate()
	#@nonl
	#@-node:expandAllSubheads
	#@+node:expandLevel1..9
	def expandLevel1 (self): self.expandToLevel(1)
	def expandLevel2 (self): self.expandToLevel(2)
	def expandLevel3 (self): self.expandToLevel(3)
	def expandLevel4 (self): self.expandToLevel(4)
	def expandLevel5 (self): self.expandToLevel(5)
	def expandLevel6 (self): self.expandToLevel(6)
	def expandLevel7 (self): self.expandToLevel(7)
	def expandLevel8 (self): self.expandToLevel(8)
	def expandLevel9 (self): self.expandToLevel(9)
	#@-node:expandLevel1..9
	#@+node:expandNextLevel
	def expandNextLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(c.expansionLevel + 1)
	#@-node:expandNextLevel
	#@+node:expandNode
	def expandNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.expand()
		c.endUpdate()
	
	#@-node:expandNode
	#@+node:expandPrevLevel
	def expandPrevLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(max(1,c.expansionLevel - 1))
	#@-node:expandPrevLevel
	#@+node:contractSubtree
	def contractSubtree (self,v):
	
		last = v.lastNode()
		while v and v != last:
			v.contract()
			v = v.threadNext()
	#@nonl
	#@-node:contractSubtree
	#@+node:expandSubtree
	def expandSubtree (self,v):
	
		c = self
		last = v.lastNode()
		while v and v != last:
			v.expand()
			v = v.threadNext()
		c.redraw()
	#@nonl
	#@-node:expandSubtree
	#@+node:expandToLevel
	def expandToLevel (self,level):
	
		c = self
		c.beginUpdate()
		if 1: # 1/31/03: The expansion is local to the present node.
			v = c.currentVnode() ; n = v.level()
			after = v.nodeAfterTree()
			while v and v != after:
				if v.level() - n + 1 < level:
					v.expand()
				else:
					v.contract()
				v = v.threadNext()
		else: # The expansion is global
			# Start the recursion.
			# First contract everything.
			c.contractAllHeadlines()
			v = c.rootVnode()
			while v:
				c.expandTreeToLevelFromLevel(v,level,1)
				v = v.next()
		c.expansionLevel = level
		c.expansionNode = c.currentVnode()
		c.endUpdate()
	#@nonl
	#@-node:expandToLevel
	#@+node:goNextVisitedNode
	def goNextVisitedNode(self):
		
		c = self
	
		while c.beadPointer + 1 < len(c.beadList):
			c.beadPointer += 1
			v = c.beadList[c.beadPointer]
			if v.exists(c):
				c.beginUpdate()
				c.frame.tree.expandAllAncestors(v)
				c.selectVnode(v,updateBeadList=false)
				c.endUpdate()
				c.frame.tree.idle_scrollTo(v)
				return
	#@nonl
	#@-node:goNextVisitedNode
	#@+node:goPrevVisitedNode
	def goPrevVisitedNode(self):
		
		c = self
	
		while c.beadPointer > 0:
			c.beadPointer -= 1
			v = c.beadList[c.beadPointer]
			if v.exists(c):
				c.beginUpdate()
				c.frame.tree.expandAllAncestors(v)
				c.selectVnode(v,updateBeadList=false)
				c.endUpdate()
				c.frame.tree.idle_scrollTo(v)
				return
	#@-node:goPrevVisitedNode
	#@+node:goToFirstNode
	def goToFirstNode(self):
		
		c = self
		v = c.rootVnode()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:goToFirstNode
	#@+node:goToLastNode
	def goToLastNode(self):
		
		c = self
		v = c.rootVnode()
		while v and v.threadNext():
			v = v.threadNext()
		if v:
			c.beginUpdate()
			c.frame.tree.expandAllAncestors(v)
			c.selectVnode(v)
			c.endUpdate()
	
	#@-node:goToLastNode
	#@+node:goToNextClone
	def goToNextClone(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		if not current.isCloned(): return
	
		v = current.threadNext()
		while v and v.t != current.t:
			v = v.threadNext()
			
		if not v:
			# Wrap around.
			v = c.rootVnode()
			while v and v != current and v.t != current.t:
				v = v.threadNext()
	
		if v:
			c.beginUpdate()
			c.endEditing()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:goToNextClone
	#@+node:goToNextDirtyHeadline
	def goToNextDirtyHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		while v and not v.isDirty():
			v = v.threadNext()
		if not v:
			v = c.rootVnode()
			while v and not v.isDirty():
				v = v.threadNext()
		if v:
			c.selectVnode(v)
	#@nonl
	#@-node:goToNextDirtyHeadline
	#@+node:goToNextMarkedHeadline
	def goToNextMarkedHeadline(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		while v and not v.isMarked():
			v = v.threadNext()
		if v:
			c.beginUpdate()
			c.endEditing()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:goToNextMarkedHeadline
	#@+node:goToNextSibling
	def goToNextSibling(self):
		
		c = self
		v = c.currentVnode()
		if not v: return
		next = v.next()
		if next:
			c.beginUpdate()
			c.selectVnode(next)
			c.endUpdate()
	#@nonl
	#@-node:goToNextSibling
	#@+node:goToParent
	def goToParent(self):
		
		c = self
		v = c.currentVnode()
		if not v: return
		p = v.parent()
		if p:
			c.beginUpdate()
			c.selectVnode(p)
			c.endUpdate()
	#@-node:goToParent
	#@+node:goToPrevSibling
	def goToPrevSibling(self):
		
		c = self
		v = c.currentVnode()
		if not v: return
		back = v.back()
		if back:
			c.beginUpdate()
			c.selectVnode(back)
			c.endUpdate()
	#@-node:goToPrevSibling
	#@+node:markChangedHeadlines
	def markChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				v.setMarked()
				c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markChangedHeadlines
	#@+node:markChangedRoots
	def markChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				s = v.bodyString()
				flag, i = is_special(s,0,"@root")
				if flag:
					v.setMarked()
					c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markChangedRoots
	#@+node:markAllAtFileNodesDirty
	def markAllAtFileNodesDirty (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isAtFileNode()and not v.isDirty():
				v.setDirty()
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markAllAtFileNodesDirty
	#@+node:markAtFileNodesDirty
	def markAtFileNodesDirty (self):
	
		c = self
		v = c.currentVnode()
		if not v: return
		after = v.nodeAfterTree()
		c.beginUpdate()
		while v and v != after:
			if v.isAtFileNode() and not v.isDirty():
				v.setDirty()
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markAtFileNodesDirty
	#@+node:markClones
	def markClones (self):
	
		c = self ; current = v = c.currentVnode()
		if not v: return
		if not v.isCloned(): return
		
		v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.t == current.t:
				v.setMarked()
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markClones
	#@+node:markHeadline
	def markHeadline (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		c.beginUpdate()
		if v.isMarked():
			v.clearMarked()
		else:
			v.setMarked()
			v.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:markHeadline
	#@+node:markSubheads
	def markSubheads(self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		while child:
			if not child.isMarked():
				child.setMarked()
				child.setDirty()
				c.setChanged(true)
			child = child.next()
		c.endUpdate()
	#@nonl
	#@-node:markSubheads
	#@+node:unmarkAll
	def unmarkAll(self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isMarked():
				v.clearMarked()
				v.setDirty()
				c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:unmarkAll
	#@+node:demote
	def demote(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.next(): return
		last = v.lastChild() # EKR: 3/19/03
		# Make sure all the moves will be valid.
		child = v.next()
		while child:
			if not c.checkMoveWithParentWithWarning(child,v,true):
				return
			child = child.next()
		c.beginUpdate()
		if 1: # update range...
			c.mInhibitOnTreeChanged = true
			c.endEditing()
			while v.next():
				child = v.next()
				child.moveToNthChildOf(v,v.numberOfChildren())
			v.expand()
			c.selectVnode(v)
			v.setDirty()
			c.setChanged(true)
			c.mInhibitOnTreeChanged = false
			c.initAllCloneBits() # 7/6/02
		c.endUpdate()
		c.undoer.setUndoParams("Demote",v,lastChild=last)
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:demote
	#@+node:moveOutlineDown
	#@+at 
	#@nonl
	# Moving down is more tricky than moving up; we can't move v to be a child 
	# of itself.  An important optimization:  we don't have to call 
	# checkMoveWithParentWithWarning() if the parent of the moved node remains 
	# the same.
	#@-at
	#@@c
	
	def moveOutlineDown(self):
	
		c = self
		v = c.currentVnode()
		if not v: return
		if not c.canMoveOutlineDown(): # 11/4/03: Support for hoist.
			if c.hoistStack: es("Can't move node out of hoisted outline",color="blue")
			return
		# Set next to the node after which v will be moved.
		next = v.visNext()
		while next and v.isAncestorOf(next):
			next = next.visNext()
		if not next: return
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			#@		<< Move v down >>
			#@+node:<< Move v down >>
			# Remember both the before state and the after state for undo/redo
			oldBack = v.back()
			oldParent = v.parent()
			oldN = v.childIndex()
			
			if next.hasChildren() and next.isExpanded():
				# Attempt to move v to the first child of next.
				if c.checkMoveWithParentWithWarning(v,next,true):
					v.moveToNthChildOf(next,0)
					c.undoer.setUndoParams("Move Down",v,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			else:
				# Attempt to move v after next.
				if c.checkMoveWithParentWithWarning(v,next.parent(),true):
					v.moveAfter(next)
					c.undoer.setUndoParams("Move Down",v,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			#@nonl
			#@-node:<< Move v down >>
			#@nl
			v.setDirty() # This second call is essential.
			c.selectVnode(v)# 4/23/01
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:moveOutlineDown
	#@+node:moveOutlineLeft
	def moveOutlineLeft(self):
		
		# clear_stats() ; # stat()
		c = self
		v = c.currentVnode()
		if not v: return
		if not c.canMoveOutlineLeft(): # 11/4/03: Support for hoist.
			if c.hoistStack: es("Can't move node out of hoisted outline",color="blue")
			return
		parent = v.parent()
		if not parent: return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			v.moveAfter(parent)
			c.undoer.setUndoParams("Move Left",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
		# print_stats()
	#@nonl
	#@-node:moveOutlineLeft
	#@+node:moveOutlineRight
	def moveOutlineRight(self):
		
		# clear_stats() ; # stat()
		c = self
		v = c.currentVnode()
		if not v: return
		if not c.canMoveOutlineRight(): # 11/4/03: Support for hoist.
			if c.hoistStack: es("Can't move node out of hoisted outline",color="blue")
			return
		back = v.back()
		if not back: return
		if not c.checkMoveWithParentWithWarning(v,back,true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			n = back.numberOfChildren()
			v.moveToNthChildOf(back,n)
			c.undoer.setUndoParams("Move Right",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 7/6/02
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
		# print_stats()
	#@nonl
	#@-node:moveOutlineRight
	#@+node:moveOutlineUp
	def moveOutlineUp(self):
	
		c = self
		v = c.currentVnode()
		if not v: return
		if not c.canMoveOutlineUp(): # 11/4/03: Support for hoist.
			if c.hoistStack: es("Can't move node out of hoisted outline",color="blue")
			return
		back = v.visBack()
		if not back: return
		back2 = back.visBack()
		if v in back2.t.joinList:
			# 1/26/04: A weird special case: just select back2.
			c.selectVnode(back2)
			return
		c = self
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			#@		<< Move v up >>
			#@+node:<< Move v up >>
			# Remember both the before state and the after state for undo/redo
			oldBack = v.back()
			oldParent = v.parent()
			oldN = v.childIndex()
			
			if not back2:
				# v will be the new root node
				v.moveToRoot(c.rootVnode()) # 3/16/02, 5/17/02
				c.undoer.setUndoParams("Move Up",v,
					oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			elif back2.hasChildren() and back2.isExpanded():
				if c.checkMoveWithParentWithWarning(v,back2,true):
					v.moveToNthChildOf(back2,0)
					c.undoer.setUndoParams("Move Up",v,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			elif c.checkMoveWithParentWithWarning(v,back2.parent(),true):
				# Insert after back2.
				v.moveAfter(back2)
				c.undoer.setUndoParams("Move Up",v,
					oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			#@nonl
			#@-node:<< Move v up >>
			#@nl
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	
	#@-node:moveOutlineUp
	#@+node:promote
	def promote(self):
	
		c = self
		v = c.currentVnode()
		if not v or not v.hasChildren(): return
		last = v.lastChild() # EKR: 3/19/03
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			after = v
			while v.hasChildren():
				child = v.firstChild()
				child.moveAfter(after)
				after = child
			v.setDirty()
			c.setChanged(true)
			c.selectVnode(v)
		c.endUpdate()
		c.undoer.setUndoParams("Promote",v,lastChild=last)
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:promote
	#@+node:openCompareWindow
	def openCompareWindow (self):
		
		c = self ; frame = c.frame
		
		if not frame.comparePanel:
			frame.comparePanel = app.gui.createComparePanel(c)
	
		frame.comparePanel.bringToFront()
	#@nonl
	#@-node:openCompareWindow
	#@+node:openPythonWindow (Dave Hein)
	def openPythonWindow(self):
	
		if sys.platform == "linux2":
			#@		<< open idle in Linux >>
			#@+node:<< open idle in Linux >>
			# 09-SEP-2002 DHEIN: Open Python window under linux
			
			try:
				pathToLeo = os_path_join(app.loadDir,"leo.py")
				sys.argv = [pathToLeo]
				from idlelib import idle
				if app.idle_imported:
					reload(idle)
				app.idle_imported = true
			except:
				try:
					es("idlelib could not be imported.")
					es("Probably IDLE is not installed.")
					es("Run Tools/idle/setup.py to build idlelib.")
					es("Can not import idle")
					es_exception() # This can fail!!
				except: pass
			#@-node:<< open idle in Linux >>
			#@nl
		else:
			#@		<< open idle in Windows >>
			#@+node:<< open idle in Windows >>
			# Initialize argv: the -t option sets the title of the Idle interp window.
			sys.argv = ["leo","-t","leo"]
			
			ok = false
			#@<< Try to open idle in pre-Python 2.3 systems>>
			#@+node:<< Try to open idle in pre-Python 2.3 systems>>
			try:
				executable_dir = os_path_dirname(sys.executable)
				idle_dir = os_path_join(executable_dir,"Tools","idle")
			
				if idle_dir not in sys.path:
					sys.path.append(idle_dir)
			
				import PyShell
					
				if app.idle_imported:
					reload(idle)
					app.idle_imported = true
					
				if 1: # Mostly works, but causes problems when opening other .leo files.
					PyShell.main()
				else: # Doesn't work: destroys all of Leo when Idle closes.
					self.leoPyShellMain()
				ok = true
			except:
				ok = false
				# es_exception()
			#@nonl
			#@-node:<< Try to open idle in pre-Python 2.3 systems>>
			#@nl
			
			if not ok:
				#@	<< Try to open idle in Python 2.3 systems >>
				#@+node:<< Try to open idle in Python 2.3 systems >>
				try:
					idle_dir = None
					
					import idlelib.PyShell
				
					if app.idle_imported:
						reload(idle)
						app.idle_imported = true
						
					idlelib.PyShell.main()
					ok = true
				
				except:
					ok = false
					es_exception()
				#@nonl
				#@-node:<< Try to open idle in Python 2.3 systems >>
				#@nl
			
			if not ok:
				es("Can not import idle")
				if idle_dir and idle_dir not in sys.path:
					es("Please add '%s' to sys.path" % idle_dir)
			#@nonl
			#@-node:<< open idle in Windows >>
			#@nl
	#@-node:openPythonWindow (Dave Hein)
	#@+node:leoPyShellMain
	#@+at 
	#@nonl
	# The key parts of Pyshell.main(), but using Leo's root window instead of 
	# a new Tk root window.
	# 
	# This does _not_ work well.  Using Leo's root window means that Idle will 
	# shut down Leo without warning when the Idle window is closed!
	#@-at
	#@@c
	
	def leoPyShellMain(self):
		
		import PyShell
		root = app.root
		PyShell.fixwordbreaks(root)
		flist = PyShell.PyShellFileList(root)
		shell = PyShell.PyShell(flist)
		flist.pyshell = shell
		shell.begin()
	#@nonl
	#@-node:leoPyShellMain
	#@+node:about (version number & date)
	def about(self):
		
		c = self
		
		# Don't use triple-quoted strings or continued strings here.
		# Doing so would add unwanted leading tabs.
		version = c.getSignOnLine() + "\n\n"
		copyright = (
			"Copyright 1999-2003 by Edward K. Ream\n" +
			"All Rights Reserved\n" +
			"Leo is distributed under the Python License")
		url = "http://webpages.charter.net/edreamleo/front.html"
		email = "edreamleo@charter.net"
	
		app.gui.runAboutLeoDialog(version,copyright,url,email)
	#@nonl
	#@-node:about (version number & date)
	#@+node:leoDocumentation
	def leoDocumentation (self):
		
		c = self
	
		fileName = os_path_join(app.loadDir,"..","doc","LeoDocs.leo")
	
		try:
			openWithFileName(fileName,c)
		except:
			es("not found: LeoDocs.leo")
	#@-node:leoDocumentation
	#@+node:leoHome
	def leoHome (self):
		
		import webbrowser
	
		url = "http://webpages.charter.net/edreamleo/front.html"
		try:
			webbrowser.open_new(url)
		except:
			es("not found: " + url)
	#@nonl
	#@-node:leoHome
	#@+node:leoTutorial (version number)
	def leoTutorial (self):
		
		import webbrowser
	
		if 1: # new url
			url = "http://www.3dtree.com/ev/e/sbooks/leo/sbframetoc_ie.htm"
		else:
			url = "http://www.evisa.com/e/sbooks/leo/sbframetoc_ie.htm"
		try:
			webbrowser.open_new(url)
		except:
			es("not found: " + url)
	#@nonl
	#@-node:leoTutorial (version number)
	#@+node:leoConfig
	def leoConfig (self):
	
		# 4/21/03 new code suggested by fBechmann@web.de
		c = self
		loadDir = app.loadDir
		configDir = app.config.configDir
	
		# Look in configDir first.
		fileName = os_path_join(configDir, "leoConfig.leo")
	
		ok, frame = openWithFileName(fileName,c)
		if not ok:
			if configDir == loadDir:
				es("leoConfig.leo not found in " + loadDir)
			else:
				# Look in loadDir second.
				fileName = os_path_join(loadDir,"leoConfig.leo")
	
				ok, frame = openWithFileName(fileName,c)
				if not ok:
					es("leoConfig.leo not found in " + configDir + " or " + loadDir)
	#@nonl
	#@-node:leoConfig
	#@+node:applyConfig
	def applyConfig (self):
	
		c = self
		app.config.init()
		c.frame.reconfigureFromConfig()
	#@nonl
	#@-node:applyConfig
	#@+node:c.dragAfter
	def dragAfter(self,v,after):
	
		c = self
		if not c.checkMoveWithParentWithWarning(v,after.parent(),true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			v.moveAfter(after)
			c.undoer.setUndoParams("Drag",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragAfter
	#@+node:c.dragCloneToNthChildOf (changed in 3.11.1)
	def dragCloneToNthChildOf (self,v,parent,n):
	
		c = self
		c.beginUpdate()
		# trace("v,parent,n:"+v.headString()+","+parent.headString()+","+`n`)
		clone = v.clone(v) # Creates clone & dependents, does not set undo.
		if not c.checkMoveWithParentWithWarning(clone,parent,true):
			clone.doDelete(v) # Destroys clone & dependents. Makes v the current node.
			c.endUpdate(false) # Nothing has changed.
			return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.endEditing()
		clone.setDirty()
		clone.moveToNthChildOf(parent,n)
		c.initJoinedCloneBits(clone) # Bug fix: 4/29/03
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		clone.setDirty()
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragCloneToNthChildOf (changed in 3.11.1)
	#@+node:c.dragToNthChildOf
	def dragToNthChildOf(self,v,parent,n):
	
		# es("dragToNthChildOf")
		c = self
		if not c.checkMoveWithParentWithWarning(v,parent,true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			v.moveToNthChildOf(parent,n)
			c.undoer.setUndoParams("Drag",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragToNthChildOf
	#@+node:c.dragCloneAfter
	def dragCloneAfter (self,v,after):
	
		c = self
		c.beginUpdate()
		clone = v.clone(v) # Creates clone & dependents, does not set undo.
		# trace("v,after:",v.headString(),after.headString())
		if not c.checkMoveWithParentWithWarning(clone,after.parent(),true):
			trace("invalid clone move")
			clone.doDelete(v) # Destroys clone & dependents. Makes v the current node.
			c.endUpdate(false) # Nothing has changed.
			return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.endEditing()
		clone.setDirty()
		clone.moveAfter(after)
		c.initJoinedCloneBits(clone) # Bug fix: 4/29/03
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		clone.setDirty()
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragCloneAfter
	#@+node:beginUpdate
	def beginUpdate(self):
	
		self.frame.tree.beginUpdate()
		
	BeginUpdate = beginUpdate # Compatibility with old scripts
	#@nonl
	#@-node:beginUpdate
	#@+node:bringToFront
	def bringToFront(self):
	
		self.frame.deiconify()
	
	BringToFront = bringToFront # Compatibility with old scripts
	#@nonl
	#@-node:bringToFront
	#@+node:endUpdate
	def endUpdate(self, flag=true):
		
		self.frame.tree.endUpdate(flag)
		
	EndUpdate = endUpdate # Compatibility with old scripts
	#@nonl
	#@-node:endUpdate
	#@+node:recolor
	def recolor(self):
	
		c = self ; frame = c.frame
		frame.body.recolor(frame.tree.currentVnode())
	#@nonl
	#@-node:recolor
	#@+node:redraw & repaint
	def redraw(self):
	
		self.frame.tree.redraw()
		
	# Compatibility with old scripts
	Redraw = redraw 
	repaint = redraw
	Repaint = redraw
	#@nonl
	#@-node:redraw & repaint
	#@+node:canContractAllHeadlines
	def canContractAllHeadlines (self):
	
		c = self ; v = c.rootVnode()
		if not v: return false
		while v:
			if v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canContractAllHeadlines
	#@+node:canContractAllSubheads
	def canContractAllSubheads (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		next = v.nodeAfterTree()
		v = v.threadNext()
		while v and v != next:
			if v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canContractAllSubheads
	#@+node:canContractParent
	def canContractParent (self):
	
		c = self ; v = c.currentVnode()
		return v.parent() != None
	#@nonl
	#@-node:canContractParent
	#@+node:canContractSubheads
	def canContractSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		v = v.firstChild()
		while v:
			if v.isExpanded():
				return true
			v = v.next()
		return false
	#@nonl
	#@-node:canContractSubheads
	#@+node:canCutOutline & canDeleteHeadline
	def canDeleteHeadline (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		if v.parent(): # v is below the top level.
			return true
		else: # v is at the top level.  We can not delete the last node.
			return v.threadBack() or v.next()
	
	canCutOutline = canDeleteHeadline
	#@nonl
	#@-node:canCutOutline & canDeleteHeadline
	#@+node:canDemote
	def canDemote (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		return v.next() != None
	#@nonl
	#@-node:canDemote
	#@+node:canExpandAllHeadlines
	def canExpandAllHeadlines (self):
	
		c = self ; v = c.rootVnode()
		if not v: return false
		while v:
			if not v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canExpandAllHeadlines
	#@+node:canExpandAllSubheads
	def canExpandAllSubheads (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		next = v.nodeAfterTree()
		v = v.threadNext()
		while v and v != next:
			if not v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canExpandAllSubheads
	#@+node:canExpandSubheads
	def canExpandSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		v = v.firstChild()
		while v:
			if not v.isExpanded():
				return true
			v = v.next()
		return false
	#@nonl
	#@-node:canExpandSubheads
	#@+node:canExtract, canExtractSection & canExtractSectionNames
	def canExtract (self):
	
		c = self ; body = c.frame.body
		return body and body.hasTextSelection()
		
	canExtractSectionNames = canExtract
			
	def canExtractSection (self):
	
		c = self ; body = c.frame.body
		if not body: return false
		
		s = body.getSelectedText()
		if not s: return false
	
		line = get_line(s,0)
		i1 = line.find("<<")
		j1 = line.find(">>")
		i2 = line.find("@<")
		j2 = line.find("@>")
		return -1 < i1 < j1 or -1 < i2 < j2
	#@nonl
	#@-node:canExtract, canExtractSection & canExtractSectionNames
	#@+node:canFindMatchingBracket
	def canFindMatchingBracket (self):
		
		c = self ; brackets = "()[]{}"
		c1 = c.frame.body.getCharAtInsertPoint()
		c2 = c.frame.body.getCharBeforeInsertPoint()
		return (c1 and c1 in brackets) or (c2 and c2 in brackets)
	#@nonl
	#@-node:canFindMatchingBracket
	#@+node:canGoToNextDirtyHeadline
	def canGoToNextDirtyHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return false
	
		v = c.rootVnode()
		while v:
			if v.isDirty()and v != current:
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canGoToNextDirtyHeadline
	#@+node:canGoToNextMarkedHeadline
	def canGoToNextMarkedHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return false
	
		v = c.rootVnode()
		while v:
			if v.isMarked()and v != current:
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canGoToNextMarkedHeadline
	#@+node:canMarkChangedHeadline
	def canMarkChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canMarkChangedHeadline
	#@+node:canMarkChangedRoots
	def canMarkChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canMarkChangedRoots
	#@+node:canMoveOutlineDown (changed for hoist)
	def canMoveOutlineDown (self):
	
		c = self
		if 1: # The permissive way
			current = c.currentVnode()
			if not current: return false
			v = current.visNext()
			while v and current.isAncestorOf(v):
				v = v.visNext()
				
			if c.hoistStack:
				h = c.hoistStack[-1]
				return v and v != h and h.isAncestorOf(v)
			else:
				return v != None
		else: # The MORE way.
			return c.currentVnode().next() != None
	#@nonl
	#@-node:canMoveOutlineDown (changed for hoist)
	#@+node:canMoveOutlineLeft (changed for hoist)
	def canMoveOutlineLeft (self):
	
		c = self ; v = c.currentVnode()
		if c.hoistStack:
			h = c.hoistStack[-1]
			if v and v.parent():
				p = v.parent()
				return p != h and h.isAncestorOf(p)
			else:
				return false
		else:
			return v and v.parent()
	#@nonl
	#@-node:canMoveOutlineLeft (changed for hoist)
	#@+node:canMoveOutlineRight (changed for hoist)
	def canMoveOutlineRight (self):
	
		c = self ; v = c.currentVnode()
		if c.hoistStack:
			h = c.hoistStack[-1]
			return v and v.back() and v != h
		else:
			return v and v.back()
	#@nonl
	#@-node:canMoveOutlineRight (changed for hoist)
	#@+node:canMoveOutlineUp (changed for hoist)
	def canMoveOutlineUp (self):
	
		c = self ; v = c.currentVnode()
		if 1: # The permissive way.
			if c.hoistStack:
				h = c.hoistStack[-1] ; vback = v.visBack()
				return v and vback and h != v and h.isAncestorOf(vback)
			else:
				return v and v.visBack()
		else: # The MORE way.
			return v and v.back()
	#@nonl
	#@-node:canMoveOutlineUp (changed for hoist)
	#@+node:canPasteOutline
	def canPasteOutline (self,s=None):
	
		c = self
		if s == None:
			s = app.gui.getTextFromClipboard()
		if not s:
			return false
	
		# trace(s)
		if match(s,0,app.prolog_prefix_string):
			return true
		elif len(s) > 0:
			return c.importCommands.stringIsValidMoreFile(s)
		else:
			return false
	#@nonl
	#@-node:canPasteOutline
	#@+node:canPromote
	def canPromote (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
	#@nonl
	#@-node:canPromote
	#@+node:canRevert
	def canRevert (self):
	
		# c.mFileName will be "untitled" for unsaved files.
		c = self
		return (c.frame and c.mFileName and c.isChanged())
	#@nonl
	#@-node:canRevert
	#@+node:canSelect....
	# 7/29/02: The shortcuts for these commands are now unique.
	
	def canSelectThreadBack (self):
		v = self.currentVnode()
		return v and v.threadBack()
		
	def canSelectThreadNext (self):
		v = self.currentVnode()
		return v and v.threadNext()
	
	def canSelectVisBack (self):
		v = self.currentVnode()
		return v and v.visBack()
		
	def canSelectVisNext (self):
		v = self.currentVnode()
		return v and v.visNext()
	#@nonl
	#@-node:canSelect....
	#@+node:canShiftBodyLeft/Right
	def canShiftBodyLeft (self):
	
		c = self
		if c.frame.body:
			s = c.frame.body.getAllText()
			return s and len(s) > 0
		else:
			return false
			
	def canShiftBodyRight (self):
	
		c = self
		if c.frame.body:
			s = c.frame.body.getAllText()
			return s and len(s) > 0
		else:
			return false
	#@nonl
	#@-node:canShiftBodyLeft/Right
	#@+node:canSortChildren, canSortSiblings
	def canSortChildren (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
		
	def canSortSiblings (self):
	
		c = self ; v = c.currentVnode()
		return v.next() or v.back()
	#@nonl
	#@-node:canSortChildren, canSortSiblings
	#@+node:canUndo & canRedo
	def canUndo (self):
	
		c = self
		return c.undoer.canUndo()
		
	def canRedo (self):
	
		c = self
		return c.undoer.canRedo()
	#@nonl
	#@-node:canUndo & canRedo
	#@+node:canUnmarkAll
	# Returns true if any node is marked.
	
	def canUnmarkAll (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isMarked():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canUnmarkAll
	#@+node:currentVnode
	# Compatibility with scripts
	
	def currentVnode (self):
	
		return self.frame.tree.currentVnode()
	#@-node:currentVnode
	#@+node:clearAllMarked
	def clearAllMarked (self):
	
		c = self ; v = c.rootVnode()
		while v:
			v.clearMarked()
			v = v.threadNext()
	#@nonl
	#@-node:clearAllMarked
	#@+node:clearAllVisited
	def clearAllVisited (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			# tick("clearAllVisited loop")
			v.clearVisited()
			if v.t:
				v.t.clearVisited()
			v = v.threadNext()
		c.endUpdate(false) # never redraw the tree.
	#@nonl
	#@-node:clearAllVisited
	#@+node:fileName
	# Compatibility with scripts
	
	def fileName (self):
	
		return self.mFileName
	#@-node:fileName
	#@+node:isChanged
	def isChanged (self):
	
		return self.changed
	#@nonl
	#@-node:isChanged
	#@+node:rootVnode
	# Compatibility with scripts
	
	def rootVnode (self):
	
		return self.frame.tree.rootVnode()
	#@-node:rootVnode
	#@+node:c.setChanged
	def setChanged (self,changedFlag):
	
		c = self
		if not c.frame: return
		# Clear all dirty bits _before_ setting the caption.
		# 9/15/01 Clear all dirty bits except orphaned @file nodes
		if not changedFlag:
			# trace("clearing all dirty bits")
			v = c.rootVnode()
			while v:
				if v.isDirty() and not (v.isAtFileNode() or v.isAtRawFileNode()):
					v.clearDirtyJoined()
				v = v.threadNext()
		# Update all derived changed markers.
		c.changed = changedFlag
		s = c.frame.getTitle()
		if len(s) > 2 and not c.loading: # don't update while loading.
			if changedFlag:
				# import traceback ; traceback.print_stack()
				if s [0] != '*': c.frame.setTitle("* " + s)
			else:
				if s[0:2]=="* ": c.frame.setTitle(s[2:])
	#@nonl
	#@-node:c.setChanged
	#@+node:editVnode (calls tree.editLabel)
	# Selects v: sets the focus to v and edits v.
	
	def editVnode(self,v):
	
		c = self
	
		if v:
			c.selectVnode(v)
			c.frame.tree.editLabel(v)
	#@nonl
	#@-node:editVnode (calls tree.editLabel)
	#@+node:endEditing (calls tree.endEditLabel)
	# Ends the editing in the outline.
	
	def endEditing(self):
	
		self.frame.tree.endEditLabel()
	#@-node:endEditing (calls tree.endEditLabel)
	#@+node:selectThreadBack
	def selectThreadBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.threadBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-node:selectThreadBack
	#@+node:selectThreadNext
	def selectThreadNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:selectThreadNext
	#@+node:selectVisBack
	# This has an up arrow for a control key.
	
	def selectVisBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.visBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:selectVisBack
	#@+node:selectVisNext
	def selectVisNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.visNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-node:selectVisNext
	#@+node:selectVnode (calls tree.select)
	def selectVnode(self,v,updateBeadList=true):
		
		"""Select a new vnode."""
	
		# All updating and "synching" of nodes are now done in the event handlers!
		c = self
		c.frame.tree.endEditLabel()
		c.frame.tree.select(v,updateBeadList)
		c.frame.body.setFocus()
		self.editing = false
	#@nonl
	#@-node:selectVnode (calls tree.select)
	#@+node:selectVnodeWithEditing
	# Selects the given node and enables editing of the headline if editFlag is true.
	
	def selectVnodeWithEditing(self,v,editFlag):
	
		c = self
		if editFlag:
			c.editVnode(v)
		else:
			c.selectVnode(v)
	#@-node:selectVnodeWithEditing
	#@+node:Syntax coloring interface
	#@+at 
	#@nonl
	# These routines provide a convenient interface to the syntax colorer.
	#@-at
	#@-node:Syntax coloring interface
	#@+node:updateSyntaxColorer
	def updateSyntaxColorer(self,v):
	
		self.frame.body.updateSyntaxColorer(v)
	#@-node:updateSyntaxColorer
	#@-others

class Commands (baseCommands):
	"""A class that implements most of Leo's commands."""
	pass
#@nonl
#@-node:@file leoCommands.py
#@-leo
