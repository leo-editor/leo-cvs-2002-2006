#@+leo
#@+node:0::@file leoUtils.py
#@+body
#@@language python

# Global utility functions

from leoGlobals import *
import os, string, sys, time, types, Tkinter, traceback


#@+others
#@+node:1::@language and @comment directives (leoUtils)
#@+node:1::set_delims_from_language
#@+body
# Returns a tuple (single,start,end) of comment delims

def set_delims_from_language(language):
	
	val = language_delims_dict.get(language)
	if val:
		delim1,delim2,delim3 = set_delims_from_string(val)
		if delim2 and not delim3:
			return None,delim1,delim2
		else: # 0,1 or 3 params.
			return delim1,delim2,delim3
	else:
		return None, None, None # Indicate that no change should be made

#@-body
#@-node:1::set_delims_from_language
#@+node:2::set_delims_from_string
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
		
	# 'rr 09/25/02
	if count == 2: # delims[0] is always the single-line delim.
		delims[2] = delims[1]
		delims[1] = delims[0]
		delims[0] = None

	# 7/8/02: The "REM hack": replace underscores by blanks.
	# 9/25/02: The "perlpod hack": replace double underscores by newlines.
	for i in xrange(0,3):
		if delims[i]:
			delims[i] = string.replace(delims[i],"__",'\n') 
			delims[i] = string.replace(delims[i],'_',' ')

	return delims[0], delims[1], delims[2]
#@-body
#@-node:2::set_delims_from_string
#@+node:3::set_language
#@+body
#@+at
#   Scans the @language directive that appears at s[i].
# 
# Returns (language, delim1, delim2, delim3)

#@-at
#@@c

def set_language(s,i,issue_errors_flag):

	tag = "@language"
	# trace(`get_line(s,i)`)
	assert(i != None)
	assert(match_word(s,i,tag))
	i += len(tag) ; i = skip_ws(s, i)
	# Get the argument.
	j = i ; i = skip_c_id(s,i)
	# Allow tcl/tk.
	arg = string.lower(s[j:i])
	if language_delims_dict.get(arg):
		language = arg
		delim1, delim2, delim3 = set_delims_from_language(language)
		return language, delim1, delim2, delim3
	
	if issue_errors_flag:
		es("ignoring: " + get_line(s,i))

	return None, None, None, None,
#@-body
#@-node:3::set_language
#@-node:1::@language and @comment directives (leoUtils)
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
#@+node:4::CheckVersion (Dave Hein)
#@+body
#@+at
# 
# CheckVersion() is a generic version checker.  Assumes a
# version string of up to four parts, or tokens, with
# leftmost token being most significant and each token
# becoming less signficant in sequence to the right.
# 
# RETURN VALUE
# 
# 1 if comparison is true
# 0 if comparison is false
# 
# PARAMETERS
# 
# version: the version string to be tested
# againstVersion: the reference version string to be
#                 compared against
# condition: can be any of "==", "!=", ">=", "<=", ">", or "<"
# stringCompare: whether to test a token using only the
#                leading integer of the token, or using the
# 			   entire token string.  For example, a value
# 			   of "0.0.1.0" means that we use the integer
# 			   value of the first, second, and fourth
# 			   tokens, but we use a string compare for the
# 			   third version token.
# delimiter: the character that separates the tokens in the
#            version strings.
# 
# The comparison uses the precision of the version string
# with the least number of tokens.  For example a test of
# "8.4" against "8.3.3" would just compare the first two
# tokens.
# 
# The version strings are limited to a maximum of 4 tokens.

#@-at
#@@c

