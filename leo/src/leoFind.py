#@+leo-ver=4
#@+node:@file leoFind.py
#@@language python

#@<< Theory of operation of find/change >>
#@+node:<< Theory of operation of find/change >>
#@+at 
#@nonl
# The find and change commands are tricky; there are many details that must be 
# handled properly. This documentation describes the leo.py code. Previous 
# versions of Leo used an inferior scheme.  The following principles govern 
# the leoFind class:
# 
# 1.	Find and Change commands initialize themselves using only the state of 
# the present Leo window. In particular, the Find class must not save internal 
# state information from one invocation to the next. This means that when the 
# user changes the nodes, or selects new text in headline or body text, those 
# changes will affect the next invocation of any Find or Change command. 
# Failure to follow this principle caused all kinds of problems in the Borland 
# and Macintosh codes. There is one exception to this rule: we must remember 
# where interactive wrapped searches start. This principle simplifies the code 
# because most ivars do not persist. However, each command must ensure that 
# the Leo window is left in a state suitable for restarting the incremental 
# (interactive) Find and Change commands. Details of initialization are 
# discussed below.
# 
# 2. The Find and Change commands must not change the state of the outline or 
# body pane during execution. That would cause severe flashing and slow down 
# the commands a great deal. In particular, c.selectVnode and c.editVnode 
# methods must not be called while looking for matches.
# 
# 3. When incremental Find or Change commands succeed they must leave the Leo 
# window in the proper state to execute another incremental command. We 
# restore the Leo window as it was on entry whenever an incremental search 
# fails and after any Find All and Change All command.
# 
# Initialization involves setting the self.c, self.v, self.in_headline, 
# self.wrapping and self.s_text ivars. Setting self.in_headline is tricky; we 
# must be sure to retain the state of the outline pane until initialization is 
# complete. Initializing the Find All and Change All commands is much easier 
# because such initialization does not depend on the state of the Leo window.
# 
# Using Tk.Text widgets for both headlines and body text results in a huge 
# simplification of the code. Indeed, the searching code does not know whether 
# it is searching headline or body text. The search code knows only that 
# self.s_text is a Tk.Text widget that contains the text to be searched or 
# changed and the insert and sel Tk attributes of self.search_text indicate 
# the range of text to be searched. Searching headline and body text 
# simultaneously is complicated. The selectNextVnode() method handles the many 
# details involved by setting self.s_text and its insert and sel attributes.
#@-at
#@-node:<< Theory of operation of find/change >>
#@nl

from leoGlobals import *
import leoDialog
import string,sys,Tkinter,types
Tk=Tkinter

#@+others
#@+node:class leoFindBase
class leoFindBase (leoDialog.leoDialog):
	"""The base class for Leo's Find panel."""
	#@	@+others
	#@+node:findBase.__init__
	def __init__(self,title,resizeable=false):
	
		leoDialog.leoDialog.__init__(self,title,resizeable)
		self.createTopFrame()
		self.top.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
	#@nonl
	#@-node:findBase.__init__
	#@+node:onCloseWindow
	def onCloseWindow(self):
	
		self.top.withdraw()
	#@nonl
	#@-node:onCloseWindow
	#@+node:resetWrap
	def resetWrap (self,event=None):
	
		self.wrapVnode = None
		self.onlyVnode = None
	#@nonl
	#@-node:resetWrap
	#@+node:OnReturnKey (no longer used)
	def OnReturnKey (self,event):
		
		# Remove the newly inserted newline from the search & change strings.
		for text in (self.find_text,self.change_text):
			ch = text.get("insert - 1c")
			ch= toUnicode(ch,app().tkEncoding) # 9/28/03
			if ch in ('\r','\n'):
				text.delete("insert - 1c")
	
		# Do the default command.
		self.findNextCommand(top())
		return "break"
	#@nonl
	#@-node:OnReturnKey (no longer used)
	#@-others
