#line1
#line2
#@+leo
#@+node:0::@file leoAtFile.py 
#@+body
#@@first
#@@first


#@@language python


#@+at
#  Class to read and write @file nodes.
# 
# This code uses readline() to get each line rather than reading the entire 
# file into a buffer.  This is more memory efficient and saves us from having 
# to scan for the end of each line.  The result is cleaner and faster code.  
# This code also accumulates body text line-by-line rather than 
# character-by-character, a much faster way.

#@-at
#@@c

from leoGlobals import *
import leoColor,leoNodes
import filecmp,os,os.path,time

class atFile:
	
	#@<< atFile constants >>
	#@+node:1::<< atFile constants >>
	#@+body
	# The kind of at_directives.
	
	noDirective		=  1 # not an at-directive.
	delimsDirective =  2 # @delims (not used!)
	docDirective	=  3 # @doc.
	atDirective		=  4 # @<space> or @<newline>
	codeDirective	=  5 # @code
	cDirective		=  6 # @c<space> or @c<newline>
	othersDirective	=  7 # at-others
	miscDirective	=  8 # All other directives
	rawDirective = 9 # @raw
	endRawDirective = 10 # @end_raw
	
	# The kind of sentinel line.
	noSentinel		=  9 # Not a sentinel
	endAt			= 10 # @-at
	endBody			= 11 # @-body
	endDoc			= 12 # @-doc
	endLeo			= 13 # @-leo
	endNode			= 14 # @-node
	endOthers		= 15 # @-others
	startAt			= 16 # @+at
	startBody		= 17 # @+body
	startComment = 18 # @comment 10/16/02
	startDelims		= 19 # @delims
	startDirective	= 20 # @@
	startDoc		= 21 # @+doc
	startLeo		= 22 # @+leo
	startNode		= 23 # @+node
	startOthers		= 24 # @+others
	startNewline = 25 # @newline 9/27/02
	startNoNewline = 26 # @nonewline 9/27/02
	startRef		= 27 # @< < ... > >
	startVerbatim	= 28 # @verbatim
	startVerbatimAfterRef = 29 # @verbatimAfterRef
	
	#@-body
	#@-node:1::<< atFile constants >>


	#@+others
	#@+node:2::atFile ctor
	#@+body
	def __init__(self,theCommander): 
	
		# trace("__init__", "atFile.__init__")
		self.commands = theCommander # The commander for the current window.
		self.initIvars()
	
	def initIvars(self):
	
		
		#@<< initialize atFile ivars >>
		#@+node:1::<< initialize atFile ivars >>
		#@+body
		#@+at
		#  errors is the number of errors seen while reading and writing.  
		# structureErrors are errors reported by createNthChild.  If structure 
		# errors are found we delete the outline tree and rescan.

		#@-at
		#@@c
		self.errors = 0
		self.structureErrors = 0
		

		#@+at
		#  Initialized by atFile.scanAllDirectives.  8/1/02: set all to None here.

		#@-at
		#@@c
		self.default_directory = None
		self.page_width = None
		self.tab_width  = None
		self.startSentinelComment = None
		self.endSentinelComment = None
		self.language = None
		

		#@+at
		#  The files used by the output routines.  When tangling, we first 
		# write to a temporary output file.  After tangling is temporary 
		# file.  Otherwise we delete the old target file and rename the 
		# temporary file to be the target file.

		#@-at
		#@@c
		self.shortFileName = "" # short version of file name used for messages.
		self.targetFileName = u"" # EKR 1/21/03: now a unicode string
		self.outputFileName = u"" # EKR 1/21/03: now a unicode string
		self.outputFile = None # The temporary output file.
		

		#@+at
		#  The indentation used when outputting section references or 
		# at-others sections.  We add the indentation of the line containing 
		# the at-node directive and restore the old value when the
		# expansion is complete.

		#@-at
		#@@c
		self.indent = 0  # The unit of indentation is spaces, not tabs.
		
		# The root of tree being written.
		self.root = None
		
		# Ivars used to suppress newlines between sentinels.
		self.suppress_newlines = true # true: enable suppression of newlines.
		self.newline_pending = false # true: newline is pending on read or write.
		
		# Support of output_newline option
		self.output_newline = getOutputNewline()
		
		# Support of @raw
		self.raw = false # true: in @raw mode
		self.sentinels = true # true: output sentinels while expanding refs.
		
		# For tracing problems involing indentation and blank lines.
		self.trace = false
		
		# The encoding used to convert from unicode to a byte stream.
		self.encoding = app().config.default_derived_file_encoding
		#@-body
		#@-node:1::<< initialize atFile ivars >>
	#@-body
	#@-node:2::atFile ctor
	#@+node:3::Sentinels
	#@+node:1::nodeSentinelText
	#@+body
	def nodeSentinelText(self,v):
	
		config = app().config
	
		if config.write_clone_indices:
			cloneIndex = v.t.cloneIndex
			clone_s = choose(cloneIndex > 0, "C=" + `cloneIndex`, "")
		else: clone_s = ""
		
		if v == self.root or not v.parent():
			index = 0
		else:
			index = v.childIndex() + 1
	
		h = v.headString()
		
		#@<< remove comment delims from h if necessary >>
		#@+node:1::<< remove comment delims from h if necessary >>
		#@+body
		#@+at
		#  Bug fix 1/24/03:
		# 
		# If the present @language/@comment settings do not specify a 
		# single-line comment we remove all block comment delims from h.  This 
		# prevents headline text from interfering with the parsing of node sentinels.

		#@-at
		#@@c

		start = self.startSentinelComment
		end = self.endSentinelComment
		
		if end and len(end) > 0:
			h = h.replace(start,"")
			h = h.replace(end,"")
		#@-body
		#@-node:1::<< remove comment delims from h if necessary >>

	
		return str(index) + ':' + clone_s + ':' + h
	#@-body
	#@-node:1::nodeSentinelText
	#@+node:2::putCloseNodeSentinel
	#@+body
	def putCloseNodeSentinel(self,v):
	
		s = self.nodeSentinelText(v)
		self.putSentinel("@-node:" + s)
	#@-body
	#@-node:2::putCloseNodeSentinel
	#@+node:3::putCloseSentinels
	#@+body
	#@+at
	#  root is an ancestor of v, or root == v.  We call putCloseSentinel for v 
	# up to, but not including, root.

	#@-at
	#@@c
	def putCloseSentinels(self,root,v):
	
		self.putCloseNodeSentinel(v)
		while 1:
			v = v.parent()
			assert(v) # root must be an ancestor of v.
			if  v == root: break
			self.putCloseNodeSentinel(v)
	#@-body
	#@-node:3::putCloseSentinels
	#@+node:4::putOpenLeoSentinel
	#@+body
	#@+at
	#  This method is the same as putSentinel except we don't put an opening 
	# newline and leading whitespace.

	#@-at
	#@@c
	def putOpenLeoSentinel(self,s):
		
		if not self.sentinels: return # Handle @nosentinelsfile.
	
		self.os(self.startSentinelComment)
		self.os(s)
		encoding = self.encoding.lower()
		if encoding != "utf-8":
			self.os("-encoding=")
			self.os(encoding)
			self.os(".")
		self.os(self.endSentinelComment)
		if self.suppress_newlines: # 9/27/02
			self.newline_pending = true # Schedule a newline.
		else:
			self.onl() # End of sentinel.
	#@-body
	#@-node:4::putOpenLeoSentinel
	#@+node:5::putOpenNodeSentinel
	#@+body
	#@+at
	#  This method puts an open node sentinel for node v.

	#@-at
	#@@c
	def putOpenNodeSentinel(self,v):
	
		if v.isAtFileNode() and v != self.root:
			self.writeError("@file not valid in: " + v.headString())
		else:
			s = self.nodeSentinelText(v)
			self.putSentinel("@+node:" + s)
	#@-body
	#@-node:5::putOpenNodeSentinel
	#@+node:6::putOpenSentinels
	#@+body
	#@+at
	#  root is an ancestor of v, or root == v.  We call putOpenNodeSentinel on 
	# all the descendents of root which are the ancestors of v.

	#@-at
	#@@c
	def putOpenSentinels(self,root,v):
	
		last = root
		while last != v:
			# Set node to v or the ancestor of v that is a child of last.
			node = v
			while node and node.parent() != last:
				node = node.parent()
			assert(node)
			self.putOpenNodeSentinel(node)
			last = node
	#@-body
	#@-node:6::putOpenSentinels
	#@+node:7::putSentinel (applies cweb hack)
	#@+body
	#@+at
	#  All sentinels are eventually output by this method.
	# 
	# Sentinels include both the preceding and following newlines. This rule 
	# greatly simplies the code and has several important benefits:
	# 
	# 1. Callers never have to generate newlines before or after sentinels.  
	# Similarly, routines that expand code and doc parts never have to add 
	# "extra" newlines.
	# 2. There is no need for a "no-newline" directive.  If text follows a 
	# section reference, it will appear just after the newline that ends 
	# sentinel at the end of the expansion of the reference.  If no 
	# significant text follows a reference, there will be two newlines 
	# following the ending sentinel.
	# 
	# The only exception is that no newline is required before the opening 
	# "leo" sentinel. The putLeoSentinel and isLeoSentinel routines handle 
	# this minor exception.

	#@-at
	#@@c
	def putSentinel(self,s):
		
		if not self.sentinels:
			if self.trace: trace(s)
			return # Handle @nosentinelsfile.
	
		self.newline_pending = false # discard any pending newline.
		self.onl() ; self.putIndent(self.indent) # Start of sentinel.
		self.os(self.startSentinelComment)
	
		# 11/1/02: The cweb hack: if the opening comment delim ends in '@',
		# double all '@' signs except the first, which is "doubled" by the
		# trailing '@' in the opening comment delimiter.
		start = self.startSentinelComment
		if start and len(start) > 0 and start[-1] == '@':
			assert(s and len(s)>0 and s[0]=='@')
			s = s.replace('@','@@')[1:]
	
		self.os(s)
		self.os(self.endSentinelComment)
		if self.suppress_newlines:
			self.newline_pending = true # Schedule a newline.
		else:
			self.onl() # End of sentinel.
	#@-body
	#@-node:7::putSentinel (applies cweb hack)
	#@+node:8::sentinelKind
	#@+body
	#@+at
	#  This method tells what kind of sentinel appears in line s.  Typically s 
	# will be an empty line before the actual sentinel, but it is also valid 
	# for s to be an actual sentinel line.
	# 
	# Returns (kind, s, emptyFlag), where emptyFlag is true if kind == 
	# noSentinel and s was an empty line on entry.

	#@-at
	#@@c

	sentinelDict = {
		"@comment" : startComment, # 10/16/02
		"@delims" : startDelims, # 10/26/02
		"@newline" : startNewline,
		"@nonewline" : startNoNewline,
		"@verbatim": startVerbatim,
		"@verbatimAfterRef": startVerbatimAfterRef,
		"@+at": startAt, "@-at": endAt,
		"@+body": startBody, "@-body": endBody,
		"@+doc": startDoc, "@-doc": endDoc,
		"@+leo": startLeo, "@-leo": endLeo,
		"@+node": startNode, "@-node": endNode,
		"@+others": startOthers, "@-others": endOthers }
	
	def sentinelKind(self,s):
	
		i = skip_ws(s,0)
		if match(s,i,self.startSentinelComment): 
			i += len(self.startSentinelComment)
		else:
			return atFile.noSentinel
	
		# 10/30/02: locally undo cweb hack here
		start = self.startSentinelComment
		if start and len(start) > 0 and start[-1] == '@':
			s = s[:i] + string.replace(s[i:],'@@','@')
	
		# Do not skip whitespace here!
		if match(s,i,"@<<"): return atFile.startRef
		if match(s,i,"@@"): return atFile.startDirective
		if not match(s,i,'@'): return atFile.noSentinel
		j = i # start of lookup
		i += 1 # skip the at sign.
		if match(s,i,'+') or match(s,i,'-'):
			i += 1
		i = skip_c_id(s,i)
		# trace(`s[j:i]`)
		key = s[j:i]
		if len(key) > 0 and atFile.sentinelDict.has_key(key):
			return atFile.sentinelDict[key]
		else:
			return atFile.noSentinel
	#@-body
	#@-node:8::sentinelKind
	#@+node:9::sentinelName
	#@+body
	# Returns the name of the sentinel for warnings.
	
	sentinelNameDict = {
		endAt: "@-at", endBody: "@-body",
		endDoc: "@-body", endLeo: "@-leo",
		endNode: "@-node", endOthers: "@-others",
		noSentinel: "<no sentinel>",
		startAt: "@+at", startBody: "@+body",
		startDirective: "@@", startDoc: "@+doc",
		startLeo: "@+leo", startNode: "@+node",
		startNewline : "@newline", startNoNewline : "@nonewline",
	 	startOthers: "@+others", startVerbatim: "@verbatim" }
	
	def sentinelName(self, kind):
		if atFile.sentinelNameDict.has_key(kind):
			return atFile.sentinelNameDict[kind]
		else:
			return "<unknown sentinel!>"
	#@-body
	#@-node:9::sentinelName
	#@+node:10::skipSentinelStart
	#@+body
	def skipSentinelStart(self,s,i):
	
		start = self.startSentinelComment
		assert(start and len(start)>0)
	
		if is_nl(s,i): i = skip_nl(s,i)
		i = skip_ws(s,i)
		assert(match(s,i,start))
		i += len(start)
		# 7/8/02: Support for REM hack
		i = skip_ws(s,i)
		assert(i < len(s) and s[i] == '@')
		return i + 1
	
	#@-body
	#@-node:10::skipSentinelStart
	#@-node:3::Sentinels
	#@+node:4::Utilites
	#@+node:1::atFile.scanAllDirectives (calls writeError on errors)
	#@+body
	#@+at
	#  This code scans the node v and all of v's ancestors looking for 
	# directives.  If found, the corresponding Tangle/Untangle globals are set.
	# 
	# Once a directive is seen, no other related directives in nodes further 
	# up the tree have any effect.  For example, if an @color directive is 
	# seen in node v, no @color or @nocolor directives are examined in any 
	# ancestor of v.
	# 
	# This code is similar to Commands::scanAllDirectives, but it has been 
	# modified for use by the atFile class.

	#@-at
	#@@c

	def scanAllDirectives(self,v):
	
		c = self.commands
		
		#@<< Set ivars >>
		#@+node:1::<< Set ivars >>
		#@+body
		self.page_width = self.commands.page_width
		self.tab_width  = self.commands.tab_width
		
		self.default_directory = None # 8/2: will be set later.
		
		delim1, delim2, delim3 = set_delims_from_language(c.target_language)
		self.language = c.target_language
		
		self.encoding = app().config.default_derived_file_encoding
		#@-body
		#@-node:1::<< Set ivars >>

		
		#@<< Set path from @file node >>
		#@+node:2::<< Set path from @file node >>
		#@+body
		# An absolute path in an @file node over-rides everything else.
		# A relative path gets appended to the relative path by the open logic.
		
		# Bug fix: 10/16/02
		if v.isAtFileNode():
			name = v.atFileNodeName()
		elif v.isAtRawFileNode():
			name = v.atRawFileNodeName()
		elif v.isAtNoSentinelsFileNode():
			name = v.atNoSentinelsFileNodeName()
		else:
			name = ""
		
		dir = choose(name,os.path.dirname(name),None)
		if dir and len(dir) > 0 and os.path.isabs(dir):
			if os.path.exists(dir):
				self.default_directory = dir
			else: # 9/25/02
				self.default_directory = makeAllNonExistentDirectories(dir)
				if not self.default_directory:
					self.error("Directory \"" + dir + "\" does not exist")
					
		
		#@-body
		#@-node:2::<< Set path from @file node >>

		old = {}
		while v:
			s = v.t.bodyString
			dict = get_directives_dict(s)
			
			#@<< Test for @path >>
			#@+node:6::<< Test for @path >>
			#@+body
			# We set the current director to a path so future writes will go to that directory.
			
			loadDir = app().loadDir
			
			if not self.default_directory and not old.has_key("path") and dict.has_key("path"):
			
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
				path = path.strip()
				
				if 0: # 11/14/02: we want a _relative_ path, not an absolute path.
					path = os.path.join(loadDir,path)
				#@-body
				#@-node:1::<< compute relative path from s[k:] >>

				if path and len(path) > 0:
					base = getBaseDirectory() # returns "" on error.
					path = os.path.join(base,path)
					if os.path.isabs(path):
						
						#@<< handle absolute path >>
						#@+node:2::<< handle absolute path >>
						#@+body
						# path is an absolute path.
						
						if os.path.exists(path):
							self.default_directory = path
						else: # 9/25/02
							self.default_directory = makeAllNonExistentDirectories(path)
							if not self.default_directory:
								self.error("invalid @path: " + path)
						
						#@-body
						#@-node:2::<< handle absolute path >>

					else:
						self.error("ignoring bad @path: " + path)
				else:
					self.error("ignoring empty @path")
			#@-body
			#@-node:6::<< Test for @path >>

			
			#@<< Test for @encoding >>
			#@+node:4::<< Test for @encoding >>
			#@+body
			if not old.has_key("encoding") and dict.has_key("encoding"):
				
				k = dict["encoding"]
				j = len("@encoding")
				i = skip_to_end_of_line(s,k)
				encoding = s[k+j:i].strip()
				# trace("encoding:",encoding)
				if isValidEncoding(encoding):
					self.encoding = encoding
				else:
					es("invalid @encoding:", encoding)
			
			#@-body
			#@-node:4::<< Test for @encoding >>

			
			#@<< Test for @comment and @language >>
			#@+node:3::<< Test for @comment and @language >>
			#@+body
			# 10/17/02: @language and @comment may coexist in @file trees.
			# For this to be effective the @comment directive should follow the @language directive.
			
			if not old.has_key("comment") and dict.has_key("comment"):
				k = dict["comment"]
				# 11/14/02: Similar to fix below.
				delim1, delim2, delim3 = set_delims_from_string(s[k:])
			
			# Reversion fix: 12/06/02: We must use elif here, not if.
			elif not old.has_key("language") and dict.has_key("language"):
				k = dict["language"]
				# 11/14/02: Fix bug reported by J.M.Gilligan.
				self.language,delim1,delim2,delim3 = set_language(s,k)
			#@-body
			#@-node:3::<< Test for @comment and @language >>

			
			#@<< Test for @header and @noheader >>
			#@+node:5::<< Test for @header and @noheader >>
			#@+body
			# EKR: 10/10/02: perform the sames checks done by tangle.scanAllDirectives.
			if dict.has_key("header") and dict.has_key("noheader"):
				es("conflicting @header and @noheader directives")
			#@-body
			#@-node:5::<< Test for @header and @noheader >>

			
			#@<< Test for @pagewidth >>
			#@+node:7::<< Test for @pagewidth >>
			#@+body
			if dict.has_key("pagewidth") and not old.has_key("pagewidth"):
			
				k = dict["pagewidth"]
				j = i = k + len("@pagewidth")
				i, val = skip_long(s,i)
				if val != None and val > 0:
					self.page_width = val
				else:
					i = skip_to_end_of_line(s,i)
					self.error("Ignoring " + s[k:i])
			#@-body
			#@-node:7::<< Test for @pagewidth >>

			
			#@<< Test for @tabwidth >>
			#@+node:8::<< Test for @tabwidth >>
			#@+body
			if dict.has_key("tabwidth") and not old.has_key("tabwidth"):
			
				k = dict["tabwidth"]
				j = i = k + len("@tabwidth")
				i, val = skip_long(s, i)
				if val != None and val != 0:
					self.tab_width = val
				else:
					i = skip_to_end_of_line(s,i)
					self.error("Ignoring " + s[k:i])
			
			#@-body
			#@-node:8::<< Test for @tabwidth >>

			old.update(dict)
			v = v.parent()
		
		#@<< Set current directory >>
		#@+node:9::<< Set current directory >>
		#@+body
		# This code is executed if no valid absolute path was specified in the @file node or in an @path directive.
		
		if c.frame and not self.default_directory:
			base = getBaseDirectory() # returns "" on error.
			for dir in (c.tangle_directory,c.frame.openDirectory,c.openDirectory):
				if dir and len(dir) > 0:
					dir = os.path.join(base,dir)
					if os.path.isabs(dir): # Errors may result in relative or invalid path.
						if os.path.exists(dir):
							self.default_directory = dir ; break
						else: # 9/25/02
							self.default_directory = makeAllNonExistentDirectories(dir)
		
		if not self.default_directory:
			# This should never happen: c.openDirectory should be a good last resort.
			self.error("No absolute directory specified anywhere.")
			self.default_directory = ""
		#@-body
		#@-node:9::<< Set current directory >>

		
		#@<< Set comment Strings from delims >>
		#@+node:10::<< Set comment Strings from delims >>
		#@+body
		# Use single-line comments if we have a choice.
		# 8/2/01: delim1,delim2,delim3 now correspond to line,start,end
		if delim1:
			self.startSentinelComment = delim1
			self.endSentinelComment = "" # Must not be None.
		elif delim2 and delim3:
			self.startSentinelComment = delim2
			self.endSentinelComment = delim3
		else: # Emergency!
			# assert(0)
			es("Unknown language: using Python comment delimiters")
			es("c.target_language:"+`c.target_language`)
			es("delim1,delim2,delim3:" + `delim1`+":"+`delim2`+":"+`delim3`)
			self.startSentinelComment = "#" # This should never happen!
			self.endSentinelComment = ""
		#@-body
		#@-node:10::<< Set comment Strings from delims >>
	#@-body
	#@-node:1::atFile.scanAllDirectives (calls writeError on errors)
	#@+node:2::directiveKind
	#@+body
	# Returns the kind of at-directive or noDirective.
	
	def directiveKind(self,s,i):
	
		n = len(s)
		if i >= n or s[i] != '@':
			return atFile.noDirective
	
		table = (
			("@c",atFile.cDirective),
			("@code",atFile.codeDirective),
			("@doc",atFile.docDirective),
			("@end_raw",atFile.endRawDirective),
			("@others",atFile.othersDirective),
			("@raw",atFile.rawDirective))
	
		# This code rarely gets executed, so simple code suffices.
		if i+1 >= n or match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@\n"):
			# 10/25/02: @space is not recognized in cweb mode.
			# 11/15/02: Noweb doc parts are _never_ scanned in cweb mode.
			return choose(self.language=="cweb",
				atFile.noDirective,atFile.atDirective)
	
		# 10/28/02: @c and @(nonalpha) are not recognized in cweb mode.
		# We treat @(nonalpha) separately because @ is in the colorizer table.
		if self.language=="cweb" and (
			match_word(s,i,"@c") or
			i+1>= n or s[i+1] not in string.letters):
			return atFile.noDirective
	
		for name,directive in table:
			if match_word(s,i,name):
				return directive
		# 10/14/02: return miscDirective only for real directives.
		for name in leoColor.leoKeywords:
			if match_word(s,i,name):
				return atFile.miscDirective
	
		return atFile.noDirective
	#@-body
	#@-node:2::directiveKind
	#@+node:3::error
	#@+body
	def error(self,message):
	
		es(message)
		self.errors += 1
	#@-body
	#@-node:3::error
	#@+node:4::skipIndent
	#@+body
	# Skip past whitespace equivalent to width spaces.
	
	def skipIndent(self,s,i,width):
	
		ws = 0 ; n = len(s)
		while i < n and ws < width:
			if   s[i] == '\t': ws += (abs(self.tab_width) - (ws % abs(self.tab_width)))
			elif s[i] == ' ':  ws += 1
			else: break
			i += 1
		return i
	#@-body
	#@-node:4::skipIndent
	#@+node:5::readError
	#@+body
	def readError(self,message):
	
		# This is useful now that we don't print the actual messages.
		if self.errors == 0:
			es("----- error reading @file " + self.targetFileName)
			self.error(message) # 9/10/02: we must increment self.errors!
	
		if 0: # CVS conflicts create too many messages.
			self.error(message)
		
		self.root.setOrphan()
		self.root.setDirty()
	#@-body
	#@-node:5::readError
	#@+node:6::updateCloneIndices
	#@+body
	#@+at
	#  The new Leo2 computes clone indices differently from the old Leo2:
	# 
	# 1. The new Leo2 recomputes clone indices for every write.
	# 2. The new Leo2 forces the clone index of the @file node to be zero.
	# 
	# Also, the read logic ignores the clone index of @file nodes, thereby 
	# ensuring that we don't mistakenly join an @file node to another node.

	#@-at
	#@@c
	def updateCloneIndices(self,root,next):
	
		if root.isCloned():
			if 0: # 9/26/02: Silently allow this.  Everything appears to work.
				self.error("ignoring clone mark for " + root.headString())
			root.t.setCloneIndex(0)
		index = 0
		# 12/17/01: increment each cloneIndex at most once.
		v = root
		while v and v != next:
			v.t.cloneIndex = 0
			v = v.threadNext()
		v = root
		while v and v != next:
			vIs = v.isCloned()
			vShould = v.shouldBeClone() #verbose
			if 0: # vIs or vShould:
				es("update:"+`index`+" is:"+`vIs`+" should:"+`vShould`+`v`) ; enl()
			if v.t.cloneIndex == 0 and vIs and vShould:
				index += 1
				v.t.cloneIndex = index
			v = v.threadNext()
		# Make sure the root's clone index is zero.
		root.t.setCloneIndex(0)
	#@-body
	#@-node:6::updateCloneIndices
	#@+node:7::writeError
	#@+body
	def writeError(self,message):
	
		if self.errors == 0:
			es("errors writing: " + self.targetFileName)
		self.error(message)
		self.root.setOrphan()
		self.root.setDirty()
	#@-body
	#@-node:7::writeError
	#@-node:4::Utilites
	#@+node:5::Reading
	#@+node:1::createNthChild
	#@+body
	#@+at
	#  Sections appear in the derived file in reference order, not tree 
	# order.  Therefore, when we insert the nth child of the parent there is 
	# no guarantee that the previous n-1 children have already been inserted. 
	# And it won't work just to insert the nth child as the last child if 
	# there aren't n-1 previous siblings.  For example, if we insert the third 
	# child followed by the second child followed by the first child the 
	# second and third children will be out of order.
	# 
	# To ensure that nodes are placed in the correct location we create 
	# "dummy" children as needed as placeholders.  In the example above, we 
	# would insert two dummy children when inserting the third child.  When 
	# inserting the other two children we replace the previously inserted 
	# dummy child with the actual children.
	# 
	# vnode child indices are zero-based.  Here we use 1-based indices.
	# 
	# With the "mirroring" scheme it is a structure error if we ever have to 
	# create dummy vnodes.  Such structure errors cause a second pass to be 
	# made, with an empty root.  This second pass will generate other 
	# structure errors, which are ignored.

	#@-at
	#@@c
	def createNthChild(self,n,parent,headline):
	
		assert(n > 0)
	
		# Create any needed dummy children.
		dummies = n - parent.numberOfChildren() - 1
		if dummies > 0:
			if 0: # CVS produces to many errors for this to be useful.
				es("dummy created")
			self.structureErrors += 1
		while dummies > 0:
			dummies -= 1
			dummy = parent.insertAsLastChild(leoNodes.tnode())
			# The user should never see this headline.
			dummy.initHeadString("Dummy")
	
		if n <= parent.numberOfChildren():
			
			#@<< check the headlines >>
			#@+node:1::<< check the headlines >>
			#@+body
			#@+at
			#  1/24/03: A kludgy fix to the problem of headlines containing 
			# comment delims.
			# 
			# The comparisons of headlines will disappear in 4.0.  However, 
			# the problems created by having block comment delimiters in 
			# headlines will remain: they can't be allowed to interfere with 
			# the block comment delimiters in sentinels.

			#@-at
			#@@c
			result = parent.nthChild(n-1)
			resulthead = result.headString()
			
			if headline.strip() != resulthead.strip():
				start = self.startSentinelComment
				end = self.endSentinelComment
				if end and len(end) > 0:
					# 1/25/03: The kludgy fix.
					# Compare the headlines without the delims.
					h1 =   headline.replace(start,"").replace(end,"")
					h2 = resulthead.replace(start,"").replace(end,"")
					if h1.strip() == h2.strip():
						# 1/25/03: Another kludge: use the headline from the outline, not the derived file.
						headline = resulthead
					else:
						self.structureErrors += 1
				else:
					self.structureErrors += 1
			
			#@-body
			#@-node:1::<< check the headlines >>

		else:
			# This is using a dummy; we should already have bumped structureErrors.
			result = parent.insertAsLastChild(leoNodes.tnode())
		result.initHeadString(headline)
		
		result.setVisited() # Suppress all other errors for this node.
		return result
	#@-body
	#@-node:1::createNthChild
	#@+node:2::joinTrees
	#@+body
	#@+at
	#  This function joins all nodes in the two trees which should have the 
	# same topology. This code makes no other assumptions about the two trees; 
	# some or all of the nodes may already have been joined.
	# 
	# There are several differences between this method and the similar 
	# vnode:joinTreeTo method.  First, we can not assert that the two trees 
	# have the same topology because the derived file could have been edited 
	# outside of Leo.  Second, this method also merges the tnodes of all 
	# joined nodes.

	#@-at
	#@@c
	def joinTrees(self,tree1,tree2):
	
		assert(tree1 and tree2)
		# Use a common tnode for both nodes.
		if tree1.t != tree2.t:
			tree1.setT(tree2.t)
		# Join the roots using the vnode class.
		tree1.joinNodeTo(tree2)
		# Recursively join all subtrees.
		child1 = tree1.firstChild()
		child2 = tree2.firstChild()
		while child1 and child2:
			self.joinTrees(child1, child2)
			child1 = child1.next()
			child2 = child2.next()
		if child1 or child2:
			self.readError("cloned nodes have different topologies")
	#@-body
	#@-node:2::joinTrees
	#@+node:3::atFile.read
	#@+body
	#@+at
	#  This is the entry point to the read code.  The root vnode should be an 
	# @file node.  If doErrorRecoveryFlag is false we are doing an update.  In 
	# that case it would be very unwise to do any error recovery which might 
	# clear clone links.  If doErrorRecoveryFlag is true and there are 
	# structure errors during the first pass we delete root's children and its 
	# body text, then rescan.  All other errors indicate potentially serious 
	# problems with sentinels.
	# 
	# The caller has enclosed this code in beginUpdate/endUpdate.

	#@-at
	#@@c
	def read(self,root):
	
		t1 = getTime()
		c = self.commands
		root.clearVisitedInTree() # Clear the list of nodes for orphans logic.
		if root.isAtFileNode():
			self.targetFileName = root.atFileNodeName()
		else:
			self.targetFileName = root.atRawFileNodeName()
		self.root = root
		self.raw = false
		self.errors = self.structureErrors = 0
		
		#@<< open file >>
		#@+node:1::<< open file >>
		#@+body
		self.scanAllDirectives(root) # 1/30/02
		
		if not self.targetFileName or len(self.targetFileName) == 0:
			self.readError("Missing file name.  Restoring @file tree from .leo file.")
		else:
			# print self.default_directory, self.targetFileName
			fn = os.path.join(self.default_directory, self.targetFileName)
			fn = os.path.normpath(fn)
			fn = toUnicode(fn,"ascii")
			try:
				file = open(fn,'r')
				if file:
					
					#@<< warn on read-only file >>
					#@+node:1::<< warn on read-only file >>
					#@+body
					try:
						read_only = not os.access(fn,os.W_OK)
						if read_only:
							es("read only: " + fn)
					except:
						pass # os.access() may not exist on all platforms.
					
					#@-body
					#@-node:1::<< warn on read-only file >>

			except:
				self.readError("Can not open: " + '"@file ' + fn + '"')
		#@-body
		#@-node:1::<< open file >>

		if self.errors > 0: return 0
		es("reading: " + root.headString())
		
		#@<< Scan the file buffer >>
		#@+node:2::<< Scan the file buffer  >>
		#@+body
		# 14-SEP-2002 DTHEIN: firstLines & lastLines logic.
		# 18-SEP-2002 EKREAM: all body text set in scanText.
		
		firstLines = self.scanHeader(file)
		
		self.indent = 0 ; out = [] ; implicitChildIndex = 0
		lastLines = self.scanText(file,root,out,atFile.endLeo,implicitChildIndex)
		# 18-SEP-2002 DTHEIN: update the bodyString directly, because
		# out no longer holds body text of node.
		if root.t.hasBody:
			bodyLines = root.t.bodyString.split('\n')
			self.completeFirstDirectives(bodyLines,firstLines)
			self.completeLastDirectives(bodyLines,lastLines)
			bodyText = '\n'.join(bodyLines)
			bodyText = bodyText.replace('\r', '')
			root.t.setTnodeText(bodyText)
		
		#@-body
		#@-node:2::<< Scan the file buffer  >>

		
		#@<< Bump mStructureErrors if any vnodes are unvisited >>
		#@+node:3::<< Bump mStructureErrors if any vnodes are unvisited >>
		#@+body
		#@+at
		#  createNthNode marks all nodes in the derived file as visited.  Any 
		# unvisited nodes are either dummies or nodes that don't exist in the 
		# derived file.

		#@-at
		#@@c

		next = root.nodeAfterTree()
		v = root.threadNext()
		while v and v != next:
			if not v.isVisited():
				if 0: # CVS produces to many errors for this to be useful.
					es("unvisited node: " + v.headString())
				self.structureErrors += 1
			v = v.threadNext()
		
		#@-body
		#@-node:3::<< Bump mStructureErrors if any vnodes are unvisited >>

		next = root.nodeAfterTree()
		if self.structureErrors > 0:
			self.readError("-- Rereading file.  Clone links into this file will be lost.") ;
			self.errors = 0
			root.clearVisitedInTree() # Clear the list of nodes for orphans logic.
			
			#@<< Delete root's tree and body text >>
			#@+node:4::<< Delete root's tree and body text >>
			#@+body
			while root.firstChild():
				root.firstChild().doDelete(root)
			
			root.setBodyStringOrPane("")
			#@-body
			#@-node:4::<< Delete root's tree and body text >>

			file.seek(0)
			
			#@<< Scan the file buffer >>
			#@+node:2::<< Scan the file buffer  >>
			#@+body
			# 14-SEP-2002 DTHEIN: firstLines & lastLines logic.
			# 18-SEP-2002 EKREAM: all body text set in scanText.
			
			firstLines = self.scanHeader(file)
			
			self.indent = 0 ; out = [] ; implicitChildIndex = 0
			lastLines = self.scanText(file,root,out,atFile.endLeo,implicitChildIndex)
			# 18-SEP-2002 DTHEIN: update the bodyString directly, because
			# out no longer holds body text of node.
			if root.t.hasBody:
				bodyLines = root.t.bodyString.split('\n')
				self.completeFirstDirectives(bodyLines,firstLines)
				self.completeLastDirectives(bodyLines,lastLines)
				bodyText = '\n'.join(bodyLines)
				bodyText = bodyText.replace('\r', '')
				root.t.setTnodeText(bodyText)
			
			#@-body
			#@-node:2::<< Scan the file buffer  >>

		file.close()
		if self.errors == 0:
			next = root.nodeAfterTree()
			if 0: # 9/26/02: No longer used: derived files contain no clone indices.
				root.clearAllVisitedInTree()
				
				#@<< Handle clone bits >>
				#@+node:5::<< Handle clone bits >>
				#@+body
				h = {}
				v = root
				while v and v != next:
					cloneIndex = v.t.cloneIndex
					# new Leo2: we skip the root node: @file nodes can not be cloned.
					if cloneIndex > 0 and v != root:
						if h.has_key(cloneIndex):
							t = h[cloneIndex]
							# v is a clone: share the previous tnode.
							v.setT(t)
							t.setVisited() # We will mark these clones later.
						else: h[cloneIndex] = v.t
					v = v.threadNext()
				
				# Set clone marks for all visited tnodes.
				v = root
				while v and v != next:
					if v.t.isVisited():
						if v == root:
							pass
						elif v.shouldBeClone():
							v.initClonedBit(true)
						else:
							# Not a serious error.
							es("clone links cleared for: " + v.headString())
							v.unjoinTree();
							t.setCloneIndex(0) # t is no longer cloned.
					v = v.threadNext()
				#@-body
				#@-node:5::<< Handle clone bits >>

				
				#@<< Join cloned trees >>
				#@+node:6::<< Join cloned trees >>
				#@+body
				#@+at
				#  In most cases, this code is not needed, because the outline 
				# already has been read and nodes joined.  However, there 
				# could be problems on read errors, so we also join nodes here.

				#@-at
				#@@c

				h = {}
				v = root
				while v and v != next:
					cloneIndex = v.t.cloneIndex
					# new Leo2: we skip the root node: @file nodes can not be cloned.
					if cloneIndex > 0 and v != root:
						if h.has_key(cloneIndex):
							clone = h[cloneIndex]
							if v.headString() == clone.headString():
								self.joinTrees(clone,v)
							else:
								# An extremely serious error.  Data may be lost.
								self.readError(
									"Outline corrupted: " +
									"different nodes have same clone index!\n\t" +
									v.headString() + "\n\t" + clone.headString())
						# Enter v so we can join the next clone to it.
						# The next call to lookup will find this v, not the previous.
						h[cloneIndex] = v
					v = v.threadNext()
				#@-body
				#@-node:6::<< Join cloned trees >>

			
			#@<< Handle all status bits >>
			#@+node:7::<< Handle all status bits >>
			#@+body
			current = None
			v = root
			while v and v != next:
				if v.isSelected():
					self.commands.tree.currentVnode = current = v
				if v.isTopBitSet():
					# Just tell the open code we have seen the top vnode.
					self.commands.tree.topVnode = v ;
				v = v.threadNext()
			
			if current:
				# Indicate what the current node will be.
				c.tree.currentVnode = current
			
			#@-body
			#@-node:7::<< Handle all status bits >>

		if self.errors > 0:
			# A serious error has occured that has not been corrected.
			self.readError("----- File may have damaged sentinels!")
			root.unjoinTree();
		else: root.clearDirty()
		# esDiffTime("read: exit", t1)
		return self.errors == 0
	#@-body
	#@-node:3::atFile.read
	#@+node:4::readAll (Leo2)
	#@+body
	#@+at
	#  This method scans all vnodes, calling read for every @file node found.  
	# v should point to the root of the entire tree on entry.
	# 
	# Bug fix: 9/19/01 This routine clears all orphan status bits, so we must 
	# set the dirty bit of orphan @file nodes to force the writing of those 
	# nodes on saves.  If we didn't do this, a _second_ save of the .leo file 
	# would effectively wipe out bad @file nodes!
	# 
	# 10/19/01: With the "new" Leo2 there are no such problems, and setting 
	# the dirty bit here is still correct.

	#@-at
	#@@c

	def readAll(self,root,partialFlag):
	
		c = self.commands
		c.endEditing() # Capture the current headline.
		anyRead = false
		self.initIvars()
		v = root
		if partialFlag: after = v.nodeAfterTree()
		else: after = None
		while v and v != after:
			if v.isAtIgnoreNode():
				v = v.nodeAfterTree()
			elif v.isAtFileNode() or v.isAtRawFileNode():
				anyRead = true
				if partialFlag:
					# We are forcing the read.
					self.read(v)
				else:
					# f v is an orphan, we don't expect to see a derived file,
					# and we shall read a derived file if it exists.
					wasOrphan = v.isOrphan()
					ok = self.read(v)
					if wasOrphan and not ok:
						# Remind the user to fix the problem.
						v.setDirty()
						c.setChanged(true)
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		# Clear all orphan bits.
		v = root
		while v:
			v.clearOrphan()
			v = v.threadNext()
			
		if partialFlag and not anyRead:
			es("no @file nodes in the selected tree")
	#@-body
	#@-node:4::readAll (Leo2)
	#@+node:5::readLine
	#@+body
	def readLine (self,file):
		"""Reads one line from file using the present encoding"""
		
		s = readlineForceUnixNewline(file)
		u = toUnicode(s,self.encoding)
		return u
	
	
	#@-body
	#@-node:5::readLine
	#@+node:6::scanDoc
	#@+body
	# Scans the doc part and appends the text out.
	# s,i point to the present line on entry.
	
	def scanDoc(self,file,s,i,out,kind):
	
		endKind = choose(kind == atFile.startDoc, atFile.endDoc, atFile.endAt)
		single = len(self.endSentinelComment) == 0
		
		#@<< Skip the opening sentinel >>
		#@+node:1::<< Skip the opening sentinel >>
		#@+body
		assert(match(s,i,choose(kind == atFile.startDoc, "+doc", "+at")))
		
		out.append(choose(kind == atFile.startDoc, "@doc", "@"))
		s = self.readLine(file)
		
		#@-body
		#@-node:1::<< Skip the opening sentinel >>

		
		#@<< Skip an opening block delim >>
		#@+node:2::<< Skip an opening block delim >>
		#@+body
		if not single:
			j = skip_ws(s,0)
			if match(s,j,self.startSentinelComment):
				s = self.readLine(file)
		#@-body
		#@-node:2::<< Skip an opening block delim >>

		nextLine = None ; kind = atFile.noSentinel
		while len(s) > 0:
			
			#@<< set kind, nextLine >>
			#@+node:3::<< set kind, nextLine >>
			#@+body
			#@+at
			#  For non-sentinel lines we look ahead to see whether the next 
			# line is a sentinel.

			#@-at
			#@@c

			assert(nextLine==None)
			
			kind = self.sentinelKind(s)
			
			if kind == atFile.noSentinel:
				j = skip_ws(s,0)
				blankLine = s[j] == '\n'
				nextLine = self.readLine(file)
				nextKind = self.sentinelKind(nextLine)
				if blankLine and nextKind == endKind:
					kind = endKind # stop the scan now
			
			#@-body
			#@-node:3::<< set kind, nextLine >>

			if kind == endKind: break
			
			#@<< Skip the leading stuff >>
			#@+node:4::<< Skip the leading stuff >>
			#@+body
			# Point i to the start of the real line.
			
			if single: # Skip the opening comment delim and a blank.
				i = skip_ws(s,0)
				if match(s,i,self.startSentinelComment):
					i += len(self.startSentinelComment)
					if match(s,i," "): i += 1
			else:
				i = self.skipIndent(s,0, self.indent)
			
			#@-body
			#@-node:4::<< Skip the leading stuff >>

			
			#@<< Append s to out >>
			#@+node:5::<< Append s to out >>
			#@+body
			# Append the line with a newline if it is real
			
			line = s[i:-1] # remove newline for rstrip.
			
			if line == line.rstrip():
				# no trailing whitespace: the newline is real.
				out.append(line + '\n')
			else:
				# trailing whitespace: the newline is not real.
				out.append(line)
			
			#@-body
			#@-node:5::<< Append s to out >>

			if nextLine:
				s = nextLine ; nextLine = None
			else: s = self.readLine(file)
		if kind != endKind:
			self.readError("Missing " + self.sentinelName(endKind) + " sentinel")
		
		#@<< Remove a closing block delim from out >>
		#@+node:6::<< Remove a closing block delim from out >>
		#@+body
		# This code will typically only be executed for HTML files.
		
		if not single:
		
			delim = self.endSentinelComment
			n = len(delim)
			
			# Remove delim and possible a leading newline.
			s = string.join(out,"")
			s = s.rstrip()
			if s[-n:] == delim:
				s = s[:-n]
			if s[-1] == '\n':
				s = s[:-1]
				
			# Rewrite out in place.
			del out[:]
			out.append(s)
		
		#@-body
		#@-node:6::<< Remove a closing block delim from out >>
	#@-body
	#@-node:6::scanDoc
	#@+node:7::scanHeader
	#@+body
	#@+at
	#  This method sets self.startSentinelComment and self.endSentinelComment 
	# based on the first @+leo sentinel line of the file.  We can not call 
	# sentinelKind here because that depends on the comment delimiters we set 
	# here.  @first lines are written "verbatim", so nothing more needs to be done!
	# 
	# 7/8/02: Leading whitespace is now significant here before the @+leo.  
	# This is part of the "REM hack".  We do this so that sentinelKind need 
	# not skip whitespace following self.startSentinelComment.  This is 
	# correct: we want to be as restrictive as possible about what is 
	# recognized as a sentinel.  This minimizes false matches.
	# 
	# 14-SEP-2002 DTHEIN:  Queue up the lines before the @+leo.  These will be 
	# used to add as parameters to the @first directives, if any.  Empty lines 
	# are ignored (because empty @first directives are ignored). NOTE: the 
	# function now returns a list of the lines before @+leo.

	#@-at
	#@@c
	def scanHeader(self,file):
	
		valid = true
		tag = "@+leo"
		encoding_tag = "-encoding="
		
		#@<< skip any non @+leo lines >>
		#@+node:1::<< skip any non @+leo lines >>
		#@+body
		firstLines = [] # The lines before @+leo.
		s = self.readLine(file)
		while len(s) > 0:
			j = s.find(tag)
			if j != -1: break
			firstLines.append(s) # Queue the line
			s = self.readLine(file)
		n = len(s)
		valid = n > 0
		# s contains the tag
		i = j = skip_ws(s,0)
		# The opening comment delim is the initial non-whitespace.
		# 7/8/02: The opening comment delim is the initial non-tag
		while i < n and not match(s,i,tag) and not is_nl(s,i):
			i += 1
		if j < i:
			self.startSentinelComment = s[j:i]
		else: valid = false
		#@-body
		#@-node:1::<< skip any non @+leo lines >>

		
		#@<< make sure we have @+leo >>
		#@+node:2::<< make sure we have @+leo >>
		#@+body
		if 0:# 7/8/02: make leading whitespace significant.
			i = skip_ws(s,i)
		
		if match(s,i,tag):
			i += len(tag)
		else: valid = false
		#@-body
		#@-node:2::<< make sure we have @+leo >>

		
		#@<< read optional encoding param >>
		#@+node:3::<< read optional encoding param >>
		#@+body
		# 1/20/03: EKR: Read optional encoding param, e.g., -encoding=utf-8,
		
		# Set the default encoding
		self.encoding = app().config.default_derived_file_encoding
		
		if match(s,i,encoding_tag):
			i += len(encoding_tag)
			# Skip to the next comma
			j = i
			while i < len(s) and not is_nl(s,i) and s[i] not in (',','.'):
				i += 1
			if match(s,i,',') or match(s,i,'.'):
				encoding = s[j:i]
				i += 1
				# print "@+leo-encoding=",encoding
				if isValidEncoding(encoding):
					self.encoding = encoding
				else:
					es("bad encoding in derived file:",encoding)
			else:
				valid = false
		
		#@-body
		#@-node:3::<< read optional encoding param >>

		
		#@<< set the closing comment delim >>
		#@+node:4::<< set the closing comment delim >>
		#@+body
		# The closing comment delim is the trailing non-whitespace.
		i = j = skip_ws(s,i)
		while i < n and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		self.endSentinelComment = s[j:i]
		#@-body
		#@-node:4::<< set the closing comment delim >>

		if not valid:
			self.readError("Bad @+leo sentinel in " + self.targetFileName)
		return firstLines
	#@-body
	#@-node:7::scanHeader
	#@+node:8::completeFirstDirectives (Dave Hein)
	#@+body
	# 14-SEP-2002 DTHEIN: added for use by atFile.read()
	
	# this function scans the lines in the list 'out' for @first directives
	# and appends the corresponding line from 'firstLines' to each @first 
	# directive found.  NOTE: the @first directives must be the very first
	# lines in 'out'.
	def completeFirstDirectives(self,out,firstLines):
	
		tag = "@first"
		foundAtFirstYet = 0
		outRange = range(len(out))
		j = 0
		for k in outRange:
			# skip leading whitespace lines
			if (not foundAtFirstYet) and (len(out[k].strip()) == 0): continue
			# quit if something other than @first directive
			i = 0
			if not match(out[k],i,tag): break;
			foundAtFirstYet = 1
			# quit if no leading lines to apply
			if j >= len(firstLines): break
			# make the new @first directive
			#18-SEP-2002 DTHEIN: remove trailing newlines because they are inserted later
			# 21-SEP-2002 DTHEIN: no trailing whitespace on empty @first directive
			leadingLine = " " + firstLines[j]
			out[k] = tag + leadingLine.rstrip() ; j += 1
	
	#@-body
	#@-node:8::completeFirstDirectives (Dave Hein)
	#@+node:9::completeLastDirectives (Dave Hein)
	#@+body
	# 14-SEP-2002 DTHEIN: added for use by atFile.read()
	
	# this function scans the lines in the list 'out' for @last directives
	# and appends the corresponding line from 'lastLines' to each @last 
	# directive found.  NOTE: the @first directives must be the very last
	# lines in 'out'.
	def completeLastDirectives(self,out,lastLines):
	
		tag = "@last"
		foundAtLastYet = 0
		outRange = range(-1,-len(out),-1)
		j = -1
		for k in outRange:
			# skip trailing whitespace lines
			if (not foundAtLastYet) and (len(out[k].strip()) == 0): continue
			# quit if something other than @last directive
			i = 0
			if not match(out[k],i,tag): break;
			foundAtLastYet = 1
			# quit if no trailing lines to apply
			if j < -len(lastLines): break
			# make the new @last directive
			#18-SEP-2002 DTHEIN: remove trailing newlines because they are inserted later
			# 21-SEP-2002 DTHEIN: no trailing whitespace on empty @last directive
			trailingLine = " " + lastLines[j]
			out[k] = tag + trailingLine.rstrip() ; j -= 1
	
	#@-body
	#@-node:9::completeLastDirectives (Dave Hein)
	#@+node:10::scanText
	#@+body
	#@+at
	#  This method is the heart of the new read code.  It reads lines from the 
	# file until the given ending sentinel is found, and warns if any other 
	# ending sentinel is found instead.  It calls itself recursively to handle 
	# most nested sentinels.
	# 

	#@-at
	#@@c
	def scanText (self,file,v,out,endSentinelKind,implicitChildIndex):
	
		c = self.commands ; config = app().config
		lastLines = [] # 14-SEP-2002 DTHEIN: the last lines, after @-leo
		lineIndent = 0 ; linep = 0 # Changed only for sentinels.
		nextLine = None
	
		while 1:
			if nextLine:
				s = nextLine ; nextLine = None
			else:
				s = self.readLine(file) # EKR: 1/21/03
				if len(s) == 0: break
			# trace(`s`)
			
			#@<< set kind, nextKind >>
			#@+node:1::<< set kind, nextKind >>
			#@+body
			#@+at
			#  For non-sentinel lines we look ahead to see whether the next 
			# line is a sentinel.  If so, the newline that ends a non-sentinel 
			# line belongs to the next sentinel.

			#@-at
			#@@c

			assert(nextLine==None)
			
			kind = self.sentinelKind(s)
			
			if kind == atFile.noSentinel:
				nextLine = self.readLine(file)
				nextKind = self.sentinelKind(nextLine)
			else:
				nextLine = nextKind = None
			
			# nextLine != None only if we have a non-sentinel line.
			# Therefore, nextLine == None whenever scanText returns.
			#@-body
			#@-node:1::<< set kind, nextKind >>

			if kind != atFile.noSentinel:
				
				#@<< set lineIndent, linep and leading_ws >>
				#@+node:2::<< Set lineIndent, linep and leading_ws >>
				#@+body
				#@+at
				#  lineIndent is the total indentation on a sentinel line.  
				# The first "self.indent" portion of that must be removed when 
				# recreating text.  leading_ws is the remainder of the leading 
				# whitespace.  linep points to the first "real" character of a 
				# line, the character following the "indent" whitespace.

				#@-at
				#@@c

				# Point linep past the first self.indent whitespace characters.
				if self.raw: # 10/15/02
					linep =0
				else:
					linep = self.skipIndent(s,0,self.indent)
				
				# Set lineIndent to the total indentation on the line.
				lineIndent = 0 ; i = 0
				while i < len(s):
					if s[i] == '\t': lineIndent += (abs(self.tab_width) - (lineIndent % abs(self.tab_width)))
					elif s[i] == ' ': lineIndent += 1
					else: break
					i += 1
				# trace("lineIndent:" +`lineIndent` + ", " + `s`)
				
				# Set leading_ws to the additional indentation on the line.
				leading_ws = s[linep:i]
				#@-body
				#@-node:2::<< Set lineIndent, linep and leading_ws >>

				i = self.skipSentinelStart(s,0)
			# All cases must appear here so we can set the next line properly below.
			if kind == atFile.noSentinel:
				
				#@<< append non-sentinel line >>
				#@+node:3::<< append non-sentinel line >>
				#@+body
				# We don't output the trailing newline if the next line is a sentinel.
				if self.raw: # 10/15/02
					i = 0
				else:
					i = self.skipIndent(s,0,self.indent)
				
				assert(nextLine != None)
				
				if nextKind == atFile.noSentinel:
					line = s[i:]
					out.append(line)
				else:
					line = s[i:-1] # don't output the newline
					out.append(line)
				
				#@-body
				#@-node:3::<< append non-sentinel line >>

			elif kind == atFile.startAt:
				
				#@<< scan @+at >>
				#@+node:6::start sentinels
				#@+node:1::<< scan @+at >>
				#@+body
				assert(match(s,i,"+at"))
				self.scanDoc(file,s,i,out,kind)
				#@-body
				#@-node:1::<< scan @+at >>
				#@-node:6::start sentinels

			elif kind == atFile.startBody:
				
				#@<< scan @+body >>
				#@+node:6::start sentinels
				#@+node:2::<< scan @+body >> (revised read code)
				#@+body
				assert(match(s,i,"+body"))
				
				child_out = [] ; child = v # Do not change out or v!
				oldIndent = self.indent ; self.indent = lineIndent
				self.scanText(file,child,child_out,atFile.endBody,implicitChildIndex)
				
				if child.isOrphan():
					self.readError("Replacing body text of orphan: " + child.headString())
				
				# Set the body, removing cursed newlines.
				# Note:  This code must be done here, not in the @+node logic.
				body = string.join(child_out, "")
				body = body.replace('\r', '')
				child.t.setTnodeText(body)
				self.indent = oldIndent
				#@-body
				#@-node:2::<< scan @+body >> (revised read code)
				#@-node:6::start sentinels

			elif kind == atFile.startDelims:
				
				#@<< scan @delims >>
				#@+node:7::unpaired sentinels
				#@+node:3::<< scan @delims >>
				#@+body
				assert(match(s,i-1,"@delims"));
				
				# Skip the keyword and whitespace.
				i0 = i-1
				i = skip_ws(s,i-1+7)
					
				# Get the first delim.
				j = i
				while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
					i += 1
				
				if j < i:
					self.startSentinelComment = s[j:i]
					# print "delim1:", self.startSentinelComment
				
					# Get the optional second delim.
					j = i = skip_ws(s,i)
					while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
						i += 1
					end = choose(j<i,s[j:i],"")
					i2 = skip_ws(s,i)
					if end == self.endSentinelComment and (i2 >= len(s) or is_nl(s,i2)):
						self.endSentinelComment = "" # Not really two params.
						line = s[i0:j]
						line = line.rstrip()
						out.append(line+'\n')
					else:
						self.endSentinelComment = end
						# print "delim2:",end
						line = s[i0:i]
						line = line.rstrip()
						out.append(line+'\n')
				else:
					self.readError("Bad @delims")
					# Append the bad @delims line to the body text.
					out.append("@delims")
				#@-body
				#@-node:3::<< scan @delims >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startDirective:
				
				#@<< scan @@ >>
				#@+node:7::unpaired sentinels
				#@+node:1::<< scan @@ >>
				#@+body
				# The first '@' has already been eaten.
				assert(match(s,i,"@"))
				
				if match_word(s,i,"@raw"):
					self.raw = true
				elif match_word(s,i,"@end_raw"):
					self.raw = false
				
				e = self.endSentinelComment
				s2 = s[i:]
				if len(e) > 0:
					k = s.rfind(e,i)
					if k != -1:
						s2 = s[i:k] + '\n'
					
				start = self.startSentinelComment
				if start and len(start) > 0 and start[-1] == '@':
					s2 = s2.replace('@@','@')
				out.append(s2)
				# trace(`s2`)
				#@-body
				#@-node:1::<< scan @@ >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startDoc:
				
				#@<< scan @+doc >>
				#@+node:6::start sentinels
				#@+node:3::<< scan @+doc >>
				#@+body
				assert(match(s,i,"+doc"))
				self.scanDoc(file,s,i,out,kind)
				#@-body
				#@-node:3::<< scan @+doc >>
				#@-node:6::start sentinels

			elif kind == atFile.startLeo:
				
				#@<< scan @+leo >>
				#@+node:6::start sentinels
				#@+node:4::<< scan @+leo >>
				#@+body
				assert(match(s,i,"+leo"))
				self.readError("Ignoring unexpected @+leo sentinel")
				#@-body
				#@-node:4::<< scan @+leo >>
				#@-node:6::start sentinels

			elif kind == atFile.startNode:
				
				#@<< scan @+node >>
				#@+node:6::start sentinels
				#@+node:5::<< scan @+node >> (revised read code)
				#@+body
				assert(match(s,i,"+node:"))
				i += 6
				
				childIndex = 0 ; cloneIndex = 0
				
				#@<< Set childIndex >>
				#@+node:1::<< Set childIndex >>
				#@+body
				i = skip_ws(s,i) ; j = i
				while i < len(s) and s[i] in string.digits:
					i += 1
				
				if j == i:
					implicitChildIndex += 1
					childIndex = implicitChildIndex
				else:
					childIndex = int(s[j:i])
				
				if match(s,i,':'):
					i += 1 # Skip the ":".
				else:
					self.readError("Bad child index in @+node")
				#@-body
				#@-node:1::<< Set childIndex >>

				
				#@<< Set cloneIndex >>
				#@+node:2::<< Set cloneIndex >>
				#@+body
				while i < len(s) and s[i] != ':' and not is_nl(s,i):
					if match(s,i,"C="):
						# set cloneIndex from the C=nnn, field
						i += 2 ; j = i
						while i < len(s) and s[i] in string.digits:
							i += 1
						if j < i:
							cloneIndex = int(s[j:i])
					else: i += 1 # Ignore unknown status bits.
				
				if match(s,i,":"):
					i += 1
				else:
					self.readError("Bad attribute field in @+node")
				#@-body
				#@-node:2::<< Set cloneIndex >>

				headline = ""
				
				#@<< Set headline and ref >>
				#@+node:3::<< Set headline and ref >>
				#@+body
				# Set headline to the rest of the line.
				if len(self.endSentinelComment) == 0:
					headline = string.strip(s[i:-1])
				else:
					# 10/24/02: search from the right, not the left.
					k = s.rfind(self.endSentinelComment,i)
					headline = string.strip(s[i:k]) # works if k == -1
					
				# 10/23/02: The cweb hack: undouble @ signs if the opening comment delim ends in '@'.
				if self.startSentinelComment[-1:] == '@':
					headline = headline.replace('@@','@')
				
				# Set reference if it exists.
				i = skip_ws(s,i)
				
				if 0: # no longer used
					if match(s,i,"<<"):
						k = s.find(">>",i)
						if k != -1: ref = s[i:k+2]
				#@-body
				#@-node:3::<< Set headline and ref >>

				
				# print childIndex,headline
				
				if childIndex == 0: # The root node.
					
					#@<< Check the filename in the sentinel >>
					#@+node:4::<< Check the filename in the sentinel >>
					#@+body
					h = headline.strip()
					
					if h[:5] == "@file":
						i,junk = scanAtFileOptions(h)
						fileName = string.strip(h[i:])
						if fileName != self.targetFileName:
							self.readError("File name in @node sentinel does not match file's name")
					elif h[:8] == "@rawfile":
						fileName = string.strip(h[8:])
						if fileName != self.targetFileName:
							self.readError("File name in @node sentinel does not match file's name")
					else:
						self.readError("Missing @file in root @node sentinel")
					
					#@-body
					#@-node:4::<< Check the filename in the sentinel >>

					# Put the text of the root node in the current node.
					self.scanText(file,v,out,atFile.endNode,implicitChildIndex)
					v.t.setCloneIndex(cloneIndex)
					# if cloneIndex > 0: trace("clone index:" + `cloneIndex` + ", " + `v`)
				else:
					# NB: this call to createNthChild is the bottleneck!
					child = self.createNthChild(childIndex,v,headline)
					child.t.setCloneIndex(cloneIndex)
					# if cloneIndex > 0: trace("clone index:" + `cloneIndex` + ", " + `child`)
					self.scanText(file,child,out,atFile.endNode,implicitChildIndex)
				
				
				#@<< look for sentinels that may follow a reference >>
				#@+node:5::<< look for sentinels that may follow a reference >>
				#@+body
				s = self.readLine(file)
				kind = self.sentinelKind(s)
				
				if len(s) > 1 and kind == atFile.startVerbatimAfterRef:
					s = self.readLine(file)
					# trace("verbatim:"+`s`)
					out.append(s)
				elif kind == atFile.startNewline:
					out.append('\n')
					s = self.readLine(file)
					nextline = s
					# trace(`s`)
				elif kind == atFile.startNoNewline:
					s = self.readLine(file)
					nextline = s
				elif len(s) > 1 and self.sentinelKind(s) == atFile.noSentinel:
					out.append(s)
				else:
					nextLine = s # Handle the sentinel or blank line later.
				
				#@-body
				#@-node:5::<< look for sentinels that may follow a reference >>
				#@-body
				#@-node:5::<< scan @+node >> (revised read code)
				#@-node:6::start sentinels

			elif kind == atFile.startOthers:
				
				#@<< scan @+others >>
				#@+node:6::start sentinels
				#@+node:6::<< scan @+others >>
				#@+body
				assert(match(s,i,"+others"))
				
				# Make sure that the generated at-others is properly indented.
				if 0: # # 9/27/02
					out.append('\n')
				out.append(leading_ws + "@others")
				
				# 9/26/02: @others temporarily resets the implicit child index.
				oldImplicitChildIndex = implicitChildIndex
				implicitChildIndex = 0
				self.scanText(file,v,out,atFile.endOthers,implicitChildIndex)
				implicitChildIndex = oldImplicitChildIndex
				#@-body
				#@-node:6::<< scan @+others >>
				#@-node:6::start sentinels

			elif kind == atFile.startRef:
				
				#@<< scan @ref >>
				#@+node:7::unpaired sentinels
				#@+node:4::<< scan @ref >>
				#@+body
				#@+at
				#  The sentinel contains an @ followed by a section name in 
				# angle brackets.  This code is different from the code for 
				# the @@ sentinel: the expansion of the reference does not 
				# include a trailing newline.

				#@-at
				#@@c

				assert(match(s,i,"<<"))
				
				if len(self.endSentinelComment) == 0:
					line = s[i:-1] # No trailing newline
				else:
					k = s.find(self.endSentinelComment,i)
					line = s[i:k] # No trailing newline, whatever k is.
						
				# 10/30/02: undo cweb hack here
				start = self.startSentinelComment
				if start and len(start) > 0 and start[-1] == '@':
					line = line.replace('@@','@')
				
				out.append(line)
				#@-body
				#@-node:4::<< scan @ref >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startVerbatim:
				
				#@<< scan @verbatim >>
				#@+node:7::unpaired sentinels
				#@+node:5::<< scan @verbatim >>
				#@+body
				assert(match(s,i,"verbatim"))
				
				# Skip the sentinel.
				s = self.readLine(file) 
				
				# Append the next line to the text.
				i = self.skipIndent(s,0,self.indent)
				out.append(s[i:])
				
				#@-body
				#@-node:5::<< scan @verbatim >>
				#@-node:7::unpaired sentinels

			elif kind == atFile.startComment:
				
				#@<< scan @comment >>
				#@+node:7::unpaired sentinels
				#@+node:2::<< scan @comment >>
				#@+body
				assert(match(s,i,"comment"))
				
				# We need do nothing more to ignore the comment line!
				
				#@-body
				#@-node:2::<< scan @comment >>
				#@-node:7::unpaired sentinels

			elif ( kind == atFile.endAt or kind == atFile.endBody or
				kind == atFile.endDoc or kind == atFile.endLeo or
				kind == atFile.endNode or kind == atFile.endOthers ):
				
				#@<< handle an ending sentinel >>
				#@+node:4::<< handle an ending sentinel >> (new read code)
				#@+body
				if kind == endSentinelKind:
					if kind == atFile.endLeo:
						# 9/11/02: ignore everything after @-leo.
						# Such lines were presumably written by @last
						while 1:
							s = self.readLine(file)
							if len(s) == 0: break
							# 21-SEP-2002 DTHEIN: capture _all_ the trailing lines, even if empty
							lastLines.append(s) # 14-SEP-2002 DTHEIN: capture the trailing lines
					elif kind == atFile.endBody:
						self.raw = false
					# nextLine != None only if we have a non-sentinel line.
					# Therefore, nextLine == None whenever scanText returns.
					assert(nextLine==None)
					return lastLines # 14-SEP-2002 DTHEIN: return the captured lines after @-leo
				else:
					# Tell of the structure error.
					name = self.sentinelName(kind)
					expect = self.sentinelName(endSentinelKind)
					self.readError("Ignoring " + name + " sentinel.  Expecting " + expect)
				#@-body
				#@-node:4::<< handle an ending sentinel >> (new read code)

			else:
				
				#@<< warn about unknown sentinel >>
				#@+node:8::<< warn about unknown sentinel >>
				#@+body
				j = i
				i = skip_line(s,i)
				line = s[j:i]
				self.readError("Unknown sentinel: " + line)
				#@-body
				#@-node:8::<< warn about unknown sentinel >>

		
		#@<< handle unexpected end of text >>
		#@+node:5::<< handle unexpected end of text >>
		#@+body
		# Issue the error.
		name = self.sentinelName(endSentinelKind)
		self.readError("Unexpected end of file. Expecting " + name + "sentinel" )
		
		#@-body
		#@-node:5::<< handle unexpected end of text >>

		assert(len(s)==0 and nextLine==None) # We get here only if readline fails.
		return lastLines # 14-SEP-2002 DTHEIN: shouldn't get here unless problems
	#@-body
	#@+node:6::start sentinels
	#@-node:6::start sentinels
	#@+node:7::unpaired sentinels
	#@-node:7::unpaired sentinels
	#@-node:10::scanText
	#@-node:5::Reading
	#@+node:6::Writing
	#@+node:1::atFile.checkForLeoCustomize
	#@+body
	# Check file given by v, or self.targetFileName if v == None.
	
	def checkForLeoCustomize (self,v=None):
	
		return true # This routine is no longer needed.
	#@-body
	#@-node:1::atFile.checkForLeoCustomize
	#@+node:2::atFile.closeWriteFile
	#@+body
	def closeWriteFile (self):
		
		if self.outputFile:
			if self.suppress_newlines and self.newline_pending:
				self.newline_pending = false
				self.onl() # Make sure file ends with a newline.
			self.outputFile.flush()
			self.outputFile.close()
			self.outputFile = None
	
	#@-body
	#@-node:2::atFile.closeWriteFile
	#@+node:3::atFile.handleWriteException
	#@+body
	def handleWriteException (self,root=None):
		
		es("exception writing:" + self.targetFileName)
		es_exception()
		
		if self.outputFile:
			self.outputFile.flush()
			self.outputFile.close()
			self.outputFile = None
		
		if self.outputFileName != None:
			try: # Just delete the temp file.
				os.remove(self.outputFileName)
			except:
				es("exception deleting:" + self.outputFileName)
				es_exception()
	
		if root:
			# Make sure we try to rewrite this file.
			root.setOrphan()
			root.setDirty()
	#@-body
	#@-node:3::atFile.handleWriteException
	#@+node:4::atFile.openWriteFile (assert)
	#@+body
	# Open files.  Set root.orphan and root.dirty flags and return on errors.
	
	def openWriteFile (self,root):
	
		try:
			self.scanAllDirectives(root)
			valid = self.errors == 0
		except:
			es("exception in atFile.scanAllDirectives")
			es_exception()
			valid = false
		
		if valid:
			try:
				fn = self.targetFileName
				self.shortFileName = fn # name to use in status messages.
				self.targetFileName = os.path.join(self.default_directory,fn)
				self.targetFileName = os.path.normpath(self.targetFileName)
				path = os.path.dirname(self.targetFileName)
				if path and len(path) > 0:
					valid = os.path.exists(path)
					if not valid:
						self.writeError("path does not exist: " + path)
				else:
					valid = false
			except:
				es("exception creating path:" + fn)
				es_exception()
				valid = false
		
		if valid:
			if os.path.exists(self.targetFileName):
				try:
					read_only = not os.access(self.targetFileName,os.W_OK)
					if read_only:
						es("read only: " + self.targetFileName)
						valid = false
				except:
					pass # os.access() may not exist on all platforms.
			
		if valid:
			try:
				self.outputFileName = self.targetFileName + ".tmp"
				self.outputFile = open(self.outputFileName,'wb')
				valid = self.outputFile != None
				if not valid:
					self.writeError("can not open " + self.outputFileName)
			except:
				es("exception opening:" + self.outputFileName)
				es_exception()
				valid = false
		
		if not valid:
			root.setOrphan()
			root.setDirty()
		
		return valid
	#@-body
	#@-node:4::atFile.openWriteFile (assert)
	#@+node:5::atFile.rawWrite
	#@+body
	def rawWrite(self,root):
	
		# trace(`root`)
		c = self.commands ; self.root = root
		self.errors = 0
		c.endEditing() # Capture the current headline.
		try:
			self.targetFileName = root.atRawFileNodeName()
			ok = self.openWriteFile(root)
			if not ok: return
			next = root.nodeAfterTree()
			
			#@<< write root's tree >>
			#@+node:1::<< write root's tree >>
			#@+body
			next = root.nodeAfterTree()
			self.updateCloneIndices(root, next)
			
			
			#@<< put all @first lines in root >>
			#@+node:1::<< put all @first lines in root >>
			#@+body
			#@+at
			#  Write any @first lines.  These lines are also converted to 
			# @verbatim lines, so the read logic simply ignores lines 
			# preceding the @+leo sentinel.

			#@-at
			#@@c

			s = root.t.bodyString
			tag = "@first"
			i = 0
			while match(s,i,tag):
				i += len(tag)
				i = skip_ws(s,i)
				j = i
				i = skip_to_end_of_line(s,i)
				# 21-SEP-2002 DTHEIN: write @first line, whether empty or not
				line = s[j:i]
				self.os(line) ; self.onl()
				i = skip_nl(s,i)
			#@-body
			#@-node:1::<< put all @first lines in root >>

			self.putOpenLeoSentinel("@+leo")
			
			#@<< put optional @comment sentinel lines >>
			#@+node:2::<< put optional @comment sentinel lines >>
			#@+body
			s2 = app().config.output_initial_comment
			if s2:
				lines = string.split(s2,"\\n")
				for line in lines:
					line = line.replace("@date",time.asctime())
					if len(line)> 0:
						self.putSentinel("@comment " + line)
			
			#@-body
			#@-node:2::<< put optional @comment sentinel lines >>

			
			v = root
			while v and v != next:
				
				#@<< Write v's node >>
				#@+node:3::<< Write v's node >>
				#@+body
				self.putOpenNodeSentinel(v)
					
				s = v.bodyString()
				if s and len(s) > 0:
					self.putSentinel("@+body")
					if self.newline_pending:
						self.newline_pending = false
						self.onl()
					self.outputFile.write(s)
					self.putSentinel("@-body")
					
				self.putCloseNodeSentinel(v)
				
				#@-body
				#@-node:3::<< Write v's node >>

				v = v.threadNext()
			
			self.putSentinel("@-leo")
			
			#@<< put all @last lines in root >>
			#@+node:4::<< put all @last lines in root >>
			#@+body
			#@+at
			#  Write any @last lines.  These lines are also converted to 
			# @verbatim lines, so the read logic simply ignores lines 
			# following the @-leo sentinel.

			#@-at
			#@@c

			tag = "@last"
			lines = string.split(root.t.bodyString,'\n')
			n = len(lines) ; j = k = n - 1
			# Don't write an empty last line.
			if j >= 0 and len(lines[j])==0:
				j = k = n - 2
			# Scan backwards for @last directives.
			while j >= 0:
				line = lines[j]
				if match(line,0,tag): j -= 1
				else: break
			# Write the @last lines.
			for line in lines[j+1:k+1]:
				i = len(tag) ; i = skip_ws(line,i)
				self.os(line[i:]) ; self.onl()
			#@-body
			#@-node:4::<< put all @last lines in root >>
			#@-body
			#@-node:1::<< write root's tree >>

			self.closeWriteFile()
			self.replaceTargetFileIfDifferent()
			root.clearOrphan() ; root.clearDirty()
		except:
			self.handleWriteException(root)
	#@-body
	#@-node:5::atFile.rawWrite
	#@+node:6::atFile.replaceTargetFileIfDifferent
	#@+body
	def replaceTargetFileIfDifferent (self):
		
		assert(self.outputFile == None)
		
		if os.path.exists(self.targetFileName):
			if filecmp.cmp(self.outputFileName,self.targetFileName):
				
				#@<< delete the output file >>
				#@+node:1::<< delete the output file >>
				#@+body
				try: # Just delete the temp file.
					os.remove(self.outputFileName)
				except:
					es("exception deleting:" + self.outputFileName)
					es_exception()
				
				es("unchanged: " + self.shortFileName)
				#@-body
				#@-node:1::<< delete the output file >>

			else:
				if self.checkForLeoCustomize() == false:
					return
				
				#@<< replace the target file with the output file >>
				#@+node:2::<< replace the target file with the output file >>
				#@+body
				try:
					# 10/6/02: retain the access mode of the previous file,
					# removing any setuid, setgid, and sticky bits.
					mode = (os.stat(self.targetFileName))[0] & 0777
				except:
					mode = None
				
				try: # Replace target file with temp file.
					os.remove(self.targetFileName)
					utils_rename(self.outputFileName,self.targetFileName)
					if mode: # 10/3/02: retain the access mode of the previous file.
						os.chmod(self.targetFileName,mode)
					es("writing: " + self.shortFileName)
				except:
					self.writeError("exception removing and renaming:" + self.outputFileName +
						" to " + self.targetFileName)
					es_exception()
				#@-body
				#@-node:2::<< replace the target file with the output file >>

				
		elif self.checkForLeoCustomize() == false:
			return
		else:
			
			#@<< rename the output file to be the target file >>
			#@+node:3::<< rename the output file to be the target file >>
			#@+body
			try:
				utils_rename(self.outputFileName,self.targetFileName)
				es("creating: " + self.targetFileName)
			except:
				self.writeError("exception renaming:" + self.outputFileName +
					" to " + self.targetFileName)
				es_exception()
			#@-body
			#@-node:3::<< rename the output file to be the target file >>

	
	#@-body
	#@-node:6::atFile.replaceTargetFileIfDifferent
	#@+node:7::atFile.silentWrite
	#@+body
	def silentWrite(self,root):
	
		# trace(`root`)
		c = self.commands ; self.root = root
		self.errors = 0
		c.endEditing() # Capture the current headline.
		try:
			self.targetFileName = root.atSilentFileNodeName()
			ok = self.openWriteFile(root)
			if not ok: return
			next = root.nodeAfterTree()
			v = root
			while v and v != next:
				
				#@<< Write v's headline if it starts with @@ >>
				#@+node:1::<< Write v's headline if it starts with @@ >>
				#@+body
				s = v.headString()
				if match(s,0,"@@"):
					s = s[2:]
					if s and len(s) > 0:
						self.outputFile.write(s)
				
				#@-body
				#@-node:1::<< Write v's headline if it starts with @@ >>

				
				#@<< Write v's body >>
				#@+node:2::<< Write v's body >>
				#@+body
				s = v.bodyString()
				if s and len(s) > 0:
					self.outputFile.write(s)
				#@-body
				#@-node:2::<< Write v's body >>

				v = v.threadNext()
			self.closeWriteFile()
			self.replaceTargetFileIfDifferent()
			root.clearOrphan() ; root.clearDirty()
		except:
			self.handleWriteException(root)
	#@-body
	#@-node:7::atFile.silentWrite
	#@+node:8::atFile.write
	#@+body
	# This is the entry point to the write code.  root should be an @file vnode.
	
	def write(self,root,nosentinels=false):
	
		c = self.commands
		self.sentinels = not nosentinels
		
		#@<< initialize >>
		#@+node:1::<< initialize >>
		#@+body
		self.errors = 0 # 9/26/02
		c.setIvarsFromPrefs()
		self.root = root
		self.raw = false
		c.endEditing() # Capture the current headline.
		
		#@-body
		#@-node:1::<< initialize >>

		try:
			
			#@<< open the file; return on error >>
			#@+node:2::<< open the file; return on error >>
			#@+body
			if nosentinels:
				self.targetFileName = root.atNoSentinelsFileNodeName()
			else:
				self.targetFileName = root.atFileNodeName()
			ok = self.openWriteFile(root)
			if not ok: return
			#@-body
			#@-node:2::<< open the file; return on error >>

			
			#@<< write then entire @file tree >>
			#@+node:3::<< write then entire @file tree >>
			#@+body
			# unvisited nodes will be orphans, except in cweb trees.
			root.clearVisitedInTree()
			next = root.nodeAfterTree()
			self.updateCloneIndices(root, next)
			
			
			#@<< put all @first lines in root >>
			#@+node:1::<< put all @first lines in root >>
			#@+body
			#@+at
			#  Write any @first lines.  These lines are also converted to 
			# @verbatim lines, so the read logic simply ignores lines 
			# preceding the @+leo sentinel.

			#@-at
			#@@c

			s = root.t.bodyString
			tag = "@first"
			i = 0
			while match(s,i,tag):
				i += len(tag)
				i = skip_ws(s,i)
				j = i
				i = skip_to_end_of_line(s,i)
				# 21-SEP-2002 DTHEIN: write @first line, whether empty or not
				line = s[j:i]
				self.os(line) ; self.onl()
				i = skip_nl(s,i)
			#@-body
			#@-node:1::<< put all @first lines in root >>

			self.putOpenLeoSentinel("@+leo")
			
			#@<< put optional @comment sentinel lines >>
			#@+node:2::<< put optional @comment sentinel lines >>
			#@+body
			s2 = app().config.output_initial_comment
			if s2:
				lines = string.split(s2,"\\n")
				for line in lines:
					line = line.replace("@date",time.asctime())
					if len(line)> 0:
						self.putSentinel("@comment " + line)
			#@-body
			#@-node:2::<< put optional @comment sentinel lines >>

			
			self.putOpenNodeSentinel(root)
			self.putBodyPart(root)
			self.putCloseNodeSentinel(root)
			
			root.setVisited()
			self.putSentinel("@-leo")
			
			#@<< put all @last lines in root >>
			#@+node:3::<< put all @last lines in root >>
			#@+body
			#@+at
			#  Write any @last lines.  These lines are also converted to 
			# @verbatim lines, so the read logic simply ignores lines 
			# following the @-leo sentinel.

			#@-at
			#@@c

			tag = "@last"
			lines = string.split(root.t.bodyString,'\n')
			n = len(lines) ; j = k = n - 1
			# Don't write an empty last line.
			if j >= 0 and len(lines[j])==0:
				j = k = n - 2
			# Scan backwards for @last directives.
			while j >= 0:
				line = lines[j]
				if match(line,0,tag): j -= 1
				else: break
			# Write the @last lines.
			for line in lines[j+1:k+1]:
				i = len(tag) ; i = skip_ws(line,i)
				self.os(line[i:]) ; self.onl()
			#@-body
			#@-node:3::<< put all @last lines in root >>
			#@-body
			#@-node:3::<< write then entire @file tree >>

			self.closeWriteFile()
			
			#@<< warn about @ignored and orphans >>
			#@+node:4::<< Warn about @ignored and orphans  >>
			#@+body
			# 10/26/02: Always warn, even when language=="cweb"
			
			next = root.nodeAfterTree()
			v = root
			while v and v != next:
				if not v.isVisited():
					self.writeError("Orphan node:  " + v.headString())
				if v.isAtIgnoreNode():
					self.writeError("@ignore node: " + v.headString())
				v = v.threadNext()
			
			#@-body
			#@-node:4::<< Warn about @ignored and orphans  >>

			
			#@<< finish writing >>
			#@+node:5::<< finish writing >>
			#@+body
			#@+at
			#  We set the orphan and dirty flags if there are problems writing 
			# the file to force Commands::write_LEO_file to write the tree to 
			# the .leo file.

			#@-at
			#@@c

			if self.errors > 0 or self.root.isOrphan():
				root.setOrphan()
				root.setDirty() # 2/9/02: make _sure_ we try to rewrite this file.
				os.remove(self.outputFileName) # Delete the temp file.
				es("Not written: " + self.outputFileName)
			else:
				root.clearOrphan()
				root.clearDirty()
				self.replaceTargetFileIfDifferent()
			#@-body
			#@-node:5::<< finish writing >>

		except:
			self.handleWriteException()
	#@-body
	#@-node:8::atFile.write
	#@+node:9::atFile.writeAll
	#@+body
	#@+at
	#  This method scans all vnodes, calling write for every @file node 
	# found.  If partialFlag is true we write all @file nodes in the selected 
	# outline.  Otherwise we write @file nodes in the entire outline.

	#@-at
	#@@c
	def writeAll(self,v,partialFlag):
	
		self.initIvars()
		writtenFiles = [] # List of files that might be written again.
		# Kludge: look at whole tree if forceFlag is false;
		if partialFlag: after = v.nodeAfterTree()
		else: after = None
		
		#@<< Clear all orphan bits >>
		#@+node:1::<< Clear all orphan bits >>
		#@+body
		#@+at
		#  We must clear these bits because they may have been set on a 
		# previous write.  Calls to atFile::write may set the orphan bits in 
		# @file nodes.  If so, write_LEO_file will write the entire @file tree.

		#@-at
		#@@c

		v2 = v
		while v2 and v2 != after:
			v2.clearOrphan()
			v2 = v2.threadNext()
		#@-body
		#@-node:1::<< Clear all orphan bits >>

		while v and v != after:
			# trace(`v`)
			if v.isAnyAtFileNode() or v.isAtIgnoreNode():
				
				#@<< handle v's tree >>
				#@+node:2::<< handle v's tree >>
				#@+body
				# This code is a little tricky: @ignore not recognised in @silentfile nodes.
				if v.isDirty() or partialFlag or v.t in writtenFiles:
					if v.isAtSilentFileNode():
						self.silentWrite(v)
					elif v.isAtIgnoreNode():
						pass
					elif v.isAtRawFileNode():
						self.rawWrite(v)
					elif v.isAtNoSentinelsFileNode():
						self.write(v,nosentinels=true)
					elif v.isAtFileNode():
						self.write(v)
				
					if not v.isAtIgnoreNode():
						writtenFiles.append(v.t)
				
				elif v.isAtFileNode():
					self.checkForLeoCustomize(v)
					
				
				
				
				#@-body
				#@-node:2::<< handle v's tree >>

				v = v.nodeAfterTree()
			else:
				v = v.threadNext()
		if partialFlag: # This is the Write @file Nodes command.
			if len(writtenFiles) > 0:
				es("finished")
			else:
				es("no @file or similar nodes in the selected tree")
	
	#@-body
	#@-node:9::atFile.writeAll
	#@+node:10::atFile.writeMissing
	#@+body
	def writeMissing(self,v):
	
		self.initIvars()
		writtenFiles = false
		after = v.nodeAfterTree()
		while v and v != after:
			if v.isAtSilentFileNode() or (
				v.isAnyAtFileNode() and not v.isAtIgnoreNode()):
				missing = false ; valid = true
				self.targetFileName = v.anyAtFileNodeName()
				
				#@<< set missing if the file does not exist >>
				#@+node:1::<< set missing if the file does not exist >>
				#@+body
				# This is similar, but not the same as, the logic in openWriteFile.
				
				valid = self.targetFileName and len(self.targetFileName) > 0
				
				if valid:
					try:
						# Creates missing directives if option is enabled.
						self.scanAllDirectives(v)
						valid = self.errors == 0
					except:
						es("exception in atFile.scanAllDirectives")
						es_exception()
						valid = false
				
				if valid:
					try:
						fn = self.targetFileName
						self.shortFileName = fn # name to use in status messages.
						self.targetFileName = os.path.join(self.default_directory,fn)
						self.targetFileName = os.path.normpath(self.targetFileName)
						path = self.targetFileName # Look for the full name, not just the directory.
						valid = path and len(path) > 0
						if valid:
							missing = not os.path.exists(path)
					except:
						es("exception creating path:" + fn)
						es_exception()
						valid = false
				#@-body
				#@-node:1::<< set missing if the file does not exist >>

				if valid and missing:
					if not v.isAtFileNode() or self.checkForLeoCustomize(v):
						
						#@<< create self.outputFile >>
						#@+node:2::<< create self.outputFile >>
						#@+body
						try:
							self.outputFileName = self.targetFileName + ".tmp"
							self.outputFile = open(self.outputFileName,'wb')
							if self.outputFile == None:
								self.writeError("can not open " + self.outputFileName)
						except:
							es("exception opening:" + self.outputFileName)
							es_exception()
							self.outputFile = None
						
						#@-body
						#@-node:2::<< create self.outputFile >>

						if self.outputFile:
							
							#@<< write the @file node >>
							#@+node:3::<< write the @file node >>
							#@+body
							if v.isAtSilentFileNode():
								self.silentWrite(v)
							elif v.isAtRawFileNode():
								self.rawWrite(v)
							elif v.isAtNoSentinelsFileNode():
								self.write(v,nosentinels=true)
							elif v.isAtFileNode():
								self.write(v)
							else: assert(0)
							
							writtenFiles = true
							
							#@-body
							#@-node:3::<< write the @file node >>

				v = v.nodeAfterTree()
			elif v.isAtIgnoreNode():
				v = v.nodeAfterTree()
			else:
				v = v.threadNext()
		
		if writtenFiles > 0:
			es("finished")
		else:
			es("no missing @file node in the selected tree")
	#@-body
	#@-node:10::atFile.writeMissing
	#@+node:11::os, onl, etc. (leoAtFile)
	#@+body
	def oblank(self):
		self.os(' ')
	
	def oblanks(self,n):
		self.os(' ' * abs(n))
	
	def onl(self):
		self.os(self.output_newline)
	
	def os(self,s):
		if s is None or len(s) == 0: return
		if self.trace: trace(`s`)
		if self.suppress_newlines and self.newline_pending:
			self.newline_pending = false
			s = self.output_newline + s
		if self.outputFile:
			try:
				s = toEncodedString(s,self.encoding,reportErrors=true)
				self.outputFile.write(s)
			except:
				es("exception writing:" + `s`)
				es_exception()
	
	def otabs(self,n):
		self.os('\t' * abs(n))
	#@-body
	#@-node:11::os, onl, etc. (leoAtFile)
	#@+node:12::putBodyPart (removes trailing lines)
	#@+body
	#@+at
	#  We generate the body part only if it contains something besides 
	# whitespace. The check for at-ignore is made in atFile::write.

	#@-at
	#@@c
	def putBodyPart(self,v):
	
		# trace(`v`)
		s = v.t.bodyString
		i = skip_ws_and_nl(s, 0)
		if i >= len(s): return
		s = removeTrailingWs(s) # don't use string.rstrip!
		self.putSentinel("@+body")
		
		#@<< put code/doc parts and sentinels >>
		#@+node:1::<< put code/doc parts and sentinels >>
		#@+body
		i = 0 ; n = len(s)
		firstLastHack = 1
		
		if firstLastHack:
			
			#@<< initialize lookingForFirst/Last & initialLastDirective >>
			#@+node:1::<< initialize lookingForFirst/Last & initialLastDirective >>
			#@+body
			# 14-SEP-2002 DTHEIN: If this is the root node, then handle all @first directives here
			lookingForLast = 0
			lookingForFirst = 0
			initialLastDirective = -1
			lastDirectiveCount = 0
			if (v == self.root):
				lookingForLast = 1
				lookingForFirst = 1
			#@-body
			#@-node:1::<< initialize lookingForFirst/Last & initialLastDirective >>

		while i < n:
			kind = self.directiveKind(s,i)
			if firstLastHack:
				
				#@<< set lookingForFirst/Last & initialLastDirective >>
				#@+node:2::<< set lookingForFirst/Last & initialLastDirective >>
				#@+body
				# 14-SEP-2002 DTHEIN: If first directive isn't @first, then stop looking for @first
				if lookingForFirst:
					if kind != atFile.miscDirective:
						lookingForFirst = 0
					elif not match_word(s,i,"@first"):
						lookingForFirst = 0
				
				if lookingForLast:
					if initialLastDirective == -1:
						if (kind == atFile.miscDirective) and match_word(s,i,"@last"):
							# mark the point where the last directive was found
							initialLastDirective = i
					else:
						if (kind != atFile.miscDirective) or (not match_word(s,i,"@last")):
							# found something after @last, so process the @last directives
							# in 'ignore them' mode
							i, initialLastDirective = initialLastDirective, -1
							lastDirectiveCount = 0
							kind = self.directiveKind(s,i)
				#@-body
				#@-node:2::<< set lookingForFirst/Last & initialLastDirective >>

			j = i
			if kind == atFile.docDirective or kind == atFile.atDirective:
				i = self.putDoc(s,i,kind)
			elif ( # 10/16/02
				kind == atFile.miscDirective or
				kind == atFile.rawDirective or
				kind == atFile.endRawDirective ):
				if firstLastHack:
					
					#@<< handle misc directives >>
					#@+node:3::<< handle misc directives >>
					#@+body
					if lookingForFirst: # DTHEIN: can only be true if it is @first directive
						i = self.putEmptyDirective(s,i)
					elif (initialLastDirective != -1) and match_word(s,i,"@last"):
						# DTHEIN: can only be here if lookingForLast is true
						# skip the last directive ... we'll output it at the end if it
						# is truly 'last'
						lastDirectiveCount += 1
						i = skip_line(s,i)
					else:
						i = self.putDirective(s,i)
					#@-body
					#@-node:3::<< handle misc directives >>

				else:
					i = self.putDirective(s,i)
			elif kind == atFile.noDirective or kind == atFile.othersDirective:
				i = self.putCodePart(s,i,v)
			elif kind == atFile.cDirective or kind == atFile.codeDirective:
				i = self.putDirective(s,i)
				i = self.putCodePart(s,i,v)
			else: assert(false) # We must handle everything that directiveKind returns
			assert(n == len(s))
			assert(j < i) # We must make progress.
		
		if firstLastHack:
			
			#@<< put out the last directives, if any >>
			#@+node:4::<< put out the last directives, if any >>
			#@+body
			# 14-SEP-2002 DTHEIN
			if initialLastDirective != -1:
				d = initialLastDirective
				for k in range(lastDirectiveCount):
					d = self.putEmptyDirective(s,d)
			#@-body
			#@-node:4::<< put out the last directives, if any >>
		#@-body
		#@-node:1::<< put code/doc parts and sentinels >>

		self.putSentinel("@-body")
	#@-body
	#@-node:12::putBodyPart (removes trailing lines)
	#@+node:13::putCodePart & allies
	#@+body
	#@+at
	#  This method expands a code part, terminated by any at-directive except 
	# at-others.  It expands references and at-others and outputs @verbatim 
	# sentinels as needed.

	#@-at
	#@@c
	def putCodePart(self,s,i,v):
	
		c = self.commands
		atOthersSeen = false # true: at-others has been expanded.
		if self.trace: trace("%d %s" % (self.indent,get_line(s,i)))
		while i < len(s):
			
			#@<< handle the start of a line >>
			#@+node:1::<< handle the start of a line >>
			#@+body
			#@+at
			#  The at-others directive is the only directive that is 
			# recognized following leading whitespace, so it is just a little 
			# tricky to recognize it.

			#@-at
			#@@c

			leading_nl = (s[i] == body_newline) # 9/27/02: look ahead before outputting newline.
			if leading_nl:
				i = skip_nl(s,i)
				if self.trace: trace("leading nl")
				self.onl() # 10/15/02: simpler to do it here.
			
			#leading_ws1 = i # 1/27/03
			j,delta = skip_leading_ws_with_indent(s,i,self.tab_width)
			#leading_ws2 = j # 1/27/03
			kind1 = self.directiveKind(s,i)
			kind2 = self.directiveKind(s,j)
			if self.raw:
				if kind1 == atFile.endRawDirective:
					
					#@<< handle @end_raw >>
					#@+node:3::<< handle @end_raw >>
					#@+body
					self.raw = false
					self.putSentinel("@@end_raw")
					i = skip_line(s,i)
					#@-body
					#@-node:3::<< handle @end_raw >>

			else:
				if kind1 == atFile.othersDirective or kind2 == atFile.othersDirective:
					
					#@<< handle @others >>
					#@+node:1::<< handle @others >>
					#@+body
					# This skips all indent and delta whitespace, so putAtOthers must generate it all.
					
					if 0: # 9/27/02: eliminates the newline preceeding the @+others sentinel.
						# This does not seem to be a good idea.
						i = skip_line(s,i) 
					else:
						i = skip_to_end_of_line(s,i)
					
					if atOthersSeen:
						self.writeError("@others already expanded in: " + v.headString())
					else:
						atOthersSeen = true
						self.putAtOthers(v, delta)
						
						# 12/8/02: Skip the newline _after_ the @others.
						if not self.sentinels and is_nl(s,i):
							if self.trace: trace("skip nl after @others")
							i = skip_nl(s,i)
					
					#@-body
					#@-node:1::<< handle @others >>

				elif kind1 == atFile.rawDirective:
					
					#@<< handle @raw >>
					#@+node:2::<< handle @raw >>
					#@+body
					self.raw = true
					self.putSentinel("@@raw")
					i = skip_line(s,i)
					#@-body
					#@-node:2::<< handle @raw >>

				elif kind1 == atFile.noDirective:
					
					#@<< put @verbatim sentinel if necessary >>
					#@+node:4::<< put @verbatim sentinel if necessary >>
					#@+body
					if match (s,i,self.startSentinelComment + '@'):
						self.putSentinel("verbatim")
					#@-body
					#@-node:4::<< put @verbatim sentinel if necessary >>

				else:
					break # all other directives terminate the code part.
			#@-body
			#@-node:1::<< handle the start of a line >>

			
			#@<< put the line >>
			#@+node:2::<< put the line >>
			#@+body
			if not self.raw:
				# 12/8/02: Don't write trailing indentation if not writing sentinels.
				if not self.sentinels and i >= len(s):
					if self.trace: trace("skipping trailing indentation")
					pass
				else:
					if self.trace: trace("start line")
					self.putIndent(self.indent)
			
			newlineSeen = false
			# 12/8/02: we buffer characters here for two reasons:
			# 1) to make traces easier to read and 2) to increase speed.
			buf = i # Indicate the start of buffered characters.
			while i < len(s) and not newlineSeen:
				ch = s[i]
				if ch == body_newline:
					break
				elif ch == body_ignored_newline:
					i += 1
				elif ch == '<' and not self.raw:
					
					#@<< put possible section reference >>
					#@+node:1::<< put possible section reference >>
					#@+body
					isSection, j = self.isSectionName(s, i)
					
					if isSection:
						if 0: # 1/27/03:  This is complex and doesn't always work.
							if self.sentinels:
								# Output the buffered characters and clear the buffer.
								self.os(s[buf:i]) ; buf = i
							else:
								# Remove any leading whitespace before the section ref.
								old_i = i ; i -= 1
								while i >= 0 and s[i] in (' ','\t'):
									i -= 1
								self.os(s[buf:i]) ; buf = i = old_i
						else: # The old way...
							# Output the buffered characters and clear the buffer.
							self.os(s[buf:i]) ; buf = i
						# Output the expansion.
						name = s[i:j]
						j,newlineSeen = self.putRef(name,v,s,j,delta)
						assert(j > i) # isSectionName must have made progress
						i = j ; buf = i
					else:
						# This is _not_ an error.
						i += 1
					#@-body
					#@-node:1::<< put possible section reference >>

				else:
					i += 1
			# Output any buffered characters.
			self.os(s[buf:i])
			#@-body
			#@-node:2::<< put the line >>

	
		# Raw code parts can only end at the end of body text.
		self.raw = false
		return i
	#@-body
	#@+node:3::isSectionName
	#@+body
	# returns (flag, end). end is the index of the character after the section name.
	
	def isSectionName(self,s,i):
	
		if not match(s,i,"<<"):
			return false, -1
		i = find_on_line(s,i,">>")
		if i:
			return true, i + 2
		else:
			return false, -1
	#@-body
	#@-node:3::isSectionName
	#@+node:4::inAtOthers
	#@+body
	#@+at
	#  Returns true if v should be included in the expansion of the at-others 
	# directive in the body text of v's parent.
	# 
	# 7/30/02: v will not be included if it is a definition node or if its 
	# body text contains an @ignore directive. Previously, a "nested" @others 
	# directive would also inhibit the inclusion of v.

	#@-at
	#@@c
	def inAtOthers(self,v):
	
		# Return false if this has been expanded previously.
		if  v.isVisited(): return false
		# Return false if this is a definition node.
		h = v.headString()
		i = skip_ws(h,0)
		isSection, j = self.isSectionName(h,i)
		if isSection: return false
		# Return false if v's body contains an @ignore or at-others directive.
		if 1: # 7/29/02: New code.  Amazingly, this appears to work!
			return not v.isAtIgnoreNode()
		else: # old & reliable code
			return not v.isAtIgnoreNode() and not v.isAtOthersNode()
	#@-body
	#@-node:4::inAtOthers
	#@+node:5::putAtOthers
	#@+body
	#@+at
	#  The at-others directive is recognized only at the start of the line.  
	# This code must generate all leading whitespace for the opening sentinel.

	#@-at
	#@@c
	def putAtOthers(self,v,delta):
	
		self.indent += delta
		self.putSentinel("@+others")
	
		child = v.firstChild()
		while child:
			if self.inAtOthers( child ):
				self.putAtOthersChild( child )
			child = child.next()
	
		self.putSentinel("@-others")
		self.indent -= delta
	#@-body
	#@-node:5::putAtOthers
	#@+node:6::putAtOthersChild
	#@+body
	def putAtOthersChild(self,v):
		
		# trace("%d %s" % (self.indent,`v`))
	
		self.putOpenNodeSentinel(v)
		
		# Insert the expansion of v.
		v.setVisited() # Make sure it is never expanded again.
		self.putBodyPart(v)
	
		# Insert expansions of all children.
		child = v.firstChild()
		while child:
			if self.inAtOthers( child ):
				self.putAtOthersChild( child )
			child = child.next()
	
		self.putCloseNodeSentinel(v)
	#@-body
	#@-node:6::putAtOthersChild
	#@+node:7::putRef
	#@+body
	def putRef (self,name,v,s,i,delta):
	
		if self.trace: trace(get_line(s,i))
		newlineSeen = false
		ref = findReference(name, v)
		if not ref:
			self.writeError("undefined section: " + name +
				"\n\treferenced from: " + v.headString())
			return i,newlineSeen
	
		
		#@<< Generate the expansion of the reference >>
		#@+node:1::<< Generate the expansion of the reference >>
		#@+body
		# 2/24/02: adjust indent here so sentinel looks better.
		self.indent += delta 
		self.putSentinel("@" + name)
		self.putOpenSentinels(v,ref)
		self.putBodyPart(ref)
		ref.setVisited()
		self.putCloseSentinels(v,ref)
		self.indent -= delta
		
		#@-body
		#@-node:1::<< Generate the expansion of the reference >>

	
		# 2/25/02: Add a sentinel if required.
		j = skip_ws(s,i)
		if j < len(s) and match(s,j,self.startSentinelComment + '@'):
			self.putSentinel("@verbatimAfterRef")
			# 9/27/02: Put the line immediately, before the @-node sentinel.
			k = skip_to_end_of_line(s,i)
			self.os(s[i:k])
			i = k ; newlineSeen = false
		else:
			if 0: # 9/27/02: generate new directives.
				if is_nl(s,j):
					self.putSentinel("@newline")
					i = skip_nl(s,j) ; newlineSeen = true
				else:
					self.putSentinel("@nonewline")
					i = j ; newlineSeen = false
			if 0: # The old code did nothing
				if is_nl(s,j):
					i = j ; newlineSeen = false
				else:
					k = skip_to_end_of_line(s,i)
					self.os(s[i:k])
					i = k ; newlineSeen = false
	
		# The newlineSeen allows the caller to break out of the loop.
		return i,newlineSeen
	#@-body
	#@-node:7::putRef
	#@-node:13::putCodePart & allies
	#@+node:14::putDirective  (handles @delims)
	#@+body
	# This method outputs s, a directive or reference, in a sentinel.
	
	def putDirective(self,s,i):
	
		tag = "@delims"
		assert(i < len(s) and s[i] == '@')
		k = i
		j = skip_to_end_of_line(s,i)
		directive = s[i:j]
	
		if match_word(s,k,tag):
			
			#@<< handle @delims >>
			#@+node:1::<< handle @delims >>
			#@+body
			# Put a space to protect the last delim.
			self.putSentinel(directive + " ") # 10/23/02: put @delims, not @@delims
			
			# Skip the keyword and whitespace.
			j = i = skip_ws(s,k+len(tag))
			
			# Get the first delim.
			while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
				i += 1
			if j < i:
				self.startSentinelComment = s[j:i]
				# Get the optional second delim.
				j = i = skip_ws(s,i)
				while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
					i += 1
				self.endSentinelComment = choose(j<i, s[j:i], "")
			else:
				self.writeError("Bad @delims directive")
			#@-body
			#@-node:1::<< handle @delims >>

		else:
			self.putSentinel("@" + directive)
	
		i = skip_line(s,k)
		return i
	#@-body
	#@-node:14::putDirective  (handles @delims)
	#@+node:15::putDoc
	#@+body
	#@+at
	#  This method outputs a doc section terminated by @code or end-of-text.  
	# All other interior directives become part of the doc part.

	#@-at
	#@@c
	def putDoc(self,s,i,kind):
	
		if self.trace: trace("%d %s" % (self.indent,get_line(s,i)))
	
		if kind == atFile.atDirective:
			i += 1 ; tag = "at"
		elif kind == atFile.docDirective:
			i += 4 ; tag = "doc"
		else: assert(false)
		# Set j to the end of the doc part.
		n = len(s) ; j = i
		while j < n:
			j = skip_line(s, j)
			kind = self.directiveKind(s, j)
			if kind == atFile.codeDirective or kind == atFile.cDirective:
				break
		self.putSentinel("@+" + tag)
		self.putDocPart(s[i:j])
		self.putSentinel("@-" + tag)
		return j
	#@-body
	#@-node:15::putDoc
	#@+node:16::putDocPart
	#@+body
	# Puts a comment part in comments.
	# Note: this routine is _never_ called in cweb mode,
	# so noweb section references are _valid_ in cweb doc parts!
	
	def putDocPart(self,s):
	
		# j = skip_line(s,0) ; trace(`s[:j]`)
		c = self.commands
		single = len(self.endSentinelComment) == 0
		if not single:
			self.putIndent(self.indent)
			self.os(self.startSentinelComment) ; self.onl()
		# Put all lines.
		i = 0 ; n = len(s)
		while i < n:
			self.putIndent(self.indent)
			leading = self.indent
			if single:
				self.os(self.startSentinelComment) ; self.oblank()
				leading += len(self.startSentinelComment) + 1
			
			#@<< copy words, splitting the line if needed >>
			#@+node:1::<< copy words, splitting the line if needed >>
			#@+body
			#@+at
			#  We remove trailing whitespace from lines that have _not_ been 
			# split so that a newline has been inserted by this routine if and 
			# only if it is preceded by whitespace.

			#@-at
			#@@c

			line = i # Start of the current line.
			while i < n:
				word = i # Start of the current word.
				# Skip the next word and trailing whitespace.
				i = skip_ws(s, i)
				while i < n and not is_nl(s,i) and not is_ws(s[i]):
					i += 1
				i = skip_ws(s,i)
				# Output the line if no more is left.
				if i < n and is_nl(s,i):
					break
				# Split the line before the current word if needed.
				lineLen = i - line
				if line == word or leading + lineLen < self.page_width:
					word = i # Advance to the next word.
				else:
					# Write the line before the current word and insert a newline.
					theLine = s[line:word]
					self.os(theLine)
					self.onl() # This line must contain trailing whitespace.
					line = i = word  # Put word on the next line.
					break
			# Remove trailing whitespace and output the remainder of the line.
			theLine = string.rstrip(s[line:i]) # from right.
			self.os(theLine)
			if i < n and is_nl(s,i):
				i = skip_nl(s,i)
				self.onl() # No inserted newline and no trailing whitespace.
			#@-body
			#@-node:1::<< copy words, splitting the line if needed >>

		if not single:
			# This comment is like a sentinel.
			self.onl() ; self.putIndent(self.indent)
			self.os(self.endSentinelComment)
			self.onl() # Note: no trailing whitespace.
	#@-body
	#@-node:16::putDocPart
	#@+node:17::putEmptyDirective (Dave Hein)
	#@+body
	# 14-SEP-2002 DTHEIN
	# added for use by putBodyPart()
	
	# This method outputs the directive without the parameter text
	def putEmptyDirective(self,s,i):
	
		assert(i < len(s) and s[i] == '@')
		
		endOfLine = s.find('\n',i)
		# 21-SEP-2002 DTHEIN: if no '\n' then just use line length
		if endOfLine == -1:
			endOfLine = len(s)
		token = s[i:endOfLine].split()
		directive = token[0]
		self.putSentinel("@" + directive)
	
		i = skip_line(s,i)
		return i
	#@-body
	#@-node:17::putEmptyDirective (Dave Hein)
	#@+node:18::putIndent
	#@+body
	# Puts tabs and spaces corresponding to n spaces, assuming that we are at the start of a line.
	
	def putIndent(self,n):
	
		if self.trace: trace(`n`)
		c = self.commands
		w = self.tab_width
		if w > 1:
			q,r = divmod(n,w) 
			self.otabs(q) 
			self.oblanks(r)
		else:
			self.oblanks(n)
	#@-body
	#@-node:18::putIndent
	#@-node:6::Writing
	#@+node:7::Testing
	#@+node:1::scanAll
	#@+body
	def scanAll (self):
	
		c = self.commands ; v = c.rootVnode()
		while v:
			if v.isAtIgnoreNode():
				v = v.nodeAfterTree()
			elif v.isAtFileNode():
				self.scanFile(v)
				v = v.nodeAfterTree()
			else: v = v.threadNext()
	#@-body
	#@-node:1::scanAll
	#@+node:2::scanFile
	#@+body
	def scanFile(self,root):
	
		es("scanning: " + root.headString())
		self.targetFileName = root.atFileNodeName()
		self.root = root
		self.errors = self.structureErrors = 0
		
		#@<< open file >>
		#@+node:1::<< open file >>
		#@+body
		if len(self.targetFileName) == 0:
			self.readError("Missing file name")
		else:
			try:
				file = open(self.targetFileName,'r')
			except:
				self.readError("Error reading file")
		
		#@-body
		#@-node:1::<< open file >>

		if self.errors > 0: return 0
		
		#@<< Scan the file buffer >>
		#@+node:2::<< Scan the file buffer  >>
		#@+body
		self.indent = 0
		out = []
		self.scanHeader(file)
		self.scanText(file,root,out,atFile.endLeo,implicitChildIndex)
		s = string.join(out, "")
		root.setBodyStringOrPane(s)
		#@-body
		#@-node:2::<< Scan the file buffer  >>

		if self.structureErrors > 0:
			self.readError(`self.structureErrors` + " errors scanning file")
		return self.errors == 0
	
	#@-body
	#@-node:2::scanFile
	#@-node:7::Testing
	#@-others



#@@last
#@@last
#@-body
#@-node:0::@file leoAtFile.py 
#@-leo
#last1
#last2
