#@+leo-ver=4
#@+node:@file leoCommands.py
#@@language python

from leoGlobals import *

import leoAtFile,leoFileCommands,leoImport,leoNodes,leoTangle,leoUndo

class baseCommands:
	"""The base class for Leo's main commander."""
	#@	@+others
	#@+node:c.__init__, initIvars
	def __init__(self,frame,fileName):
		
		# trace("Commands",fileName)
	
		self.frame = frame
		self.mFileName = fileName
		self.initIvars()
	
		# initialize the sub-commanders
		self.fileCommands = leoFileCommands.fileCommands(self)
		self.atFileCommands = leoAtFile.atFile(self)
		self.importCommands = leoImport.leoImportCommands(self)
		self.tangleCommands = leoTangle.tangleCommands(self)
		self.undoer = leoUndo.undoer(self)
	
	def initIvars(self):
	
		#@	<< initialize ivars >>
		#@+node:<< initialize ivars >>
		# per-document info...
		self.hookFunction = None
		self.openDirectory = None # 7/2/02
		
		self.expansionLevel = 0  # The expansion level of this outline.
		self.expansionNode = None # The last node we expanded or contracted.
		self.changed = false # true if any data has been changed since the last save.
		self.loading = false # true if we are loading a file: disables c.setChanged()
		
		# For tangle/untangle
		self.tangle_errrors = 0
		
		# Global options
		self.page_width = 132
		self.tab_width = 4
		self.tangle_batch_flag = false
		self.untangle_batch_flag = false
		# Default Tangle options
		self.tangle_directory = ""
		self.use_header_flag = false
		self.output_doc_flag = false
		# Default Target Language
		self.target_language = "python" # 8/11/02: Required if leoConfig.txt does not exist.
		
		# These are defined here, and updated by the tree.select()
		self.beadList = [] # list of vnodes for the Back and Forward commands.
		self.beadPointer = -1 # present item in the list.
		self.visitedList = [] # list of vnodes for the Nodes dialog.
		#@nonl
		#@-node:<< initialize ivars >>
		#@nl
		self.setIvarsFromFind()
	#@nonl
	#@-node:c.__init__, initIvars
	#@+node:c.__repr__ & __str__
	def __repr__ (self):
		
		try:
			return "Commander: " + self.mFileName
		except:
			return "Commander: bad mFileName"
			
	__str__ = __repr__
	#@-node:c.__repr__ & __str__
	#@+node:c.setIvarsFromFind
	# This should be called whenever we need to use find values:
	# i.e., before reading or writing
	
	def setIvarsFromFind (self):
	
		c = self ; find = app.findFrame
		if find:
			find.set_ivars(c)
	#@-node:c.setIvarsFromFind
	#@+node:c.setIvarsFromPrefs
	#@+at 
	#@nonl
	# This should be called whenever we need to use preference:
	# i.e., before reading, writing, tangling, untangling.
	# 
	# 7/2/02: We no longer need this now that the Prefs dialog is modal.
	#@-at
	#@@c
	
	def setIvarsFromPrefs (self):
	
		pass
	#@nonl
	#@-node:c.setIvarsFromPrefs
	#@+node:cutOutline
	def cutOutline(self):
	
		c = self
		if c.canDeleteHeadline():
			c.copyOutline()
			c.deleteHeadline("Cut Node")
			c.recolor()
	#@nonl
	#@-node:cutOutline
	#@+node:copyOutline
	def copyOutline(self):
	
		# Copying an outline has no undo consequences.
		c = self
		c.endEditing()
		c.fileCommands.assignFileIndices()
		s = c.fileCommands.putLeoOutline()
		app.gui.replaceClipboardWith(s)
	#@nonl
	#@-node:copyOutline
	#@+node:pasteOutline
	#@+at 
	#@nonl
	# To cut and paste between apps, just copy into an empty body first, then 
	# copy to Leo's clipboard.
	#@-at
	#@@c
	
	def pasteOutline(self):
	
		c = self ; current = c.currentVnode()
		
		s = app.gui.getTextFromClibboard()
		
		if 0: # old code
			try:
				s = app.root.selection_get(selection="CLIPBOARD")
			except:
				s = None # This should never happen.
	
		if not s or not c.canPasteOutline(s):
			return # This should never happen.
	
		isLeo = match(s,0,app.prolog_prefix_string)
	
		# trace(`s`)
		if isLeo:
			v = c.fileCommands.getLeoOutline(s)
		else:
			v = c.importCommands.convertMoreStringToOutlineAfter(s,current)
		if v:
			c.endEditing()
			c.beginUpdate()
			if 1: # inside update...
				v.createDependents()# To handle effects of clones.
				c.validateOutline()
				c.selectVnode(v)
				v.setDirty()
				c.setChanged(true)
				# paste as first child if back is expanded.
				back = v.back()
				if back and back.isExpanded():
					v.moveToNthChildOf(back,0)
				c.undoer.setUndoParams("Paste Node",v)
			c.endUpdate()
			c.recolor()
		else:
			es("The clipboard is not a valid " + choose(isLeo,"Leo","MORE") + " file")
	#@nonl
	#@-node:pasteOutline
	#@+node:beginUpdate
	def beginUpdate(self):
	
		self.frame.beginUpdate()
		
	BeginUpdate = beginUpdate # Compatibility with old scripts
	#@nonl
	#@-node:beginUpdate
	#@+node:bringToFront
	def bringToFront(self):
	
		self.frame.deiconify()
	
	BringToFront = bringToFront # Compatibility with old scripts
	#@nonl
	#@-node:bringToFront
	#@+node:endUpdate
	def endUpdate(self, flag=true):
		
		self.frame.endUpdate(flag)
		
	EndUpdate = endUpdate # Compatibility with old scripts
	#@nonl
	#@-node:endUpdate
	#@+node:recolor
	def recolor(self):
	
		self.frame.recolor(self.frame.currentVnode())
	#@nonl
	#@-node:recolor
	#@+node:redraw & repaint
	def redraw(self):
	
		self.frame.redraw()
		
	# Compatibility with old scripts
	Redraw = redraw 
	repaint = redraw
	Repaint = redraw
	#@nonl
	#@-node:redraw & repaint
	#@+node:convertAllBlanks
	def convertAllBlanks (self):
		
		c = self ; v = current = c.currentVnode()
		next = v.nodeAfterTree()
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = c.body.getAllText()
		oldSel = c.body.getTextSelection()
		count = 0
		while v and v != next:
			if v == current:
				if c.convertBlanks(setUndoParams=false):
					count += 1
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				assert(isUnicode(text))
				lines = string.split(text, '\n')
				for line in lines:
					s = optimizeLeadingWhitespace(line,tabWidth)
					if s != line:
						changed = true ; count += 1
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
		if count > 0:
			newText = c.body.getAllText()
			newSel = c.body.getTextSelection()
			c.undoer.setUndoParams("Convert All Blanks",
				current,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		es("blanks converted to tabs in %d nodes" % count)
	#@nonl
	#@-node:convertAllBlanks
	#@+node:convertAllTabs
	def convertAllTabs (self):
	
		c = self ; v = current = c.currentVnode()
		next = v.nodeAfterTree()
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = c.body.getAllText()
		oldSel = c.body.getTextSelection()
		count = 0
		while v and v != next:
			if v == current:
				if self.convertTabs(setUndoParams=false):
					count += 1
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				assert(isUnicode(text))
				lines = string.split(text, '\n')
				for line in lines:
					i,w = skip_leading_ws_with_indent(line,0,tabWidth)
					s = computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
					if s != line:
						changed = true ; count += 1
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
		if count > 0:
			newText = c.body.getAllText()
			newSel = c.body.getTextSelection() # 7/11/03
			c.undoer.setUndoParams("Convert All Tabs",
				current,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		es("tabs converted to blanks in %d nodes" % count)
	#@nonl
	#@-node:convertAllTabs
	#@+node:convertBlanks
	def convertBlanks (self,setUndoParams=true):
	
		c = self
		head,lines,tail,oldSel,oldYview = c.getBodyLines()
		result = [] ; changed = false
	
		# DTHEIN 3-NOV-2002: use the relative @tabwidth, not the global one
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
	
		if 0: # DTHEIN 3-NOV-2002: don't use the global @tabwidth
			for line in lines:
				s = optimizeLeadingWhitespace(line,c.tab_width)
				if s != line: changed = true
				result.append(s)
		else: # DTHEIN 3-NOV-2002: use relative @tabwidth (tabWidth)
			for line in lines:
				s = optimizeLeadingWhitespace(line,tabWidth)
				if s != line: changed = true
				result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			undoType = choose(setUndoParams,"Convert Blanks",None)
			c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
			c.body.selectAllText()
	
		return changed
	#@-node:convertBlanks
	#@+node:convertTabs
	def convertTabs (self,setUndoParams=true):
	
		c = self
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		
		# DTHEIN 3-NOV-2002: use the relative @tabwidth, not the global one
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
	
		if 0: # DTHEIN 3-NOV-2002: don't use the global @tabwidth
			for line in lines:
				i,w = skip_leading_ws_with_indent(line,0,c.tab_width)
				s = computeLeadingWhitespace(w,-abs(c.tab_width)) + line[i:] # use negative width.
				if s != line: changed = true
				result.append(s)
		else: # DTHEIN 3-NOV-2002: use the relative @tabwidth (tabWidth)
			for line in lines:
				i,w = skip_leading_ws_with_indent(line,0,tabWidth)
				s = computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
				if s != line: changed = true
				result.append(s)
	
		if changed:
			result = string.join(result,'\n')
			undoType = choose(setUndoParams,"Convert Tabs",None)
			c.updateBodyPane(head,result,tail,undoType,oldSel,oldYview) # Handles undo
			c.body.selectAllText()
			
		return changed
	#@nonl
	#@-node:convertTabs
	#@+node:createLastChildNode
	def createLastChildNode (self,parent,headline,body):
		
		c = self
		if body and len(body) > 0:
			body = string.rstrip(body)
		if not body or len(body) == 0:
			body = ""
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		v.t.setTnodeText(body)
		v.createDependents() # To handle effects of clones.
		v.setDirty()
		c.validateOutline()
	#@nonl
	#@-node:createLastChildNode
	#@+node:dedentBody
	def dedentBody (self):
	
		c = self
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width-abs(c.tab_width),c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Undent",oldSel,oldYview)
	#@nonl
	#@-node:dedentBody
	#@+node:extract
	def extract(self):
	
		c = self ; current = v = c.currentVnode()
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		oldText = c.body.getAllText()
		oldSel = c.body.getTextSelection()
		#@	<< Set headline for extract >>
		#@+node:<< Set headline for extract >>
		headline = string.strip(headline)
		while len(headline) > 0 and headline[0] == '/':
			headline = headline[1:]
		headline = string.strip(headline)
		#@nonl
		#@-node:<< Set headline for extract >>
		#@nl
		# Remove leading whitespace from all body lines.
		result = []
		for line in lines:
			# Remove the whitespace on the first line
			line = removeLeadingWhitespace(line,ws,c.tab_width)
			result.append(line)
		# Create a new node from lines.
		body = string.join(result,'\n')
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		if 1: # update range...
			c.createLastChildNode(v,headline,body)
			undoType =  "Can't Undo" # 12/8/02: None enables further undoes, but there are bugs now.
			c.updateBodyPane(head,None,tail,undoType,oldSel,oldYview)
			newText = c.body.getAllText()
			newSel = c.body.getTextSelection() # 7/11/03
			c.undoer.setUndoParams("Extract",
				v,select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		c.endUpdate()
	#@nonl
	#@-node:extract
	#@+node:extractSection
	def extractSection(self):
	
		c = self ; current = v = c.currentVnode()
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		line1 = "\n" + headline
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		# trace("v:     " + `v`)
		# trace("v_copy:" + `v_copy`)
		oldText = c.body.getAllText()
		oldSel = c.body.getTextSelection()
		#@	<< Set headline for extractSection >>
		#@+node:<< Set headline for extractSection >>
		while len(headline) > 0 and headline[0] == '/':
			headline = headline[1:]
		headline = string.strip(headline)
		
		# Make sure we have a @< or <<
		if headline[0:2] != '<<' and headline[0:2] != '@<':
			es("Selected text should start with a section name",color="blue")
			return
		#@nonl
		#@-node:<< Set headline for extractSection >>
		#@nl
		# Remove leading whitespace from all body lines.
		result = []
		for line in lines:
			# Remove the whitespace on the first line
			line = removeLeadingWhitespace(line,ws,c.tab_width)
			result.append(line)
		# Create a new node from lines.
		body = string.join(result,'\n')
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		if 1: # update range...
			c.createLastChildNode(v,headline,body)
			undoType = None # Set undo params later.
			c.updateBodyPane(head,line1,tail,undoType,oldSel,oldYview)
			newText = c.body.getAllText()
			newSel = c.body.getTextSelection()
			c.undoer.setUndoParams("Extract Section",v,
				select=current,oldTree=v_copy,
				oldText=oldText,newText=newText,
				oldSel=oldSel,newSel=newSel)
		c.endUpdate()
	#@nonl
	#@-node:extractSection
	#@+node:extractSectionNames
	def extractSectionNames(self):
	
		c = self ; current = v = c.currentVnode()
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		# Create copy for undo.
		v_copy = c.undoer.saveTree(v)
		# No change to body or selection of this node.
		oldText = newText = c.body.getAllText()
		i, j = oldSel = newSel = c.body.getTextSelection()
		c.beginUpdate()
		if 1: # update range...
			found = false
			for s in lines:
				#@			<< Find the next section name >>
				#@+node:<< Find the next section name >>
				head1 = string.find(s,"<<")
				if head1 > -1:
					head2 = string.find(s,">>",head1)
				else:
					head1 = string.find(s,"@<")
					if head1 > -1:
						head2 = string.find(s,"@>",head1)
						
				if head1 == -1 or head2 == -1 or head1 > head2:
					name = None
				else:
					name = s[head1:head2+2]
				#@nonl
				#@-node:<< Find the next section name >>
				#@nl
				if name:
					self.createLastChildNode(v,name,None)
					found = true
			c.selectVnode(v)
			c.validateOutline()
			if not found:
				es("Selected text should contain one or more section names",color="blue")
		c.endUpdate()
		# No change to body or selection
		c.undoer.setUndoParams("Extract Names",
			v,select=current,oldTree=v_copy,
			oldText=oldText,newText=newText,
			oldSel=oldSel,newSel=newSel)
		# Restore the selection.
		c.body.setTextSelection(oldSel)
		c.body.setFocus()
	#@nonl
	#@-node:extractSectionNames
	#@+node:findBoundParagraph
	def findBoundParagraph (self):
		
		c = self
		head,ins,tail = c.body.getInsertLines()
	
		if not ins or ins.isspace() or ins[0] == '@':
			return None,None,None
			
		head_lines = splitLines(head)
		tail_lines = splitLines(tail)
	
		if 0:
			#@		<< trace head_lines, ins, tail_lines >>
			#@+node:<< trace head_lines, ins, tail_lines >>
			print ; print "head_lines"
			for line in head_lines: print `line`
			print ; print "ins", `ins`
			print ; print "tail_lines"
			for line in tail_lines: print `line`
			#@nonl
			#@-node:<< trace head_lines, ins, tail_lines >>
			#@nl
	
		# Scan backwards.
		i = len(head_lines)
		while i > 0:
			i -= 1
			line = head_lines[i]
			if len(line) == 0 or line.isspace() or line[0] == '@':
				i += 1 ; break
	
		pre_para_lines = head_lines[:i]
		para_head_lines = head_lines[i:]
	
		# Scan forwards.
		i = 0
		while i < len(tail_lines):
			line = tail_lines[i]
			if len(line) == 0 or line.isspace() or line[0] == '@':
				break
			i += 1
			
		para_tail_lines = tail_lines[:i]
		post_para_lines = tail_lines[i:]
		
		head = joinLines(pre_para_lines)
		result = para_head_lines 
		result.extend([ins])
		result.extend(para_tail_lines)
		tail = joinLines(post_para_lines)
	
		return head,result,tail # string, list, string
	#@-node:findBoundParagraph
	#@+node:getBodyLines
	def getBodyLines (self):
	
		c = self
		oldVview = c.body.getYScrollPosition()
		oldSel   = c.body.getTextSelection()
		head,lines,tail = c.body.getSelectionLines()
	
		if not lines:
			lines = c.body.getAllText()
	
		lines = string.split(lines,'\n')
	
		return head,lines,tail,oldSel,oldVview
	#@nonl
	#@-node:getBodyLines
	#@+node:indentBody
	def indentBody (self):
	
		c = self
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width+abs(c.tab_width),c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Indent",oldSel,oldYview)
	#@nonl
	#@-node:indentBody
	#@+node:reformatParagraph
	def reformatParagraph(self):
	
		"""Reformat a text paragraph in a Tk.Text widget
	
	Wraps the concatenated text to present page width setting. Leading tabs are
	sized to present tab width setting. First and second line of original text is
	used to determine leading whitespace in reformatted text. Hanging indentation
	is honored.
	
	Paragraph is bound by start of body, end of body, blank lines, and lines
	starting with "@". Paragraph is selected by position of current insertion
	cursor."""
	
		c = self ; v = c.currentVnode()
	
		if c.body.hasTextSelection():
			es("Text selection inhibits Reformat Paragraph",color="blue")
			return
	
		#@	<< compute vars for reformatParagraph >>
		#@+node:<< compute vars for reformatParagraph >>
		dict = scanDirectives(c)
		pageWidth = dict.get("pagewidth")
		tabWidth  = dict.get("tabwidth")
		
		original = c.body.getAllText()
		oldSel   = c.body.getTextSelection()
		oldYview = c.body.getYScrollPosition()
		head,lines,tail = c.findBoundParagraph()
		#@nonl
		#@-node:<< compute vars for reformatParagraph >>
		#@nl
		if lines:
			#@		<< compute the leading whitespace >>
			#@+node:<< compute the leading whitespace >>
			indents = [0,0] ; leading_ws = ["",""]
			
			for i in (0,1):
				if i < len(lines):
					# Use the original, non-optimized leading whitespace.
					leading_ws[i] = ws = get_leading_ws(lines[i])
					indents[i] = computeWidth(ws,tabWidth)
					
			indents[1] = max(indents)
			if len(lines) == 1:
				leading_ws[1] = leading_ws[0]
			#@nonl
			#@-node:<< compute the leading whitespace >>
			#@nl
			#@		<< compute the result of wrapping all lines >>
			#@+node:<< compute the result of wrapping all lines >>
			# Remember whether the last line ended with a newline.
			lastLine = lines[-1]
			trailingNL = lastLine and lastLine[-1] == '\n'
			
			# Remove any trailing newlines for wraplines.
			lines = [line[:-1] for line in lines[:-1]]
			if lastLine and trailingNL:
				lastLine = lastLine[:-1]
			lines.extend([lastLine])
			
			# Wrap the lines, decreasing the page width by indent.
			result = wrap_lines(lines,
				pageWidth-indents[1],
				pageWidth-indents[0])
			
			# Convert the result to a string.
			result = '\n'.join(result)
			if trailingNL:
				result += '\n'
			#@nonl
			#@-node:<< compute the result of wrapping all lines >>
			#@nl
			#@		<< update the body, selection & undo state >>
			#@+node:<< update the body, selection & undo state >>
			changed = original != head + result + tail
			undoType = choose(changed,"Reformat Paragraph",None)
			
			sel_start, sel_end = self.body.setSelectionAreas(head,result,tail)
			
			c.frame.onBodyChanged(v,undoType,oldSel=oldSel,oldYview=oldYview)
			
			# Advance the selection to the next paragraph.
			newSel = sel_end, sel_end
			c.body.setTextSelection(newSel)
			#@nonl
			#@-node:<< update the body, selection & undo state >>
			#@nl
	#@nonl
	#@-node:reformatParagraph
	#@+node:updateBodyPane (handles undo)
	def updateBodyPane (self,head,middle,tail,undoType,oldSel,oldYview):
		
		c = self ; v = c.currentVnode()
	
		# Update the text and notify the event handler.
		self.body.setSelectionAreas(head,middle,tail)
		self.body.setTextSelection(oldSel)
		c.frame.onBodyChanged(v,undoType,oldSel=oldSel,oldYview=oldYview)
	
		# Update the changed mark and icon.
		c.setChanged(true)
		c.beginUpdate()
		if not v.isDirty():
			v.setDirty()
		c.endUpdate()
	
		# Scroll as necessary.
		if oldYview:
			self.body.setYScrollPosition(oldYview)
		else:
			self.body.makeInsertPointVisible()
	
		c.body.setFocus()
		c.recolor()
	#@nonl
	#@-node:updateBodyPane (handles undo)
	#@+node:canContractAllHeadlines
	def canContractAllHeadlines (self):
	
		c = self ; v = c.rootVnode()
		if not v: return false
		while v:
			if v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canContractAllHeadlines
	#@+node:canContractAllSubheads
	def canContractAllSubheads (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		next = v.nodeAfterTree()
		v = v.threadNext()
		while v and v != next:
			if v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canContractAllSubheads
	#@+node:canContractParent
	def canContractParent (self):
	
		c = self ; v = c.currentVnode()
		return v.parent() != None
	#@nonl
	#@-node:canContractParent
	#@+node:canContractSubheads
	def canContractSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		v = v.firstChild()
		while v:
			if v.isExpanded():
				return true
			v = v.next()
		return false
	#@nonl
	#@-node:canContractSubheads
	#@+node:canCutOutline & canDeleteHeadline
	def canDeleteHeadline (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		if v.parent(): # v is below the top level.
			return true
		else: # v is at the top level.  We can not delete the last node.
			return v.threadBack() or v.next()
	
	canCutOutline = canDeleteHeadline
	#@nonl
	#@-node:canCutOutline & canDeleteHeadline
	#@+node:canDemote
	def canDemote (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		return v.next() != None
	#@nonl
	#@-node:canDemote
	#@+node:canExpandAllHeadlines
	def canExpandAllHeadlines (self):
	
		c = self ; v = c.rootVnode()
		if not v: return false
		while v:
			if not v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canExpandAllHeadlines
	#@+node:canExpandAllSubheads
	def canExpandAllSubheads (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		next = v.nodeAfterTree()
		v = v.threadNext()
		while v and v != next:
			if not v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canExpandAllSubheads
	#@+node:canExpandSubheads
	def canExpandSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		v = v.firstChild()
		while v:
			if not v.isExpanded():
				return true
			v = v.next()
		return false
	#@nonl
	#@-node:canExpandSubheads
	#@+node:canExtract, canExtractSection & canExtractSectionNames
	def canExtract (self):
	
		c = self
		if c.bodyCtrl:
			i, j = c.body.getTextSelection()
			return i and j and c.bodyCtrl.compare(i, "!=", j)
		else:
			return false
	
	canExtractSection = canExtract
	canExtractSectionNames = canExtract
	#@nonl
	#@-node:canExtract, canExtractSection & canExtractSectionNames
	#@+node:canFindMatchingBracket
	def canFindMatchingBracket (self):
		
		c = self ; body = c.bodyCtrl
		brackets = "()[]{}"
		c1 = body.get("insert -1c")
		c2 = body.get("insert")
		# Bug fix: 2/11/03
		return (c1 and c1 in brackets) or (c2 and c2 in brackets)
	#@nonl
	#@-node:canFindMatchingBracket
	#@+node:canGoToNextDirtyHeadline
	def canGoToNextDirtyHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return false
	
		v = c.rootVnode()
		while v:
			if v.isDirty()and v != current:
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canGoToNextDirtyHeadline
	#@+node:canGoToNextMarkedHeadline
	def canGoToNextMarkedHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return false
	
		v = c.rootVnode()
		while v:
			if v.isMarked()and v != current:
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canGoToNextMarkedHeadline
	#@+node:canMarkChangedHeadline
	def canMarkChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canMarkChangedHeadline
	#@+node:canMarkChangedRoots
	def canMarkChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canMarkChangedRoots
	#@+node:canMoveOutlineDown
	def canMoveOutlineDown (self):
	
		c = self
		if 1: # The permissive way
			current = c.currentVnode()
			if not current: return false
			v = current.visNext()
			while v and current.isAncestorOf(v):
				v = v.visNext()
			return v != None
		else: # The MORE way.
			return c.currentVnode().next() != None
	#@nonl
	#@-node:canMoveOutlineDown
	#@+node:canMoveOutlineLeft
	def canMoveOutlineLeft (self):
	
		c = self ; v = c.currentVnode()
		if 0: # Old code: assumes multiple leftmost nodes.
			return v and v.parent()
		else: # Can't move a child of the root left.
			return v and v.parent() and v.parent().parent()
	#@nonl
	#@-node:canMoveOutlineLeft
	#@+node:canMoveOutlineRight
	def canMoveOutlineRight (self):
	
		c = self ; v = c.currentVnode()
		return v and v.back()
	#@nonl
	#@-node:canMoveOutlineRight
	#@+node:canMoveOutlineUp
	def canMoveOutlineUp (self):
	
		c = self ; v = c.currentVnode()
		if 1: # The permissive way.
			return v and v.visBack()
		else: # The MORE way.
			return v and v.back()
	#@nonl
	#@-node:canMoveOutlineUp
	#@+node:canPasteOutline
	def canPasteOutline (self,s=None):
	
		c = self
		if s == None:
			s = app.gui.getTextFromClibboard()
		if not s:
			return false
	
		# trace(s)
		if match(s,0,app.prolog_prefix_string):
			return true
		elif len(s) > 0:
			return c.importCommands.stringIsValidMoreFile(s)
		else:
			return false
	#@nonl
	#@-node:canPasteOutline
	#@+node:canPromote
	def canPromote (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
	#@nonl
	#@-node:canPromote
	#@+node:canRevert
	def canRevert (self):
	
		# c.mFileName will be "untitled" for unsaved files.
		c = self
		return (c.frame and c.mFileName and c.isChanged())
	#@nonl
	#@-node:canRevert
	#@+node:canSelect....
	# 7/29/02: The shortcuts for these commands are now unique.
	
	def canSelectThreadBack (self):
		v = self.currentVnode()
		return v and v.threadBack()
		
	def canSelectThreadNext (self):
		v = self.currentVnode()
		return v and v.threadNext()
	
	def canSelectVisBack (self):
		v = self.currentVnode()
		return v and v.visBack()
		
	def canSelectVisNext (self):
		v = self.currentVnode()
		return v and v.visNext()
	#@nonl
	#@-node:canSelect....
	#@+node:canShiftBodyLeft/Right
	def canShiftBodyLeft (self):
	
		c = self
		if c.bodyCtrl:
			s = c.bodyCtrl.GetValue()
			return len(s) > 0
		else:
			return false
			
	def canShiftBodyRight (self):
	
		c = self
		if c.bodyCtrl:
			s = c.bodyCtrl.GetValue()
			return len(s) > 0
		else:
			return false
	#@nonl
	#@-node:canShiftBodyLeft/Right
	#@+node:canSortChildren, canSortSiblings
	def canSortChildren (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
		
	def canSortSiblings (self):
	
		c = self ; v = c.currentVnode()
		return v.next() or v.back()
	#@nonl
	#@-node:canSortChildren, canSortSiblings
	#@+node:canUndo & canRedo
	def canUndo (self):
	
		c = self
		return c.undoer.canUndo()
		
	def canRedo (self):
	
		c = self
		return c.undoer.canRedo()
	#@nonl
	#@-node:canUndo & canRedo
	#@+node:canUnmarkAll
	# Returns true if any node is marked.
	
	def canUnmarkAll (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isMarked():
				return true
			v = v.threadNext()
		return false
	#@nonl
	#@-node:canUnmarkAll
	#@+node:contractAllHeadlines
	def contractAllHeadlines (self):
	
		c = self ; current = c.currentVnode()
		v = c.rootVnode()
		c.beginUpdate()
	
		while v:
			c.contractSubtree(v)
			v = v.next()
	
		if not current.isVisible():
			# 1/31/03: Select the topmost ancestor of the presently selected node.
			v = current
			while v and v.parent():
				v = v.parent()
			c.selectVnode(v)
	
		c.endUpdate()
		c.expansionLevel = 1 # Reset expansion level.
	#@nonl
	#@-node:contractAllHeadlines
	#@+node:contractNode
	def contractNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.contract()
		c.endUpdate()
	#@-node:contractNode
	#@+node:contractParent
	def contractParent (self):
		
		c = self ; v = c.currentVnode()
		parent = v.parent()
		if not parent: return
		
		c.beginUpdate()
		c.selectVnode(parent)
		parent.contract()
		c.endUpdate()
	#@nonl
	#@-node:contractParent
	#@+node:expandAllHeadlines
	def expandAllHeadlines(self):
	
		c = self ; v = root = c.rootVnode()
		c.beginUpdate()
		while v:
			c.expandSubtree(v)
			v = v.next()
		c.selectVnode(root)
		c.endUpdate()
		c.expansionLevel = 0 # Reset expansion level.
	#@nonl
	#@-node:expandAllHeadlines
	#@+node:expandAllSubheads
	def expandAllSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		c.expandSubtree(v)
		while child:
			c.expandSubtree(child)
			child = child.next()
		c.selectVnode(v)
		c.endUpdate()
	#@nonl
	#@-node:expandAllSubheads
	#@+node:expandLevel1..9
	def expandLevel1 (self): self.expandToLevel(1)
	def expandLevel2 (self): self.expandToLevel(2)
	def expandLevel3 (self): self.expandToLevel(3)
	def expandLevel4 (self): self.expandToLevel(4)
	def expandLevel5 (self): self.expandToLevel(5)
	def expandLevel6 (self): self.expandToLevel(6)
	def expandLevel7 (self): self.expandToLevel(7)
	def expandLevel8 (self): self.expandToLevel(8)
	def expandLevel9 (self): self.expandToLevel(9)
	#@-node:expandLevel1..9
	#@+node:expandNextLevel
	def expandNextLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(c.expansionLevel + 1)
	#@-node:expandNextLevel
	#@+node:expandNode
	def expandNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.expand()
		c.endUpdate()
	
	#@-node:expandNode
	#@+node:expandPrevLevel
	def expandPrevLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(max(1,c.expansionLevel - 1))
	#@-node:expandPrevLevel
	#@+node:contractSubtree
	def contractSubtree (self,v):
	
		last = v.lastNode()
		while v and v != last:
			v.contract()
			v = v.threadNext()
	#@nonl
	#@-node:contractSubtree
	#@+node:expandSubtree
	def expandSubtree (self,v):
	
		c = self
		last = v.lastNode()
		while v and v != last:
			v.expand()
			v = v.threadNext()
		c.frame.redraw()
	#@nonl
	#@-node:expandSubtree
	#@+node:expandToLevel
	def expandToLevel (self,level):
	
		c = self
		c.beginUpdate()
		if 1: # 1/31/03: The expansion is local to the present node.
			v = c.currentVnode() ; n = v.level()
			after = v.nodeAfterTree()
			while v and v != after:
				if v.level() - n + 1 < level:
					v.expand()
				else:
					v.contract()
				v = v.threadNext()
		else: # The expansion is global
			# Start the recursion.
			# First contract everything.
			c.contractAllHeadlines()
			v = c.rootVnode()
			while v:
				c.expandTreeToLevelFromLevel(v,level,1)
				v = v.next()
		c.expansionLevel = level
		c.expansionNode = c.currentVnode()
		c.endUpdate()
	#@nonl
	#@-node:expandToLevel
	#@+node:c.currentVnode
	# Compatibility with scripts
	
	def currentVnode (self):
	
		return self.frame.currentVnode()
	#@-node:c.currentVnode
	#@+node:clearAllMarked
	def clearAllMarked (self):
	
		c = self ; v = c.rootVnode()
		while v:
			v.clearMarked()
			v = v.threadNext()
	#@nonl
	#@-node:clearAllMarked
	#@+node:clearAllVisited
	def clearAllVisited (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			# tick("clearAllVisited loop")
			v.clearVisited()
			if v.t:
				v.t.clearVisited()
			v = v.threadNext()
		c.endUpdate(false) # never redraw the tree.
	#@nonl
	#@-node:clearAllVisited
	#@+node:fileName
	# Compatibility with scripts
	
	def fileName (self):
	
		return self.mFileName
	#@-node:fileName
	#@+node:isChanged
	def isChanged (self):
	
		return self.changed
	#@nonl
	#@-node:isChanged
	#@+node:rootVnode
	# Compatibility with scripts
	
	def rootVnode (self):
	
		return self.frame.rootVnode()
	#@-node:rootVnode
	#@+node:c.setChanged
	def setChanged (self,changedFlag):
	
		c = self
		if not c.frame: return
		# Clear all dirty bits _before_ setting the caption.
		# 9/15/01 Clear all dirty bits except orphaned @file nodes
		if not changedFlag:
			# trace("clearing all dirty bits")
			v = c.rootVnode()
			while v:
				if v.isDirty() and not (v.isAtFileNode() or v.isAtRawFileNode()):
					v.clearDirtyJoined()
				v = v.threadNext()
		# Update all derived changed markers.
		c.changed = changedFlag
		s = c.frame.getTitle()
		if len(s) > 2 and not c.loading: # don't update while loading.
			if changedFlag:
				# import traceback ; traceback.print_stack()
				if s [0] != '*': c.frame.setTitle("* " + s)
			else:
				if s[0:2]=="* ": c.frame.setTitle(s[2:])
	#@nonl
	#@-node:c.setChanged
	#@+node:c.checkMoveWithParentWithWarning
	# Returns false if any node of tree is a clone of parent or any of parents ancestors.
	
	def checkMoveWithParentWithWarning (self,root,parent,warningFlag):
	
		clone_message = "Illegal move or drag: no clone may contain a clone of itself"
		drag_message  = "Illegal drag: Can't drag a node into its own tree"
	
		# 10/25/02: Create dictionaries for faster checking.
		parents = {} ; clones = {}
		while parent:
			parents [parent.t] = parent.t
			if parent.isCloned():
				clones [parent.t] = parent.t
			parent = parent.parent()
		
		# 10/25/02: Scan the tree only once.
		v = root ; next = root.nodeAfterTree()
		while v and v != next:
			ct = clones.get(v.t)
			if ct != None and ct == v.t:
				if warningFlag:
					alert(clone_message)
				return false
			v = v.threadNext()
	
		pt = parents.get(root.t)
		if pt == None:
			return true
		else:
			if warningFlag:
				alert(drag_message)
			return false
	#@-node:c.checkMoveWithParentWithWarning
	#@+node:c.deleteHeadline
	# Deletes the current vnode and dependent nodes. Does nothing if the outline would become empty.
	
	def deleteHeadline (self,op_name="Delete Outline"):
	
		c = self ; v = c.currentVnode()
		if not v: return
		vBack = v.visBack()
		# Bug fix: 1/18/00: if vBack is NULL we are at the top level,
		# the next node should be v.next(), _not_ v.visNext();
		if vBack: newNode = vBack
		else: newNode = v.next()
		if not newNode: return
		c.endEditing()# Make sure we capture the headline for Undo.
		c.beginUpdate()
		v.setDirtyDeleted() # 8/3/02: Mark @file nodes dirty for all clones in subtree.
		# Reinsert v after back, or as the first child of parent, or as the root.
		c.undoer.setUndoParams(op_name,v,select=newNode)
		v.doDelete(newNode) # doDelete destroys dependents.
		c.setChanged(true)
		c.endUpdate()
		c.validateOutline()
	#@nonl
	#@-node:c.deleteHeadline
	#@+node:c.insertHeadline
	# Inserts a vnode after the current vnode.  All details are handled by the vnode class.
	
	def insertHeadline (self,op_name="Insert Outline"):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		c.beginUpdate()
		if 1: # inside update...
			if current.hasChildren() and current.isExpanded():
				v = current.insertAsNthChild(0)
			else:
				v = current.insertAfter()
			c.undoer.setUndoParams(op_name,v,select=current)
			v.createDependents() # To handle effects of clones.
			c.selectVnode(v)
			c.editVnode(v)
			v.setDirty() # Essential in Leo2.
			c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:c.insertHeadline
	#@+node:c.clone
	def clone (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
		c.beginUpdate()
		clone = v.clone(v)
		c.initAllCloneBitsInTree(v) # 10/14/03
		clone.setDirty() # essential in Leo2
		c.setChanged(true)
		if c.validateOutline():
			c.selectVnode(clone)
			c.undoer.setUndoParams("Clone",clone)
		c.endUpdate() # updates all icons
	#@nonl
	#@-node:c.clone
	#@+node:initAllCloneBits & initAllCloneBitsInTree
	def initAllCloneBits (self):
		
		"""Initialize all clone bits in the entire outline"""
	
		c=self
		c.clearAllVisited()
		v = self.frame.rootVnode()
		c.beginUpdate()
		while v:
			if not v.t.isVisited():
				v.t.setVisited() # Inhibit visits to all joined nodes.
				c.initJoinedCloneBits(v)
			v = v.threadNext()
		c.endUpdate()
		
	def initAllCloneBitsInTree (self,v):
		
		"""Initialize all clone bits in the v's subtree"""
	
		c=self
		v.clearAllVisitedInTree()
		after = v.nodeAfterTree()
		c.beginUpdate()
		while v and v != after:
			if not v.t.isVisited():
				v.t.setVisited() # Inhibit visits to all joined nodes.
				c.initJoinedCloneBits(v)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:initAllCloneBits & initAllCloneBitsInTree
	#@+node:c.initJoinedClonedBits (changed in 3.11.1)
	# Initializes all clone bits in the all nodes joined to v.
	
	def initJoinedCloneBits (self,v):
		
		if 0:
			if not self.loading:
				trace(len(v.t.joinList),v)
	
		c = self
		c.beginUpdate()
		mark = v.shouldBeClone()
		if mark:
			# Set clone bit in v and all joined nodes.
			v.setClonedBit()
			for v2 in v.t.joinList:
				v2.setClonedBit()
		else:
			# Set clone bit in v and all joined nodes.
			v.clearClonedBit()
			for v2 in v.t.joinList:
				v2.clearClonedBit()
		c.endUpdate()
	#@-node:c.initJoinedClonedBits (changed in 3.11.1)
	#@+node:validateOutline
	# Makes sure all nodes are valid.
	
	def validateOutline (self):
	
		c = self ; root = c.rootVnode()
		if root:
			return root.validateOutlineWithParent(None)
		else:
			return true
	#@nonl
	#@-node:validateOutline
	#@+node:goToNextDirtyHeadline
	def goToNextDirtyHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		while v and not v.isDirty():
			v = v.threadNext()
		if not v:
			v = c.rootVnode()
			while v and not v.isDirty():
				v = v.threadNext()
		if v:
			c.selectVnode(v)
	#@nonl
	#@-node:goToNextDirtyHeadline
	#@+node:goToNextMarkedHeadline
	def goToNextMarkedHeadline(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		while v and not v.isMarked():
			v = v.threadNext()
		if v:
			c.beginUpdate()
			c.endEditing()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:goToNextMarkedHeadline
	#@+node:goToNextClone
	def goToNextClone(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		if not current.isCloned(): return
	
		v = current.threadNext()
		while v and v.t != current.t:
			v = v.threadNext()
			
		if not v:
			# Wrap around.
			v = c.rootVnode()
			while v and v != current and v.t != current.t:
				v = v.threadNext()
	
		if v:
			c.beginUpdate()
			c.endEditing()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:goToNextClone
	#@+node:markChangedHeadlines
	def markChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				v.setMarked()
				c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markChangedHeadlines
	#@+node:markChangedRoots
	def markChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				s = v.bodyString()
				flag, i = is_special(s,0,"@root")
				if flag:
					v.setMarked()
					c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markChangedRoots
	#@+node:markAllAtFileNodesDirty
	def markAllAtFileNodesDirty (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isAtFileNode()and not v.isDirty():
				v.setDirty()
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markAllAtFileNodesDirty
	#@+node:markAtFileNodesDirty
	def markAtFileNodesDirty (self):
	
		c = self
		v = c.currentVnode()
		if not v: return
		after = v.nodeAfterTree()
		c.beginUpdate()
		while v and v != after:
			if v.isAtFileNode() and not v.isDirty():
				v.setDirty()
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markAtFileNodesDirty
	#@+node:markClones
	def markClones (self):
	
		c = self ; current = v = c.currentVnode()
		if not v: return
		if not v.isCloned(): return
		
		v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.t == current.t:
				v.setMarked()
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:markClones
	#@+node:markHeadline
	def markHeadline (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		c.beginUpdate()
		if v.isMarked():
			v.clearMarked()
		else:
			v.setMarked()
			v.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:markHeadline
	#@+node:markSubheads
	def markSubheads(self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		while child:
			if not child.isMarked():
				child.setMarked()
				child.setDirty()
				c.setChanged(true)
			child = child.next()
		c.endUpdate()
	#@nonl
	#@-node:markSubheads
	#@+node:unmarkAll
	def unmarkAll(self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isMarked():
				v.clearMarked()
				v.setDirty()
				c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@nonl
	#@-node:unmarkAll
	#@+node:c.dragAfter
	def dragAfter(self,v,after):
	
		# es("dragAfter")
		c = self
		if not c.checkMoveWithParentWithWarning(v,after.parent(),true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			v.moveAfter(after)
			c.undoer.setUndoParams("Drag",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragAfter
	#@+node:c.dragCloneToNthChildOf (changed in 3.11.1)
	def dragCloneToNthChildOf (self,v,parent,n):
	
		c = self
		c.beginUpdate()
		# trace("v,parent,n:"+v.headString()+","+parent.headString()+","+`n`)
		clone = v.clone(v) # Creates clone & dependents, does not set undo.
		if not c.checkMoveWithParentWithWarning(clone,parent,true):
			clone.doDelete(v) # Destroys clone & dependents. Makes v the current node.
			c.endUpdate(false) # Nothing has changed.
			return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.endEditing()
		clone.setDirty()
		clone.moveToNthChildOf(parent,n)
		c.initJoinedCloneBits(clone) # Bug fix: 4/29/03
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		clone.setDirty()
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragCloneToNthChildOf (changed in 3.11.1)
	#@+node:c.dragToNthChildOf
	def dragToNthChildOf(self,v,parent,n):
	
		# es("dragToNthChildOf")
		c = self
		if not c.checkMoveWithParentWithWarning(v,parent,true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			v.moveToNthChildOf(parent,n)
			c.undoer.setUndoParams("Drag",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragToNthChildOf
	#@+node:c.sortChildren, sortSiblings
	def sortChildren(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.hasChildren(): return
		#@	<< Set the undo info for sortChildren >>
		#@+node:<< Set the undo info for sortChildren >>
		# Get the present list of children.
		children = []
		child = v.firstChild()
		while child:
			children.append(child)
			child = child.next()
		c.undoer.setUndoParams("Sort Children",v,sort=children)
		#@nonl
		#@-node:<< Set the undo info for sortChildren >>
		#@nl
		c.beginUpdate()
		c.endEditing()
		v.sortChildren()
		v.setDirty()
		c.setChanged(true)
		c.endUpdate()
		
	def sortSiblings (self):
		
		c = self ; v = c.currentVnode()
		if not v: return
		parent = v.parent()
		if not parent:
			c.sortTopLevel()
		else:
			#@		<< Set the undo info for sortSiblings >>
			#@+node:<< Set the undo info for sortSiblings >>
			# Get the present list of siblings.
			sibs = []
			sib = parent.firstChild()
			while sib:
				sibs.append(sib)
				sib = sib.next()
			c.undoer.setUndoParams("Sort Siblings",v,sort=sibs)
			#@nonl
			#@-node:<< Set the undo info for sortSiblings >>
			#@nl
			c.beginUpdate()
			c.endEditing()
			parent.sortChildren()
			parent.setDirty()
			c.setChanged(true)
			c.endUpdate()
	#@nonl
	#@-node:c.sortChildren, sortSiblings
	#@+node:c.sortTopLevel
	def sortTopLevel (self):
		
		# Create a list of vnode, headline tuples
		c = self ; v = root = c.rootVnode()
		if not v: return
		#@	<< Set the undo info for sortTopLevel >>
		#@+node:<< Set the undo info for sortTopLevel >>
		# Get the present list of children.
		sibs = []
		sib = c.rootVnode()
		while sib:
			sibs.append(sib)
			sib = sib.next()
		c.undoer.setUndoParams("Sort Top Level",v,sort=sibs)
		#@nonl
		#@-node:<< Set the undo info for sortTopLevel >>
		#@nl
		pairs = []
		while v:
			pairs.append((v.headString().lower(), v))
			v = v.next()
		# Sort the list on the headlines.
		pairs.sort()
		sortedNodes = pairs
		# Move the nodes
		c.beginUpdate()
		h,v = sortedNodes[0]
		if v != root:
			v.moveToRoot(oldRoot=root)
		for h,next in sortedNodes[1:]:
			next.moveAfter(v)
			v = next
		c.endUpdate()
	#@nonl
	#@-node:c.sortTopLevel
	#@+node:demote
	def demote(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.next(): return
		last = v.lastChild() # EKR: 3/19/03
		# Make sure all the moves will be valid.
		child = v.next()
		while child:
			if not c.checkMoveWithParentWithWarning(child,v,true):
				return
			child = child.next()
		c.beginUpdate()
		if 1: # update range...
			c.mInhibitOnTreeChanged = true
			c.endEditing()
			while v.next():
				child = v.next()
				child.moveToNthChildOf(v,v.numberOfChildren())
			v.expand()
			c.selectVnode(v)
			v.setDirty()
			c.setChanged(true)
			c.mInhibitOnTreeChanged = false
			c.initAllCloneBits() # 7/6/02
		c.endUpdate()
		c.undoer.setUndoParams("Demote",v,lastChild=last)
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:demote
	#@+node:moveOutlineDown
	#@+at 
	#@nonl
	# Moving down is more tricky than moving up; we can't move v to be a child 
	# of itself.  An important optimization:  we don't have to call 
	# checkMoveWithParentWithWarning() if the parent of the moved node remains 
	# the same.
	#@-at
	#@@c
	
	def moveOutlineDown(self):
	
		c = self
		v = c.currentVnode()
		if not v: return
		# Set next to the node after which v will be moved.
		next = v.visNext()
		while next and v.isAncestorOf(next):
			next = next.visNext()
		if not next: return
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			#@		<< Move v down >>
			#@+node:<< Move v down >>
			# Remember both the before state and the after state for undo/redo
			oldBack = v.back()
			oldParent = v.parent()
			oldN = v.childIndex()
			
			if next.hasChildren() and next.isExpanded():
				# Attempt to move v to the first child of next.
				if c.checkMoveWithParentWithWarning(v,next,true):
					v.moveToNthChildOf(next,0)
					c.undoer.setUndoParams("Move Down",v,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			else:
				# Attempt to move v after next.
				if c.checkMoveWithParentWithWarning(v,next.parent(),true):
					v.moveAfter(next)
					c.undoer.setUndoParams("Move Down",v,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			#@nonl
			#@-node:<< Move v down >>
			#@nl
			v.setDirty() # This second call is essential.
			c.selectVnode(v)# 4/23/01
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:moveOutlineDown
	#@+node:moveOutlineLeft
	def moveOutlineLeft(self):
		
		# clear_stats() ; # stat()
		c = self
		v = c.currentVnode()
		if not v: return
		parent = v.parent()
		if not parent: return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			v.moveAfter(parent)
			c.undoer.setUndoParams("Move Left",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
		# print_stats()
	#@nonl
	#@-node:moveOutlineLeft
	#@+node:moveOutlineRight
	def moveOutlineRight(self):
		
		# clear_stats() ; # stat()
		c = self
		v = c.currentVnode()
		if not v: return
		back = v.back()
		if not back: return
		if not c.checkMoveWithParentWithWarning(v,back,true): return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			n = back.numberOfChildren()
			v.moveToNthChildOf(back,n)
			c.undoer.setUndoParams("Move Right",v,
				oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 7/6/02
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
		# print_stats()
	#@nonl
	#@-node:moveOutlineRight
	#@+node:moveOutlineUp
	def moveOutlineUp(self):
	
		c = self
		v = c.currentVnode()
		if not v: return
		back = v.visBack()
		if not back: return
		back2 = back.visBack()
		c = self
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			v.setDirty()
			#@		<< Move v up >>
			#@+node:<< Move v up >>
			# Remember both the before state and the after state for undo/redo
			oldBack = v.back()
			oldParent = v.parent()
			oldN = v.childIndex()
			
			if not back2:
				# v will be the new root node
				v.moveToRoot(c.frame.rootVnode()) # 3/16/02, 5/17/02
				c.undoer.setUndoParams("Move Up",v,
					oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			elif back2.hasChildren() and back2.isExpanded():
				if c.checkMoveWithParentWithWarning(v,back2,true):
					v.moveToNthChildOf(back2,0)
					c.undoer.setUndoParams("Move Up",v,
						oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			elif c.checkMoveWithParentWithWarning(v,back2.parent(),true):
				# Insert after back2.
				v.moveAfter(back2)
				c.undoer.setUndoParams("Move Up",v,
					oldBack=oldBack,oldParent=oldParent,oldN=oldN)
			#@nonl
			#@-node:<< Move v up >>
			#@nl
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
			c.initJoinedCloneBits(v) # 10/8/03
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:moveOutlineUp
	#@+node:promote
	def promote(self):
	
		c = self
		v = c.currentVnode()
		if not v or not v.hasChildren(): return
		last = v.lastChild() # EKR: 3/19/03
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			after = v
			while v.hasChildren():
				child = v.firstChild()
				child.moveAfter(after)
				after = child
			v.setDirty()
			c.setChanged(true)
			c.selectVnode(v)
		c.endUpdate()
		c.undoer.setUndoParams("Promote",v,lastChild=last)
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@nonl
	#@-node:promote
	#@+node:c.dragCloneAfter (changed in 3.11.1)
	def dragCloneAfter (self,v,after):
	
		c = self
		c.beginUpdate()
		clone = v.clone(v) # Creates clone & dependents, does not set undo.
		# trace("v,after:"+v.headString()+","+after.headString())
		if not c.checkMoveWithParentWithWarning(clone,after.parent(),true):
			trace("invalid clone move")
			clone.doDelete(v) # Destroys clone & dependents. Makes v the current node.
			c.endUpdate(false) # Nothing has changed.
			return
		# Remember both the before state and the after state for undo/redo
		oldBack = v.back()
		oldParent = v.parent()
		oldN = v.childIndex()
		c.endEditing()
		clone.setDirty()
		clone.moveAfter(after)
		c.initJoinedCloneBits(clone) # Bug fix: 4/29/03
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		clone.setDirty()
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@nonl
	#@-node:c.dragCloneAfter (changed in 3.11.1)
	#@+node:editVnode (calls tree.editLabel)
	# Selects v: sets the focus to v and edits v.
	
	def editVnode(self,v):
	
		c = self
		# trace(v)
		if v:
			c.selectVnode(v)
			c.frame.editLabel(v)
	#@nonl
	#@-node:editVnode (calls tree.editLabel)
	#@+node:endEditing (calls tree.endEditLabel)
	# Ends the editing in the outline.
	
	def endEditing(self):
	
		self.frame.endEditLabel()
	#@-node:endEditing (calls tree.endEditLabel)
	#@+node:selectThreadBack
	def selectThreadBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.threadBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-node:selectThreadBack
	#@+node:selectThreadNext
	def selectThreadNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:selectThreadNext
	#@+node:selectVisBack
	# This has an up arrow for a control key.
	
	def selectVisBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.visBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@nonl
	#@-node:selectVisBack
	#@+node:selectVisNext
	def selectVisNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.visNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-node:selectVisNext
	#@+node:c.selectVnode (calls tree.select)
	# This is called inside commands to select a new vnode.
	
	def selectVnode(self,v,updateBeadList=true):
	
		# All updating and "synching" of nodes are now done in the event handlers!
		c = self
		c.frame.endEditLabel()
		c.frame.select(v,updateBeadList)
		c.body.setFocus()
		self.editing = false
	#@nonl
	#@-node:c.selectVnode (calls tree.select)
	#@+node:selectVnodeWithEditing
	# Selects the given node and enables editing of the headline if editFlag is true.
	
	def selectVnodeWithEditing(self,v,editFlag):
	
		c = self
		if editFlag:
			c.editVnode(v)
		else:
			c.selectVnode(v)
	#@-node:selectVnodeWithEditing
	#@+node:Syntax coloring interface
	#@+at 
	#@nonl
	# These routines provide a convenient interface to the syntax colorer.
	#@-at
	#@-node:Syntax coloring interface
	#@+node:updateSyntaxColorer
	def updateSyntaxColorer(self,v):
	
		self.frame.updateSyntaxColorer(v)
	#@-node:updateSyntaxColorer
	#@-others

class Commands (baseCommands):
	"""A class that implements most of Leo's commands."""
	pass
#@nonl
#@-node:@file leoCommands.py
#@-leo
