# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoGui.py
#@@first # -*- coding: utf-8 -*-

"""A module containing all of Leo's default gui code.

Plugins may define their own gui classes by setting app.gui."""

from leoGlobals import *
import leoFind
import os,sys,tkFont,Tkinter,traceback

Tk = Tkinter

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
	#@+node:__getattr__ & ignoreUnknownAttr
	if 0: # This makes debugging difficult.
		def __getattr__(self,name):
		
			"""tkinterGui.__getattr to handle unknown calls without crashing."""
			
			print "leoGui.__getattr__: not found:",name
			return self.ignoreUnknownAttr
		
	def  ignoreUnknownAttr(self,*args,**keys):
		
		"""A universal do-nothing routine that can be returned by __getattr__."""
		pass
	#@nonl
	#@-node:__getattr__ & ignoreUnknownAttr
	#@+node:guiName
	def guiName(self):
		
		try:
			return self.mGuiName
		except:
			return "invalid gui name"
	#@nonl
	#@-node:guiName
	#@+node:do-nothing methods
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
	#@-node:do-nothing methods
	#@+node:Birth, death & rebirth
	def createRootWindow(self):
		"""A do-nothing base class to create the hidden root window for a gui.
		
		Nothing needs to be done if the root window need not exist."""
		pass
	
	def killGui(self,exitFlag=true):
		"""A do-nothing base class to destroy a gui.
		
		The entire Leo application should terminate if exitFlag is true."""
		pass
	
	def recreateRootWindow(self):
		"""A do-nothing base class to create the hidden root window of a gui
	
		after a previous gui has terminated with killGui(false)."""
		pass
	
	#@-node:Birth, death & rebirth
	#@+node:runMainLoop
	def runMainLoop(self):
	
		"""A do-nothing base class to run the gui's main loop."""
		
		pass
	#@nonl
	#@-node:runMainLoop
	#@+node:Creating Frames
	def newColorFrame(self,commander):
		"""A do-nothing base class to create a colorFrame."""
		pass
	
	def newColorNameFrame(self,commander):
		"""A do-nothing base class to create a colorNameFrame."""
		pass
	
	def newCompareFrame(self,commander):
		"""A do-nothing base class to create a compareFrame."""
		pass
	
	def newFindFrame(self,commander):
		"""A do-nothing base class to create a findFrame."""
		pass
	
	def newFontFrame(self,commander):
		"""A do-nothing base class to create a fondFrame."""
		pass
	
	def newLeoFrame(self,commander):
		"""A do-nothing base class to create a view frame for the Leo main window."""
		pass
	
	def newPrefsFrame(self,commander):
		"""A do-nothing base class to create a prefsFrame."""
		pass
	#@nonl
	#@-node:Creating Frames
	#@+node:Creating and running dialogs
	def newAboutLeoDialog(self,commander):
		"""A do-nothing base class to create an About Leo dialog."""
		pass
	
	def newAskOkDialog(self,commander):
		"""A do-nothing base class to create an askOK dialog ."""
		pass
	
	def newAskOkCancelDialog(self,commander):
		"""A do-nothing base class to create an askOkCancel dialog."""
		pass
	
	def newAskOkCancelNumberDialog(self,commander):
		"""A do-nothing base class to create an askOkCancelNumber dialog ."""
		pass
	
	def newAskYesNoDialog(self,commander):
		"""A do-nothing base class to create an askYesNo dialog."""
		pass
	
	def newAskYesNoCancelDialg(self,commander):
		"""A do-nothing base class to create an askYesNoCancel dialog ."""
		pass
	#@nonl
	#@-node:Creating and running dialogs
	#@+node:Dialog utils
	def attachLeoIcon (self,window):
		"""Attach the Leo icon to a window."""
		pass
		
	def center_dialog(self,dialog):
		"""Center a dialog."""
		pass
		
	def create_labeled_frame (self,parent,caption=None,relief="groove",bd=2,padx=0,pady=0):
		"""Create a labeled frame."""
		pass
		
	def get_window_info (self,window):
		"""Return the window information."""
		pass
	#@-node:Dialog utils
	#@+node:Focus utils
	def get_focus(self,top):
		"""Return the widget that has focus, or the body widget if None."""
		pass
		
	def set_focus(self,commander,widget):
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		pass
		
	def force_focus(self,commander,widget):
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		pass
	#@nonl
	#@-node:Focus utils
	#@-others
