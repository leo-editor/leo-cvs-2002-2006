#@+leo

#@+node:0::@file leoTree.py
#@+body
#@@language python


#@+at
#  This class implements a tree control similar to Windows explorer.  The draw code is based on code found in Python's IDLE 
# program.  Thank you Guido van Rossum!
# 
# The tree class knows about vnodes.  The vnode class could be split into a base class (say a treeItem class) containing the ivars 
# known to the tree class, and a derived class containing everything else, including, e.g., the bodyString ivar.  I haven't chosen 
# to split the vnode class this way because nothing would be gained in Leo.

#@-at
#@@c

from leoGlobals import *
from leoUtils import *
import leoColor
import os, string, Tkinter, tkFont


#@<< about drawing and events >>
#@+node:1::<< about drawing and events >>
#@+body
#@+at
#  Leo must redraw the outline pane when commands are executed and as the result of mouse and keyboard events.  The main 
# challenges are eliminating flicker and handling events properly.  These topics are interrelated.
# 
# Eliminating flicker.  Leo must update the outline pane with minimum flicker.  Various versions of Leo have approached this 
# problem in different ways.  The drawing code in leo.py is robust, flexible, relatively simple and should work in almost any 
# conceivable environment.
# 
# Leo assumes that all code that changes the outline pane will be enclosed in matching calls to the c.beginUpdate and c.endUpdate  
# methods of the Commands class. c.beginUpdate() inhibits drawing until the matching c.endUpdate().  These calls may be nested; 
# only the outermost call to c.endUpdate() calls c.redraw() to force a redraw of the outline pane.
# 
# In leo.py, code may call c.endUpdate(flag) instead of c.endUpdate().  Leo redraws the screen only if flag is true.  This allows 
# code to suppress redrawing entirely when needed.  For example, study the idle_body_key event handler to see how Leo 
# conditionally redraws the outline pane.
# 
# The leoTree class redraws all icons automatically when c.redraw() is called.  This is a major simplification compared to 
# previous versions of Leo.  The entire machinery of drawing icons in the vnode class has been eliminated.  The v.computeIcon 
# method tells what the icon should be.  The v.iconVal ivar that tells what the present icon is. The event handler simply compares 
# these two values and sets redraw_flag if they don't match.
# 
# Handling events. Besides redrawing the screen, Leo must handle events or commands that change the text in the outline or body 
# panes.  It is surprisingly difficult to ensure that headline and body text corresponds to the vnode and tnode corresponding to 
# presently selected outline, and vice versa. For example, when the user selects a new headline in the outline pane, we must 
# ensure that 1) the vnode and tnode of the previously selected node have up-to-date information and 2) the body pane is loaded 
# from the correct data in the corresponding tnode.  Early versions of Leo attempted to satisfy these conditions when the user 
# switched outline nodes.  Such attempts never worked well; there were too many special cases.  Later versions of Leo, including 
# leo.py, use a much more direct approach.  The event handlers make sure that the vnode and tnode corresponding to the presently 
# selected node are always kept up-to-date.  In particular, every keystroke in the body pane causes the presently selected tnode 
# to be updated immediately.  There is no longer any need for the c.synchVnode method, though that method still exists for 
# compatibility with old scripts.
# 
# The leoTree class contains all the event handlers for the body and outline panes.  The actual work is done in the idle_head_key 
# and idle_body_key methods.  These routines are surprisingly complex; they must handle all the tasks mentioned above, as well as 
# others. The idle_head_key and idle_body_key methods should not be called outside the leoTree class.  However, it often happens 
# that code that handles user commands must simulate an event.  That is, the code needs to indicate that headline or body text has 
# changed so that the screen may be redrawn properly.   The leoTree class defines the following simplified event handlers: 
# onBodyChanged, onBodyWillChange, onBodyKey, onHeadChanged and onHeadlineKey.  Commanders and subcommanders call these event 
# handlers to indicate that a command has changed, or will change, the headline or body text.  Calling event handlers rather than 
# c.beginUpdate and c.endUpdate ensures that the outline pane is redrawn only when needed.

#@-at
#@-body
#@-node:1::<< about drawing and events >>


#@<< drawing constants >>
#@+node:2::<< drawing constants >>
#@+body
box_padding = 5 # extra padding between box and icon
box_width = 9 + box_padding
icon_width = 20
text_indent = 4 # extra padding between icon and tex
child_indent = 28 # was 20
hline_y = 7 # Vertical offset of horizontal line
line_height = 17 + 2 # To be replaced by Font height

root_left = 7 + box_width
root_top = 2

hiding = true # True if we don't reallocate items
#@-body
#@-node:2::<< drawing constants >>


