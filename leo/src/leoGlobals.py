# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3093:@file-thin leoGlobals.py
#@@first

"""Global constants, variables and utility functions used throughout Leo."""

#@@language python

import leoGlobals as g # So code can use g below.
# true,false defined below.

import os,string,sys,time,traceback,types

#@<< define general constants >>
#@+node:ekr.20031218072017.3094:<< define general constants >>
body_newline = '\n'
body_ignored_newline = '\r'

try:
	true,false = True,False
except NameError:
	true,false = 1,0
#@nonl
#@-node:ekr.20031218072017.3094:<< define general constants >>
#@nl

app = None # The singleton app object.

# Visible externally so plugins may add to the list of directives.

globalDirectiveList = [
	"color", "comment", "encoding", "header", "ignore",
	"language", "lineending", "nocolor", "noheader", "nowrap",
	"pagewidth", "path", "quiet", "root", "silent",
	"tabwidth", "terse", "unit", "verbose", "wrap"]

#@+others
#@+node:ekr.20031218072017.3095:Checking Leo Files...
#@+node:ekr.20031218072017.822:createTopologyList
def createTopologyList (c=None,root=None,useHeadlines=false):
	
	"""Creates a list describing a node and all its descendents"""
	
	if not c: c = g.top()
	if not root: root = c.rootVnode()
	v = root
	if useHeadlines:
		aList = [(v.numberOfChildren(),v.headString()),]
	else:
		aList = [v.numberOfChildren()]
	child = v.firstChild()
	while child:
		aList.append(g.createTopologyList(c,child,useHeadlines))
		child = child.next()
	return aList
#@nonl
#@-node:ekr.20031218072017.822:createTopologyList
#@-node:ekr.20031218072017.3095:Checking Leo Files...
#@+node:ekr.20031218072017.3097:CheckVersion (Dave Hein)
#@+at
# g.CheckVersion() is a generic version checker.  Assumes a
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
#@-node:ekr.20031218072017.3097:CheckVersion (Dave Hein)
#@+node:ekr.20031218072017.3098:class Bunch
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
		
		
		
#@-node:ekr.20031218072017.3098:class Bunch
#@+node:ekr.20031219074948.1:class nullObject
# From the Python cookbook, recipe 5.23

class nullObject:
	
	"""An object that does nothing, and does it very well."""
	
	def __init__   (self,*args,**keys): pass
	def __call__   (self,*args,**keys): return self
	
	def __repr__   (self): return "nullObject"
	
	def __nonzero__ (self): return 0
	
	def __delattr__(self,attr):     return self
	def __getattr__(self,attr):     return self
	def __setattr__(self,attr,val): return self
#@nonl
#@-node:ekr.20031219074948.1:class nullObject
#@+node:ekr.20031218072017.3099:Commands & Directives
#@+node:ekr.20031218072017.1380:Directive utils...
#@+node:ekr.20031218072017.1381:@language and @comment directives (leoUtils)
#@+node:ekr.20031218072017.1382:set_delims_from_language
# Returns a tuple (single,start,end) of comment delims

def set_delims_from_language(language):

	val = app.language_delims_dict.get(language)
	if val:
		delim1,delim2,delim3 = g.set_delims_from_string(val)
		if delim2 and not delim3:
			return None,delim1,delim2
		else: # 0,1 or 3 params.
			return delim1,delim2,delim3
	else:
		return None, None, None # Indicate that no change should be made
#@-node:ekr.20031218072017.1382:set_delims_from_language
#@+node:ekr.20031218072017.1383:set_delims_from_string
def set_delims_from_string(s):

	"""Returns (delim1, delim2, delim2), the delims following the @comment directive.
	
	This code can be called from @languge logic, in which case s can point at @comment"""

	# Skip an optional @comment
	tag = "@comment"
	i = 0
	if g.match_word(s,i,tag):
		i += len(tag)
		
	count = 0 ; delims = [None, None, None]
	while count < 3 and i < len(s):
		i = j = g.skip_ws(s,i)
		while i < len(s) and not g.is_ws(s[i]) and not g.is_nl(s,i):
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
#@-node:ekr.20031218072017.1383:set_delims_from_string
#@+node:ekr.20031218072017.1384:set_language
def set_language(s,i,issue_errors_flag=false):
	
	"""Scan the @language directive that appears at s[i:].

	Returns (language, delim1, delim2, delim3)
	"""

	tag = "@language"
	# g.trace(g.get_line(s,i))
	assert(i != None)
	assert(g.match_word(s,i,tag))
	i += len(tag) ; i = g.skip_ws(s, i)
	# Get the argument.
	j = i ; i = g.skip_c_id(s,i)
	# Allow tcl/tk.
	arg = string.lower(s[j:i])
	if app.language_delims_dict.get(arg):
		language = arg
		delim1, delim2, delim3 = g.set_delims_from_language(language)
		return language, delim1, delim2, delim3
	
	if issue_errors_flag:
		g.es("ignoring: " + g.get_line(s,i))

	return None, None, None, None,
#@nonl
#@-node:ekr.20031218072017.1384:set_language
#@-node:ekr.20031218072017.1381:@language and @comment directives (leoUtils)
#@+node:ekr.20031218072017.1385:findReference
#@+at 
#@nonl
# We search the descendents of v looking for the definition node matching 
# name.
# There should be exactly one such node (descendents of other definition nodes 
# are not searched).
#@-at
#@@c

def findReference(name,root):

	for p in root.subtree_iter():
		assert(p!=root)
		if p.matchHeadline(name) and not p.isAtIgnoreNode():
			return p

	# g.trace("not found:",name,root)
	return root.c.nullPosition()
#@nonl
#@-node:ekr.20031218072017.1385:findReference
#@+node:ekr.20031218072017.1260:get_directives_dict & globalDirectiveList
# The caller passes [root_node] or None as the second arg.  This allows us to distinguish between None and [None].

def get_directives_dict(s,root=None):
	
	"""Scans root for @directives found in globalDirectivesList.

	Returns a dict containing pointers to the start of each directive"""

	if root: root_node = root[0]
	dict = {}
	i = 0 ; n = len(s)
	while i < n:
		if s[i] == '@' and i+1 < n:
			#@			<< set dict for @ directives >>
			#@+node:ekr.20031218072017.1261:<< set dict for @ directives >>
			j = g.skip_c_id(s,i+1)
			word = s[i+1:j]
			if word in g.globalDirectiveList:
				dict [word] = i
			#@-node:ekr.20031218072017.1261:<< set dict for @ directives >>
			#@nl
		elif root and g.match(s,i,"<<"):
			#@			<< set dict["root"] for noweb * chunks >>
			#@+node:ekr.20031218072017.1262:<< set dict["root"] for noweb * chunks >>
			#@+at 
			#@nonl
			# The following looks for chunk definitions of the form < < * > > 
			# =. If found, we take this to be equivalent to @root filename if 
			# the headline has the form @root filename.
			#@-at
			#@@c
			
			i = g.skip_ws(s,i+2)
			if i < n and s[i] == '*' :
				i = g.skip_ws(s,i+1) # Skip the '*'
				if g.match(s,i,">>="):
					# < < * > > = implies that @root should appear in the headline.
					i += 3
					if root_node:
						dict["root"]=0 # value not immportant
					else:
						g.es(g.angleBrackets("*") + "= requires @root in the headline")
			#@nonl
			#@-node:ekr.20031218072017.1262:<< set dict["root"] for noweb * chunks >>
			#@nl
		i = g.skip_line(s,i)
	return dict
#@nonl
#@-node:ekr.20031218072017.1260:get_directives_dict & globalDirectiveList
#@+node:ekr.20031218072017.1386:getOutputNewline
def getOutputNewline (lineending = None):
	
	"""Convert the name of a line ending to the line ending itself.
	Use the output_newline configuration option if no lineending is given.
	"""
	
	if lineending:
		s = lineending
	else:
		s = app.config.output_newline

	s = s.lower()
	if s in ( "nl","lf"): s = '\n'
	elif s == "cr": s = '\r'
	elif s == "platform": s = os.linesep  # 12/2/03: emakital
	elif s == "crlf": s = "\r\n"
	else: s = '\n' # Default for erroneous values.
	return s
#@nonl
#@-node:ekr.20031218072017.1386:getOutputNewline
#@+node:ekr.20031218072017.1387:scanAtEncodingDirective
def scanAtEncodingDirective(s,dict):
	
	"""Scan the @encoding directive at s[dict["encoding"]:].

	Returns the encoding name or None if the encoding name is invalid.
	"""

	k = dict["encoding"]
	i = g.skip_to_end_of_line(s,k)
	j = len("@encoding")
	encoding = s[k+j:i].strip()
	if g.isValidEncoding(encoding):
		# g.trace(encoding)
		return encoding
	else:
		g.es("invalid @encoding:"+encoding,color="red")
		return None
#@nonl
#@-node:ekr.20031218072017.1387:scanAtEncodingDirective
#@+node:ekr.20031218072017.1388:scanAtLineendingDirective
def scanAtLineendingDirective(s,dict):
	
	"""Scan the @lineending directive at s[dict["lineending"]:].

	Returns the actual lineending or None if the name of the lineending is invalid.
	"""

	k = dict["lineending"]
	i = g.skip_to_end_of_line(s,k)
	j = len("@lineending")
	j = g.skip_ws(s,j)
	e = s[k+j:i].strip()

	if e in ("cr","crlf","lf","nl","platform"):
		lineending = g.getOutputNewline(e)
		# g.trace(e,lineending)
		return lineending
	else:
		# g.es("invalid @lineending directive:"+e,color="red")
		return None
#@nonl
#@-node:ekr.20031218072017.1388:scanAtLineendingDirective
#@+node:ekr.20031218072017.1389:scanAtPagewidthDirective
def scanAtPagewidthDirective(s,dict,issue_error_flag=false):
	
	"""Scan the @pagewidth directive at s[dict["pagewidth"]:].

	Returns the value of the width or None if the width is invalid.
	"""
	
	k = dict["pagewidth"]
	j = i = k + len("@pagewidth")
	i, val = g.skip_long(s,i)
	if val != None and val > 0:
		# g.trace(val)
		return val
	else:
		if issue_error_flag:
			j = g.skip_to_end_of_line(s,k)
			g.es("ignoring " + s[k:j],color="red")
		return None
#@-node:ekr.20031218072017.1389:scanAtPagewidthDirective
#@+node:ekr.20031218072017.1390:scanAtTabwidthDirective
def scanAtTabwidthDirective(s,dict,issue_error_flag=false):
	
	"""Scan the @tabwidth directive at s[dict["tabwidth"]:].

	Returns the value of the width or None if the width is invalid.
	"""
	
	k = dict["tabwidth"]
	i = k + len("@tabwidth")
	i, val = g.skip_long(s, i)
	if val != None and val != 0:
		# g.trace(val)
		return val
	else:
		if issue_error_flag:
			i = g.skip_to_end_of_line(s,k)
			g.es("Ignoring " + s[k:i],color="red")
		return None

#@-node:ekr.20031218072017.1390:scanAtTabwidthDirective
#@+node:ekr.20031218072017.1391:scanDirectives (utils)
#@+at 
#@nonl
# Perhaps this routine should be the basis of atFile.scanAllDirectives and 
# tangle.scanAllDirectives, but I am loath to make any further to these two 
# already-infamous routines.  Also, this code does not check for @color and 
# @nocolor directives: leoColor.useSyntaxColoring does that.
#@-at
#@@c

