#@+leo
#@+node:0::@file leoCommands.py
#@+body
#@@language python


#@+at
#  This class implements the most basic commands.  Subcommanders contain an 
# ivar that points to an instance of this class.

#@-at
#@@c

from leoGlobals import *

# Import the subcommanders.
import leoAtFile,leoFileCommands,leoImport,leoNodes,leoTangle,leoUndo

class Commands:

	#@+others
	#@+node:1::c.__del__
	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "c.__del__"
		pass
	#@-body
	#@-node:1::c.__del__
	#@+node:2::c.__init__ & initIvars
	#@+body
	def __init__(self,frame):
	
		# trace("__init__", "c.__init__")
		self.frame = frame
		self.initIvars(frame)
	
		# initialize the sub-commanders
		self.fileCommands = leoFileCommands.fileCommands(self)
		self.atFileCommands = leoAtFile.atFile(self)
		self.importCommands = leoImport.leoImportCommands(self)
		self.tangleCommands = leoTangle.tangleCommands(self)
		self.undoer = leoUndo.undoer(self)
	
	def initIvars(self, frame):
		
		#@<< initialize ivars >>
		#@+node:1::<< initialize ivars >>
		#@+body
		# per-document info...
		self.hookFunction = None
		self.openDirectory = None # 7/2/02
		
		self.expansionLevel = 0  # The expansion level of this outline.
		self.expansionNode = None # The last node we expanded or contracted.
		self.changed = false # true if any data has been changed since the last save.
		self.loading = false # true if we are loading a file: disables c.setChanged()
		
		# copies of frame info
		self.body = frame.body
		self.log = frame.log
		self.tree = frame.tree
		self.canvas = frame.canvas
		
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
		
		self.setIvarsFromFind()
		#@-body
		#@-node:1::<< initialize ivars >>
	#@-body
	#@-node:2::c.__init__ & initIvars
	#@+node:3::c.__repr__
	#@+body
	def __repr__ (self):
		
		try:
			return "Commander: " + self.frame.mFileName
		except:
			return "Commander: bad mFileName"
	
	#@-body
	#@-node:3::c.__repr__
	#@+node:4::c.destroy
	#@+body
	def destroy (self):
	
		# Can't trace while destroying.
		# print "c.destroy:", self.frame
	
		# Remove all links from this object to other objects.
		self.frame = None
		self.fileCommands = None
		self.atFileCommands = None
		self.importCommands = None
		self.tangleCommands = None
	#@-body
	#@-node:4::c.destroy
	#@+node:5::c.setIvarsFromFind
	#@+body
	# This should be called whenever we need to use find values:
	# i.e., before reading or writing
	
	def setIvarsFromFind (self):
	
		c = self ; find = app().findFrame
		if find:
			find.set_ivars(c)
	
	#@-body
	#@-node:5::c.setIvarsFromFind
	#@+node:6::c.setIvarsFromPrefs
	#@+body
	#@+at
	#  This should be called whenever we need to use preference:
	# i.e., before reading, writing, tangling, untangling.
	# 
	# 7/2/02: We no longer need this now that the Prefs dialog is modal.

	#@-at
	#@@c

	def setIvarsFromPrefs (self):
	
		pass
	#@-body
	#@-node:6::c.setIvarsFromPrefs
	#@+node:7::Cut & Paste Outlines
	#@+node:1::cutOutline
	#@+body
	def cutOutline(self):
	
		c = self
		if c.canDeleteHeadline():
			c.copyOutline()
			c.deleteHeadline("Cut Node")
			c.recolor()
	#@-body
	#@-node:1::cutOutline
	#@+node:2::copyOutline
	#@+body
	def copyOutline(self):
	
		c = self
		c.endEditing()
		c.fileCommands.assignFileIndices()
		s = c.fileCommands.putLeoOutline()
		# trace(`s`)
		app().root.clipboard_clear()
		app().root.clipboard_append(s)
		# Copying an outline has no undo consequences.
	
	#@-body
	#@-node:2::copyOutline
	#@+node:3::pasteOutline
	#@+body
	#@+at
	#  To cut and paste between apps, just copy into an empty body first, then 
	# copy to Leo's clipboard.

	#@-at
	#@@c

	def pasteOutline(self):
	
		a = app() ; c = self ; current = c.currentVnode()
		
		try:
			s = a.root.selection_get(selection="CLIPBOARD")
		except:
			s = None # This should never happen.
	
		if not s or not c.canPasteOutline(s):
			return # This should never happen.
	
		isLeo = match(s,0,a.prolog_prefix_string)
	
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
	#@-body
	#@-node:3::pasteOutline
	#@-node:7::Cut & Paste Outlines
	#@+node:8::Drawing Utilities
	#@+node:1::beginUpdate
	#@+body
	def beginUpdate(self):
	
		self.tree.beginUpdate()
		
	BeginUpdate = beginUpdate # Compatibility with old scripts
	#@-body
	#@-node:1::beginUpdate
	#@+node:2::bringToFront
	#@+body
	def bringToFront(self):
	
		self.frame.top.deiconify()
	
	BringToFront = bringToFront # Compatibility with old scripts
	#@-body
	#@-node:2::bringToFront
	#@+node:3::endUpdate
	#@+body
	def endUpdate(self, flag=true):
		
		self.tree.endUpdate(flag)
		
	EndUpdate = endUpdate # Compatibility with old scripts
	#@-body
	#@-node:3::endUpdate
	#@+node:4::recolor
	#@+body
	def recolor(self):
	
		tree = self.tree
		tree.recolor(tree.currentVnode)
	#@-body
	#@-node:4::recolor
	#@+node:5::redraw & repaint
	#@+body
	def redraw(self):
	
		self.tree.redraw()
		
	# Compatibility with old scripts
	Redraw = redraw 
	repaint = redraw
	Repaint = redraw
	#@-body
	#@-node:5::redraw & repaint
	#@-node:8::Drawing Utilities
	#@+node:9::Edit Body Text
	#@+node:1::convertAllBlanks
	#@+body
	def convertAllBlanks (self):
		
		c = self ; v = current = c.currentVnode()
		next = v.nodeAfterTree()
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.copyTree(v)
		anyChanged = false
		while v and v != next:
			if v == current:
				c.convertBlanks()
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				lines = string.split(text, '\n')
				for line in lines:
					s = optimizeLeadingWhitespace(line,tabWidth)
					if s != line:
						changed = true ; anyChanged = true
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
		if anyChanged:
			c.undoer.setUndoParams("Convert All Blanks",current,select=current,oldTree=v_copy)
		else:
			es("nothing changed")
	#@-body
	#@-node:1::convertAllBlanks
	#@+node:2::convertAllTabs
	#@+body
	def convertAllTabs (self):
	
		c = self ; v = current = c.currentVnode()
		next = v.nodeAfterTree()
		dict = scanDirectives(c)
		tabWidth  = dict.get("tabwidth")
		# Create copy for undo.
		v_copy = c.copyTree(v)
		anyChanged = false
		while v and v != next:
			if v == current:
				self.convertTabs()
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				lines = string.split(text, '\n')
				for line in lines:
					i,w = skip_leading_ws_with_indent(line,0,tabWidth)
					s = computeLeadingWhitespace(w,-abs(tabWidth)) + line[i:] # use negative width.
					if s != line:
						changed = true ; anyChanged = true
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
		if anyChanged:
			c.undoer.setUndoParams("Convert All Tabs",current,select=current,oldTree=v_copy)
		else:
			es("nothing changed")
	
	
	#@-body
	#@-node:2::convertAllTabs
	#@+node:3::convertBlanks
	#@+body
	def convertBlanks (self):
	
		c = self ; v = current = c.currentVnode()
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
			c.updateBodyPane(head,result,tail,"Convert Blanks",oldSel,oldYview) # Handles undo
			setTextSelection(c.body,"1.0","1.0")
	
	#@-body
	#@-node:3::convertBlanks
	#@+node:4::convertTabs
	#@+body
	def convertTabs (self):
	
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
			c.updateBodyPane(head,result,tail,"Convert Tabs",oldSel,oldYview) # Handles undo
			setTextSelection(c.body,"1.0","1.0")
	#@-body
	#@-node:4::convertTabs
	#@+node:5::createLastChildNode
	#@+body
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
	#@-body
	#@-node:5::createLastChildNode
	#@+node:6::dedentBody
	#@+body
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
	#@-body
	#@-node:6::dedentBody
	#@+node:7::extract (undo clears undo buffer)
	#@+body
	def extract(self):
	
		c = self ; current = v = c.currentVnode()
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		# Create copy for undo.
		v_copy = c.copyTree(v)
		
		#@<< Set headline for extract >>
		#@+node:1::<< Set headline for extract >>
		#@+body
		headline = string.strip(headline)
		while len(headline) > 0 and headline[0] == '/':
			headline = headline[1:]
		headline = string.strip(headline)
		#@-body
		#@-node:1::<< Set headline for extract >>

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
		c.createLastChildNode(v,headline,body)
		undoType =  "Can't Undo" # 12/8/02: None enables further undoes, but there are bugs now.
		c.updateBodyPane(head,None,tail,undoType,oldSel,oldYview)
		c.undoer.setUndoParams("Extract",v,select=current,oldTree=v_copy)
		c.endUpdate()
	#@-body
	#@-node:7::extract (undo clears undo buffer)
	#@+node:8::extractSection (undo clears undo buffer)
	#@+body
	def extractSection(self):
	
		c = self ; current = v = c.currentVnode()
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		line1 = "\n" + headline
		# Create copy for undo.
		v_copy = c.copyTree(v)
		#trace("v:     " + `v`)
		#trace("v_copy:" + `v_copy`)
		
		#@<< Set headline for extractSection >>
		#@+node:1::<< Set headline for extractSection >>
		#@+body
		while len(headline) > 0 and headline[0] == '/':
			headline = headline[1:]
		headline = string.strip(headline)
		
		# Make sure we have a @< or <<
		if headline[0:2] != '<<' and headline[0:2] != '@<': return
		#@-body
		#@-node:1::<< Set headline for extractSection >>

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
		c.createLastChildNode(v,headline,body)
		undoType =  "Can't Undo" # 2/8/02: None enables further undoes, but there are bugs now.
		c.updateBodyPane(head,line1,tail,undoType,oldSel,oldYview)
		c.undoer.setUndoParams("Extract Section",v,select=current,oldTree=v_copy)
		c.endUpdate()
	
	#@-body
	#@-node:8::extractSection (undo clears undo buffer)
	#@+node:9::extractSectionNames
	#@+body
	def extractSectionNames(self):
	
		c = self ; current = v = c.currentVnode()
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		if not lines: return
		# Save the selection.
		i, j = self.getBodySelection()
		# Create copy for undo.
		v_copy = c.copyTree(v)
		c.beginUpdate()
		for s in lines:
			
			#@<< Find the next section name >>
			#@+node:1::<< Find the next section name >>
			#@+body
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
			#@-body
			#@-node:1::<< Find the next section name >>

			if name: self.createLastChildNode(v,name,None)
		c.selectVnode(v)
		c.validateOutline()
		c.endUpdate()
		c.undoer.setUndoParams("Extract Names",v,select=current,oldTree=v_copy)
		# Restore the selection.
		setTextSelection(c.body,i,j)
		c.body.focus_force()
	#@-body
	#@-node:9::extractSectionNames
	#@+node:10::getBodyLines
	#@+body
	def getBodyLines (self):
		
		c = self
		oldYview = c.frame.body.yview()
		i, j = getTextSelection(c.body)
		oldSel = (i,j) # 11/21/02: for undo.
			# 12-SEP-2002 DTHEIN
			# i is index to first character in the selection
		# j is index to first character following the selection
		# if selection was made from back to front, then i and j are reversed
		if i and j: # Convert all lines containing any part of the selection.
			if c.body.compare(i,">",j): i,j = j,i
			i = c.body.index(i + "linestart")
			# 12-SEP-2002 DTHEIN: don't include following line in selection
			endSel = j # position of last character of selection
			trailingNewline = ""
			line,col = j.split(".")
			if col == "0":  # DTHEIN: selection ends at start of next line
				endSel = c.body.index(j + "- 1 chars")
				trailingNewline = '\n'
			else: # DTHEIN: selection ends in the midst of a line
				endSel = c.body.index(j + "lineend")
				j = endSel
			head = c.body.get("1.0",i)
			tail = c.body.get(j,"end")
		else: # Convert the entire text.
			i = "1.0" ; j = "end" ; head = tail = ""
			endSel = c.body.index(j + "- 1 chars") # 14-SEP-2002 DTHEIN
			trailingNewline = ""
		if i == endSel:
			head = tail = None ; lines = []
		else:
			lines = c.body.get(i,endSel)
			lines = string.split(lines, '\n')
			lines[-1] += trailingNewline # DTHEIN: add newline if needed
		return head,lines,tail,oldSel,oldYview
	#@-body
	#@-node:10::getBodyLines
	#@+node:11::getBodySelection
	#@+body
	def getBodySelection (self):
	
		c = self
		i, j = getTextSelection(c.body)
		if i and j and c.body.compare(i,">",j):
			i,j = j,i
		return i, j
	#@-body
	#@-node:11::getBodySelection
	#@+node:12::indentBody
	#@+body
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
	#@-body
	#@-node:12::indentBody
	#@+node:13::reformatParagraph
	#@+body
	def reformatParagraph(self):
		"""Reformat a text paragraph in a Tk.Text widget
	
	Wraps the concatenated text to present page width setting.
	Leading tabs are sized to present tab width setting.
	First and second line of original text is used to determine leading whitespace
	in reformatted text.  Hanging indentation is honored.
	
	Paragraph is bound by start of body, end of body, blank lines, and lines
	starting with "@".  Paragraph is selected by position of current insertion
	cursor."""
	
		c = self ; body = c.frame.body
		x = body.index("current")
		head,lines,tail,oldSel,oldYview = self.getBodyLines()
		result = []
	
		dict = scanDirectives(c)
		pageWidth = dict.get("pagewidth")
		tabWidth  = dict.get("tabwidth")
		# trace(`tabWidth`+","+`pageWidth`)
	
		# If active selection, then don't attempt a reformat.
		selStart, selEnd = getTextSelection(body)
		if selStart != selEnd: return
	
		# Find the paragraph range.
		data = bound_paragraph(body)
		if data:
			start, end, endsWithNL = data
			firstLine = int(float(start)) - 1 # subtract 1 to get on zero basis
			lastLine = int(float(end)) - 1
		else: return
		
		# Compute the leading whitespace.
		indents = [0,0] ; leading_ws = ["",""] # Bug fix: 11/16/02
		for i in (0,1):
			if firstLine + i < len(lines):
				# Use the original, non-optimized leading whitespace.
				leading_ws[i] = ws = get_leading_ws(lines[firstLine+i])
				indents[i] = computeWidth(ws,tabWidth)
		indents[1] = max(indents)
		# 11/17/02: Bug fix suggested by D.T.Hein.
		if 1 == (lastLine - firstLine):
			leading_ws[1] = leading_ws[0]
	
	    # Put the leading unchanged lines.
		for i in range(0,firstLine):
			result.append(lines[i])
			
		# Wrap the lines, decreasing the page width by indent.
		wrapped_lines = \
		    wrap_lines(lines[firstLine:lastLine],pageWidth-indents[1],pageWidth-indents[0])
		lineCount = len(wrapped_lines)
			
		i = 0
		for line in wrapped_lines:
			result.append(leading_ws[i] + line)
			if i < 1: i += 1
	
		# Put the trailing unchanged lines.
		for i in range(lastLine,len(lines)):
			result.append(lines[i])
	
		# Replace the text if it changed.
		for i in range(firstLine,lineCount+firstLine):
			if i >= lastLine or lines[i] != result[i]:
				result = string.join(result,'\n')
				c.updateBodyPane(head,result,tail,"Reformat Paragraph",oldSel,oldYview) # Handles undo
				break
	
		
		#@<< Set the new insert at the start of the next paragraph >>
		#@+node:1::<< Set the new insert at the start of the next paragraph >>
		#@+body
		lastLine = firstLine + lineCount
		if not endsWithNL:
			insPos = str(lastLine) + ".0lineend"
		else:
			endPos = body.index("end")
			endLine = int(float(endPos))
			lastLine += 1
			insPos = str(lastLine) + ".0"
			while lastLine < endLine:
				s = body.get(insPos,insPos + "lineend")
				if s and (0 < len(s)) and not s.isspace():
					break;
				lastLine += 1
				insPos = str(lastLine) + ".0"
		setTextSelection(body,insPos,insPos)
		#@-body
		#@-node:1::<< Set the new insert at the start of the next paragraph >>

	
		# Make sure we can see the new cursor.
		body.see("insert-5l")
	#@-body
	#@-node:13::reformatParagraph
	#@+node:14::updateBodyPane (handles undo)
	#@+body
	def updateBodyPane (self,head,middle,tail,undoType,oldSel,oldYview):
		
		c = self ; v = c.currentVnode()
		# Update the text and set start, end.
		c.body.delete("1.0","end")
		# The caller must do rstrip.head if appropriate.
		if head and len(head) > 0:
			c.body.insert("end",head)
			start = c.body.index("end-1c")
		else: start = "1.0"
		if 0: # 9/12/02: Do not gratuitously remove newlines!
			if middle and len(middle) > 0:
				middle = string.rstrip(middle)
		if middle and len(middle) > 0:
			c.body.insert("end",middle)
			end = c.body.index("end-1c")
		else: end = start
		if tail and len(tail) > 0:
			tail = string.rstrip(tail)
		if tail and len(tail) > 0:
			c.body.insert("end",tail)
		# Activate the body key handler by hand.
		c.tree.onBodyChanged(v,undoType,oldSel=oldSel,oldYview=oldYview)
		# Update the changed mark.
		if not c.isChanged():
			c.setChanged(true)
		# Update the icon.
		c.beginUpdate()
		if not v.isDirty():
			v.setDirty()
		c.endUpdate()
		# Update the selection.
		# trace(`start` + "," + `end`)
		setTextSelection(c.body,start,end)
		if oldYview:
			first,last=oldYview
			c.body.yview("moveto",first)
		else:
			c.body.see("insert")
		c.body.focus_force()
		c.recolor() # 7/5/02
	#@-body
	#@-node:14::updateBodyPane (handles undo)
	#@-node:9::Edit Body Text
	#@+node:10::Enabling Menu Items (Commands)
	#@+node:1::canContractAllHeadlines
	#@+body
	def canContractAllHeadlines (self):
	
		c = self ; v = c.rootVnode()
		if not v: return false
		while v:
			if v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:1::canContractAllHeadlines
	#@+node:2::canContractAllSubheads
	#@+body
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
	#@-body
	#@-node:2::canContractAllSubheads
	#@+node:3::canContractParent
	#@+body
	def canContractParent (self):
	
		c = self ; v = c.currentVnode()
		return v.parent() != None
	#@-body
	#@-node:3::canContractParent
	#@+node:4::canContractSubheads
	#@+body
	def canContractSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		v = v.firstChild()
		while v:
			if v.isExpanded():
				return true
			v = v.next()
		return false
	#@-body
	#@-node:4::canContractSubheads
	#@+node:5::canCutOutline & canDeleteHeadline
	#@+body
	def canDeleteHeadline (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		if v.parent(): # v is below the top level.
			return true
		else: # v is at the top level.  We can not delete the last node.
			return v.threadBack() or v.next()
	
	canCutOutline = canDeleteHeadline
	#@-body
	#@-node:5::canCutOutline & canDeleteHeadline
	#@+node:6::canDemote
	#@+body
	def canDemote (self):
	
		c = self
		v = c.currentVnode()
		if not v: return false
		return v.next() != None
	#@-body
	#@-node:6::canDemote
	#@+node:7::canExpandAllHeadlines
	#@+body
	def canExpandAllHeadlines (self):
	
		c = self ; v = c.rootVnode()
		if not v: return false
		while v:
			if not v.isExpanded():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:7::canExpandAllHeadlines
	#@+node:8::canExpandAllSubheads
	#@+body
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
	#@-body
	#@-node:8::canExpandAllSubheads
	#@+node:9::canExpandSubheads
	#@+body
	def canExpandSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return false
		v = v.firstChild()
		while v:
			if not v.isExpanded():
				return true
			v = v.next()
		return false
	#@-body
	#@-node:9::canExpandSubheads
	#@+node:10::canExtract, canExtractSection & canExtractSectionNames
	#@+body
	def canExtract (self):
	
		c = self
		if c.body:
			i, j = getTextSelection(c.body)
			return i and j and c.body.compare(i, "!=", j)
		else:
			return false
	
	canExtractSection = canExtract
	canExtractSectionNames = canExtract
	#@-body
	#@-node:10::canExtract, canExtractSection & canExtractSectionNames
	#@+node:11::canFindMatchingBracket
	#@+body
	def canFindMatchingBracket (self):
		
		c = self ; body = c.body
		brackets = "()[]{}"
		c1=body.get("insert -1c")
		c2=body.get("insert")
		return c1 in brackets or c2 in brackets
	#@-body
	#@-node:11::canFindMatchingBracket
	#@+node:12::canGoToNextDirtyHeadline
	#@+body
	def canGoToNextDirtyHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return false
	
		v = c.rootVnode()
		while v:
			if v.isDirty()and v != current:
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:12::canGoToNextDirtyHeadline
	#@+node:13::canGoToNextMarkedHeadline
	#@+body
	def canGoToNextMarkedHeadline (self):
	
		c = self ; current = c.currentVnode()
		if not current: return false
	
		v = c.rootVnode()
		while v:
			if v.isMarked()and v != current:
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:13::canGoToNextMarkedHeadline
	#@+node:14::canMarkChangedHeadline
	#@+body
	def canMarkChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:14::canMarkChangedHeadline
	#@+node:15::canMarkChangedRoots
	#@+body
	def canMarkChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:15::canMarkChangedRoots
	#@+node:16::canMoveOutlineDown
	#@+body
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
	#@-body
	#@-node:16::canMoveOutlineDown
	#@+node:17::canMoveOutlineLeft
	#@+body
	def canMoveOutlineLeft (self):
	
		c = self ; v = c.currentVnode()
		if 0: # Old code: assumes multiple leftmost nodes.
			return v and v.parent()
		else: # Can't move a child of the root left.
			return v and v.parent() and v.parent().parent()
	#@-body
	#@-node:17::canMoveOutlineLeft
	#@+node:18::canMoveOutlineRight
	#@+body
	def canMoveOutlineRight (self):
	
		c = self ; v = c.currentVnode()
		return v and v.back()
	#@-body
	#@-node:18::canMoveOutlineRight
	#@+node:19::canMoveOutlineUp
	#@+body
	def canMoveOutlineUp (self):
	
		c = self ; v = c.currentVnode()
		if 1: # The permissive way.
			return v and v.visBack()
		else: # The MORE way.
			return v and v.back()
	#@-body
	#@-node:19::canMoveOutlineUp
	#@+node:20::canPasteOutline
	#@+body
	def canPasteOutline (self,s=None):
	
		a = app() ; c = self
		if s == None:
			try:
				s = a.root.selection_get(selection="CLIPBOARD")
			except:
				return false
	
		# trace(s)
		if match(s,0,a.prolog_prefix_string):
			return true
		elif len(s) > 0:
			return c.importCommands.stringIsValidMoreFile(s)
		else:
			return false
	#@-body
	#@-node:20::canPasteOutline
	#@+node:21::canPromote
	#@+body
	def canPromote (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
	#@-body
	#@-node:21::canPromote
	#@+node:22::canRevert
	#@+body
	def canRevert (self):
	
		# c.mFileName will be "untitled" for unsaved files.
		c = self
		return (c.frame and c.frame.mFileName and
			len(c.frame.mFileName) > 0 and c.isChanged())
	#@-body
	#@-node:22::canRevert
	#@+node:23::canSelect....
	#@+body
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
	#@-body
	#@-node:23::canSelect....
	#@+node:24::canShiftBodyLeft/Right
	#@+body
	def canShiftBodyLeft (self):
	
		c = self
		if c.body:
			s = c.body.GetValue()
			return len(s) > 0
		else:
			return false
			
	def canShiftBodyRight (self):
	
		c = self
		if c.body:
			s = c.body.GetValue()
			return len(s) > 0
		else:
			return false
	#@-body
	#@-node:24::canShiftBodyLeft/Right
	#@+node:25::canSortChildren, canSortSiblings
	#@+body
	def canSortChildren (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
		
	def canSortSiblings (self):
	
		c = self ; v = c.currentVnode()
		return v.next() or v.back()
	#@-body
	#@-node:25::canSortChildren, canSortSiblings
	#@+node:26::canUndo & canRedo
	#@+body
	def canUndo (self):
	
		c = self
		return c.undoer.canUndo()
		
	def canRedo (self):
	
		c = self
		return c.undoer.canRedo()
	#@-body
	#@-node:26::canUndo & canRedo
	#@+node:27::canUnmarkAll
	#@+body
	# Returns true if any node is marked.
	
	def canUnmarkAll (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isMarked():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:27::canUnmarkAll
	#@-node:10::Enabling Menu Items (Commands)
	#@+node:11::Expand & Contract
	#@+node:1::Commands
	#@+node:1::contractAllHeadlines
	#@+body
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
	#@-body
	#@-node:1::contractAllHeadlines
	#@+node:2::contractNode
	#@+body
	def contractNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.contract()
		c.endUpdate()
	#@-body
	#@-node:2::contractNode
	#@+node:3::contractParent
	#@+body
	def contractParent (self):
		
		c = self ; v = c.currentVnode()
		parent = v.parent()
		if not parent: return
		
		c.beginUpdate()
		c.selectVnode(parent)
		parent.contract()
		c.endUpdate()
	#@-body
	#@-node:3::contractParent
	#@+node:4::expandAllSubheads
	#@+body
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
	#@-body
	#@-node:4::expandAllSubheads
	#@+node:5::expandLevel1..9
	#@+body
	def expandLevel1 (self): self.expandToLevel(1)
	def expandLevel2 (self): self.expandToLevel(2)
	def expandLevel3 (self): self.expandToLevel(3)
	def expandLevel4 (self): self.expandToLevel(4)
	def expandLevel5 (self): self.expandToLevel(5)
	def expandLevel6 (self): self.expandToLevel(6)
	def expandLevel7 (self): self.expandToLevel(7)
	def expandLevel8 (self): self.expandToLevel(8)
	def expandLevel9 (self): self.expandToLevel(9)
	
	#@-body
	#@-node:5::expandLevel1..9
	#@+node:6::expandNextLevel
	#@+body
	def expandNextLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(c.expansionLevel + 1)
	
	#@-body
	#@-node:6::expandNextLevel
	#@+node:7::expandNode
	#@+body
	def expandNode (self):
		
		c = self ; v = c.currentVnode()
		
		c.beginUpdate()
		v.expand()
		c.endUpdate()
	
	#@-body
	#@-node:7::expandNode
	#@+node:8::expandPrevLevel
	#@+body
	def expandPrevLevel (self):
	
		c = self ; v = c.currentVnode()
		
		# 1/31/02: Expansion levels are now local to a particular tree.
		if c.expansionNode != v:
			c.expansionLevel = 1
			c.expansionNode = v
			
		self.expandToLevel(max(1,c.expansionLevel - 1))
	
	#@-body
	#@-node:8::expandPrevLevel
	#@-node:1::Commands
	#@+node:2::Utilities
	#@+node:1::contractSubtree
	#@+body
	def contractSubtree (self,v):
	
		last = v.lastNode()
		while v and v != last:
			v.contract()
			v = v.threadNext()
	#@-body
	#@-node:1::contractSubtree
	#@+node:2::expandSubtree
	#@+body
	def expandSubtree (self,v):
	
		c = self
		last = v.lastNode()
		while v and v != last:
			v.expand()
			v = v.threadNext()
		c.tree.redraw()
	#@-body
	#@-node:2::expandSubtree
	#@+node:3::expandToLevel
	#@+body
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
	#@-body
	#@-node:3::expandToLevel
	#@-node:2::Utilities
	#@-node:11::Expand & Contract
	#@+node:12::Getters & Setters
	#@+node:1::c.currentVnode
	#@+body
	# Compatibility with scripts
	
	def currentVnode (self):
	
		return self.tree.currentVnode
	
	#@-body
	#@-node:1::c.currentVnode
	#@+node:2::clearAllMarked
	#@+body
	def clearAllMarked (self):
	
		c = self ; v = c.rootVnode()
		while v:
			v.clearMarked()
			v = v.threadNext()
	#@-body
	#@-node:2::clearAllMarked
	#@+node:3::clearAllVisited
	#@+body
	def clearAllVisited (self):
	
		c = self ; v = c.rootVnode()
		
		c.beginUpdate()
		while v:
			v.clearVisited()
			if v.t:
				v.t.clearVisited()
			v = v.threadNext()
		c.endUpdate(false) # never redraw the tree.
	#@-body
	#@-node:3::clearAllVisited
	#@+node:4::fileName
	#@+body
	# Compatibility with scripts
	
	def fileName (self):
	
		return self.frame.mFileName
	
	#@-body
	#@-node:4::fileName
	#@+node:5::isChanged
	#@+body
	def isChanged (self):
	
		return self.changed
	#@-body
	#@-node:5::isChanged
	#@+node:6::rootVnode
	#@+body
	# Compatibility with scripts
	
	def rootVnode (self):
	
		return self.tree.rootVnode
	
	#@-body
	#@-node:6::rootVnode
	#@+node:7::setChanged
	#@+body
	def setChanged (self,changedFlag):
	
		c = self
		if not c.frame: return
		# Clear all dirty bits _before_ setting the caption.
		# 9/15/01 Clear all dirty bits except orphaned @file nodes
		if not changedFlag:
			v = c.rootVnode()
			while v:
				if v.isDirty() and not (v.isAtFileNode() or v.isAtRawFileNode()):
					v.clearDirtyJoined()
				v = v.threadNext()
		# Update all derived changed markers.
		c.changed = changedFlag
		s = c.frame.top.title()
		if len(s) > 2 and not c.loading: # don't update while loading.
			if changedFlag:
				# import traceback ; traceback.print_stack()
				if s [0] != '*': c.frame.top.title("* " + s)
			else:
				if s[0:2]=="* ": c.frame.top.title(s[2:])
	
	
	
	#@-body
	#@-node:7::setChanged
	#@-node:12::Getters & Setters
	#@+node:13::Insert, Delete & Clone (Commands)
	#@+node:1::c.checkMoveWithParentWithWarning
	#@+body
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
	
	#@-body
	#@-node:1::c.checkMoveWithParentWithWarning
	#@+node:2::c.deleteHeadline
	#@+body
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
	#@-body
	#@-node:2::c.deleteHeadline
	#@+node:3::c.insertHeadline
	#@+body
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
			v.setDirty() # Essential in Leo2.
			c.setChanged(true)
		c.endUpdate(false)
		c.tree.redraw_now()
		c.editVnode(v)
	#@-body
	#@-node:3::c.insertHeadline
	#@+node:4::c.clone
	#@+body
	def clone (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
		c.beginUpdate()
		clone = v.clone(v)
		if clone:
			clone.setDirty() # essential in Leo2
			c.setChanged(true)
			if c.validateOutline():
				c.selectVnode(clone)
				c.undoer.setUndoParams("Clone",clone)
		c.endUpdate() # updates all icons
	#@-body
	#@-node:4::c.clone
	#@+node:5::c.copyTree
	#@+body
	# This creates a free-floating copy of v's tree for undo.
	# The copied trees must use different tnodes than the original.
	
	def copyTree(self,root):
	
		c = self
		# Create the root vnode.
		result = v = leoNodes.vnode(c,root.t)
		# Copy the headline and icon values
		v.copyNode(root,v)
		# Copy the rest of tree.
		v.copyTree(root,v)
		# Replace all tnodes in v by copies.
		assert(v.nodeAfterTree() == None)
		while v:
			v.t = leoNodes.tnode(0, v.t.bodyString)
			v = v.threadNext()
		return result
	#@-body
	#@-node:5::c.copyTree
	#@+node:6::initAllCloneBits
	#@+body
	#@+at
	#  This function initializes all clone bits in the entire outline's tree.

	#@-at
	#@@c

	def initAllCloneBits (self):
	
		c=self
		c.clearAllVisited()
		v = self.tree.rootVnode
		c.beginUpdate()
		while v:
			if v.isVisited():
				v = v.threadNext()
				continue
			mark = v.shouldBeClone()
			# Mark all nodes joined to v.
			v2 = v.getJoinList()
			while v2 and v2 != v:
				v2.setVisited()
				# Important speedup: only change the bit if it needs changing.
				if not mark and v2.isCloned():
					v2.clearClonedBit()
				elif mark and not v2.isCloned():
					v2.setClonedBit()
				v2 = v2.getJoinList()
			# Mark v.
			v.setVisited()
			if not mark and v.isCloned():
				v.clearClonedBit()
			elif mark and not v.isCloned():
				v.setClonedBit()
			v = v.threadNext()
		c.endUpdate()
	#@-body
	#@-node:6::initAllCloneBits
	#@+node:7::initJoinedClonedBits
	#@+body
	# Initializes all clone bits in the all nodes joined to v.
	
	def initJoinedCloneBits (self,v):
	
		c = self ; v1 = v
	
		c.beginUpdate()
		if 1: # update range...
			
			#@<< init clone bit for v >>
			#@+node:1::<< init clone bit for v >>
			#@+body
			mark = v.shouldBeClone()
			if not mark and v.isCloned():
				v.clearClonedBit()
			elif mark and not v.isCloned():
				v.setClonedBit()
			#@-body
			#@-node:1::<< init clone bit for v >>

			v = v.getJoinList()
			while v and v != v1:
				
				#@<< init clone bit for v >>
				#@+node:1::<< init clone bit for v >>
				#@+body
				mark = v.shouldBeClone()
				if not mark and v.isCloned():
					v.clearClonedBit()
				elif mark and not v.isCloned():
					v.setClonedBit()
				#@-body
				#@-node:1::<< init clone bit for v >>

				v = v.getJoinList()
		c.endUpdate()
	#@-body
	#@-node:7::initJoinedClonedBits
	#@+node:8::validateOutline
	#@+body
	# Makes sure all nodes are valid.
	
	def validateOutline (self):
	
		c = self ; root = c.rootVnode()
		if root:
			return root.validateOutlineWithParent(None)
		else:
			return true
	#@-body
	#@-node:8::validateOutline
	#@-node:13::Insert, Delete & Clone (Commands)
	#@+node:14::Mark & Unmark & goto
	#@+node:1::goToNextDirtyHeadline
	#@+body
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
	#@-body
	#@-node:1::goToNextDirtyHeadline
	#@+node:2::goToNextMarkedHeadline
	#@+body
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
	#@-body
	#@-node:2::goToNextMarkedHeadline
	#@+node:3::goToNextClone
	#@+body
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
	#@-body
	#@-node:3::goToNextClone
	#@+node:4::markChangedHeadlines
	#@+body
	def markChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				v.setMarked()
				c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@-body
	#@-node:4::markChangedHeadlines
	#@+node:5::markChangedRoots
	#@+body
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
	#@-body
	#@-node:5::markChangedRoots
	#@+node:6::markAllAtFileNodesDirty
	#@+body
	def markAllAtFileNodesDirty (self):
	
		c = self ; v = c.rootVnode()
		c.beginUpdate()
		while v:
			if v.isAtFileNode()and not v.isDirty():
				v.setDirty()
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	#@-body
	#@-node:6::markAllAtFileNodesDirty
	#@+node:7::markAtFileNodesDirty
	#@+body
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
	#@-body
	#@-node:7::markAtFileNodesDirty
	#@+node:8::markClones
	#@+body
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
	#@-body
	#@-node:8::markClones
	#@+node:9::markHeadline
	#@+body
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
	#@-body
	#@-node:9::markHeadline
	#@+node:10::markSubheads
	#@+body
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
	#@-body
	#@-node:10::markSubheads
	#@+node:11::unmarkAll
	#@+body
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
	#@-body
	#@-node:11::unmarkAll
	#@-node:14::Mark & Unmark & goto
	#@+node:15::Moving, Dragging, Promote, Demote, Sort
	#@+node:1::c.dragAfter
	#@+body
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
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@-body
	#@-node:1::c.dragAfter
	#@+node:2::c.dragCloneAfter
	#@+body
	def dragCloneAfter (self,v,after):
	
		c = self
		c.beginUpdate()
		clone = v.clone(v) # Creates clone & dependents, does not set undo.
		if not c.checkMoveWithParentWithWarning(clone,after.parent(),true):
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
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		clone.setDirty()
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@-body
	#@-node:2::c.dragCloneAfter
	#@+node:3::c.dragCloneToNthChildOf
	#@+body
	def dragCloneToNthChildOf (self,v,parent,n):
	
		c = self
		c.beginUpdate()
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
		c.undoer.setUndoParams("Drag & Clone",clone,
			oldBack=oldBack,oldParent=oldParent,oldN=oldN,oldV=v)
		clone.setDirty()
		c.selectVnode(clone)
		c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(clone) # Dragging can change syntax coloring.
	#@-body
	#@-node:3::c.dragCloneToNthChildOf
	#@+node:4::c.dragToNthChildOf
	#@+body
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
		c.endUpdate()
		c.updateSyntaxColorer(v) # Dragging can change syntax coloring.
	#@-body
	#@-node:4::c.dragToNthChildOf
	#@+node:5::c.sortChildren, sortSiblings
	#@+body
	def sortChildren(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.hasChildren(): return
		
		#@<< Set the undo info for sortChildren >>
		#@+node:1::<< Set the undo info for sortChildren >>
		#@+body
		# Get the present list of children.
		children = []
		child = v.firstChild()
		while child:
			children.append(child)
			child = child.next()
		c.undoer.setUndoParams("Sort Children",v,sort=children)
		#@-body
		#@-node:1::<< Set the undo info for sortChildren >>

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
			
			#@<< Set the undo info for sortSiblings >>
			#@+node:2::<< Set the undo info for sortSiblings >>
			#@+body
			# Get the present list of siblings.
			sibs = []
			sib = parent.firstChild()
			while sib:
				sibs.append(sib)
				sib = sib.next()
			c.undoer.setUndoParams("Sort Siblings",v,sort=sibs)
			#@-body
			#@-node:2::<< Set the undo info for sortSiblings >>

			c.beginUpdate()
			c.endEditing()
			parent.sortChildren()
			parent.setDirty()
			c.setChanged(true)
			c.endUpdate()
	#@-body
	#@-node:5::c.sortChildren, sortSiblings
	#@+node:6::c.sortTopLevel
	#@+body
	def sortTopLevel (self):
		
		# Create a list of vnode, headline tuples
		c = self ; v = root = c.rootVnode()
		if not v: return
		
		#@<< Set the undo info for sortTopLevel >>
		#@+node:1::<< Set the undo info for sortTopLevel >>
		#@+body
		# Get the present list of children.
		sibs = []
		sib = c.rootVnode()
		while sib:
			sibs.append(sib)
			sib = sib.next()
		c.undoer.setUndoParams("Sort Top Level",v,sort=sibs)
		#@-body
		#@-node:1::<< Set the undo info for sortTopLevel >>

		pairs = []
		while v:
			pairs.append((v.headString().lower(), v))
			v = v.next()
		# Sort the list on the headlines.
		sortedNodes = sortSequence(pairs,0)
		# Move the nodes
		c.beginUpdate()
		h,v = sortedNodes[0]
		if v != root:
			v.moveToRoot(oldRoot=root)
		for h,next in sortedNodes[1:]:
			next.moveAfter(v)
			v = next
		c.endUpdate()
	#@-body
	#@-node:6::c.sortTopLevel
	#@+node:7::demote
	#@+body
	def demote(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.next(): return
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
			last = None
			while v.next():
				child = v.next()
				child.moveToNthChildOf(v,v.numberOfChildren())
				last = child # For undo.
			c.expandVnode(v)
			c.selectVnode(v)
			v.setDirty()
			c.setChanged(true)
			c.mInhibitOnTreeChanged = false
			c.initAllCloneBits() # 7/6/02
		c.endUpdate()
		c.undoer.setUndoParams("Demote",v,lastChild=last)
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body
	#@-node:7::demote
	#@+node:8::moveOutlineDown
	#@+body
	#@+at
	#  Moving down is more tricky than moving up; we can't move v to be a 
	# child of itself.  An important optimization:  we don't have to call 
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
			
			#@<< Move v down >>
			#@+node:1::<< Move v down >>
			#@+body
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
			#@-body
			#@-node:1::<< Move v down >>

			v.setDirty() # This second call is essential.
			c.selectVnode(v)# 4/23/01
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body
	#@-node:8::moveOutlineDown
	#@+node:9::moveOutlineLeft
	#@+body
	def moveOutlineLeft(self):
	
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
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body
	#@-node:9::moveOutlineLeft
	#@+node:10::moveOutlineRight
	#@+body
	def moveOutlineRight(self):
	
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
	#@-body
	#@-node:10::moveOutlineRight
	#@+node:11::moveOutlineUp
	#@+body
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
			
			#@<< Move v up >>
			#@+node:1::<< Move v up >>
			#@+body
			# Remember both the before state and the after state for undo/redo
			oldBack = v.back()
			oldParent = v.parent()
			oldN = v.childIndex()
			
			if not back2:
				# v will be the new root node
				v.moveToRoot(c.tree.rootVnode) # 3/16/02, 5/17/02
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
			#@-body
			#@-node:1::<< Move v up >>

			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body
	#@-node:11::moveOutlineUp
	#@+node:12::promote
	#@+body
	def promote(self):
	
		c = self
		v = c.currentVnode()
		if not v or not v.hasChildren(): return
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			after = v ; last = None
			while v.hasChildren():
				child = v.firstChild()
				child.moveAfter(after)
				after = child
				last = child # for undo.
			v.setDirty()
			c.setChanged(true)
			c.selectVnode(v)
		c.endUpdate()
		c.undoer.setUndoParams("Promote",v,lastChild=last)
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body
	#@-node:12::promote
	#@-node:15::Moving, Dragging, Promote, Demote, Sort
	#@+node:16::Selecting & Updating (commands)
	#@+node:1::editVnode (calls tree.editLabel)
	#@+body
	# Selects v: sets the focus to v and edits v.
	
	def editVnode(self,v):
	
		c = self
		if v:
			c.selectVnode(v)
			c.tree.editLabel(v)
	#@-body
	#@-node:1::editVnode (calls tree.editLabel)
	#@+node:2::endEditing (calls tree.endEditLabel)
	#@+body
	# Ends the editing in the outline.
	
	def endEditing(self):
	
		self.tree.endEditLabel()
	
	#@-body
	#@-node:2::endEditing (calls tree.endEditLabel)
	#@+node:3::selectThreadBack
	#@+body
	def selectThreadBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.threadBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	
	#@-body
	#@-node:3::selectThreadBack
	#@+node:4::selectThreadNext
	#@+body
	def selectThreadNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-body
	#@-node:4::selectThreadNext
	#@+node:5::selectVisBack
	#@+body
	# This has an up arrow for a control key.
	
	def selectVisBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.visBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	#@-body
	#@-node:5::selectVisBack
	#@+node:6::selectVisNext
	#@+body
	def selectVisNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.visNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
	
	#@-body
	#@-node:6::selectVisNext
	#@+node:7::c.selectVnode (calls tree.select)
	#@+body
	# This is called inside commands to select a new vnode.
	
	def selectVnode(self,v):
	
		# All updating and "synching" of nodes are now done in the event handlers!
		c = self
		c.tree.endEditLabel()
		c.tree.select(v)
		c.body.focus_force()
		self.editing = false
	#@-body
	#@-node:7::c.selectVnode (calls tree.select)
	#@+node:8::selectVnodeWithEditing
	#@+body
	# Selects the given node and enables editing of the headline if editFlag is true.
	
	def selectVnodeWithEditing(self,v,editFlag):
	
		c = self
		if editFlag:
			c.editVnode(v)
		else:
			c.selectVnode(v)
	
	#@-body
	#@-node:8::selectVnodeWithEditing
	#@-node:16::Selecting & Updating (commands)
	#@+node:17::Syntax coloring interface
	#@+body
	#@+at
	#  These routines provide a convenient interface to the syntax colorer.

	#@-at
	#@-body
	#@+node:1::updateSyntaxColorer
	#@+body
	def updateSyntaxColorer(self,v):
	
		self.tree.colorizer.updateSyntaxColorer(v)
	
	#@-body
	#@-node:1::updateSyntaxColorer
	#@-node:17::Syntax coloring interface
	#@-others
#@-body
#@-node:0::@file leoCommands.py
#@-leo
