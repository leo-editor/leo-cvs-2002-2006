#@+leo-ver=4
#@+node:@file leoTkinterTree.py
#@@language python

#@<< about the tree classes >>
#@+node:<< about the tree classes >>
#@+at 
#@nonl
# This class implements a tree control similar to Windows explorer.  The draw 
# code is based on code found in Python's IDLE program.  Thank you Guido van 
# Rossum!
# 
# The tree class knows about vnodes.  The vnode class could be split into a 
# base class (say a treeItem class) containing the ivars known to the tree 
# class, and a derived class containing everything else, including, e.g., the 
# bodyString ivar.  I haven't chosen to split the vnode class this way because 
# nothing would be gained in Leo.
#@-at
#@-node:<< about the tree classes >>
#@nl

from leoGlobals import *
import leoFrame
import Tkinter,tkFont
import os,string,types

#@<< about drawing >>
#@+node:<< About drawing >>
#@+at 
#@nonl
# Leo must redraw the outline pane when commands are executed and as the 
# result of mouse and keyboard events.  The main challenges are eliminating 
# flicker and handling events properly.
# 
# Eliminating flicker.  Leo must update the outline pane with minimum 
# flicker.  Various versions of Leo have approached this problem in different 
# ways.  The drawing code in leo.py is robust, flexible, relatively simple and 
# should work in almost any conceivable environment.
# 
# Leo assumes that all code that changes the outline pane will be enclosed in 
# matching calls to the c.beginUpdate and c.endUpdate  methods of the Commands 
# class. c.beginUpdate() inhibits drawing until the matching c.endUpdate().  
# These calls may be nested; only the outermost call to c.endUpdate() calls 
# c.redraw() to force a redraw of the outline pane.
# 
# In leo.py, code may call c.endUpdate(flag) instead of c.endUpdate().  Leo 
# redraws the screen only if flag is true.  This allows code to suppress 
# redrawing entirely when needed.  For example, study the idle_body_key event 
# handler to see how Leo conditionally redraws the outline pane.
# 
# The leoTree class redraws all icons automatically when c.redraw() is 
# called.  This is a major simplification compared to previous versions of 
# Leo.  The entire machinery of drawing icons in the vnode class has been 
# eliminated.  The v.computeIcon method tells what the icon should be.  The 
# v.iconVal ivar that tells what the present icon is. The event handler simply 
# compares these two values and sets redraw_flag if they don't match.
#@-at
#@nonl
#@-node:<< About drawing >>
#@nl
#@<< drawing constants >>
#@+node:<< drawing constants >>
box_padding = 5 # extra padding between box and icon
box_width = 9 + box_padding
icon_width = 20
text_indent = 4 # extra padding between icon and tex
child_indent = 28 # was 20
hline_y = 7 # Vertical offset of horizontal line
root_left = 7 + box_width
root_top = 2
hiding = true # True if we don't reallocate items
line_height = 17 + 2 # To be replaced by Font height
#@nonl
#@-node:<< drawing constants >>
#@nl

