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


#@<< Define optional ivars >>
#@+node:2::<< Define optional ivars >>
#@+body
optionalIvars = (
	"lastChild",
	"parent","oldParent",
	"back","oldBack",
	"n","oldN","oldV",
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
#@-node:2::<< Define optional ivars >>

from leoGlobals import *
import types

class baseUndoer:
	"""The base class of the undoer class."""

	#@+others
	#@+node:3::undo.__init__ & clearIvars
	#@+body
	def __init__ (self,commands):
		
		u = self ; u.commands = commands
		
		# Ivars to transition to new undo scheme...
		
		u.debug = false # true: enable debugging code in new undo scheme.
		u.debug_print = false # true: enable print statements in debug code.
		u.new_undo = true # true: enable new debug code.
		
		# Statistics comparing old and new ways (only if u.debug is on).
		u.new_mem = 0
		u.old_mem = 0
		
		# State ivars...
		u.undoType = "Can't Undo"
		# Bug fix: 12/16/02: These must be set here, _not_ in clearUndoState.
		u.redoMenuLabel = "Can't Redo"
		u.undoMenuLabel = "Can't Undo"
		u.realRedoMenuLabel = "Can't Redo"
		u.realUndoMenuLabel = "Can't Undo"
		u.undoing = false # True if executing an Undo command.
		u.redoing = false # True if executing a Redo command.
	
		u.clearUndoState()
	#@-body
	#@+node:1::clearIvars
	#@+body
	def clearIvars (self):
		
		self.v = None # The node being operated upon for undo and redo.
		for ivar in optionalIvars:
			exec('self.%s = None' % ivar)
	#@-body
	#@-node:1::clearIvars
	#@-node:3::undo.__init__ & clearIvars
	#@+node:4::State routines...
	#@+node:1::clearUndoState
	#@+body
	#@+at
	#  This method clears then entire Undo state.  All non-undoable commands 
	# should call this method.

	#@-at
	#@@c

	def clearUndoState (self):
		
		u = self
		
		if 0: # Bug fix: 12/16/02: setUndo/Redo type needs the old values.
			u.redoMenuLabel = "Can't Redo" 
			u.undoMenuLabel = "Can't Undo"
		
		if 0: # Wrong: set realLabel only when calling setMenuLabel.
			realLabel = app().getRealMenuName("Can't Redo")
			u.realRedoMenuLabel = realLabel.replace("&","")
			realLabel = app().getRealMenuName("Can't Undo")
			u.realUndoMenuLabel = realLabel.replace("&","")
			
		u.setRedoType("Can't Redo")
		u.setUndoType("Can't Undo")
		u.beads = [] # List of undo nodes.
		u.bead = -1 # Index of the present bead: -1:len(beads)
		u.clearIvars()
	#@-body
	#@-node:1::clearUndoState
	#@+node:2::canRedo & canUndo
	#@+body
	# Translation does not affect these routines.
	
	def canRedo (self):
	
		u = self
		return u.redoMenuLabel != "Can't Redo"
	
	def canUndo (self):
	
		u = self
		return u.undoMenuLabel != "Can't Undo"
	
	#@-body
	#@-node:2::canRedo & canUndo
	#@+node:3::enableMenuItems
	#@+body
	def enableMenuItems (self):
	
		u = self ; c = u.commands
		menu = c.frame.getMenu("Edit")
	
		enableMenu(menu,u.redoMenuLabel,u.canRedo())
		enableMenu(menu,u.undoMenuLabel,u.canUndo())
	
	#@-body
	#@-node:3::enableMenuItems
	#@+node:4::getBead, peekBead, setBead
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
	#@-node:4::getBead, peekBead, setBead
	#@+node:5::redoMenuName, undoMenuName
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
	#@-node:5::redoMenuName, undoMenuName
	#@+node:6::setRedoType, setUndoType
	#@+body
	# These routines update both the ivar and the menu label.
	def setRedoType (self,type):
		u = self ; c = u.commands
		menu = c.frame.getMenu("Edit")
		name = u.redoMenuName(type)
		if name != u.redoMenuLabel:
			# Update menu using old name.
			realLabel = app().getRealMenuName(name)
			if realLabel == name:
				underline=choose(match(name,0,"Can't"),-1,0)
			else:
				underline = realLabel.find("&")
			realLabel = realLabel.replace("&","")
			setMenuLabel(menu,u.realRedoMenuLabel,realLabel,underline=underline)
			u.redoMenuLabel = name
			u.realRedoMenuLabel = realLabel
	
	def setUndoType (self,type):
		u = self ; c = u.commands
		menu = c.frame.getMenu("Edit")
		name = u.undoMenuName(type)
		if name != u.undoMenuLabel:
			# Update menu using old name.
			realLabel = app().getRealMenuName(name)
			if realLabel == name:
				underline=choose(match(name,0,"Can't"),-1,0)
			else:
				underline = realLabel.find("&")
			realLabel = realLabel.replace("&","")
			setMenuLabel(menu,u.realUndoMenuLabel,realLabel,underline=underline)
			u.undoType = type
			u.undoMenuLabel = name
			u.realUndoMenuLabel = realLabel
	#@-body
	#@-node:6::setRedoType, setUndoType
	#@+node:7::setUndoParams
	#@+body
	#@+at
	#  This routine saves enough information so an operation can be undone and 
	# redone.  We do nothing when called from the undo/redo logic because the 
	# Undo and Redo commands merely reset the bead pointer.

	#@-at
	#@@c

	def setUndoParams (self,undo_type,v,**keywords):
	
		u = self
		if u.redoing or u.undoing: return None
		if undo_type == None:
			return None
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
	#@-node:7::setUndoParams
	#@+node:8::setUndoTypingParams
	#@+body
	#@+at
	#  This routine saves enough information so a typing operation can be 
	# undone and redone.
	# 
	# We do nothing when called from the undo/redo logic because the Undo and 
	# Redo commands merely reset the bead pointer.

	#@-at
	#@@c

	def setUndoTypingParams (self,v,undo_type,oldText,newText,oldSel,newSel,oldYview=None):
	
		u = self ; c = u.commands
		if u.redoing or u.undoing: return None
		if undo_type == None:
			return None
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
		
		if u.debug_print:
			trace()
			print "lead,trail",leading,trailing
			print "old mid,nls:",len(old_middle_lines),old_newlines,oldText
			print "new mid,nls:",len(new_middle_lines),new_newlines,newText
			#print "lead,trail:",leading,trailing
			#print "old mid:",old_middle_lines
			#print "new mid:",new_middle_lines
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

		if u.new_undo:
			if u.debug:
				# Remember the complete text for comparisons...
				u.oldText = oldText
				u.newText = newText
				# Compute statistics comparing old and new ways...
				# The old doesn't often store the old text, so don't count it here.
				u.old_mem += len(newText)
				s1 = string.join(old_middle_lines,'\n')
				s2 = string.join(new_middle_lines,'\n')
				u.new_mem += len(s1) + len(s2)
			else:
				u.oldText = None
				u.newText = None
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
		if oldYview:
			u.yview = oldYview
		else:
			u.yview = c.frame.body.yview()
		# Push params on undo stack, clearing all forward entries.
		u.bead += 1
		d = u.setBead(u.bead)
		u.beads[u.bead:] = [d]
		# trace(`u.bead` + ":" + `len(u.beads)`)
		u.setUndoTypes() # Recalculate the menu labels.
		return d
	
	#@-body
	#@-node:8::setUndoTypingParams
	#@+node:9::setUndoTypes
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
	#@-node:9::setUndoTypes
	#@-node:4::State routines...
	#@+node:5::u.redo
	#@+body
	def redo (self):
		
		# clear_stats() ; stat()
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
			if redoType in ("Clone","Drag & Clone"):
			
				if u.back:
					u.v.linkAfter(u.back)
				elif u.parent:
					u.v.linkAsNthChild(u.parent,0)
				else:
					u.v.linkAsRoot()
			
				shared = u.findSharedVnode(u.v)
				if shared: u.v.joinTreeTo(shared)
				u.v.createDependents()
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
			elif redoType in (
				"Convert All Blanks","Convert All Tabs",
				"Extract","Extract Names","Extract Section"):
				
				# Same as undo except we interchange u.oldTree and u.v in the call to undoReplace.
				u.v = self.undoReplace(u.v,u.oldTree)
				# u.v.setBodyStringOrPane(u.v.bodyString())
				c.selectVnode(u.v) # Does full recolor.
				redrawFlag = redoType in ("Extract","Extract Names","Extract Section")
			
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
				
			elif redoType == "Sort Top Level":
				
				c.selectVnode(u.v)
				c.sortTopLevel()
				u.v = None # don't mark u.v dirty
			
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
				self.undoRedoText(
					u.v,u.leading,u.trailing,
					u.newMiddleLines,u.oldMiddleLines,
					u.newNewlines,u.oldNewlines,
					tag="redo")
				
				if u.newSel:
					start,end=u.newSel
					setTextSelection (c.frame.body,start,end)
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
				# Update all joined headlines.
				for v2 in u.v.t.joinList:
					if v2 != u.v:
						v2.setHeadString(u.newText)
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
		# print_stats()
	#@-body
	#@-node:5::u.redo
	#@+node:6::u.undo
	#@+body
	#@+at
	#  This function and its allies undo the operation described by the undo parmaters.

	#@-at
	#@@c

	def undo (self):
		
		# clear_stats() ; # stat()
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
				
			elif undoType == "Drag & Clone":
				
				c.selectVnode(u.v)
				c.deleteHeadline()
				c.selectVnode(u.oldV)
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
			elif undoType in (
				"Convert All Blanks","Convert All Tabs",
				"Extract","Extract Names","Extract Section"):
				
				# Major bug: this restores the copy, so further undos don't work properly.
				u.v = self.undoReplace(u.oldTree,u.v)
				#trace(`current`)
				#trace(`u.v`)
				# u.v.setBodyStringOrPane(u.v.bodyString())
				c.selectVnode(u.v) # Does full recolor.
				redrawFlag = true
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
				
			elif undoType == "Sort Top Level":
				
				u.undoSortTopLevel()
				u.v = None # don't mark u.v dirty
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
				self.undoRedoText(
					u.v,u.leading,u.trailing,
					u.oldMiddleLines,u.newMiddleLines,
					u.oldNewlines,u.newNewlines,
					tag="undo")
				if u.oldSel:
					start,end=u.oldSel
					setTextSelection (c.frame.body,start,end)
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
				for v2 in u.v.t.joinList:
					if v2 != u.v:
						v2.setHeadString(u.oldText)
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
		# print_stats()
	#@-body
	#@-node:6::u.undo
	#@+node:7::Undo helpers
	#@+node:1::findSharedVnode
	#@+body
	def findSharedVnode (self,target):
	
		u = self ; c = u.commands ; v = c.rootVnode()
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
		ins = v = u.v
		last = u.lastChild
		child = v.firstChild()
		assert(child)
		c.beginUpdate()
		# 3/19/03: do not undemote children up to last.
		if last:
			while child and child != last:
				child = child.next()
			if child:
				child = child.next()
		while child:
			next = child.next()
			child.moveAfter(ins)
			ins = child
			child = next
		c.selectVnode(v)
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
		assert(next)
		c.beginUpdate()
		while next:
			v = next
			next = v.next()
			n = v1.numberOfChildren()
			v.moveToNthChildOf(v1,n)
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
	# This way is more elegant than calling v.destroyDependents and v.createDependents.
	# Yes, entire trees are copied, but in the most general case that is necessary.

	#@-at
	#@@c

	def undoReplace (self,v,oldv):
	
		#trace("v   :%s" % v)
		#trace("oldv:%s" % oldv)
		assert(v)
		assert(oldv)
		u = self ; c = u.commands
		copies = []
	
		# For each node joined to v, swap in a copy of oldv.
		# trace("old" + `oldv.t.joinList`)
		# trace("new" + `v.t.joinList`)
		joinList = v.t.joinList[:] # Copy the join list: it will change.
		for j in joinList:
			if j != v:
				copy = c.copyTree(oldv)
				copies.append(copy)
				j.swap_links(copy,j)
	
		# Swap v and oldv.
		# trace("final swap")
		v.swap_links(v,oldv)
		# trace("new linked tree:"+`v`)
		
		# Join v to all copies.
		for copy in copies:
			v.joinTreeTo(copy)
			
		# Restore all clone bits.
		c.initAllCloneBits()
		
		return v
	#@-body
	#@-node:4::undoReplace
	#@+node:5::undoRedoText
	#@+body
	# Handle text undo and redo.
	# The terminology is for undo: converts _new_ text into _old_ text.
	
	def undoRedoText (self,v,
		leading,trailing, # Number of matching leading & trailing lines.
		oldMidLines,newMidLines, # Lists of unmatched lines.
		oldNewlines,newNewlines, # Number of trailing newlines.
		tag="undo"): # "undo" or "redo"
	
		u = self ; c = u.commands
		assert(v == c.currentVnode())
	
		
		#@<< Incrementally update the Tk.Text widget >>
		#@+node:1::<< Incrementally update the Tk.Text widget >>
		#@+body
		# Only update the changed lines.
		mid_text = string.join(oldMidLines,'\n')
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
		s = toUnicode(s,app().tkEncoding) # 2/25/03
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
		body = toUnicode(body,"utf-8")
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
		if u.debug_print:
			print "body:  ",`body`
			print "result:",`result`
		#@-body
		#@-node:2::<< Compute the result using v's body text >>

		#trace(`v`)
		#trace("old:"+`v.bodyString()`)
		v.t.setTnodeText(result)
		#trace("new:"+`v.bodyString()`)
		
		#@<< Get textResult from the Tk.Text widget >>
		#@+node:3::<< Get textResult from the Tk.Text widget >>
		#@+body
		textResult = c.frame.body.get("1.0","end")
		textResult = toUnicode(textResult,app().tkEncoding) # 2/25/03
		
		if textResult != result:
			# Remove the newline from textResult if that is the only difference.
			if len(textResult) > 0 and textResult[:-1] == result:
				textResult = result
		#@-body
		#@-node:3::<< Get textResult from the Tk.Text widget >>

		if textResult == result:
			# print "incremental undo:",leading,trailing
			c.tree.recolor_range(v,leading,trailing)
		else: # 11/19/02: # Rewrite the pane and do a full recolor.
			if u.debug_print:
				
				#@<< print mismatch trace >>
				#@+node:4::<< print mismatch trace >>
				#@+body
				print "undo mismatch"
				print "expected:",`result`
				print "actual  :",`textResult`
				
				#@-body
				#@-node:4::<< print mismatch trace >>

			# print "non-incremental undo"
			v.setBodyStringOrPane(result)
	
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
	#@+node:8::undoSortTopLevel
	#@+body
	def undoSortTopLevel (self):
		
		u = self ; c = u.commands
		root = c.rootVnode()
		
		c.beginUpdate()
		c.endEditing()
		v = u.sort[0]
		v.moveToRoot(oldRoot=root)
		for next in u.sort[1:]:
			next.moveAfter(v)
			v = next
		c.setChanged(true)
		c.endUpdate()
	
	#@-body
	#@-node:8::undoSortTopLevel
	#@-node:7::Undo helpers
	#@-others

	
class undoer (baseUndoer):
	"""A class that implements unlimited undo and redo."""
	pass
#@-body
#@-node:0::@file leoUndo.py
#@-leo
