# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file leoGlobals.py
#@@first # -*- coding: utf-8 -*-

# Global constants, variables and utility functions used throughout Leo.

#@@language python

import exceptions,os,re,string,sys,time,Tkinter,traceback,types

#@<< define general constants >>
#@+node:<< define general constants >>
body_newline = '\n'
body_ignored_newline = '\r'

try:
	true = True
	false = False
except:
	# print "True and False not defined"
	true = True = 1
	false = False = 0 # Better than None

assert(false!=None)
#@nonl
#@-node:<< define general constants >>
#@nl

#@+others
#@+node:createTopologyList
def createTopologyList (c=None,root=None,useHeadlines=false):
	
	"""Creates a list describing a node and all its descendents"""
	
	if not c: c = top()
	if not root: root = c.rootVnode()
	v = root
	if useHeadlines:
		aList = [(v.numberOfChildren(),v.headString()),]
	else:
		aList = [v.numberOfChildren()]
	child = v.firstChild()
	while child:
		aList.append(createTopologyList(c,child,useHeadlines))
		child = child.next()
	return aList
#@nonl
#@-node:createTopologyList
#@+node:checkClones2Links
def checkClones2Links (c=None,verbose=false):
	
	if not c: c = top()
	
	c.clearAllVisited()
	v = c.rootVnode()
	#@	<< clear statistics >>
	#@+node:<< clear statistics >>
	targetsInDerivedFiles = []
	multipleTargetsInDerivedFiles = []
	clonesInNoDerivedFiles = []
	clonedAtFileNodes = []
	#@-node:<< clear statistics >>
	#@nl
	while v:
		if v.isCloned() and not v.t.isVisited():
			v.t.setVisited()
			#@			<< handle each item in v's join list >>
			#@+node:<< handle each item in v's join list >>
			if v.isAnyAtFileNode():
				clonedAtFileNodes.append(v)
			else:
				anchors = 0 ; targets = 0
				for j in v.t.joinList:
					
					# See if j should be an anchor: i.e., whether it is in any @file node.
					p = j ; isAnchor = false
					while p:
						if p.isAnyAtFileNode():
							isAnchor = true
							break
						p = p.parent()
					if isAnchor: anchors += 1
					else: targets += 1
			
				if anchors == 1:
					targetsInDerivedFiles.append(v)
				elif anchors > 1:
					multipleTargetsInDerivedFiles.append(v)
				else:
					clonesInNoDerivedFiles.append(v)
			#@nonl
			#@-node:<< handle each item in v's join list >>
			#@nl
		v = v.threadNext()
				
	#@	<< print statistics >>
	#@+node:<< print statistics >>
	for name, theList in (
		("targetsInDerivedFiles:", targetsInDerivedFiles),
		("multipleTargetsInDerivedFiles:", multipleTargetsInDerivedFiles),
		("clonesInNoDerivedFiles:", clonesInNoDerivedFiles),
		("clonedAtFileNodes:", clonedAtFileNodes)):
	
		print ; print name, len(theList)
	
		if verbose:
			headlines = []
			for v in theList:
				headlines.append(v.cleanHeadString())
			headlines.sort()
			for h in headlines:
				print h
	#@nonl
	#@-node:<< print statistics >>
	#@nl
#@nonl
#@-node:checkClones2Links
#@+node:CheckVersion (Dave Hein)
#@+at
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
#               compared against
# condition: can be any of "==", "!=", ">=", "<=", ">", or "<"
# stringCompare: whether to test a token using only the
#              leading integer of the token, or using the
#              entire token string.  For example, a value
#              of "0.0.1.0" means that we use the integer
#              value of the first, second, and fourth
#              tokens, but we use a string compare for the
#              third version token.
# delimiter: the character that separates the tokens in the
#          version strings.
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
			raise EnvironmentError,errMsg
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
	raise EnvironmentError,"condition must be one of '>=', '>', '==', '!=', '<', or '<='."
#@-node:CheckVersion (Dave Hein)
#@+node:class Bunch
# From The Python Cookbook.

import operator

class Bunch:
	
	"""A class that represents a colection of things.
	
	Especially useful for representing a collection of related variables."""
	
	def __init__(self, **keywords):
		self.__dict__.update (keywords)

	def ivars(self):
		return self.__dict__.keys()
		
	def __setitem__ (self,key,value):
		return operator.setitem(self.__dict__,key,value)
		
	def __getitem__ (self,key):
		return operator.getitem(self.__dict__,key)
		
		
		
#@-node:class Bunch
#@+node:attachLeoIcon & allies
#@+at 
#@nonl
# This code requires Fredrik Lundh's PIL and tkIcon packages:
# 
# Download PIL    from http://www.pythonware.com/downloads/index.htm#pil
# Download tkIcon from http://www.effbot.org/downloads/#tkIcon
# 
# We wait until the window has been drawn once before attaching the icon in 
# OnVisiblity.
# 
# Many thanks to Jonathan M. Gilligan for suggesting this code.
#@-at
#@@c

leoIcon = None

def attachLeoIcon (w):
	try:
		import Image,_tkicon
		import tkIcon
		global leoIcon
		
		f = onVisibility
		callback = lambda event,w=w,f=f:f(w,event)
		w.bind("<Visibility>",callback)
		if not leoIcon:
			# Using a .gif rather than an .ico allows us to specify transparency.
			icon_file_name = os.path.join(app().loadDir,'..','Icons','LeoWin.gif')
			icon_file_name = os.path.normpath(icon_file_name)
			icon_image = Image.open(icon_file_name)
			if 1: # Doesn't resize.
				leoIcon = createLeoIcon(icon_image)
			else: # Assumes 64x64
				leoIcon = tkIcon.Icon(icon_image)
			
	except:
		# es_exception()
		leoIcon = None
#@nonl
#@-node:attachLeoIcon & allies
#@+node:createLeoIcon
# This code is adapted from tkIcon.__init__
# Unlike the tkIcon code, this code does _not_ resize the icon file.

def createLeoIcon (icon):
	
	try:
		import Image,_tkicon
		import tkIcon
		
		i = icon ; m = None
		# create transparency mask
		if i.mode == "P":
			try:
				t = i.info["transparency"]
				m = i.point(lambda i, t=t: i==t, "1")
			except KeyError: pass
		elif i.mode == "RGBA":
			# get transparency layer
			m = i.split()[3].point(lambda i: i == 0, "1")
		if not m:
			m = Image.new("1", i.size, 0) # opaque
		# clear unused parts of the original image
		i = i.convert("RGB")
		i.paste((0, 0, 0), (0, 0), m)
		# create icon
		m = m.tostring("raw", ("1", 0, 1))
		c = i.tostring("raw", ("BGRX", 0, -1))
		return _tkicon.new(i.size, c, m)
	except:
		return None
#@nonl
#@-node:createLeoIcon
#@+node:onVisibility
# Handle the "visibility" event and attempt to attach the Leo icon.
# This code must be executed whenever the window is redrawn.

def onVisibility (w,event):

	global leoIcon

	try:
		import Image,_tkicon
		import tkIcon
		if leoIcon and w and event and event.widget == w:
			if 1: # Allows us not to resize the icon.
				leoIcon.attach(w.winfo_id())
			else:
				leoIcon.attach(w)
	except: pass
#@nonl
#@-node:onVisibility
#@+node:get_window_info
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
#@nonl
#@-node:get_window_info
#@+node:center_dialog
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
#@nonl
#@-node:center_dialog
#@+node:create_labeled_frame
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
#@nonl
#@-node:create_labeled_frame
#@+node:set_delims_from_language
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
#@-node:set_delims_from_language
#@+node:set_delims_from_string
#@+at 
#@nonl
# Returns (delim1, delim2, delim2), the delims following the @comment 
# directive.
# 
# This code can be called from @languge logic, in which case s can point at 
# @comment
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
#@nonl
#@-node:set_delims_from_string
#@+node:set_language
def set_language(s,i,issue_errors_flag=false):
	
	"""Scan the @language directive that appears at s[i:].

	Returns (language, delim1, delim2, delim3)
	"""

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
#@nonl
#@-node:set_language
#@+node:findReference
#@+at 
#@nonl
# We search the descendents of v looking for the definition node matching 
# name.
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
#@-node:findReference
#@+node:get_directives_dict & globalDirectiveList
#@+at 
#@nonl
# The caller passes [root_node] or None as the second arg.  This allows us to 
# distinguish between None and [None].
# 
# 5/17/03: globalDirectiveList is now visible externally so plugins may add to 
# the list of directives.
#@-at
#@@c

