# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoGui.py
#@@first

"""A module containing the base leoGui class.

This class and its subclasses hides the details of which gui is actually being used.
Leo's core calls this class to allocate all gui objects.

Plugins may define their own gui classes by setting app.gui."""

from leoGlobals import *

import leoFrame # for null gui.

#@+others
#@+node:class leoGui
class leoGui:
	
	"""The base class of all gui classes.
	
	Subclasses are expected to override all do-nothing methods of this class."""
	
	#@	@+others
	#@+node: leoGui.__init__
	def __init__ (self,guiName):
		
		# trace("leoGui",guiName)
		
		self.leoIcon = None
		self.mGuiName = guiName
		self.mainLoop = None
		self.root = None
		self.utils = None
	#@nonl
	#@-node: leoGui.__init__
	#@+node:newLeoCommanderAndFrame (gui-independent)
	def newLeoCommanderAndFrame(self,fileName):
		
		"""Create a commander and its view frame for the Leo main window."""
		
		import leoCommands
		
		if not fileName: fileName = ""
		#@	<< compute the window title >>
		#@+node:<< compute the window title >>
		# Set the window title and fileName
		if fileName:
			title = computeWindowTitle(fileName)
		else:
			s = "untitled"
			n = app.numberOfWindows
			if n > 0:
				s += `n`
			title = computeWindowTitle(s)
			app.numberOfWindows = n+1
		
		#@-node:<< compute the window title >>
		#@nl
	
		# Create an unfinished frame to pass to the commanders.
		frame = app.gui.createLeoFrame(title)
		
		# Create the commander and its subcommanders.
		c = leoCommands.Commands(frame,fileName)
		
		# Finish creating the frame
		frame.finishCreate(c)
		
		# Finish initing the subcommanders.
		c.undoer.clearUndoState() # Menus must exist at this point.
		
		c.updateRecentFiles(fileName) # 12/01/03
		
		doHook("after-create-leo-frame",c=c)
		return c,frame
	#@nonl
	#@-node:newLeoCommanderAndFrame (gui-independent)
	#@+node:createRootWindow
	def createRootWindow(self):
	
		"""Create the hidden root window for the gui.
		
		Nothing needs to be done if the root window need not exist."""
	
		self.oops()
	#@nonl
	#@-node:createRootWindow
	#@+node:destroySelf
	def destroySelf (self):
	
		self.oops()
	#@nonl
	#@-node:destroySelf
	#@+node:finishCreate
	def finishCreate (self):
	
		"""Do any remaining chores after the root window has been created."""
	
		self.oops()
	#@nonl
	#@-node:finishCreate
	#@+node:killGui
	def killGui(self,exitFlag=true):
	
		"""Destroy the gui.
		
		The entire Leo application should terminate if exitFlag is true."""
	
		self.oops()
	#@nonl
	#@-node:killGui
	#@+node:recreateRootWindow
	def recreateRootWindow(self):
	
		"""Create the hidden root window of the gui
	    after a previous gui has terminated with killGui(false)."""
	
		self.oops()
	#@nonl
	#@-node:recreateRootWindow
	#@+node:runMainLoop
	def runMainLoop(self):
	
		"""Run the gui's main loop."""
	
		self.oops()
	#@nonl
	#@-node:runMainLoop
	#@+node:app.gui dialogs
	def runAboutLeoDialog(self,version,copyright,url,email):
		"""Create and run Leo's About Leo dialog."""
		self.oops()
		
	def runAskLeoIDDialog(self):
		"""Create and run a dialog to get app.LeoID."""
		self.oops()
	
	def runAskOkDialog(self,title,message=None,text="Ok"):
		"""Create and run an askOK dialog ."""
		self.oops()
	
	def runAskOkCancelNumberDialog(self,title,message):
		"""Create and run askOkCancelNumber dialog ."""
		self.oops()
	
	def runAskYesNoDialog(self,title,message=None):
		"""Create and run an askYesNo dialog."""
		self.oops()
	
	def runAskYesNoCancelDialog(self,title,
		message=None,yesMessage="Yes",noMessage="No",defaultButton="Yes"):
		"""Create and run an askYesNoCancel dialog ."""
		self.oops()
	#@nonl
	#@-node:app.gui dialogs
	#@+node:app.gui file dialogs
	def runOpenFileDialog(self,title,filetypes,defaultextension):
	
		"""Create and run an open file dialog ."""
	
		self.oops()
	
	def runSaveFileDialog(self,initialfile,title,filetypes,defaultextension):
	
		"""Create and run a save file dialog ."""
		
		self.oops()
	#@nonl
	#@-node:app.gui file dialogs
	#@+node:app.gui panels
	def createColorPanel(self,c):
		"""Create Color panel."""
		self.oops()
		
	def createComparePanel(self,c):
		"""Create Compare panel."""
		self.oops()
		
	def createFindPanel(self):
		"""Create a hidden Find panel."""
		self.oops()
	
	def createFontPanel(self,c):
		"""Create a Font panel."""
		self.oops()
		
	def createLeoFrame(self,title):
		"""Create a new Leo frame."""
		self.oops()
		
	def createPrefsPanel(self,c):
		"""Create a Prefs panel."""
		self.oops()
	#@nonl
	#@-node:app.gui panels
	#@+node:app.gui utils
	#@+at 
	#@nonl
	# Subclasses are expected to subclass all of the following methods.
	# 
	# These are all do-nothing methods: callers are expected to check for None 
	# returns.
	# 
	# The type of commander passed to methods depends on the type of frame or 
	# dialog being created.  The commander may be a Commands instance or one 
	# of its subcommanders.
	#@-at
	#@nonl
	#@-node:app.gui utils
	#@+node:Clipboard
	def replaceClipboardWith (self,s):
		
		self.oops()
	
	def getTextFromClibboard (self):
		
		self.oops()
	#@-node:Clipboard
	#@+node:Dialog utils
	def attachLeoIcon (self,window):
		"""Attach the Leo icon to a window."""
		self.oops()
		
	def center_dialog(self,dialog):
		"""Center a dialog."""
		self.oops()
		
	def create_labeled_frame (self,parent,caption=None,relief="groove",bd=2,padx=0,pady=0):
		"""Create a labeled frame."""
		self.oops()
		
	def get_window_info (self,window):
		"""Return the window information."""
		self.oops()
	#@-node:Dialog utils
	#@+node:Font
	def getFontFromParams(self,family,size,slant,weight):
		
		self.oops()
	#@nonl
	#@-node:Font
	#@+node:Focus
	def get_focus(self,frame):
	
		"""Return the widget that has focus, or the body widget if None."""
	
		self.oops()
			
	def set_focus(self,commander,widget):
	
		"""Set the focus of the widget in the given commander if it needs to be changed."""
	
		self.oops()
	#@nonl
	#@-node:Focus
	#@+node:Index
	def firstIndex (self):
	
		self.oops()
		
	def lastIndex (self):
	
		self.oops()
	#@-node:Index
	#@+node:Idle time
	def setIdleTimeHook (self,idleTimeHookHandler,*args,**keys):
		
		self.oops()
		
	def setIdleTimeHookAfterDelay (self,delay,idleTimeHookHandler,*args,**keys):
		
		self.oops()
	#@-node:Idle time
	#@+node:guiName
	def guiName(self):
		
		try:
			return self.mGuiName
		except:
			return "invalid gui name"
	#@nonl
	#@-node:guiName
	#@+node:oops
	def oops (self):
		
		print "leoGui oops", callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:oops
	#@-others
