#@+leo

#@+node:0::@file leoCompare.py
#@+body
#@@language python

# The code for Leo's Compare Panel and the compare class.

import difflib, filecmp, os, string

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
		
		limitToExtension = ".py",  # For directory compares.
		
		printMatches = false,
		printMismatches = true,
		printTrailingMismatches = false,
		stopAfterMismatch = false,
		
		outputFileName = None,
		verbose = false )

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
	
		ignoreAllWhitespace = false,
		ignoreBlankLines = true,
		ignoreFirstLine1 = false,
		ignoreFirstLine2 = false,
		ignoreInteriorWhitespace = false,
		ignoreLeadingWhitespace = true,
		ignoreSentinelLines = false,
	
		limitToExtension = ".py",  # For directory compares.
	
		printMatches = false,
		printMismatches = true,
		printTrailingMismatches = false,
		stopAfterMismatch = false,
	
		outputFileName = None,
		verbose = false ):
			
		# It is more convenient for the leoComparePanel to set these directly.
		self.commands = commands
	
		self.ignoreBlankLines = ignoreBlankLines
		self.ignoreFirstLine1 = ignoreFirstLine1
		self.ignoreFirstLine2 = ignoreFirstLine2
		self.ignoreInteriorWhitespace = ignoreInteriorWhitespace
		self.ignoreLeadingWhitespace = ignoreLeadingWhitespace
		self.ignoreSentinelLines = ignoreSentinelLines
	
		self.limitToExtension = limitToExtension
	
		self.printMatches = printMatches
		self.printMismatches = printMismatches
		self.printTrailingMismatches = printTrailingMismatches
		self.stopAfterMismatch = stopAfterMismatch
		self.verbose = verbose
		
		# For communication between methods...
		self.outputFileName = outputFileName
		self.fileName1 = None 
		self.fileName2 = None
		self.lines = 0
		self.mismatches = 0
		# Open files...
		self.outputFile = None
	#@-body
	#@-node:1::compare.__init__
	#@+node:2::compare_directories (entry)
	#@+body
	def compare_directories (self,dir1,dir2):
		
		# self.show("dir1:" + dir1)
		# self.show("dir2:" + dir2)
		list1 = os.listdir(dir1)
		list2 = os.listdir(dir2)
		
		# Create files and files2, the lists of files to be compared.
		files1 = []
		files2 = []
		for f in list1:
			junk, ext = os.path.splitext(f)
			if ext == self.ext:
				files1.append(f)
		for f in list2:
			junk, ext = os.path.splitext(f)
			if ext == self.ext:
				files2.append(f)
	
		# Compare the files and set the yes, no and fail lists.
		yes = [] ; no = [] ; fail = []
		for f1 in files1:
			head,f2 = os.path.split(f1)
			if f2 in files2:
				val = filecmp.cmp(dir1+self.file1,dir2+f2,0)
				if val: yes.append(f1)
				else:    no.append(f1)
			else:      fail.append(f1)
		
		# Print the results.
		self.show("\n")
		for kind, files in (
			("matches:   ",yes),
			("mismatches:",no),
			("not found: ",fail)):
			self.show(kind)
			for f in files:
				self.show(`f`)
		self.show("\n")
	#@-body
	#@-node:2::compare_directories (entry)
	#@+node:3::compare_files (entry)
	#@+body
	def compare_files (self, name1, name2):
		
		self.showIvars()
		return
		
		f1 = f2 = None
		try:
			f1=cmp.doOpen(name1)
			f2=cmp.doOpen(name2)
			if f1 and f2:
				cmp.compare_open_files(f1,f2,name1,name2)
		except: pass
	
		try:
			if f1: f1.close()
			if f2: f2.close()
		except: pass
	#@-body
	#@-node:3::compare_files (entry)
	#@+node:4::compare_lines
	#@+body
	def compare_lines (self,s1,s2):
	
		if self.ignoreAllWhitespace:
			s1 = string.replace(s1," ","")
			s1 = string.replace(s1,"\t","")
			s2 = string.replace(s2," ","")
			s2 = string.replace(s2,"\t","")
		elif self.ignoreLeadingWhitespace:
			s1 = string.lstrip(s1)
			s2 = string.lstrip(s2)
	
		return s1 == s2
	#@-body
	#@-node:4::compare_lines
	#@+node:5::compare_open_files
	#@+body
	def compare_open_files (self, f1, f2, name1, name2):
	
		self.lines = 0 ; self.mismatches = 0
		if self.ignoreFirstLines:
			s1 = f1.readline()
			s2 = f2.readline()
		while 1:
			s1 = f1.readline() ; s2 = f2.readline()
			if self.ignoreLeadingWhitespace:
				s1 = string.lstrip(s1)
				s2 = string.lstrip(s2)
			if self.ignoreBlankLines: # LeoCB doesn't delete whitespace as well as leo.py.
				
				#@<< ignore blank lines >>
				#@+node:1::<< ignore blank lines >>
				#@+body
				while 1:
					s = string.rstrip(s1)
					if len(s) == 0:
						s1 = self.file1.readline()
						if len(s1) == 0: break # end of file
					else: break
				
				while 1:
					s = string.rstrip(s2)
					if len(s) == 0:
						s2 = f2.readline()
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
			lines += 1
			if self.verbose or not match:
				mark = choose(match,' ','*')
				self.dump("1.",lines,mark,s1)
				self.dump("2.",lines,mark,s2)
				if mismatches > 9: return
	
		self.show("lines:" + `lines` + ", mismatches:", `mismatches`)
		if n1>0: dumpToEndOfFile("1",f1)
		if n2>0: dumpToEndOfFile("2",f2)
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
	#@+body
	# We don't import any leo file so that this file can be used as a script.
	#@-body
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
	def dump (self,tag,line,mark,s):
	
		out = tag + `line` + mark + ':' 
		for ch in s[:-1]: # don't print the newline
			if 0: # compact
				if ch == '\t' or ch == ' ':
					out += ' '
				else:
					out += ch
			else: # more visible
				if ch == '\t':
					out += "[" ; out += "t" ; out += "]"
				elif ch == ' ':
					out += "[" ; out += " " ; out += "]"
				else: out += ch
		self.show(out)

	#@-body
	#@-node:2::dump
	#@+node:3::dumpToEndOfFile
	#@+body
	def dumpToEndOfFile (self,tag,f):
	
		trailingLines = 0
		while 1:
			s = f.readline()
			if len(s) == 0: break
			trailingLines += 1
			if self.dumpTrailingMismatches:
				self.dump(tag,s)
	
		self.show("file " + tag, " has " + trailingLines + " trailing lines")
		return trailingLines
	#@-body
	#@-node:3::dumpToEndOfFile
	#@+node:4::show
	#@+body
	def show (self,s):
		
		if self.commands:
			from leoGlobals import es
			es(s)
		else:
			print s
			print
	#@-body
	#@-node:4::show
	#@+node:5::showIvars
	#@+body
	def showIvars (self):
		
		self.show("fileName1:" + `self.fileName1`)
		self.show("fileName2:" + `self.fileName2`)
		self.show("outputFileName:" + `self.outputFileName`)
		self.show("limitToExtension:" + `self.limitToExtension`)
		self.show("")
	
		self.show("ignoreBlankLines:"         + `self.ignoreBlankLines`)
		self.show("ignoreFirstLine1:"         + `self.ignoreFirstLine1`)
		self.show("ignoreFirstLine2:"         + `self.ignoreFirstLine2`)
		self.show("ignoreInteriorWhitespace:" + `self.ignoreInteriorWhitespace`)
		self.show("ignoreLeadingWhitespace:"  + `self.ignoreLeadingWhitespace`)
		self.show("ignoreSentinelLines:"      + `self.ignoreSentinelLines`)
		self.show("")
		
		self.show("printMatches:"            + `self.printMatches`)
		self.show("printMismatches:"         + `self.printMismatches`)
		self.show("printTrailingMismatches:" + `self.printTrailingMismatches`)
		self.show("stopAfterMismatch:"       + `self.stopAfterMismatch`)
		self.show("verbose:"                 + `self.verbose`)
	#@-body
	#@-node:5::showIvars
	#@-node:7::utils...
	#@-others
	
	#@-body
	#@-node:2::<< class leoCompare methods >>

	
