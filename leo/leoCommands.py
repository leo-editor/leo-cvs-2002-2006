#@+leo

#@+node:0::@file leoCommands.py
#@+body
#@@language python


#@+at
#  This class implements the most basic commands.  Subcommanders contain an ivar that points to an instance of this class.

#@-at
#@@c

from leoGlobals import *
from leoUtils import *

# Import the subcommanders.
import leoAtFile,leoFileCommands,leoImport,leoNodes,leoTangle,leoUndo

class Commands:

	#@+others
	#@+node:1:C=1:c.__init__
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
		self.openDirectory = None # 7/2/02
		
		self.expansionLevel = 0  # The expansion level of this outline.
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
		self.target_language = None # c_language
		
		self.setIvarsFromFind()
		#@-body
		#@-node:1::<< initialize ivars >>
	#@-body
	#@-node:1:C=1:c.__init__
	#@+node:2::c.__del__
	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "c.__del__"
		pass
	#@-body
	#@-node:2::c.__del__
	#@+node:3::c.__repr__
	#@+body
	def __repr__ (self):
	
		return "Commander: " + self.frame.title

	#@-body
	#@-node:3::c.__repr__
	#@+node:4:C=2:c.destroy
	#@+body
	def destroy (self):
	
		# Can't trace while destroying.
		# print "c.destroy:", `self.frame`
	
		# Remove all links from this object to other objects.
		self.frame = None
		self.fileCommands = None
		self.atFileCommands = None
		self.importCommands = None
		self.tangleCommands = None
	#@-body
	#@-node:4:C=2:c.destroy
	#@+node:5::c.setIvarsFromPrefs
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
	#@-node:5::c.setIvarsFromPrefs
	#@+node:6::c.setIvarsFromFind
	#@+body
	# This should be called whenever we need to use find values:
	# i.e., before reading or writing
	
	def setIvarsFromFind (self):
	
		c = self ; find = app().findFrame
		if find:
			find.set_ivars(c)

	#@-body
	#@-node:6::c.setIvarsFromFind
	#@+node:7:C=3:Cut & Paste Outlines
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
	#  To cut and paste between apps, just copy into an empty body first, then copy to Leo's clipboard.

	#@-at
	#@@c
	
	def pasteOutline(self):
	
		c = self ; current = c.currentVnode()
		
		try:
			s = app().root.selection_get(selection="CLIPBOARD")
		except:
			s = None # This should never happen.
	
		if not s or not c.canPasteOutline(s):
			return # This should never happen.
	
		# isLeo = len(s)>=len(prolog_string) and prolog_string==s[0:len(prolog_string)]
		isLeo = match(s,0,prolog_prefix_string)
	
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
	#@-node:7:C=3:Cut & Paste Outlines
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
	#@+node:9:C=4:Edit Body Text
	#@+node:1:C=5:convertAllBlanks
	#@+body
	def convertAllBlanks (self):
		
		c = self ; v = current = c.currentVnode()
		next = v.nodeAfterTree()
		while v and v != next:
			if v == current:
				c.convertBlanks()
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				lines = string.split(text, '\n')
				for line in lines:
					s = optimizeLeadingWhitespace(line,c.tab_width)
					if s != line: changed = true
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
	#@-body
	#@-node:1:C=5:convertAllBlanks
	#@+node:2:C=6:convertAllTabs
	#@+body
	def convertAllTabs (self):
	
		c = self ; v = current = c.currentVnode()
		next = v.nodeAfterTree()
		while v and v != next:
			if v == current:
				self.convertTabs()
			else:
				result = [] ; changed = false
				text = v.t.bodyString
				lines = string.split(text, '\n')
				for line in lines:
					i,w = skip_leading_ws_with_indent(line,0,c.tab_width)
					s = computeLeadingWhitespace(w,-abs(c.tab_width)) + line[i:] # use negative width.
					if s != line: changed = true
					result.append(s)
				if changed:
					result = string.join(result,'\n')
					v.t.setTnodeText(result)
			v.setDirty()
			v = v.threadNext()
	#@-body
	#@-node:2:C=6:convertAllTabs
	#@+node:3:C=7:convertBlanks
	#@+body
	def convertBlanks (self):
	
		c = self ; v = current = c.currentVnode()
		head, lines, tail = c.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			s = optimizeLeadingWhitespace(line,c.tab_width)
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Convert Blanks")
			setTextSelection(c.body,"1.0","1.0")
	#@-body
	#@-node:3:C=7:convertBlanks
	#@+node:4:C=8:convertTabs
	#@+body
	def convertTabs (self):
	
		c = self
		head, lines, tail = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i,w = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(w,-abs(c.tab_width)) + line[i:] # use negative width.
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Convert Tabs")
			setTextSelection(c.body,"1.0","1.0")
	#@-body
	#@-node:4:C=8:convertTabs
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
		head, lines, tail = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width-abs(c.tab_width),c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Undent")
	#@-body
	#@-node:6::dedentBody
	#@+node:7::extract (not undoable)
	#@+body
	def extract(self):
	
		c = self ; current = v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
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
		c.updateBodyPane(head,None,tail,"Can't Undo")
		c.undoer.setUndoParams("Extract",v,select=current,oldTree=v_copy)
		c.endUpdate()
	#@-body
	#@-node:7::extract (not undoable)
	#@+node:8::extractSection (not undoable)
	#@+body
	def extractSection(self):
	
		c = self ; current = v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		junk, ws = skip_leading_ws_with_indent(headline,0,c.tab_width)
		line1 = "\n" + headline
		# Create copy for undo.
		v_copy = c.copyTree(v)
		
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
		c.updateBodyPane(head,line1,tail,"Can't Undo")
		c.undoer.setUndoParams("Extract Section",v,select=current,oldTree=v_copy)
		c.endUpdate()
	#@-body
	#@-node:8::extractSection (not undoable)
	#@+node:9::extractSectionNames (not undoable)
	#@+body
	def extractSectionNames(self):
	
		c = self ; current = v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
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
		#c.undoer.clearUndoState()
		# Restore the selection.
		setTextSelection(c.body,i,j)
		c.body.focus_force()
	#@-body
	#@-node:9::extractSectionNames (not undoable)
	#@+node:10::getBodyLines
	#@+body
	def getBodyLines (self):
		
		c = self
		i, j = getTextSelection(c.body)
		if i and j: # Convert all lines containing any part of the selection.
			if c.body.compare(i,">",j): i,j = j,i
			i = c.body.index(i + "linestart")
			j = c.body.index(j + "lineend")
			head = c.body.get("1.0",i)
			tail = c.body.get(j,"end")
		else: # Convert the entire text.
			i = "1.0" ; j = "end" ; head = tail = ""
		lines = c.body.get(i,j)
		lines = string.split(lines, '\n')
		return head, lines, tail
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
		head, lines, tail = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width+abs(c.tab_width),c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			c.updateBodyPane(head,result,tail,"Indent")
	#@-body
	#@-node:12::indentBody
	#@+node:13:C=9:updateBodyPane
	#@+body
	def updateBodyPane (self,head,middle,tail,undoType):
		
		c = self ; v = c.currentVnode()
		# Update the text and set start, end.
		c.body.delete("1.0","end")
		# The caller must do rstrip.head if appropriate.
		if head and len(head) > 0:
			c.body.insert("end",head)
			start = c.body.index("end-1c")
		else: start = "1.0"
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
		c.tree.onBodyChanged(v,undoType)
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
		c.body.see("insert")
		c.body.focus_force()
		c.recolor() # 7/5/02
	#@-body
	#@-node:13:C=9:updateBodyPane
	#@-node:9:C=4:Edit Body Text
	#@+node:10:C=10:Enabling Menu Items (Commands)
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
	#@+node:10:C=11:canExtract, canExtractSection & canExtractSectionNames
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
	#@-node:10:C=11:canExtract, canExtractSection & canExtractSectionNames
	#@+node:11::canGoToNextDirtyHeadline
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
	#@-node:11::canGoToNextDirtyHeadline
	#@+node:12::canGoToNextMarkedHeadline
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
	#@-node:12::canGoToNextMarkedHeadline
	#@+node:13::canMarkChangedHeadline
	#@+body
	def canMarkChangedHeadlines (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:13::canMarkChangedHeadline
	#@+node:14::canMarkChangedRoots
	#@+body
	def canMarkChangedRoots (self):
	
		c = self ; v = c.rootVnode()
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@-body
	#@-node:14::canMarkChangedRoots
	#@+node:15::canMoveOutlineDown
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
	#@-node:15::canMoveOutlineDown
	#@+node:16::canMoveOutlineLeft
	#@+body
	def canMoveOutlineLeft (self):
	
		c = self ; v = c.currentVnode()
		if 0: # Old code: assumes multiple leftmost nodes.
			return v and v.parent()
		else: # Can't move a child of the root left.
			return v and v.parent() and v.parent().parent()
	#@-body
	#@-node:16::canMoveOutlineLeft
	#@+node:17::canMoveOutlineRight
	#@+body
	def canMoveOutlineRight (self):
	
		c = self ; v = c.currentVnode()
		return v and v.back()
	#@-body
	#@-node:17::canMoveOutlineRight
	#@+node:18::canMoveOutlineUp
	#@+body
	def canMoveOutlineUp (self):
	
		c = self ; v = c.currentVnode()
		if 1: # The permissive way.
			return v and v.visBack()
		else: # The MORE way.
			return v and v.back()
	#@-body
	#@-node:18::canMoveOutlineUp
	#@+node:19:C=12:canPasteOutline
	#@+body
	def canPasteOutline (self,s=None):
	
		c = self
		if s == None:
			try:
				s = app().root.selection_get(selection="CLIPBOARD")
			except:
				return false
	
		# trace(`s`)
		# if len(s) >= len(prolog_string) and s[0:len(prolog_string)] == prolog_string:
			
		if match(s,0,prolog_prefix_string):
			return true
		elif len(s) > 0:
			return c.importCommands.stringIsValidMoreFile(s)
		else:
			return false
	#@-body
	#@-node:19:C=12:canPasteOutline
	#@+node:20::canPromote
	#@+body
	def canPromote (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
	#@-body
	#@-node:20::canPromote
	#@+node:21:C=13:canRevert
	#@+body
	def canRevert (self):
	
		# c.mFileName will be "untitled" for unsaved files.
		c = self
		return (c.frame and c.frame.mFileName and
			len(c.frame.mFileName) > 0 and c.isChanged())
	#@-body
	#@-node:21:C=13:canRevert
	#@+node:22:C=14:canSelectThreadBack
	#@+body
	def canSelectThreadBack (self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.threadBack()
	#@-body
	#@-node:22:C=14:canSelectThreadBack
	#@+node:23:C=15:canSelectThreadNext
	#@+body
	def canSelectThreadNext (self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.threadNext()
	#@-body
	#@-node:23:C=15:canSelectThreadNext
	#@+node:24:C=16:canSelectVisBack
	#@+body
	def canSelectVisBack (self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.visBack()
	#@-body
	#@-node:24:C=16:canSelectVisBack
	#@+node:25:C=17:canSelectVisNext
	#@+body
	def canSelectVisNext (self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.visNext()
	#@-body
	#@-node:25:C=17:canSelectVisNext
	#@+node:26::canShiftBodyLeft
	#@+body
	def canShiftBodyLeft (self):
	
		c = self
		if c.body:
			s = c.body.GetValue()
			return len(s) > 0
		else:
			return false
	#@-body
	#@-node:26::canShiftBodyLeft
	#@+node:27::canShiftBodyRight
	#@+body
	def canShiftBodyRight (self):
	
		c = self
		if c.body:
			s = c.body.GetValue()
			return len(s) > 0
		else:
			return false
	#@-body
	#@-node:27::canShiftBodyRight
	#@+node:28::canSortChildren, canSortSiblings
	#@+body
	def canSortChildren (self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
		
	def canSortSiblings (self):
	
		c = self ; v = c.currentVnode()
		parent = v.parent()
		return parent and parent.hasChildren()
	#@-body
	#@-node:28::canSortChildren, canSortSiblings
	#@+node:29::canUndo & canRedo
	#@+body
	def canUndo (self):
	
		c = self
		return c.undoer.canUndo()
		
	def canRedo (self):
	
		c = self
		return c.undoer.canRedo()
	#@-body
	#@-node:29::canUndo & canRedo
	#@+node:30::canUnmarkAll
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
	#@-node:30::canUnmarkAll
	#@-node:10:C=10:Enabling Menu Items (Commands)
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
			c.selectVnode(c.rootVnode())
		c.endUpdate()
		c.expansionLevel = 1 # Reset expansion level.
	#@-body
	#@-node:1::contractAllHeadlines
	#@+node:2::contractAllSubheads
	#@+body
	# Contracts all offspring of the current node.
	
	def contractAllSubheads (self):
	
		c = self ;v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		while child:
			c.contractSubtree(child)
			child = child.next()
		c.endUpdate()
		c.selectVnode(v) # Needed?
		c.expansionLevel = 0
	#@-body
	#@-node:2::contractAllSubheads
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
	#@+node:4::contractSubheads
	#@+body
	# Contracts the children of the current node.
	
	def contractSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		while child:
			c.contractVnode(child)
			child = child.next()
		c.endUpdate()
		c.selectVnode(v) # Needed?
		c.expansionLevel = 0
	#@-body
	#@-node:4::contractSubheads
	#@+node:5::expandLevel1
	#@+body
	def expandLevel1 (self):
	
		self.expandToLevel(1)
	#@-body
	#@-node:5::expandLevel1
	#@+node:6::expandLevel2
	#@+body
	def expandLevel2 (self):
	
		self.expandToLevel(2)
	#@-body
	#@-node:6::expandLevel2
	#@+node:7::expandLevel3
	#@+body
	def expandLevel3 (self):
	
		self.expandToLevel(3)
	#@-body
	#@-node:7::expandLevel3
	#@+node:8::expandLevel4
	#@+body
	def expandLevel4 (self):
	
		self.expandToLevel(4)
	#@-body
	#@-node:8::expandLevel4
	#@+node:9::expandLevel5
	#@+body
	def expandLevel5 (self):
	
		self.expandToLevel(5)
	#@-body
	#@-node:9::expandLevel5
	#@+node:10::expandLevel6
	#@+body
	def expandLevel6 (self):
	
		self.expandToLevel(6)
	#@-body
	#@-node:10::expandLevel6
	#@+node:11::expandLevel7
	#@+body
	def expandLevel7 (self):
	
		self.expandToLevel(7)
	#@-body
	#@-node:11::expandLevel7
	#@+node:12::expandLevel8
	#@+body
	def expandLevel8 (self):
	
		self.expandToLevel(8)
	#@-body
	#@-node:12::expandLevel8
	#@+node:13::expandLevel9
	#@+body
	def expandLevel9 (self):
	
		self.expandToLevel(9)
	#@-body
	#@-node:13::expandLevel9
	#@+node:14::expandNextLevel
	#@+body
	def expandNextLevel (self):
	
		c = self
		self.expandToLevel(c.expansionLevel + 1)
	#@-body
	#@-node:14::expandNextLevel
	#@+node:15::expandAllHeadlines
	#@+body
	def expandAllHeadlines(self):
	
		c = self ; v = root = c.rootVnode()
		c.beginUpdate()
		while v:
			c.expandSubtree(v)
			v = v.next()
		c.selectVnode(root)
		c.endUpdate()
		c.expansionLevel = 0 # Reset expansion level.
	#@-body
	#@-node:15::expandAllHeadlines
	#@+node:16::expandAllSubheads
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
	#@-node:16::expandAllSubheads
	#@+node:17::expandSubheads
	#@+body
	def expandSubheads (self):
	
		c = self ; v = c.currentVnode()
		if not v: return
	
		child = v.firstChild()
		c.beginUpdate()
		c.expandVnode(v)
		while child:
			c.expandVnode(child)
			child = child.next()
		c.selectVnode(v)
		c.endUpdate()
	#@-body
	#@-node:17::expandSubheads
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
	#@+node:2::contractVnode
	#@+body
	def contractVnode (self,v):
	
		v.contract()
		self.tree.redraw()
	#@-body
	#@-node:2::contractVnode
	#@+node:3::expandSubtree
	#@+body
	def expandSubtree (self,v):
	
		c = self
		last = v.lastNode()
		while v and v != last:
			v.expand()
			v = v.threadNext()
		c.tree.redraw()
	#@-body
	#@-node:3::expandSubtree
	#@+node:4::expandToLevel
	#@+body
	def expandToLevel (self,level):
	
		c = self
		c.beginUpdate()
		# First contract everything.
		c.contractAllHeadlines()
		# Start the recursion.
		v = c.rootVnode()
		while v:
			c.expandTreeToLevelFromLevel(v,level,1)
			v = v.next()
		c.expansionLevel = level
		c.endUpdate()
	#@-body
	#@-node:4::expandToLevel
	#@+node:5::expandVnode
	#@+body
	def expandVnode (self,v):
	
		v.expand()
	#@-body
	#@-node:5::expandVnode
	#@+node:6::expandTreeToLevelFromLevel
	#@+body
	def expandTreeToLevelFromLevel (self,v,toLevel,fromLevel):
	
		if toLevel <= fromLevel: return
		c = self
		while v:
			# Expand this node.
			c.expandVnode(v)
			# Recursively expand lower levels.
			c.expandTreeToLevelFromLevel(v.firstChild(),toLevel,fromLevel + 1)
			v = v.next()
	#@-body
	#@-node:6::expandTreeToLevelFromLevel
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
				if v.isDirty() and not v.isAtFileNode():
					v.clearDirtyJoined()
				v = v.threadNext()
		# Update all derived changed markers.
		c.changed = changedFlag
		s = c.frame.top.title()
		if len(s) > 2 and not c.loading: # don't update while loading.
			if changedFlag:
				# print_stack()
				if s [0] != '*': c.frame.top.title("* " + s)
			else:
				if s[0:2]=="* ": c.frame.top.title(s[2:])
	#@-body
	#@-node:7::setChanged
	#@-node:12::Getters & Setters
	#@+node:13::Insert, Delete & Clone (Commands)
	#@+node:1:C=18:c.checkMoveWithParentWithWarning
	#@+body
	# Returns false if any node of tree is a clone of parent or any of parents ancestors.
	
	def checkMoveWithParentWithWarning (self,root,parent,warningFlag):
	
		next = root.nodeAfterTree() ; parent1 = parent
		clone_message = "Illegal move or drag: no clone may contain a clone of itself"
		while parent:
			if parent.isCloned():
				v = root
				while v and v != next:
					if v.t == parent.t:
						if warningFlag:
							alert(clone_message)
						return false
					v = v.threadNext()
			parent = parent.parent()
			
		drag_message = "Can't drag a node into its own tree"
		parent = parent1
		while parent:
			if root == parent:
				if warningFlag:
					alert(drag_message)
				return false
			parent = parent.parent()
		return true
	#@-body
	#@-node:1:C=18:c.checkMoveWithParentWithWarning
	#@+node:2:C=19:c.deleteHeadline
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
		v.setDirty() # 1/30/02: Mark @file nodes dirty!
		# Reinsert v after back, or as the first child of parent, or as the root.
		c.undoer.setUndoParams(op_name,v,select=newNode)
		v.doDelete(newNode) # doDelete destroys dependents.
		c.setChanged(true)
		c.endUpdate()
		c.validateOutline()
	#@-body
	#@-node:2:C=19:c.deleteHeadline
	#@+node:3:C=20:c.insertHeadline
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
	#@-node:3:C=20:c.insertHeadline
	#@+node:4::clone (Commands)
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
	#@-node:4::clone (Commands)
	#@+node:5:C=21:c.copyTree
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
	#@-node:5:C=21:c.copyTree
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
	#@+node:14::Mark & Unmark
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
	#@+node:3::markChangedHeadlines
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
	#@-node:3::markChangedHeadlines
	#@+node:4::markChangedRoots
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
	#@-node:4::markChangedRoots
	#@+node:5::markAllAtFileNodesDirty
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
	#@-node:5::markAllAtFileNodesDirty
	#@+node:6::markAtFileNodesDirty
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
	#@-node:6::markAtFileNodesDirty
	#@+node:7::markHeadline
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
	#@-node:7::markHeadline
	#@+node:8::markSubheads
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
	#@-node:8::markSubheads
	#@+node:9::unmarkAll
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
	#@-node:9::unmarkAll
	#@-node:14::Mark & Unmark
	#@+node:15:C=22:Moving, Dragging, Promote, Demote, Sort
	#@+node:1:C=23:c.dragAfter
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
	#@-node:1:C=23:c.dragAfter
	#@+node:2:C=24:c.dragToNthChildOf
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
	#@-node:2:C=24:c.dragToNthChildOf
	#@+node:3:C=25:c.sortChildren, sortSiblings
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
		if 1: # inside update...
			c.endEditing()
			v.sortChildren()
			v.setDirty()
			c.setChanged(true)
		c.endUpdate()
		
	def sortSiblings (self):
		
		c = self ; v = c.currentVnode()
		if not v: return
		parent = v.parent()
		if not parent: return # can't sort the top level this way.
		
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
		if 1: # inside update...
			c.endEditing()
			parent.sortChildren()
			parent.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@-body
	#@-node:3:C=25:c.sortChildren, sortSiblings
	#@+node:4::demote
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
	#@-node:4::demote
	#@+node:5:C=26:moveOutlineDown
	#@+body
	#@+at
	#  Moving down is more tricky than moving up; we can't move v to be a child of itself.  An important optimization:  we don't 
	# have to call checkMoveWithParentWithWarning() if the parent of the moved node remains the same.

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
	#@-node:5:C=26:moveOutlineDown
	#@+node:6::moveOutlineLeft
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
	#@-node:6::moveOutlineLeft
	#@+node:7::moveOutlineRight
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
	#@-node:7::moveOutlineRight
	#@+node:8:C=27:moveOutlineUp
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
	#@-node:8:C=27:moveOutlineUp
	#@+node:9::promote
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
	#@-node:9::promote
	#@-node:15:C=22:Moving, Dragging, Promote, Demote, Sort
	#@+node:16::Selecting & Updating (commands)
	#@+node:1:C=28:editVnode (calls tree.editLabel)
	#@+body
	# Selects v: sets the focus to v and edits v.
	
	def editVnode(self,v):
	
		c = self
		if v:
			c.selectVnode(v)
			c.tree.editLabel(v)
	#@-body
	#@-node:1:C=28:editVnode (calls tree.editLabel)
	#@+node:2::endEditing (calls tree.endEditLabel)
	#@+body
	# Ends the editing in the outline.
	
	def endEditing(self):
	
		self.tree.endEditLabel()

	#@-body
	#@-node:2::endEditing (calls tree.endEditLabel)
	#@+node:3:C=29:selectThreadBack
	#@+body
	def selectThreadBack(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.threadBack()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
			c.frame.canvas.focus_force()
	#@-body
	#@-node:3:C=29:selectThreadBack
	#@+node:4:C=30:selectThreadNext
	#@+body
	def selectThreadNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
	
		v = current.threadNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
			c.frame.canvas.focus_force()
	#@-body
	#@-node:4:C=30:selectThreadNext
	#@+node:5:C=31:selectVisBack
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
			c.frame.canvas.focus_force()
	#@-body
	#@-node:5:C=31:selectVisBack
	#@+node:6:C=32:selectVisNext
	#@+body
	def selectVisNext(self):
	
		c = self ; current = c.currentVnode()
		if not current: return
		
		v = current.visNext()
		if v:
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
			c.frame.canvas.focus_force()
	#@-body
	#@-node:6:C=32:selectVisNext
	#@+node:7::c.selectVnode (calls tree.select)
	#@+body
	# This is called inside commands to select a new vnode.
	
	def selectVnode(self,v):
	
		# All updating and "synching" of nodes are now done in the event handlers!
		c = self
		c.tree.endEditLabel()
		c.tree.select(v)
		c.body.mark_set("insert","1.0")
		# c.body.see("1.0")
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
