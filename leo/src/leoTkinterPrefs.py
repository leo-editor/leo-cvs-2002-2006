#@+leo-ver=4
#@+node:@file leoTkinterPrefs.py
#@@language python

from leoGlobals import *
import leoPrefs
import string,Tkinter
Tk = Tkinter

class leoTkinterPrefs (leoPrefs.leoPrefs):

	"""A class that creates Leo's preferenes panel."""

	#@	@+others
	#@+node:tkinterPrefs.__init__
	def __init__ (self,c):
		
		"""Ctor for the leoTkinterPrefs class."""
		
		# Init the base class
		leoPrefs.leoPrefs.__init__(self,c)
		
		self.createFrame()
		self.setWidgets()
	#@nonl
	#@-node:tkinterPrefs.__init__
	#@+node:createFrame
	def createFrame (self):
		
		"""Create the tkinter Prefs panel."""
	
		c = self.c ; gui = app.gui
		self.top = top = Tk.Toplevel()
		c.frame.prefsPanel = self
		head,tail = os_path_split(c.frame.title)
		self.top.title("Prefs for " + tail)
		
		# Create the outer frame
		outer = Tk.Frame(top,bd=2,relief="groove")
		outer.pack(fill="both",expand=1,padx=2,pady=2)
		#@	<< Create the Tk.IntVars >>
		#@+node:<< Create the Tk.IntVars >>
		self.replace_tabs_var = Tk.IntVar()
		self.tangle_batch_var = Tk.IntVar()
		self.untangle_batch_var = Tk.IntVar()
		
		self.use_header_var = Tk.IntVar()
		self.output_doc_var = Tk.IntVar()
		
		self.lang_var = Tk.StringVar()
		#@nonl
		#@-node:<< Create the Tk.IntVars >>
		#@nl
		#@	<< Create the Global Options frame >>
		#@+node:<< Create the Global Options frame >>
		# Frame and title
		w,glob = gui.create_labeled_frame (outer,caption="Global Options")
		w.pack(padx=2,pady=2,expand=1,fill="x")
		
		# Page width & page width
		f = Tk.Frame(glob)
		f.pack(anchor="w", pady="1m", expand=1, fill="x")
		
		lab = Tk.Label(f, anchor="w", padx="1m", text="Page width:")
		self.pageWidthText = txt = Tk.Text(f, height=1, width=4)
		lab.pack(side="left")
		txt.pack(side="left")
		txt.bind("<Key>", self.idle_set_ivars)
		
		lab2 = Tk.Label(f, padx="1m", text="Tab width:")
		self.tabWidthText = txt2 = Tk.Text(f, height=1, width=4)
		lab2.pack(side="left")
		txt2.pack(side="left")
		txt2.bind("<Key>", self.idle_set_ivars)
		
		# Batch Checkbuttons...
		self.replaceTabsBox = replaceBox = Tk.Checkbutton(glob,anchor="w",
			text="Replace tabs with spaces",
			variable=self.replace_tabs_var,command=self.idle_set_ivars)
		self.doneBox = doneBox = Tk.Checkbutton(glob,anchor="w",
			text="Run tangle_done.py after Tangle",
			variable=self.tangle_batch_var,command=self.idle_set_ivars)
		self.unBox = unBox = Tk.Checkbutton(glob,anchor="w",
			text="Run untangle_done.py after Untangle",
			variable=self.untangle_batch_var,command=self.idle_set_ivars)
		
		for box in (replaceBox, doneBox, unBox):
			box.pack(fill="x")
		#@nonl
		#@-node:<< Create the Global Options frame >>
		#@nl
		#@	<< Create the Tangle Options frame >>
		#@+node:<< Create the Tangle Options frame >>
		# Frame and title
		w,tangle = gui.create_labeled_frame (outer,caption="Default Options")
		w.pack(padx=2,pady=2,expand=1,fill="x")
		
		# Label and text
		lab3 = Tk.Label(tangle, anchor="w", text="Default tangle directory")
		self.tangleDirectoryText = txt3 = Tk.Text(tangle, height=1, width=30)
		txt3.bind("<Key>", self.idle_set_ivars) # Capture the change immediately
		lab3.pack(            padx="1m", pady="1m", fill="x")
		txt3.pack(anchor="w", padx="1m", pady="1m", fill="x")
		
		# Checkbuttons
		self.headerBox = header = Tk.Checkbutton(tangle,anchor="w",
			text="Tangle outputs header line",
			variable=self.use_header_var,command=self.idle_set_ivars)
		self.docBox = doc = Tk.Checkbutton(tangle,anchor="w",
			text="Tangle outputs document chunks",
			variable=self.output_doc_var,command=self.idle_set_ivars)
		header.pack(fill="x")
		doc.pack(fill="x")
		#@nonl
		#@-node:<< Create the Tangle Options frame >>
		#@nl
		#@	<< Create the Target Language frame >>
		#@+node:<< Create the Target Language frame >> frame
		# Frame and title
		w,target = gui.create_labeled_frame (outer,caption="Default Target Language")
		w.pack(padx=2,pady=2,expand=1,fill="x")
		
		# Frames for two columns of radio buttons
		lt = Tk.Frame(target)
		rt = Tk.Frame(target)
		lt.pack(side="left")
		rt.pack(side="right")
		
		# Left column of radio buttons.
		left_data = [
			("ActionScript", "actionscript"),
			("C/C++","c"),
			("C#",   "csharp"),
			("CWEB", "cweb"),
			("elisp","elisp"),
			("HTML", "html"),
			("Java", "java"),
			("LaTeX", "latex")]
		
		for text,value in left_data:
			button = Tk.Radiobutton(lt,anchor="w",text=text,
				variable=self.lang_var,value=value,command=self.set_lang)
			button.pack(fill="x")
		
		# Right column of radio buttons.
		right_data = [
			("Pascal", "pascal"),
			("Perl", "perl"),
			("Perl+POD", "perlpod"),
			("PHP", "php"),
			("Plain Text", "plain"),
			("Python", "python"),
			("Rebol", "rebol"),
			("tcl/tk", "tcltk")]
		
		for text,value in right_data:
			button = Tk.Radiobutton(rt,anchor="w",text=text,
				variable=self.lang_var,value=value,command=self.set_lang)
			button.pack(fill="x")
		#@nonl
		#@-node:<< Create the Target Language frame >> frame
		#@nl
		#@	<< Create the Ok, Cancel & Revert buttons >>
		#@+node:<< Create the Ok, Cancel & Revert buttons >>
		buttons = Tk.Frame(outer)
		buttons.pack(padx=2,pady=2,expand=1,fill="x")
		
		okButton = Tk.Button(buttons,text="OK",width=7,command=self.onOK)
		cancelButton = Tk.Button(buttons,text="Cancel",width=7,command=self.onCancel)
		revertButton = Tk.Button(buttons,text="Revert",width=7,command=self.onRevert)
		
		okButton.pack(side="left",pady=7,expand=1)
		cancelButton.pack(side="left",pady=7,expand=0)
		revertButton.pack(side="left",pady=7,expand=1)
		#@nonl
		#@-node:<< Create the Ok, Cancel & Revert buttons >>
		#@nl
		gui.center_dialog(top) # Do this _after_ building the dialog!
		top.resizable(0,0) # neither height or width is resizable.
		self.top.protocol("WM_DELETE_WINDOW", self.onCancel)
	#@nonl
	#@-node:createFrame
	#@+node:setWidgets
	def setWidgets (self):
		
		"""Set the values of checkbox & other widgets from the commander's ivars."""
		
		c = self.c
	
		# Global options
		self.replace_tabs_var.set(choose(c.tab_width<0,1,0))
		self.tangle_batch_var.set(c.tangle_batch_flag)
		self.untangle_batch_var.set(c.untangle_batch_flag)
		self.pageWidthText.delete("1.0","end")
		self.pageWidthText.insert("end",`c.page_width`)
		self.tabWidthText.delete("1.0","end")
		self.tabWidthText.insert("end",`abs(c.tab_width)`)
	
		# Default Tangle Options
		self.tangleDirectoryText.delete("1.0","end")
		self.tangleDirectoryText.insert("end",c.tangle_directory)
		self.output_doc_var.set(c.output_doc_flag)
		self.use_header_var.set(c.use_header_flag)
	
		# Default Target Language
		if c.target_language == None:
			c.target_language = "python"
		self.lang_var.set(c.target_language)
	#@nonl
	#@-node:setWidgets
	#@+node:bringToFront
	def bringToFront (self):
		
		"""Bring the tkinter Prefs Panel to the front."""
	
		self.top.deiconify()
		self.top.lift()
	#@nonl
	#@-node:bringToFront
	#@+node:hide
	def hide (self):
		
		"""Hide the tkinter Prefs panel."""
		
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			self.c.frame.prefsPanel = None
			self.top.destroy()
	#@nonl
	#@-node:hide
	#@+node:onOK, onCancel, onRevert
	def onOK (self):
		"""Handle a click in the OK button in the tkinter Prefs panel."""
		app.config.setConfigIvars(self.c)
		app.config.update()
		self.hide()
	
	def onCancel (self):
		"""Handle a click in the Cancel button in the tkinter Prefs panel."""
		c = self.c
		self.restoreOptions()
		self.init(c)
		self.set_ivars(c)
		self.hide()
	
	def onRevert (self):
		"""Handle a click in the Revert button in the tkinter Prefs panel."""
		c = self.c
		self.restoreOptions()
		self.init(c)
		self.set_ivars(c)
	#@nonl
	#@-node:onOK, onCancel, onRevert
	#@+node:set_ivars & idle_set_ivars
	# These event handlers get executed when the user types in the prefs panel.
	
	def set_ivars (self,c):
		
		"""Idle-time code to any change in the tkinter Prefs panel."""
	
		#@	<< update ivars >>
		#@+node:<< update ivars >>
		# Global options
		w = self.pageWidthText.get("1.0","end")
		w = string.strip(w)
		try:
			self.page_width = abs(int(w))
		except:
			self.page_width = self.default_page_width
			
		w = self.tabWidthText.get("1.0","end")
		w = string.strip(w)
		try:
			self.tab_width = abs(int(w))
			if self.replace_tabs_var.get(): # 1/30/03
				self.tab_width = - abs(self.tab_width)
			# print self.tab_width
		except:
			self.tab_width = self.default_tab_width
		
		self.tangle_batch_flag = self.tangle_batch_var.get()
		self.untangle_batch_flag = self.untangle_batch_var.get()
		
		# Default Tangle options
		dir = self.tangleDirectoryText.get("1.0","end")
		self.tangle_directory = string.strip(dir)
		
		self.use_header_flag = self.use_header_var.get()
		self.output_doc_flag = self.output_doc_var.get()
		
		# Default Target Language
		self.target_language = self.lang_var.get()
		#@-node:<< update ivars >>
		#@nl
		for var in self.ivars:
			val = getattr(self,var)
			setattr(c,var,val)
			
		c.frame.setTabWidth(c.tab_width)
		# self.print_ivars()
	
	def idle_set_ivars (self, event=None):
		
		"""Handle any change in the tkinter Prefs panel."""
		
		c = top() ; v = c.currentVnode()
		self.top.after_idle(self.set_ivars,c)
		c.frame.body.recolor(v)
		# print self.print_ivars()
	#@nonl
	#@-node:set_ivars & idle_set_ivars
	#@+node:set_lang
	def set_lang (self):
		
		"""Handle a change to the Default Target Language radio box."""
		
		c = self.c
		v = c.currentVnode()
		language = self.lang_var.get()
		c.target_language = self.target_language = language
		c.frame.body.recolor(v)
		# trace(language)
	#@nonl
	#@-node:set_lang
	#@-others
#@nonl
#@-node:@file leoTkinterPrefs.py
#@-leo
