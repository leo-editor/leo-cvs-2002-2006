#@+leo-ver=4
#@+node:@file leoFrame.py
"""The base classes for all Leo Windows, their body, log and tree panes, key bindings and menus.

These classes should be overridden to create frames for a particular gui."""

from leoGlobals import *
import leoColor
import os,string,sys,time

#@<< About handling events >>
#@+node:<< About handling events >>
#@+at 
#@nonl
# Leo must handle events or commands that change the text in the outline or 
# body panes.  It is surprisingly difficult to ensure that headline and body 
# text corresponds to the vnode and tnode corresponding to presently selected 
# outline, and vice versa. For example, when the user selects a new headline 
# in the outline pane, we must ensure that 1) the vnode and tnode of the 
# previously selected node have up-to-date information and 2) the body pane is 
# loaded from the correct data in the corresponding tnode.
# 
# Early versions of Leo attempted to satisfy these conditions when the user 
# switched outline nodes.  Such attempts never worked well; there were too 
# many special cases.  Later versions of Leo, including leo.py, use a much 
# more direct approach.  The event handlers make sure that the vnode and tnode 
# corresponding to the presently selected node are always kept up-to-date.  In 
# particular, every keystroke in the body pane causes the presently selected 
# tnode to be updated immediately.  There is no longer any need for the 
# c.synchVnode method.  (That method still exists for compatibility with old 
# scripts.)
# 
# The leoTree class contains all the event handlers for the tree pane, and the 
# leoBody class contains the event handlers for the body pane.  The actual 
# work is done in the idle_head_key and idle_body_key methods.  These routines 
# are surprisingly complex; they must handle all the tasks mentioned above, as 
# well as others. The idle_head_key and idle_body_key methods should not be 
# called outside their respective classes.  However, sometimes code in the 
# Commands must simulate an event.  That is, the code needs to indicate that 
# headline or body text has changed so that the screen may be redrawn 
# properly.   The leoBody class defines the following simplified event 
# handlers: onBodyChanged, onBodyWillChange and onBodyKey. Similarly, the 
# leoTree class defines onHeadChanged and onHeadlineKey.  Commanders and 
# subcommanders call these event handlers to indicate that a command has 
# changed, or will change, the headline or body text.  Calling event handlers 
# rather than c.beginUpdate and c.endUpdate ensures that the outline pane is 
# redrawn only when needed.
#@-at
#@-node:<< About handling events >>
#@nl

#@+others
#@+node:class leoBody
class leoBody:
	
	"""The base class for the body pane in Leo windows."""
	
	#@	@+others
	#@+node:leoBody.__init__
	def __init__ (self,frame,parentFrame):
	
		self.frame = frame
		self.c = c = frame.c
		self.forceFullRecolorFlag = false
		
		self.bodyCtrl = self.createControl(frame,parentFrame)
		frame.body = self
	
		self.setBodyFontFromConfig()
		
		self.colorizer = leoColor.colorizer(c)
	#@nonl
	#@-node:leoBody.__init__
	#@+node:Must be overriden in subclasses
	def createBindings (self,frame):
		self.oops()
	
	def createControl (self,frame,parentFrame):
		self.oops()
		
	def initialRatios (self):
		self.oops()
		
	def onBodyChanged (self,v,undoType,oldSel=None,oldYview=None,newSel=None,oldText=None):
		self.oops()
		
	def setBodyFontFromConfig (self):
		self.oops()
		
	def oops (self):
		print "leoBody oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:Must be overriden in subclasses
	#@+node:Coloring 
	# It's weird to have the tree class be responsible for coloring the body pane!
	
	def getColorizer(self):
		
		return self.colorizer
	
	def recolor_now(self,v,incremental=false):
	
		self.colorizer.colorize(v,incremental)
	
	def recolor_range(self,v,leading,trailing):
		
		self.colorizer.recolor_range(v,leading,trailing)
	
	def recolor(self,v,incremental=false):
		
		if 0: # Do immediately
			self.colorizer.colorize(v,incremental)
		else: # Do at idle time
			self.colorizer.schedule(v,incremental)
		
	def updateSyntaxColorer(self,v):
		
		return self.colorizer.updateSyntaxColorer(v)
	#@nonl
	#@-node:Coloring 
	#@-others
