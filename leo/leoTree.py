#@+leo

#@+node:0::@file leoTree.py

#@+body

#@+at
#  This class implements a tree control similar to Windows explorer.  The draw code is based on code found in Python's IDLE 
# program.  Thank you Guido van Rossum!
# 
# The vnode class contains all per-node information.  The vnode class handles all tree operations except drawing, selecting and 
# events.  Inserting, deleting and moving vnodes is done by altering the strurcture links, that is, the the v.mParent, 
# v.mFirstChild, v.mNext, v.mBack and ivars, then redrawing the entire tree.
# 
# The tree class knows about vnodes.  The vnode class could be split into a base class (say a treeItem class) containing the ivars 
# known to the tree class, and a derived class containing everything else, including, e.g., the bodyString ivar.  I haven't chosen 
# to split the vnode class this way because nothing would be gained in Leo.
# 
# The Commands class is responsible for redrawing the screen.  This should be done by enclosing code that could modify the screen 
# in c.beginUpdate()/c.endUpdate() pairs.  This is a simple and highly efficient mechanism.

#@-at

#@@c

from leoGlobals import *
from leoUtils import *
import leoApp, leoColor, leoNodes
import os, string, traceback, Tkinter


#@<< drawing constants >>

#@+node:1::<< drawing constants >>

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

#@-node:1::<< drawing constants >>


