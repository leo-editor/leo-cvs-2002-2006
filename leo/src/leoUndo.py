#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3603:@thin leoUndo.py
#@@language python

# Undo manager for leo.py.

#@<< How Leo implements unlimited undo >>
#@+node:ekr.20031218072017.2413:<< How Leo implements unlimited undo >>
#@+at 
#@nonl
# Only leo.py supports unlimited undo.  Unlimited undo is straightforward; it 
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
#@-node:ekr.20031218072017.2413:<< How Leo implements unlimited undo >>
#@nl
#@<< Define optional ivars >>
#@+node:ekr.20031218072017.3604:<< Define optional ivars >>
optionalIvars = [
	"lastChild",
	"parent","oldParent",
	"back","oldBack",
	"n","oldN","oldV",
	"oldText","newText",
	"oldSel","newSel",
	"sort","select",
	"oldTree","newTree", # Added newTree 10/14/03
	"yview",
	# For incremental undo typing...
	"leading","trailing",
	"oldMiddleLines","newMiddleLines",
	"oldNewlines","newNewlines" ]
#@nonl
#@-node:ekr.20031218072017.3604:<< Define optional ivars >>
#@nl

import leoGlobals as g
from leoGlobals import true,false

import string,types

#@+others
#@+node:ekr.20031218072017.3605:class undoer
class baseUndoer:
	"""The base class of the undoer class."""
	#@	@+others
	#@+node:ekr.20031218072017.3606:undo.__init__ & clearIvars
	def __init__ (self,c):
		
		u = self ; u.c = c
		
		# Ivars to transition to new undo scheme...
		
		u.debug = false # true: enable debugging code in new undo scheme.
		u.debug_print = false # true: enable print statements in debug code.
		u.new_undo = true # true: enable new debug code.
	
		# Statistics comparing old and new ways (only if u.debug is on).
		u.new_mem = 0
		u.old_mem = 0
	
		# State ivars...
		u.undoType = "Can't Undo"
		
		# These must be set here, _not_ in clearUndoState.
		u.redoMenuLabel = "Can't Redo"
		u.undoMenuLabel = "Can't Undo"
		u.realRedoMenuLabel = "Can't Redo"
		u.realUndoMenuLabel = "Can't Undo"
		u.undoing = false # true if executing an Undo command.
		u.redoing = false # true if executing a Redo command.
	#@nonl
	#@+node:ekr.20031218072017.3607:clearIvars
	def clearIvars (self):
		
		self.p = None # The position/node being operated upon for undo and redo.
		for ivar in optionalIvars:
			setattr(self,ivar,None)
	#@nonl
	#@-node:ekr.20031218072017.3607:clearIvars
	#@-node:ekr.20031218072017.3606:undo.__init__ & clearIvars
	#@+node:ekr.20031218072017.3608:State routines...
	#@+node:ekr.20031218072017.3609:clearUndoState
	def clearUndoState (self):
	
		"""Clears then entire Undo state.
		
		All non-undoable commands should call this method."""
		
		u = self
		u.setRedoType("Can't Redo")
		u.setUndoType("Can't Undo")
		u.beads = [] # List of undo nodes.
		u.bead = -1 # Index of the present bead: -1:len(beads)
		u.clearIvars()
	#@nonl
	#@-node:ekr.20031218072017.3609:clearUndoState
	#@+node:ekr.20031218072017.3610:canRedo & canUndo
	# Translation does not affect these routines.
	
	def canRedo (self):
	
		u = self
		return u.redoMenuLabel != "Can't Redo"
	
	def canUndo (self):
	
		u = self
		return u.undoMenuLabel != "Can't Undo"
	#@-node:ekr.20031218072017.3610:canRedo & canUndo
	#@+node:ekr.20031218072017.3611:enableMenuItems
	def enableMenuItems (self):
	
		u = self ; frame = u.c.frame
		
		menu = frame.menu.getMenu("Edit")
		frame.menu.enableMenu(menu,u.redoMenuLabel,u.canRedo())
		frame.menu.enableMenu(menu,u.undoMenuLabel,u.canUndo())
	#@-node:ekr.20031218072017.3611:enableMenuItems
	#@+node:ekr.20031218072017.3612:getBead, peekBead, setBead
	def getBead (self,n):
		
		u = self
		if n < 0 or n >= len(u.beads):
			return None
		d = u.beads[n]
		# g.trace(n,len(u.beads),d)
		self.clearIvars()
		u.p = d["v"]
		u.undoType = d["undoType"]
	
		for ivar in optionalIvars:
			val = d.get(ivar,None)
			setattr(u,ivar,val)
	
		if not u.new_undo: # Recreate an "oldText" entry if necessary.
			if u.undoType == "Typing" and u.oldText == None:
				assert(n > 0)
				old_d = u.beads[n-1]
				# The user will lose data if these asserts fail.
				assert(old_d["undoType"] == "Typing")
				assert(old_d["v"] == u.p)
				u.oldText = old_d["newText"]
				# g.trace(u.oldText)
		return d
		
	def peekBead (self,n):
		
		u = self
		if n < 0 or n >= len(u.beads):
			return None
		d = u.beads[n]
		# g.trace(n,len(u.beads),d)
		return d
	
	def setBead (self,n,keywords=None):
	
		u = self ; d = {}
		d["undoType"]=u.undoType
		d["v"]=u.p
		# Only enter significant entries into the dictionary.
		# This is an important space optimization for typing.
		for ivar in optionalIvars:
			if getattr(u,ivar) != None:
				d[ivar] = getattr(u,ivar)
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
				if old_d["undoType"] == "Typing" and old_d["v"] == u.p:
					del d["oldText"] # We can recreate this entry from old_d["newText"]
					# g.trace(u.oldText)
		# g.trace(d)
		return d
	#@-node:ekr.20031218072017.3612:getBead, peekBead, setBead
	#@+node:ekr.20031218072017.3613:redoMenuName, undoMenuName
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
	#@nonl
	#@-node:ekr.20031218072017.3613:redoMenuName, undoMenuName
	#@+node:ekr.20031218072017.3614:setRedoType, setUndoType
	# These routines update both the ivar and the menu label.
	def setRedoType (self,type):
		u = self ; frame = u.c.frame
		menu = frame.menu.getMenu("Edit")
		name = u.redoMenuName(type)
		if name != u.redoMenuLabel:
			# Update menu using old name.
			realLabel = frame.menu.getRealMenuName(name)
			if realLabel == name:
				underline=g.choose(g.match(name,0,"Can't"),-1,0)
			else:
				underline = realLabel.find("&")
			realLabel = realLabel.replace("&","")
			frame.menu.setMenuLabel(menu,u.realRedoMenuLabel,realLabel,underline=underline)
			u.redoMenuLabel = name
			u.realRedoMenuLabel = realLabel
	
	def setUndoType (self,type):
		u = self ; frame = u.c.frame
		menu = frame.menu.getMenu("Edit")
		name = u.undoMenuName(type)
		if name != u.undoMenuLabel:
			# Update menu using old name.
			realLabel = frame.menu.getRealMenuName(name)
			if realLabel == name:
				underline=g.choose(g.match(name,0,"Can't"),-1,0)
			else:
				underline = realLabel.find("&")
			realLabel = realLabel.replace("&","")
			frame.menu.setMenuLabel(menu,u.realUndoMenuLabel,realLabel,underline=underline)
			u.undoType = type
			u.undoMenuLabel = name
			u.realUndoMenuLabel = realLabel
	#@nonl
	#@-node:ekr.20031218072017.3614:setRedoType, setUndoType
	#@+node:ekr.20031218072017.3615:setUndoParams
	#@+at 
	#@nonl
	# This routine saves enough information so an operation can be undone and 
	# redone.  We do nothing when called from the undo/redo logic because the 
	# Undo and Redo commands merely reset the bead pointer.
	#@-at
	#@@c
	
	def setUndoParams (self,undo_type,p,**keywords):
		
		# g.trace(undo_type,p,keywords)
	
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
		u.p = p.copy()
		u.parent = p.parent()
		u.back = p.back()
		u.n = p.childIndex()
		# Push params on undo stack, clearing all forward entries.
		u.bead += 1
		d = u.setBead(u.bead,keywords)
		u.beads[u.bead:] = [d]
		# g.trace(len(u.beads),u.bead,keywords)
		# Recalculate the menu labels.
		u.setUndoTypes()
		return d
	#@-node:ekr.20031218072017.3615:setUndoParams
	#@+node:ekr.20031218072017.1490:setUndoTypingParams
	#@+at 
	#@nonl
	# This routine saves enough information so a typing operation can be 
	# undone and redone.
	# 
	# We do nothing when called from the undo/redo logic because the Undo and 
	# Redo commands merely reset the bead pointer.
	#@-at
	#@@c
	
	def setUndoTypingParams (self,p,undo_type,oldText,newText,oldSel,newSel,oldYview=None):
		
		# g.trace(undo_type,p,"old:",oldText,"new:",newText)
		u = self ; c = u.c
		#@	<< return if there is nothing to do >>
		#@+node:ekr.20040324061854:<< return if there is nothing to do >>
		if u.redoing or u.undoing:
			return None
		
		if undo_type == None:
			return None
		
		if undo_type == "Can't Undo":
			u.clearUndoState()
			return None
		
		if oldText == newText:
			# g.trace("no change")
			return None
		#@nonl
		#@-node:ekr.20040324061854:<< return if there is nothing to do >>
		#@nl
		#@	<< init the undo params >>
		#@+node:ekr.20040324061854.1:<< init the undo params >>
		# Clear all optional params.
		for ivar in optionalIvars:
			setattr(u,ivar,None)
		
		# Set the params.
		u.undoType = undo_type
		u.p = p
		#@nonl
		#@-node:ekr.20040324061854.1:<< init the undo params >>
		#@nl
		#@	<< compute leading, middle & trailing  lines >>
		#@+node:ekr.20031218072017.1491:<< compute leading, middle & trailing  lines >>
		#@+at 
		#@nonl
		# Incremental undo typing is similar to incremental syntax coloring.  
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
			g.trace()
			print "lead,trail",leading,trailing
			print "old mid,nls:",len(old_middle_lines),old_newlines,oldText
			print "new mid,nls:",len(new_middle_lines),new_newlines,newText
			#print "lead,trail:",leading,trailing
			#print "old mid:",old_middle_lines
			#print "new mid:",new_middle_lines
			print "---------------------"
		#@nonl
		#@-node:ekr.20031218072017.1491:<< compute leading, middle & trailing  lines >>
		#@nl
		#@	<< save undo text info >>
		#@+node:ekr.20031218072017.1492:<< save undo text info >>
		#@+at 
		#@nonl
		# This is the start of the incremental undo algorithm.
		# 
		# We must save enough info to do _both_ of the following:
		# 
		# Undo: Given newText, recreate oldText.
		# Redo: Given oldText, recreate oldText.
		# 
		# The "given" texts for the undo and redo routines are simply 
		# v.bodyString().
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
		#@nonl
		#@-node:ekr.20031218072017.1492:<< save undo text info >>
		#@nl
		#@	<< save the selection and scrolling position >>
		#@+node:ekr.20040324061854.2:<< save the selection and scrolling position >>
		#Remember the selection.
		u.oldSel = oldSel
		u.newSel = newSel
		
		# Remember the scrolling position.
		if oldYview:
			u.yview = oldYview
		else:
			u.yview = c.frame.body.getYScrollPosition()
		#@-node:ekr.20040324061854.2:<< save the selection and scrolling position >>
		#@nl
		#@	<< adjust the undo stack, clearing all forward entries >>
		#@+node:ekr.20040324061854.3:<< adjust the undo stack, clearing all forward entries >>
		# Push params on undo stack, clearing all forward entries.
		u.bead += 1
		d = u.setBead(u.bead)
		u.beads[u.bead:] = [d]
		
		# g.trace(len(u.beads), u.bead)
		#@nonl
		#@-node:ekr.20040324061854.3:<< adjust the undo stack, clearing all forward entries >>
		#@nl
		u.setUndoTypes() # Recalculate the menu labels.
		return d
	#@nonl
	#@-node:ekr.20031218072017.1490:setUndoTypingParams
	#@+node:ekr.20031218072017.3616:setUndoTypes
	def setUndoTypes (self):
		
		u = self
		# g.trace(u.bead,len(u.beads))
	
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
	#@nonl
	#@-node:ekr.20031218072017.3616:setUndoTypes
	#@-node:ekr.20031218072017.3608:State routines...
	#@+node:ekr.20031218072017.2030:u.redo
	def redo (self):
	
		u = self ; c = u.c
		if not u.canRedo(): return
		if not u.getBead(u.bead+1): return
		current = c.currentPosition()
		if not current: return
		# g.trace(u.bead+1,len(u.beads),u.peekBead(u.bead+1))
		u.redoing = true ; redrawFlag = true
		redoType = u.undoType # Use the type of the next bead.
		updateSetChangedFlag = true
		c.beginUpdate()
		if 1: # range...
			#@		<< redo clone cases >>
			#@+node:ekr.20031218072017.2031:<< redo clone cases >>
			if redoType in ("Clone Node","Drag & Clone"):
				
				if u.back:
					u.p.linkAfter(u.back)
				elif u.parent:
					u.p.linkAsNthChild(u.parent,0)
				else:
					oldRoot = c.rootPosition()
					u.p.linkAsRoot(oldRoot)
			
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2031:<< redo clone cases >>
			#@nl
			#@		<< redo hoist cases >>
			#@+node:ekr.20031218072017.2033:<< redo hoist cases >>
			elif redoType == "Hoist":
				
				c.selectVnode(u.p)
				c.hoist()
				updateSetChangedFlag = false
				
			elif redoType == "De-Hoist":
				
				c.selectVnode(u.p)
				c.dehoist()
				updateSetChangedFlag = false
			#@nonl
			#@-node:ekr.20031218072017.2033:<< redo hoist cases >>
			#@nl
			#@		<< redo insert cases >>
			#@+node:ekr.20031218072017.2034:<< redo insert cases >>
			elif redoType in ["Import","Insert Node","Paste Node"]:
			
				if u.back:
					u.p.linkAfter(u.back)
				elif u.parent:
					u.p.linkAsNthChild(u.parent,0)
				else:
					oldRoot = c.rootPosition()
					u.p.linkAsRoot(oldRoot)
					
				# Restore all vnodeLists (and thus all clone marks).
				u.p.restoreLinksInTree()
			
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2034:<< redo insert cases >>
			#@nl
			#@		<< redo delete cases >>
			#@+node:ekr.20031218072017.2032:<< redo delete cases >>
			elif redoType == "Delete Node" or redoType == "Cut Node":
			
				c.selectVnode(u.p)
				c.deleteOutline()
			#@nonl
			#@-node:ekr.20031218072017.2032:<< redo delete cases >>
			#@nl
			#@		<< redo move & drag cases >>
			#@+node:ekr.20031218072017.2035:<< redo move & drag cases >>
			elif redoType in ["Drag","Move Down","Move Left","Move Right","Move Up"]:
			
				# g.trace(u.p)
				if u.parent:
					u.p.moveToNthChildOf(u.parent,u.n)
				elif u.back:
					u.p.moveAfter(u.back)
				else:
					oldRoot = c.rootPosition() # Bug fix: 4/9/04
					u.p.moveToRoot(oldRoot)
			
				c.selectVnode(u.p)
				
			elif redoType == "Drag":
			
				u.p.moveToNthChildOf(u.parent,u.n)
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2035:<< redo move & drag cases >>
			#@nl
			#@		<< redo promote and demote cases >>
			#@+node:ekr.20031218072017.2036:<< redo promote and demote cases >>
			elif redoType == "Demote":
			
				c.selectVnode(u.p)
				c.demote()
				
			elif redoType == "Promote":
			
				c.selectVnode(u.p)
				c.promote()
			#@nonl
			#@-node:ekr.20031218072017.2036:<< redo promote and demote cases >>
			#@nl
			#@		<< redo replace cases >>
			#@+node:ekr.20031218072017.1713:<< redo replace cases >>
			elif redoType in (
				"Convert All Blanks","Convert All Tabs",
				"Extract","Extract Names","Extract Section",
				"Read @file Nodes"):
			
				u.p = self.undoReplace(u.p,u.oldTree,u.newTree,u.newText)
				c.selectVnode(u.p) # Does full recolor.
				if u.newSel:
					c.frame.body.setTextSelection(u.newSel)
				redrawFlag = redoType in ("Extract","Extract Names","Extract Section","Read @file Nodes")
			#@nonl
			#@-node:ekr.20031218072017.1713:<< redo replace cases >>
			#@nl
			#@		<< redo sort cases >>
			#@+node:ekr.20031218072017.2037:<< redo sort cases >>
			elif redoType == "Sort Children":
			
				c.selectVnode(u.p)
				c.sortChildren()
			
			elif redoType == "Sort Siblings":
			
				c.selectVnode(u.p)
				c.sortSiblings()
				
			elif redoType == "Sort Top Level":
				
				c.selectVnode(u.p)
				c.sortTopLevel()
				u.p = None # don't mark u.p dirty
			#@nonl
			#@-node:ekr.20031218072017.2037:<< redo sort cases >>
			#@nl
			#@		<< redo typing cases >>
			#@+node:ekr.20031218072017.2038:<< redo typing cases >>
			elif redoType in ( "Typing",
				"Change","Convert Blanks","Convert Tabs","Cut",
				"Delete","Indent","Paste","Reformat Paragraph","Undent"):
			
				# g.trace(redoType,u.p)
				# selectVnode causes recoloring, so avoid if possible.
				if current != u.p:
					c.selectVnode(u.p)
				elif redoType in ("Cut","Paste"):
					c.frame.body.forceFullRecolor()
			
				self.undoRedoText(
					u.p,u.leading,u.trailing,
					u.newMiddleLines,u.oldMiddleLines,
					u.newNewlines,u.oldNewlines,
					tag="redo",undoType=redoType)
				
				if u.newSel:
					c.frame.body.setTextSelection(u.newSel)
				if u.yview:
					c.frame.body.setYScrollPosition(u.yview)
				redrawFlag = (current != u.p)
					
			elif redoType == "Change All":
			
				count = 0
				while 1:
					u.bead += 1
					d = u.getBead(u.bead+1)
					assert(d)
					redoType = u.undoType
					# g.trace(redoType,u.p,u.newText)
					if redoType == "Change All":
						c.selectVnode(u.p)
						break
					elif redoType == "Change":
						u.p.v.setTnodeText(u.newText)
						u.p.setDirty()
						count += 1
					elif redoType == "Change Headline":
						u.p.initHeadString(u.newText)
						count += 1
					else: assert(false)
				g.es("redo %d instances" % count)
			
			elif redoType == "Change Headline":
				
				# g.trace(redoType,u.p,u.newText)
				u.p.setHeadStringOrHeadline(u.newText)
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2038:<< redo typing cases >>
			#@nl
			else: g.trace("Unknown case: ",redoType)
			if updateSetChangedFlag:
				c.setChanged(true)
				if u.p: u.p.setDirty()
		c.endUpdate(redrawFlag) # 11/08/02
		u.redoing = false
		u.bead += 1
		u.setUndoTypes()
	#@nonl
	#@-node:ekr.20031218072017.2030:u.redo
	#@+node:ekr.20031218072017.2039:u.undo
	def undo (self):
	
		"""This function and its allies undo the operation described by the undo parmaters."""
		
		u = self ; c = u.c
		if not u.canUndo(): return
		if not u.getBead(u.bead): return
		current = c.currentPosition()
		if not current: return
		# g.trace(len(u.beads),u.bead,u.peekBead(u.bead))
		c.endEditing()# Make sure we capture the headline for a redo.
		u.undoing = true
		undoType = u.undoType
		redrawFlag = true
		updateSetChangedFlag = true
		c.beginUpdate()
		if 1: # update...
			#@		<< undo clone cases >>
			#@+node:ekr.20031218072017.2040:<< undo clone cases >>
			# We can immediately delete the clone because clone() can recreate it using only v.
			
			if undoType == "Clone Node":
				
				c.selectVnode(u.p)
				c.deleteOutline()
				c.selectVnode(u.back)
			
			elif undoType == "Drag & Clone":
				
				c.selectVnode(u.p)
				c.deleteOutline()
				c.selectVnode(u.oldV)
			#@nonl
			#@-node:ekr.20031218072017.2040:<< undo clone cases >>
			#@nl
			#@		<< undo delete cases >>
			#@+node:ekr.20031218072017.2041:<< undo delete cases >>
			#@+at 
			#@nonl
			# Deleting a clone is _not_ the same as undoing a clone:
			# the clone may have been moved, so there is no necessary 
			# relationship between the two nodes.
			#@-at
			#@@c
			
			elif undoType == "Delete Node" or undoType == "Cut Node":
				
				if u.back:
					u.p.linkAfter(u.back)
				elif u.parent:
					u.p.linkAsNthChild(u.parent,0)
				else:
					oldRoot = c.rootPosition()
					u.p.linkAsRoot(oldRoot)
					
				# Restore all vnodeLists (and thus all clone marks).
				u.p.restoreLinksInTree()
			
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2041:<< undo delete cases >>
			#@nl
			#@		<< undo hoist cases >>
			#@+node:ekr.20031218072017.2042:<< undo hoist cases >>
			elif undoType == "Hoist":
				
				c.selectVnode(u.p)
				c.dehoist()
				updateSetChangedFlag = false
			
			elif undoType == "De-Hoist":
				
				c.selectVnode(u.p)
				c.hoist()
				updateSetChangedFlag = false
			#@-node:ekr.20031218072017.2042:<< undo hoist cases >>
			#@nl
			#@		<< undo insert cases >>
			#@+node:ekr.20031218072017.2043:<< undo insert cases >>
			elif undoType in ["Import","Insert Node","Paste Node"]:
				
				# g.trace(u.p)
				c.selectVnode(u.p)
				c.deleteOutline()
				if u.select:
					# g.trace("Insert/Paste:",u.select)
					c.selectVnode(u.select)
			#@nonl
			#@-node:ekr.20031218072017.2043:<< undo insert cases >>
			#@nl
			#@		<< undo move & drag cases >>
			#@+node:ekr.20031218072017.2044:<< undo move  & drag cases >>
			elif undoType in ["Drag", "Move Down","Move Left","Move Right","Move Up"]:
			
				# g.trace("oldParent",u.oldParent)
			
				if u.oldParent:
					u.p.moveToNthChildOf(u.oldParent,u.oldN)
				elif u.oldBack:
					u.p.moveAfter(u.oldBack)
				else:
					oldRoot = c.rootPosition() # Bug fix: 4/9/04
					u.p.moveToRoot(oldRoot)
			
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2044:<< undo move  & drag cases >>
			#@nl
			#@		<< undo promote and demote cases >>
			#@+node:ekr.20031218072017.2045:<< undo promote and demote cases >>
			#@+at 
			#@nonl
			# Promote and demote operations are the hard to undo, because they 
			# involve relinking a list of nodes. We pass the work off to 
			# routines dedicated to the task.
			#@-at
			#@@c
			
			elif undoType == "Demote":
			
				u.undoDemote()
			
			elif undoType == "Promote":
				
				u.undoPromote()
			#@nonl
			#@-node:ekr.20031218072017.2045:<< undo promote and demote cases >>
			#@nl
			#@		<< undo replace cases >>
			#@+node:ekr.20031218072017.1712:<< undo replace cases >>
			elif undoType in (
				"Convert All Blanks","Convert All Tabs",
				"Extract","Extract Names","Extract Section",
				"Read @file Nodes"):
			
				u.p = self.undoReplace(u.p,u.newTree,u.oldTree,u.oldText)
				c.selectVnode(u.p) # Does full recolor.
				if u.oldSel:
					c.frame.body.setTextSelection(u.oldSel)
				redrawFlag = true
			#@nonl
			#@-node:ekr.20031218072017.1712:<< undo replace cases >>
			#@nl
			#@		<< undo sort cases >>
			#@+node:ekr.20031218072017.2046:<< undo sort cases >>
			#@+at 
			#@nonl
			# Sort operations are the hard to undo, because they involve 
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
				u.p = None # don't mark u.p dirty
			#@nonl
			#@-node:ekr.20031218072017.2046:<< undo sort cases >>
			#@nl
			#@		<< undo typing cases >>
			#@+node:ekr.20031218072017.2047:<< undo typing cases >>
			#@+at 
			#@nonl
			# When making "large" changes to text, we simply save the old and 
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
			
				# g.trace(undoType,u.p)
				# selectVnode causes recoloring, so don't do this unless needed.
				if current != u.p:
					c.selectVnode(u.p)
				elif undoType in ("Cut","Paste"):
					c.frame.body.forceFullRecolor()
			
				self.undoRedoText(
					u.p,u.leading,u.trailing,
					u.oldMiddleLines,u.newMiddleLines,
					u.oldNewlines,u.newNewlines,
					tag="undo",undoType=undoType)
				if u.oldSel:
					c.frame.body.setTextSelection(u.oldSel)
				if u.yview:
					c.frame.body.setYScrollPosition(u.yview)
				redrawFlag = (current != u.p)
					
			elif undoType == "Change All":
			
				count = 0
				while 1:
					u.bead -= 1
					d = u.getBead(u.bead)
					assert(d)
					undoType = u.undoType
					# g.trace(undoType,u.p,u.oldText)
					if undoType == "Change All":
						c.selectVnode(u.p)
						break
					elif undoType == "Change":
						u.p.setTnodeText(u.oldText)  # p.setTnodeText
						count += 1
						u.p.setDirty()
					elif undoType == "Change Headline":
						u.p.initHeadString(u.oldText)  # p.initHeadString
						count += 1
					else: assert(false)
				g.es("undo %d instances" % count)
					
			elif undoType == "Change Headline":
				
				# g.trace(u.oldText)
				u.p.setHeadStringOrHeadline(u.oldText)
				c.selectVnode(u.p)
			#@nonl
			#@-node:ekr.20031218072017.2047:<< undo typing cases >>
			#@nl
			else: g.trace("Unknown case: ",u.undoType)
			if updateSetChangedFlag:
				c.setChanged(true)
				if u.p: u.p.setDirty()
		c.endUpdate(redrawFlag) # 11/9/02
		u.undoing = false
		u.bead -= 1
		u.setUndoTypes()
		# g.print_stats()
	#@-node:ekr.20031218072017.2039:u.undo
	#@+node:ekr.20031218072017.3617:Undo helpers
	#@+node:ekr.20031218072017.3618:u.saveTree, restoreExtraAttributes
	def saveTree (self,p):
		
		tree = None ## no longer used??
		headlines = []
		bodies = []
		extraAttributes = []
		for p in p.self_and_subtree_iter(copy=true):
			headlines.append(p.headString())
			bodies.append(p.bodyString())
			data = p.v.extraAttributes(), p.v.t.extraAttributes()
			extraAttributes.append(data)
	
		return tree, headlines, bodies, extraAttributes
	
	def restoreExtraAttributes (self,v,extraAttributes):
	
		v_extraAttributes, t_extraAttributes = extraAttributes
		v.setExtraAttributes(v_extraAttributes)
		v.t.setExtraAttributes(t_extraAttributes)
	#@nonl
	#@-node:ekr.20031218072017.3618:u.saveTree, restoreExtraAttributes
	#@+node:ekr.20031218072017.3620:undoDemote
	# undoes the previous demote operation.
	def undoDemote (self):
		
		u = self ; c = u.c
		p   = u.p.copy()
		ins = u.p.copy()
		last = u.lastChild
		assert(p.hasFirstChild)
		child = p.firstChild()
		c.beginUpdate()
		if 1: # update...
			# Do not undemote children up to last.
			# Do not use an iterator here.
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
			c.selectVnode(p)
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.3620:undoDemote
	#@+node:ekr.20031218072017.3621:undoPromote
	# Undoes the previous promote operation.
	def undoPromote (self):
		
		u = self ; c = u.c ; p = u.p
		next = p.next()
		last = u.lastChild
		assert(next)
		c.beginUpdate()
		if 1: # update...
			while next: # don't use an iterator here.
				p2 = next
				next = p2.next()
				n = p.numberOfChildren()
				p2.moveToNthChildOf(p,n)
				if p2 == last: break
			c.selectVnode(p)
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.3621:undoPromote
	#@+node:ekr.20031218072017.1714:undoReplace
	#@+at 
	#@nonl
	# This routine implements undo for any kind of operation, no matter how 
	# complex.  Just do:
	# 
	# 	v_copy = c.undoer.saveTree(v)
	# 	...make arbitrary changes to p's tree.
	# 	c.undoer.setUndoParams("Op Name",p,select=current,oldTree=v_copy)
	#@-at
	#@@c
	
	def undoReplace (self,p,new_data,old_data,text):
	
		"""Replace new_v with old_v during undo."""
	
		u = self ; c = u.c
		if 0:
			g.trace(u.undoType)
			g.trace("u.bead",u.bead, type(u.peekBead(u.bead)))
			g.trace("new_data:",type(new_data))
			g.trace("old_data:",type(old_data))
	
		assert(type(new_data)==type((),) or type(old_data)==type((),))
	
		# new_data will be None the first time we undo this operation.
		# In that case, we must save the new tree for later undo operation.
		try:
			new_v, new_headlines, new_bodies, new_attributes = new_data
		except:
			new_data = u.saveTree(p)
			new_v, new_headlines, new_bodies, new_attributes = new_data
			# Put the new data in the bead.
			d = u.beads[u.bead]
			d["newTree"] = new_data
			u.beads[u.bead] = d
			
		# The previous code should already have created this data.
		old_v, old_headlines, old_bodies, old_attributes = old_data
		assert(new_bodies != None)
		assert(old_bodies != None)
	
		result = old_v
	
		# Restore all headlines and bodies from the saved lists.
		encoding = g.app.tkEncoding
		i = 0
		for p in result.self_and_subtree_iter():
			p.initHeadString(old_headlines[i],encoding)
			p.setTnodeText(old_bodies[i],encoding)
			u.restoreExtraAttributes(p,old_attributes[i])
			i += 1
	
		result.setBodyStringOrPane(result.bodyString())
		return result
	#@nonl
	#@-node:ekr.20031218072017.1714:undoReplace
	#@+node:ekr.20031218072017.1493:undoRedoText
	# Handle text undo and redo.
	# The terminology is for undo: converts _new_ text into _old_ text.
	
	def undoRedoText (self,p,
		leading,trailing, # Number of matching leading & trailing lines.
		oldMidLines,newMidLines, # Lists of unmatched lines.
		oldNewlines,newNewlines, # Number of trailing newlines.
		tag="undo", # "undo" or "redo"
		undoType=None):
	
		u = self ; c = u.c
		assert(p == c.currentPosition())
		v = p.v
	
		#@	<< Incrementally update the Tk.Text widget >>
		#@+node:ekr.20031218072017.1494:<< Incrementally update the Tk.Text widget >>
		# Only update the changed lines.
		mid_text = string.join(oldMidLines,'\n')
		new_mid_len = len(newMidLines)
		# Maybe this could be simplified, and it is good to treat the "end" with care.
		if trailing == 0:
			c.frame.body.deleteLine(leading)
			if leading > 0:
				c.frame.body.insertAtEnd('\n')
			c.frame.body.insertAtEnd(mid_text)
		else:
			if new_mid_len > 0:
				c.frame.body.deleteLines(leading,new_mid_len)
			elif leading > 0:
				c.frame.body.insertAtStartOfLine(leading,'\n')
			c.frame.body.insertAtStartOfLine(leading,mid_text)
		# Try to end the Tk.Text widget with oldNewlines newlines.
		# This may be off by one, and we don't care because
		# we never use body text to compute undo results!
		s = c.frame.body.getAllText()
		newlines = 0 ; i = len(s) - 1
		while i >= 0 and s[i] == '\n':
			newlines += 1 ; i -= 1
		while newlines > oldNewlines:
			c.frame.body.deleteLastChar()
			newlines -= 1
		if oldNewlines > newlines:
			c.frame.body.insertAtEnd('\n'*(oldNewlines-newlines))
		#@nonl
		#@-node:ekr.20031218072017.1494:<< Incrementally update the Tk.Text widget >>
		#@nl
		#@	<< Compute the result using v's body text >>
		#@+node:ekr.20031218072017.1495:<< Compute the result using v's body text >>
		# Recreate the text using the present body text.
		body = v.bodyString()
		body = g.toUnicode(body,"utf-8")
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
			print "body:  ",body
			print "result:",result
		#@nonl
		#@-node:ekr.20031218072017.1495:<< Compute the result using v's body text >>
		#@nl
		# g.trace(v)
		# g.trace("old:",v.bodyString())
		v.setTnodeText(result)
		# g.trace("new:",v.bodyString())
		#@	<< Get textResult from the Tk.Text widget >>
		#@+node:ekr.20031218072017.1496:<< Get textResult from the Tk.Text widget >>
		textResult = c.frame.body.getAllText()
		
		if textResult != result:
			# Remove the newline from textResult if that is the only difference.
			if len(textResult) > 0 and textResult[:-1] == result:
				textResult = result
		#@nonl
		#@-node:ekr.20031218072017.1496:<< Get textResult from the Tk.Text widget >>
		#@nl
		if textResult == result:
			if undoType in ("Cut","Paste"):
				# g.trace("non-incremental undo")
				c.frame.body.recolor(p,incremental=false)
			else:
				# g.trace("incremental undo:",leading,trailing)
				c.frame.body.recolor_range(p,leading,trailing)
		else: # 11/19/02: # Rewrite the pane and do a full recolor.
			if u.debug_print:
				#@			<< print mismatch trace >>
				#@+node:ekr.20031218072017.1497:<< print mismatch trace >>
				print "undo mismatch"
				print "expected:",result
				print "actual  :",textResult
				#@nonl
				#@-node:ekr.20031218072017.1497:<< print mismatch trace >>
				#@nl
			# g.trace("non-incremental undo")
			p.setBodyStringOrPane(result)
	#@nonl
	#@-node:ekr.20031218072017.1493:undoRedoText
	#@+node:ekr.20031218072017.3622:undoSortChildren
	def undoSortChildren (self):
	
		u = self ; c = u.c ; p = u.p
		assert(p)
		c.beginUpdate()
		if 1: # inside update...
			c.endEditing()
			index = 0
			for child in u.sort:
				child.moveToNthChildOf(p,index)
				index += 1
			p.setDirty()
			c.setChanged(true)
		c.endUpdate()
	#@nonl
	#@-node:ekr.20031218072017.3622:undoSortChildren
	#@+node:ekr.20031218072017.3623:undoSortSiblings
	def undoSortSiblings (self):
		
		u = self ; c = u.c ; p = u.p
		parent = p.parent()
		assert(p and parent)
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
	#@nonl
	#@-node:ekr.20031218072017.3623:undoSortSiblings
	#@+node:ekr.20031218072017.3624:undoSortTopLevel
	def undoSortTopLevel (self):
		
		u = self ; c = u.c
		root = c.rootPosition()
		
		c.beginUpdate()
		c.endEditing()
		v = u.sort[0]
		v.moveToRoot(oldRoot=root)
		for next in u.sort[1:]:
			next.moveAfter(v)
			v = next
		c.setChanged(true)
		c.endUpdate()
	#@-node:ekr.20031218072017.3624:undoSortTopLevel
	#@-node:ekr.20031218072017.3617:Undo helpers
	#@-others
	
class undoer (baseUndoer):
	"""A class that implements unlimited undo and redo."""
	pass
#@nonl
#@-node:ekr.20031218072017.3605:class undoer
#@+node:ekr.20031218072017.2243:class nullUndoer
class nullUndoer (undoer):

	def __init__ (self,c):
		
		undoer.__init__(self,c) # init the base class.
		
	def clearUndoState (self):
		pass
		
	def canRedo (self):
		return false

	def canUndo (self):
		return false
		
	def enableMenuItems (self):
		pass

	def getBead (self,n):
		return {}
	
	def peekBead (self,n):
		return {}

	def setBead (self,n,keywords=None):
		return {}
		
	def redoMenuName (self,name):
		return "Can't Redo"
	
	def undoMenuName (self,name):
		return "Can't Undo"
			
	def setUndoParams (self,undo_type,v,**keywords):
		pass
		
	def setUndoTypingParams (self,v,undo_type,oldText,newText,oldSel,newSel,oldYview=None):
		pass
		
	def setUndoTypes (self):
		pass
		
#@nonl
#@-node:ekr.20031218072017.2243:class nullUndoer
#@-others
#@nonl
#@-node:ekr.20031218072017.3603:@thin leoUndo.py
#@-leo