def scanDirectives(c,p=None):
	
	"""Scan vnode v and v's ancestors looking for directives.

	Returns a dict containing the results, including defaults."""

	if c == None or g.top() == None:
		return {} # For unit tests.
	if p is None:
		p = c.currentPosition()

	#@	<< Set local vars >>
	#@+node:ekr.20031218072017.1392:<< Set local vars >>
	page_width = c.page_width
	tab_width  = c.tab_width
	language = c.target_language
	delim1, delim2, delim3 = g.set_delims_from_language(c.target_language)
	path = None
	encoding = None # 2/25/03: This must be none so that the caller can set a proper default.
	lineending = g.getOutputNewline() # 4/24/03 initialize from config settings.
	wrap = app.config.getBoolWindowPref("body_pane_wraps") # 7/7/03: this is a window pref.
	#@nonl
	#@-node:ekr.20031218072017.1392:<< Set local vars >>
	#@nl
	old = {}
	pluginsList = [] # 5/17/03: a list of items for use by plugins.
	for p in p.self_and_parents_iter():
		s = p.v.t.bodyString
		dict = g.get_directives_dict(s)
		#@		<< Test for @comment and @language >>
		#@+node:ekr.20031218072017.1393:<< Test for @comment and @language >>
		# @language and @comment may coexist in @file trees.
		# For this to be effective the @comment directive should follow the @language directive.
		
		if not old.has_key("comment") and dict.has_key("comment"):
			k = dict["comment"]
			delim1,delim2,delim3 = g.set_delims_from_string(s[k:])
		
		# Reversion fix: 12/06/02: We must use elif here, not if.
		elif not old.has_key("language") and dict.has_key("language"):
			k = dict["language"]
			language,delim1,delim2,delim3 = g.set_language(s,k)
		#@nonl
		#@-node:ekr.20031218072017.1393:<< Test for @comment and @language >>
		#@nl
		#@		<< Test for @encoding >>
		#@+node:ekr.20031218072017.1394:<< Test for @encoding >>
		if not old.has_key("encoding") and dict.has_key("encoding"):
			
			e = g.scanAtEncodingDirective(s,dict)
			if e:
				encoding = e
		#@-node:ekr.20031218072017.1394:<< Test for @encoding >>
		#@nl
		#@		<< Test for @lineending >>
		#@+node:ekr.20031218072017.1395:<< Test for @lineending >>
		if not old.has_key("lineending") and dict.has_key("lineending"):
			
			e = g.scanAtLineendingDirective(s,dict)
			if e:
				lineending = e
		#@-node:ekr.20031218072017.1395:<< Test for @lineending >>
		#@nl
		#@		<< Test for @pagewidth >>
		#@+node:ekr.20031218072017.1396:<< Test for @pagewidth >>
		if dict.has_key("pagewidth") and not old.has_key("pagewidth"):
			
			w = g.scanAtPagewidthDirective(s,dict)
			if w and w > 0:
				page_width = w
		#@nonl
		#@-node:ekr.20031218072017.1396:<< Test for @pagewidth >>
		#@nl
		#@		<< Test for @path >>
		#@+node:ekr.20031218072017.1397:<< Test for @path >>
		if not path and not old.has_key("path") and dict.has_key("path"):
		
			k = dict["path"]
			#@	<< compute relative path from s[k:] >>
			#@+node:ekr.20031218072017.1398:<< compute relative path from s[k:] >>
			j = i = k + len("@path")
			i = g.skip_to_end_of_line(s,i)
			path = string.strip(s[j:i])
			
			# Remove leading and trailing delims if they exist.
			if len(path) > 2 and (
				(path[0]=='<' and path[-1] == '>') or
				(path[0]=='"' and path[-1] == '"') ):
				path = path[1:-1]
			
			path = string.strip(path)
			if 0: # 11/14/02: we want a _relative_ path, not an absolute path.
				path = g.os_path_join(app.loadDir,path)
			#@nonl
			#@-node:ekr.20031218072017.1398:<< compute relative path from s[k:] >>
			#@nl
			if path and len(path) > 0:
				base = g.getBaseDirectory() # returns "" on error.
				path = g.os_path_join(base,path)
				
		#@nonl
		#@-node:ekr.20031218072017.1397:<< Test for @path >>
		#@nl
		#@		<< Test for @tabwidth >>
		#@+node:ekr.20031218072017.1399:<< Test for @tabwidth >>
		if dict.has_key("tabwidth") and not old.has_key("tabwidth"):
			
			w = g.scanAtTabwidthDirective(s,dict)
			if w and w > 0:
				tab_width = w
		#@nonl
		#@-node:ekr.20031218072017.1399:<< Test for @tabwidth >>
		#@nl
		#@		<< Test for @wrap and @nowrap >>
		#@+node:ekr.20031218072017.1400:<< Test for @wrap and @nowrap >>
		if not old.has_key("wrap") and not old.has_key("nowrap"):
			
			if dict.has_key("wrap"):
				wrap = true
			elif dict.has_key("nowrap"):
				wrap = false
		#@nonl
		#@-node:ekr.20031218072017.1400:<< Test for @wrap and @nowrap >>
		#@nl
		g.doHook("scan-directives",c=c,v=p,s=s,
			old_dict=old,dict=dict,pluginsList=pluginsList)
		old.update(dict)

	if path == None: path = g.getBaseDirectory()

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
#@nonl
#@-node:ekr.20031218072017.1391:scanDirectives (utils)
#@-node:ekr.20031218072017.1380:Directive utils...
#@+node:ekr.20031218072017.2052:openWithFileName
def openWithFileName(fileName,old_c,enableLog=true):
	
	"""Create a Leo Frame for the indicated fileName if the file exists."""

	# g.trace(fileName)
	assert(app.config)

	if not fileName or len(fileName) == 0:
		return false, None

	# Create a full normalized path name.
	# Display the file name with case intact.
	fileName = g.os_path_join(os.getcwd(), fileName)
	fileName = g.os_path_normpath(fileName)
	oldFileName = fileName 
	fileName = g.os_path_normcase(fileName)

	# If the file is already open just bring its window to the front.
	list = app.windowList
	for frame in list:
		fn = g.os_path_normcase(frame.c.mFileName)
		fn = g.os_path_normpath(fn)
		if fileName == fn:
			frame.deiconify()
			app.setLog(frame.log,"openWithFileName")
			# g.es("This window already open")
			return true, frame
			
	fileName = oldFileName # Use the idiosyncratic file name.

	try:
		# 11/4/03: open the file in binary mode to allow 0x1a in bodies & headlines.
		file = open(fileName,'rb')
		if file:
			c,frame = app.gui.newLeoCommanderAndFrame(fileName)
			frame.log.enable(enableLog)
			if not g.doHook("open1",old_c=old_c,new_c=c,fileName=fileName):
				app.setLog(frame.log,"openWithFileName")
				app.lockLog()
				frame.c.fileCommands.open(file,fileName) # closes file.
				app.unlockLog()
			frame.openDirectory = g.os_path_dirname(fileName)
			g.doHook("open2",old_c=old_c,new_c=frame.c,fileName=fileName)
			return true, frame
		else:
			g.es("can not open: " + fileName,color="red")
			return false, None
	except IOError:
		g.es("can not open: " + fileName, color="blue")
		return false, None
	except:
		if 1:
			print "exceptions opening:", fileName
			traceback.print_exc()
		else:
			g.es("exceptions opening: " + fileName,color="red")
			g.es_exception()
		return false, None
#@nonl
#@-node:ekr.20031218072017.2052:openWithFileName
#@+node:ekr.20031218072017.3100:wrap_lines
#@+at 
#@nonl
# Important note: this routine need not deal with leading whitespace.  
# Instead, the caller should simply reduce pageWidth by the width of leading 
# whitespace wanted, then add that whitespace to the lines returned here.
# 
# The key to this code is the invarient that line never ends in whitespace.
#@-at
#@@c

def wrap_lines (lines,pageWidth,firstLineWidth=None):

	"""Returns a list of lines, consisting of the input lines wrapped to the given pageWidth."""

	if pageWidth < 10:
		pageWidth = 10
		
	# DTHEIN 3-NOV-2002: First line is special
	if not firstLineWidth:
		firstLineWidth = pageWidth
	if firstLineWidth < 10:
		firstLineWidth = 10
	outputLineWidth = firstLineWidth

	# g.trace(lines)
	result = [] # The lines of the result.
	line = "" # The line being formed.  It never ends in whitespace.
	for s in lines:
		i = 0
		while i < len(s):
			assert(len(line) <= outputLineWidth) # DTHEIN 18-JAN-2004
			j = g.skip_ws(s,i)   # ;   ws = s[i:j]
			k = g.skip_non_ws(s,j) ; word = s[j:k]
			assert(k>i)
			i = k
			# DTHEIN 18-JAN-2004: wrap at exactly the text width, 
			# not one character less
			# 
			wordLen = len(word)
			if len(line) > 0 and wordLen > 0: wordLen += len(" ")
			if wordLen + len(line) <= outputLineWidth:
				if wordLen > 0:
					#@					<< place blank and word on the present line >>
					#@+node:ekr.20031218072017.3101:<< place blank and word on the present line >>
					if len(line) == 0:
						# Just add the word to the start of the line.
						line = word
					else:
						# Add the word, preceeded by a blank.
						line = " ".join([line,word]) # DTHEIN 18-JAN-2004: better syntax
					#@nonl
					#@-node:ekr.20031218072017.3101:<< place blank and word on the present line >>
					#@nl
				else: pass # discard the trailing whitespace.
			else:
				#@				<< place word on a new line >>
				#@+node:ekr.20031218072017.3102:<< place word on a new line >>
				# End the previous line.
				if len(line) > 0:
					result.append(line)
					outputLineWidth = pageWidth # DTHEIN 3-NOV-2002: width for remaining lines
					
				# Discard the whitespace and put the word on a new line.
				line = word
				
				# Careful: the word may be longer than pageWidth.
				if len(line) > pageWidth: # DTHEIN 18-JAN-2004: line can equal pagewidth
					result.append(line)
					outputLineWidth = pageWidth # DTHEIN 3-NOV-2002: width for remaining lines
					line = ""
				#@-node:ekr.20031218072017.3102:<< place word on a new line >>
				#@nl
	if len(line) > 0:
		result.append(line)
	# g.trace(result)
	return result
#@nonl
#@-node:ekr.20031218072017.3100:wrap_lines
#@-node:ekr.20031218072017.3099:Commands & Directives
#@+node:ekr.20031218072017.3103:computeWindowTitle
def computeWindowTitle (fileName):

	if fileName == None:
		return "untitled"
	else:
		path,fn = g.os_path_split(fileName)
		if path:
			title = fn + " in " + path
		else:
			title = fn
		return title
#@nonl
#@-node:ekr.20031218072017.3103:computeWindowTitle
#@+node:ekr.20031218072017.3104:Debugging, Dumping, Timing, Tracing & Sherlock
#@+node:ekr.20031218072017.3105:alert
def alert(message):

	g.es(message)

	import tkMessageBox
	tkMessageBox.showwarning("Alert", message)
#@-node:ekr.20031218072017.3105:alert
#@+node:ekr.20031218072017.3106:angleBrackets & virtual_event_name
# Returns < < s > >

def angleBrackets(s):

	return ( "<<" + s +
		">>") # must be on a separate line.

virtual_event_name = angleBrackets
#@nonl
#@-node:ekr.20031218072017.3106:angleBrackets & virtual_event_name
#@+node:ekr.20031218072017.3107:callerName
def callerName (n=1):

	try: # get the function name from the call stack.
		f1 = sys._getframe(n) # The stack frame, n levels up.
		code1 = f1.f_code # The code object
		return code1.co_name # The code name
	except:
		g.es_exception()
		return "<no caller name>"
#@-node:ekr.20031218072017.3107:callerName
#@+node:ekr.20031218072017.3108:Dumps
#@+node:ekr.20031218072017.3109:dump
def dump(s):
	
	out = ""
	for i in s:
		out += str(ord(i)) + ","
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
#@-node:ekr.20031218072017.3109:dump
#@+node:ekr.20031218072017.3110:es_error
def es_error (s):
	
	config = app.config

	if config: # May not exist during initialization.
		color = config.getWindowPref("log_error_color")
		g.es(s,color=color)
	else:
		g.es(s)
#@nonl
#@-node:ekr.20031218072017.3110:es_error
#@+node:ekr.20031218072017.3111:es_event_exception
def es_event_exception (eventName,full=false):

	g.es("exception handling ", eventName, " event")
	typ,val,tb = sys.exc_info()

	if full:
		errList = traceback.format_exception(typ,val,tb)
	else:
		errList = traceback.format_exception_only(typ,val)

	for i in errList:
		g.es(i)
		
	if not g.stdErrIsRedirected(): # 2/16/04
		traceback.print_exc()
#@nonl
#@-node:ekr.20031218072017.3111:es_event_exception
#@+node:ekr.20031218072017.3112:es_exception
def es_exception (full=true,c=None):
	
	typ,val,tb = sys.exc_info()
	errList = traceback.format_exception(typ,val,tb)
	
	if full:
		lines = errList
	else:
		# Strip cruft lines.
		s1 = "Traceback (most recent call last):"
		s2 = "exec s in {}"
		lines = []
		for line in errList[-4:]:
			if not g.match(line,0,s1) and line.find(s2) == -1:
				lines.append(line)

	for line in lines:
		g.es_error(line)
		if not g.stdErrIsRedirected():
			print line
#@nonl
#@-node:ekr.20031218072017.3112:es_exception
#@+node:ekr.20031218072017.3113:printBindings
def print_bindings (name,window):

	bindings = window.bind()
	print
	print "Bindings for", name
	for b in bindings:
		print b
#@nonl
#@-node:ekr.20031218072017.3113:printBindings
#@+node:ekr.20031218072017.3114:printGlobals
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
#@-node:ekr.20031218072017.3114:printGlobals
#@+node:ekr.20031218072017.3115:printLeoModules
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
#@-node:ekr.20031218072017.3115:printLeoModules
#@-node:ekr.20031218072017.3108:Dumps
#@+node:ekr.20031218072017.1317:file/module/plugin_date
def module_date (mod,format=None):
	file = g.os_path_join(app.loadDir,mod.__file__)
	root,ext = g.os_path_splitext(file) 
	return g.file_date(root + ".py",format=format)

def plugin_date (plugin_mod,format=None):
	file = g.os_path_join(app.loadDir,"..","plugins",plugin_mod.__file__)
	root,ext = g.os_path_splitext(file) 
	return g.file_date(root + ".py",format=format)

def file_date (file,format=None):
	if file and len(file)and g.os_path_exists(file):
		try:
			import time
			n = g.os_path_getmtime(file)
			if format == None:
				format = "%m/%d/%y %H:%M:%S"
			return time.strftime(format,time.gmtime(n))
		except: pass
	return ""
#@-node:ekr.20031218072017.1317:file/module/plugin_date
#@+node:ekr.20031218072017.3116:Files & Directories...
#@+node:ekr.20031218072017.3117:create_temp_name
# Returns a temporary file name.

