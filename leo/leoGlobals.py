#@+leo
#@+node:0::@file leoGlobals.py
#@+body
# Global constants, variables and utility functions used throughout Leo.


#@@language python

import exceptions,os,string,sys,time,types,Tkinter


#@<< define general constants >>
#@+node:1::<< define general constants >>
#@+body
body_newline = '\n'
body_ignored_newline = '\r'

try:
	true = True
	false = False
except:
	# print "True and False not defined"
	true = 1
	false = 0 # Better than None

assert(false!=None)
#@-body
#@-node:1::<< define general constants >>



#@+others
#@+node:2::Most common functions
#@+body
# These are guaranteed always to exist for scripts.
#@-body
#@+node:1::app, setApp
#@+body
# *** Note *** the global statement makes sense only within functions!

gApp = None # Not needed, and keeps Pychecker happy.

def app():
	global gApp
	return gApp

def setApp(app):
	global gApp
	gApp = app
#@-body
#@-node:1::app, setApp
#@+node:2::choose
#@+body
def choose(cond, a, b): # warning: evaluates all arguments

	if cond: return a
	else: return b
#@-body
#@-node:2::choose
#@+node:3::es, enl, ecnl
#@+body
def ecnl():
	ecnls(1)

def ecnls(n):
	log = app().log
	if log:
		while log.es_newlines < n:
			enl()

def enl():
	log = app().log
	if log:
		log.es_newlines += 1
		log.putnl()

def es(s):
	if s == None or len(s) == 0: return
	log = app().log
	if log:
		log.put(s) # No change needed for Unicode!
		# 6/2/02: This logic will fail if log is None.
		for ch in s:
			if ch == '\n': log.es_newlines += 1
			else: log.es_newlines = 0
		ecnl() # only valid here
	else:
		# print "Null log:",
		print s
#@-body
#@-node:3::es, enl, ecnl
#@+node:4::top
#@+body
#@+at
#  11/6/02: app().log is now set correctly when there are multiple windows.
# 
# Before 11/6/02, app().log depended on activate events, and was not 
# reliable.  The following routines now set app().log:
# 
# - frame.doCommand
# - frame.OnMenuClick
# 
# Thus, top() will be reliable after any command is executed.  Creating a new 
# window and opening a .leo file also set app().log correctly, so it appears 
# that all holes have now been plugged.
# 
# Note 1: handleLeoHook calls top(), so the wrong hook function might be 
# dispatched if this routine does not return the proper value.
# 
# Note 2: The value of top() may change during a new or open command, which 
# may change the routine used to execute the "command1" and "command2" hooks.  
# This is not a bug, and hook routines must be aware of this fact.

#@-at
#@@c

def top():

	# 11/6/02: app().log is now set correctly when there are multiple windows.
	frame = app().log # the current frame
	if frame:
		return frame.commands
	else:
		return None

#@-body
#@-node:4::top
#@+node:5::trace is defined below
#@-node:5::trace is defined below
#@+node:6::windows
#@+body
def windows():
	return app().windowList
#@-body
#@-node:6::windows
#@-node:2::Most common functions
#@+node:3::Commands, Dialogs, Directives, & Menus...
#@+node:1::Dialog utils...
#@+node:1::attachLeoIcon & allies
#@+body
#@+at
#  This code requires Fredrik Lundh's PIL and tkIcon packages:
# 
# Download PIL    from http://www.pythonware.com/downloads/index.htm#pil
# Download tkIcon from http://www.effbot.org/downloads/#tkIcon
# 
# We wait until the window has been drawn once before attaching the icon in OnVisiblity.
# 
# Many thanks to Jonathan M. Gilligan for suggesting this code.

#@-at
#@@c

leoIcon = None

