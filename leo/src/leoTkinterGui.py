# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoTkinterGui.py
#@@first

"""Leo's Tkinter Gui module."""

from leoGlobals import *
import leoGui
import leoTkinterColorPanels,leoTkinterComparePanel,leoTkinterDialog
import leoTkinterFind,leoTkinterFontPanel,leoTkinterFrame
import leoTkinterPrefs
import tkFont,Tkinter,tkFileDialog

Tk = Tkinter

class tkinterGui(leoGui.leoGui):
	
	"""A class encapulating all calls to tkinter."""
	
	#@	@+others
	#@+node: tkinterGui.__init__
	def __init__ (self):
	
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
				path = os_path_join(app.loadDir,"..","Icons")
				if os_path_exists(path):
					file = os_path_join(path,"LeoApp16.ico")
					if os_path_exists(path):
						self.bitmap = Tkinter.BitmapImage(file)
					else:
						es("LeoApp16.ico not in Icons directory", color="red")
				else:
					es("Icons directory not found: "+path, color="red")
		except:
			print "exception setting bitmap"
			import traceback ; traceback.print_exc()
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
	def destroySelf (self):
	
		if 0: # Works in Python 2.1 and 2.2.  Leaves Python window open.
			self.root.destroy()
			
		else: # Works in Python 2.3.  Closes Python window.
			self.root.quit()
	#@nonl
	#@-node:destroySelf
	#@+node:finishCreate (not used: must be present)
	def finishCreate (self):
		
		pass
		
	#@-node:finishCreate (not used: must be present)
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
	#@+node:app.gui.Tkinter dialogs
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
			title,message,yesMessage,noMessage,defaultButton)
	 	return d.run(modal=true)
	#@nonl
	#@-node:app.gui.Tkinter dialogs
	#@+node:app.gui.Tkinter file dialogs
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
	#@-node:app.gui.Tkinter file dialogs
	#@+node:app.gui.Tkinter panels
	def createColorPanel(self,c):
		"""Create a Tkinter color picker panel."""
		return leoTkinterColorPanels.leoTkinterColorPanel(c)
		
	def createComparePanel(self,c):
		"""Create a Tkinter color picker panel."""
		return leoTkinterComparePanel.leoTkinterComparePanel(c)
	
	def createFindPanel(self): # The find panel is global, so no c param.
		"""Create a hidden Tkinter find panel."""
		panel = leoTkinterFind.leoTkinterFind()
		panel.top.withdraw()
		return panel
	
	def createFontPanel(self,c):
		"""Create a Tkinter font panel."""
		return leoTkinterFontPanel.leoTkinterFontPanel(c)
		
	def createLeoFrame(self,title):
		"""Create a new Leo frame."""
		return leoTkinterFrame.leoTkinterFrame(title)
	
	def createPrefsPanel(self,c):
		"""Create a Tkinter find panel."""
		return leoTkinterPrefs.leoTkinterPrefs(c)
	#@nonl
	#@-node:app.gui.Tkinter panels
	#@+node:replaceClipboardWith
	def replaceClipboardWith (self,s):
	
		self.root.clipboard_clear()
		self.root.clipboard_append(s)
		
	#@-node:replaceClipboardWith
	#@+node:getTextFromClibboard
	def getTextFromClibboard (self):
		
		try:
			return self.root.selection_get(selection="CLIPBOARD")
		except:
			return None
	#@nonl
	#@-node:getTextFromClibboard
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
	def center_dialog(self,top):
	
		"""Center the dialog on the screen.
	
		WARNING: Call this routine _after_ creating a dialog.
		(This routine inhibits the grid and pack geometry managers.)"""
	
		sw = top.winfo_screenwidth()
		sh = top.winfo_screenheight()
		w,h,x,y = self.get_window_info(top)
		
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
	#@+node:get_focus
	def get_focus(self,frame):
		
		"""Returns the widget that has focus, or body if None."""
	
		return frame.top.focus_displayof()
		
	#@-node:get_focus
	#@+node:set_focus
	def set_focus(self,c,widget):
		
		"""Set the focus of the widget in the given commander if it needs to be changed."""
		
		focus = c.frame.top.focus_displayof()
		if focus != widget:
			widget.focus_set()
	#@nonl
	#@-node:set_focus
	#@+node:tkGui.getFontFromParams
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
	#@-node:tkGui.getFontFromParams
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
					icon_file_name = os_path_join(app.loadDir,'..','Icons','LeoWin.gif')
					icon_file_name = os_path_normpath(icon_file_name)
					icon_image = Image.open(icon_file_name)
					if 1: # Doesn't resize.
						self.leoIcon = self.createLeoIcon(icon_image)
					else: # Assumes 64x64
						self.leoIcon = tkIcon.Icon(icon_image)
				#@nonl
				#@-node:<< try to use the PIL and tkIcon packages to draw the icon >>
				#@nl
			except:
				# import traceback ; traceback.print_exc()
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
	#@+node:setIdleTimeHook
	def setIdleTimeHook (self,idleTimeHookHandler,*args,**keys):
		
		# trace(idleTimeHookHandler)
		if self.root:
			self.root.after_idle(idleTimeHookHandler,*args,**keys)
			
	#@-node:setIdleTimeHook
	#@+node:setIdleTimeHookAfterDelay
	def setIdleTimeHookAfterDelay (self,delay,idleTimeHookHandler,*args,**keys):
		
		if self.root:
			app.root.after(app.idleTimeDelay,idleTimeHookHandler)
	#@nonl
	#@-node:setIdleTimeHookAfterDelay
	#@+node:firstIndex
	def firstIndex (self):
	
		return "1.0"
	#@nonl
	#@-node:firstIndex
	#@+node:lastIndex
	def lastIndex (self):
	
		return "end"
	#@nonl
	#@-node:lastIndex
	#@+node:moveIndexBackward
	def moveIndexBackward(self,index,n):
	
		return "%s-%dc" % (index,n)
	#@-node:moveIndexBackward
	#@+node:moveIndexForward
	def moveIndexForward(self,index,n):
	
		return "%s+%dc" % (index,n)
	#@nonl
	#@-node:moveIndexForward
	#@+node:compareIndices
	def compareIndices (self,t,n1,rel,n2):
		return t.compare(n1,rel,n2)
	#@nonl
	#@-node:compareIndices
	#@+node:getindex
	def getindex(self,text,index):
		
		"""Convert string index of the form line.col into a tuple of two ints."""
		
		return tuple(map(int,string.split(text.index(index), ".")))
	#@nonl
	#@-node:getindex
	#@+node:getInsertPoint
	def getInsertPoint(self,t):
	
		return t.index("insert")
	#@nonl
	#@-node:getInsertPoint
	#@+node:setInsertPoint
	def setInsertPoint (self,t,pos):
	
		return t.mark_set("insert",pos)
	#@nonl
	#@-node:setInsertPoint
	#@+node:getSelectionRange
	def getSelectionRange (self,t):
	
		return t.tag_ranges("sel")
	#@nonl
	#@-node:getSelectionRange
	#@+node:getTextSelection
	def getTextSelection (self,t):
		
		"""Return a tuple representing the selected range of t, a Tk.Text widget.
		
		Return a tuple giving the insertion point if no range of text is selected."""
	
		# To get the current selection
		sel = t.tag_ranges("sel")  ## Do not remove:  remove entire routine instead!!
		if len(sel) == 2:
			return sel
		else:
			# 7/1/03: Return the insertion point if there is no selected text.
			insert = t.index("insert")
			return insert,insert
	#@nonl
	#@-node:getTextSelection
	#@+node:setSelectionRange
	def setSelectionRange(self,t,n1,n2):
	
		return app.gui.setTextSelection(t,n1,n2)
	#@nonl
	#@-node:setSelectionRange
	#@+node:setSelectionRangeWithLength
	def setSelectionRangeWithLength(self,t,start,length):
		
		return app.gui.setTextSelection(t,start,start + "+" + `length` + "c")
	#@-node:setSelectionRangeWithLength
	#@+node:setTextSelection
	def setTextSelection (self,t,start,end):
		
		"""tk gui: set the selection range in Tk.Text widget t."""
	
		if not start or not end:
			return
	
		if t.compare(start, ">", end):
			start,end = end,start
			
		t.tag_remove("sel","1.0",start)
		t.tag_add("sel",start,end)
		t.tag_remove("sel",end,"end")
		t.mark_set("insert",end)
	#@nonl
	#@-node:setTextSelection
	#@+node:getAllText
	def getAllText (self,t):
		
		"""Return all the text of Tk.Text t converted to unicode."""
		
		s = t.get("1.0","end")
		if s is None:
			return u""
		else:
			return toUnicode(s,app.tkEncoding)
	#@nonl
	#@-node:getAllText
	#@+node:getCharAfterIndex
	def getCharAfterIndex (self,t,index):
		
		if t.compare(index + "+1c",">=","end"):
			return None
		else:
			ch = t.get(index + "+1c")
			return toUnicode(ch,app.tkEncoding)
	#@nonl
	#@-node:getCharAfterIndex
	#@+node:getCharAtIndex
	def getCharAtIndex (self,t,index):
		ch = t.get(index)
		return toUnicode(ch,app.tkEncoding)
	#@nonl
	#@-node:getCharAtIndex
	#@+node:getCharBeforeIndex
	def getCharBeforeIndex (self,t,index):
		
		index = t.index(index)
		if index == "1.0":
			return None
		else:
			ch = t.get(index + "-1c")
			return toUnicode(ch,app.tkEncoding)
	#@nonl
	#@-node:getCharBeforeIndex
	#@+node:getLineContainingIndex
	def getLineContainingIndex (self,t,index):
	
		line = t.get(index + " linestart", index + " lineend")
		return toUnicode(line,app.tkEncoding)
	#@nonl
	#@-node:getLineContainingIndex
	#@+node:replaceSelectionRangeWithText
	def replaceSelectionRangeWithText (self,t,start,end,text):
	
		t.delete(start,end)
		t.insert(start,text)
	#@nonl
	#@-node:replaceSelectionRangeWithText
	#@+node:makeIndexVisible
	def makeIndexVisible(self,t,index):
	
		return t.see(index)
	#@nonl
	#@-node:makeIndexVisible
	#@-others
#@nonl
#@-node:@file leoTkinterGui.py
#@-leo