def create_temp_name ():

	import tempfile
	temp = tempfile.mktemp()
	# g.trace(temp)
	return temp
#@nonl
#@-node:ekr.20031218072017.3117:create_temp_name
#@+node:ekr.20031218072017.3118:ensure_extension
def ensure_extension (name, ext):

	file, old_ext = g.os_path_splitext(name)
	if len(name) == 0:
		return name # don't add to an empty name.
	elif old_ext and old_ext == ext:
		return name
	else:
		return file + ext
#@nonl
#@-node:ekr.20031218072017.3118:ensure_extension
#@+node:ekr.20031218072017.1264:getBaseDirectory
# Handles the conventions applying to the "relative_path_base_directory" configuration option.

def getBaseDirectory():

	base = app.config.relative_path_base_directory

	if base and base == "!":
		base = app.loadDir
	elif base and base == ".":
		base = g.top().openDirectory

	# g.trace(base)
	if base and len(base) > 0 and g.os_path_isabs(base):
		return base # base need not exist yet.
	else:
		return "" # No relative base given.
#@-node:ekr.20031218072017.1264:getBaseDirectory
#@+node:ekr.20031218072017.3119:makeAllNonExistentDirectories
# This is a generalization of os.makedir.

def makeAllNonExistentDirectories (dir):

	"""Attempt to make all non-existent directories"""

	if not app.config.create_nonexistent_directories:
		return None

	dir1 = dir = g.os_path_normpath(dir)

	# Split dir into all its component parts.
	paths = []
	while len(dir) > 0:
		head,tail=g.os_path_split(dir)
		if len(tail) == 0:
			paths.append(head)
			break
		else:
			paths.append(tail)
			dir = head
	path = ""
	paths.reverse()
	for s in paths:
		path = g.os_path_join(path,s)
		if not g.os_path_exists(path):
			try:
				os.mkdir(path)
				g.es("created directory: "+path)
			except:
				g.es("exception creating directory: "+path)
				g.es_exception()
				return None
	return dir1 # All have been created.
#@nonl
#@-node:ekr.20031218072017.3119:makeAllNonExistentDirectories
#@+node:ekr.20031218072017.3120:readlineForceUnixNewline (Steven P. Schaefer)
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
#@-node:ekr.20031218072017.3120:readlineForceUnixNewline (Steven P. Schaefer)
#@+node:ekr.20031218072017.3124:sanitize_filename
def sanitize_filename(s):

	"""Prepares string s to be a valid file name:
	
	- substitute '_' whitespace and characters used special path characters.
	- eliminate all other non-alphabetic characters.
	- strip leading and trailing whitespace.
	- return at most 128 characters."""

	result = ""
	for ch in s.strip():
		if ch in string.ascii_letters:
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
#@-node:ekr.20031218072017.3124:sanitize_filename
#@+node:ekr.20031218072017.3125:shortFileName
def shortFileName (fileName):
	
	return g.os_path_basename(fileName)
#@nonl
#@-node:ekr.20031218072017.3125:shortFileName
#@+node:ekr.20031218072017.1241:update_file_if_changed
def update_file_if_changed(file_name,temp_name):

	"""Compares two files.
	
	If they are different, we replace file_name with temp_name.
	Otherwise, we just delete temp_name.
	Both files should be closed."""

	if g.os_path_exists(file_name):
		import filecmp
		if filecmp.cmp(temp_name, file_name):
			try: # Just delete the temp file.
				os.remove(temp_name)
			except: pass
			g.es("unchanged: " + file_name)
		else:
			try:
				# 10/6/02: retain the access mode of the previous file,
				# removing any setuid, setgid, and sticky bits.
				mode = (os.stat(file_name))[0] & 0777
			except:
				mode = None
			try: # Replace file with temp file.
				os.remove(file_name)
				g.utils_rename(temp_name, file_name)
				if mode: # 10/3/02: retain the access mode of the previous file.
					os.chmod(file_name,mode)
				g.es("***updating: " + file_name)
			except:
				g.es("Rename failed: no file created!",color="red")
				g.es(file_name," may be read-only or in use")
				g.es_exception()
	else:
		try:
			# os.rename(temp_name, file_name)
			g.utils_rename(temp_name, file_name)
			g.es("creating: " + file_name)
		except:
			g.es("rename failed: no file created!",color="red")
			g.es(file_name," may be read-only or in use")
			g.es_exception()
#@-node:ekr.20031218072017.1241:update_file_if_changed
#@+node:ekr.20031218072017.1263:utils_rename
# os.rename may fail on some Unix flavors if src and dst are on different filesystems.

def utils_rename(src,dst):

	"""Platform-independent rename."""
	
	head,tail=g.os_path_split(dst)
	if head and len(head) > 0:
		g.makeAllNonExistentDirectories(head)
	
	if sys.platform=="win32":
		os.rename(src,dst)
	else:
		from distutils.file_util import move_file
		move_file(src,dst)
#@nonl
#@-node:ekr.20031218072017.1263:utils_rename
#@-node:ekr.20031218072017.3116:Files & Directories...
#@+node:ekr.20031218072017.3121:redirecting stderr and stdout
class redirectClass:
	#@	<< redirectClass methods >>
	#@+node:ekr.20031218072017.1656:<< redirectClass methods >>
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
		# g.trace(s)
		if self.old:
			if app.log: app.log.put(s)
			else: self.old.write(s)
		else: print s # Typically will not happen.
	#@-node:ekr.20031218072017.1656:<< redirectClass methods >>
	#@nl

# Create two redirection objects, one for each stream.
redirectStdErrObj = redirectClass()
redirectStdOutObj = redirectClass()

#@<< define convenience methods for redirecting streams >>
#@+node:ekr.20031218072017.3122:<< define convenience methods for redirecting streams >>
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
#@-node:ekr.20031218072017.3122:<< define convenience methods for redirecting streams >>
#@nl

if 0: # Test code: may be safely and conveniently executed in the child node.
	#@	<< test code >>
	#@+node:ekr.20031218072017.3123:<< test code >>
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", g.stdOutIsRedirected()
	print "stderr isRedirected:", g.stdErrIsRedirected()
	
	from leoGlobals import redirectStderr,redirectStdout
	g.redirectStderr()
	g.redirectStdout()
	
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", g.stdOutIsRedirected()
	print "stderr isRedirected:", g.stdErrIsRedirected()
	
	from leoGlobals import restoreStderr
	g.restoreStderr()
	
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", g.stdOutIsRedirected()
	print "stderr isRedirected:", g.stdErrIsRedirected()
	
	from leoGlobals import restoreStdout
	g.restoreStdout()
	
	from leoGlobals import stdErrIsRedirected,stdOutIsRedirected
	print "stdout isRedirected:", g.stdOutIsRedirected()
	print "stderr isRedirected:", g.stdErrIsRedirected()
	#@nonl
	#@-node:ekr.20031218072017.3123:<< test code >>
	#@nl
#@nonl
#@-node:ekr.20031218072017.3121:redirecting stderr and stdout
#@+node:ekr.20031218072017.3127:get_line & get_line_after
# Very useful for tracing.

def get_line (s,i):

	nl = ""
	if g.is_nl(s,i):
		i = g.skip_nl(s,i)
		nl = "[nl]"
	j = g.find_line_start(s,i)
	k = g.skip_to_end_of_line(s,i)
	return nl + s[j:k]
	
def get_line_after (s,i):
	
	nl = ""
	if g.is_nl(s,i):
		i = g.skip_nl(s,i)
		nl = "[nl]"
	k = g.skip_to_end_of_line(s,i)
	return nl + s[i:k]
#@-node:ekr.20031218072017.3127:get_line & get_line_after
#@+node:ekr.20031218072017.3128:pause
def pause (s):
	
	print s
	
	i = 0
	while i < 1000000L:
		i += 1
#@nonl
#@-node:ekr.20031218072017.3128:pause
#@+node:ekr.20031218072017.3129:Sherlock... (trace)
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
# g.trace(string) prints string if tracing for f has been enabled.  For 
# example, the following statment prints from s[i] to the end of the line if 
# tracing for f has been enabled.
# 
#   j = g.skip_line(s,i) ; g.trace(s[i:j])
# 
# g.trace(function) exectutes the function if tracing for f has been enabled.  
# For example,
# 
#   g.trace(self.f2)
# 
# You enable and disable tracing by calling g.init_trace(args).  Examples:
# 
#   g.init_trace("+*")         # enable all traces
#   g.init_trace("+a","+b")    # enable traces for a and b
#   g.init_trace(("+a","+b"))  # enable traces for a and b
#   g.init_trace("-a")         # disable tracing for a
#   traces = g.init_trace("?") # return the list of enabled traces
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
#   g.trace_tag("-nocolor", self.disable_color)
#@-at
#@+node:ekr.20031218072017.3130:init_sherlock
# Called by startup code.
# Args are all the arguments on the command line.

def init_sherlock (args):
	
	g.init_trace(args,echo=0)
	# g.trace("sys.argv:",sys.argv)
#@nonl
#@-node:ekr.20031218072017.3130:init_sherlock
#@+node:ekr.20031218072017.3131:get_Sherlock_args
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
			fn = g.os_path_join(app.loadDir,"SherlockArgs")
			f = open(fn)
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
#@-node:ekr.20031218072017.3131:get_Sherlock_args
#@+node:ekr.20031218072017.3132:init_trace
def init_trace(args,echo=1):

	t = app.trace_list
	args = g.get_Sherlock_args(args)

	for arg in args:
		if arg[0] in string.ascii_letters: prefix = '+'
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
#@-node:ekr.20031218072017.3132:init_trace
#@+node:ekr.20031218072017.2317:trace
# Convert all args to strings.
# Print if tracing for the presently executing function has been enabled.

def trace (*args,**keys):
	
	callers = keys.get("callers",false)

	s = ""
	for arg in args:
		if type(arg) == type(u""):
			try:    arg = str(arg)
			except: arg = repr(arg)
		elif type(arg) != type(""):
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
		traceback.print_stack()
		
	if 1: # Print all traces.
		print name + ": " + message
	else: # Print only enabled traces.
		t = app.trace_list
		# tracepoint names starting with '-' must match exactly.
		minus = len(name) > 0 and name[0] == '-'
		if minus: name = name[1:]
		if (not minus and '*' in t) or name.lower() in t:
			s = name + ": " + message
			print s # Traces _always_ get printed.
#@-node:ekr.20031218072017.2317:trace
#@+node:ekr.20031218072017.2318:trace_tag
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

	t = app.trace_list
	# tracepoint names starting with '-' must match exactly.
	minus = len(name) > 0 and name[0] == '-'
	if minus: name = name[1:]
	if (not minus and '*' in t) or name.lower() in t:
		s = name + ": " + message
		print s # Traces _always_ get printed.
#@nonl
#@-node:ekr.20031218072017.2318:trace_tag
#@-node:ekr.20031218072017.3129:Sherlock... (trace)
#@+node:ekr.20031218072017.3133:Statistics
#@+node:ekr.20031218072017.3134:clear_stats
def clear_stats():
	
	app.stats = {}
#@-node:ekr.20031218072017.3134:clear_stats
#@+node:ekr.20031218072017.3135:print_stats
def print_stats (name=None):
	
	if name:
		if type(name) != type(""):
			name = repr(name)
	else:
		name = g.callerName(n=2) # Get caller name 2 levels back.
	
	try:
		stats = app.stats
	except:
		print ; print "no statistics at", name ; print
		return
		
	items = stats.items()
	items.sort()
	print ; print "statistics at",name ; print
	for key,value in items:
		print key,value
		
	g.clear_stats()
#@-node:ekr.20031218072017.3135:print_stats
#@+node:ekr.20031218072017.3136:stat
def stat (name=None):

	"""Increments the statistic for name in app.stats
	The caller's name is used by default.
	"""
	
	if name:
		if type(name) != type(""):
			name = repr(name)
	else:
		name = g.callerName(n=2) # Get caller name 2 levels back.

	try:
		stats = app.stats
	except:
		app.stats = stats = {}

	stats[name] = 1 + stats.get(name,0)
#@-node:ekr.20031218072017.3136:stat
#@-node:ekr.20031218072017.3133:Statistics
#@+node:ekr.20031218072017.3137:Timing
# pychecker bug: pychecker complains that there is no attribute time.clock

def getTime():
	return time.clock()
	
def esDiffTime(message, start):
	g.es("%s %6.3f" % (message,(time.clock()-start)))
	return time.clock()
	
def printDiffTime(message, start):
	print "%s %6.3f" % (message,(time.clock()-start))
	return time.clock()
#@nonl
#@-node:ekr.20031218072017.3137:Timing
#@-node:ekr.20031218072017.3104:Debugging, Dumping, Timing, Tracing & Sherlock
#@+node:ekr.20040331083824.1:fileLikeObject
class fileLikeObject:
	
	"""Define a file-like object for redirecting i/o."""
	
	# Used by Execute Script command and rClick plugin.
	
	def __init__(self): self.s = ""
	def clear (self):   self.s = ""
	def close (self):   pass
	def flush (self):   pass
		
	def get (self):
		return self.s
		
	def write (self,s):
		if s:
			self.s = self.s + s
