# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoTkinterGui.py
#@@first

"""Leo's Tkinter Gui module."""

from leoGlobals import *
import leoGui
import leoTkinterColorPanels,leoTkinterDialog,leoTkinterFind,leoTkinterFrame
import tkFont,Tkinter,tkFileDialog

Tk = Tkinter

class tkinterGui(leoGui.leoGui):
	
	"""A class encapulating all calls to tkinter."""
	
	#@	@+others
	#@+node: tkinterGui.__init__
	def __init__ (self):
		
		# trace("tkinterGui")
		
		# Initialize the base class.
		leoGui.leoGui.__init__(self,"tkinter")
		
		self.bitmap_name = None
		self.bitmap = None
	#@nonl
	#@-node: tkinterGui.__init__
	#@+node:createRootWindow & allies
	def createRootWindow(self):
	
		"""Create a hidden Tk root window."""
	
		self.root = root = Tkinter.Tk()
		root.title("Leo Main Window")
		root.withdraw()
		
		self.setDefaultIcon()
		self.getDefaultConfigFont(app.config)
		self.createGlobalWindows()
	
		return root
	#@nonl
	#@-node:createRootWindow & allies
	#@+node:setDefaultIcon
	def setDefaultIcon(self):
		
		"""Set the icon to be used in all Leo windows.
		
		This code does nothing for Tk versions before 8.4.3."""
		
		gui = self
	
		try:
			version = gui.root.getvar("tk_patchLevel")
			if CheckVersion(version,"8.4.3"):
				# tk 8.4.3 or greater: load a 16 by 16 icon.
				path = os.path.join(app.loadDir,"..","Icons")
				if os.path.exists(path):
					file = os.path.join(path,"LeoApp16.ico")
					if os.path.exists(path):
						self.bitmap = Tkinter.BitmapImage(file)
					else:
						es("LeoApp16.ico not in Icons directory", color="red")
				else:
					es("Icons directory not found: "+path, color="red")
		except:
			print "exception setting bitmap"
			traceback.print_exc()
	#@nonl
	#@-node:setDefaultIcon
	#@+node:getDefaultConfigFont
	def getDefaultConfigFont(self,config):
		
		"""Get the default font from a new text widget."""
	
		t = Tkinter.Text()
		fn = t.cget("font")
		font = tkFont.Font(font=fn)
		config.defaultFont = font
		config.defaultFontFamily = font.cget("family")
	#@nonl
	#@-node:getDefaultConfigFont
	#@+node:createGlobalWindows
	def createGlobalWindows (self):
		
		"""Create the global windows for the application."""
	
		app.findFrame = app.gui.createFindPanel()
		app.globalWindows.append(app.findFrame)
	#@nonl
	#@-node:createGlobalWindows
	#@+node:destroySelf
	if 0:
		def destroySelf (self,frame):
			trace()
			self.top.destroy()
	#@nonl
	#@-node:destroySelf
	#@+node:destroy
	if 0:
		def destroy(self,widget):
			trace()
			widget.destroy()
	#@nonl
	#@-node:destroy
	#@+node:finishCreate
	def finishCreate (self):
		
		pass
		
	#@-node:finishCreate
	#@+node:killGui (not used)
	def killGui(self,exitFlag=true):
		
		"""Destroy a gui and terminate Leo if exitFlag is true."""
	
		pass # Not ready yet.
	
	#@-node:killGui (not used)
	#@+node:recreateRootWindow (not used)
	def recreateRootWindow(self):
		"""A do-nothing base class to create the hidden root window of a gui
	
		after a previous gui has terminated with killGui(false)."""
		pass
	
	#@-node:recreateRootWindow (not used)
	#@+node:runMainLoop
	def runMainLoop(self):
	
		"""Run tkinter's main loop."""
	
		# trace("tkinterGui")
		self.root.mainloop()
	#@nonl
	#@-node:runMainLoop
	#@+node:getFontFromParams
	def getFontFromParams(self,family,size,slant,weight):
		
		family_name = family
		
		try:
			font = tkFont.Font(family=family,size=size,slant=slant,weight=weight)
			#print family_name,family,size,slant,weight
			#print "actual_name:",font.cget("family")
			return font
		except:
			es("exception setting font from " + `family_name`)
			es("family,size,slant,weight:"+
				`family`+':'+`size`+':'+`slant`+':'+`weight`)
			es_exception()
			return app.config.defaultFont
	#@nonl
	#@-node:getFontFromParams
	#@+node:Clipboard (leoTkinterGui)
	def replaceClipboardWith (self,s):
	
		self.root.clipboard_clear()
		self.root.clipboard_append(s)
		
	def getTextFromClibboard (self):
		
		try:
			return self.root.selection_get(selection="CLIPBOARD")
		except:
			return None
	#@nonl
	#@-node:Clipboard (leoTkinterGui)
	#@+node:Idle Time (leoTkinterGui)
	def setIdleTimeHook (self,idleTimeHookHandler,*args,**keys):
		
		# trace(idleTimeHookHandler)
		if self.root:
			self.root.after_idle(idleTimeHookHandler,*args,**keys)
			
	def setIdleTimeHookAfterDelay (self,delay,idleTimeHookHandler,*args,**keys):
		
		if self.root:
			app.root.after(app.idleTimeDelay,idleTimeHookHandler)
	#@nonl
	#@-node:Idle Time (leoTkinterGui)
	#@+node:Creating and running tkinter dialogs
	def runAboutLeoDialog(self,version,copyright,url,email):
		"""Create and run a Tkinter About Leo dialog."""
		d = leoTkinterDialog.tkinterAboutLeo(version,copyright,url,email)
		return d.run(modal=false)
		
	def runAskLeoIDDialog(self):
		"""Create and run a dialog to get app.LeoID."""
		d = leoTkinterDialog.tkinterAskLeoID()
		return d.run(modal=true)
	
	def runAskOkDialog(self,title,message=None,text="Ok"):
		"""Create and run a Tkinter an askOK dialog ."""
		d = leoTkinterDialog.tkinterAskOk(title,message,text)
		return d.run(modal=true)
	
	def runAskOkCancelNumberDialog(self,title,message):
		"""Create and run askOkCancelNumber dialog ."""
		d = leoTkinterDialog.tkinterAskOkCancelNumber(title,message)
		return d.run(modal=true)
	
	def runAskYesNoDialog(self,title,message=None):
		"""Create and run an askYesNo dialog."""
		d = leoTkinterDialog.tkinterAskYesNo(title,message)
		return d.run(modal=true)
	
	def runAskYesNoCancelDialog(self,title,
		message=None,yesMessage="Yes",noMessage="No",defaultButton="Yes"):
		"""Create and run an askYesNoCancel dialog ."""
		d = leoTkinterDialog.tkinterAskYesNoCancel(
			title,message,noMessage,defaultButton)
	 	return d.run(modal=true)
	#@nonl
	#@-node:Creating and running tkinter dialogs
	#@+node:Creating and running tkinter file dialogs
	def runOpenFileDialog(self,title,filetypes,defaultextension):
	
		"""Create and run an Tkinter open file dialog ."""
	
		return tkFileDialog.askopenfilename(
			title=title,
			filetypes=filetypes,
			defaultextension=defaultextension)
	
	def runSaveFileDialog(self,initialfile,title,filetypes,defaultextension):
	
		"""Create and run an Tkinter save file dialog ."""
	
		return tkFileDialog.asksaveasfilename(
			initialfile=initialfile,
			title=title,
			filetypes=filetypes,
			defaultextension=defaultextension)
	#@nonl
	#@-node:Creating and running tkinter file dialogs
	#@+node:Creating and running tkinter panels
	def createFindPanel(self):
		"""Create a hidden Tkinter find panel."""
		panel = leoTkinterFind.leoTkinterFind()
		panel.top.withdraw()
		return panel
		
	def runColorPanel(self,c):
		"""Create and run a Tkinter color picker panel."""
		panel = leoTkinterColorPanels.leoTkinterColorPanel(c)
		panel.run()
		
	def runColorNamePanel(self,colorPanel,name,color):
		"""Create and run a Tkinter color name picker panel."""
		panel = leoTkinterColorPanels.leoTkinterColorNamePanel(colorPanel,name,color)
		panel.run(name,color)
		
	def showColorPanel(self,colorPanel):
		"""Show a Tkinter color panel."""
		# Not used at present.
		colorPanel.top.deiconify()
		colorPanel.top.lift()
	#@nonl
	#@-node:Creating and running tkinter panels
	#@+node:Creating Frames
	def newColorFrame(self,commander):
		"""Create a colorFrame."""
		pass # To do
	
	def newColorNameFrame(self,commander):
		"""Create a colorNameFrame."""
		pass # To do
	
	def newCompareFrame(self,commander):
		"""Create a compareFrame."""
		pass # To do
	
	def newFindFrame(self,commander):
		"""Create a findFrame."""
		pass # To do
	
	def newFontFrame(self,commander):
		"""Create a fontFrame."""
		pass # To do
	
	def newLeoFrame(self,title):
		"""Create a view frame for the Leo main window."""
		return leoTkinterFrame.leoTkinterFrame(title)
	
	def newPrefsFrame(self,commander):
		"""Create a prefsFrame."""
		pass # To do
	#@nonl
	#@-node:Creating Frames
	#@+node:Focus (leoTkinterGui)
	def force_focus(self,commands,widget):
		
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		
		focus = commands.frame.top.focus_displayof()
		if focus != widget:
			widget.focus_force() # Apparently it is not a good idea to call focus_force.
	
	def get_focus(self,frame):
		
		"""Returns the widget that has focus, or body if None."""
	
		return frame.top.focus_displayof()
		
	def set_focus(self,commands,widget):
		
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		
		focus = commands.frame.top.focus_displayof()
		if focus != widget:
			widget.focus_set()
	#@nonl
	#@-node:Focus (leoTkinterGui)
	#@+node:attachLeoIcon & createLeoIcon
	def attachLeoIcon (self,w):
		
		"""Try to attach a Leo icon to the Leo Window.
		
		Use tk's wm_iconbitmap function if available (tk 8.3.4 or greater).
		Otherwise, try to use the Python Imaging Library and the tkIcon package."""
	
		if self.bitmap != None:
			# We don't need PIL or tkicon: this is tk 8.3.4 or greater.
			try:
				w.wm_iconbitmap(self.bitmap)
			except:
				self.bitmap = None
		
		if self.bitmap == None:
			try:
				#@			<< try to use the PIL and tkIcon packages to draw the icon >>
				#@+node:<< try to use the PIL and tkIcon packages to draw the icon >>
				#@+at 
				#@nonl
				# This code requires Fredrik Lundh's PIL and tkIcon packages:
				# 
				# Download PIL    from 
				# http://www.pythonware.com/downloads/index.htm#pil
				# Download tkIcon from http://www.effbot.org/downloads/#tkIcon
				# 
				# Many thanks to Jonathan M. Gilligan for suggesting this 
				# code.
				#@-at
				#@@c
				
				import Image,tkIcon,_tkicon
				
				# Wait until the window has been drawn once before attaching the icon in OnVisiblity.
				def visibilityCallback(event,self=self,w=w):
					try: self.leoIcon.attach(w.winfo_id())
					except: pass
				w.bind("<Visibility>",visibilityCallback)
				if not self.leoIcon:
					# Load a 16 by 16 gif.  Using .gif rather than an .ico allows us to specify transparency.
					icon_file_name = os.path.join(app.loadDir,'..','Icons','LeoWin.gif')
					icon_file_name = os.path.normpath(icon_file_name)
					icon_image = Image.open(icon_file_name)
					if 1: # Doesn't resize.
						self.leoIcon = self.createLeoIcon(icon_image)
					else: # Assumes 64x64
						self.leoIcon = tkIcon.Icon(icon_image)
				#@nonl
				#@-node:<< try to use the PIL and tkIcon packages to draw the icon >>
				#@nl
			except:
				# traceback.print_exc()
				self.leoIcon = None
	#@nonl
	#@-node:attachLeoIcon & createLeoIcon
	#@+node:createLeoIcon
	# This code is adapted from tkIcon.__init__
	# Unlike the tkIcon code, this code does _not_ resize the icon file.
	
	def createLeoIcon (self,icon):
		
		try:
			import Image,tkIcon,_tkicon
			
			i = icon ; m = None
			# create transparency mask
			if i.mode == "P":
				try:
					t = i.info["transparency"]
					m = i.point(lambda i, t=t: i==t, "1")
				except KeyError: pass
			elif i.mode == "RGBA":
				# get transparency layer
				m = i.split()[3].point(lambda i: i == 0, "1")
			if not m:
				m = Image.new("1", i.size, 0) # opaque
			# clear unused parts of the original image
			i = i.convert("RGB")
			i.paste((0, 0, 0), (0, 0), m)
			# create icon
			m = m.tostring("raw", ("1", 0, 1))
			c = i.tostring("raw", ("BGRX", 0, -1))
			return _tkicon.new(i.size, c, m)
		except:
			return None
	#@nonl
	#@-node:createLeoIcon
	#@+node:get_window_info
	# WARNING: Call this routine _after_ creating a dialog.
	# (This routine inhibits the grid and pack geometry managers.)
	
	def get_window_info (self,top):
		
		top.update_idletasks() # Required to get proper info.
	
		# Get the information about top and the screen.
		geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
		dim,x,y = string.split(geom,'+')
		w,h = string.split(dim,'x')
		w,h,x,y = int(w),int(h),int(x),int(y)
		
		return w,h,x,y
	#@nonl
	#@-node:get_window_info
	#@+node:center_dialog
	# Center the dialog on the screen.
	# WARNING: Call this routine _after_ creating a dialog.
	# (This routine inhibits the grid and pack geometry managers.)
	
	def center_dialog(self,top):
	
		sw = top.winfo_screenwidth()
		sh = top.winfo_screenheight()
		w,h,x,y = get_window_info(top)
		
		# Set the new window coordinates, leaving w and h unchanged.
		x = (sw - w)/2
		y = (sh - h)/2
		top.geometry("%dx%d%+d%+d" % (w,h,x,y))
		
		return w,h,x,y
	#@nonl
	#@-node:center_dialog
	#@+node:create_labeled_frame
	# Returns frames w and f.
	# Typically the caller would pack w into other frames, and pack content into f.
	
	def create_labeled_frame (self,parent,
		caption=None,relief="groove",bd=2,padx=0,pady=0):
		
		Tk = Tkinter
		# Create w, the master frame.
		w = Tk.Frame(parent)
		w.grid(sticky="news")
		
		# Configure w as a grid with 5 rows and columns.
		# The middle of this grid will contain f, the expandable content area.
		w.columnconfigure(1,minsize=bd)
		w.columnconfigure(2,minsize=padx)
		w.columnconfigure(3,weight=1)
		w.columnconfigure(4,minsize=padx)
		w.columnconfigure(5,minsize=bd)
		
		w.rowconfigure(1,minsize=bd)
		w.rowconfigure(2,minsize=pady)
		w.rowconfigure(3,weight=1)
		w.rowconfigure(4,minsize=pady)
		w.rowconfigure(5,minsize=bd)
	
		# Create the border spanning all rows and columns.
		border = Tk.Frame(w,bd=bd,relief=relief) # padx=padx,pady=pady)
		border.grid(row=1,column=1,rowspan=5,columnspan=5,sticky="news")
		
		# Create the content frame, f, in the center of the grid.
		f = Tk.Frame(w,bd=bd)
		f.grid(row=3,column=3,sticky="news")
		
		# Add the caption.
		if caption and len(caption) > 0:
			caption = Tk.Label(parent,text=caption,highlightthickness=0,bd=0)
			caption.tkraise(w)
			caption.grid(in_=w,row=0,column=2,rowspan=2,columnspan=3,padx=4,sticky="w")
	
		return w,f
	#@nonl
	#@-node:create_labeled_frame
	#@-others
#@nonl
#@-node:@file leoTkinterGui.py
#@-leo
