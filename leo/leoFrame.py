#@+leo
#@+node:0::@file leoFrame.py
#@+body
# To do: Use config params for window height, width and bar color, relief and width.


#@@language python 

from leoGlobals import *
from leoUtils import *
import leoColor, leoCompare, leoDialog, leoFontPanel, leoNodes, leoPrefs
import os,string,sys,traceback,Tkinter,tkFileDialog,tkFont

# Needed for menu commands
import leoCommands, leoNodes, leoTree
import os, sys, traceback

class LeoFrame:

	#@+others
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
		self.editBodyMenu = self.editHeadlineMenu = self.moveSelectMenu = self.markGotoMenu = None
		self.menuShortcuts = None # List of menu shortcuts for warnings.
		
		# Used by event handlers...
		self.redrawCount = 0
		self.activeFrame = None
		self.draggedItem = None
		self.recentFiles = [] # List of recent files
		#@-body
		#@-node:1::<< set the LeoFrame ivars >>

		self.top = top = Tk.Toplevel()
		top.withdraw() # 7/15/02
		# print `top`
		
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
		app().log = self # the LeoFrame containing the log
		app().windowList.append(self)
		# Sign on.
		es("Leo Log Window...")
		n1,n2,n3,junk,junk=sys.version_info
		ver1 = "Python %d.%d.%d" % (n1,n2,n3)
		ver2 = ", Tk " + self.top.getvar("tk_patchLevel")
		es(ver1 + ver2) ; enl()
	
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
		if sys.platform == "linux2": # This crashes tcl83.dll
			self.tree.canvas.bind("<MouseWheel>", self.OnMouseWheel)
	#@-body
	#@-node:1::frame.__init__
	#@+node:2::frame.__del__
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
		self.editBodyMenu = self.editHeadlineMenu = self.moveSelectMenu = self.markGotoMenu = None
	#@-body
	#@-node:2::frame.__del__
	#@+node:3::frame.__repr__
	#@+body
	def __repr__ (self):
	
		return "leoFrame: " + self.title
	
	#@-body
	#@-node:3::frame.__repr__
	#@+node:4::frame.destroy
	#@+body
	def destroy (self):
	
		# don't trace during shutdown logic.
		# print "frame.destroy:", `self`, `self.top`
		self.tree.destroy()
		self.tree = None
		self.commands.destroy()
		self.commands = None
		self.top.destroy() # Actually close the window.
		self.top = None
	#@-body
	#@-node:4::frame.destroy
	#@+node:5::f.setTabWidth
	#@+body
	def setTabWidth (self, w):
		
		try: # 8/11/02: This can fail when called from scripts.
			# 9/20/22: Use the present font for computations.
			font = self.body.cget("font")
			font = font = tkFont.Font(font=font)
			tabw = font.measure(" " * abs(w)) # 7/2/02
			# print "frame.setTabWidth:" + `w` + "," + `tabw`
			self.body.configure(tabs=tabw)
		except:
			# es_exception()
			pass
	
	#@-body
	#@-node:5::f.setTabWidth
	#@+node:6::canonicalizeShortcut
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

	def canonicalizeShortcut (self, shortcut):
		
		if shortcut == None or len(shortcut) == 0:
			return None,None
		s = string.strip(shortcut)
		s = string.lower(s)
		has_alt = string.find(s,"alt") >= 0
		has_ctrl = string.find(s,"control") >= 0 or string.find(s,"ctrl") >= 0
		has_shift = string.find(s,"shift") >= 0 or string.find(s,"shft") >= 0
		
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
			if ch in string.ascii_letters:
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
			if len(last) > 1 or (len(last)==1 and last[0] not in string.ascii_letters):
				bind_head = "Shift-"
		
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

		# print `shortcut`,`bind_shortcut`,`menu_shortcut`
		return bind_shortcut,menu_shortcut
	#@-body
	#@-node:6::canonicalizeShortcut
	#@+node:7::createMenuBar
	#@+body
	def createMenuBar(self, top):
	
		c = self.commands
		Tk = Tkinter
		self.topMenu = menu = Tk.Menu(top,postcommand=self.OnMenuClick)
		self.menuShortcuts = []
	
		# To do: use Meta rathter than Control for accelerators for Unix
		
		#@<< create the file menu >>
		#@+node:2::<< create the file menu >>
		#@+body
		self.fileMenu = fileMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="File",menu=fileMenu)
		
		
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
			("New","Ctrl+N",self.OnNew),
			("Open...","Ctrl+O",self.OnOpen),
			("Open With...","Shift+Ctrl+O",self.OnOpenWith),
			("-",None,None),
			("Close","Ctrl+W",self.OnClose),
			("Save","Ctrl+S",self.OnSave),
			("Save As","Shift+Ctrl+S",self.OnSaveAs),
			("Save To",None,self.OnSaveTo),
			("Revert To Saved",None,self.OnRevert))
				
		self.createMenuEntries(fileMenu,table)
		#@-body
		#@-node:1::<< create the top-level file entries >>

		
		#@<< create the recent files submenu >>
		#@+node:2::<< create the recent files submenu >>
		#@+body
		recentFilesMenu = self.recentFilesMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Recent Files...", menu=recentFilesMenu)
		
		self.recentFiles = app().config.getRecentFiles()
		
		for i in xrange(len(self.recentFiles)):
			name = self.recentFiles[i]
			# 9/15/02: Added self=self to remove Python 2.1 warning.
			callback = lambda n=i,self=self: self.OnOpenRecentFile(n)
			recentFilesMenu.add_command(label=name,command=callback)
		
		#@-body
		#@-node:2::<< create the recent files submenu >>

		fileMenu.add_separator()
		
		#@<< create the read/write submenu >>
		#@+node:3::<< create the read/write submenu >>
		#@+body
		readWriteMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Read/Write...", menu=readWriteMenu)
		
		table = (
			("Read Outline Only","Shift+Ctrl+R",self.OnReadOutlineOnly),
			("Read @file Nodes",None,self.OnReadAtFileNodes),
			("Write Outline Only",None,self.OnWriteOutlineOnly),
			("Write @file Nodes","Shift+Ctrl+W",self.OnWriteAtFileNodes))
		
		self.createMenuEntries(readWriteMenu,table)
		
		#@-body
		#@-node:3::<< create the read/write submenu >>

		
		#@<< create the tangle submenu >>
		#@+node:4::<< create the tangle submenu >>
		#@+body
		tangleMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Tangle...", menu=tangleMenu)
		
		table = (
			("Tangle All","Shift+Ctrl+A",self.OnTangleAll),
			("Tangle Marked","Shift+Ctrl+M",self.OnTangleMarked),
			("Tangle","Shift+Ctrl+T",self.OnTangle))
		
		self.createMenuEntries(tangleMenu,table)
		
		#@-body
		#@-node:4::<< create the tangle submenu >>

		
		#@<< create the untangle submenu >>
		#@+node:5::<< create the untangle submenu >>
		#@+body
		untangleMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Untangle...", menu=untangleMenu)
		
		table = (
			("Untangle All",None,self.OnUntangleAll),
			("Untangle Marked",None,self.OnUntangleMarked),
			("Untangle","Shift+Ctrl+U",self.OnUntangle))
			
		self.createMenuEntries(untangleMenu,table)
		
		#@-body
		#@-node:5::<< create the untangle submenu >>

		
		#@<< create the import submenu >>
		#@+node:6::<< create the import submenu >>
		#@+body
		importMenu = Tk.Menu(fileMenu,tearoff=0)
		fileMenu.add_cascade(label="Import/Export...", menu=importMenu)
		
		table = (
			("Import To @file","Shift+Ctrl+F",self.OnImportAtFile),
			("Import To @root",None,self.OnImportAtRoot),
			("Import CWEB Files",None,self.OnImportCWEBFiles),
			("Import noweb Files",None,self.OnImportNowebFiles),
			("Import Flattened Outline",None,self.OnImportFlattenedOutline),
			("-",None,None),
			("Outline To CWEB",None,self.OnOutlineToCWEB),
			("Outline To Noweb",None,self.OnOutlineToNoweb),
			("Flatten Outline",None,self.OnFlattenOutline),
			("Remove Sentinels",None,self.OnRemoveSentinels),
			("Weave",None,self.OnWeave))
		
		self.createMenuEntries(importMenu,table)
		
		#@-body
		#@-node:6::<< create the import submenu >>

		fileMenu.add_separator()
		# Create the last entries.
		exitTable = (("Exit","Ctrl-Q",self.OnQuit),)
		self.createMenuEntries(fileMenu,exitTable)
		
		#@-body
		#@-node:2::<< create the file menu >>

		
		#@<< create the edit menu >>
		#@+node:1::<< create the edit menu >>
		#@+body
		self.editMenu = editMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Edit", menu=editMenu)
		
		
		#@<< create the first top-level edit entries >>
		#@+node:1::<< create the first top-level edit entries >>
		#@+body
		table = (
			("Can't Undo","Ctrl+Z",self.OnUndo),
			("Can't Redo","Shift+Ctrl+Z",self.OnRedo),
			("-",None,None),
			("Cut","Ctrl+X",self.OnCutFromMenu),
			("Copy","Ctrl+C",self.OnCopyFromMenu),
			("Paste","Ctrl+V",self.OnPasteFromMenu),
			("Delete",None,self.OnDelete),
			("Select All","Ctrl+A",self.OnSelectAll),
			("-",None,None))
		
		self.createMenuEntries(editMenu,table)
		
		#@-body
		#@-node:1::<< create the first top-level edit entries >>

		
		#@<< create the edit body submenu >>
		#@+node:2::<< create the edit body submenu >>
		#@+body
		self.editBodyMenu = editBodyMenu = Tk.Menu(editMenu,tearoff=0)
		editMenu.add_cascade(label="Edit Body...", menu=editBodyMenu)
		
		# DTHEIN 27-OCT-2002: added reformat paragraph
		table = (
			("Extract Section","Shift+Ctrl+E",self.OnExtractSection),
			("Extract Names","Shift+Ctrl+N",self.OnExtractNames),
			("Extract","Shift+Ctrl+D",self.OnExtract),
			("-",None,None),
			("Convert All Blanks",None,self.OnConvertAllBlanks),
			("Convert All Tabs",None,self.OnConvertAllTabs),
			("Convert Blanks","Shift+Ctrl+B",self.OnConvertBlanks),
			("Convert Tabs","Shift+Ctrl+J",self.OnConvertTabs),
			("Reformat Paragraph","Shift+Ctrl+P",self.OnReformatParagraph),
			("-",None,None),
			("Indent","Ctrl+]",self.OnIndent),
			("Unindent","Ctrl+[",self.OnDedent),
			("Match Brackets","Ctrl+K",self.OnFindMatchingBracket))
			#("-",None,None),
			#("Insert Graphic File...",None,self.OnInsertGraphicFile))
			
		self.createMenuEntries(editBodyMenu,table)
		
		#@-body
		#@-node:2::<< create the edit body submenu >>

		
		#@<< create the edit headline submenu >>
		#@+node:3::<< create the edit headline submenu >>
		#@+body
		self.editHeadlineMenu = editHeadlineMenu = Tk.Menu(editMenu,tearoff=0)
		editMenu.add_cascade(label="Edit Headline...", menu=editHeadlineMenu)
		
		table = (
			("Edit Headline","Ctrl+H",self.OnEditHeadline),
			("End Edit Headline","Escape",self.OnEndEditHeadline),
			("Abort Edit Headline","Shift-Escape",self.OnAbortEditHeadline))
			
		self.createMenuEntries(editHeadlineMenu,table)
		
		#@-body
		#@-node:3::<< create the edit headline submenu >>

		
		#@<< create the find submenu >>
		#@+node:4::<< create the find submenu >>
		#@+body
		findMenu = Tk.Menu(editMenu,tearoff=0)
		editMenu.add_cascade(label="Find...", menu=findMenu)
		
		#It is no longer possible to specify two shortcuts for exactly the same command name.
		#("Find Next","Ctrl+G",self.OnFindNext),
		
		table = (
			("Find Panel","Ctrl+F",self.OnFindPanel),
			("-",None,None),
			("Find Next","F3",self.OnFindNext),
			("Find Previous","F4",self.OnFindPrevious),
			("Replace","Ctrl+=",self.OnReplace),
			("Replace, Then Find","Ctrl+-",self.OnReplaceThenFind))
		
		self.createMenuEntries(findMenu,table)
		
		#@-body
		#@-node:4::<< create the find submenu >>

		
		#@<< create the last top-level edit entries >>
		#@+node:5::<< create the last top-level edit entries >>
		#@+body
		label = choose(c.tree.colorizer.showInvisibles,"Hide Invisibles","Show Invisibles")
			
		table = (
			("Execute Script","Alt+E",self.OnExecuteScript),
			("Set Font...","Shift+Alt+T",self.OnFontPanel),
			("Set Colors...","Shift+Alt+S",self.OnColorPanel),
			(label,"Alt+V",self.OnViewAllCharacters),
			("-",None,None),
			("Preferences","Ctrl+Y",self.OnPreferences))
		
		self.createMenuEntries(editMenu,table)
		
		#@-body
		#@-node:5::<< create the last top-level edit entries >>
		#@-body
		#@-node:1::<< create the edit menu >>

		
		#@<< create the outline menu >>
		#@+node:3::<< create the outline menu >>
		#@+body
		self.outlineMenu = outlineMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Outline", menu=outlineMenu)
		
		
		#@<< create top-level outline menu >>
		#@+node:1::<< create top-level outline menu >>
		#@+body
		table = (
			("Cut Node","Shift+Ctrl+X",self.OnCutNode),
			("Copy Node","Shift+Ctrl+C",self.OnCopyNode),
			("Paste Node","Shift+Ctrl+V",self.OnPasteNode),
			("Delete Node","Shift+Ctrl+BkSp",self.OnDeleteNode),
			("-",None,None),
			("Insert Node","Ctrl+I",self.OnInsertNode),
			("Clone Node","Ctrl+`",self.OnCloneNode),
			("Sort Children",None,self.OnSortChildren),
			("Sort Siblings","Alt-A",self.OnSortSiblings),
			("-",None,None))
		
		self.createMenuEntries(outlineMenu,table)
		#@-body
		#@-node:1::<< create top-level outline menu >>

		
		#@<< create expand/contract submenu >>
		#@+node:2::<< create expand/contract submenu >>
		#@+body
		self.expandContractMenu = expandContractMenu = Tk.Menu(outlineMenu,tearoff=0)
		outlineMenu.add_cascade(label="Expand/Contract...", menu=expandContractMenu)
		
		table = (
			("Expand All","Alt+9",self.OnExpandAll),
			("Expand All Children",None,self.OnExpandAllChildren),
			("Expand Children",None,self.OnExpandChildren),
			("-",None,None),
			("Contract Parent","Alt+0",self.OnContractParent),
			("Contract All","Alt+1",self.OnContractAll),
			("Contract All Children",None,self.OnContractAllChildren),
			("Contract Children",None,self.OnContractChildren),
			("-",None,None),
			("Expand Next Level","Alt+=",self.OnExpandNextLevel),
			("Expand To Level 1",None,self.OnExpandToLevel1),
			("Expand To Level 2","Alt+2",self.OnExpandToLevel2),
			("Expand To Level 3","Alt+3",self.OnExpandToLevel3),
			("Expand To Level 4","Alt+4",self.OnExpandToLevel4),
			("Expand To Level 5","Alt+5",self.OnExpandToLevel5),
			("Expand To Level 6","Alt+6",self.OnExpandToLevel6),
			("Expand To Level 7","Alt+7",self.OnExpandToLevel7),
			("Expand To Level 8","Alt+8",self.OnExpandToLevel8))
		
		self.createMenuEntries(expandContractMenu,table)
		#@-body
		#@-node:2::<< create expand/contract submenu >>

		
		#@<< create move/select submenu >>
		#@+node:3::<< create move/select submenu >>
		#@+body
		self.moveSelectMenu = moveSelectMenu = Tk.Menu(outlineMenu,tearoff=0)
		outlineMenu.add_cascade(label="Move/Select...", menu=moveSelectMenu)
		
		table = (
			("Move Down", "Ctrl+D",self.OnMoveDown),
			("Move Left", "Ctrl+L",self.OnMoveLeft),
			("Move Right","Ctrl+R",self.OnMoveRight),
			("Move Up",   "Ctrl+U",self.OnMoveUp),
			("-",None,None),
			("Promote","Ctrl+{",self.OnPromote),
			("Demote", "Ctrl+}",self.OnDemote),
			("-",None,None),
			("Go Prev Visible","Alt-UpArrow",self.OnGoPrevVisible),
			("Go Next Visible","Alt-DnArrow",self.OnGoNextVisible),
			("-",None,None),
			("Go Back","Alt-Shift+UpArrow",self.OnGoBack),
			("Go Next","Alt-Shift-DnArrow",self.OnGoNext))
			
		self.createMenuEntries(moveSelectMenu,table)
		
		#@-body
		#@-node:3::<< create move/select submenu >>

		
		#@<< create mark/goto submenu >>
		#@+node:4::<< create mark/goto submenu >>
		#@+body
		self.markGotoMenu = markGotoMenu = Tk.Menu(outlineMenu,tearoff=0)
		outlineMenu.add_cascade(label="Mark/Go To...", menu=markGotoMenu)
		
		table = (
			("Mark","Ctrl-M",self.OnMark),
			("Mark Subheads","Alt+S",self.OnMarkSubheads),
			("Mark Changed Items","Alt+C",self.OnMarkChangedItems),
			("Mark Changed Roots","Alt+R",self.OnMarkChangedRoots),
			("-",None,None),
			("Unmark All","Alt+U",self.OnUnmarkAll),
			("Go To Next Marked","Alt+M",self.OnGoToNextMarked),
			("Go To Next Changed","Alt+D",self.OnGoToNextChanged))
			
		self.createMenuEntries(markGotoMenu,table)
		
		#@-body
		#@-node:4::<< create mark/goto submenu >>
		#@-body
		#@-node:3::<< create the outline menu >>

		
		#@<< create the window menu >>
		#@+node:4::<< create the window menu >>
		#@+body
		self.windowMenu = windowMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Window", menu=windowMenu)
		
		table = (
			("Equal Sized Panes","Ctrl-E",self.OnEqualSizedPanes),
			("Toggle Active Pane","Ctrl-T",self.OnToggleActivePane),
			("Toggle Split Direction",None,self.OnToggleSplitDirection),
			("-",None,None),
			("Cascade",None,self.OnCascade),
			("Minimize All",None,self.OnMinimizeAll),
			("-",None,None),
			("Open Compare Window",None,self.OnOpenCompareWindow),
			("Open Python Window","Alt+P",self.OnOpenPythonWindow))
		
		self.createMenuEntries(windowMenu,table)
		
		#@-body
		#@-node:4::<< create the window menu >>

		
		#@<< create the help menu >>
		#@+node:5::<< create the help menu >>
		#@+body
		self.helpMenu = helpMenu = Tk.Menu(menu,tearoff=0)
		menu.add_cascade(label="Help", menu=helpMenu)
		
		table = (
			("About Leo...",None,self.OnAbout),
			("Online Home Page",None,self.OnLeoHome),
			("-",None,None),
			("Open Online Tutorial",None,self.OnLeoTutorial))
		self.createMenuEntries(helpMenu,table)
		
		if sys.platform=="win32":
			table = (("Open Offline Tutorial",None,self.OnLeoHelp),)
			self.createMenuEntries(helpMenu,table)
		
		table = (
			("Open LeoDocs.leo",None,self.OnLeoDocumentation),
			("-",None,None),
			("Open LeoConfig.leo",None,self.OnLeoConfig),
			("Apply Settings",None,self.OnApplyConfig))
		self.createMenuEntries(helpMenu,table)
		#@-body
		#@-node:5::<< create the help menu >>

		top.config(menu=menu) # Display the menu.
		app().menuWarningsGiven = true
	#@-body
	#@-node:7::createMenuBar
	#@+node:8::createMenuEntries
	#@+body
	#@+at
	#  The old, non-user-configurable code bound shortcuts in createMenuBar.  
	# The new user-configurable code binds shortcuts here.
	# 
	# Centralized tables of shortscuts no longer exist as they did in 
	# createAccelerators.  To check for duplicates, (possibly arising from 
	# leoConfig.txt) we add entries to a central dictionary here, and report 
	# duplicates if an entry for a cononicalized shortcut already exists.

	#@-at
	#@@c

	def createMenuEntries (self,menu,table):
		
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
					if ch in string.ascii_letters or ch in string.digits:
						name2 = name2 + ch
				name = name2
				
				config = app().config
				accel2 = config.getShortcut(name)
				if accel2 and len(accel2) > 0:
					accel = accel2
					# print `name`,`accel`
				else:
					pass
					# print "no default:",`name`
				
				bind_shortcut,menu_shortcut = self.canonicalizeShortcut(accel)
				
				# Kludge: disable the shortcuts for cut, copy, paste.
				# This has already been bound in leoFrame.__init__
				if bind_shortcut in ("<Control-c>","<Control-v>","<Control-x>"):
					bind_shortcut = None
				#@-body
				#@-node:1::<< get menu and bind shortcuts >>

				if menu_shortcut:
					menu.add_command(label=label,accelerator=menu_shortcut,command=command)
				else:
					menu.add_command(label=label,command=command)
					
				if bind_shortcut:
					if bind_shortcut in self.menuShortcuts:
						if not app().menuWarningsGiven:
							print "duplicate shortcut:", accel, `bind_shortcut`, label
					else:
						self.menuShortcuts.append(bind_shortcut)
						try:
							if 0: # This may cause problems when multiple Leo windows are present.
								self.top.bind_all(bind_shortcut,command)
								# This should work, and doesn't.
								# self.body.bind_class(bind_shortcut,command) # For headlines created later.
							else: # This seems safer.
								self.body.bind(bind_shortcut,command) # Necessary to override defaults in body.
								self.top.bind (bind_shortcut,command)
						except: # could be a user error
							if not app().menuWarningsGiven:
								print "exception binding menu shortcut..."
								print `bind_shortcut`
								# es_exception()
	#@-body
	#@-node:8::createMenuEntries
	#@+node:9::initialRatios
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
	#@-node:9::initialRatios
	#@+node:10::getFocus
	#@+body
	# Returns the frame that has focus, or body if None.
	
	def getFocus(self):
	
		f = self.top.focus_displayof()
		if f:
			return f
		else:
			return self.body
	#@-body
	#@-node:10::getFocus
	#@+node:11::notYet
	#@+body
	def notYet(self,name):
	
		es(name + " not ready yet")
	
	#@-body
	#@-node:11::notYet
	#@+node:12::frame.put, putnl
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
	#@-node:12::frame.put, putnl
	#@+node:13::resizePanesToRatio
	#@+body
	def resizePanesToRatio(self,ratio,secondary_ratio):
	
		self.divideLeoSplitter(self.splitVerticalFlag, ratio)
		self.divideLeoSplitter(not self.splitVerticalFlag, secondary_ratio)
		# trace(`ratio`)
	
	#@-body
	#@-node:13::resizePanesToRatio
	#@+node:14::Event handlers
	#@+node:1::frame.OnCloseLeoEvent
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
	#@-node:1::frame.OnCloseLeoEvent
	#@+node:2::OnActivateBody & OnBodyDoubleClick
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
	#@-node:2::OnActivateBody & OnBodyDoubleClick
	#@+node:3::OnActivateLeoEvent
	#@+body
	def OnActivateLeoEvent(self,event=None):
	
		c = self.commands
		app().log = self
	
	#@-body
	#@-node:3::OnActivateLeoEvent
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
	#@+node:6::OnMouseWheel (Tomaz Ficko)
	#@+body
	# Contributed by Tomaz Ficko.  This works on some systems.
	# On XP it causes a crash in tcl83.dll.  Clearly a Tk bug.
	
	def OnMouseWheel(self, event=None):
	
		if event.delta < 1:
			self.canvas.yview(Tkinter.SCROLL, 1, Tkinter.UNITS)
		else:
			self.canvas.yview(Tkinter.SCROLL, -1, Tkinter.UNITS)
	#@-body
	#@-node:6::OnMouseWheel (Tomaz Ficko)
	#@-node:14::Event handlers
	#@+node:15::Menu enablers (Frame)
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
	
		c = self.commands
		if not c: return
		v = c.currentVnode()
		
		menu = self.fileMenu
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
		enableMenu(menu,"Match Brackets",c.canFindMatchingBracket())
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
	#@-node:15::Menu enablers (Frame)
	#@+node:16::Menu Command Handlers
	#@+node:1::File Menu
	#@+node:1::top level
	#@+node:1::OnNew
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
		return "break" # inhibit further command processing
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
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:2::frame.OnOpen
	#@+node:3::frame.OnOpenWith
	#@+body
	#@+at
	#  To do:
	# 
	# 1. handle @path and default tangle directory similar to scanAllDirectives.
	# 2. Use leoConfig.txt to determine which editor to open for various file types.
	# 	Figure out how config module can create list of association.

	#@-at
	#@@c

	def OnOpenWith(self,event=None):
		
		a = app() ; c = self.commands ; v = c.currentVnode()
		
		
		#@<< set ext based on the present language >>
		#@+node:1::<< set ext based on the present language >>
		#@+body
		ext = language_extension_dict.get(c.target_language)
		if ext == None: ext = "txt"
		ext = "." + ext
		# trace(c.target_language + "," + ext)
		#@-body
		#@-node:1::<< set ext based on the present language >>

		
		#@<< open a temp file f with extension ext >>
		#@+node:2::<< open a temp file f with extension ext >>
		#@+body
		f = None
		while f == None:
		
			a.openWithFileNum += 1
			name = "LeoTemp" + str(a.openWithFileNum) + ext
			path = os.path.join(a.loadDir,name)
			
			if not os.path.exists(path):
				try:
					f = open(path,"w")
					es("creating: " + path)
					data = (f,path)
					a.openWithFiles.append(data)
				except:
					f = None
					es("exception opening temp file")
					es_exception()
		
		#@-body
		#@-node:2::<< open a temp file f with extension ext >>

		if f:
			f.write(v.bodyString())
			f.flush()
			f.close()
		
		#@<< open f in the external editor >>
		#@+node:3::<< open f in the external editor >>
		#@+body
		try:
			os.startfile("c:/python22/tools/idle/idle.py " + path)
		except:
			es("exception opening " + path)
			es_exception()
		
		#@-body
		#@-node:3::<< open f in the external editor >>

		
		if 0: # old code
			isAtFile = v.isAtFileNode()
			if not isAtFile: return  "break"
			
			name = v.atFileNodeName()
			if name == None or len(name) == 0: return  "break"
			
			## To do: 
			name = string.strip(name)
			f = os.path.join(app().loadDir,name)
			print f
		
			# This doesn't work for .py files or .bat files.
			# Probably not too swift for other files either.
			if 0:
				os.startfile(f)
				
		return "break" # inhibit further command processing
	
	#@-body
	#@-node:3::frame.OnOpenWith
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
				#@+node:1::<< make fileName the most recent file of frame >>
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
						# 9/15/02: Added self=self to remove Python 2.1 warning.
						callback = lambda n=i,self=self: self.OnOpenRecentFile(n)
						frame.recentFilesMenu.add_command(label=name,command=callback)
						i += 1
					
				# Update the config file.
				app().config.setRecentFiles(frame.recentFiles)
				app().config.update()
				#@-body
				#@-node:1::<< make fileName the most recent file of frame >>

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
		
		self.OnCloseLeoEvent() # Destroy the frame unless the user cancels.
		return "break" # inhibit further command processing
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
			self.top.title(self.mFileName)
			self.commands.fileCommands.saveAs(self.mFileName)
	
		return "break" # inhibit further command processing
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnSaveTo
	#@+node:9::OnRevert
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:10::frame.OnQuit
	#@-node:1::top level
	#@+node:2::Recent Files submenu
	#@+node:1::OnOpenFileN
	#@+body
	def OnOpenRecentFile(self,n):
		
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

		if n < len(self.recentFiles):
			fileName = self.recentFiles[n]
			ok, frame = self.OpenWithFileName(fileName)
			if ok and closeFlag:
				app().windowList.remove(self)
				self.destroy() # force the window to go away now.
				app().log = frame # Sets the log stream for es()
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnOpenFileN
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
	#@+node:10::OnWeave
	#@+body
	def OnWeave (self,event=None):
		
		filetypes = [("Text files", "*.txt"),("All files", "*")]
	
		fileName = tkFileDialog.asksaveasfilename(
			title="Weave",filetypes=filetypes,
			initialfile="weave.txt",defaultextension=".txt")
	
		if fileName and len(fileName) > 0:
			c = self.commands
			c.importCommands.weave(fileName)
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:10::OnWeave
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
	#@+node:3::frame.OnCut, OnCutFrom Menu
	#@+body
	def OnCut (self,event=None):
	
		# Activate the body key handler by hand.
		c = self.commands ; v = c.currentVnode()
		self.commands.tree.onBodyWillChange(v,"Cut")
		return # Allow the actual cut!
	
	def OnCutFromMenu (self,event=None):
	
		w = self.getFocus()
		w.event_generate(virtual_event_name("Cut"))
		
		# 11/2/02: Make sure the event sticks.
		c = self.commands ; v = c.currentVnode()
		c.tree.onHeadChanged(v) # Works even if it wasn't the headline that changed.
		return "break"
	#@-body
	#@-node:3::frame.OnCut, OnCutFrom Menu
	#@+node:4::frame.OnCopy, OnCopyFromMenu
	#@+body
	def OnCopy (self,event=None):
	
		# Copy never changes dirty bits or syntax coloring.
		return # Allow the actual copy!
		
	def OnCopyFromMenu (self,event=None):
	
		# trace()
		w = self.getFocus()
		w.event_generate(virtual_event_name("Copy"))
		return "break"
	#@-body
	#@-node:4::frame.OnCopy, OnCopyFromMenu
	#@+node:5::frame.OnPaste, OnPasteNode, OnPasteFromMenu
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:6::OnDelete
	#@+node:7::OnExecuteScript
	#@+body
	#@+at
	#  This executes body text as a Python script.  We execute the selected 
	# text, or the entire presently selected body text if no text is selected 
	# and the node's headline starts with @pythonscript.

	#@-at
	#@@c

	def OnExecuteScript(self,event=None):
		
		c = self.commands ; body = self.body
		v = c.currentVnode() ; s = None
		
		# Assume any selected body text is a script.
		if self.getFocus() == body:
			start,end = getTextSelection(body)
			if start and end:
				s = body.get(start,end)
				s = s.strip()
				
		# Otherwise, the script is v's body text if v is an @pythonscript node.
		if s == None or len(s) == 0:
			h = v.headString()
			if match_word(h,0,"@pythonscript"):
				s = v.bodyString()
				
		#trace(`s`)
		if s and len(s) > 0:
			try:
				exec(s,globals(),locals())
			except:
				es_exception(full=true)
		else:
			es("no script selected")
	
		return "break" # inhibit further command processing
	#@-body
	#@-node:7::OnExecuteScript
	#@+node:8::OnSelectAll
	#@+body
	def OnSelectAll(self,event=None):
	
		setTextSelection(self.body,"1.0","end")
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnSelectAll
	#@+node:9::OnFontPanel
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
	#@-node:9::OnFontPanel
	#@+node:10::OnColorPanel
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
	#@-node:10::OnColorPanel
	#@+node:11::OnViewAllCharacters
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
	#@-node:11::OnViewAllCharacters
	#@+node:12::OnPreferences
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
	#@-node:12::OnPreferences
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
		
	#DTHEIN 27-OCT-2002
	def OnReformatParagraph(self,event=None):
		
		self.commands.reformatParagraph()
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
			return "break"
		
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
		
		return "break"
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
		return "break" # inhibit further command processing
	#@-body
	#@-node:8::OnIndent
	#@+node:9::OnInsertGraphicFile
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
				es_exception()
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
	#@-node:9::OnInsertGraphicFile
	#@-node:2::Edit Body submenu
	#@+node:3::Edit Headline submenu
	#@+node:1::OnEditHeadline
	#@+body
	def OnEditHeadline(self,event=None):
	
		tree = self.commands.tree
		tree.editLabel(tree.currentVnode)
		
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnEditHeadline
	#@+node:2::OnEndEditHeadline
	#@+body
	def OnEndEditHeadline(self,event=None):
		
		tree = self.commands.tree
		tree.endEditLabelCommand()
	
		return "break"
	#@-body
	#@-node:2::OnEndEditHeadline
	#@+node:3::OnAbortEditHeadline
	#@+body
	def OnAbortEditHeadline(self,event=None):
		
		tree = self.commands.tree
		tree.abortEditLabelCommand()
		
		return "break"
	#@-body
	#@-node:3::OnAbortEditHeadline
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
	#@-node:4::Find submenu (frame methods)
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
	#@+node:1::OnMoveDownwn
	#@+body
	def OnMoveDown(self,event=None):
	
		self.commands.moveOutlineDown()
		return "break" # inhibit further command processing
	#@-body
	#@-node:1::OnMoveDownwn
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
	
		frame = self
		frame.resizePanesToRatio(0.5,frame.secondary_ratio)
	
		return "break" # inhibit further command processing
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
		return "break" # inhibit further command processing
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
		return "break" # inhibit further command processing
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
	#@-node:4::OnCascade
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
	#@+node:6::OnHideLogWindow
	#@+body
	def OnHideLogWindow (self):
		
		c = self.commands ; frame = c.frame
	
		frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)
	#@-body
	#@-node:6::OnHideLogWindow
	#@+node:7::OnOpenCompareWindow
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

	
		return "break" # inhibit further command processing.
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
		version = "leo.py 3.8, Build " + build + ", October 29, 2002\n\n"
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
	#@-node:1::OnAbout (version number & date)
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
					es_exception()
	
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
	#@+node:5::OnLeoTutorial (version number)
	#@+body
	def OnLeoTutorial (self,event=None):
		
		import webbrowser
	
		url = "http://www.evisa.com/e/sbooks/leo/sbframetoc_ie.htm"
		try:
			webbrowser.open(url)
		except:
			es("not found: " + url)
		
		return "break" # inhibit further command processing
	#@-body
	#@-node:5::OnLeoTutorial (version number)
	#@+node:6::OnLeoConfig, OnApplyConfig
	#@+body
	def OnLeoConfig (self,event=None):
	
		dir = app().loadDir
		fileName = os.path.join(dir, "leoConfig.leo")
		try:
			self.OpenWithFileName(fileName)
		except:
			es("not found: leoConfig.leo")
	
		return "break" # inhibit further command processing
		
	def OnApplyConfig (self,event=None):
	
		app().config.init()
		self.commands.frame.reconfigureFromConfig()
	#@-body
	#@-node:6::OnLeoConfig, OnApplyConfig
	#@-node:5::Help Menu
	#@-node:16::Menu Command Handlers
	#@+node:17::Configuration
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
		#print "body",`self.body`
		
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
			
		if sys.platform != "win32": # Maybe a Windows bug.
			fg = config.getWindowPref("body_cursor_foreground_color")
			bg = config.getWindowPref("body_cursor_background_color")
			# print `fg`, `bg`
			if fg and bg:
				cursor="xterm" + " " + fg + " " + bg
				try: body.configure(cursor=cursor)
				except:
					traceback.print_exc()
	#@-body
	#@-node:4::f.setBodyFontFromConfig
	#@+node:5::f.setLogFontFromConfig
	#@+body
	def setLogFontFromConfig (self):
	
		log = self.log ; config = app().config
		#print "log",`self.log`
	
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
	#@+node:6::f.setTreeColorsFromConfig
	#@+body
	def setTreeColorsFromConfig (self):
		
		config = app().config ; tree = self.tree
	
		bg = config.getWindowPref("outline_pane_background_color")
		if bg:
			try: self.canvas.configure(bg=bg)
			except: pass
	
	#@-body
	#@-node:6::f.setTreeColorsFromConfig
	#@+node:7::reconfigurePanes (use config bar_width)
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
	#@-node:7::reconfigurePanes (use config bar_width)
	#@-node:17::Configuration
	#@+node:18::Splitter stuff
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
	#@+node:1::bindBar
	#@+body
	def bindBar (self, bar, verticalFlag):
		
		if verticalFlag == self.splitVerticalFlag:
			bar.bind("<B1-Motion>", self.onDragMainSplitBar)
		else:
			bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)
	#@-body
	#@-node:1::bindBar
	#@+node:2::createBothLeoSplitters
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
		#@+node:1::<< create the body pane >>
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
		#@-node:1::<< create the body pane >>

		
		#@<< create the tree pane >>
		#@+node:2::<< create the tree pane >>
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
		#@-node:2::<< create the tree pane >>

		
		#@<< create the log pane >>
		#@+node:3::<< create the log pane >>
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
		#@-node:3::<< create the log pane >>

		# Give the log and body panes the proper borders.
		self.reconfigurePanes()
	#@-body
	#@-node:2::createBothLeoSplitters
	#@+node:3::createLeoSplitter
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
	#@+node:6::onDrag...
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
	#@-node:6::onDrag...
	#@+node:7::placeSplitter
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
	#@-node:7::placeSplitter
	#@-node:18::Splitter stuff
	#@-others
#@-body
#@-node:0::@file leoFrame.py
#@-leo