globalDirectiveList = [
	"color", "comment", "encoding", "header", "ignore",
	"language", "lineending", "nocolor", "noheader", "nowrap",
	"pagewidth", "path", "quiet", "root", "silent",
	"tabwidth", "terse", "unit", "verbose", "wrap"]

def get_directives_dict(s,root=None):
	
	"""Scans root for @directives found in globalDirectivesList
	Returns a dict containing pointers to the start of each directive"""

	if root: root_node = root[0]
	dict = {}
	i = 0 ; n = len(s)
	while i < n:
		if s[i] == '@' and i+1 < n:
			#@			<< set dict for @ directives >>
			#@+node:<< set dict for @ directives >>
			j = skip_c_id(s,i+1)
			word = s[i+1:j]
			if word in globalDirectiveList:
				dict [word] = i
			#@-node:<< set dict for @ directives >>
			#@nl
		elif root and match(s,i,"<<"):
			#@			<< set dict["root"] for noweb * chunks >>
			#@+node:<< set dict["root"] for noweb * chunks >>
			#@+at 
			#@nonl
			# The following looks for chunk definitions of the form < < * > > 
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
			#@nonl
			#@-node:<< set dict["root"] for noweb * chunks >>
			#@nl
		i = skip_line(s,i)
	return dict
#@nonl
#@-node:get_directives_dict & globalDirectiveList
#@+node:getOutputNewline
def getOutputNewline (lineending = None):
	
	"""Convert the name of a line ending to the line ending itself.
	Use the output_newline configuration option if no lineending is given.
	"""
	
	if lineending:
		s = lineending
	else:
		s = app().config.output_newline
	s = string.lower(s)
	if s in ( "nl","lf","platform"): s = '\n'
	elif s == "cr": s = '\r'
	elif s == "crlf": s = "\r\n"
	else: s = '\n' # Default for erroneous values.
	return s
#@nonl
#@-node:getOutputNewline
#@+node:scanAtEncodingDirective
def scanAtEncodingDirective(s,dict):
	
	"""Scan the @encoding directive at s[dict["encoding"]:].

	Returns the encoding name or None if the encoding name is invalid.
	"""

	k = dict["encoding"]
	i = skip_to_end_of_line(s,k)
	j = len("@encoding")
	encoding = s[k+j:i].strip()
	if isValidEncoding(encoding):
		# trace(encoding)
		return encoding
	else:
		es("invalid @encoding:"+encoding,color="red")
		return None
#@nonl
#@-node:scanAtEncodingDirective
#@+node:scanAtLineendingDirective
def scanAtLineendingDirective(s,dict):
	
	"""Scan the @lineending directive at s[dict["lineending"]:].

	Returns the actual lineending or None if the name of the lineending is invalid.
	"""

	k = dict["lineending"]
	i = skip_to_end_of_line(s,k)
	j = len("@lineending")
	j = skip_ws(s,j)
	e = s[k+j:i].strip()

	if e in ("cr","crlf","lf","nl","platform"):
		lineending = getOutputNewline(e)
		# trace(`e`,`lineending`)
		return lineending
	else:
		es("invalid @lineending directive:"+e,color="red")
		return None
#@-node:scanAtLineendingDirective
#@+node:scanAtPagewidthDirective
def scanAtPagewidthDirective(s,dict,issue_error_flag=false):
	
	"""Scan the @pagewidth directive at s[dict["pagewidth"]:].

	Returns the value of the width or None if the width is invalid.
	"""
	
	k = dict["pagewidth"]
	j = i = k + len("@pagewidth")
	i, val = skip_long(s,i)
	if val != None and val > 0:
		# trace(val)
		return val
	else:
		if issue_error_flag:
			j = skip_to_end_of_line(s,k)
			es("ignoring " + s[k:j],color="red")
		return None
#@-node:scanAtPagewidthDirective
#@+node:scanAtTabwidthDirective
def scanAtTabwidthDirective(s,dict,issue_error_flag=false):
	
	"""Scan the @tabwidth directive at s[dict["tabwidth"]:].

	Returns the value of the width or None if the width is invalid.
	"""
	
	k = dict["tabwidth"]
	j = i = k + len("@tabwidth")
	i, val = skip_long(s, i)
	if val != None and val != 0:
		# trace(`val`)
		return val
	else:
		if issue_error_flag:
			i = skip_to_end_of_line(s,k)
			es("Ignoring " + s[k:i],color="red")
		return None

#@-node:scanAtTabwidthDirective
#@+node:scanDirectives (utils)
#@+at 
#@nonl
# A general-purpose routine that scans v and its ancestors for directives.  It 
# returns a dict containing the settings in effect as the result of the 
# @comment, @language, @lineending, @pagewidth, @path and @tabwidth 
# directives.  This code does not check on the existence of paths, and issues 
# no error messages.
# 
# Perhaps this routine should be the basis of atFile.scanAllDirectives and 
# tangle.scanAllDirectives, but I am loath to make any further to these two 
# already-infamous routines.  Also, this code does not check for @color and 
# @nocolor directives: leoColor.useSyntaxColoring does that.
#@-at
#@@c

def scanDirectives(c,v=None):
	
	"""Scan vnode v and v's ancestors looking for directives.

	Returns a dict containing the results, including defaults.
	"""

	if c == None or top() == None:
		return {} # 7/16/03: for unit tests.
	if v == None: v = c.currentVnode()
	a = app()
	# trace(`v`)
	#@	<< Set local vars >>
	#@+node:<< Set local vars >>
	loadDir = a.loadDir
	
	page_width = c.page_width
	tab_width  = c.tab_width
	language = c.target_language
	delim1, delim2, delim3 = set_delims_from_language(c.target_language)
	path = None
	encoding = None # 2/25/03: This must be none so that the caller can set a proper default.
	lineending = getOutputNewline() # 4/24/03 initialize from config settings.
	wrap = a.config.getBoolWindowPref("body_pane_wraps") # 7/7/03: this is a window pref.
	#@nonl
	#@-node:<< Set local vars >>
	#@nl
	old = {}
	pluginsList = [] # 5/17/03: a list of items for use by plugins.
	while v:
		s = v.t.bodyString
		dict = get_directives_dict(s)
		#@		<< Test for @comment and @language >>
		#@+node:<< Test for @comment and @language >>
		# @language and @comment may coexist in @file trees.
		# For this to be effective the @comment directive should follow the @language directive.
		
		if not old.has_key("comment") and dict.has_key("comment"):
			k = dict["comment"]
			delim1,delim2,delim3 = set_delims_from_string(s[k:])
		
		# Reversion fix: 12/06/02: We must use elif here, not if.
		elif not old.has_key("language") and dict.has_key("language"):
			k = dict["language"]
			language,delim1,delim2,delim3 = set_language(s,k)
		#@nonl
		#@-node:<< Test for @comment and @language >>
		#@nl
		#@		<< Test for @encoding >>
		#@+node:<< Test for @encoding >>
		if not old.has_key("encoding") and dict.has_key("encoding"):
			
			e = scanAtEncodingDirective(s,dict)
			if e:
				encoding = e
		#@-node:<< Test for @encoding >>
		#@nl
		#@		<< Test for @lineending >>
		#@+node:<< Test for @lineending >>
		if not old.has_key("lineending") and dict.has_key("lineending"):
			
			e = scanAtLineendingDirective(s,dict)
			if e:
				lineending = e
		#@-node:<< Test for @lineending >>
		#@nl
		#@		<< Test for @pagewidth >>
		#@+node:<< Test for @pagewidth >>
		if dict.has_key("pagewidth") and not old.has_key("pagewidth"):
			
			w = scanAtPagewidthDirective(s,dict)
			if w and w > 0:
				page_width = w
		#@nonl
		#@-node:<< Test for @pagewidth >>
		#@nl
		#@		<< Test for @path >>
		#@+node:<< Test for @path >>
		if not path and not old.has_key("path") and dict.has_key("path"):
		
			k = dict["path"]
			#@	<< compute relative path from s[k:] >>
			#@+node:<< compute relative path from s[k:] >>
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
			#@nonl
			#@-node:<< compute relative path from s[k:] >>
			#@nl
			if path and len(path) > 0:
				base = getBaseDirectory() # returns "" on error.
				path = os.path.join(base,path)
		#@nonl
		#@-node:<< Test for @path >>
		#@nl
		#@		<< Test for @tabwidth >>
		#@+node:<< Test for @tabwidth >>
		if dict.has_key("tabwidth") and not old.has_key("tabwidth"):
			
			w = scanAtTabwidthDirective(s,dict)
			if w and w > 0:
				tab_width = w
		#@nonl
		#@-node:<< Test for @tabwidth >>
		#@nl
		#@		<< Test for @wrap and @nowrap >>
		#@+node:<< Test for @wrap and @nowrap >>
		if not old.has_key("wrap") and not old.has_key("nowrap"):
			
			if dict.has_key("wrap"):
				wrap = true
			elif dict.has_key("nowrap"):
				wrap = false
		#@nonl
		#@-node:<< Test for @wrap and @nowrap >>
		#@nl
		doHook("scan-directives",c=c,v=v,s=s,
			old_dict=old,dict=dict,pluginsList=pluginsList)
		old.update(dict)
		v = v.parent()

	if path == None: path = getBaseDirectory()

	return {
		"delims"    : (delim1,delim2,delim3),
		"encoding"  : encoding,
		"language"  : language,
		"lineending": lineending,
		"pagewidth" : page_width,
		"path"      : path,
		"tabwidth"  : tab_width,
		"pluginsList": pluginsList,
		"wrap"      : wrap }