#@nonl
#@-node:ekr.20040331083824.1:fileLikeObject
#@+node:ekr.20031218072017.3126:funcToMethod
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
	# g.trace(name)
#@nonl
#@-node:ekr.20031218072017.3126:funcToMethod
#@+node:ekr.20031218072017.3138:executeScript
def executeScript (name):
	
	"""Execute a script whose short python file name is given"""
	
	mod_name,ext = g.os_path_splitext(name)
	file = None
	try:
		# This code is in effect an import or a reload.
		# This allows the user to modify scripts without leaving Leo.
		import imp
		file,filename,description = imp.find_module(mod_name)
		imp.load_module(mod_name,file,filename,description)
	except:
		g.es("Exception executing " + name,color="red")
		g.es_exception()

	if file:
		file.close()

#@-node:ekr.20031218072017.3138:executeScript
#@+node:ekr.20031218072017.1588:Garbage Collection
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
#@+node:ekr.20031218072017.1589:clearAllIvars
def clearAllIvars (o):
	
	"""Clear all ivars of o, a member of some class."""
	
	o.__dict__.clear()
#@-node:ekr.20031218072017.1589:clearAllIvars
#@+node:ekr.20031218072017.1590:collectGarbage
def collectGarbage(message=None):
	
	if not debugGC: return
	
	if not message:
		message = g.callerName(n=2)
	
	try: gc.collect()
	except: pass
	
	if 1:
		g.printGc(message)
	
	if 0: # This isn't needed unless we want to look at individual objects.
	
		#@		<< make a list of the new objects >>
		#@+node:ekr.20031218072017.1591:<< make a list of the new objects >>
		# WARNING: the id trick is not proper because newly allocated objects can have the same address as old objets.
		
		global lastObjectsDict
		objects = gc.get_objects()
		
		newObjects = [o for o in objects if not lastObjectsDict.has_key(id(o))]
		
		lastObjectsDict = {}
		for o in objects:
			lastObjectsDict[id(o)]=o
		#@nonl
		#@-node:ekr.20031218072017.1591:<< make a list of the new objects >>
		#@nl
		print "%25s: %d new, %d total objects" % (message,len(newObjects),len(objects))
#@-node:ekr.20031218072017.1590:collectGarbage
#@+node:ekr.20031218072017.1592:printGc
def printGc(message=None,onlyPrintChanges=false):
	
	if not debugGC: return None
	
	if not message:
		message = g.callerName(n=2)
	
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
#@-node:ekr.20031218072017.1592:printGc
#@+node:ekr.20031218072017.1593:printGcRefs
def printGcRefs (verbose=true):

	refs = gc.get_referrers(app.windowList[0])
	print '-' * 30

	if verbose:
		print "refs of", app.windowList[0]
		for ref in refs:
			print type(ref)
	else:
		print "%d referers" % len(refs)
#@nonl
#@-node:ekr.20031218072017.1593:printGcRefs
#@-others
#@-node:ekr.20031218072017.1588:Garbage Collection
#@+node:ekr.20031218072017.3139:Hooks & plugins (leoGlobals)
#@+node:ekr.20031218072017.1315:enableIdleTimeHook, disableIdleTimeHook, idleTimeHookHandler
#@+at 
#@nonl
# Enables the "idle" hook.
# After enableIdleTimeHook is called, Leo will call the "idle" hook
# approximately every idleTimeDelay milliseconds.
#@-at
#@@c
def enableIdleTimeHook(idleTimeDelay=100):
	app.idleTimeHook = true
	app.idleTimeDelay = idleTimeDelay # Delay in msec.
	app.gui.setIdleTimeHook(idleTimeHookHandler)
	
# Disables the "idle" hook.
def disableIdleTimeHook():
	app.idleTimeHook = false
	
# An internal routine used to dispatch the "idle" hook.
trace_count = 0
def idleTimeHookHandler(*args,**keys):
	
	if 0:
		global trace_count ; trace_count += 1
		if trace_count % 10 == 0: g.trace(trace_count)

	# New for Python 2.3: may be called during shutdown.
	if app.killed: return
	c = g.top()
	if c: v = c.currentVnode()
	else: v = None
	g.doHook("idle",c=c,v=v)
	# Requeue this routine after 100 msec.  Faster requeues overload the system.
	if app.idleTimeHook:
		app.gui.setIdleTimeHookAfterDelay(app.idleTimeDelay,idleTimeHookHandler)
		app.afterHandler = idleTimeHookHandler
	else:
		app.afterHandler = None
#@nonl
#@-node:ekr.20031218072017.1315:enableIdleTimeHook, disableIdleTimeHook, idleTimeHookHandler
#@+node:ekr.20031218072017.1596:frame.doHook
#@+at 
#@nonl
# This global function calls a hook routine.  Hooks are identified by the tag 
# param.
# Returns the value returned by the hook routine, or None if the there is an 
# exception.
# 
# We look for a hook routine in three places:
# 1. g.top().hookFunction
# 2. app.hookFunction
# 3. leoPlugins.doPlugins()
# We set app.hookError on all exceptions.  Scripts may reset app.hookError to 
# try again.
#@-at
#@@c

def doHook(tag,*args,**keywords):

	c = g.top() # c may be None during startup.
	
	if app.killed or app.hookError:
		return None
	elif not app.config.use_plugins:
		if tag == "start1":
			g.es("Plugins disabled: use_plugins is 0",color="blue")
		return None
	elif c and c.hookFunction:
		try:
			return c.hookFunction(tag,keywords)
		except:
			g.es("exception in c.hookFunction for " + c.frame.getTitle())
	elif app.hookFunction:
		try:
			return app.hookFunction(tag,keywords)
		except:
			g.es("exception in app.hookFunction")
	else:
		import leoPlugins
		try:
			app.hookFunction = leoPlugins.doPlugins
			return app.hookFunction(tag,keywords)
		except:
			app.hookFunction = None
			g.es("exception in plugin")

	# Handle all exceptions.
	g.es_exception()
	app.hookError = true # Supress this function.
	app.idleTimeHook = false # Supress idle-time hook
	return None # No return value
#@nonl
#@-node:ekr.20031218072017.1596:frame.doHook
#@+node:ekr.20031218072017.1318:plugin_signon
def plugin_signon(module_name,verbose=false):
	
	exec("import %s ; m = %s" % (module_name,module_name))
	
	if verbose:
		g.es("...%s.py v%s: %s" % (
			m.__name__, m.__version__, g.plugin_date(m)))

		print m.__name__, m.__version__
		
	app.loadedPlugins.append(module_name)
#@nonl
#@-node:ekr.20031218072017.1318:plugin_signon
#@-node:ekr.20031218072017.3139:Hooks & plugins (leoGlobals)
#@+node:ekr.20031218072017.2278:importFromPath
def importFromPath (name,path):
	
	import imp

	try:
		file = None ; result = None
		try:
			fn = g.shortFileName(name)
			mod_name,ext = g.os_path_splitext(fn)
			path = g.os_path_normpath(path)
			if g.CheckVersion(sys.version,"2.3"):
				path = g.toEncodedString(path,app.tkEncoding) # 12/01/03
			else:
				path = str(path) # 1/29/04: May throw exception.
			# g.trace(path)
			data = imp.find_module(mod_name,[path]) # This can open the file.
			if data:
				file,pathname,description = data
				result = imp.load_module(mod_name,file,pathname,description)
		except:
			g.es_exception()

	# Bug fix: 6/12/03: Put no return statements before here!
	finally: 
		if file: file.close()

	return result
#@nonl
#@-node:ekr.20031218072017.2278:importFromPath
#@+node:ekr.20031218072017.3140:Lists...
#@+node:ekr.20031218072017.3141:appendToList
def appendToList(out, s):

	for i in s:
		out.append(i)
#@nonl
#@-node:ekr.20031218072017.3141:appendToList
#@+node:ekr.20031218072017.3142:flattenList
def flattenList (theList):

	result = []
	for item in theList:
		if type(item) == types.ListType:
			result.extend(g.flattenList(item))
		else:
			result.append(item)
	return result
#@nonl
#@-node:ekr.20031218072017.3142:flattenList
#@+node:ekr.20031218072017.3143:listToString
def listToString(theList):

	if list:
		theList = g.flattenList(theList)
		return string.join(theList,"")
	else:
		return ""
#@nonl
#@-node:ekr.20031218072017.3143:listToString
#@-node:ekr.20031218072017.3140:Lists...
#@+node:ekr.20031218072017.3144:makeDict
# From the Python cookbook.

def makeDict(**keys):
	
	"""Returns a Python dictionary from using the optional keyword arguments."""

	return keys
#@nonl
#@-node:ekr.20031218072017.3144:makeDict
#@+node:ekr.20031218072017.3145:Most common functions...
# These are guaranteed always to exist for scripts.
#@+node:ekr.20031218072017.3146:app & leoProxy (no longer used)
if 0: # No longer needed with the new import scheme.

	class leoProxy:
	
		"""A proxy for the gApp object that can be created before gApp itself.
		
		After gApp is created, both app.x and app().x refer to gApp.x."""
	
		def __getattr__(self,attr):
			return getattr(gApp,attr)
			
		def __setattr__(self,attr,val):
			setattr(gApp,attr,val)
	
		def __call__(self):
			return gApp
			
	# The code can use app.x and app().x to refer to ivars of the leoApp class.
	app = leoProxy()
#@nonl
#@-node:ekr.20031218072017.3146:app & leoProxy (no longer used)
#@+node:ekr.20031218072017.3147:choose
def choose(cond, a, b): # warning: evaluates all arguments

	if cond: return a
	else: return b
#@nonl
#@-node:ekr.20031218072017.3147:choose
#@+node:ekr.20031218072017.1474:es, enl, ecnl
def ecnl():
	g.ecnls(1)

def ecnls(n):
	log = app.log
	if log:
		while log.newlines < n:
			g.enl()

def enl():
	log = app.log
	if log:
		log.newlines += 1
		log.putnl()

def es(s,*args,**keys):
	if app.killed:
		return
	newline = keys.get("newline",true)
	color = keys.get("color",None)
	if type(s) != type("") and type(s) != type(u""): # 1/20/03
		s = repr(s)
	for arg in args:
		if type(arg) != type("") and type(arg) != type(u""): # 1/20/03
			arg = repr(arg)
		s = s + ", " + arg
	if app.batchMode:
		if app.log:
			app.log.put(s)
	else:
		log = app.log
		if log:
			log.put(s,color=color)
			for ch in s:
				if ch == '\n': log.newlines += 1
				else: log.newlines = 0
			if newline:
				g.ecnl() # only valid here
		elif newline:
			app.logWaiting.append((s+'\n',color),) # 2/16/03
			print s
		else:
			app.logWaiting.append((s,color),) # 2/16/03
			print s,
#@nonl
#@-node:ekr.20031218072017.1474:es, enl, ecnl
#@+node:ekr.20031218072017.3148:top
#@+at 
#@nonl
# c.doCommand and frame.OnMenuClick now set app.log, so g.top() will be 
# reliable after any command is executed.
# 
# Note 1: The value of g.top() may change during a new or open command, which 
# may change the routine used to execute the "command1" and "command2" hooks.  
# This is not a bug, and hook routines must be aware of this fact.
#@-at
#@@c

def top():
	
	"""Return the commander of the topmost window"""
	
	# Warning: may be called during startup or shutdown when nothing exists.
	try:
		return app.log.c
	except:
		return None
#@nonl
#@-node:ekr.20031218072017.3148:top
#@+node:ekr.20031218072017.3149:trace is defined below
#@-node:ekr.20031218072017.3149:trace is defined below
#@+node:ekr.20031218072017.3150:windows
def windows():
	return app.windowList
#@nonl
#@-node:ekr.20031218072017.3150:windows
#@-node:ekr.20031218072017.3145:Most common functions...
#@+node:ekr.20031218072017.2145:os.path wrappers (leoGlobals.py)
#@+node:ekr.20031218072017.2146:os_path_abspath
def os_path_abspath(path,encoding=None):
	
	"""Convert a path to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	path = os.path.abspath(path)
	
	path = g.toUnicodeFileEncoding(path,encoding)
	
	return path
#@nonl
#@-node:ekr.20031218072017.2146:os_path_abspath
#@+node:ekr.20031218072017.2147:os_path_basename
def os_path_basename(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	path = os.path.basename(path)
	
	path = g.toUnicodeFileEncoding(path,encoding)
	
	return path
#@nonl
#@-node:ekr.20031218072017.2147:os_path_basename
#@+node:ekr.20031218072017.2148:os_path_dirname
def os_path_dirname(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	path = os.path.dirname(path)
	
	path = g.toUnicodeFileEncoding(path,encoding)
	
	return path
#@nonl
#@-node:ekr.20031218072017.2148:os_path_dirname
#@+node:ekr.20031218072017.2149:os_path_exists
def os_path_exists(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	return os.path.exists(path)
#@nonl
#@-node:ekr.20031218072017.2149:os_path_exists
#@+node:ekr.20031218072017.2150:os_path_getmtime
def os_path_getmtime(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	return os.path.getmtime(path)
#@nonl
#@-node:ekr.20031218072017.2150:os_path_getmtime
#@+node:ekr.20031218072017.2151:os_path_isabs
def os_path_isabs(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	return os.path.isabs(path)
#@nonl
#@-node:ekr.20031218072017.2151:os_path_isabs
#@+node:ekr.20031218072017.2152:os_path_isdir (not used)
def os_path_isdir(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	return os.path.isdir(path)
#@nonl
#@-node:ekr.20031218072017.2152:os_path_isdir (not used)
#@+node:ekr.20031218072017.2153:os_path_isfile
def os_path_isfile(path,encoding=None):
	
	"""Normalize the path and convert it to an absolute path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	return os.path.isfile(path)
