#@+leo

#@+node:0::@file leoUtils.py
#@+body
#@@language python

# Global utility functions

from leoGlobals import *
import os, string, sys, time, types, Tkinter, traceback


#@+others
#@+node:1:C=1:@language and @comment directives
#@+node:1:C=2:set_delims_from_language
#@+body
# Returns a tuple (single,start,end) of comment delims

def set_delims_from_language(language):
	
	# trace(`language`)

	for lang, val in [ (cweb_language, "// /* */"),
		(c_language, "// /* */"), (java_language, "// /* */"),
		(fortran_language, "C"), (fortran90_language, "!"),
		(html_language, "<!-- -->"), (pascal_language, "// { }"),
		(perl_language, "#"), (perlpod_language, "# =pod =cut"),
		(plain_text_language, "#"), # 7/8/02: we have to pick something.
		(shell_language, "#"), (python_language, "#"),
		(tcltk_language, "#") ]: # 7/18/02
		if lang == language:
			# trace(`val`)
			return set_delims_from_string(val)

	return None, None, None # Indicate that no change should be made
#@-body
#@-node:1:C=2:set_delims_from_language
#@+node:2:C=3:set_delims_from_string
#@+body
#@+at
#  Returns (delim1, delim2, delim2), the delims following the @comment directive.
# 
# This code can be called from @languge logic, in which case s can point at @comment

#@-at
#@@c

def set_delims_from_string(s):
	
	# trace(`s`)

	# Skip an optional @comment
	tag = "@comment"
	i = 0
	if match_word(s,i,tag):
		i += len(tag)
		
	count = 0 ; delims = [None, None, None]
	while count < 3 and i < len(s):
		i = j = skip_ws(s,i)
		while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		if j == i: break
		delims[count] = s[j:i]
		count += 1
		
	# Restore defaults if nothing specified
	if not delims[0]:
		delims[0], delims[1], delims[2] = "//", "/*", "*/"

	# 7/8/02: The "REM hack": replace underscores by blanks.
	for i in xrange(0,3):
		if delims[i]:
			delims[i] = string.replace(delims[i],'_',' ')

	return delims[0], delims[1], delims[2]
#@-body
#@-node:2:C=3:set_delims_from_string
#@+node:3:C=4:set_language
#@+body
#@+at
#   Scans the @language directive that appears at s[i]. 'default' returns default_language.
# 
# Returns (language, delim1, delim2, delim3)

#@-at
#@@c

def set_language(s,i,issue_errors_flag,default_language):

	tag = "@language"
	# trace(`get_line(s,i)`)
	assert(i != None)
	assert(match_word(s,i,tag))
	i += len(tag) ; i = skip_ws(s, i)
	# Get the argument.
	j = i
	i = skip_c_id(s,i)
	# Allow tcl/tk.
	arg = string.lower(s[j:i])
	if len(arg) > 0:
		for name, language in [ ("ada", ada_language),
			("c", c_language), ("c++", c_language),
			("cweb", cweb_language), ("default", default_language),
			("fortran", fortran_language), ("fortran90", fortran90_language),
			("html", html_language), ("java", java_language),
			("lisp", lisp_language), ("objective-c", c_language),
			("pascal", pascal_language), ("perl", perl_language),
			("perlpod", perlpod_language),
			("plain", plain_text_language), # 7/8/02
			("python", python_language),
			("shell", shell_language),
			("tcl", tcltk_language) ]: # 7/18/02.  Note: this also matches tcl/tk.
		
			if arg == name:
				delim1, delim2, delim3 = set_delims_from_language(language)
				return language, delim1, delim2, delim3

	if issue_errors_flag:
		es("ignoring: " + get_line(s,i))

	return None, None, None, None,
#@-body
#@-node:3:C=4:set_language
#@-node:1:C=1:@language and @comment directives
#@+node:2::angleBrackets & virtual_event_name
#@+body
# Returns < < s > >

def angleBrackets(s):

	return ( "<<" + s +
		">>") # must be on a separate line.

virtual_event_name = angleBrackets
#@-body
#@-node:2::angleBrackets & virtual_event_name
#@+node:3::btest
#@+body
# bit testing.

def btest(b1, b2):

	return (b1 & b2) != 0
#@-body
#@-node:3::btest
#@+node:4::create_temp_name
#@+body
# Returns a temporary file name.

def create_temp_name ():

	import tempfile
	temp = tempfile.mktemp()
	# trace(`temp`)
	return temp
#@-body
#@-node:4::create_temp_name
#@+node:5::Dialog utilites...
#@+node:1::get_window_info
#@+body
# WARNING: Call this routine _after_ creating a dialog.
# (This routine inhibits the grid and pack geometry managers.)

def get_window_info (top):
	
	top.update_idletasks() # Required to get proper info.

	# Get the information about top and the screen.
	g = top.geometry() # g = "WidthxHeight+XOffset+YOffset"
	dim,x,y = string.split(g,'+')
	w,h = string.split(dim,'x')
	w,h,x,y = int(w),int(h),int(x),int(y)
	
	return w,h,x,y
