#@+leo-ver=4
#@+node:@file leoFileCommands.py
#@@language python

from leoGlobals import *
import leoNodes
import os,time

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
	
		# trace("__init__", "fileCommands.__init__")
		self.c = c
		self.frame = c.frame
		self.initIvars()
	
	def initIvars(self):
	
		# General
		self.maxTnodeIndex = 0
		self.numberOfTnodes = 0
		self.topVnode = None
		self.mFileName = ""
		self.fileDate = -1
		self.leo_file_encoding = app.config.new_leo_file_encoding
		# For reading
		self.fileFormatNumber = 0
		self.ratio = 0.5
		self.fileBuffer = None ; self.fileIndex = 0
		# For writing
		self.read_only = false
		self.outputFile = None # File for normal writing
		self.outputString = None # String for pasting
		self.openDirectory = None
		self.usingClipboard = false
		# New in 3.12
		self.copiedTree = None
		self.tnodesDict = {}
	#@nonl
	#@-node:leoFileCommands._init_
	#@+node:canonicalTnodeIndex
	def canonicalTnodeIndex(self,index):
		
		"""Convert Tnnn to nnn, leaving gnx's unchanged."""
	
		# index might be Tnnn, nnn, or gnx.
		id,time,n = app.nodeIndices.scanGnx(index,0)
		if time == None: # A pre-4.1 file index.
			if index[0] == "T":
				index = index[1:]
	
		return index
	#@nonl
	#@-node:canonicalTnodeIndex
	#@+node:createVnode
	def createVnode(self,parent,back,tref,headline,attrDict):
		
		# trace(`headline` + ", parent:" + `parent` + ", back:" + `back`)
		v = None ; c = self.c
		# Shared tnodes are placed in the file even if empty.
		if tref == -1:
			t = leoNodes.tnode()
		else:
			tref = self.canonicalTnodeIndex(tref)
			t = self.tnodesDict.get(tref)
			if not t:
				t = self.newTnode(tref)
		if back: # create v after back.
			v = back.insertAfter(t)
		elif parent: # create v as the parent's first child.
			v = parent.insertAsNthChild(0,t)
		else: # create a root vnode
			v = leoNodes.vnode(c,t)
			v.moveToRoot()
			c.frame.tree.setRootVnode(v)
		v.initHeadString(headline,encoding=self.leo_file_encoding)
		#@	<< handle unknown vnode attributes >>
		#@+node:<< handle unknown vnode attributes >>
		keys = attrDict.keys()
		if keys:
			v.unknownAttributes = attrDict
			if 0: # For debugging.
				s = "unknown attributes for " + v.headString()
				print s ; es(s, color = "blue")
				for key in keys:
					s = "%s = %s" % (key,attrDict.get(key))
					print s ; es(s)
		#@nonl
		#@-node:<< handle unknown vnode attributes >>
		#@nl
		return v
	#@nonl
	#@-node:createVnode
	#@+node:finishPaste
	# This method finishes pasting the outline from the clipboard.
	def finishPaste(self):
	
		c = self.c
		current = c.currentVnode()
		after = current.nodeAfterTree()
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
		
		v = current
		v.clearVisitedInTree()
		after = v.nodeAfterTree()
		
		while v and v != after:
			if not v.t.isVisited():
				v.t.setVisited()
				self.maxTnodeIndex += 1
				v.t.setFileIndex(self.maxTnodeIndex)
				# trace(v,self.maxTnodeIndex)
			v = v.threadNext()
		#@nonl
		#@-node:<< reassign tnode indices and clear all clone links >>
		#@nl
		self.setAllJoinLinks(root=current) # 12/8/03
		c.initAllCloneBits() # 12/8/03
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
		trace(tag,val)
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
		j = skip_c_id(self.fileBuffer,i)
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
	
		c = self.c ; config = app.config ; findFrame = app.findFrame
		#@	<< Set defaults of all flags >>
		#@+node:<< Set defaults of all flags >>
		if app.gui.guiName() == "tkinter":
		
			for var in findFrame.intKeys:
				attr = "%s_flag" % (var)
				setattr(c,attr,false)
				# trace(attr)
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
		if app.gui.guiName() == "tkinter":
			app.findFrame.init(c)
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
	#@+node:getLeoFile (calls setAllJoinLinks, initAllCloneBits)
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
				es("read only: " + fileName,color="red")
		except:
			if 0: # testing only: access may not exist on all platforms.
				es("exception getting file access")
				es_exception()
		#@nonl
		#@-node:<< warn on read-only files >>
		#@nl
		self.mFileName = c.mFileName
		self.tnodesDict = {}
		ok = true
		c.frame.tree.setIniting(true) # Disable changes in endEditLabel
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
			es("reading: " + fileName)
			
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
			
			es_exception()
			alert(self.mFileName + " is not a valid Leo file: " + `message`)
			#@nonl
			#@-node:<< raise an alert >>
			#@nl
			ok = false
		self.setAllJoinLinks() # 9/23/03: Must do this before reading @file nodes.
		c.initAllCloneBits() # 9/23/03
		if ok and atFileNodesFlag:
			c.atFileCommands.readAll(c.rootVnode(),partialFlag=false)
		if not c.frame.tree.currentVnode():
			c.frame.tree.setCurrentVnode(c.rootVnode())
		c.selectVnode(c.frame.tree.currentVnode()) # load body pane
		c.frame.tree.setIniting(false) # Enable changes in endEditLabel
		c.loading = false # reenable c.changed
		c.setChanged(c.changed) # Refresh the changed marker.
		self.tnodesDict = {}
		return ok, self.ratio
	#@nonl
	#@-node:getLeoFile (calls setAllJoinLinks, initAllCloneBits)
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
				# trace("max_tnode_index:",self.maxTnodeIndex)
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
	
		c = self.c ; config = app.config
		
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
				if not os_path_exists(c.tangle_directory):
					es("default tangle directory not found:" + c.tangle_directory)
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
		for name in app.language_delims_dict.keys():
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
			elif self.matchTag(">"):
				break
			else: # New for 4.0: allow unknown attributes.
				attr,val = self.getUnknownTag()
				attrDict[attr] = val
				
		if app.use_gnx:
			# index might be Tnnn, nnn, or gnx.
			id,time,n = app.nodeIndices.scanGnx(index,0)
			if time == None: # A pre-4.1 file index.
				if index[0] == "T":
					index = index[1:]
	
		index = self.canonicalTnodeIndex(index)
		t = self.tnodesDict.get(index)
		# trace(t)
		#@	<< handle unknown attributes >>
		#@+node:<< handle unknown attributes >>
		keys = attrDict.keys()
		if keys:
			t.unknownAttributes = attrDict
			if 0: # For debugging.
				s = "unknown attributes for tnode"
				print s ; es(s, color = "blue")
				for key in keys:
					s = "%s = %s" % (key,attrDict.get(key))
					print s ; es(s)
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
					# trace(`index`,`len(s)`)
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
			es("no tnode with index: " + `index` + ".  The text will be discarded")
		self.getTag("</t>")
	#@nonl
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
	#@+node:getVnode
	def getVnode (self,parent,back):
	
		# trace("parent:" + `parent` + ", back:" + `back`)
		c = self.c
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
		# Link v into the outline using parent and back.
		v = self.createVnode(parent,back,tref,headline,attrDict)
		if tnodeList:
			v.tnodeList = tnodeList # New for 4.0
			# trace("%4d" % len(tnodeList),v)
		#@	<< Set the remembered status bits >>
		#@+node:<< Set the remembered status bits >>
		if setCurrent:
			c.frame.tree.setCurrentVnode(v)
		
		if setExpanded:
			v.initExpandedBit()
		
		if setMarked:
			v.setMarked()
		
		if setOrphan:
			v.setOrphan()
		
		if setTop:
			c.mTopVnode = v  # Not used at present.
		
		#@-node:<< Set the remembered status bits >>
		#@nl
		# Recursively create all nested nodes.
		parent = v ; back = None
		while self.matchTag("<v"):
			back = self.getVnode(parent,back)
		# End this vnode.
		self.getTag("</v>")
		return v
	#@nonl
	#@-node:getVnode
	#@+node:getTnodeList (4.0)
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
				# trace("not allocated: %s" % index)
				t = self.newTnode(index)
			tnodeList.append(t)
			
		return tnodeList
	#@nonl
	#@-node:getTnodeList (4.0)
	#@+node:getVnodes
	def getVnodes (self):
	
		c = self.c
		if  self.usingClipboard:
			# Paste after the current vnode.
			back = c.currentVnode() ; parent = back.parent()
		else:
			back = None ; parent = None
	
		if self.getOpenTag("<vnodes>"):
			return
	
		while self.matchTag("<v"):
			back = self.getVnode(parent,back)
	
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
	
		self.getTag(app.prolog_prefix_string)
		encoding = self.getDqString()
		self.getTag(app.prolog_postfix_string)
	
		if isValidEncoding(encoding):
			self.leo_file_encoding = encoding
			es("File encoding: " + encoding, color="blue")
		else:
			es("invalid encoding in .leo file: " + encoding, color="red")
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
			es("bad tnode index: " + `index` + ". Using empty text.")
			return leoNodes.tnode()
		else:
			# Create the tnode.  Use the _original_ index as the key in tnodesDict.
			t = leoNodes.tnode()
			self.tnodesDict[index] = t
		
			if type(index) not in (type(""),type(u"")):
				es("newTnode: unexpected index type:"+`type(index)`+`index`,color="red")
			
			# Convert any pre-4.1 index to a gnx.
			id,time,n = gnx = app.nodeIndices.scanGnx(index,0)
			if time != None:
				t.setFileIndex(gnx)
	
			return t
	#@nonl
	#@-node:newTnode
	#@+node:readAtFileNodes
	def readAtFileNodes (self):
	
		c = self.c ; current = c.currentVnode()
		c.atFileCommands.readAll(current,partialFlag=true)
		self.setAllJoinLinks(current) # 5/3/03
		c.initAllCloneBits() # 5/3/03
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
		
		dir = os_path_dirname(fileName)
		
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
		# This should be done after the pane size has been set.
		if 0: # This can not be done at present.
			if self.topVnode:
				c.frame.tree.scrollTo(self.topVnode)
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
		
		dir = os_path_dirname(fileName)
		
		if len(dir) > 0:
			c.openDirectory = dir
		#@nonl
		#@-node:<< Set the default directory >> in fileCommands.readOutlineOnly
		#@nl
		c.beginUpdate()
		ok, ratio = self.getLeoFile(fileName,atFileNodesFlag=true)
		frame.resizePanesToRatio(ratio,frame.secondary_ratio) # 12/2/03
		#@	<< Make the top node visible >>
		#@+node:<< Make the top node visible >>
		if 0: # This can't be done directly.
		
			# This should be done after the pane size has been set.
			top = c.frame.tree.topVnode()
		
			if top:
				c.frame.tree.scrollTo(top)
		#@nonl
		#@-node:<< Make the top node visible >>
		#@nl
		c.endUpdate()
		# delete the file buffer
		self.fileBuffer = ""
		return ok
	#@nonl
	#@-node:fileCommands.open
	#@+node:fileCommands.setAllJoinLinks
	def setAllJoinLinks (self,root=None):
		
		"""Update all join links in the tree"""
	
		if root: # Only update the subtree.
			v = root # 6/3/03
			after = root.nodeAfterTree()
			while v and v != after:
				if v not in v.t.joinList:
					v.t.joinList.append(v)
				v = v.threadNext()
		else: # Update everything.
			v = self.c.rootVnode()
			while v:
				# trace(v,v.t)
				if v not in v.t.joinList:
					v.t.joinList.append(v)
				v = v.threadNext()
	#@nonl
	#@-node:fileCommands.setAllJoinLinks
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
		
		c = self.c ; nodeIndices = app.nodeIndices
		root = c.rootVnode() # 4.1: Always assign all indices.
		nodeIndices.setTimestamp() # This call is fairly expensive.
		
		# trace(app.use_gnx,root)
	
		if app.use_gnx:
			#@		<< assign missing gnx's, converting ints to gnx's >>
			#@+node:<< assign missing gnx's, converting ints to gnx's >>
			# Always assign an (immutable) index, even if the tnode is empty.
			
			v = root
			while v:
				try: # Will fail for None or any pre 4.1 file index.
					id,time,n = v.t.fileIndex
				except:
					# Don't convert to string until the actual write.
					v.t.fileIndex = nodeIndices.getNewIndex()
				v = v.threadNext()
			#@nonl
			#@-node:<< assign missing gnx's, converting ints to gnx's >>
			#@nl
		else:
			#@		<< reassign all tnode indices >>
			#@+node:<< reassign all tnode indices >>
			# Clear out all indices.
			v = root
			while v:
				v.t.fileIndex = None
				v = v.threadNext()
				
			# Recreate integer indices.
			self.maxTnodeIndex = 0
			v = root
			while v:
				if v.t.fileIndex == None:
					self.maxTnodeIndex += 1
					v.t.fileIndex = self.maxTnodeIndex
				v = v.threadNext()
			#@nonl
			#@-node:<< reassign all tnode indices >>
			#@nl
	
	# Indices are now immutable, so there is no longer any difference between these two routines.
	compactFileIndices = assignFileIndices
	#@nonl
	#@-node:assignFileIndices & compactFileIndices
	#@+node:put (basic)(leoFileCommands)
	# All output eventually comes here.
	def put (self,s):
		if s and len(s) > 0:
			if self.outputFile:
				s = toEncodedString(s,self.leo_file_encoding,reportErrors=true)
				self.outputFile.write(s)
			elif self.outputString != None: # Write to a string
				self.outputString += s
	
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
	#@nonl
	#@-node:put (basic)(leoFileCommands)
	#@+node:putClipboardHeader
	def putClipboardHeader (self):
	
		tnodes = 0
		#@	<< count the number of tnodes >>
		#@+node:<< count the number of tnodes >>
		c = self.c
		c.clearAllVisited()
		
		# Count the vnode and tnodes.
		v = c.currentVnode()
		after = v.nodeAfterTree()
		while v and v != after:
			t = v.t
			# if t and not t.isVisited() and (t.hasBody() or len(v.t.joinList) > 0):
			if t and not t.isVisited():
				t.setVisited()
				tnodes += 1
			v = v.threadNext()
		#@nonl
		#@-node:<< count the number of tnodes >>
		#@nl
		self.put('<leo_header file_format="1" tnodes=')
		self.put_in_dquotes(`tnodes`)
		self.put(" max_tnode_index=")
		self.put_in_dquotes(`tnodes`)
		self.put("/>") ; self.put_nl()
	#@nonl
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
	
		c = self.c ; config = app.config
	
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
		
		self.put(" body_outline_ratio=") ; self.put_in_dquotes(`c.frame.ratio`)
		#@nonl
		#@-node:<< put the body/outline ratio >>
		#@nl
		self.put(">") ; self.put_nl()
		#@	<< put the position of this frame >>
		#@+node:<< put the position of this frame >>
		width,height,left,top = c.frame.get_window_info()
		
		self.put_tab()
		self.put("<global_window_position")
		self.put(" top=") ; self.put_in_dquotes(`top`)
		self.put(" left=") ; self.put_in_dquotes(`left`)
		self.put(" height=") ; self.put_in_dquotes(`height`)
		self.put(" width=") ; self.put_in_dquotes(`width`)
		self.put("/>") ; self.put_nl()
		#@nonl
		#@-node:<< put the position of this frame >>
		#@nl
		#@	<< put the position of the log window >>
		#@+node:<< put the position of the log window >>
		top = left = height = width = 0 # no longer used
		self.put_tab()
		self.put("<global_log_window_position")
		self.put(" top=") ; self.put_in_dquotes(`top`)
		self.put(" left=") ; self.put_in_dquotes(`left`)
		self.put(" height=") ; self.put_in_dquotes(`height`)
		self.put(" width=") ; self.put_in_dquotes(`width`)
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
		self.put(" tnodes=") ; self.put_in_dquotes(`tnodes`)
		self.put(" max_tnode_index=") ; self.put_in_dquotes(`self.maxTnodeIndex`)
		self.put(" clone_windows=") ; self.put_in_dquotes(`clone_windows`)
		self.put("/>") ; self.put_nl()
	#@nonl
	#@-node:putHeader
	#@+node:putLeoOutline (to clipboard)
	# Writes a Leo outline to s in a format suitable for pasting to the clipboard.
	
	def putLeoOutline (self):
	
		self.outputString = "" ; self.outputFile = None
		self.usingClipboard = true
		self.assignFileIndices() # 6/11/03: Must do this for 3.x code.
		self.putProlog()
		self.putClipboardHeader()
		self.putVnodes()
		self.putTnodes()
		self.putPostlog()
		s = self.outputString
		self.outputString = None
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
	
		c = self.c ; config = app.config
	
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
			self.put(" page_width=") ; self.put_in_dquotes(`c.page_width`)
			self.put(" tab_width=") ; self.put_in_dquotes(`c.tab_width`)
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
	
		c = self.c ; config = app.config
	
		#@	<< Put the <?xml...?> line >>
		#@+node:<< Put the <?xml...?> line >>
		# 1/22/03: use self.leo_file_encoding encoding.
		self.put(app.prolog_prefix_string)
		self.put_dquote() ; self.put(self.leo_file_encoding) ; self.put_dquote()
		self.put(app.prolog_postfix_string) ; self.put_nl()
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
		if app.use_gnx:
			gnx = app.nodeIndices.toString(t.fileIndex)
			self.put_in_dquotes(gnx)
		else:
			self.put_in_dquotes("T" + `t.fileIndex`)
	
		if hasattr(t,"unknownAttributes"):
			#@		<< put unknown tnode attributes >>
			#@+node:<< put unknown tnode attributes >>
			attrDict = t.unknownAttributes
			keys = attrDict.keys()
			for key in keys:
				val = attrDict[key]
				attr = ' %s="%s"' % (key,self.xmlEscape(val))
				self.put(attr)
				if 0: # For debugging.
					s = "putting unknown tnode attribute"
					print s ;  es(s, color="red")
					print attr, es(attr)
			#@nonl
			#@-node:<< put unknown tnode attributes >>
			#@nl
		self.put(">")
	
		if t.bodyString:
			self.putEscapedString(t.bodyString)
	
		self.put("</t>") ; self.put_nl()
	#@nonl
	#@-node:putTnode
	#@+node:putTnodeList (4.0)
	def putTnodeList (self,v):
		
		"""Put the optional tnodeList attribute of a vnode."""
		
		# Remember: entries in the tnodeList correspond to @+node sentinels, _not_ to tnodes!
	
		fc = self ; nodeIndices = app.nodeIndices
		if v.tnodeList:
			# trace("%4d" % len(v.tnodeList),v)
			fc.put(" tnodeList=") ; fc.put_dquote()
			if app.use_gnx:
				for t in v.tnodeList:
					try: # Will fail for None or any pre 4.1 file index.
						id,time,n = t.fileIndex
					except:
						trace("assigning gnx for ",v,t)
						gnx = nodeIndices.getNewIndex()
						t.setFileIndex(gnx) # Don't convert to string until the actual write.
				s = ','.join([nodeIndices.toString(t.fileIndex) for t in v.tnodeList])
			else:
				s = ','.join([str(t.fileIndex) for t in v.tnodeList])
			# trace(s)
			fc.put(s) ; fc.put_dquote()
	#@nonl
	#@-node:putTnodeList (4.0)
	#@+node:putTnodes
	def putTnodes (self):
		
		"""Puts all tnodes as required for copy or save commands"""
	
		c = self.c
		if self.usingClipboard: # write the current tree.
			v = c.currentVnode() ; after = v.nodeAfterTree()
		else: # write everything
			v = c.rootVnode() ; after = None
	
		self.put("<tnodes>") ; self.put_nl()
		#@	<< write only those tnodes that were referenced >>
		#@+node:<< write only those tnodes that were referenced >>
		# Populate tnodes
		tnodes = {}
		while v and v != after:
			index = v.t.fileIndex
			if index > 0 and not tnodes.has_key(index):
				tnodes[index] = v.t
			v = v.threadNext()
		
		# Put all tnodes in index order.
		keys = tnodes.keys() ; keys.sort()
		for index in keys:
			t = tnodes[index]
			assert(t)
			# Write only those tnodes whose vnodes were written.
			if t.isVisited(): self.putTnode(t)
		#@nonl
		#@-node:<< write only those tnodes that were referenced >>
		#@nl
		self.put("</tnodes>") ; self.put_nl()
	#@nonl
	#@-node:putTnodes
	#@+node:putVnode (3.x and 4.x)
	def putVnode (self,v,topVnode):
	
		"""Write a <v> element corresponding to a vnode."""
	
		fc = self ; c = fc.c
		fc.put("<v")
		#@	<< Put tnode index >>
		#@+node:<< Put tnode index >>
		if v.t.fileIndex:
			if app.use_gnx:
				gnx = app.nodeIndices.toString(v.t.fileIndex)
				fc.put(" t=") ; fc.put_in_dquotes(gnx)
			else:
				fc.put(" t=") ; fc.put_in_dquotes("T" + `v.t.fileIndex`)
			v.t.setVisited() # Indicate we wrote the body text.
		else:
			trace(v.t.fileIndex,v)
			es("error writing file(bad v.t.fileIndex)!")
			es("try using the Save To command")
		#@nonl
		#@-node:<< Put tnode index >>
		#@nl
		#@	<< Put attribute bits >>
		#@+node:<< Put attribute bits >>
		current = c.currentVnode()
		top = topVnode
		if ( v.isCloned() or v.isExpanded() or v.isMarked() or
			v == current or v == top ):
			fc.put(" a=") ; fc.put_dquote()
			if 0: # 10/25/03: Clone bits are never used.
				if v.isCloned(): fc.put("C")
			if v.isExpanded(): fc.put("E")
			if v.isMarked(): fc.put("M")
			if v.isOrphan(): fc.put("O")
			if v == top: fc.put("T")
			if v == current: fc.put("V")
			fc.put_dquote()
		#@nonl
		#@-node:<< Put attribute bits >>
		#@nl
		# 12/13/03 Write tnodeList only for @file nodes.
		if hasattr(v,"tnodeList") and len(v.tnodeList) > 0 and v.isAnyAtFileNode():
			fc.putTnodeList(v) # New in 4.0
		if hasattr(v,"unknownAttributes"): # New in 4.0
			#@		<< put unknown vnode attributes >>
			#@+node:<< put unknown vnode attributes >>
			attrDict = v.unknownAttributes
			keys = attrDict.keys()
			for key in keys:
				val = attrDict[key]
				attr = ' %s="%s"' % (key,self.xmlEscape(val))
				self.put(attr)
				if 0: # For debugging.
					s = "putting unknown attribute for " + v.headString()
					print s ;  es(s, color="red")
					print attr, es(attr)
			#@nonl
			#@-node:<< put unknown vnode attributes >>
			#@nl
		fc.put(">")
		#@	<< write the head text >>
		#@+node:<< write the head text >>
		headString = v.headString()
		if len(headString) > 0:
			fc.put("<vh>")
			fc.putEscapedString(headString)
			fc.put("</vh>")
		#@nonl
		#@-node:<< write the head text >>
		#@nl
		child = v.firstChild()
		if child:
			fc.put_nl()
			while child:
				fc.putVnode(child,topVnode)
				child = child.next()
		fc.put("</v>") ; fc.put_nl()
	#@nonl
	#@-node:putVnode (3.x and 4.x)
	#@+node:putVnodes
	def putVnodes (self):
	
		"""Puts all <v> elements in the order in which they appear in the outline."""
	
		c = self.c
		c.clearAllVisited()
	
		self.put("<vnodes>") ; self.put_nl()
		if self.usingClipboard:
			self.putVnode(
				c.currentVnode(), # Write only current tree.
				None) # Don't write top vnode status bit.
		else: 
			v = c.rootVnode()
			while v:
				self.putVnode(
					v, # Write the next top-level node.
					c.frame.tree.topVnode()) # Write the top-vnode status bit.
				v = v.next()
		self.put("</vnodes>") ; self.put_nl()
	#@nonl
	#@-node:putVnodes
	#@+node:save
	def save(self,fileName):
	
		c = self.c ; v = c.currentVnode()
	
		if not doHook("save1",c=c,v=v,fileName=fileName):
			c.beginUpdate()
			c.endEditing()# Set the current headline text.
			self.compactFileIndices()
			self.setDefaultDirectoryForNewFiles(fileName)
			if self.write_LEO_file(fileName,false): # outlineOnlyFlag
				c.setChanged(false) # Clears all dirty bits.
				es("saved: " + shortFileName(fileName))
				if app.config.save_clears_undo_buffer:
					es("clearing undo")
					c.undoer.clearUndoState()
			c.endUpdate()
		doHook("save2",c=c,v=v,fileName=fileName)
	#@nonl
	#@-node:save
	#@+node:saveAs
	def saveAs(self,fileName):
	
		c = self.c ; v = c.currentVnode()
	
		if not doHook("save1",c=c,v=v,fileName=fileName):
			c.beginUpdate()
			c.endEditing() # Set the current headline text.
			self.compactFileIndices()
			self.setDefaultDirectoryForNewFiles(fileName)
			if self.write_LEO_file(fileName,false): # outlineOnlyFlag
				c.setChanged(false) # Clears all dirty bits.
				es("saved: " + shortFileName(fileName))
			c.endUpdate()
		doHook("save2",c=c,v=v,fileName=fileName)
	#@-node:saveAs
	#@+node:saveTo
	def saveTo (self,fileName):
	
		c = self.c ; v = c.currentVnode()
	
		if not doHook("save1",c=c,v=v,fileName=fileName):
			c.beginUpdate()
			c.endEditing()# Set the current headline text.
			self.compactFileIndices()
			self.setDefaultDirectoryForNewFiles(fileName)
			if self.write_LEO_file(fileName,false): # outlineOnlyFlag
				es("saved: " + shortFileName(fileName))
			c.endUpdate()
		doHook("save2",c=c,v=v,fileName=fileName)
	#@-node:saveTo
	#@+node:setDefaultDirectoryForNewFiles
	def setDefaultDirectoryForNewFiles (self,fileName):
		
		"""Set c.openDirectory for new files for the benefit of leoAtFile.scanAllDirectives."""
		
		c = self.c
	
		if not c.openDirectory or len(c.openDirectory) == 0:
			dir = os_path_dirname(fileName)
	
			if len(dir) > 0 and os_path_isabs(dir) and os_path_exists(dir):
				c.openDirectory = dir
	#@nonl
	#@-node:setDefaultDirectoryForNewFiles
	#@+node:write_LEO_file
	def write_LEO_file(self,fileName,outlineOnlyFlag):
	
		c = self.c ; config = app.config
	
		if not outlineOnlyFlag:
			try:
				# Leo2: write all @file nodes and set orphan bits.
				at = c.atFileCommands
				at.writeAll()
			except:
				es_error("exception writing derived files")
				es_exception()
				return false
				
		if self.read_only:
			es_error("read only: " + fileName)
			return false
	
		try:
			#@		<< create backup file >>
			#@+node:<< create backup file >> in write_LEO_file
			# rename fileName to fileName.bak if fileName exists.
			if os_path_exists(fileName):
				try:
					backupName = os_path_join(app.loadDir,fileName)
					backupName = fileName + ".bak"
					if os_path_exists(backupName):
						os.unlink(backupName)
					# os.rename(fileName,backupName)
					utils_rename(fileName,backupName)
				except:
					es("exception creating " + backupName)
					es_exception()
					backupName = None
			else:
				backupName = None
			#@nonl
			#@-node:<< create backup file >> in write_LEO_file
			#@nl
			self.mFileName = fileName
			self.outputFile = open(fileName, 'wb') # 9/18/02
			if not self.outputFile:
				es("can not open " + fileName)
				#@			<< delete backup file >>
				#@+node:<< delete backup file >>
				if backupName and os_path_exists(backupName):
					try:
						os.unlink(backupName)
					except:
						es("exception deleting " + backupName)
						es_exception()
				#@-node:<< delete backup file >>
				#@nl
				return false
			
			# 8/6/02: Update leoConfig.txt completely here.
			c.setIvarsFromFind()
			config.setConfigFindIvars(c)
			c.setIvarsFromPrefs()
			config.setCommandsIvars(c)
			config.update()
			
			self.putProlog()
			self.putHeader()
			self.putGlobals()
			self.putPrefs()
			self.putFindSettings()
			self.putVnodes()
			self.putTnodes()
			self.putPostlog()
			# raise BadLeoFile # testing
		except:
			es("exception writing: " + fileName)
			es_exception() 
			if self.outputFile:
				try:
					self.outputFile.close()
					self.outputFile = None
				except:
					es("exception closing: " + fileName)
					es_exception()
			#@		<< erase filename and rename backupName to fileName >>
			#@+node:<< erase filename and rename backupName to fileName >>
			es("error writing " + fileName)
			
			if fileName and os_path_exists(fileName):
				try:
					os.unlink(fileName)
				except:
					es("exception deleting " + fileName)
					es_exception()
					
			if backupName:
				es("restoring " + fileName + " from " + backupName)
				try:
					# os.rename(backupName, fileName)
					utils_rename(backupName, fileName)
				except:
					es("exception renaming " + backupName + " to " + fileName)
					es_exception()
			#@-node:<< erase filename and rename backupName to fileName >>
			#@nl
			return false
	
		if self.outputFile:
			try:
				self.outputFile.close()
				self.outputFile = None
			except:
				es("exception closing: " + fileName)
				es_exception()
			#@		<< delete backup file >>
			#@+node:<< delete backup file >>
			if backupName and os_path_exists(backupName):
				try:
					os.unlink(backupName)
				except:
					es("exception deleting " + backupName)
					es_exception()
			#@-node:<< delete backup file >>
			#@nl
			return true
		else: # This probably will never happen because errors should raise exceptions.
			#@		<< erase filename and rename backupName to fileName >>
			#@+node:<< erase filename and rename backupName to fileName >>
			es("error writing " + fileName)
			
			if fileName and os_path_exists(fileName):
				try:
					os.unlink(fileName)
				except:
					es("exception deleting " + fileName)
					es_exception()
					
			if backupName:
				es("restoring " + fileName + " from " + backupName)
				try:
					# os.rename(backupName, fileName)
					utils_rename(backupName, fileName)
				except:
					es("exception renaming " + backupName + " to " + fileName)
					es_exception()
			#@-node:<< erase filename and rename backupName to fileName >>
			#@nl
			return false
	#@nonl
	#@-node:write_LEO_file
	#@+node:writeAtFileNodes
	def writeAtFileNodes (self):
		
		c = self.c
	
		changedFiles = c.atFileCommands.writeAll(writeAtFileNodesFlag=true)
		assert(changedFiles != None)
		if changedFiles:
			es("auto-saving outline",color="blue")
			c.save() # Must be done to set or clear tnodeList.
	#@nonl
	#@-node:writeAtFileNodes
	#@+node:writeDirtyAtFileNodes
	def writeDirtyAtFileNodes (self): # fileCommands
	
		"""The Write Dirty @file Nodes command"""
		
		c = self.c
	
		changedFiles = c.atFileCommands.writeAll(writeDirtyAtFileNodesFlag=true)
		
		assert(changedFiles != None)
		if changedFiles:
			es("auto-saving outline",color="blue")
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
				es("auto-saving outline",color="blue")
				c.save() # Must be done to set or clear tnodeList.
	#@nonl
	#@-node:writeMissingAtFileNodes
	#@+node:writeOutlineOnly
	def writeOutlineOnly (self):
	
		c = self.c
		c.endEditing()
		self.compactFileIndices()
		self.write_LEO_file(self.mFileName,true) # outlineOnlyFlag
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
#@nonl
#@-node:@file leoFileCommands.py
#@-leo
