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


optionalIvars = [
	"parent","back","n","lastChild","sort","select",
	"oldTree", # 7/5/02: a copy of the old tree.
	"oldParent","oldBack","oldN",
	"oldText","newText","oldSel","newSel"]

from leoGlobals import *

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
	#@-node:2::undo.__init__
	#@+node:3::State routines...
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
	# undone and redone..  We do nothing when called from the undo/redo logic 
	# because the Undo and Redo commands merely reset the bead pointer.
	# 
	# This is called with the following undo Types: "Typing", "Cut", "Paste", 
	# "Delete", "Change"

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
	#@-node:3::State routines...
	#@+node:4::redo
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
			elif type in ["Import", "Insert Outline", "Paste Node"]:
			
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
			elif type in ["Drag","Move Down","Move Left","Move Right","Move Up"]:
			
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
				
			elif type == "Drag":
			
				u.v.moveToNthChildOf(u.parent,u.n)
				c.initJoinedCloneBits(u.v) # 7/6/02
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

			
			#@<< redo replace cases >>
			#@+node:6::<< redo replace cases >>
			#@+body
			elif type in [
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
			elif type == "Sort Children":
			
				c.selectVnode(u.v)
				c.sortChildren()
			
			elif type == "Sort Siblings":
			
				c.selectVnode(u.v)
				c.sortSiblings()
			#@-body
			#@-node:7::<< redo sort cases >>

			
			#@<< redo typing cases >>
			#@+node:8::<< redo typing cases >>
			#@+body
			# DTHEIN 27-OCT-2002: added reformat paragraph
			elif type in [ "Typing",
				"Change",
				"Convert Blanks", "Convert Tabs",
				"Reformat Paragraph",
				"Cut", "Paste", "Delete",
				"Indent", "Undent" ]:
			
				# trace(`type` + ":" + `u.v`)
				# selectVnode causes recoloring, so don't do this unless needed.
				if current != u.v:
					c.selectVnode(u.v)
				# This rewrites the body pane, so we must do a full recolor.
				u.v.setBodyStringOrPane(u.newText)
				c.tree.recolor(u.v)
				if u.newSel:
					c.body.mark_set("insert",u.newSel)
					c.body.see(u.oldSel)
				redrawFlag = (current != u.v)
					
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
				# 9/24/02: update all joined headlines.
				v2 = u.v.joinList
				while v2 and v2 != u.v:
					v2.setHeadString(u.newText)
					v2 = v2.joinList
				c.selectVnode(u.v)
			#@-body
			#@-node:8::<< redo typing cases >>

			else: trace("Unknown case: " + `type`)
			c.setChanged(true)
			if u.v: u.v.setDirty()
		c.endUpdate(redrawFlag) # 11/08/02
		u.redoing = false
		u.bead += 1
		u.setUndoTypes()
	#@-body
	#@-node:4::redo
	#@+node:5::undo
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
		redrawFlag = true
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
			#  Deleting a clone is _not_ the same as undoing a clone: the 
			# clone may have been moved, so there is no necessary relationship 
			# between the two nodes.

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

			
			#@<< undo insert cases >>
			#@+node:3::<< undo insert cases >>
			#@+body
			elif type in ["Import", "Insert Outline", "Paste Node"]:
				
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
			elif type in ["Drag", "Move Down","Move Left","Move Right","Move Up"]:
			
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

			elif type == "Demote":
			
				u.undoDemote()
			
			elif type == "Promote":
				
				u.undoPromote()
			#@-body
			#@-node:5::<< undo promote and demote cases >>

			
			#@<< undo replace cases >>
			#@+node:6::<< undo replace cases >>
			#@+body
			elif type in [
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

			elif type == "Sort Children":
				
				u.undoSortChildren()
			
			elif type == "Sort Siblings":
				
				u.undoSortSiblings()
			#@-body
			#@-node:7::<< undo sort cases >>

			
			#@<< undo typing cases >>
			#@+node:8::<< undo typing cases >>
			#@+body
			# DTHEIN 27-OCT-2002: added reformat paragraph
			elif type in [ "Typing",
				"Change",
				"Convert Blanks", "Convert Tabs",
				"Reformat Paragraph",
				"Cut", "Paste", "Delete",
				"Indent", "Undent" ]:
			
				# trace(`type` + ":" + `u.v`)
				# selectVnode causes recoloring, so don't do this unless needed.
				if current != u.v:
					c.selectVnode(u.v)
				# This rewrites the body pane, so we must do a full recolor.
				u.v.setBodyStringOrPane(u.oldText)
				c.tree.recolor(u.v)
				if u.oldSel:
					c.body.mark_set("insert",u.oldSel)
					c.body.see(u.oldSel)
				redrawFlag = (current != u.v)
					
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
	#@-node:5::undo
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
	#@+node:5::undoSortChildren
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
	#@-node:5::undoSortChildren
	#@+node:6::undoSortSiblings
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
	#@-node:6::undoSortSiblings
	#@-node:6::Undo helpers
	#@-others
#@-body
#@-node:0::@file leoUndo.py
#@-leo
