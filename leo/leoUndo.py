#@+leo
#@+node:0::@file leoUndo.py
#@+body
#@@language python

# Undo manager for leo.py.


#@<< How Leo implements unlimited undo >>
#@+node:1::<< How Leo implements unlimited undo >>
#@+body
#@+at
#  Only leo.py supports unlimited undo.  Unlimited undo is straightforward; it 
# merely requires that all commands that affect the outline or body text must 
# be undoable. In other words, everything that affects the outline or body 
# text must be remembered.
# 
# We may think of all the actions that may be Undone or Redone as a string of 
# beads (undo nodes). Undoing an operation moves backwards to the next bead; 
# redoing an operation moves forwards to the next bead. A bead pointer points 
# to the present bead. The bead pointer points in front of the first bead when 
# Undo is disabled.  The bead pointer points at the last bead when Redo is 
# disabled. An undo node is a Python dictionary containing all information 
# needed to undo or redo the operation.
# 
# The Undo command uses the present bead to undo the action, then moves the 
# bead pointer backwards. The Redo command uses the bead after the present 
# bead to redo the action, then moves the bead pointer forwards. All undoable 
# operations call setUndoParams() to create a new bead. The list of beads does 
# not branch; all undoable operations (except the Undo and Redo commands 
# themselves) delete any beads following the newly created bead.
# 
# I did not invent this model of unlimited undo.  I first came across it in 
# the documentation for Apple's Yellow Box classes.

#@-at
#@-body
#@-node:1::<< How Leo implements unlimited undo >>


#@<< Define optionl ivars >>
#@+node:2::<< Define optionl ivars >>
#@+body

optionalIvars = (
	"lastChild",
	"parent","oldParent",
	"back","oldBack",
	"n","oldN",
	"oldText","newText",
	"oldSel","newSel",
	"sort","select",
	"oldTree",
	"yview",
	# For incremental undo typing...
	"leading","trailing",
	"oldMiddleLines","newMiddleLines",
	"oldNewlines","newNewlines")
#@-body
#@-node:2::<< Define optionl ivars >>

from leoGlobals import *
import types