class leoTree:

	#@+others

	#@+node:2:C=1:tree.__init__

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
		
		# Controlling redraws
		self.updateCount = 0 # self.redraw does nothing unless this is zero.
		self.redrawCount = 0 # For traces
		self.redrawScheduled = false # true if redraw scheduled.
	
		# Selection ivars.
		self.currentVnode = None # The presently selected vnode.
		self.editVnode = None # The vnode being edited.
		self.initing = false # true: opening file.
	#@-body

	#@-node:2:C=1:tree.__init__

	#@+node:3::tree.__del__

	#@+body
	def __del__ (self):
	
		# Can't trace while destroying.
		# print "tree.__del__"
		pass
	#@-body

	#@-node:3::tree.__del__

	#@+node:4:C=2:tree.destroy

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

	#@-node:4:C=2:tree.destroy

	#@+node:5:C=3:tree.expandAllAncestors

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

	#@-node:5:C=3:tree.expandAllAncestors

	#@+node:6::Drawing

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

	#@+node:2:C=4:beginUpdate

	#@+body
	def beginUpdate (self):
	
		self.updateCount += 1
	#@-body

	#@-node:2:C=4:beginUpdate

	#@+node:3:C=5:drawBox

	#@+body
	def drawBox (self,v,x,y):
	
		y += 7 # draw the box at x, y+7
	
		iconname = choose(v.isExpanded(), "Icons\\minusnode.GIF", "Icons\\plusnode.GIF")
		image = self.getIconImage(iconname)
		id = self.canvas.create_image(x,y,image=image)
		if 0: # don't create a reference to this!
			v.box_id = id
		self.canvas.tag_bind(id, "<1>", v.OnBoxClick)
		self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
	#@-body

	#@-node:3:C=5:drawBox

	#@+node:4:C=6:tree.drawIcon

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
		if 0: # don't create a reference!
			v.icon_id = id
		self.canvas.tag_bind(id, "<1>", v.OnIconClick)
		self.canvas.tag_bind(id, "<Double-1>", v.OnBoxClick)
	
		return 0 # dummy icon height
	#@-body

	#@-node:4:C=6:tree.drawIcon

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

	#@+node:7:C=7:drawText

	#@+body
	# draws text for v at x,y
	
	def drawText(self,v,x,y):
	
		x += text_indent
		if v.edit_text: # self.canvas.delete("all") may already have done this, but do it anyway.
			v.edit_text.destroy()
		v.edit_text = t = Tkinter.Text(self.canvas,bd=0,relief="flat",width=self.headWidth(v),height=1)
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
		t.bind("<Double-1>", v.OnBoxClick)
		t.bind("<Key>", v.OnHeadlineKey)
		id = self.canvas.create_window(x,y,anchor="nw",window=t)
		if 0: # don't create this reference!
			v.edit_text_id = id
		self.canvas.tag_lower(id)
	
		return line_height
	#@-body

	#@-node:7:C=7:drawText

	#@+node:8:C=8:endUpdate

	#@+body
	def endUpdate (self, flag=true):
	
		assert(self.updateCount > 0)
		self.updateCount -= 1
		if flag and self.updateCount == 0:
			self.redraw()
	#@-body

	#@-node:8:C=8:endUpdate

	#@+node:9:C=9:tree.getIconImage

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

	#@-node:9:C=9:tree.getIconImage

	#@+node:10::headWidth

	#@+body

	#@+at
	#  Returns the proper width of the entry widget for the headline. This has been a problem.

	#@-at

	#@@c
	
	def headWidth(self,v):
	
		return max(10,len(v.headString()))
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

	#@+node:14:C=10:lastVisible

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

	#@-node:14:C=10:lastVisible

	#@+node:15:C=11:tree.recolor & recolor_now

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

	#@-node:15:C=11:tree.recolor & recolor_now

	#@+node:16:C=12:tree.redraw , force_redraw, redraw_now

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

	#@-node:16:C=12:tree.redraw , force_redraw, redraw_now

	#@+node:17:C=13:tree.idle_scrollTo

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
	
	def idle_scrollTo(self):
	
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

	#@-node:17:C=13:tree.idle_scrollTo

	#@+node:18:C=14:yoffset

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

	#@-node:18:C=14:yoffset

	#@-node:6::Drawing

	#@+node:7::Event handers

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

	#@+node:3:C=15:tree.onBodyChanged & OnBodyKey & idle_body_key

	#@+body

	#@+at
	#  The <Key> event generates the event before the body text is changed(!), so we register an idle-event handler to do the work later.
	# 
	# 1/17/02: Rather than trying to figure out whether the control or alt keys are down, we always schedule the idle_handler.  
	# The idle_handler sees if any change has, in fact, been made to the body text, and sets the changed and dirty bits only if 
	# so.  This is the clean and safe way.

	#@-at

	#@@c
	
	# Called by command handlers.
	def onBodyChanged (self):
		v = self.currentVnode
		self.commands.body.after_idle(self.idle_body_key,v)
	
	# Bound to any keystroke.
	def OnBodyKey (self,event): 
	
		v = self.currentVnode ; ch = event.char
		self.commands.body.after_idle(self.idle_body_key,v,ch)
	
	def idle_body_key (self,v,ch=None):
	
		c = self.commands
		if not c or not v or v != c.currentVnode(): return
		# Ignore characters that don't change the body text.
		s = c.body.get("1.0", "end")
		s = string.rstrip(s)
		changed = s != v.bodyString()
		# Needed so that control keys by themselves won't make a node dirty.
		if not changed and ch != '\r' and ch != '\n' :return
		# trace(c.body.index("insert")+":"+c.body.get("insert linestart","insert lineend"))
		# print "idle_body_key", `ch`	# Update changed mark if necessary.
		if ch == '\r' or ch == '\n':
			
	#@<< Do auto indent >>

			#@+node:1::<< Do Auto indent >>

			#@+body
			# Get the previous line.
			s=c.body.get("insert linestart - 1 lines","insert linestart -1c")
			
			# Add the leading whitespace to the present line.
			junk,width = skip_leading_ws_with_indent(s,0,c.tab_width)
			if s and len(s) > 0 and s[-1]==':':
				# For Python: increase auto-indent after colons.
				language = self.colorizer.scanColorDirectives(v)
				if language == python_language:
					width += c.tab_width
			ws = computeLeadingWhitespace (width,c.tab_width)
			if ws and len(ws) > 0:
				c.body.insert("insert", ws)
			#@-body

			#@-node:1::<< Do Auto indent >>

			s = c.body.get("1.0", "end")
			s = string.rstrip(s)
		# Update the tnode.
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

	#@-node:3:C=15:tree.onBodyChanged & OnBodyKey & idle_body_key

	#@+node:4::OnDeactivate

	#@+body
	def OnDeactivate (self, event=None):
	
		self.endEditLabel()
		self.dimEditLabel()
		self.active = false
	#@-body

	#@-node:4::OnDeactivate

	#@+node:5:C=16:tree.OnHeadlineKey

	#@+body

	#@+at
	#  The <Key> event generates the event before the headline text is changed(!), so we register an idle-event handler to do the 
	# work later.

	#@-at

	#@@c
	
	def OnHeadlineKey(self,v,event):
	
		v = self.currentVnode ; ch = event.char
		self.commands.body.after_idle(self.idle_head_key,v,ch)
	
	def idle_head_key (self,v,ch=None):
	
		c = self.commands
		if not v or not v.edit_text or v != c.currentVnode():
			return
		s = v.edit_text.get("1.0","end")
		# print "idle_head_key", s
		# remove all newlines and update the vnode
		s = string.replace(s,'\n','')
		s = string.replace(s,'\r','')
		changed = s != v.headString()
		done = ch and (ch == '\r' or ch == '\n')
	
		if not changed and not done:
			return
			
		index = v.edit_text.index("insert")
			
		# print `ch` + ", changed:" + `changed` + ", " + `s`
	
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

	#@-node:5:C=16:tree.OnHeadlineKey

	#@-node:7::Event handers

	#@+node:8:C=17:Selecting & editing (tree)

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

	#@+node:2:C=18:editLabel

	#@+body
	# Start editing v.edit_text
	
	def editLabel (self, v):
	
		# End any previous editing
		if self.editVnode and v != self.editVnode:
			self.endEditLabel()
			
		# Start editing
		if v and v.edit_text:
			self.setNormalLabelState(v)
			v.edit_text.tag_remove("sel","1.0","end")
			v.edit_text.tag_add("sel","1.0","end")
			self.editVnode = v
		else:
			self.editVnode = None
	#@-body

	#@-node:2:C=18:editLabel

	#@+node:3:C=19:endEditLabel

	#@+body
	# End editing for self.editText
	
	def endEditLabel (self):
	
		v = self.editVnode
		
		if v and v.edit_text:
			self.setUnselectedLabelState(v)
			self.editVnode = None
		
		if v and v.joinList:
			self.redraw() # force a redraw of joined headlines.
	#@-body

	#@-node:3:C=19:endEditLabel

	#@+node:4:C=20:tree.select

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

	#@-node:4:C=20:tree.select

	#@+node:5:C=21:tree.set...LabelState

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

	#@-node:5:C=21:tree.set...LabelState

	#@-node:8:C=17:Selecting & editing (tree)

	#@-others

#@-body

#@-node:0::@file leoTree.py

#@-leo