#@-node:scanDirectives (utils)
#@+node:canonicalizeMenuName & cononicalizeTranslatedMenuName
def canonicalizeMenuName (name):
	
	name = name.lower() ; newname = ""
	for ch in name:
		# if ch not in (' ','\t','\n','\r','&'):
		if ch in string.letters:
			newname = newname+ch
	return newname
	
def canonicalizeTranslatedMenuName (name):
	
	name = name.lower() ; newname = ""
	for ch in name:
		if ch not in (' ','\t','\n','\r','&'):
		# if ch in string.letters:
			newname = newname+ch
	return newname
#@-node:canonicalizeMenuName & cononicalizeTranslatedMenuName
#@+node:enableMenu & disableMenu & setMenuLabel
# 11/17/02: Fail gracefully if the item name does not exist.
def enableMenu (menu,name,val):
	state = choose(val,"normal","disabled")
	try:
		menu.entryconfig(name,state=state)
	except:
		try:
			realName = app().getRealMenuName(name)
			realName = realName.replace("&","")
			menu.entryconfig(realName,state=state)
		except:
			print "enableMenu menu,name,val:",menu,name,val
			es_exception()
			pass

def disableMenu (menu,name):
	try:
		menu.entryconfig(name,state="disabled")
	except: 
		try:
			realName = app().getRealMenuName(name)
			realName = realName.replace("&","")
			menu.entryconfig(realName,state="disabled")
		except:
			print "disableMenu menu,name:",menu,name
			es_exception()
			pass

def setMenuLabel (menu,name,label,underline=-1):
	try:
		if type(name) == type(0):
			# "name" is actually an index into the menu.
			menu.entryconfig(name,label=label,underline=underline)
		else:
			# Bug fix: 2/16/03: use translated name.
			realName = app().getRealMenuName(name)
			realName = realName.replace("&","")
			# Bug fix: 3/25/03" use tranlasted label.
			label = app().getRealMenuName(label)
			label = label.replace("&","")
			menu.entryconfig(realName,label=label,underline=underline)
	except:
		print "setMenuLabel menu,name,label:",menu,name,label
		es_exception()
		pass
#@nonl
#@-node:enableMenu & disableMenu & setMenuLabel
#@+node:openWithFileName (leoGlobals)
def openWithFileName(fileName,old_c=None):
	
	"""Create a Leo Frame for the indicated fileName if the file exists."""
	
	from leoFrame import LeoFrame
	assert(app().config)

	if not fileName or len(fileName) == 0:
		return false, None

	# Create a full normalized path name.
	# Display the file name with case intact.
	fileName = os.path.join(os.getcwd(), fileName)
	fileName = os.path.normpath(fileName)
	oldFileName = fileName 
	fileName = os.path.normcase(fileName)

	# If the file is already open just bring its window to the front.
	list = app().windowList
	for frame in list:
		fn = os.path.normcase(frame.mFileName)
		fn = os.path.normpath(fn)
		if fileName == fn:
			frame.top.deiconify()
			app().setLog(frame,"OpenWithFileName")
			# es("This window already open")
			return true, frame
			
	fileName = oldFileName # Use the idiosyncratic file name.

	try:
		file = open(fileName,'r')
		if file:
			frame = LeoFrame(fileName)
			if not doHook("open1",
				old_c=old_c,new_c=frame.commands,fileName=fileName):
				app().setLog(frame,"OpenWithFileName") # 5/12/03
				app().lockLog() # 6/30/03
				frame.commands.fileCommands.open(file,fileName) # closes file.
				app().unlockLog() # 6/30/03
			frame.openDirectory=os.path.dirname(fileName)
			frame.updateRecentFiles(fileName)
			doHook("open2",
				old_c=old_c,new_c=frame.commands,fileName=fileName)
			return true, frame
		else:
			es("can not open" + fileName)
			return false, None
	except:
		es("exceptions opening" + fileName)
		es_exception()
		return false, None
#@nonl
#@-node:openWithFileName (leoGlobals)
#@+node:wrap_lines
#@+at 
#@nonl
# Returns a list of lines, consisting of the input lines wrapped to the given 
# pageWidth.
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
					#@					<< place blank and word on the present line >>
					#@+node:<< place blank and word on the present line >>
					if len(line) == 0:
						# Just add the word to the start of the line.
						line = word
					else:
						# Add the word, preceeded by a blank.
						line = string.join((line,' ',word),'')
					#@nonl
					#@-node:<< place blank and word on the present line >>
					#@nl
				else: pass # discard the trailing whitespace.
			else:
				#@				<< place word on a new line >>
				#@+node:<< place word on a new line >>
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
				#@-node:<< place word on a new line >>
				#@nl
	if len(line) > 0:
		result.append(line)
	# trace(`result`)
	return result
#@nonl
#@-node:wrap_lines
#@+node:create_temp_name
# Returns a temporary file name.

def create_temp_name ():

	import tempfile
	temp = tempfile.mktemp()
	# trace(`temp`)
	return temp
#@nonl
#@-node:create_temp_name
#@+node:ensure_extension
def ensure_extension (name, ext):

	file, old_ext = os.path.splitext(name)
	if len(name) == 0:
		return name # don't add to an empty name.
	elif old_ext and old_ext == ext:
		return name
	else:
		return file + ext
#@nonl
#@-node:ensure_extension
#@+node:getBaseDirectory
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
#@-node:getBaseDirectory
#@+node:makeAllNonExistentDirectories
#@+at 
#@nonl
# This is a generalization of os.makedir.
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
#@nonl
#@-node:makeAllNonExistentDirectories
#@+node:readlineForceUnixNewline (Steven P. Schaefer)
#@+at 
#@nonl
# Stephen P. Schaefer 9/7/2002
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
#@-node:readlineForceUnixNewline (Steven P. Schaefer)
#@+node:redirecting stderr and stdout
class redirectClass:
	#@	<< redirectClass methods >>
	#@+node:<< redirectClass methods >>
	# To redirect stdout a class only needs to implement a write(self,s) method.
	def __init__ (self):
		self.old = None
		
	def isRedirected (self):
		return self.old != None
		
	def flush(self, *args):
		return # 6/14/03:  For LeoN: just for compatibility.
	
	def redirect (self,stdout=1):
		import sys
		if not self.old:
			if stdout:
				self.old,sys.stdout = sys.stdout,self
			else:
				self.old,sys.stderr = sys.stderr,self
	
	def undirect (self,stdout=1):
		import sys
		if self.old:
			if stdout:
				sys.stdout,self.old = self.old,None
			else:
				sys.stderr,self.old = self.old,None
	
	def write(self,s):
		if self.old:
			if app().log: app().log.put(s)
			else: self.old.write(s)
		else: print s # Typically will not happen.
	#@-node:<< redirectClass methods >>
	#@nl

# Create two redirection objects, one for each stream.
redirectStdErrObj = redirectClass()
redirectStdOutObj = redirectClass()

#@<< define convenience methods for redirecting streams >>
#@+node:<< define convenience methods for redirecting streams >>

# Redirect streams to the current log window.
def redirectStderr():
	global redirectStdErrObj
	redirectStdErrObj.redirect(stdout=false)

def redirectStdout():
	global redirectStdOutObj
	redirectStdOutObj.redirect()

