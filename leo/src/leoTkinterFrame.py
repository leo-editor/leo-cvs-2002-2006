# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoTkinterFrame.py
#@@first

# To do: Use config params for window height, width and bar color, relief and width.

#@@language python

from leoGlobals import *
import leoColor,leoFrame,leoNodes
import leoTkinterMenu,leoTkinterTree
import Tkinter,tkFont
import os,string,sys,time

Tk = Tkinter

#@+others
#@+node:class leoTkinterFrame
class leoTkinterFrame (leoFrame.leoFrame):
	
	"""A class that represents a Leo window."""

	#@	@+others
	#@+node:f.__init__
	def __init__(self,title):
	
		# Init the base class.
		leoFrame.leoFrame.__init__(self)
	
		self.title = title
		leoTkinterFrame.instances += 1
		self.c = None # Set in finishCreate.
	
		#@	<< set the leoTkinterFrame ivars >>
		#@+node:<< set the leoTkinterFrame ivars >>
		# Created in createLeoFrame and its allies.
		self.top = None
		self.tree = None
		self.f1 = self.f2 = None
		self.log = None  ; self.logBar = None
		self.body = None ; self.bodyCtrl = None ; self.bodyBar = None ; self.bodyXBar = None
		self.canvas = None ; self.treeBar = None
		self.splitter1 = self.splitter2 = None
		self.icon = None
		self.outerFrame = None # 5/20/02
		self.iconFrame = None # 5/20/02
		self.statusFrame = None # 5/20/02
		self.statusText = None # 5/20/02
		self.statusLabel = None # 5/20/02
		
		# Used by event handlers...
		self.redrawCount = 0
		self.draggedItem = None
		self.controlKeyIsDown = false # For control-drags
		self.revertHeadline = None # Previous headline text for abortEditLabel.
		#@nonl
		#@-node:<< set the leoTkinterFrame ivars >>
		#@nl
	#@-node:f.__init__
	#@+node:f.__repr__
	def __repr__ (self):
	
		return "<leoTkinterFrame: %s>" % self.title
	#@-node:f.__repr__
	#@+node:f.createCanvas
	def createCanvas (self,parentFrame):
		
		frame = self ; config = app.config ; Tk = Tkinter
		
		scrolls = config.getBoolWindowPref('outline_pane_scrolls_horizontally')
		scrolls = choose(scrolls,1,0)
	
		canvas = Tk.Canvas(parentFrame,name="canvas",
			bd=0,bg="white",relief="flat")
	
		frame.treeBar = treeBar = Tk.Scrollbar(parentFrame,name="treeBar")
		
		# Bind mouse wheel event to canvas
		if sys.platform != "win32": # Works on 98, crashes on XP.
			canvas.bind("<MouseWheel>", self.OnMouseWheel)
			
		canvas['yscrollcommand'] = self.setCallback
		treeBar['command']     = self.yviewCallback
		
		treeBar.pack(side="right", fill="y")
		if scrolls: 
			treeXBar = Tk.Scrollbar( 
				parentFrame,name='treeXBar',orient="horizontal") 
			canvas['xscrollcommand'] = treeXBar.set 
			treeXBar['command'] = canvas.xview 
			treeXBar.pack(side="bottom", fill="x")
		
		canvas.pack(expand=1,fill="both")
	
		canvas.bind("<Button-1>", frame.OnActivateTree)
	
		# Handle mouse wheel in the outline pane.
		if sys.platform == "linux2": # This crashes tcl83.dll
			canvas.bind("<MouseWheel>", frame.OnMouseWheel)
		
		# print_bindings("canvas",canvas)
		return canvas
	#@nonl
	#@-node:f.createCanvas
	#@+node:f.finishCreate
	def finishCreate (self,c):
		
		frame = self ; frame.c = c
		Tk = Tkinter ; gui = app.gui
	
		#@	<< create the toplevel frame >>
		#@+node:<< create the toplevel frame >>
		frame.top = top = Tk.Toplevel()
		gui.attachLeoIcon(top)
		top.title(frame.title)
		top.minsize(30,10) # In grid units.
		
		frame.top.protocol("WM_DELETE_WINDOW", frame.OnCloseLeoEvent)
		frame.top.bind("<Button-1>", frame.OnActivateLeoEvent)
		
		frame.top.bind("<Activate>", frame.OnActivateLeoEvent) # Doesn't work on windows.
		frame.top.bind("<Deactivate>", frame.OnDeactivateLeoEvent) # Doesn't work on windows.
		
		frame.top.bind("<Control-KeyPress>",frame.OnControlKeyDown)
		frame.top.bind("<Control-KeyRelease>",frame.OnControlKeyUp)
		
		if 0: # 10/31/03: Trying to catch these events seems dubious.
			# However, frame.controlKeyIsDown is not always in the correct state!
			app.gui.root.bind("<Control-KeyPress>",frame.OnControlKeyDown)
			app.gui.root.bind("<Control-KeyRelease>",frame.OnControlKeyUp)
		#@nonl
		#@-node:<< create the toplevel frame >>
		#@nl
		#@	<< create all the subframes >>
		#@+node:<< create all the subframes >>
		# Create the outer frame.
		self.outerFrame = outerFrame = Tk.Frame(top)
		self.outerFrame.pack(expand=1,fill="both")
		
		self.createIconBar()
		#@<< create both splitters >>
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
		
		# Create the canvas, tree, log and body.
		frame.canvas   = self.createCanvas(self.split2Pane1)
		frame.tree     = leoTkinterTree.leoTkinterTree(c,frame,frame.canvas)
		frame.log      = leoTkinterLog(frame,self.split2Pane2)
		frame.body     = leoTkinterBody(frame,self.split1Pane2)
		
		# Yes, this an "official" ivar: this is a kludge.
		frame.bodyCtrl = frame.body.bodyCtrl
		
		# Configure.  N.B. There may be Tk bugs here that make the order significant!
		frame.setTabWidth(c.tab_width)
		frame.tree.setTreeColorsFromConfig()
		self.reconfigurePanes()
		self.body.setFontFromConfig()
		
		if 0: # No longer done automatically.
		
			# Create the status line.
			self.createStatusLine()
			self.putStatusLine("Welcome to Leo")
		#@nonl
		#@-node:<< create all the subframes >>
		#@nl
		#@	<< create the first tree node >>
		#@+node:<< create the first tree node >>
		t = leoNodes.tnode()
		v = leoNodes.vnode(c,t)
		v.initHeadString("NewHeadline")
		v.moveToRoot()
		
		c.beginUpdate()
		c.selectVnode(v)
		c.redraw()
		c.frame.getFocus()
		c.editVnode(v)
		c.endUpdate(false)
		#@nonl
		#@-node:<< create the first tree node >>
		#@nl
	
		self.menu = leoTkinterMenu.leoTkinterMenu(frame)
	
		v = c.currentVnode()
		if not doHook("menu1",c=c,v=v):
			frame.menu.createMenuBar(self)
	
		app.setLog(frame.log,"tkinterFrame.__init__") # the leoTkinterFrame containing the log
	
		app.windowList.append(frame)
		
		c.initVersion()
		c.signOnWithVersion()
		
		self.body.createBindings(frame)
	#@nonl
	#@-node:f.finishCreate
	#@+node:Creating the splitter
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
	#@-node:Creating the splitter
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
					imagefile = os_path_join(app.loadDir,imagefile)
					imagefile = os_path_normpath(imagefile)
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
	#@+node:Creating the status area
	#@@tabwidth 4
	#@-node:Creating the status area
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
		
		if "black" not in self.log.colorTags:
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
		
		c = self.c ; body = self.bodyCtrl ; lab = self.statusLabel
		gui = app.gui
		
		# New for Python 2.3: may be called during shutdown.
		if app.killed:
			return
	
		if 0: # New code
			index = c.frame.body.getInsertionPoint()
			row,col = c.frame.body.indexToRowColumn(index)
			index1 = c.frame.body.rowColumnToIndex(row,0)
		else:
			index = body.index("insert")
			row,col = gui.getindex(body,index)
		
		if col > 0:
			if 0: # new code
				s = c.frame.body.getRange(index1,index2)
			else:
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
	#@+node:destroyAllObjects
	def destroyAllObjects (self):
	
		"""Clear all links to objects in a Leo window."""
	
		frame = self ; c = self.c ; tree = frame.tree ; body = self.body
	
		# Do this first.
		#@	<< clear all vnodes and tnodes in the tree >>
		#@+node:<< clear all vnodes and tnodes in the tree>>
		# Using a dict here is essential for adequate speed.
		vList = [] ; tDict = {}
		
		v = c.rootVnode()
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
		
		vList = [] ; tDict = {} # Remove these references immediately.
		#@nonl
		#@-node:<< clear all vnodes and tnodes in the tree>>
		#@nl
	
		# Destroy all ivars in subclasses.
		clearAllIvars(c.atFileCommands)
		clearAllIvars(c.fileCommands)
		clearAllIvars(c.importCommands)
		clearAllIvars(c.tangleCommands)
		clearAllIvars(c.undoer)
		clearAllIvars(c)
		clearAllIvars(body.colorizer)
		clearAllIvars(body)
		clearAllIvars(tree)
		clearAllIvars(tree)
	
		# This must be done last.
		frame.destroyAllPanels()
		clearAllIvars(frame)
	#@nonl
	#@-node:destroyAllObjects
	#@+node:destroyAllPanels
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
	#@-node:destroyAllPanels
	#@+node:destroySelf
	def destroySelf (self):
		
		top = self.top # Remember this: we are about to destroy all of our ivars!
	
		if app.windowList:
			self.destroyAllObjects()
	
		top.destroy()
	#@nonl
	#@-node:destroySelf
	#@+node:bringToFront
	def bringToFront (self):
		
		"""Bring the tkinter Prefs Panel to the front."""
	
		self.top.deiconify()
		self.top.lift()
	#@nonl
	#@-node:bringToFront
	#@+node:configureBar
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
	#@-node:configureBar
	#@+node:configureBarsFromConfig
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
	#@-node:configureBarsFromConfig
	#@+node:reconfigureFromConfig
	def reconfigureFromConfig (self):
		
		frame = self ; c = frame.c
		
		# Not ready yet: just reset the width and color.
		# We need self.bar1 and self.bar2 ivars.
		# self.reconfigureBar(...)
		
		# The calls to redraw are workarounds for an apparent Tk bug.
		# Without them the text settings get applied to the wrong widget!
		# Moreover, only this order seems to work on Windows XP...
		frame.tree.setFontFromConfig()
		frame.tree.setTreeColorsFromConfig()
		frame.configureBarsFromConfig()
		c.redraw()
		frame.body.setFontFromConfig()
		frame.setTabWidth(c.tab_width) # 12/2/03
		c.redraw()
		frame.log.setFontFromConfig()
		c.redraw()
	#@-node:reconfigureFromConfig
	#@+node:setInitialWindowGeometry
	def setInitialWindowGeometry(self):
		
		"""Set the position and size of the frame to config params."""
		
		config = app.config
	
		h = config.getIntWindowPref("initial_window_height")
		w = config.getIntWindowPref("initial_window_width")
		x = config.getIntWindowPref("initial_window_left")
		y = config.getIntWindowPref("initial_window_top")
		
		if h and w and x and y:
			self.setTopGeometry(w,h,x,y)
	#@nonl
	#@-node:setInitialWindowGeometry
	#@+node:setTabWidth
	def setTabWidth (self, w):
		
		try: # This can fail when called from scripts
			# Use the present font for computations.
			font = self.bodyCtrl.cget("font")
			root = app.root # 4/3/03: must specify root so idle window will work properly.
			font = tkFont.Font(root=root,font=font)
			tabw = font.measure(" " * abs(w)) # 7/2/02
			# tablist = `tabw` + ' ' + `2*tabw`
			self.bodyCtrl.configure(tabs=tabw)
			self.tab_width = w
			# trace(w,tabw)
		except:
			es_exception()
			pass
	#@-node:setTabWidth
	#@+node:setWrap
	def setWrap (self,v):
		
		c = self.c
		dict = scanDirectives(c,v)
		if dict != None:
			# 8/30/03: Add scroll bars if we aren't wrapping.
			wrap = dict.get("wrap")
			if wrap:
				self.bodyCtrl.configure(wrap="word")
				self.bodyXBar.pack_forget()
			else:
				self.bodyCtrl.configure(wrap="none")
				self.bodyXBar.pack(side="bottom",fill="x")
	#@-node:setWrap
	#@+node:setTopGeometry
	def setTopGeometry(self,w,h,x,y,adjustSize=true):
		
		# Put the top-left corner on the screen.
		x = max(10,x) ; y = max(10,y)
		
		if adjustSize:
			top = self.top
			sw = top.winfo_screenwidth()
			sh = top.winfo_screenheight()
	
			# Adjust the size so the whole window fits on the screen.
			w = min(sw-10,w)
			h = min(sh-10,h)
	
			# Adjust position so the whole window fits on the screen.
			if x + w > sw: x = 10
			if y + h > sh: y = 10
		
		geom = "%dx%d%+d%+d" % (w,h,x,y)
		
		self.top.geometry(geom)
	#@nonl
	#@-node:setTopGeometry
	#@+node:reconfigurePanes (use config bar_width)
	def reconfigurePanes (self):
		
		border = app.config.getIntWindowPref('additional_body_text_border')
		if border == None: border = 0
		
		# The body pane needs a _much_ bigger border when tiling horizontally.
		border = choose(self.splitVerticalFlag,2+border,6+border)
		self.bodyCtrl.configure(bd=border)
		
		# The log pane needs a slightly bigger border when tiling vertically.
		border = choose(self.splitVerticalFlag,4,2) 
		self.log.configureBorder(border)
	#@nonl
	#@-node:reconfigurePanes (use config bar_width)
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
			frame = self ; c = frame.c ; gui = app.gui
			app.setLog(frame.log,"OnActivateBody")
			self.tree.OnDeactivate()
			gui.set_focus(c,frame.body.bodyCtrl) # Reference to bodyCtrl is allowable in an event handler.
		except:
			es_event_exception("activate body")
	#@nonl
	#@-node:OnActivateBody
	#@+node:OnActivateLeoEvent, OnDeactivateLeoEvent
	def OnActivateLeoEvent(self,event=None):
	
		try:
			app.setLog(self.log,"OnActivateLeoEvent")
		except:
			es_event_exception("activate Leo")
	
	def OnDeactivateLeoEvent(self,event=None):
		
		if 0: # This causes problems on the Mac.
			try:
				app.setLog(None,"OnDeactivateLeoEvent")
			except:
				es_event_exception("deactivate Leo")
	#@nonl
	#@-node:OnActivateLeoEvent, OnDeactivateLeoEvent
	#@+node:OnActivateTree
	def OnActivateTree (self,event=None):
	
		try:
			frame = self ; c = frame.c ; gui = app.gui
			app.setLog(frame.log,"OnActivateTree")
			self.tree.undimEditLabel()
			gui.set_focus(c, frame.bodyCtrl)
		except:
			es_event_exception("activate tree")
	#@-node:OnActivateTree
	#@+node:OnBodyClick, OnBodyRClick (Events)
	def OnBodyClick (self,event=None):
	
		try:
			c = self.c ; v = c.currentVnode()
			if not doHook("bodyclick1",c=c,v=v,event=event):
				self.OnActivateBody(event=event)
			doHook("bodyclick2",c=c,v=v,event=event)
		except:
			es_event_exception("bodyclick")
	
	def OnBodyRClick(self,event=None):
		
		try:
			c = self.c ; v = c.currentVnode()
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
			c = self.c ; v = c.currentVnode()
			if not doHook("bodydclick1",c=c,v=v,event=event):
				if event: # 8/4/02: prevent wandering insertion point.
					index = "@%d,%d" % (event.x, event.y) # Find where we clicked
				body = self.bodyCtrl
				start = body.index(index + " wordstart")
				end = body.index(index + " wordend")
				self.body.setTextSelection(start,end)
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
	#@+node:abortEditLabelCommand
	def abortEditLabelCommand (self):
		
		frame = self ; c = frame.c ; v = c.currentVnode() ; tree = frame.tree
		
		if app.batchMode:
			c.notValidInBatchMode("Abort Edit Headline")
			return
	
		if self.revertHeadline and v.edit_text() and v == tree.editVnode():
		
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("end",self.revertHeadline)
			tree.idle_head_key(v) # Must be done immediately.
			tree.revertHeadline = None
			tree.select(v)
			if v and len(v.t.joinList) > 0:
				tree.force_redraw() # force a redraw of joined headlines.
	#@nonl
	#@-node:abortEditLabelCommand
	#@+node:frame.OnCut, OnCutFrom Menu
	def OnCut (self,event=None):
		
		"""The handler for the virtual Cut event."""
	
		frame = self ; c = frame.c ; v = c.currentVnode()
		
		# This is probably being subverted by Tk.
		if app.gui.win32clipboard:
			data = frame.body.getSelectedText()
			if data:
				app.gui.replaceClipboardWith(data)
	
		# Activate the body key handler by hand.
		frame.body.forceFullRecolor()
		frame.body.onBodyWillChange(v,"Cut")
	
	def OnCutFromMenu (self):
		
		w = self.getFocus()
		w.event_generate(virtual_event_name("Cut"))
	
		if 0: # Make sure the event sticks.
			frame = self ; c = frame.c ; v = c.currentVnode()
			frame.body.forceFullRecolor()
			frame.tree.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	
	
	
	
	#@-node:frame.OnCut, OnCutFrom Menu
	#@+node:frame.OnCopy, OnCopyFromMenu
	def OnCopy (self,event=None):
		
		frame = self
	
		if app.gui.win32clipboard:
			data = frame.body.getSelectedText()
			if data:
				app.gui.replaceClipboardWith(data)
			
		# Copy never changes dirty bits or syntax coloring.
		
	def OnCopyFromMenu (self):
	
		frame = self
		w = frame.getFocus()
		w.event_generate(virtual_event_name("Copy"))
	
	#@-node:frame.OnCopy, OnCopyFromMenu
	#@+node:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	def OnPaste (self,event=None):
		
		frame = self ; c = frame.c ; v = c.currentVnode()
	
		# Activate the body key handler by hand.
		frame.body.forceFullRecolor()
		frame.body.onBodyWillChange(v,"Paste")
		
	def OnPasteFromMenu (self):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Paste"))
		
		if 0: # Make sure the event sticks.
			frame = self ; c = frame.c ; v = c.currentVnode()
			frame.body.forceFullRecolor()
			frame.tree.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	#@-node:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+node:endEditLabelCommand
	def endEditLabelCommand (self):
	
		frame = self ; c = frame.c ; tree = frame.tree ; gui = app.gui
		
		if app.batchMode:
			c.notValidInBatchMode("End Edit Headline")
			return
		
		v = frame.tree.editVnode()
	
		# trace(v)
		if v and v.edit_text():
			tree.select(v)
		if v: # Bug fix 10/9/02: also redraw ancestor headlines.
			tree.force_redraw() # force a redraw of joined headlines.
	
		gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02
	#@nonl
	#@-node:endEditLabelCommand
	#@+node:insertHeadlineTime
	def insertHeadlineTime (self):
	
		frame = self ; c = frame.c ; v = c.currentVnode()
		h = v.headString() # Remember the old value.
		
		if app.batchMode:
			c.notValidInBatchMode("Insert Headline Time")
			return
	
		if v.edit_text():
			sel1,sel2 = app.gui.getTextSelection(v.edit_text())
			if sel1 and sel2 and sel1 != sel2: # 7/7/03
				v.edit_text().delete(sel1,sel2)
			v.edit_text().insert("insert",c.getTime(body=false))
			frame.tree.idle_head_key(v)
	
		# A kludge to get around not knowing whether we are editing or not.
		if h.strip() == v.headString().strip():
			es("Edit headline to append date/time")
	#@nonl
	#@-node:insertHeadlineTime
	#@+node:toggleActivePane
	def toggleActivePane(self):
		
		c = self.c ; gui = app.gui
		if gui.get_focus(self) == self.bodyCtrl:
			gui.set_focus(c,self.canvas)
		else:
			gui.set_focus(c,self.bodyCtrl)
	#@nonl
	#@-node:toggleActivePane
	#@+node:cascade
	def cascade(self):
	
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
			frame.setTopGeometry(w,h,x,y,adjustSize=false)
	
			# Compute the new offsets.
			x += 30 ; y += 30
			if x > 200:
				x = 10 + delta ; y = 40 + delta
				delta += 10
	#@-node:cascade
	#@+node:equalSizedPanes
	def equalSizedPanes(self):
	
		frame = self
		frame.resizePanesToRatio(0.5,frame.secondary_ratio)
	#@-node:equalSizedPanes
	#@+node:hideLogWindow
	def hideLogWindow (self):
		
		frame = self
		frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)
	#@nonl
	#@-node:hideLogWindow
	#@+node:minimizeAll
	def minimizeAll(self):
	
		self.minimize(app.findFrame)
		self.minimize(app.pythonFrame)
		for frame in app.windowList:
			self.minimize(frame)
		
	def minimize(self, frame):
	
		if frame and frame.top.state() == "normal":
			frame.top.iconify()
	#@nonl
	#@-node:minimizeAll
	#@+node:toggleSplitDirection
	# The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.
	def toggleSplitDirection(self):
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
	#@-node:toggleSplitDirection
	#@+node:leoHelp
	def leoHelp (self):
		
		file = os_path_join(app.loadDir,"..","doc","sbooks.chm")
	
		if os_path_exists(file):
			os.startfile(file)
		else:	
			answer = app.gui.runAskYesNoDialog(
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
						os.chdir(app.loadDir)
						webbrowser.open_new(url)
				except:
					es("exception dowloading sbooks.chm")
					es_exception()
	#@nonl
	#@-node:leoHelp
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
	#@+node:Tk bindings...
	def getFocus(self):
		
		"""Returns the widget that has focus, or body if None."""
		f = self.top.focus_displayof()
		if f:
			return f
		else:
			return self.bodyCtrl
			
	def getTitle (self):
		return self.top.title()
		
	def setTitle (self,title):
		return self.top.title(title)
		
	def get_window_info(self):
		return app.gui.get_window_info(self.top)
		
	def iconify(self):
		self.top.iconify()
	
	def deiconify (self):
		self.top.deiconify()
		
	def lift (self):
		self.top.lift()
		
	def update (self):
		self.top.update()
	#@-node:Tk bindings...
	#@-others
#@nonl
#@-node:class leoTkinterFrame
#@+node:class leoTkinterBody
class leoTkinterBody (leoFrame.leoBody):
	
	"""A class that represents the body pane of a Tkinter window."""

	#@	@+others
	#@+node:tkBody. __init__
	def __init__ (self,frame,parentFrame):
		
		# trace("leoTkinterBody")
		
		# Call the base class constructor.
		leoFrame.leoBody.__init__(self,frame,parentFrame)
	
		self.bodyCtrl = self.createControl(frame,parentFrame)
	
		self.colorizer = leoColor.colorizer(self.c)
	#@nonl
	#@-node:tkBody. __init__
	#@+node:tkBody.createBindings
	def createBindings (self,frame):
		
		t = self.bodyCtrl
		
		# Event handlers...
		t.bind("<Button-1>", frame.OnBodyClick)
		t.bind("<Button-3>", frame.OnBodyRClick)
		t.bind("<Double-Button-1>", frame.OnBodyDoubleClick)
		t.bind("<Key>", frame.body.onBodyKey)
	
		# Gui-dependent commands...
		t.bind(virtual_event_name("Cut"), frame.OnCut)
		t.bind(virtual_event_name("Copy"), frame.OnCopy)
		t.bind(virtual_event_name("Paste"), frame.OnPaste)
	#@nonl
	#@-node:tkBody.createBindings
	#@+node:tkBody.createControl
	def createControl (self,frame,parentFrame):
		
		config = app.config
	
		# A light selectbackground value is needed to make syntax coloring look good.
		wrap = config.getBoolWindowPref('body_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		# Setgrid=1 cause severe problems with the font panel.
		body = Tk.Text(parentFrame,name='body',
			bd=2,bg="white",relief="flat",
			setgrid=0,wrap=wrap, selectbackground="Gray80") 
		
		bodyBar = Tk.Scrollbar(parentFrame,name='bodyBar')
		frame.bodyBar = self.bodyBar = bodyBar
		body['yscrollcommand'] = bodyBar.set
		bodyBar['command'] = body.yview
		bodyBar.pack(side="right", fill="y")
		
		# 8/30/03: Always create the horizontal bar.
		self.bodyXBar = bodyXBar = Tk.Scrollbar(
			parentFrame,name='bodyXBar',orient="horizontal")
		body['xscrollcommand'] = bodyXBar.set
		bodyXBar['command'] = body.xview
		self.bodyXbar = frame.bodyXBar = bodyXBar
		
		if wrap == "none":
			bodyXBar.pack(side="bottom", fill="x")
			
		body.pack(expand=1, fill="both")
	
		if 0: # Causes the cursor not to blink.
			body.configure(insertofftime=0)
			
		return body
	#@nonl
	#@-node:tkBody.createControl
	#@+node:tkBody.setFontFromConfig
	def setFontFromConfig (self):
	
		config = app.config ; body = self.bodyCtrl
		
		font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight",
			config.defaultBodyFontSize, tag = "body")
	
		if app.trace:
			trace(body.cget("font"),font.cget("family"),font.cget("weight"))
	
		body.configure(font=font)
		
		bg = config.getWindowPref("body_text_background_color")
		if bg:
			try: body.configure(bg=bg)
			except:
				es("exception setting body background color")
				es_exception()
		
		fg = config.getWindowPref("body_text_foreground_color")
		if fg:
			try: body.configure(fg=fg)
			except:
				es("exception setting body foreground color")
				es_exception()
	
		bg = config.getWindowPref("body_insertion_cursor_color")
		if bg:
			try: body.configure(insertbackground=bg)
			except:
				es("exception setting insertion cursor color")
				es_exception()
			
		if sys.platform != "win32": # Maybe a Windows bug.
			fg = config.getWindowPref("body_cursor_foreground_color")
			bg = config.getWindowPref("body_cursor_background_color")
			# print fg, bg
			if fg and bg:
				cursor="xterm" + " " + fg + " " + bg
				try: body.configure(cursor=cursor)
				except:
					import traceback ; traceback.print_exc()
	#@nonl
	#@-node:tkBody.setFontFromConfig
	#@+node:body key handlers
	#@+at 
	#@nonl
	# The <Key> event generates the event before the body text is changed(!), 
	# so we register an idle-event handler to do the work later.
	# 
	# 1/17/02: Rather than trying to figure out whether the control or alt 
	# keys are down, we always schedule the idle_handler.  The idle_handler 
	# sees if any change has, in fact, been made to the body text, and sets 
	# the changed and dirty bits only if so.  This is the clean and safe way.
	# 
	# 2/19/02: We must distinguish between commands like "Find, Then Change", 
	# that call onBodyChanged, and commands like "Cut" and "Paste" that call 
	# onBodyWillChange.  The former commands have already changed the body 
	# text, and that change must be captured immediately.  The latter commands 
	# have not changed the body text, and that change may only be captured at 
	# idle time.
	#@-at
	#@@c
	
	#@+others
	#@+node:idle_body_key
	def idle_body_key (self,v,oldSel,undoType,ch=None,oldYview=None,newSel=None,oldText=None):
		
		"""Update the body pane at idle time."""
	
		# trace(ch,ord(ch))
	
		c = self.c
		if not c or not v or v != c.currentVnode():
			return "break"
		if doHook("bodykey1",c=c,v=v,ch=ch,oldSel=oldSel,undoType=undoType):
			return "break" # The hook claims to have handled the event.
		body = v.bodyString()
		if not newSel:
			newSel = c.frame.body.getTextSelection()
		if oldText != None:
			s = oldText
		else:
			s = c.frame.body.getAllText()
		#@	<< return if nothing has changed >>
		#@+node:<< return if nothing has changed >>
		# 6/22/03: Make sure we handle delete key properly.
		
		if ch not in ('\n','\r',chr(8)):
		
			if s == body:
				return "break"
			
			# Do nothing for control characters.
			if (ch == None or len(ch) == 0) and body == s[:-1]:
				return "break"
			
		# print repr(ch),len(body),len(s)
		#@nonl
		#@-node:<< return if nothing has changed >>
		#@nl
		#@	<< set removeTrailing >>
		#@+node:<< set removeTrailing >>
		#@+at 
		#@nonl
		# Tk will add a newline only if:
		# 1. A real change has been made to the Tk.Text widget, and
		# 2. the change did _not_ result in the widget already containing a 
		# newline.
		# 
		# It's not possible to tell, given the information available, what Tk 
		# has actually done. We need only make a reasonable guess here.   
		# setUndoTypingParams stores the number of trailing newlines in each 
		# undo bead, so whatever we do here can be faithfully undone and 
		# redone.
		#@-at
		#@@c
		new = s ; old = body
		
		if len(new) == 0 or new[-1] != '\n':
			# There is no newline to remove.  Probably will never happen.
			# trace("false: no newline to remove")
			removeTrailing = false
		elif len(old) == 0:
			# Ambigous case.
			# trace("false: empty old")
			removeTrailing = ch != '\n' # false
		elif old == new[:-1]:
			# A single trailing character has been added.
			# trace("false: only changed trailing.")
			removeTrailing = false
		else:
			# The text didn't have a newline, and now it does.
			# Moveover, some other change has been made to the text,
			# So at worst we have misreprented the user's intentions slightly.
			# trace("true")
			removeTrailing = true
			
		# trace(ch,removeTrailing)
		
		
		#@-node:<< set removeTrailing >>
		#@nl
		if ch in ('\n','\r'):
			#@		<< Do auto indent >>
			#@+node:<< Do auto indent >> (David McNab)
			# Do nothing if we are in @nocolor mode or if we are executing a Change command.
			if self.frame.body.colorizer.useSyntaxColoring(v) and undoType != "Change":
				# Get the previous line.
				s=c.frame.bodyCtrl.get("insert linestart - 1 lines","insert linestart -1c")
				# Add the leading whitespace to the present line.
				junk,width = skip_leading_ws_with_indent(s,0,c.tab_width)
				if s and len(s) > 0 and s[-1]==':':
					# For Python: increase auto-indent after colons.
					if self.colorizer.scanColorDirectives(v) == "python":
						width += abs(c.tab_width)
				if app.config.getBoolWindowPref("smart_auto_indent"):
					# Added Nov 18 by David McNab, david@rebirthing.co.nz
					# Determine if prev line has unclosed parens/brackets/braces
					brackets = [width]
					tabex = 0
					for i in range(0, len(s)):
						if s[i] == '\t':
							tabex += c.tab_width - 1
						if s[i] in '([{':
							brackets.append(i+tabex + 1)
						elif s[i] in '}])' and len(brackets) > 1:
							brackets.pop()
					width = brackets.pop()
					# end patch by David McNab
				ws = computeLeadingWhitespace (width,c.tab_width)
				if ws and len(ws) > 0:
					c.frame.bodyCtrl.insert("insert", ws)
					removeTrailing = false # bug fix: 11/18
			#@nonl
			#@-node:<< Do auto indent >> (David McNab)
			#@nl
		elif ch == '\t' and c.tab_width < 0:
			#@		<< convert tab to blanks >>
			#@+node:<< convert tab to blanks >>
			# Do nothing if we are executing a Change command.
			if undoType != "Change":
				
				# Get the characters preceeding the tab.
				prev=c.frame.bodyCtrl.get("insert linestart","insert -1c")
				
				if 1: # 6/26/03: Convert tab no matter where it is.
			
					w = computeWidth(prev,c.tab_width)
					w2 = (abs(c.tab_width) - (w % abs(c.tab_width)))
					# trace("prev w:",w,"prev chars:",prev)
					c.frame.bodyCtrl.delete("insert -1c")
					c.frame.bodyCtrl.insert("insert",' ' * w2)
				
				else: # Convert only leading tabs.
				
					# Get the characters preceeding the tab.
					prev=c.frame.bodyCtrl.get("insert linestart","insert -1c")
			
					# Do nothing if there are non-whitespace in prev:
					all_ws = true
					for ch in prev:
						if ch != ' ' and ch != '\t':
							all_ws = false
					if all_ws:
						w = computeWidth(prev,c.tab_width)
						w2 = (abs(c.tab_width) - (w % abs(c.tab_width)))
						# trace("prev w:",w,"prev chars:",prev)
						c.frame.bodyCtrl.delete("insert -1c")
						c.frame.bodyCtrl.insert("insert",' ' * w2)
			#@nonl
			#@-node:<< convert tab to blanks >>
			#@nl
		#@	<< set s to widget text, removing trailing newlines if necessary >>
		#@+node:<< set s to widget text, removing trailing newlines if necessary >>
		s = c.frame.body.getAllText()
		if len(s) > 0 and s[-1] == '\n' and removeTrailing:
			s = s[:-1]
		#@nonl
		#@-node:<< set s to widget text, removing trailing newlines if necessary >>
		#@nl
		if undoType: # 11/6/03: set oldText properly when oldText param exists.
			if not oldText: oldText = body
			newText = s
			c.undoer.setUndoTypingParams(v,undoType,oldText,newText,oldSel,newSel,oldYview=oldYview)
		v.t.setTnodeText(s)
		v.t.insertSpot = c.frame.body.getInsertionPoint()
		#@	<< recolor the body >>
		#@+node:<< recolor the body >>
		self.frame.scanForTabWidth(v)
		
		incremental = undoType not in ("Cut","Paste") and not self.forceFullRecolorFlag
		self.frame.body.recolor_now(v,incremental=incremental)
		
		self.forceFullRecolorFlag = false
		#@nonl
		#@-node:<< recolor the body >>
		#@nl
		if not c.changed:
			c.setChanged(true)
		#@	<< redraw the screen if necessary >>
		#@+node:<< redraw the screen if necessary >>
		redraw_flag = false
		
		c.beginUpdate()
		
		# Update dirty bits.
		if not v.isDirty() and v.setDirty(): # Sets all cloned and @file dirty bits
			redraw_flag = true
			
		# Update icons.
		val = v.computeIcon()
		if val != v.iconVal:
			v.iconVal = val
			redraw_flag = true
		
		c.endUpdate(redraw_flag) # redraw only if necessary
		#@nonl
		#@-node:<< redraw the screen if necessary >>
		#@nl
		doHook("bodykey2",c=c,v=v,ch=ch,oldSel=oldSel,undoType=undoType)
		return "break"
	#@nonl
	#@-node:idle_body_key
	#@+node:onBodyChanged (called from core)
	# Called by command handlers that have already changed the text.
	
	def onBodyChanged (self,v,undoType,oldSel=None,oldYview=None,newSel=None,oldText=None):
		
		"""Handle a change to the body pane."""
		
		c = self.c
		if not v:
			v = c.currentVnode()
	
		if not oldSel:
			oldSel = c.frame.body.getTextSelection()
	
		self.idle_body_key(v,oldSel,undoType,oldYview=oldYview,newSel=newSel,oldText=oldText)
	#@-node:onBodyChanged (called from core)
	#@+node:onBodyKey
	def onBodyKey (self,event):
		
		"""Handle any key press event in the body pane."""
	
		c = self.c ; v = c.currentVnode()
		ch = event.char 
		oldSel = c.frame.body.getTextSelection()
					
		if 0: # won't work when menu keys are bound.
			self.handleStatusLineKey(event)
			
		# We must execute this even if len(ch) > 0 to delete spurious trailing newlines.
		self.c.frame.bodyCtrl.after_idle(self.idle_body_key,v,oldSel,"Typing",ch)
	#@-node:onBodyKey
	#@+node:handleStatusLineKey
	def handleStatusLineKey (self,event):
		
		c = self.c ; frame = c.frame
		ch = event.char ; keysym = event.keysym
		keycode = event.keycode ; state = event.state
	
		if 1: # ch and len(ch)>0:
			#@		<< trace the key event >>
			#@+node:<< trace the key event >>
			try:    self.keyCount += 1
			except: self.keyCount  = 1
			
			printable = choose(ch == keysym and state < 4,"printable","")
			
			print "%4d %s %d %s %x %s" % (
				self.keyCount,repr(ch),keycode,keysym,state,printable)
			#@nonl
			#@-node:<< trace the key event >>
			#@nl
	
		try:
			status = self.keyStatus
		except:
			status = [] ; frame.clearStatusLine()
		
		for sym,name in (
			("Alt_L","Alt"),("Alt_R","Alt"),
			("Control_L","Control"),("Control_R","Control"),
			("Escape","Esc"),
			("Shift_L","Shift"), ("Shift_R","Shift")):
			if keysym == sym:
				if name not in status:
					status.append(name)
					frame.putStatusLine(name + ' ')
				break
		else:
			status = [] ; frame.clearStatusLine()
	
		self.keyStatus = status
	#@nonl
	#@-node:handleStatusLineKey
	#@+node:onBodyWillChange
	# Called by command handlers that change the text just before idle time.
	
	def onBodyWillChange (self,v,undoType,oldSel=None,oldYview=None):
		
		"""Queue the body changed idle handler."""
		
		c = self.c
		if not v: v = c.currentVnode()
		if not oldSel:
			oldSel = c.frame.body.getTextSelection()
			
		#trace()
		self.c.frame.bodyCtrl.after_idle(self.idle_body_key,v,oldSel,undoType,oldYview)
	
	#@-node:onBodyWillChange
	#@-others
	#@nonl
	#@-node:body key handlers
	#@+node:forceRecolor
	def forceFullRecolor (self):
		
		self.forceFullRecolorFlag = true
	#@nonl
	#@-node:forceRecolor
	#@+node:Tk bindings (leoTkinterBody)
	#@+at
	# I could have used this to redirect all calls from the body class and the 
	# bodyCtrl to Tk. OTOH:
	# 
	# 1. Most of the wrappers do more than the old Tk routines now and
	# 2. The wrapper names are more discriptive than the Tk names.
	# 
	# Still, using the Tk names would have had its own appeal.  If I had 
	# prefixed the tk routine with tk_ the __getatt__ routine could have 
	# stripped it off!
	#@-at
	#@@c
	
	if 0: # This works.
		def __getattr__(self,attr):
			return getattr(self.bodyCtrl,attr)
			
	if 0: # This would work if all tk wrapper routines were prefixed with tk_
		def __getattr__(self,attr):
			if attr[0:2] == "tk_":
				return getattr(self.bodyCtrl,attr[3:])
	#@nonl
	#@-node:Tk bindings (leoTkinterBody)
	#@+node:Bounding box (Tk spelling)
	def bbox(self,index):
	
		return self.bodyCtrl.bbox(index)
	#@nonl
	#@-node:Bounding box (Tk spelling)
	#@+node:Color tags (Tk spelling)
	# Could have been replaced by the __getattr__ routine above...
	# 12/19/03: no: that would cause more problems.
	
	def tag_add (self,tagName,index1,index2):
		self.bodyCtrl.tag_add(tagName,index1,index2)
	
	def tag_bind (self,tagName,event,callback):
		self.bodyCtrl.tag_bind(tagName,event,callback)
	
	def tag_configure (self,colorName,**keys):
		self.bodyCtrl.tag_configure(colorName,keys)
	
	def tag_delete(self,tagName):
		self.bodyCtrl.tag_delete(tagName)
	
	def tag_remove (self,tagName,index1,index2):
		return self.bodyCtrl.tag_remove(tagName,index1,index2)
	#@nonl
	#@-node:Color tags (Tk spelling)
	#@+node:Configuration (Tk spelling)
	def cget(self,*args,**keys):
		
		val = self.bodyCtrl.cget(*args,**keys)
		
		if app.trace:
			trace(val,args,keys)
	
		return val
		
	def configure (self,*args,**keys):
		
		if app.trace:
			trace(args,keys)
		
		return self.bodyCtrl.configure(*args,**keys)
	#@nonl
	#@-node:Configuration (Tk spelling)
	#@+node:Focus
	def hasFocus (self):
		
		return self.bodyCtrl == self.frame.top.focus_displayof()
		
	def setFocus (self):
		
		self.bodyCtrl.focus_set()
	#@nonl
	#@-node:Focus
	#@+node:Height & width
	def getBodyPaneHeight (self):
		
		return self.bodyCtrl.winfo_height()
	
	def getBodyPaneWidth (self):
		
		return self.bodyCtrl.winfo_width()
	#@nonl
	#@-node:Height & width
	#@+node:Idle time...
	def scheduleIdleTimeRoutine (self,function,*args,**keys):
	
		self.bodyCtrl.after_idle(function,*args,**keys)
	#@nonl
	#@-node:Idle time...
	#@+node:adjustIndex
	def adjustIndex (self,index,offset):
		
		t = self.bodyCtrl
		return t.index("%s + %dc" % (t.index(index),offset))
	#@nonl
	#@-node:adjustIndex
	#@+node:compareIndices
	def compareIndices(self,i,rel,j):
	
		return self.bodyCtrl.compare(i,rel,j)
	#@nonl
	#@-node:compareIndices
	#@+node:convertRowColumnToIndex
	def convertRowColumnToIndex (self,row,column):
		
		return self.bodyCtrl.index("%s.%s" % (row,column))
	#@nonl
	#@-node:convertRowColumnToIndex
	#@+node:convertIndexToRowColumn
	def convertIndexToRowColumn (self,index):
		
		index = self.bodyCtrl.index(index)
		start, end = string.split(index,'.')
		return int(start),int(end)
	#@nonl
	#@-node:convertIndexToRowColumn
	#@+node:getImageIndex
	def getImageIndex (self,image):
		
		return self.bodyCtrl.index(image)
	#@nonl
	#@-node:getImageIndex
	#@+node:tkIndex (internal use only)
	def tkIndex(self,index):
		
		"""Returns the canonicalized Tk index."""
		
		if index == "start": index = "1.0"
		
		return self.bodyCtrl.index(index)
	#@nonl
	#@-node:tkIndex (internal use only)
	#@+node:getInsertionPoint & getBeforeInsertionPoint
	def getBeforeInsertionPoint (self):
		
		return self.bodyCtrl.index("insert-1c")
	
	def getInsertionPoint (self):
		
		return self.bodyCtrl.index("insert")
	#@nonl
	#@-node:getInsertionPoint & getBeforeInsertionPoint
	#@+node:getCharAtInsertPoint & getCharBeforeInsertPoint
	def getCharAtInsertPoint (self):
		
		s = self.bodyCtrl.get("insert")
		return toUnicode(s,app.tkEncoding)
	
	def getCharBeforeInsertPoint (self):
	
		s = self.bodyCtrl.get("insert -1c")
		return toUnicode(s,app.tkEncoding)
	#@nonl
	#@-node:getCharAtInsertPoint & getCharBeforeInsertPoint
	#@+node:makeInsertPointVisible
	def makeInsertPointVisible (self):
		
		self.bodyCtrl.see("insert -5l")
	#@nonl
	#@-node:makeInsertPointVisible
	#@+node:setInsertionPointTo...
	def setInsertionPoint (self,index):
		self.bodyCtrl.mark_set("insert",index)
	
	def setInsertionPointToEnd (self):
		self.bodyCtrl.mark_set("insert","end")
		
	def setInsertPointToStartOfLine (self,lineNumber): # zero-based line number
		self.bodyCtrl.mark_set("insert",str(1+lineNumber)+".0 linestart")
	#@nonl
	#@-node:setInsertionPointTo...
	#@+node:Menus
	def bind (self,*args,**keys):
		
		return self.bodyCtrl.bind(*args,**keys)
	#@-node:Menus
	#@+node:deleteTextSelection
	def deleteTextSelection (self):
		
		t = self.bodyCtrl
		sel = t.tag_ranges("sel")
		if len(sel) == 2:
			start,end = sel
			if t.compare(start,"!=",end):
				t.delete(start,end)
	#@nonl
	#@-node:deleteTextSelection
	#@+node:getSelectedText
	def getSelectedText (self):
		
		"""Return the selected text of the body frame, converted to unicode."""
	
		start, end = self.getTextSelection()
		if start and end and start != end:
			s = self.bodyCtrl.get(start,end)
			if s is None:
				return u""
			else:
				return toUnicode(s,app.tkEncoding)
		else:
			return None
	#@nonl
	#@-node:getSelectedText
	#@+node:getTextSelection
	def getTextSelection (self):
		
		"""Return a tuple representing the selected range of body text.
		
		Return a tuple giving the insertion point if no range of text is selected."""
	
		bodyCtrl = self.bodyCtrl
		sel = bodyCtrl.tag_ranges("sel")
	
		if len(sel) == 2:
			return sel
		else:
			# Return the insertion point if there is no selected text.
			insert = bodyCtrl.index("insert")
			return insert,insert
	#@nonl
	#@-node:getTextSelection
	#@+node:hasTextSelection
	def hasTextSelection (self):
	
		sel = self.bodyCtrl.tag_ranges("sel")
		return sel and len(sel) == 2
	#@nonl
	#@-node:hasTextSelection
	#@+node:selectAllText
	def selectAllText (self):
		
		app.gui.setTextSelection(self.bodyCtrl,"1.0","end")
	#@-node:selectAllText
	#@+node:setTextSelection
	def setTextSelection (self,i,j=None):
		
		# Allow the user to pass either a 2-tuple or two separate args.
		if i is None:
			i,j = "1.0","1.0"
		elif len(i) == 2:
			i,j = i
	
		app.gui.setTextSelection(self.bodyCtrl,i,j)
	#@nonl
	#@-node:setTextSelection
	#@+node:delete...
	def deleteAllText(self):
		self.bodyCtrl.delete("1.0","end")
	
	def deleteCharacter (self,index):
		t = self.bodyCtrl
		t.delete(t.index(index))
		
	def deleteLastChar (self):
		self.bodyCtrl.delete("end-1c")
		
	def deleteLine (self,lineNumber): # zero based line number.
		self.bodyCtrl.delete(str(1+lineNumber)+".0","end")
		
	def deleteLines (self,line1,numberOfLines): # zero based line numbers.
		self.bodyCtrl.delete(str(1+line1)+".0",str(1+line1+numberOfLines-1)+".0 lineend")
		
	def deleteRange (self,index1,index2):
		t = self.bodyCtrl
		t.delete(t.index(index1),t.index(index2))
	#@nonl
	#@-node:delete...
	#@+node:getAllText
	def getAllText (self):
		
		"""Return all the body text, converted to unicode."""
		
		s = self.bodyCtrl.get("1.0","end")
		if s is None:
			return u""
		else:
			return toUnicode(s,app.tkEncoding)
	#@nonl
	#@-node:getAllText
	#@+node:getCharAtIndex
	def getCharAtIndex (self,index):
		
		"""Return all the body text, converted to unicode."""
		
		s = self.bodyCtrl.get(index)
		if s is None:
			return u""
		else:
			return toUnicode(s,app.tkEncoding)
	#@nonl
	#@-node:getCharAtIndex
	#@+node:getInsertLines
	def getInsertLines (self):
		
		"""Return before,after where:
			
		before is all the lines before the line containing the insert point.
		sel is the line containing the insert point.
		after is all the lines after the line containing the insert point.
		
		All lines end in a newline, except possibly the last line."""
		
		t = self.bodyCtrl
	
		before = t.get("1.0","insert linestart")
		ins    = t.get("insert linestart","insert lineend + 1c")
		after  = t.get("insert lineend + 1c","end")
	
		before = toUnicode(before,app.tkEncoding)
		ins    = toUnicode(ins,   app.tkEncoding)
		after  = toUnicode(after ,app.tkEncoding)
	
		return before,ins,after
	#@nonl
	#@-node:getInsertLines
	#@+node:getSelectionAreas
	def getSelectionAreas (self):
		
		"""Return before,sel,after where:
			
		before is the text before the selected text
		(or the text before the insert point if no selection)
		sel is the selected text (or "" if no selection)
		after is the text after the selected text
		(or the text after the insert point if no selection)"""
		
		trace()
		t = self.bodyCtrl
		
		sel_index = t.getTextSelection()
		if len(sel_index) == 2:
			i,j = sel_index
			sel = t.get(i,j)
		else:
			i = j = t.index("insert")
			sel = ""
	
		before = t.get("1.0",i)
		after  = t.get(j,"end")
		
		before = toUnicode(before,app.tkEncoding)
		sel    = toUnicode(sel,   app.tkEncoding)
		after  = toUnicode(after ,app.tkEncoding)
		return before,sel,after
	#@nonl
	#@-node:getSelectionAreas
	#@+node:getSelectionLines (tkBody)
	def getSelectionLines (self):
		
		"""Return before,sel,after where:
			
		before is the all lines before the selected text
		(or the text before the insert point if no selection)
		sel is the selected text (or "" if no selection)
		after is all lines after the selected text
		(or the text after the insert point if no selection)"""
		
		# At present, called only by c.getBodyLines.
	
		t = self.bodyCtrl
		sel_index = t.tag_ranges("sel") 
		if len(sel_index) != 2:
			if 1: # Choose the insert line.
				index = t.index("insert")
				sel_index = index,index
			else:
				return "","","" # Choose everything.
	
		i,j = sel_index
		i = t.index(i + "linestart")
		j = t.index(j + "lineend") # 10/24/03: -1c  # 11/4/03: no -1c.
		before = toUnicode(t.get("1.0",i),app.tkEncoding)
		sel    = toUnicode(t.get(i,j),    app.tkEncoding)
		after  = toUnicode(t.get(j,"end-1c"),app.tkEncoding)
		
		# trace(i,j)
		return before,sel,after
	#@nonl
	#@-node:getSelectionLines (tkBody)
	#@+node:getTextRange
	def getTextRange (self,index1,index2):
		
		t = self.bodyCtrl
		return t.get(t.index(index1),t.index(index2))
	#@nonl
	#@-node:getTextRange
	#@+node:insertAtInsertPoint
	def insertAtInsertPoint (self,s):
		
		self.bodyCtrl.insert("insert",s)
	#@nonl
	#@-node:insertAtInsertPoint
	#@+node:insertAtEnd
	def insertAtEnd (self,s):
		
		self.bodyCtrl.insert("end",s)
	#@nonl
	#@-node:insertAtEnd
	#@+node:insertAtStartOfLine
	def insertAtStartOfLine (self,lineNumber,s):
		
		self.bodyCtrl.insert(str(1+lineNumber)+".0",s)
	#@nonl
	#@-node:insertAtStartOfLine
	#@+node:setSelectionAreas
	def setSelectionAreas (self,before,sel,after):
		
		"""Replace the body text by before + sel + after and
		set the selection so that the sel text is selected."""
	
		t = self.bodyCtrl ; gui = app.gui
		t.delete("1.0","end")
	
		if before: t.insert("1.0",before)
		sel_start = t.index("end-1c") # 10/24/03: -1c
	
		if sel: t.insert("end",sel)
		sel_end = t.index("end")
	
		if after:
			# A horrible Tk kludge.  Remove a trailing newline so we don't keep extending the text.
			if after[-1] == '\n':
				after = after[:-1]
			t.insert("end",after)
	
		gui.setTextSelection(t,sel_start,sel_end)
		# trace(sel_start,sel_end)
		
		return t.index(sel_start), t.index(sel_end)
	#@nonl
	#@-node:setSelectionAreas
	#@+node:Visibility & scrolling
	def makeIndexVisible (self,index):
		
		self.bodyCtrl.see(index)
		
	def setFirstVisibleIndex (self,index):
		
		self.bodyCtrl.yview("moveto",index)
		
	def getYScrollPosition (self):
		
		return self.bodyCtrl.yview()
		
	def setYScrollPosition (self,scrollPosition):
	
		if len(scrollPosition) == 2:
			first,last = scrollPosition
		else:
			first = scrollPosition
		self.bodyCtrl.yview("moveto",first)
		
	def scrollUp (self):
		
		self.bodyCtrl.yview("scroll",-1,"units")
		
	def scrollDown (self):
	
		self.bodyCtrl.yview("scroll",1,"units")
	#@nonl
	#@-node:Visibility & scrolling
	#@-others
#@nonl
#@-node:class leoTkinterBody
#@+node:class leoTkinterLog
class leoTkinterLog (leoFrame.leoLog):
	
	"""A class that represents the log pane of a Tkinter window."""

	#@	@+others
	#@+node:tkLog.__init__
	def __init__ (self,frame,parentFrame):
		
		# trace("leoTkinterLog")
		
		# Call the base class constructor.
		leoFrame.leoLog.__init__(self,frame,parentFrame)
		
		self.colorTags = [] # list of color names used as tags in log window.
		
		self.logCtrl.bind("<Button-1>", self.onActivateLog)
	#@nonl
	#@-node:tkLog.__init__
	#@+node:tkLog.configureBorder & configureFont
	def configureBorder(self,border):
		
		self.logCtrl.configure(bd=border)
		
	def configureFont(self,font):
	
		self.logCtrl.configure(font=font)
	#@nonl
	#@-node:tkLog.configureBorder & configureFont
	#@+node:tkLog.createControl
	def createControl (self,parentFrame):
		
		config = app.config
		
		wrap = config.getBoolWindowPref('log_pane_wraps')
		wrap = choose(wrap,"word","none")
	
		log = Tk.Text(parentFrame,name="log",
			setgrid=0,wrap=wrap,bd=2,bg="white",relief="flat")
		
		self.logBar = logBar = Tk.Scrollbar(parentFrame,name="logBar")
	
		log['yscrollcommand'] = logBar.set
		logBar['command'] = log.yview
		
		logBar.pack(side="right", fill="y")
		# rr 8/14/02 added horizontal elevator 
		if wrap == "none": 
			logXBar = Tk.Scrollbar( 
				parentFrame,name='logXBar',orient="horizontal") 
			log['xscrollcommand'] = logXBar.set 
			logXBar['command'] = log.xview 
			logXBar.pack(side="bottom", fill="x")
		log.pack(expand=1, fill="both")
	
		return log
	#@nonl
	#@-node:tkLog.createControl
	#@+node:tkLog.getFontConfig
	def getFontConfig (self):
	
		font = self.logCtrl.cget("font")
		# trace(font)
		return font
	#@nonl
	#@-node:tkLog.getFontConfig
	#@+node:tkLog.hasFocus
	def hasFocus (self):
		
		return app.gui.get_focus(self.frame) == self.logCtrl
	#@nonl
	#@-node:tkLog.hasFocus
	#@+node:tkLog.onActivateLog
	def onActivateLog (self,event=None):
	
		try:
			app.setLog(self,"OnActivateLog")
			self.frame.tree.OnDeactivate()
		except:
			es_event_exception("activate log")
	#@nonl
	#@-node:tkLog.onActivateLog
	#@+node:tkLog.put & putnl
	# All output to the log stream eventually comes here.
	
	def put (self,s,color=None):
		if app.quitting: return
		if self.logCtrl:
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,app.tkEncoding)
			if color:
				if color not in self.colorTags:
					self.colorTags.append(color)
					self.logCtrl.tag_config(color,foreground=color)
				self.logCtrl.insert("end",s)
				self.logCtrl.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
				if "black" not in self.colorTags:
					self.colorTags.append("black")
					self.logCtrl.tag_config("black",foreground="black")
				self.logCtrl.tag_add("black","end")
			else:
				self.logCtrl.insert("end",s)
			self.logCtrl.see("end")
			self.logCtrl.update_idletasks()
		else:
			app.logWaiting.append((s,color),) # 2/25/03
			print "Null tkinter log"
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,"ascii")
			print s
	
	def putnl (self):
		if app.quitting: return
		if self.logCtrl:
			self.logCtrl.insert("end",'\n')
			self.logCtrl.see("end")
			self.logCtrl.update_idletasks()
		else:
			app.logWaiting.append(('\n',"black"),) # 6/28/03
			print "Null tkinter log"
			print
	#@nonl
	#@-node:tkLog.put & putnl
	#@+node:tkLog.setFontFromConfig
	def setFontFromConfig (self):
	
		logCtrl = self.logCtrl ; config = app.config
	
		font = config.getFontFromParams(
			"log_text_font_family", "log_text_font_size",
			"log_text_font_slant",  "log_text_font_weight",
			config.defaultLogFontSize)
		
		logCtrl.configure(font=font)
	
		bg = config.getWindowPref("log_text_background_color")
		if bg:
			try: logCtrl.configure(bg=bg)
			except: pass
		
		fg = config.getWindowPref("log_text_foreground_color")
		if fg:
			try: logCtrl.configure(fg=fg)
			except: pass
	#@nonl
	#@-node:tkLog.setFontFromConfig
	#@-others
#@nonl
#@-node:class leoTkinterLog
#@-others
#@nonl
#@-node:@file leoTkinterFrame.py
#@-leo
