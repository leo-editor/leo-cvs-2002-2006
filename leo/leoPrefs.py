#@+leo

#@+node:0::@file leoPrefs.py
#@+body
from leoGlobals import *
from leoUtils import *
import string, Tkinter

# Private constants
default_page_width = 132
default_tab_width = 4

ivars = [
	"tangle_batch_flag", "untangle_batch_flag",
	"use_header_flag", "output_doc_flag",
	"tangle_directory", "page_width", "tab_width",
	"target_language" ]

class LeoPrefs:

	#@+others
	#@+node:1:C=1:prefs.__init__
	#@+body
	def __init__ (self):
	
		Tk = Tkinter
		
		#@<< set ivars >>
		#@+node:1::<< Set ivars >>
		#@+body
		# These ivars have the same names as the corresponding ivars in commands class.
		
		# Global options
		self.page_width = 132
		self.tab_width = 4
		self.tangle_batch_flag = 0
		self.untangle_batch_flag = 0
		
		self.tangle_batch_var = Tk.IntVar()
		self.untangle_batch_var = Tk.IntVar()
		
		# Default Tangle options
		self.tangle_directory = ""
		self.use_header_flag = 0
		self.output_doc_flag = 0
		
		self.use_header_var = Tk.IntVar()
		self.output_doc_var = Tk.IntVar()
		
		# Default Target Language
		self.target_language = python_language
		self.lang_var = Tk.IntVar()
		#@-body
		#@-node:1::<< Set ivars >>

		self.top = top = Tk.Toplevel()
		self.top.title("Leo Preferences")
		top.resizable(0,0) # neither height or width is resizable.
		
		#@<< Create the Global Options frame >>
		#@+node:2::<< Create the Global Options frame >>
		#@+body
		glob = Tk.Frame(top, bd="2", relief="groove") 
		glob.pack(anchor="n", pady=2, ipadx="1m", expand=1, fill="x")
		
		globTitle = Tk.Label(glob, text="Global Options...")
		globTitle.pack(pady="1m")
		
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
		# Can't easily use a list becasue we use different variables.
		self.doneBox = doneBox = Tk.Checkbutton(glob,anchor="w",
			text="Run tangle_done.py after Tangle",
			variable=self.tangle_batch_var,command=self.idle_set_ivars)
		self.unBox = unBox = Tk.Checkbutton(glob,anchor="w",
			text="Run untangle_done.py after Untangle",
			variable=self.untangle_batch_var,command=self.idle_set_ivars)
		doneBox.pack(fill="x")
		unBox.pack(fill="x")
		#@-body
		#@-node:2::<< Create the Global Options frame >>

		
		#@<< Create the Tangle Options frame >>
		#@+node:3::<< Create the Tangle Options frame >>
		#@+body
		# Frame and title
		tangle = Tk.Frame(top, bd="2", relief="groove")
		tangle.pack(anchor="n", ipadx="1m", expand=1, fill="x")
		
		tangleTitle = Tk.Label(tangle, text="Default Options...")
		tangleTitle.pack(pady="1m")
		
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
		target = Tk.Frame(top, bd="2", relief="groove")
		target.pack(anchor="n", pady=2, expand=1, fill="x") #   
		
		targetTitle = Tk.Label(target, text="Default Target Language...")
		targetTitle.pack(pady="1m")
		
		# Frames for two columns of radio buttons
		lt = Tk.Frame(target)
		rt = Tk.Frame(target)
		lt.pack(side="left")
		rt.pack(side="right")
		
		# Left column of radio buttons.
		left_data = [
			("C/C++",c_language), ("CWEB", cweb_language),
			("HTML", html_language), ("Java", java_language),
			("Pascal", pascal_language) ]
		
		for text,value in left_data:
			button = Tk.Radiobutton(lt,anchor="w",text=text,
				variable=self.lang_var,value=value,command=self.set_lang)
			button.pack(fill="x") 
			
		# Right column of radio buttons.
		right_data = [ ("Perl", perl_language), ("Perl+POD", perlpod_language),
			("Plain Text", plain_text_language), ("Python", python_language) ]
			
		for text,value in right_data:
			button = Tk.Radiobutton(rt,anchor="w",text=text,
				variable=self.lang_var,value=value,command=self.set_lang)
			button.pack(fill="x")
		#@-body
		#@-node:4::<< Create the Target Language frame >>

		self.top.protocol("WM_DELETE_WINDOW", self.OnClosePrefsFrame)
		# es("Prefs.__init__")
	#@-body
	#@-node:1:C=1:prefs.__init__
	#@+node:2:C=2:prefs.init
	#@+body
	def init(self,c):
	
		# trace(`self.target_language`)
		for var in ivars:
			exec("self.%s = c.%s" % (var,var))
			
		
		#@<< set widgets >>
		#@+node:1::<< set widgets >>
		#@+body
		# Global options
		self.tangle_batch_var.set(c.tangle_batch_flag)
		self.untangle_batch_var.set(c.untangle_batch_flag)
		self.pageWidthText.delete("1.0","end")
		self.pageWidthText.insert("end",`c.page_width`)
		self.tabWidthText.delete("1.0","end")
		self.tabWidthText.insert("end",`c.tab_width`)
		# Default Tangle Options
		self.tangleDirectoryText.delete("1.0","end")
		self.tangleDirectoryText.insert("end",c.tangle_directory)
		self.output_doc_var.set(c.output_doc_flag)
		self.use_header_var.set(c.use_header_flag)
		# Default Target Language
		self.lang_var.set(c.target_language)
		#@-body
		#@-node:1::<< set widgets >>

		# print "init" ; print self.print_ivars()
	#@-body
	#@-node:2:C=2:prefs.init
	#@+node:3:C=3:prefs.set_ivars & idle_set_ivars & print_ivars
	#@+body
	def set_ivars (self,c=None):
	
		if c == None: c = top()
		
		#@<< update ivars >>
		#@+node:1::<< update ivars >>
		#@+body
		# Global options
		w = self.pageWidthText.get("1.0","end")
		w = string.strip(w)
		try: self.page_width = int(w)
		except: self.page_width = default_page_width
			
		w = self.tabWidthText.get("1.0","end")
		w = string.strip(w)
		try: self.tab_width = int(w)
		except: self.tab_width = default_tab_width
		
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
			exec("c.%s = self.%s" % (var,var))
		# print "set_ivars" ; print self.print_ivars()
	
	def idle_set_ivars (self, event=None):
		
		c = top() ; v = c.currentVnode()
		self.top.after_idle(self.set_ivars,c)
		c.tree.recolor(v)
		# print "idle_set_ivars" ; print self.print_ivars()
		
	def print_ivars (self):
		
		for var in ivars:
			exec("print self.%s, '%s'" % (var,var))
	#@-body
	#@-node:3:C=3:prefs.set_ivars & idle_set_ivars & print_ivars
	#@+node:4:C=4:set_lang
	#@+body
	def set_lang (self):
		
		c = top() ; v = c.currentVnode()
		language = self.lang_var.get()
		c.target_language = self.target_language = language
		c.tree.recolor(v)
		# print "set_lang" ; print self.print_ivars()
	#@-body
	#@-node:4:C=4:set_lang
	#@+node:5::OnClosePrefsFrame
	#@+body
	def OnClosePrefsFrame(self):
	
		self.top.withdraw() # Just hide the window.
	#@-body
	#@-node:5::OnClosePrefsFrame
	#@-others

#@-body
#@-node:0::@file leoPrefs.py
#@-leo