#@nonl
#@-node:class leoGui
#@+node:class nullGui (runs scripts)
class nullGui(leoGui):
	
	"""Null gui class."""
	
	#@	@+others
	#@+node: nullGui.__init__
	def __init__ (self,guiName):
		
		leoGui.__init__ (self,guiName) # init the base class.
		
		self.script = None
		self.lastFrame = None
	#@nonl
	#@-node: nullGui.__init__
	#@+node:createLeoFrame
	def createLeoFrame(self,title):
		
		"""Create a null Leo Frame."""
	
		self.lastFrame = leoFrame.nullFrame(title)
		return self.lastFrame
	#@nonl
	#@-node:createLeoFrame
	#@+node:createRootWindow
	def createRootWindow(self):
		pass
	#@nonl
	#@-node:createRootWindow
	#@+node:finishCreate
	def finishCreate (self):
		pass
	#@nonl
	#@-node:finishCreate
	#@+node:runMainLoop
	def runMainLoop(self):
	
		"""Run the gui's main loop."""
		
		if self.script:
			frame = self.lastFrame
			app.log = frame.log
			# es("Start of batch script...\n")
			self.lastFrame.c.executeScript(script=self.script)
			# es("\nEnd of batch script")
		
		# Getting here will terminate Leo.
	#@nonl
	#@-node:runMainLoop
	#@+node:oops
	def oops(self):
			
		"""Default do-nothing method for nullGui class.
		
		It is NOT an error to use this method."""
		
		trace("nullGui",callerName(2))
		pass
	#@nonl
	#@-node:oops
	#@+node:setScript
	def setScript (self,script=None,scriptFileName=None):
	
		self.script = script
		self.scriptFileName = scriptFileName
	#@nonl
	#@-node:setScript
	#@-others
#@nonl
#@-node:class nullGui (runs scripts)
#@-others
#@nonl
#@-node:@file leoGui.py
#@-leo