#@-body
#@-node:1::get_window_info
#@+node:2::center_dialog
#@+body
# Center the dialog on the screen.
# WARNING: Call this routine _after_ creating a dialog.
# (This routine inhibits the grid and pack geometry managers.)

def center_dialog(top):

	sw = top.winfo_screenwidth()
	sh = top.winfo_screenheight()
	w,h,x,y = get_window_info(top)
	
	# Set the new window coordinates, leaving w and h unchanged.
	x = (sw - w)/2
	y = (sh - h)/2
	top.geometry("%dx%d%+d%+d" % (w,h,x,y))
	
	return w,h,x,y
#@-body
#@-node:2::center_dialog
#@+node:3:C=5:create_labeled_frame
#@+body
# Returns frames w and f.
# Typically the caller would pack w into other frames, and pack content into f.

def create_labeled_frame (parent,
	caption=None,relief="groove",bd=2,padx=0,pady=0):
	
	Tk = Tkinter
	# Create w, the master frame.
	w = Tk.Frame(parent)
	w.grid(sticky="news")
	
	# Configure w as a grid with 5 rows and columns.
	# The middle of this grid will contain f, the expandable content area.
	w.columnconfigure(1,minsize=bd)
	w.columnconfigure(2,minsize=padx)
	w.columnconfigure(3,weight=1)
	w.columnconfigure(4,minsize=padx)
	w.columnconfigure(5,minsize=bd)
	
	w.rowconfigure(1,minsize=bd)
	w.rowconfigure(2,minsize=pady)
	w.rowconfigure(3,weight=1)
	w.rowconfigure(4,minsize=pady)
	w.rowconfigure(5,minsize=bd)

	# Create the border spanning all rows and columns.
	border = Tk.Frame(w,bd=bd,relief=relief) # padx=padx,pady=pady)
	border.grid(row=1,col=1,rowspan=5,columnspan=5,sticky="news")
	
	# Create the content frame, f, in the center of the grid.
	f = Tk.Frame(w,bd=bd)
	f.grid(row=3,col=3,sticky="news")
	
	# Add the caption.
	if caption and len(caption) > 0:
		caption = Tk.Label(parent,text=caption,highlightthickness=0,bd=0)
		caption.tkraise(w)
		caption.grid(in_=w,row=0,col=2,rowspan=2,columnspan=3,padx=4,sticky="w")

	return w,f
#@-body
#@-node:3:C=5:create_labeled_frame
#@-node:5::Dialog utilites...
#@+node:6::Dumping, Tracing & Sherlock
#@+node:1::dump
#@+body
def dump(s):
	
	out = ""
	for i in s:
		out += `ord(i)` + ","
	return out
		
def oldDump(s):

	out = ""
	for i in s:
		if i=='\n':
			out += "[" ; out += "n" ; out += "]"
		if i=='\t':
			out += "[" ; out += "t" ; out += "]"
		elif i==' ':
			out += "[" ; out += " " ; out += "]"
		else: out += i
	return out
#@-body
#@-node:1::dump
#@+node:2:C=6:get_line & get_line_after
#@+body
# Very useful for tracing.

def get_line (s,i):

	nl = ""
	if is_nl(s,i):
		i = skip_nl(s,i)
		nl = "[nl]"
	j = find_line_start(s,i)
	k = skip_to_end_of_line(s,i)
	return nl + s[j:k]
	
def get_line_after (s,i):
	
	nl = ""
	if is_nl(s,i):
		i = skip_nl(s,i)
		nl = "[nl]"
	k = skip_to_end_of_line(s,i)
	return nl + s[i:k]

#@-body
#@-node:2:C=6:get_line & get_line_after
#@+node:3::printBindings
#@+body
def print_bindings (name,window):

	bindings = window.bind()
	print
	print "Bindings for", name
	for b in bindings:
		print `b`
#@-body
#@-node:3::printBindings
#@+node:4:C=7:Sherlock...
#@+body
#@+at
#  Starting with this release, you will see trace statements throughout the code.  The trace function is defined in leoUtils.py; 
# trace implements much of the functionality of my Sherlock tracing package.  Traces are more convenient than print statements for 
# two reasons: 1) you don't need explicit trace names and 2) you can disable them without recompiling.
# 
# In the following examples, suppose that the call to trace appears in function f.
# 
# trace(string) prints string if tracing for f has been enabled.  For example, the following statment prints from s[i] to the end 
# of the line if tracing for f has been enabled.
# 
# 	j = skip_line(s,i) ; trace(s[i:j])
# 
# trace(function) exectutes the function if tracing for f has been enabled.  For example,
# 
# 	trace(self.f2)
# 
# You enable and disable tracing by calling init_trace(args).  Examples:
# 
# 	init_trace("+*")         # enable all traces
# 	init_trace("+a","+b")    # enable traces for a and b
# 	init_trace(("+a","+b"))  # enable traces for a and b
# 	init_trace("-a")         # disable tracing for a
# 	traces = init_trace("?") # return the list of enabled traces
# 
# If two arguments are supplied to trace, the first argument is the "tracepoint name" and the second argument is the "tracepoint 
# action" as shown in the examples above.  If tracing for the tracepoint name is enabled, the tracepoint action is printed (if it 
# is a string) or exectuted (if it is a function name).
# 
# "*" will not match an explicit tracepoint name that starts with a minus sign.  For example,
# 
# 	trace("-nocolor", self.disable_color)

