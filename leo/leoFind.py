#@+leo

#@+node:0::@file leoFind.py

#@+body

#@<< Theory of operation >>

#@+node:1:C=1:<< Theory of operation >>

#@+body

#@+at
#  The find command is surprisingly tricky; there are many details that must be handled properly.  This documentation states some 
# important design principles and discusses some code details.
# 
# 
# Design Principles:
# 
# The following principles influence all aspects of the Find class:
# 
# 1. Find and Change commands initialize themselves using only the state of the present Leo window. In particular, the Find class 
# must not save internal state inforamtion from one invocation to the next.  This means that when the user changes the nodes, or 
# selects new text in headline or body text, those changes will affect the next invocation of any Find or Change command.  Failure 
# to follow this cardinal principle caused all kinds of problems in the Borland and Macintosh code.
# 
# This principle simplifies the code somewhat because ivars do not persist.  OTOH, each command must ensure that the Leo window is 
# left in a state suitable for restarting the incremental(interactive) Find and Change commands.  Initialization is by far the 
# most tricky aspect of the Find class.  Details are discussed below in the "About Initialization" section.
# 
# There is one exception to this rule. We must remember where interactive wrapped searches start. We clear self.wrapVnode when the 
# Find panel changes.  Interactive searches set and clear these persistent ivars as needed.
# 
# 2. Commands must not change the state of the outline or body pane during execution: that would cause severe flashing and slow 
# down the commands a great deal.  In particular, c.selectVnode() and c.editVnode() must not be called while looking for matches.  
# This has several important consequences, discussed below in the About Searching section.
# 
# 3.  The Find All and Change All commands always restore the Leo window to its state on entry.  Incremental commands restore the 
# Leo window to its state on entry if no match is found.  The save and restore routines do this.
# 
# About Initialization
# 
# The setup_commands() and setup_buttons() methods perform common initialization for menu commands and Find panel buttons 
# respectively.  The initBatchCommands(), initInteractiveCommands() and initInHeadline() methods handle details of 
# initialization.  Initialization involves setting the self.c, self.v, self.in_headline, self.wrapping and self.s_text ivars.  
# Setting self.in_headline is tricky: we must be sure to retain the state of the outline pane until initialization is complete.  
# Initializing the Find All and Change All commands is much easier than initializing incremental Find or Change commands because 
# such initialization does not depend greatly on the state of the Leo window.
# 
# About Searching
# 
# Using Tk.Text widgets for both headlines and body text results in a _huge_ simplification of the code.  The actual searching 
# takes place in the search() method.  search() must not assume that c.currentVnode() is the current node to be searched.  
# Instead, search() assumes that:
# 
# 1. self.s_text is a Tk.Text widget that contains the text to be searched or changed.
# 2. The "insert" and "sel" attributes of self.search_text indicate the range of text to be searched.
# 
# The selectNextVnode() method handles the many details of selecting the next node to be searched.  selectNextVnode() and its 
# allies set self.s_text, including its "insert" and "sel" attributes.
# 
# The actual searching is easy: search() just calls the Tk search_text.search() method.
# 
# About Finalization
# 
# When incremental Find or Change commands succeeed they must leave the Leo window in the proper state to execute another 
# incremental command.  The showSuccess() method does this.  show_success() calls c.currentVnode() or c.editVnode and set the 
# insertion point and the range of selected text.
# 
# We restore the Leo window as it was on entry whenever an incremental search fails and after any Find All and Change All 
# command.  The save() and restore() methods do this.

#@-at

#@-body

#@-node:1:C=1:<< Theory of operation >>


from leoGlobals import *
from leoUtils import *
import Tkinter

# Abbreviations
set_undo_params = true ; dont_set_undo_params = false
all = true

#define is_word(c)(isalnum(c)or(c)== '_')

# The names of the actual ivars have "_flag" appended to these.
# Note: batch_flag now records the "context" checkbox.
ivars = [ "batch", "wrap", "whole_word", "ignore_case",
	"pattern_match", "search_headline", "search_body",
	"suboutline_only", "mark_changes", "mark_finds", "reverse" ]