class leoComparePanel:
	
	#@<< class leoComparePanel methods >>
	#@+node:3::<< class leoComparePanel methods >>
	#@+body
	#@+others
	#@+node:1:C=1:comparePanel.__init__
	#@+body
	def __init__ (self,c,cmp):
		
		import Tkinter
		Tk = Tkinter
		
		self.commands = c
		self.cmp = cmp
		
		# Ivars pointing to Tk elements.
		self.browseEntries = []
		self.extensionEntry = None
		
		# Create IntVars for all checkboxes...
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
		
		self.printMatchesVar             = Tk.IntVar()
		self.printMismatchesVar          = Tk.IntVar()
		self.printTrailingMismatchesVar  = Tk.IntVar()
		self.stopAfterMismatchVar        = Tk.IntVar()
		
		self.verboseVar                  = Tk.IntVar()
		
		# These ivars are set from Entry widgets.
		self.limitToExtension = ".py"
		self.pathName1 = None
		self.pathName2 = None
		self.outputFileName = None
		
		#--------------------
		
		self.ignoreFirstLine1Var.set(0)
		self.ignoreFirstLine2Var.set(0)
		self.useOutputFileVar.set(0)
		
		self.stopAfterMismatchVar.set(0)
	#@-body
	#@-node:1:C=1:comparePanel.__init__
	#@+node:2:C=2:run
	#@+body
	def run (self):
		
		# We import these here so as not to interfere with scripts
		from leoUtils   import center_dialog, create_labeled_frame, shortFileName
		from leoGlobals import app
		import leoApp, leoCommands, Tkinter
	
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
			("Ignore interior whitespace",self.ignoreInteriorWhitespaceVar) ):
			
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
		
		for text,var in (
			("Stop at first mismatch",        self.stopAfterMismatchVar),      
			("Print matched lines",           self.printMatchesVar),
			("Print mismatched lines",        self.printMismatchesVar),
			("Print unmatched trailing lines",self.printTrailingMismatchesVar),
			("Verbose",                       self.verboseVar) ):
			
			b = Tk.Checkbutton(f,text=text,variable=var)
			b.pack(side="top",anchor="w")
			
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
	#@-body
	#@-node:2:C=2:run
	#@+node:3:C=3:setIvarsFromWidgets
	#@+body
	def setIvarsFromWidgets (self):
		
		import os
		from leoGlobals import es
		cmp = self.cmp ; result = true
		
		# File paths.
		e = self.browseEntries[0]
		cmp.fileName1 = e.get()
		
		e = self.browseEntries[1]
		cmp.fileName2 = e.get()
		
		# Make sure paths actually exist.
		for name in (self.pathName1, self.pathName2):
			if name and len(name) > 0:
				if not os.path.exists(name):
					es("path not found: " + name)
					result = false
			else:
				es("missing compare path")
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
		
		# Whitespace options.
		cmp.ignoreBlankLines         = self.ignoreBlankLinesVar.get()
		cmp.ignoreInteriorWhitespace = self.ignoreInteriorWhitespaceVar.get()
		cmp.ignoreLeadingWhitespace  = self.ignoreLeadingWhitespaceVar.get()
		cmp.ignoreSentinelLines      = self.ignoreSentinelLinesVar.get()
		
		# Print options.
		cmp.printMatches            = self.printMatchesVar.get()
		cmp.printMismatches         = self.printMismatchesVar.get()
		cmp.printTrailingMismatches = self.printTrailingMismatchesVar.get()
		cmp.stopAfterMismatch       = self.stopAfterMismatchVar.get()
		cmp.verbose                 = self.verboseVar.get()
		
		return result
	#@-body
	#@-node:3:C=3:setIvarsFromWidgets
	#@+node:4:C=4:Event handlers...
	#@+node:1::onClose
	#@+body
	def onClose (self):
		
		self.top.withdraw()
	#@-body
	#@-node:1::onClose
	#@+node:2::onCompare...
	#@+body
	def onCompareDirectories (self):
	
		ok = self.setIvarsFromWidgets()
		self.cmp.showIvars()
		if ok:
			self.cmp.compare_directories(cmp.pathName1,cmp.pathName2)
	
	def onCompareFiles (self):
	
		ok = self.setIvarsFromWidgets()
		self.cmp.showIvars()
		if ok:
			self.cmp.compare_files(cmp.pathName1,cmp.pathName2)
	#@-body
	#@-node:2::onCompare...
	#@+node:3::onBrowse...
	#@+body
	def onBrowse1 (self):
		
		pass
		
	def onBrowse2 (self):
		
		pass
		
	def onBrowse3 (self):
		
		pass
	#@-body
	#@-node:3::onBrowse...
	#@-node:4:C=4:Event handlers...
	#@-others
	
	#@-body
	#@-node:3::<< class leoComparePanel methods >>

	
if __name__ == "__main__":
	pass
#@-body
#@-node:0::@file leoCompare.py
#@-leo