#@-at
#@-body
#@+node:1::get_Sherlock_args
#@+body
#@+at
#  It no args are given we attempt to get them from the "SherlockArgs" file.  If there are still no arguments we trace 
# everything.  This default makes tracing much more useful in Python.

#@-at
#@@c

def get_Sherlock_args (args):

	if not args or len(args)==0:
		try:
			f = open(os.path.join(app().loadDir,"SherlockArgs"))
			args = f.readlines()
			f.close()
		except: pass
	elif type(args[0]) == type(("1","2")):
		args = args[0] # strip away the outer tuple.

	# No args means trace everything.
	if not args or len(args)==0: args = ["+*"] 
	# print "get_Sherlock_args:" + `args`
	return args
#@-body
#@-node:1::get_Sherlock_args
#@+node:2::init_trace
#@+body
def init_trace(args):

	t = app().trace_list
	args = get_Sherlock_args(args)

	for arg in args:
		if arg[0] in string.letters: prefix = '+'
		else: prefix = arg[0] ; arg = arg[1:]
		
		if prefix == '?':
			print "trace list:", `t`
		elif prefix == '+' and not arg in t:
			t.append(string.lower(arg))
			# print "enabling:", arg
		elif prefix == '-' and arg in t:
			t.remove(string.lower(arg))
			# print "disabling:", arg
		else:
			print "ignoring:", prefix + arg
#@-body
#@-node:2::init_trace
#@+node:3::trace
#@+body
def trace (s1=None,s2=None):

	if s1 and s2:
		name = s1 ; message = s2
	else: # use the funtion name as the tracepoint name.
		message = s1 # may be None
		try: # get the function name from the call stack.
			f1 = sys._getframe(1) # The stack frame, one level up.
			code1 = f1.f_code # The code object
			name = code1.co_name # The code name
		except: name = ""
		
	t = app().trace_list
	# tracepoint names starting with '-' must match exactly.
	minus = len(name) > 0 and name[0] == '-'
	if minus: name = name[1:]
	if (not minus and '*' in t) or string.lower(name) in t:
		if not message: message = ""
		if type(message) == type("a"):
			s = name + ": " + message
			if 1: print s
			else: es(s)
		else: # assume we have a method and try to execute it.
			# print `type(message)`
			message()
#@-body
#@-node:3::trace
#@-node:4:C=7:Sherlock...
#@-node:6::Dumping, Tracing & Sherlock
#@+node:7::ensure_extension
#@+body
def ensure_extension (name, ext):

	file, old_ext = os.path.splitext(name)
	if len(name) == 0:
		return name # don't add to an empty name.
	elif old_ext and old_ext == ext:
		return name
	else:
		return file + ext
#@-body
#@-node:7::ensure_extension
#@+node:8:C=8:findReference
#@+body
#@+at
#  We search the descendents of v looking for the definition node matching name.
# There should be exactly one such node (descendents of other definition nodes are not searched).

#@-at
#@@c

def findReference(name,root):

	after = root.nodeAfterTree()
	v = root.firstChild()
	while v and v != after:
		if v.matchHeadline(name) and not v.isAtIgnoreNode():
			return v
		v = v.threadNext()
	return None

#@-body
#@-node:8:C=8:findReference
#@+node:9:C=9:Leading & trailing whitespace...
#@+node:1::computeLeadingWhitespace
#@+body
# Returns optimized whitespace corresponding to width with the indicated tab_width.

def computeLeadingWhitespace (width, tab_width):

	if width <= 0:
		return ""
	if tab_width > 1:
		tabs   = width / tab_width
		blanks = width % tab_width
		return ('\t' * tabs) + (' ' * blanks)
	else: # 7/3/02: negative tab width always gets converted to blanks.
		return (' ' * width)
#@-body
#@-node:1::computeLeadingWhitespace
#@+node:2::computeWidth
#@+body
# Returns the width of s, assuming s starts a line, with indicated tab_width.

def computeWidth (s, tab_width):
		
	w = 0
	for ch in s:
		if ch == '\t':
			w += (abs(tab_width) - (w % abs(tab_width)))
		else:
			w += 1
	return w
#@-body
#@-node:2::computeWidth
#@+node:3::optimizeLeadingWhitespace
#@+body
# Optimize leading whitespace in s with the given tab_width.

def optimizeLeadingWhitespace (line,tab_width):

	i, width = skip_leading_ws_with_indent(line,0,tab_width)
	s = computeLeadingWhitespace(width,tab_width) + line[i:]
	return s
#@-body
#@-node:3::optimizeLeadingWhitespace
#@+node:4::removeLeadingWhitespace
#@+body
# Remove whitespace up to first_ws wide in s, given tab_width, the width of a tab.

