#@+leo-ver=4
#@+node:@file leoGui.py
"""A module containing all of Leo's default gui code.

Plugins may define their own gui classes by setting app().gui."""

from leoGlobals import *
import os,sys,tkFont,traceback

class tkinterGuiClass:
	
	"""A class encapulating all calls to tkinter."""
	
	#@	@+others
	#@+node:__getattr__ & ignoreUnknownAttr
	def __getattr__(self,name):
		
		"""tkinterGuiClass.__getattr to handle unknown calls without crashing."""
		
		print "tkinterGui.__getattr__: not found:",name
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
	#@+node:createRootWindow
	def createRootWindow(self):
	
		"""Create a hidden Tk root window and the app object"""
		
		# Create a hidden main window: this window never becomes visible!
		
		print "createRootWindow"
	
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
				
		print "setEncoding",a.tkEncoding
	#@nonl
	#@-node:setGuiEncoding
	#@+node:setDefaultIcon
	def setDefaultIcon(self):
		
		print "setDefaultIcon"
		
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
		
		print "getDefaultConfigFont",`config`
	
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
	#@+node:createFrame
	def createFrame (self,frame):
		
		"""Create a tkinter leo Window for the given leoFrame class."""
		
		trace(`frame`)
	#@nonl
	#@-node:createFrame
	#@+node:createMenus
	def createMenus (self,frame):
		
		trace(`frame`)
	#@nonl
	#@-node:createMenus
	#@-others
#@nonl
#@-node:@file leoGui.py
#@-leo