class leoTree:

	#@+others
	#@+node:3:C=1:tree.__init__
	#@+body
	def __init__(self,commands,canvas):
	
		self.canvas = canvas
		self.commands = commands
		self.rootVnode = None
		self.topVnode = None
		self.iconimages = {} # Image cache set by getIconImage().
		self.colorizer = leoColor.colorizer(commands)
		self.bodyKeepsFocus = true # true if body keeps focus when tree canvas clicked
		self.vnode_alloc_list = [] # List of all vnodes ever allocated in this tree.
		self.active = false # true if tree is active
		
		# We use the system defaults below if self.font == None.
		config = app().config
		self.font = config.getFontFromParams(
			"headline_text_font_family", "headline_text_font_size",
			"headline_text_font_slant",  "headline_text_font_weight")
	
		# self.font and self.fontName must exist for self.getFont.
		if self.font:
			self.fontName = config.getWindowPref("headline_text_font_family")
		else:
			# Get the name and font from the system defaults.
			t = Tkinter.Text()
			self.fontName = fn = t.cget("font")
			self.font = tkFont.Font(font=fn)
		assert(self.font)
		
		# Controlling redraws
		self.updateCount = 0 # self.redraw does nothing unless this is zero.
		self.redrawCount = 0 # For traces
		self.redrawScheduled = false # true if redraw scheduled.
	
		# Selection ivars.
		self.currentVnode = None # The presently selected vnode.
		self.editVnode = None # The vnode being edited.
		self.initing = false # true: opening file.
		
		# Drag and drop
		self.oldcursor = None # To reset cursor after drag
		self.drag_id = None # To reset bindings after drag
	#@-body
	#@-node:3:C=1:tree.__init__
	#@+node:4::tree.__del__
	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "tree.__del__"
		pass
	#@-body
	#@-node:4::tree.__del__
	#@+node:5:C=2:tree.destroy
	#@+body
	def destroy (self):
	
		if not app().deleteOnClose:
			return
			
		# Can't trace while destroying.
		# print "tree.destroy"
	
		for v in self.vnode_alloc_list:
			v.destroy()
		del self.vnode_alloc_list # del all vnodes
	
		self.iconimages = None
		del self.colorizer
		self.colorizer = None
	
		# Remove links to objects destroyed by frame.
		self.commands = None
		self.canvas = None
	
		# Remove all links to nodes
		self.currentVnode = None # The presently selected vnode.
		self.editVnode = None # The vnode being edited.
		self.rootVnode = None
		self.topVnode = None
	#@-body
	#@-node:5:C=2:tree.destroy
	#@+node:6:C=3:tree.expandAllAncestors
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
	#@-node:6:C=3:tree.expandAllAncestors
	#@+node:7:C=4:tree.findVnodeWithIconId
	#@+body
	def findVnodeWithIconId (self,id):
	
		v = self.rootVnode
		while v:
			if v.icon_id == id or (v.icon_id,) == id:
				return v
			v = v.threadNext()
		return None
	#@-body
	#@-node:7:C=4:tree.findVnodeWithIconId
	#@+node:8::getFont/setFont (used by leoFontPanel)
	#@+body
	def getFont (self):
	
		return self.font
			
	def setFont (self, font=None, fontName=None):
		
		if fontName:
			self.fontName = fontName
			self.font = tkFont.Font(font=fontName)
		else:
			self.fontName = None
			self.font = font
	#@-body
	#@-node:8::getFont/setFont (used by leoFontPanel)
	#@+node:9::Drawing
	#@+node:1::About drawing and updating
	#@+body
	#@+at
	#  About drawing and updating strategy.
	# 
	# This version of Leo draws the outline "by hand" using the Tk canvas widget.  Surprisingly, this is not only easy, but 
	# simplifies the vnode and Commands classes.
	# 
	# 1.  Updating and redraw.  The tree.redraw() method is called automatically from the "outermost" call to tree.endUpdate.  
	# Moreover, calling .tree.redraw() inside a tree.beginUpdate/tree.endUpdate pair does nothing.  c.redraw(), c.beginUpdate() 
	# and c.endUpdate() just call the corresponding tree methods.  Finally, beginUpdate()/endUpdate(false) can be used to suppress 
	# redrawing entirely.
	# 
	# Therefore, the Commands class never needs to worry about extra calls to tree.redraw() provided all code that draws to the 
	# tree is enclosed in a tree.beginUpdate/tree.endUpdate pair.  The tree.idle_body_key event handler manages redrawing "by 
	# hand" by maintaining a redraw_flag and then calling endUpdate(redraw_flag).
	# 
	# 2.  The tree.redraw() method deletes all old canvas items and recomputes all data, including v.iconVal.  This means that 
	# v.doDelete need not actually delete vnodes for them to disappear from the screen.  Indeed, vnode are never actually deleted, 
	# only unlinked.  It would be valid for "dependent" vnodes to be deleted, but there really is no need to do so.

	#@-at
	#@-body
	#@-node:1::About drawing and updating
	#@+node:2:C=5:beginUpdate
	#@+body
	def beginUpdate (self):
	
		self.updateCount += 1
	#@-body
	#@-node:2:C=5:beginUpdate
	#@+node:3:C=6:drawBox
	#@+body
	def drawBox (self,v,x,y):
	
		y += 7 # draw the box at x, y+7
	
		# Portability fix for linux.
		minus_node = os.path.join("Icons", "minusnode.gif")
		plus_node = os.path.join("Icons", "plusnode.gif")
		iconname = choose(v.isExpanded(), minus_node, plus_node)
		
		image = self.getIconImage(iconname)
		id = self.canvas.create_image(x,y,image=image)
		if 0: # don't create a reference to this!
			v.box_id = id
		self.canvas.tag_bind(id, "<1>", v.OnBoxClick)
		self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
	#@-body
	#@-node:3:C=6:drawBox
	#@+node:4:C=7:tree.drawIcon
	#@+body
	# Draws icon for v at x,y
	
	def drawIcon(self,v,x,y):
	
		v.iconx, v.icony = x,y
	
		y += 2 # draw icon at y + 2
	
		# Always recompute icon.
		val = v.iconVal = v.computeIcon()
		assert(0 <= val <= 15)
		
		# Compute the image name
		imagename = os.path.join("Icons", "box")
		if val < 10: imagename += "0"
		imagename += `val`
	
		# Get the image
		image = self.getIconImage(imagename + ".GIF")
		id = self.canvas.create_image(x,y,anchor="nw",image=image)
		if 1: # 6/15/02: this reference is now cleared in v.__del__
			v.icon_id = id
		self.canvas.tag_bind(id, "<1>", v.OnIconClick)
		self.canvas.tag_bind(id, "<Double-1>", v.OnBoxClick)
	
		return 0 # dummy icon height
	#@-body
	#@-node:4:C=7:tree.drawIcon
	#@+node:5::drawTree
	#@+body
	def drawTree(self,v,x,y,h,level):
	
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
	#@-node:5::drawTree
	#@+node:6::drawNode
	#@+body
	def drawNode(self,v,x,y):
	
		# Draw horizontal line from vertical line to icon.
		self.canvas.create_line(x, y+7, x+box_width, y+7,tag="lines",fill="gray50") # stipple="gray25")
		if v.firstChild(): self.drawBox(v,x,y)
		icon_height = self.drawIcon(v,x+box_width,y)
		text_height = self.drawText(v,x+box_width+icon_width,y)
		return max(icon_height, text_height)
	#@-body
	#@-node:6::drawNode
	#@+node:7:C=8:drawText
	#@+body
	# draws text for v at x,y
	
	def drawText(self,v,x,y):
	
		x += text_indent
		if v.edit_text: # self.canvas.delete("all") may already have done this, but do it anyway.
			v.edit_text.destroy()
		v.edit_text = t = Tkinter.Text(self.canvas,
			font=self.font,bd=0,relief="flat",width=self.headWidth(v),height=1)
	
		t.insert("end", v.headString())
		
		#@<< configure the text depending on state >>
		#@+node:1::<< configure the text depending on state >>
		#@+body
		if v == self.currentVnode:
			if self.bodyKeepsFocus:
				t.configure(state="disabled",fg="black",bg="gray80")
			else:
				w = self.commands.frame.getFocus()
				if w == self.canvas:
					t.configure(state="normal",fg="white",bg="DarkBlue")
				else:
					t.configure(state="disabled",fg="black",bg="gray80")
		else:
			t.configure(state="disabled",fg="black",bg="white")
		#@-body
		#@-node:1::<< configure the text depending on state >>

		t.bind("<1>", v.OnHeadlineClick)
		if 0: # 6/15/02: Bill Drissel objects to this binding.
			t.bind("<Double-1>", v.OnBoxClick)
		t.bind("<Key>", v.OnHeadlineKey)
		id = self.canvas.create_window(x,y,anchor="nw",window=t)
		if 0: # don't create this reference!
			v.edit_text_id = id
		self.canvas.tag_lower(id)
	
		return line_height
	#@-body
	#@-node:7:C=8:drawText
	#@+node:8:C=9:endUpdate
	#@+body
	def endUpdate (self, flag=true):
	
		assert(self.updateCount > 0)
		self.updateCount -= 1
		if flag and self.updateCount == 0:
			self.redraw()
	#@-body
	#@-node:8:C=9:endUpdate
	#@+node:9:C=10:tree.getIconImage
	#@+body
	def getIconImage (self, name):
	
		# Return the image from the cache if possible.
		if self.iconimages.has_key(name):
			return self.iconimages[name]
			
		try:
			dir = app().loadDir
			file, ext = os.path.splitext(name)
			fullname = os.path.join(dir, file + ext)
			fullname = os.path.normpath(fullname)
			image = Tkinter.PhotoImage(master=self.canvas, file=fullname)
			self.iconimages[name] = image
			return image
		except:
			es("Can not load: " + fullname)
			es("dir:" + `dir` + ", file:" + `file` + ", ext:" + `ext`)
			return None
	#@-body
	#@-node:9:C=10:tree.getIconImage
	#@+node:10::headWidth
	#@+body
	#@+at
	#  Returns the proper width of the entry widget for the headline. This has been a problem.

	#@-at
	#@@c
	
	def headWidth(self,v):
	
		return max(10,5 + len(v.headString()))
	#@-body
	#@-node:10::headWidth
	#@+node:11::hideAllChildren
	#@+body
	def hideAllChildren(self,v):
	
		child = v.firstChild()
		while child:
			self.hideTree(child)
			child = child.next()
	#@-body
	#@-node:11::hideAllChildren
	#@+node:12::hideNode (no longer used)
	#@+body
	def hideNode(self,v):
	
		self.canvas.delete(v.box_id)
		self.canvas.delete(v.icon_id)
		self.canvas.delete(v.edit_text)
		self.canvas.delete(v.edit_text_id)
		v.box_id = v.icon_id = None
		v.edit_text = v.edit_text_id = None
	#@-body
	#@-node:12::hideNode (no longer used)
	#@+node:13::hideTree (no longer used)
	#@+body
	def hideTree(self,v):
	
		last = v.lastNode()
		while v:
			self.hideNode(v)
			if v == last: break
			v = v.threadNext()
	#@-body
	#@-node:13::hideTree (no longer used)
	#@+node:14:C=11:lastVisible
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
	#@-node:14:C=11:lastVisible
	#@+node:15:C=12:tree.recolor & recolor_now
	#@+body
	def recolor(self,v):
	
		body = self.commands.frame.body
		
		if 0: # Do immediately
			self.colorizer.colorize(v,body)
		else: # Do at idle time
			self.colorizer.schedule(v,body)
	
	def recolor_now(self,v):
	
		body = self.commands.frame.body
		self.colorizer.colorize(v,body)
	#@-body
	#@-node:15:C=12:tree.recolor & recolor_now
	#@+node:16:C=13:tree.redraw , force_redraw, redraw_now
	#@+body
	# Calling redraw inside c.beginUpdate()/c.endUpdate() does nothing.
	# This _is_ useful when a flag is passed to c.endUpdate.
	def redraw (self):
		if self.updateCount == 0 and not self.redrawScheduled:
			# print "tree.redraw"
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
			
	# Schedules a redraw even if inside beginUpdate/endUpdate
	def force_redraw (self):
		# print "tree.force_redraw"
		if not self.redrawScheduled:
			self.redrawScheduled = true
			self.canvas.after_idle(self.idle_redraw)
			
	# Redraws immediately: used by Find so a redraw doesn't mess up selections.
	# It is up to the caller to ensure that no other redraws are pending.
	def redraw_now (self):
	
		# print "tree.redraw_now: ", self.redrawScheduled
		self.idle_redraw()
	
	def idle_redraw (self):
	
		self.redrawScheduled = false
		frame = self.commands.frame
		if frame in app().windowList and app().quitting == 0:
			# self.redrawCount += 1 ; trace(`self.redrawCount`)
			self.expandAllAncestors(self.currentVnode)
			# Erase and redraw the entire tree.
			oldcursor = self.canvas['cursor']
			self.canvas['cursor'] = "watch"
			self.canvas.delete("all")
			self.drawTree(self.rootVnode,root_left,root_top,0,0)
			self.canvas['cursor'] = oldcursor
			# Set up the scroll region.
			x0, y0, x1, y1 = self.canvas.bbox("all")
			self.canvas.configure(scrollregion=(0, 0, x1, y1))
			# Schedule a scrolling operation after the scrollbar is redrawn
			self.canvas.after_idle(self.idle_scrollTo)
	#@-body
	#@-node:16:C=13:tree.redraw , force_redraw, redraw_now
	#@+node:17:C=14:tree.idle_scrollTo
	#@+body
	#@+at
	#  This scrolls the canvas so that v is in view.  This is done at idle time after a redraw so that treeBar.get() will return 
	# proper values.  Earlier versions of this routine were called _before_ a redraw so that the calls to yoffset() were 
	# required.  We could use v.icony instead, and that might be better.
	# 
	# Another approach would be to add a "draw" flat to the drawing routines so that they just compute a height if the draw flag 
	# is false.  However, that would complicate the drawing logic quite a bit.

	#@-at
	#@@c
	
	def idle_scrollTo(self,v=None):
	
		if v == None:
			v = self.currentVnode
		last = self.lastVisible()
		h1 = self.yoffset(v)
		h2 = self.yoffset(last)
		# Compute the fraction to scroll, minus a smidge so the first line will be entirely visible.
		if h2 > 0.1:
			frac = float(h1)/float(h2)
		else:
			frac = 0.0 # probably any value would work here.
		frac = min(frac,1.0)
		frac = max(frac,0.0)
		
		# Do nothing if the line is already in view
		frame = self.commands.frame
		lo, hi = frame.treeBar.get()
		if frac < lo or frac > hi:
			# print "h1, h2, frac, hi, lo:", h1, h2, frac, hi, lo
			self.canvas.yview("moveto", frac)
	#@-body
	#@-node:17:C=14:tree.idle_scrollTo
	#@+node:18:C=15:tree.yoffset
	#@+body
	#@+at
	#  We can't just return icony because the tree hasn't been redrawn yet.  For the same reason we can't rely on any TK canvas 
	# methods here.

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
			h += line_height
			child = v.firstChild()
			if v.isExpanded() and child:
				h2, flag = self.yoffsetTree(child,v1)
				h += h2
				if flag: return h, true
			v = v.next()
		return h, false
	#@-body
	#@-node:18:C=15:tree.yoffset
	#@+node:19:C=16:tree.numberOfVisibleNodes
	#@+body
	def numberOfVisibleNodes(self):
		
		n = 0 ; v = self.rootVnode
		while v:
			n += 1
			v = v.visNext()
		return n
	#@-body
	#@-node:19:C=16:tree.numberOfVisibleNodes
	#@-node:9::Drawing
	#@+node:10::Event handers
	#@+node:1::OnActivate
	#@+body
	def OnActivate (self,v):
	
		c=self.commands
		# trace(`v`)
	
		if v == self.currentVnode:
			# w = self.commands.frame.getFocus()
			if self.active:
				self.editLabel(v)
			else:
				self.undimEditLabel()
				self.canvas.focus_set()
		else:
			self.select(v)
			c.body.mark_set("insert","1.0")
			c.body.focus_force()
	
		self.active = true
	#@-body
	#@-node:1::OnActivate
	#@+node:2::OnBoxClick
	#@+body
	# Called on click in box and double-click in headline.
	
	def OnBoxClick (self,v):
	
		if v.isExpanded():
			v.contract()
		else:
			v.expand()
	
		self.active = true
		self.select(v)
		self.canvas.focus_set() # This is safe.
		self.redraw()
	#@-body
	#@-node:2::OnBoxClick
	#@+node:3:C=17:tree.OnDrag
	#@+body
	#@+at
	#  Auto-scrolls the canvas as needed and opens nodes if the control key is down.

	#@-at
	#@@c
	
	def OnDrag(self,v,event):
		
		# es("tree.OnDrag" + `v`)
		assert(v == self.drag_v)
	
		if not event: return
		c = self.commands ; canvas = self.canvas ; frame = self.commands.frame
		x,y = event.x,event.y
	
		
		#@<< set vdrag and expandFlag >>
		#@+node:1::<< set vdrag and expandFlag >>
		#@+body
		#@+at
		#  vdrag is the node presently under the cursor.  childFlag is set if vdrag could be expanded.

		#@-at
		#@@c
		
		canvas_x = canvas.canvasx(x)
		canvas_y = canvas.canvasy(y)
		
		id = self.canvas.find_closest(canvas_x,canvas_y)
		vdrag = self.findVnodeWithIconId(id)
		expandFlag = vdrag and vdrag.hasChildren() and not vdrag.isExpanded()
		#@-body
		#@-node:1::<< set vdrag and expandFlag >>

		if 0: # Confusing: we should only do this if a modifier key is down.
			if vdrag and vdrag != v and expandFlag:
				
				#@<< expand vdrag and redraw >>
				#@+node:2::<< expand vdrag and redraw >>
				#@+body
				# redrawing will change id's.
				if self.drag_id:
					canvas.tag_unbind(self.drag_id , "<B1-Motion>")
					canvas.tag_unbind(self.drag_id , "<Any-ButtonRelease-1>")
					
				vdrag.expand()
				c.dragToNthChildOf(v,vdrag,0)
				self.redraw_now()
				self.idle_scrollTo(vdrag)
				
				if 0: # This doesn't work, because we haven't had a mouse down event in the new node.
					# Pretend the expanded node is what we are dragging!
					self.drag_id = vdrag.icon_id
					# es("OnDrag expanding:" + `vdrag` + " " + `self.drag_id`)
					if self.drag_id:
						canvas.tag_bind(self.drag_id, "<B1-Motion>", v.OnDrag)
						canvas.tag_bind(self.drag_id, "<Any-ButtonRelease-1>", v.OnEndDrag)
				else:
					self.canvas['cursor'] = self.oldcursor
				#@-body
				#@-node:2::<< expand vdrag and redraw >>

	
		if self.drag_id: # OnEndDrag can stop the scheduling of more events.
			
			#@<< scroll the canvas as needed >>
			#@+node:3::<< scroll the canvas as needed >>
			#@+body
			# Scroll the screen up or down one line if the cursor (y) is outside the canvas.
			h = canvas.winfo_height()
			if y < 0 or y > h:
				lo, hi = frame.treeBar.get()
				n = self.numberOfVisibleNodes()
				line_frac = 1.0 / float(n)
				frac = choose(y < 0, lo - line_frac, lo + line_frac)
				frac = min(frac,1.0)
				frac = max(frac,0.0)
				# es("lo,hi,frac:" + `lo` + " " + `hi` + " " + `frac`)
				canvas.yview("moveto", frac)
				
			# Queue up another event to keep scrolling while the cursor is outside the canvas.
			# OnEndDrag() halts the scrolling by clearing self.drag_id when the mouse button goes up.
			if 0: # This doesn't work very well.  Just moving the cursor to force scrolling seems better.
				lo, hi = frame.treeBar.get()
				if (y < 0 and lo > 0.1) or (y > h and hi < 0.9):
					canvas.after_idle(self.OnDrag,v,event)
			#@-body
			#@-node:3::<< scroll the canvas as needed >>
	#@-body
	#@-node:3:C=17:tree.OnDrag
	#@+node:4:C=18:tree.OnEndDrag
	#@+body
	def OnEndDrag(self,v,event):
		
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

			if vdrag and vdrag != v:
				if childFlag:
					c.dragToNthChildOf(v,vdrag,0)
				else:
					c.dragAfter(v,vdrag)
			else:
				if v and vdrag == None: es("not dragged: " + v.headString())
				if 0: # Don't undo the scrolling we just did!
					self.idle_scrollTo(v)
			self.canvas['cursor'] = self.oldcursor
	
		if self.drag_id:
			canvas.tag_unbind(self.drag_id , "<B1-Motion>")
			canvas.tag_unbind(self.drag_id , "<Any-ButtonRelease-1>")
			self.drag_id = None
	#@-body
	#@-node:4:C=18:tree.OnEndDrag
	#@+node:5:C=19:tree.OnIconClick
	#@+body
	def OnIconClick (self,v,event):
	
		canvas = self.canvas
		# es("OnIconClick" + `v`)
		
		if event:
			canvas_x = canvas.canvasx(event.x)
			canvas_y = canvas.canvasy(event.y)
			id = canvas.find_closest(canvas_x,canvas_y)
			if id:
				self.drag_id = id
				self.drag_v = v
				canvas.tag_bind(id, "<B1-Motion>", v.OnDrag)
				canvas.tag_bind(id, "<Any-ButtonRelease-1>", v.OnEndDrag)
				self.oldcursor = self.canvas['cursor']
				self.canvas['cursor'] = "hand2" # "center_ptr"
	
		self.select(v)
	#@-body
	#@-node:5:C=19:tree.OnIconClick
	#@+node:6:C=20:tree.onBodyChanged, onBodyWillChange, OnBodyKey, idle_body_key
	#@+body
	#@+at
	#  The <Key> event generates the event before the body text is changed(!), so we register an idle-event handler to do the work later.
	# 
	# 1/17/02: Rather than trying to figure out whether the control or alt keys are down, we always schedule the idle_handler.  
	# The idle_handler sees if any change has, in fact, been made to the body text, and sets the changed and dirty bits only if 
	# so.  This is the clean and safe way.
	# 
	# 2/19/02: We must distinguish between commands like "Find, Then Change", which must call onBodyChanged, and commands like 
	# "Cut" and "Paste" that must call onBodyWillChange.  The former commands have already changed the body text, and that change 
	# must be captured immediately.  The latter commands have not changed the body text, and that change may only be captured at 
	# idle time.

	#@-at
	#@@c
	
	# Called by command handlers that have already changed the text.
	def onBodyChanged (self,v,undoType):
	
		c = self.commands
		if not v: v = c.currentVnode()
		oldSel = c.body.index("insert")
		# trace(`oldSel`)
		self.idle_body_key(v,oldSel,undoType)
		
	# Called by command handlers that change the text just before idle time.
	def onBodyWillChange (self,v,undoType):
	
		c = self.commands
		if not v: v = c.currentVnode()
		oldSel = c.body.index("insert")
		# trace(`oldSel`)
		self.commands.body.after_idle(self.idle_body_key,v,oldSel,undoType)
	
	# Bound to any key press.
	def OnBodyKey (self,event):
	
		c = self.commands
		v = c.currentVnode() ; ch = event.char
		oldSel = c.body.index("insert")
		# trace(`oldSel`)
		self.commands.body.after_idle(self.idle_body_key,v,oldSel,"Typing",ch)
	
	# Does the real work of updating the body pane.
	def idle_body_key (self,v,oldSel,undoType,ch=None):
	
		c = self.commands
		if not c or not v or v != c.currentVnode(): return
		if 0: # prints on control-alt keys
			trace(`ch` + ":" + `c.body.get("1.0", "end")`)
			trace(c.body.index("insert")+":"+c.body.get("insert linestart","insert lineend"))
		# Ignore characters that don't change the body text.
		s = c.body.get("1.0", "end")
		if len(s) > 0 and s[-1]=='\n': s = s[:-1]
		if s == v.bodyString(): return
		# trace(`ch`)
		# trace(`ch` + ":" + `s`)
		# trace(c.body.index("insert")+":"+c.body.get("insert linestart","insert lineend"))
		newSel = c.body.index("insert")
		if ch == '\r' or ch == '\n':
			
			#@<< Do auto indent >>
			#@+node:1::<< Do Auto indent >>
			#@+body
			# Do nothing if we are in @nocolor mode or if we are executing a Change command.
			if self.colorizer.useSyntaxColoring(v) and undoType != "Change":
				# Get the previous line.
				s=c.body.get("insert linestart - 1 lines","insert linestart -1c")
				# Add the leading whitespace to the present line.
				junk,width = skip_leading_ws_with_indent(s,0,c.tab_width)
				if s and len(s) > 0 and s[-1]==':':
					# For Python: increase auto-indent after colons.
					language = self.colorizer.scanColorDirectives(v)
					if language == python_language:
						width += abs(c.tab_width)
				ws = computeLeadingWhitespace (width,c.tab_width)
				if ws and len(ws) > 0:
					c.body.insert("insert", ws)

			#@-body
			#@-node:1::<< Do Auto indent >>

			s = c.body.get("1.0", "end")
			s = string.rstrip(s)
		elif ch == '\t' and c.tab_width < 0:
			
			#@<< convert leading tab to blanks >>
			#@+node:2::<< convert leading tab to blanks >>
			#@+body
			# Do nothing if we are in @nocolor mode or if we are executing a Change command.
			if self.colorizer.useSyntaxColoring(v) and undoType != "Change":
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
			#@-node:2::<< convert leading tab to blanks >>

		# Update the tnode.
		if s == None: s = ""
		c.undoer.setUndoTypingParams(v,undoType,v.bodyString(),s,oldSel,newSel)
		v.t.bodyString = s
		# Recolor the body.
		self.recolor_now(v) # We are already at idle time, so this doesn't help much.
		# Update dirty bits and changed bit.
		if not c.changed:
			c.setChanged(true) 
		redraw_flag = false
		c.beginUpdate()
		if not v.isDirty() and v.setDirty(): # Sets all cloned and @file dirty bits
			redraw_flag = true
		# update icons.
		val = v.computeIcon()
		if val != v.iconVal:
			v.iconVal = val
			redraw_flag = true
		c.endUpdate(redraw_flag) # redraw only if necessary
	#@-body
	#@-node:6:C=20:tree.onBodyChanged, onBodyWillChange, OnBodyKey, idle_body_key
	#@+node:7::OnDeactivate
	#@+body
	def OnDeactivate (self, event=None):
	
		self.endEditLabel()
		self.dimEditLabel()
		self.active = false
	#@-body
	#@-node:7::OnDeactivate
	#@+node:8:C=21:tree.OnHeadlineKey, onHeadlineChanged, idle_head_key
	#@+body
	#@+at
	#  The <Key> event generates the event before the headline text is changed(!), so we register an idle-event handler to do the 
	# work later.

	#@-at
	#@@c
	
	def onHeadChanged (self,v):
		self.commands.body.after_idle(self.idle_head_key,v)
	
	def OnHeadlineKey (self,v,event):
	
		# v = self.currentVnode ;
		ch = event.char
		self.commands.body.after_idle(self.idle_head_key,v,ch)
	
	def idle_head_key (self,v,ch=None):
	
		c = self.commands
		if not v or not v.edit_text or v != c.currentVnode():
			return
		s = v.edit_text.get("1.0","end")
		# remove all newlines and update the vnode
		s = string.replace(s,'\n','')
		s = string.replace(s,'\r','')
		if not s: s = ""
		changed = s != v.headString()
		done = ch and (ch == '\r' or ch == '\n')
		if not changed and not done:
			return
		if changed:
			c.undoer.setUndoParams("Change Headline",v,newText=s,oldText=v.headString())
		index = v.edit_text.index("insert")
		# trace(`s`)
		if changed:
			c.beginUpdate()
			# Update changed bit.
			if not c.changed:
				c.setChanged(true)
			# Update all dirty bits.
			v.setDirty() 
			# Update v.
			v.initHeadString(s)
			v.edit_text.delete("1.0","end")
			v.edit_text.insert("end",s)
			v.edit_text.mark_set("insert",index)
			# Update all joined nodes.
			v2 = v.joinList
			while v2 and v2 != v:
				v2.initHeadString(s)
				if v2.edit_text: # v2 may not be visible
					v2.edit_text.delete("1.0","end")
					v2.edit_text.insert("end",s)
				v2 = v2.joinList
			c.endUpdate(false) # do not redraw now.
	
		# Reconfigure v's headline.
		if done:
			if self.bodyKeepsFocus:
				v.edit_text.configure(state="disabled",fg="black",bg="gray80",width=self.headWidth(v))
			else:
				v.edit_text.configure(state="disabled",fg="white",bg="DarkBlue",width=self.headWidth(v))
		else:
			v.edit_text.configure(width=self.headWidth(v))
	
		# Reconfigure all joined headlines.
		v2 = v
		while v2 and v2 != v:
			if v2.edit_text: # v2 may not be visible
				v2.edit_text.configure(width=self.headWidth(v2))
			v2 = v2.joinList
			
		# Update the screen.
		if done:
			c.beginUpdate()
			self.endEditLabel()
			c.endUpdate()
		elif changed:
			# update v immediately.  Joined nodes are redrawn later by endEditLabel.
			# Redrawing the whole screen now messes up the cursor in the headline.
			self.drawIcon(v,v.iconx,v.icony) # just redraw the icon.
	#@-body
	#@-node:8:C=21:tree.OnHeadlineKey, onHeadlineChanged, idle_head_key
	#@-node:10::Event handers
	#@+node:11::Selecting & editing (tree)
	#@+node:1::dimEditLabel, undimEditLabel
	#@+body
	# Convenience methods so the caller doesn't have to know the present edit node.
	
	def dimEditLabel (self):
	
		v = self.currentVnode
		self.setDisabledLabelState(v)
	
	def undimEditLabel (self):
	
		v = self.currentVnode
		self.setSelectedLabelState(v)
	#@-body
	#@-node:1::dimEditLabel, undimEditLabel
	#@+node:2:C=22:editLabel
	#@+body
	# Start editing v.edit_text
	
	def editLabel (self, v):
	
		# End any previous editing
		if self.editVnode and v != self.editVnode:
			self.endEditLabel()
			
		# Start editing
		if v and v.edit_text:
			# es("editLabel" + `v`)
			self.setNormalLabelState(v)
			v.edit_text.tag_remove("sel","1.0","end")
			v.edit_text.tag_add("sel","1.0","end")
			v.edit_text.focus_force()
			self.editVnode = v
		else:
			self.editVnode = None
	#@-body
	#@-node:2:C=22:editLabel
	#@+node:3:C=23:endEditLab (es here helps set focus properly!)
	#@+body
	# End editing for self.editText
	
	def endEditLabel (self):
	
		v = self.editVnode
		# es("EndEditLabel" + `v`)
		
		if v and v.edit_text:
			self.setUnselectedLabelState(v)
			self.editVnode = None
		
		if v and v.joinList:
			self.redraw_now() # force a redraw of joined headlines.
	#@-body
	#@-node:3:C=23:endEditLab (es here helps set focus properly!)
	#@+node:4:C=24:tree.select
	#@+body
	#@+at
	#  Warning: do not try to "optimize" this be returning if v==tree.currentVnode.

	#@-at
	#@@c
	
	def select (self, v):
	
		# Replace body text
		body = self.commands.frame.body
		body.delete("1.0", "end")
		body.insert("1.0", v.t.bodyString)
		self.recolor_now(v)
		# Unselect any previous selected but unedited label.
		self.endEditLabel()
		old = self.currentVnode
		if old and old != v and old.edit_text:
			self.setUnselectedLabelState(old)
		self.currentVnode = v
		self.setSelectedLabelState(v)
		# Set focus.
		if self.bodyKeepsFocus:
			self.commands.body.focus_set()
		else:
			self.canvas.focus_set()
	#@-body
	#@-node:4:C=24:tree.select
	#@+node:5:C=25:tree.set...LabelState
	#@+body
	def setNormalLabelState (self,v): # selected, editing
		if v and v.edit_text:
			v.edit_text.configure(state="normal",highlightthickness=1,fg="black", bg="white")
	
	def setDisabledLabelState (self,v): # selected, disabled
		if v and v.edit_text:
			v.edit_text.configure(state="disabled",highlightthickness=0,fg="black",bg="gray80")
	
	def setSelectedLabelState (self,v): # selected, not editing
		if self.bodyKeepsFocus:
			self.setDisabledLabelState(v)
		elif v and v.edit_text:
			v.edit_text.configure(state="disabled",highlightthickness=0,fg="white",bg="DarkBlue")
	
	def setUnselectedLabelState (self,v): # not selected.
		if v and v.edit_text:
			v.edit_text.configure(state="disabled",highlightthickness=0,fg="black",bg="white")
	#@-body
	#@-node:5:C=25:tree.set...LabelState
	#@-node:11::Selecting & editing (tree)
	#@-others
#@-body
#@-node:0::@file leoTree.py
#@-leo
