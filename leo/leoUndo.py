#@+leo

#@+node:0::@file leoUndo.py
#@+body
# Undo manager for leo.py.


#@<< How Leo implements unlimited undo >>
#@+node:1::<< How Leo implements unlimited undo >>
#@+body
#@+at
#  Unlimited undo is straightforward, and it requires that all commands that affect the outline or body text must be undoable.
# 
# We can think of all the actions that may be Undone or Redone as a string of beads (undo nodes).  Undoing an operation moves 
# backwards to the next bead; redoing an operation moves forwards to the next bead.  A "bead pointer" points to the present bead.  
# The bead pointer may point in front of the first bead (Undo is disabled) or at the last bead (Redo is disabled). An undo node is 
# just a dictionary containing all information needed to undo or redo the operation.
# 
# The Undo command uses the present bead to undo the action, then moves the bead pointer backwards.  The Redo command uses the 
# bead after the present bead to redo the action, then moves the bead pointer forwards.  All undoable operations call 
# setUndoParams() to create a new bead.  The list of beads does not branch: all undoable operations (except the Undo and Redo 
# commands themselves) delete any beads following the newly created bead.
# 
# The undoType ivar is a string indicating the operation that may be currently undone, or "Can't Redo" if the Undo command is 
# presently disabled.  The undoType ivar contains just the operation name, not the "Undo" prefix found in the actual menu titles.  
# There is no independent redoType ivar: it is computed from the undoType ivar of the next bead on the string.

#@-at
#@@c
#@-body
#@-node:1::<< How Leo implements unlimited undo >>


optionalIvars = [
	"parent","back","n","lastChild","sort","select",
	"oldParent","oldBack","oldN",
	"oldText","newText","oldSel","newSel"]

from leoGlobals import *
from leoUtils import *

