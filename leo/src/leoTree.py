#@+leo
#@+node:0::@file leoTree.py
#@+body
#@@language python


#@<< about the tree classes >>
#@+node:1::<< about the tree classes >>
#@+body
#@+at
#  This class implements a tree control similar to Windows explorer.  The draw 
# code is based on code found in Python's IDLE program.  Thank you Guido van Rossum!
# 
# The tree class knows about vnodes.  The vnode class could be split into a 
# base class (say a treeItem class) containing the ivars known to the tree 
# class, and a derived class containing everything else, including, e.g., the 
# bodyString ivar.  I haven't chosen to split the vnode class this way because 
# nothing would be gained in Leo.

#@-at
#@-body
#@-node:1::<< about the tree classes >>


from leoGlobals import *
import leoColor
import os,string,Tkinter,tkFont,types


#@<< about drawing and events >>
#@+node:2::<< About drawing and events >>
#@+body
#@+at
#  Leo must redraw the outline pane when commands are executed and as the 
# result of mouse and keyboard events.  The main challenges are eliminating 
# flicker and handling events properly.  These topics are interrelated.
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
# 
# Handling events. Besides redrawing the screen, Leo must handle events or 
# commands that change the text in the outline or body panes.  It is 
# surprisingly difficult to ensure that headline and body text corresponds to 
# the vnode and tnode corresponding to presently selected outline, and vice 
# versa. For example, when the user selects a new headline in the outline 
# pane, we must ensure that 1) the vnode and tnode of the previously selected 
# node have up-to-date information and 2) the body pane is loaded from the 
# correct data in the corresponding tnode.  Early versions of Leo attempted to 
# satisfy these conditions when the user switched outline nodes.  Such 
# attempts never worked well; there were too many special cases.  Later 
# versions of Leo, including leo.py, use a much more direct approach.  The 
# event handlers make sure that the vnode and tnode corresponding to the 
# presently selected node are always kept up-to-date.  In particular, every 
# keystroke in the body pane causes the presently selected tnode to be updated 
# immediately.  There is no longer any need for the c.synchVnode method, 
# though that method still exists for compatibility with old scripts.
# 
# The leoTree class contains all the event handlers for the body and outline 
# panes.  The actual work is done in the idle_head_key and idle_body_key 
# methods.  These routines are surprisingly complex; they must handle all the 
# tasks mentioned above, as well as others. The idle_head_key and 
# idle_body_key methods should not be called outside the leoTree class.  
# However, it often happens that code that handles user commands must simulate 
# an event.  That is, the code needs to indicate that headline or body text 
# has changed so that the screen may be redrawn properly.   The leoTree class 
# defines the following simplified event handlers: onBodyChanged, 
# onBodyWillChange, onBodyKey, onHeadChanged and onHeadlineKey.  Commanders 
# and subcommanders call these event handlers to indicate that a command has 
# changed, or will change, the headline or body text.  Calling event handlers 
# rather than c.beginUpdate and c.endUpdate ensures that the outline pane is 
# redrawn only when needed.

#@-at
#@-body
#@-node:2::<< About drawing and events >>


#@<< drawing constants >>
#@+node:3::<< drawing constants >>
#@+body
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
#@-body
#@-node:3::<< drawing constants >>