def removeLeadingWhitespace (s,first_ws,tab_width):

	j = 0 ; ws = 0
	for ch in s:
		if ws >= first_ws:
			break
		elif ch == ' ':
			j += 1 ; ws += 1
		elif ch == '\t':
			j += 1 ; ws += (abs(tab_width) - (ws % abs(tab_width)))
		else: break
	if j > 0:
		s = s[j:]
	return s
#@-body
#@-node:4::removeLeadingWhitespace
#@+node:5::removeTrailingWs
#@+body
# Warning: string.rstrip also removes newlines!

def removeTrailingWs(s):

	j = len(s)-1
	while j >= 0 and (s[j] == ' ' or s[j] == '\t'):
		j -= 1
	return s[:j+1]

#@-body
#@-node:5::removeTrailingWs
#@+node:6::skip_leading_ws
#@+body
# Skips leading up to width leading whitespace.

def skip_leading_ws(s,i,ws,tab_width):

	count = 0
	while count < ws and i < len(s):
		ch = s[i]
		if ch == ' ':
			count += 1
			i += 1
		elif ch == '\t':
			count += (abs(tab_width) - (count % abs(tab_width)))
			i += 1
		else: break

	return i
#@-body
#@-node:6::skip_leading_ws
#@+node:7::skip_leading_ws_with_indent
#@+body
#@+at
#  Skips leading whitespace and returns (i, indent), where i points after the whitespace and indent is the width of the 
# whitespace, assuming tab_width wide tabs.

#@-at
#@@c

def skip_leading_ws_with_indent(s,i,tab_width):

	count = 0 ; n = len(s)
	while i < n:
		ch = s[i]
		if ch == ' ':
			count += 1
			i += 1
		elif ch == '\t':
			count += (abs(tab_width) - (count % abs(tab_width)))
			i += 1
		else: break

	return i, count
#@-body
#@-node:7::skip_leading_ws_with_indent
#@-node:9:C=9:Leading & trailing whitespace...
#@+node:10::List utilities...
#@+node:1::appendToList
#@+body
def appendToList(out, s):

	for i in s:
		out.append(i)
#@-body
#@-node:1::appendToList
#@+node:2::flattenList
#@+body
def flattenList (theList):

	result = []
	for item in theList:
		if type(item) == types.ListType:
			result.extend(flattenList(item))
		else:
			result.append(item)
	return result
#@-body
#@-node:2::flattenList
#@+node:3::listToString
#@+body
def listToString(theList):

	if list:
		theList = flattenList(theList)
		return string.join(theList,"")
	else:
		return ""
#@-body
#@-node:3::listToString
#@-node:10::List utilities...
#@+node:11::Menu utlities...
#@+node:1::enableMenu & disableMenu & setMenuLabel
#@+body
def enableMenu (menu,name,val):

	state = choose(val,"normal","disabled")
	menu.entryconfig(name,state=state)

def disableMenu (menu,name):

	menu.entryconfig(name,state="disabled")

def setMenuLabel (menu,name,label):

	menu.entryconfig(name,label=label)
#@-body
#@-node:1::enableMenu & disableMenu & setMenuLabel
#@-node:11::Menu utlities...
#@+node:12::scanError
#@+body
#@+at
#  It seems dubious to bump the Tangle error count here.  OTOH, it really doesn't hurt.

#@-at
#@@c

def scanError(s):

	# Bump the error count in the tangle command.
	import leo
	c = leo.topCommands()
	c.tangleCommands.errors += 1

	es(s)
#@-body
#@-node:12::scanError
#@+node:13::Scanners: calling scanError
#@+body
#@+at
#  These scanners all call scanError() directly or indirectly, so they will call es() if they find an error.  scanError() also 
# bumps commands.tangleCommands.errors, which is harmless if we aren't tangling, and useful if we are.
# 
# These routines are called by the Import routines and the Tangle routines.

#@-at
#@-body
#@+node:1::skip_block_comment
#@+body
# Scans past a block comment (an old_style C comment).

def skip_block_comment (s,i):

	assert(match(s,i,"/*"))
	j = i ; i += 2 ; n = len(s)
	
	k = string.find(s,"*/",i)
	if k == -1:
		scanError("Run on block comment: " + s[j:i])
		return n
	else: return k + 2
#@-body
#@-node:1::skip_block_comment
#@+node:2::skip_braces
#@+body
# Skips from the opening to the matching . If no matching is found i is set to len(s).

def skip_braces(s,i):

	assert(match(s,i,'{'))
	level = 0 ; n = len(s)
	while i < n:
		c = s[i]
		if c == '{':
			level += 1 ; i += 1
		elif c == '}':
			level -= 1
			if level <= 0: return i
			i += 1
		elif c == '\'' or c == '"': i = skip_string(s,i)
		elif match(s,i,'//'): i = skip_to_end_of_line(s,i)
		elif match(s,i,'/*'): i = skip_block_comment(s,i)
		else: i += 1
	return i
#@-body
#@-node:2::skip_braces
#@+node:3::skip_parens
#@+body
#@+at
#  Skips from the opening ( to the matching ) . If no matching is found i is set to len(s)

