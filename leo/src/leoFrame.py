#@+leo-ver=4
#@+node:@file leoFrame.py
"""The base classes for all Leo Windows, their body, log and tree panes, key bindings and menus.

These classes should be overridden to create frames for a particular gui."""

from leoGlobals import *

#@+others
#@+node:class leoBody
class leoBody:
	
	"""The base class for the body pane in Leo windows."""
	
	#@	@+others
	#@+node:leoBody.__init__
	def __init__ (self,frame,parentFrame):
	
		self.frame = frame
		self.c = frame.commands
	
		self.bodyCtrl = self.createControl(frame,parentFrame)
		self.setBodyFontFromConfig()
	#@nonl
	#@-node:leoBody.__init__
	#@+node:leoBody.createControl
	def createControl (self,frame,parentFrame):
		
		self.oops()
	#@nonl
	#@-node:leoBody.createControl
	#@+node:Body abstractions
	# The corresponding routines in the derived class is called from Leo's core.
	
	# Bounding box...
	def getBoundingBox (self,index): self.oops()
	
	# Colorizer tags...
	def bindColor (self,tagName,event,callback):   self.oops()
	def colorRange (self,tagName,index1,index2):   self.oops()
	def configureColor (self,colorName,**keys):    self.oops()
	def removeColor(self,tagName):                 self.oops()
	def uncolorRange (self,tagName,index1,index2): self.oops()
	
	# Focus...
	def hasFocus (self): self.oops()
	def setFocus (self): self.oops()
	
	# Font...
	def setBodyFontFromConfig(self): self.oops()
	
	# Getting & setting text...
	# (These routines replace most of the former insert/delete and index routines)
	def getAllText (self):                         self.oops()
	def getInsertLines (self):                     self.oops()
	def getSelectionAreas (self):                  self.oops()
	def getSelectionLines (self):                  self.oops()
	def setSelectionAreas (self,before,sel,after): self.oops() # A very powerful routine.
	
	# Idle-time callback.
	def scheduleIdleTimeRoutine (self,function,*args,**keys): self.oops()
	
	# Indices...
	def convertXYToIndex (self,x,y):               self.oops()
	def convertRowColumnToIndex (self,row,column): self.oops()
	def getImageIndex (self,image):                self.oops()
	
	# Height & width info...
	def getBodyPaneHeight (self): self.oops()
	def getBodyPaneWidth (self):  self.oops()
	
	# Selection & insertion point...
	def getInsertionPoint (self):       self.oops()
	def getTextSelection (self):        self.oops()
	def selectAllText (self):           self.oops()
	def setInsertionPoint (self,index): self.oops()
	def setTextSelection (self,i,j):    self.oops()
	
	# Visibility & scrolling...
	def makeIndexVisible (self,index):     self.oops()
	def setFirstVisibleIndex (self,index): self.oops()
	def getFirstVisibleIndex (self):       self.oops()
	def scrollUp (self):                   self.oops()
	def scrollDown (self):                 self.oops()
	#@-node:Body abstractions
	#@+node:leoBody.oops
	def oops (self):
	
		print "leoBody oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:leoBody.oops
	#@-others
#@nonl
#@-node:class leoBody
#@+node:class leoFrame
class leoFrame:
	
	"""The base class for all Leo windows."""
	
	#@	@+others
	#@+node:leoFrame abstractions
	def getMenu (self,name): self.oops()
	#@nonl
	#@-node:leoFrame abstractions
	#@+node:leoFrame.oops
	def oops (self):
	
		print "leoFrame oops:", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:leoFrame.oops
	#@-others
#@nonl
#@-node:class leoFrame
#@+node:class leoKeys (not used yet)
class leoKeys:
	
	"""The base class for key bindings in Leo windows."""
	
	#@	@+others
	#@-others
#@nonl
#@-node:class leoKeys (not used yet)
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
#@+node:class leoMenus (not used yet)
class leoMenus:
	
	"""The base class for menus in Leo windows."""
	
	#@	@+others
	#@-others
#@nonl
#@-node:class leoMenus (not used yet)
#@+node:class leoTree
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