#@nonl
#@-node:class leoGui
#@+node:class tkinterGui(leoGui)
class tkinterGui(leoGui):
	
	"""A class encapulating all calls to tkinter."""
	
	#@	@+others
	#@+node: tkinterGui.__init__
	def __init__ (self):
		
		# trace("tkinterGui")
		
		# Initialize the base class.
		leoGui.__init__(self,"tkinter")
		
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
		self.setEncoding()
		self.createGlobalWindows()
	
		return root
	#@nonl
	#@-node:createRootWindow & allies
	#@+node:setDefaultIcon
	def setDefaultIcon(self):
		
		"""Set the icon to be used in all Leo windows.
		
		This code does nothing for Tk versions before 8.3.4."""
		
		gui = self
	
		try:
			version = gui.root.getvar("tk_patchLevel")
			if CheckVersion(version,"8.3.4"):
				# tk 8.3.4 or greater: load a 16 by 16 icon.
				bitmap_name = os.path.join(app.loadDir,"..","Icons","LeoApp16.ico")
				self.bitmap = Tkinter.BitmapImage(bitmap_name)
		except:
			print "exception setting bitmap"
			traceback.print_exc()
	#@nonl
	#@-node:setDefaultIcon
	#@+node:setEncoding
	#@+at 
	#@nonl
	# According to Martin v. Löwis, getdefaultlocale() is broken, and cannot 
	# be fixed. The workaround is to copy the getpreferredencoding() function 
	# from locale.py in Python 2.3a2.  This function is now in leoGlobals.py.
	#@-at
	#@@c
	
	def setEncoding (self):
	
		for (encoding,src) in (
			(app.config.tkEncoding,"config"),
			#(locale.getdefaultlocale()[1],"locale"),
			(getpreferredencoding(),"locale"),
			(sys.getdefaultencoding(),"sys"),
			("utf-8","default")):
		
			if isValidEncoding (encoding): # 3/22/03
				app.tkEncoding = encoding
				# trace(app.tkEncoding,src)
				break
			elif encoding and len(encoding) > 0:
				trace("ignoring invalid " + src + " encoding: " + `encoding`)
				
		# trace(app.tkEncoding)
	#@nonl
	#@-node:setEncoding
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
	
		app.findFrame = leoFind.leoFind()
		app.findFrame.top.withdraw()
		app.globalWindows.append(app.findFrame)
	#@nonl
	#@-node:createGlobalWindows
	#@+node:destroy
	def destroy(self,widget):
		
		widget.destroy()
	#@nonl
	#@-node:destroy
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
			return self.defaultFont
	#@nonl
	#@-node:getFontFromParams
	#@+node:Creating and running dialogs
	def newAboutLeoDialog(self,commander):
		"""A do-nothing base class to create an About Leo dialog."""
		pass
	
	def newAskOkDialog(self,commander):
		"""A do-nothing base class to create an askOK dialog ."""
		pass
	
	def newAskOkCancelDialog(self,commander):
		"""A do-nothing base class to create an askOkCancel dialog."""
		pass
	
	def newAskOkCancelNumberDialog(self,commander):
		"""A do-nothing base class to create an askOkCancelNumber dialog ."""
		pass
	
	def newAskYesNoDialog(self,commander):
		"""A do-nothing base class to create an askYesNo dialog."""
		pass
	
	def newAskYesNoCancelDialg(self,commander):
		"""A do-nothing base class to create an askYesNoCancel dialog ."""
		pass
	#@nonl
	#@-node:Creating and running dialogs
	#@+node:Creating Frames
	def newColorFrame(self,commander):
		"""A do-nothing base class to create a colorFrame."""
		pass
	
	def newColorNameFrame(self,commander):
		"""A do-nothing base class to create a colorNameFrame."""
		pass
	
	def newCompareFrame(self,commander):
		"""A do-nothing base class to create a compareFrame."""
		pass
	
	def newFindFrame(self,commander):
		"""A do-nothing base class to create a findFrame."""
		pass
	
	def newFontFrame(self,commander):
		"""A do-nothing base class to create a fondFrame."""
		pass
	
	def newLeoFrame(self,commander):
		"""A do-nothing base class to create a view frame for the Leo main window."""
		trace()
		return leoFrame.LeoFrame(commander)
	
	def newPrefsFrame(self,commander):
		"""A do-nothing base class to create a prefsFrame."""
		pass
	#@nonl
	#@-node:Creating Frames
	#@+node:get_focus
	def get_focus(self,top):
		
		"""Returns the widget that has focus, or body if None."""
	
		return top.focus_displayof()
	#@nonl
	#@-node:get_focus
	#@+node:set_focus
	def set_focus(self,commands,widget):
		
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		
		focus = commands.frame.top.focus_displayof()
		if focus != widget:
			widget.focus_set()
	#@nonl
	#@-node:set_focus
	#@+node:force_focus
	def force_focus(self,commands,widget):
		
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		
		focus = commands.frame.top.focus_displayof()
		if focus != widget:
			widget.focus_force() # Apparently it is not a good idea to call focus_force.
	#@nonl
	#@-node:force_focus
	#@+node:attachLeoIcon & createLeoIcon
	def attachLeoIcon (self,w):
		
		"""Try to attach a Leo icon to the Leo Window.
		
		Use tk's wm_iconbitmap function if available (tk 8.3.4 or greater).
		Otherwise, try to use the Python Imaging Library and the tkIcon package."""
	
		if self.bitmap:
			# We don't need PIL or tkicon: this is tk 8.3.4 or greater.
			w.wm_iconbitmap(self.bitmap)
		else:
			#@		<< try to use the PIL and tkIcon packages to draw the icon >>
			#@+node:<< try to use the PIL and tkIcon packages to draw the icon >>
			#@+at 
			#@nonl
			# This code requires Fredrik Lundh's PIL and tkIcon packages:
			# 
			# Download PIL    from 
			# http://www.pythonware.com/downloads/index.htm#pil
			# Download tkIcon from http://www.effbot.org/downloads/#tkIcon
			# 
			# Many thanks to Jonathan M. Gilligan for suggesting this code.
			#@-at
			#@@c
			
			try:
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
			except:
				# traceback.print_exc()
				self.leoIcon = None
			#@nonl
			#@-node:<< try to use the PIL and tkIcon packages to draw the icon >>
			#@nl
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
	#@+node:runMainLoop
	def runMainLoop(self):
	
		"""Run tkinter's main loop."""
	
		self.root.mainloop()
	#@nonl
	#@-node:runMainLoop
	#@-others
#@nonl
#@-node:class tkinterGui(leoGui)
#@-others
#@nonl
#@-node:@file leoGui.py
#@-leo
