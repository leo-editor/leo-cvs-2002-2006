#@+leo-ver=4
#@+node:@file leoFrame.py
"""The base classes for all Leo Windows, their body, log and tree panes, key bindings and menus.

These classes should be overridden to create frames for a particular gui."""

from leoGlobals import *
import leoColor,leoMenu,leoUndo
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
		frame.body = self
		
		# May be overridden in subclasses...
		self.bodyCtrl = self
		
		# Must be overridden in subclasses...
		self.colorizer = None
	#@nonl
	#@-node:leoBody.__init__
	#@+node:oops
	def oops (self):
		
		trace("leoBody oops:", callerName(2), "should be overridden in subclass")
	#@nonl
	#@-node:oops
	#@+node:leoBody.setFontFromConfig
	def setFontFromConfig (self):
		
		self.oops()
	#@nonl
	#@-node:leoBody.setFontFromConfig
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
		
	#@-node:Must be overriden in subclasses
	#@+node:Bounding box (Tk spelling)
	def bbox(self,index):
	
		self.oops()
	#@nonl
	#@-node:Bounding box (Tk spelling)
	#@+node:Color tags (Tk spelling)
	def tag_add (self,tagName,index1,index2):
	
		self.oops()
	
	def tag_bind (self,tagName,event,callback):
	
		self.oops()
	
	def tag_configure (self,colorName,**keys):
	
		self.oops()
	
	def tag_delete(self,tagName):
	
		self.oops()
	
	def tag_remove (self,tagName,index1,index2):
		self.oops()
	#@nonl
	#@-node:Color tags (Tk spelling)
	#@+node:Configuration (Tk spelling)
	def cget(self,*args,**keys):
		
		self.oops()
		
	def configure (self,*args,**keys):
		
		self.oops()
	#@nonl
	#@-node:Configuration (Tk spelling)
	#@+node:Focus
	def hasFocus (self):
		
		self.oops()
		
	def setFocus (self):
		
		self.oops()
	#@nonl
	#@-node:Focus
	#@+node:Height & width
	def getBodyPaneHeight (self):
		
		self.oops()
	
	def getBodyPaneWidth (self):
		
		self.oops()
	#@nonl
	#@-node:Height & width
	#@+node:Idle time...
	def scheduleIdleTimeRoutine (self,function,*args,**keys):
	
		self.oops()
	#@nonl
	#@-node:Idle time...
	#@+node:Indices
	def adjustIndex (self,index,offset):
		
		self.oops()
		
	def compareIndices(self,i,rel,j):
	
		self.oops()
		
	def convertRowColumnToIndex (self,row,column):
		
		self.oops()
		
	def convertIndexToRowColumn (self,index):
		
		self.oops()
		
	def getImageIndex (self,image):
		
		self.oops()
	#@nonl
	#@-node:Indices
	#@+node:Insert point
	def getBeforeInsertionPoint (self):
		self.oops()
	
	def getInsertionPoint (self):
		self.oops()
		
	def getCharAtInsertPoint (self):
		self.oops()
	
	def getCharBeforeInsertPoint (self):
		self.oops()
		
	def makeInsertPointVisible (self):
		self.oops()
		
	def setInsertionPoint (self,index):
		self.oops()
	
	def setInsertionPointToEnd (self):
		self.oops()
		
	def setInsertPointToStartOfLine (self,lineNumber): # zero-based line number
		self.oops()
	#@nonl
	#@-node:Insert point
	#@+node:Menus
	def bind (self,*args,**keys):
		
		self.oops()
	#@-node:Menus
	#@+node:Selection
	def deleteTextSelection (self):
		self.oops()
		
	def getSelectedText (self):
		self.oops()
		
	def getTextSelection (self):
		self.oops()
		
	def hasTextSelection (self):
		self.oops()
		
	def selectAllText (self):
		self.oops()
		
	def setTextSelection (self,i,j=None):
		self.oops()
	#@nonl
	#@-node:Selection
	#@+node:delete...
	def deleteAllText(self):
		self.oops()
	
	def deleteCharacter (self,index):
		self.oops()
		
	def deleteLastChar (self):
		self.oops()
		
	def deleteLine (self,lineNumber): # zero based line number.
		self.oops()
		
	def deleteLines (self,line1,numberOfLines): # zero based line numbers.
		self.oops()
		
	def deleteRange (self,index1,index2):
		self.oops()
	#@nonl
	#@-node:delete...
	#@+node:get...
	def getAllText (self):
		self.oops()
		
	def getCharAtIndex (self,index):
		self.oops()
		
	def getInsertLines (self):
		self.oops()
		return None,None,None
		
	def getSelectionAreas (self):
		self.oops()
		return None,None,None
		
	def getSelectionLines (self):
		self.oops()
		return None,None,None
		
	def getTextRange (self,index1,index2):
		self.oops()
	#@nonl
	#@-node:get...
	#@+node:Insert...
	def insertAtInsertPoint (self,s):
		
		self.oops()
		
	def insertAtEnd (self,s):
		
		self.oops()
		
	def insertAtStartOfLine (self,lineNumber,s):
		
		self.oops()
	#@nonl
	#@-node:Insert...
	#@+node:setSelectionAreas
	def setSelectionAreas (self,before,sel,after):
		self.oops()
	#@nonl
	#@-node:setSelectionAreas
	#@+node:Visibility & scrolling
	def makeIndexVisible (self,index):
		self.oops()
		
	def setFirstVisibleIndex (self,index):
		self.oops()
		
	def getYScrollPosition (self):
		self.oops()
		
	def setYScrollPosition (self,scrollPosition):
		self.oops()
		
	def scrollUp (self):
		self.oops()
		
	def scrollDown (self):
		self.oops()
	#@nonl
	#@-node:Visibility & scrolling
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
	#@+node:  leoFrame.__init__
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
		self.splitVerticalFlag,self.ratio, self.secondary_ratio = self.initialRatios()
		self.startupWindow=false # True if initially opened window
		self.stylesheet = None # The contents of <?xml-stylesheet...?> line.
	
		# Colors of log pane.
		self.statusColorTags = [] # list of color names used as tags in status window.
	
		# Previous row and column shown in the status area.
		self.lastStatusRow = self.lastStatusCol = 0
		self.tab_width = 0 # The tab width in effect in this pane.
	#@nonl
	#@-node:  leoFrame.__init__
	#@+node: gui-dependent commands
	# In the Edit menu...
	def OnCopy  (self,event=None): self.oops()
	def OnCut   (self,event=None): self.oops()
	def OnPaste (self,event=None): self.oops()
	
	def OnCutFromMenu  (self):     self.oops()
	def OnCopyFromMenu (self):     self.oops()
	def OnPasteFromMenu (self):    self.oops()
	
	def abortEditLabelCommand (self): self.oops()
	def endEditLabelCommand (self):   self.oops()
	def insertHeadlineTime (self):    self.oops()
	
	# In the Window menu...
	def cascade(self):              self.oops()
	def equalSizedPanes(self):      self.oops()
	def hideLogWindow (self):       self.oops()
	def minimizeAll(self):          self.oops()
	def toggleActivePane(self):     self.oops()
	def toggleSplitDirection(self): self.oops()
	
	# In help menu...
	def leoHelp (self): self.oops()
	#@nonl
	#@-node: gui-dependent commands
	#@+node:bringToFront, deiconify, lift & update
	def bringToFront (self):
		
		self.oops()
	
	def deiconify (self):
		
		self.oops()
		
	def lift (self):
		
		self.oops()
		
	def update (self):
		
		self.oops()
	#@-node:bringToFront, deiconify, lift & update
	#@+node:resizePanesToRatio
	def resizePanesToRatio (self,ratio,secondary_ratio):
		
		pass
	#@nonl
	#@-node:resizePanesToRatio
	#@+node:setInitialWindowGeometry
	def setInitialWindowGeometry (self):
		
		self.oops()
	#@nonl
	#@-node:setInitialWindowGeometry
	#@+node:setTopGeometry
	def setTopGeometry (self,w,h,x,y,adjustSize=true):
		
		self.oops()
	#@nonl
	#@-node:setTopGeometry
	#@+node:setTabWidth
	def setTabWidth (self,w):
		
		# Subclasses may override this to affect drawing.
		self.tab_width = w
	#@nonl
	#@-node:setTabWidth
	#@+node:getTitle & setTitle
	def getTitle (self):
		return self.title
		
	def setTitle (self,title):
		self.title = title
	#@nonl
	#@-node:getTitle & setTitle
	#@+node:initialRatios
	def initialRatios (self):
	
		config = app.config
	
		s = config.getWindowPref("initial_splitter_orientation")
		verticalFlag = s == None or (s != "h" and s != "horizontal")
	
		if verticalFlag:
			r = config.getFloatWindowPref("initial_vertical_ratio")
			if r == None or r < 0.0 or r > 1.0: r = 0.5
			r2 = config.getFloatWindowPref("initial_vertical_secondary_ratio")
			if r2 == None or r2 < 0.0 or r2 > 1.0: r2 = 0.8
		else:
			r = config.getFloatWindowPref("initial_horizontal_ratio")
			if r == None or r < 0.0 or r > 1.0: r = 0.3
			r2 = config.getFloatWindowPref("initial_horizontal_secondary_ratio")
			if r2 == None or r2 < 0.0 or r2 > 1.0: r2 = 0.8
	
		# print (`r`,`r2`)
		return verticalFlag,r,r2
	#@nonl
	#@-node:initialRatios
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
	#@+node:leoLog.setFontFromConfig
	def setFontFromConfig (self):
		
		self.oops()
	#@nonl
	#@-node:leoLog.setFontFromConfig
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
				#   file://home/me/todolist.html
				#@-at
				#@@c
				
				try:
					import os
					os.chdir(app.loadDir)
				
					if match(url,0,"file:") and url[-4:]==".leo":
						ok,frame = openWithFileName(url[5:],c)
						if ok:
							frame.bringToFront()
					else:
						import webbrowser
						webbrowser.open(url)
				except:
					es("exception opening " + url)
					es_exception()
				
				#@-node:<< pass the url to the web browser >>
				#@nl
			doHook("@url2",c=c,v=v)
	#@nonl
	#@-node:tree.OnIconDoubleClick (@url)
	#@-others