# Restore standard streams.
def restoreStderr():
	global redirectStdErrObj
	redirectStdErrObj.undirect(stdout=false)
	
def restoreStdout():
	global redirectStdOutObj
	redirectStdOutObj.undirect()
		
def stdErrIsRedirected():
	global redirectStdErrObj
	return redirectStdErrObj.isRedirected()
	
def stdOutIsRedirected():
	global redirectStdOutObj
	return redirectStdOutObj.isRedirected()
#@nonl
#@-node:<< define convenience methods for redirecting streams >>
#@nl

if 0: # Test code: may be safely and conveniently executed in the child node.
	#@	<< test code >>
	#@+node:<< test code >>
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", stdOutIsRedirected()
	print "stderr isRedirected:", stdErrIsRedirected()
	
	from leoGlobals import redirectStderr,redirectStdout
	redirectStderr()
	redirectStdout()
	
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", stdOutIsRedirected()
	print "stderr isRedirected:", stdErrIsRedirected()
	
	from leoGlobals import restoreStderr
	restoreStderr()
	
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", stdOutIsRedirected()
	print "stderr isRedirected:", stdErrIsRedirected()
	
	from leoGlobals import restoreStdout
	restoreStdout()
	
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", stdOutIsRedirected()
	print "stderr isRedirected:", stdErrIsRedirected()
	#@nonl
	#@-node:<< test code >>
	#@nl
#@nonl
#@-node:redirecting stderr and stdout
#@+node:sanitize_filename
#@+at 
#@nonl
# This prepares string s to be a valid file name:
# 
# - substitute '_' whitespace and characters used special path characters.
# - eliminate all other non-alphabetic characters.
# - strip leading and trailing whitespace.
# - return at most 128 characters.
#@-at
#@@c

def sanitize_filename(s):

	result = ""
	for ch in s.strip():
		if ch in string.letters:
			result += ch
		elif ch in string.whitespace: # Translate whitespace.
			result += '_'
		elif ch in ('.','\\','/',':'): # Translate special path characters.
			result += '_'
	while 1:
		n = len(result)
		result = result.replace('__','_')
		if len(result) == n:
			break
	result = result.strip()
	return result [:128]
#@nonl
#@-node:sanitize_filename
#@+node:shortFileName
def shortFileName (fileName):
	
	return os.path.basename(fileName)
#@nonl
#@-node:shortFileName
#@+node:update_file_if_changed
#@+at 
#@nonl
# This function compares two files. If they are different, we replace 
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
				es("Rename failed: no file created!",color="red")
				es(`file_name` + " may be read-only or in use")
				es_exception()
	else:
		try:
			# os.rename(temp_name, file_name)
			utils_rename(temp_name, file_name)
			es("creating: " + file_name)
		except:
			es("rename failed: no file created!",color="red")
			es(`file_name` + " may be read-only or in use")
			es_exception()
#@nonl
#@-node:update_file_if_changed
#@+node:utils_rename
#@+at 
#@nonl
# Platform-independent rename.
# 
# os.rename may fail on some Unix flavors if src and dst are on different 
# filesystems.
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
#@nonl
#@-node:utils_rename
#@+node:Sherlock...
#@+at 
#@nonl
# Starting with this release, you will see trace statements throughout the 
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
#   j = skip_line(s,i) ; trace(s[i:j])
# 
# trace(function) exectutes the function if tracing for f has been enabled.  
# For example,
# 
#   trace(self.f2)
# 
# You enable and disable tracing by calling init_trace(args).  Examples:
# 
#   init_trace("+*")         # enable all traces
#   init_trace("+a","+b")    # enable traces for a and b
#   init_trace(("+a","+b"))  # enable traces for a and b
#   init_trace("-a")         # disable tracing for a
#   traces = init_trace("?") # return the list of enabled traces
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
#   trace_tag("-nocolor", self.disable_color)
#@-at
#@-node:Sherlock...
#@+node:init_sherlock
# Called by startup code.
# Args are all the arguments on the command line.

def init_sherlock (args):
	
	init_trace(args,echo=0)
	# trace("argv", "sys.argv: " + `sys.argv`)
#@nonl
#@-node:init_sherlock
#@+node:get_Sherlock_args
#@+at 
#@nonl
# It no args are given we attempt to get them from the "SherlockArgs" file.  
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
	# print "get_Sherlock_args:", args
	return args
#@nonl
#@-node:get_Sherlock_args
#@+node:init_trace
def init_trace(args,echo=1):

	t = app().trace_list
	args = get_Sherlock_args(args)

	for arg in args:
		if arg[0] in string.letters: prefix = '+'
		else: prefix = arg[0] ; arg = arg[1:]
		
		if prefix == '?':
			print "trace list:", t
		elif prefix == '+' and not arg in t:
			t.append(string.lower(arg))
			if echo:
				print "enabling:", arg
		elif prefix == '-' and arg in t:
			t.remove(string.lower(arg))
			if echo:
				print "disabling:", arg
		else:
			print "ignoring:", prefix + arg
#@nonl
#@-node:init_trace
#@+node:trace
# Convert all args to strings.
# Print if tracing for the presently executing function has been enabled.

def trace (*args,**keys):
	
	callers = keys.get("callers",false)

	s = ""
	for arg in args:
		if type(arg) != type(""):
			arg = repr(arg)
		if len(s) > 0:
			s = s + " " + arg
		else:
			s = arg
	message = s
	try: # get the function name from the call stack.
		f1 = sys._getframe(1) # The stack frame, one level up.
		code1 = f1.f_code # The code object
		name = code1.co_name # The code name
	except: name = ""
	if name == "?":
		name = "<unknown>"

	if callers:
		import traceback
		traceback.print_stack()

	t = app().trace_list
	# tracepoint names starting with '-' must match exactly.
	minus = len(name) > 0 and name[0] == '-'
	if minus: name = name[1:]
	if (not minus and '*' in t) or name.lower() in t:
		s = name + ": " + message
		if 1: print s
		else: es(s)
#@-node:trace
#@+node:trace_tag
# Convert all args to strings.
# Print if tracing for name has been enabled.

def trace_tag (name, *args):
	
	s = ""
	for arg in args:
		if type(arg) != type(""):
			arg = repr(arg)
		if len(s) > 0:
			s = s + ", " + arg
		else:
			s = arg
	message = s

	t = app().trace_list
	# tracepoint names starting with '-' must match exactly.
	minus = len(name) > 0 and name[0] == '-'
	if minus: name = name[1:]
	if (not minus and '*' in t) or name.lower() in t:
		s = name + ": " + message
		if 1: print s
		else: es(s)
#@-node:trace_tag
#@+node:clear_stats
def clear_stats():
	
	app().stats = {}
#@-node:clear_stats
#@+node:print_stats
def print_stats (name=None):
	
	if name:
		if type(name) != type(""):
			name = repr(name)
	else:
		name = callerName(n=2) # Get caller name 2 levels back.
	
	try:
		stats = app().stats
	except:
		print ; print "no statistics at", name ; print
		return
		
	items = stats.items()
	items.sort()
	print ; print "statistics at",name ; print
	for key,value in items:
		print key,value
		
	clear_stats()
#@-node:print_stats
#@+node:stat
def stat (name=None):

	"""Increments the statistic for name in app().stats
	The caller's name is used by default.
	"""
	
	if name:
		if type(name) != type(""):
			name = repr(name)
	else:
		name = callerName(n=2) # Get caller name 2 levels back.

	try:
		stats = app().stats
	except:
		app().stats = stats = {}

	stats[name] = 1 + stats.get(name,0)
#@-node:stat
#@+node:Timing
#@+at 
#@nonl
# pychecker bug: pychecker complains that there is no attribute time.clock
#@-at
#@@c

def getTime():
	return time.clock()
	
def esDiffTime(message, start):
	es(message + ("%6.3f" % (time.clock()-start)))
	return time.clock()
#@nonl
#@-node:Timing
#@+node:alert
def alert(message):

	es(message)

	import tkMessageBox
	tkMessageBox.showwarning("Alert", message)
#@-node:alert
#@+node:angleBrackets & virtual_event_name
# Returns < < s > >

def angleBrackets(s):

	return ( "<<" + s +
		">>") # must be on a separate line.

virtual_event_name = angleBrackets
#@nonl
#@-node:angleBrackets & virtual_event_name
#@+node:callerName
def callerName (n=1):

	try: # get the function name from the call stack.
		f1 = sys._getframe(n) # The stack frame, n levels up.
		code1 = f1.f_code # The code object
		return code1.co_name # The code name
	except:
		es_exception()
		return "<no caller name>"