def CheckVersion( version, againstVersion, condition=">=", stringCompare="0.0.0.0", delimiter='.' ):
	import sre  # Unicode-aware regular expressions
	#
	# tokenize the stringCompare flags
	compareFlag = string.split( stringCompare, '.' )
	#
	# tokenize the version strings
	testVersion = string.split( version, delimiter )
	testAgainst = string.split( againstVersion, delimiter )
	#
	# find the 'precision' of the comparison
	tokenCount = 4
	if tokenCount > len(testAgainst):
		tokenCount = len(testAgainst)
	if tokenCount > len(testVersion):
		tokenCount = len(testVersion)
	#
	# Apply the stringCompare flags
	justInteger = sre.compile("^[0-9]+")
	for i in range(tokenCount):
		if "0" == compareFlag[i]:
			m = justInteger.match( testVersion[i] )
			testVersion[i] = m.group()
			m = justInteger.match( testAgainst[i] )
			testAgainst[i] = m.group()
		elif "1" != compareFlag[i]:
			errMsg = "stringCompare argument must be of " +\
				 "the form \"x.x.x.x\" where each " +\
				 "'x' is either '0' or '1'."
			raise errMsg
	#
	# Compare the versions
	if condition == ">=":
		for i in range(tokenCount):
			if testVersion[i] < testAgainst[i]:
				return 0
			if testVersion[i] > testAgainst[i]:
				return 1 # it was greater than
		return 1 # it was equal
	if condition == ">":
		for i in range(tokenCount):
			if testVersion[i] < testAgainst[i]:
				return 0
			if testVersion[i] > testAgainst[i]:
				return 1 # it was greater than
		return 0 # it was equal
	if condition == "==":
		for i in range(tokenCount):
			if testVersion[i] != testAgainst[i]:
				return 0 # any token was not equal
		return 1 # every token was equal
	if condition == "!=":
		for i in range(tokenCount):
			if testVersion[i] != testAgainst[i]:
				return 1 # any token was not equal
		return 0 # every token was equal
	if condition == "<":
		for i in range(tokenCount):
			if testVersion[i] >= testAgainst[i]:
				return 0
			if testVersion[i] < testAgainst[i]:
				return 1 # it was less than
		return 0 # it was equal
	if condition == "<=":
		for i in range(tokenCount):
			if testVersion[i] > testAgainst[i]:
				return 0
			if testVersion[i] < testAgainst[i]:
				return 1 # it was less than
		return 1 # it was equal
	#
	# didn't find a condition that we expected.
	raise "condition must be one of '>=', '>', '==', '!=', '<', or '<='."

#@-body
#@-node:4::CheckVersion (Dave Hein)
#@+node:5::create_temp_name
#@+body
# Returns a temporary file name.

def create_temp_name ():

	import tempfile
	temp = tempfile.mktemp()
	# trace(`temp`)
	return temp
#@-body
#@-node:5::create_temp_name
#@+node:6::Dialog utilites...
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
#@+node:3::create_labeled_frame
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
	border.grid(row=1,column=1,rowspan=5,columnspan=5,sticky="news")
	
	# Create the content frame, f, in the center of the grid.
	f = Tk.Frame(w,bd=bd)
	f.grid(row=3,column=3,sticky="news")
	
	# Add the caption.
	if caption and len(caption) > 0:
		caption = Tk.Label(parent,text=caption,highlightthickness=0,bd=0)
		caption.tkraise(w)
		caption.grid(in_=w,row=0,column=2,rowspan=2,columnspan=3,padx=4,sticky="w")

	return w,f
#@-body
#@-node:3::create_labeled_frame
#@-node:6::Dialog utilites...
#@+node:7::Dumping, Tracing & Sherlock
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
#@+node:2::es_exception
#@+body
def es_exception ():

	typ,val,tb = sys.exc_info()
	errList = traceback.format_exception_only(typ,val)
	for i in errList:
		es(i)
	traceback.print_exc()
#@-body
#@-node:2::es_exception
#@+node:3::get_line & get_line_after
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
#@-node:3::get_line & get_line_after
#@+node:4::printBindings
#@+body
def print_bindings (name,window):

	bindings = window.bind()
	print
	print "Bindings for", name
	for b in bindings:
		print `b`
#@-body
#@-node:4::printBindings
#@+node:5::Sherlock...
#@+body
#@+at
#  Starting with this release, you will see trace statements throughout the 
# code.  The trace function is defined in leoUtils.py; trace implements much 
# of the functionality of my Sherlock tracing package.  Traces are more 
# convenient than print statements for two reasons: 1) you don't need explicit 
# trace names and 2) you can disable them without recompiling.
# 
# In the following examples, suppose that the call to trace appears in 
# function f.
# 
# trace(string) prints string if tracing for f has been enabled.  For example, 
# the following statment prints from s[i] to the end of the line if tracing 
# for f has been enabled.
# 
# 	j = skip_line(s,i) ; trace(s[i:j])
# 
# trace(function) exectutes the function if tracing for f has been enabled.  
# For example,
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
# If two arguments are supplied to trace, the first argument is the 
# "tracepoint name" and the second argument is the "tracepoint action" as 
# shown in the examples above.  If tracing for the tracepoint name is enabled, 
# the tracepoint action is printed (if it is a string) or exectuted (if it is 
# a function name).
# 
# "*" will not match an explicit tracepoint name that starts with a minus 
# sign.  For example,
# 
# 	trace("-nocolor", self.disable_color)