#@nonl
#@-node:class leoTree
#@+node:class nullBody
class nullBody (leoBody):

	#@	@+others
	#@+node: nullBody.__init__
	def __init__ (self,frame,parentFrame):
		
		leoBody.__init__ (self,frame,parentFrame) # Init the base class.
	
		self.insertPoint = 0
		self.selection = 0,0
		self.s = "" # The body text
		
		self.colorizer = leoColor.nullColorizer(self.c)
	#@nonl
	#@-node: nullBody.__init__
	#@+node:findStartOfLine
	def findStartOfLine (self,lineNumber):
		
		lines = splitLines(self.s)
		i = 0 ; index = 0
		for line in lines:
			if i == lineNumber: break
			i += 1
			index += len(line)
		return index
	#@nonl
	#@-node:findStartOfLine
	#@+node:scanToStartOfLine
	def scanToStartOfLine (self,index):
		
		if index <= 0:
			return 0
			
		assert(self.s[i] != '\n')
		
		while i >= 0:
			if s[i] == '\n':
				return i + 1
		
		return 0
	#@nonl
	#@-node:scanToStartOfLine
	#@+node:scanToEndOfLine
	def scanToEndOfLine (self,i):
		
		if index >= len(self.s):
			return len(self.s)
			
		assert(self.s[i] != '\n')
		
		while i < len(s):
			if s[i] == '\n':
				return i - 1
		
		return i
	#@nonl
	#@-node:scanToEndOfLine
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
	#@nonl
	#@-node:Must be overriden in subclasses
	#@+node:Bounding box
	def bbox(self,index):
		return (0,0)
	#@nonl
	#@-node:Bounding box
	#@+node:Color tags
	def tag_add (self,tagName,index1,index2):
		pass
	
	def tag_bind (self,tagName,event,callback):
		pass
	
	def tag_configure (self,colorName,**keys):
		pass
	
	def tag_delete(self,tagName):
		pass
	
	def tag_remove (self,tagName,index1,index2):
		pass
	#@nonl
	#@-node:Color tags
	#@+node:Configuration
	def cget(self,*args,**keys):
		pass
		
	def configure (self,*args,**keys):
		pass
	#@nonl
	#@-node:Configuration
	#@+node:Focus
	def hasFocus (self):
		return true
		
	def setFocus (self):
		pass
	#@nonl
	#@-node:Focus
	#@+node:Height & width (use dummy values...)
	def getBodyPaneHeight (self):
		
		return 500
	
	def getBodyPaneWidth (self):
	
		return 600
	#@nonl
	#@-node:Height & width (use dummy values...)
	#@+node:Idle time...
	def scheduleIdleTimeRoutine (self,function,*args,**keys):
	
		trace()
	#@nonl
	#@-node:Idle time...
	#@+node:Indices
	def adjustIndex (self,index,offset):
		return index + offset
		
	def compareIndices(self,i,rel,j):
	
		return eval("%d %s %d" % (i,rel,j))
		
	def convertRowColumnToIndex (self,row,column):
		
		# Probably not used.
		n = self.findStartOfLine(row)
		trace(n + column)
		return n + column
		
	def convertIndexToRowColumn (self,index):
		
		# Probably not used.
		trace(index)
		return index
		
	def getImageIndex (self,image):
		self.oops()
	#@-node:Indices
	#@+node:Insert point
	def getBeforeInsertionPoint (self):
		return self.insertPoint - 1
	
	def getInsertionPoint (self):
		return self.insertPoint
		
	def getCharAtInsertPoint (self):
		try: return self.s[self.insertPoint]
		except: return None
	
	def getCharBeforeInsertPoint (self):
		try: return self.s[self.insertPoint - 1]
		except: return None
		
	def makeInsertPointVisible (self):
		pass
		
	def setInsertionPoint (self,index):
		self.insertPoint = index
	
	def setInsertionPointToEnd (self):
		self.insertPoint = len(self.s)
		
	def setInsertPointToStartOfLine (self,lineNumber): # zero-based line number
		self.insertPoint = self.findStartOfLine(lineNumber)
	#@nonl
	#@-node:Insert point
	#@+node:Menus
	def bind (self,*args,**keys):
		pass
	#@-node:Menus
	#@+node:Selection
	def deleteTextSelection (self):
		i,j = self.selection
		self.s = self.s[:i] + self.s[j:]
		
	def getSelectedText (self):
		i,j = self.selection
		trace(self.s[i:j])
		return self.s[i:j]
		
	def getTextSelection (self):
		trace(self.selection)
		return self.selection
		
	def hasTextSelection (self):
		i,j = self.selection
		return i != j
		
	def selectAllText (self):
		self.selection = 0,len(self.s)
		
	def setTextSelection (self,i,j=None):
		trace(i,j)
		if i is None:
			self.selection = 0,0
		elif j is None:
			self.selection = i # a tuple
		else:
			self.selection = i,j
	#@nonl
	#@-node:Selection
	#@+node:delete...
	def deleteAllText(self):
		self.insertPoint = 0
		self.selection = 0,0
		self.s = "" # The body text
	
	def deleteCharacter (self,index):
		self.s = self.s[:index] + self.s[index+1:]
		
	def deleteLastChar (self):
		if self.s:
			del self.s[-1]
		
	def deleteLine (self,lineNumber): # zero based line number.
		self.deleteLines(lineNumber,1)
		
	def deleteLines (self,line1,numberOfLines): # zero based line numbers.
		n1 = self.findStartOfLine(lineNumber)
		n2 = self.findStartOfLine(lineNumber+numberOfLines+1)
		if n2:
			self.s = self.s[:n1] + self.s[n2:]
		else:
			self.s = self.s[:n1]
		
	def deleteRange (self,index1,index2):
		del self.s[index1:index2]
	#@nonl
	#@-node:delete...
	#@+node:get...
	def getAllText (self):
		return toUnicode(self.s,app.tkEncoding)
		
	def getCharAtIndex (self,index):
		
		try:
			s = self.s[index]
			return toUnicode(s,app.tkEncoding)
		except: return None
		
	def getTextRange (self,index1,index2):
	
		s = self.s[index1:index2]
		return toUnicode(s,app.tkEncoding)
	#@nonl
	#@-node:get...
	#@+node:getInsertLines
	def getInsertLines (self):
		
		"""Return before,after where:
			
		before is all the lines before the line containing the insert point.
		sel is the line containing the insert point.
		after is all the lines after the line containing the insert point.
		
		All lines end in a newline, except possibly the last line."""
	
		n1 = self.scanToStartOfLine(self.insertPoint)
		n2 = self.scanToEndOfLine(self.insertPoint)
		
		before = self.s[:n1]
		sel    = self.s[n1:n2+1]
		after  = self.s[n2+1:]
	
		before = toUnicode(before,app.tkEncoding)
		ins    = toUnicode(ins,   app.tkEncoding)
		after  = toUnicode(after ,app.tkEncoding)
	
		return before,ins,after
	#@-node:getInsertLines
	#@+node:getSelectionAreas
	def getSelectionAreas (self):
		
		"""Return before,sel,after where:
			
		before is the text before the selected text
		(or the text before the insert point if no selection)
		sel is the selected text (or "" if no selection)
		after is the text after the selected text
		(or the text after the insert point if no selection)"""
		
		if not self.hasTextSelection():
			n1,n2 = self.insertPoint,self.insertPoint
		else:
			n2,n2 = self.selection
	
		before = self.s[:n1]
		sel    = self.s[n1:n2+1]
		after  = self.s[n2+1:]
		
		before = toUnicode(before,app.tkEncoding)
		sel    = toUnicode(sel,   app.tkEncoding)
		after  = toUnicode(after ,app.tkEncoding)
		return before,sel,after
	#@nonl
	#@-node:getSelectionAreas
	#@+node:getSelectionLines
	def getSelectionLines (self):
		
		"""Return before,sel,after where:
			
		before is the all lines before the selected text
		(or the text before the insert point if no selection)
		sel is the selected text (or the line containing the insert point if no selection)
		after is all lines after the selected text
		(or the text after the insert point if no selection)"""
		
		# At present, called only by c.getBodyLines.
		if not self.hasTextSelection():
			start,end = self.insertPoint,self.insertPOint
		else:
			start,end = self.selection
	
		n1 = self.scanToStartOfLine(start)
		n2 = self.scanToEndOfLine(end)
	
		before = self.s[:n1]
		sel    = self.s[n1:n2+1]
		after  = self.s[n2+1:]
		
		before = toUnicode(before,app.tkEncoding)
		sel    = toUnicode(sel,   app.tkEncoding)
		after  = toUnicode(after ,app.tkEncoding)
		return before,sel,after
	#@nonl
	#@-node:getSelectionLines
	#@+node:Insert...
	def insertAtInsertPoint (self,s):
		
		i = self.insertPoint
		self.s = self.s[:i] + s + self.s[i:]
		
	def insertAtEnd (self,s):
		
		self.s = self.s + s
		
	def insertAtStartOfLine (self,lineNumber,s):
		
		i = self.findStartOfLine(lineNumber)
		self.s = self.s[:i] + s + self.s[i:]
	#@nonl
	#@-node:Insert...
	#@+node:setSelectionAreas
	def setSelectionAreas (self,before,sel,after):
		
		if before is None: before = ""
		if sel    is None: sel = ""
		if after  is None: after = ""
		
		self.s = before + sel + after
		
		self.selection = len(before), len(before) + len(sel)
	#@nonl
	#@-node:setSelectionAreas
	#@+node:Visibility & scrolling
	def makeIndexVisible (self,index):
		pass
		
	def setFirstVisibleIndex (self,index):
		pass
		
	def getYScrollPosition (self):
		return 0
		
	def setYScrollPosition (self,scrollPosition):
		pass
		
	def scrollUp (self):
		pass
		
	def scrollDown (self):
		pass
	#@nonl
	#@-node:Visibility & scrolling
	#@+node:oops
	def oops(self):
	
		trace("nullBody:", callerName(2))
		pass
	#@nonl
	#@-node:oops
	#@-others