#@-node:callerName
#@+node:dump
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
#@nonl
#@-node:dump
#@+node:es_error
def es_error (s):
	
	config = app().config
	if config: # May not exist during initialization.
		color = config.getWindowPref("log_error_color")
		es(s,color=color)
	else:
		es(s)
#@nonl
#@-node:es_error
#@+node:es_event_exception
def es_event_exception (eventName,full=false):

	import traceback
	es("exception handling ", eventName, " event")
	typ,val,tb = sys.exc_info()
	if full:
		errList = traceback.format_exception(typ,val,tb)
	else:
		errList = traceback.format_exception_only(typ,val)
	for i in errList:
		es(i)
	traceback.print_exc()
#@nonl
#@-node:es_event_exception
#@+node:es_exception
def es_exception (full=false):

	import traceback
	typ,val,tb = sys.exc_info()
	if full:
		errList = traceback.format_exception(typ,val,tb)
	else:
		errList = traceback.format_exception_only(typ,val)
	for i in errList:
		es_error(i)
	traceback.print_exc()
#@nonl
#@-node:es_exception
#@+node:file/module/plugin_date
def module_date (mod,format=None):
	file = os.path.join(app().loadDir,mod.__file__)
	root,ext = os.path.splitext(file) 
	return file_date(root + ".py",format=format)

def plugin_date (plugin_mod,format=None):
	file = os.path.join(app().loadDir,"..","plugins",plugin_mod.__file__)
	root,ext = os.path.splitext(file) 
	return file_date(root + ".py",format=format)

def file_date (file,format=None):
	if file and len(file)and os.path.exists(file):
		try:
			import time
			n = os.path.getmtime(file)
			if format == None:
				format = "%m/%d/%y %H:%M:%S"
			return time.strftime(format,time.gmtime(n))
		except: pass
	return ""
#@-node:file/module/plugin_date
#@+node:funcToMethod
#@+at 
#@nonl
# The following is taken from page 188 of the Python Cookbook.
# 
# The following method allows you to add a function as a method of any class.  
# That is, it converts the function to a method of the class.  The method just 
# added is available instantly to all existing instances of the class, and to 
# all instances created in the future.
# 
# The function's first argument should be self.
# 
# The newly created method has the same name as the function unless the 
# optional name argument is supplied, in which case that name is used as the 
# method name.
#@-at
#@@c

def funcToMethod(f,theClass,name=None):
	setattr(theClass,name or f.__name__,f)
	# trace(`name`)
#@nonl
#@-node:funcToMethod
#@+node:get_line & get_line_after
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
#@-node:get_line & get_line_after
#@+node:pause
def pause (s):
	
	print s
	
	i = 0
	while i < 1000000L:
		i += 1
#@nonl
#@-node:pause
#@+node:printBindings
def print_bindings (name,window):

	bindings = window.bind()
	print
	print "Bindings for", name
	for b in bindings:
		print b
#@nonl
#@-node:printBindings
#@+node:printGlobals
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
#@nonl
#@-node:printGlobals
#@+node:printLeoModules
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
#@nonl
#@-node:printLeoModules
#@+node:executeScript
def executeScript (name):
	
	"""Execute a script whose short python file name is given"""
	
	mod_name,ext = os.path.splitext(name)
	file = None
	try:
		# This code is in effect an import or a reload.
		# This allows the user to modify scripts without leaving Leo.
		import imp
		file,filename,description = imp.find_module(mod_name)
		imp.load_module(mod_name,file,filename,description)
	except:
		es("Exception executing " + name,color="red")
		es_exception()

	if file:
		file.close()

#@-node:executeScript
#@+node:get_focus
def get_focus(top):
	
	"""Returns the widget that has focus, or body if None."""

	return top.focus_displayof()
#@nonl
#@-node:get_focus
#@+node:set_focus
def set_focus(commands,widget):
	
	"""Set the focus of the widget in the given commander if it needs to be changed."""
	
	focus = commands.frame.top.focus_displayof()
	if focus != widget:
		# trace(`widget`)
		widget.focus_set()
#@nonl
#@-node:set_focus
#@+node:force_focus
def force_focus(widget):
	
	focus = commands.frame.top.focus_displayof()
	if focus != widget:
		trace(widget)
		widget.focus_force() # Apparently it is not a good idea to call focus_force.
#@nonl
#@-node:force_focus
#@+node:Garbage Collection
lastObjectCount = 0
lastObjectsDict = {}
debugGC = false

# gc may not exist everywhere.
try: 
	import gc
	if 0:
		if debugGC:
			gc.set_debug(
				gc.DEBUG_STATS |# prints statistics.
				# gc.DEBUG_LEAK | # Same as all below.
				gc.DEBUG_COLLECTABLE |
				gc.DEBUG_UNCOLLECTABLE |
				gc.DEBUG_INSTANCES |
				gc.DEBUG_OBJECTS |
				gc.DEBUG_SAVEALL)
except:
	traceback.print_exc()

#@+others
#@+node:clearAllIvars
def clearAllIvars (o):
	
	"""Clear all ivars of o, a member of some class."""
	
	o.__dict__.clear()
#@-node:clearAllIvars
#@+node:collectGarbage
def collectGarbage(message=None):
	
	if not debugGC: return
	
	if not message:
		message = callerName(n=2)
	
	try: gc.collect()
	except: pass
	
	if 1:
		printGc(message)
	
	if 0: # This isn't needed unless we want to look at individual objects.
	
		#@		<< make a list of the new objects >>
		#@+node:<< make a list of the new objects >>
		# WARNING: the id trick is not proper because newly allocated objects can have the same address as old objets.
		
		global lastObjectsDict
		objects = gc.get_objects()
		
		newObjects = [o for o in objects if not lastObjectsDict.has_key(id(o))]
		
		lastObjectsDict = {}
		for o in objects:
			lastObjectsDict[id(o)]=o
		#@nonl
		#@-node:<< make a list of the new objects >>
		#@nl
		print "%25s: %d new, %d total objects" % (message,len(newObjects),len(objects))
#@-node:collectGarbage
#@+node:printGc
def printGc(message=None,onlyPrintChanges=false):
	
	if not debugGC: return None
	
	if not message:
		message = callerName(n=2)
	
	global lastObjectCount

	try:
		n = len(gc.garbage)
		n2 = len(gc.get_objects())
		delta = n2-lastObjectCount
		if not onlyPrintChanges or delta:
			if n:
				print "garbage: %d, objects: %+6d =%7d %s" % (n,delta,n2,message)
			else:
				print "objects: %+6d =%7d %s" % (n2-lastObjectCount,n2,message)

		lastObjectCount = n2
		return delta
	except:
		traceback.print_exc()
		return None
#@nonl
#@-node:printGc
#@+node:printGcRefs
def printGcRefs (verbose=true):

	import leoFrame

	refs = gc.get_referrers(app().windowList[0])
	print '-' * 30
	
	
	if verbose:
		print "refs of", app().windowList[0]
		for ref in refs:
			print type(ref)
			if 0:
				if type(ref) == type({}):
					keys = ref.keys()
					keys.sort()
					for key in keys:
						val = ref[key]
						if isinstance(val,leoFrame.LeoFrame):
							print key,ref[key]
	else:
		print "%d referers" % len(refs)
#@nonl
#@-node:printGcRefs
#@-others
#@-node:Garbage Collection
#@+node:enableIdleTimeHook, disableIdleTimeHook, idleTimeHookHandler
#@+at 
#@nonl
# Enables the "idle" hook.
# After enableIdleTimeHook is called, Leo will call the "idle" hook
# approximately every idleTimeDelay milliseconds.
#@-at
#@@c
def enableIdleTimeHook(idleTimeDelay=100):
	app().idleTimeHook = true
	app().idleTimeDelay = idleTimeDelay # Delay in msec.
	app().root.after_idle(idleTimeHookHandler)
	
# Disables the "idle" hook.
def disableIdleTimeHook():
	app().idleTimeHook = false
	
# An internal routine used to dispatch the "idle" hook.
def idleTimeHookHandler(*args):
	
	a = app()
	# New for Python 2.3: may be called during shutdown.
	if a.killed:
		return
	c = top()
	if c: v = c.currentVnode()
	else: v = None
	doHook("idle",c=c,v=v)
	# Requeue this routine after 100 msec.
	# Faster requeues overload the system.
	if a.idleTimeHook:
		a.afterHandler = a.root.after(a.idleTimeDelay,idleTimeHookHandler)
	else:
		a.afterHandler = None