#@nonl
#@-node:class leoBody
#@+node:class leoFrame
class leoFrame:
	
	"""The base class for all Leo windows."""
	
	instances = 0
	
	#@	@+others
	#@+node: leoFrame.__init__
	def __init__ (self):
		
		self.c = None # Must be created by subclasses.
		self.title = None # Must be created by subclasses.
		
		# Objects attached to this frame.
		self.menu = None
		self.keys = None
		self.colorPanel = None 
		self.fontPanel = None 
		self.prefsPanel = None
		self.comparePanel = None
	
		# Gui-independent data
		self.es_newlines = 0 # newline count for this log stream
		self.openDirectory = ""
		self.outlineToNowebDefaultFileName = "noweb.nw" # For Outline To Noweb dialog.
		self.saved=false # True if ever saved
		self.splitVerticalFlag,self.ratio,self.secondary_ratio = self.initialRatios()
		self.startupWindow=false # True if initially opened window
		self.stylesheet = None # The contents of <?xml-stylesheet...?> line.
	
		# Colors of log pane.
		self.statusColorTags = [] # list of color names used as tags in status window.
	
		# Previous row and column shown in the status area.
		self.lastStatusRow = self.lastStatusCol = 0
		self.tab_width = 0 # The tab width in effect in this pane.
	#@nonl
	#@-node: leoFrame.__init__
	#@+node:gui-dependent commands (must be defined  in subclasses)
	# Gui-dependent commands in the Edit menu...
	def OnCopy  (self,event=None): self.oops()
	def OnCut   (self,event=None): self.oops()
	def OnPaste (self,event=None): self.oops()
	
	def OnCutFromMenu  (self):     self.oops()
	def OnCopyFromMenu (self):     self.oops()
	def OnPasteFromMenu (self):    self.oops()
	
	def insertHeadlineTime (self): self.oops()
	
	# Gui-dependent commands in the Window menu...
	def cascade(self):              self.oops()
	def equalSizedPanes(self):      self.oops()
	def hideLogWindow (self):       self.oops()
	def minimizeAll(self):          self.oops()
	def toggleSplitDirection(self): self.oops()
	#@nonl
	#@-node:gui-dependent commands (must be defined  in subclasses)
	#@+node:longFileName & shortFileName
	def longFileName (self):
	
		return self.c.mFileName
		
	def shortFileName (self):
	
		return shortFileName(self.c.mFileName)
	#@nonl
	#@-node:longFileName & shortFileName
	#@+node:oops
	def oops(self):
		
		print "leoFrame oops:", callerName(2), "should be overridden in subclass"
	#@-node:oops
	#@+node:promptForSave
	def promptForSave (self):
		
		"""Prompt the user to save changes.
		
		Return true if the user vetos the quit or save operation."""
		
		c = self.c
		name = choose(c.mFileName,c.mFileName,self.title)
		type = choose(app.quitting, "quitting?", "closing?")
	
		answer = app.gui.runAskYesNoCancelDialog(
			"Confirm",
			'Save changes to %s before %s' % (name,type))
			
		# print answer	
		if answer == "cancel":
			return true # Veto.
		elif answer == "no":
			return false # Don't save and don't veto.
		else:
			if not c.mFileName:
				#@			<< Put up a file save dialog to set mFileName >>
				#@+node:<< Put up a file save dialog to set mFileName >>
				# Make sure we never pass None to the ctor.
				if not c.mFileName:
					c.mFileName = ""
				
				c.mFileName = app.gui.runSaveFileDialog(
					initialfile = c.mFileName,
					title="Save",
					filetypes=[("Leo files", "*.leo")],
					defaultextension=".leo")
				#@nonl
				#@-node:<< Put up a file save dialog to set mFileName >>
				#@nl
			if c.mFileName:
				# print "saving", c.mFileName
				c.fileCommands.save(c.mFileName)
				return false # Don't veto.
			else:
				return true # Veto.
	#@nonl
	#@-node:promptForSave
	#@+node:scanForTabWidth
	# Similar to code in scanAllDirectives.
	
	def scanForTabWidth (self, v):
		
		c = self.c ; w = c.tab_width
	
		while v:
			s = v.t.bodyString
			dict = get_directives_dict(s)
			#@		<< set w and break on @tabwidth >>
			#@+node:<< set w and break on @tabwidth >>
			if dict.has_key("tabwidth"):
				
				val = scanAtTabwidthDirective(s,dict,issue_error_flag=false)
				if val and val != 0:
					w = val
					break
			#@nonl
			#@-node:<< set w and break on @tabwidth >>
			#@nl
			v = v.parent()
	
		c.frame.setTabWidth(w)
	#@nonl
	#@-node:scanForTabWidth
	#@-others
#@nonl
#@-node:class leoFrame
#@+node:class leoLog
class leoLog:
	
	"""The base class for the log pane in Leo windows."""
	
	#@	@+others
	#@+node:leoLog.__init__
	def __init__ (self,frame,parentFrame):
		
		self.frame = frame
		self.c = frame.c
		self.newlines = 0
	
		self.logControl = self.createControl(parentFrame)
		self.setFontFromConfig()
	#@-node:leoLog.__init__
	#@+node:leoLog.configure
	def configure (self,*args,**keys):
		
		self.oops()
	#@nonl
	#@-node:leoLog.configure
	#@+node:leoLog.configureBorder
	def configureBorder(self,border):
		
		self.oops()
	#@-node:leoLog.configureBorder
	#@+node:leoLog.createControl
	def createControl (self,parentFrame):
		
		self.oops()
	#@nonl
	#@-node:leoLog.createControl
	#@+node:leoLog.oops
	def oops (self):
		
		print "leoLog oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:leoLog.oops
	#@+node:leoLog.setLogFontFromConfig
	def setFontFromConfig (self):
		
		self.oops()
	#@nonl
	#@-node:leoLog.setLogFontFromConfig
	#@+node:leoLog.onActivateLog
	def onActivateLog (self,event=None):
	
		try:
			app.setLog(self,"OnActivateLog")
		except:
			es_event_exception("activate log")
	#@nonl
	#@-node:leoLog.onActivateLog
	#@+node:leoLog.put & putnl
	# All output to the log stream eventually comes here.
	
	def put (self,s,color=None):
		self.oops()
	
	def putnl (self):
		self.oops()
	#@nonl
	#@-node:leoLog.put & putnl
	#@-others
