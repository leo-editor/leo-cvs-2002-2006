#@+leo

#@+node:0::@file leoFrame.py
#@+body
# To do: Use config params for window height, width and bar color, relief and width.


#@@language python

from leoGlobals import *
from leoUtils import *
import leoColor, leoCompare, leoDialog, leoFontPanel, leoNodes, leoPrefs
import os,sys,traceback,Tkinter,tkFileDialog,tkFont

# Needed for menu commands
import leoCommands, leoNodes, leoTree
import os, sys, traceback

class LeoFrame:

	#@+others
	#@+node:1:C=1:frame.__init__
	#@+body
	def __init__(self, title = None):
	
		Tk = Tkinter ; config = app().config
		
		#@<< set the LeoFrame ivars >>
		#@+node:1:C=2:<< set the LeoFrame ivars >>
		#@+body
		# Set title and fileName
		if title:
			self.mFileName = title
		else:
			title = "untitled"
			n = app().numberOfWindows
			if n > 0: title += `n`
			app().numberOfWindows = n+1
			self.mFileName = ""
		
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
		
		config = app().config
		s = config.getWindowPref("initial_splitter_orientation")
		self.splitVerticalFlag = s == None or (s != "h" and s != "horizontal")
		if self.splitVerticalFlag:
			r = config.getFloatWindowPref("initial_vertical_ratio")
			if r == None or r < 0.0 or r > 1.0: r = 0.5
		else:
			r = config.getFloatWindowPref("initial_horizontal_ratio")
			if r == None or r < 0.0 or r > 1.0: r = 0.3
		# print `r`
		self.ratio = r
		
		# Created below
		self.commands = None
		
		self.tree = None
		
		self.f1 = self.f2 = None
		self.log = None  ; self.logBar = None
		self.body = None ; self.bodyBar = None
		self.canvas = None ; self.treeBar = None
		self.splitter1 = self.splitter2 = None
		
		# Menu bars
		self.topMenu = self.fileMenu = self.editMenu = None
		self.outlineMenu = self.windowMenu = self.helpMenu = None
		# Submenus
		self.editBodyMenu = self.moveSelectMenu = self.markGotoMenu = None
		
		# Used by event handlers...
		self.redrawCount = 0
		self.activeFrame = None
		self.draggedItem = None
		self.recentFiles = [] # List of recent files
		#@-body
		#@-node:1:C=2:<< set the LeoFrame ivars >>

		self.top = top = Tk.Toplevel()
		top.withdraw() # 7/15/02
		
		if sys.platform=="win32":
			self.hwnd = top.frame()
			# trace("__init__", "frame.__init__: self.hwnd:" + `self.hwnd`)
		top.title(title)
		
		top.minsize(30,10) # In grid units. This doesn't work as I expect.
		
		c = None # Make sure we don't mess with c yet.
		self.createBothLeoSplitters(top)
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

		self.createMenuBar(top)
		self.createAccelerators(top)
		app().log = self # the LeoFrame containing the log
		app().windowList.append(self)
		es("Leo Log Window...") ; enl()
	
		self.top.protocol("WM_DELETE_WINDOW", self.OnCloseLeoEvent)
		self.top.bind("<Button-1>", self.OnActivateLeoEvent)
		self.tree.canvas.bind("<Button-1>", self.OnActivateTree)
		self.body.bind("<Button-1>", self.OnActivateBody)
		self.body.bind("<Double-Button-1>", self.OnBodyDoubleClick)
		self.log.bind("<Button-1>", self.OnActivateLog)
		self.body.bind("<Key>", self.tree.OnBodyKey)
		self.body.bind(virtual_event_name("Cut"), self.OnCut)
		self.body.bind(virtual_event_name("Copy"), self.OnCopy)
		self.body.bind(virtual_event_name("Paste"), self.OnPaste)
		
		# Handle mouse wheel in the outline pane.
		if 0: # This crashes tcl83.dll
			self.tree.canvas.bind("<MouseWheel>", self.OnRoll)
	#@-body
	#@-node:1:C=1:frame.__init__
	#@+node:2:C=3:frame.__del__
	#@+body
	# Warning:  calling del self will not necessarily call this routine.
	
	def __del__ (self):
		
		# Can't trace while destroying.
		# print "frame.__del__"
		
		self.log = self.body = self.tree = None
		self.treeBar = self.canvas = self.splitter1 = self.splitter2 = None
		# Menu bars.
		self.topMenu = self.fileMenu = self.editMenu = None
		self.outlineMenu = self.windowMenu = self.helpMenu = None
		# Submenus.
		self.editBodyMenu = self.moveSelectMenu = self.markGotoMenu = None
	#@-body
	#@-node:2:C=3:frame.__del__
	#@+node:3::frame.__repr__
	#@+body
	def __repr__ (self):
	
		return "leoFrame: " + self.title

	#@-body
	#@-node:3::frame.__repr__
	#@+node:4:C=4:frame.destroy
	#@+body
	def destroy (self):
	
		# don't trace during shutdown logic.
		# print "frame.destroy:", `self`
		self.tree.destroy()
		self.tree = None
		self.commands.destroy()
		self.commands = None
		self.top.destroy() # Actually close the window.
		self.top = None
	#@-body
	#@-node:4:C=4:frame.destroy
	#@+node:5:C=5:frame.setTabWidth
	#@+body
	def setTabWidth (self, w):
		
		try: # 8/11/02: This can fail when called from scripts.
			# 2/28/02: made code size platform dependent.
			if sys.platform=="win32": # Windows
				font = tkFont.Font(family="Courier",size=9)
			else:
				font = tkFont.Font(family="Courier",size=12)
				
			tabw = font.measure(" " * abs(w)) # 7/2/02
			# print "frame.setTabWidth:" + `w` + "," + `tabw`
			self.body.configure(tabs=tabw)
		except: pass
	#@-body
	#@-node:5:C=5:frame.setTabWidth
	#@+node:6:C=6:createMenuBar
	#@+body
	def createMenuBar(self, top):
	
		c = self.commands
		Tk = Tkinter
		self.topMenu = menu = Tk.Menu(top,postcommand=self.OnMenuClick)
		# To do: use Meta rathter than Control for accelerators for Unix
		
		#@<< create the file menu >>
		#@+node:1::<< create the file menu >>
		#@+body
		self.fileMenu = fileMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="File",menu=fileMenu)
		
		#@<< create the top-level file entries >>
		#@+node:1::<< create the top-level file entries >>
		#@+body
		fileMenu.add_command(label="New",accelerator="Ctrl+N", command=self.OnNew)
		fileMenu.add_command(label="Open...",accelerator="Ctrl+O", command=self.OnOpen)
		fileMenu.add_separator()
		
		fileMenu.add_command(label="Close",accelerator="Ctrl+W", command=self.OnClose)
		fileMenu.add_command(label="Save",accelerator="Ctrl+S", command=self.OnSave)
		fileMenu.add_command(label="Save As",accelerator="Shift+Ctrl+S", command=self.OnSaveAs)
		fileMenu.add_command(label="Save To",command=self.OnSaveTo)
		fileMenu.add_command(label="Revert To Saved",command=self.OnRevert)
		

		#@+at
		#  It is doubtful that leo.py will ever support a Print command directly.  Rather, users can use export commands to create 
		# text files that may then be formatted and printed as desired.

		#@-at
		#@@c
		if 0:
			fileMenu.add_command(label="Page Setup", accelerator="Shift+Ctrl+P",command=self.OnPageSetup)
			fileMenu.add_command(label="Print", accelerator="Ctrl+P", command=self.OnPrint)
			fileMenu.add_separator()
		#@-body
		#@-node:1::<< create the top-level file entries >>

		
		#@<< create the recent files submenu >>
		#@+node:2:C=7:<< create the recent files submenu >>
		#@+body
		recentFilesMenu = self.recentFilesMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Recent Files...", menu=recentFilesMenu)
		
		self.recentFiles = app().config.getRecentFiles()
		
		for i in xrange(len(self.recentFiles)):
			name = self.recentFiles[i]
			callback = lambda n=i: self.OnOpenRecentFile(n)
			recentFilesMenu.add_command(label=name,command=callback)

		#@-body
		#@-node:2:C=7:<< create the recent files submenu >>

		fileMenu.add_separator()
		
		#@<< create the read/write submenu >>
		#@+node:3::<< create the read/write submenu >>
		#@+body
		readWriteMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Read/Write...", menu=readWriteMenu)
		
		readWriteMenu.add_command(label="Read Outline Only",
			accelerator="Shift+Control+R",command=self.OnReadOutlineOnly)
		readWriteMenu.add_command(label="Read @file Nodes",command=self.OnReadAtFileNodes)
		readWriteMenu.add_command(label="Write Outline Only",command=self.OnWriteOutlineOnly)
		readWriteMenu.add_command(label="Write @file Nodes",
			accelerator="Shift+Control+W",command=self.OnWriteAtFileNodes)
		#@-body
		#@-node:3::<< create the read/write submenu >>

		
		#@<< create the tangle submenu >>
		#@+node:4::<< create the tangle submenu >>
		#@+body
		tangleMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Tangle...", menu=tangleMenu)
		
		tangleMenu.add_command(label="Tangle All",
			accelerator="Shift+Ctrl+A",
			command=self.OnTangleAll)
		tangleMenu.add_command(label="Tangle Marked",
			accelerator="Shift+Ctrl+M",
			command=self.OnTangleMarked)
		tangleMenu.add_command(label="Tangle",
			accelerator="Shift+Ctrl+T",
			command=self.OnTangle)
		#@-body
		#@-node:4::<< create the tangle submenu >>

		
		#@<< create the untangle submenu >>
		#@+node:5::<< create the untangle submenu >>
		#@+body
		untangleMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Untangle...", menu=untangleMenu)
		
		untangleMenu.add_command(label="Untangle All",
			command=self.OnUntangleAll)
		untangleMenu.add_command(label="Untangle Marked",
			command=self.OnUntangleMarked)
		untangleMenu.add_command(label="Untangle",
			accelerator="Shift+Ctrl+U",command=self.OnUntangle)
		#@-body
		#@-node:5::<< create the untangle submenu >>

		
		#@<< create the import submenu >>
		#@+node:6::<< create the import submenu >>
		#@+body
		importMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Import/Export...", menu=importMenu)
		
		importMenu.add_command(label="Import To @file",accelerator="Shift+Ctrl+F",
			command=self.OnImportAtFile)
		importMenu.add_command(label="Import To @root",
			command=self.OnImportAtRoot)
		importMenu.add_command(label="Import CWEB Files",
			command=self.OnImportCWEBFiles)
		importMenu.add_command(label="Import noweb Files",
			command=self.OnImportNowebFiles)
		importMenu.add_command(label="Import Flattened Outline",
			command=self.OnImportFlattenedOutline)
		importMenu.add_separator()
		
		importMenu.add_command(label="Outline To CWEB",
			command=self.OnOutlineToCWEB)
		importMenu.add_command(label="Outline To Noweb",
			command=self.OnOutlineToNoweb)
		importMenu.add_command(label="Flatten Outline",
			command=self.OnFlattenOutline)
		importMenu.add_command(label="Remove Sentinels",
			command=self.OnRemoveSentinels)
		#@-body
		#@-node:6::<< create the import submenu >>

		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=self.OnQuit)
		#@-body
		#@-node:1::<< create the file menu >>

		
		#@<< create the edit menu >>
		#@+node:2::<< create the edit menu >>
		#@+body
		self.editMenu = editMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Edit", menu=editMenu)
		
		editMenu.add_command(label="Can't Undo",
			accelerator="Ctrl+Z",command=self.OnUndo)
		editMenu.add_command(label="Can't Redo",
			accelerator="Shift+Ctrl+Z",command=self.OnRedo)
		editMenu.add_separator()
		
		editMenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.OnCutFromMenu)
		editMenu.add_command(label="Copy", accelerator="Ctrl+C", command=self.OnCopyFromMenu)
		editMenu.add_command(label="Paste", accelerator="Ctrl+V", command=self.OnPasteFromMenu) 
		
		editMenu.add_command(label="Delete",
			command=self.OnDelete)
		editMenu.add_command(label="Select All",
			command=self.OnSelectAll)
		editMenu.add_separator()
		
		editMenu.add_command(label="Edit Headline",
			accelerator="Ctrl+H",command=self.OnEditHeadline)
		
		#@<< create the edit body submenu >>
		#@+node:1::<< create the edit body submenu >>
		#@+body
		self.editBodyMenu = editBodyMenu = Tk.Menu(editMenu,tearoff=0)
		editMenu.add_cascade(label="Edit Body...", menu=editBodyMenu)
		
		editBodyMenu.add_command(label="Extract Section",
			accelerator="Shift+Ctrl+E",command=self.OnExtractSection)
		editBodyMenu.add_command(label="Extract Names",
			accelerator="Shift+Ctrl+N",command=self.OnExtractNames)
		editBodyMenu.add_command(label="Extract",
			accelerator="Shift+Ctrl+D",command=self.OnExtract)
		editBodyMenu.add_separator()
			
		editBodyMenu.add_command(label="Convert All Blanks",
			command=self.OnConvertAllBlanks)
		editBodyMenu.add_command(label="Convert All Tabs",
			command=self.OnConvertAllTabs)
		editBodyMenu.add_command(label="Convert Blanks",
			accelerator="Shift+Ctrl+B",command=self.OnConvertBlanks)
		editBodyMenu.add_command(label="Convert Tabs",
			accelerator="Shift+Ctrl+J",command=self.OnConvertTabs)
		editBodyMenu.add_separator()
		
		editBodyMenu.add_command(label="Indent",
			accelerator="Ctrl+]",command=self.OnIndent)
		editBodyMenu.add_command(label="Unindent",
			accelerator="Ctrl+[",command=self.OnDedent)
			
		if 0: # Not ready yet.
			editBodyMenu.add_separator()
			editBodyMenu.add_command(label="Insert Graphic File...",
				command=self.OnInsertGraphicFile)
		#@-body
		#@-node:1::<< create the edit body submenu >>

		
		#@<< create the find submenu >>
		#@+node:2::<< create the find submenu >>
		#@+body
		findMenu = Tk.Menu(editMenu,tearoff=0)
		editMenu.add_cascade(label="Find...", menu=findMenu)
		
		findMenu.add_command(label="Find Panel",accelerator="Ctrl+F",
			command=self.OnFindPanel)
		findMenu.add_separator()
		
		findMenu.add_command(label="Find Next",accelerator="F3",
			command=self.OnFindNext)
		findMenu.add_command(label="Find Next",accelerator="Ctrl+G",
			command=self.OnFindNext)
		findMenu.add_command(label="Find Previous",accelerator="Shift+Ctrl+G",
			command=self.OnFindPrevious)
		findMenu.add_command(label="Replace",accelerator="Ctrl+=",
			command=self.OnReplace)
		findMenu.add_command(label="Replace, Then Find",accelerator="Ctrl+-",
			command=self.OnReplaceThenFind)
		#@-body
		#@-node:2::<< create the find submenu >>

		editMenu.add_command(label="Set Font...",
			accelerator="Shift+Alt+T",command=self.OnFontPanel)
		editMenu.add_command(label="Set Colors...",
			accelerator="Shift+Alt+S",command=self.OnColorPanel)
		
		label = choose(c.tree.colorizer.showInvisibles,"Hide Invisibles","Show Invisibles")
		editMenu.add_command(label=label,command=self.OnViewAllCharacters,
			accelerator="Alt+V")
		editMenu.add_separator()
		
		editMenu.add_command(label="Preferences",accelerator="Ctrl+Y",command=self.OnPreferences)
		#@-body
		#@-node:2::<< create the edit menu >>

		
		#@<< create the outline menu >>
		#@+node:3::<< create the outline menu >>
		#@+body
		self.outlineMenu = outlineMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Outline", menu=outlineMenu)
		
		outlineMenu.add_command(label="Cut Node",
			accelerator="Shift+Ctrl+X",command=self.OnCutNode)
		outlineMenu.add_command(label="Copy Node",
			accelerator="Shift+Ctrl+C",command=self.OnCopyNode)
		outlineMenu.add_command(label="Paste Node",
			accelerator="Shift+Ctrl+V",command=self.OnPasteNode)
		outlineMenu.add_command(label="Delete Node",
			accelerator="Shift+Ctrl+BkSp",command=self.OnDeleteNode)
		outlineMenu.add_separator()
		
		outlineMenu.add_command(label="Insert Node",
			accelerator="Ctrl+I",command=self.OnInsertNode)
		outlineMenu.add_command(label="Clone Node",
			accelerator="Ctrl+`",command=self.OnCloneNode)
		outlineMenu.add_command(label="Sort Children",
			command=self.OnSortChildren)
		outlineMenu.add_command(label="Sort Siblings",
			accelerator="Alt-A",command=self.OnSortSiblings)
		outlineMenu.add_separator()
		
		
		#@<< create expand/contract submenu >>
		#@+node:1::<< create expand/contract submenu >>
		#@+body
		self.expandContractMenu = expandContractMenu = Tk.Menu(outlineMenu,tearoff=0)
		outlineMenu.add_cascade(label="Expand/Contract...", menu=expandContractMenu)
		
		expandContractMenu.add_command(label="Expand All",
			accelerator="Alt+9",command=self.OnExpandAll)
		expandContractMenu.add_command(label="Expand All Children",
			command=self.OnExpandAllChildren)
		expandContractMenu.add_command(label="Expand Children",
			command=self.OnExpandChildren)
		expandContractMenu.add_separator()
		
		expandContractMenu.add_command(label="Contract Parent",
			accelerator="Alt+0",command=self.OnContractParent)
		expandContractMenu.add_command(label="Contract All",
			accelerator="Alt+1",command=self.OnContractAll)
		expandContractMenu.add_command(label="Contract All Children",
			command=self.OnContractAllChildren)
		expandContractMenu.add_command(label="Contract Children",
			command=self.OnContractChildren)
		expandContractMenu.add_separator()
		
		expandContractMenu.add_command(label="Expand Next Level",
			accelerator="Alt+=",command=self.OnExpandNextLevel)
		expandContractMenu.add_command(label="Expand To Level 1",
			accelerator="Alt+1",command=self.OnExpandToLevel1)
		expandContractMenu.add_command(label="Expand To Level 2",
			accelerator="Alt+2",command=self.OnExpandToLevel2)
		expandContractMenu.add_command(label="Expand To Level 3",
			accelerator="Alt+3",command=self.OnExpandToLevel3)
		expandContractMenu.add_command(label="Expand To Level 4",
			accelerator="Alt+4",command=self.OnExpandToLevel4)
		expandContractMenu.add_command(label="Expand To Level 5",
			accelerator="Alt+5",command=self.OnExpandToLevel5)
		expandContractMenu.add_command(label="Expand To Level 6",
			accelerator="Alt+6",command=self.OnExpandToLevel6)
		expandContractMenu.add_command(label="Expand To Level 7",
			accelerator="Alt+7",command=self.OnExpandToLevel7)
		expandContractMenu.add_command(label="Expand To Level 8",
			accelerator="Alt+8",command=self.OnExpandToLevel8)
		#expandContractMenu.add_command(label="Expand To Level 9",
			#accelerator="Alt+9",command=self.OnExpandToLevel9)
		#@-body
		#@-node:1::<< create expand/contract submenu >>

		
		#@<< create move/select submenu >>
		#@+node:2::<< create move/select submenu >>
		#@+body
		self.moveSelectMenu = moveSelectMenu = Tk.Menu(outlineMenu,tearoff=0)
		outlineMenu.add_cascade(label="Move/Select...", menu=moveSelectMenu)
		
		moveSelectMenu.add_command(label="Move Down",
			accelerator="Ctrl+D",command=self.OnMoveDown)
		moveSelectMenu.add_command(label="Move Left",
			accelerator="Ctrl+L",command=self.OnMoveLeft)
		moveSelectMenu.add_command(label="Move Right",
			accelerator="Ctrl+R",command=self.OnMoveRight)
		moveSelectMenu.add_command(label="Move Up",
			accelerator="Ctrl+U", command=self.OnMoveUp)
		moveSelectMenu.add_separator()
		
		moveSelectMenu.add_command(label="Promote",
			accelerator="Shift+Ctrl+[", command=self.OnPromote)
		moveSelectMenu.add_command(label="Demote",
			accelerator="Shift+Ctrl+]", command=self.OnDemote)
		moveSelectMenu.add_separator()
		
		moveSelectMenu.add_command(label="Go Prev Visible",
			accelerator="Alt-Shift-U",command=self.OnGoPrevVisible)
		moveSelectMenu.add_command(label="Go Next Visible",
			accelerator="Alt-Shift-D",command=self.OnGoNextVisible)
		moveSelectMenu.add_separator()
		
		moveSelectMenu.add_command(label="Go Back",
			accelerator="Alt-Shift+V",command=self.OnGoBack)
		moveSelectMenu.add_command(label="Go Next",
			accelerator="Alt-Shift-W",command=self.OnGoNext)
		#@-body
		#@-node:2::<< create move/select submenu >>

		
		#@<< create mark/goto submenu >>
		#@+node:3::<< create mark/goto submenu >>
		#@+body
		self.markGotoMenu = markGotoMenu = Tk.Menu(outlineMenu,tearoff=0)
		outlineMenu.add_cascade(label="Mark/Go To...", menu=markGotoMenu)
		
		markGotoMenu.add_command(label="Mark",
			accelerator="Ctrl-M",command=self.OnMark)
		markGotoMenu.add_command(label="Mark Subheads",
			accelerator="Alt+S",command=self.OnMarkSubheads)
		markGotoMenu.add_command(label="Mark Changed Items",
			accelerator="Alt+C",command=self.OnMarkChangedItems)
		markGotoMenu.add_command(label="Mark Changed Roots",
			accelerator="Alt+R",command=self.OnMarkChangedRoots)
		markGotoMenu.add_separator()
		
		markGotoMenu.add_command(label="Unmark All",
			accelerator="Alt+U",command=self.OnUnmarkAll)
		markGotoMenu.add_command(label="Go To Next Marked",
			accelerator="Alt+M",command=self.OnGoToNextMarked)
		markGotoMenu.add_command(label="Go To Next Changed",
			accelerator="Alt+C",command=self.OnGoToNextChanged)
		#@-body
		#@-node:3::<< create mark/goto submenu >>
		#@-body
		#@-node:3::<< create the outline menu >>

		
		#@<< create the window menu >>
		#@+node:4::<< create the window menu >>
		#@+body
		self.windowMenu = windowMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Window", menu=windowMenu)
		
		windowMenu.add_command(label="Equal Sized Panes",
			accelerator="Ctrl-E",command=self.OnEqualSizedPanes)
		windowMenu.add_command(label="Toggle Active Pane",
			accelerator="Ctrl-T",command=self.OnToggleActivePane)
		windowMenu.add_command(label="Toggle Split Direction",
			command=self.OnToggleSplitDirection)
		windowMenu.add_separator()
		
		windowMenu.add_command(label="Cascade",
			command=self.OnCascade)
		windowMenu.add_command(label="Minimize All",
			command=self.OnMinimizeAll)
		windowMenu.add_separator()
		
		windowMenu.add_command(label="Open Compare Window",
			command=self.OnOpenCompareWindow)
		windowMenu.add_command(label="Open Python Window",
			accelerator="Alt+P",command=self.OnOpenPythonWindow)
		#@-body
		#@-node:4::<< create the window menu >>

		
		#@<< create the help menu >>
		#@+node:5::<< create the help menu >>
		#@+body
		self.helpMenu = helpMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Help", menu=helpMenu)
		
		helpMenu.add_command(label="About Leo...", command=self.OnAbout)
		helpMenu.add_command(label="Online Home Page...", command=self.OnLeoHome)
		helpMenu.add_separator()
		helpMenu.add_command(label="Online Tutorial (Start Here)...", command=self.OnLeoTutorial)
		if sys.platform=="win32": # Windows
			helpMenu.add_command(label="Tutorial (sbooks.chm)...", command=self.OnLeoHelp)
		helpMenu.add_command(label="Reference (LeoDocs.leo)...", command=self.OnLeoDocumentation)

		#@-body
		#@-node:5::<< create the help menu >>

		top.config(menu=menu) # Display the menu.
	#@-body
	#@-node:6:C=6:createMenuBar
	#@+node:7:C=8:createAccelerators
	#@+body
	#@+at
	#  The accelerator entry specified when creating a menu item just creates text.  The actual correspondance between keys and 
	# routines is defined here.

	#@-at
	#@@c
	
	def createAccelerators (self,top):
	
		body = self.body ; canvas = self.canvas
	
		fkeyBindings = [
			("F3", self.OnFindNext)
		]
		for accel, command in fkeyBindings:
			top.bind("<" + accel + ">", command)
	
		controlBindings = [
			
			#@<< control key bindings >>
			#@+node:1::<< control key bindings >>
			#@+body
			# The names at http://tcl.activestate.com/man/tcl8.4/TkCmd/keysyms.htm must be used here.
			("equal", self.OnReplace), # "="
			("quoteleft", self.OnCloneNode), # "`"
			("minus", self.OnReplaceThenFind),
			
			("braceleft", self.OnPromote), # "{"
			("braceright", self.OnDemote), # "}"
			("bracketleft", self.OnDedent), # "["
			("bracketright", self.OnIndent), # "]"
			("Shift-BackSpace", self.OnDeleteNode),
			
			("a", self.OnSelectAll),
			# "b" unused
			# ("c", self.OnCopy), # Done in frame.__init__
			("d", self.OnMoveDown),
			("e", self.OnEqualSizedPanes),
			("f", self.OnFindPanel),
			("g", self.OnFindNext),
			("h", self.OnEditHeadline),
			("i", self.OnInsertNode), # Control-I == '\t'
			# Control-J == '\n'
			# Control-k no longer used
			("l", self.OnMoveLeft),
			("m", self.OnMark),
			("n", self.OnNew),
			("o", self.OnOpen),
			# "p" unused.
			("q", self.OnQuit),
			("r", self.OnMoveRight),
			("s", self.OnSave),
			("t", self.OnToggleActivePane),
			("u", self.OnMoveUp),
			# ("v", self.OnCopy), # Done in frame.__init__
			("w", self.OnClose),
			# ("x", self.OnCut), # Done in frame.__init__
			("y", self.OnPreferences),
			("z", self.OnUndo),
			# Shift-Control...
			("A", self.OnTangleAll),
			("B", self.OnConvertBlanks),
			("C", self.OnCopyNode),
			("D", self.OnExtract),
			("E", self.OnExtractSection),
			("F", self.OnImportAtFile),
			("G", self.OnFindPrevious),
			# H unused
			# I reserved
			("J", self.OnConvertTabs),
			# K unused
			# L unused
			("M", self.OnTangleMarked),
			("N", self.OnExtractNames),
			# O unused
			# P unused
			# Q unused
			("R", self.OnReadAtFileNodes), # EKR: 9/3/02
			("S", self.OnSaveAs),
			("T", self.OnTangle),
			("U", self.OnUntangle),
			("V", self.OnPasteNode),
			("W", self.OnWriteAtFileNodes), # EKR: 9/3/02
			("X", self.OnCutNode),
			("Z", self.OnRedo)
			#@-body
			#@-node:1::<< control key bindings >>

		]
		# Warnings: two sets of actions will be taken for these
		# unless all event handlers returns "break".
		for accel, command in controlBindings:
			body.bind("<Control-" + accel + ">", command) # Necessary to override defaults in body.
			top.bind ("<Control-" + accel + ">", command)
	
		altBindings = [
			
			#@<< alt key bindings >>
			#@+node:2::<< alt key bindings >>
			#@+body
			("equal", self.OnExpandNextLevel),
			("Key-0", self.OnContractParent),
			("Key-1", self.OnExpandToLevel1), # Note 1-5 all by itself refers to button 1-5, not key 1-5.
			("Key-2", self.OnExpandToLevel2),
			("Key-3", self.OnExpandToLevel3),
			("Key-4", self.OnExpandToLevel4),
			("Key-5", self.OnExpandToLevel5),
			("Key-6", self.OnExpandToLevel6),
			("Key-7", self.OnExpandToLevel7),
			("Key-8", self.OnExpandToLevel8),
			("Key-9", self.OnExpandAll),
			("a", self.OnSortSiblings),
			# "b" unused
			("c", self.OnMarkChangedItems),
			("d", self.OnGoToNextChanged),
			# "e" opens Edit menu
			# "f" opens File menu
			# "g" unused
			# "h" opens Help menu
			# "i" unused (reserved?)
			# "j" unused (reserved?)
			# "k" unused
			# "l" unused
			("m", self.OnGoToNextMarked),
			# "n" unused
			# "o" opens Outline menu
			("p", self.OnOpenPythonWindow),
			# "q" unused
			("r", self.OnMarkChangedRoots),
			("s", self.OnMarkSubheads),
			# "t" unused
			("u", self.OnUnmarkAll),
			("v", self.OnViewAllCharacters),
			# "w" opens Window menu
			# "x" unused
			# "y" unused
			# "z" unused
			
			# Shift-Alt...
			
			# ("E", self.OnExecuteScript),
			("S", self.OnColorPanel),
			("T", self.OnFontPanel),
			

			#@+at
			#  7/29/02: It's too confusing to have arrow keys mean different things in different panes.
			# 
			# For one thing, we want to leave the focus in the body pane after the first click in the outline pane, but that means 
			# that the arrow keys must still be functional in the _body_ pane!
			# 
			# Alas, all the various combinations of key bindings of arrow keys appear to do something; there are none left to use 
			# for moving around in the outline pane.  So we are stuck with poor shortcuts.

			#@-at
			#@@c
			
			# We would love to use arrow keys, and we can't.
			("D", self.OnGoNextVisible),
			("U", self.OnGoPrevVisible),
			("V", self.OnGoBack),
			("W", self.OnGoNext),
			#@-body
			#@-node:2::<< alt key bindings >>

		]
		# Warnings: two sets of actions will be taken for these
		# unless all event handlers returns "break".
		for accel, command in altBindings:
			body.bind("<Alt-" + accel + ">", command) # Necessary to override defaults in body.
			top.bind ("<Alt-" + accel + ">", command)
			
		if 0: # A useful trace
			print_bindings("top",self.top)
			print_bindings("body",self.body)
			print_bindings("canvas",self.canvas)
	#@-body
	#@-node:7:C=8:createAccelerators
	#@+node:8::getFocus
	#@+body
	# Returns the frame that has focus, or body if None.
	
	def getFocus(self):
	
		f = self.top.focus_displayof()
		if f:
			return f
		else:
			return self.body
	#@-body
	#@-node:8::getFocus
	#@+node:9::notYet
	#@+body
	def notYet(self,name):
	
		es(name + " not ready yet")

	#@-body
	#@-node:9::notYet
	#@+node:10:C=9:frame.put, putnl
	#@+body
	# All output to the log stream eventually comes here.
	
	def put (self,s):
		if app().quitting > 0: return
		if self.log:
				self.log.insert("end",s)
				self.log.see("end")
				self.log.update_idletasks()
		else:
			print "Null log"
			print s
	
	def putnl (self):
		if app().quitting > 0: return
		if self.log:
			self.log.insert("end",'\n')
			self.log.see("end")
			self.log.update_idletasks()
		else:
			print "Null log"
			print
	#@-body
	#@-node:10:C=9:frame.put, putnl
	#@+node:11:C=10:resizePanesToRatio
	#@+body
	def resizePanesToRatio(self,ratio):
	
		self.divideLeoSplitter(self.splitVerticalFlag, ratio)
		# trace(`ratio`)

	#@-body
	#@-node:11:C=10:resizePanesToRatio
	#@+node:12:C=11:Event handlers
	#@+node:1:C=12:frame.OnCloseLeoEvent
	#@+body
	# Called from quit logic and when user closes the window.
	# Returns true if the close happened.
	
	def OnCloseLeoEvent(self):
	
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
		return true
	#@-body
	#@-node:1:C=12:frame.OnCloseLeoEvent
	#@+node:2:C=13:OnActivateLeoEvent
	#@+body
	def OnActivateLeoEvent(self,event=None):
	
		c = self.commands
		app().log = self

	#@-body
	#@-node:2:C=13:OnActivateLeoEvent
	#@+node:3:C=14:OnActivateBody & OnBodyDoubleClick
	#@+body
	def OnActivateBody (self,event=None):
	
		app().log = self
		self.tree.OnDeactivate()
	
	def OnBodyDoubleClick (self,event=None):
	
		if event: # 8/4/02: prevent wandering insertion point.
			index = "@%d,%d" % (event.x, event.y) # Find where we clicked
		body = self.body
		start = body.index(index + " wordstart")
		end = body.index(index + " wordend")
		setTextSelection(self.body,start,end)
		return "break" # Inhibit all further event processing.
	#@-body
	#@-node:3:C=14:OnActivateBody & OnBodyDoubleClick
	#@+node:4::OnActivateLog
	#@+body
	def OnActivateLog (self,event=None):
	
		app().log = self
		self.tree.OnDeactivate()
	#@-body
	#@-node:4::OnActivateLog
	#@+node:5::OnActivateTree
	#@+body
	def OnActivateTree (self,event=None):
	
		app().log = self
		self.tree.undimEditLabel()
		self.tree.canvas.focus_set()
	#@-body
	#@-node:5::OnActivateTree
	#@+node:6::OnRoll
	#@+body
	def OnRoll (self,event):
		
		print "OnRoll"
	#@-body
	#@-node:6::OnRoll
	#@-node:12:C=11:Event handlers
	#@+node:13:C=15:Menu enablers (Frame)
	#@+node:1::OnMenuClick (enables and disables all menu items)
	#@+body
	# This is the Tk "postcommand" callback.  It should update all menu items.
	
	def OnMenuClick (self):
	
		self.updateFileMenu()
		self.updateEditMenu()
		self.updateOutlineMenu()
	#@-body
	#@-node:1::OnMenuClick (enables and disables all menu items)
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
	
		c = self.commands ; menu = self.fileMenu
		if not c: return
		enableMenu(menu,"Revert To Saved", c.canRevert())
	#@-body
	#@-node:3::updateFileMenu
	#@+node:4::updateEditMenu
	#@+body
	def updateEditMenu (self):
	
		c = self.commands
		if not c: return
		menu = self.editMenu
		# Top level entries.
		c.undoer.enableMenuItems()
		if 0: # Always on for now.
			enableMenu(menu,"Cut",c.canCut())
			enableMenu(menu,"Copy",c.canCut()) # delete
			enableMenu(menu,"Paste",c.canPaste())
		if 0: # Always on for now.
			menu = self.findMenu
			enableMenu(menu,"Find Next",c.canFind())
			flag = c.canReplace()
			enableMenu(menu,"Replace",flag)
			enableMenu(menu,"Replace, Then Find",flag)
		# Edit Body submenu
		menu = self.editBodyMenu
		enableMenu(menu,"Extract Section",c.canExtractSection())
		enableMenu(menu,"Extract Names",c.canExtractSectionNames())
		enableMenu(menu,"Extract",c.canExtract())
	#@-body
	#@-node:4::updateEditMenu
	#@+node:5::updateOutlineMenu
	#@+body
	def updateOutlineMenu (self):
	
		c = self.commands ; v = c.currentVnode()
		if not c: return
	
		menu = self.outlineMenu
		enableMenu(menu,"Cut Node",c.canCutOutline())
		enableMenu(menu,"Delete Node",c.canDeleteHeadline())
		enableMenu(menu,"Paste Node",c.canPasteOutline())
		enableMenu(menu,"Sort Siblings",c.canSortSiblings())
		# Expand/Contract submenu
		menu = self.expandContractMenu
		enableMenu(menu,"Contract Parent",c.canContractParent())
		# Move/Select submenu
		menu = self.moveSelectMenu
		enableMenu(menu,"Move Down",c.canMoveOutlineDown())
		enableMenu(menu,"Move Left",c.canMoveOutlineLeft())
		enableMenu(menu,"Move Right",c.canMoveOutlineRight())
		enableMenu(menu,"Move Up",c.canMoveOutlineUp())
		enableMenu(menu,"Promote",c.canPromote())
		enableMenu(menu,"Demote",c.canDemote())
		enableMenu(menu,"Go Prev Visible",c.canSelectVisBack())
		enableMenu(menu,"Go Next Visible",c.canSelectVisNext())
		enableMenu(menu,"Go Back",c.canSelectThreadBack())
		enableMenu(menu,"Go Next",c.canSelectThreadNext())
		# Mark/Go To submenu
		menu = self.markGotoMenu
		label = choose(v and v.isMarked(),"Unmark","Mark")
		setMenuLabel(menu,0,label)
		enableMenu(menu,"Mark Subheads",(v and v.hasChildren()))
		enableMenu(menu,"Mark Changed Items",c.canMarkChangedHeadlines())
		enableMenu(menu,"Mark Changed Roots",c.canMarkChangedRoots())
		enableMenu(menu,"Go To Next Marked",c.canGoToNextMarkedHeadline())
		enableMenu(menu,"Go To Next Changed",c.canGoToNextDirtyHeadline())
	#@-body
	#@-node:5::updateOutlineMenu
	#@-node:13:C=15:Menu enablers (Frame)
	#@+node:14:C=16:Menu Command Handlers
	#@+node:1::File Menu
	#@+node:1::top level
	#@+node:1:C=17:OnNew
	#@+body
	def OnNew (self,event=None):
	
		config = app().config
		frame = LeoFrame() # Create another Leo window.
		top = frame.top
		
		# Set the size of the new window.
		h = config.getIntWindowPref("initial_window_height")
		w = config.getIntWindowPref("initial_window_width")
		x = config.getIntWindowPref("initial_window_left")
		y = config.getIntWindowPref("initial_window_top")
		# print h,w,x,y
		if h == None or h < 5: h = 5
		if w == None or w < 5: w = 10
		y = max(y,0) ; x = max(x,0)
		g = "%dx%d%+d%+d" % (w,h,x,y)
		top.geometry(g)
		top.deiconify()
		top.lift()
		frame.resizePanesToRatio(self.ratio) # Resize the _new_ frame.
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:1:C=17:OnNew
	#@+node:2:C=18:frame.OnOpen
	#@+body
	def OnOpen(self,event=None):
	
		c = self.commands
		
		#@<< Set closeFlag if the only open window is empty >>
		#@+node:1::<< Set closeFlag if the only open window is empty >>
		#@+body
		#@+at
		#  If this is the only open window was opened when the app started, and the window has never been written to or saved, 
		# then we will automatically close that window if this open command completes successfully.

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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2:C=18:frame.OnOpen
	#@+node:3:C=19:frame.OpenWithFileName
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
				es("This window already open")
				return true, frame
				
		fileName = oldFileName # Use the idiosyncratic file name.
	
		try:
			file = open(fileName,'r')
			if file:
				frame = LeoFrame(fileName)
				frame.commands.fileCommands.open(file,fileName) # closes file.
				frame.openDirectory=os.path.dirname(fileName)
				
				#@<< make fileName the most recent file of frame >>
				#@+node:1:C=20:<< make fileName the most recent file of frame >>
				#@+body
				# Update the recent files list in all windows.
				normFileName = os.path.normcase(fileName)
				
				for frame in app().windowList:
				
					# Make sure we remove all versions of the file name.
					for name in frame.recentFiles:
						name2 = os.path.normcase(name)
						name2 = os.path.normpath(name2)
						if normFileName == name2:
							frame.recentFiles.remove(name)
					frame.recentFiles.insert(0,fileName)
					
					# Delete all elements of frame.recentFilesMenu.
					frame.recentFilesMenu.delete(0,len(frame.recentFiles))
					
					# Recreate frame.recentFilesMenu.
					i = 0
					for name in frame.recentFiles:
						callback = lambda n=i: self.OnOpenRecentFile(n)
						frame.recentFilesMenu.add_command(label=name,command=callback)
						i += 1
					
				# Update the config file.
				app().config.setRecentFiles(frame.recentFiles)
				app().config.update()
				#@-body
				#@-node:1:C=20:<< make fileName the most recent file of frame >>

				return true, frame
			else:
				es("can not open" + fileName)
				return false, None
		except:
			es("exceptions opening" + fileName)
			traceback.print_exc()
			return false, None
	#@-body
	#@-node:3:C=19:frame.OpenWithFileName
	#@+node:4::OnClose
	#@+body
	# Called when File-Close command is chosen.
	
	def OnClose(self,event=None):
		
		self.OnCloseLeoEvent() # Destroy the frame unless the user cancels.
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnClose
	#@+node:5:C=21:OnSave
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
			return "break" # inhibit further command processing
	
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Save",
			filetypes=[("Leo files", "*.leo")],
			defaultextension=".leo")
	
		if len(fileName) > 0:
			# 7/2/02: don't change mFileName until the dialog has suceeded.
			self.mFileName = ensure_extension(fileName, ".leo")
			self.title = self.mFileName
			self.top.title(self.mFileName)
			c.fileCommands.save(self.mFileName)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:5:C=21:OnSave
	#@+node:6:C=22:OnSaveAs
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
			self.top.title(self.mFileName)
			self.commands.fileCommands.saveAs(self.mFileName)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:6:C=22:OnSaveAs
	#@+node:7:C=23:OnSaveTo
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:7:C=23:OnSaveTo
	#@+node:8:C=24:OnRevert
	#@+body
	def OnRevert(self,event=None):
	
		# Make sure the user wants to Revert.
		if not self.mFileName:
			self.mFileName = ""
		if len(self.mFileName)==0:
			return "break" # inhibit further command processing
		
		d = leoDialog.leoDialog()
		reply = d.askYesNo("Revert",
			"Revert to previous version of " + self.mFileName + "?")
	
		if reply=="no":
			return "break" # inhibit further command processing
	
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:8:C=24:OnRevert
	#@+node:9:C=25:frame.OnQuit
	#@+body
	def OnQuit(self,event=None):
	
		app().quitting += 1
		
		while app().windowList:
			w = app().windowList[0]
			if not w.OnCloseLeoEvent():
				break
				
		app().quitting -= 1 # If we get here the quit has been disabled.
		return "break" # inhibit further command processing
	#@-body
	#@-node:9:C=25:frame.OnQuit
	#@-node:1::top level
	#@+node:2:C=26:Recent Files submenu
	#@+node:1::OnOpenFileN
	#@+body
	def OnOpenRecentFile(self,n):
		
		if n < len(self.recentFiles):
			fileName = self.recentFiles[n]
			ok, frame = self.OpenWithFileName(fileName)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnOpenFileN
	#@-node:2:C=26:Recent Files submenu
	#@+node:3::Read/Write submenu
	#@+node:1:C=27:fileCommands.OnReadOutlineOnly
	#@+body
	def OnReadOutlineOnly (self,event=None):
	
		fileName = tkFileDialog.askopenfilename(
			title="Read Outline Only",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension=".leo")
	
		if not fileName or len(fileName) == 0:
			return "break" # inhibit further command processing
			
		file = open(fileName,'r')
		if file:
			frame = LeoFrame(fileName)
			frame.top.deiconify()
			frame.top.lift()
			app().root.update() # Force a screen redraw immediately.
			frame.commands.fileCommands.readOutlineOnly(file,fileName) # closes file.
		else:
			es("can not open:" + fileName)
		return "break" # inhibit further command processing
	#@-body
	#@-node:1:C=27:fileCommands.OnReadOutlineOnly
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnReadAtFileNodes
	#@+node:3::OnWriteOutlineOnly
	#@+body
	def OnWriteOutlineOnly (self,event=None):
	
		self.commands.fileCommands.writeOutlineOnly()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnWriteOutlineOnly
	#@+node:4::OnWriteAtFileNodes
	#@+body
	def OnWriteAtFileNodes (self,event=None):
	
		self.commands.fileCommands.writeAtFileNodes()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnWriteAtFileNodes
	#@-node:3::Read/Write submenu
	#@+node:4::Tangle submenu
	#@+node:1::OnTangleAll
	#@+body
	def OnTangleAll(self,event=None):
	
		self.commands.tangleCommands.tangleAll()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnTangleAll
	#@+node:2::OnTangleMarked
	#@+body
	def OnTangleMarked(self,event=None):
	
		self.commands.tangleCommands.tangleMarked()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnTangleMarked
	#@+node:3::OnTangle
	#@+body
	def OnTangle (self,event=None):
	
		self.commands.tangleCommands.tangle()
		return "break" # inhibit further command processing
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnUntangleAll
	#@+node:2::OnUntangleMarked
	#@+body
	def OnUntangleMarked(self,event=None):
	
		c = self.commands
		self.commands.tangleCommands.untangleMarked()
		c.undoer.clearUndoState()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnUntangleMarked
	#@+node:3::OnUntangle
	#@+body
	def OnUntangle(self,event=None):
	
		c = self.commands
		self.commands.tangleCommands.untangle()
		c.undoer.clearUndoState()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnUntangle
	#@-node:5::Untangle submenu
	#@+node:6::Import&Export submenu
	#@+node:1::OnFlattenOutline
	#@+body
	def OnFlattenOutline (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Flatten Outline",filetypes=filetypes,
			initialfile="flat.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.flattenOutline(fileName)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnFlattenOutline
	#@+node:2::OnImportAtRoot
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnImportAtRoot
	#@+node:3::OnImportAtFile
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnImportAtFile
	#@+node:4::OnImportCWEBFiles
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
		
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnImportCWEBFiles
	#@+node:5::OnImportFlattenedOutline
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
			
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnImportFlattenedOutline
	#@+node:6::OnImportNowebFiles
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
		
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnImportNowebFiles
	#@+node:7::OnOutlineToCWEB
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnOutlineToCWEB
	#@+node:8::OnOutlineToNoweb
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnOutlineToNoweb
	#@+node:9::OnRemoveSentinels
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:9::OnRemoveSentinels
	#@-node:6::Import&Export submenu
	#@-node:1::File Menu
	#@+node:2::Edit Menu (change to handle log pane too)
	#@+node:1::Edit top level
	#@+node:1::OnUndo
	#@+body
	def OnUndo(self,event=None):
	
		self.commands.undoer.undo()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnUndo
	#@+node:2::OnRedo
	#@+body
	def OnRedo(self,event=None):
	
		self.commands.undoer.redo()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnRedo
	#@+node:3:C=28:frame.OnCut, OnCutFrom Menu
	#@+body
	def OnCut (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.commands.tree.onBodyWillChange(v,"Cut")
		
		# Copy the selection to the internal clipboard.
		if 0: # no longer needed.
			app().clipboard = getSelectedText(self.body)
			# trace(`app().clipboard`)
		return # Allow the actual cut!
	
	def OnCutFromMenu (self,event=None):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Cut"))
	#@-body
	#@-node:3:C=28:frame.OnCut, OnCutFrom Menu
	#@+node:4:C=29:frame.OnCopy, OnCopyFromMenu
	#@+body
	def OnCopy (self,event=None):
	
		# Copy never changes dirty bits or syntax coloring.
		
		# Copy the selection to the internal clipboard.
		if 0: # no longer needed.
			app().clipboard = getSelectedText(self.body)
			# trace(`app().clipboard`)
		return # Allow the actual copy!
		
	def OnCopyFromMenu (self,event=None):
	
		trace()
		w = self.getFocus()
		w.event_generate(virtual_event_name("Copy"))
	#@-body
	#@-node:4:C=29:frame.OnCopy, OnCopyFromMenu
	#@+node:5:C=30:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+body
	def OnPaste (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.commands.tree.onBodyWillChange(v,"Paste")
		return # Allow the actual paste!
		
	def OnPasteNode (self,event=None):
	
		# trace(`event`)
		return "break" # inhibit further command processing ??
		
	def OnPasteFromMenu (self,event=None):
	
		# trace()
		w = self.getFocus()
		w.event_generate(virtual_event_name("Paste"))
	#@-body
	#@-node:5:C=30:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+node:6:C=31:OnDelete
	#@+body
	def OnDelete(self,event=None):
	
		c = self.commands ; v = c.currentVnode()
		first, last = getTextSelection(self.body)
		if first and last:
			self.body.delete(first,last)
			c.tree.onBodyChanged(v,"Delete")
		return "break" # inhibit further command processing
	#@-body
	#@-node:6:C=31:OnDelete
	#@+node:7:C=32:OnSelectAll
	#@+body
	def OnSelectAll(self,event=None):
	
		setTextSelection(self.body,"1.0","end")
		return "break" # inhibit further command processing
	#@-body
	#@-node:7:C=32:OnSelectAll
	#@+node:8::OnEditHeadline
	#@+body
	def OnEditHeadline(self,event=None):
	
		tree = self.commands.tree
		tree.editLabel(tree.currentVnode)
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnEditHeadline
	#@+node:9:C=33:OnFontPanel
	#@+body
	def OnFontPanel(self,event=None):
	
		if self.fontPanel:
			# trace()
			self.fontPanel.top.deiconify()
		else:
			self.fontPanel = fp =  leoFontPanel.leoFontPanel(self.commands)
			fp.run()
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:9:C=33:OnFontPanel
	#@+node:10:C=34:OnColorPanel
	#@+body
	def OnColorPanel(self,event=None):
		
		if self.colorPanel:
			# trace()
			self.colorPanel.top.deiconify()
		else:
			self.colorPanel = cp = leoColor.leoColorPanel(self.commands)
			cp.run()
	
		return "break" # inhibit further command processing

	#@-body
	#@-node:10:C=34:OnColorPanel
	#@+node:11:C=35:OnViewAllCharacters
	#@+body
	def OnViewAllCharacters (self, event=None):
	
		c = self.commands ; v = c.currentVnode() ; colorizer = c.tree.colorizer
		colorizer.showInvisibles = choose(colorizer.showInvisibles,0,1)
		# It is much easier to change the menu name here than in the menu updater.
		menu = c.frame.editMenu
		if colorizer.showInvisibles:
			setMenuLabel(menu,"Show Invisibles","Hide Invisibles")
		else:
			setMenuLabel(menu,"Hide Invisibles","Show Invisibles")
	
		c.tree.recolor_now(v)
		return "break" # inhibit further command processing
	#@-body
	#@-node:11:C=35:OnViewAllCharacters
	#@+node:12:C=36:OnPreferences
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:12:C=36:OnPreferences
	#@-node:1::Edit top level
	#@+node:2::Edit Body submenu
	#@+node:1::OnConvertBlanks & OnConvertAllBlanks
	#@+body
	def OnConvertBlanks(self,event=None):
	
		self.commands.convertBlanks()
		return "break" # inhibit further command processing
		
	def OnConvertAllBlanks(self,event=None):
	
		self.commands.convertAllBlanks()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnConvertBlanks & OnConvertAllBlanks
	#@+node:2::OnConvertTabs & OnConvertAllTabs
	#@+body
	def OnConvertTabs(self,event=None):
	
		self.commands.convertTabs()
		return "break" # inhibit further command processing
		
	def OnConvertAllTabs(self,event=None):
	
		self.commands.convertAllTabs()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnConvertTabs & OnConvertAllTabs
	#@+node:3::OnDedent
	#@+body
	def OnDedent (self,event=None):
	
		self.commands.dedentBody()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnDedent
	#@+node:4::OnExtract
	#@+body
	def OnExtract(self,event=None):
	
		self.commands.extract()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnExtract
	#@+node:5::OnExtractNames
	#@+body
	def OnExtractNames(self,event=None):
	
		self.commands.extractSectionNames()
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnExtractNames
	#@+node:6::OnExtractSection
	#@+body
	def OnExtractSection(self,event=None):
	
		self.commands.extractSection()
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnExtractSection
	#@+node:7::OnIndent
	#@+body
	def OnIndent(self,event=None):
	
		self.commands.indentBody()
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnIndent
	#@+node:8:C=37:OnInsertGraphicFile
	#@+body
	def OnInsertGraphicFile(self,event=None):
		
		c = self.commands
		
		filetypes = [("Gif", "*.gif"),("All files", "*.*")]
			# Only Gif images are allowed.
			#("Bitmap", "*.bmp"),
			#("Icon", "*.ico"),
		
		fileName = tkFileDialog.askopenfilename(
			title="Insert Graphic",
			filetypes=filetypes,
			defaultextension=".gif")
	
		if fileName and len(fileName) > 0 and os.path.exists(fileName):
			try:
				fileName = os.path.join(app().loadDir,fileName)
				fileName = os.path.normpath(fileName)
				image = Tkinter.PhotoImage(file=fileName)
			except:
				es("Exception loading: " + fileName)
				traceback.print_exc()
				image = None
			if image:
				# print image.height()
				index = c.body.index("insert")
				if 1: # same behavior
					bg = c.body.cget("background")
					w = Tkinter.Label(c.body,image=image,bd=0,bg=bg)
					c.body.window_create(index,window=w,align="baseline")
				else:
					c.body.image_create(index,image=image,align="baseline")
				#traceback.print_stack()
				# c.body.dump(index) # The image isn't drawn unless we take an exception!
				
		return "break" # inhibit further command processing
	#@-body
	#@-node:8:C=37:OnInsertGraphicFile
	#@-node:2::Edit Body submenu
	#@+node:3::Find submenu (frame methods)
	#@+node:1::OnFindPanel
	#@+body
	def OnFindPanel(self,event=None):
	
		find = app().findFrame
		find.top.deiconify()
		find.find_text.focus_set()
		find.commands = self
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnFindPanel
	#@+node:2::OnFindNext
	#@+body
	def OnFindNext(self,event=None):
	
		c = self.commands
		app().findFrame.findNextCommand(c)
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnFindNext
	#@+node:3::OnFindPrevious
	#@+body
	def OnFindPrevious(self,event=None):
	
		c = self.commands
		app().findFrame.findPreviousCommand(c)
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnFindPrevious
	#@+node:4::OnReplace
	#@+body
	def OnReplace(self,event=None):
	
		c = self.commands
		app().findFrame.changeCommand(c)
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnReplace
	#@+node:5::OnReplaceThenFind
	#@+body
	def OnReplaceThenFind(self,event=None):
	
		c = self.commands
		app().findFrame.changeThenFindCommand(c)
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnReplaceThenFind
	#@-node:3::Find submenu (frame methods)
	#@-node:2::Edit Menu (change to handle log pane too)
	#@+node:3::Outline Menu
	#@+node:1::top level
	#@+node:1::OnCutNode
	#@+body
	def OnCutNode(self,event=None):
	
		self.commands.cutOutline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnCutNode
	#@+node:2::OnCopyNode
	#@+body
	def OnCopyNode(self,event=None):
	
		self.commands.copyOutline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnCopyNode
	#@+node:3::OnPasteNodee
	#@+body
	def OnPasteNode(self,event=None):
	
		self.commands.pasteOutline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnPasteNodee
	#@+node:4::OnDeleteNode
	#@+body
	def OnDeleteNode(self,event=None):
	
		self.commands.deleteHeadline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnDeleteNode
	#@+node:5::OnInsertNode
	#@+body
	def OnInsertNode(self,event=None):
	
		self.commands.insertHeadline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnInsertNode
	#@+node:6::OnCloneNode
	#@+body
	def OnCloneNode(self,event=None):
	
		self.commands.clone()
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnCloneNode
	#@+node:7::OnSortChildren, OnSortSiblings
	#@+body
	def OnSortChildren(self,event=None):
	
		self.commands.sortChildren()
		return "break" # inhibit further command processing
		
	def OnSortSiblings(self,event=None):
	
		self.commands.sortSiblings()
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnSortChildren, OnSortSiblings
	#@-node:1::top level
	#@+node:2::Expand/Contract
	#@+node:1::OnContractParent
	#@+body
	def OnContractParent(self,event=None):
	
		self.commands.contractParent()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnContractParent
	#@+node:2::OnExpandAll
	#@+body
	def OnExpandAll(self,event=None):
	
		self.commands.expandAllHeadlines()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnExpandAll
	#@+node:3::OnExpandAllChildren
	#@+body
	def OnExpandAllChildren(self,event=None):
	
		self.commands.expandAllSubheads()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnExpandAllChildren
	#@+node:4::OnExpandChildren
	#@+body
	def OnExpandChildren(self,event=None):
	
		self.commands.expandSubheads()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnExpandChildren
	#@+node:5::OnContractAll
	#@+body
	def OnContractAll(self,event=None):
	
		self.commands.contractAllHeadlines()
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnContractAll
	#@+node:6::OnContractAllChildren
	#@+body
	def OnContractAllChildren(self,event=None):
	
		self.commands.contractAllSubheads()
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnContractAllChildren
	#@+node:7::OnContractChildren
	#@+body
	def OnContractChildren(self,event=None):
	
		self.commands.contractSubheads()
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnContractChildren
	#@+node:8::OnExpandNextLevel
	#@+body
	def OnExpandNextLevel(self,event=None):
	
		self.commands.expandNextLevel()
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnExpandNextLevel
	#@+node:9::OnExpandToLevel1
	#@+body
	def OnExpandToLevel1(self,event=None):
	
		self.commands.expandLevel1()
		return "break" # inhibit further command processing
	#@-body
	#@-node:9::OnExpandToLevel1
	#@+node:10::OnExpandToLevel2
	#@+body
	def OnExpandToLevel2(self,event=None):
	
		self.commands.expandLevel2()
		return "break" # inhibit further command processing
	#@-body
	#@-node:10::OnExpandToLevel2
	#@+node:11::OnExpandToLevel3
	#@+body
	def OnExpandToLevel3(self,event=None):
	
		self.commands.expandLevel3()
		return "break" # inhibit further command processing
	#@-body
	#@-node:11::OnExpandToLevel3
	#@+node:12::OnExpandToLevel4
	#@+body
	def OnExpandToLevel4(self,event=None):
	
		self.commands.expandLevel4()
		return "break" # inhibit further command processing
	#@-body
	#@-node:12::OnExpandToLevel4
	#@+node:13::OnExpandToLevel5
	#@+body
	def OnExpandToLevel5(self,event=None):
	
		self.commands.expandLevel5()
		return "break" # inhibit further command processing
	#@-body
	#@-node:13::OnExpandToLevel5
	#@+node:14::OnExpandToLevel6
	#@+body
	def OnExpandToLevel6(self,event=None):
	
		self.commands.expandLevel6()
		return "break" # inhibit further command processing
	#@-body
	#@-node:14::OnExpandToLevel6
	#@+node:15::OnExpandToLevel7
	#@+body
	def OnExpandToLevel7(self,event=None):
	
		self.commands.expandLevel7()
		return "break" # inhibit further command processing
	#@-body
	#@-node:15::OnExpandToLevel7
	#@+node:16::OnExpandToLevel8
	#@+body
	def OnExpandToLevel8(self,event=None):
	
		self.commands.expandLevel8()
		return "break" # inhibit further command processing
	#@-body
	#@-node:16::OnExpandToLevel8
	#@+node:17::OnExpandToLevel9
	#@+body
	def OnExpandToLevel9(self,event=None):
	
		self.commands.expandLevel9()
		return "break" # inhibit further command processing
	#@-body
	#@-node:17::OnExpandToLevel9
	#@-node:2::Expand/Contract
	#@+node:3::Move/Select
	#@+node:1:C=38:OnMoveDownwn
	#@+body
	def OnMoveDown(self,event=None):
	
		self.commands.moveOutlineDown()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1:C=38:OnMoveDownwn
	#@+node:2::OnMoveLeft
	#@+body
	def OnMoveLeft(self,event=None):
	
		self.commands.moveOutlineLeft()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnMoveLeft
	#@+node:3::OnMoveRight
	#@+body
	def OnMoveRight(self,event=None):
	
		self.commands.moveOutlineRight()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnMoveRight
	#@+node:4::OnMoveUp
	#@+body
	def OnMoveUp(self,event=None):
	
		self.commands.moveOutlineUp()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnMoveUp
	#@+node:5::OnPromote
	#@+body
	def OnPromote(self,event=None):
	
		self.commands.promote()
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnPromote
	#@+node:6::OnDemote
	#@+body
	def OnDemote(self,event=None):
	
		self.commands.demote()
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnDemote
	#@+node:7::OnGoPrevVisible
	#@+body
	def OnGoPrevVisible(self,event=None):
	
		self.commands.selectVisBack()
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnGoPrevVisible
	#@+node:8::OnGoNextVisible
	#@+body
	def OnGoNextVisible(self,event=None):
	
		self.commands.selectVisNext()
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnGoNextVisible
	#@+node:9::OnGoBack
	#@+body
	def OnGoBack(self,event=None):
	
		self.commands.selectThreadBack()
		return "break" # inhibit further command processing
	#@-body
	#@-node:9::OnGoBack
	#@+node:10::OnGoNext
	#@+body
	def OnGoNext(self,event=None):
	
		self.commands.selectThreadNext()
		return "break" # inhibit further command processing
	#@-body
	#@-node:10::OnGoNext
	#@-node:3::Move/Select
	#@+node:4::Mark/Goto
	#@+node:1::OnMark
	#@+body
	def OnMark(self,event=None):
	
		self.commands.markHeadline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnMark
	#@+node:2::OnMarkSubheads
	#@+body
	def OnMarkSubheads(self,event=None):
	
		self.commands.markSubheads()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnMarkSubheads
	#@+node:3::OnMarkChangedItems
	#@+body
	def OnMarkChangedItems(self,event=None):
	
		self.commands.markChangedHeadlines()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnMarkChangedItems
	#@+node:4::OnMarkChangedRoots
	#@+body
	def OnMarkChangedRoots(self,event=None):
	
		self.commands.markChangedRoots()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnMarkChangedRoots
	#@+node:5::OnUnmarkAll
	#@+body
	def OnUnmarkAll(self,event=None):
	
		self.commands.unmarkAll()
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnUnmarkAll
	#@+node:6::OnGoToNextMarked
	#@+body
	def OnGoToNextMarked(self,event=None):
	
		self.commands.goToNextMarkedHeadline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnGoToNextMarked
	#@+node:7::OnGoToNextChanged
	#@+body
	def OnGoToNextChanged(self,event=None):
	
		self.commands.goToNextDirtyHeadline()
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnGoToNextChanged
	#@-node:4::Mark/Goto
	#@-node:3::Outline Menu
	#@+node:4::Window Menu
	#@+node:1::OnEqualSizedPanes
	#@+body
	def OnEqualSizedPanes(self,event=None):
	
		self.resizePanesToRatio(0.5)
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnEqualSizedPanes
	#@+node:2:C=39:OnToggleActivePane
	#@+body
	def OnToggleActivePane (self,event=None):
	
		# trace(`event`)
		if self.getFocus() == self.body:
			self.canvas.focus_force()
		else:
			self.body.focus_force()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2:C=39:OnToggleActivePane
	#@+node:3:C=40:OnToggleSplitDirection
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
		ratio = choose(verticalFlag,0.5,0.3)
		self.resizePanesToRatio(ratio)
		return "break" # inhibit further command processing
	#@-body
	#@-node:3:C=40:OnToggleSplitDirection
	#@+node:4:C=41:OnCascade
	#@+body
	def OnCascade(self,event=None):
		
		c = self ; x,y,delta = 10,10,10
		for frame in app().windowList:
			top = frame.top
			# Compute w,h
			top.update_idletasks() # Required to get proper info.
			g = top.geometry() # g = "WidthxHeight+XOffset+YOffset"
			dim,junkx,junky = string.split(g,'+')
			w,h = string.split(dim,'x')
			w,h = int(w),int(h)
			# Set new x,y and old w,h
			frame.top.geometry("%dx%d%+d%+d" % (w,h,x,y))
			# Compute the new offsets.
			x += 30 ; y += 30
			if x > 200:
				x = 10 + delta ; y = 40 + delta
				delta += 10
		
		return "break" # inhibit further command processing

	#@-body
	#@-node:4:C=41:OnCascade
	#@+node:5::OnMinimizeAll
	#@+body
	def OnMinimizeAll(self,event=None):
	
		self.minimize(app().findFrame)
		self.minimize(app().pythonFrame)
		for frame in app().windowList:
			self.minimize(frame)
		return "break" # inhibit further command processing
			
	def minimize(self, frame):
	
		if frame and frame.top.state() == "normal":
			frame.top.iconify()
	#@-body
	#@-node:5::OnMinimizeAll
	#@+node:6:C=42:OnOpenCompareWindow
	#@+body
	def OnOpenCompareWindow (self):
		
		c = self.commands
		cp = self.comparePanel
		
		if cp:
			cp.top.deiconify()
		else:
			cmp = leoCompare.leoCompare(c)
			self.comparePanel = cp =  leoCompare.leoComparePanel(c,cmp)
			cp.run()
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:6:C=42:OnOpenCompareWindow
	#@+node:7:C=43:OnOpenPythonWindow
	#@+body
	def OnOpenPythonWindow(self,event=None):
	
		try:
			import idle
			if app().idle_imported:
				reload(idle)
			app().idle_imported = true
		except:
			try:
				executable_dir = os.path.dirname(sys.executable)
				idle_dir=os.path.join(executable_dir, "tools/idle")
				sys.path.append(idle_dir)
				# Try again
				import idle
				app().idle_imported = true
			except:
				es("Can not import idle")
				es("Please add \Python2x\Tools\idle to sys.paths")
				traceback.print_exc()
	
		return "break" # inhibit further command processing.
	#@-body
	#@-node:7:C=43:OnOpenPythonWindow
	#@-node:4::Window Menu
	#@+node:5::Help Menu
	#@+node:1:C=44:OnAbout (version number)
	#@+body
	def OnAbout(self,event=None):
		
		# Don't use triple-quoted strings or continued strings here.
		# Doing so would add unwanted leading tabs.
		version = "leo.py 3.5, August 14, 2002\n\n"
		copyright = (
			"Copyright 1999-2002 by Edward K. Ream\n" +
			"All Rights Reserved\n" +
			"Leo is distributed under the Python License")
		url = "http://personalpages.tds.net/~edream/front.html"
		email = "edream@tds.net"
	
		if 1: # Much better looking and includes icon.
			import leoDialog
			d = leoDialog.leoDialog()
			d.aboutLeo(version,copyright,url,email)
		else:
			import tkMessageBox
			tkMessageBox.showinfo("About Leo",
				version + copyright + '\n' + url + '\n' + email)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:1:C=44:OnAbout (version number)
	#@+node:2::OnLeoDocumentation
	#@+body
	def OnLeoDocumentation (self,event=None):
	
		dir = app().loadDir
		fileName = os.path.join(dir, "LeoDocs.leo")
		try:
			self.OpenWithFileName(fileName)
		except:
			es("not found: LeoDocs.leo")
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnLeoDocumentation
	#@+node:3::OnLeoHome
	#@+body
	def OnLeoHome (self,event=None):
		
		import webbrowser
		
		url = "http://personalpages.tds.net/~edream/front.html"
		try:
			webbrowser.open(url)
		except:
			es("not found: " + url)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnLeoHome
	#@+node:4::OnLeoHelp
	#@+body
	def OnLeoHelp (self,event=None):
		
		f = os.path.join(app().loadDir,"sbooks.chm")
		if os.path.exists(f):
			os.startfile(f)
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
						urllib.urlretrieve(url,f,self.showProgressBar)
						if self.scale:
							self.scale.destroy()
							self.scale = None
					else:
						url = "http://prdownloads.sourceforge.net/leo/sbooks.chm?download"
						import webbrowser
						os.chdir(app().loadDir)
						webbrowser.open(url)
				except:
					es("exception dowloading sbooks.chm")
					traceback.print_exc()
	
		return "break" # inhibit further command processing
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
	#@+node:5:C=45:OnLeoTutorial (version number)
	#@+body
	def OnLeoTutorial (self,event=None):
		
		import webbrowser
		
		version = "?vernum=3.5"
		url = "http://www.evisa.com/e/sbooks/leo/sbframetoc_ie.htm"
	
		try:
			webbrowser.open(url + version)
		except:
			es("not found: " + url)
		
		return "break" # inhibit further command processing
	#@-body
	#@-node:5:C=45:OnLeoTutorial (version number)
	#@-node:5::Help Menu
	#@-node:14:C=16:Menu Command Handlers
	#@+node:15:C=46:Splitter stuff
	#@+body
	#@+at
	#  The key invariants used throughout this code:
	# 
	# 1. self.splitVerticalFlag tells the alignment of the main splitter and
	# 2. not self.splitVerticalFlag tells the alignment of the secondary splitter.
	# 
	# Only the general-purpose divideAnySplitter routine doesn't know about these invariants.  So most of this code is specialized 
	# for Leo's window.  OTOH, creating a single splitter window would be much easier than this code.

	#@-at
	#@-body
	#@+node:1::bindBar
	#@+body
	def bindBar (self, bar, verticalFlag):
		
		if verticalFlag == self.splitVerticalFlag:
			bar.bind("<B1-Motion>", self.onDragMainSplitBar)
		else:
			bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)
	#@-body
	#@-node:1::bindBar
	#@+node:2:C=47:configureBar
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
			es("error in user configuration for splitbar")
			traceback.print_exc()
			if verticalFlag:
				# Panes arranged vertically; horizontal splitter bar
				bar.configure(height=7,cursor="sb_v_double_arrow")
			else:
				# Panes arranged horizontally; vertical splitter bar
				bar.configure(width=7,cursor="sb_h_double_arrow")
	#@-body
	#@-node:2:C=47:configureBar
	#@+node:3:C=48:createBothLeoSplitters (use config.body_font,etc)
	#@+body
	def createBothLeoSplitters (self,top):
	
		Tk = Tkinter ; config = app().config
	
		# Splitter 1 is the main splitter containing splitter2 and the body pane.
		f1,bar1,split1Pane1,split1Pane2 = self.createLeoSplitter(top, self.splitVerticalFlag)
		self.f1,self.bar1 = f1,bar1
		self.split1Pane1,self.split1Pane2 = split1Pane1,split1Pane2
		# Splitter 2 is the secondary splitter containing the tree and log panes.
		f2,bar2,split2Pane1,split2Pane2 = self.createLeoSplitter(split1Pane1, not self.splitVerticalFlag)
		self.f2,self.bar2 = f2,bar2
		self.split2Pane1,self.split2Pane2 = split2Pane1,split2Pane2
		
		#@<< create the body pane >>
		#@+node:1:C=49:<< create the body pane >>
		#@+body
		# A light selectbackground value is needed to make syntax coloring look good.
		wrap = config.getBoolWindowPref('body_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		self.body = body = Tk.Text(split1Pane2,name='body',
			bd=2,bg="white",relief="flat",
			setgrid=1,wrap=wrap,
			# selectforeground="white",
			selectbackground="Gray80")
		
		font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight")
		
		if font:
			body.configure(font=font)
		
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
		#@-node:1:C=49:<< create the body pane >>

		
		#@<< create the tree pane >>
		#@+node:2::<< create the tree pane >>
		#@+body
		scrolls = config.getBoolWindowPref('outline_pane_scrolls_horizontally')
		scrolls = choose(scrolls,1,0)
		
		self.canvas = tree = Tk.Canvas(split2Pane1,name="tree",
			bd=0,bg="white",relief="flat")
		
		# The font is set in the tree code.
		
		# These do nothing...
		# selectborderwidth=0,selectforeground="white",selectbackground="white")
		self.treeBar = treeBar = Tk.Scrollbar(split2Pane1,name="treeBar")
		
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
		#@-node:2::<< create the tree pane >>

		
		#@<< create the log pane >>
		#@+node:3::<< create the log pane >>
		#@+body
		wrap = config.getBoolWindowPref('log_pane_wraps')
		wrap = choose(wrap,"word","none")
		
		self.log = log = Tk.Text(split2Pane2,name="log",
			setgrid=1,wrap=wrap,bd=2,bg="white",relief="flat")
			
		font = config.getFontFromParams(
			"log_text_font_family", "log_text_font_size",
			"log_text_font_slant",  "log_text_font_weight")
		
		if font:
			log.configure(font=font)
		
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
		#@-node:3::<< create the log pane >>

		# Give the log and body panes the proper borders.
		self.reconfigurePanes()
	#@-body
	#@-node:3:C=48:createBothLeoSplitters (use config.body_font,etc)
	#@+node:4::createLeoSplitter (use config params)
	#@+body
	# Create a splitter window and panes into which the caller packs widgets.
	# Returns (f, bar, pane1, pane2)
	
	def createLeoSplitter (self, parent, verticalFlag):
	
		Tk = Tkinter
		# Create the frames.
		f = Tk.Frame(parent,width="8i",height="6.5i",bd=0,bg="white",relief="flat")
		f.pack(expand=1,fill="both")
		pane1 = Tk.Frame(f,bd=0,bg="white",relief="flat")
		pane2 = Tk.Frame(f,bg="white",relief="flat")
		bar =   Tk.Frame(f,bd=2,relief="raised",bg="LightSteelBlue2")
		# Configure and place the frames.
		self.configureBar(bar,verticalFlag)
		self.bindBar(bar,verticalFlag)
		self.placeSplitter(bar,pane1,pane2,verticalFlag)
		
		return f, bar, pane1, pane2
	#@-body
	#@-node:4::createLeoSplitter (use config params)
	#@+node:5::divideAnySplitter
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
	#@-node:5::divideAnySplitter
	#@+node:6::divideLeoSplitter
	#@+body
	# Divides the main or secondary splitter, using the key invariant.
	def divideLeoSplitter (self, verticalFlag, frac):
		if self.splitVerticalFlag == verticalFlag:
			self.divideLeoSplitter1(frac,verticalFlag)
			self.ratio = frac # Ratio of body pane to tree pane.
		else:
			self.divideLeoSplitter2(frac,verticalFlag)
	
	# Divides the main splitter.
	def divideLeoSplitter1 (self, frac, verticalFlag): 
		self.divideAnySplitter(frac, verticalFlag,
			self.bar1, self.split1Pane1, self.split1Pane2)
	
	# Divides the secondary splitter.
	def divideLeoSplitter2 (self, frac, verticalFlag): 
		self.divideAnySplitter (frac, verticalFlag,
			self.bar2, self.split2Pane1, self.split2Pane2)
	#@-body
	#@-node:6::divideLeoSplitter
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
	#@+node:9::reconfigurePanes (use config bar_width)
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
	#@-node:9::reconfigurePanes (use config bar_width)
	#@-node:15:C=46:Splitter stuff
	#@-others
#@-body
#@-node:0::@file leoFrame.py
#@-leo
