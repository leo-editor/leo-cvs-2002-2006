#@+leo-ver=4
#@+node:@file leoFrame.py
"""The base classes for all Leo Windows, their body, log and tree panes, key bindings and menus.

These classes should be overridden to create frames for a particular gui."""

from leoGlobals import *
import leoCompare,leoFontPanel,leoNodes,leoPrefs
import os,string,sys,time,traceback

#@+others
#@+node:class leoBody
class leoBody:
	
	"""The base class for the body pane in Leo windows."""
	
	#@	@+others
	#@+node:leoBody.__init__
	def __init__ (self,frame,parentFrame):
	
		self.frame = frame
		self.c = frame.c
	
		self.bodyCtrl = self.createControl(frame,parentFrame)
		self.setBodyFontFromConfig()
	#@nonl
	#@-node:leoBody.__init__
	#@+node:Must be overriden in subclasses
	def createBindings (self,frame):
		self.oops()
	
	def createControl (self,frame,parentFrame):
		self.oops()
		
	def setBodyFontFromConfig (self):
		self.oops()
		
	def oops (self):
		print "leoBody oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:Must be overriden in subclasses
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
	#@-others
#@nonl
#@-node:class leoTree
#@-others
#@nonl
#@-node:@file leoFrame.py
#@-leo