def attachLeoIcon (w):
	try:
		global leoIcon
		import Image,tkIcon
		f = onVisibility
		callback = lambda event,w=w,f=f:f(w,event)
		w.bind("<Visibility>",callback)
		if not leoIcon:
			icon_file_name = os.path.join(app().loadDir,'Icons','LeoDoc.ico') # LeoDoc64.ico looks worse :-(
			icon_file_name = os.path.normpath(icon_file_name)
			icon_image = Image.open(icon_file_name)
			leoIcon = tkIcon.Icon(icon_image)
	except:
		# es_exception()
		leoIcon = None
#@-body
#@+node:1::onVisibility
#@+body
# Handle the "visibility" event and attempt to attach the Leo icon.
# This code must be executed whenever the window is redrawn.

def onVisibility (w,event):

	# print "globals.onVisibility"
	global leoIcon
	if leoIcon and w and event and event.widget == w:

		# print "OnVisibility"
		leoIcon.attach(w)
#@-body
#@-node:1::onVisibility
#@-node:1::attachLeoIcon & allies
#@+node:2::get_window_info
#@+body
# WARNING: Call this routine _after_ creating a dialog.
# (This routine inhibits the grid and pack geometry managers.)

def get_window_info (top):
	
	top.update_idletasks() # Required to get proper info.

	# Get the information about top and the screen.
	geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
	dim,x,y = string.split(geom,'+')
	w,h = string.split(dim,'x')
	w,h,x,y = int(w),int(h),int(x),int(y)
	
	return w,h,x,y
#@-body
#@-node:2::get_window_info
#@+node:3::center_dialog
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
#@-node:3::center_dialog
#@+node:4::create_labeled_frame
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
#@-node:4::create_labeled_frame
#@-node:1::Dialog utils...
#@+node:2::Directives...
#@+node:1::@language and @comment directives (leoUtils)
#@+node:1::set_delims_from_language
#@+body
# Returns a tuple (single,start,end) of comment delims

def set_delims_from_language(language):
	
	a = app()
	
	val = a.language_delims_dict.get(language)
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

def set_language(s,i,issue_errors_flag=false):

	a = app()
	tag = "@language"
	# trace(`get_line(s,i)`)
	assert(i != None)
	assert(match_word(s,i,tag))
	i += len(tag) ; i = skip_ws(s, i)
	# Get the argument.
	j = i ; i = skip_c_id(s,i)
	# Allow tcl/tk.
	arg = string.lower(s[j:i])
	if a.language_delims_dict.get(arg):
		language = arg
		delim1, delim2, delim3 = set_delims_from_language(language)
		return language, delim1, delim2, delim3
	
	if issue_errors_flag:
		es("ignoring: " + get_line(s,i))

	return None, None, None, None,
#@-body
#@-node:3::set_language
#@-node:1::@language and @comment directives (leoUtils)
#@+node:2::scanDirectives (utils)
#@+body
#@+at
#  A general-purpose routine that scans v and its ancestors for directives.  
# It returns a dict containing the settings in effect as the result of the 
# @comment, @language, @pagewidth, @path and @tabwidth directives.  This code 
# does not check on the existence of paths, and issues no error messages.
# 
# Perhaps this routine should be the basis of atFile.scanAllDirectives and 
# tangle.scanAllDirectives, but I am loath to make any further to these two 
# already-infamous routines.  Also, this code does not check for @color and 
# @nocolor directives: leoColor.useSyntaxColoring does that.

#@-at
#@@c

