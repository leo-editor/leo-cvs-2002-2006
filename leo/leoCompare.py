#@+leo

#@+node:0::@file leoCompare.py
#@+body
#@@language python

# The code for Leo's Compare Panel and the compare class.

import difflib, filecmp, os, string, traceback
import Tkinter, tkFileDialog

# We try to interfere with scripts as little as possible.
true = 1
false = 0 # Better than none.


#@+others
#@-others



#@<< define functions >>
#@+node:1::<< define functions >>
#@+body
#@+others
#@+node:1::choose
#@+body
def choose(cond, a, b): # warning: evaluates all arguments

	if cond: return a
	else: return b

#@-body
#@-node:1::choose
#@+node:2::go
#@+body
def go (self,name=None):

	cmp = leoCompare(
		commands = None,

		ignoreBlankLines = true,
		ignoreFirstLine1 = false,
		ignoreFirstLine2 = false,
		ignoreInteriorWhitespace = false,
		ignoreLeadingWhitespace = true,
		ignoreSentinelLines = false,
		
		limitCount = 9, # Zero means don't stop.
		limitToExtension = ".py",  # For directory compares.
		makeWhitespaceVisible = true,
		
		printBothMatches = false,
		printMatches = false,
		printMismatches = true,
		printTrailingMismatches = false,

		outputFileName = None)

	if 1: # Compare all files in Tangle test directories

		path1 = "c:\\prog\\test\\tangleTest\\"
		path2 = "c:\\prog\\test\\tangleTestCB\\"
		cmp.compare_directories(path1,path2)

	else: # Compare two files.

		name1 = "c:\\prog\\test\\compare1.txt"
		name2 = "c:\\prog\\test\\compare2.txt"
		cmp.compare_files(name1,name2)
#@-body
#@-node:2::go
#@-others
#@-body
#@-node:1::<< define functions >>