#@nonl
#@-node:enableIdleTimeHook, disableIdleTimeHook, idleTimeHookHandler
#@+node:doHook
#@+at 
#@nonl
# This global function calls a hook routine.  Hooks are identified by the tag 
# param.
# Returns the value returned by the hook routine, or None if the there is an 
# exception.
# 
# We look for a hook routine in three places:
# 1. top().hookFunction
# 2. app().hookFunction
# 3. leoPlugins.doPlugins()
# We set app().hookError on all exceptions.  Scripts may reset app().hookError 
# to try again.
#@-at
#@@c

def doHook(tag,*args,**keywords):

	a = app() ; c = top() # c may be None during startup.
	
	if not a.config.use_plugins:
		return None
	elif a.hookError:
		return None
	elif c and c.hookFunction:
		try:
			return c.hookFunction(tag,keywords)
		except:
			es("exception in c.hookFunction for " + c.frame.top.title())
	elif a.hookFunction:
		try:
			return a.hookFunction(tag,keywords)
		except:
			es("exception in app().hookFunction")
	else:
		import leoPlugins
		try:
			a.hookFunction = leoPlugins.doPlugins
			return a.hookFunction(tag,keywords)
		except:
			a.hookFunction = None
			es("exception in plugin")

	# Handle all exceptions.
	es_exception()
	a.hookError = true # Supress this function.
	a.idleTimeHook = false # Supress idle-time hook
	return None # No return value
#@nonl
#@-node:doHook
#@+node:plugin_signon
def plugin_signon(module_name,verbose=false):
	
	exec("import %s ; m = %s" % (module_name,module_name))
	
	if verbose:
		es("...%s.py v%s: %s" % (
			m.__name__, m.__version__, plugin_date(m)))

		print m.__name__, m.__version__
		
	# Increment a global count.
	import leoPlugins
	leoPlugins.count += 1
#@-node:plugin_signon
#@+node:importFromPath
def importFromPath (name,path):
	
	import imp

	try:
		file = None ; result = None
		try:
			fn = shortFileName(name)
			mod_name,ext = os.path.splitext(fn)
			path = os.path.normpath(path)
			data = imp.find_module(mod_name,[path]) # This can open the file.
			if data:
				file,pathname,description = data
				result = imp.load_module(mod_name,file,pathname,description)
		except:
			es_exception()

	# Bug fix: 6/12/03: Put no return statements before here!
	finally: 
		if file: file.close()

	return result
#@nonl
#@-node:importFromPath
#@+node:appendToList
def appendToList(out, s):

	for i in s:
		out.append(i)
#@nonl
#@-node:appendToList
#@+node:flattenList
def flattenList (theList):

	result = []
	for item in theList:
		if type(item) == types.ListType:
			result.extend(flattenList(item))
		else:
			result.append(item)
	return result
#@nonl
#@-node:flattenList
#@+node:listToString
def listToString(theList):

	if list:
		theList = flattenList(theList)
		return string.join(theList,"")
	else:
		return ""
#@nonl
#@-node:listToString
#@+node:makeDict
# From the Python cookbook.

def makeDict(**keys):
	
	"""Returns a Python dictionary from using the optional keyword arguments."""

	return keys
#@nonl
#@-node:makeDict
#@+node:Most common functions
# These are guaranteed always to exist for scripts.
#@-node:Most common functions
#@+node:app, setApp
# *** Note *** the global statement makes sense only within functions!

gApp = None # Not needed, and keeps Pychecker happy.

def app():
	global gApp
	return gApp

def setApp(app):
	global gApp
	gApp = app
#@nonl
#@-node:app, setApp
#@+node:choose
def choose(cond, a, b): # warning: evaluates all arguments

	if cond: return a
	else: return b
#@nonl
#@-node:choose
#@+node:es, enl, ecnl
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

def es(s,*args,**keys):
	newline = keys.get("newline",true)
	color = keys.get("color",None)
	if type(s) != type("") and type(s) != type(u""): # 1/20/03
		s = repr(s)
	for arg in args:
		if type(arg) != type("") and type(arg) != type(u""): # 1/20/03
			arg = repr(arg)
		s = s + ", " + arg
	a = app() ; log = a.log
	if log:
		# print s
		log.put(s,color=color)
		# 6/2/02: This logic will fail if log is None.
		for ch in s:
			if ch == '\n': log.es_newlines += 1
			else: log.es_newlines = 0
		if newline:
			ecnl() # only valid here
	elif newline:
		a.logWaiting.append((s+'\n',color),) # 2/16/03
		print s
	else:
		a.logWaiting.append((s,color),) # 2/16/03
		print s,
#@nonl
#@-node:es, enl, ecnl
#@+node:top
#@+at 
#@nonl
# frame.doCommand and frame.OnMenuClick now set app().log, so top() will be 
# reliable after any command is executed.
# 
# Note 1: The value of top() may change during a new or open command, which 
# may change the routine used to execute the "command1" and "command2" hooks.  
# This is not a bug, and hook routines must be aware of this fact.
#@-at
#@@c

def top():
	
	"""Return the commander of the topmost window"""
	
	# Warning: may be called during startup or shutdown when nothing exists.
	try:
		return app().log.commands
	except:
		return None
#@nonl
#@-node:top
#@+node:windows
def windows():
	return app().windowList
#@nonl
#@-node:windows
#@+node:getindex
def getindex(text, index):
	
	"""Convert string index of the form line.col into a tuple of two ints."""
	
	return tuple(map(int,string.split(text.index(index), ".")))
#@nonl
#@-node:getindex
#@+node:scanAtFileOptions
def scanAtFileOptions (h,err_flag=false):
	
	assert(match(h,0,"@file"))
	i = len("@file")
	atFileType = "@file"
	optionsList = []

	while match(h,i,'-'):
		#@		<< scan another @file option >>
		#@+node:<< scan another @file option >>
		i += 1 ; err = -1
		
		if match_word(h,i,"asis"):
			if atFileType == "@file":
				atFileType = "@silentfile"
			elif err_flag:
				es("using -asis option in:" + h)
		elif match(h,i,"noref"): # Just match the prefix.
			if atFileType == "@file":
				atFileType = "@rawfile"
			elif atFileType == "@nosentinelsfile":
				atFileType = "@silentfile"
			elif err_flag:
				es("ignoring redundant -noref in:" + h)
		elif match(h,i,"nosent"): # Just match the prefix.
			if atFileType == "@file":
				atFileType = "@nosentinelsfile"
			elif atFileType == "@rawfile":
				atFileType = "@silentfile"
			elif err_flag:
				es("ignoring redundant -nosent in:" + h)
		else:
			for option in ("fat","new","now","old","thin","wait"):
				if match_word(h,i,option):
					optionsList.append(option)
			if len(option) == 0:
				err = i-1
		# Scan to the next minus sign.
		while i < len(h) and h[i] not in (' ','\t','-'):
			i += 1
		if err > -1:
			es("unknown option:" + h[err:i] + " in " + h)
		#@nonl
		#@-node:<< scan another @file option >>
		#@nl
		
	# Convert atFileType to a list of options.
	for fileType,option in (
		("@silentfile","asis"),
		("@nosentinelsfile","nosent"),
		("@rawfile","noref")):
		if atFileType == fileType:
			optionsList.append(option)
			
	# trace(atFileType,optionsList)

	return i,atFileType,optionsList
#@nonl
#@-node:scanAtFileOptions
#@+node:scanAtRootOptions
def scanAtRootOptions (s,i,err_flag=false):
	
	assert(match(s,i,"@root"))
	i += len("@root")
	mode = None 
	while match(s,i,'-'):
		#@		<< scan another @root option >>
		#@+node:<< scan another @root option >>
		i += 1 ; err = -1
		
		if match_word(s,i,"code"): # Just match the prefix.
			if not mode: mode = "code"
			elif err_flag: es("modes conflict in:" + get_line(s,i))
		elif match(s,i,"doc"): # Just match the prefix.
			if not mode: mode = "doc"
			elif err_flag: es("modes conflict in:" + get_line(s,i))
		else:
			err = i-1
			
		# Scan to the next minus sign.
		while i < len(s) and s[i] not in (' ','\t','-'):
			i += 1
		
		if err > -1 and err_flag:
			es("unknown option:" + s[err:i] + " in " + get_line(s,i))
		#@nonl
		#@-node:<< scan another @root option >>
		#@nl

	if mode == None:
		doc = app().config.at_root_bodies_start_in_doc_mode
		mode = choose(doc,"doc","code")
	return i,mode