#@-at
#@@c

def skip_parens(s,i):
	level = 0 ; n = len(s)
	assert(match(s,i,'('))
	while i < n:
		c = s[i]
		if c == '(':
			level += 1 ; i += 1
		elif c == ')':
			level -= 1
			if level <= 0:  return i
			i += 1
		elif c == '\'' or c == '"': i = skip_string(s,i)
		elif match(s,i,"//"): i = skip_to_end_of_line(s,i)
		elif match(s,i,"/*"): i = skip_block_comment(s,i)
		else: i += 1
	return i
#@-body
#@-node:3::skip_parens
#@+node:4::skip_pascal_begin_end
#@+body
#@+at
#  Skips from begin to matching end.
# If found, i points to the end. Otherwise, i >= len(s)
# The end keyword matches begin, case, class, record, and try.

#@-at
#@@c

def skip_pascal_begin_end(s,i):

	assert(match_c_word(s,i,"begin"))
	i1 = i # for traces
	level = 1 ; i = skip_c_id(s,i) # Skip the opening begin.
	while i < len(s):
		ch = s[i]
		if ch =='{' : i = skip_pascal_braces(s,i)
		elif ch =='"' or ch == '\'': i = skip_pascal_string(s,i)
		elif match(s,i,"//"): i = skip_line(s,i)
		elif match(s,i,"(*"): i = skip_pascal_block_comment(s,i)
		elif match_c_word(s,i,"end"):
			level -= 1 ;
			if level == 0:
				# lines = s[i1:i+3] ; trace('\n' + lines + '\n')
				return i
			else: i = skip_c_id(s,i)
		elif is_c_id(ch):
			j = i ; i = skip_c_id(s,i) ; name = s[j:i]
			if name in ["begin", "case", "class", "record", "try"]:
				level += 1
		else: i += 1
	# trace(`s[i1:i]`)
	return i
#@-body
#@-node:4::skip_pascal_begin_end
#@+node:5::skip_pascal_block_comment
#@+body
# Scans past a pascal comment delimited by (* and *).

def skip_pascal_block_comment(s,i):
	
	j = i
	assert(match(s,i,"(*"))
	i = string.find(s,"*)",i)
	if i > -1: return i + 2
	else:
		scanError("Run on comment" + s[j:i])
		return len(s)

#	n = len(s)
#	while i < n:
#		if match(s,i,"*)"): return i + 2
#		i += 1
#	scanError("Run on comment" + s[j:i])
#	return i
#@-body
#@-node:5::skip_pascal_block_comment
#@+node:6::skip_pascal_string : called by tangle
#@+body
def skip_pascal_string(s,i):

	j = i ; delim = s[i] ; i += 1
	assert(delim == '"' or delim == '\'')

	while i < len(s):
		if s[i] == delim:
			return i + 1
		else: i += 1

	scanError("Run on string: " + s[j:i])
	return i
#@-body
#@-node:6::skip_pascal_string : called by tangle
#@+node:7::skip_pp_directive
#@+body
# Now handles continuation lines and block comments.

def skip_pp_directive(s,i):

	while i < len(s):
		if is_nl(s,i):
			if escaped(s,i): i = skip_nl(s,i)
			else: break
		elif match(s,i,"//"): i = skip_to_end_of_line(s,i)
		elif match(s,i,"/*"): i = skip_block_comment(s,i)
		else: i += 1
	return i
#@-body
#@-node:7::skip_pp_directive
#@+node:8::skip_pp_if
#@+body
# Skips an entire if or if def statement, including any nested statements.

def skip_pp_if(s,i):

	assert(match(s,i,'#'))
	if ( not match_word(s,i,"#if") and
		not match_word(s,i,"ifdef") and
		not match_word(s,i,"#ifndef") ): return skip_to_end_of_line(s,i)

	level = 0
	while i < len(s):
		c = s[i]
		if match_word(s,i,"#if") or match_word(s,i,"ifdef") or match_word(s,i,"#ifndef"):
			level += 1 ; i = skip_to_end_of_line(s,i)
		elif match_word(s,i,"#endif"):
			level -= 1 ; i = skip_to_end_of_line(s,i)
			if level <= 0: return i
		elif c == '\'' or c == '"': i = skip_string(s,i)
		elif match(s,i,"//"): i = skip_to_end_of_line(s,i)
		elif match(s,i,"/*"): i = skip_block_comment(s,i)
		else: i += 1
	return i
#@-body
#@-node:8::skip_pp_if
#@+node:9::skip_to_semicolon
#@+body
# Skips to the next semicolon that is not in a comment or a string.

def skip_to_semicolon(s,i):

	n = len(s)
	while i < n:
		c = s[i]
		if c == ';': return i
		elif c == '\'' or c == '"' : i = skip_string(s,i)
		elif match(s,i,"//"): i = skip_to_end_of_line(s,i)
		elif match(s,i,"/*"): i = skip_block_comment(s,i)
		else: i += 1
	return i
