#@+leo-ver=4
#@+node:@file leoFrame.py
# To do: Use config params for window height, width and bar color, relief and width.

#@@language python

__pychecker__ = 'argumentsused=0' # Pychecker param.

from leoGlobals import *
import leoColor,leoCommands,leoCompare,leoDialog,leoFontPanel,leoNodes,leoPlugins,leoPrefs,leoTree
import os,string,sys,tempfile,time,traceback
import Tkinter,tkFileDialog,tkFont

Tk = Tkinter

class baseLeoFrame:
	"""A base class for Leo's main frame class."""
	instances = 0
	#@	@+others
	#@+node:f.__init__
	def __init__(self,title):
	
		# trace("LeoFrame")
	
		self.title = title
		LeoFrame.instances += 1
	
		#@	<< set the LeoFrame ivars >>
		#@+node:<< set the LeoFrame ivars >>
		self.stylesheet = None # The contents of <?xml-stylesheet...?> line.
		
		# These are set the first time a panel is opened.
		# The panel remains open (perhaps hidden) until this frame is closed.
		self.colorPanel = None 
		self.fontPanel = None 
		self.prefsPanel = None
		self.comparePanel = None
			
		self.outlineToNowebDefaultFileName = "noweb.nw" # For Outline To Noweb dialog.
		self.saved=false # True if ever saved
		self.startupWindow=false # True if initially opened window
		self.openDirectory = ""
		self.es_newlines = 0 # newline count for this log stream
		
		self.splitVerticalFlag,self.ratio,self.secondary_ratio = self.initialRatios()
		
		# Created in createLeoFrame and its allies.
		self.tree = None
		self.f1 = self.f2 = None
		self.log = None  ; self.logBar = None
		self.body = None ; self.bodyBar = None ; self.bodyXBar = None
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
		self.draggedItem = None
		self.recentFiles = [] # List of recent files
		self.controlKeyIsDown = false # For control-drags
		
		# Colors of log pane.
		self.logColorTags = [] # list of color names used as tags in log window.
		self.statusColorTags = [] # list of color names used as tags in status window.
		
		# Previous row and column shown in the status area.
		self.lastStatusRow = self.lastStatusCol = 0
		self.tab_width = 0 # The tab width in effect in this pane.
		#@nonl
		#@-node:<< set the LeoFrame ivars >>
		#@nl
		
		self.initVersion()
	#@-node:f.__init__
	#@+node:f.version & signon stuff
	def getBuildNumber(self):
		return self.ver[10:-1] # Strip off "$Reversion" and the trailing "$"
	
	def getSignOnLine (self):
		return "Leo 4.0 beta 3 build %s, October 9, 2003" % self.getBuildNumber()
		
	def initVersion (self):
		self.ver = "$Revision$" # CVS will update this.
		
	def signOnWithVersion (self):
	
		frame = self
		color = app.config.getWindowPref("log_error_color")
		signon = frame.getSignOnLine()
		n1,n2,n3,junk,junk=sys.version_info
		tkLevel = frame.top.getvar("tk_patchLevel")
		
		es("Leo Log Window...",color=color)
		es(signon)
		es("Python %d.%d.%d, Tk %s" % (n1,n2,n3,tkLevel))
		enl()
	#@nonl
	#@-node:f.version & signon stuff
	#@+node:f.finishCreate
	def finishCreate (self,c):
		
		frame = self ; frame.commands = c ; Tk = Tkinter
		
		# Create the toplevel.
		frame.top = top = Tk.Toplevel()
		attachLeoIcon(top)
		top.title(frame.title)
		top.minsize(30,10) # In grid units.
	
		# Create all the subframes.
		frame.createLeoFrame(top)
		c.body = frame.body ## To be deleted.
		frame.tree = leoTree.leoTree(c,frame,frame.canvas)
		frame.setTabWidth(c.tab_width)
	
		#@	<< create the first tree node >>
		#@+node:<< create the first tree node >>
		t = leoNodes.tnode()
		v = leoNodes.vnode(c,t)
		v.initHeadString("NewHeadline")
		v.moveToRoot()
		
		c.beginUpdate()
		c.frame.redraw()
		c.frame.focus_get()
		c.editVnode(v)
		c.endUpdate(false)
		#@nonl
		#@-node:<< create the first tree node >>
		#@nl
		v = c.currentVnode()
		
		if not doHook("menu1",c=c,v=v):
			frame.createMenuBar(top)
		app.setLog(frame,"frame.__init__") # the LeoFrame containing the log
		app.windowList.append(frame)
		
		self.signOnWithVersion()
		
		frame.top.protocol("WM_DELETE_WINDOW", frame.OnCloseLeoEvent)
		frame.top.bind("<Button-1>", frame.OnActivateLeoEvent)
		
		frame.top.bind("<Activate>", frame.OnActivateLeoEvent) # Doesn't work on windows.
		frame.top.bind("<Deactivate>", frame.OnDeactivateLeoEvent) # Doesn't work on windows.
	
		frame.top.bind("<Control-KeyPress>",frame.OnControlKeyDown)
		frame.top.bind("<Control-KeyRelease>",frame.OnControlKeyUp)
		
		frame.tree.canvas.bind("<Button-1>", frame.OnActivateTree)
		frame.log.bind("<Button-1>", frame.OnActivateLog)
		
		frame.body.bind("<Button-1>", frame.OnBodyClick)
		frame.body.bind("<Button-3>", frame.OnBodyRClick)
		frame.body.bind("<Double-Button-1>", frame.OnBodyDoubleClick)
		frame.body.bind("<Key>", frame.tree.OnBodyKey)
	
		frame.body.bind(virtual_event_name("Cut"), frame.OnCut)
		frame.body.bind(virtual_event_name("Copy"), frame.OnCopy)
		frame.body.bind(virtual_event_name("Paste"), frame.OnPaste)
	
		# Handle mouse wheel in the outline pane.
		if sys.platform == "linux2": # This crashes tcl83.dll
			frame.tree.canvas.bind("<MouseWheel>", frame.OnMouseWheel)
			
		# print_bindings("canvas",frame.tree.canvas)
	#@-node:f.finishCreate
	#@+node:f.__repr__
	def __repr__ (self):
	
		return "<leoFrame: %s>" % self.title
	#@-node:f.__repr__
	#@+node:f.clearAllIvars
	def clearAllIvars(self):
		
		"""Clear all ivars in helper classes."""
	
		frame = self
		clearAllIvars(frame.tree.colorizer)
		clearAllIvars(frame.tree)
	#@nonl
	#@-node:f.clearAllIvars
	#@+node:f.createLeoFrame
	def createLeoFrame (self,top):
	
		Tk = Tkinter ; config = app.config
		
		self.outerFrame = outerFrame = Tk.Frame(top)
		self.outerFrame.pack(expand=1,fill="both")
	
		self.createIconBar()
		#@	<< create both splitters >>
		#@+node:<< create both splitters >>
		# Splitter 1 is the main splitter containing splitter2 and the body pane.
		f1,bar1,split1Pane1,split1Pane2 = self.createLeoSplitter(outerFrame, self.splitVerticalFlag)
		self.f1,self.bar1 = f1,bar1
		self.split1Pane1,self.split1Pane2 = split1Pane1,split1Pane2
		# Splitter 2 is the secondary splitter containing the tree and log panes.
		f2,bar2,split2Pane1,split2Pane2 = self.createLeoSplitter(split1Pane1, not self.splitVerticalFlag)
		self.f2,self.bar2 = f2,bar2
		self.split2Pane1,self.split2Pane2 = split2Pane1,split2Pane2
		#@nonl
		#@-node:<< create both splitters >>
		#@nl
		#@	<< create the body pane >>
		#@+node:<< create the body pane >>
		# A light selectbackground value is needed to make syntax coloring look good.
		wrap = config.getBoolWindowPref('body_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		# Setgrid=1 cause severe problems with the font panel.
		self.body = body = Tk.Text(split1Pane2,name='body',
			bd=2,bg="white",relief="flat",
			setgrid=0,wrap=wrap, selectbackground="Gray80") 
		self.setBodyFontFromConfig()
		
		self.bodyBar = bodyBar = Tk.Scrollbar(split1Pane2,name='bodyBar')
		body['yscrollcommand'] = bodyBar.set
		bodyBar['command'] = body.yview
		bodyBar.pack(side="right", fill="y")
		
		# 8/30/03: Always create the horizontal bar.
		self.bodyXBar = bodyXBar = Tk.Scrollbar(
			split1Pane2,name='bodyXBar',orient="horizontal")
		body['xscrollcommand'] = bodyXBar.set
		bodyXBar['command'] = body.xview
		
		if wrap == "none":
			bodyXBar.pack(side="bottom", fill="x")
			
		body.pack(expand=1, fill="both")
		#@nonl
		#@-node:<< create the body pane >>
		#@nl
		#@	<< create the tree pane >>
		#@+node:<< create the tree pane >>
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
			
		tree['yscrollcommand'] = self.setCallback
		treeBar['command']     = self.yviewCallback
		
		treeBar.pack(side="right", fill="y")
		if scrolls: 
			treeXBar = Tk.Scrollbar( 
				split2Pane1,name='treeXBar',orient="horizontal") 
			tree['xscrollcommand'] = treeXBar.set 
			treeXBar['command'] = tree.xview 
			treeXBar.pack(side="bottom", fill="x")
		tree.pack(expand=1,fill="both")
		#@nonl
		#@-node:<< create the tree pane >>
		#@nl
		#@	<< create the log pane >>
		#@+node:<< create the log pane >>
		wrap = config.getBoolWindowPref('log_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		self.log = log = Tk.Text(split2Pane2,name="log",
			setgrid=0,wrap=wrap,bd=2,bg="white",relief="flat")
			
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
		#@nonl
		#@-node:<< create the log pane >>
		#@nl
		self.reconfigurePanes()
		
		self.createStatusLine()
		self.putStatusLine("Welcome to Leo")
	#@-node:f.createLeoFrame
	#@+node:frame.destroyAllPanels
	def destroyAllPanels (self):
		
		"""Destroy all panels attached to this frame."""
		
		panels = (self.comparePanel, self.colorPanel, self.fontPanel, self.prefsPanel)
	
		for panel in panels:
			if panel:
				panel.top.destroy()
				
		self.comparePanel = None
		self.colorPanel = None
		self.fontPanel = None
		self.prefsPanel = None
	#@nonl
	#@-node:frame.destroyAllPanels
	#@+node:frame.promptForSave
	def promptForSave (self):
		
		"""Prompt the user to save changes.
		
		Return true if the user vetos the quit or save operation."""
		
		c = self.commands
		name = choose(c.mFileName,c.mFileName,self.title)
		type = choose(app.quitting, "quitting?", "closing?")
		
		answer = leoDialog.askYesNoCancel("Confirm",
			'Save changes to %s before %s' % (name,type)).run(modal=true)
			
		# print answer	
		if answer == "cancel":
			return true # Veto.
		elif answer == "no":
			return false # Don't save and don't veto.
		else:
			if not c.mFileName:
				#@			<< Put up a file save dialog to set mFileName >>
				#@+node:<< Put up a file save dialog to set mFileName >>
				# Make sure we never pass None to the ctor.
				if not c.mFileName:
					c.mFileName = ""
					
				c.mFileName = tkFileDialog.asksaveasfilename(
					initialfile = c.mFileName,
					title="Save",
					filetypes=[("Leo files", "*.leo")],
					defaultextension=".leo")
				#@-node:<< Put up a file save dialog to set mFileName >>
				#@nl
			if c.mFileName:
				# print "saving", c.mFileName
				c.fileCommands.save(c.mFileName)
				return false # Don't veto.
			else:
				return true # Veto.
	#@nonl
	#@-node:frame.promptForSave
	#@+node:f.configureBar
	def configureBar (self, bar, verticalFlag):
		
		config = app.config
	
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
	#@nonl
	#@-node:f.configureBar
	#@+node:f.configureBarsFromConfig
	def configureBarsFromConfig (self):
		
		config = app.config
	
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
	#@nonl
	#@-node:f.configureBarsFromConfig
	#@+node:f.reconfigureFromConfig
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
	#@nonl
	#@-node:f.reconfigureFromConfig
	#@+node:f.setBodyFontFromConfig
	def setBodyFontFromConfig (self):
		
		config = app.config ; body = self.body
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
					traceback.print_exc()
	#@nonl
	#@-node:f.setBodyFontFromConfig
	#@+node:f.setInitialWindowGeometry
	def setInitialWindowGeometry(self):
		
		"""Set the position and size of the frame to config params."""
		
		config = app.config
	
		h = config.getIntWindowPref("initial_window_height")
		w = config.getIntWindowPref("initial_window_width")
		x = config.getIntWindowPref("initial_window_left")
		y = config.getIntWindowPref("initial_window_top")
		# print h,w,x,y
		
		if h == None or h < 5: h = 5
		if w == None or w < 5: w = 10
		y = max(y,0) ; x = max(x,0)
	
		self.top.geometry("%dx%d%+d%+d" % (w,h,x,y))
	#@nonl
	#@-node:f.setInitialWindowGeometry
	#@+node:f.setLogFontFromConfig
	def setLogFontFromConfig (self):
	
		log = self.log ; config = app.config
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
	
	#@-node:f.setLogFontFromConfig
	#@+node:f.setTabWidth
	def setTabWidth (self, w):
		
		try: # This can fail when called from scripts
			# Use the present font for computations.
			font = self.body.cget("font")
			root = app.root # 4/3/03: must specify root so idle window will work properly.
			font = tkFont.Font(root=root,font=font)
			tabw = font.measure(" " * abs(w)) # 7/2/02
			# tablist = `tabw` + ' ' + `2*tabw`
			self.body.configure(tabs=tabw)
			self.tab_width = w
			# print "frame.setTabWidth:" + `w` + "," + `tabw`
		except:
			es_exception()
			pass
	#@-node:f.setTabWidth
	#@+node:f.setTreeColorsFromConfig
	def setTreeColorsFromConfig (self):
	
		bg = app.config.getWindowPref("outline_pane_background_color")
		if bg:
			try: self.canvas.configure(bg=bg)
			except: pass
	#@-node:f.setTreeColorsFromConfig
	#@+node:f.setWrap
	def setWrap (self,v):
		
		c = self.commands
		dict = scanDirectives(c,v)
		if dict != None:
			# 8/30/03: Add scroll bars if we aren't wrapping.
			wrap = dict.get("wrap")
			if wrap:
				self.body.configure(wrap="word")
				self.bodyXBar.pack_forget()
			else:
				self.body.configure(wrap="none")
				self.bodyXBar.pack(side="bottom",fill="x")
	#@-node:f.setWrap
	#@+node:reconfigurePanes (use config bar_width)
	def reconfigurePanes (self):
		
		border = app.config.getIntWindowPref('additional_body_text_border')
		if border == None: border = 0
		
		# The body pane needs a _much_ bigger border when tiling horizontally.
		border = choose(self.splitVerticalFlag,2+border,6+border)
		self.body.configure(bd=border)
		
		# The log pane needs a slightly bigger border when tiling vertically.
		border = choose(self.splitVerticalFlag,4,2) 
		self.log.configure(bd=border)
	#@nonl
	#@-node:reconfigurePanes (use config bar_width)
	#@+node:The interface with frame internals
	def getTitle (self):
		return self.top.title()
		
	def setTopGeometry(self,geom):
		self.top.geometry(geom)
		
	def deiconify (self):
		self.top.deiconify()
		
	def lift (self):
		self.top.lift()
		
	def update (self):
		self.top.update()
	#@nonl
	#@-node:The interface with frame internals
	#@+node:The interface with the tree class
	# Coloring...
	def getColorizer(self): return self.tree.colorizer
	def recolor_now(self,v): return self.tree.recolor_now(v)
	def recolor_range(self,v,leading,trailing): return self.tree.recolor_range(v,leading,trailing)
	def recolor(self,v,incremental=false): return self.tree.recolor(v,incremental)
	def updateSyntaxColorer(self,v): return self.tree.colorizer.updateSyntaxColorer(v)
	
	# Drawing.
	def beginUpdate(self): return self.tree.beginUpdate()
	def endUpdate(self,flag=true): return self.tree.endUpdate(flag)
	def drawIcon(self,v,x,y): return self.tree.drawIcon(v,x,y)
	def redraw(self): return self.tree.redraw()
	def redraw_now(self): return self.tree.redraw_now()
	
	# Editing...
	def editLabel(self,v): return self.tree.editLabel(v)
	def editVnode(self): return self.tree.editVnode  
	def endEditLabel(self): return self.tree.endEditLabel()
	def setEditVnode(self,v): self.tree.editVnode = v
	def setNormalLabelState(self,v): return self.tree.setNormalLabelState(v)
	
	# Focus...
	def focus_get(self): return self.tree.canvas.focus_get()
	
	# Fonts...
	def getFont(self): return self.tree.getFont()
	def setFont(self,font): return self.tree.setFont(font)  
	
	# Scrolling... 
	def scrollTo(self,v): return self.tree.scrollTo(v)
	def idle_scrollTo(self,v): return self.tree.idle_scrollTo(v)
	
	# Selecting...
	def select(self,v,updateBeadList=true): return self.tree.select(v,updateBeadList)
	
	# Getters and setters...
	def currentVnode(self): return self.tree.currentVnode
	def dragging(self): return self.tree.dragging
	def rootVnode(self): return self.tree.rootVnode
	def topVnode(self): return self.tree.topVnode
	def setCurrentVnode(self,v): self.tree.currentVnode = v
	def setRootVnode(self,v): 	self.tree.rootVnode = v
	def setTreeIniting(self,flag): self.tree.initing = flag
	
	# vnode callbacks: to be removed.
	if 1: # No longer needed if the tree class injects the vnode callbacks.
		def OnBoxClick(self,v): return self.tree.OnBoxClick(v)
		def OnIconClick(self,v,event): return self.tree.OnIconClick(v,event)
		def OnIconDoubleClick(self,v,event): return self.tree.OnIconDoubleClick(v,event)
		def OnIconRightClick(self,v,event): return self.tree.OnIconRightClick(v,event)
		def OnDrag(self,v,event): return self.tree.OnDrag(v,event)
		def OnEndDrag(self,v,event): return self.tree.OnEndDrag(v,event)
		def OnPopup(self,v,event): return self.tree.OnPopup(v,event)
	# OnHeadlineClick
	# OnHeadlineRightClick
	def OnActivateHeadline(self,v): return self.tree.OnActivate(v)
	
	# Notifications. Can these be folded into convenience routines??
	def onBodyChanged(self,*args,**keys): return self.tree.onBodyChanged(*args,**keys)
	def onHeadChanged(self,*args,**keys): return self.tree.onHeadChanged(*args,**keys)
	def OnHeadlineKey(self,v,event): return self.tree.OnHeadlineKey(v,event)
	def idle_head_key(self,v): return self.tree.idle_head_key(v)
	
	# Others...
	def expandAllAncestors(self,v): return self.tree.expandAllAncestors(v)
	def getEditTextDict(self,v): return self.tree.edit_text_dict.get(v)
	#@nonl
	#@-node:The interface with the tree class
	#@+node:Scrolling callbacks (frame)
	def setCallback (self,*args,**keys):
		
		"""Callback to adjust the scrollbar.
		
		Args is a tuple of two floats describing the fraction of the visible area."""
	
		# if self.tree.trace: print "setCallback:",self.tree.redrawCount,`args`
	
		apply(self.treeBar.set,args,keys)
	
		if self.tree.allocateOnlyVisibleNodes:
			self.tree.setVisibleArea(args)
			
	def yviewCallback (self,*args,**keys):
		
		"""Tell the canvas to scroll"""
		
		# if self.tree.trace: print "vyiewCallback",`args`,`keys`
	
		if self.tree.allocateOnlyVisibleNodes:
			self.tree.allocateNodesBeforeScrolling(args)
	
		apply(self.canvas.yview,args,keys)
		
		
	#@-node:Scrolling callbacks (frame)
	#@+node:frame.OnCloseLeoEvent
	# Called from quit logic and when user closes the window.
	# Returns true if the close happened.
	
	def OnCloseLeoEvent(self):
	
		app.closeLeoWindow(self)
	#@nonl
	#@-node:frame.OnCloseLeoEvent
	#@+node:frame.OnControlKeyUp/Down
	def OnControlKeyDown (self,event=None):
		
		self.controlKeyIsDown = true
		
	def OnControlKeyUp (self,event=None):
	
		self.controlKeyIsDown = false
	#@-node:frame.OnControlKeyUp/Down
	#@+node:frame.OnVisibility
	# Handle the "visibility" event and attempt to attach the Leo icon.
	# This code must be executed whenever the window is redrawn.
	
	def OnVisibility (self,event):
	
		if self.icon and event.widget is self.top:
	
			# print "OnVisibility"
			self.icon.attach(self.top)
	#@nonl
	#@-node:frame.OnVisibility
	#@+node:OnActivateBody
	def OnActivateBody (self,event=None):
	
		try:
			c = self.commands
			app.setLog(self,"OnActivateBody")
			self.tree.OnDeactivate()
			set_focus(c,c.body)
		except:
			es_event_exception("activate body")
	
	
	#@-node:OnActivateBody
	#@+node:OnActivateLeoEvent, OnDeactivateLeoEvent
	def OnActivateLeoEvent(self,event=None):
	
		try:
			app.setLog(self,"OnActivateLeoEvent")
		except:
			es_event_exception("activate Leo")
	
	def OnDeactivateLeoEvent(self,event=None):
	
		try:
			app.setLog(None,"OnDeactivateLeoEvent")
		except:
			es_event_exception("deactivate Leo")
	#@nonl
	#@-node:OnActivateLeoEvent, OnDeactivateLeoEvent
	#@+node:OnActivateLog
	def OnActivateLog (self,event=None):
	
		try:
			app.setLog(self,"OnActivateLog")
			self.tree.OnDeactivate()
		except:
			es_event_exception("activate log")
	#@nonl
	#@-node:OnActivateLog
	#@+node:OnActivateTree
	def OnActivateTree (self,event=None):
	
		try:
			c = self.commands
			app.setLog(self,"OnActivateTree")
			self.tree.undimEditLabel()
			set_focus(c,c.frame.body) # 7/12/03
		except:
			es_event_exception("activate tree")
	#@-node:OnActivateTree
	#@+node:OnBodyClick, OnBodyRClick (Events)
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
	#@nonl
	#@-node:OnBodyClick, OnBodyRClick (Events)
	#@+node:OnBodyDoubleClick (Events)
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
	#@nonl
	#@-node:OnBodyDoubleClick (Events)
	#@+node:OnMouseWheel (Tomaz Ficko)
	# Contributed by Tomaz Ficko.  This works on some systems.
	# On XP it causes a crash in tcl83.dll.  Clearly a Tk bug.
	
	def OnMouseWheel(self, event=None):
		
		trace()
	
		try:
			if event.delta < 1:
				self.canvas.yview(Tkinter.SCROLL, 1, Tkinter.UNITS)
			else:
				self.canvas.yview(Tkinter.SCROLL, -1, Tkinter.UNITS)
		except:
			es_event_exception("scroll wheel")
	
		return "break"
	#@nonl
	#@-node:OnMouseWheel (Tomaz Ficko)
	#@+node:createIconBar
	def createIconBar (self):
		
		"""Create an empty icon bar in the packer's present position"""
	
		if not self.iconFrame:
			self.iconFrame = Tk.Frame(self.outerFrame,height="5m",bd=2,relief="groove")
			self.iconFrame.pack(fill="x",pady=2)
	#@nonl
	#@-node:createIconBar
	#@+node:hideIconBar
	def hideIconBar (self):
		
		"""Hide the icon bar by unpacking it.
		
		A later call to showIconBar will repack it in a new location."""
		
		if self.iconFrame:
			self.iconFrame.pack_forget()
	#@-node:hideIconBar
	#@+node:clearIconBar
	def clearIconBar(self):
		
		"""Destroy all the widgets in the icon bar"""
		
		f = self.iconFrame
		if not f: return
		
		for slave in f.pack_slaves():
			slave.destroy()
	
		f.configure(height="5m") # The default height.
		app.iconWidgetCount = 0
		app.iconImageRefs = []
	#@-node:clearIconBar
	#@+node:showIconBar
	def showIconBar(self):
		
		"""Show the icon bar by repacking it"""
	
		self.iconFrame.pack(fill="x",pady=2)
	#@nonl
	#@-node:showIconBar
	#@+node:addIconButton
	def addIconButton(self,text=None,imagefile=None,image=None,command=None,bg=None):
		
		"""Add a button containing text or a picture to the icon bar.
		
		Pictures take precedence over text"""
		
		f = self.iconFrame
		if not imagefile and not image and not text: return
	
		# First define n.	
		try:
			app.iconWidgetCount += 1
			n = app.iconWidgetCount
		except:
			n = app.iconWidgetCount = 1
	
		if not command:
			def command(n=n):
				print "command for widget %s" % (n)
	
		if imagefile or image:
			#@		<< create a picture >>
			#@+node:<< create a picture >>
			try:
				if imagefile:
					# Create the image.  Throws an exception if file not found
					imagefile = os.path.join(app.loadDir,imagefile)
					imagefile = os.path.normpath(imagefile)
					image = Tkinter.PhotoImage(master=app.root,file=imagefile)
					
					# Must keep a reference to the image!
					try:
						refs = app.iconImageRefs
					except:
						refs = app.iconImageRefs = []
				
					refs.append((imagefile,image),)
				
				if not bg:
					bg = f.cget("bg")
			
				b = Tk.Button(f,image=image,relief="flat",bd=0,command=command,bg=bg)
				b.pack(side="left",fill="y")
				return b
				
			except:
				es_exception()
				return None
			#@nonl
			#@-node:<< create a picture >>
			#@nl
		elif text:
			w = min(6,len(text))
			b = Tk.Button(f,text=text,width=w,relief="groove",bd=2,command=command)
			b.pack(side="left", fill="y")
			return b
			
		return None
	#@nonl
	#@-node:addIconButton
	#@+node:f.longFileName & shortFileName
	def longFileName (self):
		return self.commands.mFileName
		
	def shortFileName (self):
		return shortFileName(self.commands.mFileName)
	#@nonl
	#@-node:f.longFileName & shortFileName
	#@+node:f.put, putnl
	# All output to the log stream eventually comes here.
	
	def put (self,s,color=None):
		# print `app.quitting`,`self.log`
		if app.quitting: return
		if self.log:
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,app.tkEncoding)
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
			app.logWaiting.append((s,color),) # 2/25/03
			print "Null log"
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,"ascii")
			print s
	
	def putnl (self):
		if app.quitting: return
		if self.log:
			self.log.insert("end",'\n')
			self.log.see("end")
			self.log.update_idletasks()
		else:
			app.logWaiting.append(('\n',"black"),) # 6/28/03
			print "Null log"
			print
	#@nonl
	#@-node:f.put, putnl
	#@+node:f.getFocus
	def getFocus(self):
		
		"""Returns the widget that has focus, or body if None."""
	
		f = self.top.focus_displayof()
		if f:
			return f
		else:
			return self.body
	#@nonl
	#@-node:f.getFocus
	#@+node:canonicalizeShortcut
	#@+at 
	#@nonl
	# This code "canonicalizes" both the shortcuts that appear in menus and 
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
		#@	<< set the last field, preserving case >>
		#@+node:<< set the last field, preserving case >>
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
			if not app.menuWarningsGiven:
				print "bad shortcut specifier:", s
			return None,None
		
		last = fields[-1]
		if last == None or len(last) == 0:
			if not app.menuWarningsGiven:
				print "bad shortcut specifier:", s
			return None,None
		#@nonl
		#@-node:<< set the last field, preserving case >>
		#@nl
		#@	<< canonicalize the last field >>
		#@+node:<< canonicalize the last field >>
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
				#@		<< define dict of Tk bind names >>
				#@+node:<< define dict of Tk bind names >>
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
				#@nonl
				#@-node:<< define dict of Tk bind names >>
				#@nl
				if ch in dict.keys():
					bind_last = dict[ch]
		elif len(last) > 0:
			#@	<< define dict of special names >>
			#@+node:<< define dict of special names >>
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
			#@nonl
			# The following are not translated, so what appears in the menu is 
			# the same as what is passed to Tk.  Case is significant.
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
			#@-node:<< define dict of special names >>
			#@nl
			last2 = string.lower(last)
			if last2 in dict.keys():
				bind_last,menu_last = dict[last2]
		#@nonl
		#@-node:<< canonicalize the last field >>
		#@nl
		#@	<< synthesize the shortcuts from the information >>
		#@+node:<< synthesize the shortcuts from the information >>
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
		#@nonl
		#@-node:<< synthesize the shortcuts from the information >>
		#@nl
		# print shortcut,bind_shortcut,menu_shortcut
		return bind_shortcut,menu_shortcut
	#@nonl
	#@-node:canonicalizeShortcut
	#@+node:createMenuBar
	def createMenuBar(self, top):
	
		c = self.commands
		Tk = Tkinter
		topMenu = Tk.Menu(top,postcommand=self.OnMenuClick)
		self.setMenu("top",topMenu)
		self.menuShortcuts = []
		# To do: use Meta rathter than Control for accelerators for Unix
		#@	<< create the file menu >>
		#@+node:<< create the file menu >>
		fileMenu = self.createNewMenu("&File")
		#@<< create the top-level file entries >>
		#@+node:<< create the top-level file entries >>
		#@+at 
		#@nonl
		# leo.py will probably never have a Print command.  Instead, export 
		# text files that may be formatted and printed as desired.
		#@-at
		#@@c
		
		table = (
			("&New","Ctrl+N",self.OnNew),
			("&Open...","Ctrl+O",self.OnOpen))
		self.createMenuEntries(fileMenu,table)
		
		# 7/1/03: Create a new menu rather than call OnOpenWith.
		self.createNewMenu("Open &With...","File")
		
		table = (
			("-",None,None),
			("&Close","Ctrl+W",self.OnClose),
			("&Save","Ctrl+S",self.OnSave),
			("Save &As","Shift+Ctrl+S",self.OnSaveAs),
			("Save To",None,self.OnSaveTo), # &Tangle
			("Re&vert To Saved",None,self.OnRevert)) # &Read/Write
		self.createMenuEntries(fileMenu,table)
		#@nonl
		#@-node:<< create the top-level file entries >>
		#@nl
		#@<< create the recent files submenu >>
		#@+node:<< create the recent files submenu >>
		self.createNewMenu("Recent &Files...","File")
		self.recentFiles = app.config.getRecentFiles()
		self.createRecentFilesMenuItems()
		
		if 0: # now in Recent Files menu.
			table = (("Clear Recent Files",None,self.OnClearRecentFiles),)
			self.createMenuEntries(fileMenu,table)
		#@nonl
		#@-node:<< create the recent files submenu >>
		#@nl
		fileMenu.add_separator()
		#@<< create the read/write submenu >>
		#@+node:<< create the read/write submenu >>
		readWriteMenu = self.createNewMenu("&Read/Write...","File")
		
		table = (
				("&Read Outline Only","Shift+Ctrl+R",self.OnReadOutlineOnly),
				("Read @file &Nodes",None,self.OnReadAtFileNodes),
				("-",None,None),
				("Write &Dirty @file Nodes","Shift+Ctrl+Q",self.OnWriteDirtyAtFileNodes),
				("Write &Missing @file Nodes",None,self.OnWriteMissingAtFileNodes),
				("Write &Outline Only",None,self.OnWriteOutlineOnly),
				("&Write @file Nodes","Shift+Ctrl+W",self.OnWriteAtFileNodes),
				("-",None,None),
				("Write 4.x Derived Files",None,self.OnWriteNewDerivedFiles),
				("Write 3.x Derived Files",None,self.OnWriteOldDerivedFiles))
		
		self.createMenuEntries(readWriteMenu,table)
		#@nonl
		#@-node:<< create the read/write submenu >>
		#@nl
		#@<< create the tangle submenu >>
		#@+node:<< create the tangle submenu >>
		tangleMenu = self.createNewMenu("&Tangle...","File")
		
		table = (
			("Tangle &All","Shift+Ctrl+A",self.OnTangleAll),
			("Tangle &Marked","Shift+Ctrl+M",self.OnTangleMarked),
			("&Tangle","Shift+Ctrl+T",self.OnTangle))
		
		self.createMenuEntries(tangleMenu,table)
		
		#@-node:<< create the tangle submenu >>
		#@nl
		#@<< create the untangle submenu >>
		#@+node:<< create the untangle submenu >>
		untangleMenu = self.createNewMenu("&Untangle...","File")
		
		table = (
			("Untangle &All",None,self.OnUntangleAll),
			("Untangle &Marked",None,self.OnUntangleMarked),
			("&Untangle","Shift+Ctrl+U",self.OnUntangle))
			
		self.createMenuEntries(untangleMenu,table)
		
		#@-node:<< create the untangle submenu >>
		#@nl
		#@<< create the import submenu >>
		#@+node:<< create the import submenu >>
		importMenu = self.createNewMenu("&Import...","File")
		
		table = (
			("Import Derived File",None,self.OnImportDerivedFile),
			("Import To @&file","Shift+Ctrl+F",self.OnImportAtFile),
			("Import To @&root",None,self.OnImportAtRoot),
			("Import &CWEB Files",None,self.OnImportCWEBFiles),
			
			("Import &noweb Files",None,self.OnImportNowebFiles),
			("Import Flattened &Outline",None,self.OnImportFlattenedOutline))
			
		self.createMenuEntries(importMenu,table)
		
		#@-node:<< create the import submenu >>
		#@nl
		#@<< create the export submenu >>
		#@+node:<< create the export submenu >>
		exportMenu = self.createNewMenu("&Export...","File")
		
		table = [
			("Export &Headlines",None,self.OnExportHeadlines),
			("Outline To &CWEB",None,self.OnOutlineToCWEB),
			("Outline To &Noweb",None,self.OnOutlineToNoweb),
			("&Flatten Outline",None,self.OnFlattenOutline),
			("&Remove Sentinels",None,self.OnRemoveSentinels),
			("&Weave",None,self.OnWeave)]
		
		self.createMenuEntries(exportMenu,table)
		#@-node:<< create the export submenu >>
		#@nl
		fileMenu.add_separator()
		# Create the last entries.
		exitTable = (("E&xit","Ctrl-Q",self.OnQuit),)
		self.createMenuEntries(fileMenu,exitTable)
		
		#@-node:<< create the file menu >>
		#@nl
		#@	<< create the edit menu >>
		#@+node:<< create the edit menu >>
		editMenu = self.createNewMenu("&Edit")
		#@<< create the first top-level edit entries >>
		#@+node:<< create the first top-level edit entries >>
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
		#@-node:<< create the first top-level edit entries >>
		#@nl
		#@<< create the edit body submenu >>
		#@+node:<< create the edit body submenu >>
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
		
		#@-node:<< create the edit body submenu >>
		#@nl
		#@<< create the edit headline submenu >>
		#@+node:<< create the edit headline submenu >>
		editHeadlineMenu = self.createNewMenu("Edit &Headline...","Edit")
		
		table = (
			("Edit &Headline","Ctrl+H",self.OnEditHeadline),
			("&End Edit Headline","Escape",self.OnEndEditHeadline),
			("&Abort Edit Headline","Shift-Escape",self.OnAbortEditHeadline),
			("Insert Headline Time/&Date","Shift+Ctrl+H",self.OnInsertHeadlineTime))
			
			# 5/16/03 EKR: I dislike this command.
			#("Toggle Angle Brackets","Ctrl+B",self.OnToggleAngleBrackets)
			
		self.createMenuEntries(editHeadlineMenu,table)
		
		#@-node:<< create the edit headline submenu >>
		#@nl
		#@<< create the find submenu >>
		#@+node:<< create the find submenu >>
		findMenu = self.createNewMenu("&Find...","Edit")
		
		table = (
			("&Find Panel","Ctrl+F",self.OnFindPanel),
			("-",None,None),
			("Find &Next","F3",self.OnFindNext),
			("Find &Previous","F4",self.OnFindPrevious),
			("&Replace","Ctrl+=",self.OnReplace),
			("Replace, &Then Find","Ctrl+-",self.OnReplaceThenFind))
		
		self.createMenuEntries(findMenu,table)
		#@-node:<< create the find submenu >>
		#@nl
		#@<< create the last top-level edit entries >>
		#@+node:<< create the last top-level edit entries >>
		label = choose(c.frame.getColorizer().showInvisibles,"Hide In&visibles","Show In&visibles")
		
		table = (
			("&Go To Line Number","Alt+G",self.OnGoToLineNumber),
			("&Execute Script","Alt+Shift+E",self.OnExecuteScript),
			("Set Fon&t...","Shift+Alt+T",self.OnFontPanel),
			("Set &Colors...","Shift+Alt+C",self.OnColorPanel),
			(label,"Alt+V",self.OnViewAllCharacters),
			("-",None,None),
			("Prefere&nces","Ctrl+Y",self.OnPreferences))
		
		self.createMenuEntries(editMenu,table)
		#@nonl
		#@-node:<< create the last top-level edit entries >>
		#@nl
		#@-node:<< create the edit menu >>
		#@nl
		#@	<< create the outline menu >>
		#@+node:<< create the outline menu >>
		outlineMenu = self.createNewMenu("&Outline")
		#@<< create top-level outline menu >>
		#@+node:<< create top-level outline menu >>
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
		#@nonl
		#@-node:<< create top-level outline menu >>
		#@nl
		#@<< create expand/contract submenu >>
		#@+node:<< create expand/contract submenu >>
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
		#@nonl
		#@-node:<< create expand/contract submenu >>
		#@nl
		#@<< create move submenu >>
		#@+node:<< create move submenu >>
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
		#@-node:<< create move submenu >>
		#@nl
		#@<< create mark submenu >>
		#@+node:<< create mark submenu >>
		markMenu = self.createNewMenu("M&ark/Unmark...","Outline")
		
		table = (
			("&Mark","Ctrl-M",self.OnMark),
			("Mark &Subheads","Alt+S",self.OnMarkSubheads),
			("Mark Changed &Items","Alt+C",self.OnMarkChangedItems),
			("Mark Changed &Roots","Alt+R",self.OnMarkChangedRoots),
			("Mark &Clones","Alt+K",self.OnMarkClones),
			("&Unmark All","Alt+U",self.OnUnmarkAll))
			
		self.createMenuEntries(markMenu,table)
		#@-node:<< create mark submenu >>
		#@nl
		#@<< create goto submenu >>
		#@+node:<< create goto submenu >>
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
		#@-node:<< create goto submenu >>
		#@nl
		#@nonl
		#@-node:<< create the outline menu >>
		#@nl
		doHook("create-optional-menus",c=c)
		#@	<< create the window menu >>
		#@+node:<< create the window menu >>
		windowMenu = self.createNewMenu("&Window")
		
		table = (
			("&Equal Sized Panes","Ctrl-E",self.OnEqualSizedPanes),
			("Toggle &Active Pane","Ctrl-T",self.OnToggleActivePane),
			("Toggle &Split Direction",None,self.OnToggleSplitDirection),
			("-",None,None),
			("Casca&de",None,self.OnCascade),
			("&Minimize All",None,self.OnMinimizeAll),
			("-",None,None),
			("Open &Compare Window",None,self.OnOpenCompareWindow))
			
			# 
			# ("Open &Python Window","Alt+P",self.OnOpenPythonWindow))
		
		self.createMenuEntries(windowMenu,table)
		#@-node:<< create the window menu >>
		#@nl
		#@	<< create the help menu >>
		#@+node:<< create the help menu >>
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
		#@nonl
		#@-node:<< create the help menu >>
		#@nl
		top.config(menu=topMenu) # Display the menu.
		app.menuWarningsGiven = true
	#@-node:createMenuBar
	#@+node:frame.doCommand
	#@+at 
	#@nonl
	# Executes the given command, invoking hooks and catching exceptions.
	# Command handlers no longer need to return "break".  Yippee!
	# 
	# The code assumes that the "command1" hook has completely handled the 
	# command if doHook("command1") returns false.  This provides a very 
	# simple mechanism for overriding commands.
	#@-at
	#@@c
	
	def doCommand (self,command,label,event=None):
		
		# A horrible kludge: set app.log to cover for a possibly missing activate event.
		app.setLog(self,"doCommand")
	
		if label == "cantredo": label = "redo"
		if label == "cantundo": label = "undo"
		app.commandName = label
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
	#@-node:frame.doCommand
	#@+node:get/set/destroyMenu
	def getMenu (self,menuName):
	
		cmn = canonicalizeMenuName(menuName)
		return self.menus.get(cmn)
		
	def setMenu (self,menuName,menu):
		
		cmn = canonicalizeMenuName(menuName)
		self.menus [cmn] = menu
		
	def destroyMenu (self,menuName):
		
		cmn = canonicalizeMenuName(menuName)
		del self.menus[cmn]
	#@-node:get/set/destroyMenu
	#@+node:OnNew
	def OnNew (self,event=None):
	
		c,frame = app.gui.newLeoCommanderAndFrame(fileName=None)
		top = frame.top
		
		# 5/16/03: Needed for hooks.
		doHook("new",old_c=self,new_c=c)
		
		# Use the config params to set the size and location of the window.
		frame.setInitialWindowGeometry()
		top.deiconify()
		top.lift()
		frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio) # Resize the _new_ frame.
		
		c.beginUpdate()
		if 1: # within update
			t = leoNodes.tnode()
			v = leoNodes.vnode(c,t)
			v.initHeadString("NewHeadline")
			v.moveToRoot()
			c.editVnode(v)
		c.endUpdate()
		
		set_focus(c,frame.body)
	#@nonl
	#@-node:OnNew
	#@+node:frame.OnOpen
	def OnOpen(self,event=None):
	
		c = self.commands
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
			self.startupWindow==true and # The window was open on startup
			c.changed==false and self.saved==false and # The window has never been changed
			app.numberOfWindows == 1) # Only one untitled window has ever been opened
		#@-node:<< Set closeFlag if the only open window is empty >>
		#@nl
		# trace(`closeFlag`)
	
		fileName = tkFileDialog.askopenfilename(
			title="Open",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if fileName and len(fileName) > 0:
			ok, frame = self.OpenWithFileName(fileName)
			if ok and closeFlag:
				app.destroyWindow(self)
	#@nonl
	#@-node:frame.OnOpen
	#@+node:frame.OnOpenWith and allies
	#@+at 
	#@nonl
	# This routine handles the items in the Open With... menu.
	# These items can only be created by createOpenWithMenuFromTable().
	# Typically this would be done from the "open2" hook.
	#@-at
	#@@c
	
	def OnOpenWith(self,data=None):
		
		c = self.commands ; v = c.currentVnode()
		if not data or len(data) != 3: return # 6/22/03
		try:
			# print "OnOpenWith:",`data`
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
				searchPath = self.openWithTempFilePath(v,ext)
				
				if os.path.exists(searchPath):
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
						new_time=os.path.getmtime(path)
					except:
						new_time=None
						
					body_changed = old_body != new_body
					temp_changed = old_time != new_time
					
					if body_changed and temp_changed:
						#@	<< Raise dialog about conflict and set result >>
						#@+node:<< Raise dialog about conflict and set result >>
						message = (
							"Conflicting changes in outline and temp file\n\n" +
							"Do you want to use the code in the outline or the temp file?\n\n")
						
						result = leoDialog.askYesNoCancel(
							"Conflict!", message,
							yesMessage = "Outline",
							noMessage = "File",
							defaultButton = "Cancel").run(modal=1)
						
						#@-node:<< Raise dialog about conflict and set result >>
						#@nl
						if result == "cancel": return
						rewrite = result == "outline"
					else:
						rewrite = body_changed
							
					if rewrite:
						path = self.createOpenWithTempFile(v,ext)
					else:
						es("reopening: " + shortFileName(path),color="blue")
					#@nonl
					#@-node:<< create or recreate temp file as needed >>
					#@nl
				else:
					path = self.createOpenWithTempFile(v,ext)
				
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
				#@nonl
				#@-node:<< execute a command to open path in external editor >>
				#@nl
			doHook("openwith2",c=c,v=v,openType=openType,arg=arg,ext=ext)
		except:
			es("exception in OnOpenWith")
			es_exception()
	
		return "break"
	#@nonl
	#@-node:frame.OnOpenWith and allies
	#@+node:frame.createOpenWithTempFile
	def createOpenWithTempFile (self, v, ext):
		
		c = self.commands
		path = self.openWithTempFilePath(v,ext)
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
				encoding = app.config.default_derived_file_encoding
			s = toEncodedString(s,encoding,reportErrors=true) 
			file.write(s)
			file.flush()
			file.close()
			try:    time=os.path.getmtime(path)
			except: time=None
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
	#@-node:frame.createOpenWithTempFile
	#@+node:frame.openWithTempFilePath
	def openWithTempFilePath (self,v,ext):
		
		"""Return the path to the temp file corresponding to v and ext."""
	
		name = "LeoTemp_" + str(id(v.t)) + '_' + sanitize_filename(v.headString()) + ext
		td = os.path.abspath(tempfile.gettempdir())
		path = os.path.join(td,name)
		
		# print "openWithTempFilePath",path
		return path
	#@nonl
	#@-node:frame.openWithTempFilePath
	#@+node:frame.OpenWithFileName
	def OpenWithFileName(self,fileName):
		
		return openWithFileName(fileName,self.commands)
	#@nonl
	#@-node:frame.OpenWithFileName
	#@+node:frame.OnClose
	def OnClose(self,event=None):
		
		"""Handle the File-Close command."""
		
		app.closeLeoWindow(self)
	#@nonl
	#@-node:frame.OnClose
	#@+node:OnSave
	def OnSave(self,event=None):
	
		c = self.commands
		
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			self.title = ""
			c.mFileName = ""
	
		if c.mFileName != "":
			c.fileCommands.save(c.mFileName)
			c.setChanged(false)
			return
	
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = c.mFileName,
			title="Save",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			c.mFileName = ensure_extension(fileName, ".leo")
			self.title = c.mFileName
			self.top.title(computeWindowTitle(c.mFileName)) # 3/25/03
			c.fileCommands.save(c.mFileName)
			self.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:OnSave
	#@+node:OnSaveAs
	def OnSaveAs(self,event=None):
		
		c = self.commands
	
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			self.title = ""
			
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = c.mFileName,
			title="Save As",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			c.mFileName = ensure_extension(fileName, ".leo")
			self.title = c.mFileName
			self.top.title(computeWindowTitle(c.mFileName)) # 3/25/03
			self.commands.fileCommands.saveAs(c.mFileName)
			self.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:OnSaveAs
	#@+node:OnSaveTo
	def OnSaveTo(self,event=None):
		
		c = self.commands
	
		# Make sure we never pass None to the ctor.
		if not c.mFileName:
			self.title = ""
	
		# set local fileName, _not_ c.mFileName
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = c.mFileName,
			title="Save To",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			fileName = ensure_extension(fileName, ".leo")
			self.commands.fileCommands.saveTo(fileName)
			self.updateRecentFiles(c.mFileName)
	#@-node:OnSaveTo
	#@+node:frame.OnRevert
	def OnRevert(self,event=None):
		
		c = self.commands
	
		# Make sure the user wants to Revert.
		if not c.mFileName:
			c.mFileName = ""
		if len(c.mFileName)==0:
			return
	
		reply = leoDialog.askYesNo("Revert",
			"Revert to previous version of " + c.mFileName + "?").run(modal=true)
	
		if reply=="no":
			return
	
		# Kludge: rename this frame so OpenWithFileName won't think it is open.
		fileName = c.mFileName ; c.mFileName = ""
	
		# Create a new frame before deleting this frame.
		ok, frame = self.OpenWithFileName(fileName)
		if ok:
			frame.deiconify()
			app.destroyWindow(self)
		else:
			c.mFileName = fileName
	#@-node:frame.OnRevert
	#@+node:frame.OnQuit
	def OnQuit(self,event=None):
		
		app.onQuit()
	#@nonl
	#@-node:frame.OnQuit
	#@+node:frame.updateRecentFiles
	def updateRecentFiles (self, fileName):
		
		if not fileName or len(fileName) == 0:
			return
		
		# Update the recent files list in all windows.
		normFileName = os.path.normcase(fileName)
		
		for frame in app.windowList:
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
		app.config.setRecentFiles(frame.recentFiles)
		app.config.update()
	#@nonl
	#@-node:frame.updateRecentFiles
	#@+node:OnClearRecentFiles
	def OnClearRecentFiles (self,event=None):
		
		"""Clear the recent files list, then add the present file."""
		
		f = self ; c = f.commands
		
		recentFilesMenu = f.getMenu("Recent Files...")
		recentFilesMenu.delete(0,len(f.recentFiles))
		f.recentFiles = []
		f.createRecentFilesMenuItems()
		f.updateRecentFiles(c.mFileName)
	#@nonl
	#@-node:OnClearRecentFiles
	#@+node:frame.OnOpenRecentFile
	def OnOpenRecentFile(self,name=None):
		
		c = self.commands ; v = c.currentVnode()
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
			self.startupWindow==true and # The window was open on startup
			c.changed==false and self.saved==false and # The window has never been changed
			app.numberOfWindows == 1) # Only one untitled window has ever been opened
		#@-node:<< Set closeFlag if the only open window is empty >>
		#@nl
		if not name:
			return
	
		fileName = name
		if not doHook("recentfiles1",c=c,v=v,fileName=fileName,closeFlag=closeFlag):
			ok, frame = self.OpenWithFileName(fileName)
			if ok and closeFlag:
				app.destroyWindow(self)
				app.setLog(frame,"OnOpenRecentFile") # Sets the log stream for es()
	
		doHook("recentfiles2",c=c,v=v,fileName=fileName,closeFlag=closeFlag)
	#@nonl
	#@-node:frame.OnOpenRecentFile
	#@+node:createRecentFilesMenuItems
	def createRecentFilesMenuItems (self):
		
		f = self ; c = f.commands
		recentFilesMenu = f.getMenu("Recent Files...")
		
		# Delete all previous entries.
		recentFilesMenu.delete(0,len(f.recentFiles)+2)
		
		# Create the first two entries.
		table = (
			("Clear Recent Files",None,self.OnClearRecentFiles),
			("-",None,None))
		self.createMenuEntries(recentFilesMenu,table)
		
		# Create all the other entries.
		i = 3
		for name in f.recentFiles:
			callback = lambda f=f,name=name:f.OnOpenRecentFile(name)
			label = "%d %s" % (i-2,computeWindowTitle(name))
			recentFilesMenu.add_command(label=label,command=callback,underline=0)
			i += 1
	#@nonl
	#@-node:createRecentFilesMenuItems
	#@+node:fileCommands.OnReadOutlineOnly
	def OnReadOutlineOnly (self,event=None):
	
		fileName = tkFileDialog.askopenfilename(
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
	#@-node:fileCommands.OnReadOutlineOnly
	#@+node:OnReadAtFileNodes
	def OnReadAtFileNodes (self,event=None):
	
		c = self.commands ; v = c.currentVnode()
	
		# Create copy for undo.
		v_copy = v.copyTree()
		oldText = getAllText(c.body)
		oldSel = getTextSelection(c.body)
	
		c.fileCommands.readAtFileNodes()
	
		newText = getAllText(c.body)
		newSel = getTextSelection(c.body)
	
		c.undoer.setUndoParams("Read @file Nodes",
			v,select=v,oldTree=v_copy,
			oldText=oldText,newText=newText,
			oldSel=oldSel,newSel=newSel)
	#@nonl
	#@-node:OnReadAtFileNodes
	#@+node:OnWriteDirtyAtFileNodes
	def OnWriteDirtyAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeDirtyAtFileNodes()
	#@-node:OnWriteDirtyAtFileNodes
	#@+node:OnWriteMissingAtFileNodes
	def OnWriteMissingAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeMissingAtFileNodes()
	#@-node:OnWriteMissingAtFileNodes
	#@+node:OnWriteOutlineOnly
	def OnWriteOutlineOnly (self,event=None):
	
		self.commands.fileCommands.writeOutlineOnly()
	#@-node:OnWriteOutlineOnly
	#@+node:OnWriteAtFileNodes
	def OnWriteAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeAtFileNodes()
	#@-node:OnWriteAtFileNodes
	#@+node:OnImportDerivedFile
	def OnImportDerivedFile (self,event=None):
		
		"""Create a new outline from a 4.0 derived file."""
		
		frame = self ; c = frame.commands ; v = c.currentVnode()
		at = c.atFileCommands
		
		if v.isAtFileNode():
			fileName = v.atFileNodeName()
			c.importCommands.importDerivedFiles(v,fileName)
		else:
			es("not an @file node",color="blue")
	#@nonl
	#@-node:OnImportDerivedFile
	#@+node:OnWriteNew/OldDerivedFiles
	def OnWriteNewDerivedFiles (self,event=None):
		
		c = self.commands
	
		c.atFileCommands.writeNewDerivedFiles()
		es("auto-saving outline",color="blue")
		self.OnSave() # Must be done to preserve tnodeList.
		
	def OnWriteOldDerivedFiles (self,event=None):
		
		c = self.commands
		c.atFileCommands.writeOldDerivedFiles()
		es("auto-saving outline",color="blue")
		self.OnSave() # Must be done to clear tnodeList.
	#@nonl
	#@-node:OnWriteNew/OldDerivedFiles
	#@+node:OnTangleAll
	def OnTangleAll(self,event=None):
	
		self.commands.tangleCommands.tangleAll()
	#@-node:OnTangleAll
	#@+node:OnTangleMarked
	def OnTangleMarked(self,event=None):
	
		self.commands.tangleCommands.tangleMarked()
	#@-node:OnTangleMarked
	#@+node:OnTangle
	def OnTangle (self,event=None):
	
		self.commands.tangleCommands.tangle()
	#@-node:OnTangle
	#@+node:OnUntangleAll
	def OnUntangleAll(self,event=None):
	
		c = self.commands
		c.tangleCommands.untangleAll()
		c.undoer.clearUndoState()
	#@-node:OnUntangleAll
	#@+node:OnUntangleMarked
	def OnUntangleMarked(self,event=None):
	
		c = self.commands
		self.commands.tangleCommands.untangleMarked()
		c.undoer.clearUndoState()
	#@-node:OnUntangleMarked
	#@+node:OnUntangle
	def OnUntangle(self,event=None):
	
		c = self.commands
		self.commands.tangleCommands.untangle()
		c.undoer.clearUndoState()
	#@-node:OnUntangle
	#@+node:OnExportHeadlines
	def OnExportHeadlines (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Export Headlines",filetypes=filetypes,
			initialfile="headlines.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			self.commands.importCommands.exportHeadlines(fileName)
	#@-node:OnExportHeadlines
	#@+node:OnFlattenOutline
	def OnFlattenOutline (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Flatten Outline",filetypes=filetypes,
			initialfile="flat.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.flattenOutline(fileName)
	#@-node:OnFlattenOutline
	#@+node:OnImportAtRoot
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
	#@-node:OnImportAtRoot
	#@+node:OnImportAtFile
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
	#@-node:OnImportAtFile
	#@+node:OnImportCWEBFiles
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
	#@-node:OnImportCWEBFiles
	#@+node:OnImportFlattenedOutline
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
	#@-node:OnImportFlattenedOutline
	#@+node:OnImportNowebFiles
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
	#@-node:OnImportNowebFiles
	#@+node:OnOutlineToCWEB
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
	#@-node:OnOutlineToCWEB
	#@+node:OnOutlineToNoweb
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
	#@-node:OnOutlineToNoweb
	#@+node:OnRemoveSentinels
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
	#@-node:OnRemoveSentinels
	#@+node:OnWeave
	def OnWeave (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Weave",filetypes=filetypes,
			initialfile="weave.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.weave(fileName)
	#@-node:OnWeave
	#@+node:OnUndo
	def OnUndo(self,event=None):
	
		self.commands.undoer.undo()
	#@-node:OnUndo
	#@+node:OnRedo
	def OnRedo(self,event=None):
	
		self.commands.undoer.redo()
	#@-node:OnRedo
	#@+node:frame.OnCut, OnCutFrom Menu
	def OnCut (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.tree.forceFullRecolor()
		self.tree.onBodyWillChange(v,"Cut")
	
	def OnCutFromMenu (self,event=None):
	
		w = self.getFocus()
		self.tree.forceFullRecolor()
		w.event_generate(virtual_event_name("Cut"))
		
		# 11/2/02: Make sure the event sticks.
		c = self.commands ; v = c.currentVnode()
		c.frame.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	#@-node:frame.OnCut, OnCutFrom Menu
	#@+node:frame.OnCopy, OnCopyFromMenu
	def OnCopy (self,event=None):
	
		# Copy never changes dirty bits or syntax coloring.
		pass
		
	def OnCopyFromMenu (self,event=None):
	
		# trace()
		w = self.getFocus()
		w.event_generate(virtual_event_name("Copy"))
	#@-node:frame.OnCopy, OnCopyFromMenu
	#@+node:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	def OnPaste (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.tree.forceFullRecolor()
		self.tree.onBodyWillChange(v,"Paste")
		
	def OnPasteNode (self,event=None):
	
		# trace(`event`)
		pass
		
	def OnPasteFromMenu (self,event=None):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Paste"))
		
		# 10/23/02: Make sure the event sticks.
		c = self.commands ; v = c.currentVnode()
		self.tree.forceFullRecolor()
		c.frame.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	#@-node:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+node:OnDelete
	def OnDelete(self,event=None):
	
		c = self.commands ; v = c.currentVnode()
		first, last = oldSel = getTextSelection(self.body)
		if first and last and first != last:
			self.body.delete(first,last)
			c.frame.onBodyChanged(v,"Delete",oldSel=oldSel)
	#@-node:OnDelete
	#@+node:OnExecuteScript
	#@+at 
	#@nonl
	# This executes body text as a Python script.  We execute the selected 
	# text, or the entire body text if no text is selected.
	#@-at
	#@@c
	
	def OnExecuteScript(self,event=None,v=None):
		
		c = self.commands ; body = self.body ; s = None
		if v == None:
			v = c.currentVnode() 
	
		# Assume any selected body text is a script.
		start,end = getTextSelection(body)
		if start and end and start != end:
			s = getSelectedText(body) # 9/28/03
		else:
			s = getAllText(body)
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
	#@nonl
	#@-node:OnExecuteScript
	#@+node:OnGoToLineNumber & allies
	def OnGoToLineNumber (self,event=None):
	
		c = self.commands
		#@	<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		#@+node:<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
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
		#@nonl
		#@-node:<< set root to the nearest @file, @silentfile or @rawfile ancestor node >>
		#@nl
		#@	<< read the file into lines >>
		#@+node:<< read the file into lines >>
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
			
		#@-node:<< read the file into lines >>
		#@nl
		#@	<< get n, the line number, from a dialog >>
		#@+node:<< get n, the line number, from a dialog >>
		d = leoDialog.askOkCancelNumber("Enter Line Number","Line number:")
		n = d.run(modal=true)
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
					print s ; es(s, color="red") ; ok = false
				
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
							s = "Mismatched vnodeName\nExpecting: %s\n got: %s" % (v.headString(),vnodeName)
							print s ; es(s, color="red") ; ok = false
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
		c.frame.expandAllAncestors(v)
		c.selectVnode(v)
		c.endUpdate()
		#@nonl
		#@-node:<< select v and make it visible >>
		#@nl
		#@	<< put the cursor on line n2 of the body text >>
		#@+node:<< put the cursor on line n2 of the body text >>
		if found:
			c.frame.body.mark_set("insert",str(n2)+".0 linestart")
		else:
			c.frame.body.mark_set("insert","end-1c")
			es("%d lines" % len(lines), color="blue")
		c.frame.body.see("insert")
		#@nonl
		#@-node:<< put the cursor on line n2 of the body text >>
		#@nl
	#@nonl
	#@-node:OnGoToLineNumber & allies
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
			return root.headString(),0,1
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
	#@+node:OnSelectAll
	def OnSelectAll(self,event=None):
	
		setTextSelection(self.body,"1.0","end")
	#@-node:OnSelectAll
	#@+node:OnFontPanel
	def OnFontPanel(self,event=None):
	
		if self.fontPanel:
			# trace()
			self.fontPanel.top.deiconify()
			self.fontPanel.top.lift()
		else:
			self.fontPanel = fp =  leoFontPanel.leoFontPanel(self.commands)
			fp.run()
	#@-node:OnFontPanel
	#@+node:OnColorPanel
	def OnColorPanel(self,event=None):
		
		if self.colorPanel:
			# trace()
			self.colorPanel.top.deiconify()
			self.colorPanel.top.lift()
		else:
			self.colorPanel = cp = leoColor.leoColorPanel(self.commands)
			cp.run()
	
	#@-node:OnColorPanel
	#@+node:OnViewAllCharacters
	def OnViewAllCharacters (self, event=None):
	
		c = self.commands ; v = c.currentVnode() ; colorizer = c.frame.getColorizer()
		colorizer.showInvisibles = choose(colorizer.showInvisibles,0,1)
		# print `colorizer.showInvisibles`
	
		# It is much easier to change the menu name here than in the menu updater.
		menu = self.getMenu("Edit")
		if colorizer.showInvisibles:
			setMenuLabel(menu,"Show Invisibles","Hide Invisibles")
		else:
			setMenuLabel(menu,"Hide Invisibles","Show Invisibles")
	
		c.frame.recolor_now(v)
	#@-node:OnViewAllCharacters
	#@+node:OnPreferences
	def OnPreferences(self,event=None):
		
		c = self.commands
		if self.prefsPanel:
			# trace()
			self.prefsPanel.top.deiconify()
			self.prefsPanel.top.lift()
		else:
			self.prefsPanel = prefs = leoPrefs.LeoPrefs(c)
			top = prefs.top
			center_dialog(top)
	
			if 0: # No need to make this modal
				top.grab_set() # Make the dialog a modal dialog.
				top.focus_set() # Get all keystrokes.
				app.root.wait_window(top)
	#@-node:OnPreferences
	#@+node:OnConvertBlanks & OnConvertAllBlanks
	def OnConvertBlanks(self,event=None):
	
		self.commands.convertBlanks()
	
		
	def OnConvertAllBlanks(self,event=None):
	
		self.commands.convertAllBlanks()
	#@-node:OnConvertBlanks & OnConvertAllBlanks
	#@+node:OnConvertTabs & OnConvertAllTabs
	def OnConvertTabs(self,event=None):
	
		self.commands.convertTabs()
		
	def OnConvertAllTabs(self,event=None):
	
		self.commands.convertAllTabs()
	
	def OnReformatParagraph(self,event=None):
		
		self.commands.reformatParagraph()
	#@-node:OnConvertTabs & OnConvertAllTabs
	#@+node:OnDedent
	def OnDedent (self,event=None):
	
		self.commands.dedentBody()
	#@-node:OnDedent
	#@+node:OnExtract
	def OnExtract(self,event=None):
	
		self.commands.extract()
	#@-node:OnExtract
	#@+node:OnExtractNames
	def OnExtractNames(self,event=None):
	
		self.commands.extractSectionNames()
	#@-node:OnExtractNames
	#@+node:OnExtractSection
	def OnExtractSection(self,event=None):
	
		self.commands.extractSection()
	#@-node:OnExtractSection
	#@+node:OnFindMatchingBracket
	def OnFindMatchingBracket (self,event=None):
		
		c = self ; body = c.body
		brackets = "()[]{}<>"
		ch1=body.get("insert -1c")
		ch1= toUnicode(ch1,app.tkEncoding) # 9/28/03
		ch2=body.get("insert")
		ch2= toUnicode(ch2,app.tkEncoding) # 9/28/03
	
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
	#@-node:OnFindMatchingBracket
	#@+node:findMatchingBracket
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
			ch2= toUnicode(ch2,app.tkEncoding) # 9/28/03
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
	#@nonl
	#@-node:findMatchingBracket
	#@+node:OnIndent
	def OnIndent(self,event=None):
	
		self.commands.indentBody()
	#@-node:OnIndent
	#@+node:OnInsertBody/HeadlineTime & allies
	def OnInsertBodyTime (self,event=None):
		
		c = self.commands ; v = c.currentVnode()
		sel1,sel2 = oldSel = getTextSelection(c.body)
		if sel1 and sel2 and sel1 != sel2: # 7/7/03
			c.body.delete(sel1,sel2)
		c.body.insert("insert",self.getTime(body=true))
		c.frame.onBodyChanged(v,"Typing",oldSel=oldSel)
		
	def OnInsertHeadlineTime (self,event=None):
	
		c = self.commands ; v = c.currentVnode()
		s = v.headString() # Remember the old value.
	
		if v.edit_text():
			sel1,sel2 = getTextSelection(v.edit_text())
			if sel1 and sel2 and sel1 != sel2: # 7/7/03
				v.edit_text().delete(sel1,sel2)
			v.edit_text().insert("insert",self.getTime(body=false))
			c.frame.idle_head_key(v)
			
		# A kludge to get around not knowing whether we are editing or not.
		if s.strip() == v.headString().strip():
			es("Edit headline to append date/time")
	#@nonl
	#@-node:OnInsertBody/HeadlineTime & allies
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
	#@+node:OnEditHeadline
	def OnEditHeadline(self,event=None):
	
		tree = self.tree
		tree.editLabel(tree.currentVnode)
	#@nonl
	#@-node:OnEditHeadline
	#@+node:OnEndEditHeadline
	def OnEndEditHeadline(self,event=None):
		
		tree = self.commands.tree
		tree.endEditLabelCommand()
	#@-node:OnEndEditHeadline
	#@+node:OnAbortEditHeadline
	def OnAbortEditHeadline(self,event=None):
		
		tree = self.commands.tree
		tree.abortEditLabelCommand()
	#@-node:OnAbortEditHeadline
	#@+node:OnToggleAngleBrackets
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
		
		c.frame.editLabel(v)
		if v.edit_text():
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("1.0",s)
			c.frame.onHeadChanged(v)
	#@-node:OnToggleAngleBrackets
	#@+node:OnFindPanel
	def OnFindPanel(self,event=None):
	
		c = self.commands
	
		find = app.findFrame
		# 15-SEP-2002 DTHEIN: call withdraw() to force findFrame to top after 
		#                     opening multiple Leo files.
		find.top.withdraw()
		find.top.deiconify()
		find.top.lift()
		
		t = find.find_text
		set_focus(c,t)
		setTextSelection (t,"1.0","end") # Thanks Rich.
		find.commands = self
	#@-node:OnFindPanel
	#@+node:OnFindNext
	def OnFindNext(self,event=None):
	
		c = self.commands
		app.findFrame.findNextCommand(c)
	#@-node:OnFindNext
	#@+node:OnFindPrevious
	def OnFindPrevious(self,event=None):
	
		c = self.commands
		app.findFrame.findPreviousCommand(c)
	#@-node:OnFindPrevious
	#@+node:OnReplace
	def OnReplace(self,event=None):
	
		c = self.commands
		app.findFrame.changeCommand(c)
	#@-node:OnReplace
	#@+node:OnReplaceThenFind
	def OnReplaceThenFind(self,event=None):
	
		c = self.commands
		app.findFrame.changeThenFindCommand(c)
	#@-node:OnReplaceThenFind
	#@+node:OnCutNode
	def OnCutNode(self,event=None):
	
		self.commands.cutOutline()
	#@-node:OnCutNode
	#@+node:OnCopyNode
	def OnCopyNode(self,event=None):
	
		self.commands.copyOutline()
	#@-node:OnCopyNode
	#@+node:OnPasteNodee
	def OnPasteNode(self,event=None):
	
		self.commands.pasteOutline()
	#@-node:OnPasteNodee
	#@+node:OnDeleteNode
	def OnDeleteNode(self,event=None):
	
		self.commands.deleteHeadline()
	#@-node:OnDeleteNode
	#@+node:OnInsertNode
	def OnInsertNode(self,event=None):
	
		self.commands.insertHeadline()
	#@nonl
	#@-node:OnInsertNode
	#@+node:OnCloneNode
	def OnCloneNode(self,event=None):
	
		self.commands.clone()
	#@-node:OnCloneNode
	#@+node:OnSortChildren, OnSortSiblings
	def OnSortChildren(self,event=None):
	
		self.commands.sortChildren()
		
	def OnSortSiblings(self,event=None):
	
		self.commands.sortSiblings()
	#@nonl
	#@-node:OnSortChildren, OnSortSiblings
	#@+node:OnContractChildren (no longer used)
	def OnContractChildren(self,event=None):
	
		self.commands.contractSubheads()
	#@-node:OnContractChildren (no longer used)
	#@+node:OnContractAllChildren (no longer used)
	def OnContractAllChildren(self,event=None):
	
		self.commands.contractAllSubheads()
	#@-node:OnContractAllChildren (no longer used)
	#@+node:OnExpandAllChildren (no longer used)
	def OnExpandAllChildren(self,event=None):
	
		self.commands.expandAllSubheads()
	#@-node:OnExpandAllChildren (no longer used)
	#@+node:OnExpandChildren (no longer used)
	def OnExpandChildren(self,event=None):
	
		self.commands.expandSubheads()
	#@-node:OnExpandChildren (no longer used)
	#@+node:OnContractAll
	def OnContractAll(self,event=None):
	
		self.commands.contractAllHeadlines()
	#@-node:OnContractAll
	#@+node:OnContractNode
	def OnContractNode(self,event=None):
	
		self.commands.contractNode()
	#@-node:OnContractNode
	#@+node:OnContractParent
	def OnContractParent(self,event=None):
	
		self.commands.contractParent()
	#@-node:OnContractParent
	#@+node:OnExpandAll
	def OnExpandAll(self,event=None):
	
		self.commands.expandAllHeadlines()
	#@-node:OnExpandAll
	#@+node:OnExpandNextLevel
	def OnExpandNextLevel(self,event=None):
	
		self.commands.expandNextLevel()
	#@-node:OnExpandNextLevel
	#@+node:OnExpandNode
	def OnExpandNode(self,event=None):
	
		self.commands.expandNode()
	#@-node:OnExpandNode
	#@+node:OnExpandPrevLevel
	def OnExpandPrevLevel(self,event=None):
	
		self.commands.expandPrevLevel()
	#@-node:OnExpandPrevLevel
	#@+node:OnExpandToLevel1..9
	def OnExpandToLevel1(self,event=None): self.commands.expandLevel1()
	def OnExpandToLevel2(self,event=None): self.commands.expandLevel2()
	def OnExpandToLevel3(self,event=None): self.commands.expandLevel3()
	def OnExpandToLevel4(self,event=None): self.commands.expandLevel4()
	def OnExpandToLevel5(self,event=None): self.commands.expandLevel5()
	def OnExpandToLevel6(self,event=None): self.commands.expandLevel6()
	def OnExpandToLevel7(self,event=None): self.commands.expandLevel7()
	def OnExpandToLevel8(self,event=None): self.commands.expandLevel8()
	def OnExpandToLevel9(self,event=None): self.commands.expandLevel9()
	#@-node:OnExpandToLevel1..9
	#@+node:OnMoveDownwn
	def OnMoveDown(self,event=None):
	
		self.commands.moveOutlineDown()
	#@-node:OnMoveDownwn
	#@+node:OnMoveLeft
	def OnMoveLeft(self,event=None):
	
		self.commands.moveOutlineLeft()
	#@-node:OnMoveLeft
	#@+node:OnMoveRight
	def OnMoveRight(self,event=None):
	
		self.commands.moveOutlineRight()
	#@-node:OnMoveRight
	#@+node:OnMoveUp
	def OnMoveUp(self,event=None):
	
		self.commands.moveOutlineUp()
	#@-node:OnMoveUp
	#@+node:OnPromote
	def OnPromote(self,event=None):
	
		self.commands.promote()
	#@-node:OnPromote
	#@+node:OnDemote
	def OnDemote(self,event=None):
	
		self.commands.demote()
	#@-node:OnDemote
	#@+node:OnGoPrevVisible
	def OnGoPrevVisible(self,event=None):
	
		self.commands.selectVisBack()
	#@-node:OnGoPrevVisible
	#@+node:OnGoNextVisible
	def OnGoNextVisible(self,event=None):
	
		self.commands.selectVisNext()
	#@-node:OnGoNextVisible
	#@+node:OnGoBack
	def OnGoBack(self,event=None):
	
		self.commands.selectThreadBack()
	#@-node:OnGoBack
	#@+node:OnGoNext
	def OnGoNext(self,event=None):
	
		self.commands.selectThreadNext()
	#@-node:OnGoNext
	#@+node:OnGoPrevVisitedNode
	def OnGoPrevVisitedNode(self,event=None):
		
		c = self.commands
	
		while c.beadPointer > 0:
			c.beadPointer -= 1
			v = c.beadList[c.beadPointer]
			if v.exists(c):
				c.beginUpdate()
				c.frame.expandAllAncestors(v)
				c.selectVnode(v,updateBeadList=false)
				c.endUpdate()
				c.frame.idle_scrollTo(v)
				return
	#@-node:OnGoPrevVisitedNode
	#@+node:OnGoNextVisitedNode
	def OnGoNextVisitedNode(self,event=None):
		
		c = self.commands
	
		while c.beadPointer + 1 < len(c.beadList):
			c.beadPointer += 1
			v = c.beadList[c.beadPointer]
			if v.exists(c):
				c.beginUpdate()
				c.frame.expandAllAncestors(v)
				c.selectVnode(v,updateBeadList=false)
				c.endUpdate()
				c.frame.idle_scrollTo(v)
				return
	#@nonl
	#@-node:OnGoNextVisitedNode
	#@+node:OnGoToFirstNode
	def OnGoToFirstNode(self,event=None):
		
		c = self.commands
		v = c.rootVnode()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:OnGoToFirstNode
	#@+node:OnGoToLastNode
	def OnGoToLastNode(self,event=None):
		
		c = self.commands
		v = c.rootVnode()
		while v and v.threadNext():
			v = v.threadNext()
		if v:
			c.beginUpdate()
			c.frame.expandAllAncestors(v)
			c.selectVnode(v)
			c.endUpdate()
	
	#@-node:OnGoToLastNode
	#@+node:OnGoToNextChanged
	def OnGoToNextChanged(self,event=None):
	
		self.commands.goToNextDirtyHeadline()
	#@-node:OnGoToNextChanged
	#@+node:OnGoToNextClone
	def OnGoToNextClone(self,event=None):
	
		self.commands.goToNextClone()
	#@-node:OnGoToNextClone
	#@+node:OnGoToNextMarked
	def OnGoToNextMarked(self,event=None):
	
		self.commands.goToNextMarkedHeadline()
	#@-node:OnGoToNextMarked
	#@+node:OnGoToNextSibling
	def OnGoToNextSibling(self,event=None):
		
		c = self.commands
		v = c.currentVnode()
		if not v: return
		next = v.next()
		if next:
			c.beginUpdate()
			c.selectVnode(next)
			c.endUpdate()
	#@nonl
	#@-node:OnGoToNextSibling
	#@+node:OnGoToParent
	def OnGoToParent(self,event=None):
		
		c = self.commands
		v = c.currentVnode()
		if not v: return
		p = v.parent()
		if p:
			c.beginUpdate()
			c.selectVnode(p)
			c.endUpdate()
	#@-node:OnGoToParent
	#@+node:OnGoToPrevSibling
	def OnGoToPrevSibling(self,event=None):
		
		c = self.commands
		v = c.currentVnode()
		if not v: return
		back = v.back()
		if back:
			c.beginUpdate()
			c.selectVnode(back)
			c.endUpdate()
	#@-node:OnGoToPrevSibling
	#@+node:OnMark
	def OnMark(self,event=None):
	
		self.commands.markHeadline()
	#@-node:OnMark
	#@+node:OnMarkChangedItems
	def OnMarkChangedItems(self,event=None):
	
		self.commands.markChangedHeadlines()
	#@-node:OnMarkChangedItems
	#@+node:OnMarkChangedRoots
	def OnMarkChangedRoots(self,event=None):
	
		self.commands.markChangedRoots()
	#@-node:OnMarkChangedRoots
	#@+node:OnMarkClones
	def OnMarkClones(self,event=None):
	
		self.commands.markClones()
	#@-node:OnMarkClones
	#@+node:OnMarkSubheads
	def OnMarkSubheads(self,event=None):
	
		self.commands.markSubheads()
	#@-node:OnMarkSubheads
	#@+node:OnUnmarkAll
	def OnUnmarkAll(self,event=None):
	
		self.commands.unmarkAll()
	#@-node:OnUnmarkAll
	#@+node:OnEqualSizedPanes
	def OnEqualSizedPanes(self,event=None):
	
		frame = self
	
		frame.resizePanesToRatio(0.5,frame.secondary_ratio)
	#@-node:OnEqualSizedPanes
	#@+node:OnToggleActivePane
	def OnToggleActivePane (self,event=None):
	
		# trace(`event`)
		c = self.commands
	
		if self.getFocus() == self.body:
			set_focus(c,self.canvas)
		else:
			set_focus(c,self.body)
	#@nonl
	#@-node:OnToggleActivePane
	#@+node:OnToggleSplitDirection
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
		app.config.setWindowPref("initial_splitter_orientation",orientation)
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
	#@nonl
	#@-node:OnToggleSplitDirection
	#@+node:OnCascade
	def OnCascade(self,event=None):
		
		x,y,delta = 10,10,10
		for frame in app.windowList:
			top = frame.top
			# Compute w,h
			top.update_idletasks() # Required to get proper info.
			geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
			dim,junkx,junky = string.split(geom,'+')
			w,h = string.split(dim,'x')
			w,h = int(w),int(h)
			# Set new x,y and old w,h
			geom = "%dx%d%+d%+d" % (w,h,x,y)
			frame.setTopGeometry(geom) # frame.top.geometry("%dx%d%+d%+d" % (w,h,x,y))
			# Compute the new offsets.
			x += 30 ; y += 30
			if x > 200:
				x = 10 + delta ; y = 40 + delta
				delta += 10
	#@-node:OnCascade
	#@+node:OnMinimizeAll
	def OnMinimizeAll(self,event=None):
	
		self.minimize(app.findFrame)
		self.minimize(app.pythonFrame)
		for frame in app.windowList:
			self.minimize(frame)
		
	def minimize(self, frame):
	
		if frame and frame.top.state() == "normal":
			frame.top.iconify()
	#@nonl
	#@-node:OnMinimizeAll
	#@+node:OnHideLogWindow
	def OnHideLogWindow (self):
		
		c = self.commands ; frame = c.frame
		frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)
	#@nonl
	#@-node:OnHideLogWindow
	#@+node:OnOpenCompareWindow
	def OnOpenCompareWindow (self,event=None):
		
		c = self.commands
		cp = self.comparePanel
		
		if cp:
			cp.top.deiconify()
			cp.top.lift()
		else:
			cmp = leoCompare.leoCompare(c)
			self.comparePanel = cp =  leoCompare.leoComparePanel(c,cmp)
			cp.run()
	#@nonl
	#@-node:OnOpenCompareWindow
	#@+node:OnOpenPythonWindow (Dave Hein)
	def OnOpenPythonWindow(self,event=None):
	
		if sys.platform == "linux2":
			#@		<< open idle in Linux >>
			#@+node:<< open idle in Linux >>
			# 09-SEP-2002 DHEIN: Open Python window under linux
			
			try:
				pathToLeo = os.path.join(app.loadDir,"leo.py")
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
			try:
				executable_dir = os.path.dirname(sys.executable)
				idle_dir=os.path.join(executable_dir,"Tools","idle")
				if idle_dir not in sys.path:
					sys.path.append(idle_dir)
				# Initialize argv: the -t option sets the title of the Idle interp window.
				# pathToLeo = os.path.join(app.loadDir,"leo.py")
				sys.argv = ["leo","-t","leo"]
				import PyShell
				if app.idle_imported:
					reload(idle)
					app.idle_imported = true
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
			#@nonl
			#@-node:<< open idle in Windows >>
			#@nl
	#@-node:OnOpenPythonWindow (Dave Hein)
	#@+node:leoPyShellMain
	#@+at 
	#@nonl
	# The key parts of Pyshell.main(), but using Leo's root window instead of 
	# a new Tk root window.
	# 
	# This does _not_ work.  Using Leo's root window means that Idle will shut 
	# down Leo without warning when the Idle window is closed!
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
	#@+node:OnAbout (version number & date)
	def OnAbout(self,event=None):
		
		# Don't use triple-quoted strings or continued strings here.
		# Doing so would add unwanted leading tabs.
		version = self.getSignOnLine() + "\n\n"
		copyright = (
			"Copyright 1999-2003 by Edward K. Ream\n" +
			"All Rights Reserved\n" +
			"Leo is distributed under the Python License")
		url = "http://webpages.charter.net/edreamleo/front.html"
		email = "edreamleo@charter.net"
	
		leoDialog.aboutLeo(version,copyright,url,email).run(modal=false)
	#@-node:OnAbout (version number & date)
	#@+node:OnLeoDocumentation
	def OnLeoDocumentation (self,event=None):
	
		fileName = os.path.join(app.loadDir,"..","doc","LeoDocs.leo")
		try:
			self.OpenWithFileName(fileName)
		except:
			es("not found: LeoDocs.leo")
	#@-node:OnLeoDocumentation
	#@+node:OnLeoHome
	def OnLeoHome (self,event=None):
		
		import webbrowser
	
		url = "http://webpages.charter.net/edreamleo/front.html"
		try:
			webbrowser.open_new(url)
		except:
			es("not found: " + url)
	#@nonl
	#@-node:OnLeoHome
	#@+node:OnLeoHelp
	def OnLeoHelp (self,event=None):
		
		file = os.path.join(app.loadDir,"..","doc","sbooks.chm")
		if os.path.exists(file):
			os.startfile(file)
		else:
			answer = leoDialog.askYesNo(
				"Download Tutorial?",
				"Download tutorial (sbooks.chm) from SourceForge?").run(modal=true)
	
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
						os.chdir(app.loadDir)
						webbrowser.open_new(url)
				except:
					es("exception dowloading sbooks.chm")
					es_exception()
	#@nonl
	#@-node:OnLeoHelp
	#@+node:showProgressBar
	def showProgressBar (self,count,size,total):
	
		# trace("count,size,total:" + `count` + "," + `size` + "," + `total`)
		if self.scale == None:
			#@		<< create the scale widget >>
			#@+node:<< create the scale widget >>
			Tk = Tkinter
			top = Tk.Toplevel()
			top.title("Download progress")
			self.scale = scale = Tk.Scale(top,state="normal",orient="horizontal",from_=0,to=total)
			scale.pack()
			top.lift()
			#@nonl
			#@-node:<< create the scale widget >>
			#@nl
		self.scale.set(count*size)
		self.scale.update_idletasks()
	#@nonl
	#@-node:showProgressBar
	#@+node:OnLeoTutorial (version number)
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
	#@nonl
	#@-node:OnLeoTutorial (version number)
	#@+node:OnLeoConfig, OnApplyConfig
	def OnLeoConfig (self,event=None):
	
		# 4/21/03 new code suggested by fBechmann@web.de
		loadDir = app.loadDir
		configDir = app.config.configDir
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
	
		app.config.init()
		self.commands.frame.reconfigureFromConfig()
	#@nonl
	#@-node:OnLeoConfig, OnApplyConfig
	#@+node:Menu Convenience Routines
	#@+at 
	#@nonl
	# The following convenience routines make creating menus easier.
	# 
	# The Plugins section gives examples of how to use these routines to 
	# create custom menus and to add items to the Open With menu.
	#@-at
	#@-node:Menu Convenience Routines
	#@+node:createMenuEntries
	#@+at 
	#@nonl
	# The old, non-user-configurable code bound shortcuts in createMenuBar.  
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
				#@			<< set name to the label for doCommand >>
				#@+node:<< set name to the label for doCommand >>
				name = label.strip().lower()
				
				# Remove special characters from command names.
				name2 = ""
				for ch in name:
					if ch in string.letters or ch in string.digits:
						name2 = name2 + ch
				name = name2
				#@-node:<< set name to the label for doCommand >>
				#@nl
				#@			<< set accel to the shortcut for name >>
				#@+node:<< set accel to the shortcut for name >>
				config = app.config
				accel2 = config.getShortcut(name)
				
				# 7/19/03: Make sure "None" overrides the default shortcut.
				if accel2 == None or len(accel2) == 0:
					pass # Use default shortcut, if any.
				elif accel2.lower() == "none":
					accel = None # Remove the default shortcut.
				else:
					accel = accel2 # Override the default shortcut.
				#@nonl
				#@-node:<< set accel to the shortcut for name >>
				#@nl
				#@			<< set bind_shortcut and menu_shortcut using accel >>
				#@+node:<< set bind_shortcut and menu_shortcut using accel >>
				bind_shortcut,menu_shortcut = self.canonicalizeShortcut(accel)
				
				# Kludge: disable the shortcuts for cut, copy, paste.
				# This has already been bound in leoFrame.__init__
				# 2/13/03: A _possible_ fix for the Linux control-v bug.
				
				if sys.platform not in ("linux1","linux2"):
					if bind_shortcut in ("<Control-c>","<Control-v>","<Control-x>"):
						bind_shortcut = None
				#@nonl
				#@-node:<< set bind_shortcut and menu_shortcut using accel >>
				#@nl
				#@			<< define callback function >>
				#@+node:<< define callback function >>
				#@+at 
				#@nonl
				# Tkinter will call the callback function with:
				# 
				# 	- one event argument if the user uses a menu shortcut.
				# 	- no arguments otherwise.
				# 
				# Therefore, the first parameter must be event, and it must 
				# default to None.
				#@-at
				#@@c
				
				if openWith:
					def callback(event=None,self=self,data=command):
						# print "event",`event` ; print "self",`self` ; print "data",`data`
						return self.OnOpenWith(data=data)
						
				else:
					def callback(event=None,self=self,command=command,label=name):
						# print "event",`event` ; print "self",`self` ; print "command",`command`
						return self.doCommand(command,label,event)
				#@nonl
				#@-node:<< define callback function >>
				#@nl
				#@			<< set realLabel, amp_index and menu_shortcut >>
				#@+node:<< set realLabel, amp_index and menu_shortcut >>
				realLabel = app.getRealMenuName(label)
				amp_index = realLabel.find("&")
				realLabel = realLabel.replace("&","")
				if not menu_shortcut:
					menu_shortcut = ""
				#@nonl
				#@-node:<< set realLabel, amp_index and menu_shortcut >>
				#@nl
	
				menu.add_command(label=realLabel,accelerator=menu_shortcut,
					command=callback,underline=amp_index)
	
				if bind_shortcut:
					#@				<< handle bind_shorcut >>
					#@+node:<< handle bind_shorcut >>
					if bind_shortcut in self.menuShortcuts:
						if not app.menuWarningsGiven:
							es("duplicate shortcut:", accel, bind_shortcut, label,color="red")
							print "duplicate shortcut:", accel, bind_shortcut, label
					else:
						self.menuShortcuts.append(bind_shortcut)
						try:
							self.body.bind(bind_shortcut,callback)
							self.top.bind (bind_shortcut,callback)
						except: # could be a user error
							if not app.menuWarningsGiven:
								print "exception binding menu shortcut..."
								print bind_shortcut
								es_exception()
								app.menuWarningsGive = true
					#@nonl
					#@-node:<< handle bind_shorcut >>
					#@nl
	#@nonl
	#@-node:createMenuEntries
	#@+node:createMenuItemsFromTable
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
	#@nonl
	#@-node:createMenuItemsFromTable
	#@+node:createNewMenu
	def createNewMenu (self,menuName,parentName="top",before=None):
	
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
				label=app.getRealMenuName(menuName)
				amp_index = label.find("&")
				label = label.replace("&","")
				if before: # Insert the menu before the "before" menu.
					index_label=app.getRealMenuName(before)
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
	#@nonl
	#@-node:createNewMenu
	#@+node:createOpenWithMenuFromTable
	#@+at 
	#@nonl
	# Entries in the table passed to createOpenWithMenuFromTable are
	# tuples of the form (commandName,shortcut,data).
	# 
	# - command is one of "os.system", "os.startfile", "os.spawnl", 
	# "os.spawnv" or "exec".
	# - shortcut is a string describing a shortcut, just as for 
	# createMenuItemsFromTable.
	# - data is a tuple of the form (command,arg,ext).
	# 
	# Leo executes command(arg+path) where path is the full path to the temp 
	# file.
	# If ext is not None, the temp file has the given extension.
	# Otherwise, Leo computes an extension based on the @language directive in 
	# effect.
	#@-at
	#@@c
	
	def createOpenWithMenuFromTable (self,table):
	
		app.openWithTable = table # Override any previous table.
		# Delete the previous entry.
		parent = self.getMenu("File")
		label=app.getRealMenuName("Open &With...")
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
		for triple in table:
			if len(triple) == 3: # 6/22/03
				shortcut_table.append(triple)
			else:
				es("createOpenWithMenuFromTable: invalid data",color="red")
				return
				
		# for i in shortcut_table: print i
		self.createMenuItemsFromTable("Open &With...",shortcut_table,openWith=1)
	#@-node:createOpenWithMenuFromTable
	#@+node:deleteMenu
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
	#@nonl
	#@-node:deleteMenu
	#@+node:deleteMenuItem
	# Delete itemName from the menu whose name is menuName.
	def deleteMenuItem (self,itemName,menuName="top"):
	
		try:
			menu = self.getMenu(menuName)
			if menu:
				realItemName=app.getRealMenuName(itemName)
				menu.delete(realItemName)
			else:
				es("menu not found: " + menuName)
		except:
			es("exception deleting " + itemName + " from " + menuName + " menu")
			es_exception()
	#@nonl
	#@-node:deleteMenuItem
	#@+node:setRealMenuNamesFromTable
	def setRealMenuNamesFromTable (self,table):
	
		try:
			app.setRealMenuNamesFromTable(table)
		except:
			es("exception in setRealMenuNamesFromTable")
			es_exception()
	#@-node:setRealMenuNamesFromTable
	#@+node:frame.OnMenuClick (enables and disables all menu items)
	# This is the Tk "postcommand" callback.  It should update all menu items.
	
	def OnMenuClick (self):
		
		# A horrible kludge: set app.log to cover for a possibly missing activate event.
		app.setLog(self,"OnMenuClick")
		
		# Allow the user first crack at updating menus.
		c = self.commands ; v = c.currentVnode() # 2/8/03
		if not doHook("menu2",c=c,v=v):
			self.updateFileMenu()
			self.updateEditMenu()
			self.updateOutlineMenu()
	
	#@-node:frame.OnMenuClick (enables and disables all menu items)
	#@+node:hasSelection
	# Returns true if text in the outline or body text is selected.
	
	def hasSelection (self):
	
		if self.body:
			first, last = getTextSelection(self.body)
			return first != last
		else:
			return false
	#@nonl
	#@-node:hasSelection
	#@+node:updateFileMenu
	def updateFileMenu (self):
		
		c = self.commands
		if not c: return
	
		try:
			menu = self.getMenu("File")
			enableMenu(menu,"Revert To Saved", c.canRevert())
	
			# openWithMenu = self.getMenu("Open With...")
			enableMenu(menu,"Open With...", app.hasOpenWithMenu)
	
		except:
			es("exception updating File menu")
			es_exception()
	#@-node:updateFileMenu
	#@+node:updateEditMenu
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
	#@nonl
	#@-node:updateEditMenu
	#@+node:updateOutlineMenu
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
	#@nonl
	#@-node:updateOutlineMenu
	#@+node:Splitter stuff
	#@+at 
	#@nonl
	# The key invariants used throughout this code:
	# 
	# 1. self.splitVerticalFlag tells the alignment of the main splitter and
	# 2. not self.splitVerticalFlag tells the alignment of the secondary 
	# splitter.
	# 
	# Only the general-purpose divideAnySplitter routine doesn't know about 
	# these invariants.  So most of this code is specialized for Leo's 
	# window.  OTOH, creating a single splitter window would be much easier 
	# than this code.
	#@-at
	#@-node:Splitter stuff
	#@+node:resizePanesToRatio
	def resizePanesToRatio(self,ratio,secondary_ratio):
	
		self.divideLeoSplitter(self.splitVerticalFlag, ratio)
		self.divideLeoSplitter(not self.splitVerticalFlag, secondary_ratio)
		# trace(`ratio`)
	#@-node:resizePanesToRatio
	#@+node:bindBar
	def bindBar (self, bar, verticalFlag):
		
		if verticalFlag == self.splitVerticalFlag:
			bar.bind("<B1-Motion>", self.onDragMainSplitBar)
	
		else:
			bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)
	#@-node:bindBar
	#@+node:createLeoSplitter
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
	#@nonl
	#@-node:createLeoSplitter
	#@+node:divideAnySplitter
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
	#@nonl
	#@-node:divideAnySplitter
	#@+node:divideLeoSplitter
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
	#@nonl
	#@-node:divideLeoSplitter
	#@+node:initialRatios
	def initialRatios (self):
	
		config = app.config
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
	#@nonl
	#@-node:initialRatios
	#@+node:onDrag...
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
	#@nonl
	#@-node:onDrag...
	#@+node:placeSplitter
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
	#@nonl
	#@-node:placeSplitter
	#@+node:Status line: convenience routines
	#@@tabwidth 4
	#@-node:Status line: convenience routines
	#@+node:createStatusLine
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
		self.statusText = Tk.Text(statusFrame,height=1,state="disabled",bg=bg,relief="groove")
		self.statusText.pack(side="left",expand=1,fill="x")
	
		# Register an idle-time handler to update the row and column indicators.
		self.statusFrame.after_idle(self.updateStatusRowCol)
	#@nonl
	#@-node:createStatusLine
	#@+node:clearStatusLine
	def clearStatusLine (self):
		
		t = self.statusText
		t.configure(state="normal")
		t.delete("1.0","end")
		t.configure(state="disabled")
	#@-node:clearStatusLine
	#@+node:putStatusLine
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
	#@nonl
	#@-node:putStatusLine
	#@+node:updateStatusRowCol
	def updateStatusRowCol (self):
		
		body = self.body ; lab = self.statusLabel
		
		# New for Python 2.3: may be called during shutdown.
		if app.killed:
			return
	
		index = body.index("insert")
		row,col = getindex(body,index)
		if col > 0:
			s = body.get("%d.0" % (row),index)
			s = toUnicode(s,app.tkEncoding) # 9/28/03
			col = computeWidth (s,self.tab_width)
	
		if row != self.lastStatusRow or col != self.lastStatusCol:
			s = "line %d, col %d " % (row,col)
			lab.configure(text=s)
			self.lastStatusRow = row
			self.lastStatusCol = col
			
		# Reschedule this routine 100 ms. later.
		# Don't use after_idle: it hangs Leo.
		self.statusFrame.after(100,self.updateStatusRowCol)
	#@nonl
	#@-node:updateStatusRowCol
	#@-others

class LeoFrame (baseLeoFrame):
	"""A class that represents a Leo window."""
	pass
#@-node:@file leoFrame.py
#@-leo