#@nonl
#@-node:scanAtRootOptions
#@+node:scanError
#@+at 
#@nonl
# It seems dubious to bump the Tangle error count here.  OTOH, it really 
# doesn't hurt.
#@-at
#@@c

def scanError(s):

	# Bump the error count in the tangle command.
	top().tangleCommands.errors += 1

	es(s)
#@nonl
#@-node:scanError
#@+node:scanf
# A quick and dirty sscanf.  Understands only %s and %d.

def scanf (s,pat):
	import re
	count = pat.count("%s") + pat.count("%d")
	pat = pat.replace("%s","(\S+)")
	pat = pat.replace("%d","(\d+)")
	parts = re.split(pat,s)
	result = []
	for part in parts:
		if len(part) > 0 and len(result) < count:
			result.append(part)
	# trace("scanf returns:",result)
	return result
	
if 0: # testing
	from leoGlobals import trace
	scanf("1.0","%d.%d",)
#@nonl
#@-node:scanf
#@+node:Scanners: calling scanError
#@+at 
#@nonl
# These scanners all call scanError() directly or indirectly, so they will 
# call es() if they find an error.  scanError() also bumps 
# commands.tangleCommands.errors, which is harmless if we aren't tangling, and 
# useful if we are.
# 
# These routines are called by the Import routines and the Tangle routines.
#@-at
#@-node:Scanners: calling scanError
#@+node:skip_block_comment
# Scans past a block comment (an old_style C comment).

def skip_block_comment (s,i):

	assert(match(s,i,"/*"))
	j = i ; i += 2 ; n = len(s)
	
	k = string.find(s,"*/",i)
	if k == -1:
		scanError("Run on block comment: " + s[j:i])
		return n
	else: return k + 2
#@nonl
#@-node:skip_block_comment
#@+node:skip_braces
#@+at 
#@nonl
# Skips from the opening to the matching . If no matching is found i is set to 
# len(s).
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
#@nonl
#@-node:skip_braces
#@+node:skip_php_braces (Dave Hein)
#@+at 
#@nonl
# 08-SEP-2002 DTHEIN: Added for PHP import support
# Skips from the opening to the matching . If no matching is found i is set to 
# len(s).
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
#@-node:skip_php_braces (Dave Hein)
#@+node:skip_parens
#@+at 
#@nonl
# Skips from the opening ( to the matching ) . If no matching is found i is 
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
#@nonl
#@-node:skip_parens
#@+node:skip_pascal_begin_end
#@+at 
#@nonl
# Skips from begin to matching end.
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
#@nonl
#@-node:skip_pascal_begin_end
#@+node:skip_pascal_block_comment
# Scans past a pascal comment delimited by (* and *).

def skip_pascal_block_comment(s,i):
	
	j = i
	assert(match(s,i,"(*"))
	i = string.find(s,"*)",i)
	if i > -1: return i + 2
	else:
		scanError("Run on comment" + s[j:i])
		return len(s)

#   n = len(s)
#   while i < n:
#       if match(s,i,"*)"): return i + 2
#       i += 1
#   scanError("Run on comment" + s[j:i])
#   return i
#@nonl
#@-node:skip_pascal_block_comment
#@+node:skip_pascal_string : called by tangle
def skip_pascal_string(s,i):

	j = i ; delim = s[i] ; i += 1
	assert(delim == '"' or delim == '\'')

	while i < len(s):
		if s[i] == delim:
			return i + 1
		else: i += 1

	scanError("Run on string: " + s[j:i])
	return i
#@nonl
#@-node:skip_pascal_string : called by tangle
#@+node:skip_heredoc_string : called by php import (Dave Hein)
#@+at 
#@nonl
# 08-SEP-2002 DTHEIN:  added function skip_heredoc_string
# A heredoc string in PHP looks like:
# 
#   <<<EOS
#   This is my string.
#   It is mine. I own it.
#   No one else has it.
#   EOS
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
#@-node:skip_heredoc_string : called by php import (Dave Hein)
#@+node:skip_pp_directive
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
#@nonl
#@-node:skip_pp_directive
#@+node:skip_pp_if
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
#@-node:skip_pp_if
#@+node:skip_pp_part
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
#@nonl
#@-node:skip_pp_part
#@+node:skip_python_string
def skip_python_string(s,i):

	if match(s,i,"'''") or match(s,i,'"""'):
		j = i ; delim = s[i]*3 ; i += 3
		k = string.find(s,delim,i)
		if k > -1: return k+3
		scanError("Run on triple quoted string: " + s[j:i])
		return len(s)
	else:
		return skip_string(s,i)
#@nonl
#@-node:skip_python_string
#@+node:skip_string : called by tangle
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
#@nonl
#@-node:skip_string : called by tangle
#@+node:skip_to_semicolon
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
#@nonl
#@-node:skip_to_semicolon
#@+node:skip_typedef
def skip_typedef(s,i):

	n = len(s)
	while i < n and is_c_id(s[i]):
		i = skip_c_id(s,i)
		i = skip_ws_and_nl(s,i)
	if match(s,i,'{'):
		i = skip_braces(s,i)
		i = skip_to_semicolon(s,i)
	return i
#@nonl
#@-node:skip_typedef
#@+node:escaped
# Returns true if s[i] is preceded by an odd number of backslashes.

def escaped(s,i):

	count = 0
	while i-1 >= 0 and s[i-1] == '\\':
		count += 1
		i -= 1
	return (count%2) == 1
#@nonl
#@-node:escaped
#@+node:find_line_start
def find_line_start(s,i):

	# bug fix: 11/2/02: change i to i+1 in rfind
	i = string.rfind(s,'\n',0,i+1) # Finds the highest index in the range.
	if i == -1: return 0
	else: return i + 1
#@nonl
#@-node:find_line_start
#@+node:find_on_line
def find_on_line(s,i,pattern):

	# j = skip_line(s,i) ; trace(`s[i:j]`)
	j = string.find(s,'\n',i)
	if j == -1: j = len(s)
	k = string.find(s,pattern,i,j)
	if k > -1: return k
	else: return None
#@nonl
#@-node:find_on_line
#@+node:is_c_id
def is_c_id(ch):

	return ch in string.letters or ch in string.digits or ch == '_'
#@nonl
#@-node:is_c_id
#@+node:is_nl
def is_nl(s,i):

	return i < len(s) and (s[i] == '\n' or s[i] == '\r')
#@nonl
#@-node:is_nl
#@+node:is_special
#@+at 
#@nonl
# Return true if the body text contains the @ directive.
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
#@nonl
#@-node:is_special
#@+node:is_ws & is_ws_or_nl
def is_ws(c):

	return c == '\t' or c == ' '
	
def is_ws_or_nl(s,i):

	return is_nl(s,i) or (i < len(s) and is_ws(s[i]))
#@nonl
#@-node:is_ws & is_ws_or_nl
#@+node:match
# Warning: this code makes no assumptions about what follows pattern.

def match(s,i,pattern):

	return s and pattern and string.find(s,pattern,i,i+len(pattern)) == i
#@nonl
#@-node:match
#@+node:match_c_word
def match_c_word (s,i,name):

	if name == None: return false
	n = len(name)
	if n == 0: return false
	return name == s[i:i+n] and (i+n == len(s) or not is_c_id(s[i+n]))
#@nonl
#@-node:match_c_word
#@+node:match_ignoring_case
def match_ignoring_case(s1,s2):

	if s1 == None or s2 == None: return false
	return string.lower(s1) == string.lower(s2)
#@nonl
#@-node:match_ignoring_case
#@+node:match_word
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
#@nonl
#@-node:match_word
#@+node:skip_blank_lines
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
#@nonl
#@-node:skip_blank_lines
#@+node:skip_c_id
def skip_c_id(s,i):

	n = len(s)
	while i < n:
		c = s[i]
		if c in string.letters or c in string.digits or c == '_':
			i += 1
		else: break
	return i
#@nonl
#@-node:skip_c_id
#@+node:skip_line, skip_to_end_of_line
#@+at 
#@nonl
# These methods skip to the next newline, regardless of whether the newline 
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
#@nonl
#@-node:skip_line, skip_to_end_of_line
#@+node:skip_long
def skip_long(s,i):
	
	"""Scan s[i:] for a valid int.
	Return (i, val) or (i, None) if s[i] does not point at a number.
	"""

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
	try: # 4/24/03: There may be no digits, which would raise an exception.
		val = int(s[j:i])
		return i, val
	except:
		return i,None