class LeoFind:

	#@+others

	#@+node:2:C=2:find.__init__

	#@+body
	def __init__(self):
	
		Tk=Tkinter
		
	#@<< Initialize the leoFind ivars >>

		#@+node:1::<< Initialize the leoFind ivars >>

		#@+body
		# Initialize the ivars for the find panel.
		for var in ivars:
			exec ("self.%s_flag = Tk.IntVar()" % var)
			
		# The c.x_flag ivars contain the user preferences.
		# These are updated just before executing any find/change command.
		
		# Ivars containing internal state...
		self.commands = None # The commander for this search.
		self.v = None # The vnode being searched.  Never saved between searches!
		self.in_headline = false # true: searching headline text.
		self.wrapping = false # true: wrapping is enabled. _not_ the same as c.wrap_flag for batch searches.
		self.s_text = Tk.Text() # Used by find.search()
		

		#@+at
		#  Initializing a wrapped search is tricky.  The search() method will fail if v==wrapVnode and pos >= wrapPos.  
		# selectNextVnode() will fail if v == wrapVnode.  We set wrapPos on entry, before the first search.  We set wrapVnode in 
		# selectNextVnode after the first search fails.  We also set wrapVnode on exit if the first search suceeds.

		#@-at

		#@@c
		self.wrapVnode = None # The start of wrapped searches: persists between calls.
		self.onlyVnode = None # The starting node for suboutline-only searches.
		self.wrapPos = None # The starting position of the wrapped search: persists between calls.
		#@-body

		#@-node:1::<< Initialize the leoFind ivars >>

		self.top = top = Tk.Toplevel()
		top.title("Leo Find/Change")
		top.resizable(0,0) # neither height or width is resizable.
		# self.top.SetIcon("LeoIcon")
	
		# Create the find panel...
		
	#@<< Create the Find and Change panes >>

		#@+node:2::<< Create the Find and Change panes >>

		#@+body
		fc = Tk.Frame(top, bd="1m")
		fc.pack(anchor="n", fill="x", expand=1)
		
		fpane = Tk.Frame(fc, borderwidth=1, height="0.95i", width="1.5i")
		cpane = Tk.Frame(fc, borderwidth=1, height="0.95i", width="1.5i")
		
		fpane.pack(anchor="n", expand=1, fill="x")
		cpane.pack(anchor="s", expand=1, fill="x")
		
		# Create the labels and text fields...
		flab = Tk.Label(fpane, width=8, text="Find:")
		clab = Tk.Label(cpane, width=8, text="Change:")
		self.find_text   = ftxt = Tk.Text(fpane, height=2, width=20)
		self.change_text = ctxt = Tk.Text(cpane, height=2, width=20)
		
		flab.pack(side="left")
		clab.pack(side="left")
		ctxt.pack(side="right", expand=1, fill="both")
		ftxt.pack(side="right", expand=1, fill="both")
		#@-body

		#@-node:2::<< Create the Find and Change panes >>

		
	#@<< Create two columns of checkboxes >>

		#@+node:3::<< Create two columns of checkboxes >>

		#@+body
		boxes = Tk.Frame(top, bd="1m")
		boxes.pack(anchor="n", expand=1, fill="x")
		
		lt = Tk.Frame(boxes, bd=1)
		rt = Tk.Frame(boxes, bd=1)
		lt.pack(side="left", padx="5m")
		rt.pack(side="right", ipadx="2m")
		
		lt_list = [
			("Show Context", "batch"), # batch flag now records Show context.
			("Wrap Around", "wrap"), ("Whole Word", "whole_word"),
			("Ignore Case", "ignore_case"),("Pattern Match", "pattern_match") ]
		
		rt_list = [ ("Search Headline Text", "search_headline"),
			("Search Body Text", "search_body"), ("Suboutline Only", "suboutline_only"),
			("Mark Changes", "mark_changes"), ("Mark Finds", "mark_finds") ]
		
		for name, var in lt_list:
			exec ( 'box = Tk.Checkbutton(lt, anchor="w", text="' + name +
				'", variable=self.' + var + "_flag)" )
			box.pack(fill="x")
			box.bind("<1>", self.resetWrap)
			
		for name, var in rt_list:
			exec ( 'box = Tk.Checkbutton(rt, anchor="w", text="' + name +
				'", variable=self.' + var + "_flag)" )
			box.pack(fill="x")
			box.bind("<1>", self.resetWrap)
		#@-body

		#@-node:3::<< Create two columns of checkboxes >>

		
	#@<< Create two rows of buttons >>

		#@+node:4::<< Create two rows of buttons >>

		#@+body
		# Create the button panes
		buttons  = Tk.Frame(top, bd=1)
		buttons2 = Tk.Frame(top, bd=1)
		buttons.pack (anchor="n", expand=1, fill="x")
		buttons2.pack(anchor="n", expand=1, fill="x")
		
		# Create the first row of buttons
		findButton   =Tk.Button     (buttons,width=8,text="Find",command=self.findButton)
		reverseBox   =Tk.Checkbutton(buttons,width=8,text="Reverse",variable=self.reverse_flag)
		findAllButton=Tk.Button     (buttons,width=8,text="Find All",command=self.findAllButton)
		
		reverseBox.bind("<1>", self.resetWrap)
		
		findButton.pack   (pady="1m",padx="1m",side="left")
		reverseBox.pack   (pady="1m",          side="left",expand=1)
		findAllButton.pack(pady="1m",padx="1m",side="left")
		
		# Create the second row of buttons
		changeButton    =Tk.Button(buttons2,width=8,text="Change",command=self.changeButton)
		changeFindButton=Tk.Button(buttons2,        text="Change, Then Find",command=self.changeThenFindButton)
		changeAllButton =Tk.Button(buttons2,width=8,text="Change All",command=self.changeAllButton)
		
		changeButton.pack    (pady="1m",padx="1m",side="left")
		changeFindButton.pack(pady="1m",          side="left",expand=1)
		changeAllButton.pack (pady="1m",padx="1m",side="right")
		#@-body

		#@-node:4::<< Create two rows of buttons >>

		self.top.protocol("WM_DELETE_WINDOW", self.OnCloseFindEvent)
		self.find_text.bind  ("<1>", self.resetWrap)
		self.change_text.bind("<1>", self.resetWrap)
		self.find_text.bind  ("<Key>", self.resetWrap)
		self.change_text.bind("<Key>", self.resetWrap)
	#@-body

	#@-node:2:C=2:find.__init__

	#@+node:3:C=3:find.init

	#@+body
	def init (self,c):
	
		for var in ivars:
			exec("self.%s_flag.set(c.%s_flag)" % (var,var))
	
		
	#@<< set widgets >>

		#@+node:1::<< set widgets >>

		#@+body
		self.find_text.delete("1.0","end")
		self.find_text.insert("end",c.find_text)
		
		self.change_text.delete("1.0","end")
		self.change_text.insert("end",c.change_text)
		#@-body

		#@-node:1::<< set widgets >>

		
		# trace("__init__", "find.init")
	#@-body

	#@-node:3:C=3:find.init

	#@+node:4::find.set_ivars

	#@+body
	def set_ivars (self,c):
	
		for var in ivars:
			exec("c.%s_flag = self.%s_flag.get()" % (var,var))
	
		c.find_text = self.find_text.get("1.0","end - 1c") # Remove trailing newline
		c.change_text = self.change_text.get("1.0","end - 1c") # Remove trailing newline
	#@-body

	#@-node:4::find.set_ivars

	#@+node:5:C=4:resetWrap

	#@+body
	def resetWrap (self,event=None):
	
		self.wrapVnode = None
		self.onlyVnode = None
	#@-body

	#@-node:5:C=4:resetWrap

	#@+node:6::OnCloseFindEvent

	#@+body
	def OnCloseFindEvent(self):
	
		self.top.withdraw()
	#@-body

	#@-node:6::OnCloseFindEvent

	#@+node:7:C=5:Top Level Commands

	#@+node:1::changeButton

	#@+body
	
	# The user has pushed the "Change" button from the find panel.
	
	def changeButton(self):
	
		c = self.setup_button()
		self.change()
	#@-body

	#@-node:1::changeButton

	#@+node:2::changeAllButton

	#@+body
	# The user has pushed the "Change All" button from the find panel.
	
	def changeAllButton(self):
	
		c = self.setup_button()
		c.clearAllVisited() # Clear visited for context reporting.
		self.changeAll()
	#@-body

	#@-node:2::changeAllButton

	#@+node:3::changeThenFindButton

	#@+body
	# The user has pushed the "Change Then Find" button from the find panel.
	
	def changeThenFindButton(self):
	
		c = self.setup_button()
		self.changeThenFind()
	#@-body

	#@-node:3::changeThenFindButton

	#@+node:4::findButton

	#@+body
	# The user has pushed the "Find" button from the find panel.
	
	def findButton(self):
	
		c = self.setup_button()
		self.findNext()
	#@-body

	#@-node:4::findButton

	#@+node:5::findAllButton

	#@+body
	# The user has pushed the "Find All" button from the find panel.
	
	def findAllButton(self):
	
		c = self.setup_button()
		c.clearAllVisited() # Clear visited for context reporting.
		self.findAll()
	#@-body

	#@-node:5::findAllButton

	#@+node:6::changeCommand

	#@+body
	# The user has selected the "Replace" menu item.
	
	def changeCommand(self,c):
	
		self.setup_command(c)
		self.change()
	#@-body

	#@-node:6::changeCommand

	#@+node:7::changeThenFindCommandd

	#@+body
	# The user has pushed the "Change Then Find" button from the Find menu.
	
	def changeThenFindCommand(self,c):
	
		self.setup_command(c)
		self.changeThenFind()
	#@-body

	#@-node:7::changeThenFindCommandd

	#@+node:8::findNextCommand

	#@+body
	# The user has selected the "Find Next" menu item.
	
	def findNextCommand(self,c):
	
		self.setup_command(c)
		self.findNext()
	#@-body

	#@-node:8::findNextCommand

	#@+node:9::fndPreviousCommand

	#@+body
	# The user has selected the "Find Previous" menu item.
	
	def findPreviousCommand(self,c):
	
		self.setup_command(c)
		c.reverse_flag = not c.reverse_flag
		self.findNext()
		c.reverse_flag = not c.reverse_flag
	#@-body

	#@-node:9::fndPreviousCommand

	#@+node:10::setup_button

	#@+body
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
	#@-body

	#@-node:10::setup_button

	#@+node:11::setup_command

	#@+body
	# Initializes a search when a command is invoked from the menu.
	
	def setup_command(self,c):
	
		self.commands = c
		self.v = c.currentVnode()
		if 0: # We _must_ retain the editing status for incremental searches!
			c.endEditing()
		c.setIvarsFromFind()
	#@-body

	#@-node:11::setup_command

	#@-node:7:C=5:Top Level Commands

	#@+node:8:C=6:Utilities

	#@+node:1::batchChange

	#@+body

	#@+at
	#  This routine performs a single batch change operation, updating the head or body string of v and leaving the result in 
	# s_text.  We update the c.body if we are changing the body text of c.currentVnode().
	# 
	# s_text contains the found text on entry and contains the changed text on exit.  pos and pos2 indicate the selection.  The 
	# selection will never be empty. NB: we can not assume that self.v is visible.

	#@-at

	#@@c
	
	def batchChange (self,pos1,pos2):
	
		c = self.commands ; v = self.v ; st = self.s_text
		# Replace the selection with c.change_text
		# s = st.get("1.0","end") ; trace("entry:" + `s`)
		if st.compare(pos1, ">", pos2):
			pos1,pos2=pos2,pos1
		st.delete(pos1,pos2)
		st.insert(pos1,c.change_text)
		s = st.get("1.0","end")
		# Update the selection.
		insert=choose(c.reverse_flag,pos1,pos1+'+'+`len(c.change_text)`+'c')
		st.tag_remove("sel","1.0","end")
		st.mark_set("insert",insert)
		# trace("result:" + `insert` + ", " + `s`)
		# Update the node
		if self.in_headline:
			v.initHeadString(s)
		else:
			v.setBodyStringOrPane(s)
		# Set mark, changed and dirty bits.
		if c.mark_changes_flag:
			v.setMarked()
		if not c.isChanged():
			c.setChanged(true)
		v.setDirty()
	#@-body

	#@-node:1::batchChange

	#@+node:2::change

	#@+body
	def change(self):
	
		if self.checkArgs():
			self.initInHeadline()
			self.changeSelection()
	#@-body

	#@-node:2::change

	#@+node:3::changeAll

	#@+body
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
				self.batchChange(pos1,pos2)
				line = st.get(pos1 + " linestart", pos1 + " lineend")
				self.printLine(line,all)
			else: break
		c.endUpdate() # self.restore
		# Make sure the headline and body text are updated.
		v = c.currentVnode()
		c.tree.idle_head_key(v)
		c.tree.idle_body_key(v)
		es("changed: " + `count`)
		self.restore(data)
	#@-body

	#@-node:3::changeAll

	#@+node:4::changeSelection

	#@+body
	# Replace selection with c.change_text.
	# If no selection, insert c.change_text at the cursor.
	
	def changeSelection(self):
		
		c = self.commands ; v = self.v
		# trace(`self.in_headline`)
		t = choose(self.in_headline,v.edit_text,c.body)
		# Not yet: set undo params.
		sel = t.tag_ranges("sel")
		if len(sel) != 2:
			es("No text selected")
			return false
		# trace(`sel` + ", " + `c.change_text`)
		# Replace the selection
		start,end = sel
		t.delete(start,end)
		t.insert(start,c.change_text)
		# 2/7/02: Also update s_text in case we find another match on the same line.
		self.s_text.delete(start,end)
		self.s_text.insert(start,c.change_text)
		# Update the selection for the next match.
		setTextSelection(t,start,start + "+" + `len(c.change_text)` + "c")
		t.focus_force()
	
		c.beginUpdate()
		if c.mark_changes_flag:
			v.setMarked()
			c.tree.drawIcon(v,v.iconx,v.icony) # redraw only the icon.
		# update node, dirty flag, changed mark & recolor
		if self.in_headline:
			c.tree.idle_head_key(v)
		else:
			c.tree.idle_body_key(v)
		c.endUpdate(false) # No redraws here: they would destroy the headline selection.
		# trace(c.body.index("insert")+":"+c.body.get("insert linestart","insert lineend"))
		return true
	#@-body

	#@-node:4::changeSelection

	#@+node:5::changeThenFind

	#@+body
	def changeThenFind(self):
	
		c = self.commands
		if not self.checkArgs():
			return
	
		self.initInHeadline()
		if self.changeSelection():
			self.findNext(false) # don't reinitialize
	#@-body

	#@-node:5::changeThenFind

	#@+node:6::findAll

	#@+body
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
				self.printLine(line,all)
			else: break
		c.endUpdate()
		es("found: " + `count`)
		self.restore(data)
	#@-body

	#@-node:6::findAll

	#@+node:7::findNext

	#@+body
	def findNext(self,initFlag = true):
	
		c = self.commands ; v = self.v
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
				es("not found: " + `c.find_text`)
			self.restore(data)
	#@-body

	#@-node:7::findNext

	#@+node:8::findNextMatch

	#@+body
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
			else:
				v = self.v = self.selectNextVnode()
		return None, None
	#@-body

	#@-node:8::findNextMatch

	#@+node:9::selectNextVnode

	#@+body
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
	#@-body

	#@-node:9::selectNextVnode

	#@+node:10::search

	#@+body

	#@+at
	#  Searches the present headline or body text for c.find_text and returns true if found.
	# c.whole_word_flag, c.ignore_case_flag, and c.pattern_match_flag control the search.

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
				# trace("not found")
				return None, None
			newpos = pos + "+" + `len(c.find_text)` + "c"
			
	#@<< return if we are passed the wrap point >>

			#@+node:1::<< return if we are passed the wrap point >>

			#@+body
			if self.wrapping and self.wrapPos and self.wrapVnode and self.v == self.wrapVnode:
				if c.reverse_flag and t.compare(pos, "<", self.wrapPos):
					# trace("wrap done")
					return None, None
				if not c.reverse_flag and t.compare(newpos, ">", self.wrapPos):
					return None, None
			#@-body

			#@-node:1::<< return if we are passed the wrap point >>

			if c.whole_word_flag:
				index = t.index(choose(c.reverse_flag,pos,newpos))
				
	#@<< test for whole word match >>

				#@+node:2::<< test for whole word match >>

				#@+body
				# Set pos to None if word characters preceed or follow the selection.
				
				before = t.get(pos + "-1c", pos)
				first  = t.get(pos)
				last   = t.get(newpos)
				after  = t.get(newpos, newpos + "+1c")
				# print `before`, `first`, `last`, `after`
				
				if before and is_c_id(before) and first and is_c_id(first):
					pos = None
				if after  and is_c_id(after)  and last  and is_c_id(last):
					pos = None
				#@-body

				#@-node:2::<< test for whole word match >>

				if not pos: continue
			# trace("found:" + `pos` + ":" + `newpos` + ":" + `v`)
			# set the insertion point.
			setTextSelection(t,pos,newpos)
			t.mark_set("insert",choose(c.reverse_flag,pos,newpos))
			return pos, newpos
	#@-body

	#@-node:10::search

	#@+node:11::Initializing & finalizing & selecting

	#@+node:1::checkArgs

	#@+body
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
	#@-body

	#@-node:1::checkArgs

	#@+node:2::initBatchCommands

	#@+body
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
	#@-body

	#@-node:2::initBatchCommands

	#@+node:3::initBatchText & initNextText

	#@+body

	#@+at
	#  Returns s_text with "insert" point set properly for batch searches.

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
	#@-body

	#@-node:3::initBatchText & initNextText

	#@+node:4::initInHeadline

	#@+body
	# Guesses which pane to start in for incremental searches and changes.
	# This must not alter the current "insert" or "sel" marks.
	
	def initInHeadline (self):
	
		c = self.commands ; v = self.v
		
		if c.search_headline_flag and c.search_body_flag:
			# Do not change this line without careful thought and extensive testing!
			self.in_headline = (v == c.tree.editVnode)
		else:
			self.in_headline = c.search_headline_flag
	#@-body

	#@-node:4::initInHeadline

	#@+node:5::initInteractiveCommands

	#@+body
	# For incremental searches
	
	def initInteractiveCommands(self):
	
		c = self.commands ; v = self.v
		
		if self.in_headline:
			t = v.edit_text
			c.tree.editVnode = v
			pos = t.index("insert")
			# trace(`pos` + ":" + `self.in_headline` + ":" + `v==c.tree.editVnode` + ":" + `v`)
		else:
			t = c.body
			pos = t.index("insert")
	
		st = self.initNextText()
		t.focus_force()
		st.mark_set("insert",pos)
		self.wrapping = c.wrap_flag
		if c.wrap_flag and self.wrapVnode == None:
			self.wrapPos = pos
			# Do not set self.wrapVnode here: that must be done after the first search.
	#@-body

	#@-node:5::initInteractiveCommands

	#@+node:6::printLine

	#@+body
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
	#@-body

	#@-node:6::printLine

	#@+node:7::restore

	#@+body
	# Restores the screen after a search fails
	
	def restore (self,data):
	
		c = self.commands
		v,t,insert,start,end = data
		# trace(`insert` + ":" + `start` + ":" + `end`)
		c.selectVnode(v) # Don't try to reedit headline.
		if 0: # Looks bad.
			if start and end:
				setTextSelection(t,start,end)
		else: # Looks good and provides clear indication of failure or termination.
			t.tag_remove("sel","1.0","end")
		t.mark_set("insert",insert)
		t.see("insert")
		t.focus_force()
	#@-body

	#@-node:7::restore

	#@+node:8::save

	#@+body
	def save (self):
	
		c = self.commands ; v = self.v
		t = choose(self.in_headline,v.edit_text,c.body)
		insert = t.index("insert")
		sel = t.tag_ranges("sel")
		if len(sel) == 2:
			start,end = sel
		else:
			start,end = None,None
		return (v,t,insert,start,end)
	#@-body

	#@-node:8::save

	#@+node:9:C=7:showSuccess

	#@+body

	#@+at
	#  This is used for displaying the final result.  It returns self.dummy_vnode, v.edit_text or c.body with "insert" and "sel" 
	# points set properly.

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
				assert(v.edit_text)
			else:
				c.selectVnode(v)
		c.endUpdate(false) # Do not draw again!
	
		t = choose(self.in_headline,v.edit_text,c.body)
		# trace(`self.in_headline` + "," + `t`)
		insert = choose(c.reverse_flag,pos,newpos)
		t.mark_set("insert",insert)
		setTextSelection(t,pos,newpos)
		if not self.in_headline:
			t.see(insert)
		t.focus_force()
		if c.wrap_flag and not self.wrapVnode:
			self.wrapVnode = self.v
	#@-body

	#@-node:9:C=7:showSuccess

	#@-node:11::Initializing & finalizing & selecting

	#@-node:8:C=6:Utilities

	#@-others

#@-body

#@-node:0::@file leoFind.py

#@-leo