#@nonl
#@-node:class leoFindBase
#@+node:class leoFind
class leoFind (leoFindBase):
	"""A class that implements Leo's find commands."""
	#@	@+others
	#@+node:find.__init__ (creates find panel)
	def __init__(self):
		
		leoFindBase.__init__(self,"Leo Find/Change",resizeable=false)
	
		#@	<< Initialize the leoFind ivars >>
		#@+node:<< Initialize the leoFind ivars >>
		self.dict = {}
		
		# Order is important for compatibility with 3.x.  Sheesh.
		self.intKeys = [
			"batch", "wrap", "whole_word", "ignore_case", "node_only",
			"pattern_match", "search_headline", "search_body",
			"suboutline_only", "mark_changes", "mark_finds", "reverse"]
		self.newIntKeys = ["script_change"]
		self.newStringKeys = ["radio-find-type", "radio-search-scope"]
		# self.stringKeys = ["change_text","find_text"]
		
		for key in self.intKeys:
			self.dict[key] = Tk.IntVar()
		for key in self.newIntKeys:
			self.dict[key] = Tk.IntVar()
		for key in self.newStringKeys:
			self.dict[key] = Tk.StringVar()
			
		# The c.x_flag ivars contain the user preferences.
		# These are updated just before executing any find/change command.
		
		# Ivars containing internal state...
		self.commands = None # The commander for this search.
		self.v = None # The vnode being searched.  Never saved between searches!
		self.in_headline = false # true: searching headline text.
		self.wrapping = false # true: wrapping is enabled. _not_ the same as c.wrap_flag for batch searches.
		self.s_text = Tk.Text() # Used by find.search()
		
		#@+at 
		#@nonl
		# Initializing a wrapped search is tricky.  The search() method will 
		# fail if v==wrapVnode and pos >= wrapPos.  selectNextVnode() will 
		# fail if v == wrapVnode.  We set wrapPos on entry, before the first 
		# search.  We set wrapVnode in selectNextVnode after the first search 
		# fails.  We also set wrapVnode on exit if the first search suceeds.
		#@-at
		#@@c
		self.wrapVnode = None # The start of wrapped searches: persists between calls.
		self.onlyVnode = None # The starting node for suboutline-only searches.
		self.wrapPos = None # The starting position of the wrapped search: persists between calls.
		#@nonl
		#@-node:<< Initialize the leoFind ivars >>
		#@nl
		
		self.createFrame()
	#@nonl
	#@-node:find.__init__ (creates find panel)
	#@+node:find.createFrame
	def createFrame (self):
		
		# Create the find panel...
		outer = Tk.Frame(self.frame,relief="groove",bd=2)
		outer.pack(padx=2,pady=2)
	
		#@	<< Create the Find and Change panes >>
		#@+node:<< Create the Find and Change panes >>
		fc = Tk.Frame(outer, bd="1m")
		fc.pack(anchor="n", fill="x", expand=1)
		
		# Removed unused height/width params: using fractions causes problems in some locales!
		fpane = Tk.Frame(fc, bd=1)
		cpane = Tk.Frame(fc, bd=1)
		
		fpane.pack(anchor="n", expand=1, fill="x")
		cpane.pack(anchor="s", expand=1, fill="x")
		
		# Create the labels and text fields...
		flab = Tk.Label(fpane, width=8, text="Find:")
		clab = Tk.Label(cpane, width=8, text="Change:")
		
		# Use bigger boxes for scripts.
		self.find_text   = ftxt = Tk.Text(fpane, height=10, width=80)
		self.change_text = ctxt = Tk.Text(cpane, height=10, width=80)
		
		fBar = Tk.Scrollbar(fpane,name='findBar')
		cBar = Tk.Scrollbar(cpane,name='changeBar')
		
		# Add scrollbars.
		for bar,txt in ((fBar,ftxt),(cBar,ctxt)):
			txt['yscrollcommand'] = bar.set
			bar['command'] = txt.yview
			bar.pack(side="right", fill="y")
		
		flab.pack(side="left")
		clab.pack(side="left")
		ctxt.pack(side="right", expand=1, fill="both")
		ftxt.pack(side="right", expand=1, fill="both")
		#@nonl
		#@-node:<< Create the Find and Change panes >>
		#@nl
		#@	<< Create four columns of radio and checkboxes >>
		#@+node:<< Create four columns of radio and checkboxes >>
		columnsFrame = Tk.Frame(outer,relief="groove",bd=2)
		columnsFrame.pack(anchor="e",expand=1,padx="7m",pady="2m") # Don't fill.
		
		numberOfColumns = 4 # Number of columns
		columns = [] ; radioLists = [] ; checkLists = []
		for i in xrange(numberOfColumns):
			columns.append(Tk.Frame(columnsFrame,bd=1))
			radioLists.append([])
			checkLists.append([])
		
		for i in xrange(numberOfColumns):
			columns[i].pack(side="left",padx="1m") # fill="y" Aligns to top. padx expands columns.
		
		radioLists[0] = [
			(self.dict["radio-find-type"],"Plain Search","plain-search"),  
			(self.dict["radio-find-type"],"Pattern Match Search","pattern-search"),
			(self.dict["radio-find-type"],"Script Search",None)] #"script-search")]
		checkLists[0] = [
			("Script Change",None)] # self.dict["script_change"]),]
		checkLists[1] = [
			("Whole Word",  self.dict["whole_word"]),
			("Ignore Case", self.dict["ignore_case"]),
			("Wrap Around", self.dict["wrap"]),
			("Reverse",     self.dict["reverse"])]
		radioLists[2] = [
			(self.dict["radio-search-scope"],"Entire Outline","entire-outine"),
			(self.dict["radio-search-scope"],"Suboutline Only","suboutline-only"),  
			(self.dict["radio-search-scope"],"Node Only","snode-only"),           
			(self.dict["radio-search-scope"],"Selection Only",None)] # "selected-text-only")]
		checkLists[2] = []
		checkLists[3] = [
			("Search Headline Text", self.dict["search_headline"]),
			("Search Body Text",     self.dict["search_body"]),
			("Mark Finds",           self.dict["mark_finds"]),
			("Mark Changes",         self.dict["mark_changes"])]
		
		for i in xrange(numberOfColumns):
			for var,name,val in radioLists[i]:
				box = Tk.Radiobutton(columns[i],anchor="w",text=name,variable=var,value=val)
				box.pack(fill="x")
				box.bind("<1>", self.resetWrap)
				if val == None: box.configure(state="disabled")
			for name, var in checkLists[i]:
				box = Tk.Checkbutton(columns[i],anchor="w",text=name,variable=var)
				box.pack(fill="x")
				box.bind("<1>", self.resetWrap)
				if var == None: box.configure(state="disabled")
		#@nonl
		#@-node:<< Create four columns of radio and checkboxes >>
		#@nl
		#@	<< Create two rows of buttons >>
		#@+node:<< Create two rows of buttons >>
		# Create the button panes
		buttons  = Tk.Frame(outer,bd=1)
		buttons2 = Tk.Frame(outer,bd=1)
		buttons.pack (anchor="n",expand=1,fill="x")
		buttons2.pack(anchor="n",expand=1,fill="x")
		
		# Create the first row of buttons
		findButton=Tk.Button(buttons,width=8,text="Find",command=self.findButton)
		contextBox=Tk.Checkbutton(buttons,anchor="w",text="Show Context",variable=self.dict["batch"])
		findAllButton=Tk.Button(buttons,width=8,text="Find All",command=self.findAllButton)
		
		findButton.pack   (pady="1m",padx="25m",side="left")
		contextBox.pack   (pady="1m",          side="left",expand=1)
		findAllButton.pack(pady="1m",padx="25m",side="right",fill="x",)
		
		# Create the second row of buttons
		changeButton    =Tk.Button(buttons2,width=8,text="Change",command=self.changeButton)
		changeFindButton=Tk.Button(buttons2,        text="Change, Then Find",command=self.changeThenFindButton)
		changeAllButton =Tk.Button(buttons2,width=8,text="Change All",command=self.changeAllButton)
		
		changeButton.pack    (pady="1m",padx="25m",side="left")
		changeFindButton.pack(pady="1m",          side="left",expand=1)
		changeAllButton.pack (pady="1m",padx="25m",side="right")
		#@nonl
		#@-node:<< Create two rows of buttons >>
		#@nl
		
		self.find_text.bind  ("<1>", self.resetWrap)
		self.change_text.bind("<1>", self.resetWrap)
		self.find_text.bind  ("<Key>", self.resetWrap)
		self.change_text.bind("<Key>", self.resetWrap)
	#@-node:find.createFrame
	#@+node:find.init
	def init (self,c):
	
		# N.B.: separate c.ivars are much more convenient than a dict.
		for key in self.intKeys:
			val = getattr(c, key + "_flag")
			self.dict[key].set(val)
			# trace(key,val)
	
		#@	<< set widgets >>
		#@+node:<< set widgets >>
		self.find_text.delete("1.0","end")
		self.find_text.insert("end",c.find_text)
		
		self.change_text.delete("1.0","end")
		self.change_text.insert("end",c.change_text)
		#@nonl
		#@-node:<< set widgets >>
		#@nl
		
		# Set radio buttons from ivars.
		val = self.dict["pattern_match"].get()
		self.dict["radio-find-type"].set(
			choose(val,"pattern-search","plain-search"))
	
		val = self.dict["suboutline_only"].get()
		self.dict["radio-search-scope"].set(
			choose(val,"suboutline-only","entire-outine"))
	#@nonl
	#@-node:find.init
	#@+node:find.set_ivars
	def set_ivars (self,c):
		
		# N.B.: separate c.ivars are much more convenient than a dict.
		for key in self.intKeys:
			val = self.dict[key].get()
			setattr(c, key + "_flag", val)
			# trace(key,val)
	
		# Set ivars from radio buttons.
		c.pattern_match_flag   = self.dict["radio-find-type"].get()    == "pattern-search"
		c.suboutline_only_flag = self.dict["radio-search-scope"].get() == "suboutline-only"
	
		s = self.find_text.get("1.0","end - 1c") # Remove trailing newline
		s = toUnicode(s,app().tkEncoding) # 2/25/03
		c.find_text = s
	
		s = self.change_text.get("1.0","end - 1c") # Remove trailing newline
		s = toUnicode(s,app().tkEncoding) # 2/25/03
		c.change_text = s
	#@nonl
	#@-node:find.set_ivars
	#@+node:changeButton
	
	# The user has pushed the "Change" button from the find panel.
	
	def changeButton(self):
	
		self.setup_button()
		self.change()
	#@nonl
	#@-node:changeButton
	#@+node:changeAllButton
	# The user has pushed the "Change All" button from the find panel.
	
	def changeAllButton(self):
	
		c = self.setup_button()
		c.clearAllVisited() # Clear visited for context reporting.
		self.changeAll()
	#@nonl
	#@-node:changeAllButton
	#@+node:changeThenFindButton
	# The user has pushed the "Change Then Find" button from the find panel.
	
	def changeThenFindButton(self):
	
		self.setup_button()
		self.changeThenFind()
	#@nonl
	#@-node:changeThenFindButton
	#@+node:findButton
	# The user has pushed the "Find" button from the find panel.
	
	def findButton(self):
	
		self.setup_button()
		self.findNext()
	#@nonl
	#@-node:findButton
	#@+node:findAllButton
	# The user has pushed the "Find All" button from the find panel.
	
	def findAllButton(self):
	
		c = self.setup_button()
		c.clearAllVisited() # Clear visited for context reporting.
		self.findAll()
	#@nonl
	#@-node:findAllButton
	#@+node:changeCommand
	# The user has selected the "Replace" menu item.
	
	def changeCommand(self,c):
	
		self.setup_command(c)
		self.change()
	#@nonl
	#@-node:changeCommand
	#@+node:changeThenFindCommandd
	# The user has pushed the "Change Then Find" button from the Find menu.
	
	def changeThenFindCommand(self,c):
	
		self.setup_command(c)
		self.changeThenFind()
	#@nonl
	#@-node:changeThenFindCommandd
	#@+node:findNextCommand
	# The user has selected the "Find Next" menu item.
	
	def findNextCommand(self,c):
	
		self.setup_command(c)
		self.findNext()
	#@nonl
	#@-node:findNextCommand
	#@+node:fndPreviousCommand
	# The user has selected the "Find Previous" menu item.
	
	def findPreviousCommand(self,c):
	
		self.setup_command(c)
		c.reverse_flag = not c.reverse_flag
		self.findNext()
		c.reverse_flag = not c.reverse_flag
	#@nonl
	#@-node:fndPreviousCommand
	#@+node:setup_button
	# Initializes a search when a button is pressed in the Find panel.
	
	def setup_button(self):
	
		self.commands = c = app().log.commands
		self.v = c.currentVnode()
		assert(c)
		c.bringToFront()
		if 0: # We _must_ retain the editing status for incremental searches!
			c.endEditing()
		c.setIvarsFromFind()
		return c
	#@nonl
	#@-node:setup_button
	#@+node:setup_command
	# Initializes a search when a command is invoked from the menu.
	
	def setup_command(self,c):
	
		self.commands = c
		self.v = c.currentVnode()
		if 0: # We _must_ retain the editing status for incremental searches!
			c.endEditing()
		c.setIvarsFromFind()
	#@nonl
	#@-node:setup_command
	#@+node:batchChange
	#@+at 
	#@nonl
	# This routine performs a single batch change operation, updating the head 
	# or body string of v and leaving the result in s_text.  We update the 
	# c.body if we are changing the body text of c.currentVnode().
	# 
	# s_text contains the found text on entry and contains the changed text on 
	# exit.  pos and pos2 indicate the selection.  The selection will never be 
	# empty. NB: we can not assume that self.v is visible.
	#@-at
	#@@c
	
	def batchChange (self,pos1,pos2,count):
	
		c = self.commands ; v = self.v ; st = self.s_text
		# Replace the selection with c.change_text
		if st.compare(pos1, ">", pos2):
			pos1,pos2=pos2,pos1
		st.delete(pos1,pos2)
		st.insert(pos1,c.change_text)
		s = getAllText(st)
		# Update the selection.
		insert=choose(c.reverse_flag,pos1,pos1+'+'+`len(c.change_text)`+'c')
		st.tag_remove("sel","1.0","end")
		st.mark_set("insert",insert)
		# trace("result:" + `insert` + ", " + `s`)
		# Update the node
		if self.in_headline:
			#@		<< set the undo head params >>
			#@+node:<< set the undo head params >>
			sel = None
			if len(s) > 0 and s[-1]=='\n': s = s[:-1]
			if s != v.headString():
				if count == 1:
					c.undoer.setUndoParams("Change All",v) # Tag the start of the Change all.
				c.undoer.setUndoTypingParams(v,"Change Headline",v.bodyString(),s,sel,sel)
			#@nonl
			#@-node:<< set the undo head params >>
			#@nl
			v.initHeadString(s)
		else:
			#@		<< set the undo body typing params >>
			#@+node:<< set the undo body typing params >>
			sel = c.body.index("insert")
			if len(s) > 0 and s[-1]=='\n': s = s[:-1]
			if s != v.bodyString():
				if count == 1:
					c.undoer.setUndoParams("Change All",v) # Tag the start of the Change all.
				c.undoer.setUndoTypingParams(v,"Change",v.bodyString(),s,sel,sel)
			#@nonl
			#@-node:<< set the undo body typing params >>
			#@nl
			v.setBodyStringOrPane(s)
		# Set mark, changed and dirty bits.
		if c.mark_changes_flag:
			v.setMarked()
		if not c.isChanged():
			c.setChanged(true)
		v.setDirty()
	#@nonl
	#@-node:batchChange
	#@+node:change
	def change(self):
	
		if self.checkArgs():
			self.initInHeadline()
			self.changeSelection()
	#@nonl
	#@-node:change
	#@+node:changeAll
	def changeAll(self):
	
		c = self.commands ; st = self.s_text
		if not self.checkArgs():
			return
		self.initInHeadline()
		data = self.save()
		self.initBatchCommands()
		count = 0
		c.beginUpdate()
		while 1:
			pos1, pos2 = self.findNextMatch()
			if pos1:
				count += 1
				self.batchChange(pos1,pos2,count)
				line = st.get(pos1 + " linestart", pos1 + " lineend")
				line = toUnicode(line,app().tkEncoding) # 9/28/03
				self.printLine(line,allFlag=true)
			else: break
		c.endUpdate() # self.restore
		# Make sure the headline and body text are updated.
		v = c.currentVnode()
		c.tree.onHeadChanged(v)
		c.tree.onBodyChanged(v,"Can't Undo")
		if count > 0:
			# A change was made.  Tag the end of the Change All command.
			c.undoer.setUndoParams("Change All",v)
		es("changed: " + `count`)
		self.restore(data)
	#@nonl
	#@-node:changeAll
	#@+node:changeSelection
	# Replace selection with c.change_text.
	# If no selection, insert c.change_text at the cursor.
	
	def changeSelection(self):
		
		c = self.commands ; v = self.v
		# trace(`self.in_headline`)
		t = choose(self.in_headline,v.edit_text(),c.body)
		oldSel = sel = t.tag_ranges("sel")
		if len(sel) == 2:
			start,end = sel
			if start == end:
				sel = None
		if len(sel) != 2:
			es("No text selected")
			return false
		# trace(`sel` + ", " + `c.change_text`)
		# Replace the selection
		start,end = oldSel
		t.delete(start,end)
		t.insert(start,c.change_text)
		# 2/7/02: Also update s_text in case we find another match on the same line.
		self.s_text.delete(start,end)
		self.s_text.insert(start,c.change_text)
		# Update the selection for the next match.
		setTextSelection(t,start,start + "+" + `len(c.change_text)` + "c")
		newSel = getTextSelection(t)
		set_focus(c,t)
	
		c.beginUpdate()
		if c.mark_changes_flag:
			v.setMarked()
			c.tree.drawIcon(v,v.iconx,v.icony) # redraw only the icon.
		# update node, undo status, dirty flag, changed mark & recolor
		if self.in_headline:
			c.tree.idle_head_key(v)
		else:
			c.tree.onBodyChanged(v,"Change",oldSel=oldSel,newSel=newSel)
		c.endUpdate(false) # No redraws here: they would destroy the headline selection.
		# trace(c.body.index("insert")+":"+c.body.get("insert linestart","insert lineend"))
		return true
	#@nonl
	#@-node:changeSelection
	#@+node:changeThenFind
	def changeThenFind(self):
	
		if not self.checkArgs():
			return
	
		self.initInHeadline()
		if self.changeSelection():
			self.findNext(false) # don't reinitialize
	#@nonl
	#@-node:changeThenFind
	#@+node:findAll
	def findAll(self):
	
		c = self.commands ; st = self.s_text
		if not self.checkArgs():
			return
		self.initInHeadline()
		data = self.save()
		self.initBatchCommands()
		count = 0
		c.beginUpdate()
		while 1:
			pos, newpos = self.findNextMatch()
			if pos:
				count += 1
				line = st.get(pos + " linestart", pos + " lineend")
				line = toUnicode(line,app().tkEncoding) # 9/28/03
				self.printLine(line,allFlag=true)
			else: break
		c.endUpdate()
		es("found: " + `count`)
		self.restore(data)
	#@nonl
	#@-node:findAll
	#@+node:findNext
	def findNext(self,initFlag = true):
	
		c = self.commands
		if not self.checkArgs():
			return
			
		if initFlag:
			self.initInHeadline()
			data = self.save()
			self.initInteractiveCommands()
		else:
			data = self.save()
		
		c.beginUpdate()
		pos, newpos = self.findNextMatch()
		c.endUpdate(false) # Inhibit redraws so that headline remains selected.
		
		if pos:
			self.showSuccess(pos,newpos)
		else:
			if self.wrapping:
				es("end of wrapped search")
			else:
				es("not found: " + "'" + c.find_text + "'")
			self.restore(data)
	#@nonl
	#@-node:findNext
	#@+node:findNextMatch
	# Resumes the search where it left off.
	# The caller must call set_first_incremental_search or set_first_batch_search.
	
	def findNextMatch(self):
	
		c = self.commands
	
		if not c.search_headline_flag and not c.search_body_flag:
			return None, None
	
		if len(c.find_text) == 0:
			return None, None
			
		v = self.v
		while v:
			pos, newpos = self.search()
			if pos:
				if c.mark_finds_flag:
					v.setMarked()
					c.tree.drawIcon(v,v.iconx,v.icony) # redraw only the icon.
				return pos, newpos
			elif c.node_only_flag:
				# We are only searching one node.
				return None,None
			else:
				v = self.v = self.selectNextVnode()
		return None, None
	#@nonl
	#@-node:findNextMatch
	#@+node:selectNextVnode
	# Selects the next node to be searched.
	
	def selectNextVnode(self):
	
		c = self.commands ; v = self.v
		# trace(`v`)
		
		# Start suboutline only searches.
		if c.suboutline_only_flag and not self.onlyVnode:
			self.onlyVnode = v
	
		# Start wrapped searches.
		if self.wrapping and not self.wrapVnode:
			assert(self.wrapPos != None)
			self.wrapVnode = v
	
		if self.in_headline and c.search_body_flag:
			# just switch to body pane.
			self.in_headline = false
			self.initNextText()
			# trace(`v`)
			return v
	
		if c.reverse_flag:
			v = v.threadBack()
		else:
			v = v.threadNext()
	
		# Wrap if needed.
		if not v and self.wrapping and not c.suboutline_only_flag:
			v = c.rootVnode()
			if c.reverse_flag:
				# Set search_v to the last node of the tree.
				while v and v.next():
					v = v.next()
				if v: v = v.lastNode()
	
		# End wrapped searches.
		if self.wrapping and v and v == self.wrapVnode:
			# trace("ending wrapped search")
			v = None ; self.resetWrap()
			
		# End suboutline only searches.
		if (c.suboutline_only_flag and self.onlyVnode and v and
			(v == self.onlyVnode or not self.onlyVnode.isAncestorOf(v))):
			# trace("end outline-only")
			v = None ; self.onlyVnode = None
	
		self.v = v # used in initNextText().
		if v: # select v and set the search point within v.
			self.in_headline = c.search_headline_flag
			self.initNextText()
		return v
	#@nonl
	#@-node:selectNextVnode
	#@+node:search
	#@+at 
	#@nonl
	# Searches the present headline or body text for c.find_text and returns 
	# true if found.
	# c.whole_word_flag, c.ignore_case_flag, and c.pattern_match_flag control 
	# the search.
	#@-at
	#@@c
	
	def search (self):
	
		c = self.commands ; v = self.v ; t = self.s_text
		assert(c and t and v)
		index = t.index("insert")
		stopindex = choose(c.reverse_flag,"1.0","end")
		while 1:
			# trace(`index`+":"+`stopindex`+":"+t.get(index+" linestart",index+" lineend"))
			pos = t.search(c.find_text,index,
				stopindex=stopindex,backwards=c.reverse_flag,
				regexp=c.pattern_match_flag,nocase=c.ignore_case_flag)
			if not pos:
				return None, None
			newpos = pos + "+" + `len(c.find_text)` + "c"
			if c.reverse_flag and t.compare(newpos,"==",index): # 10/3/02
				#@			<< search again after getting stuck going backward >>
				#@+node:<< search again after getting stuck going backward >>
				# print "stuck"
				index = newpos + "-" + `len(c.find_text)` + "c"
				pos = t.search(c.find_text,index,
					stopindex=stopindex,backwards=c.reverse_flag,
					regexp=c.pattern_match_flag,nocase=c.ignore_case_flag)
				
				if not pos:
					return None, None
				newpos = pos + "+" + `len(c.find_text)` + "c"
				#@nonl
				#@-node:<< search again after getting stuck going backward >>
				#@nl
			# trace(`pos`+":"+`newpos`)
			#@		<< return if we are passed the wrap point >>
			#@+node:<< return if we are passed the wrap point >>
			if self.wrapping and self.wrapPos and self.wrapVnode and self.v == self.wrapVnode:
				if c.reverse_flag and t.compare(pos, "<", self.wrapPos):
					# trace("wrap done")
					return None, None
				if not c.reverse_flag and t.compare(newpos, ">", self.wrapPos):
					return None, None
			#@nonl
			#@-node:<< return if we are passed the wrap point >>
			#@nl
			if c.whole_word_flag:
				index = t.index(choose(c.reverse_flag,pos,newpos))
				#@			<< test for whole word match >>
				#@+node:<< test for whole word match >>
				# Set pos to None if word characters preceed or follow the selection.
				
				before = t.get(pos + "-1c", pos)
				first  = t.get(pos)
				last   = t.get(newpos)
				after  = t.get(newpos, newpos + "+1c")
				
				before = toUnicode(before,app().tkEncoding) # 9/28/03
				first  = toUnicode(first, app().tkEncoding) # 9/28/03
				last   = toUnicode(last,  app().tkEncoding) # 9/28/03
				after  = toUnicode(after, app().tkEncoding) # 9/28/03
				
				# print before, first, last, after
				
				if before and is_c_id(before) and first and is_c_id(first):
					pos = None
				if after  and is_c_id(after)  and last  and is_c_id(last):
					pos = None
				#@nonl
				#@-node:<< test for whole word match >>
				#@nl
				if not pos: continue
			# trace("found:" + `pos` + ":" + `newpos` + ":" + `v`)
			# set the insertion point.
			setTextSelection(t,pos,newpos)
			t.mark_set("insert",choose(c.reverse_flag,pos,newpos))
			return pos, newpos
	#@nonl
	#@-node:search
	#@+node:checkArgs
	def checkArgs (self):
	
		c = self.commands 
		val = true
		if not c.search_headline_flag and not c.search_body_flag:
			es("not searching headline or body")
			val = false
		if len(c.find_text) == 0:
			es("empty find patttern")
			val = false
		return val
	#@nonl
	#@-node:checkArgs
	#@+node:initBatchCommands
	# Initializes for the Find All and Change All commands.
	
	def initBatchCommands (self):
	
		c = self.commands
		self.in_headline = c.search_headline_flag # Search headlines first.
	
		# Select the first node.
		if c.suboutline_only_flag:
			self.v = c.currentVnode()
		else:
			v = c.rootVnode()
			if c.reverse_flag:
				while v and v.next():
					v = v.next()
				v = v.lastNode()
			self.v = v
		
		# Set the insert point.
		self.initBatchText()
	#@nonl
	#@-node:initBatchCommands
	#@+node:initBatchText & initNextText
	#@+at 
	#@nonl
	# Returns s_text with "insert" point set properly for batch searches.
	#@-at
	#@@c
	
	def initBatchText(self):
		c = self.commands ; v = self.v ; st = self.s_text	
		s = choose(self.in_headline,v.headString(), v.bodyString())
		st.delete("1.0","end")
		st.insert("end",s)
		st.mark_set("insert",choose(c.reverse_flag,"end","1.0"))
		self.wrapping = false # Only interactive commands allow wrapping.
		return st
	
	# Call this routine when moving to the next node when a search fails.
	# Same as above except we don't reset wrapping flag.
	def initNextText(self):
		c = self.commands ; v = self.v ; st = self.s_text	
		s = choose(self.in_headline,v.headString(), v.bodyString())
		st.delete("1.0","end")
		st.insert("end",s)
		st.mark_set("insert",choose(c.reverse_flag,"end","1.0"))
		return st
	#@nonl
	#@-node:initBatchText & initNextText
	#@+node:initInHeadline
	# Guesses which pane to start in for incremental searches and changes.
	# This must not alter the current "insert" or "sel" marks.
	
	def initInHeadline (self):
	
		c = self.commands ; v = self.v
		
		if c.search_headline_flag and c.search_body_flag:
			# Do not change this line without careful thought and extensive testing!
			self.in_headline = (v == c.tree.editVnode)
		else:
			self.in_headline = c.search_headline_flag
	#@nonl
	#@-node:initInHeadline
	#@+node:initInteractiveCommands
	# For incremental searches
	
	def initInteractiveCommands(self):
	
		c = self.commands ; v = self.v
		
		if self.in_headline:
			t = v.edit_text()
			c.tree.editVnode = v
			pos = t.index("insert")
			# trace(`pos` + ":" + `self.in_headline` + ":" + `v==c.tree.editVnode` + ":" + `v`)
		else:
			t = c.body
			pos = t.index("insert")
	
		st = self.initNextText()
		set_focus(c,t)
		st.mark_set("insert",pos)
		self.wrapping = c.wrap_flag
		if c.wrap_flag and self.wrapVnode == None:
			self.wrapPos = pos
			# Do not set self.wrapVnode here: that must be done after the first search.
	#@nonl
	#@-node:initInteractiveCommands
	#@+node:printLine
	def printLine (self,line,allFlag=false):
	
		c = self.commands
		both = c.search_body_flag and c.search_headline_flag
		context = c.batch_flag # "batch" now indicates context
	
		if allFlag and both and context:
			es(`self.v`)
			type = choose(self.in_headline,"head: ","body: ")
			es(type + line)
		elif allFlag and context and not self.v.isVisited():
			# We only need to print the context once.
			es(`self.v`)
			es(line)
			self.v.setVisited()
		else:
			es(line)
	#@nonl
	#@-node:printLine
	#@+node:restore
	# Restores the screen after a search fails
	
	def restore (self,data):
	
		c = self.commands
		in_headline,v,t,insert,start,end = data
		# trace(`insert` + ":" + `start` + ":" + `end`)
		# Don't try to reedit headline.
		c.selectVnode(v) 
		if not in_headline:
			if 0: # Looks bad.
				if start and end:
					setTextSelection(t,start,end)
			else: # Looks good and provides clear indication of failure or termination.
				t.tag_remove("sel","1.0","end")
			t.mark_set("insert",insert)
			t.see("insert")
			set_focus(c,t)
	#@nonl
	#@-node:restore
	#@+node:save
	def save (self):
	
		c = self.commands ; v = self.v
		t = choose(self.in_headline,v.edit_text(),c.body)
		insert = t.index("insert")
		sel = t.tag_ranges("sel")
		if len(sel) == 2:
			start,end = sel
		else:
			start,end = None,None
		return (self.in_headline,v,t,insert,start,end)
	#@nonl
	#@-node:save
	#@+node:showSuccess
	#@+at 
	#@nonl
	# This is used for displaying the final result.  It returns 
	# self.dummy_vnode, v.edit_text() or c.body with "insert" and "sel" points 
	# set properly.
	#@-at
	#@@c
	
	def showSuccess(self,pos,newpos):
	
		c = self.commands ; v = self.v
		
		c.beginUpdate() # Prevent all redraws except c.tree.redraw_now()
		if 1: # range of update...
			c.selectVnode(v)
			c.tree.redraw_now() # Redraw now so selections are not destroyed.
			# Select the found vnode again after redraw.
			if self.in_headline:
				c.editVnode(v)
				c.tree.setNormalLabelState(v)
				assert(v.edit_text())
			else:
				c.selectVnode(v)
		c.endUpdate(false) # Do not draw again!
	
		t = choose(self.in_headline,v.edit_text(),c.body)
		# trace(`self.in_headline` + "," + `t`)
		insert = choose(c.reverse_flag,pos,newpos)
		t.mark_set("insert",insert)
		setTextSelection(t,pos,newpos)
		if not self.in_headline:
			t.see(insert)
		set_focus(c,t)
		if c.wrap_flag and not self.wrapVnode:
			self.wrapVnode = self.v
	#@nonl
	#@-node:showSuccess
	#@-others
#@nonl
#@-node:class leoFind
#@-others
#@nonl
#@-node:@file leoFind.py
#@-leo
