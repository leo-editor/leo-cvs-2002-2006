#@+leo

#@+node:0::@file leoCompare.py
#@+body
#@@language python

# The code for Leo's Compare Panel and the compare class.

import difflib, filecmp, os, string


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
	
	cmp = leoCompare(None,verbose=0)

	if 1: # Compare all files in Tangle test directories
		path1 = "c:\\prog\\test\\tangleTest\\"
		path2 = "c:\\prog\\test\\tangleTestCB\\"
		verbose = 0
		cmp.compare_directories(path1,path2)

	else: # Compare two files.
		name1 = "c:\\prog\\test\\compare1.txt"
		name2 = "c:\\prog\\test\\compare2.txt"
		verbose = 0
		cmp.compare_files(name1,name2)
#@-body
#@-node:2::go
#@-others
#@-body
#@-node:1::<< define functions >>


class leoCompare:
	
	#@<< class leoCompare constants >>
	#@+node:2::<< class leoCompare constants >>
	#@+body
	# Comparison modes
	print_mismatches = "print mismatches"
	print_all_lines = "print all lines"
	#@-body
	#@-node:2::<< class leoCompare constants >>

	
	#@<< class leoCompare methods >>
	#@+node:3::<< class leoCompare methods >>
	#@+body
	#@+others
	#@+node:1::compare.__init__
	#@+body
	# All these ivars are known to the leoComparePanel class.
	
	def __init__ (self,
	
		# Keyword arguments are much convenient and more clear for scripts.
		commands = None,
		dumpTrailingMismatches = false,
		ext = ".py",  # The file extension to use when compared in directories.
		ignoreAllWhitespace = false,
		ignoreBlankLines = true,
		ignoreFirstLines = false,
		ignoreLeadingWhitespace = true,
		printMode = print_mismatches, # print_all or print_all_lines.
		resultFileName = None, # Print to file.
		stopAfterMismatch = false,
		verbose = false ):
			
		# It is more convenient for the leoComparePanel to set these directly.
		self.commands = commands
		self.dumpTrailingMismatches = dumpTrailingMismatches
		self.ext = ".py"
		self.ignoreAllWhitespace = ignoreAllWhitespace
		self.ignoreBlankLines = ignoreBlankLines
		self.ignoreFirstLines = ignoreFirstLines
		self.ignoreLeadingWhitespace = ignoreLeadingWhitespace
		self.printMode = printMode
		self.resultFileName = resultFileName
		self.stopAfterMismatch = stopAfterMismatch
		self.verbose = verbose
		
		# For communication between methods...
		if 0:
			self.directoryName1 = None
			self.directoryName2 = None
		self.fileName1 = None 
		self.fileName2 = None
		self.lines = 0
		self.mismatches = 0
		# Open files...
		self.resultFile = None # The result file, if any.
	#@-body
	#@-node:1::compare.__init__
	#@+node:2::compare_directories (entry)
	#@+body
	def compare_directories (self,dir1,dir2):
	
		self.doPrint("dir1:" + dir1)
		self.doPrint("dir2:" + dir2)
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
		self.doPrint("\n")
		for kind, files in (
			("matches:   ",yes),
			("mismatches:",no),
			("not found: ",fail)):
			self.doPrint(kind)
			for f in files:
				self.doPrint(`f`)
		self.doPrint("\n")
	#@-body
	#@-node:2::compare_directories (entry)
	#@+node:3::compare_files (entry)
	#@+body
	def compare_files (self, name1, name2):
		
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
			if n1==0 and n2 != 0: self.doPrint("eof on" + name1)
			if n2==0 and n1 != 0: self.doPrint("eof on" + name2)
			if n1==0 or n2==0: break
			match = self.compare_lines(s1,s2)
			if not match: mismatches += 1
			lines += 1
			if self.verbose or not match:
				mark = choose(match,' ','*')
				self.dump("1.",lines,mark,s1)
				self.dump("2.",lines,mark,s2)
				if mismatches > 9: return
	
		self.doPrint("lines:" + `lines` + ", mismatches:", `mismatches`)
		if n1>0: dumpToEndOfFile("1",f1)
		if n2>0: dumpToEndOfFile("2",f2)
	#@-body
	#@-node:5::compare_open_files
	#@+node:6::filecmp
	#@+body
	def self.filecmp (self,f1,f2):
	
		val = filecmp.cmp(f1,f2)
		if 1:
			if val: self.doPrint("equal")
			else:   self.doPrint("*** not equal")
		else:
			self.doPrint("filecmp.cmp returns:")
			if val: self.doPrint(`val` + " (equal)"
			else:   self.doPrint(`val` + " (not equal)"
	
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
			self.doPrint("can not open:" + `name`)
			return None
	#@-body
	#@-node:1::doOpen
	#@+node:2::doPrint
	#@+body
	def doPrint (self,s):
		
		if self.commands:
			es(s) ; enl()
		else:
			print s
			print
	#@-body
	#@-node:2::doPrint
	#@+node:3::dump
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
		self.doPrint(out)

	#@-body
	#@-node:3::dump
	#@+node:4::dumpToEndOfFile
	#@+body
	def dumpToEndOfFile (self,tag,f):
	
		trailingLines = 0
		while 1:
			s = f.readline()
			if len(s) == 0: break
			trailingLines += 1
			if self.dumpTrailingMismatches:
				self.dump(tag,s)
	
		self.doPrint("file " + tag, " has " + trailingLines + " trailing lines")
		return trailingLines
	#@-body
	#@-node:4::dumpToEndOfFile
	#@-node:7::utils...
	#@-others
	
	#@-body
	#@-node:3::<< class leoCompare methods >>

	
class leoComparePanel:
	
	#@<< class leoComparePanel methods >>
	#@+node:4::<< class leoComparePanel methods >>
	#@+body
	#@+others
	#@+node:1::comparePanel.__init__
	#@+body
	def __init__ (self):
		pass
	#@-body
	#@-node:1::comparePanel.__init__
	#@-others
	
	#@-body
	#@-node:4::<< class leoComparePanel methods >>

	
if __name__ == "__main__":
	pass
#@-body
#@-node:0::@file leoCompare.py
#@-leo