#@-at
#@-body
#@+node:1::get_Sherlock_args
#@+body
#@+at
#  It no args are given we attempt to get them from the "SherlockArgs" file.  
# If there are still no arguments we trace everything.  This default makes 
# tracing much more useful in Python.

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
#@-node:5::Sherlock...
#@-node:7::Dumping, Tracing & Sherlock
#@+node:8::ensure_extension
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
#@-node:8::ensure_extension
#@+node:9::findReference
#@+body
#@+at
#  We search the descendents of v looking for the definition node matching name.
# There should be exactly one such node (descendents of other definition nodes 
# are not searched).

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
#@-node:9::findReference
#@+node:10::get_directives_dict
#@+body
#@+at
#  Scans root for @directives and returns a dict containing pointers to the 
# start of each directive.
# 
# The caller passes [root_node] or None as the second arg.  This allows us to 
# distinguish between None and [None].

#@-at
#@@c

def get_directives_dict(s,root=None):

	if root: root_node = root[0]
	dict = {}
	i = 0 ; n = len(s)
	while i < n:
		if s[i] == '@' and i+1 < n:
			
			#@<< set dict for @ directives >>
			#@+node:1::<< set dict for @ directives >>
			#@+body
			# EKR: rewritten 10/10/02
			directiveList = (
				"color", "comment", "header", "ignore",
				"language", "nocolor", "noheader",
				"pagewidth", "path", "quiet", "root", "silent",
				"tabwidth", "terse", "unit", "verbose")
			
			j = skip_c_id(s,i+1)
			word = s[i+1:j]
			if word in directiveList:
				dict [word] = i
			
			#@-body
			#@-node:1::<< set dict for @ directives >>

		elif root and match(s,i,"<<"):
			
			#@<< set dict["root"] for noweb * chunks >>
			#@+node:2::<< set dict["root"] for noweb * chunks >>
			#@+body
			#@+at
			#  The following looks for chunk definitions of the form < < * > > 
			# =. If found, we take this to be equivalent to @root filename if 
			# the headline has the form @root filename.

			#@-at
			#@@c

			i = skip_ws(s,i+2)
			if i < n and s[i] == '*' :
				i = skip_ws(s,i+1) # Skip the '*'
				if match(s,i,">>="):
					# < < * > > = implies that @root should appear in the headline.
					i += 3
					if root_node:
						dict["root"]=0 # value not immportant
					else:
						es(angleBrackets("*") + "= requires @root in the headline")
			#@-body
			#@-node:2::<< set dict["root"] for noweb * chunks >>

		i = skip_line(s,i)
	return dict
#@-body
#@-node:10::get_directives_dict
#@+node:11::getBaseDirectory
#@+body
# Handles the conventions applying to the "relative_path_base_directory" configuration option.

def getBaseDirectory():

	base = app().config.relative_path_base_directory

	if base and base == "!":
		base = app().loadDir
	elif base and base == ".":
		base = top().openDirectory

	# trace(`base`)
	if base and len(base) > 0 and os.path.isabs(base):
		return base # base need not exist yet.
	else:
		return "" # An error.
#@-body
#@-node:11::getBaseDirectory
#@+node:12::getUserNewline
#@+body
def getOutputNewline ():
	
	s = app().config.output_newline
	s = string.lower(s)
	if s == "nl" or s == "lf": s = '\n'
	elif s == "cr": s = '\r'
	elif s == "crlf": s = "\r\n"
	else: s = '\n'
	return s

#@-body
#@-node:12::getUserNewline
#@+node:13::Leading & trailing whitespace...
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
#  Skips leading whitespace and returns (i, indent), where i points after the 
# whitespace and indent is the width of the whitespace, assuming tab_width 
# wide tabs.

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
#@-node:13::Leading & trailing whitespace...
#@+node:14::List utilities...
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
#@-node:14::List utilities...
#@+node:15::Menu utlities...
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
#@-node:15::Menu utlities...
#@+node:16::readlineForceUnixNewline (Steven P. Schaefer)
#@+body
#@+at
#  Stephen P. Schaefer 9/7/2002
# 
# The Unix readline() routine delivers "\r\n" line end strings verbatim, while 
# the windows versions force the string to use the Unix convention of using 
# only "\n".  This routine causes the Unix readline to do the same.