#@nonl
#@-node:ekr.20031218072017.2153:os_path_isfile
#@+node:ekr.20031218072017.2154:os_path_join
def os_path_join(*args,**keys):
	
	encoding = keys.get("encoding")

	uargs = [g.toUnicodeFileEncoding(arg,encoding) for arg in args]

	path = os.path.join(*uargs)
	
	path = g.toUnicodeFileEncoding(path,encoding)

	return path
#@nonl
#@-node:ekr.20031218072017.2154:os_path_join
#@+node:ekr.20031218072017.2155:os_path_norm
def os_path_norm(path,encoding=None):
	
	"""Normalize both the path and the case."""

	path = g.toUnicodeFileEncoding(path,encoding)

	path = os.path.normcase(path)
	path = os.path.normpath(path)
	
	path = g.toUnicodeFileEncoding(path,encoding)
	
	return path
#@nonl
#@-node:ekr.20031218072017.2155:os_path_norm
#@+node:ekr.20031218072017.2156:os_path_normcase
def os_path_normcase(path,encoding=None):
	
	"""Normalize the path's case."""

	path = g.toUnicodeFileEncoding(path,encoding)

	path = os.path.normcase(path)
	
	path = g.toUnicodeFileEncoding(path,encoding)
	
	return path
#@nonl
#@-node:ekr.20031218072017.2156:os_path_normcase
#@+node:ekr.20031218072017.2157:os_path_normpath
def os_path_normpath(path,encoding=None):
	
	"""Normalize the path."""

	path = g.toUnicodeFileEncoding(path,encoding)

	path = os.path.normpath(path)
	
	path = g.toUnicodeFileEncoding(path,encoding)
	
	return path
#@nonl
#@-node:ekr.20031218072017.2157:os_path_normpath
#@+node:ekr.20031218072017.2158:os_path_split
def os_path_split(path,encoding=None):
	
	path = g.toUnicodeFileEncoding(path,encoding)

	head,tail = os.path.split(path)

	head = g.toUnicodeFileEncoding(head,encoding)
	tail = g.toUnicodeFileEncoding(tail,encoding)

	return head,tail
#@nonl
#@-node:ekr.20031218072017.2158:os_path_split
#@+node:ekr.20031218072017.2159:os_path_splitext
def os_path_splitext(path,encoding=None):

	path = g.toUnicodeFileEncoding(path,encoding)

	head,tail = os.path.splitext(path)

	head = g.toUnicodeFileEncoding(head,encoding)
	tail = g.toUnicodeFileEncoding(tail,encoding)

	return head,tail
#@nonl
#@-node:ekr.20031218072017.2159:os_path_splitext
#@+node:ekr.20031218072017.2160:toUnicodeFileEncoding
def toUnicodeFileEncoding(path,encoding):

	if not encoding:
		if sys.platform == "win32":
			encoding = "mbcs"
		else:
			encoding = app.tkEncoding

	return g.toUnicode(path,encoding)
#@nonl
#@-node:ekr.20031218072017.2160:toUnicodeFileEncoding
#@-node:ekr.20031218072017.2145:os.path wrappers (leoGlobals.py)
#@+node:EKR.20040504150046:class mulderUpdateAlgorithm (leoGlobals)
import difflib,shutil

class mulderUpdateAlgorithm:
	
	"""A class to update derived files using
	diffs in files without sentinels."""
	
	#@	@+others
	#@+node:EKR.20040504150046.3:__init__
	def __init__ (self):
		
		self.testing = false
		self.do_backups = false
	#@nonl
	#@-node:EKR.20040504150046.3:__init__
	#@+node:EKR.20040504150046.9:copy_sentinels
	#@+at 
	#@nonl
	# This script retains _all_ sentinels.  If lines are replaced, or deleted,
	# we restore deleted sentinel lines by checking for gaps in the mapping.
	#@-at
	#@@c
	
	def copy_sentinels (self,write_lines,fat_lines,fat_pos,mapping,startline,endline):
		"""
		
		Copy sentinel lines from fat_lines to write_lines.
	
		Copy all sentinels _after_ the current reader postion up to,
		but not including, mapping[endline].
	
		"""
	
		j_last = mapping[startline]
		i = startline + 1
		while i <= endline:
			j = mapping[i]
			if j_last + 1 != j:
				fat_pos = j_last + 1
				# Copy the deleted sentinels that comprise the gap.
				while fat_pos < j:
					line = fat_lines[fat_pos]
					write_lines.append(line)
					if self.testing: print "Copy sentinel:",fat_pos,line,
					fat_pos += 1
			j_last = j ; i += 1
	
		fat_pos = mapping[endline]
		return fat_pos
	#@nonl
	#@-node:EKR.20040504150046.9:copy_sentinels
	#@+node:EKR.20040504155109:copy_time
	def copy_time(self,sourcefilename,targetfilename):
		
		"""
		Set the target file's modification time to
		that of the source file.
		"""
	
		st = os.stat(sourcefilename)
		if hasattr(os, 'utime'):
			os.utime(targetfilename, (st.st_atime, st.st_mtime))
		elif hasattr(os, 'mtime'):
			os.mtime(targetfilename, st.st_mtime)
		else:
			g.trace("Can not set modification time")
	#@nonl
	#@-node:EKR.20040504155109:copy_time
	#@+node:EKR.20040504150046.6:create_mapping
	def create_mapping (self,lines,marker):
		"""
	
		'lines' is a list of lines of a file with sentinels.
	 
		Returns:
	
		result: lines with all sentinels removed.
	
		mapping: a list such that result[mapping[i]] == lines[i]
		for all i in range(len(result))
	
		"""
	
		mapping = [] ; result = []
		for i in xrange(len(lines)):
			line = lines[i]
			if not self.is_sentinel(line,marker):
				result.append(line)
				mapping.append(i)
	
		# Create a last mapping entry for copy_sentinels.
		mapping.append(i)
	
		return result, mapping
	#@nonl
	#@-node:EKR.20040504150046.6:create_mapping
	#@+node:EKR.20040504154039:is_sentinel NOT CORRECT
	def is_sentinel (self,line,marker):
		
		"""
		Check if line starts with a sentinel comment.
		"""
		
		return line.lstrip().startswith(marker)
	#@-node:EKR.20040504154039:is_sentinel NOT CORRECT
	#@+node:EKR.20040504150046.4:marker_from_extension
	def marker_from_extension(self,filename):
		"""
		Tries to guess the sentinel leadin
		comment from the filename extension.
		
		This code should probably be shared
		with the main Leo code.
		"""
		root, ext = os.path.splitext(filename)
		if ext == '.tmp':
			root, ext = os.path.splitext(root)
		if ext in ('.h', '.c'):
			marker = "//@"
		elif ext in (".py", ".cfg", ".bat", ".ksh"):
			marker = "#@"
		else:
			g.trace("unknown extension %s" % ext)
			marker = None
	
		return marker
	#@nonl
	#@-node:EKR.20040504150046.4:marker_from_extension
	#@+node:EKR.20040505080156:Get or remove sentinel lines
	# These routines originally were part of push_filter & push_filter_lines.
	#@nonl
	#@+node:EKR.20040505081121:separateSentinelsFromFile/Lines
	def separateSentinelsFromFile (self,filename):
		
		"""Separate the lines of the file into a tuple of two lists,
		containing the sentinel and non-sentinel lines of the file."""
		
		lines = file(filename).readlines()
		marker = self.marker_from_extension(filename)
		
		return self.separateSentinelsFromLines(lines,marker)
		
	def separateSentinelsFromLines (self,lines,marker):
		
		"""Separate lines (a list of lines) into a tuple of two lists,
		containing the sentinel and non-sentinel lines of the original list."""
		
		strippedLines = self.removeSentinelsFromLines(lines,marker)
		sentinelLines = self.getSentinelsFromLines(lines,marker)
		
		return strippedLines,sentinelLines
	#@nonl
	#@-node:EKR.20040505081121:separateSentinelsFromFile/Lines
	#@+node:EKR.20040505080156.2:removeSentinelsFromFile/Lines
	def removeSentinelsFromFile (self,filename):
		
		"""Return a copy of file with all sentinels removed."""
		
		lines = file(filename).readlines()
		marker = self.marker_from_extension(filename)
		
		return removeSentinelsFromLines(lines,marker)
		
	def removeSentinelsFromLines (self,lines,marker):
	
		"""Return a copy of lines with all sentinels removed."""
		
		return [line for line in lines if not self.is_sentinel(line,marker)]
	#@nonl
	#@-node:EKR.20040505080156.2:removeSentinelsFromFile/Lines
	#@+node:EKR.20040505080156.3:getSentinelsFromFile/Lines
	def getSentinelsFromFile (self,filename,marker):
		
		"""Returns all sentinels lines in a file."""
		
		lines = file(filename).readlines()
		marker = self.marker_from_extension(filename)
	
		return getSentinelsFromLines(lines,marker)
		
	def getSentinelsFromLines (self,lines,marker):
		
		"""Returns all sentinels lines in lines."""
		
		return [line for line in lines if self.is_sentinel(line,marker)]
	#@nonl
	#@-node:EKR.20040505080156.3:getSentinelsFromFile/Lines
	#@-node:EKR.20040505080156:Get or remove sentinel lines
	#@+node:EKR.20040504150046.10:propagateDiffsToSentinelsFile (was pull_source)
	def propagateDiffsToSentinelsFile(self,sourcefilename,targetfilename):
		
		#@	<< init propagateDiffsToSentinelsFile vars >>
		#@+node:EKR.20040504150046.11:<< init propagateDiffsToSentinelsFile vars >>
		# Get the sentinel comment marker.
		marker = self.marker_from_extension(sourcefilename)
		if not marker:
			return
		
		try:
			# Create the readers.
			sfile = file(sourcefilename)
			tfile = file(targetfilename)
			
			fat_lines = sfile.readlines() # Contains sentinels.
			j_lines   = tfile.readlines() # No sentinels.
			
			i_lines,mapping = self.create_mapping(fat_lines,marker)
			
			sfile.close()
			tfile.close()
		except:
			g.es_exception("can not open files")
			return
		#@nonl
		#@-node:EKR.20040504150046.11:<< init propagateDiffsToSentinelsFile vars >>
		#@nl
		
		write_lines = self.propagateDiffsToSentinelsLines(
			i_lines,j_lines,fat_lines,mapping)
			
		# Update _source_ file if it is not the same as write_lines.
		written = self.write_if_changed(write_lines,targetfilename,sourcefilename)
		if written:
			#@		<< paranoia check>>
			#@+node:EKR.20040504150046.12:<<paranoia check>>
			# Check that 'push' will re-create the changed file.
			strippedLines,sentinel_lines = self.separateSentinelsFromFile(sourcefilename)
			
			if strippedLines != j_lines:
				self.report_mismatch(strippedLines, j_lines,
					"Propagating diffs did not work as expected",
					"Content of sourcefile:",
					"Content of modified file:")
			
			# Check that no sentinels got lost.
			fat_sentinel_lines = self.getSentinelsFromLines(fat_lines,marker)
			
			if sentinel_lines != fat_sentinel_lines:
				self.report_mismatch(sentinel_lines,fat_sentinel_lines,
					"Propagating diffs modified sentinel lines:",
					"Current sentinel lines:",
					"Old sentinel lines:")
			#@nonl
			#@-node:EKR.20040504150046.12:<<paranoia check>>
			#@nl
	#@nonl
	#@-node:EKR.20040504150046.10:propagateDiffsToSentinelsFile (was pull_source)
	#@+node:EKR.20040504145804.1:propagateDiffsToSentinelsLines
	def propagateDiffsToSentinelsLines (self,i_lines,j_lines,fat_lines,mapping):
		
		"""Compare the 'i_lines' with 'j_lines' and propagate the diffs back into
		'write_lines' making sure that all sentinels of 'fat_lines' are copied.
	
		i/j_lines have no sentinels.  fat_lines does."""
	
		#@	<< init propagateDiffsToSentinelsLines vars >>
		#@+node:EKR.20040504145804.2:<< init propagateDiffsToSentinelsLines vars >>
		# Indices into i_lines, j_lines & fat_lines.
		i_pos = j_pos = fat_pos = 0
		
		# These vars check that all ranges returned by get_opcodes() are contiguous.
		i2_old = j2_old = -1
		
		# Create the output lines.
		write_lines = []
		
		matcher = difflib.SequenceMatcher(None,i_lines,j_lines)
		
		testing = self.testing
		#@nonl
		#@-node:EKR.20040504145804.2:<< init propagateDiffsToSentinelsLines vars >>
		#@nl
		#@	<< copy the sentinels at the beginning of the file >>
		#@+node:EKR.20040504145804.3:<< copy the sentinels at the beginning of the file >>
		while fat_pos < mapping[0]:
			line = fat_lines[fat_pos]
			write_lines.append(line)
			if testing: print "copy initial line",fat_pos,line,
			fat_pos += 1
		#@nonl
		#@-node:EKR.20040504145804.3:<< copy the sentinels at the beginning of the file >>
		#@nl
		for tag, i1, i2, j1, j2 in matcher.get_opcodes():
			if testing:
				print ; print "Opcode",tag,i1,i2,j1,j2 ; print
			#@		<< update and check the loop invariant >>
			#@+node:EKR.20040504145804.4:<< update and check the loop invariant>>
			# We need the ranges returned by get_opcodes to completely cover the source lines being compared.
			# We also need the ranges not to overlap.
			
			assert(i2_old in (-1,i1))
			assert(j2_old in (-1,j1))
			
			i2_old = i2 ; j2_old = j2
			
			# Check the loop invariants.
			assert i_pos == i1
			assert j_pos == j1
			assert fat_pos == mapping[i1]
			
			if 0: # not yet.
				if testing: # A bit costly.
					t_sourcelines,t_sentinel_lines = push_filter_lines(write_lines, marker)
					# Check that we have all the modifications so far.
					assert t_sourcelines == j_lines[:j1],"t_sourcelines == j_lines[:j1]"
					# Check that we kept all sentinels so far.
					assert t_sentinel_lines == push_filter_lines(fat_lines[:fat_pos], marker)[1]
			#@nonl
			#@-node:EKR.20040504145804.4:<< update and check the loop invariant>>
			#@nl
			if tag == 'equal':
				#@			<< handle 'equal' tag >>
				#@+node:EKR.20040504145804.5:<< handle 'equal' tag >>
				# Copy the lines, including sentinels.
				while fat_pos <= mapping[i2-1]:
					line = fat_lines[fat_pos]
					if 0: # too verbose.
						if testing: print "Equal: copying ", line,
					write_lines.append(line)
					fat_pos += 1
				
				if testing:
					print "Equal: synch i", i_pos,i2
					print "Equal: synch j", j_pos,j2
				
				i_pos = i2
				j_pos = j2
				
				# Copy the sentinels which might follow the lines.       
				fat_pos = self.copy_sentinels(write_lines,fat_lines,fat_pos,mapping,i2-1,i2)
				#@nonl
				#@-node:EKR.20040504145804.5:<< handle 'equal' tag >>
				#@nl
			elif tag == 'replace':
				#@			<< handle 'replace' tag >>
				#@+node:EKR.20040504145804.6:<< handle 'replace' tag >>
				#@+at 
				#@nonl
				# Replace lines that may span sentinels.
				# 
				# For now, we put all the new contents after the first 
				# sentinel.
				# 
				# A more complex approach: run the difflib across the 
				# different lines and try to
				# construct a mapping changed line => orignal line.
				#@-at
				#@@c
				
				while j_pos < j2:
					line = j_lines[j_pos]
					if testing: print "Replace:", line,
					write_lines.append(line)
					j_pos += 1
					
				i_pos = i2
				
				# Copy the sentinels which might be between the changed code.         
				fat_pos = self.copy_sentinels(write_lines,fat_lines,fat_pos,mapping,i1,i2)
				#@nonl
				#@-node:EKR.20040504145804.6:<< handle 'replace' tag >>
				#@nl
			elif tag == 'delete':
				#@			<< handle 'delete' tag >>
				#@+node:EKR.20040504145804.7:<< handle 'delete' tag >>
				if testing:
					print "delete: i",i_pos,i1
					print "delete: j",j_pos,j1
				
				j_pos = j2
				i_pos = i2
				
				# Restore any deleted sentinels.
				fat_pos = self.copy_sentinels(write_lines,fat_lines,fat_pos,mapping,i1,i2)
				#@nonl
				#@-node:EKR.20040504145804.7:<< handle 'delete' tag >>
				#@nl
			elif tag == 'insert':
				#@			<< handle 'insert' tag >>
				#@+node:EKR.20040504145804.8:<< handle 'insert' tag >>
				while j_pos < j2:
					line = j_lines[j_pos]
					if testing: print "Insert:", line,
					write_lines.append(line)
					j_pos += 1
				
				# The input streams are already in synch.
				#@nonl
				#@-node:EKR.20040504145804.8:<< handle 'insert' tag >>
				#@nl
			else: assert 0,"bad tag"
		#@	<< copy the sentinels at the end of the file >>
		#@+node:EKR.20040504145804.9:<< copy the sentinels at the end of the file >>
		while fat_pos < len(fat_lines):
			line = fat_lines[fat_pos]
			write_lines.append(line)
			if testing: print "Append last line",line
			fat_pos += 1
		#@nonl
		#@-node:EKR.20040504145804.9:<< copy the sentinels at the end of the file >>
		#@nl
		return write_lines
	#@-node:EKR.20040504145804.1:propagateDiffsToSentinelsLines
	#@+node:EKR.20040504150046.5:report_mismatch
	def report_mismatch (self,lines1,lines2,message,lines1_message,lines2_message):
	
		"""
		Generate a report when something goes wrong.
		"""
	
		print '='*20
		print message
		
		if 0:
			print lines1_message
			print '-'*20
			for line in lines1:
			  print line,
			 
			print '='*20
		
			print lines2_message
			print '-'*20
			for line in lines2:
				print line,
	#@nonl
	#@-node:EKR.20040504150046.5:report_mismatch
	#@+node:EKR.20040504160820:write_if_changed
	def write_if_changed(self,lines,sourcefilename,targetfilename):
		"""
		
		Replaces target file if it is not the same as 'lines',
		and makes the modification date of target file the same as the source file.
		
		Optionally backs up the overwritten file.
	
		"""
		
		copy = not os.path.exists(targetfilename) or lines != file(targetfilename).readlines()
			
		if self.testing:
			if copy:
				print "Writing",targetfilename,"without sentinals"
			else:
				print "Files are identical"
	
		if copy:
			if self.do_backups:
				#@			<< make backup file >>
				#@+node:EKR.20040504160820.1:<< make backup file >>
				if os.path.exists(targetfilename):
					count = 0
					backupname = "%s.~%s~" % (targetfilename,count)
					while os.path.exists(backupname):
						count += 1
						backupname = "%s.~%s~" % (targetfilename,count)
					os.rename(targetfilename, backupname)
					if testing:
						print "backup file in ", backupname
				#@nonl
				#@-node:EKR.20040504160820.1:<< make backup file >>
				#@nl
			outfile = open(targetfilename, "w")
			for line in lines:
				outfile.write(line)
			outfile.close()
			self.copy_time(sourcefilename,targetfilename)
		return copy
	#@-node:EKR.20040504160820:write_if_changed
	#@-others
	