#@-node:skip_long
#@+node:skip_matching_delims
def skip_matching_delims(s,i,delim1,delim2):
	
	assert(match(s,i,delim1))

	i += len(delim1)
	k = string.find(s,delim2,i)
	if k == -1:
		return len(s)
	else:
		return k + len(delim2)
#@nonl
#@-node:skip_matching_delims
#@+node:skip_nl
#@+at 
#@nonl
# This function skips a single "logical" end-of-line character.  We need this 
# function because different systems have different end-of-line conventions.
#@-at
#@@c

def skip_nl (s,i):

	if match(s,i,"\r\n"): return i + 2
	elif match(s,i,'\n') or match(s,i,'\r'): return i + 1
	else: return i
#@nonl
#@-node:skip_nl
#@+node:skip_non_ws
def skip_non_ws (s,i):

	n = len(s)
	while i < n and not is_ws(s[i]):
		i += 1
	return i
#@nonl
#@-node:skip_non_ws
#@+node:skip_pascal_braces
# Skips from the opening { to the matching }.

def skip_pascal_braces(s,i):

	# No constructs are recognized inside Pascal block comments!
	k = string.find(s,'}',i)
	if i == -1: return len(s)
	else: return k
#@nonl
#@-node:skip_pascal_braces
#@+node:skip_to_char
def skip_to_char(s,i,ch):
	
	j = string.find(s,ch,i)
	if j == -1:
		return len(s),s[i:]
	else:
		return j,s[i:j]
#@-node:skip_to_char
#@+node:skip_ws, skip_ws_and_nl
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
#@nonl
#@-node:skip_ws, skip_ws_and_nl
#@+node:bound_paragraph
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
#@nonl
#@-node:bound_paragraph
#@+node:getindex
def getindex(text, index):
	
	"""Convert string index of the form line.col into a tuple of two ints."""
	
	return tuple(map(int,string.split(text.index(index), ".")))
#@nonl
#@-node:getindex
#@+node:getSelectedText
# t is a Tk.Text widget.  Returns the text of the selected range of t.

def getSelectedText (t):

	start, end = getTextSelection(t)
	if start and end and start != end: # 7/7/03
		return t.get(start,end)
	else:
		return None
#@nonl
#@-node:getSelectedText
#@+node:getTextSelection
def getTextSelection (t):
	
	"""Return a tuple representing the selected range of t, a Tk.Text widget.
	
	Return a tuple giving the insertion point if no range of text is selected."""

	# To get the current selection
	sel = t.tag_ranges("sel")
	if len(sel) == 2:
		return sel
	else:
		# 7/1/03: Return the insertion point if there is no selected text.
		insert = t.index("insert")
		return insert,insert
#@nonl
#@-node:getTextSelection
#@+node:setTextSelection
#@+at 
#@nonl
# t is a Tk.Text widget.  start and end are positions.  Selects from start to 
# end.
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
#@-node:setTextSelection
#@+node:computeLeadingWhitespace
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
#@nonl
#@-node:computeLeadingWhitespace
#@+node:computeWidth
# Returns the width of s, assuming s starts a line, with indicated tab_width.

def computeWidth (s, tab_width):
		
	w = 0
	for ch in s:
		if ch == '\t':
			w += (abs(tab_width) - (w % abs(tab_width)))
		else:
			w += 1
	return w
#@nonl
#@-node:computeWidth
#@+node:get_leading_ws
def get_leading_ws(s):
	
	"""Returns the leading whitespace of 's'."""

	i = 0 ; n = len(s)
	while i < n and s[i] in (' ','\t'):
		i += 1
	return s[0:i]
#@-node:get_leading_ws
#@+node:optimizeLeadingWhitespace
# Optimize leading whitespace in s with the given tab_width.

def optimizeLeadingWhitespace (line,tab_width):

	i, width = skip_leading_ws_with_indent(line,0,tab_width)
	s = computeLeadingWhitespace(width,tab_width) + line[i:]
	return s
#@nonl
#@-node:optimizeLeadingWhitespace
#@+node:removeLeadingWhitespace
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
#@nonl
#@-node:removeLeadingWhitespace
#@+node:removeTrailingWs
# Warning: string.rstrip also removes newlines!

def removeTrailingWs(s):

	j = len(s)-1
	while j >= 0 and (s[j] == ' ' or s[j] == '\t'):
		j -= 1
	return s[:j+1]
#@-node:removeTrailingWs
#@+node:skip_leading_ws
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
#@nonl
#@-node:skip_leading_ws
#@+node:skip_leading_ws_with_indent
#@+at 
#@nonl
# Skips leading whitespace and returns (i, indent), where i points after the 
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
#@nonl
#@-node:skip_leading_ws_with_indent
#@+node:isValidEncoding
def isValidEncoding (encoding):
	
	try:
		if len(encoding) == 0:
			return false
		u = unicode("a",encoding)
		return true
	except:
		return false
#@-node:isValidEncoding
#@+node:reportBadChars
def reportBadChars (s,encoding):
	
	errors = 0
	if type(s) == type(u""):
		for ch in s:
			try: ch.encode(encoding,"strict")
			except: errors += 1
		if errors:
			# import traceback ; traceback.print_stack()
			es("%d errors converting %s to %s" % 
				(errors, s.encode(encoding,"replace"),encoding))

	elif type(s) == type(""):
		for ch in s:
			try: unicode(ch,encoding,"strict")
			except: errors += 1
		if errors:
			es("%d errors converting %s from %s to unicode" % 
				(errors, s.encode(encoding,"replace"),encoding))
#@nonl
#@-node:reportBadChars
#@+node:toUnicode & toEncodedString
def toUnicode (s,encoding,reportErrors=false):
	
	if type(s) == type(""):
		try:
			s = unicode(s,encoding,"strict")
		except:
			if reportErrors:
				reportBadChars(s,encoding)
			s = unicode(s,encoding,"replace")
	return s
	
def toEncodedString (s,encoding,reportErrors=false):

	if type(s) == type(u""):
		try:
			s = s.encode(encoding,"strict")
		except:
			if reportErrors:
				reportBadChars(s,encoding)
			s = s.encode(encoding,"replace")
	return s
#@nonl
#@-node:toUnicode & toEncodedString
#@+node:getpreferredencoding from 2.3a2
try:
	# Use Python's version of getpreferredencoding if it exists.
	# It is new in Python 2.3.
	import locale
	getpreferredencoding = locale.getpreferredencoding
except:
	# Use code copied from locale.py in Python 2.3alpha2.
	if sys.platform in ('win32', 'darwin', 'mac'):
		#@		<< define getpreferredencoding using _locale >>
		#@+node:<< define getpreferredencoding using _locale >>
		# On Win32, this will return the ANSI code page
		# On the Mac, it should return the system encoding;
		# it might return "ascii" instead.
		
		def getpreferredencoding(do_setlocale = true):
			"""Return the charset that the user is likely using."""
			try:
				import _locale
				return _locale._getdefaultlocale()[1]
			except:
				return None # Good enough for a.finishCreate.
		#@nonl
		#@-node:<< define getpreferredencoding using _locale >>
		#@nl
	else:
		#@		<< define getpreferredencoding for *nix >>
		#@+node:<< define getpreferredencoding for *nix >>
		# On Unix, if CODESET is available, use that.
		try:
			local.CODESET
		except NameError:
			# Fall back to parsing environment variables :-(
			def getpreferredencoding(do_setlocale = true):
				"""Return the charset that the user is likely using,
				by looking at environment variables."""
				try:
					return locale.getdefaultlocale()[1]
				except:
					return None # Good enough for a.finishCreate.
		else:
			def getpreferredencoding(do_setlocale = true):
				"""Return the charset that the user is likely using,
				according to the system configuration."""
				try:
					if do_setlocale:
						oldloc = locale.setlocale(LC_CTYPE)
						locale.setlocale(LC_CTYPE, "")
						result = locale.nl_langinfo(CODESET)
						locale.setlocale(LC_CTYPE, oldloc)
						return result
					else:
						return locale.nl_langinfo(CODESET)
				except:
					return None # Good enough for a.finishCreate.
		#@nonl
		#@-node:<< define getpreferredencoding for *nix >>
		#@nl
#@-node:getpreferredencoding from 2.3a2
#@-others
#@nonl
#@-node:@file leoGlobals.py
#@-leo
