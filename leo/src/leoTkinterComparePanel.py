#@+leo-ver=4
#@+node:@file leoTkinterComparePanel.py
#@@language python

"""Leo's base compare class."""

from leoGlobals import *
import leoCompare
import Tkinter,tkFileDialog

Tk = Tkinter

class leoTkinterComparePanel (leoCompare.leoCompare):
	
	"""A class that creates Leo's compare panel."""

	#@	@+others
	#@+node: tkinterComparePanel.__init__
	def __init__ (self,c):
		
		# Init the base class.
		leoCompare.leoCompare.__init__ (self,c)
		self.c = c
	
		#@	<< init tkinter compare ivars >>
		#@+node:<< init tkinter compare ivars >>
		# Ivars pointing to Tk elements.
		self.browseEntries = []
		self.extensionEntry = None
		self.countEntry = None
		self.printButtons = []
			
		# No corresponding ivar in the leoCompare class.
		self.useOutputFileVar = Tk.IntVar()
		
		# These all correspond to ivars in leoCompare....
		self.appendOutputVar             = Tk.IntVar()
		
		self.ignoreBlankLinesVar         = Tk.IntVar()
		self.ignoreFirstLine1Var         = Tk.IntVar()
		self.ignoreFirstLine2Var         = Tk.IntVar()
		self.ignoreInteriorWhitespaceVar = Tk.IntVar()
		self.ignoreLeadingWhitespaceVar  = Tk.IntVar()
		self.ignoreSentinelLinesVar      = Tk.IntVar()
		
		self.limitToExtensionVar         = Tk.IntVar()
		self.makeWhitespaceVisibleVar    = Tk.IntVar()
		
		self.printBothMatchesVar         = Tk.IntVar()
		self.printMatchesVar             = Tk.IntVar()
		self.printMismatchesVar          = Tk.IntVar()
		self.printTrailingMismatchesVar  = Tk.IntVar()
		self.stopAfterMismatchVar        = Tk.IntVar()
		#@nonl
		#@-node:<< init tkinter compare ivars >>
		#@nl
		
		# These ivars are set from Entry widgets.
		self.limitCount = 0
		self.limitToExtension = None
		
		# The default file name in the "output file name" browsers.
		self.defaultOutputFileName = "CompareResults.txt"
		
		self.createFrame()
	#@nonl
	#@-node: tkinterComparePanel.__init__
	#@+node:finishCreate
	# Initialize ivars from config parameters.
	
	def finishCreate (self):
	
		config = app.config
		
		# File names.
		for i,option in (
			(0,"compare_file_1"),
			(1,"compare_file_2"),
			(2,"output_file") ):
				
			name = config.getComparePref(option)
			if name and len(name) > 0:
				e = self.browseEntries[i]
				e.delete(0,"end")
				e.insert(0,name)
				
		name = config.getComparePref("output_file")
		b = choose(name and len(name) > 0,1,0)
		self.useOutputFileVar.set(b)
	
		# File options.
		b = config.getBoolComparePref("ignore_first_line_of_file_1")
		if b == None: b = 0
		self.ignoreFirstLine1Var.set(b)
		
		b = config.getBoolComparePref("ignore_first_line_of_file_2")
		if b == None: b = 0
		self.ignoreFirstLine2Var.set(b)
		
		b = config.getBoolComparePref("append_output_to_output_file")
		if b == None: b = 0
		self.appendOutputVar.set(b)
	
		ext = config.getComparePref("limit_directory_search_extension")
		b = ext and len(ext) > 0
		b = choose(b and b != 0,1,0)
		self.limitToExtensionVar.set(b)
		if b:
			e = self.extensionEntry
			e.delete(0,"end")
			e.insert(0,ext)
			
		# Print options.
		b = config.getBoolComparePref("print_both_lines_for_matches")
		if b == None: b = 0
		self.printBothMatchesVar.set(b)
		
		b = config.getBoolComparePref("print_matching_lines")
		if b == None: b = 0
		self.printMatchesVar.set(b)
		
		b = config.getBoolComparePref("print_mismatching_lines")
		if b == None: b = 0
		self.printMismatchesVar.set(b)
		
		b = config.getBoolComparePref("print_trailing_lines")
		if b == None: b = 0
		self.printTrailingMismatchesVar.set(b)
		
		n = config.getIntComparePref("limit_count")
		b = n and n > 0
		b = choose(b and b != 0,1,0)
		self.stopAfterMismatchVar.set(b)
		if b:
			e = self.countEntry
			e.delete(0,"end")
			e.insert(0,`n`)
	
		# Whitespace options.
		b = config.getBoolComparePref("ignore_blank_lines")
		if b == None: b = 1 # unusual default.
		self.ignoreBlankLinesVar.set(b)
		
		b = config.getBoolComparePref("ignore_interior_whitespace")
		if b == None: b = 0
		self.ignoreInteriorWhitespaceVar.set(b)
		
		b = config.getBoolComparePref("ignore_leading_whitespace")
		if b == None: b = 0
		self.ignoreLeadingWhitespaceVar.set(b)
		
		b = config.getBoolComparePref("ignore_sentinel_lines")
		if b == None: b = 0
		self.ignoreSentinelLinesVar.set(b)
		
		b = config.getBoolComparePref("make_whitespace_visible")
		if b == None: b = 0
		self.makeWhitespaceVisibleVar.set(b)
	#@nonl
	#@-node:finishCreate
	#@+node:createFrame
	def createFrame (self):
	
		gui = app.gui
		self.top = top = Tk.Toplevel(app.root)
		top.title("Leo Compare files and directories")
		top.protocol("WM_DELETE_WINDOW", self.onClose)
	
		#@	<< create the organizer frames >>
		#@+node:<< create the organizer frames >>
		outer = Tk.Frame(top, bd=2,relief="groove")
		outer.pack(pady=4)
		
		row1 = Tk.Frame(outer)
		row1.pack(pady=4)
		
		row2 = Tk.Frame(outer)
		row2.pack(pady=4)
		
		row3 = Tk.Frame(outer)
		row3.pack(pady=4)
		
		row4 = Tk.Frame(outer)
		row4.pack(pady=4,expand=1,fill="x") # for left justification.
		
		options = Tk.Frame(outer)
		options.pack(pady=4)
		
		ws = Tk.Frame(options)
		ws.pack(side="left",padx=4)
		
		pr = Tk.Frame(options)
		pr.pack(side="right",padx=4)
		
		lower = Tk.Frame(outer)
		lower.pack(pady=6)
		#@nonl
		#@-node:<< create the organizer frames >>
		#@nl
		#@	<< create the browser rows >>
		#@+node:<< create the browser rows >>
		for row,text,text2,command,var in (
			(row1,"Compare path 1:","Ignore first line",self.onBrowse1,self.ignoreFirstLine1Var),
			(row2,"Compare path 2:","Ignore first line",self.onBrowse2,self.ignoreFirstLine2Var),
			(row3,"Output file:",   "Use output file",  self.onBrowse3,self.useOutputFileVar) ):
		
			lab = Tk.Label(row,anchor="e",text=text,width=13)
			lab.pack(side="left",padx=4)
			
			e = Tk.Entry(row)
			e.pack(side="left",padx=2)
			self.browseEntries.append(e)
			
			b = Tk.Button(row,text="browse...",command=command)
			b.pack(side="left",padx=6)
		
			b = Tk.Checkbutton(row,text=text2,anchor="w",variable=var,width=15)
			b.pack(side="left")
		#@nonl
		#@-node:<< create the browser rows >>
		#@nl
		#@	<< create the extension row >>
		#@+node:<< create the extension row >>
		b = Tk.Checkbutton(row4,anchor="w",var=self.limitToExtensionVar,
			text="Limit directory compares to type:")
		b.pack(side="left",padx=4)
		
		self.extensionEntry = e = Tk.Entry(row4,width=6)
		e.pack(side="left",padx=2)
		
		b = Tk.Checkbutton(row4,anchor="w",var=self.appendOutputVar,
			text="Append output to output file")
		b.pack(side="left",padx=4)
		#@nonl
		#@-node:<< create the extension row >>
		#@nl
		#@	<< create the whitespace options frame >>
		#@+node:<< create the whitespace options frame >>
		w,f = gui.create_labeled_frame(ws,caption="Whitespace options",relief="groove")
			
		for text,var in (
			("Ignore Leo sentinel lines", self.ignoreSentinelLinesVar),
			("Ignore blank lines",        self.ignoreBlankLinesVar),
			("Ignore leading whitespace", self.ignoreLeadingWhitespaceVar),
			("Ignore interior whitespace",self.ignoreInteriorWhitespaceVar),
			("Make whitespace visible",   self.makeWhitespaceVisibleVar) ):
			
			b = Tk.Checkbutton(f,text=text,variable=var)
			b.pack(side="top",anchor="w")
			
		spacer = Tk.Frame(f)
		spacer.pack(padx="1i")
		#@nonl
		#@-node:<< create the whitespace options frame >>
		#@nl
		#@	<< create the print options frame >>
		#@+node:<< create the print options frame >>
		w,f = gui.create_labeled_frame(pr,caption="Print options",relief="groove")
		
		row = Tk.Frame(f)
		row.pack(expand=1,fill="x")
		
		b = Tk.Checkbutton(row,text="Stop after",variable=self.stopAfterMismatchVar)
		b.pack(side="left",anchor="w")
		
		self.countEntry = e = Tk.Entry(row,width=4)
		e.pack(side="left",padx=2)
		e.insert(01,"1")
		
		lab = Tk.Label(row,text="mismatches")
		lab.pack(side="left",padx=2)
		
		for padx,text,var in (    
			(0,  "Print matched lines",           self.printMatchesVar),
			(20, "Show both matching lines",      self.printBothMatchesVar),
			(0,  "Print mismatched lines",        self.printMismatchesVar),
			(0,  "Print unmatched trailing lines",self.printTrailingMismatchesVar) ):
			
			b = Tk.Checkbutton(f,text=text,variable=var)
			b.pack(side="top",anchor="w",padx=padx)
			self.printButtons.append(b)
			
		# To enable or disable the "Print both matching lines" button.
		b = self.printButtons[0]
		b.configure(command=self.onPrintMatchedLines)
		
		spacer = Tk.Frame(f)
		spacer.pack(padx="1i")
		#@nonl
		#@-node:<< create the print options frame >>
		#@nl
		#@	<< create the compare buttons >>
		#@+node:<< create the compare buttons >>
		for text,command in (
			("Compare files",      self.onCompareFiles),
			("Compare directories",self.onCompareDirectories) ):
			
			b = Tk.Button(lower,text=text,command=command,width=18)
			b.pack(side="left",padx=6)
		#@nonl
		#@-node:<< create the compare buttons >>
		#@nl
	
		gui.center_dialog(top) # Do this _after_ building the dialog!
		top.resizable(0,0)
		self.finishCreate()
	#@nonl
	#@-node:createFrame
	#@+node:setIvarsFromWidgets
	def setIvarsFromWidgets (self):
	
		# File paths: checks for valid file name.
		e = self.browseEntries[0]
		self.fileName1 = e.get()
		
		e = self.browseEntries[1]
		self.fileName2 = e.get()
	
		# Ignore first line settings.
		self.ignoreFirstLine1 = self.ignoreFirstLine1Var.get()
		self.ignoreFirstLine2 = self.ignoreFirstLine2Var.get()
		
		# Output file: checks for valid file name.
		if self.useOutputFileVar.get():
			e = self.browseEntries[2]
			name = e.get()
			if name != None and len(name) == 0:
				name = None
			self.outputFileName = name
		else:
			self.outputFileName = None
	
		# Extension settings.
		if self.limitToExtensionVar.get():
			self.limitToExtension = self.extensionEntry.get()
			if len(self.limitToExtension) == 0:
				self.limitToExtension = None
		else:
			self.limitToExtension = None
			
		self.appendOutput = self.appendOutputVar.get()
		
		# Whitespace options.
		self.ignoreBlankLines         = self.ignoreBlankLinesVar.get()
		self.ignoreInteriorWhitespace = self.ignoreInteriorWhitespaceVar.get()
		self.ignoreLeadingWhitespace  = self.ignoreLeadingWhitespaceVar.get()
		self.ignoreSentinelLines      = self.ignoreSentinelLinesVar.get()
		self.makeWhitespaceVisible    = self.makeWhitespaceVisibleVar.get()
		
		# Print options.
		self.printMatches            = self.printMatchesVar.get()
		self.printMismatches         = self.printMismatchesVar.get()
		self.printTrailingMismatches = self.printTrailingMismatchesVar.get()
		
		if self.printMatches:
			self.printBothMatches = self.printBothMatchesVar.get()
		else:
			self.printBothMatches = false
		
		if self.stopAfterMismatchVar.get():
			try:
				count = self.countEntry.get()
				self.limitCount = int(count)
			except: self.limitCount = 0
		else:
			self.limitCount = 0
	#@nonl
	#@-node:setIvarsFromWidgets
	#@+node:bringToFront
	def bringToFront(self):
		
		self.top.deiconify()
		self.top.lift()
	#@-node:bringToFront
	#@+node:browser
	def browser (self,n):
		
		types = [
			("C/C++ files","*.c"),
			("C/C++ files","*.cpp"),
			("C/C++ files","*.h"),
			("C/C++ files","*.hpp"),
			("Java files","*.java"),
			("Pascal files","*.pas"),
			("Python files","*.py"),
			("Text files","*.txt"),
			("All files","*") ]
	
		fileName = tkFileDialog.askopenfilename(
			title="Choose compare file" + n,
			filetypes=types,
			defaultextension=".txt")
			
		if fileName and len(fileName) > 0:
			# The dialog also warns about this, so this may never happen.
			if not os_path_exists(fileName):
				self.show("not found: " + fileName)
				fileName = None
		else: fileName = None
			
		return fileName
	#@nonl
	#@-node:browser
	#@+node:onBrowse...
	def onBrowse1 (self):
		
		fileName = self.browser("1")
		if fileName:
			e = self.browseEntries[0]
			e.delete(0,"end")
			e.insert(0,fileName)
		self.top.deiconify()
		
	def onBrowse2 (self):
		
		fileName = self.browser("2")
		if fileName:
			e = self.browseEntries[1]
			e.delete(0,"end")
			e.insert(0,fileName)
		self.top.deiconify()
		
	def onBrowse3 (self): # Get the name of the output file.
	
		fileName = tkFileDialog.asksaveasfilename(
			initialfile = self.defaultOutputFileName,
			title="Set output file",
			filetypes=[("Text files", "*.txt")],
			defaultextension=".txt")
			
		if fileName and len(fileName) > 0:
			self.defaultOutputFileName = fileName
			self.useOutputFileVar.set(1) # The user will expect this.
			e = self.browseEntries[2]
			e.delete(0,"end")
			e.insert(0,fileName)
	#@nonl
	#@-node:onBrowse...
	#@+node:onClose
	def onClose (self):
		
		self.top.withdraw()
	#@nonl
	#@-node:onClose
	#@+node:onCompare...
	def onCompareDirectories (self):
	
		self.setIvarsFromWidgets()
		self.compare_directories(self.fileName1,self.fileName2)
	
	def onCompareFiles (self):
	
		self.setIvarsFromWidgets()
		self.compare_files(self.fileName1,self.fileName2)
	#@nonl
	#@-node:onCompare...
	#@+node:onPrintMatchedLines
	def onPrintMatchedLines (self):
		
		v = self.printMatchesVar.get()
		b = self.printButtons[1]
		state = choose(v,"normal","disabled")
		b.configure(state=state)
	#@nonl
	#@-node:onPrintMatchedLines
	#@-others
#@nonl
#@-node:@file leoTkinterComparePanel.py
#@-leo