#@-at
#@@c

def readlineForceUnixNewline(f):

	s = f.readline()
	if len(s) >= 2 and s[-2] == "\r" and s[-1] == "\n":
		s = s[0:-2] + "\n"
	return s

#@-body
#@-node:16::readlineForceUnixNewline (Steven P. Schaefer)
#@+node:17::scanError
#@+body
#@+at
#  It seems dubious to bump the Tangle error count here.  OTOH, it really 
# doesn't hurt.

#@-at
#@@c

def scanError(s):

	# Bump the error count in the tangle command.
	import leo
	c = leo.topCommands()
	c.tangleCommands.errors += 1

	es(s)
#@-body
#@-node:17::scanError
#@+node:18::Scanners: calling scanError
#@+body
#@+at
#  These scanners all call scanError() directly or indirectly, so they will 
# call es() if they find an error.  scanError() also bumps 
# commands.tangleCommands.errors, which is harmless if we aren't tangling, and 
# useful if we are.
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
#@+at
#  Skips from the opening to the matching . If no matching is found i is set 
# to len(s).
# 
# This code is called only from the import logic, so we are allowed to try 
# some tricks.  In particular, we assume all braces are matched in #if blocks.

#@-at
#@@c

def skip_braces(s,i):

	start = get_line(s,i)
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
		# 7/29/02: be more careful handling conditional code.
		elif match_word(s,i,"#if") or match_word(s,i,"#ifdef") or match_word(s,i,"#ifndef"):
			i,delta = skip_pp_if(s,i)
			level += delta
		else: i += 1
	return i
#@-body
#@-node:2::skip_braces
#@+node:3::skip_php_braces (Dave Hein)
#@+body
#@+at
#  08-SEP-2002 DTHEIN: Added for PHP import support
# Skips from the opening to the matching . If no matching is found i is set to len(s).
# 
# This code is called only from the import logic, and only for PHP imports.

#@-at
#@@c

def skip_php_braces(s,i):

	start = get_line(s,i)
	assert(match(s,i,'{'))
	level = 0 ; n = len(s)
	while i < n:
		c = s[i]
		if c == '{':
			level += 1 ; i += 1
		elif c == '}':
			level -= 1
			if level <= 0: return i + 1
			i += 1
		elif c == '\'' or c == '"': i = skip_string(s,i)
		elif match(s,i,"<<<"): i = skip_heredoc_string(s,i)
		elif match(s,i,'//') or match(s,i,'#'): i = skip_to_end_of_line(s,i)
		elif match(s,i,'/*'): i = skip_block_comment(s,i)
		else: i += 1
	return i

#@-body
#@-node:3::skip_php_braces (Dave Hein)
#@+node:4::skip_parens
#@+body
#@+at
#  Skips from the opening ( to the matching ) . If no matching is found i is 
# set to len(s)

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
#@-node:4::skip_parens
#@+node:5::skip_pascal_begin_end
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
#@-node:5::skip_pascal_begin_end
#@+node:6::skip_pascal_block_comment
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
#@-node:6::skip_pascal_block_comment
#@+node:7::skip_pascal_string : called by tangle
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
#@-node:7::skip_pascal_string : called by tangle
#@+node:8::skip_heredoc_string : called by php import (Dave Hein)
#@+body
#@+at
#  08-SEP-2002 DTHEIN:  added function skip_heredoc_string
# A heredoc string in PHP looks like:
# 
# 	<<<EOS
# 	This is my string.
# 	It is mine. I own it.
# 	No one else has it.
# 	EOS
# 
# It begins with <<< plus a token (naming same as PHP variable names).
# It ends with the token on a line by itself (must start in first position.
# 