def scanDirectives(c,v=None):

	if v == None: v = c.currentVnode()
	
	#@<< Set local vars >>
	#@+node:1::<< Set local vars >>
	#@+body
	loadDir = app().loadDir
	
	page_width = c.page_width
	tab_width  = c.tab_width
	language = c.target_language
	delim1, delim2, delim3 = set_delims_from_language(c.target_language)
	path = None
	
	#@-body
	#@-node:1::<< Set local vars >>

	old = {}
	while v:
		s = v.t.bodyString
		dict = get_directives_dict(s)
		
		#@<< Test for @comment and @language >>
		#@+node:2::<< Test for @comment and @language >>
		#@+body
		# @language and @comment may coexist in @file trees.
		# For this to be effective the @comment directive should follow the @language directive.
		
		if not old.has_key("comment") and dict.has_key("comment"):
			k = dict["comment"]
			delim1,delim2,delim3 = set_delims_from_string(s[k:])
		
		if not old.has_key("language") and dict.has_key("language"):
			k = dict["language"]
			language,delim1,delim2,delim3 = set_language(s,k)
		#@-body
		#@-node:2::<< Test for @comment and @language >>

		
		#@<< Test for @pagewidth >>
		#@+node:3::<< Test for @pagewidth >>
		#@+body
		if dict.has_key("pagewidth") and not old.has_key("pagewidth"):
		
			k = dict["pagewidth"]
			j = i = k + len("@pagewidth")
			i, val = skip_long(s,i)
			if val != None and val > 0:
				page_width = val
		#@-body
		#@-node:3::<< Test for @pagewidth >>

		
		#@<< Test for @path >>
		#@+node:4::<< Test for @path >>
		#@+body
		if not path and not old.has_key("path") and dict.has_key("path"):
		
			k = dict["path"]
			
			#@<< compute relative path from s[k:] >>
			#@+node:1::<< compute relative path from s[k:] >>
			#@+body
			j = i = k + len("@path")
			i = skip_to_end_of_line(s,i)
			path = string.strip(s[j:i])
			
			# Remove leading and trailing delims if they exist.
			if len(path) > 2 and (
				(path[0]=='<' and path[-1] == '>') or
				(path[0]=='"' and path[-1] == '"') ):
				path = path[1:-1]
			
			path = string.strip(path)
			if 0: # 11/14/02: we want a _relative_ path, not an absolute path.
				path = os.path.join(loadDir,path)
			#@-body
			#@-node:1::<< compute relative path from s[k:] >>

			if path and len(path) > 0:
				base = getBaseDirectory() # returns "" on error.
				path = os.path.join(base,path)
		#@-body
		#@-node:4::<< Test for @path >>

		
		#@<< Test for @tabwidth >>
		#@+node:5::<< Test for @tabwidth >>
		#@+body
		if dict.has_key("tabwidth") and not old.has_key("tabwidth"):
		
			k = dict["tabwidth"]
			j = i = k + len("@tabwidth")
			i, val = skip_long(s, i)
			if val != None and val != 0:
				tab_width = val
		#@-body
		#@-node:5::<< Test for @tabwidth >>

		old.update(dict)
		v = v.parent()
	return {
		"delims"    : (delim1,delim2,delim3),
		"language"  : language,
		"pagewidth" : page_width,
		"path"      : path,
		"tabwidth"  : tab_width }

#@-body
#@-node:2::scanDirectives (utils)
#@+node:3::findReference
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
#@-node:3::findReference
#@-node:2::Directives...
#@+node:3::enableMenu & disableMenu & setMenuLabel
#@+body
# 11/17/02: Fail gracefully if the item name does not exist.
def enableMenu (menu,name,val):
	try:
		state = choose(val,"normal","disabled")
		menu.entryconfig(name,state=state)
	except: pass

def disableMenu (menu,name):
	try:
		menu.entryconfig(name,state="disabled")
	except: pass

def setMenuLabel (menu,name,label):
	try:
		menu.entryconfig(name,label=label)
	except: pass
#@-body
#@-node:3::enableMenu & disableMenu & setMenuLabel
#@+node:4::sortSequence
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
#@-node:4::sortSequence
#@+node:5::wrap_lines
#@+body
#@+at
#  Returns a list of lines, consisting of the input lines wrapped to the given pageWidth.
# 
# Important note: this routine need not deal with leading whitespace.  
# Instead, the caller should simply reduce pageWidth by the width of leading 
# whitespace wanted, then add that whitespace to the lines returned here.
# 
# The key to this code is the invarient that line never ends in whitespace.

#@-at
#@@c
# DTHEIN 3-NOV-2002: handle indented first line (normal or hanging indent)

