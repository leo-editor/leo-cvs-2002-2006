#@+leo-ver=4
#@+node:@file leoMenu.py
"""Gui-independent menu handling for Leo."""

from leoGlobals import *

class leoMenu:
	
	"""The base class for all Leo menus."""

	#@	@+others
	#@+node: leoMenu.__init__
	def __init__ (self,frame):
		
		self.c = frame.c
		self.frame = frame
		self.menus = {} # Menu dictionary.
		self.menuShortcuts = []
		
		self.defineMenuTables()
	#@nonl
	#@-node: leoMenu.__init__
	#@+node:defineMenuTables
	def defineMenuTables (self):
		
		c = self.c ; f = self.frame
		
		#@	<< define edit menu tables >>
		#@+node:<< define edit menu tables >>
		#@<< define editMenuTopTable >>
		#@+node:<< define editMenuTopTable >>
		self.editMenuTopTable = (
			("Can't Undo","Ctrl+Z",c.undoer.undo), # &U reserved for Undo
			("Can't Redo","Shift+Ctrl+Z",c.undoer.redo), # &R reserved for Redo
			("-",None,None),
			("Cu&t","Ctrl+X",f.OnCutFromMenu), 
			("Cop&y","Ctrl+C",f.OnCopyFromMenu),
			("&Paste","Ctrl+V",f.OnPasteFromMenu),
			("&Delete",None,c.delete),
			("Select &All","Ctrl+A",f.body.selectAllText),
			("-",None,None))
		#@nonl
		#@-node:<< define editMenuTopTable >>
		#@nl
		#@<< define editMenuEditBodyTable >>
		#@+node:<< define editMenuEditBodyTable >>
		self.editMenuEditBodyTable = (
			("Extract &Section","Shift+Ctrl+E",c.extractSection),
			("Extract &Names","Shift+Ctrl+N",c.extractSectionNames),
			("&Extract","Shift+Ctrl+D",c.extract),
			("-",None,None),
			("Convert All B&lanks",None,c.convertAllBlanks),
			("Convert All T&abs",None,c.convertAllTabs),
			("Convert &Blanks","Shift+Ctrl+B",c.convertBlanks),
			("Convert &Tabs","Shift+Ctrl+J",c.convertTabs),
			("Insert Body Time/&Date","Shift+Ctrl+G",c.insertBodyTime),
			("&Reformat Paragraph","Shift+Ctrl+P",c.reformatParagraph),
			("-",None,None),
			("&Indent","Ctrl+]",c.indentBody),
			("&Unindent","Ctrl+[",c.dedentBody),
			("&Match Brackets","Ctrl+K",c.findMatchingBracket))
		#@nonl
		#@-node:<< define editMenuEditBodyTable >>
		#@nl
		#@<< define editMenuEditHeadlineTable >>
		#@+node:<< define editMenuEditHeadlineTable >>
		self.editMenuEditHeadlineTable = (
			("Edit &Headline","Ctrl+H",c.editHeadline),
			("&End Edit Headline","Escape",f.endEditLabelCommand),
			("&Abort Edit Headline","Shift-Escape",f.abortEditLabelCommand),
			("Insert Headline Time/&Date","Shift+Ctrl+H",f.insertHeadlineTime))
			# 5/16/03 EKR: I dislike this command.
			#("Toggle Angle Brackets","Ctrl+B",c.toggleAngleBrackets)
		#@nonl
		#@-node:<< define editMenuEditHeadlineTable >>
		#@nl
		#@<< define editMenuFindMenuTable >>
		#@+node:<< define editMenuFindMenuTable >>
		self.editMenuFindMenuTable = (
			("&Find Panel","Ctrl+F",c.findPanel),
			("-",None,None),
			("Find &Next","F3",c.findNext),
			("Find &Previous","F4",c.findPrevious),
			("&Replace","Ctrl+=",c.replace),
			("Replace, &Then Find","Ctrl+-",c.replaceThenFind))
		#@nonl
		#@-node:<< define editMenuFindMenuTable >>
		#@nl
		#@<< define editMenuTop2Table >>
		#@+node:<< define editMenuTop2Table >>
		try:
			show = c.frame.body.getColorizer().showInvisibles
		except:
			show = false
		
		label = choose(show,"Hide In&visibles","Show In&visibles")
			
		self.editMenuTop2Table = (
			("&Go To Line Number","Alt+G",c.goToLineNumber),
			("&Execute Script","Alt+Shift+E",c.executeScript),
			("Set Fon&t...","Shift+Alt+T",c.fontPanel),
			("Set &Colors...","Shift+Alt+C",c.colorPanel),
			(label,"Alt+V",c.viewAllCharacters),
			("-",None,None),
			("Prefere&nces","Ctrl+Y",c.preferences))
		#@nonl
		#@-node:<< define editMenuTop2Table >>
		#@nl
		#@nonl
		#@-node:<< define edit menu tables >>
		#@nl
		#@	<< define file menu tables >>
		#@+node:<< define file menu tables >>
		#@<< define fileMenuTopTable >>
		#@+node:<< define fileMenuTopTable >>
		self.fileMenuTopTable = (
			("&New","Ctrl+N",c.new),
			("&Open...","Ctrl+O",c.open))
		#@nonl
		#@-node:<< define fileMenuTopTable >>
		#@nl
		#@<< define fileMenuTop2Table >>
		#@+node:<< define fileMenuTop2Table >>
		self.fileMenuTop2Table = (
			("-",None,None),
			("&Close","Ctrl+W",c.close),
			("&Save","Ctrl+S",c.save),
			("Save &As","Shift+Ctrl+S",c.saveAs),
			("Save To",None,c.saveTo), # &Tangle
			("Re&vert To Saved",None,c.revert)) # &Read/Write
		#@nonl
		#@-node:<< define fileMenuTop2Table >>
		#@nl
		#@<< define fileMenuReadWriteMenuTable >>
		#@+node:<< define fileMenuReadWriteMenuTable >>
		self.fileMenuReadWriteMenuTable = (
			("&Read Outline Only","Shift+Ctrl+R",c.readOutlineOnly),
			("Read @file &Nodes",None,c.readAtFileNodes),
			("-",None,None),
			("Write &Dirty @file Nodes","Shift+Ctrl+Q",c.fileCommands.writeDirtyAtFileNodes),
			("Write &Missing @file Nodes",None,c.fileCommands.writeMissingAtFileNodes),
			("Write &Outline Only",None,c.fileCommands.writeOutlineOnly),
			("&Write @file Nodes","Shift+Ctrl+W",c.fileCommands.writeAtFileNodes),
			("-",None,None),
			("Write 4.x Derived Files",None,c.writeNewDerivedFiles),
			("Write 3.x Derived Files",None,c.writeOldDerivedFiles))
		#@nonl
		#@-node:<< define fileMenuReadWriteMenuTable >>
		#@nl
		#@<< define fileMenuTangleMenuTable >>
		#@+node:<< define fileMenuTangleMenuTable >>
		self.fileMenuTangleMenuTable = (
			("Tangle &All","Shift+Ctrl+A",c.tangleAll),
			("Tangle &Marked","Shift+Ctrl+M",c.tangleMarked),
			("&Tangle","Shift+Ctrl+T",c.tangle))
		#@nonl
		#@-node:<< define fileMenuTangleMenuTable >>
		#@nl
		#@<< define fileMenuUntangleMenuTable >>
		#@+node:<< define fileMenuUntangleMenuTable >>
		self.fileMenuUntangleMenuTable = (
			("Untangle &All",None,c.untangleAll),
			("Untangle &Marked",None,c.untangleMarked),
			("&Untangle","Shift+Ctrl+U",c.untangle))
		#@nonl
		#@-node:<< define fileMenuUntangleMenuTable >>
		#@nl
		#@<< define fileMenuImportMenuTable >>
		#@+node:<< define fileMenuImportMenuTable >>
		self.fileMenuImportMenuTable = (
			("Import Derived File",None,c.importDerivedFile),
			("Import To @&file","Shift+Ctrl+F",c.importAtFile),
			("Import To @&root",None,c.importAtRoot),
			("Import &CWEB Files",None,c.importCWEBFiles),
			
			("Import &noweb Files",None,c.importNowebFiles),
			("Import Flattened &Outline",None,c.importFlattenedOutline))
		#@nonl
		#@-node:<< define fileMenuImportMenuTable >>
		#@nl
		#@<< define fileMenuExportMenuTable >>
		#@+node:<< define fileMenuExportMenuTable >>
		self.fileMenuExportMenuTable = [
			("Export &Headlines",None,c.exportHeadlines),
			("Outline To &CWEB",None,c.outlineToCWEB),
			("Outline To &Noweb",None,c.outlineToNoweb),
			("&Flatten Outline",None,c.flattenOutline),
			("&Remove Sentinels",None,c.removeSentinels),
			("&Weave",None,c.weave)]
		#@nonl
		#@-node:<< define fileMenuExportMenuTable >>
		#@nl
		#@<< define fileMenuTop3MenuTable >>
		#@+node:<< define fileMenuTop3MenuTable >>
		self.fileMenuTop3MenuTable = (
			("E&xit","Ctrl-Q",app.onQuit),)
		#@nonl
		#@-node:<< define fileMenuTop3MenuTable >>
		#@nl
		#@nonl
		#@-node:<< define file menu tables >>
		#@nl
		#@	<< define outline menu tables >>
		#@+node:<< define outline menu tables >>
		#@<< define outlineMenuTopMenuTable >>
		#@+node:<< define outlineMenuTopMenuTable >>
		self.outlineMenuTopMenuTable = (
			("C&ut Node","Shift+Ctrl+X",c.cutOutline),
			("C&opy Node","Shift+Ctrl+C",c.copyOutline),
			("&Paste Node","Shift+Ctrl+V",c.pasteOutline),
			("&Delete Node","Shift+Ctrl+BkSp",c.deleteOutline),
			("-",None,None),
			("&Insert Node","Ctrl+I",c.insertHeadline),
			("&Clone Node","Ctrl+`",c.clone),
			("Sort C&hildren",None,c.sortChildren),
			("&Sort Siblings","Alt-A",c.sortSiblings),
			("Chec&k Outline",None,c.checkOutline),
			("-",None,None),
			("&Hoist",None,c.hoist),
			("D&e-Hoist",None,f.c.dehoist),
			("-",None,None))
		#@nonl
		#@-node:<< define outlineMenuTopMenuTable >>
		#@nl
		#@<< define outlineMenuExpandContractMenuTable >>
		#@+node:<< define outlineMenuExpandContractMenuTable >>
		self.outlineMenuExpandContractMenuTable = (
			("&Contract All","Alt+-",c.contractAllHeadlines),
			("Contract &Node","Alt+[",c.contractNode),
			("Contract &Parent","Alt+0",c.contractParent),
			("-",None,None),
			("Expand P&rev Level","Alt+.",c.expandPrevLevel),
			("Expand N&ext Level","Alt+=",c.expandNextLevel),
			("-",None,None),
			("Expand To Level &1","Alt+1",c.expandLevel1),
			("Expand To Level &2","Alt+2",c.expandLevel2),
			("Expand To Level &3","Alt+3",c.expandLevel3),
			("Expand To Level &4","Alt+4",c.expandLevel4),
			("Expand To Level &5","Alt+5",c.expandLevel5),
			("Expand To Level &6","Alt+6",c.expandLevel6),
			("Expand To Level &7","Alt+7",c.expandLevel7),
			("Expand To Level &8","Alt+8",c.expandLevel8),
			# ("Expand To Level &9","Alt+9",c.expandLevel9),
			("-",None,None),
			("Expand &All","Alt+9",c.expandAllHeadlines),
			("Expand N&ode","Alt+]",c.expandNode))
		#@nonl
		#@-node:<< define outlineMenuExpandContractMenuTable >>
		#@nl
		#@<< define outlineMenuMoveMenuTable >>
		#@+node:<< define outlineMenuMoveMenuTable >>
		self.outlineMenuMoveMenuTable = (
			("Move &Down", "Ctrl+D",c.moveOutlineDown),
			("Move &Left", "Ctrl+L",c.moveOutlineLeft),
			("Move &Right","Ctrl+R",c.moveOutlineRight),
			("Move &Up",   "Ctrl+U",c.moveOutlineUp),
			("-",None,None),
			("&Promote","Ctrl+{",c.promote),
			("&Demote", "Ctrl+}",c.demote))
		#@nonl
		#@-node:<< define outlineMenuMoveMenuTable >>
		#@nl
		#@<< define outlineMenuMarkMenuTable >>
		#@+node:<< define outlineMenuMarkMenuTable >>
		self.outlineMenuMarkMenuTable = (
			("&Mark","Ctrl-M",c.markHeadline),
			("Mark &Subheads","Alt+S",c.markSubheads),
			("Mark Changed &Items","Alt+C",c.markChangedHeadlines),
			("Mark Changed &Roots","Alt+R",c.markChangedRoots),
			("Mark &Clones","Alt+K",c.markClones),
			("&Unmark All","Alt+U",c.unmarkAll))
		#@nonl
		#@-node:<< define outlineMenuMarkMenuTable >>
		#@nl
		#@<< define outlineMenuGoToMenuTable >>
		#@+node:<< define outlineMenuGoToMenuTable >>
		self.outlineMenuGoToMenuTable = (
			("Go Back",None,c.goPrevVisitedNode), # Usually use buttons for this.
			("Go Forward",None,c.goNextVisitedNode),
			("-",None,None),
			("Go To Next &Marked","Alt+M",c.goToNextMarkedHeadline),
			("Go To Next C&hanged","Alt+D",c.goToNextDirtyHeadline),
			("Go To Next &Clone","Alt+N",c.goToNextClone),
			("-",None,None),
			("Go To &First Node","Alt+Shift+G",c.goToFirstNode),
			("Go To &Last Node","Alt+Shift+H",c.goToLastNode),
			("Go To &Parent","Alt+Shift+P",c.goToParent),
			("Go To P&rev Sibling","Alt+Shift+R",c.goToPrevSibling),
			("Go To Next &Sibling","Alt+Shift+S",c.goToNextSibling),
			("-",None,None),
			("Go To Prev V&isible","Alt-UpArrow",c.selectVisBack),
			("Go To Next &Visible","Alt-DnArrow",c.selectVisNext),
			("Go To Prev Node","Alt-Shift+UpArrow",c.selectThreadBack),
			("Go To Next Node","Alt-Shift-DnArrow",c.selectThreadNext))
		#@nonl
		#@-node:<< define outlineMenuGoToMenuTable >>
		#@nl
		#@nonl
		#@-node:<< define outline menu tables >>
		#@nl
		#@	<< define window menu tables >>
		#@+node:<< define window menu tables >>
		self.windowMenuTopTable = (
			("&Equal Sized Panes","Ctrl-E",f.equalSizedPanes),
			("Toggle &Active Pane","Ctrl-T",f.toggleActivePane),
			("Toggle &Split Direction",None,f.toggleSplitDirection),
			("-",None,None),
			("Casca&de",None,f.cascade),
			("&Minimize All",None,f.minimizeAll),
			("-",None,None),
			("Open &Compare Window",None,c.openCompareWindow),
			("Open &Python Window","Alt+P",c.openPythonWindow))
		#@nonl
		#@-node:<< define window menu tables >>
		#@nl
		#@	<< define help menu tables >>
		#@+node:<< define help menu tables >>
		self.helpMenuTopTable = (
			("&About Leo...",None,c.about),
			("Online &Home Page",None,c.leoHome),
			("-",None,None),
			("Open Online &Tutorial",None,c.leoTutorial))
			
		self.helpMenuTop2Table = (
			("Open &Offline Tutorial",None,f.leoHelp),)
			
		self.helpMenuTop3Table = (
			("Open Leo&Docs.leo",None,c.leoDocumentation),
			("-",None,None),
			("Open Leo&Config.leo",None,c.leoConfig),
			("Apply &Settings",None,c.applyConfig))
		#@nonl
		#@-node:<< define help menu tables >>
		#@nl
	#@nonl
	#@-node:defineMenuTables
	#@+node:oops
	def oops (self):
	
		print "leoMenu oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:oops
	#@+node:updateAllMenus
	def updateAllMenus (self):
		
		"""The Tk "postcommand" callback called when a click happens in any menu.
		
		Updates (enables or disables) all menu items."""
		
		# A horrible kludge: set app.log to cover for a possibly missing activate event.
		app.setLog(self.frame.log,"updateAllMenus")
		
		# Allow the user first crack at updating menus.
		c = self.c ; v = c.currentVnode()
		if not doHook("menu2",c=c,v=v):
			self.updateFileMenu()
			self.updateEditMenu()
			self.updateOutlineMenu()
	#@nonl
	#@-node:updateAllMenus
	#@+node:updateFileMenu
	def updateFileMenu (self):
		
		c = self.c ; frame = c.frame
		if not c: return
	
		try:
			enable = frame.menu.enableMenu
			menu = frame.menu.getMenu("File")
			enable(menu,"Revert To Saved", c.canRevert())
			enable(menu,"Open With...", app.hasOpenWithMenu)
		except:
			es("exception updating File menu")
			es_exception()
	#@nonl
	#@-node:updateFileMenu
	#@+node:updateEditMenu
	def updateEditMenu (self):
	
		c = self.c ; frame = c.frame
		if not c: return
		try:
			# Top level Edit menu...
			enable = frame.menu.enableMenu
			menu = frame.menu.getMenu("Edit")
			c.undoer.enableMenuItems()
			if 0: # Always on for now.
				enable(menu,"Cut",c.canCut())
				enable(menu,"Copy",c.canCut())
				enable(menu,"Paste",c.canPaste())
			if 0: # Always on for now.
				menu = frame.menu.getMenu("Find...")
				enable(menu,"Find Next",c.canFind())
				flag = c.canReplace()
				enable(menu,"Replace",flag)
				enable(menu,"Replace, Then Find",flag)
			# Edit Body submenu...
			menu = frame.menu.getMenu("Edit Body...")
			enable(menu,"Extract Section",c.canExtractSection())
			enable(menu,"Extract Names",c.canExtractSectionNames())
			enable(menu,"Extract",c.canExtract())
			enable(menu,"Match Brackets",c.canFindMatchingBracket())
		except:
			es("exception updating Edit menu")
			es_exception()
	#@nonl
	#@-node:updateEditMenu
	#@+node:updateOutlineMenu
	def updateOutlineMenu (self):
	
		c = self.c ; frame = c.frame ; v = c.currentVnode()
		if not c: return
		try:
			enable = frame.menu.enableMenu
			# Top level outline menu...
			menu = frame.menu.getMenu("Outline")
			enable(menu,"Cut Node",c.canCutOutline())
			enable(menu,"Delete Node",c.canDeleteHeadline())
			enable(menu,"Paste Node",c.canPasteOutline())
			enable(menu,"Sort Siblings",c.canSortSiblings())
			enable(menu,"Hoist",c.canHoist())
			enable(menu,"De-Hoist",c.canDehoist())
			# Expand/Contract submenu...
			menu = frame.menu.getMenu("Expand/Contract...")
			hasChildren = v.hasChildren()
			isExpanded = v.isExpanded()
			enable(menu,"Contract Parent",c.canContractParent())
			enable(menu,"Contract Node",hasChildren and isExpanded)
			enable(menu,"Expand Node",hasChildren and not isExpanded)
			enable(menu,"Expand Prev Level",hasChildren and isExpanded)
			enable(menu,"Expand Next Level",hasChildren)
			enable(menu,"Expand To Level 1",hasChildren and isExpanded)
			for i in xrange(2,9):
				frame.menu.enableMenu(menu,"Expand To Level " + str(i), hasChildren)
			# Move submenu...
			menu = frame.menu.getMenu("Move...")
			enable(menu,"Move Down",c.canMoveOutlineDown())
			enable(menu,"Move Left",c.canMoveOutlineLeft())
			enable(menu,"Move Right",c.canMoveOutlineRight())
			enable(menu,"Move Up",c.canMoveOutlineUp())
			enable(menu,"Promote",c.canPromote())
			enable(menu,"Demote",c.canDemote())
			# Go To submenu
			menu = frame.menu.getMenu("Go To...")
			enable(menu,"Go Back",c.beadPointer > 1)
			enable(menu,"Go Forward",c.beadPointer + 1 < len(c.beadList))
			enable(menu,"Go To Prev Visible",c.canSelectVisBack())
			enable(menu,"Go To Next Visible",c.canSelectVisNext())
			enable(menu,"Go To Next Marked",c.canGoToNextMarkedHeadline())
			enable(menu,"Go To Next Changed",c.canGoToNextDirtyHeadline())
			enable(menu,"Go To Next Clone",v.isCloned())
			enable(menu,"Go To Prev Node",c.canSelectThreadBack())
			enable(menu,"Go To Next Node",c.canSelectThreadNext())
			enable(menu,"Go To Parent",v.parent() != None)
			enable(menu,"Go To Prev Sibling",v.back() != None)
			enable(menu,"Go To Next Sibling",v.next() != None)
			# Mark submenu
			menu = frame.menu.getMenu("Mark/Unmark...")
			label = choose(v and v.isMarked(),"Unmark","Mark")
			frame.menu.setMenuLabel(menu,0,label)
			enable(menu,"Mark Subheads",(v and v.hasChildren()))
			enable(menu,"Mark Changed Items",c.canMarkChangedHeadlines())
			enable(menu,"Mark Changed Roots",c.canMarkChangedRoots())
			enable(menu,"Mark Clones",v.isCloned())
		except:
			es("exception updating Outline menu")
			es_exception()
	#@nonl
	#@-node:updateOutlineMenu
	#@+node:hasSelection
	# Returns true if text in the outline or body text is selected.
	
	def hasSelection (self):
		
		body = self.frame.body
	
		if body:
			first, last = body.getTextSelection()
			return first != last
		else:
			return false
	#@nonl
	#@-node:hasSelection
	#@+node:get/setRealMenuName & setRealMenuNamesFromTable (MOVED to leoMenu class)
	# Returns the translation of a menu name or an item name.
	
	def getRealMenuName (self,menuName):
	
		cmn = self.canonicalizeTranslatedMenuName(menuName)
		return app.realMenuNameDict.get(cmn,menuName)
		
	def setRealMenuName (self,untrans,trans):
	
		cmn = self.canonicalizeTranslatedMenuName(untrans)
		app.realMenuNameDict[cmn] = trans
	
	def setRealMenuNamesFromTable (self,table):
	
		try:
			for untrans,trans in table:
				self.setRealMenuName(untrans,trans)
		except:
			es("exception in setRealMenuNamesFromTable")
			es_exception()
	#@nonl
	#@-node:get/setRealMenuName & setRealMenuNamesFromTable (MOVED to leoMenu class)
	#@+node:canonicalizeMenuName & cononicalizeTranslatedMenuName
	def canonicalizeMenuName (self,name):
		
		name = name.lower() ; newname = ""
		for ch in name:
			# if ch not in (' ','\t','\n','\r','&'):
			if ch in string.ascii_letters:
				newname = newname+ch
		return newname
		
	def canonicalizeTranslatedMenuName (self,name):
		
		name = name.lower() ; newname = ""
		for ch in name:
			if ch not in (' ','\t','\n','\r','&'):
			# if ch in string.ascii_letters:
				newname = newname+ch
		return newname
	#@-node:canonicalizeMenuName & cononicalizeTranslatedMenuName
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
		has_cmd   = s.find("cmd") >= 0     or s.find("command") >= 0 # 11/18/03
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
			if ch in string.ascii_letters:
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
		
		if has_cmd: # 11/18/03
			bind_head = bind_head + "Command-"
			menu_head = menu_head + "Command+"
		
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
		#@nonl
		#@-node:<< synthesize the shortcuts from the information >>
		#@nl
		# print shortcut,bind_shortcut,menu_shortcut
		return bind_shortcut,menu_shortcut
	#@nonl
	#@-node:canonicalizeShortcut
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
	
	def createMenuEntries (self,menu,table,openWith=false):
		
		for label,accel,command in table:
			if label == None or command == None or label == "-":
				self.add_separator(menu)
			else:
				#@			<< set name to the label for doCommand >>
				#@+node:<< set name to the label for doCommand >>
				name = label.strip().lower()
				
				# Remove special characters from command names.
				name2 = ""
				for ch in name:
					if ch in string.ascii_letters or ch in string.digits:
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
				# This has already been bound in leoTkinterFrame.__init__
				# 2/13/03: A _possible_ fix for the Linux control-v bug.
				
				if sys.platform not in ("linux1","linux2"):
					if bind_shortcut in ("<Control-c>","<Control-v>","<Control-x>"):
						bind_shortcut = None
				#@nonl
				#@-node:<< set bind_shortcut and menu_shortcut using accel >>
				#@nl
				#@			<< define callback function >>
				#@+node:<< define callback function >>
				if openWith:
					callback = self.defineOpenWithMenuCallback(command)
				else:
					callback = self.defineMenuCallback(command,name)
				#@nonl
				#@-node:<< define callback function >>
				#@nl
				#@			<< set realLabel, amp_index and menu_shortcut >>
				#@+node:<< set realLabel, amp_index and menu_shortcut >>
				realLabel = self.getRealMenuName(label)
				amp_index = realLabel.find("&")
				realLabel = realLabel.replace("&","")
				if not menu_shortcut:
					menu_shortcut = ""
				#@nonl
				#@-node:<< set realLabel, amp_index and menu_shortcut >>
				#@nl
		
				self.add_command(menu,label=realLabel,accelerator=menu_shortcut,
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
							self.frame.body.bind(bind_shortcut,callback)
							self.bind(bind_shortcut,callback)
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
	def createMenuItemsFromTable (self,menuName,table,openWith=false):
		
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
			
		app.menuWarningsGiven = true
	#@nonl
	#@-node:createMenuItemsFromTable
	#@+node:createMenusFromTables
	def createMenusFromTables (self):
	
		c = self.c
		#@	<< create the file menu >>
		#@+node:<< create the file menu >>
		fileMenu = self.createNewMenu("&File")
		
		self.createMenuEntries(fileMenu,self.fileMenuTopTable)
		self.createNewMenu("Open &With...","File")
		self.createMenuEntries(fileMenu,self.fileMenuTop2Table)
		#@<< create the recent files submenu >>
		#@+node:<< create the recent files submenu >>
		self.createNewMenu("Recent &Files...","File")
		c.recentFiles = app.config.getRecentFiles()
		
		if 0: # Not needed, and causes problems in wxWindows...
			self.createRecentFilesMenuItems()
		#@nonl
		#@-node:<< create the recent files submenu >>
		#@nl
		self.add_separator(fileMenu)
		#@<< create the read/write submenu >>
		#@+node:<< create the read/write submenu >>
		readWriteMenu = self.createNewMenu("&Read/Write...","File")
		
		self.createMenuEntries(readWriteMenu,self.fileMenuReadWriteMenuTable)
		#@nonl
		#@-node:<< create the read/write submenu >>
		#@nl
		#@<< create the tangle submenu >>
		#@+node:<< create the tangle submenu >>
		tangleMenu = self.createNewMenu("&Tangle...","File")
		
		self.createMenuEntries(tangleMenu,self.fileMenuTangleMenuTable)
		#@nonl
		#@-node:<< create the tangle submenu >>
		#@nl
		#@<< create the untangle submenu >>
		#@+node:<< create the untangle submenu >>
		untangleMenu = self.createNewMenu("&Untangle...","File")
		
		self.createMenuEntries(untangleMenu,self.fileMenuUntangleMenuTable)
		#@nonl
		#@-node:<< create the untangle submenu >>
		#@nl
		#@<< create the import submenu >>
		#@+node:<< create the import submenu >>
		importMenu = self.createNewMenu("&Import...","File")
		
		self.createMenuEntries(importMenu,self.fileMenuImportMenuTable)
		#@nonl
		#@-node:<< create the import submenu >>
		#@nl
		#@<< create the export submenu >>
		#@+node:<< create the export submenu >>
		exportMenu = self.createNewMenu("&Export...","File")
		
		self.createMenuEntries(exportMenu,self.fileMenuExportMenuTable)
		#@nonl
		#@-node:<< create the export submenu >>
		#@nl
		self.add_separator(fileMenu)
		self.createMenuEntries(fileMenu,self.fileMenuTop3MenuTable)
		#@nonl
		#@-node:<< create the file menu >>
		#@nl
		#@	<< create the edit menu >>
		#@+node:<< create the edit menu >>
		editMenu = self.createNewMenu("&Edit")
		
		self.createMenuEntries(editMenu,self.editMenuTopTable)
		
		#@<< create the edit body submenu >>
		#@+node:<< create the edit body submenu >>
		editBodyMenu = self.createNewMenu("Edit &Body...","Edit")
		
		self.createMenuEntries(editBodyMenu,self.editMenuEditBodyTable)
		#@nonl
		#@-node:<< create the edit body submenu >>
		#@nl
		#@<< create the edit headline submenu >>
		#@+node:<< create the edit headline submenu >>
		editHeadlineMenu = self.createNewMenu("Edit &Headline...","Edit")
		
		self.createMenuEntries(editHeadlineMenu,self.editMenuEditHeadlineTable)
		#@nonl
		#@-node:<< create the edit headline submenu >>
		#@nl
		#@<< create the find submenu >>
		#@+node:<< create the find submenu >>
		findMenu = self.createNewMenu("&Find...","Edit")
		
		self.createMenuEntries(findMenu,self.editMenuFindMenuTable)
		#@nonl
		#@-node:<< create the find submenu >>
		#@nl
		
		self.createMenuEntries(editMenu,self.editMenuTop2Table)
		#@nonl
		#@-node:<< create the edit menu >>
		#@nl
		#@	<< create the outline menu >>
		#@+node:<< create the outline menu >>
		outlineMenu = self.createNewMenu("&Outline")
		
		self.createMenuEntries(outlineMenu,self.outlineMenuTopMenuTable)
		
		#@<< create expand/contract submenu >>
		#@+node:<< create expand/contract submenu >>
		expandMenu = self.createNewMenu("&Expand/Contract...","Outline")
		
		self.createMenuEntries(expandMenu,self.outlineMenuExpandContractMenuTable)
		#@nonl
		#@-node:<< create expand/contract submenu >>
		#@nl
		#@<< create move submenu >>
		#@+node:<< create move submenu >>
		moveSelectMenu = self.createNewMenu("&Move...","Outline")
		
		self.createMenuEntries(moveSelectMenu,self.outlineMenuMoveMenuTable)
		#@nonl
		#@-node:<< create move submenu >>
		#@nl
		#@<< create mark submenu >>
		#@+node:<< create mark submenu >>
		markMenu = self.createNewMenu("M&ark/Unmark...","Outline")
		
		self.createMenuEntries(markMenu,self.outlineMenuMarkMenuTable)
		#@nonl
		#@-node:<< create mark submenu >>
		#@nl
		#@<< create goto submenu >>
		#@+node:<< create goto submenu >>
		gotoMenu = self.createNewMenu("&Go To...","Outline")
		
		self.createMenuEntries(gotoMenu,self.outlineMenuGoToMenuTable)
		#@nonl
		#@-node:<< create goto submenu >>
		#@nl
		#@nonl
		#@-node:<< create the outline menu >>
		#@nl
		doHook("create-optional-menus",c=c)
		#@	<< create the window menu >>
		#@+node:<< create the window menu >>
		windowMenu = self.createNewMenu("&Window")
		
		self.createMenuEntries(windowMenu,self.windowMenuTopTable)
		#@nonl
		#@-node:<< create the window menu >>
		#@nl
		#@	<< create the help menu >>
		#@+node:<< create the help menu >>
		helpMenu = self.createNewMenu("&Help")
		
		self.createMenuEntries(helpMenu,self.helpMenuTopTable)
		
		if sys.platform=="win32":
			self.createMenuEntries(helpMenu,self.helpMenuTop2Table)
		
		self.createMenuEntries(helpMenu,self.helpMenuTop3Table)
		#@nonl
		#@-node:<< create the help menu >>
		#@nl
	#@nonl
	#@-node:createMenusFromTables
	#@+node:createNewMenu
	def createNewMenu (self,menuName,parentName="top",before=None):
	
		try:
			parent = self.getMenu(parentName)
			
			if 0: # 11/13/03: Allow parent to be None.
				if parent == None:
					es("unknown parent menu: " + parentName)
					return None
	
			menu = self.getMenu(menuName)
			if menu:
				es("menu already exists: " + menuName,color="red")
			else:
				menu = self.new_menu(parent,tearoff=0)
				self.setMenu(menuName,menu)
				label = self.getRealMenuName(menuName)
				amp_index = label.find("&")
				label = label.replace("&","")
				if before: # Insert the menu before the "before" menu.
					index_label = self.getRealMenuName(before)
					amp_index = index_label.find("&")
					index_label = index_label.replace("&","")
					index = parent.index(index_label)
					self.insert_cascade(parent,index=index,label=label,menu=menu,underline=amp_index)
				else:
					self.add_cascade(parent,label=label,menu=menu,underline=amp_index)
				return menu
		except:
			es("exception creating " + menuName + " menu")
			es_exception()
			return None
	#@nonl
	#@-node:createNewMenu
	#@+node:createRecentFilesMenuItems (leoMenu)
	def createRecentFilesMenuItems (self):
		
		c = self.c ; frame = c.frame
		recentFilesMenu = self.getMenu("Recent Files...")
		
		# Delete all previous entries.
		self.delete_range(recentFilesMenu,0,len(c.recentFiles)+2)
		
		# Create the first two entries.
		table = (
			("Clear Recent Files",None,c.clearRecentFiles),
			("-",None,None))
		self.createMenuEntries(recentFilesMenu,table)
		
		# Create all the other entries.
		i = 3
		for name in c.recentFiles:
			callback = lambda f=frame,name=name:c.openRecentFile(name)
			label = "%d %s" % (i-2,computeWindowTitle(name))
			self.add_command(recentFilesMenu,label=label,command=callback,underline=0)
			i += 1
	#@nonl
	#@-node:createRecentFilesMenuItems (leoMenu)
	#@+node:deleteMenu
	def deleteMenu (self,menuName):
	
		try:
			menu = self.getMenu(menuName)
			if menu:
				self.destroy(menu)
				self.destroyMenu(menuName)
			else:
				es("can't delete menu: " + menuName)
		except:
			es("exception deleting " + menuName + " menu")
			es_exception()
	#@nonl
	#@-node:deleteMenu
	#@+node:deleteMenuItem
	def deleteMenuItem (self,itemName,menuName="top"):
		
		"""Delete itemName from the menu whose name is menuName.."""
	
		try:
			menu = self.getMenu(menuName)
			if menu:
				realItemName = self.getRealMenuName(itemName)
				self.delete(menu,realItemName)
			else:
				es("menu not found: " + menuName)
		except:
			es("exception deleting " + itemName + " from " + menuName + " menu")
			es_exception()
	#@nonl
	#@-node:deleteMenuItem
	#@+node:getMenu, setMenu, destroyMenu
	def getMenu (self,menuName):
	
		cmn = self.canonicalizeMenuName(menuName)
		return self.menus.get(cmn)
		
	def setMenu (self,menuName,menu):
		
		cmn = self.canonicalizeMenuName(menuName)
		self.menus [cmn] = menu
		
	def destroyMenu (self,menuName):
		
		cmn = self.canonicalizeMenuName(menuName)
		del self.menus[cmn]
	#@nonl
	#@-node:getMenu, setMenu, destroyMenu
	#@+node:9 Routines with Tk spellings
	def add_cascade (self,parent,label,menu,underline):
		self.oops()
		
	def add_command (self,menu,**keys):
		self.oops()
		
	def add_separator(self,menu):
		self.oops()
		
	def bind (self,bind_shortcut,callback):
		self.oops()
	
	def delete (self,menu,realItemName):
		self.oops()
		
	def delete_range (self,menu,n1,n2):
		self.oops()
	
	def destroy (self,menu):
		self.oops()
	
	def insert_cascade (self,parent,index,label,menu,underline):
		self.oops()
	
	def new_menu(self,parent,tearoff=0):
		self.oops()
	#@nonl
	#@-node:9 Routines with Tk spellings
	#@+node:7 Routines with new spellings
	def createMenuBar (self,frame):
		self.oops()
		
	def createOpenWithMenuFromTable (self,table):
		self.oops()
	
	def defineMenuCallback(self,command,name):
		self.oops()
		
	def defineOpenWithMenuCallback(self,command):
		self.oops()
		
	def disableMenu (self,menu,name):
		self.oops()
		
	def enableMenu (self,menu,name,val):
		self.oops()
		
	def setMenuLabel (self,menu,name,label,underline=-1):
		self.oops()
	#@nonl
	#@-node:7 Routines with new spellings
	#@-others
#@nonl
#@-node:@file leoMenu.py
#@-leo