#@-at
#@@c
def skip_heredoc_string(s,i):
	
	import re
	
	j = i
	assert(match(s,i,"<<<"))
	m = re.match("\<\<\<([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)", s[i:])
	if (None == m):
		i += 3
		return i

	# 14-SEP-2002 DTHEIN: needed to add \n to find word, not just string
	delim = m.group(1) + '\n' 
	
	i = skip_line(s,i) # 14-SEP-2002 DTHEIN: look after \n, not before
	n = len(s)
	while i < n and not match(s,i,delim):
		i = skip_line(s,i) # 14-SEP-2002 DTHEIN: move past \n
		
	if i >= n:
		scanError("Run on string: " + s[j:i])
	elif match(s,i,delim):
		i += len(delim)
	return i

#@-body
#@-node:8::skip_heredoc_string : called by php import (Dave Hein)
#@+node:9::skip_pp_directive
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
#@-node:9::skip_pp_directive
#@+node:10::skip_pp_if
#@+body
# Skips an entire if or if def statement, including any nested statements.

def skip_pp_if(s,i):
	
	start_line = get_line(s,i) # used for error messages.
	# trace(start_line)

	assert(
		match_word(s,i,"#if") or
		match_word(s,i,"#ifdef") or
		match_word(s,i,"#ifndef"))

	i = skip_line(s,i)
	i,delta1 = skip_pp_part(s,i)
	i = skip_ws(s,i)
	if match_word(s,i,"#else"):
		i = skip_line(s,i)
		i = skip_ws(s,i)
		i,delta2 = skip_pp_part(s,i)
		if delta1 != delta2:
			es("#if and #else parts have different braces: " + start_line)
	i = skip_ws(s,i)
	if match_word(s,i,"#endif"):
		i = skip_line(s,i)
	else:
		es("no matching #endif: " + start_line)
		
	# trace(`delta1` + ":" + start_line)
	return i,delta1

#@-body
#@-node:10::skip_pp_if
#@+node:11::skip_pp_part
#@+body
# Skip to an #else or #endif.  The caller has eaten the #if, #ifdef, #ifndef or #else

def skip_pp_part(s,i):
		
	start_line = get_line(s,i) # used for error messages.
	# trace(start_line)
	
	delta = 0
	while i < len(s):
		c = s[i]
		if 0:
			if c == '\n':
				trace(`delta` + ":" + get_line(s,i))
		if match_word(s,i,"#if") or match_word(s,i,"#ifdef") or match_word(s,i,"#ifndef"):
			i,delta1 = skip_pp_if(s,i)
			delta += delta1
		elif match_word(s,i,"#else") or match_word(s,i,"#endif"):
			return i,delta
		elif c == '\'' or c == '"': i = skip_string(s,i)
		elif c == '{':
			delta += 1 ; i += 1
		elif c == '}':
			delta -= 1 ; i += 1
		elif match(s,i,"//"): i = skip_line(s,i)
		elif match(s,i,"/*"): i = skip_block_comment(s,i)
		else: i += 1
	return i,delta
#@-body
#@-node:11::skip_pp_part
#@+node:12::skip_python_string
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
#@-node:12::skip_python_string
#@+node:13::skip_string : called by tangle
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
#@-node:13::skip_string : called by tangle
#@+node:14::skip_to_semicolon
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
#@-node:14::skip_to_semicolon
#@+node:15::skip_typedef
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
#@-node:15::skip_typedef
#@-node:18::Scanners: calling scanError
#@+node:19::Scanners: no error messages
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
#@+node:2::find_line_start
#@+body
def find_line_start(s,i):

	i = string.rfind(s,'\n',0,i) # Finds the highest index in the range.
	if i == -1: return 0
	else: return i + 1
#@-body
#@-node:2::find_line_start
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
# We no longer require that the directive appear befor any @c directive or 
# section definition.

#@-at
#@@c

def is_special(s,i,directive):

	# j = skip_line(s,i) ; trace(`s[i:j]` + " : " + `directive`)
	assert (directive and directive [0] == '@' )

	# 10/23/02: all directives except @others must start the line.
	skip_flag = directive == "@others"
	while i < len(s):
		if match_word(s,i,directive):
			return true, i
		else:
			i = skip_line(s,i)
			if skip_flag:
				i = skip_ws(s,i)
	return false, -1
#@-body
#@-node:6::is_special
#@+node:7::is_ws & is_ws_or_nl
#@+body
def is_ws(c):

	return c == '\t' or c == ' '
	
def is_ws_or_nl(s,i):

	return is_nl(s,i) or (i < len(s) and is_ws(s[i]))