def wrap_lines (lines,pageWidth,firstLineWidth=None):
	
	if pageWidth < 10:
		pageWidth = 10
		
	# DTHEIN 3-NOV-2002: First line is special
	if not firstLineWidth:
		firstLineWidth = pageWidth
	if firstLineWidth < 10:
		firstLineWidth = 10
	outputLineWidth = firstLineWidth

	# trace(`lines`)
	result = [] # The lines of the result.
	line = "" # The line being formed.  It never ends in whitespace.
	for s in lines:
		i = 0
		while i < len(s):
			assert(len(line) < outputLineWidth)
			j = skip_ws(s,i)   # ;   ws = s[i:j]
			k = skip_non_ws(s,j) ; word = s[j:k]
			assert(k>i)
			i = k
			if 1 + len(word) + len(line) < outputLineWidth:
				if len(word) > 0:
					
					#@<< place blank and word on the present line >>
					#@+node:1::<< place blank and word on the present line >>
					#@+body
					if len(line) == 0:
						# Just add the word to the start of the line.
						line = word
					else:
						# Add the word, preceeded by a blank.
						line = string.join((line,' ',word),'')
					#@-body
					#@-node:1::<< place blank and word on the present line >>

				else: pass # discard the trailing whitespace.
			else:
				
				#@<< place word on a new line >>
				#@+node:2::<< place word on a new line >>
				#@+body
				# End the previous line.
				if len(line) > 0:
					result.append(line)
					outputLineWidth = pageWidth # DTHEIN 3-NOV-2002: width for remaining lines
					
				# Discard the whitespace and put the word on a new line.
				line = word
				
				# Careful: the word may be longer than pageWidth.
				if len(line) >= pageWidth:
					result.append(line)
					outputLineWidth = pageWidth # DTHEIN 3-NOV-2002: width for remaining lines
					line = ""
				
				#@-body
				#@-node:2::<< place word on a new line >>

	if len(line) > 0:
		result.append(line)
	# trace(`result`)
	return result
#@-body
#@-node:5::wrap_lines
#@-node:3::Commands, Dialogs, Directives, & Menus...
#@+node:4::Hooks
#@+node:1::enableIdleTimeHook, disableIdleTimeHook, idleTimeHookHandler
#@+body
def enableIdleTimeHook(idleTimeDelay=100):
	app().idleTimeHook = true
	app().idleTimeDelay = idleTimeDelay # Delay in msec.
	app().root.after_idle(idleTimeHookHandler)

def disableIdleTimeHook():
	app().idleTimeHook = false
	
def idleTimeHookHandler(*args):
	a = app()
	handleLeoHook("idle")
	# Requeue this routine after 100 msec.
	# Faster requeues overload the system.
	if a.idleTimeHook:
		a.root.after(a.idleTimeDelay,idleTimeHookHandler)
#@-body
#@-node:1::enableIdleTimeHook, disableIdleTimeHook, idleTimeHookHandler
#@+node:2::handleLeoHook
#@+body
#@+at
#  This global function calls a hook routine.  Hooks are identified by the tag param.
# Returns the value returned by the hook routine, or None if the there is an exception.
# 
# We look for a hook routine in three places:
# 1. top().hookFunction
# 2. app().hookFunction
# 3. customizeLeo.customizeLeo()
# We set app().hookError on all exceptions.  Scripts that reset 
# app().hookError to try again.

#@-at
#@@c

def handleLeoHook(tag,**keywords):

	a = app() ; c = top() # c may be None during startup.
	
	if not app().config.use_configureLeo_dot_py:
		return None # not enabled.

	if a.hookError:
		return None
	elif c and c.hookFunction:
		try:
			title = c.frame.top.title()
			return c.hookFunction(tag)
		except:
			es("exception in hook function for " + title)
	elif a.hookFunction:
		try:
			return a.hookFunction(tag,keywords)
		except:
			es("exception in app().hookFunction")
	else:
		try:
			from customizeLeo import customizeLeo
			try:
				a.hookFunction = customizeLeo
				return customizeLeo(tag,keywords)
			except:
				a.hookFunction = None
				es("exception in customizeLeo")
		except exceptions.ImportError:
			# print "import customizeLeo failed"
			# Import failed.  This is not an error.
			a.hookError = true # Supress this function.
			a.idleTimeHook = false # Supress idle-time hook
			return None
		except:
			es("error error in customizeLeo")

	# Handle all exceptions except import failure.
	es_exception()
	a.hookError = true # Supress this function.
	a.idleTimeHook = false # Supress idle-time hook
	return None # No return value
