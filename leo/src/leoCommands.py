#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2810:@thin leoCommands.py
#@@language python

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoAtFile,leoFileCommands,leoImport,leoNodes,leoTangle,leoUndo
import os
import string
import sys
import tempfile

class baseCommands:
	"""The base class for Leo's main commander."""
	#@	@+others
	#@+node:ekr.20031218072017.2811: c.Birth & death
	#@+node:ekr.20031218072017.2812:c.__init__, initIvars
	def __init__(self,frame,fileName):
	
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
		#@+node:ekr.20031218072017.2813:<< initialize ivars >>
		self._currentPosition = self.nullPosition()
		self._rootPosition    = self.nullPosition()
		self._topPosition     = self.nullPosition()
		
		# per-document info...
		self.hookFunction = None
		self.openDirectory = None
		
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
		#@-node:ekr.20031218072017.2813:<< initialize ivars >>
		#@nl
		self.setIvarsFromFind()
	#@nonl
	#@-node:ekr.20031218072017.2812:c.__init__, initIvars
	#@+node:ekr.20031218072017.2814:c.__repr__ & __str__
	def __repr__ (self):
		
		try:
			return "Commander %d: %s" % (id(self),repr(self.mFileName))
		except:
			return "Commander: %d: bad mFileName" % id(self)
			
	__str__ = __repr__
	
	#@-node:ekr.20031218072017.2814:c.__repr__ & __str__
	#@+node:ekr.20031218072017.2815:c.setIvarsFromFind
	# This should be called whenever we need to use find values:
	# i.e., before reading or writing
	
	def setIvarsFromFind (self):
	
		c = self ; find = g.app.findFrame
		if find != None:
			find.set_ivars(c)
	#@-node:ekr.20031218072017.2815:c.setIvarsFromFind
	#@+node:ekr.20031218072017.2816:c.setIvarsFromPrefs
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
	#@-node:ekr.20031218072017.2816:c.setIvarsFromPrefs
	#@-node:ekr.20031218072017.2811: c.Birth & death
	#@+node:ekr.20031218072017.2817: doCommand
	def doCommand (self,command,label,event=None):
	
		"""Execute the given command, invoking hooks and catching exceptions.
		
		The code assumes that the "command1" hook has completely handled the command if
		g.doHook("command1") returns false.
		This provides a simple mechanism for overriding commands."""
		
		c = self ; p = c.currentPosition()
	
		# A horrible kludge: set g.app.log to cover for a possibly missing activate event.
		g.app.setLog(c.frame.log,"doCommand")
	
		if label == "cantredo": label = "redo"
		if label == "cantundo": label = "undo"
		g.app.commandName = label
	
		if not g.doHook("command1",c=c,v=p,label=label):
			try:
				command()
			except:
				g.es("exception executing command")
				print "exception executing command"
				g.es_exception(c=c)
				c.frame.tree.redrawAfterException() # 1/26/04
		
		g.doHook("command2",c=c,v=p,label=label)
				
		return "break" # Inhibit all other handlers.
	#@nonl
	#@-node:ekr.20031218072017.2817: doCommand
	#@+node:ekr.20031218072017.2582: version & signon stuff
	def getBuildNumber(self):
		c = self
		return c.ver[10:-1] # Strip off "(dollar)Revision" and the trailing "$"
	
	def getSignOnLine (self):
		c = self
		return "Leo 4.2 alpha 3, build %s, June 1, 2004" % c.getBuildNumber()
		
	def initVersion (self):
		c = self
		c.ver = "$Revision$" # CVS will update this.
		
	def signOnWithVersion (self):
	
		c = self
		color = g.app.config.getWindowPref("log_error_color")
		signon = c.getSignOnLine()
		n1,n2,n3,junk,junk=sys.version_info
		tkLevel = c.frame.top.getvar("tk_patchLevel")
		
		g.es("Leo Log Window...",color=color)
		g.es(signon)
		g.es("Python %d.%d.%d, Tk %s, %s" % (n1,n2,n3,tkLevel,sys.platform))
		g.enl()
	#@nonl
	#@-node:ekr.20031218072017.2582: version & signon stuff
	#@+node:ekr.20040312090934:c.iterators
	#@+node:EKR.20040529091232:c.all_positions_iter == allNodes_iter
	def allNodes_iter(self,copy=false):
		
		c = self
		return c.rootPosition().allNodes_iter(copy)
		
	all_positions_iter = allNodes_iter
	#@nonl
	#@-node:EKR.20040529091232:c.all_positions_iter == allNodes_iter
	#@+node:EKR.20040529091232.1:c.all_tnodes_iter
	def all_tnodes_iter(self):
		
		c = self
		for p in c.all_positions_iter():
			yield p.v.t
	
		# return c.rootPosition().all_tnodes_iter(all=true)
	#@nonl
	#@-node:EKR.20040529091232.1:c.all_tnodes_iter
	#@+node:EKR.20040529091232.2:c.all_unique_tnodes_iter
	def all_unique_tnodes_iter(self):
		
		c = self ; marks = {}
		
		for p in c.all_positions_iter():
			if not p.v.t in marks:
				marks[p.v.t] = p.v.t
				yield p.v.t
	#@nonl
	#@-node:EKR.20040529091232.2:c.all_unique_tnodes_iter
	#@+node:EKR.20040529091232.3:c.all_vnodes_iter
	def all_vnodes_iter(self):
		
		c = self
		for p in c.all_positions_iter():
			yield p.v
	#@nonl
	#@-node:EKR.20040529091232.3:c.all_vnodes_iter
	#@+node:EKR.20040529091232.4:c.all_unique_vnodes_iter
	def all_unique_vnodes_iter(self):
		
		c = self ; marks = {}
		for p in c.all_positions_iter():
			if not p.v in marks:
				marks[p.v] = p.v
				yield p.v
	#@nonl
	#@-node:EKR.20040529091232.4:c.all_unique_vnodes_iter
	#@-node:ekr.20040312090934:c.iterators
	#@+node:ekr.20031218072017.2818:Command handlers...
	#@+node:ekr.20031218072017.2819:File Menu
	#@+node:ekr.20031218072017.2820:top level
	#@+node:ekr.20031218072017.1623:new
	def new (self):
	
		c,frame = g.app.gui.newLeoCommanderAndFrame(fileName=None)
		
		# 5/16/03: Needed for hooks.
		g.doHook("new",old_c=self,new_c=c)
		
		# Use the config params to set the size and location of the window.
		frame.setInitialWindowGeometry()
		frame.deiconify()
		frame.lift()
		frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio) # Resize the _new_ frame.
		
		c.beginUpdate()
		if 1: # within update
			t = leoNodes.tnode()
			v = leoNodes.vnode(c,t)
			p = leoNodes.position(v,[])
			v.initHeadString("NewHeadline")
			v.moveToRoot()
			c.editPosition(p)
		c.endUpdate()
	
		frame.body.setFocus()
	#@nonl
	#@-node:ekr.20031218072017.1623:new
	#@+node:ekr.20031218072017.2821:open
	def open(self):
	
		c = self
		#@	<< Set closeFlag if the only open window is empty >>
		#@+node:ekr.20031218072017.2822:<< Set closeFlag if the only open window is empty >>
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
			g.app.numberOfWindows == 1) # Only one untitled window has ever been opened
		#@-node:ekr.20031218072017.2822:<< Set closeFlag if the only open window is empty >>
		#@nl
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Open",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if fileName and len(fileName) > 0:
			ok, frame = g.openWithFileName(fileName,c)
			if ok and closeFlag:
				g.app.destroyWindow(c.frame)
	#@nonl
	#@-node:ekr.20031218072017.2821:open
	#@+node:ekr.20031218072017.2823:openWith and allies
	def openWith(self,data=None):
	
		"""This routine handles the items in the Open With... menu.
	
		These items can only be created by createOpenWithMenuFromTable().
		Typically this would be done from the "open2" hook."""
		
		c = self ; v = c.currentVnode()
		if not data or len(data) != 3: return # 6/22/03
		try:
			openType,arg,ext=data
			if not g.doHook("openwith1",c=c,v=v,openType=openType,arg=arg,ext=ext):
				#@			<< set ext based on the present language >>
				#@+node:ekr.20031218072017.2824:<< set ext based on the present language >>
				if not ext:
					dict = g.scanDirectives(c)
					language = dict.get("language")
					ext = g.app.language_extension_dict.get(language)
					# print language,ext
					if ext == None:
						ext = "txt"
					
				if ext[0] != ".":
					ext = "."+ext
					
				# print "ext",ext
				#@nonl
				#@-node:ekr.20031218072017.2824:<< set ext based on the present language >>
				#@nl
				#@			<< create or reopen temp file, testing for conflicting changes >>
				#@+node:ekr.20031218072017.2825:<< create or reopen temp file, testing for conflicting changes >>
				dict = None ; path = None
				#@<< set dict and path if a temp file already refers to v.t >>
				#@+node:ekr.20031218072017.2826:<<set dict and path if a temp file already refers to v.t >>
				searchPath = c.openWithTempFilePath(v,ext)
				
				if g.os_path_exists(searchPath):
					for dict in g.app.openWithFiles:
						if v == dict.get("v") and searchPath == dict.get("path"):
							path = searchPath
							break
				#@-node:ekr.20031218072017.2826:<<set dict and path if a temp file already refers to v.t >>
				#@nl
				if path:
					#@	<< create or recreate temp file as needed >>
					#@+node:ekr.20031218072017.2827:<< create or recreate temp file as needed >>
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
					new_body = g.toEncodedString(new_body,encoding,reportErrors=true)
					
					old_time = dict.get("time")
					try:
						new_time = g.os_path_getmtime(path)
					except:
						new_time = None
						
					body_changed = old_body != new_body
					temp_changed = old_time != new_time
					
					if body_changed and temp_changed:
						#@	<< Raise dialog about conflict and set result >>
						#@+node:ekr.20031218072017.2828:<< Raise dialog about conflict and set result >>
						message = (
							"Conflicting changes in outline and temp file\n\n" +
							"Do you want to use the code in the outline or the temp file?\n\n")
						
						result = g.app.gui.runAskYesNoCancelDialog(
							"Conflict!", message,
							yesMessage = "Outline",
							noMessage = "File",
							defaultButton = "Cancel")
						#@nonl
						#@-node:ekr.20031218072017.2828:<< Raise dialog about conflict and set result >>
						#@nl
						if result == "cancel": return
						rewrite = result == "outline"
					else:
						rewrite = body_changed
							
					if rewrite:
						path = c.createOpenWithTempFile(v,ext)
					else:
						g.es("reopening: " + g.shortFileName(path),color="blue")
					#@nonl
					#@-node:ekr.20031218072017.2827:<< create or recreate temp file as needed >>
					#@nl
				else:
					path = c.createOpenWithTempFile(v,ext)
				
				if not path:
					return # An error has occured.
				#@nonl
				#@-node:ekr.20031218072017.2825:<< create or reopen temp file, testing for conflicting changes >>
				#@nl
				#@			<< execute a command to open path in external editor >>
				#@+node:ekr.20031218072017.2829:<< execute a command to open path in external editor >>
				try:
					if arg == None: arg = ""
					shortPath = path # g.shortFileName(path)
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
						filename = g.os_path_basename(arg)
						command = "os.spawnl("+arg+","+filename+','+ shortPath+")"
						apply(os.spawnl,(os.P_NOWAIT,arg,filename,path))
					elif openType == "os.spawnv":
						filename = g.os_path_basename(arg)
						command = "os.spawnv("+arg+",("+filename+','+ shortPath+"))"
						apply(os.spawnl,(os.P_NOWAIT,arg,(filename,path)))
					else:
						command="bad command:"+str(openType)
					# This seems a bit redundant.
					# g.es(command)
				except:
					g.es("exception executing: "+command)
					g.es_exception()
				#@nonl
				#@-node:ekr.20031218072017.2829:<< execute a command to open path in external editor >>
				#@nl
			g.doHook("openwith2",c=c,v=v,openType=openType,arg=arg,ext=ext)
		except:
			g.es("exception in openWith")
			g.es_exception()
	
		return "break"
	#@nonl
	#@+node:ekr.20031218072017.2830:createOpenWithTempFile
	def createOpenWithTempFile (self, v, ext):
		
		c = self
		path = c.openWithTempFilePath(v,ext)
		try:
			if g.os_path_exists(path):
				g.es("recreating:  " + g.shortFileName(path),color="red")
			else:
				g.es("creating:  " + g.shortFileName(path),color="blue")
			file = open(path,"w")
			# 3/7/03: convert s to whatever encoding is in effect.
			s = v.bodyString()
			dict = g.scanDirectives(c,p=v)
			encoding = dict.get("encoding",None)
			if encoding == None:
				encoding = g.app.config.default_derived_file_encoding
			s = g.toEncodedString(s,encoding,reportErrors=true) 
			file.write(s)
			file.flush()
			file.close()
			try:    time = g.os_path_getmtime(path)
			except: time = None
			# g.es("time: " + str(time))
			# 4/22/03: add body and encoding entries to dict for later comparisons.
			dict = {"body":s, "c":c, "encoding":encoding, "f":file, "path":path, "time":time, "v":v}
			#@		<< remove previous entry from app.openWithFiles if it exists >>
			#@+node:ekr.20031218072017.2831:<< remove previous entry from app.openWithFiles if it exists >>
			for d in g.app.openWithFiles[:]: # 6/30/03
				v2 = d.get("v")
				if v.t == v2.t:
					print "removing previous entry in g.app.openWithFiles for",v
					g.app.openWithFiles.remove(d)
			#@nonl
			#@-node:ekr.20031218072017.2831:<< remove previous entry from app.openWithFiles if it exists >>
			#@afterref
 # 4/22/03
			g.app.openWithFiles.append(dict)
			return path
		except:
			file = None
			g.es("exception creating temp file",color="red")
			g.es_exception()
			return None
	#@nonl
	#@-node:ekr.20031218072017.2830:createOpenWithTempFile
	#@+node:ekr.20031218072017.2832:openWithTempFilePath
	def openWithTempFilePath (self,v,ext):
		
		"""Return the path to the temp file corresponding to v and ext."""
	
		name = "LeoTemp_" + str(id(v.t)) + '_' + g.sanitize_filename(v.headString()) + ext
		name = g.toUnicode(name,g.app.tkEncoding) # 10/20/03
	
		td = g.os_path_abspath(tempfile.gettempdir())
		path = g.os_path_join(td,name)
		
		# print "openWithTempFilePath",path
		return path
	#@nonl
	#@-node:ekr.20031218072017.2832:openWithTempFilePath
	#@-node:ekr.20031218072017.2823:openWith and allies
	#@+node:ekr.20031218072017.2833:close
	def close(self):
		
		"""Handle the File-Close command."""
	
		g.app.closeLeoWindow(self.frame)
	#@nonl
	#@-node:ekr.20031218072017.2833:close
	#@+node:ekr.20031218072017.2834:save
	def save(self):
	
		c = self
		
		if g.app.disableSave:
			g.es("Save commands disabled",color="purple")
			return
		
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			c.frame.title = ""
			c.mFileName = ""
	
		if c.mFileName != "":
			# Calls c.setChanged(false) if no error.
			c.fileCommands.save(c.mFileName) 
			return
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile = c.mFileName,
			title="Save",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if fileName:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			c.mFileName = g.ensure_extension(fileName, ".leo")
			c.frame.title = c.mFileName
			c.frame.setTitle(g.computeWindowTitle(c.mFileName))
			c.fileCommands.save(c.mFileName)
			c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:ekr.20031218072017.2834:save
	#@+node:ekr.20031218072017.2835:saveAs
	def saveAs(self):
		
		c = self
		
		if g.app.disableSave:
			g.es("Save commands disabled",color="purple")
			return
	
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			c.frame.title = ""
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile = c.mFileName,
			title="Save As",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if fileName:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			c.mFileName = g.ensure_extension(fileName, ".leo")
			c.frame.title = c.mFileName
			c.frame.setTitle(g.computeWindowTitle(c.mFileName))
			# Calls c.setChanged(false) if no error.
			c.fileCommands.saveAs(c.mFileName)
			c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:ekr.20031218072017.2835:saveAs
	#@+node:ekr.20031218072017.2836:saveTo
	def saveTo(self):
		
		c = self
		
		if g.app.disableSave:
			g.es("Save commands disabled",color="purple")
			return
	
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			c.frame.title = ""
	
		# set local fileName, _not_ c.mFileName
		fileName = g.app.gui.runSaveFileDialog(
			initialfile = c.mFileName,
			title="Save To",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if fileName:
			fileName = g.ensure_extension(fileName, ".leo")
			c.fileCommands.saveTo(fileName)
			c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:ekr.20031218072017.2836:saveTo
	#@+node:ekr.20031218072017.2837:revert
	def revert(self):
		
		c = self
	
		# Make sure the user wants to Revert.
		if not c.mFileName:
			return
			
		reply = g.app.gui.runAskYesNoDialog("Revert",
			"Revert to previous version of " + c.mFileName + "?")
	
		if reply=="no":
			return
	
		# Kludge: rename this frame so openWithFileName won't think it is open.
		fileName = c.mFileName ; c.mFileName = ""
	
		# Create a new frame before deleting this frame.
		ok, frame = g.openWithFileName(fileName,c)
		if ok:
			frame.deiconify()
			g.app.destroyWindow(c.frame)
		else:
			c.mFileName = fileName
	#@-node:ekr.20031218072017.2837:revert
	#@-node:ekr.20031218072017.2820:top level
	#@+node:ekr.20031218072017.2079:Recent Files submenu & allies
	#@+node:ekr.20031218072017.2080:clearRecentFiles
	def clearRecentFiles (self):
		
		"""Clear the recent files list, then add the present file."""
	
		c = self ; f = c.frame
		
		recentFilesMenu = f.menu.getMenu("Recent Files...")
		f.menu.delete_range(recentFilesMenu,0,len(c.recentFiles))
		
		c.recentFiles = []
		f.menu.createRecentFilesMenuItems()
		c.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:ekr.20031218072017.2080:clearRecentFiles
	#@+node:ekr.20031218072017.2081:openRecentFile
	def openRecentFile(self,name=None):
		
		if not name: return
	
		c = self ; v = c.currentVnode()
		#@	<< Set closeFlag if the only open window is empty >>
		#@+node:ekr.20031218072017.2082:<< Set closeFlag if the only open window is empty >>
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
			g.app.numberOfWindows == 1) # Only one untitled window has ever been opened
		#@nonl
		#@-node:ekr.20031218072017.2082:<< Set closeFlag if the only open window is empty >>
		#@nl
		
		fileName = name
		if not g.doHook("recentfiles1",c=c,v=v,fileName=fileName,closeFlag=closeFlag):
			ok, frame = g.openWithFileName(fileName,c)
			if ok and closeFlag:
				g.app.destroyWindow(c.frame) # 12/12/03
				g.app.setLog(frame.log,"openRecentFile") # Sets the log stream for g.es()
				c = frame.c # 6/10/04: Switch to the new commander so the "recentfiles2" hook doesn't crash.
	
		g.doHook("recentfiles2",c=c,v=v,fileName=fileName,closeFlag=closeFlag)
	#@-node:ekr.20031218072017.2081:openRecentFile
	#@+node:ekr.20031218072017.2083:updateRecentFiles
	def updateRecentFiles (self,fileName):
		
		"""Create the RecentFiles menu.  May be called with Null fileName."""
		
		# g.trace(fileName)
		
		# Update the recent files list in all windows.
		if fileName:
			normFileName = g.os_path_norm(fileName)
			for frame in g.app.windowList:
				c = frame.c
				# Remove all versions of the file name.
				for name in c.recentFiles:
					if normFileName == g.os_path_norm(name):
						c.recentFiles.remove(name)
				c.recentFiles.insert(0,fileName)
				# Recreate the Recent Files menu.
				frame.menu.createRecentFilesMenuItems()
		else: # 12/01/03
			for frame in g.app.windowList:
				frame.menu.createRecentFilesMenuItems()
			
		# Update the config file.
		g.app.config.setRecentFiles(self.recentFiles) # Use self, _not_ c.
		g.app.config.update()
	#@nonl
	#@-node:ekr.20031218072017.2083:updateRecentFiles
	#@-node:ekr.20031218072017.2079:Recent Files submenu & allies
	#@+node:ekr.20031218072017.2838:Read/Write submenu
	#@+node:ekr.20031218072017.2839:readOutlineOnly
	def readOutlineOnly (self):
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Read Outline Only",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if not fileName:
			return
	
		try:
			file = open(fileName,'r')
			c,frame = g.app.gui.newLeoCommanderAndFrame(fileName)
			frame.deiconify()
			frame.lift()
			g.app.root.update() # Force a screen redraw immediately.
			c.fileCommands.readOutlineOnly(file,fileName) # closes file.
		except:
			g.es("can not open:" + fileName)
	#@nonl
	#@-node:ekr.20031218072017.2839:readOutlineOnly
	#@+node:ekr.20031218072017.1839:readAtFileNodes
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
	#@-node:ekr.20031218072017.1839:readAtFileNodes
	#@+node:ekr.20031218072017.2840:4.0 Commands
	#@+node:ekr.20031218072017.1809:importDerivedFile
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
		
		fileName = g.app.gui.runOpenFileDialog(
			title="Import Derived File",
			filetypes=types,
			defaultextension=".leo")
	
		if fileName:
			c.importCommands.importDerivedFiles(v,fileName)
	#@nonl
	#@-node:ekr.20031218072017.1809:importDerivedFile
	#@+node:ekr.20031218072017.2014:writeNew/OldDerivedFiles
	def writeNewDerivedFiles (self):
		
		c = self
		autoSave = c.atFileCommands.writeNewDerivedFiles()
		if autoSave:
			g.es("auto-saving outline",color="blue")
			c.save() # Must be done to preserve tnodeList.
		
	def writeOldDerivedFiles (self):
		
		c = self
		c.atFileCommands.writeOldDerivedFiles()
		g.es("auto-saving outline",color="blue")
		c.save() # Must be done to clear tnodeList.
	#@nonl
	#@-node:ekr.20031218072017.2014:writeNew/OldDerivedFiles
	#@-node:ekr.20031218072017.2840:4.0 Commands
	#@-node:ekr.20031218072017.2838:Read/Write submenu
	#@+node:ekr.20031218072017.2841:Tangle submenu
	#@+node:ekr.20031218072017.2842:tangleAll
	def tangleAll(self):
		
		c = self
		c.tangleCommands.tangleAll()
	#@-node:ekr.20031218072017.2842:tangleAll
	#@+node:ekr.20031218072017.2843:tangleMarked
	def tangleMarked(self):
	
		c = self
		c.tangleCommands.tangleMarked()
	#@-node:ekr.20031218072017.2843:tangleMarked
	#@+node:ekr.20031218072017.2844:tangle
	def tangle (self):
	
		c = self
		c.tangleCommands.tangle()
	#@nonl
	#@-node:ekr.20031218072017.2844:tangle
	#@-node:ekr.20031218072017.2841:Tangle submenu
	#@+node:ekr.20031218072017.2845:Untangle submenu
	#@+node:ekr.20031218072017.2846:untangleAll
	def untangleAll(self):
	
		c = self
		c.tangleCommands.untangleAll()
		c.undoer.clearUndoState()
	#@-node:ekr.20031218072017.2846:untangleAll
	#@+node:ekr.20031218072017.2847:untangleMarked
	def untangleMarked(self):
	
		c = self
		c.tangleCommands.untangleMarked()
		c.undoer.clearUndoState()
	#@-node:ekr.20031218072017.2847:untangleMarked
	#@+node:ekr.20031218072017.2848:untangle
	def untangle(self):
	
		c = self
		c.tangleCommands.untangle()
		c.undoer.clearUndoState()
	#@-node:ekr.20031218072017.2848:untangle
	#@-node:ekr.20031218072017.2845:Untangle submenu
	#@+node:ekr.20031218072017.2849:Import&Export submenu
	#@+node:ekr.20031218072017.2850:exportHeadlines
	def exportHeadlines (self):
		
		c = self
	
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile="headlines.txt",
			title="Export Headlines",
			filetypes=filetypes,
			defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c.importCommands.exportHeadlines(fileName)
	
	#@-node:ekr.20031218072017.2850:exportHeadlines
	#@+node:ekr.20031218072017.2851:flattenOutline
	def flattenOutline (self):
		
		c = self
	
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile="flat.txt",
			title="Flatten Outline",
			filetypes=filetypes,
			defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c.importCommands.flattenOutline(fileName)
	
	#@-node:ekr.20031218072017.2851:flattenOutline
	#@+node:ekr.20031218072017.2852:importAtRoot
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
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Import To @root",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFilesCommand (paths,"@root")
	
	#@-node:ekr.20031218072017.2852:importAtRoot
	#@+node:ekr.20031218072017.2853:importAtFile
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
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Import To @file",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFilesCommand (paths,"@file")
	#@nonl
	#@-node:ekr.20031218072017.2853:importAtFile
	#@+node:ekr.20031218072017.2854:importCWEBFiles
	def importCWEBFiles (self):
		
		c = self
		
		filetypes = [
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Import CWEB Files",
			filetypes=filetypes,
			defaultextension=".w")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importWebCommand(paths,"cweb")
	#@-node:ekr.20031218072017.2854:importCWEBFiles
	#@+node:ekr.20031218072017.2855:importFlattenedOutline
	def importFlattenedOutline (self):
		
		c = self
		
		types = [("Text files","*.txt"), ("All files","*")]
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Import MORE Text",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFlattenedOutline(paths)
	#@-node:ekr.20031218072017.2855:importFlattenedOutline
	#@+node:ekr.20031218072017.2856:importNowebFiles
	def importNowebFiles (self):
		
		c = self
	
		filetypes = [
			("Noweb files", "*.nw"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Import Noweb Files",
			filetypes=filetypes,
			defaultextension=".nw")
	
		if fileName and len(fileName) > 0:
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importWebCommand(paths,"noweb")
	
	#@-node:ekr.20031218072017.2856:importNowebFiles
	#@+node:ekr.20031218072017.2857:outlineToCWEB
	def outlineToCWEB (self):
		
		c = self
	
		filetypes=[
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile="cweb.w",
			title="Outline To CWEB",
			filetypes=filetypes,
			defaultextension=".w")
	
		if fileName and len(fileName) > 0:
			c.importCommands.outlineToWeb(fileName,"cweb")
	
	#@-node:ekr.20031218072017.2857:outlineToCWEB
	#@+node:ekr.20031218072017.2858:outlineToNoweb
	def outlineToNoweb (self):
		
		c = self
		
		filetypes=[
			("Noweb files", "*.nw"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile=self.outlineToNowebDefaultFileName,
			title="Outline To Noweb",
			filetypes=filetypes,
			defaultextension=".nw")
	
		if fileName and len(fileName) > 0:
			c.importCommands.outlineToWeb(fileName,"noweb")
			c.outlineToNowebDefaultFileName = fileName
	
	#@-node:ekr.20031218072017.2858:outlineToNoweb
	#@+node:ekr.20031218072017.2859:removeSentinels
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
	
		fileName = g.app.gui.runOpenFileDialog(
			title="Remove Sentinels",
			filetypes=types,
			defaultextension=".py")
	
		if fileName and len(fileName) > 0:
			# alas, askopenfilename returns only a single name.
			c.importCommands.removeSentinelsCommand (fileName)
	
	#@-node:ekr.20031218072017.2859:removeSentinels
	#@+node:ekr.20031218072017.2860:weave
	def weave (self):
		
		c = self
	
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = g.app.gui.runSaveFileDialog(
			initialfile="weave.txt",
			title="Weave",
			filetypes=filetypes,
			defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c.importCommands.weave(fileName)
	#@-node:ekr.20031218072017.2860:weave
	#@-node:ekr.20031218072017.2849:Import&Export submenu
	#@-node:ekr.20031218072017.2819:File Menu
	#@+node:ekr.20031218072017.2861:Edit Menu...
	#@+node:ekr.20031218072017.2862:Edit top level
	#@+node:ekr.20031218072017.2863:delete
	def delete(self):
	
		c = self ; v = c.currentVnode()
	
		if c.frame.body.hasTextSelection():
			oldSel = c.frame.body.getTextSelection()
			c.frame.body.deleteTextSelection()
			c.frame.body.onBodyChanged(v,"Delete",oldSel=oldSel)
	#@nonl
	#@-node:ekr.20031218072017.2863:delete
	#@+node:ekr.20031218072017.2140:executeScript
	def executeScript(self,p=None,script=None):
	
		"""This executes body text as a Python script.
		
		We execute the selected text, or the entire body text if no text is selected."""
		
		error = false
		c = self ; s = None
	
		if script:
			s = script
		else:
			#@		<< get script into s >>
			#@+node:ekr.20031218072017.2142:<< get script into s >>
			try:
				try:
					if not p:
						p = c.currentPosition()
				
					old_body = p.bodyString()
			
					if c.frame.body.hasTextSelection():
						# Temporarily replace v's body text with just the selected text.
						s = c.frame.body.getSelectedText()
						p.v.setTnodeText(s) 
					else:
						s = c.frame.body.getAllText()
				
					if s.strip():
						g.app.scriptDict["script1"]=s
						df = c.atFileCommands.new_df
						df.scanAllDirectives(p,scripting=true)
						# Force Python comment delims.
						df.startSentinelComment = "#"
						df.endSentinelComment = None
						# Write the "derived file" into fo.
						fo = g.fileLikeObject()
						df.write(p.copy(),nosentinels=true,scriptFile=fo)
						assert(p)
						s = fo.get()
						g.app.scriptDict["script2"]=s
						error = len(s) == 0
				except:
					s = "unexpected exception"
					print s ; g.es(s)
					g.es_exception()
			finally:
				p.v.setTnodeText(old_body)
			#@nonl
			#@-node:ekr.20031218072017.2142:<< get script into s >>
			#@nl
		#@	<< redirect output if redirect_execute_script_output_to_log_pane >>
		#@+node:ekr.20031218072017.2143:<< redirect output if redirect_execute_script_output_to_log_pane >>
		if g.app.config.redirect_execute_script_output_to_log_pane:
		
			from leoGlobals import redirectStdout,redirectStderr
			g.redirectStdout() # Redirect stdout
			g.redirectStderr() # Redirect stderr
		#@nonl
		#@-node:ekr.20031218072017.2143:<< redirect output if redirect_execute_script_output_to_log_pane >>
		#@nl
		s = s.strip()
		if s:
			s += '\n' # Make sure we end the script properly.
			try:
				exec s in {} # Use {} to get a pristine environment!
				if not script:
					g.es("end of script",color="purple")
			except:
				g.es("exception executing script")
				g.es_exception(full=false,c=c)
				c.frame.tree.redrawAfterException() # 1/26/04
		elif not error:
			g.es("no script selected",color="blue")
			
		# 4/3/04: The force a redraw _after_ all messages have been output.
		c.redraw() 
	#@nonl
	#@-node:ekr.20031218072017.2140:executeScript
	#@+node:ekr.20031218072017.2864:goToLineNumber & allies
	def goToLineNumber (self):
	
		c = self ; p = c.currentPosition()
		#@	<< set root to the nearest ancestor @file node >>
		#@+node:ekr.20031218072017.2865:<< set root to the nearest ancestor @file node >>
		fileName = None
		for p in p.self_and_parents_iter():
			fileName = p.anyAtFileNodeName()
			if fileName: break
		
		# New in 4.2: Search the entire tree for joined nodes.
		if not fileName:
			p1 = c.currentPosition()
			for p in c.all_positions_iter():
				if p.v.t == p1.v.t and p != p1:
					# Found a joined position.
					for p in p.self_and_parents_iter():
						fileName = p.anyAtFileNodeName()
						if fileName: break
				if fileName: break
			
		if fileName:
			# g.trace(fileName,p)
			root = p.copy()
		else:
			g.es("Go to line number: ancestor must be @file node", color="blue")
			return
		#@nonl
		#@-node:ekr.20031218072017.2865:<< set root to the nearest ancestor @file node >>
		#@nl
		#@	<< read the file into lines >>
		#@+node:ekr.20031218072017.2866:<< read the file into lines >>
		# 1/26/03: calculate the full path.
		d = g.scanDirectives(c)
		path = d.get("path")
		
		fileName = g.os_path_join(path,fileName)
		
		try:
			file=open(fileName)
			lines = file.readlines()
			file.close()
		except:
			g.es("not found: " + fileName)
			return
			
		#@-node:ekr.20031218072017.2866:<< read the file into lines >>
		#@nl
		#@	<< get n, the line number, from a dialog >>
		#@+node:ekr.20031218072017.2867:<< get n, the line number, from a dialog >>
		n = g.app.gui.runAskOkCancelNumberDialog("Enter Line Number","Line number:")
		if n == -1:
			return
		#@nonl
		#@-node:ekr.20031218072017.2867:<< get n, the line number, from a dialog >>
		#@nl
		if n==1:
			p = root ; n2 = 1 ; found = true
		elif n >= len(lines):
			p = root ; found = false
			n2 = p.bodyString().count('\n')
		elif root.isAtAsisFileNode():
			#@		<< count outline lines, setting p,n2,found >>
			#@+node:ekr.20031218072017.2868:<< count outline lines, setting p,n2,found >> (@file-nosent only)
			p = lastv = root
			prev = 0 ; found = false
			for p in p.self_and_subtree_iter():
				lastv = p.copy()
				s = p.bodyString()
				lines = s.count('\n')
				if len(s) > 0 and s[-1] != '\n':
					lines += 1
				# print lines,prev,p
				if prev + lines >= n:
					found = true ; break
				prev += lines
			
			p = lastv
			n2 = max(1,n-prev)
			#@nonl
			#@-node:ekr.20031218072017.2868:<< count outline lines, setting p,n2,found >> (@file-nosent only)
			#@nl
		else:
			vnodeName,childIndex,gnx,n2,delim = self.convertLineToVnodeNameIndexLine(lines,n,root)
			found = true
			if not vnodeName:
				g.es("invalid derived file: " + fileName)
				return
			#@		<< set p to the node given by vnodeName and gnx or childIndex or n >>
			#@+node:ekr.20031218072017.2869:<< set p to the node given by vnodeName and gnx or childIndex or n >>
			if gnx:
				#@	<< 4.2: get node from gnx >>
				#@+node:EKR.20040609110138:<< 4.2: get node from gnx >>
				found = false
				gnx = g.app.nodeIndices.scanGnx(gnx,0)
				
				# g.trace(vnodeName)
				# g.trace(gnx)
				
				for p in root.self_and_subtree_iter():
					if p.matchHeadline(vnodeName):
						# g.trace(p.v.t.fileIndex)
						if p.v.t.fileIndex == gnx:
							found = true ; break
				
				if not found:
					g.es("not found: " + vnodeName, color="red")
					return
				#@nonl
				#@-node:EKR.20040609110138:<< 4.2: get node from gnx >>
				#@nl
			elif childIndex == -1:
				#@	<< 4.x: scan for the node using tnodeList and n >>
				#@+node:ekr.20031218072017.2870:<< 4.x: scan for the node using tnodeList and n >>
				# This is about the best that can be done without replicating the entire atFile write logic.
				
				ok = true
				
				if not hasattr(root.v.t,"tnodeList"):
					s = "no child index for " + root.headString()
					print s ; g.es(s, color="red")
					ok = false
				
				if ok:
					tnodeList = root.v.t.tnodeList
					#@	<< set tnodeIndex to the number of +node sentinels before line n >>
					#@+node:ekr.20031218072017.2871:<< set tnodeIndex to the number of +node sentinels before line n >>
					tnodeIndex = -1 # Don't count the @file node.
					scanned = 0 # count of lines scanned.
					
					for s in lines:
						if scanned >= n:
							break
						i = g.skip_ws(s,0)
						if g.match(s,i,delim):
							i += len(delim)
							if g.match(s,i,"+node"):
								# g.trace(tnodeIndex,s.rstrip())
								tnodeIndex += 1
						scanned += 1
					#@nonl
					#@-node:ekr.20031218072017.2871:<< set tnodeIndex to the number of +node sentinels before line n >>
					#@nl
					tnodeIndex = max(0,tnodeIndex)
					#@	<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
					#@+node:ekr.20031218072017.2872:<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
					#@+at 
					#@nonl
					# We use the tnodeList to find a _tnode_ corresponding to 
					# the proper node, so the user will for sure be editing 
					# the proper text, even if several nodes happen to have 
					# the same headline.  This is really all that we need.
					# 
					# However, this code has no good way of distinguishing 
					# between different cloned vnodes in the file: they all 
					# have the same tnode.  So this code just picks p = 
					# t.vnodeList[0] and leaves it at that.
					# 
					# The only way to do better is to scan the outline, 
					# replicating the write logic to determine which vnode 
					# created the given line.  That's way too difficult, and 
					# it would create an unwanted dependency in this code.
					#@-at
					#@@c
					
					# g.trace("tnodeIndex",tnodeIndex)
					if tnodeIndex < len(tnodeList):
						t = tnodeList[tnodeIndex]
						# Find the first vnode whose tnode is t.
						found = false
						for p in root.self_and_subtree_iter():
							if p.v.t == t:
								found = true ; break
						if not found:
							s = "tnode not found for " + vnodeName
							print s ; g.es(s, color="red") ; ok = false
						elif p.headString().strip() != vnodeName:
							if 0: # Apparently this error doesn't prevent a later scan for working properly.
								s = "Mismatched vnodeName\nExpecting: %s\n got: %s" % (p.headString(),vnodeName)
								print s ; g.es(s, color="red")
							ok = false
					else:
						s = "Invalid computed tnodeIndex: %d" % tnodeIndex
						print s ; g.es(s, color = "red") ; ok = false
					#@nonl
					#@-node:ekr.20031218072017.2872:<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
					#@nl
							
				if not ok:
					# Fall back to the old logic.
					#@	<< set p to the first node whose headline matches vnodeName >>
					#@+node:ekr.20031218072017.2873:<< set p to the first node whose headline matches vnodeName >>
					found = false
					for p in root.self_and_subtree_iter():
						if p.matchHeadline(vnodeName):
							found = true ; break
					
					if not found:
						s = "not found: " + vnodeName
						print s ; g.es(s, color="red")
						return
					#@nonl
					#@-node:ekr.20031218072017.2873:<< set p to the first node whose headline matches vnodeName >>
					#@nl
				#@nonl
				#@-node:ekr.20031218072017.2870:<< 4.x: scan for the node using tnodeList and n >>
				#@nl
			else:
				#@	<< 3.x: scan for the node with the given childIndex >>
				#@+node:ekr.20031218072017.2874:<< 3.x: scan for the node with the given childIndex >>
				found = false
				for p in root.self_and_subtree_iter():
					if p.matchHeadline(vnodeName):
						if childIndex <= 0 or p.childIndex() + 1 == childIndex:
							found = true ; break
				
				if not found:
					g.es("not found: " + vnodeName, color="red")
					return
				#@nonl
				#@-node:ekr.20031218072017.2874:<< 3.x: scan for the node with the given childIndex >>
				#@nl
			#@nonl
			#@-node:ekr.20031218072017.2869:<< set p to the node given by vnodeName and gnx or childIndex or n >>
			#@nl
		#@	<< select p and make it visible >>
		#@+node:ekr.20031218072017.2875:<< select p and make it visible >>
		c.beginUpdate()
		c.frame.tree.expandAllAncestors(p)
		c.selectVnode(p)
		c.endUpdate()
		#@nonl
		#@-node:ekr.20031218072017.2875:<< select p and make it visible >>
		#@nl
		#@	<< put the cursor on line n2 of the body text >>
		#@+node:ekr.20031218072017.2876:<< put the cursor on line n2 of the body text >>
		if found:
			c.frame.body.setInsertPointToStartOfLine(n2-1)
		else:
			c.frame.body.setInsertionPointToEnd()
			g.es("%d lines" % len(lines), color="blue")
		
		c.frame.body.makeInsertPointVisible()
		#@nonl
		#@-node:ekr.20031218072017.2876:<< put the cursor on line n2 of the body text >>
		#@nl
	#@nonl
	#@+node:ekr.20031218072017.2877:convertLineToVnodeNameIndexLine
	#@+at 
	#@nonl
	# We count "real" lines in the derived files, ignoring all sentinels that 
	# do not arise from source lines.  When the indicated line is found, we 
	# scan backwards for an @+body line, get the vnode's name from that line 
	# and set p to the indicated vnode.  This will fail if vnode names have 
	# been changed, and that can't be helped.
	# 
	# Returns (vnodeName,offset)
	# 
	# vnodeName: the name found in the previous @+body sentinel.
	# offset: the offset within p of the desired line.
	#@-at
	#@@c
	
	def convertLineToVnodeNameIndexLine (self,lines,n,root):
		
		"""Convert a line number n to a vnode name, (child index or gnx) and line number."""
		
		c = self ; at = c.atFileCommands
		childIndex = 0 ; gnx = None ; newDerivedFile = false
		thinFile = root.isAtThinFileNode()
		#@	<< set delim, leoLine from the @+leo line >>
		#@+node:ekr.20031218072017.2878:<< set delim, leoLine from the @+leo line >>
		# Find the @+leo line.
		tag = "@+leo"
		i = 0 
		while i < len(lines) and lines[i].find(tag)==-1:
			i += 1
		leoLine = i # Index of the line containing the leo sentinel
		
		if leoLine < len(lines):
			s = lines[leoLine]
			valid,newDerivedFile,start,end = at.parseLeoSentinel(s)
			if valid: delim = start + '@'
			else:     delim = None
		else:
			delim = None
		#@-node:ekr.20031218072017.2878:<< set delim, leoLine from the @+leo line >>
		#@nl
		if not delim:
			g.es("bad @+leo sentinel")
			return None,None,None,None,None
		#@	<< scan back to @+node, setting offset,nodeSentinelLine >>
		#@+node:ekr.20031218072017.2879:<< scan back to  @+node, setting offset,nodeSentinelLine >>
		offset = 0 # This is essentially the Tk line number.
		nodeSentinelLine = -1
		line = n - 1
		while line >= 0:
			s = lines[line]
			# g.trace(s)
			i = g.skip_ws(s,0)
			if g.match(s,i,delim):
				#@		<< handle delim while scanning backward >>
				#@+node:ekr.20031218072017.2880:<< handle delim while scanning backward >>
				if line == n:
					g.es("line "+str(n)+" is a sentinel line")
				i += len(delim)
				
				if g.match(s,i,"-node"):
					# The end of a nested section.
					line = self.skipToMatchingNodeSentinel(lines,line,delim)
				elif g.match(s,i,"+node"):
					nodeSentinelLine = line
					break
				elif g.match(s,i,"<<") or g.match(s,i,"@first"):
					offset += 1 # Count these as a "real" lines.
				#@nonl
				#@-node:ekr.20031218072017.2880:<< handle delim while scanning backward >>
				#@nl
			else:
				offset += 1 # Assume the line is real.  A dubious assumption.
			line -= 1
		#@nonl
		#@-node:ekr.20031218072017.2879:<< scan back to  @+node, setting offset,nodeSentinelLine >>
		#@nl
		if nodeSentinelLine == -1:
			# The line precedes the first @+node sentinel
			# g.trace("before first line")
			return root.headString(),0,1,delim # 10/13/03
		s = lines[nodeSentinelLine]
		# g.trace(s)
		#@	<< set vnodeName and (childIndex or gnx) from s >>
		#@+node:ekr.20031218072017.2881:<< set vnodeName and (childIndex or gnx) from s >>
		if newDerivedFile:
			i = 0
			if thinFile:
				# gnx is lies between the first and second ':':
				i = s.find(':',i)
				if i > 0:
					i += 1
					j = s.find(':',i)
					if j > 0:
						gnx = s[i:j]
					else: i = len(s)
				else: i = len(s)
			# vnode name is everything following the first or second':'
			# childIndex is -1 as a flag for later code.
			i = s.find(':',i)
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
						junk,childIndex = g.skip_long(s,i+1)
				i += 1
			vnodeName = s[i:].strip()
			
		# g.trace("gnx",gnx,"vnodeName:",vnodeName)
		if not vnodeName:
			vnodeName = None
			g.es("bad @+node sentinel")
		#@nonl
		#@-node:ekr.20031218072017.2881:<< set vnodeName and (childIndex or gnx) from s >>
		#@nl
		# g.trace("childIndex,offset",childIndex,offset,vnodeName)
		return vnodeName,childIndex,gnx,offset,delim
	#@-node:ekr.20031218072017.2877:convertLineToVnodeNameIndexLine
	#@+node:ekr.20031218072017.2882:skipToMatchingNodeSentinel
	def skipToMatchingNodeSentinel (self,lines,n,delim):
		
		s = lines[n]
		i = g.skip_ws(s,0)
		assert(g.match(s,i,delim))
		i += len(delim)
		if g.match(s,i,"+node"):
			start="+node" ; end="-node" ; delta=1
		else:
			assert(g.match(s,i,"-node"))
			start="-node" ; end="+node" ; delta=-1
		# Scan to matching @+-node delim.
		n += delta ; level = 0
		while 0 <= n < len(lines):
			s = lines[n] ; i = g.skip_ws(s,0)
			if g.match(s,i,delim):
				i += len(delim)
				if g.match(s,i,start):
					level += 1
				elif g.match(s,i,end):
					if level == 0: break
					else: level -= 1
			n += delta
			
		# g.trace(n)
		return n
	#@nonl
	#@-node:ekr.20031218072017.2882:skipToMatchingNodeSentinel
	#@-node:ekr.20031218072017.2864:goToLineNumber & allies
	#@+node:ekr.20031218072017.2088:fontPanel
	def fontPanel(self):
		
		c = self ; frame = c.frame
	
		if not frame.fontPanel:
			frame.fontPanel = g.app.gui.createFontPanel(c)
			
		frame.fontPanel.bringToFront()
	#@nonl
	#@-node:ekr.20031218072017.2088:fontPanel
	#@+node:ekr.20031218072017.2090:colorPanel
	def colorPanel(self):
		
		c = self ; frame = c.frame
	
		if not frame.colorPanel:
			frame.colorPanel = g.app.gui.createColorPanel(c)
			
		frame.colorPanel.bringToFront()
	#@nonl
	#@-node:ekr.20031218072017.2090:colorPanel
	#@+node:ekr.20031218072017.2883:viewAllCharacters
	def viewAllCharacters (self, event=None):
	
		c = self ; frame = c.frame
		p = c.currentPosition()
		colorizer = frame.body.getColorizer()
	
		colorizer.showInvisibles = g.choose(colorizer.showInvisibles,0,1)
	
		# It is much easier to change the menu name here than in the menu updater.
		menu = frame.menu.getMenu("Edit")
		if colorizer.showInvisibles:
			frame.menu.setMenuLabel(menu,"Show Invisibles","Hide Invisibles")
		else:
			frame.menu.setMenuLabel(menu,"Hide Invisibles","Show Invisibles")
	
		c.frame.body.recolor_now(p)
	#@nonl
	#@-node:ekr.20031218072017.2883:viewAllCharacters
	#@+node:ekr.20031218072017.2086:preferences
	def preferences(self):
		
		"""Show the Preferences Panel, creating it if necessary."""
		
		c = self ; frame = c.frame
	
		if not frame.prefsPanel:
			frame.prefsPanel = g.app.gui.createPrefsPanel(c)
			
		frame.prefsPanel.bringToFront()
	#@nonl
	#@-node:ekr.20031218072017.2086:preferences
	#@-node:ekr.20031218072017.2862:Edit top level
	#@+node:ekr.20031218072017.2884:Edit Body submenu
	#@+node:ekr.20031218072017.1704:convertAllBlanks
	def convertAllBlanks (self):
		
		c = self ; body = c.frame.body ; v = current = c.currentVnode()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Convert All Blanks")
			return
		next = v.nodeAfterTree()
		dict = g.scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		count = 0
		while v and v != next:
			if v == current:
				if c.convertBlanks(setUndoParams=false):
					count += 1 ; v.setDirty()
			else:
				changed = false ; result = []
				text = v.t.bodyString
				assert(g.isUnicode(text))
				lines = string.split(text, '\n')
				for line in lines:
					s = g.optimizeLeadingWhitespace(line,tabWidth)
					if s != line: changed = true
					result.append(s)
				if changed:
					count += 1 ; v.setDirty()
					result = string.join(result,'\n')
					v.setTnodeText(result)
			v = v.threadNext()
		if count > 0:
			newText = body.getAllText()
			newSel = body.getTextSelection()
			c.undoer.setUndoParams("Convert All Blanks",
				current,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		g.es("blanks converted to tabs in %d nodes" % count)
	#@nonl
	#@-node:ekr.20031218072017.1704:convertAllBlanks
	#@+node:ekr.20031218072017.1705:convertAllTabs
	def convertAllTabs (self):
	
		c = self ; body = c.frame.body ; v = current = c.currentVnode()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Convert All Tabs")
			return
		next = v.nodeAfterTree()
		dict = g.scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		count = 0
		while v and v != next:
			if v == current:
				if self.convertTabs(setUndoParams=false):
					count += 1 ; v.setDirty()
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				assert(g.isUnicode(text))
				lines = string.split(text, '\n')
				for line in lines:
					i,w = g.skip_leading_ws_with_indent(line,0,tabWidth)
					s = g.computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
					if s != line: changed = true
					result.append(s)
				if changed:
					count += 1 ; v.setDirty()
					result = string.join(result,'\n')
					v.setTnodeText(result)
			v = v.threadNext()
		if count > 0:
			newText = body.getAllText()
			newSel = body.getTextSelection() # 7/11/03
			c.undoer.setUndoParams("Convert All Tabs",
				current,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		g.es("tabs converted to blanks in %d nodes" % count)
	#@nonl
	#@-node:ekr.20031218072017.1705:convertAllTabs
	#@+node:ekr.20031218072017.1821:convertBlanks
	def convertBlanks (self,setUndoParams=true):
	
		c = self ; body = c.frame.body
		
		if g.app.batchMode:
			c.notValidInBatchMode("Convert Blanks")
			return false
	
		head,lines,tail,oldSel,oldYview = c.getBodyLines(expandSelection=true)
		result = [] ; changed = false
	
		# Use the relative @tabwidth, not the global one.
		dict = g.scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		if not tabWidth: return false
	
		for line in lines:
			s = g.optimizeLeadingWhitespace(line,tabWidth)
			if s != line: changed = true
			result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			undoType = g.choose(setUndoParams,"Convert Blanks",None)
			c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
	
		return changed
	#@nonl
	#@-node:ekr.20031218072017.1821:convertBlanks
	#@+node:ekr.20031218072017.1822:convertTabs
	def convertTabs (self,setUndoParams=true):
	
		c = self ; body = c.frame.body
		
		if g.app.batchMode:
			c.notValidInBatchMode("Convert Tabs")
			return false
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines(expandSelection=true)
		result = [] ; changed = false
		
		# Use the relative @tabwidth, not the global one.
		dict = g.scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		if not tabWidth: return false
	
		for line in lines:
			i,w = g.skip_leading_ws_with_indent(line,0,tabWidth)
			s = g.computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
			if s != line: changed = true
			result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			undoType = g.choose(setUndoParams,"Convert Tabs",None)
			c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
			
		return changed
	#@-node:ekr.20031218072017.1822:convertTabs
	#@+node:ekr.20031218072017.1823:createLastChildNode
	def createLastChildNode (self,parent,headline,body):
		
		c = self
		if body and len(body) > 0:
			body = string.rstrip(body)
		if not body or len(body) == 0:
			body = ""
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		v.setTnodeText(body)
		v.setDirty()
		c.validateOutline()
	#@nonl
	#@-node:ekr.20031218072017.1823:createLastChildNode
	#@+node:ekr.20031218072017.1824:dedentBody
	def dedentBody (self):
		
		c = self ; p = c.currentPosition()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Unindent")
			return
	
		d = g.scanDirectives(c,p) # Support @tab_width directive properly.
		tab_width = d.get("tabwidth",c.tab_width) # ; g.trace(tab_width)
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = g.skip_leading_ws_with_indent(line,0,tab_width)
			s = g.computeLeadingWhitespace(width-abs(tab_width),tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Undent",oldSel,oldYview)
	#@nonl
	#@-node:ekr.20031218072017.1824:dedentBody
	#@+node:ekr.20031218072017.1706:extract
	def extract(self):
		
		c = self ; body = c.frame.body ; current = v = c.currentVnode()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Extract")
			return
		
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = g.skip_leading_ws_with_indent(headline,0,c.tab_width)
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		#@	<< Set headline for extract >>
		#@+node:ekr.20031218072017.1707:<< Set headline for extract >>
		headline = string.strip(headline)
		while len(headline) > 0 and headline[0] == '/':
			headline = headline[1:]
		headline = string.strip(headline)
		#@nonl
		#@-node:ekr.20031218072017.1707:<< Set headline for extract >>
		#@nl
		# Remove leading whitespace from all body lines.
		result = []
		for line in lines:
			# Remove the whitespace on the first line
			line = g.removeLeadingWhitespace(line,ws,c.tab_width)
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
	#@-node:ekr.20031218072017.1706:extract
	#@+node:ekr.20031218072017.1708:extractSection
	def extractSection(self):
	
		c = self ; body = c.frame.body ; current = v = c.currentVnode()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Extract Section")
			return
	
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = g.skip_leading_ws_with_indent(headline,0,c.tab_width)
		line1 = "\n" + headline
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = body.getAllText()
		oldSel = body.getTextSelection()
		#@	<< Set headline for extractSection >>
		#@+node:ekr.20031218072017.1709:<< Set headline for extractSection >>
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
			g.es("Selected text should start with a section name",color="blue")
			return
		#@nonl
		#@-node:ekr.20031218072017.1709:<< Set headline for extractSection >>
		#@nl
		# Remove leading whitespace from all body lines.
		result = []
		for line in lines:
			# Remove the whitespace on the first line
			line = g.removeLeadingWhitespace(line,ws,c.tab_width)
			result.append(line)
		# Create a new node from lines.
		newBody = string.join(result,'\n')
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		if 1: # update range...
			c.createLastChildNode(v,headline,newBody)
			# g.trace(v)
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
	#@-node:ekr.20031218072017.1708:extractSection
	#@+node:ekr.20031218072017.1710:extractSectionNames
	def extractSectionNames(self):
	
		c = self ; body = c.frame.body ; current = v = c.currentVnode()
		
		if g.app.batchMode:
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
				#@+node:ekr.20031218072017.1711:<< Find the next section name >>
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
				#@-node:ekr.20031218072017.1711:<< Find the next section name >>
				#@nl
				if name:
					self.createLastChildNode(v,name,None)
					found = true
			c.selectVnode(v)
			c.validateOutline()
			if not found:
				g.es("Selected text should contain one or more section names",color="blue")
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
	#@-node:ekr.20031218072017.1710:extractSectionNames
	#@+node:ekr.20031218072017.1825:findBoundParagraph
	def findBoundParagraph (self):
		
		c = self
		head,ins,tail = c.frame.body.getInsertLines()
	
		if not ins or ins.isspace() or ins[0] == '@':
			return None,None,None,None # DTHEIN 18-JAN-2004
			
		head_lines = g.splitLines(head)
		tail_lines = g.splitLines(tail)
	
		if 0:
			#@		<< trace head_lines, ins, tail_lines >>
			#@+node:ekr.20031218072017.1826:<< trace head_lines, ins, tail_lines >>
			if 0:
				print ; print "head_lines"
				for line in head_lines: print line
				print ; print "ins", ins
				print ; print "tail_lines"
				for line in tail_lines: print line
			else:
				g.es("head_lines: ",head_lines)
				g.es("ins: ",ins)
				g.es("tail_lines: ",tail_lines)
			#@nonl
			#@-node:ekr.20031218072017.1826:<< trace head_lines, ins, tail_lines >>
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
		trailingNL = false # DTHEIN 18-JAN-2004: properly capture terminating NL
		while i < len(tail_lines):
			line = tail_lines[i]
			if len(line) == 0 or line.isspace() or line[0] == '@':
				trailingNL = line.endswith(u'\n') or line.startswith(u'@') # DTHEIN 21-JAN-2004
				break
			i += 1
			
	#	para_tail_lines = tail_lines[:i]
		para_tail_lines = tail_lines[:i]
		post_para_lines = tail_lines[i:]
		
		head = g.joinLines(pre_para_lines)
		result = para_head_lines 
		result.extend([ins])
		result.extend(para_tail_lines)
		tail = g.joinLines(post_para_lines)
	
		# DTHEIN 18-JAN-2004: added trailingNL to return value list
		return head,result,tail,trailingNL # string, list, string, bool
	#@nonl
	#@-node:ekr.20031218072017.1825:findBoundParagraph
	#@+node:ekr.20031218072017.1827:findMatchingBracket
	def findMatchingBracket (self):
		
		c = self ; body = c.frame.body
		
		if g.app.batchMode:
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
			g.es("unmatched '%s'",ch)
	#@nonl
	#@+node:ekr.20031218072017.1828:findMatchingBracket
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
				# g.trace("not found")
				return None
			ch2 = body.getCharAtIndex(index)
			if ch2 == ch:
				level += 1 #; g.trace(level,index)
			if ch2 == match_ch:
				level -= 1 #; g.trace(level,index)
				if level <= 0:
					return index
			if not forward and body.compareIndices(index,"<=","1.0"):
				# g.trace("not found")
				return None
			adj = g.choose(forward,1,-1)
			index = body.adjustIndex(index,adj)
		return 0 # unreachable: keeps pychecker happy.
	# Test  (
	# ([(x){y}]))
	# Test  ((x)(unmatched
	#@nonl
	#@-node:ekr.20031218072017.1828:findMatchingBracket
	#@-node:ekr.20031218072017.1827:findMatchingBracket
	#@+node:ekr.20031218072017.1829:getBodyLines
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
	#@-node:ekr.20031218072017.1829:getBodyLines
	#@+node:ekr.20031218072017.1830:indentBody
	def indentBody (self):
	
		c = self ; p = c.currentPosition()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Indent")
			return
	
		d = g.scanDirectives(c,p) # Support @tab_width directive properly.
		tab_width = d.get("tabwidth",c.tab_width) # ; g.trace(tab_width)
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = g.skip_leading_ws_with_indent(line,0,tab_width)
			s = g.computeLeadingWhitespace(width+abs(tab_width),tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Indent",oldSel,oldYview)
	#@nonl
	#@-node:ekr.20031218072017.1830:indentBody
	#@+node:ekr.20031218072017.1831:insertBodyTime & allies
	def insertBodyTime (self):
		
		c = self ; v = c.currentVnode()
		
		if g.app.batchMode:
			c.notValidInBatchMode("xxx")
			return
		
		oldSel = c.frame.body.getTextSelection()
		c.frame.body.deleteTextSelection() # Works if nothing is selected.
		s = self.getTime(body=true)
		c.frame.body.insertAtInsertPoint(s)
		c.frame.body.onBodyChanged(v,"Typing",oldSel=oldSel)
	#@nonl
	#@+node:ekr.20031218072017.1832:getTime
	def getTime (self,body=true):
	
		config = g.app.config
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
			g.es_exception() # Probably a bad format string in leoConfig.txt.
			s = time.strftime(default_format,time.gmtime())
		return s
	#@-node:ekr.20031218072017.1832:getTime
	#@-node:ekr.20031218072017.1831:insertBodyTime & allies
	#@+node:ekr.20031218072017.1833:reformatParagraph
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
		
		if g.app.batchMode:
			c.notValidInBatchMode("xxx")
			return
	
		if body.hasTextSelection():
			g.es("Text selection inhibits Reformat Paragraph",color="blue")
			return
	
		#@	<< compute vars for reformatParagraph >>
		#@+node:ekr.20031218072017.1834:<< compute vars for reformatParagraph >>
		dict = g.scanDirectives(c)
		pageWidth = dict.get("pagewidth")
		tabWidth  = dict.get("tabwidth")
		
		original = body.getAllText()
		oldSel   = body.getTextSelection()
		oldYview = body.getYScrollPosition()
		head,lines,tail,trailingNL = c.findBoundParagraph() # DTHEIN 18-JAN-2004: add trailingNL
		#@nonl
		#@-node:ekr.20031218072017.1834:<< compute vars for reformatParagraph >>
		#@nl
		if lines:
			#@		<< compute the leading whitespace >>
			#@+node:ekr.20031218072017.1835:<< compute the leading whitespace >>
			indents = [0,0] ; leading_ws = ["",""]
			
			for i in (0,1):
				if i < len(lines):
					# Use the original, non-optimized leading whitespace.
					leading_ws[i] = ws = g.get_leading_ws(lines[i])
					indents[i] = g.computeWidth(ws,tabWidth)
					
			indents[1] = max(indents)
			if len(lines) == 1:
				leading_ws[1] = leading_ws[0]
			#@-node:ekr.20031218072017.1835:<< compute the leading whitespace >>
			#@nl
			#@		<< compute the result of wrapping all lines >>
			#@+node:ekr.20031218072017.1836:<< compute the result of wrapping all lines >>
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
			result = g.wrap_lines(lines,
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
			#@-node:ekr.20031218072017.1836:<< compute the result of wrapping all lines >>
			#@nl
			#@		<< update the body, selection & undo state >>
			#@+node:ekr.20031218072017.1837:<< update the body, selection & undo state >>
			sel_start, sel_end = body.setSelectionAreas(head,result,tail)
			
			changed = original != head + result + tail
			undoType = g.choose(changed,"Reformat Paragraph",None)
			body.onBodyChanged(v,undoType,oldSel=oldSel,oldYview=oldYview)
			
			# Advance the selection to the next paragraph.
			newSel = sel_end, sel_end
			body.setTextSelection(newSel)
			body.makeIndexVisible(sel_end)
			
			c.recolor()
			#@nonl
			#@-node:ekr.20031218072017.1837:<< update the body, selection & undo state >>
			#@nl
	#@nonl
	#@-node:ekr.20031218072017.1833:reformatParagraph
	#@+node:ekr.20031218072017.1838:updateBodyPane (handles undo)
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
	#@-node:ekr.20031218072017.1838:updateBodyPane (handles undo)
	#@-node:ekr.20031218072017.2884:Edit Body submenu
	#@+node:ekr.20031218072017.2885:Edit Headline submenu
	#@+node:ekr.20031218072017.2886:editHeadline
	def editHeadline(self):
		
		c = self ; tree = c.frame.tree
		
		if g.app.batchMode:
			c.notValidInBatchMode("Edit Headline")
			return
	
		tree.editLabel(c.currentPosition())
	#@nonl
	#@-node:ekr.20031218072017.2886:editHeadline
	#@+node:ekr.20031218072017.2290:toggleAngleBrackets
	def toggleAngleBrackets (self):
		
		c = self ; v = c.currentVnode()
		
		if g.app.batchMode:
			c.notValidInBatchMode("Toggle Angle Brackets")
			return
	
		s = v.headString().strip()
		if (s[0:2] == "<<"
			or s[-2:] == ">>"): # Must be on separate line.
			if s[0:2] == "<<": s = s[2:]
			if s[-2:] == ">>": s = s[:-2]
			s = s.strip()
		else:
			s = g.angleBrackets(' ' + s + ' ')
		
		c.frame.tree.editLabel(v)
		if v.edit_text():
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("1.0",s)
			c.frame.tree.onHeadChanged(v)
	#@-node:ekr.20031218072017.2290:toggleAngleBrackets
	#@-node:ekr.20031218072017.2885:Edit Headline submenu
	#@+node:ekr.20031218072017.2887:Find submenu (frame methods)
	#@+node:ekr.20031218072017.2888:findPanel
	def findPanel(self):
	
		c = self
	
		find = g.app.findFrame
		find.bringToFront()
		find.c = self
	#@-node:ekr.20031218072017.2888:findPanel
	#@+node:ekr.20031218072017.2889:findNext
	def findNext(self):
	
		c = self
		g.app.findFrame.findNextCommand(c)
	#@-node:ekr.20031218072017.2889:findNext
	#@+node:ekr.20031218072017.2890:findPrevious
	def findPrevious(self):
	
		c = self
		g.app.findFrame.findPreviousCommand(c)
	#@-node:ekr.20031218072017.2890:findPrevious
	#@+node:ekr.20031218072017.2891:replace
	def replace(self):
	
		c = self
		g.app.findFrame.changeCommand(c)
	#@-node:ekr.20031218072017.2891:replace
	#@+node:ekr.20031218072017.2892:replaceThenFind
	def replaceThenFind(self):
	
		c = self
		g.app.findFrame.changeThenFindCommand(c)
	#@-node:ekr.20031218072017.2892:replaceThenFind
	#@-node:ekr.20031218072017.2887:Find submenu (frame methods)
	#@+node:ekr.20031218072017.2893:notValidInBatchMode
	def notValidInBatchMode(self, commandName):
		
		g.es("%s command is not valid in batch mode" % commandName)
	#@-node:ekr.20031218072017.2893:notValidInBatchMode
	#@-node:ekr.20031218072017.2861:Edit Menu...
	#@+node:ekr.20031218072017.2894:Outline menu...
	#@+node:ekr.20031218072017.2895: Top Level...
	#@+node:ekr.20031218072017.1548:Cut & Paste Outlines
	#@+node:ekr.20031218072017.1549:cutOutline
	def cutOutline(self):
	
		c = self
		if c.canDeleteHeadline():
			c.copyOutline()
			c.deleteOutline("Cut Node")
			c.recolor()
	#@nonl
	#@-node:ekr.20031218072017.1549:cutOutline
	#@+node:ekr.20031218072017.1550:copyOutline
	def copyOutline(self):
	
		# Copying an outline has no undo consequences.
		c = self
		c.endEditing()
		c.fileCommands.assignFileIndices()
		s = c.fileCommands.putLeoOutline()
		g.app.gui.replaceClipboardWith(s)
	#@nonl
	#@-node:ekr.20031218072017.1550:copyOutline
	#@+node:ekr.20031218072017.1551:pasteOutline
	# To cut and paste between apps, just copy into an empty body first, then copy to Leo's clipboard.
	
	def pasteOutline(self):
	
		c = self ; current = c.currentPosition()
		
		s = g.app.gui.getTextFromClipboard()
	
		if not s or not c.canPasteOutline(s):
			return # This should never happen.
	
		isLeo = g.match(s,0,g.app.prolog_prefix_string)
	
		if isLeo:
			p = c.fileCommands.getLeoOutline(s)
		else:
			p = c.importCommands.convertMoreStringToOutlineAfter(s,current)
			
		if p:
			c.endEditing()
			c.beginUpdate()
			if 1: # inside update...
				c.validateOutline()
				c.selectVnode(p)
				p.setDirty()
				c.setChanged(true)
				# paste as first child if back is expanded.
				back = p.back()
				if back and back.isExpanded():
					p.moveToNthChildOf(back,0)
				c.undoer.setUndoParams("Paste Node",p)
			c.endUpdate()
			c.recolor()
		else:
			g.es("The clipboard is not a valid " + g.choose(isLeo,"Leo","MORE") + " file")
	#@nonl
	#@-node:ekr.20031218072017.1551:pasteOutline
	#@-node:ekr.20031218072017.1548:Cut & Paste Outlines
	#@+node:ekr.20031218072017.2072:c.checkOutline
	def checkOutline (self,verbose=true,unittest=false):
		
		"""Report any possible clone errors in the outline.
		
		Remove any unused tnodeLists."""
		
		c = self ; count = 1 ; errors = 0 ; full = true
		if full and not unittest:
			g.es("all tests enabled: this may take awhile",color="blue")
	
		p = c.rootPosition()
		#@	<< assert equivalence of lastVisible methods >>
		#@+node:ekr.20040314062338:<< assert equivalence of lastVisible methods >>
		if 0:
			g.app.debug = true
		
			p1 = p.oldLastVisible()
			p2 = p.lastVisible()
			
			if p1 != p2:
				print "oldLastVisible",p1
				print "   lastVisible",p2
			
			assert p1 and p2 and p1 == p2, "oldLastVisible==lastVisible"
			assert p1.isVisible() and p2.isVisible(), "p1.isVisible() and p2.isVisible()"
			
			g.app.debug = false
		#@nonl
		#@-node:ekr.20040314062338:<< assert equivalence of lastVisible methods >>
		#@nl
		for p in c.allNodes_iter():
			try:
				count += 1
				#@			<< remove unused tnodeList >>
				#@+node:ekr.20040313150633:<< remove unused tnodeList >>
				# Empty tnodeLists are not errors.
				v = p.v
				
				# New in 4.2: tnode list is in tnode.
				if hasattr(v.t,"tnodeList") and len(v.t.tnodeList) > 0 and not v.isAnyAtFileNode():
					s = "deleting tnodeList for " + repr(v)
					print s ; g.es(s,color="blue")
					delattr(v.t,"tnodeList")
				#@nonl
				#@-node:ekr.20040313150633:<< remove unused tnodeList >>
				#@nl
				if not unittest: # this would be very slow.
					if full: # For testing only.
						#@					<< do full tests >>
						#@+node:ekr.20040323155951:<< do full tests >>
						if count % 100 == 0:
							g.es('.',newline=false)
						if count % 2000 == 0:
							g.enl()
						
						#@+others
						#@+node:ekr.20040314035615:assert consistency of threadNext & threadBack links
						threadBack = p.threadBack()
						threadNext = p.threadNext()
						
						if threadBack:
							assert p == threadBack.threadNext(), "p==threadBack.threadNext"
						
						if threadNext:
							assert p == threadNext.threadBack(), "p==threadNext.threadBack"
						#@nonl
						#@-node:ekr.20040314035615:assert consistency of threadNext & threadBack links
						#@+node:ekr.20040314035615.1:assert consistency of next and back links
						back = p.back()
						next = p.next()
						
						if back:
							assert p == back.next(), "p==back.next"
								
						if next:
							assert p == next.back(), "p==next.back"
						#@nonl
						#@-node:ekr.20040314035615.1:assert consistency of next and back links
						#@+node:ekr.20040314035615.2:assert consistency of parent and child links
						if p.hasParent():
							n = p.childIndex()
							assert p == p.parent().moveToNthChild(n), "p==parent.moveToNthChild"
							
						for child in p.children_iter():
							assert p == child.parent(), "p==child.parent"
						
						if p.hasNext():
							assert p.next().parent() == p.parent(), "next.parent==parent"
							
						if p.hasBack():
							assert p.back().parent() == p.parent(), "back.parent==parent"
						#@nonl
						#@-node:ekr.20040314035615.2:assert consistency of parent and child links
						#@+node:ekr.20040323155951.1:assert consistency of directParents and parent
						if p.hasParent():
							t = p.parent().v.t
							for v in p.directParents():
								try:
									assert v.t == t
								except:
									print "p",p
									print "p.directParents",p.directParents()
									print "v",v
									print "v.t",v.t
									print "t = p.parent().v.t",t
									raise AssertionError,"v.t == t"
						#@-node:ekr.20040323155951.1:assert consistency of directParents and parent
						#@+node:ekr.20040323161837:assert consistency of p.v.t.vnodeList, & v.parents for cloned nodes
						if p.isCloned():
							parents = p.v.t.vnodeList
							for child in p.children_iter():
								vparents = child.directParents()
								assert len(parents) == len(vparents), "len(parents) == len(vparents)"
								for parent in parents:
									assert parent in vparents, "parent in vparents"
								for parent in vparents:
									assert parent in parents, "parent in parents"
						#@nonl
						#@-node:ekr.20040323161837:assert consistency of p.v.t.vnodeList, & v.parents for cloned nodes
						#@+node:ekr.20040323162707:assert that clones actually share subtrees
						if p.isCloned() and p.hasChildren():
							childv = p.firstChild().v
							assert childv == p.v.t._firstChild, "childv == p.v.t._firstChild"
							assert id(childv) == id(p.v.t._firstChild), "id(childv) == id(p.v.t._firstChild)"
							for v in p.v.t.vnodeList:
								assert v.t._firstChild == childv, "v.t._firstChild == childv"
								assert id(v.t._firstChild) == id(childv), "id(v.t._firstChild) == id(childv)"
						#@nonl
						#@-node:ekr.20040323162707:assert that clones actually share subtrees
						#@+node:ekr.20040314043623:assert consistency of vnodeList
						vnodeList = p.v.t.vnodeList
							
						for v in vnodeList:
							
							try:
								assert v.t == p.v.t
							except AssertionError:
								print "p",p
								print "v",v
								print "p.v",p.v
								print "v.t",v.t
								print "p.v.t",p.v.t
								raise AssertionError, "v.t == p.v.t"
						
							if p.v.isCloned():
								assert v.isCloned(), "v.isCloned"
								assert len(vnodeList) > 1, "len(vnodeList) > 1"
							else:
								assert not v.isCloned(), "not v.isCloned"
								assert len(vnodeList) == 1, "len(vnodeList) == 1"
						#@nonl
						#@-node:ekr.20040314043623:assert consistency of vnodeList
						#@-others
						#@-node:ekr.20040323155951:<< do full tests >>
						#@nl
			except AssertionError,message:
				errors += 1
				#@			<< give test failed message >>
				#@+node:ekr.20040314044652:<< give test failed message >>
				if 1: # errors == 1:
					s = "test failed: %s %s" % (message,repr(p))
					print s ; print
					g.es(s,color="red")
				#@nonl
				#@-node:ekr.20040314044652:<< give test failed message >>
				#@nl
		if not unittest:
			#@		<< print summary message >>
			#@+node:ekr.20040314043900:<<print summary message >>
			if full:
				print
				g.enl()
			
			s = "%d nodes checked, %d errors" % (count,errors)
			if errors or verbose:
				print s ; g.es(s,color="red")
			elif verbose:
				g.es(s,color="green")
			#@nonl
			#@-node:ekr.20040314043900:<<print summary message >>
			#@nl
		return errors
	#@nonl
	#@-node:ekr.20031218072017.2072:c.checkOutline
	#@+node:ekr.20040412060927:c.dumpOutline
	def dumpOutline (self):
		
		""" Dump all nodes in the outline."""
		
		c = self
	
		for p in c.allNodes_iter():
			p.dump()
	#@nonl
	#@-node:ekr.20040412060927:c.dumpOutline
	#@+node:ekr.20031218072017.2028:Hoist & dehoist & enablers
	def dehoist(self):
	
		c = self ; p = c.currentPosition()
		g.trace(p)
		if p and c.canDehoist():
			c.undoer.setUndoParams("De-Hoist",p)
			h,expanded = c.hoistStack.pop()
			if expanded: p.expand()
			else:        p.contract()
			c.redraw()
			c.frame.clearStatusLine()
			if c.hoistStack:
				p,junk = c.hoistStack[-1]
				c.frame.putStatusLine("Hoist: " + p.headString())
			else:
				c.frame.putStatusLine("No hoist")
	
	def hoist(self):
	
		c = self ; p = c.currentPosition()
		if p and c.canHoist():
			c.undoer.setUndoParams("Hoist",p)
			# New in 4.2: remember expansion state.
			c.hoistStack.append((p,p.isExpanded()),)
			p.expand()
			c.redraw()
			c.frame.clearStatusLine()
			c.frame.putStatusLine("Hoist: " + p.headString())
	#@nonl
	#@-node:ekr.20031218072017.2028:Hoist & dehoist & enablers
	#@+node:ekr.20031218072017.1759:Insert, Delete & Clone (Commands)
	#@+node:ekr.20031218072017.1760:c.checkMoveWithParentWithWarning
	def checkMoveWithParentWithWarning (self,root,parent,warningFlag):
		
		"""Return false if root or any of root's descedents is a clone of
		parent or any of parents ancestors."""
	
		message = "Illegal move or drag: no clone may contain a clone of itself"
	
		# g.trace("root",root,"parent",parent)
		clonedTnodes = {}
		for ancestor in parent.self_and_parents_iter():
			if ancestor.isCloned():
				t = ancestor.v.t
				clonedTnodes[t] = t
	
		if not clonedTnodes:
			return true
	
		for p in root.self_and_subtree_iter():
			if p.isCloned() and clonedTnodes.get(p.v.t):
				if warningFlag:
					g.alert(message)
				return false
		return true
	#@nonl
	#@-node:ekr.20031218072017.1760:c.checkMoveWithParentWithWarning
	#@+node:ekr.20031218072017.1193:c.deleteOutline
	def deleteOutline (self,op_name="Delete Node"):
		
		"""Deletes the current position.
		
		Does nothing if the outline would become empty."""
	
		c = self ; p = c.currentPosition()
		if not p: return
		# If vBack is NULL we are at the top level,
		# the next node should be v.next(), _not_ v.visNext();
		if p.hasVisBack(): newNode = p.visBack()
		else:              newNode = p.next()
		if not newNode: return
	
		c.endEditing() # Make sure we capture the headline for Undo.
		c.beginUpdate()
		if 1: # update...
			p.setAllAncestorAtFileNodesDirty()
			c.undoer.setUndoParams(op_name,p,select=newNode)
			p.doDelete(newNode)
			c.setChanged(true)
		c.endUpdate()
		c.validateOutline()
	#@nonl
	#@-node:ekr.20031218072017.1193:c.deleteOutline
	#@+node:ekr.20031218072017.1761:c.insertHeadline
	# Inserts a vnode after the current vnode.  All details are handled by the vnode class.
	
	def insertHeadline (self,op_name="Insert Node"):
	
		c = self ; p = c.currentPosition()
		hasChildren = p.hasChildren()
		isExpanded  = p.isExpanded()
		if not p: return
	
		c.beginUpdate()
		if 1: # inside update...
			if (
				# 1/31/04: Make sure new node is visible when hoisting.
				(hasChildren and isExpanded) or
				(c.hoistStack and p == c.hoistStack[-1][0])
			):
				p = p.insertAsNthChild(0)
			else:
				p = p.insertAfter()
			c.undoer.setUndoParams(op_name,p,select=p)
			c.selectVnode(p)
			c.editPosition(p)
			p.setAllAncestorAtFileNodesDirty()
			c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.1761:c.insertHeadline
	#@+node:ekr.20031218072017.1762:c.clone
	def clone (self):
	
		c = self
		p = c.currentPosition()
		if not p: return
		
		c.beginUpdate()
		if 1: # update...
			clone = p.clone(p)
			clone.setAllAncestorAtFileNodesDirty()
			c.setChanged(true)
			if c.validateOutline():
				c.selectVnode(clone)
				c.undoer.setUndoParams("Clone Node",clone)
		c.endUpdate() # updates all icons
	#@nonl
	#@-node:ekr.20031218072017.1762:c.clone
	#@+node:ekr.20031218072017.1765:c.validateOutline
	# Makes sure all nodes are valid.
	
	def validateOutline (self):
	
		c = self
		
		if not g.app.debug:
			return true
	
		root = c.rootPosition()
		parent = c.nullPosition()
	
		if root:
			return root.validateOutlineWithParent(parent)
		else:
			return true
	#@nonl
	#@-node:ekr.20031218072017.1765:c.validateOutline
	#@-node:ekr.20031218072017.1759:Insert, Delete & Clone (Commands)
	#@+node:ekr.20031218072017.1188:c.sortChildren, sortSiblings
	def sortChildren(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.hasChildren(): return
		#@	<< Set the undo info for sortChildren >>
		#@+node:ekr.20031218072017.1189:<< Set the undo info for sortChildren >>
		# Get the present list of children.
		children = []
		child = v.firstChild()
		while child:
			children.append(child)
			child = child.next()
		c.undoer.setUndoParams("Sort Children",v,sort=children)
		#@nonl
		#@-node:ekr.20031218072017.1189:<< Set the undo info for sortChildren >>
		#@nl
		c.beginUpdate()
		c.endEditing()
		v.sortChildren()
		# v.setDirty()
		v.setAllAncestorAtFileNodesDirty() # 1/12/04
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
			#@+node:ekr.20031218072017.1190:<< Set the undo info for sortSiblings >>
			# Get the present list of siblings.
			sibs = []
			sib = parent.firstChild()
			while sib:
				sibs.append(sib)
				sib = sib.next()
			c.undoer.setUndoParams("Sort Siblings",v,sort=sibs)
			#@nonl
			#@-node:ekr.20031218072017.1190:<< Set the undo info for sortSiblings >>
			#@nl
			c.beginUpdate()
			c.endEditing()
			parent.sortChildren()
			# parent.setDirty()
			parent.setAllAncestorAtFileNodesDirty() # 1/12/04
			c.setChanged(true)
			c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.1188:c.sortChildren, sortSiblings
	#@+node:ekr.20031218072017.2896:c.sortTopLevel
	def sortTopLevel (self):
		
		# Create a list of position, headline tuples
		c = self ; root = c.rootPosition()
		if not root: return
		#@	<< Set the undo info for sortTopLevel >>
		#@+node:ekr.20031218072017.2897:<< Set the undo info for sortTopLevel >>
		# Get the present list of children.
		sibs = []
		
		for sib in root.self_and_siblings_iter(copy=true):
			sibs.append(sib)
			
		c.undoer.setUndoParams("Sort Top Level",root,sort=sibs)
		#@nonl
		#@-node:ekr.20031218072017.2897:<< Set the undo info for sortTopLevel >>
		#@nl
		pairs = []
		for p in root.self_and_siblings_iter(copy=true):
			pairs.append((p.headString().lower(),p),)
		# Sort the list on the headlines.
		pairs.sort()
		sortedNodes = pairs
		# Move the nodes
		c.beginUpdate()
		h,p = sortedNodes[0]
		if p != root:
			p.setAllAncestorAtFileNodesDirty()
			p.moveToRoot(oldRoot=root)
			p.setAllAncestorAtFileNodesDirty()
		for h,next in sortedNodes[1:]:
			next.moveAfter(p)
			p = next
		if 0:
			g.trace("-----moving done")
			for p in c.rootPosition().self_and_siblings_iter():
				print p,p.v
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.2896:c.sortTopLevel
	#@-node:ekr.20031218072017.2895: Top Level...
	#@+node:ekr.20031218072017.2898:Expand & Contract...
	#@+node:ekr.20031218072017.2899:Commands
	#@+node:ekr.20031218072017.2900:contractAllHeadlines
	def contractAllHeadlines (self):
	
		c = self
		
		c.beginUpdate()
		if 1: # update...
			for p in c.allNodes_iter():
				p.contract()
			# Select the topmost ancestor of the presently selected node.
			p = c.currentPosition()
			while p and p.hasParent():
				p.moveToParent()
			c.selectVnode(p)
		c.endUpdate()
	
		c.expansionLevel = 1 # Reset expansion level.
	#@nonl
	#@-node:ekr.20031218072017.2900:contractAllHeadlines
	#@+node:ekr.20031218072017.2901:contractNode
	def contractNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.contract()
		c.endUpdate()
	#@-node:ekr.20031218072017.2901:contractNode
	#@+node:ekr.20031218072017.2902:contractParent
	def contractParent (self):
		
		c = self ; v = c.currentVnode()
		parent = v.parent()
		if not parent: return
		
		c.beginUpdate()
		c.selectVnode(parent)
		parent.contract()
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.2902:contractParent
	#@+node:ekr.20031218072017.2903:expandAllHeadlines
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
	#@-node:ekr.20031218072017.2903:expandAllHeadlines
	#@+node:ekr.20031218072017.2904:expandAllSubheads
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
	#@-node:ekr.20031218072017.2904:expandAllSubheads
	#@+node:ekr.20031218072017.2905:expandLevel1..9
	def expandLevel1 (self): self.expandToLevel(1)
	def expandLevel2 (self): self.expandToLevel(2)
	def expandLevel3 (self): self.expandToLevel(3)
	def expandLevel4 (self): self.expandToLevel(4)
	def expandLevel5 (self): self.expandToLevel(5)
	def expandLevel6 (self): self.expandToLevel(6)
	def expandLevel7 (self): self.expandToLevel(7)
	def expandLevel8 (self): self.expandToLevel(8)
	def expandLevel9 (self): self.expandToLevel(9)
	#@-node:ekr.20031218072017.2905:expandLevel1..9
	#@+node:ekr.20031218072017.2906:expandNextLevel
	def expandNextLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(c.expansionLevel + 1)
	#@-node:ekr.20031218072017.2906:expandNextLevel
	#@+node:ekr.20031218072017.2907:expandNode
	def expandNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.expand()
		c.endUpdate()
	
	#@-node:ekr.20031218072017.2907:expandNode
	#@+node:ekr.20031218072017.2908:expandPrevLevel
	def expandPrevLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(max(1,c.expansionLevel - 1))
	#@-node:ekr.20031218072017.2908:expandPrevLevel
	#@-node:ekr.20031218072017.2899:Commands
	#@+node:ekr.20031218072017.2909:Utilities
	#@+node:ekr.20031218072017.2910:contractSubtree
	def contractSubtree (self,p):
	
		for p in p.subtree_iter():
			p.contract()
	#@nonl
	#@-node:ekr.20031218072017.2910:contractSubtree
	#@+node:ekr.20031218072017.2911:expandSubtree
	def expandSubtree (self,v):
	
		c = self
		last = v.lastNode()
		while v and v != last:
			v.expand()
			v = v.threadNext()
		c.redraw()
	#@nonl
	#@-node:ekr.20031218072017.2911:expandSubtree
	#@+node:ekr.20031218072017.2912:expandToLevel
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
	#@-node:ekr.20031218072017.2912:expandToLevel
	#@-node:ekr.20031218072017.2909:Utilities
	#@-node:ekr.20031218072017.2898:Expand & Contract...
	#@+node:ekr.20031218072017.2913:Goto
	#@+node:ekr.20031218072017.1628:goNextVisitedNode
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
	#@-node:ekr.20031218072017.1628:goNextVisitedNode
	#@+node:ekr.20031218072017.1627:goPrevVisitedNode
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
	#@-node:ekr.20031218072017.1627:goPrevVisitedNode
	#@+node:ekr.20031218072017.2914:goToFirstNode
	def goToFirstNode(self):
		
		c = self
		v = c.rootVnode()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.2914:goToFirstNode
	#@+node:ekr.20031218072017.2915:goToLastNode
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
	
	#@-node:ekr.20031218072017.2915:goToLastNode
	#@+node:ekr.20031218072017.2916:goToNextClone
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
	#@-node:ekr.20031218072017.2916:goToNextClone
	#@+node:ekr.20031218072017.2917:goToNextDirtyHeadline
	def goToNextDirtyHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		while v and not v.isDirty():
			v = v.threadNext()
	
		if not v:
			# Wrap around.
			v = c.rootVnode()
			while v and not v.isDirty():
				v = v.threadNext()
	
		if v:
			c.selectVnode(v)
		else:
			g.es("done",color="blue")
	#@nonl
	#@-node:ekr.20031218072017.2917:goToNextDirtyHeadline
	#@+node:ekr.20031218072017.2918:goToNextMarkedHeadline
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
		else:
			g.es("done",color="blue")
	#@nonl
	#@-node:ekr.20031218072017.2918:goToNextMarkedHeadline
	#@+node:ekr.20031218072017.2919:goToNextSibling
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
	#@-node:ekr.20031218072017.2919:goToNextSibling
	#@+node:ekr.20031218072017.2920:goToParent
	def goToParent(self):
		
		c = self
		v = c.currentVnode()
		if not v: return
		p = v.parent()
		if p:
			c.beginUpdate()
			c.selectVnode(p)
			c.endUpdate()
	#@-node:ekr.20031218072017.2920:goToParent
	#@+node:ekr.20031218072017.2921:goToPrevSibling
	def goToPrevSibling(self):
		
		c = self
		v = c.currentVnode()
		if not v: return
		back = v.back()
		if back:
			c.beginUpdate()
			c.selectVnode(back)
			c.endUpdate()
	#@-node:ekr.20031218072017.2921:goToPrevSibling
	#@-node:ekr.20031218072017.2913:Goto
	#@+node:ekr.20031218072017.2922:Mark...
	#@+node:ekr.20031218072017.2923:markChangedHeadlines
	def markChangedHeadlines (self): 
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				v.setMarked()
				c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
		g.es("done",color="blue")
	#@-node:ekr.20031218072017.2923:markChangedHeadlines
	#@+node:ekr.20031218072017.2924:markChangedRoots
	def markChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				s = v.bodyString()
				flag, i = g.is_special(s,0,"@root")
				if flag:
					v.setMarked()
					c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
		g.es("done",color="blue")
	#@nonl
	#@-node:ekr.20031218072017.2924:markChangedRoots
	#@+node:ekr.20031218072017.2925:markAllAtFileNodesDirty
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
	#@-node:ekr.20031218072017.2925:markAllAtFileNodesDirty
	#@+node:ekr.20031218072017.2926:markAtFileNodesDirty
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
	#@-node:ekr.20031218072017.2926:markAtFileNodesDirty
	#@+node:ekr.20031218072017.2927:markClones
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
	#@-node:ekr.20031218072017.2927:markClones
	#@+node:ekr.20031218072017.2928:markHeadline
	def markHeadline (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		c.beginUpdate()
		if v.isMarked():
			v.clearMarked()
		else:
			v.setMarked()
			v.setDirty()
			if 0: # 4/3/04: Marking a headline is a minor operation.
				c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.2928:markHeadline
	#@+node:ekr.20031218072017.2929:markSubheads
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
	#@-node:ekr.20031218072017.2929:markSubheads
	#@+node:ekr.20031218072017.2930:unmarkAll
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
	#@-node:ekr.20031218072017.2930:unmarkAll
	#@-node:ekr.20031218072017.2922:Mark...
	#@+node:ekr.20031218072017.1766:Move... (Commands)
	#@+node:ekr.20031218072017.1767:demote
	def demote(self):
	
		c = self ; p = c.currentPosition()
		if not p or not p.hasNext(): return
	
		last = p.lastChild()
		# Make sure all the moves will be valid.
		for child in p.children_iter():
			if not c.checkMoveWithParentWithWarning(child,p,true):
				return
		c.beginUpdate()
		if 1: # update...
			c.endEditing()
			while p.hasNext(): # Do not use iterator here.
				child = p.next()
				child.moveToNthChildOf(p,p.numberOfChildren())
			p.expand()
			c.selectVnode(p)
			p.setAllAncestorAtFileNodesDirty()
			c.setChanged(true)
		c.endUpdate()
		c.undoer.setUndoParams("Demote",p,lastChild=last)
		c.updateSyntaxColorer(p) # Moving can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.1767:demote
	#@+node:ekr.20031218072017.1768:moveOutlineDown
	#@+at 
	#@nonl
	# Moving down is more tricky than moving up; we can't move p to be a child 
	# of itself.  An important optimization:  we don't have to call 
	# checkMoveWithParentWithWarning() if the parent of the moved node remains 
	# the same.
	#@-at
	#@@c
	
	def moveOutlineDown(self):
	
		c = self ; p = c.currentPosition()
		if not p: return
	
		if not c.canMoveOutlineDown(): # 11/4/03: Support for hoist.
			if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
			return
		# Set next to the node after which p will be moved.
		next = p.visNext()
		while next and p.isAncestorOf(next):
			next = next.visNext()
		if not next: return
		c.beginUpdate()
		if 1: # update...
			c.endEditing()
			p.setAllAncestorAtFileNodesDirty()
			#@		<< Move v down >>
			#@+node:ekr.20031218072017.1769:<< Move v down >>
			# Remember both the before state and the after state for undo/redo
			oldBack = p.back()
			oldParent = p.parent()
			oldN = p.childIndex()
			
			if next.hasChildren() and next.isExpanded():
				# Attempt to move p to the first child of next.
				if c.checkMoveWithParentWithWarning(p,next,true):
					p.moveToNthChildOf(next,0)
					c.undoer.setUndoParams("Move Down",p,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			else:
				# Attempt to move p after next.
				if c.checkMoveWithParentWithWarning(p,next.parent(),true):
					p.moveAfter(next)
					c.undoer.setUndoParams("Move Down",p,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			#@nonl
			#@-node:ekr.20031218072017.1769:<< Move v down >>
			#@nl
			p.setAllAncestorAtFileNodesDirty()
			c.selectVnode(p)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(p) # Moving can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.1768:moveOutlineDown
	#@+node:ekr.20031218072017.1770:moveOutlineLeft
	def moveOutlineLeft(self):
		
		c = self ; p = c.currentPosition()
		if not p: return
	
		if not c.canMoveOutlineLeft(): # 11/4/03: Support for hoist.
			if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
			return
		
		if not p.hasParent(): return
		# Remember both the before state and the after state for undo/redo
		parent = p.parent()
		oldBack = p.back()
		oldParent = p.parent()
		oldN = p.childIndex()
		c.beginUpdate()
		if 1: # update...
			c.endEditing()
			p.setAllAncestorAtFileNodesDirty()
			p.moveAfter(parent)
			c.undoer.setUndoParams("Move Left",p,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			p.setAllAncestorAtFileNodesDirty()
			c.selectVnode(p)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(p) # Moving can change syntax coloring.
	#@-node:ekr.20031218072017.1770:moveOutlineLeft
	#@+node:ekr.20031218072017.1771:moveOutlineRight
	def moveOutlineRight(self):
		
		c = self ; p = c.currentPosition()
		if not p: return
		
		if not c.canMoveOutlineRight(): # 11/4/03: Support for hoist.
			if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
			return
		
		if not p.hasBack: return
		back = p.back()
		if not c.checkMoveWithParentWithWarning(p,back,true): return
	
		# Remember both the before state and the after state for undo/redo
		oldBack = back
		oldParent = p.parent()
		oldN = p.childIndex()
		c.beginUpdate()
		if 1: # update...
			c.endEditing()
			p.setAllAncestorAtFileNodesDirty()
			n = back.numberOfChildren()
			p.moveToNthChildOf(back,n)
			c.undoer.setUndoParams("Move Right",p,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			p.setAllAncestorAtFileNodesDirty()
			c.selectVnode(p)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(p) # Moving can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.1771:moveOutlineRight
	#@+node:ekr.20031218072017.1772:moveOutlineUp
	def moveOutlineUp(self):
	
		c = self ; p = c.currentPosition()
		if not p: return
	
		if not c.canMoveOutlineUp(): # 11/4/03: Support for hoist.
			if c.hoistStack: g.es("Can't move node out of hoisted outline",color="blue")
			return
		back = p.visBack()
		if not back: return
		back2 = back.visBack()
		# A weird special case: just select back2.
		if back2 and p.v in back2.v.t.vnodeList:
			# g.trace('-'*20,"no move, selecting visBack")
			c.selectVnode(back2)
			return
		c = self
		c.beginUpdate()
		if 1: # update...
			c.endEditing()
			p.setAllAncestorAtFileNodesDirty()
			#@		<< Move v up >>
			#@+node:ekr.20031218072017.1773:<< Move v up >>
			# Remember both the before state and the after state for undo/redo
			oldBack = p.back()
			oldParent = p.parent()
			oldN = p.childIndex()
			if 0:
				g.trace("visBack",back)
				g.trace("visBack2",back2)
				g.trace("oldParent",oldParent)
				g.trace("back2.hasChildren",back2.hasChildren())
				g.trace("back2.isExpanded",back2.isExpanded())
			
			if not back2:
				# p will be the new root node
				p.moveToRoot(c.rootVnode())
				c.undoer.setUndoParams("Move Up",p,
					oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			elif back2.hasChildren() and back2.isExpanded():
				if c.checkMoveWithParentWithWarning(p,back2,true):
					p.moveToNthChildOf(back2,0)
					c.undoer.setUndoParams("Move Up",p,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			elif c.checkMoveWithParentWithWarning(p,back2.parent(),true):
				# Insert after back2.
				p.moveAfter(back2)
				c.undoer.setUndoParams("Move Up",p,
					oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			#@nonl
			#@-node:ekr.20031218072017.1773:<< Move v up >>
			#@nl
			p.setAllAncestorAtFileNodesDirty()
			c.selectVnode(p)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(p) # Moving can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.1772:moveOutlineUp
	#@+node:ekr.20031218072017.1774:promote
	def promote(self):
	
		c = self ; p = c.currentPosition()
		if not p or not p.hasChildren(): return
	
		last = p.lastChild()
		c.beginUpdate()
		if 1: # update...
			c.endEditing()
			after = p
			while p.hasChildren(): # Don't use an iterator.
				child = p.firstChild()
				child.moveAfter(after)
				after = child
			p.setAllAncestorAtFileNodesDirty()
			c.setChanged(true)
			c.selectVnode(p)
		c.endUpdate()
		c.undoer.setUndoParams("Promote",p,lastChild=last)
		c.updateSyntaxColorer(p) # Moving can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.1774:promote
	#@-node:ekr.20031218072017.1766:Move... (Commands)
	#@-node:ekr.20031218072017.2894:Outline menu...
	#@+node:ekr.20031218072017.2931:Window Menu
	#@+node:ekr.20031218072017.2092:openCompareWindow
	def openCompareWindow (self):
		
		c = self ; frame = c.frame
		
		if not frame.comparePanel:
			frame.comparePanel = g.app.gui.createComparePanel(c)
	
		frame.comparePanel.bringToFront()
	#@nonl
	#@-node:ekr.20031218072017.2092:openCompareWindow
	#@+node:ekr.20031218072017.2932:openPythonWindow (Dave Hein)
	def openPythonWindow(self):
	
		if sys.platform == "linux2":
			#@		<< open idle in Linux >>
			#@+node:ekr.20031218072017.2933:<< open idle in Linux >>
			# 09-SEP-2002 DHEIN: Open Python window under linux
			
			try:
				pathToLeo = g.os_path_join(g.app.loadDir,"leo.py")
				sys.argv = [pathToLeo]
				from idlelib import idle
				if g.app.idle_imported:
					reload(idle)
				g.app.idle_imported = true
			except:
				try:
					g.es("idlelib could not be imported.")
					g.es("Probably IDLE is not installed.")
					g.es("Run Tools/idle/setup.py to build idlelib.")
					g.es("Can not import idle")
					g.es_exception() # This can fail!!
				except: pass
			#@-node:ekr.20031218072017.2933:<< open idle in Linux >>
			#@nl
		else:
			#@		<< open idle in Windows >>
			#@+node:ekr.20031218072017.2934:<< open idle in Windows >>
			# Initialize argv: the -t option sets the title of the Idle interp window.
			sys.argv = ["leo"] # ,"-t","Leo"]
			
			ok = false
			if g.CheckVersion(sys.version,"2.3"):
				#@	<< Try to open idle in Python 2.3 systems >>
				#@+node:ekr.20031218072017.2936:<< Try to open idle in Python 2.3 systems >>
				try:
					idle_dir = None
					
					import idlelib.PyShell
				
					if g.app.idle_imported:
						reload(idle)
						g.app.idle_imported = true
						
					idlelib.PyShell.main()
					ok = true
				
				except:
					ok = false
					g.es_exception()
				#@nonl
				#@-node:ekr.20031218072017.2936:<< Try to open idle in Python 2.3 systems >>
				#@nl
			else:
				#@	<< Try to open idle in Python 2.2 systems >>
				#@+node:ekr.20031218072017.2935:<< Try to open idle in Python 2.2 systems>>
				try:
					executable_dir = g.os_path_dirname(sys.executable)
					idle_dir = g.os_path_join(executable_dir,"Tools","idle")
				
					# 1/29/04: sys.path doesn't handle unicode in 2.2.
					idle_dir = str(idle_dir) # May throw an exception.
				
					# 1/29/04: must add idle_dir to sys.path even when using importFromPath.
					if idle_dir not in sys.path:
						sys.path.insert(0,idle_dir)
				
					if 1:
						import PyShell
					else: # Works, but is not better than import.
						PyShell = g.importFromPath("PyShell",idle_dir)
				
					if g.app.idle_imported:
						reload(idle)
						g.app.idle_imported = true
						
					if 1: # Mostly works, but causes problems when opening other .leo files.
						PyShell.main()
					else: # Doesn't work: destroys all of Leo when Idle closes.
						self.leoPyShellMain()
					ok = true
				except ImportError:
					ok = false
					g.es_exception()
				#@nonl
				#@-node:ekr.20031218072017.2935:<< Try to open idle in Python 2.2 systems>>
				#@nl
			
			if not ok:
				g.es("Can not import idle")
				if idle_dir and idle_dir not in sys.path:
					g.es("Please add '%s' to sys.path" % idle_dir)
			#@nonl
			#@-node:ekr.20031218072017.2934:<< open idle in Windows >>
			#@nl
	#@+node:ekr.20031218072017.2937:leoPyShellMain
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
		root = g.app.root
		PyShell.fixwordbreaks(root)
		flist = PyShell.PyShellFileList(root)
		shell = PyShell.PyShell(flist)
		flist.pyshell = shell
		shell.begin()
	#@nonl
	#@-node:ekr.20031218072017.2937:leoPyShellMain
	#@-node:ekr.20031218072017.2932:openPythonWindow (Dave Hein)
	#@-node:ekr.20031218072017.2931:Window Menu
	#@+node:ekr.20031218072017.2938:Help Menu
	#@+node:ekr.20031218072017.2939:about (version number & date)
	def about(self):
		
		c = self
		
		# Don't use triple-quoted strings or continued strings here.
		# Doing so would add unwanted leading tabs.
		version = c.getSignOnLine() + "\n\n"
		copyright = (
			"Copyright 1999-2004 by Edward K. Ream\n" +
			"All Rights Reserved\n" +
			"Leo is distributed under the Python License")
		url = "http://webpages.charter.net/edreamleo/front.html"
		email = "edreamleo@charter.net"
	
		g.app.gui.runAboutLeoDialog(version,copyright,url,email)
	#@nonl
	#@-node:ekr.20031218072017.2939:about (version number & date)
	#@+node:ekr.20031218072017.2940:leoDocumentation
	def leoDocumentation (self):
		
		c = self
	
		fileName = g.os_path_join(g.app.loadDir,"..","doc","LeoDocs.leo")
	
		try:
			g.openWithFileName(fileName,c)
		except:
			g.es("not found: LeoDocs.leo")
	#@-node:ekr.20031218072017.2940:leoDocumentation
	#@+node:ekr.20031218072017.2941:leoHome
	def leoHome (self):
		
		import webbrowser
	
		url = "http://webpages.charter.net/edreamleo/front.html"
		try:
			webbrowser.open_new(url)
		except:
			g.es("not found: " + url)
	#@nonl
	#@-node:ekr.20031218072017.2941:leoHome
	#@+node:ekr.20031218072017.2942:leoTutorial (version number)
	def leoTutorial (self):
		
		import webbrowser
	
		if 1: # new url
			url = "http://www.3dtree.com/ev/e/sbooks/leo/sbframetoc_ie.htm"
		else:
			url = "http://www.evisa.com/e/sbooks/leo/sbframetoc_ie.htm"
		try:
			webbrowser.open_new(url)
		except:
			g.es("not found: " + url)
	#@nonl
	#@-node:ekr.20031218072017.2942:leoTutorial (version number)
	#@+node:ekr.20031218072017.2943:leoConfig
	def leoConfig (self):
	
		# 4/21/03 new code suggested by fBechmann@web.de
		c = self
		loadDir = g.app.loadDir
		configDir = g.app.config.configDir
	
		# Look in configDir first.
		fileName = g.os_path_join(configDir, "leoConfig.leo")
	
		ok, frame = g.openWithFileName(fileName,c)
		if not ok:
			if configDir == loadDir:
				g.es("leoConfig.leo not found in " + loadDir)
			else:
				# Look in loadDir second.
				fileName = g.os_path_join(loadDir,"leoConfig.leo")
	
				ok, frame = g.openWithFileName(fileName,c)
				if not ok:
					g.es("leoConfig.leo not found in " + configDir + " or " + loadDir)
	#@nonl
	#@-node:ekr.20031218072017.2943:leoConfig
	#@+node:ekr.20031218072017.2944:applyConfig
	def applyConfig (self):
	
		c = self
		g.app.config.init()
		c.frame.reconfigureFromConfig()
	#@nonl
	#@-node:ekr.20031218072017.2944:applyConfig
	#@-node:ekr.20031218072017.2938:Help Menu
	#@-node:ekr.20031218072017.2818:Command handlers...
	#@+node:ekr.20031218072017.2945:Dragging (commands)
	#@+node:ekr.20031218072017.2353:c.dragAfter
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
			# v.setDirty()
			v.setAllAncestorAtFileNodesDirty() # 1/12/04
			v.moveAfter(after)
			c.undoer.setUndoParams("Drag",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			# v.setDirty()
			v.setAllAncestorAtFileNodesDirty() # 1/12/04
			c.selectVnode(v)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.2353:c.dragAfter
	#@+node:ekr.20031218072017.2946:c.dragCloneToNthChildOf (changed in 3.11.1)
	def dragCloneToNthChildOf (self,v,parent,n):
	
		c = self
		c.beginUpdate()
		# g.trace("v,parent,n:",v.headString(),parent.headString(),n)
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
		# clone.setDirty()
		clone.setAllAncestorAtFileNodesDirty() # 1/12/04
		clone.moveToNthChildOf(parent,n)
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		# clone.setDirty()
		clone.setAllAncestorAtFileNodesDirty() # 1/12/04
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@-node:ekr.20031218072017.2946:c.dragCloneToNthChildOf (changed in 3.11.1)
	#@+node:ekr.20031218072017.2947:c.dragToNthChildOf
	def dragToNthChildOf(self,v,parent,n):
	
		# g.es("dragToNthChildOf")
		c = self
		if not c.checkMoveWithParentWithWarning(v,parent,true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			# v.setDirty()
			v.setAllAncestorAtFileNodesDirty() # 1/12/04
			v.moveToNthChildOf(parent,n)
			c.undoer.setUndoParams("Drag",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			# v.setDirty()
			v.setAllAncestorAtFileNodesDirty() # 1/12/04
			c.selectVnode(v)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.2947:c.dragToNthChildOf
	#@+node:ekr.20031218072017.2948:c.dragCloneAfter
	def dragCloneAfter (self,v,after):
	
		c = self
		c.beginUpdate()
		clone = v.clone(v) # Creates clone & dependents, does not set undo.
		# g.trace("v,after:",v.headString(),after.headString())
		if not c.checkMoveWithParentWithWarning(clone,after.parent(),true):
			g.trace("invalid clone move")
			clone.doDelete(v) # Destroys clone & dependents. Makes v the current node.
			c.endUpdate(false) # Nothing has changed.
			return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.endEditing()
		# clone.setDirty()
		clone.setAllAncestorAtFileNodesDirty() # 1/12/04
		clone.moveAfter(after)
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		# clone.setDirty()
		clone.setAllAncestorAtFileNodesDirty() # 1/12/04
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@nonl
	#@-node:ekr.20031218072017.2948:c.dragCloneAfter
	#@-node:ekr.20031218072017.2945:Dragging (commands)
	#@+node:ekr.20031218072017.2949:Drawing Utilities (commands)
	#@+node:ekr.20031218072017.2950:beginUpdate
	def beginUpdate(self):
	
		self.frame.tree.beginUpdate()
		
	BeginUpdate = beginUpdate # Compatibility with old scripts
	#@nonl
	#@-node:ekr.20031218072017.2950:beginUpdate
	#@+node:ekr.20031218072017.2951:bringToFront
	def bringToFront(self):
	
		self.frame.deiconify()
	
	BringToFront = bringToFront # Compatibility with old scripts
	#@nonl
	#@-node:ekr.20031218072017.2951:bringToFront
	#@+node:ekr.20031218072017.2952:endUpdate
	def endUpdate(self, flag=true):
		
		self.frame.tree.endUpdate(flag)
		
	EndUpdate = endUpdate # Compatibility with old scripts
	#@nonl
	#@-node:ekr.20031218072017.2952:endUpdate
	#@+node:ekr.20031218072017.2953:recolor
	def recolor(self):
	
		c = self
	
		c.frame.body.recolor(c.currentVnode())
	#@nonl
	#@-node:ekr.20031218072017.2953:recolor
	#@+node:ekr.20031218072017.2954:redraw & repaint
	def redraw(self):
	
		self.frame.tree.redraw()
		
	# Compatibility with old scripts
	Redraw = redraw 
	repaint = redraw
	Repaint = redraw
	#@nonl
	#@-node:ekr.20031218072017.2954:redraw & repaint
	#@-node:ekr.20031218072017.2949:Drawing Utilities (commands)
	#@+node:ekr.20031218072017.2955:Enabling Menu Items
	#@+node:ekr.20040323172420:Slow routines: no longer used
	#@+node:ekr.20031218072017.2966:canGoToNextDirtyHeadline (slow)
	def canGoToNextDirtyHeadline (self):
		
		c = self ; current = c.currentPosition()
	
		for p in c.allNodes_iter():
			if p != current and p.isDirty():
				return true
		
		return false
	#@nonl
	#@-node:ekr.20031218072017.2966:canGoToNextDirtyHeadline (slow)
	#@+node:ekr.20031218072017.2967:canGoToNextMarkedHeadline (slow)
	def canGoToNextMarkedHeadline (self):
		
		c = self ; current = c.currentPosition()
			
		for p in c.allNodes_iter():
			if p != current and p.isMarked():
				return true
	
		return false
	#@-node:ekr.20031218072017.2967:canGoToNextMarkedHeadline (slow)
	#@+node:ekr.20031218072017.2968:canMarkChangedHeadline (slow)
	def canMarkChangedHeadlines (self):
		
		c = self
		
		for p in c.allNodes_iter():
			if p.isDirty():
				return true
		
		return false
	#@nonl
	#@-node:ekr.20031218072017.2968:canMarkChangedHeadline (slow)
	#@+node:ekr.20031218072017.2969:canMarkChangedRoots (slow)
	def canMarkChangedRoots (self):
		
		c = self
		
		for p in c.allNodes_iter():
			if p.isDirty and p.isAnyAtFileNode():
				return true
	
		return false
	#@nonl
	#@-node:ekr.20031218072017.2969:canMarkChangedRoots (slow)
	#@-node:ekr.20040323172420:Slow routines: no longer used
	#@+node:ekr.20040131170659:canClone (new for hoist)
	def canClone (self):
	
		c = self
		
		if c.hoistStack:
			current = c.currentPosition()
			p,junk = c.hoistStack[-1]
			return current != p
		else:
			return true
	#@nonl
	#@-node:ekr.20040131170659:canClone (new for hoist)
	#@+node:ekr.20031218072017.2956:canContractAllHeadlines
	def canContractAllHeadlines (self):
		
		c = self
		
		for p in c.allNodes_iter():
			if p.isExpanded():
				return true
	
		return false
	#@nonl
	#@-node:ekr.20031218072017.2956:canContractAllHeadlines
	#@+node:ekr.20031218072017.2957:canContractAllSubheads
	def canContractAllSubheads (self):
	
		c = self ; current = c.currentPosition()
		
		for p in current.subtree_iter():
			if p != current and p.isExpanded():
				return true
	
		return false
	#@nonl
	#@-node:ekr.20031218072017.2957:canContractAllSubheads
	#@+node:ekr.20031218072017.2958:canContractParent
	def canContractParent (self):
	
		c = self
		return c.currentPosition().parent()
	#@nonl
	#@-node:ekr.20031218072017.2958:canContractParent
	#@+node:ekr.20031218072017.2959:canContractSubheads
	def canContractSubheads (self):
		
		c = self ; current = c.currentPosition()
	
		for child in current.children_iter():
			if child.isExpanded():
				return true
			
		return false
	#@nonl
	#@-node:ekr.20031218072017.2959:canContractSubheads
	#@+node:ekr.20031218072017.2960:canCutOutline & canDeleteHeadline
	def canDeleteHeadline (self):
		
		c = self ; p = c.currentPosition()
	
		return p.hasParent() or p.hasThreadBack() or p.hasNext()
	
	canCutOutline = canDeleteHeadline
	#@nonl
	#@-node:ekr.20031218072017.2960:canCutOutline & canDeleteHeadline
	#@+node:ekr.20031218072017.2961:canDemote
	def canDemote (self):
	
		c = self
		return c.currentPosition().hasNext()
	#@nonl
	#@-node:ekr.20031218072017.2961:canDemote
	#@+node:ekr.20031218072017.2962:canExpandAllHeadlines
	def canExpandAllHeadlines (self):
		
		c = self
		
		for p in c.allNodes_iter():
			if not p.isExpanded():
				return true
	
		return false
	#@-node:ekr.20031218072017.2962:canExpandAllHeadlines
	#@+node:ekr.20031218072017.2963:canExpandAllSubheads
	def canExpandAllSubheads (self):
	
		c = self
		
		for p in c.currentPosition().subtree_iter():
			if not p.isExpanded():
				return true
			
		return false
	#@nonl
	#@-node:ekr.20031218072017.2963:canExpandAllSubheads
	#@+node:ekr.20031218072017.2964:canExpandSubheads
	def canExpandSubheads (self):
	
		c = self
		
		for p in c.currentPosition().children_iter():
			if p != current and not p.isExpanded():
				return true
	
		return false
	#@nonl
	#@-node:ekr.20031218072017.2964:canExpandSubheads
	#@+node:ekr.20031218072017.2287:canExtract, canExtractSection & canExtractSectionNames
	def canExtract (self):
	
		c = self ; body = c.frame.body
		return body and body.hasTextSelection()
		
	canExtractSectionNames = canExtract
			
	def canExtractSection (self):
	
		c = self ; body = c.frame.body
		if not body: return false
		
		s = body.getSelectedText()
		if not s: return false
	
		line = g.get_line(s,0)
		i1 = line.find("<<")
		j1 = line.find(">>")
		i2 = line.find("@<")
		j2 = line.find("@>")
		return -1 < i1 < j1 or -1 < i2 < j2
	#@nonl
	#@-node:ekr.20031218072017.2287:canExtract, canExtractSection & canExtractSectionNames
	#@+node:ekr.20031218072017.2965:canFindMatchingBracket
	def canFindMatchingBracket (self):
		
		c = self ; brackets = "()[]{}"
		c1 = c.frame.body.getCharAtInsertPoint()
		c2 = c.frame.body.getCharBeforeInsertPoint()
		return (c1 and c1 in brackets) or (c2 and c2 in brackets)
	#@nonl
	#@-node:ekr.20031218072017.2965:canFindMatchingBracket
	#@+node:ekr.20040303165342:canHoist & canDehoist
	def canDehoist(self):
		
		return len(self.hoistStack) > 0
			
	def canHoist(self):
		
		c = self
		root = c.rootPosition()
		p = c.currentPosition()
	
		if c.hoistStack:
			p2,junk = c.hoistStack[-1]
			return p2 != p
		elif p == root:
			return p.hasNext()
		else:
			return true
	#@nonl
	#@-node:ekr.20040303165342:canHoist & canDehoist
	#@+node:ekr.20031218072017.2970:canMoveOutlineDown (changed for hoist)
	def canMoveOutlineDown (self):
	
		c = self ; current = c.currentPosition()
			
		p = current.visNext()
		while p and current.isAncestorOf(p):
			p.moveToVisNext()
	
		if c.hoistStack:
			h,junk = c.hoistStack[-1]
			return p and p != h and h.isAncestorOf(p)
		else:
			return p
	#@nonl
	#@-node:ekr.20031218072017.2970:canMoveOutlineDown (changed for hoist)
	#@+node:ekr.20031218072017.2971:canMoveOutlineLeft (changed for hoist)
	def canMoveOutlineLeft (self):
	
		c = self ; p = c.currentPosition()
	
		if c.hoistStack:
			h,junk = c.hoistStack[-1]
			if p and p.hasParent():
				p.moveToParent()
				return p != h and h.isAncestorOf(p)
			else:
				return false
		else:
			return p and p.hasParent()
	#@nonl
	#@-node:ekr.20031218072017.2971:canMoveOutlineLeft (changed for hoist)
	#@+node:ekr.20031218072017.2972:canMoveOutlineRight (changed for hoist)
	def canMoveOutlineRight (self):
	
		c = self ; p = c.currentPosition()
		
		if c.hoistStack:
			h,junk = c.hoistStack[-1]
			return p and p.hasBack() and p != h
		else:
			return p and p.hasBack()
	#@nonl
	#@-node:ekr.20031218072017.2972:canMoveOutlineRight (changed for hoist)
	#@+node:ekr.20031218072017.2973:canMoveOutlineUp (changed for hoist)
	def canMoveOutlineUp (self):
	
		c = self ; p = c.currentPosition()
		if not p: return false
		
		pback = p.visBack()
		if not pback: return false
	
		if c.hoistStack:
			h,junk = c.hoistStack[-1]
			return h != p and h.isAncestorOf(pback)
		else:
			return true
	#@nonl
	#@-node:ekr.20031218072017.2973:canMoveOutlineUp (changed for hoist)
	#@+node:ekr.20031218072017.2974:canPasteOutline
	def canPasteOutline (self,s=None):
	
		c = self
		if s == None:
			s = g.app.gui.getTextFromClipboard()
		if not s:
			return false
	
		# g.trace(s)
		if g.match(s,0,g.app.prolog_prefix_string):
			return true
		elif len(s) > 0:
			return c.importCommands.stringIsValidMoreFile(s)
		else:
			return false
	#@nonl
	#@-node:ekr.20031218072017.2974:canPasteOutline
	#@+node:ekr.20031218072017.2975:canPromote
	def canPromote (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
	#@nonl
	#@-node:ekr.20031218072017.2975:canPromote
	#@+node:ekr.20031218072017.2976:canRevert
	def canRevert (self):
	
		# c.mFileName will be "untitled" for unsaved files.
		c = self
		return (c.frame and c.mFileName and c.isChanged())
	#@nonl
	#@-node:ekr.20031218072017.2976:canRevert
	#@+node:ekr.20031218072017.2977:canSelect....
	# 7/29/02: The shortcuts for these commands are now unique.
	
	def canSelectThreadBack (self):
		c = self ; p = c.currentPosition()
		return p.hasThreadBack()
		
	def canSelectThreadNext (self):
		c = self ; p = c.currentPosition()
		return p.hasThreadNext()
	
	def canSelectVisBack (self):
		c = self ; p = c.currentPosition()
		return p.hasVisBack()
		
	def canSelectVisNext (self):
		c = self ; p = c.currentPosition()
		return p.hasVisNext()
	#@nonl
	#@-node:ekr.20031218072017.2977:canSelect....
	#@+node:ekr.20031218072017.2978:canShiftBodyLeft/Right
	def canShiftBodyLeft (self):
	
		c = self ; body = c.frame.body
		return body and body.getAllText()
	
	canShiftBodyRight = canShiftBodyLeft
	#@nonl
	#@-node:ekr.20031218072017.2978:canShiftBodyLeft/Right
	#@+node:ekr.20031218072017.2979:canSortChildren, canSortSiblings
	def canSortChildren (self):
		
		c = self ; p = c.currentPosition()
		return p and p.hasChildren()
	
	def canSortSiblings (self):
	
		c = self ; p = c.currentPosition()
		return p and (p.hasNext() or p.hasBack())
	#@nonl
	#@-node:ekr.20031218072017.2979:canSortChildren, canSortSiblings
	#@+node:ekr.20031218072017.2980:canUndo & canRedo
	def canUndo (self):
	
		c = self
		return c.undoer.canUndo()
		
	def canRedo (self):
	
		c = self
		return c.undoer.canRedo()
	#@nonl
	#@-node:ekr.20031218072017.2980:canUndo & canRedo
	#@+node:ekr.20031218072017.2981:canUnmarkAll
	def canUnmarkAll (self):
		
		c = self
		
		for p in c.allNodes_iter():
			if p.isMarked():
				return true
	
		return false
	#@nonl
	#@-node:ekr.20031218072017.2981:canUnmarkAll
	#@-node:ekr.20031218072017.2955:Enabling Menu Items
	#@+node:ekr.20031218072017.2982:Getters & Setters
	#@+node:ekr.20031218072017.2983:c.currentPosition & c.setCurrentPosition
	def currentPosition (self,copy=true):
		
		"""Return the presently selected position."""
		
		return self._currentPosition.copy()
		
	def setCurrentPosition (self,p):
		
		"""Set the presently selected position."""
	
		self._currentPosition = p
		
	# Define these for compatibiility with old scripts.
	currentVnode = currentPosition
	setCurrentVnode = setCurrentPosition
	#@nonl
	#@-node:ekr.20031218072017.2983:c.currentPosition & c.setCurrentPosition
	#@+node:ekr.20031218072017.2984:c.clearAllMarked
	def clearAllMarked (self):
	
		c = self
	
		for p in c.allNodes_iter():
			p.v.clearMarked()
	#@nonl
	#@-node:ekr.20031218072017.2984:c.clearAllMarked
	#@+node:ekr.20031218072017.2985:c.clearAllVisited
	def clearAllVisited (self):
	
		c = self
	
		for p in c.allNodes_iter():
			p.v.clearVisited()
			p.v.t.clearVisited()
			p.v.t.clearWriteBit()
	#@-node:ekr.20031218072017.2985:c.clearAllVisited
	#@+node:ekr.20031218072017.2986:c.fileName
	# Compatibility with scripts
	
	def fileName (self):
	
		return self.mFileName
	#@-node:ekr.20031218072017.2986:c.fileName
	#@+node:ekr.20031218072017.2987:c.isChanged
	def isChanged (self):
	
		return self.changed
	#@nonl
	#@-node:ekr.20031218072017.2987:c.isChanged
	#@+node:ekr.20031218072017.2988:c.rootPosition & c.setRootPosition
	def rootPosition(self):
		
		"""Return the root position."""
		
		return self._rootPosition.copy()
	
	def setRootPosition(self,p):
		
		"""Set the root positioin."""
	
		self._rootPosition = p.copy() # Potential bug fix: 5/2/04
		
	# Define these for compatibiility with old scripts.
	rootVnode = rootPosition
	setRootVnode = setRootPosition
	#@nonl
	#@-node:ekr.20031218072017.2988:c.rootPosition & c.setRootPosition
	#@+node:ekr.20040311173238:c.topPosition & c.setTopPosition
	def topPosition(self):
		
		"""Return the root position."""
		
		return self._topPosition.copy()
	
	def setTopPosition(self,p):
		
		"""Set the root positioin."""
	
		self._topPosition = p
		
	# Define these for compatibiility with old scripts.
	topVnode = topPosition
	setTopVnode = setTopPosition
	#@nonl
	#@-node:ekr.20040311173238:c.topPosition & c.setTopPosition
	#@+node:ekr.20031218072017.2989:c.setChanged
	def setChanged (self,changedFlag):
	
		c = self
		if not c.frame: return
		# Clear all dirty bits _before_ setting the caption.
		# 9/15/01 Clear all dirty bits except orphaned @file nodes
		if not changedFlag:
			# g.trace("clearing all dirty bits")
			for p in c.allNodes_iter():
				if p.isDirty() and not (p.isAtFileNode() or p.isAtNorefFileNode()):
					p.clearDirty()
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
	#@-node:ekr.20031218072017.2989:c.setChanged
	#@+node:ekr.20040311094927:c.nullPosition
	def nullPosition (self):
		
		return leoNodes.position(None,[])
	#@nonl
	#@-node:ekr.20040311094927:c.nullPosition
	#@-node:ekr.20031218072017.2982:Getters & Setters
	#@+node:ekr.20031218072017.2990:Selecting & Updating (commands)
	#@+node:ekr.20031218072017.2991:c.editVnode (calls tree.editLabel)
	# Selects v: sets the focus to p and edits p.
	
	def editPosition(self,p):
	
		c = self
	
		if p:
			c.selectVnode(p)
			c.frame.tree.editLabel(p)
	#@nonl
	#@-node:ekr.20031218072017.2991:c.editVnode (calls tree.editLabel)
	#@+node:ekr.20031218072017.2992:endEditing (calls tree.endEditLabel)
	# Ends the editing in the outline.
	
	def endEditing(self):
	
		self.frame.tree.endEditLabel()
	#@-node:ekr.20031218072017.2992:endEditing (calls tree.endEditLabel)
	#@+node:ekr.20031218072017.2993:selectThreadBack
	def selectThreadBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.threadBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-node:ekr.20031218072017.2993:selectThreadBack
	#@+node:ekr.20031218072017.2994:selectThreadNext
	def selectThreadNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.2994:selectThreadNext
	#@+node:ekr.20031218072017.2995:selectVisBack
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
	#@-node:ekr.20031218072017.2995:selectVisBack
	#@+node:ekr.20031218072017.2996:selectVisNext
	def selectVisNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.visNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-node:ekr.20031218072017.2996:selectVisNext
	#@+node:ekr.20031218072017.2997:selectVnode (calls tree.select)
	def selectVnode(self,p,updateBeadList=true):
		
		"""Select a new vnode."""
	
		# All updating and "synching" of nodes are now done in the event handlers!
		c = self
		c.frame.tree.endEditLabel()
		c.frame.tree.select(p,updateBeadList)
		c.frame.body.setFocus()
		self.editing = false
		
	selectPosition = selectVnode
	#@nonl
	#@-node:ekr.20031218072017.2997:selectVnode (calls tree.select)
	#@+node:ekr.20031218072017.2998:selectVnodeWithEditing
	# Selects the given node and enables editing of the headline if editFlag is true.
	
	def selectVnodeWithEditing(self,v,editFlag):
	
		c = self
		if editFlag:
			c.editPosition(v)
		else:
			c.selectVnode(v)
	
	selectPositionWithEditing = selectVnodeWithEditing
	#@nonl
	#@-node:ekr.20031218072017.2998:selectVnodeWithEditing
	#@-node:ekr.20031218072017.2990:Selecting & Updating (commands)
	#@+node:ekr.20031218072017.2999:Syntax coloring interface
	#@+at 
	#@nonl
	# These routines provide a convenient interface to the syntax colorer.
	#@-at
	#@+node:ekr.20031218072017.3000:updateSyntaxColorer
	def updateSyntaxColorer(self,v):
	
		self.frame.body.updateSyntaxColorer(v)
	#@-node:ekr.20031218072017.3000:updateSyntaxColorer
	#@-node:ekr.20031218072017.2999:Syntax coloring interface
	#@-others

class Commands (baseCommands):
	"""A class that implements most of Leo's commands."""
	pass
#@nonl
#@-node:ekr.20031218072017.2810:@thin leoCommands.py
#@-leo
