#@+leo-ver=4-thin
#@+node:ekr.20031218072017.4138:@file-thin leoTkinterTree.py
#@@language python

#@<< about the tree classes >>
#@+node:ekr.20031218072017.4139:<< about the tree classes >>
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
#@-node:ekr.20031218072017.4139:<< about the tree classes >>
#@nl

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoFrame
import Tkinter,tkFont
import os,string,sys,types

#@<< about drawing >>
#@+node:ekr.20031218072017.2409:<< About drawing >>
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
#@-node:ekr.20031218072017.2409:<< About drawing >>
#@nl
#@<< drawing constants >>
#@+node:ekr.20031218072017.4140:<< drawing constants >>
box_padding = 5 # extra padding between box and icon
box_width = 9 + box_padding
icon_width = 20
icon_padding = 2
text_indent = 4 # extra padding between icon and tex
child_indent = 28 # was 20
hline_y = 7 # Vertical offset of horizontal line
root_left = 7 + box_width
root_top = 2
hiding = true # true if we don't reallocate items
line_height = 17 + 2 # To be replaced by Font height
#@nonl
#@-node:ekr.20031218072017.4140:<< drawing constants >>
#@nl

class leoTkinterTree (leoFrame.leoTree):
	
	callbacksInjected = false

	"""Leo tkinter tree class."""
	
	#@	@+others
	#@+node:ekr.20031218072017.4141:tree.Birth & death (Tkinter)
	#@+node:ekr.20031218072017.1017:tree.__init__
	def __init__(self,c,frame,canvas):
		
		# Init the base class.
		leoFrame.leoTree.__init__(self,frame)
	
		# Objects associated with this tree.
		self.canvas = canvas
	
		# Miscellaneous info.
		self.iconimages = {} # Image cache set by getIconImage().
		self.active = false # true if tree is active
		self._editPosition = None
		self.lineyoffset = 0 # y offset for this headline.
		self.disableRedraw = false # True: reschedule a redraw for later.
		
		# Set self.font and self.fontName.
		self.setFontFromConfig()
		
		# Recycling bindings.
		self.bindings = [] # List of bindings to be unbound when redrawing.
		self.tagBindings = [] # List of tag bindings to be unbound when redrawing.
		self.icon_id_dict = {} # New in 3.12: keys are icon id's, values are vnodes.
		self.widgets = [] # Widgets that must be destroyed when redrawing.
		
		# Drag and drop
		self.drag_p = None
		self.controlDrag = false # true: control was down when drag started.
		self.drag_id = None # To reset bindings after drag
		
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
	#@-node:ekr.20031218072017.1017:tree.__init__
	#@+node:ekr.20031218072017.4142:tree.deleteBindings
	def deleteBindings (self):
		
		"""Delete all tree bindings and all references to tree widgets."""
		
		# g.trace(len(self.tagBindings),len(self.bindings))
	
		count = 0
		# Unbind all the tag bindings.
		if 0:  # testing.
			self.tagBindings = []
			self.bindings = []
		else:
			for id,id2,binding in self.tagBindings:
				self.canvas.tag_unbind(id,binding,id2)
				count += 1
			self.tagBindings = []
			# Unbind all the text bindings.
			for t,id,binding in self.bindings:
				t.unbind(binding,id)
				count += 1
			self.bindings = []
	
			# g.trace("bindings freed:",count)
	#@nonl
	#@-node:ekr.20031218072017.4142:tree.deleteBindings
	#@+node:ekr.20031218072017.4143:tree.deleteWidgets
	# canvas.delete("all") does _not_ delete the Tkinter objects associated with those objects!
	
	def deleteWidgets (self):
		
		"""Delete all widgets in the canvas"""
		
		# g.trace(len(self.widgets))
		
		self.icon_id_dict = {} # Delete all references to icons.
		self.edit_text_dict = {} # Delete all references to Tk.Edit widgets.
			
		# Fixes a _huge_ memory leak.
		for w in self.widgets:
			w.destroy() 
	
		self.widgets = []
		
		# g.trace("done")
	#@nonl
	#@-node:ekr.20031218072017.4143:tree.deleteWidgets
	#@+node:ekr.20031218072017.1956:tree.injectCallbacks (class method)
	def injectCallbacks(self):
		
		import leoNodes
		
		#@	<< define tkinter callbacks to be injected in the position class >>
		#@+node:ekr.20031218072017.1957:<< define tkinter callbacks to be injected in the position class >>
		# N.B. These vnode methods are entitled to know about details of the leoTkinterTree class.
		
		#@+others
		#@+node:ekr.20031218072017.1958:OnBoxClick
		# Called when the box is clicked.
		
		def OnBoxClick(self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("boxclick1",c=c,p=p,event=event):
					c.frame.tree.OnBoxClick(p)
				g.doHook("boxclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("boxclick")
		#@nonl
		#@-node:ekr.20031218072017.1958:OnBoxClick
		#@+node:ekr.20031218072017.1959:OnDrag
		def OnDrag(self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if c.frame.tree.dragging():
					if not g.doHook("dragging1",c=c,p=p,event=event):
						c.frame.tree.OnDrag(p,event)
					g.doHook("dragging2",c=c,p=p,event=event)
				else:
					if not g.doHook("drag1",c=c,p=p,event=event):
						c.frame.tree.OnDrag(p,event)
					g.doHook("drag2",c=c,p=p,event=event)
			except:
				g.es_event_exception("drag")
		#@nonl
		#@-node:ekr.20031218072017.1959:OnDrag
		#@+node:ekr.20031218072017.1960:OnEndDrag
		def OnEndDrag(self,event=None):
			
			"""Callback injected into vnode or position class."""
			
			# g.trace()
		
			try:
				p = self ; c = p.c
				# 7/10/03: Always call frame.OnEndDrag, regardless of state.
				if not g.doHook("enddrag1",c=c,p=p,event=event):
					c.frame.tree.OnEndDrag(p,event)
				g.doHook("enddrag2",c=c,p=p,event=event)
			except:
				g.es_event_exception("enddrag")
		#@nonl
		#@-node:ekr.20031218072017.1960:OnEndDrag
		#@+node:ekr.20031218072017.1961:OnHeadlineClick & OnHeadlineRightClick
		def OnHeadlineClick(self,event=None):
			"""Callback injected into vnode or position class."""
			try:
				p = self ; c = p.c
				if not g.doHook("headclick1",c=c,p=p,event=event):
					c.frame.tree.OnActivate(p)
				g.doHook("headclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("headclick")
			
		def OnHeadlineRightClick(self,event=None):
		
			"""Callback injected into vnode or position class."""
		
			#g.trace()
			try:
				p = self ; c = p.c
				if not g.doHook("headrclick1",c=c,p=p,event=event):
					c.frame.tree.OnActivate(p)
					c.frame.tree.OnPopup(self,event)
				g.doHook("headrclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("headrclick")
		#@nonl
		#@-node:ekr.20031218072017.1961:OnHeadlineClick & OnHeadlineRightClick
		#@+node:ekr.20031218072017.1962:OnHyperLinkControlClick
		def OnHyperLinkControlClick (self,event):
			
			"""Callback injected into vnode or position class."""
		
			# g.trace()
			try:
				p = self ; c = p.c
				if not g.doHook("hypercclick1",c=c,p=p,event=event):
					c.beginUpdate()
					c.selectVnode(p)
					c.endUpdate()
					c.frame.bodyCtrl.mark_set("insert","1.0")
				g.doHook("hypercclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("hypercclick")
		#@nonl
		#@-node:ekr.20031218072017.1962:OnHyperLinkControlClick
		#@+node:ekr.20031218072017.1963:OnHeadlineKey
		def OnHeadlineKey (self,event=None):
		
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("headkey1",c=c,p=p,event=event):
					c.frame.tree.OnHeadlineKey(p,event)
				g.doHook("headkey2",c=c,p=p,event=event)
			except:
				g.es_event_exception("headkey")
		#@nonl
		#@-node:ekr.20031218072017.1963:OnHeadlineKey
		#@+node:ekr.20031218072017.1964:OnHyperLinkEnter
		def OnHyperLinkEnter (self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("hyperenter1",c=c,p=p,event=event):
					if 0: # This works, and isn't very useful.
						c.frame.bodyCtrl.tag_config(p.tagName,background="green")
				g.doHook("hyperenter2",c=c,p=p,event=event)
			except:
				g.es_event_exception("hyperenter")
		#@nonl
		#@-node:ekr.20031218072017.1964:OnHyperLinkEnter
		#@+node:ekr.20031218072017.1965:OnHyperLinkLeave
		def OnHyperLinkLeave (self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("hyperleave1",c=c,p=p,event=event):
					if 0: # This works, and isn't very useful.
						c.frame.bodyCtrl.tag_config(p.tagName,background="white")
				g.doHook("hyperleave2",c=c,p=p,event=event)
			except:
				g.es_event_exception("hyperleave")
		#@nonl
		#@-node:ekr.20031218072017.1965:OnHyperLinkLeave
		#@+node:ekr.20031218072017.1966:OnIconClick & OnIconRightClick
		def OnIconClick(self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("iconclick1",c=c,p=p,event=event):
					c.frame.tree.OnIconClick(p,event)
				g.doHook("iconclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("iconclick")
			
		def OnIconRightClick(self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("iconrclick1",c=c,p=p,event=event):
					c.frame.tree.OnIconRightClick(p,event)
				g.doHook("iconrclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("iconrclick")
		#@-node:ekr.20031218072017.1966:OnIconClick & OnIconRightClick
		#@+node:ekr.20031218072017.1967:OnIconDoubleClick
		def OnIconDoubleClick(self,event=None):
			
			"""Callback injected into vnode or position class."""
		
			try:
				p = self ; c = p.c
				if not g.doHook("icondclick1",c=c,p=p,event=event):
					c.frame.tree.OnIconDoubleClick(self)
				g.doHook("icondclick2",c=c,p=p,event=event)
			except:
				g.es_event_exception("icondclick")
		#@-node:ekr.20031218072017.1967:OnIconDoubleClick
		#@-others
		#@nonl
		#@-node:ekr.20031218072017.1957:<< define tkinter callbacks to be injected in the position class >>
		#@nl
	
		for f in (
			OnBoxClick,OnDrag,OnEndDrag,
			OnHeadlineClick,OnHeadlineRightClick,OnHeadlineKey,
			OnHyperLinkControlClick,OnHyperLinkEnter,OnHyperLinkLeave,
			OnIconClick,OnIconDoubleClick,OnIconRightClick):
			
			g.funcToMethod(f,leoNodes.position)
	#@nonl
	#@-node:ekr.20031218072017.1956:tree.injectCallbacks (class method)
	#@-node:ekr.20031218072017.4141:tree.Birth & death (Tkinter)
	#@+node:ekr.20031218072017.1011:Updating routines (tree)...
	#@+node:ekr.20031218072017.1012:tree.redraw
	# Calling redraw inside c.beginUpdate()/c.endUpdate() does nothing.
	# This _is_ useful when a flag is passed to c.endUpdate.
	
	def redraw (self,event=None):
		
		# g.trace(self.updateCount,self.redrawScheduled)
		
		if self.updateCount == 0 and not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
	#@nonl
	#@-node:ekr.20031218072017.1012:tree.redraw
	#@+node:ekr.20040106095546:tkTree.redrawAfterException
	#@+at 
	#@nonl
	# This is called only from doCommand.  The implicit assumption is that 
	# doCommand itself is not contained in a beginUpdate/endUpdate pair.
	#@-at
	#@@c
	
	def redrawAfterException (self):
		
		"""Make sure drawing is enabled following an exception."""
			
		if not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
			self.updateCount = 0 # would not work if we are in a beginUpdate/endUpdate pair.
	#@nonl
	#@-node:ekr.20040106095546:tkTree.redrawAfterException
	#@+node:ekr.20031218072017.1013:force_redraw
	# Schedules a redraw even if inside beginUpdate/endUpdate
	def force_redraw (self):
		
		# g.trace(self.redrawScheduled)
		# import traceback ; traceback.print_stack()
	
		if not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
	#@nonl
	#@-node:ekr.20031218072017.1013:force_redraw
	#@+node:ekr.20031218072017.1014:redraw_now
	# Redraws immediately: used by Find so a redraw doesn't mess up selections.
	# It is up to the caller to ensure that no other redraws are pending.
	
	def redraw_now (self,scroll=true):
		
		# g.trace()
	
		self.idle_redraw(scroll=scroll)
	#@-node:ekr.20031218072017.1014:redraw_now
	#@+node:ekr.20031218072017.1015:idle_redraw
	def idle_redraw (self,scroll=true):
		
		c = self.c ; frame = c.frame
	
		self.redrawScheduled = false # Always do this here.
	
		#@	<< return if disabled, or quitting or dragging >>
		#@+node:ekr.20040324090957:<< return if disabled, or quitting or dragging >>
		if self.disableRedraw:
			# We have been called as the result of an update_idletasks in the log pane.
			# Don't do anything now.
			return
		
		if frame not in g.app.windowList or g.app.quitting:
			# g.trace("no frame")
			return
		
		if self.drag_p:
			# g.trace("dragging",self.drag_p)
			return
		#@-node:ekr.20040324090957:<< return if disabled, or quitting or dragging >>
		#@nl
	
		# g.print_bindings("canvas",self.canvas)
	
		self.expandAllAncestors(c.currentPosition())
	
		oldcursor = self.canvas['cursor']
		self.canvas['cursor'] = "watch"
	
		if not g.doHook("redraw-entire-outline",c=self.c):
			self.allocatedNodes = 0
			#@		<< Erase and redraw the entire tree >>
			#@+node:ekr.20040324090957.1:<< Erase and redraw the entire tree >>
			# Delete all widgets.
			c.setTopVnode(None)
			self.deleteBindings()
			self.canvas.delete("all")
			self.deleteWidgets()
			
			# Redraw the tree.
			self.setVisibleAreaToFullCanvas()
			self.drawTopTree()
			
			# Set up the scroll region after the tree has been redrawn.
			x0, y0, x1, y1 = self.canvas.bbox("all")
			self.canvas.configure(scrollregion=(0, 0, x1, y1))
			
			# g.printGc()
			
			# Do a scrolling operation after the scrollbar is redrawn
			if scroll:
				self.canvas.after_idle(self.idle_scrollTo)
			#@nonl
			#@-node:ekr.20040324090957.1:<< Erase and redraw the entire tree >>
			#@nl
			if self.trace:
				self.redrawCount += 1
				print "idle_redraw allocated:",self.redrawCount,self.allocatedNodes
		g.doHook("after-redraw-outline",c=self.c)
	
		self.canvas['cursor'] = oldcursor
	#@-node:ekr.20031218072017.1015:idle_redraw
	#@+node:ekr.20031218072017.1016:idle_second_redraw
	def idle_second_redraw (self):
		
		c = self.c
		
		g.trace()
			
		# Erase and redraw the entire tree the SECOND time.
		# This ensures that all visible nodes are allocated.
		c.setTopVnode(None)
		args = self.canvas.yview()
		self.setVisibleArea(args)
		self.deleteBindings()
		self.canvas.delete("all")
		self.drawTopTree()
		
		if self.trace:
			print "idle_second_redraw allocated:",self.redrawCount, self.allocatedNodes
	#@nonl
	#@-node:ekr.20031218072017.1016:idle_second_redraw
	#@-node:ekr.20031218072017.1011:Updating routines (tree)...
	#@+node:ekr.20031218072017.4144:Drawing (tkTree)
	#@+node:ekr.20031218072017.4145:About drawing and updating
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
	#@-node:ekr.20031218072017.4145:About drawing and updating
	#@+node:ekr.20031218072017.1000:drawBox (tag_bind)
	def drawBox (self,p,x,y):
	
		y += 7 # draw the box at x, y+7
		h = self.line_height
	
		tree = self
		iconname = g.choose(p.isExpanded(),"minusnode.gif", "plusnode.gif")
		image = self.getIconImage(iconname)
		id = self.canvas.create_image(x,y+self.lineyoffset,image=image)
		
		if 1: # New in 4.2.  Create a frame to catch all clicks.
			id4 = self.canvas.create_rectangle(0,y-7,1000,y-7+h-3)
			color = ""
			self.canvas.itemconfig(id4,fill=color,outline=color)
			self.canvas.lower(id4)
			id3 = self.canvas.tag_bind(id4, "<1>", p.OnBoxClick)
			self.tagBindings.append((id,id3,"<1>"),)
	
		id1 = self.canvas.tag_bind(id, "<1>", p.OnBoxClick)
		id2 = self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
		
		# Remember the bindings so deleteBindings can delete them.
		self.tagBindings.append((id,id1,"<1>"),)
		self.tagBindings.append((id,id2,"<Double-1>"),)
	#@-node:ekr.20031218072017.1000:drawBox (tag_bind)
	#@+node:ekr.20031218072017.1002:drawIcon (tag_bind)
	def drawIcon(self,p,x=None,y=None):
		
		"""Draws icon for position p at x,y, or at p.v.iconx,p.v.icony if x,y = None,None"""
	
		tree = self
		
		# Make sure the bindings refer to the _present_ position.
		v = p.v
	
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
	
		# Always recompute v.iconVal.
		# This is an important drawing optimization.
		val = v.iconVal = v.computeIcon()
		assert(0 <= val <= 15)
	
		# Get the image.
		imagename = "box%02d.GIF" % val
		image = self.getIconImage(imagename)
		id = self.canvas.create_image(x,y+self.lineyoffset,anchor="nw",image=image)
		self.icon_id_dict[id] = p # Remember which vnode belongs to the icon.
	
		id1 = self.canvas.tag_bind(id,"<1>",p.OnIconClick)
		id2 = self.canvas.tag_bind(id,"<Double-1>",p.OnIconDoubleClick)
		id3 = self.canvas.tag_bind(id,"<3>",p.OnIconRightClick)
		
		# Remember the bindings so deleteBindings can delete them.
		self.tagBindings.append((id,id1,"<1>"),)
		self.tagBindings.append((id,id2,"<Double-1>"),)
		self.tagBindings.append((id,id3,"<3>"),)
	
		return 0,icon_width # dummy icon height,width
	#@nonl
	#@-node:ekr.20031218072017.1002:drawIcon (tag_bind)
	#@+node:ekr.20031218072017.1004:drawNode & force_draw_node (good trace)
	def drawNode(self,p,x,y):
	
		"""Draw horizontal line from vertical line to icon"""
		
		if 1:
			self.lineyoffset = 0
		else:
			if hasattr(p.v.t,"unknownAttributes"):
				self.lineyoffset = p.v.t.unknownAttributes.get("lineYOffset",0)
			else:
				self.lineyoffset = 0
			
		self.canvas.create_line(x,y+7+self.lineyoffset,
			x+box_width,y+7+self.lineyoffset,
			tag="lines",fill="gray50") # stipple="gray25")
	
		if self.inVisibleArea(y):
			return self.force_draw_node(p,x,y)
		else:
			return self.line_height,0
	#@nonl
	#@+node:ekr.20040317171729:force_draw_node (new)
	def force_draw_node(self,p,x,y):
	
		self.allocatedNodes += 1
		h,w = self.drawUserIcons(p,"beforeBox",x,y)
		xw = w # The extra indentation before the icon box.
		if p.hasChildren():
			self.drawBox(p,x+w,y)
		w += box_width # even if box isn't drawn.
	
		h2,w2 = self.drawUserIcons(p,"beforeIcon",x+w,y)
		h = max(h,h2) ; w += w2 ; xw += w2
	
		h2,w2 = self.drawIcon(p,x+w,y)
		h = max(h,h2) ; w += w2
	
		h2,w2 = self.drawUserIcons(p,"beforeHeadline",x+w,y)
		h = max(h,h2) ; w += w2
	
		h2 = self.drawText(p,x+w,y)
		h = max(h,h2)
		w += self.widthInPixels(p.headString())
	
		h2,w2 = self.drawUserIcons(p,"afterHeadline",x+w,y)
		h = max(h,h2)
	
		return h,xw
	#@nonl
	#@-node:ekr.20040317171729:force_draw_node (new)
	#@+node:ekr.20040318090335:force_draw_node (old)
	def force_draw_nodeOLD(self,p,x,y):
	
		self.allocatedNodes += 1
	
		if p.hasChildren():
			self.drawBox(p,x,y)
		w = box_width # Even if the box isn't drawn.
	
		h2,w2 = self.drawIcon(p,x+w,y)
		w += w2
	
		h = self.drawText(p,x+w,y)
		
		return h,0
	#@-node:ekr.20040318090335:force_draw_node (old)
	#@-node:ekr.20031218072017.1004:drawNode & force_draw_node (good trace)
	#@+node:ekr.20031218072017.1005:drawText (bind)
	def drawText(self,p,x,y):
		
		"""draw text for v at nominal coordinates x,y."""
	
		tree = self ; c = self.c ; v = p.v
		x += text_indent
	
		t = Tkinter.Text(self.canvas,
			font=self.font,bd=0,relief="flat",width=self.headWidth(v),height=1)
	
		# New in 4.2: entries a pairs (p,t) indexed by v.
		# Remember which text widget belongs to v.
		d = self.edit_text_dict
		val = d.get(v,[])
		val.append((p,t),)
		d[v] = val
		# g.trace("entry",d[p.v])
	
		# Remember the widget so deleteBindings can delete it.
		self.widgets.append(t) # Fixes a _huge_ memory leak.
	
		t.insert("end", v.headString())
		#@	<< configure the text depending on state >>
		#@+node:ekr.20031218072017.1006:<< configure the text depending on state >>
		if p and p == c.currentPosition():
			if p == self.editPosition():
				self.setNormalLabelState(p)
			else:
				self.setDisabledLabelState(p) # selected, disabled
		else:
			self.setUnselectedLabelState(p) # unselected
		#@nonl
		#@-node:ekr.20031218072017.1006:<< configure the text depending on state >>
		#@nl
	
		# Use vnode or postion callbacks.
		id1 = t.bind("<1>",p.OnHeadlineClick)
		id2 = t.bind("<3>",p.OnHeadlineRightClick)
		
		if 0: # 6/15/02: Bill Drissel objects to this binding.
			t.bind("<Double-1>", p.OnBoxClick)
		id3 = t.bind("<Key>", p.OnHeadlineKey)
		id4 = t.bind("<Control-t>",self.OnControlT)
			# 10/16/02: Stamp out the erroneous control-t binding.
			
		# Remember the bindings so deleteBindings can delete them.
		self.bindings.append((t,id1,"<1>"),)
		self.bindings.append((t,id2,"<3>"),)
		self.bindings.append((t,id3,"<Key>"),)
		self.bindings.append((t,id4,"<Control-t>"),)
	
		id = self.canvas.create_window(x,y+self.lineyoffset,anchor="nw",window=t)
		self.canvas.tag_lower(id)
		
		# This doesn't work: must call update_idletasks first, and that's hard here.
		# g.trace(t,t.winfo_height(),t.winfo_width())
		
		return self.line_height
	#@nonl
	#@-node:ekr.20031218072017.1005:drawText (bind)
	#@+node:ekr.20031218072017.2029:drawTopTree
	def drawTopTree (self):
		
		"""Draws the top-level tree, taking into account the hoist state."""
		
		c = self.c
		
		if c.hoistStack:
			p,junk = c.hoistStack[-1]
			self.drawTree(p.copy(),root_left,root_top,0,0,hoistFlag=true)
		else:
			self.drawTree(c.rootPosition(),root_left,root_top,0,0)
			
		# g.trace(g.app.copies) ; g.app.copies = 0
		# import traceback ; traceback.print_stack()
	#@nonl
	#@-node:ekr.20031218072017.2029:drawTopTree
	#@+node:ekr.20031218072017.1008:drawTree
	def drawTree(self,p,x,y,h,level,hoistFlag=false):
	
		yfirst = ylast = y
		if level==0: yfirst += 10
		w = 0
		
		# We must make copies for drawText and drawBox and drawIcon,
		# So making copies here actually reduces the total number of copies.
		### This will change for incremental redraw.
		p = p.copy()
		while p: # Do not use iterator.
			h,w = self.drawNode(p,x,y)
			y += h ; ylast = y
			if p.isExpanded() and p.hasFirstChild():
				# Must make an additional copy here by calling firstChild.
				y,w2 = self.drawTree(p.firstChild(),x+child_indent+w,y,h,level+1)
				x += w2 ; w += w2
			if hoistFlag: break
			else:         p = p.next()
		#@	<< draw vertical line >>
		#@+node:ekr.20031218072017.1009:<< draw vertical line >>
		id = self.canvas.create_line(
			x, yfirst-hline_y,
			x, ylast+hline_y-h,
			fill="gray50", # stipple="gray50"
			tag="lines")
		
		self.canvas.tag_lower(id)
		#@nonl
		#@-node:ekr.20031218072017.1009:<< draw vertical line >>
		#@nl
		return y,w
	#@nonl
	#@-node:ekr.20031218072017.1008:drawTree
	#@+node:ekr.20040317095510:drawUserIcon
	def drawUserIcon (self,where,x,y,dict):
		
		h,w = 0,0
	
		if where != dict.get("where","beforeHeadline"):
			return h,w
			
		# g.trace(where,x,y,dict)
		
		#@	<< set offsets and pads >>
		#@+node:ekr.20040317173849:<< set offsets and pads >>
		xoffset = dict.get("xoffset")
		try:    xoffset = int(xoffset)
		except: xoffset = 0
		
		yoffset = dict.get("yoffset")
		try:    yoffset = int(yoffset)
		except: yoffset = 0
		
		xpad = dict.get("xpad")
		try:    xpad = int(xpad)
		except: xpad = 0
		
		ypad = dict.get("ypad")
		try:    ypad = int(ypad)
		except: ypad = 0
		#@nonl
		#@-node:ekr.20040317173849:<< set offsets and pads >>
		#@nl
		type = dict.get("type")
		if type == "icon":
			s = dict.get("icon")
			#@		<< draw the icon in string s >>
			#@+node:ekr.20040317095153:<< draw the icon in string s >>
			pass
			#@nonl
			#@-node:ekr.20040317095153:<< draw the icon in string s >>
			#@nl
		elif type == "file":
			file = dict.get("file")
			#@		<< draw the icon at file >>
			#@+node:ekr.20040317100702:<< draw the icon at file >>
			try:
				image = self.iconimages[file]
				# Get the image from the cache if possible.
			except KeyError:
				try:
					fullname = g.os_path_join(g.app.loadDir,"..","Icons",file)
					fullname = g.os_path_normpath(fullname)
					image = Tkinter.PhotoImage(master=self.canvas,file=fullname)
					self.iconimages[fullname] = image
				except:
					#g.es("Exception loading: " + fullname)
					#g.es_exception()
					image = None
					
			if image:
				id = self.canvas.create_image(x+xoffset,y+yoffset,anchor="nw",image=image)
				self.canvas.lift(id)
				h = image.height() + yoffset + ypad
				w = image.width()  + xoffset + xpad
			#@nonl
			#@-node:ekr.20040317100702:<< draw the icon at file >>
			#@nl
		elif type == "url":
			url = dict.get("url")
			#@		<< draw the icon at url >>
			#@+node:ekr.20040317095153.1:<< draw the icon at url >>
			pass
			#@nonl
			#@-node:ekr.20040317095153.1:<< draw the icon at url >>
			#@nl
			
		# Allow user to specify height, width explicitly.
		h = dict.get("height",h)
		w = dict.get("width",w)
	
		return h,w
	#@nonl
	#@-node:ekr.20040317095510:drawUserIcon
	#@+node:ekr.20040317094609:drawUserIcons
	def drawUserIcons(self,p,where,x,y):
		
		"""Draw any icons specified by p.v.t.unknownAttributes["icons"]."""
		
		h,w = 0,0 ; t = p.v.t
		
		if not hasattr(t,"unknownAttributes"):
			return h,w
		
		iconsList = t.unknownAttributes.get("icons")
		# g.trace(iconsList)
		
		try:
			for dict in iconsList:
				h2,w2 = self.drawUserIcon(where,x+w,y,dict)
				h = max(h,h2) ; w += w2
		except:
			g.es_exception()
	
		return h,w
	#@nonl
	#@-node:ekr.20040317094609:drawUserIcons
	#@+node:ekr.20031218072017.1010:inVisibleArea & inExpandedVisibleArea
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
	#@-node:ekr.20031218072017.1010:inVisibleArea & inExpandedVisibleArea
	#@+node:ekr.20031218072017.4147:tree.getIconImage
	def getIconImage (self, name):
	
		# Return the image from the cache if possible.
		if self.iconimages.has_key(name):
			return self.iconimages[name]
			
		try:
			fullname = g.os_path_join(g.app.loadDir,"..","Icons",name)
			fullname = g.os_path_normpath(fullname)
			image = Tkinter.PhotoImage(master=self.canvas, file=fullname)
			self.iconimages[name] = image
			return image
		except:
			g.es("Exception loading: " + fullname)
			g.es_exception()
			return None
	#@nonl
	#@-node:ekr.20031218072017.4147:tree.getIconImage
	#@+node:ekr.20040322122232:tree.scrollTo
	def scrollTo (self,p):
		
		def scrollToCallback(event=None,self=self,p=p):
			g.trace(event,self,p)
			self.idle_scrollTo(p)
		
		self.canvas.after_idle(scrollToCallback)
	#@nonl
	#@-node:ekr.20040322122232:tree.scrollTo
	#@+node:ekr.20031218072017.1018:tree.idle_scrollTo
	def idle_scrollTo(self,p=None):
	
		"""Scrolls the canvas so that v is in view.
		
		This is done at idle time after a redraw so that treeBar.get() will return proper values."""
	
		c = self.c ; frame = c.frame
		if not p: p = self.c.currentPosition()
		if not p: p = self.c.rootPosition() # 4/8/04.
		try:
			last = p.lastVisible()
			nextToLast = last.visBack()
			h1 = self.yoffset(p)
			h2 = self.yoffset(last)
			#@		<< compute approximate line height >>
			#@+node:ekr.20040314092716:<< compute approximate line height >>
			if nextToLast: # 2/2/03: compute approximate line height.
				lineHeight = h2 - self.yoffset(nextToLast)
			else:
				lineHeight = 20 # A reasonable default.
			#@nonl
			#@-node:ekr.20040314092716:<< compute approximate line height >>
			#@nl
			#@		<< Compute the fractions to scroll down/up >>
			#@+node:ekr.20040314092716.1:<< Compute the fractions to scroll down/up >>
			data = frame.treeBar.get()
			try: lo, hi = data
			except: lo,hi = 0.0,1.0
			if h2 > 0.1:
				frac = float(h1)/float(h2) # For scrolling down.
				frac2 = float(h1+lineHeight/2)/float(h2) # For scrolling up.
				frac2 = frac2 - (hi - lo)
			else:
				frac = frac2 = 0.0 # probably any value would work here.
				
			frac =  max(min(frac,1.0),0.0)
			frac2 = max(min(frac2,1.0),0.0)
			#@nonl
			#@-node:ekr.20040314092716.1:<< Compute the fractions to scroll down/up >>
			#@nl
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
				
			c.setTopVnode(p) # 1/30/04: remember a pseudo "top" node.
			# print "%3d %3d %1.3f %1.3f %1.3f %1.3f" % (h1,h2,frac,frac2,lo,hi)
		except:
			g.es_exception()
	#@nonl
	#@-node:ekr.20031218072017.1018:tree.idle_scrollTo
	#@+node:ekr.20031218072017.4148:tree.numberOfVisibleNodes
	def numberOfVisibleNodes(self):
		
		n = 0 ; p = self.c.rootPosition()
		while p:
			n += 1
			p.moveToVisNext()
		return n
	#@nonl
	#@-node:ekr.20031218072017.4148:tree.numberOfVisibleNodes
	#@+node:ekr.20031218072017.4149:tree.yoffset
	#@+at 
	#@nonl
	# We can't just return icony because the tree hasn't been redrawn yet.  
	# For the same reason we can't rely on any TK canvas methods here.
	#@-at
	#@@c
	
	def yoffset(self, v1):
	
		# if not v1.isVisible(): print "yoffset not visible:",v1
		root = self.c.rootPosition()
		h, flag = self.yoffsetTree(root,v1)
		# flag can be false during initialization.
		# if not flag: print "yoffset fails:",h,v1
		return h
	
	# Returns the visible height of the tree and all sibling trees, stopping at p1
	
	def yoffsetTree(self,p,p1):
	
		h = 0
		for p in p.siblings_iter():
			# print "yoffsetTree:", p
			if p == p1:
				return h, true
			h += self.line_height
			if p.isExpanded() and p.hasChildren():
				child = p.firstChild()
				h2, flag = self.yoffsetTree(child,p1)
				h += h2
				if flag: return h, true
		
		return h, false
	#@nonl
	#@-node:ekr.20031218072017.4149:tree.yoffset
	#@-node:ekr.20031218072017.4144:Drawing (tkTree)
	#@+node:ekr.20031218072017.4150:Config & Measuring
	#@+node:ekr.20031218072017.4151:tree.getFont,setFont,setFontFromConfig
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
	
		font = g.app.config.getFontFromParams(
			"headline_text_font_family", "headline_text_font_size",
			"headline_text_font_slant",  "headline_text_font_weight",
			g.app.config.defaultTreeFontSize)
	
		self.setFont(font)
	#@nonl
	#@-node:ekr.20031218072017.4151:tree.getFont,setFont,setFontFromConfig
	#@+node:ekr.20031218072017.4152:headWidth & widthInPixels
	def headWidth(self,v):
	
		"""Returns the proper width of the entry widget for the headline."""
	
		return max(10,5 + len(v.headString()))
		
	def widthInPixels(self,s):
	
		s = g.toEncodedString(s,g.app.tkEncoding)
		
		width = self.font.measure(s)
		
		# g.trace(width,s)
		
		return width
	#@nonl
	#@-node:ekr.20031218072017.4152:headWidth & widthInPixels
	#@+node:ekr.20031218072017.4153:setLineHeight
	def setLineHeight (self,font):
		
		try:
			metrics = font.metrics()
			linespace = metrics ["linespace"]
			self.line_height = linespace + 5 # Same as before for the default font on Windows.
			# print metrics
		except:
			self.line_height = line_height # was 17 + 2
			g.es("exception setting outline line height")
			g.es_exception()
	#@nonl
	#@-node:ekr.20031218072017.4153:setLineHeight
	#@+node:ekr.20031218072017.4154:setTreeColorsFromConfig
	def setTreeColorsFromConfig (self):
	
		bg = g.app.config.getWindowPref("outline_pane_background_color")
		if bg:
			try: self.canvas.configure(bg=bg)
			except: pass
	#@-node:ekr.20031218072017.4154:setTreeColorsFromConfig
	#@-node:ekr.20031218072017.4150:Config & Measuring
	#@+node:ekr.20031218072017.2336:Event handers (tree)
	#@+at 
	#@nonl
	# Important note: most hooks are created in the vnode callback routines, 
	# _not_ here.
	#@-at
	#@+node:ekr.20031218072017.2337:OnActivate
	def OnActivate (self,p,event=None):
	
		try:
			c = self.c ; gui = g.app.gui
			#@		<< activate this window >>
			#@+node:ekr.20031218072017.2338:<< activate this window >>
			current = c.currentPosition()
			
			if p == current:
				if self.active:
					self.editLabel(p)
				else:
					self.undimEditLabel()
					gui.set_focus(c,self.canvas) # Essential for proper editing.
			else:
				self.select(p)
				g.app.findFrame.handleUserClick(p) # 4/3/04
				if p.v.t.insertSpot != None: # 9/1/02
					c.frame.bodyCtrl.mark_set("insert",p.v.t.insertSpot)
					c.frame.bodyCtrl.see(p.v.t.insertSpot)
				else:
					c.frame.bodyCtrl.mark_set("insert","1.0")
				gui.set_focus(c,c.frame.bodyCtrl)
			
			self.active = true
			#@nonl
			#@-node:ekr.20031218072017.2338:<< activate this window >>
			#@nl
		except:
			g.es_event_exception("activate tree")
	#@nonl
	#@-node:ekr.20031218072017.2337:OnActivate
	#@+node:ekr.20031218072017.2339:OnBoxClick
	# Called on click in box and double-click in headline.
	
	def OnBoxClick (self,p):
		
		# g.trace(p)
	
		# Note: "boxclick" hooks handled by vnode callback routine.
		c = self.c ; gui = g.app.gui
	
		if p.isExpanded(): p.contract()
		else:              p.expand()
	
		self.active = true
		self.select(p)
		g.app.findFrame.handleUserClick(p) # 4/3/04
		gui.set_focus(c,c.frame.bodyCtrl) # 7/12/03
		self.redraw()
	#@nonl
	#@-node:ekr.20031218072017.2339:OnBoxClick
	#@+node:ekr.20031218072017.2340:tree.OnDeactivate (caused double-click problem)
	def OnDeactivate (self,event=None):
		
		"""Deactivate the tree pane, dimming any headline being edited."""
	
		tree = self ; c = self.c
		focus = g.app.gui.get_focus(c.frame)
	
		# Bug fix: 7/13/03: Only do this as needed.
		# Doing this on every click would interfere with the double-clicking.
		if not c.frame.log.hasFocus() and focus != c.frame.bodyCtrl:
			try:
				# g.trace(focus)
				tree.endEditLabel()
				tree.dimEditLabel()
			except:
				g.es_event_exception("deactivate tree")
	#@nonl
	#@-node:ekr.20031218072017.2340:tree.OnDeactivate (caused double-click problem)
	#@+node:ekr.20031218072017.2341:tree.findVnodeWithIconId
	def findVnodeWithIconId (self,id):
		
		# Due to an old bug, id may be a tuple.
		try:
			return self.icon_id_dict.get(id[0])
		except:
			return self.icon_id_dict.get(id)
	#@nonl
	#@-node:ekr.20031218072017.2341:tree.findVnodeWithIconId
	#@+node:ekr.20031218072017.2342:tree.OnContinueDrag
	def OnContinueDrag(self,p,event):
	
		try:
			#@		<< continue dragging >>
			#@+node:ekr.20031218072017.2343:<< continue dragging >>
			# g.trace(p)
			assert(p == self.drag_p)
			
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
				#@+node:ekr.20031218072017.2344:<< scroll the canvas as needed >>
				# Scroll the screen up or down one line if the cursor (y) is outside the canvas.
				h = canvas.winfo_height()
				if y < 0 or y > h:
					lo, hi = frame.treeBar.get()
					n = self.savedNumberOfVisibleNodes
					line_frac = 1.0 / float(n)
					frac = g.choose(y < 0, lo - line_frac, lo + line_frac)
					frac = min(frac,1.0)
					frac = max(frac,0.0)
					# g.es("lo,hi,frac:",lo,hi,frac)
					canvas.yview("moveto", frac)
					
					# Queue up another event to keep scrolling while the cursor is outside the canvas.
					lo, hi = frame.treeBar.get()
					if (y < 0 and lo > 0.1) or (y > h and hi < 0.9):
						canvas.after_idle(self.OnContinueDrag,p,None) # Don't propagate the event.
				#@nonl
				#@-node:ekr.20031218072017.2344:<< scroll the canvas as needed >>
				#@nl
			#@nonl
			#@-node:ekr.20031218072017.2343:<< continue dragging >>
			#@nl
		except:
			g.es_event_exception("continue drag")
	#@nonl
	#@-node:ekr.20031218072017.2342:tree.OnContinueDrag
	#@+node:ekr.20031218072017.2345:tree.OnCtontrolT
	# This works around an apparent Tk bug.
	
	def OnControlT (self,event=None):
	
		# If we don't inhibit further processing the Tx.Text widget switches characters!
		return "break"
	#@nonl
	#@-node:ekr.20031218072017.2345:tree.OnCtontrolT
	#@+node:ekr.20031218072017.1776:tree.OnDrag
	# This precomputes numberOfVisibleNodes(), a significant optimization.
	# We also indicate where findVnodeWithIconId() should start looking for tree id's.
	
	def OnDrag(self,p,event):
	
		# Note: "drag" hooks handled by vnode callback routine.
	
		c = self.c ; v = p.v
		assert(p == self.drag_p)
	
		if not event:
			return
	
		if not self.dragging():
			windowPref = g.app.config.getBoolWindowPref
			# Only do this once: greatly speeds drags.
			self.savedNumberOfVisibleNodes = self.numberOfVisibleNodes()
			self.setDragging(true)
			if windowPref("allow_clone_drags"):
				self.controlDrag = c.frame.controlKeyIsDown
				if windowPref("look_for_control_drag_on_mouse_down"):
					if windowPref("enable_drag_messages"):
						if self.controlDrag:
							g.es("dragged node will be cloned")
						else:
							g.es("dragged node will be moved")
			else: self.controlDrag = false
			self.canvas['cursor'] = "hand2" # "center_ptr"
	
		self.OnContinueDrag(p,event)
	#@nonl
	#@-node:ekr.20031218072017.1776:tree.OnDrag
	#@+node:ekr.20031218072017.1777:tree.OnEndDrag
	def OnEndDrag(self,p,event):
		
		"""Tree end-of-drag handler called from vnode event handler."""
		
		v = p.v
		
		# 7/10/03: Make sure we are still dragging.
		if not self.drag_p:
			return
	
		assert(p == self.drag_p)
		c = self.c ; canvas = self.canvas ; config = g.app.config
	
		if event:
			#@		<< set vdrag, childFlag >>
			#@+node:ekr.20031218072017.1778:<< set vdrag, childFlag >>
			x,y = event.x,event.y
			canvas_x = canvas.canvasx(x)
			canvas_y = canvas.canvasy(y)
			
			id = self.canvas.find_closest(canvas_x,canvas_y)
			vdrag = self.findVnodeWithIconId(id)
			childFlag = vdrag and vdrag.hasChildren() and vdrag.isExpanded()
			#@nonl
			#@-node:ekr.20031218072017.1778:<< set vdrag, childFlag >>
			#@nl
			if config.getBoolWindowPref("allow_clone_drags"):
				if not config.getBoolWindowPref("look_for_control_drag_on_mouse_down"):
					self.controlDrag = c.frame.controlKeyIsDown
	
			if vdrag and vdrag != p:
				if self.controlDrag: # Clone p and move the clone.
					if childFlag:
						c.dragCloneToNthChildOf(p,vdrag,0)
					else:
						c.dragCloneAfter(p,vdrag)
				else: # Just drag p.
					if childFlag:
						c.dragToNthChildOf(p,vdrag,0)
					else:
						c.dragAfter(p,vdrag)
			else:
				if p and self.dragging():
					pass # g.es("not dragged: " + p.headString())
				if 0: # Don't undo the scrolling we just did!
					self.idle_scrollTo(p)
		
		# 1216/02: Reset the old cursor by brute force.
		self.canvas['cursor'] = "arrow"
	
		if self.drag_id:
			canvas.tag_unbind(self.drag_id,"<B1-Motion>")
			canvas.tag_unbind(self.drag_id,"<Any-ButtonRelease-1>")
			self.drag_id = None
			
		self.setDragging(false)
		self.drag_p = None
	#@nonl
	#@-node:ekr.20031218072017.1777:tree.OnEndDrag
	#@+node:ekr.20031218072017.1332:headline key handlers (tree)
	#@+at 
	#@nonl
	# The <Key> event generates the event before the headline text is 
	# changed(!), so we register an idle-event handler to do the work later.
	#@-at
	#@@c
	
	#@+others
	#@+node:ekr.20031218072017.1333:onHeadChanged
	def onHeadChanged (self,p):
		
		"""Handle a change to headline text."""
	
		self.c.frame.bodyCtrl.after_idle(self.idle_head_key,p)
	#@nonl
	#@-node:ekr.20031218072017.1333:onHeadChanged
	#@+node:ekr.20031218072017.1334:OnHeadlineKey
	def OnHeadlineKey (self,p,event):
		
		"""Handle a key event in a headline."""
	
		ch = event.char
		self.c.frame.bodyCtrl.after_idle(self.idle_head_key,p,ch)
	
	#@-node:ekr.20031218072017.1334:OnHeadlineKey
	#@+node:ekr.20031218072017.1335:idle_head_key
	def idle_head_key (self,p,ch=None):
		
		"""Update headline text at idle time."""
	
		c = self.c ; v = p.v
	
		if not p or not p.edit_text() or p != c.currentPosition():
			return "break"
			
		edit_text = p.edit_text()
	
		if g.doHook("headkey1",c=c,p=p,ch=ch):
			return "break" # The hook claims to have handled the event.
	
		#@	<< set s to the widget text >>
		#@+node:ekr.20031218072017.1336:<< set s to the widget text >>
		s = edit_text.get("1.0","end")
		s = g.toUnicode(s,g.app.tkEncoding) # 2/25/03
		
		if not s:
			s = u""
		s = s.replace('\n','')
		s = s.replace('\r','')
		# g.trace(s)
		#@-node:ekr.20031218072017.1336:<< set s to the widget text >>
		#@nl
		#@	<< set head to vnode text >>
		#@+node:ekr.20031218072017.1337:<< set head to vnode text >>
		head = p.headString()
		if head == None:
			head = u""
		head = g.toUnicode(head,"utf-8")
		#@-node:ekr.20031218072017.1337:<< set head to vnode text >>
		#@nl
		changed = s != head
		done = ch and (ch == '\r' or ch == '\n')
		if not changed and not done:
			return "break"
		if changed:
			c.undoer.setUndoParams("Change Headline",p,newText=s,oldText=head)
		index = edit_text.index("insert")
		if changed:
			#@		<< update v and all nodes joined to v >>
			#@+node:ekr.20031218072017.1338:<< update v and all nodes joined to v >>
			c.beginUpdate()
			if 1: # update...
				# Update changed bit.
				if not c.changed:
					c.setChanged(true)
				# Update all dirty bits.
				p.setDirty()
				# Update v.
				v.initHeadString(s)
				edit_text.delete("1.0","end")
				edit_text.insert("end",s)
				edit_text.mark_set("insert",index)
			c.endUpdate(false) # do not redraw now.
			#@nonl
			#@-node:ekr.20031218072017.1338:<< update v and all nodes joined to v >>
			#@nl
		#@	<< reconfigure v and all nodes joined to v >>
		#@+node:ekr.20031218072017.1339:<< reconfigure v and all nodes joined to v >>
		# Reconfigure v's headline.
		if done:
			self.setDisabledLabelState(p)
		
		edit_text.configure(width=self.headWidth(v))
		#@nonl
		#@-node:ekr.20031218072017.1339:<< reconfigure v and all nodes joined to v >>
		#@nl
		#@	<< update the screen >>
		#@+node:ekr.20031218072017.1340:<< update the screen >>
		if done:
			c.beginUpdate()
			self.endEditLabel()
			c.endUpdate()
		
		elif changed:
			# update v immediately.  Joined nodes are redrawn later by endEditLabel.
			# Redrawing the whole screen now messes up the cursor in the headline.
			self.drawIcon(p) # just redraw the icon.
		#@nonl
		#@-node:ekr.20031218072017.1340:<< update the screen >>
		#@nl
	
		g.doHook("headkey2",c=c,p=p,ch=ch)
		return "break"
	#@nonl
	#@-node:ekr.20031218072017.1335:idle_head_key
	#@-others
	#@nonl
	#@-node:ekr.20031218072017.1332:headline key handlers (tree)
	#@+node:ekr.20031218072017.2346:tree.OnIconClick & OnIconRightClick
	def OnIconClick (self,p,event):
		
		# g.trace(p)
		
		p = p.copy() # Make sure callbacks use the _present_ position.
	
		tree = self ; canvas = tree.canvas
		if event:
			canvas_x = canvas.canvasx(event.x)
			canvas_y = canvas.canvasy(event.y)
			id = canvas.find_closest(canvas_x,canvas_y)
			if id != None:
				try: id = id[0]
				except: pass
				self.drag_p = p
				self.drag_id = id
				
				# Create the bindings.
				id4 = canvas.tag_bind(id,"<B1-Motion>", p.OnDrag)
				id5 = canvas.tag_bind(id,"<Any-ButtonRelease-1>", p.OnEndDrag)
				
				# Remember the bindings so deleteBindings can delete them.
				self.tagBindings.append((id,id4,"<B1-Motion>"),)
				self.tagBindings.append((id,id5,"<Any-ButtonRelease-1>"),)
		tree.select(p)
		g.app.findFrame.handleUserClick(p) # 4/3/04
		return "break" # disable expanded box handling.
		
	def OnIconRightClick (self,p,event):
	
		self.select(p)
		g.app.findFrame.handleUserClick(p) # 4/3/04
		return "break" # disable expanded box handling.
	#@nonl
	#@-node:ekr.20031218072017.2346:tree.OnIconClick & OnIconRightClick
	#@+node:ekr.20031218072017.2348:tree.OnPopup & allies
	def OnPopup (self,p,event):
		
		"""Handle right-clicks in the outline."""
		
		# Note: "headrclick" hooks handled by vnode callback routine.
	
		if event != None:
			c = self.c
			if not g.doHook("create-popup-menu",c=c,p=p,event=event):
				self.createPopupMenu(event)
			if not g.doHook("enable-popup-menu-items",c=c,p=p,event=event):
				self.enablePopupMenuItems(p,event)
			if not g.doHook("show-popup-menu",c=c,p=p,event=event):
				self.showPopupMenu(event)
	
		return "break"
	#@nonl
	#@+node:ekr.20031218072017.2349:OnPopupFocusLost
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
		
	#@-node:ekr.20031218072017.2349:OnPopupFocusLost
	#@+node:ekr.20031218072017.2249:createPopupMenu
	def createPopupMenu (self,event):
		
		c = self.c ; frame = c.frame
		
		# If we are going to recreate it, we had better destroy it.
		if self.popupMenu:
			self.popupMenu.destroy()
			self.popupMenu = None
		
		self.popupMenu = menu = Tkinter.Menu(g.app.root, tearoff=0)
		
		# Add the Open With entries if they exist.
		if g.app.openWithTable:
			frame.menu.createMenuEntries(menu,g.app.openWithTable,openWith=1)
			table = (("-",None,None),)
			frame.menu.createMenuEntries(menu,table)
			
		#@	<< Create the menu table >>
		#@+node:ekr.20031218072017.2250:<< Create the menu table >>
		table = (
			("&Read @file Nodes",None,c.readAtFileNodes),
			("&Write @file Nodes",None,c.fileCommands.writeAtFileNodes),
			("-",None,None),
			("&Tangle","Shift+Ctrl+T",c.tangle),
			("&Untangle","Shift+Ctrl+U",c.untangle),
			("-",None,None),
			# 2/16/04: Remove shortcut for Toggle Angle Brackets command.
			("Toggle Angle &Brackets",None,c.toggleAngleBrackets),
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
		#@-node:ekr.20031218072017.2250:<< Create the menu table >>
		#@nl
		
		# 11/27/03: Don't actually set binding: it would conflict with previous.
		frame.menu.createMenuEntries(menu,table,dontBind=true)
	#@nonl
	#@-node:ekr.20031218072017.2249:createPopupMenu
	#@+node:ekr.20031218072017.2350:enablePopupMenuItems
	def enablePopupMenuItems (self,v,event):
		
		"""Enable and disable items in the popup menu."""
		
		c = self.c ; menu = self.popupMenu
	
		#@	<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		#@+node:ekr.20031218072017.2351:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		isAtFile = false
		isAtRoot = false
		
		for v2 in v.self_and_subtree_iter():
			if isAtFile and isAtRoot:
				break
			if (v2.isAtFileNode() or
				v2.isAtNorefFileNode() or
				v2.isAtAsisFileNode() or
				v2.isAtNoSentFileNode()
			):
				isAtFile = true
				
			isRoot,junk = g.is_special(v2.bodyString(),0,"@root")
			if isRoot:
				isAtRoot = true
		#@nonl
		#@-node:ekr.20031218072017.2351:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		#@nl
		isAtFile = g.choose(isAtFile,1,0)
		isAtRoot = g.choose(isAtRoot,1,0)
		canContract = v.parent() != None
		canContract = g.choose(canContract,1,0)
		
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
	#@-node:ekr.20031218072017.2350:enablePopupMenuItems
	#@+node:ekr.20031218072017.2352:showPopupMenu
	def showPopupMenu (self,event):
		
		"""Show a popup menu."""
		
		c = self.c ; menu = self.popupMenu ; gui = g.app.gui
	
		if sys.platform == "linux2": # 20-SEP-2002 DTHEIN: not needed for Windows
			menu.bind("<FocusOut>",self.OnPopupFocusLost)
		
		menu.post(event.x_root, event.y_root)
	
		# Make certain we have focus so we know when we lose it.
		# I think this is OK for all OSes.
		gui.set_focus(c,menu)
	#@nonl
	#@-node:ekr.20031218072017.2352:showPopupMenu
	#@-node:ekr.20031218072017.2348:tree.OnPopup & allies
	#@-node:ekr.20031218072017.2336:Event handers (tree)
	#@+node:ekr.20031218072017.4155:Incremental drawing
	#@+node:ekr.20031218072017.1027:allocateNodes
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
		self.updateTree(self.c.rootPosition(),root_left,root_top,0,0)
		# if self.updatedNodeCount: print "updatedNodeCount:", self.updatedNodeCount
	#@-node:ekr.20031218072017.1027:allocateNodes
	#@+node:ekr.20031218072017.1028:allocateNodesBeforeScrolling
	def allocateNodesBeforeScrolling (self, args):
		
		"""Calculate the nodes that will become visible as the result of an upcoming scroll.
	
		args is the tuple passed to the Tk.Canvas.yview method"""
	
		if not self.allocateOnlyVisibleNodes: return
	
		# print "allocateNodesBeforeScrolling:",self.redrawCount,args
	
		assert(self.visibleArea)
		assert(len(args)==2 or len(args)==3)
		kind = args[0] ; n = args[1]
		lines = 2 # Update by 2 lines to account for rounding.
		if len(args) == 2:
			assert(kind=="moveto")
			frac1,frac2 = args
			if float(n) != frac1:
				where = g.choose(n<frac1,"above","below")
				self.allocateNodes(where=where,lines=lines)
		else:
			assert(kind=="scroll")
			linesPerPage = self.canvas.winfo_height()/self.line_height + 2
			n = int(n) ; assert(abs(n)==1)
			where = g.choose(n == 1,"below","above")
			lines = g.choose(args[2] == "pages",linesPerPage,lines)
			self.allocateNodes(where=where,lines=lines)
	#@nonl
	#@-node:ekr.20031218072017.1028:allocateNodesBeforeScrolling
	#@+node:ekr.20031218072017.4156:updateNode
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
	#@-node:ekr.20031218072017.4156:updateNode
	#@+node:ekr.20031218072017.1030:setVisibleAreaToFullCanvas
	def setVisibleAreaToFullCanvas(self):
		
		if self.visibleArea:
			y1,y2 = self.visibleArea
			y2 = max(y2,y1 + self.canvas.winfo_height())
			self.visibleArea = y1,y2
	#@nonl
	#@-node:ekr.20031218072017.1030:setVisibleAreaToFullCanvas
	#@+node:ekr.20031218072017.1029:setVisibleArea
	def setVisibleArea (self,args):
	
		r1,r2 = args
		r1,r2 = float(r1),float(r2)
		# print "scroll ratios:",r1,r2
	
		try:
			s = self.canvas.cget("scrollregion")
			x1,y1,x2,y2 = g.scanf(s,"%d %d %d %d")
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
	#@-node:ekr.20031218072017.1029:setVisibleArea
	#@+node:ekr.20031218072017.1031:tree.updateTree
	def updateTree (self,v,x,y,h,level):
	
		yfirst = ylast = y
		if level==0: yfirst += 10
		while v:
			# g.trace(x,y,v)
			h = self.updateNode(v,x,y)
			y += h ; ylast = y
			if v.isExpanded() and v.firstChild():
				y = self.updateTree(v.firstChild(),x+child_indent,y,h,level+1)
			v = v.next()
		return y
	#@-node:ekr.20031218072017.1031:tree.updateTree
	#@-node:ekr.20031218072017.4155:Incremental drawing
	#@+node:ekr.20031218072017.4157:Selecting & editing (tree)
	#@+node:ekr.20031218072017.4158:dimEditLabel, undimEditLabel
	# Convenience methods so the caller doesn't have to know the present edit node.
	
	def dimEditLabel (self):
	
		p = self.c.currentPosition()
		self.setDisabledLabelState(p)
	
	def undimEditLabel (self):
	
		p = self.c.currentPosition()
		self.setSelectedLabelState(p)
	#@nonl
	#@-node:ekr.20031218072017.4158:dimEditLabel, undimEditLabel
	#@+node:ekr.20031218072017.4159:editLabel
	def editLabel (self,p):
		
		"""Start editing p.edit_text."""
		
		# g.trace(p)
	
		if self.editPosition() and p != self.editPosition():
			self.endEditLabel()
			self.frame.revertHeadline = None
			
		self.setEditPosition(p)
	
		# Start editing
		if p and p.edit_text():
			self.setNormalLabelState(p)
			self.frame.revertHeadline = p.headString()
			self.setEditPosition(p)
	#@nonl
	#@-node:ekr.20031218072017.4159:editLabel
	#@+node:ekr.20031218072017.4160:endEditLabel
	def endEditLabel (self):
		
		"""End editing for self.editText."""
	
		c = self.c ; gui = g.app.gui
		
		p = self.editPosition()
	
		if p and p.edit_text():
			self.setUnselectedLabelState(p)
			self.setEditPosition(None)
	
			# force a redraw of joined and ancestor headlines.
			self.force_redraw() 
	
		gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02
	#@nonl
	#@-node:ekr.20031218072017.4160:endEditLabel
	#@+node:ekr.20031218072017.4161:tree.expandAllAncestors
	def expandAllAncestors (self,p):
		
		redraw_flag = false
	
		for p in p.parents_iter():
			if not p.isExpanded():
				p.expand()
				redraw_flag = true
	
		return redraw_flag
	
	#@-node:ekr.20031218072017.4161:tree.expandAllAncestors
	#@+node:ekr.20031218072017.1019:tree.select
	# Warning: do not try to "optimize" this by returning if v==tree.currentVnode.
	
	def select (self,p,updateBeadList=true):
	
		if not p: return
		
		#@	<< define vars and stop editing >>
		#@+node:ekr.20031218072017.1020:<< define vars and stop editing >>
		c = self.c
		frame = c.frame ; body = frame.bodyCtrl
		
		old_p = c.currentPosition()
		
		# Unselect any previous selected but unedited label.
		self.endEditLabel()
		self.setUnselectedLabelState(old_p)
		#@nonl
		#@-node:ekr.20031218072017.1020:<< define vars and stop editing >>
		#@nl
		
		# g.trace(p)
	
		if not g.doHook("unselect1",c=c,new_v=p,old_v=old_p):
			#@		<< unselect the old node >>
			#@+node:ekr.20031218072017.1021:<< unselect the old node >> (changed in 4.2)
			# Remember the position of the scrollbar before making any changes.
			yview=body.yview()
			insertSpot = c.frame.body.getInsertionPoint()
			
			# Remember the old body text
			old_body = body.get("1.0","end")
			
			if old_p and old_p != p:
				# g.trace("different node")
				self.endEditLabel()
				self.setUnselectedLabelState(old_p)
			
			if old_p and old_p.edit_text():
				old_p.v.t.scrollBarSpot = yview
				old_p.v.t.insertSpot = insertSpot
			#@nonl
			#@-node:ekr.20031218072017.1021:<< unselect the old node >> (changed in 4.2)
			#@nl
		else: old_body = u""
	
		g.doHook("unselect2",c=c,new_v=p,old_v=old_p)
		
		if not g.doHook("select1",c=c,new_v=p,old_v=old_p):
			#@		<< select the new node >>
			#@+node:ekr.20031218072017.1022:<< select the new node >>
			frame.setWrap(p)
			
			# Delete only if necessary: this may reduce flicker slightly.
			s = p.v.t.bodyString
			s = g.toUnicode(s,"utf-8")
			old_body = g.toUnicode(old_body,"utf-8")
			if old_body != s:
				body.delete("1.0","end")
				body.insert("1.0",s)
				
			# We must do a full recoloring: we may be changing context!
			self.frame.body.recolor_now(p)
			
			if p.v and p.v.t.scrollBarSpot != None:
				first,last = p.v.t.scrollBarSpot
				body.yview("moveto",first)
			
			if p.v.t.insertSpot != None: # 9/21/02: moved from c.selectVnode
				c.frame.bodyCtrl.mark_set("insert",p.v.t.insertSpot)
				c.frame.bodyCtrl.see(p.v.t.insertSpot)
			else:
				c.frame.bodyCtrl.mark_set("insert","1.0")
			#@nonl
			#@-node:ekr.20031218072017.1022:<< select the new node >>
			#@nl
			if p and p != old_p: # 3/26/03: Suppress duplicate call.
				try: # may fail during initialization
					self.idle_scrollTo(p)
				except: pass
			#@		<< update c.beadList or c.beadPointer >>
			#@+node:ekr.20031218072017.1023:<< update c.beadList or c.beadPointer >>
			if updateBeadList:
				
				if c.beadPointer > -1:
					present_p = c.beadList[c.beadPointer]
				else:
					present_p = c.nullPosition()
				
				if p != present_p:
					# Replace the tail of c.beadList by c and make c the present node.
					# print "updating c.beadList"
					c.beadPointer += 1
					c.beadList[c.beadPointer:] = []
					c.beadList.append(p)
					
				# g.trace(c.beadPointer,p,present_p)
			#@nonl
			#@-node:ekr.20031218072017.1023:<< update c.beadList or c.beadPointer >>
			#@nl
			#@		<< update c.visitedList >>
			#@+node:ekr.20031218072017.1024:<< update c.visitedList >>
			# Make p the most recently visited position on the list.
			if p in c.visitedList:
				c.visitedList.remove(p)
			
			c.visitedList.insert(0,p)
			#@nonl
			#@-node:ekr.20031218072017.1024:<< update c.visitedList >>
			#@nl
	
		#@	<< set the current node >>
		#@+node:ekr.20031218072017.1025:<< set the current node >>
		self.c.setCurrentPosition(p)
		self.setSelectedLabelState(p)
		self.frame.scanForTabWidth(p) #GS I believe this should also get into the select1 hook
		g.app.gui.set_focus(c,c.frame.bodyCtrl)
		#@nonl
		#@-node:ekr.20031218072017.1025:<< set the current node >>
		#@nl
		
		g.doHook("select2",c=c,new_v=p,old_v=old_p)
		g.doHook("select3",c=c,new_v=p,old_v=old_p)
	#@nonl
	#@-node:ekr.20031218072017.1019:tree.select
	#@+node:ekr.20031218072017.4162:tree.set...LabelState
	def setNormalLabelState (self,p): # selected, editing
	
		# g.trace(p)
		if p and p.edit_text():
			#@		<< set editing headline colors >>
			#@+node:ekr.20031218072017.4163:<< set editing headline colors >>
			config = g.app.config
			fg   = config.getWindowPref("headline_text_editing_foreground_color")
			bg   = config.getWindowPref("headline_text_editing_background_color")
			selfg = config.getWindowPref("headline_text_editing_selection_foreground_color")
			selbg = config.getWindowPref("headline_text_editing_selection_background_color")
			
			if not fg or not bg:
				fg,bg = "black","white"
			
			try:
				if selfg and selbg:
					p.edit_text().configure(
						selectforeground=selfg,selectbackground=selbg,
						state="normal",highlightthickness=1,fg=fg,bg=bg)
				else:
					p.edit_text().configure(
						state="normal",highlightthickness=1,fg=fg,bg=bg)
			except:
				g.es_exception()
			#@nonl
			#@-node:ekr.20031218072017.4163:<< set editing headline colors >>
			#@nl
			p.edit_text().tag_remove("sel","1.0","end")
			p.edit_text().tag_add("sel","1.0","end")
			g.app.gui.set_focus(self.c,p.edit_text())
	
	def setDisabledLabelState (self,p): # selected, disabled
	
		# g.trace(p,g.callerName(2),g.callerName(3))
		if p and p.edit_text():
			#@		<< set selected, disabled headline colors >>
			#@+node:ekr.20031218072017.4164:<< set selected, disabled headline colors >>
			config = g.app.config
			fg = config.getWindowPref("headline_text_selected_foreground_color")
			bg = config.getWindowPref("headline_text_selected_background_color")
			
			if not fg or not bg:
				fg,bg = "black","gray80"
			
			try:
				p.edit_text().configure(
					state="disabled",highlightthickness=0,fg=fg,bg=bg)
			except:
				g.es_exception()
			#@nonl
			#@-node:ekr.20031218072017.4164:<< set selected, disabled headline colors >>
			#@nl
	
	def setSelectedLabelState (self,p): # selected, not editing
	
		# g.trace(p)
		self.setDisabledLabelState(p)
	
	def setUnselectedLabelState (self,p): # not selected.
	
		# g.trace(p)
		if p and p.edit_text():
			#@		<< set unselected headline colors >>
			#@+node:ekr.20031218072017.4165:<< set unselected headline colors >>
			config = g.app.config
			fg = config.getWindowPref("headline_text_unselected_foreground_color")
			bg = config.getWindowPref("headline_text_unselected_background_color")
			
			if not fg or not bg:
				fg,bg = "black","white"
			
			try:
				p.edit_text().configure(
					state="disabled",highlightthickness=0,fg=fg,bg=bg)
			except:
				g.es_exception()
			#@nonl
			#@-node:ekr.20031218072017.4165:<< set unselected headline colors >>
			#@nl
	#@-node:ekr.20031218072017.4162:tree.set...LabelState
	#@-node:ekr.20031218072017.4157:Selecting & editing (tree)
	#@+node:ekr.20031218072017.1141:tree.moveUpDown
	def OnUpKey   (self,event=None): return self.moveUpDown("up")
	def OnDownKey (self,event=None): return self.moveUpDown("down")
	
	def moveUpDown (self,upOrDown):
		c = self.c ; body = c.frame.bodyCtrl
		# Make the insertion cursor visible so bbox won't return an empty list.
		body.see("insert")
		# Find the coordinates of the cursor and set the new height.
		# There may be roundoff errors because character postions may not match exactly.
		ins =  body.index("insert")
		lines,char = g.scanf(ins,"%d.%d")
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
		# g.trace("entry:  %s.%s" % (lines,char))
		# g.trace("result:",result)
		# g.trace("insert:",body.index("insert"))
		return "break" # Inhibit further bindings.
	#@nonl
	#@-node:ekr.20031218072017.1141:tree.moveUpDown
	#@-others
#@nonl
#@-node:ekr.20031218072017.4138:@file-thin leoTkinterTree.py
#@-leo
