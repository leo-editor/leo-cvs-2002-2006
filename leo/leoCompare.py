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
		
		appendOutput = true,

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
#@+node:3::class leoCompare
#@+body
class leoCompare:

	#@+others
	#@+node:1::compare.__init__
	#@+body
	# All these ivars are known to the leoComparePanel class.
	
	def __init__ (self,
	
		# Keyword arguments are much convenient and more clear for scripts.
		commands = None,
		
		appendOutput = false,
	
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
		
		self.appendOutput = appendOutput
	
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
	#@+node:2::compare_directories (entry)
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
		ok = self.outputFileName == None or self.outputFile
		if not ok:
			return
	
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
		for kind, files in (
			("----- matches --------",yes),
			("----- mismatches -----",no),
			("----- not found ------",fail)):
			self.show(kind)
			for f in files:
				self.show(f)
		
		if self.outputFile:
			self.outputFile.close()
			self.outputFile = None
	#@-body
	#@-node:2::compare_directories (entry)
	#@+node:3::compare_files (entry)
	#@+body
	def compare_files (self, name1, name2):
		
		if name1 == name2:
			self.show("File names are identical.\nPlease pick distinct files.")
			return
	
		f1 = f2 = None
		try:
			f1 = self.doOpen(name1)
			f2 = self.doOpen(name2)
			if self.outputFileName:
				self.openOutputFile()
			ok = self.outputFileName == None or self.outputFile
			ok = choose(ok and ok != 0,1,0)
			if f1 and f2 and ok: # Don't compare if there is an error opening the output file.
				self.compare_open_files(f1,f2,name1,name2)
		except:
			import traceback
			self.show("exception comparing files")
			traceback.print_exc()
		try:
			if f1: f1.close()
			if f2: f2.close()
			if self.outputFile:
				self.outputFile.close() ; self.outputFile = None
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
	
		# self.show("compare_open_files")
		lines1 = 0 ; lines2 = 0 ; mismatches = 0 ; printTrailing = true
		sentinelComment1 = sentinelComment2 = None
		if self.openOutputFile():
			self.show("1: " + name1)
			self.show("2: " + name2)
			self.show("")
		s1 = s2 = None
		
		#@<< handle opening lines >>
		#@+node:1::<< handle opening lines >>
		#@+body
		if self.ignoreSentinelLines:
			
			s1 = readlineForceUnixNewline(f1) ; lines1 += 1
			s2 = readlineForceUnixNewline(f2) ; lines2 += 1
			# Note: isLeoHeader may return None.
			sentinelComment1 = self.isLeoHeader(s1)
			sentinelComment2 = self.isLeoHeader(s2)
			if not sentinelComment1: self.show("no @+leo line for " + name1)
			if not sentinelComment2: self.show("no @+leo line for " + name2)
				
		if self.ignoreFirstLine1:
			if s1 == None:
				readlineForceUnixNewline(f1) ; lines1 += 1
			s1 = None
		
		if self.ignoreFirstLine2:
			if s2 == None:
				readlineForceUnixNewline(f2) ; lines2 += 1
			s2 = None
		#@-body
		#@-node:1::<< handle opening lines >>

		while 1:
			if s1 == None:
				s1 = readlineForceUnixNewline(f1) ; lines1 += 1
			if s2 == None:
				s2 = readlineForceUnixNewline(f2) ; lines2 += 1
			
			#@<< ignore blank lines and/or sentinels >>
			#@+node:2::<< ignore blank lines and/or sentinels >>
			#@+body
			# Completely empty strings denotes end-of-file.
			if s1 and len(s1) > 0:
				if self.ignoreBlankLines and len(string.strip(s1)) == 0:
					s1 = None ; continue
					
				if self.ignoreSentinelLines and sentinelComment1 and self.isSentinel(s1,sentinelComment1):
					s1 = None ; continue
			
			if s2 and len(s2) > 0:
				if self.ignoreBlankLines and len(string.strip(s2)) == 0:
					s2 = None ; continue
			
				if self.ignoreSentinelLines and sentinelComment2 and self.isSentinel(s2,sentinelComment2):
					s2 = None ; continue

			#@-body
			#@-node:2::<< ignore blank lines and/or sentinels >>

			n1 = len(s1) ; n2 = len(s2)
			if n1==0 and n2 != 0: self.show("1.eof***:")
			if n2==0 and n1 != 0: self.show("2.eof***:")
			if n1==0 or n2==0: break
			match = self.compare_lines(s1,s2)
			if not match: mismatches += 1
			
			#@<< print matches and/or mismatches >>
			#@+node:3::<< print matches and/or mismatches >>
			#@+body
			if self.limitCount == 0 or mismatches <= self.limitCount:
			
				if match and self.printMatches:
					
					if self.printBothMatches:
						self.dump(string.rjust("1." + `lines1`,6) + ' :',s1)
						self.dump(string.rjust("2." + `lines2`,6) + ' :',s2)
					else:
						self.dump(string.rjust(       `lines1`,6) + ' :',s1)
				
				if not match and self.printMismatches:
					
					self.dump(string.rjust("1." + `lines1`,6) + '*:',s1)
					self.dump(string.rjust("2." + `lines2`,6) + '*:',s2)
			#@-body
			#@-node:3::<< print matches and/or mismatches >>

			
			#@<< warn if mismatch limit reached >>
			#@+node:4::<< warn if mismatch limit reached >>
			#@+body
			if self.limitCount > 0 and mismatches >= self.limitCount:
				
				if printTrailing:
					self.show("")
					self.show("limit count reached")
					self.show("")
					printTrailing = false
			#@-body
			#@-node:4::<< warn if mismatch limit reached >>

			s1 = s2 = None # force a read of both lines.
		
		#@<< handle reporting after at least one eof is seen >>
		#@+node:5::<< handle reporting after at least one eof is seen >>
		#@+body
		if n1 > 0: 
			lines1 += self.dumpToEndOfFile("1.",f1,s1,lines1,printTrailing)
			
		if n2 > 0:
			lines2 += self.dumpToEndOfFile("2.",f2,s2,lines2,printTrailing)
		
		self.show("")
		self.show("lines1:" + `lines1`)
		self.show("lines2:" + `lines2`)
		self.show("mismatches:" + `mismatches`)
		#@-body
		#@-node:5::<< handle reporting after at least one eof is seen >>
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
			self.show("can not open:" + '"' + name + '"')
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
				if 1:
					out += ch
				else: # I don't know why I thought this was a good idea ;-)
					if ch == '\t' or ch == ' ':
						out += ' '
					else:
						out += ch
	
		self.show(out)
	#@-body
	#@-node:2::dump
	#@+node:3::dumpToEndOfFile
	#@+body
	def dumpToEndOfFile (self,tag,f,s,line,printTrailing):
	
		trailingLines = 0
		while 1:
			if not s:
				s = readlineForceUnixNewline(f)
			if len(s) == 0: break
			trailingLines += 1
			if self.printTrailingMismatches and printTrailing:
				tag2 = string.rjust(tag + `line`,6) + "+:"
				self.dump(tag2,s)
			s = None
	
		self.show(tag + `trailingLines` + " trailing lines")
		return trailingLines
	#@-body
	#@-node:3::dumpToEndOfFile
	#@+node:4::isLeoHeader & isSentinel
	#@+body
	#@+at
	#  These methods are based on atFile.scanHeader().  They are simpler 
	# because we only care about the starting sentinel comment: any line 
	# starting with the starting sentinel comment is presumed to be a sentinel line.

	#@-at
	#@@c
	
	def isLeoHeader (self,s):
		
		from leoUtils import skip_ws
		tag = "@+leo"
		j = string.find(s,tag)
		if j > 0:
			i = skip_ws(s,0)
			if i < j: return s[i:j]
			else: return None
		else: return None
			
	def isSentinel (self,s,sentinelComment):
		
		from leoUtils import skip_ws, match
		i = skip_ws(s,0)
		return match(s,i,sentinelComment)
	#@-body
	#@-node:4::isLeoHeader & isSentinel
	#@+node:5::openOutputFile (compare)
	#@+body
	def openOutputFile (self):
		
		if self.outputFileName == None:
			return
		dir,name = os.path.split(self.outputFileName)
		if len(dir) == 0:
			self.show("empty output directory")
			return
		if len(name) == 0:
			self.show("empty output file name")
			return
		if not os.path.exists(dir):
			self.show("output directory not found: " + dir)
		else:
			try:
				if self.appendOutput:
					self.show("appending to " + self.outputFileName)
					self.outputFile = open(self.outputFileName,"ab")
				else:
					self.show("writing to " + self.outputFileName)
					self.outputFile = open(self.outputFileName,"wb")
			except:
				self.outputFile = None
				self.show("exception opening output file")
				traceback.print_exc()
	#@-body
	#@-node:5::openOutputFile (compare)
	#@+node:6::show
	#@+body
	def show (self,s):
		
		# print s
		if self.outputFile:
			self.outputFile.write(s + '\n')
		elif self.commands:
			from leoGlobals import es
			es(s)
		else:
			print s
			print
	#@-body
	#@-node:6::show
	#@+node:7::showIvars
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
	#@-node:7::showIvars
	#@-node:7::utils...
	#@-others
#@-body
#@-node:3::class leoCompare
#@+node:4::class leoComparePanel
#@+body
class leoComparePanel:

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
	#@+node:2::comparePanel.__init__
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
		
		# These ivars are set from Entry widgets.
		self.limitCount = 0
		self.limitToExtension = None 
		if 0: # we just use the cmp ivars.
			self.pathName1 = None
			self.pathName2 = None
			self.outputFileName = None
		
		# The default file name in the "output file name" browsers.
		self.defaultOutputFileName = "CompareResults.txt"
	#@-body
	#@-node:2::comparePanel.__init__
	#@+node:3::finishCreate
	#@+body
	# Initialize ivars from config parameters.
	
	def finishCreate (self):
		
		from leoGlobals import app
		config = app().config
		
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
		self.ignoreFirstLine1Var.set(b)
		
		b = config.getBoolComparePref("ignore_first_line_of_file_2")
		self.ignoreFirstLine2Var.set(b)
		
		b = config.getBoolComparePref("append_output_to_output_file")
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
		self.printBothMatchesVar.set(b)
		
		b = config.getBoolComparePref("print_matching_lines")
		self.printMatchesVar.set(b)
		
		b = config.getBoolComparePref("print_mismatching_lines")
		self.printMismatchesVar.set(b)
		
		b = config.getBoolComparePref("print_trailing_lines")
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
		self.ignoreBlankLinesVar.set(b)
		
		b = config.getBoolComparePref("ignore_interior_whitespace")
		self.ignoreInteriorWhitespaceVar.set(b)
		
		b = config.getBoolComparePref("ignore_leading_whitespace")
		self.ignoreLeadingWhitespaceVar.set(b)
		
		b = config.getBoolComparePref("ignore_sentinel_lines")
		self.ignoreSentinelLinesVar.set(b)
		
		b = config.getBoolComparePref("make_whitespace_visible")
		self.makeWhitespaceVisibleVar.set(b)
	#@-body
	#@-node:3::finishCreate
	#@+node:4::run
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
			text="Limit directory compares to type:")
		b.pack(side="left",padx=4)
		
		self.extensionEntry = e = Tk.Entry(row4,width=6)
		e.pack(side="left",padx=2)
		
		b = Tk.Checkbutton(row4,anchor="w",var=self.appendOutputVar,
			text="Append output to output file")
		b.pack(side="left",padx=4)
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
	#@-node:4::run
	#@+node:5::show
	#@+body
	def show (self,s):
		
		self.cmp.show(s)
	#@-body
	#@-node:5::show
	#@+node:6::setIvarsFromWidgets
	#@+body
	def setIvarsFromWidgets (self):
	
		cmp = self.cmp
		
		# File paths. cmp checks for valid file name.
		e = self.browseEntries[0]
		cmp.fileName1 = e.get()
		
		e = self.browseEntries[1]
		cmp.fileName2 = e.get()
	
		# Ignore first line settings.
		cmp.ignoreFirstLine1 = self.ignoreFirstLine1Var.get()
		cmp.ignoreFirstLine2 = self.ignoreFirstLine2Var.get()
		
		# Output file.  cmp checks for valid file name.
		if self.useOutputFileVar.get():
			e = self.browseEntries[2]
			name = e.get()
			if name != None and len(name) == 0:
				name = None
			cmp.outputFileName = name
		else:
			cmp.outputFileName = None
	
		# Extension settings.
		if self.limitToExtensionVar.get():
			cmp.limitToExtension = self.extensionEntry.get()
			if len(cmp.limitToExtension) == 0:
				cmp.limitToExtension = None
		else:
			cmp.limitToExtension = None
			
		cmp.appendOutput = self.appendOutputVar.get()
		
		# Whitespace options.
		cmp.ignoreBlankLines         = self.ignoreBlankLinesVar.get()
		cmp.ignoreInteriorWhitespace = self.ignoreInteriorWhitespaceVar.get()
		cmp.ignoreLeadingWhitespace  = self.ignoreLeadingWhitespaceVar.get()
		cmp.ignoreSentinelLines      = self.ignoreSentinelLinesVar.get()
		cmp.makeWhitespaceVisible    = self.makeWhitespaceVisibleVar.get()
		
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
	#@-body
	#@-node:6::setIvarsFromWidgets
	#@+node:7::Event handlers...
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
		self.setIvarsFromWidgets()
		cmp.compare_directories(cmp.fileName1,cmp.fileName2)
	
	def onCompareFiles (self):
	
		cmp = self.cmp
		ok = self.setIvarsFromWidgets()
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
	#@-node:7::Event handlers...
	#@-others
#@-body
#@-node:4::class leoComparePanel
#@-others


if __name__ == "__main__":
	pass
#@-body
#@-node:0::@file leoCompare.py
#@-leo