class leoCompare:
	
	#@<< class leoCompare methods >>
	#@+node:2::<< class leoCompare methods >>
	#@+body
	#@+others
	#@+node:1::compare.__init__
	#@+body
	# All these ivars are known to the leoComparePanel class.
	
	def __init__ (self,
	
		# Keyword arguments are much convenient and more clear for scripts.
		commands = None,
	
		ignoreBlankLines = true,
		ignoreFirstLine1 = false,
		ignoreFirstLine2 = false,
		ignoreInteriorWhitespace = false,
		ignoreLeadingWhitespace = true,
		ignoreSentinelLines = false,
	
		limitCount = 0, # Zero means don't stop.
		limitToExtension = ".py",  # For directory compares.
		makeWhitespaceVisible = true,
	
		printBothMatches = false,
		printMatches = false,
		printMismatches = true,
		printTrailingMismatches = false,
	
		outputFileName = None ):
			
		# It is more convenient for the leoComparePanel to set these directly.
		self.commands = commands
	
		self.ignoreBlankLines = ignoreBlankLines
		self.ignoreFirstLine1 = ignoreFirstLine1
		self.ignoreFirstLine2 = ignoreFirstLine2
		self.ignoreInteriorWhitespace = ignoreInteriorWhitespace
		self.ignoreLeadingWhitespace = ignoreLeadingWhitespace
		self.ignoreSentinelLines = ignoreSentinelLines
	
		self.limitCount = limitCount
		self.limitToExtension = limitToExtension
	
		self.printBothMatches = printBothMatches
		self.printMatches = printMatches
		self.printMismatches = printMismatches
		self.printTrailingMismatches = printTrailingMismatches
		
		# For communication between methods...
		self.outputFileName = outputFileName
		self.fileName1 = None 
		self.fileName2 = None
		# Open files...
		self.outputFile = None
	#@-body
	#@-node:1::compare.__init__
	#@+node:2::compare_directories (entry) (convert file names to directory names)
	#@+body
	# We ignore the filename portion of path1 and path2 if it exists.
	
	def compare_directories (self,path1,path2):
		
		# Ignore everything except the directory name.
		dir1 = os.path.dirname(path1)
		dir2 = os.path.dirname(path2)
		dir1 = os.path.normpath(dir1)
		dir2 = os.path.normpath(dir2)
		
		if dir1 == dir2:
			self.show("Directory names are identical.\nPlease pick distinct directories.")
			return
			
		try:
			list1 = os.listdir(dir1)
		except:
			self.show("invalid directory:" + dir1)
			return
		try:
			list2 = os.listdir(dir2)
		except:
			self.show("invalid directory:" + dir2)
			return
			
		if self.outputFileName:
			self.openOutputFile()
	
		# Create files and files2, the lists of files to be compared.
		files1 = []
		files2 = []
		for f in list1:
			junk, ext = os.path.splitext(f)
			if self.limitToExtension:
				if ext == self.limitToExtension:
					files1.append(f)
			else:
				files1.append(f)
		for f in list2:
			junk, ext = os.path.splitext(f)
			if self.limitToExtension:
				if ext == self.limitToExtension:
					files2.append(f)
			else:
				files2.append(f)
	
		# Compare the files and set the yes, no and fail lists.
		yes = [] ; no = [] ; fail = []
		for f1 in files1:
			head,f2 = os.path.split(f1)
			if f2 in files2:
				try:
					name1 = os.path.join(dir1,f1)
					name2 = os.path.join(dir2,f2)
					val = filecmp.cmp(name1,name2,0)
					if val: yes.append(f1)
					else:    no.append(f1)
				except:
					self.show("exception in filecmp.cmp")
					traceback.print_exc()
					fail.append(f1)
			else:
				fail.append(f1)
		
		# Print the results.
		self.show("\n")
		for kind, files in (
			("----- matches --------",yes),
			("----- mismatches -----",no),
			("----- not found ------",fail)):
			self.show(kind)
			for f in files:
				self.show(f)
		self.show("\n")
		
		if self.outputFile:
			self.outputFile.close()
			self.outputFile = None
	#@-body
	#@-node:2::compare_directories (entry) (convert file names to directory names)
	#@+node:3::compare_files (entry)
	#@+body
	def compare_files (self, name1, name2):
		
		#from leoUtils import trace
		#trace()
		
		if name1 == name2:
			self.show("File names are identical.\nPlease pick distinct files.")
			return
	
		f1 = f2 = None
		try:
			f1=self.doOpen(name1)
			f2=self.doOpen(name2)
			if f1 and f2:
				self.compare_open_files(f1,f2,name1,name2)
		except:
			import traceback
			self.show("exception comparing files")
			traceback.print_exc()
			
		try:
			if f1: f1.close()
			if f2: f2.close()
		except:
			import traceback
			self.show("exception closing files")
			traceback.print_exc()
	#@-body
	#@-node:3::compare_files (entry)
	#@+node:4::compare_lines
	#@+body
	def compare_lines (self,s1,s2):
		
		if self.ignoreLeadingWhitespace:
			s1 = string.lstrip(s1)
			s2 = string.lstrip(s2)
	
		if self.ignoreInteriorWhitespace:
			from leoUtils import skip_ws
			k1 = skip_ws(s1,0)
			k2 = skip_ws(s2,0)
			ws1 = s1[:k1]
			ws2 = s2[:k2]
			tail1 = s1[k1:]
			tail2 = s2[k2:]
			tail1 = string.replace(tail1," ","")
			tail1 = string.replace(tail1,"\t","")
			tail2 = string.replace(tail2," ","")
			tail2 = string.replace(tail2,"\t","")
			s1 = ws1 + tail1
			s2 = ws2 + tail2
	
		return s1 == s2
	#@-body
	#@-node:4::compare_lines
	#@+node:5::compare_open_files
	#@+body
	def compare_open_files (self, f1, f2, name1, name2):
	
		lines1 = 0 ; lines2 = 0 ; mismatches = 0
		printTrailing = true
		if self.outputFileName:
			self.openOutputFile()
		if self.ignoreFirstLine1:
			s1 = f1.readline() ; lines1 += 1
		if self.ignoreFirstLine2:
			s2 = f2.readline() ; lines2 += 1
		while 1:
			s1 = f1.readline() ; lines1 += 1
			s2 = f2.readline() ; lines2 += 1
			if self.ignoreLeadingWhitespace:
				s1 = string.lstrip(s1)
				s2 = string.lstrip(s2)
			if self.ignoreBlankLines:
				
				#@<< ignore blank lines >>
				#@+node:1::<< ignore blank lines >>
				#@+body
				while 1:
					s = string.rstrip(s1)
					if len(s) == 0:
						s1 = f1.readline()
						lines1 += 1
						if len(s1) == 0: break # end of file
					else: break
				
				while 1:
					s = string.rstrip(s2)
					if len(s) == 0:
						s2 = f2.readline()
						lines2 += 1
						if len(s1) == 0: break # end of file
					else: break
				#@-body
				#@-node:1::<< ignore blank lines >>

			n1 = len(s1) ; n2 = len(s2)
			if n1==0 and n2 != 0: self.show("eof on" + name1)
			if n2==0 and n1 != 0: self.show("eof on" + name2)
			if n1==0 or n2==0: break
			match = self.compare_lines(s1,s2)
			if not match: mismatches += 1
			if match and self.printMatches:
				if self.printBothMatches:
					self.dump(string.rjust("1." + `lines1`,6) + ' :',s1)
					self.dump(string.rjust("2." + `lines2`,6) + ' :',s2)
				else:
					self.dump(string.rjust(`lines1`,6) + ' :',s1)
			if not match and self.printMisMatches:
				self.dump(string.rjust("1." + `lines1`,6) + '*:',s1)
				self.dump(string.rjust("2." + `lines2`,6) + '*:',s2)
				if self.limitCount > 0 and mismatches > self.limitCount:
					self.show("limit count exceeded")
					printTrailing = false
					break
		if self.printTrailingMismatches and printTrailing:
			if n1 > 0: self.dumpToEndOfFile("1.",f1,lines1)
			if n2 > 0: self.dumpToEndOfFile("2.",f2,lines2)
		self.show("lines1:" + `lines1`)
		self.show("lines2:" + `lines2`)
		self.show("mismatches:" + `mismatches`)
		if self.outputFile:
			self.outputFile.close()
			self.outputFile = None
	#@-body
	#@-node:5::compare_open_files
	#@+node:6::filecmp
	#@+body
	def filecmp (self,f1,f2):
	
		val = filecmp.cmp(f1,f2)
		if 1:
			if val: self.show("equal")
			else:   self.show("*** not equal")
		else:
			self.show("filecmp.cmp returns:")
			if val: self.show(`val` + " (equal)")
			else:   self.show(`val` + " (not equal)")
	
		return val
	#@-body
	#@-node:6::filecmp
	#@+node:7::utils...
	#@+node:1::doOpen
	#@+body
	def doOpen (self,name):
	
		try:
			f = open(name,'r')
			return f
		except:
			self.show("can not open:" + `name`)
			return None
	#@-body
	#@-node:1::doOpen
	#@+node:2::dump
	#@+body
	def dump (self,tag,s):
	
		out = tag
	
		for ch in s[:-1]: # don't print the newline
		
			if self.makeWhitespaceVisible:
				if ch == '\t':
					out += "[" ; out += "t" ; out += "]"
				elif ch == ' ':
					out += "[" ; out += " " ; out += "]"
				else: out += ch
			else: 
				if ch == '\t' or ch == ' ':
					out += ' '
				else:
					out += ch
	
		self.show(out)

	#@-body
	#@-node:2::dump
	#@+node:3::dumpToEndOfFile
	#@+body
	def dumpToEndOfFile (self,tag,f,line):
	
		trailingLines = 0
		while 1:
			s = f.readline()
			if len(s) == 0: break
			trailingLines += 1
			if self.dumpTrailingMismatches:
				tag = string.rjust(tag + `line`,6) + "+:"
				self.dump(tag,s)
	
		self.show("file " + tag, " has " + trailingLines + " trailing lines")
		return trailingLines
	#@-body
	#@-node:3::dumpToEndOfFile
	#@+node:4::openOutput
	#@+body
	def openOutputFile (self):
		
		if self.outputFileName:
			dir = os.path.dirname(self.outputFileName)
			if not os.path.exists(dir):
				self.show("output directory not found: " + dir)
			else:
				try:
					self.show("writing to " + self.outputFileName)
					self.outputFile = open(self.outputFileName,"w")
				except:
					self.outputFile = None
					self.show("exception opening output file")
					traceback.print_exc()
	#@-body
	#@-node:4::openOutput
	#@+node:5::show
	#@+body
	def show (self,s):
		
		if self.outputFile:
			self.outputFile.write(s + '\n')
		elif self.commands:
			from leoGlobals import es
			es(s)
		else:
			print s
			print
	#@-body
	#@-node:5::show
	#@+node:6::showIvars
	#@+body
	def showIvars (self):
		
		self.show("fileName1:"        + `self.fileName1`)
		self.show("fileName2:"        + `self.fileName2`)
		self.show("outputFileName:"   + `self.outputFileName`)
		self.show("limitToExtension:" + `self.limitToExtension`)
		self.show("")
	
		self.show("ignoreBlankLines:"         + `self.ignoreBlankLines`)
		self.show("ignoreFirstLine1:"         + `self.ignoreFirstLine1`)
		self.show("ignoreFirstLine2:"         + `self.ignoreFirstLine2`)
		self.show("ignoreInteriorWhitespace:" + `self.ignoreInteriorWhitespace`)
		self.show("ignoreLeadingWhitespace:"  + `self.ignoreLeadingWhitespace`)
		self.show("ignoreSentinelLines:"      + `self.ignoreSentinelLines`)
		self.show("")
		
		self.show("limitCount:"              + `self.limitCount`)
		self.show("printMatches:"            + `self.printMatches`)
		self.show("printMismatches:"         + `self.printMismatches`)
		self.show("printTrailingMismatches:" + `self.printTrailingMismatches`)
	#@-body
	#@-node:6::showIvars
	#@-node:7::utils...
	#@-others
	
	#@-body
	#@-node:2::<< class leoCompare methods >>

	