#@-body
#@-node:9::skip_to_semicolon
#@+node:10::skip_python_string
#@+body
def skip_python_string(s,i):

	if match(s,i,"'''") or match(s,i,'"""'):
		j = i ; delim = s[i]*3 ; i += 3
		k = string.find(s,delim,i)
		if k > -1: return k+3
		scanError("Run on triple quoted string: " + s[j:i])
		return len(s)
	else:
		return skip_string(s,i)
#@-body
#@-node:10::skip_python_string
#@+node:11::skip_string : called by tangle
#@+body
def skip_string(s,i):
	
	j = i ; delim = s[i] ; i += 1
	assert(delim == '"' or delim == '\'')
	n = len(s)
	while i < n and s[i] != delim:
		if s[i] == '\\' : i += 2
		else: i += 1

	if i >= n:
		scanError("Run on string: " + s[j:i])
	elif s[i] == delim:
		i += 1
	return i
#@-body
#@-node:11::skip_string : called by tangle
#@+node:12::skip_typedef
#@+body
def skip_typedef(s,i):

	n = len(s)
	while i < n and is_c_id(s[i]):
		i = skip_c_id(s,i)
		i = skip_ws_and_nl(s,i)
	if match(s,i,'{'):
		i = skip_braces(s,i)
		i = skip_to_semicolon(s,i)
	return i
#@-body
#@-node:12::skip_typedef
#@-node:13::Scanners: calling scanError
#@+node:14::Scanners: no error messages
#@+node:1::escaped
#@+body
# Returns true if s[i] is preceded by an odd number of backslashes.

def escaped(s,i):

	count = 0
	while i-1 >= 0 and s[i-1] == '\\':
		count += 1
		i -= 1
	return (count%2) == 1
#@-body
#@-node:1::escaped
#@+node:2:C=10:find_line_start
#@+body
def find_line_start(s,i):

	i = string.rfind(s,'\n',0,i) # Finds the highest index in the range.
	if i == -1: return 0
	else: return i + 1
#@-body
#@-node:2:C=10:find_line_start
#@+node:3::find_on_line
#@+body
def find_on_line(s,i,pattern):

	# j = skip_line(s,i) ; trace(`s[i:j]`)
	j = string.find(s,'\n',i)
	if j == -1: j = len(s)
	k = string.find(s,pattern,i,j)
	if k > -1: return k
	else: return None
#@-body
#@-node:3::find_on_line
#@+node:4::is_c_id
#@+body
def is_c_id(ch):

	return ch in string.letters or ch in string.digits or ch == '_'
#@-body
#@-node:4::is_c_id
#@+node:5::is_nl
#@+body
def is_nl(s,i):

	return i < len(s) and (s[i] == '\n' or s[i] == '\r')
#@-body
#@-node:5::is_nl
#@+node:6::is_special
#@+body
#@+at
#  Return true if the body text contains the @ directive.
# 
# We no longer require that the directive appear befor e any @c directive or section definition.

#@-at
#@@c

def is_special(s,i,directive):

	# j = skip_line(s,i) ; trace(`s[i:j]` + " : " + `directive`)
	assert (directive and directive [0] == '@' )
	while i < len(s):
		i = skip_ws_and_nl(s,i)
		if match_word(s,i,directive):
			return true, i
		else:
			i = skip_line(s,i)
	return false, -1
#@-body
#@-node:6::is_special
#@+node:7:C=11:is_special_bits
#@+body
#@+at
#  Returns bits, dict where:
# bits is a bit-set representing all the @directives of a particular body text.
# dict contains various pointers into the text.
# 
# The caller passes [root_node] or None as the second arg.  This allows us to distinguish between None and [None].

#@-at
#@@c

def is_special_bits(s,root=None):

	if root: root_node = root[0]
	bits = 0 ; dict = {}
	i = 0 ; n = len(s)
	while i < n:
		if s[i] == '@' and i+1 < n:
			
			#@<< set bits for @ directives >>
			#@+node:1::<< set bits for @ directives >>
			#@+body
			ch = s[i+1]
			if ch == 'c':
				if   match_word(s,i,"@color"): bits |= color_bits
				elif match_word(s,i,"@comment"):
					bits |= comment_bits ; dict["comment"] = i
			elif ch == 'h':
				if match_word(s,i,"@header"): bits |= header_bits
			elif ch == 'i':
				if match_word(s,i,"@ignore"): bits |= ignore_bits
			elif ch == 'l':
				if match_word(s,i,"@language"):
					# trace(`s[i:]`)
					bits |= language_bits ; dict ["language"] = i
			elif ch == 'n':
				if   match_word(s,i,"@nocolor"):  bits |= nocolor_bits
				elif match_word(s,i,"@noheader"): bits |= noheader_bits
			elif ch == 'p':
				if   match_word(s,i,"@pagewidth"):
					bits |= page_width_bits ; dict["page_width"] = i
				elif match_word(s,i,"@path"):
					bits |= path_bits ; dict["path"] = i
			elif ch == 'r':
				if match_word(s,i,"@root"): bits |= root_bits # skip_body finds the root.
			elif ch == 's':
				if match_word(s,i,"@silent"): bits |= silent_bits
			elif ch == 't':
				if   match_word(s,i,"@tabwidth"):
					bits |= tab_width_bits ; dict["tab_width"] = i
				elif match_word(s,i,"@terse"):
					bits |= terse_bits
			elif ch == 'u':
				if match_word(s,i,"@unit"): bits |= unit_bits
			elif ch == 'v':
				if match_word(s,i,"@verbose"): bits |= verbose_bits
			#@-body
			#@-node:1::<< set bits for @ directives >>

		elif root and match(s,i,"<<"):
			
			#@<< set root bits for noweb * chunks >>
			#@+node:2::<< set root bits for noweb * chunks >>
			#@+body
			#@+at
			#  The following looks for chunk definitions of the form < < * > > =. If found, we take this to be equivalent to @root 
			# filename if the headline has the form @root filename.

			#@-at
			#@@c
			
			i = skip_ws(s,i+2)
			if i < n and s[i] == '*' :
				i = skip_ws(s,i+1) # Skip the '*'
				if match(s,i,">>="):
					# < < * > > = implies that @root should appear in the headline.
					i += 3
					if root_node:
						bits |= root_bits
					else:
						es("<<" +
							"*>>= requires @root in the headline")
			#@-body
			#@-node:2::<< set root bits for noweb * chunks >>

		i = skip_line(s,i)
	return bits, dict
