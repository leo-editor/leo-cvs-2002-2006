# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoGui.py
#@@first

"""A module containing the base leoGui class.

This class and its subclasses hides the details of which gui is actually being used.
Leo's core calls this class to allocate all gui objects.

Plugins may define their own gui classes by setting app.gui."""

from leoGlobals import *
import leoCommands
import os,sys,traceback

#@+others
#@+node:class leoGui
class leoGui:
	
	"""The base class of all gui classes.
	
	Subclasses are expected to override all do-nothing methods of this class."""
	
	#@	@+others
	#@+node:leoGui.__init__
	def __init__ (self,guiName):
		
		# trace("leoGui",guiName)
		
		self.leoIcon = None
		self.mGuiName = guiName
		self.mainLoop = None
		self.root = None
	#@nonl
	#@-node:leoGui.__init__
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
	#@+node:interface to Leo's core
	#@+at 
	#@nonl
	# Leo's core code calls these routine to create commanders and the 
	# corresponding frame objects.
	#@-at
	#@nonl
	#@-node:interface to Leo's core
	#@+node: newLeoCommanderAndFrame
	def newLeoCommanderAndFrame(self,fileName):
		
		"""Create a commander and its view frame for the Leo main window."""
		
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
		frame = app.gui.newLeoFrame(title)
		
		# Create the commander and its subcommanders.
		c = leoCommands.Commands(frame,fileName)
		
		# Finish creating the frame (kludge: sets c.bodyCtrl so it can create the outline.)
		frame.finishCreate(c)
		c.log = c.frame.log # Kludge: should replace c.log by abstract log routines.
		
		# Finish initing the subcommanders.
		c.undoer.clearUndoState() # Menus must exist at this point.
		
		doHook("after-create-leo-frame",c=c)
		return c,frame
	#@nonl
	#@-node: newLeoCommanderAndFrame
	#@+node:destroySelf
	def destroySelf (self,frame):
	
		self.oops()
	#@nonl
	#@-node:destroySelf
	#@+node:destroy
	def destroy (self,widget):
	
		self.oops()
	#@nonl
	#@-node:destroy
	#@+node:base-class methods: overridden in subclasses
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
	#@-node:base-class methods: overridden in subclasses
	#@+node:Birth, death & rebirth
	def createRootWindow(self):
		"""Create the hidden root window for the gui.
		
		Nothing needs to be done if the root window need not exist."""
		self.oops()
		
	def finishCreate (self):
		"""Do any remaining chores after the root window has been created."""
		self.oops()
	
	def killGui(self,exitFlag=true):
		"""Destroy the gui.
		
		The entire Leo application should terminate if exitFlag is true."""
		self.oops()
	
	def recreateRootWindow(self):
		"""Create the hidden root window of the gui
	    after a previous gui has terminated with killGui(false)."""
		self.oops()
	#@-node:Birth, death & rebirth
	#@+node:Clipboard
	def replaceClipboardWith (self,s): self.oops()
	def getTextFromClibboard (self):   self.oops()
	#@nonl
	#@-node:Clipboard
	#@+node:Creating and running dialogs (leoGui)
	def runAboutLeoDialog(self,version,copyright,url,email):
		"""Create and run an About Leo dialog."""
		self.oops()
		
	def runAskLeoIDDialog(self,version,copyright,url,email):
		"""Create and run a dialog to get app.LeoID."""
		self.oops()
	
	def runAskOkDialog(self,title,message=None,text="Ok"):
		"""Create and run an askOK dialog ."""
		self.oops()
	
	def runAskOkCancelNumberDialog(self,title,message):
		"""Create and run an askOkCancelNumber dialog ."""
		self.oops()
	
	def runAskYesNoDialog(self,title,message=None):
		"""Create and run an askYesNo dialog."""
		self.oops()
	
	def runAskYesNoCancelDialog(self,title,
		message=None,yesMessage="Yes",noMessage="No",defaultButton="Yes"):
		"""Create and run an askYesNoCancel dialog ."""
		self.oops()
		
	def runOpenFileDialog(self,title,filetypes,defaultextension):
		"""Create and run an open file dialog ."""
		self.oops()
		
	def runSaveFileDialog(self,initialfile,title,filetypes,defaultextension):
		"""Create and run an open file dialog ."""
		self.oops()
	#@nonl
	#@-node:Creating and running dialogs (leoGui)
	#@+node:Creating and running panels (leoGui)
	def createFindPanel(self):
		"""Create a hidden find panel."""
		self.oops()
	
	def runColorPanel(self):
		"""Create and run an About Leo dialog."""
		self.oops()
		
	def runColorNamePanel(self,colorPanel,name,color):
		"""Create and run an About Leo dialog."""
		self.oops()
		
	def showColorPanel(self,colorPanel):
		"""Show a color panel."""
		self.oops()
	#@nonl
	#@-node:Creating and running panels (leoGui)
	#@+node:Creating frames
	def newColorFrame(self,commander):
		"""Create a colorFrame."""
		self.oops()
	
	def newColorNameFrame(self,commander):
		"""Create a colorNameFrame."""
		self.oops()
	
	def newCompareFrame(self,commander):
		"""Create a compareFrame."""
		self.oops()
	
	def newFindFrame(self,commander):
		"""Create a findFrame."""
		self.oops()
	
	def newFontFrame(self,commander):
		"""Create a fontFrame."""
		self.oops()
	
	def newLeoFrame(self,title):
		"""Create a view frame for the Leo main window."""
		self.oops()
	
	def newPrefsFrame(self,commander):
		"""Create a prefsFrame."""
		self.oops()
	#@nonl
	#@-node:Creating frames
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
	#@+node:Focus (leoGui)
	def get_focus(self,frame):
		"""Return the widget that has focus, or the body widget if None."""
		self.oops()
			
	def set_focus(self,commander,widget):
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		self.oops()
		
	def force_focus(self,commander,widget):
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		self.oops()
	#@nonl
	#@-node:Focus (leoGui)
	#@+node:Idle time (leoGui)
	def setIdleTimeHook (self,idleTimeHookHandler,*args,**keys):
		
		self.oops()
		
	def setIdleTimeHookAfterDelay (self,delay,idleTimeHookHandler,*args,**keys):
		
		self.oops()
	#@-node:Idle time (leoGui)
	#@+node:runMainLoop
	def runMainLoop(self):
	
		"""Run the gui's main loop."""
		self.oops()
	#@nonl
	#@-node:runMainLoop
	#@-others
#@nonl
#@-node:class leoGui
#@-others
#@nonl
#@-node:@file leoGui.py
#@-leo
