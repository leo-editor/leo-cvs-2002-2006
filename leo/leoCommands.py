#@+leo

#@+node:0::@file leoCommands.py

#@+body

#@+at
#  This class implements the most basic commands.  All other commanders contain an commands ivar that points to an instance of 
# this class.

#@-at

#@@c

from leoGlobals import *
from leoUtils import *

import leoAtFile
import leoFileCommands
import leoTangle

class Commands:
	
#@<< Commands constants >>

	#@+node:1::<< Commands constants >>

	#@+body
	# The code assumes that the "redo" constants are one more than the corresponding "undo" constants.
	
	CANT_UNDO = 0
	UNDO_CLONE = 1 ; REDO_CLONE = 2
	UNDO_DELETE_OUTLINE = 3 ; REDO_DELETE_OUTLINE = 4
	UNDO_DEMOTE = 5 ; REDO_DEMOTE = 6
	UNDO_DRAG = 7 ; REDO_DRAG = 8
	UNDO_INSERT_OUTLINE = 9 ; REDO_INSERT_OUTLINE = 10
	UNDO_MOVE = 11 ; REDO_MOVE = 12
	UNDO_PROMOTE = 13 ; REDO_PROMOTE = 14
	#@-body

	#@-node:1::<< Commands constants >>


	#@+others

	#@+node:2::c.__init__

	#@+body
	def __init__(self,frame):
	
		# trace("__init__", "c.__init__")
		self.frame = frame
		self.initIvars(frame)
	
		# initialize the sub-commanders
		self.fileCommands = leoFileCommands.fileCommands(self)
		self.atFileCommands = leoAtFile.atFile(self)
		# self.importCommands = leoImportCommands.importCommands(self)
		self.tangleCommands = leoTangle.tangleCommands(self)
	
	def initIvars(self, frame):
		
	#@<< initialize ivars >>

		#@+node:1::<< initialize ivars >>

		#@+body
		# per-document info...
		self.expansionLevel = 0  # The expansion level of this outline.
		self.changed = false # true if any data has been changed since the last save.
		self.loading = false # true if we are loading a file: disables c.setChanged()
		
		# undo info...
		self.undoDVnodes = None  # Undo info for delete.
		self.undoLastChild = None  # Undo info for promote & demote.
		self.undoType = 0  # Set by Commands::setUndoParams...
		self.undoVnode = self.undoParent = self.undoBack = None
		self.undoN = 0
		
		# copies of frame info
		self.body = frame.body
		self.log = frame.log
		self.tree = frame.tree
		self.canvas = frame.canvas
		
		# For tangle/untangle
		self.tangle_errrors = 0
		
		self.setIvarsFromPrefs()
		self.setIvarsFromFind()
		#@-body

		#@-node:1::<< initialize ivars >>

	#@-body

	#@-node:2::c.__init__

	#@+node:3::c.__del__

	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "c.__del__"
		pass
	#@-body

	#@-node:3::c.__del__

	#@+node:4::c.__repr__

	#@+body
	def __repr__ (self):
	
		return "Commander: " + self.frame.title

	#@-body

	#@-node:4::c.__repr__

	#@+node:5:C=1:c.destroy

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

	#@-node:5:C=1:c.destroy

	#@+node:6::c.setIvarsFromPrefs

	#@+body
	# This should be called whenever we need to use preference:
	# i.e., before reading, writing, tangling, untangling.
	
	def setIvarsFromPrefs (self):
	
		c = self ; prefs = app().prefsFrame
		if prefs:
			prefs.set_ivars(c)
	#@-body

	#@-node:6::c.setIvarsFromPrefs

	#@+node:7::c.setIvarsFromFind

	#@+body
	# This should be called whenever we need to use find values:
	# i.e., before reading or writing
	
	def setIvarsFromFind (self):
	
		c = self ; find = app().findFrame
		if find:
			find.set_ivars(c)

	#@-body

	#@-node:7::c.setIvarsFromFind

	#@+node:8:C=2:Cut & Paste Outlines

	#@+node:1::cutOutline

	#@+body
	def cutOutline(self):
	
		c = self
		if c.canDeleteHeadline():
			c.copyOutline()
			c.deleteHeadline()
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
		app().clipboard = s
	
		# This is not essential for cutting and pasting between apps.
		if 0:
			if len(s) > 0:
				app().root.clipboard_clear()
				app().root.clipboard_append(s)
	#@-body

	#@-node:2::copyOutline

	#@+node:3::pasteOutline

	#@+body

	#@+at
	#  To cut and paste between apps, just copy into an empty body first, then copy to Leo's clipboard.

	#@-at

	#@@c
	
	def pasteOutline(self):
	
		c = self ; s = app().clipboard
		if not c.canPasteOutline(s):
			es("The clipboard is not a valid outline")
			return
	
		isLeo = len(s)>=len(prolog_string) and prolog_string==s[0:len(prolog_string)]
	
		# trace(`s`)
		if isLeo:
			v = c.fileCommands.getLeoOutline(s)
		else:
			v = c.convertMoreStringsToOutlineAfter(s,current) ## s used to be a stringlist
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
			c.endUpdate()
			c.recolor()
		else:
			es("The clipboard is not a valid " + choose(isLeo,"Leo","MORE") + " file")
	#@-body

	#@-node:3::pasteOutline

	#@-node:8:C=2:Cut & Paste Outlines

	#@+node:9::Drawing Utilities

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

	#@-node:9::Drawing Utilities

	#@+node:10:C=3:Edit Body Text

	#@+node:1::convertBlanks

	#@+body
	def convertBlanks (self):
	
		c = self ; v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			s = optimizeLeadingWhitespace(line,c.tab_width)
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			self.updateBodyPane(head,result,tail)
	#@-body

	#@-node:1::convertBlanks

	#@+node:2::createLastChildNode

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

	#@-node:2::createLastChildNode

	#@+node:3::dedentBody

	#@+body
	def dedentBody (self):
	
		c = self ; v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width-c.tab_width,c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			self.updateBodyPane(head,result,tail)
	#@-body

	#@-node:3::dedentBody

	#@+node:4::extract

	#@+body
	def extract(self):
	
		c = self ; v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		
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
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			result.append(line[i:])
		# Create a new node from lines.
		body = string.join(result,'\n')
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		self.createLastChildNode(v,headline,body)
		self.updateBodyPane(head,None,tail)
		c.endUpdate()
	#@-body

	#@-node:4::extract

	#@+node:5::extractSection

	#@+body
	def extractSection(self):
	
		c = self ; v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		if not lines: return
		headline = lines[0] ; del lines[0]
		
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
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			result.append(line[i:])
		# Create a new node from lines.
		body = string.join(result,'\n')
		if head and len(head) > 0:
			head = string.rstrip(head)
		c.beginUpdate()
		self.createLastChildNode(v,headline,body)
		self.updateBodyPane(head,None,tail)
		c.endUpdate()
	#@-body

	#@-node:5::extractSection

	#@+node:6::extractSectionNames

	#@+body
	def extractSectionNames(self):
	
		c = self ; v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		if not lines: return
		# Save the selection.
		i, j = self.getBodySelection()
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
		# Restore the selection.
		setTextSelection(c.body,i,j)
		c.body.focus_force()
	#@-body

	#@-node:6::extractSectionNames

	#@+node:7::getBodyLines

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

	#@-node:7::getBodyLines

	#@+node:8::getBodySelection

	#@+body
	def getBodySelection (self):
	
		c = self
		i, j = getTextSelection(c.body)
		if i and j and c.body.compare(i,">",j):
			i,j = j,i
		return i, j
	#@-body

	#@-node:8::getBodySelection

	#@+node:9::indentBody

	#@+body
	def indentBody (self):
	
		c = self ; v = c.currentVnode()
		head, lines, tail = self.getBodyLines()
		result = [] ; changed = false
		for line in lines:
			i, width = skip_leading_ws_with_indent(line,0,c.tab_width)
			s = computeLeadingWhitespace(width+c.tab_width,c.tab_width) + line[i:]
			if s != line: changed = true
			result.append(s)
		if changed:
			result = string.join(result,'\n')
			self.updateBodyPane(head,result,tail)
	#@-body

	#@-node:9::indentBody

	#@+node:10::updateBodyPane

	#@+body
	def updateBodyPane (self,head,middle,tail):
		
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
		c.tree.onBodyChanged()
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
	#@-body

	#@-node:10::updateBodyPane

	#@-node:10:C=3:Edit Body Text

	#@+node:11:C=4:Enabling Menu Items (Commands)

	#@+node:1::canContractAllHeadlines

	#@+body
	def canContractAllHeadlines(self):
	
		c = self
		v = c.tree.rootVnode
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
	def canContractAllSubheads(self):
	
		c = self
		v = c.tree.currentVnode
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
	def canContractSubheads(self):
	
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
	def canDeleteHeadline(self):
	
		c = self ; v = c.tree.currentVnode
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
	def canDemote(self):
	
		c = self
		v = c.tree.currentVnode
		if not v: return false
		return v.next() != None
	#@-body

	#@-node:6::canDemote

	#@+node:7::canExpandAllHeadlines

	#@+body
	def canExpandAllHeadlines(self):
	
		c = self
		v = c.tree.rootVnode
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
	def canExpandAllSubheads(self):
	
		c = self
		v = c.tree.currentVnode
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
	def canExpandSubheads(self):
	
		c = self
		v = c.tree.currentVnode
		if not v: return false
		v = v.firstChild()
		while v:
			if not v.isExpanded():
				return true
			v = v.next()
		return false
	#@-body

	#@-node:9::canExpandSubheads

	#@+node:10:C=5:canExtract, canExtractSection & canExtractSectionNames

	#@+body
	def canExtract(self):
	
		c = self
		if c.body:
			i, j = getTextSelection(c.body)
			return i and j and c.body.compare(i, "!=", j)
		else:
			return false
	
	canExtractSection = canExtract
	canExtractSectionNames = canExtract
	#@-body

	#@-node:10:C=5:canExtract, canExtractSection & canExtractSectionNames

	#@+node:11::canGoToNextDirtyHeadline

	#@+body
	def canGoToNextDirtyHeadline(self):
	
		c = self
		current = c.tree.currentVnode
		if not current: return false
		v = c.tree.rootVnode
		while v:
			if v.isDirty()and v != current:
				return true
			v = v.threadNext()
		return false
	#@-body

	#@-node:11::canGoToNextDirtyHeadline

	#@+node:12::canGoToNextMarkedHeadline

	#@+body
	def canGoToNextMarkedHeadline(self):
	
		c = self
		current = c.tree.currentVnode
		if not current: return false
		v = c.tree.rootVnode
		while v:
			if v.isMarked()and v != current:
				return true
			v = v.threadNext()
		return false
	#@-body

	#@-node:12::canGoToNextMarkedHeadline

	#@+node:13::canMarkChangedHeadline

	#@+body
	def canMarkChangedHeadlines(self):
	
		c = self
		v = c.tree.rootVnode
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@-body

	#@-node:13::canMarkChangedHeadline

	#@+node:14::canMarkChangedRoots

	#@+body
	def canMarkChangedRoots(self):
	
		c = self
		v = c.tree.rootVnode
		while v:
			if v.isDirty():
				return true
			v = v.threadNext()
		return false
	#@-body

	#@-node:14::canMarkChangedRoots

	#@+node:15::canMoveOutlineDown

	#@+body
	def canMoveOutlineDown(self):
	
		c = self
		if 1: # The permissive way
			current = c.tree.currentVnode
			if not current: return false
			v = current.visNext()
			while v and current.isAncestorOf(v):
				v = v.visNext()
			return v != None
		else: # The MORE way.
			return c.tree.currentVnode.next() != None
	#@-body

	#@-node:15::canMoveOutlineDown

	#@+node:16::canMoveOutlineLeft

	#@+body
	def canMoveOutlineLeft(self):
	
		c = self
		v = c.tree.currentVnode
		if 0: # Old code: assumes multiple leftmost nodes.
			return v and v.parent()
		else: # Can't move a child of the root left.
			return v and v.parent() and v.parent().parent()
	#@-body

	#@-node:16::canMoveOutlineLeft

	#@+node:17::canMoveOutlineRight

	#@+body
	def canMoveOutlineRight(self):
	
		c = self
		v = c.tree.currentVnode
		return v and v.back()
	#@-body

	#@-node:17::canMoveOutlineRight

	#@+node:18::canMoveOutlineUp

	#@+body
	def canMoveOutlineUp(self):
	
		c = self
		v = c.tree.currentVnode
		if 1: # The permissive way.
			return v and v.visBack()
		else: # The MORE way.
			return v and v.back()
	#@-body

	#@-node:18::canMoveOutlineUp

	#@+node:19:C=6:canPasteOutline

	#@+body
	def canPasteOutline(self, s=None):
	
		c = self
		if s == None: s = app().clipboard
	
		# trace(`s`)
		if s and len(s) >= len(prolog_string) and s[0:len(prolog_string)] == prolog_string:
			return true
		else:
			return false ## not yet.
			return c.stringsAreValidMoreFile(s)
	#@-body

	#@-node:19:C=6:canPasteOutline

	#@+node:20::canPromote

	#@+body
	def canPromote(self):
	
		c = self
		v = c.tree.currentVnode
		return v and v.hasChildren()
	#@-body

	#@-node:20::canPromote

	#@+node:21:C=7:canRevert

	#@+body
	def canRevert(self):
	
		# c.mFileName will be "untitled" for unsaved files.
		c = self
		return ( c.frame and c.frame.mFileName and
			len(c.frame.mFileName) > 0 and c.isChanged() )
	#@-body

	#@-node:21:C=7:canRevert

	#@+node:22:C=8:canSelectThreadBack

	#@+body
	def canSelectThreadBack(self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.threadBack()
	#@-body

	#@-node:22:C=8:canSelectThreadBack

	#@+node:23:C=9:canSelectThreadNext

	#@+body
	def canSelectThreadNext(self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.threadNext()
	#@-body

	#@-node:23:C=9:canSelectThreadNext

	#@+node:24:C=10:canSelectVisBack

	#@+body
	def canSelectVisBack(self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.visBack()
	#@-body

	#@-node:24:C=10:canSelectVisBack

	#@+node:25:C=11:canSelectVisNext

	#@+body
	def canSelectVisNext(self):
	
		c = self ; v = c.currentVnode()
		w = c.frame.top.focus_get()
		return w == c.canvas and v and v.visNext()
	#@-body

	#@-node:25:C=11:canSelectVisNext

	#@+node:26::canShiftBodyLeft

	#@+body
	def canShiftBodyLeft(self):
	
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
	def canShiftBodyRight(self):
	
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
	def canSortChildren(self):
	
		c = self ; v = c.currentVnode()
		return v and v.hasChildren()
		
	def canSortSiblings(self):
	
		c = self ; v = c.currentVnode()
		parent = v.parent()
		return parent and parent.hasChildren()
	#@-body

	#@-node:28::canSortChildren, canSortSiblings

	#@+node:29::canUnmarkAll

	#@+body
	# Returns true if any node is marked.
	
	def canUnmarkAll(self):
	
		c = self
		v = c.tree.rootVnode
		while v:
			if v.isMarked():
				return true
			v = v.threadNext()
		return false
	#@-body

	#@-node:29::canUnmarkAll

	#@-node:11:C=4:Enabling Menu Items (Commands)

	#@+node:12::Expand & Contract

	#@+node:1::Commands

	#@+node:1::contractAllHeadlines

	#@+body
	def contractAllHeadlines(self):
	
		c = self
		current = c.tree.currentVnode
		v = c.tree.rootVnode
		c.beginUpdate()
		while v:
			c.contractSubtree(v)
			v = v.next()
		if not current.isVisible():
			c.selectVnode(c.tree.rootVnode)
		c.endUpdate()
		c.expansionLevel = 1 # Reset expansion level.
	#@-body

	#@-node:1::contractAllHeadlines

	#@+node:2::contractAllSubheads

	#@+body
	# Contracts all offspring of the current node.
	
	def contractAllSubheads(self):
	
		c = self
		v = c.tree.currentVnode
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
	
	def contractSubheads(self):
	
		c = self
		v = c.tree.currentVnode
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
	def expandLevel1(self):
	
		self.expandToLevel(1)
	#@-body

	#@-node:5::expandLevel1

	#@+node:6::expandLevel2

	#@+body
	def expandLevel2(self):
	
		self.expandToLevel(2)
	#@-body

	#@-node:6::expandLevel2

	#@+node:7::expandLevel3

	#@+body
	def expandLevel3(self):
	
		self.expandToLevel(3)
	#@-body

	#@-node:7::expandLevel3

	#@+node:8::expandLevel4

	#@+body
	def expandLevel4(self):
	
		self.expandToLevel(4)
	#@-body

	#@-node:8::expandLevel4

	#@+node:9::expandLevel5

	#@+body
	def expandLevel5(self):
	
		self.expandToLevel(5)
	#@-body

	#@-node:9::expandLevel5

	#@+node:10::expandLevel6

	#@+body
	def expandLevel6(self):
	
		self.expandToLevel(6)
	#@-body

	#@-node:10::expandLevel6

	#@+node:11::expandLevel7

	#@+body
	def expandLevel7(self):
	
		self.expandToLevel(7)
	#@-body

	#@-node:11::expandLevel7

	#@+node:12::expandLevel8

	#@+body
	def expandLevel8(self):
	
		self.expandToLevel(8)
	#@-body

	#@-node:12::expandLevel8

	#@+node:13::expandLevel9

	#@+body
	def expandLevel9(self):
	
		self.expandToLevel(9)
	#@-body

	#@-node:13::expandLevel9

	#@+node:14::expandNextLevel

	#@+body
	def expandNextLevel(self):
	
		c = self
		self.expandToLevel(c.expansionLevel + 1)
	#@-body

	#@-node:14::expandNextLevel

	#@+node:15::expandAllHeadlines

	#@+body
	def expandAllHeadlines(self):
	
		c = self
		v = root = c.tree.rootVnode
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
	def expandAllSubheads(self):
	
		c = self
		v = c.tree.currentVnode
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
	def expandSubheads(self):
	
		c = self
		v = c.tree.currentVnode
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
	def contractSubtree(self,v):
	
		c = self
		last = v.lastNode()
		while v and v != last:
			v.contract()
			v = v.threadNext()
	#@-body

	#@-node:1::contractSubtree

	#@+node:2::contractVnode

	#@+body
	def contractVnode(self,v):
	
		v.contract()
		self.tree.redraw()
	#@-body

	#@-node:2::contractVnode

	#@+node:3::expandSubtree

	#@+body
	def expandSubtree(self,v):
	
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
	def expandToLevel(self,level):
	
		c = self
		c.beginUpdate()
		# First contract everything.
		c.contractAllHeadlines()
		# Start the recursion.
		v = c.tree.rootVnode
		while v:
			c.expandTreeToLevelFromLevel(v,level,1)
			v = v.next()
		c.expansionLevel = level
		c.endUpdate()
	#@-body

	#@-node:4::expandToLevel

	#@+node:5::expandVnode

	#@+body
	def expandVnode(self,v):
	
		c = self
		v.expand()
	#@-body

	#@-node:5::expandVnode

	#@+node:6::expandTreeToLevelFromLevel

	#@+body
	def expandTreeToLevelFromLevel(self,v,toLevel,fromLevel):
	
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

	#@-node:12::Expand & Contract

	#@+node:13::Getters & Setters

	#@+node:1::c.currentVnode

	#@+body
	# Compatibility with scripts
	
	def currentVnode (self):
	
		return self.tree.currentVnode

	#@-body

	#@-node:1::c.currentVnode

	#@+node:2::clearAllMarked

	#@+body
	def clearAllMarked(self):
	
		c = self
		v = c.tree.rootVnode
		while v:
			v.clearMarked()
			v = v.threadNext()
	#@-body

	#@-node:2::clearAllMarked

	#@+node:3::clearAllVisited

	#@+body
	def clearAllVisited(self):
	
		c = self
		v = c.tree.rootVnode
		
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
	def setChanged(self,changedFlag):
	
		c = self
		if not c.frame: return
		# Clear all dirty bits _before_ setting the caption.
		# 9/15/01 Clear all dirty bits except orphaned @file nodes
		if not changedFlag:
			v = c.tree.rootVnode
			while v:
				if v.isDirty() and not v.isAtFileNode():
					v.clearDirtyJoined()
				v = v.threadNext()
		# Update all derived changed markers.
		c.changed = changedFlag
		s = c.frame.top.title()
		if len(s) > 2 and not c.loading: # don't update while loading.
			if changedFlag:
				if s [0] != '*': c.frame.top.title("* " + s)
			else:
				if s[0:2]=="* ": c.frame.top.title(s[2:])
	#@-body

	#@-node:7::setChanged

	#@-node:13::Getters & Setters

	#@+node:14::Insert, Delete & Clone (Commands)

	#@+node:1::checkMoveWithParentWithWarning

	#@+body
	# Returns false if any node of tree is a clone of parent or any of parents ancestors.
	
	def checkMoveWithParentWithWarning(self,tree,parent,warningFlag):
	
		c = self
		next = tree.nodeAfterTree()
		message = "Illegal move or drag: no clone may contain a clone of itself"
		while parent:
			if parent.isCloned():
				v = tree
				while v and v != next:
					if v.t== parent.t:
						if warningFlag:
							alert(message)
						return false
					v = v.threadNext()
			parent = parent.parent()
		return true
	#@-body

	#@-node:1::checkMoveWithParentWithWarning

	#@+node:2::clone (Commands)

	#@+body
	def clone(self):
	
		c = self ; v = c.tree.currentVnode
		if not v: return
		c.beginUpdate()
		clone = v.clone(v)
		if clone:
			clone.setDirty() # essential in Leo2
			c.setChanged(true)
			if c.validateOutline():
				c.selectVnode(clone)
				c.setUndoParams(Commands.UNDO_CLONE,clone)
		c.endUpdate() # updates all icons
	#@-body

	#@-node:2::clone (Commands)

	#@+node:3::deleteHeadline

	#@+body
	# Deletes the current vnode and dependent nodes. Does nothing if the outline would become empty.
	
	def deleteHeadline(self):
	
		c = self
		v = c.tree.currentVnode
		if not v: return
		vBack = v.visBack()
		# Bug fix: 1/18/00: if vBack is NULL we are at the top level,
		# the next node should be v.next(), _not_ v.visNext();
		if vBack: newNode = vBack
		else: newNode = v.next()
		if not newNode: return
		c.setUndoParams(Commands.UNDO_DELETE_OUTLINE,v)
		c.endEditing()# Make sure we capture the headline for Undo.
		c.beginUpdate()
		v.setDirty() # 1/30/02: Mark @file nodes dirty!
		c.undoDVnodes = v.doDelete(newNode) # doDelete destroys dependents.
		c.setChanged(true)
		c.endUpdate()
		c.validateOutline()
	#@-body

	#@-node:3::deleteHeadline

	#@+node:4::initAllCloneBits

	#@+body

	#@+at
	#  This function initializes all clone bits in the entire outline's tree.

	#@-at

	#@@c
	
	def initAllCloneBits(self):
	
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

	#@-node:4::initAllCloneBits

	#@+node:5::insertHeadline

	#@+body
	# Inserts a vnode after the current vnode.  All details are handled by the vnode class.
	
	def insertHeadline(self):
	
		c = self ; current = c.tree.currentVnode
		if not current: return
		c.beginUpdate()
		if 1: # inside update...
			if current.hasChildren() and current.isExpanded():
				v = current.insertAsNthChild(0)
			else:
				v = current.insertAfter()
			v.createDependents() # To handle effects of clones.
			c.setUndoParams(Commands.UNDO_INSERT_OUTLINE,v)
			c.selectVnode(v)
			v.setDirty() # Essential in Leo2.
			c.setChanged(true)
		c.endUpdate()
		c.editVnode(v)
	#@-body

	#@-node:5::insertHeadline

	#@+node:6::validateOutline

	#@+body
	# Makes sure all nodes are valid.
	
	def validateOutline(self):
	
		c = self
		root = c.tree.rootVnode
		if root:
			return root.validateOutlineWithParent(None)
		else:
			return true
	#@-body

	#@-node:6::validateOutline

	#@-node:14::Insert, Delete & Clone (Commands)

	#@+node:15::Mark & Unmark

	#@+node:1::goToNextDirtyHeadline

	#@+body
	def goToNextDirtyHeadline(self):
	
		c = self
		current = c.tree.currentVnode
		if not current: return
		v = current.threadNext()
		while v and not v.isDirty():
			v = v.threadNext()
		if not v:
			v = c.tree.rootVnode
			while v and not v.isDirty():
				v = v.threadNext()
		if v:
			c.selectVnode(v)
	#@-body

	#@-node:1::goToNextDirtyHeadline

	#@+node:2::goToNextMarkedHeadline

	#@+body
	def goToNextMarkedHeadline(self):
	
		c = self
		current = c.tree.currentVnode
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
	def markChangedHeadlines(self):
	
		c = self
		v = c.tree.rootVnode
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
	def markChangedRoots(self):
	
		c = self
		v = c.tree.rootVnode
		c.beginUpdate()
		while v:
			if v.isDirty()and not v.isMarked():
				s = v.t.bodyString
				flag, i = is_special(s,"@root")
				if flag:
					v.setMarked()
					c.setChanged(true)
			v = v.threadNext()
		c.endUpdate()
	#@-body

	#@-node:4::markChangedRoots

	#@+node:5::markAllAtFileNodesDirty

	#@+body
	def markAllAtFileNodesDirty(self):
	
		c = self
		v = c.tree.rootVnode
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
	def markAtFileNodesDirty(self):
	
		c = self
		v = c.tree.currentVnode
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
	def markHeadline(self):
	
		c = self ; v = c.tree.currentVnode
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
	
		c = self ; v = c.tree.currentVnode
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
	
		c = self ; v = c.tree.rootVnode
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

	#@-node:15::Mark & Unmark

	#@+node:16::Moving, Promote, Demote, Sort

	#@+node:1::demote

	#@+body
	def demote(self):
	
		c = self ; v = c.tree.currentVnode
		if not v or not v.next(): return
		# Make sure all the moves will be valid.
		child = v.next()
		while child:
			if not c.checkMoveWithParentWithWarning(child,v,true):
				return
			child = child.next()
		c.setUndoParams(Commands.UNDO_DEMOTE,v)
		c.beginUpdate()
		c.mInhibitOnTreeChanged = true
		c.endEditing()
		while v.next():
			child = v.next()
			child.moveToNthChildOf(v,v.numberOfChildren())
			c.undoLastChild = child # For undo.
		c.expandVnode(v)
		c.selectVnode(v)
		v.setDirty()
		c.setChanged(true)
		c.mInhibitOnTreeChanged = false
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body

	#@-node:1::demote

	#@+node:2::moveOutlineDown

	#@+body

	#@+at
	#  Moving down is more tricky than moving up; we can't move v to be a child of itself.  An important optimization:  we don't 
	# have to call checkMoveWithParentWithWarning() if the parent of the moved node remains the same.

	#@-at

	#@@c
	
	def moveOutlineDown(self):
	
		c = self
		v = c.tree.currentVnode
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
			if next.hasChildren() and next.isExpanded():
				# Attempt to move v to the first child of next.
				if c.checkMoveWithParentWithWarning(v,next,true):
					c.setUndoParams(Commands.UNDO_MOVE,v)
					v.moveToNthChildOf(next,0)
			else:
				# Attempt to move v after next.
				if c.checkMoveWithParentWithWarning(v,next.parent(),true):
					c.setUndoParams(Commands.UNDO_MOVE,v)
					v.moveAfter(next)
			#@-body

			#@-node:1::<< Move v down >>

			v.setDirty() # This second call is essential.
			c.selectVnode(v)# 4/23/01
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body

	#@-node:2::moveOutlineDown

	#@+node:3::moveOutlineLeft

	#@+body
	def moveOutlineLeft(self):
	
		c = self
		v = c.tree.currentVnode
		if not v: return
		parent = v.parent()
		if not parent: return
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			c.setUndoParams(Commands.UNDO_MOVE,v)
			v.setDirty()
			v.moveAfter(parent)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body

	#@-node:3::moveOutlineLeft

	#@+node:4::moveOutlineRight

	#@+body
	def moveOutlineRight(self):
	
		c = self
		v = c.tree.currentVnode
		if not v: return
		back = v.back()
		if not back: return
		if not c.checkMoveWithParentWithWarning(v,back,true): return
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			c.setUndoParams(Commands.UNDO_MOVE,v)
			v.setDirty()
			n = back.numberOfChildren()
			v.moveToNthChildOf(back,n)
			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body

	#@-node:4::moveOutlineRight

	#@+node:5::moveOutlineUp

	#@+body
	def moveOutlineUp(self):
	
		c = self
		v = c.tree.currentVnode
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
			if not back2:
				# v will be the new root node
				c.setUndoParams(Commands.UNDO_MOVE,v)
				back.moveAfter(v)
			elif back2.hasChildren() and back2.isExpanded():
				if c.checkMoveWithParentWithWarning(v,back2,true):
					c.setUndoParams(Commands.UNDO_MOVE,v)
					v.moveToNthChildOf(back2,0)
			elif c.checkMoveWithParentWithWarning(v,back2.parent(),true):
				# Insert after back2.
				c.setUndoParams(Commands.UNDO_MOVE,v)
				v.moveAfter(back2)
			#@-body

			#@-node:1::<< Move v up >>

			v.setDirty()
			c.selectVnode(v)
			c.setChanged(true)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body

	#@-node:5::moveOutlineUp

	#@+node:6::promote

	#@+body
	def promote(self):
	
		c = self
		v = c.tree.currentVnode
		if not v or not v.hasChildren(): return
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			after = v
			c.setUndoParams(Commands.UNDO_PROMOTE,v)
			while v.hasChildren():
				child = v.firstChild()
				child.moveAfter(after)
				after = child
				c.undoLastChild = child # for undo.
			v.setDirty()
			c.setChanged(true)
			c.selectVnode(v)
		c.endUpdate()
		c.updateSyntaxColorer(v) # Moving can change syntax coloring.
	#@-body

	#@-node:6::promote

	#@+node:7:C=12:sortChildren, sortSiblings

	#@+body
	def sortChildren(self):
	
		c = self ; v = c.currentVnode()
		if not v or not v.hasChildren(): return
	
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			# For now, sorting can not be undone.
			v.sortChildren()
			v.setDirty()
			c.setChanged(true)
		c.endUpdate()
		
	def sortSiblings (self):
		
		c = self ; v = c.currentVnode()
		if not v: return
		parent = v.parent()
		if not parent: return # can't sort the top level this way.
	
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			# For now, sorting can not be undone.
			parent.sortChildren()
			parent.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@-body

	#@-node:7:C=12:sortChildren, sortSiblings

	#@-node:16::Moving, Promote, Demote, Sort

	#@+node:17::Selecting & Updating (commands)

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

	#@+node:3:C=13:selectThreadBack

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

	#@-node:3:C=13:selectThreadBack

	#@+node:4:C=14:selectThreadNext

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

	#@-node:4:C=14:selectThreadNext

	#@+node:5:C=15:selectVisBack

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

	#@-node:5:C=15:selectVisBack

	#@+node:6:C=16:selectVisNext

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

	#@-node:6:C=16:selectVisNext

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

	#@-node:17::Selecting & Updating (commands)

	#@+node:18::Syntax coloring interface

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

	#@-node:18::Syntax coloring interface

	#@+node:19::Undo

	#@+body

	#@+at
	#  The following routines handle the many details associated with undoing an outline operation. All operations that may be 
	# undone call setUndoParams()to remember enough information to undo the operation.

	#@-at

	#@-body

	#@+node:1::canUndo

	#@+body
	def canUndo(self):
	
		c = self
		return c.undoType != Commands.CANT_UNDO
	#@-body

	#@-node:1::canUndo

	#@+node:2::undoCaption

	#@+body
	def undoCaption(self):
	
		captionDict = {} ## not ready yet
		c = self
		if captionDict.has_key(c.undoType):
			return captionDict[c.undoType]
		else:
			return "Undo"
	#@-body

	#@-node:2::undoCaption

	#@+node:3::findSharedVnode

	#@+body
	def findSharedVnode(self,target):
	
		c = self
		v = c.tree.rootVnode
		t = target.t
		while v:
			if v != target and v.t== t:
				return v
			v = v.threadNext()
		return None
	#@-body

	#@-node:3::findSharedVnode

	#@+node:4::setUndoParams

	#@+body

	#@+at
	#  This routine saves enough information so an operation can be undone.  This routine should be called before performing the 
	# operation so that the previous state is saved.

	#@-at

	#@@c
	
	def setUndoParams(self,undo_type,v):
	
		# Remember the undo parameters
		c = self
		c.undoType = undo_type
		c.undoVnode = v
		c.undoParent = v.parent()
		c.undoBack = v.back()
		c.undoN = choose(c.undoParent, v.childIndex(), 0)
	#@-body

	#@-node:4::setUndoParams

	#@+node:5::undo

	#@+body

	#@+at
	#  This function and its allies, undoPromote() and undoDenote(), undo the operation described by the undo parmaters.

	#@-at

	#@@c
	
	def undo(self):
	
		c = self
		if c.undoType == Commands.CANT_UNDO: return
		current = c.tree.currentVnode
		if current:
			vBack = vNext = shared = None
			
	#@<< save the undo vars in local vars >>

			#@+node:1::<< save the undo vars in local vars >>

			#@+body

			#@+at
			#  setUndoParams will alter the undo variables, so we preserve these variables by copying them to local vars.

			#@-at

			#@@c
			
			old_type = c.undoType
			v = c.undoVnode
			parent = c.undoParent
			back = c.undoBack
			dv = c.undoDVnodes
			undoN = c.undoN
			#@-body

			#@-node:1::<< save the undo vars in local vars >>

			c.beginUpdate()
			
	#@<< clone cases >>

			#@+node:2::<< clone cases >>

			#@+body
			# We can immediately delete c because clone() can recreate it using only v.
			if c.undoType == Commands.UNDO_CLONE:
			
				c.selectVnode(v)
				c.deleteHeadline()
				c.undoType = Commands.REDO_CLONE
			
			elif c.undoType == Commands.REDO_CLONE:
				v = current.restoreOutlineFromDVnodes(dv,parent,back)
				shared = c.findSharedVnode(v)
				if shared: v.joinTreeTo(shared)
				v.createDependents()
				if v.shouldBeClone():
					# Optimizations make setting the icon a bit tricky.
					v.iconVal = -1 ; v.setClonedBit()
				c.initAllCloneBits()
				c.undoDVnodes = None
				c.setUndoParams(Commands.UNDO_CLONE,v)
				c.selectVnode(v)
			#@-body

			#@-node:2::<< clone cases >>

			
	#@<< insert cases >>

			#@+node:4::<< insert cases >>

			#@+body
			elif c.undoType == Commands.UNDO_INSERT_OUTLINE:
			
				vBack = v.visBack() ; vNext = v.visNext()
				c.endEditing()# Make sure we capture the headline for a redo.
				if vBack or vNext: # new logic: 1/18/00
					newVnode = choose(vBack,vBack,vNext)
					c.undoDVnodes = v.doDelete(newVnode)
					c.undoType = Commands.REDO_INSERT_OUTLINE
					c.selectVnode(choose(vBack,vBack,vNext))
			
			elif c.undoType == Commands.REDO_INSERT_OUTLINE:
			
				v = current.restoreOutlineFromDVnodes(dv,parent,back)
				c.undoDVnodes = None
				c.setUndoParams(Commands.UNDO_INSERT_OUTLINE,v)
				if v: c.selectVnode(v)
			#@-body

			#@-node:4::<< insert cases >>

			
	#@<< delete cases >>

			#@+node:3::<< delete cases >>

			#@+body

			#@+at
			#  Deleting a clone is _not_ the same as undoing a clone: the clone may have been moved, so there is no necessary 
			# relationship between the two nodes.
			# 
			# parent,back and n indicate where the new node is to be placed.

			#@-at

			#@@c
			
			elif c.undoType == Commands.UNDO_DELETE_OUTLINE:
			
				v = current.restoreOutlineFromDVnodes(dv,parent,back)
				shared = c.findSharedVnode(v)
				if shared: v.joinTreeTo(shared)
				v.createDependents()
				if v.shouldBeClone():
					# Optimizations make setting the icon a bit tricky.
					v.iconVal = 1 ; v.setClonedBit()
				c.initAllCloneBits()
				c.undoDVnodes = None
				c.setUndoParams(Commands.REDO_DELETE_OUTLINE,v)
				c.selectVnode(v)
			
			elif c.undoType == Commands.REDO_DELETE_OUTLINE:
			
				c.selectVnode(v)
				c.deleteHeadline()
			#@-body

			#@-node:3::<< delete cases >>

			
	#@<< move cases >>

			#@+node:5::<< move cases >>

			#@+body
			elif (
				c.undoType == Commands.UNDO_MOVE or
				c.undoType == Commands.REDO_MOVE):
			
				c.setUndoParams(
					choose(old_type==Commands.UNDO_MOVE,
						Commands.REDO_MOVE,Commands.UNDO_MOVE), v)
				if parent:
					v.moveToNthChildOf(parent,n)
				elif back:
					v.moveAfter(back)
				else:
					v.moveToRoot()
				c.selectVnode(v)
			
			elif (
				c.undoType == Commands.UNDO_DRAG or
				c.undoType == Commands.REDO_DRAG):
			
				c.setUndoParams(
					choose(old_type==Commands.UNDO_DRAG,
						Commands.REDO_DRAG, Commands.UNDO_DRAG), v)
				v.moveToNthChildOf(parent,n)
				c.selectVnode(v)
			#@-body

			#@-node:5::<< move cases >>

			
	#@<< promote and demote cases >>

			#@+node:6::<< promote and demote cases >>

			#@+body

			#@+at
			#  Promote and demote operations are the hardest to undo, because they involve relinking a list of nodes. We pass the 
			# work off to routines dedicated to the task.

			#@-at

			#@@c
			
			elif c.undoType == Commands.UNDO_DEMOTE:
				c.undoDemote()
				assert(c.undoType == Commands.REDO_DEMOTE)
			
			elif c.undoType == Commands.REDO_DEMOTE:
				c.selectVnode(v)
				c.demote()
				assert(c.undoType == Commands.UNDO_DEMOTE)
			
			elif c.undoType == Commands.UNDO_PROMOTE:
				c.undoPromote()
				assert(c.undoType == Commands.REDO_PROMOTE)
			
			elif c.undoType == Commands.REDO_PROMOTE:
				c.selectVnode(v)
				c.promote()
				assert(c.undoType == Commands.UNDO_PROMOTE)
			#@-body

			#@-node:6::<< promote and demote cases >>

			c.setChanged(true)
			if v: v.setDirty()
			c.endUpdate()
	#@-body

	#@-node:5::undo

	#@+node:6::undoDemote

	#@+body
	# undoes the previous demote operation.
	def undoDemote(self):
	
		c = self
		ins = v = c.undoVnode
		last = c.undoLastChild
		child = v.firstChild()
		assert(child and last)
		c.setUndoParams(Commands.REDO_DEMOTE,v)
		c.beginUpdate()
		while 1:
			save_next = child.next()
			child.moveAfter(ins)
			ins = child
			c.undoLastChild = child
			child = save_next
			assert(ins == last or child)
			if ins == last: break
		c.selectVnode(v)
		c.endUpdate()
	#@-body

	#@-node:6::undoDemote

	#@+node:7::undoPromote

	#@+body
	# Undoes the previous promote operation.
	def undoPromote(self):
	
		v = v1 = c.undoVnode
		assert(v1)
		last = c.undoLastChild
		next = v.next()
		assert(next and last)
		c.setUndoParams(Commands.REDO_PROMOTE,v1)
		c.beginUpdate()
		while 1:
			v = next
			ASSERT(v)
			next = v.next()
			n = v1.numberOfChildren()
			v.moveToNthChildOf(v1,n)
			c.undoLastChild = v
			if v == last: break
		c.selectVnode(v1)
		c.endUpdate()
	#@-body

	#@-node:7::undoPromote

	#@-node:19::Undo

	#@-others

#@-body

#@-node:0::@file leoCommands.py

#@-leo
