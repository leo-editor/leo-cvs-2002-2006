#@+leo
#@+node:0::@file leoFrame.py
#@+body
# To do: Use config params for window height, width and bar color, relief and width.


#@@language python

__pychecker__ = 'argumentsused=0' # Pychecker param.

from leoGlobals import *
import leoColor,leoCommands,leoCompare,leoDialog,leoFontPanel,leoNodes,leoPlugins,leoPrefs,leoTree
import os,string,sys,Tkinter,tkFileDialog,tkFont
import tempfile

Tk = Tkinter

class LeoFrame:

	#@+others
	#@+node:1::Birth & Death
	#@+node:1::frame.__init__
	#@+body
	def __init__(self, title = None):
	
		Tk = Tkinter
		
		#@<< set the LeoFrame ivars >>
		#@+node:1::<< set the LeoFrame ivars >>
		#@+body
		# Set title and fileName
		if title:
			self.mFileName = title
			title = self.setWindowTitle(title)
		else:
			title = "untitled"
			n = app().numberOfWindows
			if n > 0: title += `n`
			app().numberOfWindows = n+1
			self.mFileName = ""
			
		self.stylesheet = None # The contents of <?xml-stylesheet...?> line.
		
		# These are set the first time a panel is opened.
		# The panel remains open (perhaps hidden) until this frame is closed.
		self.colorPanel = None 
		self.fontPanel = None 
		self.prefsPanel = None
		self.comparePanel = None
			
		self.outlineToNowebDefaultFileName = "noweb.nw" # For Outline To Noweb dialog.
		self.title=title # Title of window, not including dirty mark
		self.saved=false # True if ever saved
		self.startupWindow=false # True if initially opened window
		self.openDirectory = ""
		self.es_newlines = 0 # newline count for this log stream
		
		self.splitVerticalFlag,self.ratio,self.secondary_ratio = self.initialRatios()
		
		# Created in createLeoFrame and its allies.
		self.commands = None
		self.tree = None
		self.f1 = self.f2 = None
		self.log = None  ; self.logBar = None
		self.body = None ; self.bodyBar = None
		self.canvas = None ; self.treeBar = None
		self.splitter1 = self.splitter2 = None
		self.icon = None
		self.outerFrame = None # 5/20/02
		self.iconFrame = None # 5/20/02
		self.statusFrame = None # 5/20/02
		self.statusText = None # 5/20/02
		self.statusLabel = None # 5/20/02
		
		self.menus = {} # Menu dictionary.
		self.menuShortcuts = None # List of menu shortcuts for warnings.
		
		# Used by event handlers...
		self.redrawCount = 0
		self.activeFrame = None
		self.draggedItem = None
		self.recentFiles = [] # List of recent files
		self.controlKeyIsDown = false # For control-drags
		
		# Colors of log pane.
		self.logColorTags = [] # list of color names used as tags in log window.
		self.statusColorTags = [] # list of color names used as tags in status window.
		
		# Previous row and column shown in the status area.
		self.lastStatusRow = self.lastStatusCol = 0
		self.tab_width = 0 # The tab width in effect in this pane.
		#@-body
		#@-node:1::<< set the LeoFrame ivars >>

		self.top = top = Tk.Toplevel()
		top.withdraw() # 7/15/02
		attachLeoIcon(top)
		# print top
		
		if sys.platform=="win32":
			self.hwnd = top.frame()
			# trace("__init__", "frame.__init__: self.hwnd:" + `self.hwnd`)
	
		top.title(title)
		top.minsize(30,10) # In grid units. This doesn't work as I expect.
		
		c = None # Make sure we don't mess with c yet.
		self.createLeoFrame(top)
		self.commands = c = leoCommands.Commands(self)
		self.tree = leoTree.leoTree(self.commands, self.canvas)
		c.tree = self.tree
		self.setTabWidth(c.tab_width)
		
		#@<< create the first tree node >>
		#@+node:2::<< create the first tree node >>
		#@+body
		t = leoNodes.tnode()
		v = leoNodes.vnode(c,t)
		v.initHeadString("NewHeadline")
		v.moveToRoot()
		
		c.beginUpdate()
		c.tree.redraw()
		c.tree.canvas.focus_get()
		c.editVnode(v)
		c.endUpdate(false)
		#@-body
		#@-node:2::<< create the first tree node >>

		v = c.currentVnode()
		if not doHook("menu1",c=c,v=v):
			self.createMenuBar(top)
		app().log = self # the LeoFrame containing the log
		app().windowList.append(self)
		# Sign on.
		color = app().config.getWindowPref("log_error_color")
		es("Leo Log Window...",color=color)
		es("Leo 4.0 alpha 2, ",newline=0)
		n1,n2,n3,junk,junk=sys.version_info
		ver1 = "Python %d.%d.%d" % (n1,n2,n3)
		ver2 = ", Tk " + self.top.getvar("tk_patchLevel")
		es(ver1 + ver2) ; enl()
		
		self.top.protocol("WM_DELETE_WINDOW", self.OnCloseLeoEvent)
		self.top.bind("<Button-1>", self.OnActivateLeoEvent)
		
		self.top.bind("<Activate>", self.OnActivateLeoEvent) # Doesn't work on windows.
		self.top.bind("<Deactivate>", self.OnDeactivateLeoEvent) # Doesn't work on windows.
	
		self.top.bind("<Control-KeyPress>",self.OnControlKeyDown)
		self.top.bind("<Control-KeyRelease>",self.OnControlKeyUp)
		
		self.tree.canvas.bind("<Button-1>", self.OnActivateTree)
		self.log.bind("<Button-1>", self.OnActivateLog)
		
		self.body.bind("<Button-1>", self.OnBodyClick) # 2/8/03
		self.body.bind("<Button-3>", self.OnBodyRClick) # 2/8/03
		self.body.bind("<Double-Button-1>", self.OnBodyDoubleClick)
		self.body.bind("<Key>", self.tree.OnBodyKey)
	
		self.body.bind(virtual_event_name("Cut"), self.OnCut)
		self.body.bind(virtual_event_name("Copy"), self.OnCopy)
		self.body.bind(virtual_event_name("Paste"), self.OnPaste)
		
		# Handle mouse wheel in the outline pane.
		if sys.platform == "linux2": # This crashes tcl83.dll
			self.tree.canvas.bind("<MouseWheel>", self.OnMouseWheel)
			
		# Remove the initially selected node from the list.
		c.beadPointer = -1
		c.beadList = []
		c.visitedList = []
		doHook("after-create-leo-frame",c=c)
	#@-body
	#@-node:1::frame.__init__
	#@+node:2::frame.__repr__
	#@+body
	def __repr__ (self):
	
		return "leoFrame: " + self.title
	
	#@-body
	#@-node:2::frame.__repr__
	#@+node:3::frame.destroy
	#@+body
	def destroy (self):
	
		# don't trace during shutdown logic.
		# print "frame.destroy:", self, self.top
		self.tree.destroy()
		self.tree = None
		self.commands.destroy()
		self.commands = None
		self.top.destroy() # Actually close the window.
		self.top = None
	#@-body
	#@-node:3::frame.destroy
	#@+node:4::frame.setWindowTitle
	#@+body
	def setWindowTitle (self,fileName):
		
		path,fn = os.path.split(fileName)
		if path and len(path) > 0:
			title = fn + " in " + path
		else:
			title = fn
		return title
	#@-body
	#@-node:4::frame.setWindowTitle
	#@+node:5::sectionList.createLeoFrame
	#@+body
	def createLeoFrame (self,top):
	
		Tk = Tkinter ; config = app().config
		
		self.outerFrame = outerFrame = Tk.Frame(top)
		self.outerFrame.pack(expand=1,fill="both")
	
		self.createIconBar()
		
		#@<< create both splitters >>
		#@+node:1::<< create both splitters >>
		#@+body
		# Splitter 1 is the main splitter containing splitter2 and the body pane.
		f1,bar1,split1Pane1,split1Pane2 = self.createLeoSplitter(outerFrame, self.splitVerticalFlag)
		self.f1,self.bar1 = f1,bar1
		self.split1Pane1,self.split1Pane2 = split1Pane1,split1Pane2
		# Splitter 2 is the secondary splitter containing the tree and log panes.
		f2,bar2,split2Pane1,split2Pane2 = self.createLeoSplitter(split1Pane1, not self.splitVerticalFlag)
		self.f2,self.bar2 = f2,bar2
		self.split2Pane1,self.split2Pane2 = split2Pane1,split2Pane2
		#@-body
		#@-node:1::<< create both splitters >>

		
		#@<< create the body pane >>
		#@+node:2::<< create the body pane >>
		#@+body
		# A light selectbackground value is needed to make syntax coloring look good.
		wrap = config.getBoolWindowPref('body_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		self.body = body = Tk.Text(split1Pane2,name='body',
			bd=2,bg="white",relief="flat",
			setgrid=1,wrap=wrap, selectbackground="Gray80")
		
		self.setBodyFontFromConfig()
		
		self.bodyBar = bodyBar = Tk.Scrollbar(split1Pane2,name='bodyBar')
		body['yscrollcommand'] = bodyBar.set
		bodyBar['command'] = body.yview
		bodyBar.pack(side="right", fill="y")
		
		if wrap == "none":
			bodyXBar = Tk.Scrollbar(
				split1Pane2,name='bodyXBar',orient="horizontal")
			body['xscrollcommand'] = bodyXBar.set
			bodyXBar['command'] = body.xview
			bodyXBar.pack(side="bottom", fill="x")
			
		body.pack(expand=1, fill="both")
		#@-body
		#@-node:2::<< create the body pane >>

		
		#@<< create the tree pane >>
		#@+node:3::<< create the tree pane >>
		#@+body
		scrolls = config.getBoolWindowPref('outline_pane_scrolls_horizontally')
		scrolls = choose(scrolls,1,0)
		
		self.canvas = tree = Tk.Canvas(split2Pane1,name="tree",
			bd=0,bg="white",relief="flat")
			
		self.setTreeColorsFromConfig()
		
		# The font is set in the tree code.
		
		# These do nothing...
		# selectborderwidth=0,selectforeground="white",selectbackground="white")
		self.treeBar = treeBar = Tk.Scrollbar(split2Pane1,name="treeBar")
		
		# Bind mouse wheel event to canvas
		if sys.platform != "win32": # Works on 98, crashes on XP.
			self.canvas.bind("<MouseWheel>", self.OnMouseWheel)
		
		tree['yscrollcommand'] = treeBar.set
		treeBar['command'] = tree.yview
		
		treeBar.pack(side="right", fill="y")
		if scrolls: 
			treeXBar = Tk.Scrollbar( 
				split2Pane1,name='treeXBar',orient="horizontal") 
			tree['xscrollcommand'] = treeXBar.set 
			treeXBar['command'] = tree.xview 
			treeXBar.pack(side="bottom", fill="x")
		tree.pack(expand=1,fill="both")
		#@-body
		#@-node:3::<< create the tree pane >>

		
		#@<< create the log pane >>
		#@+node:4::<< create the log pane >>
		#@+body
		wrap = config.getBoolWindowPref('log_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		self.log = log = Tk.Text(split2Pane2,name="log",
			setgrid=1,wrap=wrap,bd=2,bg="white",relief="flat")
			
		self.setLogFontFromConfig()
		
		self.logBar = logBar = Tk.Scrollbar(split2Pane2,name="logBar")
		
		log['yscrollcommand'] = logBar.set
		logBar['command'] = log.yview
		
		logBar.pack(side="right", fill="y")
		# rr 8/14/02 added horizontal elevator 
		if wrap == "none": 
			logXBar = Tk.Scrollbar( 
				split2Pane2,name='logXBar',orient="horizontal") 
			log['xscrollcommand'] = logXBar.set 
			logXBar['command'] = log.xview 
			logXBar.pack(side="bottom", fill="x")
		log.pack(expand=1, fill="both")
		#@-body
		#@-node:4::<< create the log pane >>

		self.reconfigurePanes()
		
		self.createStatusLine()
		self.putStatusLine("Welcome to Leo")
	
	#@-body
	#@-node:5::sectionList.createLeoFrame
	#@-node:1::Birth & Death
	#@+node:2::Configuration
	#@+node:1::f.configureBar
	#@+body
	def configureBar (self, bar, verticalFlag):
		
		config = app().config
	
		# Get configuration settings.
		w = config.getWindowPref("split_bar_width")
		if not w or w < 1: w = 7
		relief = config.getWindowPref("split_bar_relief")
		if not relief: relief = "flat"
		color = config.getWindowPref("split_bar_color")
		if not color: color = "LightSteelBlue2"
	
		try:
			if verticalFlag:
				# Panes arranged vertically; horizontal splitter bar
				bar.configure(relief=relief,height=w,bg=color,cursor="sb_v_double_arrow")
			else:
				# Panes arranged horizontally; vertical splitter bar
				bar.configure(relief=relief,width=w,bg=color,cursor="sb_h_double_arrow")
		except: # Could be a user error. Use all defaults
			es("exception in user configuration for splitbar")
			es_exception()
			if verticalFlag:
				# Panes arranged vertically; horizontal splitter bar
				bar.configure(height=7,cursor="sb_v_double_arrow")
			else:
				# Panes arranged horizontally; vertical splitter bar
				bar.configure(width=7,cursor="sb_h_double_arrow")
	#@-body
	#@-node:1::f.configureBar
	#@+node:2::f.configureBarsFromConfig
	#@+body
	def configureBarsFromConfig (self):
		
		config = app().config
	
		w = config.getWindowPref("split_bar_width")
		if not w or w < 1: w = 7
		
		relief = config.getWindowPref("split_bar_relief")
		if not relief or relief == "": relief = "flat"
	
		color = config.getWindowPref("split_bar_color")
		if not color or color == "": color = "LightSteelBlue2"
	
		if self.splitVerticalFlag:
			bar1,bar2=self.bar1,self.bar2
		else:
			bar1,bar2=self.bar2,self.bar1
			
		try:
			bar1.configure(relief=relief,height=w,bg=color)
			bar2.configure(relief=relief,width=w,bg=color)
		except: # Could be a user error.
			es("exception in user configuration for splitbar")
			es_exception()
	#@-body
	#@-node:2::f.configureBarsFromConfig
	#@+node:3::f.reconfigureFromConfig
	#@+body
	def reconfigureFromConfig (self):
		
		f = self ; c = f.commands
		
		# Not ready yet: just reset the width and color.
		# We need self.bar1 and self.bar2 ivars.
		# self.reconfigureBar(...)
		
		# The calls to redraw are workarounds for an apparent Tk bug.
		# Without them the text settings get applied to the wrong widget!
		# Moreover, only this order seems to work on Windows XP...
		f.tree.setFontFromConfig()
		f.setTreeColorsFromConfig()
		f.configureBarsFromConfig()
		c.redraw()
		f.setBodyFontFromConfig()
		f.setTabWidth(c.tab_width)
		c.redraw()
		f.setLogFontFromConfig()
		c.redraw()
	#@-body
	#@-node:3::f.reconfigureFromConfig
	#@+node:4::f.setBodyFontFromConfig
	#@+body
	def setBodyFontFromConfig (self):
		
		config = app().config ; body = self.body
		#print "body",self.body
		
		font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight")
	
		body.configure(font=font)
		
		bg = config.getWindowPref("body_text_background_color")
		if bg:
			try: body.configure(bg=bg)
			except: pass
		
		fg = config.getWindowPref("body_text_foreground_color")
		if fg:
			try: body.configure(fg=fg)
			except: pass
			
		# 1/24/03: Gareth McCaughan
		bg = config.getWindowPref("body_insertion_cursor_color")
		if bg:
			try: body.configure(insertbackground=bg)
			except: pass
			
		if sys.platform != "win32": # Maybe a Windows bug.
			fg = config.getWindowPref("body_cursor_foreground_color")
			bg = config.getWindowPref("body_cursor_background_color")
			# print fg, bg
			if fg and bg:
				cursor="xterm" + " " + fg + " " + bg
				try: body.configure(cursor=cursor)
				except:
					import traceback
					traceback.print_exc()
	#@-body
	#@-node:4::f.setBodyFontFromConfig
	#@+node:5::f.setLogFontFromConfig
	#@+body
	def setLogFontFromConfig (self):
	
		log = self.log ; config = app().config
		#print "log",self.log
	
		font = config.getFontFromParams(
			"log_text_font_family", "log_text_font_size",
			"log_text_font_slant",  "log_text_font_weight")
		
		log.configure(font=font)
		
		bg = config.getWindowPref("log_text_background_color")
		if bg:
			try: log.configure(bg=bg)
			except: pass
		
		fg = config.getWindowPref("log_text_foreground_color")
		if fg:
			try: log.configure(fg=fg)
			except: pass
	
	#@-body
	#@-node:5::f.setLogFontFromConfig
	#@+node:6::f.setTabWidth
	#@+body
	def setTabWidth (self, w):
		
		try: # This can fail when called from scripts
			# Use the present font for computations.
			font = self.body.cget("font")
			root = app().root # 4/3/03: must specify root so idle window will work properly.
			font = tkFont.Font(root=root,font=font)
			tabw = font.measure(" " * abs(w)) # 7/2/02
			# tablist = `tabw` + ' ' + `2*tabw`
			self.body.configure(tabs=tabw)
			self.tab_width = w
			# print "frame.setTabWidth:" + `w` + "," + `tabw`
		except:
			es_exception()
			pass
	
	#@-body
	#@-node:6::f.setTabWidth
	#@+node:7::f.setTreeColorsFromConfig
	#@+body
	def setTreeColorsFromConfig (self):
		
		config = app().config ; tree = self.tree
	
		bg = config.getWindowPref("outline_pane_background_color")
		if bg:
			try: self.canvas.configure(bg=bg)
			except: pass
	
	#@-body
	#@-node:7::f.setTreeColorsFromConfig
	#@+node:8::reconfigurePanes (use config bar_width)
	#@+body
	def reconfigurePanes (self):
		
		border = app().config.getIntWindowPref('additional_body_text_border')
		if border == None: border = 0
		
		# The body pane needs a _much_ bigger border when tiling horizontally.
		border = choose(self.splitVerticalFlag,2+border,6+border)
		self.body.configure(bd=border)
		
		# The log pane needs a slightly bigger border when tiling vertically.
		border = choose(self.splitVerticalFlag,4,2) 
		self.log.configure(bd=border)
	#@-body
	#@-node:8::reconfigurePanes (use config bar_width)
	#@-node:2::Configuration
	#@+node:3::Event handlers (Frame)
	#@+node:1::frame.OnCloseLeoEvent
	#@+body
	# Called from quit logic and when user closes the window.
	# Returns true if the close happened.
	
	def OnCloseLeoEvent(self):
	
		try:
			
			#@<< handle request to close a leo window >>
			#@+node:1::<< handle request to close a leo window >>
			#@+body
			# trace(`self in app().windowList` + ":" + `self`)
			veto=false
			c = self.commands ; frame = c.frame
			if c.changed:
				
				#@<< Prompt for change.  Set veto if the user cancels >>
				#@+node:1::<< Prompt for change.  Set veto if the user cancels >>
				#@+body
				name = choose(self.mFileName, self.mFileName, self.title)
				type = choose(app().quitting, "quitting?", "closing?")
				
				d = leoDialog.leoDialog()
				answer = d.askYesNoCancel("Confirm",
					'Save changes to "' + name + '" before ' + type)
				
				if answer=="yes":
					if not self.mFileName or self.mFileName == "":
						
						#@<< Put up a file save dialog; set veto if the user cancels >>
						#@+node:1::<< Put up a file save dialog; set veto if the user cancels >>
						#@+body
						# Make sure we never pass None to the ctor.
						if not self.title:
							self.title = ""
							
						self.mFileName = tkFileDialog.asksaveasfilename(
							initialfile = self.mFileName,
							title="Save",
							filetypes=[("Leo files", "*.leo")],
							defaultextension=".leo")
							
						if not self.mFileName:
							veto = true
						
						#@-body
						#@-node:1::<< Put up a file save dialog; set veto if the user cancels >>

					if veto==false and self.mFileName and self.mFileName != "":
						self.commands.fileCommands.save( self.mFileName )
				
				elif answer=="cancel":
					veto = true #The user wants to cancel the close.
				
				else: veto = false # The user wants to close without saving.
				#@-body
				#@-node:1::<< Prompt for change.  Set veto if the user cancels >>

			if veto: return false
			app().log = None # no log until we reactive a window.
			# Destroy all windows attached to this windows.
			# This code will be executed if we haven't explicitly closed the windows.
			if self.comparePanel:
				self.comparePanel.top.destroy()
			if self.colorPanel:
				self.colorPanel.top.destroy()
			if self.fontPanel:
				self.fontPanel.top.destroy()
			if self.prefsPanel:
				self.prefsPanel.top.destroy()
				
			doHook("close-frame",c=c)
			
			if self in app().windowList:
				app().windowList.remove(self)
				self.destroy() # force the window to go away now.
			if app().windowList:
				# Pick a window to activate so we can set the log.
				w = app().windowList[0]
				w.top.deiconify()
				w.top.lift()
				app().log = w
			else:
				app().quit()
			
			#@-body
			#@-node:1::<< handle request to close a leo window >>

			return true
		except:
			es_event_exception("close window")
			return false
	
	#@-body
	#@-node:1::frame.OnCloseLeoEvent
	#@+node:2::frame.OnControlKeyUp/Down
	#@+body
	def OnControlKeyDown (self,event=None):
		
		self.controlKeyIsDown = true
		
	def OnControlKeyUp (self,event=None):
	
		self.controlKeyIsDown = false
	
	#@-body
	#@-node:2::frame.OnControlKeyUp/Down
	#@+node:3::frame.OnVisibility
	#@+body
	# Handle the "visibility" event and attempt to attach the Leo icon.
	# This code must be executed whenever the window is redrawn.
	
	def OnVisibility (self,event):
	
		if self.icon and event.widget is self.top:
	
			# print "OnVisibility"
			self.icon.attach(self.top)
	#@-body
	#@-node:3::frame.OnVisibility
	#@+node:4::OnActivateBody
	#@+body
	def OnActivateBody (self,event=None):
	
		try:
			c = self.commands ; v = c.currentVnode()
			app().log = self
			self.tree.OnDeactivate()
			# trace(`app().log`)
		except:
			es_event_exception("activate body")
	
	
	#@-body
	#@-node:4::OnActivateBody
	#@+node:5::OnActivateLeoEvent, OnDeactivateLeoEvent
	#@+body
	def OnActivateLeoEvent(self,event=None):
	
		try:
			app().log = self
			# trace(`app().log`)
		except:
			es_event_exception("activate Leo")
	
	def OnDeactivateLeoEvent(self,event=None):
	
		try:
			app().log = None
			# trace(`app().log`)
		except:
			es_event_exception("deactivate Leo")
	#@-body
	#@-node:5::OnActivateLeoEvent, OnDeactivateLeoEvent
	#@+node:6::OnActivateLog
	#@+body
	def OnActivateLog (self,event=None):
	
		try:
			app().log = self
			self.tree.OnDeactivate()
			# trace(`app().log`)
		except:
			es_event_exception("activate log")
	#@-body
	#@-node:6::OnActivateLog
	#@+node:7::OnActivateTree
	#@+body
	def OnActivateTree (self,event=None):
	
		try:
			app().log = self
			self.tree.undimEditLabel()
			self.tree.canvas.focus_set()
			# trace(`app().log`)
		except:
			es_event_exception("activate tree")
	
	#@-body
	#@-node:7::OnActivateTree
	#@+node:8::OnBodyClick, OnBodyRClick (Events)
	#@+body
	def OnBodyClick (self,event=None):
	
		try:
			c = self.commands ; v = c.currentVnode()
			if not doHook("bodyclick1",c=c,v=v,event=event):
				self.OnActivateBody(event=event)
			doHook("bodyclick2",c=c,v=v,event=event)
		except:
			es_event_exception("bodyclick")
	
	def OnBodyRClick(self,event=None):
		
		try:
			c = self.commands ; v = c.currentVnode()
			if not doHook("bodyrclick1",c=c,v=v,event=event):
				pass # By default Leo does nothing.
			doHook("bodyrclick2",c=c,v=v,event=event)
		except:
			es_event_exception("iconrclick")
	#@-body
	#@-node:8::OnBodyClick, OnBodyRClick (Events)
	#@+node:9::OnBodyDoubleClick (Events)
	#@+body
	def OnBodyDoubleClick (self,event=None):
	
		try:
			c = self.commands ; v = c.currentVnode()
			if not doHook("bodydclick1",c=c,v=v,event=event):
				if event: # 8/4/02: prevent wandering insertion point.
					index = "@%d,%d" % (event.x, event.y) # Find where we clicked
				body = self.body
				start = body.index(index + " wordstart")
				end = body.index(index + " wordend")
				setTextSelection(self.body,start,end)
			doHook("bodydclick1",c=c,v=v,event=event)
		except:
			es_event_exception("bodydclick")
	
		return "break" # Inhibit all further event processing.
	#@-body
	#@-node:9::OnBodyDoubleClick (Events)
	#@+node:10::OnMouseWheel (Tomaz Ficko)
	#@+body
	# Contributed by Tomaz Ficko.  This works on some systems.
	# On XP it causes a crash in tcl83.dll.  Clearly a Tk bug.
	
	def OnMouseWheel(self, event=None):
	
		try:
			if event.delta < 1:
				self.canvas.yview(Tkinter.SCROLL, 1, Tkinter.UNITS)
			else:
				self.canvas.yview(Tkinter.SCROLL, -1, Tkinter.UNITS)
		except:
			es_event_exception("scroll wheel")
	
		return "break"
	#@-body
	#@-node:10::OnMouseWheel (Tomaz Ficko)
	#@-node:3::Event handlers (Frame)
	#@+node:4::Icon area: convenience routines
	#@+node:1::createIconBar
	#@+body
	def createIconBar (self):
		
		"""Create an empty icon bar in the packer's present position"""
	
		if not self.iconFrame:
			self.iconFrame = Tk.Frame(self.outerFrame,height="5m",bd=2,relief="groove")
			self.iconFrame.pack(fill="x",pady=2)
	#@-body
	#@-node:1::createIconBar
	#@+node:2::hideIconBar
	#@+body
	def hideIconBar (self):
		
		"""Hide the icon bar by unpacking it.
		
		A later call to showIconBar will repack it in a new location."""
		
		if self.iconFrame:
			self.iconFrame.pack_forget()
	
	#@-body
	#@-node:2::hideIconBar
	#@+node:3::clearIconBar
	#@+body
	def clearIconBar(self):
		
		"""Destroy all the widgets in the icon bar"""
		
		a = app() ; f = self.iconFrame
		if not f: return
		
		for slave in f.pack_slaves():
			slave.destroy()
	
		f.configure(height="5m") # The default height.
		a.iconWidgetCount = 0
		a. iconImageRefs = []
	
	#@-body
	#@-node:3::clearIconBar
	#@+node:4::showIconBar
	#@+body
	def showIconBar(self):
		
		"""Show the icon bar by repacking it"""
	
		self.iconFrame.pack(fill="x",pady=2)
	#@-body
	#@-node:4::showIconBar
	#@+node:5::addIconButton
	#@+body
	def addIconButton(self,text=None,imagefile=None,image=None,command=None,bg=None):
		
		"""Add a button containing text or a picture to the icon bar.
		
		Pictures take precedence over text"""
		
		a = app() ; f = self.iconFrame
		if not imagefile and not image and not text: return
	
		# First define n.	
		try:
			a.iconWidgetCount += 1
			n = a.iconWidgetCount
		except:
			n = a.iconWidgetCount = 1
	
		if not command:
			def command(n=n):
				print "command for widget %s" % (n)
	
		if imagefile or image:
			
			#@<< create a picture >>
			#@+node:1::<< create a picture >>
			#@+body
			try:
				if imagefile:
					# Create the image.  Throws an exception if file not found
					imagefile = os.path.join(app().loadDir,imagefile)
					imagefile = os.path.normpath(imagefile)
					image = Tkinter.PhotoImage(master=app().root,file=imagefile)
					
					# Must keep a reference to the image!
					try:
						refs = a.iconImageRefs
					except:
						refs = a.iconImageRefs = []
				
					refs.append((imagefile,image),)
				
				if not bg:
					bg = f.cget("bg")
			
				b = Tk.Button(f,image=image,relief="raised",command=command,bg=bg)
				b.pack(side="left",fill="y")
				return b
				
			except:
				es_exception()
				return None
			#@-body
			#@-node:1::<< create a picture >>

		elif text:
			b = Tk.Button(f,text=text,relief="raised",command=command)
			b.pack(side="left", fill="y")
			return b
			
		return None
	#@-body
	#@-node:5::addIconButton
	#@-node:4::Icon area: convenience routines
	#@+node:5::frame.longFileName & shortFileName
	#@+body
	def longFileName (self):
		return self.mFileName
		
	def shortFileName (self):
		return shortFileName(self.mFileName)
	#@-body
	#@-node:5::frame.longFileName & shortFileName
	#@+node:6::frame.put, putnl
	#@+body
	# All output to the log stream eventually comes here.
	
	def put (self,s,color=None):
		# print `app().quitting`,`self.log`
		if app().quitting > 0: return
		if self.log:
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,app().tkEncoding)
			if color:
				if color not in self.logColorTags:
					self.logColorTags.append(color)
					self.log.tag_config(color,foreground=color)
				self.log.insert("end",s)
				self.log.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
				if "black" not in self.logColorTags:
					self.logColorTags.append("black")
					self.log.tag_config("black",foreground="black")
				self.log.tag_add("black","end")
			else:
				self.log.insert("end",s)
			self.log.see("end")
			self.log.update_idletasks()
		else:
			app().logWaiting.append((s,color),) # 2/25/03
			print "Null log"
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,"ascii")
			print s
	
	def putnl (self):
		if app().quitting > 0: return
		if self.log:
			self.log.insert("end",'\n')
			self.log.see("end")
			self.log.update_idletasks()
		else:
			a.logWaiting.append(('\n',"black"),) # 2/16/03
			print "Null log"
			print
	#@-body
	#@-node:6::frame.put, putnl
	#@+node:7::getFocus
	#@+body
	# Returns the frame that has focus, or body if None.
	
	def getFocus(self):
	
		f = self.top.focus_displayof()
		if f:
			return f
		else:
			return self.body
	#@-body
	#@-node:7::getFocus
	#@+node:8::Menus
	#@+node:1::canonicalizeShortcut
	#@+body
	#@+at
	#  This code "canonicalizes" both the shortcuts that appear in menus and 
	# the arguments to bind, mostly ignoring case and the order in which 
	# special keys are specified in leoConfig.txt.
	# 
	# For example, Ctrl+Shift+a is the same as Shift+Control+A.  Either may 
	# appear in leoConfig.txt.  Each generates Shift+Ctrl-A in the menu and 
	# Control+A as the argument to bind.
	# 
	# Returns (bind_shortcut, menu_shortcut)

	#@-at
	#@@c

	def canonicalizeShortcut (self,shortcut):
		
		if shortcut == None or len(shortcut) == 0:
			return None,None
		s = shortcut.strip().lower()
		has_alt   = s.find("alt") >= 0
		has_ctrl  = s.find("control") >= 0 or s.find("ctrl") >= 0
		has_shift = s.find("shift") >= 0   or s.find("shft") >= 0
		
		#@<< set the last field, preserving case >>
		#@+node:2::<< set the last field, preserving case >>
		#@+body
		s2 = shortcut
		s2 = string.strip(s2)
		
		# Replace all minus signs by plus signs, except a trailing minus:
		if len(s2) > 0 and s2[-1] == "-":
			s2 = string.replace(s2,"-","+")
			s2 = s2[:-1] + "-"
		else:
			s2 = string.replace(s2,"-","+")
		
		fields = string.split(s2,"+")
		if fields == None or len(fields) == 0:
			if not app().menuWarningsGiven:
				print "bad shortcut specifier:", s
			return None,None
		
		last = fields[-1]
		if last == None or len(last) == 0:
			if not app().menuWarningsGiven:
				print "bad shortcut specifier:", s
			return None,None
		#@-body
		#@-node:2::<< set the last field, preserving case >>

		
		#@<< canonicalize the last field >>
		#@+node:1::<< canonicalize the last field >>
		#@+body
		bind_last = menu_last = last
		if len(last) == 1:
			ch = last[0]
			if ch in string.letters:
				menu_last = string.upper(last)
				if has_shift:
					bind_last = string.upper(last)
				else:
					bind_last = string.lower(last)
			elif ch in string.digits:
				bind_last = "Key-" + ch # 1-5 refer to mouse buttons, not keys.
			else:
				
				#@<< define dict of Tk bind names >>
				#@+node:1::<< define dict of Tk bind names >>
				#@+body
				# These are defined at http://tcl.activestate.com/man/tcl8.4/TkCmd/keysyms.htm.
				dict = {
					"!" : "exclam",
					'"' : "quotedbl",
					"#" : "numbersign",
					"$" : "dollar",
					"%" : "percent",
					"&" : "ampersand",
					"'" : "quoteright",
					"(" : "parenleft",
					")" : "parenright",
					"*" : "asterisk",
					"+" : "plus",
					"," : "comma",
					"-" : "minus",
					"." : "period",
					"/" : "slash",
					":" : "colon",
					";" : "semicolon",
					"<" : "less",
					"=" : "equal",
					">" : "greater",
					"?" : "question",
					"@" : "at",
					"[" : "bracketleft",
					"\\": "backslash",
					"]" : "bracketright",
					"^" : "asciicircum",
					"_" : "underscore",
					"`" : "quoteleft",
					"{" : "braceleft",
					"|" : "bar",
					"}" : "braceright",
					"~" : "asciitilde" }
				#@-body
				#@-node:1::<< define dict of Tk bind names >>

				if ch in dict.keys():
					bind_last = dict[ch]
		elif len(last) > 0:
			
			#@<< define dict of special names >>
			#@+node:2::<< define dict of special names >>
			#@+body
			# These keys are simply made-up names.  The menu_bind values are known to Tk.
			# Case is not significant in the keys.
			
			dict = {
				"bksp"    : ("BackSpace","BkSp"),
				"esc"     : ("Escape","Esc"),
				# Arrow keys...
				"dnarrow" : ("Down", "DnArrow"),
				"ltarrow" : ("Left", "LtArrow"),
				"rtarrow" : ("Right","RtArrow"),
				"uparrow" : ("Up",   "UpArrow"),
				# Page up/down keys...
				"pageup"  : ("Prior","PgUp"),
				"pagedn"  : ("Next", "PgDn")
			}
			

			#@+at
			#   The following are not translated, so what appears in the menu 
			# is the same as what is passed to Tk.  Case is significant.
			# 
			# Note: the Tk documentation states that not all of these may be 
			# available on all platforms.
			# 
			# F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,
			# BackSpace, Break, Clear, Delete, Escape, Linefeed, Return, Tab,
			# Down, Left, Right, Up,
			# Begin, End, Home, Next, Prior,
			# Num_Lock, Pause, Scroll_Lock, Sys_Req,
			# KP_Add, KP_Decimal, KP_Divide, KP_Enter, KP_Equal,
			# KP_Multiply, KP_Separator,KP_Space, KP_Subtract, KP_Tab,
			# KP_F1,KP_F2,KP_F3,KP_F4,
			# KP_0,KP_1,KP_2,KP_3,KP_4,KP_5,KP_6,KP_7,KP_8,KP_9

			#@-at
			#@-body
			#@-node:2::<< define dict of special names >>

			last2 = string.lower(last)
			if last2 in dict.keys():
				bind_last,menu_last = dict[last2]
		#@-body
		#@-node:1::<< canonicalize the last field >>

		
		#@<< synthesize the shortcuts from the information >>
		#@+node:3::<< synthesize the shortcuts from the information >>
		#@+body
		bind_head = menu_head = ""
		
		if has_shift:
			menu_head = "Shift+"
			if len(last) > 1 or (len(last)==1 and last[0] not in string.letters):
				bind_head = "Shift-"
			# else: print "no shift: last:", `last`
		
		if has_alt:
			bind_head = bind_head + "Alt-"
			menu_head = menu_head + "Alt+"
		
		if has_ctrl:
			bind_head = bind_head + "Control-"
			menu_head = menu_head + "Ctrl+"
			
		bind_shortcut = "<" + bind_head + bind_last + ">"
		menu_shortcut = menu_head + menu_last
		#@-body
		#@-node:3::<< synthesize the shortcuts from the information >>

		# print shortcut,bind_shortcut,menu_shortcut
		return bind_shortcut,menu_shortcut
	#@-body
	#@-node:1::canonicalizeShortcut
	#@+node:2::createMenuBar
	#@+body
	def createMenuBar(self, top):
	
		c = self.commands
		Tk = Tkinter
		topMenu = Tk.Menu(top,postcommand=self.OnMenuClick)
		self.setMenu("top",topMenu)
		self.menuShortcuts = []
		# To do: use Meta rathter than Control for accelerators for Unix
		
		#@<< create the file menu >>
		#@+node:2::<< create the file menu >>
		#@+body
		fileMenu = self.createNewMenu("&File")
		
		#@<< create the top-level file entries >>
		#@+node:1::<< create the top-level file entries >>
		#@+body
		#@+at
		#  It is doubtful that leo.py will ever support a Print command 
		# directly.  Rather, users can use export commands to create text 
		# files that may then be formatted and printed as desired.

		#@-at
		#@@c

		table = (
			("&New","Ctrl+N",self.OnNew),
			("&Open...","Ctrl+O",self.OnOpen),
			("Open &With...","Shift+Ctrl+O",self.OnOpenWith),
			("-",None,None),
			("&Close","Ctrl+W",self.OnClose),
			("&Save","Ctrl+S",self.OnSave),
			("Save &As","Shift+Ctrl+S",self.OnSaveAs),
			("Save To",None,self.OnSaveTo), # &Tangle
			("Re&vert To Saved",None,self.OnRevert)) # &Read/Write
				
		self.createMenuEntries(fileMenu,table)
		
		
		#@-body
		#@-node:1::<< create the top-level file entries >>

		
		#@<< create the recent files submenu >>
		#@+node:2::<< create the recent files submenu >>
		#@+body
		recentFilesMenu = self.createNewMenu("Recent &Files...","File")
		self.recentFiles = app().config.getRecentFiles()
		self.createRecentFilesMenuItems()
		
		
		#@-body
		#@-node:2::<< create the recent files submenu >>

		fileMenu.add_separator()
		
		#@<< create the read/write submenu >>
		#@+node:3::<< create the read/write submenu >>
		#@+body
		readWriteMenu = self.createNewMenu("&Read/Write...","File")
		
		table = [
				("&Read Outline Only","Shift+Ctrl+R",self.OnReadOutlineOnly),
				("Read @file &Nodes",None,self.OnReadAtFileNodes),
				("-",None,None),
				("Write &Dirty @file Nodes","Shift+Ctrl+Q",self.OnWriteDirtyAtFileNodes),
				("Write &Missing @file Nodes",None,self.OnWriteMissingAtFileNodes),
				("Write &Outline Only",None,self.OnWriteOutlineOnly),
				("&Write @file Nodes","Shift+Ctrl+W",self.OnWriteAtFileNodes)]
		
		if app().use_gnx: # Testing.
			table2 = (
				("-",None,None),
				("Read 4.0 Derived File",None,self.OnReadGnxFile),
				("Write 4.0 Derived File",None,self.OnWriteGnxFile),
				("Clear All Node Indices",None,self.OnClearAllNodeIndices))
			table.extend(table2)
		
		self.createMenuEntries(readWriteMenu,table)
		#@-body
		#@-node:3::<< create the read/write submenu >>

		
		#@<< create the tangle submenu >>
		#@+node:4::<< create the tangle submenu >>
		#@+body
		tangleMenu = self.createNewMenu("&Tangle...","File")
		
		table = (
			("Tangle &All","Shift+Ctrl+A",self.OnTangleAll),
			("Tangle &Marked","Shift+Ctrl+M",self.OnTangleMarked),
			("&Tangle","Shift+Ctrl+T",self.OnTangle))
		
		self.createMenuEntries(tangleMenu,table)
		
		
		#@-body
		#@-node:4::<< create the tangle submenu >>

		
		#@<< create the untangle submenu >>
		#@+node:5::<< create the untangle submenu >>
		#@+body
		untangleMenu = self.createNewMenu("&Untangle...","File")
		
		table = (
			("Untangle &All",None,self.OnUntangleAll),
			("Untangle &Marked",None,self.OnUntangleMarked),
			("&Untangle","Shift+Ctrl+U",self.OnUntangle))
			
		self.createMenuEntries(untangleMenu,table)
		
		
		#@-body
		#@-node:5::<< create the untangle submenu >>

		
		#@<< create the import submenu >>
		#@+node:6::<< create the import submenu >>
		#@+body
		importMenu = self.createNewMenu("&Import...","File")
		
		table = (
			("Import To @&file","Shift+Ctrl+F",self.OnImportAtFile),
			("Import To @&root",None,self.OnImportAtRoot),
			("Import &CWEB Files",None,self.OnImportCWEBFiles),
			("Import &noweb Files",None,self.OnImportNowebFiles),
			("Import Flattened &Outline",None,self.OnImportFlattenedOutline))
		
		self.createMenuEntries(importMenu,table)
		
		
		#@-body
		#@-node:6::<< create the import submenu >>

		
		#@<< create the export submenu >>
		#@+node:7::<< create the export submenu >>
		#@+body
		exportMenu = self.createNewMenu("&Export...","File")
		
		table = [
			("Export &Headlines",None,self.OnExportHeadlines),
			("Outline To &CWEB",None,self.OnOutlineToCWEB),
			("Outline To &Noweb",None,self.OnOutlineToNoweb),
			("&Flatten Outline",None,self.OnFlattenOutline),
			("&Remove Sentinels",None,self.OnRemoveSentinels),
			("&Weave",None,self.OnWeave)]
			
		if app().use_gnx:
			table2 = (
				("Write Old Format Outline",None,self.OnWriteOldOutline),)
			table.extend(table2)
		
		self.createMenuEntries(exportMenu,table)
		
		#@-body
		#@-node:7::<< create the export submenu >>

		fileMenu.add_separator()
		# Create the last entries.
		exitTable = (("E&xit","Ctrl-Q",self.OnQuit),)
		self.createMenuEntries(fileMenu,exitTable)
		
		
		#@-body
		#@-node:2::<< create the file menu >>

		
		#@<< create the edit menu >>
		#@+node:1::<< create the edit menu >>
		#@+body
		editMenu = self.createNewMenu("&Edit")
		
		#@<< create the first top-level edit entries >>
		#@+node:1::<< create the first top-level edit entries >>
		#@+body
		table = (
			("Can't Undo","Ctrl+Z",self.OnUndo), # &U reserved for Undo
			("Can't Redo","Shift+Ctrl+Z",self.OnRedo), # &R reserved for Redo
			("-",None,None),
			("Cu&t","Ctrl+X",self.OnCutFromMenu), 
			("Cop&y","Ctrl+C",self.OnCopyFromMenu),
			("&Paste","Ctrl+V",self.OnPasteFromMenu),
			("&Delete",None,self.OnDelete),
			("Select &All","Ctrl+A",self.OnSelectAll),
			("-",None,None))
		
		self.createMenuEntries(editMenu,table)
		
		#@-body
		#@-node:1::<< create the first top-level edit entries >>

		
		#@<< create the edit body submenu >>
		#@+node:2::<< create the edit body submenu >>
		#@+body
		editBodyMenu = self.createNewMenu("Edit &Body...","Edit")
		
		table = (
			("Extract &Section","Shift+Ctrl+E",self.OnExtractSection),
			("Extract &Names","Shift+Ctrl+N",self.OnExtractNames),
			("&Extract","Shift+Ctrl+D",self.OnExtract),
			("-",None,None),
			("Convert All B&lanks",None,self.OnConvertAllBlanks),
			("Convert All T&abs",None,self.OnConvertAllTabs),
			("Convert &Blanks","Shift+Ctrl+B",self.OnConvertBlanks),
			("Convert &Tabs","Shift+Ctrl+J",self.OnConvertTabs),
			("Insert Body Time/&Date","Shift+Ctrl+G",self.OnInsertBodyTime),
			("&Reformat Paragraph","Shift+Ctrl+P",self.OnReformatParagraph),
			("-",None,None),
			("&Indent","Ctrl+]",self.OnIndent),
			("&Unindent","Ctrl+[",self.OnDedent),
			("&Match Brackets","Ctrl+K",self.OnFindMatchingBracket))
			
		self.createMenuEntries(editBodyMenu,table)
		
		
		#@-body
		#@-node:2::<< create the edit body submenu >>

		
		#@<< create the edit headline submenu >>
		#@+node:3::<< create the edit headline submenu >>
		#@+body
		editHeadlineMenu = self.createNewMenu("Edit &Headline...","Edit")
		
		table = (
			("Edit &Headline","Ctrl+H",self.OnEditHeadline),
			("&End Edit Headline","Escape",self.OnEndEditHeadline),
			("&Abort Edit Headline","Shift-Escape",self.OnAbortEditHeadline),
			("Insert Headline Time/&Date","Shift+Ctrl+H",self.OnInsertHeadlineTime))
			
			# 5/16/03 EKR: I dislike this command.
			#("Toggle Angle Brackets","Ctrl+B",self.OnToggleAngleBrackets)
			
		self.createMenuEntries(editHeadlineMenu,table)
		
		
		#@-body
		#@-node:3::<< create the edit headline submenu >>

		
		#@<< create the find submenu >>
		#@+node:4::<< create the find submenu >>
		#@+body
		findMenu = self.createNewMenu("&Find...","Edit")
		
		table = (
			("&Find Panel","Ctrl+F",self.OnFindPanel),
			("-",None,None),
			("Find &Next","F3",self.OnFindNext),
			("Find &Previous","F4",self.OnFindPrevious),
			("&Replace","Ctrl+=",self.OnReplace),
			("Replace, &Then Find","Ctrl+-",self.OnReplaceThenFind))
		
		self.createMenuEntries(findMenu,table)
		
		#@-body
		#@-node:4::<< create the find submenu >>

		
		#@<< create the last top-level edit entries >>
		#@+node:5::<< create the last top-level edit entries >>
		#@+body
		label = choose(c.tree.colorizer.showInvisibles,"Hide In&visibles","Show In&visibles")
		
		table = (
			("&Go To Line Number","Alt+G",self.OnGoToLineNumber),
			("&Execute Script","Alt+Shift+E",self.OnExecuteScript),
			("Set Fon&t...","Shift+Alt+T",self.OnFontPanel),
			("Set &Colors...","Shift+Alt+C",self.OnColorPanel),
			(label,"Alt+V",self.OnViewAllCharacters),
			("-",None,None),
			("Prefere&nces","Ctrl+Y",self.OnPreferences))
		
		self.createMenuEntries(editMenu,table)
		#@-body
		#@-node:5::<< create the last top-level edit entries >>

		
		#@-body
		#@-node:1::<< create the edit menu >>

		
		#@<< create the outline menu >>
		#@+node:3::<< create the outline menu >>
		#@+body
		outlineMenu = self.createNewMenu("&Outline")
		
		#@<< create top-level outline menu >>
		#@+node:1::<< create top-level outline menu >>
		#@+body
		table = (
			("C&ut Node","Shift+Ctrl+X",self.OnCutNode),
			("C&opy Node","Shift+Ctrl+C",self.OnCopyNode),
			("&Paste Node","Shift+Ctrl+V",self.OnPasteNode),
			("&Delete Node","Shift+Ctrl+BkSp",self.OnDeleteNode),
			("-",None,None),
			("&Insert Node","Ctrl+I",self.OnInsertNode),
			("&Clone Node","Ctrl+`",self.OnCloneNode),
			("Sort C&hildren",None,self.OnSortChildren),
			("&Sort Siblings","Alt-A",self.OnSortSiblings),
			("-",None,None))
		
		self.createMenuEntries(outlineMenu,table)
		#@-body
		#@-node:1::<< create top-level outline menu >>

		
		#@<< create expand/contract submenu >>
		#@+node:2::<< create expand/contract submenu >>
		#@+body
		expandMenu = self.createNewMenu("&Expand/Contract...","Outline")
		
		table = (
			("&Contract All","Alt+-",self.OnContractAll),
			("Contract &Node","Alt+[",self.OnContractNode),
			("Contract &Parent","Alt+0",self.OnContractParent),
			("-",None,None),
			("Expand P&rev Level","Alt+.",self.OnExpandPrevLevel),
			("Expand N&ext Level","Alt+=",self.OnExpandNextLevel),
			("-",None,None),
			("Expand To Level &1","Alt+1",self.OnExpandToLevel1),
			("Expand To Level &2","Alt+2",self.OnExpandToLevel2),
			("Expand To Level &3","Alt+3",self.OnExpandToLevel3),
			("Expand To Level &4","Alt+4",self.OnExpandToLevel4),
			("Expand To Level &5","Alt+5",self.OnExpandToLevel5),
			("Expand To Level &6","Alt+6",self.OnExpandToLevel6),
			("Expand To Level &7","Alt+7",self.OnExpandToLevel7),
			("Expand To Level &8","Alt+8",self.OnExpandToLevel8),
			# ("Expand To Level &9","Alt+9",self.OnExpandToLevel9),
			("-",None,None),
			("Expand &All","Alt+9",self.OnExpandAll),
			("Expand N&ode","Alt+]",self.OnExpandNode))
		
		
		self.createMenuEntries(expandMenu,table)
		#@-body
		#@-node:2::<< create expand/contract submenu >>

		
		#@<< create move submenu >>
		#@+node:3::<< create move submenu >>
		#@+body
		moveSelectMenu = self.createNewMenu("&Move...","Outline")
		
		table = (
			("Move &Down", "Ctrl+D",self.OnMoveDown),
			("Move &Left", "Ctrl+L",self.OnMoveLeft),
			("Move &Right","Ctrl+R",self.OnMoveRight),
			("Move &Up",   "Ctrl+U",self.OnMoveUp),
			("-",None,None),
			("&Promote","Ctrl+{",self.OnPromote),
			("&Demote", "Ctrl+}",self.OnDemote))
			
		self.createMenuEntries(moveSelectMenu,table)
		
		#@-body
		#@-node:3::<< create move submenu >>

		
		#@<< create mark submenu >>
		#@+node:4::<< create mark submenu >>
		#@+body
		markMenu = self.createNewMenu("M&ark/Unmark...","Outline")
		
		table = (
			("&Mark","Ctrl-M",self.OnMark),
			("Mark &Subheads","Alt+S",self.OnMarkSubheads),
			("Mark Changed &Items","Alt+C",self.OnMarkChangedItems),
			("Mark Changed &Roots","Alt+R",self.OnMarkChangedRoots),
			("Mark &Clones","Alt+K",self.OnMarkClones),
			("&Unmark All","Alt+U",self.OnUnmarkAll))
			
		self.createMenuEntries(markMenu,table)
		
		#@-body
		#@-node:4::<< create mark submenu >>

		
		#@<< create goto submenu >>
		#@+node:5::<< create goto submenu >>
		#@+body
		gotoMenu = self.createNewMenu("&Go To...","Outline")
		
		table = (
			("Go Back",None,self.OnGoPrevVisitedNode), # Usually use buttons for this.
			("Go Forward",None,self.OnGoNextVisitedNode),
			("-",None,None),
			("Go To Next &Marked","Alt+M",self.OnGoToNextMarked),
			("Go To Next C&hanged","Alt+D",self.OnGoToNextChanged),
			("Go To Next &Clone","Alt+N",self.OnGoToNextClone),
			("-",None,None),
			("Go To &First Node","Alt+Shift+G",self.OnGoToFirstNode),
			("Go To &Last Node","Alt+Shift+H",self.OnGoToLastNode),
			("Go To &Parent","Alt+Shift+P",self.OnGoToParent),
			("Go To P&rev Sibling","Alt+Shift+R",self.OnGoToPrevSibling),
			("Go To Next &Sibling","Alt+Shift+S",self.OnGoToNextSibling),
			("-",None,None),
			("Go To Prev V&isible","Alt-UpArrow",self.OnGoPrevVisible),
			("Go To Next &Visible","Alt-DnArrow",self.OnGoNextVisible),
			("Go To Prev Node","Alt-Shift+UpArrow",self.OnGoBack),
			("Go To Next Node","Alt-Shift-DnArrow",self.OnGoNext))
			
		self.createMenuEntries(gotoMenu,table)
		
		#@-body
		#@-node:5::<< create goto submenu >>
		#@-body
		#@-node:3::<< create the outline menu >>

		doHook("create-optional-menus",c=c)
		
		#@<< create the window menu >>
		#@+node:4::<< create the window menu >>
		#@+body
		windowMenu = self.createNewMenu("&Window")
		
		table = (
			("&Equal Sized Panes","Ctrl-E",self.OnEqualSizedPanes),
			("Toggle &Active Pane","Ctrl-T",self.OnToggleActivePane),
			("Toggle &Split Direction",None,self.OnToggleSplitDirection),
			("-",None,None),
			("Casca&de",None,self.OnCascade),
			("&Minimize All",None,self.OnMinimizeAll),
			("-",None,None),
			("Open &Compare Window",None,self.OnOpenCompareWindow),
			("Open &Python Window","Alt+P",self.OnOpenPythonWindow))
		
		self.createMenuEntries(windowMenu,table)
		
		#@-body
		#@-node:4::<< create the window menu >>

		
		#@<< create the help menu >>
		#@+node:5::<< create the help menu >>
		#@+body
		helpMenu = self.createNewMenu("&Help")
		
		table = (
			("&About Leo...",None,self.OnAbout),
			("Online &Home Page",None,self.OnLeoHome),
			("-",None,None),
			("Open Online &Tutorial",None,self.OnLeoTutorial))
		
		self.createMenuEntries(helpMenu,table)
		
		if sys.platform=="win32":
			table = (("Open &Offline Tutorial",None,self.OnLeoHelp),)
			self.createMenuEntries(helpMenu,table)
		
		table = (
			("Open Leo&Docs.leo",None,self.OnLeoDocumentation),
			("-",None,None),
			("Open Leo&Config.leo",None,self.OnLeoConfig),
			("Apply &Settings",None,self.OnApplyConfig))
		
		self.createMenuEntries(helpMenu,table)
		#@-body
		#@-node:5::<< create the help menu >>

		top.config(menu=topMenu) # Display the menu.
		app().menuWarningsGiven = true
	
	#@-body
	#@-node:2::createMenuBar
	#@+node:3::createMenuEntries
	#@+body
	#@+at
	#  The old, non-user-configurable code bound shortcuts in createMenuBar.  
	# The new user-configurable code binds shortcuts here.
	# 
	# Centralized tables of shortscuts no longer exist as they did in 
	# createAccelerators.  To check for duplicates, (possibly arising from 
	# leoConfig.txt) we add entries to a central dictionary here, and report 
	# duplicates if an entry for a canonicalized shortcut already exists.

	#@-at
	#@@c

	def createMenuEntries (self,menu,table,openWith=0):
		
		for label,accel,command in table:
			if label == None or command == None or label == "-":
				menu.add_separator()
			else:
				
				#@<< get menu and bind shortcuts >>
				#@+node:1::<< get menu and bind shortcuts >>
				#@+body
				name = string.strip(label)
				name = string.lower(name)
				# Remove special characters from command names.
				name2 = ""
				for ch in name:
					if ch in string.letters or ch in string.digits:
						name2 = name2 + ch
				name = name2
				
				config = app().config
				accel2 = config.getShortcut(name)
				if accel2 and len(accel2) > 0:
					accel = accel2
					# print name,accel
				else:
					pass
					# print "no default:",name
				
				bind_shortcut,menu_shortcut = self.canonicalizeShortcut(accel)
				
				# Kludge: disable the shortcuts for cut, copy, paste.
				# This has already been bound in leoFrame.__init__
				# 2/13/03: A _possible_ fix for the Linux control-v bug.
				if sys.platform not in ("linux1","linux2"):
					if bind_shortcut in ("<Control-c>","<Control-v>","<Control-x>"):
						bind_shortcut = None
				#@-body
				#@-node:1::<< get menu and bind shortcuts >>

				if openWith:
					callback=lambda self=self,path=command:self.OnOpenWith(path)
				else:
					callback=lambda self=self,cmd=command,label=name:self.doCommand(cmd,label)
				realLabel = app().getRealMenuName(label)
				amp_index = realLabel.find("&")
				realLabel = realLabel.replace("&","")
				if not menu_shortcut: menu_shortcut = ""
				menu.add_command(label=realLabel,accelerator=menu_shortcut,
					command=callback,underline=amp_index)
					
				if bind_shortcut:
					if bind_shortcut in self.menuShortcuts:
						if not app().menuWarningsGiven:
							print "duplicate shortcut:", accel, bind_shortcut, label
					else:
						self.menuShortcuts.append(bind_shortcut)
						try:
							# The self and event params must be unbound.
							if openWith:
								f = self.OnOpenWith
								callback=lambda event,f=f,path=command:f(path)
							else:
								f = self.doCommand
								callback=lambda event,f=f,cmd=command,label=name:f(cmd,label,event)
							self.body.bind(bind_shortcut,callback) # To override defaults in body.
							self.top.bind (bind_shortcut,callback)
						except: # could be a user error
							if not app().menuWarningsGiven:
								print "exception binding menu shortcut..."
								print bind_shortcut
								es_exception()
								app().menuWarningsGive = true
	#@-body
	#@-node:3::createMenuEntries
	#@+node:4::createRecentFilesMenuItems
	#@+body
	def createRecentFilesMenuItems (self):
		
		f = self
		recentFilesMenu = f.getMenu("Recent Files...")
		recentFilesMenu.delete(0,len(f.recentFiles))
		i = 1
		for name in f.recentFiles:
			callback = lambda f=f,name=name:f.OnOpenRecentFile(name)
			label = str(i)+" "+name
			recentFilesMenu.add_command(label=label,command=callback,underline=0)
			i += 1
	
	#@-body
	#@-node:4::createRecentFilesMenuItems
	#@+node:5::frame.doCommand
	#@+body
	#@+at
	#  Executes the given command, invoking hooks and catching exceptions.
	# Command handlers no longer need to return "break".  Yippee!
	# 
	# The code assumes that the "command1" hook has completely handled the 
	# command if doHook("command1") returns false.  This provides a very 
	# simple mechanism for overriding commands.

	#@-at
	#@@c

	def doCommand (self,command,label,event=None):
		
		# A horrible kludge: set app().log to cover for a possibly missing activate event.
		app().log = self
	
		if label == "cantredo": label = "redo"
		if label == "cantundo": label = "undo"
		app().commandName = label
		c = self.commands ; v = c.currentVnode() # 2/8/03
		if not doHook("command1",c=c,v=v,label=label):
			try:
				command(event)
			except:
				es("exception executing command")
				print "exception executing command"
				es_exception()
		
		doHook("command2",c=c,v=v,label=label)
				
		return "break" # Inhibit all other handlers.
	#@-body
	#@-node:5::frame.doCommand
	#@+node:6::get/set/destroyMenu
	#@+body
	def getMenu (self,menuName):
	
		cmn = canonicalizeMenuName(menuName)
		return self.menus.get(cmn)
		
	def setMenu (self,menuName,menu):
		
		cmn = canonicalizeMenuName(menuName)
		self.menus [cmn] = menu
		
	def destroyMenu (self,menuName):
		
		cmn = canonicalizeMenuName(menuName)
		del self.menus[cmn]
	
	#@-body
	#@-node:6::get/set/destroyMenu
	#@+node:7::Menu Command Handlers
	#@+node:1::File Menu
	#@+node:1::top level
	#@+node:1::OnNew
	#@+body
	def OnNew (self,event=None):
	
		config = app().config
		frame = LeoFrame() # Create another Leo window.
		top = frame.top
		
		# 5/16/03: Needed for hooks.
		doHook("new",old_c=self,new_c=frame.commands)
	
		# Set the size of the new window.
		h = config.getIntWindowPref("initial_window_height")
		w = config.getIntWindowPref("initial_window_width")
		x = config.getIntWindowPref("initial_window_left")
		y = config.getIntWindowPref("initial_window_top")
		# print h,w,x,y
		if h == None or h < 5: h = 5
		if w == None or w < 5: w = 10
		y = max(y,0) ; x = max(x,0)
		geom = "%dx%d%+d%+d" % (w,h,x,y)
		top.geometry(geom)
		top.deiconify()
		top.lift()
		frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio) # Resize the _new_ frame.
		c = frame.commands # Use the commander of the _new_ frame.
		c.beginUpdate()
		if 1: # within update
			t = leoNodes.tnode()
			v = leoNodes.vnode(c,t)
			v.initHeadString("NewHeadline")
			v.moveToRoot()
			c.editVnode(v)
		c.endUpdate()
		
		frame.body.focus_set()
	#@-body
	#@-node:1::OnNew
	#@+node:2::frame.OnOpen
	#@+body
	def OnOpen(self,event=None):
	
		c = self.commands
		
		#@<< Set closeFlag if the only open window is empty >>
		#@+node:1::<< Set closeFlag if the only open window is empty >>
		#@+body
		#@+at
		#  If this is the only open window was opened when the app started, 
		# and the window has never been written to or saved, then we will 
		# automatically close that window if this open command completes successfully.

		#@-at
		#@@c
			
		closeFlag = (
			self.startupWindow==true and # The window was open on startup
			c.changed==false and self.saved==false and # The window has never been changed
			app().numberOfWindows == 1) # Only one untitled window has ever been opened
		
		#@-body
		#@-node:1::<< Set closeFlag if the only open window is empty >>

		# trace(`closeFlag`)
	
		fileName = tkFileDialog.askopenfilename(
			title="Open",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if fileName and len(fileName) > 0:
			ok, frame = self.OpenWithFileName(fileName)
			if ok and closeFlag:
				app().windowList.remove(self)
				self.destroy() # force the window to go away now.
				app().log = frame # Sets the log stream for es()
	
	#@-body
	#@-node:2::frame.OnOpen
	#@+node:3::frame.OnOpenWith and allies
	#@+body
	#@+at
	#  This routine handles the items in the Open With... menu.
	# These items can only be created by createOpenWithMenuFromTable().
	# Typically this would be done from the "open2" hook.

	#@-at
	#@@c

	def OnOpenWith(self,data=None,event=None):
		
		a = app() ; c = self.commands ; v = c.currentVnode()
		if not data: return
		try:
			openType,arg,ext=data
			if not doHook("openwith1",c=c,v=v,openType=openType,arg=arg,ext=ext):
				
				#@<< set ext based on the present language >>
				#@+node:1::<< set ext based on the present language >>
				#@+body
				if ext == None or len(ext) == 0:
					dict = scanDirectives(c)
					language = dict.get("language")
					ext = a.language_extension_dict.get(language)
					# print language,ext
					if ext == None:
						ext = "txt"
					
				if ext[0] != ".":
					ext = "."+ext
				#@-body
				#@-node:1::<< set ext based on the present language >>

				
				#@<< create or reopen temp file, testing for conflicting changes >>
				#@+node:2::<< create or reopen temp file, testing for conflicting changes >>
				#@+body
				path = None
				
				#@<< set dict and path if a temp file already refers to v.t >>
				#@+node:1::<<set dict and path if a temp file already refers to v.t >>
				#@+body
				for dict in a.openWithFiles:
					v2 = dict.get("v")
					if v.t == v2.t:
						path = dict.get("path")
						if os.path.exists(path):
							break
				#@-body
				#@-node:1::<<set dict and path if a temp file already refers to v.t >>

				if path:
					
					#@<< create or recreate temp file as needed >>
					#@+node:2::<< create or recreate temp file as needed >>
					#@+body
					#@+at
					#  We test for changes in both v and the temp file:
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
						new_time=os.path.getmtime(path)
					except:
						new_time=None
						
					body_changed = old_body != new_body
					temp_changed = old_time != new_time
					
					if body_changed and temp_changed:
						
						#@<< Raise dialog about conflict and set result >>
						#@+node:1::<< Raise dialog about conflict and set result >>
						#@+body
						message = (
							"Conflicting changes in outline and temp file\n\n" +
							"Do you want to use the code in the outline or the temp file?\n\n")
						
						d = leoDialog.leoDialog()
						result = d.askYesNoCancel(
							"Conflict!", message,
							yesMessage = "Outline",
							noMessage = "File",
							defaultButton = "Cancel")
						
						
						#@-body
						#@-node:1::<< Raise dialog about conflict and set result >>

						if result == "cancel": return
						rewrite = result == "outline"
					else:
						rewrite = body_changed
							
					if rewrite:
						path = self.createOpenWithTempFile(v,ext)
					else:
						es("reopening: " + shortFileName(path),color="blue")
					#@-body
					#@-node:2::<< create or recreate temp file as needed >>

				else:
					path = self.createOpenWithTempFile(v,ext)
				
				if not path:
					return # An error has occured.
				#@-body
				#@-node:2::<< create or reopen temp file, testing for conflicting changes >>

				
				#@<< execute a command to open path in external editor >>
				#@+node:3::<< execute a command to open path in external editor >>
				#@+body
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
						filename = os.path.basename(arg)
						command = "os.spawnl("+arg+","+filename+','+ shortPath+")"
						apply(os.spawnl,(os.P_NOWAIT,arg,filename,path))
					elif openType == "os.spawnv":
						filename = os.path.basename(arg)
						command = "os.spawnv("+arg+",("+filename+','+ shortPath+"))"
						apply(os.spawnl,(os.P_NOWAIT,arg,(filename,path)))
					else:
						command="bad command:"+str(openType)
					# This seems a bit redundant.
					# es(command)
				except:
					es("exception executing: "+command)
					es_exception()
				#@-body
				#@-node:3::<< execute a command to open path in external editor >>

			doHook("openwith2",c=c,v=v,openType=openType,arg=arg,ext=ext)
		except:
			es("exception in OnOpenWith")
			es_exception()
	
		return "break"
	#@-body
	#@+node:4::frame.createOpenWithTempFile
	#@+body
	def createOpenWithTempFile (self, v, ext):
		
		c = self.commands ; a = app()
		name = "LeoTemp_" + str(id(v.t)) + '_' + sanitize_filename(v.headString()) + ext
		td = os.path.abspath(tempfile.gettempdir())
		path = os.path.join(td,name)
		try:
			if os.path.exists(path):
				es("recreating:  " + shortFileName(path),color="red")
			else:
				es("creating:  " + shortFileName(path),color="blue")
			file = open(path,"w")
			# 3/7/03: convert s to whatever encoding is in effect.
			s = v.bodyString()
			dict = scanDirectives(self.commands,v=v)
			encoding = dict.get("encoding",None)
			if encoding == None:
				encoding = a.config.default_derived_file_encoding
			s = toEncodedString(s,encoding,reportErrors=true) 
			file.write(s)
			file.flush()
			file.close()
			try:    time=os.path.getmtime(path)
			except: time=None
			# es("time: " + str(time))
			# 4/22/03: add body and encoding entries to dict for later comparisons.
			dict = {"body":s, "c":c, "encoding":encoding, "f":file, "path":path, "time":time, "v":v}
			
			#@<< remove previous entry from a.openWithFiles if it exists >>
			#@+node:1::<< remove previous entry from a.openWithFiles if it exists >>
			#@+body
			openWithList = a.openWithFiles # 5/25/03
			
			for dict in openWithList:
				v2 = dict.get("v")
				if v.t == v2.t:
					print "removing previous entry in a.openWithFiles for",v
					openWithList.remove(dict)
			#@-body
			#@-node:1::<< remove previous entry from a.openWithFiles if it exists >>
 # 4/22/03
			a.openWithFiles.append(dict)
			return path
		except:
			file = None
			es("exception creating temp file",color="red")
			es_exception()
			return None
	#@-body
	#@-node:4::frame.createOpenWithTempFile
	#@-node:3::frame.OnOpenWith and allies
	#@+node:4::frame.OpenWithFileName
	#@+body
	def OpenWithFileName(self, fileName):
	
		if not fileName or len(fileName) == 0:
			return false, None
	
		# Create a full normalized path name.
		# Display the file name with case intact.
		fileName = os.path.join(os.getcwd(), fileName)
		fileName = os.path.normpath(fileName)
		oldFileName = fileName 
		fileName = os.path.normcase(fileName)
	
		# If the file is already open just bring its window to the front.
		list = app().windowList
		for frame in list:
			fn = os.path.normcase(frame.mFileName)
			fn = os.path.normpath(fn)
			if fileName == fn:
				frame.top.deiconify()
				app().log = frame
				# es("This window already open")
				return true, frame
				
		fileName = oldFileName # Use the idiosyncratic file name.
	
		try:
			file = open(fileName,'r')
			if file:
				frame = LeoFrame(fileName)
				if not doHook("open1",
					old_c=self,new_c=frame.commands,fileName=fileName):
					app().log = frame # 5/12/03
					frame.commands.fileCommands.open(file,fileName) # closes file.
				frame.openDirectory=os.path.dirname(fileName)
				frame.updateRecentFiles(fileName)
				doHook("open2",
					old_c=self,new_c=frame.commands,fileName=fileName)
				return true, frame
			else:
				es("can not open" + fileName)
				return false, None
		except:
			es("exceptions opening" + fileName)
			es_exception()
			return false, None
	#@-body
	#@-node:4::frame.OpenWithFileName
	#@+node:5::OnClose
	#@+body
	# Called when File-Close command is chosen.
	
	def OnClose(self,event=None):
		
		u = self.commands.undoer
		if 0:
			if u and u.new_undo and u.debug:
				print "old undo mem:",u.old_mem
				print "new undo mem:",u.new_mem
				print "ratio new/old:",float(u.new_mem)/float(u.old_mem)
		
		self.OnCloseLeoEvent() # Destroy the frame unless the user cancels.
	#@-body
	#@-node:5::OnClose
	#@+node:6::OnSave
	#@+body
	def OnSave(self,event=None):
	
		c = self.commands
		
		# Make sure we never pass None to the ctor.
		if not self.mFileName:
			self.title = ""
			self.mFileName = ""
	
		if self.mFileName != "":
			c.fileCommands.save(self.mFileName)
			c.setChanged(false)
			return
	
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Save",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			self.mFileName = ensure_extension(fileName, ".leo")
			self.title = self.mFileName
			self.top.title(self.setWindowTitle(self.mFileName)) # 3/25/03
			c.fileCommands.save(self.mFileName)
			self.updateRecentFiles(self.mFileName)
	#@-body
	#@-node:6::OnSave
	#@+node:7::OnSaveAs
	#@+body
	def OnSaveAs(self,event=None):
	
		# Make sure we never pass None to the ctor.
		if not self.mFileName:
			self.title = ""
			
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Save As",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			self.mFileName = ensure_extension(fileName, ".leo")
			self.title = self.mFileName
			self.top.title(self.setWindowTitle(self.mFileName)) # 3/25/03
			self.commands.fileCommands.saveAs(self.mFileName)
			self.updateRecentFiles(self.mFileName)
	#@-body
	#@-node:7::OnSaveAs
	#@+node:8::OnSaveTo
	#@+body
	def OnSaveTo(self,event=None):
	
		# Make sure we never pass None to the ctor.
		if not self.mFileName:
			self.title = ""
	
		# set local fileName, _not_ self.mFileName
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Save To",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			fileName = ensure_extension(fileName, ".leo")
			self.commands.fileCommands.saveTo(fileName)
			self.updateRecentFiles(self.mFileName)
	
	#@-body
	#@-node:8::OnSaveTo
	#@+node:9::OnRevert
	#@+body
	def OnRevert(self,event=None):
	
		# Make sure the user wants to Revert.
		if not self.mFileName:
			self.mFileName = ""
		if len(self.mFileName)==0:
			return
		
		d = leoDialog.leoDialog()
		reply = d.askYesNo("Revert",
			"Revert to previous version of " + self.mFileName + "?")
	
		if reply=="no":
			return
	
		# Kludge: rename this frame so OpenWithFileName won't think it is open.
		fileName = self.mFileName ; self.mFileName = ""
	
		# Create a new frame before deleting this frame.
		ok, frame = self.OpenWithFileName(fileName)
		if ok:
			frame.top.deiconify()
			app().windowList.remove(self)
			self.destroy() # Destroy this frame.
		else:
			self.mFileName = fileName
	
	#@-body
	#@-node:9::OnRevert
	#@+node:10::frame.OnQuit
	#@+body
	def OnQuit(self,event=None):
	
		app().quitting += 1
		
		while app().windowList:
			w = app().windowList[0]
			if not w.OnCloseLeoEvent():
				break
				
		app().quitting -= 1 # If we get here the quit has been disabled.
	
	
	#@-body
	#@-node:10::frame.OnQuit
	#@+node:11::frame.updateRecentFiles
	#@+body
	def updateRecentFiles (self, fileName):
		
		if not fileName or len(fileName) == 0:
			return
		
		# Update the recent files list in all windows.
		normFileName = os.path.normcase(fileName)
		
		for frame in app().windowList:
			# Remove all versions of the file name.
			for name in frame.recentFiles:
				name2 = os.path.normcase(name)
				name2 = os.path.normpath(name2)
				if normFileName == name2:
					frame.recentFiles.remove(name)
			frame.recentFiles.insert(0,fileName)
			# Recreate the Recent Files menu.
			frame.createRecentFilesMenuItems()
			
		# Update the config file.
		app().config.setRecentFiles(frame.recentFiles)
		app().config.update()
	#@-body
	#@-node:11::frame.updateRecentFiles
	#@-node:1::top level
	#@+node:2::Recent Files submenu
	#@+node:1::frame.OpenWithFileName
	#@+body
	def OpenWithFileName(self, fileName):
	
		if not fileName or len(fileName) == 0:
			return false, None
	
		# Create a full normalized path name.
		# Display the file name with case intact.
		fileName = os.path.join(os.getcwd(), fileName)
		fileName = os.path.normpath(fileName)
		oldFileName = fileName 
		fileName = os.path.normcase(fileName)
	
		# If the file is already open just bring its window to the front.
		list = app().windowList
		for frame in list:
			fn = os.path.normcase(frame.mFileName)
			fn = os.path.normpath(fn)
			if fileName == fn:
				frame.top.deiconify()
				app().log = frame
				# es("This window already open")
				return true, frame
				
		fileName = oldFileName # Use the idiosyncratic file name.
	
		try:
			file = open(fileName,'r')
			if file:
				frame = LeoFrame(fileName)
				if not doHook("open1",
					old_c=self,new_c=frame.commands,fileName=fileName):
					app().log = frame # 5/12/03
					frame.commands.fileCommands.open(file,fileName) # closes file.
				frame.openDirectory=os.path.dirname(fileName)
				frame.updateRecentFiles(fileName)
				doHook("open2",
					old_c=self,new_c=frame.commands,fileName=fileName)
				return true, frame
			else:
				es("can not open" + fileName)
				return false, None
		except:
			es("exceptions opening" + fileName)
			es_exception()
			return false, None
	#@-body
	#@-node:1::frame.OpenWithFileName
	#@+node:2::frame.OnOpenRecentFile
	#@+body
	def OnOpenRecentFile(self,name=None):
		
		c = self.commands ; v = c.currentVnode()
		
		#@<< Set closeFlag if the only open window is empty >>
		#@+node:1::<< Set closeFlag if the only open window is empty >>
		#@+body
		#@+at
		#  If this is the only open window was opened when the app started, 
		# and the window has never been written to or saved, then we will 
		# automatically close that window if this open command completes successfully.

		#@-at
		#@@c
			
		closeFlag = (
			self.startupWindow==true and # The window was open on startup
			c.changed==false and self.saved==false and # The window has never been changed
			app().numberOfWindows == 1) # Only one untitled window has ever been opened
		
		#@-body
		#@-node:1::<< Set closeFlag if the only open window is empty >>

		if not name:
			return
	
		fileName = name
		if not doHook("recentfiles1",c=c,v=v,fileName=fileName,closeFlag=closeFlag):
			ok, frame = self.OpenWithFileName(fileName)
			if ok and closeFlag:
				app().windowList.remove(self)
				self.destroy() # force the window to go away now.
				app().log = frame # Sets the log stream for es()
		doHook("recentfiles2",c=c,v=v,fileName=fileName,closeFlag=closeFlag)
	#@-body
	#@-node:2::frame.OnOpenRecentFile
	#@-node:2::Recent Files submenu
	#@+node:3::Read/Write submenu
	#@+node:1::fileCommands.OnReadOutlineOnly
	#@+body
	def OnReadOutlineOnly (self,event=None):
	
		fileName = tkFileDialog.askopenfilename(
			title="Read Outline Only",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if not fileName or len(fileName) == 0:
			return
			
		try: # 11/18/02
			file = open(fileName,'r')
			frame = LeoFrame(fileName)
			frame.top.deiconify()
			frame.top.lift()
			app().root.update() # Force a screen redraw immediately.
			frame.commands.fileCommands.readOutlineOnly(file,fileName) # closes file.
		except:
			es("can not open:" + fileName)
	#@-body
	#@-node:1::fileCommands.OnReadOutlineOnly
	#@+node:2::OnReadAtFileNodes
	#@+body
	def OnReadAtFileNodes (self,event=None):
	
		c = self.commands
		
		d = leoDialog.leoDialog()
		answer = d.askOkCancel("Proceed?",
			"Read @file Nodes is not undoable." +
			"\nProceed?")
	
		if answer=="ok":
			c.fileCommands.readAtFileNodes()
			c.undoer.clearUndoState()
	
	#@-body
	#@-node:2::OnReadAtFileNodes
	#@+node:3::OnWriteDirtyAtFileNodes
	#@+body
	def OnWriteDirtyAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeDirtyAtFileNodes()
	
	#@-body
	#@-node:3::OnWriteDirtyAtFileNodes
	#@+node:4::OnWriteMissingAtFileNodes
	#@+body
	def OnWriteMissingAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeMissingAtFileNodes()
	
	#@-body
	#@-node:4::OnWriteMissingAtFileNodes
	#@+node:5::OnWriteOutlineOnly
	#@+body
	def OnWriteOutlineOnly (self,event=None):
	
		self.commands.fileCommands.writeOutlineOnly()
	
	#@-body
	#@-node:5::OnWriteOutlineOnly
	#@+node:6::OnWriteAtFileNodes
	#@+body
	def OnWriteAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeAtFileNodes()
	
	#@-body
	#@-node:6::OnWriteAtFileNodes
	#@+node:7::OnReadGnxFile
	#@+body
	def OnReadGnxFile (self,event=None):
		
		trace()
		c = self.commands ; v = c.currentVnode()
		
		c.beginUpdate()
		c.atFileCommands.using_gnx = true # Flag to add ".txt" to file name.
		c.atFileCommands.read(v)
		c.atFileCommands.using_gnx = false
		c.initAllCloneBits() ## Must be done after all reads.
		c.endUpdate()
		c.recolor()
		es("finished")
	
	#@-body
	#@-node:7::OnReadGnxFile
	#@+node:8::OnWriteGnxFile
	#@+body
	def OnWriteGnxFile (self,event=None):
		
		c = self.commands ; v = c.currentVnode()
	
		c.atFileCommands.using_gnx = true
		c.atFileCommands.write(v)
		c.atFileCommands.using_gnx = false
		es("finished")
	
	#@-body
	#@-node:8::OnWriteGnxFile
	#@+node:9::OnClearAllNodeIndices
	#@+body
	def OnClearAllNodeIndices (self,event=None):
		
		c = self.commands ; root = c.rootVnode()
		v = root
		while v:
			v.t.gnx = None
			v = v.threadNext()
		es("all tnode indices cleared",color="red")
	#@-body
	#@-node:9::OnClearAllNodeIndices
	#@-node:3::Read/Write submenu
	#@+node:4::Tangle submenu
	#@+node:1::OnTangleAll
	#@+body
	def OnTangleAll(self,event=None):
	
		self.commands.tangleCommands.tangleAll()
	
	#@-body
	#@-node:1::OnTangleAll
	#@+node:2::OnTangleMarked
	#@+body
	def OnTangleMarked(self,event=None):
	
		self.commands.tangleCommands.tangleMarked()
	
	#@-body
	#@-node:2::OnTangleMarked
	#@+node:3::OnTangle
	#@+body
	def OnTangle (self,event=None):
	
		self.commands.tangleCommands.tangle()
	
	#@-body
	#@-node:3::OnTangle
	#@-node:4::Tangle submenu
	#@+node:5::Untangle submenu
	#@+node:1::OnUntangleAll
	#@+body
	def OnUntangleAll(self,event=None):
	
		c = self.commands
		c.tangleCommands.untangleAll()
		c.undoer.clearUndoState()
	
	#@-body
	#@-node:1::OnUntangleAll
	#@+node:2::OnUntangleMarked
	#@+body
	def OnUntangleMarked(self,event=None):
	
		c = self.commands
		self.commands.tangleCommands.untangleMarked()
		c.undoer.clearUndoState()
	
	#@-body
	#@-node:2::OnUntangleMarked
	#@+node:3::OnUntangle
	#@+body
	def OnUntangle(self,event=None):
	
		c = self.commands
		self.commands.tangleCommands.untangle()
		c.undoer.clearUndoState()
	
	#@-body
	#@-node:3::OnUntangle
	#@-node:5::Untangle submenu
	#@+node:6::Import&Export submenu
	#@+node:1::OnExportHeadlines
	#@+body
	def OnExportHeadlines (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Export Headlines",filetypes=filetypes,
			initialfile="headlines.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			self.commands.importCommands.exportHeadlines(fileName)
	
	#@-body
	#@-node:1::OnExportHeadlines
	#@+node:2::OnFlattenOutline
	#@+body
	def OnFlattenOutline (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Flatten Outline",filetypes=filetypes,
			initialfile="flat.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.flattenOutline(fileName)
	
	#@-body
	#@-node:2::OnFlattenOutline
	#@+node:3::OnImportAtRoot
	#@+body
	def OnImportAtRoot (self,event=None):
		
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
	
		fileName = tkFileDialog.askopenfilename(
			title="Import To @root",filetypes=types)
		if fileName and len(fileName) > 0:
			c = self.commands
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFilesCommand (paths,"@root")
	
	#@-body
	#@-node:3::OnImportAtRoot
	#@+node:4::OnImportAtFile
	#@+body
	def OnImportAtFile (self,event=None):
		
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
				
		fileName = tkFileDialog.askopenfilename(
			title="Import To @file",filetypes=types)
		if fileName and len(fileName) > 0:
			c = self.commands
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFilesCommand (paths,"@file")
	
	#@-body
	#@-node:4::OnImportAtFile
	#@+node:5::OnImportCWEBFiles
	#@+body
	def OnImportCWEBFiles (self,event=None):
		
		filetypes = [
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = tkFileDialog.askopenfilename(
			title="Import CWEB Files",filetypes=filetypes,
			defaultextension=".w")
		if fileName and len(fileName) > 0:
			c = self.commands
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importWebCommand(paths,"cweb")
	
	#@-body
	#@-node:5::OnImportCWEBFiles
	#@+node:6::OnImportFlattenedOutline
	#@+body
	def OnImportFlattenedOutline (self,event=None):
		
		types = [("Text files","*.txt"), ("All files","*")]
			
		fileName = tkFileDialog.askopenfilename(
			title="Import MORE Text",
			filetypes=types,
			defaultextension=".py")
		if fileName and len(fileName) > 0:
			c = self.commands
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importFlattenedOutline(paths)
	
	#@-body
	#@-node:6::OnImportFlattenedOutline
	#@+node:7::OnImportNowebFiles
	#@+body
	def OnImportNowebFiles (self,event=None):
		
		filetypes = [
			("Noweb files", "*.nw"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = tkFileDialog.askopenfilename(
			title="Import Noweb Files",filetypes=filetypes,
			defaultextension=".nw")
		if fileName and len(fileName) > 0:
			c = self.commands
			paths = [fileName] # alas, askopenfilename returns only a single name.
			c.importCommands.importWebCommand(paths,"noweb")
	
	#@-body
	#@-node:7::OnImportNowebFiles
	#@+node:8::OnOutlineToCWEB
	#@+body
	def OnOutlineToCWEB (self,event=None):
		
		filetypes=[
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Outline To CWEB",filetypes=filetypes,
			initialfile="cweb.w",defaultextension=".w")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.outlineToWeb(fileName,"cweb")
	
	#@-body
	#@-node:8::OnOutlineToCWEB
	#@+node:9::OnOutlineToNoweb
	#@+body
	def OnOutlineToNoweb (self,event=None):
		
		filetypes=[
			("Noweb files", "*.nw"),
			("Text files", "*.txt"),
			("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Outline To Noweb",filetypes=filetypes,
			initialfile=self.outlineToNowebDefaultFileName,defaultextension=".nw")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.outlineToWeb(fileName,"noweb")
			self.outlineToNowebDefaultFileName = fileName
	
	#@-body
	#@-node:9::OnOutlineToNoweb
	#@+node:10::OnRemoveSentinels
	#@+body
	def OnRemoveSentinels (self,event=None):
		
		types = [
			("All files","*"),
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py") ]
			
		fileName = tkFileDialog.askopenfilename(
			title="Remove Sentinels",filetypes=types)
	
		if fileName and len(fileName) > 0:
			c = self.commands
			# alas, askopenfilename returns only a single name.
			c.importCommands.removeSentinelsCommand (fileName)
	
	#@-body
	#@-node:10::OnRemoveSentinels
	#@+node:11::OnWeave
	#@+body
	def OnWeave (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Weave",filetypes=filetypes,
			initialfile="weave.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.weave(fileName)
	
	#@-body
	#@-node:11::OnWeave
	#@+node:12::OnWriteOldOutline
	#@+body
	# Based on the Save As code.
	
	def OnWriteOldOutline (self,event=None):
		
		"""Saves a pre-4.0 outline"""
		a = app()
	
		# Make sure we never pass None to the ctor.
		if not self.mFileName:
			self.title = ""
	
		# set local fileName, _not_ self.mFileName
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Write Pre 4.0 Outline",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			fileName = ensure_extension(fileName, ".leo")
			old = a.use_gnx ; a.use_gnx = false
			self.commands.fileCommands.saveTo(fileName)
			self.updateRecentFiles(self.mFileName)
			a.use_gnx = old
	#@-body
	#@-node:12::OnWriteOldOutline
	#@-node:6::Import&Export submenu
	#@-node:1::File Menu
	#@+node:2::Edit Menu (change to handle log pane too)
	#@+node:1::Edit top level
	#@+node:1::OnUndo
	#@+body
	def OnUndo(self,event=None):
	
		self.commands.undoer.undo()
	
	#@-body
	#@-node:1::OnUndo
	#@+node:2::OnRedo
	#@+body
	def OnRedo(self,event=None):
	
		self.commands.undoer.redo()
	
	#@-body
	#@-node:2::OnRedo
	#@+node:3::frame.OnCut, OnCutFrom Menu
	#@+body
	def OnCut (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.commands.tree.onBodyWillChange(v,"Cut")
	
	def OnCutFromMenu (self,event=None):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Cut"))
		
		# 11/2/02: Make sure the event sticks.
		c = self.commands ; v = c.currentVnode()
		c.tree.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	
	#@-body
	#@-node:3::frame.OnCut, OnCutFrom Menu
	#@+node:4::frame.OnCopy, OnCopyFromMenu
	#@+body
	def OnCopy (self,event=None):
	
		# Copy never changes dirty bits or syntax coloring.
		pass
		
	def OnCopyFromMenu (self,event=None):
	
		# trace()
		w = self.getFocus()
		w.event_generate(virtual_event_name("Copy"))
	
	#@-body
	#@-node:4::frame.OnCopy, OnCopyFromMenu
	#@+node:5::frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+body
	def OnPaste (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.commands.tree.onBodyWillChange(v,"Paste")
		
	def OnPasteNode (self,event=None):
	
		# trace(`event`)
		pass
		
	def OnPasteFromMenu (self,event=None):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Paste"))
		
		# 10/23/02: Make sure the event sticks.
		c = self.commands ; v = c.currentVnode()
		c.tree.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	
	#@-body
	#@-node:5::frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+node:6::OnDelete
	#@+body
	def OnDelete(self,event=None):
	
		c = self.commands ; v = c.currentVnode()
		first, last = getTextSelection(self.body)
		if first and last:
			self.body.delete(first,last)
			c.tree.onBodyChanged(v,"Delete")
	
	#@-body
	#@-node:6::OnDelete
	#@+node:7::OnExecuteScript
	#@+body
	#@+at
	#  This executes body text as a Python script.  We execute the selected 
	# text, or the entire body text if no text is selected.

	#@-at
	#@@c

	def OnExecuteScript(self,event=None,v=None):
		
		c = self.commands ; body = self.body ; s = None
		if v == None:
			v = c.currentVnode() 
	
		# Assume any selected body text is a script.
		start,end = getTextSelection(body)
		if start and end:
			s = body.get(start,end)
		else:
			s = body.get("1.0","end")
		if s == None:
			s = ""
			
		s = s.strip()
		if s and len(s) > 0:
			s += '\n' # Make sure we end the script properly.
			try:
				# 12/11/02: Use {} to get a pristine environment!
				exec s in {}
			except:
				es("exception executing script")
				es_exception(full=false)
		else:
			es("no script selected")
	#@-body
	#@-node:7::OnExecuteScript
	#@+node:8::OnGoToLineNumber & allies
	#@+body
	def OnGoToLineNumber (self,event=None):
	
		c = self.commands
		
		#@<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		#@+node:1::<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		#@+body
		v = c.currentVnode()
		fileName = None
		while v and not fileName:
			if v.isAtFileNode():
				fileName = v.atFileNodeName()
			elif v.isAtSilentFileNode():
				fileName = v.atSilentFileNodeName()
			elif v.isAtRawFileNode():
				fileName = v.atRawFileNodeName()
			else:
				v = v.parent()
		
		root = v
		if not root:
			es("no @file node found") ; return
		#@-body
		#@-node:1::<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>

		
		#@<< read the file into lines >>
		#@+node:2::<< read the file into lines >>
		#@+body
		# 1/26/03: calculate the full path.
		d = scanDirectives(c)
		path = d.get("path")
		fileName = os.path.join(path,fileName)
		
		try:
			file=open(fileName)
			lines = file.readlines()
			file.close()
		except:
			es("not found: " + fileName)
			return
			
		
		#@-body
		#@-node:2::<< read the file into lines >>

		
		#@<< get n, the line number, from a dialog >>
		#@+node:3::<< get n, the line number, from a dialog >>
		#@+body
		import leoDialog
		
		d = leoDialog.leoDialog()
		n = d.askOkCancelNumber("Enter Line Number","Line number:")
		if n == -1:
			return
		#@-body
		#@-node:3::<< get n, the line number, from a dialog >>

		# trace("n:"+`n`)
		if n==1:
			v = root ; n2 = 1 ; found = true
		elif n >= len(lines):
			v = root.lastNode()
			n2 = v.bodyString().count('\n')
			found = false
		elif root.isAtSilentFileNode():
			
			#@<< count outline lines, setting v,n2,found >>
			#@+node:4::<< count outline lines, setting v,n2,found >>
			#@+body
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
			#@-body
			#@-node:4::<< count outline lines, setting v,n2,found >>

		else:
			# To do: choose a "suitable line" for searching.
			vnodeName,n2 = self.convertLineToVnodeAndLine(lines,n,root)
			found = true
			if not vnodeName:
				es("invalid derived file: " + fileName)
				return
			
			#@<< set v to the node whose headline is vnodeName >>
			#@+node:5::<< set v to the node whose headline is vnodeName >>
			#@+body
			after = root.nodeAfterTree()
			while v and v != after and not v.matchHeadline(vnodeName):
				v = v.threadNext()
			
			if not v or v == after:
				es("vnode not found in outline: " + vnodeName)
				return
			#@-body
			#@-node:5::<< set v to the node whose headline is vnodeName >>

		# To do: search for the "suitable line".
		
		#@<< select v and make it visible >>
		#@+node:6::<< select v and make it visible >>
		#@+body
		c.beginUpdate()
		c.tree.expandAllAncestors(v)
		c.selectVnode(v)
		c.endUpdate()
		#@-body
		#@-node:6::<< select v and make it visible >>

		
		#@<< put the cursor on line n2 of the body text >>
		#@+node:7::<< put the cursor on line n2 of the body text >>
		#@+body
		if found:
			c.frame.body.mark_set("insert",str(n2)+".0 linestart")
		else:
			c.frame.body.mark_set("insert","end-1line")
			es(root.headString() + " has " + `len(lines)` + " lines.")
		#@-body
		#@-node:7::<< put the cursor on line n2 of the body text >>
	#@-body
	#@+node:8::convertLineToVnodeAndLine
	#@+body
	#@+at
	#  This routine converts a line number, n, in a derived file to a vnode 
	# and offset within the vnode
	# 
	# We count "real" lines in the derived files, ignoring all sentinels that 
	# do not arise from source lines.  When the indicated line is found, we 
	# scan backwards for an @+body line, get the vnode's name from that line 
	# and set v to the indicated vnode.  This will fail if vnode names have 
	# been changed, and that can't be helped.
	# 
	# Returns vnodeName,n2,found
	# vnodeName: the name found in the previous @+body sentinel.
	# offset: the offset within v of the desired line.

	#@-at
	#@@c

	def convertLineToVnodeAndLine (self,lines,n,root):
		
		
		#@<< set delim, leoLine from the @+leo line >>
		#@+node:1::<< set delim, leoLine from the @+leo line >>
		#@+body
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
			delim = s[i:j]
			if len(delim)==0:
				delim=None
			else:
				delim += '@'
		#@-body
		#@-node:1::<< set delim, leoLine from the @+leo line >>

		if not delim:
			es("bad @+leo sentinel")
			return None,None
		
		#@<< scan back to @+node, setting offset,nodeSentinelLine >>
		#@+node:2::<< scan back to  @+node, setting offset,nodeSentinelLine >>
		#@+body
		offset = 0 # This is essentially the Tk line number.
		nodeSentinelLine = -1
		line = n - 1
		while line >= 0:
			s = lines[line]
			# trace(`s`)
			i = skip_ws(s,0)
			if match(s,i,delim):
				
				#@<< handle delim while scanning backward >>
				#@+node:1::<< handle delim while scanning backward >>
				#@+body
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
				#@-body
				#@-node:1::<< handle delim while scanning backward >>

			else:
				offset += 1 # Assume the line is real.  A dubious assumption.
			line -= 1
		#@-body
		#@-node:2::<< scan back to  @+node, setting offset,nodeSentinelLine >>

		if nodeSentinelLine == -1:
			# The line precedes the first @+node sentinel
			return root.headString(),1
		s = lines[nodeSentinelLine]
		
		#@<< set vnodeName from s >>
		#@+node:3::<< set vnodeName from s >>
		#@+body
		# vnode name is everything following the third ':'
		
		# trace("last body:"+`s`)
		vnodeName = None
		i = 0 ; colons = 0
		while i < len(s) and colons < 3:
			if s[i] == ':': colons += 1
			i += 1
		vnodeName = s[i:].strip()
		# trace("vnodeName:"+`vnodeName`)
		
		if len(vnodeName) == 0:
			vnodeName = None
		if not vnodeName:
			es("bad @+node sentinel")
		#@-body
		#@-node:3::<< set vnodeName from s >>

		return vnodeName,offset
	#@-body
	#@-node:8::convertLineToVnodeAndLine
	#@+node:9::skipToMatchingSentinel
	#@+body
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
					if level == 0: return n
					else: level -= 1
			n += delta # bug fix: 1/30/02
		return n
	#@-body
	#@-node:9::skipToMatchingSentinel
	#@-node:8::OnGoToLineNumber & allies
	#@+node:9::OnSelectAll
	#@+body
	def OnSelectAll(self,event=None):
	
		setTextSelection(self.body,"1.0","end")
	
	#@-body
	#@-node:9::OnSelectAll
	#@+node:10::OnFontPanel
	#@+body
	def OnFontPanel(self,event=None):
	
		if self.fontPanel:
			# trace()
			self.fontPanel.top.deiconify()
		else:
			self.fontPanel = fp =  leoFontPanel.leoFontPanel(self.commands)
			fp.run()
	
	#@-body
	#@-node:10::OnFontPanel
	#@+node:11::OnColorPanel
	#@+body
	def OnColorPanel(self,event=None):
		
		if self.colorPanel:
			# trace()
			self.colorPanel.top.deiconify()
		else:
			self.colorPanel = cp = leoColor.leoColorPanel(self.commands)
			cp.run()
	
	
	#@-body
	#@-node:11::OnColorPanel
	#@+node:12::OnViewAllCharacters
	#@+body
	def OnViewAllCharacters (self, event=None):
	
		c = self.commands ; v = c.currentVnode() ; colorizer = c.tree.colorizer
		colorizer.showInvisibles = choose(colorizer.showInvisibles,0,1)
		# print `colorizer.showInvisibles`
	
		# It is much easier to change the menu name here than in the menu updater.
		menu = self.getMenu("Edit")
		if colorizer.showInvisibles:
			setMenuLabel(menu,"Show Invisibles","Hide Invisibles")
		else:
			setMenuLabel(menu,"Hide Invisibles","Show Invisibles")
	
		c.tree.recolor_now(v)
	
	#@-body
	#@-node:12::OnViewAllCharacters
	#@+node:13::OnPreferences
	#@+body
	def OnPreferences(self,event=None):
		
		c = self.commands
		if self.prefsPanel:
			# trace()
			self.prefsPanel.top.deiconify()
		else:
			self.prefsPanel = prefs = leoPrefs.LeoPrefs(c)
			top = prefs.top
			center_dialog(top)
	
			if 0: # No need to make this modal
				top.grab_set() # Make the dialog a modal dialog.
				top.focus_force() # Get all keystrokes.
				app().root.wait_window(top)
	
	#@-body
	#@-node:13::OnPreferences
	#@-node:1::Edit top level
	#@+node:2::Edit Body submenu
	#@+node:1::OnConvertBlanks & OnConvertAllBlanks
	#@+body
	def OnConvertBlanks(self,event=None):
	
		self.commands.convertBlanks()
	
		
	def OnConvertAllBlanks(self,event=None):
	
		self.commands.convertAllBlanks()
	
	#@-body
	#@-node:1::OnConvertBlanks & OnConvertAllBlanks
	#@+node:2::OnConvertTabs & OnConvertAllTabs
	#@+body
	def OnConvertTabs(self,event=None):
	
		self.commands.convertTabs()
		
	def OnConvertAllTabs(self,event=None):
	
		self.commands.convertAllTabs()
	
	def OnReformatParagraph(self,event=None):
		
		self.commands.reformatParagraph()
	
	#@-body
	#@-node:2::OnConvertTabs & OnConvertAllTabs
	#@+node:3::OnDedent
	#@+body
	def OnDedent (self,event=None):
	
		self.commands.dedentBody()
	
	#@-body
	#@-node:3::OnDedent
	#@+node:4::OnExtract
	#@+body
	def OnExtract(self,event=None):
	
		self.commands.extract()
	
	#@-body
	#@-node:4::OnExtract
	#@+node:5::OnExtractNames
	#@+body
	def OnExtractNames(self,event=None):
	
		self.commands.extractSectionNames()
	
	#@-body
	#@-node:5::OnExtractNames
	#@+node:6::OnExtractSection
	#@+body
	def OnExtractSection(self,event=None):
	
		self.commands.extractSection()
	
	#@-body
	#@-node:6::OnExtractSection
	#@+node:7::OnFindMatchingBracket
	#@+body
	def OnFindMatchingBracket (self,event=None):
		
		c = self ; body = c.body
		brackets = "()[]{}<>"
		ch1=body.get("insert -1c")
		ch2=body.get("insert")
	
		# Prefer to match the character to the left of the cursor.
		if ch1 in brackets:
			ch = ch1 ; index = body.index("insert -1c")
		elif ch2 in brackets:
			ch = ch2 ; index = body.index("insert")
		else:
			return
		
		index2 = self.findMatchingBracket(ch,body,index)
		if index2:
			if body.compare(index,"<=",index2):
				setTextSelection(self.body,index,index2+"+1c")
			else:
				setTextSelection(self.body,index2,index+"+1c")
			body.mark_set("insert",index2+"+1c")
			body.see(index2+"+1c")
		else:
			es("unmatched " + `ch`)
	
	#@-body
	#@+node:1::findMatchingBracket
	#@+body
	# Test  unmatched())
	def findMatchingBracket(self,ch,body,index):
	
		open_brackets  = "([{<"
		close_brackets = ")]}>"
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
			if (forward and body.compare(index, ">=", "end")):
				return None
			if (not forward and body.compare(index,"<=","1.0")):
				return None
			ch2 = body.get(index)
			if ch2 == ch: level += 1
			if ch2 == match_ch:
				level -= 1
				if level <= 0:
					return index
			index = index + choose(forward,"+1c","-1c")
			index = body.index(index)
		return 0 # unreachable: keeps pychecker happy.
	# Test  (
	# ([(x){y}]))
	# Test  ((x)(unmatched
	#@-body
	#@-node:1::findMatchingBracket
	#@-node:7::OnFindMatchingBracket
	#@+node:8::OnIndent
	#@+body
	def OnIndent(self,event=None):
	
		self.commands.indentBody()
	
	#@-body
	#@-node:8::OnIndent
	#@+node:9::OnInsertBody/HeadlineTime & allies
	#@+body
	def OnInsertBodyTime (self,event=None):
		
		c = self.commands ; v = c.currentVnode()
		sel1,sel2 = getTextSelection(c.body)
		if sel1 and sel2:
			c.body.delete(sel1,sel2)
		c.body.insert("insert",self.getTime(body=true))
		c.tree.onBodyChanged(v,"Typing")
		
	def OnInsertHeadlineTime (self,event=None):
	
		c = self.commands ; v = c.currentVnode()
		s = v.headString() # Remember the old value.
	
		if v.edit_text:
			sel1,sel2 = getTextSelection(v.edit_text)
			if sel1 and sel2:
				v.edit_text.delete(sel1,sel2)
			v.edit_text.insert("insert",self.getTime(body=false))
			c.tree.idle_head_key(v)
			
		# A kludge to get around not knowing whether we are editing or not.
		if s.strip() == v.headString().strip():
			es("Edit headline to append date/time")
	#@-body
	#@+node:1::getTime
	#@+body
	def getTime (self,body=true):
		
		import time
		
		config = app().config
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
	
	#@-body
	#@-node:1::getTime
	#@-node:9::OnInsertBody/HeadlineTime & allies
	#@-node:2::Edit Body submenu
	#@+node:3::Edit Headline submenu
	#@+node:1::OnEditHeadline
	#@+body
	def OnEditHeadline(self,event=None):
	
		tree = self.commands.tree
		tree.editLabel(tree.currentVnode)
	
	#@-body
	#@-node:1::OnEditHeadline
	#@+node:2::OnEndEditHeadline
	#@+body
	def OnEndEditHeadline(self,event=None):
		
		tree = self.commands.tree
		tree.endEditLabelCommand()
	
	#@-body
	#@-node:2::OnEndEditHeadline
	#@+node:3::OnAbortEditHeadline
	#@+body
	def OnAbortEditHeadline(self,event=None):
		
		tree = self.commands.tree
		tree.abortEditLabelCommand()
	
	#@-body
	#@-node:3::OnAbortEditHeadline
	#@+node:4::OnToggleAngleBrackets
	#@+body
	def OnToggleAngleBrackets (self,event=None):
		
		c = self.commands ; v = c.currentVnode()
		s = v.headString().strip()
		if (s[0:2] == "<<"
			or s[-2:] == ">>"): # Must be on separate line.
			if s[0:2] == "<<": s = s[2:]
			if s[-2:] == ">>": s = s[:-2]
			s = s.strip()
		else:
			s = angleBrackets(' ' + s + ' ')
		
		c.tree.editLabel(v)
		if v.edit_text:
			v.edit_text.delete("1.0","end")
			v.edit_text.insert("1.0",s)
			c.tree.onHeadChanged(v)
	
	#@-body
	#@-node:4::OnToggleAngleBrackets
	#@-node:3::Edit Headline submenu
	#@+node:4::Find submenu (frame methods)
	#@+node:1::OnFindPanel
	#@+body
	def OnFindPanel(self,event=None):
	
		find = app().findFrame
		# 15-SEP-2002 DTHEIN: call withdraw() to force findFrame to top after 
		#                     opening multiple Leo files.
		find.top.withdraw()
		find.top.deiconify()
		
		t = find.find_text
		t.focus_set()
		setTextSelection (t,"1.0","end") # Thanks Rich.
		find.commands = self
	
	#@-body
	#@-node:1::OnFindPanel
	#@+node:2::OnFindNext
	#@+body
	def OnFindNext(self,event=None):
	
		c = self.commands
		app().findFrame.findNextCommand(c)
	
	#@-body
	#@-node:2::OnFindNext
	#@+node:3::OnFindPrevious
	#@+body
	def OnFindPrevious(self,event=None):
	
		c = self.commands
		app().findFrame.findPreviousCommand(c)
	
	#@-body
	#@-node:3::OnFindPrevious
	#@+node:4::OnReplace
	#@+body
	def OnReplace(self,event=None):
	
		c = self.commands
		app().findFrame.changeCommand(c)
	
	#@-body
	#@-node:4::OnReplace
	#@+node:5::OnReplaceThenFind
	#@+body
	def OnReplaceThenFind(self,event=None):
	
		c = self.commands
		app().findFrame.changeThenFindCommand(c)
	
	#@-body
	#@-node:5::OnReplaceThenFind
	#@-node:4::Find submenu (frame methods)
	#@-node:2::Edit Menu (change to handle log pane too)
	#@+node:3::Outline Menu
	#@+node:1::top level
	#@+node:1::OnCutNode
	#@+body
	def OnCutNode(self,event=None):
	
		self.commands.cutOutline()
	
	#@-body
	#@-node:1::OnCutNode
	#@+node:2::OnCopyNode
	#@+body
	def OnCopyNode(self,event=None):
	
		self.commands.copyOutline()
	
	#@-body
	#@-node:2::OnCopyNode
	#@+node:3::OnPasteNodee
	#@+body
	def OnPasteNode(self,event=None):
	
		self.commands.pasteOutline()
	
	#@-body
	#@-node:3::OnPasteNodee
	#@+node:4::OnDeleteNode
	#@+body
	def OnDeleteNode(self,event=None):
	
		self.commands.deleteHeadline()
	
	#@-body
	#@-node:4::OnDeleteNode
	#@+node:5::OnInsertNode
	#@+body
	def OnInsertNode(self,event=None):
	
		self.commands.insertHeadline()
	#@-body
	#@-node:5::OnInsertNode
	#@+node:6::OnCloneNode
	#@+body
	def OnCloneNode(self,event=None):
	
		self.commands.clone()
	
	#@-body
	#@-node:6::OnCloneNode
	#@+node:7::OnSortChildren, OnSortSiblings
	#@+body
	def OnSortChildren(self,event=None):
	
		self.commands.sortChildren()
		
	def OnSortSiblings(self,event=None):
	
		self.commands.sortSiblings()
	#@-body
	#@-node:7::OnSortChildren, OnSortSiblings
	#@-node:1::top level
	#@+node:2::Expand/Contract
	#@+node:1::No longer used
	#@+node:1::OnContractChildren (no longer used)
	#@+body
	def OnContractChildren(self,event=None):
	
		self.commands.contractSubheads()
	
	#@-body
	#@-node:1::OnContractChildren (no longer used)
	#@+node:2::OnContractAllChildren (no longer used)
	#@+body
	def OnContractAllChildren(self,event=None):
	
		self.commands.contractAllSubheads()
	
	#@-body
	#@-node:2::OnContractAllChildren (no longer used)
	#@+node:3::OnExpandAllChildren (no longer used)
	#@+body
	def OnExpandAllChildren(self,event=None):
	
		self.commands.expandAllSubheads()
	
	#@-body
	#@-node:3::OnExpandAllChildren (no longer used)
	#@+node:4::OnExpandChildren (no longer used)
	#@+body
	def OnExpandChildren(self,event=None):
	
		self.commands.expandSubheads()
	
	#@-body
	#@-node:4::OnExpandChildren (no longer used)
	#@-node:1::No longer used
	#@+node:2::OnContractAll
	#@+body
	def OnContractAll(self,event=None):
	
		self.commands.contractAllHeadlines()
	
	#@-body
	#@-node:2::OnContractAll
	#@+node:3::OnContractNode
	#@+body
	def OnContractNode(self,event=None):
	
		self.commands.contractNode()
	
	#@-body
	#@-node:3::OnContractNode
	#@+node:4::OnContractParent
	#@+body
	def OnContractParent(self,event=None):
	
		self.commands.contractParent()
	
	#@-body
	#@-node:4::OnContractParent
	#@+node:5::OnExpandAll
	#@+body
	def OnExpandAll(self,event=None):
	
		self.commands.expandAllHeadlines()
	
	#@-body
	#@-node:5::OnExpandAll
	#@+node:6::OnExpandNextLevel
	#@+body
	def OnExpandNextLevel(self,event=None):
	
		self.commands.expandNextLevel()
	
	#@-body
	#@-node:6::OnExpandNextLevel
	#@+node:7::OnExpandNode
	#@+body
	def OnExpandNode(self,event=None):
	
		self.commands.expandNode()
	
	#@-body
	#@-node:7::OnExpandNode
	#@+node:8::OnExpandPrevLevel
	#@+body
	def OnExpandPrevLevel(self,event=None):
	
		self.commands.expandPrevLevel()
	
	#@-body
	#@-node:8::OnExpandPrevLevel
	#@+node:9::OnExpandToLevel1..9
	#@+body
	def OnExpandToLevel1(self,event=None): self.commands.expandLevel1()
	def OnExpandToLevel2(self,event=None): self.commands.expandLevel2()
	def OnExpandToLevel3(self,event=None): self.commands.expandLevel3()
	def OnExpandToLevel4(self,event=None): self.commands.expandLevel4()
	def OnExpandToLevel5(self,event=None): self.commands.expandLevel5()
	def OnExpandToLevel6(self,event=None): self.commands.expandLevel6()
	def OnExpandToLevel7(self,event=None): self.commands.expandLevel7()
	def OnExpandToLevel8(self,event=None): self.commands.expandLevel8()
	def OnExpandToLevel9(self,event=None): self.commands.expandLevel9()
	
	#@-body
	#@-node:9::OnExpandToLevel1..9
	#@-node:2::Expand/Contract
	#@+node:3::Move/Select
	#@+node:1::OnMoveDownwn
	#@+body
	def OnMoveDown(self,event=None):
	
		self.commands.moveOutlineDown()
	
	#@-body
	#@-node:1::OnMoveDownwn
	#@+node:2::OnMoveLeft
	#@+body
	def OnMoveLeft(self,event=None):
	
		self.commands.moveOutlineLeft()
	
	#@-body
	#@-node:2::OnMoveLeft
	#@+node:3::OnMoveRight
	#@+body
	def OnMoveRight(self,event=None):
	
		self.commands.moveOutlineRight()
	
	#@-body
	#@-node:3::OnMoveRight
	#@+node:4::OnMoveUp
	#@+body
	def OnMoveUp(self,event=None):
	
		self.commands.moveOutlineUp()
	
	#@-body
	#@-node:4::OnMoveUp
	#@+node:5::OnPromote
	#@+body
	def OnPromote(self,event=None):
	
		self.commands.promote()
	
	#@-body
	#@-node:5::OnPromote
	#@+node:6::OnDemote
	#@+body
	def OnDemote(self,event=None):
	
		self.commands.demote()
	
	#@-body
	#@-node:6::OnDemote
	#@+node:7::OnGoPrevVisible
	#@+body
	def OnGoPrevVisible(self,event=None):
	
		self.commands.selectVisBack()
	
	#@-body
	#@-node:7::OnGoPrevVisible
	#@+node:8::OnGoNextVisible
	#@+body
	def OnGoNextVisible(self,event=None):
	
		self.commands.selectVisNext()
	
	#@-body
	#@-node:8::OnGoNextVisible
	#@+node:9::OnGoBack
	#@+body
	def OnGoBack(self,event=None):
	
		self.commands.selectThreadBack()
	
	#@-body
	#@-node:9::OnGoBack
	#@+node:10::OnGoNext
	#@+body
	def OnGoNext(self,event=None):
	
		self.commands.selectThreadNext()
	
	#@-body
	#@-node:10::OnGoNext
	#@-node:3::Move/Select
	#@+node:4::Mark/Goto
	#@+node:1::recentButtonCallback
	#@+body
	def recentButtonCallback(self,event=None):
		
		c = self.c ; d = self.recentSectionsDialog
		
		if d:
			d.top.deiconify()
			d.fillbox()
		else:
			# Create and run the dialog.]
			title = "Recent Nodes"
			label = "Recent nodes: " + shortFileName(c.frame.mFileName)
			d = leoDialog.recentSectionsDialog(c,self.nav_buttons,title,label)
			self.recentSectionsDialog = d
			d.root.wait_window(d.top)
	
	#@-body
	#@-node:1::recentButtonCallback
	#@+node:2::OnGoPrevVisitedNode
	#@+body
	def OnGoPrevVisitedNode(self,event=None):
		
		c = self.commands
	
		while c.beadPointer > 0:
			c.beadPointer -= 1
			v = c.beadList[c.beadPointer]
			if v.exists(c):
				c.beginUpdate()
				c.tree.expandAllAncestors(v)
				c.selectVnode(v,updateBeadList=false)
				c.endUpdate()
				c.tree.idle_scrollTo(v)
				return
	
	#@-body
	#@-node:2::OnGoPrevVisitedNode
	#@+node:3::OnGoNextVisitedNode
	#@+body
	def OnGoNextVisitedNode(self,event=None):
		
		c = self.commands
	
		while c.beadPointer + 1 < len(c.beadList):
			c.beadPointer += 1
			v = c.beadList[c.beadPointer]
			if v.exists(c):
				c.beginUpdate()
				c.tree.expandAllAncestors(v)
				c.selectVnode(v,updateBeadList=false)
				c.endUpdate()
				c.tree.idle_scrollTo(v)
				return
	#@-body
	#@-node:3::OnGoNextVisitedNode
	#@+node:4::OnGoToFirstNode
	#@+body
	def OnGoToFirstNode(self,event=None):
		
		c = self.commands
		v = c.rootVnode()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-body
	#@-node:4::OnGoToFirstNode
	#@+node:5::OnGoToLastNode
	#@+body
	def OnGoToLastNode(self,event=None):
		
		c = self.commands
		v = c.rootVnode()
		while v and v.threadNext():
			v = v.threadNext()
		if v:
			c.beginUpdate()
			c.tree.expandAllAncestors(v)
			c.selectVnode(v)
			c.endUpdate()
	
	#@-body
	#@-node:5::OnGoToLastNode
	#@+node:6::OnGoToNextChanged
	#@+body
	def OnGoToNextChanged(self,event=None):
	
		self.commands.goToNextDirtyHeadline()
	
	#@-body
	#@-node:6::OnGoToNextChanged
	#@+node:7::OnGoToNextClone
	#@+body
	def OnGoToNextClone(self,event=None):
	
		self.commands.goToNextClone()
	
	#@-body
	#@-node:7::OnGoToNextClone
	#@+node:8::OnGoToNextMarked
	#@+body
	def OnGoToNextMarked(self,event=None):
	
		self.commands.goToNextMarkedHeadline()
	
	#@-body
	#@-node:8::OnGoToNextMarked
	#@+node:9::OnGoToNextSibling
	#@+body
	def OnGoToNextSibling(self,event=None):
		
		c = self.commands
		v = c.currentVnode()
		if not v: return
		next = v.next()
		if next:
			c.beginUpdate()
			c.selectVnode(next)
			c.endUpdate()
	#@-body
	#@-node:9::OnGoToNextSibling
	#@+node:10::OnGoToParent
	#@+body
	def OnGoToParent(self,event=None):
		
		c = self.commands
		v = c.currentVnode()
		if not v: return
		p = v.parent()
		if p:
			c.beginUpdate()
			c.selectVnode(p)
			c.endUpdate()
	
	#@-body
	#@-node:10::OnGoToParent
	#@+node:11::OnGoToPrevSibling
	#@+body
	def OnGoToPrevSibling(self,event=None):
		
		c = self.commands
		v = c.currentVnode()
		if not v: return
		back = v.back()
		if back:
			c.beginUpdate()
			c.selectVnode(back)
			c.endUpdate()
	
	#@-body
	#@-node:11::OnGoToPrevSibling
	#@+node:12::OnMark
	#@+body
	def OnMark(self,event=None):
	
		self.commands.markHeadline()
	
	#@-body
	#@-node:12::OnMark
	#@+node:13::OnMarkChangedItems
	#@+body
	def OnMarkChangedItems(self,event=None):
	
		self.commands.markChangedHeadlines()
	
	#@-body
	#@-node:13::OnMarkChangedItems
	#@+node:14::OnMarkChangedRoots
	#@+body
	def OnMarkChangedRoots(self,event=None):
	
		self.commands.markChangedRoots()
	
	#@-body
	#@-node:14::OnMarkChangedRoots
	#@+node:15::OnMarkClones
	#@+body
	def OnMarkClones(self,event=None):
	
		self.commands.markClones()
	
	#@-body
	#@-node:15::OnMarkClones
	#@+node:16::OnMarkSubheads
	#@+body
	def OnMarkSubheads(self,event=None):
	
		self.commands.markSubheads()
	
	#@-body
	#@-node:16::OnMarkSubheads
	#@+node:17::OnUnmarkAll
	#@+body
	def OnUnmarkAll(self,event=None):
	
		self.commands.unmarkAll()
	
	#@-body
	#@-node:17::OnUnmarkAll
	#@-node:4::Mark/Goto
	#@-node:3::Outline Menu
	#@+node:4::Window Menu
	#@+node:1::OnEqualSizedPanes
	#@+body
	def OnEqualSizedPanes(self,event=None):
	
		frame = self
	
		frame.resizePanesToRatio(0.5,frame.secondary_ratio)
	
	#@-body
	#@-node:1::OnEqualSizedPanes
	#@+node:2::OnToggleActivePane
	#@+body
	def OnToggleActivePane (self,event=None):
	
		# trace(`event`)
		if self.getFocus() == self.body:
			self.canvas.focus_force()
		else:
			self.body.focus_force()
	#@-body
	#@-node:2::OnToggleActivePane
	#@+node:3::OnToggleSplitDirection
	#@+body
	# The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.
	
	def OnToggleSplitDirection(self,event=None):
		# Abbreviations.
		frame = self
		bar1 = self.bar1 ; bar2 = self.bar2
		split1Pane1,split1Pane2 = self.split1Pane1,self.split1Pane2
		split2Pane1,split2Pane2 = self.split2Pane1,self.split2Pane2
		# Switch directions.
		verticalFlag = self.splitVerticalFlag = not self.splitVerticalFlag
		orientation = choose(verticalFlag,"vertical","horizontal")
		app().config.setWindowPref("initial_splitter_orientation",orientation)
		# Reconfigure the bars.
		bar1.place_forget()
		bar2.place_forget()
		self.configureBar(bar1,verticalFlag)
		self.configureBar(bar2,not verticalFlag)
		# Make the initial placements again.
		self.placeSplitter(bar1,split1Pane1,split1Pane2,verticalFlag)
		self.placeSplitter(bar2,split2Pane1,split2Pane2,not verticalFlag)
		# Adjust the log and body panes to give more room around the bars.
		self.reconfigurePanes()
		# Redraw with an appropriate ratio.
		vflag,ratio,secondary_ratio = frame.initialRatios()
		self.resizePanesToRatio(ratio,secondary_ratio)
	#@-body
	#@-node:3::OnToggleSplitDirection
	#@+node:4::OnCascade
	#@+body
	def OnCascade(self,event=None):
		
		c = self ; x,y,delta = 10,10,10
		for frame in app().windowList:
			top = frame.top
			# Compute w,h
			top.update_idletasks() # Required to get proper info.
			geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
			dim,junkx,junky = string.split(geom,'+')
			w,h = string.split(dim,'x')
			w,h = int(w),int(h)
			# Set new x,y and old w,h
			frame.top.geometry("%dx%d%+d%+d" % (w,h,x,y))
			# Compute the new offsets.
			x += 30 ; y += 30
			if x > 200:
				x = 10 + delta ; y = 40 + delta
				delta += 10
	
	#@-body
	#@-node:4::OnCascade
	#@+node:5::OnMinimizeAll
	#@+body
	def OnMinimizeAll(self,event=None):
	
		self.minimize(app().findFrame)
		self.minimize(app().pythonFrame)
		for frame in app().windowList:
			self.minimize(frame)
		
	def minimize(self, frame):
	
		if frame and frame.top.state() == "normal":
			frame.top.iconify()
	#@-body
	#@-node:5::OnMinimizeAll
	#@+node:6::OnHideLogWindow
	#@+body
	def OnHideLogWindow (self):
		
		c = self.commands ; frame = c.frame
		frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)
	#@-body
	#@-node:6::OnHideLogWindow
	#@+node:7::OnOpenCompareWindow
	#@+body
	def OnOpenCompareWindow (self,event=None):
		
		c = self.commands
		cp = self.comparePanel
		
		if cp:
			cp.top.deiconify()
		else:
			cmp = leoCompare.leoCompare(c)
			self.comparePanel = cp =  leoCompare.leoComparePanel(c,cmp)
			cp.run()
	#@-body
	#@-node:7::OnOpenCompareWindow
	#@+node:8::OnOpenPythonWindow (Dave Hein)
	#@+body
	def OnOpenPythonWindow(self,event=None):
	
		if sys.platform == "linux2":
			
			#@<< open idle in Linux >>
			#@+node:1::<< open idle in Linux >>
			#@+body
			# 09-SEP-2002 DHEIN: Open Python window under linux
			
			try:
				pathToLeo = os.path.join(app().loadDir,"leo.py")
				sys.argv = [pathToLeo]
				from idlelib import idle
				if app().idle_imported:
					reload(idle)
				app().idle_imported = true
			except:
				try:
					es("idlelib could not be imported.")
					es("Probably IDLE is not installed.")
					es("Run Tools/idle/setup.py to build idlelib.")
					es("Can not import idle")
					es_exception() # This can fail!!
				except: pass
			
			#@-body
			#@-node:1::<< open idle in Linux >>

		else:
			
			#@<< open idle in Windows >>
			#@+node:2::<< open idle in Windows >>
			#@+body
			try:
				executable_dir = os.path.dirname(sys.executable)
				idle_dir=os.path.join(executable_dir,"Tools","idle")
				if idle_dir not in sys.path:
					sys.path.append(idle_dir)
				# Initialize argv: the -t option sets the title of the Idle interp window.
				# pathToLeo = os.path.join(app().loadDir,"leo.py")
				sys.argv = ["leo","-t","leo"]
				import PyShell
				if app().idle_imported:
					reload(idle)
					app().idle_imported = true
				if 1: # Mostly works, but causes problems when opening other .leo files.
					PyShell.main()
				else: # Doesn't work: destroys all of Leo when Idle closes.
					self.leoPyShellMain()
			except:
				try:
					es("Can not import idle")
					es("Please add " + `idle_dir` + " to sys.path")
					es_exception() # This can fail!!
				except: pass
			#@-body
			#@-node:2::<< open idle in Windows >>

	
	#@-body
	#@+node:3::leoPyShellMain
	#@+body
	#@+at
	#  The key parts of Pyshell.main(), but using Leo's root window instead of 
	# a new Tk root window.
	# 
	# This does _not_ work.  Using Leo's root window means that Idle will shut 
	# down Leo without warning when the Idle window is closed!

	#@-at
	#@@c

	def leoPyShellMain(self):
		
		import PyShell
		root = app().root
		PyShell.fixwordbreaks(root)
		flist = PyShell.PyShellFileList(root)
		shell = PyShell.PyShell(flist)
		flist.pyshell = shell
		shell.begin()
	#@-body
	#@-node:3::leoPyShellMain
	#@-node:8::OnOpenPythonWindow (Dave Hein)
	#@-node:4::Window Menu
	#@+node:5::Help Menu
	#@+node:1::OnAbout (version number & date)
	#@+body
	def OnAbout(self,event=None):
		
		# Don't use triple-quoted strings or continued strings here.
		# Doing so would add unwanted leading tabs.
		ver = "$Revision$" # CVS will update this.
		build = ver[10:-1] # Strip off "$Reversion" and "$"
		version = "leo.py 4.0 alpha 2, Build " + build + ", May 12, 2003\n\n"
		copyright = (
			"Copyright 1999-2003 by Edward K. Ream\n" +
			"All Rights Reserved\n" +
			"Leo is distributed under the Python License")
		url = "http://webpages.charter.net/edreamleo/front.html"
		email = "edreamleo@charter.net"
	
		if 1: # Much better looking and includes icon.
			import leoDialog
			d = leoDialog.leoDialog()
			d.aboutLeo(version,copyright,url,email)
		else:
			import tkMessageBox
			tkMessageBox.showinfo("About Leo",
				version + copyright + '\n' + url + '\n' + email)
	#@-body
	#@-node:1::OnAbout (version number & date)
	#@+node:2::OnLeoDocumentation
	#@+body
	def OnLeoDocumentation (self,event=None):
	
		fileName = os.path.join(app().loadDir,"..","doc","LeoDocs.leo")
		try:
			self.OpenWithFileName(fileName)
		except:
			es("not found: LeoDocs.leo")
	
	#@-body
	#@-node:2::OnLeoDocumentation
	#@+node:3::OnLeoHome
	#@+body
	def OnLeoHome (self,event=None):
		
		import webbrowser
		
		url = "http://personalpages.tds.net/~edream/front.html"
		try:
			webbrowser.open_new(url)
		except:
			es("not found: " + url)
	#@-body
	#@-node:3::OnLeoHome
	#@+node:4::OnLeoHelp
	#@+body
	def OnLeoHelp (self,event=None):
		
		file = os.path.join(app().loadDir,"..","doc","sbooks.chm")
		if os.path.exists(file):
			os.startfile(file)
		else:
			d = leoDialog.leoDialog()
			answer = d.askYesNo(
				"Download Tutorial?",
				"Download tutorial (sbooks.chm) from SourceForge?")
			if answer == "yes":
				try:
					if 0: # Download directly.  (showProgressBar needs a lot of work)
						url = "http://umn.dl.sourceforge.net/sourceforge/leo/sbooks.chm"
						import urllib
						self.scale = None
						urllib.urlretrieve(url,file,self.showProgressBar)
						if self.scale:
							self.scale.destroy()
							self.scale = None
					else:
						url = "http://prdownloads.sourceforge.net/leo/sbooks.chm?download"
						import webbrowser
						os.chdir(app().loadDir)
						webbrowser.open_new(url)
				except:
					es("exception dowloading sbooks.chm")
					es_exception()
	#@-body
	#@+node:1::showProgressBar
	#@+body
	def showProgressBar (self,count,size,total):
	
		# trace("count,size,total:" + `count` + "," + `size` + "," + `total`)
		if self.scale == None:
			
			#@<< create the scale widget >>
			#@+node:1::<< create the scale widget >>
			#@+body
			Tk = Tkinter
			top = Tk.Toplevel()
			top.title("Download progress")
			self.scale = scale = Tk.Scale(top,state="normal",orient="horizontal",from_=0,to=total)
			scale.pack()
			top.lift()
			#@-body
			#@-node:1::<< create the scale widget >>

		self.scale.set(count*size)
		self.scale.update_idletasks()
	#@-body
	#@-node:1::showProgressBar
	#@-node:4::OnLeoHelp
	#@+node:5::OnLeoTutorial (version number)
	#@+body
	def OnLeoTutorial (self,event=None):
		
		import webbrowser
	
		if 1: # new url
			url = "http://www.3dtree.com/ev/e/sbooks/leo/sbframetoc_ie.htm"
		else:
			url = "http://www.evisa.com/e/sbooks/leo/sbframetoc_ie.htm"
		try:
			webbrowser.open_new(url)
		except:
			es("not found: " + url)
	#@-body
	#@-node:5::OnLeoTutorial (version number)
	#@+node:6::OnLeoConfig, OnApplyConfig
	#@+body
	def OnLeoConfig (self,event=None):
	
		# 4/21/03 new code suggested by fBechmann@web.de
		loadDir = app().loadDir
		configDir = app().config.configDir
		# Look in configDir first.
		fileName = os.path.join(configDir, "leoConfig.leo")
		ok, frame = self.OpenWithFileName(fileName)
		if not ok:
			if configDir == loadDir:
				es("leoConfig.leo not found in " + loadDir)
			else:
				# Look in loadDir second.
				fileName = os.path.join(loadDir,"leoConfig.leo")
				ok, frame = self.OpenWithFileName(fileName)
				if not ok:
					es("leoConfig.leo not found in " + configDir + " or " + loadDir)
		
	def OnApplyConfig (self,event=None):
	
		app().config.init()
		self.commands.frame.reconfigureFromConfig()
	#@-body
	#@-node:6::OnLeoConfig, OnApplyConfig
	#@-node:5::Help Menu
	#@-node:7::Menu Command Handlers
	#@+node:8::Menu Convenience Routines
	#@+body
	#@+at
	#  The following convenience routines make creating menus easier.
	# 
	# The Plugins section gives examples of how to use these routines to 
	# create custom menus and to add items to the Open With menu.

	#@-at
	#@-body
	#@+node:1::createMenuItemsFromTable
	#@+body
	def createMenuItemsFromTable (self,menuName,table,openWith=0):
		
		try:
			menu = self.getMenu(menuName)
			if menu == None:
				print "menu does not exist: ", menuName
				es("menu does not exist: " + `menuName`)
				return
			self.createMenuEntries(menu,table,openWith)
		except:
			print "exception creating items for ", menuName," menu"
			es("exception creating items for " + `menuName` + " menu")
			es_exception()
	#@-body
	#@-node:1::createMenuItemsFromTable
	#@+node:2::createNewMenu
	#@+body
	def createNewMenu (self,menuName,parentName="top",before=None):
		
		import Tkinter
		from leoGlobals import app
		try:
			parent = self.getMenu(parentName)
			if parent == None:
				es("unknown parent menu: " + parentName)
				return None
				
			menu = self.getMenu(menuName)
			if menu:
				es("menu already exists: " + menuName,color="red")
			else:
				menu = Tkinter.Menu(parent,tearoff=0)
				self.setMenu(menuName,menu)
				label=app().getRealMenuName(menuName)
				amp_index = label.find("&")
				label = label.replace("&","")
				if before: # Insert the menu before the "before" menu.
					index_label=app().getRealMenuName(before)
					amp_index = index_label.find("&")
					index_label = index_label.replace("&","")
					index = parent.index(index_label)
					parent.insert_cascade(index=index,label=label,menu=menu,underline=amp_index)
				else:
					parent.add_cascade(label=label,menu=menu,underline=amp_index)
				return menu
		except:
			es("exception creating " + menuName + " menu")
			es_exception()
			return None
	#@-body
	#@-node:2::createNewMenu
	#@+node:3::createOpenWithMenuFromTable
	#@+body
	#@+at
	#  Entries in the table passed to createOpenWithMenuFromTable are
	# tuples of the form (commandName,shortcut,data).
	# 
	# - command is one of "os.system", "os.startfile", "os.spawnl", 
	# "os.spawnv" or "exec".
	# - shortcut is a string describing a shortcut, just as for createMenuItemsFromTable.
	# - data is a tuple of the form (command,arg,ext).
	# 
	# Leo executes command(arg+path) where path is the full path to the temp file.
	# If ext is not None, the temp file has the given extension.
	# Otherwise, Leo computes an extension based on the @language directive in effect.

	#@-at
	#@@c

	def createOpenWithMenuFromTable (self,table):
	
		a = app()
		a.openWithTable = table # Override any previous table.
		# Delete the previous entry.
		parent = self.getMenu("File")
		label=a.getRealMenuName("Open &With...")
		amp_index = label.find("&")
		label = label.replace("&","")
		try:
			index = parent.index(label)
			parent.delete(index)
		except:
			try:
				index = parent.index("Open With...")
				parent.delete(index)
			except: return
		# Create the "Open With..." menu.
		openWithMenu = Tkinter.Menu(parent,tearoff=0)
		self.setMenu("Open With...",openWithMenu)
		parent.insert_cascade(index,label=label,menu=openWithMenu,underline=amp_index)
		# Populate the "Open With..." menu.
		shortcut_table = []
		for name,shortcut,data in table:
			try:
				data2 = (name,shortcut,data)
				shortcut_table.append(data2)
			except:
				es("createOpenWithMenuFromTable: invalid data")
				return
		# for i in shortcut_table: print i
		self.createMenuItemsFromTable("Open &With...",shortcut_table,openWith=1)
	
	#@-body
	#@-node:3::createOpenWithMenuFromTable
	#@+node:4::deleteMenu
	#@+body
	def deleteMenu (self,menuName):
	
		try:
			menu = self.getMenu(menuName)
			if menu:
				menu.destroy()
				self.destroyMenu(menuName)
			else:
				es("can't delete menu: " + menuName)
		except:
			es("exception deleting " + menuName + " menu")
			es_exception()
	#@-body
	#@-node:4::deleteMenu
	#@+node:5::deleteMenuItem
	#@+body
	# Delete itemName from the menu whose name is menuName.
	def deleteMenuItem (self,itemName,menuName="top"):
	
		from leoGlobals import app
		try:
			menu = self.getMenu(menuName)
			if menu:
				realItemName=app().getRealMenuName(itemName)
				menu.delete(realItemName)
			else:
				es("menu not found: " + menuName)
		except:
			es("exception deleting " + itemName + " from " + menuName + " menu")
			es_exception()
	#@-body
	#@-node:5::deleteMenuItem
	#@+node:6::setRealMenuNamesFromTable
	#@+body
	def setRealMenuNamesFromTable (self,table):
	
		try:
			app().setRealMenuNamesFromTable(table)
		except:
			es("exception in setRealMenuNamesFromTable")
			es_exception()
	
	#@-body
	#@-node:6::setRealMenuNamesFromTable
	#@-node:8::Menu Convenience Routines
	#@+node:9::Menu enablers (Frame)
	#@+node:1::frame.OnMenuClick (enables and disables all menu items)
	#@+body
	# This is the Tk "postcommand" callback.  It should update all menu items.
	
	def OnMenuClick (self):
		
		# A horrible kludge: set app().log to cover for a possibly missing activate event.
		app().log = self
		
		# Allow the user first crack at updating menus.
		c = self.commands ; v = c.currentVnode() # 2/8/03
		if not doHook("menu2",c=c,v=v):
			self.updateFileMenu()
			self.updateEditMenu()
			self.updateOutlineMenu()
	
	#@-body
	#@-node:1::frame.OnMenuClick (enables and disables all menu items)
	#@+node:2::hasSelection
	#@+body
	# Returns true if text in the outline or body text is selected.
	
	def hasSelection (self):
	
		if self.body:
			first, last = getTextSelection(self.body)
			return first != last
		else:
			return false
	#@-body
	#@-node:2::hasSelection
	#@+node:3::updateFileMenu
	#@+body
	def updateFileMenu (self):
		
		c = self.commands
		if not c: return
	
		try:
			menu = self.getMenu("File")
			enableMenu(menu,"Revert To Saved", c.canRevert())
				
			openWithMenu = self.getMenu("Open With...")
			enableMenu(menu,"Open With...", openWithMenu != None)
		except:
			es("exception updating File menu")
			es_exception()
	
	#@-body
	#@-node:3::updateFileMenu
	#@+node:4::updateEditMenu
	#@+body
	def updateEditMenu (self):
	
		c = self.commands
		if not c: return
		try:
			# Top level Edit menu...
			menu = self.getMenu("Edit")
			c.undoer.enableMenuItems()
			if 0: # Always on for now.
				enableMenu(menu,"Cut",c.canCut())
				enableMenu(menu,"Copy",c.canCut())
				enableMenu(menu,"Paste",c.canPaste())
			if 0: # Always on for now.
				menu = self.getMenu("Find...")
				enableMenu(menu,"Find Next",c.canFind())
				flag = c.canReplace()
				enableMenu(menu,"Replace",flag)
				enableMenu(menu,"Replace, Then Find",flag)
			# Edit Body submenu...
			menu = self.getMenu("Edit Body...")
			enableMenu(menu,"Extract Section",c.canExtractSection())
			enableMenu(menu,"Extract Names",c.canExtractSectionNames())
			enableMenu(menu,"Extract",c.canExtract())
			enableMenu(menu,"Match Brackets",c.canFindMatchingBracket())
		except:
			es("exception updating Edit menu")
			es_exception()
	#@-body
	#@-node:4::updateEditMenu
	#@+node:5::updateOutlineMenu
	#@+body
	def updateOutlineMenu (self):
	
		c = self.commands ; v = c.currentVnode()
		if not c: return
		try:
			# Top level outline menu...
			menu = self.getMenu("Outline")
			enableMenu(menu,"Cut Node",c.canCutOutline())
			enableMenu(menu,"Delete Node",c.canDeleteHeadline())
			enableMenu(menu,"Paste Node",c.canPasteOutline())
			enableMenu(menu,"Sort Siblings",c.canSortSiblings())
			# Expand/Contract submenu...
			menu = self.getMenu("Expand/Contract...")
			hasChildren = v.hasChildren()
			isExpanded = v.isExpanded()
			enableMenu(menu,"Contract Parent",c.canContractParent())
			enableMenu(menu,"Contract Node",hasChildren and isExpanded)
			enableMenu(menu,"Expand Node",hasChildren and not isExpanded)
			enableMenu(menu,"Expand Prev Level",hasChildren and isExpanded)
			enableMenu(menu,"Expand Next Level",hasChildren)
			enableMenu(menu,"Expand To Level 1",hasChildren and isExpanded)
			for i in xrange(2,9):
				enableMenu(menu,"Expand To Level " + str(i), hasChildren)
			# Move submenu...
			menu = self.getMenu("Move...")
			enableMenu(menu,"Move Down",c.canMoveOutlineDown())
			enableMenu(menu,"Move Left",c.canMoveOutlineLeft())
			enableMenu(menu,"Move Right",c.canMoveOutlineRight())
			enableMenu(menu,"Move Up",c.canMoveOutlineUp())
			enableMenu(menu,"Promote",c.canPromote())
			enableMenu(menu,"Demote",c.canDemote())
			# Go To submenu
			menu = self.getMenu("Go To...")
			enableMenu(menu,"Go Back",c.beadPointer > 1)
			enableMenu(menu,"Go Forward",c.beadPointer + 1 < len(c.beadList))
			enableMenu(menu,"Go To Prev Visible",c.canSelectVisBack())
			enableMenu(menu,"Go To Next Visible",c.canSelectVisNext())
			enableMenu(menu,"Go To Next Marked",c.canGoToNextMarkedHeadline())
			enableMenu(menu,"Go To Next Changed",c.canGoToNextDirtyHeadline())
			enableMenu(menu,"Go To Next Clone",v.isCloned())
			enableMenu(menu,"Go To Prev Node",c.canSelectThreadBack())
			enableMenu(menu,"Go To Next Node",c.canSelectThreadNext())
			enableMenu(menu,"Go To Parent",v.parent() != None)
			enableMenu(menu,"Go To Prev Sibling",v.back() != None)
			enableMenu(menu,"Go To Next Sibling",v.next() != None)
			# Mark submenu
			menu = self.getMenu("Mark/Unmark...")
			label = choose(v and v.isMarked(),"Unmark","Mark")
			setMenuLabel(menu,0,label)
			enableMenu(menu,"Mark Subheads",(v and v.hasChildren()))
			enableMenu(menu,"Mark Changed Items",c.canMarkChangedHeadlines())
			enableMenu(menu,"Mark Changed Roots",c.canMarkChangedRoots())
			enableMenu(menu,"Mark Clones",v.isCloned())
		except:
			es("exception updating Outline menu")
			es_exception()
	#@-body
	#@-node:5::updateOutlineMenu
	#@-node:9::Menu enablers (Frame)
	#@-node:8::Menus
	#@+node:9::notYet
	#@+body
	def notYet(self,name):
	
		es(name + " not ready yet")
	
	#@-body
	#@-node:9::notYet
	#@+node:10::Splitter stuff
	#@+body
	#@+at
	#  The key invariants used throughout this code:
	# 
	# 1. self.splitVerticalFlag tells the alignment of the main splitter and
	# 2. not self.splitVerticalFlag tells the alignment of the secondary splitter.
	# 
	# Only the general-purpose divideAnySplitter routine doesn't know about 
	# these invariants.  So most of this code is specialized for Leo's 
	# window.  OTOH, creating a single splitter window would be much easier 
	# than this code.

	#@-at
	#@-body
	#@+node:1::resizePanesToRatio
	#@+body
	def resizePanesToRatio(self,ratio,secondary_ratio):
	
		self.divideLeoSplitter(self.splitVerticalFlag, ratio)
		self.divideLeoSplitter(not self.splitVerticalFlag, secondary_ratio)
		# trace(`ratio`)
	
	#@-body
	#@-node:1::resizePanesToRatio
	#@+node:2::bindBar
	#@+body
	def bindBar (self, bar, verticalFlag):
		
		if verticalFlag == self.splitVerticalFlag:
			bar.bind("<B1-Motion>", self.onDragMainSplitBar)
		else:
			bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)
	#@-body
	#@-node:2::bindBar
	#@+node:3::createLeoSplitter
	#@+body
	# 5/20/03: Removed the ancient kludge for forcing the height & width of f.
	# The code in leoFileCommands.getGlobals now works!
	
	def createLeoSplitter (self, parent, verticalFlag):
		
		"""Create a splitter window and panes into which the caller packs widgets.
		
		Returns (f, bar, pane1, pane2) """
	
		Tk = Tkinter
		
		# Create the frames.
		f = Tk.Frame(parent,bd=0,relief="flat")
		f.pack(expand=1,fill="both",pady=1)
		pane1 = Tk.Frame(f)
		pane2 = Tk.Frame(f)
		bar =   Tk.Frame(f,bd=2,relief="raised",bg="LightSteelBlue2")
	
		# Configure and place the frames.
		self.configureBar(bar,verticalFlag)
		self.bindBar(bar,verticalFlag)
		self.placeSplitter(bar,pane1,pane2,verticalFlag)
	
		return f, bar, pane1, pane2
	#@-body
	#@-node:3::createLeoSplitter
	#@+node:4::divideAnySplitter
	#@+body
	# This is the general-purpose placer for splitters.
	# It is the only general-purpose splitter code in Leo.
	
	def divideAnySplitter (self, frac, verticalFlag, bar, pane1, pane2):
	
		if verticalFlag:
			# Panes arranged vertically; horizontal splitter bar
			bar.place(rely=frac)
			pane1.place(relheight=frac)
			pane2.place(relheight=1-frac)
		else:
			# Panes arranged horizontally; vertical splitter bar
			bar.place(relx=frac)
			pane1.place(relwidth=frac)
			pane2.place(relwidth=1-frac)
	#@-body
	#@-node:4::divideAnySplitter
	#@+node:5::divideLeoSplitter
	#@+body
	# Divides the main or secondary splitter, using the key invariant.
	def divideLeoSplitter (self, verticalFlag, frac):
		if self.splitVerticalFlag == verticalFlag:
			self.divideLeoSplitter1(frac,verticalFlag)
			self.ratio = frac # Ratio of body pane to tree pane.
		else:
			self.divideLeoSplitter2(frac,verticalFlag)
			self.secondary_ratio = frac # Ratio of tree pane to log pane.
	
	# Divides the main splitter.
	def divideLeoSplitter1 (self, frac, verticalFlag): 
		self.divideAnySplitter(frac, verticalFlag,
			self.bar1, self.split1Pane1, self.split1Pane2)
	
	# Divides the secondary splitter.
	def divideLeoSplitter2 (self, frac, verticalFlag): 
		self.divideAnySplitter (frac, verticalFlag,
			self.bar2, self.split2Pane1, self.split2Pane2)
	#@-body
	#@-node:5::divideLeoSplitter
	#@+node:6::initialRatios
	#@+body
	def initialRatios (self):
	
		config = app().config
		s = config.getWindowPref("initial_splitter_orientation")
		verticalFlag = s == None or (s != "h" and s != "horizontal")
	
		if verticalFlag:
			r = config.getFloatWindowPref("initial_vertical_ratio")
			if r == None or r < 0.0 or r > 1.0: r = 0.5
			r2 = config.getFloatWindowPref("initial_vertical_secondary_ratio")
			if r2 == None or r2 < 0.0 or r2 > 1.0: r2 = 0.8
		else:
			r = config.getFloatWindowPref("initial_horizontal_ratio")
			if r == None or r < 0.0 or r > 1.0: r = 0.3
			r2 = config.getFloatWindowPref("initial_horizontal_secondary_ratio")
			if r2 == None or r2 < 0.0 or r2 > 1.0: r2 = 0.8
	
		# print (`r`,`r2`)
		return verticalFlag,r,r2
	#@-body
	#@-node:6::initialRatios
	#@+node:7::onDrag...
	#@+body
	def onDragMainSplitBar (self, event):
		self.onDragSplitterBar(event,self.splitVerticalFlag)
		
	def onDragSecondarySplitBar (self, event):
		self.onDragSplitterBar(event,not self.splitVerticalFlag)
	
	def onDragSplitterBar (self, event, verticalFlag):
	
		# x and y are the coordinates of the cursor relative to the bar, not the main window.
		bar = event.widget
		x = event.x
		y = event.y
		top = bar.winfo_toplevel()
	
		if verticalFlag:
			# Panes arranged vertically; horizontal splitter bar
			wRoot	= top.winfo_rooty()
			barRoot = bar.winfo_rooty()
			wMax	= top.winfo_height()
			offset = float(barRoot) + y - wRoot
		else:
			# Panes arranged horizontally; vertical splitter bar
			wRoot	= top.winfo_rootx()
			barRoot = bar.winfo_rootx()
			wMax	= top.winfo_width()
			offset = float(barRoot) + x - wRoot
	
		# Adjust the pixels, not the frac.
		if offset < 3: offset = 3
		if offset > wMax - 2: offset = wMax - 2
		# Redraw the splitter as the drag is occuring.
		frac = float(offset) / wMax
		# trace(`frac`)
		self.divideLeoSplitter(verticalFlag, frac)
	#@-body
	#@-node:7::onDrag...
	#@+node:8::placeSplitter
	#@+body
	def placeSplitter (self,bar,pane1,pane2,verticalFlag):
	
		if verticalFlag:
			# Panes arranged vertically; horizontal splitter bar
			pane1.place(relx=0.5, rely =   0, anchor="n", relwidth=1.0, relheight=0.5)
			pane2.place(relx=0.5, rely = 1.0, anchor="s", relwidth=1.0, relheight=0.5)
			bar.place  (relx=0.5, rely = 0.5, anchor="c", relwidth=1.0)
		else:
			# Panes arranged horizontally; vertical splitter bar
			# adj gives tree pane more room when tiling vertically.
			adj = choose(verticalFlag != self.splitVerticalFlag,0.65,0.5)
			pane1.place(rely=0.5, relx =   0, anchor="w", relheight=1.0, relwidth=adj)
			pane2.place(rely=0.5, relx = 1.0, anchor="e", relheight=1.0, relwidth=1.0-adj)
			bar.place  (rely=0.5, relx = adj, anchor="c", relheight=1.0)
	#@-body
	#@-node:8::placeSplitter
	#@-node:10::Splitter stuff
	#@+node:11::Status line: convenience routines
	#@+body
	#@@tabwidth 4
	#@-body
	#@+node:1::createStatusLine
	#@+body
	def createStatusLine (self):
		
		if self.statusFrame and self.statusLabel:
			return
		
		self.statusFrame = statusFrame = Tk.Frame(self.outerFrame,bd=2)
		statusFrame.pack(fill="x",pady=1)
		
		text = "line 0, col 0"
		width = len(text) + 4
		self.statusLabel = Tk.Label(statusFrame,text=text,width=width,anchor="w")
		self.statusLabel.pack(side="left",padx=1)
		
		bg = statusFrame.cget("background")
		self.statusText = Tk.Text(statusFrame,height=1,state="disabled",bg=bg,relief="groove") # Text panes are much more flexible.
		self.statusText.pack(side="left",expand=1,fill="x")
		
		def idleStatusUpdateCallback(tag,keywords):
			c=keywords.get("c")
			if c: c.frame.updateStatusRowCol()
		
		# Register an idle-time handler to update the row and column indicators.
		leoPlugins.registerHandler("idle",idleStatusUpdateCallback)
	
	#@-body
	#@-node:1::createStatusLine
	#@+node:2::clearStatusLine
	#@+body
	def clearStatusLine (self):
		
		t = self.statusText
		t.configure(state="normal")
		t.delete("1.0","end")
		t.configure(state="disabled")
	
	#@-body
	#@-node:2::clearStatusLine
	#@+node:3::putStatusLine
	#@+body
	def putStatusLine (self,s,color=None):
		
		t = self.statusText ; tags = self.statusColorTags
		if not t: return
	
		t.configure(state="normal")
		
		if "black" not in self.logColorTags:
			tags.append("black")
			
		if color and color not in tags:
			tags.append(color)
			t.tag_config(color,foreground=color)
	
		if color:
			t.insert("end",s)
			t.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
			t.tag_config("black",foreground="black")
			t.tag_add("black","end")
		else:
			t.insert("end",s)
		
		t.configure(state="disabled")
	#@-body
	#@-node:3::putStatusLine
	#@+node:4::updateStatusRowCol()
	#@+body
	# This is a hook routine, so it must have the tag and keyword arguments.
	
	def updateStatusRowCol (self):
		
		c = self.commands ; body = self.body ; lab = self.statusLabel
	
		index = body.index("insert")
		row,col = getindex(body,index)
		if col > 0:
			s = body.get("%d.0" % (row),index)
			col = computeWidth (s,self.tab_width)
	
		if row != self.lastStatusRow or col != self.lastStatusCol:
			s = "line %d, col %d " % (row,col)
			lab.configure(text=s)
			self.lastStatusRow = row
			self.lastStatusCol = col
	
	#@-body
	#@-node:4::updateStatusRowCol()
	#@-node:11::Status line: convenience routines
	#@-others
#@-body
#@-node:0::@file leoFrame.py
#@-leo