#@nonl
#@-node:class leoLog
#@+node:class leoTree
# This would be useful if we removed all the tree redirection routines.
# However, those routines are pretty ingrained into Leo...

class leoTree:
	
	"""The base class for the outline pane in Leo windows."""
	
	#@	@+others
	#@+node:  tree.__init__
	def __init__ (self,frame):
		
		self.frame = frame
		self.c = frame.c
		
		self.edit_text_dict = {} # New in 3.12: keys vnodes, values are edit_text (Tk.Text widgets)
		
		# "public" ivars: correspond to setters & getters.
		self.mCurrentVnode = None
		self.mDragging = false
		self.mEditVnode = None
		self.mRootVnode = None
		self.mTopVnode = None
		
		# Controlling redraws
		self.updateCount = 0 # self.redraw does nothing unless this is zero.
		self.redrawCount = 0 # For traces
		self.redrawScheduled = false # true if redraw scheduled.
	#@nonl
	#@-node:  tree.__init__
	#@+node:Drawing
	def drawIcon(self,v,x=None,y=None):
		self.oops()
	
	def redraw(self,event=None): # May be bound to an event.
		self.oops()
	
	def redraw_now(self):
		self.oops()
	#@nonl
	#@-node:Drawing
	#@+node:Edit label
	def editLabel(self,v):
		self.oops()
	
	def endEditLabel(self):
		self.oops()
	
	def setNormalLabelState(self,v):
		self.oops()
	#@nonl
	#@-node:Edit label
	#@+node:Fonts
	def getFont(self):
		self.oops()
		
	def setFont(self,font=None,fontName=None):
		self.oops()
	#@nonl
	#@-node:Fonts
	#@+node:Notifications
	# These should all be internal to the tkinter.frame class.
	
	def OnActivateHeadline(self,v):
		self.oops()
		
	def onHeadChanged(self,v):
		self.oops()
	
	def OnHeadlineKey(self,v,event):
		self.oops()
	
	def idle_head_key(self,v,ch=None):
		self.oops()
	#@nonl
	#@-node:Notifications
	#@+node:Scrolling
	def scrollTo(self,v):
		self.oops()
	
	def idle_scrollTo(self,v):
		
		self.oops()
	
	
	#@-node:Scrolling
	#@+node:Selecting
	def select(self,v,updateBeadList=true):
		
		self.oops()
	#@nonl
	#@-node:Selecting
	#@+node:Tree operations
	def expandAllAncestors(self,v):
		
		self.oops()
	#@nonl
	#@-node:Tree operations
	#@+node:beginUpdate
	def beginUpdate (self):
	
		self.updateCount += 1
	#@nonl
	#@-node:beginUpdate
	#@+node:endUpdate
	def endUpdate (self,flag=true):
	
		assert(self.updateCount > 0)
		self.updateCount -= 1
		if flag and self.updateCount == 0:
			self.redraw()
	#@nonl
	#@-node:endUpdate
	#@+node:Getters
	def currentVnode(self):
		return self.mCurrentVnode
		
	def dragging(self):
		return self.mDragging
		
	def getEditTextDict(self,v):
		return self.edit_text_dict.get(v)
		
	def editVnode(self):
		return self.mEditVnode
	
	def rootVnode(self):
		return self.mRootVnode
	
	def topVnode(self):
		return self.mTopVnode
	#@nonl
	#@-node:Getters
	#@+node:Setters
	def setCurrentVnode(self,v):
		self.mCurrentVnode = v
		
	def setDragging(self,flag):
		self.mDragging = flag
		
	def setEditVnode(self,v):
		self.mEditVnode = v
	
	def setRootVnode(self,v):
		self.mRootVnode = v
		
	def setIniting(self,flag):
		pass # No longer used
		
	def setTopVnode(self,v):
		self.mTopVnode = v
	#@nonl
	#@-node:Setters
	#@+node:oops
	def oops(self):
		
		print "leoTree oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:oops
	#@-others
#@nonl
#@-node:class leoTree
#@-others
#@nonl
#@-node:@file leoFrame.py
#@-leo