#@-body
#@-node:7:C=11:is_special_bits
#@+node:8::is_ws & is_ws_or_nl
#@+body
def is_ws(c):

	return c == '\t' or c == ' '
	
def is_ws_or_nl(s,i):

	return is_nl(s,i) or (i < len(s) and is_ws(s[i]))
#@-body
#@-node:8::is_ws & is_ws_or_nl
#@+node:9::match
#@+body
# Warning: this code makes no assumptions about what follows pattern.

def match(s,i,pattern):

	return s and pattern and string.find(s,pattern,i,i+len(pattern)) == i
#@-body
#@-node:9::match
#@+node:10::match_c_word
#@+body
def match_c_word (s,i,name):

	n = len(name)
	return name == s[i:i+n] and (i+n == len(s) or not is_c_id(s[i+n]))
#@-body
#@-node:10::match_c_word
#@+node:11::match_ignoring_case
#@+body
def match_ignoring_case(s1,s2):

	return string.lower(s1) == string.lower(s2)
#@-body
#@-node:11::match_ignoring_case
#@+node:12::match_word
#@+body
def match_word(s,i,pattern):

	j = len(pattern)
	if string.find(s,pattern,i,i+j) != i:
		return false
	if i+j >= len(s):
		return true
	c = s[i+j]
	return not (c in string.letters or c in string.digits or c == '_')
#@-body
#@-node:12::match_word
#@+node:13::skip_blank_lines
#@+body
def skip_blank_lines(s,i):

	while i < len(s):
		if is_nl(s,i) :
			i = skip_nl(s,i)
		elif is_ws(s[i]):
			j = skip_ws(s,i)
			if is_nl(s,j):
				i = j
			else: break
		else: break
	return i
#@-body
#@-node:13::skip_blank_lines
#@+node:14::skip_c_id
#@+body
def skip_c_id(s,i):

	n = len(s)
	while i < n:
		c = s[i]
		if c in string.letters or c in string.digits or c == '_':
			i += 1
		else: break
	return i
#@-body
#@-node:14::skip_c_id
#@+node:15::skip_line, skip_to_end_of_line
#@+body
#@+at
#  These methods skip to the next newline, regardless of whether the newline may be preceeded by a backslash. Consequently, they 
# should be used only when we know that we are not in a preprocessor directive or string.

#@-at
#@@c

def skip_line (s,i):

	i = string.find(s,'\n',i)
	if i == -1: return len(s)
	else: return i + 1
		
def skip_to_end_of_line (s,i):

	i = string.find(s,'\n',i)
	if i == -1: return len(s)
	else: return i
#@-body
#@-node:15::skip_line, skip_to_end_of_line
#@+node:16::skip_long
#@+body
# returns (i, val) or (i, None) if s[i] does not point at a number.

def skip_long(s,i):

	val = 0
	i = skip_ws(s,i)
	n = len(s)
	if i >= n or s[i] not in string.digits:
		return i, None
	# Rewritten: 7/18/02.
	j = i
	while i < n and s[i] in string.digits:
		i += 1
	val = int(s[j:i])
	return i, val
#@-body
#@-node:16::skip_long
#@+node:17::skip_matching_delims
#@+body
def skip_matching_delims(s,i,delim1,delim2):
	
	assert(match(s,i,delim1))

	i += len(delim1)
	k = string.find(s,delim2,i)
	if k == -1:
		return len(s)
	else:
		return k + len(delim2)
#@-body
#@-node:17::skip_matching_delims
#@+node:18::skip_nl
#@+body
#@+at
#  This function skips a single "logical" end-of-line character.  We need this function because different systems have different 
# end-of-line conventions.

#@-at
#@@c

