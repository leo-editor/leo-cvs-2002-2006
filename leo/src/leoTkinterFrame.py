# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoTkinterFrame.py
#@@first

# To do: Use config params for window height, width and bar color, relief and width.

#@@language python

from leoGlobals import *
import leoColor,leoCommands,leoFrame,leoNodes,leoPlugins
import leoTkinterMenu,leoTkinterTree
import Tkinter,tkFont
import os,string,sys,time,traceback

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
	
		frame.canvas = canvas = Tk.Canvas(parentFrame,name="canvas",
			bd=0,bg="white",relief="flat")
			
		frame.setTreeColorsFromConfig()
	
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
			
		# print_bindings("canvas",frame.tree.canvas)
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
		
		# Create the canvas.
		self.createCanvas(self.split2Pane1)
		# Create the log class.
		c.log  = frame.log = leoTkinterLog(frame,self.split2Pane2)
		# Create the body class.
		c.body = frame.body = leoTkinterBody(frame,self.split1Pane2)
		frame.bodyCtrl = frame.body.bodyCtrl
		# Create the tree class.
		frame.tree = leoTkinterTree.leoTkinterTree(c,frame,frame.canvas)
		# Configure.
		frame.setTabWidth(c.tab_width)
		self.reconfigurePanes()
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
		c.frame.redraw()
		c.frame.getFocus()
		c.editVnode(v)
		c.endUpdate(false)
		#@nonl
		#@-node:<< create the first tree node >>
		#@nl
	
		self.menu = leoTkinterMenu.leoTkinterMenu(frame)
		self.body.createBindings(frame)
	
		v = c.currentVnode()
		if not doHook("menu1",c=c,v=v):
			frame.menu.createMenuBar(self)
	
		app.setLog(self.log,"tkinterFrame.__init__") # the leoTkinterFrame containing the log
	
		app.windowList.append(frame)
		
		c.initVersion()
		c.signOnWithVersion()
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
					imagefile = toUnicode(imagefile,app.tkEncoding) # 10/20/03
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
			index = c.body.getInsertionPoint()
			row,col = c.body.indexToRowColumn(index)
			index1 = c.body.rowColumnToIndex(row,0)
		else:
			index = body.index("insert")
			row,col = gui.getindex(body,index)
		
		if col > 0:
			if 0: # new code
				s = c.body.getRange(index1,index2)
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
	
		frame = self ; c = self.c ; tree = frame.tree
	
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
		clearAllIvars(tree.colorizer)
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
		
		f = self ; c = f.c
		
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
		f.log.setFontFromConfig()
		c.redraw()
	#@nonl
	#@-node:f.reconfigureFromConfig
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
	#@+node:f.setTabWidth
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
	#@-node:f.setWrap
	#@+node:f.reconfigurePanes (use config bar_width)
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
	#@-node:f.reconfigurePanes (use config bar_width)
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
			c = self.c ; gui = app.gui
			app.setLog(self.log,"OnActivateBody")
			self.tree.OnDeactivate()
			gui.set_focus(c,self.body.bodyCtrl) # Reference to bodyCtrl is allowable in an event handler.
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
	
		try:
			app.setLog(None,"OnDeactivateLeoEvent")
		except:
			es_event_exception("deactivate Leo")
	#@nonl
	#@-node:OnActivateLeoEvent, OnDeactivateLeoEvent
	#@+node:OnActivateTree
	def OnActivateTree (self,event=None):
	
		try:
			c = self.c ; gui = app.gui
			app.setLog(self.log,"OnActivateTree")
			self.tree.undimEditLabel()
			gui.set_focus(c,c.frame.bodyCtrl) # 7/12/03
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
	#@+node:frame.OnCut, OnCutFrom Menu
	def OnCut (self,event=None):
	
		# Activate the body key handler by hand.
		c = self ; v = c.currentVnode()
		c.tree.forceFullRecolor()
		c.tree.onBodyWillChange(v,"Cut")
	
	def OnCutFromMenu (self):
	
		w = self.getFocus()
		c.tree.forceFullRecolor()
		w.event_generate(virtual_event_name("Cut"))
		
		# 11/2/02: Make sure the event sticks.
		c = self ; v = c.currentVnode()
		c.frame.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	#@-node:frame.OnCut, OnCutFrom Menu
	#@+node:frame.OnCopy, OnCopyFromMenu
	def OnCopy (self,event=None):
	
		# Copy never changes dirty bits or syntax coloring.
		pass
		
	def OnCopyFromMenu (self):
	
		# trace()
		c = self
		w = c.frame.getFocus()
		w.event_generate(virtual_event_name("Copy"))
	#@nonl
	#@-node:frame.OnCopy, OnCopyFromMenu
	#@+node:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	def OnPaste (self,event=None):
	
		# Activate the body key handler by hand.
		c = self ; v = c.currentVnode()
		self.tree.forceFullRecolor()
		#trace()
		self.tree.onBodyWillChange(v,"Paste")
		
	def OnPasteFromMenu (self):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Paste"))
		
		# 10/23/02: Make sure the event sticks.
		c = self ; v = c.currentVnode()
		self.tree.forceFullRecolor()
		#trace()
		c.frame.onHeadChanged(v) # Works even if it wasn't the headline that changed.
	
	#@-node:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+node:insertHeadlineTime
	def insertHeadlineTime (self):
	
		frame = self ; c = frame.c ; v = c.currentVnode()
		h = v.headString() # Remember the old value.
	
		if v.edit_text():
			sel1,sel2 = app.gui.getTextSelection(v.edit_text())
			if sel1 and sel2 and sel1 != sel2: # 7/7/03
				v.edit_text().delete(sel1,sel2)
			v.edit_text().insert("insert",c.getTime(body=false))
			frame.idle_head_key(v)
	
		# A kludge to get around not knowing whether we are editing or not.
		if h.strip() == v.headString().strip():
			es("Edit headline to append date/time")
	#@nonl
	#@-node:insertHeadlineTime
	#@+node:endEditLabelCommand
	def endEditLabelCommand (self):
	
		c = self.c ; tree = self.tree ; v = self.editVnode ; gui = app.gui
	
		# trace(v)
		if v and v.edit_text():
			tree.select(v)
		if v: # Bug fix 10/9/02: also redraw ancestor headlines.
			# 3/26/03: changed redraw_now to force_redraw.
			tree.force_redraw() # force a redraw of joined headlines.
	
		gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02
	#@nonl
	#@-node:endEditLabelCommand
	#@+node:abortEditLabelCommand
	def abortEditLabelCommand (self):
		
		c = self.c ; v = c.currentVnode ; tree = self.tree
		# trace(v)
		if self.revertHeadline and v.edit_text() and v == self.editVnode:
			
			# trace(`self.revertHeadline`)
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("end",self.revertHeadline)
			tree.idle_head_key(v) # Must be done immediately.
			tree.revertHeadline = None
			tree.select(v)
			if v and len(v.t.joinList) > 0:
				# 3/26/03: changed redraw_now to force_redraw.
				tree.force_redraw() # force a redraw of joined headlines.
	#@nonl
	#@-node:abortEditLabelCommand
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
			geom = "%dx%d%+d%+d" % (w,h,x,y)
			frame.setTopGeometry(geom) # frame.top.geometry("%dx%d%+d%+d" % (w,h,x,y))
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
	
	def setTopGeometry(self,geom):
		self.top.geometry(geom)
		
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
	#@nonl
	#@-node:Tk bindings...
	#@+node:Redirection routines...
	#@+at 
	#@nonl
	# These are hard to remove, because there is no official tree class yet.
	#@-at
	#@nonl
	#@-node:Redirection routines...
	#@+node:Coloring 
	# It's weird to have the tree class be responsible for coloring the body pane!
	
	def getColorizer(self):
		
		return self.tree.colorizer
	
	def recolor_now(self,v):
		
		return self.tree.recolor_now(v)
	
	def recolor_range(self,v,leading,trailing):
		
		return self.tree.recolor_range(v,leading,trailing)
	
	def recolor(self,v,incremental=false):
		
		return self.tree.recolor(v,incremental)
		
	def updateSyntaxColorer(self,v):
		
		return self.tree.colorizer.updateSyntaxColorer(v)
	#@-node:Coloring 
	#@+node:Drawing
	def beginUpdate(self):
	
		return self.tree.beginUpdate()
	
	def endUpdate(self,flag=true):
	
		return self.tree.endUpdate(flag)
	
	def drawIcon(self,v,x=None,y=None):
	
		return self.tree.drawIcon(v,x,y)
	
	def redraw(self):
	
		return self.tree.redraw()
	
	def redraw_now(self):
	
		return self.tree.redraw_now()
	#@nonl
	#@-node:Drawing
	#@+node:Editing
	def editLabel(self,v):
		
		return self.tree.editLabel(v)
	
	def editVnode(self):
		
		return self.tree.editVnode
	
	def endEditLabel(self):
		
		return self.tree.endEditLabel()
		
	def getEditTextDict(self,v):
		
		return self.tree.edit_text_dict.get(v)
	
	def setEditVnode(self,v):
		
		self.tree.editVnode = v
	
	def setNormalLabelState(self,v):
		
		return self.tree.setNormalLabelState(v)
	#@-node:Editing
	#@+node:Fonts
	def getFont(self):
		
		return self.tree.getFont()
		
	def setFont(self,font):
		
		return self.tree.setFont(font)
	#@nonl
	#@-node:Fonts
	#@+node:Getters & setters
	# Getters...
	def currentVnode(self):
		return self.tree.currentVnode
		
	def dragging(self):
		return self.tree.dragging
	
	def rootVnode(self):
		return self.tree.rootVnode
	
	def topVnode(self):
		return self.tree.topVnode
	
	# Setters...
	
	def setCurrentVnode(self,v):
		self.tree.currentVnode = v
	
	def setRootVnode(self,v):
		self.tree.rootVnode = v
		
	def setTreeIniting(self,flag):
		self.tree.initing = flag
	#@nonl
	#@-node:Getters & setters
	#@+node:Notifications
	# These should all be internal to the tkinter.frame class.
	
	def OnActivateHeadline(self,v):
		return self.tree.OnActivate(v)
		
	def onBodyChanged(self,*args,**keys):
		return self.tree.onBodyChanged(*args,**keys)
	
	def onHeadChanged(self,*args,**keys):
		return self.tree.onHeadChanged(*args,**keys)
	
	def OnHeadlineKey(self,v,event):
		return self.tree.OnHeadlineKey(v,event)
	
	def idle_head_key(self,v):
		return self.tree.idle_head_key(v)
	#@nonl
	#@-node:Notifications
	#@+node:Scrolling
	def scrollTo(self,v):
		
		return self.tree.scrollTo(v)
	
	def idle_scrollTo(self,v):
		
		return self.tree.idle_scrollTo(v)
	
	
	#@-node:Scrolling
	#@+node:Selecting
	def select(self,v,updateBeadList=true):
		
		return self.tree.select(v,updateBeadList)
	#@-node:Selecting
	#@+node:Tree operations
	def expandAllAncestors(self,v):
		
		return self.tree.expandAllAncestors(v)
	#@nonl
	#@-node:Tree operations
	#@-others
