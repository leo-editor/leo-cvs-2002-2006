#@+leo

#@+node:0::@file leoCompare.py
#@+body
#@+at
#  This file contains compare routines used for testing and I hack away as needed.  To save typing, I usually invoke the go() from 
# the Python interpreter.

#@-at
#@@c

import difflib, filecmp, os, string


#@+others
#@+node:1::choose
#@+body
def choose(cond, a, b): # warning: evaluates all arguments

	if cond: return a
	else: return b

#@-body
#@-node:1::choose
#@+node:2::cmp
#@+body
def cmp(name1,name2):

	val = filecmp.cmp(name1,name2,0)
	if 1:
		if val: print "equal"
		else:   print "*** not equal"
	else:
		print "filecmp.cmp returns:",
		if val: print val, "(equal)"
		else:   print val, "(not equal)"

	return val
#@-body
#@-node:2::cmp
#@+node:3::compare
#@+body
def compare(f1,f2,name1,name2,verbose):

	lines = 0 ; mismatches = 0
	s1 = f1.readline() ; s2 = f2.readline() # Ignore the first line!
	while 1:
		s1 = f1.readline() ; s2 = f2.readline()
		if 1: # Ignore leading whitespace
			s1 = string.lstrip(s1)
			s2 = string.lstrip(s2)
		if 1: # LeoCB doesn't delete whitespace as well as leo.py.
			
			#@<< ignore blank lines >>
			#@+node:1::<< ignore blank lines >>
			#@+body
			while 1:
				s = string.rstrip(s1)
				if len(s) == 0:
					s1 = f1.readline()
					if len(s1) == 0: break
				else: break
			while 1:
				s = string.rstrip(s2)
				if len(s) == 0:
					s2 = f2.readline()
					if len(s1) == 0: break
				else: break
			#@-body
			#@-node:1::<< ignore blank lines >>

		n1 = len(s1) ; n2 = len(s2)
		if n1==0 and n2 != 0: print "eof on", name1
		if n2==0 and n1 != 0: print "eof on", name2
		if n1==0 or n2==0: break
		match = compare_lines(s1,s2)
		if not match: mismatches += 1
		lines += 1
		if verbose or not match:
			mark = choose(match,' ','*')
			dump("1.",lines,mark,s1)
			dump("2.",lines,mark,s2)
			if mismatches > 9: return

	return #
	print "lines", lines, "mismatches:", mismatches
	if n1>0: dumpEnd("1",f1)
	if n2>0: dumpEnd("2",f2)
#@-body
#@-node:3::compare
#@+node:4::compare_files
#@+body
def compare_files (name1,name2,verbose):
	
	f1=doOpen(name1)
	f2=doOpen(name2)
	if f1 and f2:
		compare(f1,f2,name1,name2,verbose)
	try:
		f1.close()
		f2.close()
	except: pass
#@-body
#@-node:4::compare_files
#@+node:5::compare_lines
#@+body
def compare_lines(s1,s2):

	if 0: # ignore all whitespace
		s1 = string.replace(s1," ","")
		s1 = string.replace(s1,"\t","")
		s2 = string.replace(s2," ","")
		s2 = string.replace(s2,"\t","")
	else: # ignore leading and/or trailing whitespace
		s1 = string.strip(s1)
		s2 = string.strip(s2)
	return s1==s2
#@-body
#@-node:5::compare_lines
#@+node:6::compareDirs
#@+body
def compareDirs(dir1,dir2): # make ".py" an arg.

  print "dir1:", dir1
  print "dir2:", dir2
  list1 = os.listdir(dir1)
  list2 = os.listdir(dir2)
  py1 = [] ; py2 = []
  for f in list1:
    root, ext = os.path.splitext(f)
    if ext == ".py": py1.append(f)
  for f in list2:
    root, ext = os.path.splitext(f)
    if ext == ".py": py2.append(f)
  print "comparing using filecmp.cmp"
  print
  yes = [] ; no = [] ; fail = []
  for f1 in py1:
    head,f2 = os.path.split(f1)
    if f2 in py2:
      val = filecmp.cmp(dir1+f1,dir2+f2,0)
      if val:  yes.append(f1)
      else: no.append(f1)
    else: fail.append(f1)

  print "matches:",
  for f in yes:  print f,
  print ; print "mismatches:",
  for f in no:   print f,
  print ; print "not found:",
  for f in fail: print f,
