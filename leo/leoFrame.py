#@+leo

#@+node:0::@file leoFrame.py
#@+body
from leoGlobals import *
from leoUtils import *
import leoDialog, leoNodes
import Tkinter, tkFileDialog, tkFont

# Needed for menu commands
import leoCommands, leoNodes, leoTree
import os, sys

class LeoFrame:

	#@+others
	#@+node:1:C=1:frame.__init__
	#@+body
	def __init__(self, title = None):
	
		Tk = Tkinter
		
		#@<< set the LeoFrame ivars >>
		#@+node:1::<< set the LeoFrame ivars >>
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
			
		self.outlineToNowebDefaultFileName = "noweb.nw" # For Outline To Noweb dialog.
		
		self.title=title # Title of window, not including dirty mark
		self.saved=false # True if ever saved
		self.startupWindow=false # True if initially opened window
		self.openDirectory = ""
		self.splitVerticalFlag = true # True: main paines split vertically (horizontal main splitter)
		self.ratio = 0.5 # Ratio of body pane to tree pane.
		self.es_newlines = 0 # newline count for this log stream
		
		# Created below
		self.log = None
		self.body = None
		self.tree = None
		self.treeBar = None # Used by tree.idle_scrollTo
		self.canvas = None
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
		#@-body
		#@-node:1::<< set the LeoFrame ivars >>

		self.top = top = Tk.Toplevel()
		if sys.platform=="win32":
			self.hwnd = top.frame()
			# trace("__init__", "frame.__init__: self.hwnd:" + `self.hwnd`)
		top.title(title)
		top.minsize(30,10) # This doesn't work as I expect.
		g = "+%d%+d" % (30, 30)
		top.geometry(g)
		
		
		#@<< create the Leo frame >>
		#@+node:2::<< create the Leo frame >>
		#@+body
		# Create two splitters
		# Splitter 1 contains splitter2 and the body pane.
		# Splitter 2 contains the tree and log panes.
		bar1, split1Pane1, split1Pane2 = self.createSplitter(top, self.splitVerticalFlag)
		self.bar1, self.split1Pane1, self.split1Pane2 = bar1, split1Pane1, split1Pane2
		
		bar2, split2Pane1, split2Pane2 = self.createSplitter(split1Pane1, not self.splitVerticalFlag)
		self.bar2, self.split2Pane1, self.split2Pane2 = bar2, split2Pane1, split2Pane2
		
		# Create the body pane.
			# Verdana is good looking, but not fixed size.
			# Courier is fixed size, not great looking.
			# A light selectbackground value is needed to make syntax coloring look good.
		
		# EKR 2/28/02: made code size platform dependent.
		if sys.platform=="win32": # Windows
			font = tkFont.Font(family="Courier",size=9)
		else:
			font = tkFont.Font(family="Courier",size=12)
		
		tabw = font.measure("    ")
		self.body = body = Tk.Text(split1Pane2,name='body',bd=2,bg="white",relief="flat",
			setgrid=1,font=font,tabs=tabw,wrap="word",selectbackground="Gray80")
		bodyBar = Tk.Scrollbar(split1Pane2,name='bodyBar')
		body['yscrollcommand'] = bodyBar.set
		bodyBar['command'] = body.yview
		bodyBar.pack(side="right", fill="y")
		body.pack(expand=1, fill="both")
		
		# Create the tree pane.
		self.canvas = tree = Tk.Canvas(split2Pane1,name="tree",bd=0,bg="white",relief="flat")
			# These do nothing...
			# selectborderwidth=0,selectforeground="white",selectbackground="white")
		self.treeBar = treeBar = Tk.Scrollbar(split2Pane1,name="treeBar")
		tree['yscrollcommand'] = treeBar.set
		treeBar['command'] = tree.yview
		
		treeBar.pack(side="right", fill="y")
		tree.pack(expand=1,fill="both")
		
		# Create the log pane.
		# -padx is needed to handle overlap of splitter bar
		self.log = log = Tk.Text(split2Pane2,name="log",setgrid=1,wrap="word",
			bd=4,bg="white",relief="flat")
		logBar = Tk.Scrollbar(split2Pane2,name="logBar")
		log['yscrollcommand'] = logBar.set
		logBar['command'] = log.yview
		
		logBar.pack(side="right", fill="y")
		log.pack(expand=1, fill="both")
		#@-body
		#@-node:2::<< create the Leo frame >>

		self.commands = c = leoCommands.Commands(self)
		self.tree = leoTree.leoTree(self.commands, self.canvas)
		c.tree = self.tree
		
		#@<< create the first tree node >>
		#@+node:3::<< create the first tree node >>
		#@+body
		t = leoNodes.tnode()
		v = leoNodes.vnode(c,t)
		v.initHeadString("NewHeadline")
		v.moveToRoot()
		c.tree.redraw()
		c.tree.canvas.focus_get()
		c.editVnode(v)
		#@-body
		#@-node:3::<< create the first tree node >>

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
		# self.body.bind("<Control-d>", self.OnMoveDown) # Makes control-d problem worse!!
		self.body.bind(virtual_event_name("Cut"), self.OnCut)
		self.body.bind(virtual_event_name("Copy"), self.OnCopy)
		self.body.bind(virtual_event_name("Paste"), self.OnPaste)
	#@-body
	#@-node:1:C=1:frame.__init__
	#@+node:2:C=2:frame.__del__
	#@+body
	# Warning:  call del self will not necessarily call this routine.
	
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
	#@-node:2:C=2:frame.__del__
	#@+node:3::frame.__repr__
	#@+body
	def __repr__ (self):
	
		return "leoFrame: " + self.title

	#@-body
	#@-node:3::frame.__repr__
	#@+node:4:C=3:frame.destroy
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
	#@-node:4:C=3:frame.destroy
	#@+node:5:C=4:createMenuBar
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
		fileMenu.add_command(label="Revert To Saved",command=self.OnRevert) # ,state="disabled") #
		fileMenu.add_separator()
		

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

		
		#@<< create the read/write submenu >>
		#@+node:2::<< create the read/write submenu >>
		#@+body
		readWriteMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Read/Write...", menu=readWriteMenu)
		
		readWriteMenu.add_command(label="Read Outline Only",command=self.OnReadOutlineOnly)
		readWriteMenu.add_command(label="Read @file Nodes",command=self.OnReadAtFileNodes)
		readWriteMenu.add_command(label="Write Outline Only",command=self.OnWriteOutlineOnly)
		readWriteMenu.add_command(label="Write @file Nodes",command=self.OnWriteAtFileNodes)
		#@-body
		#@-node:2::<< create the read/write submenu >>

		
		#@<< create the tangle submenu >>
		#@+node:3::<< create the tangle submenu >>
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
		#@-node:3::<< create the tangle submenu >>

		
		#@<< create the untangle submenu >>
		#@+node:4::<< create the untangle submenu >>
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
		#@-node:4::<< create the untangle submenu >>

		
		#@<< create the import submenu >>
		#@+node:5::<< create the import submenu >>
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
		#@-node:5::<< create the import submenu >>

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
		editBodyMenu.add_command(label="Convert Blanks",
			accelerator="Shift+Ctrl+B",command=self.OnConvertBlanks)
		editBodyMenu.add_separator()
		
		editBodyMenu.add_command(label="Indent",
			accelerator="Ctrl+]",command=self.OnIndent)
		editBodyMenu.add_command(label="Unindent",
			accelerator="Ctrl+[",command=self.OnDedent)
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

		editMenu.add_command(label="Font Panel",
			accelerator="Shift+Alt+T",command=self.OnFontPanel,state="disabled") #
		editMenu.add_command(label="Syntax Coloring...",
			accelerator="Shift+Alt+S",command=self.OnSyntaxColoring,state="disabled") #
		
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
			accelerator="Ctrl+Up",command=self.OnGoPrevVisible)
		moveSelectMenu.add_command(label="Go Next Visible",
			accelerator="Ctrl+Down",command=self.OnGoNextVisible)
		moveSelectMenu.add_separator()
		
		moveSelectMenu.add_command(label="Go Back",
			accelerator="Shift+Ctrl+Up",command=self.OnGoBack)
		moveSelectMenu.add_command(label="Go Next",
			accelerator="Shift+Ctrl+Down",command=self.OnGoNext)
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
			command=self.OnToggleSplitDirection, state="disabled") #
		windowMenu.add_separator()
		
		windowMenu.add_command(label="Cascade",
			command=self.OnCascade)
		windowMenu.add_command(label="Minimize All",
			command=self.OnMinimizeAll,state="disabled") #
		windowMenu.add_separator()
		
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
		helpMenu.add_command(label="Leo Documentation...", command=self.OnLeoDocumentation)
		#@-body
		#@-node:5::<< create the help menu >>

		top.config(menu=menu) # Display the menu.
	#@-body
	#@-node:5:C=4:createMenuBar
	#@+node:6:C=5:createAccelerators
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
			
			# Note: These keys must be bound _only_ to the body pane!
			# ("Down", self.OnGoNextVisible),
			# ("Up", self.OnGoPrevVisible),
			# ("Shift-Down", self.OnGoBack),
			# ("Shift-Up", self.OnGoNext),
			
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
			# J reserved
			# K unused
			# L unused
			("M", self.OnTangleMarked),
			("N", self.OnExtractNames),
			# O unused
			# P unused
			# Q unused
			# R unused
			("S", self.OnSaveAs),
			("T", self.OnTangle),
			("U", self.OnUntangle),
			("V", self.OnPasteNode),
			# W unused
			("X", self.OnCutNode),
			("Z", self.OnRedo)
			#@-body
			#@-node:1::<< control key bindings >>

		]
		# Warnings: two sets of actions will be taken for these
		# unless all event handlers returns "break".
		for accel, command in controlBindings:
			body.bind("<Control-" + accel + ">", command) # Necessary to override defaults in body.
			top.bind("<Control-" + accel + ">", command)
			
		# These keys must be bound only in the canvas widget.
		canvasControlBindings = [
			
			#@<< canvas control bindings >>
			#@+node:2::<< canvas control bindings >>
			#@+body
			("Down", self.OnGoNextVisible),
			("Up", self.OnGoPrevVisible),
			("Shift-Down", self.OnGoNext),
			("Shift-Up", self.OnGoBack),
			#@-body
			#@-node:2::<< canvas control bindings >>

		]
		for accel, command in canvasControlBindings:
			canvas.bind("<Control-" + accel + ">", command)
	
		altBindings = [
			
			#@<< alt key bindings >>
			#@+node:3::<< alt key bindings >>
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
			# Shift-Alt
			# ("E", self.OnExecuteScript),
			("S", self.OnSyntaxColoring),
			("T", self.OnFontPanel)
			#@-body
			#@-node:3::<< alt key bindings >>

		]
		# Warnings: two sets of actions will be taken for these
		# unless all event handlers returns "break".
		for accel, command in altBindings:
			body.bind("<Alt-" + accel + ">", command) # Necessary to override defaults in body.
			top.bind("<Alt-" + accel + ">", command)
			
		if 0: # A useful trace
			print_bindings("top",self.top)
			print_bindings("body",self.body)
			print_bindings("canvas",self.canvas)
	#@-body
	#@-node:6:C=5:createAccelerators
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
	#@+node:8::notYet
	#@+body
	def notYet(self,name):
	
		es(name + " not ready yet")

	#@-body
	#@-node:8::notYet
	#@+node:9:C=6:frame.put, putnl
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
	#@-node:9:C=6:frame.put, putnl
	#@+node:10::resizePanesToRatio
	#@+body
	def resizePanesToRatio(self,ratio):
	
		self.divideSplitter(self.splitVerticalFlag, 0.5)

	#@-body
	#@-node:10::resizePanesToRatio
	#@+node:11::Event handlers
	#@+node:1:C=7:frame.OnCloseLeoEvent
	#@+body
	# Called from quit logic and when user closes the window.
	# Returns true if the close happened.
	
	def OnCloseLeoEvent(self):
	
		# trace(`self in app().windowList` + ":" + `self`)
		veto=false
		c = self.commands
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
						defaultextension="leo")
						
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
		app().log = None # no log until we reactive a window
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
	#@-node:1:C=7:frame.OnCloseLeoEvent
	#@+node:2:C=8:OnActivateLeoEvent
	#@+body
	def OnActivateLeoEvent(self,event=None):
	
		c = self.commands
		app().log = self
		# 2/9/02: It is very important to handle Default Tangle Directory properly!
		prefs = app().prefsFrame
		if prefs:
			prefs.init(c)
	#@-body
	#@-node:2:C=8:OnActivateLeoEvent
	#@+node:3:C=9:OnActivateBody & OnBodyDoubleClick
	#@+body
	def OnActivateBody (self,event=None):
	
		app().log = self
		self.tree.OnDeactivate()
	
	def OnBodyDoubleClick (self,event=None):
	
		body = self.body
		start = body.index("insert wordstart")
		end = body.index("insert wordend")
		setTextSelection(self.body,start,end)
		return "break" # Inhibit all further event processing.
	#@-body
	#@-node:3:C=9:OnActivateBody & OnBodyDoubleClick
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
	#@-node:11::Event handlers
	#@+node:12:C=10:Menu enablers (Frame)
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
	#@-node:12:C=10:Menu enablers (Frame)
	#@+node:13:C=11:Menu Command Handlers
	#@+node:1::File Menu (Unfinished: Page Setup, Print, Import...)
	#@+node:1::top level
	#@+node:1::OnNew
	#@+body
	def OnNew (self,event=None):
	
		frame = LeoFrame() # Create another Leo window.
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
	#@-node:1::OnNew
	#@+node:2:C=12:frame.OnOpen
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
			defaultextension="leo")
	
		if fileName and len(fileName) > 0:
			ok, frame = self.OpenWithFileName(fileName)
			if ok and closeFlag:
				app().windowList.remove(self)
				self.destroy() # force the window to go away now.
				app().log = frame # Sets the log stream for es()
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2:C=12:frame.OnOpen
	#@+node:3:C=13:frame.OpenWithFileName
	#@+body
	def OpenWithFileName(self, fileName):
	
		if not fileName or len(fileName) == 0:
			return false, None
			
		# Display the _unnormalized_ file name
		oldFileName = fileName
			
		# Create a full normalized path name only for comparison.
		fileName = os.path.join(os.getcwd(), fileName)
		fileName = os.path.normcase(fileName)
		fileName = os.path.normpath(fileName)
	
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
	
		file = open(fileName,'r')
		if file:
			frame = LeoFrame(fileName)
			frame.top.deiconify()
			frame.top.lift()
			app().root.update() # Force a screen redraw immediately.
			frame.commands.fileCommands.open(file,fileName) # closes file.
			frame.openDirectory=os.path.dirname(fileName)
			return true, frame
		else:
			es("can not open:" + fileName)
			return false, None
	#@-body
	#@-node:3:C=13:frame.OpenWithFileName
	#@+node:4::OnClose
	#@+body
	# Called when File-Close command is chosen.
	
	def OnClose(self,event=None):
		
		self.OnCloseLeoEvent() # Destroy the frame unless the user cancels.
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnClose
	#@+node:5:C=14:OnSave
	#@+body
	def OnSave(self,event=None):
	
		c = self.commands
		
		# Make sure we never pass None to the ctor.
		if not self.mFileName:
			self.title = ""
	
		if self.mFileName != "":
			c.fileCommands.save(self.mFileName)
			c.setChanged(false)
			return "break" # inhibit further command processing
	
		self.mFileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Save",
			filetypes=[("Leo files", "*.leo")],
			defaultextension="leo")
	
		if len(self.mFileName) > 0:
			self.mFileName = ensure_extension(self.mFileName, ".leo")
			self.title = self.mFileName
			self.top.title(self.mFileName)
			c.fileCommands.save(self.mFileName)
		return "break" # inhibit further command processing
	#@-body
	#@-node:5:C=14:OnSave
	#@+node:6::OnSaveAs
	#@+body
	def OnSaveAs(self,event=None):
	
		# Make sure we never pass None to the ctor.
		if not self.mFileName:
			self.title = ""
			
		self.mFileName = tkFileDialog.asksaveasfilename(
			initialfile = self.mFileName,
			title="Save As",
			filetypes=[("Leo files", "*.leo")],
			defaultextension="leo")
	
		if len(self.mFileName) > 0:
			self.mFileName = ensure_extension(self.mFileName, ".leo")
			self.title = self.mFileName
			self.top.title(self.mFileName)
			self.commands.fileCommands.saveAs(self.mFileName)
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnSaveAs
	#@+node:7::OnSaveTo
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
			defaultextension="leo")
	
		if len(fileName) > 0:
			fileName = ensure_extension(fileName, ".leo")
			self.commands.fileCommands.saveTo(fileName)
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnSaveTo
	#@+node:8:C=15:OnRevert (rewrite)
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
	#@-node:8:C=15:OnRevert (rewrite)
	#@+node:9:C=16:frame.OnQuit
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
	#@-node:9:C=16:frame.OnQuit
	#@-node:1::top level
	#@+node:2::Read/Write submenu
	#@+node:1:C=17:fileCommands.OnReadOutlineOnly
	#@+body
	def OnReadOutlineOnly (self,event=None):
	
		fileName = tkFileDialog.askopenfilename(
			title="Read Outline Only",
			filetypes=[("Leo files", "*.leo"), ("All files", "*")],
			defaultextension="leo")
	
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
	#@-node:1:C=17:fileCommands.OnReadOutlineOnly
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
	#@-node:2::Read/Write submenu
	#@+node:3::Tangle submenu
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
	#@-node:3::Tangle submenu
	#@+node:4::Untangle submenu
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
	#@-node:4::Untangle submenu
	#@+node:5:C=18:Import&Export submenu
	#@+node:1::OnFlattenOutline
	#@+body
	def OnFlattenOutline (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Flatten Outline",filetypes=filetypes,
			initialfile="flat.txt",defaultextension="txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.flattenOutline(fileName)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnFlattenOutline
	#@+node:2::OnImportAtFile
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
	
		d = leoDialog.leoDialog()
		answer = d.askOkCancel("Proceed?",
			"Import to @file is not undoable." +
			"\nProceed?")
	
		if answer=="ok":
			fileName = tkFileDialog.askopenfilename(
				title="Import To @file",filetypes=types)
			if fileName and len(fileName) > 0:
				c = self.commands
				paths = [fileName] # alas, askopenfilename returns only a single name.
				c.importCommands.importFilesCommand (paths,"@file")
				c.undoer.clearUndoState()
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnImportAtFile
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
			
		d = leoDialog.leoDialog()
		answer = d.askOkCancel("Proceed?",
			"Import to @root is not undoable." +
			"\nProceed?")
	
		if answer=="ok":
			fileName = tkFileDialog.askopenfilename(
				title="Import To @root",filetypes=types)
			if fileName and len(fileName) > 0:
				c = self.commands
				paths = [fileName] # alas, askopenfilename returns only a single name.
				c.importCommands.importFilesCommand (paths,"@root")
				c.undoer.clearUndoState()
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnImportAtRoot
	#@+node:4::OnImportCWEBFiles
	#@+body
	def OnImportCWEBFiles (self,event=None):
		
		filetypes = [
			("CWEB files", "*.w"),
			("Text files", "*.txt"),
			("All files", "*")]
			
		d = leoDialog.leoDialog()
		answer = d.askOkCancel("Proceed?",
			"Import CWEB files is not undoable." +
			"\nProceed?")
		
		if answer=="ok":
			fileName = tkFileDialog.askopenfilename(
				title="Import CWEB Files",filetypes=filetypes,
				defaultextension="w")
			if fileName and len(fileName) > 0:
				c = self.commands
				paths = [fileName] # alas, askopenfilename returns only a single name.
				c.importCommands.importWebCommand(paths,"cweb")
				c.undoer.clearUndoState()
		
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnImportCWEBFiles
	#@+node:5::OnImportFlattenedOutline
	#@+body
	def OnImportFlattenedOutline (self,event=None):
		
		types = [("Text files","*.txt"), ("All files","*")]
		
		d = leoDialog.leoDialog()
		answer = d.askOkCancel("Proceed?",
			"Import Flattened Outline is not undoable." +
			"\nProceed?")
		
		if answer=="ok":
			fileName = tkFileDialog.askopenfilename(
				title="Import MORE Text",
				filetypes=types,
				defaultextension="py")
			if fileName and len(fileName) > 0:
				c = self.commands
				paths = [fileName] # alas, askopenfilename returns only a single name.
				c.importCommands.importFlattenedOutline(paths)
				c.undoer.clearUndoState()
			
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
			
		d = leoDialog.leoDialog()
		answer = d.askOkCancel("Proceed?",
			"Import Noweb files is not undoable." +
			"\nProceed?")
		
		if answer=="ok":
			fileName = tkFileDialog.askopenfilename(
				title="Import Noweb Files",filetypes=filetypes,
				defaultextension="nw")
			if fileName and len(fileName) > 0:
				c = self.commands
				paths = [fileName] # alas, askopenfilename returns only a single name.
				c.importCommands.importWebCommand(paths,"noweb")
				c.undoer.clearUndoState()
		
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
			initialfile="cweb.w",defaultextension="w")
	
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
			initialfile=self.outlineToNowebDefaultFileName,defaultextension="nw")
	
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
	#@-node:5:C=18:Import&Export submenu
	#@-node:1::File Menu (Unfinished: Page Setup, Print, Import...)
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
	#@+node:3:C=19:frame.OnCut, OnCutFrom Menu
	#@+body
	def OnCut (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.commands.tree.onBodyWillChange(v,"Cut")
		
		# Copy the selection to the internal clipboard.
		app().clipboard = getSelectedText(self.body)
		# trace(`app().clipboard`)
		return # Allow the actual cut!
	
	def OnCutFromMenu (self,event=None):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Cut"))
	#@-body
	#@-node:3:C=19:frame.OnCut, OnCutFrom Menu
	#@+node:4:C=20:frame.OnCopy, OnCopyFromMenu
	#@+body
	def OnCopy (self,event=None):
	
		# Copy never changes dirty bits or syntax coloring.
		
		# Copy the selection to the internal clipboard.
		app().clipboard = getSelectedText(self.body)
		# trace(`app().clipboard`)
		return # Allow the actual copy!
		
	def OnCopyFromMenu (self,event=None):
	
		# trace()
		w = self.getFocus()
		w.event_generate(virtual_event_name("Copy"))
	#@-body
	#@-node:4:C=20:frame.OnCopy, OnCopyFromMenu
	#@+node:5:C=21:frame.OnPaste, OnPasteNode, OnPasteFromMenu
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
	#@-node:5:C=21:frame.OnPaste, OnPasteNode, OnPasteFromMenu
	#@+node:6:C=22:OnDelete
	#@+body
	def OnDelete(self,event=None):
	
		c = self.commands ; v = c.currentVnode()
		first, last = getTextSelection(self.body)
		if first and last:
			self.body.delete(first,last)
			c.tree.onBodyChanged(v,"Delete")
		return "break" # inhibit further command processing
	#@-body
	#@-node:6:C=22:OnDelete
	#@+node:7:C=23:OnSelectAll
	#@+body
	def OnSelectAll(self,event=None):
	
		setTextSelection(self.body,"1.0","end")
		return "break" # inhibit further command processing
	#@-body
	#@-node:7:C=23:OnSelectAll
	#@+node:8::OnEditHeadline
	#@+body
	def OnEditHeadline(self,event=None):
	
		tree = self.commands.tree
		tree.editLabel(tree.currentVnode)
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnEditHeadline
	#@+node:9::OnFontPanel (set font)
	#@+body
	def OnFontPanel(self,event=None):
	
		self.notYet("Font Panel")
		return "break" # inhibit further command processing
	
		data = SetInitialFont(self.body.GetFont())
		data.SetColour(self.body.GetForegroundColour())
	
		d = wxFontDialog (self, data)
		if wxPlatform != "__WXGTK__": # Causes problems on GTK+.
			dialog.CentreOnScreen()
	
		if d.ShowModal() != wxID_OK:
			return "break" # inhibit further command processing
		retData = d.GetFontData()
		font = retData.GetChosenFont()
		color = retData.GetColour()
	
		# On Linux, SetFont apparently clears the text control's text string!
		if wxPlatform == "__WXGTK__":
			contents = self.body.GetValue()
			self.body.SetFont ( font )
			self.body.SetForegroundColour(color)
			self.body.SetValue(contents)
		else:
			self.body.SetFont ( font )
			self.body.SetForegroundColour(color)
	
		self.Refresh()
		return "break" # inhibit further command processing
	#@-body
	#@-node:9::OnFontPanel (set font)
	#@+node:10::OnSyntaxColoring (rewrite)
	#@+body
	def OnSyntaxColoring(self,event=None):
	
		self.notYet("Syntax Coloring")
		return "break" # inhibit further command processing
	#@-body
	#@-node:10::OnSyntaxColoring (rewrite)
	#@+node:11:C=24:OnViewAllCharacters
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
	#@-node:11:C=24:OnViewAllCharacters
	#@+node:12::OnPreferences
	#@+body
	def OnPreferences(self,event=None):
	
		frame = app().prefsFrame
		frame.top.deiconify()
		frame.top.lift()
		return "break" # inhibit further command processing
	#@-body
	#@-node:12::OnPreferences
	#@-node:1::Edit top level
	#@+node:2::Edit Body submenu
	#@+node:1::OnConvertBlanks
	#@+body
	def OnConvertBlanks(self,event=None):
	
		self.commands.convertBlanks()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnConvertBlanks
	#@+node:2::OnDedent
	#@+body
	def OnDedent (self,event=None):
	
		self.commands.dedentBody()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnDedent
	#@+node:3::OnExtract
	#@+body
	def OnExtract(self,event=None):
	
		self.commands.extract()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnExtract
	#@+node:4::OnExtractNames
	#@+body
	def OnExtractNames(self,event=None):
	
		self.commands.extractSectionNames()
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnExtractNames
	#@+node:5::OnExtractSection
	#@+body
	def OnExtractSection(self,event=None):
	
		self.commands.extractSection()
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnExtractSection
	#@+node:6::OnIndent
	#@+body
	def OnIndent(self,event=None):
	
		self.commands.indentBody()
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnIndent
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
	#@+node:1:C=25:OnMoveDownwn
	#@+body
	def OnMoveDown(self,event=None):
	
		self.commands.moveOutlineDown()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1:C=25:OnMoveDownwn
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
	#@+node:4::Window Menu (complete excet Recent Windows)
	#@+node:1::OnEqualSizedPanes
	#@+body
	def OnEqualSizedPanes(self,event=None):
	
		self.resizePanesToRatio(0.5)
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnEqualSizedPanes
	#@+node:2:C=26:OnToggleActivePane
	#@+body
	def OnToggleActivePane (self,event=None):
	
		# trace(`event`)
		if self.getFocus() == self.body:
			self.canvas.focus_force()
		else:
			self.body.focus_force()
		return "break" # inhibit further command processing
	#@-body
	#@-node:2:C=26:OnToggleActivePane
	#@+node:3::OnToggleSplitDirection
	#@+body
	def OnToggleSplitDirection(self,event=None):
	
		self.notYet("Toggle Split Direction")
		return "break" # inhibit further command processing
	
		self.splitVerticalFlag = not self.splitVerticalFlag
		self.resizePanesToRatio(0.5)
		self.body.focus_set()
		return "break" # inhibit further command processing
	#@-body
	#@-node:3::OnToggleSplitDirection
	#@+node:4::OnCascade
	#@+body
	def OnCascade(self,event=None):
	
		self.notYet("Cascade")
		return "break" # inhibit further command processing
	
		p = wxPoint(10,10)
		list = app().windowList
		for frame in list:
			frame.Move(p)
			p.x += 30
			p.y += 30
			if p.x > 200:
				p.x = 10
				p.y = 40
		return "break" # inhibit further command processing
	#@-body
	#@-node:4::OnCascade
	#@+node:5::OnMinimizeAll
	#@+body
	def OnMinimizeAll(self,event=None):
	
		self.minimize(app().prefsFrame)
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
	#@+node:6:C=27:OnOpenPythonWindow
	#@+body
	def OnOpenPythonWindow(self,event=None):
	
		try:
			if 0: # Python 2.2 warns that import * must be at the module level.
				from leoApp import *
				from leoGlobals import *
				from leoUtils import *
			import idle
			if app().idle_imported:
				reload(idle)
			app().idle_imported = true
		except:
			es("Can not import idle")
			es("Please add \Python2x\Tools\idle to sys.paths")
		return "break" # inhibit further command processing
	#@-body
	#@-node:6:C=27:OnOpenPythonWindow
	#@+node:7::OnRecentWindows (to do)
	#@+body
	def OnRecentWindows(self,event=None):
	
		self.notYet("Recent Windows")
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnRecentWindows (to do)
	#@-node:4::Window Menu (complete excet Recent Windows)
	#@+node:5::Help Menu
	#@+node:1:C=28:OnAbout (version number)
	#@+body
	def OnAbout(self,event=None):
	
		import tkMessageBox
	
		tkMessageBox.showinfo(
			"About Leo",
			"Leo in Python/Tk\n" +
			"Version 2.2, June 2, 2002\n\n" +
	
			"Copyright 1999-2002 by Edward K. Ream\n" +
			"All Rights Reserved\n" +
			"Leo is distributed under the Python License")
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:1:C=28:OnAbout (version number)
	#@+node:2::OnLeoDocumentation
	#@+body
	def OnLeoDocumentation (self,event=None):
	
		dir = app().loadDir
		fileName = os.path.join(dir, "LeoDocs.leo")
		try:
			self.OpenWithFileName(fileName)
		except:
			es("LeoDocs.leo not found")
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::OnLeoDocumentation
	#@-node:5::Help Menu
	#@-node:13:C=11:Menu Command Handlers
	#@+node:14::Splitter stuff
	#@+node:1::createSplitter
	#@+body
	# Create a splitter window and panes into which the caller packs widgets.
	# Returns (bar, pane1, pane2)
	
	# To do:
	#	height, width could be params
	#	constrain the minimum size of each pane
	
	def createSplitter (self, parent, verticalFlag):
	
		Tk = Tkinter
		f = Tk.Frame(parent,width="8i",height="6.5i",bd=0,bg="white",relief="flat")
		f.pack(expand=1,fill="both")
	
		pane1 = Tk.Frame(f)
		pane2 = Tk.Frame(f)
		pane1.configure(bd=0,bg="white",relief="flat")
		pane2.configure(bd=0,bg="white",relief="flat")
	
		if verticalFlag:
			# Panes arranged vertically; horizontal splitter bar
			bar = Tk.Frame(f,height=7,bd=2,relief="raised",bg="LightSteelBlue2",cursor="sb_v_double_arrow")
	
			pane1.place(relx=0.5, rely =   0, anchor="n", relwidth=1.0, relheight=0.5)
			pane2.place(relx=0.5, rely = 1.0, anchor="s", relwidth=1.0, relheight=0.5)
			bar.place  (relx=0.5, rely = 0.5, anchor="c", relwidth=1.0)
	
			bar.bind("<ButtonPress-1>",   self.onGrabVSplitBar)
			bar.bind("<B1-Motion>",	      self.onDragVSplitBar)
			bar.bind("<ButtonRelease-1>", self.onDropVSplitBar)
		else:
			# Panes arranged horizontally; vertical splitter bar
			bar = Tk.Frame(f,width=7,bd=2,relief="raised",bg="LightSteelBlue2",cursor="sb_h_double_arrow")
			
			f = 0.65 # give tree pane more room
			pane1.place(rely=0.5, relx =   0, anchor="w", relheight=1.0, relwidth=f)
			pane2.place(rely=0.5, relx = 1.0, anchor="e", relheight=1.0, relwidth=1.0-f)
			bar.place  (rely=0.5, relx = f, anchor="c", relheight=1.0)
		
			bar.bind("<ButtonPress-1>",		self.onGrabHSplitBar)
			bar.bind("<ButtonRelease-1>",	self.onDropHSplitBar)
			bar.bind("<B1-Motion>",			self.onDragHSplitBar)
	
		return bar, pane1, pane2
	#@-body
	#@-node:1::createSplitter
	#@+node:2::divideSplitter
	#@+body
	def divideSplitter (self, verticalFlag, frac):
	
		if verticalFlag:
			self.ratio = frac # Ratio of body pane to tree pane.
			# Panes arranged vertically; horizontal splitter bar
			self.bar1.place(rely=frac)
			self.split1Pane1.place(relheight=frac)
			self.split1Pane2.place(relheight=1-frac)
		else:
			# Panes arranged horizontally; vertical splitter bar
			self.bar2.place(relx=frac)
			self.split2Pane1.place(relwidth=frac)
			self.split2Pane2.place(relwidth=1-frac)
	#@-body
	#@-node:2::divideSplitter
	#@+node:3::onGrabSplitterBar, onGrabHSplitBar, onGrabVSplitVar
	#@+body
	def onGrabHSplitBar (self, event):
		self.onGrabSplitterBar(event, 0)
		
	def onGrabVSplitBar (self, event):
		self.onGrabSplitterBar(event, 1)
		
	def onGrabSplitterBar (self, event, verticalFlag):
		pass
	#@-body
	#@-node:3::onGrabSplitterBar, onGrabHSplitBar, onGrabVSplitVar
	#@+node:4::onDragSplitterBar, onDragHSplitBar, onDragVSplitBar
	#@+body
	def onDragHSplitBar (self, event):
		self.onDragSplitterBar(event, 0)
		
	def onDragVSplitBar (self, event):
		self.onDragSplitterBar(event, 1)
	
	def onDragSplitterBar (self, event, verticalFlag):
	
		if not self.splitVerticalFlag:
			return ## disable for now...
	
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
		self.divideSplitter(verticalFlag, frac)
	#@-body
	#@-node:4::onDragSplitterBar, onDragHSplitBar, onDragVSplitBar
	#@+node:5::onDropSplitterBar, onDropHSplitBar, onDropVSplitBar
	#@+body
	def onDropHSplitBar (self, event):
		self.onDropSplitterBar(event, 0)
		
	def onDropVSplitBar (self, event):
		self.onDropSplitterBar(event, 1)
		
	# We could call divideSplitter here (instead of On DragSplitterBar) for non-dynamic updates.
	def onDropSplitterBar (self, event, verticalFlag):
		pass
	#@-body
	#@-node:5::onDropSplitterBar, onDropHSplitBar, onDropVSplitBar
	#@-node:14::Splitter stuff
	#@-others
#@-body
#@-node:0::@file leoFrame.py
#@-leo