class leoTkinterTree (leoFrame.leoTree):
	
	callbacksInjected = false

	"""Leo tkinter tree class."""
	
	#@	@+others
	#@+node:tree.__init__
	def __init__(self,c,frame,canvas):
		
		# Init the base class.
		leoFrame.leoTree.__init__(self,frame)
	
		# Objects associated with this tree.
		self.canvas = canvas
	
		# Miscellaneous info.
		self.iconimages = {} # Image cache set by getIconImage().
		self.active = false # true if tree is active
		
		# Set self.font and self.fontName.
		self.setFontFromConfig()
		
		# Recycling bindings.
		self.bindings = [] # List of bindings to be unbound when redrawing.
		self.tagBindings = [] # List of tag bindings to be unbound when redrawing.
		self.icon_id_dict = {} # New in 3.12: keys are icon id's, values are vnodes.
		self.widgets = [] # Widgets that must be destroyed when redrawing.
		
		# Drag and drop
		self.drag_v = None
		self.controlDrag = false # true: control was down when drag started.
		self.drag_id = None # To reset bindings after drag
		self.keyCount = 0 # For debugging.
		
		# 20-SEP-2002 DTHEIN: keep track of popup menu so we can handle
		#                     behavior better on Linux
		# Context menu
		self.popupMenu = None
		
		# Incremental redraws:
		self.allocateOnlyVisibleNodes = false # true: enable incremental redraws.
		self.trace = false # true enabling of various traces.
		self.prevMoveToFrac = None
		self.visibleArea = None
		self.expandedVisibleArea = None
		
		self.allocatedNodes = 0 # A crucial statistic.
			# Incremental drawing allocates visible nodes at most twice.
			# Non-incremetal drawing allocates all visible nodes once.
			
		if self.allocateOnlyVisibleNodes:
			self.frame.bar1.bind("<B1-ButtonRelease>", self.redraw)
		
		if not leoTkinterTree.callbacksInjected: # Class var.
			leoTkinterTree.callbacksInjected = true
			self.injectCallbacks()
	#@nonl
	#@-node:tree.__init__
	#@+node:tree.deleteBindings
	def deleteBindings (self):
		
		"""Delete all tree bindings and all references to tree widgets."""
		
		# print "deleteBindings: %d, %d" % (len(self.tagBindings),len(self.bindings))
	
		count = 0
		# Unbind all the tag bindings.
		for id,id2,binding in self.tagBindings:
			self.canvas.tag_unbind(id,binding,id2)
			count += 1
		self.tagBindings = []
		# Unbind all the text bindings.
		for t,id,binding in self.bindings:
			t.unbind(binding,id)
			count += 1
		self.bindings = []
		# print("bindings freed:"+`count`)
	#@nonl
	#@-node:tree.deleteBindings
	#@+node:tree.deleteWidgets
	# canvas.delete("all") does _not_ delete the Tkinter objects associated with those objects!
	
	def deleteWidgets (self):
		
		"""Delete all widgets in the canvas"""
		
		self.icon_id_dict = {} # Delete all references to icons.
		self.edit_text_dict = {} # Delete all references to Tk.Edit widgets.
			
		# Fixes a _huge_ memory leak.
		for w in self.widgets:
			w.destroy() 
		self.widgets = []
	#@nonl
	#@-node:tree.deleteWidgets
	#@+node:tree.injectCallbacks (class method)
	def injectCallbacks(self):
		
		import leoNodes
		
		#@	<< define tkinter callbacks to be injected in the vnode class >>
		#@+node:<< define tkinter callbacks to be injected in the vnode class >>
		# N.B. These vnode methods are entitled to know about details of the leoTkinterTree class.
		
		#@+others
		#@+node:OnBoxClick
		# Called when the box is clicked.
		
		def OnBoxClick(self,event=None):
			
			"""Callback injected into vnode class."""
		
			# trace()
			try:
				v = self ; c = v.c
				if not doHook("boxclick1",c=c,v=v,event=event):
					c.frame.tree.OnBoxClick(v)
				doHook("boxclick2",c=c,v=v,event=event)
			except:
				es_event_exception("boxclick")
		#@nonl
		#@-node:OnBoxClick
		#@+node:OnDrag
		def OnDrag(self,event=None):
			
			"""Callback injected into vnode class."""
		
			# trace()
			try:
				v = self ; c = v.c
				if c.frame.tree.dragging():
					if not doHook("dragging1",c=c,v=v,event=event):
						c.frame.tree.OnDrag(v,event)
					doHook("dragging2",c=c,v=v,event=event)
				else:
					if not doHook("drag1",c=c,v=v,event=event):
						c.frame.tree.OnDrag(v,event)
					doHook("drag2",c=c,v=v,event=event)
			except:
				es_event_exception("drag")
		#@nonl
		#@-node:OnDrag
		#@+node:OnEndDrag
		def OnEndDrag(self,event=None):
			
			"""Callback injected into vnode class."""
			
			# trace()
		
			try:
				v = self ; c = v.c
				# 7/10/03: Always call frame.OnEndDrag, regardless of state.
				if not doHook("enddrag1",c=c,v=v,event=event):
					c.frame.tree.OnEndDrag(v,event)
				doHook("enddrag2",c=c,v=v,event=event)
			except:
				es_event_exception("enddrag")
		#@nonl
		#@-node:OnEndDrag
		#@+node:OnHeadlineClick & OnHeadlineRightClick
		def OnHeadlineClick(self,event=None):
			"""Callback injected into vnode class."""
			#trace()
			try:
				v = self ; c = v.c
				if not doHook("headclick1",c=c,v=v,event=event):
					c.frame.tree.OnActivate(v)
				doHook("headclick2",c=c,v=v,event=event)
			except:
				es_event_exception("headclick")
			
		def OnHeadlineRightClick(self,event=None):
			"""Callback injected into vnode class."""
			#trace()
			try:
				v = self ; c = v.c
				if not doHook("headrclick1",c=c,v=v,event=event):
					c.frame.tree.OnActivate(v)
					c.frame.tree.OnPopup(self,event)
				doHook("headrclick2",c=c,v=v,event=event)
			except:
				es_event_exception("headrclick")
		#@nonl
		#@-node:OnHeadlineClick & OnHeadlineRightClick
		#@+node:OnHyperLinkControlClick
		def OnHyperLinkControlClick (self,event):
			
			"""Callback injected into vnode class."""
		
			# trace()
			try:
				v = self ; c = v.c
				if not doHook("hypercclick1",c=c,v=v,event=event):
					c.beginUpdate()
					c.selectVnode(v)
					c.endUpdate()
					c.frame.bodyCtrl.mark_set("insert","1.0")
				doHook("hypercclick2",c=c,v=v,event=event)
			except:
				es_event_exception("hypercclick")
		#@nonl
		#@-node:OnHyperLinkControlClick
		#@+node:OnHeadlineKey
		def OnHeadlineKey (self,event=None):
		
			"""Callback injected into vnode class."""
		
			try:
				v = self ; c = v.c
				if not doHook("headkey1",c=c,v=v,event=event):
					c.frame.tree.OnHeadlineKey(v,event)
				doHook("headkey2",c=c,v=v,event=event)
			except:
				es_event_exception("headkey")
		#@nonl
		#@-node:OnHeadlineKey
		#@+node:OnHyperLinkEnter
		def OnHyperLinkEnter (self,event=None):
			
			"""Callback injected into vnode class."""
		
			try:
				v = self ; c = v.c
				if not doHook("hyperenter1",c=c,v=v,event=event):
					if 0: # This works, and isn't very useful.
						c.frame.bodyCtrl.tag_config(v.tagName,background="green")
				doHook("hyperenter2",c=c,v=v,event=event)
			except:
				es_event_exception("hyperenter")
		#@nonl
		#@-node:OnHyperLinkEnter
		#@+node:OnHyperLinkLeave
		def OnHyperLinkLeave (self,event=None):
			
			"""Callback injected into vnode class."""
		
			try:
				v = self ; c = v.c
				if not doHook("hyperleave1",c=c,v=v,event=event):
					if 0: # This works, and isn't very useful.
						c.frame.bodyCtrl.tag_config(v.tagName,background="white")
				doHook("hyperleave2",c=c,v=v,event=event)
			except:
				es_event_exception("hyperleave")
		#@nonl
		#@-node:OnHyperLinkLeave
		#@+node:OnIconClick & OnIconRightClick
		def OnIconClick(self,event=None):
			
			"""Callback injected into vnode class."""
		
			try:
				v = self ; c = v.c
				if not doHook("iconclick1",c=c,v=v,event=event):
					c.frame.tree.OnIconClick(v,event)
				doHook("iconclick2",c=c,v=v,event=event)
			except:
				es_event_exception("iconclick")
			
		def OnIconRightClick(self,event=None):
			
			"""Callback injected into vnode class."""
		
			try:
				v = self ; c = v.c
				if not doHook("iconrclick1",c=c,v=v,event=event):
					c.frame.tree.OnIconRightClick(v,event)
				doHook("iconrclick2",c=c,v=v,event=event)
			except:
				es_event_exception("iconrclick")
		#@-node:OnIconClick & OnIconRightClick
		#@+node:OnIconDoubleClick
		def OnIconDoubleClick(self,event=None):
			
			"""Callback injected into vnode class."""
		
			try:
				v = self ; c = v.c
				if not doHook("icondclick1",c=c,v=v,event=event):
					c.frame.tree.OnIconDoubleClick(self)
				doHook("icondclick2",c=c,v=v,event=event)
			except:
				es_event_exception("icondclick")
		#@-node:OnIconDoubleClick
		#@-others
		#@nonl
		#@-node:<< define tkinter callbacks to be injected in the vnode class >>
		#@nl
	
		for f in (
			OnBoxClick,OnDrag,OnEndDrag,
			OnHeadlineClick,OnHeadlineRightClick,OnHeadlineKey,
			OnHyperLinkControlClick,OnHyperLinkEnter,OnHyperLinkLeave,
			OnIconClick,OnIconDoubleClick,OnIconRightClick):
	
			# trace(f)
			funcToMethod(f,leoNodes.vnode)
	#@nonl
	#@-node:tree.injectCallbacks (class method)
	#@+node:redraw
	# Calling redraw inside c.beginUpdate()/c.endUpdate() does nothing.
	# This _is_ useful when a flag is passed to c.endUpdate.
	
	def redraw (self,event=None):
		
		# trace()
		
		if self.updateCount == 0 and not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
	#@nonl
	#@-node:redraw
	#@+node:force_redraw
	# Schedules a redraw even if inside beginUpdate/endUpdate
	def force_redraw (self):
	
		# trace()
	
		if not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
	#@nonl
	#@-node:force_redraw
	#@+node:redraw_now
	# Redraws immediately: used by Find so a redraw doesn't mess up selections.
	# It is up to the caller to ensure that no other redraws are pending.
	
	def redraw_now (self):
	
		self.idle_redraw()
	#@nonl
	#@-node:redraw_now
	#@+node:idle_redraw
	def idle_redraw (self):
		
		self.redrawScheduled = false # 7/10/03: Always do this here.
	
		frame = self.c.frame
		if frame not in app.windowList or app.quitting:
			# trace("no frame")
			return
			
		if self.drag_v:
			# trace("dragging",self.drag_v)
			return
	
		# trace()
		# print_bindings("canvas",self.canvas)
	
		self.expandAllAncestors(self.currentVnode())
		oldcursor = self.canvas['cursor']
		self.canvas['cursor'] = "watch"
		self.allocatedNodes = 0
		if not doHook("redraw-entire-outline",c=self.c):
			# Erase and redraw the entire tree.
			self.setTopVnode(None)
			self.deleteBindings()
			self.canvas.delete("all")
			self.deleteWidgets()
			self.setVisibleAreaToFullCanvas()
			self.drawTopTree()
			# Set up the scroll region after the tree has been redrawn.
			x0, y0, x1, y1 = self.canvas.bbox("all")
			self.canvas.configure(scrollregion=(0, 0, x1, y1))
			# Do a scrolling operation after the scrollbar is redrawn
			# printGc()
			self.canvas.after_idle(self.idle_scrollTo)
			if self.trace:
				self.redrawCount += 1
				print "idle_redraw allocated:",self.redrawCount, self.allocatedNodes
			doHook("after_redraw-outline",c=self.c)
	
		self.canvas['cursor'] = oldcursor
	#@nonl
	#@-node:idle_redraw
	#@+node:idle_second_redraw
	def idle_second_redraw (self):
		
		# trace()
			
		# Erase and redraw the entire tree the SECOND time.
		# This ensures that all visible nodes are allocated.
		self.setTopVnode(None)
		args = self.canvas.yview()
		self.setVisibleArea(args)
		self.deleteBindings()
		self.canvas.delete("all")
		self.drawTopTree()
		
		if self.trace:
			print "idle_second_redraw allocated:",self.redrawCount, self.allocatedNodes
	#@nonl
	#@-node:idle_second_redraw
	#@+node:About drawing and updating
	#@+at 
	#@nonl
	# About drawing and updating strategy.
	# 
	# This version of Leo draws the outline "by hand" using the Tk canvas 
	# widget.  Surprisingly, this is not only easy, but simplifies the vnode 
	# and Commands classes.
	# 
	# 1.  Updating and redraw.  The tree.redraw() method is called 
	# automatically from the "outermost" call to tree.endUpdate.  Moreover, 
	# calling .tree.redraw() inside a tree.beginUpdate/tree.endUpdate pair 
	# does nothing.  c.redraw(), c.beginUpdate() and c.endUpdate() just call 
	# the corresponding tree methods.  Finally, beginUpdate()/endUpdate(false) 
	# can be used to suppress redrawing entirely.
	# 
	# Therefore, the Commands class never needs to worry about extra calls to 
	# tree.redraw() provided all code that draws to the tree is enclosed in a 
	# tree.beginUpdate/tree.endUpdate pair.  The tree.idle_body_key event 
	# handler manages redrawing "by hand" by maintaining a redraw_flag and 
	# then calling endUpdate(redraw_flag).
	# 
	# 2.  The tree.redraw() method deletes all old canvas items and recomputes 
	# all data, including v.iconVal.  This means that v.doDelete need not 
	# actually delete vnodes for them to disappear from the screen.  Indeed, 
	# vnode are never actually deleted, only unlinked.  It would be valid for 
	# "dependent" vnodes to be deleted, but there really is no need to do so.
	#@-at
	#@-node:About drawing and updating
	#@+node:drawBox (tag_bind)
	def drawBox (self,v,x,y):
		
		y += 7 # draw the box at x, y+7
	
		tree = self
		iconname = choose(v.isExpanded(),"minusnode.gif", "plusnode.gif")
		image = self.getIconImage(iconname)
		id = self.canvas.create_image(x,y,image=image)
		
		if 1: # use vnode callbacks
			id1 = self.canvas.tag_bind(id, "<1>", v.OnBoxClick)
		else:
			#@		<< define onBoxClickCallback >>
			#@+node:<< define onBoxClickCallback >>
			def onBoxClickCallback(event,tree=tree,v=v):
				try:
					c = v.c
					if not doHook("boxclick1",c=c,v=v,event=event):
						tree.OnBoxClick(v)
					doHook("boxclick2",c=c,v=v,event=event)
				except:
					es_event_exception("boxclick")
			#@nonl
			#@-node:<< define onBoxClickCallback >>
			#@nl
			id1 = self.canvas.tag_bind(id, "<1>", onBoxClickCallback)
		id2 = self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
		
		# Remember the bindings so deleteBindings can delete them.
		self.tagBindings.append((id,id1,"<1>"),)
		self.tagBindings.append((id,id2,"<Double-1>"),)
	#@nonl
	#@-node:drawBox (tag_bind)
	#@+node:drawIcon (tag_bind)
	def drawIcon(self,v,x=None,y=None):
		
		"""Draws icon for v at x,y, or at v.iconx,v.icony if x,y = None,None"""
	
		tree = self
		
		if x is None and y is None:
			try:
				x,y = v.iconx, v.icony
			except:
				# Inject the ivars.
				x,y = v.iconx, v.icony = 0,0
		else:
			# Inject the ivars.
			v.iconx, v.icony = x,y
	
		y += 2 # draw icon at y + 2
	
		# Always recompute icon.
		val = v.iconVal = v.computeIcon()
		assert(0 <= val <= 15)
		
		# Compute the image name
		imagename = "box"
		if val < 10: imagename += "0"
		imagename += `val`
	
		# Get the image
		image = self.getIconImage(imagename + ".GIF")
		id = self.canvas.create_image(x,y,anchor="nw",image=image)
		self.icon_id_dict[id] = v # Remember which vnode belongs to the icon.
		
		if 1: # use vnode callbacks.
			id1 = self.canvas.tag_bind(id,"<1>",v.OnIconClick)
			id2 = self.canvas.tag_bind(id,"<Double-1>",v.OnIconDoubleClick)
			id3 = self.canvas.tag_bind(id,"<3>",v.OnIconRightClick)
		else:
			#@		<< define icon click callbacks >>
			#@+node:<< define icon click callbacks >>
			def onIconClickCallback(event,tree=tree,v=v):
				try:
					c = v.c
					if not doHook("iconclick1",c=c,v=v,event=event):
						tree.OnIconClick(v,event)
					doHook("iconclick2",c=c,v=v,event=event)
				except:
					es_event_exception("iconclick")
					
			def onIconDoubleClickCallback(event,tree=tree,v=v):
				try:
					c = v.c
					if not doHook("icondclick1",c=c,v=v,event=event):
						tree.OnIconDoubleClick(self)
					doHook("icondclick2",c=c,v=v,event=event)
				except:
					es_event_exception("icondclick")
				
			def onIconRightClickCallback(event,tree=tree,v=v):
				try:
					c = v.c
					if not doHook("iconrclick1",c=c,v=v,event=event):
						tree.OnIconRightClick(v,event)
					doHook("iconrclick2",c=c,v=v,event=event)
				except:
					es_event_exception("iconrclick")
			#@-node:<< define icon click callbacks >>
			#@nl
			id1 = self.canvas.tag_bind(id,"<1>",onIconClickCallback)
			id2 = self.canvas.tag_bind(id,"<Double-1>",onIconDoubleClickCallback)
			id3 = self.canvas.tag_bind(id,"<3>",onIconRightClickCallback)
		
		# Remember the bindings so deleteBindings can delete them.
		self.tagBindings.append((id,id1,"<1>"),)
		self.tagBindings.append((id,id2,"<Double-1>"),)
		self.tagBindings.append((id,id3,"<3>"),)
	
		return 0 # dummy icon height
	#@nonl
	#@-node:drawIcon (tag_bind)
	#@+node:drawNode & force_draw_node
	def drawNode(self,v,x,y):
	
		"""Draw horizontal line from vertical line to icon"""
	
		self.canvas.create_line(x, y+7, x+box_width, y+7,tag="lines",fill="gray50") # stipple="gray25")
	
		if self.inVisibleArea(y):
			return self.force_draw_node(v,x,y)
		else:
			return self.line_height
		
	def force_draw_node(self,v,x,y):
	
		self.allocatedNodes += 1
		if v.firstChild():
			self.drawBox(v,x,y)
		icon_height = self.drawIcon(v,x+box_width,y)
		text_height = self.drawText(v,x+box_width+icon_width,y)
		return max(icon_height, text_height)
	#@nonl
	#@-node:drawNode & force_draw_node
	#@+node:drawText (bind)
	# draws text for v at x,y
	
	def drawText(self,v,x,y):
		
		tree = self
		x += text_indent
	
		t = Tkinter.Text(self.canvas,
			font=self.font,bd=0,relief="flat",width=self.headWidth(v),height=1)
		self.edit_text_dict[v] = t # Remember which text widget belongs to v.
		
		# Remember the widget so deleteBindings can delete it.
		self.widgets.append(t) # Fixes a _huge_ memory leak.
	
		t.insert("end", v.headString())
		#@	<< configure the text depending on state >>
		#@+node:<< configure the text depending on state >>
		if v == self.currentVnode():
			if v == self.editVnode():
				self.setNormalLabelState(v)
			else:
				self.setDisabledLabelState(v) # selected, disabled
		else:
			self.setUnselectedLabelState(v) # unselected
		#@nonl
		#@-node:<< configure the text depending on state >>
		#@nl
	
		if 1: # Use vnode callbacks.
			id1 = t.bind("<1>",v.OnHeadlineClick)
			id2 = t.bind("<3>",v.OnHeadlineRightClick)
		else:
			#@		<< define the headline click callbacks >>
			#@+node:<< define the headline click callbacks >>
			def onHeadlineClickCallback(event,tree=tree,v=v):
				try:
					c = v.c
					if not doHook("headclick1",c=c,v=v,event=event):
						tree.OnActivate(v)
					doHook("headclick2",c=c,v=v,event=event)
				except:
					es_event_exception("headclick")
				
			def onHeadlineRightClickCallback(event,tree=tree,v=v):
				try:
					c = v.c
					if not doHook("headrclick1",c=c,v=v,event=event):
						tree.OnActivate(v)
						tree.OnPopup(v,event)
					doHook("headrclick2",c=c,v=v,event=event)
				except:
					es_event_exception("headrclick")
			#@nonl
			#@-node:<< define the headline click callbacks >>
			#@nl
			id1 = t.bind("<1>",onHeadlineClickCallback)
			id2 = t.bind("<3>",onHeadlineRightClickCallback)
		if 0: # 6/15/02: Bill Drissel objects to this binding.
			t.bind("<Double-1>", v.OnBoxClick)
		id3 = t.bind("<Key>", v.OnHeadlineKey)
		id4 = t.bind("<Control-t>",self.OnControlT)
			# 10/16/02: Stamp out the erroneous control-t binding.
			
		# Remember the bindings so deleteBindings can delete them.
		self.bindings.append((t,id1,"<1>"),)
		self.bindings.append((t,id2,"<3>"),)
		self.bindings.append((t,id3,"<Key>"),)
		self.bindings.append((t,id4,"<Control-t>"),)
	
		id = self.canvas.create_window(x,y,anchor="nw",window=t)
		self.canvas.tag_lower(id)
	
		return self.line_height
	#@nonl
	#@-node:drawText (bind)
	#@+node:drawTopTree
	def drawTopTree (self):
		
		"""Draws the top-level tree, taking into account the hoist state."""
		
		c = self.c
		
		if c.hoistStack:
			v = c.hoistStack[-1]
			self.drawTree(v,root_left,root_top,0,0,hoistFlag=true)
		else:
			self.drawTree(self.rootVnode(),root_left,root_top,0,0)
	#@nonl
	#@-node:drawTopTree
	#@+node:drawTree
	def drawTree(self,v,x,y,h,level,hoistFlag=false):
		
		yfirst = ylast = y
		if level==0: yfirst += 10
		while v:
			# trace(`x` + ", " + `y` + ", " + `v`)
			h = self.drawNode(v,x,y)
			y += h ; ylast = y
			if v.isExpanded() and v.firstChild():
				y = self.drawTree(v.firstChild(),x+child_indent,y,h,level+1)
			if hoistFlag:
				v = None
			else:
				v = v.next()
		#@	<< draw vertical line >>
		#@+node:<< draw vertical line >>
		id = self.canvas.create_line(
			x, yfirst-hline_y+4,
			x, ylast+hline_y-h,
			fill="gray50", # stipple="gray50"
			tag="lines")
		
		self.canvas.tag_lower(id)
		#@nonl
		#@-node:<< draw vertical line >>
		#@nl
		return y
	#@nonl
	#@-node:drawTree
	#@+node:inVisibleArea & inExpandedVisibleArea
	def inVisibleArea (self,y1):
		
		if self.allocateOnlyVisibleNodes:
			if self.visibleArea:
				vis1,vis2 = self.visibleArea
				y2 = y1 + self.line_height
				return y2 >= vis1 and y1 <= vis2
			else: return false
		else:
			return true # This forces all nodes to be allocated on all redraws.
			
	def inExpandedVisibleArea (self,y1):
		
		if self.expandedVisibleArea:
			vis1,vis2 = self.expandedVisibleArea
			y2 = y1 + self.line_height
			return y2 >= vis1 and y1 <= vis2
		else:
			return false
	#@nonl
	#@-node:inVisibleArea & inExpandedVisibleArea
	#@+node:lastVisible
	# Returns the last visible node of the screen.
	
	def lastVisible (self):
	
		v = self.rootVnode()
		while v:
			last = v
			if v.firstChild():
				if v.isExpanded():
					v = v.firstChild()
				else:
					v = v.nodeAfterTree()
			else:
				v = v.threadNext()
		return last
	#@nonl
	#@-node:lastVisible
	#@+node:tree.getIconImage
	def getIconImage (self, name):
	
		# Return the image from the cache if possible.
		if self.iconimages.has_key(name):
			return self.iconimages[name]
			
		try:
			fullname = os_path_join(app.loadDir,"..","Icons",name)
			fullname = os_path_normpath(fullname)
			image = Tkinter.PhotoImage(master=self.canvas, file=fullname)
			self.iconimages[name] = image
			return image
		except:
			es("Exception loading: " + fullname)
			es_exception()
			return None
	#@nonl
	#@-node:tree.getIconImage
	#@+node:tree.idle_scrollTo
	def idle_scrollTo(self,v=None):
	
		"""Scrolls the canvas so that v is in view.
		
		This is done at idle time after a redraw so that treeBar.get() will return proper values."""
	
		frame = self.c.frame
		last = self.lastVisible()
		nextToLast = last.visBack()
		# print 'v,last',`v`,`last`
		if v == None:
			v = self.currentVnode()
		h1 = self.yoffset(v)
		h2 = self.yoffset(last)
		if nextToLast: # 2/2/03: compute approximate line height.
			lineHeight = h2 - self.yoffset(nextToLast)
		else:
			lineHeight = 20 # A reasonable default.
		# Compute the fractions to scroll down/up.
		lo, hi = frame.treeBar.get()
		if h2 > 0.1:
			frac = float(h1)/float(h2) # For scrolling down.
			frac2 = float(h1+lineHeight/2)/float(h2) # For scrolling up.
			frac2 = frac2 - (hi - lo)
		else:
			frac = frac2 = 0.0 # probably any value would work here.
		# 2/2/03: new logic for scrolling up.
		frac =  max(min(frac,1.0),0.0)
		frac2 = max(min(frac2,1.0),0.0)
	
		if frac <= lo:
			if self.prevMoveToFrac != frac:
				self.prevMoveToFrac = frac
				self.canvas.yview("moveto",frac)
		elif frac2 + (hi - lo) >= hi:
			if self.prevMoveToFrac != frac2:
				self.prevMoveToFrac = frac2
				self.canvas.yview("moveto",frac2)
				
		if self.allocateOnlyVisibleNodes:
			self.canvas.after_idle(self.idle_second_redraw)
	
		# print "%3d %3d %1.3f %1.3f %1.3f %1.3f" % (h1,h2,frac,frac2,lo,hi)
	#@-node:tree.idle_scrollTo
	#@+node:tree.numberOfVisibleNodes
	def numberOfVisibleNodes(self):
		
		n = 0 ; v = self.rootVnode()
		while v:
			n += 1
			v = v.visNext()
		return n
	#@nonl
	#@-node:tree.numberOfVisibleNodes
	#@+node:tree.yoffset
	#@+at 
	#@nonl
	# We can't just return icony because the tree hasn't been redrawn yet.  
	# For the same reason we can't rely on any TK canvas methods here.
	#@-at
	#@@c
	
	def yoffset(self, v1):
	
		# if not v1.isVisible(): print "yoffset not visible:", `v1`
		root = self.rootVnode()
		h, flag = self.yoffsetTree(root,v1)
		# flag can be false during initialization.
		# if not flag: print "yoffset fails:", h, `v1`
		return h
	
	# Returns the visible height of the tree and all sibling trees, stopping at v1
	
	def yoffsetTree(self,v,v1):
	
		h = 0
		while v:
			# print "yoffsetTree:", `v`
			if v == v1:
				return h, true
			h += self.line_height
			child = v.firstChild()
			if v.isExpanded() and child:
				h2, flag = self.yoffsetTree(child,v1)
				h += h2
				if flag: return h, true
			v = v.next()
		return h, false
	#@nonl
	#@-node:tree.yoffset
	#@+node:tree.getFont,setFont,setFontFromConfig
	def getFont (self):
	
		return self.font
			
	# Called by leoFontPanel.
	def setFont (self, font=None, fontName=None):
		
		if fontName:
			self.fontName = fontName
			self.font = tkFont.Font(font=fontName)
		else:
			self.fontName = None
			self.font = font
			
		self.setLineHeight(self.font)
		
	# Called by ctor and when config params are reloaded.
	def setFontFromConfig (self):
	
		font = app.config.getFontFromParams(
			"headline_text_font_family", "headline_text_font_size",
			"headline_text_font_slant",  "headline_text_font_weight")
	
		self.setFont(font)
	#@nonl
	#@-node:tree.getFont,setFont,setFontFromConfig
	#@+node:headWidth
	def headWidth(self,v):
	
		"""Returns the proper width of the entry widget for the headline."""
	
		return max(10,5 + len(v.headString()))
	#@nonl
	#@-node:headWidth
	#@+node:setLineHeight
	def setLineHeight (self,font):
		
		try:
			metrics = font.metrics()
			linespace = metrics ["linespace"]
			self.line_height = linespace + 5 # Same as before for the default font on Windows.
			# print metrics
		except:
			self.line_height = line_height # was 17 + 2
			es("exception setting outline line height")
			es_exception()
	#@nonl
	#@-node:setLineHeight
	#@+node:Event handers (tree)
	#@+at 
	#@nonl
	# Important note: most hooks are created in the vnode callback routines, 
	# _not_ here.
	#@-at
	#@-node:Event handers (tree)
	#@+node:OnActivate
	def OnActivate (self,v,event=None):
	
		try:
			c = self.c
			#@		<< activate this window >>
			#@+node:<< activate this window >>
			c = self.c ; gui = app.gui
			
			if v == self.currentVnode():
				if self.active:
					self.editLabel(v)
				else:
					self.undimEditLabel()
					gui.set_focus(c,self.canvas) # Essential for proper editing.
			else:
				self.select(v)
				if v.t.insertSpot != None: # 9/1/02
					c.frame.bodyCtrl.mark_set("insert",v.t.insertSpot)
					c.frame.bodyCtrl.see(v.t.insertSpot)
				else:
					c.frame.bodyCtrl.mark_set("insert","1.0")
				gui.set_focus(c,c.frame.bodyCtrl)
			
			self.active = true
			#@nonl
			#@-node:<< activate this window >>
			#@nl
		except:
			es_event_exception("activate tree")
	#@nonl
	#@-node:OnActivate
	#@+node:OnBoxClick
	# Called on click in box and double-click in headline.
	
	def OnBoxClick (self,v):
	
		# Note: "boxclick" hooks handled by vnode callback routine.
		c = self.c ; gui = app.gui
	
		if v.isExpanded():
			v.contract()
		else:
			v.expand()
	
		self.active = true
		self.select(v)
		gui.set_focus(c,c.frame.bodyCtrl) # 7/12/03
		self.redraw()
	#@nonl
	#@-node:OnBoxClick
	#@+node:tree.OnDeactivate (caused double-click problem)
	def OnDeactivate (self,event=None):
		
		"""Deactivate the tree pane, dimming any headline being edited."""
	
		tree = self ; c = self.c
		focus = app.gui.get_focus(c.frame)
	
		# Bug fix: 7/13/03: Only do this as needed.
		# Doing this on every click would interfere with the double-clicking.
		if not c.frame.log.hasFocus() and focus != c.frame.bodyCtrl:
			try:
				# trace(focus)
				tree.endEditLabel()
				tree.dimEditLabel()
			except:
				es_event_exception("deactivate tree")
	#@nonl
	#@-node:tree.OnDeactivate (caused double-click problem)
	#@+node:tree.findVnodeWithIconId
	def findVnodeWithIconId (self,id):
		
		# Due to an old bug, id may be a tuple.
		try:
			return self.icon_id_dict.get(id[0])
		except:
			return self.icon_id_dict.get(id)
	#@-node:tree.findVnodeWithIconId
	#@+node:tree.OnContinueDrag
	def OnContinueDrag(self,v,event):
	
		try:
			#@		<< continue dragging >>
			#@+node:<< continue dragging >>
			# trace(`v`)
			assert(v == self.drag_v)
			
			canvas = self.canvas
			frame = self.c.frame
			
			if event:
				x,y = event.x,event.y
			else:
				x,y = frame.top.winfo_pointerx(),frame.top.winfo_pointery()
				if x == -1 or y == -1: return # Stop the scrolling if we go outside the entire window.
			
			if 0: # no longer used.
				canvas_x = canvas.canvasx(x)
				canvas_y = canvas.canvasy(y)
				id = self.canvas.find_closest(canvas_x,canvas_y)
			
			# OnEndDrag() halts the scrolling by clearing self.drag_id when the mouse button goes up.
			if self.drag_id: # This gets cleared by OnEndDrag()
				#@	<< scroll the canvas as needed >>
				#@+node:<< scroll the canvas as needed >>
				# Scroll the screen up or down one line if the cursor (y) is outside the canvas.
				h = canvas.winfo_height()
				if y < 0 or y > h:
					lo, hi = frame.treeBar.get()
					n = self.savedNumberOfVisibleNodes
					line_frac = 1.0 / float(n)
					frac = choose(y < 0, lo - line_frac, lo + line_frac)
					frac = min(frac,1.0)
					frac = max(frac,0.0)
					# es("lo,hi,frac:" + `lo` + " " + `hi` + " " + `frac`)
					canvas.yview("moveto", frac)
					
					# Queue up another event to keep scrolling while the cursor is outside the canvas.
					lo, hi = frame.treeBar.get()
					if (y < 0 and lo > 0.1) or (y > h and hi < 0.9):
						canvas.after_idle(self.OnContinueDrag,v,None) # Don't propagate the event.
				#@nonl
				#@-node:<< scroll the canvas as needed >>
				#@nl
			#@nonl
			#@-node:<< continue dragging >>
			#@nl
		except:
			es_event_exception("continue drag")
	#@nonl
	#@-node:tree.OnContinueDrag
	#@+node:tree.OnCtontrolT
	# This works around an apparent Tk bug.
	
	def OnControlT (self,event=None):
	
		# If we don't inhibit further processing the Tx.Text widget switches characters!
		return "break"
	#@nonl
	#@-node:tree.OnCtontrolT
	#@+node:tree.OnDrag
	# This precomputes numberOfVisibleNodes(), a significant optimization.
	# We also indicate where findVnodeWithIconId() should start looking for tree id's.
	
	def OnDrag(self,v,event):
	
		# Note: "drag" hooks handled by vnode callback routine.
		# trace(event)
		
		c = self.c
		assert(v == self.drag_v)
	
		if not event:
			return
	
		if not self.dragging():
			windowPref = app.config.getBoolWindowPref
			# Only do this once: greatly speeds drags.
			self.savedNumberOfVisibleNodes = self.numberOfVisibleNodes()
			self.setDragging(true)
			if windowPref("allow_clone_drags"):
				self.controlDrag = c.frame.controlKeyIsDown
				if windowPref("look_for_control_drag_on_mouse_down"):
					if windowPref("enable_drag_messages"):
						if self.controlDrag:
							es("dragged node will be cloned")
						else:
							es("dragged node will be moved")
			else: self.controlDrag = false
			self.canvas['cursor'] = "hand2" # "center_ptr"
	
		self.OnContinueDrag(v,event)
	#@nonl
	#@-node:tree.OnDrag
	#@+node:tree.OnEndDrag
	def OnEndDrag(self,v,event):
		
		"""Tree end-of-drag handler called from vnode event handler."""
		
		# trace(v)
		
		# 7/10/03: Make sure we are still dragging.
		if not self.drag_v:
			return
	
		assert(v == self.drag_v)
		c = self.c ; canvas = self.canvas ; config = app.config
	
		if event:
			#@		<< set vdrag, childFlag >>
			#@+node:<< set vdrag, childFlag >>
			x,y = event.x,event.y
			canvas_x = canvas.canvasx(x)
			canvas_y = canvas.canvasy(y)
			
			id = self.canvas.find_closest(canvas_x,canvas_y)
			vdrag = self.findVnodeWithIconId(id)
			childFlag = vdrag and vdrag.hasChildren() and vdrag.isExpanded()
			#@nonl
			#@-node:<< set vdrag, childFlag >>
			#@nl
			if config.getBoolWindowPref("allow_clone_drags"):
				if not config.getBoolWindowPref("look_for_control_drag_on_mouse_down"):
					self.controlDrag = c.frame.controlKeyIsDown
	
			if vdrag and vdrag != v:
				if self.controlDrag: # Clone v and move the clone.
					if childFlag:
						c.dragCloneToNthChildOf(v,vdrag,0)
					else:
						c.dragCloneAfter(v,vdrag)
				else: # Just drag v.
					if childFlag:
						c.dragToNthChildOf(v,vdrag,0)
					else:
						c.dragAfter(v,vdrag)
			else:
				if v and self.dragging():
					pass # es("not dragged: " + v.headString())
				if 0: # Don't undo the scrolling we just did!
					self.idle_scrollTo(v)
		
		# 1216/02: Reset the old cursor by brute force.
		self.canvas['cursor'] = "arrow"
	
		if self.drag_id:
			canvas.tag_unbind(self.drag_id , "<B1-Motion>")
			canvas.tag_unbind(self.drag_id , "<Any-ButtonRelease-1>")
			self.drag_id = None
			
		self.setDragging(false)
		self.drag_v = None
	#@nonl
	#@-node:tree.OnEndDrag
	#@+node:headline key handlers (tree)
	#@+at 
	#@nonl
	# The <Key> event generates the event before the headline text is 
	# changed(!), so we register an idle-event handler to do the work later.
	#@-at
	#@@c
	
	#@+others
	#@+node:onHeadChanged
	def onHeadChanged (self,v):
		
		"""Handle a change to headline text."""
	
		self.c.frame.bodyCtrl.after_idle(self.idle_head_key,v)
	
	
	#@-node:onHeadChanged
	#@+node:OnHeadlineKey
	def OnHeadlineKey (self,v,event):
		
		"""Handle a key event in a headline."""
	
		ch = event.char
		self.c.frame.bodyCtrl.after_idle(self.idle_head_key,v,ch)
	
	#@-node:OnHeadlineKey
	#@+node:idle_head_key
	def idle_head_key (self,v,ch=None):
		
		"""Update headline text at idle time."""
	
		c = self.c
		if not v or not v.edit_text() or v != c.currentVnode():
			return "break"
		if doHook("headkey1",c=c,v=v,ch=ch):
			return "break" # The hook claims to have handled the event.
	
		#@	<< set s to the widget text >>
		#@+node:<< set s to the widget text >>
		s = v.edit_text().get("1.0","end")
		s = toUnicode(s,app.tkEncoding) # 2/25/03
		
		if not s:
			s = u""
		s = s.replace('\n','')
		s = s.replace('\r','')
		# trace(`s`)
		#@-node:<< set s to the widget text >>
		#@nl
		#@	<< set head to vnode text >>
		#@+node:<< set head to vnode text >>
		head = v.headString()
		if head == None:
			head = u""
		head = toUnicode(head,"utf-8")
		#@-node:<< set head to vnode text >>
		#@nl
		changed = s != head
		done = ch and (ch == '\r' or ch == '\n')
		if not changed and not done:
			return "break"
		if changed:
			c.undoer.setUndoParams("Change Headline",v,newText=s,oldText=head)
		index = v.edit_text().index("insert")
		if changed:
			#@		<< update v and all nodes joined to v >>
			#@+node:<< update v and all nodes joined to v >>
			c.beginUpdate()
			
			# Update changed bit.
			if not c.changed:
				c.setChanged(true)
			
			# Update all dirty bits.
			v.setDirty()
			
			# Update v.
			v.initHeadString(s)
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("end",s)
			v.edit_text().mark_set("insert",index)
			
			# Update all joined nodes.
			for v2 in v.t.joinList:
				if v2 != v:
					v2.initHeadString(s)
					if v2.edit_text(): # v2 may not be visible
						v2.edit_text().delete("1.0","end")
						v2.edit_text().insert("end",s)
			
			c.endUpdate(false) # do not redraw now.
			#@nonl
			#@-node:<< update v and all nodes joined to v >>
			#@nl
		#@	<< reconfigure v and all nodes joined to v >>
		#@+node:<< reconfigure v and all nodes joined to v >>
		# Reconfigure v's headline.
		if done:
			self.setDisabledLabelState(v)
		
		v.edit_text().configure(width=self.headWidth(v))
		
		# Reconfigure all joined headlines.
		for v2 in v.t.joinList:
			if v2 != v:
				if v2.edit_text(): # v2 may not be visible
					v2.edit_text().configure(width=self.headWidth(v2))
		#@nonl
		#@-node:<< reconfigure v and all nodes joined to v >>
		#@nl
		#@	<< update the screen >>
		#@+node:<< update the screen >>
		if done:
			c.beginUpdate()
			self.endEditLabel()
			c.endUpdate()
		
		elif changed:
			# update v immediately.  Joined nodes are redrawn later by endEditLabel.
			# Redrawing the whole screen now messes up the cursor in the headline.
			self.drawIcon(v) # just redraw the icon.
		#@nonl
		#@-node:<< update the screen >>
		#@nl
	
		doHook("headkey2",c=c,v=v,ch=ch)
		return "break"
	#@nonl
	#@-node:idle_head_key
	#@-others
	#@nonl
	#@-node:headline key handlers (tree)
	#@+node:tree.OnIconClick & OnIconRightClick
	def OnIconClick (self,v,event):
	
		tree = self ; canvas = tree.canvas
		if event:
			canvas_x = canvas.canvasx(event.x)
			canvas_y = canvas.canvasy(event.y)
			id = canvas.find_closest(canvas_x,canvas_y)
			if id != None:
				try: id = id[0]
				except: pass
				self.drag_v = v
				self.drag_id = id
				if 1: # Use vnode callbacks.
					id4 = canvas.tag_bind(id,"<B1-Motion>", v.OnDrag)
					id5 = canvas.tag_bind(id,"<Any-ButtonRelease-1>", v.OnEndDrag)
				else:
					#@				<< define drag callbacks >>
					#@+node:<< define drag callbacks >>
					def onDragCallback(event,tree=tree,v=v):
						try:
							c = v.c
							if tree.dragging():
								if not doHook("dragging1",c=c,v=v,event=event):
									tree.OnDrag(v,event)
								doHook("dragging2",c=c,v=v,event=event)
							else:
								if not doHook("drag1",c=c,v=v,event=event):
									tree.OnDrag(v,event)
								doHook("drag2",c=c,v=v,event=event)
						except:
							es_event_exception("drag")
							
					def onEndDragCallback(event,tree=tree,v=v):
						try:
							c = v.c
							if not doHook("enddrag1",c=c,v=v,event=event):
								tree.OnEndDrag(v,event)
							doHook("enddrag2",c=c,v=v,event=event)
						except:
							es_event_exception("enddrag")
							
							
					#@-node:<< define drag callbacks >>
					#@nl
					id4 = canvas.tag_bind(id,"<B1-Motion>", onDragCallback)
					id5 = canvas.tag_bind(id,"<Any-ButtonRelease-1>", onEndDragCallback)
				# Remember the bindings so deleteBindings can delete them.
				self.tagBindings.append((id,id4,"<B1-Motion>"),)
				self.tagBindings.append((id,id5,"<Any-ButtonRelease-1>"),)
		tree.select(v)
		
	def OnIconRightClick (self,v,event):
	
		self.select(v)
	#@nonl
	#@-node:tree.OnIconClick & OnIconRightClick
	#@+node:tree.OnIconDoubleClick (@url)
	def OnIconDoubleClick (self,v,event=None):
	
		# Note: "icondclick" hooks handled by vnode callback routine.
	
		c = self.c
		s = v.headString().strip()
		if match_word(s,0,"@url"):
			if not doHook("@url1",c=c,v=v):
				url = s[4:].strip()
				#@			<< stop the url after any whitespace >>
				#@+node:<< stop the url after any whitespace  >>
				# For safety, the URL string should end at the first whitespace.
				
				url = url.replace('\t',' ')
				i = url.find(' ')
				if i > -1:
					if 0: # No need for a warning.  Assume everything else is a comment.
						es("ignoring characters after space in url:"+url[i:])
						es("use %20 instead of spaces")
					url = url[:i]
				#@-node:<< stop the url after any whitespace  >>
				#@nl
				#@			<< check the url; return if bad >>
				#@+node:<< check the url; return if bad >>
				if not url or len(url) == 0:
					es("no url following @url")
					return
					
				#@+at 
				#@nonl
				# A valid url is (according to D.T.Hein):
				# 
				# 3 or more lowercase alphas, followed by,
				# one ':', followed by,
				# one or more of: (excludes !"#;<>[\]^`|)
				#   $%&'()*+,-./0-9:=?@A-Z_a-z{}~
				# followed by one of: (same as above, except no minus sign or 
				# comma).
				#   $%&'()*+/0-9:=?@A-Z_a-z}~
				#@-at
				#@@c
				
				urlPattern = "[a-z]{3,}:[\$-:=?-Z_a-z{}~]+[\$-+\/-:=?-Z_a-z}~]"
				import re
				# 4/21/03: Add http:// if required.
				if not re.match('^([a-z]{3,}:)',url):
					url = 'http://' + url
				if not re.match(urlPattern,url):
					es("invalid url: "+url)
					return
				#@-node:<< check the url; return if bad >>
				#@nl
				#@			<< pass the url to the web browser >>
				#@+node:<< pass the url to the web browser >>
				#@+at 
				#@nonl
				# Most browsers should handle the following urls:
				#   ftp://ftp.uu.net/public/whatever.
				#   http://localhost/MySiteUnderDevelopment/index.html
				#   file:///home/me/todolist.html
				#@-at
				#@@c
				
				try:
					import os
					import webbrowser
					os.chdir(app.loadDir)
					# print "url:",url
					webbrowser.open(url)
				except:
					es("exception opening " + url)
					es_exception()
				#@nonl
				#@-node:<< pass the url to the web browser >>
				#@nl
			doHook("@url2",c=c,v=v)
	#@nonl
	#@-node:tree.OnIconDoubleClick (@url)
	#@+node:tree.OnPopup & allies
	def OnPopup (self,v,event):
		
		"""Handle right-clicks in the outline."""
		
		# Note: "headrclick" hooks handled by vnode callback routine.
	
		if event != None:
			c = self.c
			if not doHook("create-popup-menu",c=c,v=v,event=event):
				self.createPopupMenu(event)
			if not doHook("enable-popup-menu-items",c=c,v=v,event=event):
				self.enablePopupMenuItems(v,event)
			if not doHook("show-popup-menu",c=c,v=v,event=event):
				self.showPopupMenu(event)
	
		return "break"
	#@nonl
	#@-node:tree.OnPopup & allies
	#@+node:OnPopupFocusLost
	#@+at 
	#@nonl
	# On Linux we must do something special to make the popup menu "unpost" if 
	# the mouse is clicked elsewhere.  So we have to catch the <FocusOut> 
	# event and explicitly unpost.  In order to process the <FocusOut> event, 
	# we need to be able to find the reference to the popup window again, so 
	# this needs to be an attribute of the tree object; hence, 
	# "self.popupMenu".
	# 
	# Aside: though Tk tries to be muli-platform, the interaction with 
	# different window managers does cause small differences that will need to 
	# be compensated by system specific application code. :-(
	#@-at
	#@@c
	
	# 20-SEP-2002 DTHEIN: This event handler is only needed for Linux.
	
	def OnPopupFocusLost(self,event=None):
	
		self.popupMenu.unpost()
		
	#@-node:OnPopupFocusLost
	#@+node:createPopupMenu
	def createPopupMenu (self,event):
		
		c = self.c ; frame = c.frame
		
		# If we are going to recreate it, we had better destroy it.
		if self.popupMenu:
			self.popupMenu.destroy()
			self.popupMenu = None
		
		self.popupMenu = menu = Tkinter.Menu(app.root, tearoff=0)
		
		# Add the Open With entries if they exist.
		if app.openWithTable:
			frame.menu.createMenuEntries(menu,app.openWithTable,openWith=1)
			table = (("-",None,None),)
			frame.menu.createMenuEntries(menu,table)
			
		#@	<< Create the menu table >>
		#@+node:<< Create the menu table >>
		table = (
			("&Read @file Nodes",None,c.readAtFileNodes),
			("&Write @file Nodes",None,c.fileCommands.writeAtFileNodes),
			("-",None,None),
			("&Tangle","Shift+Ctrl+T",c.tangle),
			("&Untangle","Shift+Ctrl+U",c.untangle),
			("-",None,None),
			("Toggle Angle &Brackets","Ctrl+B",c.toggleAngleBrackets),
			("-",None,None),
			("Cut Node","Shift+Ctrl+X",c.cutOutline),
			("Copy Node","Shift+Ctrl+C",c.copyOutline),
			("&Paste Node","Shift+Ctrl+V",c.pasteOutline),
			("&Delete Node","Shift+Ctrl+BkSp",c.deleteOutline),
			("-",None,None),
			("&Insert Node","Ctrl+I",c.insertHeadline),
			("&Clone Node","Ctrl+`",c.clone),
			("Sort C&hildren",None,c.sortChildren),
			("&Sort Siblings","Alt-A",c.sortSiblings),
			("-",None,None),
			("Contract Parent","Alt+0",c.contractParent))
		#@nonl
		#@-node:<< Create the menu table >>
		#@nl
		frame.menu.createMenuEntries(menu,table)
	#@nonl
	#@-node:createPopupMenu
	#@+node:enablePopupMenuItems
	def enablePopupMenuItems (self,v,event):
		
		"""Enable and disable items in the popup menu."""
		
		c = self.c ; menu = self.popupMenu
	
		#@	<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		#@+node:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		isAtFile = false ; isAtRoot = false
		v2 = v ; next = v.nodeAfterTree()
		
		while (not isAtFile or not isAtRoot) and v2 != None and v2 != next:
			if (
				v2.isAtFileNode() or
				v.isAtRawFileNode() or
				v.isAtSilentFileNode() or
				v.isAtNoSentinelsFileNode()):
				isAtFile = true
		
			isRoot, junk = is_special(v2.bodyString(),0,"@root")
			if isRoot:
				isAtRoot = true
			v2 = v2.threadNext()
		#@nonl
		#@-node:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		#@nl
		isAtFile = choose(isAtFile,1,0)
		isAtRoot = choose(isAtRoot,1,0)
		canContract = v.parent() != None
		canContract = choose(canContract,1,0)
		
		enable = self.frame.menu.enableMenu
		
		for name in ("Read @file Nodes", "Write @file Nodes"):
			enable(menu,name,isAtFile)
		for name in ("Tangle", "Untangle"):
			enable(menu,name,isAtRoot)
	
		enable(menu,"Cut Node",c.canCutOutline())
		enable(menu,"Delete Node",c.canDeleteHeadline())
		enable(menu,"Paste Node",c.canPasteOutline())
		enable(menu,"Sort Children",c.canSortChildren())
		enable(menu,"Sort Siblings",c.canSortSiblings())
		enable(menu,"Contract Parent",c.canContractParent())
	#@nonl
	#@-node:enablePopupMenuItems
	#@+node:showPopupMenu
	def showPopupMenu (self,event):
		
		"""Show a popup menu."""
		
		c = self.c ; menu = self.popupMenu ; gui = app.gui
	
		if sys.platform == "linux2": # 20-SEP-2002 DTHEIN: not needed for Windows
			menu.bind("<FocusOut>",self.OnPopupFocusLost)
		
		menu.post(event.x_root, event.y_root)
	
		# Make certain we have focus so we know when we lose it.
		# I think this is OK for all OSes.
		gui.set_focus(c,menu)
	#@nonl
	#@-node:showPopupMenu
	#@+node:allocateNodes
	def allocateNodes(self,where,lines):
		
		"""Allocate Tk widgets in nodes that will become visible as the result of an upcoming scroll"""
		
		assert(where in ("above","below"))
	
		# print "allocateNodes: %d lines %s visible area" % (lines,where)
		
		# Expand the visible area: a little extra delta is safer.
		delta = lines * (self.line_height + 4)
		y1,y2 = self.visibleArea
	
		if where == "below":
			y2 += delta
		else:
			y1 = max(0.0,y1-delta)
	
		self.expandedVisibleArea=y1,y2
		# print "expandedArea:   %5.1f %5.1f" % (y1,y2)
		
		# Allocate all nodes in expanded visible area.
		self.updatedNodeCount = 0
		self.updateTree(self.rootVnode(),root_left,root_top,0,0)
		# if self.updatedNodeCount: print "updatedNodeCount:", self.updatedNodeCount
	#@-node:allocateNodes
	#@+node:allocateNodesBeforeScrolling
	def allocateNodesBeforeScrolling (self, args):
		
		"""Calculate the nodes that will become visible as the result of an upcoming scroll.
	
		args is the tuple passed to the Tk.Canvas.yview method"""
	
		if not self.allocateOnlyVisibleNodes: return
	
		# print "allocateNodesBeforeScrolling:",self.redrawCount,`args`
	
		assert(self.visibleArea)
		assert(len(args)==2 or len(args)==3)
		kind = args[0] ; n = args[1]
		lines = 2 # Update by 2 lines to account for rounding.
		if len(args) == 2:
			assert(kind=="moveto")
			frac1,frac2 = args
			if float(n) != frac1:
				where = choose(n<frac1,"above","below")
				self.allocateNodes(where=where,lines=lines)
		else:
			assert(kind=="scroll")
			linesPerPage = self.canvas.winfo_height()/self.line_height + 2
			n = int(n) ; assert(abs(n)==1)
			where = choose(n == 1,"below","above")
			lines = choose(args[2] == "pages",linesPerPage,lines)
			self.allocateNodes(where=where,lines=lines)
	#@nonl
	#@-node:allocateNodesBeforeScrolling
	#@+node:updateNode
	def updateNode (self,v,x,y):
		
		"""Draw a node that may have become visible as a result of a scrolling operation"""
	
		if self.inExpandedVisibleArea(y):
			# This check is a major optimization.
			if not v.edit_text():
				return self.force_draw_node(v,x,y)
			else:
				return self.line_height
	
		return self.line_height
	#@nonl
	#@-node:updateNode
	#@+node:setVisibleAreaToFullCanvas
	def setVisibleAreaToFullCanvas(self):
		
		if self.visibleArea:
			y1,y2 = self.visibleArea
			y2 = max(y2,y1 + self.canvas.winfo_height())
			self.visibleArea = y1,y2
	#@nonl
	#@-node:setVisibleAreaToFullCanvas
	#@+node:setVisibleArea
	def setVisibleArea (self,args):
	
		r1,r2 = args
		r1,r2 = float(r1),float(r2)
		# print "scroll ratios:",r1,r2
	
		try:
			s = self.canvas.cget("scrollregion")
			x1,y1,x2,y2 = scanf(s,"%d %d %d %d")
			x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
		except:
			self.visibleArea = None
			return
			
		scroll_h = y2-y1
		# print "height of scrollregion:", scroll_h
	
		vy1 = y1 + (scroll_h*r1)
		vy2 = y1 + (scroll_h*r2)
		self.visibleArea = vy1,vy2
		# print "setVisibleArea: %5.1f %5.1f" % (vy1,vy2)
	#@-node:setVisibleArea
	#@+node:tree.updateTree
	def updateTree (self,v,x,y,h,level):
	
		yfirst = ylast = y
		if level==0: yfirst += 10
		while v:
			# trace(`x` + ", " + `y` + ", " + `v`)
			h = self.updateNode(v,x,y)
			y += h ; ylast = y
			if v.isExpanded() and v.firstChild():
				y = self.updateTree(v.firstChild(),x+child_indent,y,h,level+1)
			v = v.next()
		return y
	#@-node:tree.updateTree
	#@+node:dimEditLabel, undimEditLabel
	# Convenience methods so the caller doesn't have to know the present edit node.
	
	def dimEditLabel (self):
	
		v = self.currentVnode()
		self.setDisabledLabelState(v)
	
	def undimEditLabel (self):
	
		v = self.currentVnode()
		self.setSelectedLabelState(v)
	#@nonl
	#@-node:dimEditLabel, undimEditLabel
	#@+node:editLabel
	def editLabel (self, v):
		
		"""Start editing v.edit_text."""
	
		# End any previous editing
		if self.editVnode() and v != self.editVnode():
			self.endEditLabel()
			self.frame.revertHeadline = None
			
		self.setEditVnode(v)
	
		# Start editing
		if v and v.edit_text():
			self.setNormalLabelState(v)
			self.frame.revertHeadline = v.headString()
	#@nonl
	#@-node:editLabel
	#@+node:endEditLabel
	def endEditLabel (self):
		
		"""End editing for self.editText."""
	
		c = self.c ; v = self.editVnode() ; gui = app.gui
	
		if v and v.edit_text():
			self.setUnselectedLabelState(v)
			self.setEditVnode(None)
		if v: # Bug fix 10/9/02: also redraw ancestor headlines.
			self.force_redraw() # force a redraw of joined and ancestor headlines.
		gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02
	#@nonl
	#@-node:endEditLabel
	#@+node:tree.expandAllAncestors
	def expandAllAncestors (self,v):
	
		redraw_flag = false
		p = v.parent()
		while p:
			if not p.isExpanded():
				p.expand()
				redraw_flag = true
			p = p.parent()
		return redraw_flag
	#@nonl
	#@-node:tree.expandAllAncestors
	#@+node:tree.select
	# Warning: do not try to "optimize" this by returning if v==tree.currentVnode.
	
	def select (self,v,updateBeadList=true):
	
		#@	<< define vars and stop editing >>
		#@+node:<< define vars and stop editing >>
		c = self.c ; frame = c.frame ; body = frame.bodyCtrl
		old_v = c.currentVnode()
		
		# Unselect any previous selected but unedited label.
		self.endEditLabel()
		old = self.currentVnode()
		self.setUnselectedLabelState(old)
		#@nonl
		#@-node:<< define vars and stop editing >>
		#@nl
	
		if not doHook("unselect1",c=c,new_v=v,old_v=old_v):
			#@		<< unselect the old node >>
			#@+node:<< unselect the old node >>
			# Remember the position of the scrollbar before making any changes.
			yview=body.yview()
			insertSpot = c.frame.body.getInsertionPoint()
			
			# Remember the old body text
			old_body = body.get("1.0","end")
			
			if old and old != v and old.edit_text():
				old.t.scrollBarSpot = yview
				old.t.insertSpot = insertSpot
			#@-node:<< unselect the old node >>
			#@nl
		else: old_body = u""
	
		doHook("unselect2",c=c,new_v=v,old_v=old_v)
		
		if not doHook("select1",c=c,new_v=v,old_v=old_v):
			#@		<< select the new node >>
			#@+node:<< select the new node >>
			frame.setWrap(v)
			
			# Delete only if necessary: this may reduce flicker slightly.
			s = v.t.bodyString
			s = toUnicode(s,"utf-8")
			old_body = toUnicode(old_body,"utf-8")
			if old_body != s:
				body.delete("1.0","end")
				body.insert("1.0",s)
			
			# We must do a full recoloring: we may be changing context!
			self.frame.body.recolor_now(v)
			
			if v and v.t.scrollBarSpot != None:
				first,last = v.t.scrollBarSpot
				body.yview("moveto",first)
			
			if v.t.insertSpot != None: # 9/21/02: moved from c.selectVnode
				c.frame.bodyCtrl.mark_set("insert",v.t.insertSpot)
				c.frame.bodyCtrl.see(v.t.insertSpot)
			else:
				c.frame.bodyCtrl.mark_set("insert","1.0")
			#@nonl
			#@-node:<< select the new node >>
			#@nl
			if v and v != old_v: # 3/26/03: Suppress duplicate call.
				try: # may fail during initialization
					self.idle_scrollTo(v)
				except: pass
			#@		<< update c.beadList or c.beadPointer >>
			#@+node:<< update c.beadList or c.beadPointer >>
			if updateBeadList:
				
				if c.beadPointer > -1:
					present_v = c.beadList[c.beadPointer]
				else:
					present_v = None
				
				if v != present_v:
					# Replace the tail of c.beadList by c and make c the present node.
					# print "updating c.beadList"
					c.beadPointer += 1
					c.beadList[c.beadPointer:] = []
					c.beadList.append(v)
					
				# trace(c.beadPointer,v,present_v)
			
			#@-node:<< update c.beadList or c.beadPointer >>
			#@nl
			#@		<< update c.visitedList >>
			#@+node:<< update c.visitedList >>
			# Make v the most recently visited node on the list.
			if v in c.visitedList:
				c.visitedList.remove(v)
				
			c.visitedList.insert(0,v)
			#@nonl
			#@-node:<< update c.visitedList >>
			#@nl
	
		#@	<< set the current node and redraw >>
		#@+node:<< set the current node and redraw >>
		self.setCurrentVnode(v)
		self.setSelectedLabelState(v)
		self.frame.scanForTabWidth(v) # 9/13/02 #GS I believe this should also get into the select1 hook
		app.gui.set_focus(c,c.frame.bodyCtrl)
		#@nonl
		#@-node:<< set the current node and redraw >>
		#@nl
		doHook("select2",c=c,new_v=v,old_v=old_v)
		doHook("select3",c=c,new_v=v,old_v=old_v)
	#@-node:tree.select
	#@+node:tree.set...LabelState
	def setNormalLabelState (self,v): # selected, editing
	
		if v and v.edit_text():
			#@		<< set editing headline colors >>
			#@+node:<< set editing headline colors >>
			config = app.config
			fg   = config.getWindowPref("headline_text_editing_foreground_color")
			bg   = config.getWindowPref("headline_text_editing_background_color")
			selfg = config.getWindowPref("headline_text_editing_selection_foreground_color")
			selbg = config.getWindowPref("headline_text_editing_selection_background_color")
			
			if not fg or not bg:
				fg,bg = "black","white"
				
			try:
				if selfg and selbg:
					v.edit_text().configure(
						selectforeground=selfg,selectbackground=selbg,
						state="normal",highlightthickness=1,fg=fg,bg=bg)
				else:
					v.edit_text().configure(
						state="normal",highlightthickness=1,fg=fg,bg=bg)
			except:
				es_exception()
			#@nonl
			#@-node:<< set editing headline colors >>
			#@nl
			v.edit_text().tag_remove("sel","1.0","end")
			v.edit_text().tag_add("sel","1.0","end")
			app.gui.set_focus(self.c,v.edit_text())
	
	def setDisabledLabelState (self,v): # selected, disabled
		if v and v.edit_text():
			#@		<< set selected, disabled headline colors >>
			#@+node:<< set selected, disabled headline colors >>
			config = app.config
			fg = config.getWindowPref("headline_text_selected_foreground_color")
			bg = config.getWindowPref("headline_text_selected_background_color")
			
			if not fg or not bg:
				fg,bg = "black","gray80"
			
			try:
				v.edit_text().configure(
					state="disabled",highlightthickness=0,fg=fg,bg=bg)
			except:
				es_exception()
			#@nonl
			#@-node:<< set selected, disabled headline colors >>
			#@nl
	
	def setSelectedLabelState (self,v): # selected, not editing
		self.setDisabledLabelState(v)
	
	def setUnselectedLabelState (self,v): # not selected.
		if v and v.edit_text():
			#@		<< set unselected headline colors >>
			#@+node:<< set unselected headline colors >>
			config = app.config
			fg = config.getWindowPref("headline_text_unselected_foreground_color")
			bg = config.getWindowPref("headline_text_unselected_background_color")
			
			if not fg or not bg:
				fg,bg = "black","white"
			
			try:
				v.edit_text().configure(
					state="disabled",highlightthickness=0,fg=fg,bg=bg)
			except:
				es_exception()
			#@nonl
			#@-node:<< set unselected headline colors >>
			#@nl
	#@nonl
	#@-node:tree.set...LabelState
	#@+node:tree.moveUpDown
	def OnUpKey   (self,event=None): return self.moveUpDown("up")
	def OnDownKey (self,event=None): return self.moveUpDown("down")
	
	def moveUpDown (self,upOrDown):
		c = self.c ; body = c.frame.bodyCtrl
		# Make the insertion cursor visible so bbox won't return an empty list.
		body.see("insert")
		# Find the coordinates of the cursor and set the new height.
		# There may be roundoff errors because character postions may not match exactly.
		ins =  body.index("insert")
		lines,char = scanf(ins,"%d.%d")
		x,y,junk,textH = body.bbox("insert")
		bodyW,bodyH = body.winfo_width(),body.winfo_height()
		junk,maxy,junk,junk = body.bbox("@%d,%d" % (bodyW,bodyH))
		# Make sure y is within text boundaries.
		if upOrDown == "up":
			if y <= textH:
				body.yview("scroll",-1,"units")
			else: y = max(y-textH,0)
		else:
			if y >= maxy:
				body.yview("scroll",1,"units")
			else: y = min(y+textH,maxy)
		# Position the cursor on the proper side of the characters.
		newx,newy,width,junk = body.bbox("@%d,%d" % (x,y))
		if x > newx + width/2:
			x = newx + width + 1
		result = body.index("@%d,%d" % (x,y))
		body.mark_set("insert",result)
		# trace("entry:  %s.%s" % (lines,char))
		# trace("result:",result)
		# trace("insert:",body.index("insert"))
		return "break" # Inhibit further bindings.
	#@nonl
	#@-node:tree.moveUpDown
	#@-others
#@nonl
#@-node:@file leoTkinterTree.py
#@-leo