def skip_nl (s,i):

	if match(s,i,"\r\n"): return i + 2
	elif match(s,i,'\n') or match(s,i,'\r'): return i + 1
	else: return i
#@-body
#@-node:18::skip_nl
#@+node:19::skip_pascal_braces
#@+body
# Skips from the opening { to the matching }.

def skip_pascal_braces(s,i):

	# No constructs are recognized inside Pascal block comments!
	k = string.find(s,'}',i)
	if i == -1: return len(s)
	else: return k
#@-body
#@-node:19::skip_pascal_braces
#@+node:20::skip_ws, skip_ws_and_nl
#@+body
def skip_ws(s,i):

	n = len(s)
	while i < n and is_ws(s[i]):
		i += 1
	return i
	
def skip_ws_and_nl(s,i):

	n = len(s)
	while i < n and (is_ws(s[i]) or is_nl(s,i)):
		i += 1
	return i
#@-body
#@-node:20::skip_ws, skip_ws_and_nl
#@-node:14::Scanners: no error messages
#@+node:15::shortFileName
#@+body
def shortFileName (fileName):
	
	if 0: # I don't like the conversion to lower case
		fileName = os.path.normpath(fileName)
	head,tail = os.path.split(fileName)
	return tail
#@-body
#@-node:15::shortFileName
#@+node:16::sortSequence
#@+body
#@+at
#  sequence is a sequence of items, each of which is a sequence containing at least n elements.
# returns a list of the the items sorted on the n'th element of each tuple.

#@-at
#@@c

def sortSequence (sequence, n):

	keys = [] ; links = {}
	for item in sequence:
		key = item[n]
		links[key] = item
		keys.append(key)
	keys.sort() ; sorted = []
	for key in keys:
		sorted.append(links[key])
	return sorted
	

#@+at
#  The sort() method takes an optional argument specifying a comparison function of two arguments (list items) which should return 
# -1, 0 or 1 depending on whether the first argument is considered smaller than, equal to, or larger than the second argument.
# 
# Note that this slows the sorting process down considerably; e.g. to sort a list in reverse order it is much faster to use calls 
# to the methods sort() and reverse() than to use the built-in function sort() with a comparison function that reverses the 
# ordering of the elements.
# 
# So a "clever" solution wouldn't be so clever after all.

#@-at
#@@c
#@-body
#@-node:16::sortSequence
#@+node:17::Timing
#@+body
#@+at
#  pychecker bug: pychecker complains that there is no attribute time.clock

#@-at
#@@c

def getTime():
	return time.clock()
	
def esDiffTime(message, start):
	es(message + ("%6.3f" % (time.clock()-start)))
	return time.clock()
#@-body
#@-node:17::Timing
#@+node:18:C=12:Tk.Text selection (utils)
#@+node:1::getTextSelection
#@+body
# t is a Tk.Text widget.  Returns the selected range of t.

def getTextSelection (t):

	# To get the current selection
	sel = t.tag_ranges("sel")
	if len(sel) == 2:
		start, end = sel # unpack tuple.
		return start, end
	else: return None, None
#@-body
#@-node:1::getTextSelection
#@+node:2::getSelectedText
#@+body
# t is a Tk.Text widget.  Returns the text of the selected range of t.

def getSelectedText (t):

	start, end = getTextSelection(t)
	if start and end:
		return t.get(start,end)
	else:
		return None
#@-body
#@-node:2::getSelectedText
#@+node:3:C=13:setTextSelection
#@+body
#@+at
#  t is a Tk.Text widget.  start and end are positions.  Selects from start to end.

#@-at
#@@c

def setTextSelection (t,start,end): 

	if not start or not end:
		return
	if t.compare(start, ">", end):
		start,end = end,start
		
	t.tag_remove("sel","1.0",start)
	t.tag_add("sel",start,end)
	t.tag_remove("sel",end,"end")
	t.mark_set("insert",end)
#@-body
#@-node:3:C=13:setTextSelection
#@-node:18:C=12:Tk.Text selection (utils)
#@+node:19::update_file_if_changed
#@+body
#@+at
#  This function compares two files. If they are different, we replace file_name with temp_name. Otherwise, we just delete 
# temp_name.  Both files should be closed.

#@-at
#@@c

def update_file_if_changed(file_name,temp_name):

	if os.path.exists(file_name):
		import filecmp
		if filecmp.cmp(temp_name, file_name):
			try: # Just delete the temp file.
				os.remove(temp_name)
			except: pass
			es("unchanged: " + file_name)
		else:
			try: # Replace file with temp file.
				os.remove(file_name)
				os.rename(temp_name, file_name)
				es("***updating: " + file_name)
			except:
				es("Rename failed: no file created! (file may be read-only)")
				traceback.print_exc()
	else:
		try:
			os.rename(temp_name, file_name)
			es("Creating: " + file_name)
		except:
			es("Rename failed: no file created! (file may be read-only)")
			traceback.print_exc()
#@-body
#@-node:19::update_file_if_changed
#@-others
#@-body
#@-node:0::@file leoUtils.py
#@-leo