class leoComparePanel:
	
	#@<< class leoComparePanel methods >>
	#@+node:3::<< class leoComparePanel methods >>
	#@+body
	#@+others
	#@+node:1::browser
	#@+body
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
			if not os.path.exists(fileName):
				self.show("not found: " + fileName)
				fileName = None
		else: fileName = None
			
		return fileName
	#@-body
	#@-node:1::browser
	#@+node:2:C=1:comparePanel.__init__
	#@+body
	def __init__ (self,c,cmp):
	
		Tk = Tkinter
		self.commands = c
		self.cmp = cmp
		
		# Ivars pointing to Tk elements.
		self.browseEntries = []
		self.extensionEntry = None
		self.countEntry = None
		self.printButtons = []
		
		# No corresponding cmp ivar.
		self.useOutputFileVar = Tk.IntVar()
		
		# These all correspond to ivars in leoCompare.
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
		
		# These ivars are set from Entry widgets.
		self.limitCount = 1
		self.limitToExtension = ".py"
		if 0: # we just use the cmp ivars.
			self.pathName1 = None
			self.pathName2 = None
			self.outputFileName = None
		
		# The default file name in the "output file name" browsers.
		self.defaultOutputFileName = "CompareResults.txt"
	#@-body
	#@-node:2:C=1:comparePanel.__init__
	#@+node:3:C=2:finishCreate
	#@+body
	# Initialize ivars to values I like.
	# To do: set all these from config parameters.
	
	def finishCreate (self):
		
		# File names.
		for i,name in (
			(0,"C:/prog/test/tangleTest/args.c"),
			(1,"C:/prog/test/tangleTestCB/args.c"),
			(2,"C:/prog/test/CompareResults.txt") ):
	
			e = self.browseEntries[i]
			e.delete(0,"end")
			e.insert(0,name)
	
		self.useOutputFileVar.set(1)
		self.makeWhitespaceVisibleVar.set(0)
		
		# Print options.
		self.printMatchesVar.set(1)
		self.printMismatchesVar.set(1)
		self.printTrailingMismatchesVar.set(1)
		
		self.stopAfterMismatchVar.set(1)
		self.countEntry.delete(0,"end")
		self.countEntry.insert(0,"9")
		
		# Whitespace options.
		self.ignoreBlankLinesVar.set(1)
	#@-body
	#@-node:3:C=2:finishCreate
	#@+node:4:C=3:run
	#@+body
	def run (self):
		
		# We import these here so as not to interfere with scripts
		from leoUtils   import center_dialog, create_labeled_frame, shortFileName
		from leoGlobals import app
		import leoApp, leoCommands
	
		c = self.commands ; cmp = self.cmp ; Tk = Tkinter
		self.top = top = Tk.Toplevel(app().root)
		top.title("Compare files and directories (" + shortFileName(c.frame.title) + ")")
		top.protocol("WM_DELETE_WINDOW", self.onClose)
		
		#@<< create the organizer frames >>
		#@+node:1::<< create the organizer frames >>
		#@+body
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
		#@-body
		#@-node:1::<< create the organizer frames >>

		
		#@<< create the browser rows >>
		#@+node:2::<< create the browser rows >>
		#@+body
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
		#@-body
		#@-node:2::<< create the browser rows >>

		
		#@<< create the extension row >>
		#@+node:3::<< create the extension row >>
		#@+body
		b = Tk.Checkbutton(row4,anchor="w",var=self.limitToExtensionVar,
			text="Limit directory compares extension:")
		b.pack(side="left",padx=4)
		
		self.extensionEntry = e = Tk.Entry(row4,width=6)
		e.pack(side="left",padx=2)
		e.insert(0,".py")
		#@-body
		#@-node:3::<< create the extension row >>

		
		#@<< create the whitespace options frame >>
		#@+node:4::<< create the whitespace options frame >>
		#@+body
		w,f = create_labeled_frame(ws,caption="Whitespace options",relief="groove")
			
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
		#@-body
		#@-node:4::<< create the whitespace options frame >>

		
		#@<< create the print options frame >>
		#@+node:5::<< create the print options frame >>
		#@+body
		w,f = create_labeled_frame(pr,caption="Print options",relief="groove")
		
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
		#@-body
		#@-node:5::<< create the print options frame >>

		
		#@<< create the compare buttons >>
		#@+node:6::<< create the compare buttons >>
		#@+body
		for text,command in (
			("Compare files",      self.onCompareFiles),
			("Compare directories",self.onCompareDirectories) ):
			
			b = Tk.Button(lower,text=text,command=command,width=18)
			b.pack(side="left",padx=6)
		#@-body
		#@-node:6::<< create the compare buttons >>

		center_dialog(top) # Do this _after_ building the dialog!
		top.resizable(0,0)
		self.finishCreate()
	#@-body
	#@-node:4:C=3:run
	#@+node:5:C=4:setIvarsFromWidgets
	#@+body
	def setIvarsFromWidgets (self):
	
		cmp = self.cmp ; result = true
		
		# File paths.
		e = self.browseEntries[0]
		cmp.fileName1 = e.get()
		
		e = self.browseEntries[1]
		cmp.fileName2 = e.get()
		
		# Make sure paths actually exist.
		for name in (cmp.fileName1, cmp.fileName2):
			if name and len(name) > 0:
				if not os.path.exists(name):
					self.show("path not found: " + name)
					result = false
			else:
				self.show("missing compare path")
				result = false
	
		# Ignore first line settings.
		cmp.ignoreFirstLine1 = self.ignoreFirstLine1Var.get()
		cmp.ignoreFirstLine2 = self.ignoreFirstLine2Var.get()
		
		# Output file.
		if self.useOutputFileVar.get():
			e = self.browseEntries[2]
			cmp.outputFileName = e.get()
		else:
			cmp.outputFileName = None
	
		# Extension settings.
		if self.limitToExtensionVar.get():
			cmp.limitToExtension = self.extensionEntry.get()
			if len(cmp.limitToExtension) == 0:
				cmp.limitToExtension = None
		else:
			cmp.limitToExtension = None
			
		cmp.makeWhitespaceVisible = self.makeWhitespaceVisibleVar.get()
		
		# Whitespace options.
		cmp.ignoreBlankLines         = self.ignoreBlankLinesVar.get()
		cmp.ignoreInteriorWhitespace = self.ignoreInteriorWhitespaceVar.get()
		cmp.ignoreLeadingWhitespace  = self.ignoreLeadingWhitespaceVar.get()
		cmp.ignoreSentinelLines      = self.ignoreSentinelLinesVar.get()
		
		# Print options.
		cmp.printMatches            = self.printMatchesVar.get()
		cmp.printMismatches         = self.printMismatchesVar.get()
		cmp.printTrailingMismatches = self.printTrailingMismatchesVar.get()
		
		if cmp.printMatches:
			cmp.printBothMatches = self.printBothMatchesVar.get()
		else:
			cmp.printBothMatches = false
		
		if self.stopAfterMismatchVar.get():
			try:
				count = self.countEntry.get()
				cmp.limitCount = int(count)
			except: cmp.limitCount = 0
		else:
			cmp.limitCount = 0
		
		return result
	#@-body
	#@-node:5:C=4:setIvarsFromWidgets
	#@+node:6:C=5:Event handlers...
	#@+node:1::onBrowse...
	#@+body
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
	#@-body
	#@-node:1::onBrowse...
	#@+node:2::onClose
	#@+body
	def onClose (self):
		
		self.top.withdraw()
	#@-body
	#@-node:2::onClose
	#@+node:3::onCompare...
	#@+body
	def onCompareDirectories (self):
	
		cmp = self.cmp
		ok = self.setIvarsFromWidgets()
		#cmp.showIvars()
		if ok:
			cmp.compare_directories(cmp.fileName1,cmp.fileName2)
	
	def onCompareFiles (self):
	
		cmp = self.cmp
		ok = self.setIvarsFromWidgets()
		#cmp.showIvars()
		if ok:
			cmp.compare_files(cmp.fileName1,cmp.fileName2)
	#@-body
	#@-node:3::onCompare...
	#@+node:4::onPrintMatchedLines
	#@+body
	def onPrintMatchedLines (self):
		
		v = self.printMatchesVar.get()
		b = self.printButtons[1]
		state = choose(v,"normal","disabled")
		b.configure(state=state)
	#@-body
	#@-node:4::onPrintMatchedLines
	#@-node:6:C=5:Event handlers...
	#@-others
	
	#@-body
	#@-node:3::<< class leoComparePanel methods >>

	
if __name__ == "__main__":
	pass
#@-body
#@-node:0::@file leoCompare.py
#@-leo