class undoer:

	#@+others
	#@+node:3::undo.__init__
	#@+body
	def __init__ (self,commands):
		
		self.commands = commands
		
		# Ivars to transition to new undo scheme...
		
		self.debug = true # true: enable debugging code in new undo scheme.
		self.debug_print = false # true: enable print statements in debug code.
		self.new_undo = true # true: enable new debug code.
		
		# Statistics comparing old and new ways (only if self.debug is on).
		self.new_mem = 0
		self.old_mem = 0
		
		# State ivars...
	
		self.redoMenuLabel = "Can't Redo" # Set here to indicate initial menu entry.
		self.undoMenuLabel = "Can't Undo" # Set here to indicate initial menu entry.
		self.undoType = "Can't Undo"
		self.undoing = false # True if executing an Undo command.
		self.redoing = false # True if executing a Redo command.
	
		self.clearUndoState()
	#@-body
	#@+node:1::clearUndoState & clearIvars
	#@+body
	#@+at
	#  This method clears then entire Undo state.  All non-undoable commands 
	# should call this method.

	#@-at
	#@@c

	def clearUndoState (self):
		
		self.setRedoType("Can't Redo")
		self.setUndoType("Can't Undo")
		self.beads = [] # List of undo nodes.
		self.bead = -1 # Index of the present bead: -1:len(beads)
		self.clearIvars()
		
	def clearIvars (self):
		
		self.v = None # The node being operated upon for undo and redo.
		for ivar in optionalIvars:
			exec('self.%s = None' % ivar)
		
		if 0:
			# Params describing the "before" state for undo.
			self.oldParent = self.oldBack = self.oldN = None
			self.sort = None # List of nodes before being sorted.
			self.oldText = None
			# Params describing the "after" state for redo.
			self.parent = self.back = self.lastChild = self.n = None
			self.select = None
			self.newText = None
	#@-body
	#@-node:1::clearUndoState & clearIvars
	#@-node:3::undo.__init__
	#@+node:4::State routines...
	#@+node:1::canRedo & canUndo
	#@+body
	def canRedo (self):
	
		return self.redoMenuLabel != "Can't Redo"
	
	def canUndo (self):
	
		return self.undoMenuLabel != "Can't Undo"
	#@-body
	#@-node:1::canRedo & canUndo
	#@+node:2::enableMenuItems
	#@+body
	def enableMenuItems (self):
	
		u = self ; c = u.commands ; menu = c.frame.menus.get("Edit")
		enableMenu(menu,u.redoMenuLabel,u.canRedo())
		enableMenu(menu,u.undoMenuLabel,u.canUndo())
	#@-body
	#@-node:2::enableMenuItems
	#@+node:3::getBead, peekBead, setBead
	#@+body
	def getBead (self,n):
		
		u = self
		if n < 0 or n >= len(u.beads): return false
		d = u.beads[n]
		# trace(`n` + ":" + `len(u.beads)` + ":" + `d`)
		self.clearIvars()
		u.v = d["v"]
		u.undoType = d["undoType"]
	
		for ivar in optionalIvars:
			if d.has_key(ivar):
				exec('u.%s = d["%s"]' % (ivar,ivar))
			else:
				exec('u.%s = None' % ivar)
	
		if not u.new_undo: # Recreate an "oldText" entry if necessary.
			if u.undoType == "Typing" and u.oldText == None:
				assert(n > 0)
				old_d = u.beads[n-1]
				# The user will lose data if these asserts fail.
				assert(old_d["undoType"] == "Typing")
				assert(old_d["v"] == u.v)
				u.oldText = old_d["newText"]
				# trace(`u.oldText`)
		return d
		
	def peekBead (self,n):
		
		u = self
		if n < 0 or n >= len(u.beads): return false
		d = u.beads[n]
		# trace(`n` + ":" + `len(u.beads)` + ":" + `d`)
		return d
	
	def setBead (self,n,keywords=None):
	
		u = self ; d = {}
		d["undoType"]=u.undoType
		d["v"]=u.v
		# Only enter significant entries into the dictionary.
		# This is an important space optimization for typing.
		for ivar in optionalIvars:
			exec('if u.%s != None: d["%s"] = u.%s' % (ivar,ivar,ivar))
		# copy all significant keywords to d.
		if keywords:
			for key in keywords.keys():
				if keywords[key] != None:
					d[key] = keywords[key]
		# Clear the "oldText" entry if the previous entry was a "Typing" entry.
		# This optimization halves the space needed for Undo/Redo Typing.
		if not u.new_undo:
			if u.undoType == "Typing" and n > 0:
				old_d = u.beads[n-1]
				if old_d["undoType"] == "Typing" and old_d["v"] == u.v:
					del d["oldText"] # We can recreate this entry from old_d["newText"]
					# trace(`u.oldText`)
		# trace(`d`)
		return d
	#@-body
	#@-node:3::getBead, peekBead, setBead
	#@+node:4::redoMenuName, undoMenuName
	#@+body
	def redoMenuName (self,name):
	
		if name=="Can't Redo":
			return name
		else:
			return "Redo " + name
	
	def undoMenuName (self,name):
	
		if name=="Can't Undo":
			return name
		else:
			return "Undo " + name
	#@-body
	#@-node:4::redoMenuName, undoMenuName
	#@+node:5::setRedoType, setUndoType
	#@+body
	# These routines update both the ivar and the menu label.
	def setRedoType (self,type):
	
		u = self ; c = u.commands ; menu = c.frame.menus.get("Edit")
		name = u.redoMenuName(type)
		if name != u.redoMenuLabel:
			# Update menu using old name.
			setMenuLabel(menu,u.redoMenuLabel,name)
			u.redoMenuLabel = name
	
	def setUndoType (self,type):
	
		u = self ; c = u.commands ; menu = c.frame.menus.get("Edit")
		name = u.undoMenuName(type)
		if name != u.undoMenuLabel:
			# Update menu using old name.
			setMenuLabel(menu,u.undoMenuLabel,name)
			u.undoType = type
			u.undoMenuLabel = name
	#@-body
	#@-node:5::setRedoType, setUndoType
	#@+node:6::setUndoParams
	#@+body
	#@+at
	#  This routine saves enough information so an operation can be undone and 
	# redone.  We do nothing when called from the undo/redo logic because the 
	# Undo and Redo commands merely reset the bead pointer.

	#@-at
	#@@c

	def setUndoParams (self,undo_type,v,**keywords):
	
		# trace(`undo_type`)
		u = self
		if u.redoing or u.undoing: return None
		if undo_type == "Can't Undo":
			u.clearUndoState()
			return None
		# Set the type: set the menu labels later.
		u.undoType = undo_type
		# Calculate the standard derived information.
		u.v = v
		u.parent = v.parent()
		u.back = v.back()
		u.n = v.childIndex()
		# Push params on undo stack, clearing all forward entries.
		u.bead += 1
		d = u.setBead(u.bead,keywords)
		u.beads[u.bead:] = [d]
		# trace(`u.bead` + ":" + `len(u.beads)` + ":" + `keywords`)
		# Recalculate the menu labels.
		u.setUndoTypes()
		return d
	#@-body
	#@-node:6::setUndoParams
	#@+node:7::setUndoTypingParams
	#@+body
	#@+at
	#  This routine saves enough information so a typing operation can be 
	# undone and redone.
	# 
	# We do nothing when called from the undo/redo logic because the Undo and 
	# Redo commands merely reset the bead pointer.

	#@-at
	#@@c

	def setUndoTypingParams (self,v,undo_type,oldText,newText,oldSel,newSel):
	
		u = self ; c = self.commands
		if u.redoing or u.undoing: return None
		if undo_type == "Can't Undo":
			u.clearUndoState()
			return None
		if oldText == newText:
			# trace("no change")
			return None
		# Clear all optional params.
		for ivar in optionalIvars:
			exec('u.%s = None' % ivar)
		# Set the params.
		u.undoType = undo_type
		u.v = v
		
		#@<< compute leading, middle & trailing  lines >>
		#@+node:1::<< compute leading, middle & trailing  lines >>
		#@+body
		#@+at
		#  Incremental undo typing is similar to incremental syntax coloring.  
		# We compute the number of leading and trailing lines that match, and 
		# save both the old and new middle lines.
		# 
		# NB: the number of old and new middle lines may be different.

		#@-at
		#@@c

		old_lines = string.split(oldText,'\n')
		new_lines = string.split(newText,'\n')
		new_len = len(new_lines)
		old_len = len(old_lines)
		min_len = min(old_len,new_len)
		
		i = 0
		while i < min_len:
			if old_lines[i] != new_lines[i]:
				break
			i += 1
		leading = i
		
		if leading == new_len:
			# This happens when we remove lines from the end.
			# The new text is simply the leading lines from the old text.
			trailing = 0
		else:
			i = 0
			while i < min_len - leading:
				if old_lines[old_len-i-1] != new_lines[new_len-i-1]:
					break
				i += 1
			trailing = i
			
		# NB: the number of old and new middle lines may be different.
		if trailing == 0:
			old_middle_lines = old_lines[leading:]
			new_middle_lines = new_lines[leading:]
		else:
			old_middle_lines = old_lines[leading:-trailing]
			new_middle_lines = new_lines[leading:-trailing]
			
		# Remember how many trailing newlines in the old and new text.
		i = len(oldText) - 1 ; old_newlines = 0
		while i >= 0 and oldText[i] == '\n':
			old_newlines += 1
			i -= 1
		
		i = len(newText) - 1 ; new_newlines = 0
		while i >= 0 and newText[i] == '\n':
			new_newlines += 1
			i -= 1
		
		if self.debug_print:
			trace()
			print "lead,trail",`leading`,`trailing`
			print "old mid,nls:",`len(old_middle_lines)`,`old_newlines`,`oldText`
			print "new mid,nls:",`len(new_middle_lines)`,`new_newlines`,`newText`
			#print "lead,trail:",leading,trailing
			#print "old mid:",`old_middle_lines`
			#print "new mid:",`new_middle_lines`
			print "---------------------"
		#@-body
		#@-node:1::<< compute leading, middle & trailing  lines >>

		
		#@<< save undo text info >>
		#@+node:2::<< save undo text info >>
		#@+body
		#@+at
		#  This is the start of the incremental undo algorithm.
		# 
		# We must save enough info to do _both_ of the following:
		# 
		# Undo: Given newText, recreate oldText.
		# Redo: Given oldText, recreate oldText.
		# 
		# The "given" texts for the undo and redo routines are simply v.bodyString().

		#@-at
		#@@c

		if self.new_undo:
			if self.debug:
				# Remember the complete text for comparisons...
				u.oldText = oldText
				u.newText = newText
				# Compute statistics comparing old and new ways...
				# The old doesn't often store the old text, so don't count it here.
				self.old_mem += len(newText)
				s1 = string.join(old_middle_lines,'\n')
				s2 = string.join(new_middle_lines,'\n')
				self.new_mem += len(s1) + len(s2)
		else:
			u.oldText = oldText
			u.newText = newText
		
		self.leading = leading
		self.trailing = trailing
		self.oldMiddleLines = old_middle_lines
		self.newMiddleLines = new_middle_lines
		self.oldNewlines = old_newlines
		self.newNewlines = new_newlines
		#@-body
		#@-node:2::<< save undo text info >>

		u.oldSel = oldSel ; u.newSel = newSel
		# 11/13/02: Remember the scrolling position.
		u.yview = c.frame.body.yview()
		# Push params on undo stack, clearing all forward entries.
		u.bead += 1
		d = u.setBead(u.bead)
		u.beads[u.bead:] = [d]
		# trace(`u.bead` + ":" + `len(u.beads)`)
		u.setUndoTypes() # Recalculate the menu labels.
		return d
	#@-body
	#@-node:7::setUndoTypingParams
	#@+node:8::setUndoTypes
	#@+body
	def setUndoTypes (self):
		
		u = self
		# trace(`u.bead` + ":" + `len(u.beads)`)
	
		# Set the undo type and undo menu label.
		d = u.peekBead(u.bead)
		if d:
			u.setUndoType(d["undoType"])
		else:
			u.setUndoType("Can't Undo")
	
		# Set only the redo menu label.
		d = u.peekBead(u.bead+1)
		if d:
			u.setRedoType(d["undoType"])
		else:
			u.setRedoType("Can't Redo")
	
	
	
	
	#@-body
	#@-node:8::setUndoTypes
	#@-node:4::State routines...
	#@+node:5::redo
	#@+body
	def redo (self):
		
		u = self ; c = u.commands
		if not u.canRedo(): return
		if not u.getBead(u.bead+1): return
		current = c.currentVnode()
		if not current: return
		# trace(`u.bead+1` + ":" + `len(u.beads)` + ":" + `u.peekBead(u.bead+1)`)
		u.redoing = true
		redrawFlag = true
		c.beginUpdate()
		redoType = u.undoType # Use the type of the next bead.
		if 1: # range...
			
			#@<< redo clone cases >>
			#@+node:1::<< redo clone cases >>
			#@+body
			if redoType == "Clone":
			
				if u.back:
					u.v.linkAfter(u.back)
				elif u.parent:
					u.v.linkAsNthChild(u.parent,0)
				else:
					u.v.linkAsRoot()
			
				shared = u.findSharedVnode(u.v)
				if shared: u.v.joinTreeTo(shared)
				u.v.createDependents()
				if u.v.shouldBeClone():
					u.v.setClonedBit()
				c.initAllCloneBits()
				c.selectVnode(u.v)
			#@-body
			#@-node:1::<< redo clone cases >>

			
			#@<< redo insert cases >>
			#@+node:3::<< redo insert cases >>
			#@+body
			elif redoType in ["Import", "Insert Outline", "Paste Node"]:
			
				if u.back:
					u.v.linkAfter(u.back)
				elif u.parent:
					u.v.linkAsNthChild(u.parent,0)
				else:
					u.v.linkAsRoot()
			
				shared = u.findSharedVnode(u.v)
				if shared: u.v.joinTreeTo(shared)
				u.v.createDependents()
				if u.v.shouldBeClone():
					u.v.setClonedBit()
				c.initAllCloneBits()
				c.selectVnode(u.v)
			#@-body
			#@-node:3::<< redo insert cases >>

			
			#@<< redo delete cases >>
			#@+node:2::<< redo delete cases >>
			#@+body
			elif redoType == "Delete Outline" or redoType == "Cut Node":
			
				c.selectVnode(u.v)
				c.deleteHeadline()
			#@-body
			#@-node:2::<< redo delete cases >>

			
			#@<< redo move & drag cases >>
			#@+node:4::<< redo move & drag cases >>
			#@+body
			elif redoType in ["Drag","Move Down","Move Left","Move Right","Move Up"]:
			
				if u.parent:
					u.v.moveToNthChildOf(u.parent,u.n)
				elif u.back:
					u.v.moveAfter(u.back)
				else:
					# 3/16/02: Moving up is the only case that can do this.
					parent = u.v.parent()
					u.v.moveToRoot(c.tree.rootVnode) # 5/27/02
					if parent: # We could assert(parent)
						parent.moveAfter(u.v)
				c.initJoinedCloneBits(u.v) # 7/6/02
				c.selectVnode(u.v)
				
			elif redoType == "Drag":
			
				u.v.moveToNthChildOf(u.parent,u.n)
				c.initJoinedCloneBits(u.v) # 7/6/02
				c.selectVnode(u.v)
			#@-body
			#@-node:4::<< redo move & drag cases >>

			
			#@<< redo promote and demote cases >>
			#@+node:5::<< redo promote and demote cases >>
			#@+body
			elif redoType == "Demote":
			
				c.selectVnode(u.v)
				c.demote()
				
			elif redoType == "Promote":
			
				c.selectVnode(u.v)
				c.promote()
			#@-body
			#@-node:5::<< redo promote and demote cases >>

			
			#@<< redo replace cases >>
			#@+node:6::<< redo replace cases >>
			#@+body
			elif redoType in [
				"Convert All Blanks",
				"Convert All Tabs",
				"Extract",
				"Extract Names",
				"Extract Section"]:
				
				# Same as undo except we interchange u.oldTree and u.v in the call to undoReplace.
				self.undoReplace(u.oldTree,u.v)
				u.v,u.oldTree = u.oldTree,u.v
				
				v = u.oldTree
				# selectVnode causes recoloring, so don't do this unless needed.
				if current != u.v:
					c.selectVnode(v)
				# This rewrites the body pane, so we must do a full recolor.
				v.setBodyStringOrPane(v.bodyString())
				c.tree.recolor(u.v)
				redrawFlag = (current != u.v)
			
			#@-body
			#@-node:6::<< redo replace cases >>

			
			#@<< redo sort cases >>
			#@+node:7::<< redo sort cases >>
			#@+body
			elif redoType == "Sort Children":
			
				c.selectVnode(u.v)
				c.sortChildren()
			
			elif redoType == "Sort Siblings":
			
				c.selectVnode(u.v)
				c.sortSiblings()
			#@-body
			#@-node:7::<< redo sort cases >>

			
			#@<< redo typing cases >>
			#@+node:8::<< redo typing cases >>
			#@+body
			elif redoType in ( "Typing",
				"Change","Convert Blanks","Convert Tabs","Cut",
				"Delete","Indent","Paste","Reformat Paragraph","Undent"):
			
				# trace(`redoType` + ":" + `u.v`)
				# selectVnode causes recoloring, so avoid if possible.
				if current != u.v:
					c.selectVnode(u.v) ## Optimize this away??
				if u.leading == None:
					print "**** Non-incremental redo should never happen! *****"
					u.v.setBodyStringOrPane(u.newText)
					c.tree.recolor(u.v)
				else:
					self.undoRedoText(
						u.v,u.leading,u.trailing,
						u.newMiddleLines,u.oldMiddleLines,
						u.newNewlines,u.oldNewlines,
						tag="redo",
						expectedStart =u.oldText,
						expectedResult=u.newText)
				if u.newSel:
					c.body.mark_set("insert",u.newSel)
				if u.yview:
					first,last=u.yview
					c.body.yview("moveto",first)
				redrawFlag = (current != u.v)
					
			elif redoType == "Change All":
			
				while 1:
					u.bead += 1
					d = u.getBead(u.bead+1)
					assert(d)
					redoType = u.undoType
					# trace(`redoType`)
					if redoType == "Change All":
						c.selectVnode(u.v)
						break
					elif redoType == "Change":
						u.v.t.setTnodeText(u.newText)
						u.v.setDirty()
					elif redoType == "Change Headline":
						u.v.initHeadString(u.newText)
					else: assert(false)
			
			elif redoType == "Change Headline":
				
				# trace(`u.newText`)
				u.v.setHeadStringOrHeadline(u.newText)
				# 9/24/02: update all joined headlines.
				v2 = u.v.joinList
				while v2 and v2 != u.v:
					v2.setHeadString(u.newText)
					v2 = v2.joinList
				c.selectVnode(u.v)
			#@-body
			#@-node:8::<< redo typing cases >>

			else: trace("Unknown case: " + `redoType`)
			c.setChanged(true)
			if u.v: u.v.setDirty()
		c.endUpdate(redrawFlag) # 11/08/02
		u.redoing = false
		u.bead += 1
		u.setUndoTypes()
	#@-body
	#@-node:5::redo
	#@+node:6::undo
	#@+body
	#@+at
	#  This function and its allies undo the operation described by the undo parmaters.

	#@-at
	#@@c

	def undo (self):
	
		u = self ; c = u.commands
		if not u.canUndo(): return
		if not u.getBead(u.bead): return
		current = c.currentVnode()
		if not current: return
		# trace(`u.bead` + ":" + `len(u.beads)` + ":" + `u.peekBead(u.bead)`)
		c.endEditing()# Make sure we capture the headline for a redo.
		u.undoing = true
		c.beginUpdate()
		undoType = u.undoType
		redrawFlag = true
		if 1: # range...
			
			#@<< undo clone cases >>
			#@+node:1::<< undo clone cases >>
			#@+body
			# We can immediately delete the clone because clone() can recreate it using only v.
			
			if undoType == "Clone":
				
				c.selectVnode(u.v)
				c.deleteHeadline()
				c.selectVnode(u.back)
			#@-body
			#@-node:1::<< undo clone cases >>

			
			#@<< undo delete cases >>
			#@+node:2::<< undo delete cases >>
			#@+body
			#@+at
			#  Deleting a clone is _not_ the same as undoing a clone: the 
			# clone may have been moved, so there is no necessary relationship 
			# between the two nodes.

			#@-at
			#@@c

			elif undoType == "Delete Outline" or undoType == "Cut Node":
				
				if u.back:
					u.v.linkAfter(u.back)
				elif u.parent:
					u.v.linkAsNthChild(u.parent,0)
				else:
					u.v.linkAsRoot()
				shared = u.findSharedVnode(u.v)
				if shared: u.v.joinTreeTo(shared)
				u.v.createDependents()
				if u.v.shouldBeClone():
					u.v.setClonedBit()
				c.initAllCloneBits()
				c.selectVnode(u.v)
			#@-body
			#@-node:2::<< undo delete cases >>

			
			#@<< undo insert cases >>
			#@+node:3::<< undo insert cases >>
			#@+body
			elif undoType in ["Import", "Insert Outline", "Paste Node"]:
				
				c.selectVnode(u.v)
				c.deleteHeadline()
				if u.select:
					# trace("Insert/Paste:" + `u.select`)
					c.selectVnode(u.select)
			#@-body
			#@-node:3::<< undo insert cases >>

			
			#@<< undo move & drag cases >>
			#@+node:4::<< undo move  & drag cases >>
			#@+body
			elif undoType in ["Drag", "Move Down","Move Left","Move Right","Move Up"]:
			
				if u.oldParent:
					u.v.moveToNthChildOf(u.oldParent,u.oldN)
				elif u.oldBack:
					u.v.moveAfter(u.oldBack)
				else:
					# 3/16/02: Moving up is the only case that can do this.
					parent = u.v.parent()
					u.v.moveToRoot(c.tree.rootVnode) # 5/27/02
					if parent: # We could assert(parent)
						parent.moveAfter(u.v)
				
				c.initJoinedCloneBits(u.v) # 7/6/02
				c.selectVnode(u.v)
			#@-body
			#@-node:4::<< undo move  & drag cases >>

			
			#@<< undo promote and demote cases >>
			#@+node:5::<< undo promote and demote cases >>
			#@+body
			#@+at
			#  Promote and demote operations are the hard to undo, because 
			# they involve relinking a list of nodes. We pass the work off to 
			# routines dedicated to the task.

			#@-at
			#@@c

			elif undoType == "Demote":
			
				u.undoDemote()
			
			elif undoType == "Promote":
				
				u.undoPromote()
			#@-body
			#@-node:5::<< undo promote and demote cases >>

			
			#@<< undo replace cases >>
			#@+node:6::<< undo replace cases >>
			#@+body
			elif undoType in [
				"Convert All Blanks",
				"Convert All Tabs",
				"Extract",
				"Extract Names",
				"Extract Section"]:
				
				self.undoReplace(u.v,u.oldTree)
				u.v,u.oldTree = u.oldTree,u.v
				
				v = u.v
				# selectVnode causes recoloring, so don't do this unless needed.
				if current != u.v:
					c.selectVnode(v)
				# This rewrites the body pane, so we must do a full recolor.
				v.setBodyStringOrPane(v.bodyString())
				c.tree.recolor(u.v)
				redrawFlag = (current != u.v)
			#@-body
			#@-node:6::<< undo replace cases >>

			
			#@<< undo sort cases >>
			#@+node:7::<< undo sort cases >>
			#@+body
			#@+at
			#  Sort operations are the hard to undo, because they involve 
			# relinking a list of nodes. We pass the work off to routines 
			# dedicated to the task.

			#@-at
			#@@c

			elif undoType == "Sort Children":
				
				u.undoSortChildren()
			
			elif undoType == "Sort Siblings":
				
				u.undoSortSiblings()
			#@-body
			#@-node:7::<< undo sort cases >>

			
			#@<< undo typing cases >>
			#@+node:8::<< undo typing cases >>
			#@+body
			#@+at
			#  When making "large" changes to text, we simply save the old and 
			# new text for undo and redo.  This happens rarely, so the expense 
			# is minor.
			# 
			# But for typical typing situations, where we are typing a single 
			# character, saving both the old and new text wastes a huge amount 
			# of space and puts extreme stress on the garbage collector.  This 
			# in turn can cause big performance problems.

			#@-at
			#@@c
				
			elif undoType in ( "Typing",
				"Change","Convert Blanks","Convert Tabs","Cut",
				"Delete","Indent","Paste","Reformat Paragraph","Undent"):
			
				# trace(`undoType` + ":" + `u.v`)
				# selectVnode causes recoloring, so don't do this unless needed.
				if current != u.v:
					c.selectVnode(u.v) ## Optimize this away??
				if u.leading == None:
					print "**** Non-incremental undo should never happen! *****"
					u.v.setBodyStringOrPane(u.oldText)
					c.tree.recolor(u.v,incremental=false)
				else:
					self.undoRedoText(
						u.v,u.leading,u.trailing,
						u.oldMiddleLines,u.newMiddleLines,
						u.oldNewlines,u.newNewlines,
						expectedStart =u.newText,
						expectedResult=u.oldText)
				if u.oldSel:
					c.body.mark_set("insert",u.oldSel)
				if u.yview:
					first,last=u.yview
					c.body.yview("moveto",first)
				redrawFlag = (current != u.v)
					
			elif undoType == "Change All":
			
				while 1:
					u.bead -= 1
					d = u.getBead(u.bead)
					assert(d)
					undoType = u.undoType
					# trace(`undoType`)
					if undoType == "Change All":
						c.selectVnode(u.v)
						break
					elif undoType == "Change":
						u.v.t.setTnodeText(u.oldText)
						u.v.setDirty()
					elif undoType == "Change Headline":
						u.v.initHeadString(u.oldText)
					else: assert(false)
					
			elif undoType == "Change Headline":
				
				# trace(`u.oldText`)
				u.v.setHeadStringOrHeadline(u.oldText)
				# 9/24/02: update all joined headlines.
				v2 = u.v.joinList
				while v2 and v2 != u.v:
					v2.setHeadString(u.oldText)
					v2 = v2.joinList
				c.selectVnode(u.v)
			#@-body
			#@-node:8::<< undo typing cases >>

			else: trace("Unknown case: " + `u.undoType`)
			c.setChanged(true)
			if u.v: u.v.setDirty()
		c.endUpdate(redrawFlag) # 11/9/02
		u.undoing = false
		u.bead -= 1
		u.setUndoTypes()
	#@-body
	#@-node:6::undo
	#@+node:7::Undo helpers
	#@+node:1::findSharedVnode
	#@+body
	def findSharedVnode (self,target):
	
		c = self.commands ; v = c.rootVnode()
		while v:
			if v != target and v.t == target.t:
				return v
			v = v.threadNext()
		return None
	#@-body
	#@-node:1::findSharedVnode
	#@+node:2::undoDemote
	#@+body
	# undoes the previous demote operation.
	def undoDemote (self):
	
		u = self ; c = u.commands
		ins = u.v
		last = u.lastChild
		child = u.v.firstChild()
		assert(child and last)
		c.beginUpdate()
		while 1:
			save_next = child.next()
			child.moveAfter(ins)
			ins = child
			u.lastChild = child
			child = save_next
			assert(ins == last or child)
			if ins == last: break
		c.selectVnode(u.v)
		c.endUpdate()
	#@-body
	#@-node:2::undoDemote
	#@+node:3::undoPromote
	#@+body
	# Undoes the previous promote operation.
	def undoPromote (self):
	
		u = self ; c = u.commands
		v = v1 = u.v
		assert(v1)
		last = u.lastChild
		next = v.next()
		assert(next and last)
		c.beginUpdate()
		while 1:
			v = next
			assert(v)
			next = v.next()
			n = v1.numberOfChildren()
			v.moveToNthChildOf(v1,n)
			u.lastChild = v
			if v == last: break
		c.selectVnode(v1)
		c.endUpdate()
	#@-body
	#@-node:3::undoPromote
	#@+node:4::undoReplace
	#@+body
	#@+at
	#  This routine implements undo by properly replacing v's tree by the oldv 
	# tree.  For redo, just call this routine with these two variables interchanged.
	# 
	# This routine shows how to implement undo for any kind of operation, no 
	# matter how complex.  Just do:
	# 
	# 	v_copy = c.copyTree(v)
	# 	< < make arbitrary changes to v's tree > >
	# 	c.undoer.setUndoParams("Op Name",v,select=current,oldTree=v_copy)
	# 
	# This way is far more elegant than calling v.destroyDependents and 
	# v.createDependents.  This is the way it is written in "The Book." Yes, 
	# entire trees are copied, but in the most general case that is necessary.

	#@-at
	#@@c

	def undoReplace (self,v,oldv):
	
		assert(v)
		assert(oldv)
		u = self ; c = u.commands
		j = v.joinList
		copies = []
	
		# For each node joined to v, swap in a copy of oldv.
		while j and j != v:
			nextj = j.joinList
			copy = c.copyTree(oldv)
			copies.append(copy)
			j.swap_links(copy,j)
			j = nextj
	
		# Swap v and oldv.
		v.swap_links(oldv,v)
		v = oldv
		
		# Join v to all copies.
		for copy in copies:
			v.joinTreeTo(copy)
			
		# Restore all clone bits.
		if v.shouldBeClone():
			v.setClonedBit()
		c.initAllCloneBits()
	#@-body
	#@-node:4::undoReplace
	#@+node:5::undoRedoText
	#@+body
	# Handle text undo and redo.
	# The terminology is for undo: converts _new_ text into _old_ text.
	
	def undoRedoText (self, v,
		leading,trailing, # Number of matching leading & trailing lines.
		oldMidLines,newMidLines, # Lists of unmatched lines.
		oldNewlines,newNewlines, # Number of trailing newlines.
		tag="undo", # "undo" or "redo".
		expectedStart=None,expectedResult=None):
			# For debugging. The expected starting & result text.
		
		c = self.commands
		assert(v == c.currentVnode())
	
		if self.new_undo:
			
			#@<< Incrementally update the Tk.Text widget >>
			#@+node:1::<< Incrementally update the Tk.Text widget >>
			#@+body
			# Only update the changed lines.
			mid_text = string.join(oldMidLines,'\n')
			old_mid_len = len(oldMidLines)
			new_mid_len = len(newMidLines)
			# Maybe this could be simplified, and it is good to treat the "end" with care.
			if trailing == 0:
				c.frame.body.delete(str(1+leading)+".0","end")
				if leading > 0:
					c.frame.body.insert("end",'\n')
				c.frame.body.insert("end",mid_text)
			else:
				if new_mid_len > 0:
					c.frame.body.delete(str(1+leading)+".0",
						str(leading+new_mid_len)+".0 lineend")
				elif leading > 0:
					c.frame.body.insert(str(1+leading)+".0",'\n')
				c.frame.body.insert(str(1+leading)+".0",mid_text)
			# Try to end the Tk.Text widget with oldNewlines newlines.
			# This may be off by one, and we don't care because
			# we never use body text to compute undo results!
			s = c.frame.body.get("1.0","end")
			newlines = 0 ; i = len(s) - 1
			while i >= 0 and s[i] == '\n':
				newlines += 1 ; i -= 1
			while newlines > oldNewlines:
				c.frame.body.delete("end-1c")
				newlines -= 1
			if oldNewlines > newlines:
				c.frame.body.insert("end",'\n'*(oldNewlines-newlines))
			#@-body
			#@-node:1::<< Incrementally update the Tk.Text widget >>

			
			#@<< Compute the result using v's body text >>
			#@+node:2::<< Compute the result using v's body text >>
			#@+body
			# Recreate the text using the present body text.
			body = v.bodyString()
			body_lines = body.split('\n')
			s = []
			if leading > 0:
				s.extend(body_lines[:leading])
			if len(oldMidLines) > 0:
				s.extend(oldMidLines)
			if trailing > 0:
				s.extend(body_lines[-trailing:])
			s = string.join(s,'\n')
			# Remove trailing newlines in s.
			while len(s) > 0 and s[-1] == '\n':
				s = s[:-1]
			# Add oldNewlines newlines.
			if oldNewlines > 0:
				s = s + '\n' * oldNewlines
			result = s
			
			if self.debug_print:
				print "body:  ",`body`
				print "result:",`result`
			#@-body
			#@-node:2::<< Compute the result using v's body text >>

			
			#@<< Compare the result with the expected result >>
			#@+node:3::<< Compare the result with the expected result >>
			#@+body
			if self.debug and expectedResult != result:
			
				print "----- result computed using Tk.Text != expectedResult in", tag
				print "expected:",`expectedResult`
				print "actual  :",`s`
			
				#print "newMidLines",new_mid_len,`newMidLines`
				#print "oldMidLines",old_mid_len,`oldMidLines`
				#print "midText",`mid_text`
			#@-body
			#@-node:3::<< Compare the result with the expected result >>

			v.t.setTnodeText(result)
			if 1: # A bit of protection in case the trailing newline doesn't match.
				c.tree.recolor_range(v,leading,trailing)
			else:
				c.tree.recolor(v,incremental=true)
	
		else: # Rewrite the body pane and do a full recolor.
			v.setBodyStringOrPane(expectedResult)
	#@-body
	#@-node:5::undoRedoText
	#@+node:6::undoSortChildren
	#@+body
	def undoSortChildren (self):
	
		u = self ; c = u.commands ; v = u.v
		assert(v)
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			index = 0
			for child in u.sort:
				child.moveToNthChildOf(v,index)
				index += 1
			v.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@-body
	#@-node:6::undoSortChildren
	#@+node:7::undoSortSiblings
	#@+body
	def undoSortSiblings (self):
		
		u = self ; c = u.commands ; v = u.v
		parent = v.parent()
		assert(v and parent)
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			index = 0
			for sib in u.sort:
				sib.moveToNthChildOf(parent,index)
				index += 1
			parent.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@-body
	#@-node:7::undoSortSiblings
	#@-node:7::Undo helpers
	#@-others
#@-body
#@-node:0::@file leoUndo.py
#@-leo