def doMulderUpdateAlgorithm(sourcefilename,targetfilename):

	mu = mulderUpdateAlgorithm()

	mu.pull_source(sourcefilename,targetfilename)
	mu.copy_time(targetfilename,sourcefilename)
#@nonl
#@-node:EKR.20040504150046:class mulderUpdateAlgorithm (leoGlobals)
#@+node:ekr.20031218072017.3151:Scanning...
#@+node:ekr.20031218072017.3152:g.scanAtFileOptions
def scanAtFileOptions (h,err_flag=false):
	
	assert(g.match(h,0,"@file"))
	i = len("@file")
	atFileType = "@file"
	optionsList = []

	while g.match(h,i,'-'):
		#@		<< scan another @file option >>
		#@+node:ekr.20031218072017.3153:<< scan another @file option >>
		i += 1 ; err = -1
		
		if g.match_word(h,i,"asis"):
			if atFileType == "@file":
				atFileType = "@silentfile"
			elif err_flag:
				g.es("using -asis option in:" + h)
		elif g.match(h,i,"noref"): # Just match the prefix.
			if atFileType == "@file":
				atFileType = "@rawfile"
			elif atFileType == "@nosentinelsfile":
				atFileType = "@silentfile"
			elif err_flag:
				g.es("ignoring redundant -noref in:" + h)
		elif g.match(h,i,"nosent"): # Just match the prefix.
			if atFileType == "@file":
				atFileType = "@nosentinelsfile"
			elif atFileType == "@rawfile":
				atFileType = "@silentfile"
			elif err_flag:
				g.es("ignoring redundant -nosent in:" + h)
		elif g.match_word(h,i,"thin"):
			if atFileType == "@file":
				atFileType = "@thinfile"
			elif err_flag:
				g.es("using -thin option in:" + h)
		else:
			if 0: # doesn't work
				for option in ("fat","new","now","old","thin","wait"):
					if g.match_word(h,i,option):
						optionsList.append(option)
				if len(option) == 0:
					err = i-1
		# Scan to the next minus sign.
		while i < len(h) and h[i] not in (' ','\t','-'):
			i += 1
		if err > -1:
			g.es("unknown option:" + h[err:i] + " in " + h)
		#@nonl
		#@-node:ekr.20031218072017.3153:<< scan another @file option >>
		#@nl
		
	# Convert atFileType to a list of options.
	for fileType,option in (
		("@silentfile","asis"),
		("@nosentinelsfile","nosent"),
		("@rawfile","noref"),
		("@thinfile","thin")
	):
		if atFileType == fileType and option not in optionsList:
			optionsList.append(option)
			
	# g.trace(atFileType,optionsList)

	return i,atFileType,optionsList
#@nonl
#@-node:ekr.20031218072017.3152:g.scanAtFileOptions
#@+node:ekr.20031218072017.3154:scanAtRootOptions
def scanAtRootOptions (s,i,err_flag=false):
	
	assert(g.match(s,i,"@root"))
	i += len("@root")
	mode = None 
	while g.match(s,i,'-'):
		#@		<< scan another @root option >>
		#@+node:ekr.20031218072017.3155:<< scan another @root option >>
		i += 1 ; err = -1
		
		if g.match_word(s,i,"code"): # Just match the prefix.
			if not mode: mode = "code"
			elif err_flag: g.es("modes conflict in:" + g.get_line(s,i))
		elif g.match(s,i,"doc"): # Just match the prefix.
			if not mode: mode = "doc"
			elif err_flag: g.es("modes conflict in:" + g.get_line(s,i))
		else:
			err = i-1
			
		# Scan to the next minus sign.
		while i < len(s) and s[i] not in (' ','\t','-'):
			i += 1
		
		if err > -1 and err_flag:
			g.es("unknown option:" + s[err:i] + " in " + g.get_line(s,i))
		#@nonl
		#@-node:ekr.20031218072017.3155:<< scan another @root option >>
		#@nl

	if mode == None:
		doc = app.config.at_root_bodies_start_in_doc_mode
		mode = g.choose(doc,"doc","code")
	return i,mode
#@nonl
#@-node:ekr.20031218072017.3154:scanAtRootOptions
#@+node:ekr.20031218072017.3156:scanError
# It seems dubious to bump the Tangle error count here.  OTOH, it really doesn't hurt.

def scanError(s):

	"""Bump the error count in the tangle command."""

	g.top().tangleCommands.errors += 1

	g.es(s)
#@nonl
#@-node:ekr.20031218072017.3156:scanError
#@+node:ekr.20031218072017.3157:scanf
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
	# g.trace("scanf returns:",result)
	return result
	
if 0: # testing
	from leoGlobals import trace
	g.scanf("1.0","%d.%d",)
#@nonl
#@-node:ekr.20031218072017.3157:scanf
#@+node:ekr.20031218072017.3158:Scanners: calling scanError
#@+at 
#@nonl
# These scanners all call g.scanError() directly or indirectly, so they will 
# call g.es() if they find an error.  g.scanError() also bumps 
# c.tangleCommands.errors, which is harmless if we aren't tangling, and useful 
# if we are.
# 
# These routines are called by the Import routines and the Tangle routines.
#@-at
#@+node:ekr.20031218072017.3159:skip_block_comment
# Scans past a block comment (an old_style C comment).

def skip_block_comment (s,i):

	assert(g.match(s,i,"/*"))
	j = i ; i += 2 ; n = len(s)
	
	k = string.find(s,"*/",i)
	if k == -1:
		g.scanError("Run on block comment: " + s[j:i])
		return n
	else: return k + 2
#@nonl
#@-node:ekr.20031218072017.3159:skip_block_comment
#@+node:ekr.20031218072017.3160:skip_braces
#@+at 
#@nonl
# This code is called only from the import logic, so we are allowed to try 
# some tricks.  In particular, we assume all braces are matched in #if blocks.
#@-at
#@@c

def skip_braces(s,i):

	"""Skips from the opening to the matching brace.
	
	If no matching is found i is set to len(s)"""

	# start = g.get_line(s,i)
	assert(g.match(s,i,'{'))
	level = 0 ; n = len(s)
	while i < n:
		c = s[i]
		if c == '{':
			level += 1 ; i += 1
		elif c == '}':
			level -= 1
			if level <= 0: return i
			i += 1
		elif c == '\'' or c == '"': i = g.skip_string(s,i)
		elif g.match(s,i,'//'): i = g.skip_to_end_of_line(s,i)
		elif g.match(s,i,'/*'): i = g.skip_block_comment(s,i)
		# 7/29/02: be more careful handling conditional code.
		elif g.match_word(s,i,"#if") or g.match_word(s,i,"#ifdef") or g.match_word(s,i,"#ifndef"):
			i,delta = g.skip_pp_if(s,i)
			level += delta
		else: i += 1
	return i