#@nonl
#@-node:class nullBody
#@+node:class nullFrame
class nullFrame (leoFrame):
	
	"""A null frame class for tests and batch execution."""
	
	def __init__ (self,title):

		leoFrame.__init__(self) # Init the base class.
		assert(self.c is None)
		self.title = title

	def finishCreate(self,c):

		self.c = c
		# Create do-nothing component objects.
		self.tree = nullTree(frame=self)
		self.body = nullBody(frame=self,parentFrame=None)
		self.log  = nullLog (frame=self,parentFrame=None)
		self.menu = leoMenu.nullMenu(frame=self)
		assert(c.undoer)
		c.undoer = leoUndo.nullUndoer(c)
		
	def oops(self):
		# trace("nullFrame:", callerName(2))
		pass # This is NOT an error.
#@nonl
#@-node:class nullFrame
#@+node:class nullLog
class nullLog (leoLog):
	
	def __init__ (self,frame=None,parentFrame=None):
		
		leoLog.__init__(self,frame,parentFrame) # Init the base class.
		if app.batchMode:
			if app.log: self.enabled = app.log.enabled
			else:       self.enabled = true
			app.log = self
		else:
			self.enabled = true
		# trace("nullLog",self.enabled)
		
	def createControl (self,parentFrame):
		pass
		
	def disable (self):
		self.enabled = false
		
	def enable (self):
		self.enabled = true

	def oops(self):
		trace("nullLog:", callerName(2))
		
	def put (self,s,color=None):
		if self.enabled:
			print s

	def putnl (self):
		pass
		
	def setFontFromConfig (self):
		pass
