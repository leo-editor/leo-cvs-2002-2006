#@+leo
#@+node:0::@file leoPrefs.py
#@+body
#@@language python

from leoGlobals import *
import string,Tkinter

# Public constants used for defaults when leoConfig.txt can not be read.
default_page_width = 132
default_tab_width = 4
default_target_language = "python"
default_default_directory = None

ivars = [
	"tangle_batch_flag", "untangle_batch_flag",
	"use_header_flag", "output_doc_flag",
	"tangle_directory", "page_width", "tab_width",
	"target_language" ]

class baseLeoPrefs:
	"""The base class of Leo's preferences panel."""

	#@+others
	#@+node:1::prefs.__init__
	#@+body
	def __init__ (self,c):
	
		Tk = Tkinter
		
		#@<< set ivars >>
		#@+node:1::<< Set ivars >>
		#@+body
		# These ivars have the same names as the corresponding ivars in commands class.
		
		# Global options
		self.page_width = default_page_width
		self.tab_width = default_tab_width
		self.tangle_batch_flag = 0
		self.untangle_batch_flag = 0
		
		self.replace_tabs_var = Tk.IntVar() # 1/30/03
		self.tangle_batch_var = Tk.IntVar()
		self.untangle_batch_var = Tk.IntVar()
		
		# Default Tangle options
		self.tangle_directory = ""
		self.use_header_flag = 0
		self.output_doc_flag = 0
		
		self.use_header_var = Tk.IntVar()
		self.output_doc_var = Tk.IntVar()
		
		# Default Target Language
		self.target_language = default_target_language
		self.lang_var = Tk.StringVar()
		#@-body
		#@-node:1::<< Set ivars >>

		self.commands = c
		self.top = top = Tk.Toplevel()
		c.frame.prefsPanel = self
		head,tail = os.path.split(c.frame.title)
		self.top.title("Prefs for " + tail)
		
		# Create the outer frame
		outer = Tk.Frame(top,bd=2,relief="groove")
		outer.pack(fill="both",expand=1,padx=2,pady=2)
		
		#@<< Create the Global Options frame >>
		#@+node:2::<< Create the Global Options frame >>
		#@+body
		# Frame and title
		w,glob = create_labeled_frame (outer,caption="Global Options")
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
		#@-body
		#@-node:2::<< Create the Global Options frame >>

		
		#@<< Create the Tangle Options frame >>
		#@+node:3::<< Create the Tangle Options frame >>
		#@+body
		# Frame and title
		w,tangle = create_labeled_frame (outer,caption="Default Options")
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
		#@-body
		#@-node:3::<< Create the Tangle Options frame >>

		
		#@<< Create the Target Language frame >>
		#@+node:4::<< Create the Target Language frame >>
		#@+body
		# Frame and title
		w,target = create_labeled_frame (outer,caption="Default Target Language")
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
			("CWEB", "cweb"),
			("HTML", "html"),
			("Java", "java"),
			("LaTeX", "latex"),
			("Pascal", "pascal")]
		
		for text,value in left_data:
			button = Tk.Radiobutton(lt,anchor="w",text=text,
				variable=self.lang_var,value=value,command=self.set_lang)
			button.pack(fill="x") 
			
		# Right column of radio buttons.
		right_data = [
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
		
		#@-body
		#@-node:4::<< Create the Target Language frame >>

		
		#@<< Create the Ok, Cancel & Revert buttons >>
		#@+node:5::<< Create the Ok, Cancel & Revert buttons >>
		#@+body
		buttons = Tk.Frame(outer)
		buttons.pack(padx=2,pady=2,expand=1,fill="x")
		
		okButton = Tk.Button(buttons,text="OK",width=7,command=self.onOK)
		cancelButton = Tk.Button(buttons,text="Cancel",width=7,command=self.onCancel)
		revertButton = Tk.Button(buttons,text="Revert",width=7,command=self.onRevert)
		
		okButton.pack(side="left",pady=7,expand=1)
		cancelButton.pack(side="left",pady=7,expand=0)
		revertButton.pack(side="left",pady=7,expand=1)
		#@-body
		#@-node:5::<< Create the Ok, Cancel & Revert buttons >>

		center_dialog(top) # Do this _after_ building the dialog!
		top.resizable(0,0) # neither height or width is resizable.
		self.top.protocol("WM_DELETE_WINDOW", self.onCancel) # 1/31/03
		self.init(c)
		# es("Prefs.__init__")
	#@-body
	#@-node:1::prefs.__init__
	#@+node:2::prefs.init
	#@+body
	# Initializes prefs ivars and widgets from c's ivars.
	
	def init(self,c):
	
		self.commands = c
		#trace(`c.tab_width`)
	
		for var in ivars:
			val = getattr(c,var)
			setattr(self,var,val)
			# trace(val,var)
	
		
		#@<< remember values for revert >>
		#@+node:1::<< remember values for revert >>
		#@+body
		# Global options
		self.revert_tangle_batch_flag = c.tangle_batch_flag
		self.revert_untangle_batch_flag = c.untangle_batch_flag
		self.revert_page_width = c.page_width
		self.revert_tab_width = c.tab_width
		# Default Tangle Options
		self.revert_tangle_directory = c.tangle_directory
		self.revert_output_doc_flag = c.output_doc_flag
		self.revert_use_header_flag = c.use_header_flag
		# Default Target Language
		if c.target_language == None: # 7/29/02
			c.target_language = "python"
		self.revert_target_language = c.target_language
		#@-body
		#@-node:1::<< remember values for revert >>

		
		#@<< set widgets >>
		#@+node:2::<< set widgets >>
		#@+body
		# Global options
		self.replace_tabs_var.set(choose(c.tab_width<0,1,0)) # 1/30/03
		self.tangle_batch_var.set(c.tangle_batch_flag)
		self.untangle_batch_var.set(c.untangle_batch_flag)
		self.pageWidthText.delete("1.0","end")
		self.pageWidthText.insert("end",`c.page_width`)
		self.tabWidthText.delete("1.0","end")
		self.tabWidthText.insert("end",`abs(c.tab_width)`) # 1/30/03
		# Default Tangle Options
		self.tangleDirectoryText.delete("1.0","end")
		self.tangleDirectoryText.insert("end",c.tangle_directory)
		self.output_doc_var.set(c.output_doc_flag)
		self.use_header_var.set(c.use_header_flag)
		# Default Target Language
		if c.target_language == None:
			c.target_language = "python" # 7/29/02
		self.lang_var.set(c.target_language)
		#@-body
		#@-node:2::<< set widgets >>

		# print "init" ; print self.print_ivars()
	#@-body
	#@-node:2::prefs.init
	#@+node:3::Event handlers
	#@+node:1::prefs.set_ivars & idle_set_ivars & print_ivars
	#@+body
	# These event handlers get executed when the user types in the prefs panel.
	
	def set_ivars (self,c):
	
		
		#@<< update ivars >>
		#@+node:1::<< update ivars >>
		#@+body
		# Global options
		w = self.pageWidthText.get("1.0","end")
		w = string.strip(w)
		try:
			self.page_width = abs(int(w))
		except:
			self.page_width = default_page_width
			
		w = self.tabWidthText.get("1.0","end")
		w = string.strip(w)
		try:
			self.tab_width = abs(int(w))
			if self.replace_tabs_var.get(): # 1/30/03
				self.tab_width = - abs(self.tab_width)
			# print self.tab_width
		except:
			self.tab_width = default_tab_width
		
		self.tangle_batch_flag = self.tangle_batch_var.get()
		self.untangle_batch_flag = self.untangle_batch_var.get()
		
		# Default Tangle options
		dir = self.tangleDirectoryText.get("1.0","end")
		self.tangle_directory = string.strip(dir)
		
		self.use_header_flag = self.use_header_var.get()
		self.output_doc_flag = self.output_doc_var.get()
		
		# Default Target Language
		self.target_language = self.lang_var.get()
		
		#@-body
		#@-node:1::<< update ivars >>

		for var in ivars:
			val = getattr(self,var)
			setattr(c,var,val)
			
		c.frame.setTabWidth(c.tab_width)
		# self.print_ivars()
	
	def idle_set_ivars (self, event=None):
		
		c = top() ; v = c.currentVnode()
		self.top.after_idle(self.set_ivars,c)
		c.tree.recolor(v)
		# print self.print_ivars()
		
	def print_ivars (self):
		
		for var in ivars:
			trace(var, getattr(self,var))
	#@-body
	#@-node:1::prefs.set_ivars & idle_set_ivars & print_ivars
	#@+node:2::set_lang
	#@+body
	# This event handler gets executed when the user choose a new default language.
	
	def set_lang (self):
		
		c = top() ; v = c.currentVnode()
		language = self.lang_var.get()
		c.target_language = self.target_language = language
		c.tree.recolor(v)
		# print "set_lang",language
	#@-body
	#@-node:2::set_lang
	#@+node:3::prefs.onOK, onCancel, onRevert
	#@+body
	def onOK (self):
		app().config.setConfigIvars(self.commands)
		app().config.update()
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			self.commands.frame.prefsPanel = None
			self.top.destroy()
		
	def onCancel (self):
		c = self.commands
		
		#@<< restore options >>
		#@+node:1::<< restore options >>
		#@+body
		# Global options
		c.tangle_batch_flag = self.revert_tangle_batch_flag
		c.untangle_batch_flag = self.revert_untangle_batch_flag
		c.page_width = self.revert_page_width
		c.tab_width = self.revert_tab_width
		
		# Default Tangle Options
		c.tangle_directory = self.revert_tangle_directory
		c.output_doc_flag = self.revert_output_doc_flag
		c.use_header_flag = self.revert_use_header_flag
		
		# Default Target Language
		c.target_language = self.revert_target_language
		#@-body
		#@-node:1::<< restore options >>

		self.init(c)
		self.set_ivars(c)
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			self.commands.frame.prefsPanel = None
			self.top.destroy()
	
	def onRevert (self):
		c = self.commands
		
		#@<< restore options >>
		#@+node:1::<< restore options >>
		#@+body
		# Global options
		c.tangle_batch_flag = self.revert_tangle_batch_flag
		c.untangle_batch_flag = self.revert_untangle_batch_flag
		c.page_width = self.revert_page_width
		c.tab_width = self.revert_tab_width
		
		# Default Tangle Options
		c.tangle_directory = self.revert_tangle_directory
		c.output_doc_flag = self.revert_output_doc_flag
		c.use_header_flag = self.revert_use_header_flag
		
		# Default Target Language
		c.target_language = self.revert_target_language
		#@-body
		#@-node:1::<< restore options >>

		self.init(c)
		self.set_ivars(c)
	#@-body
	#@-node:3::prefs.onOK, onCancel, onRevert
	#@-node:3::Event handlers
	#@-others

	
class LeoPrefs (baseLeoPrefs):
	"""A class that creates Leo's preferenes panel."""
	pass
#@-body
#@-node:0::@file leoPrefs.py
#@-leo