#@-body
#@-node:2::handleLeoHook
#@-node:4::Hooks
#@+node:5::Dumping, Timing, Tracing & Sherlock
#@+node:1::alert
#@+body
def alert(message):

	es(message)

	import tkMessageBox
	tkMessageBox.showwarning("Alert", message)

#@-body
#@-node:1::alert
#@+node:2::angleBrackets & virtual_event_name
#@+body
# Returns < < s > >

def angleBrackets(s):

	return ( "<<" + s +
		">>") # must be on a separate line.

virtual_event_name = angleBrackets
#@-body
#@-node:2::angleBrackets & virtual_event_name
#@+node:3::dump
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
#@-node:3::dump
#@+node:4::es_exception
#@+body
def es_exception (full=false):

	import traceback
	typ,val,tb = sys.exc_info()
	if full:
		errList = traceback.format_exception(typ,val,tb)
	else:
		errList = traceback.format_exception_only(typ,val)
	for i in errList:
		es(i)
	traceback.print_exc()
#@-body
#@-node:4::es_exception
#@+node:5::get_line & get_line_after
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
#@-node:5::get_line & get_line_after
#@+node:6::printBindings
#@+body
def print_bindings (name,window):

	bindings = window.bind()
	print
	print "Bindings for", name
	for b in bindings:
		print `b`
#@-body
#@-node:6::printBindings
#@+node:7::printGlobals
#@+body
def printGlobals(message=None):
	
	# Get the list of globals.
	globs = list(globals())
	globs.sort()
	
	# Print the list.
	if message:
		leader = "-" * 10
		print leader, ' ', message, ' ', leader
	for glob in globs:
		print glob
#@-body
#@-node:7::printGlobals
#@+node:8::printLeoModules
#@+body
def printLeoModules(message=None):
	
	# Create the list.
	mods = []
	for name in sys.modules.keys():
		if name and name[0:3] == "leo":
			mods.append(name)

	# Print the list.
	if message:
		leader = "-" * 10
		print leader, ' ', message, ' ', leader
	mods.sort()
	for m in mods:
		print m,
	print
#@-body
#@-node:8::printLeoModules
#@+node:9::Sherlock...
#@+body
#@+at
#  Starting with this release, you will see trace statements throughout the 
# code.  The trace function is defined in leoGlobals.py; trace implements much 
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
#@-node:9::Sherlock...
#@+node:10::Timing
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
#@-node:10::Timing
#@-node:5::Dumping, Timing, Tracing & Sherlock
#@+node:6::Files & Directories...
#@+node:1::create_temp_name
#@+body
# Returns a temporary file name.

def create_temp_name ():

	import tempfile
	temp = tempfile.mktemp()
	# trace(`temp`)
	return temp
#@-body
#@-node:1::create_temp_name
#@+node:2::ensure_extension
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
#@-node:2::ensure_extension
#@+node:3::get_directives_dict
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
#@-node:3::get_directives_dict
#@+node:4::getBaseDirectory
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
		return "" # No relative base given.

#@-body
#@-node:4::getBaseDirectory
#@+node:5::getUserNewline
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
#@-node:5::getUserNewline
#@+node:6::makeAllNonExistentDirectories
#@+body
#@+at
#  This is a generalization of os.makedir.
# It attempts to make all non-existent directories.

#@-at
#@@c