class baseLeoTree:
	"""The base class of the Leo's tree class."""

	#@+others
	#@+node:4::Birth & death
	#@+node:1::tree.__init__
	#@+body
	def __init__(self,commands,canvas):
	
		# Objects associated with this tree.
		self.colorizer = leoColor.colorizer(commands)
		self.commands = commands
		self.canvas = canvas
		self.rootVnode = None
		self.topVnode = None
		
		# Miscellaneous info.
		self.iconimages = {} # Image cache set by getIconImage().
		self.active = false # true if tree is active
		self.revertHeadline = None # Previous headline text for abortEditLabel.
		
		# Set self.font and self.fontName.
		self.setFontFromConfig()
		
		# Recycling bindings.
		self.bindings = [] # List of bindings to be unbound when redrawing.
		self.tagBindings = [] # List of tag bindings to be unbound when redrawing.
		self.icon_id_dict = {} # New in 3.12: keys are icon id's, values are vnodes.
		self.edit_text_dict = {} # New in 3.12: keys vnodes, values are edit_text (Tk.Text widgets)
		self.widgets = [] # Widgets that must be destroyed when redrawing.
	
		# Controlling redraws
		self.updateCount = 0 # self.redraw does nothing unless this is zero.
		self.redrawCount = 0 # For traces
		self.redrawScheduled = false # true if redraw scheduled.
	
		# Selection ivars.
		self.currentVnode = None # The presently selected vnode.
		self.editVnode = None # The vnode being edited.
		self.initing = false # true: opening file.
		
		# Drag and drop
		self.dragging = false # true: presently dragging.
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
			self.commands.frame.bar1.bind("<B1-ButtonRelease>", self.redraw)
	#@-body
	#@-node:1::tree.__init__
	#@+node:2::tree.deleteBindings
	#@+body
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
	#@-body
	#@-node:2::tree.deleteBindings
	#@+node:3::tree.deleteWidgets
	#@+body
	# canvas.delete("all") does _not_ delete the Tkinter objects associated with those objects!
	
	def deleteWidgets (self):
		
		"""Delete all widgets in the canvas"""
		
		self.icon_id_dict = {} # Delete all references to icons.
		self.edit_text_dict = {} # Delete all references to Tk.Edit widgets.
			
		# Fixes a _huge_ memory leak.
		for w in self.widgets:
			w.destroy() 
		self.widgets = []
	#@-body
	#@-node:3::tree.deleteWidgets
	#@-node:4::Birth & death
	#@+node:5::Drawing
	#@+node:1::About drawing and updating
	#@+body
	#@+at
	#  About drawing and updating strategy.
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
	#@-body
	#@-node:1::About drawing and updating
	#@+node:2::beginUpdate
	#@+body
	def beginUpdate (self):
	
		self.updateCount += 1
	#@-body
	#@-node:2::beginUpdate
	#@+node:3::drawBox (tag_bind)
	#@+body
	def drawBox (self,v,x,y):
		
		y += 7 # draw the box at x, y+7
	
		iconname = choose(v.isExpanded(),"minusnode.gif", "plusnode.gif")
		image = self.getIconImage(iconname)
		id = self.canvas.create_image(x,y,image=image)
	
		id1 = self.canvas.tag_bind(id, "<1>", v.OnBoxClick)
		id2 = self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
		
		# Remember the bindings so deleteBindings can delete them.
		self.tagBindings.append((id,id1,"<1>"),)
		self.tagBindings.append((id,id2,"<Double-1>"),)
	
	#@-body
	#@-node:3::drawBox (tag_bind)
	#@+node:4::drawIcon (tag_bind)
	#@+body
	# Draws icon for v at x,y
	
	def drawIcon(self,v,x,y):
	
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
	
		id1 = self.canvas.tag_bind(id,"<1>",v.OnIconClick)
		id2 = self.canvas.tag_bind(id,"<Double-1>",v.OnIconDoubleClick)
		id3 = self.canvas.tag_bind(id,"<3>",v.OnIconRightClick)
		
		# Remember the bindings so deleteBindings can delete them.
		self.tagBindings.append((id,id1,"<1>"),)
		self.tagBindings.append((id,id2,"<Double-1>"),)
		self.tagBindings.append((id,id3,"<3>"),)
	
		return 0 # dummy icon height
	
	
	#@-body
	#@-node:4::drawIcon (tag_bind)
	#@+node:5::drawNode & force_draw_node
	#@+body
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
	#@-body
	#@-node:5::drawNode & force_draw_node
	#@+node:6::drawText (bind)
	#@+body
	# draws text for v at x,y
	
	def drawText(self,v,x,y):
		
		x += text_indent
	
		t = Tkinter.Text(self.canvas,
			font=self.font,bd=0,relief="flat",width=self.headWidth(v),height=1)
		self.edit_text_dict[v] = t # Remember which text widget belongs to v.
		
		# Remember the widget so deleteBindings can delete it.
		self.widgets.append(t) # Fixes a _huge_ memory leak.
	
		t.insert("end", v.headString())
		
		#@<< configure the text depending on state >>
		#@+node:1::<< configure the text depending on state >>
		#@+body
		if v == self.currentVnode:
			# trace("editVnode",self.editVnode)
			if v == self.editVnode:
				self.setNormalLabelState(v) # 7/7/03
			else:
				self.setDisabledLabelState(v) # selected, disabled
		else:
			self.setUnselectedLabelState(v) # unselected
		#@-body
		#@-node:1::<< configure the text depending on state >>

	
		id1 = t.bind("<1>", v.OnHeadlineClick)
		id2 = t.bind("<3>", v.OnHeadlineRightClick) # 9/11/02.
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
	#@-body
	#@-node:6::drawText (bind)
	#@+node:7::drawTree
	#@+body
	def drawTree(self,v,x,y,h,level):
		
		# Recursive routine, stat() not useful.
		yfirst = ylast = y
		if level==0: yfirst += 10
		while v:
			# trace(`x` + ", " + `y` + ", " + `v`)
			h = self.drawNode(v,x,y)
			y += h ; ylast = y
			if v.isExpanded() and v.firstChild():
				y = self.drawTree(v.firstChild(),x+child_indent,y,h,level+1)
			v = v.next()
		
		#@<< draw vertical line >>
		#@+node:1::<< draw vertical line >>
		#@+body
		id = self.canvas.create_line(
			x, yfirst-hline_y+4,
			x, ylast+hline_y-h,
			fill="gray50", # stipple="gray50"
			tag="lines")
		
		self.canvas.tag_lower(id)
		#@-body
		#@-node:1::<< draw vertical line >>

		return y
	#@-body
	#@-node:7::drawTree
	#@+node:8::endUpdate
	#@+body
	def endUpdate (self, flag=true):
	
		assert(self.updateCount > 0)
		self.updateCount -= 1
		if flag and self.updateCount == 0:
			self.redraw()
	#@-body
	#@-node:8::endUpdate
	#@+node:9::headWidth
	#@+body
	#@+at
	#  Returns the proper width of the entry widget for the headline. This has 
	# been a problem.

	#@-at
	#@@c

	def headWidth(self,v):
	
		return max(10,5 + len(v.headString()))
	#@-body
	#@-node:9::headWidth
	#@+node:10::inVisibleArea & inExpandedVisibleArea
	#@+body
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
	#@-body
	#@-node:10::inVisibleArea & inExpandedVisibleArea
	#@+node:11::lastVisible
	#@+body
	# Returns the last visible node of the screen.
	
	def lastVisible (self):
	
		v = self.rootVnode
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
	#@-body
	#@-node:11::lastVisible
	#@+node:12::Drawing routines (tree)...
	#@+node:1::redraw
	#@+body
	# Calling redraw inside c.beginUpdate()/c.endUpdate() does nothing.
	# This _is_ useful when a flag is passed to c.endUpdate.
	
	def redraw (self,event=None):
		
		if self.updateCount == 0 and not self.redrawScheduled:
			# stat() # print "tree.redraw"
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
			
	
	#@-body
	#@-node:1::redraw
	#@+node:2::force_redraw
	#@+body
	# Schedules a redraw even if inside beginUpdate/endUpdate
	def force_redraw (self):
		# print "tree.force_redraw"
		if not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
			
	
	#@-body
	#@-node:2::force_redraw
	#@+node:3::redraw_now
	#@+body
	# Redraws immediately: used by Find so a redraw doesn't mess up selections.
	# It is up to the caller to ensure that no other redraws are pending.
	def redraw_now (self):
	
		# trace(`self.redrawScheduled`)
		self.idle_redraw()
	#@-body
	#@-node:3::redraw_now
	#@+node:4::idle_redraw
	#@+body
	def idle_redraw (self):
	
		frame = self.commands.frame
		if frame not in app().windowList or app().quitting:
			return
			
		# trace("*" * 40)
	
		self.expandAllAncestors(self.currentVnode)
		oldcursor = self.canvas['cursor']
		self.canvas['cursor'] = "watch"
		self.allocatedNodes = 0
		if not doHook("redraw-entire-outline",c=self.commands):
			# Erase and redraw the entire tree.
			self.topVnode = None
			self.deleteBindings()
			self.canvas.delete("all")
			self.deleteWidgets()
			self.setVisibleAreaToFullCanvas()
			self.drawTree(self.rootVnode,root_left,root_top,0,0)
			# Set up the scroll region after the tree has been redrawn.
			x0, y0, x1, y1 = self.canvas.bbox("all")
			self.canvas.configure(scrollregion=(0, 0, x1, y1))
			# Do a scrolling operation after the scrollbar is redrawn
			self.canvas.after_idle(self.idle_scrollTo)
			if self.trace:
				self.redrawCount += 1
				print "idle_redraw allocated:",self.redrawCount, self.allocatedNodes
			doHook("after_redraw-outline",c=self.commands)
	
		self.canvas['cursor'] = oldcursor
		self.redrawScheduled = false
	#@-body
	#@-node:4::idle_redraw
	#@+node:5::idle_second_redraw
	#@+body
	def idle_second_redraw (self):
		
		# trace()
			
		# Erase and redraw the entire tree the SECOND time.
		# This ensures that all visible nodes are allocated.
		self.topVnode = None
		args = self.canvas.yview()
		self.setVisibleArea(args)
		self.deleteBindings()
		self.canvas.delete("all")
		self.drawTree(self.rootVnode,root_left,root_top,0,0)
		
		if self.trace:
			print "idle_second_redraw allocated:",self.redrawCount, self.allocatedNodes
	#@-body
	#@-node:5::idle_second_redraw
	#@-node:12::Drawing routines (tree)...
	#@+node:13::setLineHeight
	#@+body
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
	#@-body
	#@-node:13::setLineHeight
	#@+node:14::tree.getFont,setFont,setFontFromConfig
	#@+body
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
	
		font = app().config.getFontFromParams(
			"headline_text_font_family", "headline_text_font_size",
			"headline_text_font_slant",  "headline_text_font_weight")
	
		self.setFont(font)
	#@-body
	#@-node:14::tree.getFont,setFont,setFontFromConfig
	#@+node:15::tree.getIconImage
	#@+body
	def getIconImage (self, name):
	
		# Return the image from the cache if possible.
		if self.iconimages.has_key(name):
			return self.iconimages[name]
			
		try:
			fullname = os.path.join(app().loadDir,"..","Icons",name)
			fullname = os.path.normpath(fullname)
			image = Tkinter.PhotoImage(master=self.canvas, file=fullname)
			self.iconimages[name] = image
			return image
		except:
			es("Exception loading: " + fullname)
			es_exception()
			return None
	#@-body
	#@-node:15::tree.getIconImage
	#@+node:16::tree.idle_scrollTo
	#@+body
	#@+at
	#  This scrolls the canvas so that v is in view.  This is done at idle 
	# time after a redraw so that treeBar.get() will return proper values.

	#@-at
	#@@c

	def idle_scrollTo(self,v=None):
	
		frame = self.commands.frame
		last = self.lastVisible()
		nextToLast = last.visBack()
		# print 'v,last',`v`,`last`
		if v == None:
			v = self.currentVnode
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
	#@-body
	#@-node:16::tree.idle_scrollTo
	#@+node:17::tree.numberOfVisibleNodes
	#@+body
	def numberOfVisibleNodes(self):
		
		n = 0 ; v = self.rootVnode
		while v:
			n += 1
			v = v.visNext()
		return n
	#@-body
	#@-node:17::tree.numberOfVisibleNodes
	#@+node:18::tree.recolor, recolor_now, recolor_range
	#@+body
	def recolor(self,v,incremental=0):
	
		body = self.commands.frame.body
		
		if 0: # Do immediately
			self.colorizer.colorize(v,body,incremental)
		else: # Do at idle time
			self.colorizer.schedule(v,body,incremental)
	
	def recolor_now(self,v,incremental=0):
	
		body = self.commands.frame.body
		self.colorizer.colorize(v,body,incremental)
		
	def recolor_range(self,v,leading,trailing):
	
		body = self.commands.frame.body
		self.colorizer.recolor_range(v,body,leading,trailing)
	#@-body
	#@-node:18::tree.recolor, recolor_now, recolor_range
	#@+node:19::tree.yoffset
	#@+body
	#@+at
	#  We can't just return icony because the tree hasn't been redrawn yet.  
	# For the same reason we can't rely on any TK canvas methods here.

	#@-at
	#@@c

	def yoffset(self, v1):
	
		# if not v1.isVisible(): print "yoffset not visible:", `v1`
		root = self.rootVnode
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
	#@-body
	#@-node:19::tree.yoffset
	#@-node:5::Drawing
	#@+node:6::Event handers (tree)
	#@+body
	#@+at
	#  Important note: most hooks are created in the vnode callback routines, 
	# _not_ here.

	#@-at
	#@-body
	#@+node:1::OnActivate
	#@+body
	def OnActivate (self,v,event=None):
	
		try:
			c = self.commands
			
			#@<< activate this window >>
			#@+node:1::<< activate this window >>
			#@+body
			c=self.commands
			# trace(`v`)
			
			if v == self.currentVnode:
				# w = self.commands.frame.getFocus()
				if self.active:
					self.editLabel(v)
				else:
					self.undimEditLabel()
					set_focus(self.canvas)
			else:
				self.select(v)
				if v.t.insertSpot != None: # 9/1/02
					c.body.mark_set("insert",v.t.insertSpot)
					c.body.see(v.t.insertSpot)
				else:
					c.body.mark_set("insert","1.0")
				set_focus(c.body)
			
			self.active = true
			#@-body
			#@-node:1::<< activate this window >>

		except:
			es_event_exception("activate tree")
	#@-body
	#@-node:1::OnActivate
	#@+node:2::OnBoxClick
	#@+body
	# Called on click in box and double-click in headline.
	
	def OnBoxClick (self,v):
	
		# Note: "boxclick" hooks handled by vnode callback routine.
	
		if v.isExpanded():
			v.contract()
		else:
			v.expand()
	
		self.active = true
		self.select(v)
		set_focus(self.canvas) # This is safe.
		self.redraw()
	#@-body
	#@-node:2::OnBoxClick
	#@+node:3::OnDeactivate
	#@+body
	def OnDeactivate (self,event=None):
	
		try:
			self.endEditLabel()
			self.dimEditLabel()
			self.active = false
		except:
			es_event_exception("deactivate tree")
	#@-body
	#@-node:3::OnDeactivate
	#@+node:4::tree.findVnodeWithIconId
	#@+body
	def findVnodeWithIconId (self,id):
		
		# Due to an old bug, id may be a tuple.
		try:
			return self.icon_id_dict.get(id[0])
		except:
			return self.icon_id_dict.get(id)
	
	#@-body
	#@-node:4::tree.findVnodeWithIconId
	#@+node:5::body key handlers (tree)
	#@+body
	#@+at
	#  The <Key> event generates the event before the body text is changed(!), 
	# so we register an idle-event handler to do the work later.
	# 
	# 1/17/02: Rather than trying to figure out whether the control or alt 
	# keys are down, we always schedule the idle_handler.  The idle_handler 
	# sees if any change has, in fact, been made to the body text, and sets 
	# the changed and dirty bits only if so.  This is the clean and safe way.
	# 
	# 2/19/02: We must distinguish between commands like "Find, Then Change", 
	# that call onBodyChanged, and commands like "Cut" and "Paste" that call 
	# onBodyWillChange.  The former commands have already changed the body 
	# text, and that change must be captured immediately.  The latter commands 
	# have not changed the body text, and that change may only be captured at 
	# idle time.

	#@-at
	#@@c


	#@+others
	#@+node:1::idle_body_key
	#@+body
	def idle_body_key (self,v,oldSel,undoType,ch=None,oldYview=None,newSel=None):
		
		"""Update the body pane at idle time."""
	
		c = self.commands
		if not c or not v or v != c.currentVnode():
			return "break"
		if doHook("bodykey1",c=c,v=v,ch=ch,oldSel=oldSel,undoType=undoType):
			return "break" # The hook claims to have handled the event.
		body = v.bodyString()
		if not newSel:
			newSel = getTextSelection(c.body)
		
		#@<< set s to the widget text >>
		#@+node:1::<< set s to the widget text >>
		#@+body
		s = c.body.get("1.0", "end")
		
		if s == None:
			s = u""
		
		if type(s) == type(""):
			s = toUnicode(s,app().tkEncoding) # 2/25/03
			# if len(ch) > 0: print `s`
		#@-body
		#@-node:1::<< set s to the widget text >>

		
		#@<< return if nothing has changed >>
		#@+node:2::<< return if nothing has changed >>
		#@+body
		# 6/22/03: Make sure we handle delete key properly.
		
		if ch not in ('\n','\r',chr(8)):
		
			if s == body:
				return "break"
			
			# Do nothing for control characters.
			if (ch == None or len(ch) == 0) and body == s[:-1]:
				return "break"
			
		# print `ch`,len(body),len(s)
		#@-body
		#@-node:2::<< return if nothing has changed >>

		
		#@<< set removeTrailing >>
		#@+node:3::<< set removeTrailing >>
		#@+body
		#@+at
		#  Tk will add a newline only if:
		# 1. A real change has been made to the Tk.Text widget, and
		# 2. the change did _not_ result in the widget already containing a newline.
		# 
		# It's not possible to tell, given the information available, what Tk 
		# has actually done. We need only make a reasonable guess here.   
		# setUndoTypingParams stores the number of trailing newlines in each 
		# undo bead, so whatever we do here can be faithfully undone and redone.

		#@-at
		#@@c
		new = s ; old = body
		
		if len(new) == 0 or new[-1] != '\n':
			# There is no newline to remove.  Probably will never happen.
			# trace("false: no newline to remove")
			removeTrailing = false
		elif len(old) == 0:
			# Ambigous case.
			# trace("false: empty old")
			removeTrailing = ch != '\n' # false
		elif old == new[:-1]:
			# A single trailing character has been added.
			# trace("false: only changed trailing.")
			removeTrailing = false
		else:
			# The text didn't have a newline, and now it does.
			# Moveover, some other change has been made to the text,
			# So at worst we have misreprented the user's intentions slightly.
			# trace("true")
			removeTrailing = true
			
		# trace(`ch`+","+`removeTrailing`)
		
		
		
		#@-body
		#@-node:3::<< set removeTrailing >>

		if ch in ('\n','\r'):
			
			#@<< Do auto indent >>
			#@+node:4::<< Do auto indent >> (David McNab)
			#@+body
			# Do nothing if we are in @nocolor mode or if we are executing a Change command.
			if self.colorizer.useSyntaxColoring(v) and undoType != "Change":
				# Get the previous line.
				s=c.body.get("insert linestart - 1 lines","insert linestart -1c")
				# Add the leading whitespace to the present line.
				junk,width = skip_leading_ws_with_indent(s,0,c.tab_width)
				if s and len(s) > 0 and s[-1]==':':
					# For Python: increase auto-indent after colons.
					if self.colorizer.scanColorDirectives(v) == "python":
						width += abs(c.tab_width)
				if app().config.getBoolWindowPref("smart_auto_indent"):
					# Added Nov 18 by David McNab, david@rebirthing.co.nz
					# Determine if prev line has unclosed parens/brackets/braces
					brackets = [width]
					tabex = 0
					for i in range(0, len(s)):
						if s[i] == '\t':
							tabex += c.tab_width - 1
						if s[i] in '([{':
							brackets.append(i+tabex + 1)
						elif s[i] in '}])' and len(brackets) > 1:
							brackets.pop()
					width = brackets.pop()
					# end patch by David McNab
				ws = computeLeadingWhitespace (width,c.tab_width)
				if ws and len(ws) > 0:
					c.body.insert("insert", ws)
					removeTrailing = false # bug fix: 11/18
			#@-body
			#@-node:4::<< Do auto indent >> (David McNab)

		elif ch == '\t' and c.tab_width < 0:
			
			#@<< convert tab to blanks >>
			#@+node:5::<< convert tab to blanks >>
			#@+body
			# Do nothing if we are executing a Change command.
			if undoType != "Change":
				
				# Get the characters preceeding the tab.
				prev=c.body.get("insert linestart","insert -1c")
				
				if 1: # 6/26/03: Convert tab no matter where it is.
			
					w = computeWidth(prev,c.tab_width)
					w2 = (abs(c.tab_width) - (w % abs(c.tab_width)))
					# print "prev w:" + `w` + ", prev chars:" + `prev`
					c.body.delete("insert -1c")
					c.body.insert("insert",' ' * w2)
				
				else: # Convert only leading tabs.
				
					# Get the characters preceeding the tab.
					prev=c.body.get("insert linestart","insert -1c")
			
					# Do nothing if there are non-whitespace in prev:
					all_ws = true
					for ch in prev:
						if ch != ' ' and ch != '\t':
							all_ws = false
					if all_ws:
						w = computeWidth(prev,c.tab_width)
						w2 = (abs(c.tab_width) - (w % abs(c.tab_width)))
						# print "prev w:" + `w` + ", prev chars:" + `prev`
						c.body.delete("insert -1c")
						c.body.insert("insert",' ' * w2)
			#@-body
			#@-node:5::<< convert tab to blanks >>

		
		#@<< set s to widget text, removing trailing newlines if necessary >>
		#@+node:6::<< set s to widget text, removing trailing newlines if necessary >>
		#@+body
		s = c.body.get("1.0", "end")
		s = toUnicode(s,app().tkEncoding) #2/25/03
		if len(s) > 0 and s[-1] == '\n' and removeTrailing:
			s = s[:-1]
		#@-body
		#@-node:6::<< set s to widget text, removing trailing newlines if necessary >>

		c.undoer.setUndoTypingParams(v,undoType,body,s,oldSel,newSel,oldYview=oldYview)
		v.t.setTnodeText(s)
		v.t.insertSpot = c.body.index("insert")
		
		#@<< recolor the body >>
		#@+node:7::<< recolor the body >>
		#@+body
		self.scanForTabWidth(v)
		incremental = undoType not in ("Cut","Paste")
		self.recolor_now(v,incremental=incremental)
		#@-body
		#@-node:7::<< recolor the body >>

		if not c.changed:
			c.setChanged(true)
		
		#@<< redraw the screen if necessary >>
		#@+node:8::<< redraw the screen if necessary >>
		#@+body
		redraw_flag = false
		
		c.beginUpdate()
		
		# Update dirty bits.
		if not v.isDirty() and v.setDirty(): # Sets all cloned and @file dirty bits
			redraw_flag = true
			
		# Update icons.
		val = v.computeIcon()
		if val != v.iconVal:
			v.iconVal = val
			redraw_flag = true
		
		c.endUpdate(redraw_flag) # redraw only if necessary
		#@-body
		#@-node:8::<< redraw the screen if necessary >>

		doHook("bodykey2",c=c,v=v,ch=ch,oldSel=oldSel,undoType=undoType)
		return "break"
	#@-body
	#@-node:1::idle_body_key
	#@+node:2::onBodyChanged
	#@+body
	# Called by command handlers that have already changed the text.
	
	def onBodyChanged (self,v,undoType,oldSel=None,oldYview=None,newSel=None):
		
		"""Handle a change to the body pane."""
		
		c = self.commands
		if not v:
			v = c.currentVnode()
	
		if not oldSel:
			oldSel = getTextSelection(c.body)
	
		self.idle_body_key(v,oldSel,undoType,oldYview=oldYview,newSel=newSel)
	
	#@-body
	#@-node:2::onBodyChanged
	#@+node:3::OnBodyKey
	#@+body
	def OnBodyKey (self,event):
		
		"""Handle any key press event in the body pane."""
	
		c = self.commands ; v = c.currentVnode() ; ch = event.char
		oldSel = getTextSelection(c.body)
		
		if 0:
			self.keyCount += 1
			if ch and len(ch)>0: print "%4d %s" % (self.keyCount,repr(ch))
			
		# We must execute this even if len(ch) > 0 to delete spurious trailing newlines.
		self.commands.body.after_idle(self.idle_body_key,v,oldSel,"Typing",ch)
	#@-body
	#@-node:3::OnBodyKey
	#@+node:4::onBodyWillChange
	#@+body
	# Called by command handlers that change the text just before idle time.
	
	def onBodyWillChange (self,v,undoType,oldSel=None,oldYview=None):
		
		"""Queue the body changed idle handler."""
		
		c = self.commands
		if not v: v = c.currentVnode()
		if not oldSel:
			oldSel = getTextSelection(c.body)
		  
		self.commands.body.after_idle(self.idle_body_key,v,oldSel,undoType,oldYview)
	
	
	#@-body
	#@-node:4::onBodyWillChange
	#@-others
	
	#@-body
	#@-node:5::body key handlers (tree)
	#@+node:6::tree.OnContinueDrag
	#@+body
	def OnContinueDrag(self,v,event):
	
		try:
			
			#@<< continue dragging >>
			#@+node:1::<< continue dragging >>
			#@+body
			# trace(`v`)
			assert(v == self.drag_v)
			
			c = self.commands 
			canvas = self.canvas
			frame = self.commands.frame
			
			if event:
				x,y = event.x,event.y
			else:
				x,y = frame.top.winfo_pointerx(),frame.top.winfo_pointery()
				if x == -1 or y == -1: return # Stop the scrolling if we go outside the entire window.
			
			canvas_x = canvas.canvasx(x)
			canvas_y = canvas.canvasy(y)
			
			id = self.canvas.find_closest(canvas_x,canvas_y)
			
			# OnEndDrag() halts the scrolling by clearing self.drag_id when the mouse button goes up.
			if self.drag_id: # This gets cleared by OnEndDrag()
				
				#@<< scroll the canvas as needed >>
				#@+node:1::<< scroll the canvas as needed >>
				#@+body
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
				#@-body
				#@-node:1::<< scroll the canvas as needed >>
			#@-body
			#@-node:1::<< continue dragging >>

		except:
			es_event_exception("continue drag")
	#@-body
	#@-node:6::tree.OnContinueDrag
	#@+node:7::tree.OnCtontrolT
	#@+body
	# This works around an apparent Tk bug.
	
	def OnControlT (self,event=None):
	
		# If we don't inhibit further processing the Tx.Text widget switches characters!
		return "break"
	#@-body
	#@-node:7::tree.OnCtontrolT
	#@+node:8::tree.OnDrag
	#@+body
	# This precomputes numberOfVisibleNodes(), a significant optimization.
	# We also indicate where findVnodeWithIconId() should start looking for tree id's.
	
	def OnDrag(self,v,event):
	
		# Note: "drag" hooks handled by vnode callback routine.
		
		c = self.commands
		assert(v == self.drag_v)
	
		if not event:
			return
	
		if not self.dragging:
			# 11/25/02: Only do this once: greatly speeds drags.
			self.savedNumberOfVisibleNodes = self.numberOfVisibleNodes()
			self.dragging = true
			self.controlDrag = c.frame.controlKeyIsDown
			# 1/29/03: support this new option.
			flag = app().config.getBoolWindowPref("look_for_control_drag_on_mouse_down")
			if flag:
				if self.controlDrag:
					es("dragged node will be cloned")
				else:
					es("dragged node will be moved")
			self.canvas['cursor'] = "hand2" # "center_ptr"
	
		self.OnContinueDrag(v,event)
	#@-body
	#@-node:8::tree.OnDrag
	#@+node:9::tree.OnEndDrag
	#@+body
	def OnEndDrag(self,v,event):
		
		# Note: "enddrag" hooks handled by vnode callback routine.
		
		# es("tree.OnEndDrag" + `v`)
		assert(v == self.drag_v)
		c = self.commands ; canvas = self.canvas
	
		if event:
			
			#@<< set vdrag, childFlag >>
			#@+node:1::<< set vdrag, childFlag >>
			#@+body
			x,y = event.x,event.y
			canvas_x = canvas.canvasx(x)
			canvas_y = canvas.canvasy(y)
			
			id = self.canvas.find_closest(canvas_x,canvas_y)
			vdrag = self.findVnodeWithIconId(id)
			childFlag = vdrag and vdrag.hasChildren() and vdrag.isExpanded()
			#@-body
			#@-node:1::<< set vdrag, childFlag >>

			# 1/29/03: support for this new option.
			flag = app().config.getBoolWindowPref("look_for_control_drag_on_mouse_down")
			if not flag:
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
				if v and self.dragging:
					pass # es("not dragged: " + v.headString())
				if 0: # Don't undo the scrolling we just did!
					self.idle_scrollTo(v)
		
		# 1216/02: Reset the old cursor by brute force.
		self.canvas['cursor'] = "arrow"
	
		if self.drag_id:
			canvas.tag_unbind(self.drag_id , "<B1-Motion>")
			canvas.tag_unbind(self.drag_id , "<Any-ButtonRelease-1>")
			self.drag_id = None
			
		self.dragging = false
	
	#@-body
	#@-node:9::tree.OnEndDrag
	#@+node:10::headline key handlers (tree)
	#@+body
	#@+at
	#  The <Key> event generates the event before the headline text is 
	# changed(!), so we register an idle-event handler to do the work later.

	#@-at
	#@@c


	#@+others
	#@+node:1::onHeadChanged
	#@+body
	def onHeadChanged (self,v):
		
		"""Handle a change to headline text."""
	
		self.commands.body.after_idle(self.idle_head_key,v)
	
	
	
	#@-body
	#@-node:1::onHeadChanged
	#@+node:2::OnHeadlineKey
	#@+body
	def OnHeadlineKey (self,v,event):
		
		"""Handle a key event in a headline."""
	
		ch = event.char
		self.commands.body.after_idle(self.idle_head_key,v,ch)
	
	
	#@-body
	#@-node:2::OnHeadlineKey
	#@+node:3::idle_head_key
	#@+body
	def idle_head_key (self,v,ch=None):
		
		"""Update headline text at idle time."""
	
		c = self.commands
		if not v or not v.edit_text() or v != c.currentVnode():
			return "break"
		if doHook("headkey1",c=c,v=v,ch=ch):
			return "break" # The hook claims to have handled the event.
	
		
		#@<< set s to the widget text >>
		#@+node:1::<< set s to the widget text >>
		#@+body
		s = v.edit_text().get("1.0","end")
		s = toUnicode(s,app().tkEncoding) # 2/25/03
		if not s:
			s = u""
		s = s.replace('\n','')
		s = s.replace('\r','')
		# trace(`s`)
		
		#@-body
		#@-node:1::<< set s to the widget text >>

		
		#@<< set head to vnode text >>
		#@+node:2::<< set head to vnode text >>
		#@+body
		head = v.headString()
		if head == None:
			head = u""
		head = toUnicode(head,"utf-8")
		
		#@-body
		#@-node:2::<< set head to vnode text >>

		changed = s != head
		done = ch and (ch == '\r' or ch == '\n')
		if not changed and not done:
			return "break"
		if changed:
			c.undoer.setUndoParams("Change Headline",v,newText=s,oldText=head)
		index = v.edit_text().index("insert")
		if changed:
			
			#@<< update v and all nodes joined to v >>
			#@+node:3::<< update v and all nodes joined to v >>
			#@+body
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
			#@-body
			#@-node:3::<< update v and all nodes joined to v >>

		
		#@<< reconfigure v and all nodes joined to v >>
		#@+node:4::<< reconfigure v and all nodes joined to v >>
		#@+body
		# Reconfigure v's headline.
		if done:
			self.setDisabledLabelState(v)
		
		v.edit_text().configure(width=self.headWidth(v))
		
		# Reconfigure all joined headlines.
		for v2 in v.t.joinList:
			if v2 != v:
				if v2.edit_text(): # v2 may not be visible
					v2.edit_text().configure(width=self.headWidth(v2))
		#@-body
		#@-node:4::<< reconfigure v and all nodes joined to v >>

		
		#@<< update the screen >>
		#@+node:5::<< update the screen >>
		#@+body
		if done:
			c.beginUpdate()
			self.endEditLabel()
			c.endUpdate()
		
		elif changed:
			# update v immediately.  Joined nodes are redrawn later by endEditLabel.
			# Redrawing the whole screen now messes up the cursor in the headline.
			self.drawIcon(v,v.iconx,v.icony) # just redraw the icon.
		#@-body
		#@-node:5::<< update the screen >>

	
		doHook("headkey2",c=c,v=v,ch=ch)
		return "break"
	#@-body
	#@-node:3::idle_head_key
	#@-others
	
	#@-body
	#@-node:10::headline key handlers (tree)
	#@+node:11::tree.OnIconClick & OnIconRightClick
	#@+body
	def OnIconClick (self,v,event):
	
		# Note: "iconclick" hooks handled by vnode callback routine.
	
		canvas = self.canvas
		if event:
			canvas_x = canvas.canvasx(event.x)
			canvas_y = canvas.canvasy(event.y)
			id = canvas.find_closest(canvas_x,canvas_y)
			if id:
				self.drag_id = id
				self.drag_v = v
				canvas.tag_bind(id,"<B1-Motion>", v.OnDrag)
				canvas.tag_bind(id,"<Any-ButtonRelease-1>", v.OnEndDrag)
		self.select(v)
		
	def OnIconRightClick (self,v,event):
	
		self.select(v)
	
	#@-body
	#@-node:11::tree.OnIconClick & OnIconRightClick
	#@+node:12::tree.OnIconDoubleClick (@url)
	#@+body
	def OnIconDoubleClick (self,v,event=None):
	
		# Note: "icondclick" hooks handled by vnode callback routine.
	
		c = self.commands
		s = v.headString().strip()
		if match_word(s,0,"@url"):
			if not doHook("@url1",c=c,v=v):
				url = s[4:].strip()
				
				#@<< stop the url after any whitespace >>
				#@+node:1::<< stop the url after any whitespace  >>
				#@+body
				# For safety, the URL string should end at the first whitespace.
				
				url = url.replace('\t',' ')
				i = url.find(' ')
				if i > -1:
					if 0: # No need for a warning.  Assume everything else is a comment.
						es("ignoring characters after space in url:"+url[i:])
						es("use %20 instead of spaces")
					url = url[:i]
				
				#@-body
				#@-node:1::<< stop the url after any whitespace  >>

				
				#@<< check the url; return if bad >>
				#@+node:2::<< check the url; return if bad >>
				#@+body
				if not url or len(url) == 0:
					es("no url following @url")
					return
					

				#@+at
				#  A valid url is (according to D.T.Hein):
				# 
				# 3 or more lowercase alphas, followed by,
				# one ':', followed by,
				# one or more of: (excludes !"#;<>[\]^`|)
				#   $%&'()*+,-./0-9:=?@A-Z_a-z{}~
				# followed by one of: (same as above, except no minus sign or comma).
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
				
				#@-body
				#@-node:2::<< check the url; return if bad >>

				
				#@<< pass the url to the web browser >>
				#@+node:3::<< pass the url to the web browser >>
				#@+body
				#@+at
				#  Most browsers should handle the following urls:
				#   ftp://ftp.uu.net/public/whatever.
				#   http://localhost/MySiteUnderDevelopment/index.html
				#   file:///home/me/todolist.html

				#@-at
				#@@c

				try:
					import os
					import webbrowser
					os.chdir(app().loadDir)
					# print "url:",url
					webbrowser.open(url)
				except:
					es("exception opening " + url)
					es_exception()
				#@-body
				#@-node:3::<< pass the url to the web browser >>

			doHook("@url2",c=c,v=v)
	#@-body
	#@-node:12::tree.OnIconDoubleClick (@url)
	#@+node:13::tree.OnPopup & allies
	#@+body
	def OnPopup (self,v,event):
		
		"""Handle right-clicks in the outline."""
		
		# Note: "headrclick" hooks handled by vnode callback routine.
	
		if event != None:
			c = self.commands
			if not doHook("create-popup-menu",c=c,v=v,event=event):
				self.createPopupMenu(v,event)
			if not doHook("enable-popup-menu-items",c=c,v=v,event=event):
				self.enablePopupMenuItems(v,event)
			if not doHook("show-popup-menu",c=c,v=v,event=event):
				self.showPopupMenu(v,event)
	
		return "break"
	#@-body
	#@+node:1::OnPopupFocusLost
	#@+body
	#@+at
	#  On Linux we must do something special to make the popup menu "unpost" 
	# if the mouse is clicked elsewhere.  So we have to catch the <FocusOut> 
	# event and explicitly unpost.  In order to process the <FocusOut> event, 
	# we need to be able to find the reference to the popup window again, so 
	# this needs to be an attribute of the tree object; hence, "self.popupMenu".
	# 
	# Aside: though Tk tries to be muli-platform, the interaction with 
	# different window managers does cause small differences that will need to 
	# be compensated by system specific application code. :-(

	#@-at
	#@@c

	# 20-SEP-2002 DTHEIN: This event handler is only needed for Linux.
	
	def OnPopupFocusLost(self,event=None):
	
		self.popupMenu.unpost()
		
	
	#@-body
	#@-node:1::OnPopupFocusLost
	#@+node:2::createPopupMenu
	#@+body
	def createPopupMenu (self,v,event):
		
		a = app() ; c = self.commands ; frame = c.frame
		
		# If we are going to recreate it, we had better destroy it.
		if self.popupMenu:
			self.popupMenu.destroy()
			self.popupMenu = None
		
		self.popupMenu = menu = Tkinter.Menu(app().root, tearoff=0)
		
		# Add the Open With entries if they exist.
		if a.openWithTable:
			frame.createMenuEntries(menu,a.openWithTable,openWith=1)
			table = (("-",None,None),)
			frame.createMenuEntries(menu,table)
			
		
		#@<< Create the menu table >>
		#@+node:1::<< Create the menu table >>
		#@+body
		table = (
			("&Read @file Nodes",None,frame.OnReadAtFileNodes),
			("&Write @file Nodes",None,frame.OnWriteAtFileNodes),
			("-",None,None),
			("&Tangle","Shift+Ctrl+T",frame.OnTangle),
			("&Untangle","Shift+Ctrl+U",frame.OnUntangle),
			("-",None,None),
			("Toggle Angle &Brackets","Ctrl+B",frame.OnToggleAngleBrackets),
			("-",None,None),
			("Cut Node","Shift+Ctrl+X",frame.OnCutNode),
			("Copy Node","Shift+Ctrl+C",frame.OnCopyNode),
			("&Paste Node","Shift+Ctrl+V",frame.OnPasteNode),
			("&Delete Node","Shift+Ctrl+BkSp",frame.OnDeleteNode),
			("-",None,None),
			("&Insert Node","Ctrl+I",frame.OnInsertNode),
			("&Clone Node","Ctrl+`",frame.OnCloneNode),
			("Sort C&hildren",None,frame.OnSortChildren),
			("&Sort Siblings","Alt-A",frame.OnSortSiblings),
			("-",None,None),
			("Contract Parent","Alt+0",frame.OnContractParent))
		#@-body
		#@-node:1::<< Create the menu table >>

		frame.createMenuEntries(menu,table)
	#@-body
	#@-node:2::createPopupMenu
	#@+node:3::enablePopupMenuItems
	#@+body
	def enablePopupMenuItems (self,v,event):
		
		"""Enable and disable items in the popup menu."""
		
		c = self.commands ; menu = self.popupMenu
	
		
		#@<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		#@+node:1::<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
		#@+body
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
		#@-body
		#@-node:1::<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>

		isAtFile = choose(isAtFile,1,0)
		isAtRoot = choose(isAtRoot,1,0)
		canContract = v.parent() != None
		canContract = choose(canContract,1,0)
		
		for name in ("Read @file Nodes", "Write @file Nodes"):
			enableMenu(menu,name,isAtFile)
		for name in ("Tangle", "Untangle"):
			enableMenu(menu,name,isAtRoot)
		
		enableMenu(menu,"Cut Node",c.canCutOutline())
		enableMenu(menu,"Delete Node",c.canDeleteHeadline())
		enableMenu(menu,"Paste Node",c.canPasteOutline())
		enableMenu(menu,"Sort Children",c.canSortChildren())
		enableMenu(menu,"Sort Siblings",c.canSortSiblings())
		enableMenu(menu,"Contract Parent",c.canContractParent())
	#@-body
	#@-node:3::enablePopupMenuItems
	#@+node:4::showPopupMenu
	#@+body
	def showPopupMenu (self,v,event):
		
		"""Show a popup menu."""
		
		menu = self.popupMenu
	
		if sys.platform == "linux2": # 20-SEP-2002 DTHEIN: not needed for Windows
			menu.bind("<FocusOut>",self.OnPopupFocusLost)
		
		menu.post(event.x_root, event.y_root)
	
		# Make certain we have focus so we know when we lose it.
		# I think this is OK for all OSes.
		set_focus(menu)
	#@-body
	#@-node:4::showPopupMenu
	#@-node:13::tree.OnPopup & allies
	#@-node:6::Event handers (tree)
	#@+node:7::Incremental drawing
	#@+node:1::allocateNodes
	#@+body
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
		self.updateTree(self.rootVnode,root_left,root_top,0,0)
		# if self.updatedNodeCount: print "updatedNodeCount:", self.updatedNodeCount
	
	#@-body
	#@-node:1::allocateNodes
	#@+node:2::allocateNodesBeforeScrolling
	#@+body
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
	#@-body
	#@-node:2::allocateNodesBeforeScrolling
	#@+node:3::updateNode
	#@+body
	def updateNode (self,v,x,y):
		
		"""Draw a node that may have become visible as a result of a scrolling operation"""
	
		if self.inExpandedVisibleArea(y):
			# This check is a major optimization.
			if not v.edit_text():
				return self.force_draw_node(v,x,y)
			else:
				return self.line_height
	
		return self.line_height
	#@-body
	#@-node:3::updateNode
	#@+node:4::setVisibleAreaToFullCanvas
	#@+body
	def setVisibleAreaToFullCanvas(self):
		
		if self.visibleArea:
			y1,y2 = self.visibleArea
			y2 = max(y2,y1 + self.canvas.winfo_height())
			self.visibleArea = y1,y2
	#@-body
	#@-node:4::setVisibleAreaToFullCanvas
	#@+node:5::setVisibleArea
	#@+body
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
	
	#@-body
	#@-node:5::setVisibleArea
	#@+node:6::tree.updateTree
	#@+body
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
	
	#@-body
	#@-node:6::tree.updateTree
	#@-node:7::Incremental drawing
	#@+node:8::Selecting & editing (tree)
	#@+node:1::abortEditLabelCommand
	#@+body
	def abortEditLabelCommand (self):
		
		v = self.currentVnode
		# trace(v)
		if self.revertHeadline and v.edit_text() and v == self.editVnode:
			
			# trace(`self.revertHeadline`)
			v.edit_text().delete("1.0","end")
			v.edit_text().insert("end",self.revertHeadline)
			self.idle_head_key(v) # Must be done immediately.
			self.revertHeadline = None
			self.select(v)
			if v and len(v.t.joinList) > 0:
				# 3/26/03: changed redraw_now to force_redraw.
				self.force_redraw() # force a redraw of joined headlines.
	#@-body
	#@-node:1::abortEditLabelCommand
	#@+node:2::dimEditLabel, undimEditLabel
	#@+body
	# Convenience methods so the caller doesn't have to know the present edit node.
	
	def dimEditLabel (self):
	
		v = self.currentVnode
		self.setDisabledLabelState(v)
	
	def undimEditLabel (self):
	
		v = self.currentVnode
		self.setSelectedLabelState(v)
	#@-body
	#@-node:2::dimEditLabel, undimEditLabel
	#@+node:3::editLabel
	#@+body
	# Start editing v.edit_text()
	
	def editLabel (self, v):
	
		# End any previous editing
		if self.editVnode and v != self.editVnode:
			self.endEditLabel()
			self.revertHeadline = None
			
		self.editVnode = v # 7/7/03.
	
		# Start editing
		if v and v.edit_text():
			# trace(`v`)
			self.setNormalLabelState(v)
			self.revertHeadline = v.headString()
	#@-body
	#@-node:3::editLabel
	#@+node:4::endEditLabel & endEditLabelCommand
	#@+body
	# End editing for self.editText
	
	def endEditLabel (self):
	
		v = self.editVnode
		# trace(v)
		if v and v.edit_text():
			self.setUnselectedLabelState(v)
			self.editVnode = None
		if v: # Bug fix 10/9/02: also redraw ancestor headlines.
			# 3/26/03: changed redraw_now to force_redraw.
			self.force_redraw() # force a redraw of joined and ancestor headlines.
		set_focus(self.commands.body) # 10/14/02
			
	def endEditLabelCommand (self):
	
		v = self.editVnode
		# trace(v)
		if v and v.edit_text():
			self.select(v)
		if v: # Bug fix 10/9/02: also redraw ancestor headlines.
			# 3/26/03: changed redraw_now to force_redraw.
			self.force_redraw() # force a redraw of joined headlines.
		set_focus(self.commands.body) # 10/14/02
	#@-body
	#@-node:4::endEditLabel & endEditLabelCommand
	#@+node:5::tree.expandAllAncestors
	#@+body
	def expandAllAncestors (self,v):
	
		redraw_flag = false
		p = v.parent()
		while p:
			if not p.isExpanded():
				p.expand()
				redraw_flag = true
			p = p.parent()
		return redraw_flag
	#@-body
	#@-node:5::tree.expandAllAncestors
	#@+node:6::tree.scanForTabWidth
	#@+body
	# Similar to code in scanAllDirectives.
	
	def scanForTabWidth (self, v):
		
		c = self.commands ; w = c.tab_width
	
		while v:
			s = v.t.bodyString
			dict = get_directives_dict(s)
			
			#@<< set w and break on @tabwidth >>
			#@+node:1::<< set w and break on @tabwidth >>
			#@+body
			if dict.has_key("tabwidth"):
				
				val = scanAtTabwidthDirective(s,dict,issue_error_flag=false)
				if val and val != 0:
					w = val
					break
			#@-body
			#@-node:1::<< set w and break on @tabwidth >>

			v = v.parent()
	
		c.frame.setTabWidth(w)
	#@-body
	#@-node:6::tree.scanForTabWidth
	#@+node:7::tree.select
	#@+body
	# Warning: do not try to "optimize" this by returning if v==tree.currentVnode.
	
	def select (self,v,updateBeadList=true):
		
		# trace(v)
	
		
		#@<< define vars and stop editing >>
		#@+node:1::<< define vars and stop editing >>
		#@+body
		c = self.commands ; frame = c.frame ; body = frame.body
		old_v = c.currentVnode()
		
		# Unselect any previous selected but unedited label.
		self.endEditLabel()
		old = self.currentVnode
		self.setUnselectedLabelState(old)
		#@-body
		#@-node:1::<< define vars and stop editing >>

	
		if not doHook("unselect1",c=c,new_v=v,old_v=old_v):
			
			#@<< unselect the old node >>
			#@+node:2::<< unselect the old node >>
			#@+body
			# Remember the position of the scrollbar before making any changes.
			yview=body.yview()
			insertSpot = c.body.index("insert")
			
			# Remember the old body text
			old_body = body.get("1.0","end")
			
			if old and old != v and old.edit_text():
				old.t.scrollBarSpot = yview
				old.t.insertSpot = insertSpot
			
			#@-body
			#@-node:2::<< unselect the old node >>

		else: old_body = u""
	
		doHook("unselect2",c=c,new_v=v,old_v=old_v)
		
		if not doHook("select1",c=c,new_v=v,old_v=old_v):
			
			#@<< select the new node >>
			#@+node:3::<< select the new node >>
			#@+body
			self.commands.frame.setWrap(v)
			
			# Delete only if necessary: this may reduce flicker slightly.
			s = v.t.bodyString
			s = toUnicode(s,"utf-8")
			old_body = toUnicode(old_body,"utf-8")
			if old_body != s:
				body.delete("1.0","end")
				body.insert("1.0",s)
			
			# We must do a full recoloring: we may be changing context!
			self.recolor_now(v)
			
			if v and v.t.scrollBarSpot != None:
				first,last = v.t.scrollBarSpot
				body.yview("moveto",first)
			
			if v.t.insertSpot != None: # 9/21/02: moved from c.selectVnode
				c.body.mark_set("insert",v.t.insertSpot)
				c.body.see(v.t.insertSpot)
			else:
				c.body.mark_set("insert","1.0")
			#@-body
			#@-node:3::<< select the new node >>

			if v and v != old_v: # 3/26/03: Suppress duplicate call.
				try: # may fail during initialization
					self.idle_scrollTo(v)
				except: pass
			
			#@<< update c.beadList or c.beadPointer >>
			#@+node:5::<< update c.beadList or c.beadPointer >>
			#@+body
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
			
			#@-body
			#@-node:5::<< update c.beadList or c.beadPointer >>

			
			#@<< update c.visitedList >>
			#@+node:6::<< update c.visitedList >>
			#@+body
			# Make v the most recently visited node on the list.
			if v in c.visitedList:
				c.visitedList.remove(v)
				
			c.visitedList.insert(0,v)
			#@-body
			#@-node:6::<< update c.visitedList >>

	
		
		#@<< set the current node and redraw >>
		#@+node:4::<< set the current node and redraw >>
		#@+body
		self.currentVnode = v
		self.setSelectedLabelState(v)
		self.scanForTabWidth(v) # 9/13/02 #GS I believe this should also get into the select1 hook
		set_focus(self.commands.body)
		
		#@-body
		#@-node:4::<< set the current node and redraw >>

		doHook("select2",c=c,new_v=v,old_v=old_v)
		doHook("select3",c=c,new_v=v,old_v=old_v)
	
	#@-body
	#@-node:7::tree.select
	#@+node:8::tree.set...LabelState
	#@+body
	def setNormalLabelState (self,v): # selected, editing
		if v and v.edit_text():
			# trace(v)
			
			#@<< set editing headline colors >>
			#@+node:1::<< set editing headline colors >>
			#@+body
			config = app().config
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
			#@-body
			#@-node:1::<< set editing headline colors >>

			v.edit_text().tag_remove("sel","1.0","end")
			v.edit_text().tag_add("sel","1.0","end")
			set_focus(v.edit_text())
	
	def setDisabledLabelState (self,v): # selected, disabled
		if v and v.edit_text():
			# trace(v)
			
			#@<< set selected, disabled headline colors >>
			#@+node:2::<< set selected, disabled headline colors >>
			#@+body
			config = app().config
			fg = config.getWindowPref("headline_text_selected_foreground_color")
			bg = config.getWindowPref("headline_text_selected_background_color")
			
			if not fg or not bg:
				fg,bg = "black","gray80"
			
			try:
				v.edit_text().configure(
					state="disabled",highlightthickness=0,fg=fg,bg=bg)
			except:
				es_exception()
			#@-body
			#@-node:2::<< set selected, disabled headline colors >>

	
	def setSelectedLabelState (self,v): # selected, not editing
		self.setDisabledLabelState(v)
	
	def setUnselectedLabelState (self,v): # not selected.
		if v and v.edit_text():
			# trace(v)
			
			#@<< set unselected headline colors >>
			#@+node:3::<< set unselected headline colors >>
			#@+body
			config = app().config
			fg = config.getWindowPref("headline_text_unselected_foreground_color")
			bg = config.getWindowPref("headline_text_unselected_background_color")
			
			if not fg or not bg:
				fg,bg = "black","white"
			
			try:
				v.edit_text().configure(
					state="disabled",highlightthickness=0,fg=fg,bg=bg)
			except:
				es_exception()
			#@-body
			#@-node:3::<< set unselected headline colors >>
	#@-body
	#@-node:8::tree.set...LabelState
	#@-node:8::Selecting & editing (tree)
	#@+node:9::tree.moveUpDown
	#@+body
	def OnUpKey   (self,event=None): return self.moveUpDown("up")
	def OnDownKey (self,event=None): return self.moveUpDown("down")
	
	def moveUpDown (self,upOrDown):
		c = self.commands ; body = c.frame.body
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
	#@-body
	#@-node:9::tree.moveUpDown
	#@-others

	
class leoTree (baseLeoTree):
	"""A class that draws and handles events in an outline."""
	pass
#@-body
#@-node:0::@file leoTree.py
#@-leo
