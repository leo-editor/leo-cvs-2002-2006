#@+leo-ver=4
#@+node:@file nav_buttons.py
"""Adds navigation buttons to icon bar"""

#@@language python

from leoPlugins import *
from leoGlobals import *
from leoTkinterDialog import tkinterListBoxDialog

try:
	import Tkinter
except ImportError:
	Tkinter = None
Tk = Tkinter

import os

if Tkinter: # Register the handlers...

	#@	@+others
	#@+node:class commanderInfoClass
	class commanderInfoClass:
		#@	@+others
		#@+node:__init__ (commanderInfoClass)
		def __init__ (self,c,globalInfo):
			
			self.c = c
			self.globalInfo = globalInfo
			
			# The icon frame in c.
			self.iconFrame = c.frame.iconFrame
			
			# Dialogs.
			self.marksDialog = None
			self.recentSectionsDialog = None
		
			# Images for arrow buttons.
			self.lt_nav_disabled_image = self.lt_nav_enabled_image = None
			self.rt_nav_disabled_image = self.rt_nav_enabled_image = None
			
			# The arrow and text buttons.
			self.lt_nav_button = self.rt_nav_button = None
			sections_button = self.marks_button = None
			
			self.nav_buttons = None
		#@-node:__init__ (commanderInfoClass)
		#@+node:addWidgets
		def addWidgets (self):
			
			c = self.c ; d = self
			
			d.lt_nav_disabled_image = self.createImage("../Icons/lt_arrow_disabled.gif")
			d.lt_nav_enabled_image  = self.createImage("../Icons/lt_arrow_enabled.gif")
			
			d.rt_nav_disabled_image = self.createImage("../Icons/rt_arrow_disabled.gif")
			d.rt_nav_enabled_image  = self.createImage("../Icons/rt_arrow_enabled.gif")
			
			for image in (
				self.lt_nav_disabled_image, self.lt_nav_enabled_image,
				self.rt_nav_disabled_image, self.rt_nav_enabled_image):
				if not image:
					return
			
			# It's so nice to be able to add ivars to classes at any time!
			self.lt_nav_button = c.frame.addIconButton(
				image=self.lt_nav_disabled_image,
				command=c.goPrevVisitedNode)
				
			#@	<< define callbacks >>
			#@+node:<< define callbacks >>
			# These are functions, not methods, so we must bind self at definition time.
			
			def onMarksButton(self=self):
			
				self.marksButtonCallback()
				
			def onRecentButton(self=self):
			
				self.recentButtonCallback()
			#@nonl
			#@-node:<< define callbacks >>
			#@nl
		
			self.sections_button = c.frame.addIconButton(
				text="Recent",command=onRecentButton)
				
			self.marks_button = c.frame.addIconButton(
				text="Marks",command=onMarksButton)
			
			self.rt_nav_button = c.frame.addIconButton(
				image=self.rt_nav_disabled_image,
				command=c.goNextVisitedNode)
				
			# Don't dim the button when it is inactive.
			for b in (self.lt_nav_button,self.rt_nav_button):
				fg = b.cget("foreground")
				b.configure(disabledforeground=fg)
				
			# Package these buttons for the recentSectionsDialog class in leoTkinterDialog.py
			self.nav_buttons = (self.lt_nav_button, self.rt_nav_button)
		#@nonl
		#@-node:addWidgets
		#@+node:createImage
		def createImage (self,path):
			
			path = os.path.join(app.loadDir,path)
			path = os.path.normpath(path)
			
			try:
				image = Tkinter.PhotoImage(master=app.root,file=path)
			except:
				es("can not load icon: " + shortFileName(path))
				image = None
			return image
		
		#@-node:createImage
		#@+node:updateNavButtons (nav_buttons.py)
		def updateNavButtons (self):	
		
			d = self ; c = self.c
			
			# Make sure we have initialized properly.
			if not hasattr(d,"lt_nav_button") or not hasattr(d,"rt_nav_button"):
				return
				
			if not d.lt_nav_button or not d.rt_nav_button: # 6/30/03
				return
			
			b = d.lt_nav_button
			if c.beadPointer > 1: # 10/19/03: A bit of a kludge.
				image = self.lt_nav_enabled_image
				state = "normal"
			else:
				image = d.lt_nav_disabled_image
				state = "normal" # "disabled" makes the icon look bad.
			b.configure(image=image,state=state)
			
			b = d.rt_nav_button
			if c.beadPointer + 1 < len(c.beadList):
				image =self.rt_nav_enabled_image
				state = "normal"
			else:
				image = self.rt_nav_disabled_image
				state = "normal" # "disabled" makes the icon look bad.
			b.configure(image=image,state=state)
		#@nonl
		#@-node:updateNavButtons (nav_buttons.py)
		#@+node:marksButtonCallback
		def marksButtonCallback(self,event=None):
			
			c = self.c ; d = self.marksDialog
		
			if d:
				d.top.deiconify()
			else:
				# Create and run the dialog.
				title = "Marks"
				label = "Marks: " + shortFileName(c.mFileName)
				d = marksDialog(c,title,label)
				self.marksDialog = d
				d.root.wait_window(d.top)
		#@-node:marksButtonCallback
		#@+node:recentButtonCallback
		def recentButtonCallback(self,event=None):
			
			c = self.c ; d = self.recentSectionsDialog
			
			if d:
				d.top.deiconify()
				d.fillbox()
			else:
				# Create and run the dialog.]
				title = "Recent Nodes"
				label = "Recent nodes: " + shortFileName(c.mFileName)
				d = recentSectionsDialog(c,self.nav_buttons,title,label)
				self.recentSectionsDialog = d
				d.root.wait_window(d.top)
		#@-node:recentButtonCallback
		#@-others
	#@nonl
	#@-node:class commanderInfoClass
	#@+node:class globalInfoClass
	class globalInfoClass:
		#@	@+others
		#@+node:__init__ ( globalInfoClass)
		def __init__ (self):
			
			self.commanderInfo = {} # keys are commanders, values are navCommanderInfo objects
		#@-node:__init__ ( globalInfoClass)
		#@+node:addNavWidgets
		def addNavWidgets(self,tag,keywords):
			
			c = keywords.get("c")
			
			# Create the commanderInfo object.
			d = commanderInfoClass(c,self)
			self.commanderInfo[c] = d
			
			# Add the widgets.
			d.addWidgets()
			
		#@-node:addNavWidgets
		#@+node:destroyFrame, destroyAllFrames, destroyOneFrame
		def destroyAllFrames(self,tag,keywords):
			
			for d in self.commanderInfo.values():
				self.destroyOneFrame(d)
				
		def destroyFrame(self,tag,keywords):
		
			c = keywords.get("c")
			d = self.commanderInfo.get(c)
			if d:
				self.destroyOneFrame(d)
				
		def destroyOneFrame(self,d):
		
			if d.marksDialog:
				d.marksDialog.top.destroy()
			if d.recentSectionsDialog:
				d.recentSectionsDialog.top.destroy()
			del self.commanderInfo[d.c]
		#@nonl
		#@-node:destroyFrame, destroyAllFrames, destroyOneFrame
		#@+node:updateRecentSections
		def updateRecentSections (self,tag,keywords):
			
			c = keywords.get("c")
			info = self.commanderInfo.get(c)
		
			if info:
				info.updateNavButtons()
				d = info.recentSectionsDialog
				if d:
					d.fillbox()
		#@-node:updateRecentSections
		#@+node:updateMarks & updateMarksAfterCommand
		def updateMarksAfterCommand (self,tag,keywords):
			
			"""Update the marks dialog when a new window is opened."""
			
			name = keywords.get("label")
			
			if name and name.lower() in ("open","new"):
				self.updateMarks(tag,keywords)
			
		def updateMarks (self,tag,keywords):
			
			"""Update the marks dialog."""
			
			c = keywords.get("c")
			# trace()
			info = self.commanderInfo.get(c)
			if info and info.marksDialog:
				info.marksDialog.fillbox()
		#@nonl
		#@-node:updateMarks & updateMarksAfterCommand
		#@+node:updateNavButtons
		def updateNavButtons (self,tag,keywords):
		
			"""Update the colors of c's nav buttons"""
			
			c = keywords.get("c")
			info = self.commanderInfo.get(c)
			
			if info:
				info.updateNavButtons()
		#@-node:updateNavButtons
		#@-others
	#@nonl
	#@-node:class globalInfoClass
	#@+node:class marksDialog (listBoxDialog)
	class marksDialog (tkinterListBoxDialog):
		
		"""A class to create the marks dialog"""
	
		#@	@+others
		#@+node:marksDialog.__init__
		def __init__ (self,c,title,label):
			
			"""Create a Marks listbox dialog."""
		
			tkinterListBoxDialog.__init__(self,c,title,label)
		#@-node:marksDialog.__init__
		#@+node:createFrame
		def createFrame(self):
			
			"""Create the frame for a Marks listbox dialog."""
		
			tkinterListBoxDialog.createFrame(self)
			self.addButtons()
		#@nonl
		#@-node:createFrame
		#@+node:addbuttons
		def addButtons (self):
			
			"""Add buttons to a Marks listbox dialog."""
			
			f = Tk.Frame(self.outerFrame)
			f.pack()
			self.addStdButtons(f)
		#@nonl
		#@-node:addbuttons
		#@+node:fillbox
		def fillbox(self,event=None):
		
			"""Update a Marks listbox dialog and update the listbox and update vnodeList & tnodeList ivars"""
		
			self.box.delete(0,"end")
			self.vnodeList = []
			self.tnodeList = []
		
			# Make sure the node still exists.
			# Insert only the last cloned node.
			c = self.c ; v = c.rootVnode()
			i = 0
			while v:
				if v.isMarked() and v.t not in self.tnodeList:
					self.box.insert(i,v.headString().strip())
					self.tnodeList.append(v.t)
					self.vnodeList.append(v)
					i += 1
				v = v.threadNext()
		#@nonl
		#@-node:fillbox
		#@-others
	#@nonl
	#@-node:class marksDialog (listBoxDialog)
	#@+node:class recentSectionsDialog (tkinterListBoxDialog)
	class recentSectionsDialog (tkinterListBoxDialog):
		
		"""A class to create the recent sections dialog"""
	
		#@	@+others
		#@+node:__init__  recentSectionsDialog
		def __init__ (self,c,buttons,title,label):
			
			"""Create a Recent Sections listbox dialog."""
			
			self.lt_nav_iconFrame_button, self.rt_nav_iconFrame_button = buttons
		
			tkinterListBoxDialog.__init__(self,c,title,label)
		
		#@-node:__init__  recentSectionsDialog
		#@+node:addButtons
		def addButtons (self):
			
			"""Add buttons for a Recent Sections listbox dialog."""
		
			self.buttonFrame = f = Tk.Frame(self.outerFrame)
			f.pack()
			
			row1 = Tk.Frame(f)
			row1.pack()
			
			# Create the back and forward buttons, cloning the images & commands of the already existing buttons.
			image   = self.lt_nav_iconFrame_button.cget("image")
			command = self.lt_nav_iconFrame_button.cget("command")
		
			self.lt_nav_button = b = Tk.Button(row1,image=image,command=command)
			b.pack(side="left",pady=2,padx=5)
			
			image   = self.rt_nav_iconFrame_button.cget("image")
			command = self.rt_nav_iconFrame_button.cget("command")
		
			self.rt_nav_button = b = Tk.Button(row1,image=image,command=command)
			b.pack(side="left",pady=2,padx=5)
			
			row2 = Tk.Frame(f)
			row2.pack()
			self.addStdButtons(row2)
			
			row3 = Tk.Frame(f)
			row3.pack()
			
			self.clear_button = b =  Tk.Button(row3,text="Clear All",
				width=6,command=self.clearAll)
			b.pack(side="left",pady=2,padx=5)
			
			self.delete_button = b =  Tk.Button(row3,text="Delete",
				width=6,command=self.deleteEntry)
			b.pack(side="left",pady=2,padx=5)
		#@-node:addButtons
		#@+node:clearAll
		def clearAll (self,event=None):
		
			"""Handle clicks in the "Delete" button of the Recent Sections listbox dialog."""
		
			self.c.visitedList = []
			self.vnodeList = []
			self.fillbox()
		#@-node:clearAll
		#@+node:createFrame
		def createFrame(self):
			
			"""Create the frame of a Recent Sections listbox dialog."""
			
			tkinterListBoxDialog.createFrame(self)	
			self.addButtons()
		#@-node:createFrame
		#@+node:deleteEntry
		def deleteEntry (self,event=None):
		
			"""Handle clicks in the "Delete" button of a Recent Sections listbox dialog."""
			
			c = self.c ; box = self.box
			
			# Work around an old Python bug.  Convert strings to ints.
			items = box.curselection()
			try:
				items = map(int, items)
			except ValueError: pass
		
			if items:
				n = items[0]
				v = self.vnodeList[n]
				del self.vnodeList[n]
				if v in c.visitedList:
					c.visitedList.remove(v)
				self.fillbox()
		#@-node:deleteEntry
		#@+node:destroy
		def destroy (self,event=None):
			
			"""Hide a Recent Sections listbox dialog and mark it inactive.
			
			This is an escape from possible performace penalties"""
				
			# This is enough to disable fillbox.
			self.top.withdraw()
		#@-node:destroy
		#@+node:fillbox (recent sections)
		def fillbox(self,event=None):
		
			"""Update a Recent Sections listbox dialog and update vnodeList & tnodeList ivars"""
		
			# Only fill the box if the dialog is visible.
			# This is an important protection against bad performance.
		
			if self.top.state() == "normal":
				#@		<< reconstruct the contents of self.box >>
				#@+node:<< reconstruct the contents of self.box >>>
				c = self.c
				
				self.box.delete(0,"end")
				self.vnodeList = []
				self.tnodeList = []
				
				# Make sure the node still exists.
				# Insert only the last cloned node.
				i = 0
				for v in c.visitedList:
					if v.exists(self.c) and v.t not in self.tnodeList:
						self.box.insert(i,v.headString().strip())
						self.tnodeList.append(v.t)
						self.vnodeList.append(v)
						i += 1
				#@-node:<< reconstruct the contents of self.box >>>
				#@nl
				self.synchButtons()
		#@nonl
		#@-node:fillbox (recent sections)
		#@+node:synchNavButtons
		def synchButtons (self):
			
			"""Synchronize the arrow boxes of a Recent Sections listbox dialog."""
		
			image = self.lt_nav_iconFrame_button.cget("image")
			self.lt_nav_button.configure(image=image)
			
			image = self.rt_nav_iconFrame_button.cget("image")
			self.rt_nav_button.configure(image=image)
		#@nonl
		#@-node:synchNavButtons
		#@-others
	#@nonl
	#@-node:class recentSectionsDialog (tkinterListBoxDialog)
	#@-others
	
	globalInfo = globalInfoClass()

	if app.gui is None:
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":

		registerHandler("after-create-leo-frame", globalInfo.addNavWidgets)
		registerHandler("select2",globalInfo.updateRecentSections)
		registerHandler("command2",globalInfo.updateMarksAfterCommand)
		registerHandler(("set-mark","clear-mark"),globalInfo.updateMarks)
		registerHandler("close-frame",globalInfo.destroyFrame)
		registerHandler("destroy-all-global-windows",globalInfo.destroyAllFrames)

		__version__ = "1.2"
		plugin_signon(__name__)
#@nonl
#@-node:@file nav_buttons.py
#@-leo
