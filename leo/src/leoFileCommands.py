#@+leo-ver=4
#@+node:@file leoFileCommands.py
#@@language python

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoNodes
import os,string,time

#@+at 
#@nonl
# The list of language names that are written differently from the names in 
# language_delims_dict in leoGlobals.py.  This is needed for compatibility 
# with the borland version of Leo.
# 
# We convert from names in xml_language_names to names in language_delims_dict 
# by converting the name to lowercase and by removing slashes.
#@-at
#@@c

xml_language_names = (
	"CWEB","C","HTML","Java","LaTeX",
	"Pascal","PerlPod","Perl","Plain","Python","tcl/tk")

class BadLeoFile(Exception):
	def __init__(self, message):
		self.message = message
		Exception.__init__(self,message) # 4/26/03: initialize the base class.
	def __str__(self):
		return "Bad Leo File:" + self.message

class baseFileCommands:
	"""A base class for the fileCommands subcommander."""
	#@	@+others
	#@+node:leoFileCommands._init_
	def __init__(self,c):
	
		# g.trace("__init__", "fileCommands.__init__")
		self.c = c
		self.frame = c.frame
		self.initIvars()
	
	def initIvars(self):
	
		# General
		self.maxTnodeIndex = 0
		self.numberOfTnodes = 0
		self.topPosition = None
		self.mFileName = ""
		self.fileDate = -1
		self.leo_file_encoding = g.app.config.new_leo_file_encoding
		# For reading
		self.fileFormatNumber = 0
		self.ratio = 0.5
		self.fileBuffer = None ; self.fileIndex = 0
		self.currentVnodeStack = [] # A stack of vnodes giving the current position.
		self.topVnodeStack     = [] # A stack of vnodes giving the top position.
		# For writing
		self.read_only = false
		self.outputFile = None # File for normal writing
		self.outputList = None # List of strings for pasting
		self.openDirectory = None
		self.topVnode = None
		self.usingClipboard = false
		self.currentPosition = None
		# New in 3.12
		self.copiedTree = None
		self.tnodesDict = {}  # keys are gnx strings as returned by canonicalTnodeIndex.
	#@nonl
	#@-node:leoFileCommands._init_
	#@+node:canonicalTnodeIndex
	def canonicalTnodeIndex(self,index):
		
		"""Convert Tnnn to nnn, leaving gnx's unchanged."""
	
		# index might be Tnnn, nnn, or gnx.
		id,time,n = g.app.nodeIndices.scanGnx(index,0)
		if time == None: # A pre-4.1 file index.
			if index[0] == "T":
				index = index[1:]
	
		return index
	#@nonl
	#@-node:canonicalTnodeIndex
	#@+node:convertStackToPosition
	def convertStackToPosition (self,stack):
	
		c = self.c ; p2 = None
		if not stack: return None
	
		for p in c.allNodes_iter():
			if p.v == stack[0]:
				p2 = p.copy()
				for n in xrange(len(stack)):
					if not p2: break
					# g.trace("compare",n,p2.v,stack[n])
					if p2.v != stack[n]:
						p2 = None
					elif n + 1 == len(stack):
						break
					else:
						p2.moveToParent()
				if p2: return p
	
		return None
	#@nonl
	#@-node:convertStackToPosition
	#@+node:createVnode (changed for 4.2)
	def createVnode (self,parent,back,tref,headline,attrDict):
		
		# g.trace(parent,headline)
		v = None ; c = self.c
		# Shared tnodes are placed in the file even if empty.
		if tref == -1:
			t = leoNodes.tnode()
		else:
			tref = self.canonicalTnodeIndex(tref)
			t = self.tnodesDict.get(tref)
			if not t: t = self.newTnode(tref)
		if back: # create v after back.
			v = back.insertAfter(t)
		elif parent: # create v as the parent's first child.
			v = parent.insertAsNthChild(0,t)
		else: # create a root vnode
			v = leoNodes.vnode(c,t)
			v.moveToRoot()
	
		if v not in v.t.vnodeList:
			v.t.vnodeList.append(v) # New in 4.2.
	
		skip = len(v.t.vnodeList) > 1
	
		v.initHeadString(headline,encoding=self.leo_file_encoding)
		#@	<< handle unknown vnode attributes >>
		#@+node:<< handle unknown vnode attributes >>
		keys = attrDict.keys()
		if keys:
			p.v.unknownAttributes = attrDict
		
			if 0: # For debugging.
				s = "unknown attributes for " + p.headString()
				print s ; g.es(s,color="blue")
				for key in keys:
					s = "%s = %s" % (key,attrDict.get(key))
					print s ; g.es(s)
		#@nonl
		#@-node:<< handle unknown vnode attributes >>
		#@nl
		return v,skip
	#@nonl
	#@-node:createVnode (changed for 4.2)
	#@+node:getExistingVnode
	def getExistingVnode (self,tref):
	
		assert(tref > -1)
		tref = self.canonicalTnodeIndex(tref)
		t = self.tnodesDict.get(tref)
		return t.vnodeList[0]
	#@nonl
	#@-node:getExistingVnode
	#@+node:finishPaste
	# This method finishes pasting the outline from the clipboard.
	def finishPaste(self):
	
		c = self.c
		current = c.currentPosition()
		c.beginUpdate()
		#@	<< reassign tnode indices and clear all clone links >>
		#@+node:<< reassign tnode indices and clear all clone links >>
		#@+at 
		#@nonl
		# putLeoOutline calls assignFileIndices (when copying nodes) so that 
		# vnode can be associated with tnodes.
		# However, we must _reassign_ the indices here so that no "false 
		# clones" are created.
		#@-at
		#@@c
		
		current.clearVisitedInTree()
		
		for p in current.self_and_subtree_iter():
			t = p.v.t
			if not t.isVisited():
				t.setVisited()
				self.maxTnodeIndex += 1
				t.setFileIndex(self.maxTnodeIndex)
		#@nonl
		#@-node:<< reassign tnode indices and clear all clone links >>
		#@nl
		c.selectVnode(current)
		c.endUpdate()
		return current
	#@nonl
	#@-node:finishPaste
	#@+node:get routines
	def getBool (self):
		self.skipWs() # guarantees at least one more character.
		ch = self.fileBuffer[self.fileIndex]
		if ch == '0':
			self.fileIndex += 1 ; return false
		elif ch == '1':
			self.fileIndex += 1 ; return true
		else:
			raise BadLeoFile("expecting bool constant")
			
	def getDqBool (self):
		self.getDquote() ; val = self.getBool() ; self.getDquote()
		return val
		
	def getDqString (self): # 7/10/02
		self.getDquote()
		i = self.fileIndex
		self.fileIndex = j = string.find(self.fileBuffer,'"',i)
		if j == -1: raise BadLeoFile("unterminated double quoted string")
		s = self.fileBuffer[i:j]
		self.getDquote()
		return s
	
	def getDouble (self):
		self.skipWs()
		i = self.fileIndex ; buf = self.fileBuffer
		floatChars = string.digits + 'e' + 'E' + '.' + '+' + '-'
		n = len(buf)
		while i < n and buf[i] in floatChars:
			i += 1
		if i == self.fileIndex:
			raise BadLeoFile("expecting float constant")
		val = float(buf[self.fileIndex:i])
		self.fileIndex = i
		return val
	
	def getDquote (self):
		self.getTag('"')
		
	def getIndex (self):
		val = self.getLong()
		if val < 0: raise BadLeoFile("expecting index")
		return val
		
	def getLong (self):
		self.skipWs() # guarantees at least one more character.
		i = self.fileIndex
		if self.fileBuffer[i] == '-':
			i += 1
		n = len(self.fileBuffer)
		while i < n and self.fileBuffer[i] in string.digits:
			i += 1
		if i == self.fileIndex:
			raise BadLeoFile("expecting int constant")
		val = int(self.fileBuffer[self.fileIndex:i])
		self.fileIndex = i
		return val
			
	def getStringToTag (self,tag):
		buf = self.fileBuffer
		blen = len(buf) ; tlen = len(tag)
		i = j = self.fileIndex
		while i < blen:
			if tag == buf[i:i+tlen]:
				self.fileIndex = i
				return buf[j:i]
			else: i += 1
		raise BadLeoFile("expecting string terminated by " + tag)
		return ""
		
	# Look ahead for collapsed tag: tag may or may not end in ">"
	# Skips tag and /> if found, otherwise does not alter index.
	def getOpenTag (self,tag):
		if tag[-1] == ">":
			# Only the tag itself or a collapsed tag are valid.
			if self.matchTag(tag):
				return false # Not a collapsed tag.
			elif self.matchTag(tag[:-1]):
				# It must be a collapsed tag.
				self.skipWs()
				if self.matchTag("/>"):
					return true
			print "getOpenTag(", tag, ") failed:"
			raise BadLeoFile("expecting" + tag)
		else:
			# The tag need not be followed by "/>"
			if self.matchTag(tag):
				old_index = self.fileIndex
				self.skipWs()
				if self.matchTag("/>"):
					return true
				else:
					self.fileIndex = old_index
					return false
			else:
				print "getOpenTag(", tag, ") failed:"
				raise BadLeoFile("expecting" + tag)
		
	# 11/24/02: Look ahead for closing />
	# Return true if found.
	def getTag (self,tag):
		if self.matchTag(tag):
			return
		else:
			print "getTag(", tag, ") failed:"
			raise BadLeoFile("expecting" + tag)
			
	def getUnknownTag(self):
		
		self.skipWsAndNl() # guarantees at least one more character.
		tag = self.getStringToTag('=')
		if not tag:
			print "getUnknownTag failed"
			raise BadLeoFile("unknown tag not followed by '='")
		self.fileIndex += 1
		val = self.getDqString()
		g.trace(tag,val)
		return tag,val
		
	#@nonl
	#@-node:get routines
	#@+node:match routines
	def matchChar (self,ch):
		self.skipWs() # guarantees at least one more character.
		if ch == self.fileBuffer[self.fileIndex]:
			self.fileIndex += 1 ; return true
		else: return false
	
	# Warning: does not check for end-of-word,
	# so caller must match prefixes first.
	def matchTag (self,tag):
		self.skipWsAndNl() # guarantees at least one more character.
		i = self.fileIndex
		if tag == self.fileBuffer[i:i+len(tag)]:
			self.fileIndex += len(tag)
			return true
		else:
			return false
	
	def matchTagWordIgnoringCase (self,tag):
		self.skipWsAndNl() # guarantees at least one more character.
		i = self.fileIndex
		tag = string.lower(tag)
		j = g.skip_c_id(self.fileBuffer,i)
		word = self.fileBuffer[i:j]
		word = string.lower(word)
		if tag == word:
			self.fileIndex += len(tag)
			return true
		else:
			return false
	#@-node:match routines
	#@+node:getClipboardHeader
	def getClipboardHeader (self):
	
		if self.getOpenTag("<leo_header"):
			return # 11/24/02
	
		while 1:
			if self.matchTag("file_format="):
				self.getDquote() ; self.fileFormatNumber = self.getLong() ; self.getDquote()
			elif self.matchTag("tnodes="):
				self.getDquote() ; self.getLong() ; self.getDquote() # no longer used
			elif self.matchTag("max_tnode_index="):
				self.getDquote() ; self.getLong() ; self.getDquote() # no longer used
			else:
				self.getTag("/>")
				break
	#@nonl
	#@-node:getClipboardHeader
	#@+node:getCloneWindows
	# For compatibility with old file formats.
	
	def getCloneWindows (self):
	
		if not self.matchTag("<clone_windows>"):
			return
	
		while self.matchTag("<clone_window vtag=\"V"):
			self.getLong() ; self.getDquote() ; self.getTag(">")
			if not self.getOpenTag("<global_window_position"):
				self.getTag("<global_window_position")
				self.getPosition()
				self.getTag("/>")
			self.getTag("</clone_window>")
		self.getTag("</clone_windows>")
	#@nonl
	#@-node:getCloneWindows
	#@+node:getEscapedString
	def getEscapedString (self):
	
		# The next '<' begins the ending tag.
		i = self.fileIndex
		self.fileIndex = j = string.find(self.fileBuffer,'<',i)
		if j == -1:
			print self.fileBuffer[i:]
			raise BadLeoFile("unterminated escaped string")
		else:
			# Allocates memory
			return self.xmlUnescape(self.fileBuffer[i:j])
	#@nonl
	#@-node:getEscapedString
	#@+node:getFindPanelSettings
	def getFindPanelSettings (self):
	
		c = self.c ; config = g.app.config ; findFrame = g.app.findFrame
		#@	<< Set defaults of all flags >>
		#@+node:<< Set defaults of all flags >>
		if g.app.gui.guiName() == "tkinter":
		
			for var in findFrame.intKeys:
				attr = "%s_flag" % (var)
				setattr(c,attr,false)
				# g.trace(attr)
		#@-node:<< Set defaults of all flags >>
		#@nl
		if not self.getOpenTag("<find_panel_settings"):
			while 1:
				if   self.matchTag("batch="): c.batch_flag = self.getDqBool()
				elif self.matchTag("ignore_case="): c.ignore_case_flag = self.getDqBool()
				elif self.matchTag("mark_changes="): c.mark_changes_flag = self.getDqBool()
				elif self.matchTag("mark_finds="): c.mark_finds_flag = self.getDqBool()
				elif self.matchTag("node_only="): c.node_only_flag = self.getDqBool()
				elif self.matchTag("pattern_match="): c.pattern_match_flag = self.getDqBool()
				elif self.matchTag("reverse="): c.reverse_flag = self.getDqBool()
				elif self.matchTag("script_change="): c.script_change_flag = self.getDqBool() # 11/05/03
				elif self.matchTag("script_search="): c.script_search_flag = self.getDqBool() # 11/05/03
				elif self.matchTag("search_headline="): c.search_headline_flag = self.getDqBool()
				elif self.matchTag("search_body="): c.search_body_flag = self.getDqBool()
				elif self.matchTag("selection_only="): c.selection_only_flag = self.getDqBool() # 11/9/03
				elif self.matchTag("suboutline_only="): c.suboutline_only_flag = self.getDqBool()
				elif self.matchTag("whole_word="): c.whole_word_flag = self.getDqBool()
				elif self.matchTag("wrap="): c.wrap_flag = self.getDqBool()
				elif self.matchTag(">"): break
				else: self.getUnknownTag() # New in 4.1: ignore all other tags.
			#
			self.getTag("<find_string>")
			c.find_text = self.getEscapedString()
			self.getTag("</find_string>")
			#
			self.getTag("<change_string>")
			c.change_text = self.getEscapedString()
			self.getTag("</change_string>")
			#
			self.getTag("</find_panel_settings>")
		
		# Override .leo file's preferences if settings are in leoConfig.txt.
		config.setCommandsFindIvars(c)
		# Update the settings immediately.
		if g.app.gui.guiName() == "tkinter":
			g.app.findFrame.init(c)
	#@nonl
	#@-node:getFindPanelSettings
	#@+node:getGlobals
	def getGlobals (self):
	
		if self.getOpenTag("<globals"):
			return
	
		self.getTag("body_outline_ratio=\"")
		self.ratio = self.getDouble() ; self.getDquote() ; self.getTag(">")
	
		self.getTag("<global_window_position")
		y,x,h,w = self.getPosition() ; self.getTag("/>")
		self.frame.setTopGeometry(w,h,x,y)
	
		# 7/15/02: Redraw the window before writing into it.
		self.frame.deiconify()
		self.frame.lift()
		self.frame.update()
	
		self.getTag("<global_log_window_position")
		self.getPosition() ;
		self.getTag("/>") # no longer used.
	
		self.getTag("</globals>")
	#@nonl
	#@-node:getGlobals
	#@+node:getLeoFile
	# The caller should enclose this in begin/endUpdate.
	
	def getLeoFile (self,fileName,atFileNodesFlag=true):
	
		c = self.c
		c.setChanged(false) # 10/1/03: May be set when reading @file nodes.
		#@	<< warn on read-only files >>
		#@+node:<< warn on read-only files >>
		try:
			self.read_only = false
			self.read_only = not os.access(fileName,os.W_OK)
			if self.read_only:
				g.es("read only: " + fileName,color="red")
		except:
			if 0: # testing only: access may not exist on all platforms.
				g.es("exception getting file access")
				g.es_exception()
		#@nonl
		#@-node:<< warn on read-only files >>
		#@nl
		self.mFileName = c.mFileName
		self.tnodesDict = {}
		ok = true
		c.loading = true # disable c.changed
		
		try:
			#@		<< scan all the xml elements >>
			#@+node:<< scan all the xml elements >>
			self.getXmlVersionTag()
			self.getXmlStylesheetTag()
			self.getTag("<leo_file>")
			self.getLeoHeader()
			self.getGlobals()
			self.getPrefs()
			self.getFindPanelSettings()
			
			# Causes window to appear.
			c.frame.resizePanesToRatio(c.frame.ratio,c.frame.secondary_ratio) 
			g.es("reading: " + fileName)
			
			self.getVnodes()
			self.getTnodes()
			self.getCloneWindows()
			self.getTag("</leo_file>")
			#@nonl
			#@-node:<< scan all the xml elements >>
			#@nl
		except BadLeoFile, message:
			#@		<< raise an alert >>
			#@+node:<< raise an alert >>
			# All other exceptions are Leo bugs.
			
			g.es_exception()
			g.alert(self.mFileName + " is not a valid Leo file: " + str(message))
			#@nonl
			#@-node:<< raise an alert >>
			#@nl
			ok = false
	
		c.frame.tree.redraw_now(scroll=false)
		
		if ok and atFileNodesFlag:
			c.atFileCommands.readAll(c.rootVnode(),partialFlag=false)
	
		if not c.currentPosition():
			c.setCurrentPosition(c.rootPosition())
	
		c.selectVnode(c.currentPosition()) # load body pane
		c.loading = false # reenable c.changed
		c.setChanged(c.changed) # Refresh the changed marker.
		self.tnodesDict = {}
		return ok, self.ratio
	#@nonl
	#@-node:getLeoFile
	#@+node:getLeoHeader
	def getLeoHeader (self):
	
		# Set defaults.
		self.maxTnodeIndex = 0
		self.numberOfTnodes = 0
		if self.getOpenTag("<leo_header"):
			return
	
		# New in version 1.7: attributes may appear in any order.
		while 1:
			if self.matchTag("file_format="):
				self.getDquote() ; self.fileFormatNumber = self.getLong() ; self.getDquote()
			elif self.matchTag("tnodes="):
				self.getDquote() ; self.numberOfTnodes = self.getLong() ; self.getDquote()
			elif self.matchTag("max_tnode_index="):
				self.getDquote() ; self.maxTnodeIndex = self.getLong() ; self.getDquote()
				# g.trace("max_tnode_index:",self.maxTnodeIndex)
			elif self.matchTag("clone_windows="):
				self.getDquote() ; self.getLong() ; self.getDquote() # no longer used.
			else:
				self.getTag("/>")
				break
	#@nonl
	#@-node:getLeoHeader
	#@+node:getLeoOutline (from clipboard)
	# This method reads a Leo outline from string s in clipboard format.
	def getLeoOutline (self,s):
	
		self.usingClipboard = true
		self.fileBuffer = s ; self.fileIndex = 0
		self.tnodesDict = {}
	
		try:
			self.getXmlVersionTag() # leo.py 3.0
			self.getXmlStylesheetTag() # 10/25/02
			self.getTag("<leo_file>")
			self.getClipboardHeader()
			self.getVnodes()
			self.getTnodes()
			self.getTag("</leo_file>")
			v = self.finishPaste()
		except BadLeoFile:
			v = None
	
		# Clean up.
		self.fileBuffer = None ; self.fileIndex = 0
		self.usingClipboard = false
		self.tnodesDict = {}
		return v
	#@nonl
	#@-node:getLeoOutline (from clipboard)
	#@+node:getPosition
	def getPosition (self):
	
		top = left = height = width = 0
		# New in version 1.7: attributes may appear in any order.
		while 1:
			if self.matchTag("top=\""):
				top = self.getLong() ; self.getDquote()
			elif self.matchTag("left=\""):
				left = self.getLong() ; self.getDquote()
			elif self.matchTag("height=\""):
				height = self.getLong() ; self.getDquote()
			elif self.matchTag("width=\""):
				width = self.getLong() ; self.getDquote()
			else: break
		return top, left, height, width
	#@nonl
	#@-node:getPosition
	#@+node:getPrefs
	def getPrefs (self):
	
		c = self.c ; config = g.app.config
		
		if self.getOpenTag("<preferences"):
			return
	
		table = (
			("allow_rich_text",None,None), # Ignored.
			("tab_width","tab_width",self.getLong),
			("page_width","page_width",self.getLong),
			("tangle_bat","tangle_batch_flag",self.getBool),
			("untangle_bat","untangle_batch_flag",self.getBool),
			("output_doc_chunks","output_doc_flag",self.getBool),
			("noweb_flag",None,None), # Ignored.
			("extended_noweb_flag",None,None), # Ignored.
			("defaultTargetLanguage","target_language",self.getTargetLanguage),
			("use_header_flag","use_header_flag",self.getBool))
		
		while 1:
			found = false
			for tag,var,f in table:
				if self.matchTag("%s=" % tag):
					if var:
						self.getDquote() ; val = f() ; self.getDquote()
						setattr(c,var,val)
					else:
						self.getDqString()
					found = true ; break
			if not found:
				if self.matchTag(">"):
					break
				else: # New in 4.1: ignore all other tags.
					self.getUnknownTag()
	
		while 1:
			if self.matchTag("<defaultDirectory>"):
				# New in version 0.16.
				c.tangle_directory = self.getEscapedString()
				self.getTag("</defaultDirectory>")
				if not g.os_path_exists(c.tangle_directory):
					g.es("default tangle directory not found:" + c.tangle_directory)
			elif self.matchTag("<TSyntaxMemo_options>"):
				self.getEscapedString() # ignored
				self.getTag("</TSyntaxMemo_options>")
			else: break
		self.getTag("</preferences>")
		
		# Override .leo file's preferences if settings are in leoConfig.txt.
		if config.configsExist:
			config.setCommandsIvars(c)
	#@nonl
	#@-node:getPrefs
	#@+node:getTargetLanguage
	def getTargetLanguage (self):
		
		# Must match longer tags before short prefixes.
		for name in g.app.language_delims_dict.keys():
			if self.matchTagWordIgnoringCase(name):
				language = name.replace("/","")
				# self.getDquote()
				return language
				
		return "c" # default
	#@nonl
	#@-node:getTargetLanguage
	#@+node:getSize
	def getSize (self):
	
		# New in version 1.7: attributes may appear in any order.
		height = 0 ; width = 0
		while 1:
			if self.matchTag("height=\""):
				height = self.getLong() ; self.getDquote()
			elif self.matchTag("width=\""):
				width = self.getLong() ; self.getDquote()
			else: break
		return height, width
	#@nonl
	#@-node:getSize
	#@+node:getTnode
	def getTnode (self):
	
		# we have already matched <t.
		index = -1 ; attrDict = {}
		# New in version 1.7: attributes may appear in any order.
		while 1:	
			if self.matchTag("tx="):
				# New for 4.1.  Read either "Tnnn" or "gnx".
				index = self.getDqString()
			elif self.matchTag("rtf=\"1\""): pass # ignored
			elif self.matchTag("rtf=\"0\""): pass # ignored
			elif self.matchTag(">"):         break
			else: # New for 4.0: allow unknown attributes.
				attr,val = self.getUnknownTag()
				attrDict[attr] = val
				
		if g.app.use_gnx:
			# index might be Tnnn, nnn, or gnx.
			id,time,n = g.app.nodeIndices.scanGnx(index,0)
			if time == None: # A pre-4.1 file index.
				if index[0] == "T":
					index = index[1:]
	
		index = self.canonicalTnodeIndex(index)
		t = self.tnodesDict.get(index)
		# g.trace(t)
		#@	<< handle unknown attributes >>
		#@+node:<< handle unknown attributes >>
		keys = attrDict.keys()
		if keys:
			t.unknownAttributes = attrDict
			if 0: # For debugging.
				s = "unknown attributes for tnode"
				print s ; g.es(s, color = "blue")
				for key in keys:
					s = "%s = %s" % (key,attrDict.get(key))
					print s ; g.es(s)
		#@nonl
		#@-node:<< handle unknown attributes >>
		#@nl
		if t:
			if self.usingClipboard:
				#@			<< handle read from clipboard >>
				#@+node:<< handle read from clipboard >>
				if t:
					s = self.getEscapedString()
					t.setTnodeText(s,encoding=self.leo_file_encoding)
					# g.trace(index,len(s))
				#@nonl
				#@-node:<< handle read from clipboard >>
				#@nl
			else:
				#@			<< handle read from file >>
				#@+node:<< handle read from file >>
				s = self.getEscapedString()
				t.setTnodeText(s,encoding=self.leo_file_encoding)
				#@nonl
				#@-node:<< handle read from file >>
				#@nl
		else:
			g.es("no tnode with index: %s.  The text will be discarded" % str(index))
		self.getTag("</t>")
	#@-node:getTnode
	#@+node:getTnodes
	def getTnodes (self):
	
		# A slight change: we require a tnode element.  But Leo always writes this.
		if self.getOpenTag("<tnodes>"):
			return
			
		while self.matchTag("<t"):
			self.getTnode()
	
		self.getTag("</tnodes>")
	#@-node:getTnodes
	#@+node:getVnode changed for 4.2)
	def getVnode (self,parent,back,skip,appendToCurrentStack,appendToTopStack):
	
		c = self.c ; v = None
		setCurrent = setExpanded = setMarked = setOrphan = setTop = false
		tref = -1 ; headline = "" ; tnodeList = None ; attrDict = {} 
		# we have already matched <v.
		while 1:
			if self.matchTag("a=\""):
				#@			<< Handle vnode attribute bits >>
				#@+node:<< Handle vnode attribute bits  >>
				# The a=" has already been seen.
				while 1:
					if   self.matchChar('C'): pass # Not used: clone bits are recomputed later.
					elif self.matchChar('D'): pass # Not used.
					elif self.matchChar('E'): setExpanded = true
					elif self.matchChar('M'): setMarked = true
					elif self.matchChar('O'): setOrphan = true
					elif self.matchChar('T'): setTop = true
					elif self.matchChar('V'): setCurrent = true
					else: break
				
				self.getDquote()
				#@nonl
				#@-node:<< Handle vnode attribute bits  >>
				#@nl
			elif self.matchTag("t="):
				# New for 4.1.  Read either "Tnnn" or "gnx".
				tref = self.getDqString()
			elif self.matchTag("vtag=\"V"):
				self.getIndex() ; self.getDquote() # ignored
			elif self.matchTag("tnodeList="):
				s = self.getDqString()
				tnodeList = self.getTnodeList(s) # New for 4.0
			elif self.matchTag(">"):
				break
			else: # New for 4.0: allow unknown attributes.
				attr,val = self.getUnknownTag()
				attrDict[attr] = val
		# Headlines are optional.
		if self.matchTag("<vh>"):
			headline = self.getEscapedString() ; self.getTag("</vh>")
		
		# g.trace("skip:",skip,"parent:",parent,"back:",back,"headline:",headline)
		if skip:
			v = self.getExistingVnode(tref)
		else:
			v,skip = self.createVnode(parent,back,tref,headline,attrDict)
			if tnodeList:
				v.t.tnodeList = tnodeList # New for 4.0, 4.2: now in tnode.
				# g.trace("%4d" % len(tnodeList),v)
	
		#@	<< Set the remembered status bits >>
		#@+node:<< Set the remembered status bits >>
		if setCurrent:
			self.currentVnodeStack = [v]
		
		if setTop:
			self.topVnodeStack = [v]
			
		if setExpanded:
			v.initExpandedBit()
			
		if setMarked:
			v.initMarkedBit() # 3/25/03: Do not call setMarkedBit here!
		
		if setOrphan:
			v.setOrphan()
		#@nonl
		#@-node:<< Set the remembered status bits >>
		#@nl
	
		# Recursively create all nested nodes.
		parent = v ; back = None
		while self.matchTag("<v"):
			append1 = appendToCurrentStack and len(self.currentVnodeStack) == 0
			append2 = appendToTopStack and len(self.topVnodeStack) == 0
			back = self.getVnode(parent,back,skip,
				appendToCurrentStack=append1,appendToTopStack=append2)
				
		#@	<< Append to current or top stack >>
		#@+node:<< Append to current or top stack >>
		if not setCurrent and len(self.currentVnodeStack) > 0 and appendToCurrentStack:
			#g.trace("append current",v)
			self.currentVnodeStack.append(v)
			
		if not setTop and len(self.topVnodeStack) > 0 and appendToTopStack:
			#g.trace("append top",v)
			self.topVnodeStack.append(v)
		#@nonl
		#@-node:<< Append to current or top stack >>
		#@nl
	
		# End this vnode.
		self.getTag("</v>")
		return v
	#@nonl
	#@-node:getVnode changed for 4.2)
	#@+node:getTnodeList (4.0,4.2)
	def getTnodeList (self,s):
	
		"""Parse a list of tnode indices in string s."""
		
		# Remember: entries in the tnodeList correspond to @+node sentinels, _not_ to tnodes!
		
		fc = self ; 
	
		indexList = s.split(',') # The list never ends in a comma.
		tnodeList = []
		for index in indexList:
			index = self.canonicalTnodeIndex(index)
			t = fc.tnodesDict.get(index)
			if not t:
				# Not an error: create a new tnode and put it in fc.tnodesDict.
				# g.trace("not allocated: %s" % index)
				t = self.newTnode(index)
			tnodeList.append(t)
			
		# if tnodeList: g.trace(len(tnodeList))
		return tnodeList
	#@-node:getTnodeList (4.0,4.2)
	#@+node:getVnodes
	def getVnodes (self):
	
		c = self.c
	
		if self.getOpenTag("<vnodes>"):
			return
			
		if self.usingClipboard:
			oldRoot = c.rootPosition()
			oldCurrent = c.currentPosition()
	
		back = parent = None # This routine _must_ work on vnodes!
		
		self.currentVnodeStack = []
		self.topVnodeStack = []
		while self.matchTag("<v"):
			append1 = not self.usingClipboard and len(self.currentVnodeStack) == 0
			append2 = not self.usingClipboard and len(self.topVnodeStack) == 0
			back = self.getVnode(parent,back,skip=false,
				appendToCurrentStack=append1,appendToTopStack=append2)
	
		if self.usingClipboard:
			# Link in the pasted nodes after the current position.
			newRoot = c.rootPosition()
			c.setRootPosition(oldRoot)
			newRoot.v.linkAfter(oldCurrent.v)
			newCurrent = oldCurrent.copy()
			newCurrent.v = newRoot.v
			c.setCurrentPosition(newCurrent)
		else:
			#@		<< set current and top positions >>
			#@+node:<< set current and top positions >>
			current = self.convertStackToPosition(self.currentVnodeStack)
			if current:
				c.setCurrentPosition(current)
			else:
				g.trace(self.currentVnodeStack)
				c.setCurrentPosition(c.rootPosition())
				
			# At present this is useless: the drawing code doesn't set the top position properly.
			top = self.convertStackToPosition(self.topVnodeStack)
			if top:
				c.setTopPosition(top)
			#@nonl
			#@-node:<< set current and top positions >>
			#@nl
	
		self.getTag("</vnodes>")
	#@nonl
	#@-node:getVnodes
	#@+node:getXmlStylesheetTag
	def getXmlStylesheetTag (self):
	
		"""Parses the optional xml stylesheet string, and sets the corresponding config option.
		
		For example, given: <?xml_stylesheet s?> the config option is s."""
		
		c = self.c
		tag = "<?xml-stylesheet "
	
		if self.matchTag(tag):
			s = self.getStringToTag("?>")
			# print "reading:", tag + s + "?>"
			c.frame.stylesheet = s
			self.getTag("?>")
	#@nonl
	#@-node:getXmlStylesheetTag
	#@+node:getXmlVersionTag
	# Parses the encoding string, and sets self.leo_file_encoding.
	
	def getXmlVersionTag (self):
	
		self.getTag(g.app.prolog_prefix_string)
		encoding = self.getDqString()
		self.getTag(g.app.prolog_postfix_string)
	
		if g.isValidEncoding(encoding):
			self.leo_file_encoding = encoding
			g.es("File encoding: " + encoding, color="blue")
		else:
			g.es("invalid encoding in .leo file: " + encoding, color="red")
	#@-node:getXmlVersionTag
	#@+node:skipWs
	def skipWs (self):
	
		while self.fileIndex < len(self.fileBuffer):
			ch = self.fileBuffer[self.fileIndex]
			if ch == ' ' or ch == '\t':
				self.fileIndex += 1
			else: break
	
		# The caller is entitled to get the next character.
		if  self.fileIndex >= len(self.fileBuffer):
			raise BadLeoFile("")
	#@nonl
	#@-node:skipWs
	#@+node:skipWsAndNl
	def skipWsAndNl (self):
	
		while self.fileIndex < len(self.fileBuffer):
			ch = self.fileBuffer[self.fileIndex]
			if ch == ' ' or ch == '\t' or ch == '\r' or ch == '\n':
				self.fileIndex += 1
			else: break
	
		# The caller is entitled to get the next character.
		if  self.fileIndex >= len(self.fileBuffer):
			raise BadLeoFile("")
	#@nonl
	#@-node:skipWsAndNl
	#@+node:newTnode
	def newTnode(self,index):
	
		if self.tnodesDict.has_key(index):
			g.es("bad tnode index: %s. Using empty text." % str(index))
			return leoNodes.tnode()
		else:
			# Create the tnode.  Use the _original_ index as the key in tnodesDict.
			t = leoNodes.tnode()
			self.tnodesDict[index] = t
		
			if type(index) not in (type(""),type(u"")):
				g.es("newTnode: unexpected index type:",type(index),index,color="red")
			
			# Convert any pre-4.1 index to a gnx.
			id,time,n = gnx = g.app.nodeIndices.scanGnx(index,0)
			if time != None:
				t.setFileIndex(gnx)
	
			return t
	#@nonl
	#@-node:newTnode
	#@+node:readAtFileNodes
	def readAtFileNodes (self):
	
		c = self.c ; current = c.currentVnode()
		c.atFileCommands.readAll(current,partialFlag=true)
		c.redraw() # 4/4/03
		
		# 7/8/03: force an update of the body pane.
		current.setBodyStringOrPane(current.bodyString())
		c.frame.body.onBodyChanged(current,undoType=None)
	#@nonl
	#@-node:readAtFileNodes
	#@+node:fileCommands.readOutlineOnly
	def readOutlineOnly (self,file,fileName):
	
		c = self.c
		# Read the entire file into the buffer
		self.fileBuffer = file.read() ; file.close()
		self.fileIndex = 0
		#@	<< Set the default directory >>
		#@+node:<< Set the default directory >> in fileCommands.readOutlineOnly
		#@+at 
		#@nonl
		# The most natural default directory is the directory containing the 
		# .leo file that we are about to open.  If the user has specified the 
		# "Default Directory" preference that will over-ride what we are about 
		# to set.
		#@-at
		#@@c
		
		dir = g.os_path_dirname(fileName)
		
		if len(dir) > 0:
			c.openDirectory = dir
		#@nonl
		#@-node:<< Set the default directory >> in fileCommands.readOutlineOnly
		#@nl
		c.beginUpdate()
		ok, ratio = self.getLeoFile(fileName,atFileNodesFlag=false)
		c.endUpdate()
		c.frame.deiconify()
		vflag,junk,secondary_ratio = self.frame.initialRatios()
		c.frame.resizePanesToRatio(ratio,secondary_ratio)
		if 0: # 1/30/04: this is useless.
			# This should be done after the pane size has been set.
			if self.topPosition:
				c.frame.tree.setTopPosition(self.topPosition)
				c.redraw()
		# delete the file buffer
		self.fileBuffer = ""
		return ok
	#@nonl
	#@-node:fileCommands.readOutlineOnly
	#@+node:fileCommands.open
	def open(self,file,fileName):
	
		c = self.c ; frame = c.frame
		# Read the entire file into the buffer
		self.fileBuffer = file.read() ; file.close()
		self.fileIndex = 0
		#@	<< Set the default directory >>
		#@+node:<< Set the default directory >> in fileCommands.readOutlineOnly
		#@+at 
		#@nonl
		# The most natural default directory is the directory containing the 
		# .leo file that we are about to open.  If the user has specified the 
		# "Default Directory" preference that will over-ride what we are about 
		# to set.
		#@-at
		#@@c
		
		dir = g.os_path_dirname(fileName)
		
		if len(dir) > 0:
			c.openDirectory = dir
		#@nonl
		#@-node:<< Set the default directory >> in fileCommands.readOutlineOnly
		#@nl
		self.topPosition = None
		c.beginUpdate()
		ok, ratio = self.getLeoFile(fileName,atFileNodesFlag=true)
		frame.resizePanesToRatio(ratio,frame.secondary_ratio) # 12/2/03
		if 0: # 1/30/04: this is useless.
			if self.topPosition: 
				c.setTopVnode(self.topPosition)
		c.endUpdate()
		# delete the file buffer
		self.fileBuffer = ""
		return ok
	#@nonl
	#@-node:fileCommands.open
	#@+node:xmlUnescape
	def xmlUnescape(self,s):
	
		if s:
			s = string.replace(s, '\r', '')
			s = string.replace(s, "&lt;", '<')
			s = string.replace(s, "&gt;", '>')
			s = string.replace(s, "&amp;", '&')
		return s
	#@nonl
	#@-node:xmlUnescape
	#@+node:assignFileIndices & compactFileIndices
	def assignFileIndices (self):
		
		"""Assign a file index to all tnodes"""
		
		c = self.c ; nodeIndices = g.app.nodeIndices
	
		nodeIndices.setTimestamp() # This call is fairly expensive.
	
		if g.app.use_gnx:
			#@		<< assign missing gnx's, converting ints to gnx's >>
			#@+node:<< assign missing gnx's, converting ints to gnx's >>
			# Always assign an (immutable) index, even if the tnode is empty.
			
			for p in c.allNodes_iter():
				try: # Will fail for None or any pre 4.1 file index.
					id,time,n = p.v.t.fileIndex
				except TypeError:
					# Don't convert to string until the actual write.
					p.v.t.fileIndex = nodeIndices.getNewIndex()
			#@nonl
			#@-node:<< assign missing gnx's, converting ints to gnx's >>
			#@nl
		else:
			#@		<< reassign all tnode indices >>
			#@+node:<< reassign all tnode indices >>
			# Clear out all indices.
			for p in c.allNodes_iter():
				p.v.t.fileIndex = None
				
			# Recreate integer indices.
			self.maxTnodeIndex = 0
			
			for p in c.allNodes_iter():
				if p.v.t.fileIndex == None:
					self.maxTnodeIndex += 1
					p.v.t.fileIndex = self.maxTnodeIndex
			#@nonl
			#@-node:<< reassign all tnode indices >>
			#@nl
			
		if 0: # debugging:
			for p in c.allNodes_iter():
				g.trace(p.v.t.fileIndex)
	
	# Indices are now immutable, so there is no longer any difference between these two routines.
	compactFileIndices = assignFileIndices
	#@nonl
	#@-node:assignFileIndices & compactFileIndices
	#@+node:put (basic)(leoFileCommands)
	# All output eventually comes here.
	def put (self,s):
		if s and len(s) > 0:
			if self.outputFile:
				s = g.toEncodedString(s,self.leo_file_encoding,reportErrors=true)
				self.outputFile.write(s)
			elif self.outputList != None: # Write to a list.
				self.outputList.append(s) # 1/8/04: avoid using string concatenation here!
	
	def put_dquote (self):
		self.put('"')
			
	def put_dquoted_bool (self,b):
		if b: self.put('"1"')
		else: self.put('"0"')
			
	def put_flag (self,a,b):
		if a:
			self.put(" ") ; self.put(b) ; self.put('="1"')
			
	def put_in_dquotes (self,a):
		self.put('"')
		if a: self.put(a) # will always be true if we use backquotes.
		else: self.put('0')
		self.put('"')
	
	def put_nl (self):
		self.put("\n")
		
	def put_tab (self):
		self.put("\t")
		
	def put_tabs (self,n):
		while n > 0:
			self.put("\t")
			n -= 1
	#@-node:put (basic)(leoFileCommands)
	#@+node:putClipboardHeader
	def putClipboardHeader (self):
	
		c = self.c ; tnodes = 0
		#@	<< count the number of tnodes >>
		#@+node:<< count the number of tnodes >>
		c.clearAllVisited()
		
		for p in c.currentPosition().self_and_subtree_iter():
			t = p.v.t
			if t and not t.isVisited():
				t.setVisited()
				tnodes += 1
		#@nonl
		#@-node:<< count the number of tnodes >>
		#@nl
		self.put('<leo_header file_format="1" tnodes=')
		self.put_in_dquotes(str(tnodes))
		self.put(" max_tnode_index=")
		self.put_in_dquotes(str(tnodes))
		self.put("/>") ; self.put_nl()
	#@-node:putClipboardHeader
	#@+node:putEscapedString
	# Surprisingly, the call to xmlEscape here is _much_ faster than calling put for each characters of s.
	
	def putEscapedString (self,s):
	
		if s and len(s) > 0:
			self.put(self.xmlEscape(s))
	#@nonl
	#@-node:putEscapedString
	#@+node:putFindSettings
	def putFindSettings (self):
	
		c = self.c ; config = g.app.config
	
		self.put("<find_panel_settings")
		
		#@	<< put find settings that may exist in leoConfig.txt >>
		#@+node:<< put find settings that may exist in leoConfig.txt >>
		if config.configsExist and not config.read_only: # 8/6/02
			pass # config.update has already been called.
		else:
			self.put_flag(c.batch_flag,"batch")
			self.put_flag(c.ignore_case_flag,"ignore_case")
			self.put_flag(c.mark_changes_flag,"mark_changes")
			self.put_flag(c.mark_finds_flag,"mark_finds")
			self.put_flag(c.pattern_match_flag,"pattern_match")
			self.put_flag(c.reverse_flag,"reverse")
			self.put_flag(c.search_headline_flag,"search_headline")
			self.put_flag(c.search_body_flag,"search_body")
			self.put_flag(c.suboutline_only_flag,"suboutline_only")
			self.put_flag(c.whole_word_flag,"whole_word")
			self.put_flag(c.wrap_flag,"wrap")
			self.put_flag(c.node_only_flag,"node_only")
		
		self.put(">") ; self.put_nl()
		
		if config.configsExist and not config.read_only: # 8/6/02
			self.put_tab()
			self.put("<find_string></find_string>") ; self.put_nl()
		else:
			self.put_tab()
			self.put("<find_string>") ; self.putEscapedString(c.find_text)
			self.put("</find_string>") ; self.put_nl()
		
		if config.configsExist and not config.read_only: # 8/6/02
			self.put_tab()
			self.put("<change_string></change_string>") ; self.put_nl()
		else:
			self.put_tab()
			self.put("<change_string>") ; self.putEscapedString(c.change_text)
			self.put("</change_string>") ; self.put_nl()
		#@nonl
		#@-node:<< put find settings that may exist in leoConfig.txt >>
		#@nl
		
		self.put("</find_panel_settings>") ; self.put_nl()
	#@nonl
	#@-node:putFindSettings
	#@+node:fileCommands.putGlobals (changed for 4.0)
	def putGlobals (self):
	
		c = self.c
		self.put("<globals")
		#@	<< put the body/outline ratio >>
		#@+node:<< put the body/outline ratio >>
		# Puts an innumerate number of digits
		
		self.put(" body_outline_ratio=")
		self.put_in_dquotes(str(c.frame.ratio))
		#@nonl
		#@-node:<< put the body/outline ratio >>
		#@nl
		self.put(">") ; self.put_nl()
		#@	<< put the position of this frame >>
		#@+node:<< put the position of this frame >>
		width,height,left,top = c.frame.get_window_info()
		
		self.put_tab()
		self.put("<global_window_position")
		self.put(" top=") ; self.put_in_dquotes(str(top))
		self.put(" left=") ; self.put_in_dquotes(str(left))
		self.put(" height=") ; self.put_in_dquotes(str(height))
		self.put(" width=") ; self.put_in_dquotes(str(width))
		self.put("/>") ; self.put_nl()
		#@nonl
		#@-node:<< put the position of this frame >>
		#@nl
		#@	<< put the position of the log window >>
		#@+node:<< put the position of the log window >>
		top = left = height = width = 0 # no longer used
		self.put_tab()
		self.put("<global_log_window_position")
		self.put(" top=") ; self.put_in_dquotes(str(top))
		self.put(" left=") ; self.put_in_dquotes(str(left))
		self.put(" height=") ; self.put_in_dquotes(str(height))
		self.put(" width=") ; self.put_in_dquotes(str(width))
		self.put("/>") ; self.put_nl()
		#@nonl
		#@-node:<< put the position of the log window >>
		#@nl
		self.put("</globals>") ; self.put_nl()
	#@nonl
	#@-node:fileCommands.putGlobals (changed for 4.0)
	#@+node:putHeader
	def putHeader (self):
	
		tnodes = 0 ; clone_windows = 0 # Always zero in Leo2.
	
		self.put("<leo_header")
		self.put(" file_format=") ; self.put_in_dquotes("2")
		self.put(" tnodes=") ; self.put_in_dquotes(str(tnodes))
		self.put(" max_tnode_index=") ; self.put_in_dquotes(str(self.maxTnodeIndex))
		self.put(" clone_windows=") ; self.put_in_dquotes(str(clone_windows))
		self.put("/>") ; self.put_nl()
	#@nonl
	#@-node:putHeader
	#@+node:putLeoOutline (to clipboard)
	# Writes a Leo outline to s in a format suitable for pasting to the clipboard.
	
	def putLeoOutline (self):
	
		self.outputList = [] ; self.outputFile = None
		self.usingClipboard = true
		self.assignFileIndices() # 6/11/03: Must do this for 3.x code.
		self.putProlog()
		self.putClipboardHeader()
		self.putVnodes()
		self.putTnodes()
		self.putPostlog()
		s = ''.join(self.outputList) # 1/8/04: convert the list to a string.
		self.outputList = []
		self.usingClipboard = false
		return s
	#@nonl
	#@-node:putLeoOutline (to clipboard)
	#@+node:putPostlog
	def putPostlog (self):
	
		self.put("</leo_file>") ; self.put_nl()
	#@nonl
	#@-node:putPostlog
	#@+node:putPrefs
	def putPrefs (self):
	
		c = self.c ; config = g.app.config
	
		self.put("<preferences")
		
		if 0:
			self.put(" allow_rich_text=") ; self.put_dquoted_bool(0) # no longer used
		
		#@	<< put prefs that may exist in leoConfig.txt >>
		#@+node:<< put prefs that may exist in leoConfig.txt >> (putPrefs)
		language = c.target_language
		for name in xml_language_names:
			s = string.lower(name)
			s = string.replace(s,"/","")
			if s == language:
				language = name ; break
		
		if config.configsExist and not config.read_only: # 8/6/02
			pass # config.update has already been called.
		else:
			self.put(" defaultTargetLanguage=") ; self.put_in_dquotes(language)
			self.put(" node_only=") ; self.put_dquoted_bool(c.node_only_flag)
			self.put(" output_doc_chunks=") ; self.put_dquoted_bool(c.output_doc_flag)
			self.put(" page_width=") ; self.put_in_dquotes(str(c.page_width))
			self.put(" tab_width=") ; self.put_in_dquotes(str(c.tab_width))
			self.put(" tangle_bat=") ; self.put_dquoted_bool(c.tangle_batch_flag)
			self.put(" untangle_bat=") ; self.put_dquoted_bool(c.untangle_batch_flag)
			self.put(" use_header_flag=") ; self.put_dquoted_bool(c.use_header_flag)
		
		self.put(">") ; self.put_nl()
		# New in version 0.16
		#@<< put default directory >>
		#@+node:<< put default directory >>
		if config.configsExist:
			pass # Has been done earlier.
		elif len(c.tangle_directory) > 0:
			self.put_tab()
			self.put("<defaultDirectory>")
			self.putEscapedString(c.tangle_directory)
			self.put("</defaultDirectory>")
			self.put_nl()
		#@nonl
		#@-node:<< put default directory >>
		#@nl
		#@nonl
		#@-node:<< put prefs that may exist in leoConfig.txt >> (putPrefs)
		#@nl
		
		self.put("</preferences>") ; self.put_nl()
	#@nonl
	#@-node:putPrefs
	#@+node:putProlog
	def putProlog (self):
	
		c = self.c ; config = g.app.config
	
		#@	<< Put the <?xml...?> line >>
		#@+node:<< Put the <?xml...?> line >>
		# 1/22/03: use self.leo_file_encoding encoding.
		self.put(g.app.prolog_prefix_string)
		self.put_dquote() ; self.put(self.leo_file_encoding) ; self.put_dquote()
		self.put(g.app.prolog_postfix_string) ; self.put_nl()
		#@nonl
		#@-node:<< Put the <?xml...?> line >>
		#@nl
		#@	<< Put the optional <?xml-stylesheet...?> line >>
		#@+node:<< Put the optional <?xml-stylesheet...?> line >>
		if config.stylesheet or c.frame.stylesheet:
			
			# The stylesheet in the .leo file takes precedence over the default stylesheet.
			if c.frame.stylesheet:
				s = c.frame.stylesheet
			else:
				s = config.stylesheet
				
			tag = "<?xml-stylesheet "
			# print "writing:", tag + s + "?>"
			self.put(tag) ; self.put(s) ; self.put("?>") ; self.put_nl()
		#@-node:<< Put the optional <?xml-stylesheet...?> line >>
		#@nl
	
		self.put("<leo_file>") ; self.put_nl()
	#@nonl
	#@-node:putProlog
	#@+node:putTnode
	def putTnode (self,t):
	
		self.put("<t")
		self.put(" tx=")
	
		if g.app.use_gnx:
			gnx = g.app.nodeIndices.toString(t.fileIndex)
			self.put_in_dquotes(gnx)
		else:
			self.put_in_dquotes("T" + str(t.fileIndex))
	
		if hasattr(t,"unknownAttributes"):
			#@		<< put unknown tnode attributes >>
			#@+node:<< put unknown tnode attributes >>
			attrDict = t.unknownAttributes
			keys = attrDict.keys()
			for key in keys:
				val = attrDict[key]
				attr = ' %s="%s"' % (key,self.xmlEscape(val))
				self.put(attr)
				if 1: # For debugging.
					s = "putting unknown tnode attribute"
					print s ;  g.es(s, color="red")
					print attr, g.es(attr)
			#@nonl
			#@-node:<< put unknown tnode attributes >>
			#@nl
		self.put(">")
	
		# g.trace(t)
		if t.bodyString:
			self.putEscapedString(t.bodyString)
	
		self.put("</t>") ; self.put_nl()
	#@nonl
	#@-node:putTnode
	#@+node:putTnodeList (4.0,4.2)
	def putTnodeList (self,v):
		
		"""Put the tnodeList attribute of a tnode."""
		
		# g.trace(v)
		
		# Remember: entries in the tnodeList correspond to @+node sentinels, _not_ to tnodes!
	
		fc = self ; nodeIndices = g.app.nodeIndices
		tnodeList = v.t.tnodeList
		if tnodeList:
			# g.trace("%4d" % len(tnodeList),v)
			fc.put(" tnodeList=") ; fc.put_dquote()
			if g.app.use_gnx:
				for t in tnodeList:
					try: # Will fail for None or any pre 4.1 file index.
						id,time,n = t.fileIndex
					except:
						g.trace("assigning gnx for ",v,t)
						gnx = nodeIndices.getNewIndex()
						v.t.setFileIndex(gnx) # Don't convert to string until the actual write.
				s = ','.join([nodeIndices.toString(t.fileIndex) for t in tnodeList])
			else:
				s = ','.join([str(t.fileIndex) for t in tnodeList])
			fc.put(s) ; fc.put_dquote()
	#@nonl
	#@-node:putTnodeList (4.0,4.2)
	#@+node:putTnodes
	def putTnodes (self):
		
		"""Puts all tnodes as required for copy or save commands"""
	
		c = self.c
	
		self.put("<tnodes>") ; self.put_nl()
		#@	<< write only those tnodes that were referenced >>
		#@+node:<< write only those tnodes that were referenced >>
		# Populate tnodes
		tnodes = {}
		
		if self.usingClipboard: # write the current tree.
			root = c.currentPosition()
		else: # write everything
			root = c.rootPosition()
		
		for p in c.allNodes_iter():
			index = p.v.t.fileIndex
			assert(index)
			tnodes[index] = p.v.t
		
		# Put all tnodes in index order.
		keys = tnodes.keys() ; keys.sort()
		for index in keys:
			# g.trace(index)
			t = tnodes.get(index)
			assert(t)
			# Write only those tnodes whose vnodes were written.
			if t.isVisited():
				self.putTnode(t)
		#@nonl
		#@-node:<< write only those tnodes that were referenced >>
		#@nl
		self.put("</tnodes>") ; self.put_nl()
	#@nonl
	#@-node:putTnodes
	#@+node:putVnode (3.x and 4.x)
	def putVnode (self,p):
	
		"""Write a <v> element corresponding to a vnode."""
	
		fc = self ; c = fc.c ; v = p.v
	
		fc.put("<v")
		#@	<< Put tnode index >>
		#@+node:<< Put tnode index >>
		if v.t.fileIndex:
			if g.app.use_gnx:
				gnx = g.app.nodeIndices.toString(v.t.fileIndex)
				fc.put(" t=") ; fc.put_in_dquotes(gnx)
			else:
				fc.put(" t=") ; fc.put_in_dquotes("T" + str(v.t.fileIndex))
				
			# g.trace(v.t)
			v.t.setVisited() # Indicate we wrote the body text.
		else:
			g.trace(v.t.fileIndex,v)
			g.es("error writing file(bad v.t.fileIndex)!")
			g.es("try using the Save To command")
		#@nonl
		#@-node:<< Put tnode index >>
		#@nl
		#@	<< Put attribute bits >>
		#@+node:<< Put attribute bits >>
		attr = ""
		if p.v.isExpanded():          attr += "E"
		if p.v.isMarked():            attr += "M"
		if p.v.isOrphan():            attr += "O"
		if 1: # No longer a bottleneck now that we use p.equal rather than p.__cmp__
			# Almost 30% of the entire writing time came from here!!!
			if p.equal(self.topPosition):     attr += "T" # was a bottleneck
			if p.equal(self.currentPosition): attr += "V" # was a bottleneck
		
		if attr: fc.put(' a="%s"' % attr)
		#@-node:<< Put attribute bits >>
		#@nl
		#@	<< Put tnodeList and unKnownAttributes >>
		#@+node:<< Put tnodeList and unKnownAttributes >>
		# Write tnodeList only for @file nodes.
		# New in 4.2: tnode list is in tnode.
		
		if hasattr(v.t,"tnodeList") and len(v.t.tnodeList) > 0 and v.isAnyAtFileNode():
			fc.putTnodeList(v) # New in 4.0
		
		if hasattr(v,"unknownAttributes"): # New in 4.0
			#@	<< put unknown vnode attributes >>
			#@+node:<< put unknown vnode attributes >>
			attrDict = v.unknownAttributes
			keys = attrDict.keys()
			for key in keys:
				val = attrDict[key]
				attr = ' %s="%s"' % (key,self.xmlEscape(val))
				self.put(attr)
				if 0: # For debugging.
					s = "putting unknown attribute for " + v.headString()
					print s ;  g.es(s, color="red")
					print attr, g.es(attr)
			#@nonl
			#@-node:<< put unknown vnode attributes >>
			#@nl
		#@nonl
		#@-node:<< Put tnodeList and unKnownAttributes >>
		#@nl
		fc.put(">")
		#@	<< Write the head text >>
		#@+node:<< Write the head text >>
		headString = p.v.headString()
		
		if headString:
			fc.put("<vh>")
			fc.putEscapedString(headString)
			fc.put("</vh>")
		#@nonl
		#@-node:<< Write the head text >>
		#@nl
	
		# New in 4.2: don't write child nodes of @file-thin trees.
		if p.hasChildren():
			if p.isAtThinFileNode() and not p.isOrphan():
				# g.trace("skipping child vnodes for", p.headString())
				pass
			else:
				fc.put_nl()
				# This optimization eliminates all "recursive" copies.
				p.moveToFirstChild()
				while 1:
					fc.putVnode(p)
					if p.hasNext(): p.moveToNext()
					else:           break
				p.moveToParent()
	
		fc.put("</v>") ; fc.put_nl()
	#@nonl
	#@-node:putVnode (3.x and 4.x)
	#@+node:putVnodes
	def putVnodes (self):
	
		"""Puts all <v> elements in the order in which they appear in the outline."""
	
		c = self.c
		c.clearAllVisited()
	
		self.put("<vnodes>") ; self.put_nl()
	
		# Make only one copy for all calls.
		self.currentPosition = c.currentPosition() 
		self.topPosition     = c.topPosition()
	
		if self.usingClipboard:
			self.putVnode(self.currentPosition) # Write only current tree.
		else:
			for p in c.rootPosition().self_and_siblings_iter():
				self.putVnode(p) # Write the next top-level node.
	
		self.put("</vnodes>") ; self.put_nl()
	#@nonl
	#@-node:putVnodes
	#@+node:save
	def save(self,fileName):
	
		c = self.c ; v = c.currentVnode()
	
		if not g.doHook("save1",c=c,v=v,fileName=fileName):
			c.beginUpdate()
			c.endEditing()# Set the current headline text.
			self.compactFileIndices()
			self.setDefaultDirectoryForNewFiles(fileName)
			if self.write_Leo_file(fileName,false): # outlineOnlyFlag
				c.setChanged(false) # Clears all dirty bits.
				g.es("saved: " + g.shortFileName(fileName))
				if g.app.config.save_clears_undo_buffer:
					g.es("clearing undo")
					c.undoer.clearUndoState()
			c.endUpdate()
		g.doHook("save2",c=c,v=v,fileName=fileName)
	#@nonl
	#@-node:save
	#@+node:saveAs
	def saveAs(self,fileName):
	
		c = self.c ; v = c.currentVnode()
	
		if not g.doHook("save1",c=c,v=v,fileName=fileName):
			c.beginUpdate()
			c.endEditing() # Set the current headline text.
			self.compactFileIndices()
			self.setDefaultDirectoryForNewFiles(fileName)
			if self.write_Leo_file(fileName,false): # outlineOnlyFlag
				c.setChanged(false) # Clears all dirty bits.
				g.es("saved: " + g.shortFileName(fileName))
			c.endUpdate()
		g.doHook("save2",c=c,v=v,fileName=fileName)
	#@-node:saveAs
	#@+node:saveTo
	def saveTo (self,fileName):
	
		c = self.c ; v = c.currentVnode()
	
		if not g.doHook("save1",c=c,v=v,fileName=fileName):
			c.beginUpdate()
			c.endEditing()# Set the current headline text.
			self.compactFileIndices()
			self.setDefaultDirectoryForNewFiles(fileName)
			if self.write_Leo_file(fileName,false): # outlineOnlyFlag
				g.es("saved: " + g.shortFileName(fileName))
			c.endUpdate()
		g.doHook("save2",c=c,v=v,fileName=fileName)
	#@-node:saveTo
	#@+node:setDefaultDirectoryForNewFiles
	def setDefaultDirectoryForNewFiles (self,fileName):
		
		"""Set c.openDirectory for new files for the benefit of leoAtFile.scanAllDirectives."""
		
		c = self.c
	
		if not c.openDirectory or len(c.openDirectory) == 0:
			dir = g.os_path_dirname(fileName)
	
			if len(dir) > 0 and g.os_path_isabs(dir) and g.os_path_exists(dir):
				c.openDirectory = dir
	#@nonl
	#@-node:setDefaultDirectoryForNewFiles
	#@+node:write_Leo_file
	def write_Leo_file(self,fileName,outlineOnlyFlag):
	
		c = self.c ; config = g.app.config
	
		if not outlineOnlyFlag:
			#@		<< write all @file nodes >>
			#@+node:<< write all @file nodes >>
			try:
				# Write all @file nodes and set orphan bits.
				c.atFileCommands.writeAll()
			except:
				g.es_error("exception writing derived files")
				g.es_exception()
				return false
			#@nonl
			#@-node:<< write all @file nodes >>
			#@nl
		#@	<< return if the .leo file is read-only >>
		#@+node:<< return if the .leo file is read-only >>
		# self.read_only is not valid for Save As and Save To commands.
		
		if g.os_path_exists(fileName):
			try:
				if not os.access(fileName,os.W_OK):
					self.writeError("can not create: read only: " + self.targetFileName)
					return false
			except:
				pass # os.access() may not exist on all platforms.
		#@nonl
		#@-node:<< return if the .leo file is read-only >>
		#@nl
		try:
			#@		<< create backup file >>
			#@+node:<< create backup file >>
			# rename fileName to fileName.bak if fileName exists.
			if g.os_path_exists(fileName):
				try:
					backupName = g.os_path_join(g.app.loadDir,fileName)
					backupName = fileName + ".bak"
					if g.os_path_exists(backupName):
						os.unlink(backupName)
					# os.rename(fileName,backupName)
					g.utils_rename(fileName,backupName)
				except OSError:
					if self.read_only:
						g.es("read only",color="red")
					else:
						g.es("exception creating backup file: " + backupName)
						g.es_exception()
					return false
				except:
					g.es("exception creating backup file: " + backupName)
					g.es_exception()
					backupName = None
					return false
			else:
				backupName = None
			#@nonl
			#@-node:<< create backup file >>
			#@nl
			self.mFileName = fileName
			#@		<< create the output file >>
			#@+node:<< create the output file >>
			self.outputFile = open(fileName, 'wb') # 9/18/02
			if not self.outputFile:
				g.es("can not open " + fileName)
				#@	<< delete backup file >>
				#@+node:<< delete backup file >>
				if backupName and g.os_path_exists(backupName):
					try:
						os.unlink(backupName)
					except OSError:
						if self.read_only:
							g.es("read only",color="red")
						else:
							g.es("exception deleting backup file:" + backupName)
							g.es_exception()
						return false
					except:
						g.es("exception deleting backup file:" + backupName)
						g.es_exception()
						return false
				#@-node:<< delete backup file >>
				#@nl
				return false
			#@nonl
			#@-node:<< create the output file >>
			#@nl
			#@		<< update leoConfig.txt >>
			#@+node:<< update leoConfig.txt >>
			c.setIvarsFromFind()
			config.setConfigFindIvars(c)
			c.setIvarsFromPrefs()
			config.setCommandsIvars(c)
			config.update()
			#@nonl
			#@-node:<< update leoConfig.txt >>
			#@nl
			#@		<< put the .leo file >>
			#@+node:<< put the .leo file >>
			self.putProlog()
			self.putHeader()
			self.putGlobals()
			self.putPrefs()
			self.putFindSettings()
			#start = g.getTime()
			self.putVnodes()
			#start = g.printDiffTime("vnodes ",start)
			self.putTnodes()
			#start = g.printDiffTime("tnodes ",start)
			self.putPostlog()
			#@nonl
			#@-node:<< put the .leo file >>
			#@nl
		except:
			#@		<< report the exception >>
			#@+node:<< report the exception >>
			g.es("exception writing: " + fileName)
			g.es_exception() 
			if self.outputFile:
				try:
					self.outputFile.close()
					self.outputFile = None
				except:
					g.es("exception closing: " + fileName)
					g.es_exception()
			#@nonl
			#@-node:<< report the exception >>
			#@nl
			#@		<< erase filename and rename backupName to fileName >>
			#@+node:<< erase filename and rename backupName to fileName >>
			g.es("error writing " + fileName)
			
			if fileName and g.os_path_exists(fileName):
				try:
					os.unlink(fileName)
				except OSError:
					if self.read_only:
						g.es("read only",color="red")
					else:
						g.es("exception deleting: " + fileName)
						g.es_exception()
				except:
					g.es("exception deleting: " + fileName)
					g.es_exception()
					
			if backupName:
				g.es("restoring " + fileName + " from " + backupName)
				try:
					g.utils_rename(backupName, fileName)
				except OSError:
					if self.read_only:
						g.es("read only",color="red")
					else:
						g.es("exception renaming " + backupName + " to " + fileName)
						g.es_exception()
				except:
					g.es("exception renaming " + backupName + " to " + fileName)
					g.es_exception()
			#@nonl
			#@-node:<< erase filename and rename backupName to fileName >>
			#@nl
			return false
		if self.outputFile:
			#@		<< close the output file >>
			#@+node:<< close the output file >>
			try:
				self.outputFile.close()
				self.outputFile = None
			except:
				g.es("exception closing: " + fileName)
				g.es_exception()
			#@nonl
			#@-node:<< close the output file >>
			#@nl
			#@		<< delete backup file >>
			#@+node:<< delete backup file >>
			if backupName and g.os_path_exists(backupName):
				try:
					os.unlink(backupName)
				except OSError:
					if self.read_only:
						g.es("read only",color="red")
					else:
						g.es("exception deleting backup file:" + backupName)
						g.es_exception()
					return false
				except:
					g.es("exception deleting backup file:" + backupName)
					g.es_exception()
					return false
			#@-node:<< delete backup file >>
			#@nl
			return true
		else: # This probably will never happen because errors should raise exceptions.
			#@		<< erase filename and rename backupName to fileName >>
			#@+node:<< erase filename and rename backupName to fileName >>
			g.es("error writing " + fileName)
			
			if fileName and g.os_path_exists(fileName):
				try:
					os.unlink(fileName)
				except OSError:
					if self.read_only:
						g.es("read only",color="red")
					else:
						g.es("exception deleting: " + fileName)
						g.es_exception()
				except:
					g.es("exception deleting: " + fileName)
					g.es_exception()
					
			if backupName:
				g.es("restoring " + fileName + " from " + backupName)
				try:
					g.utils_rename(backupName, fileName)
				except OSError:
					if self.read_only:
						g.es("read only",color="red")
					else:
						g.es("exception renaming " + backupName + " to " + fileName)
						g.es_exception()
				except:
					g.es("exception renaming " + backupName + " to " + fileName)
					g.es_exception()
			#@nonl
			#@-node:<< erase filename and rename backupName to fileName >>
			#@nl
			return false
	#@nonl
	#@-node:write_Leo_file
	#@+node:writeAtFileNodes
	def writeAtFileNodes (self):
		
		c = self.c
	
		changedFiles = c.atFileCommands.writeAll(writeAtFileNodesFlag=true)
		assert(changedFiles != None)
		if changedFiles:
			g.es("auto-saving outline",color="blue")
			c.save() # Must be done to set or clear tnodeList.
	#@nonl
	#@-node:writeAtFileNodes
	#@+node:writeDirtyAtFileNodes
	def writeDirtyAtFileNodes (self): # fileCommands
	
		"""The Write Dirty @file Nodes command"""
		
		c = self.c
	
		changedFiles = c.atFileCommands.writeAll(writeDirtyAtFileNodesFlag=true)
		if changedFiles:
			g.es("auto-saving outline",color="blue")
			c.save() # Must be done to set or clear tnodeList.
	#@nonl
	#@-node:writeDirtyAtFileNodes
	#@+node:writeMissingAtFileNodes
	def writeMissingAtFileNodes (self):
	
		c = self.c ; v = c.currentVnode()
	
		if v:
			at = c.atFileCommands
			changedFiles = at.writeMissing(v)
			assert(changedFiles != None)
			if changedFiles:
				g.es("auto-saving outline",color="blue")
				c.save() # Must be done to set or clear tnodeList.
	#@nonl
	#@-node:writeMissingAtFileNodes
	#@+node:writeOutlineOnly
	def writeOutlineOnly (self):
	
		c = self.c
		c.endEditing()
		self.compactFileIndices()
		self.write_Leo_file(self.mFileName,true) # outlineOnlyFlag
	#@nonl
	#@-node:writeOutlineOnly
	#@+node:xmlEscape
	# Surprisingly, this is a time critical routine.
	
	def xmlEscape(self,s):
	
		assert(s and len(s) > 0) # check is made in putEscapedString
		s = string.replace(s, '\r', '')
		s = string.replace(s, '&', "&amp;")
		s = string.replace(s, '<', "&lt;")
		s = string.replace(s, '>', "&gt;")
		return s
	#@nonl
	#@-node:xmlEscape
	#@-others
	
class fileCommands (baseFileCommands):
	"""A class creating the fileCommands subcommander."""
	pass
#@-node:@file leoFileCommands.py
#@-leo