#@-body
#@-node:7::is_ws & is_ws_or_nl
#@+node:8::match
#@+body
# Warning: this code makes no assumptions about what follows pattern.

def match(s,i,pattern):

	return s and pattern and string.find(s,pattern,i,i+len(pattern)) == i
#@-body
#@-node:8::match
#@+node:9::match_c_word
#@+body
def match_c_word (s,i,name):

	if name == None: return false
	n = len(name)
	if n == 0: return false
	return name == s[i:i+n] and (i+n == len(s) or not is_c_id(s[i+n]))
#@-body
#@-node:9::match_c_word
#@+node:10::match_ignoring_case
#@+body
def match_ignoring_case(s1,s2):

	if s1 == None or s2 == None: return false
	return string.lower(s1) == string.lower(s2)
#@-body
#@-node:10::match_ignoring_case
#@+node:11::match_word
#@+body
def match_word(s,i,pattern):

	if pattern == None: return false
	j = len(pattern)
	if j == 0: return false
	if string.find(s,pattern,i,i+j) != i:
		return false
	if i+j >= len(s):
		return true
	c = s[i+j]
	return not (c in string.letters or c in string.digits or c == '_')
#@-body
#@-node:11::match_word
#@+node:12::skip_blank_lines
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
#@-node:12::skip_blank_lines
#@+node:13::skip_c_id
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
#@-node:13::skip_c_id
#@+node:14::skip_line, skip_to_end_of_line
#@+body
#@+at
#  These methods skip to the next newline, regardless of whether the newline 
# may be preceeded by a backslash. Consequently, they should be used only when 
# we know that we are not in a preprocessor directive or string.

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
#@-node:14::skip_line, skip_to_end_of_line
#@+node:15::skip_long
#@+body
# returns (i, val) or (i, None) if s[i] does not point at a number.

def skip_long(s,i):

	digits = string.digits
	val = 0
	i = skip_ws(s,i)
	n = len(s)
	if i >= n or s[i] not in "+-" + digits:
		return i, None
	# Rewritten: 7/18/02.
	j = i
	if s[i] in '+-':    # whr allow sign if first digit
		i +=1
	while i < n and s[i] in digits:
		i += 1
	val = int(s[j:i])
	return i, val
#@-body
#@-node:15::skip_long
#@+node:16::skip_matching_delims
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
#@-node:16::skip_matching_delims
#@+node:17::skip_nl
#@+body
#@+at
#  This function skips a single "logical" end-of-line character.  We need this 
# function because different systems have different end-of-line conventions.

#@-at
#@@c

def skip_nl (s,i):

	if match(s,i,"\r\n"): return i + 2
	elif match(s,i,'\n') or match(s,i,'\r'): return i + 1
	else: return i
#@-body
#@-node:17::skip_nl
#@+node:18::skip_pascal_braces
#@+body
# Skips from the opening { to the matching }.

def skip_pascal_braces(s,i):

	# No constructs are recognized inside Pascal block comments!
	k = string.find(s,'}',i)
	if i == -1: return len(s)
	else: return k
#@-body
#@-node:18::skip_pascal_braces
#@+node:19::skip_ws, skip_ws_and_nl
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
#@-node:19::skip_ws, skip_ws_and_nl
#@-node:19::Scanners: no error messages
#@+node:20::shortFileName
#@+body
def shortFileName (fileName):
	
	if 0: # I don't like the conversion to lower case
		fileName = os.path.normpath(fileName)
	head,tail = os.path.split(fileName)
	return tail
#@-body
#@-node:20::shortFileName
#@+node:21::sortSequence
#@+body
#@+at
#  sequence is a sequence of items, each of which is a sequence containing at 
# least n elements.
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
#  The sort() method takes an optional argument specifying a comparison 
# function of two arguments (list items) which should return -1, 0 or 1 
# depending on whether the first argument is considered smaller than, equal 
# to, or larger than the second argument.
# 
# Note that this slows the sorting process down considerably; e.g. to sort a 
# list in reverse order it is much faster to use calls to the methods sort() 
# and reverse() than to use the built-in function sort() with a comparison 
# function that reverses the ordering of the elements.
# 
# So a "clever" solution wouldn't be so clever after all.