class undoer:

	#@+others
	#@+node:2::undo.__init__
	#@+body
	def __init__ (self,commands):
		
		self.commands = commands
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
	#  This method clears then entire Undo state.  All non-undoable commands should call this method.

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
	#@-node:2::undo.__init__
	#@+node:3:C=1:State routines...
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
	
		u = self ; c = u.commands ; menu = c.frame.editMenu
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
		if 1: # Recreate an "oldText" entry if necessary.
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
		if 1:
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
	
		u = self ; c = u.commands ; menu = c.frame.editMenu
		name = u.redoMenuName(type)
		if name != u.redoMenuLabel:
			# Update menu using old name.
			setMenuLabel(menu,u.redoMenuLabel,name)
			u.redoMenuLabel = name
	
	def setUndoType (self,type):
	
		u = self ; c = u.commands ; menu = c.frame.editMenu
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
	#  This routine saves enough information so an operation can be undone and redone.  We do nothing when called from the 
	# undo/redo logic because the Undo and Redo commands merely reset the bead pointer.

	#@-at
	#@@c
	
	def setUndoParams (self,undo_type,v,**keywords):
	
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
	#  This routine saves enough information so a typing operation can be undone and redone..  We do nothing when called from the 
	# undo/redo logic because the Undo and Redo commands merely reset the bead pointer.
	# 
	# This is called with the following undo Types: "Typing", "Cut", "Paste", "Delete", "Change"

	#@-at
	#@@c
	
	def setUndoTypingParams (self,v,undo_type,oldText,newText,oldSel,newSel):
	
		u = self
		if u.redoing or u.undoing: return None
		if undo_type == "Can't Undo":
			u.clearUndoState()
			return None
		# Clear all optional params.
		for ivar in optionalIvars:
			exec('u.%s = None' % ivar)
		# Set the params.
		u.undoType = undo_type
		u.v = v
		u.oldText = oldText ; u.newText = newText
		u.oldSel = oldSel ; u.newSel = newSel
		# Push params on undo stack, clearing all forward entries.
		u.bead += 1
		d = u.setBead(u.bead)
		u.beads[u.bead:] = [d]
		# trace(`u.bead` + ":" + `len(u.beads)`)
		# Recalculate the menu labels.
		u.setUndoTypes()
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
	#@-node:3:C=1:State routines...
	#@+node:4:C=2:redo
	#@+body
	def redo (self):
		
		u = self ; c = u.commands
		if not u.canRedo(): return
		if not u.getBead(u.bead+1): return
		current = c.currentVnode()
		if not current: return
		# trace(`u.bead+1` + ":" + `len(u.beads)` + ":" + `u.peekBead(u.bead+1)`)
		u.redoing = true
		c.beginUpdate()
		type = u.undoType # Use the type of the next bead.
		if 1: # range...
			
			#@<< redo clone cases >>
			#@+node:1::<< redo clone cases >>
			#@+body
			if type == "Clone":
			
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
			elif type == "Insert Outline" or type == "Paste Node":
			
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
			elif type == "Delete Outline" or type == "Cut Node":
			
				c.selectVnode(u.v)
				c.deleteHeadline()
			#@-body
			#@-node:2::<< redo delete cases >>

			
			#@<< redo move & drag cases >>
			#@+node:4::<< redo move & drag cases >>
			#@+body
			elif type in ["Move Down","Move Left","Move Right","Move Up"]:
			
				if u.parent:
					u.v.moveToNthChildOf(u.parent,u.n)
				elif u.back:
					u.v.moveAfter(u.back)
				else:
					u.v.moveToRoot()
				c.selectVnode(u.v)
				
			elif type == "Drag":
			
				u.v.moveToNthChildOf(u.parent,u.n)
				c.selectVnode(u.v)
			#@-body
			#@-node:4::<< redo move & drag cases >>

			
			#@<< redo promote and demote cases >>
			#@+node:5::<< redo promote and demote cases >>
			#@+body
			elif type == "Demote":
			
				c.selectVnode(u.v)
				c.demote()
				
			elif type == "Promote":
			
				c.selectVnode(u.v)
				c.promote()
			#@-body
			#@-node:5::<< redo promote and demote cases >>

			
			#@<< redo sort cases >>
			#@+node:6::<< redo sort cases >>
			#@+body
			elif type == "Sort Children":
			
				c.selectVnode(u.v)
				c.sortChildren()
			
			elif type == "Sort Siblings":
			
				c.selectVnode(u.v)
				c.sortSiblings()
			#@-body
			#@-node:6::<< redo sort cases >>

			
			#@<< redo typing cases >>
			#@+node:7::<< redo typing cases >>
			#@+body
			elif type in [
				"Typing","Change","Cut","Paste","Delete",
				"Convert Blanks","Indent","Undent"]:
			
				# trace(`type` + ":" + `u.v`)
				c.selectVnode(u.v)
				u.v.setBodyStringOrPane(u.newText)
				c.tree.recolor(u.v)
				if u.newSel:
					c.body.mark_set("insert",u.newSel)
					c.body.see(u.oldSel)
					
			elif type == "Change All":
			
				while 1:
					u.bead += 1
					d = u.getBead(u.bead+1)
					assert(d)
					type = u.undoType
					# trace(`type`)
					if type == "Change All":
						c.selectVnode(u.v)
						break
					elif type == "Change":
						u.v.t.setTnodeText(u.newText)
						u.v.setDirty()
					elif type == "Change Headline":
						u.v.initHeadString(u.newText)
					else: assert(false)
			
			elif type == "Change Headline":
				
				# trace(`u.newText`)
				u.v.setHeadStringOrHeadline(u.newText)
				c.selectVnode(u.v)
			#@-body
			#@-node:7::<< redo typing cases >>

			else: trace("Unknown case: " + `type`)
			c.setChanged(true)
			if u.v: u.v.setDirty()
		c.endUpdate()
		u.redoing = false
		u.bead += 1
		u.setUndoTypes()
	#@-body
	#@-node:4:C=2:redo
	#@+node:5:C=3:undo
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
		type = u.undoType
		if 1: # range...
			
			#@<< undo clone cases >>
			#@+node:1::<< undo clone cases >>
			#@+body
			# We can immediately delete the clone because clone() can recreate it using only v.
			
			if type == "Clone":
				
				c.selectVnode(u.v)
				c.deleteHeadline()
				c.selectVnode(u.back)
			#@-body
			#@-node:1::<< undo clone cases >>

			
			#@<< undo delete cases >>
			#@+node:2::<< undo delete cases >>
			#@+body
			#@+at
			#  Deleting a clone is _not_ the same as undoing a clone: the clone may have been moved, so there is no necessary 
			# relationship between the two nodes.

			#@-at
			#@@c
			
			elif type == "Delete Outline" or type == "Cut Node":
				
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

			
			#@<< undo drag cases >>
			#@+node:3::<< undo drag cases >>
			#@+body
			elif type == "Drag":
				
				u.v.moveToNthChildOf(u.parent,u.n)
				c.selectVnode(u.v)
			#@-body
			#@-node:3::<< undo drag cases >>

			
			#@<< undo insert cases >>
			#@+node:4::<< undo insert cases >>
			#@+body
			elif type == "Insert Outline" or type == "Paste Node":
				
				c.selectVnode(u.v)
				c.deleteHeadline()
				if u.select:
					trace("Insert/Paste:" + `u.select`)
					c.selectVnode(u.select)
			#@-body
			#@-node:4::<< undo insert cases >>

			
			#@<< undo move cases >>
			#@+node:5::<< undo move cases >>
			#@+body
			elif type in ["Move Down","Move Left","Move Right","Move Up"]:
			
				if u.oldParent:
					u.v.moveToNthChildOf(u.oldParent,u.oldN)
				elif u.oldBack:
					u.v.moveAfter(u.oldBack)
				else:
					u.v.moveToRoot()
				c.selectVnode(u.v)
			#@-body
			#@-node:5::<< undo move cases >>

			
			#@<< undo promote and demote cases >>
			#@+node:6::<< undo promote and demote cases >>
			#@+body
			#@+at
			#  Promote and demote operations are the hard to undo, because they involve relinking a list of nodes. We pass the 
			# work off to routines dedicated to the task.

			#@-at
			#@@c
			
			elif type == "Demote":
			
				u.undoDemote()
			
			elif type == "Promote":
				
				u.undoPromote()
			#@-body
			#@-node:6::<< undo promote and demote cases >>

			
			#@<< undo sort cases >>
			#@+node:7::<< undo sort cases >>
			#@+body
			#@+at
			#  Sort operations are the hard to undo, because they involve relinking a list of nodes. We pass the work off to 
			# routines dedicated to the task.

			#@-at
			#@@c
			
			elif type == "Sort Children":
				
				u.undoSortChildren()
			
			elif type == "Sort Siblings":
				
				u.undoSortSiblings()
			#@-body
			#@-node:7::<< undo sort cases >>

			
			#@<< undo typing cases >>
			#@+node:8::<< undo typing cases >>
			#@+body
			elif type in [
				"Typing","Change","Cut","Paste","Delete",
				"Convert Blanks","Indent","Undent"]:
			
				# trace(`type` + ":" + `u.v`)
				c.selectVnode(u.v)
				u.v.setBodyStringOrPane(u.oldText)
				c.tree.recolor(u.v)
				if u.oldSel:
					c.body.mark_set("insert",u.oldSel)
					c.body.see(u.oldSel)
					
			elif type == "Change All":
			
				while 1:
					u.bead -= 1
					d = u.getBead(u.bead)
					assert(d)
					type = u.undoType
					# trace(`type`)
					if type == "Change All":
						c.selectVnode(u.v)
						break
					elif type == "Change":
						u.v.t.setTnodeText(u.oldText)
						u.v.setDirty()
					elif type == "Change Headline":
						u.v.initHeadString(u.oldText)
					else: assert(false)
					
			elif type == "Change Headline":
				
				# trace(`u.oldText`)
				u.v.setHeadStringOrHeadline(u.oldText)
				c.selectVnode(u.v)
			#@-body
			#@-node:8::<< undo typing cases >>

			else: trace("Unknown case: " + `u.undoType`)
			c.setChanged(true)
			if u.v: u.v.setDirty()
		c.endUpdate()
		u.undoing = false
		u.bead -= 1
		u.setUndoTypes()
	#@-body
	#@-node:5:C=3:undo
	#@+node:6::Undo helpers
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
	#@+node:2:C=4:undoDemote
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
	#@-node:2:C=4:undoDemote
	#@+node:3:C=5:undoPromote
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
	#@-node:3:C=5:undoPromote
	#@+node:4::undoSortChildren
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
	#@-node:4::undoSortChildren
	#@+node:5::undoSortSiblings
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
	#@-node:5::undoSortSiblings
	#@-node:6::Undo helpers
	#@-others

#@-body
#@-node:0::@file leoUndo.py
#@-leo
