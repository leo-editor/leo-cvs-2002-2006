#@+leo-ver=4
#@+node:@file leoFind.py
#@@language python

from leoGlobals import *

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

class leoFind:

	"""The base class for Leo's Find commands."""

	#@	@+others
	#@+node:leoFind.__init__
	def __init__ (self):
	
		#@	<< init the gui-independent ivars >>
		#@+node:<< init the gui-independent ivars >>
		self.wrapVnode = None
		self.onlyVnode = None
		
		# Note: the ivars have _flag appended.
		# We can't easily change this hack because the corresponding config ivars do _not_ have _flag appended.
		self.intKeys = [
			"batch", "wrap", "whole_word", "ignore_case", "node_only",
			"pattern_match", "search_headline", "search_body",
			"suboutline_only", "mark_changes", "mark_finds", "reverse",
			"script_search","script_change","selection_only"] # 11/9/03
		
		self.newStringKeys = ["radio-find-type", "radio-search-scope"]
		
		# The c.x_flag ivars contain the user preferences.
		# These are updated just before executing any find/change command.
		
		# Ivars containing internal state...
		self.c = None # The commander for this search.
		self.v = None # The vnode being searched.  Never saved between searches!
		self.in_headline = false # true: searching headline text.
		self.s_text = None # The search text for this search.
		self.wrapping = false # true: wrapping is enabled.
			# This is _not_ the same as c.wrap_flag for batch searches.
		
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
		self.errors = 0
		self.selStart = self.selEnd = None # For selection-only searches.
		#@nonl
		#@-node:<< init the gui-independent ivars >>
		#@nl
	#@nonl
	#@-node:leoFind.__init__
	#@+node:changeButton
	
	# The user has pushed the "Change" button from the find panel.
	
	def changeButton(self):
	
		c  = self.setup_button()
	
		if c.script_change_flag:
			self.doChangeScript()
		else:
			self.change()
	#@nonl
	#@-node:changeButton
	#@+node:changeAllButton
	# The user has pushed the "Change All" button from the find panel.
	
	def changeAllButton(self):
	
		c = self.setup_button()
		c.clearAllVisited() # Clear visited for context reporting.
		
		if c.script_change_flag:
			self.doChangeAllScript()
		elif c.selection_only_flag:
			self.change()
		else:
			self.changeAll()
	#@nonl
	#@-node:changeAllButton
	#@+node:changeThenFindButton
	# The user has pushed the "Change Then Find" button from the find panel.
	
	def changeThenFindButton(self):
	
		c = self.setup_button()
		
		if c.script_change_flag:
			self.doChangeScript()
			if c.script_search_flag:
				self.doFindScript()
			else:
				self.findNext()
		else:
		 	if c.script_search_flag:
				self.change()
				self.doFindScript()
			else:
				self.changeThenFind()
	#@nonl
	#@-node:changeThenFindButton
	#@+node:findButton
	# The user has pushed the "Find" button from the find panel.
	
	def findButton(self):
	
		c = self.setup_button()
		
		if c.script_search_flag:
			self.doFindScript()
		else:
			self.findNext()
	#@nonl
	#@-node:findButton
	#@+node:findAllButton
	# The user has pushed the "Find All" button from the find panel.
	
	def findAllButton(self):
	
		c = self.setup_button()
		c.clearAllVisited() # Clear visited for context reporting.
		
		if c.script_search_flag:
			self.doFindAllScript()
		elif c.selection_only_flag:
			self.findNext()
		else:
			self.findAll()
	#@nonl
	#@-node:findAllButton
	#@+node:changeCommand
	# The user has selected the "Replace" menu item.
	
	def changeCommand(self,c):
	
		self.setup_command(c)
		
		if c.script_search_flag:
			self.doChangeScript()
		else:
			self.change()
	#@nonl
	#@-node:changeCommand
	#@+node:changeThenFindCommandd
	# The user has pushed the "Change Then Find" button from the Find menu.
	
	def changeThenFindCommand(self,c):
	
		self.setup_command(c)
		
		if c.script_search_flag:
			self.doChangeScript()
			self.doFindScript()
		else:
			self.changeThenFind()
	#@nonl
	#@-node:changeThenFindCommandd
	#@+node:findNextCommand
	# The user has selected the "Find Next" menu item.
	
	def findNextCommand(self,c):
	
		self.setup_command(c)
		
		if c.script_search_flag:
			self.doFindScript()
		else:
			self.findNext()
	#@nonl
	#@-node:findNextCommand
	#@+node:fndPreviousCommand
	# The user has selected the "Find Previous" menu item.
	
	def findPreviousCommand(self,c):
	
		self.setup_command(c)
		
		c.reverse_flag = not c.reverse_flag
		
		if c.script_search_flag:
			self.doFindScript()
		else:
			self.findNext()
	
		c.reverse_flag = not c.reverse_flag
	#@nonl
	#@-node:fndPreviousCommand
	#@+node:setup_button
	# Initializes a search when a button is pressed in the Find panel.
	
	def setup_button(self):
	
		self.c = c = app.log.c ; self.v = c.currentVnode()
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
	
		self.c = c ; self.v = c.currentVnode()
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
	# body if we are changing the body text of c.currentVnode().
	# 
	# s_text contains the found text on entry and contains the changed text on 
	# exit.  pos and pos2 indicate the selection.  The selection will never be 
	# empty. NB: we can not assume that self.v is visible.
	#@-at
	#@@c
	
	def batchChange (self,pos1,pos2,count):
	
		c = self.c ; v = self.v ; st = self.s_text ; gui = app.gui
		# Replace the selection with c.change_text
		if gui.compareIndices(st,pos1, ">", pos2):
			pos1,pos2=pos2,pos1
		gui.replaceSelectionRangeWithText(st,pos1,pos2,c.change_text)
		s = gui.getAllText(st)
		# Update the selection.
		insert=choose(c.reverse_flag,pos1,pos1+'+'+`len(c.change_text)`+'c')
		gui.setSelectionRange(st,insert,insert)
		gui.setInsertPoint(st,insert)
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
			sel = c.frame.body.getInsertionPoint()
			
			if len(s) > 0 and s[-1]=='\n': s = s[:-1]
			
			if s != v.bodyString():
				if count == 1:
					c.undoer.setUndoParams("Change All",v) # Tag the start of the Change all.
					
				# 11/5/03: Changed setUndoTypingParams to setUndoParams (avoids incremental undo).
				c.undoer.setUndoParams(
					"Change",v,oldText=v.bodyString(),newText=s,oldSel=sel,newSel=sel)
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
	
		c = self.c ; st = self.s_text ; gui = app.gui
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
				line = gui.getLineContainingIndex(st,pos1)
				self.printLine(line,allFlag=true)
			else: break
		c.endUpdate()
		# Make sure the headline and body text are updated.
		v = c.currentVnode()
		c.frame.tree.onHeadChanged(v)
		c.frame.body.onBodyChanged(v,"Can't Undo")
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
		
		c = self.c ; v = self.v ; gui = app.gui
		# trace(`self.in_headline`)
		t = choose(self.in_headline,v.edit_text(),c.frame.bodyCtrl)
		oldSel = sel = gui.getTextSelection(t)
		if sel and len(sel) == 2:
			start,end = sel
			if start == end:
				sel = None
		if not sel or len(sel) != 2:
			es("No text selected")
			return false
	
		# Replace the selection in _both_ controls.
		start,end = oldSel
		gui.replaceSelectionRangeWithText(t,          start,end,c.change_text)
		gui.replaceSelectionRangeWithText(self.s_text,start,end,c.change_text)
	
		# Update the selection for the next match.
		gui.setSelectionRangeWithLength(t,start,len(c.change_text))
		newSel = gui.getTextSelection(t)
		gui.set_focus(c,t)
	
		c.beginUpdate()
		if c.mark_changes_flag:
			v.setMarked()
			c.frame.tree.drawIcon(v) # redraw only the icon.
		# update node, undo status, dirty flag, changed mark & recolor
		if self.in_headline:
			c.frame.idle_head_key(v)
		else:
			c.frame.body.onBodyChanged(v,"Change",oldSel=oldSel,newSel=newSel)
		c.endUpdate(false) # No redraws here: they would destroy the headline selection.
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
	#@+node:doChange...Script
	def doChangeScript (self):
		
		app.searchDict["type"] = "change"
		self.runChangeScript()
		
	def doChangeAllScript (self):
		
		app.searchDict["type"] = "changeAll"
		self.runChangeScript()
		
	def runChangeScript (self):
		
		c = self.c ; d = app.searchDict
		try:
			while 1:
				if c.script_change_flag:
					exec c.change_text in {} # Use {} to get a pristine environment!
					flag = d.get("continue")
					if not flag: break
				else:
					self.changeSelection()
					break
		except:
			es("exception executing change script")
			es_exception(full=false)
	#@nonl
	#@-node:doChange...Script
	#@+node:doFind...Script
	def doFindScript (self):
		
		app.searchDict["type"] = "find"
		self.runFindScript()
		
	def doFindAllScript (self):
		
		app.searchDict["type"] = "findAll"
		self.runFindScript()
	
	def runFindScript (self):
	
		c = self.c
		try:
			while 1:
				exec c.find_text in {} # Use {} to get a pristine environment!
				flag = app.searchDict.get("continue")
				if not flag: break
		except:
			es("exception executing find script")
			es_exception(full=false)
	#@nonl
	#@-node:doFind...Script
	#@+node:findAll
	def findAll(self):
	
		c = self.c ; t = self.s_text ; gui = app.gui
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
				line = gui.getLineContainingIndex(t,pos)
				self.printLine(line,allFlag=true)
			else: break
		c.endUpdate()
		es("found: " + `count`)
		self.restore(data)
	#@nonl
	#@-node:findAll
	#@+node:findNext
	def findNext(self,initFlag = true):
	
		c = self.c
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
	
		c = self.c
	
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
					c.frame.tree.drawIcon(v) # redraw only the icon.
				return pos, newpos
			elif self.errors:
				return None,None # Abort the search.
			elif c.node_only_flag:
				return None,None # We are only searching one node.
			else:
				v = self.v = self.selectNextVnode()
		return None, None
	#@nonl
	#@-node:findNextMatch
	#@+node:resetWrap
	def resetWrap (self,event=None):
	
		self.wrapVnode = None
		self.onlyVnode = None
	#@nonl
	#@-node:resetWrap
	#@+node:search
	def search (self):
	
		"""Searches the present headline or body text for c.find_text and returns true if found.
	
		c.whole_word_flag, c.ignore_case_flag, and c.pattern_match_flag control the search."""
	
		c = self.c ; v = self.v ; t = self.s_text ; gui = app.gui
		assert(c and t and v)
		if c.selection_only_flag: # 11/9/03
			index,stopindex = self.selStart, self.selEnd
			# trace(index,stopindex,v)
			if index == stopindex:
				return None, None
		else:
			index = gui.getInsertPoint(t)
			stopindex = choose(c.reverse_flag,gui.firstIndex(),gui.lastIndex())
		while 1:
			try:
				pos = self.gui_search(t,c.find_text,index,
					stopindex=stopindex,backwards=c.reverse_flag,
					regexp=c.pattern_match_flag,nocase=c.ignore_case_flag)
			except:
				es_exception(full=false)
				self.errors += 1
				return None, None
			if not pos:
				return None, None
			newpos = gui.moveIndexForward(pos,len(c.find_text))
			if c.reverse_flag and gui.compareIndices(t,newpos,"==",index):
				#@			<< search again after getting stuck going backward >>
				#@+node:<< search again after getting stuck going backward >>
				index = gui.moveIndexBackward(newpos,len(c.find_text))
				
				pos = self.gui_search(t,c.find_text,index,
					stopindex=stopindex,backwards=c.reverse_flag,
					regexp=c.pattern_match_flag,nocase=c.ignore_case_flag)
				
				if not pos:
					return None, None
				
				newpos = gui.moveIndexForward(pos,len(c.find_text))
				#@nonl
				#@-node:<< search again after getting stuck going backward >>
				#@nl
			#@		<< return if we are passed the wrap point >>
			#@+node:<< return if we are passed the wrap point >>
			if self.wrapping and self.wrapPos and self.wrapVnode and self.v == self.wrapVnode:
			
				if c.reverse_flag and gui.compareIndices(t,pos, "<", self.wrapPos):
					# trace("wrap done")
					return None, None
			
				if not c.reverse_flag and gui.compareIndices(t,newpos, ">", self.wrapPos):
					return None, None
			#@nonl
			#@-node:<< return if we are passed the wrap point >>
			#@nl
			if c.whole_word_flag:
				index = t.index(choose(c.reverse_flag,pos,newpos))
				#@			<< continue if not whole word match >>
				#@+node:<< continue if not whole word match >>
				# Set pos to None if word characters preceed or follow the selection.
				before = gui.getCharBeforeIndex(t,pos)
				first  = gui.getCharAtIndex    (t,pos)
				last   = gui.getCharBeforeIndex(t,newpos)
				after  = gui.getCharAtIndex    (t,newpos)
				
				#trace("before,first",before,first,is_c_id(before),is_c_id(first))
				#trace("after,last",  after,last,  is_c_id(after), is_c_id(last))
				
				if is_c_id(before) and is_c_id(first):
					continue
				
				if is_c_id(after) and is_c_id(last):
					continue
				#@nonl
				#@-node:<< continue if not whole word match >>
				#@nl
			#trace("found:",pos,newpos,v)
			gui.setTextSelection(t,pos,newpos)
			return pos, newpos
	#@nonl
	#@-node:search
	#@+node:selectNextVnode
	# Selects the next node to be searched.
	
	def selectNextVnode(self):
	
		c = self.c ; v = self.v
		# trace(`v`)
		
		if c.selection_only_flag:
			return None
		
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
	#@+node:checkArgs
	def checkArgs (self):
	
		c = self.c 
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
	
		c = self.c
		self.in_headline = c.search_headline_flag # Search headlines first.
		self.errors = 0
	
		# Select the first node.
		if c.suboutline_only_flag or c.node_only_flag or c.selection_only_flag: # 11/9/03
			self.v = c.currentVnode()
			if c.selection_only_flag: self.selStart,self.selEnd = c.frame.body.getTextSelection()
			else:                     self.selStart,self.selEnd = None,None
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
	# Returns s_text with "insert" point set properly for batch searches.
	def initBatchText(self):
		v = self.v
		self.wrapping = false # Only interactive commands allow wrapping.
		s = choose(self.in_headline,v.headString(), v.bodyString())
		return self.init_s_text(s)
	
	# Call this routine when moving to the next node when a search fails.
	# Same as above except we don't reset wrapping flag.
	def initNextText(self):
		v = self.v
		s = choose(self.in_headline,v.headString(), v.bodyString())
		return self.init_s_text(s)
	#@nonl
	#@-node:initBatchText & initNextText
	#@+node:initInHeadline
	# Guesses which pane to start in for incremental searches and changes.
	# This must not alter the current "insert" or "sel" marks.
	
	def initInHeadline (self):
	
		c = self.c ; v = self.v
		
		if c.search_headline_flag and c.search_body_flag:
			# Do not change this line without careful thought and extensive testing!
			self.in_headline = (v == c.frame.editVnode())
		else:
			self.in_headline = c.search_headline_flag
	#@nonl
	#@-node:initInHeadline
	#@+node:initInteractiveCommands
	# For incremental searches
	
	def initInteractiveCommands(self):
	
		c = self.c ; v = self.v ; gui = app.gui
		
		self.errors = 0
		if self.in_headline:
			c.frame.tree.setEditVnode(v)
			t = v.edit_text()
			sel = None
			# trace(`pos` + ":" + `self.in_headline` + ":" + `v==c.frame.editVnode()` + ":" + `v`)
		else:
			t = c.frame.bodyCtrl
			sel = gui.getTextSelection(t)
		pos = gui.getInsertPoint(t)
		st = self.initNextText()
		gui.set_focus(c,t)
		gui.setInsertPoint(st,pos)
		if sel:
			self.selStart,self.selEnd = sel
		else:
			self.selStart,self.selEnd = None,None
		self.wrapping = c.wrap_flag
		if c.wrap_flag and self.wrapVnode == None:
			self.wrapPos = pos
			# Do not set self.wrapVnode here: that must be done after the first search.
	#@nonl
	#@-node:initInteractiveCommands
	#@+node:printLine
	def printLine (self,line,allFlag=false):
	
		c = self.c
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
	
		c = self.c ; gui = app.gui
		in_headline,v,t,insert,start,end = data
	
		# Don't try to reedit headline.
		c.selectVnode(v) 
		if not in_headline:
	
			if 0: # Looks bad.
				gui.setSelectionRange(t,start,end)
			else: # Looks good and provides clear indication of failure or termination.
				gui.setSelectionRange(t,insert,insert)
		
			gui.setInsertPoint(t,insert)
			gui.makeIndexVisible(t,insert)
			gui.set_focus(c,t)
	#@nonl
	#@-node:restore
	#@+node:save
	def save (self):
	
		c = self.c ; v = self.v ; gui = app.gui
		t = choose(self.in_headline,v.edit_text(),c.frame.bodyCtrl)
		insert = gui.getInsertPoint(t)
		sel = gui.getSelectionRange(t)
		if len(sel) == 2:
			start,end = sel
		else:
			start,end = None,None
		return (self.in_headline,v,t,insert,start,end)
	#@nonl
	#@-node:save
	#@+node:showSuccess
	def showSuccess(self,pos,newpos):
	
		"""Displays the final result.
		
		Returns self.dummy_vnode, v.edit_text() or c.frame.bodyCtrl with
		"insert" and "sel" points set properly."""
	
		c = self.c ; v = self.v ; gui = app.gui
		
		c.beginUpdate()
		if 1: # range of update...
			c.selectVnode(v)
			c.frame.tree.redraw_now() # Redraw now so selections are not destroyed.
			# Select the found vnode again after redraw.
			if self.in_headline:
				c.editVnode(v)
				c.frame.tree.setNormalLabelState(v)
				assert(v.edit_text())
			else:
				c.selectVnode(v)
		c.endUpdate(false) # Do not draw again!
	
		t = choose(self.in_headline,v.edit_text(),c.frame.bodyCtrl)
		# trace(`self.in_headline` + "," + `t`)
		insert = choose(c.reverse_flag,pos,newpos)
		gui.setInsertPoint(t,insert)
		gui.setSelectionRange(t,pos,newpos)
		if not self.in_headline:
			gui.makeIndexVisible(t,insert)
		gui.set_focus(c,t)
		if c.wrap_flag and not self.wrapVnode:
			self.wrapVnode = self.v
	#@-node:showSuccess
	#@+node:Must be overridden in subclasses
	def init_s_text (self,s):
		self.oops()
		
	def bringToFront (self):
		self.oops()
		
	def gui_search (self,t,*args,**keys):
		self.oops()
		
	def oops(self):
		print ("leoFind oops:",
			callerName(2),
			"should be overridden in subclass")
	#@-node:Must be overridden in subclasses
	#@-others
#@nonl
#@-node:@file leoFind.py
#@-leo