#@-at
#@@c
#@-body
#@-node:21::sortSequence
#@+node:22::Timing
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
#@-node:22::Timing
#@+node:23::Tk.Text selection (utils)
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
#@+node:3::setTextSelection
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
#@-node:3::setTextSelection
#@-node:23::Tk.Text selection (utils)
#@+node:24::Unicode...
#@+node:1::convertChar/String/ToXMLCharRef
#@+body
def convertCharToXMLCharRef(c,xml_encoding):

	try:
		if type(c) == types.UnicodeType:
			xml_encoding = app().config.xml_version_string
			e = c.encode(xml_encoding)
			e = unicode(e,xml_encoding)
			return e
		else:
			s = unicode(c,xml_encoding)
			return s
	except:
		#Convert to a character reference.
		return u"&#%d;" % ord(c)

def convertStringToXMLCharRef(s,xml_encoding):
	
	s2 = u""
	for c in s:
		s2 += convertCharToXMLCharRef(c,xml_encoding)
	return s2
#@-body
#@-node:1::convertChar/String/ToXMLCharRef
#@+node:2::replaceNonEncodingChar/s
#@+body
def replaceNonEncodingChar(c,c2,xml_encoding):

	try:
		if type(c) == types.UnicodeType:
			xml_encoding = app().config.xml_version_string
			e = c.encode(xml_encoding)
			e = unicode(e,xml_encoding)
			return e
		else:
			s = unicode(c,xml_encoding)
			return s
	except:
		if 0:
			m = "invalid in "+xml_encoding+": "
			c2 = c.encode("utf-8")
			m = unicode(m,"utf-8") + unicode(c2,"utf-8")
			es(m)
		return c2
			
def replaceNonEncodingChars(s,c2,xml_encoding):
	
	s2 = u""
	for c in s:
		s2 += replaceNonEncodingChar(c,c2,xml_encoding)
	return s2
#@-body
#@-node:2::replaceNonEncodingChar/s
#@+node:3::es_nonEncodingChar, returnNonEncodingChar
#@+body
def es_nonEncodingChars(s,xml_encoding):

	for c in s:
		s2 = returnNonEncodingChar(c,xml_encoding)
		if len(s2) > 0:
			es(s2)
		
def returnNonEncodingChar(c,xml_encoding):
	try:
		if type(c) == types.UnicodeType:
			xml_encoding = app().config.xml_version_string
			e = c.encode(xml_encoding)
			unicode(e,xml_encoding)
			return u""
		else:
			unicode(c,xml_encoding)
			return u""
	except:
		if ord(c) < 32 or ord(c) >= 128:
			return c + "=" + hex(ord(c))
		else:
			return c
#@-body
#@-node:3::es_nonEncodingChar, returnNonEncodingChar
#@-node:24::Unicode...
#@+node:25::update_file_if_changed
#@+body
#@+at
#  This function compares two files. If they are different, we replace 
# file_name with temp_name. Otherwise, we just delete temp_name.  Both files 
# should be closed.

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
			try:
				# 10/6/02: retain the access mode of the previous file,
				# removing any setuid, setgid, and sticky bits.
				mode = (os.stat(file_name))[0] & 0777
			except:
				mode = None
			try: # Replace file with temp file.
				os.remove(file_name)
				utils_rename(temp_name, file_name)
				if mode: # 10/3/02: retain the access mode of the previous file.
					os.chmod(file_name,mode)
				es("***updating: " + file_name)
			except:
				es("Rename failed: no file created!")
				es(`file_name` + " may be read-only or in use")
				es_exception()
	else:
		try:
			# os.rename(temp_name, file_name)
			utils_rename(temp_name, file_name)
			es("Creating: " + file_name)
		except:
			es("Rename failed: no file created!")
			es(`file_name` + " may be read-only or in use")
			es_exception()
#@-body
#@-node:25::update_file_if_changed
#@+node:26::utils_rename
#@+body
#@+at
#  Platform-independent rename.
# 
# os.rename may fail on some Unix flavors if src and dst are on different filesystems.

#@-at
#@@c

def utils_rename(src,dst):
	
	if sys.platform=="win32":
		os.rename(src,dst)
	else:
		from distutils.file_util import move_file
		move_file(src,dst)

#@-body
#@-node:26::utils_rename
#@-others
#@-body
#@-node:0::@file leoUtils.py
#@-leo
