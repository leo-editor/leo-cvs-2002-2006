# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoGui.py
#@@first # -*- coding: utf-8 -*-

"""A module containing all of Leo's default gui code.

Plugins may define their own gui classes by setting app().gui."""

from leoGlobals import *
import os,sys,tkFont,Tkinter,traceback

Tk = Tkinter

class tkinterGuiClass:
	
	"""A class encapulating all calls to tkinter."""
	
	#@	@+others
	#@+node:__getattr__ & ignoreUnknownAttr
	def __getattr__(self,name):
		
		"""tkinterGuiClass.__getattr to handle unknown calls without crashing."""
		
		# print "tkinterGui.__getattr__: not found:",name
		return self.ignoreUnknownAttr
		
	def  ignoreUnknownAttr(self,*args,**keys):
		
		"""A universal do-nothing routine that can be returned by __getattr__."""
		pass
	#@nonl
	#@-node:__getattr__ & ignoreUnknownAttr
	#@+node:guiName
	def guiName(self):
		return "tkinter"
	#@nonl
	#@-node:guiName
	#@+node:destroy
	def destroy(self,widget):
		
		widget.destroy()
	#@nonl
	#@-node:destroy
	#@+node:attachLeoIcon & allies
	#@+at 
	#@nonl
	# This code requires Fredrik Lundh's PIL and tkIcon packages:
	# 
	# Download PIL    from http://www.pythonware.com/downloads/index.htm#pil
	# Download tkIcon from http://www.effbot.org/downloads/#tkIcon
	# 
	# We wait until the window has been drawn once before attaching the icon 
	# in OnVisiblity.
	# 
	# Many thanks to Jonathan M. Gilligan for suggesting this code.
	#@-at
	#@@c
	
	leoIcon = None
	
	def attachLeoIcon (self,w):
		try:
			import Image,_tkicon
			import tkIcon
			global leoIcon
			
			f = onVisibility
			callback = lambda event,w=w,f=f:f(w,event)
			w.bind("<Visibility>",callback)
			if not leoIcon:
				# Using a .gif rather than an .ico allows us to specify transparency.
				icon_file_name = os.path.join(app().loadDir,'..','Icons','LeoWin.gif')
				icon_file_name = os.path.normpath(icon_file_name)
				icon_image = Image.open(icon_file_name)
				if 1: # Doesn't resize.
					leoIcon = createLeoIcon(icon_image)
				else: # Assumes 64x64
					leoIcon = tkIcon.Icon(icon_image)
				
		except:
			# es_exception()
			leoIcon = None
	#@nonl
	#@-node:attachLeoIcon & allies
	#@+node:createLeoIcon
	# This code is adapted from tkIcon.__init__
	# Unlike the tkIcon code, this code does _not_ resize the icon file.
	
	def createLeoIcon (self,icon):
		
		try:
			import Image,_tkicon
			import tkIcon
			
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
	#@+node:onVisibility
	# Handle the "visibility" event and attempt to attach the Leo icon.
	# This code must be executed whenever the window is redrawn.
	
	def onVisibility (self,w,event):
	
		global leoIcon
	
		try:
			import Image,_tkicon
			import tkIcon
			if leoIcon and w and event and event.widget == w:
				if 1: # Allows us not to resize the icon.
					leoIcon.attach(w.winfo_id())
				else:
					leoIcon.attach(w)
		except: pass
	#@nonl
	#@-node:onVisibility
	#@+node:center_dialog
	# Center the dialog on the screen.
	# WARNING: Call this routine _after_ creating a dialog.
	# (This routine inhibits the grid and pack geometry managers.)
	
	def center_dialog(self,dialog,top):
	
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
	#@+node:createRootWindow
	def createRootWindow(self):
	
		"""Create a hidden Tk root window and the app object"""
		
		# Create a hidden main window: this window never becomes visible!
		
		# print "createRootWindow"
	
		root = Tkinter.Tk()
		root.title("Leo Main Window")
		root.withdraw()
		return root
	#@nonl
	#@-node:createRootWindow
	#@+node:setGuiEncoding
	#@+at 
	#@nonl
	# According to Martin v. Löwis, getdefaultlocale() is broken, and cannot 
	# be fixed. The workaround is to copy the getpreferredencoding() function 
	# from locale.py in Python 2.3a2.  This function is now in leoGlobals.py.
	#@-at
	#@@c
	
	def setEncoding (self):
		
		a = app()
	
		for (encoding,src) in (
			(a.config.tkEncoding,"config"),
			#(locale.getdefaultlocale()[1],"locale"),
			(getpreferredencoding(),"locale"),
			(sys.getdefaultencoding(),"sys"),
			("utf-8","default")):
		
			if isValidEncoding (encoding): # 3/22/03
				a.tkEncoding = encoding
				# print a.tkEncoding,src
				break
			elif encoding and len(encoding) > 0:
				print "ignoring invalid " + src + " encoding: " + `encoding`
				
		# print "setEncoding",a.tkEncoding
	#@nonl
	#@-node:setGuiEncoding
	#@+node:setDefaultIcon
	def setDefaultIcon(self):
		
		# print "setDefaultIcon"
		
		a = app()
		try:
			bitmap_name = os.path.join(a.loadDir,"..","Icons","LeoApp.ico")
			bitmap = Tkinter.BitmapImage(bitmap_name)
		except:
			print "exception creating bitmap"
			traceback.print_exc()
		
		try:
			version = a.root.getvar("tk_patchLevel")
			#@		<< set v834 if version is 8.3.4 or greater >>
			#@+node:<< set v834 if version is 8.3.4 or greater >>
			# 04-SEP-2002 DHEIN: simplify version check
			# 04-SEP-2002 Stephen P. Schaefer: make sure v834 is set
			v834 = CheckVersion(version, "8.3.4")
			#@-node:<< set v834 if version is 8.3.4 or greater >>
			#@nl
		except:
			print "exception getting version"
			traceback.print_exc()
			v834 = None
			
		if v834:
			try:
				if sys.platform=="win32": # Windows
					top.wm_iconbitmap(bitmap,default=1)
				else:
					top.wm_iconbitmap(bitmap)
			except:
				if 0: # Let's ignore this for now until I understand the issues better.
					es("exception setting bitmap")
					es_exception()
	#@nonl
	#@-node:setDefaultIcon
	#@+node:getDefaultConfigFont
	def getDefaultConfigFont(self,config):
		
		"""Get the default font from a new text widget."""
		
		# print "getDefaultConfigFont",`config`
	
		t = Tkinter.Text()
		fn = t.cget("font")
		font = tkFont.Font(font=fn)
		config.defaultFont = font
		config.defaultFontFamily = font.cget("family")
	#@nonl
	#@-node:getDefaultConfigFont
	#@+node:getFontFromParams
	def getFontFromParams(self,family,size,slant,weight):
		
		# print "getFontFromParams"
		
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
	#@-others
#@nonl
#@-node:@file leoGui.py
#@-leo