#@nonl
#@-node:class nullLog
#@+node:class nullTree
class nullTree (leoTree):

	#@	@+others
	#@+node: nullTree.__init__
	def __init__ (self,frame):
		
		leoTree.__init__(self,frame) # Init the base class.
		
		assert(self.frame)
		self.font = None
		self.fontName = None
		
	#@nonl
	#@-node: nullTree.__init__
	#@+node:oops
	def oops(self):
			
		# It is not an error to call this routine...
		trace("nullTree:", callerName(2))
		pass
	#@nonl
	#@-node:oops
	#@+node:Drawing
	def drawIcon(self,v,x=None,y=None):
		pass
	
	def redraw(self,event=None):
		pass
	
	def redraw_now(self):
		pass
	#@nonl
	#@-node:Drawing
	#@+node:Edit label
	def editLabel(self,v):
		pass
	
	def endEditLabel(self):
		pass
	
	def setNormalLabelState(self,v):
		pass
	#@nonl
	#@-node:Edit label
	#@+node:Scrolling
	def scrollTo(self,v):
		pass
	
	def idle_scrollTo(self,v):
		pass
	#@-node:Scrolling
	#@+node:Tree operations
	def expandAllAncestors(self,v):
	
		pass
	#@nonl
	#@-node:Tree operations
	#@+node:getFont & setFont
	def getFont(self):
	
		return self.font
		
	def setFont(self,font=None,fontName=None):
	
		self.font = font
		self.fontName = fontName
	#@nonl
	#@-node:getFont & setFont
	#@+node:select
	def select(self,v,updateBeadList=true):
		
		self.setCurrentVnode(v)
		self.frame.scanForTabWidth(v)
	#@nonl
	#@-node:select
	#@-others
#@nonl
#@-node:class nullTree
#@-others
#@nonl
#@-node:@file leoFrame.py
#@-leo