#@-body
#@-node:6::compareDirs
#@+node:7::compare_directories
#@+body
def compare_directories(path1,path2,verbose):

	files = os.listdir(path1)
	files.sort()
	for f in files:
		if os.path.exists(path2 + f):
			val = filecmp.cmp(path1 + f, path2 + f)
			# print "cmp:", val, f
		else:
			print path2+f, "does not exist in both directories"
			files.remove(f)

	print "1." + path1
	print "2." + path2
	for f in files:
		name1 = path1 + f ; name2 = path2 + f
		val = filecmp.cmp(name1,name2)
		if val == 0:
			f1 = open(name1) ; f2 = open(name2)
			print f
			# note: should have param telling how to deal with whitespace.
			compare(f1,f2,name1,name2,verbose)
			f1.close() ; f2.close()
			## return ## just one
#@-body
#@-node:7::compare_directories
#@+node:8::crlf & count_crlf
#@+body
def crlf(f1,f2):
	s1=f1.read() ; s2=f2.read()
	cr, lf = count_crlf(s1)
	print name1, cr, lf
	cr, lf = count_crlf(s2)
	print name2, cr, lf

def count_crlf(s):
	cr, lf = 0, 0
	for i in s:
		if i == '\n': lf += 1
		if i == '\r': cr += 1
	return cr,lf

#@-body
#@-node:8::crlf & count_crlf
#@+node:9::diff (does not exist!)
#@+body
def diff(f1,f2):

	s1=f1.read() ; s2=f2.read()
	s = difflib.Differ()
	delta = s.compare(s1,s2)
	print len(delta)
#@-body
#@-node:9::diff (does not exist!)
#@+node:10::doOpen
#@+body
def doOpen(name):

	try:
		f = open(name,'r')
		return f
	except:
		print "can not open:", `name`
		return None
#@-body
#@-node:10::doOpen
#@+node:11::dump
#@+body
def dump(tag,line,mark,s):

	out = tag + `line` + mark + ':' 
	for ch in s[:-1]: # don't print the newline
		if 0: # compact
			if ch == '\t' or ch == ' ':
				out += ' '
			else:
				out += ch
		else: # more visible
			if ch=='\t':
				out += "[" ; out += "t" ; out += "]"
			elif ch==' ':
				out += "[" ; out += " " ; out += "]"
			else: out += ch
	print out

#@-body
#@-node:11::dump
#@+node:12::dumpEnd
#@+body
def dumpEnd(tag,f):

	lines = 0
	while 1:
		s = f.readline()
		if len(s) == 0: break
		lines += 1
		# dump(tag,s)

	print "file", tag, "has", lines, "trailing lines"
#@-body
#@-node:12::dumpEnd
#@+node:13::go()
#@+body
def go(name=None):

	if 1: # Compare all files in Tangle test directories
		path1 = "c:\\prog\\test\\tangleTest\\"
		path2 = "c:\\prog\\test\\tangleTestCB\\"
		verbose = 0
		compare_directories(path1,path2,verbose)
	else: # Compare two files.
		name1 = "c:\\prog\\test\\compare1.txt"
		name2 = "c:\\prog\\test\\compare2.txt"
		verbose = 0
		compare_files(name1,name2,verbose)
#@-body
#@-node:13::go()
#@+node:14::sequence (hangs)
#@+body
def sequence(f1,f2):

	s = difflib.SequenceMatcher()
	s1 = f1.read() ; s2 = f2.read()
	print len(s1), len(s2)
	# codes = s.get_opcodes() # hangs.
	# print len(codes)
	# print s.ratio() # hangs

#@-body
#@-node:14::sequence (hangs)
#@-others

#@-body
#@-node:0::@file leoCompare.py
#@-leo