#@-node:ekr.20031218072017.3160:skip_braces
#@+node:ekr.20031218072017.3161:skip_php_braces (Dave Hein)
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

	# start = g.get_line(s,i)
	assert(g.match(s,i,'{'))
	level = 0 ; n = len(s)
	while i < n:
		c = s[i]
		if c == '{':
			level += 1 ; i += 1
		elif c == '}':
			level -= 1
			if level <= 0: return i + 1
			i += 1
		elif c == '\'' or c == '"': i = g.skip_string(s,i)
		elif g.match(s,i,"<<<"): i = g.skip_heredoc_string(s,i)
		elif g.match(s,i,'//') or g.match(s,i,'#'): i = g.skip_to_end_of_line(s,i)
		elif g.match(s,i,'/*'): i = g.skip_block_comment(s,i)
		else: i += 1
	return i
#@nonl
#@-node:ekr.20031218072017.3161:skip_php_braces (Dave Hein)
#@+node:ekr.20031218072017.3162:skip_parens
def skip_parens(s,i):

	"""Skips from the opening ( to the matching ).
	
	If no matching is found i is set to len(s)"""

	level = 0 ; n = len(s)
	assert(g.match(s,i,'('))
	while i < n:
		c = s[i]
		if c == '(':
			level += 1 ; i += 1
		elif c == ')':
			level -= 1
			if level <= 0:  return i
			i += 1
		elif c == '\'' or c == '"': i = g.skip_string(s,i)
		elif g.match(s,i,"//"): i = g.skip_to_end_of_line(s,i)
		elif g.match(s,i,"/*"): i = g.skip_block_comment(s,i)
		else: i += 1
	return i
#@nonl
#@-node:ekr.20031218072017.3162:skip_parens
#@+node:ekr.20031218072017.3163:skip_pascal_begin_end
def skip_pascal_begin_end(s,i):

	"""Skips from begin to matching end.
	If found, i points to the end. Otherwise, i >= len(s)
	The end keyword matches begin, case, class, record, and try."""

	assert(g.match_c_word(s,i,"begin"))
	level = 1 ; i = g.skip_c_id(s,i) # Skip the opening begin.
	while i < len(s):
		ch = s[i]
		if ch =='{' : i = g.skip_pascal_braces(s,i)
		elif ch =='"' or ch == '\'': i = g.skip_pascal_string(s,i)
		elif g.match(s,i,"//"): i = g.skip_line(s,i)
		elif g.match(s,i,"(*"): i = g.skip_pascal_block_comment(s,i)
		elif g.match_c_word(s,i,"end"):
			level -= 1 ;
			if level == 0:
				# lines = s[i1:i+3] ; g.trace('\n' + lines + '\n')
				return i
			else: i = g.skip_c_id(s,i)
		elif g.is_c_id(ch):
			j = i ; i = g.skip_c_id(s,i) ; name = s[j:i]
			if name in ["begin", "case", "class", "record", "try"]:
				level += 1
		else: i += 1
	return i
#@-node:ekr.20031218072017.3163:skip_pascal_begin_end
#@+node:ekr.20031218072017.3164:skip_pascal_block_comment
# Scans past a pascal comment delimited by (* and *).

def skip_pascal_block_comment(s,i):
	
	j = i
	assert(g.match(s,i,"(*"))
	i = string.find(s,"*)",i)
	if i > -1: return i + 2
	else:
		g.scanError("Run on comment" + s[j:i])
		return len(s)

#   n = len(s)
#   while i < n:
#       if g.match(s,i,"*)"): return i + 2
#       i += 1
#   g.scanError("Run on comment" + s[j:i])
#   return i
#@nonl
#@-node:ekr.20031218072017.3164:skip_pascal_block_comment
#@+node:ekr.20031218072017.3165:skip_pascal_string : called by tangle
def skip_pascal_string(s,i):

	j = i ; delim = s[i] ; i += 1
	assert(delim == '"' or delim == '\'')

	while i < len(s):
		if s[i] == delim:
			return i + 1
		else: i += 1

	g.scanError("Run on string: " + s[j:i])
	return i
#@nonl
#@-node:ekr.20031218072017.3165:skip_pascal_string : called by tangle
#@+node:ekr.20031218072017.3166:skip_heredoc_string : called by php import (Dave Hein)
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
	assert(g.match(s,i,"<<<"))
	m = re.match("\<\<\<([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)", s[i:])
	if (None == m):
		i += 3
		return i

	# 14-SEP-2002 DTHEIN: needed to add \n to find word, not just string
	delim = m.group(1) + '\n' 
	
	i = g.skip_line(s,i) # 14-SEP-2002 DTHEIN: look after \n, not before
	n = len(s)
	while i < n and not g.match(s,i,delim):
		i = g.skip_line(s,i) # 14-SEP-2002 DTHEIN: move past \n
		
	if i >= n:
		g.scanError("Run on string: " + s[j:i])
	elif g.match(s,i,delim):
		i += len(delim)
	return i
#@-node:ekr.20031218072017.3166:skip_heredoc_string : called by php import (Dave Hein)
#@+node:ekr.20031218072017.3167:skip_pp_directive
# Now handles continuation lines and block comments.

def skip_pp_directive(s,i):

	while i < len(s):
		if g.is_nl(s,i):
			if g.escaped(s,i): i = g.skip_nl(s,i)
			else: break
		elif g.match(s,i,"//"): i = g.skip_to_end_of_line(s,i)
		elif g.match(s,i,"/*"): i = g.skip_block_comment(s,i)
		else: i += 1
	return i
#@nonl
#@-node:ekr.20031218072017.3167:skip_pp_directive
#@+node:ekr.20031218072017.3168:skip_pp_if
# Skips an entire if or if def statement, including any nested statements.

def skip_pp_if(s,i):
	
	start_line = g.get_line(s,i) # used for error messages.
	# g.trace(start_line)

	assert(
		g.match_word(s,i,"#if") or
		g.match_word(s,i,"#ifdef") or
		g.match_word(s,i,"#ifndef"))

	i = g.skip_line(s,i)
	i,delta1 = g.skip_pp_part(s,i)
	i = g.skip_ws(s,i)
	if g.match_word(s,i,"#else"):
		i = g.skip_line(s,i)
		i = g.skip_ws(s,i)
		i,delta2 = g.skip_pp_part(s,i)
		if delta1 != delta2:
			g.es("#if and #else parts have different braces: " + start_line)
	i = g.skip_ws(s,i)
	if g.match_word(s,i,"#endif"):
		i = g.skip_line(s,i)
	else:
		g.es("no matching #endif: " + start_line)

	# g.trace(delta1,start_line)
	return i,delta1
#@-node:ekr.20031218072017.3168:skip_pp_if
#@+node:ekr.20031218072017.3169:skip_pp_part
# Skip to an #else or #endif.  The caller has eaten the #if, #ifdef, #ifndef or #else

def skip_pp_part(s,i):

	# g.trace(g.get_line(s,i))

	delta = 0
	while i < len(s):
		c = s[i]
		if 0:
			if c == '\n':
				g.trace(delta,g.get_line(s,i))
		if g.match_word(s,i,"#if") or g.match_word(s,i,"#ifdef") or g.match_word(s,i,"#ifndef"):
			i,delta1 = g.skip_pp_if(s,i)
			delta += delta1
		elif g.match_word(s,i,"#else") or g.match_word(s,i,"#endif"):
			return i,delta
		elif c == '\'' or c == '"': i = g.skip_string(s,i)
		elif c == '{':
			delta += 1 ; i += 1
		elif c == '}':
			delta -= 1 ; i += 1
		elif g.match(s,i,"//"): i = g.skip_line(s,i)
		elif g.match(s,i,"/*"): i = g.skip_block_comment(s,i)
		else: i += 1
	return i,delta
#@nonl
#@-node:ekr.20031218072017.3169:skip_pp_part
#@+node:ekr.20031218072017.3170:skip_python_string
def skip_python_string(s,i):

	if g.match(s,i,"'''") or g.match(s,i,'"""'):
		j = i ; delim = s[i]*3 ; i += 3
		k = string.find(s,delim,i)
		if k > -1: return k+3
		g.scanError("Run on triple quoted string: " + s[j:i])
		return len(s)
	else:
		return g.skip_string(s,i)
#@nonl
#@-node:ekr.20031218072017.3170:skip_python_string
#@+node:ekr.20031218072017.2369:skip_string : called by tangle
def skip_string(s,i):
	
	j = i ; delim = s[i] ; i += 1
	assert(delim == '"' or delim == '\'')
	
	n = len(s)
	while i < n and s[i] != delim:
		if s[i] == '\\' : i += 2
		else: i += 1

	if i >= n:
		g.scanError("Run on string: " + s[j:i])
	elif s[i] == delim:
		i += 1

	# g.trace(s[j:i])
	return i
#@-node:ekr.20031218072017.2369:skip_string : called by tangle
#@+node:ekr.20031218072017.3171:skip_to_semicolon
# Skips to the next semicolon that is not in a comment or a string.

def skip_to_semicolon(s,i):

	n = len(s)
	while i < n:
		c = s[i]
		if c == ';': return i
		elif c == '\'' or c == '"' : i = g.skip_string(s,i)
		elif g.match(s,i,"//"): i = g.skip_to_end_of_line(s,i)
		elif g.match(s,i,"/*"): i = g.skip_block_comment(s,i)
		else: i += 1
	return i
#@nonl
#@-node:ekr.20031218072017.3171:skip_to_semicolon
#@+node:ekr.20031218072017.3172:skip_typedef
def skip_typedef(s,i):

	n = len(s)
	while i < n and g.is_c_id(s[i]):
		i = g.skip_c_id(s,i)
		i = g.skip_ws_and_nl(s,i)
	if g.match(s,i,'{'):
		i = g.skip_braces(s,i)
		i = g.skip_to_semicolon(s,i)
	return i
#@nonl
#@-node:ekr.20031218072017.3172:skip_typedef
#@-node:ekr.20031218072017.3158:Scanners: calling scanError
#@+node:ekr.20031218072017.3173:Scanners: no error messages
#@+node:ekr.20031218072017.3174:escaped
# Returns true if s[i] is preceded by an odd number of backslashes.

def escaped(s,i):

	count = 0
	while i-1 >= 0 and s[i-1] == '\\':
		count += 1
		i -= 1
	return (count%2) == 1
#@nonl
#@-node:ekr.20031218072017.3174:escaped
#@+node:ekr.20031218072017.3175:find_line_start
def find_line_start(s,i):

	# bug fix: 11/2/02: change i to i+1 in rfind
	i = string.rfind(s,'\n',0,i+1) # Finds the highest index in the range.
	if i == -1: return 0
	else: return i + 1
#@nonl
#@-node:ekr.20031218072017.3175:find_line_start
#@+node:ekr.20031218072017.3176:find_on_line
def find_on_line(s,i,pattern):

	# j = g.skip_line(s,i) ; g.trace(s[i:j])
	j = string.find(s,'\n',i)
	if j == -1: j = len(s)
	k = string.find(s,pattern,i,j)
	if k > -1: return k
	else: return None
#@nonl
#@-node:ekr.20031218072017.3176:find_on_line
#@+node:ekr.20031218072017.3177:is_c_id
def is_c_id(ch):

	return ch and (ch in string.ascii_letters or ch in string.digits or ch == '_')
#@-node:ekr.20031218072017.3177:is_c_id
#@+node:ekr.20031218072017.3178:is_nl
def is_nl(s,i):

	return i < len(s) and (s[i] == '\n' or s[i] == '\r')
#@nonl
#@-node:ekr.20031218072017.3178:is_nl
#@+node:ekr.20031218072017.3179:is_special
# We no longer require that the directive appear befor any @c directive or section definition.

def is_special(s,i,directive):

	"""Return true if the body text contains the @ directive."""

	# j = g.skip_line(s,i) ; g.trace(s[i:j],':',directive)
	assert (directive and directive [0] == '@' )

	# 10/23/02: all directives except @others must start the line.
	skip_flag = directive == "@others"
	while i < len(s):
		if g.match_word(s,i,directive):
			return true, i
		else:
			i = g.skip_line(s,i)
			if skip_flag:
				i = g.skip_ws(s,i)
	return false, -1
#@nonl
#@-node:ekr.20031218072017.3179:is_special
#@+node:ekr.20031218072017.3180:is_ws & is_ws_or_nl
def is_ws(c):

	return c == '\t' or c == ' '
	
def is_ws_or_nl(s,i):

	return g.is_nl(s,i) or (i < len(s) and g.is_ws(s[i]))
#@nonl
#@-node:ekr.20031218072017.3180:is_ws & is_ws_or_nl
#@+node:ekr.20031218072017.3181:match
# Warning: this code makes no assumptions about what follows pattern.

def match(s,i,pattern):

	return s and pattern and string.find(s,pattern,i,i+len(pattern)) == i
#@nonl
#@-node:ekr.20031218072017.3181:match
#@+node:ekr.20031218072017.3182:match_c_word
def match_c_word (s,i,name):

	if name == None: return false
	n = len(name)
	if n == 0: return false
	return name == s[i:i+n] and (i+n == len(s) or not g.is_c_id(s[i+n]))