def makeAllNonExistentDirectories (dir):

	if not app().config.create_nonexistent_directories:
		return None

	dir1 = dir = os.path.normpath(dir)
	# Split dir into all its component parts.
	paths = []
	while len(dir) > 0:
		head,tail=os.path.split(dir)
		if len(tail) == 0:
			paths.append(head)
			break
		else:
			paths.append(tail)
			dir = head
	path = ""
	paths.reverse()
	for s in paths:
		path=os.path.join(path,s)
		if not os.path.exists(path):
			try:
				os.mkdir(path)
				es("created directory: "+path)
			except:
				es("exception creating directory: "+path)
				es_exception()
				return None
	return dir1 # All have been created.
#@-body
#@-node:6::makeAllNonExistentDirectories
#@+node:7::readlineForceUnixNewline (Steven P. Schaefer)
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
#@-node:7::readlineForceUnixNewline (Steven P. Schaefer)
#@+node:8::shortFileName
#@+body
def shortFileName (fileName):
	
	if 0: # I don't like the conversion to lower case
		fileName = os.path.normpath(fileName)
	head,tail = os.path.split(fileName)
	return tail
#@-body
#@-node:8::shortFileName
#@+node:9::update_file_if_changed
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
			es("creating: " + file_name)
		except:
			es("rename failed: no file created!")
			es(`file_name` + " may be read-only or in use")
			es_exception()
#@-body
#@-node:9::update_file_if_changed
#@+node:10::utils_rename
#@+body
#@+at
#  Platform-independent rename.
# 
# os.rename may fail on some Unix flavors if src and dst are on different filesystems.

#@-at
#@@c

def utils_rename(src,dst):
	
	head,tail=os.path.split(dst)
	if head and len(head) > 0:
		makeAllNonExistentDirectories(head)
	
	if sys.platform=="win32":
		os.rename(src,dst)
	else:
		from distutils.file_util import move_file
		move_file(src,dst)
#@-body
#@-node:10::utils_rename
#@-node:6::Files & Directories...
#@+node:7::Lists...
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
#@-node:7::Lists...
#@+node:8::Scanning, selection, text & whitespace...
#@+node:1::scanError
#@+body
#@+at
#  It seems dubious to bump the Tangle error count here.  OTOH, it really 
# doesn't hurt.

#@-at
#@@c

def scanError(s):

	# Bump the error count in the tangle command.
	top().tangleCommands.errors += 1

	es(s)
#@-body
#@-node:1::scanError
#@+node:2::Scanners: calling scanError
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
#@-node:2::Scanners: calling scanError
#@+node:3::Scanners: no error messages
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

	# bug fix: 11/2/02: change i to i+1 in rfind
	i = string.rfind(s,'\n',0,i+1) # Finds the highest index in the range.
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
#@+node:18::skip_non_ws
#@+body
def skip_non_ws (s,i):

	n = len(s)
	while i < n and not is_ws(s[i]):
		i += 1
	return i
#@-body
#@-node:18::skip_non_ws
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
#@-node:3::Scanners: no error messages
#@+node:4::Whitespace...
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
#@+node:3::get_leading_ws
#@+body
def get_leading_ws(s):
	
	"""Returns the leading whitespace of 's'."""

	i = 0 ; n = len(s)
	while i < n and s[i] in (' ','\t'):
		i += 1
	return s[0:i]

#@-body
#@-node:3::get_leading_ws
#@+node:4::optimizeLeadingWhitespace
#@+body
# Optimize leading whitespace in s with the given tab_width.

def optimizeLeadingWhitespace (line,tab_width):

	i, width = skip_leading_ws_with_indent(line,0,tab_width)
	s = computeLeadingWhitespace(width,tab_width) + line[i:]
	return s
#@-body
#@-node:4::optimizeLeadingWhitespace
#@+node:5::removeLeadingWhitespace
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
#@-node:5::removeLeadingWhitespace
#@+node:6::removeTrailingWs
#@+body
# Warning: string.rstrip also removes newlines!

def removeTrailingWs(s):

	j = len(s)-1
	while j >= 0 and (s[j] == ' ' or s[j] == '\t'):
		j -= 1
	return s[:j+1]