#@nonl
#@-node:class leoTkinterFrame
#@+node:class leoTkinterBody
class leoTkinterBody (leoFrame.leoBody):
	
	"""A class that represents the body pane of a Tkinter window."""

	#@	@+others
	#@+node:tkBody.__init__
	def __init__ (self,frame,parentFrame):
		
		# trace("leoTkinterBody")
		
		# Call the base class constructor.
		leoFrame.leoBody.__init__(self,frame,parentFrame)
	#@nonl
	#@-node:tkBody.__init__
	#@+node:tkBody.createBindings
	def createBindings (self,frame):
		
		t = self.bodyCtrl
		
		# Event handlers...
		t.bind("<Button-1>", frame.OnBodyClick)
		t.bind("<Button-3>", frame.OnBodyRClick)
		t.bind("<Double-Button-1>", frame.OnBodyDoubleClick)
		t.bind("<Key>", frame.tree.OnBodyKey)
	
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
	#@+node:tkBody.setBodyFontFromConfig
	def setBodyFontFromConfig (self):
		
		config = app.config ; body = self.bodyCtrl
		
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
	#@-node:tkBody.setBodyFontFromConfig
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
		
		return self.bodyCtrl.cget(*args,**keys)
		
	def configure (self,*args,**keys):
		
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
		if len(i) == 2:
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
	#@+node:getInsertLines (leoTkinterBody)
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
	#@-node:getInsertLines (leoTkinterBody)
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
	#@+node:getSelectionLines
	def getSelectionLines (self):
		
		"""Return before,sel,after where:
			
		before is the all lines before the selected text
		(or the text before the insert point if no selection)
		sel is the selected text (or "" if no selection)
		after is all lines after the selected text
		(or the text after the insert point if no selection)"""
		
		# At present, called only by getBodyLines.
	
		t = self.bodyCtrl
		sel_index = t.tag_ranges("sel") 
		if len(sel_index) != 2:
			return "","",""
			
		i,j = sel_index
		i = t.index(i + "linestart")
		j = t.index(j + "lineend") # 10/24/03: -1c  # 11/4/03: no -1c.
		before = toUnicode(t.get("1.0",i),app.tkEncoding)
		sel    = toUnicode(t.get(i,j),    app.tkEncoding)
		after  = toUnicode(t.get(j,"end-1c"),app.tkEncoding)
	
		return before,sel,after
	#@nonl
	#@-node:getSelectionLines
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
		
		self.logControl.bind("<Button-1>", self.onActivateLog)
	#@nonl
	#@-node:tkLog.__init__
	#@+node:tkLog.configureBorder & configureFont
	def configureBorder(self,border):
		
		self.logControl.configure(bd=border)
		
	def configureFont(self,font):
	
		self.logControl.configure(font=font)
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
	
		font = self.logControl.cget("font")
		# trace(font)
		return font
	#@nonl
	#@-node:tkLog.getFontConfig
	#@+node:tkLog.hasFocus
	def hasFocus (self):
		
		return app.gui.get_focus(self.frame) == self.logControl
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
		# print `app.quitting`,`self.logControl`
		if app.quitting: return
		if self.logControl:
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,app.tkEncoding)
			if color:
				if color not in self.colorTags:
					self.colorTags.append(color)
					self.logControl.tag_config(color,foreground=color)
				self.logControl.insert("end",s)
				self.logControl.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
				if "black" not in self.colorTags:
					self.colorTags.append("black")
					self.logControl.tag_config("black",foreground="black")
				self.logControl.tag_add("black","end")
			else:
				self.logControl.insert("end",s)
			self.logControl.see("end")
			self.logControl.update_idletasks()
		else:
			app.logWaiting.append((s,color),) # 2/25/03
			print "Null tkinter log"
			if type(s) == type(u""): # 3/18/03
				s = toEncodedString(s,"ascii")
			print s
	
	def putnl (self):
		if app.quitting: return
		if self.logControl:
			self.logControl.insert("end",'\n')
			self.logControl.see("end")
			self.logControl.update_idletasks()
		else:
			app.logWaiting.append(('\n',"black"),) # 6/28/03
			print "Null tkinter log"
			print
	#@nonl
	#@-node:tkLog.put & putnl
	#@+node:tkLog.setFontFromConfig
	def setFontFromConfig (self):
	
		logCtrl = self.logControl ; config = app.config
	
		font = config.getFontFromParams(
			"log_text_font_family", "log_text_font_size",
			"log_text_font_slant",  "log_text_font_weight")
		
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

#@-node:@file leoTkinterFrame.py
#@-leo