#@nonl
#@-node:ekr.20031218072017.3182:match_c_word
#@+node:ekr.20031218072017.3183:match_ignoring_case
def match_ignoring_case(s1,s2):

	if s1 == None or s2 == None: return false
	return string.lower(s1) == string.lower(s2)
#@nonl
#@-node:ekr.20031218072017.3183:match_ignoring_case
#@+node:ekr.20031218072017.3184:match_word
def match_word(s,i,pattern):

	if pattern == None: return false
	j = len(pattern)
	if j == 0: return false
	if string.find(s,pattern,i,i+j) != i:
		return false
	if i+j >= len(s):
		return true
	c = s[i+j]
	return not (c in string.ascii_letters or c in string.digits or c == '_')
#@nonl
#@-node:ekr.20031218072017.3184:match_word
#@+node:ekr.20031218072017.3185:skip_blank_lines
def skip_blank_lines(s,i):

	while i < len(s):
		if g.is_nl(s,i) :
			i = g.skip_nl(s,i)
		elif g.is_ws(s[i]):
			j = g.skip_ws(s,i)
			if g.is_nl(s,j):
				i = j
			else: break
		else: break
	return i
#@nonl
#@-node:ekr.20031218072017.3185:skip_blank_lines
#@+node:ekr.20031218072017.3186:skip_c_id
def skip_c_id(s,i):

	n = len(s)
	while i < n:
		c = s[i]
		if c in string.ascii_letters or c in string.digits or c == '_':
			i += 1
		else: break
	return i
#@nonl
#@-node:ekr.20031218072017.3186:skip_c_id
#@+node:ekr.20031218072017.3187:skip_line, skip_to_end_of_line
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
#@-node:ekr.20031218072017.3187:skip_line, skip_to_end_of_line
#@+node:ekr.20031218072017.3188:skip_long
def skip_long(s,i):
	
	"""Scan s[i:] for a valid int.
	Return (i, val) or (i, None) if s[i] does not point at a number.
	"""

	digits = string.digits
	val = 0
	i = g.skip_ws(s,i)
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
#@-node:ekr.20031218072017.3188:skip_long
#@+node:ekr.20031218072017.3189:skip_matching_delims
def skip_matching_delims(s,i,delim1,delim2):
	
	assert(g.match(s,i,delim1))

	i += len(delim1)
	k = string.find(s,delim2,i)
	if k == -1:
		return len(s)
	else:
		return k + len(delim2)
#@nonl
#@-node:ekr.20031218072017.3189:skip_matching_delims
#@+node:ekr.20031218072017.3190:skip_nl
# We need this function because different systems have different end-of-line conventions.

def skip_nl (s,i):

	"""Skips a single "logical" end-of-line character."""

	if g.match(s,i,"\r\n"): return i + 2
	elif g.match(s,i,'\n') or g.match(s,i,'\r'): return i + 1
	else: return i
#@nonl
#@-node:ekr.20031218072017.3190:skip_nl
#@+node:ekr.20031218072017.3191:skip_non_ws
def skip_non_ws (s,i):

	n = len(s)
	while i < n and not g.is_ws(s[i]):
		i += 1
	return i
#@nonl
#@-node:ekr.20031218072017.3191:skip_non_ws
#@+node:ekr.20031218072017.3192:skip_pascal_braces
# Skips from the opening { to the matching }.

def skip_pascal_braces(s,i):

	# No constructs are recognized inside Pascal block comments!
	k = string.find(s,'}',i)
	if i == -1: return len(s)
	else: return k
#@nonl
#@-node:ekr.20031218072017.3192:skip_pascal_braces
#@+node:ekr.20031218072017.3193:skip_to_char
def skip_to_char(s,i,ch):
	
	j = string.find(s,ch,i)
	if j == -1:
		return len(s),s[i:]
	else:
		return j,s[i:j]
#@-node:ekr.20031218072017.3193:skip_to_char
#@+node:ekr.20031218072017.3194:skip_ws, skip_ws_and_nl
def skip_ws(s,i):

	n = len(s)
	while i < n and g.is_ws(s[i]):
		i += 1
	return i
	
def skip_ws_and_nl(s,i):

	n = len(s)
	while i < n and (g.is_ws(s[i]) or g.is_nl(s,i)):
		i += 1
	return i
#@nonl
#@-node:ekr.20031218072017.3194:skip_ws, skip_ws_and_nl
#@-node:ekr.20031218072017.3173:Scanners: no error messages
#@+node:ekr.20031218072017.3195:splitLines & joinLines
def splitLines (s):
	
	"""Split s into lines, preserving the number of lines and the ending of the last line."""
	
	if s:
		return s.splitlines(true) # This is a Python string function!
	else:
		return []

	if 0:# Rewritten: 4/2/04.  This works, but why bother?
		if s:
			lines = s.split('\n')
			result = [line + '\n' for line in lines[:-1]]
			if s[-1] != '\n':
				result.append(lines[-1])
			return result
		else:
			return []

def joinLines (aList):
	
	return ''.join(aList)
#@nonl
#@-node:ekr.20031218072017.3195:splitLines & joinLines
#@-node:ekr.20031218072017.3151:Scanning...
#@+node:ekr.20040327103735.2:Script Tools (leoGlobals.py)
#@+node:ekr.20031218072017.2418:g.initScriptFind (set up dialog)
def initScriptFind(findHeadline,changeHeadline=None,firstNode=None,
	script_search=true,script_change=true):
	
	import leoTest
	import leoGlobals as g
	from leoGlobals import true,false
	
	# Find the scripts.
	c = g.top() ; p = c.currentPosition()
	u = leoTest.testUtils()
	find_p = u.findNodeInTree(p,findHeadline)
	if find_p:
		find_text = find_p.bodyString()
	else:
		g.es("no Find script node",color="red")
		return
	if changeHeadline:
		change_p = u.findNodeInTree(p,changeHeadline)
	else:
		change_p = None
	if change_p:
		change_text = change_p.bodyString()
	else:
		change_text = ""
	# print find_p,change_p
	
	# Initialize the find panel.
	c.script_search_flag = script_search
	c.script_change_flag = script_change and change_text
	if script_search:
		c.find_text = find_text.strip() + "\n"
	else:
		c.find_text = find_text
	if script_change:
		c.change_text = change_text.strip() + "\n"
	else:
		c.change_text = change_text
	g.app.findFrame.init(c)
	c.findPanel()
#@nonl
#@-node:ekr.20031218072017.2418:g.initScriptFind (set up dialog)
#@+node:ekr.20040321065415:g.findNodeInTree, findNodeAnywhere, findTopLevelNode
def findNodeInTree(p,headline):

	"""Search for a node in v's tree matching the given headline."""
	
	c = p.c
	for p in p.subtree_iter():
		if p.headString().strip() == headline.strip():
			return p.copy()
	return c.nullPosition()

def findNodeAnywhere(headline):
	
	c = g.top()
	for p in c.allNodes_iter():
		if p.headString().strip() == headline.strip():
			return p.copy()
	return c.nullPosition()
	
def findTopLevelNode(headline):
	
	c = g.top()
	for p in c.rootPosition().self_and_siblings_iter():
		if p.headString().strip() == headline.strip():
			return p.copy()
	return c.nullPosition()
#@nonl
#@-node:ekr.20040321065415:g.findNodeInTree, findNodeAnywhere, findTopLevelNode
#@-node:ekr.20040327103735.2:Script Tools (leoGlobals.py)
#@+node:ekr.20031218072017.1498:Unicode utils...
#@+node:ekr.20031218072017.1499:isUnicode
def isUnicode(s):
	
	return s is None or type(s) == type(u' ')
#@nonl
#@-node:ekr.20031218072017.1499:isUnicode
#@+node:ekr.20031218072017.1500:isValidEncoding
def isValidEncoding (encoding):
	
	try:
		if len(encoding) == 0:
			return false
		unicode("a",encoding)
		return true
	except:
		return false
#@-node:ekr.20031218072017.1500:isValidEncoding
#@+node:ekr.20031218072017.1501:reportBadChars
def reportBadChars (s,encoding):
	
	errors = 0
	if type(s) == type(u""):
		for ch in s:
			try: ch.encode(encoding,"strict")
			except: errors += 1
		if errors:
			# traceback.print_stack()
			g.es("%d errors converting %s to %s" % 
				(errors, s.encode(encoding,"replace"),encoding))

	elif type(s) == type(""):
		for ch in s:
			try: unicode(ch,encoding,"strict")
			except: errors += 1
		if errors:
			g.es("%d errors converting %s (%s encoding) to unicode" % 
				(errors, unicode(s,encoding,"replace"),encoding)) # 10/23/03
#@nonl
#@-node:ekr.20031218072017.1501:reportBadChars
#@+node:ekr.20031218072017.1502:toUnicode & toEncodedString
def toUnicode (s,encoding,reportErrors=false):
	
	if s is None:
		s = u""
	if type(s) == type(""):
		try:
			s = unicode(s,encoding,"strict")
		except:
			if reportErrors:
				g.reportBadChars(s,encoding)
			s = unicode(s,encoding,"replace")
	return s
	
def toEncodedString (s,encoding,reportErrors=false):

	if type(s) == type(u""):
		try:
			s = s.encode(encoding,"strict")
		except:
			if reportErrors:
				g.reportBadChars(s,encoding)
			s = s.encode(encoding,"replace")
	return s
#@nonl
#@-node:ekr.20031218072017.1502:toUnicode & toEncodedString
#@+node:ekr.20031218072017.1503:getpreferredencoding from 2.3a2
try:
	# Use Python's version of getpreferredencoding if it exists.
	# It is new in Python 2.3.
	import locale
	getpreferredencoding = locale.getpreferredencoding
except:
	# Use code copied from locale.py in Python 2.3alpha2.
	if sys.platform in ('win32', 'darwin', 'mac'):
		#@		<< define getpreferredencoding using _locale >>
		#@+node:ekr.20031218072017.1504:<< define getpreferredencoding using _locale >>
		# On Win32, this will return the ANSI code page
		# On the Mac, it should return the system encoding;
		# it might return "ascii" instead.
		
		def getpreferredencoding(do_setlocale = true):
			"""Return the charset that the user is likely using."""
			try:
				import _locale
				return _locale._getdefaultlocale()[1]
			except:
				return None
		#@nonl
		#@-node:ekr.20031218072017.1504:<< define getpreferredencoding using _locale >>
		#@nl
	else:
		#@		<< define getpreferredencoding for *nix >>
		#@+node:ekr.20031218072017.1505:<< define getpreferredencoding for *nix >>
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
					return None
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
					return None
		#@nonl
		#@-node:ekr.20031218072017.1505:<< define getpreferredencoding for *nix >>
		#@nl
#@-node:ekr.20031218072017.1503:getpreferredencoding from 2.3a2
#@-node:ekr.20031218072017.1498:Unicode utils...
#@+node:ekr.20031218072017.3197:Whitespace...
#@+node:ekr.20031218072017.3198:computeLeadingWhitespace
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
#@-node:ekr.20031218072017.3198:computeLeadingWhitespace
#@+node:ekr.20031218072017.3199:computeWidth
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
#@-node:ekr.20031218072017.3199:computeWidth
#@+node:ekr.20031218072017.3200:get_leading_ws
def get_leading_ws(s):
	
	"""Returns the leading whitespace of 's'."""

	i = 0 ; n = len(s)
	while i < n and s[i] in (' ','\t'):
		i += 1
	return s[0:i]
#@-node:ekr.20031218072017.3200:get_leading_ws
#@+node:ekr.20031218072017.3201:optimizeLeadingWhitespace
# Optimize leading whitespace in s with the given tab_width.

def optimizeLeadingWhitespace (line,tab_width):

	i, width = g.skip_leading_ws_with_indent(line,0,tab_width)
	s = g.computeLeadingWhitespace(width,tab_width) + line[i:]
	return s
#@nonl
#@-node:ekr.20031218072017.3201:optimizeLeadingWhitespace
#@+node:ekr.20031218072017.3202:removeLeadingWhitespace
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
#@-node:ekr.20031218072017.3202:removeLeadingWhitespace
#@+node:ekr.20031218072017.3203:removeTrailingWs
# Warning: string.rstrip also removes newlines!

def removeTrailingWs(s):

	j = len(s)-1
	while j >= 0 and (s[j] == ' ' or s[j] == '\t'):
		j -= 1
	return s[:j+1]
#@-node:ekr.20031218072017.3203:removeTrailingWs
#@+node:ekr.20031218072017.3204:skip_leading_ws
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
#@-node:ekr.20031218072017.3204:skip_leading_ws
#@+node:ekr.20031218072017.3205:skip_leading_ws_with_indent
def skip_leading_ws_with_indent(s,i,tab_width):

	"""Skips leading whitespace and returns (i, indent), 
	
	- i points after the whitespace
	- indent is the width of the whitespace, assuming tab_width wide tabs."""

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
#@-node:ekr.20031218072017.3205:skip_leading_ws_with_indent
#@-node:ekr.20031218072017.3197:Whitespace...
#@-others
#@nonl
#@-node:ekr.20031218072017.3093:@file-thin leoGlobals.py
#@-leo
