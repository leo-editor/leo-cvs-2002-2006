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
	"target_language"]

class LeoPrefs:

	#@+others

	#@+node:1::prefs.__init__

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
		
		lab2 = Tk.Label(f, padx="1m", text="Tab width:")
		self.tabWidthText = txt2 = Tk.Text(f, height=1, width=4)
		lab2.pack(side="left")
		txt2.pack(side="left")
		
		# Batch Checkbuttons...
		self.doneBox = doneBox = Tk.Checkbutton(glob,anchor="w",
			text="Run tangle_done.py after Tangle", variable=self.tangle_batch_var)
		self.unBox = unBox = Tk.Checkbutton(glob,anchor="w",
			text="Run untangle_done.py after Untangle", variable=self.untangle_batch_var)
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
		
		lab3.pack(            padx="1m", pady="1m", fill="x")
		txt3.pack(anchor="w", padx="1m", pady="1m", fill="x")
		
		# Checkbuttons
		self.headerBox = header = Tk.Checkbutton(tangle,anchor="w",
			text="Tangle outputs header line", variable=self.use_header_var)
		self.docBox = doc = Tk.Checkbutton(tangle,anchor="w",
			text="Tangle outputs document chunks", variable=self.output_doc_var)
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
		
		# Left column of radio buttons
		self.cButton = cButton = Tk.Radiobutton(lt,anchor="w",text="C/C++",
			variable=self.lang_var, value = c_language)
		self.cwebButton = cwebButton = Tk.Radiobutton(lt,anchor="w",text="CWEB",
			variable=self.lang_var, value = cweb_language)
		self.htmlButton = htmlButton = Tk.Radiobutton(lt,anchor="w",text="HTML",
			variable=self.lang_var, value = html_language)
		self.javaButton = javaButton = Tk.Radiobutton(lt,anchor="w",text="Java",
			variable=self.lang_var, value = java_language)
		self.pascalButton = pascalButton = Tk.Radiobutton(lt,anchor="w",text="Pascal",
			variable=self.lang_var, value = pascal_language)
		
		cButton.pack     (fill="x")
		cwebButton.pack  (fill="x")
		htmlButton.pack  (fill="x")
		javaButton.pack  (fill="x")
		pascalButton.pack(fill="x")
		
		# Right column of radio buttons
		self.perlButton = perlButton = Tk.Radiobutton(rt,anchor="w",text="Perl",
			variable=self.lang_var, value = perl_language)
		self.perlPodButton = perlPodButton = Tk.Radiobutton(rt,anchor="w",text="Perl + POD",
			variable=self.lang_var, value = perlpod_language)
		self.plainButton = plainButton = Tk.Radiobutton(rt,anchor="w",text="Plain Text",
			variable=self.lang_var, value = plain_text_language)
		self.pythonButton = pythonButton = Tk.Radiobutton(rt,anchor="w",text="Python",
			variable=self.lang_var, value = python_language)
		
		perlButton.pack   (fill="x")
		perlPodButton.pack(fill="x")
		plainButton.pack  (fill="x")
		pythonButton.pack (fill="x")

		#@-body

		#@-node:4::<< Create the Target Language frame >>

		self.top.protocol("WM_DELETE_WINDOW", self.OnClosePrefsFrame)
		# es("Prefs.__init__")
	#@-body

	#@-node:1::prefs.__init__

	#@+node:2::prefs.init

	#@+body
	def init(self,c):
	
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

	#@-body

	#@-node:2::prefs.init

	#@+node:3::prefs.set_ivars

	#@+body
	def set_ivars (self, c):
	
		
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

	#@-body

	#@-node:3::prefs.set_ivars

	#@+node:4::OnClosePrefsFrame

	#@+body
	def OnClosePrefsFrame(self):
	
		self.top.withdraw() # Just hide the window.
	#@-body

	#@-node:4::OnClosePrefsFrame

	#@-others

#@-body

#@-node:0::@file leoPrefs.py

#@-leo