#@-body
#@-node:6::removeTrailingWs
#@+node:7::skip_leading_ws
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
#@-node:7::skip_leading_ws
#@+node:8::skip_leading_ws_with_indent
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
#@-node:8::skip_leading_ws_with_indent
#@-node:4::Whitespace...
#@+node:5::Tk.Text selection (utils)
#@+node:1::bound_paragraph
#@+body
def bound_paragraph(t=None):
	"""Find the bounds of the text paragraph that contains the current cursor position.
	
t: a Tk.Text widget

Returns:
	None if the cursor is on a whitespace line or a delimeter line.
	Otherwise: (start,end,endsWithNL,wsFirst,wsSecond)

start: the paragraph starting position,
end: the paragraph ending position,
endsWithNL: true if the paragraph ends with a newline"""

	if not t: return None
	x=t.index("insert")
	
	# Return if the selected line is all whitespace or a Leo directive.
	s = t.get(x+"linestart",x+"lineend")
	if len(s)==0 or s.isspace() or s[0] == '@':
		return None	

	# Point start and end at the start and end of the selected line.
	start = t.index(x+"linestart")
	tmpLine = int(float(start))
	end = str(tmpLine + 1) + ".0"
	
	# EKR: This is needlessly complex.
	# It would be much easier to use a list of lines,
	# rather than asking TK to do so much work.

	# Set start to the start of the paragraph.
	while (tmpLine > 1):
		tmpLine -= 1
		tmp = str(tmpLine) + ".0"
		s = t.get(tmp,tmp+"lineend")
		if len(s)==0 or s.isspace() or s[0] == '@':
			break
		start = tmp

	# Set end to the end of the paragraph.
	tmpLine = int(float(end))
	bodyEnd = t.index("end")

	while end != bodyEnd:
		end = str(tmpLine) + ".0"
		s = t.get(end,end+"lineend")
		if len(s)==0 or s.isspace() or s[0] == '@':
			break
		tmpLine += 1

	# do we insert a trailing NL?
	endsWithNL = len(t.get(end))

	return start, end, endsWithNL
#@-body
#@-node:1::bound_paragraph
#@+node:2::getTextSelection
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
#@-node:2::getTextSelection
#@+node:3::getSelectedText
#@+body
# t is a Tk.Text widget.  Returns the text of the selected range of t.

def getSelectedText (t):

	start, end = getTextSelection(t)
	if start and end:
		return t.get(start,end)
	else:
		return None
#@-body
#@-node:3::getSelectedText
#@+node:4::setTextSelection
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
#@-node:4::setTextSelection
#@-node:5::Tk.Text selection (utils)
#@+node:6::Unicode...
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
#@-node:6::Unicode...
#@-node:8::Scanning, selection, text & whitespace...
#@+node:9::Startup & initialization...
#@+node:1::CheckVersion (Dave Hein)
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
#@-node:1::CheckVersion (Dave Hein)
#@+node:2::unloadAll
#@+body
#@+at
#  Unloads all of Leo's modules.  Based on code from the Python Cookbook.
# 
# It would be very confusing to call this reloadAll.  In fact, this routine 
# does no reloading at all.  You must understand that modules are reloaded 
# _only_ as the result of a later call to import.
# 
# Actually, the more I think about it, the less useful this routine appears.  
# It is easy enought to save LeoPy.leo and then reload it, and trying to do 
# this kind of processing looks like asking for trouble...

#@-at
#@@c

def unloadAll():

	try:
		import sys
		a = app()
		modules = []
		for name in sys.modules.keys():
			if name and name[0:3]=="leo":
				del (sys.modules[name])
				modules.append(name)
		# Restore gApp.  This must be done first.
		setApp(a)
		print "unloaded",str(len(modules)),"modules"
	except:
		es_exception()

#@-body
#@-node:2::unloadAll
#@-node:9::Startup & initialization...
#@-others
#@-body
#@-node:0::@file leoGlobals.py
#@-leo
